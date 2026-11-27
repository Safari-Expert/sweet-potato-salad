# Location contracts

For location fields, follow the shared [live location-reference category](../location-reference/live-reference.md) on every run; use the intended customer's filtered reference when validating that customer's availability.

Use for entry, access, conservation, reserve, sanctuary and marine-park fees, including supported flat or vehicle charges. Read [shared schema and validation](../general/schema-and-validation.md) and [source ETL](../general/source-etl.md) first.

## Row meaning and field mapping

One row describes one location fee rule for a contract type, age band, validity period and a fixed combination of base charge and supplements. Use the twelve-column location template when working from older eleven-column exports. Do not add `contract_name`, CSV pax bounds, resident category, `age_min`, `age_max`, `price` or provenance columns.

| Field | Location-specific meaning |
| --- | --- |
| `location_name` | Exact reference name for the place charging the fee. A similarly named park, airstrip or town is not interchangeable. |
| `contract_type` | `person` for a charge per visitor; `group` for a supported flat, vehicle or other non-person charge. |
| `description` | Empty for `person`; required, concise and stable for `group`. Identify the actual charge, such as `Vehicle entry fee`. Do not put research commentary or monetary amounts here. |
| `cost` | Main entry/access or flat fee in the stated currency. Do not replace it with a resale price or an age-category marker. |
| `overnight` | Additive overnight supplement. Keep it separate from `cost`. |
| `camping` | Additive camping supplement. Keep it separate from both other amounts. |
| `currency` | Currency of these amounts; follow the shared source-currency and catalog-currency checks. A USD preference does not authorize silently relabelling local-currency prices. |
| `tax` | Retain the selected schema's column; supplied location examples leave it empty and the published template provides no basis for treating it as a payable addition. Do not invent or calculate a tax value. Escalate meaningful nonempty source tax when its preservation affects the result. |

Use the location template without pax columns. A flat fee belongs to its named group product.

For a synthetic adult tariff of entry `120`, overnight supplement `30` and camping supplement `20`, map to `cost=120, overnight=30, camping=20`. Do not make three person rows with overlapping eligibility, and do not collapse the values into `cost=170`. This example explains the mapping, not a real tariff or reference location.

## Extract the tariff's actual distinctions

1. Identify the managing authority, tariff validity, visitor category, charge basis and exact location for each fee. Historical project requests defaulted to foreign non-resident/international fees; obey any current request for a different category. Keep tariff categories in extraction notes, not invented CSV columns.
2. Extract each published age boundary and amount independently. Published child amounts, free ages and restrictions differ by authority and sometimes by park. Do not calculate a child rate as half the adult rate unless the source expressly defines that ratio. Equal adult and child fees also require evidence rather than automatic correction.
3. Include a free age row when the source establishes eligibility at zero cost. A minimum admitted age, missing tariff or silence about infants does not establish free entry. Do not borrow another park's child definition to make coverage look continuous. Record unresolved eligibility outside the CSV; preserve confirmed rows without presenting the unresolved dataset as complete.
4. Distinguish entry validity from an overnight supplement. A 24-hour ticket that must be bought again for a second day is not automatically a separate overnight amount. Conversely, a separately stated bed-night or overnight levy must not disappear just because entry also exists.
5. Determine whether camping is a supported additive supplement for the selected tariff, a separate operator product, or one of several mutually exclusive campsite categories. Do not sum optional alternatives or select one without evidence. A permit, guided activity or border charge is not automatically a park-entry fee; use the relevant domain when it is a separate service.
6. Encode absent/nonapplicable supplement fields as numeric `0`. If the source is missing rather than establishing absence, record that distinction in the review notes. Never use this convention to invent a free main `cost` or to hide a known but unresolved paid supplement.

Do not freeze past national tariff amounts or park age policies into new work. Open the governing authority’s actual tariff for the requested period. Search snippets and prior exports are insufficient evidence for amounts, age policies or the completeness of a park list.

## Fee families, ages and seasons

Compare person rows by the resolved location and fee type. Distinguish actual group-fee families with stable descriptions. Changing capitalization does not create a distinct fee.

Within each real family, ensure age/date bands do not produce multiple applicable prices. If base cost, overnight or camping changes, split at every affected seasonal boundary and carry the correct complete combination on each row. An adult seasonal change does not imply a child seasonal change. Preserve the actual tariff's valid period; an annual convenience format must not extend an expired tariff.

For an explicitly requested year rollover, preserve month/day boundaries and every non-date field unless the user requests other changes. Compare rows after the date shift: remove only exact duplicates, and surface differing costs or supplements that now collide. Check year-specific camping and overnight amounts against each available edition. This operation copies an instructed scenario; it does not verify future supplier prices.

## Final checks before import

- Leave person descriptions empty and identify each group-fee family in its description.
- Distinguish different charge families using their source meaning.
- Preserve fractional `overnight` and `camping` amounts exactly. Check that a quoted 12.75 still reads back as 12.75.
- **Validator scope:** use the shared validation workflow. Passing age/date checks does not establish tariff accuracy, current validity, successful tax preservation or deployment parity.
- Check finite nonnegative costs, actual visitor scope, date/age coverage and overlap with existing contracts.
