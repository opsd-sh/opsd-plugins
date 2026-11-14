---
name: billing
description: Check payroll subscriptions, practice client enablement, billing suspensions, invoice history and live payment-method setup in Opsd. Use for billing status and charge breakdowns, not payroll calculations or payment actions.
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
- To check whether a standalone business has a default payment method, call
  `get_business_billing_status` with `business_id`. If details of its saved
  methods are needed, call `list_business_payment_methods` with the same ID.
  Both require direct business admin membership.
- For the practice's shared payment setup, use `get_practice_billing_status`
  or `list_practice_payment_methods` with `practice_id`. Both require practice
  admin membership. Payment setup belongs to the practice, not each client.

All ten tools require `api:read`. The business operational role from `get_business`
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
after cancellation or during suspension. Invoice tools use saved local state;
the billing-status and payment-method tools instead read Stripe live. None of
these tools takes payment, changes agreements or payment setup, downloads PDFs,
or reports a live outstanding balance. Do not request payment or HMRC credentials.

`payment_method_saved` means Stripe currently records a default payment method.
False can mean no default or missing/pending customer setup; it does not prove
there are no attached methods. True does not establish that payroll is enabled,
unsuspended or guaranteed to collect successfully. Check the agreement only
when the user's question also requires payroll service status.

Payment-method lists include IDs, types, the current `is_default` marker and,
for cards, brand, last four digits and expiry. `card: null` means a non-card
method, not missing payment setup. These reads expose the customer's invoice
default; they do not select a method or change existing invoices.

For payment-method pagination, pass `next_starting_after` as `starting_after`
with the same payer ID until null. `limit` defaults to 25 and allows 1 to 100.
This cursor is a returned payment-method ID, unlike an invoice month or offset.
The default may be on a later page. Methods and defaults can change between
reads, so a listing is not a frozen snapshot. If a cursor becomes invalid,
check the payer and restart from the first page once; report a repeated failure.
An empty successful list includes missing or pending customer setup. A provider
failure is an error, not an empty list or a false billing status; explain the
returned problem and any indicated retry delay.

Treat failures separately from status values. Not found may mean a missing or
inaccessible business or practice, a business outside the supplied practice,
or an invoice outside the supplied payer. Use local invoice UUIDs from invoice
listings, not provider IDs.
Forbidden requires the appropriate admin role. For insufficient scope, reconnect
with Read permission; reconnecting cannot grant a missing admin role. For an
authentication failure, reconnect the selected Opsd connection. Identify failed
lookups when reporting several businesses rather than implying complete results.
