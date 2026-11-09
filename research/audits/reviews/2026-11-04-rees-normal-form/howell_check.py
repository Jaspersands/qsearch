# Brute-force check of the Howell-form normalizer step over Z/p^e (local Howell
# sequences of Lemma tb-chart, Step 2), left kernels, Smith forms, (M1), (M2), (M3).
import itertools, random, sys
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

def setup(p, e):
    global P, E, M
    P, E, M = p, e, p**e

def val(a):
    a %= M
    if a == 0: return E
    v = 0
    while a % P == 0: a //= P; v += 1
    return v

def unit_part_inv(a, v):
    u = (a % M) // P**v
    return pow(u, -1, M)

ops = [0]
def howell(gens, K):
    """Construction of Lemma tb-chart Step 2. Returns list of (pivot_pos, a, row)."""
    rem = [list(g) for g in gens if any(x % M for x in g)]
    q0 = max(len(rem), 1)
    out = []
    for j in range(K):
        assert len(rem) <= q0
        best = None
        for idx, r in enumerate(rem):
            v = val(r[j])
            if v < E and (best is None or v < best[0]): best = (v, idx)
        if best is None: continue
        a, idx = best
        piv = rem.pop(idx)
        inv = unit_part_inv(piv[j], a)
        piv = [(x * inv) % M for x in piv]
        assert piv[j] == P**a
        new = []
        for r in rem:
            f = (r[j] % M) // P**a
            assert (r[j] % M) % P**a == 0
            r = [(x - f * y) % M for x, y in zip(r, piv)]
            ops[0] += K
            if any(r): new.append(r)
        ap = [(P**(E - a) * x) % M for x in piv]
        if any(ap): new.append(ap)
        rem = new
        out.append((j, a, piv))
    return out

def member(v, H, K):
    v = [x % M for x in v]
    coeff = [0] * len(H)
    hp = {j: t for t, (j, a, r) in enumerate(H)}
    for j in range(K):
        if v[j] == 0: continue
        if j in hp:
            t = hp[j]; _, a, r = H[t]
            if v[j] % P**a: return False, None
            f = v[j] // P**a
            coeff[t] = (coeff[t] + f) % M
            v = [(x - f * y) % M for x, y in zip(v, r)]
        else:
            return False, None
    return (not any(v)), coeff

def left_kernel(A, K):
    a = len(A)
    rows = [list(A[i]) + [1 if t == i else 0 for t in range(a)] for i in range(a)]
    H = howell(rows, K + a)
    ker = [r[K:] for (j, aa, r) in H if j >= K]
    for r in H:
        if r[0] >= K: assert not any(x % M for x in r[2][:K])
    return ker

def smith(C, ncols):
    C = [list(r) for r in C]
    nr = len(C)
    Q = [[1 if i == j else 0 for j in range(ncols)] for i in range(ncols)]
    Qi = [[1 if i == j else 0 for j in range(ncols)] for i in range(ncols)]
    diag = []
    for t in range(min(nr, ncols)):
        best = None
        for i in range(t, nr):
            for j in range(t, ncols):
                v = val(C[i][j])
                if v < E and (best is None or v < best[0]): best = (v, i, j)
        if best is None: break
        a, i, j = best
        C[t], C[i] = C[i], C[t]
        if j != t:
            for r in C: r[t], r[j] = r[j], r[t]
            for r in Q: r[t], r[j] = r[j], r[t]
            Qi[t], Qi[j] = Qi[j], Qi[t]
        inv = unit_part_inv(C[t][t], a)
        C[t] = [(x * inv) % M for x in C[t]]
        for i2 in range(nr):
            if i2 != t and C[i2][t] % M:
                f = C[i2][t] // P**a
                C[i2] = [(x - f * y) % M for x, y in zip(C[i2], C[t])]
        for j2 in range(ncols):
            if j2 != t and C[t][j2] % M:
                f = C[t][j2] // P**a
                for r in C: r[j2] = (r[j2] - f * r[t]) % M
                for r in Q: r[j2] = (r[j2] - f * r[t]) % M
                Qi[t] = [(x + f * y) % M for x, y in zip(Qi[t], Qi[j2])]
        diag.append(a)
    diag += [E] * (ncols - len(diag))
    return diag, Q, Qi, C

def matvec_row(v, Q):
    n = len(Q[0])
    return [sum(v[i] * Q[i][j] for i in range(len(v))) % M for j in range(n)]

# ---- Lie rings
class Ring:
    def __init__(s, es, c):
        s.es, s.c, s.m = es, c, len(es)
    def psi(s, t): return [(P**(E - s.es[i]) * t[i]) % M for i in range(s.m)]
    def psiinv(s, v):
        out = []
        for i in range(s.m):
            d = P**(E - s.es[i]); assert v[i] % d == 0
            out.append((v[i] // d) % P**s.es[i])
        return out
    def br(s, x, y):
        z = [0] * s.m
        for (i, j), vec in s.c.items():
            if x[i] and y[j]:
                for k, ck in vec.items(): z[k] += x[i] * y[j] * ck
        return [z[k] % P**s.es[k] for k in range(s.m)]
    def brV(s, u, v): return s.psi(s.br(s.psiinv(u), s.psiinv(v)))
    def elems(s):
        for t in itertools.product(*[range(P**x) for x in s.es]): yield list(t)

def heis_mixed():
    # x,y order 9, z order 3, w order 9 central-ish, [x,y]=z, [x,w]=3? keep Lie: [x,w]=3 z? z order 3 so 3z=0; use [y,w]=... simple
    es = [2, 2, 1, 2]
    c = {}
    def put(i, j, k, v):
        c.setdefault((i, j), {})[k] = v; c.setdefault((j, i), {})[k] = -v
    put(0, 1, 2, 1)
    put(0, 3, 3, 3)  # [x,w] = 3w (order 3 element)
    return Ring(es, c)

def check_jacobi(R):
    basis = [[1 if i == j else 0 for j in range(R.m)] for i in range(R.m)]
    for a, b, d in itertools.product(basis, repeat=3):
        t1 = R.br(a, R.br(b, d)); t2 = R.br(b, R.br(d, a)); t3 = R.br(d, R.br(a, b))
        assert all((t1[k] + t2[k] + t3[k]) % P**R.es[k] == 0 for k in range(R.m)), "Jacobi"
    for i in range(R.m):
        for j in range(R.m):
            x = [P**R.es[i] if t == i else 0 for t in range(R.m)]
            y = basis[j]
            assert not any(R.br(x, y)), "well-defined"

def subring(R, gens):
    H = howell([R.psi(g) for g in gens], R.m)
    while True:
        rows = [r for (_, _, r) in H]
        new = rows + [R.brV(a, b) for a in rows for b in rows]
        H2 = howell(new, R.m)
        if len(H2) == len(H) and all(member(r, H, R.m)[0] for (_, _, r) in H2): return H
        H = H2

def size(H): return 1 if not H else eval('*'.join(str(P**(E - a)) for (_, a, _) in H))

def present(R, S, K):
    """(M1) on the Howell sequences S, K of psi-images."""
    s = [r for (_, _, r) in S]; k = [r for (_, _, r) in K]
    ker = left_kernel(s + k, R.m)
    Rm = [l[:len(s)] for l in ker]
    d, Q, Qi, D = smith(Rm, len(s)) if Rm else ([E] * len(s), None, None, None)
    if Q is None:
        Q = [[1 if i == j else 0 for j in range(len(s))] for i in range(len(s))]; Qi = Q
    I = [i for i in range(len(s)) if d[i] >= 1]
    u = {i: [sum(Qi[i][j] * s[j][t] for j in range(len(s))) % M for t in range(R.m)] for i in I}
    def coord(y):
        ok, lam = member(y, S, R.m); assert ok
        lq = matvec_row(lam, Q)
        return {i: lq[i] % P**d[i] for i in I}
    return I, d, u, coord

def theta_of(Kp, m):
    rows = [r for (_, _, r) in Kp]
    if not rows: return lambda v: list(v)
    d, Q, Qi, D = smith(rows, m)
    return lambda v: [(P**(E - d[l]) * x) % M for l, x in enumerate(matvec_row(v, Q))]

def idealizer(R, S, Kp):
    s = [r for (_, _, r) in S]; kp = [r for (_, _, r) in Kp]
    th = theta_of(Kp, R.m)
    A = [sum((th(R.brV(si, kl)) for kl in kp), []) for si in s]
    if not kp: return S
    ker = left_kernel(A, len(kp) * R.m)
    gens = [[sum(l[i] * s[i][t] for i in range(len(s))) % M for t in range(R.m)] for l in ker]
    return howell(gens, R.m)

def run(R, trials):
    elems = list(R.elems())
    for tr in range(trials):
        S = subring(R, [random.choice(elems) for _ in range(random.randint(1, 3))])
        Sset = [x for x in elems if member(R.psi(x), S, R.m)[0]]
        assert len(Sset) == size(S)
        # K' arbitrary subring of S (not nec. ideal) for idealizer test
        Kp = subring(R, [random.choice(Sset) for _ in range(random.randint(0, 2))])
        I2 = idealizer(R, S, Kp)
        brute = [y for y in Sset if all(member(R.brV(R.psi(y), r), Kp, R.m)[0] for (_, _, r) in Kp)]
        got = [y for y in elems if member(R.psi(y), I2, R.m)[0]]
        assert sorted(map(tuple, brute)) == sorted(map(tuple, got)), "idealizer"
        # presentation of S'/K' with K' ideal of S' = I_S(K')
        Sp = I2
        I, d, u, coord = present(R, Sp, Kp)
        order = 1
        for i in I: order *= P**d[i]
        assert order * size(Kp) == size(Sp), "order"
        for i in I:
            assert member(u[i], Sp, R.m)[0]
            # p^{d_i} u_i in K', p^{d_i - 1} u_i not in K'
            assert member([(P**d[i] * x) % M for x in u[i]], Kp, R.m)[0]
            assert not member([(P**(d[i] - 1) * x) % M for x in u[i]], Kp, R.m)[0]
        # coordinate map inverts section on random elements
        for _ in range(20):
            y = R.psi(random.choice([x for x in elems if member(R.psi(x), Sp, R.m)[0]]))
            t = coord(y)
            sig = [sum(t[i] * u[i][c] for i in I) % M for c in range(R.m)]
            diff = [(a - b) % M for a, b in zip(y, sig)]
            assert member(diff, Kp, R.m)[0], "coord"
        # socle tensor divisibility (M3)
        for i in I:
            for j in I:
                b = R.brV([(P**(d[i]-1) * x) % M for x in u[i]], [(P**(d[j]-1) * x) % M for x in u[j]])
                tc = coord(b)
                for k in I: assert tc[k] % P**(d[k] - 1) == 0, "socle"
    return True

def kernel_test(trials):
    for _ in range(trials):
        a, K = random.randint(1, 4), random.randint(1, 3)
        A = [[random.randrange(M) if random.random() < .7 else P * random.randrange(M) for _ in range(K)] for _ in range(a)]
        ker = left_kernel(A, K)
        H = howell(ker, a) if ker else []
        for lam in itertools.product(range(M), repeat=a):
            z = all(sum(lam[i] * A[i][j] for i in range(a)) % M == 0 for j in range(K))
            assert z == (member(list(lam), H, a)[0] if H else not any(lam)), "kernel"

for (p, e) in [(3, 2), (2, 3), (3, 3), (5, 2)]:
    setup(p, e); kernel_test(40 if M < 30 else 10)
setup(3, 2); R = heis_mixed(); check_jacobi(R); run(R, 60)
# n_3(Z/9) plus abelian Z/3 summand, all mixed
es = [2, 2, 2, 1]; c = {}
def put(i, j, k, v):
    c.setdefault((i, j), {})[k] = v; c.setdefault((j, i), {})[k] = -v
put(0, 1, 2, 1); put(0, 3, 2, 3)
R2 = Ring(es, c); check_jacobi(R2); run(R2, 60)
print("all checks passed; row ops", ops[0])
