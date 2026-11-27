---
name: meister-operator
description: Operate MeisterCRM through connected MCP tools. Onboard a workspace from a tour website and build a demo proposal with zero or placeholder prices. Manage leads, travelers, tasks, members, catalog items, rates, messages and templates. Populate Draft itineraries and save reusable proposal templates.
---

# Meister Operator

**Open [Approval Gates](references/approval-gates.md) at the start of every run, including read-only requests.** If the file is unavailable, stop before calling a tool. Choose the guide for the requested task below.

For supplier documents, use **Meister PDF to Contract** to prepare the rates and workbook. For a reviewed workbook or an existing supplier contract, use **Meister Contract Operator** to import, amend or verify catalog data.

## Connect and check access

In MeisterCRM, open **Settings → Integrations → MCP**, choose your client, and copy its setup prompt into that client. For manual setup, copy the server address and client ID on the card. Sign in yourself. On the approval screen, check the client, account and workspace. Choose **Read only**, **Select all**, or expand a category and check individual actions. Select all includes only actions available to your role and requested by this client. Review the selection before approving. Ask “Which MeisterCRM workspace am I connected to?” to check a connection with `get_context` access.

Check the tools on the current connection and the granted actions under **MCP** before starting a workflow. Reading and sending correspondence, managing templates and managing records have separate grants. To reply to a conversation, select both read and send for that channel. To look up a lead’s contact details, include lead read access. Correspondence already carries any lead links found by the CRM. To personalize a send with a saved template, include view access to templates for that channel. If a required grant is missing, the user can reconnect and review their selection. Newly available permissions require their approval. If the client only requests lead permissions, it must request the additional actions before they can appear. If an action is still unavailable on an older connection or the user’s role cannot perform it, give the CRM steps from the guide. A permission grant lets a tool run. The user still decides which records to change and which messages to send.

## What do you want to do?

| Task | Tools to look for on the connection | Guide |
| --- | --- | --- |
| Onboard an operator or recreate a published tour with demo pricing | Brand Kit, geography, catalog, lead and Draft itinerary actions | [Website itinerary to demo proposal](references/website-itinerary.md) |
| Identify the user and workspace, find pipeline stages or resolve a country or location | `get_context`, `list_countries`, `list_locations` | [Workspace](references/workspace.md) |
| Read workspace settings, check seats and members, invite a teammate, update a role or your profile | `get_workspace_seats`, `list_workspace_members`, `invite_workspace_member`, `update_member_role`, `get_workspace_settings`, `update_my_profile` | [Workspace](references/workspace.md) |
| Find, read, create, update or delete a lead. Change its stage, contact or traveler roster | `list_leads`, `get_lead`, `create_lead`, `update_lead`, `delete_lead` | [Leads](references/leads.md) |
| Read customer email, reply in a thread or send to a lead or email address | `list_email_accounts`, `list_emails`, `get_email`, `reply_email`, `send_email` | [Email](references/communications/email.md) |
| Read WhatsApp messages, reply in a chat or send to a phone number | `list_whatsapp_chats`, `list_whatsapp_messages`, `reply_whatsapp`, `send_whatsapp` | [WhatsApp](references/communications/whatsapp.md) |
| Find, apply, create, edit or delete a multilingual email or WhatsApp template | `list_message_templates`, `get_message_template`, `render_message_template`, `create_message_template`, `update_message_template`, `delete_message_template` | [Message templates and missing values](references/communications/templates.md) |
| Assign a lead to another user | `list_assignable_agents`, `assign_lead_agents` | [Lead assignment](references/leads.md) |
| Find, create, edit, resolve or reopen a task | `list_tasks`, `get_task`, `list_task_types`, `create_task`, `update_task`, `resolve_task`, `reopen_task` | [Tasks](references/tasks.md) |
| Choose which catalog record to edit | `describe_catalog_type`, `list_catalog_items`, `get_catalog_item` | [Catalog item types](references/catalog/item-types.md) |
| Create catalog items with verified descriptions and pictures, or edit an existing property, room, activity or fleet | `create_catalog_item`, `update_catalog_item`, `delete_catalog_item`, `attach_catalog_image`, `get_catalog_item` | [Catalog master records](references/catalog/master-records.md) |
| Add, change or remove an individual rate | `list_catalog_contracts`, `get_catalog_contract`, `create_catalog_contract`, `update_catalog_contract`, `delete_catalog_contract` | [Catalog contracts](references/catalog/contracts.md) |
| Download a template, validate and import a file, or export one item or a filtered catalog view | In MeisterCRM | [Catalog import and export](references/catalog/import-export.md) |
| View proposals, create a Draft, populate its itinerary or save a new reusable template | `get_proposal`, `create_proposal`, `set_draft_itinerary`, `create_proposal_template` and proposal list/context tools | [Proposals](references/proposals.md) |

For an owned Draft, use the [proposal guide](references/proposals.md) to populate its dated and global selections. Use the saved editor link for changes outside that action. A reusable template can be created from a saved proposal. Ordinary lead operations keep their documented effects on linked proposals.

Before a change, identify the workspace and exact record. When names match more than one record, ask the user to choose using the least personal information needed. Report what the saved result establishes. If a write times out, check the record before considering another write. If the result is still uncertain, say so.
