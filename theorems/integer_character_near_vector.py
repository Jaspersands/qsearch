"""Guarded Fourier-to-near-vector reduction for an explicit dual lattice.

Review pending. This is absolute-distance search in one structured lattice
family, not approximate CVP for arbitrary lattices or a speedup claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import arb, ctx
import numpy as np

from theorems import integer_character_interpolation as integer
from theorems import integer_character_uniform as uniform
from theorems.balanced_signed_mpi import multinomial_box

REPORT = ROOT / "research/reductions/integer_character_near_vector.json"
GRID_THRESHOLD = Q(13, 200)


def construct(primes, cap, moment=16):
    integer.validate_support(primes)
    if (type(cap) is not int or cap < 1 or type(moment) is not int
            or moment < 2 or primes[0] != 2):
        raise ValueError("positive cap, at least two moments, and first prime 2 required")
    exponent, modulus = 2, 9
    threshold = 2*max(primes)**(2*cap+moment)
    while modulus <= threshold:
        exponent += 1
        modulus *= 3
    license_record = integer.height_license(primes, cap, exponent, moment)
    labels, updates = [], 0
    for p in primes:
        label, cost = integer.lifted_log(p, exponent)
        labels.append(label)
        updates += cost["residual_modular_updates"]
    if labels[0] != 1:
        raise ArithmeticError("the explicit dual basis requires a_1=1")
    return {
        "primes": list(primes), "labels": labels,
        "exponent": exponent, "modulus": modulus, "order": 2*3**(exponent-1),
        "license": license_record,
        "preprocessing": {
            "ternary_digit_steps": len(primes)*(exponent-1),
            "residual_modular_updates": updates,
            "construction_verification_exponentiations": len(primes),
            "shared_inverse_power_cubings": exponent-1,
            "exponential_group_table_used": False,
        },
    }


def distance_bound(first_mean_lower, second_mean_upper, moment):
    if (not isinstance(first_mean_lower, Q) or not isinstance(second_mean_upper, Q)
            or not 0 <= first_mean_lower <= 1 or not 0 <= second_mean_upper <= 1
            or type(moment) is not int or moment < 2):
        raise ValueError("rational moment bounds and an integer budget at least two required")
    coefficient = -first_mean_lower+second_mean_upper/4+Q(1, moment)
    # pi^2 is between 9 and 484/49; use the correct endpoint for the sign.
    denominator = Q(484, 49) if coefficient <= 0 else Q(9)
    bound = Q(1, 12)+coefficient/denominator
    if bound < 0:
        raise ValueError("these moment bounds imply an impossible negative squared distance")
    return {
        "first_cosine_mean_lower": str(first_mean_lower),
        "second_cosine_mean_upper": str(second_mean_upper),
        "licensed_moment_budget": moment,
        "coefficient_before_pi_squared_division": str(coefficient),
        "pi_squared_endpoint_used": str(denominator),
        "mean_normalized_squared_distance_upper": str(bound),
        "grid_distance_threshold": str(GRID_THRESHOLD),
        "ideal_grid_success_lower": str(max(Q(0), 1-bound/GRID_THRESHOLD)),
        "tail_argument": "sum_{j>J} 1/j^2 <= 1/J; no assumption about unlicensed harmonics",
    }


def source_moments(length, cap, t=Q(1, 20)):
    z = multinomial_box(length, cap, cap, t)
    both = multinomial_box(length-1, cap-1, cap-1, t)
    first = Q(integer.source_mean(length, cap, t)["mean_cosine_lower"])
    second = (t/2)*both/z
    return first, second


def uniform_certificate():
    uniform.uniform_constants()
    cert = distance_bound(uniform.MEAN_LOWER, Q(40, 1561), 16)
    bound = Q(cert["mean_normalized_squared_distance_upper"])
    conditional_success = 1-Q(3, 50)/GRID_THRESHOLD-Q(1, 10000)
    if not (bound < Q(3, 50) and conditional_success/8 > Q(1, 128)):
        raise ArithmeticError("uniform near-vector bound failed")
    with ctx.workprec(96):
        pi_squared = arb.pi()**2
        if not (pi_squared > 9 and pi_squared < arb(484)/49):
            raise ArithmeticError("pi enclosure failed")
    return {
        **cert,
        "minimum_length": uniform.MIN_LENGTH,
        "cap_rule": "floor(7*m/200)",
        "coarse_mean_square_upper": "3/50",
        "conditional_success_after_tv_error_lower": str(conditional_success),
        "charged_per_trial_success_lower": "1/128",
        "trials_per_failure_bit": 128,
        "arbitrary_rational_target_rms_radius": "13/50",
        "arbitrary_target_modulus_guard": "N >= 100",
        "radius_rounding_check": str((Q(13, 50)-Q(1, 200))**2),
        "pi_bounds_interval_checked": True,
        "relative_CVP_approximation_factor_claimed": False,
    }


def validate_labels(labels, order):
    if type(order) is not int or order < 2:
        raise ValueError("integer cyclic order at least two required")
    if (not labels or labels[0] != 1
            or any(type(a) is not int or not 0 <= a < order for a in labels)):
        raise ValueError("canonical integer labels with a_1=1 required")


def lattice_bases(labels, order):
    """Integer decoder basis and numerator basis for its exact rational dual."""
    validate_labels(labels, order)
    m = len(labels)
    decoder = [[order]+[0]*(m-1)]
    dual_numerator = [list(labels)]
    for i in range(1, m):
        row = [0]*m
        row[0], row[i] = -labels[i], 1
        decoder.append(row)
        row = [0]*m
        row[i] = order
        dual_numerator.append(row)
    return decoder, dual_numerator


def recover_assignment(labels, order, numerator):
    validate_labels(labels, order)
    if len(numerator) != len(labels) or any(type(v) is not int for v in numerator):
        raise ValueError("one exact integer numerator per coordinate required")
    assignment = numerator[0] % order
    if any((v-a*assignment) % order for a, v in zip(labels, numerator)):
        raise ValueError("vector is not in the declared dual lattice")
    return assignment


def witness(labels, centers, order, assignment):
    validate_labels(labels, order)
    if (len(centers) != len(labels)
            or any(type(c) is not int or not 0 <= c < order for c in centers)
            or type(assignment) is not int or not 0 <= assignment < order):
        raise ValueError("canonical integer centers and assignment required")
    # Ties at half a period are represented on the negative side.
    residues = [(a*assignment-c+order//2) % order-order//2
                for a, c in zip(labels, centers)]
    numerator = [c+r for c, r in zip(centers, residues)]
    if recover_assignment(labels, order, numerator) != assignment:
        raise ArithmeticError("lattice membership replay failed")
    distance = Q(sum(r*r for r in residues), len(labels)*order*order)
    return {
        "assignment": assignment, "numerator": numerator,
        "centered_residuals": residues, "mean_square": distance,
        "accepted": distance <= GRID_THRESHOLD,
    }


def rational_target_centers(target, order):
    if type(order) is not int or order < 2 or not target:
        raise ValueError("nonempty rational target and integer order required")
    if any(not isinstance(t, Q) for t in target):
        raise ValueError("exact rational target coordinates required")
    rounded = []
    for t in target:
        scaled = order*t
        rounded.append((2*scaled.numerator+scaled.denominator)//(2*scaled.denominator))
    centers = [b % order for b in rounded]
    translations = [(b-c)//order for b, c in zip(rounded, centers)]
    errors = [Q(b, order)-t for b, t in zip(rounded, target)]
    if any(abs(e) > Q(1, 2*order) for e in errors):
        raise ArithmeticError("target rounding exceeded its exact bound")
    return centers, translations, errors


def unsafe_cosine_control():
    # A legitimate residual vector can beat cosine 0.3 yet lose to uniform
    # rounding in squared distance. It is not a quantum distribution.
    return {
        "length": 50, "zero_residual_count": 33, "half_period_residual_count": 17,
        "mean_cosine": "8/25", "mean_square": "17/200",
        "continuous_uniform_mean_square": "1/12",
        "scope": "counterexample to inferring a distance bound from cosine alone",
    }


def higher_alias_control():
    public = integer.construct((2, 5, 7), 1)
    labels, order = public["labels"], public["order"]
    shifted, other = (0, 3, 1), (0, -1, 0)
    if sum(a*(u-v) for a, u, v in zip(labels, shifted, other)) % order:
        raise ArithmeticError("higher-harmonic alias control failed")
    integer.height_license((2, 5, 7), 1, public["exponent"], moment=1)
    return {
        "modulus": public["modulus"], "order": order, "labels": labels,
        "source": [0, 0, 1], "shifted_by_three_at_index_one": list(shifted),
        "alias": list(other), "first_moment_height_guard_valid": True,
        "third_harmonic_alias_present": True,
        "integer_identity": "5^4*7 = 1 + 6*729",
    }


def small_control(moment):
    public = construct((2, 5), 1, moment)
    labels, order = public["labels"], public["order"]
    if order > 50000:
        raise ValueError("enumeration is restricted to bounded identity controls")
    words = [y for y in product((-1, 0, 1), repeat=2)
             if y.count(1) <= 1 and y.count(-1) <= 1]
    centers = np.array([2, 5])
    residues = (np.arange(order)[:, None]*np.array(labels)-centers) % order
    t, z = Q(1, 20), multinomial_box(2, 1, 1, Q(1, 20))
    amplitude = np.zeros(order, dtype=np.complex128)
    for y in words:
        active = sum(bool(v) for v in y)
        weight = float((1-t)**(2-active)*(t/2)**active/z)**.5
        amplitude += weight*np.exp(2j*np.pi*(residues @ np.array(y) % order)/order)
    probability = abs(amplitude)**2/order
    moments = [float(probability @ np.cos(2*np.pi*j*residues/order).mean(axis=1))
               for j in range(1, moment+1)]
    centered = (residues+order//2) % order-order//2
    mean_square = float(probability @ ((centered/order)**2).mean(axis=1))
    first, second = source_moments(2, 1)
    return {
        "length": 2, "moment_budget": moment, "order": order,
        "target_norm": float(probability.sum()), "target_cosine_moments": moments,
        "source_first_mean_lower": str(first), "source_second_mean": str(second),
        "target_mean_square": mean_square,
        "distance_bound": distance_bound(first, second, moment),
        "scope": "finite identity control, not an optimizer or advantage experiment",
    }


def native_control():
    m, cap, moment = 1024, 35, 16
    public = construct(integer.prime_support(m), cap, moment)
    integer.validate_public_labels(public["primes"], public["labels"], public["exponent"])
    rng = random.Random(2026102016)
    centers = [rng.randrange(public["order"]) for _ in range(m)]
    base = witness(public["labels"], centers, public["order"], 0)
    first, second = source_moments(m, cap)
    original_bytes = integer.REPORT.read_bytes()
    original = json.loads(original_bytes)["native"]
    if original["public_primes"] != public["primes"] or original["cap_each_sign"] != cap:
        raise ValueError("the native source control no longer matches")
    positive, negative = original["positive_positions"], original["negative_positions"]
    if (len(positive) != cap or len(negative) != cap
            or len(set(positive+negative)) != 2*cap
            or any(type(i) is not int or not 0 <= i < m for i in positive+negative)):
        raise ValueError("invalid saved native signed pattern")
    error = [0]*m
    for position in positive:
        error[position] = 1
    for position in negative:
        error[position] = -1
    syndrome = sum(a*y for a, y in zip(public["labels"], error)) % public["order"]
    if integer.decode(public["primes"], cap, public["exponent"], syndrome) != tuple(error):
        raise ArithmeticError("stronger-modulus syndrome-only decode failed")
    try:
        integer.height_license(public["primes"], cap, original["modulus_exponent"], moment)
    except ValueError:
        old_modulus_licensed = False
    else:
        old_modulus_licensed = True
    return {
        "length": m, "cap_each_sign": cap, "moment_budget": moment,
        "public_primes": public["primes"],
        "public_labels_decimal": list(map(str, public["labels"])),
        "modulus_exponent": public["exponent"],
        "modulus_decimal": str(public["modulus"]),
        "cyclic_order_decimal": str(public["order"]),
        "license": public["license"], "preprocessing": public["preprocessing"],
        "independent_label_replay_exponentiations": m,
        "center_seed": 2026102016, "centers_decimal": list(map(str, centers)),
        "source_control_artifact_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "positive_positions": positive, "negative_positions": negative,
        "syndrome_only_errors_decoded": sum(bool(y) for y in error),
        "observed_syndrome_decimal": str(syndrome),
        "distance_bound": distance_bound(first, second, moment),
        "old_cosine_modulus_covers_sixteen_moments": old_modulus_licensed,
        "zero_assignment_validation_control": {
            "mean_square": str(base["mean_square"]),
            "meets_grid_threshold": base["accepted"],
            "scope": "integer-rounding control; not a serious classical portfolio",
        },
        "native_quantum_optimizer_executed": False,
        "native_classical_optimizer_executed": False,
    }


def report():
    return {
        "schema": "integer_character_near_vector_v1",
        "status": "structured_absolute_near_vector_reduction_pending_review",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependencies_sha256": {
            name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            for name, module in (("integer_character_interpolation", integer),
                                 ("integer_character_uniform", uniform))
        },
        "uniform_certificate": uniform_certificate(),
        "native": native_control(),
        "small_controls": [small_control(j) for j in (2, 4)],
        "unsafe_cosine_control": unsafe_cosine_control(),
        "higher_alias_control": higher_alias_control(),
        "general_lattice_hardness_reduction": False,
        "relative_CVP_approximation_factor": None,
        "classical_speedup_separation": False,
        "blocked": ["strong matched classical lattice and p-adic attacks",
                    "independent proof and novelty review against quantum transference",
                    "a hardness or application reduction beyond this explicit lattice family",
                    "concrete coherent compilation and fault-tolerant resources"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    native = result["native"]
    print(json.dumps({
        "output": str(args.output),
        "native_order_bits": native["license"]["cyclic_order_bits"],
        "native_mean_square_upper": float(Q(
            native["distance_bound"]["mean_normalized_squared_distance_upper"])),
        "old_cosine_modulus_covers_sixteen_moments": native[
            "old_cosine_modulus_covers_sixteen_moments"],
        "speedup_claimed": False,
    }))


if __name__ == "__main__":
    main()
