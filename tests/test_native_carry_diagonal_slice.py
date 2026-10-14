"""Classical degree reduction, real word witnesses and honest row/population costs."""
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product
import json
import math
import subprocess

from flint import nmod_mat
import pytest

from theorems import native_carry_diagonal_slice as D
from native_prefix_carry_lift import compile_carry
from native_short_preimage_reduction import PublicWordFamily


def family(k=8, q=9):
    pairs = (((1, 0), (0, 0)), ((0, 1), (0, 0)))+(((1, 1), (1, 0)),)*k
    return PublicWordFamily(q, 2, 1, k+2, (pairs,))


def circuit(k=8, q=9, target=(7, 8)):
    return compile_carry(family(k, q), 0, target)


@pytest.mark.parametrize("k,q", ((0, 9), (2, 9), (8, 27), (12, 3**64)))
def test_normalized_outputs_are_invertible_not_literal_residuals_or_solved_equations(k, q):
    raw = circuit(k, q)
    N = D.normalize(raw)
    for free in D.degree3_probe_points(k) if k <= 2 else ((0,)*k, tuple(i % 3 for i in range(k))):
        actual = raw.evaluate(free)
        expected = tuple(sum(a*b for a, b in zip(row, actual)) % 3 for row in N.output_inverse)
        assert N.evaluate(free) == expected
        assert all(x == 0 for x in expected) == all(x == 0 for x in actual)
    weights = N.record()["F3_pivot_weights"]
    assert tuple(tuple(weights[j][i]["cube"] for j in range(2)) for i in range(2)) == ((1, 0), (0, 1))
    assert not N.record()["output_is_literal_native_digit_residual"]
    assert not N.record()["uniform_fibre_sampler_or_solver_supplied_by_output_normalization"]


def test_normalizer_rejects_a_forged_cube_minor():
    raw = circuit(2)
    weights = tuple(tuple(dict(w) for w in row) for row in raw.pivot_weights)
    weights[0][0]["cube"] = (weights[0][0]["cube"]+1) % 3
    with pytest.raises(ArithmeticError, match="minor"): D.normalize(replace(raw, pivot_weights=weights))


@pytest.mark.parametrize("k", (0, 1, 2, 8, 12, 1000))
def test_kernel_blocks_are_disjoint_independent_and_remove_mixed_cubics(k):
    N = D.normalize(circuit(k));S = D.disjoint_kernel_slice(N)
    assert len(S.directions) >= k//3
    occupied = set()
    for v in S.directions:
        support = {i for i, x in enumerate(v) if x}
        assert support and not occupied & support
        occupied |= support
        assert all(sum(a*b for a, b in zip(f["coefficients"], v)) % 3 == 0 for f in N.raw.pivot_forms)
    points = tuple(product(range(3), repeat=len(S.directions))) if len(S.directions) <= 4 else (
        (0,)*len(S.directions), tuple(i % 3 for i in range(len(S.directions))))
    for z in points:
        assert S.evaluate(z) == N.evaluate(S.free(z))
    assert S.record()["uniform_prefix_projection_acceptance"]["negative_exponent"] == k-len(S.directions)
    assert not S.record()["full_prefix_zero_set_preserved"]


def test_kernel_without_disjoint_support_does_not_make_divided_cubes_linear():
    b, v, w = (1, 1, 1), (1, 2, 0), (0, 1, 2)
    assert sum(a*x for a, x in zip(b, v)) % 3 == sum(a*x for a, x in zip(b, w)) % 3 == 0
    combined = tuple((a+2*c) % 3 for a, c in zip(v, w))
    assert D.divided_cube(b, combined) != (D.divided_cube(b, v)+2*D.divided_cube(b, w)) % 3


@pytest.mark.parametrize("kind", ("overlap", "nonkernel", "zero", "width"))
def test_invalid_slice_directions_are_not_admitted(kind):
    N = D.normalize(circuit(8));S = D.disjoint_kernel_slice(N)
    if kind == "overlap": directions = (S.directions[0], S.directions[0])
    elif kind == "nonkernel": directions = ((1,)+(0,)*7,)
    elif kind == "zero": directions = ((0,)*8,)
    else: directions = ((1,),)
    with pytest.raises(ValueError): D.restrict_diagonal(N, directions)


def test_slice_survives_higher_label_changes_but_equations_change():
    f = family(8);raw = compile_carry(f, 0, (7, 8));base = D.disjoint_kernel_slice(D.normalize(raw))
    pairs = tuple(tuple(tuple((a+3) % 9 for a in label) for label in pair) for pair in f.paired_labels[0])
    changed = compile_carry(PublicWordFamily(9, 2, 1, 10, (pairs,)), 0, (7, 8))
    other = D.disjoint_kernel_slice(D.normalize(changed))
    assert base.directions == other.directions
    assert base.normalized.transformed.pivot_weights == other.normalized.transformed.pivot_weights
    assert not base.record()["slice_choice_uses_higher_labels"]


def test_valid_external_kernel_directions_do_not_prove_low_only_selection():
    N = D.normalize(circuit(8));known = D.disjoint_kernel_slice(N)
    external = D.restrict_diagonal(N, known.directions)
    assert external.record()["slice_choice_uses_higher_labels"] is None
    assert external.record()["selection_policy"] == "EXTERNAL_SELECTION_PROVENANCE_UNVERIFIED"
    assert not external.record()["selection_provenance_inferred_from_kernel_validity"]


def test_diagonal_quadratic_columns_are_actual_low_a_projections():
    raw = circuit(12);N = D.normalize(raw);S = D.disjoint_kernel_slice(N)
    a_free = tuple(tuple(raw.family.paired_labels[0][site][0][i] % 3 for site in raw.prefix_recipe.free_columns) for i in range(2))
    for j, v in enumerate(S.directions):
        original = tuple(sum(a*x*x for a, x in zip(row, v)) % 3 for row in a_free)
        expected = tuple(sum(a*b for a, b in zip(row, original)) % 3 for row in N.output_inverse)
        assert expected == tuple(row[j] for row in S.quadratic)


def test_disjoint_diagonal_columns_are_uniform_when_low_a_labels_vary_at_fixed_slopes():
    # A conditional population check, not permission to modify a given source.
    observed = Counter()
    for free_a in product(range(3), repeat=4):
        pairs = (((1,), (0,)),)+tuple(((a,), ((1-a) % 3,)) for a in free_a)
        raw = compile_carry(PublicWordFamily(9, 1, 1, 5, (pairs,)), 0, (7,))
        S = D.disjoint_kernel_slice(D.normalize(raw))
        assert len(S.directions) == 2
        observed[S.quadratic[0]] += 1
    assert len(observed) == 9 and set(observed.values()) == {9}


@pytest.mark.parametrize("t", (0, 1, 2, 4, 9))
def test_probe_grid_is_unisolvent_for_all_canonical_degree3_polynomials(t):
    exponents = [(0,)*t]
    for i in range(t):
        for e in (1, 2):
            p = [0]*t;p[i] = e;exponents.append(tuple(p))
    for i, j in combinations(range(t), 2):
        for a, b in ((1, 1), (1, 2), (2, 1)):
            p = [0]*t;p[i], p[j] = a, b;exponents.append(tuple(p))
    for i, j, h in combinations(range(t), 3):
        p = [0]*t;p[i] = p[j] = p[h] = 1;exponents.append(tuple(p))
    grid = D.degree3_probe_points(t)
    assert len(grid) == len(exponents)
    matrix = [[math.prod(x**p for x, p in zip(point, exponent)) % 3 for exponent in exponents] for point in grid]
    assert int(nmod_mat(matrix, 3).rank()) == len(grid)


@pytest.mark.parametrize("k", (2, 8, 12))
def test_mitm_matches_exhaustive_slice_search_and_actual_native_frequency(k):
    S = D.disjoint_kernel_slice(D.normalize(circuit(k)))
    solutions = [z for z in product(range(3), repeat=len(S.directions)) if not any(S.evaluate(z))]
    answer = D.meet_in_middle(S)
    if not solutions:
        assert answer["status"] == "COMPLETE_SEARCH_NO_SOLUTION_ON_THIS_SLICE"
        assert not answer["absence_of_full_prefix_or_root_solutions_inferred"]
    else:
        assert answer["parameters"] in solutions
        assert answer["actual_frequency"] == S.normalized.raw.target
        assert answer["whole_root_target_matched"]
    left = len(S.directions)//2
    assert answer["assignments_evaluated"] <= 3**left+3**(len(S.directions)-left)
    assert answer["stored_entries"] <= 3**left
    assert not answer["cost"]["uniform_solution_sampler"]


@pytest.mark.parametrize("caps", ((1, 100000), (100000, 1)))
def test_solver_preflights_runtime_and_memory_without_false_no_solution(caps):
    S = D.disjoint_kernel_slice(D.normalize(circuit(12)))
    answer = D.meet_in_middle(S, *caps)
    assert answer["status"] == "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION"
    assert answer["assignments_evaluated"] == answer["stored_entries"] == 0


def test_failed_slice_can_have_a_real_full_prefix_witness_outside_it():
    raw = circuit(8);S = D.disjoint_kernel_slice(D.normalize(raw))
    # Search several prescribed targets for an explicit countercontrol to an overbroad cut.
    found = False
    for target in product(range(9), repeat=2):
        c = compile_carry(raw.family, 0, target);s = D.disjoint_kernel_slice(D.normalize(c))
        if D.meet_in_middle(s)["status"] != "COMPLETE_SEARCH_NO_SOLUTION_ON_THIS_SLICE": continue
        for free in product(range(3), repeat=8):
            if not any(c.evaluate(free)):
                assert c.family.frequency(0, c.word(free)) == target
                found = True;break
        if found: break
    assert found


def test_affine_mask_map_is_uniform_and_nonlinear_core_is_fixed_under_complete_high_label_population():
    low = (((1,), (1,)), ((0,), (1,)))
    f = PublicWordFamily(9, 1, 1, 2, (low,));base = compile_carry(f, 0, (7,))
    masks = Counter()
    for digits in product(range(3), repeat=4):
        deltas = tuple(((digits[2*j],), (digits[2*j+1],)) for j in range(2))
        constants, linear = D.affine_mask_change(base, deltas)
        pairs = tuple(tuple(tuple((a+3*d) % 9 for a, d in zip(label, delta)) for label, delta in zip(pair, ds))
                      for pair, ds in zip(low, deltas))
        changed = compile_carry(PublicWordFamily(9, 1, 1, 2, (pairs,)), 0, (7,))
        assert changed.pivot_weights == base.pivot_weights and changed.diagonal_quadratic == base.diagonal_quadratic
        assert changed.constants == tuple((a+b) % 3 for a, b in zip(base.constants, constants))
        assert changed.linear == tuple(tuple((a+b) % 3 for a, b in zip(row, delta)) for row, delta in zip(base.linear, linear))
        masks[(constants, linear)] += 1
    assert len(masks) == 9 and set(masks.values()) == {9}


@pytest.mark.parametrize("n,k", ((1, 2), (2, 2)))
def test_uniform_affine_mask_solution_counts_have_exact_first_and_second_moments(n, k):
    # Independent complete affine-mask population on the actual native cubic core.
    if n == 2: raw = circuit(2)
    else:
        pairs = (((1,), (1,)), ((0,), (1,)), ((2,), (1,)))
        raw = compile_carry(PublicWordFamily(9, 1, 1, 3, (pairs,)), 0, (7,))
    points = tuple(product(range(3), repeat=k));core = [raw.evaluate(u) for u in points]
    counts = []
    for mask in product(range(3), repeat=n*(k+1)):
        c = mask[:n];linear = [mask[n+i*k:n+(i+1)*k] for i in range(n)]
        counts.append(sum(all((v[i]+c[i]+sum(a*x for a, x in zip(linear[i], u))) % 3 == 0 for i in range(n))
                          for u, v in zip(points, core)))
    mean = Fraction(sum(counts), len(counts));variance = sum((Fraction(x)-mean)**2 for x in counts)/len(counts)
    ledger = D.moment_ledger(n, k, k)
    assert mean == Fraction(ledger["single_slice_mean_solution_count"])
    assert variance == Fraction(ledger["single_slice_solution_count_variance"])
    exists = Fraction(sum(x > 0 for x in counts), len(counts))
    assert Fraction(ledger["single_slice_solution_existence_probability_lower"]) <= exists <= Fraction(ledger["single_slice_solution_existence_probability_upper"])


def test_population_ledger_does_not_assign_independence_to_reused_data():
    L = D.moment_ledger(128, 16280, 126)
    assert not L["repeated_slices_on_same_data_are_independent"]
    assert not L["existence_bound_constructs_witness_or_coherent_sampler"]
    assert not L["later_carry_or_full_root_decoder_established"]
    assert len(json.dumps(L)) < 1800


def test_original_all_root_frequency_is_block_additive_and_choices_have_real_source_correlation():
    # Actual wide-label control, not an arbitrary independently sampled vector-sum instance.
    control = json.loads(D.REPORT.read_text())["actual_native_slice_controls"][2]
    data = control["raw_carry"]["public_family"]
    pairs = tuple(tuple(tuple(int(x) for x in a) for a in pair) for pair in data["paired_labels"][0])
    f = PublicWordFamily(int(data["modulus"]), data["dimension"], 1, data["sites"], (pairs,))
    raw = compile_carry(f, 0, tuple(control["raw_carry"]["target"]))
    S = D.disjoint_kernel_slice(D.normalize(raw));q, remaining = f.modulus, f.modulus//3
    base = f.frequency(0, raw.word((0,)*S.record()["free_prefix_trits"]))
    choices = []
    for v in S.directions:
        column = [(0,)*f.dimension]
        for z in (1, 2):
            free = tuple(x*z % 3 for x in v)
            word = raw.word(free)
            assert all(word[j] == raw.offsets[j] for j in raw.prefix_recipe.pivot_columns)
            value = f.frequency(0, word)
            diff = tuple((a-b) % q for a, b in zip(value, base))
            assert all(x % 3 == 0 for x in diff)
            column.append(tuple(x//3 for x in diff))
        choices.append(tuple(column))
        active_a = tuple(sum(f.paired_labels[0][site][0][i] for l, site in enumerate(raw.prefix_recipe.free_columns) if v[l]) % remaining for i in range(f.dimension))
        assert tuple((a+b) % remaining for a, b in zip(column[1], column[2])) == tuple(-x % remaining for x in active_a)
    for z in product(range(3), repeat=len(S.directions)):
        predicted = tuple((base[i]+3*sum(column[value][i] for column, value in zip(choices, z))) % q for i in range(f.dimension))
        assert predicted == f.frequency(0, raw.word(S.free(z)))


def test_actual_word_pair_coefficients_have_unit_minor_but_difference_choices_do_not():
    beta = ((1, 0), (-1, 1), (0, -1))
    for a, b in combinations(beta, 2): assert abs(a[0]*b[1]-a[1]*b[0]) == 1
    differences = ((-2, 1), (-1, -1))
    assert differences[0][0]*differences[1][1]-differences[0][1]*differences[1][0] == 3


def test_live_controls_keep_full_root_mismatch_failure_and_nonexhaustive_count_unknown():
    p = json.loads(D.REPORT.read_text());controls = p["actual_native_slice_controls"]
    assert any(c["solver"]["status"] == "COMPLETE_SEARCH_NO_SOLUTION_ON_THIS_SLICE" for c in controls)
    assert any(c["solver"]["status"] == "VERIFIED_CLASSICAL_FIRST_CARRY_WITNESS" and not c["solver"]["whole_root_target_matched"] for c in controls)
    assert controls[-1]["solution_count"] is None and not controls[-1]["slice_exhaustively_enumerated"]
    assert controls[-1]["degree3_unisolvent_grid_used"]
    assert not p["accepted_speedup_candidate"] and not p["growing_root_classical_preimage_solver_or_uniform_coherent_row_sampler"]


def test_independent_checker_replays_real_native_restrictions_and_paid_solver():
    checker = D.ROOT/"research/certificates/native_carry_diagonal_slice_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("mutation", ("inverse", "direction", "quadratic", "witness", "memory", "mass", "independence", "count", "scope"))
def test_independent_checker_rejects_forged_degree_reduction_or_solver_claims(mutation, tmp_path):
    p = json.loads(D.REPORT.read_text());c = p["actual_native_slice_controls"][1]
    if mutation == "inverse": c["output_normalization"]["output_inverse"][0][0] = (c["output_normalization"]["output_inverse"][0][0]+1) % 3
    if mutation == "direction": c["diagonal_slice"]["directions"][0] = [0]*len(c["diagonal_slice"]["directions"][0])
    if mutation == "quadratic": c["diagonal_slice"]["F3_quadratic_columns"][0][0] = (c["diagonal_slice"]["F3_quadratic_columns"][0][0]+1) % 3
    if mutation == "witness": c["solver"]["native_word"][0] = (c["solver"]["native_word"][0]+1) % 3
    if mutation == "memory": c["solver"]["stored_entries"] = 0
    if mutation == "mass": c["diagonal_slice"]["uniform_prefix_projection_acceptance"]["negative_exponent"] = 0
    if mutation == "independence": c["conditional_population_ledger"]["repeated_slices_on_same_data_are_independent"] = True
    if mutation == "count": p["actual_native_slice_controls"][-1]["solution_count"] = 1
    if mutation == "scope": p["growing_root_classical_preimage_solver_or_uniform_coherent_row_sampler"] = True
    target = tmp_path/"forged.json";target.write_text(json.dumps(p))
    checker = D.ROOT/"research/certificates/native_carry_diagonal_slice_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert result.returncode != 0, mutation
