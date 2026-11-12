#!/usr/bin/env python3
"""PreToolUse hook: approve `call_api` only for `…/preview_cost/` POSTs.

A preview spends nothing, so the hook answers `allow` for it, which lets the
call run without a permission prompt. Every other `call_api` use is blocked
(exit 2). Tools other than `call_api` are left to the permission system."""
import json
import sys


def decide(payload: dict) -> tuple[int, str, str]:
    """Returns (exit code, stdout, stderr)."""
    name = str(payload.get("tool_name", ""))
    if name.rsplit("__", 1)[-1] != "call_api":
        return 0, "", ""
    inp = payload.get("tool_input") or {}
    method = str(inp.get("method", "")).upper()
    # Ignore query and fragment so "…/generate/x/?p=/preview_cost" cannot pass.
    path = str(inp.get("path", "")).split("?", 1)[0].split("#", 1)[0]
    if method == "POST" and path.rstrip("/").endswith("/preview_cost"):
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow",
                                      "permissionDecisionReason": "preview_cost spends nothing"}}
        return 0, json.dumps(out), ""
    return 2, "", ("evals: call_api is allowed only for POST …/preview_cost/ routes in this run; "
                   f"refused {method or '?'} {path or '?'}\n")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    code, out, err = decide(payload)
    if out:
        sys.stdout.write(out)
    if err:
        sys.stderr.write(err)
    return code


if __name__ == "__main__":
    sys.exit(main())
