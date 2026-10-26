from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
import pytest

from theorems import paired_residual_classical as f


def control():
    problem = f.Problem(11, 6, (1, 2, 3, 4, 5),
                        tuple(tuple((i+j*j) % 11 for j in range(1, 6)) for i in range(5)))
    positions = (0, 2, 4)
    x, y = np.zeros(5, dtype=np.int64), np.zeros(5, dtype=np.int64)
    for j, i in enumerate(positions):
        x[i] = j+2
        y[i] = (problem.allowed[i][j]-problem.multipliers[i]*x[i]**2) % 11
    c = f.coefficients_from_information(problem, positions, x, y)
    return problem, positions, c


def test_nonconsecutive_information_map_equals_original_polynomial_evaluation():
    problem, positions, c = control()
    A, B = f.information_map(problem, positions)
    x, y = problem.values(c)
    assert np.array_equal((A@x[list(positions)]+B@y[list(positions)]) % 11, x)
    assert np.array_equal((B@x[list(positions)]+A@y[list(positions)]) % 11, y)
    assert f.coefficients_from_information(problem, positions, x, y) == c
    for j, anchor in enumerate(positions):
        assert A[anchor, j] == 1 and B[anchor, j] == 0
        for i in set(range(problem.M))-set(positions):
            assert (A[i, j]**2-B[i, j]**2) % problem.p != 0


def test_every_intrinsic_move_matches_quartic_and_reconstructs_a_native_polynomial():
    problem, I, c = control()
    x, y = problem.values(c)
    A, B = f.information_map(problem, I)
    original = problem.residuals(x, y)
    for j, anchor in enumerate(I):
        for kind in ("root", "residual"):
            symbols = list(range(11)) if kind == "root" else problem.allowed[anchor]
            old = int(x[anchor]) if kind == "root" else int(original[anchor])
            curve = f.residual_polynomial(problem, x, y, A[:, j], B[:, j], anchor, kind)
            predicted = f.evaluate_residual_polynomial(curve, (np.array(symbols)-old) % 11, 11)
            for row, symbol in enumerate(symbols):
                xx, yy = f.move(problem, x, y, A[:, j], B[:, j], anchor, kind, symbol)
                assert np.array_equal(predicted[row], problem.residuals(xx, yy))
                for i in I:
                    assert int(problem.residuals(xx, yy)[i]) in problem.allowed[i]
                    if kind == "root" or i != anchor:
                        assert problem.residuals(xx, yy)[i] == original[i]
                cc = f.coefficients_from_information(problem, I, xx, yy)
                check_x, check_y = problem.values(cc)
                assert np.array_equal(xx, check_x) and np.array_equal(yy, check_y)
            degree = 4 if kind == "root" else 2
            assert len(curve) == degree+1
            assert all(curve[-1, i] != 0 for i in set(range(5))-set(I))


def test_dropping_quadratic_value_displacement_does_not_preserve_anchor_residual():
    problem, I, c = control()
    x, y = problem.values(c)
    anchor = I[0]
    delta = 1
    wrong_x = (int(x[anchor])+delta) % 11
    wrong_y = (int(y[anchor])-2*problem.multipliers[anchor]*int(x[anchor])*delta) % 11
    wrong = (wrong_y+problem.multipliers[anchor]*wrong_x**2) % 11
    assert wrong != problem.residuals(x, y)[anchor]


def test_greedy_search_is_native_monotone_and_charges_all_proposals():
    problem, I, c = control()
    result = f.greedy_search(problem, c, positions=I, max_sweeps=2, batch=4)
    assert result["final_score"] == problem.independent_score(result["coefficients"])
    assert all(row["after"] >= row["before"] for row in result["trace"])
    proposals_per_sweep = problem.K*(problem.p+(problem.p-1)//2)
    assert result["work"]["candidate_evaluations"] == proposals_per_sweep*result["work"]["sweeps_completed"]
    assert result["work"]["predicate_lookups"] == result["work"]["candidate_evaluations"]*problem.M
    if result["status"] == "COMPLETE_INTRINSIC_COORDINATE_FIXED_POINT":
        last = result["trace"][-2*problem.K:]
        assert not any(row["strict_improvement"] for row in last)
    assert not result["global_optimum_or_classical_lower_bound_claimed"]


def test_batch_size_does_not_change_the_exact_coordinate_search():
    problem, I, c = control()
    a = f.greedy_search(problem, c, positions=I, max_sweeps=1, batch=1)
    b = f.greedy_search(problem, c, positions=I, max_sweeps=1, batch=20)
    assert a["coefficients"] == b["coefficients"]
    assert a["trace"] == b["trace"]


def test_two_coordinate_block_moves_and_annealing_preserve_information_feasibility():
    problem, I, c = control()
    x, y = problem.values(c)
    A, B = f.information_map(problem, I)
    nx, ny = f.block_move(problem, x, y, A, B, 0, 2, I[0], I[2],
                          "root", 7, "residual", problem.allowed[I[2]][-1])
    seq_x, seq_y = f.move(problem, x, y, A[:, 0], B[:, 0], I[0], "root", 7)
    seq_x, seq_y = f.move(problem, seq_x, seq_y, A[:, 2], B[:, 2],
                          I[2], "residual", problem.allowed[I[2]][-1])
    assert np.array_equal(nx, seq_x) and np.array_equal(ny, seq_y)
    nr = problem.residuals(nx, ny)
    assert all(int(nr[i]) in problem.allowed[i] for i in I)

    block_res = f.block_search(problem, c, positions=I, proposals=32, seed=91)
    assert block_res["final_score"] == problem.independent_score(block_res["coefficients"])
    assert block_res["work"]["candidate_evaluations"] == 32
    assert block_res["work"]["predicate_lookups"] == 32*problem.M

    anneal_res = f.annealing_search(problem, c, positions=I, steps=32, seed=92)
    assert anneal_res["best_score"] == problem.independent_score(anneal_res["coefficients"])
    assert anneal_res["best_score"] >= anneal_res["initial_score"]
    assert anneal_res["work"]["candidate_evaluations"] == 32

    fresh = f.random_information_witness(problem, (1, 2, 3), 93)
    fx, fy = problem.values(fresh)
    fr = problem.residuals(fx, fy)
    assert all(int(fr[i]) in problem.allowed[i] for i in (1, 2, 3))


def test_conditioned_target_counts_and_full_pair_law_by_all_coefficients():
    result = f.conditional_control()
    one, full = result["rows"]
    assert one["accepted_polynomials"] == 3*7**3
    assert full["accepted_polynomials"] == (7*3)**2
    assert Q(one["pair_TV_exact"]) == 0
    assert Q(full["pair_TV_exact"]) > 0
    for row in result["rows"]:
        assert Q(row["pair_chi_square_exact"]) <= Q(row["bound"]["unforced_pair_chi_square_upper_exact"])
        assert Q(row["mean_fraction_exact"]) <= Q(row["bound"]["uniform_component_mean_upper_exact"])


def test_native_uniform_component_is_not_a_bound_on_adaptive_search():
    bound = f.uniform_component_bound(2053, 1026, 204)
    assert Q(bound["uniform_component_mean_upper_exact"]) < Q(55, 100)
    assert Q(bound["unforced_pair_TV_upper_exact"]) > 0
    assert Q(bound["unforced_pair_TV_upper_exact"]) < Q(1, 10**48)
    assert bound["input_sets_may_be_fixed_adversarial"]
    assert not bound["adaptive_within_component_search_covered"]
    assert not bound["full_unforced_joint_distribution_identified"]
    for pins in (0, 1, 101):
        assert Q(f.uniform_component_bound(2053, 1026, 204, pins)["unforced_pair_TV_upper_exact"]) == 0


@pytest.mark.parametrize("allowed", [(0, 1, 2), (1, 2, 4), (2, 3, 6)])
def test_parabolic_halfset_has_no_complete_nonconstant_affine_line(allowed):
    p, b = 7, 3
    for x, y in product(range(p), repeat=2):
        for dx, dy in [(0, 1), *[(1, d) for d in range(p)]]:
            images = {((y+t*dy)+b*(x+t*dx)**2) % p for t in range(p)}
            assert len(images) in ((p+1)//2, p)
            assert not images.issubset(allowed)


def test_invalid_moves_and_information_domains_fail_closed():
    problem, I, c = control()
    x, y = problem.values(c)
    A, B = f.information_map(problem, I)
    with pytest.raises(ValueError):
        f.information_map(problem, (0, 0, 2))
    with pytest.raises(ValueError):
        f.move(problem, x, y, A[:, 0], B[:, 0], I[0], "residual", 0)
    with pytest.raises(ValueError):
        f.block_move(problem, x, y, A, B, 0, 0, I[0], I[0], "root", 1, "root", 2)
    with pytest.raises(ValueError):
        f.uniform_component_bound(11, 5, 6, 4)
    with pytest.raises(ValueError):
        f.greedy_search(problem, c, positions=I, max_sweeps=0)
    with pytest.raises(ValueError):
        f.annealing_search(problem, c, positions=I, steps=8, t_start=0.2, t_end=0.5)


def test_live_native_record_has_independent_original_polynomial_replay():
    if not f.REPORT.exists():
        pytest.skip("live producer artifact not generated yet")
    report = json.loads(f.REPORT.read_text())
    native = report["native_search"]
    assert report["same_paired_instance_and_starting_polynomial"]
    assert native["initial_score"] == 536
    assert native["final_score"] >= native["initial_score"]
    assert native["original_Horner_and_full_value_replay"]
    assert native["work"]["restarts"] == 0
    assert native["work"]["candidate_evaluations"] == sum(row["proposals"] for row in native["trace"])
    assert not native["full_classical_portfolio_complete"]
    portfolio = report["portfolio_campaign"]
    assert portfolio["starting_fixed_point_score"] == 632
    assert portfolio["best_portfolio_score"] >= 633
    assert portfolio["escaped_initial_single_coordinate_fixed_point"]
    assert portfolio["all_runs_and_nonimproving_trajectories_retained"]
    assert portfolio["original_Horner_and_full_value_replay"]
    assert not portfolio["full_classical_portfolio_complete"]
    assert not report["quantum_advantage_or_general_classical_hardness_established"]
