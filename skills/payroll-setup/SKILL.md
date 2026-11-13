---
name: payroll-setup
description: Inspect existing PAYE schemes, pay schedules and practice HMRC reporting details in Opsd. Use for discovery and selection, not creating or changing setup.
---

Use the Opsd connection selected by the user or established in the conversation.
All three tools require `api:read`.

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
scope, ask the user to reconnect with Read permission; for authentication
failure, ask them to reconnect the same Opsd connection.
