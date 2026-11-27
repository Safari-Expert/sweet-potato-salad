# Hotel child policy, ages and admission

## Derive age bands before expanding seasons

Read the actual inclusive/exclusive age wording, then produce disjoint integer bands. Synthetic example: free through age 2, child discount through age 16, then adult gives `0-2`, `3-16`, `17-99` when that adult upper bound is the selected convention. These are `min_age`/`max_age`, not pax fields. Do not copy these cutoffs into another supplier.

Distinguish "20% off" (pays 80%) from "pays 20%". For an unlabelled percentage use the [approved bare-percentage default](#unlabelled-child-percentages-21-october-2026). Record the relevant adult/room/meal base. Do not expand a prohibited child-age group into a zero-priced contract.

Build child rules by adult count and room arrangement before emitting age rows. One-parent, two-parent and child-own-room clauses can use different adult bases, discount denominators and age endpoints. An explicit parent-and-child package can replace the ordinary single-use adult amount; adding the usual single supplement to that package may overcharge. "Half the Double rate" must retain whether Double is a whole-room quote or a per-person sharing quote. Do not derive child accommodation ages from transfer, conservation or other fee exemptions. Preserve unquoted arrangements as unknown or apply only the separately documented user fallback.

Separate pricing ages from admission and accompaniment rules. A guest charged an adult rate can still require a parent or guardian in the booking; that does not establish a same-room sharing requirement. Preserve the source's booking, room or property scope, and test eligibility independently from the tariff.

A free extra bed is not necessarily free child accommodation or a waived additional-guest charge. Preserve those components and their sharing conditions separately. When an explicit child tariff disagrees with generic percentage prose, retain both with their room/board/market scope; do not silently choose one or create a universal child price. Literal "over 65" excludes age 65; do not convert exclusive age wording into an inclusive boundary.

Once source child rules are extracted, apply the [current child-composition decision sequence](#child-rates-and-unspecified-extras). Retain the original condition, selected tariff or fallback, and price impact in private evidence. This accepted modelling simplification does not establish unquoted adult extra-bed eligibility or physical capacity.

## Unlabelled child percentages, 21 October 2026

When the applicable child-pricing clause gives only a percentage, without saying “discount/off” or “pays/of the rate”, treat a percentage **below 50% as a discount**: `child_price = stated_base * (1 - percentage / 100)`. For example, bare `25%` means the child pays 75% of the stated base, not 25%. Explicit wording or a scoped human answer controls instead; “pays 25%” still means 25% payable. At exactly 50%, either reading produces half price. This instruction does not settle an unlabelled percentage above 50%; use further source context or retain that ambiguity.

Apply the default only after identifying the applicable age, sharing arrangement, component and adult/room/meal base. It does not resolve a missing base or extend an accommodation discount to meals. Record the source wording/page, assumed discount and resulting payable fraction privately, and remove only the blocker resolved by this default.

## Child rates and unspecified extras

If adjacent published age brackets omit a boundary age, the 10 October preparation default assigns that missing age to the **lower age bracket**. For example, "under five free" followed by "six to twelve" includes age five in the free band. Record the default separately from the literal wording; it fills an omitted endpoint, not an unknown tariff for an arbitrary age range. Explicit exclusions and resolved property-specific answers still control. This is an **omission**, distinct from two bands both including an age; shared endpoints use the later [overlapping-age rule](#unresolved-overlapping-age-endpoints).

When a source explicitly prices an inclusive child band but generic admission wording excludes that same lower endpoint, the 10 October user answer treats the priced endpoint as admitted. Retain the rest of the admission restriction: an explicit five-to-twelve tariff supports age five, not admission of ages zero to four. Distinguish this contradiction from an unpriced omitted endpoint before applying the lower-bracket default.

When published older age bands make the youngest unpriced band clear, the user's normal preparation convention is to treat that youngest band as free infants, including applicable meal supplements. Record that this is a business default, not a quoted supplier tariff. Do not invent a child accommodation discount: an unqualified per-person tariff also applies to paying children unless a source discount or a scoped user decision establishes otherwise. Do not carry a child policy from another contract edition merely because the room name is unchanged.

Normal allocation places children with adults, but a free row does not override admission, adult accompaniment, bedding or physical capacity. In particular, omit an infant-only capacity-one Single row when the source requires the infant to share with an adult. A free-child rule does not create extra places or permission for a child-only room. [Source eligibility analysis](#derive-age-bands-before-expanding-seasons) precedes the accepted child-composition fallback below.

This preparation workflow cannot enforce adult/child **count** restrictions such as exactly two adults and two children; normal allocation guarantees at least one accompanying adult in the room. The 11 October clarification selects an explicitly quoted **child sharing with one adult** accommodation tariff when prices differ by adult count. Do not apply the cheaper two-adult child condition when allocation cannot guarantee it. Preserve that quote's age, room and charging basis; a reference to the Double sharing amount is not automatically the matching Triple adult amount. Record the original condition and the accepted one-adult simplification privately rather than leaving the adult-count decision as a blocker.

Where no applicable one-adult child tariff is quoted, retain the approved adult-accommodation fallback; preserve independently calculable child meals. Normal allocation does not create a child-only Single booking. This clarification does not supply an unknown price, physical capacity, or adult extra-bed eligibility: a child-only third bed is not evidence that a third adult is permitted.

For the equivalent case of a child-only third place without a supported adult Triple, the user's 11 October choice is to retain the ordinary **capacity-two** product and record the child-only place as a manual-booking option in hotel master notes. Do not create an unrestricted capacity-three variant or keep the already settled representation choice as a pricing blocker. Retain the excluded option's source eligibility and quoted price privately; this does not resolve an unrelated missing room capacity, tariff or meal amount.

Keep an approved adult-price fallback for unrepresentable **child accommodation composition** confined to that component. Preserve independently calculable child meal discounts. A source discount covering room and meals must be assessed against each component's stated base; a general meal discount may cover a festive dinner addition, but record that as a scoped deduction when the festive child price is not printed separately.

For a known per-person extra with no specific child rate or exemption, the user's normal fallback is the full fee for paying children and no fee for free infants. Use the actual lodge's age bands, not ages copied from the example that established the convention. Explicit component-specific discounts or exclusions take precedence. This fallback resolves fee-age silence only: it does not supply an unknown amount, unit, event date or compulsory status. Government-fee decisions belong in [hotel VAT and country adjustments](../hotels.md#vat-country-adjustments-and-rounding).

## Extra-place and child-only quotes

- When a child pays a percentage of an **extra adult**, apply it to the stated extra-person charge, not automatically to the adult sharing rate or an included room place. Preserve the base room/bundle and identify whether that child occupies an included or additional place; a correct discounted extra fee alone cannot validate the complete mixed-party total.
- A child-only room or group price is not an unconditional child tariff for sharing with adults. Retain the exact party condition and discount base. If the schema cannot express it, use the documented user fallback or keep the case unresolved; do not infer the missing sharing rate from the child-only price.

The [occupancy examples](occupancy-and-ages.md#establish-units-and-room-identity) retain the complete family-bundle and positional-price calculations. Apply their party reconstruction before choosing a child fallback; a matching all-adult total alone does not validate a mixed party.

<a id="unresolved-overlapping-age-endpoints"></a>

## Overlapping age bands, 21 October 2026

The earlier instruction to require a separate human answer for every shared endpoint is superseded by the **21 October 2026 higher-charge default**. When overlapping printed pricing bands have the same room, dates, component and sharing scope, allocate the shared age to the higher applicable charge to avoid underquoting. At an ordinary child-to-older-child or adult transition, end the lower band one year before the next starts: `0–8` and `8–12` become `0–7` and `8–12`; if adult pricing begins at 12, the middle band instead ends at 11. Similarly, `8–15` and `15–99` become `8–14` and `15–99`. If free and paying child bands both include age five, age five belongs to the paying band.

Preserve all other ages and source conditions, producing exactly one applicable price per eligible age. If two equivalent bands quote the same price, merge their coverage or split it without duplicates. Nested bands such as `8–12` and `8–15` need their scopes compared, not an invented age-12 tariff: use the higher applicable charge across a genuine same-scope pricing overlap, while preserving the rest of each band's coverage. Do not use this rule to mix incompatible sharing arrangements, override an explicit admission ban or invent a missing charge. Those unresolved scope/base questions remain blockers.

Keep the printed bands, source page, normalized bands and boundary price checks in private evidence. This is a user-approved conservative preparation policy, not a statement of supplier intent. An explicit scoped human boundary answer remains controlling. The older lower-band rule for an **omitted** age remains separate.
