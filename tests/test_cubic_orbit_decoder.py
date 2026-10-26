from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
import pytest
from flint import nmod_mat

from theorems import cubic_orbit_decoder as f
from theorems import paired_residual_decoder as paired


@pytest.mark.parametrize("p,n", [(13, 12), (19, 12), (2053, 204)])
def test_domain_is_a_disjoint_cover_by_actual_cubic_orbits(p, n):
    d = f.Domain.create(p, n)
    flat = [a for o in d.orbits for a in o]
    assert sorted(flat) == list(range(1, p))
    assert pow(d.zeta, 3, p) == 1 and d.zeta != 1
    assert pow(d.eta, (p-1)//2, p) == p-1
    assert len({pow(o[0], 3, p) for o in d.orbits}) == d.M


def test_folded_rows_are_exactly_one_original_syndrome_and_unfold_without_advice():
    d = f.Domain.create(19, 12)
    labels = [[0]*3 for _ in d.orbits]
    labels[0] = [2, 5, 7]
    labels[3] = [8, 3, 9]
    rows = f.orbit_syndrome(d, labels)
    original = f.syndrome(d.p, f.scalar_errors(d, labels), d.n)
    assert all(rows[r] == original[r::3] for r in range(3))
    result = f.decode_orbits(d, 3, rows)
    assert result["status"] == "VERIFIED_UNIQUE_ORBIT_LABEL"
    assert result["labels"] == labels
    assert result["extra_quantum_copies"] == 0
    assert result["decoder"]["whole_cap_uniqueness_certified"]
    assert not result["decoder"]["source_error_or_support_supplied"]


def test_public_orbit_boundary_rejects_a_decoded_non_cube():
    d = f.Domain.create(13, 12)
    nodes = {pow(o[0], 3, 13) for o in d.orbits}
    bad_node = next(a for a in range(1, 13) if a not in nodes)
    rows = [[pow(bad_node, j, 13) for j in range(4)], [0]*4, [0]*4]
    assert f.decode_orbits(d, 2, rows)["status"] == "ABSTAIN_OUTSIDE_PUBLIC_ORBITS"


def test_zero_source_is_accepted_and_correlated_nonzero_source_can_fail():
    d = f.Domain.create(13, 12)
    assert f.decode_orbits(d, 3, [[0]*4 for _ in range(3)])["status"] == "VERIFIED_UNIQUE_ORBIT_LABEL"
    labels = [[1, 1, 1], [2, 2, 2], [0, 0, 0], [0, 0, 0]]
    rows = f.orbit_syndrome(d, labels)
    assert rows[1:] == [[0]*4, [0]*4]
    assert f.decode_orbits(d, 3, rows)["status"] == "ABSTAIN"


@pytest.mark.parametrize("allowed", [(0, 1, 2, 3, 4, 5), (1, 3, 4, 7, 9, 10)])
def test_actual_fixed_table_fourier_law_has_two_uniform_frequencies(allowed):
    p, b, eta = 13, 5, 2
    indicator, transformed = f.local_fourier(p, b, eta, allowed)
    h = (np.isin(np.arange(p), allowed).astype(float)-(p-1)/(2*p))
    h /= np.sqrt((p-1)/(2*p)*(p+1)/(2*p))
    spectrum = np.fft.fft(h)/p
    assert np.max(abs(transformed[:, :, 0])) < 1e-14
    for v in range(1, p):
        assert np.max(abs(abs(transformed[:, :, v])**2-abs(spectrum[v])**2/p**2)) < 1e-14
    assert abs(np.sum(abs(transformed)**2)-1) < 1e-13
    assert int(indicator.sum()) == p*p*len(allowed)


def test_general_rank_count_reduces_exactly_to_paired_bound():
    for p, n in ((13, 10), (19, 16), (2053, 204)):
        for D in range(1, min(10, (n-2)//3+1)):
            a = f.rank_failure_bound(p, 2, n, D, D+1)
            assert Q(a["failure_upper_exact"]) == paired.failure_bound(p, n, D, D+1)


def test_source_preparation_retains_relative_gauss_phase_and_erases_subset_flag():
    control = f.source_phase_control()
    assert control["complex_amplitude_max_error"] < 1e-14
    assert control["local_isometry_gram_error"] < 1e-14
    assert abs(control["omitting_anisotropic_Gauss_sign_state_distance"]-2) < 1e-14
    assert control["empty_plus_active_overlap_if_sign_omitted"] < 1e-14
    assert control["active_has_zero_last_frequency_mass"] == 0
    assert control["subset_flag_is_recoverable_from_nonzero_last_frequency"]
    assert not control["local_postselection_needed"]


def test_saturated_random_columns_are_counted_not_treated_as_independent_rows():
    bound = f.rank_failure_bound(13, 3, 12, 2, 3)
    term = bound["terms"][-1]
    assert term["random_column_rank"] == 3
    assert term["admissible_nullvector_dimension"] == 2
    assert Q(term["term_exact"]) == Q(14, 13**3)
    assert not bound["folded_rows_assumed_independent_uniform"]
    control = f.rank_control()
    for row in control["rows"][:2]:
        assert row["failed"] == 13*12
        assert Q(row["actual_failure_exact"]) <= Q(bound["failure_upper_exact"])
    assert control["rows"][-1]["failed"] == 3*13**2-2*13
    assert Q(control["rows"][-1]["actual_failure_exact"]) > Q(bound["failure_upper_exact"])


def test_cap_factor_columns_match_recurrence_rank_on_every_small_uniform_draw():
    d = f.Domain.create(13, 12)
    for u, v in product(range(13), repeat=2):
        supported = [[u, v, 1], [3, 4, 2]]
        columns = f.cap_columns(d, 3, (0, 1), supported)
        labels = supported+[[0]*3, [0]*3]
        rows = f.orbit_syndrome(d, labels)
        recurrence = [[row[j+k] for k in range(3)] for row in rows for j in range(1)]
        assert nmod_mat(columns, 13).rank() == nmod_mat(recurrence, 13).rank()


def test_anisotropic_norm_precludes_local_lines_but_local_norm_inversion_is_easy():
    result = f.norm_control()
    assert result["norm_preimage_counts"] == [1]+[8]*6
    p, eta = 7, 3
    allowed = {0, 1, 2}
    for dx, dy, dz in product(range(p), repeat=3):
        if (dx, dy, dz) == (0, 0, 0):
            continue
        for x, y, z in ((0, 0, 0), (1, 3, 2), (4, 6, 5)):
            values = {(z+t*dz+(x+t*dx)**2-eta*(y+t*dy)**2) % p for t in range(p)}
            assert len(values) in ((p+1)//2, p)
            assert not values <= allowed
    assert result["split_form_counterexample"]["residual_along_line"] == [0]*p


def test_guard_is_necessary_even_when_norm_and_source_support_are_correct():
    result = f.observable_control()
    p = result["p"]
    for power in range(result["n"]):
        assert sum(v*pow(a, power, p) for a, v in
                   zip(result["kernel_points"], result["kernel_values"])) % p == 0
    assert abs(result["source_norm"]-1) < 1e-14
    assert abs(result["target_norm"]-1) < 1e-14
    assert result["unsafe_mean_error"] > 1e-7
    assert result["accepted_labels"] == [False, False, True]
    assert abs(result["retained_mass"]-0.5) < 1e-14
    assert result["guarded_mean_error"] < 1e-14
    assert result["native_failure_probability_bound_does_not_apply_to_this_control"]


def test_generic_polynomial_norm_factorization_is_not_orbit_covariance():
    control = f.norm_compatibility_control()
    assert control["all_degree_below_two_orbit_norm_preimages"] == []
    assert all(control["degree_d_leading_factors_mod_three"])
    assert not control["paired_or_triple_optimization_infeasibility_claimed"]
    assert control["exact_coefficient_inverse"]["status"] == "NO_POLYNOMIAL_SQUARE_ROOT"
    d = f.Domain.create(13, 12)
    for degree in range(1, 10):
        c = [3]+[0]*(degree-1)+[5]
        norm = f.orbit_norm(d, c)
        assert norm.degree() == 2*degree


def test_orbit_norm_inverse_is_just_coefficient_rescaling_and_a_square_root():
    d = f.Domain.create(13, 12)
    for c in product(range(13), repeat=2):
        norm = f.orbit_norm(d, c)
        values = [int(norm[j]) for j in range(max(1, norm.degree()+1))]
        result = f.recover_orbit_norm(d, values)
        assert result["status"] == "VERIFIED_ORBIT_NORM_ROOT"
        root = f.ring(13)(result["coefficients"])
        P = f.ring(13)(list(c))
        assert root in (P, -P)
        assert not result["optimization_of_halfset_score_solved"]
    for j in range(9):
        monomial = [0]*j+[1]
        norm = f.orbit_norm(d, monomial)
        assert norm[2*j] == (1-d.eta*pow(d.zeta, 2*j, 13)) % 13
    assert f.recover_orbit_norm(d, [0])["coefficients"] == [0]


def test_cubic_information_manifold_and_intrinsic_greedy_search():
    d = f.Domain.create(19, 12)
    multipliers = (1, 2, 3, 4, 5, 6)
    allowed = tuple(tuple((i+j*j) % 19 for j in range(1, 10)) for i in range(6))
    I = (0, 2, 3, 5)
    c = f.sample_cubic_information_witness(d, multipliers, allowed, I, 41)
    x, y, w = f.cubic_orbit_values(d, c)
    C = f.cubic_information_map(d, I)
    assert np.array_equal((C[0]@x[list(I)] + C[2]@y[list(I)] + C[1]@w[list(I)]) % 19, x)
    assert np.array_equal((C[1]@x[list(I)] + C[0]@y[list(I)] + C[2]@w[list(I)]) % 19, y)
    assert np.array_equal((C[2]@x[list(I)] + C[1]@y[list(I)] + C[0]@w[list(I)]) % 19, w)
    assert f.coefficients_from_cubic_information(d, I, x, y, w) == c

    res = f.cubic_intrinsic_greedy_search(d, multipliers, allowed, c, positions=I, max_sweeps=2, batch=8)
    assert res["final_score"] >= res["initial_score"]
    assert res["final_score"] == f.independent_cubic_score(d, multipliers, allowed, res["coefficients"])
    assert res["original_Horner_and_full_three_point_replay"]


def test_native_certificate_keeps_guard_failure_and_classical_blockers():
    result = f.score_certificate()
    assert result["guard_cap"] == result["degree"]+1
    assert result["rank"]["cap_equations"] >= result["degree"]
    assert 0 < Q(result["rank"]["failure_upper_exact"]) < Q(1, 10**6)
    assert Q(result["one_attempt_mean_lower_ABORT_score_zero"]) < Q(result["conditional_mean_lower_exact"])
    assert result["degree"] > result["ordinary_scalar_guarantee_degree"]
    assert Q(result["one_attempt_tail_lower_exact"]) > 0
    assert not result["classical_separation_or_novelty_claimed"]
    assert not result["compiled_circuit"]


@pytest.mark.parametrize("args", [(7, 6, None), (13, 11, None), (13, 12, 3), (13, 15, None)])
def test_invalid_domain_fails_closed(args):
    p, n, M = args
    if args == (7, 6, None):
        with pytest.raises(ValueError):
            f.decode_orbits(f.Domain.create(p, n, M), 2, [[0]*2 for _ in range(3)])
    else:
        with pytest.raises(ValueError):
            f.Domain.create(p, n, M)


def test_invalid_rank_and_fourier_premises_fail_closed():
    for args in ((13, 3, 12, 4, 3), (13, 3, 15, 1, 2), (13, 5, 10, 1, 1)):
        with pytest.raises(ValueError):
            f.rank_failure_bound(*args)
    with pytest.raises(ValueError):
        f.local_fourier(13, 1, 1, tuple(range(6)))


def test_saved_native_basis_witness_and_classical_portfolio():
    if not f.REPORT.exists():
        pytest.skip("native producer not yet run")
    report = json.loads(f.REPORT.read_text())
    assert report["schema"] == "cubic-orbit-decoder-v2"
    native = report["native"]
    assert native["decoder"]["status"] == "VERIFIED_UNIQUE_ORBIT_LABEL"
    assert native["decoder"]["labels"] == native["source_labels"]
    assert native["actual_scalar_weight"] > 102
    assert native["ordinary_scalar_decoder_status"] != "VERIFIED_UNIQUE_BURST"
    assert native["valid_pilot_but_correlated_frequency_countercontrol"]["status"] == "ABSTAIN"
    inverse = native["planted_polynomial_norm_round_trip"]
    assert inverse["inverse"]["status"] == "VERIFIED_ORBIT_NORM_ROOT"
    assert not inverse["optimization_search_or_high_score_witness"]
    portfolio = native["classical_intrinsic_portfolio"]
    assert portfolio["initial_information_set_score"] == 387
    assert portfolio["best_score"] >= 435
    assert portfolio["original_Horner_and_full_three_point_replay"]
    assert not portfolio["full_classical_portfolio_complete"]
    assert native["strong_classical_portfolio_NOT_run"]
    assert not report["accepted_speedup_candidate"]
