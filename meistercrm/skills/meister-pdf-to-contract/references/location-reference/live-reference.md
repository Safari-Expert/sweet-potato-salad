# Location reference

Use canonical places available to the customer through the connected MeisterCRM tools. When working offline, record unverified matches for later checking.

Commercial fares continue to come from the authorized supplier evidence and its applicable validity periods.

## Identity and allowed location types

Match the source's intended place using the designated reference's `location_id`, canonical `location_name`, country and relevant site context. Preserve canonical spelling in name fields and record the chosen ID in private preparation evidence. Treat IDs as identifiers.

A valid destination, town, park, reserve or other existing location can be used when it represents the intended endpoint or the user explicitly approves that modelling choice. Do not require an Airport/Airstrip type merely because the item is a flight. Keep its actual type and source label; do not create a new airport or label an existing destination missing solely because its type is broader. Apply the existing [hotel destination conventions](../hotels/workflow.md#safari-destinations-when-an-exact-location-is-unavailable) where relevant.

A grouped supplier label needs either supported individual members or an explicit approved mapping to one existing destination. A park-level mapping does not authorize inventing member routes, airstrips or every pair of endpoints. Preserve the supplier group wording and the approved scope in the preparation evidence.

When the source place is truly absent, record the missing identity as a blocker. Location-reference lookup is read-only and does not itself authorize creation or editing of global locations.

## Duplicate names and transport

Do not choose the first matching name. Use country/site evidence and an explicit user-selected ID where available, then verify that ID and its current name against the connected catalog reference. Identically named records may be different countries or duplicates; matching names alone do not establish the same place.

Keep three results separate:

1. The intended location identity has been resolved.
2. The selected workbook or connected import operation can express that exact ID.
3. The actual target accepted and persisted that ID.

An explicit ID choice resolves the business identity. A legacy name-only CSV can still have a transport limitation. Inspect the connected tool’s schema before claiming the choice is encoded; use documented ID fields when supported. Do not invent extra import columns, rename canonical locations, silently remove competing reference records, or suppress an ambiguity failure to produce a passing report. Preserve the connected reference identity and lookup date and the ID decision; record a scoped validation exception or remaining transport dependency accurately. File preparation is distinct from live import.

## Applying a customer’s flight mapping

An operator can explicitly select a named destination for a grouped “all airstrips” fare or choose one official airstrip for a general park label. Keep the supplier’s literal label, resolved place, direction, edition and approval together. If duplicate names resolve to different IDs, verify the saved endpoints after import. Where one user once selected a broad destination or a specific duplicate, obtain the current customer’s mapping before reusing the choice.
