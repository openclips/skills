# Shared OpenClips rules, short form

The `openclips` hub skill carries these in full; this is the fallback when it is not installed.

- Tools are written `openclips:<tool>`; match them on the name after the last `__` or `:` on your host. If no OpenClips tool is visible, tell the user to connect the server and stop; the developer path in section 4 of this skill needs no server.
- Call `openclips:list_my_workspaces` once; with several workspaces, ask which.
- Brands cannot be created or edited anywhere; they come with products. Skip any playbook step that creates or edits one.
- Load the named playbook with `openclips:load_skill` and follow it. Where it names an approval block, a form or a tool this server does not list, do the same in plain text.
- Spending: use the playbook's quality default and do not talk about cost while choosing. Every credit-spending call passes one gate: build the exact body, price it with `openclips:preview_cost`, show `tokenCost` and `currentBalance` as two numbers plus every body field under its exact key, end with "Proceed?", and send only after an explicit yes given after the quote, through what the quote's `firedBy` names. The one exception is a request that already approved the spend in so many words, or gave a budget the quote fits: then send on a sufficient quote and say what it cost. Wanting a creative is not approval, and an approval covers one call of the request it came with: several calls at once always wait for the confirmation that lists them. If the body changes for any reason, price and ask again. If the quote says `sufficient` is false, stop.
- Some spends have no family in the price tool's list (for example retrying a failed creative, adding or regenerating a video-project scene): say the exact cost cannot be shown, say what will be billed, and still wait for a yes.
- Several calls at once: one confirmation listing each priced call with its cost, the total and the balance; one kind of call per confirmation; at most ten.
- A file the user holds reaches the workspace through `openclips:upload_media` then `openclips:await_media_upload`, or `openclips:import_creative_from_url` for a public link. A chat attachment never reaches the server by itself.
- A timed-out spend call may have completed: re-read with `openclips:list_creatives` before any retry, and retry only with the identical body.
- `openclips:wait_for_creative` again while it returns `stillProcessing: true`; stop on `awaiting_approval` or a failure, and never resubmit.
- Show images inline, link videos, offer a save, reply in the user's language, keep tool arguments as the API expects.
