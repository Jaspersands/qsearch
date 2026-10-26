import hashlib
from itertools import product
import json
from random import Random

import pytest
from flint import fq_default_poly_ctx

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.reciprocal_affine_pencil import (
    REPORT, ROOT, check_root_completeness, identity_family_budget, pencil_word, solve_pencil,
)


def brute_parameters(bits, points, dimension, slopes, offsets, target):
    result = []
    for u in range(1 << bits):
        word = pencil_word(bits, slopes, offsets, u)
        parity = [sum((element(bits, a)**j*element(bits, x) for a, x in zip(points, word)),
                      field(bits).zero()) for j in range(dimension)]
        if all(x == 0 for x in parity) and tuple(reciprocal_trace(bits, x) for x in word) == target:
            result.append(u)
    return result


def check_against_brute(bits, points, dimension, slopes, offsets, target):
    expected = brute_parameters(bits, points, dimension, slopes, offsets, target)
    result = solve_pencil(bits, points, dimension, slopes, offsets, target)
    assert result["solution_parameter_count"] == len(expected)
    assert (result["status"] == "VERIFIED_CLASSICAL_WITNESS") == bool(expected)
    if result["parameters"] is not None:
        assert result["parameters"] == expected
    else:
        system = result["trace_system"]
        described = [u for u in range(1 << bits)
                     if all(sum(c*((u >> j) & 1) for j, c in enumerate(row[:-1])) % 2 == row[-1]
                            for row in system["rref"])]
        assert described == expected
    if expected:
        assert result["parameter"] in expected
        assert tuple(result["witness"]) == pencil_word(bits, slopes, offsets, result["parameter"])
    assert not result["full_native_problem_decided"]
    return result


@pytest.mark.parametrize("bits", [2, 3, 4])
def test_all_targets_of_deterministic_random_pencils_match_exhaustive_search(bits):
    rng = Random(1022+bits)
    q = 1 << bits
    points = tuple(range(4))
    for dimension in (1, 2):
        for _ in range(8):
            slopes = tuple(rng.randrange(q) for _ in points)
            offsets = tuple(rng.randrange(q) for _ in points)
            for target in product((0, 1), repeat=4):
                check_against_brute(bits, points, dimension, slopes, offsets, target)


def test_identity_line_is_complete_including_the_zero_codeword():
    slopes = tuple(encoded(element(3, x)**-1) for x in (1, 2, 4, 7))
    for target in product((0, 1), repeat=4):
        result = check_against_brute(3, (0, 1, 2, 3), 1, slopes, (0,)*4, target)
        if result["trace_system"]["consistent"]:
            assert result["formal_code_identity"]
    result = solve_pencil(3, (0, 1, 2, 3), 1, slopes, (0,)*4, (0,)*4)
    assert result["witness"] == (0,)*4
    assert result["solution_parameter_count"] == 1


def test_exceptional_pole_can_be_the_only_solution_and_gcd_root_is_not_required():
    result = check_against_brute(3, (0, 1, 2), 1, (1, 1, 0), (0, 1, 1), (0, 1, 1))
    assert result["parameters"] == [0]
    assert result["regular_parameters_checked"] == []
    assert result["witness"] == (0, 1, 1)
    assert result["root_completeness_checked"]


def test_repeated_poles_and_constant_zero_coordinates():
    for target in product((0, 1), repeat=4):
        check_against_brute(3, (0, 1, 2, 3), 1, (1, 1, 0, 0), (2, 2, 0, 0), target)


def test_multiple_identity_pole_groups_and_constant_kernel_part():
    result = check_against_brute(3, tuple(range(6)), 1,
                                (1, 1, 2, 2, 0, 0), (0, 0, 1, 1, 1, 1), (0, 0, 1, 1, 1, 1))
    assert result["formal_code_identity"]
    assert result["distinct_poles"] == 2


def test_formal_rational_identity_is_not_inferred_from_finite_field_agreement():
    # Across all F4 points, inversion permutes the field and its sum is zero.
    # The formal rational function has four nonzero residues nonetheless.
    for target in product((0, 1), repeat=4):
        result = check_against_brute(2, tuple(range(4)), 1, (1,)*4, tuple(range(4)), target)
        if result["trace_system"]["consistent"]:
            assert not result["formal_code_identity"]
            assert result["exceptional_parameters_checked"] == list(range(4))


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_large_field_regular_root_uses_polynomial_degree_not_field_enumeration(bits):
    result = solve_pencil(bits, (0, 1), 1, (1, 0), (0, 1), (1, 1))
    assert result["parameters"] == [1]
    assert result["gcd_degree"] == 1
    assert result["parameter_checks"] == 2
    assert not result["field_table_enumerated"]


def test_certifier_rejects_missing_extra_or_duplicate_roots():
    ring = fq_default_poly_ctx(field(3))
    x = ring.gen()
    polynomial = x**2*(x+1)**4
    roots = [element(3, 0), element(3, 1)]
    assert check_root_completeness(polynomial, roots, 3) == x*(x+1)
    for bad in (roots[:1], roots+roots[:1], roots+[element(3, 2)]):
        with pytest.raises(ArithmeticError, match="root list"):
            check_root_completeness(polynomial, bad, 3)
    with pytest.raises(ValueError, match="zero polynomial"):
        check_root_completeness(ring.zero(), [], 3)


def test_constant_pencils_including_a_constant_noncodeword():
    valid = check_against_brute(3, (0, 1), 1, (0, 0), (1, 1), (1, 1))
    assert valid["solution_parameter_count"] == 8
    invalid = check_against_brute(3, (0, 1), 1, (0, 0), (1, 0), (1, 0))
    assert invalid["solution_parameter_count"] == 0
    assert invalid["gcd_degree"] == 0


def test_empty_pencil_does_not_mean_native_instance_is_unsatisfiable():
    target = (1, 0, 1, 0)
    result = solve_pencil(3, (0, 1, 2, 3), 1, (1, 2, 3, 4), (0,)*4, target)
    assert result["trace_system"]["consistent"]
    assert result["solution_parameter_count"] == 0
    # A witness outside this pencil exists for the SAME input.
    witness = (1, 0, 1, 0)
    assert tuple(reciprocal_trace(3, x) for x in witness) == target
    assert sum((element(3, x) for x in witness), field(3).zero()) == 0


@pytest.mark.parametrize("n,gap", [(17, 170), (31, 744), (61, 3294)])
def test_fixed_identity_family_bound_has_explicit_nonadaptive_scope(n, gap):
    row = identity_family_budget(n, n*n, n*n//8)
    assert row["max_nonconstant_groups"] == 7
    assert row["uniform_target_hit_probability_upper_power_of_two"] == -gap
    assert "NOT_ADAPTIVE" in row["scope"]
    assert not row["classical_hardness_established"]


@pytest.mark.parametrize("points,dimension,slopes,offsets,targets", [
    ((0, 0), 1, (1, 1), (0, 0), (0, 0)),
    ((0, 1), 1, (1,), (0, 0), (0, 0)),
    ((0, 1), 2, (1, 1), (0, 0), (0, 0)),
    ((0, 1), 1, (8, 1), (0, 0), (0, 0)),
    ((0, 1), 1, (1, 1), (0, 0), (True, 0)),
])
def test_invalid_inputs_rejected(points, dimension, slopes, offsets, targets):
    with pytest.raises(ValueError):
        solve_pencil(3, points, dimension, slopes, offsets, targets)


def test_live_pencil_certificates_replay_and_bind_to_source_and_proof():
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/reciprocal_affine_pencil.py").read_bytes()).hexdigest()
    assert report["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/RECIPROCAL_AFFINE_PENCIL.md").read_bytes()).hexdigest()
    assert not report["general_classical_solver"]
    for case in report["controls"]:
        inputs = dict(case["input"])
        modulus = inputs.pop("field_modulus")
        replay = solve_pencil(**inputs)
        assert replay["input"]["field_modulus"] == modulus
        assert replay["status"] == case["status"]
        assert replay["solution_parameter_count"] == case["solution_parameter_count"]
