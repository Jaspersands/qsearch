"""Physical rounding, native posterior laws and construction provenance."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random

import pytest

from theorems.bpqm_gibbs_frontier import MessageLaw, combine, point_channel
from theorems.polar_conditional_sampler import calibration, sample_gibbs, source_biases, transform
from theorems.polar_source_design import (
    Grid, REPORT, LARGE_REPORT, _transitions, combine_self, construct, mean_overlap, point_law,
)


@pytest.mark.parametrize("direction,old_direction", [("upper", "degrade"), ("lower", "upgrade")])
def test_uniform_special_case_matches_existing_independent_integer_combiner(direction, old_direction):
    grid = Grid(8, 1, 32)
    rng = random.Random(29)
    weights = [0]*9
    for _ in range(256):
        weights[rng.randrange(9)] += 1 << 24
    law = tuple(weights)
    for kind, old_kind in (("source_even", "equality"), ("source_odd", "parity")):
        old = combine(MessageLaw(8, 32, law), MessageLaw(8, 32, law), old_kind, direction=old_direction)
        assert combine_self(law, grid, kind, direction=direction) == old.weights
    assert point_law(Fraction(13, 20), grid, direction) == point_channel(Fraction(13, 20), 8, 32, direction=old_direction).weights


@pytest.mark.parametrize("power", [2, 4])
def test_every_nonuniform_transition_brackets_the_exact_native_fraction_and_normalizes(power):
    grid = Grid(8, power, 32)
    upper, lower = _transitions(grid, "upper"), _transitions(grid, "lower")
    D = grid.denominator
    for key, (u_product, u_parity) in upper.items():
        i, j = key
        a, b = Fraction(grid.nodes[i], D), Fraction(grid.nodes[j], D)
        l_product, l_parity = lower[key]
        assert Fraction(grid.nodes[l_product], D) <= a*b <= Fraction(grid.nodes[u_product], D)
        assert sum(d for _, d in u_parity) == 2*D*D
        actual = [(a+b)/(1+a*b)]
        if a*b != 1:
            actual.append(abs(a-b)/(1-a*b))
        for (lo, _), (hi, _), value in zip(l_parity, u_parity, actual):
            assert Fraction(grid.nodes[lo], D) <= value <= Fraction(grid.nodes[hi], D)


@pytest.mark.parametrize("N", [2, 4, 8])
def test_all_native_source_biases_are_bracketed_after_repeated_physical_rounding(N):
    c, grid = Fraction(13, 20), Grid(16, 4, 64)
    native = tuple(2*x for x in source_biases(N, (1-c)/2))
    for direction in ("upper", "lower"):
        laws = (point_law(c, grid, direction),)
        while len(laws) < N:
            laws = tuple(child for parent in laws for child in (
                combine_self(parent, grid, "source_even", direction=direction),
                combine_self(parent, grid, "source_odd", direction=direction)))
        values = tuple(mean_overlap(law, grid) for law in laws)
        assert all(a <= b for a, b in zip(native, values)) if direction == "upper" else all(a >= b for a, b in zip(native, values))


def test_polar_design_upper_bound_controls_actual_all_syndrome_TV_not_just_bias():
    row = construct(8, Fraction(13, 20), 4, grid=Grid(32, 4, 64))
    frozen = tuple(row["frozen_coordinates"])
    native = calibration(8, Fraction(7, 40), frozen)
    assert Fraction(native["frozen_prefix_bias_sum"]) <= Fraction(row["frozen_prefix_bias_sum_upper"])
    assert Fraction(native["uniform_syndrome_average_TV"]) <= Fraction(row["uniform_sign_average_Gibbs_TV_upper"])
    assert not row["full_source_table_materialized"]
    assert row["guarantee_is_average_uniform_sign_not_worst_sign"]


def test_deeper_information_bounds_against_65536_independent_native_source_words():
    # Deliberately exponential TEST calibration, never used by the constructor.
    N, denominator = 16, 40**16
    numerators = [0]*(1 << N)
    weights = [7**w*33**(N-w) for w in range(N+1)]
    for e in range(1 << N):
        numerators[transform(e, N)] = weights[e.bit_count()]
    assert sum(numerators) == denominator
    exact = []
    for i in range(N):
        masses = [[0, 0] for _ in range(1 << i)]
        for u, probability in enumerate(numerators):
            masses[u & ((1 << i)-1)][(u >> i) & 1] += probability
        exact.append(Fraction(sum(abs(a-b) for a, b in masses), denominator))
    row = construct(N, Fraction(13, 20), N//2, grid=Grid(16, 4, 64))
    assert all(a <= b for a, b in zip(exact, map(Fraction, row["all_source_mean_absolute_bias_upper"])))


def test_degradation_is_not_false_first_order_stochastic_ordering_of_posterior_bias():
    def plus(a, b):
        return (((a+b)/(1+a*b), (1+a*b)/2), (abs(a-b)/(1-a*b), (1-a*b)/2))
    lo, hi = plus(Fraction(1, 10), Fraction(9, 10)), plus(Fraction(1, 2), Fraction(9, 10))
    assert sum(w for x, w in hi if x <= Fraction(4, 5)) > sum(w for x, w in lo if x <= Fraction(4, 5))
    assert sum(w for x, w in hi if x <= Fraction(19, 20)) < sum(w for x, w in lo if x <= Fraction(19, 20))
    # CDFs cross. The proof must use flagged PSC channel degradation, not FOSD.


def test_invalid_inputs_and_failed_target_are_not_dequantization_or_hardness_claims():
    for bad in (Grid(8, 4, 32),):
        with pytest.raises(ValueError):
            combine_self((0,)*9, bad, "source_even")
    with pytest.raises(ValueError):
        Grid(7, 4, 32)
    row = construct(16, Fraction(13, 20), 16)
    assert not row["target_certified"]
    assert row["status"] == "UNKNOWN_AT_THIS_GRID_AND_LENGTH_NOT_HARDNESS"
    assert not row["quantum_decoder_executed"]


def test_live_source_design_and_native_samples_replay_without_any_source_table():
    if not REPORT.exists():
        pytest.skip("producer not yet generated")
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/polar_source_design.py").read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not report["all_codes_dequantized"]
    followup = report["explicit_three_eighths_rate_followup"]
    original = report["instances"][followup["source_bound_row_index"]]
    bounds = tuple(map(Fraction, original["all_source_mean_absolute_bias_upper"]))
    assert Fraction(followup["uniform_sign_average_Gibbs_TV_upper"]) == sum(bounds[i] for i in followup["frozen_coordinates"])
    assert Fraction(followup["uniform_sign_average_Gibbs_TV_upper"]) < Fraction(1, 40)
    assert followup["beyond_product_USD_rate_ceiling"]
    assert not followup["prefix_exact_family"]
    assert not followup["worst_case_sign_guarantee"]
    for row in report["instances"]:
        values = tuple(map(Fraction, row["all_source_mean_absolute_bias_upper"]))
        frozen = row["frozen_coordinates"]
        assert len(values) == row["positions"] and len(frozen) == row["constraint_count"]
        assert sum(values[i] for i in frozen)/2 == Fraction(row["frozen_prefix_bias_sum_upper"])
        maximum = row["maximum_frozen_coordinates_at_target"]
        assert len(maximum) == row["maximum_constraints_at_target"]
        assert sum(values[i] for i in maximum) == Fraction(row["maximum_at_target_average_TV_upper"])
        assert Fraction(row["maximum_at_target_average_TV_upper"]) <= Fraction(row["target_average_TV"])
        assert row["maximum_is_for_this_bound_vector_not_true_optimal_code"]
        if row["positions"] <= 64:
            replay = construct(row["positions"], row["channel_overlap"], row["constraint_count"], grid=Grid(**{
                k: row["grid"][k] for k in ("intervals", "power", "mass_bits")}))
            assert {k: v for k, v in row.items() if k not in ("native_Gibbs_samples", "certified_set_Gibbs_samples")} == replay
        for draw in row.get("native_Gibbs_samples", []):
            assert sample_gibbs(row["positions"], row["channel_overlap"], tuple(frozen),
                                int(draw["public_clause_signs_hex"], 16), draw["seed"]) == draw
        for draw in row.get("certified_set_Gibbs_samples", []):
            assert sample_gibbs(row["positions"], row["channel_overlap"], tuple(maximum),
                                int(draw["public_clause_signs_hex"], 16), draw["seed"]) == draw


def test_constructed_nonprefix_code_beyond_USD_has_a_live_native_Gibbs_sampler():
    row = construct(1024, Fraction(13, 20), 512)
    frozen = tuple(row["maximum_frozen_coordinates_at_target"])
    assert len(frozen) == 361 and Fraction(len(frozen), 1024) > Fraction(7, 20)
    assert frozen != tuple(range(len(frozen)))
    assert Fraction(row["maximum_at_target_average_TV_upper"]) < Fraction(1, 10)
    out = sample_gibbs(1024, Fraction(13, 20), frozen, (1 << 1024)-1, 29)
    y = int(out["Gibbs_kernel_word_hex"], 16)
    assert all((y & int(mask, 16)).bit_count() % 2 == 0 for mask in out["code_check_masks_hex"])
    assert not out["unconditional_source_table_materialized"]
    assert out["recursive_work"]["recursive_calls"] == (1024-361)*(2*1024-1)
    # The average-law guarantee comes from the design proof, not this feasible sample.
    assert not out["native_conditional_distribution_certified"]


def test_large_certificate_sums_and_provenance_without_repeating_a_billion_pair_updates():
    if not LARGE_REPORT.exists():
        pytest.skip("large producer not yet generated")
    report = json.loads(LARGE_REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/polar_source_design.py").read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    row, = report["instances"]
    assert (row["positions"], row["constraint_count"]) == (32768, 16384)
    bounds = tuple(map(Fraction, row["all_source_mean_absolute_bias_upper"]))
    assert len(bounds) == 32768 and all(0 <= value <= 1 for value in bounds)
    total = sum(bounds[i] for i in row["frozen_coordinates"])
    assert total == Fraction(row["uniform_sign_average_Gibbs_TV_upper"])
    assert total < Fraction(11, 1000)
    assert row["target_certified"] and row["beyond_product_USD_rate_ceiling"]
    assert row["construction_work"]["channel_combinations"] == 2*32768-2
    assert row["guarantee_is_average_uniform_sign_not_worst_sign"]
