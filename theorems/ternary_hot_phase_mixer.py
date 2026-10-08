"""Actual hot phase/mixer fiber search and one-round native population law.

LOCAL DERIVATION / REVIEW PENDING. Multiple layers remain outside the bound.
This prepares from known uniform words, not a new native-secret decoder.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import root_digits
from ternary_cyclic_extractor import random_even_source
from ternary_native_block_walk import _integer
from ternary_native_spectral_access import sqrt_integer_interval
from ternary_residual_fiber_cooling import ResidualFiberParent

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_HOT_PHASE_MIXER.md"
REPORT = ROOT / "research/phase_workbench/ternary_hot_phase_mixer.json"


def ceil_cube_root(value):
    _integer(value, "integer cube-root argument")
    low, high = 0, 1 << ((value.bit_length()+2)//3)
    while high-low > 1:
        mid = (low+high)//2
        if mid**3 < value:
            low = mid
        else:
            high = mid
    return high


def sqrt_rational_upper(value):
    value = Fraction(value)
    _, high = sqrt_integer_interval(value.numerator*value.denominator, 80)
    return high/value.denominator


def one_layer_pi_population(n, q, inputs):
    _integer(n, "native dimension"); root_digits(q); _integer(inputs, "original native inputs")
    eta, diagonal = Fraction(2-q, q)**n, Fraction(-1, 3)**inputs
    probability = ((eta+(1-eta)*diagonal)**2+(1-eta*eta)*(1-diagonal*diagonal))/q**n
    return {"dimension": n, "modulus": str(q), "source_inputs": inputs,
            "phase_mean_exact": str(eta), "mixer_diagonal_exact": str(diagonal),
            "uniform_target_population_success_exact": str(probability),
            "phase_angle": "pi", "mixer_angle": "pi",
            "target_is_uniform_full_frequency_not_Born_weighted": True}


def one_layer_adaptive_angle_bound(n, q, inputs):
    _integer(n, "native dimension"); root_digits(q); _integer(inputs, "original native inputs")
    G, D = q**n, 3**inputs
    steps = ceil_cube_root(G)
    discretization = Fraction(44*(n+inputs), 7*steps)
    uniform = min(Fraction(1), Fraction(9*steps*steps, G)+discretization)
    born = min(Fraction(1), uniform+sqrt_rational_upper(Fraction(G-1, D)*uniform))
    return {"dimension": n, "modulus": str(q), "source_inputs": inputs,
            "native_word_dimension": str(D), "full_frequency_group": str(G),
            "one_fixed_angle_pair_uniform_population_success_upper": str(min(Fraction(1), Fraction(9, G))),
            "implicit_angle_net_points_per_axis": str(steps),
            "implicit_angle_net_points_total": str(steps*steps),
            "net_is_mathematical_certificate_not_executed_optimizer": True,
            "probability_discretization_error_upper": str(discretization),
            "best_label_and_target_adaptive_angles_uniform_population_success_upper": str(uniform),
            "best_label_and_target_adaptive_angles_Born_population_success_upper": str(born),
            "labels_and_target_may_select_continuous_angles": True,
            "mixer_form_and_one_layer_template_fixed": True,
            "multiple_layers_or_label_adaptive_mixer_shapes_are_not_covered": True,
            "arbitrary_quantum_receiver_lower_bound": False}


class HotPhaseMixer:
    def __init__(self, source, target):
        self.parent = ResidualFiberParent(source, target)
        self.source, self.target = source, self.parent.target

    def energy_program(self, word):
        return {"residual_energy": self.parent.energy(word),
                "full_frequency": self.source.value(word),
                "original_public_row_evaluations_upper": self.source.inputs*self.source.dimension,
                "whole_word_or_secret_grid_required": False,
                "unknown_secret_or_unknown_state_inverse_used": False}

    def reference(self, layers, max_words=4096, max_layers=32):
        _integer(max_words, "whole word reference cap"); _integer(max_layers, "whole layer cap")
        if 3**self.source.inputs > max_words or not layers or len(layers) > max_layers:
            raise ValueError("whole phase/mixer reference exceeds cap or has no layers")
        for gamma, beta in layers:
            if type(gamma) not in (float, int) or type(beta) not in (float, int) or not math.isfinite(gamma) or not math.isfinite(beta):
                raise ValueError("finite explicit public numeric angles required")
        words = tuple(product(range(3), repeat=self.source.inputs))
        energies = np.array([self.parent.energy(w) for w in words])
        state = np.ones(len(words), dtype=complex)/math.sqrt(len(words))
        for gamma, beta in layers:
            state *= np.exp(-1j*gamma*energies)
            phase = np.exp(-1j*beta)
            gate = phase*np.eye(3)+(1-phase)*np.ones((3, 3))/3
            tensor = state.reshape((3,)*self.source.inputs)
            for axis in range(self.source.inputs):
                tensor = np.moveaxis(tensor, axis, 0)
                shape = tensor.shape
                tensor = np.moveaxis((gate@tensor.reshape(3, -1)).reshape(shape), 0, axis)
            state = tensor.ravel()
        if abs(float(np.vdot(state, state).real)-1) > 1e-10:
            raise ArithmeticError("actual phase/mixer reference lost normalization")
        marked = np.flatnonzero(energies == 0)
        success = float(np.sum(abs(state[marked])**2))
        coherent_overlap = float(abs(np.sum(state[marked]))**2/len(marked)) if len(marked) else 0.0
        p = Fraction(len(marked), len(words))
        return {"layers": layers, "complete_words": words, "complete_residual_energies": energies.tolist(),
                "target_frequency": self.target, "marked_word_indices": marked.tolist(),
                "state_amplitudes_numeric": [[float(a.real), float(a.imag)] for a in state],
                "raw_fiber_membership_probability_numeric": success,
                "normalized_uniform_fiber_overlap_squared_numeric": coherent_overlap,
                "classical_uniform_word_rejection_probability_exact": str(p),
                "Grover_one_marked_reflection_probability_exact": str(p*(3-4*p)**2),
                "classical_reference_word_enumerations_charged": len(words),
                "numeric_reference_is_scalable_compiler_or_exact_roundoff_certificate": False,
                "fiber_membership_is_not_clean_uniform_fiber_erasure": True}


def exact_pi_census(q, inputs):
    root_digits(q); _integer(inputs, "census input width")
    if q**(2*inputs) > 10000 or 3**inputs > 27:
        raise ValueError("entire native label census exceeds cap")
    level = 2*root_digits(q)
    words = tuple(product(range(3), repeat=inputs)); D = len(words)
    uniform = born = Fraction(0); total = 0
    for flat in product(range(q), repeat=2*inputs):
        labels = tuple((inverse_frequency_coordinates(flat[2*i], flat[2*i+1], level),) for i in range(inputs))
        source = native_source(labels, level)
        values = [source.value(w)[0] for w in words]; counts = Counter(values)
        for y in range(q):
            amplitudes = [Fraction((-1)**(v != y)) for v in values]
            for axis in range(inputs):
                out = []
                for word in words:
                    coefficient = Fraction(0)
                    for a in range(3):
                        previous = list(word); previous[axis] = a
                        index = sum(t*3**(inputs-1-i) for i, t in enumerate(previous))
                        coefficient += (Fraction(2, 3)-int(a == word[axis]))*amplitudes[index]
                    out.append(coefficient)
                amplitudes = out
            probability = sum((amplitudes[i]**2 for i, v in enumerate(values) if v == y), Fraction(0))/D
            uniform += probability/q
            born += probability*Fraction(counts[y], D)
        total += 1
    uniform /= total; born /= total
    predicted = one_layer_pi_population(1, q, inputs)
    if uniform != Fraction(predicted["uniform_target_population_success_exact"]):
        raise ArithmeticError(f"complete label census {uniform} violates exact one-layer law {predicted['uniform_target_population_success_exact']}")
    return {"dimension": 1, "modulus": q, "native_level": level, "source_inputs": inputs,
            "entire_native_label_matrices": total, "all_uniform_target_cases": total*q,
            "uniform_target_mean_success_exact": str(uniform), "Born_target_mean_success_exact": str(born),
            "one_layer_prediction": predicted}


def five_word_torsion_pi_census(q):
    """Actual native five-word path: zero and the four binary weight-three words."""
    root_digits(q)
    if q**4 > 10000:
        raise ValueError("entire five-word frequency census exceeds cap")
    # Unused second native frequency rows integrate out; only four IID first rows matter.
    signed = quarter_real = quarter_imag = 0
    for first_rows in product(range(q), repeat=4):
        total = sum(first_rows)
        differences = [(total-a) % q for a in first_rows]
        signed += (-1)**sum(d != 0 for d in differences)
        phase = (sum(d != 0 for d in differences[2:])-sum(d != 0 for d in differences[:2])) % 4
        quarter_real += (1, 0, -1, 0)[phase]
        quarter_imag += (0, 1, 0, -1)[phase]
    a, b = Fraction(2-q, q), Fraction(2, q)
    actual, expected = Fraction(signed, q**4), a**4+2*b**4
    if actual != expected:
        raise ArithmeticError("native five-word torsion moment violates annihilator formula")
    eta_norm2, b_norm2 = Fraction(1+(q-1)**2, q*q), Fraction(2, q*q)
    quarter_expected = eta_norm2**2+2*b_norm2**2
    if quarter_imag or Fraction(quarter_real, q**4) != quarter_expected:
        raise ArithmeticError("mixed-sign quarter-phase native moment violates annihilator formula")
    return {"modulus": q, "base_original_word": [0, 0, 0, 0],
            "other_original_words": [[int(i != j) for j in range(4)] for i in range(4)],
            "pointed_first_row_coefficient_matrix": [[int(i != j) for j in range(4)] for i in range(4)],
            "pointed_matrix_determinant": -3, "independent_IID_first_row_assignments_checked": q**4,
            "unused_second_native_rows_integrated_out_not_assumed_fixed_in_population": True,
            "actual_four_phase_pi_moment_exact": str(actual),
            "false_full_independence_prediction_exact": str(a**4),
            "mixed_quarter_phase_moment_exact": str(quarter_expected),
            "mixed_quarter_phase_imaginary_part_exact": "0",
            "false_independent_mixed_quarter_phase_prediction_exact": str(eta_norm2**2),
            "kernel_characters_are_uniform_all_four_coordinates_at_multiples_of_q_over_three": True,
            "correlation_is_an_executed_two_layer_advantage": False}


def run_controls():
    source = random_even_source(2, 4, 5, 89881)
    values = Counter(source.value(w) for w in product(range(3), repeat=source.inputs))
    target = min(values, key=lambda y: (-values[y], y))
    program = HotPhaseMixer(source, target)
    angles = [0.0, math.pi/2, math.pi, 3*math.pi/2]
    trials = [program.reference([(g, b)]) for g in angles for b in angles]
    best = max(trials, key=lambda r: r["raw_fiber_membership_probability_numeric"])
    # A native field-root positive control guards against generic circuit claims.
    linear = native_source(((inverse_frequency_coordinates(1, 2, 2),),), 2)
    positive = HotPhaseMixer(linear, (1,)).reference([(2*math.pi/3, 2*math.pi/3)])
    return {"status": "HOT_PHASE_MIXER_ACTUAL_PROGRAM_AND_ONE_LAYER_BOUND_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_source": {"seed": 89881, "dimension": source.dimension, "modulus": source.modulus,
                "native_level": source.level, "source_inputs": source.inputs,
                "original_ring_labels": source.labels, "native_frequencies": source.frequencies},
            "one_layer_public_angle_menu": trials, "best_public_finite_menu_trial": best,
            "finite_menu_selection_uses_charged_classical_statevector_enumeration": True,
            "two_layer_open_scope_control": program.reference([(math.pi/2, math.pi/3), (math.pi, math.pi/2)]),
            "native_field_root_positive_control": positive,
            "exact_native_population_censuses": [exact_pi_census(3, 2), exact_pi_census(9, 1)],
            "five_word_torsion_controls": [five_word_torsion_pi_census(q) for q in (3, 9)],
            "one_layer_adaptive_scaling_ledgers": [one_layer_adaptive_angle_bound(n, q, n*root_digits(q)+8)
                                                  for n, q in ((8, 9), (32, 81), (128, 243), (512, 729))],
            "gate_recipe": "Known uniform qutrits; reversible full F and coordinate mismatch count; phase rotation; clean scratch reversal; product exp(-i beta*(I-|+><+|)) gates. Repeat only with all layer/error costs charged.",
            "multiple_layers_are_not_excluded": True, "arbitrary_quantum_receiver_lower_bound": False,
            "efficient_clean_fiber_preparation_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True); REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "efficient_clean_fiber_preparation_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
