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
| aspect ratio, size | `aspectRatio`, `outputFormats` | Each tool names it differently; follow the playbook |
| price check | `preview_cost` | Spends nothing |
| playbook | a skill served by `openclips:load_skill` | The server's instructions for one workflow |

## Casting an avatar: which value goes where

Look the avatar up with `openclips:list_avatars` first, then:

| Field | Used by | Takes |
|---|---|---|
| `creators` | clips films | the avatar row's `externalId` |
| `creatorAssetId` | image templates, property videos | the avatar row's `id`, as a string |

Sending the other value is refused, or silently renders without the avatar. Marketplace models take no avatar at all: to put an avatar in an image ad, use image templates. When unsure, the playbook for the flow names the field.
