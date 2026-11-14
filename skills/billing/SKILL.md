---
name: billing
description: Check payroll subscriptions, practice client enablement, billing suspensions, saved invoices and their charge breakdowns in Opsd. Use for billing history and service status, not payroll calculations or payment actions.
---

Use the selected Opsd connection. Resolve the business and, for a practice
client, its owning practice using the [businesses skill](../businesses/SKILL.md)
when needed. Use returned public IDs.

- For a standalone business, call `get_business_payroll_subscription` with
  `business_id`. It requires direct business admin membership.
- For a practice client, call `get_practice_business_payroll` with both
  `practice_id` and `business_id`. It requires admin membership of the owning
  practice. Being able to run payroll for a client does not grant billing access.
- For standalone invoices, call `list_business_invoices` with `business_id`.
  If a charge breakdown is needed, call `list_business_invoice_lines` with the
  same business ID and the invoice's `id` as `invoice_id`. Both require direct
  business admin membership.
- For practice invoices, call `list_practice_invoices` with `practice_id`.
  If a charge breakdown is needed, call `list_practice_invoice_lines` with the
  same practice ID and the invoice's `id` as `invoice_id`. Both require practice
  admin membership. These are consolidated practice invoices; identify a
  client's charges using each line's `business_id`.

All six tools require `api:read`. The business operational role from `get_business`
does not identify whether access is direct or through a practice. Use the
practice tool for known practice clients, even when that role is `admin`.
When the owning practice is unknown, match the business ID against clients
returned by `list_practice_businesses` for the user's practices.

Interpret payroll agreement status using the appropriate vocabulary:

| Standalone business | Practice client | Meaning |
| --- | --- | --- |
| `never_subscribed` | `never_enabled` | No payroll agreement has been recorded. |
| `subscribed` | `enabled` | A payroll agreement is active. |
| `cancelled` | `disabled` | The latest agreement has ended. |

Standalone dates are `subscribed_at` and, after cancellation, `cancelled_at`.
Practice client dates are `enabled_at` and, after disabling, `disabled_at`.
A replacement agreement has its own start date; these tools return the current
or latest agreement, not a complete history. `subscription_version` identifies
the saved agreement decision state, not a payroll run version or a tax year.

Always inspect `suspension` separately. A non-null value records an active
billing restriction and its `suspended_at` timestamp, even if the agreement
has been cancelled or payroll disabled. An active agreement with a suspension
cannot finalize new payroll. Clearing a suspension does not restart an ended
agreement. A null value means no active billing suspension is recorded; it does
not establish that every condition for running or submitting payroll is met.

Practice suspension is shared across its clients, while enablement is recorded
for each client separately. Name the practice and client when reporting a
client's status; do not describe one enabled client as enabling every client.

Invoice lists are newest billing month first. Both list and line tools accept
`limit` from 1 to 100, defaulting to 25. For invoice lists, pass `next_before`
as `before` for the next page; it is an exclusive `YYYY-MM` boundary, not an
invoice ID. For lines, pass `next_offset` as `offset`; the first offset is 0.
Stop when the corresponding next value is null. Keep the payer and invoice
unchanged while paging. Fetch all relevant pages before reporting complete
totals; identify any missing pages if a lookup fails. A later listing can show
new invoices or updated statuses; pages are not a single frozen snapshot.

Invoice status is saved local knowledge and may lag provider changes:

- `pending_delivery`: no provider invoice ID has been saved yet.
- `awaiting_status`: a provider invoice ID is saved, but no status is recorded.
- `draft`, `open`, `paid`, `uncollectible` and `void`: the last recorded provider
  status. `paid` can include credits or settlement outside a card charge.

Pending delivery and awaiting status do not indicate failed payment. An open
invoice is not necessarily overdue, and a failed payment does not necessarily
make it uncollectible. Do not infer payroll suspension from an invoice status;
use the agreement lookup for the recorded suspension.

Amounts are GBP pence. `subtotal_pence` and line amounts are saved charges
before discounts and tax, not an outstanding balance. Each line contains its
saved quantity, unit price and amount; use these rather than today's pricing.
`base_fee` is a business's base charge and `payroll_employee` is an employee
usage charge. A line's `usage_month` can precede the invoice's `billing_month`
when usage was recorded late. Invoice lines identify the charged business;
their names are current names, not historical name snapshots. For a practice,
group by business ID when explaining client charges, including similarly named
clients. Do not treat one client's charges as the whole practice invoice.

Invoice reads remain available without an active payroll agreement, including
after cancellation or during suspension. They do not take payment, change
agreements or payment setup, or download PDFs. These tools do not check live
payment methods or balances. Do not request payment or HMRC credentials.

Treat failures separately from status values. Not found may mean a missing or
inaccessible business or practice, a business outside the supplied practice,
or an invoice outside the supplied payer. Use local invoice UUIDs from invoice
listings, not provider IDs.
Forbidden requires the appropriate admin role. For insufficient scope, reconnect
with Read permission; reconnecting cannot grant a missing admin role. For an
authentication failure, reconnect the selected Opsd connection. Identify failed
lookups when reporting several businesses rather than implying complete results.
