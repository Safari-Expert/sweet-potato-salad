"""Offline selection and comparison of explicitly supplied hotel price cases.

No ages, dates, tariff policies, source interpretations or API calls are inferred.
Money is supplied as decimal strings/integers, never binary JSON floats.

JSON job schema (unknown keys are rejected):
  {version: 1, candidates?: [{case_id: stable string, features: [unique strings]}],
   required_features?: [unique strings], max_cases?: nonnegative int,
   expectations?: [expectation], responses?: [response]}
Supply candidates+required_features for selection, expectations+responses for
comparison, or both. max_cases applies only to selection.
expectation = {case_id, evidence_kind: source_reviewed|serialized_rows,
  evidence_ref: nonempty string, ids: {explicit identity names: integer|string},
  currency: nonempty string, money: {explicit field names: decimal string|int|null},
  tolerance?: {absolute: nonnegative decimal string|int, reason: nonempty string}}
response = {case_id, http_status: integer, body: raw decoded response object|array,
  ids: {explicit identity names: integer|string}, currency: string,
  money: {explicit field names: decimal string|int|null}}
Response fields may be absent to report missing/invalid evidence as findings.
Raw body contents are inspected for embedded failures even with HTTP 200.
Output separates supplied source-reviewed expectations from stored-data consistency;
neither label certifies PDF reading. Greedy selection reports uncovered labels.
CLI: JSON_JOB --output REPORT; exits 0 if requested checks pass, 1 for comparison
findings/uncovered features, 3 for invalid input/IO. No API requests are executed.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal

from _hotel_common import decimal_value, distinct_paths, load_json, write_json

EVIDENCE_KINDS = {"source_reviewed", "serialized_rows"}


def _shape(value, allowed, required, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    if set(value) - set(allowed) or set(required) - set(value):
        raise ValueError(f"{name} has unknown or missing keys")


def _labels(value, name):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value) or len(set(value)) != len(value):
        raise ValueError(f"{name} must be unique nonempty string labels")
    return set(value)


def _index(items, name, allow_duplicates=False):
    if not isinstance(items, list):
        raise ValueError(f"{name} must be a list")
    out = {}
    for item in items:
        if name == "candidate":
            _shape(item, {"case_id", "features"}, {"case_id", "features"}, "candidate")
        elif name == "expected":
            _shape(item, {"case_id", "evidence_kind", "evidence_ref", "ids", "currency", "money", "tolerance"},
                   {"case_id", "evidence_kind", "evidence_ref", "ids", "currency", "money"}, "expectation")
        else:
            _shape(item, {"case_id", "http_status", "body", "ids", "currency", "money"}, {"case_id"}, "response")
        key = item.get("case_id")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("case_id must be a nonempty stable string")
        if key in out and not allow_duplicates:
            raise ValueError(f"Duplicate {name} case_id: {key}")
        out.setdefault(key, []).append(item)
    return out


def select_cases(candidates, required_features, max_cases=None):
    """Deterministic greedy set coverage; equal gains use case_id lexical order."""
    indexed = _index(candidates, "candidate")
    needed = _labels(required_features, "required_features")
    if max_cases is not None and (type(max_cases) is not int or max_cases < 0):
        raise ValueError("max_cases must be a nonnegative integer")
    features = {key: _labels(items[0].get("features", []), "features") for key, items in indexed.items()}
    remaining, selected = set(needed), []
    while remaining and (max_cases is None or len(selected) < max_cases):
        ranked = sorted(((-len(labels & remaining), key) for key, labels in features.items() if key not in selected))
        if not ranked or ranked[0][0] == 0:
            break
        key = ranked[0][1]
        selected.append(key)
        remaining -= features[key]
    return {"selected_case_ids": selected, "covered_features": sorted(needed - remaining),
            "uncovered_features": sorted(remaining), "all_required_features_covered": not remaining,
            "method": "greedy supplied-feature coverage; ties by case_id; no claim of minimum case count"}


def _embedded_errors(value, path="body"):
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            here = f"{path}.{key}"
            if (key.lower() in {"error", "errors", "validation_errors", "error_message", "error_export", "error_file"}
                    and item not in (None, False, "", [], {})):
                found.append(here)
            if key.lower() in {"success", "valid", "ok"} and item is False:
                found.append(here)
            if key.lower() == "status" and isinstance(item, str) and item.lower() in {"error", "failed", "failure", "partial", "partial_success"}:
                found.append(here)
            found.extend(_embedded_errors(item, here))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_embedded_errors(item, f"{path}[{index}]"))
    return sorted(set(found))


def _null_or_decimal(value):
    return None if value is None else decimal_value(value)


def compare_responses(expectations, responses):
    """Compare exact named fields/identities and classify baseline evidence explicitly.

    Expected: case_id, evidence_kind, evidence_ref, ids, currency, money; optional
    tolerance={absolute:<decimal>, reason:<nonempty text>}. Response: case_id,
    http_status, body (raw decoded response), ids, currency, money (explicitly
    extracted fields). A response's HTTP status alone never establishes success.
    """
    expected = _index(expectations, "expected")
    actual = _index(responses, "response", allow_duplicates=True)
    if not expected:
        raise ValueError("At least one explicit expectation is required")
    results = []
    for case_id in sorted(expected):
        item = expected[case_id][0]
        kind = item.get("evidence_kind")
        if kind not in EVIDENCE_KINDS or not isinstance(item.get("evidence_ref"), str) or not item["evidence_ref"].strip():
            raise ValueError("Expected cases need evidence_kind and a nonempty evidence_ref")
        ids, currency, money = item.get("ids"), item.get("currency"), item.get("money")
        if not isinstance(ids, dict) or not ids or any(not isinstance(k, str) or not k or type(v) not in (int, str) or v == "" for k, v in ids.items()):
            raise ValueError("Expected cases need explicit nonempty identity fields")
        if not isinstance(currency, str) or not currency.strip() or not isinstance(money, dict) or not money:
            raise ValueError("Expected cases need currency and monetary fields")
        if any(not isinstance(k, str) or not k for k in money):
            raise ValueError("Monetary fields must have explicit names")
        expected_money = {key: _null_or_decimal(value) for key, value in money.items()}
        tolerance = Decimal(0)
        if "tolerance" in item:
            definition = item["tolerance"]
            _shape(definition, {"absolute", "reason"}, {"absolute", "reason"}, "tolerance")
            tolerance = decimal_value(definition["absolute"])
            if tolerance < 0 or not isinstance(definition.get("reason"), str) or not definition["reason"].strip():
                raise ValueError("Tolerance needs a nonnegative amount and documented reason")
        matches = actual.get(case_id, [])
        issues, differences = [], []
        if not matches:
            issues.append({"code": "missing_response"})
        elif len(matches) != 1:
            issues.append({"code": "duplicate_response", "count": len(matches)})
        else:
            response = matches[0]
            status = response.get("http_status")
            if type(status) is not int or not 200 <= status < 300:
                issues.append({"code": "http_error", "http_status": status})
            if "body" not in response or not isinstance(response["body"], (dict, list)):
                issues.append({"code": "missing_or_invalid_raw_body"})
            else:
                embedded = _embedded_errors(response["body"])
                if embedded:
                    issues.append({"code": "embedded_error", "paths": embedded})
            actual_ids = response.get("ids", {})
            if not isinstance(actual_ids, dict):
                issues.append({"code": "invalid_identity_object"})
                actual_ids = {}
            for field, wanted in ids.items():
                observed = actual_ids.get(field)
                if type(observed) is not type(wanted) or observed != wanted:
                    issues.append({"code": "identity_mismatch", "field": field, "expected": wanted, "actual": observed})
            if response.get("currency") != currency:
                issues.append({"code": "currency_mismatch", "expected": currency, "actual": response.get("currency")})
            observed_money = response.get("money", {})
            if not isinstance(observed_money, dict):
                issues.append({"code": "invalid_money_object"})
                observed_money = {}
            for field, wanted in expected_money.items():
                if field not in observed_money:
                    issues.append({"code": "missing_monetary_field", "field": field})
                    continue
                try:
                    observed = _null_or_decimal(observed_money[field])
                except (ValueError, TypeError):
                    issues.append({"code": "invalid_monetary_value", "field": field})
                    continue
                difference = None if wanted is None or observed is None else abs(observed - wanted)
                equal = wanted is None and observed is None or difference is not None and difference <= tolerance
                differences.append({"field": field, "expected": None if wanted is None else str(wanted),
                                    "actual": None if observed is None else str(observed),
                                    "absolute_difference": None if difference is None else str(difference), "matches": equal})
                if not equal:
                    issues.append({"code": "monetary_mismatch", "field": field})
        results.append({"case_id": case_id, "evidence_kind": kind, "evidence_ref": item["evidence_ref"],
                        "passed": not issues, "issues": issues, "monetary_comparisons": differences,
                        "tolerance": str(tolerance), "tolerance_reason": item.get("tolerance", {}).get("reason"),
                        "claim": "Comparison against supplied source-reviewed expectation" if kind == "source_reviewed"
                                 else "Stored-data consistency only; not source/PDF accuracy"})
    unexpected = sorted(set(actual) - set(expected))
    return {"passed": all(r["passed"] for r in results) and not unexpected,
            "results": results, "unexpected_response_ids": unexpected,
            "limitations": ["Evidence labels and expected values are supplied assertions, not independently verified PDF facts.",
                            "No requests executed; matching serialized rows alone does not establish source accuracy."]}


def run_job(job):
    _shape(job, {"version", "candidates", "required_features", "max_cases", "expectations", "responses"}, {"version"}, "job")
    if type(job["version"]) is not int or job["version"] != 1:
        raise ValueError("Expected job version 1")
    if ("candidates" in job) != ("required_features" in job) or ("expectations" in job) != ("responses" in job):
        raise ValueError("Supply both members of each selection/comparison input pair")
    if "max_cases" in job and "candidates" not in job:
        raise ValueError("max_cases requires candidate selection")
    result = {"version": 1, "offline_only": True}
    if "candidates" in job:
        result["selection"] = select_cases(job["candidates"], job["required_features"], job.get("max_cases"))
    if "expectations" in job:
        result["comparison"] = compare_responses(job["expectations"], job["responses"])
    if len(result) == 2:
        raise ValueError("Supply candidates or expectations")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        distinct_paths((args.output,), (args.job,))
        result = run_job(load_json(args.job))
        write_json(args.output, result, protected=(args.job,))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 3
    return 0 if result.get("comparison", {}).get("passed", True) and result.get("selection", {}).get("all_required_features_covered", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
