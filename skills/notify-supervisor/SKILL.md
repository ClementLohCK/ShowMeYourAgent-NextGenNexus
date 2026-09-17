---
name: notify-supervisor
description: Notify the site supervisor about an urgent or critical safety, equipment, or operational issue that requires prompt attention or acknowledgment.
user-invocable: true
---

# Notify Supervisor

Use this skill when the site supervisor needs to be notified, especially when work is halted or safety is at risk, even if they do not explicitly ask to notify.

If the issue is not urgent or critical and the user has not asked to notify the supervisor, use a more appropriate reporting skill instead.

## Output

When all required values are available, return exactly one valid JSON object and no surrounding Markdown, explanation, or code fence.

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

### 1. Output contract
- Always use the exact `action` and `endpoint` values shown above.
- Use only the fields in the schema; do not add, rename, or omit any required keys.
- Return the JSON only after every required field is present and unambiguous.

### 2. Capture the notification
- Put the reported urgency in `payload.urgency`. Use only `low`, `medium`, or `critical`.
<!-- TODO=: - Preserve an explicitly provided urgency unless it is lower than the urgency implied by the context, then ask for confirmation. -->
- Put the concise, factual message and its operational impact in `payload.message`, preserving the user's wording where possible.

### 3. Resolve the supervisor
- Always set `payload.recipient_contractor` to `PowerGen`.
- Consult `workspace/COMPANY_HIERARCHY.md` as the single source of truth.
- If `workspace/COMPANY_HIERARCHY.md` does not exist, ask the user for the required supervisor contact details and set `payload.contact_details.supervisor_role` and `payload.contact_details.supervisor_name` from the user's answers.
<!-- TODO=: `notify_admin` about this missing info -->
- Match the current user's name to exactly one `users` entry. If there is no unique match, ask for the user's name before performing the hierarchy lookup.
- Set `payload.recipient_role` to the matched entry's `supervisor_role`.
- Set `payload.recipient_name` to the matched entry's `supervisor_name`.

### 4. Ask only when needed
- If a required value is missing or ambiguous, ask follow-up question(s) instead of inventing it.
- If more than one value is missing or ambiguous, ask exactly one concise follow-up question per turn, then wait for the user's answer before asking the next question.
- If the user answers a question with information for multiple fields, record every unambiguous value and ask only for the next missing or ambiguous field.

### 5. Validation
- Before producing the JSON, check every required payload field for missing, unclear, or conflicting values.
- Never return placeholders or invented details.
- Preserve the user's wording and keep the report factual, concise, and free of invented details.