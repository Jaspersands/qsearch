"""Item 3 (campaign 4): Lemma app-sub-lift, Corollary app-sub-cancel, Remark app-sub-multiple-p.

Groups: Heis(F_3), Heis(F_5) (class 2) and the class-3 filiform group of
dimension 4 over F_5, with R the right regular representation on C[G] and
V = span{v_1, v_2} (r = 2), v_i = sum_h psi0(h)^{-1} R(h) w_i for a nontrivial
linear character psi0 of H.  Then chi = det(R|_V) = psi0^2 on H.
For each H we check (complex128):
  * stab(V) = H by enumeration, and the exact gap delta;
  * Phi = 1 on the whole of H~ with a zero-moment design, |Phi| <= 1 - delta^2/2
    (and <= (1-delta^2)^{r/2}) off H~;
  * for Heis: sigma_{S,l} as a p^n x p^n matrix: trace 1, PSD, and the exact
    TD(sigma, rho_{H~}) against the bound (1/2) p^{n/2} (1-gamma)^l;
  * falsifier: c distinct points that are not a design give |Phi - 1| > 0 on H~;
  * Remark multiple-p: the same points with l a multiple of p give Phi^l = 1 on H~.
Run: /opt/anaconda3/bin/python check_lift.py
"""
import itertools

import numpy as np

from check_character import Lie, heis, filiform

rng = np.random.default_rng(2026)


class Group:
    def __init__(self, L):
        self.L = L
        self.elts = list(itertools.product(range(L.p), repeat=L.n))
        self.idx = {g: i for i, g in enumerate(self.elts)}

    def mul(self, a, b):
        return self.L.bch(a, b)

    def inv(self, a):
        return self.L.neg(a)


def cover(L, gamma_dims):
    """positive Rees cover for an L whose gamma_k is spanned by the last g_k basis vectors."""
    n0 = L.n
    c = len(gamma_dims)
    basis = [(k, i) for k in range(1, c + 1) for i in range(n0 - gamma_dims[k - 1], n0)]
    pos = {b: t for t, b in enumerate(basis)}
    br = {}
    for (k1, i), (k2, j) in itertools.product(basis, repeat=2):
        if (i, j) in L.T and k1 + k2 <= c:
            vec = {}
            for kk, coef in L.T[(i, j)].items():
                assert (k1 + k2, kk) in pos, "bracket leaves gamma_{k1+k2}"
                vec[pos[(k1 + k2, kk)]] = coef
            br[(pos[(k1, i)], pos[(k2, j)])] = vec
    A = Lie(L.p, len(basis), {}, "cover", L.cls)
    A.T = br

    def E(s, a):
        out = [0] * n0
        for t, (k, i) in enumerate(basis):
            if a[t]:
                out[i] = (out[i] + pow(s, k, L.p) * a[t]) % L.p
        return tuple(out)

    return A, basis, E


def subspace_elements(L, gens):
    from check_character import subalgebra_closure, elements
    return elements(L, subalgebra_closure(L, gens))


def run_case(name, L, gamma_dims, hgens, lam, designs, falsifier, do_sigma, r=2, samples=None):
    p = L.p
    G = Group(L)
    N = len(G.elts)
    Hset = subspace_elements(L, hgens)
    Hl = sorted(Hset)
    omega = np.exp(2j * np.pi / p)
    psi0 = {h: omega ** (sum(a * b for a, b in zip(lam, h)) % p) for h in Hl}
    # check psi0 is a homomorphism of H
    for _ in range(300):
        a, b = Hl[rng.integers(len(Hl))], Hl[rng.integers(len(Hl))]
        assert abs(psi0[G.mul(a, b)] - psi0[a] * psi0[b]) < 1e-12
    # right regular action: (R(g)Y)[y] = Y[y * g]
    right = {}

    def perm(g):
        if g not in right:
            right[g] = np.array([G.idx[G.mul(y, g)] for y in G.elts])
        return right[g]

    W = rng.normal(size=(N, r)) + 1j * rng.normal(size=(N, r))
    Vm = np.zeros((N, r), complex)
    for h in Hl:
        Vm += np.conj(psi0[h]) * W[perm(h)]
    Y, _ = np.linalg.qr(Vm)

    def phi(g):
        return np.linalg.det(Y.conj().T @ Y[perm(g)])

    # stabilizer and gap
    stab, gap = [], 2.0
    for g in G.elts:
        M = Y.conj().T @ Y[perm(g)]
        sv = np.clip(np.linalg.svd(M, compute_uv=False), 0, 1)
        if np.all(sv > 1 - 1e-10):
            stab.append(g)
        else:
            gap = min(gap, np.mean(np.sqrt(1 - sv ** 2)))
    assert set(stab) == Hset, (name, "stab(V) != H")
    delta = gap
    gamma = delta ** 2 / 2
    # chi = psi0^r on H
    chi_err = max(abs(phi(h) - psi0[h] ** r) for h in Hl)
    A, basis, E = cover(L, gamma_dims)
    n = A.n
    Aelts = list(itertools.product(range(p), repeat=n))
    # hlift membership: E_s(C) in H for all s != 0
    def in_hlift(C):
        return all(E(s, C) in Hset for s in range(1, p))
    phi_cache = {}

    def phic(g):
        if g not in phi_cache:
            phi_cache[g] = phi(g)
        return phi_cache[g]

    def Phi(C, S):
        out = 1.0 + 0j
        for s in S:
            out *= phic(E(s, C))
        return out

    pool = Aelts if samples is None else [Aelts[i] for i in rng.choice(len(Aelts), samples, replace=False)]
    Ht = [C for C in Aelts if in_hlift(C)]
    lines = [f"{name}: |G| = {N}, |H| = {len(Hl)}, n = {n}, |H~| = {len(Ht)}, stab(V) = H, "
             f"delta = {delta:.4f}, max|phi - psi0^r| on H = {chi_err:.1e}"]
    for S in designs:
        on = max(abs(Phi(C, S) - 1) for C in Ht)
        off = max(abs(Phi(C, S)) for C in pool if not in_hlift(C))
        assert on < 1e-9 and off <= 1 - gamma + 1e-12 and off <= (1 - delta ** 2) ** (r / 2) + 1e-12
        line = f"  design {S}: max|Phi-1| on H~ = {on:.1e}; max|Phi| off H~ = {off:.4f} <= (1-d^2)^(r/2) = {(1 - delta**2)**(r/2):.4f} <= 1-d^2/2 = {1-gamma:.4f}"
        if do_sigma:
            PhiArr = np.array([Phi(C, S) for C in Aelts])
            Aidx = {a: i for i, a in enumerate(Aelts)}
            # entries depend on b^{-1} * a
            diffidx = np.empty((len(Aelts), len(Aelts)), dtype=np.int64)
            for ia, a in enumerate(Aelts):
                for ib, b in enumerate(Aelts):
                    diffidx[ia, ib] = Aidx[A.bch(A.neg(b), a)]
            inH = np.array([in_hlift(C) for C in Aelts], dtype=float)
            rhoH = inH[diffidx] / p ** n
            for ell in (1, 2, 3, 5):
                sig = PhiArr[diffidx] ** ell / p ** n
                ev = np.linalg.eigvalsh((sig + sig.conj().T) / 2)
                herm = abs(sig - sig.conj().T).max()
                td = 0.5 * abs(np.linalg.eigvalsh(sig - rhoH)).sum()
                bound = 0.5 * p ** (n / 2) * (1 - gamma) ** ell
                assert ev.min() > -1e-12 and abs(np.trace(sig) - 1) < 1e-12 and herm < 1e-12 and td <= bound + 1e-12
                line += f"\n    l={ell}: tr=1, min eig {ev.min():.1e}, TD = {td:.4f} <= bound {bound:.2f}"
        lines.append(line)
    on_f = max(abs(Phi(C, falsifier) - 1) for C in Ht)
    lines.append(f"  falsifier points {falsifier} (not a design): max|Phi-1| on H~ = {on_f:.3f}")
    mp_err = max(abs(Phi(C, falsifier) ** p - 1) for C in Ht)
    lines.append(f"  Remark multiple-p: same points, l = p: max|Phi^p - 1| on H~ = {mp_err:.1e}")
    print("\n".join(lines))
    return on_f


if __name__ == "__main__":
    # Heis basis X=0, Y=1, Z=2; gamma_1 = all, gamma_2 = {Z}
    for p, design in ((3, (1, 1, 1, 2, 2, 2)), (5, (1, 2, 3, 4))):
        L = heis(p)
        X, Yv, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
        cases = [("H = Z(G)", [Z], (0, 0, 1)),
                 ("H = <exp X> (nonnormal)", [X], (1, 0, 0)),
                 ("H = <exp X, exp Z>", [X, Z], (1, 0, 1))]
        for hn, gens, lam in cases:
            f = run_case(f"Heis(F_{p}), {hn}", L, [3, 1], gens, lam, [design], (1, 2), do_sigma=True)
            assert f > 1e-3 or hn != "H = Z(G)"
    # class-3 filiform over F_5: [e0,e1]=e2, [e0,e2]=e3; gamma = (4, 2, 1)
    L = filiform(5, 4)
    e = lambda i: tuple(int(j == i) for j in range(4))
    # H = span{e0, e2, e3}: nonabelian ([e0,e2] = e3), nonnormal ([e1,e0] = -e2 ok, [e1, e2] = 0... checked by stab)
    run_case("filiform4(F_5), H = <e0, e2, e3> (nonabelian)", L, [4, 2, 1], [e(0), e(2)], (1, 1, 0, 0),
             [(1, 2, 3, 4)], (1, 2, 3), do_sigma=False, samples=6000)
    run_case("filiform4(F_5), H = <e1> (nonnormal)", L, [4, 2, 1], [e(1)], (0, 1, 0, 0),
             [(1, 2, 3, 4)], (1, 2, 3), do_sigma=False, samples=6000)
    print("ALL OK")
