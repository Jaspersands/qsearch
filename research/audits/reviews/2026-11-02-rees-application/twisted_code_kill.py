"""Known-method route for the twisted translation code rho_{U,P}.

rho_{U,P} = E_{lam in U^perp} |psi_{P+lam.x}><psi_{P+lam.x}|
          = D_P Pi_U D_P^dagger / p^(n-k).

Part 1 (float check): the vector-register shift x_i -> x_i - delta_i w on
copies of rho_{U,P_1}, ..., rho_{U,P_M}, followed by measuring the shifted
registers z, gives uniform z and leaves exactly rho_{U,P_z} with
P_z(w) = sum_m P_m(z_m + delta_m w), whenever some delta_m != 0.

Part 2 (exact computation over F_p): the Ivanyos-Santha style elimination
run in that n-dimensional register, tracked at the level of the public
matrices Y (state phase = Y eta, eta = unknown coefficients of P), reaches
a phase that is constant for EVERY eta.  By Part 1 the final state is then
Pi_U / p^(n-k), whose Fourier samples are uniform in U^perp.

Run: /opt/anaconda3/bin/python -I twisted_code_kill.py
"""

import itertools
import random
from math import gcd

import numpy as np


# ---------------------------------------------------------------- polynomials
def monomials(n, d):
    return [a for t in range(d + 1)
            for a in itertools.product(range(t + 1), repeat=n) if sum(a) == t]


def peval(coef, mons, x, p):
    s = 0
    for c, a in zip(coef, mons):
        if c:
            t = c
            for xj, aj in zip(x, a):
                t = t * pow(xj, aj, p) % p
            s += t
    return s % p


def subst_matrix(mons, z, delta, p):
    """T with (T c)[beta] = coefficients in w of sum_alpha c_alpha (z+delta w)^alpha."""
    index = {a: i for i, a in enumerate(mons)}
    T = np.zeros((len(mons), len(mons)), dtype=np.int64)
    from math import comb
    for i, a in enumerate(mons):
        # product over coordinates of sum_b C(a_j,b) z_j^(a_j-b) delta^b w_j^b
        terms = {(): 1}
        for j, aj in enumerate(a):
            new = {}
            for pre, val in terms.items():
                for b in range(aj + 1):
                    v = val * comb(aj, b) * pow(z[j], aj - b, p) * pow(delta, b, p) % p
                    new[pre + (b,)] = (new.get(pre + (b,), 0) + v) % p
            terms = new
        for beta, v in terms.items():
            T[index[beta], i] = (T[index[beta], i] + v) % p
    return T


# ------------------------------------------------------------- linear algebra
def nullspace_mod(A, p):
    A = np.array(A, dtype=np.int64) % p
    rows, cols = A.shape
    A = A.copy()
    piv = []
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i, c]), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        piv.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i, f]) % p
        basis.append(v)
    return basis


def rank_mod(A, p):
    A = np.array(A, dtype=np.int64) % p
    return A.shape[1] - len(nullspace_mod(A, p))


# ------------------------------------------------------------------- part 1
def rho_twisted(coef, mons, U_perp, n, p, pts):
    om = np.exp(2j * np.pi / p)
    N = len(pts)
    rho = np.zeros((N, N), complex)
    for lam in U_perp:
        v = np.array([om ** ((peval(coef, mons, x, p) + sum(l * xi for l, xi in zip(lam, x))) % p)
                      for x in pts]) / np.sqrt(N)
        rho += np.outer(v, v.conj())
    return rho / len(U_perp)


def check_lemma(n, p, polys, deltas, mons, u0, rng, trials):
    pts = list(itertools.product(range(p), repeat=n))
    idx = {x: i for i, x in enumerate(pts)}
    N = len(pts)
    om = np.exp(2j * np.pi / p)
    U_perp = [lam for lam in pts if sum(l * u for l, u in zip(lam, u0)) % p == 0]
    M = len(polys)
    # pure components of the input: one per (lam_1..lam_M)
    comps = []
    for lams in itertools.product(U_perp, repeat=M):
        vecs = []
        for coef, lam in zip(polys, lams):
            vecs.append(np.array([om ** ((peval(coef, mons, x, p) + sum(l * xi for l, xi in zip(lam, x))) % p)
                                  for x in pts]) / np.sqrt(N))
        comps.append(vecs)
    worst_prob, worst_dist = 0.0, 0.0
    for _ in range(trials):
        z = [tuple(rng.randrange(p) for _ in range(n)) for _ in range(M)]
        rho_w = np.zeros((N, N), complex)
        total = 0.0
        for vecs in comps:
            # apply |x_1..x_M, w> -> |x_1 - d_1 w, ..., w> to (vecs (x) |+>), project z
            amp = np.zeros(N, complex)
            for wi, w in enumerate(pts):
                a = 1.0 / np.sqrt(N)
                for m in range(M):
                    x = tuple((z[m][j] + deltas[m] * w[j]) % p for j in range(n))
                    a *= vecs[m][idx[x]]
                amp[wi] = a
            pr = float(np.vdot(amp, amp).real)
            total += pr / len(comps)
            rho_w += np.outer(amp, amp.conj()) / len(comps)
        rho_w /= total
        worst_prob = max(worst_prob, abs(total - 1.0 / N ** M))
        # predicted P_z
        Pz = np.zeros(len(mons), dtype=np.int64)
        for coef, zm, dm in zip(polys, z, deltas):
            Pz = (Pz + subst_matrix(mons, zm, dm, p) @ np.array(coef, dtype=np.int64)) % p
        pred = rho_twisted(list(Pz), mons, U_perp, n, p, pts)
        worst_dist = max(worst_dist, float(np.abs(rho_w - pred).max()))
    return worst_prob, worst_dist


# ------------------------------------------------------------------- part 2
class Stats:
    copies = 0


def nonzero_rows_of_degree(Y, mons, j):
    return Y[[i for i, a in enumerate(mons) if sum(a) == j], :]


def top_degree(Y, mons):
    for j in range(max(sum(a) for a in mons), 0, -1):
        if nonzero_rows_of_degree(Y, mons, j).any():
            return j
    return 0


def is_jth_power(c, j, p):
    return c == 0 or pow(c, (p - 1) // gcd(j, p - 1), p) == 1


def jth_root(c, j, p):
    for x in range(p):
        if pow(x, j, p) == c:
            return x
    return None


def state_at_most(j, n, p, d, mons, rng, Id):
    """A public pair (Y, noise_alive): a state rho_(U, Y eta) whose degree-i
    part is zero for every i > j and EVERY eta.  Fresh copies have Y = Id."""
    if j >= d:
        Stats.copies += 1
        return Id.copy(), True
    level = j + 1
    children = []
    while True:
        children.append(state_at_most(level, n, p, d, mons, rng, Id))
        Mj = np.array([nonzero_rows_of_degree(Yc, mons, level).reshape(-1)
                       for Yc, _ in children]).T % p
        null = nullspace_mod(Mj, p)
        if not null:
            continue
        found = None
        for _ in range(4000):
            v = np.zeros(len(children), dtype=np.int64)
            for b in null:
                v = (v + rng.randrange(p) * b) % p
            if v.any() and all(is_jth_power(int(c), level, p) for c in v):
                found = v
                break
        if found is not None:
            break
    deltas = [jth_root(int(c), level, p) for c in found]
    z = [tuple(rng.randrange(p) for _ in range(n)) for _ in children]
    Ynew = np.zeros_like(Id)
    noise = False
    for (Yc, alive), zm, dm in zip(children, z, deltas):
        Ynew = (Ynew + subst_matrix(mons, zm, dm, p) @ Yc) % p
        noise = noise or (dm != 0 and alive)
    assert not nonzero_rows_of_degree(Ynew, mons, level).any()
    return Ynew, noise


def pipeline(n, p, d, seed, samples):
    rng = random.Random(seed)
    mons = monomials(n, d)
    Id = np.eye(len(mons), dtype=np.int64)
    out = []
    for _ in range(samples):
        Stats.copies = 0
        Y, noise = state_at_most(0, n, p, d, mons, rng, Id)
        const = not any(nonzero_rows_of_degree(Y, mons, j).any() for j in range(1, d + 1))
        out.append((const, noise, Stats.copies))
    return out


def learn_U(n, p, k, rng, n_samples):
    pts = list(itertools.product(range(p), repeat=n))
    U_basis = [tuple(rng.randrange(p) for _ in range(n)) for _ in range(k)]
    U_perp = [lam for lam in pts if all(sum(l * u for l, u in zip(lam, ub)) % p == 0 for ub in U_basis)]
    samples = [rng.choice(U_perp) for _ in range(n_samples)]
    Uhat = nullspace_mod(np.array(samples), p)
    return rank_mod(np.array(U_basis), p), len(Uhat), rank_mod(np.array(U_basis + [tuple(v) for v in Uhat]), p)

# ------------------------------------------------------------------- part 4
def shift_measure(inputs, deltas, z, n, p, pts, idx):
    """inputs: list of (weights, vectors) spectral decompositions; returns the
    normalized post-state on w and Pr[z], applying the literal permutation."""
    N = len(pts)
    rho_w = np.zeros((N, N), complex)
    total = 0.0
    for combo in itertools.product(*[range(len(w)) for w, _ in inputs]):
        weight = np.prod([inputs[m][0][c] for m, c in enumerate(combo)])
        vecs = [inputs[m][1][c] for m, c in enumerate(combo)]
        amp = np.zeros(N, complex)
        for wi, w in enumerate(pts):
            a = 1.0 / np.sqrt(N)
            for m, dm in enumerate(deltas):
                a *= vecs[m][idx[tuple((z[m][j] + dm * w[j]) % p for j in range(n))]]
            amp[wi] = a
        pr = float(np.vdot(amp, amp).real)
        total += weight * pr
        rho_w += weight * np.outer(amp, amp.conj())
    return rho_w / total, total


def spectral(rho, tol=1e-9):
    ev, V = np.linalg.eigh(rho)
    keep = ev > tol
    return list(ev[keep]), [V[:, i] for i in np.where(keep)[0]]


def check_two_stages(n, p, rng):
    """Stage 1 twice (cubic -> quadratic, delta=(1,-1)), then stage 2 on the two
    simulated outputs with delta'=(1,2), all on state vectors; compare with the
    polynomial predicted by applying Lemma D twice."""
    d = 3
    mons = monomials(n, d)
    pts = list(itertools.product(range(p), repeat=n))
    idx = {x: i for i, x in enumerate(pts)}
    P = [rng.randrange(p) for _ in mons]
    u0 = (1, rng.randrange(p))
    U_perp = [lam for lam in pts if sum(l * u for l, u in zip(lam, u0)) % p == 0]
    rho0 = rho_twisted(P, mons, U_perp, n, p, pts)
    src0 = spectral(rho0)
    outs, preds = [], []
    for _ in range(2):
        z = [tuple(rng.randrange(p) for _ in range(n)) for _ in range(2)]
        r, _ = shift_measure([src0, src0], [1, p - 1], z, n, p, pts, idx)
        outs.append(r)
        Pz = (subst_matrix(mons, z[0], 1, p) @ np.array(P) + subst_matrix(mons, z[1], p - 1, p) @ np.array(P)) % p
        preds.append(Pz)
    dev1 = max(float(np.abs(o - rho_twisted(list(q), mons, U_perp, n, p, pts)).max()) for o, q in zip(outs, preds))
    z2 = [tuple(rng.randrange(p) for _ in range(n)) for _ in range(2)]
    r2, pr2 = shift_measure([spectral(outs[0]), spectral(outs[1])], [1, 2], z2, n, p, pts, idx)
    P2 = (subst_matrix(mons, z2[0], 1, p) @ preds[0] + subst_matrix(mons, z2[1], 2, p) @ preds[1]) % p
    dev2 = float(np.abs(r2 - rho_twisted(list(P2), mons, U_perp, n, p, pts)).max())
    top = max([sum(a) for a, c in zip(mons, P2) if c] or [0])
    return dev1, dev2, abs(pr2 - 1.0 / len(pts) ** 2), top


if __name__ == "__main__":
    rng = random.Random(11)
    print("== 1. vector-register shift lemma (float check)")
    for (n, p, d, label) in [(2, 5, 3, "cubic"), (2, 7, 3, "cubic")]:
        mons = monomials(n, d)
        P = [rng.randrange(p) for _ in mons]
        u0 = (1, rng.randrange(p))
        wp, wd = check_lemma(n, p, [P, P], [1, p - 1], mons, u0, rng, trials=6)
        print(f"n={n} p={p} two copies of rho_(U,P), P {label}, delta=(1,-1), U=F_p*{u0}: "
              f"max|Pr[z]-p^-2n|={wp:.2e}; max|rho_w - rho_(U,P_z)|={wd:.2e}")
    n, p = 2, 7
    mons = monomials(n, 2)
    Q1 = [rng.randrange(p) for _ in mons]
    Q2 = [rng.randrange(p) for _ in mons]
    u0 = (1, rng.randrange(p))
    wp, wd = check_lemma(n, p, [Q1, Q2], [1, 3], mons, u0, rng, trials=6)
    print(f"n=2 p=7 different quadratics Q1,Q2, delta=(1,3), U=F_p*{u0}: "
          f"max|Pr[z]-p^-2n|={wp:.2e}; max|rho_w - rho_(U,P_z)|={wd:.2e}")
    print("== 2. elimination in the n-dim register, phase constant for every eta (exact over F_p)")
    for (n, p, d) in [(2, 7, 3), (3, 7, 3), (2, 13, 4)]:
        res = pipeline(n, p, d, seed=3, samples=3)
        print(f"n={n} p={p} d={d}: constant for all eta={[r[0] for r in res]}, "
              f"noise survives={[r[1] for r in res]}, copies per Fourier sample={[r[2] for r in res]}")
    print("== 3. U from Fourier samples of Pi_U/p^(n-k) (exact over F_p)")
    for (n, p, k) in [(4, 7, 1), (5, 11, 2)]:
        rU, dimUhat, rboth = learn_U(n, p, k, random.Random(5), n_samples=3 * n)
        print(f"n={n} p={p} k={k}: rank U={rU}, dim of recovered space={dimUhat}, rank of U+recovered={rboth} (equal means recovered=U)")
    print("== 4. two consecutive Lemma D stages on state vectors (float check)")
    for p in (5, 7):
        dev1, dev2, dpr, top = check_two_stages(2, p, random.Random(p))
        print(f"n=2 p={p} d=3: stage-1 max deviation={dev1:.2e}; stage-2 max deviation={dev2:.2e}; "
              f"|Pr[z']-p^-2n|={dpr:.2e}; degree of predicted stage-2 phase={top}")
