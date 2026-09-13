---
name: openclips
description: >-
  Entry point for OpenClips, which makes ad creative (image ads, videos,
  creator clips) from a brand's product catalogue via the OpenClips MCP
  server. Connects, picks the workspace, finds products, brands and
  creatives, applies the shared spending, waiting and safety rules, and
  routes each request to the right OpenClips skill. Use when: "OpenClips",
  "what can OpenClips do", "which workspace am I in", "show my products",
  "list my creatives", "what is this creative", "launch my campaign"
  (answered: OpenClips makes creative, not ad delivery). NOT for: image
  ads (openclips-image-ads), video ads (openclips-video-ads), creator,
  cinematic or paper films (openclips-clips), editing a creative or its
  copy (openclips-edit), products or brand setup (openclips-brand-intel),
  recreating a competitor's ad (not offered), listing, software or
  store ads (openclips-real-estate, openclips-saas-explainer,
  openclips-ecommerce), folders or API code (openclips-api), hooks,
  scripts and test ideas (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server at https://mcp.openclips.ai/mcp, connected and signed in.
---

# OpenClips

OpenClips makes advertising creative from a brand's product catalogue: static image ads, marketing videos, creator-led clips, and edits of creatives that already exist. It does **not** run ads. It produces the files, and the user publishes them in their own ads manager.

This skill is the entry point. It finds the OpenClips tools, the workspace and the products, applies the rules every OpenClips request shares, and routes the work to the skill or server playbook that does it. The server's deep instructions are read with `openclips:load_skill`.

## 1. Find the OpenClips tools

This pack writes every tool as `openclips:<tool>`. Your host names them according to how OpenClips was connected, for example `mcp__openclips__list_skills`, `mcp__plugin_openclips_openclips__list_skills` or `mcp__claude_ai_OpenClips__list_skills`. Match on the part after the last `__` or `:`, and use the OpenClips tool with that name. Never invent a prefix.

Some hosts list tools by name only until they are loaded. Before deciding OpenClips is missing, search your tools for one whose name ends in `list_my_workspaces`.

- **No OpenClips server at all:** before answering anything else, read `references/connect.md` and reply with the install step for this host (Claude Code: `/plugin marketplace add https://github.com/openclips/skills`, `/plugin install openclips@openclips`, then `/mcp` to sign in). Do not describe what OpenClips can do and do not offer to check a workspace; there is none until the server is connected.
- **The server is there but not signed in** (the host says it needs authentication, or shows it with no tools): tell the user to open `/mcp`, choose OpenClips and authenticate, or reconnect it in claude.ai connector settings. Do not reinstall, and do not retry in a loop.
- **More than one server exposes OpenClips tools:** prefer the one named exactly `openclips` or `OpenClips`. If that does not settle it, ask the user which to use.

Never fall back to calling the OpenClips REST API yourself. The server also serves a playbook named `openclips`, written as the in-app agent's persona; do not load it, because this skill takes its place.

## 2. Pick the workspace

- Call `openclips:list_my_workspaces` once per session and reuse the answer.
- One workspace: use it. Several: ask which, by name.
- `tokenBalance` is the credit balance. `hasMetaConnection` means nothing here, because OpenClips neither reads nor runs campaigns.

## 3. Find what the user means

- **Products:** `openclips:list_products`, `openclips:get_product`, or `openclips:get_product_by_url` for a URL.
- **Brands:** `openclips:list_brands`, `openclips:get_brand`. Brands can be read but never created or edited, here or in the app; a brand is matched or created automatically when a product is added. Skip any playbook step that creates or edits one.
- **Creatives:** `openclips:list_creatives`, `openclips:get_creative`. **Avatars:** `openclips:list_avatars`, `openclips:get_avatar`.
- Refer to products, creatives and brands as `#ID (name)`. Never guess an id; when several things match, ask, naming them.

## 4. Route the request

| The user wants | Go to | Playbooks behind it (load them yourself if that skill is not installed) |
|---|---|---|
| A new image ad | `openclips-image-ads` | `generate-marketplace-proxy-image`; `generate-image-templates` for a preset style |
| A new video ad from a model, with no presenter | `openclips-video-ads` | `generate-marketplace-proxy-video` |
| A person on screen (creator, testimonial, unboxing), a cinematic commercial, a paper-collage film, or one film in several languages | `openclips-clips` | `clips` |
| An explainer or app-demo video for a software product | `openclips-saas-explainer` | `clips` |
| Ads for a property listing | `openclips-real-estate` | `generate-property-video` |
| Ads across a store's catalogue | `openclips-ecommerce` | `generate-image-templates` |
| To change an existing creative (size, language, sharpness, background, variations) or write its ad copy | `openclips-edit` | `revise-creative-other`, `revise-creative-variate`, `enhance-asset`, `generate-ad-copy` |
| Their own version of a competitor's ad | not offered: say so, and offer a new ad from their own brief through `openclips-image-ads` | none |
| To add or update a product, or "set up my brand" | `openclips-brand-intel` | `create-product`, `update-product` |
| Folders, any endpoint no skill covers, or OpenClips from their own code | `openclips-api` | `creative-folders` for folders |
| Hooks, scripts, storyboards, test ideas, or copy with no creative to attach it to | `openclips-ad-craft` | none |
| To know what something is | stay here | `identify-entity` |
| To launch, pause, budget, target or report on ads | stay here | none. Say plainly that OpenClips makes the creative and the user publishes it in their own ads manager |
| Anything else OpenClips cannot do (organic posts, audiences, billing, users) | stay here | `unsupported-features`, ignoring its pointers to campaign, pixel or Advertise screens |

When two rows fit, the more specific one wins: a software product goes to `openclips-saas-explainer`, a listing to `openclips-real-estate`, a whole catalogue to `openclips-ecommerce`.

## 5. Playbooks, and which rule wins

The playbooks were written for the OpenClips app's own agent. Follow their validation rules, defaults and field names over your own judgement, with four exceptions:

- When a playbook names an approval block, a form, a selection widget or a tool this server does not list, do the same thing in plain text: ask the question, or write the gate in section 6.
- Skip any step that creates or edits a brand.
- Where a playbook shows prices while a model is being chosen, or labels a request expensive, section 6 wins.
- Where a playbook's list or card rules differ from section 8, section 8 wins.

Load the specific playbook first. Load `creative-generation` when that playbook refers to it.

## 6. Spending credits

- Aim for the best result first. Use the model, resolution and duration the playbook recommends, and never downgrade any of them to save credits unless the user asks.
- Do not estimate, compare or comment on cost while planning, briefing or choosing a model. If the user asks what something costs, get the number from the matching `preview_cost` route; never quote a remembered price.
- Every credit-spending call passes this gate exactly once:
  1. Build the exact body you will send.
  2. Preview it: call the matching `…/preview_cost/` route with `openclips:call_api` and the same body.
  3. Show the cost and the balance as two separate numbers, list every field of the body under its exact key, and end with "Proceed?".
  4. Send only after an explicit yes in a later message, given after the user has seen that preview. A yes given before the preview is not consent.
  5. Send the same body. If the body changes for any reason, preview it again and ask again.
- For several calls at once: one confirmation listing each previewed call with its own cost, the total and the balance. One yes covers exactly the listed calls. One kind of call per confirmation, and at most ten.
- Some spend routes have no preview, for example retrying a failed creative, training or retraining an avatar, and rendering a video-project scene. An Image or Video Agent run is charged after it delivers, so its preview is an estimate. For these, say plainly that the exact cost cannot be shown in advance, say what will be billed, and still wait for an explicit yes.
- Writing ad copy onto an existing creative costs nothing and needs no preview.
- If the preview says the balance is insufficient, stop and say so.
- A clips job in `awaiting_approval` is alive and holding credits. Report it and never resubmit.

## 7. Waiting for results

- `openclips:wait_for_creative` waits about twenty seconds. If it returns `stillProcessing: true`, call it again; that is expected for videos. Stop and report when the creative's `actionStatus` is `awaiting_approval` or a failure. Hosts that show a live OpenClips card update it themselves, so there you may stop after the first wait.
- `openclips:await_product`: `pending_product_timeout` means wait again with the same correlation id; `pending_product_failed` is final, so report it.
- While waiting, one short status line is enough. Do not narrate each check.

## 8. Showing results

- Lead with what was made, then show it. Embed images as markdown images and link videos as plain links, because inline video rarely renders in chat. Offer to save the files locally.
- Do not paste raw JSON. In results, turn enum values into plain words (`humanise-labels` covers the cases). At the gate, keep exact field keys.
- Some hosts render product, creative and brand lists as a card. When yours does, write one short summary line and do not retype the rows. When it does not, show a table of at most twenty rows.
- Reply in the user's language. Tool arguments stay exactly as the API expects them.
- After a result, stop. Offer one next step at most.

## 9. When something goes wrong

- **A spend call that timed out has not necessarily failed.** The server may have finished it after the client stopped waiting. Re-read with `openclips:list_creatives` or `openclips:get_creative` first. If you retry, send the identical body: the server then returns the original result, or `409 request_in_flight` while it still runs, instead of charging twice. Never change a timed-out request and send it as new.
- **A failure the server reports definitely:** do not resend the same input. Say what failed and suggest one change that keeps the quality default.
- **Deleting anything** (a product, creative, folder or avatar) needs the user to name the item and confirm in a later message.
- For any other message, read `references/errors.md`. When the user's words and the API's differ, read `references/terminology.md`.

## Load on demand

- `references/connect.md`: connecting OpenClips on each host. Read it when no OpenClips server is found, or sign-in fails.
- `references/errors.md`: the server's error and refusal messages, and what each one means. Read it when a call fails or is refused.
- `references/terminology.md`: the user's words against the API's, including which avatar value each field takes. Read it when a field or a term is unclear.
