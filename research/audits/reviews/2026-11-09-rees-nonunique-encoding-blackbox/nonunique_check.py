"""Finite control for the free-cover route with NON-unique encodings (9 Nov 2026, AI only).

Run from the repo root:
    nice -n 19 /opt/anaconda3/bin/python \
      research/audits/reviews/2026-11-09-rees-nonunique-encoding-blackbox/nonunique_check.py

Black box. Each group element (a hidden permutation) has k in {2,3,4} random 40-bit strings.
The multiplication oracle maps a PAIR OF STRINGS to one encoding of the product, chosen
pseudo-randomly but deterministically from the input strings. The algorithm side gets the
generator strings and this oracle only: no identity test, no inverse oracle, no equality of
strings is ever used as a group-element test. The hiding function f is a function of the
element (left coset label), as the model requires.

What it checks.
  A. Exponent p (groups_exp_p.txt): the instance (F_{s,c}(F_p), f o Phi) of
     Definition def:input-contract, with Phi the free Lazard pullback evaluated on strings.
     Graded: f o Phi hides Phi^{-1}(H) (sampled pairs, BCH product), Phi^{-1}(H) is a Lie
     subalgebra containing ker Phi, and the push-forward of its basis generates H. The field
     solver is an ORACLE-ONLY brute force on f o Phi (stand-in for Theorem thm:main; it is NOT
     Theorem thm:main). The thm:main query bound at m = d is tallied.
  B. Exponent p^e (../2026-11-09-rees-exponent-pe-blackbox/groups.txt, small cases): Algorithm
     RtF (Prop tb-recursion) on the free ring F_{s,c}(Z/M) itself (K' = 0), with M the exponent
     and, separately, M = p * exponent (a known multiple, as p^L would be). Brute-force field
     solver as above; every field call validated as an instance of def:input-contract.
  C. Why the kernel step of cor:black-box fails: the exact Fourier law of u -> string(Phi(u))
     (numpy FFT over F_p^d), its mass on (ker Phi)^perp (1 under unique encodings), and the
     Lemma tb-kernel readout from t samples of that law.
Ground truth (hidden permutations) is used only to build f and to grade. Finite check: it
proves nothing for other groups.
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
from theorems.universal_lazard_words import UniversalLazardWords  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "pe", HERE.parent / "2026-11-09-rees-exponent-pe-blackbox" / "exponent_pe_check.py")
pe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pe)
FreeLieZ, ChartRing, parse_groups, pad = pe.FreeLieZ, pe.ChartRing, pe.parse_groups, pe.pad
schedule1_queries, lcs_dims_fp, mods_basis = pe.schedule1_queries, pe.lcs_dims_fp, pe.mods_basis


class NonUniqueBox:
    def __init__(self, gens, seed):
        self.rng = random.Random(seed)
        self.encs, self.key, self.memo = {}, {}, {}
        self.calls = 0
        self.generators = [self._some(tuple(g)) for g in gens]

    def _encs(self, perm):
        e = self.encs.get(perm)
        if e is None:
            e = []
            for _ in range(self.rng.choice((2, 3, 4))):
                while True:
                    h = self.rng.getrandbits(40)
                    if h not in self.key:
                        break
                self.key[h] = perm
                e.append(h)
            self.encs[perm] = e
        return e

    def _some(self, perm):
        return self.rng.choice(self._encs(perm))

    def mul(self, x, y):  # the oracle: a deterministic function of the two STRINGS
        self.calls += 1
        r = self.memo.get((x, y))
        if r is None:
            a, b = self.key[x], self.key[y]
            r = self._some(tuple(b[i] for i in a))
            self.memo[(x, y)] = r
        return r

    # grading only
    def elt(self, h):
        return self.key[h]

    @staticmethod
    def pmul(a, b):
        return tuple(b[i] for i in a)

    def closure(self, perms, deg):
        e = tuple(range(deg))
        seen, frontier = {e}, [e]
        while frontier:
            new = []
            for g in frontier:
                for s in perms:
                    h = self.pmul(g, s)
                    if h not in seen:
                        seen.add(h)
                        new.append(h)
            frontier = new
        return seen


def pow_noid(box, x, n):
    """x^n for n >= 1 by multiplications only (no identity encoding needed)."""
    acc, base = None, x
    while n:
        if n & 1:
            acc = base if acc is None else box.mul(acc, base)
        n >>= 1
        if n:
            base = box.mul(base, base)
    return acc


def coset_labels(G, Hset):
    label, nxt = {}, 0
    for x in G:
        if x not in label:
            for y in Hset:
                label[NonUniqueBox.pmul(x, y)] = nxt
            nxt += 1
    return label


def setup(g, M, rng):
    p, c, deg = g["p"], g["cls"], g["deg"]
    box = NonUniqueBox([pad(x, deg) for x in g["gens"]], seed=rng.getrandbits(32))
    s = len(box.generators)
    one = pow_noid(box, box.generators[0], M)  # an encoding of 1, by multiplication only
    W = UniversalLazardWords(p, c, one, box.mul, modulus=M)
    F = FreeLieZ(s, c)
    img = {}
    for w in sorted(F.words, key=len):
        if len(w) == 1:
            img[w] = box.generators[w[0]]
        else:
            u, v = pe.std_factor(w)
            img[w] = W.lie_bracket(img[u], img[v])
    hgen = [img[w] for w in F.words]
    T = [[[x % M for x in row] for row in F.table[i]] for i in range(F.d)]
    L = ChartRing(p, [M] * F.d, T, c)
    elems = L.elements()
    Phi = {t: W.linear_combination(hgen, list(t)) for t in elems}  # strings
    return box, F, L, elems, Phi


def kernel_law(p, d, elems, Phi, Kset, rng, tsamp, trials=20):
    """Exact Fourier law of u -> |string(Phi(u))>, over F_p^d (exponent p only)."""
    shape = (p,) * d
    fib = {}
    for t, h in Phi.items():
        fib.setdefault(h, []).append(t)
    P = np.zeros(shape)
    for pts in fib.values():
        a = np.zeros(shape)
        for t in pts:
            a[t] = 1.0
        P += np.abs(np.fft.fftn(a)) ** 2
    P /= float(p ** d) ** 2
    assert abs(P.sum() - 1) < 1e-9
    Kb = list(Kset)
    perp = np.zeros(shape, dtype=bool)
    for chi in elems:
        perp[chi] = all(sum(a * b for a, b in zip(chi, k)) % p == 0 for k in Kb)
    mass = float(P[perp].sum())
    flat = P.reshape(-1)
    flat = flat / flat.sum()
    idx = np.arange(flat.size)
    eq = sub = 0
    for _ in range(trials):
        S = [np.unravel_index(i, shape) for i in rng.choices(idx, weights=flat, k=tsamp)]
        Kp = {t for t in elems if all(sum(a * b for a, b in zip(t, chi)) % p == 0 for chi in S)}
        eq += int(Kp == Kset)
        sub += int(Kp < Kset)
    return mass, len(fib), eq, sub


def run_exp_p(g, rng, eps=0.1, log=print):
    t0 = time.time()
    p, c, deg = g["p"], g["cls"], g["deg"]
    M = p
    box, F, L, elems, Phi = setup(g, M, rng)
    d = F.d
    Gperm = box.closure([tuple(pad(x, deg)) for x in g["gens"]], deg)
    assert len(Gperm) == g["order"]
    E = {t: box.elt(h) for t, h in Phi.items()}  # grading only
    assert set(E.values()) == Gperm, "Phi not onto"
    ident = tuple(range(deg))
    Kset = {t for t in elems if E[t] == ident}
    nstrings_used = len(set(Phi.values()))
    for _ in range(300):
        x, y = rng.choice(elems), rng.choice(elems)
        assert E[L.bch(x, y)] == box.pmul(E[x], E[y]), "Phi not a homomorphism"
    # Part C: kernel step under non-unique strings
    tsamp = min(d, math.floor(40 / math.log2(p))) + math.ceil(math.log(8 / eps, p))
    if p ** d <= 3125:
        mass, nfib, eq, sub = kernel_law(p, d, elems, Phi, Kset, rng, tsamp)
    else:
        mass, nfib, eq, sub = None, None, None, None
    gds = [len([w for w in F.words if len(w) >= k]) for k in range(2, c + 1)]
    qbound = schedule1_queries(c, d, gds, eps / 2, p)
    ok = nsub = 0
    for sg in g["subs"]:
        Hp = [tuple(pad(x, deg)) for x in sg]
        Hset = box.closure(Hp, deg)
        label = coset_labels(Gperm, Hset)
        fo = {t: label[box.elt(Phi[t])] for t in elems}  # f o Phi, f a function of strings
        Ut = {t for t in elems if E[t] in Hset}  # Phi^{-1}(H), grading
        for _ in range(150):
            x, y = rng.choice(elems), rng.choice(elems)
            assert (fo[x] == fo[y]) == (L.bch(L.neg(x), y) in Ut), "f o Phi does not hide"
        U = {t for t in elems if fo[t] == fo[L.zero]}  # brute-force stand-in for thm:main
        assert U == Ut and Kset <= U
        assert all(L.br(x, y) in U for x in list(U)[:40] for y in list(U)[:40])
        basis, span = [], {L.zero}
        for u in sorted(U):
            if u not in span:
                basis.append(u)
                span = {L.add(y, L.smul(a, u)) for y in span for a in range(p)}
        assert span == U
        out = box.closure([box.elt(Phi[u]) for u in basis], deg) if basis else {ident}
        nsub += 1
        ok += int(out == Hset)
    res = dict(part="A", tag=g["tag"], p=p, order=g["order"], cls=c, s=len(box.generators),
               d=d, dimK=round(math.log(len(Kset), p)), strings_for_Phi=nstrings_used,
               fourier_mass_on_Kperp=None if mass is None else round(mass, 4),
               fibres=nfib, t_samples=tsamp, readout_eq_K=eq, readout_strictly_inside_K=sub,
               subs=nsub, ok=ok, thm_main_bound_m_d=qbound,
               identity_tests=0, mults=box.calls, seconds=round(time.time() - t0, 1))
    log(json.dumps(res))
    return res


def run_exp_pe(g, M, rng, eps=0.1, log=print):
    t0 = time.time()
    p, c, deg = g["p"], g["cls"], g["deg"]
    box, F, L, elems, Phi = setup(g, M, rng)
    d = F.d
    Gperm = box.closure([tuple(pad(x, deg)) for x in g["gens"]], deg)
    E = {t: box.elt(h) for t, h in Phi.items()}
    assert set(E.values()) == Gperm
    for _ in range(300):
        x, y = rng.choice(elems), rng.choice(elems)
        assert E[L.bch(x, y)] == box.pmul(E[x], E[y]), "Phi not a homomorphism"
    b = d * round(math.log(M, p))
    pE = {t: L.smul(p, t) for t in elems}
    stats = dict(subs=0, ok=0, calls_max=0, instances=0, nonabelian_instances=0)
    for sg in g["subs"]:
        Hset = box.closure([tuple(pad(x, deg)) for x in sg], deg)
        label = coset_labels(Gperm, Hset)
        f = lambda t: label[box.elt(Phi[t])]
        hset = {t for t in elems if E[t] in Hset}
        K, gensK, S = {L.zero}, [], set(elems)
        calls = 0
        while S != K:
            P = [x for x in S if pE[x] in K]
            span, coord, basis = set(K), {k: () for k in K}, []
            for x in P:
                if x in span:
                    continue
                basis.append(x)
                newspan, newcoord = set(), {}
                for y in span:
                    for a in range(p):
                        z = L.add(y, L.smul(a, x))
                        newspan.add(z)
                        newcoord[z] = coord[y] + (a,)
                coord = {z: v + (0,) * (len(basis) - len(v)) for z, v in newcoord.items()}
                span = newspan
            k = len(basis)
            assert set(P) == span

            def lift(a):
                z = L.zero
                for ai, bi in zip(a, basis):
                    z = L.add(z, L.smul(ai, bi))
                return z
            co = lambda z: coord[z]
            Tw = [[list(co(L.br(basis[i], basis[j]))) for j in range(k)] for i in range(k)]
            gds = lcs_dims_fp(Tw, k, p, c)
            Om = ChartRing(p, [p] * k, Tw, c)
            vecs = Om.elements()
            for _ in range(40):
                x, y, z = rng.choice(vecs), rng.choice(vecs), rng.choice(vecs)
                jac = Om.add(Om.add(Om.br(x, Om.br(y, z)), Om.br(y, Om.br(z, x))),
                             Om.br(z, Om.br(x, y)))
                assert jac == Om.zero
                assert co(L.bch(lift(x), lift(y))) == Om.bch(x, y)
            assert K <= hset <= S
            Utrue = {co(z) for z in hset & set(P)}
            fo = {a: f(lift(a)) for a in vecs}
            for _ in range(100):
                x, y = rng.choice(vecs), rng.choice(vecs)
                assert (fo[x] == fo[y]) == (Om.bch(Om.neg(x), y) in Utrue), "not hiding"
            stats["instances"] += 1
            stats["nonabelian_instances"] += int(any(gds))
            U = {a for a in vecs if fo[a] == fo[Om.zero]}
            calls += 1
            assert U == Utrue
            if U == {Om.zero} or any(Om.br(x, y) not in U for x in U for y in U):
                break
            Kn = {z for z in P if co(z) in U}
            ubasis, uspan = [], {Om.zero}
            for u in sorted(U):
                if u not in uspan:
                    ubasis.append(u)
                    uspan = {Om.add(y, Om.smul(a, u)) for y in uspan for a in range(p)}
            gensK = gensK + [lift(u) for u in ubasis]
            Sn = {x for x in S if all(L.br(x, gk) in Kn for gk in gensK)}
            assert Kn <= hset <= Sn
            K, S = Kn, Sn
        assert calls <= b
        out = box.closure([box.elt(Phi[x]) for x in gensK], deg) if gensK else {tuple(range(deg))}
        stats["subs"] += 1
        stats["ok"] += int(out == Hset)
        stats["calls_max"] = max(stats["calls_max"], calls)
    res = dict(part="B", tag=g["tag"], p=p, order=g["order"], cls=c, exponent=g["exp"], M=M,
               s=len(box.generators), d=d, cap_b=b, identity_tests=0, mults=box.calls,
               seconds=round(time.time() - t0, 1), **stats)
    log(json.dumps(res))
    return res


def main():
    rng = random.Random(20261109)
    out = open(HERE / "results.jsonl", "w")
    log = lambda s: (print(s, flush=True), out.write(s + "\n"), out.flush())
    res = []
    for g in parse_groups(HERE / "groups_exp_p.txt"):
        d = FreeLieZ(len(g["gens"]), g["cls"]).d
        if g["p"] ** d > 20000:
            log(json.dumps(dict(part="A", tag=g["tag"], skipped=f"|F| = {g['p']}^{d}")))
            continue
        res.append(run_exp_p(g, rng, log=log))
    for g in parse_groups(HERE.parent / "2026-11-09-rees-exponent-pe-blackbox" / "groups.txt"):
        d = FreeLieZ(len(g["gens"]), g["cls"]).d
        for M in (g["exp"], g["p"] * g["exp"]):
            if M ** d <= 20000 and len(g["subs"]) <= 400:
                res.append(run_exp_pe(g, M, rng, log=log))
    A = [r for r in res if r["part"] == "A"]
    B = [r for r in res if r["part"] == "B"]
    log(f"SUMMARY A groups={len(A)} subgroups={sum(r['subs'] for r in A)} "
        f"recovered={sum(r['ok'] for r in A)}; B runs={len(B)} "
        f"subgroups={sum(r['subs'] for r in B)} recovered={sum(r['ok'] for r in B)} "
        f"instances={sum(r['instances'] for r in B)} "
        f"nonabelian={sum(r['nonabelian_instances'] for r in B)}; identity tests used: 0")


if __name__ == "__main__":
    main()
