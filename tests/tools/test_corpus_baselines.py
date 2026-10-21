from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tests.tools.conftest import NEGATIVES
from tests.tools.test_corpus_mcp import _call
from tools.corpus.api import Corpus
from tools.corpus.baselines import load_catalog, recommend, tokens, validate_catalog
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
    assert validate_catalog([first, "oops", None]) == ["entry 2: must be an object", "entry 3: must be an object"]


def test_tokens_drop_a_plural_s_but_keep_a_double_s() -> None:
    assert tokens("spin glasses") == tokens("spin glass") == ["spin", "glass"]
    assert tokens("Gibbs codes processes") == ["gibb", "code", "process"]
    assert tokens("is gas bias") == ["is", "gas", "bia"]  # short words kept; a single final s still dropped


def test_tokens_fold_accents_and_spelling_variants() -> None:
    assert tokens("Gröbner") == tokens("Gröbner") == tokens("Grobner") == tokens("Groebner") == ["groebner"]
    assert tokens("MaxCut") == tokens("Max-Cut") == ["max", "cut"]
    assert tokens("graph colouring") == tokens("graph coloring") == ["graph", "coloring"]
    assert tokens("colourings") == ["coloring"]


QAOA_NOTE = (
    "# QAOA Barrier\n\n"
    "Goemans-Williamson rounding of the semidefinite relaxation bounds shallow QAOA on max-3-cut.\n"
)


@pytest.mark.parametrize("cut", ["max-3-cut", "Max-q-Cut", "max 3-cut", "max-k-cut"])
def test_a_concrete_max_k_cut_ranks_the_lp_decoder_first(fake_repo: Path, cut: str) -> None:
    corpus = _corpus_with_note(fake_repo, "QAOA_BARRIER", QAOA_NOTE)
    recs = recommend(corpus, f"DQI for {cut} on a ternary cycle code")
    assert recs[0].baseline["id"] == "lp-decoding-cycle-codes"
    assert recs[0].matched == ["cycle code", "max k cut"]
    sdp = next(rec for rec in recs if rec.baseline["id"] == "sdp-relaxation")
    assert sdp.score < recs[0].score


def test_max_k_cut_needs_its_number_between_max_and_cut(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    recs = {rec.baseline["id"]: rec for rec in recommend(corpus, "QAOA on max cut at depth 3", k=20)}
    assert "max k cut" not in recs.get("lp-decoding-cycle-codes", recs["sdp-relaxation"]).matched
    assert recs["sdp-relaxation"].matched == ["max cut", "qaoa"]
    assert recommend(corpus, "QAOA on MaxCut", k=20)[0].baseline["id"] == "sdp-relaxation"


def test_british_and_accented_spellings_match_their_keywords(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    colouring = {rec.baseline["id"]: rec for rec in recommend(corpus, "graph colouring codes", k=20)}
    assert colouring["lp-decoding-cycle-codes"].matched == ["graph coloring"]
    groebner = {rec.baseline["id"]: rec for rec in recommend(corpus, "Gröbner basis attack on ternary LWE", k=20)}
    assert groebner["groebner-mq"].matched == ["groebner basis"]


def test_spin_glasses_match_the_spin_glass_keyword(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    recs = recommend(corpus, "sampling Gibbs states of mean-field spin glasses")
    assert recs[0].baseline["id"] == "stochastic-localization-pspin"
    assert recs[0].matched == ["gibbs sampling", "spin glass"]


def test_a_negative_k_returns_nothing(fake_repo: Path, capsys) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    assert len(recommend(corpus, IDEA)) >= 2
    assert recommend(corpus, IDEA, k=0) == recommend(corpus, IDEA, k=-1) == []
    with pytest.raises(SystemExit):
        main(["--root", str(fake_repo), "baselines", IDEA, "-k", "-1"])
    assert "-k must be at least 0" in capsys.readouterr().err
    server = create_server(fake_repo, dense="off")
    assert _call(server, "classical_baselines", {"idea": IDEA, "k": -1})["recommendations"] == []


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


KANGAROO_SECTIONS = (
    "# Kangaroo Hop\n\n"
    "## Question\n\nThe kangaroo hop question was settled classically by belief propagation.\n\n"
    "## Method\n\nKangaroo hop messages follow belief propagation on its factor graph.\n\n"
    "## Verdict\n\nBelief propagation already decodes every kangaroo hop instance.\n"
)
KANGAROO_NEGATIVES = [
    {
        "id": f"NEG-KANGAROO-HOP-{n}",
        "claim": f"Kangaroo hop instance {n} needs a quantum decoder.",
        "reason_invalid": "Belief propagation decodes the kangaroo hop instance classically.",
        "lesson": "Run belief propagation first.",
    }
    for n in (1, 2)
]


def test_a_note_cites_a_baseline_once_however_many_sections_are_near(fake_repo: Path) -> None:
    registry = fake_repo / "research" / "registry" / "negative_results.json"
    registry.write_text(json.dumps(NEGATIVES + KANGAROO_NEGATIVES, indent=2), encoding="utf-8")
    corpus = _corpus_with_note(fake_repo, "KANGAROO_HOP", KANGAROO_SECTIONS)
    hits = corpus.search("kangaroo hop", kinds=("note", "negative"), k=10)
    assert sum(hit.path == "research/KANGAROO_HOP.md" for hit in hits) == 3  # three near sections of one note
    recs = recommend(corpus, "kangaroo hop")
    assert [rec.baseline["id"] for rec in recs] == ["belief-propagation-ldpc"]
    # one note and two registry records (one file, but each record is its own source)
    assert recs[0].score == pytest.approx(0.3)
    sources = sorted(hit.path if hit.kind == "note" else hit.doc_id for hit in recs[0].evidence)
    assert sources == ["negative:NEG-KANGAROO-HOP-1", "negative:NEG-KANGAROO-HOP-2", "research/KANGAROO_HOP.md"]


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
