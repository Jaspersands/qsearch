from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path

import pytest

from tests.tools.conftest import NEGATIVES
from tests.tools.test_corpus_mcp import _call
from tools.corpus.api import Corpus
from tools.corpus import baselines as baselines_module
from tools.corpus.baselines import CatalogError, _name_pattern, load_catalog, recommend, tokens, validate_catalog
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


@pytest.mark.parametrize(
    ("change", "problem"),
    [
        ({"mechanisms": ["a", "b", "c", "d", "e", "f", "g"]}, "mechanisms must be 3 to 6 keywords, found 7"),
        ({"mechanisms": "gibbs sampling"}, "mechanisms must be a list"),
        ({"references": {"arxiv": "2610.06753"}}, "references must be a list"),
        ({"aliases": "Prange"}, "aliases must be a list"),
        ({"aliases": ["Prange", " "]}, "aliases must be non-empty strings"),
        ({"name": "  "}, "name must be a non-empty string"),
        ({"summary": 3}, "summary must be a non-empty string"),
        (
            {"runnable": "python tools/dqi_screen/screen.py"},
            "runnable must be null or {command?, entry?} with at least one, entry path.py:name",
        ),
        ({"runnable": {}}, "runnable must be null or {command?, entry?} with at least one, entry path.py:name"),
        (
            {"runnable": {"entry": "prange_restarts"}},
            "runnable must be null or {command?, entry?} with at least one, entry path.py:name",
        ),
        (
            {"runnable": {"command": "python x.py", "script": "x.py"}},
            "runnable must be null or {command?, entry?} with at least one, entry path.py:name",
        ),
        # a keyword with no word the matcher keeps would match every idea
        ({"mechanisms": ["gibbs sampling", "parity check", "-"]}, 'mechanism "-" has no letter or digit, so it would match every idea'),
        ({"mechanisms": ["gibbs sampling", "parity check", "格"]}, 'mechanism "格" has letters the matcher ignores (格); spell it in ASCII'),
        ({"mechanisms": ["gibbs sampling", "χ² test", "code"]}, 'mechanism "χ² test" has letters the matcher ignores (χ); spell it in ASCII'),
        ({"mechanisms": ["gibbs sampling", "parity check", 3]}, "mechanism 3 must be a string"),
        ({"mechanisms": ["Gibbs sampling", "parity check", "code"]}, 'mechanism "Gibbs sampling" must be lowercase'),
    ],
)
def test_validate_catalog_names_each_broken_rule(change: dict, problem: str) -> None:
    entry = dict(load_catalog()[1], id="broken", **change)
    assert validate_catalog([entry]) == [f"broken: {problem}"]


def test_accented_and_numbered_keywords_are_valid() -> None:
    entry = dict(load_catalog()[1], id="fine", mechanisms=["gröbner basis", "max k cut", "3-sat"])
    assert validate_catalog([entry]) == []


def test_recommend_refuses_an_invalid_catalog(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    every_idea = dict(load_catalog()[1], id="every-idea", mechanisms=["格", "-", "χ²"])
    with pytest.raises(CatalogError, match="every-idea: mechanism"):
        recommend(corpus, "Shor factoring of RSA moduli", catalog=[every_idea])  # scored 0.6667 on any idea
    with pytest.raises(CatalogError, match="found 0"):  # was ZeroDivisionError
        recommend(corpus, IDEA, catalog=[dict(load_catalog()[1], id="none", mechanisms=[])])


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (None, "cannot read the baseline catalog"),
        ('{"baselines": [', "is not valid JSON"),
        ('{"entries": []}', 'must be an object with a "baselines" list'),
        ("[]", 'must be an object with a "baselines" list'),
        ('{"baselines": [{"id": "lonely"}]}', "invalid baseline catalog"),
    ],
)
def test_a_broken_catalog_file_is_a_clean_error(
    fake_repo: Path, tmp_path: Path, monkeypatch, capsys, content: str | None, message: str
) -> None:
    catalog = tmp_path / "catalog" / "baselines.json"
    if content is not None:
        catalog.parent.mkdir()
        catalog.write_text(content, encoding="utf-8")
    monkeypatch.setattr(baselines_module, "CATALOG", catalog)
    assert main(["--root", str(fake_repo), "baselines", IDEA]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("error: ") and message in captured.err and str(catalog) in captured.err
    server = create_server(fake_repo, dense="off")
    payload = _call(server, "classical_baselines", {"idea": IDEA})
    assert set(payload) == {"error"} and message in payload["error"]


def test_a_citation_matches_the_name_in_any_case(fake_repo: Path) -> None:
    shout = "# PRANGE SHOUT\n\nPRANGE decoding already solves syndrome decoding of this random linear code.\n"
    corpus = _corpus_with_note(fake_repo, "PRANGE_SHOUT", shout)
    recs = recommend(corpus, IDEA)
    assert recs[0].baseline["id"] == "prange-isd"
    assert recs[0].evidence[0].doc_id.startswith("note:PRANGE_SHOUT")
    assert recs[0].score == pytest.approx(2 / 5 + 1 / 10)


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


USD_NOTE = (
    "# Kangaroo Sampler\n\n"
    "The product-USD/Prange sampler and the block-Prange decoder sample the kangaroo Gibbs law.\n"
)


def test_a_longer_name_of_another_baseline_is_not_a_citation_of_its_part(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "KANGAROO_SAMPLER", USD_NOTE)
    recs = {rec.baseline["id"]: rec for rec in recommend(corpus, "kangaroo Gibbs sampler", k=20)}
    assert recs["usd-prange-rejection-sampler"].evidence[0].doc_id.startswith("note:KANGAROO_SAMPLER")
    assert "prange-isd" not in recs  # "Prange" only occurs inside USD-Prange names
    both = _corpus_with_note(fake_repo, "KANGAROO_SAMPLER", USD_NOTE + "\nPlain Prange decoding fails on kangaroo.\n")
    recs = {rec.baseline["id"]: rec for rec in recommend(both, "kangaroo Gibbs sampler", k=20)}
    assert recs["prange-isd"].evidence[0].doc_id.startswith("note:KANGAROO_SAMPLER")
    assert recs["usd-prange-rejection-sampler"].evidence[0].doc_id.startswith("note:KANGAROO_SAMPLER")


def test_spin_glasses_match_the_spin_glass_keyword(fake_repo: Path) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    recs = recommend(corpus, "sampling Gibbs states of mean-field spin glasses")
    assert recs[0].baseline["id"] == "stochastic-localization-pspin"
    assert recs[0].matched == ["gibbs sampling", "spin glass"]


def test_a_negative_k_returns_nothing(fake_repo: Path, capsys) -> None:
    corpus = _corpus_with_note(fake_repo, "PRANGE_SYNDROME", PRANGE_NOTE)
    assert len(recommend(corpus, IDEA)) >= 2
    assert recommend(corpus, IDEA, k=0) == recommend(corpus, IDEA, k=-1) == []
    for k in ("-1", "0"):  # -k 0 would print that no baseline matches, which is false
        with pytest.raises(SystemExit):
            main(["--root", str(fake_repo), "baselines", IDEA, "-k", k])
        assert "-k must be at least 1" in capsys.readouterr().err
    server = create_server(fake_repo, dense="off")
    assert _call(server, "classical_baselines", {"idea": IDEA, "k": -1})["recommendations"] == []


def test_catalog_note_references_exist() -> None:
    if not (REPO / "research" / "registry").is_dir():
        pytest.skip("no research registry in this checkout")
    stems = [ref["note"] for entry in load_catalog() for ref in entry["references"] if "note" in ref]
    assert stems
    assert [stem for stem in stems if not (REPO / "research" / f"{stem}.md").is_file()] == []


def test_catalog_note_references_name_their_baseline() -> None:
    if not (REPO / "research" / "registry").is_dir():
        pytest.skip("no research registry in this checkout")
    silent = [
        f"{entry['id']}: {ref['note']}"
        for entry in load_catalog()
        for ref in entry["references"]
        if "note" in ref
        and not _name_pattern(entry).search((REPO / "research" / f"{ref['note']}.md").read_text(encoding="utf-8"))
    ]
    assert silent == []


def test_runnables_run_as_printed_or_name_an_existing_function() -> None:
    if not (REPO / "tools" / "dqi_screen").is_dir():
        pytest.skip("Project 1 not merged")
    runnable = [entry["runnable"] for entry in load_catalog() if entry["runnable"]]
    assert runnable
    for item in runnable:
        if item.get("entry"):
            path, _, name = item["entry"].partition(":")
            assert re.search(rf"^def {re.escape(name)}\(", (REPO / path).read_text(encoding="utf-8"), re.M)
        if item.get("command"):  # the CLI prints it as "run:", so it must run from the repository root
            done = subprocess.run(shlex.split(item["command"]), cwd=REPO, capture_output=True, text=True, timeout=120)
            assert done.returncode == 0, (item["command"], done.stderr[-500:])


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
    out = capsys.readouterr().out
    assert "call: tools/dqi_screen/prange.py:prange_restarts (a library function; it needs an instance)" in out
    assert "run:" not in out and "screener computes both" not in out
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
