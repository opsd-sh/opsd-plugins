# Edit a payroll payment

Use `update_payroll_run_payment` for a requested gross-pay or working-hours-band
override on one included employment in a draft or reopened payroll run. Supply
`business_id`, `payroll_run_id` and `employment_id`, plus at least one of
`gross_pay_pence` and `normal_weekly_hours_band`. The employment ID is not the
employee ID; one person can have multiple employments.

Use known IDs and inputs directly. When the target or amount is unclear, use
`get_payroll_run` and the employee discovery tools with Read permission to
resolve it, or ask for the missing information. Business admins and payroll
operators, including practice members, can edit payments. Write permission
alone is sufficient for the edit.

Both fields replace the saved input for this run. Omission preserves the other
field; explicit null is invalid. Send only the requested changes. If both are
provided, they are applied together or neither is applied.

- `gross_pay_pence` is the complete replacement gross amount in integer pence,
  from 0 through 99,999,999,999. For example, £2,500 is 250000 pence. For an
  increase or decrease, use the known current run amount to calculate the new
  total; do not send the adjustment itself or use an employment default as the
  current payment. Zero is a valid explicit amount; unknown pay is not zero.
- `normal_weekly_hours_band` describes the normal weekly working pattern, not
  hours paid in this run. Use `less_than_16`, `sixteen_to_less_than_24`,
  `twenty_four_to_less_than_30`, `thirty_or_more` or `other`. Other means there
  is no normal weekly working pattern; do not use it for missing information.

The edit preserves employment defaults, other included payments and frozen
revisions from previous submissions. Use `update_employment` for a requested
change to future defaults. This tool cannot include or exclude an employment,
change the payment date or schedule, or alter tax settings. An excluded
employment cannot be edited through this tool, and setting pay to zero is not
an exclusion.

A successful response has empty content and means the edit completed. It does
not return the payment or calculate payroll. Report the requested change as
saved; use `get_payroll_run` for current saved inputs or `preview_payroll_run`
for a fresh calculation when needed and Read permission is available. Do not
report a new net-pay figure without a calculation. Editing does not finalize,
submit to HMRC or establish that anyone has been paid.

Every successful call advances the run version, even if values are unchanged.
Do not automatically replay an uncertain result. Read the current payment when
possible, and do not overwrite another edit based on stale information. If the
outcome or desired current values remain unclear, explain that and ask before
retrying. Future actions requiring a version must use a freshly read version;
this edit tool itself has no `expected_version` argument.

Explain returned failures. Payroll must have an active agreement; the employment
must still belong to the run's business, scheme and schedule and already be
included. Finalized, accepted and cancelled runs cannot be edited. Do not change
agreements, employment relationships or payroll state to bypass a rejected edit.
