from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONTRACT = ROOT / ".github" / "readme_design_contract.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized_public_text() -> str:
    return read(README).replace("**", "").replace(chr(96), "").replace("_", " ")


def test_approved_icon_is_byte_stable() -> None:
    contract = json.loads(read(CONTRACT))
    icon_path = ROOT / contract["suite_visual_shell"]["approved_icon_path"]
    data = icon_path.read_bytes()
    git_blob = hashlib.sha1(
        f"blob {len(data)}\0".encode("ascii") + data
    ).hexdigest()
    assert git_blob == contract["suite_visual_shell"]["approved_icon_git_blob_sha"]


def test_public_readme_header_is_suite_consistent() -> None:
    text = read(README)
    header = text.split("---", 1)[0]
    contract = json.loads(read(CONTRACT))
    assert 'width="112"' in header
    assert len(re.findall(r"<img alt=", header)) == 3
    assert "CBD validation" in header
    assert "MIT / CC BY 4.0" in header

    nav_match = re.search(r'<p align="center"><small>\s*(.*?)\s*</small></p>', header, re.S)
    assert nav_match is not None
    assert len(re.findall(r'<a href=', nav_match.group(1))) <= contract["public_readme_quality_budget"]["maximum_quick_navigation_links"]

    assert "event-driven cognitive state-transition and agent-level stochastic dynamical model" not in header.lower()
    assert "A research model for studying how information exposure, memory, corrective context" in header


def test_public_readme_first_section_stays_compact() -> None:
    text = read(README)
    contract = json.loads(read(CONTRACT))
    intro = text.split("### What is CBD?", 1)[1].split("### Research purpose", 1)[0]
    paragraphs = [
        block.strip()
        for block in re.split(r"\n\s*\n", intro)
        if block.strip() and not block.strip().startswith("<")
    ]
    assert len(paragraphs) <= contract["public_readme_quality_budget"]["maximum_intro_paragraphs"]
    intro_plain = re.sub(r"<[^>]+>", " ", intro)
    intro_words = re.findall(r"\b[\w][\w./+-]*\b", intro_plain)
    assert len(intro_words) <= contract["public_readme_quality_budget"]["maximum_intro_words"]


def test_public_readme_follows_reader_oriented_information_order() -> None:
    text = read(README)
    sections = (
        "### What is CBD?",
        "### Research purpose",
        "### Conceptual model",
        "### Research questions CBD can explore",
        "### Scientific foundations",
        "### Current capabilities and scientific limits",
        "### Research direction",
        "### Using and reproducing CBD",
        "### Where to go next",
        "### Support, citation and license",
    )
    positions = [text.index(section) for section in sections]
    assert positions == sorted(positions)


def test_public_readme_avoids_internal_development_identifiers() -> None:
    text = normalized_public_text()
    contract = json.loads(read(CONTRACT))
    for token in contract["public_readme_forbidden_internal_terms"]:
        assert token.lower() not in text.lower()


def test_public_readme_explains_current_model_and_scientific_boundaries() -> None:
    text = normalized_public_text().lower()
    required = (
        "event-driven cognitive state-transition and agent-level stochastic dynamical model",
        "not currently a formal system dynamics model",
        "sequence of information-related events is supplied from outside the model",
        "decisions can remain probabilistic while simulations remain reproducible",
        "not currently a validated predictor of individual or population human behavior",
        "a truth detector, a diagnostic system or an automatic judge",
        "do not by themselves establish human validation",
        "not every concept documented in cbd is currently implemented in the simulator",
    )
    for token in required:
        assert token in text


def test_public_readme_routes_audit_detail_to_reference_files() -> None:
    text = read(README)
    assert "[STATUS.md](STATUS.md)" in text
    assert "[DEVELOPMENT.md](DEVELOPMENT.md)" in text
    assert "[CHANGELOG.md](CHANGELOG.md)" in text
    assert "[model/](model/)" in text
    assert "### Research purpose" in text
    assert "### Conceptual model" in text
    assert "### Research questions CBD can explore" in text
    assert "### Scientific foundations" in text
    assert "### Current capabilities and scientific limits" in text
    assert "**1. The agent carries state forward.**" not in text
    assert "### How CBD works" not in text


def test_public_readme_local_links_resolve() -> None:
    text = read(README)
    targets = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    targets.update(re.findall(r'(?:href|src|srcset)="([^"]+)"', text))
    unresolved = []
    for target in targets:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0]
        if clean and not (ROOT / clean).exists():
            unresolved.append(target)
    assert unresolved == []


def test_public_readme_stays_within_quality_budget() -> None:
    text = read(README)
    contract = json.loads(read(CONTRACT))
    budget = contract["public_readme_quality_budget"]
    plain = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\b[\w][\w./+-]*\b", plain)
    headings = [
        line for line in text.splitlines()
        if re.match(r"^#{1,6}\s", line) or re.search(r"<h[1-6]", line)
    ]
    assert len(words) <= budget["maximum_words"]
    assert len(headings) <= budget["maximum_primary_headings"]
    assert len(re.findall(r"<img alt=", text.split("---", 1)[0])) <= budget["maximum_primary_header_badges"]
    table_separators = re.findall(r"(?m)^\|\s*:?-{3,}[^\n]*\|\s*$", text)
    assert len(table_separators) <= budget["maximum_tables"]


def test_public_readme_uses_mobile_readable_structured_lists() -> None:
    text = read(README)
    assert "| Concept | What it represents in CBD |" not in text
    assert "| Area | Current model | Possible mature direction, if supported |" not in text
    assert "| Research question | What CBD provides |" not in text
    assert "| If you want to… | Start here |" not in text
    assert "**Information history:**" in text
    assert "**Probabilistic action:**" in text
    assert "**Information sequence:** Current released baseline —" in text
    assert "**Empirical status:** Current —" in text


def test_public_readme_reproducibility_routes_are_current() -> None:
    text = read(README)
    assert "### Using and reproducing CBD" in text
    assert "requirements/ci-py312-linux.lock.txt" in text
    assert "python -m build --no-isolation" in text
    assert "cemodel validate --root ." in text
    assert ".github/workflows/cbd-validation.yml" in text
    assert "DEVELOPMENT.md" in text


def test_public_markdown_has_no_literal_newline_escapes() -> None:
    for path in (
        README,
        ROOT / "STATUS.md",
        ROOT / "DEVELOPMENT.md",
        ROOT / "CHANGELOG.md",
        ROOT / "model" / "benchmarks" / "README.md",
        ROOT / "releases" / "v0.1.1.md",
    ):
        assert r"\n" not in read(path)
