from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "requirements/ci-py312-linux.lock.txt"
WORKFLOW = ROOT / ".github/workflows/cbd-validation.yml"
PYPROJECT = ROOT / "pyproject.toml"


def locked_versions() -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in LOCK.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        assert "==" in line
        assert " @ " not in line
        assert "git+" not in line
        name, version = line.split("==", 1)
        key = re.sub(r"[-_.]+", "-", name).lower()
        assert key not in result
        assert version
        result[key] = version
    return result


def test_ci_lock_contains_direct_build_test_and_runtime_dependencies() -> None:
    locked = locked_versions()
    required = {
        "pip",
        "build",
        "hatchling",
        "pytest",
        "hypothesis",
        "numpy",
        "scipy",
        "jsonschema",
    }
    assert required <= set(locked)

    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    for requirement in pyproject["project"]["dependencies"]:
        package = re.split(r"[<>=!~\[; ]", requirement, maxsplit=1)[0]
        key = re.sub(r"[-_.]+", "-", package).lower()
        assert key in locked


def test_ci_lock_is_platform_scoped_and_contains_only_exact_pins() -> None:
    text = LOCK.read_text(encoding="utf-8")
    assert "GitHub-hosted Ubuntu runner, CPython 3.12" in text
    assert "not presented as a universal lock" in text
    assert len(locked_versions()) >= 20


def test_validation_workflow_uses_lock_for_all_install_surfaces() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "requirements/ci-py312-linux.lock.txt" in workflow
    assert 'pip==26.2.1' in workflow
    assert "python -m build --no-isolation" in workflow
    assert '-c "$CBD_CI_CONSTRAINTS"' in workflow
    assert workflow.count("-c requirements/ci-py312-linux.lock.txt") >= 2
    assert workflow.count("requirements/ci-py312-linux.lock.txt") >= 3
    assert "pip freeze" not in workflow
