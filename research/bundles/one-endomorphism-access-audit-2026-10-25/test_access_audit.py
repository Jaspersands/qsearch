from pathlib import Path
import json
import sys

import pytest
from sympy import Matrix, eye

sys.path.insert(0, str(Path(__file__).resolve().parent))
from access_audit import (
    commutant, frobenius_product_control, gram_nonclosure_control, matrix_algebra,
    odd_maximal_split, projective_centralizer_count, same_degree_ambiguity_control,
    stabilized_controls,
    unbounded_primitive_family_control,
)


@pytest.mark.parametrize("prime", [3, 5, 7, 13, 17])
def test_one_operator_has_a_nonscalar_projective_ambiguity(prime):
    alpha = odd_maximal_split(11, prime)[1]
    assert len(commutant((alpha,), prime)) == 2
    expected = prime-1 if prime % 4 == 1 else prime+1
    assert projective_centralizer_count(alpha, prime) == expected


@pytest.mark.parametrize("prime", [3, 5, 7])
@pytest.mark.parametrize("copies", [1, 2, 3])
def test_stabilization_does_not_complete_the_known_order(prime, copies):
    record = stabilized_controls(prime, copies)
    assert record["generated_algebra_dimension"] == 2*copies*copies
    assert record["commutant_dimension"] == 2


@pytest.mark.parametrize("prime", [3, 5, 7, 13])
def test_natural_frobenius_does_not_add_the_missing_generator(prime):
    record = frobenius_product_control(prime)
    assert record["generated_algebra_dimension"] == 8
    assert not record["actual_curve_backend_executed"]


@pytest.mark.parametrize("prime", [5, 7, 13, 17])
def test_known_equal_degree_does_not_resolve_one_operator_ambiguity(prime):
    assert same_degree_ambiguity_control(prime)["original_degree_three_kernels_distinct"]


def test_gram_allowed_set_is_not_a_group():
    assert not gram_nonclosure_control()["product_gram_in_field"]


@pytest.mark.parametrize("prime", [3, 5, 7])
def test_genuinely_noncommuting_second_operator_completes_local_algebra(prime):
    actions = odd_maximal_split(11, prime)
    generators = (actions[1], actions[2])
    assert len(matrix_algebra(generators, prime)) == 4
    assert len(commutant(generators, prime)) == 1


def test_scalar_input_is_not_mislabeled_quadratic():
    assert len(commutant((eye(2),), 5)) == 4
    with pytest.raises(ValueError, match="nonscalar"):
        projective_centralizer_count(eye(2), 5)


def test_repeated_root_local_case_is_not_assigned_a_torus_count():
    # A nonscalar Jordan block has r projective units, rather than r+-1.
    assert projective_centralizer_count(Matrix([[1, 1], [0, 1]]), 5) == 5


def test_large_prime_enumeration_is_rejected():
    with pytest.raises(ValueError, match="cap"):
        projective_centralizer_count(Matrix([[0, -1], [1, 0]]), 65537)


def test_primitive_maps_of_fixed_quadratic_input_have_unbounded_degree():
    result = unbounded_primitive_family_control()
    assert result["controls"][-1]["degree"] == 3**64
    assert not result["bound_on_every_primitive_intertwiner_from_fixed_input"]
    assert not result["minimal_degree_intertwiner_lower_bound_claim"]


def test_receipt_keeps_negative_scope_and_execution_flags():
    from replay_access_audit import evidence
    record = json.loads(json.dumps(evidence()))
    assert len(record["negative_records"]) == 4
    assert not any(record["scope_flags"].values())
