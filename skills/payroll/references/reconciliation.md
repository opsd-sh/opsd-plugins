# Resume payroll reconciliation

Use `create_payroll_run_reconciliation_link` to resume checking HMRC for an
existing submission whose outcome is uncertain. It supports `credentials_required`,
`reconciliation_paused` and `needs_attention` on a finalized run. It does not
resend payroll or create another attempt. For `polling_paused`, follow
[polling recovery guidance](polling-recovery.md).

Supply the business ID, run ID and reviewed `expected_version`. Write
(`api:write`) is required; Read and Submit are independent. With Read, inspect
the current run and history first. Known IDs and a reviewed version can be
used directly. Do not guess or silently refresh a version after a conflict.

Show the returned 15-minute link to the user. They must sign in with the same
Opsd account and enter the password for the original HMRC user ID shown on the
page. Never request credentials in chat, pass them to tools or enter them
through browser automation. The password is used for this recovery without
being saved; it does not authorize future submissions.

Confirmation rechecks business access. The worker checks the version, pause,
payroll agreement, suspension, ownership and saved HMRC destination. It retains
the frozen revision and attempt identity, honours the saved HMRC delay, and
consumes the link atomically when recovery resumes. Report failures without
changing payroll or billing settings to bypass a guard.

The receipt follows the existing attempt, including any later pause or recovery
of that attempt. Resumption does not establish acceptance. With Read, inspect
the run and history; otherwise the user can check status on the browser page
while the link is valid. After an uncertain response, check status before any
further action. Do not automatically create a replacement link or resubmit.
A consumed link cannot resume another pause: review the new state and version
before requesting a fresh link. A later submission attempt has its own receipt.
