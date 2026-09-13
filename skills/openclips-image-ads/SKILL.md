---
name: openclips-image-ads
description: >-
  Makes new static image ads with OpenClips from a product in the workspace
  or a reference photo: a marketplace image model by default, the preset
  template lane when the user asks for a template or one look across sizes,
  and the beta Image Agent for a hands-off brief. Use when: "make an image
  ad", "static ad", "Instagram post for my product", "banner", "product photo
  for ads", "four image ads for this product", "make an ad from this photo",
  "ad in the style of this template", "use an image model by name". NOT
  for: changing a creative that exists, resizing, translating, upscaling or
  variations of it (openclips-edit), a competitor's ad as the source (not
  offered), any video (openclips-video-ads, or
  openclips-clips for a person on camera), listing images
  (openclips-real-estate), a whole store (openclips-ecommerce), a product not
  yet in the workspace (openclips-brand-intel), copy with nothing to attach
  it to (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips image ads

New static image creative. Three routes, one default. If the `openclips` hub skill is installed, its rules on finding tools, the workspace, spending, waiting and presenting apply here; if it is not, read `references/rules.md` first.

## 1. Resolve the source

- **A product in the workspace** is the usual source: find it with `openclips:list_products` or `openclips:get_product_by_url` and refer to it as `#ID (name)`. Several match: ask by name. None, and the user named one: hand over to brand intel.
- **A photo URL** with "make an ad from this" is a reference for a new ad, and this skill handles it: the URL goes into the reference images. There is no upload step on this surface, so a picture pasted without a link needs a hosted URL first. Only when the user wants *that image itself* changed is it editing.
- No product and no image: text-only generation is allowed; say that nothing anchors the product's real look.

## 2. Pick the route

| The user wants | Route | Playbook to load |
|---|---|---|
| An image ad, several image ads, a count of them, a reference photo turned into an ad | **Marketplace model.** The server's default front door for image ads | `generate-marketplace-proxy-image` |
| A template, "in the style of this template", one look fanned out across several sizes or formats | **Template lane.** Opt-in, only on an explicit ask like this | `generate-image-templates` |
| A brief with no art direction, "just handle it" | **Image Agent (beta).** Researches the brand itself and saves an editable project | `generate-image-agent` |

The marketplace route wins unless the user asked for what another route offers. An image ad that shows a workspace avatar belongs to the template lane, which casts one by `creatorAssetId`; marketplace models take no avatar.

## 3. Follow the playbook

Load it with `openclips:load_skill` and follow it for fields, defaults and validation. What decides most outcomes:

- **Marketplace:** the model is a request parameter and the prompt is literal. Read the live index with `openclips:marketplace_models`, then the chosen model's contract, before composing: every model accepts different fields, and an omitted field becomes a server default that still bills. Pick the model with `references/model-choice.md` and state one default. With a product set, the product's own images seed the reference; reference images are otherwise optional and capped per model.
- **Template lane:** a source is required (a product, a brand, a URL or an attached image), at least one output format is required, and a template URL is a style reference only, never the subject.
- **Image Agent:** on this surface it runs straight through with no draft pause, launched through `openclips:call_api`; the preview is an estimate at the base tier, and the render fee is settled after delivery. The gate before launch is the only approval, so say all of that at the gate. Poll the run with `openclips:call_api` on the run's own status route, not with the creative wait tool.

Then the hub's gate: preview the exact body, show the cost and the balance, wait for an explicit yes, send the same body.

## 4. Wait and show

`openclips:wait_for_creative` until a creative settles. Show the image inline, name the model that made it, and offer a save. One next step at most: a size, a translation or variations, all of which are editing.

## Load on demand

- `references/model-choice.md`: user phrasings to a marketplace model family, with a default. Read it when the user has not named a model.
- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
