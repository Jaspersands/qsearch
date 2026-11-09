"""Tests for round 3 (2026-11-05): the coset-symmetry reduction and hub
decomposition that give the exact level-0 output law of the class-three
terminal sample (n4(F_5)), its checkpoints at c = 3, and the c = 2 validation
against round 2. AI-checked, pending human review. Report:
research/audits/reviews/2026-11-05-rees-receiver-round3.md. The default run
takes a few minutes on an idle machine; the long runs are behind REES_SLOW."""
import copy
import os

import numpy as np
import pytest

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
import theorems.rees_circuit_mono as M
import theorems.rees_circuit_mono_c3 as R

SLOW = pytest.mark.skipif(not os.environ.get("REES_SLOW"), reason="long run; set REES_SLOW=1")


@pytest.fixture(scope="module")
def n4():
    cfg, insts, ts, steps, an = R.setup("n4_f5")
    return cfg, {i.name.split("H=")[1]: i for i in insts}, ts, steps, an


@pytest.fixture(scope="module")
def heis():
    cfg, insts = M.job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    return cfg, {i.name.split("H=")[1]: i for i in insts}, ts, steps


def test_status_gate_stays_false():
    assert R.STATUS["coherent_receiver_implemented"] is False
    assert M.STATUS["coherent_receiver_implemented"] is False


# ---------------------------------------------------------------- program anatomy

def test_anatomy_partitions_the_c3_program(n4):
    cfg, insts, ts, steps, an = n4
    assert an["ok"]
    assert len(an["nodes"]) == cfg.arity[2] == 6
    covered = set()
    for n in an["nodes"]:
        covered |= set(range(n["A"][0], n["A"][1]+1)) | set(range(n["inst"][0], n["inst"][1]+1))
    assert covered | set(an["root"]["steps"]) == set(range(len(steps)))
    assert not covered & set(an["root"]["steps"])
    rel = R.subtree_relabeling_check(ts, steps, an)
    assert rel["nodes_1_to_5_equal_node_0_up_to_wire_bijection"]


def test_relabeling_check_rejects_a_changed_subtree(n4):
    cfg, insts, ts, steps, an = n4
    n1 = an["nodes"][1]
    i = R._first_perm_step(steps, n1["A"][0], n1["A"][1], "bch_merge_grade3")
    stp, _ = R.drop_gate_at(steps, i, "cx", "middle")
    assert not R.subtree_relabeling_check(ts, stp, an)["per_node"][0]


def test_lemma_footprint_hypotheses_hold_and_a_violation_is_caught(n4):
    """Hypotheses (2)-(4) of Lemmas A and B read off the program; negative
    control: a CX from an oracle-output wire into the root's workspace, inserted
    in a root step, violates Lemma A (2)."""
    cfg, insts, ts, steps, an = n4
    h = R.lemma_hypotheses_check(ts, steps, an)
    assert h["ok"], h
    assert len(h["sources"]) == 12 and len(h["grade2_nodes"]) == 6
    y = M._wires(an["nodes"][0]["node"]["kids"][0]["ys"])[0]
    w = an["work"][0]
    i = next(i for i in an["root"]["steps"] if steps[i][0] == "perm")
    stp = [list(s_) for s_ in steps]
    stp[i] = [stp[i][0], [("cx", (y, w)), *stp[i][1], ("cx", (y, w))], stp[i][2], set(stp[i][3]), stp[i][4]]
    assert not R.lemma_hypotheses_check(ts, stp, an)["ok"]
    # negative control of the own-instrument condition: node 0's Q_2 touched inside node 1's
    # grade-2 instrument (an allowed component name, but not its own instrument)
    q = an["nodes"][0]["q2"][0]
    lo, hi = an["nodes"][1]["inst"]
    i = next(i for i in range(lo, hi+1) if steps[i][0] == "perm")
    stp = [list(s_) for s_ in steps]
    stp[i] = [stp[i][0], [("cx", (q, w)), *stp[i][1], ("cx", (q, w))], stp[i][2], set(stp[i][3]), stp[i][4]]
    h2 = R.lemma_hypotheses_check(ts, stp, an)
    assert not h2["ok"]
    assert h2["grade2_nodes"][0]["instrument_is_own_grade2_instrument"] is False
    assert all(r["ok"] for r in h2["sources"])


def test_combine_hub_ranges_requires_a_partition_and_equal_signatures():
    base = {"name": "x", "node": 0, "hubs": 10, "coset_x0": 0, "all_checkpoints_pass": True,
            "rho_Q2_signature": "a"}
    runs = [{**base, "hub_range": [0, 4]}, {**base, "hub_range": [4, 10]}]
    assert R.combine_hub_ranges(runs)["combined_all_checkpoints_pass_every_hub"]
    gap = [{**base, "hub_range": [0, 4]}, {**base, "hub_range": [5, 10]}]
    assert not R.combine_hub_ranges(gap)["combined_all_checkpoints_pass_every_hub"]
    sig = [{**base, "hub_range": [0, 4]}, {**base, "hub_range": [4, 10], "rho_Q2_signature": "b"}]
    assert not R.combine_hub_ranges(sig)["combined_all_checkpoints_pass_every_hub"]
    bad = [{**base, "hub_range": [0, 4]}, {**base, "hub_range": [4, 10], "all_checkpoints_pass": False}]
    assert not R.combine_hub_ranges(bad)["combined_all_checkpoints_pass_every_hub"]


# ---------------------------------------------------------------- PackedHub against a dense statevector

def _dense_run(n, H_wires, init_rows, gates):
    """Dense statevector of n wires from basis rows with amplitudes, then permutation gates."""
    psi = np.zeros(2**n, dtype=complex)
    for bits, a in init_rows:
        psi[sum(b << w for w, b in enumerate(bits))] += a
    idx = np.arange(2**n)
    for g, q in gates:
        bit = lambda w: (idx >> w) & 1
        if g == "x":
            src = idx ^ (1 << q[0])
        elif g == "cx":
            src = idx ^ (bit(q[0]) << q[1])
        elif g == "ccx":
            src = idx ^ ((bit(q[0]) & bit(q[1])) << q[2])
        else:
            a, b = q
            src = idx ^ ((bit(a) ^ bit(b)) << a) ^ ((bit(a) ^ bit(b)) << b)
        psi = psi[src]
    return psi


@pytest.mark.parametrize("seed", range(6))
def test_packed_hub_equals_dense(seed):
    """Random state sum_h |h> (x) |psi_1(h)> (x) |psi_2(h)> on 10 wires (hub wires
    0-2, child 1 wires 3-5, child 2 wires 6-8, workspace 9), random gates that
    never couple the children; the PackedHub representation equals the dense run."""
    rng = np.random.default_rng(seed)
    n, hubw, c1, c2, ws = 10, [0, 1, 2], [3, 4, 5], [6, 7, 8], [9]
    H = 8
    hub_bits = np.array([[(h >> k) & 1 for k in range(3)] for h in range(H)], dtype=np.uint8)
    kids = []
    for cw in (c1, c2):
        rows = []
        for h in range(H):
            k = int(rng.integers(1, 4))
            vals = rng.choice(8, size=k, replace=False)
            amps = rng.integers(1, 4, size=k)
            rows.append([(int(v), int(a)) for v, a in zip(vals, amps)])
        kids.append(rows)
    gates = []

    def rand_gate(targets, controls):
        g = ["x", "cx", "ccx"][int(rng.integers(3))]
        k = {"x": 0, "cx": 1, "ccx": 2}[g]
        t = int(rng.choice(targets))
        cs = [int(w) for w in rng.choice([w for w in controls if w != t], size=k, replace=False)]
        return (g, tuple(cs+[t]))
    for _ in range(4):
        gates += [rand_gate(hubw, hubw) for _ in range(5)]           # hub-only gates (hub targets)
        for side in (c1, c2):
            A = [rand_gate(ws, hubw+side[:1]) for _ in range(3)]      # compute into the workspace
            Cg = [rand_gate(side[1:], hubw+side+ws) for _ in range(8)]   # act on the child
            gates += A + Cg + A[::-1]                                  # uncompute: workspace back to 0
            gates.append(("swap", (side[1], side[2])))
    # dense reference: amplitude of (h, x1, x2) = a1 * a2
    init = []
    for h in range(H):
        for v1, a1 in kids[0][h]:
            for v2, a2 in kids[1][h]:
                bits = [0]*n
                for k in range(3):
                    bits[k] = int(hub_bits[h, k])
                for k in range(3):
                    bits[c1[k]] = (v1 >> k) & 1
                    bits[c2[k]] = (v2 >> k) & 1
                init.append((bits, a1*a2))
    psi = _dense_run(n, hubw, init, gates)
    # PackedHub
    engines, amps = [], []
    for kk, cw in enumerate((c1, c2)):
        hr, vals, am = [], [], []
        for h in range(H):
            for v, a in kids[kk][h]:
                hr.append(h)
                vals.append(v)
                am.append(a)
        e = R._Rows(np.array(hr), np.arange(len(hr)), H)
        for k, w in enumerate(cw):
            e.cols[w] = R.pack([(v >> k) & 1 for v in vals])
        engines.append(e)
        amps.append(np.array(am))
    ph = R.PackedHub(H, {w: hub_bits[:, k] for k, w in enumerate(hubw)}, engines)
    for g, q in gates:
        ph.gate(g, q)
        ph.delocalize_zeros(q)
    # rebuild the dense vector from PackedHub: product over the two children per hub
    out = np.zeros(2**n, dtype=complex)
    vals = []
    for kk, cw in enumerate((c1, c2)):
        e = ph.E[kk]
        full = {w: ph.read(kk, [w]) for w in range(n) if w in e.cols}
        vals.append(full)
    for h in range(H):
        r1 = np.nonzero(ph.E[0].h == h)[0]
        r2 = np.nonzero(ph.E[1].h == h)[0]
        for i1 in r1:
            for i2 in r2:
                idx = 0
                for w in range(n):
                    if w in ph.E[0].cols:
                        b = vals[0][w][i1]
                    elif w in ph.E[1].cols:
                        b = vals[1][w][i2]
                    else:
                        b = int(ph.hub[w][h]) if w in ph.hub else 0
                    idx |= int(b) << w
                out[idx] += amps[0][ph.E[0].src[i1]]*amps[1][ph.E[1].src[i2]]
    assert np.allclose(out, psi)


def test_packed_hub_refuses_a_gate_joining_two_children():
    e1 = R._Rows(np.array([0]), np.array([0]), 1)
    e2 = R._Rows(np.array([0]), np.array([0]), 1)
    e1.cols[1] = R.pack([1])
    e2.cols[2] = R.pack([1])
    ph = R.PackedHub(1, {}, [e1, e2])
    with pytest.raises(AssertionError):
        ph.gate("cx", (1, 2))


# ---------------------------------------------------------------- the reduction at c = 2 against round 2

@pytest.mark.parametrize("name", ["<[(0, 0, 1)]> normal", "<[(1, 0, 0), (0, 0, 1)]> normal",
                                  "<[(1, 0, 0)]> non-normal"])
def test_coset_conditioning_leaves_the_c2_level0_law_unchanged(heis, name):
    cfg, insts, ts, steps = heis
    inst = insts[name]
    base = M.exact_level0_law(ts, inst, steps)
    S = set(G.stage_indices(cfg, inst.log_h, 2).tolist())
    x_out = next(x for x in range(cfg.laws[2].order) if x not in S)
    for x0 in (0, x_out):
        r = M.exact_level0_law(ts, inst, steps, condition_sources=x0)
        L1 = {k: np.array([v, 0, 0]) for k, v in base["law"].items()}
        L2 = {k: np.array([v, 0, 0]) for k, v in r["law"].items()}
        assert M.laws_proportional(L1, L2, cfg.p)
        assert r["all_checkpoints_pass"]


def test_a_changed_oracle_entry_changes_the_conditioned_c2_law(heis):
    """Negative control for the reduction check (conditioned law against the
    unreduced law of the same oracle): with one changed oracle entry the key
    fibres are no longer the left cosets (Lemma A (1) fails), and the conditioned
    law differs from the unreduced law of that oracle, so the comparison can fail.
    (Against the unmutated law it would not: conditioning on the identity coset
    projects most of the change away.)"""
    cfg, insts, ts, steps = heis
    inst = insts["<[(0, 0, 1)]> normal"]
    bad = copy.copy(inst)
    tab = np.array(inst.oracle_table).copy()
    x0 = int(np.nonzero(tab != tab[0])[0][0])
    tab[x0] = tab[0]
    bad.oracle_table = tab
    unred = M.exact_level0_law(ts, bad, steps, checkpoints=False)
    r = M.exact_level0_law(ts, bad, steps, condition_sources=0, checkpoints=False)
    L1 = {k: np.array([v, 0, 0]) for k, v in unred["law"].items()}
    L2 = {k: np.array([v, 0, 0]) for k, v in r["law"].items()}
    assert not M.laws_proportional(L1, L2, cfg.p)


# ---------------------------------------------------------------- Phase A / B at c = 3

def test_sources_ks_and_conditioning(n4):
    cfg, insts, ts, steps, an = n4
    r = R.phase_a(ts, insts["<e2> non-normal"], steps, an, 0, sources_only=True)
    assert r["all_checkpoints_pass"]
    assert r["checkpoints"]["KS_source_state_is_coset_superposition"]
    assert r["checkpoints"]["K2_instrument_equals_reference"]


def test_ks_catches_a_changed_oracle_entry_at_c3(n4):
    cfg, insts, ts, steps, an = n4
    inst = insts["<e2> non-normal"]
    bad = copy.copy(inst)
    tab = np.array(inst.oracle_table).copy()
    x0 = int(np.nonzero(tab != tab[0])[0][0])
    tab[x0] = tab[0]
    bad.oracle_table = tab
    r = R.phase_a(ts, bad, steps, an, 0, sources_only=True)
    assert r["checkpoints"]["KS_source_state_is_coset_superposition"] is False


def test_instrument_reference_rejects_a_wrong_coset(n4):
    cfg, insts, ts, steps, an = n4
    law = cfg.laws[3]
    # address 0 against a non-central address (first coordinate 1); a central
    # address would give the same keys with other phases
    e1 = np.zeros((1, law.n), dtype=np.int64)
    e1[0, 0] = 1
    x1 = int(law.encode(e1)[0])
    assert 0 not in cfg.top(3)
    k1, a1, _ = R.instrument_reference(law, cfg.top(3), np.array([0]), 1, 5)
    k2, a2, _ = R.instrument_reference(law, cfg.top(3), np.array([x1]), 1, 5)
    assert not np.array_equal(k1, k2)
    # and a central address: same keys, amplitudes not proportional
    zc = np.zeros((1, law.n), dtype=np.int64)
    zc[0, cfg.top(3)[0]] = 1
    k3, a3, _ = R.instrument_reference(law, cfg.top(3), law.encode(zc), 1, 5)
    assert np.array_equal(np.sort(k1), np.sort(k3))
    o1, o3 = np.argsort(k1), np.argsort(k3)
    a1s, a3s = a1[o1], a3[o3]
    # proportional over Z[zeta_5] iff a1[0]*a3[j] == a1[j]*a3[0] for every j
    cross = M.cyc_mul_rows(np.repeat(a1s[:1], len(a1s), 0), a3s, 5) - M.cyc_mul_rows(a1s, np.repeat(a3s[:1], len(a3s), 0), 5)
    assert M.cyc_canon(cross).any()


def test_phase_b_root_merge_conditional_law(n4):
    """Phase B on <e2> (K_2^perp has 25 labels) conditioned on the zero grade-2
    label tuple: all checkpoints, and the conditional law is uniform on h^perp."""
    cfg, insts, ts, steps, an = n4
    inst = insts["<e2> non-normal"]
    lt = R.label_tuple_choices(cfg, inst, 0)[0]
    r = R.phase_b(ts, inst, steps, an, label_tuple=lt)
    assert r["all_checkpoints_pass"] and r["exact_law_uniform_on_h_perp"]


@SLOW
def test_phase_a_trivial_all_checkpoints(n4):
    cfg, insts, ts, steps, an = n4
    r = R.phase_a(ts, insts["trivial"], steps, an, 0, direct_gram=True, return_rows=True)
    keep_rows, kids, _, _, qv, descs = r.pop("_rows")
    assert r["all_checkpoints_pass"]
    assert all(r["direct_gram_equals_descriptor"])
    # negative control of the cross-check: one changed amplitude of child 1 (a row
    # of label tuple 0) or one changed descriptor entry is detected
    bad = [dict(k) for k in kids]
    amp = bad[1]["amp"].copy()
    src0 = keep_rows[0][2][1][1][0]
    amp[src0] = 2*amp[src0]
    bad[1]["amp"] = amp
    assert not R._direct_gram_check(keep_rows, bad, 0, descs[0], 5, len(qv))
    Qs, Qps, vals = descs[0]
    v2 = vals.copy()
    v2[0, 0] += 1
    assert not R._direct_gram_check(keep_rows, kids, 0, (Qs, Qps, v2), 5, len(qv))


@SLOW
def test_phase_a_g_sign_mutant_caught(n4):
    _, insts_m, tsm, stm, anm = R.setup("n4_f5", mutate_block="g_sign")
    inst = next(i for i in insts_m if i.name.endswith("H=<e2> non-normal"))
    r = R.phase_a(tsm, inst, stm, anm, 0)
    assert not r["all_checkpoints_pass"]
    assert r["checkpoints"]["K4_children_equal_reference_translation_every_hub"] is False


@SLOW
def test_phase_b_gamma2_exact_law(n4):
    cfg, insts, ts, steps, an = n4
    r = R.phase_b(ts, insts["<e3,e4> = gamma_2"], steps, an)
    assert r["all_checkpoints_pass"] and r["exact_law_uniform_on_h_perp"]


# ---------------------------------------------------------------- overflow-free Gram products

def test_cyc_mul_rows_exact_matches_int64_and_survives_overflow():
    rng = np.random.default_rng(1)
    a = rng.integers(-50, 50, size=(7, 5))
    b = rng.integers(-50, 50, size=(7, 5))
    assert np.array_equal(R.cyc_mul_rows_exact(a, b, 5), M.cyc_mul_rows(a, b, 5))
    big = a.astype(object) * (1 << 40)
    out = R.cyc_mul_rows_exact(big, b.astype(object) * (1 << 40), 5)
    assert out.dtype == object
    assert np.array_equal(out, M.cyc_mul_rows(a, b, 5).astype(object) * (1 << 80))


def test_law_signature_is_scale_free_and_separates_laws():
    L = {(0, 0): np.array([3, 0, 0, 0, 0]), (1, 0): np.array([3, 0, 0, 0, 0])}
    L2 = {k: 7*v for k, v in L.items()}
    L3 = {(0, 0): np.array([3, 0, 0, 0, 0]), (1, 0): np.array([6, 0, 0, 0, 0])}
    assert R.law_signature(L) == R.law_signature(L2)
    assert R.law_signature(L) != R.law_signature(L3)


def test_fast_left_coset_ids_equal_the_reference(n4):
    cfg, insts, ts, steps, an = n4
    for name, d in (("<e2,e4> non-normal", 3), ("<e2,e4> non-normal", 2), ("<e3,e4> = gamma_2", 2),
                    ("<e2> non-normal", 3)):
            S = G.stage_indices(cfg, insts[name].log_h, d)
            assert np.array_equal(R.left_coset_ids(cfg.laws[d], S), M._left_coset_ids(cfg.laws[d], S))
