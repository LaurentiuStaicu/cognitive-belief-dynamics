from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONTRACT = ROOT / ".github" / "readme_design_contract.json"
LIGHT = ROOT / "assets" / "readme" / "cbd-concept-overview-light.svg"
DARK = ROOT / "assets" / "readme" / "cbd-concept-overview-dark.svg"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_public_readme_header_is_suite_consistent() -> None:
    text = read(README)
    header = text.split("---", 1)[0]
    assert 'width="112"' in header
    assert len(re.findall(r"<img alt=", header)) == 3
    assert "CBD validation" in header
    assert "MIT / CC BY 4.0" in header


def test_public_readme_preserves_current_paradigm_boundary() -> None:
    text = re.sub(r"[*_`]", "", read(README)).lower()
    required = (
        "not currently a formal system dynamics model",
        "event schedule is externally supplied",
        "share action does not automatically create future exposure",
        "progressive endogenization",
        "not an already implemented capability",
    )
    for token in required:
        assert token in text


def test_public_readme_reports_full_m1_e4_boundary() -> None:
    text = read(README)
    lower = text.lower()
    result = json.loads(
        read(
            ROOT
            / "model"
            / "benchmarks"
            / "results"
            / "m1_e4_protocol_robustness_authoritative_2026-09-17.json"
        )
    )
    assert "18 / 18 primary p64_x10 cells meet the 0.80 recovery gate" in lower
    assert "0.92" in text
    assert "PROTOCOL_ROBUSTNESS_FAIL" in text
    assert "3 / 18 cells below 0.80" in lower
    assert "minimum recovery 0.56" in lower
    for cell_id in result["formal_failed_cells"]:
        assert cell_id in text
    assert "human-participant validation | **not established**" in lower
    assert "pencode | **not identified or estimated**" in lower


def test_public_readme_distinguishes_conceptual_and_executable_scope() -> None:
    text = read(README)
    assert "20 modules" in text
    assert "12 implemented M0" in text
    assert "10 candidate" in text
    assert "Platform / Network, AI System, and Learning / Adaptation remain **future**" in text


def test_public_assets_exist_and_are_theme_aware() -> None:
    assert LIGHT.is_file()
    assert DARK.is_file()
    text = read(README)
    assert "assets/readme/cbd-concept-overview-light.svg" in text
    assert "assets/readme/cbd-concept-overview-dark.svg" in text
    assert "prefers-color-scheme: dark" in text
    assert "prefers-color-scheme: light" in text


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


def test_public_readme_reproducibility_routes_are_current() -> None:
    text = read(README)
    assert "requirements/ci-py312-linux.lock.txt" in text
    assert "python -m build --no-isolation" in text
    assert "cemodel validate --root ." in text
    assert "DEVELOPMENT.md" in text
    assert "releases/v0.1.1.manifest.json" in text


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
