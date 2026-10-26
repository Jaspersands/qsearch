from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from flint import fmpz_mat
import pytest

from theorems import integer_character_interpolation as integer
from theorems import integer_character_near_vector as near


def test_uniform_bound_has_exact_distance_and_success_margins():
    cert = near.uniform_certificate()
    assert Q(cert["mean_normalized_squared_distance_upper"]) < Q(3, 50)
    assert Q(cert["conditional_success_after_tv_error_lower"])/8 > Q(1, 128)
    assert Q(cert["radius_rounding_check"]) > near.GRID_THRESHOLD
    assert not cert["relative_CVP_approximation_factor_claimed"]


def test_fourier_tail_bound_uses_the_right_sign_of_pi_endpoint():
    positive = near.distance_bound(Q(0), Q(1), 2)
    negative = near.distance_bound(Q(1, 2), Q(0), 16)
    assert positive["pi_squared_endpoint_used"] == "9"
    assert negative["pi_squared_endpoint_used"] == "484/49"


@pytest.mark.parametrize("moment", [2, 4])
def test_finite_distribution_checks_mean_second_moment_and_distance(moment):
    control = near.small_control(moment)
    assert abs(control["target_norm"]-1) < 1e-12
    first, second = control["target_cosine_moments"][:2]
    assert abs(first-float(Q(control["source_first_mean_lower"]))) < 1e-12
    assert abs(second-float(Q(control["source_second_mean"]))) < 1e-12
    assert all(abs(v) < 1e-12 for v in control["target_cosine_moments"][2:])
    assert control["target_mean_square"] <= float(Q(
        control["distance_bound"]["mean_normalized_squared_distance_upper"]))


def test_first_moment_guard_does_not_justify_third_harmonic():
    counter = near.higher_alias_control()
    assert counter["first_moment_height_guard_valid"]
    assert counter["third_harmonic_alias_present"]
    assert 5**4*7 == 1+6*729
    with pytest.raises(ValueError):
        integer.height_license((2, 5, 7), 1, 6, moment=16)


def test_cosine_threshold_does_not_imply_useful_euclidean_distance():
    counter = near.unsafe_cosine_control()
    assert Q(counter["mean_cosine"]) > Q(3, 10)
    assert Q(counter["mean_square"]) > Q(counter["continuous_uniform_mean_square"])
    assert counter["zero_residual_count"]+counter["half_period_residual_count"] == 50


@pytest.mark.parametrize("order,labels", [(18, [1, 5, 16]), (21, [1, 7, 3, 20])])
def test_exact_primal_dual_bases_including_nonunit_labels(order, labels):
    decoder, numerator = near.lattice_bases(labels, order)
    left, right = fmpz_mat(decoder), fmpz_mat(numerator)
    m = len(labels)
    assert left.det() == order
    assert right.det() == order**(m-1)
    assert right*left.transpose() == fmpz_mat(
        [[order*int(i == j) for j in range(m)] for i in range(m)])


def test_lattice_witness_and_inverse_are_exact_for_large_integers():
    order = 2*3**700
    labels = [1, order-5, order//3+11]
    centers, assignment = [order-1, 23, order//2], order-17
    found = near.witness(labels, centers, order, assignment)
    assert near.recover_assignment(labels, order, found["numerator"]) == assignment
    assert all(-order//2 <= r < order//2 for r in found["centered_residuals"])
    assert found["mean_square"] == sum(
        (Q(v-c, order)**2 for v, c in zip(found["numerator"], centers)), Q(0))/3
    bad = found["numerator"].copy()
    bad[1] += 1
    with pytest.raises(ValueError):
        near.recover_assignment(labels, order, bad)


@pytest.mark.parametrize("bad", [([0, 1], 18), ([1.0, 3], 18), ([1, 18], 18)])
def test_invalid_lattice_labels_are_rejected(bad):
    with pytest.raises(ValueError):
        near.lattice_bases(*bad)


def test_arbitrary_rational_targets_pay_rounding_and_integer_translation():
    target = [Q(-17, 13), Q(1000000, 7), Q(1, 36)]
    centers, shifts, errors = near.rational_target_centers(target, 18)
    assert all(0 <= c < 18 for c in centers)
    for t, c, z, error in zip(target, centers, shifts, errors):
        assert Q(c, 18)+z-t == error
        assert abs(error) <= Q(1, 36)
    local = near.witness([1, 5, 16], centers, 18, 9)
    lifted = [Q(v, 18)+z for v, z in zip(local["numerator"], shifts)]
    assert all(w-t == Q(r, 18)+e
               for w, t, r, e in zip(lifted, target, local["centered_residuals"], errors))


def test_native_report_has_stronger_guard_and_no_optimizer_claim():
    saved = json.loads(near.REPORT.read_text())
    assert saved["producer_sha256"] == hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest()
    native = saved["native"]
    assert native["source_control_artifact_sha256"] == hashlib.sha256(
        integer.REPORT.read_bytes()).hexdigest()
    labels = list(map(int, native["public_labels_decimal"]))
    centers = list(map(int, native["centers_decimal"]))
    order = int(native["cyclic_order_decimal"])
    integer.validate_public_labels(
        native["public_primes"], labels, native["modulus_exponent"])
    integer.height_license(
        native["public_primes"], 35, native["modulus_exponent"], moment=16)
    error = [0]*1024
    for position in native["positive_positions"]:
        error[position] = 1
    for position in native["negative_positions"]:
        error[position] = -1
    syndrome = sum(a*y for a, y in zip(labels, error)) % order
    assert str(syndrome) == native["observed_syndrome_decimal"]
    assert integer.decode(native["public_primes"], 35,
                          native["modulus_exponent"], syndrome) == tuple(error)
    replay = near.witness(labels, centers, order, 0)
    assert str(replay["mean_square"]) == native[
        "zero_assignment_validation_control"]["mean_square"]
    first, second = near.source_moments(1024, 35)
    assert near.distance_bound(first, second, 16) == native["distance_bound"]
    assert Q(native["distance_bound"]["mean_normalized_squared_distance_upper"]) < Q(3, 50)
    assert not native["old_cosine_modulus_covers_sixteen_moments"]
    assert not native["native_quantum_optimizer_executed"]
    assert not native["native_classical_optimizer_executed"]
    assert not saved["general_lattice_hardness_reduction"]
