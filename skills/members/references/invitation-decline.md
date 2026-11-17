# Decline a received invitation

Use `decline_business_invitation` or `decline_practice_invitation` when the
user asks to turn down an invitation addressed to the connected account.
Each takes only `invitation_id` and requires `api:write`; existing membership
and admin privileges are not needed. The recipient comes from authentication.
Do not supply a user ID, email, business/practice ID or role as extra arguments.

When the invitation is not already identified, use the corresponding received
invitation list with Read permission to match the business or practice, inviter
and offered role. Ask if several invitations fit. Listing invitations does not
authorize declining them. Write alone suffices when the invitation is identified
and the user has asked to decline it.

Declining is the recipient's action. Use cancellation tools to withdraw an
outgoing invitation as its sender's administrator. Neither action removes
an existing membership or recalls an email. Do not interpret a request to
leave a business or practice as a request to decline an old invitation.

Only pending, unexpired invitations can be declined. Success is an empty
acknowledgement: report that the identified invitation was declined and can no
longer be accepted. No decline email is sent. Joining later requires a fresh
invitation from an administrator.

Missing, expired, cancelled, accepted, already declined and other-recipient
invitations all return not found. Do not infer which state caused that error.
An accepted invitation cannot be declined to undo membership.

After an uncertain outcome, retrying the exact same ID cannot decline a newer
reissued invitation, but a not-found response does not prove the first attempt
succeeded. With Read permission, check received invitations if useful; absence
alone does not establish why an invitation disappeared. Keep any uncertainty
clear and do not silently substitute another invitation ID.
