# Select a default payment method

Use `set_business_default_payment_method` with `business_id` and
`payment_method_id` for a standalone business, or
`set_practice_default_payment_method` with `practice_id` and
`payment_method_id` for a practice. Both require `api:write` and the
corresponding admin membership. The payer's Stripe customer is resolved by
Opsd; never supply a customer ID.

Select an already saved method attached to that payer. If discovery is needed,
use the corresponding `list_*_payment_methods` tool with Read permission and
match the intended method using its ID and safe display details. Last four
digits alone may not uniquely identify a card. Non-card methods can also be
selected. Write alone suffices when the payer and intended saved method are
already clear. Do not request card numbers, security codes or provider secrets.

A request to inspect payment methods does not authorize changing the default.
For practice clients, the practice pays the consolidated bill: selecting its
default affects shared practice billing, not just the named client. Establish
that this is the intended payer and change before selecting.

Success is an empty acknowledgement that Stripe confirmed the chosen customer
invoice default. Report the selection, not a payment or proof that collection
will succeed. This operation does not itself charge, retry collection, refund,
edit invoices, attach a new method or delete the old one. It does not start a
payroll subscription, enable client payroll, or clear a billing suspension.
The changed default can be used for subsequent collection. Do not promise
that only newly created invoices can use it, or that an unpaid bill is settled.

Missing or pending customer setup returns not found; this tool does not create
a customer or start setup. A method not attached to the payer is rejected.
Do not try another payer or method merely to get past a rejection. If no suitable
saved method exists, direct the user to the application's billing setup.

A provider failure can leave the outcome uncertain, including when Stripe
applied the change but its reply could not confirm it. Do not report a failed
call as proof that the previous default is unchanged. If authorized, list the
payer's methods with Read permission and inspect the current `is_default`
marker; follow pagination if needed. Billing status alone cannot identify the
selected method. Repeating the same selection has no additional effect while
the preference is unchanged, but can overwrite a newer choice. Retry only if
it still matches the user's intended selection; stop and report a repeated
provider failure instead of retrying indefinitely.
