# Workspace and team

[Skill index](../SKILL.md) · [Approval Gates](approval-gates.md)

## Identify the workspace and destination

| User needs | Connected tool | What to check |
| --- | --- | --- |
| Confirm the account, workspace or available lead stages | `get_context` with `{}` (no arguments) | Check the returned user and workspace before acting. Match a stage by its label in that workspace. Use `list_assignable_agents` for lead assignments, `list_workspace_members` for the team and `get_workspace_seats` for seat counts. |
| Select a destination country | `list_countries` with `{}` | Match the country by name and use the returned country ID in the lead tool. |
| Choose a location | `list_locations` with `{}` | Match both the location and its country. The available list is limited to the workspace’s countries. If two places match, ask which one the user means. If none match, report that before attempting a write. |

`get_context` identifies the connected user and returns the fields used for lead work. These include the user’s ID, name, language and time zone, plus workspace identity and lead stages when available. Team membership, seats, billing and integration settings are outside this tool’s response.

## Manage workspace settings and profile details

For onboarding, use [Brand Kit, countries and locations](destination-setup.md) to review the business brand and enable the trip’s destinations.

Use `get_workspace_settings` to review the current workspace defaults and your own profile. For a teammate, use `list_workspace_members` and match the exact identity. Use `get_my_tenant` for brand and enabled countries and `update_my_tenant` for explicitly approved brand fields and country additions. The CRM settings sections handle other workspace defaults. For an invitation, profile update or member-role change, follow [Approval Gates](approval-gates.md) and use the exact workspace ID the user approved.

| Change | Where to go in MeisterCRM | Verify |
| --- | --- | --- |
| Update your own name, phone, language or time zone with `update_my_profile` | **Settings → Account**. Review the signed-in identity, update the chosen field and save. | Reopen the profile and read back that field. |
| Change the workspace name, currency or proposal margin default in the CRM | Choose the section that owns it. For example, open **Settings → Brand Kit** for the organization’s displayed name or **Settings → Proposal** for proposal defaults. Identify the workspace and distinguish a workspace-wide default from a change to a single record. | Reopen the same setting. When changing a list, retain the entries the user wanted to keep. |
| Change a member’s role with `update_member_role` | Open **Settings → Subscription → Members**. Match the person by email, review the current and requested roles, then use the role control if available. | Check the role beside the same member after saving. |

The CRM shows restricted Settings sections to organization owners and managers. Available actions also depend on the signed-in user’s permissions. If the required control is unavailable, refer the user to a workspace administrator.

## Check seats and send an invitation

1. Read `get_workspace_seats` or open **Settings → Subscription** to check the current seat allowance and occupied seats for the named workspace. A workspace with eight seats and six members has two seats available at that moment. Report the available seats, or tell the user when capacity is unknown. If all seats are occupied, explain that the workspace has no free seats. The CRM applies its normal invitation rules.
2. Use `invite_workspace_member` with the exact recipient email and approved workspace, or choose **Invite User** in **Members**. An operator using an invitation tool must obtain approval for that workspace and email before sending. An invitation does not authorize purchasing seats or changing roles.
3. A successful request is acknowledged. Report it as an **invitation request received**. Delivery, acceptance and membership are separate outcomes. Verify membership from the Members list when needed.
