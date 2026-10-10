"""Unit tests for DCP Babai Deviation Depth & Coordinate Dispersion Barrier."""

from __future__ import annotations

import json
import math
from pathlib import Path
import pytest

from theorems.dcp_babai_deviation_depth_barrier import (
    canonical_deviation_probability,
    coordinate_moment_audit,
    hoeffding_tail_bound,
    list_candidate_count,
    run_dcp_babai_deviation_depth_barrier,
    write_report,
    REPORT_PATH,
)


def test_canonical_deviation_probabilities():
    """Verify exact values and strict monotonicity of canonical deviation probabilities."""
    assert canonical_deviation_probability(0.0) == 1.0
    p1 = canonical_deviation_probability(1.0)
    p_sqrt2 = canonical_deviation_probability(math.sqrt(2.0))
    p2 = canonical_deviation_probability(2.0)
    p3 = canonical_deviation_probability(3.0)
    p4 = canonical_deviation_probability(4.0)

    assert abs(p1 - 0.617075) < 1e-4
    assert abs(p_sqrt2 - 0.479500) < 1e-4
    assert abs(p2 - 0.317311) < 1e-4
    assert abs(p3 - 0.133614) < 1e-4
    assert abs(p4 - 0.045500) < 1e-4

    # Monotonic decay
    assert 1.0 > p1 > p_sqrt2 > p2 > p3 > p4 > 0.0


def test_coordinate_moment_audit():
    """Verify Rademacher projections have variance 1/||b_i*||^2 and pairwise orthogonality."""
    audit = coordinate_moment_audit(dim=15, num_samples=3000, seed=42)
    assert audit["variance_matches_theory"] is True
    assert audit["covariance_matches_zero"] is True
    assert audit["max_abs_mean"] < 0.10
    assert abs(audit["sample_covariance_0_1"]) < 0.05


def test_list_candidate_counts():
    """Verify combinatorial list candidate count formula sum_{j=0}^k 2^j binom(d, j)."""
    for dim in [5, 10, 21, 37]:
        # Depth 0: only 1 candidate
        assert list_candidate_count(dim, 0) == 1
        # Depth 1: 1 + 2*dim
        assert list_candidate_count(dim, 1) == 1 + 2 * dim
        # Depth 2: 1 + 2*dim + 4*binom(dim, 2) = 1 + 2*dim^2
        assert list_candidate_count(dim, 2) == 1 + 2 * (dim ** 2)

    # Specific checked value: dim=21 (from n=20) -> 1 + 2*(21^2) = 883
    assert list_candidate_count(21, 2) == 883


def test_hoeffding_tail_bounds():
    """Verify Hoeffding tail bounds decay exponentially as dimension and expected deviations grow."""
    # When branch depth >= expected K, bound is 1.0
    assert hoeffding_tail_bound(2.0, 20, 2) == 1.0
    assert hoeffding_tail_bound(1.5, 20, 2) == 1.0

    # When expected K > branch depth, bound is strictly < 1.0
    b_small = hoeffding_tail_bound(5.0, 37, 2)
    assert 0.0 < b_small < 1.0

    # As dimension grows with constant deviation rate kappa=0.15:
    b_64 = hoeffding_tail_bound(0.15 * 65, 65, 2)
    b_128 = hoeffding_tail_bound(0.15 * 129, 129, 2)
    b_256 = hoeffding_tail_bound(0.15 * 257, 257, 2)

    assert b_64 > b_128 > b_256
    assert b_128 < 0.01
    assert b_256 < 1e-4


def test_report_generation_and_claim_gate(tmp_path):
    """Verify report creation, claim gating, and metric consistency."""
    test_report_path = tmp_path / "test_report.json"
    report = write_report(output_path=test_report_path, write_registry=False)

    assert test_report_path.exists()
    assert report["status"] == "dcp-babai-deviation-depth-exponential-barrier-proved"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["linear_deviation_scaling_proved"] is True
    assert report["claim_gate"]["exponential_list_coverage_collapse_proved"] is True

    # Check finite scaling rows
    rows = report["finite_scaling_rows"]
    assert len(rows) >= 5
    # Tail rows n >= 28 must have 0 empirical depth-two success
    tail_rows = [r for r in rows if r["n_bits"] >= 28]
    for tr in tail_rows:
        assert tr["empirical_depth_two_success_count"] == 0


def test_negative_result_registry_entry():
    """Verify NEG-DCP-BABAI-DEVIATION-DEPTH-EXPONENTIAL-BARRIER is recorded."""
    registry_path = Path("research/registry/negative_results.json")
    assert registry_path.exists()
    registry = json.loads(registry_path.read_text())
    entry = next(
        (item for item in registry if item.get("id") == "NEG-DCP-BABAI-DEVIATION-DEPTH-EXPONENTIAL-BARRIER"),
        None,
    )
    assert entry is not None
    assert "DHS-GOWERS-SIEVE" in entry["applies_to"]
    assert "Hoeffding" in entry["reason_invalid"]
