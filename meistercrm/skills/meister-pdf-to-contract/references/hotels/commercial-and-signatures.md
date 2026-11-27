# Hotel buying-rate evidence

## STO buying rates only

- Use STO (special tour operator / B2B) buying rates. Never use a RACK/retail/B2C amount directly as the contract buying cost. Use an explicit STO buying table first; where STO is absent, use the identified NET buying table rather than RACK. Retain the selected source label and applicability. Contradictory NET amounts or discount formulas still require the commercial-evidence checks below.
- Where both appear, identify the correct table or column and retain its heading, currency, unit, market, validity and footnotes. Column position or the cheapest number is not reliable evidence.
- When eligible buying rates have alternative VAT-exclusive and VAT-inclusive tables, apply the [VAT-inclusive table preference](../hotels.md#vat-country-adjustments-and-rounding). This selects a published buying tariff; it does not authorize VAT arithmetic or substituting RACK.
- An explicitly stated STO discount or derivation may be calculated from its stated base. Record the formula; never invent a discount or assume a commission turns RACK into STO.
- Retain a supplier's levy formula and any RACK-based calculation as source evidence separate from the STO accommodation buying rate. Government-fee preparation is governed solely by [hotel VAT and country adjustments](../hotels.md#vat-country-adjustments-and-rounding); do not revive a superseded source-cash allocation through commercial interpretation. A levy reference to RACK never selects RACK accommodation. Preserve differing source wording privately alongside the applied country policy.
- Check the discount's component scope: accommodation-only discounts do not reduce separately quoted meals. When source evidence or an explicit user answer confirms that the STO discount covers all quoted pricing components, apply the same factor exactly once to accommodation, extra-person/bed charges, source single-occupancy deductions and HB/FB/AI upgrades that are quoted. Preserve the direction of a deduction; a source single-use tariff remains distinct from the current output's adult-cost `single_supplement` convention. Do not discount an already NET/STO amount again or expand the answer to another supplier, edition or agreement.
- If no RACK/retail rates are mentioned and rates are otherwise unlabelled, the user's convention is to assume the supplied rates are STO. Record `rate_basis=STO` with `rate_basis_assumed=true` and the evidence scope. Do not describe assumed STO as explicitly labelled STO.
- Apply that assumption to supplier evidence, not an unlabelled curated CSV or workbook. Establish the output's property and rate dates first. An expired supplier sheet can support historical diagnostics without establishing later buying rates; a mixed-year output needs separate authority for each year. Keep unsupported output scope unknown rather than inheriting the supplier's assumed-STO label.
- RACK-only documents without an explicit STO derivation cannot supply buying rates. Preserve the source and mark the affected conversion unresolved. Explicit retail wording takes precedence over an absence of the literal word "RACK".
- Read each table's pricing scope. Select the requested room, market, valid dates and package from the supplied rates.
- Take season boundaries and conditions from the selected STO table too; a neighbouring RACK table can use different dates. Keep labels for different market or residency tariffs distinct when they change the price.
- Verify STO selection for each room/occupancy cell and separately charged meal or service: one component can match RACK while another matches STO. A workbook-wide label or a matching accommodation quote does not validate its single-use quote or meal supplement. Keep an explicit all-guests fee separate from discounted lodging; free accommodation does not waive a fee whose source scope includes every guest.
- A commissionable trade offer is not automatically a net buying quote. Preserve gross/net basis, eligible products, settlement terms and stay-length conditions; commission and markup are different operations. Resolve the supported buying-cost derivation instead of inferring it from a zero margin or a generic TO heading.
- Visually resolve merged or visually shared cells within their labelled room/season columns. Blank extracted text can mean a shared table cell rather than unavailable pricing. Do not let a parser shift a neighbouring RACK amount into the STO column.

## Current nightly-rate scope

For this hotel-output workflow, use the ordinary **one-night accommodation tariff**. Exclude conditional length-of-stay discounts, optional game-package supplements and activities from that baseline, even when printed beside it. Retain their source scope in private evidence. This is the user's 8 October preparation policy, not a claim that the supplier offers no packages or that a minimum-stay condition can be ignored.

Do not strip included services from an inseparable source package to invent an unquoted room-only price. Where no ordinary nightly product is supplied, retain that limitation or obtain a scoped decision; [baseline and meal plans](meal-plans.md) still govern inclusive-only products.

### Park-fee exclusion and forced purchases

Prepare accommodation tariffs **exclusive of park fees**. If the lodge bundles park fees into its quoted tariff, or requires park-fee payment through the lodge as a condition of buying that tariff, flag the product for human review and block its automatic import. This includes mandatory supplier collection even when the fee is itemized separately. Record the relevant PDF page, included or forced fee, and the question needed to obtain a usable park-exclusive arrangement. Do not guess a deduction to manufacture a rate the supplier has not quoted.

Keep separately supported park-exclusive tariffs usable when the condition applies only to another product. Ordinary authority entry charges paid separately at a park gate do not, by themselves, make the accommodation tariff a forced supplier bundle. Do not infer fee inclusion from the destination label, or classify unrelated VAT, TDL or local charges as park fees; [hotel VAT and country adjustments](../hotels.md#vat-country-adjustments-and-rounding) remains their owner. Imported stays true for an already present hotel while its affected rates are blocked for review.

### Quoted options and request-only prices

Keep **unquoted request prices and configurations with no supported tariff outside published-rate scope**, rather than inventing a price or withholding supported rooms. An explicitly fixed-priced option remains usable even when availability is on request: retain its manual confirmation condition and apply its quoted units and guest rules. Record any exclusions; an unpriced optional fifth guest need not prevent completing a quoted four-place product. A source that quotes no usable ordinary accommodation tariff is still incomplete.

## Pairing and provenance

Use the tariff supplied or selected for this task. Keep each source's rates, validity, revision and terms together. If two distinct rate schedules cover the same pricing scope and the intended schedule is unclear after applying edition precedence, ask which tariff to use and continue with independent rates.

A collection PDF can supply rates for multiple properties. Verify the property sections, shared terms, validity and rate basis before linking each tariff to its hotel. Keep the supplier original and prepared files in the customer's authorized destination.
