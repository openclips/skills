# Changelog

All notable changes to this pack. The format follows Keep a Changelog, and the pack uses semantic versioning: a patch for wording and fixes, a minor for a new skill or install path, a major for renaming or removing a skill or changing the server name.

## [Unreleased]

## [0.4.0] - 2026-11-10

The server moved a long way since 0.3.1 and the pack had not: six tools it named were gone, eleven playbooks it routed to were no longer served, and most of what the server added was never mentioned. This release brings every skill back in line with the server, and adds the gate that keeps it there.

### Added
- `scripts/server_surface.json`: the tools and playbooks the server lists for an ordinary account, and which tools only read. The pack lint fails on any tool or playbook a skill names that is not in it, and before a release on a copy that is old or that `scripts/snapshot_server.py` did not write.
- The hub runs the video jobs the server added: a reel from the user's footage or from a script written first, a finished video's package, and it routes playable ads, faceless stories and custom avatars to their playbooks.
- `openclips-saas-explainer` opens the presenter tutorial job.
- `openclips-edit` covers the one-file video tools (trim, reframe, rotate, sound), exact words on a video and joining clips.
- `openclips-image-ads` and `openclips-ecommerce` make marketplace listing sets.
- A file the user holds is uploaded through the server's upload panel; every skill that said there was no upload step now says how.

### Changed
- **Image ads start at the server's presets.** A marketplace model is used when the user names one, writes the whole picture, or wants a picture that promotes nothing. The template lane and the Image Agent route are gone from the server and from the pack.
- **Prices come from the price tool.** Every gate calls `openclips:preview_cost` and sends through what its quote names; the server refuses a price route sent through `openclips:call_api`.
- **The gate follows the server's consent rule**, including its one exception: a request that already approved the spend in so many words, or gave a budget the quote fits. The exception covers one call of that request, never a batch.
- A change to an existing image (another frame, another language, a worded change, variations) is an image edit on the marketplace image tool; the revise tools are gone from the server.
- A reel, a TikTok or a Short where someone talks and sells starts with its script, before any lane or model.
- Every prompt sent to an image or video model goes through the server's preflight playbook first.
- The property video has no playbook any more: its route's own validation, read at the free price check, is the contract.
- The eval runner withholds every tool the server does not mark read-only, read from the snapshot, instead of a hand-kept list of spend tools.

### Removed
- Ad copy for an existing creative: the route is gone from the server.
- The Video Agent route: closed on this server.

## [0.3.1] - 2026-09-13

### Changed
- The public repository carries no history: each release is one commit, and only the current tag and release are kept. `CONTRIBUTING.md` says so.

## [0.3.0] - 2026-09-13

### Changed
- `openclips-catalog-setup` is renamed `openclips-brand-intel`. Same job: get products into the workspace and keep them current; brands come with products. A rename is a breaking change for anyone invoking the skill by name, hence the minor bump before 1.0.

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
- Six capability skills: `openclips-image-ads`, `openclips-video-ads`, `openclips-clips`, `openclips-edit`, `openclips-brand-intel`, `openclips-competitor-recreate`. Each is a thin router over the server's own playbooks; models, lanes, prices and enums are read live.
- Three verticals: `openclips-real-estate`, `openclips-saas-explainer`, `openclips-ecommerce`.
- `openclips-api`: the escape hatch through `list_endpoints` and `call_api`, folders, the removal confirmation, and the developer path with a personal access token against `api.openclips.ai`.
- `openclips-ad-craft`: hooks, beat maps, storyboards, creator briefs, test plans and reviews. Names no model and calls no tool.
- Plugin manifests for Claude Code, Codex and Cursor. The Claude Code and Cowork plugin registers the OpenClips MCP server on install.
- Install guides for people and for agents.
- An eval harness (`evals/`) that runs every skill against the development server with spend tools withheld.
- A pack lint, a dev-to-public sync, and one script that runs every gate locally (`scripts/check.sh`); there is no CI.
