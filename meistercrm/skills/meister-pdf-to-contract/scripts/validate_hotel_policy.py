#!/usr/bin/env python3
"""Read-only hotel policy checks against a source-reviewed, exact-file manifest.

This verifies declared decisions; it does not establish their supplier truth or
replace CSV preflight, PDF review, target-state validation, or live price checks.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

SUPPLEMENTS = ('single_supplement', 'hb_supplement', 'fb_supplement', 'ai_supplement')
MATCH_FIELDS = ('location_name', 'hotel_name', 'room_name', 'currency',
                'start_date', 'end_date', 'min_pax', 'max_pax', 'max_cap')
ROLES = {'adult', 'paying_child', 'paying_guest', 'free'}


def money(value) -> Decimal:
    if not isinstance(value, str) or not value:
        raise ValueError('Money must be a nonempty decimal string')
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid money') from exc
    if not parsed.is_finite() or parsed < 0:
        raise ValueError('Money must be finite and nonnegative')
    return parsed


def validate_policy(csv_path: Path, manifest: dict | None, delimiter: str = ',') -> dict:
    errors, review = [], []

    def issue(code, row=0, **details):
        errors.append({'code': code, 'row': row, **details})

    with csv_path.open(encoding='utf-8-sig', newline='') as handle:
        matrix = list(csv.reader(handle, delimiter=delimiter, strict=True))
    header = matrix[0] if matrix else []
    records = {i: dict(zip(header, cells)) for i, cells in enumerate(matrix[1:], 2)
               if cells and any(cells)}

    def result():
        return {'status': 'fail' if errors else 'review' if review else 'pass',
                'scope': 'Source-reviewed manifest consistency only; PDF truth, CSV preflight and target-state checks remain separate',
                'source_policy_checked': bool(manifest is not None and not errors),
                'rows': len(records), 'errors': errors, 'review': review}

    if manifest is None:
        review.append({'code': 'hotel_source_policy_not_checked', 'row': 0,
                       'reason': 'No grounded policy manifest supplied; do not infer adult roles or Single/AI policy from names or ages'})
        return result()
    if (not isinstance(manifest, dict) or set(manifest) != {'version', 'csv_sha256', 'rows'} or
            type(manifest.get('version')) is not int or manifest.get('version') != 1):
        issue('invalid_policy_manifest', reason='Expected version 1, csv_sha256 and rows')
        return result()
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if manifest.get('csv_sha256') != digest:
        issue('policy_csv_hash_mismatch', expected=manifest.get('csv_sha256'), actual=digest)
        return result()
    if (not header or len(set(header)) != len(header) or
            not set((*MATCH_FIELDS, 'cost', *SUPPLEMENTS)).issubset(header) or
            any(len(cells) != len(header) for cells in matrix[1:] if cells and any(cells))):
        issue('policy_csv_structure_invalid', reason='Run CSV preflight; required fields, unique headers and row widths are required')
        return result()
    if not records:
        issue('no_data_rows')
        return result()
    if not isinstance(manifest['rows'], list):
        issue('invalid_policy_manifest', reason='rows must be a list')
        return result()

    decisions = {}
    required = {'row', 'role', 'quoted_single', 'ai_only', 'expected_cost', 'evidence'}
    for decision in manifest['rows']:
        if (not isinstance(decision, dict) or not required.issubset(decision) or
                set(decision) - required - {'adult_row'} or type(decision.get('row')) is not int or
                not isinstance(decision.get('role'), str) or decision.get('role') not in ROLES or
                type(decision.get('quoted_single')) is not bool or type(decision.get('ai_only')) is not bool or
                not isinstance(decision.get('evidence'), str) or not decision['evidence'].strip()):
            issue('invalid_policy_row', reason='Each row needs explicit role, boolean Single/AI decisions, expected cost and evidence')
            continue
        rownum = decision['row']
        if rownum in decisions:
            issue('duplicate_policy_row', rownum)
        decisions[rownum] = decision
        try:
            money(decision['expected_cost'])
        except ValueError:
            issue('invalid_expected_cost', rownum)
    for missing in sorted(set(records) - set(decisions)):
        issue('policy_row_missing', missing)
    for extra in sorted(set(decisions) - set(records)):
        issue('policy_row_not_in_csv', extra)
    if errors:
        return result()

    periods = {}
    for rownum, row in records.items():
        try:
            if any(not re.fullmatch(r'\d{4}-\d{2}-\d{2}', row[field]) for field in ('start_date', 'end_date')):
                raise ValueError
            start, end = (date.fromisoformat(row[field]) for field in ('start_date', 'end_date'))
            if start > end:
                raise ValueError
            periods[rownum] = (start, end)
        except ValueError:
            issue('policy_invalid_date_interval', rownum)
    if errors:
        return result()

    for rownum, row in records.items():
        decision = decisions[rownum]
        try:
            cost, expected = money(row['cost']), money(decision['expected_cost'])
            amounts = {field: money(value) for field in SUPPLEMENTS if (value := row[field]) != ''}
        except ValueError:
            issue('policy_invalid_money', rownum)
            continue
        if cost != expected:
            issue('source_expected_cost_mismatch', rownum, expected=str(expected), actual=str(cost))
        if 'single_supplement' not in amounts:
            issue('single_supplement_missing', rownum)

        if decision['ai_only']:
            if row['hb_supplement'] != '' or row['fb_supplement'] != '' or row['ai_supplement'] != '0':
                issue('ai_only_encoding', rownum, expected='HB and FB blank; AI numeric 0; full reviewed package in cost')

        if decision['role'] == 'free':
            if cost != 0:
                issue('free_row_has_cost', rownum)
            for field, amount in amounts.items():
                if amount != 0:
                    issue('free_row_has_supplement', rownum, field=field)
        elif cost <= 0:
            issue('paying_row_has_zero_cost', rownum)

        if decision['quoted_single']:
            try:
                capacity_one = all(money(row[field]) == 1 for field in ('max_cap', 'min_pax', 'max_pax'))
            except ValueError:
                capacity_one = False
            if not capacity_one:
                issue('quoted_single_capacity', rownum)
            if amounts.get('single_supplement') != 0:
                issue('quoted_single_supplement', rownum, expected='0')
        elif decision['role'] != 'free':
            adult_rownum = decision.get('adult_row')
            if decision['role'] == 'adult' and adult_rownum != rownum:
                issue('adult_row_must_reference_itself', rownum,
                      reason='An explicit adult row uses its own current cost; a discounted nonstandard guest requires its reviewed guest role')
                continue
            if (type(adult_rownum) is not int or adult_rownum not in records or
                    decisions[adult_rownum]['role'] != 'adult'):
                issue('adult_basis_missing_or_not_adult', rownum)
                continue
            adult = records[adult_rownum]
            differing = [field for field in MATCH_FIELDS
                         if field not in ('start_date', 'end_date') and row[field] != adult[field]]
            if not (periods[adult_rownum][0] <= periods[rownum][0] <= periods[rownum][1] <= periods[adult_rownum][1]):
                differing.append('adult_interval_does_not_cover_row')
            if differing or decisions[adult_rownum]['quoted_single'] or decisions[adult_rownum]['ai_only'] != decision['ai_only']:
                issue('adult_basis_scope_mismatch', rownum, adult_row=adult_rownum, fields=differing)
                continue
            try:
                adult_cost = money(adult['cost'])
            except ValueError:
                issue('adult_basis_invalid_cost', rownum, adult_row=adult_rownum)
                continue
            if adult_cost <= 0 or amounts.get('single_supplement') != adult_cost:
                issue('adult_cost_supplement_mismatch', rownum, adult_row=adult_rownum,
                      expected=str(adult_cost), actual=row['single_supplement'])
    return result()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', type=Path)
    parser.add_argument('--policy', type=Path, help='Source-reviewed version-1 manifest bound to exact CSV SHA-256')
    parser.add_argument('--delimiter', default=',', choices=[',', ';', '|'])
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report:
        for source in (args.csv_path, args.policy):
            if source and (args.report.resolve() == source.resolve() or
                           (args.report.exists() and source.exists() and args.report.samefile(source))):
                parser.error('Report must not overwrite CSV or policy evidence')
    try:
        manifest = json.loads(args.policy.read_text(encoding='utf-8-sig')) if args.policy else None
        report = validate_policy(args.csv_path, manifest, args.delimiter)
        encoded = json.dumps(report, indent=2, ensure_ascii=False)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(encoded + '\n', encoding='utf-8')
        print(encoded)
        return 1 if report['status'] == 'fail' else 2 if report['status'] == 'review' else 0
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({'status': 'error', 'message': str(exc)}))
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
