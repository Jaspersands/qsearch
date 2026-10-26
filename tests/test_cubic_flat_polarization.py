"""Polar tensor identities, extension iff tests, and native witness replays."""
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random

from theorems.cubic_flat_polarization import (
    REPORT, FLAT_REPORT, Cubic, find_polar_flat, flat_points, from_specification,
    finite_success_bound, local_density_bound, monomials, null_basis,
    polar_mask, sample_span, verify_witness,
)
from theorems.cubic_rs_affine_flats import find_flat


def derivative(polynomial, origin, directions):
    return sum(polynomial.direct(x) for x in flat_points(origin, directions)) & 1


def test_contraction_equals_third_derivative_including_translations():
    rng = random.Random(31)
    # Test every individual cubic coefficient as well as mixtures/lower terms.
    polynomials = [Cubic(5, 1 << i) for i in range(len(monomials(5)))]
    polynomials += [Cubic(5, rng.getrandbits(len(monomials(5)))) for _ in range(20)]
    for polynomial in polynomials:
        for _ in range(20):
            a, u, v, w = [rng.randrange(32) for _ in range(4)]
            mask = polar_mask(polynomial, u, v)
            assert (mask & w).bit_count() % 2 == derivative(polynomial, a, (u, v, w))
            assert mask == polar_mask(polynomial, v, u)
            assert polar_mask(polynomial, u, u) == 0
            assert (mask & u).bit_count() % 2 == 0
            assert (mask & v).bit_count() % 2 == 0


def test_linear_kernel_plus_k_plus_one_checks_is_iff_full_extension():
    rng = random.Random(73)
    dimensions = set()
    for _ in range(20):
        p = Cubic(6, rng.getrandbits(len(monomials(6))))
        flat = find_flat(p, 3, 4096, rng)
        # Greedy search can get stuck at small n; its partial flat is still valid.
        assert flat["origin"] is not None
        origin, directions = flat["origin"], flat["directions"]
        dimensions.add(len(directions))
        assert all(p.direct(x) == 0 for x in flat_points(origin, directions))
        rows = [polar_mask(p, u, v) for u, v in combinations(directions, 2)]
        for word in range(64):
            predicted = all((row & word).bit_count() % 2 == 0 for row in rows)
            predicted &= all(p.evaluate(origin ^ word ^ u) == 0 for u in (0, *directions))
            actual = all(p.direct(x ^ word) == 0 for x in flat_points(origin, directions))
            assert predicted == actual
    assert 3 in dimensions


def test_null_space_basis_is_complete_and_span_sampler_has_no_outside_outputs():
    rows = (0b101101, 0b011010, 0b110111)
    basis, rank = null_basis(rows, 6)
    values = flat_points(0, basis)
    assert len(set(values)) == 2**(6-rank)
    assert set(values) == {x for x in range(64) if all((x&r).bit_count() % 2 == 0 for r in rows)}
    rng = random.Random(71)
    assert all(sample_span(basis, rng) in values for _ in range(100))


def test_polar_search_returns_only_independent_exact_zero_flats():
    rng = random.Random(83)
    statuses = set()
    for _ in range(10):
        p = Cubic(8, rng.getrandbits(len(monomials(8))))
        flat = find_polar_flat(p, 3, 4096, rng)
        statuses.add(flat["status"])
        assert flat["origin"] is not None
        points = flat_points(flat["origin"], flat["directions"])
        assert len(set(points)) == 1 << len(flat["directions"])
        assert all(p.direct(x) == 0 for x in points)
        assert flat["work"]["polar_contractions"] == 1
        assert flat["work"]["linear_systems"] == 3
    assert statuses == {"ACCEPTED_FLAT", "UNKNOWN_FLAT_BUDGET"}


def test_failures_are_retained_not_certificates_of_original_unsatisfiability():
    flat = find_polar_flat(Cubic(8, 1), 3, 5, random.Random(71))
    assert flat["status"] == "UNKNOWN_FLAT_BUDGET"
    assert flat["work"]["point_evaluations"] == 5
    # x0*x1*x2 cannot vanish on a three-dimensional flat of F2^3.
    flat = find_polar_flat(Cubic(3, 1 << 7), 3, 4096, random.Random(71))
    assert flat["status"] == "THIS_FLAT_HAS_NO_POLAR_EXTENSION"
    assert flat["work"]["stages"][-1]["kernel_dimension"] == 2
    assert len(flat["directions"]) == 2


def test_minimum_weight_extension_bound_is_valid_on_enumerated_kernels():
    rng = random.Random(111)
    for _ in range(6):
        p = Cubic(9, rng.getrandbits(len(monomials(9))))
        flat = find_polar_flat(p, 1, 4096, rng)
        assert flat["status"] == "ACCEPTED_FLAT"
        origin, u = flat["origin"], flat["directions"][0]
        good = sum(p.direct(origin ^ w) == 0 and p.direct(origin ^ w ^ u) == 0
                   for w in range(512) if w not in (0, u))
        assert Fraction(good, 512) >= local_density_bound(9, 1, 9)


def test_finite_success_bound_charges_all_failures_without_asymptotic_claim():
    small = finite_success_bound(16, 256, 30, 3, 4096)
    native = finite_success_bound(32, 1024, 120, 4, 4096)
    assert small["certified_success_lower_rounded_down"] == "999/1000"
    assert native["certified_success_lower_rounded_down"] == "499/1000"
    assert native["stage_failure_upper_negative_power_two_exponents"] == [731, 731, 182, 45, 11]
    assert native["constant_one_input_probability_per_block"] == "2^-5489"
    assert not native["probability_assertion_for_the_recorded_PRNG_seed"]
    assert not native["asymptotic_polynomial_time_claim"]
    insufficient = finite_success_bound(64, 4096, 480, 8, 4096)
    assert insufficient["certified_success_lower_rounded_down"] == "0"


def test_saved_native_witnesses_and_larger_local_controls_keep_distinct_scope():
    report = json.loads(REPORT.read_text())
    original = json.loads(FLAT_REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/cubic_flat_polarization.py").read_bytes()).hexdigest()
    assert report["input_report_sha256"] == hashlib.sha256(FLAT_REPORT.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    for case, previous in zip(report["native_cases"], original["cases"]):
        spec = previous["specification"]
        assert case["original_input_sha256"] == hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
        polynomials = from_specification(spec)
        assert case["status"] == "NATIVE_CLASSICAL_WITNESS"
        assert not case["flat_failures"]
        assert not case["input_resampled"]
        assert Fraction(case["finite_success_bound"]["certified_success_lower_rounded_down"]) >= Fraction(499, 1000)
        assert case["restricted_linear_solve"]["rank"] == spec["bits"]*spec["checks"]
        for p, flat in zip(polynomials, case["flats"]):
            points = flat_points(flat["origin"], flat["directions"])
            assert len(set(points)) == 1 << case["flat_dimension"]
            assert all(p.direct(x) == 0 for x in points)
        modulus = sum(c << j for j, c in enumerate(spec["field_modulus_coefficients"]))
        witness = [int(x, 16) for x in case["native_witness_hex"]]
        assert verify_witness(polynomials, spec["points"], spec["checks"], witness, modulus) == case["verification"]
    local = report["larger_local_control"]
    assert local["bits"] == 64 and local["blocks_tested"] == 16
    assert not local["flat_failures"]
    assert not local["all_n_squared_blocks_tested"]
    assert not local["global_RS_constraints_solved"]
    assert not local["end_to_end_n64_solver_demonstrated"]
    for row in local["rows"]:
        p = Cubic(64, int(row["polynomial_coefficients_hex"], 16))
        flat = row["flat"]
        points = flat_points(flat["origin"], flat["directions"])
        assert len(set(points)) == 256
        assert all(p.direct(x) == 0 for x in points)
        assert row["all_flat_points_independently_verified"]
    assert not report["classical_hardness_conjecture_refuted"]
    assert not report["asymptotic_polynomial_success_proved"]
