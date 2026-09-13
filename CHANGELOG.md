# Changelog

All notable changes to this pack. The format follows Keep a Changelog, and the pack uses semantic versioning: a patch for wording and fixes, a minor for a new skill or install path, a major for renaming or removing a skill or changing the server name.

## [Unreleased]

## [0.2.0] - 2026-09-13

### Removed
- `openclips-competitor-recreate`. Recreating a competitor's ad is no longer offered by this pack; the hub says so and offers a new ad from the user's own brief. Removing a skill is a breaking change, hence the minor bump before 1.0.

## [0.1.2] - 2026-09-13

### Fixed
- With no OpenClips server connected, the hub now gives the install steps first instead of describing capabilities and offering to check a workspace that is not there.
- The Codex, Cursor and generic install commands are non-interactive: `npx skills add openclips/skills -y --skill '*' --agent <name>`. The bare form stops at a selection prompt.
- `openclips-api` never fetches the developer guides; it gives the links.

## [0.1.1] - 2026-09-13

### Changed
- The eval unit tests use a placeholder host; no development hostname ships in the public tree.

## [0.1.0] - 2026-09-12

First release: the hub, six capability skills, three verticals, the API skill and the craft skill.

### Added
- `openclips`, the hub skill: connecting, workspace and product resolution, the spending and waiting rules, and routing.
- Six capability skills: `openclips-image-ads`, `openclips-video-ads`, `openclips-clips`, `openclips-edit`, `openclips-catalog-setup`, `openclips-competitor-recreate`. Each is a thin router over the server's own playbooks; models, lanes, prices and enums are read live.
- Three verticals: `openclips-real-estate`, `openclips-saas-explainer`, `openclips-ecommerce`.
- `openclips-api`: the escape hatch through `list_endpoints` and `call_api`, folders, the removal confirmation, and the developer path with a personal access token against `api.openclips.ai`.
- `openclips-ad-craft`: hooks, beat maps, storyboards, creator briefs, test plans and reviews. Names no model and calls no tool.
- Plugin manifests for Claude Code, Codex and Cursor. The Claude Code and Cowork plugin registers the OpenClips MCP server on install.
- Install guides for people and for agents.
- An eval harness (`evals/`) that runs every skill against the development server with spend tools withheld.
- A pack lint, a dev-to-public sync, and one script that runs every gate locally (`scripts/check.sh`); there is no CI.
