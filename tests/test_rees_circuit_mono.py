"""Tests for theorems/rees_circuit_mono.py (monolithic trajectory simulation of
the assembled coherent terminal sample). AI-checked, pending human review.
Default run well under 60 s. The full runs are in the report folder
research/audits/reviews/2026-11-05-rees-receiver-sims/."""
import random
from contextlib import contextmanager

import numpy as np
import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
import theorems.rees_circuit_mono as M
from theorems.rees_circuit_arith import Anc, anc_size
from theorems.rees_coherent_sde import Macro, Prog


@pytest.fixture(scope="module")
def heis():
    cfg, insts = M.job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    return cfg, insts, ts, steps


@pytest.fixture(scope="module")
def n4():
    cfg, insts = M.job("n4_f5")
    ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    return cfg, insts, ts, steps


def test_status_gates_stay_false():
    assert M.STATUS["coherent_receiver_implemented"] is False
    assert M.STATUS["speedup_claim_allowed"] is False


# ---------------------------------------------------------------- the simulator against a dense statevector

def _dense_run(n, p, prog):
    """Dense statevector of n qubits; prog items: ('perm', gates) or ('qft'|'qft_dg', reg)."""
    psi = np.zeros(2**n, dtype=complex)
    psi[0] = 1
    idx = np.arange(2**n)
    for kind, payload in prog:
        if kind == "perm":
            for g, q in payload:
                bit = lambda w: (idx >> w) & 1
                if g == "x":
                    src = idx ^ (1 << q[0])
                elif g == "cx":
                    src = idx ^ (bit(q[0]) << q[1])
                elif g == "ccx":
                    src = idx ^ ((bit(q[0]) & bit(q[1])) << q[2])
                else:
                    a, b = q
                    diff = bit(a) ^ bit(b)
                    src = idx ^ (diff << a) ^ (diff << b)
                psi = psi[src]
        else:
            F = G.qft_matrix(p, inverse=(kind == "qft_dg"))
            reg = payload
            val = sum(((idx >> w) & 1) << i for i, w in enumerate(reg))
            rest = idx & ~sum(1 << w for w in reg)
            out = np.zeros_like(psi)
            for y in range(F.shape[0]):
                tgt = rest | sum(((y >> i) & 1) << w for i, w in enumerate(reg))
                np.add.at(out, tgt, F[y, val]*psi)
            psi = out
    return psi


def _factor_dense(st, n):
    psi = np.ones(1, dtype=complex)
    wires_done = []
    vec = {0: 1+0j}
    for fid, f in st.F.items():
        amps = M.cyc_to_complex(f.amp, st.p)
        rows = np.zeros(f.N, dtype=np.int64)
        for w, c in f.cols.items():
            rows |= M._unpack(c, f.N).astype(np.int64) << w
        vec = {k | int(r): v*a for k, v in vec.items() for r, a in zip(rows, amps)}
    const = sum(st.cval[w] << w for w in range(n) if st.owner[w] < 0)
    out = np.zeros(2**n, dtype=complex)
    for k, v in vec.items():
        out[k | const] += v
    return out


def _same_ray(u, v):
    u, v = u/np.linalg.norm(u), v/np.linalg.norm(v)
    return abs(abs(np.vdot(u, v))-1) < 1e-9


@pytest.mark.parametrize("seed", range(6))
def test_factor_state_equals_dense_random_qubit_circuits(seed):
    rng = random.Random(seed)
    n = 9
    prog = []
    for _ in range(45):
        r = rng.random()
        if r < 0.25:
            prog.append(("qft", (rng.randrange(n),)))          # QFT_2 = H
        else:
            k = rng.choice(["x", "cx", "ccx", "swap"])
            q = rng.sample(range(n), {"x": 1, "cx": 2, "ccx": 3, "swap": 2}[k])
            prog.append(("perm", [(k, tuple(q))]))
    st = M.FactorState(n, 2)
    for kind, payload in prog:
        if kind == "perm":
            st.run(payload)
            st.split_constants({w for _, q in payload for w in q})
        else:
            st.qft(payload)
    assert _same_ray(_factor_dense(st, n), _dense_run(n, 2, prog))


def test_factor_state_equals_dense_mod3_arithmetic():
    p, b = 3, 2
    regs = [(0, 1), (2, 3), (4, 5)]
    anc = Anc(list(range(6, 6+anc_size(b))), b)
    n = 6+anc_size(b)
    items = [("qft", regs[0]), ("qft", regs[1]),
             ("perm", Macro("add_product", 2, (regs[2], regs[0], regs[1]))),
             ("qft_dg", regs[0]), ("perm", Macro("add_scaled", 1, (regs[1], regs[2]))),
             ("qft", regs[2]), ("perm", Macro("add_scaled", 2, (regs[0], regs[2]))), ("qft_dg", regs[1])]
    prog = []
    for kind, it in items:
        prog.append(("perm", C.flatten(Prog([it]), p, anc)) if kind == "perm" else (kind, it))
    st = M.FactorState(n, p)
    for kind, payload in prog:
        if kind == "perm":
            st.run(payload)
            st.split_constants({w for _, q in payload for w in q})
        else:
            st.qft(payload, inverse=(kind == "qft_dg"))
    assert _same_ray(_factor_dense(st, n), _dense_run(n, p, prog))
    assert all(st.owner[w] < 0 and st.cval[w] == 0 for w in anc.all)      # ancillas split off clean


# ---------------------------------------------------------------- schedule

def test_schedule_verified_and_labels_only_controls(heis, n4):
    for cfg, insts, ts, steps in (heis, n4):
        for level in (1, 2):
            sched, ok = M.measurement_schedule(ts, steps, level)
            assert ok
            tags = [t for lst in sched.values() for t, _ in lst]
            assert tags.count("oracle_output") == ts.counts()["oracle_calls"]
        assert ts.structure()["garbage_never_touched_again"]


# ---------------------------------------------------------------- whole terminal samples

def test_heis_all_subgroups_one_trajectory_exactly_uniform(heis):
    cfg, insts, ts, steps = heis
    sched, _ = M.measurement_schedule(ts, steps, 2)
    rng = np.random.default_rng(7)
    assert len(insts) == 19
    for inst in insts:
        r = M.run_terminal_sample(ts, inst, steps, sched, rng)
        assert r["exactly_uniform_on_h_perp"] and r["workspace_clean"], inst.name
        assert r["counts"]["gates"] == 115282 and r["counts"]["oracle_calls"] == 6
        assert r["counts"]["qft"]+r["counts"]["qft_dg"] == 24


def test_heis_recovery_levels_1_and_2(heis):
    cfg, insts, ts, steps = heis
    for level in (1, 2):
        sched, _ = M.measurement_schedule(ts, steps, level)
        for inst in insts[1:4]:
            r = M.run_recovery(ts, inst, steps, sched, seed=level)
            assert r["recovered"], (level, inst.name)


def test_heis_fully_coherent_exact_law(heis):
    """level 0: nothing measured before the readout; the computed law is the
    exact output law of the whole circuit."""
    cfg, insts, ts, steps = heis
    sched, _ = M.measurement_schedule(ts, steps, 0)
    assert sched == {}
    inst = next(i for i in insts if i.name == "Heis(F_3) H=<[(0, 0, 1)]> normal")
    r = M.run_terminal_sample(ts, inst, steps, sched, np.random.default_rng(0))
    assert r["exactly_uniform_on_h_perp"] and r["readout_factor_extra_wires"] > 0


def test_n4_trajectories(n4):
    cfg, insts, ts, steps = n4
    sched, _ = M.measurement_schedule(ts, steps, 2)
    rng = np.random.default_rng(3)
    for name in ("trivial", "<e2> non-normal"):
        inst = next(i for i in insts if name in i.name)
        r = M.run_terminal_sample(ts, inst, steps, sched, rng)
        assert r["exactly_uniform_on_h_perp"] and r["workspace_clean"], name
        assert r["counts"]["gates"] == 2694596 and r["counts"]["oracle_calls"] == 36
        assert r["counts"]["qft"]+r["counts"]["qft_dg"] == 176


# ---------------------------------------------------------------- negative controls

@contextmanager
def _mutated_blocks(mut):
    orig = C.MergeBlock
    C.MergeBlock = lambda cfg, d, mutate=None: orig(cfg, d, mutate=mut)
    try:
        yield
    finally:
        C.MergeBlock = orig


def test_broken_bennett_schedule_detected(heis):
    """Merge blocks without the Bennett uncompute leave bracket garbage and
    break the readout. (The 'g_sign' mutation is not visible in the readout
    law on these trajectories; it is caught by the coherent backend's block
    checks.)"""
    cfg, insts, _, _ = heis
    with _mutated_blocks({"skip_bennett"}):
        ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    sched, _ = M.measurement_schedule(ts, steps, 2)
    rng = np.random.default_rng(1)
    bad = 0
    for inst in [i for i in insts if not i.normal][:4]:
        for _ in range(3):
            r = M.run_terminal_sample(ts, inst, steps, sched, rng)
            bad += not (r["support_in_h_perp"] and r["workspace_clean"])
    assert bad > 0


def test_early_measurement_of_a_target_register_detected(heis):
    """Measuring the root Q right after its preparation (it is later a merge
    control and the readout register) breaks the readout, and the schedule
    verifier rejects such a schedule."""
    cfg, insts, ts, steps = heis
    sched, _ = M.measurement_schedule(ts, steps, 2)
    root = tuple(w for q in ts.root for w in q)
    first = max(i for i, s in enumerate(steps) if s[0] == "qft" and set(s[1]) <= set(root)
                and s[2] == "q_prep_qft")
    bad_sched = {k: list(v) for k, v in sched.items()}
    bad_sched.setdefault(first, []).append(("child_grade1", root))
    rng = np.random.default_rng(2)
    inst2 = next(i for i in insts if i.normal and len(i.log_h) == 2)
    r = M.run_terminal_sample(ts, inst2, steps, bad_sched, rng)
    assert not r["exactly_uniform_on_h_perp"]
    # the verifier: a register used as a target later is not schedulable
    wires = set(root)
    assert any(s[3] & wires for s in steps[first+1:])
