# Reopen payroll for corrections

Use `reopen_payroll_run` when the user intends to edit an eligible finalized run.
Supply `business_id`, `payroll_run_id` and the reviewed `expected_version` from
the run's returned details. With Read permission, use `get_payroll_run` and
`get_payroll_run_history` to understand its current state and earlier attempts.
Use known IDs and versions directly; Write alone permits reopening. Do not guess
the version or request HMRC credentials.

The run must be `finalized`, and every submission attempt must be rejected or
confirmed not sent. A rejected latest attempt is not enough if an earlier
attempt remains unresolved. Pending, unknown and paused outcomes need their
appropriate recovery process; reopening cannot bypass them. Accepted runs cannot
be reopened or corrected with this tool. Draft, reopened and cancelled states
are also rejected. The run's `available_actions` can indicate reopening is
available, but the server rechecks eligibility and the version when called.

Business admins and payroll operators, including practice members, may reopen
runs. The payroll agreement must be active, no applicable business or practice
payroll suspension may be active, and no worker may currently own the run.
Explain any failure without changing billing or payroll state to bypass it.

Reopening preserves the run's saved payments and overrides rather than copying
current employment defaults. It retains frozen revisions and attempts, records
the user's decision and advances the version. Existing preparation failure
notices are marked resolved; this does not establish that the underlying
submission problem has been fixed. Reopening does not submit, retry, calculate
or undo anything at HMRC, and it does not remove an HMRC retry delay.

The response contains the resulting run details. Report its state and version.
For `status: reopened`, the response includes saved payment inputs and
`calculation: null`. The retained revision ID refers to history, not a fresh
calculation of the reopened inputs. Use
`preview_payroll_run` for a live preview when Read permission is available.
Follow the payment or inclusion guidance for requested edits. Reopened runs
cannot be discarded. Retrying would send the same frozen revision again;
reopening allows corrections before a later finalization creates a new revision.
To stop the reopened run instead, follow [cancellation guidance](cancellation.md).
Do not cancel it as an automatic response to an editing failure. To finalize
the corrected run, follow [submission guidance](submission.md). Retrying a
frozen revision is not yet available through these tools.

A version conflict requires reviewing the current state. Do not silently fetch
a new version and retry; establish that reopening still matches the user's
intended correction. After an uncertain outcome, inspect the same run and its
history when Read permission is available. A repeat call is rejected, including
when already reopened. Do not infer success from a conflict alone or automatically
repeat a later edit. A retry of an uncertain call must keep the same run ID and
original reviewed version.
