---
name: openclips-edit
description: >-
  Changes a creative that already exists in OpenClips instead of making a
  new one: an image in another aspect ratio or language, a change described
  in words, variations, signal-level clean-ups (sharpen, denoise, relight,
  remove a background, vectorise, upscale, lip-sync a video), a video
  trimmed, reframed, rotated, given new sound or exact words on screen,
  clips joined, or the OpenClips watermark by name. Use when: "make it
  square", "resize for Stories", "translate this to German", "upscale it",
  "remove the background", "make three versions of this", "make this
  video vertical", "add a caption to this video", "join these clips",
  "lip-sync this to my audio".
  NOT for: a brand-new image or video (openclips-image-ads,
  openclips-video-ads, openclips-clips), a competitor's ad as the source
  (not offered), editing a product's details (openclips-brand-intel),
  deleting a creative (openclips-api), sizes or markets across a whole
  catalogue (openclips-ecommerce), the user's own logo as a watermark
  (not offered).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips edit

Something exists and one thing about it should change. Regenerating instead spends credits on a brand-new creative and loses the approved composition, so this skill is chosen over the generation skills whenever the user points at a creative. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Find the source

- **A library creative** is the usual source: `openclips:list_creatives` or `openclips:get_creative`; "my latest" is the newest finished one. Refer to it as `#ID (name)` and pass it by id, never by a URL read off a card, because a card URL can be a display rendition.
- **A file the user holds** comes into the workspace first: `openclips:upload_media` then `openclips:await_media_upload`, or `openclips:import_creative_from_url` for a public link. The creative it becomes is the source.
- **A hosted image URL with no creative behind it** is accepted by the image edit as its source; the one-file video tools take a library creative only.
- Several candidates: ask by name. Nothing to point at: this is generation, not editing.

## 2. Pick the operation

| The user wants | Operation | Playbook | Tool |
|---|---|---|---|
| **A change described in words** about an image's content: a new background, remove the badge, swap the colour, the same ad in another language, "another like this", N versions | an image edit: the source goes in the images, the change in the prompt | `generate-marketplace-proxy-image` | `openclips:generate_marketplace_image` |
| An **image** recomposed for another aspect ratio: "square", "for Stories", "landscape" | the same image edit, asking for the new frame | `generate-marketplace-proxy-image` | `openclips:generate_marketplace_image` |
| A **video or an image** put in another frame as it is, cropped or over a blurred copy | reframe | none | `openclips:reframe_media` |
| **A signal-level clean-up** with no content described: sharpen, denoise, relight, restore, cut out the subject, remove the background, vectorise, upscale; and a video upscale, smoothing or lip-sync | enhance; the operation is the `model` field, whose accepted values are listed in the tool's schema and explained in the playbook's table | `enhance-asset` | `openclips:enhance_asset_proxy` |
| A video cut to one span, turned or mirrored | trim, rotate | none | `openclips:trim_video`, `openclips:rotate_media` |
| A video's sound removed, swapped, cleaned or saved alone | replace, clean, extract | none | `openclips:replace_audio`, `openclips:clean_voice`, `openclips:extract_audio` |
| **Exact words on a video**: captions, a title, an offer, an end card | text set from real fonts; never ask a video model to draw words | none | `openclips:add_text_to_video` |
| Finished clips joined into one film, in order | join | none | `openclips:join_clips` |
| One moment of a video kept as a still | save a frame | none | `openclips:save_frame` |
| The OpenClips watermark, asked for in so many words | watermark; irreversible | none | `openclips:watermark_creative` |

The line that matters most: **words about content mean an image edit; a named signal fix means enhance.** Replacing a background or repainting a region through enhance happens only when the user names that operation, or an edit already failed this session. Upscale changes resolution and nothing else. Every operation makes a new library creative and leaves the source untouched, except the watermark.

## 3. Run it

- **An image edit** names only what changes. Load the playbook for the source and link fields: a library creative is sent both as the source and as the parent, so the result becomes its newest version; a pasted URL is the source alone. The playbook names the default edit model; follow the user if they name another. N versions are N calls under one confirmation, per the hub's batch rule. A prompt the user did not give is asked for, not invented.
- **A translation** is an image edit whose prompt names the language and what stays. Look at the rendered words afterwards: models misspell.
- **Enhance** operations are not in `openclips:marketplace_models`: the accepted `model` values come from the tool's schema and the playbook's table. Some need a second input (a mask and a prompt, a prompt for a new background, an audio track for lip-sync), and the request is refused without it. Ask; never guess a mask or substitute a track.
- **The one-file video tools** take a library creative and a few fields the tool's schema lists. Each is priced first and then called with the quoted figure. A reframe of a talking video can follow the speaker; say so when it applies.
- **Words on a video** are sent exactly as the user wrote them, with where and when they show. Ask for the words rather than writing them.
- **Words on a video and a join quote themselves:** called without a price they only answer it. Show it, and on the user's yes call again with the same fields and that price. That quote is the gate for these two.
- **Watermark:** never offer it. It stamps the OpenClips logo, not the user's, and no route removes it; afterwards every read serves the branded copy. Confirm with the `#ID`, say the clean master will no longer be served, and act only on a yes in a later message.
- An edit that consumes another edit's output waits for the first to land: "sharpen it and upscale it" is two steps with two gates, because the second id does not exist yet. Same for a generation followed by an edit.

Then the hub's gate for every credit-spending call: price the exact body with `openclips:preview_cost`, show cost and balance, wait for an explicit yes, send the same body.

## 4. Wait and show

An image edit or an enhancement makes a new creative: `openclips:wait_for_creative` until it settles. A one-file video tool starts a job: `openclips:wait_for_job` until it is done. A text pass or a join that is still rendering answers with a job reference: call the same tool again with it. Show the result, name what changed, keep the source's `#ID` in view, offer a save. The watermark changes the source itself and makes nothing new: re-read the source with `openclips:get_creative` after a short wait and report what landed, honestly, if nothing has yet.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
