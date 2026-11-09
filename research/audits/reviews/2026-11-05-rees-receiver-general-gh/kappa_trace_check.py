"""(A) controls for the written proof that CoherentSDEKappa (power mode, the
circuit the receiver builds at kappa_d >= 3) writes the canonical witness on
every canonical input. Report: ../2026-11-05-rees-receiver-general-gh.md, Section 2.

AI-written, pending human review. Imports theorems/ read-only, writes only the
JSON named by --out.

For every input of a stated set it checks, against a reference written here
from the definition (own discrete logs, own coset map, own first dependency by
fresh elimination per prefix, the paper-faithful stop test v_{k+1} in U_k,
own lexicographic contraction search for small p, brute-force least roots):

  T1  after F: F_k = [k = K] (one-hot at the stop round);
  T2  after F: delta registers of every genuine round k <= K hold delta^(k);
  T3  after F: tau_l holds zeta_l (the value read at back-substitution step l),
      0 for l > K;  za_l holds zeta_l * alpha_{cos zeta_l};
  T4  after F: the weight registers X hold x(lambda);
  T5  after F then C: every wire outside S has its post-F value (C changes only S);
  T6  after U = F C F^-1: S = s(lambda) = rho(x)^u, labels restored, every other
      wire 0, s != 0, sum_i s_i^d lambda_i = 0;
  L4  Lemma 4' on every genuine round of the reference: v_{k+1} in U_k
      <=> every nonzero delta_i in P <=> v_{k+1} = 0.

Static scans (S1-S5) on the program items and the flattened gate list.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time

REPO = "/Users/jaspersands/Developer/qsearch"
sys.path.insert(0, REPO)

import numpy as np  # noqa: E402

from theorems.rees_circuit_arith import add_product_ops, add_scaled_ops  # noqa: E402
from theorems.rees_coherent_sde import BitSim, Macro, Prog  # noqa: E402
from theorems.rees_coherent_sde_k2 import all_inputs, block_offsets, columns, structured_inputs  # noqa: E402
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa  # noqa: E402


# ====================================================================== flattening

def flat(prog, p, anc):
    cache, out = {}, []
    for it in prog:
        if not isinstance(it, Macro):
            out.append(it)
            continue
        key = (it.kind, it.coeff, it.args)
        ops = cache.get(key)
        if ops is None:
            fn = add_product_ops if it.kind == "add_product" else add_scaled_ops
            ops = fn(p, *[list(r) for r in it.args], it.coeff, anc)
            cache[key] = ops
        out.extend(reversed(ops) if it.inv else ops)
    return out


def gate_targets(g):
    name, q = g
    if name == "x":
        return {q[0]}
    if name == "cx":
        return {q[1]}
    if name == "ccx":
        return {q[2]}
    if name == "swap":
        return set(q)
    raise ValueError(name)


def item_wires(it):
    if isinstance(it, Macro):
        return {w for r in it.args for w in r}
    return set(it[1])


# ====================================================================== independent reference

def factor(n):
    out, q = [], 2
    while q*q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


class Ref:
    """Definition-level canonical witness, written independently of the module."""

    def __init__(self, p, d, contraction=None):
        self.p, self.d = p, d
        self.kappa = k = math.gcd(d, p-1)
        self.h = (p-1)//k
        qs = factor(p-1)
        gam = next(x for x in range(2, p) if all(pow(x, (p-1)//q, p) != 1 for q in qs))
        self.dl = {pow(gam, e, p): e for e in range(p-1)}
        # least g >= 2 whose image generates F_p^x / P: discrete log prime to kappa
        self.g = next(x for x in range(2, p) if math.gcd(self.dl[x], k) == 1)
        self.ginv_mod = pow(self.dl[self.g] % k, -1, k) if k > 1 else 0
        self.u = 1 if self.h == 1 else next(u for u in range(1, self.h+1) if u*(d//k) % self.h == 1)
        roots = {}
        for r in range(p):
            roots.setdefault(pow(r, k, p), r)
        self.root = roots
        if contraction is None:
            contraction = self.lex_contraction()
        self.alpha, self.beta = [int(v) % p for v in contraction[0]], [int(v) % p for v in contraction[1]]
        assert self.valid(self.alpha, self.beta)

    def cos(self, y):
        y %= self.p
        if y == 0:
            return None
        return self.dl[y]*self.ginv_mod % self.kappa

    def in_class(self, val, target):
        c = self.cos(val)
        return c is None or c == target % self.kappa

    def valid(self, alpha, beta):
        k = self.kappa
        return (alpha[0] % self.p == 1 and beta[0] % self.p == 0 and
                all(self.in_class(alpha[j]+beta[i], -(i+j)) for i in range(k) for j in range(k)))

    def all_contractions(self):
        k, p = self.kappa, self.p
        out = []
        for tup in itertools.product(range(p), repeat=2*(k-1)):
            beta = [0, *tup[:k-1]]
            alpha = [1, *tup[k-1:]]
            if self.valid(alpha, beta):
                out.append((tuple(alpha), tuple(beta)))
        return out

    def lex_contraction(self):
        """Least (beta_1..beta_{k-1}, alpha_1..alpha_{k-1}) in lex order: DFS over beta,
        then the least alpha_j per j (independent given beta)."""
        k, p = self.kappa, self.p

        def dfs(i, beta):
            if i == k:
                al = [1]
                for j in range(1, k):
                    t = next((t for t in range(p) if all(self.in_class(t+beta[ii], -(ii+j)) for ii in range(k))),
                             None)
                    if t is None:
                        return None
                    al.append(t)
                return al, beta
            for t in range(p):
                if self.in_class(1+t, -i):
                    r = dfs(i+1, beta+[t])
                    if r is not None:
                        return r
            return None
        r = dfs(1, [0])
        if r is None:
            raise ValueError("no contraction (p in E_2(kappa))")
        return r

    # -- linear algebra by fresh elimination per prefix
    def in_span(self, basis, w):
        """Coordinates c with sum c_i basis_i = w, or None."""
        p = self.p
        n, a = len(basis), len(w)
        if n == 0:
            return [] if not any(x % p for x in w) else None
        A = [[basis[j][r] % p for j in range(n)]+[w[r] % p] for r in range(a)]
        piv_cols, row = [], 0
        for col in range(n):
            pr = next((r for r in range(row, a) if A[r][col]), None)
            if pr is None:
                continue
            A[row], A[pr] = A[pr], A[row]
            iv = pow(A[row][col], -1, p)
            A[row] = [x*iv % p for x in A[row]]
            for r in range(a):
                if r != row and A[r][col]:
                    f = A[r][col]
                    A[r] = [(x-f*y) % p for x, y in zip(A[r], A[row])]
            piv_cols.append(col)
            row += 1
        if any(A[r][n] for r in range(row, a)):
            return None
        c = [0]*n
        for r, col in enumerate(piv_cols):
            c[col] = A[r][n]
        return c

    def first_dep(self, vecs):
        for j in range(len(vecs)):
            c = self.in_span(vecs[:j], vecs[j])
            if c is not None:
                y = [(-x) % self.p for x in c]+[1]+[0]*(len(vecs)-j-1)
                return j, y
        return None

    def run(self, cols):
        p, k = self.p, self.kappa
        a = len(cols[0])
        M = columns(a)
        offs = block_offsets(a)
        V, Ys, Ds, l4 = [], [], [], []
        K = None
        for r in range(a+1):
            blk = [list(cols[offs[r]+i]) for i in range(a+1-r)]
            j, y = self.first_dep(V+blk)
            assert j >= r
            delta = y[r:]
            v = [sum(self.beta[self.cos(dl)]*dl*bl[row] for dl, bl in zip(delta, blk) if dl) % p
                 for row in range(a)]
            in_U = self.in_span(V, v) is not None
            all_P = all(self.cos(dl) == 0 for dl in delta if dl)
            l4.append(in_U == all_P == (not any(v)))
            Ys.append(y)
            Ds.append(delta)
            if in_U:
                K = r
                yprime = self.first_dep(V+[v])[1]
                break
            V.append(v)
        x = [0]*M
        for i, dl in enumerate(Ds[K]):
            if dl:
                x[offs[K]+i] = dl*(1+self.beta[self.cos(dl)]) % p
        tau = [(Ys[K][l]+yprime[l]) % p for l in range(K)]
        zeta = [0]*(a+1)
        za = [0]*(a+1)
        for l in range(K, 0, -1):
            z = tau[l-1]
            zeta[l] = z
            if z == 0:
                continue
            n = self.cos(z)
            za[l] = z*self.alpha[n] % p
            for i, dl in enumerate(Ds[l-1]):
                if dl:
                    x[offs[l-1]+i] = z*dl*(self.alpha[n]+self.beta[self.cos(dl)]) % p
            for j in range(1, l):
                tau[j-1] = (tau[j-1]+z*self.alpha[n]*Ys[l-1][j-1]) % p
        assert all(xi == 0 or self.cos(xi) == 0 for xi in x)
        s = [pow(self.root[xi], self.u, p) for xi in x]
        sig = (K, tuple(tuple(None if dl == 0 else self.cos(dl) for dl in Ds[r]) for r in range(K+1)),
               tuple(None if zeta[l] == 0 else self.cos(zeta[l]) for l in range(1, K+1)))
        return {"K": K, "D": Ds, "zeta": zeta, "za": za, "x": x, "s": s, "l4": all(l4), "sig": sig}


# ====================================================================== the check

def degenerate_inputs(p, a, rng, n_rand=8):
    """Hand-built degenerate column tuples (A[n, row, col])."""
    M = columns(a)
    out = [np.zeros((a, M), dtype=np.int64)]
    for _ in range(n_rand):
        v = rng.integers(0, p, size=a)
        out.append(np.repeat(v[:, None], M, axis=1) % p)                     # all equal
        out.append(np.stack([v*(c % p) for c in range(M)], axis=1) % p)        # multiples 0, 1, 2, ...
        out.append(np.stack([v*(1 if c % 2 == 0 else p-1) for c in range(M)], axis=1) % p)  # +-v
        A = rng.integers(0, p, size=(a, M))
        out.append(A % p)
        for c in range(M):
            B = A.copy()
            B[:, c] = 0
            out.append(B % p)
            if c:
                C = A.copy()
                C[:, c] = C[:, c-1]
                out.append(C % p)
                D = A.copy()
                D[:, c] = (-D[:, c-1]) % p
                out.append(D % p)
        for rk in range(a):
            B = rng.integers(0, p, size=(a, max(rk, 1)))
            C = rng.integers(0, p, size=(max(rk, 1), M))
            out.append((B @ C) % p if rk else np.zeros((a, M), dtype=np.int64))
    for i in range(a):
        E = np.zeros((a, M), dtype=np.int64)
        E[i, :] = 1
        out.append(E)
    return np.array(out, dtype=np.int64)


def trace_check(p, a, d, A, contraction=None, mutate=None, ref=None, label=""):
    t0 = time.time()
    circ = CoherentSDEKappa(p, a, d, contraction=contraction, mutate=mutate)
    ref = ref or Ref(p, d, (circ.const["alpha"], circ.const["beta"]) if contraction is None else contraction)
    # the module's canonical contraction must be the lexicographically least one (own search)
    if contraction is None:
        own = ref.lex_contraction()
        lex_ok = (tuple(own[0]) == tuple(circ.const["alpha"]) and tuple(own[1]) == tuple(circ.const["beta"]))
    else:
        lex_ok = None
    M = circ.M
    N = A.shape[0]
    R = [ref.run([tuple(int(A[n, r, c]) for r in range(a)) for c in range(M)]) for n in range(N)]
    t_ref = time.time()-t0
    Fg = flat(circ.F, p, circ.anc)
    Cg = flat(circ.C, p, circ.anc)
    Ig = flat(circ.F.inverse(), p, circ.anc)
    sim = BitSim(circ.nw, N)
    for c in range(M):
        for r in range(a):
            sim.load(circ.L[c][r], A[:, r, c])
    sim.run(Fg)
    Kv = np.array([q["K"] for q in R])
    res = {}
    # T1
    Fk = np.stack([sim.read([circ.Fk[k]]) for k in range(a+1)], axis=1)
    res["T1_Fk_one_hot_at_K"] = bool(np.array_equal(Fk, (np.arange(a+1)[None, :] == Kv[:, None]).astype(np.int64)))
    # T2
    ok2 = True
    for k in range(a+1):
        mask = Kv >= k
        if not mask.any():
            continue
        for i in range(a+1-k):
            got = sim.read(circ.Ds[k][i])[mask]
            want = np.array([R[n]["D"][k][i] for n in np.nonzero(mask)[0]])
            ok2 &= bool(np.array_equal(got, want))
    res["T2_delta_genuine_rounds"] = ok2
    # T3
    ok3 = True
    for l in range(1, a+1):
        ok3 &= bool(np.array_equal(sim.read(circ.tau[l-1]), np.array([q["zeta"][l] for q in R])))
        ok3 &= bool(np.array_equal(sim.read(circ.ZA[l]), np.array([q["za"][l] for q in R])))
    res["T3_tau_final_and_za"] = ok3
    # T4
    X = np.stack([sim.read(circ.X[i]) for i in range(M)], axis=1)
    res["T4_weights_equal_definition"] = bool(np.array_equal(X, np.array([q["x"] for q in R])))
    # T5
    Sw = {w for r in circ.S for w in r}
    snap = sim.S.copy()
    loc0 = list(sim.loc)
    sim.run(Cg)
    res["T5_copy_stage_changes_only_S"] = all(np.array_equal(sim.S[sim.loc[w]], snap[loc0[w]])
                                              for w in range(circ.nw) if w not in Sw)
    # T6
    sim.run(Ig)
    s = np.stack([sim.read(circ.S[i]) for i in range(M)], axis=1)
    want_s = np.array([q["s"] for q in R])
    sd = np.array([pow(t, d, p) for t in range(p)])[np.minimum(s, p-1)]
    res["T6_S_equals_reference_witness"] = bool(np.array_equal(s, want_s))
    res["T6_labels_restored"] = all(np.array_equal(sim.read(circ.L[c][r]), A[:, r, c])
                                    for c in range(M) for r in range(a))
    res["T6_workspace_zero"] = not any(sim.wire_nonzero(w) for w in range(circ.nw) if w not in circ.io_wires)
    res["T6_s_nonzero"] = bool(s.any(axis=1).all())
    res["T6_equation"] = bool((np.einsum("nrc,nc->nr", A, sd) % p == 0).all())
    res["T6_canonical"] = bool((s < p).all())
    res["L4_lemma4prime_all_genuine_rounds"] = all(q["l4"] for q in R)
    ok = all(v for v in res.values())
    sigs = {q["sig"] for q in R}
    pairs = set()
    for q in R:
        for l in range(1, q["K"]+1):
            if q["zeta"][l]:
                for dl in q["D"][l-1]:
                    pairs.add((ref.cos(q["zeta"][l]), None if dl == 0 else ref.cos(dl)))
    return {"label": label, "p": p, "a": a, "d": d, "kappa": circ.kappa, "u": circ.u, "M": M,
            "alpha": list(circ.alpha), "beta": list(circ.beta), "g": circ.g,
            "lex_least_contraction_matches_own_search": lex_ok,
            "inputs": int(N), "gates_U": len(Fg)*2+len(Cg), "qubits": circ.nw,
            "K_hist": np.bincount(Kv, minlength=a+1).tolist(), "branch_signatures": len(sigs),
            "zeta_delta_class_pairs": len(pairs), "all_pass": ok, **res,
            "seconds": round(time.time()-t0, 1), "ref_seconds": round(t_ref, 1)}


# ====================================================================== static scans

def static_scan(p, a, d):
    circ = CoherentSDEKappa(p, a, d)
    Sw = {w for r in circ.S for w in r}
    Lw = {w for col in circ.L for r in col for w in r}
    out = {"p": p, "a": a, "d": d}
    out["S1_F_touches_no_S_wire"] = not any(item_wires(it) & Sw for it in circ.F)
    sitems = [it for it in circ.C if item_wires(it) & Sw]
    out["S2_C_touches_S_only_by_M_add_scaled_coeff1"] = (
        len(sitems) == circ.M and all(isinstance(it, Macro) and it.kind == "add_scaled" and it.coeff == 1
                                      and set(it.args[0]) <= Sw and not (set(it.args[1]) & Sw)
                                      for it in sitems)
        and sorted(tuple(it.args[0]) for it in sitems) == sorted(tuple(r) for r in circ.S))
    macros = [it for it in circ.prog if isinstance(it, Macro)]
    out["S3_no_macro_target_aliases_an_operand"] = all(not (set(it.args[0]) & {w for r in it.args[1:] for w in r})
                                                       for it in macros)
    out["S3_aliased_operand_products_squarings"] = sum(1 for it in macros if it.kind == "add_product"
                                                       and it.args[1] == it.args[2])
    out["S3_macro_kinds_coeffs"] = sorted({f"{it.kind}:{it.coeff}" for it in macros})
    gates = flat(circ.prog, p, circ.anc)
    tg = set()
    for g in gates:
        tg |= gate_targets(g)
    out["S4_labels_never_target_in_flattened_U"] = not (tg & Lw)
    rawC = [it for it in circ.C if not isinstance(it, Macro)]
    out["S5_raw_gate_kinds_in_C"] = sorted({it[0] for it in rawC})
    out["gates_U"] = len(gates)
    return out


def comparator_check(b):
    """_less_into exhaustively on all pairs of b-bit words, through the module's own method."""
    from theorems.rees_circuit_arith import Anc, anc_size
    nw = 2*b+1+anc_size(b)
    x, y, out = list(range(b)), list(range(b, 2*b)), 2*b
    dummy = type("D", (), {})()
    dummy.anc = Anc(list(range(2*b+1, nw)), b)
    P = Prog()
    CoherentSDEKappa._less_into(dummy, P, x, y, out)
    N = 1 << (2*b)
    idx = np.arange(N, dtype=np.int64)
    xv, yv = idx & ((1 << b)-1), idx >> b
    sim = BitSim(nw, N)
    sim.load(x, xv)
    sim.load(y, yv)
    sim.run(list(P))
    return {"b": b, "pairs": int(N),
            "flag_equals_less": bool(np.array_equal(sim.read([out]), (xv < yv).astype(np.int64))),
            "operands_restored": bool(np.array_equal(sim.read(x), xv) and np.array_equal(sim.read(y), yv)),
            "ancillas_zero": not any(sim.wire_nonzero(w) for w in range(2*b+1, nw))}


# ====================================================================== main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(20261105)
    rows, t0 = [], time.time()
    report = {"rows": rows}

    def dump():
        report["seconds"] = round(time.time()-t0, 1)
        with open(args.out, "w") as f:
            json.dump(report, f, indent=1, default=str)

    def log(r):
        print(json.dumps({k: r[k] for k in ("label", "p", "a", "d", "kappa", "inputs", "all_pass", "seconds")
                          if k in r}), flush=True)

    exhaustive = [(7, 1, 3), (13, 1, 3), (19, 1, 3), (13, 1, 9), (19, 1, 15), (37, 1, 3), (41, 1, 4)]
    if args.quick:
        exhaustive = exhaustive[:2]
    for (p, a, d) in exhaustive:
        r = trace_check(p, a, d, all_inputs(p, a), label="exhaustive")
        rows.append(r)
        log(r)
        dump()
    sampled = [(7, 2, 3, 3000), (13, 2, 3, 1500), (19, 2, 3, 800), (7, 3, 3, 600), (109, 1, 3, 3000),
               (41, 2, 4, 600), (7, 4, 3, 150)]
    for p, a, d, n in ([] if args.quick else sampled):
        A = np.concatenate([structured_inputs(p, a, n, seed=p*100+a), degenerate_inputs(p, a, rng)])
        r = trace_check(p, a, d, A, label="sampled(structured+degenerate)")
        rows.append(r)
        log(r)
        dump()
    # kappa = 6 (composite, two root chains): first prime p = 1 mod 6 outside E_2(6) found by the module
    if not args.quick:
        for p in [q for q in range(7, 200) if all(q % t for t in range(2, int(q**0.5)+1)) and q % 6 == 1]:
            try:
                CoherentSDEKappa(p, 1, 6)
            except ValueError:
                continue
            A = all_inputs(p, 1) if p**3 <= 60000 else np.concatenate([structured_inputs(p, 1, 3000, seed=6),
                                                                      degenerate_inputs(p, 1, rng)])
            r = trace_check(p, 1, 6, A, label="kappa6 first p outside E_2(6)")
            rows.append(r)
            log(r)
            dump()
            break
    # every valid normalised contraction, not only the canonical one
    alt = []
    for p in ([7, 13] if args.quick else [7, 13, 19]):
        ref = Ref(p, 3)
        allc = ref.all_contractions()
        pick = allc if len(allc) <= 6 else [allc[i] for i in sorted(set(np.linspace(0, len(allc)-1, 6).astype(int)))]
        for con in pick:
            r = trace_check(p, 1, 3, all_inputs(p, 1), contraction=con, ref=Ref(p, 3, con),
                            label=f"contraction {con}")
            alt.append({k: r[k] for k in ("p", "alpha", "beta", "inputs", "all_pass")})
            log(r)
        alt.append({"p": p, "number_of_valid_normalised_contractions": len(allc)})
        report["alternative_contractions"] = alt
        dump()
    # mutants (each must FAIL the trace check)
    muts = [{"beta": None}, {"alpha": None}, {"omega_min": True}, {"tau1": 1}, {"out": 2}]
    mres = []
    for m in muts:
        p, a, d = 13, 1, 3
        base = CoherentSDEKappa(p, a, d)
        if "beta" in m:
            m = {"beta": (0, (base.beta[1]+1) % p, base.beta[2])}
        if "alpha" in m:
            m = {"alpha": (1, base.alpha[1], (base.alpha[2]+1) % p)}
        r = trace_check(p, a, d, all_inputs(p, a), mutate=m, ref=Ref(p, d), label=f"mutant {m}")
        mres.append({"mutant": str(m), "detected": not r["all_pass"],
                     "failing": [k for k in r if k[:2] in ("T1", "T2", "T3", "T4", "T5", "T6") and r[k] is False]})
        log(r)
    report["mutants_13_1_3"] = mres
    dump()
    report["static"] = [static_scan(p, a, d) for (p, a, d) in
                        ([(7, 1, 3), (13, 2, 3)] if args.quick else
                         [(7, 1, 3), (7, 2, 3), (13, 2, 3), (19, 1, 3), (7, 3, 3), (41, 1, 4), (109, 2, 3)])]
    dump()
    report["comparator"] = [comparator_check(b) for b in range(2, 9)]
    dump()
    print(json.dumps({"done": True, "all_rows_pass": all(r["all_pass"] for r in rows),
                      "mutants_all_detected": all(m["detected"] for m in mres),
                      "seconds": report["seconds"]}), flush=True)


if __name__ == "__main__":
    main()
