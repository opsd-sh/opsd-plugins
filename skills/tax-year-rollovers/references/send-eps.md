# Send the new-year EPS after final FPS acceptance

Use `create_tax_year_rollover_eps_submission_link` for an explicit request to
continue a rollover whose final FPS is accepted and whose EPS status is
`credentials_required_to_send`. The `send_eps` available action describes this
state; it is not OAuth permission or approval. Do not use this flow for an EPS
attempt that is rejected, confirmed not sent, pending or uncertain, or for an
EPS preparation failure. Those need the appropriate retry or recovery action.

The tool requires both Write and Submit permissions. With Read, review the
rollover and its saved Employment Allowance decision. Without Read, use
established business, scheme and rollover IDs and a reviewed version. Explain
that approval sends the new-year EPS, without resending the final FPS. EPS
acceptance completes the rollover and applies the saved next-year settings.

Call with `business_id`, `paye_scheme_id`, `rollover_id` and `expected_version`.
Link creation does not contact HMRC or change rollover state. Present the URL
as an Opsd confirmation link. It expires after fifteen minutes and requires
the same Opsd account that requested it. The page shows the business, PAYE
scheme, years and saved allowance decision. The user enters their HMRC user
ID and password on Opsd; never ask for credentials in chat or tool arguments.
The saved rollover decisions cannot be changed through the link.

Approval is consumed once when dispatch resumes. Normal access, billing,
state, version and worker-claim checks apply. A consumed approval can initially
have no EPS attempt while preparation runs. Preparation can fail or stop
without creating an attempt; that is not a rejection or permission to retry.
Use the page's status check, or inspect the same rollover with Read permission.

The receipt retains only the attempt created by that approval. If preparation
stopped without an attempt, a later approval's EPS does not become its receipt.
Report the attempt's outcome separately from overall rollover status: a later
successful retry does not change an earlier rejection. Acknowledgement alone
does not establish HMRC acceptance or completion.

On expiry, conflict or an uncertain response, review the same rollover before
further action. Do not silently refresh the version, create another link,
resubmit credentials or choose a replacement rollover. Use the separate
[retry flow](retry.md) for an eligible failed EPS attempt. Starting a rollover
is not yet supported.
