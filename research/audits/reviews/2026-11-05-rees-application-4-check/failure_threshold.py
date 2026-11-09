"""Where does the Lie test of Theorem W actually start to fail?
For L in {n3 (nu=3), heis4 (nu=4)}, plain forms Q of degree <= delta in D
variables (levels = 1, so the p-weight equals delta and F = Q), and random
B in L (conjugated), search by exact linear algebra for
  under:  Q o exp(B) == Q  but  Lie derivative D_B Q != 0,
  over:   D_B Q == 0       but  Q o exp(B) != Q.
By Theorem W(a) neither exists when p > max((nu-1)delta, 2 delta).
Reports, for each p, the smallest delta tried at which a witness exists.
Run: nice -n 10 /opt/anaconda3/envs/qsearch-cas/bin/python failure_threshold.py"""
import sys, time
sys.path.insert(0, '.')
from check_theorem_w import (Planted, algebra, conj_UT, mexp, GF,
                             identity_matrix, set_random_seed)
import random
set_random_seed(71105)
random.seed(int(71105))
T0 = time.time()
for alg, nu in (('n3', 3), ('heis4', 4)):
    for p in (5, 7, 11, 13):
        Fp = GF(p)
        start = max(1, (p - 1) // max(nu - 1, 2))  # last delta inside the guard
        for delta in range(start, p):
            if time.time() - T0 > 900:
                print('time budget reached'); sys.exit(0)
            D, L = algebra(alg, p)
            L = conj_UT(L, p)
            PL = Planted(p, D, delta, 1)
            n = len(PL.mons)
            I = identity_matrix(Fp, n)
            res = {'under': False, 'over': False}
            for _ in range(4):
                B = sum(Fp.random_element() * b for b in L)
                if B == 0:
                    continue
                KI = (PL.subst_matrix(mexp(B)) - I).right_kernel()
                KJ = PL.lie_matrix(B).right_kernel()
                if not KI.is_subspace(KJ):
                    res['under'] = True
                if not KJ.is_subspace(KI):
                    res['over'] = True
                if res['under'] and res['over']:
                    break
            inside = p > max((nu - 1) * delta, 2 * delta)
            print('%-5s p=%-2d delta=%-2d inside_guard=%-5s (nu-1)delta=%-2d under=%s over=%s  [%.0fs]'
                  % (alg, p, delta, inside, (nu - 1) * delta, res['under'], res['over'], time.time() - T0))
            sys.stdout.flush()
            if inside and (res['under'] or res['over']):
                print('!!! COUNTEREXAMPLE INSIDE THE GUARD')
            if res['under'] and res['over']:
                break
print('total %.0f s' % (time.time() - T0))
