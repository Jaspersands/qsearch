"""Native least-trit collimation through an ordinary two-witness interface.

LOCAL DERIVATIONS / REVIEW PENDING. Established collimation mechanics;
the exact native transfer does not supply a polynomial witness finder.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import phase, root_digits
from ternary_cyclic_extractor import _integer, _word, random_even_source

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_pair_collimation.json"


@dataclass(frozen=True)
class LowProblem:
    moduli: tuple
    frequencies: tuple
    target_coordinate: int

    def __post_init__(self):
        object.__setattr__(self, "moduli", tuple(self.moduli))
        object.__setattr__(self, "frequencies", tuple(tuple(tuple(row) for row in pair) for pair in self.frequencies))
        if not self.moduli or any(type(q) is not int or q < 1 or (q != 1 and root_digits(q) < 1) for q in self.moduli):
            raise ValueError("nonempty power-of-three nuisance group required")
        n = len(self.moduli)
        if type(self.target_coordinate) is not int or not 0 <= self.target_coordinate < n:
            raise ValueError("canonical target coordinate required")
        if not self.frequencies or any(len(pair) != 2 for pair in self.frequencies):
            raise ValueError("two original native rows per source register required")
        if any(len(row) != n or any(type(x) is not int or not 0 <= x < q for x, q in zip(row, self.moduli))
               for pair in self.frequencies for row in pair):
            raise ValueError("canonical nuisance-group frequencies required")

    @property
    def width(self): return len(self.frequencies)

    @property
    def group_size(self): return math.prod(self.moduli)

    def value(self, word):
        word = _word(word, self.width)
        return _value(self.frequencies, self.moduli, word)

    def target(self, target):
        target = tuple(target)
        if len(target) != len(self.moduli) or any(type(x) is not int or not 0 <= x < q for x, q in zip(target, self.moduli)):
            raise ValueError("canonical nuisance-group target required")
        return target


def low_problem(source, coordinate=0):
    if source.level % 2:
        raise ValueError("original even-native source required")
    _integer(coordinate, "target coordinate")
    if coordinate >= source.dimension: raise ValueError("target coordinate out of range")
    moduli = tuple(source.modulus//3 if j == coordinate else source.modulus for j in range(source.dimension))
    return LowProblem(moduli, tuple(tuple(tuple(x % q for x, q in zip(row, moduli)) for row in pair)
                                    for pair in source.frequencies), coordinate)


def _value(pairs, moduli, word):
    return tuple(sum(pairs[i][x-1][j] if x else 0 for i, x in enumerate(word)) % q for j, q in enumerate(moduli))


def verify_pair(problem, target, pair):
    target = problem.target(target)
    if len(pair) != 2: raise ValueError("two witnesses, not a single answer, required")
    pair = tuple(_word(w, problem.width) for w in pair)
    if pair[0] == pair[1]: raise ValueError("distinct witnesses required")
    if any(problem.value(w) != target for w in pair): raise ValueError("witnesses must lie in the measured nuisance fiber")
    return pair


def mitm_pair(problem, target, max_half_words=100_000):
    """Ordinary exponential reference; stores at most two words per left sum."""
    target = problem.target(target); _integer(max_half_words, "half-table budget", 1)
    split = problem.width//2; bounds = (3**split, 3**(problem.width-split))
    cost = {"raw_half_assignments": tuple(str(x) for x in bounds), "left_words_enumerated": 0,
            "right_words_enumerated": 0, "retained_left_words": 0, "right_hash_lookups": 0,
            "uses_only_LowProblem": True, "polynomial_witness_finder": False}
    if max(bounds) > max_half_words:
        return {"status": "BUDGET_EXHAUSTED_NO_PARTIAL_PAIR", "pair": (), "cost": cost}
    left = defaultdict(list)
    for word in product(range(3), repeat=split):
        key = _value(problem.frequencies[:split], problem.moduli, word)
        if len(left[key]) < 2: left[key].append(word)
        cost["left_words_enumerated"] += 1
    cost["retained_left_words"] = sum(map(len, left.values()))
    answers = []
    for word in product(range(3), repeat=problem.width-split):
        value = _value(problem.frequencies[split:], problem.moduli, word)
        key = tuple((a-b) % q for a, b, q in zip(target, value, problem.moduli))
        cost["right_words_enumerated"] += 1; cost["right_hash_lookups"] += 1
        for prefix in left.get(key, ()):
            answers.append((*prefix, *word))
            if len(answers) == 2:
                pair = verify_pair(problem, target, answers)
                return {"status": "VERIFIED_PAIR_REFERENCE_ONLY", "pair": pair, "cost": cost}
    return {"status": "EMPTY_OR_SINGLETON_TARGET", "pair": (), "cost": cost}


def pair_recipe(first, second):
    first = tuple(first); first = _word(first, len(first)); second = _word(second, len(first))
    if not first or first == second: raise ValueError("nonempty distinct native endpoints required")
    delta = tuple((b-a) % 3 for a, b in zip(first, second)); pivot = next(i for i, x in enumerate(delta) if x)
    gates = [{"gate": "ADD_F3", "target": i, "coefficient": -x % 3} for i, x in enumerate(first) if x]
    if delta[pivot] == 2: gates.append({"gate": "SCALE_F3", "target": pivot, "coefficient": 2})
    gates.extend({"gate": "SUM_F3", "control": pivot, "target": i, "coefficient": -x % 3}
                 for i, x in enumerate(delta) if x and i != pivot)
    return {"source_width": len(first), "pivot": pivot, "gates": gates,
            "projector": {"accepted_words": (first, second), "do_not_measure_which_endpoint": True},
            "readout": "inverse_F3_on_pivot_then_computational_measurement",
            "all_nonpivot_coordinates_zero_on_accepted_pair": True,
            "unknown_state_preparation_inverse_cloning_or_fiber_counter_required": False,
            "identically_labeled_unknown_copies_required": False,
            "hardware_qubit_synthesis_and_error_certified": False}


def apply_recipe(word, recipe):
    word = list(_word(word, recipe["source_width"]))
    for g in recipe["gates"]:
        t = g["target"]
        if g["gate"] == "ADD_F3": word[t] = (word[t]+g["coefficient"]) % 3
        elif g["gate"] == "SCALE_F3": word[t] = word[t]*g["coefficient"] % 3
        else: word[t] = (word[t]+g["coefficient"]*word[g["control"]]) % 3
    return tuple(word)


def syndrome_recipe(problem):
    tape = [{"gate": "digit_controlled_constant_modular_ADD", "source_wire": i,
             "source_digit": digit, "target_component": j, "constant": row[j], "modulus": q}
            for i, pair in enumerate(problem.frequencies) for digit, row in enumerate(pair, 1)
            for j, q in enumerate(problem.moduli) if q > 1 and row[j]]
    return {"source_registers": problem.width, "nuisance_moduli": problem.moduli,
            "clean_syndrome_qutrits": sum(0 if q == 1 else root_digits(q) for q in problem.moduli),
            "constant_addition_tape": tape, "measure_only_nuisance_syndrome": True,
            "original_phase_register_retained_while_solver_runs": True,
            "solver_runs_in_separate_workspace_not_controlled_by_unknown_word": True,
            "constant_modular_ADD_elementary_decomposition_not_supplied": True,
            "polynomial_public_arithmetic_not_an_inverse_function_oracle": True}


def apply_syndrome_tape(problem, word, ancilla, inverse=False):
    word = _word(word, problem.width); ancilla = list(problem.target(ancilla))
    if type(inverse) is not bool: raise ValueError("Boolean inverse mode required")
    tape = syndrome_recipe(problem)["constant_addition_tape"]
    for gate in reversed(tape) if inverse else tape:
        if word[gate["source_wire"]] == gate["source_digit"]:
            j = gate["target_component"]
            ancilla[j] = (ancilla[j]+(-1 if inverse else 1)*gate["constant"]) % gate["modulus"]
    return tuple(ancilla)


def physical_control(source, coordinate, secret):
    if source.inputs > 6 or len(secret) != source.dimension or any(type(x) is not int for x in secret):
        raise ValueError("bounded native replay / integer calibration secret required")
    problem = low_problem(source, coordinate); D = 3**source.inputs; Q = source.modulus//3
    words = list(product(range(3), repeat=source.inputs)); buckets = defaultdict(list)
    # Reversible known-label sum evaluation, followed by syndrome measurement.
    for word in words: buckets[problem.value(word)].append(word)
    records, acceptance, max_error = [], Fraction(0), 0.
    for target, fiber in sorted(buckets.items()):
        solved = mitm_pair(problem, target); C = len(fiber)
        record = {"target": target, "reference_fiber_size_not_used_by_solver": C,
                  "syndrome_probability": str(Fraction(C, D)), "solver": solved,
                  "informative_projection_probability_unconditional": "0"}
        if not solved["pair"]:
            record["rejection"] = "NO_VERIFIED_DISTINCT_PAIR"; records.append(record); continue
        u, v = solved["pair"]; F0, F1 = source.value(u), source.value(v)
        difference = tuple((b-a) % source.modulus for a, b in zip(F0, F1))
        assert all(x == 0 for j, x in enumerate(difference) if j != coordinate) and difference[coordinate] % Q == 0
        delta = difference[coordinate]//Q
        record.update({"relative_full_frequency": difference, "target_trit_multiplier": delta,
                       "selected_pair_projection_probability_given_syndrome": str(Fraction(2, C))})
        if not delta:
            record["rejection"] = "ZERO_TARGET_TRIT_MULTIPLIER_AFTER_LOW_ONLY_SELECTION"
            records.append(record); continue
        recipe = pair_recipe(u, v); permutation = [apply_recipe(w, recipe) for w in words]
        assert len(set(permutation)) == D
        assert apply_recipe(u, recipe) == (0,)*source.inputs
        assert apply_recipe(v, recipe) == tuple(int(j == recipe["pivot"]) for j in range(source.inputs))
        # Endpoint equality projector preserves relative phase; no endpoint tag.
        original = {w: phase(sum(a*s for a, s in zip(source.value(w), secret)), source.modulus)/math.sqrt(D) for w in (u, v)}
        transformed = {apply_recipe(w, recipe): amplitude for w, amplitude in original.items()}
        zero = (0,)*source.inputs; one = tuple(int(j == recipe["pivot"]) for j in range(source.inputs))
        pivot = np.array([transformed[zero], transformed[one], 0j])
        anchor = phase(sum(a*s for a, s in zip(F0, secret)), source.modulus)
        expected = anchor*np.array([1, phase(delta*secret[coordinate], 3), 0])/math.sqrt(D)
        max_error = max(max_error, float(np.max(abs(pivot-expected))))
        probability = Fraction(2, D); acceptance += probability
        F3 = np.array([[phase(-a*b, 3)/math.sqrt(3) for b in range(3)] for a in range(3)])
        probabilities = abs(F3@pivot/math.sqrt(float(probability)))**2
        correct = delta*(secret[coordinate] % 3) % 3
        assert abs(probabilities[correct]-2/3) < 1e-12
        record.update({"recipe": recipe, "reference_whole_basis_permutation": permutation,
                       "original_anchor_phase_frequency": F0,
                       "unnormalized_pivot_amplitudes": [[float(x.real), float(x.imag)] for x in pivot],
                       "informative_projection_probability_unconditional": str(probability),
                       "inverse_F3_probabilities": [float(x) for x in probabilities],
                       "guess_rule": "inverse(target_trit_multiplier)*measured_digit mod3",
                       "conditional_correct_probability": "2/3",
                       "projection_failure_probability_unconditional": str(Fraction(C-2, D))})
        records.append(record)
    assert max_error < 1e-12
    return {"original_even_level": source.level, "original_modulus": str(source.modulus),
            "native_labels": source.labels, "target_coordinate": coordinate, "calibration_secret_only": secret,
            "low_solver_view": {"moduli": problem.moduli, "frequencies": problem.frequencies},
            "syndrome_recipe": syndrome_recipe(problem), "all_nonempty_syndrome_branches": records,
            "informative_acceptance": str(acceptance), "all_rejections_and_projection_failures": str(1-acceptance),
            "unconditional_correct_including_uniform_failure_guess": str(Fraction(1, 3)+acceptance/3),
            "calibration_full_root_phase_amplitude_error": max_error,
            "source_qutrits_consumed_per_attempt": source.inputs,
            "classical_calibration_only_not_a_quantum_hardware_run": True,
            "polynomial_witness_finder_or_full_depth_algorithm": False}


def pointed_unit_minor(base, first, second):
    base = tuple(base); base = _word(base, len(base)); first = _word(first, len(base)); second = _word(second, len(base))
    if len({base, first, second}) != 3: raise ValueError("three distinct native words required")
    rows = [tuple(int(w[i] == d)-int(base[i] == d) for i in range(len(base)) for d in (1, 2)) for w in (first, second)]
    for a, b in combinations(range(2*len(base)), 2):
        determinant = rows[0][a]*rows[1][b]-rows[0][b]*rows[1][a]
        if abs(determinant) == 1: return {"rows": rows, "columns": (a, b), "integer_determinant": determinant}
    raise AssertionError("pointed native simplex differences must have a unit minor")


def solver_contract(n, digits, pair_success=Fraction(2, 3)):
    _integer(n, "secret dimension", 1); _integer(digits, "root digits", 1)
    M = n*digits-2
    if M < 1: raise ValueError("underfull contract requires n*r>=3")
    xi = Fraction(pair_success)
    if not 0 < xi <= 1: raise ValueError("pointwise pair success in(0,1] required")
    D, H = 3**M, 3**(n*digits-1)
    mass = Fraction(D-1, H)-Fraction((D-1)*(D-2), H*H)
    beta = xi*mass/6
    return {"dimension": n, "root_digits": digits, "original_native_inputs_per_call": M,
            "word_space_size": str(D), "nuisance_group_size": str(H), "density": "1/3",
            "source_mean_neighbors": str(Fraction(D-1, H)),
            "source_second_factorial_neighbor_moment": str(Fraction((D-1)*(D-2), H*H)),
            "natural_mass_of_exactly_two_word_fibers_lower": str(mass),
            "pointwise_distinct_pair_solver_success_required": str(xi),
            "uniform_target_pair_success_beta_lower": str(beta),
            "source_mean_informative_acceptance_lower": str(4*beta),
            "source_mean_least_trit_advantage_lower": str(4*beta/3),
            "uniform_target_beta_to_informative_acceptance": "4*beta",
            "uniform_target_beta_to_raw_least_trit_success": "1/3+4*beta/3",
            "pointwise_solver_guarantee_is_supplied": False,
            "MITM_raw_half_assignment_bounds": (str(3**(M//2)), str(3**(M-M//2))),
            "separate_word_retention_and_solver_runtime_costs_required": True,
            "expected_binary_phase_inputs_if_fresh_IID_vector_phases_available": str(Fraction(8*M, 3)),
            "cyclic_DHSP_natural_source_reduction_for_n_greater_than_one_supplied": False,
            "full_secret_bootstrap_supplied_conditionally_elsewhere": True,
            "polynomial_full_depth_algorithm": False}


def capped_runtime_transfer(expected_uniform_runtime, beta_lower):
    runtime, beta = Fraction(expected_uniform_runtime), Fraction(beta_lower)
    if runtime <= 0 or not 0 < beta <= Fraction(1, 18):
        raise ValueError("positive runtime and possible underfull uniform-target coverage required")
    return {"expected_uniform_target_runtime_assumed": str(runtime), "uniform_target_pair_beta_assumed": str(beta),
            "pointwise_runtime_cap": str(2*runtime/beta), "uniform_target_beta_after_cap_lower": str(beta/2),
            "informative_native_acceptance_after_cap_lower": str(2*beta),
            "raw_native_least_trit_advantage_after_cap_lower": str(2*beta/3),
            "unweighted_runtime_equals_physical_Born_runtime": False,
            "assumed_runtime_and_coverage_estimates_certified": False}


def exhaustive_one_input_census(n=1, digits=3):
    _integer(n, "census dimension", 1); _integer(digits, "census root digits", 1)
    if n*digits > 3: raise ValueError("entire original source census capped at n*r<=3")
    q, D = 3**digits, 3
    moduli = (q//3, *((q,)*(n-1))); H = math.prod(moduli)
    vectors = list(product(*(range(v) for v in moduli)))
    size_law = Counter(); paired, singleton, natural_two = 0, 0, Fraction(0)
    verified_high_lifts, informative_lifts = 0, 0
    for a, c in product(vectors, repeat=2):
        p = LowProblem(moduli, ((a, c),), 0)
        for target in vectors:
            fiber = [w for w in product(range(3), repeat=1) if p.value(w) == target]
            C = len(fiber); size_law[C] += 1
            pair = mitm_pair(p, target)["pair"]
            assert bool(pair) == (C >= 2)
            paired += bool(pair); singleton += C == 1
            if C == 2: natural_two += Fraction(C, D*H*H)
            if pair:
                for ha, hc in product(range(3), repeat=2):
                    frequencies = (0, a[0]+(q//3)*ha, c[0]+(q//3)*hc)
                    delta = (frequencies[pair[1][0]]-frequencies[pair[0][0]]) % q
                    assert delta % (q//3) == 0
                    verified_high_lifts += 1; informative_lifts += delta != 0
    beta = Fraction(paired, H**3)
    acceptance = Fraction(2*informative_lifts, D*(3*H)**2)
    assert acceptance == Fraction(4*H, 3*D)*beta and informative_lifts*3 == verified_high_lifts*2
    return {"dimension": n, "original_modulus": q, "original_even_level": 2*digits, "native_input_registers": 1,
            "nuisance_moduli": moduli, "nuisance_group_size": H,
            "low_label_arrays": H*H, "uniform_target_instances": H**3,
            "full_native_label_arrays": (3*H)**2, "fiber_size_instance_counts": dict(sorted(size_law.items())),
            "uniform_target_pair_success_beta": str(beta), "informative_acceptance_exact": str(acceptance),
            "raw_least_trit_success_exact": str(Fraction(1, 3)+acceptance/3),
            "natural_two_element_mass_exact": str(natural_two),
            "verified_pair_high_lifts": verified_high_lifts, "informative_pair_high_lifts": informative_lifts,
            "singleton_only_single_witness_uniform_success": str(Fraction(singleton, H**3)),
            "singleton_only_two_witness_success": "0",
            "not_an_asymptotic_witness_algorithm": True}


def build_report():
    positive = native_source([[inverse_frequency_coordinates(9, 18, 6)]], 6)
    negative = native_source([[inverse_frequency_coordinates(0, 9, 6)]], 6)
    controls = [physical_control(positive, 0, (17,)), physical_control(negative, 0, (17,))]
    controls.extend(physical_control(random_even_source(n, 2*r, n*r-2, seed), j, tuple(7+i for i in range(n)))
                    for n, r, j, seed in ((1, 4, 0, 76214), (2, 3, 1, 76223)))
    controls.append(physical_control(native_source([[inverse_frequency_coordinates(3, 6, 4)]], 4), 0, (8,)))
    controls.append(physical_control(native_source([[inverse_frequency_coordinates(1, 2, 2),
                                                   inverse_frequency_coordinates(0, 0, 2)]], 2), 0, (8, 19)))
    minor_checks = 0
    for M in (1, 2, 3):
        words = list(product(range(3), repeat=M))
        for base in words:
            for u in words:
                for v in words:
                    if len({base, u, v}) == 3:
                        pointed_unit_minor(base, u, v); minor_checks += 1
    return {"status": "SOURCE_VALID_LEAST_TRIT_PAIR_INSTRUMENT_AND_CONDITIONAL_SOLVER_REDUCTION_REVIEW_PENDING",
            "prior_art": ["Regev quant-ph/0406151 Section3", "Kuperberg arXiv1112.3333 Section4.2"],
            "all_native_pointed_triples_unit_minor_checks": minor_checks,
            "complete_original_source_census": exhaustive_one_input_census(),
            "constant_boundary_root_source_censuses": [exhaustive_one_input_census(n, r) for n, r in ((1, 1), (1, 2), (2, 1))],
            "native_full_root_physical_controls": controls,
            "underfull_solver_contracts": [solver_contract(n, r) for n, r in ((1, 3), (1, 16), (1, 32), (8, 32), (32, 128))],
            "open_required_primitive": "Polynomial ordinary distinct-pair finder with proven nonnegligible UNIFORM-target coverage and capped runtime on the stripped native nuisance-group distribution.",
            "known_classical_phase_tags_substituted_for_unknown_native_secret": False,
            "quantum_state_oracle_inverse_cloning_fiber_counter_or_identical_copies_granted": False,
            "average_single_witness_success_implies_pair_coverage": False,
            "accepted_candidate": False, "novelty_claim": False,
            "polynomial_witness_finder": False, "new_full_depth_quantum_algorithm": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        print(json.dumps({"report": str(REPORT), "exact_native_acceptance": report["complete_original_source_census"]["informative_acceptance_exact"],
                          "uniform_target_pair_transfer": "4*beta", "polynomial_witness_finder": False}))
    else: print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__": main()
