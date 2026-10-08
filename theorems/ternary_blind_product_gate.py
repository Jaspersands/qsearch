"""Label-independent product POVM copy gate, including opposite secrets.

LOCAL DERIVATION / REVIEW PENDING. Arbitrary classical processing is covered;
label-dependent and adaptive quantum measurements are explicitly NOT covered.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
import sympy as sp

from ternary_product_trine import fixed_trine_gate

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/classical_baselines/ternary_blind_product_gate.json"
OMEGA = (-1+sp.sqrt(3)*sp.I)/2


def _integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def _rational(x):
    x = sp.simplify(x)
    if x.is_Rational is not True:
        raise ValueError("control requires exact rational scalar invariants")
    return Fraction(int(sp.numer(x)), int(sp.denom(x)))


def effects_invariants(effects):
    """Exact finite controls; reject unproved PSD or unresolved scalars."""
    effects = tuple(sp.Matrix(e) for e in effects)
    if not effects or any(e.shape != (3, 3) for e in effects):
        raise ValueError("nonempty qutrit POVM required")
    total = sp.zeros(3)
    d, eta, zero = sp.S.Zero, sp.S.Zero, sp.S.Zero
    for e in effects:
        if (e.applyfunc(sp.conjugate).T-e).applyfunc(sp.simplify) != sp.zeros(3):
            raise ValueError("Hermitian effects required")
        for k in (1, 2, 3):
            for indices in combinations(range(3), k):
                if sp.simplify(e.extract(indices, indices).det()).is_nonnegative is not True:
                    raise ValueError("all principal minors must be certified nonnegative")
        tr = sp.simplify(sp.trace(e))
        if tr.is_positive is not True:
            raise ValueError("omit null effects; positive trace required")
        off = [(i, j) for i in range(3) for j in range(3) if i != j]
        d += sum(e[i, j]*sp.conjugate(e[i, j]) for i, j in off)/(3*tr)
        eta += sum(e[i, j]**2 for i, j in off)/(3*tr)
        zero += (sum(e)-tr)**2/(3*tr)
        total += e
    if total.applyfunc(sp.simplify) != sp.eye(3):
        raise ValueError("POVM must sum exactly to identity")
    d, eta, zero = map(_rational, (d, eta, zero))
    if not 0 <= d <= Fraction(2, 3) or abs(eta) > d or not 0 <= zero <= 2:
        raise ArithmeticError("positive POVM violates derived invariant bounds")
    return {"nonzero_diagonal": d, "opposite_nonzero_secret_Gram": eta,
            "zero_diagonal": zero, "exact_PSD_and_completeness_certified": True}


def blind_product_gate(n, digits, samples, desired_advantage=Fraction(1, 10)):
    result = fixed_trine_gate(n, digits, samples, desired_advantage)
    G = 3**(n*digits)
    d = Fraction(5, 3)**samples-1
    squared = d/G
    zero = Fraction(result["zero_secret_advantage_upper"])
    eps = Fraction(desired_advantage)
    return {"dimension": n, "digits": digits, "original_independent_qutrits": samples,
            "nonzero_Gram_operator_norm_upper": str(2*d),
            "nonzero_contribution_advantage_upper_squared": str(squared),
            "zero_secret_advantage_upper": str(zero), "requested_advantage": str(eps),
            "necessary_copy_gate_passed": eps <= zero or squared >= (eps-zero)**2,
            "scope": "arbitrary fixed label-independent single-qutrit POVMs followed by ANY joint classical processing; IID full labels; ALL uniform secrets",
            "different_POVM_per_original_copy_covered": True,
            "shared_independent_public_measurement_randomness_covered": True,
            "opposite_secret_correlations_kept": True,
            "label_dependent_quantum_measurements_covered": False,
            "outcome_adaptive_quantum_measurements_covered": False,
            "collective_quantum_measurements_covered": False,
            "chosen_labels_or_retained_sieve_law_covered": False,
            "speedup_claim_allowed": False, "status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def invariant_product_gate(invariants, n, digits):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    diag, opposite = Fraction(1), Fraction(1)
    for inv in invariants:
        d, eta = Fraction(inv["nonzero_diagonal"]), Fraction(inv["opposite_nonzero_secret_Gram"])
        if not 0 <= d <= Fraction(2, 3) or abs(eta) > d:
            raise ValueError("lawful invariant range required")
        diag *= 1+d; opposite *= 1+eta
    diag -= 1; opposite -= 1
    operator = diag+abs(opposite)
    return {"nonzero_product_diagonal": str(diag), "opposite_product_entry": str(opposite),
            "nonzero_Gram_operator_norm": str(operator),
            "nonzero_contribution_advantage_upper_squared": str(operator/(2*3**(n*digits))),
            "invariant_inputs_are_assumptions_unless_POVM_certified": True}


def example_povms():
    computational = [sp.diag(*[int(i == j) for j in range(3)]) for i in range(3)]
    fourier = [sp.Matrix(3, 3, lambda i, j: sp.simplify(OMEGA**((i-j)*z % 3)/3)) for z in range(3)]
    real_pair = [sp.Matrix([[sp.Rational(1, 2), sign*sp.Rational(1, 2), 0],
                           [sign*sp.Rational(1, 2), sp.Rational(1, 2), 0], [0, 0, 0]]) for sign in (1, -1)]
    real_pair.append(sp.diag(0, 0, 1))
    householder = sp.eye(3)-sp.ones(3)*sp.Rational(2, 3)
    real_dense = [householder[:, j]*householder[:, j].T for j in range(3)]
    return {"computational": computational, "inverse_F3": fourier,
            "real_pair_basis": real_pair, "real_dense_basis": real_dense,
            "public_half_F3_half_real_dense": [e/2 for e in fourier+real_dense]}


def physical_gram_control(effects, q=9):
    """Full native-label and secret census; no selected-label signal estimate."""
    if q not in (3, 9):
        raise ValueError("dense full-population control capped at q9")
    inv = effects_invariants(effects)
    matrices = np.array([np.array(e.evalf(), dtype=complex) for e in effects])
    reference = np.trace(matrices, axis1=1, axis2=2).real/3
    gram = np.zeros((q, q))
    for a, c in product(range(q), repeat=2):
        s = np.arange(q)
        state = np.stack((np.ones(q), np.exp(2j*np.pi*(a*s % q)/q), np.exp(2j*np.pi*(c*s % q)/q)), axis=1)/np.sqrt(3)
        born = np.einsum("si,yij,sj->sy", state.conj(), matrices, state).real
        centered = born/reference-1
        gram += (centered*reference) @ centered.T/(q*q)
    expected = np.zeros((q, q)); expected[0, 0] = float(inv["zero_diagonal"])
    for s in range(1, q):
        expected[s, s] = float(inv["nonzero_diagonal"])
        expected[s, (-s) % q] = float(inv["opposite_nonzero_secret_Gram"])
    residual = float(np.max(abs(gram-expected)))
    if residual > 2e-12:
        raise ArithmeticError("arbitrary-basis native Born Gram contradicts exact invariants")
    return {"modulus": q, "complete_native_label_pairs": q*q, "complete_secret_pairs": q*q,
            "outcomes": len(effects), "actual_Born_Gram_residual": residual,
            "exact_invariants": inv, "nonprimitive_and_zero_secrets_kept": True}


def encode_effect(e):
    """Entries in Q(omega), stored as two canonical rational coefficients."""
    result = []
    for i in range(3):
        row = []
        for j in range(3):
            b = _rational(2*sp.im(e[i, j])/sp.sqrt(3))
            a = _rational(sp.re(e[i, j]))+b/2
            row.append([str(a), str(b)])
        result.append(row)
    return result


def report():
    cases = []
    for name, effects in example_povms().items():
        inv = effects_invariants(effects)
        cases.append({"name": name, "effects_Qomega": [encode_effect(e) for e in effects],
                      "invariants": inv, "physical_control": physical_gram_control(effects),
                      "eight_copy_scalar_gate": invariant_product_gate([inv]*8, 1, 8)})
    return {"status": "LABEL_INDEPENDENT_PRODUCT_POVM_GATE_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256((ROOT/"research/TERNARY_BLIND_PRODUCT_GATE.md").read_bytes()).hexdigest(),
            "quantum_speedup_proved": False, "candidate_record_accepted": False, "novelty_claim": False,
            "all_LOCC_or_general_quantum_lower_bound": False,
            "universal_scaling_gates": [blind_product_gate(1, r, r-2) for r in (8, 16, 32, 64)],
            "certified_POVM_controls": cases,
            "falsifiers": ["A positive complete fixed qutrit POVM violates d<=2/3 or |eta|<=d.",
                           "A native full-label Born census has a nonzero Gram entry outside s=t, s=-t or s=t=0.",
                           "A label-independent product POVM classifier violates the source-average copy bound."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    value = report()
    encoded = json.dumps(value, indent=2, default=lambda x: str(x) if isinstance(x, Fraction) else x, allow_nan=False)+"\n"
    if args.write:
        REPORT.write_text(encoded)
    print(json.dumps({"status": value["status"], "exact_POVMs": len(value["certified_POVM_controls"]),
                      "scaling_gates": len(value["universal_scaling_gates"]), "quantum_speedup_proved": False}))


if __name__ == "__main__":
    main()
