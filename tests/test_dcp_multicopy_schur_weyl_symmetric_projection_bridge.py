"""Tests for dcp_multicopy_schur_weyl_symmetric_projection_bridge."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from theorems.dcp_multicopy_schur_weyl_symmetric_projection_bridge import (
    generate_dcp_multicopy_schur_weyl_symmetric_projection_certificate,
    verify_dicke_harmonic_and_noncommuting_quadrature_separation,
    verify_half_period_commuting_majority_optimality,
    verify_symmetric_projection_secret_independence,
)


def test_symmetric_projection_secret_independence() -> None:
    for r_copies, gamma in [(2, 0.8), (3, 0.75), (4, 0.5), (3, 1.0), (3, 0.0)]:
        res = verify_symmetric_projection_secret_independence(
            r_copies=r_copies,
            gamma=gamma,
            test_thetas=[0.0, 0.4, math.pi / 3.0, math.pi / 2.0, math.pi],
        )
        assert res["secret_independent_projection_verified"] is True


def test_half_period_commuting_majority_optimality() -> None:
    for r_copies, gamma in [(2, 0.8), (3, 0.8), (4, 0.65)]:
        res = verify_half_period_commuting_majority_optimality(r_copies=r_copies, gamma=gamma)
        assert res["classical_majority_matches_collective_helstrom"] is True
        if r_copies >= 3 and 0.0 < gamma < 1.0:
            assert res["non_symmetric_sector_trace_distance_loss"] > 0.0


def test_dicke_harmonic_and_noncommuting_quadrature_separation() -> None:
    res = verify_dicke_harmonic_and_noncommuting_quadrature_separation(
        r_copies=2,
        gamma=0.8,
        theta_quad=math.pi / 2.0,
    )
    assert res["harmonic_identity_error"] < 1e-12
    assert res["collective_minus_fixed_basis_tv_gain"] > 0.08
    assert abs(res["collective_helstrom_tv"] - res["symmetric_subspace_helstrom_tv"]) < 1e-12


def test_input_validation_rejects_invalid_r_or_gamma() -> None:
    try:
        verify_half_period_commuting_majority_optimality(r_copies=0, gamma=0.5)
        raise AssertionError("Expected ValueError for r_copies=0")
    except ValueError as exc:
        assert "r_copies" in str(exc)

    try:
        verify_half_period_commuting_majority_optimality(r_copies=2, gamma=1.2)
        raise AssertionError("Expected ValueError for gamma=1.2")
    except ValueError as exc:
        assert "gamma" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_multicopy_schur_weyl_symmetric_projection_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_multicopy_schur_weyl_symmetric_projection_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_multicopy_schur_weyl_symmetric_projection_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
