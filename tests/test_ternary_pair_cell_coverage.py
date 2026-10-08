from fractions import Fraction
from itertools import combinations, product
import math
import random

import pytest

from native_rlwe_primal_babai import exact_row_profile
from ternary_pair_collimation import LowProblem
from ternary_pair_lattice import (
    coset_target, embed, extract_witness, lattice_pair, nearest_plane_list,
    prepared_bases, public_center_offsets, word_coordinates,
)
from ternary_pair_cell_coverage import (
    best_repair_cost, compile_chart, exact_word_census, integer_gs_directions,
    planted_word_probe, population_pair_lower, public_charts, projection_moments, repair_cost, repair_list_size, rounded_errors,
)


def problem(A=(1, 7, 11, 18), Q=27):
    return LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(A[::2], A[1::2])), 0)


def raw_recovered(view, target, prepared):
    data = coset_target(view, (target,), prepared["geometry"])
    if data is None: return set()
    z0, T = data; result = set()
    for basis in prepared["bases"]:
        for offset in prepared["offsets"]:
            center = tuple(a+b for a, b in zip(T, offset))
            for answer in nearest_plane_list(basis["rows"], center, basis["profile"]):
                word, z, norm = extract_witness(view, (target,), z0, answer["point"])
                if word is not None: result.add(word)
    return result


@pytest.mark.parametrize("A,Q", [((0, 3), 9), ((1, 7, 11, 18), 27), ((9, 23, 41, 37, 65, 19), 81)])
def test_exact_predicate_replays_every_word_and_every_target_of_actual_pair_decoder(A, Q):
    view = problem(A, Q); prepared = public_charts(view, seed=83371)
    raw = {t: raw_recovered(view, t, prepared) for t in range(Q)}
    predicted = {t: set() for t in range(Q)}
    for word in product(range(3), repeat=view.width):
        cost = best_repair_cost(word, prepared["charts"])
        recovered = cost is not None and cost <= 1
        assert recovered == (word in raw[view.value(word)[0]])
        if recovered: predicted[view.value(word)[0]].add(word)
    for t in range(Q):
        assert raw[t] == predicted[t]
        solver = lattice_pair(view, (t,), seed=83371,
            prepared=(prepared["geometry"], prepared["bases"]), max_decodes=6*(1+4*view.width))
        assert bool(solver["pair"]) == (len(predicted[t]) >= 2)
    census = exact_word_census(view, prepared)
    depth = census["layers"][0]["depths"][1]
    assert depth["pair_covered_targets"] == sum(len(v) >= 2 for v in predicted.values())
    assert depth["recovered_words"] == sum(map(len, predicted.values()))


def test_primitive_gs_projection_reciprocal_and_exact_native_error_values():
    view = problem(); prepared = public_charts(view)
    for basis, directions in zip(prepared["bases"], prepared["directions"]):
        for i, row in enumerate(directions):
            v = row["direction"]
            assert math.gcd(*v) == 1
            assert all(sum(a*b for a, b in zip(v, prior)) == 0 for prior in basis["rows"][:i])
            assert row["multiplier"] == Fraction(1, sum(a*b for a, b in zip(v, basis["rows"][i])))
        for offset in prepared["offsets"]:
            chart = compile_chart(directions, offset)
            for word in product(range(3), repeat=view.width):
                z = word_coordinates(word); E = embed(z); ones = embed([1]*len(z))
                error = tuple(a-3*b+c for a, b, c in zip(ones, E, offset))
                expected = []
                for row in directions:
                    rho = sum(a*b for a, b in zip(error, row["direction"]))*row["multiplier"]
                    expected.append((2*rho.numerator+rho.denominator)//(2*rho.denominator))
                assert rounded_errors(word, chart) == tuple(expected)


def test_half_cell_boundaries_are_asymmetric_and_exact():
    rows = ((3, -3, 0), (3, 0, -3)); profile = exact_row_profile(rows)
    directions = integer_gs_directions(rows, profile)
    chart = compile_chart(directions, (0, 0, 0))
    assert rounded_errors((0,), chart)[0] == 1  # +1/2, outside.
    assert rounded_errors((1,), chart)[0] == 0  # -1/2, inside.
    eps = Fraction(1, 10**25)
    for sign in (-1, 1):
        offset = (sign*eps, -sign*eps, 0)
        changed = compile_chart(directions, offset)
        assert rounded_errors((0,), changed)[0] == (0 if sign < 0 else 1)
        assert rounded_errors((1,), changed)[0] == (-1 if sign < 0 else 0)


def test_exact_uniform_native_projection_moments_and_covariances_without_independence():
    prepared = public_charts(problem(), basis_count=1)
    direction = prepared["directions"][0]
    errors = []
    for word in product(range(3), repeat=2):
        z = word_coordinates(word); E = embed(z); ones = embed([1]*len(z))
        e = tuple(a-3*b for a, b in zip(ones, E)); errors.append(e)
    projections = [[sum(a*b for a, b in zip(e, row["direction"]))*row["multiplier"] for e in errors] for row in direction]
    for i, row in enumerate(direction):
        for offset in prepared["offsets"]:
            mean = sum(a*b for a, b in zip(offset, row["direction"]))*row["multiplier"]
            values = [x+mean for x in projections[i]]; moments = projection_moments(row, offset)
            assert sum(values)/len(values) == moments["mean"]
            assert sum(x*x for x in values)/len(values) == moments["raw_second"]
            assert sum(x**4 for x in values)/len(values) == moments["raw_fourth"]
            true_strict_tail = Fraction(sum(abs(x) > Fraction(1, 2) for x in values), len(values))
            true_rounding = Fraction(sum((2*x.numerator+x.denominator)//(2*x.denominator) != 0 for x in values), len(values))
            assert moments["strict_half_cell_tail_probability_lower"] <= true_strict_tail
            assert true_rounding <= moments["rounding_error_probability_upper"]
        moments = projection_moments(row)
        assert sum(x**3 for x in projections[i])/len(errors) == moments["centered_third"]
        for j in range(i): assert sum(a*b for a, b in zip(projections[i], projections[j])) == 0
    # Uncorrelated variables are not independent: an exact shared native block.
    rows = ((3, -3, 0), (3, 0, -3)); d = integer_gs_directions(rows, exact_row_profile(rows))
    values = []
    for w in ((0,), (1,), (2,)):
        E = embed(word_coordinates(w)); e = tuple(a-3*b for a, b in zip(embed((1, 1)), E))
        values.append(tuple(sum(a*b for a, b in zip(e, r["direction"]))*r["multiplier"] for r in d))
    assert sum(x*y for x, y in values) == 0
    assert Fraction(sum(x == 0 and y < 0 for x, y in values), 3) != Fraction(sum(x == 0 for x, y in values), 3)*Fraction(sum(y < 0 for x, y in values), 3)


def generalized_points(rows, profile, target, repairs, magnitude):
    d = len(rows); mu = profile["mu"]; norms = profile["gs_squared"]
    inner = []
    for i, row in enumerate(rows):
        inner.append(sum(x*y for x, y in zip(row, target))-sum(mu[i][j]*inner[j] for j in range(i)))
    shifts = [x for x in range(-magnitude, magnitude+1) if x]
    for k in range(repairs+1):
        for indices in combinations(range(d), k):
            for values in product(shifts, repeat=k):
                forced = dict(zip(indices, values)); coordinates = [a/b for a, b in zip(inner, norms)]; coeff = [0]*d
                for i in range(d-1, -1, -1):
                    x = coordinates[i]
                    coeff[i] = (2*x.numerator+x.denominator)//(2*x.denominator)+forced.get(i, 0)
                    for j in range(i): coordinates[j] -= coeff[i]*mu[i][j]
                yield tuple(sum(c*r[j] for c, r in zip(coeff, rows)) for j in range(len(target)))


@pytest.mark.parametrize("k,B", [(0, 1), (1, 1), (2, 1), (1, 2), (2, 2)])
def test_general_repair_predicate_iff_actual_forced_rounding_paths(k, B):
    view = problem(); prepared = public_charts(view, basis_count=1, perturbations=0)
    basis = prepared["bases"][0]; chart = prepared["charts"][0]; by_target = {}
    for word in product(range(3), repeat=2):
        t = view.value(word)[0]
        if t not in by_target:
            z0, T = coset_target(view, (t,), prepared["geometry"])
            points = list(generalized_points(basis["rows"], basis["profile"], T, k, B))
            assert len(points) == repair_list_size(4, k, B)
            by_target[t] = {extract_witness(view, (t,), z0, p)[0] for p in points}
        cost = repair_cost(rounded_errors(word, chart), B)
        assert (word in by_target[t]) == (cost is not None and cost <= k)


def test_counting_bound_and_distinct_pair_layers_include_empty_and_singleton_targets():
    view = problem(); prepared = public_charts(view)
    census = exact_word_census(view, prepared)
    assert census["words_classified"] == 9
    assert census["empty_uniform_targets"] == 19
    assert census["singleton_uniform_targets"] == 7
    assert census["true_pair_targets"] == 1
    for layer in census["layers"]:
        last = 0
        for row in layer["depths"]:
            beta = Fraction(row["beta_exact_conditional_uniform_targets"])
            gamma = Fraction(row["gamma_exact_conditional"])
            assert beta <= gamma/6
            assert Fraction(row["full_truth_minus_missing_words_pair_lower"]) <= beta
            assert row["pair_covered_targets"] >= last; last = row["pair_covered_targets"]
    capped = exact_word_census(view, prepared, max_words=8)
    assert capped["status"] == "WORD_BUDGET_NO_PARTIAL_CENSUS" and capped["words_classified"] == 0


def test_easy_zero_labels_can_have_tiny_word_recovery_yet_a_verified_pair():
    M = 4; view = problem((0,)*(2*M), 3**(M+1))
    # The explicit unreduced block basis isolates the metric pitfall.
    rows = tuple(tuple(3*x for x in embed([int(i == j) for i in range(2*M)])) for j in range(2*M))
    directions = integer_gs_directions(rows, exact_row_profile(rows)); chart = compile_chart(directions, (0,)*(3*M))
    histogram = {}
    for word in product(range(3), repeat=M):
        k = repair_cost(rounded_errors(word, chart)); histogram[k] = histogram.get(k, 0)+1
    assert histogram == {k: math.comb(M, k)*2**k for k in range(M+1)}
    assert lattice_pair(view, (0,))["pair"]
    assert Fraction(histogram[0]+histogram[1], 3**M) == Fraction(1+2*M, 3**M)
    # Tiny word fraction is not a hardness or pair-finding impossibility claim.


def test_planted_geometry_records_are_never_uniform_target_pair_coverage():
    view = problem(); prepared = public_charts(view)
    a = planted_word_probe(view, prepared, samples=64, seed=881)
    b = planted_word_probe(view, prepared, samples=64, seed=881)
    assert a == b
    assert a["targets_would_be_planted_size_biased"]
    assert not a["uniform_target_pair_coverage_estimated"]
    assert sum(a["minimum_repairs_magnitude_one_histogram"].values()) == 64
    for i, stats in enumerate(a["repair_pattern_sample_statistics"]):
        errors = [rounded_errors(tuple(w["word"]), prepared["charts"][i]) for w in a["word_records"]]
        pairs = sum(errors[i] == errors[j] for i in range(64) for j in range(i))
        assert stats["equal_pattern_sample_pairs"] == pairs
        assert Fraction(stats["empirical_pair_collision_rate_not_population_proof"]) == Fraction(pairs, math.comb(64, 2))
    single = planted_word_probe(view, prepared, samples=1)
    assert all(x["empirical_pair_collision_rate_not_population_proof"] is None for x in single["repair_pattern_sample_statistics"])
    with pytest.raises(ValueError): planted_word_probe(problem((1, 2)), prepared)


def test_real_pair_counterexample_is_replayed_against_actual_full_scheduled_decoder():
    rng = random.Random(83370); view = problem(tuple(rng.randrange(2187) for _ in range(12)), 2187)
    prepared = public_charts(view, 83376)
    result = exact_word_census(view, prepared)
    c = result["missed_pair_target_certificate"]
    assert c is not None and len(c["complete_actual_fiber"]) >= 2
    assert sum(k is not None and k <= 1 for k in c["minimum_repairs_per_word_magnitude_one"]) < 2
    assert all(view.value(w) == (int(c["target"]),) for w in c["complete_actual_fiber"])
    assert c["actual_decoder_candidate_cost"] == 150
    assert "EXHAUSTED" in c["actual_complete_scheduled_decoder_status"]


def test_population_word_to_pair_lower_survives_complete_native_label_census():
    gamma_sum = Fraction(0); beta_sum = Fraction(0)
    for A in product(range(9), repeat=2):
        view = problem(A, 9); prepared = public_charts(view, seed=883)
        row = exact_word_census(view, prepared)["layers"][0]["depths"][1]
        gamma_sum += Fraction(row["gamma_exact_conditional"])
        beta_sum += Fraction(row["beta_exact_conditional_uniform_targets"])
    lower = population_pair_lower(1, gamma_sum/81)
    assert Fraction(lower["population_beta_lower_if_expected_gamma_proved"]) <= beta_sum/81
    assert lower["expected_gamma_is_an_unproved_assumption_not_a_sample_estimate"]
    assert population_pair_lower(10, Fraction(8, 9))["population_beta_lower_if_expected_gamma_proved"] == "0"
    assert Fraction(population_pair_lower(10, Fraction(9, 10))["population_beta_lower_if_expected_gamma_proved"]) > 0
    with pytest.raises(ValueError): population_pair_lower(10, 0.9)


@pytest.mark.parametrize("call", [lambda: repair_cost((0,), True), lambda: repair_cost((0.5,)), lambda: repair_list_size(2, 3),
    lambda: rounded_errors((True,), ()), lambda: public_center_offsets(0),
    lambda: public_center_offsets(1, seed=True), lambda: best_repair_cost((0,), ()),
    lambda: compile_chart((), ()), lambda: planted_word_probe(problem(), public_charts(problem()), samples=0)])
def test_invalid_inputs_rejected(call):
    with pytest.raises(ValueError): call()
