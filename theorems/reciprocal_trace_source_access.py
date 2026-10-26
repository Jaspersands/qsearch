"""Classical Fourier-source access via known binary elliptic point counting.

The scalable point counter is an explicit imported dependency, NOT implemented
by the exponential reference here. No coherent filter simulation is claimed.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from random import Random

from theorems.balanced_codeword_filter import integer
from theorems.explicit_quadratic_opi import element, field


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/reciprocal_trace_source_access.json"


@lru_cache(maxsize=128)
def reference_curve_order(bits, parameter):
    """Count O(q^2) pairs on v^2+z*v=z^3+parameter, plus infinity."""
    integer(bits, 2, 5, "exponential reference bits")
    integer(parameter, 1, (1 << bits)-1, "nonsingular curve parameter")
    values = tuple(element(bits, z) for z in range(1 << bits))
    a = element(bits, parameter)
    return 1+sum(v*v+z*v == z*z*z+a for z in values for v in values)


def walsh_from_counter(bits, frequency, point_counter):
    """The counter must return the exact order in the SAME public field basis.

    Hasse/divisibility checks detect malformed output, not every wrong count.
    They are not a replacement for a correct point-counting backend.
    """
    integer(bits, 2, 128, "field bits")
    q = 1 << bits
    integer(frequency, 0, q-1, "frequency")
    if not frequency:
        return 0
    count = point_counter(bits, frequency)
    if type(count) is not int or count <= 0 or (count-q-1)**2 > 4*q or count % 4:
        raise ValueError("point count violates the native Hasse/divisibility checks")
    return count-q


def scaled_amplitude(bits, frequency, target, point_counter):
    """Return sqrt(2)*q times the signed normalized source amplitude."""
    integer(target, 0, 1, "target")
    value = walsh_from_counter(bits, frequency, point_counter)
    return (1 << bits) if frequency == 0 else (-1)**target*value


def sample_nonzero_fourier(bits, point_counter, attempts=128, seed=1022, rng=None):
    """Exact nonzero law conditional on acceptance, with an explicit ABORT.

    Expected eight trials for an exact counter and IID uniform random bits.
    Fixed-cap failure is (7/8)^attempts, never silently normalized away.
    """
    integer(bits, 2, 128, "field bits")
    integer(attempts, 1, 1_000_000, "attempt cap")
    rng = Random(seed) if rng is None else rng
    calls = 0
    for trial in range(1, attempts+1):
        u = rng.getrandbits(bits)
        integer(u, 0, (1 << bits)-1, "random frequency")
        w = walsh_from_counter(bits, u, point_counter)
        calls += int(u != 0)
        threshold = rng.getrandbits(bits+3)
        integer(threshold, 0, (1 << (bits+3))-1, "random acceptance threshold")
        if threshold < w*w:
            return {"status": "ACCEPTED_NONZERO_FOURIER_SAMPLE", "frequency": u,
                    "signed_walsh": w, "trials": trial, "point_counter_calls": calls,
                    "coherent_state_prepared": False}
    return {"status": "ABORT_ATTEMPT_CAP", "frequency": None, "trials": attempts,
            "point_counter_calls": calls, "coherent_state_prepared": False}


def finite_audit(bits):
    integer(bits, 2, 5, "exponential audit bits")
    q = 1 << bits
    counts = [None]+[reference_curve_order(bits, u) for u in range(1, q)]
    walsh = [0]+[count-q for count in counts[1:]]
    if sum(w*w for w in walsh) != q*q:
        raise ArithmeticError("point counts failed the balanced Walsh Parseval check")
    if any(w*w > 8*q for w in walsh):
        raise ArithmeticError("rejection envelope violated")
    return {"bits": bits, "field_modulus": list(map(int, field(bits).modulus().coeffs())),
            "point_counts": counts, "signed_walsh": walsh,
            "one_trial_acceptance": [1, 8], "nonzero_law_denominator": q*q,
            "nonzero_law_numerators": [w*w for w in walsh],
            "affine_pairs_enumerated": (q-1)*q*q,
            "reference_is_polynomial_in_field_bits": False,
            "source_sampler_control": sample_nonzero_fourier(bits, reference_curve_order, seed=1000*bits+22)}


def report():
    cap = 128
    abort = Fraction(7, 8)**cap
    return {"status": "KNOWN_CLASSICAL_FOURIER_SOURCE_ACCESS_NOT_FULL_DEQUANTIZATION",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/RECIPROCAL_TRACE_SOURCE_ACCESS.md").read_bytes()).hexdigest(),
            "scalable_point_counter_implemented": False,
            "point_counter_dependency": "Correct characteristic-two elliptic-curve point counting in the supplied field basis",
            "full_native_solver_or_coherent_readout_simulator": False,
            "speedup_established": False,
            "nonzero_rejection_attempt_cap": cap,
            "nonzero_sampler_abort_probability": [abort.numerator, abort.denominator],
            "finite_controls": [finite_audit(n) for n in (2, 3, 4, 5)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = report()
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"], "scalable_point_counter_implemented": False,
                      "checked_fields": [r["bits"] for r in data["finite_controls"]],
                      "checked_nonsingular_curves": sum((1 << r["bits"])-1 for r in data["finite_controls"])}, indent=2))


if __name__ == "__main__":
    main()
