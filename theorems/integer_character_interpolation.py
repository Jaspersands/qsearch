"""Public prime-power character interpolation via bounded rational decoding.

The integer prime-product lattice is known (Ducas--Pierrot, 2018).
This source/readout application is a review-pending candidate, not a speedup.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import gcd, isqrt
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz
import numpy as np
from sympy import sieve

from theorems.balanced_signed_mpi import multinomial_box
from theorems.nonlinear_filter_pinning import enclose
from theorems.prime_character_finite_readout import sqrt_interval

REPORT = ROOT / "research/phase_workbench/integer_character_interpolation.json"


def prime_support(length):
    if type(length) is not int or length < 1:
        raise ValueError("positive support length required")
    return tuple(int(p) for p in sieve[1:length+2] if p != 3)


def validate_support(primes):
    if (not primes or any(type(p) is not int or p < 2 for p in primes)
            or len(set(primes)) != len(primes)
            or any(p == 3 or not fmpz(p).is_prime() for p in primes)):
        raise ValueError("distinct primes other than 3 required")


@lru_cache(maxsize=16)
def lifting_data(exponent):
    if type(exponent) is not int or exponent < 2:
        raise ValueError("modulus exponent must be an integer at least two")
    modulus, order = 3**exponent, 2*3**(exponent-1)
    if (pow(2, order, modulus) != 1 or pow(2, order//2, modulus) == 1
            or pow(2, order//3, modulus) == 1):
        raise ArithmeticError("generator 2 does not have the declared order")
    inverse_powers, power = [], pow(4, -1, modulus)
    for _ in range(exponent-1):
        inverse_powers.append(power)
        power = pow(power, 3, modulus)
    return modulus, order, tuple(inverse_powers)


def lifted_log(value, exponent):
    """Pohlig--Hellman specialized to 2*3^(k-1), without group enumeration."""
    modulus, order, inverses = lifting_data(exponent)
    if type(value) is not int or gcd(value, modulus) != 1:
        raise ValueError("integer unit modulo 3^k required")
    parity = int(value % 3 == 2)
    residual = value % modulus
    if parity:
        residual = residual*pow(2, -1, modulus) % modulus
    log4, place, updates = 0, 1, 0
    for inverse in inverses:
        scale = 3*place
        if (residual-1) % scale:
            raise ArithmeticError("ternary lifting invariant failed")
        digit = ((residual-1)//scale) % 3
        log4 += digit*place
        if digit:
            residual = residual*pow(inverse, digit, modulus) % modulus
            updates += 1
        place *= 3
    label = parity+2*log4
    if residual != 1 or not 0 <= label < order or pow(2, label, modulus) != value % modulus:
        raise ArithmeticError("public logarithm verification failed")
    return label, {"ternary_digits_processed": exponent-1,
                   "residual_modular_updates": updates,
                   "verification_exponentiations": 1}


def height_license(primes, cap, exponent, moment=1):
    validate_support(primes)
    if any(type(v) is not int or v < 0 for v in (cap, moment)):
        raise ValueError("nonnegative integer source and observable budgets required")
    modulus, order, _ = lifting_data(exponent)
    bound = max(primes)**(2*cap+moment)
    if modulus <= 2*bound:
        raise ValueError("modulus does not certify the rational height/readout bound")
    return {"cap_each_sign": cap, "observable_l1_budget": moment,
            "modulus_exponent": exponent, "modulus_bits": modulus.bit_length(),
            "cyclic_order_bits": order.bit_length(), "prime_bound": max(primes),
            "cross_product_height_bound": str(bound),
            "strict_guard": "3^k > 2*B^(2*cap+moment)",
            "strict_guard_verified": True}


def construct(primes, cap):
    validate_support(primes)
    if type(cap) is not int or cap < 0:
        raise ValueError("nonnegative integer cap required")
    exponent, modulus = 2, 9
    threshold = 2*max(primes)**(2*cap+1)
    while modulus <= threshold:
        exponent += 1
        modulus *= 3
    license_record = height_license(primes, cap, exponent)
    labels, updates = [], 0
    for p in primes:
        label, cost = lifted_log(p, exponent)
        labels.append(label)
        updates += cost["residual_modular_updates"]
    return {
        "primes": list(primes), "labels": labels, "exponent": exponent,
        "modulus": modulus, "order": 2*3**(exponent-1),
        "license": license_record,
        "preprocessing": {
            "method": "classical ternary digit lifting; exact public exponent verification",
            "ternary_digits_processed": len(primes)*(exponent-1),
            "residual_modular_updates": updates,
            "shared_inverse_power_cubings": exponent-1,
            "verification_exponentiations": len(primes),
            "integer_bits_upper": modulus.bit_length(),
            "full_group_table_used": False,
            "quantum_discrete_log_preprocessing_used": False,
        },
    }


def validate_public_labels(primes, labels, exponent):
    validate_support(primes)
    modulus, order, _ = lifting_data(exponent)
    if len(labels) != len(primes):
        raise ValueError("one explicit public label per prime required")
    if any(type(a) is not int or not 0 <= a < order or pow(2, a, modulus) != p % modulus
           for p, a in zip(primes, labels)):
        raise ValueError("invalid public logarithm label")


def rational_reconstruct(residue, modulus):
    """Standard Euclidean bounded rational reconstruction, using integer bounds."""
    if type(modulus) is not int or modulus < 3 or type(residue) is not int:
        raise ValueError("integer residue and modulus at least three required")
    bound = isqrt((modulus-1)//2)
    previous, current, t_previous, t_current = modulus, residue % modulus, 0, 1
    while current > bound:
        quotient, remainder = divmod(previous, current)
        previous, current = current, remainder
        t_previous, t_current = t_current, t_previous-quotient*t_current
    numerator, denominator = current, t_current
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    if (not 0 < denominator <= bound or abs(numerator) > bound
            or gcd(numerator, denominator) != 1 or gcd(denominator, modulus) != 1
            or (numerator-residue*denominator) % modulus):
        return None
    return Q(numerator, denominator)


def decode(primes, cap, exponent, observed):
    """Syndrome-only decoder; trial factors are the public prime support."""
    height_license(primes, cap, exponent, moment=0)
    modulus, order, _ = lifting_data(exponent)
    if type(observed) is not int or not 0 <= observed < order:
        raise ValueError("canonical integer syndrome required")
    ratio = rational_reconstruct(pow(2, observed, modulus), modulus)
    if ratio is None or ratio <= 0:
        return None
    numerator, denominator = ratio.numerator, ratio.denominator
    result, positive, negative = [], 0, 0
    for p in primes:
        plus = minus = 0
        while numerator % p == 0:
            numerator //= p
            plus += 1
        while denominator % p == 0:
            denominator //= p
            minus += 1
        value = plus-minus
        positive += plus
        negative += minus
        result.append(value)
    if (numerator != 1 or denominator != 1 or positive > cap or negative > cap
            or any(abs(value) > 1 for value in result)):
        return None
    return tuple(result)


def source_mean(length, cap, t):
    z = multinomial_box(length, cap, cap, t)
    edge = multinomial_box(length-1, cap-1, cap, t)
    low, high = sqrt_interval(2*t*(1-t), 192)
    mean_low = enclose(low*edge/z)
    return {"length": length, "cap_each_sign": cap, "active_probability": str(t),
            "retained_source_mass_lower": str(enclose(z)),
            "mean_cosine_lower": str(mean_low),
            "mean_cosine_upper": str(enclose(high*edge/z, upper=True)),
            "score_threshold": "3/10",
            "ideal_success_lower": str(enclose(max(Q(0), (mean_low-Q(3, 10))/Q(7, 10)))),
            "coherent_gate_and_precision_budget_complete": False}


def small_control(length):
    public = construct(prime_support(length), 1)
    labels, order = public["labels"], public["order"]
    if order > 10000:
        raise ValueError("target enumeration is a bounded validation control only")
    words = [word for word in product((-1, 0, 1), repeat=length)
             if word.count(1) <= 1 and word.count(-1) <= 1]
    syndrome = lambda y: sum(a*e for a, e in zip(labels, y)) % order
    images = {syndrome(y): y for y in words}
    if len(images) != len(words):
        raise ArithmeticError("licensed box collision")
    comparisons = 0
    for y in words:
        if decode(public["primes"], 1, public["exponent"], syndrome(y)) != y:
            raise ArithmeticError("small syndrome-only decoding failed")
        for i in range(length):
            for sign in (-1, 1):
                shifted = list(y)
                shifted[i] += sign
                other = images.get(syndrome(shifted))
                comparisons += 1
                if other is not None and tuple(shifted) != other:
                    raise ArithmeticError("licensed observable alias")
    t, centers = Q(1, 20), np.arange(length)*2
    x = np.arange(order, dtype=np.int64)
    residues = (x[:, None]*np.array(labels)-centers) % order
    amplitude = np.zeros(order, dtype=np.complex128)
    z = multinomial_box(length, 1, 1, t)
    for y in words:
        active = sum(bool(v) for v in y)
        coefficient = float((1-t)**(length-active)*(t/2)**active/z)**.5
        amplitude += coefficient*np.exp(2j*np.pi*(residues @ np.array(y) % order)/order)
    mass = abs(amplitude)**2
    return {"length": length, "order": order, "patterns_decoded": len(words),
            "observable_images_checked": comparisons,
            "target_norm": float(mass.mean()),
            "target_mean_cosine": float((mass*np.cos(2*np.pi*residues/order).mean(axis=1)).mean()),
            "source_mean": source_mean(length, 1, t),
            "scope": "finite identity validation, not an advantage experiment"}


def readout_alias_control():
    primes, exponent = (2, 5, 7), 3
    labels = tuple(lifted_log(p, exponent)[0] for p in primes)
    order = 18
    words = [y for y in product((-1, 0, 1), repeat=3)
             if y.count(1) <= 1 and y.count(-1) <= 1]
    syndrome = lambda y: sum(a*e for a, e in zip(labels, y)) % order
    shifted, other = (-2, 0, 0), (0, 0, 1)
    if len({syndrome(y) for y in words}) != len(words) or syndrome(shifted) != syndrome(other):
        raise ArithmeticError("unsafe readout countercontrol failed")
    return {"primes": list(primes), "exponent": exponent, "labels": list(labels),
            "source": [-1, 0, 0], "shifted": list(shifted), "alias": list(other),
            "box_injective": True, "readout_license_valid": False,
            "identity": "4*7 = 1 mod 27; a magnitude-two frequency aliases a source word"}


def native_control():
    length, cap, t = 1024, 35, Q(1, 20)
    public = construct(prime_support(length), cap)
    validate_public_labels(public["primes"], public["labels"], public["exponent"])
    rng = random.Random(201805733)
    locations = rng.sample(range(length), 2*cap)
    error = [0]*length
    for j, position in enumerate(locations):
        error[position] = 1 if j < cap else -1
    observed = sum(a*e for a, e in zip(public["labels"], error)) % public["order"]
    if decode(public["primes"], cap, public["exponent"], observed) != tuple(error):
        raise ArithmeticError("native signed rational reconstruction failed")
    outside = [int(i < cap+1) for i in range(length)]
    outside_syndrome = sum(a*e for a, e in zip(public["labels"], outside)) % public["order"]
    if decode(public["primes"], cap, public["exponent"], outside_syndrome) is not None:
        raise ArithmeticError("out-of-box control was accepted")
    return {
        "length": length, "cap_each_sign": cap, "public_primes": public["primes"],
        "public_labels_decimal": list(map(str, public["labels"])),
        "modulus_exponent": public["exponent"], "modulus_decimal": str(public["modulus"]),
        "cyclic_order_decimal": str(public["order"]), "license": public["license"],
        "preprocessing": public["preprocessing"],
        "public_labels_verified": True, "generator_prime_factors": [2, 3],
        "positive_positions": sorted(i for i, e in enumerate(error) if e == 1),
        "negative_positions": sorted(i for i, e in enumerate(error) if e == -1),
        "observed_syndrome_decimal": str(observed), "exact_recovery": True,
        "outside_positive_count": cap+1, "outside_control_rejected": True,
        "source_mean": source_mean(length, cap, t),
        "full_group_enumerated": False, "quantum_optimizer_executed": False,
        "native_classical_optimizer_executed": False,
    }


def report():
    return {
        "schema": "integer_character_interpolation_v1",
        "status": "constructive_public_input_candidate; independent_review_and_novelty_pending",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "known_integer_lattice_source": "https://doi.org/10.1007/s10623-018-0573-3",
        "native": native_control(), "small_controls": [small_control(m) for m in (3, 4)],
        "readout_alias_control": readout_alias_control(),
        "classical_hardness_or_quantum_speedup_proved": False,
        "blocked": ["matched p-adic/CRT/lattice optimization attacks",
                    "independent proof and novelty review",
                    "full coherent gate and precision budget",
                    "meaningful external hardness reduction"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    native = result["native"]
    print(json.dumps({"output": str(args.output),
                      "cyclic_order_bits": native["license"]["cyclic_order_bits"],
                      "signed_errors_decoded": 2*native["cap_each_sign"],
                      "mean_cosine_lower": float(Q(native["source_mean"]["mean_cosine_lower"])),
                      "full_group_table_used": False, "speedup_claimed": False}))


if __name__ == "__main__":
    main()
