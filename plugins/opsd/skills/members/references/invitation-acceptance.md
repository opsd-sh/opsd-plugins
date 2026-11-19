# Accept a received invitation

Use `accept_business_invitation` or `accept_practice_invitation` when the user
asks to join through that invitation. Each takes only `invitation_id` and
requires `api:write`. Existing membership and admin privileges are not needed.
The recipient is the connected account; the target and offered role come from
the invitation. Do not supply an email, user ID, business/practice ID or role
as additional arguments, or try to accept on another recipient's behalf.

When needed, use the corresponding received invitation list with Read
permission to identify the intended business or practice, inviter and offered
role. Ask if several invitations fit. A request to list invitations does not
authorize accepting them. Write alone is sufficient when the invitation is
already identified and the user has asked to accept it.

Business roles are `admin` or `payroll_operator`; practice roles are `admin`
or `member`. Acceptance uses the offered role, without changing it. A practice
invitation joins the practice and gives payroll access to all its client
businesses. If the user meant access to only one client, explain this difference
before accepting. Acceptance does not change the connection's OAuth scopes.

Success returns `id`, `name` and `role` for the resulting business or practice
membership. The returned `id` identifies that entity, not the invitation.
Report the role actually returned. This operation sends no acceptance email.

Missing, expired, cancelled, declined, already accepted and other-recipient
invitations all return not found. Do not infer the reason from that error alone.
With Read permission, received invitations and existing memberships can help
explain the current state. An expired invitation needs a new invitation from
an administrator; do not claim acceptance or silently use a different ID.

After an uncertain outcome, retrying the same invitation ID cannot create a
second membership or accept a reissued invitation. A subsequent not-found
response still does not prove the first attempt succeeded. Use membership
lookups when Read permission and the target ID are available, and describe any
remaining uncertainty. An accepted invitation cannot restore membership after
removal; joining again needs a new invitation. Treat a newly listed invitation
as a separate action that must match the user's intent.
