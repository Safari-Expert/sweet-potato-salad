# Add-on contract conversion

For location fields, follow the shared [live location-reference category](../location-reference/live-reference.md) on every run; use the intended customer's filtered reference when validating that customer's availability.

Load this for separate optional services, extras, and add-on rate sheets. Apply [shared schema validation](../general/schema-and-validation.md) and [source extraction](../general/source-etl.md). The [header-only add-on template](../../assets/templates/addon.csv) records the inspected format.

## Product and charging model

One row represents an add-on product's age/pax band and date range. Master metadata includes its name, subtitle, description, scope/type, charging type, margin/tax settings, currency, and up to four feature pairs. Pricing rows carry the numeric eligibility bands, cost, and dates.

- `addon_price_type=person` means a per-person price. `group` means the whole group price. Do not infer this from the number of pax columns.
- `addon_type` is a product scope/type field, not the price unit. Preserve a supported value appropriate to the task/source. Examples include `global` and `local`. Check the connected schema. These examples alone do not establish which scope a new commercial product needs.
- Convert a supplier's percentage or package expression to an absolute cost only after establishing its unit and valid pax band. An optional per-person meal and a flat private-service charge must remain distinct models.
- Separate product metadata from actual contracts. A description containing a Markdown price list is still text; create separate supported rate rows for the individual payable services.

## Required data and features

Current add-on validation requires `addon_name`, `addon_sub`, `addon_desc`, `addon_type`, `addon_price_type`, `margin`, `min_age`, `max_age`, `min_pax`, `max_pax`, `cost`, `currency`, `start_date`, and `end_date`. Keep the complete current template including optional fields. A zero cost can be valid; it does not excuse missing currency or subtitle on a real contract row.

Use `addon_sub` as the intended subtitle, not a hidden unique key. If the source omits a subtitle, write a supported concise subtitle from the product's actual meaning or flag the missing identity detail; do not insert placeholder text. Preserve authorized descriptive copy while keeping prices in actual numeric contract fields when creating a priced service.

Feature columns are pairs: `feature_1` with `feat_desc_1`, through pair 4. If neither is supplied, leave both blank. If either is supplied, validation requires both. Supply the feature name and description in the import language. Map older `feature_name_i` / `feature_desc_i` headings to the selected template.

Repeated rows belonging to one add-on must agree on its descriptive metadata and features. Set the intended subtitle and feature copy consistently across rows. If a later row disagrees, resolve whether it is a correction or a different product.

## Three different grouping concerns

| Purpose | Current observed key | Practical consequence |
| --- | --- | --- |
| Import bundle/master identity | addon_name + addon_type + addon_price_type | Subtitle and currency do not split bundles |
| Currency consistency | addon_name + addon_type + addon_price_type | A real master must use one raw supplier currency |
| Overlap/continuity validation | addon_name alone, case-insensitive | A different subtitle or scope cannot safely hide overlapping rates with the same name |

A different subtitle alone does not establish a distinct price rule. Resolve genuine commercial variants with stable product identities.

## Scope boundaries and source transformation

Read source exclusions carefully. A separately listed activity park fee is not automatically an add-on: entry, overnight, and camping fee logic may belong to location contracts. A meal or transport already included in another price should not also become a chargeable add-on unless the task/source makes it a separate purchase.

Create only the age/pax/season combinations supported by the add-on terms. Avoid copying activity or hotel age defaults into extras such as equipment, private services, or fees. Preserve free eligible bands when explicitly applicable; missing prices and prohibited participation are not zero-price offers.

Descriptions/features can contain commas, quotes, and line breaks. Serialize them as properly escaped CSV cells and parse the saved file to verify one product record remains one row. Do not flatten a legitimate rich description into arbitrary separate contract rows.

A spa menu printed in a description can list several prices while the enclosing row has zero cost, a blank currency or no subtitle. Match the selected service to its amount, date, eligibility, unit, currency and required subtitle before building its commercial rows. Verify that readback by name has kept its intended scope, charging unit, currency and up to four complete title/feature pairs.

## Final add-on checks

Confirm the requested scope and price unit, all mandatory metadata, feature-pair completeness, consistent first-row metadata across the master, and complete currency. Validate date/age/pax overlaps across rows sharing the name, then apply shared output checks. Reconcile each actual add-on rate to source evidence separately from descriptive examples or menus.

Apply [checking gates](../general/checking-gates.md) with these add-on distinctions:

- Confirm that the source supports the selected charging mode and product type.
- Check all four feature pairs and stable first-row subtitle/description/features. Normalize unintended master spelling differences only after verifying identity.
- A subtitle does not split global overlap groups, but a **single-target** import must match both the existing `addon_name` and `addon_sub`. Check target currency and the union with existing contracts as well.
- Review date/age/pax coverage for the actual offered service. Apply the shared closure-exception procedure to documented non-operation periods; do not manufacture a free add-on during an unavailable period.
