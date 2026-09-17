---
name: report-observation
description: Create an observation report when a fault, failure, damage, or unsafe operating condition is observed.
user-invocable: true
---

# Log Observation

Use this skill whenever the user reports or observes equipment damage, failure, a fault, or an unsafe condition, even if they do not explicitly ask to create a report.

## Output

When all required values are available, return exactly one valid JSON object and no surrounding Markdown, explanation, or code fence:

```json
{
  "action": "report_observation",
  "endpoint": "POST /v1/maintenance/observations",
  "payload": {
    "context": {
      "critical_condition": "<low|medium|critical>",
      "equipment": "<equipment identifier>",
      "location": "<site location>"
    },
    "stakeholders": {
      "reported_by": "<current user's name>",
      "reported_date_time": "<report date and time in ISO 8601 format>"
    },
    "contact_details": {
      "contractor": "PowerGen",
      "supervisor_role": "<supervisor_role from workspace/COMPANY_HIERARCHY.md>",
      "supervisor_name": "<supervisor_name from workspace/COMPANY_HIERARCHY.md>"
    },
    "observation_narrative": "<concise summary of the observation using the user's words where possible>"
  }
}
```

## Rules

- Always use the exact `action` and `endpoint` values shown above.
- Put the reported severity or condition level in `payload.context.critical_condition`. Use only `low`, `medium`, or `critical`.
- Put the reported equipment identifier in `payload.context.equipment`. Ask for it if it is missing or ambiguous.
- Put the reported site, zone, or sector in `payload.context.location`.
- Put the current user's name in `payload.stakeholders.reported_by`. Ask for the user's name if the current user has no unique match in `workspace/COMPANY_HIERARCHY.md`.
- Put the report date and time in `payload.stakeholders.reported_date_time` using ISO 8601 format. Use the date and time of the message first sent by user.
- Always set `payload.contact_details.contractor` to `PowerGen`.
- Consult `workspace/COMPANY_HIERARCHY.md` as the single source of truth to match the current user's name to exactly one `users` entry. Ask for the user's name if the current user has no unique match in `workspace/COMPANY_HIERARCHY.md`.
- Set `payload.contact_details.supervisor_role` and `payload.contact_details.supervisor_name` from the matched entry's `supervisor_role` and `supervisor_name`.
- If `workspace/COMPANY_HIERARCHY.md` does not exist, ask the user for the required contact details and set `payload.contact_details.supervisor_role` and `payload.contact_details.supervisor_name` to the user's answers.
<!-- TODO=: `notify_admin` about this missing info -->
- Summarize the gathered observation in `payload.observation_narrative`, reusing the user's words as much as possible while keeping it concise and factual.
- If a required value is missing or ambiguous, ask follow-up question(s) instead of inventing it.
  - if more than one value is missing or ambiguous, ask exactly one concise follow-up question per turn, then wait for the user's answer before asking the next question.
  - If the user answers a question with information for multiple fields, record all unambiguous values and ask only the next missing or ambiguous field.
- Before producing the JSON, check each required payload field for a missing or ambiguous value. Never return the JSON object until every required field is present and unambiguous.
- Preserve the user's wording and do not add fields that are not in the schema.
