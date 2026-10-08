"""Exact full-root two-layer population interference without a native word cube.

LOCAL DERIVATION / REVIEW PENDING. Fixed public quarter-turn angles only;
does not prepare fibers or bound arbitrary adaptive/deeper circuits.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
import hashlib
import json
import math
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form

from ternary_covariant_noise import root_digits
from ternary_native_block_walk import _integer
from ternary_hot_phase_mixer import sqrt_rational_upper

ZERO, ONE = (0, 0), (1, 0)
PATTERNS = tuple(product(range(3), repeat=4))
QUARTER_PHASES = ((1, 0), (0, -1), (-1, 0), (0, 1))
ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_TWO_LAYER_PATH_TRANSFER.md"
REPORT = ROOT / "research/phase_workbench/ternary_two_layer_path_transfer.json"


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def multiply(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def conjugate(a):
    return a[0], -a[1]


def power(a, n):
    _integer(n, "Gaussian integer exponent", 0)
    answer = ONE
    while n:
        if n & 1:
            answer = multiply(answer, a)
        a = multiply(a, a)
        n >>= 1
    return answer


def _quarter(k):
    if type(k) is not int or k not in range(4):
        raise ValueError("exact quarter-turn index0..3 required")
    return QUARTER_PHASES[k]


def pattern_columns(pattern):
    if len(pattern) != 4 or any(type(a) is not int or a not in range(3) for a in pattern):
        raise ValueError("four original native path trits required")
    return tuple(v for t in (1, 2) if any(v := tuple(int(a == t) for a in pattern)))


def lattice_matrix(basis):
    return Matrix.hstack(*(Matrix(c) for c in basis)) if basis else Matrix.zeros(4, 0)


@lru_cache(maxsize=100000)
def _extend(basis, columns):
    if not columns:
        return basis
    H = hermite_normal_form(lattice_matrix(basis).row_join(lattice_matrix(columns)))
    return tuple(tuple(int(H[i, j]) for i in range(4)) for j in range(H.cols))


def extend(basis, pattern):
    return _extend(basis, tuple(sorted(pattern_columns(pattern))))


@lru_cache(maxsize=1)
def complete_graph():
    states, lookup, edges = [()], {(): 0}, []
    cursor = 0
    while cursor < len(states):
        basis, row = states[cursor], []
        for p in PATTERNS:
            next_basis = extend(basis, p)
            if next_basis not in lookup:
                if len(states) >= 32768:
                    raise ArithmeticError("native generator-state bound exceeded; no partial graph")
                lookup[next_basis] = len(states)
                states.append(next_basis)
            row.append(lookup[next_basis])
        edges.append(tuple(row)); cursor += 1
    return tuple(states), tuple(edges)


@lru_cache(maxsize=10000)
def zero_subset_invariants(basis):
    A = lattice_matrix(basis)
    answer = []
    for zero_mask in range(16):
        rows = [i for i in range(4) if not zero_mask & (1 << i)]
        if not rows or not basis:
            invariant = ()
        else:
            S = smith_normal_form(A.extract(rows, range(A.cols)), domain=ZZ)
            invariant = tuple(abs(int(S[i, i])) for i in range(min(S.rows, S.cols)) if S[i, i])
        answer.append((len(rows), invariant))
    return tuple(answer)


def exact_zero_pattern_counts(basis, q):
    root_digits(q)
    zero_subset = [q**(r-len(d))*math.prod(math.gcd(q, x) for x in d)
                   for r, d in zero_subset_invariants(basis)]
    counts = []
    for Z in range(16):
        complement, T, count = 15 ^ Z, 15 ^ Z, 0
        while True:
            count += (-1)**T.bit_count()*zero_subset[Z | T]
            if T == 0:
                break
            T = (T-1) & complement
        if count < 0:
            raise ArithmeticError("negative exact annihilator zero-pattern count")
        counts.append(count)
    if sum(counts) != zero_subset[0] or counts[15] != 1:
        raise ArithmeticError("annihilator cardinality or zero character lost")
    return tuple(counts)


def cost_numerators(q, gamma1, gamma2):
    phase = [_quarter(gamma1), _quarter(gamma2)]
    a = [(1+(q-1)*z[0], (q-1)*z[1]) for z in phase]
    b = [(1-z[0], -z[1]) for z in phase]
    return tuple((a[i], b[i]) for i in range(2))+tuple((conjugate(a[i]), conjugate(b[i])) for i in range(2))


@lru_cache(maxsize=20000)
def moment_numerator(basis, q, gamma1, gamma2):
    coefficients = cost_numerators(q, gamma1, gamma2)
    out = ZERO
    for mask, count in enumerate(exact_zero_pattern_counts(basis, q)):
        term = ONE
        for i, (a, b) in enumerate(coefficients):
            term = multiply(term, a if mask & (1 << i) else b)
        out = add(out, (count*term[0], count*term[1]))
    if out[0]**2+out[1]**2 > q**8:
        raise ArithmeticError("unit-modulus phase expectation exceeds norm1")
    return out


def pattern_weight_numerator(pattern, beta1, beta2):
    x, t, xp, tp = pattern
    p1, p2 = _quarter(beta1), _quarter(beta2)
    def gate(p, equal):
        return (1+2*p[0], 2*p[1]) if equal else (1-p[0], -p[1])
    out = multiply(gate(p2, t == 0), gate(p1, t == x))
    return multiply(out, conjugate(multiply(gate(p2, tp == 0), gate(p1, tp == xp))))


@lru_cache(maxsize=16)
def weighted_edges(beta1, beta2):
    states, graph = complete_graph()
    weights = tuple(pattern_weight_numerator(p, beta1, beta2) for p in PATTERNS)
    edges = []
    for row in graph:
        grouped = defaultdict(lambda: ZERO)
        for j, w in zip(row, weights):
            grouped[j] = add(grouped[j], w)
        grouped = tuple((j, w) for j, w in sorted(grouped.items()) if w != ZERO)
        if tuple(map(sum, zip(*(w for j, w in grouped)))) != (81, 0):
            raise ArithmeticError("full signed coordinate transfer does not normalize")
        edges.append(grouped)
    return tuple(edges)


@lru_cache(maxsize=128)
def terminal_weights(inputs, beta1, beta2):
    _integer(inputs, "original native inputs")
    edges = weighted_edges(beta1, beta2)
    weights = {0: ONE}
    for step in range(inputs):
        out = defaultdict(lambda: ZERO)
        for i, value in weights.items():
            for j, w in edges[i]:
                out[j] = add(out[j], multiply(value, w))
        weights = {j: value for j, value in out.items() if value != ZERO}
        if tuple(map(sum, zip(*weights.values()))) != (81**(step+1), 0):
            raise ArithmeticError("full signed path multiplicity lost during transfer")
    return tuple(sorted(weights.items()))


@lru_cache(maxsize=1)
def structural_certificate():
    states, graph = complete_graph()
    active = set()
    @lru_cache(None)
    def depth(i):
        if i in active:
            raise ArithmeticError("strict integer-lattice transfer cycle")
        active.add(i)
        out = max((1+depth(j) for j in set(graph[i]) if j != i), default=0)
        active.remove(i)
        return out
    loop_values = {(a, b): tuple(next((w for j, w in row if j == i), ZERO)
                    for i, row in enumerate(weighted_edges(a, b))) for a in range(4) for b in range(4)}
    coefficient_rows, largest_l1 = [], 0
    for i in range(len(states)):
        coefficients = []
        for x in range(4):
            for y in range(4):
                z = ZERO
                for a in range(4):
                    for b in range(4):
                        character = conjugate(_quarter((a*x+b*y) % 4))
                        z = add(z, multiply(loop_values[a, b][i], character))
                if z[1] or z[0] % 16 or ((x == 2 or y == 2) and z != ZERO):
                    raise ArithmeticError("self-loop Laurent polynomial violates exact degree/integrality")
                if x != 2 and y != 2:
                    coefficients.append({"beta1_exponent": -1 if x == 3 else x,
                                         "beta2_exponent": -1 if y == 3 else y,
                                         "coefficient_numerator_over81": str(z[0]//16)})
        l1 = sum(abs(int(c["coefficient_numerator_over81"])) for c in coefficients)
        largest_l1 = max(largest_l1, l1)
        if sum(int(c["coefficient_numerator_over81"]) for c in coefficients) != 81:
            raise ArithmeticError("zero-angle self loop must equal1")
        for values in loop_values.values():
            if values[i][0]**2+values[i][1]**2 > 81**2:
                raise ArithmeticError("quarter-turn self-loop modulus exceeds1")
        coefficient_rows.append({"state": i, "Laurent_coefficients": coefficients})
    return {"maximum_strict_lattice_path_length": depth(0),
            "state_strict_remaining_depths": [depth(i) for i in range(len(states))],
            "all_quarter_self_loop_moduli_at_most_one": True,
            "continuous_self_loop_modulus_upper": str(Fraction(largest_l1, 81)),
            "continuous_Laurent_degree_per_angle": 1,
            "all_self_loop_Laurent_coefficients": coefficient_rows,
            "off_diagonal_complex_weight_row_norm_upper": "18",
            "continuous_self_loop_modulus_one_not_certified_by_this_report": True}


def _ceil_root(v, degree):
    low, high = 0, 1 << ((v.bit_length()+degree-1)//degree)
    while high-low > 1:
        mid = (low+high)//2
        if mid**degree < v:
            low = mid
        else:
            high = mid
    return high


def family_envelopes(n, q, inputs):
    _integer(n, "native dimension"); root_digits(q); _integer(inputs, "native input count")
    certificate = structural_certificate()
    d, B = certificate["maximum_strict_lattice_path_length"], Fraction(18)
    L = Fraction(certificate["continuous_self_loop_modulus_upper"])
    G, D = q**n, 3**inputs
    quarter = min(Fraction(1), sum(Fraction(math.comb(inputs, j))*B**j for j in range(min(inputs, d)+1))/G)
    continuous = min(Fraction(1), sum(Fraction(math.comb(inputs, j))*B**j*L**(inputs-j) for j in range(min(inputs, d)+1))/G)
    menu = min(Fraction(1), 256*quarter)
    inverse = (continuous.denominator+continuous.numerator-1)//continuous.numerator
    m = _ceil_root(inverse, 5)
    error = Fraction(88*(n+inputs), 7*m)
    tuned = min(Fraction(1), m**4*continuous+error)
    born = lambda s: min(Fraction(1), s+sqrt_rational_upper(Fraction(G-1, D)*s))
    return {"dimension": n, "modulus": str(q), "original_native_inputs": inputs,
            "strict_path_depth": d, "off_diagonal_weight_row_norm_upper": str(B),
            "continuous_loop_growth_upper": str(L),
            "all_fixed_quarter_angles_uniform_success_upper": str(quarter),
            "label_and_target_adaptive_quarter_menu_uniform_success_upper": str(menu),
            "label_and_target_adaptive_quarter_menu_Born_success_upper": str(born(menu)),
            "all_fixed_continuous_angles_uniform_success_upper": str(continuous),
            "implicit_four_angle_net_axis_points": str(m), "implicit_four_angle_net_total_points": str(m**4),
            "implicit_net_rounding_probability_error_upper": str(error),
            "label_and_target_adaptive_continuous_angles_uniform_success_upper": str(tuned),
            "label_and_target_adaptive_continuous_angles_Born_success_upper": str(born(tuned)),
            "continuous_near_entropy_regime_requires_M_equals_n_log3_q_plus_logarithmic_surplus": True,
            "continuous_bound_can_be_vacuous_for_much_larger_polynomial_batches": True,
            "arbitrary_mixer_shapes_more_layers_or_other_receivers_not_covered": True}


@lru_cache(maxsize=20000)
def _moment_power(basis, q, gamma1, gamma2, n):
    return power(moment_numerator(basis, q, gamma1, gamma2), n)


def evaluate(n, q, inputs, quarters=(2, 2, 2, 2)):
    _integer(n, "native frequency dimension"); root_digits(q); _integer(inputs, "native input count")
    if len(quarters) != 4:
        raise ValueError("gamma1,beta1,gamma2,beta2 quarter indices required")
    gamma1, beta1, gamma2, beta2 = quarters
    for v in quarters:
        _quarter(v)
    states, graph = complete_graph()
    weights = terminal_weights(inputs, beta1, beta2)
    moment_terms, total = [], ZERO
    for i, weight in weights:
        m = moment_numerator(states[i], q, gamma1, gamma2)
        term = multiply(weight, _moment_power(states[i], q, gamma1, gamma2, n))
        total = add(total, term)
        moment_terms.append({"state": i, "terminal_signed_weight_numerator": [str(x) for x in weight],
                             "phase_moment_numerator_over_q_to_four": [str(x) for x in m]})
    denominator = 81**inputs*q**(5*n)
    if total[1] or not 0 <= total[0] <= denominator:
        raise ArithmeticError("complete exact circuit probability is not real in[0,1]")
    success = Fraction(total[0], denominator)
    born = min(Fraction(1), success+sqrt_rational_upper(Fraction(q**n-1, 3**inputs)*success))
    return {"dimension": n, "modulus": str(q), "original_native_inputs": inputs,
            "quarters_gamma1_beta1_gamma2_beta2": quarters,
            "uniform_full_target_population_success_exact": str(success),
            "ratio_to_classical_uniform_target_rejection_exact": str(success*q**n),
            "Born_weighted_population_success_upper": str(born),
            "active_terminal_lattice_states": len(weights), "complete_graph_states": len(states),
            "terminal_terms": moment_terms, "complete_signed_path_denominator": str(denominator),
            "complete_probability_numerator": str(total[0]),
            "enumerates_original_word_cube_or_secret_group": False,
            "keeps_integer_lattice_and_full_root_torsion": True,
            "coherent_fiber_eraser_supplied": False,
            "continuous_or_label_adaptive_angles_covered": False}


def exact_circuit_census(q, inputs, quarters):
    """Independent of transfer: explicit full native labels and circuit words."""
    root_digits(q); _integer(inputs, "census input count")
    if q**(2*inputs) > 10000 or 3**inputs > 27:
        raise ValueError("complete direct native circuit census exceeds cap")
    gamma1, beta1, gamma2, beta2 = quarters
    for v in quarters:
        _quarter(v)
    words = tuple(product(range(3), repeat=inputs)); D = len(words)
    lookup = {w: i for i, w in enumerate(words)}
    sum_uniform = sum_born = Fraction(0); matrices = 0
    for flat in product(range(q), repeat=2*inputs):
        frequencies = [sum(flat[2*i+t-1] if t else 0 for i, t in enumerate(w)) % q for w in words]
        for y in range(q):
            state, denominator = [ONE]*D, 1
            for gamma, beta in ((gamma1, beta1), (gamma2, beta2)):
                state = [multiply(a, _quarter(gamma) if f != y else ONE) for a, f in zip(state, frequencies)]
                phase = _quarter(beta)
                diag, off = (1+2*phase[0], 2*phase[1]), (1-phase[0], -phase[1])
                for axis in range(inputs):
                    out = []
                    for w in words:
                        a = ZERO
                        for t in range(3):
                            previous = list(w); previous[axis] = t
                            a = add(a, multiply(diag if t == w[axis] else off, state[lookup[tuple(previous)]]))
                        out.append(a)
                    state = out; denominator *= 3
            marked = [i for i, f in enumerate(frequencies) if f == y]
            numerator = sum(state[i][0]**2+state[i][1]**2 for i in marked)
            probability = Fraction(numerator, D*denominator**2)
            sum_uniform += probability/q
            sum_born += probability*Fraction(len(marked), D)
        matrices += 1
    success, born = sum_uniform/matrices, sum_born/matrices
    predicted = evaluate(1, q, inputs, quarters)
    if success != Fraction(predicted["uniform_full_target_population_success_exact"]):
        raise ArithmeticError("full direct native circuit census contradicts lattice transfer")
    return {"dimension": 1, "modulus": str(q), "original_native_inputs": inputs,
            "quarters_gamma1_beta1_gamma2_beta2": quarters,
            "entire_IID_label_matrices": matrices, "complete_uniform_target_cases": matrices*q,
            "actual_direct_circuit_uniform_mean_exact": str(success),
            "actual_direct_circuit_Born_mean_exact": str(born)}


def menu(n, q, inputs):
    cases = [evaluate(n, q, inputs, angles) for angles in product(range(4), repeat=4)]
    best = max(cases, key=lambda r: Fraction(r["uniform_full_target_population_success_exact"]))
    fields = ("quarters_gamma1_beta1_gamma2_beta2", "uniform_full_target_population_success_exact",
              "ratio_to_classical_uniform_target_rejection_exact", "Born_weighted_population_success_upper")
    return {"dimension": n, "modulus": str(q), "original_native_inputs": inputs,
            "fixed_angle_population_menu": [{f: r[f] for f in fields} for r in cases],
            "best_fixed_angle_mean_case": best,
            "menu_selects_maximum_mean_not_instance_adaptive_mean_of_maxima": True,
            "finite_quarter_menu_does_not_bound_all_continuous_angles": True}


def run_controls():
    states, graph = complete_graph()
    return {"status": "EXACT_TWO_LAYER_NATIVE_PATH_TRANSFER_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "complete_integer_lattice_graph": [{"basis_columns": basis, "coordinate_pattern_next_states": row,
                "zero_subset_Smith_invariants": [{"remaining_rows": r, "invariants": d} for r, d in zero_subset_invariants(basis)]}
                for basis, row in zip(states, graph)],
            "native_coordinate_patterns": PATTERNS,
            "exact_direct_circuit_censuses": [exact_circuit_census(q, M, angles)
                for q, M in ((3, 2), (9, 1)) for angles in ((2, 2, 2, 2), (1, 1, 3, 1), (1, 3, 2, 2))],
            "growing_population_menus": [menu(n, q, n*root_digits(q)+8) for n, q in ((8, 9), (32, 81), (128, 243))],
            "signed_transfer_structure_certificate": structural_certificate(),
            "global_two_layer_family_envelopes": [family_envelopes(n, q, n*root_digits(q)+8)
                                                   for n, q in ((8, 9), (32, 81), (128, 243))],
            "graph_is_constant_size_for_this_two_layer_template": True,
            "no_original_word_cube_or_secret_group_in_scaling_transfer": True,
            "signed_weights_are_not_Markov_probabilities": True,
            "all_IID_uniform_full_native_rows_required": True,
            "fixed_public_quarter_turn_angles_only": True,
            "general_mixer_shape_or_deeper_circuit_lower_bound": False,
            "coherent_fiber_eraser_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.graph:
        states, edges = complete_graph()
        print(json.dumps({"complete_lattice_states": len(states), "complete_coordinate_transitions": len(states)*81}))
    elif args.write:
        result = run_controls()
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
        print(json.dumps({"status": result["status"], "report": str(REPORT),
                          "complete_lattice_states": len(result["complete_integer_lattice_graph"]),
                          "growing_menus": len(result["growing_population_menus"])}))
    else:
        result = evaluate(1, 3, 2)
        print(json.dumps({k: v for k, v in result.items() if k != "terminal_terms"}, indent=2))


if __name__ == "__main__":
    main()
