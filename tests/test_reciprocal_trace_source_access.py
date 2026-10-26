from fractions import Fraction
import hashlib
import json

import pytest

from theorems.balanced_codeword_filter import root_spectrum
from theorems.reciprocal_trace_source_access import (
    REPORT, ROOT, finite_audit, reference_curve_order, sample_nonzero_fourier,
    scaled_amplitude, walsh_from_counter,
)


@pytest.mark.parametrize("bits", [2, 3, 4, 5])
def test_actual_curve_points_equal_signed_fourier_coefficients_and_exact_sampler_law(bits):
    q = 1 << bits
    row = finite_audit(bits)
    for target in (0, 1):
        _, spectrum = root_spectrum(bits, target)
        for u in range(q):
            assert scaled_amplitude(bits, u, target, reference_curve_order) == 2*spectrum[u]
    assert row["signed_walsh"][0] == 0
    assert sum(row["nonzero_law_numerators"]) == q*q
    assert sum(Fraction(w*w, 8*q*q) for w in row["signed_walsh"]) == Fraction(1, 8)
    assert not row["reference_is_polynomial_in_field_bits"]


def test_zero_frequency_does_not_count_a_singular_curve():
    def forbidden(*args):
        raise AssertionError("zero frequency must not call the curve backend")

    assert walsh_from_counter(61, 0, forbidden) == 0
    assert scaled_amplitude(61, 0, 1, forbidden) == 1 << 61
    with pytest.raises(ValueError):
        reference_curve_order(5, 0)


def test_negative_phases_survive_and_targets_have_equal_probabilities():
    row = finite_audit(5)
    assert any(w < 0 for w in row["signed_walsh"])
    assert any(w == 0 for w in row["signed_walsh"][1:])
    for u in range(1, 32):
        a = scaled_amplitude(5, u, 0, reference_curve_order)
        b = scaled_amplitude(5, u, 1, reference_curve_order)
        assert a == -b and a*a == b*b


def test_rejection_threshold_and_counter_cost_are_exact_not_a_histogram_test():
    q = 8
    for u in range(q):
        w = walsh_from_counter(3, u, reference_curve_order)
        accepted = 0
        for threshold in range(8*q):
            class FixedBits:
                def getrandbits(self, bits):
                    return u if bits == 3 else threshold

            row = sample_nonzero_fourier(3, reference_curve_order, attempts=1, rng=FixedBits())
            accepted += row["status"] == "ACCEPTED_NONZERO_FOURIER_SAMPLE"
            assert row["point_counter_calls"] == int(u != 0)
            assert not row["coherent_state_prepared"]
        assert accepted == w*w


def test_abort_is_explicit_and_full_mixture_renormalization_would_be_biased():
    class ZeroBits:
        def getrandbits(self, bits):
            return 0

    row = sample_nonzero_fourier(61, lambda *args: 0, attempts=9, rng=ZeroBits())
    assert row["status"] == "ABORT_ATTEMPT_CAP"
    assert row["trials"] == 9 and row["point_counter_calls"] == 0
    assert row["frequency"] is None
    nonzero_abort = Fraction(7, 8)**9
    zero_mass = Fraction(1, 2)
    nonzero_mass = (1-nonzero_abort)/2
    abort_mass = nonzero_abort/2
    assert zero_mass+nonzero_mass+abort_mass == 1
    assert zero_mass/(zero_mass+nonzero_mass) > Fraction(1, 2)


@pytest.mark.parametrize("count", [True, 0, 3, 10_000])
def test_malformed_point_counts_rejected(count):
    with pytest.raises(ValueError, match="point count"):
        walsh_from_counter(5, 1, lambda *args: count)


def test_reference_cannot_silently_be_used_as_a_scalable_counter():
    with pytest.raises(ValueError, match="reference"):
        reference_curve_order(17, 1)
    with pytest.raises(ValueError):
        sample_nonzero_fourier(5, reference_curve_order, attempts=0)


def test_live_artifact_replays_counts_and_declares_missing_scalable_backend():
    data = json.loads(REPORT.read_text())
    assert data["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/reciprocal_trace_source_access.py").read_bytes()).hexdigest()
    assert data["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/RECIPROCAL_TRACE_SOURCE_ACCESS.md").read_bytes()).hexdigest()
    assert not data["scalable_point_counter_implemented"]
    assert not data["full_native_solver_or_coherent_readout_simulator"]
    assert Fraction(*data["nonzero_sampler_abort_probability"]) == Fraction(7, 8)**data["nonzero_rejection_attempt_cap"]
    for row in data["finite_controls"]:
        assert row == finite_audit(row["bits"])
