"""Tests for dcp_multi_packet_collective_helstrom_product_likelihood_bridge."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import pytest

from theorems.dcp_multi_packet_collective_helstrom_product_likelihood_bridge import (
    evaluate_three_tier_distinct_header_decision_hierarchy,
    generate_dcp_multi_packet_collective_helstrom_product_likelihood_certificate,
)


def test_three_tier_distinct_header_decision_hierarchy() -> None:
    res = evaluate_three_tier_distinct_header_decision_hierarchy(
        thetas=[math.pi / 3.0, math.pi / 2.0],
        gammas=[0.85, 0.8],
    )
    assert res["strict_three_tier_hierarchy_holds"] is True
    assert res["sign_symmetrization_collapses_to_x_basis"] is True


def test_input_validation_rejects_mismatched_packets() -> None:
    try:
        evaluate_three_tier_distinct_header_decision_hierarchy([0.5, 0.6], [0.8])
        raise AssertionError("Expected ValueError for mismatched packet counts")
    except ValueError as exc:
        assert "matching length" in str(exc)


def test_local_binary_optimality_does_not_order_product_experiments():
    theta = [math.pi / 2, 17 * math.pi / 32]
    res = evaluate_three_tier_distinct_header_decision_hierarchy(theta, [1, 1])
    # Independent pure-state overlap and two symmetric-coin calculations.
    collective = math.sqrt(1 - math.prod(math.cos(t / 2) ** 2 for t in theta))
    tilted = max(math.sin(t / 2) for t in theta)
    x_tv = 1 - math.prod(math.cos(t / 2) ** 2 for t in theta)
    assert res["tier3_collective_helstrom_tv"] == pytest.approx(collective, abs=1e-12)
    assert res["tier2_separable_tilted_helstrom_tv"] == pytest.approx(tilted, abs=1e-12)
    assert res["tier1_x_basis_tv"] == pytest.approx(x_tv, abs=1e-12)
    assert collective > x_tv > tilted
    assert not res["strict_three_tier_hierarchy_holds"]


def test_an_uninformative_second_packet_does_not_force_a_strict_collective_gain():
    res = evaluate_three_tier_distinct_header_decision_hierarchy([0.7, 1.1], [0.8, 0])
    assert res["tier3_collective_helstrom_tv"] == pytest.approx(res["tier2_separable_tilted_helstrom_tv"], abs=1e-12)
    assert not res["strict_three_tier_hierarchy_holds"]


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_multi_packet_collective_helstrom_product_likelihood_certificate()
    assert cert["all_checks_passed"] is True
    assert not cert["universal_strict_three_tier_hierarchy_claimed"]
    assert not cert["product_order_counterexample"]["evaluation"]["strict_three_tier_hierarchy_holds"]
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_multi_packet_collective_helstrom_product_likelihood_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_multi_packet_collective_helstrom_product_likelihood_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
