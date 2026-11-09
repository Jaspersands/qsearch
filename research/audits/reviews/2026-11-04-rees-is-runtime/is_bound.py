"""Explicit field-operation bound for the IS solver vs instrumented counts.
Run: /opt/anaconda3/bin/python -O is_bound.py
"""
import math
import random
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import is_count as C  # noqa: E402
S = C.S

clog = lambda n: (n - 1).bit_length()  # ceil(log2 n)


def Bl(k, a, l):
    return k ** (l * (l - 1) // 2) * (a + 1) ** l


def per_input(k, a):
    """Lambda (Gaussian elimination), Phi (combination), Theta (classifications) per input vector."""
    Lam = Phi = Th = 0.0
    for l in range(1, k + 1):
        R, E, B = k ** (l - 1) * a, k ** (l - 1) * (a + 1), Bl(k, a, l)
        Lam += (R * R * E + R) / B
        Phi += (E * (k ** (l - 1) * a + 6 * k.bit_length() + 7) + B) / B
        Th += E / B
    return Lam, Phi, Th


def omega(k):
    return len(S._prime_divisors(k)) if k > 1 else 0


def C_cls(b, nu, k):
    """split 4b + dlog [2b + w(6b + 2k*bitlen k) + nu(4b+1) + nu inversions + (w+1) integer
    inversions for the CRT] + rest_root 2b + beta 2b + 1."""
    w = omega(k)
    return (10 + 6 * w + 4 * nu) * b + 2 * w * k * k.bit_length() + 2 * nu + w + 2


def Z_bound(k, b, nu):
    """van de Woestijne Section 6.1 reduction on -1 = (p-1)*1^k with the substitute SRE."""
    if k % 2:
        return 0
    w = omega(k)
    rounds = math.ceil((k + 1) * math.log(2) * b) + k + 2
    runs = 1 + k * rounds
    order = 2 * b * (nu + w)
    join = w * (4 * b + 2 * order)
    dlog = C_cls(b, nu, k)
    sre = (k + 1) * (4 * b + join + dlog + 2 * b) + 4 * b
    return rounds * (runs * (2 * clog(k) + 4) + sre)


def F_bound(p, d, a, M, g=None):
    """Explicit bound on field mults+inversions (no verification), RAM model."""
    g = g or a
    b = p.bit_length()
    k, t = S.reduced_degree(p, d)
    pre = a * g * M + a                      # optional row reduction (_row_reduce)
    if k == 1:
        bez = (a + 1) * 2 * clog(t + 1)
        return pre + (a * a * (a + 1) + a) + bez, dict(b=b, k=k)
    nu = C.nu(p, k)
    G = S.collision_arity(k, a)
    L = clog(len(S.zero_sum_of_powers(p, k)))
    N = G ** L
    I = G * (G ** L - 1) // (G - 1)
    Lam, Phi, Th = per_input(k, a)
    run = I * (Lam + Phi + Th * C_cls(b, nu, k)) + (L + 1) * N
    restart = nu * (omega(k) * (4 * b + 4 * b * (nu + omega(k)) + 1) + C_cls(b, nu, k))
    bez = 0 if t == 1 else N * (2 * clog(t + 1))
    total = pre + (nu + 1) * run + restart + Z_bound(k, b, nu) + bez
    simple = 40 * k ** 3 * N * b * (a * a + b * b) + a * g * M + a
    return total, dict(b=b, k=k, nu=nu, G=G, L=L, N=N, I=I, Lam=Lam, Phi=Phi, Th=Th,
                       run=run, Z=Z_bound(k, b, nu), bez=bez, simple=simple)


def measured(p, d, a, early_exit, seed=0, spread=False):
    rnd = random.Random(seed)
    need = S.columns_required(p, d, a)
    cols = [tuple(rnd.randrange(1, p) for _ in range(a)) for _ in range(need)]
    r = C.run(p, d, a, cols=cols, early_exit=early_exit, spread=spread)
    adds = sum(v for f, v in C.ADD.items() if f not in C.EXCLUDE)
    other = sum(v for f, v in C.OTHERPOW.items() if f not in C.EXCLUDE and f not in ("__init__", "is_sde_solve", "reduced_degree"))
    return r, r["mult_alg"] + r["pow_mult_alg"] + r["inv_alg"] + other, adds


if __name__ == "__main__":
    print("sup over grid of (Lambda - a^2 - k^2 a)/k^3 and of Phi/(a+k):")
    for k in range(2, 9):
        vals = [per_input(k, a) for a in range(1, 400)]
        print(f"  k={k}: max (Lam-a^2-k^2a)/k^3 = {max((v[0]-a*a-k*k*a)/k**3 for a, v in zip(range(1, 400), vals)):.3f}"
              f"  max Phi/(a+2k+4clog k+5) = {max(v[1]/(a+2*k+4*clog(k)+5) for a, v in zip(range(1,400), vals)):.3f}"
              f"  max Theta = {max(v[2] for v in vals):.3f}")
    print()
    cases = [(7, 2, 1), (13, 2, 1), (97, 2, 1), (257, 2, 1), (65537, 2, 1), (7, 2, 2), (13, 2, 2),
             (97, 2, 2), (65537, 2, 2), (536870951, 2, 2), (536871001, 2, 2),
             (7, 3, 1), (13, 3, 1), (163, 3, 1), (163, 3, 2), (19, 3, 2), (536871001, 3, 2),
             (5, 3, 2), (11, 3, 1), (101, 3, 2)]
    worst = 0
    print(f"{'p':>10} d k a  N    b  nu L rst  ee | measured(mul+pow+inv)  adds | explicit bound  simple 40k^3Nb(a^2+b^2)+agM+a | ratio")
    for p, d, a in cases:
        for ee in (False, True):
            r, m, adds = measured(p, d, a, ee)
            bound, info = F_bound(p, d, a, r["M"])
            simple = info.get("simple", bound)
            worst = max(worst, m / bound)
            print(f"{p:>10} {d} {r['kappa']} {a} {r['M']:>4} {info['b']:>3} {r['nu']:>3} {r['L']} {r['restarts']:>3} {int(ee):>3} |"
                  f" {m:>12} {adds:>8} | {bound:>14.0f} {simple:>14.0f} | {m/bound:.3f}")
            if not (m <= bound and bound <= simple and adds <= m):
                raise SystemExit(f"CHECK FAILED {(p, d, a, ee, m, bound, simple, adds)}")
    print("max measured/explicit =", round(worst, 3))
    print()
    print("restart stress: spread kernel, seeds 0..7, early_exit=False")
    for p, d, a in ((65537, 2, 1), (257, 2, 2), (163, 3, 1), (2**16 * 3 + 1 if S.fmpz(2**16*3+1).is_prime() else 786433, 2, 1)):
        rs = [measured(p, d, a, False, seed=s, spread=True) for s in range(8)]
        r, m, adds = max(rs, key=lambda x: x[0]["restarts"])
        bound, info = F_bound(p, d, a, r["M"])
        print(f"  p={p} d={d} a={a}: max restarts {r['restarts']} (nu={r['nu']}), measured {m} <= bound {bound:.0f}")
        if not (r["restarts"] <= r["nu"] and m <= bound):
            raise SystemExit("restart check failed")
    print()
    print("explicit bound vs simple form 40 k^3 N b (a^2+b^2) + a g M on a grid (no runs):")
    bad = 0
    for p in (3, 5, 7, 13, 17, 97, 257, 65537, 786433, 536870951, 536871001, 2**61 - 1, 29 * 2**57 + 1):
        if not S.fmpz(p).is_prime():
            continue
        for d in (2, 3, 4, 6):
            for a in (1, 2, 3, 5, 10, 50, 200):
                bound, info = F_bound(p, d, a, S.is_arity(d, a))
                if info["k"] > 1 and bound > info["simple"]:
                    bad += 1
                    print("   simple form fails:", p, d, a, bound, info["simple"])
    print("  simple-form failures:", bad)
    worst = 0
    for p in (3, 5, 7, 13, 17, 97, 257, 65537, 786433, 536870951, 536871001, 2**61 - 1, 29 * 2**57 + 1, 2**127 - 1):
        for d in range(2, 9):
            for a in (1, 2, 3, 5, 10, 50, 200, 1000):
                bound, info = F_bound(p, d, a, 0)
                if info["k"] > 1:
                    key = (p, d, a)
                    val = (bound - a) / (info["k"] ** 3 * info["N"] * info["b"] * (a * a + info["b"] ** 2))
                    if val > worst:
                        worst, arg = val, key
    print("  sup of (F_total - agM - a) / (k^3 N b (a^2+b^2)) on the grid:", round(worst, 3), "at", arg)

