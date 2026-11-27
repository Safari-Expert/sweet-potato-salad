# Hotel contract conversion

| Decision | Reference |
| --- | --- |
| STO selection, source versions and nightly prices | [Buying-rate evidence](commercial-and-signatures.md) |
| Room-to-person conversion, room identity, capacity and missing places | [Rooms and occupancy](occupancy-and-ages.md) |
| Baseline cost and independent meal increments | [Meal plans](meal-plans.md) |
| Inclusive dates, cutoff, editions, operating calendars and stale sources | [Dates and seasons](dates-and-seasons.md) |
| Child eligibility, composition and age boundaries | [Child policy](child-policy.md) |
| Hotel rounding, country/island fee scope and TDL evidence | [Hotel money](../hotels.md#vat-country-adjustments-and-rounding), [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md) |
| Booking research, photo order, translated room names and authorized profile uploads | Hotel profile upload (see **Meister Contract Operator**, Hotel profile upload) |
| Property inventory, per-room completion evidence and final client-folder reconciliation | Hotel completion gates (see **Meister Contract Operator**, Hotel batch completion gates) |

## Decision order

1. Establish the task: supplier edition, intended tariff, current template, connected customer location reference, and new or existing hotel. Apply the [current-month cutoff](dates-and-seasons.md#start-at-the-current-calendar-month).
2. Read and bind the whole source: all applicable pages/sheets, visible headings, formulas, notes and policies. Use [source extraction](../general/source-etl.md); keep source locators and unresolved evidence.
3. Select eligible buying rates: distinguish explicit or assumed STO from RACK, and separate nightly accommodation from duration-priced packages. Apply [commercial evidence](commercial-and-signatures.md) and the [park-fee exclusion / forced-purchase gate](commercial-and-signatures.md#park-fee-exclusion-and-forced-purchases).
4. Build the source matrix: property, location, room, currency, billing unit, occupancy, ages, board, dates, taxes/extras and policy scope. Resolve identity before expanding rows; retain conditions the schema cannot express. Apply the current domain defaults before classifying blockers: [calendar normalization](dates-and-seasons.md#automatic-calendar-normalization-21-october-2026), [unlabelled child percentages](child-policy.md#unlabelled-child-percentages-21-october-2026), [overlapping age bands](child-policy.md#unresolved-overlapping-age-endpoints), [unnamed included meals](meal-plans.md#unnamed-plural-meals-included-21-october-2026) and [group capacity with a stated minimum](occupancy-and-ages.md#group-accommodation-with-a-minimum-but-no-maximum-21-october-2026). Retain printed facts separately from normalized values and approved assumptions, with source/page evidence. A resolved default is not a pending human question; missing facts outside its scope remain blockers.
5. Model whole-room outcomes using [rooms and occupancy](occupancy-and-ages.md), [child policy](child-policy.md) and [meal plans](meal-plans.md). Verify supported full and partial adult/child/infant parties, missing-place charges and independent board increments; keep unknown terms unresolved and unavailable options blank.
6. Expand and reconcile: create only supported date/age/pax rows. Compare source to output and output to source, including policy boundaries and mandatory extras. For an actual historical counterpart, report monetary differences and modelling exceptions separately.
7. Validate and deliver: reopen saved bytes and apply [shared checking gates](../general/checking-gates.md), including existing-target scope where applicable. Report source integrity, offline validation, connected import acceptance and unresolved exclusions separately; preparing a workbook does not authorize import.

## Hotel, room, and rate identity

There are three levels: hotel master, room master under that hotel, and dated room pricing rows. One row represents one room's eligible age/pax interval and one validity period. Preserve distinct room categories and occupancy variants explicitly; a room description is not a substitute for a stable `room_name`.

Resolve each physical property separately before creating folders, CSVs or masters. A combined supplier heading, shared rate table, slash or collection brand can refer to several distinct hotels. Equal tariffs do not establish a single hotel identity. Bind the named properties to source/location evidence, then use the [per-hotel collection delivery rule](source-intake.md#collection-folders). Leave an unresolved identity pending rather than importing a guessed combined property.

- Hotel identity and currency scope: `location_name + hotel_name`, across every room.
- Validation overlap scope: resolved location + hotel name + room name.
- Keep `max_cap` and `max_pax` consistent for a room across all its rows. Current validation requires **max_pax == max_cap**. Do not copy activity-style changing maximum pax tiers into one room master.
- `hotel_group` can be blank. Do not use it as a hidden occupancy or rate discriminator.
- Preserve the actual restricted-area property evidence separately from the user's current output convention. Prepared hotel files use literal `FALSE` under [hotel output representation](../general/schema-and-validation.md#current-hotel-output-representation), unless the user explicitly selects another value; a nearby town or legacy flag does not override that instruction.

For a mobile camp, bind each operating period to its actual location and fee jurisdiction. The same supplier's camp can move between a national park and a conservation area while retaining the same accommodation prices. Matching prices and open dates does not validate a copied `location_name`, protected-area flag or fee schedule. Retain the source's site and date scope, then resolve the exact location reference separately. If the user has approved a [safari-destination fallback](workflow.md#safari-destinations-when-an-exact-location-is-unavailable), keep that label distinct from the actual campsite and fee jurisdiction.
- `hotel_desc` is limited to 380 characters and `room_desc` to 480 under current validation settings. Describe only supported property/room features; do not paste one suite's amenities across every room category.

## Safari destinations when an exact location is unavailable

Group Zanzibar hotels under the exact MeisterCRM destination **Zanzibar**, rather than splitting the catalog between individual towns, beaches or resort areas. This grouping also applies when more granular location references exist, so users can find the region's hotels together. Keep the actual locality and island (Unguja or Pemba, as applicable) in the description and preparation evidence; the shared destination label does not change the property's geography or [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md).

Group hotels by their **parent park destination** when regional labels merely subdivide the same safari park. Use the exact MeisterCRM reference name **Serengeti National Park** for hotels otherwise scattered across Central Serengeti, Northern Serengeti or Southern Serengeti. Apply the same principle to comparable subdivisions of another park: a traveller should find that park's hotels together. Keep the actual subarea in the description rather than creating competing catalog destinations. Reserve hotel notes for pricing exceptions. Do not merge genuinely different parks or countries. This grouping preference applies even when separate subarea references exist.

When MeisterCRM has no matching town or conservancy location for a lodge outside a national park, **use the nearby park's exact location-reference name as its safari destination and state "outside the park" in its description**. Following the later pricing-only notes rule, keep this geographic detail in the description unless it explains a pricing exception. This is a standing preparation convention, not a location blocker requiring approval again. Preserve the source-supported actual lodge area and name the conservancy and park when established. If only a broad safari area is established and its parent park cannot be identified confidently, retain that area's exact reference and say that the precise site needs booking confirmation. Do not invent a park association or claim the camp lies inside or outside a park without evidence.

This is a destination label, not evidence of park boundaries, fee jurisdiction or restricted-area admission. Keep the correct country/island, source operating sites and dates, current output flags and government-fee treatment; do not add park fees from the label. A wrong or unresolved property identity is still a source question. Retain the actual location and fallback reason in preparation evidence.

A matrix of five rooms, ten intervals and three applicable age bands has 150 rows if every combination is supported. Use the matrix to detect missing or duplicated combinations. Each supplier still determines its own calendar, room products and age bands.

## Extract the rate basis before conversion

Use [the local helpers](preparation-tools.md) for reviewed source extraction, calendar intervals and reconciliation.

Build an intermediate matrix of room category, occupancy, eligible age, meal basis, valid dates, supplier cost, currency, and supplements. Establish whether quoted amounts are per person sharing, per room, per villa, or for an entire stay. Also extract child-sharing restrictions, minimum stay, extra-bed policy, closed periods, and mandatory extras. Preserve unsupported conditions on `Original`. Summarize known pricing exceptions the contract rows cannot apply in hotel notes (see **Meister Contract Operator**, Hotel profile upload). If a missing answer prevents preparing a rate, follow catalog review (see **Meister Contract Operator**, Review questions on the owner master).

Record the scope of each passenger-count tier: a mobile camp can price every adult by the adult count across the whole booking, while single occupancy and third-bed discounts depend on the occupants of each tent. Children may be excluded from the booking count. Such tiers do not establish tent capacities or new room categories. Test multi-room bookings on both sides of each tier boundary, minimum nights and camp limits; keep physical inventory and complimentary-guest eligibility separate. If the hotel schema cannot express the booking-level predicate, retain it as a calculation limitation rather than creating room names or changing capacity to imitate the tier.

Normalize each traveler’s rate using [rooms and occupancy](occupancy-and-ages.md). Verify full and partial occupancy against the supplier’s billing unit.

A free infant can be admitted without occupying a priced place. Verify permitted allocation and follow the [child-composition decision sequence](child-policy.md#child-rates-and-unspecified-extras).

## Mixed tariff products and eligibility

Separate accommodation tariffs from duration-priced ground packages even when they share a table or supplier. A two-night package amount is the total for that quoted duration unless the source explicitly says otherwise; a sharing package can be per person while adjacent Single/Double/Triple accommodation quotes are whole-room totals. Retain duration, product, occupancy basis and inclusions before selecting a CSV mapping. Synthetic example: a two-night sharing package at 360 per person totals 720 for two adults for the stay, not 1,440. Do not flatten drives, transfers or balloon charges into a meal supplement without a supported model.

Read the price-table labels when a supplier quotes different markets, residency categories or rate plans. Use the tariff selected for the task and keep separate schedules distinct. If several schedules match and the prices differ, ask which schedule to load.

Preserve the direction, base and scope of cancellation percentages. A deduction of 70% leaves a 30% refund; it does not promise a 70% refund. A credit note is not a cash refund, and restrictions to the same agent or hotel remain attached to that credit. A balloon safety cancellation can have a different refund rule from unused hotel nights on the same itinerary. Retain the source's deadline anchor, including reservation date or first property's arrival, rather than replacing it with the individual room's arrival.

## Supplements and meal basis

| CSV field | Import meaning | Conversion consequence |
| --- | --- | --- |
| `single_supplement` | Increment for an unoccupied priced place | Use the matched adult cost, subject to the quoted Single override, before the country adjustment. |
| `hb_supplement` | Additive half-board amount relative to base cost | Use the supported incremental amount; do not add it to cost and retain it again |
| `fb_supplement` | Additive full-board amount relative to base cost | This is not automatically an increment over half board |
| `ai_supplement` | Additive all-inclusive amount relative to base cost | This is not automatically an increment over full board |

Apply the [meal-plan cell-state contract](meal-plans.md#independent-increments) when encoding board availability: blank, zero and a positive increment have different meanings. Do not make unavailable boards available by filling blanks with zero.

For a two-place room, the current single-supplement calculation adds one supplement for one occupied place. More generally it charges for unused capacity using the selected contract's capacity. Current file preparation always uses the user-confirmed adult-cost supplement rule; reconstruct and disclose differences from a supplier's literal partial-occupancy invoice separately. Historical source-exact example, retained for comparison rather than current encoding: base per-person cost 100 and extra single-use charge 30 gives two-adult cost 200 and one-adult cost 130. Putting the full single rate 130 into that historical example's supplement would charge 230 for one guest.

## Seasons, completeness, and final checks

Use [dates, seasons and operating scope](dates-and-seasons.md) for literal validity, source and seasonal boundaries, closures, renewal/expiry, scoped year corrections and calendar checks. Its user-confirmed conventions apply before expanding and verifying rows.

Recheck ordinary supplier mandatory extras by source edition, product, guest eligibility and unit as well as amount. A per-stay extra cannot become a nightly supplement without a supported stay-length calculation. Keep drink-package exceptions and fee-specific child ages separate from accommodation discounts. Apply the bounded [user fallback for child fees](child-policy.md#child-rates-and-unspecified-extras) when only that component's child price is unspecified; other missing eligibility remains unresolved rather than inherited from another component or edition. For a Tanzanian hotel, government charges follow [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md), rather than this ordinary-extra interpretation.

For a supplier workbook, reconcile detailed calendar cells against summary prices and independently evaluate source formulas: cached agreement does not resolve a conflicting hardcoded exception. Preserve an explicitly authorized increase with its edition and calculation base. If STO is defined as a changing discount against the supplier website, keep that relationship and require a dated supplier quote for the booking; the listed STO amount must not receive the same discount twice. An amendment treated as cancellation plus a new booking can trigger a fresh quote.

When a printed buying amount differs from a stated discount calculation, retain the literal amount and the independently calculated difference with its exact table context. Neither a discount heading nor a child percentage authorizes silently replacing a published amount. If review establishes a wrong pricing unit, preserve the original interpretation as superseded evidence and attach a corrected model, source locator and affected party totals; make the correction authoritative for subsequent mapping.

Before delivery, reconcile source totals for representative occupied rooms, inspect supplement blank/zero behavior, verify all season/age boundaries and room capacities, and run shared CSV checks. Use the [worked occupancy checks](#reconcile-the-tariff-against-the-workbook) to investigate discrepancies.

## Hotel checking gates

Verify policies independently for each property, even within one supplier group. An absent child table, booking-vintage clause or board inclusion does not authorize copying a sibling property's rule. Check each property's own conditions even when branding and prices match.

Record which properties each payment, cancellation and admission section binds. Placement under one property's heading does not establish collection-wide scope. An own-child-room arithmetic clause also does not override a conflicting adult-sharing admission requirement; retain both pending adjudication.

Keep billing units separate across ordinary supplier components. A room price per night and a separately quoted supplier extra per person per day cannot become one nightly total until the extra's billable-day convention is established. Conversely, an explicitly nightly extra-bed charge does not establish the billing period of an otherwise unlabelled main tariff. Preserve material missing units as conversion blockers rather than inferring them from adjacent fees. For a Tanzanian hotel, follow [Tanzania VAT and TDL](../../country/tanzania/vat-and-tdl.md): ignored VAT/other government extras or superseded cash TDL units are not blockers to the settled percentage policy.

Apply the [shared checking gates](../general/checking-gates.md) at hotel, room and contract scope:

- Keep master currency and hotel metadata consistent across all rooms; separately compare `room_desc`, room spelling and capacity within each location + hotel + room. The importer keeps the first room metadata, so a later description change is not an update instruction.
- Check unusually short room-name groups for spelling variants or omitted periods. Keep genuinely shorter operating seasons.
- Reconcile dates per room and exact age/pax band. A source-confirmed seasonal closure is valid missing availability. Keep rates on each side of the closure and document its exact year, dates and room scope. Rainy-season closure is not a blanket rule for Zanzibar or for every room. Use the shared exception procedure even if IO emits `date_gap`.
- Check both hotel output flags against the agreed literal boolean text.
- For an existing hotel, match the selected hotel/location and known rooms, then check the existing-plus-upload union. A valid standalone room sheet does not prove compatibility with existing contracts.

## Reconcile the tariff against the workbook

- A per-room board-price difference must be normalized before per-person storage; independently reconstruct the room total to catch both unit errors and premature rounding.
- Composition-priced family bundles can already include children; applying another generic child discount can under-reconstruct the quoted package. Policy precedence stays explicit.
- Read the property, edition and validity dates on the tariff itself. If the folder names a later year, obtain renewal evidence before extending the rates.
- Mandatory holiday dates and conflicting child endpoints can be absent or unresolved even when ordinary season rows are structurally valid.
- Explicit single-use prices and paid meals for otherwise free children can require exceptions to usual supplement/infant defaults.

A tariff with blank `hotel_group` and `ai_supplement` but zero HB/FB supplements illustrates the difference between unavailable and included. Verify each property’s terms before using that pattern. Inspect the edition’s own restricted-area evidence. Never infer an age band or park membership from a prior workbook.

### Compare quoted occupancy totals

Use the following calculations to test what the supplier actually charges. Populate the workbook using the [current adult-cost supplement and quoted Single exception](occupancy-and-ages.md#current-output-rule-adult-cost-supplement-8-october-2026). Record any difference between the approved encoding and the supplier total.

For an adult base of 100 and an incremental single-use surcharge of 30, the supplier total is 130. Use 30 as the increment when checking the source calculation.

To check an explicit single-use tariff for the same product, derive its implied missing-place amount from the **single-use total**. For an explicitly supported two-adult room total `R` and single-use total `S` for that same product, the candidate encoding is `cost=R/2` and `single_supplement=S-R/2`. This candidate does not override an explicitly chosen [fixed-room product model](occupancy-and-ages.md#fixed-room-recovery-versus-guest-charges). Reconstruct both one adult (`S`) and two adults (`R`) before accepting it. This does not establish child-only eligibility, free-child recovery, extra beds or physical capacity; test those separately. A separately quoted Single product can remain its own capacity-one row.

Where a supplier's supported occupancy totals have a verified constant extra-guest increment `d`, a candidate adult-only encoding is `cost=R_C/C` and `single_supplement=cost-d`, with `R_C` the quoted total for supported priced capacity `C`. Verify `n*cost+(C-n)*single_supplement` against **every quoted occupancy**, including source minima and maxima; one matching full room is insufficient. Nonlinear increments, positional children, free guests, distinct single-use terms and composition bundles may require separate products or remain unsupported by a constant supplement. Use these candidates to compare supplier totals.

For separately quoted one-, two- and three-adult totals `S`, `D` and `T`, first check whether `S+T=2*D`. A constant per-missing-place supplement produces a linear occupancy schedule, so it cannot reproduce all three totals when this equality fails. With triple component `c=T/3`, fitting the two-adult quote gives `supplement=D-2*c`; fitting the single quote gives `supplement=(S-c)/2`. Compare both candidates against the remaining quote using exact arithmetic before rounding. Keep distinct occupancy products or an unresolved mapping when neither fits; separately quoted categories do not establish permission to retain the same room setup with fewer guests.

### Distinguish room fees from guest fees

For an independent check of supplier party totals, count actual chargeable people and rooms. Use the current supplement rule above for the serialized workbook.

| Charge | Effect on guest cost | Effect on recovery for a missing priced place |
| --- | --- | --- |
| Per eligible actual person | Add that guest's fee | Do not add the fee |
| Fixed per room | Allocate the room fee across priced capacity | Recover the corresponding room-fee share so the fee is paid once per room |

For uniform paying guests, room price `R`, priced capacity `C`, a fixed room fee `F` and a per-person fee `M` give `cost = (R + F) / C + M` and a missing-place supplement of `(R + F) / C`. With `n` paying occupants, reconstruct `R + F + n*M`. Capacity-one products have no missing priced place in their supported occupied case; put their compulsory charge in cost.

Synthetic example: a fixed two-place room costs 480 and compulsory brunch is 30 per adult. Under the comparison model, guest cost is 270 and missing-place recovery is 240: one adult pays 510, two pay 540. Recovering 270 for an empty place would incorrectly add its brunch. Conversely, a fixed room fee of 80 with no per-person charge gives cost and recovery of 280, preserving the 560 room total at either occupancy.

Do not automatically discount a fixed room fee with a child's accommodation percentage. Use the actual fee scope and verify the mixed party. Free infants, child allocation, priced-place counting and applicable supplement selection remain governed by the existing occupancy rules; the uniform-adult equation does not replace those checks.
