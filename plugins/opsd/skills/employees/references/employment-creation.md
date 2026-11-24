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
- `start_date`: YYYY-MM-DD. New starters must start in 2026–27. A continuing employment can have an earlier start date. The
  scheme must be configured for 2026-27. Use the actual start date; do not move
  it into the supported year to bypass validation.
- `ni_category`: currently A, B, C, H, J, M, V, X or Z. Use the supplied category;
  the server checks compatibility with the employee. Do not substitute A for
  a missing or unsupported category.
- `student_loan` and `postgraduate_loan`: both require an explicit
  `not_applicable` declaration. Deductions are not yet supported; do not use
  `not_applicable` as a fallback when a loan applies or the answer is unknown.
- For a new job, supply `starter_information` using one of the forms below.
- For a continuing job, supply `payroll_import` with the exact payroll ID
  (preserve leading zeros), tax year, and date of the last payday included in
  the old software's accepted figures for this employment. Use the current
  tax code and basis. For cumulative PAYE, enter applicable earlier-job pay
  and tax separately. Enter this employment's gross pay, taxable pay, income
  tax, net pay, NI gross, employee and employer NI and the three NI earnings
  bands in integer pence. The import supports one NI category. If the old
  payroll reported other YTD items such as statutory pay, explain the limit.
- For a director already paid under AL this tax year, also record whether the
  appointment week was reported, whether an annual assessment was applied and
  all six NI figures before appointment. Take these from the old payroll.
- Opserver can take over for the first payday in a later UK tax month. If the
  old system already made a payment in the proposed payday's tax month, ask for
  the next eligible payday. A switch at the start of the tax year uses zero
  current-year balances. Use the person's existing record when available.

For ordinary NI, omit `ni_method`. For a director using the alternative method,
supply `"ni_method":{"method":"AL","appointed_on":"2026-10-01"}` with the actual
appointment date and a separate `ni_category` such as `A`. Select AL when
the director agrees, is paid regularly and normally earns more than the Lower
Earnings Limit for that pay period. An occasional low payment can still use AL.
Payments before the appointment use ordinary NI. The server checks the category
against age on payday. Under 16 requires X, M and Z require an age under 21,
and H requires an age under 25.
If the operator needs the standard annual method (`AN`), explain that it is
unsupported. If the connected tool lacks `ni_method`, report that limitation
before creating the employment.

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

Repeated new-starter calls create separate employments. An import preserves one payroll ID per PAYE scheme. After an uncertain outcome, look up the employment by scheme and payroll ID before retrying.
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
