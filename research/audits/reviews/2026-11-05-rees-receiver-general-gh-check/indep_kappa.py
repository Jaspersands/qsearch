"""Independent check of CoherentSDEKappa (referee of 2026-11-05-rees-receiver-general-gh.md).

Written from the paper (prop:triangular-sde, lem:coherent-power-sde, the definition of E_2(kappa))
without reading or importing the report's scripts. Imports from theorems/ only:
  * CoherentSDEKappa (the circuit under test), kappa_constants (only to compare the refusal);
  * rees_circuit_coherent.flatten (macro expansion into the real gate lists).
Everything else is new here: primitive roots and discrete logs, the coset map, the contraction
search (plain exact DFS over beta with bitset pruning, no FFT), the triangular solver written from
the proof of prop:triangular-sde (paper-faithful stop test v_{k+1} in U_k by rank, back substitution
by coordinate solves), the least kappa-th root by table, the Bezout exponent by search, and the
bit-sliced simulator.

AI-written, pending human review.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import resource
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa, kappa_constants  # noqa: E402
from theorems.rees_circuit_coherent import flatten  # noqa: E402


# ------------------------------------------------------------------ field utilities (own)

def factor(n):
    out, q = {}, 2
    while q*q <= n:
        while n % q == 0:
            out[q] = out.get(q, 0)+1
            n //= q
        q += 1
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def prim_root(p):
    qs = list(factor(p-1))
    return next(r for r in range(2, p) if all(pow(r, (p-1)//q, p) != 1 for q in qs))


class Field:
    def __init__(self, p, kappa):
        assert (p-1) % kappa == 0
        self.p, self.kappa = p, kappa
        r = prim_root(p)
        self.log = [None]*p
        x = 1
        for e in range(p-1):
            self.log[x] = e
            x = x*r % p
        # least g >= 2 whose class generates F_p^x / P: log g invertible mod kappa
        self.g = next(g for g in range(2, p) if math.gcd(self.log[g], kappa) == 1)
        self.lg_inv = pow(self.log[self.g], -1, kappa) if kappa > 1 else 0
        # cos(y) = nu iff y in g^nu P
        self.cos = [None]+[(self.log[y]*self.lg_inv) % kappa for y in range(1, p)]
        self.ok = [np.array([y == 0 or self.cos[y] == c for y in range(p)], dtype=bool) for c in range(kappa)]
        tab = {}
        for t in range(p):
            tab.setdefault(pow(t, kappa, p), t)
        self.least_root = tab

    def in_cos0(self, y, c):
        y %= self.p
        return y == 0 or self.cos[y] == c % self.kappa


def contractions(F, limit=None, least_only=False):
    """All normalised (alpha, beta) in lex order of (beta_1.., alpha_1..): alpha_0 = 1, beta_0 = 0,
    alpha_j + beta_i in g^{-(i+j)} P u {0}. Plain DFS over beta, bitset over alpha."""
    p, k = F.p, F.kappa
    out = []
    A0 = [None]+[F.ok[(-j) % k].copy() for j in range(1, k)]
    beta = [0]*k

    def dfs(i, A):
        if limit is not None and len(out) >= limit:
            return True
        if i == k:
            lists = [np.nonzero(A[j])[0].tolist() for j in range(1, k)]
            if least_only:
                out.append(((1,)+tuple(l[0] for l in lists), tuple(beta)))
                return True
            for tup in itertools.product(*lists):
                out.append(((1,)+tuple(tup), tuple(beta)))
                if limit is not None and len(out) >= limit:
                    return True
            return False
        for t in range(p):
            if not F.in_cos0(1+t, -i):
                continue
            new = [None]+[A[j] & np.roll(F.ok[(-(i+j)) % k], -t) for j in range(1, k)]
            if all(new[j].any() for j in range(1, k)):
                beta[i] = t
                if dfs(i+1, new) and (least_only or limit is not None):
                    return True
        return False
    dfs(1, A0)
    return out


def valid(F, alpha, beta):
    k = F.kappa
    return alpha[0] % F.p == 1 and beta[0] % F.p == 0 and all(
        F.in_cos0(alpha[j]+beta[i], -(i+j)) for i in range(k) for j in range(k))


# ------------------------------------------------------------------ linear algebra (own)

def rank(p, vecs, a):
    M = [list(v) for v in vecs]
    r = 0
    for c in range(a):
        piv = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [x*inv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(x-f*y) % p for x, y in zip(M[i], M[r])]
        r += 1
    return r


def solve(p, basis, target, a):
    """Coefficients c with sum c_l basis_l = target (basis independent); None if not in span."""
    n = len(basis)
    # augmented a x (n+1)
    M = [[basis[l][r] % p for l in range(n)]+[target[r] % p] for r in range(a)]
    row, pivs = 0, []
    for c in range(n):
        piv = next((i for i in range(row, a) if M[i][c]), None)
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = pow(M[row][c], -1, p)
        M[row] = [x*inv % p for x in M[row]]
        for i in range(a):
            if i != row and M[i][c]:
                f = M[i][c]
                M[i] = [(x-f*y) % p for x, y in zip(M[i], M[row])]
        pivs.append(c)
        row += 1
    if any(M[i][n] for i in range(row, a)):
        return None
    assert len(pivs) == n, "basis not independent"
    sol = [0]*n
    for i, c in enumerate(pivs):
        sol[c] = M[i][n]
    return sol


def first_dep(p, vecs, a):
    """Smallest j with vecs[j] in span(vecs[:j]) (prefix independent); y with y_j = 1, sum y v = 0."""
    for j in range(len(vecs)):
        if rank(p, vecs[:j+1], a) == j:
            c = solve(p, vecs[:j], vecs[j], a)
            return j, [(-x) % p for x in c]+[1]+[0]*(len(vecs)-j-1)
    return None


# ------------------------------------------------------------------ the solver, from the paper

def paper_witness(F, cols, d, alpha, beta):
    p, k = F.p, F.kappa
    a = len(cols[0])
    M = len(cols)
    assert M == (a+1)*(a+2)//2
    V, E, Ds, offs = [], [], [], []
    o = 0
    x = [0]*M
    K = None
    for rnd in range(a+1):
        nb = a+1-rnd
        blk = list(range(o, o+nb))
        offs.append(o)
        o += nb
        j, y = first_dep(p, V+[cols[i] for i in blk], a)
        assert j >= rnd
        delta = y[rnd:]
        e = [sum(delta[t]*cols[blk[t]][r] for t in range(nb)) % p for r in range(a)]
        v = [sum(beta[F.cos[delta[t]]]*delta[t]*cols[blk[t]][r] for t in range(nb) if delta[t]) % p
             for r in range(a)]
        Ds.append((blk, delta))
        E.append(e)
        inU = rank(p, V+[v], a) == len(V)       # paper-faithful stop test
        if inU:
            K = rnd
            for t in range(nb):
                if delta[t]:
                    x[blk[t]] = delta[t]*(1+beta[F.cos[delta[t]]]) % p
            rho = [(e[r]+v[r]) % p for r in range(a)]
            break
        V.append(v)
    # Lemma 4' (independently): at the stop round v = 0 and all nonzero delta in P
    lemma4 = all(c == 0 for c in v) and all(F.cos[dl] == 0 for dl in Ds[K][1] if dl)
    tau = [(-c) % p for c in rho]
    for l in range(K, 0, -1):
        c = solve(p, V[:l], tau, a)
        assert c is not None
        zeta = c[l-1]
        if zeta:
            n = F.cos[zeta]
            blk, delta = Ds[l-1]
            for t in range(len(blk)):
                if delta[t]:
                    x[blk[t]] = zeta*delta[t]*(alpha[n]+beta[F.cos[delta[t]]]) % p
            tau = [(tau[r]-zeta*(alpha[n]*E[l-1][r]+V[l-1][r])) % p for r in range(a)]
    assert not any(tau)
    h = (p-1)//k
    u = 1 if h == 1 else next(u for u in range(1, h+1) if u*(d//k) % h == 1)
    for xi in x:
        assert xi == 0 or F.cos[xi] == 0
    s = [pow(F.least_root[xi], u, p) for xi in x]
    return s, K, lemma4


# ------------------------------------------------------------------ simulator (own)

class Sim:
    def __init__(self, nw, N):
        self.N, self.nwd = N, (N+63)//64
        self.S = np.zeros((nw, self.nwd), dtype=np.uint64)

    def load(self, reg, vals):
        vals = np.asarray(vals, dtype=np.uint64)
        for j, w in enumerate(reg):
            bits = ((vals >> np.uint64(j)) & np.uint64(1)).astype(np.uint8)
            buf = np.zeros(self.nwd*64, dtype=np.uint8)
            buf[:self.N] = bits
            self.S[w] = np.packbits(buf, bitorder="little").view(np.uint64)

    def read(self, reg):
        out = np.zeros(self.N, dtype=np.int64)
        for j, w in enumerate(reg):
            bits = np.unpackbits(self.S[w].view(np.uint8), bitorder="little")[:self.N]
            out |= bits.astype(np.int64) << j
        return out

    def run(self, gates):
        S = self.S
        for name, q in gates:
            if name == "cx":
                S[q[1]] ^= S[q[0]]
            elif name == "ccx":
                S[q[2]] ^= S[q[0]] & S[q[1]]
            elif name == "x":
                np.invert(S[q[0]], out=S[q[0]])
            elif name == "swap":
                t = S[q[0]].copy()
                S[q[0]] = S[q[1]]
                S[q[1]] = t
            else:
                raise ValueError(name)


def gate_targets(g):
    name, q = g
    return set(q) if name == "swap" else {q[-1]}


# ------------------------------------------------------------------ one case

def run_case(p, a, d, inputs, contraction=None, label="", chunk=1 << 16, mutate=None):
    t0 = time.time()
    k = math.gcd(d, p-1)
    F = Field(p, k)
    if contraction is None:
        least = contractions(F, least_only=True)
        assert least, "own search says p in E_2(kappa)"
        contraction = least[0]
        own_least = contraction
    else:
        own_least = None
    alpha, beta = contraction
    assert valid(F, alpha, beta)
    circ = CoherentSDEKappa(p, a, d, contraction=None if own_least else contraction, mutate=mutate)
    if own_least is not None:
        mod_c = (tuple(circ.alpha), tuple(circ.beta))
        same_least = mod_c == (tuple(alpha), tuple(beta))
    else:
        same_least = None
    gates = flatten(circ.prog, p, circ.anc)
    Lw = {w for col in circ.L for r in col for w in r}
    Sw = {w for r in circ.S for w in r}
    static = {"no_gate_targets_label": not any(gate_targets(g) & Lw for g in gates),
              "F_items_touch_no_S": not any(_touch(it) & Sw for it in circ.F),
              "gate_types": sorted({g[0] for g in gates})}
    M = len(circ.L)
    inputs = np.asarray(inputs, dtype=np.int64)          # (N, M, a)
    N = len(inputs)
    agg = {"labels_restored": True, "S_equals_paper_witness": True, "workspace_zero": True,
           "witness_valid": True, "lemma4_prime": True}
    Ks = {}
    for st in range(0, N, chunk):
        blk = inputs[st:st+chunk]
        n = len(blk)
        sim = Sim(circ.nw, n)
        for c in range(M):
            for r in range(a):
                sim.load(circ.L[c][r], blk[:, c, r])
        sim.run(gates)
        ref = []
        for row in blk:
            cols = [list(map(int, row[c])) for c in range(M)]
            s, K, l4 = paper_witness(F, cols, d, alpha, beta)
            Ks[K] = Ks.get(K, 0)+1
            agg["lemma4_prime"] &= l4
            ok = any(s) and all(sum(pow(si, d, p)*cols[c][r] for c, si in enumerate(s)) % p == 0
                                for r in range(a))
            agg["witness_valid"] &= ok
            ref.append(s)
        ref = np.array(ref, dtype=np.int64)
        for c in range(M):
            for r in range(a):
                agg["labels_restored"] &= bool(np.array_equal(sim.read(circ.L[c][r]), blk[:, c, r]))
            agg["S_equals_paper_witness"] &= bool(np.array_equal(sim.read(circ.S[c]), ref[:, c]))
        other = [w for w in range(circ.nw) if w not in Lw and w not in Sw]
        agg["workspace_zero"] &= not bool(sim.S[other].any())
        del sim
    res = {"label": label, "p": p, "a": a, "d": d, "kappa": k, "u": circ.u, "g": F.g, "inputs": int(N),
           "contraction": {"alpha": list(alpha), "beta": list(beta)},
           "module_contraction_equals_own_lex_least": same_least,
           "K_hist": {str(kk): v for kk, v in sorted(Ks.items())}, "gates": len(gates), "wires": circ.nw,
           **static, **agg}
    res["all_pass"] = all(v for kk, v in {**agg, **{x: static[x] for x in static if x != "gate_types"}}.items())
    res["seconds"] = round(time.time()-t0, 1)
    res["rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
    return res


def _touch(it):
    if hasattr(it, "args"):
        return {w for r in it.args for w in r}
    return set(it[1]) if it[0] != "swapreg" else {w for r in it[1] for w in r}


def all_inputs(p, a):
    M = (a+1)*(a+2)//2
    n = M*a
    idx = np.arange(p**n, dtype=np.int64)
    out = np.zeros((p**n, n), dtype=np.int64)
    for t in range(n-1, -1, -1):
        out[:, t] = idx % p
        idx //= p
    return out.reshape(-1, M, a)


def sampled_inputs(p, a, n, seed):
    """Random inputs plus degenerate ones (zero columns, repeated columns, low-rank tuples)."""
    rng = np.random.default_rng(seed)
    M = (a+1)*(a+2)//2
    A = rng.integers(0, p, size=(n, M, a))
    q = n//4
    for i in range(q):                    # rank <= 1 tuples
        v = rng.integers(0, p, size=a)
        A[i] = np.outer(rng.integers(0, p, size=M), v) % p
    for i in range(q, 2*q):               # sparse columns
        mask = rng.random((M, a)) < 0.6
        A[i][mask] = 0
    for i in range(2*q, 2*q+q//2):        # repeated columns
        c = rng.integers(0, M)
        A[i][:] = A[i][c]
    A[2*q+q//2] = 0
    return A


# ------------------------------------------------------------------ refusals

def refusal_scan(kappa, pmax, d=None):
    d = kappa if d is None else d
    rows = []
    for p in range(3, pmax+1):
        if not all(p % q for q in range(2, int(p**0.5)+1)) or (p-1) % kappa or math.gcd(d, p-1) != kappa:
            continue
        F = Field(p, kappa)
        own = contractions(F, least_only=True)
        try:
            C = kappa_constants(p, d)
            mod = (tuple(C["alpha"]), tuple(C["beta"]))
            err = None
        except ValueError as e:
            mod, err = None, str(e)
        rows.append({"p": p, "own_exists": bool(own), "module_refuses": err is not None,
                     "agree": bool(own) == (err is None) and (not own or tuple(map(tuple, own[0])) == mod)})
    return {"kappa": kappa, "d": d, "pmax": pmax, "primes": len(rows),
            "own_E2": [r["p"] for r in rows if not r["own_exists"]],
            "module_refused": [r["p"] for r in rows if r["module_refuses"]],
            "all_agree": all(r["agree"] for r in rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = []
    log = lambda r: print(json.dumps({k: v for k, v in r.items() if k not in ("contraction",)}), flush=True)
    if args.part == "k3":
        for p, a, d in [(31, 1, 3), (31, 1, 9), (43, 1, 3)]:
            res.append(run_case(p, a, d, all_inputs(p, a), label="kappa3 exhaustive"))
            log(res[-1])
        # alternative contractions at p = 31: count them, run four non-least ones exhaustively
        F = Field(31, 3)
        allc = contractions(F)
        zero_entry = [c for c in allc if 0 in [(c[0][j]+c[1][i]) % 31 for i in range(3) for j in range(3)]]
        print(json.dumps({"p": 31, "kappa": 3, "normalised_contractions": len(allc),
                          "with_a_zero_sum_entry": len(zero_entry)}), flush=True)
        picks = [allc[1], allc[len(allc)//2], allc[-1]]+([zero_entry[-1]] if zero_entry else [])
        for c in picks:
            res.append(run_case(31, 1, 3, all_inputs(31, 1), contraction=c, label="kappa3 alt contraction"))
            log(res[-1])
        # counts at p = 7, 13, 19 (the report says 42 at p = 19; the kappa report quoted 40)
        cnt = {}
        for p in (7, 13, 19):
            cc = contractions(Field(p, 3))
            cnt[p] = {"all": len(cc), "all_entries_nonzero": sum(
                all((c[0][j]+c[1][i]) % p for i in range(3) for j in range(3)) for c in cc)}
        print(json.dumps({"contraction_counts_kappa3": cnt}), flush=True)
        res.append({"contraction_counts_kappa3": cnt, "p31_count": len(allc), "p31_zero_entry": len(zero_entry)})
        # a = 2, sampled, with the least and with an alternative contraction
        for p in (7, 31):
            res.append(run_case(p, 2, 3, sampled_inputs(p, 2, 1500, seed=p), label="kappa3 a=2 sampled"))
            log(res[-1])
        alt7 = contractions(Field(7, 3))[-1]
        res.append(run_case(7, 2, 3, sampled_inputs(7, 2, 1500, seed=77), contraction=alt7,
                            label="kappa3 a=2 sampled alt contraction"))
        log(res[-1])
        # sensitivity: mutants of the circuit must fail against the own reference
        base = CoherentSDEKappa(13, 1, 3)
        for name, m in [("beta1+1", {"beta": (0, (base.beta[1]+1) % 13, base.beta[2])}),
                        ("alpha2+1", {"alpha": (1, base.alpha[1], (base.alpha[2]+1) % 13)}),
                        ("no least-root", {"omega_min": True}), ("out coeff 2", {"out": 2})]:
            r = run_case(13, 1, 3, all_inputs(13, 1), label="mutant "+name, mutate=m)
            r["detected"] = not r["all_pass"]
            res.append(r)
            log(r)
    elif args.part == "k4":
        res.append(run_case(61, 1, 4, all_inputs(61, 1), label="kappa4 exhaustive (p=61: every contraction has a zero entry per paper)"))
        log(res[-1])
        res.append(run_case(41, 1, 12, all_inputs(41, 1), label="kappa4 exhaustive, u != 1"))
        log(res[-1])
        alt = contractions(Field(41, 4), limit=40)[-1]
        res.append(run_case(41, 1, 4, all_inputs(41, 1), contraction=alt, label="kappa4 alt contraction"))
        log(res[-1])
        res.append(run_case(73, 2, 4, sampled_inputs(73, 2, 600, seed=73), label="kappa4 a=2 sampled"))
        log(res[-1])
    elif args.part == "refuse":
        for kappa, pmax in [(3, 400), (4, 400), (5, 200), (6, 240)]:
            r = refusal_scan(kappa, pmax)
            res.append(r)
            print(json.dumps(r), flush=True)
        r = refusal_scan(4, 120, d=12)
        res.append(r)
        print(json.dumps(r), flush=True)
        # the constructor itself refuses (not only the constants)
        rows = []
        for p, d in [(13, 4), (53, 4), (11, 5), (181, 5), (7, 6), (859, 6)]:
            try:
                CoherentSDEKappa(p, 1, d)
                rows.append({"p": p, "d": d, "refused": None})
            except ValueError as e:
                rows.append({"p": p, "d": d, "refused": str(e)})
        res.append({"constructor_refusals": rows})
        print(json.dumps(rows), flush=True)
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
