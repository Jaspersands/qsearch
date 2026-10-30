import pytest
from sympy import Matrix, diag, eye, zeros

from completion import (curve_control, integral_completion, lagrangians,
                        local_completion, recover_frobenius_polynomial,
                        spectral_gate, weak_completion_actions)
from product_corners import (alternating_form, gaussian_fixture, matrix_multiply,
                             matrix_star, mod, reference_gram)
from kernel_output import odd_maximal_split, product_actions


def native_frobenius_control():
    return diag(Matrix([[0, 1], [1, 2]]), Matrix([[0, 1], [1, 1]]))


@pytest.fixture(scope="module")
def all_planes():
    return [(plane, local_completion(plane, native_frobenius_control(), 3))
            for plane in lagrangians(3)]


def test_actual_superspecial_jacobian_is_not_only_a_local_matrix():
    control = curve_control()
    assert control["smooth"]
    assert control["cartier_manin"] == [[0, 0], [0, 0]]
    assert control["point_counts_degrees_one_two"] == [6, 26]
    assert control["characteristic_polynomial"] == [25, 0, 0, 0, 1]
    assert not control["supplied_weak_isogeny_constructed"]
    assert not control["geometric_endomorphism_lattice_extracted"]


@pytest.mark.parametrize("ell,expected", [(3, True), (31, True), (43, True), (47, False)])
def test_native_curve_spectral_gate_depends_on_the_original_prime(ell, expected):
    result = spectral_gate([25, 0, 0, 0, 1], 5, ell)
    assert result["all_lagrangians_cyclic_sufficient"] == expected
    assert not result["geometric_input_verified"]
    assert all(f["degree"] == 2 and f["multiplicity"] == 1 for f in result["factors"])


def test_all_lagrangians_complete_but_one_step_can_fail(all_planes):
    assert len(all_planes) == 40
    assert all(result["full_after_two_powers"] for _, result in all_planes)
    failures = [result for _, result in all_planes if result["cyclic_space_ranks"][1] != 4]
    assert len(failures) == 16
    assert all(result["cyclic_space_ranks"] == [2, 3, 4] for result in failures)
    assert all(result["literal_matrix_span_ranks"] == [4, 9, 16] for result in failures)


def test_exact_tensor_span_identity_for_all_forty_planes(all_planes):
    for _, result in all_planes:
        assert result["literal_matrix_span_ranks"] == [r*r for r in result["cyclic_space_ranks"]]


def test_native_frobenius_pairing_and_characteristic_polynomial():
    gamma, form = native_frobenius_control(), alternating_form(2)
    assert mod(gamma.T*form*gamma, 3) == mod(5*form, 3)
    assert [int(c) % 3 for c in gamma.charpoly().all_coeffs()] == [1, 0, 0, 0, 1]


def test_frobenius_polynomial_is_acquired_without_hidden_prime_torsion():
    gamma = Matrix([[0, 0, 0, -5], [0, 0, 1, 0], [1, 0, 0, 0], [0, 5, 0, 0]])
    report = recover_frobenius_polynomial(5, [(r, gamma) for r in (7, 11)])
    assert report["modulus"] == 77 > 60
    assert report["coefficients"] == curve_control()["characteristic_polynomial"]
    assert not report["geometric_input_verified"]
    assert recover_frobenius_polynomial(5, [(7, gamma)])["status"] == "UNKNOWN_INSUFFICIENT_CRT"


def test_large_prime_gate_is_not_a_field_enumeration():
    ell = 2**127-1
    # Actual integral-control characteristic polynomial, not a Frobenius claim.
    result = spectral_gate([169, -130, 50, -10, 1], 13, ell)
    assert result["all_lagrangians_cyclic_sufficient"]
    assert spectral_gate([25, 0, 0, 0, 1], 5, ell)["status"] == "UNKNOWN"


def test_scalar_frobenius_does_not_escape_the_transport_lattice():
    plane = eye(4)[:, [0, 2]]
    result = local_completion(plane, 2*eye(4), 3)
    assert result["cyclic_space_ranks"] == [2]*3
    assert result["literal_matrix_span_ranks"] == [4]*3
    assert not result["full_after_two_powers"]


def test_extension_field_frobenius_can_destroy_the_useful_structure():
    gamma = Matrix([[0, 0, 0, -5], [0, 0, 1, 0], [1, 0, 0, 0], [0, 5, 0, 0]])
    assert gamma**4 == -25*eye(4)
    scalar = gamma**4
    result = local_completion(eye(4)[:, [0, 2]], scalar, 3)
    assert result["literal_matrix_span_ranks"] == [4, 4, 4]
    gate = spectral_gate(list(reversed([int(c) for c in scalar.charpoly().all_coeffs()])), 5**4, 3)
    assert gate["status"] == "UNKNOWN"


def test_repeated_irreducible_factor_has_an_invariant_lagrangian():
    c = Matrix([[0, 2], [1, 0]])
    gamma, gluing = diag(c, c), eye(2)+c
    plane = eye(2).col_join(gluing)
    assert local_completion(plane, gamma, 3)["cyclic_space_ranks"] == [2]*3
    gate = spectral_gate([1, 0, 2, 0, 1], 1, 3)
    assert gate["status"] == "UNKNOWN"
    assert "repeated irreducible factor" in gate["issues"]


def test_distinct_reciprocal_pair_is_not_a_self_reciprocal_factor():
    # Standard [e1,e2,f1,f2] coordinates are permuted to [e1,f1,e2,f2].
    a = Matrix([[0, 6], [1, 0]])
    gamma = diag(a, mod(5*a.inv_mod(7).T, 7))
    permutation = eye(4)[:, [0, 2, 1, 3]]
    gamma = permutation.T*gamma*permutation
    plane = eye(4)[:, [0, 2]]
    assert local_completion(plane, gamma, 7)["cyclic_space_ranks"] == [2]*3
    gate = spectral_gate([4, 0, 5, 0, 1], 5, 7)
    assert gate["status"] == "UNKNOWN"
    assert "reciprocally paired distinct factors" in gate["issues"]


def test_self_adjoint_quadratic_map_cannot_gain_from_more_powers():
    a = Matrix([[0, 2], [1, 0]])
    permutation = eye(4)[:, [0, 2, 1, 3]]
    gamma = permutation.T*diag(a, a.T)*permutation
    form = alternating_form(2)
    assert form.inv()*gamma.T*form == gamma
    assert gamma**2 == 2*eye(4)
    result = local_completion(eye(4)[:, [0, 2]], gamma, 3)
    assert result["cyclic_space_ranks"] == [2, 2, 2]
    assert result["literal_matrix_span_ranks"] == [4, 4, 4]
    assert spectral_gate([4, 0, -4, 0, 1], 2, 3)["status"] == "UNKNOWN"


@pytest.mark.parametrize("p,parameters", [(7, (3, 1, 1)), (11, (3, 3, 1))])
def test_integral_order_not_just_full_modular_rank(p, parameters):
    order, phi = gaussian_fixture(p, *parameters)
    gamma = Matrix.vstack(Matrix([3, 2, 0, 0]), zeros(4, 1), zeros(4, 1), Matrix([2, 3, 0, 0]))
    unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, matrix_star(order, gamma), gamma) == 13*unit
    completed = integral_completion(order, phi, gamma)
    assert completed == eye(16)
    assert (completed.T*reference_gram(order)*completed).det() == p**8


def test_weak_action_interface_cancels_mask_and_matches_integral_maps():
    order, phi = gaussian_fixture(7, 3, 1, 1)
    gamma = Matrix.vstack(Matrix([3, 2, 0, 0]), zeros(4, 1), zeros(4, 1), Matrix([2, 3, 0, 0]))
    r, ell = 17, 11
    actions = product_actions(odd_maximal_split(7, r))
    evaluate = lambda coordinates: mod(sum((coordinates[i]*actions[i] for i in range(16)), zeros(4)), r)
    phi_matrix, gamma_matrix = evaluate(phi), evaluate(gamma)
    expected = weak_completion_actions(actions, phi_matrix, gamma_matrix, ell, r, 13)
    assert expected == weak_completion_actions(actions, 7*phi_matrix, gamma_matrix, ell, r, 13)
    independent_masks = phi_matrix*diag(1, 2, 3, 4)
    assert expected != weak_completion_actions(actions, independent_masks, gamma_matrix, ell, r, 13)
    # All 144 matrices, including both adjoints, must match the same real maps.
    unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    powers = [unit]
    for _ in range(2):
        powers.append(matrix_multiply(order, powers[-1], gamma))
    at = 0
    for a in range(16):
        transported = matrix_multiply(order, matrix_multiply(order, phi, eye(16)[:, a]), matrix_star(order, phi))
        for left in powers:
            for right in powers:
                actual = matrix_multiply(order, matrix_multiply(order, left, transported), matrix_star(order, right))
                assert expected[at] == evaluate(actual)
                at += 1
    assert at == 144


def test_auxiliary_map_must_respect_the_polarization():
    actions = product_actions(odd_maximal_split(7, 17))
    with pytest.raises(ValueError, match="polarized"):
        weak_completion_actions(actions, eye(4), eye(4), 11, 17, 13)


@pytest.mark.parametrize("coefficients,multiplier,ell", [([1, 0, 1], 1, 3),
    ([25, 0, 0, 0, 1], 5, 5), ([1, 0, 0, 0, 1], 5, 7), ([25, 0, 0, 0, 1], 5, 9)])
def test_invalid_spectral_inputs_rejected(coefficients, multiplier, ell):
    with pytest.raises(ValueError):
        spectral_gate(coefficients, multiplier, ell)


def test_control_cap_and_bad_plane_rejected():
    with pytest.raises(ValueError, match="cap"):
        list(lagrangians(31))
    with pytest.raises(ValueError, match="Lagrangian"):
        local_completion(eye(4)[:, :2], eye(4), 3)


def test_bad_auxiliary_records_not_promoted_to_characteristic_polynomial():
    with pytest.raises(ValueError):
        recover_frobenius_polynomial(5, [(7, eye(4))])
    gamma = Matrix([[0, 0, 0, -5], [0, 0, 1, 0], [1, 0, 0, 0], [0, 5, 0, 0]])
    with pytest.raises(ValueError, match="distinct"):
        recover_frobenius_polynomial(5, [(7, gamma), (7, gamma)])
