"""Tests for the round-2 additions (2026-11-05): the exact level-0 output law of
the assembled Heis(F_3) terminal sample by the hub decomposition, its
checkpoints against module-level reference states, the power-class SDE solver
and the class-five seeded runs. AI-checked, pending human review. Report:
research/audits/reviews/2026-11-05-rees-receiver-round2.md (full runs in the
folder of the same name). Default run well under 2 minutes."""
import copy
import random
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_mono as M
from theorems.rees_circuit_exhaustive import (
    STATUS as EX_STATUS, Config, SparseEngine, family, power_class_sde, run_algorithm_sparse_pc, truth_state)
from theorems.rees_circuit_general import all_witnesses
from theorems.rees_circuit_sparse import n5_instances

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def heis():
    cfg, insts = M.job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    return cfg, {i.name.split("H=")[1]: i for i in insts}, ts, steps


def test_status_gates_stay_false():
    assert M.STATUS["coherent_receiver_implemented"] is False
    assert EX_STATUS["coherent_receiver_implemented"] is False


# ---------------------------------------------------------------- HubState against a dense statevector

def _dense(n, prog):
    psi = np.zeros(2**n, dtype=complex)
    psi[0] = 1
    idx = np.arange(2**n)
    for kind, g, q in prog:
        bit = lambda w: (idx >> w) & 1
        if kind == "h":
            w = q[0]
            out = np.zeros_like(psi)
            lo, hi = idx & ~(1 << w), idx | (1 << w)
            b = bit(w)
            np.add.at(out, lo, psi)
            np.add.at(out, hi, np.where(b == 1, -1, 1)*psi)
            psi = out
            continue
        if g == "x":
            src = idx ^ (1 << q[0])
        elif g == "cx":
            src = idx ^ (bit(q[0]) << q[1])
        elif g == "ccx":
            src = idx ^ ((bit(q[0]) & bit(q[1])) << q[2])
        else:
            a, b_ = q
            diff = bit(a) ^ bit(b_)
            src = idx ^ (diff << a) ^ (diff << b_)
        psi = psi[src]
    return psi


def _hub_dense(hs, n):
    out = np.zeros(2**n, dtype=complex)
    amps = {fid: M.cyc_to_complex(f.amp, hs.p) for fid, f in hs.F.items()}
    for h in range(hs.H):
        base = sum(int(hs.hub[w][h]) << w for w in range(n) if hs.owner[w] < 0)
        vec = {base: complex(M.cyc_to_complex(hs.hamp[h:h+1], hs.p)[0])}
        for fid, f in hs.F.items():
            rows = np.nonzero(f.h == h)[0]
            new = {}
            for r in rows:
                k = sum(int(f.cols[w][r]) << w for w in f.cols)
                for b, v in vec.items():
                    new[b | k] = new.get(b | k, 0)+v*amps[fid][r]
            vec = new
        for k, v in vec.items():
            out[k] += v
    return out


def _same_ray(u, v):
    u, v = u/np.linalg.norm(u), v/np.linalg.norm(v)
    return abs(abs(np.vdot(u, v))-1) < 1e-9


@pytest.mark.parametrize("seed", range(8))
def test_hub_state_equals_dense_after_split(seed):
    """Random circuit: Hadamards and permutation gates on a FactorState, split
    over random hub wires, then random permutation gates (hub wires also as
    targets) on the HubState; the represented state equals the dense one."""
    rng = random.Random(seed)
    n = 8
    prog = []
    st = M.FactorState(n, 2)
    for _ in range(30):
        if rng.random() < 0.35:
            w = rng.randrange(n)
            prog.append(("h", None, (w,)))
            st.qft((w,))
        else:
            k = rng.choice(["x", "cx", "ccx", "swap"])
            q = tuple(rng.sample(range(n), {"x": 1, "cx": 2, "ccx": 3, "swap": 2}[k]))
            prog.append(("p", k, q))
            st.run([(k, q)])
            st.split_constants(q)
    hub = rng.sample(range(n), 3)
    hs = M.HubState.split(st, hub)
    assert _same_ray(_hub_dense(hs, n), _dense(n, prog))
    for _ in range(40):
        k = rng.choice(["x", "cx", "ccx", "swap"])
        q = tuple(rng.sample(range(n), {"x": 1, "cx": 2, "ccx": 3, "swap": 2}[k]))
        prog.append(("p", k, q))
        hs.run([(k, q)])
        hs.split_constants(q)
    assert _same_ray(_hub_dense(hs, n), _dense(n, prog))


def _factor_vec(hs, h, n):
    """hamp[h] (x)_f psi_f(h) as a dense vector over the factor wires (hub-classical bits 0)."""
    vec = {0: complex(M.cyc_to_complex(hs.hamp[h:h+1], hs.p)[0])}
    for fid, f in hs.F.items():
        amps = M.cyc_to_complex(f.amp, hs.p)
        new = {}
        for r in np.nonzero(f.h == h)[0]:
            k = sum(int(f.cols[w][r]) << w for w in f.cols)
            for b, v in vec.items():
                new[b | k] = new.get(b | k, 0)+v*amps[r]
        vec = new
    out = np.zeros(2**n, dtype=complex)
    for k, v in vec.items():
        out[k] += v
    return out


def test_hub_gram_equals_dense_inner_products():
    rng = random.Random(11)
    n = 7
    st = M.FactorState(n, 3)
    regs = [(0, 1), (2, 3), (4, 5)]
    for q in regs:
        st.qft(q)
    for _ in range(30):
        k = rng.choice(["cx", "ccx"])
        q = tuple(rng.sample(range(n), {"cx": 2, "ccx": 3}[k]))
        st.run([(k, q)])
    hs = M.HubState.split(st, [0, 1, 6])
    Gt = hs.total_gram()
    V = [_factor_vec(hs, h, n) for h in range(hs.H)]
    ratio = None
    for h in range(hs.H):
        for h2 in range(hs.H):
            dense = np.vdot(V[h2], V[h])
            exact = complex(M.cyc_to_complex(Gt[h, h2][None, :], 3)[0])
            assert (abs(dense) < 1e-9) == (abs(exact) < 1e-9)
            if abs(dense) > 1e-9:
                ratio = ratio or exact/dense
                assert abs(exact/dense-ratio) < 1e-6*abs(ratio)
    assert ratio is not None and abs(ratio.imag) < 1e-9 and ratio.real > 0


# ---------------------------------------------------------------- exact level-0 law of the whole circuit

def test_exact_law_matches_plain_level0_and_checkpoints(heis):
    cfg, insts, ts, steps = heis
    inst = insts["<[(0, 0, 1)]> normal"]
    r = M.exact_level0_law(ts, inst, steps)
    assert r["hub_wires_only_controls"] and r["hub_joins"] == 0
    assert r["exact_law_uniform_on_h_perp"] and r["all_checkpoints_pass"]
    # K3 checks every child after its own merge (review finding 1), K4 checks the reference witness
    assert len(r["checkpoint_detail"]["K3_child_translated_after_its_own_merge"]) == 3
    assert r["checkpoints"]["K4_reference_witness_solves_sum_s2_lambda_eq_0"] is True
    L = M.plain_level0_law(ts, inst, steps)
    hl = {tuple(int(x) for x in k.strip("()").split(", ")): np.array([v, 0, 0]) for k, v in r["law"].items()}
    assert M.laws_proportional(L, hl, 3)


def test_exact_law_nonnormal_small_S(heis):
    """A non-normal subgroup with |S| = 3: the plain level-0 run would need a
    3.9e8-row factor; the hub decomposition gives the exact output law."""
    cfg, insts, ts, steps = heis
    r = M.exact_level0_law(ts, insts["<[(0, 1, 1)]> non-normal"], steps)
    assert r["hubs"] == 729 and r["label_tuples"] == 27
    assert r["exact_law_uniform_on_h_perp"] and r["all_checkpoints_pass"]


def test_hub_law_matches_plain_law_on_a_mutant(heis):
    """Cross-check of the two exact level-0 computations on circuits whose law is
    NOT uniform (the QFT preparing one coordinate of Q removed), and on a mutant
    with a uniform law (one CCX dropped in U_SDE)."""
    cfg, insts, ts, steps = heis
    qp = [i for i, s in enumerate(steps) if s[2] == "q_prep_qft"]
    cases = [([s for i, s in enumerate(steps) if i != qp[2]], "<[(0, 0, 1)]> normal", False),
             ([s for i, s in enumerate(steps) if i != qp[0]], "<[(1, 0, 0), (0, 0, 1)]> normal", False),
             (M.mutate_steps(steps, "sde_grade2", "ccx", "first")[0], "<[(0, 0, 1)]> normal", True)]
    for stp, name, uniform in cases:
        r = M.exact_level0_law(ts, insts[name], stp)
        assert r["exact_law_uniform_on_h_perp"] is uniform
        L = M.plain_level0_law(ts, insts[name], stp)
        hl = {tuple(int(x) for x in k.strip("()").split(", ")): np.array([v, 0, 0]) for k, v in r["law"].items()}
        assert M.laws_proportional(L, hl, 3)


# ---------------------------------------------------------------- checkpoints catch what the readout test misses

def test_oracle_entry_at_Z_caught_deterministically(heis):
    """One oracle entry changed at H = Z: the trajectory readout test caught it in
    1/60 runs (2026-11-05 check). Checkpoint K1 catches it on every run."""
    cfg, insts, ts, steps = heis
    inst = insts["<[(0, 0, 1)]> normal"]
    bad = copy.copy(inst)
    tab = np.array(inst.oracle_table).copy()
    x0 = int(np.nonzero(tab != tab[0])[0][0])
    tab[x0] = tab[0]
    bad.oracle_table = tab
    r = M.exact_level0_law(ts, bad, steps)
    assert r["checkpoints"]["K1_source_rdm_equals_coset_density"] is False
    assert not r["all_checkpoints_pass"]


@contextmanager
def _mutated_blocks(mut):
    orig = C.MergeBlock
    C.MergeBlock = lambda cfg, d, mutate=None: orig(cfg, d, mutate=mut)
    try:
        yield
    finally:
        C.MergeBlock = orig


def test_g_sign_caught_by_K4(heis):
    """The g_sign mutation leaves the readout law exactly uniform (Q's reduced
    state is unchanged at grade one), but the children are translated by
    +delta_s(sigma(q)): K4 catches it."""
    cfg, insts, _, _ = heis
    with _mutated_blocks({"g_sign"}):
        ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    r = M.exact_level0_law(ts, insts["<[(1, 0, 0)]> non-normal"], steps)
    assert r["exact_law_uniform_on_h_perp"]
    assert r["checkpoints"]["K4_children_equal_reference_translation_every_hub"] is False


# ---------------------------------------------------------------- power-class solver and class-five seeded runs

def test_power_class_solver_complete():
    rng = random.Random(5)
    for p, d, M_, g in [(7, 3, 4, 3), (7, 2, 5, 2), (5, 2, 5, 2), (7, 4, 4, 2), (7, 5, 2, 1), (3, 2, 4, 1)]:
        for _ in range(10):
            labels = [tuple(rng.randrange(p) for _ in range(g)) for _ in range(M_)]
            W = {tuple(int(x) for x in s) for s in all_witnesses(labels, d, p)}
            s, tot = power_class_sde(labels, d, p, rng)
            assert tot == len(W)
            assert (s is None) == (not W) and (s is None or s in W)


def test_seeded_runs_power_class_n5():
    cfg = Config(__import__("theorems.rees_end_to_end_sim", fromlist=["filiform5"]).filiform5(5))
    eng = SparseEngine(cfg)
    inst = n5_instances(5, names=["<e2> non-normal"])[0]
    _, r = run_algorithm_sparse_pc(cfg, inst, eng, seed=3, top=truth_state(cfg, inst, cfg.c))
    assert r["recovered"]


@pytest.mark.skipif(not __import__("os").environ.get("REES_SLOW"), reason="class five: ~1 min (REES_SLOW=1)")
def test_seeded_run_class_five():
    cfg, insts = family("n6", 7)
    inst = next(i for i in insts if "<e2> non-normal" in i.name)
    _, r = run_algorithm_sparse_pc(cfg, inst, SparseEngine(cfg), seed=9, top=truth_state(cfg, inst, cfg.c))
    assert r["recovered"] and r["solver_power_class_d3"] > 0


# ---------------------------------------------------------------- Lean module present

def test_lean_module_present():
    src = (ROOT/"formal/Formal/ReesMergeReduction.lean").read_text()
    for name in ("merge_product_eq_of_labels", "exponent_cancels", "witness_coords", "zero_product_indicator"):
        assert f"theorem {name}" in src
    assert "sorry" not in src and "axiom " not in src


def test_trajectory_source_checkpoint(heis):
    """Sampled trajectories with checkpoint KS (oracle-output measurements delayed
    to the end of each source, still a valid schedule): the unmutated circuit
    passes, one changed oracle entry at H = Z fails in every terminal sample."""
    cfg, insts, ts, steps = heis
    s2, ok = M.measurement_schedule(ts, steps, 2)
    sched = M.delay_oracle_measurements(ts, steps, s2)
    assert ok and sum(len(v) for v in sched.values()) == sum(len(v) for v in s2.values())
    inst = insts["<[(0, 0, 1)]> normal"]
    bad = copy.copy(inst)
    tab = np.array(inst.oracle_table).copy()
    tab[int(np.nonzero(tab != tab[0])[0][0])] = tab[0]
    bad.oracle_table = tab
    rng = np.random.default_rng(4)
    for _ in range(3):
        r = M.run_terminal_sample(ts, inst, steps, sched, rng, source_check=True)
        assert r["source_checks"] == 3 and r["source_checks_pass"] and r["exactly_uniform_on_h_perp"]
        r = M.run_terminal_sample(ts, bad, steps, sched, rng, source_check=True)
        assert not r["source_checks_pass"]


def test_trajectory_source_checkpoint_sees_dirty_workspace(heis):
    """Review finding 4: a dropped CX in a source's evaluation leaves the address and
    oracle-output state intact but the workspace dirty; KS now requires a clean
    workspace at its check point and catches it in every terminal sample."""
    cfg, insts, ts, steps = heis
    s2, ok = M.measurement_schedule(ts, steps, 2)
    sched = M.delay_oracle_measurements(ts, steps, s2)
    bad, _ = M.mutate_steps(steps, "source_evaluation", "cx", "first")
    bad = [tuple(x) for x in bad]
    inst = insts["<[(0, 0, 1)]> normal"]
    rng = np.random.default_rng(11)
    for _ in range(3):
        r = M.run_terminal_sample(ts, inst, bad, sched, rng, source_check=True)
        assert not r["source_checks_pass"]
