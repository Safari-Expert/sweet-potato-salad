# Transfer contracts

For location fields, follow the shared [live location-reference category](../location-reference/live-reference.md) on every run; use the intended customer's filtered reference when validating that customer's availability.

Use for vehicle hire, airport transfers, and route price sheets. Load [shared schema and validation](../general/schema-and-validation.md) and [source ETL](../general/source-etl.md).

## Row model and master identity

A row is one vehicle/service master, transfer type, route (blank for daily hire), passenger band, age band, and validity band. Determine whether a source price is per vehicle, per day, per route, or per seat before expanding rows. Do not divide a whole-vehicle price by passenger count.

Names are functional identity. Keep distinct service levels and contract families separate when they represent different products. Label daily hire with the applicable channel and family where needed. Use Regular and VIP variants only where supported.

Pax tiers of the same service can remain rows under one master. Do not create separate vehicle names merely because the price changes from 1–3 to 4–6 passengers. Conversely, do not merge Regular and VIP or materially different capacity classes into one master just because the vehicle model text matches.

Keep master fields consistent per `vehicle_name`: capacity, currency, margin, tax, and proposal-margin behavior. Use the 16-column transfer template, including `tax`. A later row under the same vehicle name must agree with that vehicle’s master fields.

## Transfer types and routes

| Product | CSV representation | Required checks |
| --- | --- | --- |
| Point-to-point transfer | `transfer_type=taxi`; exact source and destination reference names | Both endpoints are established by the source/current user; route direction and price are correct |
| Daily vehicle hire without a route | `transfer_type=daily`; both endpoints empty | No filler text, no copied airport fallback, correct daily unit and seasons |
| Airport meet-and-assist when modeled as a transfer | `taxi`; same official airport in both endpoints | Confirm the source charge belongs to this product; do not create a duplicate reverse row for A-to-A |
| Shared per-seat transport | Establish price basis first; historical notes suggest `bus` | Current inspected validator accepts only `daily` or `taxi`; do not emit `bus` or silently relabel it without a supported model decision |

Use `daily` for daily hire and leave both route cells empty.

## Direction and product coverage

The established transfer business convention is to include A-to-B and B-to-A for each relevant vehicle/service level, unless the source/current business instruction establishes one-way service. That convention authorizes mirroring the known route rule; a price sheet saying “and vice versa” confirms it. Preserve different published directional prices rather than copying one over the other. If source restrictions contradict the required reverse coverage, record that conflict before calling the dataset complete.

Build a coverage matrix of expected service variants × directed routes × pax bands × seasons. A dataset with Regular and VIP but only the Regular reverse route is incomplete. Match each endpoint to the exact catalog location or a confirmed equivalent. Geographic proximity alone does not establish a match. Do not expand an unspecified endpoint into a guessed base town just to make the matrix rectangular. An airport-to-itself rule needs one row per pricing band, not two identical directions.

Vehicle mirroring for a particular destination or contract family is conditional. An example duplicated one vehicle into another with identical routes, bands, and prices. Only perform that expansion when the current source/user requires both vehicle masters; it is not a universal regional rule.

## Pricing bands

- The established transfer convention uses `min_age=0`, `max_age=99`, without age-specific discounts. A supplier document that truly contradicts this convention needs an explicit supported modeling decision.
- For a whole-vehicle rate, normally use `min_pax=1` and the applicable tier/capacity as `max_pax`. `cost` is the entire vehicle/tier price. A valid explicit zero minimum can be preserved; the supplied sample contains both `0` and `1`, so do not reject all zero minima.
- For capacity tiers, split the stated passenger ranges into disjoint rows while keeping the same vehicle capacity. Synthetic example: a six-seat service with distinct 1–3 and 4–6 rates has two bands and `max_cap=6` throughout.
- The historical per-seat convention uses `min_pax=max_pax=1` and per-person `cost`, while `max_cap` remains vehicle capacity. Its transfer-type support must be resolved as above; a historical `bus` example is not import approval.
- Require `max_cap >= max_pax`, and one consistent capacity under the same vehicle name. Do not infer capacity from a model name alone.
- Split true seasonal changes and keep source validity. Preserve currency from the supplier; do not set USD just because older examples used it. Shared guidance owns currency conversions, margins, and taxes.

## Validation gaps and final review

Compare routed transfers by vehicle, source, destination, type and age/pax/date dimensions. Different non-overlapping pax tiers may share dates.

Check daily-hire overlap and continuity by vehicle, daily type and age/pax bands. Keep the route cells empty.

Reconcile every source row to output and verify the coverage matrix, exact location mappings, capacity consistency, charge unit, and no duplicate same-airport row. Put unresolved endpoints or unsupported types in a separate review report rather than an apparently import-ready CSV.

Apply [checking gates](../general/checking-gates.md): identical pax bands with intersecting dates/ages conflict on import; unequal intersecting pax bands need source/model review even if validation accepts them. Check capacity and master spelling across every route for one vehicle. Missing reverse coverage is a review item, not permission to invent a reverse service; confirm source availability and the requested task scope. Keep actual seasonal non-operation gaps for both taxi and daily services, using the shared accepted-exception record.
