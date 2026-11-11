import sys, numpy as np, itertools
sys.path.insert(0, '.')
from lie import *

# words expressing basis vectors from generators e0,e1 (2-generated algebras)
WORDS = {
  'heis3':  [None, None, (0, 1)],
  'fil4':   [None, None, (0, 1), (0, 2)],
  'free23': [None, None, (0, 1), (0, 2), (1, 2)],
  'fil5':   [None, None, (0, 1), (0, 2), (0, 3)],
}

def brv(A, B, C, p):
    return np.einsum('ni,nj,ijk->nk', A, B, C) % p

def auts(name, p, chunk=200000):
    m, b = ALGS[name]; C = tensor(m, b, p); W = WORDS[name]
    vecs = np.array(list(itertools.product(range(p), repeat=m)), dtype=np.int64)
    out = []
    # loop over X, vectorize over Y
    for X in vecs:
        Xb = np.broadcast_to(X, vecs.shape)
        img = [Xb, vecs]
        for w in W[2:]:
            img.append(brv(img[w[0]], img[w[1]], C, p))
        M = np.stack(img, axis=1)         # (N, m, m) rows = images of basis
        ok = np.ones(len(vecs), dtype=bool)
        for i in range(m):
            for j in range(i + 1, m):
                lhs = np.einsum('k,nkl->nl', C[i, j], M) % p
                rhs = brv(M[:, i], M[:, j], C, p)
                ok &= (lhs == rhs).all(1)
        # invertibility: det mod p
        idx = np.nonzero(ok)[0]
        for t in idx:
            if rank(M[t], p) == m: out.append(M[t].copy())
    return C, np.array(out)

if __name__ == '__main__':
    import pickle
    for name, p in [('heis3', 5), ('heis3', 7), ('fil4', 5), ('fil4', 7), ('free23', 5), ('fil5', 5)]:
        C, A = auts(name, p)
        print(name, p, len(A), flush=True)
        pickle.dump((C, A), open(f'aut_{name}_{p}.pkl', 'wb'))
