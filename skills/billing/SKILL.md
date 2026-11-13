---
name: billing
description: Check a standalone business's payroll subscription or a practice client's payroll enablement and billing suspension in Opsd. Use for saved payroll service status, not payroll calculations or payment actions.
---

Use the selected Opsd connection. Resolve the business and, for a practice
client, its owning practice using the [businesses skill](../businesses/SKILL.md)
when needed. Use returned public IDs.

- For a standalone business, call `get_business_payroll_subscription` with
  `business_id`. It requires direct business admin membership.
- For a practice client, call `get_practice_business_payroll` with both
  `practice_id` and `business_id`. It requires admin membership of the owning
  practice. Being able to run payroll for a client does not grant billing access.

Both tools require `api:read`. The business operational role from `get_business`
does not identify whether access is direct or through a practice. Use the
practice tool for known practice clients, even when that role is `admin`.
When the owning practice is unknown, match the business ID against clients
returned by `list_practice_businesses` for the user's practices.

Interpret the status using the appropriate vocabulary:

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

These tools read stored agreement and suspension state. They do not establish
whether a payment method is saved, an invoice balance, or a successful payment.
They do not subscribe, cancel, enable, disable, settle debt or change payment
setup. Do not request payment or HMRC credentials for these lookups.

Treat failures separately from status values. Not found may mean a missing or
inaccessible business or practice, or a business outside the supplied practice.
Forbidden requires the appropriate admin role. For insufficient scope, reconnect
with Read permission; reconnecting cannot grant a missing admin role. For an
authentication failure, reconnect the selected Opsd connection. Identify failed
lookups when reporting several businesses rather than implying complete results.
