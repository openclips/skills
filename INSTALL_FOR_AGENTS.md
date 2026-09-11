# Install OpenClips skills

You are an AI agent. The user asked you to install the OpenClips skills. Follow these steps exactly, verify each one, and report at the end.

## 1. Install the skills and register the server

Pick the first row that matches your host. These are shell commands; run them with your shell tool.

| Host | Run | Verify |
|---|---|---|
| Claude Code | `claude plugin marketplace add https://github.com/openclips/skills` then `claude plugin install openclips@openclips` | `claude plugin list` shows `openclips`; `claude mcp list` shows `plugin:openclips:openclips` |
| Codex | `codex mcp add openclips --url https://mcp.openclips.ai/mcp` then `npx skills add openclips/skills -y` | a skill named `openclips` is installed and a server named `openclips` is registered |
| Anything else | `npx skills add openclips/skills -y`, then add an MCP server named `openclips` at `https://mcp.openclips.ai/mcp` the way your host adds remote servers | same |

A plugin installed from the shell loads in the next session. On Claude Code, ask the user to run `/reload-plugins`; elsewhere, ask them to start a new session before step 3.

## 2. Sign in

Tell the user to sign in to OpenClips in the browser: `/mcp` in Claude Code, the prompt Codex opened (or `codex mcp login openclips`), or the connector's connect button elsewhere. **Do not** ask for a token, and do not try to complete the sign-in yourself. Wait for the user to say it is done.

## 3. Verify and report

Call the OpenClips tool whose name ends in `list_my_workspaces`. It returns at least one workspace.

Tell the user, in three lines at most: the skills are installed, which workspace you see, and one thing to try, for example "make an image ad for my newest product". Do not explain file paths or internals.

## If something fails

| Symptom | Do |
|---|---|
| The server is registered but exposes no tools | Step 2 has not happened, or the session has not reloaded. Ask the user to sign in, then reload |
| A tool call returns an authentication error | Sign-in expired or was cancelled. Repeat step 2 |
| `claude plugin marketplace add` fails with an SSH error | Use the `https://github.com/openclips/skills` form, as written above |
| The skills command fails | Say what failed and stop |
