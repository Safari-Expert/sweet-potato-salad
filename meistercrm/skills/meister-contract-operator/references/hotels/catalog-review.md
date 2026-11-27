# Review questions on the owner master

Use the workflow in [MeisterCRM](../catalog-workflow.md#review-on-the-master). Use `ai_source.ai_comment` only for a concise question whose answer is needed to proceed with specific contract work. Name the affected room, dates or rows when needed. The customer owns `ai_solution`. Keep source evidence and settled decisions on `Original`. Summarize known pricing rules that the contract rows cannot apply in [hotel notes](profile-upload.md#short-booking-exception-notes).

| Type | Use when | Example `ai_comment` |
| --- | --- | --- |
| NONE | No question blocks the requested contract work. | `""` (empty string) |
| SOURCE | A required rate sheet is missing or outdated | `Can you provide the 2027 supplier rate sheet for this lodge?` |
| DATES | Applicable validity or season wording still leaves specific dates unpriceable after checking what each date governs (see **Meister PDF to Contract**, Hotel dates, seasons and operating scope) | `Which tariff applies from 5–14 February 2032? The two validity clauses for the same tariff give 5 and 15 February as its effective date.` |
| ROOM | Room identities or capacities cannot be matched confidently | `Rates 2027.pdf, p. 3: does Garden Suite replace the existing Garden Room?` |
| GUEST | The stated policy leaves a room or child arrangement unresolved. | `Rates 2027.pdf, p. 4: the child tariff is for sharing with two adults. What applies when sharing with one adult?` |
| PRICE | The applicable amount or charging basis is unclear | `Rates 2027.pdf, p. 2: is the quoted villa price per room or per person?` |
| MEALS | Meal or holiday-charge treatment is unclear | `Rates 2027.pdf, p. 5: does festive dinner replace the normal dinner charge or add to it?` |

Count PDF pages from 1. Add a printed page number only when needed to avoid confusion. For a missing document, name the edition in the question. Use an evidence-only workbook row for an unresolved clause when a source page exists. For multiple independent blockers, retain each question and its scope on `Original` and put the question that needs an answer first in `ai_comment`.

Apply established child/room conventions, one-day seasons and documented closures. An unresolved location match is a source/identity question. On the master, name the missing evidence and exact held scope even when independent rates are ready or the hotel already exists.

Read the latest `ai_solution` and apply it to the question it answers. When the blocker is resolved, replace `ai_comment` with the next outstanding blocking question, or set it to the empty string `""` if none remain. Preserve `ai_solution` and verify both fields on readback. If the question held an authorized upload, [resume it through completion](../catalog-workflow.md#resume-an-upload-after-a-blocker-clears).

For a Tanzanian hotel, record the TDL source evidence, scoped customer answer and verified action on `Original` using the Tanzania TDL decision examples (see **Meister PDF to Contract**, Tanzania hotel VAT and Tourism Development Levy). A levy included in the saved price requires no consultant action.

- Resolve the actual hotel identity and owning workspace before claiming catalog presence.
- Checked file readiness requires the current reopened workbook and its supported scope.
- An owned hotel can already exist while its prices remain unresolved.
- Use verified catalog readback to establish presence.
- Keep workbook hashes, saved-rate comparisons and outstanding uploads in private evidence. Validate the exact delivered XLSX through the connected catalog tools. Verify supplementary uploads against the existing hotel and room IDs.
- Catalog presence does not certify prices, coverage, media, translations or full-profile completion.

An owned hotel with 2026 rates and a missing requested 2027 renewal is already present. Record the missing source and affected year on that master. A checked workbook alone establishes file readiness.

## Processing a batch

Match the customer’s priorities to individual properties and collection members using verified names and aliases. Report ambiguous entries. A priority selects processing order independently of readiness. Apply scoped answers and finish independent work across the batch. Leave the next outstanding supplier question on its owning catalog master. Preserve the customer’s reply, including a new reply arriving during review. Refresh the review before updating the comment. Report the remaining questions and skipped scope at handoff.
