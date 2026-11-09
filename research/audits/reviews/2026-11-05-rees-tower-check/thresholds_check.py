"""Independent recomputation of the one-step thresholds of the tower report
(2026-11-05-rees-threshold-6.md, Sections 3-4). Written by the tower checker;
shares no code with that report's scripts. mpmath, 50 digits."""
import mpmath as mp
from itertools import product

mp.mp.dps = 50


def W(D, r):
    A = (r - 1 - mp.mpf(r) / D) * mp.mpf(D) ** r + 1
    B = r * mp.mpf(D) ** (r - 1)
    return ((A + mp.sqrt(A * A + 4 * B)) / 2) ** 2


def lhs_TR(D, r, p):
    p = mp.mpf(p)
    Delta = ((D - 1) * (D - 2) * mp.sqrt(p) + 2 * (D - 1)) / (p - D - 1)
    Er = (r - 1) * Delta ** 2 + (1 + Delta) * mp.e ** ((r - 1) * Delta) * (r - 1) ** 2 * Delta ** 2 / 2
    return mp.mpf(D) ** r * p ** (r - 1) / (p - 1) ** r + Er


def TR(D, r):
    lo, hi = mp.mpf(D + 2), mp.mpf(10) ** 30
    target = mp.mpf(1) / (D - 1)
    assert lhs_TR(D, r, hi) < target
    for _ in range(300):
        mid = (lo + hi) / 2
        if lhs_TR(D, r, mid) < target:
            hi = mid
        else:
            lo = mid
    return hi


def P(D, r):
    return max(4 * D ** (r + 1), 4 * r * r * D ** 5)


def union_weil(D, K, ell):
    w = mp.e ** (2j * mp.pi / D)
    k = len(K)
    c0 = mp.mpf(k) / D
    G = mp.mpf(0)
    for s in range(1, D):
        cs = sum(w ** (-m * s) for m in K) / D
        G += abs(cs)
    F = c0 + G
    B = ell * G * F ** (ell - 1) - (F ** ell - c0 ** ell)
    C = ell * (F ** ell - c0 ** ell) - ell * G * F ** (ell - 1)
    # c0^ell (p - ell) - B sqrt p - C > 0 ; solve in X = sqrt p
    a2 = c0 ** ell
    disc = B * B + 4 * a2 * (C + a2 * ell)
    X = (B + mp.sqrt(disc)) / (2 * a2)
    return X ** 2


def TW(k):
    A = (k - 2) * mp.mpf(k) ** k + 1
    return ((A + mp.sqrt(A * A + 4 * mp.mpf(k) ** k)) / 2) ** 2


print("== W(D,r), T_R(D,r), P(D,r)")
for (D, r) in [(4, 2), (6, 2), (6, 3), (8, 2), (8, 4), (9, 3), (12, 2), (12, 3), (16, 2), (16, 4), (18, 3), (32, 2), (5, 2), (7, 4)]:
    w, t = W(D, r), TR(D, r)
    print(f"D={D:2d} r={r}: W={mp.nstr(w, 8):>14} T_R={mp.nstr(t, 8):>14} P={P(D, r):>14}  T_R/P={mp.nstr(t / P(D, r), 3)}")

print("== identities")
for D in range(2, 10):
    assert abs(W(D, D) - TW(D)) < mp.mpf(10) ** -20 * TW(D)
print("W(D,D)=T_W(D) for D=2..9: ok")
bad = []
for D in range(2, 200):
    for r in range(2, D + 1):
        if not W(D, r) <= mp.mpf(r) ** 2 * mp.mpf(D) ** (2 * r):
            bad.append((D, r))
print("W <= r^2 D^(2r), 2<=r<=D<200:", "ok" if not bad else bad[:5])
bad = [D for D in range(4, 2000) if not W(D, 2) < ((D - 1) ** 2 + 1) ** 2]
print("W(D,2) < ((D-1)^2+1)^2, 4<=D<2000:", "ok" if not bad else bad)
print("  D=3 (excluded by the lemma):", mp.nstr(W(3, 2), 8), "vs", ((3 - 1) ** 2 + 1) ** 2)
bad = [D for D in range(2, 2000) if not W(D, 3) <= 4 * D ** 6]
print("W(D,3) <= 4 D^6, 2<=D<2000:", "ok" if not bad else bad)

print("== Lemma 3.3: D*(lhs) at p = P(D,r), 4<=D<=64, 2<=r<=D (proof claims <= 0.4312)")
worst = (0, None)
for D in range(4, 65):
    for r in range(2, D + 1):
        v = D * lhs_TR(D, r, P(D, r))
        if v > worst[0]:
            worst = (v, (D, r))
print("max D*lhs =", mp.nstr(worst[0], 6), "at", worst[1])
# also check the closed-form step constants used in the proof, at the extreme D=4
for D in (4, 5, 64, 1000):
    for r in (2, D):
        p = mp.mpf(P(D, r))
        Delta = ((D - 1) * (D - 2) * mp.sqrt(p) + 2 * (D - 1)) / (p - D - 1)
        assert Delta <= mp.mpf("0.5003") / (r * mp.sqrt(D)), (D, r)
        assert mp.mpf(D) ** r * p ** (r - 1) / (p - 1) ** r <= mp.mpf("1.001") / (4 * D)
print("Delta <= 0.5003/(r sqrt D) and first term <= 1.001/(4D) at sample (D,r): ok")
print("constant 1.1251*e^0.2502/2 =", mp.nstr(mp.mpf("1.1251") * mp.e ** mp.mpf("0.2502") / 2, 6))
print("0.7225*0.2503 =", mp.nstr(mp.mpf("0.7225") * mp.mpf("0.2503"), 6), "; 0.2503+0.1809 =", mp.mpf("0.2503") + mp.mpf("0.1809"))

print("== Theorem 4.2 / corollaries")
TA = {5: mp.mpf("1.27e4"), 7: mp.mpf("4.94e6")}
for kappa in (4, 6, 8, 9, 10, 12, 16, 18, 24, 27, 32):
    from sympy import factorint
    qs = sorted([q for q, e in factorint(kappa).items() for _ in range(e)], reverse=True)
    Ds = [1]
    for q in qs:
        Ds.append(Ds[-1] * q)
    q = qs[0]
    steps = [(Ds[t], qs[t - 1]) for t in range(2, len(Ds))]
    theta = max([min(W(D, r), TR(D, r)) for (D, r) in steps] + ([0] if q < 5 else [TA.get(q, mp.inf)]))
    closed = max(4 * kappa ** (q + 1), 4 * q * q * kappa ** 5)
    print(f"kappa={kappa:2d} chain={Ds[1:]} Theta={mp.nstr(theta, 6):>12} closed max(4k^(q+1),4q^2k^5)={closed:.3e}"
          f"  4k^max(q+1,7)={4 * kappa ** max(q + 1, 7):.3e}")
    for (D, r) in steps:
        assert min(W(D, r), TR(D, r)) <= P(D, r) <= closed
    if q == 2:
        assert theta < ((kappa - 1) ** 2 + 1) ** 2, kappa
    if q <= 3:
        assert theta <= 36 * kappa ** 5
print("step thresholds <= P(D_t,q_t) <= closed form; 2^L: Theta < ((k-1)^2+1)^2; 3-smooth: Theta <= 36k^5: ok")

print("== union-target Weil (Prop 3.4), rows ell, target K")
for (D, K) in [(5, (0, 1)), (5, (0, 1, 2)), (7, (0, 1, 2, 3)), (7, (0, 1))]:
    print(f"D={D} K={K}: threshold {mp.nstr(union_weil(D, K, D), 10)}")
# K={0} must reproduce T_W
for D in (3, 4, 5):
    assert abs(union_weil(D, (0,), D) - TW(D)) < mp.mpf(10) ** -15 * TW(D)
print("K={0} reproduces T_W at D=3,4,5: ok")
print("W(5,2) =", mp.nstr(W(5, 2), 8), " T_R(7,4) =", mp.nstr(TR(7, 4), 8))
