from __future__ import annotations

import re
from pathlib import Path

import cognitive_epistemic_model as cbd


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PREVIEW = ROOT / ".github" / "CBD_README_PREVIEW.md"
CONTRACT = ROOT / ".github" / "readme_design_contract.json"
LIGHT = ROOT / "assets" / "readme" / "cbd-concept-overview-light.svg"
DARK = ROOT / "assets" / "readme" / "cbd-concept-overview-dark.svg"
PREVIEW_LIGHT = ROOT / ".github" / "readme-assets" / "cbd-concept-overview-light.svg"
PREVIEW_DARK = ROOT / ".github" / "readme-assets" / "cbd-concept-overview-dark.svg"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_public_readme_header_is_suite_consistent() -> None:
    text = read(README)
    header = text.split("---", 1)[0]
    assert 'width="112"' in header
    assert len(re.findall(r"<img alt=", header)) == 3
    assert "Scientific reproducibility" not in header
    assert "CBD validation" in header
    assert "MIT / CC BY 4.0" in header


def test_public_version_is_consistent() -> None:
    text = read(README)
    citation = read(ROOT / "CITATION.cff")
    assert cbd.__version__ == "0.1.0"
    assert "Version: 0.1.0" in text
    assert re.search(r"(?m)^version:\s*0\.1\.0\s*$", citation)


def test_public_readme_preserves_cbd_paradigm_boundary() -> None:
    text = read(README)
    normalized = re.sub(r"[*_`]", "", text).lower()
    required = (
        "not currently a formal system dynamics model",
        "event schedules remain externally supplied",
        "share action does not automatically create future exposure",
        "synthetic recovery is not human validation",
        "not a population-calibrated cognitive law",
        "not a literal neural implementation of bayes",
    )
    for token in required:
        assert token in normalized


def test_public_readme_matches_retained_m1_e4_boundary() -> None:
    text = read(README)
    status = read(ROOT / "STATUS.md")
    benchmarks = read(ROOT / "model" / "benchmarks" / "README.md")

    normalized = text.lower()
    assert "18 / 18 primary p64_x10 cells meet the 0.80 recovery gate" in normalized
    assert "0.92" in text
    assert "human-participant validation | **not established**" in normalized
    assert "pencode | **not identified or estimated**" in normalized
    assert "participant recruitment | **not authorized by current baseline**" in normalized

    assert "all 18 primary p64_x10 cells meet the declared 0.80 recovery gate" in status.lower()
    assert "minimum observed recovery of 0.92" in status.lower()
    assert "all 18 primary p64_x10 cells meet the declared 0.80 recovery gate" in benchmarks.lower()


def test_public_assets_match_reviewed_preview_assets() -> None:
    assert LIGHT.is_file()
    assert DARK.is_file()
    assert LIGHT.read_bytes() == PREVIEW_LIGHT.read_bytes()
    assert DARK.read_bytes() == PREVIEW_DARK.read_bytes()

    text = read(README)
    assert "assets/readme/cbd-concept-overview-light.svg" in text
    assert "assets/readme/cbd-concept-overview-dark.svg" in text
    assert "prefers-color-scheme: dark" in text
    assert "prefers-color-scheme: light" in text


def test_public_readme_local_links_resolve() -> None:
    text = read(README)
    targets = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    targets.update(re.findall(r'(?:href|src|srcset)="([^"]+)"', text))

    unresolved: list[str] = []
    for target in targets:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue
        candidate = ROOT / clean
        if not candidate.exists():
            unresolved.append(target)

    assert unresolved == []


def test_public_readme_stays_within_quality_budget() -> None:
    import json

    text = read(README)
    contract = json.loads(read(CONTRACT))
    budget = contract["public_readme_quality_budget"]

    plain = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\b[\w][\w./+-]*\b", plain)
    headings = [
        line
        for line in text.splitlines()
        if re.match(r"^#{1,6}\s", line) or re.search(r"<h[1-6]", line)
    ]

    assert len(words) <= budget["maximum_words"]
    assert len(headings) <= budget["maximum_primary_headings"]


def test_public_readme_support_and_licensing_routes_are_explicit() -> None:
    text = read(README)
    assert ".github/CONTRIBUTING.md" in text
    assert ".github/SUPPORT.md" in text
    assert "LICENSING.md" in text
    assert "Source code and schemas are MIT licensed" in text
    assert "CC BY 4.0 where applicable" in text


def test_preview_is_retained_but_public_readme_is_root_adapted() -> None:
    public = read(README)
    preview = read(PREVIEW)
    assert public != preview
    assert 'src="assets/icon.png"' in public
    assert 'src="../assets/icon.png"' in preview
