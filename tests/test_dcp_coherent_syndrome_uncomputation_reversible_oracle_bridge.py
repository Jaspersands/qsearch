"""Tests for dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pytest

from theorems.dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge import (
    generate_dcp_coherent_syndrome_uncomputation_reversible_oracle_certificate,
    verify_branch_helstrom_and_unitary_invariance,
    verify_known_offset_controlled_uncomputation_control,
    branch_state,
    native_cnot_collimation_audit,
)


def test_branch_helstrom_and_convexity() -> None:
    res = verify_branch_helstrom_and_unitary_invariance(
        theta_s=[0.0, 0.0, 0.0, 0.0],
        theta_s_prime=[math.pi, -math.pi / 2.0, math.pi / 2.0, 0.0],
    )
    assert res["data_processing_hierarchy_holds"] is True
    assert res["coherent_joint_trace_distance"] > res["traceout_trace_distance"]


def test_coherent_counterexample_refutes_the_previous_branch_average_upper_bound():
    row = verify_branch_helstrom_and_unitary_invariance([0, 0], [0, math.pi])
    assert row["coherent_joint_trace_distance"] == pytest.approx(math.sqrt(3)/2)
    assert row["dephased_syndrome_trace_distance"] == pytest.approx(.5)
    assert row["traceout_trace_distance"] == pytest.approx(.5)
    assert row["v1_branch_average_is_not_a_coherent_upper_bound"]


@pytest.mark.parametrize("branches", [1, 2, 4, 8])
def test_independent_density_eigenvalues_dephasing_traceout_and_unitary(branches):
    rng = np.random.default_rng(71+branches)
    theta, other, alpha, alpha_prime = rng.uniform(-4, 4, size=(4, branches))
    state, prime = np.array(branch_state(theta, alpha)), np.array(branch_state(other, alpha_prime))
    delta = np.outer(state, state.conj())-np.outer(prime, prime.conj())
    dephased = delta.copy()
    for i in range(2*branches):
        for j in range(2*branches):
            if i//2 != j//2:
                dephased[i, j] = 0
    discarded = sum(delta[2*d:2*d+2, 2*d:2*d+2] for d in range(branches))
    distance = lambda matrix: np.abs(np.linalg.eigvalsh(matrix)).sum()/2
    row = verify_branch_helstrom_and_unitary_invariance(
        theta, other, branch_phases_s=alpha, branch_phases_s_prime=alpha_prime)
    assert row["coherent_joint_trace_distance"] == pytest.approx(distance(delta), abs=2e-14)
    assert row["dephased_syndrome_trace_distance"] == pytest.approx(distance(dephased), abs=2e-14)
    assert row["traceout_trace_distance"] == pytest.approx(distance(discarded), abs=2e-14)
    unitary, _ = np.linalg.qr(rng.normal(size=delta.shape)+1j*rng.normal(size=delta.shape))
    assert distance(unitary@delta@unitary.conj().T) == pytest.approx(distance(delta), abs=2e-14)
    assert row["data_processing_hierarchy_holds"]


@pytest.mark.parametrize("wires", [1, 2, 3, 5])
def test_native_product_state_cnot_permutation_retains_secret_dependent_branch_phases(wires):
    row = native_cnot_collimation_audit([0]*wires, [math.pi/(j+2) for j in range(wires)])
    assert row["max_native_permutation_error"] < 1e-13
    assert row["native_inner_product_error"] < 1e-13
    assert row["branch_accounting"]["data_processing_hierarchy_holds"]
    if wires > 1:
        assert row["dropping_branch_phases_changes_coherent_distance"]


def test_relative_branch_phases_cannot_be_dropped_as_global_gauge():
    same = verify_branch_helstrom_and_unitary_invariance([0, 0], [0, 0])
    opposite = verify_branch_helstrom_and_unitary_invariance(
        [0, 0], [0, 0], branch_phases_s_prime=[0, math.pi])
    assert same["coherent_joint_trace_distance"] < 3e-8
    assert opposite["coherent_joint_trace_distance"] == pytest.approx(1)
    assert opposite["dephased_syndrome_trace_distance"] == pytest.approx(0)


@pytest.mark.parametrize("theta,prime", [([], []), ([0]*3, [0]*3), ([0], [0, 0]), ([math.nan], [0])])
def test_invalid_branch_models_rejected(theta, prime):
    with pytest.raises(ValueError):
        verify_branch_helstrom_and_unitary_invariance(theta, prime)


def test_known_offset_constructive_control() -> None:
    ctrl = verify_known_offset_controlled_uncomputation_control(
        theta_0_s=0.0,
        theta_0_s_prime=math.pi / 2.0,
        known_offsets=[0.0, 0.4, -0.7, 1.1],
    )
    assert ctrl["deterministic_uncomputation_exact"] is True
    assert ctrl["unitary_helstrom_preserved"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_coherent_syndrome_uncomputation_reversible_oracle_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
