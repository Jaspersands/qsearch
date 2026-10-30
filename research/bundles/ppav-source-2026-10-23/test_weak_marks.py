from itertools import product

import pytest

from weak_marks import (
    auxiliary_plan, descent_countercontrol, multiply, normalize_pairings, rank_mod,
    repolarization_countercontrol, sign_patterns, transpose,
)


def gram(dimension):
    return tuple(tuple((1 if j == i+1 else -1 if i == j+1 else 0)
                       if i//2 == j//2 else 0 for j in range(dimension))
                 for i in range(dimension))


def reduced(matrix, prime):
    return tuple(tuple(x % prime for x in row) for row in matrix)


@pytest.mark.parametrize("prime", [3, 5, 7, 11, 13, 17, 19, 23])
def test_actual_gaussian_61_isogeny_torsion_action(prime):
    # 6+5i, with i^2=-1, on E^2; its multiplier is 61.
    phi = ((6, -5, 0, 0), (5, 6, 0, 0), (0, 0, 6, -5), (0, 0, 5, 6))
    source = gram(4)
    assert reduced(multiply(multiply(transpose(phi), source), phi), prime) == reduced(
        tuple(tuple(61*x for x in row) for row in source), prime)
    for scalar in range(1, prime):
        weak = tuple(tuple(scalar*x % prime for x in row) for row in phi)
        target = reduced(multiply(multiply(transpose(weak), source), weak), prime)
        result = normalize_pairings(prime, 61, reduced(source, prime), target)
        assert result["scale_square"] == scalar*scalar % prime
        normalized = reduced(tuple(tuple(result["normalizer"]*x for x in row) for row in weak), prime)
        assert normalized in (reduced(phi, prime), reduced(tuple(tuple(-x for x in row) for row in phi), prime))
        assert not result["global_isogeny_certified"]


@pytest.mark.parametrize("levels", range(1, 8))
def test_sign_enumeration_loses_only_global_sign(levels):
    representatives = set(sign_patterns(levels, cap=128))
    assert len(representatives) == 2**(levels-1)
    for signs in product((1, -1), repeat=levels):
        assert tuple(x*signs[0] for x in signs) in representatives


def test_branch_cap_does_not_silently_drop_missing_signs():
    with pytest.raises(ValueError, match="exceeding cap"):
        list(sign_patterns(10, cap=255))


@pytest.mark.parametrize("prime", [2, 9, 61, True])
def test_bad_auxiliary_orders_rejected(prime):
    with pytest.raises(ValueError):
        normalize_pairings(prime, 61, ((0, 1), (1, 0)), ((0, 1), (1, 0)))


def test_nonunit_and_nonsquare_scales_rejected():
    source = reduced(gram(2), 5)
    for target in [((0, 0), (0, 0)), ((0, 2), (3, 0))]:
        with pytest.raises(ValueError):
            normalize_pairings(5, 1, source, target)


def test_per_point_scalars_can_violate_common_pairing_contract():
    source = reduced(gram(4), 7)
    target = ((0, 1, 0, 0), (6, 0, 0, 0), (0, 0, 0, 2), (0, 0, 5, 0))
    with pytest.raises(ValueError, match="common-scalar"):
        normalize_pairings(7, 1, source, target)


def test_pairing_compatibility_is_not_global_morphism_certification():
    # A symplectic matrix always passes this local test; no geometric lift
    # or one-common-isogeny across several prime levels follows from that.
    result = normalize_pairings(7, 1, reduced(gram(4), 7), reduced(gram(4), 7))
    assert result["root_pair"] == (1, 6)
    assert result["global_isogeny_certified"] is False


@pytest.mark.parametrize("multiplier,dimension,characteristic", [(61, 2, 101), (1, 1, 3), (15, 3, 7), (2**127-1, 2, 101), (2**255-19, 2, 101)])
def test_auxiliary_plan_retains_every_required_budget(multiplier, dimension, characteristic):
    plan = auxiliary_plan(multiplier, dimension, characteristic)
    assert plan["interpolation_arity_condition"] and plan["projective_rigidity_condition"]
    assert all(multiplier % r and characteristic % r for r in plan["levels"])
    assert not plan["interpolator_executed"] and not plan["kernel_recovered"]
    prefix = plan["level_product"] // plan["levels"][-1]
    assert prefix <= multiplier or prefix**2 <= plan["projective_rigidity_bound_squared"]


def test_repolarization_is_not_polarized_endomorphism_of_old_model():
    result = repolarization_countercontrol()
    assert result["positive_symmetric_endomorphism"] == ((1, 1), (1, 2))
    assert result["geometric_degree_on_E_squared"] == 1
    assert result["adjoint_product_for_original_polarization"] == ((2, 3), (3, 5))
    assert not result["is_polarized_isogeny_for_original_models"]
    # The off-diagonal 3 is invisible modulo 3, but not modulo 5.
    assert reduced(result["adjoint_product_for_original_polarization"], 3) == ((2, 0), (0, 2))
    assert reduced(result["adjoint_product_for_original_polarization"], 5) != ((1, 0), (0, 1))


@pytest.mark.parametrize("matrix", [(), ((0,),), ((0, 1),), ((1, 1), (4, 0)), ((0, 5), (0, 0))])
def test_malformed_pairings_rejected(matrix):
    with pytest.raises(ValueError):
        normalize_pairings(5, 1, matrix, matrix)


def test_rank_handles_a_needed_pivot_exchange():
    assert rank_mod(((0, 1), (1, 0)), 5) == 2


def test_too_short_descent_marks_give_a_real_false_positive():
    result = descent_countercontrol()
    assert result["conjugate_numerator"] == (
        (0, 0, 11, -60), (0, 0, 60, 11),
        (11, 60, 0, 0), (-60, 11, 0, 0))
    assert result["torsion_action_matches_candidate"]
    assert result["published_interpolation_input_and_uniqueness_bounds_hold"]
    assert not result["true_conjugate_integral"]
    assert not result["descent_rigidity_bound_holds"]
    assert not result["geometric_interpolator_executed"]


def test_descent_countercontrol_has_exact_multiplier_and_norm():
    result = descent_countercontrol()
    numerator = result["conjugate_numerator"]
    assert multiply(transpose(numerator), numerator) == tuple(
        tuple(61**2 if i == j else 0 for j in range(4)) for i in range(4))
    swap = result["candidate_integral_endomorphism"]
    difference = tuple(tuple(61*a-b for a, b in zip(row_a, row_b))
                       for row_a, row_b in zip(swap, numerator))
    assert all(x % 5 == 0 for row in difference for x in row)
    assert any(x for row in difference for x in row)
    norm_squared = sum(x*x for row in difference for x in row)
    assert norm_squared == 24400
    assert 25 <= norm_squared <= 8*2*61**2
