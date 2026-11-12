---
name: payroll
description: Find payroll runs in an Opsd business, preview draft calculations and inspect saved payments and submission history. Use for read-only payroll questions, not creating, editing, finalizing or submitting payroll.
---

Use the Opsd connection and business selected by the user or established in the
conversation. If needed, resolve the business with the [business discovery skill](../businesses/SKILL.md),
including practice clients. All four payroll tools require `api:read`.

- Call `list_payroll_runs` with only `business_id` to find runs. Filter the
  returned records locally by payment date, status, PAYE scheme or pay schedule.
  The tool has no filter arguments. Listing order is creation order, so do not
  assume the last listed run has the latest payment date.
- Call `get_payroll_run` with `business_id` and `payroll_run_id` for one run's
  included employments, saved payments and any saved calculation. A known run
  ID can go directly to this tool without listing first.
- Call `preview_payroll_run` with `business_id` and `payroll_run_id` when asked
  to calculate a draft or reopened run. It uses the current draft payments,
  employment tax settings and accepted payroll history in one snapshot. It
  returns a live calculation without saving results or sending anything to HMRC.
- Call `get_payroll_run_history` with the same IDs for retained revisions,
  submission attempts, outcomes, recovery actions and preparation failures.
  Use this to explain what happened, including after reopening or cancellation.

Use the [payroll setup skill](../payroll-setup/SKILL.md) to resolve scheme and
schedule names and match their IDs. If several runs fit the request, show their
payment dates, schedules, statuses and IDs and ask which to use. To attach names
to employment IDs, use the [employee discovery skill](../employees/SKILL.md).
`employment_count` counts included employments, not necessarily distinct people.

Distinguish saved payment inputs from calculated results. The run's payments
contain gross amounts and working-hours bands; `calculation` contains saved
amounts, calculation inputs, year-to-date figures and totals. These saved values
belong to the run's revision and must not be replaced with current employment
defaults. Money fields are integer pence; preserve negative tax amounts and
convert to pounds for presentation. Employer NI is separate from deductions
from employee pay. A null gross amount is unknown, not zero.

A null `calculation` means this response has no saved calculation. In particular,
reading a draft or reopened run with `get_payroll_run` does not calculate a
preview. Use `preview_payroll_run` for that, and label its results as a preview.
A later preview can differ after inputs or payroll history change. It does not
establish that payroll has been finalized, submitted or accepted. If calculation
fails, explain the returned problem; do not substitute zeroes or partial totals.
Finalized, accepted and cancelled runs cannot be previewed. Use their saved
details and history instead.

A reopened or cancelled run may still have older revisions. History groups
attempts, actions and preparation failures under their revision; match IDs to
`current_revision_id` and `current_attempt_id` rather than merging all attempts
into one current status. A retry makes another attempt for the same frozen
revision; finalizing reopened payroll creates a new revision. History does not
return historical payment calculations, and an empty revision list does not
mean a draft has no payment inputs.

Use the top-level `status` to distinguish draft, reopened, cancelled, finalized
and accepted runs. For a finalized run, inspect `submission.status` and its
public message or rejection reason. Finalization and an attempt's `recorded_at`
do not establish HMRC acceptance. In history, an initial acknowledgement is
not acceptance: inspect the attempt status and business outcome. Cleanup is
separate from HMRC's decision. An accepted submission does not establish that
employees or HMRC have been paid.

`available_actions` describes recovery options for the run's current state; it
does not grant OAuth permissions or mean the connected tools can execute them.
Report the returned guidance and any `preparation_failure`. These tools only
read data, so do not request HMRC credentials or attempt a recovery action.

Keep failures separate from empty results. A not-found error can mean a missing
or inaccessible business, or a run absent from the supplied business. Explain
which lookup failed and label any partial results. For insufficient scope, ask
the user to reconnect with Read permission; for authentication failure, ask them
to reconnect the same Opsd connection.
