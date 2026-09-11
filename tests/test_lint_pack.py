"""Every pack-lint rule has a passing and a failing fixture. The fixture is a
minimal valid pack built in a temp dir; each test breaks one thing."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_pack  # noqa: E402

DESC = ("Makes image ads from a product. Use when: \"make an image ad\", \"static ad\". "
        "NOT for: connecting or listing (openclips).")
HUB_DESC = ("Entry point for OpenClips. Use when: \"OpenClips\", \"show my products\". "
            "NOT for: image ads (openclips-image-ads).")


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def skill(root: Path, name: str, desc: str, body: str = "Body.\n\nRead `references/notes.md` when unsure.\n", refs=None, extra_fm: str = ""):
    write(root / "skills" / name / "SKILL.md",
          f"---\nname: {name}\ndescription: >-\n  {desc}\nlicense: MIT\n{extra_fm}---\n\n# {name}\n\n{body}")
    for ref, content in (refs if refs is not None else {"notes.md": "# Notes\n\nCall `openclips:list_products` first.\n"}).items():
        write(root / "skills" / name / "references" / ref, content)


def make_pack(tmp_path: Path) -> Path:
    root = tmp_path / "pack"
    v = "0.1.0"
    write(root / "VERSION", v + "\n")
    write(root / ".mcp.json", json.dumps({"mcpServers": {"openclips": {"type": "http", "url": "https://mcp.openclips.ai/mcp"}}}))
    write(root / ".claude-plugin" / "plugin.json", json.dumps({"name": "openclips", "version": v, "mcpServers": "./.mcp.json"}))
    write(root / ".claude-plugin" / "marketplace.json", json.dumps({"name": "openclips", "metadata": {"version": v}, "plugins": [{"name": "openclips", "source": "./", "version": v}]}))
    write(root / ".codex-plugin" / "plugin.json", json.dumps({"name": "openclips", "version": v, "skills": "./skills/"}))
    write(root / ".cursor-plugin" / "plugin.json", json.dumps({"name": "openclips", "version": v, "skills": "./skills/"}))
    write(root / "README.md", "# Pack\n\n| Skill | What |\n|---|---|\n| [`openclips`](skills/openclips/SKILL.md) | hub |\n| [`openclips-image-ads`](skills/openclips-image-ads/SKILL.md) | ads |\n\nSee [INSTALL.md](INSTALL.md).\n")
    write(root / "INSTALL.md", "# Install\n")
    write(root / ".denylist", "# one per line\nacme-secret-client\nJane Realperson\n")
    skill(root, "openclips", HUB_DESC, body="Hub.\n\nMatch tools like `mcp__openclips__list_skills` or `list_my_workspaces`.\n\nRead `references/connect.md` to connect.\n",
          refs={"connect.md": "# Connect\n\n`mcp__plugin_openclips_openclips__list_products` is fine here.\n"})
    skill(root, "openclips-image-ads", DESC)
    return root


def errors(root: Path) -> list[str]:
    return [f"{e.file}: {e.message}" for e in lint_pack.lint(root, require_denylist=True)]


def test_valid_pack_has_no_errors(tmp_path):
    assert errors(make_pack(tmp_path)) == []


# --- frontmatter ---------------------------------------------------------------

def test_unknown_frontmatter_key(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, extra_fm="argument-hint: x\n")
    assert any("argument-hint" in e for e in errors(root))


def test_allowed_tools_is_forbidden(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, extra_fm="allowed-tools: Read\n")
    assert any("allowed-tools" in e for e in errors(root))


def test_license_must_be_mit(tmp_path):
    root = make_pack(tmp_path)
    p = root / "skills/openclips-image-ads/SKILL.md"; p.write_text(p.read_text().replace("license: MIT", "license: Apache-2.0"))
    assert any("license" in e for e in errors(root))


def test_name_must_match_directory_and_prefix(tmp_path):
    root = make_pack(tmp_path)
    p = root / "skills/openclips-image-ads/SKILL.md"; p.write_text(p.read_text().replace("name: openclips-image-ads", "name: image-ads"))
    errs = errors(root)
    assert any("directory" in e for e in errs)


def test_reserved_words_and_xml_tags(tmp_path):
    root = make_pack(tmp_path)
    skill(root, "openclips-claude-helper", DESC)
    (root / "README.md").write_text((root / "README.md").read_text() + "| [`openclips-claude-helper`](skills/openclips-claude-helper/SKILL.md) | x |\n")
    assert any("reserved" in e for e in errors(root))
    root2 = make_pack(tmp_path / "b"); skill(root2, "openclips-image-ads", DESC + " <b>bold</b>")
    assert any("XML" in e for e in errors(root2))


def test_description_contract(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", "Makes image ads. NOT for: editing (openclips-edit).")
    assert any("Use when:" in e for e in errors(root))
    root = make_pack(tmp_path / "b"); skill(root, "openclips-image-ads", "Makes image ads. Use when: \"x\".")
    assert any("NOT for:" in e for e in errors(root))
    root = make_pack(tmp_path / "c"); skill(root, "openclips-image-ads", "I make image ads. Use when: \"x\". NOT for: y (openclips).")
    assert any("first person" in e for e in errors(root))
    root = make_pack(tmp_path / "d"); skill(root, "openclips-image-ads", DESC + " " + "x" * 1024)
    assert any("1024" in e for e in errors(root))


def test_description_may_name_only_real_skills(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC.replace("(openclips)", "(openclips-ghost)"))
    assert any("openclips-ghost" in e for e in errors(root))


# --- body and references -------------------------------------------------------

def test_body_length_limits(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="line\n" * 301 + "Read `references/notes.md`.\n")
    assert any("300 lines" in e for e in errors(root))


def test_reference_links_both_ways(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Read `references/missing.md`.\n", refs={"orphan.md": "# O\n"})
    errs = errors(root)
    assert any("missing.md" in e and "does not exist" in e for e in errs)
    assert any("orphan.md" in e and "not linked" in e for e in errs)


def test_no_parent_paths_no_nested_references(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="See `../openclips/SKILL.md` and `references/notes.md`.\n")
    assert any("../" in e for e in errors(root))
    root = make_pack(tmp_path / "b"); skill(root, "openclips-image-ads", DESC, refs={"notes.md": "# N\n", "deep/x.md": "# X\n"})
    assert any("deep/x.md" in e and "only SKILL.md and references" in e for e in errors(root))


def test_reference_may_not_link_another_reference(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Read `references/a.md` and `references/b.md`.\n",
                                       refs={"a.md": "# A\n\nSee `references/b.md`.\n", "b.md": "# B\n"})
    assert any("one level" in e for e in errors(root))


def test_long_reference_needs_table_of_contents(tmp_path):
    long_body = "# Big\n\n" + "\n".join(f"## Section {i}\n\ntext" for i in range(60))
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, refs={"notes.md": long_body})
    assert any("table of contents" in e for e in errors(root))
    ok = "# Big\n\n## Contents\n\n- [Section 0](#section-0)\n\n" + "\n".join(f"## Section {i}\n\ntext" for i in range(60))
    root = make_pack(tmp_path / "b"); skill(root, "openclips-image-ads", DESC, refs={"notes.md": ok})
    assert not any("table of contents" in e for e in errors(root))


# --- tool names and volatile data ----------------------------------------------

def test_bare_or_mcp_tool_names_outside_hub_are_errors(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Call `list_products` then `mcp__openclips__get_product`. Read `references/notes.md`.\n")
    errs = errors(root)
    assert any("`list_products`" in e for e in errs) and any("mcp__openclips__get_product" in e for e in errs)


def test_hub_exemption_for_resolution_note(tmp_path):
    assert errors(make_pack(tmp_path)) == []   # hub body and connect.md carry bare and mcp__ names on purpose


def test_model_names_and_prices_banned_in_bodies_but_allowed_in_description_quotes(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC + " \"use Veo\"", body="Prefer Veo 3 at 40 credits. Read `references/notes.md`.\n")
    errs = errors(root)
    assert any("Veo" in e for e in errs) and any("credits" in e for e in errs)
    root = make_pack(tmp_path / "b"); skill(root, "openclips-image-ads", DESC + " \"use Veo\"")
    assert not any("Veo" in e for e in errors(root))


# --- public-safe -----------------------------------------------------------------

def test_denylist_hits_are_errors_and_word_bounded(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="An ad for Acme-Secret-Client. Read `references/notes.md`.\n")
    assert any("denylist" in e and "acme-secret-client" in e.lower() for e in errors(root))
    root = make_pack(tmp_path / "b"); (root / "INSTALL.md").write_text("Jane Realpersonage is not a match.\n")
    assert not any("denylist" in e for e in errors(root))


# --- manifests and integrity -----------------------------------------------------

def test_version_sync(tmp_path):
    root = make_pack(tmp_path); (root / "VERSION").write_text("0.2.0\n")
    assert any("version" in e.lower() for e in errors(root))


def test_readme_and_skill_dirs_match_both_ways(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-extra", DESC)
    assert any("openclips-extra" in e and "README" in e for e in errors(root))
    root = make_pack(tmp_path / "b")
    (root / "README.md").write_text((root / "README.md").read_text() + "| [`openclips-ghost`](skills/openclips-ghost/SKILL.md) | x |\n")
    assert any("openclips-ghost" in e for e in errors(root))


def test_mcp_json_pinned(tmp_path):
    root = make_pack(tmp_path)
    (root / ".mcp.json").write_text(json.dumps({"mcpServers": {"acme": {"type": "http", "url": "https://mcp.openclips.ai/mcp"}}}))
    assert any(".mcp.json" in e for e in errors(root))


def test_relative_links_resolve(tmp_path):
    root = make_pack(tmp_path); (root / "INSTALL.md").write_text("See [x](docs/nope.md).\n")
    assert any("nope.md" in e for e in errors(root))


def test_cli_exit_code(tmp_path, capsys):
    root = make_pack(tmp_path)
    assert lint_pack.main(["--root", str(root)]) == 0
    skill(root, "openclips-image-ads", DESC, extra_fm="allowed-tools: Read\n")
    assert lint_pack.main(["--root", str(root)]) == 1
    assert "allowed-tools" in capsys.readouterr().out


# --- review follow-ups --------------------------------------------------------------

def test_reference_may_not_link_a_sibling_by_bare_name(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Read `references/a.md` and `references/b.md`.\n",
                                       refs={"a.md": "# A\n\nSee `b.md` and [also](b.md).\n", "b.md": "# B\n"})
    assert any("one level" in e and "b.md" in e for e in errors(root))


def test_missing_denylist_is_an_error_only_when_required(tmp_path):
    root = make_pack(tmp_path); (root / ".denylist").unlink()
    assert any(".denylist" in e for e in errors(root))
    assert not any(".denylist" in f"{p.file}: {p.message}" for p in lint_pack.lint(root, require_denylist=False))


def test_denylist_scans_manifests_tests_and_paths(tmp_path):
    root = make_pack(tmp_path)
    (root / ".codex-plugin" / "plugin.json").write_text(json.dumps({"name": "openclips", "version": "0.1.0", "skills": "./skills/", "interface": {"developerName": "Acme-Secret-Client"}}))
    write(root / "tests" / "fixture-jane-realperson.md", "x")
    errs = errors(root)
    assert any(".codex-plugin/plugin.json" in e and "denylist" in e for e in errs)
    assert any("fixture-jane-realperson.md" in e and "path" in e for e in errs)


def test_denylist_skips_dev_only_paths(tmp_path):
    root = make_pack(tmp_path); write(root / "docs" / "notes.md", "acme-secret-client everywhere"); write(root / "CONTEXT.md", "Jane Realperson")
    assert not any("denylist" in e for e in errors(root))


def test_model_ids_lowercase_and_hyphenated_are_caught(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Use seedance-1-0-pro or veo 3 or gpt-image-2. Read `references/notes.md`.\n")
    errs = errors(root)
    assert any("seedance" in e.lower() for e in errs)


def test_model_name_unquoted_in_description_is_caught(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC + " Prefers Veo.")
    assert any("outside a quoted" in e for e in errors(root))


def test_tool_names_inside_fenced_code_and_mid_span(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="```\nmcp__openclips__list_products()\n```\nThen `call get_product now`. Read `references/notes.md`.\n")
    errs = errors(root)
    assert any("mcp__openclips__list_products" in e for e in errs) and any("`get_product`" in e for e in errs)


def test_price_forms(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="It costs €5 or 40 USD or a 40-credit run. Read `references/notes.md`.\n")
    assert any("price" in e for e in errors(root))
    root = make_pack(tmp_path / "b"); skill(root, "openclips-image-ads", DESC, body="```bash\ncurl \"$1\"\n```\nRead `references/notes.md`.\n")
    assert not any("price" in e for e in errors(root))


def test_toc_must_be_near_the_top(tmp_path):
    body = "# Big\n\n" + "\n".join(f"## Section {i}\n\ntext" for i in range(60)) + "\n## Contents\n"
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, refs={"notes.md": body})
    assert any("table of contents" in e for e in errors(root))


def test_non_markdown_files_in_a_skill_are_errors(tmp_path):
    root = make_pack(tmp_path); write(root / "skills" / "openclips-image-ads" / "references" / "data.csv", "a,b"); write(root / "skills" / "openclips-image-ads" / "scripts" / "x.py", "print(1)")
    errs = errors(root)
    assert any("data.csv" in e for e in errs) and any("x.py" in e for e in errs)


def test_nested_link_does_not_fall_back_to_root(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, refs={"notes.md": "# N\n\nSee [install](INSTALL.md).\n"})
    assert any("INSTALL.md" in e and "does not resolve" in e for e in errors(root))


def test_missing_required_keys_and_prefix_and_semver(tmp_path):
    root = make_pack(tmp_path)
    write(root / "skills" / "openclips-image-ads" / "SKILL.md", "---\nname: openclips-image-ads\n---\n\nBody. Read `references/notes.md`.\n")
    errs = errors(root)
    assert any("missing required frontmatter key description" in e for e in errs) and any("missing required frontmatter key license" in e for e in errs)
    root = make_pack(tmp_path / "b"); skill(root, "ads", DESC)
    (root / "README.md").write_text((root / "README.md").read_text() + "| [`ads`](skills/ads/SKILL.md) | x |\n")
    assert any("start with" in e for e in errors(root))
    root = make_pack(tmp_path / "c"); (root / "VERSION").write_text("v1\n")
    assert any("semantic version" in e for e in errors(root))


def test_manifest_skill_lists_are_checked_both_ways(tmp_path):
    root = make_pack(tmp_path)
    (root / ".cursor-plugin" / "plugin.json").write_text(json.dumps({"name": "openclips", "version": "0.1.0", "skills": ["./skills/openclips", "./skills/openclips-ghost"]}))
    errs = errors(root)
    assert any("openclips-ghost" in e and "cursor" in e for e in errs) and any("openclips-image-ads is not listed" in e for e in errs)


# --- verifier follow-ups ------------------------------------------------------------

def test_ordinary_words_that_are_also_model_names_pass_in_prose(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="Show the jacket on the runway. Recraft the hook until it lands; the brief is in flux. Read `references/notes.md`.\n")
    assert not any("names the model" in e for e in errors(root))


def test_model_ids_inside_fenced_code_are_caught(tmp_path):
    root = make_pack(tmp_path); skill(root, "openclips-image-ads", DESC, body="```json\n{\"model\": \"seedance-1-0-pro\"}\n```\nRead `references/notes.md`.\n")
    assert any("seedance" in e.lower() for e in errors(root))


def test_dev_only_is_anchored_at_the_root(tmp_path):
    root = make_pack(tmp_path); write(root / "evals" / "docs" / "notes.md", "acme-secret-client"); write(root / "evals" / "CONTEXT.md", "Jane Realperson")
    errs = errors(root)
    assert any("evals/docs/notes.md" in e and "denylist" in e for e in errs) and any("evals/CONTEXT.md" in e for e in errs)


def test_denylist_scans_any_text_suffix_and_strips_inline_comments(tmp_path):
    root = make_pack(tmp_path); write(root / "evals" / "x.ndjson", '{"user": "acme-secret-client"}')
    (root / ".denylist").write_text("acme-secret-client  # the client\n")
    assert any("x.ndjson" in e and "denylist" in e for e in errors(root))
