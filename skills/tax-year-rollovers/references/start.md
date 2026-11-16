# Start a tax-year rollover

Use `create_tax_year_rollover_submission_link` only when the user asks to start
a new rollover for a specific business and PAYE scheme. It requires both Write
and Submit permissions. Currently only 2025-26 to 2026-27 is supported.

With Read, use the payroll setup tools to review the scheme's current tax year
and `rollover_generation`, and check existing rollovers. Without Read, use
established IDs and a reviewed generation. Do not assume generation zero or
silently fetch a newer generation after a conflict. Cancellation leaves history
behind; starting again creates a different rollover, not a retry of the old one.

Obtain an explicit destination-year Employment Allowance choice: `claiming` or
`not_claiming`. Do not infer eligibility or reuse the previous year's choice.
Ask for destination-year HMRC tax-code notices and match each to an employment
in this scheme. Each notice needs `employment_id`, `tax_code` and `tax_basis`
(`cumulative` or `non_cumulative`). Use an empty list only when the user confirms
there are no notices to supply. Other employments follow the normal year-end
rules. Do not invent notices or treat the list as every employee's current code.

Call with `business_id`, `paye_scheme_id`, `expected_generation`,
`tax_year_start: 2026`, `employment_allowance` and `tax_code_notices`. Link
creation validates and saves the proposal; it does not close the source year,
create a rollover, change employment settings or contact HMRC. Source payroll
settings are captured again when the user confirms, matching the REST action.
The saved allowance choice and notices cannot be edited through the link.

Present the returned URL as an Opsd confirmation link. It lasts fifteen minutes
and requires the same Opsd account that requested it. The page reviews the
business, scheme, years, allowance choice and notices. Explain that approval
starts closing the source year and sends the final FPS; acceptance can
automatically send the new-year EPS. EPS acceptance completes the rollover and
applies its saved destination-year settings. The user enters HMRC credentials
only on Opsd. Never ask for credentials in chat or tool arguments.

Access, billing, scheme generation and unresolved-payroll checks run again at
confirmation. Approval is consumed atomically with creation of the rollover
and its first final FPS attempt. Failed preparation leaves the scheme open and
the approval unused. Do not repeatedly retry unchanged invalid inputs.

The receipt stays tied to that rollover and final FPS attempt. Report its
outcome separately from overall rollover status: final FPS acceptance alone
does not establish completion. Automatic EPS continuation, a later retry or a
replacement rollover does not change which attempt this receipt describes.
Use the page's status check without Read, or inspect the same rollover and its
history with Read.

After expiry, conflict or an uncertain response, review the scheme and any
created rollover before further action. Do not automatically resubmit
credentials, replace the link, refresh the generation or start a replacement.
Use the appropriate recovery or retry flow for an existing rollover.
