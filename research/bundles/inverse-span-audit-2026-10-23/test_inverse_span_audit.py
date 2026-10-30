from functools import reduce
from operator import xor

import pytest

from inverse_span_audit import (
    BinaryField, boolean_degree, certificate, census, evaluate_linearized,
    independent_indices, span, subspace_polynomial, subspaces,
)


def test_prime_degree_counterexample_is_zero_sum_but_not_a_flat():
    result = certificate()
    assert result["inverse_sum"] == 0
    assert result["inverse_span_rank"] == 7
    assert result["nonzero_scalars_making_all_traces_zero"] == 0
    assert set(result["inverse_trace_values"]) == {0, 1}
    assert result["vectorial_inverse_degree_on_subspace"] == 3
    assert result["scalar_inverse_trace_degree_on_subspace"] > 0


def test_rank_certificate_really_has_seven_independent_inverse_values():
    result = certificate()
    field = BinaryField(7, 131)
    roots = result["independent_inverse_points"]
    values = result["independent_inverse_values"]
    assert len(values) == len(independent_indices(values)) == 7
    assert all(field.multiply(x, y) == 1 for x, y in zip(roots, values))


def test_independent_flint_arithmetic_and_exhaustive_basis_combinations():
    from flint import fmpz_mod_poly_ctx
    ring = fmpz_mod_poly_ctx(2)
    modulus = ring([1, 1, 0, 0, 0, 0, 0, 1])
    result = certificate()
    for x, inverse, trace in zip(result["points"], result["inverse_values"],
                                 result["inverse_trace_values"]):
        polynomial = ring([(x >> j) & 1 for j in range(7)])
        reciprocal = polynomial.inverse_mod(modulus) if x else ring.zero()
        encoded = sum(int(reciprocal[j]) << j for j in range(7))
        assert encoded == inverse
        absolute_trace = ring.zero()
        term = reciprocal
        for _ in range(7):
            absolute_trace += term
            term = (term*term) % modulus
        assert absolute_trace == ring([trace])
    values = result["independent_inverse_values"]
    combinations = {reduce(xor, (v for j, v in enumerate(values) if (mask >> j) & 1), 0)
                    for mask in range(128)}
    assert combinations == set(range(128))


@pytest.mark.parametrize("dimension", [1, 2, 3, 4])
def test_complete_small_rref_enumeration_and_subspace_polynomial(dimension):
    field = BinaryField(5, 37)
    seen = set()
    for basis in subspaces(5, dimension):
        points = frozenset(span(basis))
        assert len(points) == 1 << dimension
        assert points not in seen
        seen.add(points)
        polynomial = subspace_polynomial(field, basis)
        zeros = {x for x in range(32) if evaluate_linearized(field, polynomial, x) == 0}
        assert zeros == points
        inverse_sum = reduce(xor, (field.inverse(x) for x in points), 0)
        assert inverse_sum == field.multiply(polynomial[1], field.inverse(polynomial[0]))
    expected = 1
    numerator, denominator = 1, 1
    for j in range(dimension):
        numerator *= 2**5-2**j
        denominator *= 2**dimension-2**j
    expected = numerator//denominator
    assert len(seen) == expected


def test_frobenius_trace_pairing_is_nondegenerate():
    field = BinaryField(7, 131)
    masks = [sum(field.trace(field.multiply(1 << i, 1 << j)) << j for j in range(7))
             for i in range(7)]
    assert len(independent_indices(masks)) == 7


def test_all_nonzero_rescalings_are_rejected_by_direct_native_predicate():
    field = BinaryField(7, 131)
    points = span((1, 18, 36, 8))
    for scalar in range(1, 128):
        scaled = [field.multiply(field.inverse(scalar), x) for x in points]
        traces = {field.trace(field.inverse(x)) for x in scaled}
        assert traces == {0, 1}


def test_nonzero_annihilators_in_a_positive_control():
    result = certificate(basis=(1, 2))
    assert result["inverse_span_rank"] < 7
    assert result["nonzero_scalars_making_all_traces_zero"] > 0


def test_degree_transform_includes_all_components_not_only_trace():
    assert boolean_degree((0, 1, 1, 0)) == 1
    assert boolean_degree((0, 0, 0, 1)) == 2
    assert boolean_degree((0, 0, 0, 0)) == -1
    assert boolean_degree((0, 2, 4, 7)) == 2


def test_enumeration_is_not_exposed_as_a_large_field_attack():
    with pytest.raises(ValueError, match="finite exhaustive"):
        list(subspaces(17, 4))
    with pytest.raises(ValueError, match="independent"):
        span((1, 2, 3))


def test_complete_seven_bit_census_records_its_scope():
    result = census()
    assert result["subspaces_enumerated"] == 11811
    assert sum(result["zero_sum_by_inverse_span_rank"].values()) > 0
    assert result["zero_sum_by_inverse_span_rank"].get("7", 0) > 0
    assert not result["asymptotic_inference"]
