# Contributing

Thank you. This pack is generated from a private development repository, so a pull request here is reviewed, then ported and released from there. Small fixes land quickly; new skills need a short discussion first, using the skill request template.

## Rules every skill follows

- **Frontmatter uses only the six Agent Skills fields**: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. No other key, because the spec validator rejects them. This pack sets `name`, `description`, `license: MIT` and `compatibility`, and never sets `allowed-tools`.
- **`name` equals the directory name**, starts with `openclips-` (the hub alone is `openclips`), and contains neither `anthropic` nor `claude`.
- **The description is a routing contract.** Third person, at most 1024 characters, with the literal `Use when:` followed by the phrases a user actually says, and the literal `NOT for:` naming the sibling skill that owns each excluded case.
- **Thin by design.** The body stays under 300 lines and routes into the server's playbooks with `openclips:load_skill`. Tables and matrices live in `references/`, one level deep, each linked from the skill with a note on when to read it.
- **Tools are written `openclips:<tool>`.** Never a bare tool name and never a host-specific prefix.
- **No volatile facts.** No model names, prices, lane lists or enum values in a skill body. Those come from `openclips:marketplace_models`, `openclips:clips_catalog`, `openclips:list_endpoints` and the playbooks at run time.
- **Public-safe.** No real people, no client or customer brands, no text derived from third-party material, no internal details, no secrets. Examples use invented brands.

## Before opening a pull request

1. Write the skill's eval cases first, at least three, in `evals/cases/`.
2. Validate: `uvx --from skills-ref agentskills validate skills/<name>`.
3. Run every gate locally: `scripts/check.sh`. It is the source of truth; there is no CI. The maintainer runs the same script before merging.
4. Fill in the pull request template. Its checklist covers what a machine cannot check.

## Requesting a new skill

Open a skill request issue. The one question that decides it: why is this a separate skill rather than a row in an existing one? If it fits an existing skill, it should go there.

## How pull requests land

This repository is generated from a private development repository on each release, so nothing is merged here directly. A pull request is reviewed here by the maintainer, then ported upstream and shipped in the next release with credit in `CHANGELOG.md`; that way a merged change is never lost to the next sync. Expect a reply on the pull request rather than a merge button. The maintainer merges only the `release/<tag>` branches into `main` here.
