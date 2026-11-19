# Employment onboarding

Use `create_employment` when the user wants to add a job for an employee. Both
business admins and payroll operators can do this, including access through a
practice. It requires `api:write`; known IDs need no preliminary Read lookup.

An employment is separate from the person record. Reuse the existing
`employee_id` when adding another job. The employee and PAYE scheme must belong
to the selected business, and the pay schedule must belong to that scheme.
Resolve ambiguous names with the discovery tools when Read is available.

Supply all of these fields:

- `business_id`, `employee_id`, `paye_scheme_id` and `pay_schedule_id`.
- `monthly_gross_pay_pence`: the agreed monthly default in integer pence, not
  pounds. Zero is valid when intended; the maximum is `99999999999` pence.
- `normal_weekly_hours_band`: `less_than_16`, `sixteen_to_less_than_24`,
  `twenty_four_to_less_than_30`, `thirty_or_more` or `other`. Use the normal
  weekly pattern, not this month's paid hours. `other` means no normal pattern,
  not missing information.
- `start_date`: YYYY-MM-DD, currently from 2026-04-06 through 2027-04-05. The
  scheme must be configured for 2026-27. Use the actual start date; do not move
  it into the supported year to bypass validation.
- `ni_category`: currently A, B, C, H, J, M, V, X or Z. Use the supplied category;
  the server checks compatibility with the employee. Do not substitute A for
  a missing or unsupported category.
- `student_loan` and `postgraduate_loan`: both require an explicit
  `not_applicable` declaration. Deductions are not yet supported; do not use
  `not_applicable` as a fallback when a loan applies or the answer is unknown.
- `starter_information`: one of the evidence forms below.

Ask for required information not already established in the conversation. Do
not infer declarations, fabricate P45 evidence or supply a guessed tax code.

For a starter checklist, use `{"type":"checklist","declaration":"A"}` with
A, B or C as supplied by the employee. For no starter information, use
`{"type":"not_provided"}` only when the user establishes that none is available;
this is an explicit choice, not a substitute for a missing answer.

For the P45 from the last previous job, use `type: "p45"` with a nested `p45`
object containing `leaving_date`, `tax_code` and `tax_details`:

- Cumulative evidence uses `basis: "cumulative"`,
  `total_pay_to_date_pence` (non-negative) and `total_tax_to_date_pence` (signed).
  Preserve tax refunds as negative pence.
- Week 1/month 1 evidence uses `basis: "non_cumulative"`, without cumulative
  totals. Keep the tax code and basis separate.
- The leaving date must not follow the new job's start date. A P45 dated before
  2025-04-06 also requires `starter_declaration` alongside the `p45` object,
  describing the employee's circumstances at the employment start. Ask for it
  when needed. Initial P45 treatment for SD2 and SD3 is not yet supported.

The server resolves and stores initial tax treatment from that evidence. Report
its returned tax code, basis and applicable previous-job amounts; do not compute
or override them yourself. Evidence totals and the resolved previous-job amounts
can differ when the P45 is from an earlier tax year.

Every successful call creates another employment, even with identical inputs.
After a timeout or another uncertain creation outcome, investigate with Read
access when available. A matching employee and scheme alone does not prove that
the call succeeded: multiple jobs are allowed. Explain unresolved uncertainty
and ask before another attempt. A clear validation rejection can be corrected.

If employee creation succeeds but employment creation fails, report the created
person and retain their ID. Do not recreate them on retry. A closing tax year,
an unconfigured scheme or incompatible NI category can block creation; explain
the returned error without changing other records to bypass it.

Return the new employment ID and its employee, scheme and schedule. Creation
does not enable billing, create a pay run, add the job to existing drafts or
submit anything to HMRC. For changes to an existing job, follow
[employment updates](employment-updates.md). For a received HMRC notice, use
[tax-code notices](tax-code-notices.md); do not replace starter evidence to apply it.
