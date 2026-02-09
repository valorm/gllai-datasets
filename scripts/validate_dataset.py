#!/usr/bin/env python3
"""Validate dataset JSONL files against schemas and basic rules."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with 'python -m pip install jsonschema'."
    ) from exc


LANG_DIRS = ("ewe", "ga", "twi")


def load_schema(schema_path: Path) -> Draft202012Validator:
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    return Draft202012Validator(data)


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line_num, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            try:
                yield line_num, json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_num} invalid JSON: {exc}") from exc


def validate_knowledge_chunks(path: Path, validator: Draft202012Validator, language: str) -> list[str]:
    errors: list[str] = []
    for line_num, record in iter_jsonl(path):
        for err in validator.iter_errors(record):
            errors.append(f"{path}:{line_num} schema error: {err.message}")
        record_language = record.get("language")
        if record_language != language:
            errors.append(
                f"{path}:{line_num} language mismatch: {record_language} != {language}"
            )
        confidence = record.get("confidence")
        if isinstance(confidence, (int, float)):
            if not (0 <= confidence <= 1):
                errors.append(
                    f"{path}:{line_num} confidence out of range: {confidence}"
                )
        else:
            errors.append(f"{path}:{line_num} confidence must be a number")
    return errors


def validate_training_pairs(path: Path, validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    for line_num, record in iter_jsonl(path):
        for err in validator.iter_errors(record):
            errors.append(f"{path}:{line_num} schema error: {err.message}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GLLAI datasets")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: repo root)",
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas",
        help="Directory containing JSON schemas",
    )
    args = parser.parse_args()

    knowledge_schema = load_schema(args.schema_dir / "knowledge_chunks.schema.json")
    training_schema = load_schema(args.schema_dir / "training_pairs.schema.json")

    errors: list[str] = []
    for lang in LANG_DIRS:
        lang_dir = args.root / lang
        if not lang_dir.exists():
            continue
        for version_dir in sorted(p for p in lang_dir.iterdir() if p.is_dir()):
            knowledge_path = version_dir / "knowledge_chunks.jsonl"
            training_path = version_dir / "training_pairs.jsonl"
            if knowledge_path.exists():
                errors.extend(
                    validate_knowledge_chunks(knowledge_path, knowledge_schema, lang)
                )
            if training_path.exists():
                errors.extend(validate_training_pairs(training_path, training_schema))

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
