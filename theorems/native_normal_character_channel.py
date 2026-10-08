"""Native normal-character measurement versus coherent retention.

LOCAL CHANNEL DERIVATION / REVIEW PENDING. A normal-subgroup measurement
is not central descent. This is an exact scoped cut, not a lower bound for
arbitrary quantum receivers or an efficient coherent fiber eraser.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import numpy as np

from cyclotomic_rescaling_gate import ideal_chart, multiply, pairing, plus, reduce_element
from cyclic_centre_state_hsp_receiver import integer
from native_state_hsp_bridge import NativeGroup

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/reductions/native_normal_character_channel.json"


@dataclass(frozen=True)
class NormalCharacterChannel:
    level: int
    normal_power: int
    labels: tuple

    def __post_init__(self):
        integer(self.level, "native level", 2)
        integer(self.normal_power, "normal ideal power", 1)
        if not self.normal_power < self.level:
            raise ValueError("nontrivial pi^c A subgroup with c<r required")
        if not self.labels or not self.labels[0]:
            raise ValueError("nonempty actual native label cohort required")
        G = NativeGroup(self.level, len(self.labels[0]))
        object.__setattr__(self, "labels", tuple(G.vector(v) for v in self.labels))

    @property
    def dimension(self):
        return len(self.labels[0])

    @property
    def copies(self):
        return len(self.labels)

    def normal_character(self, word):
        if len(word) != self.copies or any(type(j) is not int or j not in (0, 1, 2) for j in word):
            raise ValueError("one canonical trit per supplied native qutrit required")
        full = [(0, 0)]*self.dimension
        roots = ((1, 0), (0, 1), (-1, -1))
        for j, label in zip(word, self.labels):
            full = [plus(a, multiply(b, roots[j], self.level), self.level) for a, b in zip(full, label)]
        return tuple(reduce_element(v, self.level-self.normal_power) for v in full)

    def phase(self, word, secret):
        secret = NativeGroup(self.level, self.dimension).vector(secret)
        if len(word) != self.copies or any(type(j) is not int or j not in (0, 1, 2) for j in word):
            raise ValueError("one canonical native trit per supplied copy required")
        lambdas = ((0, 0), (1, 0), (1, 1))
        phase = Fraction()
        for j, label in zip(word, self.labels):
            for a, s in zip(label, secret):
                phase += pairing(a, multiply(s, lambdas[j], self.level), self.level)
        return phase % 1

    def finite_control(self, left, right):
        if self.copies > 6:
            raise ValueError("whole-word/channel simulation is calibration-only, at most six copies")
        left = NativeGroup(self.level, self.dimension).vector(left)
        right = NativeGroup(self.level, self.dimension).vector(right)
        word_list = tuple(product(range(3), repeat=self.copies))
        groups = defaultdict(list)
        differences = []
        for i, w in enumerate(word_list):
            groups[self.normal_character(w)].append(i)
            differences.append((self.phase(w, right)-self.phase(w, left)) % 1)
        D = len(word_list)
        sector_constant = all(len({differences[i] for i in indices}) == 1 for indices in groups.values())
        left_v = np.array([np.exp(2j*np.pi*float(self.phase(w, left)))/np.sqrt(D) for w in word_list])
        right_v = np.array([np.exp(2j*np.pi*float(self.phase(w, right)))/np.sqrt(D) for w in word_list])
        dephased_difference = np.zeros((D, D), complex)
        for indices in groups.values():
            a, b = left_v[indices], right_v[indices]
            dephased_difference[np.ix_(indices, indices)] = np.outer(a, a.conj())-np.outer(b, b.conj())
        trace_distance = float(np.sum(abs(np.linalg.eigvalsh(dephased_difference)))/2)
        coherent_fidelity = float(abs(np.vdot(left_v, right_v))**2)
        if sector_constant and trace_distance > 2e-11:
            raise ArithmeticError("exact sector alias disagrees with complete pinched channel")
        return {"level": self.level, "normal_ideal_power": self.normal_power,
                "labels": self.labels, "secret_dimension": self.dimension,
                "original_qutrit_copies": self.copies, "left_native_secret": left, "right_native_secret": right,
                "complete_original_words": word_list, "normal_characters": [self.normal_character(w) for w in word_list],
                "exact_phase_difference_mod1": [str(f) for f in differences],
                "complete_character_classes": [{"character": char, "word_indices": indices,
                                                "raw_Born_probability": str(Fraction(len(indices), D))} for char, indices in sorted(groups.items())],
                "exact_phase_difference_constant_within_each_class": sector_constant,
                "complete_measured_normal_channel_trace_distance": trace_distance,
                "original_and_coherently_retained_character_channel_fidelity": coherent_fidelity,
                "normal_character_measurement_outcomes_are_secret_independent": True,
                "coherent_computation_is_isometry_not_fiber_erasure": True,
                "original_word_register_erased_by_coherent_computation": False,
                "unknown_inverse_or_cloning_used": False,
                "full_character_dictionary_is_scalable_compiler": False}


def precision_ledger(level, dimension, normal_power):
    integer(level, "native level", 2)
    integer(dimension, "secret dimension", 1)
    integer(normal_power, "normal ideal power", 1)
    if normal_power >= level:
        raise ValueError("nontrivial normal subgroup required")
    original_digits = (level+1)//2
    kept = min(original_digits, (normal_power+2)//2)
    return {"native_level": level, "secret_dimension": dimension, "normal_ideal_power": normal_power,
            "normal_subgroup_is_central": normal_power == level-1,
            "ring_secret_alias_ideal": f"pi^{normal_power+1} A",
            "maximum_integer_secret_trits_retained_per_coordinate": kept,
            "integer_secret_alias_class": {"base": 3, "exponent": dimension*(original_digits-kept)},
            "uniform_full_secret_success_upper_after_ONLY_this_measurement_channel": {"numerator": 1, "denominator_base": 3, "denominator_exponent": dimension*(original_digits-kept)},
            "all_branches_including_recorded_character_outcome_included": True,
            "bound_applies_to_coherently_retained_character_register": False,
            "bound_applies_to_arbitrary_quantum_receivers": False,
            "additional_untouched_original_inputs_covered": False}


def conjugate_erase_control(channel, joint_state):
    """ALL-branch public Fourier measurement/feedforward on a computed pointer.

    The reference may be entangled. This erases ONLY the computed character
    register, restoring the original input, not erasing its word/fiber index.
    """
    if channel.copies > 6:
        raise ValueError("bounded complete eraser replay requires at most six copies")
    h = channel.level-channel.normal_power
    branches = 3**(h*channel.dimension)
    if branches > 81:
        raise ValueError("complete pointer Fourier replay capped at81 branches")
    D = 3**channel.copies
    state = np.asarray(joint_state, complex)
    if (state.ndim != 2 or state.shape[0] != D or not np.isfinite(state).all()
            or abs(np.vdot(state, state).real-1) > 2e-11):
        raise ValueError("normalized word/reference joint state required")
    h0, _, h1 = ideal_chart(h)[0]
    scalars = tuple(product(range(h0), range(h1)))
    character_words = [channel.normal_character(w) for w in product(range(3), repeat=channel.copies)]
    errors, probabilities = [], []
    for b in product(scalars, repeat=channel.dimension):
        phase = [sum((pairing(a, v, h) for a, v in zip(char, b)), Fraction()) % 1 for char in character_words]
        known_phase = np.exp(2j*np.pi*np.array([float(f) for f in phase]))[:, None]
        raw = state*known_phase.conj()/np.sqrt(branches)
        probabilities.append(float(np.vdot(raw, raw).real))
        corrected = raw*known_phase
        errors.append(float(np.linalg.norm(corrected-state/np.sqrt(branches))))
    return {"level": channel.level, "normal_ideal_power": channel.normal_power,
            "secret_dimension": channel.dimension, "original_qutrit_copies": channel.copies,
            "complete_Fourier_outcome_count": branches,
            "exact_raw_probability_of_every_outcome": str(Fraction(1, branches)),
            "maximum_raw_probability_error": max(abs(p-1/branches) for p in probabilities),
            "maximum_feedforward_corrected_joint_vector_error": max(errors),
            "reference_dimension": state.shape[1],
            "restores_input_including_reference_entanglement": True,
            "erases_original_word_register": False, "decodes_secret": False,
            "undoes_already_classically_measured_normal_character": False,
            "unknown_state_inverse_or_preparation_used": False}


def run_controls():
    specs = [(6, 2, (((1, 0),),), ((0, 0),), ((9, 0),)),
             (6, 2, (((1, 0),), ((0, 1),), ((2, 1),)), ((0, 0),), ((9, 0),)),
             (5, 1, (((1, 0),), ((0, 1),)), ((0, 0),), ((3, 0),)),
             (4, 2, (((1, 0),), ((0, 1),)), ((0, 0),), ((3, 0),)),
             (6, 5, (((1, 0),), ((0, 1),)), ((0, 0),), ((9, 0),)),
             (6, 2, (((1, 0), (0, 1)), ((0, 1), (2, 1))), ((0, 0), (0, 0)), ((9, 0), (0, 0)))]
    controls = [NormalCharacterChannel(r, c, labels).finite_control(left, right) for r, c, labels, left, right in specs]
    erasers = []
    rng = np.random.default_rng(193881)
    for r, c, labels, _, _ in specs[:3]:
        channel = NormalCharacterChannel(r, c, labels)
        state = rng.normal(size=(3**channel.copies, 2))+1j*rng.normal(size=(3**channel.copies, 2))
        state /= np.linalg.norm(state)
        erasers.append(conjugate_erase_control(channel, state))
    return {"status": "NATIVE_NORMAL_CHARACTER_PINCHING_ALIAS_AND_COHERENT_RETENTION_REVIEW_PENDING",
            "complete_channels": controls,
            "complete_public_conjugate_eraser_controls": erasers,
            "growing_precision_ledgers": [precision_ledger(r, n, c) for r, n, c in ((4, 1, 2), (6, 1, 2), (16, 8, 2), (64, 64, 2), (128, 128, 127))],
            "normal_measurement_is_not_central_descent": True,
            "multi_output_or_coherent_receiver_ruled_out": False,
            "coherent_fiber_erasure_compiled": False,
            "native_full_depth_receiver_supplied": False,
            "novelty_claimed": False, "Shor_level_result_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(r, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": r["status"], "complete_channels": len(r["complete_channels"]),
                      "deep_normal_alias_controls": sum(c["exact_phase_difference_constant_within_each_class"] for c in r["complete_channels"])}))


if __name__ == "__main__":
    main()
