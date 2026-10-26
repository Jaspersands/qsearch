"""Verified scalar Fermat witnesses for public Rees moment designs.

Known finite-field arithmetic, not a many-equation SDE solver. At large p,
a Weil-bound argument gives success >=1/(2d) per independent random trial.
The only field enumeration is guarded by p<16(d-1)^4, polynomial in d.
FLINT root finding remains an expected-time, not locally clocked dependency.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import gcd
from pathlib import Path
import random

from flint import fmpz_mod_poly_ctx

from theorems.prime_character_opi import ring


def _parameters(p, degree):
    ring(p)
    if type(degree) is not int or not 1 <= degree < p:
        raise ValueError("positive degree strictly below the odd prime required")


def verify_fermat_witness(p, degree, weights):
    _parameters(p, degree)
    if (not 1 <= len(weights) <= degree+1 or not any(weights)
            or any(type(x) is not int or not 0 <= x < p for x in weights)):
        raise ValueError("nonzero canonical scalar row of length <=d+1 required")
    if sum(pow(x, degree, p) for x in weights) % p:
        raise ArithmeticError("scalar Fermat equation does not vanish")


def large_field_regime(p, degree):
    _parameters(p, degree)
    return degree >= 2 and p**(degree-1) >= 16*(degree-1)**(2*degree+2)


def fermat_trial_cap(degree, failure):
    """Conservative sampling cap from exact error data; not a root clock."""
    if type(degree) is not int or degree < 1 or not isinstance(failure, Fraction) or not 0 < failure < 1:
        raise ValueError("positive degree and exact failure allowance in (0,1) required")
    inverse_ceiling = (failure.denominator+failure.numerator-1)//failure.numerator
    bits = (inverse_ceiling-1).bit_length()
    return 2*degree*bits


@dataclass(frozen=True)
class FermatWitness:
    p: int
    degree: int
    weights: tuple[int, ...]
    method: str
    trials: int = 0
    root_calls: int = 0
    enumerated_field_elements: int = 0
    success_probability_lower_bound: Fraction = Fraction(1)
    capped_abort_bound: Fraction = Fraction(0)
    root_runtime_locally_clocked: bool = False


def _small_field_witness(p, degree):
    if large_field_regime(p, degree) or not p < 16*(degree-1)**4:
        raise ValueError("field enumeration is allowed only in the proved degree-bounded regime")
    roots = {}
    for x in range(p):
        roots.setdefault(pow(x, degree, p), x)
    # Fix the first coordinate to 1. Existence follows by permuting/scaling
    # any nonzero homogeneous solution; all coefficients here equal one.
    levels = [{0: None}]
    target = p-1
    for _ in range(degree):
        current = {}
        for before in levels[-1]:
            for power, root in roots.items():
                after = (before+power) % p
                current.setdefault(after, (before, root))
                if after == target:
                    break
            if target in current:
                break
        levels.append(current)
        if target in current:
            recovered, value = [], target
            for level in reversed(levels[1:]):
                value, root = level[value]
                recovered.append(root)
            return (1,)+tuple(reversed(recovered))+(0,)*(degree-len(recovered))
    raise ArithmeticError("bounded dynamic program contradicted Fermat existence")


def _field_root(p, degree, value):
    found = fmpz_mod_poly_ctx(p)([-value]+[0]*(degree-1)+[1]).roots()
    if not found:
        raise ArithmeticError("root backend missed a certified power residue")
    root = min(int(item[0]) for item in found)
    if not 0 <= root < p or pow(root, degree, p) != value:
        raise ArithmeticError("invalid root returned by the arithmetic backend")
    return root


def scalar_fermat_witness(p, degree, *, max_trials=128, rng=None):
    """Find a nonzero row with sum(x**degree)=0; no hidden input is accepted.

    The cap bounds random sampling, not FLINT's internal runtime. Abort
    guarantees require independent uniform randomness; seeded runs only
    reproduce fixtures. All accepted witnesses are checked exactly.
    """
    _parameters(p, degree)
    if type(max_trials) is not int or max_trials < 1:
        raise ValueError("positive random-attempt cap required")
    if degree % 2:
        weights = (1, p-1)
        verify_fermat_witness(p, degree, weights)
        return FermatWitness(p, degree, weights, "odd_degree_pair")
    if not large_field_regime(p, degree):
        weights = _small_field_witness(p, degree)
        verify_fermat_witness(p, degree, weights)
        return FermatWitness(p, degree, weights, "degree_bounded_dynamic_program",
                             enumerated_field_elements=p)
    rng = random.SystemRandom() if rng is None else rng
    power_index = gcd(degree, p-1)
    for trial in range(1, max_trials+1):
        prefix = tuple(rng.randrange(p) for _ in range(degree))
        if any(type(x) is not int or not 0 <= x < p for x in prefix):
            raise ValueError("random source returned a noncanonical field element")
        if not any(prefix):
            continue
        value = -sum(pow(x, degree, p) for x in prefix) % p
        if value and pow(value, (p-1)//power_index, p) != 1:
            continue
        root = _field_root(p, degree, value) if value else 0
        weights = prefix+(root,)
        verify_fermat_witness(p, degree, weights)
        return FermatWitness(p, degree, weights, "weil_certified_random_root", trial, int(bool(value)),
                             0, Fraction(1, 2*degree), Fraction(2*degree-1, 2*degree)**max_trials)
    raise RuntimeError("capped scalar Fermat sampling aborted; no witness accepted")


def build_report():
    records = []
    for p, degree in ((13, 4), (101, 4), (257, 6), (2**128-275, 4), (2**128-275, 8)):
        witness = scalar_fermat_witness(p, degree, rng=random.Random(20261022))
        records.append({"p": p, "degree": degree, "weights": witness.weights, "method": witness.method,
                        "trials": witness.trials, "root_calls": witness.root_calls,
                        "enumerated_field_elements": witness.enumerated_field_elements,
                        "success_probability_lower_bound": str(witness.success_probability_lower_bound),
                        "capped_abort_bound": str(witness.capped_abort_bound),
                        "root_runtime_locally_clocked": witness.root_runtime_locally_clocked})
    return {"status": "KNOWN_SCALAR_FERMAT_BACKEND_IMPLEMENTED", "controls": records,
            "large_prime_enumeration": False, "general_many_equation_sde_implemented": False,
            "quantum_receiver_implemented": False, "novelty_established": False, "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build_report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/scalar_fermat_solver.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
