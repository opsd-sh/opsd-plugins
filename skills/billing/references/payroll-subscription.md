# Manage payroll agreements

For a standalone business, use `subscribe_business_to_payroll` to start or
restart its agreement, and `cancel_business_payroll_subscription` to end it.
Supply `business_id` and `expected_version`. Direct business admin membership
is required.

For a practice client, use `enable_practice_business_payroll` or
`disable_practice_business_payroll` with `practice_id`, `business_id` and
`expected_version`. The business must belong to that practice and the caller
must be a practice admin. These actions change only the named client's
agreement. They do not enable or disable every client, remove membership or
change the practice's payment setup. Identify both practice and client when
explaining the intended action; the practice pays the client's charges.

All four actions require Write permission. Use the reviewed
`subscription_version` for that business as `expected_version`. Read current
agreement and suspension using `get_business_payroll_subscription` for a
standalone business or `get_practice_business_payroll` for a practice client
when needed. Those lookups require Read permission. Write alone suffices when
the current target, decision and reviewed version are already known. Versions
belong to individual business agreements, not the whole practice. Do not use
a payroll run version, infer a version from dates or calculate the next value.

Before starting or enabling, explain the billing commitment and establish that
the user intends to activate payroll for this business. Any active,
unsuspended time in a UTC calendar month incurs that business's full base fee,
including partial months and quiet months before the first payroll. Fees are
not prorated. Repeated agreements in the same month do not duplicate the base
fee. Employee usage charges are separate. Use current published pricing when
an amount is needed; do not infer it from historical invoices or invent a price.

A new agreement requires a saved default payment method at Stripe for the payer:
the standalone business or the owning practice. A practice client's own payment
setup cannot satisfy the practice requirement. If a default is missing, use
the payment-method guidance to inspect the payer's setup or direct the user to
billing setup. These actions do not collect card details, create a Stripe
subscription or take immediate payment. An already-active agreement with its
current version preserves its date and version without rechecking payment setup.

Standalone start returns `status: subscribed`, `subscribed_at` and
`subscription_version`. Practice enablement returns `status: enabled`,
`enabled_at`, `subscription_version` and the current practice `suspension`.

Cancellation or disablement takes effect immediately, blocking new payroll
writes for the named business. Explain that effect before acting. Saved payment
methods, payroll records and billing history are retained. Accrued base fees
and employee charges remain payable; stopping does not refund or prorate fees,
settle debt, or withdraw HMRC submissions. The response is an empty
acknowledgement. Never-active and already-stopped agreements are unchanged when
the expected version is current. Stopping needs no payment method or Stripe call.

Neither action clears a billing suspension. Practice suspension applies across
clients, even when one is disabled. Starting or enabling while suspended does
not restore the ability to finalize payroll. The standalone start response does
not include suspension status, so inspect it separately when needed. Restarting
creates a new agreement and retains the old one. Disabling one practice client
does not change another client's agreement or settle the consolidated invoice.

A stale version returns conflict even when the requested action appears to be
a no-op. After conflict or an uncertain outcome, read the current agreement
with Read permission and explain its status before deciding again. Do not
silently replace the version and repeat a financial commitment, or stop an
agreement that someone has since restarted. A matching current state is not
proof that the earlier call caused it. If the required review cannot be made,
stop and report the uncertainty. Repeated provider failures also require a
report rather than an indefinite retry loop.
