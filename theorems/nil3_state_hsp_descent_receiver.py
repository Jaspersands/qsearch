"""Honest native level3 phase lift; quotient recovery remains unimplemented.

Uses the actual cyclotomic ring backend and secret-blind correction gates.
This is a conditional component, not a complete nil3 StateHSP receiver.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import nmod_mat
import numpy as np

from cyclotomic_rescaling_gate import ideal_chart, multiply, pairing, plus, reduce_element
from native_state_hsp_bridge import NativeGroup, ring_words
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NIL3_STATE_HSP_DESCENT.md"
REPORT = ROOT/"research/reductions/nil3_state_hsp_descent_receiver.json"
LEVEL = 3
CENTRAL = multiply((-1, 1), (-1, 1), LEVEL)


@dataclass(frozen=True)
class SuppliedPhaseSample:
    label: tuple[tuple[int, int], ...]
    state: np.ndarray
    level: int = LEVEL

    def __post_init__(self):
        if not self.label:
            raise ValueError("nonempty public label vector required")
        label = NativeGroup(self.level, len(self.label)).vector(self.label)
        state = np.asarray(self.state, dtype=complex)
        if state.shape != (3,) or not np.all(np.isfinite(state)) or abs(float(np.vdot(state, state).real)-1) > 1e-12:
            raise ValueError("normalized supplied qutrit state required")
        state = state.copy()
        state.setflags(write=False)
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "state", state)


def lower_lift(lower, width):
    if not isinstance(lower, (tuple, list)) or len(lower) != width:
        raise ValueError("actual known lower-quotient vector required")
    out = []
    for v in lower:
        if type(v) is not tuple or reduce_element(v, 2) != v:
            raise ValueError("canonical level2 representative required, not a claimed receiver")
        out.append(reduce_element(v, LEVEL))
    return tuple(out)


def phase_exponents(label, value, level=LEVEL):
    if len(label) != len(value):
        raise ValueError("matched label and native value dimensions required")
    NativeGroup(level, len(label))
    q = 3**((level+1)//2)
    return tuple(int(q*sum((pairing(a, multiply(s, lam, level), level) for a, s in zip(label, value)), Fraction())) % q
                 for lam in ((0, 0), (1, 0), (1, 1)))


def conditional_phase_lift(sample, known_lower):
    if sample.level != LEVEL:
        raise ValueError("this conditional component requires native level3")
    lower = lower_lift(known_lower, len(sample.label))
    correction = tuple((-e) % 9 for e in phase_exponents(sample.label, lower))
    diagonal = np.exp(2j*np.pi*np.array(correction)/9)
    j = np.arange(3)
    F = np.exp(-2j*np.pi*np.outer(j, j)/3)/math.sqrt(3)
    output = F@(diagonal*sample.state)
    probabilities = abs(output)**2
    probabilities /= probabilities.sum()
    row = []
    for a in sample.label:
        coefficient = 3*pairing(a, CENTRAL, LEVEL)
        if coefficient.denominator != 1:
            raise ArithmeticError("central character is not a third root")
        row.append(int(coefficient) % 3)
    return {"phase_correction_exponents_mod9": correction, "central_character_row": tuple(row),
            "measurement_probabilities": tuple(map(float, probabilities)),
            "known_lower_is_an_explicit_input_premise": True,
            "top_secret_used_in_gate_parameters": False}


def solve_full_rank_f3(rows, rhs, width):
    integer(width, "positive vector width", 1)
    if len(rows) != len(rhs) or any(len(r) != width or any(type(v) is not int or v not in (0, 1, 2) for v in r) for r in rows):
        raise ValueError("canonical F3 equations required")
    if any(type(v) is not int or v not in (0, 1, 2) for v in rhs):
        raise ValueError("canonical F3 outcomes required")
    if not rows:
        return None
    R, _ = nmod_mat([tuple(r)+(b,) for r, b in zip(rows, rhs)], 3).rref()
    out, pivots = [0]*width, []
    for row in R.tolist():
        row = tuple(map(int, row))
        if not any(row[:-1]):
            if row[-1]:
                raise ValueError("inconsistent F3 equations")
            continue
        pivot = next(j for j, v in enumerate(row[:-1]) if v)
        pivots.append(pivot)
        out[pivot] = row[-1]
    return tuple(out) if len(pivots) == width else None


def recover_top_digits(samples, known_lower, rng):
    samples = tuple(samples)
    if not samples:
        raise ValueError("finite supplied sample batch required")
    n = len(samples[0].label)
    lower_lift(known_lower, n)
    rows, rhs, consumed = [], [], 0
    for sample in samples:
        if len(sample.label) != n:
            raise ValueError("one native vector dimension required")
        lift = conditional_phase_lift(sample, known_lower)
        measured = int(rng.choice(3, p=lift["measurement_probabilities"]))
        rows.append(lift["central_character_row"])
        rhs.append(measured)
        consumed += 1
        answer = solve_full_rank_f3(rows, rhs, n)
        if answer is not None:
            return {"status": "CONDITIONAL_TOP_DIGITS_RECOVERED", "recovered_top_digits": answer,
                    "rows": rows, "measured_outcomes": rhs, "consumed_samples": consumed,
                    "available_samples": len(samples), "known_lower_premise_verified_here": False,
                    "full_secret_receiver_supplied": False}
    return {"status": "INSUFFICIENT_INDEPENDENT_LABELS", "recovered_top_digits": None,
            "rows": rows, "measured_outcomes": rhs, "consumed_samples": consumed,
            "available_samples": len(samples), "full_secret_receiver_supplied": False}


def full_nil3_receiver_simulation(*args, **kwargs):
    raise NotImplementedError("quotient state production and lower-digit recovery are not implemented; no secret values are assigned to recovered outputs")


def ring_model_countercontrols():
    G = NativeGroup(LEVEL)
    zero, one = reduce_element((0, 0), LEVEL), reduce_element((1, 0), LEVEL)
    triple = plus(one, plus(one, one, LEVEL), LEVEL)
    g = G.hidden_elements((one,))[1]
    cube = G.compose(G.compose(g, g), g)
    if triple == zero or cube != ((zero,), 0):
        raise ArithmeticError("native ramification or cyclic hidden subgroup law failed")
    return {"level": LEVEL, "ideal_HNF": ideal_chart(LEVEL)[0],
            "native_three_times_one": triple, "incorrect_characteristic_three_result": zero,
            "native_pi_squared": CENTRAL, "native_hidden_generator": g, "native_hidden_generator_cube": cube,
            "incorrect_truncated_polynomial_generator_cube_z_digit": 2,
            "native_cyclotomic_ring_is_F3_truncated_polynomial_ring": False}


def scalar_phase_controls():
    G = NativeGroup(LEVEL)
    out = []
    for lower, u, label in product(ring_words(2), range(3), ring_words(LEVEL)):
        secret = plus(reduce_element(lower, LEVEL), multiply(CENTRAL, (u, 0), LEVEL), LEVEL)
        sample = SuppliedPhaseSample((label,), G.supplied_phase_state((label,), (secret,)))
        lift = conditional_phase_lift(sample, (lower,))
        source = phase_exponents(sample.label, (secret,))
        residual = tuple((a+b) % 9 for a, b in zip(source, lift["phase_correction_exponents_mod9"]))
        k = lift["central_character_row"][0]*u % 3
        if residual != (0, 3*k, 6*k % 9) or lift["measurement_probabilities"][k] < 1-1e-12:
            raise ArithmeticError("actual native source phase correction failed")
        out.append({"known_lower": lower, "top_digit_fixture_only": u, "public_label": label,
                    "source_phase_exponents_mod9_fixture": source, **lift,
                    "exact_residual_phase_exponents_mod9": residual, "expected_top_character_outcome_fixture": k})
    return out


def conditional_batch_control(n, seed):
    G = NativeGroup(LEVEL, n)
    rng = np.random.default_rng(seed)
    lower = tuple(tuple(map(int, rng.integers(0, 3, size=2))) for _ in range(n))
    top = tuple(map(int, rng.integers(0, 3, size=n)))
    secret = tuple(plus(reduce_element(s, LEVEL), multiply(CENTRAL, (u, 0), LEVEL), LEVEL) for s, u in zip(lower, top))
    samples = []
    for _ in range(n+8):
        label = tuple((int(rng.integers(0, 9)), int(rng.integers(0, 3))) for _ in range(n))
        samples.append(SuppliedPhaseSample(label, G.supplied_phase_state(label, secret)))
    result = recover_top_digits(samples, lower, rng)
    if result["recovered_top_digits"] != top:
        raise ArithmeticError("conditional native phase receiver failed its committed calibration")
    return {"dimension": n, "known_lower_fixture": lower, "top_truth_fixture_only": top,
            "public_labels": tuple(s.label for s in samples), "result": result,
            "lower_quotient_receiver_executed": False}


def tree_dilation_complexity_ledger(n_vals=(4, 8, 16, 32), r_vals=(2, 3, 4, 8, 16)):
    out = []
    for n, r in product(n_vals, r_vals):
        integer(n, "positive dimension", 1)
        integer(r, "depth at least2", 2)
        W = (n+1)**2
        out.append({"dimension_n": n, "nilpotency_class_r": r, "window_size_W": W,
                    "copies_per_state_in_specified_disjoint_tree": str(W**(r-2)),
                    "total_copies_in_specified_disjoint_tree": str(n*n*W**(r-2)),
                    "fixed_depth_polynomial_degree_in_n": 2*r-2,
                    "every_fixed_r_is_polynomial_in_n": True,
                    "implemented_receiver_or_universal_copy_lower_bound": False})
    return out


def run_all_controls():
    return {"status": "NIL3_CONDITIONAL_NATIVE_PHASE_LIFT_NOT_COMPLETE_RECEIVER",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "ring_model_countercontrols": ring_model_countercontrols(),
            "complete_scalar_phase_controls": scalar_phase_controls(),
            "conditional_batch_controls": [conditional_batch_control(n, 9000+n) for n in (2, 4, 8)],
            "tree_dilation_ledger": tree_dilation_complexity_ledger(),
            "summary": {"nil3_state_hsp_solved_in_polynomial_time": False,
                        "nil3_copy_complexity_is_O_n4": False,
                        "conditional_top_digit_phase_lift_constructed": True,
                        "lower_quotient_receiver_supplied": False,
                        "tree_dilation_is_a_universal_lower_bound": False,
                        "growing_depth_LWE_hardness_proved": False,
                        "shor_level_speedup_claimed": False}}


def write_report(output_path=REPORT, write_registry=False):
    report = run_all_controls()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    # There is no admitted negative theorem or full receiver to register.
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--no-registry", action="store_true")
    args = parser.parse_args()
    report = write_report() if args.write else run_all_controls()
    print(json.dumps({"status": report["status"], "scalar_native_phase_controls": 729,
                      "conditional_batch_controls": 3, "full_receiver_supplied": False,
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
