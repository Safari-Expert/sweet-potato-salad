# Tanzania hotel VAT and Tourism Development Levy

Use this guidance when preparing accommodation rates for a property in Tanzania. Establish the actual island or mainland location before choosing a levy treatment.

## VAT on the published buying rate

When equivalent eligible STO/NET tables are published with and without VAT, use the VAT-inclusive table. Keep quoted amounts unchanged when only a VAT-exclusive table exists. Preserve the supplier’s VAT wording on `Original`, keep a supplied hotel `tax` field at zero, and make the TDL inclusion decision separately. A generic “tax included” clause alone does not establish that TDL is included. See [hotel VAT, country adjustments and rounding](../../references/hotels.md#vat-country-adjustments-and-rounding).

## Mainland Tanzania: TDL only, at 1%

For a lodge whose resolved location is **mainland Tanzania**, use **1% Tourism Development Levy (TDL)**. Country alone is insufficient: first exclude Unguja (commonly called Zanzibar) and Pemba Island under the regional rule below. Resolve the property's actual geography, not its folder label; a mainland property listed on a Zanzibar tab still follows the mainland rule. Ignore separately quoted dollar/currency TDL amounts and alternative source percentages when calculating the addition. Do not divide a monetary fee by `max_pax`, derive a fee from RACK, or use a previously recorded cash amount to override this rate. Missing or conflicting source cash fees do not block this settled preparation policy.

Account only for TDL in this government-fee step. Ignore other separately quoted government taxes, levies and fees. Do not strip VAT or other included charges out of an inseparable published tariff. Ordinary accommodation, supplier meals, festive supplements and extra-bed pricing still follow their respective source and user rules; they are not government fees.

Apply 1% to the **entire represented hotel booking value**, including each applicable monetary rate field:

| Field | Adjustment when TDL is not already included |
| --- | --- |
| `cost` | `round_money(base_cost * 1.01)` |
| `single_supplement` | `round_money(base_single_supplement * 1.01)` |
| `hb_supplement` | `round_money(base_hb_supplement * 1.01)` |
| `fb_supplement` | `round_money(base_fb_supplement * 1.01)` |
| `ai_supplement` | `round_money(base_ai_supplement * 1.01)` |

Apply the same treatment to any additional actual hotel price component supported by the selected schema. Do not multiply percentages, margins, master `tax`, capacities, identifiers or date fields. Do not add another 1% to the reconstructed booking total after adjusting its component fields.

First resolve STO/NET buying prices, discounts, source board differences, compulsory meals, holiday splits, age rules and the ordinary single-supplement conventions. Then apply the country adjustment once and round final monetary values. A quoted Single's zero supplement stays zero; free infant zeros stay zero. Unavailable HB/FB/AI remains blank/null, never converted to zero. This percentage does not invent fee-age bands or cash minimums.

Retain the no-double-addition rule: where TDL is established as included under the evidence sequence below, preserve that included component and round it without adding another 1%. Apply inclusion at its established edition/component scope; VAT inclusion or a generic tax-included label alone is insufficient. Rebuild revisions from the unadjusted source/base components, rather than repeatedly multiplying an already revised workbook.

### Inclusion decision sequence

Resolve mainland TDL inclusion for each applicable edition and component before multiplying any price:

1. **Applicable PDF/source evidence first.** Explicit TDL inclusion means no increase; explicit exclusion means add 1%. A TDL-inclusive bundle is included even when village or other fees are not separately itemized. Ignore quoted cash TDL amounts or different percentages when calculating the authorized increase. Prefer applicable PDF evidence over a conflicting human flag.
2. **If the source is silent, use an authorized human inclusion check.** Record its provenance and applicable year/component scope. Do not treat an older broad `Includes TDL / Tax` flag as a TDL-specific finding without confirmation; VAT-only or generic tax wording is not proof of TDL inclusion.
3. **If inclusion is still unknown, use only a task/client-authorized default.** Where the user authorized adding 1% on silence, apply it and explicitly retain `UNSPECIFIED` evidence plus an assumed-default action. That scoped authorization persists for its client/task; do not repeatedly ask the same question. Without that authorization, keep the adjustment pending, retain the supported base rates and record the inclusion question. Silence does not prove exclusion and must not silently become a global default for all future clients.

This sequence determines whether the known **1%** increase applies; a missing cash fee or unlabelled cash-fee unit is not a new amount question. If evidence differs between editions or components, preserve the raw amount and decision for each. Adjust eligible components separately before recombining. The workbook helper’s row-wide multiplier cannot represent mixed inclusion bases.

### TDL evidence and action

Record the supplier’s TDL statement, its source and the action taken on `Original`. For mixed statements identify the editions, components and dates. Use the hotel’s `ai_source.ai_comment` only for a concise question whose answer is needed to price an affected rate. For example, when a mainland tariff is silent and there is no authorized default, ask “Do the 2027 full-board rates include TDL?” After resolving the question, replace it with the next blocking question or explicitly set `ai_comment` to `""` if none remain. Preserve the customer’s `ai_solution`. A known adjustment that a consultant must apply manually belongs in hotel `notes`. A levy already reflected in the contract rates needs only the workbook evidence. See catalog review (see **Meister Contract Operator**, Connected MeisterCRM workflow).

Apply the [inclusion decision sequence](#inclusion-decision-sequence), retaining evidence and action separately. Claim an adjustment was added only after the output is saved and checked. For Unguja/Zanzibar or Pemba, the regional non-applicability rule below controls irrespective of the recorded inclusion category; never treat island exemption as mainland exclusion.

| Evidence/result | Finding | Example evidence on `Original` |
| --- | --- | --- |
| PDF explicitly includes TDL, including in a bundle | INCLUDED | PDF includes TDL. No increase. |
| PDF explicitly excludes TDL on mainland Tanzania | EXCLUDED | PDF excludes TDL. Added 1% to cost and applicable supplements. |
| Silent PDF with authorized human confirmation of inclusion | INCLUDED | PDF is silent. Human check confirms inclusion. No increase. |
| Silent PDF with authorized human confirmation of exclusion | EXCLUDED | PDF is silent. Human check confirms exclusion. Added 1%. |
| Inclusion unknown, default addition authorized and performed | UNSPECIFIED | PDF is silent. Applied the authorized 1% default. |
| Inclusion unknown and no authorized default | UNSPECIFIED | Adjustment pending confirmation of TDL inclusion. |

For mixed editions or components, record each status and action on `Original`. For example, the 2026 edition includes TDL and the 2027 edition excludes it, so only the 2027 rates receive the 1% increase. Mark the nonuniform aggregate `UNSPECIFIED` with the explanation `Mixed by year/component`. Apply the established treatment to each component. Once every component is priced, this tax decision is complete.

For **Unguja/Zanzibar and Pemba**, retain the source inclusion category if explicitly stated, otherwise `UNSPECIFIED`. On `Original`, name the verified island and record that TDL does not apply and no increase was made. Exemption is not evidence of exclusion. Never infer the mainland addition from an island row's category. Do not introduce a fourth `N/A` category.

### Rounding and checks

Use decimal arithmetic and `round_money(x) = Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)` on final monetary values. Calculate base divisions and board differences before this final rounding. Rounding to two decimal places is numeric precision; retain the established display of numeric zero as `0` and preserve blank unavailable boards. Do not round `max_pax` or change spreadsheet date/flag conventions.

Synthetic example: `cost=100`, `single_supplement=100`, `HB=20`, `FB=40`, `AI=60` become `101`, `101`, `20.20`, `40.40`, `60.60`. Two adults on FB total `2 * (101 + 40.40) = 282.80`, compared with the unadjusted `280`. One adult in that Double on HB totals `101 + 101 + 20.20 = 222.20`, compared with `220`. A base `33.335` becomes `33.67` after the 1% adjustment and final rounding. Component rounding can create a cent difference from multiplying an unrounded whole-party total; validate and explain the actual serialized calculation rather than applying TDL twice.

### Preparation policy

The preparation guidance cites Mainland Tanzania’s Tourism Act No. 29 of 2008 and Government Notice No. 69 of 7 February 2025, regulation 2(b), on the bed-night levy and room tariff. Applying the adjustment to every eligible meal and supplement is a contract-preparation convention. Keep the supplier’s literal wording, verified jurisdiction and customer direction on the evidence sheet. Consult the current official text for a legal determination. [Government Notice No. 69](https://oagmis.oag.go.tz/portal/legislation/4344/download) · [Tourism Act No. 29 of 2008](https://www.maliasili.go.tz/assets/pdfs/TheTourismActNo29-2008.pdf)

## Zanzibar: Unguja and Pemba — no TDL adjustment

The preparation rule is **no TDL for Unguja (Zanzibar) or Pemba Island**, despite their country being Tanzania. Do not add the mainland 1% to `cost`, `single_supplement`, `hb_supplement`, `fb_supplement`, `ai_supplement` or any other monetary component for properties on either island. Source silence, an excluded-TDL statement, or a FALSE inclusion flag does not trigger the mainland default in these regions.

Document the island decision on `Original` as described in [TDL evidence and action](#tdl-evidence-and-action). Preserve published STO/NET amounts, ordinary supplier extras and the existing VAT policy. Keep charges embedded in an inseparable source price and exclude other separately quoted government fees from the TDL calculation. Final two-decimal monetary rounding, numeric zeros and unavailable-board blanks still apply.

Maintain one canonical two-sheet workbook. Correct an earlier island output that received 1% using the verified unadjusted source/base values. Dividing an already rounded adjusted file by 1.01 can lose the original cents.
