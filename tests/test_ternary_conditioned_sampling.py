from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import json
import subprocess

import pytest

from theorems import ternary_conditioned_sampling as sampling
from theorems.ternary_classical_sampling import valid


def problem(forms, offsets):
    return {"spins": len(forms[0]), "forms": forms, "offsets": offsets}


@pytest.mark.parametrize("forms", [((1, 0), (0, 1), (1, 2)), ((1, 1), (2, 2), (0, 0)), ((0, 0),)])
def test_all_original_offsets_and_chart_orders_give_exact_native_uniform_proposals(forms):
    for J in product(range(3), repeat=len(forms)):
        p = problem(forms, J)
        target = {x for x in product(range(3), repeat=2) if valid(p, x)}
        domains = set()
        for order in permutations(range(len(forms))):
            chart = sampling.AffineChart.build(p, order)
            counts = Counter()
            for signs in product((1, 2), repeat=chart.rank):
                y = chart.word(signs)
                if all(y):
                    for coins in product(range(3), repeat=chart.gauge):
                        counts[chart.lift(y, coins)] += 1
            assert set(counts) == target
            assert all(count == 1 for count in counts.values())
            domains.add(2**chart.rank*3**chart.gauge)
        assert len(domains) == 1


def test_rank_conditioned_acceptance_population_law_and_gauge_not_frozen():
    forms = ((1, 1), (2, 2), (1, 1))
    total = Fraction()
    for J in product(range(3), repeat=3):
        p = problem(forms, J)
        chart = sampling.AffineChart.build(p)
        count = sum(valid(p, x) for x in product(range(3), repeat=2))
        total += Fraction(count, 2**chart.rank*3**chart.gauge)
    assert total/27 == Fraction(2, 3)**2
    p = problem(((1, 1),), (0,))
    outputs = {tuple(sampling.rank_sample(p, max_trials=10, seed=seed)["sample"]) for seed in range(100)}
    assert outputs == {x for x in product(range(3), repeat=2) if valid(p, x)}


@pytest.mark.parametrize("forms", [((1, 0), (0, 1), (1, 2)), ((1, 1), (2, 2), (0, 0))])
def test_syndrome_bridge_preserves_every_offset_solution_and_native_gauge(forms):
    for J in product(range(3), repeat=len(forms)):
        p = problem(forms, J)
        bridge = sampling.syndrome_bridge(p)
        image = Counter(tuple((j+sum(a*v for a, v in zip(row, x))) % 3 for row, j in zip(forms, J))
                        for x in product(range(3), repeat=2) if valid(p, x))
        full = {y for y in product((1, 2), repeat=len(forms)) if all(
            sum(a*v for a, v in zip(row, y)) % 3 == s for row, s in zip(bridge["parity_check_G"], bridge["syndrome_GJ"]))}
        assert set(image) == full
        assert all(c == int(bridge["native_lifts_per_full_weight_word"]) for c in image.values())
        assert not bridge["random_dense_code_distribution_claimed"]


def test_rank_chart_is_affine_extension_of_existing_classical_linear_erasure():
    from ternary_decoder_filter import linear_erasure_classical_output
    p = problem(((1, 0), (0, 1), (1, 2)), (2, 0, 1))
    chart = sampling.AffineChart.build(p)
    bridge = sampling.syndrome_bridge(p)
    G, target = bridge["parity_check_G"], bridge["syndrome_GJ"]
    other = [j for j in range(3) if j not in chart.pivots]
    R = tuple(tuple(int(j == f) for f in other) for j in range(3))
    for signs in product((1, 2), repeat=3):
        projected = linear_erasure_classical_output(G, signs, right_inverse=R)
        shifted = tuple((v+sum(a*b for a, b in zip(row, target))) % 3 for v, row in zip(projected, R))
        assert shifted == chart.word(tuple(signs[p] for p in chart.pivots))


def test_dense_code_scope_bound_matches_exhaustive_lines_and_separates_saved_regime():
    lines = [word for word in product(range(3), repeat=3) if any(word) and next(x for x in word if x) == 1]
    for weight in (1, 2, 3):
        probability = Fraction(sum(sum(x != 0 for x in word) <= weight for word in lines), len(lines))
        bound = sampling.dense_code_scope(3, 1, weight)
        assert Fraction(bound["uniform_dense_subspace_nonzero_low_weight_probability_upper"]) == probability
    bound = sampling.dense_code_scope(64, 32, 6)
    assert Fraction(bound["uniform_dense_subspace_nonzero_low_weight_probability_upper"]) < Fraction(1, 100000)
    assert bound["this_is_NOT_a_runtime_lower_bound"]


def test_fixed_rank_budget_keeps_abstention_and_charges_discarded_batch_work():
    impossible = problem(((0, 0),), (0,))
    result = sampling.rank_sample(impossible, max_trials=17, batch_size=8)
    assert result["sample"] is None
    assert result["status"] == "ABSTAIN_FIXED_PROPOSAL_BUDGET"
    assert result["proposals_computed_including_batch_overhead"] == 17
    easy = sampling.rank_sample(problem(((1, 0),), (0,)), max_trials=17, batch_size=8)
    assert easy["logical_trials_to_first_success"] == 1
    assert easy["proposals_computed_including_batch_overhead"] == 8
    assert not easy["SAT_or_count_oracle_used"]


@pytest.mark.parametrize("base", (Fraction(0), Fraction(1), Fraction(2, 3), Fraction(10091, 10092)))
@pytest.mark.parametrize("exponent", (0, 1, 2, 127, 1000))
def test_outward_failure_bounds_enclose_exact_power(base, exponent):
    lo, hi = sampling.power_interval(base, exponent, bits=64)
    assert 0 <= lo <= base**exponent <= hi <= 1
    assert hi-lo <= Fraction(1, 1 << 45)


def test_ternary_pairwise_membership_including_zero_and_rank_deficient_hashes():
    points = list(product(range(3), repeat=2))
    for x in points:
        for y in points:
            single = pair = 0
            for a in product(range(3), repeat=2):
                for b in range(3):
                    hit = sum(i*j for i, j in zip(a, x)) % 3 == b
                    single += hit
                    pair += hit and sum(i*j for i, j in zip(a, y)) % 3 == b
            assert single == 9
            assert pair == (9 if x == y else 3)


def test_all_two_spin_linear_hashes_have_bijective_CNF_models_and_native_cells():
    import pycosat
    p = problem(((0, 0),), (1,))
    for row in product(range(3), repeat=2):
        for b in range(3):
            clauses, support, variables = sampling.cell_cnf(p, (row,), (b,))
            models = list(pycosat.itersolve(clauses, vars=variables))
            words = [sampling.decode(p, [lit for lit in model if abs(lit) in support]) for model in models]
            expected = {x for x in product(range(3), repeat=2) if sum(a*v for a, v in zip(row, x)) % 3 == b}
            assert set(words) == expected
            assert len(words) == len(set(words))


def test_auxiliary_truth_table_independent_of_SAT_has_exactly_one_extension():
    p = problem(((0, 0),), (1,))
    clauses, _, variables = sampling.cell_cnf(p, ((2, 1),), (2,))
    counts = Counter()
    for booleans in product((False, True), repeat=variables):
        if all(any(booleans[abs(lit)-1] == (lit > 0) for lit in row) for row in clauses):
            x = tuple(next(j for j in range(3) if booleans[3*i+j]) for i in range(2))
            counts[x] += 1
    assert counts == Counter({x: 1 for x in product(range(3), repeat=2) if (2*x[0]+x[1]) % 3 == 2})


def test_unique_cell_requires_exhaustion_not_merely_a_found_model():
    p = problem(((0, 0),), (1,))
    multiple = sampling.solve_cell(p, ((0, 0),), (0,))
    assert multiple["status"] == "MULTIPLE" and multiple["sample"] is None
    assert multiple["native_models_seen"] == 2 and not multiple["iterator_exhausted"]
    empty = sampling.solve_cell(p, ((0, 0),), (1,))
    assert empty["status"] == "EMPTY" and empty["sample"] is None and empty["iterator_exhausted"]
    unique = sampling.solve_cell(p, ((1, 0), (0, 1)), (1, 2))
    assert unique["status"] == "UNIQUE" and unique["sample"] == (1, 2) and unique["iterator_exhausted"]


@pytest.mark.parametrize("S", [((0, 0), (0, 1), (1, 0)), ((0, 0), (0, 1), (0, 2), (1, 0))])
def test_complete_hash_family_obeys_isolation_probability_and_TV_bounds(S):
    census = sampling.isolation_census(S, 2)
    bounds = sampling.isolation_bound(len(S), len(S), 9, 32)
    assert Fraction(census["unique_cell_probability_exact"]) >= Fraction(bounds["unique_cell_probability_lower"])
    assert Fraction(census["conditional_isolation_TV_exact"]) <= Fraction(bounds["conditional_sample_TV_upper"])
    assert Fraction(census["first_witness_without_uniqueness_TV_exact"]) > 0


def test_pairwise_hash_isolation_is_not_falsely_promoted_to_exact_uniformity():
    census = sampling.isolation_census(((0, 0), (0, 1), (0, 2), (1, 0)), 2)
    assert Fraction(census["conditional_isolation_TV_exact"]) > 0


def test_hash_shape_uses_only_global_mean_and_retains_unverified_count_assumption():
    p = problem(((1, 0), (0, 1), (1, 1)), (0, 1, 2))
    mean, lower, upper = sampling.annealed_window(p)
    assert mean == Fraction(8, 3)
    rows, cells = sampling.isolation_shape(upper, "1/10")
    assert cells == 3**rows
    bounds = sampling.isolation_bound(lower, upper, cells, 256)
    assert Fraction(bounds["conditional_sample_TV_upper"]) <= Fraction(1, 10)
    assert bounds["bounds_for_UNCAPPED_exact_solver_only"]
    assert bounds["extra_runtime_timeout_or_oracle_failure_mass_NOT_bounded"]


def test_neither_sampler_reads_the_old_exact_count_or_pool_artifact(monkeypatch):
    class ForbiddenCount:
        def read_text(self):
            raise AssertionError("a count oracle was injected into the sampler")

    monkeypatch.setattr(sampling, "COUNTS", ForbiddenCount())
    p = problem(((1,), (1,)), (0, 1))  # Exactly x=1; no reference count passed.
    rank = sampling.rank_sample(p, max_trials=100)
    isolated = sampling.isolation_sample(p, attempts=256)
    assert tuple(rank["sample"]) == (1,)
    assert tuple(isolated["sample"]) == (1,)
    assert not isolated["count_or_complete_pool_used_as_sampler_input"]


def test_singular_hash_is_never_rerolled_and_exhausted_hash_budget_is_abstain(monkeypatch):
    class ZeroCoins:
        def __init__(self, seed):
            pass

        def randrange(self, q):
            return 0

    monkeypatch.setattr(sampling.random, "Random", ZeroCoins)
    p = problem(((0, 0),), (1,))
    result = sampling.isolation_sample(p, attempts=3)
    assert result["status"] == "ABSTAIN_FIXED_HASH_BUDGET"
    assert len(result["cell_traces"]) == 3
    assert all(c["status"] == "MULTIPLE" for c in result["cell_traces"])
    assert not result["partial_cell_witness_accepted"]


def test_timeout_discards_partial_witness_and_never_inherits_uncapped_law(monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 1, output='{"sample":[1,2]}')
    monkeypatch.setattr(sampling.subprocess, "run", timeout)
    result = sampling.isolation_trace(problem(((0, 0),), (1,)), timeout=1)
    assert result["sample"] is None
    assert result["status"] == "UNKNOWN_HASH_SOLVER_TIMEOUT_NO_SAMPLE"
    assert not result["capped_sampler_TV_guarantee_certified"]
    assert not result["skip_slow_cells_and_keep_sampling"]


def test_native_socket_generator_matches_saved_cases_and_entropy_ranks():
    for saved in sampling.saved_cases():
        gen = sampling.native_socket_instance(saved["spins"], saved["source_seed"])
        assert gen["forms"] == tuple(map(tuple, saved["forms"]))
        assert gen["offsets"] == tuple(saved["offsets"])
        ranks = sampling.entropy_hash_rank(gen)
        mean = Fraction(ranks["annealed_mean_exact"])
        h_lo = ranks["entropy_hash_rank_floor"]
        h_hi = ranks["entropy_hash_rank_ceil"]
        assert 3**h_lo <= mean < 3**(h_lo+1)
        assert h_hi == h_lo+1
        assert ranks["isolation_hash_rank"] >= h_hi


def test_cell_timeout_trace_records_unknown_mass_and_rejects_partial_witness(monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 1, output='{"sample":[1,2]}')
    monkeypatch.setattr(sampling.subprocess, "run", timeout)
    p = problem(((0, 0),), (1,))
    traced = sampling.solve_cell_trace(p, ((1, 0),), (1,), timeout=0.5)
    assert traced["status"] == "UNKNOWN_CELL_TIMEOUT"
    assert traced["sample"] is None
    assert traced["timed_out"]
    assert not traced["iterator_exhausted"]
    assert not traced["partial_cell_witness_accepted"]


def test_entropy_rank_hashed_campaign_separates_empty_unique_multiple_and_unconditioned_costs():
    campaign = sampling.entropy_rank_hashed_campaign(
        specs=((16, 711), (20, 713)),
        cells_per_rank=3,
        cell_timeout=None,
        seed=5101,
    )
    assert campaign["deterministic_trial_budgets_distinct_from_wall_budgets"]
    assert campaign["empty_cell_exhaustion_costs_charged"]
    assert campaign["rank_deficient_and_zero_hashes_retained"]
    assert not campaign["capped_runtime_TV_certified"]
    assert not campaign["asymptotic_classical_hardness_or_dequantization_claimed"]
    assert len(campaign["instances"]) == 2
    for row in campaign["instances"]:
        assert not row["source_conditioned_on_satisfiability"]
        assert not row["successful_seeds_selected"]
        unc = row["unconditioned_first_witness"]
        assert unc["status"] == "FIRST_WITNESS_FOUND"
        assert valid(row["problem"], unc["witness"])
        assert unc["first_witness_is_NOT_uniform_sample"]
        for ev in row["rank_evaluations"]:
            assert ev["deterministic_cell_trial_budget"] == 3
            assert (ev["empty_cells_proved"]+ev["unique_cells_proved"]
                    +ev["multiple_cells_rejected"]+ev["timeout_cells_unknown"]) == 3
            assert not ev["slow_cells_discarded"]
            assert not ev["capped_law_certified_by_uncapped_bound"]
            for trace in ev["cell_traces"]:
                if trace["status"] in ("EMPTY", "UNIQUE"):
                    assert trace["iterator_exhausted"]
                if trace["status"] == "UNIQUE":
                    assert valid(row["problem"], trace["sample"])


def test_saved_conditioned_sampling_report_includes_entropy_rank_campaign():
    if not sampling.REPORT.exists():
        pytest.skip("conditioned sampling report not yet generated")
    report = json.loads(sampling.REPORT.read_text())
    assert report["schema_version"] == 2
    campaign = report["entropy_rank_hashed_campaign"]
    assert [row["spins"] for row in campaign["instances"]] == [16, 20, 24, 28, 32]
    assert not report["polynomial_classical_conditional_sampler_established"]
    assert not report["new_quantum_algorithm_or_speedup_claimed"]


@pytest.mark.parametrize("call", [
    lambda: sampling.power_interval("3/2", 2),
    lambda: sampling.isolation_shape(10, 0),
    lambda: sampling.isolation_bound(0, 1, 9, 3),
    lambda: sampling.isolation_bound(10, 2, 27, 3),
    lambda: sampling.isolation_bound(1, 9, 9, 3),
    lambda: sampling.cell_cnf(problem(((1, 0),), (0,)), ((1, True),), (0,)),
    lambda: sampling.AffineChart.build(problem(((1, 0), (0, 1)), (0, 0)), (0, 0)),
    lambda: sampling.native_socket_instance(1, 7),
    lambda: sampling.solve_cell_trace(problem(((1, 0),), (0,)), ((1, 0),), (0,), timeout=0),
    lambda: sampling.entropy_rank_hashed_campaign(specs=()),
])
def test_invalid_bounds_or_sources_fail_closed(call):
    with pytest.raises(ValueError):
        call()
