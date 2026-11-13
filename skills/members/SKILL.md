---
name: members
description: List Opsd business or practice members, their roles, and pending invitations sent or received. Use for account access questions, not employee payroll records.
---

Use the selected Opsd connection. For member or outgoing invitation lookups,
resolve the business or practice using the businesses skill when its ID is not
already known. Received invitations can be listed without existing membership.

For invitations addressed to the connected account:

- Call `list_business_invitations` with no arguments for business invitations.
- Call `list_practice_invitations` with no arguments for practice invitations.
- For a general request such as "my invitations", include both lists. Identify
  any failed lookup rather than presenting a partial result as complete.

These tools use the authenticated account's email; they cannot look up another
recipient. Results include invitation IDs, business or practice IDs and names,
inviter emails, offered roles and expiry times. Use those names and IDs to
identify invitations; the recipient may not yet have access to retrieve the
business or practice. An offered role is not an existing membership.

For members or invitations sent by an entity:

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
`pending` status and expiry times. All invitation listings include only pending,
unexpired invitations; accepted, declined, cancelled and expired records are
excluded. An empty result means no current pending invitations in that list,
not that nobody has ever been invited. Do not treat a pending invitee as an
existing member or an invitation record as proof that its email was delivered.

All six tools require `api:read` and only inspect access. They do not change
memberships or send, accept or decline invitations. Match names or emails locally.
Member and outgoing invitation tools take the relevant business or practice ID;
received invitation tools take no arguments.

Keep failed lookups separate from empty results. A not-found response may mean
missing or inaccessible; a forbidden response requires the appropriate admin
role for member and outgoing invitation listings. Reconnecting with Read
permission addresses insufficient scope, not a missing admin role. For
authentication failures, reconnect the selected Opsd connection. If a lookup
fails, identify the gap in any combined results.
