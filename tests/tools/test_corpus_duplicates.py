from __future__ import annotations

import json
from pathlib import Path

from tests.tools.conftest import NEGATIVES
from tools.corpus.api import Corpus
from tools.corpus.duplicates import near_duplicates

HELSTROM = "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"

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
