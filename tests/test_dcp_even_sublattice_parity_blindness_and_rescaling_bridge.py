"""Tests for dcp_even_sublattice_parity_blindness_and_rescaling_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_even_sublattice_parity_blindness_and_rescaling_bridge import (
    generate_dcp_even_sublattice_parity_blindness_and_rescaling_certificate,
    verify_even_effective_column_identity,
    verify_odd_target_impossibility_and_halving_isomorphism,
    verify_upper_bit_ensemble_rescaled_uniformity,
)


def test_even_effective_column_identity() -> None:
    res = verify_even_effective_column_identity([[3, 5, 2]], [1, 1, 0], t_bits=3)
    assert res["in_mod2_kernel"] is True
    assert res["all_effective_columns_even"] is True
    assert res["halving_bijection_holds"] is True


def test_fixed_instance_resonant_controls_and_t1_blindness() -> None:
    t1 = verify_odd_target_impossibility_and_halving_isomorphism([[1, 1]], [[1, 1]], t_bits=1)
    assert t1["odd_target_strictly_blind"] is True
    assert t1["mean_conditional_advantage"] == 0.0

    c20 = verify_odd_target_impossibility_and_halving_isomorphism([[2, 0]], [[1, 1]], t_bits=2)
    assert c20["halving_isomorphism_exact"] is True
    assert abs(c20["mean_conditional_advantage"] - 1.0) < 1e-12
    assert abs(c20["unconditional_branch_contribution"] - 0.5) < 1e-12

    c11 = verify_odd_target_impossibility_and_halving_isomorphism([[1, 1]], [[1, 1]], t_bits=2)
    assert c11["halving_isomorphism_exact"] is True
    assert abs(c11["mean_conditional_advantage"] - 0.5) < 1e-12
    assert abs(c11["unconditional_branch_contribution"] - 0.25) < 1e-12


def test_upper_bit_ensemble_rescaled_uniformity() -> None:
    u = verify_upper_bit_ensemble_rescaled_uniformity(
        a_mod2=[[1, 1, 0]],
        v_basis=[[1, 1, 0]],
        x0_vec=[0, 1, 0],
        t_bits=3,
    )
    assert u["q_even_sublattice_size"] == 4
    assert u["exact_iid_uniform_over_even_sublattice"] is True
    assert u["bound_respected"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_even_sublattice_parity_blindness_and_rescaling_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_even_sublattice_parity_blindness_and_rescaling_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_even_sublattice_parity_blindness_and_rescaling_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
