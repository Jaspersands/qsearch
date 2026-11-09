"""Tests for theorems/rees_circuit_coherent_c4.py (coherent labels on the class-four
filiform algebra n5 over F_7: kappa = (2, 3, 2) at grades (4, 3, 2)).

AI-checked, pending human review. Default run is short; REES_SLOW=1 adds the wiring
check of a whole terminal sample (83 M gates), its mutants, a state check with a larger
support and a seeded recovery run. The full checks are in the CLI (report
research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md)."""
import copy
import os
import random

import numpy as np
import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
from theorems import rees_circuit_coherent_c4 as X
from theorems import rees_circuit_coherent_k3 as K
from theorems.rees_coherent_sde_k2 import CoherentSDEK2
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa
from theorems.rees_coherent_sde import Macro
from theorems.rees_end_to_end_sim import filiform5, rref

SLOW = os.environ.get("REES_SLOW") == "1"
slow = pytest.mark.skipif(not SLOW, reason="set REES_SLOW=1")


@pytest.fixture(scope="module")
def n5f7():
    cfg = X.config()
    return cfg, X.blocks(cfg)


@pytest.fixture(scope="module")
def ts(n5f7):
    return K.TerminalSampleK(n5f7[0])


@pytest.fixture(scope="module")
def engine(n5f7, ts):
    cfg, blocks = n5f7
    return X.SourceFromKernel(cfg, ts), {d: C.CircuitWitness(blk) for d, blk in blocks.items()}


def test_status_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_instances", "qft_synthesised",
              "whole_circuit_amplitude_simulation", "source_from_gate_list_on_all_addresses",
              "independent_review", "speedup_claim_allowed"):
        assert X.STATUS[k] is False, k
    assert X.STATUS["review"] == "AI-checked, pending human review"


def test_config_kappa_and_arities(n5f7):
    cfg, blocks = n5f7
    assert cfg.p == 7 and cfg.c == 4 and cfg.dims == (5, 3, 2, 1)
    assert [K.kappa(7, d) for d in (4, 3, 2)] == [2, 3, 2]
    assert cfg.arity == {2: 10, 3: 6, 4: 3}                    # (g+1)(g+2)/2, g = (3, 2, 1)
    assert G.Config(cfg.algebra).arity == {2: 7, 3: 7, 4: 3}   # the generator's CW arities
    assert isinstance(blocks[4].sde, CoherentSDEK2) and not isinstance(blocks[4].sde, CoherentSDEKappa)
    assert isinstance(blocks[3].sde, CoherentSDEKappa)
    assert isinstance(blocks[2].sde, CoherentSDEK2) and not isinstance(blocks[2].sde, CoherentSDEKappa)
    assert [blocks[d].M for d in (4, 3, 2)] == [3, 6, 10]


def test_dispatch_restored_and_fourth_backend_still_refuses(n5f7):
    for name, fn in K._ORIG.items():
        assert getattr(C, name) is fn
    with pytest.raises(ValueError):
        C.coherent_config(filiform5(7))                          # kappa_3 = 3


def test_controlled_merge_proved_and_structure(n5f7):
    for d, blk in n5f7[1].items():
        f = C.prove_controlled_merge(blk)
        assert f["proved"], (d, f)
        s = C.block_structure(blk)
        assert s["sde_never_writes_labels_or_Q_or_children"] and s["child_merges_local_footprint"], (d, s)
        assert s["merge_workspace_wires_outside_sde_workspace"] == 0


def test_sde_grade4_all_label_triples(n5f7):
    r = X.sde_check(n5f7[1][4], X.all_label_tuples(7, 1, 3))
    assert r["inputs"] == 343 and r["passed"], r


def test_rank_le1_tuples():
    T = X.rank_le1_tuples(7, 2, 3)
    assert len(T) == 1+8*(7**3-1)
    keys = {t.tobytes() for t in T}
    assert len(keys) == len(T)
    assert all(len(rref(list(t), 7)) <= 1 for t in T[::97])
    assert len(X.rank_le1_tuples(7, 2, 6)) == 941185
    R = X.random_rank_le1_tuples(7, 3, 10, 64, 0)
    assert all(len(rref(list(t), 7)) == 1 for t in R)


def test_sde_grade3_rank_le1_slice_and_random(n5f7):
    blk = n5f7[1][3]
    lam = np.concatenate([X.rank_le1_tuples(7, 2, 6)[::101], X.random_label_tuples(7, 2, 6, 4096, 1)])
    assert X.sde_check(blk, lam)["passed"]


def test_sde_grade2_sampled(n5f7):
    cfg, blocks = n5f7
    lam = np.concatenate([X.structured_tuples(cfg, 2, 512, 2), X.random_rank_le1_tuples(7, 3, 10, 512, 2),
                          X.random_label_tuples(7, 3, 10, 512, 2)])
    assert X.sde_check(blocks[2], lam)["passed"]


def test_grade4_block_all_label_triples(n5f7):
    blk = n5f7[1][4]
    r = X.block_check_labels(blk, X.repeat_labels(X.all_label_tuples(7, 1, 3), 8), 3)
    assert r["inputs"] == 8*343 and r["passed"], r


def test_grade3_and_grade2_blocks_sampled(n5f7):
    cfg, blocks = n5f7
    lam3 = np.concatenate([X.rank_le1_tuples(7, 2, 6)[::997], X.structured_tuples(cfg, 3, 512, 4)])
    assert X.block_check_labels(blocks[3], lam3, 4)["passed"]
    assert X.block_check_labels(blocks[2], X.structured_tuples(cfg, 2, 256, 5), 5)["passed"]


@pytest.mark.parametrize("mut", ["g_sign", "skip_ctrl_inv", "skip_sde_inv", "skip_bennett"])
def test_grade4_block_mutations_detected(n5f7, mut):
    cfg = n5f7[0]
    blk = K.MergeBlockK(cfg, 4, mutate={mut})
    assert not X.block_check_labels(blk, X.structured_tuples(cfg, 4, 256, 6), 6)["passed"]


@pytest.mark.parametrize("sde_mutate", [{"beta": (0, 2, 5)}, {"alpha": (1, 0, 4)}, {"omega_min": True}])
def test_kappa3_witness_mutations_detected(n5f7, sde_mutate):
    blk = K.MergeBlockK(n5f7[0], 3, sde_mutate=sde_mutate)
    lam = X.random_label_tuples(7, 2, 6, 512, 7)
    assert not X.sde_check(blk, lam)["passed"]
    assert not X.block_check_labels(blk, lam, 7)["passed"]


def test_all_block_mutants_rejected(n5f7):
    r = X.block_mutants(n5f7[0], n=128)
    assert r["all_rejected"], r


def test_gate_counts_equal_emitted_list(n5f7):
    blk = n5f7[1][4]
    assert C.prog_counts(blk.prog, blk.p)["gates"] == len(blk.flatten())


def test_terminal_sample_counts_and_structure(n5f7, ts):
    cfg = n5f7[0]
    c = ts.counts()
    assert c["qubits"] == 20566 and c["total"]["gates"] == 83492540
    assert c["oracle_calls"] == 720 and c["total"]["qft_calls"] == 3330
    assert c["sources"] == {1: 1, 2: 10, 3: 60, 4: 180}
    assert all(ts.structure().values())
    N = G.sources_per_grade(cfg)
    for d, blk in ts.blocks.items():
        seg = blk.segment_counts()
        assert c["by_component"][f"sde_grade{d}"]["gates"] == N[d-1]*seg["sde_U_and_Uinv"]["gates"]
        assert c["by_component"][f"bch_merge_grade{d}"]["gates"] == N[d-1]*seg["bch_merge"]["gates"]
        assert c["by_component"][f"witness_control_grade{d}"]["gates"] == N[d-1]*seg["witness_control_G"]["gates"]


def test_measured_generator_counts(n5f7):
    cfg = n5f7[0]
    cw = C.measured_counts(cfg.algebra)
    assert cw["qubits"] == 16302+14 and cw["oracle_calls"] == 588       # main.tex: 16302 (+ 3b+5 ancillas)
    eq = C.measured_counts(cfg.algebra, arities=dict(cfg.arity))
    assert eq["oracle_calls"] == 720 and eq["qft_calls"] == 3330


def _source_check(cfg, ts, insts):
    for inst in insts:
        info, S = X.source_exact_check(cfg, ts, inst, n_hom=256)
        assert info["passed"], (inst.name, info)
        assert len(S) == 7**info["kernel_dim"]


def test_source_exact_check_small_kernels(n5f7, ts):
    _source_check(n5f7[0], ts, X.instances()[:7])


@slow
def test_source_exact_check_gamma3_gamma2(n5f7, ts):
    _source_check(n5f7[0], ts, X.instances()[7:])              # |S| = 7^7, 7^9


def _mutant_m1(ts):
    """One source transform deleted: one address coordinate stays |0>."""
    m = copy.copy(ts)
    idx = [i for i, (c, _) in enumerate(ts.items) if c == "source_qft"][3]
    m.items = ts.items[:idx]+ts.items[idx+1:]
    return m


def _mutant_m2(ts):
    """a_0 += a_5 after the last uncompute of the first source."""
    m = copy.copy(ts)
    node, _ = X.first_source_items(ts)
    idx = next(i for i, (c, _) in enumerate(ts.items) if c == "instrument_qft")
    stray = ("source_evaluation", Macro("add_scaled", 1, (tuple(node["reg"][0]), tuple(node["reg"][5]))))
    m.items = ts.items[:idx]+[stray]+ts.items[idx:]
    return m


@pytest.mark.parametrize("mutant,flag", [(_mutant_m1, "source_transforms_one_qft_per_address"),
                                         (_mutant_m2, "address_register_restored")])
def test_source_check_rejects_source_mutants(n5f7, ts, mutant, flag):
    cfg = n5f7[0]
    inst = X.instances()[0]
    info, _ = X.source_exact_check(cfg, mutant(ts), inst, n_hom=16)
    assert not info["passed"] and not info[flag], info
    good, _ = X.source_exact_check(cfg, ts, inst, n_hom=16)
    assert good["passed"] and good["address_register_restored"] and good["oracle_outputs_distinct_fresh"]


def test_run_seeded_refuses_failed_source(n5f7, ts):
    cfg = n5f7[0]
    eng = X.SourceFromKernel(cfg, _mutant_m1(ts))
    r = X.run_seeded(cfg, X.instances()[0], eng, {}, seed=1)
    assert r["recovered"] is False and r["source_check_failed"]


@pytest.mark.parametrize("mut", ["g_sign", "skip_ctrl_inv", "skip_sde_inv", "skip_bennett"])
def test_grade2_block_mutations_detected(n5f7, mut):
    cfg = n5f7[0]
    blk = K.MergeBlockK(cfg, 2, mutate={mut})
    assert not X.block_check_labels(blk, X.structured_tuples(cfg, 2, 128, 6), 6)["passed"]


def test_state_checks_small_supports(n5f7, engine):
    cfg = n5f7[0]
    eng, wit = engine
    insts = X.instances()
    for i in (0, 1):                                          # trivial, <e1> (non-normal)
        row = X.state_checks(cfg, insts[i], eng, wit, random.Random(8), tuples=4)
        assert row["passed"], row
        assert row["grades"][4]["tuples"] == "all"


@slow
def test_state_checks_larger_support_and_run(n5f7, engine):
    cfg = n5f7[0]
    eng, wit = engine
    inst = X.instances()[4]                                    # Z(G)
    row = X.state_checks(cfg, inst, eng, wit, random.Random(9), tuples=8)
    assert row["passed"], row
    inst = X.instances()[2]                                    # <e2>, non-normal
    assert X.run_seeded(cfg, inst, eng, wit, seed=10, extra=1)["recovered"]


@slow
def test_assembled_program_wiring_and_mutants(n5f7, ts):
    assert K.assembled_basis_paths(ts, n=64, seed=11)["passed"]
    assert X.assembled_mutants(n5f7[0], n=64)["all_rejected"]
    r = X.basis_paths_checked(_mutant_m1(ts), n=16, seed=12)       # fails cleanly, no KeyError
    assert r["passed"] is False
    assert X.basis_paths_checked(_mutant_m2(ts), n=16, seed=12)["passed"] is False
