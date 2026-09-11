# Choosing an image model

Map the user's words to a kind of model, then read the live index and the chosen model's contract with `openclips:marketplace_models`. Never send a model id from memory: ids, tiers and accepted fields change, and the index is the only source.

| The user says | Lean towards | Why |
|---|---|---|
| nothing about a model, "product ad", "hero image", "ad creative" | the playbook's current default | The playbook names the default; it is the strongest general product renderer |
| "edit this photo but keep the product", "same product, new scene" | a model whose contract accepts reference images | Identity needs references; a text-only model cannot hold the product |
| "logo", "icon", "vector", "SVG" | a model whose contract says it outputs vector | Raster models cannot |
| "quick", "cheap", "draft" | the playbook's fast tier of the default | Only when the user asks; otherwise the quality default |
| a model by name | that model, if the index lists it | If it is not in the index, say so and offer the default |

Rules that hold across models:

- Expect rendered text to be misspelled. Keep copy in the caption, the template lane or a later edit rather than asking a model to spell it, unless the playbook says the chosen model renders text reliably.
- One model per request. To compare, preview each separately and let the user choose.
- Aspect ratio and resolution are per-model fields; the contract says which values exist. Do not guess.
