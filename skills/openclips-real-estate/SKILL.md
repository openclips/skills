---
name: openclips-real-estate
description: >-
  Makes listing ads for estate agents, agencies and rental managers with
  OpenClips: a 30-second property video from a listing (a creator-led tour
  or an atmospheric film), listing images for social and portals, and
  light clean-ups of listing photos. Every claim comes from the listing.
  Use when: "property video", "listing video", "real estate ad", "house
  tour video", "apartment for rent ad", "make an ad for this listing", a
  pasted listing URL, "listing images for the portal". NOT for: a product
  that is not a property (openclips-image-ads, openclips-video-ads,
  openclips-clips), altering what a property physically has (not offered),
  a 3D or virtual tour (not offered), a listing already made into a
  creative that needs a change (openclips-edit), a whole portfolio of
  products (openclips-ecommerce).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips real estate

A listing is a product in the workspace, so the listing ad starts where every other ad starts, then takes the one lane the server keeps for property: a fixed 30-second video whose facts come from the listing page. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. The listing

- **Already imported:** find it with `openclips:list_products` or, from a URL, `openclips:get_product_by_url`; refer to it as `#ID (name)`.
- **A listing URL with no product:** import it first, for free. One line of consent (it creates a product and may create a brand, nothing is charged), then `openclips:start_product_analysis` with the URL and `openclips:await_product` with the returned correlation id until the listing lands. The property route accepts the URL directly too, but scrapes it inside the call, which can outrun a chat host's timeout; the import path shows the user what was read before anything is spent.
- **No listing at all:** ask for the URL. Never build a property ad from a description alone: price, size, rooms and amenities are read from the listing, not invented.

## 2. Pick what to make

| The user wants | Route | Playbook | Tool |
|---|---|---|---|
| A property video: "tour", "walkthrough", "agent showing the place" | the creator-led tour format, the default | `generate-property-video` | the property submit route through `openclips:call_api` |
| "cinematic", "atmospheric", "luxury film" | the atmospheric film format | `generate-property-video` | same route |
| Listing images for social or a portal | a marketplace image with the listing's photo bound | `generate-marketplace-proxy-image` | `openclips:generate_marketplace_proxy` |
| Brighter or sharper listing photos | enhance: relight, sharpen, upscale | `enhance-asset` | `openclips:enhance_asset_proxy` |
| Portal and social sizes of an image that exists | resize | `revise-creative-other` | `openclips:revise_creative_resize` |

**The video.** Find the submit route and its preview sibling with `openclips:list_endpoints` (filter on `property`); load `openclips:load_skill("generate-property-video")` for the fields. Send the listing's product id; the format; and only what the user chose of language, captions, resolution and aspect ratio, so the server's defaults apply otherwise. Nobody is cast: the request schema has no presenter field, so a request for a named creator is declined with that reason; the playbook's line about routing a creator through the roster names a field the route does not read, and a value sent there is dropped and billed, so never send it. The playbook was written for the app's own agent, so its approval blocks and flow forms are done in plain text and its pending-product rule does not apply here.

**The images.** Send the listing's product id and let the playbook say how its photos are bound as the reference; name the photo in play at the gate. A listing image with no listing photo behind it shows a room that is not for sale.

## 3. What this skill refuses

- **Changing the property.** Enhancement stops at lighting, sharpness and resolution; a different crop is a resize. A pool, a wall, a window, furniture that is not there, a view that is not there: decline that part in one sentence and make the honest version.
- **Calling it a 3D or virtual tour.** It is a video edit of the listing's photos and text.
- **Inventing facts.** Every figure and feature is the listing's. When the listing lacks something the user asks to feature, say so instead of filling it in.
- **Steering.** No language that welcomes or discourages any kind of buyer or tenant; describe the property, not the people.

## 4. Gate, wait, show

The hub's gate for every credit-spending call: preview the exact body through the matching preview route, show cost and balance, list every field under its key, wait for an explicit yes, send the same body. The property video takes a few minutes: `openclips:wait_for_creative` until it settles, link the film, name the format and aspect ratio used, offer a save. Several images at once follow the hub's batch rule: one confirmation, one family, at most ten.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
