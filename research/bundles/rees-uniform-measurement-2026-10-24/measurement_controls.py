"""Bounded circuit falsifiers. These enumerations are NOT the algorithm.

The operational circuit has no hidden-subgroup or expected-projector input.
The spectator coordinate can be the noncentral part of a Rees group, and
the reference is left untouched. Only the public central translation acts.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from measurement_plan import address_plan, character_plan, decode_phase, terminal_sampling_plan
from fractions import Fraction


def _finite_contract(prime, phase_bits):
    if prime not in (3, 5, 7, 11, 13) or type(phase_bits) is not int or not 1 <= phase_bits <= 12:
        raise ValueError("bounded control only: named small primes and at most12 phase bits")


def hadamard_axis(state):
    result = state.copy()
    size = result.shape[0]
    stride = 1
    while stride < size:
        for start in range(0, size, 2 * stride):
            a = result[start:start + stride].copy()
            b = result[start + stride:start + 2 * stride].copy()
            result[start:start + stride] = (a + b) / np.sqrt(2)
            result[start + stride:start + 2 * stride] = (a - b) / np.sqrt(2)
        stride *= 2
    return result


def controlled_powers(state, prime, phase_bits, direction=1):
    """Literal t controlled modular permutations, not a spectral shortcut."""
    result = state.copy()
    indices = np.arange(1 << phase_bits)
    for k in range(phase_bits):
        mask = (indices & (1 << k)) != 0
        # Axes: phase, label, spectator, central coordinate, reference.
        result[mask] = np.roll(result[mask], -direction * pow(2, k, prime), axis=3)
    return result


def qpe(state, prime, phase_bits, *, inverse=False, direction=1):
    size = 1 << phase_bits
    if inverse:
        state = np.fft.ifft(state, axis=0) * np.sqrt(size)
        state = controlled_powers(state, prime, phase_bits, -direction)
        return hadamard_axis(state)
    state = hadamard_axis(state)
    state = controlled_powers(state, prime, phase_bits, direction)
    return np.fft.fft(state, axis=0) / np.sqrt(size)


def extract_character(state, prime, phase_bits, *, wrong_sign=False):
    """Retain the full source and phase workspace; copy a label then uncompute."""
    _finite_contract(prime, phase_bits)
    state = np.asarray(state, dtype=complex)
    if state.ndim != 3 or state.shape[1] != prime or np.prod(state.shape) > 2048:
        raise ValueError("bounded spectator x center x reference state required")
    if not np.isfinite(state).all() or abs(np.linalg.norm(state) - 1) > 1e-10:
        raise ValueError("normalized finite state required")
    registers = np.zeros((1 << phase_bits, prime, *state.shape), dtype=complex)
    registers[0, 0] = state
    direction = -1 if wrong_sign else 1
    registers = qpe(registers, prime, phase_bits, direction=direction)
    for m in range(1 << phase_bits):
        registers[m] = np.roll(registers[m], decode_phase(m, phase_bits, prime), axis=0)
    return qpe(registers, prime, phase_bits, inverse=True, direction=direction)


def spectral_projector(prime, label):
    # P_lambda = p^-1 sum_z chi_lambda(z) R(-z), matching measuredState.
    return sum(np.exp(2j * np.pi * label * z / prime) * np.roll(np.eye(prime), z, axis=0)
               for z in range(prime)) / prime


def ideal_extraction(state, prime, phase_bits):
    out = np.zeros((1 << phase_bits, prime, *state.shape), dtype=complex)
    for label in range(prime):
        out[0, label] = np.einsum("ab,qbr->qar", spectral_projector(prime, label), state)
    return out


def qpe_bad_probability(prime, phase_bits, label):
    _finite_contract(prime, phase_bits)
    if type(label) is not int or not 0 <= label < prime:
        raise ValueError("canonical character label required")
    size = 1 << phase_bits
    phase = np.exp(2j * np.pi * np.arange(size) * label / prime)
    amplitudes = np.fft.fft(phase) / size
    bad = [m for m in range(size) if decode_phase(m, phase_bits, prime) != label]
    return float(np.sum(np.abs(amplitudes[bad])**2))


def cq_trace_distance(actual, ideal):
    """Discard phase work, measure labels, keep target AND arbitrary reference."""
    distance = 0.0
    for label in range(actual.shape[1]):
        a = actual[:, label].reshape(actual.shape[0], -1)
        b = ideal[:, label].reshape(ideal.shape[0], -1)
        difference = a.T @ a.conj() - b.T @ b.conj()
        distance += float(np.linalg.eigvalsh(difference).__abs__().sum()) / 2
    return distance


def fourier_state(prime, label):
    return np.exp(2j * np.pi * label * np.arange(prime) / prime) / np.sqrt(prime)


def audit():
    rows = []
    rng = np.random.default_rng(28417)
    for prime, bits in ((3, 5), (3, 8), (5, 7), (7, 8)):
        # For p=3, spectator dimension9 is the actual Heisenberg coordinate size.
        spectator = 9 if prime == 3 else 2
        state = rng.normal(size=(spectator, prime, 2)) + 1j * rng.normal(size=(spectator, prime, 2))
        state /= np.linalg.norm(state)
        actual = extract_character(state, prime, bits)
        ideal = ideal_extraction(state, prime, bits)
        bad = max(qpe_bad_probability(prime, bits, label) for label in range(prime))
        rows.append({
            "prime": prime, "phase_bits": bits,
            "target_dimension": spectator * prime, "reference_dimension": 2,
            "maximum_rounding_failure": bad,
            "analytic_rounding_bound": 4 * prime / (1 << bits),
            "isometry_error": float(np.linalg.norm(actual - ideal)),
            "worst_sector_isometry_error_bound": float(np.sqrt(2 * bad)),
            "complete_cq_trace_distance": cq_trace_distance(actual, ideal),
            "norm_error": abs(float(np.linalg.norm(actual)) - 1),
        })
    prime, bits = 3, 8
    eigenstate = fourier_state(prime, 1)[None, :, None]
    ideal = ideal_extraction(eigenstate, prime, bits)
    wrong = extract_character(eigenstate, prime, bits, wrong_sign=True)
    wrong_sign_distance = cq_trace_distance(wrong, ideal)
    # Measuring the Fourier-transformed center and retaining that basis is wrong.
    retained_basis_state = np.eye(prime, dtype=complex)[1]
    correct_correlation = np.vdot(eigenstate.ravel(), np.roll(eigenstate.ravel(), -1))
    wrong_correlation = np.vdot(retained_basis_state, np.roll(retained_basis_state, -1))
    large_prime = 2**127 - 1
    return {
        "scope": "public-operation construction and bounded circuit falsifiers",
        "finite_controls": rows,
        "wrong_sign_complete_instrument_distance": wrong_sign_distance,
        "retained_fourier_basis_correlation_error": float(abs(correct_correlation - wrong_correlation)),
        "large_prime_plan": character_plan(large_prime, 73, Fraction(1, 1000000), public_fast_powers=True).report(),
        "public_address_plan": address_plan(large_prime, 200, Fraction(1, 1000000)),
        "terminal_sample_plan": terminal_sampling_plan(large_prime, 73, Fraction(1, 1000000)),
        "scope_flags": {
            "constructive_source_preserving_measurement": True,
            "complete_instrument_error_bound_derived": True,
            "known_phase_estimation_primitive_not_novel": True,
            "independently_reviewed_current_pass": False,
            "new_lean_theorem": False,
            "full_gate_compiler_implemented": False,
            "end_to_end_hsp_execution": False,
            "novelty_or_speedup_certified": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit()
    root = Path(__file__).resolve().parent
    names = ("measurement_plan.py", "measurement_controls.py", "test_measurement.py", "UNIFORM_MEASUREMENT.md", "HANDOFF.md")
    report["source_sha256"] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}
    formal = root.parent / "rees-formal-core-2026-10-24"
    report["prior_native_receipt_sha256"] = hashlib.sha256((formal / "native_source_receipt.json").read_bytes()).hexdigest()
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    print(payload, end="")
