---
name: members
description: List a standalone business's or practice's members, their roles, or pending outgoing invitations in Opsd. Use for account access questions, not employee payroll records.
---

Use the selected Opsd connection. Resolve the business or practice using the
businesses skill when its ID is not already known; use returned public IDs.

Choose the tool for the entity being administered:

- For a standalone business, call `list_business_members` with `business_id`.
  To see invitations it has sent, call `list_outgoing_business_invitations`
  with the same ID. Both require direct business admin membership.
- For a practice, call `list_practice_members` with `practice_id` or
  `list_outgoing_practice_invitations` with that ID. Both require practice
  admin membership.
- For a practice-owned business, use the owning practice's tools. Membership
  belongs to the practice and gives access to all its client businesses; label
  the results as practice membership, not a separate client member list.
  If the owning practice is unknown, match the business ID against clients
  returned by `list_practice_businesses` for the user's practices.

The operational role returned by `get_business` does not distinguish direct
membership from practice access. In particular, an `admin` operational role
alone does not establish permission to list business members or invitations.

Member results contain user IDs, emails, email verification and roles. These
are Opsd user accounts, not employees or employments. Use the employees skill
for payroll records. Keep business roles (`admin`, `payroll_operator`) and
practice roles (`admin`, `member`) distinct when reporting access.

Outgoing invitation results contain invitation IDs, invitee emails, roles,
`pending` status and expiry times. They include only pending, unexpired
invitations; accepted, declined, cancelled and expired records are excluded.
An empty result means no current pending invitations, not that nobody has ever
been invited. These tools do not show invitations received by the connected user.
Do not treat a pending invitee as an existing member or an invitation record as
proof that its email was delivered.

All four tools require `api:read` and only inspect access. They do not invite,
remove or change users. Match requested names or emails locally; the only tool
argument is the relevant business or practice ID.

Keep failed lookups separate from empty results. A not-found response may mean
missing or inaccessible; a forbidden response requires the appropriate admin
role. Reconnecting with Read permission addresses insufficient scope, not a
missing admin role. For authentication failures, reconnect the selected Opsd
connection. If a lookup fails, identify the gap in any combined results.
