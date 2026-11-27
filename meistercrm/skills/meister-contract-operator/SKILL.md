---
name: meister-contract-operator
description: Import reviewed supplier rates into MeisterCRM and verify the saved catalog. Use for catalog matching, file staging and validation, ID-preserving corrections, supplier PDFs, hotel photos and multilingual profiles, coverage tags, buying-price checks and resuming an authorized upload.
---

# Meister Contract Operator

Use this skill when a customer has prepared rates or wants to operate on an existing catalog. To derive rates from source documents, use **Meister PDF to Contract** first. Start with the intended workspace and record, the specific changes requested and the available evidence. For rate imports, use the reviewed workbook. Apply the customer’s selected tariff regardless of the company named on the source or its signature status.

## Approval gates

Check the workspace, requested action and current permissions at the start of every run, including reads. A read, file validation or explicitly requested routine update can proceed within that scope.

- Before committing an import, show the exact validated file, language, catalog type, workspace, target records, proposed changes and warnings. Wait for explicit approval. If the file, target or effects change, validate again and obtain approval for the revised import.
- Before removing a record, rate, saved gallery entry or shared access, identify the owner, parent, IDs, affected children and any gap in coverage. Explain whether the operation deletes an owned record or removes it from this workspace. Obtain approval for the actual removal, including any removal caused by replacing a list.
- Apply approval only to the action or batch the user reviewed. Stop the write if the user declines or cancels. For CRM operations outside supplier contracts, use **Meister Operator** and its Approval Gates.

Keep supplier prices, documents, customer identifiers and files within the customer-selected destination and connected CRM. Use the host’s supported file/document tools or the included local helpers for file handling. No network service is required for local preparation. Use [client folder operations](references/general/client-folder-operations.md) to select and reuse the customer’s delivery folder.

## Operate on the catalog

1. Resolve the catalog master, including spelling variants, location, currency and service/room identity through connected MeisterCRM search and owner catalog list. Create an identifiable missing master even when an individual rate needs clarification. Keep separate properties, routes, editions and currencies distinguishable. Use `ai_source.ai_comment` only for a concise question that blocks the work. After applying and verifying a customer's answer in `ai_source.ai_solution`, preserve the answer and set `ai_comment` to the next blocking question or `""` if none remain. Summarize only pricing adjustments or rules the contract rows cannot apply in hotel `notes`. Record the basis for calculated rates on `Original`. Follow the [master review workflow](references/catalog-workflow.md#review-on-the-master).
2. Apply [the connected import workflow](references/catalog-workflow.md). When a blocker clears, [resume the authorized upload](references/catalog-workflow.md#resume-an-upload-after-a-blocker-clears) from its last verified step and complete every applicable checking gate. Import distinct new rows that are unambiguous; skip existing exact matches. Use the single-contract update for a positively matched correction. Re-read changed masters, attachments and affected contracts. Report counts for created, imported, corrected, duplicate and held rows, property links and the exact outstanding question for each affected master.

## Select the operation

- [Connected MeisterCRM workflow](references/catalog-workflow.md)
- [Hotel catalog reconciliation](references/hotels/catalog-reconciliation.md)
- [Review questions on the owner master](references/hotels/catalog-review.md)
- [Hotel profile upload](references/hotels/profile-upload.md)
- [Hotel rate-year availability](references/hotels/rate-year-availability.md)
- [Hotel batch completion gates](references/hotels/completion-gates.md)
- [Verify a saved correction](references/saved-corrections.md)
- [Hotel coverage and buying-price tools](references/hotels/verification-tools.md)
- [Flight contract updates and checks](references/flights/live-updates-and-checks.md)
- [Customer-authorized hotel catalog cleanup](references/hotels/client-hotel-catalog-cleanup.md)
- [Compare hotel upload times](references/hotels/upload-timing.md)
