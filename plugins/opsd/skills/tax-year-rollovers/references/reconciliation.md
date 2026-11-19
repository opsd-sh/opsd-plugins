# Recover a rollover submission in the browser

Use `create_tax_year_rollover_reconciliation_link` when the user asks to recover
an uncertain final FPS or new-year EPS submission using Government Gateway
credentials. It requires both Write and Submit permissions. With Read, inspect
`get_tax_year_rollover` and its history first. Without Read, use established IDs
and a reviewed version. A status question alone does not authorize recovery.

Explain the continuation before creating the link: recovering the final FPS can
automatically send the new-year EPS using the saved Employment Allowance decision.
EPS acceptance completes the rollover and applies its saved next-year settings.
The confirmation page explains this too. This flow resumes the reviewed attempt;
it does not resend that attempt, but FPS recovery can create the EPS attempt.

The reviewed attempt must be `credentials_required`, `reconciliation_paused` or
`needs_attention`. `resume_reconciliation` in `available_actions` is a state hint,
not user approval or OAuth permission. Active processing, an inactive payroll
agreement or payroll suspension blocks recovery. Do not use this for a rejected
or confirmed not-sent attempt, paused polling, or an EPS awaiting dispatch.

Call with `business_id`, `paye_scheme_id`, the exact `rollover_id` and reviewed
`expected_version`. Link creation does not contact HMRC or change rollover state.
Present the returned URL as an Opsd confirmation link. It expires after fifteen
minutes and requires the same Opsd account that requested it. The browser shows
the business, scheme, years, saved allowance decision, stage and attempt. The
original sender ID is fixed; the user enters the password on Opsd. Never request,
accept or pass Government Gateway credentials through chat or tool arguments.

Approval is consumed once, atomically with resuming recovery. Existing roles,
billing checks, version guards and HMRC retry delays still apply. The returned
receipt follows the reviewed attempt even if the rollover moves to another
attempt. Check overall rollover status separately: accepted FPS does not mean
the rollover is complete. With Read, inspect the same rollover to report later
progress; without it, direct the user to the confirmation page's status check.

If approval expires, the version changes or the response is uncertain, review
the same rollover before requesting another link. Do not silently refresh the
version, switch to a replacement rollover or retry. A later pause of the same
attempt needs a fresh review and link. This tool does not retry a submission; use the [retry flow](retry.md) only
after rejection or confirmed non-transmission.
For an accepted final FPS waiting for credentials to send its EPS, use the
separate [EPS submission flow](send-eps.md).
