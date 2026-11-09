"""Fast tests for hcheck.py (h = 3: p = 7, 13, 19, 31; h = 4: p = 13, 17).

Run: /opt/anaconda3/bin/python -m pytest -q research/audits/reviews/2026-11-05-rees-s3-witness-h3-check/test_hcheck.py
"""
import os
import random
import sys
from fractions import Fraction as Fr
from math import gcd

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import hcheck as H  # noqa: E402

CASES = [(3, 7, 1), (3, 13, 1), (3, 19, 2), (3, 31, 2), (4, 13, 1), (4, 17, 2)]


@pytest.mark.parametrize("h,p,J", CASES)
def test_depth_values(h, p, J):
    assert H.jstar(p, h) == J
    assert H.chain(p, h, method="bits")[1] == H.chain(p, h, method="fft")[1]


@pytest.mark.parametrize("h,p,J", CASES)
def test_solver_exact_outputs(h, p, J):
    rng = random.Random(p * 10 + h)
    smp = H.Sampler(p, h, rng)
    for n in (1, 2, 4):
        for _ in range(5):
            src = H.Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
            res = smp.run(src, n)
            assert H.check_output(res, src.cols, p, smp.D[0], [0] * n)
            assert all(w in H.mu_set(p, h) for w in res.values())
    for j in range(smp.J):
        src = H.Source(gen=lambda: [rng.randrange(p) for _ in range(3)])
        y = [rng.randrange(p) for _ in range(3)]
        assert H.check_output(smp.A(j, 3, y, src), src.cols, p, smp.D[j], y)


def test_exact_s_p_and_degree():
    assert H.s_p_exact(7) == Fr(1127, 243)
    assert H.s_p_exact(13) == Fr(4154499115, 725594112)
    N = H.N_table(2, Fr(3), 6)
    # N_1(d) = 1 + 3 d(d+1)/2, N_0 has degree 3 with leading coefficient 9/6
    assert [N[1][d] for d in range(4)] == [1, 4, 10, 19]
    assert N[0][1] == 1 + 3 * N[1][0]


@pytest.mark.parametrize("p,d", [(7, 2), (13, 4), (19, 6), (31, 10), (13, 3), (17, 4)])
def test_node_never_wrong(p, d):
    rng = random.Random(p + d)
    k = gcd(d, p - 1)
    smp = H.Sampler(p, (p - 1) // k, rng)
    for _ in range(4):
        st, _, _ = H.node(p, d, 3 if smp.J == 1 else 2, rng.randint(0, 2), Fr(1, 2), rng, smp=smp)
        assert st in ("ok", "abort")


def test_negative_control_broken_table():
    rng = random.Random(1)
    smp = H.Sampler(13, 3, rng, broken=True)
    bad = 0
    for _ in range(10):
        src = H.Source(gen=lambda: [rng.randrange(13) for _ in range(4)])
        bad += not H.check_output(smp.run(src, 4), src.cols, 13, smp.D[0], [0] * 4)
    assert bad > 0
