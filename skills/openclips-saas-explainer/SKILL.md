---
name: openclips-saas-explainer
description: >-
  Makes explainer and demo videos for software products with OpenClips: a
  narrated paper-collage explainer of what the product is, or an app demo
  with a presenter walking through screens drawn from the product's own
  page, plus launch variants. Use when: "explainer video for my SaaS",
  "app demo video", "launch video for my software", "show my app screens
  in a video", "paper explainer for my app", "walk through the product".
  NOT for: a physical product (openclips-clips, openclips-video-ads,
  openclips-image-ads), a creator testimonial with no screens
  (openclips-clips), a still launch graphic (openclips-image-ads), changing
  a video that exists (openclips-edit), a software product not yet in the
  workspace (openclips-catalog-setup), the script alone (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips SaaS explainer

Two clips lanes serve software: a narrated paper-collage film that explains what the product is, and a presenter-plus-screens film that demonstrates it. Both run through `openclips:generate_clips_video`, and the catalogue decides what each needs. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Catalogue first

Call `openclips:clips_catalog` for the workspace before composing. Read the chosen lane's `inputs`: `required`, `conditional`, `locked` and `ignored`, its format list and its duration menu. The two lanes disagree on almost everything, so nothing below is sent until the catalogue confirms it.

## 2. Pick the lane

| The user wants | Lane, in the catalogue's words | What it needs, as last seen |
|---|---|---|
| "explain what it does", "how it works", "explainer", "paper", "collage" | the narrated paper-collage lane | a brand in the workspace; a product photo **or** a software category, never both; formatless; narration in English only; one fixed resolution |
| "demo", "show the app", "walk through the screens", "presenter over my product" | the presenter-plus-app-screens lane | a format from its list, the **product URL** (the lane crawls it for facts and screens and refuses to run without it), the brand name; reads a language; resolution changes the price |

Unclear, and screens were mentioned: ask one question. Unclear otherwise: the explainer. A software category with no brand in the workspace is refused by the explainer lane, and brands only come from adding a product, so hand a brand-less workspace to catalogue setup first.

## 3. Compose

- **The product:** `openclips:list_products`, or `openclips:get_product_by_url` from a link; `#ID (name)` in prose. The demo lane's product URL is the product's own page; ask for it when the product record has none.
- **Presenter:** optional on both lanes, cast as the first creator by an avatar row's `externalId` from `openclips:list_avatars` when the user asks for one; on the explainer lane that row is the narrator. Omitted, the lane picks its own. Never a raw reference image for a face.
- **Language:** the demo lane reads one, but only the few codes the catalogue lists for it sell there. The explainer lane locks to English. A language neither lane lists is refused before spend, and the offer is a lane whose catalogue entry lists it, usually a creator lane from `openclips-clips`, or the film in English.
- **Duration and format:** from the catalogue's menu and format list for that lane; an omitted duration is billed at the lane's default. When the user names no format on the demo lane, take the first in the catalogue's list for it and say so at the gate rather than asking.
- **Claims:** the film says what the product page shows. A feature the page does not show is not promised.
- Load `openclips:load_skill("clips")` for the shared rules; `generate-paper-video` and `generate-ugc-video` add lane rules but name the app's own tools, so every call they describe is `openclips:generate_clips_video` with the lane set, per the hub's precedence rule.

## 4. Gate, wait, show

The hub's gate: preview the exact body through the clips preview route, show cost and balance, list every field under its key, wait for an explicit yes, send the same body. Launch variants (another duration, another format) are separate films and separate gates, batched under the hub's batch rule. `openclips:wait_for_creative` until it settles; a job that returns `awaiting_approval` needs approval in the app and is never resubmitted. Link the film, name the lane and format, offer a save.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
