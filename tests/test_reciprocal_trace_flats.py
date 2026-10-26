from fractions import Fraction
import hashlib
from itertools import product
import json
from random import Random

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.cubic_rs_affine_flats import flat_points
from theorems.reciprocal_trace_flats import (
    REPORT, ROOT, construct_flat, local_flat_budget, solve_with_flats, verify_native_independently,
)


@pytest.mark.parametrize("bits,dimension", [(3, 1), (5, 1), (17, 3), (31, 4), (61, 5)])
@pytest.mark.parametrize("target", [0, 1])
def test_every_point_in_constructed_native_flat_is_verified(bits, dimension, target):
    result = construct_flat(bits, target, dimension, Random(1022+target))
    assert result["status"] == "ACCEPTED_FLAT"
    points = flat_points(result["origin"], result["directions"])
    assert len(set(points)) == 1 << dimension
    assert all(reciprocal_trace(bits, x) == target for x in points)
    assert result["scalar"] != 0


def test_exact_local_union_bound_is_not_a_global_rank_claim():
    row = local_flat_budget(17, 3)
    assert row["bad_translation_union_bound"] == Fraction(777, 1 << 17)
    assert "NOT_GLOBAL" in row["scope"]
    assert local_flat_budget(31, 4)["one_trial_success_lower"] > Fraction(999, 1000)


def test_capped_bad_translation_rng_is_unknown_not_unsatisfiable():
    class ZeroRng:
        def getrandbits(self, bits):
            return 0

    result = construct_flat(17, 1, 3, ZeroRng(), attempts=2)
    assert result == {"status": "UNKNOWN_TRANSLATION_BUDGET", "target": 1, "attempts": 2}


def test_zero_sampled_scalar_uses_an_actual_nonzero_null_vector():
    class ZeroFreeRng:
        def getrandbits(self, bits):
            return 16

        def randrange(self, stop):
            return 0

    flat = construct_flat(5, 0, 1, ZeroFreeRng(), attempts=1)
    assert flat["status"] == "ACCEPTED_FLAT"
    assert flat["scalar"] != 0
    assert all(reciprocal_trace(5, x) == 0 for x in flat_points(flat["origin"], flat["directions"]))


def test_small_global_restrictions_verify_or_report_only_scoped_failure():
    for targets in product((0, 1), repeat=4):
        result = solve_with_flats(3, (0, 1, 2, 3), 1, targets, 1, seed=22)
        assert not result["global_unsatisfiability_claimed"]
        if result["witness"] is not None:
            assert tuple(reciprocal_trace(3, x) for x in result["witness"]) == targets
            assert not any(result["verification"]["field_syndromes"])


def test_bad_local_dimensions_cannot_hide_an_exponential_table():
    for bits, dimension in ((17, 5), (31, 5), (61, 6)):
        with pytest.raises(ValueError, match="dimension"):
            local_flat_budget(bits, dimension)


def test_independent_verifier_rejects_a_corrupted_native_word():
    result = solve_with_flats(5, tuple(range(8)), 1, (0, 1)*4, 2, seed=22)
    assert result["status"] == "VERIFIED_NATIVE_CLASSICAL_WITNESS"
    assert result["verification"]["independent_binary_field_arithmetic"]
    witness = list(result["witness"])
    witness[0] ^= 1
    row = result["input"]
    assert not verify_native_independently(5, row["points"], 1, row["targets"],
                                          witness, row["field_modulus"])["valid"]


def test_global_target_and_point_validation():
    with pytest.raises(ValueError, match="distinct"):
        solve_with_flats(3, (0, 0), 1, (0, 1), 1)
    with pytest.raises(ValueError, match="target"):
        solve_with_flats(3, (0, 1), 1, (True, 0), 1)


def test_live_witnesses_replay_independently_with_bound_source_and_proof():
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/reciprocal_trace_flats.py").read_bytes()).hexdigest()
    assert report["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/RECIPROCAL_TRACE_FLATS.md").read_bytes()).hexdigest()
    assert not report["asymptotic_dequantization"]
    assert [case["input"]["bits"] for case in report["cases"]] == [17, 31]
    for case in report["cases"]:
        row = case["input"]
        assert verify_native_independently(row["bits"], row["points"], row["checks"], row["targets"],
                                           case["witness"], row["field_modulus"])["valid"]
        assert case["linear_system"]["rank"] == case["binary_equations"]
