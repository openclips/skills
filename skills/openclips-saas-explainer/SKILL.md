---
name: openclips-saas-explainer
description: >-
  Makes explainer, demo and tutorial videos for software products with
  OpenClips: a narrated paper-collage explainer of what the product is, an
  app demo with a presenter over screens drawn from the product's page, or
  a presenter-led tutorial over the product's real screens. Use when:
  "explainer video for my SaaS", "app demo video", "launch video for my
  software", "show my app screens in a video", "paper explainer for my
  app", "tutorial video for my product", "how-to video".
  NOT for: a physical product (openclips-clips, openclips-video-ads,
  openclips-image-ads), a creator testimonial with no screens
  (openclips-clips), a still launch graphic (openclips-image-ads), changing
  a video that exists (openclips-edit), a software product not yet in the
  workspace (openclips-brand-intel), the script alone (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips SaaS explainer

Three films serve software. Two are clips lanes: a narrated paper-collage film that explains what the product is, and a presenter-plus-screens film that demonstrates it; both run through `openclips:generate_clips_video`, and the catalogue decides what each needs. The third is a job the OpenClips agent runs: a presenter-led tutorial over the product's real screens, section 5. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Catalogue first

For either lane, call `openclips:clips_catalog` for the workspace before composing. Read the chosen lane's `inputs`: `required`, `conditional`, `locked` and `ignored`, its format list and its duration menu. The two lanes disagree on almost everything, so nothing below is sent until the catalogue confirms it.

## 2. Pick the lane

| The user wants | Lane, in the catalogue's words | What it needs, as last seen |
|---|---|---|
| "explain what it does", "how it works", "explainer", "paper", "collage" | the narrated paper-collage lane | a brand in the workspace; a product photo **or** a software category, never both; formatless; narration in English only; one fixed resolution |
| "demo", "show the app", "walk through the screens", "presenter over my product" | the presenter-plus-app-screens lane | a format from its list, the **product URL** (the lane crawls it for facts and screens and refuses to run without it), the brand name; reads a language; resolution changes the price |
| "tutorial", "how-to", "walkthrough of a feature", "a YouTube tutorial", the user's own screen recording or screenshots | the presenter tutorial job, section 5 | the product's real screens, a presenter, and the answers to the job's questions |

Unclear, and screens were mentioned: ask one question. Unclear otherwise: the explainer. A software category with no brand in the workspace is refused by the explainer lane, and brands only come from adding a product, so hand a brand-less workspace to brand intel first.

## 3. Compose

- **The product:** `openclips:list_products`, or `openclips:get_product_by_url` from a link; `#ID (name)` in prose. The demo lane's product URL is the product's own page; ask for it when the product record has none.
- **Presenter:** optional on both lanes, cast as the first creator by an avatar row's `externalId` from `openclips:list_avatars` when the user asks for one; on the explainer lane that row is the narrator. Omitted, the lane picks its own. Never a raw reference image for a face.
- **Language:** the demo lane reads one, but only the few codes the catalogue lists for it sell there. The explainer lane locks to English. A language neither lane lists is refused before spend, and the offer is a lane whose catalogue entry lists it, usually a creator lane from `openclips-clips`, or the film in English.
- **Duration and format:** from the catalogue's menu and format list for that lane; an omitted duration is billed at the lane's default. When the user names no format on the demo lane, take the first in the catalogue's list for it and say so at the gate rather than asking.
- **Claims:** the film says what the product page shows. A feature the page does not show is not promised.
- Load `openclips:load_skill("clips")` for the lane rules, and `openclips:load_skill("prompt-preflight")` once: after every quote, answer the `promptCheck` checklist it carries against the brief, fix what fails and price again.

## 4. Gate, wait, show

The hub's gate: price the exact body with `openclips:preview_cost` and the clips family, show cost and balance, list every field under its key, wait for an explicit yes, send the same body. Launch variants (another duration, another format) are separate films and separate gates, batched under the hub's batch rule. `openclips:wait_for_creative` until it settles; a job that returns `awaiting_approval` needs approval in the app and is never resubmitted. Link the film, name the lane and format, offer a save.

## 5. The presenter tutorial

A sixteen-by-nine film in which a real presenter opens and closes and sits in a small circle while the product's own screens are used click by click, with a voiceover, music, captions and chapters. The OpenClips agent makes it; this skill opens the job and relays.

1. Ask first, all at once: `openclips:brief_questions` for the presenter flow returns what is still open. Ask the user for a budget too.
2. Get the inputs into the workspace: a screen recording of the user clicking through the product is the best source, screenshots in story order the next, the product's public page the last. A file the user holds comes in through `openclips:upload_media` and `openclips:await_media_upload`. The presenter is a workspace avatar from `openclips:list_avatars` or the user's own short selfie video; a voice is one the user picked from `openclips:list_voices`, or a copy of the presenter's own, only with that person's agreement.
3. `openclips:make_presenter_tutorial` with the brief in the user's words, the answers and whatever the user chose; leave out the rest and the agent asks.
4. Read each reply with `openclips:wait_for_openclips_agent`, relay it, and answer its cards with `openclips:answer_openclips_agent`; approve a priced card only after the user said yes. A parked reply is a long render: keep waiting with the same ids.

Load `openclips:load_skill("presenter-explainer")` to plan the film with the user or to write its script yourself.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
