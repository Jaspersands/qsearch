"""Tests for dcp_clean_linear_witness_carry_obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import itertools
import numpy as np
import pytest

from theorems.dcp_clean_linear_witness_carry_obstruction import (
    DEFAULT_ARTIFACT_PATH,
    build_dcp_clean_linear_witness_carry_obstruction_report,
    compressed_parity_audit,
)


ROOT = Path(__file__).resolve().parents[1]


def test_theorem1_2adic_hensel_disjoint_boolean_translates() -> None:
    report = build_dcp_clean_linear_witness_carry_obstruction_report()
    assert report["summary"]["theorem1_hensel_disjoint_translate_passed"] is True
    assert report["summary"]["max_hensel_swap_advantage"] == 0.0
    for inst in report["instances"]:
        ha = inst["hensel_audit"]
        assert ha["theorem1_passed"] is True
        assert ha["valid_boolean_witness_count"] == (1 << inst["n"])
        assert ha["paired_valid_targets_for_h"] == 0
        assert ha["forward_swap_nonzero_entries"] == 0
        assert ha["forward_swap_advantage_exact"] == "0"
        assert Fraction(ha["verified_coverage_beta_exact"]) == Fraction(
            1 << inst["n"], inst["q"] ** inst["n"]
        )


def test_theorem2_f2_rref_carry_parity_vanishing_criterion() -> None:
    report = build_dcp_clean_linear_witness_carry_obstruction_report()
    assert report["summary"]["theorem2_f2_rref_carry_parity_vanishing_passed"] is True
    for inst in report["instances"]:
        fa = inst["f2_rref_audit"]
        assert fa["theorem2_passed"] is True
        assert fa["bitwise_identity_verified_targets"] == inst["total_targets"]
        assert fa["carry_equivalence_verified_targets"] == inst["total_targets"]
        assert fa["num_carry_constraints"] == inst["n"] * (inst["t"] - 1)


def test_theorem3_disjoint_support_kernel_linearization() -> None:
    report = build_dcp_clean_linear_witness_carry_obstruction_report()
    assert report["summary"]["theorem3_disjoint_kernel_linearization_passed"] is True
    for inst in report["instances"]:
        dk = inst["disjoint_kernel_audit"]
        assert dk["theorem3_passed"] is True
        assert dk["m_disjoint_directions"] <= dk["max_possible_disjoint_directions"]
        assert dk["linearization_verified_assignments"] == (
            1 << dk["m_disjoint_directions"]
        )
        assert dk["iid_uniform_full_group_assumption_valid"] is False
        assert dk["compressed_source_average_advantage_upper_exact"] is None
        assert dk["parity_audit"]["effective_columns_all_even"] is True
        parity = dk["parity_audit"]
        probability = Fraction(1, 1 << (dk["K_dk"] - dk["m_disjoint_directions"]))
        assert Fraction(parity["selected_affine_subspace_probability_exact"]) == probability
        for endpoint in ("lower", "upper"):
            assert Fraction(parity[f"selected_branch_unconditional_advantage_{endpoint}_exact"]) == (
                probability * Fraction(parity[f"optimal_conditional_advantage_{endpoint}_exact"]))
        assert parity["source_average_bound_inferred"] is False


def test_asymptotic_scaling_and_honesty_guardrails() -> None:
    report = build_dcp_clean_linear_witness_carry_obstruction_report()
    assert report["summary"]["all_theorems_passed"] is True
    for row in report["asymptotic_scaling"]:
        assert row["hensel_coverage_beta_power_of_two_neg_exponent"] == row["n"] * (
            row["t"] - 1
        )
        assert row["hensel_forward_swap_advantage_exact"] == "0"
        assert row["disjoint_kernel_average_advantage_upper_power_of_two_neg_exponent"] is None
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
            str(ROOT / "theorems" / "dcp_clean_linear_witness_carry_obstruction.py"),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["summary"]["all_theorems_passed"] is True


@pytest.mark.parametrize("bits", range(2, 9))
def test_one_even_effective_label_can_reveal_parity_perfectly(bits: int) -> None:
    # A=(1,q/2-1), V=(1,1) is a valid disjoint mod-2 kernel direction.
    q = 1 << bits
    a = [1, q // 2 - 1]
    assert sum(a) % 2 == 0
    audit = compressed_parity_audit([[sum(a) % q]], bits)
    assert audit["effective_columns_all_even"] is True
    assert audit["optimal_conditional_advantage_exact"] == "1/2"
    assert Fraction(audit["optimal_conditional_advantage_exact"]) > Fraction(1, 2 * q)


@pytest.mark.parametrize("bits", range(2, 7))
def test_actual_conditioned_odd_pair_law_violates_old_full_group_average_bound(bits: int) -> None:
    q = 1 << bits
    total = Fraction(0)
    pairs = list(itertools.product(range(1, q, 2), repeat=2))
    for a, b in pairs:
        audit = compressed_parity_audit([[(a + b) % q]], bits)
        total += Fraction(audit["optimal_conditional_advantage_exact"])
    actual_mean = total / len(pairs)
    assert actual_mean == Fraction(1, q)
    assert actual_mean == 2 * Fraction(1, 2 * q)


@pytest.mark.parametrize("labels,bits", [
    ([[0]], 2), ([[2]], 2), ([[2, 4, 6]], 3),
    ([[1, 1, 3]], 3), ([[2, 6], [0, 4]], 3),
])
def test_occupancy_overlap_against_independent_secret_averaged_density(labels, bits) -> None:
    q = 1 << bits
    n, m = len(labels), len(labels[0])
    rho = [np.zeros((1 << m, 1 << m), complex) for _ in range(2)]
    counts = [0, 0]
    words = list(itertools.product((0, 1), repeat=m))
    for secret in itertools.product(range(q), repeat=n):
        phases = [sum(secret[i] * sum(labels[i][j] * word[j] for j in range(m))
                      for i in range(n)) for word in words]
        state = np.exp(2j * np.pi * np.array(phases) / q) / np.sqrt(1 << m)
        parity = secret[0] % 2
        rho[parity] += np.outer(state, state.conj())
        counts[parity] += 1
    delta = rho[0] / counts[0] - rho[1] / counts[1]
    advantage = np.abs(np.linalg.eigvalsh(delta)).sum() / 4
    audit = compressed_parity_audit(labels, bits)
    lower = Fraction(audit["optimal_conditional_advantage_lower_exact"])
    upper = Fraction(audit["optimal_conditional_advantage_upper_exact"])
    assert float(lower) - 2e-14 <= advantage <= float(upper) + 2e-14
    assert upper - lower <= Fraction(1, 1 << 80)
    if labels == [[1, 1, 3]]:
        assert audit["optimal_conditional_advantage_exact"] is None


def test_selected_kernel_branch_pays_original_state_projection_probability() -> None:
    for secret in range(4):
        state = np.array([1, 1j ** secret, 1j ** secret, (-1) ** secret]) / 2
        branch = state * np.array([1, 0, 0, 1])
        probability = np.vdot(branch, branch).real
        xx = np.kron(np.array([[0, 1], [1, 0]]), np.array([[0, 1], [1, 0]]))
        signed_correct = (-1) ** secret * np.vdot(branch, xx @ branch).real
        assert probability == pytest.approx(0.5)
        assert signed_correct == pytest.approx(0.5)
        # Success-minus-one-half for the WHOLE instrument, fair guessing on failure.
        assert signed_correct / 2 == pytest.approx(0.25)


def test_reference_caps_and_label_validation_do_not_claim_hardness() -> None:
    with pytest.raises(ValueError, match="reference wires"):
        compressed_parity_audit([[0] * 17], 3)
    for labels in ([[1.0]], [[True]], [[-1]], [[8]], [[1], []]):
        with pytest.raises(ValueError):
            compressed_parity_audit(labels, 3)
