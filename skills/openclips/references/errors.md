# Errors and refusals

What the OpenClips server says when a call fails or is refused, and what to do next. Quotes are the server's wording; `…` marks a shortened quote.

## Before any row: did a spend call time out?

A generation or revision that timed out, or ran past its call budget, **may have finished** after the client stopped waiting. The server says so itself:

> "The backend did NOT cancel this request — it may have completed after we stopped waiting. Do not assume it failed: re-read the affected resource before retrying. If you do retry, send the IDENTICAL request — on guarded generation routes the server then returns the original result (or 409 request_in_flight while it still runs) instead of charging twice … Never rephrase a timed-out write and re-send it as new."

Re-read with `openclips:list_creatives` or `openclips:get_creative`. Only if nothing landed, resend the byte-identical body.

## Messages

| The server says | It means | Do this |
|---|---|---|
| `409 request_in_flight` | The identical request is still running | Wait with `openclips:wait_for_creative`. Do not resend |
| "Not enough tokens: this needs … but the workspace has … left. Top up tokens or upgrade your plan to keep generating." | The workspace balance is too low at send time, even if the preview passed | Stop and tell the user. Do not downgrade to make it fit unless they ask |
| "You've hit your token limit — ask your admin to raise it." | The user's personal limit in this workspace is spent | Stop. Their workspace admin can raise it |
| A preview returns `"sufficient": false` | The balance does not cover the request | Stop and say so |
| "Endpoint '…' is not in the OpenAPI catalogue. …" | The path is wrong, or deliberately not offered | Find the real route with `openclips:list_endpoints`. Never guess a path |
| "… is covered by the '…' tool — call that instead. …" | `openclips:call_api` was used for a route that has its own tool | Call the named tool with the same fields |
| "Brands cannot be created, edited or deleted …" | Brand writes do not exist anywhere in the product | Add or update a product instead; its brand comes with it |
| "Use the openclips surface instead: clips_catalog to pick a lane, then generate_clips_video." | A retired video pipeline was requested | Route to `openclips-clips` |
| "Ask the user to run this action through the web UI." | Deliberately closed to agents: deleting a workspace, subscriptions, releasing or repairing a clips job | Say it has to be done in the OpenClips app |
| "Skill '…' not found. Call list_skills to see available skills." | That playbook name is not served | Call `openclips:list_skills` once and pick from what it returns |
| "OpenAPI catalogue unavailable …", "Skill catalogue unavailable …" or "Skill body unavailable …" | The server could not reach its backend for a moment | Retry once after a short pause |
| `clips_brand_unresolvable` ("Send a productId or a brandId") | A clips film had nothing to anchor it: usually a paper-collage film made from a category with no brand | Send a `brandId` from `openclips:list_brands`, or a `productId`. If the workspace has no brand yet, add a product first |
| HTTP 422 with a `detail` list | A field is missing, out of range, or not accepted by that model or lane | Read `detail`. Re-check the live contract with `openclips:clips_catalog` or `openclips:marketplace_models`. Never guess an allowed value |
| HTTP 401, or an authentication error | Not signed in, or the sign-in expired | Follow the hub's connect steps. Do not retry in a loop |
| HTTP 403 | Signed in, but this user lacks the permission in this workspace | Say so. It is not a sign-in problem |
| `openclips:wait_for_creative` returns `stillProcessing: true` | Still rendering | Call it again |
| A creative's `actionStatus` is `awaiting_approval` | Not an error. A clips job is parked and holding credits | It needs approval in the OpenClips app. Stop waiting and never resubmit |
| `pending_product_timeout` from `openclips:await_product` | The wait budget ran out; the product may still land | Call `openclips:await_product` again with the same correlation id. Never start a second scrape |
| `pending_product_failed` from `openclips:await_product` | The scrape failed and will never land | Report it. Do not wait on that correlation id again |

## General rules

- After a definite failure, do not resend the same input. Say what failed and suggest one change.
- Do not switch to a different model or lane after a failure without telling the user. Losing a reference image or a creator silently changes what they asked for.
- If the same error repeats after one change, stop and report it with the server's exact message.
