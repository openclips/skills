# Shared OpenClips rules, short form

The `openclips` hub skill carries these in full; this is the fallback when it is not installed.

- Tools are written `openclips:<tool>`; match them on the name after the last `__` or `:` on your host. If no OpenClips tool is visible, tell the user to connect the server and stop.
- Call `openclips:list_my_workspaces` once; with several workspaces, ask which.
- Brands cannot be created or edited anywhere; they come with products. Skip any playbook step that creates or edits one.
- Load the named playbook with `openclips:load_skill` and follow it. Where it names an approval block, a form or a tool this server does not list, do the same in plain text.
- Spending: use the playbook's quality default and do not talk about cost while choosing. Every credit-spending call passes one gate: build the exact body, preview it through the matching `preview_cost` route with `openclips:call_api`, show cost and balance as two numbers plus every body field under its exact key, end with "Proceed?", and send only after an explicit yes in a later message given after the preview. A yes before the preview is not consent. If the body changes for any reason, preview and ask again. If the preview says insufficient, stop.
- Several calls at once: one confirmation listing each previewed call with its cost, the total and the balance; one kind of call per confirmation; at most ten.
- A timed-out spend call may have completed: re-read with `openclips:list_creatives` before any retry, and retry only with the identical body.
- `openclips:wait_for_creative` again while it returns `stillProcessing: true`; stop on `awaiting_approval` or a failure, and never resubmit.
- Show images inline, link videos, offer a save, reply in the user's language, keep tool arguments as the API expects.
