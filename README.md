# OpenClips skills

Agent skills that teach Claude, Codex and Cursor to make advertising creative with [OpenClips](https://openclips.ai): image ads, marketing videos and creator-led clips, all from your product catalogue. OpenClips produces the files; you publish them in your own ads manager.

The skills are thin by design. They connect to the OpenClips MCP server, pick the right tool or lane, apply the shared spending and safety rules, and load the server's own playbooks for the deep steps. Models, prices, lanes and formats are always read live, so the pack does not go stale when the catalogue moves.

## Install

Two things have to be true: the skills are installed, and the OpenClips MCP server at `https://mcp.openclips.ai/mcp` is connected and signed in. Signing in always happens in the browser. Name the server `openclips` everywhere, so tool names come out the same on every host.

| Host | Steps |
|---|---|
| Claude Code | `/plugin marketplace add https://github.com/openclips/skills`, then `/plugin install openclips@openclips`, then `/mcp` to sign in. The plugin installs the skills and registers the server together. |
| Cowork | Customize, then Plugins: add the marketplace `openclips/skills`, install `openclips`, and sign in when prompted. |
| Codex | `codex mcp add openclips --url https://mcp.openclips.ai/mcp` (sign-in opens at once), then `npx skills add openclips/skills -y --skill '*' --agent codex`. |
| Cursor | Add `"openclips": {"url": "https://mcp.openclips.ai/mcp"}` under `mcpServers` in `~/.cursor/mcp.json`, then `npx skills add openclips/skills -y --skill '*' --agent cursor`. |
| claude.ai chat | Customize, then Connectors: add a custom connector named `OpenClips` with the URL above. Chat gets the server only; plugins and skills do not load there. |

Skills-only installs (`npx skills add openclips/skills -y --skill '*' --agent '*'`, or `gh skill install openclips/skills --all --agent claude-code --scope user`) copy the skills and do not add the server. Full details, including what to do when sign-in fails, are in [INSTALL.md](INSTALL.md). Pointing an agent at [INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md) lets it install and verify the pack itself.

## Skills

| Skill | What it does |
|---|---|
| [`openclips`](skills/openclips/SKILL.md) | The entry point. Connects, picks the workspace, finds products and creatives, applies the spending rules, and routes to the other skills. |
| [`openclips-image-ads`](skills/openclips-image-ads/SKILL.md) | New static image ads: a marketplace model by default, the template lane for one look across sizes, the beta Image Agent for a hands-off brief. |
| [`openclips-video-ads`](skills/openclips-video-ads/SKILL.md) | New video ads from a marketplace video model, with no presenter on screen, and the beta Video Agent. |
| [`openclips-clips`](skills/openclips-clips/SKILL.md) | Creator, testimonial, per-language, two-voice, cinematic and paper-collage films on the clips lanes, catalogue first. |
| [`openclips-edit`](skills/openclips-edit/SKILL.md) | Change a creative that exists: size, language, resolution, variations, signal-level clean-ups, ad copy, watermark. |
| [`openclips-catalog-setup`](skills/openclips-catalog-setup/SKILL.md) | Import a product from its URL or photos, create one by hand, keep it current. Brands come with products. |
| [`openclips-real-estate`](skills/openclips-real-estate/SKILL.md) | Listing ads for agents: a 30-second property video from the listing, listing images, photo clean-ups. Every claim comes from the listing. |
| [`openclips-saas-explainer`](skills/openclips-saas-explainer/SKILL.md) | Explainer and app-demo videos for software products on the paper-collage and presenter-plus-screens lanes. |
| [`openclips-ecommerce`](skills/openclips-ecommerce/SKILL.md) | Ads across a store's catalogue: one look per product in every channel size, creator videos for hero products, localised variants, batched honestly. |
| [`openclips-api`](skills/openclips-api/SKILL.md) | Any endpoint: the escape hatch through `list_endpoints` and `call_api` (folders, deleting, video projects), and the developer path with a personal access token against `api.openclips.ai`. |
| [`openclips-ad-craft`](skills/openclips-ad-craft/SKILL.md) | How to make ads that work, before anything is rendered: hooks, beat maps, storyboards, creator briefs, test plans, reviews. Names no model, calls no tool. |

What changed in each release is in [CHANGELOG.md](CHANGELOG.md). See [CHANGELOG.md](CHANGELOG.md).

## How spending works

Before anything is charged, the skills preview the exact request with the server's own price check where the server can quote one, show the cost and your balance, say so plainly when a route cannot be priced in advance, and wait for your explicit yes. Nothing in this pack spends credits on its own.

## Contributing

Pull requests are welcome under the rules in [CONTRIBUTING.md](CONTRIBUTING.md) and are reviewed by the maintainer. `scripts/check.sh` runs every gate: the [Agent Skills specification](https://agentskills.io/specification), Claude Code's plugin validator, GitHub's skill publish preflight, a secret scan, and this pack's own lint. Security reports go to the address in [SECURITY.md](SECURITY.md).

## Licence

MIT. See [LICENSE](LICENSE).
