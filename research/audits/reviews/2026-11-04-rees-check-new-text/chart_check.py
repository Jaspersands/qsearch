"""Executable reading of Lemma tb-chart (Steps 2-6) over Z/p^e, checked by brute force.

* Howell construction and membership test (Step 2) against brute-force spans.
* Column scan (Step 3), Smith form (Step 4), coordinates (Step 4(c)) and
  structure constants (Step 5) on quotients F/I of free class-2 Lie rings
  F_{s,2} over Z/p^e, s = 2, 3, by random ideals I; checks that
  u -> coords(Yu) is a surjective Lie ring map with kernel exactly I and
  sum e_i = log_p |F/I|.
* The C_9 x C_3 remark of Step 3 (mod-p column test is not enough).
AI-checked, pending human review.
"""
import itertools, random

random.seed(20261104)

def val(a, p, e):
    a %= p ** e
    if a == 0:
        return e
    v = 0
    while a % p == 0:
        a //= p; v += 1
    return v

def unit_inv(a, M):
    return pow(a, -1, M)

def howell(gens, p, e, k):
    M = p ** e
    rem = [list(g) for g in gens if any(x % M for x in g)]
    piv = []  # (pos, a, row)
    for j in range(k):
        best = None
        for idx, r in enumerate(rem):
            v = val(r[j], p, e)
            if v < e and (best is None or v < best[0]):
                best = (v, idx)
        if best is None:
            continue
        a, idx = best
        r = rem.pop(idx)
        u = (r[j] % M) // p ** a
        ui = unit_inv(u, M)
        r = [(x * ui) % M for x in r]
        assert r[j] == p ** a
        new = []
        for s in rem:
            assert s[j] % p ** a == 0
            c = (s[j] // p ** a) % M
            s2 = [(x - c * y) % M for x, y in zip(s, r)]
            assert s2[j] == 0
            new.append(s2)
        new.append([(p ** (e - a) * y) % M for y in r])
        rem = [s for s in new if any(s)]
        piv.append((j, a, r))
    return piv

def member(v, H, p, e, k):
    M = p ** e
    v = [x % M for x in v]
    pos = {j: (a, r) for (j, a, r) in H}
    for j in range(k):
        if v[j] == 0:
            continue
        if j in pos and v[j] % p ** pos[j][0] == 0:
            a, r = pos[j]
            c = v[j] // p ** a
            v = [(x - c * y) % M for x, y in zip(v, r)]
        else:
            return False
    return not any(v)

def span(gens, p, e, k):
    M = p ** e
    S = {tuple([0] * k)}
    frontier = list(S)
    while frontier:
        nf = []
        for s in frontier:
            for g in gens:
                t = tuple((x + y) % M for x, y in zip(s, g))
                if t not in S:
                    S.add(t); nf.append(t)
        frontier = nf
    return S

# --- Step 2 against brute force
nt = 0
for (p, e, k) in [(3, 2, 2), (3, 2, 3), (3, 3, 2), (5, 2, 2), (2, 3, 3)]:
    M = p ** e
    allv = list(itertools.product(range(M), repeat=k))
    for trial in range(60):
        q0 = random.randint(1, k + 1)
        gens = [[random.randrange(M) * (p ** random.randint(0, e - 1)) % M for _ in range(k)] for _ in range(q0)]
        H = howell(gens, p, e, k)
        assert len(H) <= k
        for t, (j, a, r) in enumerate(H):  # (H2)
            assert member([(p ** (e - a) * x) % M for x in r], H[t + 1:], p, e, k)
        S = span(gens, p, e, k)
        for v in allv:
            assert member(list(v), H, p, e, k) == (v in S)
        nt += 1
print("Step 2: Howell construction and membership agree with brute force on %d random modules" % nt)

# --- free class-2 Lie ring F_{s,2} over Z/p^e: basis x_1..x_s, [x_i,x_j] (i<j)
def free2(s):
    basis = [(i,) for i in range(s)] + [(i, j) for i in range(s) for j in range(i + 1, s)]
    idx = {b: n for n, b in enumerate(basis)}
    d = len(basis)
    def br(u, v, M):
        w = [0] * d
        for i in range(s):
            for j in range(s):
                if i == j:
                    continue
                c = u[i] * v[j] % M
                if c == 0:
                    continue
                if i < j:
                    w[idx[(i, j)]] = (w[idx[(i, j)]] + c) % M
                else:
                    w[idx[(j, i)]] = (w[idx[(j, i)]] - c) % M
        return w
    return d, br

def chart(Y, d, k, p, e, br):
    """Steps 3-5. Y: k x d matrix (rows). Returns (J, eps list, e_i, lifts, coord fn, consts)."""
    M = p ** e
    col = lambda j: [Y[i][j] % M for i in range(k)]
    J, H = [], []
    for j in range(d):
        if not member(col(j), H, p, e, k):
            J.append(j)
            H = howell([col(jj) for jj in J], p, e, k)
    r = len(J)
    C = [[col(j)[i] for j in J] for i in range(k)]  # k x r
    P = [[int(i == j) for j in range(k)] for i in range(k)]
    Q = [[int(i == j) for j in range(r)] for i in range(r)]
    a_list = []
    for t in range(min(k, r)):
        best = None
        for i in range(t, k):
            for j in range(t, r):
                v = val(C[i][j], p, e)
                if v < e and (best is None or v < best[0]):
                    best = (v, i, j)
        if best is None:
            break
        a, i0, j0 = best
        C[t], C[i0] = C[i0], C[t]; P[t], P[i0] = P[i0], P[t]
        for row in C: row[t], row[j0] = row[j0], row[t]
        for row in Q: row[t], row[j0] = row[j0], row[t]
        u = (C[t][t] // p ** a) % M
        ui = unit_inv(u, M)
        C[t] = [x * ui % M for x in C[t]]; P[t] = [x * ui % M for x in P[t]]
        for i in range(k):
            if i != t and C[i][t]:
                c = C[i][t] // p ** a
                C[i] = [(x - c * y) % M for x, y in zip(C[i], C[t])]
                P[i] = [(x - c * y) % M for x, y in zip(P[i], P[t])]
        for j in range(r):
            if j != t and C[t][j]:
                c = C[t][j] // p ** a
                for row in C: row[j] = (row[j] - c * row[t]) % M
                for row in Q: row[j] = (row[j] - c * row[t]) % M
        a_list.append(a)
    # check PCQ diagonal
    I = [i for i, a in enumerate(a_list) if a < e]
    ei = [e - a_list[i] for i in I]
    Ccols = [[Y[i][j] % M for j in J] for i in range(k)]
    eps = []
    lifts = []
    for i in I:
        CQe = [sum(Ccols[row][aa] * Q[aa][i] for aa in range(r)) % M for row in range(k)]
        eps.append(CQe)
        lift = [0] * d
        for aa in range(r):
            lift[J[aa]] = Q[aa][i] % M
        lifts.append(lift)
    def coords(v):
        Pv = [sum(P[i][j] * v[j] for j in range(k)) % M for i in range(k)]
        out = []
        for n, i in enumerate(I):
            assert Pv[i] % p ** a_list[i] == 0
            out.append((Pv[i] // p ** a_list[i]) % p ** ei[n])
        for i in range(len(a_list), k):
            assert Pv[i] == 0
        return out
    Yv = lambda u: [sum(Y[i][j] * u[j] for j in range(d)) % M for i in range(k)]
    consts = {}
    for x in range(len(I)):
        for y in range(len(I)):
            consts[(x, y)] = coords(Yv(br(lifts[x], lifts[y], M)))
    return J, eps, ei, lifts, coords, consts, Yv, r

def ideal_closure(gens, d, br, p, e, s):
    M = p ** e
    G = [list(g) for g in gens]
    basis_x = [[int(t == i) for t in range(d)] for i in range(s)]
    for g in list(G):
        for x in basis_x:
            G.append(br(x, g, M))
    for g in list(G):  # class 2: one more round is zero but harmless
        for x in basis_x:
            G.append(br(x, g, M))
    return G

def perp_generators(I_set, d, p, e):
    M = p ** e
    Is = list(I_set)
    return [v for v in itertools.product(range(M), repeat=d)
            if all(sum(a * b for a, b in zip(v, u)) % M == 0 for u in Is)]

ncase = 0
for (s, p, e) in [(2, 3, 2), (2, 3, 3), (2, 5, 2), (3, 3, 2)]:
    M = p ** e
    d, br = free2(s)
    for trial in range(8 if d <= 3 else 3):
        ngen = random.randint(0, 2)
        gens = [[random.randrange(M) * p ** random.randint(0, e) % M for _ in range(d)] for _ in range(ngen)]
        Iset = span(ideal_closure(gens, d, br, p, e, s) + [[0] * d], p, e, d)
        perp = perp_generators(Iset, d, p, e)
        n_exp = 0
        size = M ** d // len(Iset)
        while p ** n_exp < size: n_exp += 1
        assert p ** n_exp == size
        k = n_exp + 2
        # rows of Y: random elements of the perp until they generate it
        while True:
            Y = [list(random.choice(perp)) for _ in range(k)]
            if len(span(Y, p, e, d)) == len(perp):
                break
        J, eps, ei, lifts, coords, consts, Yv, r = chart(Y, d, k, p, e, br)
        assert sum(ei) == n_exp, (sum(ei), n_exp)
        assert r <= n_exp <= k
        # kernel of u -> Yu is exactly I; coords surjective; Lie map
        img = set()
        for u in itertools.product(range(M), repeat=d):
            u = list(u)
            assert (not any(Yv(u))) == (tuple(u) in Iset)
            img.add(tuple(coords(Yv(u))))
        assert len(img) == size
        def lbr(x, y):  # bracket in L_G from constants
            out = [0] * len(ei)
            for a in range(len(ei)):
                for b in range(len(ei)):
                    c = x[a] * y[b]
                    if c:
                        for m_ in range(len(ei)):
                            out[m_] += c * consts[(a, b)][m_]
            return [o % p ** ei[m_] for m_, o in enumerate(out)]
        for _ in range(200):
            u = [random.randrange(M) for _ in range(d)]
            v = [random.randrange(M) for _ in range(d)]
            assert lbr(coords(Yv(u)), coords(Yv(v))) == coords(Yv(br(u, v, M)))
        ncase += 1
print("Steps 3-5: chart verified on %d random quotients of F_{2,2}, F_{3,2} over Z/9, Z/27, Z/25" % ncase)

# --- the C_9 x C_3 remark: F_{2,2} over Z/9, pi: x1->(1,0), x2->(0,1), [x1,x2]->0
p, e, M = 3, 2, 9
I = span([[0, 3, 0], [0, 0, 1]], p, e, 3)
perp = perp_generators(I, 3, p, e)
assert all(v[1] % 3 == 0 and v[2] == 0 for v in perp)
Y = [list(random.choice(perp)) for _ in range(6)]
while len(span(Y, p, e, 3)) != len(perp):
    Y = [list(random.choice(perp)) for _ in range(6)]
c1 = [row[0] for row in Y]; c2 = [row[1] for row in Y]
assert all(x % 3 == 0 for x in c2)                        # column 2 is 0 mod 3
assert not member(c2, howell([c1], p, e, 6), p, e, 6)      # but not in Z/9-span of column 1
print("Step 3 remark (C_9 x C_3): column 2 vanishes mod 3 but is not in the Z/9-span of column 1: confirmed")
