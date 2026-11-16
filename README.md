# Opsd plugins

Shared skills, assets and provider packaging for Opsd. This repository is intended
to become public later; this first version is local and has not been published.
The only provider currently implemented is OpenAI (ChatGPT and Codex).

Opserver handles authentication, permissions and business operations. These
packages connect to its existing MCP server.

## Source layout

```text
assets/icon.svg                 Shared Opsd icon
skills/businesses/SKILL.md       Business discovery and creation skill
skills/members/SKILL.md          Members and sent or received invitations
skills/billing/SKILL.md          Agreements, invoices and live payment setup
skills/payroll-setup/SKILL.md    Payroll setup and practice HMRC reporting
skills/employees/SKILL.md        Employee and employment discovery
skills/payroll/SKILL.md          Draft payments, previews and payroll history
skills/tax-year-rollovers/SKILL.md  Tax-year rollover progress, cancellation and history
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
    skills/members/SKILL.md
    skills/billing/SKILL.md
    skills/payroll-setup/SKILL.md
    skills/employees/SKILL.md
    skills/payroll/SKILL.md
    skills/tax-year-rollovers/SKILL.md
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

- `create_business` creates a standalone business with the connected user as admin.
- `create_practice_business` creates a client owned by an existing practice, requiring practice admin membership.
- `list_businesses` lists standalone businesses where the user has direct membership.
- `get_business` looks up a business by its public ID, including access through a practice.
- `list_practices` lists practices and the user's role in each.
- `get_practice` looks up a practice by its public ID.
- `get_practice_hmrc_reporting` reads its stored HMRC reporting identity and contact details.
- `list_practice_businesses` lists the businesses owned by a practice.
- `list_business_members` and `list_practice_members` list user accounts and roles.
- `list_outgoing_business_invitations` and `list_outgoing_practice_invitations`
  list pending, unexpired invitations sent by the business or practice.
- `list_business_invitations` and `list_practice_invitations` list pending,
  unexpired invitations received by the connected account.
- `get_business_payroll_subscription` reads a standalone business's payroll agreement and suspension.
- `get_practice_business_payroll` reads a practice client's payroll enablement and shared suspension.
- `list_business_invoices` and `list_practice_invoices` page through saved invoice summaries.
- `list_business_invoice_lines` and `list_practice_invoice_lines` page through saved charges by business.
- `get_business_billing_status` and `get_practice_billing_status` check the current default payment method at Stripe.
- `list_business_payment_methods` and `list_practice_payment_methods` read live saved methods and safe card summaries.
- `create_paye_scheme` records a PAYE scheme and its initial tax-year settings within a business.
- `create_pay_schedule` creates a monthly schedule under a scheme in that business.
- `list_paye_schemes` lists a business's PAYE schemes and recorded settings.
- `list_pay_schedules` lists its schedules, frequencies and PAYE scheme IDs.
- `create_employee` creates a person’s record within a business.
- `update_employee` changes personal details while preserving payroll-history restrictions.
- `list_employees` and `get_employee` return employee personal details.
- `create_employment` links an employee to a scheme and schedule and resolves initial tax settings from supplied starter evidence.
- `update_employment` changes payroll defaults or starter evidence while preserving payroll-history and tax-code-notice restrictions.
- `apply_employment_tax_code_notice` records a received notice without replacing starter evidence or saved payroll history.
- `list_employments` and `get_employment` return linked employment records and
  stored payroll settings.
- `create_payroll_run` creates a draft and copies the schedule’s eligible employments and payment defaults.
- `update_payroll_run_payment` changes gross pay or working-hours band on an included draft payment without changing employment defaults.
- `include_payroll_run_employment` adds an employment with current payment defaults, preserving an existing payment when already included.
- `exclude_payroll_run_employment` removes an employment's payment and overrides from a draft or reopened run.
- `discard_payroll_run` permanently deletes an ordinary draft and its payments, checking the reviewed version.
- `reopen_payroll_run` reopens an eligible finalized run for corrections, preserving saved payments and submission history.
- `cancel_payroll_run` marks an eligible finalized or reopened run as cancelled, retaining its records and submission history.
- `resume_payroll_run_polling` resumes paused HMRC status checks for an existing submission in the background.
- `create_payroll_run_submission_link` creates an expiring browser link for the user to confirm payroll submission with one-off HMRC credentials.
- `create_payroll_run_retry_link` creates a browser link to retry an eligible frozen payroll revision with one-off HMRC credentials.
- `create_payroll_run_reconciliation_link` creates a browser link to resume checks on an uncertain submission using the original sender’s password.
- `list_payroll_runs` lists payroll runs and their states.
- `get_payroll_run` returns one run with its saved payments and calculation.
- `preview_payroll_run` calculates a draft or reopened run without saving results.
- `get_payroll_run_history` returns retained revisions, attempts and outcomes.
- `list_tax_year_rollovers` lists a PAYE scheme's rollovers.
- `get_tax_year_rollover` returns current progress and recorded decisions.
- `get_tax_year_rollover_history` returns attempts and outcomes for both stages.
- `cancel_tax_year_rollover` cancels an eligible rollover while retaining its history and source tax year.
- `resume_tax_year_rollover_polling` resumes paused status checks for the existing final FPS or new-year EPS attempt.

The shared skill combines standalone businesses and practice clients for general
business discovery. It keeps practice roles separate from business operational
roles and identifies partial results if a practice lookup fails. It also routes
standalone and practice-client creation, and explains how to handle uncertain
outcomes without automatically creating duplicate businesses.

The members skill distinguishes standalone business access from practice
membership, and pending invitations from current members. Member and outgoing
invitation listings require the relevant admin role. Received invitation tools
use the authenticated recipient and do not require membership of the inviting
business or practice.

The billing skill distinguishes payroll agreement status from billing suspension,
and standalone subscriptions from practice client enablement. It also explains
invoice pagination, saved payment statuses and client charge breakdowns. Four
additional tools read payment setup live from Stripe. All ten billing tools
require the relevant admin role. Payment methods, agreement status and
suspension remain separate facts.

The payroll-setup skill helps select or create schemes and schedules within the
chosen business, using IDs to match schedules to their schemes. It explains
required settings, duplicate employer references and uncertain creation outcomes.
It also covers practice HMRC reporting details, which any practice member can read.

The employees skill distinguishes people from their employments, matches them
by ID and helps interpret stored settings without calculating payroll. It also
guides employee creation and personal-detail updates, including field clearing,
duplicate creation and payroll-history restrictions. Employment onboarding
guidance covers explicit loan declarations, P45/checklist evidence and the
server-resolved initial tax treatment. Employment update guidance covers partial
edits, stored defaults and restrictions after payroll or an HMRC notice. Notice
guidance explains cumulative amounts, basis changes and effects on live previews.

The payroll skill guides draft creation, including automatic employment inclusion,
copied pay and hours, and duplicate risks after uncertain outcomes. It explains
payment overrides, omitted fields, version changes and preservation of employment
defaults and saved revisions. Inclusion guidance distinguishes adding an employment
from re-adding it after exclusion, which copies current defaults. Discard guidance
covers deletion of an entire draft, reviewed versions and preservation of history.
Reopening guidance distinguishes corrections from retries and requires all
submission attempts to be resolved before the run can be edited again.
Cancellation guidance distinguishes stopping a run from deleting a draft or
withdrawing an HMRC submission, and explains which payment inputs are returned.
Polling recovery guidance distinguishes resuming status checks from sending
a new submission, and explains saved delays and background outcomes.
The skill also helps select a run and distinguish live previews, saved calculations
and historical submissions. Submission guidance covers same-account browser
confirmation, expiring links, reviewed versions and uncertain outcomes. The user
enters credentials directly on the Opsd page; creating a link does not submit.
Retry guidance preserves frozen inputs and distinguishes safe retries from
reopening for corrections or recovering an uncertain submission. Reconciliation
guidance resumes the existing attempt without resending payroll.

The tax-year-rollovers skill distinguishes final FPS and new-year EPS progress,
retained cancelled operations and submission retries. It supports reading status
and history, explicit cancellation and paused polling recovery using reviewed
versions. Polling can advance or complete a rollover and apply its saved next-year
settings. Starting, retrying and credential-based recovery are not yet supported.

There are fifty-seven tools: thirty-five read-only tools, ten creation tools,
eleven update tools and one deletion tool.
OAuth requests `api:read`, `api:write`, and `hmrc:submit`. On the consent page,
the user can approve any nonempty subset of these independent permissions. Lookups
require `api:read`; payroll submission and retry links require `hmrc:submit`;
rollover polling recovery requires both `api:write` and `hmrc:submit`; other
creation, updates and deletion require `api:write`. Write alone permits those
operations when the required inputs are known. Submit alone permits a submission
link when its IDs and reviewed version are known. Opserver enforces the
granted scopes alongside the user's existing membership and role permissions.

The listing's Read and Write capabilities describe the available tools; the
token's granted scopes determine which operations it can perform. OAuth endpoints
and CIMD support are discovered from Opserver; credentials are not packaged.

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
