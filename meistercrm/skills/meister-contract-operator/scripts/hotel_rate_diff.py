"""Compare explicit expected/actual rate coverage offline, without modifying it.

CLI: python hotel_rate_diff.py JOB.json --output REPORT.json
Job schema:
 {"version":1, "identity_fields":["hotel_id","room_id","currency"],
  "expected":[ROW,...], "actual":[ROW,...],
  "money_fields":["cost","single_supplement","hb_supplement",
                  "fb_supplement","ai_supplement"],
  "window":{"start_date":"YYYY-MM-DD","end_date":"YYYY-MM-DD"},
  "max_cells":100000, "max_details":200}

Required: version, identity_fields, expected and actual. Other keys are optional.
ROW has every selected identity/money field plus ISO start_date/end_date and
inclusive integer min_age/max_age/min_pax/max_pax. Identity values must be exact
nonblank strings or integers; numeric identifiers are not coerced to strings.
Ages are nonnegative and pax positive. Money is a finite decimal string, integer
or null; null differs from numeric zero, and binary floats/booleans are rejected.
Money columns default to the five shown above. All must exist on every row.
Other row metadata is ignored: explicitly include every scope discriminator
(e.g. currency, customer/agreement, room identity) in identity_fields. There is
no name matching, identity inference, tax treatment, tolerance or price repair.

Within each identity the union of all date, age and pax boundaries creates a
finite cell grid. Equal split/merged coverage is equivalent; duplicate/overlapping
rows are errors even if they agree in price. Missing expected coverage and extra
actual coverage are reported. A date-only window limits both sides explicitly.
Uncovered-on-both-sides cells are ignored, not inferred closures. max_cells caps
the full grid before comparisons (1..1000000); max_details caps detail records
(1..10000). A budget failure or empty comparison is never a successful match.
Counts are comparison cells, not hotel bookings or source decision error counts.

run_job(job) returns a report. Exit 0=equivalent, 1=differences, 2=not compared
(budget/no data), 3=invalid input. Rows in details use 1-based array positions.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import sys

from _hotel_common import decimal_value, distinct_paths, iso_date, load_json, write_json


DEFAULT_MONEY = ["cost", "single_supplement", "hb_supplement", "fb_supplement", "ai_supplement"]
RANGES = {"start_date", "end_date", "min_age", "max_age", "min_pax", "max_pax"}


def _names(value, field):
    if (not isinstance(value, list) or not value or
            any(not isinstance(name, str) or not name.strip() for name in value) or
            len(set(value)) != len(value)):
        raise ValueError(f"{field} must be a nonempty array of distinct field names")
    return value


def _integer(value, name, minimum=0, maximum=None):
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{name} must be an integer within the permitted range")
    return value


def _dates(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    start = iso_date(value["start_date"]).toordinal()
    end = iso_date(value["end_date"]).toordinal()
    if start > end:
        raise ValueError(f"{label}: reversed dates")
    return start, end + 1


def _rows(raw, label, identities, money, window):
    if not isinstance(raw, list):
        raise ValueError(f"{label} must be an array")
    groups = defaultdict(list)
    for index, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{index}] must be an object")
        required = set(identities) | set(money) | RANGES
        if required - set(item):
            raise ValueError(f"{label}[{index}] missing fields: {sorted(required - set(item))}")
        key = []
        for field in identities:
            value = item[field]
            if not (type(value) is int or isinstance(value, str) and value.strip()):
                raise ValueError(f"{label}[{index}] {field}: identity must be nonblank string or integer")
            key.append((type(value).__name__, value))
        start, stop = _dates(item, f"{label}[{index}]")
        ages = (_integer(item["min_age"], "min_age"), _integer(item["max_age"], "max_age") + 1)
        pax = (_integer(item["min_pax"], "min_pax", 1), _integer(item["max_pax"], "max_pax", 1) + 1)
        if ages[0] >= ages[1] or pax[0] >= pax[1]:
            raise ValueError(f"{label}[{index}]: reversed age or pax range")
        values = {field: None if item[field] is None else decimal_value(item[field]) for field in money}
        if window:
            start, stop = max(start, window[0]), min(stop, window[1])
        if start >= stop:
            continue
        groups[tuple(key)].append({"row": index, "identity": {field: item[field] for field in identities},
                                   "date": (start, stop), "age": ages, "pax": pax, "money": values})
    return groups


def _segments(rows, dimension):
    points = sorted({point for row in rows for point in row[dimension]})
    return list(zip(points, points[1:]))


def _money(values):
    return {key: None if value is None else format(value, "f") for key, value in values.items()}


def run_job(job):
    if not isinstance(job, dict):
        raise ValueError("job must be an object")
    allowed = {"version", "identity_fields", "expected", "actual", "money_fields", "window", "max_cells", "max_details"}
    if set(job) - allowed or {"version", "identity_fields", "expected", "actual"} - set(job):
        raise ValueError("job has unknown or missing required fields")
    if type(job["version"]) is not int or job["version"] != 1:
        raise ValueError("version must be integer 1")
    identities = _names(job["identity_fields"], "identity_fields")
    money = _names(job.get("money_fields", DEFAULT_MONEY), "money_fields")
    if set(identities) & (set(money) | RANGES) or set(money) & RANGES:
        raise ValueError("identity, money and range field names must not overlap")
    max_cells = _integer(job.get("max_cells", 100000), "max_cells", 1, 1000000)
    max_details = _integer(job.get("max_details", 200), "max_details", 1, 10000)
    window = None
    if "window" in job:
        if not isinstance(job["window"], dict) or set(job["window"]) != {"start_date", "end_date"}:
            raise ValueError("window requires exactly start_date and end_date")
        window = _dates(job["window"], "window")
    expected = _rows(job["expected"], "expected", identities, money, window)
    actual = _rows(job["actual"], "actual", identities, money, window)
    # Preserve insertion order without sorting potentially mixed identity types.
    keys = list(dict.fromkeys(list(expected) + list(actual)))
    plans = []
    cells = 0
    for key in keys:
        left, right = expected.get(key, []), actual.get(key, [])
        all_rows = left + right
        dimensions = [_segments(all_rows, field) for field in ("date", "age", "pax")]
        cells += len(dimensions[0]) * len(dimensions[1]) * len(dimensions[2])
        plans.append((left, right, dimensions))
    report = {"version": 1, "identity_fields": identities, "money_fields": money,
              "input_rows": {"expected": len(job["expected"]), "actual": len(job["actual"])},
              "in_window_rows": {"expected": sum(map(len, expected.values())), "actual": sum(map(len, actual.values()))},
              "window": job.get("window"), "planned_cells": cells, "max_cells": max_cells,
              "status": "not_compared", "equivalent": None, "details": []}
    if cells > max_cells:
        report.update(status="budget_exceeded", reason="Cell budget exceeded before comparison")
        return report
    if not plans:
        report.update(status="no_data", reason="Neither side has rate coverage in the comparison window")
        return report
    counts = {name: 0 for name in ("matched_cells", "missing_cells", "unsupported_cells", "value_mismatch_cells",
                                  "expected_overlap_cells", "actual_overlap_cells", "empty_cells")}
    detail_count = 0
    details = report["details"]
    for left, right, (dates, ages, pax_values) in plans:
        identity = (left + right)[0]["identity"]
        for date_start, date_stop in dates:
            dl = [row for row in left if row["date"][0] <= date_start < row["date"][1]]
            dr = [row for row in right if row["date"][0] <= date_start < row["date"][1]]
            for age_start, age_stop in ages:
                al = [row for row in dl if row["age"][0] <= age_start < row["age"][1]]
                ar = [row for row in dr if row["age"][0] <= age_start < row["age"][1]]
                for pax_start, pax_stop in pax_values:
                    el = [row for row in al if row["pax"][0] <= pax_start < row["pax"][1]]
                    ac = [row for row in ar if row["pax"][0] <= pax_start < row["pax"][1]]
                    if not el and not ac:
                        counts["empty_cells"] += 1
                        continue
                    issues = []
                    for side, rows in (("expected", el), ("actual", ac)):
                        if len(rows) > 1:
                            kind = side + "_overlap"
                            counts[kind + "_cells"] += 1
                            issues.append(kind)
                    differences = []
                    if not el:
                        counts["unsupported_cells"] += 1
                        issues.append("unsupported")
                    elif not ac:
                        counts["missing_cells"] += 1
                        issues.append("missing")
                    elif len(el) == len(ac) == 1:
                        differences = [field for field in money if el[0]["money"][field] != ac[0]["money"][field]]
                        if differences:
                            counts["value_mismatch_cells"] += 1
                            issues.append("value_mismatch")
                        else:
                            counts["matched_cells"] += 1
                    if issues:
                        detail_count += 1
                        if len(details) < max_details:
                            details.append({"issues": issues, "identity": identity,
                                            "start_date": date.fromordinal(date_start).isoformat(),
                                            "end_date": date.fromordinal(date_stop - 1).isoformat(),
                                            "min_age": age_start, "max_age": age_stop - 1,
                                            "min_pax": pax_start, "max_pax": pax_stop - 1,
                                            "expected_rows": [row["row"] for row in el],
                                            "actual_rows": [row["row"] for row in ac],
                                            "different_fields": differences,
                                            "expected": [{"row": row["row"], "money": _money(row["money"])} for row in el],
                                            "actual": [{"row": row["row"], "money": _money(row["money"])} for row in ac]})
    report.update(counts=counts, detail_count=detail_count, details_truncated=detail_count > len(details),
                  status="different" if detail_count else "equivalent", equivalent=detail_count == 0)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        distinct_paths([args.output], inputs=[args.job])
        report = run_job(load_json(args.job))
        write_json(args.output, report, protected=[args.job])
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(f"Invalid rate comparison job: {error}", file=sys.stderr)
        return 3
    return {"equivalent": 0, "different": 1}.get(report["status"], 2)


if __name__ == "__main__":
    raise SystemExit(main())
