---
name: openclips-ad-craft
description: >-
  Teaches how to make ads that work, before anything is rendered: hooks
  for the opening moment, beat maps and scripts timed to the film's
  length, storyboards in plain shot language, what makes a creator video
  read as real, how to test one change at a time, and how to review a
  draft as findings rather than a score. Names no model, calls no tool,
  and never needs the server. Use when: "write a hook", "five hooks for",
  "UGC script", "storyboard this ad", "shot list", "what makes a good video
  ad", "improve my brief", "what should I test next", "ad copy ideas",
  "review this ad". NOT for: generating an image or video
  (openclips-image-ads, openclips-video-ads, openclips-clips), copy written
  onto an existing creative by the server (openclips-edit), a listing or a
  software demo brief that is ready to render (openclips-real-estate,
  openclips-saas-explainer), anything about credits, models or endpoints
  (openclips, openclips-api).
license: MIT
compatibility: Needs nothing. Works with or without the OpenClips server; when the server is connected it still calls no tool.
---

# OpenClips ad craft

Craft is the part of advertising that does not rot when a model changes. This skill holds it in six short references, each written to be read in a minute and used at once. Nothing here names a model, a price, a lane or a tool, and nothing here spends: when the user is ready to render, the generation skills take over with the brief this one shaped.

## Route by what the user needs

| The user asks for | Read | Then produce |
|---|---|---|
| A hook, an opening, "the first seconds" | `references/hooks.md` | Five to eight hooks, each one line, each with the angle it takes named |
| A script, voice-over, "what do they say" | `references/beats-and-timing.md` | A beat map for the length asked, then the words per beat, counted |
| A UGC script or creator brief, "make it feel real" | `references/ugc-authenticity.md`, then `references/beats-and-timing.md` | A beat map whose lines are things to say in the creator's own words, never lines to read, plus the setting and the imperfections to keep |
| A storyboard, shot list, "what do we see" | `references/visual-rules.md` and `references/beats-and-timing.md` | Shots against the beat map in generic shot language, one action per shot |
| Ad copy ideas, headlines, primary text | `references/hooks.md`, then `references/review.md` | Headlines are hooks in writing: a set of angles with the fact each one carries, then the body copy as facts in order, checked against the failure shapes |
| "Improve my brief", "what makes a good video ad" | the three rules below, then `references/ugc-authenticity.md` and `references/visual-rules.md` | The brief rewritten as facts, setting, action, length and what to keep; or the rules, applied to the user's own case |
| A test plan, "what should I try next", "why did it flop" | `references/testing.md` | One variable to change, what stays fixed, how to read the result |
| A review of a draft, script or storyboard | `references/review.md` | A numbered list of findings, or "no findings" |

## Three rules that apply to every answer

- **Specific beats loud.** A hook or a line that could describe any product is not finished. Ask for the two or three facts that make this product itself when the brief lacks them; invent nothing about the product.
- **Time is the budget.** Every script and storyboard is timed. Say the length first, then fit the words and shots to it, and leave the first and last moments a little empty.
- **Facts, not claims.** No superlative the product page cannot back, no result the user has not measured, no person who exists. Examples use invented brands only.

## When the server is connected

This skill still calls nothing. It does not read the product from the workspace: the user is the source of the product's facts, and a generation skill reads the workspace when it is time to render. Work from the facts in the request; when they are thin, write the draft from what is there and name the two or three facts that would make it sharper. When the user wants the result made, hand over to the skill that owns it with the brief attached.

## Load on demand

- `references/hooks.md`: the opening moment, angles that work, openings to avoid.
- `references/beats-and-timing.md`: beat maps by length, the spoken-word budget, room at both ends.
- `references/visual-rules.md`: shot language, camera and subject, copy and wordmarks, describing the state you want.
- `references/ugc-authenticity.md`: what reads as real in a creator video and what breaks it.
- `references/testing.md`: one change at a time, what to hold, how to read a result.
- `references/review.md`: reviewing as findings, the common failure shapes.
