# Connecting OpenClips

The OpenClips MCP server lives at `https://mcp.openclips.ai/mcp` and signs users in with OAuth in the browser. Always name the server `openclips` (or `OpenClips` where a display name is asked for), so tool names come out the same everywhere.

## Which state are you in?

Some hosts list MCP tools by name only until they are loaded, so search your tools for a name ending in `list_my_workspaces` before deciding anything.

| What you see | What it means | Tell the user |
|---|---|---|
| No OpenClips server anywhere | Not installed | The install step for their host, below |
| An OpenClips server with no tools, or a notice that it needs authentication | Installed, not signed in | Open `/mcp`, choose OpenClips, authenticate. Codex: `codex mcp login openclips`. claude.ai or Cowork: connect it in connector settings |
| OpenClips tools that used to work now fail with an authentication error | The sign-in expired | Sign in again the same way |
| Calls succeed | Ready | Nothing |

Installing the plugin in Claude Code registers the server but does **not** sign in, so "installed, not signed in" is normal right after install. Do not tell the user to reinstall.

## Install, per host

| Host | Step | Tool names come out as |
|---|---|---|
| Claude Code, plugin | `/plugin marketplace add https://github.com/openclips/skills`, then `/plugin install openclips@openclips`, then `/mcp` to sign in | `mcp__plugin_openclips_openclips__<tool>` |
| Cowork | Customize, then Plugins: add the marketplace `openclips/skills`, install `openclips`, sign in when prompted | `mcp__plugin_openclips_openclips__<tool>` |
| Claude Code, server only | `claude mcp add --transport http --scope user openclips https://mcp.openclips.ai/mcp`, then `/mcp` to sign in | `mcp__openclips__<tool>` |
| claude.ai chat | Customize, then Connectors: add a custom connector named `OpenClips` with the URL above, then connect. Skills do not load in chat; only the server does | `mcp__claude_ai_OpenClips__<tool>` |
| Codex | `codex mcp add openclips --url https://mcp.openclips.ai/mcp`; Codex runs the sign-in straight away, or `codex mcp login openclips` if it did not | `mcp__openclips__<tool>` |
| Cursor | Add `"openclips": {"url": "https://mcp.openclips.ai/mcp"}` under `mcpServers` in `~/.cursor/mcp.json`, then sign in when prompted | as Cursor names it |

Skills installed with `npx skills add openclips/skills` or `gh skill install openclips/skills` do not add the server. Add it with the server-only step for the host.

## Troubleshooting

- **Signed in, but calls still fail with an authentication error:** sign out and in again through `/mcp`, or disconnect and reconnect the connector.
- **Two OpenClips servers are connected:** use the one named `openclips` or `OpenClips` unless the user says otherwise, and say which one you used.
- **Never** ask the user for a token or paste one into a config file. Sign-in always happens in the browser.
