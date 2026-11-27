# Hotel dates, seasons and operating scope

## Valid single-day seasons

Hotel validity dates are inclusive: `start_date <= end_date`. Equality is a valid one-day season, not invalid data. For an extra charge on one day within a longer season, split before that day, the day itself, and after it. Reject reversed dates and real overlaps, not equality.

Do not omit, widen or merge away the event to satisfy a checker that requires strict inequality. Keep the valid one-day rate in the workbook and record a rejected import on the owner master.

The user's workflow selects rates by check-in date. Preserve the requested event dates without claiming that season splitting implements night-by-night selection or arbitrary once-per-stay charges.

## Start at the current calendar month

For ordinary hotel-rate preparation, start at the **first day of the current month**, using the user's current local date. This applies in every calendar year; do not hard-code October or 2026. For example, work performed on 15 October starts on 1 October, rather than the 15th or 1 January.

Set `cutoff = first_day_of_current_month`. Omit a source interval when `end_date < cutoff`; otherwise emit `start_date = max(source_start_date, cutoff)` and retain its supported `end_date`. Apply the cutoff to all room, age, meal and holiday intervals in the payable rows of the maintained workbook. Preserve the supplier’s original validity and TDL basis on `Original`. Future-year contracts retain their actual starts; the current month number does not truncate the same months in future years. Never extend supplier validity or bridge closures to reach the cutoff.

Preserve the complete original source and its genuine **source Rate Years** in the catalog review; clipping generated rates does not erase a source year or prove imported availability. An entirely expired current-year contract produces no new rate file and needs a current source; past-calendar-year-only sources retain `YEAR OUT OF SCOPE` under [stale source coverage](#stale-source-coverage). An explicit historical-conversion request can override this default. This rule controls newly prepared files, not deletion of existing imported contracts.

## Editions and seasonal boundaries

Bind the room inventory and tariff to each edition independently. A room introduced in a later contract must not be backfilled into the earlier year. Use the quoted stay dates at year boundaries. Preserve an explicit user-authorized extension only for its stated edition, dates and components. The general conversion sequence remains in [hotel workflow](workflow.md); use the rules here to determine dates and coverage from the source.

### Stay dates and document dates

Read what each date governs. The property’s tariff table supplies the priced stay intervals within the agreement’s explicit validity. Record dates labeled as issue or contract dates separately on `Original` when they could cause confusion. An administrative date can fall after the first stay date or after the day you review the source. Apply any explicit effective or expiry date stated for the tariff to the affected stay intervals.

For example, an annual NET agreement has a contract date of 18 August 2032 and lists Low from 5 January through 31 July and High from 1 through 31 August. Prepare both full intervals and the remaining quoted seasons, even if you review the agreement before 18 August. Record the printed contract date with the tariff evidence. If the agreement instead explicitly says the rates take effect on 18 August, apply that boundary to the affected rows and use any independently supported earlier coverage.

Before raising a date blocker, identify the exact stay or booking dates affected and the applicable wording that leaves their price or eligibility unresolved. If two applicable validity clauses still disagree after precedence rules, ask one question about the affected dates and continue with independently supported rows.

For overlapping dates in successive contracts for the **same applicable property, product and buying agreement**, the user's later 8 October rule selects the newer contract and treats the older overlapping tariff as stale. Verify which edition supersedes the other and keep separate rate schedules distinct. Stop at the supplied validity end, even mid-year, without treating a missing calendar-year remainder as a blocker. Annual price validity alone does not establish where a mobile camp operates throughout that year.

When two seasons in the **same controlling tariff** include the same boundary date, the 10 October preparation default assigns that date to the higher applicable buying-rate tier to avoid underquoting. Compare the actual room tariff, retaining that season's coherent board and age rules; do not combine unrelated columns or choose RACK. This resolves a season overlap, not a missing price, conflicting agreement or invalid calendar date. Record the chosen date and the competing tariffs privately.

A month-only opening or ending statement uses the [approved month-boundary default](#automatic-calendar-normalization-21-october-2026). Repeated month columns or coloured blocks that leave competing seasons within the same month unresolved still need review. A historical output's dates cannot supply those missing split days. Preserve a genuinely explicit first-of-month endpoint; the month-only default does not widen it.

If a supplier explicitly carries forward the same rates, seasons or offers until a replacement contract is issued, preserve that condition and its market scope. Check for the replacement before relying on the extension; absence from one reserved package is not proof that no replacement exists. A same-rate extension does not authorize an annual percentage uplift. Normalize only the calendar cases approved below; a corrected-looking historical calendar does not resolve other malformed dates.

## Automatic calendar normalization, 21 October 2026

Apply these user-approved preparation defaults before expanding seasons, clipping to the current month or running interval validation. They resolve the listed source defects without another human question. Retain the printed wording, PDF/page, normalized dates and applied rule in private review evidence; report the assumption concisely in the assessment instead of leaving a resolved `DATES` blocker.

- **Impossible season-end day:** clamp the printed end day to the actual last day of its stated month and year. Thus 29 February 2027 becomes 28 February 2027, and 31 September 2027 becomes 30 September 2027. Keep 29 February in a leap year. Do not roll overflow days into the next month or change a stated year to repair a different conflict.
- **Omitted month-end day:** when adjacent seasons omit only the final day of a month, include it in that month's season. For example, a season ending 30 March followed by one starting 1 April ends on 31 March. This fills an apparent calendar omission, not an explicit closure or a missing renewal after the contract ends.
- **Festive boundary omission:** if a missing boundary date touches a festive/peak period, include it in the higher applicable buying-rate season to avoid underquoting. For example, ordinary season through 21 December and peak season from 23 December means peak starts on 22 December. Use that selected season's coherent room, age and board tariffs; do not invent an uplift or move separately dated gala meals onto the added day. Apply this festive-price check before the ordinary month-end default when both could apply.
- **Month-only opening/end:** where the month and applicable year are established but no day is specified, use the first day for opening/start and the real last day for ending/closure boundary. “Opens in November” starts 1 November; “ends in December” ends 31 December. Use the applicable leap-year calendar for February. This normalizes the operating/validity boundary; it does not supply missing prices or an unresolved year.

Explicit closed dates, exact operating restrictions and scoped human answers take precedence over these typo/default interpretations. Do not fill arbitrary interior holes, long seasonal closures or competing within-month calendars. Remaining year, scope or tariff conflicts still need review. The stricter earlier instruction to block every impossible endpoint or unexplained single-day hole is superseded **only for the cases above**. Local validators still reject invalid saved dates and actual overlapping output; normalize the reviewed source first, then validate the emitted intervals.

## Scoped source-year corrections

When festive meal years conflict with an otherwise valid contract edition: Preserve the printed wording; obtain the intended event year. An approved template-year correction applies only to that document and event scope. It does not extend room validity, import another edition's prices or create unquoted events.

An approved source-year correction remains document-specific. Record the document edition, dates, affected components and limits separately from supplier facts; do not ask the same settled question again. The general calendar-day defaults above do not authorize changing a conflicting festive year.

## Undated Easter supplements

The answered 8 October reviews establish a general preparation default: where a supplier quotes an Easter charge but omits its dates, apply it on **Good Friday, Easter Sunday and Easter Monday**. Verify those dates online for each contract year and retain the calendar source privately. Keep Saturday ordinary unless the supplier explicitly includes it. Explicit supplier dates take precedence. This resolves the event calendar only; it does not invent a charge, decide compulsory status, repair a contradictory printed year, or extend contract validity.

## Seasonal operating calendars

For a mobile camp with a confirmed seasonal location calendar, use distinct property entries for its seasonal sites and bind each tariff to the stated operating dates. The 10 October answered mobile-camp review accepts omitted relocation/low-season periods outside that calendar as excluded operating scope; do not fill them or backfill a preceding season without its contract. This is not evidence that every unquoted hotel period is a closure or that a calendar can be inferred from annual prices alone.

Migration and temporary tented camps may legitimately operate for only part of the year. Large, source-supported operating gaps alone do not make their tariffs incomplete. Process the stated periods as-is, keeping literal dates and site scope; a tented name is a clue to inspect operating terms, not permission to infer closure or repair conflicting years.

Expand each genuine room/age rule across the source's season intervals, including periods spanning year end. Preserve closures instead of filling them with fabricated rates. Do not infer next-year validity from a sample. Check completeness per room family and investigate an unexpectedly short room family or spelling variant; do not force identical row counts when the source has legitimate differences.

Compare price seasons independently from minimum-stay, deposit, cancellation and offer-blackout calendars. A night charged at the high-season price can still require festive minimum nights and a non-refundable festive deposit. Split each applicable policy at its own boundaries; a correct price-date sweep does not verify booking eligibility. For a promotion spanning seasons and room categories, preserve each stated bonus-night priority. If the season and category priorities select different nights and their precedence is unquoted, keep the competing allocations unresolved rather than choosing the cheapest night.

Use document validity and property identity over directory labels; a folder named for another year or country is not authority to change the source. Distinguish a missing output rule from an actual gap or contradiction in the supplier document itself. Apply [automatic calendar normalization](#automatic-calendar-normalization-21-october-2026) and the [overlapping-age policy](child-policy.md#unresolved-overlapping-age-endpoints) before retaining a blocker. Holes and contradictions outside those defaults remain unresolved, not inferred closures. A later-year curated output without a matching renewal is source-unverified, not by itself proof that its historical preparer made a mistake.

## Stale source coverage

An edition whose rates fall entirely in past calendar years is **YEAR OUT OF SCOPE**. Preserve that assessment on `Original`. If the missing current edition blocks the requested work, ask for it in `ai_source.ai_comment`, for example “Can you provide the 2026 rate sheet for this lodge?” Generate historical rates only when explicitly requested. Verified catalog presence is independent of coverage.

Review newer supplied editions before assigning the lodge-level status: an obsolete older edition does not invalidate independently supported current/future coverage. In a mixed-year source, omit past-year rows from the current deliverable and retain the supported in-scope periods; never roll dates forward or fabricate missing seasons. Use the supplied tariff's validity when the filename and the rate dates differ. Flag an expired current-year edition or one with only a short current-year remainder and no renewal separately as stale; legitimate seasonal gaps are not a reason to classify supported current/future periods as past-year rates. Distinguish renewal needs from unresolved tariff interpretation and keep current-upload readiness explicit.

## Calendar validation

Check explicit date boundaries independently of a printed duration or season-day count. When they disagree, retain both and flag the conflict unless an approved calendar normalization resolves it; do not build the calendar from the count. Invalid dates outside the normalization rules and conflicting end years remain unresolved, even when the filename suggests an obvious repair. Validate the normalized dates against the real calendar and check adjacency, closure preservation and non-overlap. Scope promotions to the exact nights they cover: a second-night-only discount does not discount the first night or repeat automatically on every second night. Synthetic example: a 300 room with 30% off only the second night totals 300 + 210 = 510 for two nights.
