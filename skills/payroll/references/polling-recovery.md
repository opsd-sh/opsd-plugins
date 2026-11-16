# Resume paused payroll polling

Use `resume_payroll_run_polling` when the user wants Opsd to resume checking
HMRC for an existing submission's outcome. It handles `polling_paused` on a
`finalized` run. It does not finalize payroll, create a new transmission attempt,
resend a submission or resume reconciliation. Do not request HMRC credentials.

Supply `business_id`, `payroll_run_id` and the reviewed `expected_version` from
the run's returned details. With Read permission, use `get_payroll_run` and
`get_payroll_run_history` to identify the run and its current attempt. Write
alone permits resuming when the exact run and reviewed version are known.
`available_actions` may offer `resume_polling`; the server rechecks the state,
version and access when called.

Business admins and payroll operators, including practice members, may resume
polling. The payroll agreement must be active, no applicable business or
practice payroll suspension may be active, and no worker may currently own
the run. Explain failures without changing billing or payroll state to bypass
them. For other pause states, follow
[reconciliation guidance](reconciliation.md).

The action records the user's decision, advances the run version and resumes
the same attempt in the managed background worker. It retains the revision,
payment inputs and saved calculation, and honours the saved HMRC delay.
Returning `pending` means polling has resumed, not that HMRC has accepted the
submission. The worker continues after the tool response and can subsequently
record acceptance, rejection or another pause. Normal acceptance processing
still applies; this action does not make payments to employees or HMRC.

Report the returned state and version. With Read permission, check the same run
later using `get_payroll_run`, and use history to explain its outcome. Do not
repeatedly call the resume tool to check progress or bypass a delay. Without
Read permission, explain that the result confirms resumption and that checking
later progress requires Read or the webapp.

After a conflict or uncertain result, inspect the same run and its history
when Read is available. A conflict does not prove that an earlier call succeeded.
Do not silently fetch a newer version and resume again: another pause needs a
fresh review. Any retry of an uncertain call must use the same run ID and
original reviewed version, which can authorize the transition only once.
