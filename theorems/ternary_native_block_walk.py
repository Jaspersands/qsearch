"""Costed native block heat-bath sampler and exact local-move falsifiers.

LOCAL DERIVATION / REVIEW PENDING. Tests an actual fiber-walk construction;
does not implement a fiber eraser or lower-bound general quantum receivers.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random

from cyclotomic_fiber_receiver import native_source
from ternary_covariant_noise import root_digits
from ternary_cyclic_extractor import random_even_source
from ternary_native_spectral_access import bounded_fibers

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_NATIVE_BLOCK_WALK.md"
REPORT = ROOT / "research/classical_baselines/ternary_native_block_walk.json"
SIGNATURES = ((1, 0), (0, 1), (-1, 0), (-1, 1), (0, -1), (1, -1))
TRANSITIONS = {(1, 0): (0, 1), (0, 1): (0, 2), (-1, 0): (1, 0),
               (-1, 1): (1, 2), (0, -1): (2, 0), (1, -1): (2, 1)}


def _integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} requires integer >= {minimum}")
    return value


def signature_count(width, support):
    _integer(width, "native word width")
    _integer(support, "maximum moved word coordinates")
    if support > width:
        raise ValueError("support cannot exceed native word width")
    return sum(math.comb(width, j)*6**j for j in range(1, support+1))//2


def collision_population_bound(n, q, width, support):
    _integer(n, "native dimension")
    root_digits(q)
    vocabulary = signature_count(width, support)
    G = q**n
    probability = min(Fraction(1), Fraction(vocabulary, G))
    return {"dimension": n, "modulus": str(q), "source_inputs": width,
            "maximum_changed_word_coordinates": support,
            "unoriented_nonzero_difference_signatures": str(vocabulary),
            "full_frequency_group": str(G),
            "probability_any_nontrivial_small_support_fiber_collision_upper": str(probability),
            "probability_all_small_support_fiber_walks_frozen_lower": str(1-probability),
            "requires_all_IID_uniform_full_native_rows": True,
            "label_and_word_adaptive_block_policies_covered": True,
            "all_moves_must_exactly_preserve_frequency_prefix": True,
            "temporary_prefix_violations_or_nonlocal_macros_are_outside_scope": True,
            "generic_quantum_receiver_lower_bound": False}


def quarter_distance_certificate(n, q, surplus=8):
    _integer(n, "native dimension")
    r = root_digits(q)
    _integer(surplus, "original sample surplus", 0)
    M = n*r+surplus
    if M < 4:
        raise ValueError("quarter-distance certificate requires at least four input words")
    support = M//4
    ledger = collision_population_bound(n, q, M, support)
    simple = min(Fraction(1), Fraction(3**surplus, 2)*Fraction(11, 12)**M)
    if Fraction(ledger["probability_any_nontrivial_small_support_fiber_collision_upper"]) > simple:
        raise ArithmeticError("exact signature count violates the quarter-distance Chernoff envelope")
    return {"dimension": n, "modulus": str(q), "root_digits": r, "source_inputs": M,
            "sample_surplus_over_group_entropy": surplus, "maximum_changed_coordinates": support,
            "exact_signature_population_ledger": ledger,
            "simple_rational_collision_probability_upper": str(simple),
            "fourth_power_base_comparison_left": str(Fraction(512, 729)),
            "fourth_power_base_comparison_right": str(Fraction(11, 12)**4),
            "minimum_full_fiber_collision_distance_on_no_event": support+1,
            "requires_M_equals_n_times_root_digits_plus_surplus": True,
            "polynomial_gate_macros_with_many_changed_coordinates_not_excluded": True,
            "conditional_block_enumeration_if_such_a_block_used": str(3**support),
            "distance_certificate_is_efficient_partner_finder": False}


@dataclass(frozen=True)
class NativeBlockHeatbath:
    source: object
    prefix: int | None = None

    def __post_init__(self):
        s = self.source
        if type(s.level) is not int or s.level < 2 or s.level % 2:
            raise ValueError("original even-level native source required")
        root_digits(s.modulus)
        if s.modulus != 3**(s.level//2) or s.dimension < 1 or s.inputs < 1:
            raise ValueError("actual full-root native dimensions required")
        if native_source(s.labels, s.level).frequencies != s.frequencies:
            raise ValueError("native ring chart and public frequency rows disagree")
        H = s.modulus if self.prefix is None else self.prefix
        root_digits(H)
        if H > s.modulus or s.modulus % H:
            raise ValueError("native prefix must divide the full root")
        object.__setattr__(self, "prefix", H)

    def _word(self, word):
        word = tuple(word)
        if len(word) != self.source.inputs or any(type(x) is not int or x not in (0, 1, 2) for x in word):
            raise ValueError("canonical original native word required")
        return word

    def _block(self, block):
        block = tuple(block)
        if not block or block != tuple(sorted(set(block))) or any(type(i) is not int or not 0 <= i < self.source.inputs for i in block):
            raise ValueError("nonempty sorted distinct native update positions required")
        return block

    def local_frequency(self, block, digits):
        return tuple(sum(0 if t == 0 else self.source.frequencies[i][t-1][j]
                         for i, t in zip(block, digits)) % self.prefix for j in range(self.source.dimension))

    def compatible_assignments(self, word, block, max_local_words=65536):
        word, block = self._word(word), self._block(block)
        _integer(max_local_words, "whole local conditional table cap")
        if 3**len(block) > max_local_words:
            raise ValueError("complete local conditional table exceeds cap; no partial sampler")
        target = self.local_frequency(block, tuple(word[i] for i in block))
        return tuple(digits for digits in product(range(3), repeat=len(block))
                     if self.local_frequency(block, digits) == target)

    def step(self, word, block, rng=None, max_local_words=65536):
        word, block = self._word(word), self._block(block)
        compatible = self.compatible_assignments(word, block, max_local_words)
        rng = random.SystemRandom() if rng is None else rng
        selected = compatible[rng.randrange(len(compatible))]
        out = list(word)
        for i, t in zip(block, selected):
            out[i] = t
        if tuple(x % self.prefix for x in self.source.value(out)) != tuple(x % self.prefix for x in self.source.value(word)):
            raise ArithmeticError("actual block step changed the committed native prefix")
        return {"initial_word": word, "word": tuple(out), "block": block, "conditional_candidates": len(compatible),
                "local_word_evaluations_charged": 3**len(block), "full_secret_grid_enumerated": False,
                "full_fiber_count_oracle_used": False, "quantum_state_preparation_implemented": False}

    def random_step(self, word, support, rng=None, max_local_words=65536):
        signature_count(self.source.inputs, support)
        rng = random.SystemRandom() if rng is None else rng
        block = tuple(sorted(rng.sample(range(self.source.inputs), support)))
        return self.step(word, block, rng, max_local_words)


def complete_signature_audit(walk, support, max_signatures=1_000_000):
    _integer(max_signatures, "whole difference-signature cap")
    vocabulary = signature_count(walk.source.inputs, support)
    if vocabulary > max_signatures:
        return {"status": "UNKNOWN_COMPLETE_SIGNATURE_CAP", "signature_count_required": str(vocabulary),
                "complete_vocabulary_checked": False, "all_small_moves_frozen_certified": False}
    zeros, checked = [], 0
    for j in range(1, support+1):
        for positions in combinations(range(walk.source.inputs), j):
            for coefficients in product(SIGNATURES, repeat=j):
                first = next(a for a in coefficients[0] if a)
                if first < 0:
                    continue  # Opposite signatures give the same zero event.
                checked += 1
                residual = tuple(sum(c[0]*walk.source.frequencies[i][0][l]+c[1]*walk.source.frequencies[i][1][l]
                                     for i, c in zip(positions, coefficients)) % walk.prefix for l in range(walk.source.dimension))
                if any(residual):
                    continue
                a, b = [0]*walk.source.inputs, [0]*walk.source.inputs
                for i, c in zip(positions, coefficients):
                    a[i], b[i] = TRANSITIONS[c]
                if tuple(x % walk.prefix for x in walk.source.value(a)) != tuple(x % walk.prefix for x in walk.source.value(b)):
                    raise ArithmeticError("signature witness is not a native collision")
                zeros.append({"positions": positions, "coefficients": coefficients, "first_word": a, "second_word": b})
    if checked != vocabulary:
        raise ArithmeticError("complete signature count disagrees with combinatorial formula")
    return {"status": "EXACT_COMPLETE_SMALL_MOVE_SIGNATURE_AUDIT", "complete_vocabulary_checked": True,
            "unoriented_signatures_checked": str(checked), "zero_signatures": zeros,
            "all_small_moves_frozen_certified": not zeros,
            "generic_quantum_receiver_lower_bound": False}


def transition_reference(walk, support, max_words=4096, max_work=1_000_000):
    _integer(max_words, "whole transition reference word cap")
    _integer(max_work, "whole transition reference work cap")
    signature_count(walk.source.inputs, support)
    D = 3**walk.source.inputs
    required = D*math.comb(walk.source.inputs, support)*3**support
    if D > max_words or required > max_work:
        raise ValueError("complete native transition reference exceeds cap; no partial kernel")
    blocks = tuple(combinations(range(walk.source.inputs), support))
    words, values, _, counts = bounded_fibers(walk.source, max_words=max_words)
    lookup = {word: i for i, word in enumerate(words)}
    rows, conditional_cache = [], {}
    for word in words:
        row = defaultdict(Fraction)
        for block in blocks:
            target = walk.local_frequency(block, tuple(word[i] for i in block))
            cache_key = (block, target)
            if cache_key not in conditional_cache:
                conditional_cache[cache_key] = walk.compatible_assignments(word, block)
            compatible = conditional_cache[cache_key]
            weight = Fraction(1, len(blocks)*len(compatible))
            for local in compatible:
                out = list(word)
                for i, t in zip(block, local):
                    out[i] = t
                row[lookup[tuple(out)]] += weight
        if sum(row.values()) != 1:
            raise ArithmeticError("complete conditional kernel is not stochastic")
        rows.append(dict(row))
    for i, row in enumerate(rows):
        for j, weight in row.items():
            if rows[j].get(i, Fraction(0)) != weight:
                raise ArithmeticError("uniform block heat bath is not exactly reversible")
            if tuple(x % walk.prefix for x in values[i]) != tuple(x % walk.prefix for x in values[j]):
                raise ArithmeticError("complete kernel escapes the committed prefix")
    components, unseen = [], set(range(D))
    while unseen:
        start = min(unseen)
        visited, queue = {start}, [start]
        while queue:
            i = queue.pop()
            for j in rows[i]:
                if j not in visited:
                    visited.add(j); queue.append(j)
        unseen -= visited
        components.append(sorted(visited))
    prefix_fibers = defaultdict(list)
    for i, value in enumerate(values):
        prefix_fibers[tuple(x % walk.prefix for x in value)].append(i)
    component_index = {i: j for j, C in enumerate(components) for i in C}
    fibers = []
    for y, indices in sorted(prefix_fibers.items()):
        C = len(indices)
        ids = sorted({component_index[i] for i in indices})
        disconnected = len(ids) > 1
        if disconnected:
            gap = Fraction(0)
        elif C == 1 or support == walk.source.inputs:
            gap = Fraction(1)
        else:
            edge_min = min(w for i in indices for j, w in rows[i].items() if i != j)
            gap = 2*edge_min/(C*(C-1))
        fibers.append({"prefix_frequency": y, "word_indices": indices, "component_indices": ids,
                       "uniform_fiber_stationary_subspace_dimension": len(ids),
                       "fiber_mixing_gap_certified_lower": str(gap), "exact_gap_zero_certified": disconnected,
                       "exact_gap_one_complete_heatbath": support == walk.source.inputs})
    nontrivial_mass = Fraction(sum(c for c in counts.values() if c > 1), D)
    bad_mass = Fraction(sum(len(f["word_indices"]) for f in fibers if f["exact_gap_zero_certified"]), D)
    unchanged = all(values[i] == values[j] for i, row in enumerate(rows) for j in row)
    return {"support": support, "prefix": walk.prefix, "complete_words": words, "full_frequency_values": values,
            "conditional_transition_rows": [[[j, str(w)] for j, w in sorted(row.items())] for row in rows],
            "connected_components": components, "prefix_fibers": fibers,
            "all_rows_exactly_symmetric_stochastic": True,
            "kernel_PSD_by_average_of_conditional_projection_blocks": True,
            "full_native_source_family_stationary_certified": unchanged,
            "raw_uniform_source_mass_in_disconnected_prefix_fibers": str(bad_mass),
            "raw_source_mass_in_nontrivial_FULL_frequency_fibers": str(nontrivial_mass),
            "whole_reference_word_count": D, "whole_reference_work_upper": str(required),
            "reference_enumerates_whole_native_word_cube": True,
            "reference_is_scalable_walk_compiler": False, "efficient_fiber_eraser_supplied": False}


def run_controls():
    source = random_even_source(2, 4, 5, 89881)
    full, low = NativeBlockHeatbath(source), NativeBlockHeatbath(source, 3)
    trials = []
    for walk, support in ((full, 1), (full, 2), (full, 3), (full, 5), (low, 2)):
        reference = transition_reference(walk, support)
        audit = complete_signature_audit(walk, support)
        if audit["all_small_moves_frozen_certified"] and len(reference["connected_components"]) != 3**source.inputs:
            raise ArithmeticError("global collision certificate disagrees with actual heat-bath kernel")
        step = walk.random_step((1, 0, 2, 1, 0), support, random.Random(89900+support))
        trials.append({"reference": reference, "signature_audit": audit, "live_step": step})
    if not trials[0]["signature_audit"]["all_small_moves_frozen_certified"]:
        raise ArithmeticError("prespecified one-site native falsifier is not frozen")
    if Fraction(trials[0]["reference"]["raw_source_mass_in_nontrivial_FULL_frequency_fibers"]) < Fraction(9, 10):
        raise ArithmeticError("frozen control has insufficient nontrivial source-fiber weight")
    if any(f["exact_gap_zero_certified"] for f in trials[3]["reference"]["prefix_fibers"]):
        raise ArithmeticError("complete-block positive reference fails to connect its fibers")
    ledgers = [collision_population_bound(n, q, n*root_digits(q)+8, k) for n, q, k in ((8, 9, 1), (32, 81, 3), (128, 243, 5), (512, 729, 6))]
    return {"status": "COSTED_NATIVE_BLOCK_WALK_AND_GLOBAL_SMALL_MOVE_OBSTRUCTION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_source": {"seed": 89881, "native_level": source.level, "original_ring_labels": source.labels,
                              "native_frequencies": source.frequencies, "dimension": source.dimension,
                              "modulus": source.modulus, "source_inputs": source.inputs,
                              "seed_is_population_scaling_evidence": False},
            "live_trials": trials, "global_small_move_population_ledgers": ledgers,
            "near_entropy_quarter_distance_certificates": [quarter_distance_certificate(n, q) for n, q in ((128, 243), (512, 729))],
            "coherent_kernel_preparation_specification": "Uniform block selection; bounded3^k compatible-word list/count/unrank; approximate uniform-integer state; clean scratch reversal. No whole-fiber oracle.",
            "classical_one_step_local_frequency_evaluation_bound": "O(n*M+n*k*3^k); one random block, not all binomial(M,k) blocks",
            "uniform_block_selection_does_not_enumerate_the_block_menu": True,
            "small_block_step_is_polynomial_at_logarithmic_support": True,
            "quantum_walk_gate_export_supplied": False, "stationary_state_preparation_or_inverse_granted": False,
            "efficient_fiber_eraser_supplied": False, "generic_quantum_receiver_lower_bound": False,
            "quantum_speedup_proved": False, "candidate_record_accepted": False, "novelty_claim": False,
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
                      "native_walk_trials": len(report["live_trials"]), "efficient_fiber_eraser_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
