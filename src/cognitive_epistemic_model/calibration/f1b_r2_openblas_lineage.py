from __future__ import annotations

import os
import re
from typing import Mapping


EXPECTED_OPENBLAS_CORE = "Haswell"
OPENBLAS_CORE_ENV = "OPENBLAS_CORETYPE"
MAX_RETAINED_DRAW_INDEX = 198

_CORE_RE = re.compile(r"(?:^|\n)Core:\s*([^\r\n]+)", re.MULTILINE)


def parse_openblas_verbose_cores(output: str) -> tuple[str, ...]:
    cores = tuple(match.strip() for match in _CORE_RE.findall(str(output)))
    if not cores:
        raise ValueError("OpenBLAS runtime probe did not report a core")
    return cores


def validate_candidate_environment(
    environment: Mapping[str, str | None] | None = None,
    *,
    expected_core: str = EXPECTED_OPENBLAS_CORE,
) -> None:
    env = os.environ if environment is None else environment
    actual = env.get(OPENBLAS_CORE_ENV)
    if actual != expected_core:
        raise ValueError(
            "candidate execution lineage requires "
            f"{OPENBLAS_CORE_ENV}={expected_core}; got {actual!r}"
        )


def validate_runtime_cores(
    cores: tuple[str, ...],
    *,
    expected_core: str = EXPECTED_OPENBLAS_CORE,
) -> None:
    if not cores:
        raise ValueError("OpenBLAS runtime core list must not be empty")
    unexpected = tuple(core for core in cores if core != expected_core)
    if unexpected:
        raise ValueError(
            "OpenBLAS runtime selected a non-qualified core: "
            + ", ".join(unexpected)
        )


def validate_retained_draw_indices(draw_indices) -> tuple[int, ...]:
    values = tuple(int(value) for value in draw_indices)
    if not values:
        raise ValueError("qualification draw set must not be empty")
    if tuple(sorted(set(values))) != values:
        raise ValueError(
            "qualification draw indices must be unique and increasing"
        )
    if values[0] < 0 or values[-1] > MAX_RETAINED_DRAW_INDEX:
        raise ValueError(
            "qualification may replay retained draw indices 0..198 only"
        )
    return values


def validate_qualification_config(config: dict) -> None:
    if config["status"] != (
        "NON_AUTHORITATIVE_OPENBLAS_EXECUTION_LINEAGE_QUALIFICATION"
    ):
        raise ValueError("unsupported execution-lineage qualification status")
    candidate = config["candidate_environment"]
    if candidate["variable"] != OPENBLAS_CORE_ENV:
        raise ValueError("candidate OpenBLAS environment variable changed")
    if candidate["value"] != EXPECTED_OPENBLAS_CORE:
        raise ValueError("candidate OpenBLAS core changed")
    if int(config["q2_full_replay"]["required_stream_count"]) != 224:
        raise ValueError("Q2 required stream count changed")
    if int(config["q2_full_replay"]["maximum_draw_index"]) != 198:
        raise ValueError("Q2 maximum draw index changed")
    if float(
        config["q2_full_replay"]["observed_statistic_absolute_tolerance"]
    ) != 1e-10:
        raise ValueError("Q2 observed-statistic tolerance changed")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("execution-lineage interpretation boundary weakened")
