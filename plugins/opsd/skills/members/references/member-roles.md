# Change a member's role

Use `update_business_member` with `business_id`, `user_id` and `role` for a
standalone business, or `update_practice_member` with `practice_id`, `user_id`
and `role` for a practice. Both require `api:write` and the corresponding admin
membership. The actor is always the connected account.

`user_id` is the public account ID from the member list, not an employee,
employment or invitation ID. If the target is unclear, list the relevant
members with Read permission and match their email. Write alone suffices when
the entity, existing member and desired role are already identified.

Business roles are `admin` and `payroll_operator`. Practice roles are `admin`
and `member`. Both ordinary roles retain payroll access; admin additionally
allows administration of the relevant business or practice. Use the exact role
names for that entity. This changes membership permissions, not OAuth scopes,
and does not change an account's email or verification status. A pending
invitation is not a member; changing its offered role is not supported here.

Practice clients do not have separately managed business members. A practice
role applies across all its client businesses. Do not turn a request concerning
one client into a practice-wide role change unless that matches the user's
intent. A business operational `admin` role inherited from a practice does not
authorize direct business member management.

The last administrator cannot be demoted: that returns a conflict and leaves
the role unchanged. If the user wants to hand over administration, the intended
successor must be an existing member with admin access before demoting the
current admin. Do not promote somebody else merely to bypass this guard.
Self-demotion is allowed when another admin remains, but removes the caller's
ability to manage members or list members and outgoing invitations for that
entity.

Success is an empty acknowledgement. Report that the identified member's role
is set to the requested value; the tool also succeeds if it was already set.
No membership is created or removed, and no notification email is sent. A
missing target is not an invitation to add them automatically.

After an uncertain outcome, inspect the member list with Read permission if
still authorized. Repeating the same assignment is idempotent in unchanged
state, but can overwrite a later administrator's change. Retry only while the
requested role still matches the user's intent. After self-demotion, a repeat
request can be forbidden; that does not prove the first request failed.
Reconnecting with broader OAuth scopes cannot restore a lost admin role.
