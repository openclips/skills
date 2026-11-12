# Choosing a video model

Map the user's words to a kind of model, then read the live index and the chosen model's contract with `openclips:marketplace_models`. Never send a model id, duration or resolution from memory; the index and the contract are the only source, and both change.

| The user says | Lean towards | Why |
|---|---|---|
| nothing about a model, "product video", "video ad" | the playbook's current default | The playbook names the default; it is the strongest general product renderer |
| "animate this photo", "bring the product to life" | a model whose contract has a first-frame image role | The photo becomes the first frame; a text-only model cannot hold it |
| "start here, end there" | a model with a first-and-last-frame role | Only some models accept two frames |
| "keep the product exactly like this" | a model with a reference role | Identity without dictating the frame |
| "with sound", "with music", "voice" | a model whose contract generates audio or accepts an audio input | Many models render silent; the contract says |
| "cheap", "quick draft", "test" | the playbook's fast or mini tier | Only when the user asks; otherwise the quality default |
| a model by name | that model, if the index lists it | If it is not listed, say so and offer the default |

Rules that hold across models:

- Duration is always sent and always priced; pick it deliberately and say it at the gate.
- Higher resolution is a price multiplier on several models; the quality default is what the playbook recommends, not the maximum.
- One model per request; to compare, preview each separately.
