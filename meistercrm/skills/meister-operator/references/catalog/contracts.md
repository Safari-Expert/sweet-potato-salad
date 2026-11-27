# Individual catalog contracts

Read [Approval Gates](../approval-gates.md) at the start of every run. Use this page for a dated rate, supplement, fare or fee under a catalog item. Use `list_catalog_contracts` for the parent item and `get_catalog_contract` with `kind`, `parent_id` and `contract_id` for the exact rate. Use `describe_catalog_type` for the available rate fields. If the required tool is unavailable, open the item in **Catalog** and use **Contracts**. For a room rate, select the hotel and then its room.

## Identify the rate

For a website itinerary with zero or illustrative pricing, follow [Demo items and rates](demo-itinerary-items.md) for the parent, placement and coverage to use for each service.

Confirm the [parent item](master-records.md), workspace or shared owner, currency and effective dates. Match the row's other conditions as well. An amount or a season name alone may match several rates.

For hotel rates, follow the [hotel contract review and pricing notes](master-records.md#hotel-contract-review-and-pricing-notes) guidance when an unanswered question blocks a rate or a known adjustment requires manual pricing.

| Rate | Check these terms |
| --- | --- |
| Room | Hotel and room, dates, ages, party-size band, base cost, single supplement, and half-board, full-board or all-inclusive supplement. Check the meal plans offered by the hotel. A meal-plan supplement of `0` is free. A `null` supplement is unavailable. |
| Activity | Activity, dates, minimum/maximum age, minimum/maximum party size and cost. Group pricing and capacity are activity settings. |
| Transfer | Transfer, daily or taxi service, dates, party-size band and cost. Match origin, destination and direction when applicable. |
| Flight | Airline, origin, destination, departure/arrival times, operating frequency, dates, age band and fare. Several fare rows can belong to one flight service. |
| Add-on | Add-on, dates, age band, party-size band and cost. Its master sets placement and group/person pricing. |
| Location or park fee | Location, fee description, dates, per-person or group basis and cost. Person fees can also specify age bands, overnight and camping amounts. Check the location's currency and group-capacity settings. |

## Change and verify

- **Read.** Open the rates for the identified parent. If multiple rows match the request, show the differences and resolve which ones the user means.
- **Create with `create_catalog_contract`.** Add the intended dates, terms and cost under that parent. Check existing rows for overlapping terms. Save and find the new row again under the same item.
- **Edit with `update_catalog_contract`.** Open the matched row, change only the requested fields and save. Reopen it and verify both the changed terms and the adjacent rates.
- **Delete with `delete_catalog_contract`.** Identify each selected row, its parent and the coverage that will disappear. Follow the deletion gate before removing it. Reload the parent's rates and confirm the other rows remain.

**Example.** If the user changes July's price and the existing season covers June through August, updating the whole row would change three months. Identify how to preserve June and August at their original terms without gaps or overlapping July rates. Retain age, party-size and supplement conditions. If the change requires deleting the old row, obtain approval for that effect. Verify coverage immediately before, during and after July. If the available tools cannot safely complete the split, direct the user to the Contracts tab.

For an unavailable half-board supplement, send `"fields": {"hb_supplement": null}`. For free half board, use `"fields": {"hb_supplement": 0}`. Omit `hb_supplement` when editing only the base cost.

To check a quoted price, open the item’s **Simulate** tab in MeisterCRM where available and enter the requested date and party. Reopening the rates verifies that the edit was saved. Simulation verifies the price for the chosen inputs.

[Back to the skill index](../../SKILL.md)
