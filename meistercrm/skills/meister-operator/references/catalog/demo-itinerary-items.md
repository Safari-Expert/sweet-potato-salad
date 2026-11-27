# Demo items and rates for a website itinerary

Use the trip's [day table](../website-itinerary.md) to build the smallest reusable catalog that reproduces its days and overnights. Search by kind, name, location and owner before creating anything. Use an existing item and rate when they already fit the demo. When a commercial rate would change the requested result, create a clearly labeled demo item and rate for the illustration. Keep live supplier pricing intact.

Use `describe_catalog_type` for writable fields, `create_catalog_item` for a missing master and `create_catalog_contract` for an individual rate under the saved master’s ID supplied as `parent_id`. For rooms, create the room under the hotel and the rate under the room. Supply only fields supported for that kind. Set currency on the parent that owns it. Read back each item and rate before using it. [Catalog masters](master-records.md) · [Individual contracts](contracts.md)

For every item created for the demo, follow [Descriptions and pictures for new items](master-records.md#descriptions-and-pictures-for-new-items). Carry its saved ID and matched picture into the final check.

| Source itinerary says | Catalog entry and placement |
| --- | --- |
| A visit, excursion, welcome or descriptive arrival experience | Use an activity at the actual stop, with a localized name and concise description. Place it on the stated day. Use the activity's date, age and party-size rate for the demo. |
| A named hotel or an overnight in a town | Match the property at the overnight location. If unnamed, use a demo property called “Hotel in {overnight location}” and describe it without promising amenities. For a new demo hotel create one double room with capacity two and one matching room contract. Localize hotel and room names and descriptions in English and the destination language. Apply only supported meal plans. Reuse the hotel and room on subsequent nights and check occupancy for the actual party. |
| Airport pickup or another point-to-point transfer | Use a transfer master with the required vehicle capacity and a taxi rate (`transfer_type: "taxi"`) with actual `src_location_id` and `dest_location_id`. Put the pickup and drop-off in travel order, and check the return direction separately. |
| Car rental or a vehicle retained by the day | Use a daily/standard rate (`transfer_type: "standard"`) on the appropriate transfer master. Reuse the same vehicle when the source specifies the same service. Cover every applicable day. |
| A flight with unknown schedule or fare | Keep the flight in the itinerary as a labeled zero-cost illustrative add-on on the travel day. A real flight item needs a known airline, route, times and fare. |
| Whole-trip insurance or another inclusion | Use an add-on with `addon_type: "global"` and the applicable per-person or group basis. Include it once in the proposal's global items. Use day placement for an inclusion tied to a specific date. |

## Choose placeholder terms that will calculate

- Use an explicit `cost: 0` on a demo rate for a zero-price trip. Use a nominal amount only for a requested illustrative price, label the item or rate accordingly, and record its unit and currency. Preserve zero as a numeric value. A hotel contract's unavailable meal supplement is `null`; a free supplement is `0`.
- Base the effective dates on the actual demo departure through the last service date. For reusable examples, use a rolling two-year window covering the trip. For broadly applicable illustrative activities or add-ons, age and party bands can be 0–99 where accepted and appropriate. Apply the vehicle's real capacity and the double room's one-to-two occupant band to their respective rates. Verify the lead's full party can be allocated.
- Reopen the applicable rate rows and use **Simulate** where available for the trip's date, party and meal plan. Before calling the proposal free, verify its saved customer total in the quote currency, including margins, taxes and all global items. Treat an allocation error or a date with no matching contract as unfinished work.
