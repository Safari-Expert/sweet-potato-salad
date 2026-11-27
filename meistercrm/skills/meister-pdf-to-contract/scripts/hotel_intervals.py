"""Offline inclusive calendar primitives; no rate, season or closure inference.

CLI: python hotel_intervals.py JOB.json --output REPORT.json
JSON job schema (unknown job keys are rejected):
  {"version": 1, "operation": "union|clip|subtract|split|merge_records",
   "intervals": [{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}],
   "window": {"start_date": "...", "end_date": "..."},
   "exclusions": [{"start_date": "...", "end_date": "..."}],
   "cut_dates": ["YYYY-MM-DD"],
   "records": [{"start_date": "...", "end_date": "...", "payload": {...}}]}

Only supply inputs for the chosen operation: union needs intervals; clip also
needs window; subtract needs exclusions; split needs cut_dates. merge_records
uses records instead of intervals. Dates are inclusive and start == end is
valid. A cut date starts a new segment. Split preserves input interval identity
and adds input_index (zero based); it does not union overlapping input periods.
The other calendar operations return their sorted set union. merge_records
merges adjacent/overlapping periods ONLY for an identical, complete, type-aware
payload. Payloads permit strings, integers, booleans, null, arrays and objects;
represent noninteger decimal values as strings, not JSON numbers. This prevents
serialization from silently changing their type or precision. It preserves all
payload fields and never repairs unequal overlaps.

run_job(job) is the importable API. It returns a JSON-compatible report. No
current date, country, customer, prices, holidays or inferred closures are used.
Calendar arithmetic uses ordinals so 9999-12-31 remains a valid final date.
"""

from __future__ import annotations

import argparse
from datetime import date
import sys

from _hotel_common import distinct_paths, iso_date, load_json, write_json


def _object(value, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _range(value, name="interval"):
    value = _object(value, name)
    if set(value) != {"start_date", "end_date"}:
        raise ValueError(f"{name} requires exactly start_date and end_date")
    start = iso_date(value["start_date"]).toordinal()
    end = iso_date(value["end_date"]).toordinal()
    if start > end:
        raise ValueError(f"{name} has reversed dates")
    return start, end


def _ranges(value, name):
    if not isinstance(value, list):
        raise ValueError(f"{name} must be an array")
    return [_range(item, f"{name}[{i}]") for i, item in enumerate(value)]


def _encoded(pair):
    return {"start_date": date.fromordinal(pair[0]).isoformat(),
            "end_date": date.fromordinal(pair[1]).isoformat()}


def _union(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1] + 1:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result


def _subtract(intervals, exclusions):
    result = []
    exclusions = _union(exclusions)
    for start, end in _union(intervals):
        cursor = start
        for left, right in exclusions:
            if right < cursor:
                continue
            if left > end:
                break
            if left > cursor:
                result.append((cursor, left - 1))
            cursor = max(cursor, right + 1)
            if cursor > end:
                break
        if cursor <= end:
            result.append((cursor, end))
    return result


def _freeze(value):
    """Do not equate boolean 1, number 1, string '1', or missing keys."""
    if value is None:
        return ("null",)
    if isinstance(value, bool):
        return ("boolean", value)
    if isinstance(value, int):
        return ("integer", value)
    if isinstance(value, str):
        return ("string", value)
    if isinstance(value, list):
        return ("array", tuple(_freeze(item) for item in value))
    if isinstance(value, dict) and all(isinstance(k, str) for k in value):
        return ("object", tuple((key, _freeze(value[key])) for key in sorted(value)))
    raise ValueError("payload supports strings, integers, booleans and null; encode noninteger decimals as strings")


def run_job(job):
    job = _object(job, "job")
    if type(job.get("version")) is not int or job["version"] != 1:
        raise ValueError("version must be integer 1")
    operation = job.get("operation")
    fields = {
        "union": {"intervals"}, "clip": {"intervals", "window"},
        "subtract": {"intervals", "exclusions"},
        "split": {"intervals", "cut_dates"}, "merge_records": {"records"},
    }
    if operation not in fields:
        raise ValueError("unknown operation")
    if set(job) != fields[operation] | {"version", "operation"}:
        raise ValueError(f"{operation} requires exactly {sorted(fields[operation])}")
    result = {"version": 1, "operation": operation}
    if operation == "merge_records":
        if not isinstance(job["records"], list):
            raise ValueError("records must be an array")
        groups = {}
        for i, record in enumerate(job["records"]):
            record = _object(record, f"records[{i}]")
            if set(record) != {"start_date", "end_date", "payload"}:
                raise ValueError("each record requires exactly dates and payload")
            payload = _object(record["payload"], "payload")
            key = _freeze(payload)
            if key not in groups:
                groups[key] = (payload, [])
            groups[key][1].append(_range({k: record[k] for k in ("start_date", "end_date")}))
        merged = []
        for payload, intervals in groups.values():
            merged.extend(dict(_encoded(pair), payload=payload) for pair in _union(intervals))
        result["records"] = sorted(merged, key=lambda item: (item["start_date"], item["end_date"]))
        return result
    intervals = _ranges(job["intervals"], "intervals")
    if operation == "union":
        output = [_encoded(pair) for pair in _union(intervals)]
    elif operation == "clip":
        left, right = _range(job["window"], "window")
        output = [_encoded(pair) for pair in _union(
            [(max(start, left), min(end, right)) for start, end in intervals
             if start <= right and end >= left])]
    elif operation == "subtract":
        output = [_encoded(pair) for pair in _subtract(intervals, _ranges(job["exclusions"], "exclusions"))]
    else:
        if not isinstance(job["cut_dates"], list):
            raise ValueError("cut_dates must be an array")
        cuts = sorted({iso_date(value).toordinal() for value in job["cut_dates"]})
        output = []
        for index, (start, end) in enumerate(intervals):
            boundaries = [start] + [cut for cut in cuts if start < cut <= end] + [end + 1]
            output.extend(dict(_encoded((left, right - 1)), input_index=index)
                          for left, right in zip(boundaries, boundaries[1:]))
    result["intervals"] = output
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        distinct_paths([args.output], inputs=[args.job])
        result = run_job(load_json(args.job))
        write_json(args.output, result, protected=[args.job])
    except (ValueError, TypeError, OSError) as error:
        print(f"Invalid interval job: {error}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
