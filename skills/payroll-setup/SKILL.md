---
name: payroll-setup
description: Inspect or create PAYE schemes and pay schedules in Opsd, and read practice HMRC reporting details. Use for payroll setup and selection.
---

Use the Opsd connection selected by the user or established in the conversation.
The three lookup tools require `api:read`; the two creation tools require
`api:write`. Write alone permits creation when the necessary inputs are known.

For business payroll setup, use the selected business. If it is unclear, use
the [business discovery skill](../businesses/SKILL.md) to resolve it, including
practice clients. A known business ID can go directly to the business tools.

- Call `list_paye_schemes` with `business_id` to inspect schemes. Results include
  each scheme's public ID, name, employer reference, accounts office reference,
  optional company UTR, recorded tax-year settings and rollover generation.
- Call `list_pay_schedules` with the same `business_id` to inspect schedules.
  Each schedule has its own ID, name, frequency and `paye_scheme_id`. To show
  schedules for one scheme, filter the returned records by that scheme's ID.
  The tool lists the whole business; it has no scheme-filter argument.

Use returned IDs to link schedules to schemes. Names may be repeated across
schemes, so a schedule name alone need not identify the intended schedule.
Match the user's requested scheme and schedule within the selected business.
If several candidates fit, show their names, scheme references and IDs and ask
which to use. Call only the listings needed to answer the request.

Report null tax-year settings as unconfigured; do not fill them from today's
date. Employment Allowance is the recorded choice, not evidence of eligibility
or an accepted HMRC submission. A schedule's frequency does not specify a pay
date. These listings do not establish that payroll is ready to submit.

Create setup only when requested. Both business admins and payroll operators
can create schemes and schedules, including users with access through a practice.
A known business or scheme ID needs no preliminary lookup, but a schedule's
scheme must belong to the selected business.

- Call `create_paye_scheme` with `business_id`, `name`, `employer_reference`,
  `accounts_office_reference`, `tax_year_start` and `employment_allowance`.
  Use the user's actual HMRC references. `company_utr` is optional: supply it
  when provided, otherwise omit it or pass null. The supported start year is
  currently `2026` for 2026–27. The allowance choice must be explicitly
  `claiming` or `not_claiming`; ask for missing required information instead of
  guessing the references, tax year or eligibility decision. This records an
  existing HMRC registration locally, without registering an employer with HMRC
  or submitting an Employment Allowance claim. It creates no pay schedule.
- Call `create_pay_schedule` with `business_id`, `paye_scheme_id`, `name` and
  `frequency`. Currently only `monthly` is supported; do not substitute monthly
  for a requested unsupported frequency. When a requested workflow creates both
  records, use the ID returned by successful scheme creation for the schedule.
  A schedule groups employments; it does not set a pay date or create a pay run.

Both operations leave payroll subscriptions and HMRC submissions unchanged.
Report what was created using the returned IDs. If the scheme succeeds but
schedule creation fails, report that partial result and retain the scheme ID.

An employer reference is unique within a business. A conflict from
`create_paye_scheme` does not update the existing scheme or prove its settings
match the request. If Read permission is available, inspect `list_paye_schemes`
to identify the existing record and compare its settings. Do not change the
reference merely to bypass a conflict.

Schedule names are not unique: repeating a successful creation call creates
another schedule. After a timeout, connection failure or internal error with an
uncertain outcome, do not automatically retry creation. Use the relevant listing
when Read permission is available to help check what happened; a matching name
alone is not proof of success. Explain unresolved uncertainty and ask before
another attempt. A clear validation rejection can be corrected before retrying.

For a practice's HMRC agent reporting identity, call `get_practice_hmrc_reporting`
with `practice_id`. Resolve a practice name with `list_practices` when needed.
Both practice admins and members can read these details. When starting from a
practice client, use its owning practice ID, not the client's business ID.

The reporting name is separate from the practice's display name. Report the
stored name, address and contact details as returned; null optional fields mean
not recorded. These are current saved reporting details, not Government Gateway
credentials, proof of HMRC acceptance, or a record of what a past submission
contained. Do not request HMRC credentials for these lookups.

A successful empty list means no schemes or schedules were returned for that
business. If a lookup fails or its tool is unavailable, explain which part
could not be checked and keep any partial results labelled. A not-found error
can mean the business or practice is missing or inaccessible. For insufficient
scope, explain whether the operation needs Read or Write and ask the user to
reconnect with the missing permission. For authentication failure, ask them to
reconnect the same Opsd connection.
