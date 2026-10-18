"""Tests for dcp_sieve_bucket_collision_birthday_tradeoff_audit."""

from __future__ import annotations

import json
import subprocess
import itertools
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from theorems.dcp_sieve_bucket_collision_birthday_tradeoff_audit import (
    generate_dcp_sieve_bucket_collision_birthday_tradeoff_certificate,
    verify_bucket_pairing_yield_identity_exhaustive,
    verify_multi_layer_sieve_coherence_and_controls,
    disjoint_pair_count_law,
    exact_expected_disjoint_pairs_closed_form,
)


@pytest.mark.parametrize("b", [1, 2, 3, 4])
def test_entire_occupancy_distribution_matches_independent_enumeration(b):
    for m in range(7):
        counts = Counter()
        for assignment in itertools.product(range(b), repeat=m):
            occupancy = Counter(assignment)
            counts[sum(c // 2 for c in occupancy.values())] += 1
        expected = {pairs: Fraction(count, b ** m) for pairs, count in counts.items()}
        actual = dict(disjoint_pair_count_law(m, b))
        assert actual == expected
        mean = sum((k * p for k, p in actual.items()), Fraction())
        assert float(mean) == exact_expected_disjoint_pairs_closed_form(m, b)


def test_two_layer_negative_mean_counterexample_is_repaired():
    record = verify_multi_layer_sieve_coherence_and_controls(1, [2, 2], 2)
    assert record["layers"][0]["expected_output_pairs_M"] == 0.5
    assert record["final_expected_pairs"] == 0
    assert record["layers"][1]["output_pool_distribution"] == [
        {"pairs": 0, "probability": {"numerator": "1", "denominator": "1", "float": 1.0}}]
    assert record["v1_mean_closure_retracted"]


def test_multilayer_joint_assignment_enumeration_not_mean_closure():
    # Each path has a different number of second-round assignments.
    exact = Counter()
    m, b1, b2 = 6, 3, 2
    for first in itertools.product(range(b1), repeat=m):
        count = sum(v // 2 for v in Counter(first).values())
        for second in itertools.product(range(b2), repeat=count):
            output = sum(v // 2 for v in Counter(second).values())
            exact[output] += Fraction(1, b1 ** m * b2 ** count)
    record = verify_multi_layer_sieve_coherence_and_controls(0.8, [b1, b2], m)
    saved = {r["pairs"]: Fraction(int(r["probability"]["numerator"]), int(r["probability"]["denominator"]))
             for r in record["layers"][-1]["output_pool_distribution"]}
    assert saved == exact
    assert sum(saved.values()) == 1


def test_surviving_pool_obeys_source_capacity_and_extinction():
    record = verify_multi_layer_sieve_coherence_and_controls(0.8, [8] * 9, 256)
    for depth, layer in enumerate(record["layers"], 1):
        assert 0 <= layer["expected_output_pairs_M"] <= layer["input_pool_M"] / 2
        assert max(r["pairs"] for r in layer["output_pool_distribution"]) <= 256 // 2 ** depth
    assert record["final_expected_pairs"] == 0
    assert not record["actual_DCP_output_headers_proved_IID"]


def test_correlated_noise_can_cancel_and_is_not_covered_by_squaring():
    phi = 0.7
    marginal_gamma = math.cos(phi)
    # Both wires have the SAME random +/-phi error. Their difference is zero.
    actual_difference_gamma = sum(math.cos(e - e) for e in (phi, -phi)) / 2
    assert actual_difference_gamma == 1
    assert marginal_gamma ** 2 < actual_difference_gamma


@pytest.mark.parametrize("m,b", [(-1, 2), (1.5, 2), (2, 0), (True, 2), (2, True), (513, 2)])
def test_invalid_or_unsupported_occupancy_is_not_silently_interpolated(m, b):
    with pytest.raises(ValueError):
        disjoint_pair_count_law(m, b)


def test_bucket_pairing_yield_identity_exhaustive() -> None:
    res = verify_bucket_pairing_yield_identity_exhaustive(m_balls=5, b_buckets=3)
    assert res["exact_identity_verified"] is True


def test_multi_layer_sieve_coherence_and_controls() -> None:
    noisy = verify_multi_layer_sieve_coherence_and_controls(
        gamma_0=0.8, bucket_sizes=[8, 8, 8, 8], initial_pool_m0=256
    )
    assert noisy["coherence_squaring_exact"] is True

    clean = verify_multi_layer_sieve_coherence_and_controls(
        gamma_0=1.0, bucket_sizes=[4], initial_pool_m0=16
    )
    assert clean["coherence_squaring_exact"] is True
    assert abs(clean["final_coherence_gamma"] - 1.0) < 1e-12
    assert clean["final_expected_pairs"] > 7.0


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_sieve_bucket_collision_birthday_tradeoff_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_sieve_bucket_collision_birthday_tradeoff_audit.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_sieve_bucket_collision_birthday_tradeoff_audit_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
    assert data["smallCounterexampleMean"] == 0
    expected = verify_multi_layer_sieve_coherence_and_controls(1, [3, 2], 6)
    assert data["sixStateMean"] == pytest.approx(expected["final_expected_pairs"])
