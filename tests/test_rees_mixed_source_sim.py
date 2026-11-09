"""Mixed spectral source (rem:mixed-source) substituted into the exact Rees core.

Finite falsifiers on Heis(F_3), Heis(F_5) and n4(F_5). The spectrum is
supplied as reference access; part (ii)'s instruments are not simulated.
Set REES_MIXED_SLOW=1 to also run every n4(F_5) case (several minutes).
"""
import os

import numpy as np
import pytest

from theorems.rees_end_to_end_sim import filiform4, heisenberg
from theorems.rees_mixed_source_sim import (
    DESIGNS, analyse_case, check_design, circuit_check,
    finite_ell_dense, flag_overlap, flags_for_offset, lift_source, lifted_exact_state,
    make_grid, n4_subgroups, negative_controls, positive_cases, report, run_rees,
    SourceExactBackend, stage_outputs_correct, wedge_identity_check, _left_mult_table,
    _no_oracle,
)

SLOW = os.environ.get("REES_MIXED_SLOW") == "1"


def _heis(p):
    from theorems.rees_mixed_source_sim import heis_subgroups
    return positive_cases(heisenberg(p), heis_subgroups())


HEIS3 = _heis(3)
HEIS5 = _heis(5)


def _ids(group):
    return [c.name for c, _ in group[2]]


def test_designs_have_zero_moments_and_c_distinct_points():
    for (p, c), S in DESIGNS.items():
        assert check_design(S, p, c)
    assert not check_design((1, 2), 3, 2)          # the c-point lift is not a design
    assert not check_design((1, 2, 3), 5, 3)


def test_wedge_determinant_identity_and_explicit_controlled_circuit():
    assert wedge_identity_check() < 1e-12
    err, homomorphism = circuit_check()
    assert err < 1e-12 and homomorphism


def test_instances_cover_nonnormal_and_nonflat_and_offset_dependent_flags():
    for group in (HEIS3, HEIS5):
        cases = group[2]
        flags = [c.state.inst.flags() for c, _ in cases]
        assert sum(not f["normal"] for f in flags) >= 9
        assert all(len(set(c.state.weights)) > 1 for c, _ in cases)        # nonflat
        assert any("profile D" in c.name for c, _ in cases)
        assert any("profile C" in c.name for c, _ in cases)


@pytest.mark.parametrize("index", range(len(HEIS3[2])), ids=_ids(HEIS3))
def test_heis3_source_and_end_to_end(index):
    cover, lmul, cases = HEIS3
    case, gap = cases[index]
    res = analyse_case(cover, case, lmul, DESIGNS[(3, 2)], gap=gap, seed=1)
    _assert_positive(res)


@pytest.mark.parametrize("index", range(len(HEIS5[2])), ids=_ids(HEIS5))
def test_heis5_source_and_end_to_end(index):
    cover, lmul, cases = HEIS5
    case, gap = cases[index]
    res = analyse_case(cover, case, lmul, DESIGNS[(5, 2)], gap=gap, seed=1)
    _assert_positive(res)


def _assert_positive(res):
    assert res["promise_true"]
    assert res["all_offsets_identities"]               # 0 <= B <= rho, Tr(rho-B) < delta/8, K, sum r_l
    assert res["bad_margin_within_rbar"]
    assert res["all_offsets_ray_stabilizer_H"]         # exact, every offset
    assert res["all_offsets_phase_det_character"]
    assert res["all_offsets_gap"]                      # |phi| <= 1 - delta^2/8 off H (float)
    assert res["source_correct"]
    assert res["end_to_end_ok"]
    for run in res["runs"]:
        assert not run["theory_predicts_phase_failure"]
        assert run["max_off_coset_modulus"] < 1


def test_profile_c_has_two_flag_sets_and_both_offsets_recover():
    cover, lmul, cases = HEIS5
    case, gap = next(c for c in cases if "non-normal profile C" in c[0].name)
    res = analyse_case(cover, case, lmul, DESIGNS[(5, 2)], gap=gap, seed=1)
    assert res["distinct_flag_sets"] == 2 and len(res["runs"]) == 2
    assert sorted(len(r["flag_ranks"]) for r in res["runs"]) == [2, 3]
    assert res["end_to_end_ok"]


def _n4():
    alg = filiform4(5)
    subs = n4_subgroups() if SLOW else [s for s in n4_subgroups() if s[0] == "<e2> non-normal"]
    return positive_cases(alg, subs)


N4 = _n4()


@pytest.mark.parametrize("index", range(len(N4[2])), ids=_ids(N4))
def test_n4_source_and_end_to_end(index):
    cover, lmul, cases = N4
    case, gap = cases[index]
    if not SLOW and "profile D" not in case.name and "profile C" not in case.name:
        pytest.skip("set REES_MIXED_SLOW=1 for every n4(F_5) case")
    res = analyse_case(cover, case, lmul, DESIGNS[(5, 3)], gap=gap, seed=1)
    _assert_positive(res)


def test_finite_ell_dense_source_converges_and_core_recovers():
    cover, lmul, cases = HEIS3
    case, _ = next(c for c in cases if "<x> non-normal profile D" in c[0].name)
    out = finite_ell_dense(cover, case, lmul, DESIGNS[(3, 2)], (1, 4, 16))
    tds = [r["td_sigma_rho_Htilde"] for r in out["rows"]]
    assert tds[0] > 0.05                         # ell = 1 is genuinely not the coset state
    assert tds[0] > tds[1] > tds[2] and tds[2] < 1e-10
    for r in out["rows"]:
        assert r["td_within_bound"] and r["top_label_tv_within_td"]
        assert r["recovered_equals_log_H"]


CONTROLS = negative_controls()


def test_negative_controls_match_predictions():
    kinds = {c["control"] for c in CONTROLS}
    assert kinds == {"whole_support_wedge", "overstated_delta", "true_delta_same_state",
                     "no_design_c_point_lift", "mixed_offsets"}
    assert all(c["matches_prediction"] for c in CONTROLS)


def test_wrong_sources_fail_and_recover_a_larger_subgroup():
    for c in CONTROLS:
        if c["control"] in ("whole_support_wedge", "overstated_delta"):
            assert not c["promise_true"] or c["control"] == "whole_support_wedge"
            assert c["failure_detected"]
            assert not c["ray_stabilizer_H_every_offset"]
            wrong = [r for r in c["runs"] if not r["unit_set_equals_exp_hlift"]]
            assert wrong and all(not r["recovered_equals_log_H"] for r in wrong)
            # it recovers log <x, z>, the support stabilizer, instead of log <x>
            assert all(r["recovered_basis"] == [[1, 0, 0], [0, 0, 1]] for r in wrong)
        if c["control"] == "true_delta_same_state":
            assert not c["failure_detected"]
        if c["control"] == "mixed_offsets":
            assert c["failure_detected"] and all(c["single_offset_phases_cancel"])


def test_no_design_fails_exactly_where_the_moment_formula_says():
    rows = [c for c in CONTROLS if c["control"] == "no_design_c_point_lift"]
    assert any(c["failure_detected"] for c in rows)
    # Heis(F_3), H = <x>: points (1, 2) have sum 0 and h meets gamma_2 trivially
    assert any(not c["failure_detected"] and "Heis(F_3) H=<x>" in c["case"] for c in rows)
    for c in rows:
        assert c["failure_detected"] == (not c["expect_ok"])
        for r in c["runs"]:
            assert r["unit_set_equals_exp_hlift"]      # the support is right; the phase is not


def _tampered_runs(hname, coord):
    from theorems.rees_end_to_end_sim import grade_run
    cover, lmul, cases = HEIS5
    case, _ = next(c for c in cases if f"H={hname} profile B" in c[0].name)
    st, inst = case.state, case.state.inst
    grid = make_grid(case.delta_promise, case.rbar)
    distinct, _ = flags_for_offset(st, grid, 0)
    ov = flag_overlap(inst, [[st.atoms[i] for i in sorted(q)] for q in distinct], lmul)
    lifted = lift_source(cover, inst, ov, DESIGNS[(5, 2)])
    good = lifted_exact_state(cover, lifted)
    E = cover.stage_group(cover.c).elements()
    lifted.phase = np.where(lifted.unit, E[:, coord] % 5, -1)     # a character of H~
    bad = lifted_exact_state(cover, lifted)
    out = []
    for state in (good, bad):
        backend = SourceExactBackend(cover, state)
        h, rec = run_rees(cover, _no_oracle, backend, seed=3, keep_states=True)
        g = grade_run(cover, inst, h, rec, backend)
        out.append((stage_outputs_correct(cover, inst, rec), g["recovered_equals_log_H"],
                    all(x["every_source_law_uniform_on_K_perp"] for x in g["stages"].values())))
    return out


def test_tampered_grade_one_phase_breaks_stage_outputs():
    """Mutation: a character on the grade-one part of H~ (H = <x>) survives the
    descent and must make the stage outputs wrong."""
    good, bad = _tampered_runs("<x> non-normal", 0)
    assert good == (True, True, True)
    assert not bad[0]


def test_tampered_top_center_phase_is_caught_only_by_the_label_law():
    """A character supported on the top central grade (H = Z(G)) is measured out
    by the first central instrument: stage outputs stay correct, but the label
    law is no longer uniform on K^perp. Recovery alone would not catch it."""
    good, bad = _tampered_runs("Z(G)", -1)
    assert good == (True, True, True)
    assert bad[0] and not bad[2]


def test_report_flags_stay_false():
    res = report(include_n4=False, n4_runs=False) if SLOW else None
    if res is not None:
        assert res["all_end_to_end_ok"] and res["negative_controls_match_prediction"]
        assert res["spectrum_supplied_as_reference"] is True
        assert res["part_ii_instruments_simulated"] is False
        assert res["coherent_receiver_implemented"] is False
    from theorems import rees_mixed_source_sim as mod
    assert "does NOT do" in mod.__doc__ and "REFERENCE" in mod.__doc__
