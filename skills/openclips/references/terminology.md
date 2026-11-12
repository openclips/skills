# Terminology

The user's words on the left, the API's on the right. Use the left column when talking and the right column in tool arguments.

| Say to the user | In the API | Notes |
|---|---|---|
| credits | `tokenCost`, `tokenBalance`, "tokens" | Always say "credits" to the user |
| creative | generated creative | Any image or video OpenClips made or registered |
| workspace | `workspace_id` | Everything is scoped to one |
| product | product | What most generation starts from. Real-estate listings are products too |
| brand | brand | Comes with a product. Readable, never created or edited |
| avatar, creator, presenter | depends on the field | See the next section |
| lane | `lane` | One of the specialised clips pipelines. Read the live list from `openclips:clips_catalog` |
| format (of a clips film) | `format` id | Only ids listed by `openclips:clips_catalog` are real |
| model | `model` | A marketplace model. Read the live list from `openclips:marketplace_models` |
| aspect ratio, size | `aspectRatio` | The values a route accepts come from its own contract; for a preset image, from the presets tool's `placements` |
| price check, quote | `openclips:preview_cost` | Spends nothing. `tokenCost` is the price, `currentBalance` the balance |
| the Library | the workspace's creatives | Where an uploaded file lands, and where every result is kept |
| job | a tutorial, a reel or a package the OpenClips agent runs | Followed with `openclips:wait_for_openclips_agent` |
| playbook | a skill served by `openclips:load_skill` | The server's instructions for one workflow |

## Casting an avatar: which value goes where

Look the avatar up with `openclips:list_avatars` first, then:

| Field | Used by | Takes |
|---|---|---|
| `creators` | clips films | the avatar row's `externalId` |
| a presenter on a video job | the tutorial and reel jobs | the avatar row's `id`, in the field the job tool names |
| an avatar reference on a marketplace model | only the models whose contract lists one | the form the model's contract and its playbook give |

Sending the other value is refused, or silently renders without the avatar. The property video casts nobody. When unsure, the tool's own schema names the field.
