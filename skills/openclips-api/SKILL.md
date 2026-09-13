---
name: openclips-api
description: >-
  Reaches any OpenClips endpoint: through the connected server's
  list_endpoints and call_api for what no other skill covers (folders,
  deleting, video projects and the timeline editor, environments, voices,
  workflow runs, any route in the OpenAPI catalogue), and from the user's
  own code with a personal access token sent as X-Auth-Token against
  api.openclips.ai. Use when: "OpenClips API", "X-Auth-Token", "integrate
  OpenClips into my app", "call it from Python", "api.openclips.ai",
  "openapi.json", "put these in a folder", "delete this creative", "edit the
  video timeline", "which endpoint does that". NOT for: anything a spoke
  already covers, which stays with that spoke and its gate (openclips-image-ads,
  openclips-video-ads, openclips-clips, openclips-edit, openclips-brand-intel,
  openclips-real-estate, openclips-saas-explainer, openclips-ecommerce),
  running ads or reading campaign performance (not offered: OpenClips makes
  creative and does not deliver it).
license: MIT
compatibility: The escape hatch needs the OpenClips MCP server, connected and signed in. The developer path is advice about the REST API and needs no server.
---

# OpenClips API

Two doors to the same REST API. Connected through the server, `openclips:list_endpoints` finds a route and `openclips:call_api` sends it; from the user's own code, the same routes take a personal access token. Either way the spokes keep what they own: a request they cover goes to them and through their gate, never through a raw call here. If the `openclips` hub skill is installed, its rules apply; if not, read `references/rules.md` first. The hub's connect rule covers the escape hatch only; a question about writing code needs no server.

## 1. The escape hatch

1. `openclips:list_endpoints` with a filter on a path fragment or a tag word; the catalogue is the OpenAPI document, so a route that is not listed does not exist on this surface, and `openclips:call_api` refuses it by name.
2. Read the route's summary. When the body matters and no playbook covers it, the fields are in the OpenAPI document; keep field keys exactly as the API spells them, and the path exactly as `openclips:list_endpoints` spells it, trailing slash included where it has one.
3. Decide whether it spends. A route whose summary says it is billed, or that sits under a generate or revise path, takes the hub's gate. Most have a `preview_cost/` sibling; some do not (for example retrying a failed creative, training or retraining an avatar, adding or regenerating a video-project scene), so for those say that the exact cost cannot be shown in advance, say what will be billed, and still wait for a yes. A route that spends nothing runs directly, except the removals in section 3.
4. `openclips:call_api` with the method, the path with the workspace id filled in, and the body. Show the result in plain words, not raw JSON; `#ID (name)` for anything the user will refer to again.

Some routes are refused by the server with a reason. When the reason names a tool to use instead (brand writes point at the product import, retired video lanes at the clips lanes), use that tool through the spoke that owns it. When it points at the web app (subscription changes, deleting a workspace, releasing or repairing a clips job), relay the reason and do not retry around it. When `openclips:list_skills` shows a playbook for the route, load it with `openclips:load_skill` and follow it for the route's fields, order and validation; the gate and the waits on this page still apply, as the hub's precedence rule says.

## 2. Folders

The folder routes carry the `Generated Creative Folders` tag; filter on `folder`. List, create, rename, delete, add a creative, remove a creative. A creative can be in several folders at once. "Make a folder called X" is one create call. "Put these in a folder" is list the folders, resolve the name or create it, then one add call per creative. No gate: nothing here spends credits. Deleting a folder leaves its creatives in the library. Load `openclips:load_skill("creative-folders")` for the patterns; its tool names are the app's own, so each step is the matching route through `openclips:call_api`.

## 3. Removing things

Every DELETE, and any other call that removes something (a creative, a product, a folder, an avatar, an environment, a voice), is free and still waits. Members and billing are not touched from here at all; the hub sends those to the web app. The user names the item, here or earlier, and confirms with a yes in a later message. Before asking, say the item as `#ID (name)` and what goes with it (a folder's creatives stay; a creative's variations are their own rows). Nothing is removed on the message that asks.

## 4. The developer path

For code that runs outside a chat host, the API is the product, and the skill only points at it:

- **Token:** the user generates a personal access token on the API page of the OpenClips web app and sends it as the `X-Auth-Token` header. It acts as them across their workspaces and does not expire until rotated. Never ask for it, never echo one, and keep it out of source and browser code: have the code read it from an environment variable.
- **Where to read:** `https://api.openclips.ai/openapi.json` is the machine-readable schema and `https://api.openclips.ai/docs` the reference; `https://api.openclips.ai/llms.txt` indexes the guides (authentication, quickstart, jobs and polling, credits and previews, errors). Give the user the links; never fetch them with a web tool and never retype their contents, even when a link does not answer yet.
- **The shape of every generation:** read the current user (`GET /api/auth/me/`) and pick a workspace from its list; find or import the product; send the body to the route's `preview_cost/` sibling and check `sufficient`; send the same body to the route; read the creative until its status settles.
- **Timeouts and retries:** a client timeout does not cancel the job, and a plain resend starts and charges a second one, so give the client a generous timeout and read the library before any retry. The main generation and revision submits accept an `Idempotency-Key` header (the jobs guide lists which; the other routes ignore it); derive it from the request so a retry carries the same key. Under the same key, a repeat sent while the original is still running is refused once thirty seconds have passed, and a repeat after an original that ran long gets that original's result for a while afterwards; a repeat sent sooner than thirty seconds, or after an original that answered quickly, runs and bills again. The guide has the exact windows.
- **Same rules as chat:** the credit gate is the developer's own responsibility in code; state it once and do not talk cost otherwise.

## Load on demand

- `references/rules.md`: the shared OpenClips rules in short form. Read it only when the `openclips` hub skill is not installed.
