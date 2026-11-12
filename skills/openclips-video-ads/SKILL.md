---
name: openclips-video-ads
description: >-
  Makes new video ads with OpenClips from a marketplace video model, with no
  presenter on screen: text-to-video, a product photo animated as the first
  frame, first and last frames, a reference-held product clip, in any
  language the model renders, and a longer film as shots joined. Use when:
  "make a video ad", "animate this product photo", "image to video",
  "ten-second product video", "product spin", "loop for Stories", "use a
  video model by name". NOT for: a reel, a TikTok or a Short where someone
  talks and sells, or a recut of the user's footage (openclips), a
  cinematic or paper-collage film on a clips lane, two people talking, or
  the same film in several languages (openclips-clips), a software
  explainer, tutorial or app demo (openclips-saas-explainer), a property
  tour (openclips-real-estate), changing a video that exists
  (openclips-edit), a still image (openclips-image-ads), a product not yet
  in the workspace (openclips-brand-intel), hooks, scripts or storyboards
  with nothing to render (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips video ads

New video creative from a marketplace video model: one render, or a few shots joined. A reel where someone talks and sells starts with its words and belongs to the hub's reel row; a named film style (cinematic, paper collage, two voices) or one film in several languages is a clips film and belongs to `openclips-clips`. A single video in one language, with no presenter, is this skill. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Resolve the product and bind the image

- Find the product with `openclips:list_products` or `openclips:get_product_by_url`; refer to it as `#ID (name)`. Several match: ask. None, and the user named one: hand over to brand intel.
- **A product id gives brand context only; it does not put the product in frame.** To show the real product, read its `imageUrls` with `openclips:get_product` and send one as the first image with the first-frame role, or with the reference role to hold identity without dictating the frame. Say at the gate which image is bound. Without a bound image, the model invents a stand-in.
- "Animate this" with an image URL: that URL goes straight into the images as the first frame. A picture the user holds comes in first through `openclips:upload_media` and `openclips:await_media_upload`.

## 2. Load the playbooks

Load `openclips:load_skill("generate-marketplace-proxy-video")` for fields and validation, and `openclips:load_skill("prompt-preflight")` once: every prompt is rewritten against its checklist before it is priced. Load a craft playbook only when the ask needs it:

| The ask involves | Playbook |
|---|---|
| A film longer than one render, several shots, a person or place kept the same across them | `ad-video-craft` |
| Words, prices, logos or the real product's label on screen | `on-screen-text-and-brand` |
| People, hands, a voice, lip-sync, joins between shots | `people-continuity-and-sound` |
| What one model is good and bad at | `video-model-notes` |
| How to word the prompt so it renders as meant | `video-prompt-craft` |
| The story fitting its seconds, and checking the finished file | `video-review-and-story` |

## 3. Compose and price

- **Read the model's contract first** with `openclips:marketplace_models`: duration, resolution, aspect ratio, audio and image roles are per-model fields. A field the model does not read is refused at the price check, for free, with the fields it does accept. Choose with `references/model-choice.md` and state one default.
- **Exact words never go into the prompt.** The clip is made without them, and captions, a title, an offer or an end card are added afterwards from real fonts with `openclips:add_text_to_video`.
- **Video is the expensive family** and cost varies sharply between models and durations. The hub's rule stands: no cost talk while choosing; price once the body is fixed.
- **After every quote, answer the `promptCheck` checklist it carries** against the prompt, rewrite what fails, price again, and show the user the final prompt with the price. A model whose prompt is read aloud carries no checklist: keep that script word for word.
- **A longer film** is shots, each within its model's limit, priced as one plan and asked once. Joining them with `openclips:join_clips` is a call of its own: it is quoted and confirmed once the shots exist, never under the shots' yes.

Then the hub's gate: price the exact body with `openclips:preview_cost`, show cost and balance, wait for an explicit yes, send the same body with `openclips:generate_marketplace_video`.

## 4. Wait, check and show

`openclips:wait_for_creative` again while a creative reports `stillProcessing: true`; videos take several waits. Before handing a film over, look at it. With a shell, cut frames from the creative's video file on the user's machine, for free. Without one, `openclips:frames_from_video` is a priced call on this server and takes the hub's gate like any other; `openclips:view_creatives` on the frames is free. Link the video rather than embedding it, name the model, offer a save. One next step at most: another frame for another placement, words on screen, or a creator version, which is a reel or a clips film.

## Load on demand

- `references/model-choice.md`: user phrasings to a kind of video model, with a default. Read it when the user has not named a model.
- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
