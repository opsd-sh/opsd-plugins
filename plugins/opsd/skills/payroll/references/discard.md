# Discard a payroll draft

Use `discard_payroll_run` when the user intends to delete an entire ordinary
draft. It permanently removes the run and all its saved payments and overrides.
Use `exclude_payroll_run_employment` to remove only one employment, or
`update_payroll_run_payment` to change an amount. Discarding preserves employee
and employment records, other runs and their history, and the payroll agreement.
It does not cancel a submitted run or undo anything at HMRC.

Supply `business_id`, `payroll_run_id` and `expected_version`. Use the version
of the draft reviewed for deletion, returned by creation, listing or
`get_payroll_run`; never guess it, assume zero or increment a previous version.
With Read permission, use the existing discovery tools to resolve an ambiguous
run and show its payment date, scheme/schedule, status and included employments
as needed to establish the intended deletion. Write alone is sufficient when
the exact run and its reviewed version are already known. If the version is
missing and Read is unavailable, ask for it or reconnection with Read permission.

Only `draft` runs can be discarded, including empty drafts. Reopened runs cannot
be discarded because they retain history; finalized, accepted and cancelled runs
are also rejected. Business admins and payroll operators, including practice
members, can discard drafts, and the payroll agreement must still be active.
Do not change the agreement or payroll state to bypass a failure.

A version conflict means the run changed since the supplied version. Explain
the conflict and, with Read permission, fetch its current details for review.
Do not silently substitute the latest version and repeat the deletion: establish
that the user still intends to discard the changed run first. Payment edits and
inclusion/exclusion advance the version even when payment values are unchanged.

A successful response has empty content and means the draft was deleted. Report
the selected run as discarded; do not claim that employees were removed or that
payroll was cancelled with HMRC. There is no undo tool. Do not create a replacement
as an automatic follow-up or as compensation for another operation's failure.

After an uncertain outcome, check the same run ID when Read permission is
available. A repeated call after deletion returns not found rather than another
success; not found can also mean the run is inaccessible, so it does not prove
this attempt deleted it. Any retry must keep the same run ID and reviewed
version. Do not switch to another matching draft or claim completion without
evidence of success.
