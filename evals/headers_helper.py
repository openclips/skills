#!/usr/bin/env python3
"""headersHelper for the OpenClips dev MCP during an eval sweep.

Claude Code runs this before connecting (and again on a 401) and expects a
JSON object of headers on stdout. Two credential routes, first match wins:

1. OPENCLIPS_MCP_TOKEN — a server-issued bearer token, used as-is.
2. OPENCLIPS_DEV_CLIENT_ID + OPENCLIPS_DEV_REFRESH_TOKEN — a refresh-token
   grant against the server's token endpoint, discovered from its
   OAuth authorization-server metadata.

Claude Code kills a helper after about ten seconds, so both HTTP calls use
short timeouts. Never prints or logs a token anywhere but stdout."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request


def discover_token_endpoint(server_url: str, fetch=None) -> str:
    fetch = fetch or _fetch_json
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(server_url))
    meta = fetch(f"{origin}/.well-known/oauth-authorization-server")
    endpoint = meta.get("token_endpoint")
    if not endpoint:
        raise SystemExit("evals: authorization-server metadata has no token_endpoint")
    return endpoint


def refresh_access_token(token_endpoint: str, client_id: str, refresh_token: str, post=None) -> str:
    post = post or _post_form
    body = post(token_endpoint, {"grant_type": "refresh_token", "client_id": client_id, "refresh_token": refresh_token})
    token = body.get("access_token")
    if not token:
        raise SystemExit("evals: token endpoint returned no access_token")
    return token


def headers(env: dict, server_url: str, fetch=None, post=None) -> dict:
    static = env.get("OPENCLIPS_MCP_TOKEN")
    if static:
        return {"Authorization": f"Bearer {static}"}
    cid, rt = env.get("OPENCLIPS_DEV_CLIENT_ID"), env.get("OPENCLIPS_DEV_REFRESH_TOKEN")
    if not (cid and rt):
        raise SystemExit("evals: set OPENCLIPS_MCP_TOKEN, or OPENCLIPS_DEV_CLIENT_ID and OPENCLIPS_DEV_REFRESH_TOKEN")
    endpoint = discover_token_endpoint(server_url, fetch)
    return {"Authorization": f"Bearer {refresh_access_token(endpoint, cid, rt, post)}"}


def _fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=4) as r:
        return json.load(r)


def _post_form(url: str, form: dict) -> dict:
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=4) as r:
        return json.load(r)


if __name__ == "__main__":
    url = os.environ.get("CLAUDE_CODE_MCP_SERVER_URL")
    if not url:
        raise SystemExit("evals: CLAUDE_CODE_MCP_SERVER_URL is not set; this helper is run by Claude Code")
    print(json.dumps(headers(os.environ, url)))
