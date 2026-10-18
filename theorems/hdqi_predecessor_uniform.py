"""Test the independent-Pauli predecessor-uniform HDQI construction.

The pilot-state mechanism is prior art (arXiv:2604.01022). This local,
review-pending analysis checks whether adding trivial syndrome decoding
actually supplies a hard ENERGY optimization family. It does not: with
independent symplectic labels, every added term either shifts the spectral
radius by |c| or maps it to sqrt(R**2+c**2). Dependent terms and other graphs
are deliberately rejected. No Gibbs/output-sampling dequantization follows.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_subset_sum_two_adic_search import gf2_rank


ARTIFACT = ROOT / "research/classical_baselines/hdqi_predecessor_uniform.json"


def _fraction(value) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError("coefficients must be explicit exact rationals, not floats")
    return Fraction(value)


def canonical_paulis(anticommutes_with_predecessors: Sequence[int]) -> list[str]:
    """Independent physical generators: P_j = Z_<j X_j, or just X_j."""
    bits = tuple(anticommutes_with_predecessors)
    if not bits or any(type(b) is not int or b not in (0, 1) for b in bits):
        raise ValueError("nonempty binary predecessor specification required")
    m = len(bits)
    return [("Z" if b else "I") * j + "X" + "I" * (m - j - 1) for j, b in enumerate(bits)]


def independent_profile(paulis: Sequence[str], coefficients: Sequence) -> dict:
    """Verify rank and discover an ordering; no hidden decoder/oracle premise."""
    words = tuple(paulis)
    if not words or not words[0] or any(not isinstance(p, str) or len(p) != len(words[0])
                                      or set(p) - set("IXYZ") for p in words):
        raise ValueError("nonempty equal-width Pauli words over IXYZ required")
    coeffs = tuple(_fraction(c) for c in coefficients)
    if len(words) != len(coeffs):
        raise ValueError("one exact coefficient per Pauli required")
    n, m = len(words[0]), len(words)
    masks = [(sum((p in "XY") << j for j, p in enumerate(word)),
              sum((p in "ZY") << j for j, p in enumerate(word))) for word in words]
    rank = gf2_rank([x | (z << n) for x, z in masks])
    if rank != m:
        raise ValueError("dependent symplectic labels: the energy recurrence is not licensed")
    adjacency = []
    for x, z in masks:
        adjacency.append(sum((((x & zz).bit_count() + (z & xx).bit_count()) % 2) << j
                             for j, (xx, zz) in enumerate(masks)))
    remaining = (1 << m) - 1
    removed = []
    while remaining:
        found = False
        for j in range(m):
            if not (remaining >> j) & 1:
                continue
            neighbors = adjacency[j] & remaining
            if neighbors in (0, remaining ^ (1 << j)):
                removed.append((j, int(bool(neighbors))))
                remaining ^= 1 << j
                found = True
                break
        if not found:
            raise ValueError("no predecessor-uniform order: unsupported, not hardness")
    ordered = list(reversed(removed))
    return {"qubits": n, "term_count": m, "symplectic_rank": rank,
            "order": [j for j, _ in ordered],
            "anticommutes_with_predecessors": [b for _, b in ordered],
            "ordered_coefficients": [str(coeffs[j]) for j, _ in ordered],
            "decoder": "Full-column-rank binary linear inversion; no weight promise needed",
            "original_input_sha256": hashlib.sha256(json.dumps(
                {"paulis": words, "coefficients": [str(c) for c in coeffs]}, sort_keys=True).encode()).hexdigest()}


def _sqrt_bracket(value: Fraction, bits: int) -> tuple[Fraction, Fraction]:
    scale = 1 << bits
    integer = math.isqrt(value.numerator * scale ** 2 // value.denominator)
    lo = Fraction(integer, scale)
    hi = lo if lo * lo == value else Fraction(integer + 1, scale)
    assert lo * lo <= value <= hi * hi
    return lo, hi


def energy_certificate(profile: dict, bits: int = 80) -> dict:
    """Enclose the radius recurrence for an independent_profile result.

    This low-level routine does not re-validate an arbitrary external dict.
    Raw Hamiltonian consumers must use solve_ground_energy below.
    """
    if type(bits) is not int or not 8 <= bits <= 4096:
        raise ValueError("precision must be 8..4096 bits")
    coefficients = [_fraction(c) for c in profile["ordered_coefficients"]]
    modes = profile["anticommutes_with_predecessors"]
    if len(modes) != len(coefficients) or any(type(b) is not int or b not in (0, 1) for b in modes):
        raise ValueError("invalid ordered profile")
    lo = hi = Fraction()
    steps = []
    for c, anti in zip(coefficients, modes):
        old_lo, old_hi = lo, hi
        if anti:
            lo = _sqrt_bracket(old_lo ** 2 + c ** 2, bits)[0]
            hi = _sqrt_bracket(old_hi ** 2 + c ** 2, bits)[1]
            operation = "sqrt(R^2+c^2)"
        else:
            lo, hi = lo + abs(c), hi + abs(c)
            operation = "R+abs(c)"
        steps.append({"coefficient": str(c), "operation": operation,
                      "radius_lower": str(lo), "radius_upper": str(hi)})
    width = hi - lo
    assert width <= Fraction(sum(modes), 1 << bits)
    return {"energy_lower": str(-hi), "energy_upper": str(-lo), "width": str(width),
            "precision_bits": bits, "arithmetic_steps": len(steps), "steps": steps,
            "numerical_eigensolver_used_by_solver": False,
            "claims_Gibbs_or_output_sampling_is_classical": False,
            "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def solve_ground_energy(paulis: Sequence[str], coefficients: Sequence, bits: int = 80) -> dict:
    """Validate the actual input before issuing any optimum-energy enclosure."""
    profile = independent_profile(paulis, coefficients)
    return {"profile": profile, "certificate": energy_certificate(profile, bits)}


def pauli_matrix(word: str) -> np.ndarray:
    if not word or len(word) > 8 or set(word) - set("IXYZ"):
        raise ValueError("dense physical calibration requires 1..8 qubits")
    matrices = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]),
                "Y": np.array([[0, -1j], [1j, 0]]), "Z": np.diag([1, -1])}
    result = np.ones((1, 1), dtype=complex)
    for letter in word:
        result = np.kron(result, matrices[letter])
    return result


def canonical_ground_state(modes: Sequence[int], coefficients: Sequence) -> np.ndarray:
    """Execute a canonical-family ground circuit; not a compiled HDQI circuit.

    Isolated additions prepare an X eigenstate. Universal additions append
    |0> and rotate by exp(-i theta Z_<j Y_j/2), theta=-atan2(c,R).
    """
    words = canonical_paulis(modes)
    if len(words) > 8 or len(words) != len(coefficients):
        raise ValueError("dense ground-state calibration requires <=8 terms")
    state = np.ones(1, dtype=complex)
    radius = 0.0
    for anti, raw in zip(modes, coefficients):
        c = float(_fraction(raw))
        if not anti:
            bit = np.array([1, -math.copysign(1, c)]) / math.sqrt(2) if c else np.array([1, 0])
            state = np.kron(state, bit)
            radius += abs(c)
        else:
            theta = -math.atan2(c, radius)
            z_state = np.array([(-1) ** i.bit_count() * amp for i, amp in enumerate(state)])
            state = (math.cos(theta / 2) * np.kron(state, [1, 0])
                     + math.sin(theta / 2) * np.kron(z_state, [0, 1]))
            radius = math.hypot(radius, c)
    return state


def native_control(modes: Sequence[int], coefficients: Sequence) -> dict:
    words = canonical_paulis(modes)
    profile = independent_profile(words, coefficients)
    certificate = energy_certificate(profile)
    h = sum(float(_fraction(c)) * pauli_matrix(p) for p, c in zip(words, coefficients))
    state = canonical_ground_state(modes, coefficients)
    eigenvalues = np.linalg.eigvalsh(h)
    exact_lo = float(Fraction(certificate["energy_lower"]))
    exact_hi = float(Fraction(certificate["energy_upper"]))
    native_energy = float(eigenvalues[0])
    residual = float(np.linalg.norm(h @ state - native_energy * state))
    return {"paulis": words, "coefficients": [str(_fraction(c)) for c in coefficients],
            "profile": profile, "energy_certificate": certificate,
            "native_smallest_eigenvalue": native_energy,
            "native_ground_state_residual": residual,
            "native_norm_error": abs(float(np.vdot(state, state).real) - 1),
            "float_calibration_agrees": exact_lo - 1e-10 <= native_energy <= exact_hi + 1e-10 and residual < 1e-10,
            "compiled_hdqi_circuit": False,
            "ground_state_is_for_canonical_realization_only": True}


def run_controls() -> dict:
    modes = [(0, 0, 0, 0), (0, 1, 1, 1), (0, 1, 0, 1), (0, 0, 1, 0, 1, 0)]
    controls = [native_control(seq, [(-1) ** j * Fraction(j + 1, 3) for j in range(len(seq))]) for seq in modes]
    large_modes = [0] + [int(j % 3 != 0) for j in range(1, 512)]
    large_coefficients = [str(Fraction((-1) ** j * (1 + j % 7), 5)) for j in range(512)]
    large_profile = independent_profile(canonical_paulis(large_modes), large_coefficients)
    large = {"source_specification": {"canonical_modes": large_modes, "coefficients": large_coefficients},
             "profile": large_profile, "certificate": energy_certificate(large_profile),
             "dense_quantum_run_performed": False}
    return {"schema_version": "hdqi-predecessor-uniform-v1", "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "literature": ["https://arxiv.org/abs/2604.01022", "https://arxiv.org/abs/2601.18773"],
            "question": "Does independent-label predecessor-uniform HDQI yield hard ground-energy optimization?",
            "answer": "No: a polynomial-time scalar recurrence supplies certified optimum energy for this family",
            "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NO_NOVELTY_CLAIM",
            "controls": controls, "large_symbolic_control": large,
            "new_quantum_algorithm_claimed": False,
            "central_candidate_or_negative_created": False,
            "all_native_calibrations_pass": all(c["float_calibration_agrees"] for c in controls),
            "unresolved": ["Dependent symplectic labels", "Non-predecessor-uniform graphs", "Gibbs/output sampling", "Native Clifford transport of the canonical ground circuit"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        ARTIFACT.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"all_native_calibrations_pass": report["all_native_calibrations_pass"],
                      "native_controls": len(report["controls"]), "large_terms": 512,
                      "new_quantum_algorithm_claimed": False}, indent=2))


if __name__ == "__main__":
    main()
