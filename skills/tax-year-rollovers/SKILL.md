---
name: tax-year-rollovers
description: Find a PAYE scheme's tax-year rollovers and inspect final FPS and new-year EPS progress, submission attempts and recovery history. Use for year-end status questions, cancelling an eligible rollover or resuming paused status polling. Use browser approval to start a rollover with explicit allowance and tax-code decisions, recover an uncertain submission, retry a rejected or confirmed-unsent attempt, or send the new-year EPS after final FPS acceptance.
---

Use the Opsd connection and business selected by the user or established in the
conversation. Resolve an unclear business with the [business discovery skill](../businesses/SKILL.md),
including practice clients, and select its PAYE scheme with the [payroll setup skill](../payroll-setup/SKILL.md).
The three lookup tools require `api:read`. Cancellation requires `api:write`,
independently of Read or Submit. Resuming polling and creating start, reconciliation, retry or EPS submission links require
both `api:write` and `hmrc:submit`, matching the REST rollover actions. These actions do not require
Read when the IDs and reviewed version (or scheme generation for a new start)
are already known.

- Call `list_tax_year_rollovers` with `business_id` and `paye_scheme_id` to find
  rollovers. It includes completed and cancelled records, newest created first.
  Filter locally by source year, destination year or status; the tool has no
  filter arguments. A tax-year start of 2026 means 2026-27.
- Call `get_tax_year_rollover` with those IDs and `rollover_id` for current
  progress, recorded decisions and available actions. A known rollover ID can
  go directly to this tool when its business and scheme are established.
- Call `get_tax_year_rollover_history` with the same three IDs for attempts,
  outcomes, recorded actions and preparation failures grouped under `final_fps`
  and `new_year_eps`.

For an explicit request to start a new rollover, follow [starting a rollover](references/start.md)
and call `create_tax_year_rollover_submission_link`. Review the source year,
scheme generation, destination-year Employment Allowance choice and HMRC coding
notices before creating the link. Do not infer those decisions from a status request.

For an explicit request to cancel, follow [cancellation](references/cancellation.md)
and call `cancel_tax_year_rollover`. A status lookup does not authorize cancellation.
For paused status polling, follow [polling recovery](references/polling-recovery.md)
and call `resume_tax_year_rollover_polling`. For recovery requiring credentials,
follow [browser reconciliation](references/reconciliation.md) and call
`create_tax_year_rollover_reconciliation_link`. Confirming FPS reconciliation can
automatically send the new-year EPS and complete the rollover. When the final FPS
is accepted and the rollover is waiting for credentials to send the EPS, follow
[EPS submission](references/send-eps.md) and call
`create_tax_year_rollover_eps_submission_link`. For an explicit request to retry
a rejected or confirmed not-sent attempt, follow [submission retry](references/retry.md)
and call `create_tax_year_rollover_retry_link`.

A scheme retains rollovers across tax years and can have cancelled replacements
for the same transition. Only one rollover can be active at a time. Match the
requested years and status; do not assume the first listed record is active.
If several records fit, identify them by years, status and ID before selecting.
Retrying a submission adds an attempt to the same rollover; starting again after
cancellation creates another rollover ID. Keep their histories separate.

Use top-level `status` to distinguish `in_progress`, `cancelled` and `complete`.
For an operation in progress, inspect `progress.phase` and the nested submission:
`final_fps` closes the source year; `new_year_eps` reports the destination year's
Employment Allowance decision. Final FPS acceptance alone does not establish
that the rollover is complete. Before EPS dispatch, its status can be
`awaiting_dispatch`, `preparation_failed` or `credentials_required_to_send`;
these do not have an EPS attempt ID. Do not invent one or describe an unsent EPS
as rejected. A completed response has accepted `final_fps` and `eps` summaries.

In history, distinguish initial acknowledgement from the business outcome.
An attempt's `recorded_at` marks its creation, not acceptance. Cleanup is
separate from HMRC's decision, and acceptance does not establish payment.
Use stage names and attempt IDs to link outcomes and recovery actions. An empty
EPS attempt list means no EPS attempt is recorded for that rollover, not that
the whole rollover is absent or complete.

The allowance choice and tax-code notices are saved rollover decisions, not a
fresh eligibility assessment or the current employment settings. Report public
messages and preparation failures. `available_actions` describes state-dependent
options; it does not grant OAuth permissions. Lookup tools read saved state
without contacting HMRC. Do not request Government Gateway credentials or carry
out recovery actions for a status lookup.

Keep failed lookups distinct from empty lists and label partial results. A
not-found error can mean a missing or inaccessible business, or mismatched
scheme and rollover IDs. For insufficient scope, ask the user to reconnect with
Read permission for lookups, Write for cancellation, or both Write and Submit for
starting a rollover, polling recovery, reconciliation, retry or EPS submission links. For authentication failure, reconnect
the same Opsd connection.
