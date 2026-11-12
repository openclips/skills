---
name: openclips-image-ads
description: >-
  Makes new static image ads with OpenClips from a product in the
  workspace, a product link or a reference photo: the server's image
  presets by default, a marketplace image model when the user names one or
  writes the whole picture, and the three-image listing set. Use when:
  "make an image ad", "static ad", "Instagram post for my product",
  "banner", "story from this link", "product photo for ads", "four image
  ads for this product", "make an ad from this photo", "use an image model
  by name". NOT for: changing a creative that exists, resizing,
  translating, upscaling or variations of it (openclips-edit), a
  competitor's ad as the source (not offered), any video
  (openclips-video-ads, or openclips-clips for a person on camera), listing
  images of a property (openclips-real-estate), a whole store
  (openclips-ecommerce), a product not yet in the workspace
  (openclips-brand-intel), copy with nothing to attach it to
  (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips image ads

New static image creative. Three routes, and the server names the default: an image that promotes something starts at its presets, where the user never writes a prompt. If the `openclips` hub skill is installed, its rules on finding tools, the workspace, spending, waiting and presenting apply here; if it is not, read `references/rules.md` first.

## 1. Resolve the source

- **A product in the workspace** is the usual source: find it with `openclips:list_products` or `openclips:get_product_by_url` and refer to it as `#ID (name)`. Several match: ask by name.
- **A product link with no product behind it** is enough for a preset image: the launch takes the link itself. Offer to add the product to the catalogue only when the user wants to keep working from it; that is brand intel.
- **A photo** with "make an ad from this" is a reference for a new ad, and this skill handles it. A hosted URL goes into the reference images. A file the user holds comes in first through `openclips:upload_media` and `openclips:await_media_upload`. Only when the user wants *that image itself* changed is it editing.
- No product and no image: text-only generation is allowed; say that nothing anchors the product's real look.

## 2. Pick the route

Route each ask once.

| The user wants | Route | Tools |
|---|---|---|
| An ad, a post, a banner or a story, in any words, with no model named | **Presets.** The server's front door for any image that promotes something | `openclips:image_presets`, then `openclips:generate_image_preset_agent` |
| A model by name, the picture written out with its settings, or a picture that promotes nothing | **Marketplace model**, exactly as asked | `openclips:marketplace_models`, then `openclips:generate_marketplace_image`; playbook `generate-marketplace-proxy-image` |
| The listing images of one product for a marketplace: packshot, infographic, lifestyle | **Listing set**, fixed at three looks | `openclips:generate_listing_set` |

The presets win unless the user asked for what another route offers. An edit of an image that exists is not a new ad: that is `openclips-edit`.

## 3. Run it

- **Presets:** call `openclips:image_presets` (free, no workspace needed). It returns every preset with its look and what it needs, the frames, where each placement runs with the aspect ratio to send, and `howToPropose`. Pick one preset for the product and the ask, and write the proposal the way `howToPropose` says: that short proposal, with the quote, is the gate. Do not ask the user for a prompt or a model.
- **Marketplace:** load the playbook, and load `openclips:load_skill("prompt-preflight")` once. Read the live index with `openclips:marketplace_models`, then the chosen model's contract, before composing: every model accepts different fields, and a field the model does not read is refused at the price check, for free, with the fields it does accept. Pick the model with `references/model-choice.md` and state one default. After every quote, answer the `promptCheck` checklist it carries against the prompt, rewrite what fails, price again, and show the final prompt with the price.
- **Listing set:** the three looks are fixed; never offer to add, drop or swap one. Ask the user for the features the infographic prints instead of inventing them, and bind the product's own photo. The tool's description says how the set is priced; say at the gate that it is three images.
- **A workspace that has never paid** can be refused a paid model, with an error that says so. Quote again on the free set the server's instructions name, and tell the user that any purchase unlocks the rest.

Then the hub's gate: price the exact body with `openclips:preview_cost`, show the cost and the balance, wait for an explicit yes, send the same body through what the quote names.

## 4. Wait and show

`openclips:wait_for_creative` until a creative settles. Show the image inline, name the preset or the model that made it, and offer a save. One next step at most: a size, a translation or variations, all of which are editing.

## Load on demand

- `references/model-choice.md`: user phrasings to a marketplace model family, with a default. Read it when the user asked for a marketplace model and has not named one.
- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
