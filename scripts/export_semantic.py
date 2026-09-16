"""Regenerate the deterministic OA-1 Semantic Spine index."""
from pathlib import Path

from cognitive_epistemic_model.semantic import (
    build_semantic_index,
    semantic_index_json,
    validate_semantic_index,
)

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
SCHEMA = ROOT / "schemas" / "semantic_index.schema.json"
OUTPUT = MODEL / "semantic_index.json"


def main() -> None:
    index = build_semantic_index(MODEL)
    validate_semantic_index(index, SCHEMA)
    OUTPUT.write_text(semantic_index_json(index), encoding="utf-8")


if __name__ == "__main__":
    main()
