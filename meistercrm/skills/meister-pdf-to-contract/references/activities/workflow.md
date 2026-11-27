# Activity contract rules

Load this for activity PDF, spreadsheet, email, or table conversions. Apply [shared schema validation](../general/schema-and-validation.md) and [source extraction](../general/source-etl.md), then the activity-specific rules here.

## Shape and identity

One row is one activity price rule for a location, product, eligible age band, pax band, and date interval. The [header-only activity template](../../assets/templates/activity.csv) records the inspected format. The activity template has 17 columns, including `tax`. Check older 16-column exports for the missing field. Use the selected current template, never a remembered header. Compare the exported header, including `activity_duration_min`, `group_flg`, and `max_cap`, against the selected template.

Check overlap and currency within resolved location + activity name. Keep stable names and master fields. Distinguish genuinely different capacity, inclusions or charging models.

Master fields describe the product: location, name, description, duration, margin/tax settings, group flag, and capacity. Contract fields carry ages, pax, cost, currency, and validity. The importer does not infer an age rule from a description: translate restrictions into the numeric fields too.

## Choose the charging model before expanding rows

| Supplier meaning | group_flg | Pax band | Meaning of cost |
| --- | --- | --- | --- |
| Same price per participant | FALSE | Permitted range | One participant's supplier cost |
| Per-participant price changes with group size | FALSE | Each published size or tier | One participant's cost at that group size |
| Flat private price for up to N guests | TRUE | Permitted range up to N | Total cost for the group |
| Total private price changes with group size | TRUE | Each published size or tier | Total cost for that group size |

A multi-column table headed "2 pax / 4 pax / 6 pax" does not by itself prove group pricing. Read whether the cells mean per person or total. A child discount and a group-size discount are separate dimensions; cross the applicable age bands with the published pax bands and seasons. Do not cross impossible combinations or invent unpublished intermediate tiers.

Synthetic example: an adult per-person rate of 120 at two guests and 100 at four guests, with an eligible child at 50%, produces four rows: adult/two=120, child/two=60, adult/four=100, child/four=50; all have `group_flg=FALSE`. A flat private activity priced at 300 for one to six guests is one `TRUE` row with `min_pax=1,max_pax=6,cost=300`, assuming one common eligible age interval.

## Age eligibility precedes fare policy

1. Extract activity-specific minimum/maximum age from headings, descriptions, footnotes, and terms, including forms such as `8yrs+`.
2. Extract the applicable supplier child policy and exceptions. A general supplier policy may be overridden for one activity.
3. Intersect fare bands with the eligible interval. **Ineligible is not free.** Do not add zero-cost rows below a safety minimum to make coverage start at zero.
4. Convert percentage charges to absolute numeric costs. Read whether the source says "50% of adult price" or "50% discount"; other percentages differ between these phrases.
5. Preserve explicit child and teen bands even when two adjacent bands share a price if the source/business policy needs the distinction. Do not force multiple bands onto a genuinely flat all-age rate.

Synthetic boundary example: eligible age 8+, child through 15, adult from 16 means only `8–15` and `16–99`. A generic infant-free policy does not create `0–4` here. Interpret ambiguous boundaries such as "5–12, 12–16, 16+" before writing inclusive integer ranges; do not silently assign age 12 twice.

Where the customer uses the family activity fallback, the bands are 0–4 free, 5–15 child, 16+ adult, with adult cost when a permitted child has no separate rate. Apply it only when that fallback is appropriate to the family and the source does not contradict it; identify its use in the review notes. It is not a universal supplier policy. Explicit single-age or height/guardian restrictions always win. For example, one service can charge full price from age five while another offers a child discount and requires an accompanying adult and a minimum height. Height and accompaniment conditions have no dedicated activity columns: retain them accurately in the description while applying any age minimum numerically.

## Product location, capacity, duration, and copy

- Map the **place where the activity happens**, not its gateway city. A national-park activity belongs to that park's exact reference label. Distinguish a lake, park, village, town, and airstrip even when their names resemble each other.
- Expand a source covering multiple locations only when those are real separate offerings. Never write a combined made-up reference value.
- `max_cap >= max_pax`; represent minimum participants explicitly. Do not equate a minimum booking count with maximum operational capacity.
- Convert duration units to minutes, including decimal commas: `1,5 hours` becomes `90`. Verify validity separately. A label such as “half day” does not establish an exact duration or a calendar-year selling period. Source duration wins. When the duration is missing and an estimate is used, label it as an estimate in the review notes.
- Keep `activity_desc` at most 380 characters. Describe what guests do and relevant inclusions or restrictions, without prices or unsupported promises. Count the finished text; do not truncate it mid-sentence to satisfy the limit.
- Do not silently remove included transport/meals from a bundled supplier cost. Determine whether they are included, optional, or separately priced before splitting product types. Park entry fees separately published alongside an activity are not automatically part of its cost or automatically add-ons; use the correct location/add-on model from the source and task.

## Final activity checks

Reconcile the extracted activity list with the exported products, verify every eligibility boundary, and spot-check each percentage-derived amount. Check each price model's age × pax × season expansion, consistent metadata, exact locations, and operational capacity. Apply all shared CSV checks and report unmodeled restrictions outside the CSV.

Use [checking gates](../general/checking-gates.md) to assess coverage separately for each pax band and actual eligible age range. Age coverage in one pax tier can hide missing children in another; a passing result does not require or justify adding prohibited infant rows. Check that duration is a genuine nonnegative integer and weekdays and operating periods come from supplier evidence or an explicitly scoped instruction.
