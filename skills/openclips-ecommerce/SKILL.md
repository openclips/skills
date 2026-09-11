---
name: openclips-ecommerce
description: >-
  Makes ads across an online store's catalogue with OpenClips: one
  consistent image set per product in every channel size, creator videos
  for hero products, and localised variants, batched under one
  confirmation per family. Use when: "ads for my Shopify store", "ads for
  every product", "the same style for all my products", "Amazon listing
  images", "creator videos for my bestsellers", "ads for my top ten
  products", "these in German and French too". NOT for: a single one-off
  ad (openclips-image-ads, openclips-video-ads), one creator video for one
  product (openclips-clips), adding one product (openclips-catalog-setup),
  changing one creative (openclips-edit), a property listing
  (openclips-real-estate), a software product's explainer or demo video
  (openclips-saas-explainer), certifying that an image meets a
  marketplace's listing policy (not offered).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips e-commerce

The unit of work is the catalogue, not the creative: which products, one look across them, every channel size, every market, and a batch rule that keeps N calls honest. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. The products

- `openclips:list_products` for what the workspace has; the user names the subset ("top ten", "these three", "everything"). Refer to each as `#ID (name)`. "Everything" on a large catalogue runs in rounds of at most ten.
- Product URLs not yet imported: `openclips:get_product_by_url` first, then the free import (consent, `openclips:start_product_analysis`, `openclips:await_product`) per URL, as `openclips-catalog-setup` does. Products come with their brand; nothing creates a brand directly.
- Each product's image binds through its product id on the image routes; check with `openclips:get_product` that the product carries one before composing, so the product in the ad is the product in the store.

## 2. Pick the route

| The user wants | Route | Playbook | Tool |
|---|---|---|---|
| One look across many products, "same style", "consistent catalogue", a template | the template lane: one call per product with the same template and the same output formats | `generate-image-templates` | `openclips:generate_image_templates` |
| One hero image for one product | a marketplace image | `generate-marketplace-proxy-image` | `openclips:generate_marketplace_proxy` |
| A creator video for a hero product: unboxing, review, before-and-after | the single-creator lane, format from the live catalogue | `generate-ugc-video`, `clips` | `openclips:generate_clips_video` |
| Channel sizes of images that exist | resize, one ratio per call | `revise-creative-other` | `openclips:revise_creative_resize` |
| The same images for other markets | translate, several languages in one call per image | `revise-creative-other` | `openclips:revise_creative_translate` |

The template lane fans one template across the output formats in a single call, so channel sizes for new images come from `outputFormats`, not from a resize afterwards. The formats' accepted values are in the tool's schema; the channel names the user uses map onto them.

Load the row's playbook with `openclips:load_skill` before composing each family and follow it for fields, defaults and validation: `generate-image-templates` for the template lane, `clips` and `generate-ugc-video` for the creator lane (its calls are `openclips:generate_clips_video` with the lane set, per the hub's precedence rule), `revise-creative-other` for sizes and markets, `generate-marketplace-proxy-image` for a hero image.

## 3. The batch rule

A catalogue job is several calls. Preview every body first. Then one confirmation that lists each call with its own cost, the total and the balance; one explicit yes covers exactly the listed calls. One family per confirmation: never a generation and a revision together, and never a revision of a creative that does not exist yet, so sizes and translations of new images are a second round after the first has landed. At most ten calls per confirmation; larger jobs run in rounds. If the total exceeds the balance, say so before asking and offer the subset that fits.

## 4. What this skill refuses

- **Compliance.** It makes clean product images; it cannot certify that an image meets any marketplace's listing policy, and never says an image is compliant. Point at the marketplace's own rules and make the image the user describes.
- **Publishing.** OpenClips produces files; the user uploads them to the store.

## 5. Wait and show

`openclips:wait_for_creative` per creative until each settles. Show images inline grouped by product, link videos, name what each product got, and offer the second round: sizes or markets for what landed.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
