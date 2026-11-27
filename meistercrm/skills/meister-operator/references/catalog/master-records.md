# Catalog master records

Read [Approval Gates](../approval-gates.md) at the start of every run. A master record describes a reusable supplier item. Use `list_catalog_items` to find a match, then `get_catalog_item` with its `kind` and `id`. Rooms are listed or created under a hotel’s `parent_id`. Use `describe_catalog_type` before a write. `create_catalog_item` and `update_catalog_item` take `fields` for the intended changes. Country and location references support editing the workspace’s descriptive details. For country and location pictures or a missing destination detail, use [Destination setup](../destination-setup.md). For activity, hotel, room and transfer photos, follow the [gallery upload and readback steps](#descriptions-and-pictures-for-new-items). When a suitable tool is unavailable, guide the user through **Catalog** and the relevant item tab.

## Find, create or edit

1. Select the catalog type. Search or filter by name and use the location, supplier and owner to resolve similar entries. For a room, open the hotel and select the room. In the room drawer, **Room** edits the room type and **Hotel** edits the parent property.
2. To create, check for an existing match and follow [Descriptions and pictures for new items](#descriptions-and-pictures-for-new-items). Create the hotel before adding its first room. For a country or location, open the geographic reference and edit the workspace's content. Confirm which language to change.
3. To edit, open the current record and change the requested controls. Preserve other languages, files, pricing choices and related items. Shared entries can have read-only controls. Use the applicable **Create**, **Update** or save action and reopen the item to verify the saved change.

| Record | Main choices in the drawer |
| --- | --- |
| Hotel | Property name, localized description and gallery. Settings include location, supplier, tags and offered meal plans (bed and breakfast, half board, full board and all-inclusive). Pricing includes currency, supplier VAT, reclaim VAT, markup, ignore proposal markup and zero-cost item. Use Notes for [manual pricing exceptions](#hotel-contract-review-and-pricing-notes) and Documents for rate-sheet attachments. |
| Room | Room name, localized description, gallery and maximum occupancy per room. For a seasonal price or supplement open the room's [Contracts](contracts.md). |
| Activity | Name, localized description, gallery, location, supplier, tags, maximum capacity and duration in hours. Pricing includes currency, supplier VAT, reclaim VAT, markup, group pricing, ignore proposal markup and zero-cost item. Notes and Documents belong to the activity. |
| Transfer | Localized name and description, gallery, maximum passengers, supplier, tags and automatic proposal descriptions. Pricing includes currency, supplier VAT, reclaim VAT, markup, group pricing, ignore proposal markup and zero-cost item. Use **Vehicles** for fleet records, plus Notes and Documents for the service. |
| Flight | Airline name, localized description, gallery, automatic proposal descriptions, supplier and tags. Pricing includes currency, supplier VAT, reclaim VAT, markup and ignore proposal markup. Notes and Documents belong to the airline. Use Contracts for route and schedule changes. |
| Add-on | Name, localized description, supplier, tags and ordered features with localized names and descriptions. Choose placement within a day or across the trip, and group or per-person pricing. Pricing includes supplier VAT, reclaim VAT, markup, ignore proposal markup and zero-cost item. Notes and Documents belong to the add-on. |
| Location or park fee | Header, main and ending descriptions and media, source references and documents. Location pricing settings include currency, supplier VAT, reclaim VAT, markup, ignore proposal markup and maximum group capacity. Edit a named entry fee under Contracts. |
| Country | Header, main and ending text and media for the selected country and language. Preserve other languages and source references. |

**Activity duration.** For a 90-minute activity, send `"fields": {"activity_duration_min": 90, "duration": 90}` and check both on the saved master. The catalog drawer shows `activity_duration_min` in hours (1.5). The proposal activity header uses `duration` first, so a value of 120 there still shows two hours. It falls back to `activity_duration_min` if `duration` has no positive value.

**Choosing a pricing control.** Use currency for the denomination of the supplier's costs. Enter the supplier's tax treatment and item markup as requested. **Ignore proposal markup** controls whether proposal-wide markup applies to this item. **Group pricing** changes the unit being priced. **Zero-cost item** marks a deliberately free service. If a price is missing, inspect the applicable contract.

**Updating the fleet.** Match the vehicle by registration and check its make, model and capacity. Fleet records may also hold type, year, rating, vehicle identification number, color, fuel, transmission, insurance and inspection expiry, and notes. Verify the intended vehicle changed and the rest of the fleet is still present.

## Hotel contract review and pricing notes

Use the owning hotel’s `ai_source.ai_comment` only for a concise question whose answer is needed to complete a specific part of the contract work. Identify the affected room, dates or rates as needed. Read the current question and the customer’s `ai_source.ai_solution` before updating. Once the answer resolves the question, replace it with the next blocking question, or explicitly set `ai_comment` to `""` if none remains. Preserve `ai_solution` and read back both fields on the owning hotel.

Reserve hotel `notes` for known price adjustments or pricing rules the contract rates cannot apply. Briefly state when the rule applies and what the consultant must do. For example, “When one adult shares a furnished tent with one child, confirm the Single-based price manually.” Keep adjustments already included in the rates, such as an applied levy, in the contract workbook’s `Original` sheet.

## Descriptions and pictures for new items

1. Write a factual, customer-facing description for each new catalog item in every language required for the task. Each translation must contain **200–300 characters inclusive, excluding whitespace**. Count the visible description alone, including punctuation. For example, in Python use `len("".join(description.split()))` on the plain text. Count before saving and revise any translation outside the range. Use verified details about the item, its setting and what the guest experiences.
2. Search for at least one picture that depicts the specific item. Start with the operator’s itinerary or supplier media available for reuse, then search for a suitably licensed image if needed. Check the subject and retain any required attribution. Match rooms to the room type and hotels to the property. For an unnamed demo service, use a clearly labeled illustrative picture if appropriate.
3. Once the activity, hotel, room or transfer is saved, call `attach_catalog_image` with its `kind` (`activity`, `hotel`, `room` or `transfer`), its own `id`, and one JPEG, PNG or WebP as an `image_data` data URI, up to 5 MiB decoded. For a room, use the room ID. This appends to the gallery and preserves the cover and existing order. It uses the existing `catalog.update` grant and the user’s edit access to that record. Country and location photos use [destination slots](../destination-setup.md).
4. Keep the returned `file_id`. Reopen each saved item with `get_catalog_item` (requires `catalog.view`) and match that ID in the gallery returned for that kind (`activity_photo_id`, `hotel_photo_id`, `room_images` or `transfer_photo_id`, respectively). Recount each saved description. After an uncertain upload, read the gallery first. Retrying the same image bytes preserves a single entry. Report a visual preview only if you actually viewed it.

If the connected tool list omits the upload action or the item type has no supported gallery, identify the affected item and outstanding photo. For an MCP-only request, report the gap there. If the user wants CRM instructions, point them to the item’s gallery under **Catalog**.

## Remove an item

Use `delete_catalog_item` only after the user approves the exact removal. Show the user the item, workspace, owner and any affected children. Deleting an owned hotel removes its rooms and their rates. Deleting an owned room removes its rates. Deleting an activity can remove its images and contracts. The connector deletes workspace-owned records. If the user only wants to remove a shared item from their workspace, use the CRM sharing controls and confirm the exact effect displayed. For a single rate use [Contracts](contracts.md).

Obtain approval for the identified effect, perform the authorized action once, and verify the item or shared access is gone. If the outcome is unclear, inspect the current catalog before considering another attempt.

[Back to the skill index](../../SKILL.md)
