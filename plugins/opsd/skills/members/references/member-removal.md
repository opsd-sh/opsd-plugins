# Remove a member

Use `remove_business_member` with `business_id` and `user_id` for a standalone
business, or `remove_practice_member` with `practice_id` and `user_id` for a
practice. Both require `api:write` and the corresponding admin membership.
Ordinary members cannot use these tools, even to remove themselves. The actor
comes from authentication; `user_id` identifies the member to remove.

Use the public user account ID from the member list, not an employee,
employment or invitation ID. If needed, list members with Read permission and
match the intended account by email. Write alone suffices when both IDs and
the intended removal are already clear. A request to list members does not
authorize removal. For a pending invitation, use cancellation instead.

Practice clients do not have separately managed business members. Removing a
practice member removes their subsequent access through that practice to all
its client businesses. Do not turn a request to remove access to one client
into practice-wide removal unless that matches the user's intent.

The last administrator cannot be removed: the call returns a conflict without
changing membership. If the user intends to hand over administration, use the
[role guide](member-roles.md) to establish the intended successor first. Do not
promote another person merely to bypass the guard. Self-removal is allowed
when another admin remains. It removes the caller's access through that
membership, including member lists and management.

Success is an empty acknowledgement. Report removal of the identified
membership. The user account, OAuth credentials, independent memberships,
employees and payroll history are retained. No removal email is sent and
invitation records are unchanged. Removing membership does not cancel a
payroll run, disable payroll billing or delete a business or practice.

A missing member returns not found. After an uncertain outcome, inspect the
member list with Read permission if still authorized. Report current absence
separately from proof that the earlier call succeeded. After self-removal,
subsequent calls can return not found because the caller has lost access.

A user's public ID stays the same if they later rejoin. Repeating removal is
idempotent while state is unchanged, but could remove a newer membership after
rejoining. Do not retry blindly; a further removal must still match the user's
intended access change. Restoring access requires a new invitation and
acceptance; reconnecting the plugin alone does not restore membership.
