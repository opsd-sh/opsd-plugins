---
name: payroll-setup
description: Inspect a business's existing PAYE schemes and pay schedules, and identify the scheme and schedule to use for payroll. Use for discovery and selection, not creating or changing setup.
---

Use the Opsd connection and business selected by the user or established in the
conversation. If the business is unclear, use the [business discovery skill](../businesses/SKILL.md)
to resolve it, including practice clients. A known business ID can go directly
to these tools. Both tools require `api:read`.

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

A successful empty list means no schemes or schedules were returned for that
business. If a listing fails or its tool is unavailable, explain which part
could not be checked and keep any partial results labelled. A not-found error
can mean the business is missing or inaccessible. For insufficient scope, ask
the user to reconnect with Read permission; for authentication failure, ask
them to reconnect the same Opsd connection.
