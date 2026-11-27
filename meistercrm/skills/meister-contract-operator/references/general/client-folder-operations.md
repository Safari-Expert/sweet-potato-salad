# Client folder operations

## Resolve and bind the client first

1. Resolve the requested Google Drive folder or the local directory supplied by the customer.
2. Resolve the candidate's actual target and verify its folder identity with available filesystem/Drive metadata. Generated task folders such as `.client-work-YYYYMMDD`, `Client_YYYY-MM-DD`, `_Preparation`, caches and reports are not client roots merely because their names contain a client name. Confirm that the candidate is the actual client folder/shortcut.
3. Proceed only when the evidence supports at least **95% confidence** that this is the requested client's root. Use the threshold as a decision gate, not a fabricated statistical score. An unambiguous name plus a verified target, or a user-confirmed exact root, supports proceeding. Similar competing names, an unresolved shortcut, or conflicting target identity requires one short confirmation question naming the candidate folder(s) **before client-content reads or any processing/writes**. A previous task's client is not a default.
4. Record the verified source and delivery folder identity in the private working files.

Confirm uncertainty through a concise question such as: “Should I use `<resolved client folder>` for this client?” Continue only work independent of client selection while waiting.

## Keep client information separate

- Use the selected client's sources, scoped human answers and authorized records for client facts. Reusable business rules, schemas and generic templates come from **Meister PDF to Contract**. Companion skills/tools may handle file mechanics or authorized service execution; they are not permission to bring in another client's information.
- Never read for reuse, mix, copy, move, derive from or update one client's information in another client's work. This includes rates, PDFs, prepared workbooks, human answers, notes, source mappings, IDs, media, master review comments, receipts, scripts with embedded client data, and remembered facts from other chats or local archives.
- Matching hotel names, brands, prices, filenames, terms or even identical document hashes do not permit cross-client reuse. If the current client's source is missing, record the missing evidence; do not fill it from another client. Independently process a document actually supplied for the selected client.
- Keep source inventories, caches, models, output queues, snapshots and resumable evidence separated by client identity. No shared cross-client extraction cache or combined client ledger. Reuse earlier work only when it originated within this same client's scope and its sources and dependencies still match.
- Validate resolved source and destination paths, Drive parents and shortcut targets against the bound client. Stop on links or destination changes that cross the boundary. Shared collection sources may be reused among applicable properties **within the same client**; this never extends to another client's collection.
- For a multi-client request, maintain a separate binding and local workspace for each client and process each independently. Each reviewer receives only their assigned client's scope and generic skill guidance. Verify the bound client again before every publication, master review update or authorized CRM mutation.

Generic, non-client-specific knowledge already curated into this skill remains reusable. Only use the selected customer’s evidence for their rates and decisions.

## Keep all working files on the local computer

Use a non-synced local directory, for example `<local-temp>\codex\<client-key>\<task-id>` or an available local Codex task directory. Verify that its resolved path is outside Google Drive and other cloud-sync roots; do not assume the OS temp directory is local if it has been redirected. Use a separate durable local client directory if evidence must survive temp cleanup.

Keep extraction text, rendered pages, calculations, validations, backups and receipts in the customer’s separate local working directory. Publish only the final lodge files to the selected Drive or local destination.

Author or edit a local working copy, then reopen and verify it. Some helpers create sibling temporary and backup files: give them local output paths, never the Drive publication path. Before publishing, check that the client destination has not changed since the baseline, retain any necessary backup locally, and copy/upload only the final deliverable to its canonical destination. Reopen/read back the actual published target. Keep temporary validation/import serializations local and discard them when no longer needed.

Do not mistake legacy scratch folders for client sources or resume from them automatically. A skill update is not a cleanup request. If a later task authorizes cleanup, first reconcile unique sources, human edits and needed evidence into that client's local archive; verify exact paths before removing or relocating anything.

## Keep the client folder usable

Inventory incoming originals and map each to its service and physical property. Verify folder identities before publishing.

Use one destination per lodge and deliver only the relevant rate PDF, one workbook and optional notes.

### Minimal property notes

Update one existing current notes file, such as an issues TXT or AI pricing review TXT; avoid accumulating dated review copies. Keep only:

- unresolved, answerable issues, with the affected source/page and scope when needed;
- specific instructions or exceptions needed during import;
- lasting hotel-specific facts needed for later rate maintenance.

Keep the optional notes file brief. Keep page/cell comparisons and decisions needed for future maintenance in working evidence. For CRM fields, use the [master review workflow](../catalog-workflow.md#review-on-the-master). After resolving and verifying a blocker, preserve the customer’s `ai_solution` and replace `ai_comment` with the next blocking question or `""` if none remain.
