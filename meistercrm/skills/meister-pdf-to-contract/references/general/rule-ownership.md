# Rule ownership and precedence

## Resolve authority by scope

For preparation and representation, use: **latest applicable explicit user instruction → applicable reviewed preparation rule in the subject guide → other current domain guidance → shared guidance → historical examples**. A narrow answer for one supplier, edition, customer or task does not silently become a global default. A newer vague statement does not erase a more specific confirmed rule.

- Supplier PDFs and authorized human amendments establish commercial facts. A modelling convention defines how supported facts are represented; it does not make an invented tariff a supplier quote.
- Use the reviewed rules in the guide for the subject. Once their conditions are met, apply them directly. A dated rule that explicitly supersedes an older formula takes precedence wherever that formula appears, including examples and scripts. Keep the review date, scope, rationale and superseded alternative together.
- [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md) sets the regional levy policy. [Hotel VAT and rounding](../hotels.md#vat-country-adjustments-and-rounding) applies across jurisdictions. Do not reintroduce superseded tax instructions from older human notes, source cash-fee formulas or other countries.
- The selected template governs fields except for explicit hotel overrides in [schema and validation](schema-and-validation.md). Do not remove an approved column or change a valid date merely to imitate a defective validator.
- The connected tools establish what the customer can import. Keep offline checks, actual validation results and source-supported exceptions separate.
- Each item workflow explains how to check the published tariff. A labelled superseded formula, dated incident or experiment is not an alternative active policy.

Reuse an explicit answer for the same scope. A clear later customer correction supersedes the earlier interpretation. Ask for clarification only when the source terms, applicable preparation rules and existing answers still leave a material decision unresolved. Identify the affected rows, explain what is unclear and continue with the independent rows.

The subject guides distinguish reviewed preparation rules from supplier terms, implementation observations and superseded practices. A confirmed representation rule does not rewrite a supplier's source facts or extend a property-specific decision to unrelated lodges. Record document/edition, affected dates and components for a scoped answer; reuse it only within that scope.

## Find the rule for a decision

| Decision | Guide | How to apply it |
| --- | --- | --- |
| Client onboarding, inventory, outputs, reconciliation and handoff | [Hotel source intake](../hotels/source-intake.md), then **Meister Contract Operator** → Hotel catalog reconciliation | Keep inventory, outputs and handoff within the bound client |
| Extraction, native/visual evidence, provenance and CSV writing | [Source ETL](source-etl.md) | Use the item guide for any cautions specific to that type |
| Validity, current-month cutoff, one-day seasons, holiday calendars, overlaps, closures and stale coverage | [Dates and seasons](../hotels/dates-and-seasons.md) | Apply the same interval policy to every output; do not redefine it for a checker |
| STO/NET selection, eligible nightly products, park-fee blockers and tariff provenance | [Buying-rate evidence](../hotels/commercial-and-signatures.md) | Preserve the selected tariff and its quoted scope |
| Room naming, capacity, source occupancy calculations, adult-cost supplements and quoted Singles | [Room and occupancy rules](../hotels/occupancy-and-ages.md) | Use the current confirmed encoding and retain source-total differences explicitly |
| Age/admission bands, child-sharing tariffs, accommodation fallback and child extras | [Child policy](../hotels/child-policy.md) | Keep component eligibility and discount bases distinct |
| Board increments, inclusions, compulsory/replacement charges and AI-only products | [Meal plans](../hotels/meal-plans.md) | Apply the approved meal rules with the applicable age and occupancy rules |
| Hotel identity, reference destinations, parent-park aggregation and outside-park descriptions | [Hotel workflow](../hotels/workflow.md) | Do not infer park fees or actual campsite jurisdiction from a destination label |
| Hotel VAT and rounding, regional TDL and inclusion evidence | [Hotel VAT and rounding](../hotels.md#vat-country-adjustments-and-rounding), [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md) | Report the evidence for the applicable formula |
| Source year versus edition versus imported coverage | Rate-year availability (see **Meister Contract Operator**, Hotel rate-year availability) | Reuse the classification for catalog review and tags |
| Serialization, numeric/date/boolean representation, local validator interface | [Schema and validation](schema-and-validation.md) | Test actual saved bytes/cells |
| Generic local execution interfaces for inventory, intervals, files, comparison and price cases | [Source and calendar tools](../hotels/preparation-tools.md) and **Meister Contract Operator** → Hotel coverage and buying-price tools | Execute reviewed inputs using the applicable pricing rules. Use the authenticated workflow for live writes |
| Error classification, exceptions, overlap/coverage and service limits | [Checking gates](checking-gates.md) | Distinguish acceptance from correctness |
| New imports, updates, locales, photos, attachments, tags, notes and live pricing | Profile upload (see **Meister Contract Operator**, Hotel profile upload) | Keep client-specific settings scoped |
| Evidence required to claim profile completion | Completion gates (see **Meister Contract Operator**, Hotel batch completion gates) | Report verified scope and authorized exceptions |
| Other service types | The workflow for each item type | Preserve their units, eligibility and tax rules |

Use the guide for the decision whenever a short reminder omits part of a definition or formula.

Retain source facts, approved defaults and unresolved assumptions separately in private task evidence. Exclude raw transcripts, credentials, client identifiers and confidential prices from reusable skill content. A corpus archive is a research aid, not proof that a rate was fully reviewed. Client work may reuse only that same client's isolated local evidence, with the exact-source checks in onboarding; [client isolation](client-folder-operations.md) prohibits cross-client reuse even for identical documents.
