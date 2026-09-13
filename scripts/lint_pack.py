#!/usr/bin/env python3
"""Pack lint: the rules no external validator checks.

Decided in the CI gate set (issue #15). Every rule is an error. Run from the
repo root: `python3 scripts/lint_pack.py`. In the private development repo add
`--require-denylist`, which makes a missing `.denylist` an error; the public
mirror does not carry that file and skips the check with a notice.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REQUIRED_KEYS = {"name", "description", "license"}
HUB = "openclips"
PREFIX = "openclips-"
RESERVED = ("anthropic", "claude")
MCP_URL = "https://mcp.openclips.ai/mcp"
DENYLIST = ".denylist"
# Never published, so never scanned for denylist terms or links.
DEV_ONLY = ("docs", "CONTEXT.md", ".denylist", ".claude", ".git", "__pycache__", "evals/results", "evals/results-ablation")
# Files that may carry host-specific or bare tool names on purpose: the hub's
# resolution note tells the agent how to match tools across hosts.
TOOL_NAME_EXEMPT = {"skills/openclips/SKILL.md", "skills/openclips/references/connect.md"}

# Snapshot of the OpenClips MCP tool names (prod server, 2026-09-11). Update when the server adds one.
TOOLS = {
    "list_my_workspaces", "list_brands", "get_brand", "list_products", "get_product", "get_product_by_url",
    "create_product", "update_product", "start_product_analysis", "await_product", "list_avatars", "get_avatar",
    "list_creatives", "get_creative", "generate_image_templates", "generate_clips_video", "generate_marketplace_proxy",
    "generate_competitor_recreate", "enhance_asset_proxy", "revise_creative_variate", "revise_creative_resize",
    "revise_creative_translate", "revise_creative_upscale", "watermark_creative", "clips_catalog",
    "marketplace_models", "list_skills", "load_skill", "list_endpoints", "call_api", "wait_for_creative",
    "query_user_events",
}
# Model ids that are never ordinary words: matched in any case.
MODEL_IDS = ("seedream", "seedance", "kling", "hailuo", "minimax", "midjourney", "hunyuan", "happyhorse", "pixverse",
             "gpt[- ]?image", "z[- ]?image", "nano[- ]?banana", "dall[- ]?e", "wan[- ]?2", "veo[- ]?\\d")
# Families that are also English words: matched only Capitalised, or followed by a version or id token.
MODEL_WORDS = ("Veo", "Runway", "Grok", "Ideogram", "Recraft", "Gemini", "Sora", "Luma", "Flux", "Imagen", "Pika", "Vidu")
_VERSIONED = "|".join(w.lower() for w in MODEL_WORDS)
_MODEL_ID_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(MODEL_IDS) + r")(?![A-Za-z])", re.I)
# Capitalised only mid-sentence, so a sentence that starts with "Recraft" or "Flux" is still English.
_MODEL_CAP_RE = re.compile(r"(?<=[a-z0-9,;] )(" + "|".join(MODEL_WORDS) + r")(?![a-z])")
_MODEL_VER_RE = re.compile(r"(?<![A-Za-z0-9])(" + _VERSIONED + r")(?=[ -]?v?\d|-(?:pro|dev|fast|turbo|kontext|max|mini)\b)", re.I)


def model_hit(text: str):
    """A model name where one is not allowed, or None."""
    for rx in (_MODEL_ID_RE, _MODEL_CAP_RE, _MODEL_VER_RE):
        m = rx.search(text)
        if m:
            return m
    return None


PRICE_RE = re.compile(
    r"(\b\d[\d,.]*\s*(credits?|tokens?)\b|\b\d[\d,.]*-credit\b|[$€£]\s?\d[\d,.]*\b|\b\d[\d,.]*\s?(USD|EUR|GBP)\b)", re.I)
TOOL_WORD_RE = re.compile(r"(?<![A-Za-z0-9_:])(" + "|".join(sorted(TOOLS, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")
MCP_NAME_RE = re.compile(r"\bmcp__[A-Za-z0-9_:-]+")
MAX_BODY_LINES = 300
MAX_BODY_CHARS = 20_000   # about 5,000 tokens
TOC_LINES = 100
TOC_WINDOW = 20


@dataclass
class Problem:
    file: str
    message: str


def _rel(root: Path, p: Path) -> str:
    return str(p.relative_to(root))


def _dev_only(rel: str) -> bool:
    parts = rel.split("/")
    if ".git" in parts or "__pycache__" in parts:
        return True
    return any(rel == d or rel.startswith(d + "/") for d in DEV_ONLY)


def _split(text: str) -> tuple[dict | None, str, str | None]:
    if not text.startswith("---\n"):
        return None, text, "frontmatter must start at byte 0 with ---"
    try:
        fm, body = text[4:].split("\n---\n", 1)
    except ValueError:
        return None, text, "frontmatter is not closed with ---"
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        return None, body, f"frontmatter is not valid YAML: {e}"
    if not isinstance(data, dict):
        return None, body, "frontmatter is not a mapping"
    return data, body, None


def _md_links(text: str) -> list[str]:
    out = [m.group(1) for m in re.finditer(r"\]\(\s*([^)\s#]+)(?:#[^)]*)?(?:\s+\"[^\"]*\")?\s*\)", text)]
    out += [m.group(1) for m in re.finditer(r"^\s*\[[^\]]+\]:\s*(\S+)", text, re.M)]
    return out


def _code(text: str) -> tuple[list[str], str]:
    """All code (inline spans and fenced blocks) and the prose with fences removed."""
    fenced = re.findall(r"```[^\n]*\n(.*?)```", text, re.S)
    prose = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)
    spans = re.findall(r"`([^`\n]+)`", prose)
    return spans + fenced, prose


def _strip_quotes(text: str) -> str:
    return re.sub(r"\"[^\"]*\"|“[^”]*”", "", text)


def lint_skill(root: Path, d: Path, names: set[str], problems: list[Problem]) -> None:
    sk = d / "SKILL.md"
    rel = _rel(root, sk)
    if not sk.exists():
        problems.append(Problem(_rel(root, d), "no SKILL.md"))
        return
    text = sk.read_text()
    fm, body, err = _split(text)
    if err:
        problems.append(Problem(rel, err))
        return

    # frontmatter
    extra = set(fm) - SPEC_KEYS
    if extra:
        problems.append(Problem(rel, f"unknown frontmatter key(s) {sorted(extra)}; only the six spec keys are allowed"))
    if "allowed-tools" in fm:
        problems.append(Problem(rel, "allowed-tools must not be set (it pre-approves tools; decided in the tool-name ticket)"))
    for k in sorted(REQUIRED_KEYS - set(fm)):
        problems.append(Problem(rel, f"missing required frontmatter key {k}"))
    if fm.get("license") not in (None, "MIT"):
        problems.append(Problem(rel, f"license must be MIT, got {fm.get('license')!r}"))
    name = str(fm.get("name", ""))
    desc = str(fm.get("description", "") or "").strip()
    if name != d.name:
        problems.append(Problem(rel, f"name {name!r} must equal the directory name {d.name!r}"))
    if not (name == HUB or name.startswith(PREFIX)):
        problems.append(Problem(rel, f"name must be {HUB!r} or start with {PREFIX!r}"))
    if any(w in name for w in RESERVED):
        problems.append(Problem(rel, f"name contains a reserved word ({', '.join(RESERVED)})"))
    if re.search(r"<[a-zA-Z/][^>]*>", name + " " + desc):
        problems.append(Problem(rel, "XML tags are not allowed in name or description"))
    if len(desc) > 1024:
        problems.append(Problem(rel, f"description is {len(desc)} characters; the limit is 1024"))
    if "Use when:" not in desc:
        problems.append(Problem(rel, "description must contain the literal 'Use when:' followed by quoted user phrasings"))
    if "NOT for:" not in desc:
        problems.append(Problem(rel, "description must contain the literal 'NOT for:' naming the sibling that owns each case"))
    if re.match(r"^(I|You)\b", desc):
        problems.append(Problem(rel, "description must be third person, not first person or second person"))
    for mentioned in sorted(set(re.findall(r"\bopenclips-[a-z0-9-]+\b", desc))):
        if mentioned not in names:
            problems.append(Problem(rel, f"description names {mentioned}, which is not a skill in this pack"))
    m = model_hit(_strip_quotes(desc))
    if m:
        problems.append(Problem(rel, f"description names the model {m.group(0)!r} outside a quoted user phrase"))

    # body
    lines = body.splitlines()
    if len(lines) > MAX_BODY_LINES:
        problems.append(Problem(rel, f"body is {len(lines)} lines; the limit is {MAX_BODY_LINES} lines"))
    if len(body) > MAX_BODY_CHARS:
        problems.append(Problem(rel, f"body is about {len(body) // 4} tokens; keep it under 5,000"))

    # every file in the skill: no ../, and only SKILL.md plus markdown references
    for p in sorted(x for x in d.rglob("*") if x.is_file()):
        prel = _rel(root, p)
        if "../" in p.read_text(errors="replace"):
            problems.append(Problem(prel, "no ../ paths anywhere in a skill"))
        if p == sk:
            continue
        if p.parent != d / "references":
            problems.append(Problem(prel, "a skill holds only SKILL.md and references/*.md"))
        elif p.suffix != ".md":
            problems.append(Problem(prel, "references/ holds markdown only"))

    # references, both directions, one level deep
    refs_dir = d / "references"
    linked = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", body))
    existing = {p.name for p in refs_dir.glob("*.md")} if refs_dir.exists() else set()
    for r in sorted(existing):
        p = refs_dir / r
        rtext = p.read_text()
        prel = _rel(root, p)
        siblings = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", rtext))
        siblings |= {t.split("/")[-1] for t in _md_links(rtext) if t.split("/")[-1] in existing}
        siblings |= {s for s in re.findall(r"`(?:\./)?([A-Za-z0-9_.-]+\.md)`", rtext) if s in existing}
        if siblings - {r}:
            problems.append(Problem(prel, f"links another reference {sorted(siblings - {r})}; keep references one level deep from SKILL.md"))
        n = len(rtext.splitlines())
        head = "\n".join(rtext.splitlines()[:TOC_WINDOW])
        if n > TOC_LINES and not (re.search(r"^#{1,3}\s*(Contents|Table of contents)\b", head, re.M | re.I)
                                  or re.search(r"^\s*(?:[-*]|\d+\.)\s*\[[^\]]+\]\(#[^)]+\)", head, re.M)):
            problems.append(Problem(prel, f"{n} lines: reference files over {TOC_LINES} lines open with a table of contents"))
        check_tool_names(root, p, rtext, problems)
        check_volatile(root, p, rtext, problems)
    for r in sorted(linked - existing):
        problems.append(Problem(rel, f"links references/{r}, which does not exist"))
    for r in sorted(existing - linked):
        problems.append(Problem(_rel(root, refs_dir / r), "not linked from SKILL.md (every reference needs a when-to-read pointer)"))

    check_tool_names(root, sk, body, problems)
    check_volatile(root, sk, body, problems)


def check_tool_names(root: Path, p: Path, text: str, problems: list[Problem]) -> None:
    rel = _rel(root, p)
    if rel in TOOL_NAME_EXEMPT:
        return
    code, _ = _code(text)
    for span in code:
        for m in MCP_NAME_RE.finditer(span):
            problems.append(Problem(rel, f"`{m.group(0)}` is a host-specific tool name; write openclips:<tool>"))
        for m in TOOL_WORD_RE.finditer(span):
            problems.append(Problem(rel, f"`{m.group(1)}` is a bare tool name; write openclips:{m.group(1)}"))


def check_volatile(root: Path, p: Path, text: str, problems: list[Problem]) -> None:
    rel = _rel(root, p)
    _, prose = _code(text)
    m = model_hit(text)
    if m:
        problems.append(Problem(rel, f"names the model {m.group(0)!r}; models come from openclips:marketplace_models at run time"))
    m = PRICE_RE.search(prose)
    if m:
        problems.append(Problem(rel, f"carries a price or credit figure ({m.group(0).strip()!r}); costs come from preview_cost at run time"))


def published_files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*"):
        rel = _rel(root, p)
        if _dev_only(rel) or not p.is_file():
            continue
        out.append(p)
    return out


def check_denylist(root: Path, problems: list[Problem], required: bool) -> None:
    dl = root / DENYLIST
    if not dl.exists():
        if required:
            problems.append(Problem(DENYLIST, "missing (the dev-only public-safe denylist is required here)"))
        else:
            print(f"notice: {DENYLIST} not present; public-safe denylist check skipped", file=sys.stderr)
        return
    terms = [t.split("#", 1)[0].strip() for t in dl.read_text().splitlines()]
    terms = [t for t in terms if t]
    pats = [(t, re.compile(r"(?<![A-Za-z0-9])" + re.escape(t).replace(r"\ ", r"[\s_-]+") + r"(?![A-Za-z0-9])", re.I)) for t in terms]
    for f in published_files(root):
        rel = _rel(root, f)
        for term, pat in pats:
            if pat.search(rel):
                problems.append(Problem(rel, f"denylist hit in the path: {term!r} (public-safe rule)"))
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue   # binary
        for term, pat in pats:
            if pat.search(text):
                problems.append(Problem(rel, f"denylist hit: {term!r} (public-safe rule)"))


def check_manifests(root: Path, skill_names: set[str], problems: list[Problem]) -> None:
    vfile = root / "VERSION"
    if not vfile.exists():
        problems.append(Problem("VERSION", "missing"))
        return
    version = vfile.read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?", version):
        problems.append(Problem("VERSION", f"{version!r} is not a semantic version"))

    def load(rel: str) -> dict | None:
        p = root / rel
        if not p.exists():
            problems.append(Problem(rel, "missing"))
            return None
        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError as e:
            problems.append(Problem(rel, f"invalid JSON: {e}"))
            return None

    def skills_field(rel: str, d: dict) -> None:
        s = d.get("skills")
        if isinstance(s, str) and not (root / s).exists():
            problems.append(Problem(rel, f"skills path {s!r} does not exist"))
        elif isinstance(s, list):
            listed = {(x.get("name") if isinstance(x, dict) else str(x)).split("/")[-1] for x in s}
            for n in sorted(skill_names - listed):
                problems.append(Problem(rel, f"skill {n} is not listed"))
            for n in sorted(listed - skill_names):
                problems.append(Problem(rel, f"lists {n}, which is not a skill directory"))

    for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        d = load(rel)
        if d is None:
            continue
        if d.get("version") != version:
            problems.append(Problem(rel, f"version {d.get('version')!r} differs from VERSION {version!r}"))
        if d.get("name") != "openclips":
            problems.append(Problem(rel, "plugin name must be 'openclips'"))
        skills_field(rel, d)
    m = load(".claude-plugin/marketplace.json")
    if m is not None:
        for pl in m.get("plugins") or []:
            if pl.get("version") != version:
                problems.append(Problem(".claude-plugin/marketplace.json", f"plugin version {pl.get('version')!r} differs from VERSION {version!r}"))
            if isinstance(pl, dict):
                skills_field(".claude-plugin/marketplace.json", pl)
        mv = (m.get("metadata") or {}).get("version")
        if mv is not None and mv != version:
            problems.append(Problem(".claude-plugin/marketplace.json", f"metadata.version {mv!r} differs from VERSION {version!r}"))
        if m.get("name") != "openclips":
            problems.append(Problem(".claude-plugin/marketplace.json", "marketplace name must be 'openclips'"))
    mcp = load(".mcp.json")
    if mcp is not None:
        servers = mcp.get("mcpServers") or {}
        if list(servers) != ["openclips"] or servers.get("openclips", {}).get("url") != MCP_URL:
            problems.append(Problem(".mcp.json", f"must declare exactly one server keyed 'openclips' at {MCP_URL}"))

    readme = root / "README.md"
    if readme.exists():
        listed = set(re.findall(r"\[`?(openclips[a-z0-9-]*)`?\]\(\.?/?skills/", readme.read_text()))
        for n in sorted(skill_names - listed):
            problems.append(Problem("README.md", f"skill {n} is not in the README skills table"))
        for n in sorted(listed - skill_names):
            problems.append(Problem("README.md", f"README lists {n}, which is not a skill directory"))
        if len(listed) != len(skill_names):
            problems.append(Problem("README.md", f"README lists {len(listed)} skills; skills/ has {len(skill_names)}"))
    else:
        problems.append(Problem("README.md", "missing"))


def check_links(root: Path, problems: list[Problem]) -> None:
    for f in published_files(root):
        if f.suffix != ".md":
            continue
        for target in _md_links(f.read_text()):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            base = root if target.startswith("/") else f.parent
            if not (base / target.lstrip("/")).exists():
                problems.append(Problem(_rel(root, f), f"link target {target!r} does not resolve from this file"))


def lint(root: Path, require_denylist: bool = False) -> list[Problem]:
    problems: list[Problem] = []
    skills_dir = root / "skills"
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.exists() else []
    names = {p.name for p in dirs}
    for d in dirs:
        lint_skill(root, d, names, problems)
    check_manifests(root, names, problems)
    check_denylist(root, problems, require_denylist)
    check_links(root, problems)
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--require-denylist", action="store_true", help="fail if .denylist is absent (dev repo)")
    args = ap.parse_args(argv)
    problems = lint(Path(args.root).resolve(), args.require_denylist)
    for p in problems:
        print(f"{p.file}: {p.message}")
    print(f"{len(problems)} problem(s)" if problems else "pack lint: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
