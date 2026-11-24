# Employment updates

Use `update_employment` for requested changes to an existing job's payroll
settings. It requires `api:write` and is available to business admins and payroll
operators, including practice members. Known business and employment IDs need
no preliminary Read lookup. Use the employment ID, not the employee ID; a person
can have several jobs, so resolve ambiguity before editing.

Send only the requested fields, with `business_id` and `employment_id`:

- `monthly_gross_pay_pence`: the monthly default in integer pence, from zero to
  `99999999999`. This changes the default used when adding the employment to a
  pay run; it does not replace pay amounts already stored in a run.
- `normal_weekly_hours_band`: the normal working pattern using `less_than_16`,
  `sixteen_to_less_than_24`, `twenty_four_to_less_than_30`, `thirty_or_more` or
  `other`. `other` means no normal pattern, not missing information. Like pay,
  this is a default; existing run entries retain their stored hours band.
- `ni_category`: the supplied category, currently A, B, C, H, J, M, V, X or Z.
  The server checks compatibility and payroll history; do not guess a category.
- `ni_method`: for AL, supply `{"method":"AL","appointed_on":"2026-10-01"}`
  with the actual appointment date. Check the director’s agreement, regular pay
  pattern and usual pay above the Lower Earnings Limit for that period.
  Use `{"method":"ordinary"}` for an explicit change to ordinary NI. Omission
  keeps the current method. The server rejects changes that would alter
  finalised payroll. NI category is a separate setting.
- `start_date`: the actual date in YYYY-MM-DD, currently from 2026-04-06 through
  2027-04-05. Do not move the date to bypass validation.
- `starter_information`: a complete replacement of the evidence object, using
  the P45, checklist or explicit `not_provided` forms in
  [employment onboarding](employment-creation.md). Do not infer missing evidence
  or substitute `not_provided` for an unanswered question.

Omission preserves every field. Null also preserves pay, start date, NI category
and starter information; it never clears them. Null is invalid for the hours
band. At least one non-null setting is required. Repeating the same values is
allowed, subject to the current payroll protections.

Before the first finalised payment for a local starter, changing the start
date or starter evidence updates the initial PAYE settings. If an HMRC notice
has been applied, send only `start_date` to correct the date. Opserver validates
it against the retained evidence and preserves the notice’s tax code, basis and
previous-employment figures. The starter evidence is locked. For a received
notice, use `apply_employment_tax_code_notice` following [tax-code notices](tax-code-notices.md).

A closing tax year blocks edits. Once the employment has appeared in any finalised
payroll, its start date and starter evidence are locked, including after reopening.
An imported employment retains its original start date. A new start date cannot
be later than the payday of a draft containing the employment.

If HMRC rejected the first FPS for this employment or Opsd confirmed it was
never sent, the operator can reopen the run and correct the NI category. The
next preview and finalisation use the corrected letter. A finalised or accepted
payment in another run for this employment, or its imported payroll history,
still blocks the correction. Explain conflicts without changing other records to
bypass them. Pay and hours remain editable for future drafts, and saved payroll
results retain their original values.

This tool cannot change the linked employee, PAYE scheme, schedule or loan
declarations. It does not finalize payroll or submit to HMRC. Return the
employment ID and the changed settings, distinguishing updated defaults from
amounts already recorded in payroll runs.

## Correcting a payroll import

Use `get_employment_payroll_import` to read the saved external ID, last payday
and opening figures. To amend them, call `amend_employment_payroll_import` with
the business ID, employment ID and a `changes` object. For an ID typo, send
only the corrected string, for example `{"payroll_id":"00024"}`. For an NI
correction, supply the complete `ni` block. Supply `director_history` together
with a payday correction if that payday changes the director history required.
A conflict identifies the employment that holds the ID or the payroll run
that froze the import. Existing drafts use the corrected figures at their next
preview and finalisation.
