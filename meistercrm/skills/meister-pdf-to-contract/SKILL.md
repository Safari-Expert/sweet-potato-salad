---
name: meister-pdf-to-contract
description: Convert supplier PDFs, spreadsheets and amendments into MeisterCRM contract CSVs, a two-sheet rate workbook and property-specific source PDFs. Use for hotels, activities, flights, transfers, location fees and add-ons, including source interpretation, pricing and file validation.
---

# Meister PDF to Contract

Use this skill to prepare files for review. For an import request, give **Meister Contract Operator** the reviewed workbook and source evidence, the intended workspace and master if known, and the outstanding questions for held rows. For file preparation alone, finish at delivery.

Turn the supplier’s current terms into traceable, import-ready rates. Begin with the supplied source and amendments, the requested rate scope, validity window and destination. A destination can be a connected Google Drive folder or an explicitly supplied local directory. Use the customer's connected Drive by default. Resolve the intended folder by ID and check for existing lodge files before creating anything. Ask for a destination only if access or matching is genuinely ambiguous.

Keep supplier prices, documents, customer identifiers and files within the customer-selected destination and connected CRM. Use the host’s supported file/document tools or the included local helpers for file handling. No network service is required for local preparation.

## Prepare the rates

1. Inventory source editions, printed and physical PDF page numbers, suppliers, properties, services, currencies, eligibility, geography and effective dates. Identify shared terms before splitting a multi-property PDF. Record the exact commercial scope of each table. Read [the evidence and delivery rules](references/delivery.md).
2. Open the detailed workflow in the guides below for each item family. For a quick orientation, select the relevant [hotel](references/hotels.md), [activity, transfer or flight](references/transport-activities.md), or [location or add-on](references/locations-addons.md) rules. Treat a confirmed customer instruction as authoritative within its stated scope. Apply newer applicable amendments over earlier terms, then specific dated terms over general terms. Record any instructed departure from a supplier term. Use the explicit stay or service dates for the selected tariff. Prepare the user's selected rates regardless of which company is named on the supplied document or whether it has been signed. The same eligibility rule applies at import. Skip company-name, signature and signed-return checks. Apply the documented rules directly wherever their conditions hold. If the source, an applicable rule and existing customer decisions leave a material question unresolved, ask about the affected rows and continue preparing the rest.
3. Model payable rows using the exact ordered headers in `assets/templates/`. Keep source measurements, quoted amounts and page references alongside each row. Derive original/TDL/final evidence before import. Run [the portable helpers](references/local-tools.md) for the lodge PDF and the two-sheet workbook (Contracts, then Original). Use an existing matching workbook in place. Check unreadable scans against the rendered original. Treat numbers, signs, dates and table footnotes as unreliable until visually verified.

Use the current [client folder](references/general/client-folder-operations.md), [rule precedence](references/general/rule-ownership.md), [source extraction](references/general/source-etl.md), [location matching](references/location-reference/live-reference.md), [schema and validation](references/general/schema-and-validation.md) and [checking gates](references/general/checking-gates.md). For a connected lookup, verify the target workspace and its read permission before accessing customer records. Authorize live changes separately through **Meister Contract Operator**. If CRM lookup is unavailable, identify the unresolved reference for the operator. File preparation can proceed for independently supported rows.

## Select the rate family

- [Hotel contract conversion](references/hotels/workflow.md) · [CSV template](assets/templates/hotel.csv)
- [Activity contract rules](references/activities/workflow.md) · [CSV template](assets/templates/activity.csv)
- [Transfer contracts](references/transfers/workflow.md) · [CSV template](assets/templates/transfer.csv)
- [Flight contracts](references/flights/workflow.md) · [CSV template](assets/templates/flight.csv)
- [Location contracts](references/locations/workflow.md) · [CSV template](assets/templates/location.csv)
- [Add-on contract conversion](references/addons/workflow.md) · [CSV template](assets/templates/addon.csv)

## Prepare and check hotel rates

- [Hotel source intake](references/hotels/source-intake.md)
- [Hotel buying-rate evidence](references/hotels/commercial-and-signatures.md)
- [Hotel dates, seasons and operating scope](references/hotels/dates-and-seasons.md)
- [Hotel occupancy, ages and missing places](references/hotels/occupancy-and-ages.md)
- [Hotel child policy, ages and admission](references/hotels/child-policy.md)
- [Hotel baseline and meal plans](references/hotels/meal-plans.md)
- [Tanzania hotel VAT and Tourism Development Levy](country/tanzania/vat-and-tdl.md)
- [Hotel source and calendar tools](references/hotels/preparation-tools.md)
- [Reviewing a collection of supplier contracts](references/hotels/source-review.md)

For mainland Tanzania, Unguja and Pemba, apply the country rules for inclusions, adjustments and rounding. Check worked examples under [Reconcile the tariff against the workbook](references/hotels/workflow.md#reconcile-the-tariff-against-the-workbook). For saved rate-year tags and post-import checks use **Meister Contract Operator**.
