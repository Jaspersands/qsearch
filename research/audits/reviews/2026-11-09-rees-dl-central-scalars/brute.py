"""Independent check (no GAP): all A in GL_4(F_p) that extend to automorphisms of L_DL, and the
induced action N on Z = span(e7,e8). Usage: brute.py p.  Search: a=Ae1, b=Ae2 arbitrary;
c=Ae3 constrained by beta(b,c)=0 (linear); d=Ae4 solved linearly; then the cubic conditions and
the linear (B,T) system are checked exactly."""
import sys, itertools
import numpy as np
p = int(sys.argv[1])
br = [(1,2,5,1),(1,3,6,1),(1,4,7,1),(1,5,8,-1),(2,3,8,1),(2,4,6,1),(2,6,7,-1),(3,4,5,-1),(3,5,7,-1),(4,6,8,-1)]
T3 = np.zeros((8,8,8), dtype=np.int64)
for i,j,k,c in br:
    T3[i-1,j-1,k-1] = c % p; T3[j-1,i-1,k-1] = (-c) % p
def lie(x, y): return np.einsum('i,j,ijk->k', x, y, T3) % p
def emb(v, off):
    x = np.zeros(8, dtype=np.int64); x[off:off+len(v)] = v; return x
V = lambda v: emb(v, 0); W = lambda v: emb(v, 4)
beta = lambda x, y: lie(V(x), V(y))[4:6]
omega = lambda x, y: lie(V(x), V(y))[6:8]
vw = lambda x, w: lie(V(x), W(w))[6:8]
E4 = np.eye(4, dtype=np.int64); E2 = np.eye(2, dtype=np.int64)
def rank_mod(Mx):
    Mx = Mx.copy() % p; r = 0; rows, cols = Mx.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if Mx[i, c]), None)
        if piv is None: continue
        Mx[[r, piv]] = Mx[[piv, r]]; Mx[r] = Mx[r] * pow(int(Mx[r, c]), p-2, p) % p
        for i in range(rows):
            if i != r and Mx[i, c]: Mx[i] = (Mx[i] - Mx[i, c] * Mx[r]) % p
        r += 1
    return r
def solve_mod(Mx, rhs):  # returns a solution x of Mx x = rhs (mod p) or None
    rows, cols = Mx.shape
    Aug = np.concatenate([Mx % p, (rhs % p).reshape(-1, 1)], axis=1)
    if rank_mod(Aug) != rank_mod(Mx): return None
    # back-substitute via reduced form
    R = Aug.copy(); r = 0; pivs = []
    for c in range(cols):
        piv = next((i for i in range(r, rows) if R[i, c]), None)
        if piv is None: continue
        R[[r, piv]] = R[[piv, r]]; R[r] = R[r] * pow(int(R[r, c]), p-2, p) % p
        for i in range(rows):
            if i != r and R[i, c]: R[i] = (R[i] - R[i, c] * R[r]) % p
        pivs.append(c); r += 1
    x = np.zeros(cols, dtype=np.int64)
    for i, c in enumerate(pivs): x[c] = R[i, -1]
    return x
pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
def check(A):
    """A: 4x4, columns Ae_i. Return N (2x2) if A extends to an automorphism, else None."""
    if rank_mod(A) < 4: return None
    col = [A[:, i] for i in range(4)]
    Mw = np.stack([beta(col[0], col[1]), beta(col[0], col[2])], axis=1) % p   # M e5, M e6
    if rank_mod(Mw) < 2: return None
    Mmap = lambda w: Mw.dot(w) % p
    for i, j in pairs:
        if not np.array_equal(beta(col[i], col[j]), Mmap(beta(E4[i], E4[j]))): return None
    # N from cubic: [e1,e5] = -e8, [e2,e6] = -e7
    Ne8 = (-vw(col[0], Mw[:, 0])) % p; Ne7 = (-vw(col[1], Mw[:, 1])) % p
    N = np.stack([Ne7, Ne8], axis=1) % p
    if rank_mod(N) < 2: return None
    for i in range(4):
        for k in range(2):
            if not np.array_equal(vw(col[i], Mw[:, k]), N.dot(vw(E4[i], E2[k])) % p): return None
    # linear system in B (4 columns in W: 8 unknowns) and T (2x2: 4 unknowns)
    rows = []; rhs = []
    for i, j in pairs:
        target = (N.dot(omega(E4[i], E4[j])) - omega(col[i], col[j])) % p
        bij = beta(E4[i], E4[j])
        for comp in range(2):
            row = np.zeros(12, dtype=np.int64)
            for q in range(4):
                for r in range(2):
                    w = E2[r]
                    # B e_q = sum_r B[r,q] w_r ; contributes [Ae_i, Be_j] + [Be_i, Ae_j]
                    if q == j: row[q*2 + r] += vw(col[i], w)[comp]
                    if q == i: row[q*2 + r] -= vw(col[j], w)[comp]
            for r in range(2):
                for s in range(2):
                    row[8 + comp*2 + s] = (row[8 + comp*2 + s] - (1 if r == comp else 0) * 0)
            # T beta(e_i,e_j): T is 2x2 with (comp, s) entry; contributes -T[comp,s]*bij[s]
            for s in range(2): row[8 + comp*2 + s] = (-bij[s]) % p
            rows.append(row % p); rhs.append(target[comp])
    if solve_mod(np.array(rows), np.array(rhs)) is None: return None
    return N
vecs = [np.array(v, dtype=np.int64) for v in itertools.product(range(p), repeat=4) if any(v)]
found = {}
count = 0
for a in vecs:
    for b in vecs:
        # c with beta(b,c) = 0: linear in c
        Bc = np.stack([beta(b, E4[k]) for k in range(4)], axis=1) % p   # 2x4
        for c in vecs:
            if np.any(Bc.dot(c) % p): continue
            # d: beta(a,d)=M beta(e1,e4)=0, beta(b,d)=M beta(e2,e4)=M e6=beta(a,c), beta(c,d)=M beta(e3,e4)=-M e5=-beta(a,b)
            Mx = np.concatenate([np.stack([beta(x, E4[k]) for k in range(4)], axis=1) for x in (a, b, c)], axis=0) % p
            rhs = np.concatenate([np.zeros(2, dtype=np.int64), beta(a, c), (-beta(a, b)) % p]) % p
            if rank_mod(np.concatenate([Mx, rhs.reshape(-1,1)], axis=1)) != rank_mod(Mx): continue
            # enumerate all d in the affine solution space
            d0 = solve_mod(Mx, rhs)
            kern = [v for v in vecs if not np.any(Mx.dot(v) % p)]
            for d in [d0] + [(d0 + v) % p for v in kern]:
                A = np.stack([a, b, c, d], axis=1) % p
                N = check(A)
                count += 1
                if N is not None:
                    found[tuple(map(tuple, A.T))] = N
print(f"p={p} candidates checked={count} automorphism classes on V: {len(found)}")
Ns = {tuple(map(tuple, N)) for N in found.values()}
print("distinct N on Z:", len(Ns))
scal = sorted({N[0][0] for N in Ns if N[0][1] == 0 and N[1][0] == 0 and N[0][0] == N[1][1]})
print("scalars on Z:", scal)
dets = sorted({int(round(np.linalg.det(np.array(N)))) % p for N in Ns})
print("dets:", dets)
