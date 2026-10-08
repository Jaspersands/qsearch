"""Residual-aware native Gibbs parents: actual moves and cold warm-start test.

LOCAL DERIVATION / REVIEW PENDING. Hot excursions and non-parent moves remain
open. A complete warm state is granted, not claimed efficiently prepared.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm

from ternary_covariant_noise import root_digits
from ternary_cyclic_extractor import random_even_source
from ternary_native_block_walk import NativeBlockHeatbath, _integer, signature_count
from ternary_native_spectral_access import sqrt_integer_interval
from ternary_soft_fiber_cooling import _rational

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_RESIDUAL_FIBER_COOLING.md"
REPORT = ROOT / "research/phase_workbench/ternary_residual_fiber_cooling.json"

# Trusted exact population ledgers exceed Python's default decimal I/O ceiling.
if 0 < sys.get_int_max_str_digits() < 100000:
    sys.set_int_max_str_digits(100000)


def warm_population_moments(n, q, inputs, probability_attenuation=Fraction(1, 4)):
    _integer(n, "native dimension"); root_digits(q); _integer(inputs, "original source inputs")
    z = _rational(probability_attenuation, "probability attenuation", maximum=Fraction(1))
    if z == 0:
        raise ValueError("positive finite warm temperature required")
    D, G = 3**inputs, q**n
    mu, mu2 = ((1+(q-1)*z)/q)**n, ((1+(q-1)*z*z)/q)**n
    mean = Fraction(1, D)+Fraction(D-1, D)*mu
    variance = Fraction(D-1, D*D)*(mu2-mu*mu)
    purity = Fraction(1, G)+Fraction(G-1, G*D)
    bad_normalizer = min(Fraction(1), 4*variance/(mu*mu))
    warm_success = min(Fraction(1), 2*purity/mu+bad_normalizer)
    return {"dimension": n, "modulus": str(q), "source_inputs": inputs,
            "probability_attenuation": str(z), "mean_nonself_weight_exact": str(mu),
            "second_nonself_weight_exact": str(mu2), "mean_normalizer_exact": str(mean),
            "normalizer_variance_exact": str(variance), "source_collision_purity_exact_mean": str(purity),
            "probability_normalizer_below_half_nonself_mean_upper": str(bad_normalizer),
            "source_weighted_warm_fiber_success_upper": str(warm_success),
            "target_drawn_as_frequency_of_uniform_original_word": True,
            "distinct_nonself_weights_pairwise_independent_by_pointed_unit_minor": True,
            "warm_state_preparation_granted_not_implemented": True}


def energy_barrier_population(n, q, width, support):
    _integer(n, "native dimension"); root_digits(q)
    V = signature_count(width, support)
    h = n//3
    bad = min(Fraction(1), V*2**h*Fraction(q+1, 2*q)**n)
    _, sqrtS = sqrt_integer_interval(3**support-1, 80)
    return {"dimension": n, "modulus": str(q), "source_inputs": width, "maximum_block_support": support,
            "difference_signatures": str(V), "forbidden_residual_weight_at_most": h,
            "minimum_boundary_energy_on_good_labels": h+1,
            "probability_any_small_signature_below_energy_threshold_upper": str(bad),
            "maximum_cold_amplitude_attenuation": "1/2",
            "cross_fiber_parent_operator_norm_upper": str(sqrtS/Fraction(2**(h+1))),
            "sqrt_local_class_minus_one_upper": str(sqrtS), "sqrt_interval_bits": 80,
            "all_labels_and_targets_and_blocks_covered_on_good_event": True,
            "hotter_excursions_are_outside_scope": True}


def cold_population_certificate(n, q, inputs, support, action):
    A = _rational(action, "absolute integrated cold parent action")
    warm = warm_population_moments(n, q, inputs)
    barrier = energy_barrier_population(n, q, inputs, support)
    alpha = Fraction(warm["source_weighted_warm_fiber_success_upper"])
    # sqrt(a/b)=sqrt(a*b)/b, allowing an exact directed rational interval.
    _, root = sqrt_integer_interval(alpha.numerator*alpha.denominator, 80)
    root /= alpha.denominator
    bad = Fraction(barrier["probability_any_small_signature_below_energy_threshold_upper"])
    coupling = Fraction(barrier["cross_fiber_parent_operator_norm_upper"])
    success = min(Fraction(1), bad+(root+A*coupling)**2)
    return {"warm_population_moments": warm, "energy_barrier_population": barrier,
            "absolute_integrated_parent_action": str(A), "warm_fiber_probability_sqrt_upper": str(root),
            "source_weighted_cold_raw_fiber_success_upper": str(success),
            "arbitrary_diagonal_controls_covered": True,
            "uniform_per_instance_absolute_action_cap_required": True,
            "requires_all_IID_uniform_full_native_frequency_rows": True,
            "signed_nonmonotone_schedules_with_attenuation_at_most_half_covered": True,
            "bad_labels_charged_without_conditioned_normalization": True,
            "arbitrary_quantum_or_hot_schedule_lower_bound": False,
            "efficient_fiber_eraser_supplied": False}


class ResidualFiberParent:
    def __init__(self, source, target):
        self.native = NativeBlockHeatbath(source)
        self.source = source
        target = tuple(target)
        if len(target) != source.dimension or any(type(a) is not int or not 0 <= a < source.modulus for a in target):
            raise ValueError("canonical full-root target frequency required")
        self.target = target

    def energy(self, word):
        return sum(a != b for a, b in zip(self.source.value(self.native._word(word)), self.target))

    def conditional(self, word, block, attenuation, max_local_words=65536):
        word, block = self.native._word(word), self.native._block(block)
        t = _rational(attenuation, "positive amplitude attenuation", maximum=Fraction(1))
        if t == 0:
            raise ValueError("use a positive finite residual temperature; no undefined zero-weight class")
        _integer(max_local_words, "whole local conditional table cap")
        if 3**len(block) > max_local_words:
            raise ValueError("whole local residual table exceeds cap")
        entries = []
        for digits in product(range(3), repeat=len(block)):
            out = list(word)
            for i, d in zip(block, digits):
                out[i] = d
            e = self.energy(out)
            entries.append({"digits": digits, "full_frequency": self.source.value(out),
                            "residual_energy": e, "relative_amplitude": str(t**e)})
        return {"block": block, "attenuation": str(t), "entries": entries,
                "normalizer_squared": str(sum(Fraction(e["relative_amplitude"])**2 for e in entries)),
                "local_evaluations_charged": len(entries), "full_fiber_count_oracle_used": False}

    def reference(self, support, attenuation, max_words=4096, max_work=2_000_000):
        _integer(support, "update support")
        _integer(max_words, "complete reference cap"); _integer(max_work, "complete work cap")
        M, D = self.source.inputs, 3**self.source.inputs
        if support > M:
            raise ValueError("support exceeds original input batch")
        required = D*math.comb(M, support)*3**support
        if D > max_words or required > max_work:
            raise ValueError("whole residual parent reference exceeds cap")
        t = _rational(attenuation, "positive amplitude attenuation", maximum=Fraction(1))
        if t == 0:
            raise ValueError("finite residual temperature required")
        words = tuple(product(range(3), repeat=M)); energies = [self.energy(w) for w in words]
        marked = [i for i, e in enumerate(energies) if e == 0]
        if not marked:
            raise ValueError("occupied target fiber required")
        blocks = tuple(combinations(range(M), support))
        rows = [defaultdict(Fraction) for _ in words]
        for B in blocks:
            other = tuple(i for i in range(M) if i not in B)
            classes = defaultdict(list)
            for i, word in enumerate(words):
                classes[tuple(word[j] for j in other)].append(i)
            for indices in classes.values():
                a = [t**energies[i] for i in indices]; Z = sum(x*x for x in a)
                for i, x in zip(indices, a):
                    rows[i][i] += Fraction(1, len(blocks))
                    for j, y in zip(indices, a):
                        rows[i][j] -= x*y/(Z*len(blocks))
        g = [t**e for e in energies]
        if any(sum(a*g[j] for j, a in row.items()) for row in rows):
            raise ArithmeticError("actual residual Gibbs vector not stationary")
        marked_set = set(marked)
        max_row = max(sum(abs(a) for j, a in rows[i].items() if j not in marked_set) for i in marked)
        max_col = max((sum(abs(rows[i].get(j, Fraction(0))) for i in marked) for j in range(D) if j not in marked_set), default=Fraction(0))
        return {"support": support, "attenuation": str(t), "target_frequency": self.target,
                "complete_words": words, "complete_residual_energies": energies, "marked_word_indices": marked,
                "parent_rows": [[[j, str(a)] for j, a in sorted(row.items()) if a] for row in rows],
                "cross_marked_unmarked_max_row_sum_exact": str(max_row),
                "cross_marked_unmarked_max_col_sum_exact": str(max_col),
                "cross_operator_norm_squared_Schur_upper": str(max_row*max_col),
                "Gibbs_fiber_probability_exact": str(Fraction(len(marked), sum(x*x for x in g))),
                "reference_work_upper": str(required), "reference_is_scalable_preparation": False}


def complete_warm_moment_census():
    z, D = Fraction(1, 4), 9
    all_Z, all_success = [[] for _ in range(D)], []
    words = tuple(product(range(3), repeat=2))
    for flat in product(range(3), repeat=4):
        f = [((0 if w[0] == 0 else flat[w[0]-1])+(0 if w[1] == 0 else flat[2+w[1]-1])) % 3 for w in words]
        for x in range(D):
            Z = sum(Fraction(1) if a == f[x] else z for a in f)/D
            p = Fraction(sum(a == f[x] for a in f), D)
            all_Z[x].append(Z); all_success.append(p/Z)
    means = [sum(a)/len(a) for a in all_Z]
    variances = [sum((v-m)**2 for v in a)/len(a) for a, m in zip(all_Z, means)]
    formula = warm_population_moments(1, 3, 2)
    if any(m != Fraction(formula["mean_normalizer_exact"]) for m in means) or any(v != Fraction(formula["normalizer_variance_exact"]) for v in variances):
        raise ArithmeticError("complete native pointed-pair moments disagree")
    return {"entire_native_label_matrices": 81, "original_word_targets_per_matrix": D,
            "mean_normalizer_by_fixed_original_word": [str(a) for a in means],
            "variance_normalizer_by_fixed_original_word": [str(a) for a in variances],
            "source_weighted_mean_warm_fiber_probability_exact": str(sum(all_success)/len(all_success))}


def run_controls():
    source = random_even_source(2, 4, 5, 89881)
    counts = Counter(source.value(w) for w in product(range(3), repeat=source.inputs))
    target = min(counts, key=lambda y: (-counts[y], y))
    parent = ResidualFiberParent(source, target)
    refs = [parent.reference(1, t) for t in (Fraction(1, 2), Fraction(1, 4))]
    initial = np.array([float(Fraction(1, 2)**e) for e in refs[0]["complete_residual_energies"]], dtype=complex)
    initial /= np.linalg.norm(initial); state = initial.copy()
    for ref in refs:
        H = np.zeros((len(state), len(state)))
        for i, row in enumerate(ref["parent_rows"]):
            for j, a in row:
                H[i, j] = float(Fraction(a))
        state = expm(-.2j*H) @ state
    alpha = refs[0]["Gibbs_fiber_probability_exact"]
    coupling2 = max(Fraction(r["cross_operator_norm_squared_Schur_upper"]) for r in refs)
    _, ac = sqrt_integer_interval(Fraction(alpha).numerator*Fraction(alpha).denominator, 80)
    ac /= Fraction(alpha).denominator
    _, kc = sqrt_integer_interval(coupling2.numerator*coupling2.denominator, 80)
    kc /= coupling2.denominator
    bound = min(Fraction(1), (ac+Fraction(2, 5)*kc)**2)
    measured = float(sum(abs(state[i])**2 for i in refs[0]["marked_word_indices"]))
    if measured > float(bound)+1e-10:
        raise ArithmeticError("cold finite evolution violates actual boundary norm bound")
    return {"status": "RESIDUAL_ENERGY_COLD_WARM_START_BOUND_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_source": {"seed": 89881, "dimension": source.dimension, "modulus": source.modulus,
                "native_level": source.level, "source_inputs": source.inputs,
                "original_ring_labels": source.labels, "native_frequencies": source.frequencies},
            "exact_parent_controls": refs,
            "finite_cold_dynamics": {"warm_start_attenuation": "1/2", "absolute_parent_action": "2/5",
                "initial_fiber_probability_exact": alpha, "cross_operator_norm_squared_upper": str(coupling2),
                "raw_fiber_success_numeric": measured, "raw_fiber_success_upper": str(bound),
                "complete_warm_state_granted_not_prepared": True,
                "numeric_control_is_rigorous_roundoff_certificate": False},
            "complete_warm_moment_census": complete_warm_moment_census(),
            "population_cold_ledgers": [cold_population_certificate(n, q, n*root_digits(q)+8, k, n*n)
                                       for n, q, k in ((32, 81, 3), (128, 243, 5), (512, 729, 6))],
            "hot_temperature_excursions_are_not_excluded": True,
            "arbitrary_quantum_or_hot_schedule_lower_bound": False,
            "efficient_fiber_eraser_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True); REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "efficient_fiber_eraser_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
