# Approval Gates

Read this policy at the start of every run. Determine approval by what the action will do, including any existing records it will remove. First check the operation is in scope and the connected user can perform it. For CRM-only steps, explain what the user will review and do in the application.

## Actions that require explicit approval

| Action | What to identify before asking | Explain the effect |
| --- | --- | --- |
| [Save website branding or enable countries](destination-setup.md) | Connected workspace, current brand or countries, exact brand fields or additions | Get explicit approval for the named workspace and changes before `update_my_tenant`. |
| [Replace a populated Draft itinerary](website-itinerary.md) | Draft, latest saved revision, dated and global items to retain or remove | The new plan replaces the full selection. Explain the actual changes and obtain authorization before `replace_existing`. |
| [Update a user profile or member role](workspace.md) | Workspace, person if applicable, fields or permissions, current and proposed values | Who or what changes. For a role change, include the access the member gains or loses. |
| [Invite a teammate](workspace.md) | Workspace, exact recipient email and available seats when known | MeisterCRM may send an invitation. Distinguish the invitation from joining the workspace or purchasing a seat. |
| [Delete a lead](leads.md) with `delete_lead` | Workspace and exact lead name and ID | MeisterCRM soft-deletes the lead and its associated tasks and removes the lead's document files. |
| Remove existing travelers, fleet entries or other saved records as part of an allowed lead or catalog update | [Lead](leads.md) or [catalog item](catalog/master-records.md), and the people or entries that will be removed | A replacement list can remove entries even when the action is called Update. With `update_lead`, adding a traveler while keeping every existing traveler uses ordinary lead permissions. |
| [Delete a catalog item](catalog/master-records.md), [delete rates](catalog/contracts.md) or remove shared access | Owner, parent, selected items or rates, and affected children where known | Distinguish deleting an owned item and its dependent records from removing a shared item from this workspace. Note any resulting gap in rate coverage. |
| [Delete a message template](communications/templates.md) | Saved template ID, name, channel and languages | Removes the reusable template from the channel list. |
| [Commit an import](catalog/import-export.md) | Validated file version, language, catalog type, target workspace and intended records | Summarize additions or changes, scope and validation warnings. If the file or target changes, validate again and obtain approval for the revised import. |

**How to ask.** State the target and effect together. For example, “Delete ‘Example family trip’ (lead 108) in Demo Travel? This will soft-delete the lead and its associated tasks and remove its document files.” Wait for a clear affirmative answer before executing. One approval covers the exact action or batch the user reviewed. If the target, batch or effects change, present the revised action. A refusal or cancellation ends that write.

**Ordinary requests.** Reads, file validation and an explicitly requested in-scope routine create or update need no extra confirmation. For a backward lead move that can reset linked non-confirmed proposals to Draft, explain the effect and follow the [lead stage guidance](leads.md). For standalone task deletion, offer [Resolve](tasks.md). For proposal changes outside the owned Draft itinerary action, provide the [CRM editor link](proposals.md).

## Outbound messages

An explicit request to **send** or **reply** can authorize the specified communication. A request to read, summarize, draft or preview ends with that result. Confirm any ambiguous recipient, channel, sending account or message content. If a [template](communications/templates.md#fill-missing-values) lacks required values, ask for them before sending. Use one send or reply call for each requested message. Set `confirmed` on that call only when the user has authorized that recipient, channel and content.

For bulk outreach, warn the user that sending many similar messages together can trigger spam complaints or filtering. Suggest a smaller first group. Base this advice on the recipients, messages and timing in the request or on a plan the user has already described. Do not look up, ask for or keep a running total of previous sends.

| Requested outreach | Advice to give before sending |
| --- | --- |
| Email | When the plan calls for more than **30 emails in one day**, suggest spreading the emails across several days. |
| WhatsApp | When the request calls for more than **20 outgoing messages in one go**, suggest smaller groups spaced apart. Include multiple messages to the same recipient when considering the size of the request. |

For example, if the user asks to send the same email to 40 leads today, suggest sending to 20 today and the remaining 20 another day. The ordinary send authorization above applies. Get the user's choice before changing the recipient group or timing.

Report each send that the channel confirms. If a send has an uncertain outcome, check the same mailbox or chat before considering a retry. If the user stops or disconnects, do not issue further sends.

[Back to the skill index](../SKILL.md)
