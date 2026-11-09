"""pytest checks for the 2026-11-05 sub-quadratic SDE pass (fast; about 30 s)."""
import random

from common import F, realizable, check_witness, brute_force_solutions
from circuit_flex import (flexible_lines, make_circuit, check_circuit, contains_plane)
from flexline_structure import contraction_lines, column_lines
from legendre_reduction import (class_table, build_instance, all_solutions_projective,
                                recover_f, reveals_key)


def test_theorem1_one_circuit_one_direction():
    rng = random.Random(1)
    for p, k, q in [(13, 2, 2), (7, 3, 2), (13, 3, 2), (13, 2, 3), (13, 4, 2)]:
        Fd = F(p, k)
        for _ in range(4):
            cols, delta = make_circuit(Fd, rng, q, None)
            r = check_circuit(Fd, cols, delta, q)
            if not r['mono']:
                assert not r['plane'] and r['strong']
            if r['tri'] is not None:
                assert r['tri']


def test_prop2_existence_matches_class_contractions():
    rng = random.Random(2)
    for p, k, q in [(13, 4, 2), (17, 4, 2), (37, 4, 2), (31, 5, 2), (13, 3, 2)]:
        Fd = F(p, k)
        for _ in range(4):
            cols, delta = make_circuit(Fd, rng, q, None)
            if len({Fd.cls(d) for d in delta}) == 1:
                continue
            fl = flexible_lines(Fd, realizable(Fd, cols, q), q)
            cc = contraction_lines(Fd, cols, delta, q)
            assert bool(fl) == bool(cc) and cc <= fl
            if p ** q <= 1400:
                assert fl == column_lines(Fd, cols, delta, q)


def test_all_classes_at_E2_prime_kills_flexibility():
    rng = random.Random(3)
    Fd = F(17, 4)          # 17 in E_2(4)
    for _ in range(3):
        cols, delta = make_circuit(Fd, rng, 3, [0, 1, 2, 3])
        assert not flexible_lines(Fd, realizable(Fd, cols, 3), 3)


def test_kernel_two_objects_can_be_fully_flexible():
    rng = random.Random(4)
    Fd = F(13, 2)
    found = False
    for _ in range(4):
        cols = [[rng.randrange(13) for _ in range(3)] for _ in range(5)]
        if realizable(Fd, cols, 3).all():
            found = True
    assert found


def test_reduction_tiny_exhaustive_and_planted():
    rng = random.Random(5)
    Fd = F(13, 2)
    tab = class_table(Fd)
    for _ in range(4):
        K = rng.randrange(13)
        inst = build_instance(Fd, K, 5, 2, rng)
        if inst[0] == 'key':
            assert inst[1] == K
            continue
        cols, u, c = inst
        ray = lambda x: tuple((v * pow(next(w for w in x if w), 11, 13)) % 13 for v in x)
        assert {ray(x) for x in all_solutions_projective(Fd, cols, tab)} == \
               {ray(x) for x in brute_force_solutions(Fd, cols)}
        assert check_witness(Fd, cols, [(u[i] * (K + c[i])) % 13 for i in range(5)])


def test_reduction_recovers_key_at_moderate_p():
    rng = random.Random(6)
    Fd = F(1009, 2)
    tab = class_table(Fd)
    wins = 0
    for _ in range(10):
        K = rng.randrange(1009)
        inst = build_instance(Fd, K, 18, 2, rng)
        if inst[0] == 'key':
            wins += 1
            continue
        cols, u, c = inst
        sols = all_solutions_projective(Fd, cols, tab)
        wins += all(reveals_key(Fd, recover_f(Fd, x, u, c, 2), K, 2) for x in sols)
    assert wins >= 9
