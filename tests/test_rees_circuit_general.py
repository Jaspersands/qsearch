"""Rees circuit generator for general (L, c, p): exact simulation of the compiled modules.

Finite falsifiers on fixed instances (AI-checked, pending human review). A pass
shows that the generated Qiskit gate lists reproduce the paper's sources,
instruments, merges and readout on the tested subgroups; it proves nothing
about other groups or about asymptotic cost. Slow tests are marked with the
`slow` skip mark below and run only with REES_SLOW=1 (no marker is registered
in this repo's pytest configuration, so a skipif mark is used instead).
"""
from fractions import Fraction
import os

import numpy as np
import pytest

import theorems.rees_circuit as R
import theorems.rees_circuit_general as G
from theorems.rees_end_to_end_sim import (
    HiddenInstance, NilGroup, filiform4, filiform5, heisenberg, rref,
)

slow = pytest.mark.skipif(os.environ.get("REES_SLOW") != "1", reason="slow; set REES_SLOW=1")

HEIS = G.Config(heisenberg(3))
N4 = G.Config(filiform4(5))
HEIS_INSTANCES = G.heis3_instances()
N4_INSTANCES = G.n4_instances(5)


@pytest.fixture(scope="module")
def heis_engine():
    return G.Engine(HEIS)


@pytest.fixture(scope="module")
def n4_engine():
    return G.Engine(N4)


def _sig(qc):
    return [(inst.operation.name, tuple(qc.find_bit(q).index for q in inst.qubits),
             tuple(qc.find_bit(c).index for c in inst.clbits), getattr(inst.operation, "ctrl_state", None))
            for inst in qc.data]


def _old(inst):
    return next(o for o in R.hidden_instances() if rref(o.log_h, 3) == rref(inst.log_h, 3))


# ---------------------------------------------------------------- status and algebra

def test_status_does_not_claim_a_coherent_receiver():
    for key in ("coherent_receiver_implemented", "general_sde_implemented", "formal_compiler_checked",
                "independent_review", "novelty_established", "speedup_claim_allowed"):
        assert G.STATUS[key] is False
    assert "pending human review" in G.STATUS["review"]


def test_bch_nodes_are_checked_and_match_the_classical_formula():
    assert [w for w, _ in G.bch_nodes(2)] == ["xy"]
    assert dict(G.bch_nodes(3)) == {"xy": Fraction(1, 2), "xxy": Fraction(1, 12), "yxy": Fraction(-1, 12)}
    assert len(G.bch_nodes(5)) == 13                     # free-algebra check runs inside bch_nodes
    rng = np.random.default_rng(3)
    for alg in (heisenberg(5), filiform4(5), filiform4(7), filiform5(7)):
        c = len(alg.lower_central_series())
        X, Y = rng.integers(0, alg.p, (3000, alg.dim)), rng.integers(0, alg.p, (3000, alg.dim))
        assert (G.GroupLaw(alg.tensor, c, alg.p).mul(X, Y) == NilGroup(alg.p, alg.tensor, c).mul(X, Y)).all()


def test_hidden_oracle_tables_equal_the_end_to_end_simulator():
    for alg, gens in ((heisenberg(3), ((1, 0, 0),)), (filiform4(5), ((1, 0, 1, 0),)),
                      (filiform4(5), ((0, 1, 0, 0), (0, 0, 0, 1)))):
        a, b = G.Hidden("t", alg, gens), HiddenInstance("t", alg, gens)
        assert (a.oracle_table == b.oracle_table).all() and a.log_h == b.log_h


def test_encoding_and_increment_synthesis():
    for p in (3, 5, 7, 11):
        enc = G.Encoding(p)
        for v in range(p):
            hits = [u for u in range(p) if all((u >> i & 1) == b for i, b in enc.tests[v])]
            assert hits == [v]
        for k in range(p):
            perm = list(range(p))
            for u, v in G.increment_sequence(p, k):
                perm = [v if x == u else u if x == v else x for x in perm]
            assert perm == [(x+k) % p for x in range(p)]


# ---------------------------------------------------------------- Heis(F_3): reproduce rees_circuit.py

def test_heis_subgroups_are_the_19_of_rees_circuit():
    assert len(HEIS_INSTANCES) == 19 and sum(not i.normal for i in HEIS_INSTANCES) == 12
    assert sorted(map(str, (i.log_h for i in HEIS_INSTANCES))) == \
        sorted(map(str, (rref(i.log_h, 3) for i in R.hidden_instances())))


def test_heis_circuits_are_gate_for_gate_those_of_rees_circuit():
    inst = next(i for i in HEIS_INSTANCES if not i.normal)
    old = _old(inst)
    a, b = R.source_circuit(old)[0], G.source_circuit(HEIS, inst)[0]
    assert _sig(a) == _sig(b)
    ua = next(i.operation for i in a.data if i.operation.name == "U_f")
    ub = next(i.operation for i in b.data if i.operation.name == "U_f")
    assert _sig(ua.definition) == _sig(ub.definition)
    assert _sig(R.instrument_circuit()[0]) == _sig(G.instrument_circuit(HEIS, 2)[0])
    for s in (1, 2):
        assert _sig(R.merge_circuit(s)[0]) == _sig(G.merge_circuit(HEIS, 2, s)[0])
        assert _sig(R.merge_circuit(s, bennett=False)[0]) == _sig(G.merge_circuit(HEIS, 2, s, bennett=False)[0])
    assert _sig(R.fourier_circuit("qft_final")[0]) == _sig(G.fourier_circuit(HEIS, 3, "qft_final")[0])
    for w in ((1, 2, 1), (1, 0, 1), (1, 1, 1)):
        qa, ca = R.terminal_sample_circuit(old, w)
        qb, Bb = G.terminal_sample_circuit(HEIS, inst, w)
        assert _sig(qa) == _sig(qb) and qb.num_qubits == 82 and dict(ca) == dict(Bb.counts)


def test_heis_resource_counts_equal_rees_circuit():
    _, B = G.terminal_sample_circuit(HEIS, None, (1, 2, 1))
    formula, note = G.primitive_formula(HEIS), R.paper_counts(1)
    for key, value in note.items():
        if key == "bracket_evaluations_upper_bound":
            assert formula["bracket_evaluations"] == B.counts["bracket_evaluations"] == 12
            assert G.paper_bracket_bound(HEIS) == value == 48
        else:
            assert formula[key] == B.counts[key] == value, key
    assert G.width_formula(HEIS) == 82
    qc, _ = G.terminal_sample_circuit(HEIS, None, (1, 1, 1))
    assert G.module_sum_counts(HEIS) == G.logical_ops(qc)
    assert G.gate_profile(G.merge_circuit(HEIS, 2, 2)[0]) == R.gate_profile(R.merge_circuit(2)[0])
    assert G.increment_gate_cost(3) == 8
    total = G.gate_profile(G.terminal_sample_circuit(HEIS, None, (1, 2, 1))[0])
    assert total == R.gate_profile(R.terminal_sample_circuit(None, (1, 2, 1))[0])
    assert total["transpiled_cx_u_excluding_oracle"]["cx"] == 5528 and total["qubits"] == 82


@pytest.mark.parametrize("s", [1, 2])
def test_heis_merge_proved_and_bit_level_equals_rees_circuit_table(s):
    assert G.prove_merge(HEIS, 2, s)["proved"]
    perm, flags = G.merge_bitlevel(HEIS, 2, s)
    assert all(v for k, v in flags.items() if k != "inputs") and flags["inputs"] == 27*81
    assert (perm == R.bch_reference(s)).all() and (perm == R.merge_table(s)).all()


def test_heis_every_subgroup_exhaustively(heis_engine):
    rows = [G.check_instance(HEIS, inst, heis_engine) for inst in HEIS_INSTANCES]
    assert all(r["passed"] for r in rows), [r for r in rows if not r["passed"]]
    assert all(r["grades"][2]["tuples"] == "all" for r in rows)
    assert sum(r["grades"][2]["cases"] for r in rows) == 3198          # rees_circuit's count
    assert sum(not r["normal"] for r in rows) == 12


@pytest.mark.parametrize("basis", [[(1, 0, 0)], [(0, 1, 1)], [(0, 0, 1)], [(1, 0, 0), (0, 0, 1)]])
def test_heis_exact_states_equal_rees_circuit_float_simulation(heis_engine, basis):
    inst = next(i for i in HEIS_INSTANCES if i.log_h == rref(basis, 3))
    old = _old(inst)
    st, _, _ = heis_engine.source(inst)
    assert np.abs(st.dense(HEIS.laws[2])-R.simulate_source(old)[0]).max() < 1e-12
    probs, states = heis_engine.label_law(st)
    branches, _ = R.simulate_instrument(R.simulate_source(old)[0])
    assert {l[0] for l in states} == set(branches)
    for lam, (pr, dense) in branches.items():
        assert abs(float(probs[(lam,)])-pr) < 1e-12
        assert np.abs(states[(lam,)].dense(HEIS.laws[2])-dense).max() < 1e-12
    labels = sorted(branches)[:1]*3
    for s in G.all_witnesses([(l,) for l in labels], 2, 3)[:5]:
        mine = heis_engine.merge([states[(l,)] for l, si in zip(labels, s) if si], [int(x) for x in s if x])
        theirs = R.channel_output([branches[l][1] for l in labels], tuple(int(x) for x in s))
        assert np.abs(mine.dense(HEIS.laws[1])-theirs).max() < 1e-12


@pytest.mark.parametrize("seed", [0, 1])
def test_heis_seeded_runs_recover_log_h_for_every_subgroup(heis_engine, seed):
    for inst in HEIS_INSTANCES:
        got, info = G.run_algorithm(HEIS, inst, heis_engine, seed=seed)
        assert got == rref(inst.log_h, 3) and info["oracle_queries"] == 7*3*2, inst.name


# ---------------------------------------------------------------- class three: n4(F_5)

def test_n4_config():
    assert N4.c == 3 and N4.dims == (4, 2, 1) and N4.points == (1, 2, 3)
    assert N4.arity == {2: 5, 3: 2} and N4.enc.nb == 3 and N4.label_bits == 10
    assert [w for w, _, _ in N4.nodes[3]] == ["xy", "xxy", "yxy"]
    assert sum(not i.normal for i in N4_INSTANCES) == 5


@pytest.mark.parametrize("d,s", [(d, s) for d in (2, 3) for s in range(1, 5)])
def test_n4_merge_gate_list_proved_on_all_inputs(d, s):
    flags = G.prove_merge(N4, d, s)
    assert flags["proved"], flags


@pytest.mark.parametrize("d,s", [(2, 1), (2, 4), (3, 2), (3, 3)])
def test_n4_merge_bit_level_on_sampled_q_all_x(d, s):
    rows = np.arange(0, N4.laws[d-1].order, 97 if d == 2 else 3907)
    _, flags = G.merge_bitlevel(N4, d, s, q_indices=rows)
    assert all(v for k, v in flags.items() if k != "inputs"), flags


def test_n4_merge_trace_from_bit_level_permutation(n4_engine):
    st, _, _ = n4_engine.source(N4_INSTANCES[2])
    _, states = n4_engine.label_law(st)
    lam = sorted(states)[-1]
    res = G.merge_trace_crosscheck(N4, n4_engine, states[lam], 3, 2, [0, 777, 12345])
    assert res["max_abs_diff_integer_units"] == 0 and res["equals_bch"] and res["scratch_clean"]


def test_n4_instrument_gate_lists_are_complete_central_instruments(n4_engine):
    for d in (2, 3):
        info = n4_engine.kernels[d][1]
        assert info["ok"] and info["leak"] < 1e-9 and info["circulant_err"] < 1e-9


@pytest.mark.parametrize("inst", N4_INSTANCES, ids=[i.name for i in N4_INSTANCES])
def test_n4_every_source_is_the_coset_density_of_the_lift(n4_engine, inst):
    st, S, info = n4_engine.source(inst)
    assert info["coset_state"] and info["workspace_clean"] and info["address_unchanged"]
    assert np.array_equal(np.sort(S), G.stage_indices(N4, inst.log_h, 3))
    assert st.equals_indicator(G.stage_indices(N4, inst.log_h, 3))


def test_n4_expanded_oracle_equals_table_semantics(n4_engine):
    inst = N4_INSTANCES[3]
    a, b = n4_engine.source(inst), n4_engine.source(inst, expand_oracle=True)
    assert (a[0].v == b[0].v).all() and a[2] == b[2]


@pytest.mark.parametrize("inst", N4_INSTANCES, ids=[i.name for i in N4_INSTANCES])
def test_n4_every_grade_exact(n4_engine, inst):
    row = G.check_instance(N4, inst, n4_engine, max_cases=400, sample_tuples=3, max_witnesses=25, seed=1)
    assert row["passed"], row
    for d in (3, 2):
        g = row["grades"][d]
        assert g["label_law_uniform_on_K_perp"] and g["merge_outputs_equal_rho_H"] and g["cases"] > 0
    assert row["grades"][3]["tuples"] == "all"            # every grade-3 label pair, every witness


def test_n4_seeded_runs_recover_log_h_with_is_solver_at_grade_three(n4_engine):
    for inst in N4_INSTANCES:
        got, info = G.run_algorithm(N4, inst, n4_engine, seed=20261103)
        assert got == rref(inst.log_h, 5), inst.name
        assert info["solver_is_d3"] == 8*5                  # kappa_3 = gcd(3, 4) = 1: IS applies at M_3 = 2
        # kappa_2 = 2 needs 8 or 18 columns > M_2 = 5, so brute force, except that an
        # all-zero label tuple (h contains gamma_2) is solved by IS at once (zero column)
        assert info.get("solver_brute_force_d2", 0)+info.get("solver_is_d2", 0) == 8
        assert info["oracle_queries"] == 8*10*3


def test_n4_is_solver_at_both_grades_with_arity_18():
    cfg = G.Config(filiform4(5), arities={2: 18})
    eng = G.Engine(cfg)
    for inst in (N4_INSTANCES[0], N4_INSTANCES[3], N4_INSTANCES[7]):
        got, info = G.run_algorithm(cfg, inst, eng, seed=5, extra_samples=2)
        assert got == rref(inst.log_h, 5) and "solver_brute_force_d2" not in info
        assert info["solver_is_d2"] == 6 and info["solver_is_d3"] == 6*18


def test_n4_resource_counts_match_formulas():
    qc, B = G.terminal_sample_circuit(N4, None)
    f = G.primitive_formula(N4)
    assert dict(B.counts) == f
    assert f["oracle_calls"] == 30 and f["bch_passes"] == 4*(10+5) and f["bracket_evaluations"] == 4*(10*3+5*1)
    assert f["bracket_evaluations"] <= G.paper_bracket_bound(N4)
    assert qc.num_qubits == G.width_formula(N4)
    assert G.module_sum_counts(N4) == G.logical_ops(qc)


# ---------------------------------------------------------------- negative controls (the checks can fail)

def test_negative_merge_without_bennett_uncompute_leaves_garbage():
    for cfg, d in ((HEIS, 2), (N4, 2), (N4, 3)):
        flags = G.prove_merge(cfg, d, 1, bennett=False)
        assert flags["x_equals_bch_right_translation"] and not flags["W_clean"] and not flags["proved"]


def test_negative_corrupted_macro_slice_is_rejected():
    from qiskit.circuit import CircuitInstruction
    from qiskit.circuit.library import XGate
    qc, B, _ = G.merge_circuit(N4, 3, 1)
    start = next(m[3] for m in B.macros if m[0] == "add_scaled")
    qc.data[start] = CircuitInstruction(XGate(), (qc.data[start].qubits[-1],))
    with pytest.raises(ArithmeticError):
        G.check_macros(qc, B)


def test_negative_class_two_bch_on_the_class_three_quotient_is_wrong():
    nodes = [n for n in N4.nodes[3] if len(n[0]) == 2]
    flags = G.prove_merge(N4, 3, 1, nodes=nodes)
    assert not flags["x_equals_bch_right_translation"] and not flags["proved"]


def test_negative_two_points_do_not_lift_on_class_three(n4_engine):
    inst = N4_INSTANCES[-1]                                   # trivial H
    _, S, _ = n4_engine.source(inst, points=(1, 2))
    assert len(S) > 1                                         # c-1 points hide a bigger subgroup


def test_negative_kept_evaluation_workspace_is_detected(n4_engine):
    _, S, info = n4_engine.source(N4_INSTANCES[0], uncompute=False)
    assert not info["workspace_clean"] and not np.array_equal(np.sort(S), G.stage_indices(N4, N4_INSTANCES[0].log_h, 3))


def test_negative_non_witness_scales_do_not_give_rho_h(n4_engine):
    inst = N4_INSTANCES[1]                                    # <e1>, non-normal, meets the centre trivially
    st, _, _ = n4_engine.source(inst)
    _, states = n4_engine.label_law(st)
    target = G.stage_indices(N4, inst.log_h, 2)
    labels = [(1,), (2,)]
    wrong = 0
    for s in [(1, 1), (1, 2), (2, 2)]:
        assert sum(si**3*l[0] for si, l in zip(s, labels)) % 5
        try:
            wrong += not n4_engine.merge([states[l] for l in labels], list(s)).equals_indicator(target)
        except ArithmeticError:
            wrong += 1
    assert wrong == 3


# ---------------------------------------------------------------- slow

@slow
@pytest.mark.parametrize("s", [1, 2, 3, 4])
def test_slow_n4_grade_two_merge_exhaustive_bit_level(s):
    _, flags = G.merge_bitlevel(N4, 2, s)
    assert flags["inputs"] == 625*15625 and all(v for k, v in flags.items() if k != "inputs")


@slow
@pytest.mark.parametrize("inst", N4_INSTANCES, ids=[i.name for i in N4_INSTANCES])
def test_slow_n4_more_label_tuples_all_witnesses(n4_engine, inst):
    row = G.check_instance(N4, inst, n4_engine, sample_tuples=12, seed=7)
    assert row["passed"], row


@slow
def test_slow_n4_f7_one_non_normal_subgroup():
    cfg = G.Config(filiform4(7))
    eng = G.Engine(cfg)
    inst = G.n4_instances(7)[0]
    row = G.check_instance(cfg, inst, eng, max_cases=50, sample_tuples=3, max_witnesses=8)
    assert row["passed"], row
    got, info = G.run_algorithm(cfg, inst, eng, seed=1, extra_samples=1)
    assert got == rref(inst.log_h, 7)


# ---------------------------------------------------------------- K30: exact instrument exponents

def _no_float(*a, **k):
    raise AssertionError("floating point used in the exact exponent path")


@pytest.mark.parametrize("cfg", [HEIS, N4], ids=["heis_f3", "n4_f5"])
def test_exact_instrument_exponents_use_no_float(monkeypatch, cfg):
    """The exact path never calls Operator, np.angle, np.exp, float, complex or round;
    the only float step left, the qft_gate matrix consistency check, is stubbed here."""
    monkeypatch.setattr(G, "Operator", _no_float)
    monkeypatch.setattr(G, "_qft_ok", lambda p: True)
    for name in ("float", "complex", "round"):
        monkeypatch.setattr(G, name, _no_float, raising=False)    # module globals shadow builtins
    for name in ("angle", "exp", "round", "rint"):
        monkeypatch.setattr(G.np, name, _no_float)
    for d in range(2, cfg.c+1):
        expo, info = G.instrument_semantics(cfg, d, exact=True)
        assert info["mode"] == "exact" and info["ok"]
        assert all(info[k] == 0 and type(info[k]) is int
                   for k in ("leak", "completeness_err", "circulant_err", "round_err"))
        for e in expo:
            assert e.dtype.kind == "i" and e.shape == (cfg.p, cfg.p)
        qc, top, sub_insts, orders = G._instrument_blocks(cfg, d)
        A, k = G._instrument_block_exact(sub_insts[0], {q: i for i, q in enumerate(orders[0])}, cfg.p, cfg.enc.nb)
        assert A.dtype.kind == "i" and type(k) is int and k == 2


@pytest.mark.parametrize("alg", [heisenberg(3), filiform4(5), filiform4(7), filiform5(5)],
                         ids=["heis_f3", "n4_f5", "n4_f7", "n5_f5"])
def test_exact_exponents_equal_closed_form_and_float_path(alg):
    """QFT, a -= z, QFT^dag gives k_lam(z) = zeta^(-lam z)/p, so kappa_lam(u) = zeta^(lam u):
    e[lam, u] = lam*u mod p, an integer computation; the float path agrees on every entry."""
    cfg = G.Config(alg)
    p = cfg.p
    closed = np.array([[(lam*u) % p for u in range(p)] for lam in range(p)], dtype=np.int64)
    res = G.instrument_exponent_agreement(cfg)
    assert res["mismatches"] == 0 and res["entries"] == p*p*sum(len(cfg.top(d)) for d in range(2, cfg.c+1))
    for d in range(2, cfg.c+1):
        for e in G.instrument_semantics(cfg, d)[0]:
            assert np.array_equal(e, closed)


def test_default_engine_uses_the_exact_path(heis_engine):
    assert G.INSTRUMENT_EXPONENTS == "exact"
    assert heis_engine.kernels[2][1]["mode"] == "exact"
    assert G.instrument_semantics(HEIS, 2, exact=False)[1]["mode"] == "float"


def test_exact_path_reads_the_gate_list(monkeypatch):
    """Mutations: a += z instead of a -= z flips the exponents (both paths agree);
    dropping the inverse QFT is not a complete central instrument (both paths raise)."""
    p = N4.p
    orig = G.instrument_ops

    def plus(cfg, B, d, a, z):
        role = f"qft_grade{d}"
        for j in range(len(cfg.top(d))):
            B.qft(z[j], role)
        for j, t in enumerate(cfg.top(d)):
            B.add_scaled(a[t], z[j], +1)
        for j in range(len(cfg.top(d))):
            B.qft(z[j], role, inverse=True)

    monkeypatch.setattr(G, "instrument_ops", plus)
    ex, fl = G.instrument_semantics(N4, 3, exact=True)[0], G.instrument_semantics(N4, 3, exact=False)[0]
    neg = np.array([[(-lam*u) % p for u in range(p)] for lam in range(p)])
    assert all(np.array_equal(a, neg) and np.array_equal(a, b) for a, b in zip(ex, fl))

    def no_inverse(cfg, B, d, a, z):
        for j in range(len(cfg.top(d))):
            B.qft(z[j], "r")
        for j, t in enumerate(cfg.top(d)):
            B.add_scaled(a[t], z[j], -1)

    monkeypatch.setattr(G, "instrument_ops", no_inverse)
    for exact in (True, False):
        with pytest.raises(ArithmeticError):
            G.instrument_semantics(N4, 3, exact=exact)
    monkeypatch.setattr(G, "instrument_ops", orig)
