# Hotel rate-year availability

Use this policy when assessing source Rate Years, preparing catalog year tags or checking missing-year coverage. Decide from the property's actual priced periods, operating season and supplier edition together. **There is no minimum number of months or days.** The former six-month/183-day rule is superseded.

## Separate coverage from edition and completeness

- **Supplier edition** identifies the agreement or tariff cycle. A contract released as the 2026 edition can legitimately price stays into May 2027; those dates do not turn it into a new 2027 edition. Prefer explicit agreement context over a filename or release date alone.
- **Source Rate Years** in the catalog review identify calendar years with genuine, usable priced periods in the available source evidence. A PDF's existence or nominal filename is insufficient; use this property's applicable pages. A separate PDF named for every year is unnecessary when one contract genuinely spans those years.
- **Prepared/catalog coverage** follows supported, validated output dates. Before a new upload, prepare tags from the intended dataset. For an existing hotel, reconcile its old-plus-new contracts; verify persistence before claiming the tags describe imported availability. A source year without corresponding imported rates is not an imported catalog year.
- **Completeness and renewal** remain separate checks. A year tag means supported rates exist for a genuine period and at least one product in that year. It does not promise all dates, all rooms, or that the year's successor edition has arrived. Keep missing requested periods and room questions visible in the catalog review/review.

Source availability, generated CSV coverage and imported coverage are different facts. An October–December-only conversion does not shrink the PDF's Rate Years. Conversely, an older file's year tag does not prove missing current rates are generated or imported. Past-year-only sources follow stale source coverage (see **Meister PDF to Contract**, Hotel dates, seasons and operating scope): retain the source/year evidence without generating rates, unless historical conversion was explicitly requested.

## Qualify each candidate year using context

1. Identify the property, applicable buying agreement, supplier edition, actual tariff dates and stated operating periods. Inspect the source content, including contract validity and season tables; document dates, terms-only mentions, a neighbouring hotel or a generated workbook do not establish a source-priced year. Approved alternative source evidence follows the existing source rules; never invent a missing PDF or its year.
2. Associate each priced interval with the supported rows being prepared or verified in the system. Excluded, unresolved, unquoted and unimported dates cannot prove imported coverage. Retain literal inclusive dates and room/product scope.
3. Count a year when that evidence establishes a genuine bookable tariff period in it. This includes remaining-year October–December rates, a camp's two- or three-month operating season, a real short event product, and a contract that genuinely operates across calendar years. Do not substitute another duration cutoff for the old rule.
4. Distinguish an incidental holiday tail from a separate year's tariff. A few December dates attached to the opening of a 2027 annual agreement usually do not establish substantive 2026 availability. An explicitly offered 2026 holiday season or standalone event can qualify even if short. Judge the agreement's purpose and priced scope, not the date count alone. Preserve those literal prices even when they do not warrant an additional year tag. If this distinction cannot be supported, record the uncertainty rather than silently claiming the year.
5. Record each inclusion/exclusion reason and the exact covered intervals privately. Merge duplicate dates across rooms/ages/boards for audit counts, but use those counts only as diagnostics. Keep genuine seasonal closure separate from missing prices, and do not bridge gaps merely because a year qualifies. Apply the existing stale-source policy separately.

## Contracts spanning two years

A May 2026–May 2027 agreement with meaningful operating tariffs in both years qualifies for **2026 and 2027 coverage**, while retaining **2026 supplier edition**. Record its actual last quoted date and the required successor/changeover around May 2027. The next supplier edition need not start on 1 January; use its stated dates. Do not shift endpoints or fabricate an overlap or extension from the phrase “2027 rates.”

If coverage after the old agreement's expiry is requested but no successor is supplied, preserve the valid `27` tag for the supported imported portion. Ask in `ai_source.ai_comment`, “Can you provide the renewal covering stays after [last quoted date]?” Adding a new edition still follows scoped union validation and conflict handling; year classification does not authorize overwriting existing contracts.

## Decision examples

| Evidence | Source years | Catalog tags after verified import | Scope to retain |
| --- | --- | --- | --- |
| Genuine October–December 2026 tariff | `2026` | `"26"` | Remaining-year coverage qualifies. |
| Camp operates only July–September 2027 | `2027` | `"27"` | Stated closure elsewhere is expected. |
| May 2026–May 2027 agreement, both periods genuinely priced | `2026, 2027` | `"26", "27"` | 2026 edition; successor required at actual May 2027 expiry/changeover. |
| Annual 2027 agreement starts with incidental December 2026 festive dates | `2027` | `"27"` | Retain December prices; the spillover alone does not establish a separate 2026 tariff year. |
| Annual 2027 tariff, 25 December 2026–25 December 2027; the 2026 days are its opening festive spillover | `2027` | `"27"` | Preserve literal dates; the opening 2026 tail does not qualify by itself. |
| 2026 edition also quotes the preceding December 2025 holiday period | `2026` | `"26"` when supported in-scope rows are imported | The holiday alone does not establish a 2025 rate year. |
| Migration camp explicitly operates July–October 2027 | `2027` | `"27"` | For its stated operating season. |
| Explicit two-day 2026 event tariff, not an incidental tail | `2026` | `"26"` | Record its limited event dates. |
| Whole-year source exists, only its Q4 rows are imported | That source's genuine years | The imported Q4 year qualifies | Do not claim the unimported seasons are in the system. |
| Usable 2027 PDF exists, but no 2027 rates are imported | `2027` | No `"27"` yet | Source availability and import state differ. |
| Filename says 2027, applicable table prices only 2026 | `2026` | `"26"` if imported | Flag misleading filename; do not invent 2027 coverage. |
| One supported room covers 2027; other rooms are unresolved | `2027` for the supported scope | `"27"` | Retain room blockers and actual completeness status. |
| Only a 2025 PDF exists during an ordinary current-rate review in 2026 | `2025` | No new import or tag change from that stale source | Blocker `SOURCE`. Ask “Can you provide the 2026 rate sheet for this lodge?” Existing catalog presence remains independent. |

Use individual two-digit calendar-year tags in ascending order, such as `["26", "27"]`. Preserve the customer’s existing non-year tags.
