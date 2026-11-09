"""Tests for theorems/rees_circuit_sparse.py (sparse coset-support mode of the
gate-level Rees circuit generator). Fast tests run in a few minutes; the
class-four source from its gate list is slow (REES_SLOW=1)."""
from fractions import Fraction
import os
import random

import numpy as np
import pytest

from theorems.rees_circuit_general import (
    Config, Engine, Hidden, check_instance, heis3_instances, n4_instances, prove_merge, run_algorithm,
    stage_indices,
)
from theorems.rees_circuit_sparse import (
    SPARSE_STATUS, SState, SparseEngine, check_instance_sparse, compare_with_dense, merge_gate_checks,
    n5_instances, run_algorithm_sparse,
)
from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg

slow = pytest.mark.skipif(not os.environ.get("REES_SLOW"), reason="slow; set REES_SLOW=1")


def _strip(row):
    """check_instance row without timings and sparse-only fields."""
    r = {k: v for k, v in row.items() if k not in ("seconds", "source_seconds", "group_order_top")}
    r["source"] = {k: v for k, v in r["source"].items() if k not in ("coset_generators", "chunks")}
    r["grades"] = {d: {k: v for k, v in g.items()
                       if k not in ("state_support", "branch_support_max", "group_order", "target_support")}
                   for d, g in r["grades"].items()}
    return r


@pytest.fixture(scope="module")
def heis():
    cfg = Config(heisenberg(3))
    return cfg, Engine(cfg), SparseEngine(cfg, chunk=16)


@pytest.fixture(scope="module")
def n4():
    cfg = Config(filiform4(5))
    return cfg, Engine(cfg), SparseEngine(cfg, chunk=4096)


@pytest.fixture(scope="module")
def n5():
    cfg = Config(filiform5(5))
    return cfg, SparseEngine(cfg)


def test_status_gates_stay_false():
    for k in ("coherent_receiver_implemented", "general_sde_implemented", "formal_compiler_checked",
              "independent_review", "novelty_established", "speedup_claim_allowed"):
        assert SPARSE_STATUS[k] is False


# ---------------------------------------------------------------- agreement with the dense mode

def test_heis_f3_sparse_equals_dense_all_subgroups(heis):
    cfg, dense, sparse = heis
    insts = heis3_instances()
    assert len(insts) == 19
    for inst in insts:
        r = compare_with_dense(cfg, inst, dense, sparse, merge_cases=120)
        assert r["all_equal"], (inst.name, r)
        rd, rs = check_instance(cfg, inst, dense), check_instance_sparse(cfg, inst, sparse)
        assert _strip(rd) == _strip(rs) and rs["passed"], inst.name
        assert run_algorithm(cfg, inst, dense, seed=11) == run_algorithm_sparse(cfg, inst, sparse, seed=11)


@pytest.mark.parametrize("idx", range(9))          # all 9 n4(F_5) test subgroups, 5 non-normal
def test_n4_f5_sparse_equals_dense(n4, idx):
    cfg, dense, sparse = n4
    inst = n4_instances(5)[idx]
    r = compare_with_dense(cfg, inst, dense, sparse, merge_cases=60)
    assert r["all_equal"], r
    assert r["source_info_equal"] and r["grades"][3]["branches_equal"] and r["grades"][2]["merge_outputs_equal"]
    kw = dict(max_cases=200, sample_tuples=3, max_witnesses=8, seed=idx)
    rs = check_instance_sparse(cfg, inst, sparse, **kw)
    assert _strip(check_instance(cfg, inst, dense, **kw)) == _strip(rs) and rs["passed"]
    assert run_algorithm(cfg, inst, dense, seed=3, extra_samples=1) == \
        run_algorithm_sparse(cfg, inst, sparse, seed=3, extra_samples=1)


def test_n4_f5_check_rows_identical(n4):
    cfg, dense, sparse = n4
    inst = n4_instances(5)[1]                        # <e1> non-normal
    kw = dict(max_cases=200, sample_tuples=3, max_witnesses=8, seed=5)
    rd, rs = check_instance(cfg, inst, dense, **kw), check_instance_sparse(cfg, inst, sparse, **kw)
    assert _strip(rd) == _strip(rs) and rs["passed"]
    assert rs["grades"][3]["state_support"] == 5      # |exp(h~)| = 5 of |G_3| = 78125


def test_chunking_is_irrelevant(n4):
    cfg, _, sparse = n4
    inst = n4_instances(5)[6]                        # <e2,e3> non-normal
    a = sparse.source(inst)
    b = SparseEngine(cfg, chunk=1 << 20).source(inst)
    assert np.array_equal(a[1], b[1]) and a[0].equals_indicator(b[1])
    assert a[2]["chunks"] == 20 and b[2]["chunks"] == 1
    assert {k: v for k, v in a[2].items() if k != "chunks"} == {k: v for k, v in b[2].items() if k != "chunks"}


# ---------------------------------------------------------------- negative controls

def test_dirty_workspace_detected(n4):
    cfg, dense, sparse = n4
    inst = n4_instances(5)[0]
    st, S, info = sparse.source(inst, uncompute=False)
    _, Sd, infod = dense.source(inst, uncompute=False)
    assert not info["workspace_clean"]
    assert {k: v for k, v in info.items() if k in infod} == infod and np.array_equal(S, np.sort(Sd))


def test_two_points_on_class_three_detected(n4):
    cfg, _, sparse = n4
    inst = n4_instances(5)[8]                        # trivial
    st, S, info = sparse.source(inst, points=(1, 2))
    assert info["coset_state"] and len(S) > 1          # identity fibre larger than exp(h~) = {1}
    assert not np.array_equal(S, stage_indices(cfg, inst.log_h, cfg.c))


def test_non_witness_does_not_give_rho(n4):
    cfg, _, sparse = n4
    inst = n4_instances(5)[1]                        # <e1>, grade-3 labels in F_5
    st, _, _ = sparse.source(inst)
    _, br = sparse.label_law(st)
    target = stage_indices(cfg, inst.log_h, 2)
    for s in [(1, 1), (1, 2), (2, 2)]:              # labels (1, 2): 1*s1^3 + 2*s2^3 != 0
        try:
            out = sparse.merge([br[(1,)], br[(2,)]], s)
        except ArithmeticError:
            continue
        assert not out.equals_indicator(target)


def test_merge_descent_failure_raises(n4):
    cfg, _, sparse = n4
    p = cfg.p
    # a state supported on one non-central point of G_3 cannot descend
    bad = SState(3, Fraction(1), np.array([0, 7], dtype=np.int64), np.eye(1, p, 0, dtype=np.int64).repeat(2, 0))
    with pytest.raises(ArithmeticError):
        sparse.merge([bad, bad], (1, 1))


# ---------------------------------------------------------------- class four (n5 over F_5)

def test_n5_merges_proved_all_grades(n5):
    cfg, _ = n5
    assert cfg.c == 4 and cfg.dims == (5, 3, 2, 1) and cfg.laws[4].order == 5**11
    for d in (2, 3, 4):
        for s in range(1, 5):
            assert prove_merge(cfg, d, s)["proved"], (d, s)


def test_n5_merge_bitlevel_sampled(n5):
    cfg, _ = n5
    res = merge_gate_checks(Config(filiform5(5), arities=None), rows=2, xs=256)
    assert all(v["proof"]["proved"] for v in res.values())
    assert all(all(x for k, x in v["bitlevel_sampled"].items() if k != "inputs") for v in res.values())


def test_n5_downstream_from_rho_lift(n5):
    """Class four downstream of the source: starting from rho_(exp h~) (the state the
    slow test obtains from the source gate list), label laws uniform on K_d^perp,
    sampled merges equal rho_(H_(d-1)), readout gives log H; non-normal subgroup."""
    cfg, sparse = n5
    inst = n5_instances(5, ["<e2,e5> non-normal"])[0]
    assert not inst.normal
    S = stage_indices(cfg, inst.log_h, cfg.c)
    V = np.zeros((len(S), cfg.p), dtype=np.int64)
    V[:, 0] = 1
    src = (SState(cfg.c, Fraction(1), np.sort(S).astype(np.int64), V), S,
           {"coset_state": True, "workspace_clean": True})
    row = check_instance_sparse(cfg, inst, sparse, source=src, max_cases=300, sample_tuples=3, max_witnesses=6)
    assert row["passed"], row
    assert all(g["label_law_uniform_on_K_perp"] and g["merge_outputs_equal_rho_H"] for g in row["grades"].values())
    got, info = run_algorithm_sparse(cfg, inst, sparse, seed=1, extra_samples=1, top=src[0])
    assert info["recovered"] and info["oracle_queries"] == 4*105*6


@slow
def test_n5_source_from_gates_slow(n5):
    cfg, sparse = n5
    inst = n5_instances(5, ["<e1> non-normal"])[0]
    st, S, info = sparse.source(inst)
    assert info["coset_state"] and info["workspace_clean"]
    assert np.array_equal(S, stage_indices(cfg, inst.log_h, cfg.c))
    row = check_instance_sparse(cfg, inst, sparse, source=(st, S, info), max_cases=300, sample_tuples=3,
                                max_witnesses=6)
    assert row["passed"]
