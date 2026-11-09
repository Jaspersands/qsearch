"""Independent implementations (written from the paper text only) of
  A. the triangular solver of prop:triangular-sde (main.tex 729-746),
  B. the block-steered procedure of rem:sde-block-steered on i.i.d. columns, J = 3,
  C. the reserved-basis procedure of rem:sde-worst-case(b), J = 3,
with exact verification of every returned solution.
Usage: python steer.py
"""
import random, sys, time, itertools
import sympy

class Field:
    def __init__(self, p, kappa):
        self.p, self.k = p, kappa
        self.g = sympy.primitive_root(p)
        self.cos = [None] * p
        x = 1
        for e in range(p - 1):
            self.cos[x] = e % kappa
            x = x * self.g % p
        self.inv = [0] + [pow(x, p - 2, p) for x in range(1, p)]
        self.P = [y for y in range(1, p) if self.cos[y] == 0]
    def inQo(self, y, c):
        y %= self.p
        return y == 0 or self.cos[y] == c % self.k

def solve(F, cols, target):
    """coefficients x with sum_j x_j cols[j] = target mod p (some solution), or None."""
    p = F.p
    a = len(target)
    n = len(cols)
    M = [[cols[j][i] % p for j in range(n)] + [target[i] % p] for i in range(a)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, a) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = F.inv[M[r][c]]
        M[r] = [v * iv % p for v in M[r]]
        for i in range(a):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(vi - f * vr) % p for vi, vr in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == a:
            break
    for i in range(r, a):
        if M[i][n]:
            return None
    x = [0] * n
    for i, c in enumerate(piv):
        x[c] = M[i][n]
    return x

def kernel_vec(F, cols, U):
    """nonzero delta with sum delta_j cols_j in span(U); assumes one exists.  Returns
    (delta, dim of relation space mod U)."""
    p = F.p
    # relations of cols modulo U: kernel of [cols | U] restricted to the cols part
    allc = cols + U
    a = len(cols[0])
    n = len(allc)
    M = [[allc[j][i] % p for j in range(n)] for i in range(a)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, a) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = F.inv[M[r][c]]
        M[r] = [v * iv % p for v in M[r]]
        for i in range(a):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(vi - f * vr) % p for vi, vr in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv]
    kers = []
    for fcol in free:
        v = [0] * n
        v[fcol] = 1
        for i, c in enumerate(piv):
            v[c] = (-M[i][fcol]) % p
        kers.append(v[:len(cols)])
    # relation space mod U = projection of kernel onto the cols part
    # rank of the projected kernel vectors:
    proj = [k for k in kers if any(k)]
    if not proj:
        return None, 0
    # rank
    rk = 0
    B = []
    for k in proj:
        if solve(F, B, k) is None if B else True:
            B.append(k)
    rk = len(B)
    return B[0], rk

def vsum(F, terms, a):
    p = F.p
    out = [0] * a
    for c, v in terms:
        for i in range(a):
            out[i] = (out[i] + c * v[i]) % p
    return out

def in_span(F, U, v):
    return solve(F, U, v) is not None if U else not any(x % F.p for x in v)

def add_to_basis(F, U, v):
    if not in_span(F, U, v):
        U.append(v)

def verify(F, bank, x):
    a = len(bank[0])
    ok_set = all(F.inQo(xi, 0) for xi in x)
    nz = any(xi % F.p for xi in x)
    val = vsum(F, list(zip(x, bank)), a)
    return ok_set and nz and not any(val)

# ------------------------------------------------------------------ A: triangular
def find_contraction(F):
    """alpha_0 = 1, beta_0 = 0, alpha_j + beta_i in Q^o_{-(i+j)}; DFS."""
    p, K = F.p, F.k
    candb = [[y for y in range(p) if F.inQo(1 + y, -i)] for i in range(1, K)]
    def dfs(i, betas):
        if i == K:
            alphas = [1]
            for j in range(1, K):
                ok = [y for y in range(p) if F.inQo(y, -j) and all(F.inQo(y + betas[ii], -ii - j) for ii in range(1, K))]
                if not ok:
                    return None
                alphas.append(ok[0])
            return alphas, [0] + betas[1:]
        for b in candb[i - 1]:
            bb = betas + [b]
            # prune: each column j must still have a candidate
            good = True
            for j in range(1, K):
                if not any(F.inQo(y, -j) and all(F.inQo(y + bb[ii], -ii - j) for ii in range(1, i + 1)) for y in range(p)):
                    good = False
                    break
            if good:
                r = dfs(i + 1, bb)
                if r:
                    return r
        return None
    return dfs(1, [0])

def triangular(F, bank, alpha, beta):
    p, a = F.p, len(bank[0])
    U, rounds, used = [], [], 0
    while True:
        k = len(U)
        take = a - k + 1
        if used + take > len(bank):
            return None, used
        idx = list(range(used, used + take))
        used += take
        cols = [bank[i] for i in idx]
        if k == a:
            delta = [1]
        else:
            delta, _ = kernel_vec(F, cols, U)
        # scale so that the first nonzero entry is 1
        f = next(d for d in delta if d % p)
        fi = F.inv[f % p]
        delta = [d * fi % p for d in delta]
        e = vsum(F, list(zip(delta, cols)), a)
        v = vsum(F, [(beta[F.cos[d]] * d % p, c) for d, c in zip(delta, cols) if d % p], a)
        if in_span(F, U, v) or k == a:
            R = {i: (d * (alpha[0] + beta[F.cos[d]]) % p if d % p else 0) for i, d in zip(idx, delta)}
            rho = vsum(F, [(R[i], bank[i]) for i in idx], a)
            break
        rounds.append((list(U), idx, delta, e, v))
        U.append(v)
    x = [0] * len(bank)
    for i in R:
        x[i] = R[i]
    tau = [(-t) % p for t in rho]
    for (Ub, idx, delta, e, v) in reversed(rounds):
        sol = solve(F, Ub + [v], tau)
        zeta = sol[-1]
        if zeta:
            n = F.cos[zeta]
            for i, d in zip(idx, delta):
                x[i] = zeta * d * (alpha[n] + beta[F.cos[d]]) % p if d % p else 0
            tau = [(t - zeta * (alpha[n] * ei + vi)) % p for t, ei, vi in zip(tau, e, v)]
    assert not any(tau)
    return x, used

# ------------------------------------------------------------------ blocks / back substitution
def make_blocks(F, S, delta, nblocks):
    groups = {}
    for i in S:
        groups.setdefault(F.cos[delta[i]], []).append(i)
    blocks = [g for g in groups.values()]
    while len(blocks) < nblocks:
        blocks.sort(key=len)
        big = blocks.pop()
        assert len(big) >= 2
        blocks += [big[:-1], [big[-1]]]
    return blocks

def back_substitute(F, bank, rounds, tau, rng):
    """rounds: list of (U_before, blocks, delta) in formation order.  tau in U_L.
    Returns weights dict or None on an empty Good set."""
    p, a = F.p, len(bank[0])
    x = {}
    for Ub, blocks, delta in reversed(rounds):
        W = [vsum(F, [(delta[i], bank[i]) for i in blk], a) for blk in blocks]
        e = vsum(F, [(1, w) for w in W], a)
        sol = solve(F, W[1:] + Ub, tau)
        assert sol is not None
        beta = [0] + sol[:len(W) - 1]
        cls = [F.cos[delta[blk[0]]] for blk in blocks]
        good = [s for s in range(p) if all(F.inQo(beta[b] + s, -cls[b]) for b in range(len(W)))]
        if not good:
            return None
        s = rng.choice(good)
        for b, blk in enumerate(blocks):
            for i in blk:
                x[i] = delta[i] * (beta[b] + s) % p
        val = vsum(F, [(beta[b], W[b]) for b in range(len(W))] + [(s, e)], a)
        tau = [(t - vv) % p for t, vv in zip(tau, val)]
    assert not any(tau), "residual not zero"
    return x

# ------------------------------------------------------------------ B: block-steered (iid)
def block_steered_forward(F, bank, J=3):
    p, a = F.p, len(bank[0])
    U, rounds, used = [], [], 0
    while True:
        k = len(U)
        take = a - k + 1
        if used + take > len(bank):
            return ('short', None, None, used)
        idx = list(range(used, used + take))
        used += take
        cols = [bank[i] for i in idx]
        if k == a:
            # one column, weight 1, value in U
            return ('ok', rounds, {idx[0]: 1}, used)
        dl, rk = kernel_vec(F, cols, U)
        if rk != 1 or any(d % p == 0 for d in dl):
            return ('notcircuit', None, None, used)
        delta = dict(zip(idx, dl))
        cl = {F.cos[d] for d in dl}
        if len(cl) == 1:
            nu = cl.pop()
            gi = pow(F.g, (p - 1 - nu) % (p - 1), p)  # g^{-nu}
            return ('ok', rounds, {i: delta[i] * gi % p for i in idx}, used)
        blocks = make_blocks(F, idx, delta, min(J, len(idx)))
        rounds.append((list(U), blocks, delta))
        for blk in blocks:
            add_to_basis(F, U, vsum(F, [(delta[i], bank[i]) for i in blk], a))

def run_block_steered(F, bank, rng, J=3, tries=1):
    status, rounds, fin, used = block_steered_forward(F, bank, J)
    if status != 'ok':
        return status, None
    a = len(bank[0])
    rho = vsum(F, [(w, bank[i]) for i, w in fin.items()], a)
    fails = 0
    for _ in range(tries):
        x = back_substitute(F, bank, rounds, [(-t) % F.p for t in rho], rng)
        if x is None:
            fails += 1
            continue
        sol = [0] * len(bank)
        for i, w in fin.items():
            sol[i] = w
        for i, w in x.items():
            sol[i] = w
        assert verify(F, bank, sol), "block-steered returned a wrong solution"
    return 'ok', fails

# ------------------------------------------------------------------ C: reserved basis
def reserved_forward(F, bank, J=3):
    p, a = F.p, len(bank[0])
    B, rest = [], []
    for i, v in enumerate(bank):
        if not in_span(F, [bank[j] for j in B], v):
            B.append(i)
        else:
            rest.append(i)
    r = len(B)
    U, rounds, pool, T, pi = [], [], list(rest), [], 0
    while len(U) < r:
        if not pool:
            return ('stall', rounds, B, U, pi)
        c = pool.pop(0)
        vc = bank[c]
        if in_span(F, U, vc):
            coeff = solve(F, [bank[s] for s in B], vc)
            cand = [k for k, s in enumerate(B) if coeff[k] and not in_span(F, U, bank[s])]
            if cand:
                k = cand[0]
                sigma = B[k]
                B[k] = c
                pool.append(sigma)
            else:
                pi += 1
            continue
        xs = solve(F, U + [bank[t] for t in T], vc)
        if xs is None:
            T.append(c)
            continue
        mu = xs[len(U):]
        delta = {c: 1}
        for t, m in zip(T, mu):
            if m:
                delta[t] = (-m) % p
        S = list(delta)
        blocks = make_blocks(F, S, delta, min(J, len(S)))
        rounds.append((list(U), blocks, delta))
        for blk in blocks:
            add_to_basis(F, U, vsum(F, [(delta[i], bank[i]) for i in blk], a))
        pool = [t for t in T if t not in delta] + pool
        T = []
    return ('ok', rounds, B, U, pi)

def run_reserved(F, bank, rng, J=3, tries=1):
    status, rounds, B, U, pi = reserved_forward(F, bank, J)
    if status != 'ok':
        return status, None, pi
    a = len(bank[0])
    fails = 0
    for _ in range(tries):
        t = {s: rng.choice(F.P) for s in B}
        tau = vsum(F, [((-t[s]) % F.p, bank[s]) for s in B], a)
        x = back_substitute(F, bank, rounds, tau, rng)
        if x is None:
            fails += 1
            continue
        sol = [0] * len(bank)
        for s in B:
            sol[s] = t[s]
        for i, w in x.items():
            sol[i] = w
        assert verify(F, bank, sol), "reserved-basis returned a wrong solution"
    return 'ok', fails, pi

def general_position(F, bank, r):
    for S in itertools.combinations(range(len(bank)), r):
        cols = [bank[i] for i in S]
        U = []
        for v in cols:
            add_to_basis(F, U, v)
        if len(U) < r:
            return False
    return True

if __name__ == "__main__":
    rng = random.Random(20261109)
    t0 = time.time()
    # ---------------- A
    print("A. triangular solver (prop:triangular-sde)")
    for kappa, p in [(2, 13), (2, 101), (3, 31), (3, 151), (4, 61), (4, 197)]:
        F = Field(p, kappa)
        con = find_contraction(F)
        assert con is not None, (p, kappa)
        alpha, beta = con
        # check contraction
        assert all(F.inQo(alpha[j] + beta[i], -(i + j)) for i in range(kappa) for j in range(kappa))
        bad = 0
        tot = 0
        for a in range(1, 6):
            M = (a + 1) * (a + 2) // 2
            for trial in range(60):
                mode = trial % 4
                if mode == 0:
                    bank = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                elif mode == 1:   # few distinct directions, repeated with scalings
                    base = [[rng.randrange(p) for _ in range(a)] for _ in range(2)]
                    bank = [[rng.randrange(1, p) * x % p for x in base[rng.randrange(2)]] for _ in range(M)]
                elif mode == 2:   # coordinate vectors with non-residue scalings
                    bank = [[(rng.randrange(1, p) if i == rng.randrange(a) else 0) for i in range(a)] for _ in range(M)]
                else:             # include zero columns and duplicates
                    bank = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                    bank[rng.randrange(M)] = [0] * a
                    bank[rng.randrange(M)] = list(bank[0])
                x, used = triangular(F, bank, alpha, beta)
                tot += 1
                if x is None or used > M or not verify(F, bank, x):
                    bad += 1
        print(f"  kappa={kappa} p={p}: {tot} banks (a<=5, 4 modes), failures {bad}  [{time.time()-t0:.1f}s]")
        sys.stdout.flush()
    # ---------------- B
    print("B. block-steered, J=3, iid uniform columns, M_3(a) columns")
    for kappa, p in [(2, 257), (2, 1031), (3, 2767), (3, 1009)]:
        F = Field(p, kappa)
        for a in (2, 3, 4, 6):
            M = (a + 2) ** 2 // 4 + (a % 2)
            colfail, bsfail, bstot = 0, 0, 0
            for trial in range(50):
                bank = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                st, fails = run_block_steered(F, bank, rng, tries=3)
                if st != 'ok':
                    colfail += 1
                else:
                    bsfail += fails
                    bstot += 3
            print(f"  kappa={kappa} p={p} a={a} M={M}: column-condition failures {colfail}/50; back-substitution failures {bsfail}/{bstot}  [{time.time()-t0:.1f}s]")
            sys.stdout.flush()
    # ---------------- C
    print("C. reserved basis, J=3, random banks, floor((a+2)^2/4)+a columns")
    for kappa, p in [(2, 257), (2, 1031), (3, 2767)]:
        F = Field(p, kappa)
        for a in (2, 3, 4):
            M = (a + 2) ** 2 // 4 + a
            tally = {True: [0, 0, 0, 0, 0], False: [0, 0, 0, 0, 0]}  # banks, stalls, pi, bsfail, bstot
            for trial in range(50):
                bank = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                gp = general_position(F, bank, a)
                st, fails, pi = run_reserved(F, bank, rng, tries=3)
                T_ = tally[gp]
                T_[0] += 1; T_[2] += pi
                if st != 'ok':
                    T_[1] += 1
                else:
                    T_[3] += fails; T_[4] += 3
            for gp in (True, False):
                b_, s_, pi_, f_, t_ = tally[gp]
                print(f"  kappa={kappa} p={p} a={a} M={M} {'GP' if gp else 'non-GP'}: banks {b_}, stalls {s_}, true-pool events {pi_}, back-substitution failures {f_}/{t_}  [{time.time()-t0:.1f}s]")
            sys.stdout.flush()
    # adversarial: proportional columns (not general position)
    print("C'. reserved basis on banks with many proportional columns (kappa=2, p=257)")
    F = Field(257, 2)
    for a in (3, 4, 5):
        M = (a + 2) ** 2 // 4 + a
        st_count = {}
        for trial in range(40):
            dirs = [[rng.randrange(257) for _ in range(a)] for _ in range(a)]
            bank = [[rng.randrange(1, 257) * x % 257 for x in dirs[rng.randrange(a)]] for _ in range(M)]
            st, fails, pi = run_reserved(F, bank, rng, tries=2)
            st_count[st] = st_count.get(st, 0) + 1
        print(f"  a={a} M={M}: outcomes {st_count}")
    print(f"total {time.time()-t0:.1f}s")
