"""Copy-only approximate even-level native input from independent noisy values.

Known local gate recipes, not an efficient receiver or a hardware compiler.
The source promises and every rounding/preparation error remain explicit.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random

from flint import fmpq, fmpq_poly
import numpy as np

from ternary_certified_noise_sampler import pi_box, rational, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord, gaussian_rounding_loss
from native_recovery_capacity import copy_recovery_capacity

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_NOISY_PHASE_INPUT.md"
REPORT = ROOT / "research/reductions/native_noisy_phase_input.json"


def even_frequency_matrix(digits):
    integer(digits, "positive ternary root exponent", 1)
    # MPI^2=-3Z, so q*beta advances by T=-Z^-1; T^3=-I,T^6=I.
    u, v = -1, 1
    for _ in range((digits-1) % 6):
        u, v = u+v, -u
    if u*u+u*v+v*v != 1:
        raise ArithmeticError("even native frequency map lost unimodularity")
    return ((u, v), (u+v, -u))


def native_labels(first, second, q):
    digits = root_digits(q)
    first, second = tuple(first), tuple(second)
    if not first or len(first) != len(second) or any(
            type(x) is not int or not 0 <= x < q for x in first+second):
        raise ValueError("equal nonempty canonical native frequencies required")
    (u, v), (w, z) = even_frequency_matrix(digits)
    # det=-1; the inverse is integral at EVERY root, not a finite lookup.
    return tuple(((-z*a+v*c) % q, (w*a-u*c) % q) for a, c in zip(first, second))


def angle_recipe(q, phase, bits):
    root_digits(q)
    integer(bits, "positive local gate precision", 1)
    if type(phase) is not int or not 0 <= phase < q:
        raise ValueError("canonical known phase numerator required")
    centered = phase if 2*phase < q else phase-q
    a, b, _ = pi_box(bits)
    lower, upper = sorted((2*fmpq(centered, q)*a, 2*fmpq(centered, q)*b))
    midpoint, scale = (lower+upper)/2, 2**(bits+2)
    x = midpoint*scale+fmpq(1, 2)
    dyadic = fmpq(int(x.numerator)//int(x.denominator), scale)
    error = max(abs(dyadic-lower), abs(dyadic-upper))
    if error > fmpq(1, 2**bits):
        raise ArithmeticError("known phase compiler exceeded its angle budget")
    return {"phase_numerator": phase, "centered_numerator": centered,
            "precision_bits": bits, "angle_lower": str(lower), "angle_upper": str(upper),
            "dyadic_radian_angle": str(dyadic), "angle_error_upper": str(error),
            "diagonal_operator_error_upper": str(error),
            "angle_description_is_hardware_synthesis": False}


def gate_budget(records, failure_bits):
    integer(records, "positive native input count", 1)
    integer(failure_bits, "positive failure bits", 1)
    bits = failure_bits+(2*records-1).bit_length()
    per_state = fmpq(2, 2**bits)
    return {"failure_bits": failure_bits, "local_gate_precision_bits": bits,
            "F3_operator_error_promise_upper": str(fmpq(1, 2**bits)),
            "known_diagonal_operator_error_budget_upper": str(fmpq(1, 2**bits)),
            "per_state_preparation_trace_error_upper": str(min(fmpq(1), per_state)),
            "M_state_preparation_trace_error_upper": str(min(fmpq(1), records*per_state)),
            "universal_gate_synthesis_implemented": False}


def quantum_input_bound(q, records, second_moment, failure_bits=64):
    root_digits(q)
    integer(records, "positive independent native input count", 1)
    V = rational(second_moment, "public integer error moment")
    if V < 0:
        raise ValueError("nonnegative true public error moment required")
    budget = gate_budget(records, failure_bits)
    per_state = min(fmpq(1), 20*V/(q*q))
    total = min(fmpq(1), records*per_state+rational(
        budget["M_state_preparation_trace_error_upper"], "gate loss"))
    return {"source_integer_second_moment_upper": str(V),
            "per_state_averaged_trace_distance_upper": str(per_state),
            "M_state_success_loss_before_source_rounding_upper": str(total),
            "bound_is_nonvacuous": total < 1, "gate_budget": budget,
            "input_classical_originals_required": 2*records,
            "independent_native_qutrits_supplied_in_gate_model": records,
            "assumptions": ["same unknown integer-vector secret", "IID uniform full-root labels",
                            "independent symmetric source errors", "true public second-moment bound",
                            "independent original pair per state", "copy-only receiver",
                            "F3 implementation satisfies charged operator error"],
            "promises_inferred_from_sample_values": False,
            "individual_pure_realization_has_this_noise_bound": False,
            "postselection_erases_global_error": False, "ideal_source_inverse_supplied": False,
            "efficient_receiver_supplied": False, "hardness_transfer_admitted": False}


def trace_distance_box(phi, bits=64):
    phi = rational(phi, "symmetric characteristic value")
    if not -1 <= phi <= 1:
        raise ValueError("real characteristic value must lie in[-1,1]")
    x = 1+phi
    lo, hi = sqrt_box(x*x+8, bits)
    return (1-phi)*(x+lo)/6, (1-phi)*(x+hi)/6


@dataclass(frozen=True)
class ReceiverInput:
    modulus: int
    level: int
    ring_labels: tuple
    first_frequency: tuple
    second_frequency: tuple
    state_handle: str

    def public(self):
        return {"modulus": self.modulus, "level": self.level, "ring_labels": self.ring_labels,
                "first_frequency": self.first_frequency, "second_frequency": self.second_frequency,
                "state_handle": self.state_handle, "access": "one supplied qutrit, copy-only"}


@dataclass(frozen=True)
class PreparedInputBatch:
    receiver_inputs: tuple
    reduction_side_mask: tuple
    reduction_side_recipes: tuple
    source_ancestry: tuple
    bound: dict

    def receiver_view(self):
        # Gate descriptions and noisy values stay OUTSIDE the receiver interface.
        return tuple(s.public() for s in self.receiver_inputs)

    def diagnostic(self):
        return {"receiver_inputs": self.receiver_view(), "reduction_side_mask": self.reduction_side_mask,
                "reduction_side_recipes": self.reduction_side_recipes,
                "source_ancestry": self.source_ancestry, "bound": self.bound,
                "status": "CONDITIONAL_COPY_ONLY_GATE_RECIPE_NOT_HARDWARE_EXECUTION",
                "quantum_hardware_states_executed": 0, "efficient_receiver_supplied": False,
                "ideal_unknown_state_inverse_supplied": False, "accepted_speedup_candidate": False}


def checked_source_bank(samples, mask):
    samples, mask = tuple(samples), tuple(mask)
    if not samples or len(samples) % 2 or any(not isinstance(s, NoisyLinearRecord) for s in samples):
        raise ValueError("nonempty even independent classical source records required")
    q, n = samples[0].modulus, len(samples[0].label)
    if any(s.modulus != q or len(s.label) != n for s in samples):
        raise ValueError("shared full-root modulus and dimension required")
    if len({s.source_id for s in samples}) != len(samples):
        raise ValueError("one independent original pair is charged per native qutrit")
    if len(mask) != n or any(type(x) is not int or not 0 <= x < q for x in mask):
        raise ValueError("canonical reduction-side mask required; uniformity is a source promise")
    return samples, mask, q, n


def prepare_inputs(samples, mask, second_moment, failure_bits=64):
    samples, mask, q, _ = checked_source_bank(samples, mask)
    bound = quantum_input_bound(q, len(samples)//2, second_moment, failure_bits)
    bits = bound["gate_budget"]["local_gate_precision_bits"]
    receivers, recipes, ancestry = [], [], []
    for j, (a, c) in enumerate(zip(samples[::2], samples[1::2])):
        values = tuple((s.value+sum(x*y for x, y in zip(s.label, mask))) % q for s in (a, c))
        labels = native_labels(a.label, c.label, q)
        receivers.append(ReceiverInput(q, 2*root_digits(q), labels, a.label, c.label, f"qutrit-{j}"))
        recipes.append({"state_handle": f"qutrit-{j}", "known_phase_values": values,
                        "initialize": "|0>", "gate_order": ["F3", "diag(1,exp(i*angle_b),exp(i*angle_d))"],
                        "angles": tuple(angle_recipe(q, x, bits) for x in values),
                        "F3_operator_error_promise_upper": bound["gate_budget"]["F3_operator_error_promise_upper"],
                        "secret_or_errors_as_preparation_inputs": False,
                        "hardware_synthesized": False})
        ancestry.append((a.source_id, c.source_id))
    return PreparedInputBatch(tuple(receivers), mask, tuple(recipes), tuple(ancestry), bound)


def rounded_gaussian_quantum_profile(n, q, alpha, records, failure_bits=64):
    integer(n, "positive source dimension", 1)
    integer(records, "positive native input count", 1)
    root_digits(q)
    alpha = rational(alpha, "continuous Gaussian alpha")
    if not 0 < alpha < 1:
        raise ValueError("source alpha must lie in(0,1)")
    V = q*q*alpha*alpha/3+fmpq(1, 2)
    source_guard, classical_guard = (alpha*q)**2 >= 4*n, q*q >= 2**n
    bound = quantum_input_bound(q, records, V, failure_bits)
    precision = q.bit_length()+records.bit_length()+failure_bits+3
    rounding = gaussian_rounding_loss(q, alpha, records, fmpq(1, 2**precision))
    total = min(fmpq(1), rational(bound["M_state_success_loss_before_source_rounding_upper"], "input loss")
                +rational(rounding["two_M_input_rounding_abort_union_upper"], "rounding loss"))
    return {"dimension": n, "modulus": q, "alpha": str(alpha), "native_inputs": records,
            "source_theorem": "Brakerski et al.2013 Theorem2.16 (search LWE)",
            "source_url": "https://arxiv.org/html/1306.0281",
            "source_error_law": "continuous D_alpha on torus, scaled then nearest-integer rounded",
            "Gaussian_width_is_standard_deviation": False,
            "published_quantum_worst_case_source_parameter_guard": source_guard,
            "published_classical_worst_case_source_parameter_guard": source_guard and classical_guard,
            "source_rounding_precision_bits": precision, "source_rounding_loss": rounding,
            "conditional_quantum_input_bound": bound, "composed_success_loss_upper": str(total),
            "full_recovery_capacity": copy_recovery_capacity(n, q, records),
            "nonvacuous_noise_bound_is_full_recovery_feasibility": False,
            "hardness_transfer_admitted": False, "general_full_ring_secret_covered": False,
            "remaining_debt": ["external composition and novelty review",
                               "source oracle supplies containing intervals at charged precision",
                               "uniform secret mask and independent source law promises",
                               "efficient copy-only native receiver with explicit M and success",
                               "F3/phase compilation in the selected physical gate model"]}


def finite_density_control(q):
    root_digits(q)
    if q > 81:
        raise ValueError("exact finite density replay is capped at q81, not the scalable recipe")
    coefficients = [0]*(2*q//3+1)
    coefficients[0] = coefficients[q//3] = coefficients[2*q//3] = 1
    modulus = fmpq_poly(coefficients)
    omega = fmpq_poly([0, 1])
    power = lambda k: (omega**(k % q)) % modulus
    encode = lambda a: [str(a[i]) for i in range(len(a)-1, -1, -1)]
    chi = ((-1, fmpq(1, 4)), (0, fmpq(1, 2)), (1, fmpq(1, 4)))
    phi = (1+(power(1)+power(-1))/2)/2
    density = [[fmpq_poly() for _ in range(3)] for _ in range(3)]
    for e, p in chi:
        for f, weight in chi:
            phases = (0, e, f)
            for i in range(3):
                for j in range(3):
                    density[i][j] += p*weight*power(phases[i]-phases[j])/3
    expected = [[fmpq_poly([fmpq(1, 3)]), phi/3, phi/3],
                [phi/3, fmpq_poly([fmpq(1, 3)]), (phi*phi % modulus)/3],
                [phi/3, (phi*phi % modulus)/3, fmpq_poly([fmpq(1, 3)])]]
    if density != expected:
        raise ArithmeticError("finite error-averaged density did not match independent source law")
    value = (1+math.cos(2*math.pi/q))/2
    matrix = np.array([[1, value, value], [value, 1, value*value], [value, value*value, 1]])/3
    distance = float(sum(abs(np.linalg.eigvalsh(matrix-np.ones((3, 3))/3)))/2)
    return {"modulus": q, "error_law": [[e, str(p)] for e, p in chi],
            "characteristic_phi_exact": encode(phi),
            "averaged_phase_frame_density_exact": [[encode(a) for a in row] for row in density],
            "numerical_trace_distance_diagnostic": distance,
            "moment_trace_distance_upper": str(min(fmpq(1), fmpq(10, q*q))),
            "numeric_diagnostic_is_certificate": False, "calibration_is_LWE_hardness_source": False}


def calibration(n, digits, count, seed):
    q, rng = 3**digits, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    samples, errors = [], []
    for i in range(2*count):
        label = tuple(rng.randrange(q) for _ in range(n))
        error = (-1, 0, 0, 1)[rng.randrange(4)]
        errors.append(error)
        samples.append(NoisyLinearRecord(label, (sum(a*s for a, s in zip(label, secret))+error) % q,
                                         q, f"noisy-phase-{seed}-source-{i}"))
    mask = tuple(rng.randrange(q) for _ in range(n))
    batch = prepare_inputs(samples, mask, "1/2")
    return {"dimension": n, "root_digits": digits, "native_inputs": count, "seed": seed,
            "calibration_secret": secret, "source_error_diagnostics": errors,
            "source_records": tuple(s.public() for s in samples), "batch": batch.diagnostic(),
            "calibration_is_LWE_hardness_source": False}


def build_report():
    rational_controls = []
    for phi in ("-1", "-1/2", "0", "1/4", "1/2", "999/1000", "1"):
        lo, hi = trace_distance_box(phi)
        rational_controls.append({"phi": phi, "trace_distance_lower": str(lo), "trace_distance_upper": str(hi),
                                  "one_minus_phi_upper": str(1-rational(phi, "phi")), "bits": 64})
    return {"status": "CONDITIONAL_COPY_ONLY_NOISY_PHASE_INPUT_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": [calibration(4, d, 8, 130000+d) for d in (1, 2, 16, 80, 300)],
            "exact_density_controls": [finite_density_control(q) for q in (3, 9, 27, 81)],
            "rational_trace_controls": rational_controls,
            "source_profiles": [rounded_gaussian_quantum_profile(64, q, a, 512) for q, a in
                                ((3**16, "1/1048576"), (3**64, "1/1048576"), (9, "1/1048576"), (3**16, "1/2"))],
            "shared_pair_countercontrol": {"modulus": 3, "phi_one": "1/4", "phi_two": "1/4",
                "reused_coherence_entry": "1/36", "independent_coherence_entry": "1/144",
                "entry_difference": "1/48", "same_pair_yields_IID_originals": False},
            "gate_model": "known qutrit F3 and two diagonal phases with charged operator error",
            "quantum_hardware_states_executed": 0, "efficient_native_receiver_supplied": False,
            "hardness_transfer_admitted": False, "accepted_speedup_candidate": False,
            "ideal_unknown_source_inverse_supplied": False, "arbitrary_full_ring_secrets_covered": False,
            "odd_levels_covered": False, "polynomial_input_recipe_not_polynomial_decoder": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "classical_originals": 80, "native_gate_recipes": 40,
                      "exact_density_entries": 36, "hardware_states_executed": 0,
                      "hardness_transfer_admitted": False}, indent=2))


if __name__ == "__main__":
    main()
