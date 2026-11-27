# WhatsApp

[Skill index](../../SKILL.md) · [Approval Gates](../approval-gates.md) · [Message templates](templates.md)

Use `list_whatsapp_chats` for the signed-in user's connected account. The equivalent CRM page is **Chat** (`/chat`). A disconnected user can connect their account under **Settings → Integrations → WhatsApp**.

## Find and reply to an existing chat

1. Identify the intended chat by its title and participants. For a [specific lead](../leads.md#find-the-right-lead), compare its ID with the `leads[].lead_id` entries already returned on the chat. A conversation can link to several leads or none. The user can reply in any chat they can use in the CRM.
2. Use `list_whatsapp_messages` with `chat_id`. Read messages in time order and distinguish incoming messages, outgoing messages and CRM events. For “reply to the latest message,” identify the intended incoming message. A sidebar preview shows only the last message.
3. For a send request, use `reply_whatsapp` once with that `chat_id`, the final `body` and `confirmed: true`. Check the group or participant name when several chats look similar. For a summary or draft, return the requested text.
4. To personalize a reply, [render the chat template](templates.md) first and send the completed text. In the CRM, type `/` in the composer to choose a template. Verify the intended trip when the chat has multiple linked leads.

## Send to a new number

Use `send_whatsapp` once with `recipient` set to the international phone number, the final body and send approval. The CRM equivalent is **Chat → New WhatsApp message**. For a lead, use its verified `contact.mobile`. For a new contact, use the user-supplied number. If the country calling code is unclear, ask for the full international number.

A number alone is sufficient for a plain text message. For a template with missing values, [ask for the missing information](templates.md#fill-missing-values). Follow the [outbound guidance](../approval-gates.md#outbound-messages) and send one message per call. Check the chat before retrying an uncertain send. Report delivery or a read receipt only if the channel shows it.
