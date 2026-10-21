from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.tools.conftest import NEGATIVES
from tools.corpus.api import Corpus
from tools.corpus.cli import main
from tools.corpus.duplicates import check_claim, near_duplicates

HELSTROM = "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"
# The Helstrom record's claim with two words changed ("readout" -> "measurement", "dominates" -> "beats").
NEAR_CLAIM = "Local Helstrom measurement of each dihedral coset packet beats every product X-basis readout."

DUP_A = {
    "id": "NEG-DUP-A",
    "applies_to": ["HSP"],
    "claim": "A wombat sieve over abelian coset states recovers the hidden shift in polynomial time.",
    "reason_invalid": "The wombat sieve collapses to Kuperberg merging, whose cost is subexponential.",
    "lesson": "Charge the merging cost of every sieve.",
}
DUP_B = {
    "id": "NEG-DUP-B",
    "applies_to": ["HSP"],
    "claim": "A wombat sieve over abelian coset states recovers the hidden shift in quasi-polynomial time.",
    "reason_invalid": "The wombat sieve collapses to Kuperberg merging, whose cost is subexponential.",
    "lesson": "Charge the merging cost of every sieve.",
}

# Three parameter sweeps of ten records each: identical text, ids differing in a trailing number.
SWEEPS = {
    "NEG-GOPPA-SCALE-M6-T3-N48-0": "Goppa syndrome decoding at scale stays above the information set decoding baseline.",
    "NEG-POLAR-SHAPING-N32": "Polar successive cancellation shaping matches the quantum Gibbs sampler on every frozen set.",
    "NEG-LATTICE-BABAI-DIM": "Babai nearest plane rounding recovers the planted lattice vector below the radius bound.",
}
RESTATEMENT = [
    {
        "id": "NEG-ECHIDNA-READOUT-BOUND",
        "claim": "Echidna collective readout of platypus packets beats every adaptive product readout.",
        "reason_invalid": "A certified semidefinite bound caps echidna collective readout at the adaptive value.",
        "lesson": "Bound collective platypus readout before claiming a gap.",
    },
    {
        "id": "NEG-ECHIDNA-COLLECTIVE-LIMIT",
        "claim": "Collective echidna readout of platypus packets beats adaptive product readout.",
        "reason_invalid": "A certified semidefinite bound caps collective echidna readout at the adaptive value.",
        "lesson": "Bound collective platypus readout before claiming any gap.",
    },
]


def _corpus_with(fake_repo: Path, extra: list[dict]) -> Corpus:
    path = fake_repo / "research" / "registry" / "negative_results.json"
    path.write_text(json.dumps(NEGATIVES + extra, indent=2), encoding="utf-8")
    corpus = Corpus(fake_repo)
    corpus.refresh()
    return corpus


def _sweep_records() -> list[dict]:
    return [
        {"id": f"{family}-{i}", "claim": claim, "reason_invalid": "Sweep point.", "lesson": "Sweep."}
        for family, claim in SWEEPS.items()
        for i in range(1, 11)
    ]


def test_near_duplicates_finds_the_planted_pair(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, [DUP_A, DUP_B])
    pairs = near_duplicates(corpus)
    assert (pairs[0].a, pairs[0].b) == ("negative:NEG-DUP-A", "negative:NEG-DUP-B")
    assert pairs[0].score >= 0.8
    assert pairs[0].title_a == DUP_A["claim"]
    assert not any(HELSTROM in (pair.a, pair.b) for pair in pairs)
    assert near_duplicates(corpus, threshold=1.01) == []


def test_per_family_cap_keeps_a_true_restatement_visible(fake_repo: Path) -> None:
    corpus = _corpus_with(fake_repo, _sweep_records() + RESTATEMENT)
    restatement = ("negative:NEG-ECHIDNA-COLLECTIVE-LIMIT", "negative:NEG-ECHIDNA-READOUT-BOUND")
    crowded = near_duplicates(corpus, limit=10)
    assert restatement not in [(pair.a, pair.b) for pair in crowded]  # siblings fill the top 10
    capped = near_duplicates(corpus, limit=10, per_family=2)
    assert restatement in [(pair.a, pair.b) for pair in capped]
    assert len(capped) == 3 * 2 + 1


@pytest.fixture
def corpus(fake_repo: Path) -> Corpus:
    corpus = Corpus(fake_repo)
    corpus.refresh()
    return corpus


def test_check_claim_returns_cosine_scored_negatives_above_threshold(corpus: Corpus) -> None:
    hits = check_claim(corpus, NEAR_CLAIM)
    assert hits[0].doc_id == HELSTROM
    assert 0.6 <= hits[0].score <= 1.0
    assert all(hit.kind == "negative" and hit.score >= 0.6 for hit in hits)
    assert check_claim(corpus, "zebrafish migration") == []


def test_cosine_of_a_doc_with_itself_is_one(corpus: Corpus) -> None:
    doc = corpus.get(HELSTROM)
    assert corpus.cosine(f"{doc.title} {doc.text}", [HELSTROM])[HELSTROM] == pytest.approx(1.0, abs=1e-5)


def test_cli_near_duplicates_writes_json_and_markdown(fake_repo: Path, tmp_path: Path, capsys) -> None:
    _corpus_with(fake_repo, [DUP_A, DUP_B])
    out = tmp_path / "dups.json"
    assert main(["--root", str(fake_repo), "near-duplicates", "--threshold", "0.8", "--out", str(out)]) == 0
    payload = json.loads(out.read_text())
    assert set(payload) == {"kind", "threshold", "pairs", "generated_on"}
    assert (payload["kind"], payload["threshold"]) == ("negative", 0.8)
    assert (payload["pairs"][0]["a"], payload["pairs"][0]["b"]) == ("negative:NEG-DUP-A", "negative:NEG-DUP-B")
    markdown = (tmp_path / "DUPS.md").read_text()
    assert "| 1.000 | NEG-DUP-A | NEG-DUP-B |" in markdown
    capsys.readouterr()
    assert main(["--root", str(fake_repo), "near-duplicates", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["pairs"][0]["b"] == "negative:NEG-DUP-B"


def test_cli_check_new_exit_code_gates_on_a_match(fake_repo: Path, tmp_path: Path, capsys) -> None:
    root = ["--root", str(fake_repo)]
    assert main([*root, "check-new", "--text", NEAR_CLAIM]) == 2
    assert "NEG-DCP-LOCAL-HELSTROM-HIERARCHY" in capsys.readouterr().out
    assert main([*root, "check-new", "--text", "zebrafish migration", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["matches"] == [] and payload["duplicate"] is False and "index_incomplete" in payload
    record = tmp_path / "record.json"
    record.write_text(json.dumps(NEGATIVES[0], indent=2))
    assert main([*root, "check-new", "--file", str(record)]) == 2
