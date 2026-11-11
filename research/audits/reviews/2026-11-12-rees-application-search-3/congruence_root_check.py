"""Lemma N3: if (n-1)! * N' divides M, every g in Gamma(M) = ker(UT_n(Z) -> UT_n(Z/M))
is the N'-th power of an element of UT_n(Z). Exact rational arithmetic.
Also records that (n-1)! cannot simply be dropped: a control with M = N' finds
non-integral roots. Finite check only (TRAPS 7).
Run: /opt/anaconda3/bin/python -I congruence_root_check.py
"""
import random
from fractions import Fraction
from math import factorial

def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def mat_add(A, B, c=1):
    return [[A[i][j] + c * B[i][j] for j in range(len(A))] for i in range(len(A))]

def ident(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]

def mat_log_unipotent(g):
    n = len(g); N = mat_add(g, ident(n), -1); res = [[Fraction(0)] * n for _ in range(n)]
    P = ident(n)
    for k in range(1, n):
        P = mat_mul(P, N)
        res = mat_add(res, P, Fraction((-1) ** (k + 1), k))
    return res

def mat_exp_nilpotent(X):
    n = len(X); res = ident(n); P = ident(n)
    for j in range(1, n):
        P = mat_mul(P, X)
        res = mat_add(res, P, Fraction(1, factorial(j)))
    return res

def mat_pow(A, e):
    n = len(A); R = ident(n)
    for _ in range(e):
        R = mat_mul(R, A)
    return R

def trial(n, Np, M, rng):
    X = [[Fraction(rng.randrange(-5, 6)) if j > i else Fraction(0) for j in range(n)] for i in range(n)]
    g = mat_add(ident(n), X, M)
    L = mat_log_unipotent(g)
    Y = mat_exp_nilpotent([[x / Np for x in row] for row in L])
    integral = all(y.denominator == 1 for row in Y for y in row)
    return integral, mat_pow(Y, Np) == g

rng = random.Random(20261112)
for n in (3, 4, 5, 6):
    D = factorial(n - 1)
    bad = 0; ctrl_nonint = 0
    for _ in range(60):
        Np = rng.choice([2, 3, 4, 5, 6, 7, 9, 12])
        ok_int, ok_pow = trial(n, Np, D * Np * rng.choice([1, 2, 5]), rng)
        bad += (not ok_int) or (not ok_pow)
        c_int, _ = trial(n, Np, Np, rng)
        ctrl_nonint += (not c_int)
    print(f"n={n}: M=(n-1)!N'k: failures {bad}/60;  control M=N': non-integral roots {ctrl_nonint}/60")
