"""Tests for theorems/rees_circuit_full.py (explicit QFT + coherent labels: one
gate-level circuit per terminal sample, Heis(F_3) and n4(F_5)).

AI-checked, pending human review. Default run < 90 s; the full float runs are
in the CLI (report research/audits/reviews/2026-11-04-rees-circuit-full.md)."""
import json
import math
from pathlib import Path

import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
import theorems.rees_qft_mod as Q
import theorems.rees_circuit_full as F

ROOT = Path(__file__).resolve().parents[1]
HEIS_T, N4_T = (26, 19, 15), (32, 22, 18)


@pytest.fixture(scope="module")
def heis():
    cfg = F.config("heis_f3")
    return cfg, F.FullTerminalSample(cfg, HEIS_T)


@pytest.fixture(scope="module")
def n4():
    cfg = F.config("n4_f5")
    return cfg, F.FullTerminalSample(cfg, N4_T)


def test_status_and_claim_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_instances", "kappa_ge3_grades_coherent",
              "independent_review", "speedup_claim_allowed", "monolithic_simulation", "fixed_finite_gate_set"):
        assert F.STATUS[k] is False
    assert C.STATUS["coherent_receiver_implemented"] is False
    assert Q.STATUS["rees_generator_uses_this_qft"] is False
    red = json.loads((ROOT/"research/reductions/rees_hsp_reduction.json").read_text())
    assert red["coherent_receiver_implemented"] is False


def test_targets_and_budgets(heis, n4):
    for (cfg, fts), eta, prm in ((heis, 1.5e-3, HEIS_T), (n4, 2.5e-4, N4_T)):
        cs = fts.call_summary()
        tg = F.target_params(cfg.p, cs["zero_input_forward"], cs["general"], F.n_samples(cfg))
        assert tg["eta"] == eta and tuple(tg["params"]) == prm and tg["P_lemma"] < 0.1
        hb = F.hybrid_budget(fts.calls, cfg.p, *prm, eta=eta)
        assert F.n_samples(cfg)*hb["lemma"] < 0.1 and hb["exact_formula"] < hb["lemma"]
        assert hb["B_simple"] <= eta and 3*math.pi*2.0**-prm[2] <= eta/(cfg.enc.nb+3)
    assert heis[1].call_summary()["zero_input_forward"] == 18 and heis[1].call_summary()["general"] == 6
    assert n4[1].call_summary()["zero_input_forward"] == 148 and n4[1].call_summary()["general"] == 28
    for _, fts in (heis, n4):
        assert fts.call_summary()["zero_input_inverse"] == 0


def test_heis_counts_and_gate_set(heis):
    cfg, fts = heis
    gs = F.gate_set_check(fts)
    assert gs["passed"], gs
    assert gs["total"]["gates"] == 304234 == 115282+24*7873
    assert fts.nw == 182 and fts.npool == 61 and set(fts.pool) <= set(fts.ts.pool)
    assert gs["total"]["qft_calls"] == 24 and gs["total"]["oracle_items"] == 6 and gs["total"]["measure_items"] == 1
    assert gs["max_rotation_index"] == 19
    assert set(k for k in gs["total"] if k in F.GATE_SET) == set(F.GATE_SET)


def test_n4_counts_and_gate_set(n4):
    cfg, fts = n4
    gs = F.gate_set_check(fts)
    assert gs["passed"], {k: v for k, v in gs.items() if k != "by_component"}
    assert gs["total"]["gates"] == 5035924 == 2694596+176*13303
    assert fts.nw == 1198 and fts.npool == 77
    assert gs["total"]["oracle_items"] == 36 and gs["max_rotation_index"] == 22


def test_slices_equal_lemma_and_wires(heis, n4):
    for cfg, fts in (heis, n4):
        sc = F.slice_check(fts)
        assert sc["passed"] and sc["slices"] == len(fts.calls), sc
        wc = F.wire_check(fts)
        assert wc["passed"], wc


def test_basis_paths(heis, n4):
    r = F.basis_paths(heis[1], n=1024, seed=20261104)
    assert r["passed"] and r["calls_checked"] == 24, r
    r = F.basis_paths(n4[1], n=128, seed=20261104)
    assert r["passed"] and r["calls_checked"] == 176, r


def test_mutants_rejected(heis):
    cfg, _ = heis
    for lay in ("mutant_labels", "mutant_oracle", "mutant_qudit"):
        fm = F.FullTerminalSample(cfg, HEIS_T, layout=lay)
        assert not F.wire_check(fm)["passed"]
        bp = F.basis_paths(fm, n=256, seed=1)
        assert not bp["pool_and_ancillas_zero_before_every_call"]
    sc = F.slice_check(F.FullTerminalSample(cfg, HEIS_T, mutate={"rotation"}))
    assert not sc["equal_to_lemma"]
    sc = F.slice_check(F.FullTerminalSample(cfg, HEIS_T, mutate={"footprint"}))
    assert not sc["footprint_ok"]


def test_separate_layout_counts(heis):
    cfg, _ = heis
    fs = F.FullTerminalSample(cfg, HEIS_T, layout="separate")
    assert fs.nw == 182+61 and not (set(fs.pool) & set(fs.ts.pool))
    assert F.slice_check(fs)["passed"] and F.wire_check(fs)["passed"]
    assert F.basis_paths(fs, n=256, seed=2)["passed"]


def test_per_call_float(heis):
    cfg, _ = heis
    fts = F.FullTerminalSample(cfg, (7, 7, 28))
    zero = next(i for i, c in enumerate(fts.calls) if c["component"] == "q_prep_qft")
    gen = next(i for i, c in enumerate(fts.calls) if c["kind"] == "qft_dg")
    for ci in (zero, gen):
        r = F.call_error(fts, ci)
        assert r["sigma_upper"] <= r["B"]
        assert 0.3*r["B"] <= r["sigma_max"]               # the bound is not vacuous here
    r = F.call_error(fts, zero)
    assert abs(r["column_errors"][0]-r["prep"]) < 1e-12


def test_heis_source_segment_float():
    cfg = F.config("heis_f3")
    fts = F.FullTerminalSample(cfg, (7, 7, 28))
    i0, i1 = F.first_source_segment(fts)
    r = F.segment_compare(fts, i0, i1, inst=G.heis3_instances()[1], tol=1e-10)
    hb = r["hybrid"]
    assert hb["zero_input_forward"] == 5 and hb["general"] == 1
    assert r["state_distance"] <= hb["exact_formula"]+r["prune_err_explicit"]
    assert r["state_distance"] > 0.05                         # the general call's error is visible
    assert r["exact_run_mass_on_pool_or_ancillas"] == 0.0


def test_heis_merge_segment_float_and_mutant():
    cfg = F.config("heis_f3")
    fts = F.FullTerminalSample(cfg, (7, 7, 28))
    i0, i1 = F.merge_segment(fts, 0)
    init = F.merge_inputs(fts, 0, 4, seed=1)
    r = F.segment_compare(fts, i0, i1, init=init, tol=1e-9)
    assert r["hybrid"]["zero_input_forward"] == 3 and r["hybrid"]["general"] == 0
    assert r["state_distance"] <= r["hybrid"]["exact_formula"]+r["prune_err_explicit"]
    assert r["exact_run_mass_on_pool_or_ancillas"] == 0.0 and abs(r["norm_explicit"]-1) < 1e-6
    fm = F.FullTerminalSample(cfg, (7, 7, 28), layout="mutant_labels")
    rm = F.segment_compare(fm, i0, i0+1, init=init, tol=1e-9)
    assert rm["state_distance"] > 100*(rm["hybrid"]["exact_formula"]+rm["prune_err_explicit"])
