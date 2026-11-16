# Finalize and submit through the browser

Use `create_payroll_run_submission_link` when the user intends to finalize and
submit a draft or reopened payroll run. Supply `business_id`, `payroll_run_id`
and the reviewed `expected_version`. Submit to HMRC (`hmrc:submit`) is required;
Read and Write are independent permissions. Known IDs and a reviewed version
can be used directly. With Read, use the payroll details, preview and history
tools to resolve the run and explain its current inputs and state. Never guess
a version or silently refresh it after a conflict.

The tool creates a link only. Show the returned URL to the user and explain that
they must sign in with the same Opsd account, review the selected payroll, enter
their HMRC credentials directly on the Opsd page and choose “Finalize and submit”.
Do not ask them to paste credentials into chat, pass them to tools, enter them
using browser automation or include them in notes. Opserver uses the password
for this operation without saving it. The HMRC user ID remains part of the
existing submission audit record. This flow does not set up stored HMRC
credentials or authorize later submissions.

The link expires after 15 minutes and is tied to that account, run and version.
Opening it does not submit anything. The browser shows the business, payment
date, included employment count and total saved gross pay; it is not a net-pay
or tax calculation preview. Finalization calculates payroll using the current
inputs and payroll history, following the same rules as the REST operation.

On confirmation, the server checks current business access, the reviewed account,
expiry, version and normal finalization rules. Business admins and payroll
operators, including practice members, may submit. Billing, payroll suspension,
scheme ordering, unresolved submissions and other existing guards still apply.
Explain failures without changing settings or payroll state to bypass them.

Starting finalization consumes the link atomically with creating the submission
attempt. Repeated confirmations cannot send it again. Failed preparation leaves
the link unused, but a changed run requires a fresh review and new link. A later
HMRC rejection does not make a consumed link reusable. Reopening and finalizing
creates a new revision; retrying resends the same frozen revision through a
separate browser confirmation. Follow [retry guidance](retry.md) when that is
the intended action. Reconciliation recovery is not yet available.

After confirmation, check the same run and its history when Read is granted.
With Submit alone, the user can use “Check status” on the browser page while the
link is valid. A used link shows its original attempt and frozen pay amounts,
even if someone later retries or reopens the run. Other tools show the current
run or its history; distinguish that from this particular submission. A network
error does not establish whether submission started:
check status before taking another action. Do not automatically create another
link, refresh the version or resubmit after an uncertain outcome. If an unused
link expires, a replacement still needs the same intended run and a valid,
reviewed version.

Report accepted, rejected, pending and uncertain outcomes accurately. Link
creation, finalization and an initial acknowledgement do not establish HMRC
acceptance. Background processing can continue after the browser response.
Acceptance does not mean employees or HMRC have been paid.
