from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.corpus.baselines import load_catalog, validate_catalog

REPO = Path(__file__).resolve().parents[2]


def test_catalog_is_well_formed() -> None:
    entries = load_catalog()
    assert len(entries) == 15
    assert validate_catalog(entries) == []
    first, second = entries[0], entries[1]
    broken = [
        first,
        dict(first),  # same id again
        {key: value for key, value in second.items() if key != "summary"},
        dict(second, id="too-few", mechanisms=["one", "two"]),
        dict(second, id="bad-ref", references=[{"doi": "10.1/x"}, {"arxiv": "not-an-id"}]),
    ]
    problems = validate_catalog(broken)
    assert any("duplicate id" in p for p in problems)
    assert any(p.startswith(f"{second['id']}: missing field") and "summary" in p for p in problems)
    assert any(p.startswith("too-few: mechanisms") for p in problems)
    assert sum(p.startswith("bad-ref: malformed reference") for p in problems) == 2


def test_catalog_note_references_exist() -> None:
    if not (REPO / "research" / "registry").is_dir():
        pytest.skip("no research registry in this checkout")
    stems = [ref["note"] for entry in load_catalog() for ref in entry["references"] if "note" in ref]
    assert stems
    assert [stem for stem in stems if not (REPO / "research" / f"{stem}.md").is_file()] == []


def test_runnable_commands_point_at_existing_files() -> None:
    if not (REPO / "tools" / "dqi_screen").is_dir():
        pytest.skip("Project 1 not merged")
    runnable = [entry["runnable"] for entry in load_catalog() if entry["runnable"]]
    assert runnable
    for item in runnable:
        scripts = [token for token in item["command"].split() if token.endswith(".py")]
        assert scripts and all((REPO / script).is_file() for script in scripts)
        if item.get("entry"):
            path, _, name = item["entry"].partition(":")
            assert re.search(rf"^def {re.escape(name)}\(", (REPO / path).read_text(encoding="utf-8"), re.M)
