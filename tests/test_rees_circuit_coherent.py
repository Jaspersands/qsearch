"""Tests for theorems/rees_circuit_coherent.py (coherent-label receiver backend).

AI-checked, pending human review. Default run < 90 s. The full Heis(F_3)
block exhaustion (3^18 joint inputs) and the larger runs are in the CLI
(report research/audits/reviews/2026-11-04-rees-circuit-coherent.md)."""
import random
from itertools import product

import numpy as np
import pytest

import theorems.rees_circuit_general as G
from theorems.rees_circuit_coherent import (
    STATUS, CircuitWitness, MergeBlock, TerminalSample, assembled_basis_paths, block_check, block_child_tables, block_exhaustive,
    block_input_count, block_sampled, block_structure, coherent_config, counts_report, flatten, heis_compare,
    heis_end_to_end, heis_measured_reference, job_config, n4_state_checks, prog_counts, prove_controlled_merge,
    run_coherent_witness, sde_exhaustive)
from theorems.rees_end_to_end_sim import filiform4


@pytest.fixture(scope="module")
def heis():
    cfg = job_config("heis_f3")
    blk = MergeBlock(cfg, 2)
    return cfg, blk, blk.flatten()


@pytest.fixture(scope="module")
def n4():
    cfg = job_config("n4_f5")
    return cfg, {d: MergeBlock(cfg, d) for d in (2, 3)}


def test_status_gates_stay_false():
    assert STATUS["coherent_receiver_implemented"] is False
    assert STATUS["kappa_ge3_grades_coherent"] is False
    assert STATUS["speedup_claim_allowed"] is False


def test_arities_and_kappa_refusal():
    assert job_config("heis_f3").arity == {2: 3}
    assert job_config("n4_f5").arity == {2: 6, 3: 2}          # triangular 6 instead of CW 5
    with pytest.raises(ValueError):
        coherent_config(filiform4(7))                          # kappa_3 = 3 at p = 7


def test_sde_inside_block_exhaustive(heis, n4):
    for blk in (heis[1], n4[1][3]):
        r = sde_exhaustive(blk)
        assert all(v for k, v in r.items() if isinstance(v, bool)), r


def test_controlled_merge_proved_and_structure(heis, n4):
    for blk in (heis[1], n4[1][2], n4[1][3]):
        f = prove_controlled_merge(blk)
        assert f["proved"], f
        s = block_structure(blk)
        assert s["sde_never_writes_labels_or_Q_or_children"] and s["child_merges_local_footprint"]


def test_block_sampled_all_wires(heis, n4):
    cfg, blk, gates = heis
    assert block_sampled(blk, n=4096, seed=1, gates=gates)["passed"]
    assert block_sampled(n4[1][3], n=1024, seed=2)["passed"]
    assert block_sampled(n4[1][2], n=192, seed=3)["passed"]


def test_heis_block_exhaustive_slices(heis):
    cfg, blk, gates = heis
    total = block_input_count(blk)
    assert total == 3**18
    rng = random.Random(7)
    for start in (0, rng.randrange(total-(1 << 16)), total-(1 << 16)):
        assert block_exhaustive(blk, chunk=1 << 16, start=start, stop=start+(1 << 16))["passed"]


@pytest.mark.parametrize("mut", ["g_sign", "skip_ctrl_inv", "skip_sde_inv", "skip_bennett"])
def test_block_mutations_detected(heis, mut):
    cfg = heis[0]
    assert not block_sampled(MergeBlock(cfg, 2, mutate=[mut]), n=256, seed=4)["passed"]


def test_gate_counts_equal_emitted_lists(heis, n4):
    for blk in (heis[1], n4[1][3]):
        assert prog_counts(blk.prog, blk.p)["gates"] == len(blk.flatten())


def test_heis_end_to_end_all_subgroups(heis):
    cfg, blk, gates = heis
    eng = G.Engine(cfg)
    lam = list(product(product(range(3), repeat=1), repeat=3))
    tables, clean = block_child_tables(blk, lam, gates)
    assert clean
    insts = G.heis3_instances()
    assert len(insts) == 19
    for inst in insts:
        r = heis_end_to_end(cfg, inst, blk, tables=tables)
        assert r["source_ok"] and r["instrument_ok"]
        c = heis_compare(cfg, inst, r)
        assert all(c.values()), (inst.name, c)
        assert heis_measured_reference(cfg, inst, eng)["measured_mixture_equals_rho_H1"]


def test_heis_end_to_end_detects_wrong_block(heis):
    cfg, blk, gates = heis
    lam = list(product(product(range(3), repeat=1), repeat=3))
    tables, _ = block_child_tables(blk, lam, gates)
    swapped = tables.copy()
    swapped[:, 0] = tables[:, 1]                     # child 1 translated with child 2's witness
    fails = 0
    for inst in G.heis3_instances():
        c = heis_compare(cfg, inst, heis_end_to_end(cfg, inst, blk, tables=swapped))
        fails += not c["rho_Q_equals_rho_H1"]
    assert fails >= 10


def test_n4_state_checks_and_run(n4):
    cfg, blocks = n4
    eng = G.Engine(cfg)
    wit = {d: CircuitWitness(blocks[d]) for d in (2, 3)}
    rng = random.Random(5)
    insts = G.n4_instances(5)
    for inst in (insts[0], insts[3]):
        row = n4_state_checks(cfg, inst, eng, wit, rng, grade2_tuples=3)
        assert row["passed"], row
    assert run_coherent_witness(cfg, insts[0], eng, wit, seed=11, extra=1)["recovered"]


def test_counts_and_structure():
    for job, gates, qubits, oracle in (("heis_f3", 115282, 182, 6), ("n4_f5", 2694596, 1198, 36)):
        r = counts_report(job)
        ts = r["terminal_sample"]
        assert ts["total"]["gates"] == gates and ts["qubits"] == qubits and ts["oracle_calls"] == oracle
        assert all(r["structure"].values())
        # the non-SDE, non-control part has the measured generator's macro sequence
        by = ts["by_component"]
        meas = r.get("measured_generator_coherent_arity", r["measured_generator_cw_arity"])
        for kind in ("add_product", "add_scaled"):
            ours = sum(v.get(kind, 0) for k, v in by.items()
                       if k.startswith(("bch_merge", "source_evaluation", "instrument")))
            assert ours == meas["macros"][kind]
        assert ts["total"]["qft_calls"] == meas["qft_calls"]
        # per-component totals equal block segments times the number of merges
        cfg = job_config(job)
        N = G.sources_per_grade(cfg)
        for d, b in r["blocks"].items():
            n_merges = N[int(d)-1]
            assert by[f"sde_grade{d}"]["gates"] == n_merges*b["segments"]["sde_U_and_Uinv"]["gates"]
            assert by[f"bch_merge_grade{d}"]["gates"] == n_merges*b["segments"]["bch_merge"]["gates"]


def test_assembled_program_wiring():
    """The assembled terminal-sample program on random basis paths against an
    independent classical recursion; a sign mutant of the witness control fails."""
    ts = TerminalSample(job_config("heis_f3"))
    assert assembled_basis_paths(ts, n=2048, seed=1)["passed"]
    ts.items = [(c, it.__class__(it.kind, (-it.coeff) % 3, it.args, it.inv)
                 if c.startswith("witness_control") and hasattr(it, "kind") and it.args[1] != it.args[2] else it)
                for c, it in ts.items]
    assert not assembled_basis_paths(ts, n=256, seed=2)["passed"]
    assert assembled_basis_paths(TerminalSample(job_config("n4_f5")), n=32, seed=3)["passed"]
