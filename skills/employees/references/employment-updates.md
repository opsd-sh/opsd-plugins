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

The server merges partial edits with the stored employment. A change to the
start date or starter evidence resolves initial tax treatment again using that
merged evidence. Report the returned treatment; do not set a tax code directly
or use starter corrections to apply an HMRC notice. Applying notices through
MCP is not yet supported.

A closing tax year blocks edits. Actual start-date, starter-evidence and NI
category changes are blocked after the employment appears in finalized payroll.
An applied HMRC notice also blocks start-date and starter-evidence changes.
A new start date cannot be later than the payment date of an existing draft or
reopened run containing the job. Explain conflicts without changing other
records to bypass them. Pay and hours can still be edited after finalized
payroll; saved payroll results are retained.

This tool cannot change the linked employee, PAYE scheme, schedule or loan
declarations. It does not finalize payroll or submit to HMRC. Return the
employment ID and the changed settings, distinguishing updated defaults from
amounts already recorded in payroll runs.
