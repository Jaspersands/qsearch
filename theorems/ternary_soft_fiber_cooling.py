"""Actual soft-fiber heat-bath parents and a state-specific cooling bound.

LOCAL DERIVATION / REVIEW PENDING. Not a general quantum lower bound.
Temperature schedules may violate the full frequency, unlike a frozen walk.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from ternary_covariant_noise import root_digits
from ternary_cyclic_extractor import random_even_source
from ternary_native_block_walk import NativeBlockHeatbath, _integer
from ternary_native_spectral_access import sqrt_integer_interval

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_SOFT_FIBER_COOLING.md"
REPORT = ROOT / "research/phase_workbench/ternary_soft_fiber_cooling.json"


def _rational(value, name, minimum=Fraction(0), maximum=None):
    if type(value) not in (int, Fraction, str):
        raise ValueError(f"{name} requires an exact rational, not a float or bool")
    try:
        out = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"{name} requires an exact rational") from None
    if (minimum is not None and out < minimum) or (maximum is not None and out > maximum):
        raise ValueError(f"{name} outside its admitted range")
    return out


def class_uniform_residual_squared(size, marked, attenuation):
    """Squared H_B|uniform> norm in ONE class, before division by D."""
    _integer(size, "conditional class size")
    _integer(marked, "conditional marked count", 0)
    if marked > size:
        raise ValueError("marked count exceeds conditional class")
    t = _rational(attenuation, "amplitude attenuation", maximum=Fraction(1))
    if marked in (0, size):
        return Fraction(0)
    return Fraction(marked*(size-marked))*(1-t)**2/(marked+(size-marked)*t*t)


def action_certificate(purity, support, parent_action, marker_action=0, bits=80, one_target=False):
    """Source-weighted necessary success bound, all labels and occupied fibers."""
    purity = _rational(purity, "exact collision purity", maximum=Fraction(1))
    _integer(support, "maximum conditional update support")
    A = _rational(parent_action, "integrated absolute parent coefficients")
    L = _rational(marker_action, "integrated absolute marked-projector coefficients")
    _, sqrt_upper = sqrt_integer_interval(3**support-1, bits)
    bound = min(Fraction(1), purity*(1+A*sqrt_upper+L)**2)
    if type(one_target) is not bool:
        raise ValueError("one-target scope requires a Boolean")
    return {"density_or_collision_purity": str(purity), "maximum_block_support": support,
            "parent_action": str(A), "marked_projector_action": str(L),
            "sqrt_local_class_minus_one_upper": str(sqrt_upper), "sqrt_interval_bits": bits,
            "raw_fiber_success_upper": str(bound),
            "weighting_scope": "one_target_density" if one_target else "original_source_Born_weighted_collision_purity",
            "bound_applies_to_temperature_and_block_policies_depending_on_full_labels_and_target": True,
            "arbitrary_signed_and_nonmonotone_parent_schedules_covered": True,
            "projection_or_postselection_is_not_free_parent_evolution": True,
            "starting_state_is_uniform_native_word_superposition": True,
            "arbitrary_quantum_receiver_lower_bound": False}


def population_certificate(n, q, inputs, support, parent_action, marker_action=0):
    _integer(n, "native dimension")
    root_digits(q)
    _integer(inputs, "original native source inputs")
    _integer(support, "maximum block support")
    if support > inputs:
        raise ValueError("support exceeds original batch width")
    D, G = 3**inputs, q**n
    purity = Fraction(1, G)+Fraction(G-1, G*D)
    return {"dimension": n, "modulus": str(q), "source_inputs": inputs,
            "native_word_dimension": str(D), "full_frequency_group": str(G),
            "expected_source_collision_purity_exact": str(purity),
            "action_bound": action_certificate(purity, support, parent_action, marker_action),
            "requires_all_IID_uniform_full_native_frequency_rows": True,
            "target_frequency_drawn_with_original_Born_weight": True,
            "uniform_per_instance_action_cap_required": True,
            "uses_no_small_collision_or_gap_premise": True,
            "source_weighted_fiber_erasure_squared_error_lower": str(1-Fraction(action_certificate(purity, support, parent_action, marker_action)["raw_fiber_success_upper"])),
            "efficient_fiber_eraser_supplied": False}


class SoftFiberParent:
    """Costed local conditional programs, no whole-fiber preparation oracle."""

    def __init__(self, source, target):
        self.native = NativeBlockHeatbath(source)
        self.source = source
        target = tuple(target)
        if len(target) != source.dimension or any(type(a) is not int or not 0 <= a < source.modulus for a in target):
            raise ValueError("canonical FULL-root target frequency required")
        self.target = target

    def conditional(self, word, block, attenuation, max_local_words=65536):
        word, block = self.native._word(word), self.native._block(block)
        t = _rational(attenuation, "amplitude attenuation", maximum=Fraction(1))
        _integer(max_local_words, "whole local preparation table cap")
        if 3**len(block) > max_local_words:
            raise ValueError("whole local preparation table exceeds cap; no partial kernel")
        outside = list(word)
        for i in block:
            outside[i] = 0
        base = self.source.value(outside)
        entries = []
        for digits in product(range(3), repeat=len(block)):
            local = self.native.local_frequency(block, digits)
            marked = tuple((a+b) % self.source.modulus for a, b in zip(base, local)) == self.target
            entries.append({"digits": digits, "marked": marked, "relative_amplitude": str(Fraction(1) if marked else t)})
        r = sum(e["marked"] for e in entries)
        # At t=0 a wholly unmarked class retains its continuous-limit uniform kernel.
        amplitudes = [Fraction(1) if r == 0 or e["marked"] else t for e in entries]
        Z = sum(a*a for a in amplitudes)
        return {"block": block, "entries": entries, "marked_count": r,
                "kernel_relative_amplitudes": [str(a) for a in amplitudes],
                "kernel_normalizer_squared": str(Z),
                "conditional_class_size": len(entries), "local_evaluations_charged": len(entries),
                "attenuation": str(t), "all_unmarked_zero_temperature_uses_continuous_limit": r == 0 and t == 0,
                "full_fiber_count_oracle_used": False, "hardware_gate_export_supplied": False}

    def reference(self, support, attenuation, max_words=4096, max_work=2_000_000):
        _integer(support, "update support")
        _integer(max_words, "whole reference word cap")
        _integer(max_work, "whole reference local-table work cap")
        if support > self.source.inputs:
            raise ValueError("support exceeds original batch")
        D, M = 3**self.source.inputs, self.source.inputs
        required = D*math.comb(M, support)*3**support
        if D > max_words or required > max_work:
            raise ValueError("whole parent reference exceeds cap; no partial spectral certificate")
        t = _rational(attenuation, "amplitude attenuation", maximum=Fraction(1))
        words = tuple(product(range(3), repeat=M))
        lookup = {w: i for i, w in enumerate(words)}
        values = tuple(self.source.value(w) for w in words)
        marked_indices = [i for i, y in enumerate(values) if y == self.target]
        if not marked_indices:
            raise ValueError("reference cooling requires an occupied original target fiber")
        blocks = tuple(combinations(range(M), support))
        rows = [defaultdict(Fraction) for _ in words]
        certificates, norm_sum = [], Fraction(0)
        for block in blocks:
            others = tuple(i for i in range(M) if i not in block)
            groups = defaultdict(list)
            for i, w in enumerate(words):
                groups[tuple(w[j] for j in others)].append(i)
            residual = Fraction(0)
            class_counts = []
            for indices in groups.values():
                table = self.conditional(words[indices[0]], block, t)
                r = table["marked_count"]
                amplitudes = [Fraction(a) for a in table["kernel_relative_amplitudes"]]
                Z = Fraction(table["kernel_normalizer_squared"])
                residual += class_uniform_residual_squared(len(indices), r, t)/D
                class_counts.append(r)
                for a, i in zip(amplitudes, indices):
                    rows[i][i] += Fraction(1, len(blocks))
                    for b, j in zip(amplitudes, indices):
                        rows[i][j] -= a*b/(Z*len(blocks))
            certificates.append({"block": block, "conditional_marked_counts": class_counts,
                                 "H_block_uniform_residual_squared_exact": str(residual)})
            norm_sum += residual/len(blocks)
        hu = [sum(row.values()) for row in rows]
        squared = sum(a*a for a in hu)/D
        p = Fraction(len(marked_indices), D)
        if squared > norm_sum or norm_sum > p*(3**support-1):
            raise ArithmeticError("exact native residual violates Jensen/action bound")
        g = [Fraction(1) if i in marked_indices else t for i in range(D)]
        if any(sum(a*g[j] for j, a in row.items()) for row in rows):
            raise ArithmeticError("coherent Gibbs vector is not stationary")
        return {"support": support, "attenuation": str(t), "target_frequency": self.target,
                "complete_words": words, "full_frequency_values": values, "marked_word_indices": marked_indices,
                "parent_rows": [[[j, str(a)] for j, a in sorted(row.items()) if a] for row in rows],
                "local_block_certificates": certificates,
                "fiber_density": str(p), "parent_uniform_residual_squared_exact": str(squared),
                "mean_local_uniform_residual_squared_exact": str(norm_sum),
                "uniform_residual_squared_upper": str(p*(3**support-1)),
                "coherent_Gibbs_normalizer_squared": str(len(marked_indices)+(D-len(marked_indices))*t*t),
                "coherent_Gibbs_fiber_probability_exact": str(p/(p+(1-p)*t*t)),
                "reference_work_upper": str(required), "reference_enumerates_complete_native_word_cube": True,
                "reference_is_scalable_compiler": False}


def dense_parent(reference):
    D = len(reference["complete_words"])
    out = np.zeros((D, D))
    for i, row in enumerate(reference["parent_rows"]):
        for j, a in row:
            out[i, j] = float(Fraction(a))
    return out


def evolve_reference(parent, schedule, max_words=4096):
    """Finite dynamics only; no favorable eigenvalue is called an algorithm."""
    refs, state, A, L = [], None, Fraction(0), Fraction(0)
    for segment in schedule:
        duration = _rational(segment["duration"], "evolution duration")
        coefficient = _rational(segment.get("coefficient", "1"), "signed parent coefficient", minimum=None)
        marker = _rational(segment.get("marker_coefficient", "0"), "signed marker coefficient", minimum=None)
        ref = parent.reference(segment["support"], segment["attenuation"], max_words=max_words)
        if state is None:
            state = np.ones(len(ref["complete_words"]), dtype=complex)/math.sqrt(len(ref["complete_words"]))
        H = float(coefficient)*dense_parent(ref)
        H[ref["marked_word_indices"], ref["marked_word_indices"]] += float(marker)
        state = expm(-1j*float(duration)*H) @ state
        A += duration*abs(coefficient)
        L += duration*abs(marker)
        refs.append(ref)
    if not refs:
        raise ValueError("nonempty fully charged cooling schedule required")
    support = max(r["support"] for r in refs)
    certificate = action_certificate(Fraction(refs[0]["fiber_density"]), support, A, L, one_target=True)
    success = float(sum(abs(state[i])**2 for i in refs[0]["marked_word_indices"]))
    if abs(float(np.vdot(state, state).real)-1) > 1e-10 or success > float(Fraction(certificate["raw_fiber_success_upper"]))+1e-10:
        raise ArithmeticError("finite dynamics disagrees with charged state-transfer bound")
    return {"schedule": schedule, "exact_parent_references": refs, "action_certificate": certificate,
            "raw_fiber_success_numeric": success,
            "numeric_simulation_is_asymptotic_or_rigorous_roundoff_certificate": False}


def complete_population_control():
    """Independent full native LABEL population, not a secret-selected cohort."""
    from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
    n, q, M, total = 1, 3, 2, 0
    mean = Fraction(0)
    for flat in product(range(q), repeat=2*M):
        labels = tuple((inverse_frequency_coordinates(flat[2*i], flat[2*i+1], 2),) for i in range(M))
        source = native_source(labels, 2)
        counts = defaultdict(int)
        for w in product(range(3), repeat=M):
            counts[source.value(w)] += 1
        mean += Fraction(sum(c*c for c in counts.values()), 3**(2*M))
        total += 1
    mean /= total
    expected = Fraction(1, q**n)+Fraction(q**n-1, q**n*3**M)
    if mean != expected:
        raise ArithmeticError("complete native population disagrees with pair collision law")
    return {"dimension": n, "modulus": q, "source_inputs": M,
            "entire_IID_label_matrices_checked": total, "mean_collision_purity_exact": str(mean)}


def run_controls():
    source = random_even_source(2, 4, 5, 89881)
    counts = defaultdict(int)
    for w in product(range(3), repeat=source.inputs):
        counts[source.value(w)] += 1
    target = min(counts, key=lambda y: (-counts[y], y))
    parent = SoftFiberParent(source, target)
    refs = [parent.reference(k, t) for k, t in ((1, 1), (1, Fraction(1, 3)), (1, Fraction(1, 27)), (1, 0), (2, Fraction(1, 3)))]
    schedules = [
        [{"support": 1, "attenuation": "1/3", "duration": "1/5"},
         {"support": 1, "attenuation": "1/27", "duration": "1/5"},
         {"support": 1, "attenuation": "0", "duration": "1/5"}],
        [{"support": 1, "attenuation": "1/27", "duration": "1/10", "coefficient": "-2", "marker_coefficient": "3"},
         {"support": 1, "attenuation": "1", "duration": "1/10"},
         {"support": 2, "attenuation": "1/3", "duration": "1/10"}],
    ]
    p = len(refs[0]["marked_word_indices"])/len(refs[0]["complete_words"])
    # Full-block positive control: reflection about the explicit bisector maps u to v.
    u = np.ones(3**source.inputs)/math.sqrt(3**source.inputs)
    v = np.zeros(len(u)); v[refs[0]["marked_word_indices"]] = 1/math.sqrt(counts[target])
    bisector = (u+v)/np.linalg.norm(u+v)
    reflected = 2*bisector*np.dot(bisector, u)-u
    purity = Fraction(sum(c*c for c in counts.values()), len(u)**2)
    return {"status": "NATIVE_SOFT_FIBER_COOLING_STATE_TRANSFER_BOUND_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_source": {"seed": 89881, "dimension": source.dimension, "modulus": source.modulus,
                              "native_level": source.level, "source_inputs": source.inputs,
                              "original_ring_labels": source.labels, "native_frequencies": source.frequencies,
                              "seed_is_population_scaling_evidence": False},
            "exact_parent_controls": refs,
            "finite_dynamics_controls": [evolve_reference(parent, s) for s in schedules],
            "source_collision_purity_exact": str(purity),
            "source_weighted_action_control": action_certificate(purity, 1, 1),
            "complete_native_label_population_control": complete_population_control(),
            "population_scaling_ledgers": [population_certificate(n, q, n*root_digits(q)+8, k, n*n)
                                            for n, q, k in ((8, 9, 1), (32, 81, 3), (128, 243, 5), (512, 729, 6))],
            "global_block_positive_control": {"all_words_enumerated": len(u),
                "support": source.inputs, "parent_action_numeric": math.pi,
                "bisector_amplitude_attenuation_numeric": math.sqrt(p)/(1+math.sqrt(p)),
                "target_vector_error_numeric": float(np.linalg.norm(reflected-v)),
                "full_table_preparation_is_charged_exponential": True,
                "positive_control_refutes_general_Hamiltonian_lower_bound": True},
            "gate_recipe": "Enumerate ALL3^k local assignments, compute full F=y flags, synthesize normalized weights (1,t), clean reversible scratch; conjugate a known-zero reflection to implement the conditional projector. No whole-fiber table.",
            "quantum_hardware_gate_export_supplied": False, "efficient_fiber_eraser_supplied": False,
            "arbitrary_quantum_receiver_lower_bound": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "exact_parent_controls": len(report["exact_parent_controls"]),
                      "finite_dynamics_controls": len(report["finite_dynamics_controls"]),
                      "efficient_fiber_eraser_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
