#!/usr/bin/env python
r"""Independent recomputation of Schedule 1H (core main-core.tex, Def. def:schedule1h) for the
2026-11-13 hostile referee. Written from the TeX definitions only; imports nothing from the
integrator's or the attack's scripts.

Coset-level ("cyclotomic") arithmetic: for kappa | p-1, P = kappa-th powers, cosets C_i = g^i P.
(C_i + C_j) \ {0} is a union of cosets; Add0[j] = cosets of 1+y, y in C_j, y != -1; and
0 in C_i + C_j iff j = i + coset(-1).

Rules:
  rule "D" (the definition): plans (s,F) admissible by exact T_s if p < 4 kappa^4, only (1,F1) if
           p >= 4 kappa^4.
  rule "X" (variant for comparison): exact T_s at every p.
Outputs JSON with E_H(c), attainment sets, K-check, tail check, A_2(1), A_2(3), A_4(2)@5, the
crossover table.
"""
import json, math, sys
import numpy as np
from fractions import Fraction

LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 60000


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def factor(n):
    f, d = [], 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f


def prim_root(p):
    fs = factor(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g


class Field:
    def __init__(self, p):
        self.p = p
        g = prim_root(p) if p > 2 else 1
        self.g = g
        dl = np.zeros(p, dtype=np.int64)
        x = 1
        pw = np.zeros(p - 1, dtype=np.int64)
        for k in range(p - 1):
            pw[k] = x
            x = x * g % p
        dl[pw] = np.arange(p - 1)
        self.dl = dl
        self.pw = pw


def coset_data(F, k):
    """Add0 as list of frozensets, m1 = coset(-1)."""
    p = F.p
    y = np.arange(1, p, dtype=np.int64)
    cj = F.dl[y] % k
    t = (1 + y) % p
    mask = t != 0
    M = np.zeros((k, k), dtype=bool)
    M[cj[mask], F.dl[t[mask]] % k] = True
    add0 = [frozenset(np.nonzero(M[j])[0].tolist()) for j in range(k)]
    m1 = int(F.dl[p - 1] % k)
    return add0, m1


def sumset(S1, z1, S2, z2, add0, m1, k):
    """(A + B) where A = cosets S1 (+0 if z1), B likewise; nonempty-sum convention handled by caller."""
    out, z = set(), False
    for i in S1:
        for j in S2:
            for kk in add0[(j - i) % k]:
                out.add((i + kk) % k)
            if (j - i) % k == m1:
                z = True
    if z1:
        out |= S2; z = z or z2
    if z2:
        out |= S1; z = z or z1
    return out, z


def t_value(add0, m1, k):
    # U_1 = P ; U_n = U_{n-1} u (U_{n-1} + P); t = least n with 0 in U_n
    S, z, n = {0}, False, 1
    while not z:
        S2, z2 = sumset(S, z, {0}, False, add0, m1, k)
        S |= S2; z = z or z2; n += 1
        if n > k + 2:
            raise RuntimeError("t > k+1 contradicts Chevalley-Warning")
    return n


def T_sets(F, k, add0, m1, jmax):
    """T_0..T_jmax by the recursion, as (frozenset cosets, zero flag). Also returns e=coset(eps)."""
    p, h = F.p, (F.p - 1) // k
    # q: q^h = -1. q = theta^(k/2) for least nonresidue theta (or -1 if h odd) -- T independent of q.
    if h % 2 == 1:
        q = p - 1
    else:
        th = next(x for x in range(2, p) if pow(x, (p - 1) // 2, p) == p - 1)
        q = pow(th, k // 2, p)
    assert pow(q, h, p) == p - 1
    eps = (-pow(q, p - 2, p)) % p
    e = int(F.dl[eps] % k)
    T = [(frozenset({0}), False)]
    for j in range(1, jmax + 1):
        S, z = T[-1]
        epsS = {(i + e) % k for i in S}
        out = set(S) | epsS
        zz = z
        for i in S:
            for jj in epsS:
                for kk in add0[(jj - i) % k]:
                    out.add((i + kk) % k)
                if (jj - i) % k == m1:
                    zz = True
        T.append((frozenset(out), zz))
    return T, e


def brute_T(p, k, jmax):
    """Element-level T(c^{(j)}) straight from the definition (sums over y in (P u 0)^r, y != 0)."""
    P = sorted({pow(x, k, p) for x in range(1, p)})
    h = (p - 1) // k
    if h % 2:
        q = p - 1
    else:
        th = next(x for x in range(2, p) if pow(x, (p - 1) // 2, p) == p - 1)
        q = pow(th, k // 2, p)
    eps = (-pow(q, p - 2, p)) % p
    c = [1]
    res = []
    for j in range(jmax + 1):
        if j > 0:
            c = c + [eps * x % p for x in c]
        # reach[s] = (achievable with all zero so far?) track sets: A0 = {0 with y=0}, A1 = sums with y!=0
        A1 = set()
        A0 = {0}
        for ck in c:
            terms = {y * ck % p for y in P}
            newA1 = set(A1)
            for a in A0 | A1:
                for tt in terms:
                    newA1.add((a + tt) % p)
            A1 = newA1
        res.append(A1)
    return res


def full_nonzero(S, k):
    return len(S) == k


class S1H:
    """Degrees, constants, admissible plans per (p, kappa) for one prime."""

    def __init__(self, p, rule="D"):
        self.p, self.rule = p, rule
        F = Field(p)
        self.info = {}
        divs = [k for k in range(1, 10) if (p - 1) % k == 0]
        for k in divs:
            if k == 1:
                self.info[1] = dict(e=1, K=1, cands=None)
                continue
            add0, m1 = coset_data(F, k)
            t = t_value(add0, m1, k)
            L = math.ceil(math.log2(t))
            rec = dict(t=t, L=L)
            if k % 2 == 0:
                big = p >= 4 * k ** 4
                if big and rule == "D":
                    rec["s0F0"], rec["s0F1"] = None, 1
                    rec["big"] = True
                else:
                    T, e = T_sets(F, k, add0, m1, k + 2)
                    s0F0 = next((s for s in range(1, k + 3) if T[s][1]), None)
                    s0F1 = next((s for s in range(1, k + 3) if full_nonzero(T[s][0], k)), None)
                    rec["s0F0"], rec["s0F1"] = s0F0, s0F1
                    rec["big"] = big
                    rec["T1full"] = full_nonzero(T[1][0], k)
                    rec["T1zero"] = T[1][1]
            self.info[k] = rec
        # degrees bottom-up (divisors in increasing order)
        for k in divs:
            if k == 1:
                continue
            r = self.info[k]
            cands = [("a", 0, k * r["L"], Fraction(k) ** (k * (k - 1) * r["L"] // 2) if False else k ** (k * (k - 1) * r["L"] // 2))]
            if k % 2 == 0:
                D = k // 2
                eD, KD = self.info[D]["e"], self.info[D]["K"]
                if r["s0F0"] is not None:
                    s = r["s0F0"]; cands.append(("F0", s, s * eD, KD ** s))
                if r["s0F1"] is not None:
                    s = r["s0F1"]; cands.append(("F1", s, s * eD + 1, KD ** s))
            e = min(c[2] for c in cands)
            K = min(c[3] for c in cands if c[2] == e)
            r["e"], r["K"], r["cands"] = e, K, cands

    def A(self, k, a):
        if k == 1:
            return a + 1
        r = self.info[k]
        best = None
        order = {"a": 0, "F0": 2, "F1": 3}
        for (typ, s, deg, K) in r["cands"]:
            if typ == "a":
                ar = (k ** (k * (k - 1) // 2) * (a + 1) ** k) ** r["L"]
            else:
                D = k // 2
                ar = self.A(D, a) ** s * (1 if typ == "F0" else a + 1)
            key = (ar, order[typ] if typ == "a" else 1, s, order[typ])
            if best is None or key < best[0]:
                best = (key, typ, s)
        return best[0][0]

    def plan(self, k, a):
        r = self.info[k]
        best = None
        for (typ, s, deg, K) in r["cands"]:
            if typ == "a":
                ar = (k ** (k * (k - 1) // 2) * (a + 1) ** k) ** r["L"]; key = (ar, 0, 0, 0)
            else:
                ar = self.A(k // 2, a) ** s * (1 if typ == "F0" else a + 1)
                key = (ar, 1, s, 0 if typ == "F0" else 1)
            if best is None or key < best[0]:
                best = (key, typ, s)
        return best


def ckappa(k):
    return k ** (k * (k - 1) * math.ceil(math.log2(k + 1)) // 2)


def main():
    out = {}
    primes = [p for p in primes_upto(LIM) if p >= 3]
    EH = {r: {c: (-1, []) for c in range(2, 10)} for r in ("D", "X")}
    E1 = {c: (-1, []) for c in range(2, 10)}
    Kviol, T1fail, tfail, ehat_fail = [], [], [], []
    ehat = {1: 1, 2: 2, 3: 3, 4: 3, 5: 5, 6: 4, 7: 7, 8: 4, 9: 9}
    prof = [17, 16, 14, 12, 9, 6, 3, 1]
    rows = {"heis": (2, 3, [1]), "fil": (3, 4, [2, 1]), "free": (3, 5, [3, 2]), "dl": (3, 8, [4, 2]),
            "c9": (9, 19, prof)}
    Qmax = {nm: (0, []) for nm in rows}
    maxstages = 0
    for p in primes:
        objs = {"D": S1H(p, "D")}
        if p < 30000:
            objs["X"] = S1H(p, "X")
        o = objs["D"]
        for k, r in o.info.items():
            if k >= 2:
                if r["t"] > 3 and p >= 4 * k ** 4:
                    tfail.append((p, k))
                if "T1full" in r and r["big"] and not (r["T1full"] and not r["T1zero"]):
                    T1fail.append((p, k))
                if r["K"] > ckappa(k):
                    Kviol.append((p, k, r["K"], ckappa(k)))
                for (typ, s, deg, K) in r["cands"]:
                    if typ != "a" and deg == r["e"]:
                        maxstages = max(maxstages, s)
            if p >= 26244 and o.info[k]["e"] != ehat[k]:
                ehat_fail.append((p, k, o.info[k]["e"]))
        for c in range(2, 10):
            if p <= c:
                continue
            for rl, ob in objs.items():
                tot = 1 + sum(ob.info[math.gcd(d, p - 1)]["e"] for d in range(2, c + 1))
                best, at = EH[rl][c]
                if tot > best:
                    EH[rl][c] = (tot, [p])
                elif tot == best:
                    at.append(p)
            tot1 = 1
            for d in range(2, c + 1):
                k = math.gcd(d, p - 1)
                tot1 += 1 if k == 1 else k * o.info[k]["L"]
            best, at = E1[c]
            if tot1 > best:
                E1[c] = (tot1, [p])
            elif tot1 == best:
                at.append(p)
        if p >= 11:
            for nm, (c, m, g) in rows.items():
                if p <= c:
                    continue
                Q = c * (m + 1)
                for d, gd in zip(range(2, c + 1), g):
                    Q *= o.A(math.gcd(d, p - 1), gd)
                best, at = Qmax[nm]
                if Q > best:
                    Qmax[nm] = (Q, [p])
                elif Q == best:
                    at.append(p)
    out["LIM"] = LIM
    out["E_H"] = {rl: {c: [v[0], v[1][:12], len(v[1])] for c, v in EH[rl].items()} for rl in EH}
    out["E_H_X_note"] = "rule X computed only for p < 30000"
    out["E_1"] = {c: [v[0], v[1][:12], len(v[1])] for c, v in E1.items()}
    out["K_violations"] = Kviol[:20]
    out["T1_Weil_failures"] = T1fail[:20]
    out["t_gt3_above_4k4"] = tfail[:20]
    out["ehat_failures_above_26244"] = ehat_fail[:20]
    out["max_stages_degree_optimal"] = maxstages
    out["Qmax"] = {nm: [v[0], math.log2(v[0]), v[1][:12], len(v[1])] for nm, v in Qmax.items()}
    # small arities
    o5 = S1H(5); o7 = S1H(7); o13 = S1H(13); o11 = S1H(11)
    out["A2(1)"] = {p: S1H(p).A(2, 1) for p in (3, 5, 7, 11, 13, 101, 103)}
    out["A2(3)"] = {p: S1H(p).A(2, 3) for p in (3, 5, 7, 11, 13, 101, 103)}
    out["A4(2)@5"] = o5.A(4, 2)
    out["plan4@5"] = list(o5.plan(4, 2)[1:])
    out["A2(2)@5"] = o5.A(2, 2)
    out["k6@7"] = {kk: str(v) for kk, v in o7.info[6].items()}
    o41 = S1H(41)
    out["k8@41"] = {kk: str(v) for kk, v in o41.info[8].items()}
    # brute-force cross-check of the T recursion at small primes
    bad = []
    for p in [x for x in primes if x < 120]:
        F = Field(p)
        for k in (2, 4, 6, 8):
            if (p - 1) % k:
                continue
            add0, m1 = coset_data(F, k)
            T, e = T_sets(F, k, add0, m1, 3)
            B = brute_T(p, k, 3)
            for j in range(4):
                S, z = T[j]
                elems = {int(x) for x in range(1, p) if int(F.dl[x] % k) in S}
                if z:
                    elems.add(0)
                if elems != B[j]:
                    bad.append((p, k, j))
    out["brute_T_mismatch"] = bad
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
