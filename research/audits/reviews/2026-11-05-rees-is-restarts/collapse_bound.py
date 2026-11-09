"""Explicit field-operation bound for the collapse variant, vs instrumented counts.

Run: nice -n 10 /opt/anaconda3/bin/python -O collapse_bound.py
Reuses research/audits/reviews/2026-11-04-rees-is-runtime/{is_count,is_bound}.py.
"""
import math
import random
import sys

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-is-runtime")
import is_count as C  # noqa: E402  (patches the solver module for counting)
import is_bound as B  # noqa: E402
S = C.S


def omega_mult(n):
    out, f = 0, 2
    while n > 1:
        while n % f == 0:
            n //= f
            out += 1
        f += 1
    return out


def prime_power(k):
    return len(S._prime_divisors(k)) == 1


def F_new(p, d, a):
    """Bound for collapse=True at prime-power kappa: R = Omega(kappa) runs."""
    b = p.bit_length()
    k, t = S.reduced_degree(p, d)
    assert k > 1 and prime_power(k)
    nu, w = C.nu(p, k), B.omega(k)
    e = omega_mult(k)
    G = S.collision_arity(k, a)
    L = B.clog(len(S.zero_sum_of_powers(p, k)))
    N = G ** L
    I = G * (G ** L - 1) // (G - 1)
    Lam, Phi, Th = B.per_input(k, a)
    ccls = B.C_cls(b, nu, k)
    from fractions import Fraction
    IN = float(Fraction(I, N))
    run_per_N = IN * (Lam + Phi + Th * ccls) + (L + 1)
    run = I * (Lam + Phi + Th * ccls) + (L + 1) * N if N < 10**250 else float('inf')
    join = w * (4 * b + 4 * b * (nu + w) + 1)
    anchor_pre = (a * a * (a + 1) + a) + (a + 1) * (4 * b + join)
    anchor_test = 2 * b * (nu + w) + (a + 1) * (ccls + 4 * b + 1)
    triggers = e                       # at most e triggers (e-1 restarts + 1 collapse)
    bez = 0 if t == 1 else N * (2 * B.clog(t + 1))
    Z = B.Z_bound(k, b, nu)
    total = e * run + triggers * (join + ccls) + anchor_pre + (triggers + 1) * anchor_test + Z + bez
    main = e * run + triggers * (join + ccls) + anchor_pre + (triggers + 1) * anchor_test + bez
    main_per_N = e * run_per_N + (triggers * (join + ccls) + anchor_pre + (triggers + 1) * anchor_test) / N \
        + (0 if t == 1 else 2 * B.clog(t + 1))
    return total, dict(b=b, k=k, e=e, nu=nu, N=N, run=run, Z=Z, main=main, main_per_N=main_per_N)


def measured(p, d, a, seed, early_exit, spread=False, cols=None):
    rnd = random.Random(seed)
    need = S.columns_required(p, d, a)
    if cols is None:
        cols = [tuple(rnd.randrange(1, p) for _ in range(a)) for _ in range(need)]
    C.reset()
    C.P[0] = p
    w = S.is_sde_solve(p, d, cols, early_exit=early_exit, spread=spread, collapse=True)
    assert S.verify(p, d, cols, w.s)
    mult = sum(v for f, v in C.MUL.items() if f not in C.EXCLUDE)
    pm = sum(C.pow_mults(v)[0] for f, v in C.POWS.items() if f not in C.EXCLUDE)
    inv = sum(C.pow_mults(v)[1] for f, v in C.POWS.items() if f not in C.EXCLUDE)
    other = sum(v for f, v in C.OTHERPOW.items()
                if f not in C.EXCLUDE and f not in ("__init__", "is_sde_solve", "reduced_degree"))
    return w, mult + pm + inv + other


if __name__ == "__main__":
    print("1. instrumented collapse runs vs F_new")
    worst = 0
    cases = [(7, 2, 1), (13, 2, 1), (97, 2, 1), (257, 2, 1), (65537, 2, 1), (13, 2, 2),
             (97, 2, 2), (65537, 2, 2), (536870951, 2, 2), (7, 3, 1), (19, 3, 1), (163, 3, 1),
             (163, 3, 2), (536871001, 3, 2)]
    for p, d, a in cases:
        for ee in (False, True):
            for seed in range(3):
                w, m = measured(p, d, a, seed, ee, spread=bool(seed % 2))
                bound, info = F_new(p, d, a)
                worst = max(worst, m / bound)
                if not m <= bound:
                    raise SystemExit(f"F_new FAILED {(p, d, a, ee, seed, m, bound)}")
                if w.restarts > info["e"] - 1:
                    raise SystemExit(f"restart bound FAILED {(p, d, a, ee, seed, w.restarts)}")
    print("   all within F_new; max measured/F_new =", round(worst, 3))

    print("2. simple forms on a grid (no runs), prime-power kappa only")
    sup_main = sup_Z = 0
    big_Z = [0, None]
    for p in (3, 5, 7, 13, 17, 97, 257, 65537, 786433, 536870951, 536871001, 2**61 - 1,
              29 * 2**57 + 1, 2**127 - 1):
        if not S.fmpz(p).is_prime():
            continue
        for d in (2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 25, 27, 32):
            k, _ = S.reduced_degree(p, d)
            if k == 1 or not prime_power(k):
                continue
            for a in (1, 2, 3, 5, 10, 50, 200, 1000):
                total, info = F_new(p, d, a)
                b, N, e = info["b"], info["N"], info["e"]
                vm = info["main_per_N"] / (k ** 3 * e * (a * a + b * b))
                vz = info["Z"] / (k ** 3 * b ** 3)
                if vm > sup_main:
                    sup_main, arg_m = vm, (p, d, a)
                if vz > sup_Z:
                    sup_Z, arg_z = vz, (p, d)
                if b >= 8 and vz > big_Z[0]:
                    big_Z[:] = [vz, (p, d)]
    print(f"   sup main/(k^3 e N (a^2+b^2)) = {sup_main:.3f} at {arg_m}")
    print(f"   sup Z/(k^3 b^3)              = {sup_Z:.3f} at {arg_z}")
    print(f"   sup Z/(k^3 b^3) over b >= 8   = {big_Z[0]:.3f} at {big_Z[1]}")
    ok = sup_main <= 4 and sup_Z <= 60
    print("   simple form F_new <= 4 k^3 Omega(k) N (a^2+b^2) + 60 k^3 b^3:", "OK" if ok else "FAILS")
    if not ok:
        raise SystemExit(1)
