"""Referee B's SIMPLE5 (research/audits/reviews/2026-11-09-rees-sde-fq-nest-referee-B/simple5.py):
an independent F_5^n solver for {0, +1, -1} zero-sums that uses only Fact F5 and Lemmas 1, 2(A).
At m = guarantee_simple(n) columns it must return a witness on every instance of the eight
families of attack_ref.py (series classes of size 4, 6, 7, PG(2,5) blocks, zero-sum triples,
mixed subspace/random, weight-2 signed, random): nonzero, entries in {0, 1, 4} (= {0, +1, -1}
mod 5), and sum_i x_i lambda_i = 0 mod 5.  Finite check; proves nothing for other n.
The family generators are taken from attack_ref.py itself (its source up to the first timed block).
"""
import os
import sys
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("pycosat")

FOLDER = (Path(__file__).resolve().parents[1] / "research" / "audits" / "reviews"
          / "2026-11-09-rees-sde-fq-nest-referee-B")
NS = (3, 4, 6, 9, 12)


@pytest.fixture(scope="module")
def ns():
    src = (FOLDER / "attack_ref.py").read_text().split("t0 = time.time()")[0]
    old_cwd, old_path = os.getcwd(), list(sys.path)
    os.chdir(FOLDER)                       # attack_ref.py inserts '../2026-11-08-rees-sde-fq-nest'
    sys.path.insert(0, str(FOLDER))
    try:
        space = {"__name__": "attack_ref_defs"}
        exec(compile(src, str(FOLDER / "attack_ref.py"), "exec"), space)
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
    return space


def test_simple5_witnesses_on_all_families_up_to_n12(ns):
    simple5, FAMS, p = ns["simple5"], ns["FAMS"], ns["p"]
    assert len(FAMS) == 8
    runs = 0
    for n in NS:
        m = simple5.guarantee_simple(n)
        for name, make in FAMS.items():
            lam = make(n, m).astype(np.int64)
            assert lam.shape == (n, m), (name, n, lam.shape)
            x = simple5.solve(lam, log=[])
            assert x is not None, f"SIMPLE5 ran out of columns: {name} n={n} m={m}"
            x = np.asarray(x, dtype=np.int64)
            assert x.any(), (name, n)
            assert set(int(v) % p for v in x) <= {0, 1, 4}, (name, n, sorted(set(x.tolist())))
            assert not ((lam @ x) % p).any(), (name, n)
            runs += 1
    assert runs == 8 * len(NS)
