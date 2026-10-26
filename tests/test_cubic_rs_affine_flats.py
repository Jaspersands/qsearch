"""Native cubic/RS witnesses and explicitly scoped finite-flat guarantees."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import random

import pytest

from theorems.cubic_rs_affine_flats import (
    REPORT, Cubic, affine_flat_count, element, encoded, field, find_flat,
    flat_absence_bound, flat_points, from_specification, instance_spec,
    monomials, multiply_binary, rank_bound, restricted_system, run_case,
    solve_binary, verify_witness,
)
from theorems.parity_block_usd_prange import affine_system


def test_uniform_ANF_order_and_fast_evaluation_match_independent_monomials():
    assert monomials(3) == (0, 1, 2, 4, 3, 5, 6, 7)
    for coefficients in range(256):
        polynomial = Cubic(3, coefficients)
        assert [polynomial.evaluate(x) for x in range(8)] == [
            polynomial.direct(x) for x in range(8)]
    rng = random.Random(71)
    for bits in (5, 16, 32):
        p = Cubic(bits, rng.getrandbits(len(monomials(bits))))
        for _ in range(16):
            word = rng.getrandbits(bits)
            assert p.evaluate(word) == p.direct(word)


def test_all_flat_points_are_accepted_and_directions_independent():
    _, polynomials = instance_spec(8, 7, 29)
    for i, p in enumerate(polynomials[:8]):
        flat = find_flat(p, 3, 4096, random.Random(2900+i))
        assert flat["status"] == "ACCEPTED_FLAT"
        points = flat_points(flat["origin"], flat["directions"])
        assert len(set(points)) == 8
        assert all(p.direct(point) == 0 for point in points)
        assert sum(flat["work"]["stage_attempts"]) == flat["work"]["random_words"]
        assert flat["work"]["point_evaluations"] >= 8


def test_capped_search_never_turns_failure_into_hardness_or_resamples_input():
    flat = find_flat(Cubic(5, 1), 3, 4, random.Random(7))
    assert flat["status"] == "UNKNOWN_FLAT_BUDGET"
    assert flat["origin"] is None
    assert flat["work"]["point_evaluations"] == 4
    case = run_case(5, 3, 4, 29, attempts=1)
    assert case["status"] == "UNKNOWN_FLAT_BUDGET"
    assert case["attempted_input_instances"] == 1
    assert case["local_flat_searches"] == 25
    assert case["flat_failures"]
    assert case["native_witness_hex"] is None
    assert case["specification"]["input_resampled"] is False
    assert case["original_system_unsatisfiable_claimed"] is False


def test_packed_elimination_matches_FLINT_including_zero_and_inconsistent_rows():
    rng = random.Random(97)
    for width in range(1, 10):
        for _ in range(10):
            equations = tuple((rng.getrandbits(width), rng.randrange(2))
                              for _ in range(rng.randrange(18)))
            got, expected = solve_binary(equations, width), affine_system(equations, width)
            assert got["rank"] == expected["rank"]
            assert got["consistent"] == expected["consistent"]
            if got["consistent"]:
                assert all((mask & got["solution"]).bit_count() % 2 == rhs
                           for mask, rhs in equations)
            else:
                assert got["solution"] is None


@pytest.mark.parametrize("bits", [5, 16, 32])
def test_verifier_field_multiplication_is_independent_and_matches_FLINT(bits):
    rng = random.Random(bits)
    modulus = sum(int(c) << j for j, c in enumerate(field(bits).modulus().coeffs()))
    for _ in range(32):
        a, b = rng.getrandbits(bits), rng.getrandbits(bits)
        assert multiply_binary(a, b, modulus, bits) == encoded(element(bits, a)*element(bits, b))


def test_restricted_binary_rows_equal_the_native_RS_map_for_every_small_word():
    flats = [{"origin": 3, "directions": [1, 4]},
             {"origin": 7, "directions": [2, 8]}]
    points = [1, 3]
    equations, width = restricted_system(5, 2, points, flats)
    assert width == 4
    modulus = sum(int(c) << j for j, c in enumerate(field(5).modulus().coeffs()))
    for word in range(16):
        values = [3 ^ (1 if word & 1 else 0) ^ (4 if word & 2 else 0),
                  7 ^ (2 if word & 4 else 0) ^ (8 if word & 8 else 0)]
        actual = verify_witness([Cubic(5, 0)]*2, points, 2, values, modulus)
        predicted = [sum((((mask & word).bit_count() % 2) ^ rhs) << b
                         for b, (mask, rhs) in enumerate(equations[j*5:(j+1)*5]))
                     for j in range(2)]
        assert [int(x, 16) for x in actual["field_syndromes_hex"]] == predicted


def test_MDS_rank_bound_dominates_exhaustive_small_direction_laws():
    # All local one-dimensional spaces over F2^2, three distinct RS points.
    deficient = 0
    for directions in product(range(1, 4), repeat=3):
        flats = [{"origin": 0, "directions": [v]} for v in directions]
        equations, width = restricted_system(2, 1, [0, 1, 2], flats)
        deficient += solve_binary(equations, width)["rank"] < 2
    assert deficient == 3
    bound = rank_bound(2, 3, 1, 1)
    assert Fraction(deficient, 27) <= Fraction(2)**bound["rank_failure_upper_power_two_exponent"]
    assert bound["rank_failure_upper_power_two_exponent"] == -1


def test_MDS_nullvector_first_moment_matches_exact_RS_root_enumeration():
    bits, q, blocks, checks, dimension = 3, 8, 7, 3, 2
    p0 = Fraction((1 << (bits-dimension))-1, q-1)
    observed = Fraction(0)
    for coefficients in product(range(q), repeat=checks):
        if not any(coefficients):
            continue
        zeros = 0
        for point in range(1, blocks+1):
            a, value = element(bits, point), field(bits).zero()
            for coefficient in reversed(coefficients):
                value = value*a+element(bits, coefficient)
            zeros += value.is_zero()
        observed += p0**(blocks-zeros)
    formula = sum(Fraction(comb(blocks, s))*p0**(blocks-s)*(1-p0)**s*(q**(checks-s)-1)
                  for s in range(checks))
    assert observed == formula
    assert observed <= Fraction(2)**(bits*checks-blocks*dimension)


def test_exact_flat_first_moment_and_scoped_asymptotic_obstruction():
    assert affine_flat_count(3, 0) == 8
    assert affine_flat_count(3, 1) == 28
    assert affine_flat_count(3, 2) == 14
    assert affine_flat_count(3, 3) == 1
    # Over all 256 Boolean cubic functions, each 2-flat is zero 1/16 of the time.
    all_flats = {frozenset(flat_points(a, (u, v))) for a in range(8)
                 for u in range(1, 8) for v in range(1, 8) if u != v}
    count = sum(all(Cubic(3, c).direct(x) == 0 for x in flat)
                for c in range(256) for flat in all_flats)
    assert Fraction(count, 256) == Fraction(14, 16)
    assert flat_absence_bound(32, 4)["unclipped_first_moment_power_two_exponent"] > 0
    assert flat_absence_bound(352, 44)["probability_any_accepted_flat_upper_power_two_exponent"] < -300
    assert flat_absence_bound(352, 44)["rules_out_all_classical_algorithms"] is False


def test_native_witness_checker_rejects_an_actual_constraint_violation():
    spec, p = instance_spec(5, 3, 29)
    modulus = sum(c << j for j, c in enumerate(spec["field_modulus_coefficients"]))
    words = [0]*25
    words[0] = 1
    check = verify_witness(p, spec["points"], 3, words, modulus)
    assert not check["valid"]
    assert check["field_syndromes_hex"][0] == "0x1"
    with pytest.raises(ValueError, match="complete"):
        verify_witness(p, spec["points"], 3, words[:-1], modulus)
    spec["field_modulus_coefficients"][0] ^= 1
    with pytest.raises(ValueError, match="basis changed"):
        from_specification(spec)


@pytest.mark.parametrize("bad", [True, 3.0, -1, 1 << 20])
def test_malformed_packed_coefficients_are_not_silent_family_changes(bad):
    with pytest.raises(ValueError):
        Cubic(3, bad)


def test_live_artifact_native_witnesses_not_an_asymptotic_speedup_claim():
    artifact = json.loads(REPORT.read_text())
    assert artifact["source_sha256"] == hashlib.sha256(Path("theorems/cubic_rs_affine_flats.py").read_bytes()).hexdigest()
    for name, digest in artifact["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not artifact["classical_hardness_conjecture_refuted"]
    assert not artifact["central_speedup_candidate_admitted"]
    assert not artifact["quantum_algorithm_executed"]
    assert len(artifact["cases"]) == 2
    for case in artifact["cases"]:
        spec = case["specification"]
        regenerated, _ = instance_spec(spec["bits"], spec["checks"], spec["input_seed"])
        assert regenerated == spec
        polynomials = from_specification(spec)
        assert spec["checks"]*128 == spec["blocks"]*15
        assert spec["blocks"] == spec["bits"]**2
        assert not spec["input_resampled"] and not spec["planted_witness"]
        assert case["status"] == "NATIVE_CLASSICAL_WITNESS"
        assert case["restricted_linear_solve"]["full_row_rank"]
        assert not case["flat_failures"]
        for p, flat in zip(polynomials, case["flats"]):
            points = flat_points(flat["origin"], flat["directions"])
            assert len(set(points)) == 1 << case["flat_dimension"]
            assert all(p.direct(x) == 0 for x in points)
        witness = [int(x, 16) for x in case["native_witness_hex"]]
        modulus = sum(c << j for j, c in enumerate(spec["field_modulus_coefficients"]))
        assert verify_witness(polynomials, spec["points"], spec["checks"], witness, modulus) == case["verification"]
        assert case["verification"]["valid"]
