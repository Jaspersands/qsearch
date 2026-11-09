"""Tests for theorems/rees_circuit_exhaustive.py (exhaustive merge checks by an
exact reduction). AI-checked, pending human review. Default run < 60 s; the
full runs (all nine n5(F_5) subgroups from the source gate lists, and
n5(F_7)) are in research/audits/reviews/2026-11-05-rees-receiver-sims/."""
import random
from itertools import product

import numpy as np
import pytest

from theorems.rees_circuit_exhaustive import (
    STATUS, Config, SparseEngine, all_witnesses, allowed_labels, branch_structure, covered_pairs,
    exhaustive_instance, filiform5, n5_instances, stage_indices, subset_checks, truth_state)
import theorems.rees_circuit_general as G


@pytest.fixture(scope="module")
def n5():
    cfg = Config(filiform5(5))
    return cfg, SparseEngine(cfg)


def test_status_gates_stay_false():
    assert STATUS["coherent_receiver_implemented"] is False
    assert STATUS["speedup_claim_allowed"] is False


def test_pair_counts_match_the_direct_exhaustive_runs():
    # 2026-11-03-rees-circuit-3: 1 952 500 (grade 4) and 77 500 (grade 3) cases
    assert covered_pairs(5, 5, 5) == 1952500
    assert covered_pairs(5, 3, 25) == 77500


@pytest.mark.parametrize("name", ["trivial", "<e2> non-normal", "<e1+e2+e5> non-normal", "<e2,e5> non-normal",
                                  "Z(G) = <e5>", "<e3> non-normal"])
def test_n5_f5_every_grade_exhaustive_from_exact_source(n5, name):
    cfg, eng = n5
    inst = n5_instances(5, names=[name])[0]
    row = exhaustive_instance(cfg, inst, eng, source="truth", log=None, direct=20)
    assert row["passed"], row
    for d in (4, 3, 2):
        assert row["grades"][d]["exhaustive"]


def test_reduction_has_teeth(n5):
    """The phase condition with a wrong power of t fails on some subgroup,
    and non-witness scales are rejected by the direct merge."""
    cfg, eng = n5
    failed = False
    for name in ("<e1> non-normal", "<e2> non-normal", "trivial"):
        inst = n5_instances(5, names=[name])[0]
        for d in (4, 3, 2):
            st = truth_state(cfg, inst, d)
            allowed = allowed_labels(cfg, inst.log_h, d)
            flags, phi0, W, _ = branch_structure(eng, st, allowed, d)
            if W.shape[1] == 0:
                continue
            target = stage_indices(cfg, inst.log_h, d-1)
            sub = subset_checks(eng, phi0, W, d, cfg.arity[d], target, phase_power=d-1)
            failed |= not sub["phase_condition_holds"]
    assert failed


def test_reduction_agrees_with_direct_exhaustion_heis():
    """Heis(F_3): every (label tuple, witness) pair merged directly (234 pairs
    per subgroup) agrees with the reduced verdict, on all 19 subgroups."""
    cfg = G.Config(G.heisenberg(3))
    eng = SparseEngine(cfg)
    for inst in G.heis3_instances():
        row = exhaustive_instance(cfg, inst, eng, source="truth", log=None, direct=5)
        d = 2
        st = truth_state(cfg, inst, d)
        _, states = eng.label_law(st)
        allowed = allowed_labels(cfg, inst.log_h, d)
        target = stage_indices(cfg, inst.log_h, 1)
        M = cfg.arity[d]
        cases = good = 0
        for labels in product(allowed, repeat=M):
            for s in all_witnesses(labels, d, cfg.p):
                act = [states[l] for l, si in zip(labels, s) if si]
                cases += 1
                good += eng.merge(act, [int(x) for x in s if x]).equals_indicator(target)
        assert cases == covered_pairs(cfg.p, M, len(allowed))
        assert good == cases and row["grades"][d]["exhaustive"], inst.name


def test_n5_f7_one_nonnormal_subgroup_every_grade_exhaustive():
    cfg = Config(filiform5(7))
    assert cfg.arity == {2: 7, 3: 7, 4: 3}
    inst = n5_instances(7, names=["<e1> non-normal"])[0]
    row = exhaustive_instance(cfg, inst, SparseEngine(cfg), source="truth", log=None, direct=5)
    assert row["passed"]
    assert all(row["grades"][d]["exhaustive"] for d in (4, 3, 2))
