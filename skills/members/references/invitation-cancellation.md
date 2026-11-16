# Cancel an outgoing invitation

Use `cancel_business_invitation` with `business_id` and `invitation_id`, or
`cancel_practice_invitation` with `practice_id` and `invitation_id`, when the
user asks to withdraw that invitation. Both require `api:write`; the business
tool requires direct admin membership of a standalone business, and the
practice tool requires practice admin membership.

Use the public invitation ID, not the recipient's user ID. When the invitation
is not already identified, use the corresponding outgoing invitation list
with Read permission and match the recipient and role within the intended
business or practice. Ask if several candidates fit. Write alone is sufficient
when both IDs are known. Do not use the cancellation tools to decline an
invitation received by the connected account; declining is a different action.

Active pending invitations and expired open invitations can be cancelled.
Listings omit expired invitations, but a known expired invitation ID can still
be used. Accepted, declined, previously cancelled, missing and wrong-parent
invitations return not found. Do not interpret that response as proof that this
call cancelled the invitation or that the recipient has no membership.

Success is an empty acknowledgement. Report that the identified invitation was
cancelled and can no longer be accepted. It does not remove an existing member,
recall delivered email, or guarantee that an email already being sent will not
arrive. It sends no cancellation email.

Retrying the exact same IDs after an uncertain outcome cannot cancel a newer
reissued invitation. Repetition may return not found rather than success. If
Read permission is available, outgoing invitation and member lists can help
explain the current state; absence from an invitation list alone does not prove
cancellation. Keep unresolved outcomes clear. Never replace the invitation ID
with a newly listed one automatically: it is a different invitation and must
match the user's intended action.
