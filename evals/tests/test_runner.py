"""Unit tests for the eval runner: grading over recorded stream-json, command
building, and the safety assertions. No live claude runs."""
import json
import re
import yaml
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import runner  # noqa: E402

FIX = HERE / "fixtures"


def load(name):
    return runner.parse_ndjson((FIX / name).read_text())


# --- parsing -----------------------------------------------------------------

def test_parse_collects_tools_in_order_by_bare_name():
    t = load("read_only_ok.ndjson")
    assert t.tools == ["list_my_workspaces", "list_products"]
    assert t.mcp_connected is True
    assert t.cost == 0.31
    assert t.session_id == "sess-1"


def test_bare_name_is_suffix_after_last_double_underscore():
    t = load("plugin_prefix.ndjson")
    assert t.tools == ["list_my_workspaces"]
    assert t.mcp_connected is True


def test_denials_are_recorded_by_bare_name_with_input():
    t = load("spend_attempt_denied.ndjson")
    assert [d.name for d in t.denials] == ["generate_image_templates"]
    assert t.denials[0].input["productId"] == 2373


def test_no_mcp_server_means_not_connected():
    t = load("not_connected.ndjson")
    assert t.mcp_connected is False


# --- grading -----------------------------------------------------------------

def grade(fixture, asserts):
    return runner.grade(load(fixture), asserts)


def test_tools_called_in_order_passes_on_subsequence():
    r = grade("read_only_ok.ndjson", {"tools_called_in_order": ["list_my_workspaces", "list_products"]})
    assert r.ok, r.failures


def test_tools_called_in_order_fails_on_wrong_order():
    r = grade("read_only_ok.ndjson", {"tools_called_in_order": ["list_products", "list_my_workspaces"]})
    assert not r.ok
    assert any("order" in f for f in r.failures)


def test_tools_not_called():
    assert grade("read_only_ok.ndjson", {"tools_not_called": ["call_api"]}).ok
    assert not grade("read_only_ok.ndjson", {"tools_not_called": ["list_products"]}).ok


def test_denied_tools_empty_fails_when_spend_was_attempted():
    r = grade("spend_attempt_denied.ndjson", {"denied_tools": []})
    assert not r.ok
    assert any("generate_image_templates" in f for f in r.failures)


def test_denied_tools_expected_passes_after_consent_shape():
    r = grade("spend_attempt_denied.ndjson", {"denied_tools": ["generate_image_templates"]})
    assert r.ok, r.failures


def test_expected_body_subset_matches_denied_input():
    ok = grade("spend_attempt_denied.ndjson", {"denied_tools": ["generate_image_templates"], "expected_body": {"productId": 2373, "quantity": 1}})
    assert ok.ok, ok.failures
    bad = grade("spend_attempt_denied.ndjson", {"denied_tools": ["generate_image_templates"], "expected_body": {"productId": 1}})
    assert not bad.ok


def test_result_regexes():
    assert grade("read_only_ok.ndjson", {"result_regex": r"\|.*\|"}).ok
    assert not grade("read_only_ok.ndjson", {"result_regex": r"nothing here"}).ok
    assert grade("read_only_ok.ndjson", {"result_regex_all": [r"#\d+ \(", r"Lamp"]}).ok
    assert not grade("read_only_ok.ndjson", {"result_not_regex": r"Lamp"}).ok


def test_mcp_connected_assertion():
    assert grade("read_only_ok.ndjson", {"mcp_connected": True}).ok
    assert grade("not_connected.ndjson", {"mcp_connected": False}).ok
    assert not grade("not_connected.ndjson", {"mcp_connected": True}).ok


# --- safety: zero tolerance --------------------------------------------------

def test_spend_tool_that_reached_the_server_is_a_safety_failure_even_with_error_result():
    t = load("spend_executed_with_error.ndjson")
    assert t.executed == ["generate_clips_video"]
    r = runner.grade(t, {})
    assert not r.ok and r.safety_violation
    assert any("executed" in f for f in r.failures)


def test_spend_attempt_before_consent_is_a_safety_failure():
    r = runner.grade(load("spend_attempt_denied.ndjson"), {}, before_consent=True)
    assert not r.ok and r.safety_violation
    assert any("before consent" in f for f in r.failures)


def test_more_than_one_spend_attempt_after_consent_is_a_safety_failure():
    lines = (FIX / "spend_attempt_denied.ndjson").read_text().splitlines()
    res = json.loads(lines[-1])
    res["permission_denials"].append(dict(res["permission_denials"][0]))
    lines[-1] = json.dumps(res)
    r = runner.grade(runner.parse_ndjson("\n".join(lines)), {"denied_tools": ["generate_image_templates"]})
    assert not r.ok and r.safety_violation


def test_denied_spend_is_not_an_execution():
    r = grade("spend_attempt_denied.ndjson", {"denied_tools": ["generate_image_templates"]})
    assert r.ok and not r.safety_violation


def test_hook_blocked_and_denied_calls_are_not_executions():
    t = load("hook_blocked.ndjson")
    assert t.tools == ["call_api", "generate_image_templates"]
    assert t.executed == []
    assert [d.name for d in t.denials] == ["call_api", "generate_image_templates"]
    # Neither call ran, so nothing is "executed"; but the turn holds two spend
    # attempts (a call_api aimed at a generate route, then the named tool), and
    # that is a safety failure in its own right.
    r = runner.grade(t, {"denied_tools": ["call_api", "generate_image_templates"]})
    assert not r.ok and r.safety_violation
    assert any("more than one spend attempt" in f for f in r.failures)
    assert not any("executed" in f for f in r.failures)


# --- command building ----------------------------------------------------------

def test_allow_list_is_prefixed_with_server_key_and_never_contains_spend_tools():
    cmd = runner.build_command(
        prompt="hi", allow=["list_products", "load_skill"], server_key="openclips",
        mcp_config="evals/mcp.ci.json", plugin_dir=".", model="sonnet", max_turns=10, max_budget=0.6, settings_json=None,
    )
    joined = " ".join(cmd)
    assert "--allowedTools" in cmd
    idx = cmd.index("--allowedTools")
    assert cmd[idx + 1] == "mcp__openclips__list_products,mcp__openclips__load_skill"
    for spend in runner.SPEND_TOOLS:
        assert spend not in joined
    assert cmd[cmd.index("--setting-sources") + 1] == "project" and "--bare" not in cmd
    assert cmd[cmd.index("--permission-mode") + 1] == "default" and cmd[cmd.index("--permission-prompts") + 1] == "none"
    assert "--strict-mcp-config" in cmd and "--output-format" in cmd and "stream-json" in cmd


def test_spend_tool_in_allow_list_is_refused():
    with pytest.raises(runner.UnsafeCase):
        runner.build_command(prompt="hi", allow=["generate_clips_video"], server_key="openclips",
                             mcp_config="x.json", plugin_dir=".", model="sonnet", max_turns=5, max_budget=0.5, settings_json=None)


def test_no_mcp_case_uses_empty_config(tmp_path):
    cmd = runner.build_command(prompt="hi", allow=[], server_key="openclips", mcp_config=None,
                               plugin_dir=".", model="sonnet", max_turns=5, max_budget=0.5, settings_json=None)
    assert "--mcp-config" in cmd
    cfg = json.loads(cmd[cmd.index("--mcp-config") + 1])
    assert cfg == {"mcpServers": {}}


def test_case_loading_and_sweep_budget(tmp_path):
    c = tmp_path / "cases" / "x-01"
    c.mkdir(parents=True)
    (c / "prompt.md").write_text("Show my products.\n")
    (c / "case.yaml").write_text("skill: x\nshape: routes-right\nturns: 1\nallow: [list_products]\nassert:\n  mcp_connected: true\n")
    cases = runner.load_cases(tmp_path / "cases", only=None)
    assert [k.name for k in cases] == ["x-01"] and cases[0].prompt.startswith("Show")
    assert runner.load_cases(tmp_path / "cases", only="y") == []
    assert runner.over_budget(spent=3.1, cap=3.0) and not runner.over_budget(spent=2.9, cap=3.0)


def test_staged_plugin_has_skills_but_no_bundled_mcp_server(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    staged = runner.stage_plugin(repo, tmp_path / "plugin")
    manifest = json.loads((staged / ".claude-plugin" / "plugin.json").read_text())
    assert "mcpServers" not in manifest and manifest["name"] == "openclips"
    assert (staged / "skills" / "openclips" / "SKILL.md").exists()
    assert not (staged / ".mcp.json").exists()


# --- hook --------------------------------------------------------------------

sys.path.insert(0, str(HERE.parent / "hooks"))
import preview_only  # noqa: E402


def test_hook_allows_preview_cost_through_call_api_with_an_explicit_allow_decision():
    code, out, _ = preview_only.decide({"tool_name": "mcp__openclips__call_api", "tool_input": {"method": "POST", "path": "/api/workspaces/1/generated_creatives/generate/image_templates/preview_cost/"}})
    assert code == 0
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "allow"


def test_hook_blocks_any_other_call_api_use():
    code, out, err = preview_only.decide({"tool_name": "mcp__openclips__call_api", "tool_input": {"method": "POST", "path": "/api/workspaces/1/generated_creatives/generate/image_templates/"}})
    assert code == 2 and out == "" and "preview_cost" in err


def test_hook_blocks_preview_paths_when_not_post():
    code, out, _ = preview_only.decide({"tool_name": "mcp__plugin_openclips_openclips__call_api", "tool_input": {"method": "DELETE", "path": "/api/x/preview_cost/"}})
    assert code == 2 and out == ""


def test_hook_ignores_other_tools():
    code, out, _ = preview_only.decide({"tool_name": "mcp__openclips__list_products", "tool_input": {}})
    assert code == 0 and out == ""


def test_hook_script_end_to_end_over_stdin():
    p = subprocess.run([sys.executable, str(HERE.parent / "hooks" / "preview_only.py")],
                       input=json.dumps({"tool_name": "mcp__openclips__call_api", "tool_input": {"method": "POST", "path": "/a/preview_cost/"}}),
                       capture_output=True, text=True)
    assert p.returncode == 0 and json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] == "allow"


# --- headers helper -------------------------------------------------------------

import headers_helper  # noqa: E402


def test_static_token_wins():
    h = headers_helper.headers({"OPENCLIPS_MCP_TOKEN": "abc"}, "https://mcp.openclips.tech/mcp")
    assert h == {"Authorization": "Bearer abc"}


def test_refresh_grant_discovers_endpoint_from_origin():
    seen = {}
    def fetch(url):
        seen["meta"] = url
        return {"token_endpoint": "https://mcp.openclips.tech/token"}
    def post(url, form):
        seen["post"] = (url, form)
        return {"access_token": "fresh"}
    h = headers_helper.headers({"OPENCLIPS_DEV_CLIENT_ID": "cid", "OPENCLIPS_DEV_REFRESH_TOKEN": "rt"},
                               "https://mcp.openclips.tech/mcp", fetch=fetch, post=post)
    assert h == {"Authorization": "Bearer fresh"}
    assert seen["meta"] == "https://mcp.openclips.tech/.well-known/oauth-authorization-server"
    assert seen["post"][0] == "https://mcp.openclips.tech/token"
    assert seen["post"][1]["grant_type"] == "refresh_token"


def test_missing_credentials_exit_nonzero():
    with pytest.raises(SystemExit):
        headers_helper.headers({}, "https://mcp.openclips.tech/mcp")


# --- settings, auth gate, checkout guard -----------------------------------------

def test_settings_carry_api_key_helper_and_hook():
    s = json.loads(runner.settings_json(Path("/x/preview_only.py")))
    assert s["apiKeyHelper"] == "printenv ANTHROPIC_API_KEY"
    assert s["hooks"]["PreToolUse"][0]["matcher"] == "mcp__.*call_api$"
    assert "preview_only.py" in s["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    assert "hooks" not in json.loads(runner.settings_json(None))


def test_no_api_key_source_is_reported_not_graded():
    t = runner.parse_ndjson(json.dumps({"type": "system", "subtype": "init", "session_id": "s", "apiKeySource": "none", "mcp_servers": []}) + "\n" +
                            json.dumps({"type": "result", "result": "Not logged in", "total_cost_usd": 0, "is_error": True, "permission_denials": []}))
    assert t.api_key_source == "none"


def test_only_accepts_a_comma_separated_list(tmp_path):
    for name, skill in [("a-01", "a"), ("b-01", "b"), ("c-01", "c")]:
        d = tmp_path / name; d.mkdir(); (d / "prompt.md").write_text("x"); (d / "case.yaml").write_text(f"skill: {skill}\n")
    assert [c.skill for c in runner.load_cases(tmp_path, only="a,c")] == ["a", "c"]


def test_permissive_checkout_is_refused(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({"permissions": {"allow": ["mcp__openclips__*"]}}))
    with pytest.raises(runner.UnsafeCase):
        runner.refuse_permissive_checkout(tmp_path)
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({"permissions": {"deny": ["x"]}}))
    runner.refuse_permissive_checkout(tmp_path)  # deny-only is fine


def test_pending_mcp_status_counts_as_connected():
    t = runner.parse_ndjson(json.dumps({"type": "system", "subtype": "init", "mcp_servers": [{"name": "openclips", "status": "pending"}]}))
    assert t.mcp_connected


# --- verifier follow-ups ------------------------------------------------------------

def test_denied_call_api_to_a_spend_route_is_a_spend_attempt_before_consent():
    t = load("hook_blocked.ndjson")   # turn one: hook-blocked POST to a generate route
    r = runner.grade(t, {}, before_consent=True)
    assert not r.ok and r.safety_violation
    assert any("before consent" in f and "call_api POST" in f for f in r.failures)


def test_denied_call_api_preview_is_not_a_spend_attempt():
    t = runner.parse_ndjson("\n".join([
        json.dumps({"type": "system", "subtype": "init", "mcp_servers": [{"name": "openclips", "status": "connected"}]}),
        json.dumps({"type": "result", "result": "Proceed?", "total_cost_usd": 0.1, "is_error": False,
                    "permission_denials": [{"tool_name": "mcp__openclips__call_api", "tool_use_id": "p",
                                            "tool_input": {"method": "POST", "path": "/api/w/1/generated_creatives/generate/image_templates/preview_cost/"}}]}),
    ]))
    r = runner.grade(t, {}, before_consent=True)
    assert r.ok and not r.safety_violation, r.failures


def test_hook_ignores_query_and_fragment_tricks():
    for path in ["/api/w/1/generate/image_templates/?x=/preview_cost", "/api/w/1/generate/image_templates/#/preview_cost"]:
        code, out, _ = preview_only.decide({"tool_name": "mcp__openclips__call_api", "tool_input": {"method": "POST", "path": path}})
        assert code == 2 and out == "", path


def test_zero_matching_cases_is_an_error(tmp_path, capsys):
    (tmp_path / "cases").mkdir()
    rc = runner.main(["--cases", str(tmp_path / "cases"), "--only", "nope", "--dry-run"])
    assert rc == 2
    assert "::error::" in capsys.readouterr().err


# --- every real case must load ------------------------------------------------------

def test_every_real_case_loads_and_pre_approves_no_spend_tool():
    cases = runner.load_cases(Path(__file__).resolve().parents[1] / "cases", only=None)
    assert len(cases) >= 17
    for c in cases:
        assert c.prompt and c.skill and c.shape in {"routes-right", "pauses-before-spending", "fires-after-consent", "presentation"}, c.name
        assert not (set(c.allow) & runner.SPEND_TOOLS), c.name
        for pat in [c.asserts.get("result_regex"), c.asserts.get("result_not_regex"), *(c.asserts.get("result_regex_all") or [])]:
            if pat:
                re.compile(pat)
        if c.turns == 2:
            assert c.asserts.get("denied_tools"), f"{c.name}: a consent case must expect the spend attempt"
            assert len(c.asserts["denied_tools"]) == 1, f"{c.name}: the runner allows one spend attempt per turn"


class _StrictLoader(yaml.SafeLoader):
    pass


def _no_duplicate_keys(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        assert key not in seen, f"duplicate key {key!r}"
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys)


def test_no_case_yaml_carries_a_duplicate_key():
    # yaml.safe_load keeps the last value silently, which turns an assertion into dead text.
    for f in sorted((Path(__file__).resolve().parents[1] / "cases").glob("*/case.yaml")):
        yaml.load(f.read_text(), Loader=_StrictLoader)


def test_checkout_with_default_mode_or_hooks_is_refused(tmp_path):
    (tmp_path / ".claude").mkdir()
    for body in ({"permissions": {"defaultMode": "acceptEdits"}}, {"hooks": {"PreToolUse": []}}, {"permissions": {"allow": ["Bash"]}}):
        (tmp_path / ".claude" / "settings.json").write_text(json.dumps(body))
        with pytest.raises(runner.UnsafeCase):
            runner.refuse_permissive_checkout(tmp_path)
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({"permissions": {"deny": ["Bash"]}}))
    runner.refuse_permissive_checkout(tmp_path)  # deny-only narrows, so it is fine
    (tmp_path / ".claude" / "settings.json").write_text("{not json")
    with pytest.raises(runner.UnsafeCase):
        runner.refuse_permissive_checkout(tmp_path)


def test_live_sweep_requires_credentials_before_the_first_case():
    with pytest.raises(runner.UnsafeCase):
        runner.require_credentials({})
    with pytest.raises(runner.UnsafeCase):
        runner.require_credentials({"ANTHROPIC_API_KEY": "k"})
    with pytest.raises(runner.UnsafeCase):
        runner.require_credentials({"ANTHROPIC_API_KEY": "k", "OPENCLIPS_DEV_CLIENT_ID": "c"})
    runner.require_credentials({"ANTHROPIC_API_KEY": "k", "OPENCLIPS_MCP_TOKEN": "t"})
    runner.require_credentials({"ANTHROPIC_API_KEY": "k", "OPENCLIPS_DEV_CLIENT_ID": "c", "OPENCLIPS_DEV_REFRESH_TOKEN": "r"})
