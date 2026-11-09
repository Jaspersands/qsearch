"""Tests for theorems/rees_end_to_end_ext.py (scaled exact end-to-end Rees simulation).

Every end-to-end test asserts exact recovery of log H, exactly uniform label
laws on K_d^perp for every measured state, every stage output equal to
rho_(H_d), the grade-one law uniform on (th)^perp, block sizes equal to the
charged arity, and oracle queries equal to c * S * prod_d M_d.
"""
import dataclasses
from itertools import product
import random

import numpy as np
import pytest

from theorems import rees_end_to_end_ext as X
from theorems import rees_end_to_end_sim as base
from theorems.rees_is_sde_solver import is_arity, is_sde_solve, verify


def _assert_run(row):
    assert "aborted" not in row, row
    assert row["recovered_equals_log_H"], row["instance"]
    assert row["every_stage_output_equals_rho_H_d"], row["instance"]
    assert row["top_source_equals_rho_H_c"], row["instance"]
    assert row["readout_law_uniform_on_h_perp"], row["instance"]
    assert row["queries_equal_charged"], row["instance"]
    for d, st in row["stages"].items():
        assert st["every_measured_law_uniform_on_K_perp"], (row["instance"], d)
        assert st["observed_labels_in_support"], (row["instance"], d)
        assert st["block_sizes"] == [st["charged_arity"]], (row["instance"], d)


# ---------------------------------------------------------------- Rule W

@pytest.mark.parametrize("key,expected", [
    ("heis3", {2: ("schedule1", 64)}),
    ("heis5", {2: ("schedule1", 64)}),
    ("n4_5", {2: ("schedule1", 324), 3: ("linear", 2)}),
    ("n4_7", {2: ("schedule1", 324), 3: ("schedule1", 46656)}),
    ("n5_7", {2: ("schedule1", 1024), 3: ("schedule1", 531441), 4: ("schedule1", 64)}),
    ("n5_11", {2: ("schedule1", 1024), 3: ("linear", 3), 4: ("schedule1", 64)}),
    ("heis1031", {2: ("schedule2", 4)}),
])
def test_rule_w_table(key, expected):
    cover = base.make_cover(X.catalogue()[key][0]())
    sch = X.tree_schedules(cover)
    assert {d: (s.schedule, s.arity) for d, s in sch.items()} == expected
    for s in sch.values():
        assert s.arity <= s.paper_B_d          # B_kappa(g) <= B_d(g), g_d + 1 when kappa = 1


def test_rule_w_thresholds_and_deterministic_count():
    assert X.rule_w(1019, 2, 1).schedule == "schedule1"     # 1019 < 16 * 2^6 = 1024
    assert X.rule_w(1031, 2, 1).schedule == "schedule2"
    assert X.rule_w(1031, 2, 3).arity == 16                  # (g+1)((kappa-1)g+1)
    assert X.rule_w(105019, 3, 2) == X.GradeSchedule(3, 3, 2, "schedule2", 15, is_arity(3, 2))
    assert X.rule_w(104971, 3, 2).schedule == "schedule1"   # below 16 * 3^8 = 104976
    assert X.rule_w(1031, 3, 2).schedule == "linear"        # gcd(3, 1030) = 1
    # deterministic count G(kappa, g)^ceil(log2 t): t = 2 at p = 5 (-1 a square), t = 3 at p = 7
    assert X.rule_w(5, 2, 1, count="deterministic").arity == 8
    assert X.rule_w(7, 2, 1, count="deterministic").arity == 64
    assert X.rule_w(7, 3, 2, count="deterministic").arity == 729
    with pytest.raises(ValueError):
        X.rule_w(7, 2, 1, count="other")


@pytest.mark.parametrize("p,d,g", [(1031, 2, 1), (1031, 2, 2), (1031, 2, 3), (1031, 4, 2),
                                   (105019, 3, 2), (105019, 3, 3)])
def test_schedule2_solver_with_bezout_lift(p, d, g):
    sched = X.rule_w(p, d, g)
    assert sched.schedule == "schedule2"
    rng = random.Random(p*d+g)
    families = [
        [tuple(rng.randrange(p) for _ in range(g)) for _ in range(sched.arity)],
        [tuple(int(i == j % g) for i in range(g)) for j in range(sched.arity)],
        [tuple(int(i == 0) for i in range(g))]*sched.arity,
        [tuple([0]*g)]+[tuple(rng.randrange(1, p) for _ in range(g)) for _ in range(sched.arity-1)],
    ]
    for cols in families:
        stats = X.SolverStats()
        s = X.solve_block(p, sched, cols, rng, stats)
        assert any(s) and verify(p, d, cols, s)
        assert stats.schedule2_calls == 1


def test_solve_block_refuses_wrong_block_size():
    sched = X.rule_w(5, 2, 1)
    with pytest.raises(AssertionError):
        X.solve_block(5, sched, [(1,)]*3, random.Random(0), X.SolverStats())


# ---------------------------------------------------------------- sparse backend vs round 1

def _round1_pair(key, gens):
    build = X.catalogue()[key][0]
    alg = build()
    cover = base.make_cover(alg)
    inst = base.HiddenInstance("t", alg, gens)
    dense_b = base.ExactBackend(cover)
    sparse_b = X.SparseExactBackend(cover)
    dense, _ = dense_b.prepare_source(inst.oracle)
    sparse, info = X.prepare_source(cover, inst, sparse_b, "exhaustive")
    return cover, inst, dense_b, sparse_b, dense, sparse


@pytest.mark.parametrize("key,gens", [
    ("heis3", ((1, 0, 0),)), ("heis5", ()), ("heis5", ((0, 1, 1),)), ("heis5", ((0, 0, 1),)),
    ("n4_5", ((0, 1, 0, 0),)), ("n4_5", ((0, 1, 0, 0), (0, 0, 0, 1))), ("n4_5", ((1, 0, 1, 0),)),
])
def test_sparse_backend_equals_round1_state_by_state(key, gens):
    cover, inst, db, sb, dense, sparse = _round1_pair(key, gens)
    assert sb.equals_dense(sparse, dense)
    rng = random.Random(7)
    for d in range(cover.c, 1, -1):
        law_d = db.label_probabilities(dense)
        law_s = sb.label_law(sparse).as_dict()
        assert law_d == law_s
        support = [lam for lam, pr in law_d.items() if pr]
        posts_d, posts_s = {}, {}
        for lam in support:
            posts_d[lam] = db.condition(dense, lam, law_d[lam])
            posts_s[lam] = sb.condition(sparse, lam)
            assert sb.equals_dense(posts_s[lam], posts_d[lam])
        M = X.rule_w(cover.p, d, cover.dims[d-1], count="deterministic").arity
        labels = [rng.choice(support) for _ in range(M)]
        s = is_sde_solve(cover.p, d, labels).s
        dense = db.channel([posts_d[l] for l in labels], s)
        sparse = sb.channel([posts_s[l] if x else None for l, x in zip(labels, s)], s)
        assert sb.equals_dense(sparse, dense)
    assert db.readout_probabilities(dense) and sb.readout_law(sparse)["class_mass"]


def test_monomial_mode_matches_poly_mode(monkeypatch):
    for key, gens in (("heis5", ((1, 0, 0),)), ("heis5", ((0, 0, 1),)), ("n4_5", ((0, 1, 0, 0),))):
        cover, inst, db, sb, dense, sparse = _round1_pair(key, gens)
        monkeypatch.setattr(X, "POLY_MAX_PRIME", 0)
        mb = X.SparseExactBackend(cover)
        assert mb.mono
        mono = mb.source_from_dense(dense)
        assert mb.equals_dense(mono, dense)
        law_d = db.label_probabilities(dense)
        assert mb.label_law(mono).as_dict() == law_d
        for lam, pr in law_d.items():
            if pr:
                assert mb.equals_dense(mb.condition(mono, lam), db.condition(dense, lam, pr))
        monkeypatch.setattr(X, "POLY_MAX_PRIME", 64)


@pytest.mark.parametrize("key,gens", [("n4_5", ((0, 1, 0, 0),)), ("n4_5", ((1, 1, 0, 0), (0, 0, 1, 0))),
                                      ("heis5", ((0, 0, 1),)), ("heis5", ())])
def test_source_modes_agree(key, gens):
    alg = X.catalogue()[key][0]()
    cover = base.make_cover(alg)
    inst = base.HiddenInstance("t", alg, gens)
    b = X.SparseExactBackend(cover)
    states = [X.prepare_source(cover, inst, b, mode)[0] for mode in ("exhaustive", "level_set", "substitute")]
    for st in states[1:]:
        assert (st.idx == states[0].idx).all() and b.equals_coset_state(st, states[0].idx)


# ---------------------------------------------------------------- end to end

@pytest.mark.parametrize("key,count", [("heis3", "rule_w"), ("heis5", "rule_w"), ("heis5", "deterministic"),
                                       ("n4_5", "deterministic")])
def test_end_to_end_every_subgroup(key, count):
    rows = X.run_instance(key, count=count)
    assert len(rows) == len(X.catalogue()[key][1])
    for row in rows:
        _assert_run(row)
    flags = [(r["normal"], r["meets_center_trivially"], r["contains_center"]) for r in rows]
    assert (False, True, False) in flags        # non-normal, H cap Z(G) = 1
    assert (False, False, True) in flags or key.startswith("heis")


def test_end_to_end_n4_5_rule_w_arity():
    rows = X.run_instance("n4_5", ["<e2> non-normal", "<e1+2e2+e4>", "<e2,e3> non-normal", "trivial"])
    for row in rows:
        _assert_run(row)
        assert row["stages"][2]["charged_arity"] == 324 and row["stages"][3]["charged_arity"] == 2
        assert row["oracle_queries"] == 3*8*324*2


def test_full_solver_path_runs_end_to_end():
    """Diagnostic witness policy: solve on nonzero labels, so Theorem 11 supplies witnesses."""
    rows = X.run_instance("heis5", ["trivial", "<x> non-normal"], count="rule_w", avoid_zero_columns=True)
    rows += X.run_instance("n4_5", ["trivial", "<e1+e3> non-normal"], avoid_zero_columns=True)
    for row in rows:
        _assert_run(row)
        assert row["stages"][2]["diagnostic_nonzero_solves"] > 0
        assert row["stages"][2]["theorem11_calls"] > 0


def test_class_four_n5_over_F11_rule_w():
    rows = X.run_instance("n5_11", ["<e2> non-normal"])
    (row,) = rows
    _assert_run(row)
    assert [row["stages"][d]["charged_arity"] for d in (2, 3, 4)] == [1024, 3, 64]
    assert row["oracle_queries"] == 4*9*1024*3*64
    assert row["meets_center_trivially"] and not row["normal"]


def test_schedule2_end_to_end_heis1031():
    rows = X.run_instance("heis1031", ["trivial", "<y+z> non-normal"])
    for row in rows:
        _assert_run(row)
        assert row["stages"][2]["schedule"] == "schedule2"
        assert row["stages"][2]["schedule2_calls"] == row["readout_samples"] == 7
        assert row["source"]["mode"] == "substitute"


def test_non_witness_is_detected():
    for key, gens in (("heis5", ((1, 0, 0),)), ("n4_5", ((0, 1, 0, 0),))):
        alg = X.catalogue()[key][0]()
        cover = base.make_cover(alg)
        inst = base.HiddenInstance("t", alg, gens)
        b = X.SparseExactBackend(cover)
        src, _ = X.prepare_source(cover, inst, b, "exhaustive")
        with pytest.raises(ArithmeticError, match="does not descend"):
            X.run_rees_ext(cover, src, b, X.tree_schedules(cover, "deterministic"), seed=3,
                           solver=X.non_witness_solver)


def test_single_evaluation_point_gives_wrong_stage_states():
    """Prop. single-evaluation: one point instead of c fails when [G, G] is not in H."""
    alg = base.filiform4(5)
    cover = base.make_cover(alg)
    one = base.ReesCover(cover.algebra, cover.series, cover.grades, cover.tensor, (1,))
    inst = base.HiddenInstance("t", alg, ((0, 1, 0, 0),))
    b = X.SparseExactBackend(one)
    src, _ = X.prepare_source(one, inst, b, "exhaustive")
    try:
        recovered, rec = X.run_rees_ext(one, src, b, X.tree_schedules(cover, "deterministic"), seed=3)
    except ArithmeticError as exc:
        assert "does not descend" in str(exc)
        return
    row = X.grade_ext(cover, inst, recovered, rec, b)
    assert not (row["every_stage_output_equals_rho_H_d"]
                and all(s["every_measured_law_uniform_on_K_perp"] for s in row["stages"].values()))


@pytest.mark.parametrize("key,gens", [("heis5", ()), ("heis5", ((1, 0, 0),)), ("n4_5", ((0, 1, 0, 0),)),
                                      ("n4_5", ((1, 0, 1, 0),))])
def test_multi_state_channel_and_mono_mode_match_round1(key, gens, monkeypatch):
    """Witnesses with several nonzero entries (solved on the nonzero labels), in poly and
    mono mode, against round 1's ExactBackend through to the grade-one readout law."""
    for poly_max in (64, 0):
        monkeypatch.setattr(X, "POLY_MAX_PRIME", poly_max)
        cover, inst, db, sb, dense, sparse = _round1_pair(key, gens)
        assert sb.mono == (poly_max == 0)
        rng = random.Random(11)
        multi = 0
        for d in range(cover.c, 1, -1):
            law = db.label_probabilities(dense)
            assert sb.label_law(sparse).as_dict() == law
            nonzero = [lam for lam, pr in law.items() if pr and any(lam)]
            sched = X.rule_w(cover.p, d, cover.dims[d-1], count="deterministic")
            labels = [rng.choice(nonzero) if nonzero else (0,)*cover.dims[d-1] for _ in range(sched.arity)]
            s = is_sde_solve(cover.p, d, labels).s
            multi += sum(1 for x in s if x) > 1
            dense = db.channel([db.condition(dense, l, law[l]) for l in labels], s)
            sparse = sb.channel([sb.condition(sparse, l) if x else None for l, x in zip(labels, s)], s)
            assert sb.equals_dense(sparse, dense)
        assert multi > 0
        ro = db.readout_probabilities(dense)
        cls = sb.readout_law(sparse)
        m, r = len(next(iter(ro))), len(cls["basis"])
        for k in product(range(cover.p), repeat=m):
            u = tuple(sum(a*b for a, b in zip(k, row)) % cover.p for row in cls["basis"])
            assert ro.get(k, 0) == cls["class_mass"][u]/cover.p**(m-r)
    monkeypatch.setattr(X, "POLY_MAX_PRIME", 64)


def test_parallel_trees_pool_exactly():
    row = X.run_instance_parallel("n4_5", "<e1+e3> non-normal", count="deterministic", workers=2)
    _assert_run(row)
    assert row["readout_samples"] == 8 and row["workers"] == 2
