"""Fixtures for the tools/ test suites: a tiny fake Q-Search checkout."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest


NEGATIVES = [
    {
        "applies_to": ["DCP", "PO-MEASUREMENT"],
        "claim": "Local Helstrom readout of each dihedral coset packet dominates every product X-basis readout.",
        "evidence": {"status": "derived-review-pending", "modulus": 64},
        "id": "NEG-DCP-LOCAL-HELSTROM-HIERARCHY",
        "lesson": "Local binary optimality does not order product measurements.",
        "reason_invalid": "An explicit modulus-64 counterexample has X-basis success above the product of local Helstrom successes.",
        "source": "theorems/dcp_multi_packet.py",
    },
    {
        "applies_to": ["OPI", "PO-DEQUANTIZATION"],
        "claim": "Prime-field optimal polynomial intersection with mixed quadratic cosets has no efficient classical solver.",
        "evidence": {"artifact": "research/classical_baselines/norm.json"},
        "id": "NEG-OPI-MIXED-COSET-HARDNESS",
        "lesson": "Test quadratic-extension norm constructions before claiming OPI hardness.",
        "reason_invalid": "A polynomial norm construction over the quadratic extension field solves both saved inputs perfectly.",
        "source": "theorems/prime_character_norm_attack.py",
    },
]

QUARANTINED = [
    {
        "id": "NEG-ANNEALING-GAP-BARRIER",
        "original_record": {
            "claim": "Quantum annealing achieves superpolynomial speedups via tunneling.",
            "reason_invalid": "Exponentially small spectral gaps force exponential runtime.",
            "applies_to": ["QUANTUM-ANNEALING"],
        },
        "retraction_reasons": ["The barrier was stated as a universal no-go without a scoped proof."],
        "status": "QUARANTINED_OVERBROAD_NO_GO",
    }
]

DEQUANT = [
    {
        "blocks_speedup_claim": True,
        "claim_under_test": "Polar successive cancellation source shaping prepares the Gibbs state classically.",
        "evidence": "TV bound 0.010221 at N=32768.",
        "id": "DEQ-POLAR-GIBBS-SOURCE",
        "required_action": "Charge the classical sampler before claiming a quantum Gibbs advantage.",
        "severity": "high",
        "target_id": "BPQM-GIBBS",
        "target_type": "candidate",
    }
]

PROOF_STATUS = [
    {
        "candidate_id": "CODE-COSET-COLLECTIVE",
        "evidence": "Linear code equivalence families.",
        "field": "problem_family",
        "next_action": "Convert this prose obligation into a formal lemma.",
        "obligation_id": "PO-FAMILY",
        "status": "text-present",
    }
]

NOTE = textwrap.dedent(
    """\
    # Fixed-Input OPI: A Smaller Classical Field-Size Guarantee

    2026-10-18. LOCAL APPLICATION REVIEW PENDING. No novelty is claimed.

    ## Scientific Question And Outcome

    Can the verified Morse norm solver avoid a factorial-genus error when
    the exterior power characters are used?

    ## Exact Cycle Indicator

    The determinant det(1 - t sigma) on the standard representation gives
    the n-cycle indicator as an alternating sum of exterior characters.
    """
)

SUPERSEDED_NOTE = textwrap.dedent(
    """\
    # Old Hierarchy Claim

    SUPERSEDED by the counterexample note.

    ## Claim

    Local Helstrom readout dominates product readout.
    """
)

HANDOFF = textwrap.dedent(
    """\
    # Research Agent Handoff

    Last updated: 2026-10-18

    ## Exterior-Trace Classical Falsifier

    Previous goal turn was PROGRESS. The exterior bound lowers the field threshold.

    ## Fixed-Input Morse Norm Solver

    Explicit geometry and field conditions for the Morse solver.

    ## Fixed-Input Morse Norm Solver

    An older pass with the same heading.
    """
)

THEOREM = textwrap.dedent(
    '''\
    """Exterior-character bound for the fixed-input Morse norm solver.

    Computes alternating exterior characters of the standard representation.
    """

    REPORT = "research/classical_baselines/prime_character_exterior_bound.json"


    def exterior_characters(cycle_lengths):
        """Return the exterior-power characters for a cycle type."""
        return []


    def large_fixed_input_control():
        return None
    '''
)

LITERATURE = [
    {
        "abstract": "Decoded quantum interferometry reduces optimization to decoding.",
        "id": "jordan-dqi-2024",
        "mechanism": "Prepare a superposition weighted by a polynomial and decode syndromes.",
        "no_go_barrier": "Requires efficient decoding of the dual code.",
        "open_question": "Which structured problems admit decoders?",
        "problem_family": "Optimal polynomial intersection",
        "proof_technique": "Semicircle law",
        "reduction": "OPI to Reed-Solomon decoding",
        "reusable_abstraction": "Decoder-to-optimizer reduction",
        "source": "seed",
        "tags": ["dqi", "opi"],
        "title": "Optimization by Decoded Quantum Interferometry",
        "url": "https://arxiv.org/abs/2408.08292",
        "year": 2024,
    }
]

AUDIT = {
    "status": "PRIMARY_APPLICABILITY_AUDIT",
    "checked_on": "2026-10-05",
    "records": [
        {
            "id": "ARXIV-quant-ph-0501044-v2",
            "title": "Optimal measurements for the dihedral hidden subgroup problem",
            "url": "https://arxiv.org/html/quant-ph/0501044",
            "mechanism": "Collective PGM expressed through subset-sum fiber multiplicities.",
        }
    ],
}

HYPOTHESIS = {
    "contract_id": "BPQM-GIBBS-FRONTIER",
    "status": "classical-competitor-found",
    "problem": "Sample the Gibbs distribution of a random-sign polar code objective.",
    "mechanism": "Belief propagation with quantum messages.",
}


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_fake_repo(root: Path) -> Path:
    registry = root / "research" / "registry"
    _write_json(registry / "negative_results.json", NEGATIVES)
    _write_json(registry / "quarantined_campaign_negatives.json", QUARANTINED)
    _write_json(registry / "dequantization_checks.json", DEQUANT)
    _write_json(registry / "proof_status.json", PROOF_STATUS)
    _write_json(registry / "reductions.json", {"edges": [], "counts": {}})
    (root / "research" / "PRIME_CHARACTER_EXTERIOR_BOUND.md").write_text(NOTE, encoding="utf-8")
    (root / "research" / "OLD_HIERARCHY.md").write_text(SUPERSEDED_NOTE, encoding="utf-8")
    (root / "research" / "AGENT_HANDOFF.md").write_text(HANDOFF, encoding="utf-8")
    theorems = root / "theorems"
    theorems.mkdir(parents=True, exist_ok=True)
    (theorems / "prime_character_exterior_bound.py").write_text(THEOREM, encoding="utf-8")
    (theorems / "broken_module.py").write_text("def broken(:\n    pass\n", encoding="utf-8")
    _write_json(root / "research" / "literature_records.json", LITERATURE)
    _write_json(root / "research" / "literature_audits" / "dihedral_sources.json", AUDIT)
    _write_json(root / "research" / "hypotheses" / "bpqm_gibbs_frontier_contract.json", HYPOTHESIS)
    return root


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    return build_fake_repo(tmp_path / "repo")
