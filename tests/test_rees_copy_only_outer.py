"""Physical source-transport falsifiers, not an implemented black-box HSP solver."""
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems.central_character_descent import HeisenbergFixture, controlled_discard
from theorems.rees_hsp_reduction import (
    _units, binary_zero_sum_support, black_box_copy_budget, make_rees_cover,
)
from theorems.right_abelian_induced_source import upper_triangular_lie


D8 = tuple(product(range(4), range(2)))
D8_INDEX = {g: i for i, g in enumerate(D8)}


def _mul(a, b):
    return ((a[0]+(-1)**a[1]*b[0]) % 4, (a[1]+b[1]) % 2)


def _inv(a):
    return ((-(-1)**a[1]*a[0]) % 4, a[1])


def _controls(representatives, *, left=False):
    return np.array([[D8_INDEX[_mul(g, x) if left else _mul(x, _inv(g))]
                      for x in D8] for g in representatives])


def _density(hidden):
    return np.array([[int(_mul(_inv(x), y) in hidden)/8 for y in D8] for x in D8])


def _expected(representatives, hidden):
    return np.array([[int(_mul(_inv(y), x) in hidden)/len(representatives)
                      for y in representatives] for x in representatives])


def test_restriction_consumes_one_copy_without_index_postselection_or_hidden_advice():
    hidden = {(0, 0), (0, 1)}  # A nonnormal reflection subgroup.
    assert _mul(_mul((1, 0), (0, 1)), _inv((1, 0))) not in hidden
    rho = _density(hidden)
    for subgroup in (tuple((r, 0) for r in range(4)), tuple(hidden)):
        # Operational channel receives rho and PUBLIC actions only, not H.
        out = controlled_discard(rho, _controls(subgroup))
        np.testing.assert_allclose(out, _expected(subgroup, hidden), atol=1e-14)
        np.testing.assert_allclose(np.trace(out), 1, atol=1e-14)
    np.testing.assert_allclose(np.diag(rho), np.ones(8)/8)
    wrong = controlled_discard(rho, _controls(tuple(hidden), left=True))
    assert np.linalg.norm(wrong-_expected(tuple(hidden), hidden)) > 0.3


def test_fixed_unknown_coset_pure_inputs_also_have_the_same_restriction_kernel():
    hidden = {(0, 0), (0, 1)}
    representatives = ((0, 0), (0, 1))
    for a in D8:
        ket = np.zeros(8)
        for h in hidden:
            ket[D8_INDEX[_mul(a, h)]] = 1/np.sqrt(2)
        out = controlled_discard(np.outer(ket, ket), _controls(representatives))
        np.testing.assert_allclose(out, _expected(representatives, hidden), atol=1e-14)


def test_nonhomomorphic_quotient_sections_and_flattened_nested_restriction():
    hidden = {(0, 0), (2, 0), (0, 1), (2, 1)}
    # K=<r^2> is central and contained in H. G/K=F_2^2.
    representatives = tuple(product(range(2), range(2)))
    assert _mul((1, 0), (1, 0)) == (2, 0) != representatives[0]
    actual = controlled_discard(_density(hidden), _controls(representatives))
    expected = _expected(representatives, hidden)
    np.testing.assert_allclose(actual, expected, atol=1e-14)
    changed = tuple(_mul((2, 0), g) if i % 2 else g
                    for i, g in enumerate(representatives))
    np.testing.assert_allclose(controlled_discard(_density(hidden), _controls(changed)),
                               expected, atol=1e-14)
    # Restrict to the second F_2 coordinate after quotienting; compare a
    # direct original-group representative circuit using ONE original copy.
    qindex = {q: i for i, q in enumerate(representatives)}
    subgroup = ((0, 0), (0, 1))
    qcontrols = np.array([[qindex[((x[0]+g[0]) % 2, (x[1]+g[1]) % 2)]
                          for x in representatives] for g in subgroup])
    nested = controlled_discard(actual, qcontrols)
    flattened = controlled_discard(_density(hidden), _controls(subgroup))
    np.testing.assert_allclose(nested, flattened, atol=1e-14)


def test_quotient_without_known_kernel_inside_hidden_subgroup_is_invalid():
    hidden = {(0, 0), (0, 1)}  # K=<r^2> is NOT contained in this H.
    first = ((0, 0), (0, 1), (1, 0), (1, 1))
    second = ((0, 0), (2, 1), (1, 0), (1, 1))
    a = controlled_discard(_density(hidden), _controls(first))
    b = controlled_discard(_density(hidden), _controls(second))
    assert np.linalg.norm(a-b) > 0.3  # Illegitimate representative dependence.


@pytest.mark.parametrize("hidden", [{(0, 0)}, {(0, 0), (0, 1)},
                                     {(0, 0), (2, 0), (0, 1), (2, 1)}])
def test_small_prime_zero_sum_descent_on_d8_without_lazard_or_source_inverse(hidden):
    # Class 2, characteristic 2, exponent 4: outside the Rees Lazard input.
    rho = _density(hidden)
    zperm = _controls(((2, 0),))[0]
    central = np.eye(8)[np.argsort(zperm)]
    branches = []
    for label in range(2):
        projector = (np.eye(8)+(-1)**label*central)/2
        branch = projector @ rho @ projector
        mass = np.trace(branch).real
        branches.append((mass, branch/mass if mass else None))
    representatives = tuple(product(range(2), range(2)))
    hz = {_mul(h, z) for h in hidden for z in ((0, 0), (2, 0))}
    expected = _expected(representatives, hz)
    total_mass = 0.0
    for labels in product(range(2), repeat=2):
        mass = branches[labels[0]][0]*branches[labels[1]][0]
        if not mass:
            continue
        weights = (1, 0) if labels[0] == 0 else (0, 1) if labels[1] == 0 else (1, 1)
        active = binary_zero_sum_support(2, tuple((x,) for x in labels), weights)
        kernel = np.ones((4, 4), dtype=complex)
        for i in active:
            kernel *= 4*controlled_discard(branches[labels[i]][1], _controls(representatives))
        np.testing.assert_allclose(kernel/4, expected, atol=1e-14)
        total_mass += mass
    np.testing.assert_allclose(total_mass, 1, atol=1e-14)


@pytest.mark.parametrize("kind", ["line", "center", "whole"])
def test_rees_lift_from_fresh_mixed_coset_copies_needs_no_moment_design(kind):
    group = HeisenbergFixture(3)
    source, _ = upper_triangular_lie(3, 3)
    cover = make_rees_cover(source, _units(3))
    hidden = ({(t, 0, 0) for t in range(3)} if kind == "line" else
              {(0, 0, t) for t in range(3)} if kind == "center" else set(group.elements))
    rho = group.coset_density_fixture(hidden)
    addresses = tuple(product(range(3), repeat=4))
    def encode(v):
        x, z, y = v
        return x, y, (z+2*x*y) % 3
    kernel = np.ones((81, 81), dtype=complex)
    for s in cover.points:
        controls = np.array([group.right_permutation(encode(cover.evaluate(a, s))) for a in addresses])
        kernel *= 81*controlled_discard(rho, controls)
    expected = np.empty((81, 81))
    for i, a in enumerate(addresses):
        for j, b in enumerate(addresses):
            difference = cover.multiply(tuple(-x % 3 for x in b), a)
            expected[i, j] = all(encode(row) in hidden for row in cover.coefficients(difference))/81
    np.testing.assert_allclose(kernel/81, expected, atol=2e-14)


def test_correct_one_copy_marginals_do_not_allow_correlated_target_banks():
    # G=C2, H={0}: each marginal I/2 is correct, but a Bell bank is not IID.
    controls = np.array([[0, 1], [1, 0]])
    fresh = 2*controlled_discard(np.eye(2)/2, controls)**2
    bell = np.array([1, 0, 0, 1])/np.sqrt(2)
    joint_controls = np.array([[0, 1, 2, 3], [3, 2, 1, 0]])
    correlated = controlled_discard(np.outer(bell, bell), joint_controls)
    np.testing.assert_allclose(fresh, np.eye(2)/2, atol=1e-14)
    np.testing.assert_allclose(correlated, np.ones((2, 2))/2, atol=1e-14)


def test_zero_sum_witness_uses_fermat_support_not_original_linear_weights():
    assert binary_zero_sum_support(3, ((1,),)*3, (1, 2, 1)) == (0, 1, 2)
    assert (1+2+1) % 3 != 0
    assert binary_zero_sum_support(5, ((1,),)*5, (1, 2, 3, 4, 1)) == tuple(range(5))
    assert binary_zero_sum_support(2, ((0, 0), (1, 0)), (1, 0)) == (0,)
    for p, labels, weights in ((4, ((0,),), (1,)), (True, ((0,),), (1,)),
                               (3, ((1,),), (0,)), (3, ((1,),), (1,)),
                               (2, ((0,),), (2,)), (2, ((0,), (0, 0)), (1, 0)),
                               (2, ((True,),), (1,)), (2, ((),), (1,)),
                               (2, ((0,),), (True,)), (2, ((0,),), ())):
        with pytest.raises(ValueError):
            binary_zero_sum_support(p, labels, weights)


def test_all_prime_copy_envelope_charges_both_branches_and_adaptive_error():
    b, c, eps = 7, 3, Fraction(1, 100)
    result = black_box_copy_budget(b, c, eps)
    cap, samples = 56, result["final_fourier_samples_per_call"]
    quadratic_arity, cubic_arity = (2*8**2)**2, (3**3*8**3)**2
    assert result["small_prime_zero_sum_arities"] == ((2, 8), (3, quadratic_arity))
    assert result["large_prime_original_copy_bound"] == cap*3*samples*quadratic_arity*cubic_arity
    assert result["small_prime_original_copy_bound"] == cap*samples*quadratic_arity**2
    assert result["total_original_copy_bound"] == (
        result["large_prime_original_copy_bound"]+result["small_prime_original_copy_bound"])
    assert result["small_prime_copy_dimension_exponent"] == 11
    allocated = (result["preprocessing_error_allocation"]
                 + cap*(result["chart_error_per_large_prime_call"]
                        + result["large_prime_error_per_call"]+result["small_prime_error_per_hsmc_call"]))
    assert allocated == eps == result["total_error_allocation"]
    assert result["local_rank_failure_bound"] <= eps/(12*cap)
    assert result["all_hidden_source_copy_calls_covered"]
    assert result["coherent_public_group_operations_required"]
    for flag in ("ordinary_hiding_function_required", "unknown_source_preparation_inverse_required",
                 "quantum_receiver_implemented", "general_diagonal_solver_implemented",
                 "public_group_operation_count_included", "is_total_gate_bound", "speedup_claim_allowed"):
        assert result[flag] is False


def test_abelian_budget_and_small_prime_exponent_cannot_be_omitted():
    abelian = black_box_copy_budget(2, 1)
    assert abelian["small_primes"] == ()
    assert abelian["small_prime_original_copy_bound"] == 0
    assert abelian["unused_small_prime_error_allocation"] == Fraction(1, 12)
    assert abelian["total_original_copy_bound"] == abelian["large_prime_original_copy_bound"]
    # The small-prime branch can have a worse exponent than the Rees core.
    class8 = black_box_copy_budget(2, 8)
    assert class8["small_prime_copy_dimension_exponent"] == 129
    assert class8["large_prime_copy_dimension_exponent"] == 111
    for b, c, eps in ((0, 2, Fraction(1, 3)), (2, True, Fraction(1, 3)),
                      (2, 2, 0.1), (2, 2, Fraction(1))):
        with pytest.raises(ValueError):
            black_box_copy_budget(b, c, eps)
