# Hotel profile upload

Read [completion gates](completion-gates.md) at intake and retain evidence for each selected hotel and room.

## 1. Find property data and pictures

Use media the customer has permission to reproduce. Keep the image’s source and usage basis with the private working evidence. The ability to view a photo does not establish publication rights.

- Start with the exact property's Booking.com listing; verify its location and room identities. Supplier PDFs and confirmed amendments remain authoritative for contractual prices, occupancy and inclusions. Website content supports descriptions and photo identity, not replacement retail tariffs.
- Prioritize speed: when Booking is blocked or the needed image is not readily available, move promptly to the official property site, supplier fact sheet or already available verified assets. Do not keep searching for an ideal image after an adequate truthful fallback is available. Ordinary access failures are not authorization to bypass access controls.
- Search once per property and physical room family. Download and inspect each distinct selected image once; retain its source URL, room association, local hash and intended order. Reuse appropriate family photos for Single/Double/Extra Bed pricing variants, without treating a variant name as proof of a different physical room.
- Aim for 2–3 hotel photos and 2–3 photos per room product when available. Prefer a visible double bed for a Double and two separate beds for a Twin. Match the room family before optimizing bed layout. If an exact bedding shot is unavailable, use the best relevant verified room/interior/view image; record it as a fallback and do not imply an unverified bed setup. The user's fallback instruction already authorizes this choice. A property-only image must not be presented as proof of a particular room interior.
- **First photo is the cover.** For rooms, put an attractive bed/room interior, ideally with a view, first. Put bathrooms and detail shots later. For the hotel, put an overall property/exterior or broad setting image first; restaurant and reception/check-in images are useful secondary pictures when readily available. If the preferred cover is unavailable, select the best available truthful alternative promptly and record the fallback.
Keep source images and provenance in the customer’s private working area. Attach eligible images to the catalog without adding extra deliverables to the lodge folder.
- If the user authorizes importing a named property or room without photos, record the exact subjects and instruction in private evidence and continue its other profile steps. Keep its photo list empty rather than inventing an image. Apply the [authorized media-exception gate](completion-gates.md#authorized-scope-exceptions); do not carry that permission to other properties or clients, and do not put a missing-photo notice in hotel notes.

## 2. Refine text in every requested language

Prepare the content and ordered photo packet before writes. Use original, source-supported prose. Preserve meaning, amenities and occupancy distinctions across languages; do not claim an ensuite bathroom, bed arrangement or view merely because a similarly named room has one.

| Field | Required language behavior |
| --- | --- |
| Hotel name | Use the resolved PDF/Booking property name in readable Title Case with spaces (the user's "camel case"), preserving established brand spellings and acronyms. Use that same untranslated name in every language view. |
| Hotel description | Translate into every requested language. Current target: approximately 350 characters including spaces per language. |
| Room name | Translate into every requested language, preserving proper names and the room/occupancy distinction. Apply the consistent extra-place suffixes in room naming rules (see **Meister PDF to Contract**, Hotel occupancy, ages and missing places). |
| Room description | Translate into every requested language. Current target: approximately 250 characters including spaces per language. |

The character counts are the user's content targets, not field limits. Validate them deterministically against the actual current schema. Preserve existing additional language values when merging updates. Bind each translated display name to the same captured room ID and canonical source identity; translation must not create another room or move its contracts.

For a new master, normalize inconsistent capitalization before import. For example, `example river lodge` becomes `Example River Lodge`. Retain the source spelling as a private alias.

Before saving, review each room name against the source room family and occupancy variant: correct spelling, nonblank names, no accidental duplicate/copy, and no lost distinction between Twin, Double, Single, Triple, Family, Suite, Extra Bed or Extra Guest. Translate meaning into natural French/German, retaining proper names and source-supported amenities; literal word substitution and English fallback are insufficient. After saving, compare the explicit locale fields for every captured room ID and capacity. Correct a display-name typo on its existing room ID through the supported room update; reconcile workbook/import aliases and evidence without creating a second room or moving contracts. Record a per-language semantic review of hotel/room descriptions and room names. Automated nonblank checks support that human-quality review but cannot prove translation meaning.

Use the connected catalog schema for localized hotel/room names and descriptions. Read back each requested language.

## 3. Create a hotel or add rates to an existing hotel

Prepare the hotel’s [coverage tags](#rate-year-tags) and [supplier PDF](#source-pdf-attachments).

### Resolve hotel ownership before choosing create or update

Fetch the current hotel list on the authenticated client/environment and match the actual property, including location and source identity. Names alone are insufficient. Apply these import rules:

| Matching catalog record | Import action |
| --- | --- |
| Shared hotel | Resolve an owned master before edits. Preserve the shared record. |
| Matching customer-owned hotel | Preserve its ID and existing contracts. |
| No matching record | Create a new client-owned hotel within the authorized import scope. |

Use the [connected workbook import](../catalog-workflow.md#import-and-attachment) for reviewed new rows. Inspect held rows and read back every saved ID.

### Existing hotel: add new rates with id

**Preserve the existing hotel ID.** Customer templates can already reference it. Amend a positively identified contract by its existing ID. Import independently supported missing contracts. Preserve existing history and hold ambiguous or superseded records for review.

Create missing rooms when authorized and positively identified. Amend the existing identified contract for a correction.

Traverse hotel → rooms → room contracts through the connected catalog, keeping the parent association and all pages of results. For an existing hotel, bind the stored hotel, location, currency and room IDs and use their actual spellings in the import. A Title Case display cleanup is a separate change on the same ID. An incomplete or failed room-contract lookup leaves coverage unknown. Reconcile that room before importing or retrying its rows.

Classify every reported finding. Retain genuine one-day events and source-confirmed closures. Leave blocked rows pending through MCP.

Record accepted modeling decisions and the scope of any held rows on `Original`. Use [catalog review](catalog-review.md) for a question that blocks the held rows and [hotel notes](#short-booking-exception-notes) for known pricing exceptions a consultant must handle.
Read back all affected rooms and contracts through MCP. Reconcile incoming rows, saved IDs, existing coverage and duplicates. After a timeout or partial outcome, reconcile before retrying. Validate again if the file or rates changed. Serialize imports into the same hotel.
Refresh attachments and availability tags using the resulting old-plus-new coverage. Check buying prices for new rates and affected boundaries. Record workbook readiness, catalog presence and pending scope independently.

Whitespace and spelling differences can hide duplicate room aliases. Bind each rate to the intended existing room ID. Hold ambiguous additions. If readback reveals a misrouted contract, identify its ID and affected room before seeking a scoped correction. Preserve unrelated contracts and every existing room and hotel ID.

## 4. Update pictures, text, rate-year tags and source PDFs

- Read the current hotel and room masters through MCP. Merge the intended locale maps and photos using the connected tool’s schema. Preserve unrelated fields and attachments.
- Send names/descriptions and photos together where supported. Upload each distinct new image once; reuse the returned tenant-owned file objects for appropriate variants. Preserve required file metadata and omit binary data when reusing a stored object. Do not substitute a bare URL for a structured file object when the connected catalog requires one.
- Check that each persisted photo list contains unique `file_id` values. Creating a room with photos and later merging fresh uploads with its stored references can repeat the same saved image. Reuse returned file objects; if readback shows duplicates, keep the first object and remove only repeated references, preserving all other room fields and contracts. A duplicate is not a second photo.
- Update rate-year tags on the hotel, preserving unrelated labels. Use the [connected attachment workflow](../catalog-workflow.md#import-and-attachment) for the lodge PDF. Preserve earlier attachments and check for an existing match before adding one.
- Prepare the cover-first order before uploading. Distinct master updates can run with bounded concurrency; do not race two writes to the same master. Tune concurrency from measured behavior rather than treating a previous run's setting as a service guarantee.
- Fetch fresh readbacks and compare every requested locale field, canonical hotel name, room identity, ordered image IDs and first image. Verify capacities, preserved flags, rate-year tags and source-document references too. Request success and an unordered photo/document count do not prove correct language coverage, cover order or attachment identity. If a layer reorders the images, use its supported ordering mechanism and verify again.
- Read back every requested language, photo order and cover. Inspect the returned image through a supported customer media operation when available. Record unavailable delivery checks as pending. Verify the saved source attachment by its filename and identity.

### Short booking-exception notes

Reserve the hotel's `notes` field for known price adjustments or pricing rules that the contract rows do not handle. State when the exception applies and what the consultant must charge or confirm, such as an excess Single-room charge or a child-sharing discount that requires manual adjustment. Use one to three short sentences or bullets and keep the quantities, ages, percentages or dates needed to quote correctly. If the saved rates handle the full rule, no note is needed.

Fit the current Notes control's length limit: its documented default was 200 characters on 18 October 2026. Shorten wording without losing a pricing condition; a longer value accepted by the connected catalog does not prove it fits the editor.

Do not add missing-picture notices, upload status, preparation tasks or internal follow-up messages to hotel notes. Keep media follow-up in the work records or latest review. An explicit instruction to import without pictures changes only that upload's media scope; it does not authorize inventing photos or adding a photo-status note.

Write for a travel consultant, not a developer. Do not mention catalog field names, allocation/schema mechanics, user preparation instructions, extraction history or validation details. Keep calculation proofs, source references and implementation explanations in the private audit. Remove repeated statements and combine duplicate quota or child-policy warnings; never truncate away a material limit just to shorten the note.

Review operational access conditions as well as rate restrictions. Put arrival/boat cutoffs, walking-only approaches, luggage arrangements and other descriptive information in the appropriate description or preparation evidence; use hotel notes only when the condition is a pricing exception. Retain an explicit private “reviewed; none applicable” result when no pricing exception applies.

Distinguish the hotel's offer from what the listed prices actually apply. If all eligible children use the accepted one-adult discount, stating both supplier discounts alone must not imply the system automatically applies the cheaper two-adult discount. Mention any manual adjustment simply, without explaining the engine. Synthetic wording:

> Single rate: first 2 rooms per booking; additional Singles use the Double rate.
> Children 5–12: listed prices use a 35% discount. The hotel's 50% discount with two adults requires manual adjustment.

Use only source-supported limits and discounts for the actual property; those example figures are not defaults. This wording rule does not change the accepted child-sharing price policy (see **Meister PDF to Contract**, Hotel child policy, ages and admission), Single tariffs or booking eligibility. Preserve unrelated existing notes when making an update, and verify the final saved text is concise, accurate and free of internal jargon.

### Rate-year tags

Apply [rate-year availability](rate-year-availability.md) to this property's actual validated and resulting old-plus-new imported coverage. Source editions, operating periods, genuine cross-year tariffs and incidental holiday tails determine which years qualify; there is no duration threshold. Remaining-year Q4 rates and short seasonal operations count. A May-to-May agreement can qualify for both calendar years while remaining the earlier supplier edition with a later renewal deadline.

Prepare individual two-digit year tags in ascending order, for example `26`, `27`. Preserve the customer’s other existing labels. Verify resulting rate periods and retain renewal questions. A year tag alone cannot establish full-year or all-room coverage.

### Source PDF attachments

Attach the lodge’s relevant original rate pages plus applicable shared terms. Preserve sources for every edition and amendment used. Stage the customer’s lodge PDF through the [connected attachment tool](../catalog-workflow.md#import-and-attachment).

Read back the retained PDF’s filename and identity on the owner master. Preserve existing documents on retries.

## 5. Validate buying prices

After a new import or pricing change, compare the saved room’s quoted buying price to an independent supplier calculation using a supported customer-facing pricing or quote operation. If unavailable, report live pricing unverified. Keep offline checks and import readback separate.

Independently reconstruct the whole-party buying total from supplier facts and applicable preparation conventions. Compare the source, saved rates and actual quote. Repeating per-person fractions can round differently on persistence.

Use the local rate comparator and price-check helpers (see **Meister PDF to Contract**, Hotel source and calendar tools) for normalized prepared-versus-persisted coverage, representative case selection and captured-response comparisons. Supply exact room bindings and source-reviewed expectations; the helpers neither call the service nor turn CSV-derived expectations into independent PDF evidence.

Use isolated room IDs for representative full and partial occupancy, singles/extra beds, relevant adult/child/infant boundaries, supported boards, season/holiday boundaries and an out-of-validity negative case. Include multi-night check-in-date behavior when the requested scope needs it. Inspect embedded errors even with HTTP 200. Through the connected quote tool, compare supplier costs separately from sell prices, currency conversion, margins and taxes, and reconcile totals to traveler/room entries.

Classify source transcription, approved representation choices, storage precision and runtime calculation differences separately. A calculation matching stored values is not proof that it matches the PDF. Repeating per-person fractions can become one-cent party differences when board or single-supplement columns round; preserve the evidence and report the discrepancy rather than rounding the expected source total to make the check pass. Keep unknown supplier rules unresolved.

During ordinary uploads, reuse valid source packets, downloaded assets and returned tenant-owned media references; invalidate affected work when sources, languages, room mappings or tenant change. Batch independent work and combine updates to the same record without racing writers. When timing or model comparisons are requested, use the [end-to-end timing procedure](upload-timing.md); experiments are not a prerequisite for client onboarding.

Retain source locators, coverage, attachment identities, room bindings, languages reviewed and unresolved scope.

## Attachment size and quality

If the lodge PDF exceeds the connected tool’s limit, retain the original unchanged and prepare a private derivative when compression is authorized. Include all applicable rate pages, shared terms and amendments for that property. Compare small type and table values before and after compression. Record the source and delivered filenames, page mapping, byte sizes and hashes. Deliver the single legible lodge PDF. Hold the attachment if the limit cannot be met without losing evidence.
