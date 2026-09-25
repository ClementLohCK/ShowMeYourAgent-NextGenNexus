---
name: report-observation
description: Create an observation report when a fault, failure, damage, or unsafe operating condition is observed.
user-invocable: true
---

# Log Observation

Use this skill whenever the user reports or observes equipment damage, failure, a fault, or an unsafe condition, even if they do not explicitly ask to create a report.

## Output Schema

```json
{
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
```

## Rules

### 1. Pointers to follow
- Use only the fields in the Output Schema; do not add, rename, or omit any required keys.
- Always put the exact `action` and `endpoint` values in the Output Schema.
- Always put `payload.context.location.geocoord` to `false` because geolocation and location extrapolation are not implemented.
- If a required value is missing or ambiguous and cannot be inferred from the context, ask follow-up question(s) instead of inventing it.
- Follow-up questions should be clear, direct and conversational.
- Format follow-up questions using plaintext, do not use any interactive widgets or rich UI.
- Avoid asking a single question per turn, but also not more than 5 questions at once.

### 2. Visual Evidence Collection

- After the user started a message that needs to call this skill report-observation, then ask the user if they have a photo or image of this observation to attach
- Wait for the user's response. Do not proceed until they either:
  - Send an image (you'll see it as an attachment in the next message), or
  - Reply a message meaning "no" or "skip"
- If an image is provided, note its file path for the submission command.
- If the user don't have image or wants to skip, proceed to infer from their words.

### 3. Capture the observation
- Infer from context to put `Safety`, `Environment`, or `Social` in `payload.context.classification`.
- Infer from context to put `Safe` or `Unsafe` in `payload.context.observation_type` when `classification` is `Safety`.
- Infer from context to put `Positive` or `Negative` in `payload.context.observation_type` when `classification` is `Environment` or `Social`.
- Infer from context to put `Act` or `Condition` in `payload.context.observation_act_or_condition` for every classification.
- When `payload.context.location.geocoord` is `false`, the values `payload.context.location.country` and `payload.context.location.region` are required.
- Infer from context to put `India`, `Singapore`, `Vietnam`, `UAE`, or `Kenya` in `payload.context.location.country`.
- Infer from context to put `Central`, `East`, `West`, `North`, or `North-East` in `payload.context.location.region`.
- Infer from context to put `Manufacturing & Logistics` or `Energy & Utilities` in `payload.context.location.business_unit`.
- Put the concise and factual final observation in `payload.observation_narrative`, exclude data that can be found in Output Schema, preserve the user's wording where possible.

### 4. Resolve report details
- Put the current user's name in `payload.stakeholders.reported_by`. Ask for the user's name if the current user has no unique match in `workspace/COMPANY_HIERARCHY.md`.
- Put the report timestamp in `payload.stakeholders.reported_date_time` using ISO 8601 format in Singapore time (`Asia/Singapore`, GMT+8 / UTC+08:00).
- Use the date and time of the message first sent by the user and include the `+08:00` offset in the value.

### 5. Resolve the supervisor
- Always put `PowerGen` in `payload.contact_details.contractor`.
- Consult `workspace/COMPANY_HIERARCHY.md` as the single source of truth.
- If `workspace/COMPANY_HIERARCHY.md` does not exist, ask the user for the required supervisor contact details and put user's answers in `payload.contact_details.supervisor_role` and `payload.contact_details.supervisor_name`.
<!-- TODO=: `notify_admin` about this missing info -->
- Match the current user's name to exactly one `users` entry. If there is no unique match, ask for the user's name before performing the hierarchy lookup.
- Put the matched entry's `supervisor_role` in `payload.contact_details.supervisor_role`.
- Put the matched entry's `supervisor_name` in `payload.contact_details.supervisor_name`.

### 6. Validation
- Never assume an image is available or invent a file path.
- Validate the following fields in the JSON object before submission:
  - `payload.context.classification`: must be exactly one of `Safety`, `Environment`, or `Social` and should match the observation narrative.
  - `payload.context.observation_type`: must match the classification precisely:
    - `Safety` -> `Safe` or `Unsafe`
    - `Environment` or `Social` -> `Positive` or `Negative`
  - `payload.context.observation_act_or_condition`: must be exactly `Act` or `Condition` and should match the observation narrative.
  - `payload.context.location.geocoord`: must be exactly `false`.
  - `payload.context.location.country`: must be exactly one of `India`, `Singapore`, `Vietnam`, `UAE`, or `Kenya`.
  - `payload.context.location.region`: must be exactly one of `Central`, `East`, `West`, `North`, or `North-East`.
  - `payload.context.location.business_unit`: must be exactly `Manufacturing & Logistics` or `Energy & Utilities`.
- Never return placeholders or invented details.
- Preserve the user's wording and keep the report factual, concise, and free of invented details.
- Clarify the JSON output if any single field is missing, ambiguous, inconsistent, or invented.

### 7. Submission
After producing the valid JSON output, call the following submission script. Add the image path as the second argument only when an image is provided:
```bash
python3 ~/.openclaw/workspace/skills/report-observation/submit_observation_multipart.py '<json_string>' ['<file_path-to-image>']
```