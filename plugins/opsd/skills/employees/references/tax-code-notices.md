# Received tax-code notices

Use `apply_employment_tax_code_notice` when the user wants to record an HMRC
notice they have received. Use the supplied notice rather than choosing a new
tax code or deriving one from starter evidence. The tool does not fetch notices
or verify their origin. If several notices conflict, establish which one the
user intends to apply.

Business admins and payroll operators can apply notices, including practice
members. This requires `api:write`, not `hmrc:submit`. Known business and
employment IDs and notice details need no preliminary Read lookup. Identify
the intended employment; an employee can have multiple jobs.

Supply `business_id`, `employment_id` and a required `tax_code_notice` object:

- `tax_year_start`: the notice's explicit tax year start, currently `2026` for
  2026-27. It must match the PAYE scheme's active year. Ask if the notice year
  is unclear; do not change it to bypass validation.
- `tax_code`: the code from the notice. Supply its basis separately, rather
  than appending week 1/month 1 text to the code.
- `tax_basis`: `cumulative` or `non_cumulative` as instructed by the notice.
  Week 1/month 1 means `non_cumulative`; do not infer a basis from the code.
- For cumulative treatment, optional `previous_employment` contains both
  `taxable_pay_pence` (non-negative) and `tax_paid_pence` (signed). These are
  earlier-job totals in integer pence, not pounds or this job's year-to-date
  payments. Preserve negative tax refunds. Supplied figures replace existing
  earlier-job totals; they are not added to them.

When the employment is already cumulative, omitting `previous_employment` or
passing null retains its current earlier-job figures. Switching from
non-cumulative to cumulative requires both figures explicitly. Ask for missing
amounts; use zero only when established as correct. Do not substitute this
employment's own payroll history or invent zeros to make the notice succeed.

For non-cumulative treatment, omit `previous_employment` entirely: even null is
invalid. The current treatment then has no applicable earlier-job amounts;
original starter evidence remains stored separately.

Optional `monthly_gross_pay_pence`, `normal_weekly_hours_band` and `ni_category`
can accompany the notice when the user also requests those changes. Their
[employment-update semantics](employment-updates.md) apply. All changes succeed
or fail together. Start-date and starter-evidence edits cannot accompany a
notice. A conflicting NI change can reject the whole request, including after
finalized payroll; explain the conflict before changing the requested operation.

The tool applies the notice immediately to current-year settings and has no
effective-date scheduling. If the user asks for future application, explain
that limitation rather than applying it early. Live draft previews use the new
treatment. Existing run pay and hours entries and finalized calculations are
retained, including the prior payments that supply this employment's YTD. A new
preview can show different tax and totals for the current payment. The tool
does not finalize payroll or submit anything to HMRC.

Onboarding must be complete, and a closing tax year blocks application. A notice
can otherwise be applied after finalized payroll. Applying one locks starter
evidence. Before a local starter’s first finalised payment, the operator can
still correct the start date on its own. This preserves the notice’s PAYE settings.
See [employment updates](employment-updates.md).

Report the employment ID, applied tax year, code, basis and applicable earlier-job
amounts. Distinguish the applied settings from any unchanged saved payroll result.
