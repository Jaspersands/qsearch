"""Independent checks (sub, 2026-11-09) of Proposition app-sub-ray, Lemma
app-sub-character, Corollary app-sub-cancel, Lemma app-sub-lift and Remark
app-sub-multiple-p on Heis(F_p), p = 3, 5, with R the left-regular
representation (d = p^3), r = 2 (and r = 3 at p = 3).

Group arithmetic is exact (integers mod p); the representation is float.
"""
import itertools, math, sys
import numpy as np

rng = np.random.default_rng(91109)


def run(p, r, Hname, S_list, ells=(1, 2, 3)):
    inv2 = pow(2, -1, p)
    w = np.exp(2j * np.pi / p)
    # G = Heis(F_p): coordinates (a1, a2, a3) on x, y, z; [x, y] = z.
    def gmul(a, b):
        return ((a[0] + b[0]) % p, (a[1] + b[1]) % p,
                (a[2] + b[2] + inv2 * (a[0] * b[1] - a[1] * b[0])) % p)
    elems = list(itertools.product(range(p), repeat=3))
    idx = {g: i for i, g in enumerate(elems)}
    D = len(elems)
    def Rmat(g):
        M = np.zeros((D, D))
        for h in elems:
            M[idx[gmul(g, h)], idx[h]] = 1.0
        return M
    Rs = {g: Rmat(g) for g in elems}
    # hidden-subgroup generators (as Lie subalgebras hh)
    if Hname == 'Z':
        hh_basis = [(0, 0, 1)]
        gens = [(0, 0, 1)]
    elif Hname == '<x>':
        hh_basis = [(1, 0, 0)]
        gens = [(1, 0, 0)]
    elif Hname == '<x,z>':
        hh_basis = [(1, 0, 0), (0, 0, 1)]
        gens = [(1, 0, 0), (0, 0, 1)]
    # isotypic component: joint eigenspace of R(gens) with random nontrivial eigenvalues
    P = np.eye(D, dtype=complex)
    eig = []
    for gi, g in enumerate(gens):
        j = int(rng.integers(1, p)) if gi == 0 else int(rng.integers(0, p))
        eig.append(j)
        # projector onto eigenvalue w^j of R(g) (R(g)^p = I)
        Pg = sum((w ** (-j * k)) * np.linalg.matrix_power(Rs[g], k) for k in range(p)) / p
        P = P @ Pg
    # random r-dim subspace of range(P)
    X = P @ (rng.normal(size=(D, r)) + 1j * rng.normal(size=(D, r)))
    Y, _ = np.linalg.qr(X)
    PiV = Y @ Y.conj().T
    # stabilizer
    stab = [g for g in elems if np.linalg.norm((np.eye(D) - PiV) @ Rs[g] @ Y) < 1e-9]
    # expected H as a set: span of hh_basis (subspace of F_p^3 in log coords = group elements here)
    Hset = set()
    for coeffs in itertools.product(range(p), repeat=len(hh_basis)):
        v = [0, 0, 0]
        for c, b in zip(coeffs, hh_basis):
            for t in range(3):
                v[t] = (v[t] + c * b[t]) % p
        Hset.add(tuple(v))
    ok_stab = set(stab) == Hset
    # determinant character on H and its linearity: chi(exp v) = w^{lambda(v)}
    chi = {h: np.linalg.det(Y.conj().T @ Rs[h] @ Y) for h in Hset}
    lin_err = 0.0
    lam = {}
    for h in Hset:
        k = int(round((np.angle(chi[h]) / (2 * np.pi) * p))) % p
        lam[h] = k
        lin_err = max(lin_err, abs(chi[h] - w ** k), abs(abs(chi[h]) - 1))
    for h1 in Hset:
        for h2 in Hset:
            s = tuple((h1[t] + h2[t]) % p for t in range(3))
            lin_err = max(lin_err, abs((lam[h1] + lam[h2] - lam[s]) % p))
    # gap delta and Prop app-sub-ray(c)
    rho = PiV / r
    delta = 1.0
    ray_err = 0.0
    for g in elems:
        if g in Hset:
            continue
        Ug = Rs[g]
        diff = rho - Ug @ rho @ Ug.T
        td = 0.5 * np.abs(np.linalg.eigvalsh(diff)).sum()
        delta = min(delta, td)
        ov = abs(np.linalg.det(Y.conj().T @ Ug @ Y))
        mu = 1 - np.trace(PiV @ Ug @ PiV @ Ug.T).real / r
        sv = np.linalg.svd(Y.conj().T @ Ug @ Y, compute_uv=False)
        sv = np.clip(sv, 0, 1)
        ray_err = max(ray_err, ov - np.prod(sv), ov - (1 - mu) ** (r / 2), td ** 2 - mu,
                      abs(td - np.mean(np.sqrt(1 - sv ** 2))))
    gamma = delta ** 2 / 2
    # Rees cover A of Heis: coordinates (a1, a2, a3, a4) on tx, ty, tz, t^2 z; [tx, ty] = t^2 z
    def amul(a, b):
        return ((a[0] + b[0]) % p, (a[1] + b[1]) % p, (a[2] + b[2]) % p,
                (a[3] + b[3] + inv2 * (a[0] * b[1] - a[1] * b[0])) % p)
    def ainv(a):
        return tuple((-x) % p for x in a)
    def E(s, a):
        return ((s * a[0]) % p, (s * a[1]) % p, (s * a[2] + s * s * a[3]) % p)
    Aelems = list(itertools.product(range(p), repeat=4))
    # E_s homomorphism check (exact)
    hom_err = 0
    for a in Aelems[:200]:
        for b in Aelems[:50]:
            for s in range(1, p):
                if E(s, amul(a, b)) != gmul(E(s, a), E(s, b)):
                    hom_err += 1
    # hlift = t(hh) + t^2(hh cap gamma_2); gamma_2 = span(z)
    def in_hlift(a):
        v1 = (a[0], a[1], a[2])
        z_in_hh = (0, 0, 1) in Hset
        return v1 in Hset and (a[3] == 0 or z_in_hh)
    phi = {g: np.linalg.det(Y.conj().T @ Rs[g] @ Y) for g in elems}
    out = []
    for S in S_list:
        Phi = {}
        for a in Aelems:
            val = 1.0 + 0j
            for s in S:
                val *= phi[E(s % p, a)]
            Phi[a] = val
        in_err = max(abs(Phi[a] - 1) for a in Aelems if in_hlift(a))
        off_max = max(abs(Phi[a]) for a in Aelems if not in_hlift(a))
        moments = [sum(pow(s, j, p) for s in S) % p for j in (1, 2)]
        tds = []
        for ell in ells:
            N = len(Aelems)
            sig = np.zeros((N, N), dtype=complex)
            rhoH = np.zeros((N, N))
            for i, a in enumerate(Aelems):
                for j2, b in enumerate(Aelems):
                    g = amul(ainv(b), a)
                    sig[i, j2] = Phi[g] ** ell / N
                    rhoH[i, j2] = (1.0 if in_hlift(g) else 0.0) / N
            ev_sig = np.linalg.eigvalsh((sig + sig.conj().T) / 2)
            herm = np.abs(sig - sig.conj().T).max()
            td = 0.5 * np.abs(np.linalg.eigvalsh(sig - rhoH)).sum()
            bound = 0.5 * p ** (4 / 2) * (1 - gamma) ** ell
            tds.append((ell, td, bound, ev_sig.min(), herm, np.trace(sig).real))
        out.append((S, moments, in_err, off_max, tds))
    print(f'p={p} r={r} H={Hname}: stab(V)=H: {ok_stab} (|stab|={len(stab)}), '
          f'chi linear err={lin_err:.2e}, chi values (lambda) on gens: '
          f'{[lam[g] for g in gens]}, delta={delta:.4f}, ray(c) violations max={ray_err:.2e}, '
          f'E_s hom errors={hom_err}')
    for (S, moments, in_err, off_max, tds) in out:
        print(f'   S={S} moments(1,2)={moments}: max|Phi-1| on hlift={in_err:.3e}; '
              f'max|Phi| off hlift={off_max:.4f} (1-gamma={1-gamma:.4f})')
        for (ell, td, bound, mineig, herm, trc) in tds:
            print(f'      ell={ell}: TD(sigma,rho_H~)={td:.4e}  bound={bound:.4e}  '
                  f'min eig sigma={mineig:.2e} herm-err={herm:.1e} tr={trc:.6f}')
    sys.stdout.flush()


# p = 3, c = 2: Lemma (b) design (1,1,1,2,2,2); falsifier (1,2); multiple-p route (1,2) with ell = 3
run(3, 2, 'Z', [(1, 1, 1, 2, 2, 2), (1, 2)], ells=(1, 2, 3))
run(3, 2, '<x>', [(1, 1, 1, 2, 2, 2), (1, 2)], ells=(1, 3))
run(3, 2, '<x,z>', [(1, 1, 1, 2, 2, 2), (1, 2)], ells=(1, 3))
run(3, 3, 'Z', [(1, 1, 1, 2, 2, 2), (1, 2)], ells=(1, 3))
# p = 5: Lemma (a) design mu_4 = (1,2,3,4); falsifier (1,2)
run(5, 2, 'Z', [(1, 2, 3, 4), (1, 2)], ells=(1,))
run(5, 2, '<x>', [(1, 2, 3, 4), (1, 2)], ells=(1,))
