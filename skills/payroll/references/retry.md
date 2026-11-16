# Retry a frozen payroll submission

Use `create_payroll_run_retry_link` when the user intends to resend the same
frozen payroll revision. Supply `business_id`, `payroll_run_id` and the reviewed
`expected_version`. Submit to HMRC (`hmrc:submit`) is required; Read and Write
are independent. Known IDs and a reviewed version can be used directly. With
Read, inspect the run and its history first. Never guess or silently refresh
a version after a conflict.

The run must be finalized and every previous attempt must be rejected or
confirmed not sent. A rejected latest attempt does not make an older uncertain
attempt safe to resend. Pending, unknown and paused outcomes need the relevant
recovery operation. Accepted, cancelled, draft and reopened runs cannot be
retried. The existing worker rechecks the version, membership, payroll agreement,
suspension, ownership, HMRC retry delay and saved submission environment.

Show the returned link to the user. They must sign in with the same Opsd account,
review the retry and enter credentials directly in the browser. Never request
credentials in chat, pass them to tools or enter them through browser automation.
The page says “Retry submission” and shows the frozen payment summary. It cannot
change payroll inputs or the late reporting reason. For corrections, follow
[reopening guidance](reopening.md) instead of retrying.

For an attempt confirmed not sent, the original HMRC user ID is required and
the existing transaction ID is reused. After rejection, a retry uses a new
transaction ID. Both create a new recorded attempt for the same frozen revision.
The password is used for this operation without being saved; this does not
authorize future submissions or set up stored credentials.

The link expires after 15 minutes and is consumed atomically with the new
attempt. Failed preparation leaves it unused; a later rejection does not make
it reusable. A consumed link always reports its own attempt and frozen payment
summary, even after another retry or reopening. Current-run tools may show a
later attempt, so distinguish their results from this receipt.

Creating or opening a link does not submit payroll or establish acceptance.
After an uncertain response, check the link's status or the run and history
with Read permission. Do not automatically create a replacement link, update
the version or retry again. Follow the returned error or recovery guidance
without changing payroll or billing settings to bypass a guard.
