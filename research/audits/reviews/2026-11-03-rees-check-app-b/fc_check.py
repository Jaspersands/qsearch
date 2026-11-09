"""Independent exact checks of appendix-free-coordinate.tex (snapshot sha1 39591e85, 2 Nov 21:40).

[F1] Lemma fc-rref(b): for every small (p, a, M), over all a x M matrices X, conditional on the
     rank and pivot pattern, the block R[:, F'] after the last pivot is exactly uniform.
[F2] Lemma fc-rref(c), fc-node(a)-(b),(d) and Prop rc-lower's mean identity, by enumerating every
     bank: Pr[not good] <= beta(M, n0; a); acceptance on good banks >= q^r/2; every accepted
     candidate gives y in ker X with y != 0; uniform-kernel mean over generic banks
     = (q^n - p^-n) q^a.
[F3] Lemma fc-moment: E N, Var N = h^{n+1}(q^r - q^{2r}) and Chebyshev, exactly.
[F4] Lemma fc-params closed forms and tree sum, Prop fc-uniform(a) node bound, u = 2..UMAX.
[F5] Lemma fc-choice: beta(M_d, n0; g) <= tau exactly for many (p, kappa, g, tau); the size
     display is compared in floating point (float check, labelled as such).
[F6] The p = 5 example after Prop rc-lower.

Run: /opt/anaconda3/bin/python -I fc_check.py
"""
import itertools
import math
from collections import Counter, defaultdict
from fractions import Fraction as Fr

fails = []


def rref(X, p):
    A = [list(r) for r in X]
    rows = len(A)
    cols = len(A[0]) if rows else 0
    piv, r = [], 0
    for c in range(cols):
        k = next((i for i in range(r, rows) if A[i][c] % p), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    return A[:r], piv


def beta(p, kappa, M, n0, a):
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    L = M - n0
    return Fr(4) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** L)


# [F1], [F2]
for (p, kappa, a, M, n0) in [(5, 2, 1, 4, 2), (5, 2, 2, 4, 1), (7, 3, 1, 4, 2), (7, 2, 2, 3, 1),
                             (5, 1, 2, 3, 1), (11, 5, 1, 3, 2), (13, 4, 1, 4, 2), (3, 1, 2, 4, 2)]:
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    P = sorted({pow(x, kappa, p) for x in range(1, p)})
    D = set(P) | {0}
    blocks = defaultdict(Counter)
    total = p ** (a * M)
    bad = 0
    gen_count = 0
    gen_acc_sum = Fr(0)
    worst = None
    for ent in itertools.product(range(p), repeat=a * M):
        X = [list(ent[i * M:(i + 1) * M]) for i in range(a)]
        R, piv = rref(X, p)
        r = len(piv)
        Fp_ = list(range(piv[-1] + 1, M)) if r else list(range(M))
        blk = tuple(tuple(row[j] for j in Fp_) for row in R)
        blocks[(r, tuple(piv))][blk] += 1
        n1 = len(Fp_)
        if n1 < n0:
            bad += 1
            continue
        # N = #{x in P^{n'} : -R_F' x in D^r}
        N = 0
        for x in itertools.product(P, repeat=n1):
            v = [(-sum(R[i][j] * xj for j, xj in zip(Fp_, x))) % p for i in range(r)]
            if all(vi in D for vi in v):
                N += 1
                y = [0] * M
                for j, xj in zip(Fp_, x):
                    y[j] = xj
                for i, pc in enumerate(piv):
                    y[pc] = v[i]
                if not any(y) or any(sum(X[k][j] * y[j] for j in range(M)) % p for k in range(a)):
                    fails.append(("F2 witness", p, kappa, a, M))
        if r >= 1 and Fr(N) < Fr(h ** n1) * q ** r / 2:
            bad += 1
            continue
        acc = Fr(N, h ** n1)
        if r >= 1 and acc < q ** r / 2:
            fails.append(("F2 acc", p, kappa, a, M))
        worst = acc if worst is None or acc < worst else worst
    # generic-bank mean of uniform-kernel acceptance (Prop rc-lower)
    for ent in itertools.product(range(p), repeat=a * M):
        X = [list(ent[i * M:(i + 1) * M]) for i in range(a)]
        R, piv = rref(X, p)
        if len(piv) == a and piv == list(range(a)):
            gen_count += 1
            n = M - a
            cnt = 0
            for x in itertools.product(range(p), repeat=n):
                if any(x) and all(xi in D for xi in x):
                    v = [(-sum(R[i][a + j] * x[j] for j in range(n))) % p for i in range(a)]
                    if all(vi in D for vi in v):
                        cnt += 1
            gen_acc_sum += Fr(cnt, p ** n)
    if gen_count and gen_acc_sum / gen_count != (q ** (M - a) - Fr(1, p ** (M - a))) * q ** a:
        fails.append(("rc-lower mean", p, kappa, a, M))
    for (r, piv), cnt in blocks.items():
        n1 = (M - piv[-1] - 1) if r else M
        if r == 0:
            continue
        if len(cnt) != p ** (r * n1) or len(set(cnt.values())) != 1:
            fails.append(("F1", p, a, M, r, piv))
    if Fr(bad, total) > beta(p, kappa, M, n0, a):
        fails.append(("F2 beta", p, kappa, a, M, n0, Fr(bad, total)))
    print(f"[F1/F2] p={p} kappa={kappa} a={a} M={M} n0={n0}: Pr[bad]={float(Fr(bad, total)):.4g}"
          f" beta={float(beta(p, kappa, M, n0, a)):.4g}")

# [F3]
for (p, kappa, r, n) in [(5, 2, 1, 2), (5, 2, 2, 2), (7, 3, 1, 3), (7, 2, 2, 2), (11, 5, 1, 2), (13, 3, 2, 1)]:
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    P = sorted({pow(x, kappa, p) for x in range(1, p)})
    D = set(P) | {0}
    xs = list(itertools.product(P, repeat=n))
    s1 = s2 = 0
    low = 0
    tot = p ** (r * n)
    EN = h ** n * q ** r
    for ent in itertools.product(range(p), repeat=r * n):
        C = [ent[i * n:(i + 1) * n] for i in range(r)]
        N = sum(1 for x in xs if all(sum(c * xi for c, xi in zip(row, x)) % p in D for row in C))
        s1 += N
        s2 += N * N
        low += Fr(N) < EN / 2
    E = Fr(s1, tot)
    V = Fr(s2, tot) - E * E
    ok = E == EN and V == h ** (n + 1) * (q ** r - q ** (2 * r)) and V <= h * E and Fr(low, tot) <= Fr(4) / (Fr(h) ** (n - 1) * q ** r)
    if not ok:
        fails.append(("F3", p, kappa, r, n))
print("[F3] done")

# [F4]
UMAX = 80
for u in range(2, UMAX + 1):
    first = Fr((4 * u) ** (u - 1) * 4, 15 ** (2 * u) * u ** (u + 1))
    second = Fr((4 * u) ** (u - 1) * 2, (16 * u * u) ** (u + 1))
    if first != Fr(4, 225) ** u / u ** 2 or second != Fr(2 * 4 ** (u - 1), 16 ** (u + 1) * u ** (u + 3)):
        fails.append(("F4 closed", u))
    if first + second >= Fr(1, 64):
        fails.append(("F4 tree", u))
    node = Fr(4, 15 ** (2 * u) * u ** (u + 1)) + Fr(2, (16 * u * u) ** (u + 1))
    if node >= Fr(1, 2 ** 14):
        fails.append(("F4 node", u))
    if (16 * u * u - 1) < 15 * u * u:  # h >= (16u^2-1)/u >= 15u
        fails.append(("F4 h", u))
print("[F4] done; u=2 terms:", Fr(4, 225) ** 2 / 4, Fr(2 * 4, 16 ** 3 * 2 ** 5))


# [F5]
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


cnt5 = 0
maxratio = 0.0
for p in [q for q in range(5, 3000) if is_prime(q)][::7] + [65537, 1000003]:
    for kappa in range(2, min(p - 1, 40)):
        if (p - 1) % kappa:
            continue
        h = (p - 1) // kappa
        q = Fr(h + 1, p)
        for g in (1, 2, 5, 13, 30):
            for tau in (Fr(1), Fr(1, 10 ** 3), Fr(1, 10 ** 12), Fr(1, 2 ** 100)):
                target = 8 / (q ** g * tau)
                k = 0
                while Fr(h) ** k < target:
                    k += 1
                n0 = 1 + k
                j = 0
                while Fr(p) ** j < 2 / tau:
                    j += 1
                M = n0 + g + j
                b = beta(p, kappa, M, n0, g)
                if b > tau:
                    fails.append(("F5", p, kappa, g, tau))
                lpk = math.log(p / kappa)
                disp = g * (1 + 2 * math.log(kappa) / lpk) + 3 * math.log(8 / float(tau)) / lpk + 3
                if M > disp + 1e-9:
                    fails.append(("F5 size", p, kappa, g, tau, M, disp))
                maxratio = max(maxratio, M / disp)
                cnt5 += 1
print(f"[F5] {cnt5} cases, max M/display = {maxratio:.3f}")

# [F6]
p, P2, D = 5, [1, 4], {0, 1, 4}
if any(((-2 * x) % p) in D for x in P2):
    fails.append("F6")
print("[F6] -2x mod 5 for x in P_2:", [(-2 * x) % p for x in P2])
print("failures:", len(fails))
for f in fails[:30]:
    print("FAIL", f)
