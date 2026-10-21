from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tests.tools.test_corpus_mcp import _call
from tools.corpus.api import Corpus
from tools.corpus.baselines import load_catalog, recommend, validate_catalog
from tools.corpus.cli import main
from tools.corpus.mcp_server import create_server

REPO = Path(__file__).resolve().parents[2]
IDEA = "syndrome decoding of a random linear code"
PRANGE_NOTE = (
    "# Prange Syndrome\n\n"
    "Prange information-set decoding already solves syndrome decoding of this random linear code.\n"
)
KANGAROO_NOTE = (
    "# Kangaroo Hop\n\n"
    "The kangaroo hop question was settled classically by belief propagation on its factor graph.\n"
)


def _corpus_with_note(root: Path, stem: str, text: str) -> Corpus:
    (root / "research" / f"{stem}.md").write_text(text, encoding="utf-8")
    corpus = Corpus(root)
    corpus.refresh()
    return corpus


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


def test_prange_ranks_first_when_a_note_mentions_it(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    recs = recommend(corpus, IDEA)
    assert recs[0].baseline["id"] == "prange-isd"
    assert "syndrome decoding" in recs[0].matched
    assert recs[0].evidence[0].doc_id.startswith("note:PRANGE_SYNDROME")
    # "syndrome decoding" and "linear code" of five keywords, plus one citing hit of ten
    assert recs[0].matched == ["syndrome decoding", "linear code"]
    assert recs[0].score == pytest.approx(2 / 5 + 1 / 10)
    assert [rec.score for rec in recs] == sorted((rec.score for rec in recs), reverse=True)
    assert all(rec.score > 0 for rec in recs)
    assert len(recommend(corpus, IDEA, k=1)) == 1


def test_recommend_scores_corpus_mentions_without_keyword_overlap(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "KANGAROO_HOP", KANGAROO_NOTE)
    recs = recommend(corpus, "kangaroo hop")
    assert [rec.baseline["id"] for rec in recs] == ["belief-propagation-ldpc"]
    assert recs[0].matched == []
    assert recs[0].score == pytest.approx(0.1)
    assert recs[0].evidence[0].doc_id.startswith("note:KANGAROO_HOP")
    # names match on word boundaries: "Kanga" does not cite a note that says "kangaroo"
    kanga = dict(load_catalog()[0], id="kanga", name="Kanga", aliases=[])
    assert recommend(corpus, "kangaroo hop", catalog=[kanga]) == []


def test_cli_baselines_text_and_json(fake_repo: Path, capsys) -> None:
    _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    root = ["--root", str(fake_repo)]
    assert main([*root, "baselines", IDEA]) == 0
    out = capsys.readouterr().out
    assert "1. Prange information-set decoding" in out
    assert "why: matched syndrome decoding, linear code; cited by research/PRANGE_SYNDROME.md" in out
    assert "references: research/PARITY_BLOCK_USD_PRANGE.md" in out
    assert main([*root, "baselines", "optimal polynomial intersection over a prime field"]) == 0
    assert "run: python tools/dqi_screen/screen.py" in capsys.readouterr().out
    assert main([*root, "baselines", "zebrafish migration"]) == 0
    assert "No catalog baseline" in capsys.readouterr().out
    assert main([*root, "baselines", IDEA, "--json", "-k", "1"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"idea", "recommendations", "index_incomplete", "index_issues"}
    assert payload["idea"] == IDEA and len(payload["recommendations"]) == 1
    top = payload["recommendations"][0]
    assert set(top) == {"baseline", "score", "matched", "evidence"}
    assert top["baseline"]["id"] == "prange-isd" and top["score"] == pytest.approx(0.5)
    assert top["matched"] == ["syndrome decoding", "linear code"]
    assert top["evidence"][0]["doc_id"].startswith("note:PRANGE_SYNDROME")


def test_classical_baselines_tool(fake_repo: Path) -> None:
    _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "classical_baselines", {"idea": IDEA, "k": 2})
    assert payload["idea"] == IDEA and "index_incomplete" in payload
    assert [rec["baseline"]["id"] for rec in payload["recommendations"]] == ["prange-isd", "isd-pinning-fft"]
    assert payload["recommendations"][0]["evidence"][0]["doc_id"].startswith("note:PRANGE_SYNDROME")
    assert _call(server, "classical_baselines", {"idea": "zebrafish migration"})["recommendations"] == []
