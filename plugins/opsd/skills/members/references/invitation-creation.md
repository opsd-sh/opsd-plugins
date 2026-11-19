# Create an invitation

Use these tools when the user asks to invite someone to Opsd. Resolve the
intended business or practice, recipient email and offered role before creating
an invitation. A known ID and complete inputs need no preliminary lookup;
Write permission alone is sufficient alongside the required admin membership.

- `create_business_invitation` takes `business_id`, `email` and `role` for a
  standalone business. It requires direct business admin membership. Roles are
  `admin` (including user management and billing) or `payroll_operator`.
- `create_practice_invitation` takes `practice_id`, `email` and `role`. It
  requires practice admin membership. Roles are `admin` (including practice
  user management and billing) or `member`. Both give payroll access to all
  businesses owned by the practice.

There is no default role. If the intended level of access is unclear, explain
the choices and ask; do not silently offer admin access. Use the supplied email;
the server trims surrounding whitespace and lowercases it.

Practice-owned businesses do not have direct business users. A request to give
someone access to one client does not authorize a practice-wide invitation.
Explain that practice membership covers all its clients and obtain agreement
to that broader access before using the practice invitation tool. If that is
not intended, explain the current limitation.

A successful response contains `id`, canonical `email`, `role`, `status` and
`expires_at`. Report the invitation as pending and the email as queued, not
confirmed delivered. Acceptance is still required for membership. Use the
returned expiry rather than calculating one. These tools do not accept an
invitation on the recipient's behalf.

An existing member or active pending invitation causes a conflict. Creation
cannot update an active invitation's role or resend its email. If Read
permission is available, inspect the corresponding member or outgoing
invitation list to explain the conflict. Do not change the recipient or role
merely to bypass it, or claim the requested role was granted. Do not automatically
cancel the existing invitation to bypass a conflict. For an explicit withdrawal
request, follow the [cancellation guide](invitation-cancellation.md).

An expired open invitation can be reissued; its public ID, role and expiry are
replaced and another email is queued. The previous link stops working. This is
not idempotent over time. After a timeout, connection failure or internal error
with an uncertain outcome, do not automatically retry. With Read permission,
check outgoing invitations for the intended recipient and role. Listings omit
expired and resolved invitations, so absence is not proof of failure. If the
outcome remains uncertain, explain it and ask before another attempt. A clear
validation rejection can be corrected before retrying.
