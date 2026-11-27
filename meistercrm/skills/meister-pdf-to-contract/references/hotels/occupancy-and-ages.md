# Hotel occupancy, ages and missing places

Resolve the source product, charging unit, permitted party and discount base before applying the user's encoding defaults. Explicit source terms defeat an unqualified default, but do not silently cancel an applicable user-approved simplification. Preserve source facts and selected encoding separately under [rule ownership and precedence](../general/rule-ownership.md); keep genuinely unknown or contradictory terms unresolved.

Where the supplier defines a booking-wide quota of specially priced Single rooms, preserve the quantity, excess-room tariff and booking scope as supplier evidence, then apply the [11 October Single-quota policy and pricing-note requirement](#booking-wide-single-quotas-11-october-2026). Do not revive the earlier instruction to withhold those Single rows.

## Establish units and room identity

- The import stores per-person `cost`. Keep an explicitly per-person supplier rate per person.
- Read units at row/cell level, not just the page heading: an explicit total for four guests can override a general per-person heading while an adjacent premium four-person tariff remains per person. Normalize each supported quote separately.
- For a fixed total-room rate, divide by its supported priced capacity, then apply the [current minima, capacity and extra-bed output decisions](#room-names-and-occupancy-decisions). Do not revive the superseded zero-boundary minimum.
- Record original room total, capacity/divisor, exact decimal result, emitted value and reconstructed full-room total. Do not silently round recurring divisions. Supplement model declarations use two decimal places; do not assume they retain the same precision as `cost` or proposal totals.
- Check physical capacity, extra beds, villas and minimum occupancy before applying this default. Preserve a supplier-supported exception rather than forcing unlike products into one room name.
- Read occupancy pictograms within the selected STO column. A RACK family composition or capacity is not automatically the STO composition. If maximum capacity is unquoted, apply only an applicable [approved capacity default](#group-accommodation-with-a-minimum-but-no-maximum-21-october-2026); otherwise retain the missing capacity as unresolved. Compare each extra-person variant against its own room's base quote to catch copied arithmetic.
- Separate physical capacity, a booking minimum and a minimum occupancy charge. "Not sold below two guests" prohibits that booking; "minimum charge for two guests" may permit one guest at a two-guest cost. Neither means charging every unused physical bed. For a three-place room charged at least two per-person rates, a constant missing-place supplement cannot reproduce every one/two/three-person total. Preserve the literal guest/adult wording and unresolved mapping instead of converting a charged minimum into a booking prohibition or maximum capacity.
- A double-based room quote can allow two adults plus children without pricing four adult places. Dividing by two but setting priced recovery capacity to four can double-charge two adults when children are free. Independently preserve the maximum-adult and child/bed conditions; changing a divisor or dropping permitted children is not a faithful solution by itself.
- A family price explicitly quoted for a composition such as two adults plus two children may already incorporate the child policy. Do not divide the bundle by capacity and then apply the general child discount again without reconstructing that exact party's total. Keep composition-priced bundles distinct from an ordinary adult sharing tariff; if a faithful general mapping is unavailable, record the user-approved simplification and its impact.

  When the source explicitly supports a package total `B` for `A` adults and `C` paying children, with each child charged fraction `f` of the same adult basis, a conditional recovery is `adult_cost=B/(A+C*f)` and `child_cost=f*adult_cost`. Synthetic example: a 300 package for two adults plus two half-price children uses three adult-equivalent paying units, giving adult100/child50 and total300. Dividing300 by four beds and then halving the children gives225 instead. Recover each quoted board independently, retain exact precision, and do not apply this equation if the package incorporates a separate promotion or the percentage base is unbound. Reproducing that quoted party does not establish partial occupancy, infant treatment, own-child rooms or extra positions.
- A discount or extra-bed price for the third adult is positional. Averaging a three-adult total into every adult row can reproduce that party yet misprice two adults with a child. Synthetic example: two adults at 100 plus a third adult at 70 gives total 270 and averaged cost 90; replacing the third adult with a child at 40 gives an averaged-row total 220 instead of the supplier's 240. Check partial occupancy and every supported mixed party before accepting averaged rows.
  Where the user has already approved both a selected fixed-unit model and the adult-price fallback for unrepresentable child composition, a deterministic alternative is to preserve the exact quoted all-adult unit total and give the affected paying child the same adult-equivalent unit share. In that example, cost/recovery 90 and child fallback 90 preserve 270; explicitly disclose the 30 excess over the literal mixed-party tariff of 240. This is the approved simplification, not exact supplier family pricing. Do not reopen a generic modelling question already settled by those scoped approvals, and do not apply this alternative without them. It does not resolve missing fee ages or authorize child-only Single occupancy when children must share with adults.
- Apply [extra-place child-price bases and child-only quote restrictions](child-policy.md#extra-place-and-child-only-quotes) when reconstructing those parties.
- For a unit price that includes up to a stated number of guests and charges separately above that threshold, retain the fixed unit total through the included positions and add only the explicitly priced extra positions. The included count, booking minimum and physical maximum are separate. A free child does not automatically reduce the unit price, and a room name does not establish the divisor. If a general extra-bed discount might also apply to a family room's last permitted position, retain both conditional interpretations until the source establishes precedence.

Read bed configuration separately from tariff arithmetic. A triple described as a double bed plus a single bed does not instruct adding the Double product's price to the Single product's price. Use its explicitly quoted triple tariff, and retain any conflict between the bed description, allowed adult/child composition and capacity as unresolved.

A first-adult price plus additional-adult increments is a positional tariff, not a uniform per-person sharing price. Reconstruct each quoted party before choosing import fields. Synthetic example: first adult 120 and each additional adult 70 produces 120, 190 and 260 for one, two and three adults; multiplying 120 by guest count is wrong. This arithmetic does not establish room admission, child ages, included board or an unquoted billing period.

For authorized changes to existing room products and contracts, follow the existing-hotel update procedure (see **Meister Contract Operator**, Hotel profile upload).

## Room names and occupancy decisions

For prepared files, use readable Title Case such as `Single Room`, matching the user's example described as camel case. When source evidence or the user confirms that a renamed room is the same product, use its **most up-to-date confirmed name across the supported editions**. Retain the old-to-current name mapping privately, while binding prices, units, minima and validity to each edition. A rename does not authorize carrying newer prices into older years or fill an unquoted season. This output convention does not authorize renaming existing catalog rooms.

Correct a generic human-created category by reconciling the actual source inventory. Distinct products remain distinct even if they have equal prices or capacities; compare descriptions and bed configurations as well as names. Do not retain an old bed description that contradicts the confirmed source after a rename. A newly introduced category is added only for editions that quote it.

Represent a supported extra-bed or extra-person setup as its own named room product, alongside the ordinary setup. This is the required extra-bed encoding in the current preparation workflow: for example, retain `Double Room` with two priced places and add `Double Room + Extra Bed` with three priced places. Its adult per-person accommodation cost is `(supported Double total + supported extra-place charge) / 3`, after applying any eligible buying discount exactly once. Do not keep the two-place divisor or charge the extra bed again after including it in that total. Per-person board upgrades remain per person; adding a bed does not divide those upgrades by three. Establish the ordinary-rate and extra-rate guest counts before averaging; permission to add a bed does not establish an unquoted family capacity, child allocation or booking minimum. Validate mixed-age parties under the existing [positional-rate and child fallback rules](#establish-units-and-room-identity), rather than automatically halving an averaged adult share. A unique inventory description can resolve an alias where the user confirms there is only one such house or suite; several plausible matches still require identification.

Use one consistent extra-place suffix: ` + Extra Bed` for an extra-bed product or ` + Extra Guest` for an extra-guest product, such as `Family Unit + Extra Guest`. Replace parenthesized extra-place labels and avoid adjacent `)(` groups, duplicate qualifiers or mixed naming styles. Preserve the distinction between a bed and a guest; do not relabel the commercial setup or change its capacity or prices. Translate the suffix into each requested language while keeping the same ` + ` separator. Apply this convention to prepared room names and upload display names, retaining a private alias to the source/import identity. This supersedes the earlier parenthesized examples by explicit user correction on 10 October 2026.

Check the base room identity before adding that suffix. An ordinary quoted Triple remains a Triple; it is not automatically an extra-place variant. For an extra-guest variant of a two-place family, do not rename the base to Triple and then add ` + Extra Guest`, which implies another place. Reconcile source alias, translated display name and unchanged capacity across the saved workbook, CSV mapping and captured room ID.

The current default is **`min_pax=1`**, superseding the older zero-boundary convention. Apply explicit supplier booking minima and any compatible, property-specific minimum selected by the user; keep `max_pax=max_cap` at the supported capacity. Bed count alone does not set the booking minimum. A user's decision to sell one triple only at full occupancy, or to restrict one villa to a chosen minimum, is not a rule for all triples or villas. Distinguish booking minima from minimum occupancy charges using [occupancy and ages](#establish-units-and-room-identity).

For a newly created **extra-bed variant**, the 10 October user correction instead sets **`min_pax=max_pax=max_cap`** at that variant's supported full occupancy. Keep the ordinary room separate. A Single quote commonly represents single use of the same Double room; it does not establish a distinct Single room that accepts another bed. Create the supported Double extra-bed product rather than synthesizing `Single Room + Extra Bed`. This convention does not establish an unquoted extra charge, bed eligibility or larger capacity.

When a Honeymoon Suite's source omits capacity, apply the user-confirmed 10 October 2026 preparation default: **`max_cap=2`, `min_pax=1`, `max_pax=2`**. Explicit source capacity and booking minima take precedence. Record this as an assumed two-person product, not proof of the supplier's physical maximum. This default supplies occupancy only; it does not establish unquoted rates, age rules or bed configurations, or change the quoted rate unit.

For an interconnected product, derive combined capacity from its identified component rooms when each component's capacity is established: two supported two-person rooms give four places. Preserve its own unit price and booking minimum. The word "Family" alone does not establish four places or identify those components.

### Group accommodation with a minimum but no maximum, 21 October 2026

When a **Family Room, family suite, villa or other clearly group-oriented unit** has a stated minimum guest count `m` but no maximum, use the user-approved assumption **`max_cap = max_pax = m + 2`**. Preserve an explicit booking minimum as `min_pax=m`; for example, a Family Room with minimum four and no maximum uses minimum four, maximum six. This is a preparation assumption motivated by common double-bed increments, not verified physical capacity or evidence that another bed exists.

Apply it only to the named accommodation unit, not a minimum group size across several rooms or a number of tents. A minimum occupancy **charge** remains a charging condition, not automatically a booking minimum. Explicit maximum capacities, component-room capacities, adult limits and child-only extra-place restrictions control over this default. Do not add two places to an already stated maximum or generate a separate extra-bed product without its applicable price and eligibility.

The capacity assumption does not identify the pricing divisor: a quote covering four guests plus separately charged extra guests still uses that stated basis. Resolve the whole-unit versus per-person tariff and any extra-place prices before generating those occupancies; do not divide a four-guest bundle by six or invent free extra guests. Record the source/page, stated minimum and assumed maximum in the review and pricing metadata. If a family/group unit has no capacity clues at all, retain a `ROOM` blocker. This supersedes withholding capacity solely because its maximum is missing when the stated-minimum conditions above are met.

### Other occupancy uncertainties

A villa's total pax count does not establish its bedroom count, bed layout or allocation. Ask for that configuration when it materially affects the model and the source does not provide it; retain the answered configuration and the user's chosen minimum separately. An ambiguous room unit must be resolved before division, not inferred from capacity alone.

| Source ambiguity | Decision to retain |
| --- | --- |
| A source omits one room's seasonal price and the user clarifies its name | Apply the identity answer, but keep the missing tariff separate. Neither the rename nor another room's matching high-season price supplies the omitted rate. |

## Fixed-room recovery versus guest charges

Keep a selected fixed-price Double or larger unit distinct from a separately named Single product. The existence of a Single quote does not automatically authorize switching a partially occupied Double to that cheaper tariff. When the user selects fixed-room recovery, preserve the chosen room's full price and retain the Single product's own quote separately. A true single-use tariff for the same product is a different case, covered by [occupancy and ages](occupancy-and-ages.md).

### Current output rule: adult-cost supplement, 8 October 2026

Before final [country adjustments and monetary rounding](../hotels.md#vat-country-adjustments-and-rounding), for every hotel row whose `cost > 0`, set `single_supplement` equal to the **current adult per-person `cost` for the same room, dates and pax scope**, including compulsory holiday or meal amounts already included in that adult cost, **except for the quoted Single-product override below**. Apply that adult amount to both adult and discounted child rows in the larger room products. Do not copy the child's discounted cost into this field. For a free base row, applicable base supplements are zero; unavailable board options remain blank/null.

This explicit general correction supersedes the earlier instruction to exclude per-person compulsory charges from missing-place supplements. Its earlier capacity-one treatment is superseded by the 10 October override below. A change in the adult holiday cost must therefore change the matched paid rows' supplement on that date for larger room products.

### Quoted Single-product override, 10 October 2026

For a separately quoted, fully priced **Single product with `max_cap=1`**, use that full Single price in `cost` and set **`single_supplement=0`** on its supported rows, including paying child rows where the source allows their own room. The user expressly corrected the older paid-Single adult-cost convention. It does not change the adult-cost recovery rule for a Double or larger room occupied by one person, or authorize deriving an unquoted Single price. Mandatory guest charges still enter the occupied Single's cost once. Final country adjustments follow [their separate reference](../hotels.md#vat-country-adjustments-and-rounding).

A supplement on a capacity-one room is dormant when its one paying occupant fills priced capacity. A separately quoted Single starts with zero base supplement under the [current Single override](#quoted-single-product-override-10-october-2026), followed by final [country adjustments](../hotels.md#vat-country-adjustments-and-rounding). Verify its actual base total; merely storing a surcharge in `single_supplement` does not add it to occupied cost. Keep a single-use option within a larger room's allocation separate from a capacity-one product.

### Booking-wide Single quotas, 11 October 2026

The current system cannot enforce inventory or booking-wide limits on specially priced Single rooms. Under the user's preparation policy, emit the quoted Single price for any number of Single rooms; do not withhold those rows or substitute the excess-room tariff merely to imitate a quota. Preserve the actual source limit and excess-room condition as a **hotel master note** for later profile upload, for example: "The source quotes a special Single price only for the first two rooms per booking." Use the source's actual quantity, not the example's quantity. If preparing files only, retain the note in durable per-hotel upload metadata and mention it in the latest review; the contract CSV has no hotel-master notes field. Do not put the warning into a price column or claim it was saved to a live master before an authorized upload.

This is an accepted commercial simplification, not proof of unlimited supplier inventory or source-exact pricing beyond the quota. The same rule applies to other lodges with the same booking-wide limitation. It supersedes earlier instructions to withhold unconditional Single products until booking-level enforcement exists.

For user-visible notes, follow short booking-exception notes (see **Meister Contract Operator**, Hotel profile upload): **hotel notes are reserved for pricing exceptions**. State the actual room limit/excess price or child discount and manual action briefly. Keep missing-picture notices, processing status and internal modelling rationale in the work records; describing a supplier discount must not imply it is applied automatically when the prepared rates use another accepted discount.

### Accepted adult-cost encoding example

Synthetic example before final country adjustments: adult ordinary cost 240 plus compulsory meal charge 30 gives adult cost 270 and `single_supplement=270`; a paying child's cost may be 135 while its supplement remains 270. A free row retains zero applicable supplements. For one adult in a two-place room, this encoding reconstructs 540, rather than the supplier's hypothetical 480 room plus one 30 guest charge. Retain that difference as an **accepted user encoding convention**, not as a claim about how the supplier invoices absent guests. Do not reopen this settled output policy because the historical source-exact model gives a different partial-occupancy total.

Preserve exact calculation precision before [country adjustments and monetary rounding](../hotels.md#vat-country-adjustments-and-rounding); [hotel output representation](../general/schema-and-validation.md#current-hotel-output-representation) owns the saved date, flag, board-column and monetary-cell conventions.

## Missing-place supplements

`single_supplement` is an increment per missing priced place, not the full price of a single-use room.

Build base supplements using the [adult-cost rule and quoted Single override](#current-output-rule-adult-cost-supplement-8-october-2026), then apply [country adjustments and monetary rounding](../hotels.md#vat-country-adjustments-and-rounding). Keep a separately named Single tariff's base distinct from a selected Double. Source-specific single-use surcharges remain comparison evidence and do not override this explicit user encoding. [Meal plans](meal-plans.md#independent-increments) owns inactive versus included board-cell meanings.

Synthetic examples for a triple room with adult cost 100 and supplement 100:

| Occupants | Base costs | Missing-place cost | Room total |
| --- | ---: | ---: | ---: |
| Three adults | 300 | 0 | 300 |
| Two adults | 200 | 100 | 300 |
| One adult | 100 | 200 | 300 |
| One adult and one child at 50 | 150 | 100 | 250 |
| One adult and a free infant | 100 | 200 | 300 |

For a party check, distinguish paying places from physical occupancy. A free infant still needs supplier-approved space and accompaniment. Reconstruct the missing-place charge once per unfilled priced place. For a mixed party compare the result using the largest applicable matched supplement. Count guests with positive base cost separately from free guests; never add an extra missing-place charge once per traveler. Check the supplier’s physical occupancy and admission limits independently.

When reviewing a historical workbook or generated pricing proof, reconstruct the complete party from the actual age-selected rows. An adult subtotal is not a mixed-party invoice. Use the selected room's actual capacity for missing places; a two-place formula reused for a triple can understate partial-occupancy totals. Keep the child's base cost, board increment and applicable supplement in the same reconstruction. Label parties exceeding physical capacity as arithmetic counterexamples, not valid supplier bookings. Separately test free infants, age boundaries and child-own-room arrangements; combinations of selected row indices do not prove that the runtime selects those rows for the stated ages.

The user's hypothetical child-only arithmetic, 50 + 2 x 100 = 250, demonstrates the supplement formula; it does not authorize child-only allocation.

### Check the supplier’s occupancy totals

Use the [worked occupancy comparisons](workflow.md#compare-quoted-occupancy-totals) for single-use surcharges, constant extra-guest increments and nonlinear occupancy tariffs. Populate the workbook with the current output rules above.

## Verification

For each room/season/age policy, independently reconstruct every supported occupancy total, including children and infants. Separate literal supplier agreement, accepted user modelling policy, rounding residuals and quote compatibility. Do not turn a historically curated mismatch into a new universal rule.
