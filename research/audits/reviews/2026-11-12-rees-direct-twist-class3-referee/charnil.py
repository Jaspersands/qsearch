import sys, itertools, random, numpy as np
sys.path.insert(0, '.')
from lie import *

def derivations(C, p):
    m = C.shape[0]
    # unknown D (m x m), D e_i = sum_r D[r,i] e_r ; condition for each i<j, k:
    # sum_r C[i,j,r] D[k,r] - sum_r D[r,i] C[r,j,k] - sum_r D[r,j] C[i,r,k] = 0
    rows = []
    for i in range(m):
        for j in range(i + 1, m):
            for k in range(m):
                row = np.zeros((m, m), dtype=np.int64)
                for r in range(m):
                    row[k, r] += C[i, j, r]
                    row[r, i] -= C[r, j, k]
                    row[r, j] -= C[i, r, k]
                rows.append(row.flatten() % p)
    N = nullspace(np.array(rows), p)
    return [n.reshape(m, m) for n in N]

def assoc_nilpotent(Ds, p, m):
    cur = [D % p for D in Ds]
    for _ in range(m):
        nxt = []
        for A in cur:
            for D in Ds:
                P = (A @ D) % p
                if P.any(): nxt.append(P)
        if not nxt: return True
        R, _ = rref([x.flatten() for x in nxt], p)
        cur = [np.array(r, dtype=np.int64).reshape(m, m) for r in R]
    return False

if __name__ == '__main__':
    p = 7; m = 7
    random.seed(1)
    found = None
    for trial in range(20000):
        b = {(0, i): {i + 1: 1} for i in range(1, m - 1)}
        for i in range(1, m):
            for j in range(i + 1, m):
                if i == 0: continue
                ks = [k for k in range(i + j + 1, m)]   # weight filtration i+j (0-based shift)
                d = {k: random.randrange(p) for k in ks if random.random() < 0.5}
                if d: b[(i, j)] = d
        C = tensor(m, b, p)
        if not jacobi_ok(C, p): continue
        Ds = derivations(C, p)
        if assoc_nilpotent(Ds, p, m):
            found = b; print('trial', trial, 'brackets', b, 'dimDer', len(Ds), 'lcs', [len(x) for x in lcs(C, p)]); break
    print(found)
