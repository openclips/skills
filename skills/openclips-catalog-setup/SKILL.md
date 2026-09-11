---
name: openclips-catalog-setup
description: >-
  Gets products into an OpenClips workspace and keeps them current: imports
  a product from its URL, creates one by hand when there is no page, and
  updates name, price, description or images. Brands come with products and
  cannot be created or edited directly. Use when: "add my product", "import
  this product URL", "set up my brand", "add this product to OpenClips",
  "create a product from these photos", "update the product image", "change
  the price of my product", "is this product already in my workspace". NOT
  for: generating anything from a product that is already there
  (openclips-image-ads, openclips-video-ads, openclips-clips), a property
  listing (openclips-real-estate), a whole store's catalogue
  (openclips-ecommerce), deleting a product (openclips-api), editing a
  creative rather than a product (openclips-edit).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips catalogue setup

Most generation starts from a product, so this is often the first skill a new workspace needs. Nothing here spends credits: importing and editing products is free, so there is no cost gate, only plain consent where something is created. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## The one thing to know about brands

A brand is not something a user makes. It is matched or created automatically when a product is scraped, and neither this server nor the app offers a way to create, rename or delete one. "Set up my brand" is answered by adding the brand's first product. A playbook that offers to create a brand first is describing a journey that no longer exists; skip that step.

## 1. From a product URL, the usual path

1. `openclips:get_product_by_url` first. If the URL already has a product, say so and stop; do not scrape it again.
2. One line of consent, no cost figures: it creates a product and may create a brand, nothing is charged, start the import? Wait for a yes.
3. `openclips:start_product_analysis` with the URL. It answers at once with a correlation id and scrapes in the background, resolving or creating the brand on the way.
4. `openclips:await_product` with that correlation id. A timeout is only a read, so call it again with the same id; never start a second scrape of the same URL. `pending_product_failed` is final: report it.
5. Show the product as `#ID (name)` with its brand, and offer one next step: an ad.

## 2. By hand, when there is no page

`openclips:create_product` needs a brand id and a name; everything else is optional. Use it only when the workspace already has a brand for the product to sit under and the user has no URL. It is asynchronous too: it answers with a correlation id and no product, so finish with `openclips:await_product` as above. Load `openclips:load_skill("create-product")` for the fields, and skip its brand-creation, URL-scrape and file-upload sections, which are written for the app's own tool names. Image URLs must be hosted.

## 3. From photos

A product can be created from one to ten hosted product images; the route sits with the products routes, found with `openclips:list_endpoints`, and runs asynchronously like the URL path, resolving the brand itself. The same consent line applies. Photos pasted without links cannot be used until they are hosted somewhere: the presigned-upload path in the playbook works only where you can PUT bytes yourself, which most chat hosts cannot.

## 4. Updating a product

`openclips:update_product` with the product id and only the fields that change. It fires directly, with no cost and no gate, because the app lets users edit products freely; do not ask for confirmation, report what changed. The one exception: text you authored yourself, such as a description or a tagline, is shown before it is saved. Load `openclips:load_skill("update-product")` for the image rules. An empty image list clears the images, so never send one unless that is the intent.

## 5. Show

Products, brands and creatives are `#ID (name)` in prose. After an import, say which brand the product landed under, because that is the one fact the user cannot see from the request.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
