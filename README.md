# Opsd plugins

Shared skills, assets and provider packaging for Opsd.
The only provider currently implemented is OpenAI (ChatGPT and Codex).

Opserver handles authentication, permissions and business operations. These
packages connect to its existing MCP server.

## Install in Codex

[Install Opsd in the ChatGPT desktop app](https://docs.opsd.sh/install-plugin/#add-the-plugin).

From the Codex CLI, run:

```sh
codex plugin marketplace add opsd-sh/opsd-plugins
codex plugin add opsd@opsd
```

To ask Codex to do the installation for you, paste this into a Codex chat:

> Install the Opsd plugin from the opsd-sh/opsd-plugins GitHub marketplace
> using the Codex CLI, then help me connect my Opsd account.

Start a new Codex chat after installing.

## Source layout

```text
.agents/plugins/marketplace.json          Codex marketplace catalogue
plugins/opsd/.codex-plugin/plugin.json    Production plugin manifest
plugins/opsd/.mcp.json                    Production MCP connection
plugins/opsd/skills/                      Shared skills and their reference files
plugins/opsd/assets/icon.svg              Shared Opsd icon
production.json                           Production build settings
scripts/build.py                          Shared packaging script
tests/test_build.py                       Packaging checks
```

Codex installs `plugins/opsd/` directly from the repository. The ZIP build
and the private `opsd-plugins-dev` build read the skills and icon from that
same directory.

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

Links within the plugin’s `skills/` and `assets/` are copied as ordinary files and directories.
Links to excluded content are also excluded. Links outside those directories,
broken links and directory cycles fail the build, leaving the previous package
in place.

The MCP server key matches the configured plugin name. Production uses `opsd`;
environment variants use their own names so their client-side connections remain
distinct when installed together.

The OpenAI package uses the Codex compatibility format already tested with
Codex CLI 0.167.0. That version discovered the manifest but not the MCP connection
when we previously tried the portable root `plugin.json` / `mcp.json` format.

## Production downloads

Run the **Release** workflow manually to test and build the production ZIP for
inspection in the `openai-plugin` Actions artifact. To publish, push an annotated
tag such as `v0.1.6` on the release commit. The tag must match the three-part
version in `plugins/opsd/.codex-plugin/plugin.json`.

The workflow uploads `opsd.zip` to
`https://downloads.opsd.sh/plugins/openai/releases/<tag>/opsd.zip`.
The customer download at `https://downloads.opsd.sh/plugins/openai/opsd.zip`
serves the highest published version. Rerunning the same tag reuses its original
ZIP. The AWS role and download destinations belong to the production downloads
Terraform stack in `opsd-sh/infra`.

## Test a local build

This package connects to production. Use the private development repository for
development accounts and data.

```sh
codex plugin marketplace add ./dist/openai
codex plugin add opsd@opsd
```

Restart Codex desktop or start a fresh CLI session after installation. Building
does not install the package, register a marketplace or publish anything.

In development, Codex desktop has been used to run payroll for a standalone
business and a practice client, including browser confirmation and retry after
an HMRC rejection. Signed-in production testing is pending a production user.

## Tools and authentication

- `create_business` creates a standalone business with the connected user as admin.
- `create_practice` creates a practice with its HMRC reporting identity and the connected user as admin.
- `create_practice_business` creates a client owned by an existing practice, requiring practice admin membership.
- `list_businesses` lists standalone businesses where the user has direct membership.
- `get_business` looks up a business by its public ID, including access through a practice.
- `list_practices` lists practices and the user's role in each.
- `get_practice` looks up a practice by its public ID.
- `get_practice_hmrc_reporting` reads its stored HMRC reporting identity and contact details.
- `replace_practice_hmrc_reporting` replaces those details, requiring practice admin membership. Omitted optional fields are cleared.
- `list_practice_businesses` lists the businesses owned by a practice.
- `list_business_members` and `list_practice_members` list user accounts and roles.
- `update_business_member` and `update_practice_member` change an existing member’s role, requiring the relevant admin role and preserving at least one admin.
- `remove_business_member` and `remove_practice_member` remove existing memberships, requiring the relevant admin role and preserving at least one admin.
- `create_business_invitation` and `create_practice_invitation` create pending invitations with an explicit role and queue an email, requiring the relevant admin role.
- `cancel_business_invitation` and `cancel_practice_invitation` cancel open outgoing invitations, including expired ones, requiring the relevant admin role.
- `accept_business_invitation` and `accept_practice_invitation` join through an invitation addressed to the connected account, using its offered role.
- `decline_business_invitation` and `decline_practice_invitation` turn down an invitation addressed to the connected account without changing memberships.
- `list_outgoing_business_invitations` and `list_outgoing_practice_invitations`
  list pending, unexpired invitations sent by the business or practice.
- `list_business_invitations` and `list_practice_invitations` list pending,
  unexpired invitations received by the connected account.
- `get_business_payroll_subscription` reads a standalone business's payroll agreement and suspension.
- `subscribe_business_to_payroll` starts or restarts a standalone payroll agreement after checking the reviewed version and payment setup.
- `cancel_business_payroll_subscription` cancels a standalone payroll agreement immediately, checking the reviewed version and retaining billing history.
- `get_practice_business_payroll` reads a practice client's payroll enablement and shared suspension.
- `enable_practice_business_payroll` starts or restarts payroll for one client after checking its reviewed version, owning practice and practice payment setup.
- `disable_practice_business_payroll` stops payroll for one client immediately while retaining history and leaving other clients unchanged.
- `list_business_invoices` and `list_practice_invoices` page through saved invoice summaries.
- `list_business_invoice_lines` and `list_practice_invoice_lines` page through saved charges by business.
- `get_business_billing_status` and `get_practice_billing_status` check the current default payment method at Stripe.
- `list_business_payment_methods` and `list_practice_payment_methods` read live saved methods and safe card summaries.
- `set_business_default_payment_method` and `set_practice_default_payment_method` select an attached payment method as the payer’s invoice default, requiring the relevant admin role.
- `create_paye_scheme` records a PAYE scheme and its initial tax-year settings within a business.
- `create_pay_schedule` creates a monthly schedule under a scheme in that business.
- `list_paye_schemes` lists a business's PAYE schemes and recorded settings.
- `list_pay_schedules` lists its schedules, frequencies and PAYE scheme IDs.
- `create_employee` creates a person’s record within a business.
- `update_employee` changes personal details while preserving payroll-history restrictions.
- `list_employees` and `get_employee` return employee personal details.
- `create_employment` links an employee to a scheme and schedule and resolves initial tax settings from supplied starter evidence.
- `update_employment` changes payroll defaults or starter evidence while preserving payroll-history and tax-code-notice restrictions.
- `discard_employment` deletes an unused employment and its opening balances after removal from all drafts and before its first finalised payment.
- `get_employment_payroll_import` reads the saved external payroll figures.
- `amend_employment_payroll_import` corrects them before the first finalised payroll for the employment.
- `apply_employment_tax_code_notice` records a received notice without replacing starter evidence or saved payroll history.
- `list_employments` and `get_employment` return linked employment records and
  stored payroll settings.
- `create_payroll_run` creates a draft and copies the schedule’s eligible employments and payment defaults.
- `update_payroll_run_payment` changes gross pay, working-hours band or the AL director’s final-payment decision on an included draft payment.
- `include_payroll_run_employment` adds an employment with current payment defaults, preserving an existing payment when already included.
- `exclude_payroll_run_employment` removes an employment's payment and overrides from a draft or reopened run.
- `download_payslip` returns a private, expiring PDF download for one employment in an HMRC-accepted run.
- `request_payslip_export` queues a whole accepted run as a ZIP. Use `get_payslip_export` to check progress and retrieve its expiring download link.
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
- `create_tax_year_rollover_submission_link` creates browser approval to start the supported year-end transition with an explicit allowance choice and coding notices.
- `create_tax_year_rollover_reconciliation_link` creates a same-account browser approval for recovering an existing attempt, including automatic EPS continuation after FPS acceptance.
- `create_tax_year_rollover_retry_link` creates browser approval to retry an eligible final FPS or new-year EPS using the saved decisions.
- `create_tax_year_rollover_eps_submission_link` creates browser approval to send the new-year EPS when the final FPS is accepted and the rollover is waiting for credentials.

The shared skill combines standalone businesses and practice clients for general
business discovery. It keeps practice roles separate from business operational
roles and identifies partial results if a practice lookup fails. It also routes
practice, standalone and practice-client creation, and explains how to handle
uncertain outcomes without automatically creating duplicate records. Practice
creation distinguishes the display name from the HMRC reporting identity.

The members skill distinguishes standalone business access from practice
membership, and pending invitations from current members. Member and outgoing
invitation listings require the relevant admin role. Received invitation tools
use the authenticated recipient and do not require membership of the inviting
business or practice. The two invitation creation tools require Write and the
relevant admin role. The skill explains role selection, practice-wide access,
queued email delivery, conflicts, expiry and uncertain outcomes. Cancellation
guidance distinguishes withdrawing an invitation from removing a member, and
keeps retries tied to the exact invitation ID. Acceptance requires Write and
recipient matching, with no existing membership requirement. Its guidance
explains offered roles, practice-wide access and uncertain outcomes. Decline
guidance separates rejecting a received invitation from cancelling an outgoing
one or removing a member. Role-change guidance covers member IDs, the last-admin
guard, self-demotion, practice-wide access and uncertain outcomes. Removal
guidance covers self-removal, retained accounts and records, independent
memberships, and the risk of retrying after a user rejoins.

The billing skill distinguishes payroll agreement status from billing suspension,
and standalone subscriptions from practice client enablement. It also explains
invoice pagination, saved payment statuses and client charge breakdowns. Four
additional tools read payment setup live from Stripe, and two select a saved
method as the payer’s default. Four tools start or end standalone and practice
client payroll agreements. All sixteen billing tools require the relevant
admin role. Guidance covers monthly fees, immediate cancellation or disablement,
reviewed decision versions, client ownership, shared practice billing and
uncertain provider outcomes. Payment methods, agreement
status and suspension remain separate facts.

The payroll-setup skill helps select or create schemes and schedules within the
chosen business, using IDs to match schedules to their schemes. It explains
required settings, duplicate employer references and uncertain creation outcomes.
It also covers practice HMRC reporting details, which any practice member can read
and admins can replace. Replacement guidance explains field clearing and how to
preserve unchanged details during a partial change.

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
and history, new rollover approval, explicit cancellation, paused polling
recovery, browser reconciliation, retry and EPS submission. Starting requires a
reviewed scheme generation and explicit allowance and tax-code decisions;
existing rollover actions use reviewed versions. Starting or reconciling the
final FPS can automatically send the new-year EPS. EPS acceptance completes the
rollover and applies its saved next-year settings.

There are eighty-one tools: thirty-five read-only tools, nineteen creation tools,
twenty-four update tools and three deletion tools.
OAuth requests `api:read`, `api:write`, and `hmrc:submit`. On the consent page,
the user can approve any nonempty subset of these independent permissions. Lookups
require `api:read`; payroll submission and retry links require `hmrc:submit`;
rollover start, polling recovery, reconciliation, retry and EPS submission links require
both `api:write` and `hmrc:submit`; other creation, updates and deletion require
`api:write`. Write alone permits those
operations when the required inputs are known. Submit alone permits a submission
link when its IDs and reviewed version are known. Opserver enforces the
granted scopes alongside the user's existing membership and role permissions.

The listing's Read and Write capabilities describe the available tools; the
token's granted scopes determine which operations it can perform. OAuth endpoints
and CIMD support are discovered from Opserver; credentials are not packaged.

Version 0.1.6 includes guidance on payroll preparation, HMRC submission and
recovery, practice clients, membership and billing. Starter prompts use the
display name of the package, such as Opsd or Opsd Development.

The icon is the existing Opsd favicon from `www/public/favicon.svg`.

## Checks

```sh
make test
```

The checks cover self-contained packages, shared file reuse, content exclusions,
symlink handling, rebuilding, output protection and invalid configuration.
Increment the version in
`plugins/opsd/.codex-plugin/plugin.json` when releasing package changes.

See the [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins)
for the supported manifest and marketplace formats.
