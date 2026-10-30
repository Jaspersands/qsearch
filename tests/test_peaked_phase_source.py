"""Peak/noise promise controls; no simulated scalable quantum learner."""
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from theorems.peaked_phase_source import (
    PeakPhasePlan, graph_basis_probability, quadratic_verifier_caps,
    reference_bad_offsets, reference_selection, stabilizer_basis_caps,
)


@pytest.mark.parametrize("p,R", [(3, 1), (3, 2), (11, 10), (101, 3), (2**127-1, 7)])
def test_public_grid_uses_peak_and_trace_not_input_rank(p, R):
    plan = PeakPhasePlan(p, R)
    assert plan.interval_width >= Fraction(1, 2*R*(R+1))
    assert plan.retained_rank_bound < p
    assert plan.retained_rank_bound <= 2*R-1
    for offset in (0, plan.offset_count//2, plan.offset_count-1):
        t = plan.threshold(offset)
        assert Fraction(1, p) < t < Fraction(1, R)
        assert t-plan.spectral_margin > Fraction(1, 4*R)
    assert plan.bad_offset_probability_bound <= plan.failure_budget/8


def test_full_exponential_rank_and_arbitrarily_small_tail_weights_are_allowed():
    p, n, R = 101, 200, 3
    dimension = p**n
    plan = PeakPhasePlan(p, R)
    bands = ((Fraction(1, R), 1), (Fraction(R-1, R*(dimension-1)), dimension-1))
    result = reference_selection(plan, bands, 0)
    assert result["input_rank"] == dimension
    assert result["input_rank"] % p == 0
    assert result["retained_rank"] == 1
    assert result["retained_mass"] == Fraction(1, R)
    assert result["retained_minimum_normalized_weight"] == 1
    assert result["known_spectrum_reference_only"] and not result["spectrum_measured"]


def test_near_characteristic_peak_avoids_selecting_a_divisible_rank():
    plan = PeakPhasePlan(5, 4)
    # Full rank 5, with one heavy eigenvalue and four equal lighter ones.
    bands = ((Fraction(1, 4), 1), (Fraction(3, 16), 4))
    for offset in (0, plan.offset_count-1):
        result = reference_selection(plan, bands, offset)
        assert result["retained_rank"] == 1
        assert result["retained_mass"] == Fraction(1, 4)


def test_bad_threshold_event_is_not_silently_certified_or_hidden_by_huge_multiplicity():
    plan = PeakPhasePlan(11, 3, Fraction(1, 4))
    eigenvalue = plan.threshold(91)
    dimension = 2**100
    remaining = 1-Fraction(1, 3)-eigenvalue
    bands = ((Fraction(1, 3), 1), (eigenvalue, 1), (remaining/(dimension-2), dimension-2))
    bad = reference_bad_offsets(plan, bands)
    assert 91 in bad
    assert len(bad) <= plan.nearby_eigenvalue_count_bound
    assert not reference_selection(plan, bands, 91)["good_grid_offset"]
    assert Fraction(len(bad), plan.offset_count) <= plan.bad_offset_probability_bound


def test_degenerate_retained_eigenspace_is_kept_whole():
    plan = PeakPhasePlan(11, 3)
    bands = ((Fraction(1, 3), 2), (Fraction(1, 99), 33))
    result = reference_selection(plan, bands, 0)
    assert result["retained_rank"] == 2
    assert result["retained_mass"] == Fraction(2, 3)
    assert result["retained_minimum_normalized_weight"] == Fraction(1, 2)


@pytest.mark.parametrize("R,outputs", [(1, 1), (2, 17), (7, 1000)])
def test_preparation_clocks_charge_targets_and_explicitly_exclude_programs(R, outputs):
    plan = PeakPhasePlan(101, R)
    caps = plan.preparation_caps(outputs)
    assert caps["filtered_input_cap"] == outputs*(caps["growth_attempts_per_output"]+1)
    assert caps["filter_target_copy_cap"] == caps["filtered_input_cap"]*caps["filter_trials_per_input"]
    assert caps["growth_abort_bound"] <= plan.failure_budget
    assert caps["filter_abort_bound"] <= plan.failure_budget
    assert caps["filter_half_diamond_allowance_per_call"]*caps["filter_target_copy_cap"] == plan.failure_budget/2
    assert caps["rank_training_precision"] <= plan.spectral_margin/2
    assert not caps["dme_program_copies_included"]
    assert not caps["physical_quantum_preparer_implemented"]


@pytest.mark.parametrize("p", [3, 5, 11, 29])
def test_full_support_quadratic_gap_and_near_threshold_r_fifth_power_boundary(p):
    R, m = p-1, (p-1)//2
    weights = tuple(Fraction(1, p)+(Fraction(m-min(j, p-j))-Fraction(m*m, p))/
                    (R*m*(m+1)) for j in range(p))
    assert sum(weights) == 1 and min(weights) > 0 and max(weights) == Fraction(1, R)
    cap = quadratic_verifier_caps(p, 2, R)
    gap = cap["wrong_candidate_purity_loss_lower_bound"]
    for shift in range(1, p):
        loss = sum((weights[j]-weights[(j-shift) % p])**2 for j in range(p))/2
        assert loss >= gap
    adjacent_loss = sum((weights[j]-weights[(j-1) % p])**2 for j in range(p))/2
    assert adjacent_loss == Fraction(1, R**2*m*(m+1)**2)
    assert 2 <= adjacent_loss*R**5 < 8
    if p == 29:
        # The simpler p>2R gap cannot be reused when R<p<=2R.
        assert adjacent_loss < Fraction(1, 16*R**3)


def _phase(p, quadratic, label):
    return np.exp(2j*np.pi*(quadratic*np.arange(p)**2+label*np.arange(p))/p)/np.sqrt(p)


def _rho(p, quadratic, weights):
    return sum(float(w)*np.outer(v, v.conj()) for label, w in enumerate(weights)
               for v in [_phase(p, quadratic, label)])


def test_actual_full_rank_quadratic_density_retains_verifiable_shift_gap():
    p, R = 5, 3
    weights = (Fraction(1, 3),)+(Fraction(1, 6),)*4
    rho = _rho(p, 1, weights)
    assert np.linalg.matrix_rank(rho) == p
    for y, z in product(range(p), repeat=2):
        W = np.diag(np.exp(2j*np.pi*z*np.arange(p)/p))@np.roll(np.eye(p), y, axis=0)
        loss = np.trace(rho@rho-rho@W@rho@W.conj().T).real
        f = (z-2*y) % p
        exact = sum((weights[b]-weights[(b-f) % p])**2 for b in range(p))/2
        assert loss == pytest.approx(float(exact))
        if f:
            assert exact >= quadratic_verifier_caps(p, 1, R)["wrong_candidate_purity_loss_lower_bound"]


def test_characteristic_peak_boundary_is_information_theoretic_not_a_runtime_guard():
    p = 5
    weights = (Fraction(1, p),)*p
    assert np.allclose(_rho(p, 0, weights), _rho(p, 1, weights))
    with pytest.raises(ValueError, match="less than prime"):
        PeakPhasePlan(p, p)
    plan = PeakPhasePlan(p, p-1)
    with pytest.raises(ValueError, match="peak promise"):
        reference_selection(plan, ((Fraction(1, p), p),), 0)


def test_tiny_excess_over_characteristic_threshold_needs_an_explicit_margin():
    p, xi = 5, Fraction(1, 2**18)
    weights = ((1-xi)/p+xi,)+((1-xi)/p,)*(p-1)
    assert max(weights) > Fraction(1, p)
    distance = sum(abs(np.linalg.eigvalsh(_rho(p, 0, weights)-_rho(p, 1, weights))))/2
    assert 0 < distance <= float(xi)+1e-14
    with pytest.raises(ValueError, match="peak promise"):
        reference_selection(PeakPhasePlan(p, p-1), tuple((w, 1) for w in weights), 0)


def test_strict_full_support_endpoint_can_be_identifiable_but_arbitrarily_ill_conditioned():
    p, d, s = 3, 9, Fraction(1, 64)
    t = s*(Fraction(1, p)-Fraction(1, d))/(1-Fraction(1, p))
    points = tuple(product(range(p), repeat=2))
    weights = tuple((1-s-t)*Fraction(int(b[1] == 0), p)+s/d+t*int(b == (0, 0))
                    for b in points)
    assert sum(weights) == 1 and min(weights) > 0 and max(weights) == Fraction(1, p)
    densities = []
    for quadratic in (0, 1):
        rho = np.zeros((d, d), dtype=complex)
        for b, w in zip(points, weights):
            state = np.array([np.exp(2j*np.pi*(quadratic*x[0]**2+sum(a*c for a, c in zip(b, x)))/p)
                              for x in points])/np.sqrt(d)
            rho += float(w)*np.outer(state, state.conj())
        assert np.linalg.matrix_rank(rho) == d
        densities.append(rho)
    distance = sum(abs(np.linalg.eigvalsh(densities[0]-densities[1])))/2
    assert 0 < distance <= float(t)+1e-14


def test_large_fidelity_alone_does_not_replace_phase_diagonal_promise():
    p = 5
    u, v = _phase(p, 0, 0), _phase(p, 1, 0)
    rho = (np.outer(u, u.conj())+np.outer(v, v.conj()))/2
    assert np.vdot(u, rho@u).real > 1/2
    assert np.vdot(v, rho@v).real > 1/2
    # This same input has overlap >1/2 with two inequivalent nonlinear phases.
    fourier = np.array([_phase(p, 0, b) for b in range(p)]).T
    coordinates = fourier.conj().T@rho@fourier
    assert np.linalg.norm(coordinates-np.diag(np.diag(coordinates))) > 0.1


def test_quadratic_budget_has_distinct_purity_estimate_and_paid_verification_copies():
    caps = quadratic_verifier_caps(101, 8, 3, Fraction(1, 5))
    T, m = caps["candidate_count"], caps["swap_trials_per_estimate"]
    assert caps["purity_and_overlap_estimate_count"] == T+1
    assert caps["raw_copy_cap"] == 4*T+2*(T+1)*m
    assert caps["mean_estimation_absolute_error"] == caps["wrong_candidate_purity_loss_lower_bound"]/8
    assert caps["total_error_budget"] == Fraction(1, 5)
    assert not caps["known_rank_required"] and not caps["classical_only_verifier_claimed"]


def test_graph_chart_probability_matches_all_lagrangians_in_small_actual_symplectic_space():
    from theorems.ut5_matrix_phase_alignment import _basis, _rank

    p = 3
    vectors = tuple(v for v in product(range(p), repeat=4) if any(v))
    lagrangians = set()
    for v, w in product(vectors, repeat=2):
        pairing = sum(v[2+i]*w[i]-v[i]*w[2+i] for i in range(2)) % p
        if pairing == 0 and _rank((v, w), p) == 2:
            lagrangians.add(tuple(map(tuple, _basis((v, w), p))))
    graphs = sum(_rank([row[:2] for row in L], p) == 2 for L in lagrangians)
    assert len(lagrangians) == 40 and graphs == 27
    assert Fraction(graphs, len(lagrangians)) == graph_basis_probability(3, 2)
    assert graph_basis_probability(3, 30) > Fraction(1, 2)
    assert graph_basis_probability(2**127-1, 2) > Fraction(1, 2)


def test_bad_graph_chart_cannot_supply_a_verified_full_translation_basis():
    from theorems.ut5_matrix_phase_alignment import _rank
    # Computational basis L=Z^2 has no nonzero translation labels.
    labels = [(0, 0, a, b) for a, b in product(range(3), repeat=2)]
    assert _rank([v[:2] for v in labels], 3) == 0
    # Peak>1/p gives an explicit mixed computational-basis state with exact L.
    weights = [Fraction(1, 2)]+[Fraction(1, 16)]*8
    rho = np.diag(list(map(float, weights)))
    points = tuple(product(range(3), repeat=2))
    index = {x: i for i, x in enumerate(points)}
    for y in points:
        shift = np.zeros((9, 9))
        for column, x in enumerate(points):
            shift[index[tuple((a+b) % 3 for a, b in zip(x, y))], column] = 1
        loss = np.trace(rho@rho-rho@shift@rho@shift.T)
        assert (abs(loss) < 1e-12) == (y == (0, 0))


def test_stabilizer_basis_wrapper_pays_all_charts_and_reserves_sampling_precision():
    budget = stabilizer_basis_caps(101, 4, 3, Fraction(1, 5))
    assert budget["raw_copy_cap"] == budget["chart_count_cap"]*budget["single_chart"]["raw_copy_cap"]
    assert budget["all_inner_trial_error_budget"] == Fraction(1, 20)
    assert budget["total_error_upper_bound"] <= Fraction(1, 5)
    assert not budget["bad_chart_regression_law_claimed"]
    assert not budget["original_pure_state_identified"]
    assert not budget["full_basis_learner_implemented"]


def test_four_copy_measuring_can_erase_learnable_peak_weight_information():
    p, R, scales = 5, 3, (3, 4, 1, 2)
    legal = [a for a in product(range(p), repeat=4)
             if any(a) and sum(a) % p == 0 and sum(x*x for x in a) % p == 0]
    assert len(legal) == 24 and all(sorted(a) == [1, 2, 3, 4] for a in legal)
    weights = (1+Fraction(2, 3)*np.cos(2*np.pi*np.arange(p)/p))/p
    weights = np.asarray(weights, dtype=float)
    assert max(weights) == pytest.approx(1/R)
    assert min(weights) > 0
    convolved = np.zeros(p)
    for labels in product(range(p), repeat=4):
        probability = float(np.prod([weights[b] for b in labels]))
        convolved[sum(a*b for a, b in zip(scales, labels)) % p] += probability
    assert convolved == pytest.approx(np.full(p, 1/p))
    assert not np.allclose(_rho(p, 0, weights), _rho(p, 1, weights))
    # Regression samples are now uniform for EVERY scalar Hessian, despite
    # distinct original quantum inputs; original-copy verification is needed.
    for hessian in range(p):
        law = np.array([[convolved[(z-hessian*y) % p]/p for z in range(p)] for y in range(p)])
        assert law == pytest.approx(np.full((p, p), 1/p**2))


@pytest.mark.parametrize("p,R", [(3, 2), (5, 3), (11, 10)])
def test_direct_symmetric_regression_has_a_matched_classical_difference_validator(p, R):
    weights = (Fraction(1, R),)+(Fraction(R-1, R*(p-1)),)*(p-1)
    differences = tuple(sum(weights[b]*weights[(b-e) % p] for b in range(p)) for e in range(p))
    assert differences[0] >= Fraction(1, R**2)
    hessian = 2
    for y, z in product(range(p), repeat=2):
        probability = sum((differences[e]/p for Y, e in product(range(p), repeat=2)
                           if (y*(hessian*Y+e)-z*Y) % p == 0), start=Fraction(0))
        if (z-hessian*y) % p:
            assert probability == Fraction(1, p)
        else:
            assert probability-Fraction(1, p) >= Fraction(1, R**2*(R+1)**2)


@pytest.mark.parametrize("p,R,beta", [(9, 2, Fraction(1, 4)), (5, 0, Fraction(1, 4)),
                                       (5, True, Fraction(1, 4)), (5, 5, Fraction(1, 4)),
                                       (5, 2, 0.25), (5, 2, Fraction(0))])
def test_bad_public_promises_fail_closed(p, R, beta):
    with pytest.raises(ValueError):
        PeakPhasePlan(p, R, beta)


def test_cli_writes_separate_non_execution_artifact_with_live_source_hashes(tmp_path, capsys):
    import qsearch
    args = qsearch.build_parser().parse_args(["phase-copy-baseline", "--peaked-noise", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/peaked_phase_source.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert saved["selection"]["input_rank"] == 101**40
    assert saved["selection"]["retained_rank"] == 1
    for flag in ("input_rank_bound_required", "quantum_filter_executed", "quantum_learner_executed",
                 "novelty_established", "native_classical_input_reduction_established", "speedup_claim_allowed"):
        assert saved[flag] is False
    for path, digest in saved["source_sha256"].items():
        assert hashlib.sha256((Path(qsearch.__file__).resolve().parent/path).read_bytes()).hexdigest() == digest
    assert not (tmp_path/"research/reductions/exterior_phase_learning.json").exists()
    with pytest.raises(SystemExit):
        qsearch.build_parser().parse_args(["phase-copy-baseline", "--phase-noise", "--peaked-noise"])
