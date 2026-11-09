"""Independent finite checks for the core of the Rees HSP paper (Sections 2-4).

Written for the 2026-11-03 unanchored core check. It does NOT import the
project's simulators: every object (Lie algebras, Rees cover, BCH group,
regular representation, central instrument, merge channel) is rebuilt here
from the definitions printed in docs/papers/rees-hsp/main.tex.

Labels: C1, C2, C6, C7, C8, C10 are exact integer/rational computations.
C3, C4, C5, C9 build complex density matrices and compare to tolerance 1e-9
(float checks). A finite check can only falsify; it proves nothing for all
(G, H).

Run:  /opt/anaconda3/bin/python check_core.py [--quick]
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction

import numpy as np

TOL = 1e-9


# ------------------------------------------------------------------ F_p linear algebra

def rref(rows, p):
    M = [list(int(v) % p for v in r) for r in rows]
    out, col = [], 0
    if not M:
        return []
    ncol = len(M[0])
    r = 0
    for col in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][col]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][col], -1, p)
        M[r] = [v*inv % p for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col]:
                f = M[i][col]
                M[i] = [(a-f*b) % p for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return [tuple(row) for row in M[:r] if any(row)]


def rank(rows, p):
    return len(rref(rows, p))


def in_span(basis, v, p):
    return rank(list(basis)+[v], p) == rank(list(basis), p)


def nullspace(rows, width, p):
    R = rref(rows, p)
    piv = []
    for row in R:
        piv.append(next(j for j, v in enumerate(row) if v))
    free = [j for j in range(width) if j not in piv]
    basis = []
    for f in free:
        v = [0]*width
        v[f] = 1
        for row, pc in zip(R, piv):
            v[pc] = (-row[f]) % p
        basis.append(tuple(v))
    return basis


def solve_coords(basis, v, p):
    """coefficients c with sum c_i basis_i = v (basis independent)."""
    k = len(basis)
    if k == 0:
        return [] if not any(x % p for x in v) else None
    # augmented system: columns = basis vectors
    width = len(v)
    A = [[basis[j][i] for j in range(k)]+[v[i]] for i in range(width)]
    R = rref(A, p)
    sol = [0]*k
    for row in R:
        lead = next(j for j, x in enumerate(row) if x)
        if lead == k:
            return None
        sol[lead] = row[k]
    return sol


def all_subspaces(m, p):
    """every subspace of F_p^m, as an RREF basis (list of tuples)."""
    out = []
    for r in range(m+1):
        for pivots in itertools.combinations(range(m), r):
            free = [(i, j) for i in range(r) for j in range(pivots[i]+1, m) if j not in pivots]
            for vals in itertools.product(range(p), repeat=len(free)):
                rows = [[0]*m for _ in range(r)]
                for i, pc in enumerate(pivots):
                    rows[i][pc] = 1
                for (i, j), v in zip(free, vals):
                    rows[i][j] = v
                out.append([tuple(x) for x in rows])
    return out


# ------------------------------------------------------------------ Lie algebras

class Lie:
    def __init__(self, name, p, dim, brackets):
        self.name, self.p, self.dim = name, p, dim
        T = np.zeros((dim, dim, dim), dtype=np.int64)
        for (i, j), outs in brackets.items():
            for k, v in outs.items():
                T[i, j, k] = v % p
                T[j, i, k] = (-v) % p
        self.T = T

    def br(self, x, y):
        return tuple(int(v) for v in np.einsum("i,j,ijk->k", np.array(x), np.array(y), self.T) % self.p)

    def jacobi_ok(self):
        e = np.eye(self.dim, dtype=np.int64)
        for i, j, k in itertools.product(range(self.dim), repeat=3):
            s = np.zeros(self.dim, dtype=np.int64)
            for a, b, c in ((i, j, k), (j, k, i), (k, i, j)):
                s += np.array(self.br(e[a], self.br(e[b], e[c])))
            if (s % self.p).any():
                return False
        return True

    def lcs(self):
        p, m = self.p, self.dim
        e = [tuple(int(i == j) for j in range(m)) for i in range(m)]
        series = [rref(e, p)]
        while True:
            nxt = rref([self.br(a, b) for a in e for b in series[-1]], p)
            if not nxt:
                return series
            if len(nxt) == len(series[-1]):
                raise ValueError("not nilpotent")
            series.append(nxt)

    def is_subalgebra(self, basis):
        return all(in_span(basis, self.br(a, b), self.p) for a in basis for b in basis)


def heisenberg(p):
    return Lie(f"Heis(F_{p})", p, 3, {(0, 1): {2: 1}})


def filiform4(p):
    return Lie(f"n4(F_{p})", p, 4, {(0, 1): {2: 1}, (0, 2): {3: 1}})


def dixmier_lister(p):
    # main.tex Section 2.3 table, 1-based e_i -> 0-based
    b = {(1, 2): {5: 1}, (1, 3): {6: 1}, (1, 4): {7: 1}, (1, 5): {8: -1},
         (2, 3): {8: 1}, (2, 4): {6: 1}, (2, 6): {7: -1}, (3, 4): {5: -1},
         (3, 5): {7: -1}, (4, 6): {8: -1}}
    return Lie(f"DL(F_{p})", p, 8, {(i-1, j-1): {k-1: v for k, v in o.items()} for (i, j), o in b.items()})


# ------------------------------------------------------------------ Rees cover

class Cover:
    """A = sum_k t^k gamma_k(L) in graded coordinates, plus E_s and delta_lambda."""

    def __init__(self, L, points=None):
        self.L, p = L, L.p
        self.p = p
        self.series = L.lcs()
        self.c = len(self.series)
        self.g = [len(b) for b in self.series]
        self.n = sum(self.g)
        self.grade = []
        self.basisL = []        # L-vector of each cover coordinate
        for k, B in enumerate(self.series, start=1):
            for v in B:
                self.grade.append(k)
                self.basisL.append(v)
        self.offsets = np.cumsum([0]+self.g)
        n = self.n
        T = np.zeros((n, n, n), dtype=np.int64)
        for a in range(n):
            for b in range(n):
                k = self.grade[a]+self.grade[b]
                if k > self.c:
                    continue
                v = L.br(self.basisL[a], self.basisL[b])
                coords = solve_coords(self.series[k-1], v, p)
                assert coords is not None, "bracket left gamma_{i+j}"
                for j, cj in enumerate(coords):
                    T[a, b, self.offsets[k-1]+j] = cj
        self.T = T
        self.points = tuple(points) if points else tuple(range(1, self.c+1))

    def E(self, s):
        """m x n matrix of E_s."""
        p = self.p
        M = np.zeros((self.L.dim, self.n), dtype=np.int64)
        for a in range(self.n):
            M[:, a] = (pow(s, self.grade[a], p)*np.array(self.basisL[a])) % p
        return M

    def delta(self, lam):
        return np.diag([pow(lam, k, self.p) for k in self.grade]).astype(np.int64)

    def lift(self, hbasis):
        """basis of h~ = sum_k t^k (h cap gamma_k), in cover coordinates."""
        p, out = self.p, []
        for k, B in enumerate(self.series, start=1):
            # h cap gamma_k: vectors x = sum c_j B_j with x in span(h)
            hperp = nullspace(hbasis, self.L.dim, p) if hbasis else [tuple(int(i == j) for j in range(self.L.dim)) for i in range(self.L.dim)]
            # c such that <hperp_i, sum c_j B_j> = 0
            rows = [[sum(a*b for a, b in zip(w, Bj)) % p for Bj in B] for w in hperp]
            for cvec in nullspace(rows, len(B), p) if rows else [tuple(int(i == j) for j in range(len(B))) for i in range(len(B))]:
                v = [0]*self.n
                for j, cj in enumerate(cvec):
                    v[self.offsets[k-1]+j] = cj
                out.append(tuple(v))
        return rref(out, p)


# ------------------------------------------------------------------ BCH groups (class <= 3)

class Group:
    def __init__(self, T, p):
        self.T, self.p = T % p, p
        self.n = T.shape[0]
        self.order = p**self.n
        self.w = p**np.arange(self.n-1, -1, -1, dtype=np.int64)
        self.terms = [(int(i), int(j), int(k), int(T[i, j, k])) for i, j, k in zip(*np.nonzero(self.T))]
        self.i2, self.i12 = pow(2, -1, p), (pow(12, -1, p) if p > 3 else 0)  # class < p
        # class check (<= 3 supported)
        self.cls = self._class()
        assert self.cls <= 3 and self.cls < p

    def _class(self):
        e = np.eye(self.n, dtype=np.int64)
        cur = [e[i] for i in range(self.n)]
        k = 1
        while True:
            nxt = [self.br(e[i], x) for i in range(self.n) for x in cur]
            nxt = [x for x in nxt if x.any()]
            if not nxt:
                return k
            cur, k = nxt, k+1
            if k > 6:
                raise ValueError

    def br(self, X, Y):
        out = np.zeros(np.broadcast_shapes(np.shape(X), np.shape(Y)), dtype=np.int64)
        for i, j, k, v in self.terms:
            out[..., k] += v*X[..., i]*Y[..., j]
        return out % self.p

    def mul(self, X, Y):
        X, Y = np.asarray(X, dtype=np.int64), np.asarray(Y, dtype=np.int64)
        xy = self.br(X, Y)
        out = X+Y+self.i2*xy+self.i12*(self.br(X, xy)-self.br(Y, xy))
        return out % self.p

    def inv(self, X):
        return (-np.asarray(X)) % self.p

    def enc(self, X):
        return (np.asarray(X, dtype=np.int64) % self.p) @ self.w

    def dec(self, idx):
        return (np.asarray(idx, dtype=np.int64)[..., None]//self.w) % self.p

    def elements(self):
        return self.dec(np.arange(self.order))

    def span_elements(self, basis):
        basis = np.array(basis, dtype=np.int64).reshape(-1, self.n)
        if len(basis) == 0:
            return np.zeros((1, self.n), dtype=np.int64)
        coeffs = np.array(list(itertools.product(range(self.p), repeat=len(basis))), dtype=np.int64)
        return (coeffs @ basis) % self.p

    def generated(self, gens):
        seen = np.zeros(self.order, dtype=bool)
        seen[0] = True
        frontier = np.zeros((1, self.n), dtype=np.int64)
        gens = np.array(gens, dtype=np.int64).reshape(-1, self.n)
        while len(frontier):
            new = []
            for g in gens:
                idx = self.enc(self.mul(frontier, g[None, :]))
                idx = np.unique(idx[~seen[idx]])
                seen[idx] = True
                new.append(idx)
            frontier = self.dec(np.unique(np.concatenate(new))) if new else frontier[:0]
        return np.nonzero(seen)[0]

    def coset_labels(self, H_elems):
        """lab[x] = min index of the left coset x H (an ordinary hiding function)."""
        lab = -np.ones(self.order, dtype=np.int64)
        X = self.elements()
        for x in range(self.order):
            if lab[x] >= 0:
                continue
            idx = self.enc(self.mul(X[x][None, :], H_elems))
            lab[idx] = x
        return lab


# ------------------------------------------------------------------ checks

def subalgebras(L):
    return [b for b in all_subspaces(L.dim, L.p) if L.is_subalgebra(b)]


def contains(big, small, p):
    return all(in_span(big, v, p) for v in small)


def C1_homogenization(L, points=None, minus_one=False, limit=None):
    """Lemma lem:homogeneous: tuple-oracle fibres are exactly the left cosets of exp(h~)."""
    cov = Cover(L, points)
    p = L.p
    pts = cov.points[:-1] if minus_one else cov.points
    GL, GA = Group(L.T, p), Group(cov.T, p)
    XA = GA.elements()
    Es = [cov.E(s) for s in pts]
    EA = [GL.enc((XA @ E.T) % p) for E in Es]
    res = {"algebra": L.name, "points": list(pts), "cover_dim": cov.n, "subgroups": 0, "ok": 0,
           "mismatch_examples": []}
    subs = subalgebras(L)
    if limit:
        subs = subs[:limit]
    for hb in subs:
        Hel = GL.span_elements(hb)          # log coordinates = group coordinates
        # sanity: span is a subgroup (Lazard, subgroup form)
        assert len(GL.generated(hb if hb else np.zeros((1, L.dim)))) == len(Hel)
        lab = GL.coset_labels(Hel)
        keys = np.stack([lab[e] for e in EA], axis=1)
        # partition of the cover by key
        _, cls = np.unique(keys, axis=0, return_inverse=True)
        cls = cls.ravel()
        ht = cov.lift(hb)
        S = GA.generated(ht if ht else np.zeros((1, cov.n)))
        expected_order = p**len(ht)
        ok = len(S) == expected_order
        # right-invariance under each generator of S
        for g in ht:
            idx = GA.enc(GA.mul(XA, np.array(g)[None, :]))
            ok &= bool((cls[idx] == cls).all())
        nclasses = cls.max()+1
        ok &= nclasses == GA.order//expected_order
        # delta-stability of h~
        for lam in range(2, p):
            D = cov.delta(lam)
            ok &= all(in_span(ht, tuple((D @ np.array(v)) % p), p) for v in ht)
        res["subgroups"] += 1
        res["ok"] += int(ok)
        if not ok and len(res["mismatch_examples"]) < 3:
            res["mismatch_examples"].append({"h": hb, "classes": int(nclasses),
                                             "index_of_Htilde": GA.order//expected_order})
    return res


def C2_single_evaluation(L):
    """Prop prop:single-evaluation over all subalgebras, s, lambda != 1."""
    cov = Cover(L)
    p = L.p
    g2 = cov.series[1] if cov.c >= 2 else []
    rows = {"algebra": L.name, "cases": 0, "agree": 0}
    for hb in subalgebras(L):
        hperp = nullspace(hb, L.dim, p) if hb else [tuple(int(i == j) for j in range(L.dim)) for i in range(L.dim)]
        derived_in_h = contains(hb, g2, p) if hb else not g2
        for s in range(1, p):
            E = cov.E(s)
            cons = [tuple(int(x) for x in (np.array(w) @ E) % p) for w in hperp]
            V = nullspace(cons, cov.n, p) if cons else [tuple(int(i == j) for j in range(cov.n)) for i in range(cov.n)]
            for lam in range(2, p):
                D = cov.delta(lam)
                pres = all(in_span(V, tuple((D @ np.array(v)) % p), p) for v in V)
                rows["cases"] += 1
                rows["agree"] += int(pres == derived_in_h)
    return rows


def regular_rep(G):
    """R[g] as permutation index arrays: R_g |x> = |x g^{-1}>, image index per x."""
    X = G.elements()
    perms = np.empty((G.order, G.order), dtype=np.int64)
    for g in range(G.order):
        perms[g] = G.enc(G.mul(X, G.inv(X[g])[None, :]))
    return perms


def perm_matrix(perm):
    N = len(perm)
    M = np.zeros((N, N))
    M[perm, np.arange(N)] = 1.0
    return M


def coset_state(G, perms, H_idx):
    N = G.order
    rho = np.zeros((N, N))
    for h in H_idx:
        rho[perms[h], np.arange(N)] += 1.0
    return rho/N


def C3_instrument_and_descent(L, M=3, quick=False):
    """Lemma lem:central and Prop prop:descent on the Heisenberg cover, every H,
    every label tuple, every nonzero witness. Also negative controls."""
    p = L.p
    cov = Cover(L)
    assert cov.c == 2
    GA = Group(cov.T, p)
    perms = regular_rep(GA)
    N = GA.order
    omega = np.exp(2j*np.pi/p)
    ztop = [a for a in range(cov.n) if cov.grade[a] == 2]
    assert len(ztop) == 1
    zi = ztop[0]
    Zel = []
    for z in range(p):
        v = np.zeros(cov.n, dtype=np.int64)
        v[zi] = z
        Zel.append(int(GA.enc(v)))
    Rz = [perm_matrix(perms[Zel[z]]) for z in range(p)]
    Pi = [sum(omega**(-lam*z)*Rz[z] for z in range(p))/p for lam in range(p)]
    out = {"algebra": L.name, "subgroups": 0, "projector_ok": True, "law_ok": 0, "state_ok": 0,
           "trace_formula_ok": 0, "descent_cases": 0, "descent_exact": 0,
           "nonwitness_cases": 0, "nonwitness_differs": 0, "examples": []}
    S = sum(Pi)
    out["projector_ok"] = bool(np.allclose(S, np.eye(N), atol=TOL) and all(
        np.allclose(P@P, P, atol=TOL) and np.allclose(P, P.conj().T, atol=TOL) for P in Pi))
    q_coords = [a for a in range(cov.n) if cov.grade[a] == 1]
    Q = list(itertools.product(range(p), repeat=len(q_coords)))
    nQ = len(Q)

    def sigma(q):
        v = np.zeros(cov.n, dtype=np.int64)
        v[q_coords] = q
        return v
    sig = np.array([sigma(q) for q in Q])
    subs = subalgebras(L)
    for hb in subs:
        ht = cov.lift(hb)
        Hel = GA.span_elements(ht)
        Hidx = GA.enc(Hel)
        rho = coset_state(GA, perms, Hidx)
        Kdim = sum(1 for v in ht if cov.grade[next(j for j, x in enumerate(v) if x)] == 2)
        Kset = set(z for z in range(p) if Zel[z] in set(Hidx.tolist()))
        Kperp = [lam for lam in range(p) if all((lam*z) % p == 0 for z in Kset)]
        out["subgroups"] += 1
        # law
        probs = [float(np.real(np.trace(rho@P))) for P in Pi]
        law = all(abs(probs[l]-(len(Kset)/p if l in Kperp else 0.0)) < TOL for l in range(p))
        out["law_ok"] += int(law)
        HZ = set()
        X = GA.elements()
        rho_lam = {}
        st_ok, tr_ok = True, True
        for lam in Kperp:
            r = (rho@Pi[lam])/probs[lam]
            st_ok &= bool(np.allclose(Pi[lam]@rho@Pi[lam]/probs[lam], r, atol=TOL))
            # formula (1/(|G||K|)) sum_{h,z} chi(-z) R_{hz}
            F = np.zeros((N, N), dtype=complex)
            for h in Hel:
                for z in range(p):
                    hz = GA.enc(GA.mul(h, X[Zel[z]]))
                    F[perms[hz], np.arange(N)] += omega**(-lam*z)
            F /= N*len(Kset)
            st_ok &= bool(np.allclose(F, r, atol=TOL))
            rho_lam[lam] = r
            # trace formula for every g
            vals = np.array([r[np.arange(N), perms[g]].sum() for g in range(N)])
            want = np.zeros(N, dtype=complex)
            for z in range(p):
                hcand = GA.enc(GA.mul(X, X[Zel[(-z) % p]][None, :]))   # g z^{-1}
                inH = np.isin(hcand, Hidx)
                want[inH] = omega**(lam*z)
            tr_ok &= bool(np.allclose(vals, want, atol=1e-8))
        out["state_ok"] += int(st_ok)
        out["trace_formula_ok"] += int(tr_ok)
        # expected quotient state: indicator of q - r in t h (grade-one image)
        h1 = [tuple(v[a] for a in q_coords) for v in ht if cov.grade[next(j for j, x in enumerate(v) if x)] == 1]
        expected = np.zeros((nQ, nQ))
        for iq, q in enumerate(Q):
            for ir, rr in enumerate(Q):
                diff = tuple((a-b) % p for a, b in zip(q, rr))
                expected[iq, ir] = 1.0/nQ if in_span(h1, diff, p) else 0.0
        # precompute the merge factors: F_s,lam[q, r] = tr(R_{d(s(r))}^T R_{d(s(q))} rho_lam)
        fac = {}
        for s in range(1, p):
            D = cov.delta(s)
            dsig = (sig @ D.T) % p
            Gpair = GA.enc(GA.mul(GA.inv(dsig)[None, :, :], dsig[:, None, :]))  # [iq, ir]
            for lam in Kperp:
                A = np.zeros((nQ, nQ), dtype=complex)
                for iq in range(nQ):
                    for ir in range(nQ):
                        g = Gpair[iq, ir]
                        # tr(R_g rho) = sum_y rho[y, perm_g[y]]
                        A[iq, ir] = rho_lam[lam][np.arange(N), perms[g]].sum()
                fac[(s, lam)] = A
        for labels in itertools.product(Kperp, repeat=M):
            for svec in itertools.product(range(p), repeat=M):
                if not any(svec):
                    continue
                val = sum(pow(s, 2, p)*l for s, l in zip(svec, labels)) % p
                O = np.ones((nQ, nQ), dtype=complex)/nQ
                for s, l in zip(svec, labels):
                    if s:
                        O = O*fac[(s, l)]
                good = np.allclose(O, expected, atol=1e-8)
                if val == 0:
                    out["descent_cases"] += 1
                    out["descent_exact"] += int(good)
                    if not good and len(out["examples"]) < 3:
                        out["examples"].append({"h": hb, "labels": labels, "s": svec})
                else:
                    out["nonwitness_cases"] += 1
                    out["nonwitness_differs"] += int(not good)
    return out


def C3b_base_group_control(p=3):
    """Negative control: descend on G itself (no cover) with the Heisenberg grading
    dilation, for the non-homogeneous H = <x + z>. Prop descent's hypothesis that
    delta_s preserves H fails, and the output is not rho_{HZ/Z}."""
    L = heisenberg(p)
    G = Group(L.T, p)
    perms = regular_rep(G)
    N = G.order
    omega = np.exp(2j*np.pi/p)
    Zel = [int(G.enc(np.array([0, 0, z]))) for z in range(p)]
    Pi = [sum(omega**(-lam*z)*perm_matrix(perms[Zel[z]]) for z in range(p))/p for lam in range(p)]
    hb = [(1, 0, 1)]
    Hidx = G.enc(G.span_elements(hb))
    rho = coset_state(G, perms, Hidx)
    Q = list(itertools.product(range(p), repeat=2))
    sig = np.array([[a, b, 0] for a, b in Q])
    expected = np.zeros((len(Q), len(Q)))
    for iq, q in enumerate(Q):
        for ir, r in enumerate(Q):
            d = ((q[0]-r[0]) % p, (q[1]-r[1]) % p)
            expected[iq, ir] = 1.0/len(Q) if in_span([(1, 0)], d, p) else 0.0
    bad = 0
    total = 0
    for labels in itertools.product(range(p), repeat=3):
        for svec in itertools.product(range(p), repeat=3):
            if not any(svec) or sum(s*s*l for s, l in zip(svec, labels)) % p:
                continue
            O = np.ones((len(Q), len(Q)), dtype=complex)/len(Q)
            for s, l in zip(svec, labels):
                if not s:
                    continue
                r_l = rho@Pi[l]
                pr = np.real(np.trace(r_l))
                r_l = r_l/pr
                D = np.diag([s, s, s*s]) % p
                ds = (sig @ D.T) % p
                A = np.zeros((len(Q), len(Q)), dtype=complex)
                for iq in range(len(Q)):
                    for ir in range(len(Q)):
                        g = G.enc(G.mul(G.inv(ds[ir]), ds[iq]))
                        A[iq, ir] = r_l[np.arange(N), perms[g]].sum()
                O = O*A
            total += 1
            bad += int(not np.allclose(O, expected, atol=1e-8))
    return {"group": f"Heis(F_{p}) itself, H=<x+z>", "witness_cases": total, "output_wrong": bad}


def C4_copy_lift(L):
    """Lemma lem:copy-lift: c copies of rho_H on G -> rho_{exp h~} on the cover."""
    p = L.p
    cov = Cover(L)
    GL, GA = Group(L.T, p), Group(cov.T, p)
    permL = regular_rep(GL)
    XA = GA.elements()
    EA = [GL.enc((XA @ cov.E(s).T) % p) for s in cov.points]
    ok, tot = 0, 0
    XL = GL.elements()
    for hb in subalgebras(L):
        Hidx = GL.enc(GL.span_elements(hb))
        rho = coset_state(GL, permL, Hidx)
        # T[g] = tr(R_g rho)
        trR = np.array([rho[np.arange(GL.order), permL[g]].sum() for g in range(GL.order)])
        Hset = set(GA.enc(GA.span_elements(cov.lift(hb))).tolist())
        good = True
        for a in range(GA.order):
            for b in range(GA.order):
                val = 1.0/GA.order
                for i in range(cov.c):
                    ga, gb = XL[EA[i][a]], XL[EA[i][b]]
                    g = GL.enc(GL.mul(GL.inv(gb), ga))
                    val *= trR[g]
                want = (1.0/GA.order) if int(GA.enc(GA.mul(GA.inv(XA[b]), XA[a]))) in Hset else 0.0
                if abs(val-want) > 1e-12:
                    good = False
                    break
            if not good:
                break
        tot += 1
        ok += int(good)
    return {"algebra": L.name, "subgroups": tot, "exact": ok}


def C5_refresh_counterexample(p=5):
    omega = np.exp(2j*np.pi/p)
    chi = [np.array([omega**(k*x) for x in range(p)])/np.sqrt(p) for k in range(p)]
    inv2 = pow(2, -1, p)
    bank = sum(np.kron(np.outer(chi[k], chi[k].conj()), np.outer(chi[(-k*inv2) % p], chi[(-k*inv2) % p].conj()))
               for k in range(p))/p
    marg1 = np.trace(bank.reshape(p, p, p, p), axis1=1, axis2=3)
    marg2 = np.trace(bank.reshape(p, p, p, p), axis1=0, axis2=2)
    shift = lambda g: perm_matrix(np.array([(x+g) % p for x in range(p)]))  # L_g
    Rg = lambda g: perm_matrix(np.array([(x-g) % p for x in range(p)]))     # R_g|x> = |x-g>
    tw = sum(np.kron(shift(a), shift(b)) @ bank @ np.kron(shift(a), shift(b)).T for a in range(p) for b in range(p))/p**2
    out = np.zeros((p, p), dtype=complex)
    for a in range(p):
        for b in range(p):
            Ua, Ub = np.kron(Rg(a), Rg(2*a % p)), np.kron(Rg(b), Rg(2*b % p))
            out[a, b] = np.trace(Ua @ bank @ Ub.conj().T)/p
    return {"marginals_maximally_mixed": bool(np.allclose(marg1, np.eye(p)/p) and np.allclose(marg2, np.eye(p)/p)),
            "twirl_invariant": bool(np.allclose(tw, bank)),
            "lift_output_is_uniform_projector": bool(np.allclose(out, np.ones((p, p))/p)),
            "lift_output_is_I_over_p": bool(np.allclose(out, np.eye(p)/p))}


def C6_rank_bound():
    """Rank third: P(m+t uniform vectors of F_p^e fail to span) <= 1/((p-1)p^t) <= eps/3."""
    worst = Fraction(0)
    cases = 0
    viol = []
    for p in (2, 3, 5, 7, 11):
        for m in range(1, 9):
            for eps in (Fraction(1, 3), Fraction(1, 10), Fraction(1, 1000), Fraction(9, 10)):
                t = 0
                while Fraction(p)**t < 3/eps:
                    t += 1
                Nn = m+t
                bound = Fraction(1, (p-1)*p**t)
                for e in range(0, m+1):
                    succ = Fraction(1)
                    for i in range(e):
                        succ *= 1-Fraction(p)**i/Fraction(p)**Nn
                    fail = 1-succ
                    cases += 1
                    if fail > bound or bound > eps/3:
                        viol.append((p, m, str(eps), e))
                    worst = max(worst, fail/bound if bound else 0)
    return {"cases": cases, "violations": viol, "max_fail_over_bound": float(worst)}


def B(d, a):
    return (d**(d*(d-1)//2)*(a+1)**d)**math.ceil(math.log2(d+1))


def ceil_log2(x):
    return (x-1).bit_length()


def B_exact(d, a):
    return (d**(d*(d-1)//2)*(a+1)**d)**ceil_log2(d+1)


def C7_query_count():
    """Displayed count after thm:main and its (m+1)-power bound; exponent 145 at c = 9;
    monotonicity B_k(a) <= B_d(a) for k <= d (the kappa_d reduction)."""
    res = {"bound_violations": [], "exp_c9": None, "monotone_violations": []}
    for c in range(2, 8):
        expo = sum(d*ceil_log2(d+1) for d in range(2, c+1))
        Cc = 1
        for d in range(2, c+1):
            num = d*(d-1)*ceil_log2(d+1)
            assert num % 2 == 0
            Cc *= d**(num//2)
        for m in range(c, 12):
            for gs in itertools.product(range(1, m+1), repeat=c-1):
                if any(gs[i] < gs[i+1] for i in range(len(gs)-1)) or gs[0] > m-1:
                    continue  # g_2 >= g_3 >= ... and g_2 < m
                prod = 1
                for d, g in zip(range(2, c+1), gs):
                    prod *= B_exact(d, g)
                for t in (1, 2, 5):
                    lhs = c*(m+t)*prod
                    rhs = Cc*c*(m+t)*(m+1)**expo
                    if lhs > rhs:
                        res["bound_violations"].append((c, m, gs, t))
    res["exp_c9"] = 1+sum(d*ceil_log2(d+1) for d in range(2, 10))
    for d in range(1, 13):
        for k in range(1, d+1):
            for a in range(0, 60):
                bk = a+1 if k == 1 else B_exact(k, a)
                if bk > B_exact(d, a) and d >= 2:
                    res["monotone_violations"].append((k, d, a))
    # ceil(log2) as float vs exact agrees for d <= 64
    res["ceil_log2_float_agrees"] = all(math.ceil(math.log2(d+1)) == ceil_log2(d+1) for d in range(1, 65))
    return res


def C8_dixmier_lister():
    out = {}
    for p in (5, 7, 11, 13, 17, 19, 23):
        L = dixmier_lister(p)
        jac = L.jacobi_ok()
        dims = [len(b) for b in L.lcs()]
        # derivations: D e_i = sum_k D[k,i] e_k ; D[e_i,e_j] = [De_i,e_j] + [e_i,De_j]
        m = 8
        rows = []
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    # coefficient of e_k in  D([e_i,e_j]) - [De_i, e_j] - [e_i, De_j]
                    r = [0]*(m*m)
                    for l in range(m):          # [e_i,e_j] = sum_l T[i,j,l] e_l -> D e_l
                        if L.T[i, j, l]:
                            r[k*m+l] += int(L.T[i, j, l])
                    for l in range(m):          # De_i = sum_l D[l,i] e_l ; [e_l, e_j]_k
                        if L.T[l, j, k]:
                            r[l*m+i] -= int(L.T[l, j, k])
                        if L.T[i, l, k]:
                            r[l*m+j] -= int(L.T[i, l, k])
                    rows.append([v % p for v in r])
        Dbasis = nullspace(rows, m*m, p)
        derived = L.lcs()[1]
        ok_into_derived = True
        ok_nil = True
        for v in Dbasis:
            D = np.array(v, dtype=np.int64).reshape(m, m)  # D[k,i]
            for i in range(m):
                col = tuple(int(x) for x in D[:, i] % p)
                ok_into_derived &= in_span(derived, col, p)
            ok_nil &= not (np.linalg.matrix_power(D, 3) % p).any()
        # random combination nilpotent too (sum of basis)
        Dsum = sum(np.array(v, dtype=np.int64).reshape(m, m) for v in Dbasis) % p
        cov = Cover(L)
        out[p] = {"jacobi": jac, "lcs_dims": dims, "cover_dim": cov.n,
                  "derivation_dim": len(Dbasis), "system_rank": 64-len(Dbasis),
                  "all_basis_derivations_into_derived": ok_into_derived,
                  "basis_D_cubed_zero": ok_nil,
                  "sum_D_cubed_zero": not (np.linalg.matrix_power(Dsum, 3) % p).any()}
    return out


def C10_homomorphisms(L, samples=4000, seed=1):
    """thm:rees-cover (ii)-(iii): E_s and delta_lambda are BCH homomorphisms; the
    cover product is associative. Exhaustive when the cover is small."""
    p = L.p
    cov = Cover(L)
    GL, GA = Group(L.T, p), Group(cov.T, p)
    rng = np.random.default_rng(seed)
    if GA.order**2 <= 10**6:
        X = GA.elements()
        A = np.repeat(X, GA.order, axis=0)
        Bm = np.tile(X, (GA.order, 1))
        mode = "exhaustive pairs"
    else:
        A = rng.integers(0, p, size=(samples, cov.n))
        Bm = rng.integers(0, p, size=(samples, cov.n))
        mode = f"{samples} random pairs"
    Cm = rng.integers(0, p, size=A.shape)
    ok = True
    AB = GA.mul(A, Bm)
    for s in range(0, p):
        E = cov.E(s)
        ok &= bool(((AB @ E.T) % p == GL.mul((A @ E.T) % p, (Bm @ E.T) % p)).all())
    for lam in range(1, p):
        D = cov.delta(lam)
        ok &= bool(((AB @ D.T) % p == GA.mul((A @ D.T) % p, (Bm @ D.T) % p)).all())
        for s in range(0, p):
            ok &= bool((((cov.E(s) @ D) % p) == cov.E(lam*s % p)).all())
    assoc = bool((GA.mul(AB, Cm) == GA.mul(A, GA.mul(Bm, Cm))).all())
    # Lie homomorphism on basis pairs
    lie_ok = True
    for s in range(p):
        E = cov.E(s)
        for a in range(cov.n):
            for b in range(cov.n):
                ea, eb = np.eye(cov.n, dtype=np.int64)[a], np.eye(cov.n, dtype=np.int64)[b]
                lhs = (E @ GA.br(ea, eb)) % p
                rhs = np.array(L.br(tuple(E @ ea % p), tuple(E @ eb % p)))
                lie_ok &= bool((lhs == rhs).all())
    return {"algebra": L.name, "cover_dim": cov.n, "class": cov.c, "mode": mode,
            "E_and_delta_group_homs": ok, "associative": assoc, "E_Lie_hom_on_basis": lie_ok}


def main():
    quick = "--quick" in sys.argv
    R = {}
    R["C10_homomorphisms"] = [C10_homomorphisms(L) for L in (heisenberg(3), heisenberg(5), filiform4(5), filiform4(7))]
    R["C1_homogenization"] = [C1_homogenization(heisenberg(3)), C1_homogenization(heisenberg(5)),
                              C1_homogenization(heisenberg(5), points=(2, 4)),
                              C1_homogenization(filiform4(5)),
                              C1_homogenization(filiform4(5), points=(2, 3, 4))]
    R["C1_negative_c_minus_1_points"] = [C1_homogenization(heisenberg(3), minus_one=True),
                                         C1_homogenization(filiform4(5), minus_one=True)]
    R["C2_single_evaluation"] = [C2_single_evaluation(L) for L in (heisenberg(3), heisenberg(5), filiform4(5))]
    R["C3_instrument_descent"] = [C3_instrument_and_descent(heisenberg(3), M=3)]
    if not quick:
        R["C3_instrument_descent"].append(C3_instrument_and_descent(heisenberg(5), M=2))
    R["C3b_base_group_negative_control"] = C3b_base_group_control(3)
    R["C4_copy_lift"] = [C4_copy_lift(heisenberg(3))]
    R["C5_refresh_counterexample"] = C5_refresh_counterexample(5)
    R["C6_rank_bound"] = C6_rank_bound()
    R["C7_query_count"] = C7_query_count()
    R["C8_dixmier_lister"] = C8_dixmier_lister()
    print(json.dumps(R, indent=1, default=str))


if __name__ == "__main__":
    main()
