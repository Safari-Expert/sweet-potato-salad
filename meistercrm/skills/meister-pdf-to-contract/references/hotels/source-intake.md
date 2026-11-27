# Hotel source intake

Use this route for a client batch or full-catalog audit. For one conversion start in [hotel workflow](workflow.md); do not turn a one-file request into a full onboarding project. Apply [rule ownership](../general/rule-ownership.md) and the confirmed policies in each linked domain owner.

## 1. Bind scope before processing

Resolve the customer’s authorized Drive folder or specified local directory and connected MeisterCRM workspace.

Record the authorized folder, contract types, languages, target workspace and current-month cutoff.

Choose the authorized mode: **prepare files**, **create full hotel profiles**, **top up/correct existing hotels**, or **audit a catalog**. Preparation does not authorize live import. Correction preserves hotel IDs; catalog cleanup is a separate explicitly requested operation. Do not continue a closed customer's work when a new client scope is supplied.

## 2. Inventory and organize every input

- Inventory every source, including nested folders, collection documents and native spreadsheets. Record path, hash, edition, property applicability and extraction state. Classify it as usable, duplicate, superseded/outdated, unreadable, unrelated or unresolved; nothing disappears from reconciliation.
- Separate hotel, flight and activity inputs during the onboarding intake. Add other type folders only for actual supplied/requested types. Bundled accommodation/meal tariffs stay in the hotel model; unrelated flights/activities follow their own workflows.
- Preserve originals and human-edited review notes. Organize by verified property identity, not a guessed filename. Before moving/deleting originals, check resolved paths and authorized scope.
Each lodge folder holds the relevant original PDF pages, one maintained XLSX (`Contracts`, `Original`), and an optional notes file.
- Keep calculations, old reviews, manifests, backups and resumable evidence in this client's non-synced local workspace/archive under [client folder operations](../general/client-folder-operations.md). Do not create preparation or scratch folders anywhere in Google Drive. Publish only the verified final deliverables to the bound client.

### Collection folders

Inventory every named property. Create one folder per independently bookable lodge and extract its rate pages and applicable shared terms from a collection. Keep the full original in the customer’s source location.

Use the normalized hotel name for each independently bookable property folder. Retain a shared PDF's hash and property/page mapping; one collection file is not one hotel.

Reuse earlier work only from this same client's verified scope and isolated local workspace, and only when underlying documents, property, tariff selection, edition, currency, dates and terms still match. Never use another client's files, caches or answers even when hashes match. Hash equality proves byte identity, not permission or applicability. Reapply current modelling rules and validation; unreviewed working files are not a trusted tariff baseline.

## 3. Interpret sources and generate supported rates

Read the whole source and the customer’s scoped instructions. Retain page/table/cell references, buying unit, dates, room identity, eligibility, boards, charges and arithmetic on `Original`.

Resolve years through rate-year availability (see **Meister Contract Operator**, Hotel rate-year availability), not filenames or duration thresholds. Preserve seasonal operation and literal holiday spillovers without inventing another year's tariff. Flag wholly past/unusable sources under the cutoff policy. A missing old human workbook is not a blocker: generate from supported supplier evidence.

Apply existing answers before asking another question. Park-fee bundles, unsupported guest configurations, conflicting amounts and missing dates remain review cases when no applicable answer resolves them. Create extra-bed/extra-guest products only with supported capacities and prices. Apply [country fees](../hotels.md#vat-country-adjustments-and-rounding) to the modelled base and supplements, preserving unadjusted and adjusted evidence and avoiding double addition.

For partial evidence, generate only authorized supported portions and retain exact missing scope. Do not infer permission to import partial new hotels from permission to prepare them; honour choices such as fully ready hotels only.

Reopen the canonical XLSX, derive only any technically required temporary validation serialization under the single-workbook policy, and follow [schema/validation](../general/schema-and-validation.md) and [checking gates](../general/checking-gates.md). Reconstruct party totals independently from source evidence. Check season transitions, one-day events, ages, occupancies, boards, compulsory charges and government policy. A supported closure remains a gap; an unexplained one- or two-day hole requires investigation.
