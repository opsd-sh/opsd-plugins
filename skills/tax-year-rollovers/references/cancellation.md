# Cancel a tax-year rollover

Use `cancel_tax_year_rollover` only when the user asks to cancel a specific
rollover. Confirm the business, PAYE scheme and source and destination tax years.
With Read permission, use `get_tax_year_rollover` and, if needed, its history to
review the named rollover. With Write alone, proceed only when its IDs and
reviewed version are already established; do not require Read or Submit.

Cancellation is available while the final FPS has only rejected or confirmed
not-sent attempts, before any accepted final FPS or EPS attempt. Uncertain HMRC
outcomes cannot be cancelled. An active worker claim, an inactive payroll
agreement or a payroll suspension also blocks cancellation. `available_actions`
is a state hint, not permission or user approval to act.

Explain that cancellation keeps the scheme in its source tax year and allows
ordinary payroll there again. It retains submission history and frozen rollover
decisions. It does not undo an accepted submission, delete payroll records or
end the payroll agreement. No HMRC credentials or browser handoff are needed.

Call with `business_id`, `paye_scheme_id`, the exact `rollover_id` and its reviewed
`expected_version`. On a version conflict, review the changed state with the user;
do not silently fetch a newer version and repeat the cancellation.

A successful response has `status: cancelled`. Repeating the same request returns
the same retained record without adding another cancellation decision, including
after a replacement rollover has started. Normal access and billing guards still
apply. For an uncertain response, check that exact rollover with Read permission
or repeat the original request unchanged. Never substitute a replacement ID.
Report a failed cancellation distinctly from a cancelled rollover.
