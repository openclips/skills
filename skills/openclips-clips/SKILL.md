---
name: openclips-clips
description: >-
  Makes specialised marketing films with OpenClips on the clips lanes: a
  talking creator, a testimonial, an unboxing or before-and-after, the same
  film per language, two people talking, a cinematic commercial, or a
  paper-collage film. Use when: "UGC video", "a creator talking about my
  product", "testimonial video", "unboxing video", "before and after video",
  "the same ad in Spanish and German", "two people talking", "cinematic
  commercial", "paper collage video", "use this avatar". NOT for: a bare
  video ad with no person or named style (openclips-video-ads), an explainer
  or app demo for software, including a presenter over app screens
  (openclips-saas-explainer), a property tour (openclips-real-estate), a
  still image (openclips-image-ads), creator videos across many products
  (openclips-ecommerce), changing a film that exists (openclips-edit), a
  product not yet in the workspace (openclips-catalog-setup), a script or
  storyboard with nothing to shoot (openclips-ad-craft).
license: MIT
compatibility: Needs the OpenClips MCP server, connected and signed in. Works alone; the openclips hub carries the shared rules.
---

# OpenClips clips

One tool, `openclips:generate_clips_video`, serves several lanes, and the same body means different things on each. The catalogue is the only oracle: what a lane needs, which fields it silently drops and bills anyway, and which format ids are real all come from `openclips:clips_catalog`, never from memory. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first.

## 1. Catalogue first, always

Call `openclips:clips_catalog` for the workspace before composing anything. For the lane you choose, read its `inputs`: `required`, `conditional`, `locked` (one value only, refused before spend) and `ignored` (accepted, dropped, rendered at full price anyway). Take the `format` id from that lane's own list. The lane's default duration is what an omitted duration is billed at.

## 2. Pick the lane from the kind of film

| The user describes | Lane kind, in the catalogue's own words | Watch for |
|---|---|---|
| One creator talking to camera, phone-shot, a testimonial, an unboxing, a before-and-after | the single-creator creator lane | the default when a person is on screen; some formats take a second reference |
| The same ad in several languages | the per-language creator lane | **one language per submit**: several languages means several films and several gates |
| Two people talking to each other | the two-voice lane | the only lane that binds two creators |
| A short, punchy product commercial | the short cinematic lane | duration is locked; some formats burn a hook and call to action in verbatim; no person can be cast |
| A premium filmic commercial with pacing | the cinematic lane | no person can be cast |
| A narrated torn-paper editorial film | the paper-collage lane | the one formatless lane; a product or a category, never both; a category run still needs a brand in the workspace |
| A presenter walking through a software product's screens | the presenter-plus-app-screens lane | owned by `openclips-saas-explainer`; route there |

Ties: several languages beats everything. Read `references/lanes.md` for the shape of each lane as last recorded, then trust the catalogue over it.

## 3. Cast, brief, compose

- **Creators** are avatar rows from `openclips:list_avatars`, cast by their `externalId`, never the numeric id. Stock and workspace-trained avatars both cast. The cinematic lanes ignore creators entirely; say so if the user asked for a face there.
- **The brief is the film.** One field, the user's own words as far as possible, short and concrete. Do not paraphrase their direction into marketing copy.
- **Language:** only the lanes that list a language field read one, and only the codes the catalogue lists for that lane sell. The other lanes lock the language to English, so a non-English value is refused before spend and the narration is English regardless; refuse a non-English cinematic ask and offer the creator lane instead.
- Load `openclips:load_skill("clips")` for the remaining rules. The lane playbooks `generate-ugc-video`, `generate-cinematic-video` and `generate-paper-video` add lane-specific rules; they were written for the app's own agent and name tools this server does not list, so every call they describe is `openclips:generate_clips_video` with the lane set, as the hub's precedence rule says.

## 4. Gate, wait, show

The hub's gate: preview the exact body through the clips preview route, show cost and balance, list every field under its key, wait for an explicit yes, send the same body. Clips prices are admin-controlled and moved several-fold in the last cutover, so any number remembered is wrong.

A job that returns `awaiting_approval` is alive and holding credits: it needs approval in the OpenClips app, cannot be released from here, and must never be resubmitted. Otherwise `openclips:wait_for_creative` until it settles, link the film, name the lane and format, offer a save.

## Load on demand

- `references/lanes.md`: each lane's shape as last recorded, dated. Read it to choose a lane; send only what the live catalogue confirms.
- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
