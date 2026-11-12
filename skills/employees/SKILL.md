---
name: employees
description: Find employees and their employments in an Opsd business, and inspect their personal details or stored payroll settings. Use for lookups, not creating or changing records or calculating payroll.
---

Use the Opsd connection and business selected by the user or established in the
conversation. If the business is unclear, use the [business discovery skill](../businesses/SKILL.md),
including practice clients. Keep all lookups on that connection and business.
These tools require `api:read`.

An employee is a person on the business's payroll, not an application user or
business member. An employment links that employee to a PAYE scheme and pay
schedule and holds payroll settings. One employee can have several employments,
including more than one under the same scheme. Employee and employment IDs are
different and cannot be used interchangeably.

- For a known employee ID, call `get_employee` with `business_id` and
  `employee_id`. To find someone by name, call `list_employees` with only
  `business_id` and match their forenames and surname locally.
- For a known employment ID, call `get_employment` with `business_id` and
  `employment_id`. To find an employee's employments, call `list_employments`
  with only `business_id` and filter the returned records by `employee_id`.
  This listing has no employee, scheme or schedule filter arguments.
- To identify the scheme or schedule by name, use the [payroll setup skill](../payroll-setup/SKILL.md)
  and match `paye_scheme_id` and `pay_schedule_id` within the same business.

If names or employments are ambiguous, show the matching names and IDs, with
scheme and schedule names when available, and ask which to use. Do not assume
the first employment is the intended one. A listed record already contains its
details; fetch it again only when a fresh lookup is needed. Present the personal
and payroll fields relevant to the request rather than reproducing every field.

Money fields are integer pence. `monthly_gross_pay_pence` is a stored default,
not a calculated payment. `previous_employment` amounts apply to the returned
tax year and are separate from this employment's year-to-date totals. Preserve
negative tax amounts. Starter evidence and current tax settings are separate;
report their stored values without deriving new tax treatment. Null settings
are unconfigured or unavailable, distinct from explicitly supplied `not_provided`
starter information. These records alone do not establish payroll readiness.

A successful empty list means no matching records were returned; an employee
may have no employments. A not-found error can mean a missing or inaccessible
business, or a record that is absent from the supplied business. Do not search
another business or connection to work around that error. If a tool fails or
is unavailable, identify the gap and label any partial results. For insufficient
scope, ask the user to reconnect with Read permission; for authentication
failure, ask them to reconnect the same Opsd connection.
