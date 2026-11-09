"""Tests for theorems/rees_circuit_coherent_k3.py (fifth backend: coherent labels with a
kappa_d = 3 grade, n4(F_7)).

AI-checked, pending human review. Default run is short; REES_SLOW=1 adds the per-merge
Engine state checks on a full-support instance and a seeded recovery run. The full
checks are in the CLI (report research/audits/reviews/2026-11-04-rees-circuit-coherent-k3.md)."""
import os
import random

import numpy as np
import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
from theorems import rees_circuit_coherent_k3 as K
from theorems.rees_circuit_arith import add_product_ops, add_scaled_ops
from theorems.rees_coherent_sde import Macro
from theorems.rees_coherent_sde_k2 import CoherentSDEK2
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa
from theorems.rees_end_to_end_sim import filiform4

SLOW = os.environ.get("REES_SLOW") == "1"
slow = pytest.mark.skipif(not SLOW, reason="set REES_SLOW=1")


@pytest.fixture(scope="module")
def n4f7():
    cfg = K.job_config("n4_f7")
    return cfg, {d: K.MergeBlockK(cfg, d) for d in (2, 3)}


def test_status_gates_stay_false():
    assert K.STATUS["coherent_receiver_implemented"] is False
    assert K.STATUS["general_instances"] is False
    assert K.STATUS["speedup_claim_allowed"] is False
    assert K.STATUS["review"] == "AI-checked, pending human review"


def test_config_kappa_and_arities(n4f7):
    cfg, blocks = n4f7
    assert cfg.dims == (4, 2, 1) and cfg.p == 7
    assert (K.kappa(7, 3), K.kappa(7, 2)) == (3, 2)
    assert cfg.arity == {2: 6, 3: 3}                         # (g+1)(g+2)/2 at g_2 = 2, g_3 = 1
    assert G.Config(cfg.algebra).arity == {2: 5, 3: 4}       # the generator's CW arities
    assert isinstance(blocks[3].sde, CoherentSDEKappa) and isinstance(blocks[2].sde, CoherentSDEK2)
    assert blocks[3].M == 3 and blocks[2].M == 6


def test_dispatch_restored_and_fourth_backend_still_refuses(n4f7):
    assert C.sde_circuit is K._ORIG["sde_circuit"] and C.sde_reference is K._ORIG["sde_reference"]
    with pytest.raises(ValueError):
        C.coherent_config(filiform4(7))                       # kappa_3 = 3: the fourth backend refuses
    with pytest.raises(ValueError):
        with K.kappa_dispatch():
            raise ValueError("inside")
    assert C.coherent_arity is K._ORIG["coherent_arity"]


def _key(it):
    return (it.kind, it.coeff, it.args, it.inv) if isinstance(it, Macro) else it


def test_k12_delegation_matches_fourth_backend():
    cfg = C.job_config("n4_f5")
    for d in (2, 3):
        a, b = C.MergeBlock(cfg, d), K.MergeBlockK(cfg, d)
        assert [_key(it) for it in a.prog] == [_key(it) for it in b.prog] and a.nw == b.nw


def test_sde_inside_block_all_label_triples(n4f7):
    r = K.sde_exhaustive(n4f7[1][3])
    assert r["inputs"] == 7**3
    assert all(v for v in r.values() if isinstance(v, bool)), r


def test_controlled_merge_proved_and_structure(n4f7):
    for blk in n4f7[1].values():
        f = K.prove_controlled_merge(blk)
        assert f["proved"], f
        s = K.block_structure(blk)
        assert s["sde_never_writes_labels_or_Q_or_children"] and s["child_merges_local_footprint"]
        assert s["merge_workspace_wires_outside_sde_workspace"] == 0


def test_grade3_block_all_label_triples(n4f7):
    blk = n4f7[1][3]
    L, xs, qv = K.all_labels_sampled_rest(blk, 8, seed=1)
    assert len(L) == 8*343
    assert K.block_check(blk, L, xs, qv)["passed"]


def test_blocks_structured(n4f7):
    assert K.block_sampled(n4f7[1][3], n=1024, seed=2)["passed"]
    assert K.block_sampled(n4f7[1][2], n=128, seed=3)["passed"]


@pytest.mark.parametrize("sde_mutate", [{"beta": (0, 2, 5)}, {"alpha": (1, 0, 4)}, {"omega_min": True}])
def test_kappa3_witness_mutations_detected(n4f7, sde_mutate):
    blk = K.MergeBlockK(n4f7[0], 3, sde_mutate=sde_mutate)
    assert not K.block_sampled(blk, n=512, seed=4)["passed"]


@pytest.mark.parametrize("mut", ["g_sign", "skip_ctrl_inv", "skip_sde_inv", "skip_bennett"])
def test_block_mutations_detected(n4f7, mut):
    assert not K.block_sampled(K.MergeBlockK(n4f7[0], 3, mutate=[mut]), n=256, seed=5)["passed"]


def test_gate_counts_equal_emitted_list(n4f7):
    blk = n4f7[1][3]
    assert K.prog_counts(blk.prog, blk.p)["gates"] == len(blk.flatten())


def test_terminal_sample_counts_and_structure(n4f7):
    cfg = n4f7[0]
    ts = K.TerminalSampleK(cfg)
    c = ts.counts()
    assert c["total"]["gates"] == 4832806 and c["qubits"] == 1629
    assert c["oracle_calls"] == 54 and c["total"]["qft_calls"] == 230
    assert c["sources"] == {1: 1, 2: 6, 3: 18}
    assert all(ts.structure().values())
    N = G.sources_per_grade(cfg)
    for d, blk in ts.blocks.items():
        seg = blk.segment_counts()
        assert c["by_component"][f"sde_grade{d}"]["gates"] == N[d-1]*seg["sde_U_and_Uinv"]["gates"]
        assert c["by_component"][f"bch_merge_grade{d}"]["gates"] == N[d-1]*seg["bch_merge"]["gates"]


def test_assembled_program_wiring(n4f7):
    ts = K.TerminalSampleK(n4f7[0])
    assert K.assembled_basis_paths(ts, n=16, seed=6)["passed"]


def test_state_checks_small_support_instances(n4f7):
    """Exact Engine merges with circuit witnesses on the instances whose grade-3 label
    support is a single label (fast)."""
    cfg, blocks = n4f7
    eng = G.Engine(cfg)
    wit = {d: K.CircuitWitness(blk) for d, blk in blocks.items()}
    insts = G.n4_instances(7)
    for inst in (insts[5],):                                  # gamma_2
        row = K.state_checks(cfg, inst, eng, wit, random.Random(7), grade2_tuples=3)
        assert row["passed"], row


def test_state_checks_grade3_full_label_support(n4f7):
    """insts[0] (<e2>) has all 343 grade-3 label triples; every merged output must equal
    rho_{H_{d-1}} at kappa = 3 (reduces to a few dozen distinct merges)."""
    cfg, blocks = n4f7
    eng = G.Engine(cfg)
    wit = {d: K.CircuitWitness(blk) for d, blk in blocks.items()}
    row = K.state_checks(cfg, G.n4_instances(7)[0], eng, wit, random.Random(8), grade2_tuples=3)
    g3 = row["grades"][3]
    assert g3["label_support"] == 7 and g3["tuples"] == "all" and g3["cases"] == 343, g3
    assert g3["witness_valid"] and g3["outputs_equal_rho_H"], g3
    assert row["passed"], row


def test_coset_flag_swap_mutant_detected(n4f7, monkeypatch):
    """Reversing the one-hot coset-class flags (nu=1 <-> nu=2) must be caught by both the
    sampled block check and the exhaustive SDE check."""
    class SwapFlags(CoherentSDEKappa):
        def _class_flags(self, P, y):
            return super()._class_flags(P, y)[::-1]

    monkeypatch.setattr(K, "CoherentSDEKappa", SwapFlags)
    blk = K.MergeBlockK(n4f7[0], 3)
    assert isinstance(blk.sde, SwapFlags)
    assert not K.block_sampled(blk, n=512, seed=4)["passed"]
    assert K.sde_exhaustive(blk)["equation_holds"] is False


def test_terminal_sample_emitted_gate_list_count(n4f7):
    """Stream the whole emitted TerminalSampleK gate list (not prog_counts) and count it."""
    cfg = n4f7[0]
    ts = K.TerminalSampleK(cfg)
    n = 0
    for _comp, it in ts.items:
        if isinstance(it, Macro):
            fn = add_product_ops if it.kind == "add_product" else add_scaled_ops
            n += sum(1 for _ in fn(cfg.p, *[list(r) for r in it.args], it.coeff, ts.anc))
        elif it[0] == "swapreg":
            n += len(it[1][0])
        elif it[0] in ("x", "cx", "ccx", "swap"):
            n += 1
    assert n == 4832806 == ts.counts()["total"]["gates"]


@slow
def test_state_checks_full_support_and_run(n4f7):
    cfg, blocks = n4f7
    eng = G.Engine(cfg)
    wit = {d: K.CircuitWitness(blk) for d, blk in blocks.items()}
    inst = G.n4_instances(7)[0]                               # <e2>, non-normal
    row = K.state_checks(cfg, inst, eng, wit, random.Random(8), grade2_tuples=4)
    assert row["passed"] and row["grades"][3]["tuples"] == "all" and row["grades"][3]["cases"] == 343, row
    assert K.run_coherent_witness(cfg, inst, eng, wit, seed=9, extra=1)["recovered"]
