---
name: businesses
description: Find Opsd businesses and practices, report membership roles, or create practices, standalone businesses and practice clients.
---

Use the Opsd connection selected by the user or established in the conversation.
If several connections are available and the intended one is unclear, ask which
to use. Keep lookups and creation on that connection, including when no match is
found.

Choose the lookup from the user's request:

- For standalone businesses, call `list_businesses` with no arguments. It returns
  only businesses where the user has direct membership, excluding practice clients.
- For practices, call `list_practices` with no arguments. Given a practice ID,
  call `get_practice` with it as `practice_id`. Both return the user's practice role.
- For a practice's clients, call `list_practice_businesses` with its `practice_id`.
  If only the practice name is known, resolve it with `list_practices` first.
  Each client has a business ID, name and practice ID; no business role is returned.
- Given a business ID, call `get_business` with it as `business_id`. It supports
  both direct membership and access through the owning practice; no listing is
  required first.
- For a general business list, or a business name without a specified practice, include
  both `list_businesses` and the clients of each practice from `list_practices`.
  Do not treat the standalone listing as a complete list of accessible businesses.
  Keep each client's practice name and ID with it so similarly named businesses
  can be distinguished. If the user specifies a practice, search only its clients.

Match names locally. Prefer a unique exact match, ignoring case and surrounding
whitespace. If several records could match, show their names and IDs, including
the owning practice for clients, and ask the user to choose. Use returned IDs;
do not invent them from names. If no match is returned, say what was searched.

Use the returned names and public IDs to identify records. Report roles when
requested or useful: `list_businesses` and `get_business` provide business roles;
`list_practices` and `get_practice` provide practice roles. To report a practice
client's business role, call `get_business` with its ID rather than inferring it
from the practice role. The operational role from `get_business` does not identify
whether access comes from direct membership or a practice. Avoid a follow-up
lookup when the existing result already answers the request.

For a request to create a business, establish its name and whether it should be
standalone or owned by an existing practice. Ask if that choice is unclear from
the request and context. A lookup that finds no match is not a request to create.

- Use `create_business` with `name` for a standalone business. The connected user
  becomes its admin; the response contains the new ID, name and role.
- Use `create_practice_business` with `practice_id` and `name` for a practice
  client. Resolve a named practice using the lookups above; a supplied practice
  ID needs no preliminary lookup. Creation requires practice admin membership.
  The response contains the new ID, name and owning practice ID. Access is
  inherited from the practice, with no direct business memberships.

Names are trimmed and must contain 1–120 characters with no control characters.
Creation adds the business record; payroll setup and enablement are separate
operations. Use the returned ID to identify the new business and report success
only when the tool confirms creation.

For an explicit request to create a practice, follow [practice creation](references/practice-creation.md)
and call `create_practice`. Obtain its display name and separate HMRC reporting
name; the connected user becomes its admin. This is different from creating a
client business within an existing practice.

Each successful creation call creates a new business or practice, even with an
identical name. If a timeout, connection failure or internal error leaves the outcome
uncertain, do not automatically retry. Use the appropriate listing to help check
what happened when Read permission is available; a matching name alone does not
prove which call created it. Explain unresolved uncertainty and ask before
attempting another creation. After a clear validation rejection, correct the
input before trying again.

Treat tool failures separately from successful empty results. If any practice
client listing fails, identify that gap rather than presenting the remaining
businesses as a complete list. If the connection does not expose the practice
tools, explain that practice discovery is unavailable on that connection; a
known client business ID can still be passed to `get_business`.

A not-found response can mean the business or practice is missing or inaccessible
to the connected account; do not claim to know which. For an authentication
failure, ask the user to reconnect the selected Opsd connection. For insufficient
scope, explain which permission the operation needs: lookups require `api:read`
and creation requires `api:write`. These are independent; Write alone permits
creation when the required inputs are already known. Ask the user
to reconnect with the missing permission when it is needed. For other failures,
explain the returned problem and any indicated retry delay without presenting
stale data as a successful lookup.
