---
name: notify-supervisor
description: Notify the site supervisor about an urgent or critical safety, equipment, or operational issue that requires prompt attention or acknowledgment.
user-invocable: true
---

# Notify Supervisor

Use this skill when the site supervisor needs to be notified, especially when work is halted or safety is at risk, even if they do not explicitly ask to notify.

## Output

When all required values are available, return exactly one valid JSON object and no surrounding Markdown, explanation, or code fence:

```json
{
  "action": "notify_supervisor",
  "endpoint": "POST /v1/notifications/notify",
  "payload": {
    "recipient_contractor": "PowerGen",
    "recipient_role": "<supervisor_role from workspace/COMPANY_HIERARCHY.md>",
    "recipient_name": "<supervisor_name from workspace/COMPANY_HIERARCHY.md>",
    "urgency": "<low|medium|urgent>",
    "message": "<concise description of the issue and its operational impact>"
  }
}
```

## Rules

- Always use the exact `action` and `endpoint` values shown above.
- Ask the user for their name when it is not already known.
- Always set `payload.recipient_contractor` to `PowerGen`.
  - Set `payload.recipient_role` to the matched entry's `supervisor_role`.
  - Set `payload.recipient_name` to the matched entry's `supervisor_name`.
- Consult `workspace/COMPANY_HIERARCHY.md` as the single source of truth to match the current user's name to exactly one `users` entry.
- Set `payload.urgency` to one of `low`, `medium`, or `urgent` based on the context. Preserve an explicitly provided urgency unless the explicitly provided urgency is lower than context, then ask for confirmation.
- Put a concise, factual description of the issue and its operational impact in `payload.message`.
- Preserve the user's wording and do not add fields that are not in the schema.
- If the issue is not urgent or critical and the user has not asked to notify the supervisor, use a more appropriate reporting skill instead.
- If a required value is missing or ambiguous, ask follow-up question(s) instead of inventing it.
  - if more than one value is missing or ambiguous, ask exactly one concise follow-up question per turn, then wait for the user's answer before asking the next question.
  - If the user answers a question with information for multiple fields, record all unambiguous values and ask only the next missing or ambiguous field.
- Before producing the JSON, verify that the message is present, specific, and unambiguous. Never return the JSON object with a placeholder or invented detail.