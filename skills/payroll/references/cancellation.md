# Cancel a payroll run

Use `cancel_payroll_run` when the user intends to stop an eligible finalized or
reopened run while retaining its records. For an ordinary draft, follow
[discard guidance](discard.md) instead. To correct a finalized run, follow
[reopening guidance](reopening.md). Cancellation does not withdraw a submission
from HMRC, undo accepted payroll, reverse employee payments, end employment or
cancel the payroll agreement.

Supply `business_id`, `payroll_run_id` and the reviewed `expected_version` from
the run's returned details. With Read permission, use `get_payroll_run` and
`get_payroll_run_history` to resolve the intended run and understand its state.
Write alone permits cancellation when the exact run and reviewed version are
known. Do not guess a version or request HMRC credentials.

The run must be `finalized` or `reopened`, and every submission attempt must be
rejected or confirmed not sent. A rejected latest attempt does not make earlier
uncertainty safe. Pending, unknown and paused outcomes need their appropriate
recovery process. Draft, accepted and already cancelled runs are rejected.
`available_actions` can indicate cancellation is available, but the server
rechecks eligibility and the version when called.

Business admins and payroll operators, including practice members, may cancel
runs. The payroll agreement must be active, no applicable business or practice
payroll suspension may be active, and no worker may currently own the run.
Explain failures without changing billing or payroll state to bypass them.

Cancellation records the user's decision and advances the run version. It
retains saved payment inputs, frozen revisions, calculations and submission
attempts. Existing preparation failure notices are marked resolved. Unsent edits
made while reopened remain stored, but the cancelled response's payment inputs
and employment count describe the last frozen revision, not those edits.
`calculation` is null in the response; this does not mean history was deleted.
Do not report the unsent corrections as finalized or submitted.

Report the returned state and version. A cancelled run cannot be edited,
reopened, previewed or discarded. It remains readable along with its history.
Do not automatically create a replacement run or treat cancellation as undo for
a failed edit. This action sends nothing to HMRC; any existing response cleanup
continues independently and does not withdraw a submission.

A version conflict requires reviewing the current state. Do not silently fetch
a new version and retry; establish that cancellation still matches the user's
intent. After an uncertain outcome, inspect the same run and its history when
Read permission is available. A repeat call returns a conflict, including when
already cancelled, so a conflict alone does not prove the first call succeeded.
A retry of an uncertain call must keep the same run ID and original reviewed version.
