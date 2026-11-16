# Replace practice HMRC reporting details

Use `replace_practice_hmrc_reporting` when the user requests a change to a
practice's HMRC agent reporting identity. It requires `api:write` and current
practice admin membership. Supply the public `practice_id` and a complete
`hmrc_reporting` object.

The reporting `name` is required. Optional fields are `address`, `contact_name`,
`email` and `telephone`. An address contains `lines` (one to four), with optional
`post_code` and `country`. A contact name contains `forenames` (one or two) and
`surname`, with optional `title`. Use the user's actual reporting details;
validation follows the same rules as practice creation and the REST endpoint.

This is a full replacement. Omitting an optional field or passing null clears
it, including optional fields inside `address` and `contact_name`. Supplying
only a new name therefore removes the saved address and all contact details.

For a partial change, use `get_practice_hmrc_reporting` when `api:read` is
available, preserve the returned values the user did not ask to change, and
apply the requested changes to that complete object. Make any requested
clearing clear in the proposed change. Read permission is not required when
the complete intended replacement is already known. Otherwise ask for the
missing details or permission to clear them; do not turn unknown values into
null just because they could not be read.

These settings are saved locally without contacting HMRC. The reporting name
is separate from the practice display name. This operation does not change
Government Gateway credentials or what a past submission contained. Report
the saved details using the successful response.

Repeating an identical replacement is idempotent, but it can overwrite another
user's intervening edits. There is no version check between reading and saving.
After an uncertain outcome, do not automatically retry. Inspect the current
details if Read permission is available and review any differences before
another write. If the result cannot be checked, explain the uncertainty and
ask before another attempt. A clear validation rejection can be corrected.
