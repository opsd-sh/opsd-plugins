# Retry a rollover submission

Use `create_tax_year_rollover_retry_link` for an explicit request to retry the
current final FPS or new-year EPS of an existing rollover. The attempt must be
rejected or confirmed not sent, with a `retry` available action. Pending or
uncertain outcomes need status checks or reconciliation first. A preparation
failure without an EPS attempt does not qualify for this flow.

Require both Write and Submit. With Read, review the same rollover's current
version, stage, attempt outcome and saved decisions. Without Read, use established
business, scheme and rollover IDs and a reviewed version. The tool takes
`business_id`, `paye_scheme_id`, `rollover_id` and `expected_version`. Creating or
opening the link does not send anything to HMRC.

Explain what approval will do. Retrying the final FPS can automatically continue
to the new-year EPS once HMRC accepts the FPS. Retrying an EPS does not resend
the accepted FPS. EPS acceptance completes the rollover and applies the saved
next-year settings. Frozen payroll inputs, tax-code notices and the Employment
Allowance decision cannot be changed by the retry.

Present the returned URL as an Opsd confirmation link. It lasts fifteen minutes
and requires the same Opsd account that requested it. The user reviews the
business, scheme, years and stage, then enters HMRC credentials on Opsd. Never
ask for credentials in chat or tool arguments. A confirmed-unsent retry locks
the original HMRC user ID and preserves transaction identity; a rejection allows
credentials to be corrected and creates a new transaction ID. Normal access,
billing, version, worker-claim, retry-delay and unresolved-attempt checks apply.

Approval is consumed in the transaction that records the new retry attempt.
Preparation failure records a diagnostic without consuming approval or creating
an attempt; do not keep retrying unchanged invalid inputs. The receipt follows
only that retry attempt. Automatic EPS continuation or a later successful retry
does not turn an earlier rejection into success. Report the attempt's result
separately from overall rollover status; acknowledgement is not acceptance.

After expiry, conflict or an uncertain response, review the same rollover before
further action. Do not automatically resubmit credentials, refresh the version,
create another link or start a replacement rollover. Use the confirmation page's
status check without Read, or inspect progress and history with Read. A status
lookup alone does not authorize retrying.
