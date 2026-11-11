"""Exact state checks for the adaptive scheme on free23 and fil4 (p = 5, 7), BCH group law.

(1) QUOTIENT SOURCE.  Measuring the gamma_c label lambda of |aH> leaves, on G/gamma_c, the state
    phi_lambda(a) = p^{-1/2} sum_t w^{lambda(C_a(t))} |Q_a(t)>, where a h^t = exp(Q_a(t) + C_a(t)).
    Report the fidelity with the true quotient coset state |a K/gamma_c>, averaged over the
    uniform label (this is the fidelity of the available source with the source a class-(c-1)
    HSP algorithm on G/gamma_c would consume).
(2) KNOWN-K TWIST.  For alpha in Stab(K), K = H gamma_c, h = exp(eta):
    psi_u(a) . alpha(h^t z) = w^{t u(zeta_alpha) + u(alpha z)} psi_u(a),  zeta_alpha = alpha(eta) - r eta,
    and zeta_alpha = known_alpha + eta_c (A_alpha - r)  with known_alpha computable from K alone.
    Multi-copy: the product is constant on K iff  sum u_i o A_i = 0 and sum u_i(zeta_i) = 0; the
    K-only sufficient system is  sum u_i o A_i = 0, sum r_i u_i = 0, sum u_i(known_i) = 0.
    The hidden subgroup of the resulting hiding set is K itself (support check)."""
import sys, os, json, itertools, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "2026-11-12-rees-direct-twist-class3-referee"))
from alg import bch, br
from stab_scalers import norm_line

def load(name, p):
    r = json.load(open(os.path.join(HERE, 'auts', f'{name}_{p}.json')))
    D = np.array(r['D'], dtype=np.int64); gens = [np.array(M, dtype=np.int64) for M in r['gens']]
    d = sum(1 for l in r['level'] if l == r['cls'])
    return D, gens, r['cls'], d, r['level']

def stab_elements(gens, eta, q, p, k, rng, maxtries=200000):
    out = []; line = norm_line(eta[:q], p); tries = 0
    while len(out) < k and tries < maxtries:
        tries += 1
        M = np.eye(len(eta), dtype=np.int64)
        for _ in range(rng.integers(5, 40)):
            M = M @ gens[rng.integers(len(gens))] % p
        if norm_line((eta @ M)[:q], p) == line: out.append(M)
    return out

def main(name, p, nH=4, seed=0):
    rng = np.random.default_rng(seed); D, gens, cls, d, level = load(name, p)
    m = D.shape[0]; q = m - d; w = lambda x: x % p
    mul = lambda X, Y: bch(np.asarray(X), np.asarray(Y), D, p, cls)
    key = lambda X: tuple(int(v) for v in np.asarray(X) % p)
    st = dict(alg=name, p=p, H=0, fid_mean=[], fid_pred_ok=0, fid_cases=0,
              single_cases=0, single_mismatch=0, known_mismatch=0,
              multi_tests=0, multi_pred_mismatch=0, Konly_solutions=0, Konly_invariant=0,
              support_hides_exactly_K=0)
    hard = [e for e in itertools.product(range(p), repeat=m) if any(e[i] for i in range(m) if level[i] == 1)]
    for eta in random.Random(seed).sample(hard, nH):
        eta = np.array(eta, dtype=np.int64); st['H'] += 1
        Ht = [key(t * eta) for t in range(p)]
        Z = [np.array([0] * q + list(c), dtype=np.int64) for c in itertools.product(range(p), repeat=d)]
        # (1) quotient source fidelity, several a
        for _ in range(3):
            a = rng.integers(0, p, m)
            C = [mul(a, t * eta % p)[q:] for t in range(p)]
            fs = []
            for lam in itertools.product(range(p), repeat=d):
                amp = sum(np.exp(2j * np.pi * (np.dot(lam, C[t]) % p) / p) for t in range(p)) / p
                f = abs(amp) ** 2; fs.append(f)
                # prediction: lambda o C(t) is a polynomial in t of degree <= 2 (class 3); fidelity 1, 0 or 1/p
                vals = [int(np.dot(lam, C[t]) % p) for t in range(p)]
                diffs2 = {(vals[(t + 2) % p] - 2 * vals[(t + 1) % p] + vals[t]) % p for t in range(p)}
                diffs1 = {(vals[(t + 1) % p] - vals[t]) % p for t in range(p)}
                pred = 1.0 if diffs1 == {0} else (0.0 if diffs2 == {0} else 1.0 / p)
                st['fid_cases'] += 1; st['fid_pred_ok'] += int(abs(f - pred) < 1e-9)
            st['fid_mean'].append(float(np.mean(fs)))
        # (2) single-copy twisted phases for alpha in Stab(K)
        alphas = stab_elements(gens, eta, q, p, 6, rng)
        a = rng.integers(0, p, m)
        aH = [mul(a, t * eta % p) for t in range(p)]
        supp = {}
        for z in Z:
            for x in aH: supp[key(mul(x, z))] = z[q:]
        Kel = [(t, z) for t in range(p) for z in Z]
        eta_bar = eta.copy(); eta_bar[q:] = 0; eta_c = eta[q:]
        rec = []
        for M in alphas:
            img = eta @ M % p
            r = next(int(img[i]) * pow(int(eta[i]), -1, p) % p for i in range(q) if eta[i])
            zeta = (img - r * eta) % p; assert not zeta[:q].any()
            Az = M[q:, q:]
            known = (eta_bar @ M % p)[q:]
            if ((known + eta_c @ (Az - r * np.eye(d, dtype=np.int64))) % p != zeta[q:]).any(): st['known_mismatch'] += 1
            rec.append((M, r, zeta[q:], Az, known))
            for u in itertools.product(range(p), repeat=d):
                u = np.array(u)
                psi = {x: (-np.dot(u, c)) % p for x, c in supp.items()}
                for (t, z) in random.Random(int(rng.integers(1 << 30))).sample(Kel, 6):
                    g = (t * eta + z) % p                        # exp(t eta + z) = h^t z  (z central)
                    ag = g @ M % p
                    moved = {key(mul(np.array(x), ag)): ph for x, ph in psi.items()}
                    st['single_cases'] += 1
                    if set(moved) != set(psi): st['single_mismatch'] += 1; continue
                    dset = {(moved[x] - psi[x]) % p for x in psi}
                    pred = (t * np.dot(u, zeta[q:]) + np.dot(u, z[q:] @ Az)) % p
                    if dset != {int(pred)}: st['single_mismatch'] += 1
        # (3) multi-copy: exact product phase on K vs predictions; brute force K-only solutions
        if len(rec) >= 2:
            n = 4
            for _ in range(300):
                us = [rng.integers(0, p, d) for _ in range(n)]
                ch = [rec[rng.integers(len(rec))] for _ in range(n)]
                inv = all((sum(t * np.dot(u, c[2]) + np.dot(u, z[q:] @ c[3]) for u, c in zip(us, ch)) % p) == 0
                          for (t, z) in Kel)
                # NOTE: A acts on rows: u(alpha z) = u . (z A) = (u A^T) . z
                pred = (not (sum(c[3] @ u for u, c in zip(us, ch)) % p).any()) and \
                       (sum(np.dot(u, c[2]) for u, c in zip(us, ch)) % p == 0)
                st['multi_tests'] += 1; st['multi_pred_mismatch'] += int(inv != pred)
            # K-only system: search labels u_i (as if measured) and twists from the pool
            from lie import nullspace
            for _ in range(200):
                ch = [rec[rng.integers(len(rec))] for _ in range(n)]
                # linear map (u_1..u_n) -> (sum A_i u_i, sum r_i u_i, sum known_i . u_i)
                rows = []
                for k in range(d):
                    rows.append(np.concatenate([c[3][k] for c in ch]))
                for k in range(d):
                    rows.append(np.concatenate([c[1] * np.eye(d, dtype=np.int64)[k] for c in ch]))
                rows.append(np.concatenate([c[4] for c in ch]))
                NS = nullspace(np.array(rows) % p, p)
                if len(NS) == 0: continue
                vec = (rng.integers(0, p, len(NS)) @ NS) % p
                if not vec.any(): continue
                us = [vec[i * d:(i + 1) * d] for i in range(n)]
                st['Konly_solutions'] += 1
                inv = all((sum(t * np.dot(u, c[2]) + np.dot(u, z[q:] @ c[3]) for u, c in zip(us, ch)) % p) == 0
                          for (t, z) in Kel)
                st['Konly_invariant'] += int(inv)
        # support: right translation by alpha(g) keeps supp(psi) iff g in K  (so the hiding set hides K)
        if rec:
            M = rec[0][0]; Kset = {key(mul(t * eta % p, z)) for t in range(p) for z in Z}
            ok = True
            for g in [rng.integers(0, p, m) for _ in range(40)]:
                ag = g @ M % p
                same = {key(mul(np.array(x), ag)) for x in supp} == set(supp)
                ok &= (same == (key(g) in Kset))
            st['support_hides_exactly_K'] += int(ok)
    st['fid_mean'] = [round(min(st['fid_mean']), 4), round(max(st['fid_mean']), 4)]
    print(json.dumps(st), flush=True)

if __name__ == '__main__':
    for name, p in [('fil4', 5), ('fil4', 7), ('free23', 5), ('free23', 7)]:
        main(name, p)
