"""Review-pending uniform algorithm and error budget, not a speedup claim.

The certificate checks rational constants in the accompanying proof. It is
not a compiled quantum circuit or a kernel-checked proof of that argument.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import arb, ctx, fmpq

from theorems import integer_character_interpolation as integer

REPORT = ROOT / "research/phase_workbench/integer_character_uniform.json"
MIN_LENGTH = 20000
MEAN_LOWER = Q(601, 2000)


def uniform_constants():
    """Exact endpoints for the monotone inequalities proved in the note."""
    gap_slope = Q(1, 100)-Q(199, 20000)
    gap_intercept = -Q(39, 40)
    edge_tail_coefficient = Q(39, 800)/Q(199, 20000)**2
    edge_mass_lower = Q(39, 40)
    mean_squared_lower = Q(19, 200)*edge_mass_lower**2
    if not (gap_slope > 0
            and gap_slope*MIN_LENGTH+gap_intercept >= 0
            and edge_tail_coefficient/MIN_LENGTH < 1-edge_mass_lower
            and MEAN_LOWER**2 < mean_squared_lower):
        raise ArithmeticError("uniform rational inequalities failed")
    return {
        "minimum_length": MIN_LENGTH,
        "cap_rule": "floor(7*m/200)",
        "active_probability": "1/20",
        "positive_gap_comparison_slope": str(gap_slope),
        "positive_gap_comparison_intercept": str(gap_intercept),
        "edge_tail_upper_coefficient_over_m": str(edge_tail_coefficient),
        "edge_mass_lower": str(edge_mass_lower),
        "mean_squared_lower": str(mean_squared_lower),
        "mean_cosine_lower": str(MEAN_LOWER),
        "scope": "rational constants in a written all-length proof; not formal verification",
    }


def tail_bounds(length):
    if type(length) is not int or length < MIN_LENGTH:
        raise ValueError("the uniform certificate requires m >= 20000")
    cap = 7*length//200
    variance = Q(39*length, 1600)
    z_gap = cap+1-Q(length, 40)
    z_lower = 1-2*variance/z_gap**2
    edge_variance = Q(39*(length-1), 1600)
    positive_gap = cap-Q(length-1, 40)
    negative_gap = cap+1-Q(length-1, 40)
    edge_lower = 1-edge_variance/positive_gap**2-edge_variance/negative_gap**2
    if not (z_lower >= Q(1, 4) and edge_lower > Q(39, 40)):
        raise ArithmeticError("finite tail bounds contradict the uniform certificate")
    return {
        "length": length, "cap_each_sign": cap,
        "retained_mass_lower": str(z_lower),
        "edge_mass_lower": str(edge_lower),
        "method": "union bound and separate binomial variances; no independence of sign counts",
    }


def error_budget(*, mean_lower=MEAN_LOWER, retained_mass_lower=Q(1, 4),
                 tv_error=Q(1, 10000), score_error=Q(1, 100000)):
    values = (mean_lower, retained_mass_lower, tv_error, score_error)
    if any(not isinstance(value, Q) for value in values):
        raise ValueError("exact rational bounds required")
    threshold = Q(3, 10)
    if not (Q(1, 4) <= retained_mass_lower <= 1
            and 0 < tv_error <= Q(1, 2) and score_error > 0
            and threshold+2*score_error < mean_lower <= 1):
        raise ValueError("invalid mass, accuracy or mean bound")
    source_error = tv_error/8
    qft_error = tv_error/2
    # Normalizing a projected vector costs at most 2*delta/sqrt(Z).
    conditioned_tv_upper = 4*source_error+qft_error
    herald_probability_lower = (Q(1, 2)-source_error)**2
    robust_threshold = threshold+2*score_error
    accepted_given_herald_lower = (
        (mean_lower-robust_threshold)/(1-robust_threshold)-conditioned_tv_upper
    )
    if accepted_given_herald_lower <= 0:
        raise ValueError("the error budget destroys the certified search probability")
    return {
        "target_score": str(threshold),
        "ideal_mean_lower": str(mean_lower),
        "source_state_norm_error_budget": str(source_error),
        "qft_operator_norm_error_budget": str(qft_error),
        "conditional_output_tv_upper": str(conditioned_tv_upper),
        "verifier_absolute_error": str(score_error),
        "robust_score_threshold": str(robust_threshold),
        "herald_probability_lower": str(herald_probability_lower),
        "accepted_given_herald_probability_lower": str(accepted_given_herald_lower),
        "accepted_per_trial_probability_lower": str(
            herald_probability_lower*accepted_given_herald_lower),
        "cost_model": "each rejected source preparation is a charged trial",
    }


def repetition_certificate(failure_bits):
    if type(failure_bits) is not int or failure_bits < 1:
        raise ValueError("positive integer failure exponent required")
    budget = error_budget()
    if not (Q(budget["herald_probability_lower"]) > Q(1, 8)
            and Q(budget["accepted_given_herald_probability_lower"]) > Q(1, 2000)):
        raise ArithmeticError("coarse joint success bound failed")
    return {
        "per_trial_success_lower": "1/16000",
        "trials_per_failure_bit": 16000,
        "failure_bits": failure_bits,
        "maximum_trials": 16000*failure_bits,
        "failure_probability_upper": str(Q(1, 2**failure_bits)),
        "argument": "(1-p)^r <= 1/(1+r*p) <= 1/2 for r=16000, p>=1/16000",
    }


def crt_character_label(parity, frequency, exponent):
    if type(exponent) is not int or exponent < 2:
        raise ValueError("integer modulus exponent at least two required")
    q = 3**(exponent-1)
    if type(parity) is not int or parity not in (0, 1):
        raise ValueError("canonical parity required")
    if type(frequency) is not int or not 0 <= frequency < q:
        raise ValueError("canonical ternary frequency required")
    return (q*parity+2*frequency) % (2*q)


def resource_structure(length, exponent, tv_error=Q(1, 10000)):
    if type(length) is not int or length < 1:
        raise ValueError("positive integer length required")
    if type(exponent) is not int or exponent < 2:
        raise ValueError("integer modulus exponent at least two required")
    if not isinstance(tv_error, Q) or not 0 < tv_error <= Q(1, 2):
        raise ValueError("positive rational accuracy at most one half required")
    trits = exponent-1
    qft_blocks = 1+trits+trits*(trits-1)//2
    return {
        "length": length,
        "modulus_bits": (3**exponent).bit_length(),
        "cyclic_order_bits": (2*3**trits).bit_length(),
        "source_local_qutrit_unitaries": length,
        "source_per_local_operator_error": str(tv_error/(8*length)),
        "qft_binary_hadamards": 1,
        "qft_ternary_fourier_blocks": trits,
        "qft_two_qutrit_controlled_phase_blocks": trits*(trits-1)//2,
        "qft_digit_reversal_swaps": trits//2,
        "qft_per_block_operator_error": str(tv_error/(2*qft_blocks)),
        "classical_public_preprocessing_bit_bound": "O(m*L^3), L=bit_length(3^k)",
        "reversible_arithmetic_bit_circuit_bound": "O((m+L)*L^2 + m*log(m))",
        "rotation_synthesis_overhead": "polylog((m+L)/epsilon) per fixed-dimension block",
        "arithmetic_model": "schoolbook integer arithmetic; reversible computation with saved history",
        "qft_primitive_counts_are_compiled_gate_counts": False,
        "concrete_qubit_or_T_count_claimed": False,
        "qft_domain_enumerated": False,
        "qft_implementation_source": "https://arxiv.org/abs/2003.03011",
    }


def score_interval(labels, centers, order, assignment, *, precision=96):
    """Exact residues first; interval cosine never receives rounded big integers."""
    if type(order) is not int or order < 2:
        raise ValueError("integer cyclic order at least two required")
    if (not labels or len(labels) != len(centers)
            or any(type(v) is not int or not 0 <= v < order
                   for v in (*labels, *centers))):
        raise ValueError("equally sized nonempty canonical integer labels and centers required")
    if type(assignment) is not int or not 0 <= assignment < order:
        raise ValueError("canonical integer assignment required")
    if type(precision) is not int or precision < 64:
        raise ValueError("interval precision must be an integer at least 64")
    with ctx.workprec(precision):
        total = arb(0)
        for label, center in zip(labels, centers):
            residue = (label*assignment-center) % order
            total += arb.cos_pi_fmpq(fmpq(2*residue, order))
        value = total/len(labels)
        if not value.is_finite():
            raise ArithmeticError("nonfinite score interval")
        return Q(str(value.lower().fmpq())), Q(str(value.upper().fmpq()))


def verify_score(labels, centers, order, assignment, *, score_error=Q(1, 100000)):
    if not isinstance(score_error, Q) or not 0 < score_error < Q(1, 10):
        raise ValueError("exact positive score error below one tenth required")
    precision = max(96, score_error.denominator.bit_length()+32)
    low, high = score_interval(labels, centers, order, assignment, precision=precision)
    if high-low > 2*score_error:
        raise ArithmeticError("score enclosure misses its declared precision budget")
    return {
        "score_lower": str(low), "score_upper": str(high),
        "threshold": "3/10", "precision_bits": precision,
        "accepted": low >= Q(3, 10),
        "threshold_overlap": low < Q(3, 10) <= high,
        "exact_modular_residues_used": True,
    }


def report():
    source_bytes = integer.REPORT.read_bytes()
    source = json.loads(source_bytes)
    producer_hash = hashlib.sha256(Path(integer.__file__).read_bytes()).hexdigest()
    if source["producer_sha256"] != producer_hash:
        raise ValueError("reproduce the source artifact before deriving a resource certificate")
    native = source["native"]
    budget = error_budget(
        mean_lower=Q(native["source_mean"]["mean_cosine_lower"]),
        retained_mass_lower=Q(native["source_mean"]["retained_source_mass_lower"]))
    return {
        "schema": "integer_character_uniform_v1",
        "status": "uniform_algorithm_argument_pending_independent_review_not_a_speedup",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_artifact_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "uniform_constants": uniform_constants(),
        "boundary_tail_bounds": tail_bounds(MIN_LENGTH),
        "uniform_error_budget": error_budget(),
        "uniform_repetition_certificate": repetition_certificate(20),
        "native_error_budget": budget,
        "native_resource_structure": resource_structure(
            native["length"], native["modulus_exponent"]),
        "quantum_optimizer_executed": False,
        "coherent_circuit_compiled": False,
        "kernel_checked_proof": False,
        "classical_hardness_or_speedup_proved": False,
        "blocked": ["independent proof and novelty review",
                    "matched structural classical attacks",
                    "meaningful external reduction",
                    "concrete reversible compiler and fault-tolerant resource estimate"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(args.output),
                      "uniform_minimum_length": MIN_LENGTH,
                      "uniform_mean_lower": str(MEAN_LOWER),
                      "coherent_circuit_compiled": False,
                      "speedup_claimed": False}))


if __name__ == "__main__":
    main()
