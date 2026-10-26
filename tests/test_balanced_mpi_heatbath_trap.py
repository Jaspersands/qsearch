from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from flint import arb, ctx
import numpy as np
import pytest

from theorems import balanced_mpi_heatbath_trap as trap
from theorems.balanced_mpi_product_target import harmonic_certificate, harmonic_line_log_weights


@pytest.mark.parametrize("order", [7, 15, 21])
def test_interval_dft_includes_floating_identity(order):
    residues, slopes = [0, 1, 3, 6], [0, 1, 3, 5]
    t, L = Q(1, 20), 9
    with ctx.workprec(96):
        coeffs = trap.coefficients(residues, order, t, L)
        line = trap.interval_line(coeffs, slopes, order)
        constant = 2*len(slopes)*np.log((float(1-t)**.5+float(1-3*t)**.5)/2)
        reference = harmonic_line_log_weights(residues, slopes, order, t, L)-constant
        for interval, value in zip(line, reference):
            assert float(interval) == pytest.approx(value, abs=2e-13)
            assert interval.rad() < arb("1e-20")
        tail = Q(harmonic_certificate(len(slopes), t, L)["uniform_log_weight_error_upper"])
        bound = trap.escape_log_upper(line, tail)
        shifted = np.exp(reference-reference.max())
        actual = 1-shifted[0]/shifted.sum()
        assert actual <= np.exp(float(bound))


def test_dyadic_certificates_use_directed_bounds():
    with ctx.workprec(96):
        assert trap.dyadic_log_test(Q(-178), 256)
        assert not trap.dyadic_log_test(Q(-177), 256)
        assert trap.lower(arb(2).sqrt())**2 <= 2
        assert trap.upper(arb(2).sqrt())**2 >= 2
    with pytest.raises(ValueError, match="row-map"):
        trap.stationary_log_upper(arb(0), Q(0), 7, 2, primitive_rows=False)
    with pytest.raises(ValueError, match="odd"):
        trap.stationary_log_upper(arb(0), Q(0), 8, 2, primitive_rows=True)


def test_stay_probability_is_a_finite_fixed_start_statement():
    value = trap.finite_time_tv_lower(256, 256, 250)
    assert value == Q(63, 64)-Q(1, 2**256)
    assert value > Q(98, 100)
    assert trap.finite_time_tv_lower(2, 2, 3) == 0


def test_nontrap_does_not_pass():
    with ctx.workprec(96):
        coeffs = trap.coefficients([0], 7, Q(1, 20), 9)
        values = trap.interval_line(coeffs, [1], 7)
        tail = Q(harmonic_certificate(1, Q(1, 20), 9)["uniform_log_weight_error_upper"])
        assert not trap.dyadic_log_test(trap.escape_log_upper(values, tail), 256)


def test_saved_native_certificate_scope_and_bounds():
    result = json.loads(trap.REPORT.read_text())
    assert result["producer_sha256"] == hashlib.sha256(
        Path(trap.__file__).read_bytes()).hexdigest()
    bounds = list(map(Q, result["coordinate_log_exit_upper_bounds"]))
    assert len(bounds) == result["dimension"] == 420
    assert max(bounds) == Q(result["maximum_log_exit_upper"])
    with ctx.workprec(96):
        assert trap.dyadic_log_test(max(bounds), result["escape_bound_bits"])
        assert trap.dyadic_log_test(Q(result["stationary_state_log_mass_upper"]),
                                   result["stationary_mass_bound_bits"])
    assert result["primitive_rows_verified"]
    assert result["interval_fft_roundoff_included"]
    assert not result["typical_start_obstruction_proved"]
    assert not result["systematic_basis_or_tempering_obstruction_proved"]
    assert not result["asymptotic_mixing_lower_bound_proved"]
    assert not result["classical_hardness_or_quantum_speedup_proved"]
    counter = result["systematic_basis_escape_countercontrol"]
    assert counter["conditional_exit_at_least_2_to_minus_17_verified"]
    assert Q(counter["conditional_exit_probability_lower"]) >= Q(1, 2**17)
    assert Q(counter["random_scan_exit_probability_lower"]) >= Q(1, 420*2**17)
    assert Q(counter["expected_first_exit_updates_upper"]) <= 420*2**17
    assert not counter["mixing_time_upper_bound_claimed"]
    assert not counter["score_threshold_reached_claimed"]


def test_native_witness_and_two_interval_lines_replay():
    result = json.loads(trap.REPORT.read_text())
    supports, evaluations = trap.mpi.points(13, 6000, 420)
    _, logs, generator = trap.mpi.presentation(13)
    assert generator == result["generator_encoding"]
    assert list(map(int, trap.mpi.field(13).modulus().coeffs())) == result[
        "field_modulus_coefficients"]
    matrix = np.array(logs, dtype=np.int64)[
        np.bitwise_xor(np.array(supports)[:, None], np.array(evaluations)[None, :])]
    residual = ((matrix @ np.array(result["assignment"]) -
                 np.array(result["centers"])) % 8191).tolist()
    assert np.cos(2*np.pi*np.array(residual)/8191).mean() == pytest.approx(
        result["replayed_mean_cosine"], abs=1e-14)
    counter = result["systematic_basis_escape_countercontrol"]
    direction = np.array(counter["direction"], dtype=np.int64)
    unit = np.zeros(420, dtype=np.int64)
    unit[counter["basis_column"]] = 1
    np.testing.assert_array_equal(matrix[:420] @ direction % 8191, unit)
    tail = Q(result["harmonic_certificate"]["uniform_log_weight_error_upper"])
    with ctx.workprec(96):
        coeffs = trap.coefficients(residual, 8191, Q(1, 20), 9)
        original = trap.interval_line(coeffs, matrix[:, 0].tolist(), 8191)
        assert trap.escape_log_upper(original, tail) <= Q(
            result["coordinate_log_exit_upper_bounds"][0])
        systematic = trap.interval_line(coeffs, (matrix @ direction % 8191).tolist(), 8191)
        ratio = (systematic[counter["step"]]-systematic[0]-2*trap.ball(tail)).exp()
        assert trap.lower(ratio/(1+ratio)) >= Q(counter["conditional_exit_probability_lower"])
