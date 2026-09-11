---
name: openclips-video-ads
description: >-
  Makes new video ads with OpenClips from a marketplace video model, with no
  presenter on screen: text-to-video, a product photo animated as the first
  frame, first and last frames, a reference-held product clip, in any
  language the model renders; and the beta Video Agent for a hands-off
  brief. Use when: "make a video ad", "animate this product photo", "image to
  video", "ten-second product video", "product spin", "loop for Stories",
  "use a video model by name". NOT for: a creator, testimonial, unboxing,
  presenter, two people talking, a cinematic or paper-collage film, or the
  same film in several languages (openclips-clips), a software explainer or
  app demo (openclips-saas-explainer), a property tour
  (openclips-real-estate), changing a video that exists (openclips-edit), a
  still image (openclips-image-ads), a product not yet in the workspace
  (openclips-catalog-setup), hooks, scripts or storyboards with nothing to
  render (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips video ads

New video creative from a marketplace video model. This is the server's default front door for a bare "video ad". A person on camera, a named film style (cinematic, paper collage, two voices) or one film in several languages is a clips film and belongs to `openclips-clips`; a single video in one language, with no presenter, is this skill. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Resolve the product and bind the image

- Find the product with `openclips:list_products` or `openclips:get_product_by_url`; refer to it as `#ID (name)`. Several match: ask. None, and the user named one: hand over to catalogue setup.
- **A product id gives brand context only; it does not put the product in frame.** To show the real product, read its `imageUrls` with `openclips:get_product` and send one as the first image with the first-frame role, or with the reference role to hold identity without dictating the frame. Say at the gate which image is bound. Without a bound image, the model invents a stand-in.
- "Animate this" with an image URL: that URL goes straight into the images as the first frame. There is no upload step on this surface; if the user pasted a picture rather than a link, ask for a hosted URL.

## 2. Pick the route

| The user wants | Route | Playbook to load |
|---|---|---|
| A video ad, a product photo brought to life, a short product clip | **Marketplace video model.** The default | `generate-marketplace-proxy-video` |
| "Just make me a video", a brief with no direction | **Video Agent (beta).** Researches the brand, renders, saves an editable project | `generate-video-agent` |

## 3. Follow the playbook

Load it with `openclips:load_skill` and follow it for fields and validation. What decides most outcomes:

- **Read the model's contract first** with `openclips:marketplace_models`: duration, resolution, aspect ratio, audio and image roles are per-model fields, and an omitted one becomes a server default that still bills. Choose with `references/model-choice.md` and state one default.
- **Video is the expensive family** and cost varies sharply between models and durations. The hub's rule stands: no cost talk while choosing; preview once the body is fixed. Where the playbook says to show prices beside the model options, the hub's rule wins.
- **Video Agent:** on this surface it runs straight through with no storyboard pause, launched through `openclips:call_api`. Its launch fee is charged at launch and the render fee after delivery; the preview shows only the launch fee. The gate before launch is the only approval, so say all of that at the gate. Poll the run on its own status route with `openclips:call_api`, not with the creative wait tool.

Then the hub's gate: preview the exact body, show cost and balance, wait for an explicit yes, send the same body.

## 4. Wait and show

`openclips:wait_for_creative` again while a creative reports `stillProcessing: true`; videos take several waits. Link the video rather than embedding it, name the model, offer a save. One next step at most: a resize for another placement, a translation, or a creator version, which is a clips film.

## Load on demand

- `references/model-choice.md`: user phrasings to a kind of video model, with a default. Read it when the user has not named a model.
- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
