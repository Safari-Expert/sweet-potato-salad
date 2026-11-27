# Leads and travelers

[Skill index](../SKILL.md) · [Approval Gates](approval-gates.md) · [Workspace lookups](workspace.md)

The standard connector supports lead CRUD. Each action runs with the connected user’s current permissions.

## Find the right lead

1. Use `get_context` to identify the workspace and its stage labels when needed. `list_leads` defaults to the connected agent and the usual active stages. Optional inputs are `agent_id`, `stage_ids` and a case-insensitive `query` on contact name or email. Another agent’s ID only filters the records the caller is allowed to see.
2. The list returns up to 100 matches. If `truncated` is true, narrow the search. The tool has no date filter or pagination. For a date-based search, use the date filters in the CRM’s Dashboard or Pipeline and check which date the filter applies to.
3. Use `get_lead` with a positive `lead_id` to read the exact lead, contact and travelers. When names collide, show the smallest useful set of distinguishing details and ask the user which record they mean. A lead can disappear from a filtered view after a stage change.

To open an identified lead, return a clickable **Open lead in MeisterCRM** link. In development, use `https://dev.meistercrm.com/lead?lead_id={lead_id}` with the actual lead ID. Use the CRM address for the connected environment. Include the link when a user needs to continue in the CRM or open a newly created lead.

For a request to contact the lead or read their correspondence, use the [Email](communications/email.md) or [WhatsApp](communications/whatsapp.md) guide. Match the lead ID on the conversation and verify the channel recipient.

## Create

Use `create_lead` with `fields`. For a direct inquiry, require the contact’s name, an email or mobile number, the destination country, the estimated arrival date and `contact.pref_language`. Use the customer’s known preferred language. When the preference is unavailable, send `EN`. If the user supplies an ambiguous language or any other required detail is missing or unclear, ask one question covering the missing or unclear details before creating the lead. Resolve the destination country with `list_countries` and preserve the intended calendar date. Include the trip length and per-person budget when supplied.

A synthetic example, assuming the destination lookup returned country ID 17:

```json
{
  "fields": {
    "contact": {"name": "Casey", "surname": "Example", "email": "casey@example.invalid", "pref_language": "EN"},
    "destination_country_id": 17,
    "estimated_arrival_dt": "2028-06-12T00:00:00Z",
    "duration_trip_days": 5,
    "budget_per_person": 2400
  }
}
```

The new lead is assigned to the connected user. An existing workspace contact may be reused. Check the saved lead ID, contact, preferred language and trip. If creating the lead times out, look for that lead before considering another attempt.

A represented inquiry uses a saved representative from **Brand Kit**. The standard connection supports the create-time `represented` flag but cannot look up those representatives. For an inquiry that requires that selection, use the **Lead** drawer, choose the represented option, and select the intended representative. A CRM team member assigned to a lead and the external representative are different people.

## Edit contact details, fields or stage

Use `update_lead` with `lead_id` and `changes` containing only the intended edits. For example, update an email with `{"lead_id":42,"changes":{"contact":{"email":"new@example.invalid"}}}`. A contact reused by several leads can reflect the change on those leads. When editing tags or metadata, preserve other entries in the same collection. Use the CRM for document updates or uploads.

For a stage change, resolve the requested stage ID from `get_context`. If **Quoted** is stage 7 in this workspace, send `{"lead_id":42,"changes":{"stage_id":7}}`. Verify the returned stage or reread the lead. A normal stage move can trigger configured workflows. Moving a lead back across confirmation can return linked non-confirmed proposals to Draft. Explain that effect **before** making such a move. An authorized lead move proceeds under the usual lead rules and needs no separate proposal approval. For a request to edit a proposal itself, give the user the [proposal editor link](proposals.md) for that proposal.

## Add, edit or remove travelers

1. Read `get_lead` immediately before changing travelers. A returned `travelers: []` is an empty roster. If the roster is missing or incomplete, stop before sending any replacement.
2. Copy the full roster with each existing `traveler_id` and its unchanged writable fields. Keep existing passport data out of the conversation summary. Append a new traveler without an ID. For a date of birth on create or update, send the supplied calendar day at midnight UTC as an RFC 3339 timestamp, as shown below.
3. Send the full resulting array in `changes.travelers`. An omitted person is removed. An empty array removes everyone. Follow [Approval Gates](approval-gates.md) for any omitted saved traveler ID. Only after that approval pass `confirmed: true` to `update_lead`. Additions and edits retaining every saved ID need no removal confirmation. The tool accepts up to 100 travelers. For a larger roster, use the CRM without splitting the change into multiple replacements.
4. Check the resulting IDs and people, including the retained travelers. If the write outcome is unclear, reread before any retry. An intended lead roster change can affect linked proposals.

Append this row to the roster after checking the traveler is new.

```json
{"traveler_first_name":"Robin","traveler_last_name":"Example","traveler_dob":"1990-05-14T00:00:00Z"}
```

## Assign another user

Read `get_lead` for the current agents. Find the intended teammate with `list_assignable_agents`, then use `assign_lead_agents` with `lead_id`, the intended `main_agent_id` and the complete `assigned_agent` list, including the main agent. Retain everyone the user wanted to keep. Assignment can notify the affected users. Verify both the main agent and assignee list after the change. If the tools are unavailable, open the lead’s agent selector in the CRM and choose **Update Lead Agents**.

## Delete

Resolve the exact lead and workspace. Before `delete_lead`, follow [Approval Gates](approval-gates.md) and explain that the lead and associated tasks are soft-deleted and its document files are removed. After approval, submit the exact `lead_id` once with `confirmed: true`. Verify that the result identifies that lead and reports deletion. If the result is unclear, reread where possible and report any uncertainty about the document files.
