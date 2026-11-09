"""Restart counts of the IS classifier at composite kappa (2026-11-05 composite note).

Report: research/audits/reviews/2026-11-05-rees-is-restarts-composite.md.
Code: research/audits/reviews/2026-11-05-rees-is-restarts-composite/composite_restarts.py.
"""
import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
_PATH = ROOT/"research/audits/reviews/2026-11-05-rees-is-restarts-composite/composite_restarts.py"
_spec = importlib.util.spec_from_file_location("composite_restarts", _PATH)
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)


def _omega(n):
    count, f = 0, 2
    while n > 1:
        while n % f == 0:
            n //= f
            count += 1
        f += 1
    return count


def test_rho_closed_forms():
    for kappa, p in cr.family_cases():
        data = cr.nus(p, kappa)
        r = cr.rho(p, kappa)
        assert r == max(cr.rho_star(p, kappa, ell) for ell in data)
        assert r == cr.rho_star(p, kappa, cr.best_ell_star(p, kappa))
        assert 1+max(n for n, _ in data.values()) <= r <= cr.nu(p, kappa)
    for p, kappa in ((65537, 2), (65537, 8), (1459, 9), (12289, 4), (4723921, 5)):
        assert cr.rho(p, kappa) == _omega(kappa)      # prime power: Lemma 1(ii) of the 11-05 note


def test_lattice_maximum_equals_closed_form():
    # every anchor (g, 1), and (g, h, 1) when n_pi <= 60; exact longest failing chain
    assert cr.sweep_lattice(kappas=(6, 10, 12, 15, 30), pmax=400, verbose=False) > 10000


@pytest.mark.parametrize("p,kappa,a", [(65537, 2, 3), (786433, 2, 3), (7681, 2, 2),
                                       (1459, 3, 1), (39367, 3, 2), (17, 4, 1), (97, 4, 1)])
def test_family_a_full_solver_prime_power(p, kappa, a):
    pre = cr.family_a(p, kappa, a, cr.best_ell_star(p, kappa))
    out = cr.cross_check(p, kappa, pre, a)
    assert out[False][0] == cr.nu(p, kappa)                # default: exactly nu+1 runs
    assert out[True][0]+1 == cr.rho(p, kappa) == _omega(kappa)   # variant: exactly e runs


@pytest.mark.parametrize("p", [163, 1459, 39367])
def test_family_b_full_solver_kappa3(p):
    pre = cr.family_b(p, 3, 3, 18)                          # 18 level-2 nodes = G(3, 1) columns
    out = cr.cross_check(p, 3, pre, 1)
    assert out[True] == (0, True, 1)


@pytest.mark.parametrize("kappa,exps", [(6, {2: 10, 3: 1}), (6, {2: 4, 3: 6}),
                                        (10, {2: 2, 5: 12}), (12, {2: 12, 3: 1}),
                                        (12, {2: 9, 3: 4}), (15, {3: 1, 5: 9}),
                                        (30, {2: 8, 3: 3, 5: 2})])
def test_families_composite(kappa, exps):
    p = cr.find_prime(kappa, exps)
    res = cr.check_family(kappa, p, verbose=False)        # asserts exact counts internally
    assert res[("A", False)] == (cr.rho(p, kappa), cr.nu(p, kappa)+1)
    assert res["B"] == cr.rho(p, kappa)
    star = cr.best_ell_star(p, kappa)
    pre = cr.family_c(p, kappa, 1, star, 3)
    assert cr.prefix_run(p, kappa, pre, collapse=True, level=3)["runs"] == cr.rho(p, kappa)
    assert cr.prefix_run(p, kappa, pre, collapse=False, level=3)["runs"] >= cr.rho(p, kappa)+1


def test_every_l_star_gives_its_count():
    assert cr.every_ell_star(verbose=False) == {2: 6, 3: 11, 5: 12}


def test_family_c_crosses_level4_spine():
    # nu = 76 > 70 slots of the first level-3 node: the chain continues after the copy child
    p = cr.find_prime(6, {2: 75, 3: 1})
    pre = cr.family_c(p, 6, 1, 3, 4, children=3)
    v = cr.prefix_run(p, 6, pre, collapse=True, level=3)
    assert v["runs"] == cr.rho(p, 6) == 76 and not v["collapsed"]
    assert cr.prefix_run(p, 6, pre, collapse=False, level=3)["runs"] == 77   # nu+1


def test_slot_counts():
    assert cr.family_c_slots(6, 1, 3) == 70
    assert cr.family_c_slots(6, 1, 6) == 70*431*2591*15551 > 10**12
    assert cr.family_a_slots(6, 3) == 69
