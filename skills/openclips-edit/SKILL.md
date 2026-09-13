---
name: openclips-edit
description: >-
  Changes a creative that already exists in OpenClips instead of making a
  new one: a new aspect ratio, a translation, a higher resolution, N
  variations of one image, signal-level clean-ups (sharpen, denoise,
  relight, remove a background, vectorise, upscale or lip-sync a video), ad
  copy from its landing page, or the OpenClips watermark by name. Use when:
  "make it square", "resize for Stories", "translate this to German",
  "upscale it", "make it sharper", "remove the background", "fix the
  lighting", "make three versions of this", "write copy for this creative",
  "lip-sync this to my audio". NOT for: a brand-new image or video (openclips-image-ads,
  openclips-video-ads, openclips-clips), a competitor's ad as the source
  (not offered), editing a
  product's details (openclips-catalog-setup), deleting a creative
  (openclips-api), sizes or markets across a whole catalogue
  (openclips-ecommerce), copy with nothing to attach it to
  (openclips-ad-craft), the user's own logo as a watermark (not offered).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips edit

Something exists and one thing about it should change. Regenerating instead spends credits on a brand-new image and loses the approved composition, so this skill is chosen over the generation skills whenever the user points at a creative. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Find the source

- **A library creative** is the usual source: `openclips:list_creatives` or `openclips:get_creative`; "my latest" is the newest finished one. Refer to it as `#ID (name)` and pass it by id, never by a URL read off a card, because a card URL can be a display rendition.
- **A hosted image URL with no creative behind it** is accepted by every revise tool as `sourceImageUrl` and by enhance as `imageUrl` or `videoUrl`; the tool's own schema is the authority. Where the revise playbook says the resize, translate and upscale tools take a library creative only, or that upscale takes a scale factor, it is older than the schema: the schema wins. Never mint a variation just to obtain an id. There is no upload step on this surface: a picture pasted without a link needs a hosted URL first.
- Several candidates: ask by name. Nothing to point at: this is generation, not editing.

## 2. Pick the operation

| The user wants | Operation | Playbook | Tool |
|---|---|---|---|
| Another aspect ratio for an **image**: "square", "for Stories", "landscape" | resize, one ratio per call | `revise-creative-other` | `openclips:revise_creative_resize` |
| The same **image** in other languages | translate; language codes, several in one call | `revise-creative-other` | `openclips:revise_creative_translate` |
| A higher resolution **image** | upscale, to a target resolution or an explicit size from the tool's schema | `revise-creative-other` | `openclips:revise_creative_upscale` |
| **A change described in words** about the picture's content: a new background, remove the badge, swap the colour, "another like this", N versions | variations; one per call, always with a prompt | `revise-creative-variate` | `openclips:revise_creative_variate` |
| **A signal-level clean-up** with no content described: sharpen, denoise, relight, restore, cut out the subject, remove the background, vectorise; and any **video** upscale, smoothing or lip-sync | enhance; the operation is the `model` field, whose accepted values are listed in the tool's schema and explained in the playbook's table | `enhance-asset` | `openclips:enhance_asset_proxy` |
| Headline, primary text and description for a creative, from its landing page | ad copy; costs nothing | `generate-ad-copy` | the ad-copy route through `openclips:call_api` |
| The OpenClips watermark, asked for in so many words | watermark; irreversible | none | `openclips:watermark_creative` |

The line that matters most: **words about content mean variations; a named signal fix means enhance.** Replacing a background or repainting a region through enhance happens only when the user names that operation, or a variation already failed this session. Sharpen, denoise and relight are enhance operations even where the revise playbook's blurb folds "sharper" into upscale; upscale changes resolution and nothing else. The revise tools work on images only, and a video in another aspect ratio is not offered on this surface: the honest answer is a new render in that ratio through `openclips-video-ads`.

## 3. Follow the playbook

Load it with `openclips:load_skill` and follow it. What decides most outcomes:

- Resize, translate and upscale take the source and one kind of value; product, brand and tone come from the source, so ask for nothing else. Validate language codes against the languages route found with `openclips:list_endpoints` before sending them.
- Variations need a prompt; ask for one rather than inventing it. N variations are N calls under one confirmation, per the hub's batch rule.
- Enhance operations are not in `openclips:marketplace_models`: the accepted `model` values come from the tool's schema and the playbook's table, and the price from the enhance preview route. Some need a second input (a mask and a prompt, a prompt for a new background, an audio track for lip-sync), and the request is refused without it. Ask; never guess a mask or substitute a track.
- **Ad copy** needs the creative and a landing page URL, the product's URL unless the user gives one. No cost preview, since it is free, but one line naming both and a yes before it runs.
- **Watermark:** never offer it. It stamps the OpenClips logo, not the user's, and no route removes it; afterwards every read serves the branded copy. Confirm with the `#ID`, say the clean master will no longer be served, and act only on a yes in a later message.
- An edit that consumes another edit's output waits for the first to land: "sharpen it and upscale it" is two steps with two gates, because the second id does not exist yet. Same for a generation followed by an edit.

Then the hub's gate for every credit-spending call: preview the exact body, show cost and balance, wait for an explicit yes, send the same body.

## 4. Wait and show

Revisions, variations and enhancements make a new creative: `openclips:wait_for_creative` until it settles, show it, name what changed, keep the source's `#ID` in view, offer a save. Ad copy and the watermark change the source itself and make nothing new, whatever the ad-copy route's own summary says about a child creative: re-read the source with `openclips:get_creative` after a short wait and report what landed, honestly, if nothing has yet.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
