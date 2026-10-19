from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.claim_checker import check as cc

PAPERS = json.loads((Path(__file__).parent / "fixtures" / "claim_checker_papers.json").read_text())

# Consensus caveats, fixed before the rules were written. "required" flags must fire;
# "forbidden" flags must not. Flags not listed are not scored.
EXPECTED = {
    "quant-ph/9508027": (set(), {"oracle_model", "input_loading", "readout", "heuristic_assumption", "numerical_only"}),
    "2308.06572": ({"heuristic_assumption"}, {"oracle_model", "input_loading", "readout"}),
    "2408.08292": ({"restricted_baseline"}, {"oracle_model", "input_loading"}),
    "0811.3171": ({"input_loading", "readout", "parameter_dependence"}, {"oracle_model", "heuristic_assumption"}),
    "1603.08675": ({"input_loading", "readout", "restricted_baseline"}, {"oracle_model", "heuristic_assumption"}),
    "quant-ph/0209131": ({"oracle_model"}, {"input_loading", "readout", "heuristic_assumption", "numerical_only"}),
    # Held out until the rules were frozen (3 of 4 passed; the shallow-circuit miss was "non-oracular").
    "1307.0401": ({"input_loading"}, {"oracle_model", "heuristic_assumption"}),
    "quant-ph/9605043": ({"input_loading"}, {"heuristic_assumption", "numerical_only"}),
    "1704.00690": (set(), {"oracle_model", "heuristic_assumption", "input_loading", "numerical_only"}),
    "2204.02063": ({"oracle_model"}, {"input_loading", "numerical_only"}),
}


@pytest.mark.parametrize("arxiv_id", sorted(EXPECTED))
def test_consensus_papers_get_expected_flags(arxiv_id: str) -> None:
    paper = PAPERS[arxiv_id]
    report = cc.check_text(paper["abstract"], title=paper["title"])
    flags = {flag.name for flag in report.flags if not flag.negated}
    required, forbidden = EXPECTED[arxiv_id]
    assert required <= flags, f"missing {required - flags}"
    assert not (forbidden & flags), f"wrongly flagged {forbidden & flags}"


@pytest.mark.parametrize("arxiv_id", sorted(EXPECTED))
def test_every_flag_quotes_the_text(arxiv_id: str) -> None:
    paper = PAPERS[arxiv_id]
    text = f"{paper['title']}. {paper['abstract']}"
    sentences = cc.split_sentences(text)
    for flag in cc.check_text(paper["abstract"], title=paper["title"]).flags:
        assert flag.quote in sentences, "a quote must be one whole sentence of the input"


@pytest.mark.parametrize(
    ("sentence", "flag"),
    [
        ("We assume quantum random access memory (QRAM) to load the data.", "input_loading"),
        ("Given multiple copies of the unknown state, we estimate its spectrum.", "input_loading"),
        ("The algorithm outputs a quantum state proportional to the solution.", "readout"),
        ("Our evidence comes from numerical simulations up to 30 qubits.", "numerical_only"),
        ("Relative to a random oracle, the separation is exponential.", "oracle_model"),
        ("Assuming a plausible conjecture about lattice problems, the speedup holds.", "heuristic_assumption"),
        ("The runtime scales with the condition number and the spectral gap.", "parameter_dependence"),
        ("Our method beats simulated annealing on these instances.", "restricted_baseline"),
    ],
)
def test_rule_flags_on_single_sentences(sentence: str, flag: str) -> None:
    flags = {f.name: f for f in cc.check_text(sentence).flags}
    assert flag in flags and not flags[flag].negated


@pytest.mark.parametrize(
    ("sentence", "flag"),
    [
        ("Our algorithm does not require QRAM or any quantum data structure: the input is a classical list.", "input_loading"),
        ("This is not an oracle separation.", "oracle_model"),
        ("We give an oracle-free exponential separation.", "oracle_model"),
        ("The problem is non oracular.", "oracle_model"),
        ("No black-box access is assumed.", "oracle_model"),
        ("We prove the speedup unconditionally, without relying on any conjecture or heuristic assumption.", "heuristic_assumption"),
        ("Our result is rigorous; we do not rely on numerical simulations or empirical evidence.", "numerical_only"),
        ("The runtime is independent of the condition number.", "parameter_dependence"),
        ("Unlike algorithms that only output a quantum state, ours outputs the full classical solution.", "readout"),
        ("We compare against tailored classical algorithms, not just generic heuristics.", "restricted_baseline"),
        # The negation carries along a list.
        ("The runtime is independent of the condition number, sparsity and precision.", "parameter_dependence"),
        ("Unlike algorithms that only output a quantum state or estimate expectation values, ours outputs the solution.", "readout"),
    ],
)
def test_a_caveat_the_sentence_rules_out_is_marked_negated(sentence: str, flag: str) -> None:
    flags = {f.name: f for f in cc.check_text(sentence).flags}
    assert flag in flags and flags[flag].negated


def test_negation_does_not_carry_into_a_new_clause() -> None:
    flag = next(f for f in cc.check_text("We do not use QRAM, and we assume block encodings of the matrix.").flags if f.name == "input_loading")
    assert not flag.negated and flag.match.lower().startswith("block")


def test_a_plain_mention_wins_over_an_earlier_negated_one() -> None:
    text = "We do not use QRAM in the first stage. The second stage loads the data with QRAM."
    flag = next(f for f in cc.check_text(text).flags if f.name == "input_loading")
    assert not flag.negated and flag.quote.startswith("The second stage")


def test_render_separates_ruled_out_caveats() -> None:
    report = cc.check_text("This is not an oracle separation. We assume QRAM to load the data.")
    text = cc.render(report)
    flags_part, _, ruled_out = text.partition("## Apparently ruled out")
    assert "input_loading" in flags_part and "oracle_model" in ruled_out


def test_claim_strength_is_extracted() -> None:
    report = cc.check_text("We give a quantum algorithm with an exponential speedup over classical algorithms.")
    assert report.claim == "exponential"
    assert cc.check_text("A quadratic speedup over classical search.").claim == "polynomial"
    assert cc.check_text("We study the structure of codes.").claim == "none-stated"


def test_split_sentences_keeps_abbreviations_together() -> None:
    sentences = cc.split_sentences("We use e.g. the QFT. Then we decode, i.e. we solve it. Done.")
    assert len(sentences) == 3


def test_render_report_contains_flags_questions_and_neighbours() -> None:
    paper = PAPERS["0811.3171"]
    report = cc.check_text(paper["abstract"], title=paper["title"])
    report.neighbours = [{"doc_id": "negative:NEG-X", "title": "X", "lesson": "Charge state preparation."}]
    text = cc.render(report, source="arXiv:0811.3171")
    assert "## Flags" in text and "## Questions to ask" in text and "## Nearest Q-Search records" in text
    assert "Charge state preparation." in text
    assert "abstract only" in text.lower()


def test_cli_checks_a_text_file(tmp_path: Path, capsys) -> None:
    path = tmp_path / "abstract.txt"
    path.write_text(PAPERS["quant-ph/0209131"]["abstract"])
    assert cc.main(["--file", str(path), "--no-corpus"]) == 0
    out = capsys.readouterr().out
    assert "oracle_model" in out


def test_cli_fetches_by_arxiv_id_with_injected_client(capsys) -> None:
    from tools.corpus.sources.arxiv import Paper

    class FakeClient:
        def get(self, ids):
            p = PAPERS["2308.06572"]
            return [Paper(**p)]

    assert cc.main(["2308.06572", "--no-corpus"], client=FakeClient()) == 0
    assert "heuristic_assumption" in capsys.readouterr().out
