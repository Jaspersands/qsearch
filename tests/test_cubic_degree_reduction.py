"""Exact quadratic reduction, polynomial certificates, and scoped native replays."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import random

import pytest

from theorems.cubic_degree_reduction import (
    MAX_LOCAL_BITS, REPORT, INPUT_REPORT, Cubic, bilinear, certify_zero_flat,
    combine, dimensions, from_specification, local_block_campaign, monomials,
    quadratic_value, quadratic_zero_space, remainder, sample_deterministic_cubic,
    success_bound, verify_witness, zero_flat,
)
from theorems.cubic_rs_affine_flats import flat_points


def test_every_small_quadratic_form_has_the_guaranteed_zero_space():
    width = 4
    pairs = [(i, j) for i in range(width) for j in range(i+1, width)]
    for coefficients in range(1 << len(pairs)):
        rows = [0]*width
        for p, (i, j) in enumerate(pairs):
            bit = (coefficients >> p) & 1
            rows[i] |= bit << j
            rows[j] |= bit << i
        for linear in range(1 << width):
            zero, report = quadratic_zero_space(linear, rows)
            points = flat_points(0, zero)
            assert len(set(points)) == 1 << len(zero)
            assert len(zero) >= (width-1)//2
            assert all(quadratic_value(linear, rows, point) == 0 for point in points)
            assert all(bilinear(rows, u, v) == 0 for u, v in product(zero, repeat=2))
            assert report["polar_rank"] % 2 == 0


def test_alternating_Gram_Schmidt_rejects_wrong_matrix_conventions():
    with pytest.raises(ValueError, match="alternating"):
        quadratic_zero_space(0, [1, 0])
    with pytest.raises(ValueError, match="symmetric"):
        quadratic_zero_space(0, [2, 0])


def test_degree_reduction_threshold_is_exact_and_has_sqrt_scaling():
    for n in range(3, 512):
        lowered, k = dimensions(n)
        assert lowered*(lowered-1)//2 < n
        assert lowered*(lowered+1)//2 >= n
        assert k == (lowered-1)//2
    assert dimensions(32) == (8, 3)
    assert dimensions(64) == (11, 5)
    assert dimensions(96) == (14, 6)
    assert dimensions(128) == (16, 7)
    assert dimensions(1024) == (45, 22)


def test_membership_does_not_enumerate_an_exponential_span():
    echelon = {0: 0b101, 1: 0b110}
    assert all(remainder(x, echelon) == 0 for x in flat_points(0, echelon.values()))
    assert remainder(1, echelon) != 0


def test_low_weight_certificate_detects_a_cubic_missed_by_linear_checks():
    # f=x0*x1*x2 vanishes at 0 and all unit vectors, not on their span.
    polynomial = Cubic(5, 1 << monomials(5).index(0b111))
    assert all(polynomial.direct(x) == 0 for x in (0, 1, 2, 4))
    certificate = certify_zero_flat(polynomial, 0, [1, 2, 4])
    assert not certificate["valid"]
    assert certificate["evaluations"] == 8
    assert not certify_zero_flat(Cubic(5, 0), 0, [1, 1])["valid"]


@pytest.mark.parametrize("bits", [5, 8, 16, 32])
def test_constructor_preserves_full_original_cubic_and_fixed_dimension(bits):
    rng = random.Random(900+bits)
    p = Cubic(bits, rng.getrandbits(len(monomials(bits))))
    flat = zero_flat(p, rng)
    assert flat["status"] == "ACCEPTED_FLAT"
    assert len(flat["directions"]) == dimensions(bits)[1]
    points = flat_points(flat["origin"], flat["directions"])
    assert len(set(points)) == len(points)
    assert all(p.direct(x) == 0 for x in points)
    assert flat["work"]["span_points_enumerated"] == 0
    assert flat["work"]["kernel_draws"] <= flat["target_lowered_dimension"]*2*bits


def test_beyond_64bit_cubic_degree_reduction_and_low_weight_certificate():
    campaign = local_block_campaign(72, 2, 72001, 2_072_001)
    assert campaign["bits"] == 72
    assert campaign["target_lowered_dimension"] == 12
    assert campaign["target_zero_dimension"] == 5
    assert campaign["flat_failures"] == 0
    assert campaign["total_span_points_enumerated"] == 0
    assert not campaign["global_RS_constraints_solved"]
    assert not campaign["asymptotic_result_claimed"]
    for row in campaign["rows"]:
        p = sample_deterministic_cubic(72, 72001, row["block_index"])
        assert hashlib.sha256(hex(p.coefficients).encode()).hexdigest() == row["polynomial_coefficients_sha256"]
        assert certify_zero_flat(p, row["origin"], row["directions"]) == row["certificate"]
        assert row["certificate"]["valid"]
        assert row["certificate"]["evaluations"] == 26


def test_constant_one_and_unlucky_budget_failures_are_visible():
    assert zero_flat(Cubic(8, 1), random.Random(3))["status"] == "CONSTANT_ONE_INPUT"

    class AlwaysZero:
        def getrandbits(self, bits):
            return 0

    flat = zero_flat(Cubic(8, 0), AlwaysZero())
    assert flat["status"] == "UNKNOWN_DIRECTION_BUDGET"
    assert flat["work"]["kernel_draws"] == 16
    assert zero_flat(Cubic(8, 3), AlwaysZero())["status"] == "UNKNOWN_ORIGIN_BUDGET"


def test_success_theorem_changes_rate_and_does_not_claim_fixed_rate_dequantization():
    for n in (16, 32, 64, 128, 1024):
        _, k = dimensions(n)
        bound = success_bound(n, n*n, n*(k-1))
        assert bound["rank_bound"]["slack"] == n*n
        assert bound["failure_upper_power_two_exponent"] < -10
        assert not bound["fixed_positive_check_rate_dequantized"]
        assert not bound["fixed_PRNG_seed_probability_claim"]
    assert success_bound(32, 1024, 120)["failure_upper_power_two_exponent"] == 0


def test_dyadic_rounding_is_conservative_against_exact_small_rationals():
    for n in (16, 32):
        ell, k = dimensions(n)
        m, r = n*n, n*(k-1)
        exact = (m*(Fraction(2)**(-sum(comb(n, j) for j in range(4)))
                    + Fraction(2)**(-8*n)+ell*Fraction(2)**(-2*n))
                 + Fraction(2)**(r*n-m*k))
        bound = success_bound(n, m, r)
        assert exact <= Fraction(2)**bound["failure_upper_power_two_exponent"]


def test_saved_native_results_use_the_changed_check_matrix_and_original_ANFs():
    report = json.loads(REPORT.read_text())
    original = json.loads(INPUT_REPORT.read_text())
    assert report["schema"] == "cubic-degree-reduction-v2"
    assert report["local_degree_reduction_bits_cap"] == MAX_LOCAL_BITS == 256
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/cubic_degree_reduction.py").read_bytes()).hexdigest()
    assert report["input_report_sha256"] == hashlib.sha256(INPUT_REPORT.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    for case, previous in zip(report["native_cases"], original["cases"]):
        spec = previous["specification"]
        assert case["code_constraints_changed"]
        assert case["previous_checks"] == spec["checks"] > case["checks"]
        assert not case["input_resampled"]
        p = from_specification(spec)
        for polynomial, flat in zip(p, case["flats"]):
            assert certify_zero_flat(polynomial, flat["origin"], flat["directions"]) == flat["certificate"]
            assert flat["work"]["span_points_enumerated"] == 0
        assert case["status"] == "NATIVE_CLASSICAL_WITNESS"
        assert case["restricted_linear_solve"]["rank"] == case["bits"]*case["checks"]
        witness = [int(word, 16) for word in case["native_witness_hex"]]
        modulus = sum(c << i for i, c in enumerate(spec["field_modulus_coefficients"]))
        assert verify_witness(p, spec["points"], case["checks"], witness, modulus) == case["verification"]
    assert not report["n64_full_code_constrained_instance_solved"]
    assert not report["paper_fixed_rate_classical_hardness_conjecture_refuted"]
    assert len(report["analytical_scaling_not_empirical_runs"]) == 7
    local_path = Path("research/classical_baselines/cubic_flat_polarization.json")
    assert report["local_input_report_sha256"] == hashlib.sha256(local_path.read_bytes()).hexdigest()
    local_input = json.loads(local_path.read_text())["larger_local_control"]
    assert len(report["n64_local_flats"]) == len(local_input["rows"]) == 16
    for flat, row in zip(report["n64_local_flats"], local_input["rows"]):
        p = Cubic(64, int(row["polynomial_coefficients_hex"], 16))
        assert len(flat["directions"]) == 5
        assert certify_zero_flat(p, flat["origin"], flat["directions"]) == flat["certificate"]
        assert all(p.direct(point) == 0 for point in flat_points(flat["origin"], flat["directions"]))

    expanded = report["n64_expanded_local_campaign"]
    assert expanded["bits"] == 64
    assert expanded["blocks_tested"] == 64
    assert expanded["flat_failures"] == 0
    assert expanded["total_span_points_enumerated"] == 0
    assert not expanded["all_n_squared_blocks_tested"]
    assert not expanded["global_RS_constraints_solved"]
    for row in expanded["rows"][:4]:
        p = sample_deterministic_cubic(64, expanded["input_seed"], row["block_index"])
        assert hashlib.sha256(hex(p.coefficients).encode()).hexdigest() == row["polynomial_coefficients_sha256"]
        assert certify_zero_flat(p, row["origin"], row["directions"]) == row["certificate"]

    beyond = report["beyond_64bit_local_controls"]
    assert [c["bits"] for c in beyond] == [96, 128]
    for control in beyond:
        assert control["flat_failures"] == 0
        assert control["total_span_points_enumerated"] == 0
        assert not control["global_RS_constraints_solved"]
        assert not control["asymptotic_result_claimed"]
        for row in control["rows"]:
            p = sample_deterministic_cubic(control["bits"], control["input_seed"], row["block_index"])
            assert hashlib.sha256(hex(p.coefficients).encode()).hexdigest() == row["polynomial_coefficients_sha256"]
            assert certify_zero_flat(p, row["origin"], row["directions"]) == row["certificate"]
            assert row["certificate"]["valid"]
