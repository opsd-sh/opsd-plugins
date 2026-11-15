---
name: employees
description: Find employees and employments, create employee and employment records, and update personal details in Opsd. Use for discovery, employee maintenance and employment onboarding.
---

Use the Opsd connection and business selected by the user or established in the
conversation. If the business is unclear, use the [business discovery skill](../businesses/SKILL.md),
including practice clients. Keep operations on that connection and business.
Lookups require `api:read`; creation and employee updates require `api:write`.
Write alone is sufficient when the business, employee and requested details are
known; a preliminary lookup is not required.

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

Create or update employee records when requested. Both business admins and
payroll operators can do this, including users with access through a practice.

- `create_employee` requires `business_id`, `forenames` as an ordered list,
  `surname`, `date_of_birth` in YYYY-MM-DD format, `sex` for HMRC (M or F), and
  `address`. Ask for missing required details; do not infer sex from a name or
  title. Optional `title`, `passport_number` and `national_insurance_number`
  can be omitted or null when not supplied. Provide a passport number if it was
  collected during right-to-work checks, as text preserving any leading zeros.
  Do not invent a National Insurance number when it is unknown.
- An address has `type` equal to `uk`, `foreign` or `lines`, with two to four
  `lines`. UK addresses also need `postcode`; foreign addresses need `country`
  as a name. The `lines` form has neither. Use the user's actual address and
  report validation problems rather than inventing replacement details.
- `update_employee` requires `business_id`, `employee_id` and at least one
  detail to update. Send only requested changes. Omission preserves every
  field. Null clears only `title`, `passport_number` and
  `national_insurance_number`; it leaves other fields unchanged. `forenames`
  replaces the full list and `address` replaces the whole address, so collect
  the complete replacement when either is being changed.

`create_employee` does not detect duplicate people or create an employment. Each
successful call creates another employee, even with identical details. After
an uncertain creation outcome, use Read access to investigate when available;
a matching name alone does not prove success. Explain unresolved uncertainty
and ask before another creation attempt. Use the returned employee ID for
later work and do not create another person just to add an employment.

Employee updates retain the server's payroll protections. Changes can conflict with
existing NI categories, a tax-year rollover in progress, or finalized payroll
history. After finalized payroll, identity changes and changing or clearing an
existing NI number are currently blocked; adding a missing NI number is still
permitted unless another restriction applies. Explain the returned conflict
without changing other records to bypass it. Employee maintenance does not
change employment settings, recalculate a run or submit anything to HMRC.

For employment creation, read [employment onboarding](references/employment-creation.md).
`create_employment` links an existing employee to a scheme and schedule, records
starter evidence and resolves initial tax settings. It requires explicit pay,
hours, NI and loan declarations. Existing employment updates and tax-code
notices are not yet available through tools.

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
scope, explain whether the operation needs Read or Write and ask the user to
reconnect with the missing permission. For authentication failure, ask them to
reconnect the same Opsd connection.
