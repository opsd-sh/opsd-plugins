# Resume rollover status polling

Use `resume_tax_year_rollover_polling` when the user asks to resume paused HMRC
status checks for a specific tax-year rollover. It requires both Write and Submit
permissions. With Read, use `get_tax_year_rollover` to review the current stage,
attempt and version. Without Read, use established IDs and a reviewed version.
A status question alone does not authorize recovery.

Only `polling_paused` on the final FPS or new-year EPS can be resumed this way.
`resume_polling` in `available_actions` is a state hint, not OAuth permission or
user approval. An active worker claim, inactive payroll agreement or payroll
suspension blocks the action. Do not use it for rejected, confirmed not-sent or
uncertain submissions, reconciliation pauses, or an EPS awaiting dispatch.

Call with `business_id`, `paye_scheme_id`, the exact `rollover_id` and reviewed
`expected_version`. It resumes the same attempt in the background and respects
HMRC's saved retry delay. It does not create or resend a submission, change the
saved rollover decisions or require Government Gateway credentials.

The response normally shows `pending`; that is not acceptance or completion.
With Read, check the same rollover later to report progress. Final FPS acceptance
can leave the rollover waiting for credentials to send the new-year EPS; use
the [EPS submission flow](send-eps.md) for an explicit request to continue. EPS
acceptance completes the rollover and applies its saved next-year settings.
Do not claim the source tax year has advanced on final FPS acceptance alone.

An old request cannot resume a later pause. On a version conflict or uncertain
response, check the same rollover if Read is available; otherwise report that
its current state needs review. Do not silently refresh the version, target a
replacement rollover or repeatedly resume a fresh pause. Do not ask for HMRC
credentials in chat. For a reconciliation pause, follow the separate
[browser reconciliation flow](reconciliation.md).
