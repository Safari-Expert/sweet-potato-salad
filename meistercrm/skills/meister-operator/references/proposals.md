# Proposals

[Skill index](../SKILL.md) · [Approval Gates](approval-gates.md)

Use MCP to read accessible proposals and templates, create blank or template-based Drafts, set an owned Draft’s itinerary and create a named template from a saved proposal. For other edits use the `editor_url` returned by `get_proposal`. Use the matching signed-in CRM environment.

## Find and view a saved proposal

Use `list_proposals` for the workspace or supply a `lead_id` to open the same set as a lead’s **Proposals** section. Match the name, lead, dates and status. If several versions fit, ask which one the user means. Use `get_proposal` with the selected ID to read its saved itinerary, travelers and totals. Name the proposal and currency when reporting prices. The browser may also contain unsaved edits. Reading a proposal does not authorize generating or sharing a customer copy.

## Prepare a new Draft

For a published tour, follow [Website itinerary to demo proposal](website-itinerary.md) for brand setup, destinations, catalog selections and verified demo pricing.

1. Read the lead for contact, main agent, destination, arrival and requested trip length. Resolve any missing required choices. Find a named template by name and destination even if its day count differs, and inspect its saved configuration. If the user asked for a template of a specific length, search `list_proposal_templates` by destination and days. If no template matches, search again without the days filter, follow any `next_offset`, and tell the user which alternatives are available by name and day count. Ask which template to use only if their request leaves the choice open. If the destination has no templates, offer a blank draft.
   The selected template determines the saved proposal duration. If it differs from the requested trip length, warn the user before creating the draft. For example, “This template creates a six-day proposal for your seven-day inquiry.” Proceed on the original create request once the template is identified and keep the lead’s trip length as recorded.
2. Call `get_proposal_creation_context` with `{}`. This reads the proposal defaults from the current workspace via the same account context used by the CRM create drawer. Read fresh values for this workspace. Use the customer’s explicit trip choices where given.
3. Build the create inputs below. Call `create_proposal` once. For a template-based draft pass the selected `template_id` in this same call. Use `allocation_options.max_room_capacity` only when the user selects that option. The source template remains available for reuse.
4. Check the new ID, lead and Draft status. Read it back with `get_proposal` to verify dates and itinerary. Count dated entries separately from global items. Give the user the editor link. After a timeout, check the lead's proposals before retrying.

| Create input | How the drawer fills it |
| --- | --- |
| `lead_id`, `proposal_name`, `trip_start_dt`, `arrival_country_id`, `duration_trip_days` | Use the intended lead and trip. Confirm ambiguous destinations or dates. Send the selected calendar date in ISO form, for example `2027-06-10T00:00:00Z`. Use the selected template’s `days` for `duration_trip_days` on a template draft and the intended trip length on a blank draft. The drawer sends `arrival_location_id: 1` for a new draft. |
| `proposal_currency`, `proposal_margin` | Use `default_base_currency` and the workspace `proposal_margin` fraction. For example, a 15% margin is `0.15`. If the context lacks the needed currency and the user has not specified one, clarify it. |
| `config` for a blank draft | Use `default_theme` as `theme_id`. Seed each of `sections.main`, `sections.hero` and `sections.ending` with one entry containing the destination country ID, `type: "country"` and `hide: false`. Set `hide_invoice` and `hide_printable` to false. |
| `config.features` | For a blank draft choose the first available feature-set name in the drawer’s alphabetical order from `feature_set_names`. Ignore legacy keys `true`, `false`, `included` and `excluded`. Send `{ "set_name": "<selected name>", "hide": false }`. If there are no feature sets, use an empty name and `hide: true`. |
| `config` for a template draft | Use the selected template’s theme, section entries/visibility, feature selection and printable setting when present. Retain valid selected feature sets, including a hidden set. Where a template has no configuration, use the ordinary blank-draft defaults. |
| `payment_config` | Use the lead contact’s `customer_name` and `customer_surname` from its first and last name. Set `currency` to `default_quote_currency`. Choose `account_details_id` from `account_details_ids`: prefer `default` when present, otherwise use the first returned account, and use `default` for the empty legacy selection. Include `default_payment_url` as `payment_url` when set. Use an empty `payment_schedule`, zero `customer_vat` and `discount`, and false for `hide_price`, `white_label`, `display_breakdown` and `display_aci_price` unless the user specifies a supported choice. For a requested discount, use a signed fraction between the workspace's `default_discount` (at least −1) and zero. Customer VAT is a fraction from zero to one. |

## Verify saved proposal settings

For blank and template drafts, check the fields returned by `get_proposal`. Compare the draft’s effective `config` (theme, sections, features and visibility) and `payment_config` (account selection, currency, discount, VAT and display flags) where present. Missing fields remain unverified. On older drafts, a zero, empty value or unchecked flag may be a CRM default.

If settings are missing, link to the draft and open **Timeline actions (⋮) → Edit**. **Theme Configurations** shows the effective theme, sections, feature display and Hide PDF. **Payment** shows currencies, discount, VAT, Hide Price, Whitelabel, Show Breakdown and Show ACI Prices. Report any remaining gaps. Payment account ID, payment URL, payment schedule and invoice visibility have no visible control in this drawer.

## Populate an itinerary or create a template

Read `get_proposal` for the saved status, dated and global items, and `revision`. For an owned Draft, use `set_draft_itinerary` with the complete ordered selections and `expected_revision`. Review and authorize existing item replacement before setting `replace_existing`. Read back the saved items and quotation. A new reusable template uses `create_proposal_template` with the saved ID, latest revision and a new name. Verify it with `list_proposal_templates`. See the [day and template workflow](website-itinerary.md#build-and-save-the-draft).

Use the lead’s **Proposals → Create Proposal** drawer when creation is unavailable. Use the proposal’s editor link for other changes, non-Draft itinerary edits, or timeline actions unavailable to this connection.
