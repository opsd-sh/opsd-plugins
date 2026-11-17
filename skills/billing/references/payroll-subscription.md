# Start or cancel a standalone payroll subscription

Use `subscribe_business_to_payroll` to start or restart a standalone business's
payroll agreement, and `cancel_business_payroll_subscription` to end it. Both
require `business_id`, `expected_version`, Write permission and direct business
admin membership. They do not manage a practice client's payroll enablement.

Use the reviewed `subscription_version` as `expected_version`. Read current
agreement and suspension with `get_business_payroll_subscription` when needed;
that lookup requires Read permission. Write alone suffices when the current
business, decision and reviewed version are already known. Do not use a payroll
run version, infer a version from dates or calculate the next version yourself.

Before starting, explain the billing commitment and establish that the user
intends to subscribe this business. Any subscribed, unsuspended time in a UTC
calendar month incurs that month's full base fee, including partial months
and quiet months before the first payroll. Fees are not prorated. Repeated
agreements in the same month do not duplicate the base fee. Employee usage
charges are separate. Use current published pricing when an amount is needed;
do not infer it from historical invoice lines or invent a price.

Starting a new agreement requires a saved default payment method at Stripe.
If one is missing, use the payment-method guidance to inspect existing setup
or direct the user to billing setup. This operation does not collect card
details, create a Stripe subscription or take immediate payment. A successful
response contains `status: subscribed`, `subscribed_at` and
`subscription_version`. An already-active agreement with its current version
returns its existing date and version without rechecking payment setup.

Cancellation takes effect immediately, blocking new payroll writes. Explain
that effect before acting. It retains saved payment methods, payroll records
and billing history. Accrued base fees and employee charges remain payable;
cancellation does not refund or prorate fees, settle debt, or withdraw HMRC
submissions. It returns an empty acknowledgement. A never-subscribed or
already-cancelled agreement is unchanged when the expected version is current.
Cancellation does not need a payment method or contact Stripe.

Neither action clears a billing suspension. Subscribing while suspended does
not restore the ability to finalize payroll; the start response does not
include suspension status. Cancellation does not resolve the reason for a
suspension. Inspect it separately when explaining whether payroll can proceed.
Restarting after cancellation creates a new agreement and retains the old one.

A stale version returns conflict even when the requested action appears to be
a no-op. After conflict or an uncertain outcome, read the current agreement
with Read permission and explain its status before deciding again. Do not
silently replace the version and repeat a financial commitment, or cancel an
agreement that someone has since restarted. A matching current state is not
proof that the earlier call caused it. If the required review cannot be made,
stop and report the uncertainty. Repeated provider failures also require a
report rather than an indefinite retry loop.
