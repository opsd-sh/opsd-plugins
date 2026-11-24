---
name: payroll
description: Create, edit or discard payroll drafts, reopen or cancel eligible runs, resume paused HMRC polling, preview calculations and inspect saved payments and submission history in Opsd. Arrange browser confirmation to submit or retry payroll, or resume reconciliation, with one-off HMRC credentials. Use for payroll preparation, submission and questions.
---

Use the Opsd connection and business selected by the user or established in the
conversation. If needed, resolve the business with the [business discovery skill](../businesses/SKILL.md),
including practice clients. Draft creation, edits, deletion, reopening,
cancellation, resuming polling and reconciliation links require `api:write`; the four read tools require `api:read`.
Write alone permits these operations when the required IDs and inputs are known.
Creating a submission or retry link requires `hmrc:submit`; it does not require Read or
Write when the business ID, run ID and reviewed version are already known.

For draft creation, read [draft creation guidance](references/draft-creation.md)
before calling `create_payroll_run`. It covers automatic employment inclusion,
copied payment defaults and uncertain outcomes. To change which employments are
included, read [inclusion and exclusion guidance](references/employment-inclusion.md)
before calling `include_payroll_run_employment` or `exclude_payroll_run_employment`.
For changes to gross pay, working-hours band or the final AL director payment decision, read
[payment editing guidance](references/payment-updates.md)
before calling `update_payroll_run_payment`. Use the employee skill for changes
to employment defaults instead.

To delete an entire draft, read [discard guidance](references/discard.md) before
calling `discard_payroll_run`. It requires the reviewed version and cannot delete
reopened or finalized runs.

To reopen a finalized run for corrections, read [reopening guidance](references/reopening.md)
before calling `reopen_payroll_run`. Reopening requires every submission attempt
to have been rejected or confirmed not sent; it does not submit anything to HMRC.

To stop an eligible finalized or reopened run, read [cancellation guidance](references/cancellation.md)
before calling `cancel_payroll_run`. It retains the run and its history and cannot
withdraw or undo an accepted HMRC submission.

To finalize and submit a draft or reopened run, read
[submission guidance](references/submission.md) before calling
`create_payroll_run_submission_link`. The user enters HMRC credentials and
confirms on the returned Opsd page. Never ask for or enter those credentials
in chat or tool calls. Creating or opening the link does not submit payroll.

To retry the same frozen revision after rejection or confirmation it was not sent,
read [retry guidance](references/retry.md) before calling
`create_payroll_run_retry_link`. The user reviews and confirms the retry in the
browser. Retry preserves the frozen inputs; use reopening for corrections.

To resume reconciliation of an uncertain submission, read
[reconciliation guidance](references/reconciliation.md) before calling
`create_payroll_run_reconciliation_link`. The user enters the original sender’s
password in the browser. This resumes checks on the same attempt without
sending payroll again. Write is required; Submit is not required.

To resume paused status checks for an existing submission, read
[polling recovery guidance](references/polling-recovery.md) before calling
`resume_payroll_run_polling`. It continues polling in the background without
creating or resending a submission.

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
contain gross amounts, working-hours bands and any `final_director_payment` decision. The calculation contains saved
amounts, calculation inputs, year-to-date figures and totals. These saved values
belong to the run's revision and must not be replaced with current employment
defaults. Money fields are integer pence; preserve negative tax amounts and
convert to pounds for presentation. Employer NI is separate from deductions
from employee pay. A null gross amount is unknown, not zero.

For AL directors, `inputs.annual_director_ni` identifies an annual assessment.
In each payment, `employee_ni_pence` is the employee NI assessed,
`employee_ni_deducted_pence` is the amount taken from pay (negative for a refund),
and `employer_funded_employee_ni_pence` is the shortfall covered by the employer.
Use the returned `net_pay_pence` for take-home pay. Before submission, show any
returned warnings about multiple paid jobs. The employer decides whether
separate NI calculations are appropriate and can continue after the warning.

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
Report the returned guidance and any `preparation_failure`. Finalization, retry
and reconciliation use browser confirmation; no payroll tool accepts HMRC
credentials.

Keep failures separate from empty results. A not-found error can mean a missing
or inaccessible business, or a run absent from the supplied business. Explain
which lookup failed and label any partial results. For insufficient scope, ask
the user to reconnect with the permission required by that operation: Write for
creation, edits, deletion, reopening, cancellation, resuming polling and
reconciliation links, or Read
for lookups and previews, or Submit to HMRC for submission or retry links.
For authentication failure, ask them to reconnect the same Opsd connection.
