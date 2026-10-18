"""Tests for dcp_multicopy_distinct_header_cyclic_swap_interference_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_multicopy_distinct_header_cyclic_swap_interference_bridge import (
    generate_dcp_multicopy_distinct_header_cyclic_swap_interference_certificate,
    verify_cyclic_shift_bipartite_even_flip_identity,
    verify_three_copy_distinct_header_symmetric_projection_pairwise_law,
)


def test_cyclic_shift_bipartite_even_flip_identity() -> None:
    for thetas, gammas in [
        ([0.3, 1.1], [0.85, 0.75]),
        ([0.2, 0.9, 2.1], [0.9, 0.8, 0.7]),
        ([0.15, 0.85, 1.75, 2.65], [0.9, 0.85, 0.8, 0.75]),
        ([0.1, 0.7, 1.4, 2.2, 2.9], [0.9, 0.85, 0.8, 0.75, 0.7]),
    ]:
        res = verify_cyclic_shift_bipartite_even_flip_identity(thetas, gammas)
        assert res["exact_even_flip_law_verified"] is True


def test_three_copy_distinct_header_symmetric_projection_pairwise_law() -> None:
    res = verify_three_copy_distinct_header_symmetric_projection_pairwise_law(
        thetas=[0.25, 1.15, 2.35],
        gammas=[0.9, 0.8, 0.7],
    )
    assert res["three_body_sum_absent_in_sym3_projector_verified"] is True
    assert res["pairwise_formula_error"] < 1e-12
    assert res["common_shift_invariance_error"] < 1e-12


def test_input_validation_rejects_mismatched_lengths() -> None:
    try:
        verify_cyclic_shift_bipartite_even_flip_identity([0.1, 0.2], [0.8])
        raise AssertionError("Expected ValueError for mismatched lengths")
    except ValueError as exc:
        assert "matching length" in str(exc)


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_multicopy_distinct_header_cyclic_swap_interference_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_multicopy_distinct_header_cyclic_swap_interference_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_multicopy_distinct_header_cyclic_swap_interference_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
