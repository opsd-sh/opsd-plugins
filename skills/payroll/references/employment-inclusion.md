# Include or exclude an employment

Use `include_payroll_run_employment` or `exclude_payroll_run_employment` when the
user asks to change which employments are included in a draft or reopened run.
Supply `business_id`, `payroll_run_id` and `employment_id`. There is no payment
amount, bulk-ID list or `expected_version` argument.

Use known IDs directly. To resolve names or check current inclusion with Read
permission, use `get_payroll_run` and the employee discovery tools. One person
can have multiple employments, so select the employment rather than substituting
an employee ID or assuming that a person's name identifies one payment. Write
permission alone is sufficient when the IDs and intended change are known.

- Inclusion adds the employment if absent, copying its current gross-pay and
  normal-weekly-hours defaults into a new payment. If already included, it
  preserves the existing payment and its overrides.
- Exclusion removes this run's payment, including any pay and hours overrides.
  It preserves the employment record, other runs and frozen revisions. If the
  employment is already absent, there is no payment to remove.

Exclusion followed by inclusion does not restore the old payment. It creates a
new payment from the employment's current defaults. For example, if a £3,000
default was overridden to £3,200 for this run, removing and re-including it
restores £3,000 only if that is still the current default. Use
`update_payroll_run_payment` for a requested payment change; do not use an
exclude/include cycle merely to edit an amount. A copied null gross amount
remains unknown, not zero or proof that payroll is ready.

Both tools require an active payroll agreement and an employment belonging to
the run's business, PAYE scheme and current pay schedule. Business admins and
payroll operators, including practice members, can use them. Inclusion also
requires a known start date on or before payment and a payment date within the
supported 6 April 2026–5 April 2027 tax year. Exclusion does not apply those date
checks, so incomplete or future employment data can still be removed from a
run. Finalized, accepted and cancelled runs cannot be edited.

Successful responses have empty content. Report the inclusion or exclusion as
completed; use `get_payroll_run` for the resulting payments and count, or
`preview_payroll_run` for a fresh calculation, when useful and Read permission
is available. Removing the last employment leaves an empty run; it does not
discard the run or end anyone's employment. Neither tool calculates, finalizes,
submits to HMRC or establishes that anyone has been paid.

Every successful call advances the run version, including calls that find the
employment already included or absent. Do not automatically replay an uncertain
outcome. Check current inclusion when possible; if the outcome or intended state
remains unclear, explain that and ask before retrying. Use a freshly read version
for future actions that require one.

Each call changes one employment in one transaction. For a requested set of
changes, apply only those changes and report which succeeded if a later call
fails. Do not claim that the entire set was updated or silently undo successful
changes. Explain returned failures without changing the agreement, start dates,
schedule or payroll state to bypass them.
