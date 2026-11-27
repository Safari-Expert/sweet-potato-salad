# Hotel catalog reconciliation

## 1. Record readiness and unresolved questions

Ready describes the checked current workbook. Presence in the owner catalog does not establish that all its rates were imported. Use [catalog review](../catalog-workflow.md#review-on-the-master) for blockers and preserve human replies.

### Human-readable review handoff

Follow [minimal property notes](../general/client-folder-operations.md#minimal-property-notes). Update one concise current TXT only when useful, containing unresolved issues, specific import instructions and lasting hotel-specific facts. Use short sections or bullets as needed; do not require empty sections or publish a resolved-change log. Write blockers as answerable questions with a source/page or numerical example only when needed to explain the uncertainty. Do not ask for approval to correct a workbook error when the source and established rules determine the answer.

Apply the customer’s `ai_solution` within its stated scope. Replace the resolved question in `ai_comment` with the next blocking question or write the empty string `""` if none remain. Preserve `ai_solution` and record the applied TDL basis on `Original`. When a hold is lifted on an authorized upload, [resume from the last verified step](../catalog-workflow.md#resume-an-upload-after-a-blocker-clears) and complete the remaining checks, import and delivery.

When delivering supported rows while a tariff is missing, state the exact excluded room and period and label the coverage partial. Do not call an unquoted period a closure or the whole lodge fully reviewed. Explain necessary cell references with the worksheet, field meaning and relevant amount rather than coordinates alone.

## 2. Reconcile the catalog before writes

For an authorized catalog audit, use [the connected customer account](../catalog-workflow.md), fetch hotel masters, then rooms and contracts for every relevant hotel. Separate owned/editable from public/shared view-only records. Retain hotel, room and contract IDs and source identities privately. A shared reference is not an editable owned master.

Match the physical lodge to the owning master. A shared match alone is insufficient to amend it. Resolve multiple candidate IDs before importing.

Compare supported prepared coverage with existing rows by room identity, date, age, pax, board and money. Classify: already correct; missing subset; wrong existing contract; room metadata/capacity mismatch; unsupported legacy data; new fully ready hotel; or blocked. Preserve duplicate catalog masters separately rather than silently collapsing their IDs.

Prefer contract-ID updates for corrections. Add missing unambiguous rows using the connected workbook import. Preserve the hotel master. Investigate overlaps and duplicate identities.

## 3. Import, verify and hand off

Follow [profile upload](profile-upload.md) and [completion gates](completion-gates.md). Assign one writer per master and reconcile current state before retries.

Verify persisted contracts, live calculations against source expectations, requested languages, ordered media, attachments, year tags and short pricing-exception notes. Record authorized omissions honestly. A user-approved photo omission does not waive rates, identity or price checks and does not belong in hotel pricing notes.

Reconcile inputs, actual properties, selected imports, held rows and verified profiles separately. Verify final lodge files, master comments, customer replies and import receipts.

## Changes and resumption

Tie outputs to source hashes, applicable human answers, policy revision and target identities. Changed PDFs, answers or rules invalidate affected interpretation, rows and checks; reuse unaffected evidence only with a recorded dependency match. On resume read checkpoints and current target state before replaying writes. Generated file, accepted import and verified full profile are distinct checkpoints.
