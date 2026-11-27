# Local preparation

Use Python 3.11+ on Windows, macOS and Linux. Install `openpyxl>=3.1,<4` and `pypdf>=5,<7` in your chosen Python environment when needed. The scripts only operate on named local paths. If you use equivalent document tools, apply the same saved-file verification.

## Create the lodge PDF

`python scripts/contract_files.py pdf collection.pdf lodge.pdf --pages 2 3 8` copies the selected physical pages, sorted and deduplicated. Include both the lodge pricing and applicable shared terms. Its output lists source-page to lodge-page correspondence and the final SHA-256. Omitting `--pages` copies the complete source byte-for-byte for a single-lodge original. Review the actual rendered result, including scanned pages, before attaching it.

When several PDFs apply to one lodge, select and verify the relevant pages from each source in the private working directory first. For example, if a verified two-page tariff extract and a one-page amendment both apply, assemble the delivery copy in that order:

```python
from pypdf import PdfWriter

with PdfWriter() as lodge_pdf:
    for extract in ("tariff-pages.pdf", "amendment-page.pdf"):
        lodge_pdf.append(extract, import_outline=False)
    lodge_pdf.write("lodge-rates.pdf")
```

Reopen the three-page result. Map delivered pages 1–2 and 3 back to the respective original filenames and physical pages on `Original`. Keep the supplier originals in the authorized source location.

## Create or revise one workbook

`python scripts/contract_files.py workbook reviewed.json payable.xlsx` atomically replaces the named workbook from a complete reviewed manifest. For a revision first read the existing rows and evidence, apply the requested change, then submit the full resulting row set. Use a separate local working path when the existing workbook has customer edits, formulas, comments, links, layout or content beyond the manifest. This generator builds sheets from the manifest. Use a workbook editor to merge the reviewed changes into a working copy while retaining those additions. Reopen it and compare unaffected rows, formulas, comments and source evidence before updating the same delivered workbook. The JSON is local working input, outside the customer's lodge folder.

Use this input shape; replace the abbreviated `contract` object with every key in the chosen header-only template. The helper expects ISO input dates. Use source-derived decimal strings or numbers for money, `null` for unavailable options and a true numeric zero for included options. Text containing formula characters remains literal text when written to XLSX.

```json
{
  "kind": "hotel",
  "rows": [{
    "contract": {"cost": "112.50", "single_supplement": "112.50"},
    "evidence": {
      "pdf": "Supplier terms.pdf",
      "source_pages": "2, 8",
      "lodge_pages": "1, 3",
      "scope": "Harbor Room, two adults sharing, high season",
      "quote": "USD 225 per double room per night, breakfast included",
      "region": "tz-mainland",
      "tdl_statement": "excluded",
      "tdl_action": "add-1pct",
      "basis": "Page 8 states TDL excluded for this table."
    }
  }]
}
```

Use regions `tz-mainland`, `tz-islands` or `other`. TDL evidence is `included`, `excluded`, `unspecified` or `not-applicable`; actual actions are `none` and `add-1pct`. For mainland-hotel silence include `human_decision` with the applicable instruction. For ordinary non-hotel services use `not-applicable`, `none` and an explanatory basis. All supplied money fields are modeled values *before* this pass. The final two-decimal half-up rule applies to hotels. For other families preserve the quoted precision and validate it through saved catalog readback. Do not reuse already adjusted output as input. Keep the complete quoted original price(s) and unit in `quote`, including board/child/extra prices, and original/new page numbers as strings. If a single price field combines components with different TDL treatment, retain individual source evidence and calculate each once with precise decimal arithmetic; use a workbook tool capable of saving that breakdown instead of passing a mixed or pre-adjusted amount to this helper.

The tool checks schema shape, basic bounds and the supported row-wide levy. Verify tariff semantics, matching, age/pax/date intersections, supplier conditions, import-validation results, and each expected first-sheet value against its source. Compare source PDF and attached bytes or returned file identity, including applicable amendments. Checksums identify files; they cannot verify what a tariff means.

## Stage the final workbook

Use the saved two-sheet XLSX itself. Its first tab is named **Contracts** and carries numeric payable rates. Its second tab is named **Original** and carries supplier evidence, source page references, TDL basis and results. Stage and validate the same immutable bytes as delivered; the importer selects verified new rows and skips or holds others. Never send the evidence as a second import. For the local manifest, unresolved source lines can be listed in an optional top-level `held` array with `pdf`, `source_pages`, `lodge_pages`, `scope`, `quote` and `question` text, and any established currency/region/TDL evidence. Held lines appear only on Original with a blank payable-row number. A workbook containing only held evidence is useful for review; do not submit an empty Contracts tab for import.
