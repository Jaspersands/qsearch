"""Tests for dcp_anchor_conditioned_adaptive_syndrome_routing_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_anchor_conditioned_adaptive_syndrome_routing_bridge import (
    evaluate_adaptive_vs_blind_stage2_mod4_routing,
    generate_dcp_anchor_conditioned_adaptive_syndrome_routing_certificate,
    verify_coset_gauge_equivariance_and_mod4_invariance,
    verify_single_wire_unitary_invariance_obstruction,
)


def test_coset_gauge_equivariance_and_mod4_invariance() -> None:
    res = verify_coset_gauge_equivariance_and_mod4_invariance(
        a_matrix=[[1, 3, 5, 7]],
        v_matrix=[[1, 0], [1, 0], [0, 1], [0, 1]],
        t_bits=3,
    )
    assert res["sign_equivariance_mod_2t_verified"] is True
    assert res["mod4_coset_invariance_verified"] is True
    assert res["distinct_mod4_tuples_across_syndromes"] == 4


def test_single_wire_unitary_invariance_obstruction() -> None:
    obs = verify_single_wire_unitary_invariance_obstruction(
        a_row=[1, 3],
        v_col=[1, 1],
        t_bits=3,
        s_target=2,
    )
    assert obs["single_wire_unitary_invariance_verified"] is True
    assert abs(obs["zero_mod4_syndrome_fraction"] - 0.5) < 1e-12
    assert abs(obs["two_mod4_syndrome_fraction"] - 0.5) < 1e-12


def test_adaptive_stage2_routing_100_percent_mod4_coverage() -> None:
    route_1d = evaluate_adaptive_vs_blind_stage2_mod4_routing(
        a_matrix=[[1, 3, 5, 7]],
        v_matrix=[[1, 0], [1, 0], [0, 1], [0, 1]],
        t_bits=3,
        blind_w=[1, 1],
        s_calibration=[3],
    )
    assert abs(route_1d["blind_fixed_cnot_mod4_zero_fraction"] - 0.5) < 1e-12
    assert abs(route_1d["single_wire_selection_mod4_zero_fraction"] - 0.75) < 1e-12
    assert abs(route_1d["adaptive_cnot_routing_mod4_zero_fraction"] - 1.0) < 1e-12
    assert route_1d["all_coset_representatives_and_stage2_branches_consistent"] is True
    assert route_1d["max_statevector_routing_residual"] < 1e-12


def test_input_validation_rejects_overlapping_or_non_kernel_inputs() -> None:
    try:
        verify_coset_gauge_equivariance_and_mod4_invariance(
            a_matrix=[[1, 1, 2]],
            v_matrix=[[1, 1], [1, 0], [0, 1]],
            t_bits=3,
        )
        raise AssertionError("Expected ValueError for overlapping V supports")
    except ValueError as exc:
        assert "disjoint supports" in str(exc)

    try:
        verify_coset_gauge_equivariance_and_mod4_invariance(
            a_matrix=[[1, 2]],
            v_matrix=[[1], [1]],
            t_bits=3,
        )
        raise AssertionError("Expected ValueError for non-kernel V column")
    except ValueError as exc:
        assert "ker(A mod 2)" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_anchor_conditioned_adaptive_syndrome_routing_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_anchor_conditioned_adaptive_syndrome_routing_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_anchor_conditioned_adaptive_syndrome_routing_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
    assert data["adaptiveFraction"] == 1.0
