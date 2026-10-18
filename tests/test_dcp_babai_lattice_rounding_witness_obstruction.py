"""Tests for dcp_babai_lattice_rounding_witness_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
import itertools
from fractions import Fraction
from pathlib import Path

from theorems.dcp_babai_lattice_rounding_witness_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_babai_lattice_rounding_witness_obstruction_report,
    evaluate_instance,
    native_label_controls,
    build_qary_kernel_lll_basis,
    babai_round_exact,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_coset_bijection_and_parallelepiped_vertex_identity() -> None:
    report = build_dcp_babai_lattice_rounding_witness_obstruction_report()
    assert report["summary"]["theorem1_coset_parallelepiped_identity_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem1_coset_parallelepiped_identity_passed"] is True
        assert inst["lattice_determinant"] == inst["q"] ** inst["n"]
        assert inst["coset_invariance_verified_targets"] == inst["total_targets"]
        assert (
            inst["valid_boolean_witness_targets"]
            == inst["parallelepiped_boolean_vertex_count"]
        )


def test_theorem2_half_integer_box_overflow_dichotomy() -> None:
    report = build_dcp_babai_lattice_rounding_witness_obstruction_report()
    assert report["summary"]["theorem2_half_integer_dichotomy_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem2_half_integer_dichotomy_passed"] is True
        assert (
            inst["valid_boolean_witness_targets"] + inst["box_overflow_target_count"]
            == inst["total_targets"]
        )
        assert inst["half_integer_dichotomy_verified_targets"] == inst["total_targets"]
        assert inst["overflow_observed"] == (inst["box_overflow_target_count"] > 0)


def test_theorem3_direct_filter_and_forward_swap_babai_formula() -> None:
    report = build_dcp_babai_lattice_rounding_witness_obstruction_report()
    assert report["summary"]["theorem3_babai_filter_swap_formula_passed"] is True
    for inst in report["instances"]:
        assert inst["theorem3_babai_filter_swap_formula_passed"] is True
        assert inst["swap_reciprocal_valid_pairs"] == inst["paired_valid_targets_for_h"]
        beta = Fraction(inst["verified_coverage_beta_babai_exact"])
        assert beta == Fraction(
            inst["valid_boolean_witness_targets"], inst["total_targets"]
        )


def test_sheared_lll_basis_can_have_no_boolean_overflow() -> None:
    result = evaluate_instance({"instance_id": "counterexample", "n": 1,
                                "t": 2, "K": 2, "A": [[2, 1]]})
    assert any(v not in (0, -2, 2) for row in result["B_col"] for v in row)
    assert result["box_overflow_target_count"] == 0
    assert result["verified_coverage_beta_babai_exact"] == "1"
    assert result["forward_swap_advantage_babai_exact"] == "1/2"
    assert result["theorem2_half_integer_dichotomy_passed"] is True


def test_binary_weight_family_is_not_excluded_by_volume_ratio() -> None:
    for bits in range(2, 9):
        result = evaluate_instance({"instance_id": "binary_weights", "n": 1,
                                   "t": bits, "K": bits,
                                   "A": [[1 << j for j in range(bits)]]})
        assert result["instance_passed"] is True
        assert result["box_overflow_target_count"] == 0
        assert result["direct_filter_success_babai_exact"] == "1"
        assert result["forward_swap_advantage_babai_exact"] == "1/2"


def test_native_label_controls_match_independent_exact_rational_rounding() -> None:
    report = native_label_controls(bits_grid=(2, 3), matrices_per_size=5, seed=11)
    assert report["asymptotic_advantage_or_decay_proved"] is False
    assert report["quantum_circuit_compiled"] is False
    for row in report["rows"]:
        if row["rank_failure_counted_as_zero_success"]:
            assert row["direct_filter_success"] == "0"
            continue
        q, A = 1 << row["phase_bits"], row["A"]
        piv, inverse, B, invB = build_qary_kernel_lll_basis(A, row["phase_bits"])
        valid = set()
        for target in itertools.product(range(q), repeat=row["n"]):
            initial = [0] * row["K"]
            for i, pivot in enumerate(piv):
                initial[pivot] = sum(inverse[i][j]*target[j] for j in range(row["n"])) % q
            witness, _, _ = babai_round_exact(initial, B, invB)
            if all(v in (0, 1) for v in witness):
                valid.add(target)
        beta = Fraction(len(valid), q**row["n"])
        paired = Fraction(sum(((u[0]+q//2) % q, *u[1:]) in valid for u in valid), q**row["n"])
        assert Fraction(row["coverage_fraction"]) == beta
        assert Fraction(row["direct_filter_success"]) == beta**2
        assert Fraction(row["forward_swap_advantage"]) == paired/2


def test_native_controls_retain_rank_failures(monkeypatch) -> None:
    class ZeroReplay:
        def __init__(self, seed):
            pass

        def randrange(self, q):
            return 0

    monkeypatch.setattr("theorems.dcp_babai_lattice_rounding_witness_obstruction.random.Random", ZeroReplay)
    report = native_label_controls(bits_grid=(3,), matrices_per_size=2)
    assert len(report["rows"]) == 2
    assert all(row["rank_failure_counted_as_zero_success"] for row in report["rows"])
    assert all(row["finder_calls"] == 0 for row in report["rows"])


def test_native_controls_sample_large_target_space_without_full_table() -> None:
    report = native_label_controls(bits_grid=(12,), matrices_per_size=2, target_samples=7)
    assert report["fixed_seed_is_not_IID_confidence_certificate"] is True
    for row in report["rows"]:
        if not row["rank_failure_counted_as_zero_success"]:
            assert row["finder_calls"] == 21
            assert row["target_evaluation"] == "pseudo_random_target_replay_not_confidence_certificate"


def test_live_native_control_artifact_replays_without_changing_claim_scope() -> None:
    import hashlib
    module = ROOT/"theorems/dcp_babai_lattice_rounding_witness_obstruction.py"
    artifact = ROOT/"research/phase_workbench/dcp_coordinate_rounding_native_controls.json"
    stored = json.loads(artifact.read_text())
    rebuilt = native_label_controls()
    assert stored == rebuilt
    assert stored["source_sha256"] == hashlib.sha256(module.read_bytes()).hexdigest()
    assert stored["fixed_seed_is_not_IID_confidence_certificate"] is True
    assert stored["reported_rates_are_replay_frequencies_not_performance_guarantees"] is True


def test_2adic_inverse_does_not_truncate_large_public_integer_labels() -> None:
    from theorems.dcp_clean_linear_witness_carry_obstruction import invert_matrix_mod_2adic
    q = 1 << 100
    A = [[q-1, q-2], [2, 3]]
    inverse = invert_matrix_mod_2adic(A, 100)
    assert [[sum(A[i][k]*inverse[k][j] for k in range(2)) % q for j in range(2)]
            for i in range(2)] == [[1, 0], [0, 1]]


def test_artifact_and_honesty_guardrails() -> None:
    report = build_dcp_babai_lattice_rounding_witness_obstruction_report()
    assert report["summary"]["all_theorems_passed"] is True
    hg = report["honesty_guardrails"]
    assert hg["accepted_speedup_candidate"] is False
    assert hg["new_active_negative_result_created"] is False
    assert hg["novelty_claim"] is False
    if DEFAULT_ARTIFACT_PATH.exists():
        on_disk = json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))
        assert on_disk["sha256"] == report["sha256"]


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / "theorems"
                / "dcp_babai_lattice_rounding_witness_obstruction.py"
            ),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True
