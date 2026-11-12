---
name: openclips
description: >-
  Entry point for OpenClips, which makes ad creative (image ads, videos,
  reels) from a brand's product catalogue via the OpenClips MCP server.
  Connects, picks the workspace, finds products and creatives, applies
  the spending rules, routes each request to the right OpenClips skill,
  and runs what no other skill owns: reels, video packaging, playable
  ads, faceless stories, custom avatars. Use when: "OpenClips", "which
  workspace am I in", "show my products", "make me a reel", "turn my clip into a reel", "thumbnails for
  my video", "playable ad", "train an avatar", "launch my campaign"
  (answered: OpenClips makes creative, not ad delivery). NOT for: image
  ads (openclips-image-ads), a video ad from a model (openclips-video-ads),
  cinematic or paper films (openclips-clips), editing a creative
  (openclips-edit), products (openclips-brand-intel), listing, software or
  store ads (openclips-real-estate, openclips-saas-explainer,
  openclips-ecommerce), folders or API code (openclips-api), hooks and
  scripts (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server at https://mcp.openclips.ai/mcp, connected and signed in.
---

# OpenClips

OpenClips makes advertising creative from a brand's product catalogue: static image ads, marketing videos, reels, creator-led clips, and edits of creatives that already exist. It does **not** run ads. It produces the files, and the user publishes them in their own ads manager.

This skill is the entry point. It finds the OpenClips tools, the workspace and the products, applies the rules every OpenClips request shares, and routes the work to the skill or server playbook that does it. The server's deep instructions are read with `openclips:load_skill`.

## 1. Find the OpenClips tools

This pack writes every tool as `openclips:<tool>`. Your host names them according to how OpenClips was connected, for example `mcp__openclips__list_skills`, `mcp__plugin_openclips_openclips__list_skills` or `mcp__claude_ai_OpenClips__list_skills`. Match on the part after the last `__` or `:`, and use the OpenClips tool with that name. Never invent a prefix.

Some hosts list tools by name only until they are loaded. Before deciding OpenClips is missing, search your tools for one whose name ends in `list_my_workspaces`.

- **No OpenClips server at all:** before answering anything else, read `references/connect.md` and reply with the install step for this host (Claude Code: `/plugin marketplace add https://github.com/openclips/skills`, `/plugin install openclips@openclips`, then `/mcp` to sign in). Do not describe what OpenClips can do and do not offer to check a workspace; there is none until the server is connected.
- **The server is there but not signed in** (the host says it needs authentication, or shows it with no tools): tell the user to open `/mcp`, choose OpenClips and authenticate, or reconnect it in claude.ai connector settings. Do not reinstall, and do not retry in a loop.
- **More than one server exposes OpenClips tools:** prefer the one named exactly `openclips` or `OpenClips`. If that does not settle it, ask the user which to use.

Never fall back to calling the OpenClips REST API yourself.

## 2. Pick the workspace

- Call `openclips:list_my_workspaces` once per session and reuse the answer.
- One workspace: use it. Several: ask which, by name.
- `tokenBalance` is the credit balance. `hasMetaConnection` means nothing here, because OpenClips neither reads nor runs campaigns.

## 3. Find what the user means

- **Products:** `openclips:list_products`, `openclips:get_product`, or `openclips:get_product_by_url` for a URL.
- **Brands:** `openclips:list_brands`, `openclips:get_brand`. Brands can be read but never created or edited, here or in the app; a brand is matched or created automatically when a product is added. Skip any playbook step that creates or edits one.
- **Creatives:** `openclips:list_creatives`, `openclips:get_creative`. **Avatars:** `openclips:list_avatars`, `openclips:get_avatar`. **Voices:** `openclips:list_voices`.
- **A file the user holds** (a photo, a clip, a recording) is not in the workspace until it is uploaded: `openclips:upload_media` shows the user an upload panel, and `openclips:await_media_upload` returns the creative it became. A public link comes in with `openclips:import_creative_from_url`. A chat attachment never reaches the server by itself.
- Refer to products, creatives and brands as `#ID (name)`. Never guess an id; when several things match, ask, naming them.

## 4. Route the request

| The user wants | Go to | Playbooks behind it (load them yourself if that skill is not installed) |
|---|---|---|
| A new image ad, post, banner or story | `openclips-image-ads` | none for the presets; `generate-marketplace-proxy-image` for a model the user named |
| A new video ad from a model, with no presenter | `openclips-video-ads` | `generate-marketplace-proxy-video`, `prompt-preflight` |
| A cinematic commercial, two people talking, a paper-collage film, one film in several languages, or a creator film on a clips lane | `openclips-clips` | `clips` |
| A reel, a TikTok or a Short where someone talks and sells; or captions, cards and a recut of footage the user filmed | stay here, section 5 | `reel-maker`, `reel-recut` |
| A finished video packaged for where it is posted: title, description, chapters, thumbnails, covers | stay here, section 5 | `video-packaging` |
| A tutorial, explainer or app demo for a software product | `openclips-saas-explainer` | `presenter-explainer`, `clips` |
| Ads for a property listing | `openclips-real-estate` | none |
| Ads across a store's catalogue, or the listing images of a product | `openclips-ecommerce` | none |
| To change an existing creative (size, language, sharpness, background, variations, a trim, words on a video) | `openclips-edit` | `generate-marketplace-proxy-image`, `enhance-asset` |
| A playable ad for a game | stay here | `playable-ads` |
| A narrated story reel with no person on camera | stay here | `faceless-stories` |
| A custom avatar from photos of a real person | stay here | `create-avatar` |
| Their own version of a competitor's ad | not offered: say so, and offer a new ad from their own brief through `openclips-image-ads` | none |
| To add or update a product, or "set up my brand" | `openclips-brand-intel` | `create-product`, `update-product` |
| Folders, any endpoint no skill covers, or OpenClips from their own code | `openclips-api` | none |
| Hooks, scripts, storyboards, test ideas, or copy with no creative to attach it to | `openclips-ad-craft` | none |
| To know what something is | stay here | `identify-entity` |
| To launch, pause, budget, target or report on ads | stay here | none. Say plainly that OpenClips makes the creative and the user publishes it in their own ads manager |
| Anything else OpenClips cannot do (organic posts, audiences, billing, users) | stay here | `unsupported-features`, ignoring its pointers to campaign, pixel or Advertise screens |

When two rows fit, the more specific one wins: a software product goes to `openclips-saas-explainer`, a listing to `openclips-real-estate`, a whole catalogue to `openclips-ecommerce`. A format no row names may still have a playbook: call `openclips:list_skills` once and load the one whose description matches the ask.

## 5. Video jobs the server runs for you

Three whole jobs are handed to the OpenClips agent, which runs every step on a priced card. Ask first, all at once: `openclips:brief_questions` for the job's flow returns the questions still open; pass the answers on the job tool. Ask the user for a budget too.

| The job | Tool | Playbook, for planning it with the user |
|---|---|---|
| A reel from footage the user has: best takes, captions, cards, sound, an end card | `openclips:make_explainer_reel` | `reel-recut` |
| A reel with nothing filmed yet: the words come first | `openclips:check_script` on the script the playbook writes, then the footage, then the reel tool above | `reel-maker` |
| A presenter-led product tutorial | `openclips:make_presenter_tutorial` | `presenter-explainer` |
| A finished video's package | `openclips:make_video_package` | `video-packaging` |

- Get the user's files into the workspace first (section 3) and pass their ids.
- Read each reply with `openclips:wait_for_openclips_agent` and relay it. A reply that says it is parked is a long render: keep waiting with the same ids, and never tell the user to come back later.
- Answer a card (an approval with its price, a pick, a form) with `openclips:answer_openclips_agent`, and approve a priced card only after the user said yes. With a budget passed on the job, cards that fit it are approved for you; without one, the agent shows one budget card for the whole film.
- One job per chat. `openclips:stop_agent_turn` when the user says stop.
- With a shell, parts of a job can run on the user's machine for free: `diy-video-jobs` maps each step.

Anything bigger than one generation that no row covers can be handed over the same way with `openclips:ask_openclips_agent`. Each agent turn costs credits, as in the app.

## 6. Playbooks, and which rule wins

The playbooks were written for the OpenClips app's own agent. Follow their validation rules, defaults and field names over your own judgement, with four exceptions:

- When a playbook names an approval block, a form, a selection widget or a tool this server does not list, do the same thing in plain text: ask the question, or write the gate in section 7. A playbook that opens with a note on what its chat terms mean here has already told you how.
- Skip any step that creates or edits a brand.
- Where a playbook shows prices while a model is being chosen, or labels a request expensive, section 7 wins.
- Where a playbook's list or card rules differ from section 9, section 9 wins.

Load the specific playbook first. Load `creative-generation` when that playbook refers to it. Before any prompt goes to an image or video model, load `prompt-preflight` once and run it.

## 7. Spending credits

- Aim for the best result first. Use the model, resolution and duration the playbook recommends, and never downgrade any of them to save credits unless the user asks.
- Do not estimate, compare or comment on cost while planning, briefing or choosing a model. If the user asks what something costs, get the number from `openclips:preview_cost`; never quote a remembered price.
- Every credit-spending call passes this gate exactly once:
  1. Build the exact body you will send.
  2. Price it: `openclips:preview_cost` with the workspace, the family from the tool's own list and that body. It spends nothing, and a field the route does not read comes back as a free error naming the fields it does.
  3. Show `tokenCost` and `currentBalance` as two separate numbers, list every field of the body under its exact key, and end with "Proceed?". For a preset image, the short proposal the presets tool describes is this confirmation.
  4. Send only after an explicit yes given after the user has seen that quote. A yes given before the quote is not consent. The one exception is a request that already approved the spend in so many words ("go ahead", "no need to confirm", a budget): then send on a sufficient quote that fits it, and say what it cost. Wanting a creative is not approval, and an approval covers one call of the request it came with: several calls at once always wait for the confirmation that lists them.
  5. Send the same body through what the quote's `firedBy` names: the named tool, one exact route for `openclips:call_api`, or a refusal with its reason. If the body changes for any reason, price it again and ask again.
- For several calls at once: one confirmation listing each priced call with its own cost, the total and the balance. One yes covers exactly the listed calls. One kind of call per confirmation, and at most ten.
- A tool that changes one file (a trim, a reframe, a new soundtrack) is priced the same way and then called with the quoted figure where its schema asks for one. Words on a video and a join answer their own price when called without one.
- A spend with no family in the price tool's list, for example retrying a failed creative, cannot be priced in advance: say so plainly, say what will be billed, and still wait for an explicit yes.
- If the quote says `sufficient` is false, stop and say so.
- A clips job in `awaiting_approval` is alive and holding credits. Report it and never resubmit.

## 8. Waiting for results

- `openclips:wait_for_creative` waits about twenty seconds. If it returns `stillProcessing: true`, call it again; that is expected for videos. Stop and report when the creative's `actionStatus` is `awaiting_approval` or a failure. Hosts that show a live OpenClips card update it themselves, so there you may stop after the first wait. Never read a creative in a loop instead.
- A media job (a render, a mix, an edit) is followed with `openclips:wait_for_job`, and stopped with `openclips:cancel_job`.
- `openclips:await_product`: `pending_product_timeout` means wait again with the same correlation id; `pending_product_failed` is final, so report it.
- While waiting, one short status line is enough. Do not narrate each check.

## 9. Showing results

- Lead with what was made, then show it. Embed images as markdown images and link videos as plain links, because inline video rarely renders in chat. Offer to save the files locally.
- Do not paste raw JSON. In results, turn enum values into plain words (`humanise-labels` covers the cases). At the gate, keep exact field keys.
- Some hosts render product, creative and brand lists as a card. When yours does, write one short summary line and do not retype the rows. When it does not, show a table of at most twenty rows.
- Reply in the user's language. Tool arguments stay exactly as the API expects them.
- After a result, stop. Offer one next step at most.

## 10. When something goes wrong

- **A spend call that timed out has not necessarily failed.** The server may have finished it after the client stopped waiting. Re-read with `openclips:list_creatives` or `openclips:get_creative` first. If you retry, send the identical body: the server then returns the original result, or `409 request_in_flight` while it still runs, instead of charging twice. Never change a timed-out request and send it as new.
- **A failure the server reports definitely:** do not resend the same input. Say what failed and suggest one change that keeps the quality default.
- **Deleting anything** (a product, creative, folder or avatar) needs the user to name the item and confirm in a later message.
- For any other message, read `references/errors.md`. When the user's words and the API's differ, read `references/terminology.md`.
- When the server itself got in the way (an error you could not act on, a description that steered you wrong, a missing route), tell its team once, after the user's task, with `openclips:report_mcp_feedback`. Describe the server, never the user's content.

## Load on demand

- `references/connect.md`: connecting OpenClips on each host. Read it when no OpenClips server is found, or sign-in fails.
- `references/errors.md`: the server's error and refusal messages, and what each one means. Read it when a call fails or is refused.
- `references/terminology.md`: the user's words against the API's, including which avatar value each field takes. Read it when a field or a term is unclear.
