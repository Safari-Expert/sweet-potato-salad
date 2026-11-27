# Hotel baseline and meal plans

`cost` is the standard sleeping-rate anchor, labelled BB by the system, even when the supplier does not sell breakfast or sells only an inclusive package. Retain the actual source inclusions in evidence. Do not invent a lower BB price by subtracting an unquoted meal value.

If a supplier only quotes inclusive board rates, retain that amount in `cost`, the system's BB-labelled baseline, and set the offered included board's supplement to zero. This does not assert the supplier sells BB separately. Leave unavailable boards blank; never invent an unquoted cheaper BB amount.

## Meal meanings and compulsory components

For breakfast-inclusive products, the clarified convention is **HB = breakfast + dinner**, and **FB = breakfast + lunch + dinner**. An optional supplier lunch exchange does not change the dinner default. Use lunch-as-HB only for an explicitly selected alternative or a resolved source product that includes lunch instead; do not silently select it because both meals are offered. This supersedes the abandoned HB-equals-lunch interpretation. Breakfast already included in the source room quote is not added again from a standalone breakfast tariff. Other baseline inclusions remain governed by [the baseline and independent increments](#independent-increments).

### Unnamed plural meals included, 21 October 2026

When an applicable rate says **“meals included”** in the plural but gives no HB/FB label or limiting meal list, assume **all meals / FB**. For example, “March–May prices have meals included” means FB for those priced dates and products only. Keep the inclusive tariff in `cost` and set `fb_supplement=0`; leave HB and AI blank unless independently offered. Do not add lunch or dinner again or invent a cheaper BB rate. Explicit “breakfast and dinner”, HB, a limited number of meals or other clear inclusion wording takes precedence over the plural default. A singular “meal included” does not trigger it, and FB does not imply drinks, activities or AI.

Record the source wording/page and the assumed FB basis privately and in the concise review. This explicit user preparation default resolves the missing board label, not missing meal prices, compulsory festive participation or other source contradictions.

### Compulsory and festive meal arithmetic

A published festive menu price does not, by itself, establish compulsory purchase. When the source or an explicit user decision makes a meal compulsory, include that charge in `cost` for its eligible dates and guests. Remove that same included meal from the relevant board increment, so it is charged once.

Resolve **additive versus replacement** separately from **optional versus compulsory**. Where ordinary dinner is quoted and a smaller amount is labelled a festive dinner supplement, that wording and arithmetic can support an additive interpretation, as confirmed by the user in the 8 October review. Record the deduction and check for contrary replacement wording; do not turn it into a rule that all festive prices must increase. An additive amount alone does not prove compulsory participation. For an optional dinner addition, BB cost is unchanged and the extra enters both HB and FB on the specified dates. Reuse a settled interpretation for its source scope instead of asking the same question again.

Resolve source package differences, discount board scope and quoted-versus-unquoted meal options in [independent increments](#independent-increments) before applying the compulsory-meal equations below.

For a BB-based product with dinner as HB, let `B` be the selected guest's accommodation share, `L` and `D` the resolved lunch and dinner prices, and `ML`/`MD` those meal amounts already included as compulsory:

- `cost = B + ML + MD`
- `hb_supplement = D - MD`
- `fb_supplement = L + D - ML - MD`

For an explicitly selected lunch-as-HB alternative, use hb_supplement = L - ML; FB is unchanged. Apply the guest's source-supported meal discount before these calculations. Mandatory lunch does not reduce dinner-only HB. If lunch is compulsory, HB and FB may legitimately have the same remaining dinner increment; if both meals are included, their supported increments can be zero. Use these equations for full meal prices replacing ordinary meals, not blindly for a supplier's separately quoted incremental surcharge or an already inclusive base.

### All-inclusive-only lodges, 14 October 2026

When a lodge offers **only all-inclusive packages**, put the entire supported package price in `cost`, using the established per-person conversion and age rules. Set `hb_supplement` and `fb_supplement` to blank/null and `ai_supplement` to numeric `0` on every supported row. The zero marks AI as included so the system can automatically select it; blank HB/FB prevents advertising those as separate available options. Do not split included meals, drinks or other inseparable services out of the package or charge them again through AI.

Apply the existing [adult-cost Single supplement](occupancy-and-ages.md#current-output-rule-adult-cost-supplement-8-october-2026), including its [quoted capacity-one Single override](occupancy-and-ages.md#quoted-single-product-override-10-october-2026): paying rows in larger rooms use the matching adult package cost; quoted Singles and free rows retain zero applicable supplements. Keep all three board columns. For a synthetic adult Double row before country adjustments: `cost=200`, `single_supplement=200`, `hb_supplement=null`, `fb_supplement=null`, `ai_supplement=0`. This rule is specific to AI-only lodges; mixed-board properties still use independently supported board differences under [the baseline and independent increments](#independent-increments).

## Independent increments

Each supported board supplement adds directly to `cost`:

```text
BB = cost
HB = cost + hb_supplement
FB = cost + fb_supplement
AI = cost + ai_supplement
```

HB, FB and AI are alternatives, not a cumulative chain. Their exact meal/service inclusions come from the supplier; a label alone does not establish which lunch, dinner, drinks or activities are included. Apply the user's clarified HB-dinner default and compulsory-component treatment in [meal meanings and compulsory components](#meal-meanings-and-compulsory-components).

These are emitted import-cell meanings, not interpretations of blank source cells. Establish whether a supplier option is unavailable, unquoted or represented by a merged cell. An unquoted option remains unresolved; a blank output does not certify supplier unavailability, and an unknown price must not be invented as free.

| Import cell | Calculator meaning |
| --- | --- |
| Blank/null | Option inactive in this output |
| Numeric zero | Option available and included |
| Positive amount | Extra per-person amount above the baseline |

The calculator can choose the most inclusive available plan at no higher price, considering AI, FB and HB. Never fill all empty board cells with zero for convenience.

Repeat a price check with a different board and again with the original board. Verify that an unavailable board stays unavailable and an included option remains available at zero increment.

Synthetic example: base 100, HB total 120, FB total 150 yields `cost=100`, `hb_supplement=20`, `fb_supplement=50`. Adding HB to FB would overcharge.

Normalize the source unit before calculating the increment. If HB and FB are both total-room quotes, subtract those room totals and divide by the applicable occupancy basis before storing a per-person supplement. Synthetic double-room example: HB 240 and FB 280 gives base 120, HB zero and FB 20 per person, not FB 40 per person. Reconstruct the full occupied-room price to catch this error. An independently priced extra lunch is not automatically the same as the supplier's HB-to-FB package difference.

Use the matching BB/HB/FB package differences when those totals are quoted. A separately sold restaurant meal may cost more than the package upgrade and does not replace that difference. This applies independently to each edition and guest band.

Retain a discount's explicitly stated board scope. An HB/FB-only child policy does not establish a child BB price, and mixing adult BB and child HB in the same baseline would misrepresent inclusions. A fixed packed-lunch quote can support a packed-lunch board option when described accordingly; a dining price stated only as "from" an amount does not establish a fixed dining lunch tariff.

Calculate board differences independently for each room category, capacity and season; a standard-room increment does not establish the family or extra-bed increment. Equal AI prices across two seasons do not establish equal upgrades when the HB baselines differ: derive each difference from the matching source row, with the same occupancy and tax basis. Within a collection PDF, bind every board reduction and inclusion footnote to its named properties and source version. A neighbouring hotel's reduction cannot establish a cheaper board for an unnamed property. Game-package services such as drives and transfers are a distinct bundle, not automatically AI or a meal upgrade.

Check property-specific exceptions against the collection's general inclusion paragraph. A hotel explicitly sold on BB remains BB even when neighbouring lodges include FB or drinks. A separately quoted lunch supplement on an existing FB package is not an ordinary BB-to-FB increment. Correct a generic board label in the review evidence without changing the supplier source or interpreting zero-valued workbook meal fields as proof of included meals.

Also test partial occupancy separately for every offered board. The model has one missing-place supplement, not a separate one per board, while meal increments are charged to matched guests. In that synthetic example, a single adult with supplement 120 costs 240 on HB but 260 on FB. If the supplier requires the full FB room total of 280 even for one adult, the simple encoding cannot preserve both boards at every occupancy. Record the exact discrepancy and accepted modelling policy or leave the affected case unresolved; a full-room match alone does not prove universal supplier fidelity.

Synthetic full-board-only example: `cost=100`, `single_supplement=100` under the ordinary fixed-room convention, blank HB, `fb_supplement=0`; if AI costs 85 extra over the baseline, `ai_supplement=85`. The zero FB records included board, not a fabricated free supplier upgrade from a separately sold BB product.

For a lodge offering **only AI packages**, use the [14 October AI-only encoding](#all-inclusive-only-lodges-14-october-2026). Do not reuse the FB-only example's zero FB for an AI-only lodge. Mixed-board properties retain the independent increments above.

## Children, infants and holidays

- Derive child supplements from the source's stated meal discount and base; do not assume a room discount also applies to meals. If the source discounts the whole selected board package, reconcile that discounted total: discounting only the accommodation baseline while retaining the full adult board increment overcharges the child.
- Derive board and drinks age bands independently from accommodation bands. A teenager charged adult accommodation may still qualify only for a non-alcoholic inclusive package; do not propagate the accommodation cutoff into meal or alcohol eligibility.
- Free accommodation does not establish free supplier meals. Preserve an explicit meal charge as source evidence and distinguish it from the [free-infant preparation default](child-policy.md#child-rates-and-unspecified-extras); a broad youngest age band is not automatically an infant policy. Apply the [zero-cost-row output rule](occupancy-and-ages.md#current-output-rule-adult-cost-supplement-8-october-2026), and record any difference from source billing as the accepted encoding policy. If "50% of total rate" leaves its base ambiguous, record that ambiguity rather than choose the room cost or meal increment silently. Unavailable plans remain distinct from applicable infant zeros.
- Read Christmas/New Year meals, compulsory dinners and special-date policies separately. Keep their dates and eligibility explicit; do not bury a mandatory seasonal amount in an unrelated year-round supplement.
- Distinguish an event tariff replacing the normal room price, a supplement charged per guest on every festive night, and a compulsory dinner charged once per event. A starred festive period does not widen a separately listed set of event dates. A minimum stay and a requirement to include a named holiday are independent conditions.
- Reconcile holiday increments without double counting included meals. Booking, stay-length and occupancy conditions can have representation limits. A one-day hotel season is valid under [the confirmed user rule](dates-and-seasons.md#valid-single-day-seasons); a checker mismatch does not invalidate it or block file preparation. Preserve exact dates and report actual importer acceptance separately.

If a full-board quote also explicitly permits a cheaper half-board option, that establishes a possible lower baseline, subject to confirmed units and eligibility. Derive the supported HB baseline and positive FB increment only when the source supplies enough information. Do not emit a negative HB supplement against an FB anchor, pretend both boards are free, or subtract an invented rebate. Keep unresolved unit or scope questions open.

Verify all three cell states, independent arithmetic, inclusive-only packages and age-specific exceptions against both the supplier and the selected schema. Older files may lack `ai_supplement`; absence is schema history, not evidence of a zero or included AI option. New hotel outputs must include that column under the [8 October representation rule](../general/schema-and-validation.md#current-hotel-output-representation), keeping unavailable AI blank/null.

## Scoped meal questions and holiday review

| Source ambiguity | Decision to retain |
| --- | --- |
| Ordinary meal prices are excluded on special dates, but only lunch or dinner receives a replacement quote | Resolve the unlisted counterpart. Ordinary-price fallback is a possible human-approved modelling rule, not an implied supplier quote. Do not silently use zero or invent a festive package. |
| A menu is priced, but compulsory participation is unclear | Establish whether the base booking must pay it before including it in cost. Reuse an answer already supplied for that scope. |

An approved ordinary-meal fallback or date correction is not a standing rule for every lodge. Record it separately from source facts, including document edition, dates, affected components and any limits. Do not repeatedly ask the same question after that decision is settled.

Start each holiday row from the room and age tariff applicable on that exact date. Change only the supported event components. Copying another festive block can import its peak-season accommodation into a shoulder-season holiday; a correct meal amount does not validate the room base.

Use [dates and seasons](dates-and-seasons.md#scoped-source-year-corrections) for conflicting printed event years and [undated Easter supplements](dates-and-seasons.md#undated-easter-supplements) for the confirmed missing-calendar default. A calendar resolution does not decide meal amount, compulsory purchase or replacement arithmetic.
