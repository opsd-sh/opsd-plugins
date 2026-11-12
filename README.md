# Opsd plugins

Shared skills, assets and provider packaging for Opsd. This repository is intended
to become public later; this first version is local and has not been published.
The only provider currently implemented is OpenAI (ChatGPT and Codex).

Opserver handles authentication, permissions and business operations. These
packages connect to its existing MCP server.

## Source layout

```text
assets/icon.svg                 Shared Opsd icon
skills/businesses/SKILL.md       Shared business and practice discovery skill
skills/payroll-setup/SKILL.md    PAYE scheme and pay schedule discovery
providers/openai/plugin.json     OpenAI manifest defaults
providers/openai/mcp.json        OpenAI MCP connection defaults
production.json                 Production identity and endpoint
Makefile                        Build and test commands
scripts/build.py                Shared packaging script
tests/test_build.py              Packaging checks
```

The skills and icon are maintained here once. The private `opsd-plugins-dev`
repository supplies development settings and invokes this same build script.
Future providers can add their own packaging under `providers/` while reusing
the shared content; their formats are not implemented yet.

## Build

Requires Make and Python 3.10 or newer, using only Python's standard library.
Run `make` to list the available commands.

```sh
make build
```

This creates a local marketplace and plugin ZIP under `dist/openai/`:

```text
dist/openai/
  .agents/plugins/marketplace.json
  plugins/opsd/
    .codex-plugin/plugin.json
    .mcp.json
    skills/businesses/SKILL.md
    skills/payroll-setup/SKILL.md
    assets/icon.svg
  opsd.zip
```

The ZIP contains the plugin files at its root. It excludes the marketplace,
build scripts and source configuration. Generated files are ignored by Git and
replaced on each successful build. Edit source files, not `dist/`.

Content copying excludes `.env` and `.env.*`, Python bytecode, cache and virtual
environment directories, `.git` metadata, and common editor metadata and backup
files at every level. The exact patterns are in `scripts/build.py`; these are
explicit packaging rules, not an interpretation of `.gitignore`.

Links within `skills/` and `assets/` are copied as ordinary files and directories.
Links to excluded content are also excluded. Links outside those directories,
broken links and directory cycles fail the build, leaving the previous package
in place.

The MCP server key matches the configured plugin name. Production uses `opsd`;
environment variants use their own names so their client-side connections remain
distinct when installed together.

The OpenAI package uses the Codex compatibility format already tested with
Codex CLI 0.167.0. That version discovered the manifest but not the MCP connection
when we previously tried the portable root `plugin.json` / `mcp.json` format.

## Local installation

This package connects to production. Use the private development repository for
development accounts and data.

```sh
codex plugin marketplace add ./dist/openai
codex plugin add opsd@opsd
```

Restart Codex desktop or start a fresh CLI session after installation. Building
does not install the package, register a marketplace or publish anything.

The existing development package's OAuth login and both business tools were
verified in Codex desktop. This new packaging adds the shared skill; production
login and ChatGPT web testing remain deferred until a production user exists.
The ZIP is an initial package, not a completed public catalogue submission.

## Tools and authentication

- `list_businesses` lists standalone businesses where the user has direct membership.
- `get_business` looks up a business by its public ID, including access through a practice.
- `list_practices` lists practices and the user's role in each.
- `get_practice` looks up a practice by its public ID.
- `list_practice_businesses` lists the businesses owned by a practice.
- `list_paye_schemes` lists a business's PAYE schemes and recorded settings.
- `list_pay_schedules` lists its schedules, frequencies and PAYE scheme IDs.

The shared skill combines standalone businesses and practice clients for general
business discovery. It keeps practice roles separate from business operational
roles and identifies partial results if a practice lookup fails.

The payroll-setup skill helps select an existing scheme and schedule within the
chosen business, using IDs to match schedules to their schemes.

All seven tools read data. OAuth requests `api:read`, `api:write`, and `hmrc:submit`.
On the consent page, the user can approve any nonempty subset of these independent
permissions. These tools require `api:read`; granting only write or
submission permission does not allow these lookups. Opserver enforces the granted
scopes alongside the user's existing membership and role permissions.

The listing's Read capability describes the available tools; it does not restrict
the token to read-only access. OAuth endpoints and CIMD support are discovered
from Opserver; credentials are not packaged.

Version 0.1.5 adds practice discovery guidance. Deploy the corresponding Opserver
practice tools to the target environment before testing those workflows.
The existing OAuth scopes and connection identities are unchanged. If practice
tools are unavailable, the skill reports that limit and can still look up a
known client business ID with `get_business`.

The icon is the existing Opsd favicon from `www/public/favicon.svg`.

## Checks

```sh
make test
```

The checks cover self-contained packages, shared file reuse, content exclusions,
symlink handling, rebuilding, output protection and invalid configuration.
Increment the version in
`providers/openai/plugin.json` when releasing package changes.

See the [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins)
for the supported manifest and marketplace formats.
