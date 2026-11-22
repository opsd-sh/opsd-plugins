# Create a payroll draft

Use `create_payroll_run` when the user asks to create a draft. Supply all four
arguments: `business_id`, `paye_scheme_id`, `pay_schedule_id` and `payment_date`.
The scheme must belong to the business and the schedule to that scheme. Use
known IDs directly; resolve ambiguous names with the payroll setup tools when
Read permission is available. Business admins and payroll operators, including
practice members, can create drafts.

Use the actual payment date established by the user, in `YYYY-MM-DD` format.
Do not default it to today or move it to bypass a validation failure. Creation
currently supports 6 April 2026 through 5 April 2027, and the PAYE scheme must
have that tax year open. Payroll must already be enabled for the business.
Do not enable billing or change the agreement as a side effect of this request.

The tool includes the schedule's employments whose start dates are on or before
the payment date. Future starters are excluded; an unknown start date blocks
creation. Inclusion is per employment, so one person may appear more than once.
Creation has no argument for choosing a subset of employments. For a requested
subset, create the draft and then follow the [inclusion and exclusion guidance](employment-inclusion.md).
Do not change employment records to control inclusion. These are separate
operations: report any failed adjustment rather than claiming the requested
subset is ready.

Creation copies each included employment's current gross pay and working-hours
defaults into the run's payments. Later changes to those defaults do not rewrite
the draft's saved payments. Tax settings are still live when previewing; they
are not frozen by creating a draft. A successful creation is not a complete
payroll-readiness check, and an empty schedule can produce an empty draft.
For a requested override to an included payment, follow the
[payment editing guidance](payment-updates.md).

A new draft starts with the final director payment decision unanswered. For a
regular AL payday before tax month 12, establish the operator’s decision when
annual reassessment has yet to start. A £0 entry can still require an adjustment
or FPS reporting. Keep it in the draft unless exclusion is appropriate.

Report the returned run ID, payment date, draft status and employment count.
The response is a summary, not a calculation. Use `get_payroll_run` for saved
payments or `preview_payroll_run` for a calculation when needed for the user's
request and Read permission is available. Creating the draft does not calculate,
finalize, submit to HMRC or establish that employees have been paid.

Each successful call creates a new draft, even for the same schedule and date.
Do not retry automatically after a timeout or other uncertain outcome. With
Read permission, use `list_payroll_runs` and `get_payroll_run` to investigate.
A matching date alone does not identify this attempt. If the outcome remains
uncertain, explain the possible duplicate and ask before creating another draft.

For a rejected request, explain the returned problem. Creation is blocked by an
absent or cancelled payroll agreement, a mismatched active tax year, an unfinished
tax-year rollover, or a finalized, accepted or reopened run on the same schedule
with the same or a later payment date. Do not change the date, schedule, agreement
or existing payroll to bypass those restrictions.
