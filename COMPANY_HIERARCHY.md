# Company Hierarchy

Use this file as the single source of truth for resolving a user's supervisor. Keep the entries current.

## Resolution Rules

<!-- TODO=: In the future then implement this
1. Match the current user using the most specific available identifier: `user_id`, email, employee ID, or full name. -->
1. Match the current user by asking for name.
2. Use that user's `supervisor_role` as `payload.recipient_role` and use that user's `supervisor_name` as `payload.recipient_name`.
3. If the current user has no unique match, or has multiple matches, ask one concise clarification question before producing a notification.
4. Do not infer a supervisor from a user's job title alone when a direct mapping is available.

## User-to-Supervisor Mappings

Add one mapping for each user who can use the notification skill:

```yaml
users:
  - role: "Technician"
    name: "Prudence Nyambura"
    supervisor_role: "Engineer"
    supervisor_name: "Idris Vance"
  - role: "Technician"
    name: "Sarah Jenkins"
    supervisor_role: "Engineer"
    supervisor_name: "Idris Vance"
  - role: "Technician"
    name: "Davood Choi"
    supervisor_role: "Engineer"
    supervisor_name: "Elena Rostova"
  - role: "Technician"
    name: "Jonathan Kincaid"
    supervisor_role: "Engineer"
    supervisor_name: "Elena Rostova"
```

<!-- 
// TODO=: In the future then implement this
The `user_id` should be the stable identifier available to OpenClaw. Use the same identifier consistently for each user.
-->