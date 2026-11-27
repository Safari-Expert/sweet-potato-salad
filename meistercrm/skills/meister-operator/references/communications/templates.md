# Email and WhatsApp message templates

[Skill index](../../SKILL.md) · [Approval Gates](../approval-gates.md) · [Email](email.md) · [WhatsApp](whatsapp.md)

These are reusable messages for the signed-in user. In **Settings → Integrations**, open **Email Templates** on the email card or **Manage Templates** on the WhatsApp card. Permission to manage email templates and permission to manage WhatsApp templates are separate. Use the corresponding tools below when available.

## Find and apply a template

1. Choose the channel first. List `type=email` for email or `type=chat` for WhatsApp. Identify the template by name and ID within that list.
2. Use the lead contact's `pref_language`. If it is blank, or the recipient is standalone, use the language explicitly requested for this message. Otherwise ask which language to use. Pass its key (e.g. `fr`) as `language` when rendering. Require a nonempty `message[language]` and, for a new email using a template subject, `subject[language]`. Replies keep the thread subject. WhatsApp uses only the body.
3. The picker can display fallback text when the translation is missing. Tell the user which language or field is missing and offer a matching template, an explicitly requested template translation, or a one-off draft in the requested language. Saving a reusable translation and sending a message are separate actions.
4. Use `render_message_template` with the template type and ID, and the lead ID or standalone recipient and language. For an email reply set `reply: true` to keep its thread subject. Preview the completed draft for the exact recipient and trip. Use the completed text in the single send or reply for that recipient. Resolve only the fields actually present. The supported lead fields in the composers are `{{contact.name}}`, `{{contact.surname}}`, `{{contact.mobile}}`, `{{contact.email}}` and `{{estimated_arrival_dt}}`.

## Fill missing values

An email address or phone number is enough to contact someone. A template can still be used when there is no lead, or when an identified lead is missing a value.

- Reuse values the user supplied for this recipient or that are verified on the selected lead. For example, the recipient's supplied email can fill `{{contact.email}}`. An email address does not supply a first name, mobile or arrival date.
- If a preview returns `missing`, ask for those values together. Pass the confirmed substitutions in `values`, keyed by placeholder name without braces, and render again. Check every placeholder in the selected body and any subject being used. Ask one question listing just the missing values in ordinary language. If a template contains a custom spelling such as `{{contact_name}}`, ask what text belongs there if unclear and substitute the confirmed value in the draft. The CRM's first-name field is `{{contact.name}}`.
- For example, given only a WhatsApp number and “Hi {{contact.name}}, is {{estimated_arrival_dt}} still your arrival date?”, ask **“What first name and arrival date should I use?”** If the user supplied the name already, ask only for the date. If the user doesn't know it, offer to reword that line.
- Substitute into the one-off draft and review the complete text. When automatic insertion needs a linked lead, enter the rendered text in the composer. Changes to the CRM contact or the reusable template require a separate request. Send only once all placeholders are resolved or the user chose wording that omits them.

## Create, read, update or delete

| Action | MCP tool | What to do |
| --- | --- | --- |
| List | `list_message_templates` | Read the signed-in user's channel-specific list. |
| View | `get_message_template` | Open the chosen record. Check its ID, channel and saved languages. |
| Create | `create_message_template` | Choose **New template**, give it a name and channel, enter each language's body and, for email, subject, then save. Let MeisterCRM assign the ID. |
| Update | `update_message_template` | Read the saved template first. Use the saved `id` and `type`. For each localized map you change, copy the current map, apply the requested edits and submit the complete resulting map as in the CRM. Preserve untouched languages and verify the saved translations. |
| Delete | `delete_message_template` | Identify the exact saved template, channel and languages. Follow [Approval Gates](../approval-gates.md) and verify it disappears from the correct channel list. |

Example of a new WhatsApp template with two language versions. On update, use the ID returned by the CRM and retain the other saved translations.

```json
{
  "name": "Arrival follow-up",
  "type": "chat",
  "message": {
    "en": "Hi {{contact.name}}, is {{estimated_arrival_dt}} still your arrival date?",
    "fr": "Bonjour {{contact.name}}, arrivez-vous toujours le {{estimated_arrival_dt}} ?"
  },
  "subject": { "en": "" }
}
```

For an email template, choose `"type": "email"` and supply the localized subjects, for example `"subject": {"en": "Your arrival date", "fr": "Votre date d’arrivée"}`. A template save prepares future drafts. It does not contact any recipient.
