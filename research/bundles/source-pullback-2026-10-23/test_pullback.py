from dataclasses import replace

import pytest
from sympy import Matrix, eye, zeros

from controls import frobenius_relation_fixture, unit, word_fixture
from pullback import (
    adjoint, column_basis, extract_kernel,
    matrix_multiply, matrix_star, mod, reconstruct_pullbacks, source_gram,
    weak_pullback_actions,
)
from kernel_output import action, alternating_form, product_actions


def recover(source, **overrides):
    arguments = dict(order=source.order, ell=source.ell, characteristic=source.characteristic,
                     norm_bounds=source.norms(), auxiliary_primes=source.levels(),
                     split_at=source.split, observe_at=source.observe, max_auxiliary_prime=47)
    arguments.update(overrides)
    return reconstruct_pullbacks(**arguments)


@pytest.mark.parametrize("factory", [word_fixture] + [lambda k=k: frobenius_relation_fixture(k) for k in range(3)])
def test_actual_crt_reconstruction_without_secret_as_algorithm_input(factory):
    source = factory()
    result = recover(source)
    assert result.coordinates == source.reference_pullbacks()
    assert result.modulus > 2 * result.pairing_bound
    assert tuple(source.calls) == result.primes
    assert result.weak_basis_points_required == 4 * len(result.primes)
    assert result.target_basis_points_required == 4 * len(result.primes)
    assert result.source_basis_points_required == 64 * len(result.primes)
    assert all(r not in (source.ell, source.characteristic) for r in result.primes)
    gram = source_gram(source.order)
    for x, b in zip(result.coordinates, result.trace_pairings):
        assert gram * x == b


@pytest.mark.parametrize("prime", [3, 7, 13, 17])
def test_every_nonzero_mask_cancels_in_compatible_changed_target_frame(prime):
    source = word_fixture()
    packet = source.observe(prime)
    expected = tuple(mod(action(x, product_actions(source.split(prime))), prime)
                     for x in source.reference_pullbacks())
    for scalar in range(1, prime):
        altered = replace(packet, weak_action=scalar * packet.weak_action)
        assert weak_pullback_actions(source.ell, prime, altered) == expected


def test_second_word_layer_recovers_when_first_layer_even_with_adjoints_is_partial():
    source = word_fixture()
    extracted = recover(source)
    result = extract_kernel(source.order, source.ell, source.split(source.ell), extracted.coordinates)
    assert result.rank_history == (1, 2)
    assert result.word_counts == (2, 4)
    assert result.status == "COMPLETE_UNDER_INPUT_PROMISE"
    assert result.assumptions_verified is False
    assert result.remaining_lagrangian_extensions == 1
    phi = action(source.phi, product_actions(source.split(source.ell)))
    assert mod(phi * result.known_subspace, source.ell) == zeros(4, 2)
    assert column_basis(phi, source.ell).cols == 2
    assert mod(result.known_subspace.T * alternating_form(2) * result.known_subspace, source.ell) == zeros(2)

    gamma = source.gammas[0]
    target_alphabet = (gamma, matrix_star(source.order, gamma))
    phi_star = matrix_star(source.order, source.phi)
    for index, a in enumerate(target_alphabet):
        for other, b in enumerate(target_alphabet):
            word = matrix_multiply(source.order, a, b)
            expected = matrix_multiply(source.order, matrix_multiply(source.order, phi_star, word), source.phi)
            assert result.word_coordinates[1][2 * index + other] == expected


@pytest.mark.parametrize("rank", [0, 1, 2])
def test_frobenius_relations_do_not_automatically_recover_kernel(rank):
    source = frobenius_relation_fixture(rank)
    gamma = source.gammas[0]
    identity = unit(source.order)
    assert matrix_multiply(source.order, gamma, gamma) == -7 * identity
    assert matrix_star(source.order, gamma) == -gamma
    assert matrix_multiply(source.order, matrix_star(source.order, source.phi), source.phi) == 11 * identity
    assert matrix_multiply(source.order, source.phi, matrix_star(source.order, source.phi)) == 11 * identity
    assert source.norms() == (28,)
    result = extract_kernel(source.order, 11, source.split(11), source.reference_pullbacks())
    assert result.known_subspace.cols == rank
    assert result.status == ("NO_INFORMATION", "PARTIAL", "COMPLETE_UNDER_INPUT_PROMISE")[rank]
    assert result.remaining_lagrangian_extensions == (1464, 12, 1)[rank]
    assert result.rank_history == ((0,), (1, 1), (2,))[rank]
    phi = action(source.phi, product_actions(source.split(11)))
    assert mod(phi * result.known_subspace, 11) == zeros(4, rank)


def test_no_target_map_is_manufactured_from_source_words():
    source = word_fixture()
    source.gammas = (unit(source.order),)
    result = recover(source)
    assert result.coordinates == (5 * unit(source.order),)
    output = extract_kernel(source.order, 5, source.split(5), result.coordinates)
    assert output.status == "NO_INFORMATION"
    assert output.remaining_lagrangian_extensions == 156


def test_transported_source_maps_supply_no_kernel_information():
    source = word_fixture()
    a = eye(16)[:, 3] + eye(16)[:, 8]
    gamma = matrix_multiply(source.order, matrix_multiply(source.order, source.phi, a),
                            matrix_star(source.order, source.phi))
    source.gammas = (gamma,)
    coordinates = recover(source).coordinates
    assert coordinates == (25 * a,)
    result = extract_kernel(source.order, 5, source.split(5), coordinates)
    assert result.status == "NO_INFORMATION"


def test_multiple_target_maps_and_negative_trace_pairings_reconstruct():
    source = word_fixture()
    source.gammas = (source.gammas[0], -unit(source.order))
    reconstructed = recover(source)
    assert reconstructed.coordinates == source.reference_pullbacks()
    assert any(b < 0 for pairings in reconstructed.trace_pairings for b in pairings)
    assert reconstructed.target_basis_points_required == 8 * len(reconstructed.primes)


def test_a_quadratic_word_can_have_no_single_step_full_rank():
    source = word_fixture()
    pulled = source.reference_pullbacks()[0]
    actions = product_actions(source.split(5))
    assert column_basis(action(pulled, actions), 5).cols == 1
    assert column_basis(action(matrix_star(source.order, pulled), actions), 5).cols == 1
    result = extract_kernel(source.order, 5, source.split(5), (pulled,), include_adjoints=False)
    assert result.rank_history == (1, 2)
    assert result.word_counts == (1, 1)


def test_insufficient_plan_aborts_before_any_source_queries():
    source = word_fixture()
    with pytest.raises(ValueError, match="insufficient CRT"):
        recover(source, auxiliary_primes=(3,))
    assert source.calls == []


def test_wrong_source_characteristic_is_rejected_before_queries():
    source = word_fixture()
    with pytest.raises(ValueError, match="source discriminant"):
        recover(source, characteristic=19)
    assert source.calls == []


@pytest.mark.parametrize("levels", [(3, 3, 7), (3, 5, 7), (3, 11, 13), (3, 9, 13), (3, 7, 53)])
def test_illegal_plans_are_not_silently_repaired(levels):
    source = word_fixture()
    with pytest.raises(ValueError):
        recover(source, auxiliary_primes=levels)
    assert source.calls == []


def test_noncommon_column_scalars_do_not_pass_similitude_check():
    source = word_fixture()
    packet = source.observe(7)
    bad = packet.weak_action * Matrix.diag(1, 2, 1, 1)
    with pytest.raises(ValueError, match="similitude"):
        weak_pullback_actions(5, 7, replace(packet, weak_action=bad))


def test_local_checks_do_not_certify_global_source_promise():
    source = word_fixture()
    packet = source.observe(7)
    wrong_but_local_similitude = Matrix.diag(2, 1, 2, 1)
    result = weak_pullback_actions(5, 7, replace(packet, weak_action=packet.weak_action * wrong_but_local_similitude))
    expected = tuple(mod(action(x, product_actions(source.split(7))), 7) for x in source.reference_pullbacks())
    assert result != expected  # Passing a local pairing test is not global compatibility.


def test_map_count_change_rejected():
    source = word_fixture()
    with pytest.raises(ValueError, match="map count"):
        recover(source, observe_at=lambda r: replace(source.observe(r), target_maps=()))


def test_empty_and_nonintegral_maps_rejected():
    source = word_fixture()
    with pytest.raises(ValueError, match="at least one"):
        extract_kernel(source.order, 5, source.split(5), ())
    with pytest.raises(ValueError, match="nonintegral"):
        extract_kernel(source.order, 5, source.split(5), (eye(16)[:, 0] / 2,))


def test_non_kernel_maps_are_not_accepted():
    source = word_fixture()
    with pytest.raises(ValueError, match="product identity"):
        extract_kernel(source.order, 5, source.split(5), (unit(source.order),))


def test_modular_rank_is_not_rational_rank():
    matrix = Matrix([[1, 1], [0, 3], [0, 0], [0, 0]])
    assert matrix.rank() == 2
    assert column_basis(matrix, 3).cols == 1
    assert column_basis(zeros(4, 3), 3).shape == (4, 0)


def test_pairing_adjoint_uses_the_product_symplectic_frame():
    source = word_fixture()
    maps = product_actions(source.split(7))
    for i in range(16):
        assert mod(adjoint(maps[i]), 7) == mod(action(matrix_star(source.order, eye(16)[:, i]), maps), 7)
