"""Nullspace instrument laws and actual-source classical sampling controls."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random

import numpy as np
import pytest

from theorems.affine_cluster_native_probe import (
    REPORT, exact_native_mixing, native_trajectory, run_controls, socket_instance,
    heatbath_flip_probability, replica_swap_probability, tempering_trajectory,
)
from theorems.bpqm_gibbs_frontier import (
    XorIsing, affine_jump_geometry, affine_system, cluster_step, exact_cluster_kernel,
)


@pytest.mark.parametrize("width", range(1, 7))
def test_affine_geometry_matches_every_possible_next_word(width):
    rng = random.Random(313+width)
    x = rng.randrange(1 << width)
    equations = tuple((a, (a & x).bit_count() % 2)
                      for a in (rng.randrange(1 << width) for _ in range(width+2)))
    system = affine_system(equations, width)
    modes = tuple(range(1 << width))
    geometry = affine_jump_geometry(system, width, modes)
    solutions = [y for y in range(1 << width)
                 if all((a & y).bit_count() % 2 == b for a, b in equations)]
    assert len(solutions) == 1 << geometry["nullity"]
    assert Fraction(geometry["holding_probability_exact"]) == Fraction(1, len(solutions))
    assert Fraction(geometry["expected_hamming_jump_exact"]) == Fraction(
        sum((x ^ y).bit_count() for y in solutions), len(solutions))
    for a, retained in zip(modes, geometry["parity_retained"]):
        actual = Fraction(sum((-1)**((a & y).bit_count() % 2) for y in solutions), len(solutions))
        assert actual == ((-1)**((a & x).bit_count() % 2) if retained else 0)


def test_one_free_direction_can_move_every_coordinate_not_one_coordinate():
    width = 16
    system = affine_system(tuple(((1 << i) | (1 << (i+1)), 0) for i in range(width-1)), width)
    geometry = affine_jump_geometry(system, width, (1, (1 << width)-1))
    assert geometry["nullity"] == 1
    assert geometry["coordinate_parities_fixed"] == 0
    assert geometry["expected_hamming_jump_exact"] == "8"
    assert geometry["holding_probability_exact"] == "1/2"
    assert geometry["parity_retained"] == [False, True]
    assert geometry["mixing_guarantee"] is False


def test_geometry_does_not_change_the_sampler_or_random_stream():
    model, _ = socket_instance(16, random.Random(19))
    x = 153
    for seed in range(6):
        ordinary = cluster_step(model, "13/20", x, random.Random(seed))
        instrumented = cluster_step(model, "13/20", x, random.Random(seed), geometry=True, modes=(1, 17))
        assert {k: v for k, v in instrumented.items() if k != "geometry"} == ordinary


@pytest.mark.parametrize("width", [1, 2, 4, 16, 64])
def test_socket_source_retains_all_raw_degrees_and_parallel_cancellations(width):
    model, source = socket_instance(width, random.Random(29))
    assert len(model.clauses) == 2*width
    assert source["raw_spin_socket_counts"] == [6]*width
    assert all(a.bit_count() in (1, 3) for a, _ in model.clauses)
    assert source["parallel_pairs_cancelled"] == sum((3-a.bit_count())//2 for a, _ in model.clauses)
    assert source["conditioned_on_rank_girth_sign_or_success"] is False
    rebuilt, saved = socket_instance(width, random.Random(29))
    assert model == rebuilt and source == saved
    if width == 1:
        assert source["parallel_pairs_cancelled"] == 2
        assert model.clauses[0][0] == model.clauses[1][0] == 1


def test_rowspan_retention_equals_stationary_character_dirichlet_form():
    model = XorIsing(3, ((3, 0), (6, 1), (5, 0), (7, 1)))
    c = Fraction(13, 20)
    p = 2*c/(1+c)
    target, kernel = exact_cluster_kernel(model, c)
    modes = tuple(range(1, 8))
    mean_retention = [Fraction(0)]*len(modes)
    for x in range(8):
        eligible = model.satisfied(x)
        for bits in product((0, 1), repeat=len(eligible)):
            selected = [eligible[j] for j, flag in enumerate(bits) if flag]
            probability = p**len(selected)*(1-p)**(len(eligible)-len(selected))
            system = affine_system(tuple(model.clauses[j] for j in selected), model.spins)
            geometry = affine_jump_geometry(system, model.spins, modes)
            for i, retained in enumerate(geometry["parity_retained"]):
                mean_retention[i] += target[x]*probability*retained
    for mask, retention in zip(modes, mean_retention):
        values = [(-1)**((mask & x).bit_count() % 2) for x in range(8)]
        energy = sum(target[x]*kernel[x][y]*(values[x]-values[y])**2
                     for x in range(8) for y in range(8))/2
        assert energy == 1-retention
        mean = sum(target[x]*values[x] for x in range(8))
        assert mean*mean <= retention <= 1


def test_exact_native_tv_controls_and_rayleigh_direction_against_dense_spectrum():
    model, _ = socket_instance(4, random.Random(71))
    record = exact_native_mixing(model, "13/20", squarings=2)
    target, kernel = exact_cluster_kernel(model, "13/20")
    previous = Fraction(1)
    for row in record["all_start_TV_controls"]:
        current = Fraction(row["worst_start_TV_exact"])
        assert 0 <= current <= previous
        previous = current
    actual_one_step = max(sum(abs(row[y]-target[y]) for y in range(16))/2 for row in kernel)
    assert Fraction(record["all_start_TV_controls"][0]["worst_start_TV_exact"]) == actual_one_step
    pi = np.array(list(map(float, target)))
    P = np.array([list(map(float, row)) for row in kernel])
    symmetric = np.sqrt(pi[:, None])*P/np.sqrt(pi[None, :])
    assert np.max(abs(symmetric-symmetric.T)) < 1e-14
    eig = np.linalg.eigvalsh(symmetric)
    assert eig[0] >= -1e-13
    assert eig[-1] == pytest.approx(1., abs=1e-14)
    assert 1-eig[-2] <= float(Fraction(record["spectral_gap_upper_from_character_exact"]))+1e-13
    assert record["spectral_gap_lower_bound_inferred_from_character"] is False
    assert record["asymptotic_mixing_proved"] is False


def test_infinite_temperature_exact_native_kernel_is_uniform_after_one_step():
    model, _ = socket_instance(4, random.Random(71))
    record = exact_native_mixing(model, 0, squarings=1)
    assert all(row["worst_start_TV_exact"] == "0" for row in record["all_start_TV_controls"])
    assert record["spectral_gap_upper_from_character_exact"] == "1"


def test_large_native_diagnostics_use_no_exact_kernel_or_stationary_oracle(monkeypatch):
    import theorems.affine_cluster_native_probe as probe
    import theorems.bpqm_gibbs_frontier as frontier
    def forbidden(*args, **kwargs):
        raise AssertionError("exponential Gibbs or kernel oracle in native trajectory")
    monkeypatch.setattr(probe, "exact_cluster_kernel", forbidden)
    monkeypatch.setattr(frontier, "exact_gibbs", forbidden)
    model, _ = socket_instance(64, random.Random(71))
    record = native_trajectory(model, "13/20", seed=31, start=0, steps=24, burn_in=8)
    assert record["affine_solve_calls"] == 24
    assert record["recorded_steps"] == 16
    assert record["mixing_or_TV_certificate"] is False
    assert record["stationary_initialization_claimed"] is False
    assert record["no_exponential_Gibbs_table_used"] is True
    assert 0 <= Fraction(record["mean_hamming_jump"]) <= 64


@pytest.mark.parametrize("c", ["0", "1/2", "13/20"])
def test_heatbath_component_detailed_balance_against_actual_gibbs_weights(c):
    model = XorIsing(2, ((1, 0), (2, 1), (3, 0), (0, 1)))
    value = Fraction(c)
    ratio = (1+value)/(1-value)
    for x in range(4):
        for v in range(2):
            y = x ^ (1 << v)
            incident = [(a, b) for a, b in model.clauses if (a >> v) & 1]
            sx = sum((a & x).bit_count() % 2 == b for a, b in incident)
            sy = sum((a & y).bit_count() % 2 == b for a, b in incident)
            forward = heatbath_flip_probability(c, len(incident), sx)
            reverse = heatbath_flip_probability(c, len(incident), sy)
            wx, wy = ratio**len(model.satisfied(x)), ratio**len(model.satisfied(y))
            assert wx*forward == wy*reverse


def test_swap_detailed_balance_and_acceptance_sign_not_reversed():
    model = XorIsing(2, ((1, 0), (2, 1), (3, 0)))
    for left, right in ((Fraction(0), Fraction(13, 20)), (Fraction(1, 5), Fraction(1, 2))):
        ri, rj = (1+left)/(1-left), (1+right)/(1-right)
        for x, y in product(range(4), repeat=2):
            sx, sy = len(model.satisfied(x)), len(model.satisfied(y))
            forward = replica_swap_probability(left, right, 2*sx-3, 2*sy-3)
            reverse = replica_swap_probability(left, right, 2*sy-3, 2*sx-3)
            assert ri**sx*rj**sy*forward == ri**sy*rj**sx*reverse
        assert replica_swap_probability(left, right, -3, 3) < 1
        assert replica_swap_probability(left, right, 3, -3) == 1


def test_tempering_work_counts_cached_scores_and_no_stationary_oracle(monkeypatch):
    import theorems.bpqm_gibbs_frontier as frontier
    def forbidden(*args, **kwargs):
        raise AssertionError("exact stationary oracle in replica exchange")
    monkeypatch.setattr(frontier, "exact_gibbs", forbidden)
    model, _ = socket_instance(16, random.Random(7))
    result = tempering_trajectory(model, seed=71, start=0, steps=8, burn_in=2)
    word = int(result["target_final_word_hex"], 16)
    assert result["target_final_score"] == 2*len(model.satisfied(word))-len(model.clauses)
    assert result["spin_heatbath_proposals"] == 8*5*16
    assert result["replica_swap_proposals"] == 8*4
    assert result["mixing_or_TV_certificate"] is False


def test_live_report_replay_preserves_full_source_and_no_speedup_scope():
    rebuilt = run_controls()
    assert json.loads(REPORT.read_text()) == rebuilt
    assert rebuilt["large_instance_mixing_certified"] is False
    assert rebuilt["classical_hardness_proved"] is False
    assert rebuilt["quantum_speedup_claim_allowed"] is False
    assert len(rebuilt["native_diagnostic_replays"]) == 6
    for run in rebuilt["native_diagnostic_replays"]:
        assert len(run["trajectories"]) == 2
        assert run["trajectories"][0]["seed"] != run["trajectories"][1]["seed"]
    assert rebuilt["quantum_tree_performance_on_these_finite_blocks_claimed"] is False
    targeted = rebuilt["targeted_stronger_falsifier"]
    assert targeted["chosen_after_short_run_discrepancy_not_an_unbiased_ensemble_estimate"] is True
    assert all(t["steps"] == 8192 for t in targeted["longer_cluster_replays"])
    assert len(targeted["tempering_replays"]) == 2
    reference = targeted["exact_factor_reference"]
    assert reference["full_word_table_materialized"] is False
    expected = Fraction(reference["query_parity_mean_exact"])
    for key in ("longer_cluster_replays", "tempering_replays"):
        for trace in targeted[key]:
            observed = Fraction(trace["observed_parity_means"][0])
            assert Fraction(trace["observed_query_mean_minus_exact_reference"]) == observed-expected
            assert trace["query_mean_discrepancy_is_not_full_law_TV_certificate"] is True


def test_invalid_or_forged_rref_metadata_and_reference_caps_are_rejected():
    system = affine_system(((1, 0), (2, 0)), 2)
    for forged in ({**system, "rank": 1},
                   {**system, "rref": ((1, 1, 0), (0, 1, 0))},
                   {**system, "rref": ((0, 0, 1),)},
                   {**system, "consistent": False}):
        with pytest.raises(ValueError):
            affine_jump_geometry(forged, 2, (1,))
    with pytest.raises(ValueError):
        affine_jump_geometry(system, 2, (4,))
    with pytest.raises(ValueError, match="UNKNOWN"):
        model, _ = socket_instance(16, random.Random(3))
        exact_native_mixing(model, "13/20")
    with pytest.raises(ValueError):
        socket_instance(1, random.Random(3), variable_degree=4, check_degree=5)
    with pytest.raises(ValueError):
        replica_swap_probability("0", "13/20", 1, 2)
    with pytest.raises(ValueError):
        heatbath_flip_probability("1/2", 2, 3)
