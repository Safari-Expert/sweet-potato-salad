"""Build property evidence files using local supplier material."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("hotel", "activity", "transfer", "flight", "location", "addon")
MONEY = ("cost", "single_supplement", "hb_supplement", "fb_supplement", "ai_supplement")
NUMBERS = {"min_age", "max_age", "min_pax", "max_pax", "max_cap", "activity_duration_min"}
FLAGS = {"inside_restricted_area", "ignore_proposal_margin", "group_flg"}
DATES = {"start_date", "end_date"}
FRACTIONS = {"margin", "tax", "overnight", "camping"}
SHEET = "Contracts"
EVIDENCE = "Original"
EVIDENCE_COLUMNS = ("Payable row", "Supplier PDF", "Original PDF pages", "Lodge PDF pages",
                    "Commercial scope", "Supplier quote and unit", "Currency", "Region",
                    "Supplier TDL statement", "TDL decision", "Decision basis")
REGIONS = {"tz-mainland", "tz-islands", "other"}
STATEMENTS = {"included", "excluded", "unspecified", "not-applicable"}


def decimal(value):
    if isinstance(value, bool):
        raise ValueError("A boolean is not an amount")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid number: {value}") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"Expected a finite nonnegative number: {value}")
    return result


def required(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Evidence needs a nonempty {key}")
    return value.strip()


def levy(kind, evidence):
    region, statement, action = (required(evidence, k) for k in ("region", "tdl_statement", "tdl_action"))
    if region not in REGIONS or statement not in STATEMENTS or action not in {"none", "add-1pct"}:
        raise ValueError("Unknown geography or TDL classification")
    required(evidence, "basis")
    if kind == "hotel" and region == "tz-mainland":
        if statement == "not-applicable":
            raise ValueError("Specify mainland hotel TDL evidence or an explicit scoped decision")
        if statement == "unspecified":
            required(evidence, "human_decision")
        elif action != ("add-1pct" if statement == "excluded" else "none"):
            raise ValueError("TDL action contradicts the published statement")
    elif action != "none":
        raise ValueError("A mainland hotel uplift cannot apply to this service or region")
    return Decimal("1.01") if action == "add-1pct" else Decimal(1)


def family_checks(kind, values):
    def nonempty(*keys):
        if any(values.get(k) is None or values.get(k) == "" for k in keys):
            raise ValueError(f"Missing identity or value among {keys}")

    if kind == "hotel":
        nonempty("location_name", "hotel_name", "room_name", "max_cap", "single_supplement")
    elif kind == "activity":
        nonempty("location_name", "activity_name", "group_flg", "max_cap", "activity_duration_min")
    elif kind == "transfer":
        nonempty("vehicle_name", "transfer_type", "max_cap")
        endpoints = (bool(values["src_location_name"]), bool(values["dest_location_name"]))
        if values["transfer_type"] == "daily" and endpoints != (False, False):
            raise ValueError("Daily hire has no route endpoints")
        if values["transfer_type"] == "taxi" and endpoints != (True, True):
            raise ValueError("A transfer route requires both endpoints")
        if values["transfer_type"] not in {"daily", "taxi"}:
            raise ValueError("Unsupported transfer type")
    elif kind == "flight":
        from datetime import time
        nonempty("airline_name", "src_location_name", "dest_location_name", "frequency",
                 "dep_time", "arr_time")
        days = values["frequency"].split(",")
        if len(set(days)) != len(days) or any(d not in "1 2 3 4 5 6 7".split() for d in days):
            raise ValueError("Invalid or repeated weekday")
        for col in ("dep_time", "arr_time"):
            clock = values[col]
            if len(clock) != 5 or time.fromisoformat(clock).strftime("%H:%M") != clock:
                raise ValueError("Use a 24-hour HH:MM flight time")
    elif kind == "location":
        nonempty("location_name", "contract_type", "overnight", "camping")
        if values["contract_type"] not in {"person", "group"}:
            raise ValueError("Location fees require person or group")
        if bool(values["description"]) != (values["contract_type"] == "group"):
            raise ValueError("Provide a description only for group fees")
    elif kind == "addon":
        nonempty("addon_name", "addon_sub", "addon_desc", "addon_type", "addon_price_type")
        if values["addon_price_type"] not in {"person", "group"}:
            raise ValueError("Unsupported add-on charging basis")
        for i in range(1, 5):
            if bool(values[f"feature_{i}"]) != bool(values[f"feat_desc_{i}"]):
                raise ValueError(f"Supply both fields of feature {i}")
    if "max_cap" in values and values["max_cap"] < values["max_pax"]:
        raise ValueError("Pax exceeds capacity")


def rate_row(kind, headers, item):
    rate, evidence = item["contract"], item["evidence"]
    if set(rate) != set(headers):
        raise ValueError(f"Template mismatch: {sorted(set(headers) ^ set(rate))}")
    for key in ("pdf", "source_pages", "lodge_pages", "scope", "quote", "basis"):
        required(evidence, key)
    factor = levy(kind, evidence)
    values = {}
    raw_money = []
    for col in headers:
        value = rate[col]
        if value is None or value == "":
            if col in {"cost", "currency", "start_date", "end_date", "min_age", "max_age"}:
                raise ValueError(f"Missing required {col}")
            value = None
        elif col in MONEY:
            value = decimal(value)
            if kind == "hotel":
                value = (value * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        elif col in FRACTIONS:
            value = decimal(value)
        elif col in DATES:
            value = date.fromisoformat(str(value))
        elif col in NUMBERS:
            n = decimal(value)
            if n != n.to_integral_value():
                raise ValueError(f"{col} must be integral")
            value = int(n)
        elif col in FLAGS:
            flag = str(value).upper()
            if flag not in {"FALSE", "TRUE"}:
                raise ValueError(f"{col} must be TRUE or FALSE")
            value = flag
        elif not isinstance(value, str):
            raise ValueError(f"{col} must be text")
        values[col] = value
        if col in MONEY:
            raw_money.extend((None if value is None else decimal(rate[col]), value))
    for lo, hi in (("min_age", "max_age"), ("min_pax", "max_pax"), ("start_date", "end_date")):
        if lo in values and (values[lo] is None or values[hi] is None or values[lo] > values[hi]):
            raise ValueError(f"Invalid {lo} to {hi}")
    if kind == "hotel" and values["tax"] != 0:
        raise ValueError("Hotel tax must be numeric zero")
    if kind == "flight" and (values["min_pax"], values["max_pax"]) != (1, 99):
        raise ValueError("Flight import requires matching from 1 to 99 pax")
    family_checks(kind, values)
    evidence_row = [evidence[k] for k in ("pdf", "source_pages", "lodge_pages", "scope", "quote")]
    evidence_row += [values["currency"], evidence["region"], evidence["tdl_statement"],
                     evidence["tdl_action"], evidence["basis"]]
    if evidence.get("human_decision"):
        evidence_row[-1] += " | Human direction: " + evidence["human_decision"]
    return list(values.values()), evidence_row + raw_money


def add_row(sheet, values):
    sheet.append(values)
    for cell, original in zip(sheet[sheet.max_row], values):
        if isinstance(original, str):
            cell.data_type = "s"
        elif isinstance(original, date):
            cell.number_format = "yyyy-mm-dd"
        elif isinstance(original, Decimal):
            cell.number_format = ("0.00#############;-0.00#############;0"
                                  if original.as_tuple().exponent < -2 else "0.00;-0.00;0")


def check_revision_target(dest):
    from openpyxl import load_workbook

    existing = load_workbook(dest)
    try:
        if existing.sheetnames != [SHEET, EVIDENCE]:
            raise ValueError("Existing workbook has other sheets. Generate a separate working copy.")
        for sheet in existing:
            if sheet.tables or sheet.merged_cells.ranges:
                raise ValueError("Existing workbook has a custom layout. Generate a separate working copy.")
            if any(cell.comment or cell.hyperlink or cell.data_type == "f"
                   for row in sheet.iter_rows() for cell in row):
                raise ValueError("Existing workbook has comments, links or formulas. Generate a separate working copy.")
    finally:
        existing.close()


def build(manifest, output):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter
    data = json.loads(Path(manifest).read_text(encoding="utf-8-sig"), parse_float=Decimal)
    kind = data["kind"]
    held = data.get("held", [])
    if kind not in KINDS or not (data["rows"] or held):
        raise ValueError("Specify a supported kind and at least one payable or held source row")
    dest = Path(output)
    if dest.suffix.lower() != ".xlsx":
        raise ValueError("Use an .xlsx workbook destination")
    if dest.exists():
        check_revision_target(dest)
    with (ROOT / "assets" / "templates" / f"{kind}.csv").open(encoding="utf-8-sig", newline="") as f:
        headers = next(csv.reader(f))
    book = Workbook()
    payable = book.active
    payable.title = SHEET
    evidence = book.create_sheet(EVIDENCE)
    add_row(payable, headers)
    audit_headers = list(EVIDENCE_COLUMNS)
    for col in headers:
        if col in MONEY:
            audit_headers.extend((f"{col} before TDL", f"{col} payable"))
    audit_headers.append("Review status or question")
    add_row(evidence, audit_headers)
    seen = set()
    for i, item in enumerate(data["rows"], 2):
        try:
            row, detail = rate_row(kind, headers, item)
        except (ValueError, KeyError) as exc:
            raise ValueError(f"Payable row {i}: {exc}") from exc
        identity = tuple(row)
        if identity in seen:
            raise ValueError(f"Duplicate payable row {i}")
        seen.add(identity)
        add_row(payable, row)
        add_row(evidence, [i, *detail, "Payable"])
    for record in held:
        keys = ("pdf", "source_pages", "lodge_pages", "scope", "quote")
        detail = [required(record, key) for key in keys]
        optional = ("currency", "region", "tdl_statement", "tdl_action", "basis")
        detail.extend(record.get(key) for key in optional)
        blanks = [None] * (len(audit_headers) - len(detail) - 2)
        add_row(evidence, [None, *detail, *blanks, required(record, "question")])
    for sheet in book:
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        for cell in sheet[1]:
            cell.font = Font(bold=True, color="18415D")
            sheet.column_dimensions[get_column_letter(cell.column)].width = max(15, min(38, len(cell.value) + 3))
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=dest.parent, suffix=".xlsx", delete=False) as f:
        staged = Path(f.name)
    try:
        book.save(staged)
        with staged.open("rb") as f:
            reopened = load_workbook(f, read_only=True)
            try:
                if (reopened.sheetnames != [SHEET, EVIDENCE]
                        or reopened[SHEET].max_row != len(seen) + 1
                        or reopened[EVIDENCE].max_row != len(seen) + len(held) + 1):
                    raise ValueError("Workbook failed verification")
            finally:
                reopened.close()
        staged.replace(dest)
    finally:
        staged.unlink(missing_ok=True)


def pdf(source, output, pages):
    from pypdf import PdfReader, PdfWriter
    src, dest = Path(source), Path(output)
    if src.resolve() == dest.resolve() or dest.suffix.lower() != ".pdf":
        raise ValueError("Choose a distinct output PDF")
    reader = PdfReader(src)
    count = len(reader.pages)
    selected = list(range(1, count + 1)) if pages is None else sorted(set(pages))
    if not selected or selected[0] < 1 or selected[-1] > count:
        raise ValueError(f"Select physical PDF pages within 1..{count}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=dest.parent, suffix=".pdf", delete=False) as f:
        staged = Path(f.name)
    try:
        if pages is None:
            shutil.copyfile(src, staged)
        else:
            writer = PdfWriter()
            for number in selected:
                writer.add_page(reader.pages[number - 1])
            with staged.open("wb") as stream:
                writer.write(stream)
            writer.close()
        with staged.open("rb") as stream:
            if len(PdfReader(stream).pages) != len(selected):
                raise ValueError("PDF page count changed during extraction")
        checksum = hashlib.sha256(staged.read_bytes()).hexdigest()
        staged.replace(dest)
    finally:
        staged.unlink(missing_ok=True)
        reader.close()
    return {"source_pages": selected, "lodge_pages": list(range(1, len(selected) + 1)), "sha256": checksum}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    book = commands.add_parser("workbook", help="Write all reviewed rows of one workbook")
    book.add_argument("manifest")
    book.add_argument("output")
    extract = commands.add_parser("pdf", help="Keep the original or extract explicitly selected pages")
    extract.add_argument("source")
    extract.add_argument("output")
    extract.add_argument("--pages", type=int, nargs="+", help="One-based property and shared-term pages")
    args = parser.parse_args()
    if args.command == "pdf":
        print(json.dumps(pdf(args.source, args.output, args.pages)))
    else:
        build(args.manifest, args.output)


if __name__ == "__main__":
    main()
