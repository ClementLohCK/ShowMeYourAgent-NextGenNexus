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
      "classification": "<Safety|Environment|Social>",
      "observation_type": "<Safe|Unsafe for Safety; Positive|Negative for Environment or Social>",
      "observation_act_or_condition": "<Act|Condition>",
      "location": {
        "geocoord": false,
        "country": "<India|Singapore|Vietnam|UAE|Kenya>",
        "region": "<Central|East|West|North|North-East>",
        "business_unit": "<Manufacturing & Logistics|Energy & Utilities>"
      }
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

### 1. Output contract
- Always set the exact `action` and `endpoint` values shown above.
- Use only the fields in the schema; do not add, rename, or omit any required keys.
- Return the JSON only after every required field is present and unambiguous.

### 2. Capture the observation
- Use only `Safety`, `Environment`, or `Social` in `payload.context.classification`.
- Use only `Safe` or `Unsafe` in `payload.context.observation_type` when `classification` is `Safety`.
- Use only `Positive` or `Negative` in `payload.context.observation_type` when `classification` is `Environment` or `Social`.
- Use only `Act` or `Condition` in `payload.context.observation_act_or_condition` for every classification.
- Always set `payload.context.location.geocoord` to `false` because geolocation and location extrapolation are not implemented.
- When `payload.context.location.geocoord` is `false`, the values `payload.context.location.country` and `payload.context.location.region` are required.
- Use only `India`, `Singapore`, `Vietnam`, `UAE`, or `Kenya` in `payload.context.location.country`.
- Use only `Central`, `East`, `West`, `North`, or `North-East` in `payload.context.location.region`.
- Use only `Manufacturing & Logistics` or `Energy & Utilities` in `payload.context.location.business_unit`.
- Put the concise, factual observation in `payload.observation_narrative`, preserving the user's wording where possible.

### 3. Resolve report details
- Put the current user's name in `payload.stakeholders.reported_by`. Ask for the user's name if the current user has no unique match in `workspace/COMPANY_HIERARCHY.md`.
- Put the report timestamp in `payload.stakeholders.reported_date_time` using ISO 8601 format in Singapore time (`Asia/Singapore`, GMT+8 / UTC+08:00).
- Use the date and time of the message first sent by the user and include the `+08:00` offset in the value.

### 4. Resolve the supervisor
- Always set `payload.contact_details.contractor` to `PowerGen`.
- Consult `workspace/COMPANY_HIERARCHY.md` as the single source of truth.
- If `workspace/COMPANY_HIERARCHY.md` does not exist, ask the user for the required supervisor contact details and set `payload.contact_details.supervisor_role` and `payload.contact_details.supervisor_name` from the user's answers.
<!-- TODO=: `notify_admin` about this missing info -->
- Match the current user's name to exactly one `users` entry. If there is no unique match, ask for the user's name before performing the hierarchy lookup.
- Set `payload.contact_details.supervisor_role` to the matched entry's `supervisor_role`.
- Set `payload.contact_details.supervisor_name` to the matched entry's `supervisor_name`.


### 5. Ask only when needed
- If a required value is missing or ambiguous, ask follow-up question(s) instead of inventing it.
- If more than one value is missing or ambiguous, ask exactly one concise follow-up question per turn, then wait for the user's answer before asking the next question.
- If the user answers a question with information for multiple fields, record every unambiguous value and ask only for the next missing or ambiguous field.

### 6. Validation
- Before producing the JSON, check every required payload field for missing, unclear, or conflicting values.
- Never return placeholders or invented details.
- Preserve the user's wording and keep the report factual, concise, and free of invented details.