"""Native full-label coherent-edge least-trit receiver, with charged search.

LOCAL DERIVATION / REVIEW PENDING. No classical pair finder is needed, but
time is exponential. Dense controls are calibration, not a scalable simulator
or an accepted algorithm candidate. Source acquisition remains separate.
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
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from dcp_coherent_edge_sampling import geometric_kernel, marked_amplitude, schedule_certificate
from ternary_covariant_noise import phase
from ternary_cyclic_extractor import _integer, _word, random_even_source
from ternary_pair_collimation import pointed_unit_minor

REPORT = ROOT / "research/phase_workbench/ternary_coherent_edge_receiver.json"
DERIVATION = ROOT / "research/TERNARY_COHERENT_EDGE_RECEIVER.md"


def digits(rank, width):
    _integer(width, "native width", 1)
    if type(rank) is not int or not 0 <= rank < 3**width:
        raise ValueError("canonical base-three word rank required")
    out = []
    for _ in range(width):
        rank, digit = divmod(rank, 3)
        out.append(digit)
    return tuple(out)


def rank(word):
    word = _word(word, len(word))
    if not word:
        raise ValueError("nonempty native word required")
    return sum(digit * 3**i for i, digit in enumerate(word))


def offset(width, index):
    _integer(width, "native width", 1)
    count = 3**width - 1
    padded = 1 << (count - 1).bit_length()
    if type(index) is not int or not 0 <= index < padded:
        raise ValueError("index outside padded offset domain")
    return digits(index + 1, width) if index < count else None


def add(word, delta):
    word = _word(word, len(word)); delta = _word(delta, len(word))
    return tuple((a + b) % 3 for a, b in zip(word, delta))


def negative(delta):
    return tuple(-d % 3 for d in delta)


def orientation_tape(width, word, index, bit=0, inverse=False):
    """Reversible native edge orientation, including the full padding domain."""
    _integer(width, "native width", 1); word = _word(word, width)
    if type(bit) is not int or bit not in (0, 1) or type(inverse) is not bool:
        raise ValueError("orientation bit and Boolean inverse required")
    delta = offset(width, index)
    if delta is None:
        return word, index, bit
    if inverse:
        if bit:
            delta = negative(delta)
            index = rank(delta) - 1
            word = add(word, negative(delta))
        bit ^= int(next(d for d in delta if d) == 2)
    else:
        bit ^= int(next(d for d in delta if d) == 2)
        if bit:
            word = add(word, delta)
            index = rank(negative(delta)) - 1
    return word, index, bit


@dataclass(frozen=True)
class NativeEdgeProgram:
    source: object
    coordinate: int = 0

    def __post_init__(self):
        s = self.source
        if type(s.level) is not int or s.level < 2 or s.level % 2:
            raise ValueError("original even native source required")
        if s.modulus != 3**(s.level // 2) or s.inputs != s.dimension * (s.level // 2) - 2 or s.inputs < 1:
            raise ValueError("underfull native source with M=n*r-2 required")
        if native_source(s.labels, s.level).frequencies != s.frequencies:
            raise ValueError("native labels and frequency chart must agree")
        if type(self.coordinate) is not int or not 0 <= self.coordinate < s.dimension:
            raise ValueError("canonical target coordinate required")

    @property
    def width(self): return self.source.inputs

    @property
    def size(self): return 3**self.width

    @property
    def padded(self): return 1 << (self.size - 2).bit_length()

    def target_delta(self, first, second):
        delta = tuple((b-a) % self.source.modulus for a, b in zip(first, second))
        Q = self.source.modulus // 3
        if any(a for i, a in enumerate(delta) if i != self.coordinate) or delta[self.coordinate] not in (Q, 2*Q):
            return 0
        return delta[self.coordinate] // Q

    def marked(self, word, index):
        word = _word(word, self.width); d = offset(self.width, index)
        return d is not None and bool(self.target_delta(self.source.value(word), self.source.value(add(word, d))))


def population_certificate(n, r, tail_bits=16):
    _integer(n, "secret dimension", 1); _integer(r, "root digits", 1)
    if n*r < 5:
        raise ValueError("constant advantage certificate requires n*r>=5")
    M = n*r - 2; D = 3**M; G = 3**(n*r); A = D-1
    P = 1 << (A-1).bit_length(); schedule = schedule_certificate(P, tail_bits)
    lam = Fraction(2*A, G)
    second = lam*lam + lam*(1-Fraction(2, G))
    cap = 8; mass = lam - Fraction(2, cap)*second
    kernel = Fraction(1, (1+8*cap)**2)
    universal_mass = Fraction(5, 36)
    universal_signal = universal_mass*kernel
    advantage = (universal_signal - schedule["tail_probability_upper"])/3
    if not (Fraction(1, 5) <= lam <= Fraction(2, 9) and P >= 2*cap and mass >= universal_mass):
        raise ArithmeticError("native population moment certificate failed")
    return {"dimension": n, "root_digits": r, "source_qutrits": M,
            "native_words": str(D), "full_frequency_group": str(G), "valid_offsets": str(A),
            "schedule": schedule, "useful_edge_probability": Fraction(2, G),
            "mean_degree": lam, "second_degree_moment": second,
            "bounded_degree_oriented_mass_lower": mass, "universal_mass_lower": universal_mass,
            "degree_cap_for_proof_only": cap, "kernel_lower": kernel,
            "universal_infinite_interference_lower": universal_signal,
            "raw_trit_advantage_after_charged_abort_lower": advantage,
            "positive_advantage_certified": advantage > 0,
            "label_law": "ALL_IID_UNIFORM_NATIVE_FULL_FREQUENCY_ROWS",
            "secret_scope": "EVERY_FIXED_SECRET_AVERAGED_OVER_LABELS_AND_SHARED_PUBLIC_TIME",
            "query_model": "EXPLICIT_REVERSIBLE_FULL_PUBLIC_LABEL_ARITHMETIC",
            "full_table_access_required": False, "classical_pair_finder_required": False,
            "degree_counting_required": False, "bounded_degree_vertices_selected": False,
            "uniform_public_index_reflection_only": True, "unknown_source_reflection_required": False,
            "workspace_bound": "poly(n,r); original source, index, orientation and cleaned arithmetic scratch",
            "mean_query_scaling": "O(3^(n*r/2)); polynomial arithmetic factors and public coin draws charged",
            "polynomial_runtime_proved": False, "new_quantum_speedup_proved": False,
            "cyclic_DHSP_vector_source_acquisition_supplied": False,
            "hardware_gate_export_implemented": False, "large_source_execution": False}


def source_class_trimming_bound(n, r, squared_singular_threshold=None):
    _integer(n, "secret dimension", 1); _integer(r, "root digits", 1)
    if n*r < 3:
        raise ValueError("underfull native source requires n*r>=3")
    D = 3**(n*r-2); G = 9*D
    threshold = Fraction(1, (n*r)**2) if squared_singular_threshold is None else Fraction(squared_singular_threshold)
    if not 0 < threshold <= 1:
        raise ValueError("normalized squared singular threshold in (0,1] required")
    count = (D*threshold.numerator+threshold.denominator-1)//threshold.denominator
    excess = Fraction(D-1, G)
    mass = Fraction(1) if count <= 1 else min(Fraction(1), excess/(count-1))
    return {"dimension": n, "root_digits": r, "native_words": str(D), "full_frequency_group": str(G),
            "squared_singular_threshold": threshold, "minimum_retained_class_size": str(count),
            "exact_mean_source_weighted_excess_class_size": excess,
            "mean_singleton_source_mass_lower": 1-excess,
            "mean_retained_source_mass_upper": mass,
            "raw_trit_advantage_upper_if_discarded_outputs_guessed_uniform": 2*mass/3,
            "scope": "GLOBAL_PUBLIC_FOURIER_ERASURE_CLASSES_WITH_c_OVER_D_ABOVE_THRESHOLD",
            "source_law": "ALL_IID_NATIVE_LABELS_AND_UNIFORM_ORIGINAL_WORD_WEIGHT",
            "large_classes_assumed_physically_filterable": False,
            "conditioned_success_renormalization_granted": False,
            "lower_bound_against_other_normalizations_or_quantum_receivers": False}


def short_grover_template_bound(n, r, maximum_iterations):
    _integer(maximum_iterations, "hard iteration cap", 0)
    c = population_certificate(n,r); P=c["schedule"]["padded_supports"]
    bound=min(Fraction(2,3),c["mean_degree"]*(2*maximum_iterations+1)**2/(3*P))
    return {"dimension": n, "root_digits": r, "maximum_iterations": maximum_iterations,
            "padded_offset_domain": P, "native_mean_degree": c["mean_degree"],
            "raw_trit_advantage_upper": bound,
            "amplitude_inequality": "abs(sin((2*t+1)*theta)) <= (2*t+1)*sin(theta)",
            "scope": "UNCHANGED_CLEAN_PUBLIC_INDEX_GROVER_EDGE_TEMPLATE_WITH_HARD_TIME_CAP",
            "label_dependent_shared_time_within_cap_allowed": True,
            "failure_and_all_IID_source_labels_charged": True,
            "rules_out_general_quantum_measurements_or_modified_oracles": False}


def graph(program, max_cells=30_000):
    """Explicit native source graph ONLY for bounded physical controls."""
    _integer(max_cells, "complete dense cell budget", 1)
    D, P = program.size, program.padded
    if D*P > max_cells:
        raise ValueError("complete dense diagnostic budget exceeded; no partial proof")
    words = [digits(i, program.width) for i in range(D)]
    values = [program.source.value(w) for w in words]
    marked = np.zeros((D, P), dtype=bool)
    neighbor = np.full((D, P), -1, dtype=int)
    reverse = np.full(P, -1, dtype=int)
    for i in range(D-1):
        d = offset(program.width, i); reverse[i] = rank(negative(d))-1
        for x, word in enumerate(words):
            y = rank(add(word, d)); neighbor[x, i] = y
            marked[x, i] = bool(program.target_delta(values[x], values[y]))
    if not np.array_equal(marked[:, :D-1], marked[neighbor[:, :D-1], reverse[:D-1][None, :]]):
        raise ArithmeticError("native informative edge predicate must be symmetric")
    return words, values, marked, neighbor, reverse


def explicit_rows(program, iterations):
    if type(iterations) is not int or not 0 <= iterations <= 1024:
        raise ValueError("bounded nonnegative physical iteration control required")
    words, values, marked, neighbor, reverse = graph(program)
    state = np.full(marked.shape, 1/math.sqrt(program.padded))
    for _ in range(iterations):
        state *= np.where(marked, -1, 1)
        state = 2*state.mean(axis=1, keepdims=True)-state
    return words, values, marked, neighbor, reverse, state


def physical_control(program, iterations, secret, retain_endpoint_tag=False):
    secret = tuple(secret)
    if len(secret) != program.source.dimension or any(type(s) is not int or not 0 <= s < program.source.modulus for s in secret):
        raise ValueError("canonical full calibration secret required")
    if type(retain_endpoint_tag) is not bool:
        raise ValueError("Boolean dirty-workspace countercontrol required")
    words, values, marked, neighbor, reverse, state = explicit_rows(program, iterations)
    D = program.size; degrees = marked.sum(axis=1).tolist()
    psi = [phase(sum(a*s for a, s in zip(v, secret)), program.source.modulus)/math.sqrt(D) for v in values]
    groups = {}
    for x, i in zip(*np.nonzero(marked)):
        rep, canonical, bit = orientation_tape(program.width, words[x], int(i))
        key = (rank(rep), canonical, int(i) if retain_endpoint_tag else None)
        groups.setdefault(key, np.zeros(2, dtype=complex))[bit] += psi[x]*state[x, i]
    F3 = np.array([[phase(-a*b, 3)/math.sqrt(3) for b in range(3)] for a in range(3)])
    heralded = float(np.sum(state*state*marked)/D)
    correct = (1-heralded)/3; total = 1-heralded
    for (rep, i, _), amplitudes in groups.items():
        y = rank(add(words[rep], offset(program.width, i)))
        delta = program.target_delta(values[rep], values[y])
        probabilities = abs(F3@np.array([*amplitudes, 0j]))**2
        correct += float(probabilities[delta*(secret[program.coordinate] % 3) % 3])
        total += float(probabilities.sum())
    xs, inds = np.nonzero(marked)
    G = float(np.sum(state[xs, inds]*state[neighbor[xs, inds], reverse[inds]])/D)
    predicted = 1/3 if retain_endpoint_tag else (1+G)/3
    amplitude_error = max((abs(state[x, i]-marked_amplitude(degrees[x], program.padded, iterations))
                           for x, i in zip(xs, inds)), default=0.)
    return {"iterations": iterations, "calibration_secret_only": secret,
            "heralded_probability": heralded, "oriented_interference": G,
            "raw_correct_probability": correct, "predicted_raw_correct_probability": predicted,
            "Born_score_residual": abs(correct-predicted), "probability_normalization_residual": abs(total-1),
            "Grover_row_norm_residual": float(np.max(abs(np.sum(state*state, axis=1)-1))),
            "marked_amplitude_residual": amplitude_error,
            "retained_endpoint_specific_tag_countercontrol": retain_endpoint_tag,
            "conditional_normalization_used": False, "unknown_secret_used_to_select_edges": False,
            "source_dense_cells": D*program.padded, "dense_calibration_not_scalable_storage": True}


def geometric_control(program, tail_bits=16):
    _, _, marked, neighbor, reverse = graph(program)
    D, P = marked.shape; degrees = marked.sum(axis=1).tolist()
    xs, inds = np.nonzero(marked)
    infinite = sum((geometric_kernel(degrees[x], degrees[neighbor[x, i]], P)/D
                    for x, i in zip(xs.tolist(), inds.tolist())), Fraction(0))
    schedule = schedule_certificate(P, tail_bits)
    state = np.full((D, P), 1/math.sqrt(P))
    probability = float(schedule["stop_probability"]); finite = 0.
    for _ in range(schedule["cutoff"]):
        G = float(np.sum(state[xs, inds]*state[neighbor[xs, inds], reverse[inds]])/D)
        finite += probability*G
        state *= np.where(marked, -1, 1)
        state = 2*state.mean(axis=1, keepdims=True)-state
        probability *= float(schedule["rho"])
    tail = float(schedule["rho"]**schedule["cutoff"])
    if infinite < 0 or abs(finite-float(infinite)) > tail+2e-12 or tail > float(schedule["tail_probability_upper"])+2e-12:
        raise ArithmeticError("shared-time kernel or charged clipping control failed")
    return {"infinite_interference_exact": infinite, "truncated_interference": finite,
            "truncated_raw_trit_advantage": finite/3, "actual_abort_probability": tail,
            "tail_error": abs(finite-float(infinite)), "certified_tail_upper": schedule["tail_probability_upper"],
            "degrees": degrees, "oriented_edges": len(xs),
            "per_label_constant_advantage_claimed": False, "shared_time_across_source": True,
            "no_edge_labels_retained_in_source_population_estimate": True}


def fiber_structure_control(program):
    """Expose exact tripartite structure WITHOUT granting a fiber transform."""
    words, values, marked, _, _ = graph(program)
    D = program.size; Q = program.source.modulus//3; j = program.coordinate
    fibers = {}
    for x, value in enumerate(values):
        syndrome = tuple(a % Q if i == j else a for i, a in enumerate(value))
        groups = fibers.setdefault(syndrome, [[], [], []])
        groups[value[j]//Q].append(x)
    records = []; collisions = 0; oriented = 0; optimal = 0.; max_residual = 0.
    # The source is in the uniform span of each FULL frequency class.
    # No basis or count is passed to the actual coherent-edge receiver.
    for syndrome, groups in sorted(fibers.items()):
        counts = [len(g) for g in groups]; C = sum(counts)
        indices = [x for group in groups for x in group]
        degrees = [C-c for c in counts]
        compressed = np.array([[0. if a == b else math.sqrt(counts[a]*counts[b])
                                for b in range(3)] for a in range(3)])
        weights = np.zeros((len(indices), 3))
        location = {x: i for i, x in enumerate(indices)}
        for h, group in enumerate(groups):
            for x in group:
                weights[location[x], h] = 1/math.sqrt(len(group))
        adjacency = weights@compressed@weights.T
        expected = np.array([[float(any(x in groups[a] and y in groups[b]
                                       for a in range(3) for b in range(3) if a != b))
                              for y in indices] for x in indices])
        residual = float(np.max(abs(adjacency-expected)))
        max_residual = max(max_residual, residual)
        for a, group in enumerate(groups):
            for x in group:
                if int(marked[x].sum()) != degrees[a]:
                    raise ArithmeticError("actual native graph degree must equal tripartite class degree")
                for b, other in enumerate(groups):
                    for y in other:
                        i = rank(tuple((v-u) % 3 for u, v in zip(words[x], words[y])))-1
                        actual = False if x == y else bool(marked[x, i])
                        if actual != (a != b):
                            raise ArithmeticError("native adjacency must equal exact class-incidence factorization")
        c0, c1, c2 = counts; edges = C*C-sum(c*c for c in counts)
        collisions += sum(c*c for c in counts); oriented += edges
        optimum = sum(math.sqrt(c) for c in counts)**2/(3*D); optimal += optimum
        records.append({"nuisance_syndrome": syndrome, "class_counts": counts, "word_ranks_by_high_trit": groups,
                        "class_degrees": degrees, "oriented_edges": edges,
                        "compressed_adjacency_characteristic": ["1", "0", str(-(c0*c1+c0*c2+c1*c2)), str(-2*c0*c1*c2)],
                        "compressed_adjacency_rank": 3 if c0*c1*c2 else 2 if sum(c>0 for c in counts) == 2 else 0,
                        "uniform_class_erasure_singular_values_squared": [Fraction(c, D) for c in counts],
                        "ideal_uniform_class_trine_raw_contribution": optimum,
                        "exact_class_incidence_factorization_checked": True})
    # Reversible F evaluation followed by projection of every original word
    # qutrit onto its PUBLIC uniform state has amplitude 1/sqrt(D) per word.
    # This is a costed Kraus operator, not deterministic coherent rank erasure.
    success = Fraction(collisions, D*D)
    population_mean = Fraction(1, D)+Fraction(D-1, D*program.source.group_size)
    if oriented != int(marked.sum()) or max_residual > 2e-12:
        raise ArithmeticError("tripartite compression must reconstruct the entire native graph")
    return {"status": "EXACT_NATIVE_TRIPARTITE_GEOMETRY_NOT_AN_EFFICIENT_COMPILER",
            "complete_nuisance_fibers": records, "words_enumerated": D,
            "native_uniform_source_words_partitioned": sum(sum(r["class_counts"]) for r in records),
            "exact_full_frequency_collision_count": collisions,
            "raw_public_Fourier_erasure_success": success,
            "mean_erasure_success_over_all_IID_labels": population_mean,
            "singleton_class_singular_value_squared": Fraction(1, D),
            "ideal_class_compressed_raw_trit_success": optimal,
            "compressed_adjacency_reconstruction_residual": max_residual,
            "class_counts_or_uniform_basis_given_to_receiver": False,
            "erasure_success_renormalization_free": False,
            "coherent_uniform_class_inverse_preparation_implemented": False,
            "native_inverse_singular_scale": "sqrt(D/c_min); small blocks do not remove native access normalization",
            "generic_quantum_lower_bound_proved": False, "quantum_speedup_proved": False}


def translation_control(program):
    """Exact full-root character obstruction, not a general Fourier no-go."""
    q = program.source.modulus; rows = []; failure = None
    for i, (a, c) in enumerate(program.source.frequencies):
        increments = [a, tuple((v-u) % q for u, v in zip(a, c)), tuple(-v % q for v in c)]
        linear = increments[0] == increments[1] == increments[2]
        rows.append({"source_wire": i, "three_cycle_increment_rows": increments,
                     "full_modulus_cycle_is_linear": linear})
        if not linear and failure is None:
            j = next(j for j in range(program.source.dimension) if len({row[j] for row in increments}) > 1)
            base_words = [tuple(d if k == i else 0 for k in range(program.width)) for d in range(3)]
            actual = [tuple((b-a) % q for a, b in zip(program.source.value(w), program.source.value(base_words[(d+1)%3])))
                      for d, w in enumerate(base_words)]
            if actual != increments:
                raise ArithmeticError("full native cycle increments must replay actual label arithmetic")
            failure = {"source_wire": i, "frequency_coordinate": j, "base_words": base_words,
                       "same_native_unit_offset": tuple(int(k == i) for k in range(program.width)),
                       "actual_full_frequency_increment_rows": actual}
    r = program.source.level//2; n = program.source.dimension
    return {"status": "FULL_ROOT_NATIVE_TRANSLATION_CHARACTER_SCOPE_CONTROL",
            "native_rows": rows, "first_exact_cycle_disagreement": failure,
            "native_F_is_group_homomorphism": failure is None,
            "all_secret_phase_states_are_F3_word_characters": failure is None,
            "necessary_and_sufficient_per_wire": "c=2*a modq AND 3*a=0 modq",
            "IID_probability_of_exact_homomorphism": {"base": 3, "negative_exponent": n*program.width*(2*r-1)},
            "full_root_not_modulo_three_checked": True, "dense_native_words_enumerated": 0,
            "rules_out_general_structure_aware_Fourier_transforms": False,
            "native_informative_graph_invariance_inferred_from_nonhomomorphism": False,
            "quantum_algorithm_no_go_proved": False}


def erasure_physical_control(program, secret):
    """Actual known F evaluation and native Fourier gates, with charged failure."""
    secret = tuple(secret); s = program.source; D = program.size; G = s.group_size
    if D*G > 100_000:
        raise ValueError("complete Fourier-erasure dense diagnostic budget exceeded")
    if len(secret) != s.dimension or any(type(v) is not int or not 0 <= v < s.modulus for v in secret):
        raise ValueError("canonical full erasure calibration secret required")
    state = np.zeros((D, G), dtype=complex); counts = {}; values = {}
    for x in range(D):
        value = s.value(digits(x, program.width))
        frequency_rank = sum(v*s.modulus**i for i, v in enumerate(value))
        state[x, frequency_rank] = phase(sum(a*v for a, v in zip(value, secret)), s.modulus)/math.sqrt(D)
        counts[frequency_rank] = counts.get(frequency_rank, 0)+1; values[frequency_rank] = value
    state = state.reshape((3,)*program.width+(G,))
    F3 = np.array([[phase(-a*b, 3)/math.sqrt(3) for b in range(3)] for a in range(3)])
    for axis in range(program.width):
        state = np.moveaxis(np.tensordot(F3, state, axes=(1, axis)), 0, axis)
    output = state[(0,)*program.width]
    predicted = np.zeros(G, dtype=complex)
    for f, count in counts.items():
        predicted[f] = count*phase(sum(a*v for a, v in zip(values[f], secret)), s.modulus)/D
    exact_success = Fraction(sum(c*c for c in counts.values()), D*D)
    return {"calibration_secret_only": secret, "actual_raw_erasure_success": float(np.sum(abs(output)**2)),
            "predicted_raw_erasure_success_exact": exact_success,
            "full_label_output_amplitude_residual": float(np.max(abs(output-predicted))),
            "whole_unitary_norm_residual": abs(float(np.sum(abs(state)**2))-1),
            "charged_rejection_probability": 1-float(np.sum(abs(output)**2)),
            "dense_diagnostic_cells": D*G, "source_registers_measured_only_after_F_evaluation": True,
            "output_success_renormalized": False, "unknown_source_inverse_used": False,
            "uniform_class_inverse_preparation_implemented": False}


def natural_moment_control():
    # ALL q^2 full frequency pairs at n=1,r=3,M=1, with zero exclusions.
    q = 27; first = second = 0; assignments = 0; homomorphisms = 0; singleton_words = 0
    for a, c in product(range(q), repeat=2):
        source = native_source([[inverse_frequency_coordinates(a, c, 6)]], 6)
        p = NativeEdgeProgram(source); _, _, marked, _, _ = graph(p)
        degrees = marked.sum(axis=1).tolist()
        first += sum(degrees); second += sum(d*d for d in degrees); assignments += 3
        homomorphisms += int(c == 2*a % q and 3*a % q == 0)
        singleton_words += sum([0,a,c].count(v)==1 for v in (0,a,c))
    lam = Fraction(4, q); expected_second = lam*lam+lam*(1-Fraction(2, q))
    if Fraction(first, assignments) != lam or Fraction(second, assignments) != expected_second:
        raise ArithmeticError("entire native label census violates degree moment derivation")
    if homomorphisms != 3:
        raise ArithmeticError("exact native full-root homomorphism count must equal three")
    return {"dimension": 1, "root_digits": 3, "source_qutrits": 1,
            "complete_native_label_pairs": q*q, "complete_label_word_assignments": assignments,
            "mean_degree": Fraction(first, assignments), "second_degree_moment": Fraction(second, assignments),
            "full_root_homomorphism_label_pairs": homomorphisms,
            "singleton_native_word_assignments": singleton_words,
            "constant_advantage_large_root_bound_applied_here": False}


def unit_minor_controls(width=2):
    words = [digits(i, width) for i in range(3**width)]; controls = []
    for base in words:
        for first in words:
            for second in words:
                if len({base, first, second}) != 3:
                    continue
                controls.append({"base": base, "first": first, "second": second,
                                 **pointed_unit_minor(base, first, second)})
    return controls


def _jsonable(value):
    if isinstance(value, Fraction): return str(value)
    if type(value) is int and abs(value) > 2**53-1: return str(value)
    if isinstance(value, dict): return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)): return [_jsonable(v) for v in value]
    return value


def build_report():
    populations = [population_certificate(n, r) for n, r in ((1, 5), (2, 3), (1, 16), (2, 16), (1, 64))]
    finite = []
    for n, r, seed in ((1, 5, 98301), (1, 5, 98302), (1, 5, 98303), (2, 3, 98304)):
        source = random_even_source(n, 2*r, n*r-2, seed)
        for j in range(n):
            p = NativeEdgeProgram(source, j)
            secrets = [(0,)*n, tuple((3*(i+1)) % source.modulus for i in range(n)),
                       tuple((source.modulus-1-i) % source.modulus for i in range(n))]
            physical = [physical_control(p, t, s) for t in (0, 1, 2, 5, 11) for s in secrets]
            dirty = physical_control(p, 1, secrets[-1], True)
            finite.append({"dimension": n, "root_digits": r, "seed": seed, "coordinate": j,
                           "native_labels": source.labels, "full_frequencies": source.frequencies,
                           "physical_controls": physical, "dirty_scratch_control": dirty,
                           "geometric_control": geometric_control(p),
                           "fiber_structure_control": fiber_structure_control(p),
                           "translation_control": translation_control(p),
                           "erasure_physical_control": erasure_physical_control(p, secrets[-1]),
                           "all_prespecified_labels_retained": True})
    kernel_checks = []
    for P in (8, 32, 128):
        values = [geometric_kernel(a, b, P) for a in range(1, P+1) for b in range(1, P+1)]
        bounded = [geometric_kernel(a, b, P) for a in range(1, min(8, P//2)+1) for b in range(1, min(8, P//2)+1)]
        kernel_checks.append({"padded": P, "all_positive_degree_pairs": P*P,
                              "minimum_exact_kernel": min(values), "bounded_minimum_exact_kernel": min(bounded),
                              "cap": min(8, P//2), "lower_bound": Fraction(1, (1+8*min(8, P//2))**2)})
    unequal = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(9, 0, 6)]], 6))
    cancellation = {"scope": "SELECTED_NATIVE_BOUNDARY_CALIBRATION_NOT_POPULATION_PERFORMANCE",
                    "native_labels": unequal.source.labels, "full_frequencies": unequal.source.frequencies,
                    "physical_control": physical_control(unequal, 1, (26,)),
                    "geometric_control": geometric_control(unequal),
                    "fiber_structure_control": fiber_structure_control(unequal),
                    "erasure_physical_control": erasure_physical_control(unequal, (26,))}
    translations = []
    for n, r, seed in ((1, 16, 98401), (2, 16, 98402), (1, 64, 98403)):
        source = random_even_source(n, 2*r, n*r-2, seed)
        translations.append({"dimension": n, "root_digits": r, "seed": seed,
                             "native_labels": source.labels, "full_frequencies": source.frequencies,
                             "translation_control": translation_control(NativeEdgeProgram(source)),
                             "dense_native_words_enumerated": 0})
    return _jsonable({"status": "NATIVE_FULL_LABEL_RECEIVER_WITH_EXPONENTIAL_CHARGED_SEARCH",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "kernel_source": "core/dcp_coherent_edge_sampling.py",
            "population_certificates": populations, "native_unit_minor_controls": unit_minor_controls(),
            "source_class_trimming_bounds": [source_class_trimming_bound(n,r) for n,r in ((1,5),(2,3),(1,16),(2,16),(1,64))],
            "short_Grover_template_bounds": [short_grover_template_bound(n,r,(n*r)**2) for n,r in ((1,5),(2,3),(1,16),(2,16),(1,64))],
            "whole_source_degree_census": natural_moment_control(), "kernel_checks": kernel_checks,
            "prespecified_native_physical_cases": finite,
            "fixed_time_cancellation_control": cancellation,
            "scalable_native_translation_controls": translations,
            "local_derivation_review_pending": True, "novelty_claim": False,
            "candidate_record_accepted": False, "classical_witness_finder_needed_by_this_receiver": False,
            "polynomial_time_weak_learner_implemented": False, "quantum_speedup_proved": False,
            "full_secret_decoder_implemented": False, "no_go_for_other_receivers": False})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    report = build_report()
    if args.write: REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "population_certificates": len(report["population_certificates"]),
                      "physical_cases": len(report["prespecified_native_physical_cases"]),
                      "physical_controls": sum(len(c["physical_controls"]) for c in report["prespecified_native_physical_cases"]),
                      "unit_minor_controls": len(report["native_unit_minor_controls"]), "quantum_speedup_proved": False}, indent=2))
