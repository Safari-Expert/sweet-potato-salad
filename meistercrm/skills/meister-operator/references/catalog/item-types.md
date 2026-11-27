# Catalog item types

Read [Approval Gates](../approval-gates.md) at the start of every run. Use `describe_catalog_type` to check which fields you can change for a parent item and its individual rates. Match the user’s request to a record type below. For activity, hotel, room and transfer photos, follow [Catalog gallery uploads](master-records.md#descriptions-and-pictures-for-new-items). For country or location images, follow [Destination setup](../destination-setup.md). Use the corresponding **Catalog** control for other media, spreadsheet import or export, and rate simulation.

| What the user names | What to identify | Where the change belongs |
| --- | --- | --- |
| Hotel or lodge | Property name and location | The hotel holds the property description, supplier, meal plans and property-wide pricing settings. |
| Room | Hotel and room type | The room holds the room description and maximum occupancy. Its Contracts tab holds seasonal rates and meal-plan supplements. |
| Activity | Activity name, location and supplier | The activity holds duration, capacity and pricing basis. Rate rows hold the date, age and party-size conditions. |
| Transfer | Transfer name, supplier and service type | The transfer holds vehicle capacity and fleet details. Rate rows describe daily or taxi services and applicable routes. |
| Flight | Airline, origin, destination and departure time | The airline holds the supplier and description. Its contracts hold the routes, schedules, operating frequency and fares. |
| Add-on | Name, supplier and whether it appears on a day or for the whole trip | The reusable add-on holds its description, features and group or per-person basis. Its contracts hold the rates. |
| Supplier | Supplier name and contact details | Use the supplier master to change its contact or payment schedule under the user's catalog permissions. To assign an existing supplier to an item, change the item's supplier selection. |
| Location or park fee | Location, country and fee name | The location has reusable destination content and pricing settings. The individual park or location fee is a contract. |
| Country | Country enabled in the workspace and content language | The country record holds the workspace's destination text and images. |

If names repeat, show the parent, location, supplier or other distinguishing details and ask which record the user means. Check whether the item belongs to the workspace or is shared before offering an edit.

**Examples.** “This room sleeps three” belongs in [Master records](master-records.md). “Change its July rate” belongs in [Contracts](contracts.md). “Load this hotel rates workbook” belongs in [Import and export](import-export.md). For “Use two rooms on this proposal,” check whether it is an owned Draft and follow the [proposal itinerary workflow](../proposals.md).

[Back to the skill index](../../SKILL.md)
