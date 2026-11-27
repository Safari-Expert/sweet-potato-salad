#!/usr/bin/env python3
"""Read-only offline preflight; does not import, repair, or certify supplier data."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median

TYPES = ('activity', 'flight', 'transfer', 'location', 'hotel', 'addon')
COMMON = 'min_age max_age cost currency start_date end_date'.split()
REQUIRED = {
    'activity': 'location_name activity_name activity_desc activity_duration_min margin group_flg max_cap min_pax max_pax',
    'flight': 'airline_name margin src_location_name dest_location_name dep_time arr_time frequency min_pax max_pax',
    'transfer': 'vehicle_name margin max_cap transfer_type min_pax max_pax',
    'location': 'location_name contract_type overnight camping',
    'hotel': 'location_name hotel_name hotel_desc inside_restricted_area margin room_name room_desc max_cap min_pax max_pax',
    'addon': 'addon_name addon_desc addon_sub addon_type addon_price_type margin min_pax max_pax',
}
INTEGERS = set('min_age max_age min_pax max_pax max_cap activity_duration_min'.split())
MONEY = set('cost single_supplement hb_supplement fb_supplement ai_supplement overnight camping'.split())
NUMERIC = INTEGERS | MONEY | {'margin', 'tax'}
BOOLEANS = {'group_flg', 'ignore_proposal_margin', 'inside_restricted_area'}
LIMITS = {'activity_desc': 380, 'hotel_desc': 380, 'room_desc': 480}
UPLOAD_BYTES = {'hotel': 8 * 1024 * 1024, 'flight': 5 * 1024 * 1024}
DATA_ROWS = {'flight': 3000}
HOTEL_BOARDS = ('hb_supplement', 'fb_supplement', 'ai_supplement')
HOTEL_FLAGS = ('inside_restricted_area', 'ignore_proposal_margin')
HOTEL_SUPPLEMENTS = {'single_supplement', *HOTEL_BOARDS}
MASTER_FIELDS = {
    'activity': 'activity_desc activity_duration_min margin tax ignore_proposal_margin group_flg max_cap',
    'flight': 'airline_desc margin tax ignore_proposal_margin',
    'transfer': 'margin tax ignore_proposal_margin max_cap',
    'hotel': 'hotel_group hotel_desc inside_restricted_area margin tax ignore_proposal_margin',
    'addon': 'addon_sub addon_desc margin tax ignore_proposal_margin feature_1 feat_desc_1 feature_2 feat_desc_2 feature_3 feat_desc_3 feature_4 feat_desc_4',
    'location': '',
}


def template_header(path: Path, delimiter: str = ',') -> list[str]:
    if path.suffix.lower() == '.xlsx':
        from openpyxl import load_workbook
        book = load_workbook(path, read_only=True, data_only=True)
        try:
            row = next(book.worksheets[0].iter_rows(values_only=True), ())
            return ['' if value is None else str(value) for value in row]
        finally:
            book.close()
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return next(csv.reader(handle, delimiter=delimiter, strict=True), [])


def effective_header(kind: str, header: list[str]) -> list[str]:
    """Apply current hotel board-column policy without changing other column order."""
    if kind != 'hotel':
        return header.copy()
    board_positions = [i for i, field in enumerate(header) if field in HOTEL_BOARDS]
    if board_positions:
        index = sum(field not in HOTEL_BOARDS for field in header[:min(board_positions)])
    elif 'single_supplement' in header:
        index = header.index('single_supplement') + 1
    elif 'cost' in header:
        index = header.index('cost') + 1
    else:
        index = header.index('start_date') if 'start_date' in header else len(header)
    result = [field for field in header if field not in HOTEL_BOARDS]
    result[index:index] = HOTEL_BOARDS
    return result


def hotel_flag_policy(overrides: dict | None) -> dict[str, str]:
    """An explicit, documented task choice can override a default hotel flag."""
    values = dict.fromkeys(HOTEL_FLAGS, 'FALSE')
    if overrides is None:
        return values
    if not isinstance(overrides, dict) or set(overrides) - set(HOTEL_FLAGS):
        raise ValueError('Hotel flag policy must contain only known hotel flag names')
    for field, choice in overrides.items():
        if (not isinstance(choice, dict) or set(choice) != {'value', 'reason'} or
                choice['value'] not in ('TRUE', 'FALSE') or
                not isinstance(choice['reason'], str) or not choice['reason'].strip()):
            raise ValueError('Each hotel flag override requires value TRUE/FALSE and an explicit reason')
        values[field] = choice['value']
    return values


def identity(kind: str, row: dict, currency: bool = False) -> tuple:
    keys = {
        'activity': ['location_name', 'activity_name'],
        'flight': ['airline_name'],
        'transfer': ['vehicle_name'],
        'hotel': ['location_name', 'hotel_name'],
        'addon': ['addon_name', 'addon_type', 'addon_price_type'] if currency else ['addon_name'],
        'location': ['location_name'],
    }[kind].copy()
    if not currency:
        if kind == 'flight':
            keys += ['src_location_name', 'dest_location_name', 'dep_time', 'arr_time']
        elif kind == 'transfer':
            keys += ['src_location_name', 'dest_location_name', 'transfer_type']
        elif kind == 'hotel':
            keys += ['room_name']
        elif kind == 'location':
            keys += ['contract_type']
            if row.get('contract_type') == 'group':
                keys += ['description']
    values = []
    for key in keys:
        value = row.get(key, '').strip().casefold()
        if currency:
            value = ' '.join(value.split())
        if key in ('dep_time', 'arr_time') and re.fullmatch(r'\d{1,2}:\d{2}', value):
            hour, minute = value.split(':')
            value = f'{int(hour):02}:{minute}'
        values.append(value)
    return tuple(values)


def preflight(kind: str, path: Path, template: Path, location_ref: Path | None = None,
              delimiter: str = ',', *, hotel_flag_overrides: dict | None = None) -> dict:
    errors, review = [], []

    def issue(target, code, row=0, field=None, **details):
        item = {'code': code, 'row': row}
        if field:
            item['field'] = field
        item.update(details)
        target.append(item)

    expected = template_header(template, delimiter)
    if not expected or '' in expected or len(set(expected)) != len(expected):
        raise ValueError('Template header is empty, contains blanks, or has duplicate fields')
    expected = effective_header(kind, expected)
    flag_values = hotel_flag_policy(hotel_flag_overrides) if kind == 'hotel' else {}
    if kind != 'hotel' and hotel_flag_overrides is not None:
        raise ValueError('Hotel flag overrides apply only to hotel files')
    with path.open(encoding='utf-8-sig', newline='') as handle:
        matrix = list(csv.reader(handle, delimiter=delimiter, strict=True))
    header = matrix[0] if matrix else []
    if path.stat().st_size > UPLOAD_BYTES.get(kind, 2 * 1024 * 1024):
        issue(errors, 'upload_too_large', limit=UPLOAD_BYTES.get(kind, 2 * 1024 * 1024))
    if any(len(cells) > 30 for cells in matrix):
        issue(errors, 'column_limit_exceeded', limit=30)
    if header != expected:
        issue(errors, 'header_mismatch', expected=expected, actual=header)
    if kind == 'hotel':
        for field in (*HOTEL_BOARDS, *HOTEL_FLAGS, 'single_supplement'):
            if field not in header:
                issue(errors, 'hotel_required_header_missing', field=field)
    refs = None
    if location_ref:
        entries = json.loads(location_ref.read_text(encoding='utf-8-sig'))
        if not isinstance(entries, list) or any(not isinstance(x, dict) or not isinstance(x.get('location_name'), str) or not x['location_name'] for x in entries):
            raise ValueError('Location reference must be a JSON list with nonempty location_name values')
        refs = Counter(x['location_name'] for x in entries)
    elif kind != 'addon':
        issue(review, 'location_reference_not_checked')

    seen, currencies, caps, groups, routes = {}, defaultdict(set), defaultdict(set), defaultdict(list), set()
    metadata = {}
    room_metadata = {}
    room_aliases = defaultdict(lambda: defaultdict(list))
    raw_names, rooms = defaultdict(set), defaultdict(lambda: defaultdict(list))
    records = []
    for rownum, cells in enumerate(matrix[1:], 2):
        if not cells or not any(cells):
            issue(review, 'blank_row', rownum)
            continue
        if len(cells) != len(header):
            issue(errors, 'row_width', rownum, expected=len(header), actual=len(cells))
            continue
        row = dict(zip(header, cells))
        records.append((rownum, row))
        fingerprint = tuple(cell.strip() for cell in cells)
        if fingerprint in seen:
            issue(errors, 'duplicate_row', rownum, other_row=seen[fingerprint])
        seen[fingerprint] = rownum
        for field in COMMON + REQUIRED[kind].split():
            if not row.get(field, '').strip():
                issue(errors, 'required_field_missing', rownum, field)
        values = {}
        for field, raw in row.items():
            numeric_like = bool(re.fullmatch(r'[+-]?\d+(?:\.\d+)?', raw.strip()))
            if len(raw) > LIMITS.get(field, 50 if numeric_like else 500):
                issue(errors, 'cell_too_long', rownum, field)
            if raw and raw != raw.strip():
                issue(review, 'outer_whitespace', rownum, field)
            if field in BOOLEANS and raw and raw not in ('TRUE', 'FALSE'):
                issue(errors, 'boolean_style', rownum, field)
            if kind == 'hotel' and field in HOTEL_FLAGS and raw != flag_values[field]:
                issue(errors, 'hotel_flag_policy', rownum, field, expected=flag_values[field])
            if field not in NUMERIC or raw == '':
                continue
            try:
                value = Decimal(raw)
                if not value.is_finite() or value < 0:
                    raise InvalidOperation
                if not re.fullmatch(r'\d+(?:\.\d+)?', raw):
                    raise InvalidOperation
                values[field] = value
                if kind == 'hotel' and field in MONEY and value.as_tuple().exponent < -2:
                    issue(errors, 'hotel_money_precision', rownum, field, max_decimals=2)
                if kind == 'hotel' and field in HOTEL_SUPPLEMENTS and value == 0 and raw != '0':
                    issue(errors, 'hotel_zero_supplement_style', rownum, field, expected='0')
                if kind == 'hotel' and field == 'tax' and value != 0:
                    issue(errors, 'hotel_tax_must_be_zero', rownum, field)
                if field in INTEGERS and value != value.to_integral_value():
                    issue(errors, 'fractional_integer', rownum, field)
                if field in ('margin', 'tax') and value > 1:
                    issue(errors, 'fractional_rate_out_of_range', rownum, field)
                if field in ('min_age', 'max_age') and value > 999:
                    issue(errors, 'age_out_of_range', rownum, field)
                if kind == 'hotel' and field in ('min_pax', 'max_pax', 'max_cap') and value < 1:
                    issue(errors, 'hotel_occupancy_must_be_positive', rownum, field)
                if kind == 'location' and field in ('overnight', 'camping') and value != value.to_integral_value():
                    issue(errors, 'location_supplement_truncation_risk', rownum, field)
            except InvalidOperation:
                issue(errors, 'invalid_number', rownum, field)
        for lower, upper in [('min_age', 'max_age'), ('min_pax', 'max_pax')]:
            if lower in values and upper in values and values[lower] > values[upper]:
                issue(errors, 'reversed_range', rownum, lower)
        if 'max_cap' in values and 'max_pax' in values:
            if kind in ('activity', 'transfer') and values['max_pax'] > values['max_cap']:
                issue(errors, 'capacity_exceeded', rownum, 'max_pax')
            if kind == 'hotel' and values['max_pax'] != values['max_cap']:
                issue(errors, 'hotel_capacity_mismatch', rownum, 'max_pax')
        if kind in ('transfer', 'hotel') and 'max_cap' in values:
            capkey = identity(kind, row, currency=True)
            if kind == 'hotel':
                capkey += (row.get('room_name', '').casefold(),)
            caps[capkey].add(values['max_cap'])

        dates = {}
        date_format = '%Y-%m-%d' if kind == 'hotel' else '%d/%m/%Y'
        date_pattern = r'\d{4}-\d{2}-\d{2}' if kind == 'hotel' else r'\d{2}/\d{2}/\d{4}'
        for field in ('start_date', 'end_date'):
            raw = row.get(field, '')
            try:
                if not re.fullmatch(date_pattern, raw):
                    raise ValueError
                dates[field] = datetime.strptime(raw, date_format).date()
            except ValueError:
                issue(errors, 'invalid_date', rownum, field)
        if len(dates) == 2 and (dates['start_date'] > dates['end_date'] or
                              (kind != 'hotel' and dates['start_date'] == dates['end_date'])):
            issue(errors, 'invalid_date_order', rownum)
        if kind == 'hotel':
            if 'tax' in header and row.get('tax', '') == '':
                issue(errors, 'hotel_tax_must_be_zero', rownum, 'tax')
            if not row.get('single_supplement', '').strip():
                issue(errors, 'required_field_missing', rownum, 'single_supplement')
        currency = row.get('currency', '')
        if currency and not re.fullmatch(r'[A-Z]{3}', currency):
            issue(errors, 'currency_format', rownum, 'currency')
        currencies[identity(kind, row, currency=True)].add(currency)
        masterkey = identity(kind, row, currency=True)
        name_fields = {
            'activity': ('activity_name',), 'flight': ('airline_name',),
            'transfer': ('vehicle_name',), 'hotel': ('hotel_name',),
            'addon': ('addon_name', 'addon_type', 'addon_price_type'), 'location': (),
        }[kind]
        if name_fields:
            raw_names[masterkey].add(tuple(row.get(k, '').strip() for k in name_fields))
        if kind == 'hotel':
            raw_room = row.get('room_name', '').strip()
            alias_key = masterkey + (' '.join(raw_room.casefold().split()),)
            room_aliases[alias_key][raw_room].append(rownum)
            rooms[masterkey][row.get('room_name', '').strip().casefold()].append(rownum)
            roomkey = masterkey + (row.get('room_name', '').strip().casefold(),)
            room_signature = (row.get('room_name', '').strip(), row.get('room_desc', '').strip())
            if roomkey in room_metadata and room_metadata[roomkey][0] != room_signature:
                issue(review, 'room_metadata_drift', rownum, other_row=room_metadata[roomkey][1])
            else:
                room_metadata.setdefault(roomkey, (room_signature, rownum))
        signature = tuple(row.get(k, '').strip() for k in MASTER_FIELDS[kind].split())
        if masterkey in metadata and metadata[masterkey][0] != signature:
            issue(review, 'master_metadata_drift', rownum, other_row=metadata[masterkey][1])
        else:
            metadata.setdefault(masterkey, (signature, rownum))

        for field in ('location_name', 'src_location_name', 'dest_location_name'):
            name = row.get(field, '')
            if refs is not None and name:
                if name not in refs:
                    issue(errors, 'unknown_location', rownum, field)
                elif refs[name] > 1:
                    issue(errors, 'ambiguous_location', rownum, field)
        if kind == 'location':
            contract_type, description = row.get('contract_type'), row.get('description', '')
            if contract_type not in ('person', 'group'):
                issue(errors, 'invalid_contract_type', rownum, 'contract_type')
            if contract_type == 'group' and not description.strip():
                issue(errors, 'group_description_required', rownum, 'description')
            if contract_type == 'person' and description:
                issue(errors, 'person_description_not_allowed', rownum, 'description')
            if values.get('tax', Decimal(0)) != 0:
                issue(review, 'location_tax_not_preserved', rownum, 'tax')
        if kind == 'transfer':
            transfer_type = row.get('transfer_type')
            if transfer_type not in ('taxi', 'daily'):
                issue(errors, 'invalid_transfer_type', rownum, 'transfer_type')
            src, dst = row.get('src_location_name', ''), row.get('dest_location_name', '')
            if transfer_type == 'daily' and (src or dst):
                issue(errors, 'daily_routes_must_be_blank', rownum)
            if transfer_type == 'taxi':
                if not src or not dst:
                    issue(errors, 'route_endpoint_missing', rownum)
                routes.add((row.get('vehicle_name', ''), src, dst, row.get('start_date'), row.get('end_date'), row.get('min_pax'), row.get('max_pax')))
            if row.get('min_age') != '0' or row.get('max_age') != '99':
                issue(review, 'transfer_age_policy', rownum)
        if kind == 'flight':
            frequency = row.get('frequency', '')
            tokens = frequency.rstrip(',').split(',')
            if not tokens or any(x not in '1234567' or len(x) != 1 for x in tokens) or len(tokens) != len(set(tokens)) or frequency.endswith(',,'):
                issue(errors, 'invalid_weekdays', rownum, 'frequency')
            for field in ('dep_time', 'arr_time'):
                raw = row.get(field, '')
                if not re.fullmatch(r'(?:[01]?\d|2[0-3]):[0-5]\d', raw):
                    issue(errors, 'invalid_time', rownum, field)
        if kind == 'addon':
            if row.get('addon_price_type', '') not in ('person', 'group'):
                issue(review, 'unverified_addon_price_type', rownum, 'addon_price_type')
            for index in range(1, 5):
                if bool(row.get(f'feature_{index}', '').strip()) != bool(row.get(f'feat_desc_{index}', '').strip()):
                    issue(errors, 'incomplete_feature_pair', rownum, f'feature_{index}')

        if len(dates) == 2 and all(k in values for k in ('min_age', 'max_age')):
            if kind == 'location':
                values['min_pax'], values['max_pax'] = Decimal(0), Decimal(99)
            if all(k in values for k in ('min_pax', 'max_pax')):
                groups[identity(kind, row)].append({'row': rownum, **dates, **values})

    if not records:
        issue(errors, 'no_data_rows')
    if len(records) > DATA_ROWS.get(kind, 1000):
        issue(errors, 'row_limit_exceeded', limit=DATA_ROWS.get(kind, 1000))
    for key, names in raw_names.items():
        if len(names) > 1:
            issue(review, 'master_name_spelling_drift', group=list(key), names=sorted(names))
    for key, variants in room_aliases.items():
        if len(variants) > 1:
            issue(errors, 'room_name_alias_collision', group=list(key),
                  variants=dict(variants), action='Resolve exact room identity; do not automatically merge')
    for key, room_rows in rooms.items():
        counts = [len(rows) for rows in room_rows.values()]
        if len(counts) < 2:
            continue
        typical = max(counts) if len(counts) == 2 else median(counts)
        for room, rownums in room_rows.items():
            count = len(rownums)
            if count < typical * 0.25 or (len(counts) >= 3 and count > typical * 1.5):
                issue(review, 'room_name_outlier', rownums[0], 'room_name',
                      group=list(key), room=room, rows=rownums, count=count,
                      expected_min=typical * 0.25, expected_max=typical * 1.5)
    for key, codes in currencies.items():
        if len(codes) > 1:
            issue(errors, 'mixed_master_currency', group=list(key))
    for key, capacities in caps.items():
        if len(capacities) > 1:
            issue(errors, 'inconsistent_capacity', group=list(key))
    for group, entries in groups.items():
        ordered = sorted(entries, key=lambda e: e['start_date'])
        for i, left in enumerate(ordered):
            for right in ordered[i + 1:]:
                if right['start_date'] > left['end_date']:
                    break
                if all(left[lo] <= right[hi] and right[lo] <= left[hi] for lo, hi in [('min_age', 'max_age'), ('min_pax', 'max_pax')]):
                    same_pax = all(left[k] == right[k] for k in ('min_pax', 'max_pax'))
                    issue(errors if same_pax else review,
                          'overlapping_rules' if same_pax else 'intersecting_pax_bands',
                          right['row'], other_row=left['row'], group=list(group))
        seasons, ages = defaultdict(list), defaultdict(list)
        for entry in entries:
            seasons[tuple(entry[k] for k in ('min_age', 'max_age', 'min_pax', 'max_pax'))].append(entry)
            ages[tuple(entry[k] for k in ('start_date', 'end_date', 'min_pax', 'max_pax'))].append(entry)
        for band_key, band in seasons.items():
            band.sort(key=lambda e: e['start_date'])
            covered, previous = band[0]['end_date'], band[0]
            for right in band[1:]:
                if (right['start_date'] - covered).days > 1:
                    issue(review, 'season_gap', right['row'], other_row=previous['row'],
                          group=list(group), age_band=[int(x) for x in band_key[:2]],
                          pax_band=[int(x) for x in band_key[2:]],
                          gap_start=(covered + timedelta(days=1)).strftime(date_format),
                          gap_end=(right['start_date'] - timedelta(days=1)).strftime(date_format))
                if right['end_date'] > covered:
                    covered, previous = right['end_date'], right
        for band in ages.values():
            band.sort(key=lambda e: e['min_age'])
            covered = band[0]['max_age']
            for entry in band[1:]:
                if entry['min_age'] > covered + 1:
                    issue(review, 'age_gap', entry['row'], group=list(group),
                          missing_ages=[int(covered + 1), int(entry['min_age'] - 1)],
                          pax_band=[int(entry[k]) for k in ('min_pax', 'max_pax')],
                          start_date=entry['start_date'].strftime(date_format),
                          end_date=entry['end_date'].strftime(date_format))
                covered = max(covered, entry['max_age'])
    for vehicle, src, dst, start, end, low, high in routes:
        if (vehicle, dst, src, start, end, low, high) not in routes:
            issue(review, 'reverse_transfer_missing', vehicle=vehicle, origin=src, destination=dst)
    return {'status': 'fail' if errors else 'review' if review else 'pass',
            'scope': 'offline preflight only; supplier evidence and target-state validation still required',
            'type': kind, 'rows': len(records), 'errors': errors, 'review': review}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--type', choices=TYPES, required=True)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--location-ref', type=Path)
    parser.add_argument('--delimiter', default=',', choices=[',', ';', '|'])
    parser.add_argument('--hotel-flag-policy', type=Path,
                        help='JSON of explicit flag choices: {field: {value: "TRUE", reason: "user instruction"}}')
    parser.add_argument('--report', type=Path)
    parser.add_argument('csv_path', type=Path)
    args = parser.parse_args()
    if args.report:
        for source in (args.csv_path, args.template, args.location_ref, args.hotel_flag_policy):
            if source and (args.report.resolve() == source.resolve() or
                           (args.report.exists() and source.exists() and args.report.samefile(source))):
                parser.error('Report must not overwrite an input, template, or reference')
    try:
        overrides = (json.loads(args.hotel_flag_policy.read_text(encoding='utf-8-sig'))
                     if args.hotel_flag_policy else None)
        result = preflight(args.type, args.csv_path, args.template, args.location_ref, args.delimiter,
                           hotel_flag_overrides=overrides)
        encoded = json.dumps(result, indent=2, ensure_ascii=False)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(encoded + '\n', encoding='utf-8')
        print(encoded)
        return 1 if result['status'] == 'fail' else 2 if result['status'] == 'review' else 0
    except (OSError, ValueError, csv.Error, ImportError) as exc:
        print(json.dumps({'status': 'error', 'message': str(exc)}))
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
