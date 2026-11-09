"""End-to-end Rees simulation on Heis(F_3), Heis(F_5) and class-three n4(F_5), n4(F_7).

These are finite falsifiers. A pass shows the algorithm recovered log H on
the listed (G, H) with exact arithmetic; it proves nothing for other groups.
"""
from fractions import Fraction
from itertools import product
import random

import numpy as np
import pytest

from theorems.rees_end_to_end_sim import (
    DenseBackend, ExactBackend, NilGroup, brute_force_sde, chi_square,
    class_three_instances, expected_label_support, filiform4,
    filiform5, grade_run, heisenberg, instances, make_cover, negative_controls, run_rees,
    span_elements, stage_outputs_correct,
)

SEED = 20261102


def _all_cases():
    out = []
    for cover, insts in instances()+[class_three_instances(5)]:
        out += [(cover, inst) for inst in insts]
    return out


CASES = _all_cases()


def test_cover_dimensions_match_repo_cover_and_bch_matches_ode():
    from theorems.rees_hsp_reduction import _units, make_rees_cover
    from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra
    from theorems.uniform_bch_rees import bch_via_ode
    rng = random.Random(5)
    for alg in (heisenberg(3), heisenberg(5), filiform4(5), filiform4(7), filiform5(7)):
        cover = make_cover(alg)
        public = PublicLieAlgebra(alg.p, alg.dim, alg.bracket)
        assert make_rees_cover(public, _units(alg.dim)).dimensions == cover.dims
        G = cover.stage_group(cover.c)
        bracket = lambda x, y: tuple(int(v) for v in G.bracket(np.array(x), np.array(y)))
        for _ in range(40):
            x, y = (tuple(rng.randrange(alg.p) for _ in range(G.n)) for _ in range(2))
            ode = bch_via_ode(x, y, prime=alg.p, nilpotency_class=cover.c, bracket=bracket)
            assert tuple(G.mul(np.array(x), np.array(y)).tolist()) == ode


@pytest.mark.parametrize("alg", [heisenberg(3), filiform4(5)], ids=lambda a: a.name)
def test_group_laws_evaluations_dilations_and_quotients(alg):
    cover = make_cover(alg)
    p, rng = alg.p, np.random.default_rng(3)
    G, L = cover.stage_group(cover.c), NilGroup(p, alg.tensor, cover.c)
    a, b, c = (rng.integers(0, p, size=(500, G.n)) for _ in range(3))
    assert (G.mul(G.mul(a, b), c) == G.mul(a, G.mul(b, c))).all()
    assert not G.mul(a, G.inv(a)).any()
    for s in cover.points:
        E = cover.evaluation_matrix(s)
        assert (L.mul(a @ E % p, b @ E % p) == G.mul(a, b) @ E % p).all()
    for lam in range(1, p):
        D = cover.dilation_scales(cover.c, lam)
        assert (G.mul(a*D % p, b*D % p) == G.mul(a, b)*D % p).all()
    for d in range(cover.c, 1, -1):
        Gd, Q = cover.stage_group(d), cover.stage_group(d-1)
        x, y = a[:, :Gd.n], b[:, :Gd.n]
        assert (Gd.mul(x, y)[:, :Q.n] == Q.mul(x[:, :Q.n], y[:, :Q.n])).all()


def test_instances_cover_the_required_subgroup_types():
    flags = [inst.flags() for _, inst in CASES]
    names = [inst.name for _, inst in CASES]
    for prefix in ("Heis(F_3)", "Heis(F_5)", "n4(F_5)"):
        rows = [f for f, n in zip(flags, names) if n.startswith(prefix)]
        assert any(not f["normal"] and f["meets_center_trivially"] for f in rows)
        assert any(f["contains_center"] and f["dim_h"] > 0 for f in rows)
        assert any(f["normal"] and 0 < f["dim_h"] < 3 for f in rows)
    assert any(f["contains_center"] and not f["normal"] for f, n in zip(flags, names) if n.startswith("n4"))


@pytest.mark.parametrize("cover,inst", CASES, ids=[inst.name for _, inst in CASES])
def test_exact_end_to_end_recovers_log_H_with_uniform_label_laws(cover, inst):
    calls = []

    def oracle(x):        # the only access the algorithm has to H
        calls.append(x.shape)
        return inst.oracle(x)

    recovered, rec = run_rees(cover, oracle, ExactBackend(cover), seed=SEED, keep_states=True)
    # source preparation queries f once per evaluation point, on the whole superposition
    assert calls == [(cover.stage_group(cover.c).order, cover.algebra.dim)]*cover.c
    row = grade_run(cover, inst, recovered, rec, ExactBackend.__new__(ExactBackend))
    assert row["recovered_equals_log_H"], row
    assert rec.oracle_queries == cover.c*rec.top_sources
    for d, stage in row["stages"].items():
        assert stage["every_source_law_uniform_on_K_perp"], (d, stage)
        assert stage["observed_labels_in_support"]
        assert stage["min_witness_count"] >= 1
    # every intermediate source is exactly rho of H_d, for every record and witness
    assert stage_outputs_correct(cover, inst, rec)
    # grade one: the Fourier law is exactly uniform on (t h)^perp
    perp = {tuple(int(v) for v in r) for r in span_elements(
        expected_label_support_grade_one(cover, inst), cover.algebra.dim, cover.p)}
    for _, law in rec.readout:
        assert set(law) == perp and set(law.values()) == {Fraction(1, len(perp))}


def expected_label_support_grade_one(cover, inst):
    from theorems.rees_end_to_end_sim import nullspace
    return nullspace(inst.log_h, cover.algebra.dim, cover.p)


@pytest.mark.parametrize("index", [0, 1, 3, 4, 6])
def test_exact_end_to_end_class_three_over_F7(index):
    cover, insts = class_three_instances(7)
    inst = insts[index]
    recovered, rec = run_rees(cover, inst.oracle, ExactBackend(cover), seed=SEED+index, keep_states=True)
    row = grade_run(cover, inst, recovered, rec, ExactBackend.__new__(ExactBackend))
    assert row["recovered_equals_log_H"]
    assert all(s["every_source_law_uniform_on_K_perp"] for s in row["stages"].values())
    assert stage_outputs_correct(cover, inst, rec)
    assert row["stages"][3]["arity"] == 4      # kappa_3 = gcd(3, 6) = 3: cubes are not a bijection


@pytest.mark.parametrize("p", [3, 5])
def test_dense_float_backend_recovers_log_H_independently(p):
    cover, insts = instances()[0 if p == 3 else 1]
    backend = DenseBackend(cover)
    for inst in insts:
        recovered, rec = run_rees(cover, inst.oracle, backend, seed=SEED+1)
        row = grade_run(cover, inst, recovered, rec, backend)
        assert row["recovered_equals_log_H"], inst.name
        assert all(s["every_source_law_uniform_on_K_perp"] for s in row["stages"].values())


@pytest.mark.parametrize("p", [3, 5])
def test_exact_and_dense_states_agree_on_the_same_record(p):
    cover, insts = instances()[0 if p == 3 else 1]
    exact, dense = ExactBackend(cover), DenseBackend(cover)
    rng = random.Random(11)
    for inst in insts:
        es, _ = exact.prepare_source(inst.oracle)
        ds, _ = dense.prepare_source(inst.oracle)
        assert np.allclose(exact.to_dense(es), ds[1], atol=1e-12)
        elaw, dlaw = exact.label_probabilities(es), dense.label_probabilities(ds)
        assert all(abs(float(elaw[k])-dlaw[k]) < 1e-12 for k in elaw)
        allowed = [k for k, v in elaw.items() if v]
        for _ in range(3):
            labels = [rng.choice(allowed) for _ in range(3)]
            witness, _ = brute_force_sde(labels, 2, p, rng)
            eposts = [exact.condition(es, l, elaw[l]) for l in labels]
            dposts = [dense.condition(ds, l, dlaw[l]) for l in labels]
            for e, d in zip(eposts, dposts):
                assert np.allclose(exact.to_dense(e), d[1], atol=1e-12)
            eout, dout = exact.channel(eposts, witness), dense.channel(dposts, witness)
            assert np.allclose(exact.to_dense(eout), dout[1], atol=1e-12)


def test_sequential_schur_product_equals_joint_partial_trace():
    """The dense channel multiplies one target at a time; check against the joint
    controlled-unitary circuit with two targets on random small data."""
    rng = np.random.default_rng(0)
    nq, nt = 3, 4

    def rand_rho(n):
        a = rng.normal(size=(n, n))+1j*rng.normal(size=(n, n))
        r = a @ a.conj().T
        return r/np.trace(r)

    sigma, r1, r2 = rand_rho(nq), rand_rho(nt), rand_rho(nt)
    perms = [[np.eye(nt)[rng.permutation(nt)] for _ in range(nq)] for _ in range(2)]
    dim = nq*nt*nt
    CU = np.zeros((dim, dim), dtype=complex)
    for q in range(nq):
        e = np.zeros((nq, nq))
        e[q, q] = 1
        CU += np.kron(e, np.kron(perms[0][q], perms[1][q]))
    joint = CU @ np.kron(sigma, np.kron(r1, r2)) @ CU.conj().T
    reduced = np.einsum("aijbij->ab", joint.reshape(nq, nt, nt, nq, nt, nt))
    T1 = np.array([[np.trace(perms[0][q] @ r1 @ perms[0][r].conj().T) for r in range(nq)] for q in range(nq)])
    T2 = np.array([[np.trace(perms[1][q] @ r2 @ perms[1][r].conj().T) for r in range(nq)] for q in range(nq)])
    assert np.allclose(reduced, sigma*T1*T2)


def test_negative_controls_fail_exactly_where_the_paper_predicts():
    rows = negative_controls()
    assert rows
    for row in rows:
        # single evaluation: dilations preserve E_1^-1(h) iff [G, G] <= H (Prop. single-evaluation)
        assert row["failure_detected"] == (not row["derived_subgroup_in_H"]), row
        if row["control"] == "non_witness_scales" and not row["derived_subgroup_in_H"]:
            assert "does not descend" in row["check_raised"]


def test_sde_brute_force_finds_witnesses_at_chevalley_warning_arity():
    rng = random.Random(1)
    for p, d, g in ((5, 2, 2), (7, 3, 1), (7, 2, 2), (3, 2, 1)):
        from math import gcd
        M = gcd(d, p-1)*g+1
        for labels in product(product(range(p), repeat=g), repeat=M) if p**(g*M) <= 4000 else \
                [tuple(tuple(rng.randrange(p) for _ in range(g)) for _ in range(M)) for _ in range(200)]:
            s, count = brute_force_sde(list(labels), d, p, rng)
            assert s is not None and any(s) and count >= 1
            assert not (sum(x**d*np.array(l) for x, l in zip(s, labels)) % p).any()


def test_observed_top_labels_pass_chi_square_where_counts_allow():
    cover, insts = class_three_instances(5)
    inst = insts[-1]                      # trivial H: K_3^perp is all of F_5
    _, rec = run_rees(cover, inst.oracle, ExactBackend(cover), seed=SEED, extra_samples=8)
    allowed = {tuple(int(x) for x in r) for r in span_elements(
        expected_label_support(cover, inst.log_h, 3), 1, 5)}
    result = chi_square(rec.labels[3], allowed)
    assert result["n"] >= 100 and result["p_value"] > 1e-3


def test_report_flags_stay_false():
    from theorems.rees_end_to_end_sim import report
    out = report(seeds=(SEED,), dense=False)
    assert out["coherent_receiver_implemented"] is False
    assert out["schedule_one_solver_tested"] is False and out["asymptotic_cost_tested"] is False
    assert out["all_recovered"] and out["all_laws_uniform"]
    assert out["all_exact_stage_outputs_equal_rho_H_d"] and out["negative_controls_match_prediction"]
