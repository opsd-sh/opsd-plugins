# Create a practice

Use `create_practice` when the user asks to create a new practice in Opsd.
It requires `api:write`; Read and existing practice membership are not required.
For a business owned by an existing practice, use `create_practice_business`.
An unsuccessful lookup alone does not authorize creating either record.

Obtain the practice display `name` and `hmrc_reporting.name`, the agent name
used for HMRC reporting. They are separate fields and may differ. Do not infer
the reporting name from the display name unless the user says to use the same
name. Display names allow 1–120 characters after trimming; reporting names
allow 1–35 characters and must satisfy HMRC's character restrictions.

The minimum arguments are:

```json
{
  "name": "Example Accountants",
  "hmrc_reporting": { "name": "Example Payroll Services" }
}
```

Include reporting details the user supplies under `hmrc_reporting`:

- `address`: `lines` (one to four), with optional `post_code` and `country`.
  Each line allows up to 35 characters.
- `contact_name`: `forenames` (one or two) and `surname`, with optional `title`.
- `email` and `telephone`: optional reporting contact details.

Omit optional values or use null when not supplied. Do not invent contact
information or silently replace rejected values. Report validation errors so
the user can correct the input. These are reporting details, not Government
Gateway credentials; never request HMRC passwords or sender credentials in chat.

Success returns `id`, `name` and `role: "admin"`. The connected account becomes
the practice's admin; do not supply another user ID or choose an initial role.
This saves the practice and reporting identity locally. It does not register
an agent with HMRC, invite members, create clients or enable payroll.

Every successful call creates a separate practice, even with the same name.
After an uncertain response, do not automatically retry. With Read permission,
`list_practices` can help investigate, but a matching name alone does not prove
which call created it. Explain unresolved uncertainty and ask before another
creation attempt. Use `get_practice_hmrc_reporting` if a later request needs
to inspect the saved reporting details; it requires Read permission.
