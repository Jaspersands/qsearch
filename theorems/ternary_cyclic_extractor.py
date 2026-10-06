"""Known diagonal zero-sum construction gives an exact native cyclic extractor.

LOCAL SOURCE DERIVATION / REVIEW PENDING. The F3 support finder specializes
Ivanyos--Santha Proposition9. No new fast full-depth algorithm is claimed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from cyclotomic_rescaling_gate import ideal_chart
from ternary_covariant_noise import phase

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_cyclic_extractor.json"


def _integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def _vectors(vectors):
    vectors = tuple(tuple(v) for v in vectors)
    if not vectors or not vectors[0] or any(len(v) != len(vectors[0]) for v in vectors):
        raise ValueError("nonempty rectangular curvature vectors required")
    if any(type(x) is not int or x not in (0, 1, 2) for v in vectors for x in v):
        raise ValueError("canonical F3 curvatures required")
    return vectors


def _sum(vectors, indices):
    return tuple(sum(vectors[i][j] for i in indices) % 3 for j in range(len(vectors[0])))


def kernel_relation(vectors):
    vectors = _vectors(vectors)
    n, m = len(vectors[0]), len(vectors)
    if m <= n:
        raise ValueError("more vectors than equations required")
    reduced, rank = nmod_mat([[v[j] for v in vectors] for j in range(n)], 3).rref()
    rows = [tuple(int(reduced[i, j]) for j in range(m)) for i in range(rank)]
    pivots = tuple(next(j for j, a in enumerate(row) if a) for row in rows)
    free = next(j for j in range(m) if j not in pivots)
    coefficients = [0]*m; coefficients[free] = 1
    for pivot, row in zip(pivots, rows):
        coefficients[pivot] = -row[free] % 3
    assert any(coefficients) and all(sum(v[j]*c for v, c in zip(vectors, coefficients)) % 3 == 0 for j in range(n))
    return tuple(coefficients)


def zero_sum_support(vectors):
    """Deterministic F3 specialization of the two-layer square-coefficient sieve."""
    vectors = _vectors(vectors)
    n, size = len(vectors[0]), (len(vectors[0])+1)**2
    if len(vectors) < size:
        raise ValueError("the guaranteed SDE window needs (n+1)^2 vectors")
    vectors = vectors[:size]
    inner, common = [], []
    for group in range(n+1):
        indices = tuple(range(group*(n+1), (group+1)*(n+1)))
        coefficients = kernel_relation([vectors[i] for i in indices])
        first = tuple(i for i, c in zip(indices, coefficients) if c == 1)
        second = tuple(i for i, c in zip(indices, coefficients) if c == 2)
        equal = _sum(vectors, first)
        assert equal == _sum(vectors, second)
        inner.append({"indices": indices, "coefficients": coefficients,
                      "first_support": first, "second_support": second, "common_vector": equal})
        if not first or not second:
            support = first or second
            return {"dimension": n, "window_size": size, "support": support,
                    "case": "inner_zero", "inner_relations": inner, "outer_relation": None,
                    "four_disjoint_equal_sum_supports": None, "Gaussian_kernel_calls": len(inner)}
        common.append(equal)
    coefficients = kernel_relation(common)
    left = tuple(i for i, c in enumerate(coefficients) if c == 1)
    right = tuple(i for i, c in enumerate(coefficients) if c == 2)
    equal = _sum(common, left)
    assert equal == _sum(common, right)
    outer = {"common_vectors": common, "coefficients": coefficients,
             "first_groups": left, "second_groups": right, "common_vector": equal}
    if not left or not right:
        groups = left or right
        support = tuple(sorted(i for group in groups for i in inner[group]["first_support"]))
        case, four = "outer_zero", None
    else:
        four = tuple(tuple(sorted(i for group in groups for i in inner[group][key]))
                     for groups, key in ((left, "first_support"), (left, "second_support"),
                                         (right, "first_support"), (right, "second_support")))
        assert all(four) and len(set(i for block in four for i in block)) == sum(map(len, four))
        assert all(_sum(vectors, block) == equal for block in four)
        support, case = tuple(sorted(i for block in four[:3] for i in block)), "three_equal_disjoint_sums"
    assert support and not any(_sum(vectors, support))
    return {"dimension": n, "window_size": size, "support": support, "case": case,
            "inner_relations": inner, "outer_relation": outer,
            "four_disjoint_equal_sum_supports": four, "Gaussian_kernel_calls": n+2}


def recycle_supports(vectors):
    """Select disjoint supports using ONLY curvatures; unused registers stay live."""
    vectors = _vectors(vectors)
    n, window = len(vectors[0]), (len(vectors[0])+1)**2
    remaining, outputs = list(range(len(vectors))), []
    while len(remaining) >= window:
        selected = tuple(remaining[:window])
        certificate = zero_sum_support([vectors[i] for i in selected])
        support = tuple(selected[i] for i in certificate["support"])
        outputs.append({"support": support, "window_original_indices": selected, "certificate": certificate})
        used = set(support)
        remaining = [i for i in remaining if i not in used]
    return {"dimension": n, "original_inputs": len(vectors), "outputs": outputs,
            "retained_original_registers": tuple(remaining),
            "output_count": len(outputs), "minimum_output_count_guaranteed": len(vectors)//window,
            "selection_reads_only_public_curvatures": True,
            "retained_curvature_labels_claimed_IID": False,
            "odd_children_IID_source_theorem": "LOCAL_DERIVATION_REVIEW_PENDING_DISJOINT_SUPPORTS"}


def _mask(mask):
    mask = tuple(mask)
    if not mask or any(type(x) is not int or x not in (0, 1) for x in mask) or not any(mask):
        raise ValueError("nonempty nonzero binary support mask required")
    return mask


def _word(word, width):
    word = tuple(word)
    if len(word) != width or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("canonical native word of the mask width required")
    return word


def cycle_forward(mask, word):
    mask = _mask(mask); word = _word(word, len(mask))
    pivot = mask.index(1); digit = word[pivot]
    return tuple((x-mask[i]*digit) % 3 if i != pivot else digit for i, x in enumerate(word))


def cycle_inverse(mask, word):
    mask = _mask(mask); word = _word(word, len(mask))
    pivot = mask.index(1); digit = word[pivot]
    return tuple((x+mask[i]*digit) % 3 if i != pivot else digit for i, x in enumerate(word))


def cyclic_recipe(mask):
    mask = _mask(mask); pivot = mask.index(1)
    active = tuple(i for i, x in enumerate(mask) if x)
    return {"source_registers": len(mask), "pivot": pivot, "active_support": active,
            "gates": [{"gate": "SUM_inverse_F3", "control": pivot, "target": i} for i in active if i != pivot],
            "measure_only_active_complement": tuple(i for i in active if i != pivot),
            "inactive_original_registers_untouched": tuple(i for i, x in enumerate(mask) if not x),
            "accepted_outcomes": "ALL", "acceptance_probability": "1",
            "coherent_pointer_mode": "omit complement measurements; retain all original global phases",
            "unknown_inverse_cloning_or_postselection_required": False,
            "exact_qutrit_permutation_recipe_supplied": True,
            "hardware_qubit_gate_synthesis_and_aggregate_error_charged_not_implemented": True}


def curvatures(source):
    if source.level % 2 or not source.inputs:
        raise ValueError("original even-native source required")
    return tuple(tuple((a+c) % 3 for a, c in zip(*pair)) for pair in source.frequencies)


def cyclic_output(source, mask, anchor):
    mask = _mask(mask); anchor = _word(anchor, source.inputs)
    if len(mask) != source.inputs or source.level % 2:
        raise ValueError("matching original even-native source and mask required")
    if anchor[mask.index(1)] != 0:
        raise ValueError("canonical orbit representative has pivot0")
    active = tuple(i for i, x in enumerate(mask) if x)
    if any(_sum(curvatures(source), active)):
        raise ValueError("support curvatures do not sum to zero; odd-source promise invalid")
    words = tuple(tuple((x+j*b) % 3 for x, b in zip(anchor, mask)) for j in range(3))
    values = tuple(source.value(w) for w in words)
    q = source.modulus
    first, second = (tuple((a-b) % q for a, b in zip(values[j], values[0])) for j in (1, 2))
    assert all((c-2*a) % 3 == 0 for a, c in zip(first, second))
    labels = tuple(inverse_frequency_coordinates(a, c, source.level-1) for a, c in zip(first, second))
    return {"original_even_level": source.level, "output_odd_level": source.level-1,
            "original_modulus": str(q), "output_modulus": str(q), "orbit_words": words,
            "relative_first": first, "relative_second": second, "native_odd_output_labels": labels,
            "original_pivot_phase_frequency": values[0], "pivot_phase_can_be_dropped_in_coherent_pointer_mode": False,
            "conditional_active_complement_probability": str(Fraction(1, 3**(len(active)-1))),
            "curvature_mask_reads_unknown_secret": False, "field_shadow_replacement": False,
            "IID_source_promise_requires_curvature_only_support_selection": True,
            "mask_choice_policy_verified_by_this_low_level_function": False,
            "resources": cyclic_recipe(mask)}


def apply_cycle_basis(state, mask):
    mask = _mask(mask)
    if len(mask) > 9 or len(state) != 3**len(mask):
        raise ValueError("dense gate replay capped at9 qutrits")
    state = np.asarray(state, dtype=complex).copy().reshape((3,)*len(mask))
    # Every gate is a computational-basis permutation. No source state inverse.
    for gate in cyclic_recipe(mask)["gates"]:
        output = np.zeros_like(state)
        for word in product(range(3), repeat=len(mask)):
            target = list(word); target[gate["target"]] = (target[gate["target"]]-word[gate["control"]]) % 3
            output[tuple(target)] = state[word]
        state = output
    return state.reshape(-1)


def random_even_source(n, level, inputs, seed):
    _integer(n, "dimension", 1); _integer(level, "even native level", 2); _integer(inputs, "input count", 1)
    if level % 2:
        raise ValueError("even native level required")
    rng = random.Random(seed)
    h0, _, h1 = ideal_chart(level)[0]
    return native_source([[(rng.randrange(h0), rng.randrange(h1)) for _ in range(n)] for _ in range(inputs)], level)


def dense_source_control(n, level, seed):
    source = random_even_source(n, level, (n+1)**2, seed)
    witness = zero_sum_support(curvatures(source))
    active = tuple(witness["support"]); t = len(active)
    if t > 9:
        raise ValueError("this dense control needs at most9 active registers")
    words = list(product(range(3), repeat=t)); secret = tuple((source.modulus-1-j) % source.modulus for j in range(n))
    def parent_value(word):
        original = [0]*source.inputs
        for i, x in zip(active, word): original[i] = x
        return source.value(original)
    original = np.array([phase(sum(a*s for a, s in zip(parent_value(w), secret)), source.modulus)
                         for w in words])/math.sqrt(3**t)
    transformed = apply_cycle_basis(original, (1,)*t).reshape((3,)*t)
    mask = tuple(int(i in active) for i in range(source.inputs))
    records, error = [], 0.
    for complement in product(range(3), repeat=t-1):
        anchor = [0]*source.inputs
        for i, x in zip(active[1:], complement): anchor[i] = x
        output = cyclic_output(source, mask, anchor)
        branch = np.array([transformed[(j, *complement)] for j in range(3)])
        expected = np.array([phase(sum(a*s for a, s in zip(source.value(w), secret)), source.modulus)
                             for w in output["orbit_words"]])/math.sqrt(3**t)
        error = max(error, float(np.max(abs(branch-expected))))
        records.append({"active_complement": complement, "probability": float(np.vdot(branch, branch).real),
                        "output": output, "branch_amplitudes": [[float(a.real), float(a.imag)] for a in branch]})
    assert error < 1e-12 and abs(float(np.vdot(transformed.reshape(-1), transformed.reshape(-1)).real)-1) < 1e-12
    return {"dimension": n, "native_level": level, "native_labels": source.labels,
            "calibration_secret_only": secret, "curvatures": curvatures(source), "support_certificate": witness,
            "active_inputs": t, "parent_pool_inputs": source.inputs, "inactive_inputs_untouched": source.inputs-t,
            "maximum_gate_amplitude_error": error, "all_active_complement_branches": records,
            "measured_pointer_success": "1", "unknown_secret_in_extractor": False}


def conditional_source_census():
    """Entire n1 curvature law, all pointers, and an exhaustive q9 unit minor."""
    strata, pairs = 0, 0
    for curvature in product(range(3), repeat=4):
        support = zero_sum_support([(x,) for x in curvature])["support"]
        pivot = support[0]
        for complement in product(range(3), repeat=len(support)-1):
            anchor = [0]*4
            for i, x in zip(support[1:], complement): anchor[i] = x
            outputs = Counter()
            for a0, ha, hc in product(range(3), repeat=3):
                a = [0]*4; c = list(curvature)
                a[pivot] = a0+3*ha; c[pivot] = (curvature[pivot]-a0) % 3+3*hc
                values = [sum((a[i] if (anchor[i]+j) % 3 == 1 else c[i] if (anchor[i]+j) % 3 == 2 else 0)
                              for i in support) % 9 for j in range(3)]
                outputs[((values[1]-values[0]) % 9, (values[2]-values[0]) % 9)] += 1
            expected = {(a, c) for a, c in product(range(9), repeat=2) if (c-2*a) % 3 == 0}
            assert set(outputs) == expected and set(outputs.values()) == {1}
            strata += 1; pairs += sum(outputs.values())
    return {"curvature_strata": 81, "all_active_pointer_strata": strata,
            "frequency_pairs_evaluated": pairs, "pairs_per_stratum": 27, "multiplicity_per_pair": 1,
            "output_low_first_frequency_uniform_including_zero": True,
            "native_odd_pair_constraint": "c=2a mod3; all27 allowed q9 pairs equally frequent"}


def throughput_ledger(n, digits):
    _integer(n, "dimension", 1); _integer(digits, "root digits", 1)
    levels = digits-1
    return {"dimension": n, "root_digits": digits, "root_lowerings": levels,
            "guaranteed_SDE_label_window": (n+1)**2,
            "minimum_one_output_protocol_original_copies": str((n+1)**levels),
            "fresh_batch_protocol_copies_for_one_final_field_qutrit": str((n+1)**(3*levels)),
            "fresh_batch_protocol_all_levels_acceptance": "1",
            "lower_bound_scope": "disjoint one-odd-child supports and one lower-even child per n+1 odd states",
            "inactive_register_recycling_is_included_in_lower_bound": True,
            "coherent_pointer_or_multi_output_phase_transducers_excluded_from_lower_bound": True,
            "end_to_end_field_decoder_and_full_secret_bootstrap_costs_additional": True,
            "polynomial_in_r_complete_speedup_claim_allowed": False}


def build_report():
    source = random_even_source(4, 16, 100, 88794)
    recycled = recycle_supports(curvatures(source))
    return {"status": "EXACT_NATIVE_CYCLIC_SOURCE_BRIDGE_REVIEW_PENDING_NOT_A_FULL_DEPTH_SPEEDUP",
            "known_support_primitive": "Ivanyos--Santha, arXiv1503.09016, Proposition9 specialized to F3",
            "native_dense_gate_controls": [dense_source_control(n, L, 88700+n) for n, L in ((1, 8), (2, 8))],
            "conditional_exact_source_census": conditional_source_census(),
            "larger_recyclable_native_control": {"dimension": 4, "native_level": 16, "native_labels": source.labels,
                                                 "curvatures": curvatures(source), "result": recycled},
            "one_output_recursion_gates": [throughput_ledger(n, r) for n, r in ((1, 8), (2, 8), (8, 32), (32, 128))],
            "obligations": ["independent review of exact native law conditional on curvature-only support selection",
                            "hardware qutrit-to-qubit compilation and aggregate errors",
                            "retain unknown anchor phases if complement pointers remain coherent",
                            "do not promote label-selected retained curvature law to fresh IID even source",
                            "escape exponential one-output root-depth loss with a genuine multi-output/coherent phase representation",
                            "charge original natural-problem source acquisition separately"],
            "original_source_classically_simulated_without_secret": False,
            "general_corner1_incoming_oracle_supplied": False,
            "nonlinear_pointed_cover_still_used": False,
            "accepted_candidate": False, "new_polynomial_full_depth_quantum_algorithm": False, "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        print(json.dumps({"report": str(REPORT), "cyclic_extractor_acceptance": "1",
                          "recycled_odd_children": report["larger_recyclable_native_control"]["result"]["output_count"],
                          "new_polynomial_full_depth_quantum_algorithm": False}))
    else:
        print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
