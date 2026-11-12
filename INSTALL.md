# Installing OpenClips skills

Two things have to be true: the skills are installed, and the OpenClips MCP server is connected and signed in. Signing in always happens in your browser.

Name the server `openclips` everywhere. Tool names are derived from that name, and the skills expect it.

## Claude Code

```text
/plugin marketplace add https://github.com/openclips/skills
/plugin install openclips@openclips
/mcp
```

The plugin installs the skills and registers the server together. Choose OpenClips in `/mcp` and authenticate: installing does not sign in, so "needs authentication" right after install is normal. The `owner/repo` shorthand clones over SSH by default; the `https://` form above works without an SSH key.

Server only, without the plugin:

```bash
claude mcp add --transport http --scope user openclips https://mcp.openclips.ai/mcp
```

## Cowork

Customize, then Plugins: add the marketplace `openclips/skills`, install `openclips`, and sign in when prompted. Plugins run in Cowork and Claude Code; they do not load in claude.ai chat.

## Codex

```bash
codex mcp add openclips --url https://mcp.openclips.ai/mcp
npx skills add openclips/skills -y --skill '*' --agent codex
```

Codex starts the sign-in as soon as the server is added. If no browser prompt appears, run `codex mcp login openclips`.

## Cursor

Add the server under `mcpServers` in `~/.cursor/mcp.json`, then install the skills:

```json
{ "mcpServers": { "openclips": { "url": "https://mcp.openclips.ai/mcp" } } }
```

```bash
npx skills add openclips/skills -y --skill '*' --agent cursor
```

Sign in when Cursor prompts for it.

## claude.ai chat

Customize, then Connectors: add a custom connector named `OpenClips` with the URL `https://mcp.openclips.ai/mcp`, then connect it. Chat gets the server only; skills do not load there.

## Skills only, any host

```bash
npx skills add openclips/skills -y --skill '*' --agent '*'
# or, for Claude Code
gh skill install openclips/skills --all --agent claude-code --scope user
```

These copy the skills and do not add the server. Add it with the server step for your host above.

## Updating

```bash
/plugin update openclips@openclips   # Claude Code plugin
npx skills update -y                 # skills installed with npx
gh skill update --all                # skills installed with gh
```

## When sign-in fails

- **The server is listed but has no tools, or the host says it needs authentication:** sign in with `/mcp` (Claude Code), `codex mcp login openclips` (Codex), or reconnect the connector (claude.ai, Cowork). Do not reinstall.
- **Calls that used to work now fail with an authentication error:** the sign-in expired. Sign in again the same way.
- **Two OpenClips servers are connected:** keep the one named `openclips`.
- Never paste a token into a config file. OpenClips signs in with OAuth in the browser only.
