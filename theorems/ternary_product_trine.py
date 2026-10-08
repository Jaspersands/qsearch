"""Physical product-trine receivers and a costed joint classical baseline.

LOCAL DERIVATIONS / REVIEW PENDING. Measurement access is explicit; decoding
is still exponential. Neither local gate count nor joint signal is a speedup.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import (
    CovariantRecord, ROOT_DIRECTIONS, apply_qutrit_tape, phase, receiver_recipe, root_digits,
)
from ternary_posterior_dual import solve_least_trit

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_product_trine.json"
F3 = np.array([[phase(-j*k, 3)/math.sqrt(3) for k in range(3)] for j in range(3)])


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _word(values, q, name, length=None):
    values = tuple(values)
    if not values or (length is not None and len(values) != length) or any(
            type(x) is not int or not 0 <= x < q for x in values):
        raise ValueError(f"canonical {name} required")
    return values


@dataclass(frozen=True)
class TrineRecord:
    """One fixed inverse-F3 digit, not a paired covariant observation."""

    first: tuple
    second: tuple
    digit: int
    modulus: int

    def __post_init__(self):
        root_digits(self.modulus)
        object.__setattr__(self, "first", _word(self.first, self.modulus, "first frequency"))
        object.__setattr__(self, "second", _word(self.second, self.modulus, "second frequency", len(self.first)))
        _integer(self.digit, "trine digit")
        if self.digit > 2:
            raise ValueError("trine digit must be in F3")

    def probability(self, secret):
        secret = _word(secret, self.modulus, "secret", len(self.first))
        a, c = (sum(x*s for x, s in zip(row, secret)) for row in (self.first, self.second))
        return abs(1+phase(a, self.modulus)*phase(-self.digit, 3)
                   +phase(c, self.modulus)*phase(-2*self.digit, 3))**2/9

    def public(self):
        return {"first": self.first, "second": self.second, "digit": self.digit,
                "modulus": self.modulus, "readout": "FIXED_INVERSE_F3_NO_PUBLIC_PHASE_RANDOMIZATION"}


def joint_posterior(records, original_ids, **budgets):
    """Reuse phase algebra ONLY, replacing the generative model explicitly."""
    records = tuple(records)
    if not records or any(not isinstance(r, TrineRecord) for r in records):
        raise ValueError("nonempty validated fixed-trine records required")
    adapters = tuple(CovariantRecord(r.first, r.second,
                     (r.modulus//3*r.digit, (2*r.modulus//3*r.digit) % r.modulus), r.modulus) for r in records)
    result = solve_least_trit(adapters, original_ids, **budgets)
    # The q^2/3 constant per record cancels in the posterior, not in the law.
    result.update({"records": [r.public() for r in records],
                   "observation_model": "FIXED_PRODUCT_INVERSE_F3",
                   "paired_covariant_generative_law_used": False,
                   "adapter_scope": "LIKELIHOOD_PHASE_ALGEBRA_ONLY_CONSTANTS_CANCEL",
                   "fixed_trine_probability_to_adapter_probability_ratio": str(Fraction(records[0].modulus**2, 3)),
                   "polynomial_native_weak_learner_implemented": False,
                   "speedup_claim_allowed": False})
    return result


def randomized_recipe(digits):
    """Compile the full-root covariant POVM into one randomized qutrit."""
    _integer(digits, "root digits", 1)
    return {"digits": digits, "modulus": str(3**digits), "original_qutrits": 1,
            "clean_quantum_ancillas": 0, "uniform_independent_public_random_trits": 2*digits,
            "gates": ["diag(1,chi_q(-alpha),chi_q(-beta))", "inverse_F3"],
            "report": "(y1,y2)=(alpha+(q/3)z,beta+2(q/3)z) modq",
            "settings_and_pointer_reconstructible_from_y_and_independent_uniform_z": True,
            "exact_effect_identity": "E_(y,z)=E_y/3; E_y=v_y*v_y^dagger/q^2",
            "full_q_squared_table_required": False, "unknown_source_inverse_required": False,
            "phase_synthesis_and_classical_randomness_error_must_be_charged": True,
            "hardware_gate_export_implemented": False, "novelty_claim": False}


def uniform_root(digits, rng):
    _integer(digits, "root digits", 1)
    value = 0
    for _ in range(digits):
        trit = rng.randrange(3)
        _integer(trit, "random trit")
        if trit > 2:
            raise ValueError("random trit outside F3")
        value = 3*value+trit
    return value


def randomized_outcome(q, alpha, beta, digit):
    root_digits(q)
    _word((alpha, beta), q, "public settings", 2)
    _integer(digit, "pointer digit")
    if digit > 2:
        raise ValueError("pointer outside F3")
    return ((alpha+q//3*digit) % q, (beta+2*q//3*digit) % q)


def error_budget(diagonal_error, fourier_error, random_settings_tv=0):
    """Operator-norm unitary errors imply measurement TV via telescoping."""
    values = tuple(Fraction(x) for x in (diagonal_error, fourier_error, random_settings_tv))
    if any(x < 0 for x in values) or values[2] > 1:
        raise ValueError("nonnegative operator errors and randomness TV in [0,1] required")
    return {"outcome_TV_upper": str(min(Fraction(1), sum(values))),
            "scope": "one normalized input, diagonal/F3 operator-norm errors and settings TV",
            "source_preparation_error_covered": False}


def physical_compiler_control(q, state):
    """Bounded replay of every setting/pointer AND the existing QFT circuit."""
    r = root_digits(q)
    state = np.asarray(state, dtype=complex)
    if q > 27 or state.shape != (3,) or not np.isfinite(state).all() or abs(float(np.vdot(state, state).real)-1) > 1e-12:
        raise ValueError("normalized one-qutrit control with modulus <=27 required")
    branch = np.zeros((q, q, 3))
    residual = 0.0
    effects = np.zeros((3, 3), dtype=complex)
    for a, b in product(range(q), repeat=2):
        output = F3 @ (state*np.array([1, phase(-a, q), phase(-b, q)]))
        for z in range(3):
            y = randomized_outcome(q, a, b, z)
            value = float(abs(output[z])**2/(q*q))
            branch[y[0], y[1], z] += value
            expected = abs(state[0]+state[1]*phase(-y[0], q)+state[2]*phase(-y[1], q))**2/(3*q*q)
            residual = max(residual, abs(value-expected))
        v = np.array([1, phase(a, q), phase(b, q)])
        effects += np.outer(v, v.conj())/(q*q)
    embedded = np.zeros((q, q), dtype=complex)
    embedded[0, 0], embedded[1, 0], embedded[2, 0] = state
    recipe = receiver_recipe(r)
    output = apply_qutrit_tape(embedded.ravel(), 2*r, recipe["gates"]).reshape(q, q)
    covariant = abs(output)**2
    errors = {"branch_effect_identity_residual": residual,
              "covariant_circuit_probability_residual": float(np.max(abs(branch.sum(axis=2)-covariant))),
              "independent_uniform_pointer_residual": float(np.max(abs(branch-covariant[:, :, None]/3))),
              "effect_completeness_residual": float(np.max(abs(effects-np.eye(3)))),
              "normalization_residual": abs(float(branch.sum())-1)}
    if max(errors.values()) > 2e-12:
        raise ArithmeticError("randomized one-qutrit compiler disagrees with physical POVM")
    return {"modulus": q, "input_state": [[float(x.real), float(x.imag)] for x in state],
            "settings_enumerated_for_calibration_only": q*q, **errors,
            "existing_two_register_gate_tape_replayed": True, "arbitrary_input_not_just_native_phases": True}


def fixed_trine_gram(q, first_secret, second_secret):
    """Exact centered Gram by full-label and output character orthogonality."""
    root_digits(q)
    s = _word(first_secret, q, "first secret")
    t = _word(second_secret, q, "second secret", len(s))
    count = 0
    for (u, v), (a, b) in product(ROOT_DIRECTIONS, repeat=2):
        if (u+2*v+a+2*b) % 3:
            continue
        if all((u*x+a*y) % q == 0 and (v*x+b*y) % q == 0 for x, y in zip(s, t)):
            count += 1
    return Fraction(count, 9)


def fixed_trine_gate(n, digits, samples, desired_advantage=Fraction(1, 10)):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1); _integer(samples, "samples")
    eps = Fraction(desired_advantage)
    if not 0 < eps <= Fraction(2, 3):
        raise ValueError("advantage in (0,2/3] required")
    G = 3**(n*digits)
    d = Fraction(5, 3)**samples-1
    zero = Fraction(1, G)*(1-Fraction(1, 3**samples))
    squared = d/(2*G)
    return {"dimension": n, "digits": digits, "original_independent_qutrits": samples,
            "secret_population": str(G), "nonzero_secret_centered_product_norm_squared": str(d),
            "zero_secret_centered_product_norm_squared": str(3**samples-1),
            "nonzero_contribution_advantage_upper_squared": str(squared),
            "zero_secret_advantage_upper": str(zero),
            "mean_advantage_upper_formula": "min(2/3,sqrt(nonzero_squared)+zero_upper)",
            "requested_advantage": str(eps),
            "necessary_copy_gate_passed": eps <= zero or squared >= (eps-zero)**2,
            "scope": "ANY classical joint processing of fixed inverse-F3 records; uniform ALL secrets; IID full native labels",
            "zero_secret_exception_kept": True, "other_bases_or_adaptive_LOCC_covered": False,
            "chosen_labels_or_sieve_retained_law_covered": False, "unmeasured_states_covered": False,
            "speedup_claim_allowed": False, "status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def joint_correlation_control():
    """Source-valid countercontrol: flat single marginals, informative joint law."""
    q, level = 81, 8
    rows = ((1, 2), (26, 52))
    source = native_source([[inverse_frequency_coordinates(a, c, level)] for a, c in rows], level)
    if tuple((a[0], c[0]) for a, c in source.frequencies) != rows:
        raise ArithmeticError("native label chart mismatch")
    words = tuple(product(range(3), repeat=2))
    frequencies = [sum((0, a, c)[x] for x, (a, c) in zip(w, rows)) % q for w in words]
    laws, counts = [], []
    for t in range(3):
        row, row_counts = [], []
        for output in words:
            powers = [0, 0, 0]
            for i, u in enumerate(words):
                for j, v in enumerate(words):
                    delta = (frequencies[i]-frequencies[j]) % q
                    if delta % (q//3) == 0:
                        e = (delta//(q//3)*t+sum(z*(b-a) for z, a, b in zip(output, u, v))) % 3
                        powers[e] += 1
            if powers[1] != powers[2]:
                raise ArithmeticError("joint Fourier probability must be exactly rational real")
            row.append(Fraction(powers[0]-powers[1], 81)); row_counts.append(powers)
        laws.append(row); counts.append(row_counts)
    transform = np.kron(F3, F3)
    actual = np.zeros((3, 9))
    for s in range(q):
        state = np.array([phase(f*s, q) for f in frequencies])/3
        actual[s % 3] += abs(transform @ state)**2/27
    residual = float(np.max(abs(actual-np.array([[float(x) for x in row] for row in laws]))))
    success = sum(max(laws[t][o] for t in range(3)) for o in range(9))/3
    marginal = [[sum(laws[t][i] for i, w in enumerate(words) if w[axis] == z)
                 for axis in range(2) for z in range(3)] for t in range(3)]
    if residual > 2e-12 or any(x != Fraction(1, 3) for row in marginal for x in row):
        raise ArithmeticError("joint signal/local marginal physical countercontrol failed")
    return {"modulus": q, "native_level": level, "native_labels": source.labels,
            "frequency_rows": rows, "word_frequencies": frequencies, "outputs": words,
            "exact_character_counts": counts, "joint_trit_laws": laws,
            "single_qutrit_marginals": marginal, "joint_MAP_success": success,
            "physical_all_secrets_twirl_residual": residual, "calibration_secrets_enumerated": q,
            "final_effect_word_Hamming_radius": 2, "entangling_readout_gates": 0,
            "prespecified_legal_labels_not_IID_population_evidence": True,
            "efficient_native_population_decoder_proved": False, "speedup_claim_allowed": False}


def posterior_control(records):
    q, n = records[0].modulus, len(records[0].first)
    if q**n > 729:
        raise ValueError("dense posterior calibration capped at 729 secrets")
    result = joint_posterior(records, tuple(range(len(records))))
    mass = [0.0]*3
    for s in product(range(q), repeat=n):
        mass[s[0] % 3] += math.prod(r.probability(s) for r in records)
    if sum(mass) < 1e-13:
        if result["posterior"]["status"] != "ZERO_LIKELIHOOD_DATA_NO_POSTERIOR":
            raise ArithmeticError("impossible data must not have a posterior")
        residual = 0.0
    else:
        expected = np.array(mass)/sum(mass)
        residual = float(np.max(abs(expected-result["posterior"]["posterior_probabilities"])))
        if residual > 2e-11:
            raise ArithmeticError("algebra adapter disagrees with fixed-trine likelihood")
    return {"solver": result, "dense_secret_count_calibration_only": q**n,
            "actual_fixed_trine_likelihood_residual": residual}


def report():
    states = [np.array([1, 0, 0], dtype=complex), np.ones(3)/math.sqrt(3),
              np.array([1, 2j, -3])/math.sqrt(14)]
    joint = joint_correlation_control()
    controls = [posterior_control([TrineRecord((1,), (2,), u, 81), TrineRecord((26,), (52,), v, 81)])
                for u, v in product(range(3), repeat=2)]
    gram_checks = []
    for q, n in ((3, 1), (9, 1), (27, 1), (3, 2)):
        secrets = tuple(product(range(q), repeat=n))
        for s, t in product(secrets, repeat=2):
            expected = (Fraction(2, 3) if any(s) else Fraction(2)) if s == t else Fraction(0)
            if fixed_trine_gram(q, s, t) != expected:
                raise ArithmeticError("full-secret Gram identity failed")
        gram_checks.append({"modulus": q, "dimension": n, "complete_secret_pairs": len(secrets)**2,
                            "direction_pairs_per_secret_pair": 36, "zero_diagonal": "2",
                            "nonzero_diagonal": "2/3", "off_diagonal": "0"})
    return {"status": "PHYSICAL_PRODUCT_READOUT_AND_COSTED_BASELINE_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256((ROOT/"research/TERNARY_PRODUCT_TRINE.md").read_bytes()).hexdigest(),
            "quantum_speedup_proved": False, "candidate_record_accepted": False, "novelty_claim": False,
            "randomized_recipes": [randomized_recipe(r) for r in (1, 16, 32, 64)],
            "compiler_controls": [physical_compiler_control(q, s) for q in (3, 9, 27) for s in states],
            "exact_Gram_controls": gram_checks,
            "fixed_readout_scaling_gates": [fixed_trine_gate(n, r, n*r-2) for n, r in ((1, 8), (1, 16), (1, 32), (1, 64), (2, 32))],
            "joint_correlation_countercontrol": joint, "exact_posterior_controls": controls,
            "example_approximation_error_budget": error_budget(Fraction(1, 10000), Fraction(1, 10000)),
            "falsifiers": ["Randomized branch effects differ from E_y/3 on an arbitrary input.",
                           "The fixed-readout full-label centered Gram has an off-diagonal or wrong zero diagonal.",
                           "Exact phase algebra disagrees with direct fixed-trine joint posterior.",
                           "Claimed joint signal disappears under the actual native all-secret twirl."],
            "general_quantum_hardness_or_all_LOCC_bound": False}


def _json(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    value = report()
    encoded = json.dumps(value, indent=2, default=_json, allow_nan=False)+"\n"
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(encoded)
    print(json.dumps({"status": value["status"], "compiler_controls": len(value["compiler_controls"]),
                      "joint_MAP_success": value["joint_correlation_countercontrol"]["joint_MAP_success"],
                      "posterior_controls": len(value["exact_posterior_controls"]),
                      "speedup_claim_allowed": False}, default=_json))


if __name__ == "__main__":
    main()
