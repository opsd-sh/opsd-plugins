---
name: businesses
description: List standalone Opsd businesses, find one by name, or look up a business by ID and report the user's role.
---

Use the Opsd connection selected by the user or established in the conversation.
If several connections are available and the intended one is unclear, ask which
to use. Keep the lookup on that connection, including when no match is found.

Choose the lookup from the user's request:

- To list businesses, call `list_businesses` with no arguments. It returns only
  standalone businesses where the user has direct membership; it does not list
  businesses owned by a practice.
- Given a business ID, call `get_business` with that ID as `business_id`.
  It can also return a business accessible through its owning practice, so do
  not require the ID to appear in `list_businesses` first.
- Given a business name, call `list_businesses` and match the returned names
  locally. Prefer a unique exact match, ignoring case and surrounding whitespace.
  If several businesses could match, show their names and IDs and ask the user
  to choose. Use the returned ID; do not invent one from the name.
- If no name matches, explain that no matching standalone business was returned.
  Ask for its ID if the user wants to look it up, including when it may belong
  to a practice. An empty list does not establish that the user has no access
  to any business.

Report the returned business name, public ID and role. For `get_business`, the
role is the user's operational role; it does not establish whether their access
comes from direct membership or a practice. A matching list entry already
contains these fields, so another lookup is unnecessary when it answers the
request. Keep any follow-up lookup tied to the selected business ID and connection.

Treat tool failures separately from successful empty results. A not-found
response can mean the business is missing or inaccessible to the connected
account; do not claim to know which. For an authentication failure, ask the user
to reconnect the selected Opsd connection. For other failures, explain the
returned problem and any indicated retry delay without presenting stale data
as a successful lookup.
