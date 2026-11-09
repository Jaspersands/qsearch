"""Generic k-dependency pieces at p=3: class-union realizable subgroups.

Patterns: all 3^k-1 nonzero vectors of F_3^k (one class each).  K = row space of
the k x (3^k-1) pattern matrix.  Class-union realizable set = image of {0,1}^t in
F_3^t / K.  We compute g(K) = max dim of a subgroup inside that image (k=2 directly),
and the defect-set formulation E_d (max dim of a linear subspace inside E_d u {0}).
"""
import itertools, sys
import numpy as np

def nonzero_vectors(k):
    return [v for v in itertools.product(range(3), repeat=k) if any(v)]

def rref_mod3(M):
    M = M.copy() % 3; r = 0; piv = []
    rows, cols = M.shape
    for c in range(cols):
        p = None
        for i in range(r, rows):
            if M[i, c] % 3: p = i; break
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        M[r] = (M[r] * M[r, c]) % 3  # inverse of 1 is 1, of 2 is 2
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c] * M[r]) % 3
        piv.append(c); r += 1
        if r == rows: break
    return M[:r], piv

def coset_rep(K_rref, piv, v):
    v = v.copy() % 3
    for row, c in zip(K_rref, piv):
        if v[c]: v = (v - v[c] * row) % 3
    return tuple(v)

def direct_k2():
    pats = nonzero_vectors(2); t = len(pats)
    K = np.array(pats).T % 3  # 2 x 8
    Kr, piv = rref_mod3(K)
    reps = {}
    for z in itertools.product((0, 1), repeat=t):
        reps.setdefault(coset_rep(Kr, piv, np.array(z)), []).append(z)
    img = set(reps)
    print(f"k=2: t={t}, class-union points 2^{t}={2**t}, distinct cosets hit {len(img)} of 3^{t-2}={3**(t-2)}")
    zero = coset_rep(Kr, piv, np.zeros(t, int))
    nz = [v for v in img if v != zero]
    def add(a, b, ca, cb): return tuple((ca*x + cb*y) % 3 for x, y in zip(a, b))
    best = 1; found = []
    for i, a in enumerate(nz):
        for b in nz[i+1:]:
            ok = True
            for ca in range(3):
                for cb in range(3):
                    if (ca, cb) == (0, 0): continue
                    if add(a, b, ca, cb) not in img: ok = False; break
                if not ok: break
            if ok:
                best = 2; found.append((a, b))
    print(f"k=2: 2-dim subgroup inside class-union image: {'YES' if found else 'NO'} ({len(found)} pairs)")
    return found

def defect_set(d):
    """E_d = set of defect vectors of local assignments y: F_3^d -> {0,1}, y(0)=0."""
    alphas = [a for a in itertools.product(range(3), repeat=d) if any(a)]
    units = [tuple(1 if j == i else 0 for j in range(d)) for i in range(d)]
    others = [a for a in alphas if a not in units]
    E = {}
    for bits in itertools.product((0, 1), repeat=len(alphas)):
        y = dict(zip(alphas, bits))
        e = tuple((y[a] - sum(a[j] * y[units[j]] for j in range(d))) % 3 for a in others)
        E.setdefault(e, []).append(bits)
    return others, E

def max_subspace_in(E, dim_ambient, want):
    """Largest linear subspace of F_3^n with all nonzero elements in E (greedy exhaustive up to 'want')."""
    Es = set(E); zero = tuple([0]*dim_ambient)
    nz = sorted(e for e in Es if e != zero)
    def span_ok(basis):
        for coefs in itertools.product(range(3), repeat=len(basis)):
            if not any(coefs): continue
            v = tuple(sum(c*b[i] for c, b in zip(coefs, basis)) % 3 for i in range(dim_ambient))
            if v not in Es: return False
        return True
    best = 0; witness = None
    # lines
    lines = [e for e in nz if tuple((2*x) % 3 for x in e) in Es]
    if lines: best = 1; witness = [lines[0]]
    if want >= 2:
        for i, a in enumerate(lines):
            for b in lines[i+1:]:
                if span_ok([a, b]):
                    best = max(best, 2); witness = [a, b]
                    if want >= 3:
                        for c in lines:
                            if c in (a, b): continue
                            if span_ok([a, b, c]):
                                best = 3; witness = [a, b, c]
                                return best, witness
    return best, witness

if __name__ == "__main__":
    direct_k2()
    for d in (2,):
        others, E = defect_set(d)
        n = len(others)
        print(f"d={d}: defect space F_3^{n}, |E_d| = {len(E)} of {3**n}")
        best, w = max_subspace_in(E, n, want=3)
        print(f"d={d}: max dim of linear subspace inside E_d u {{0}}: {best}; witness {w}")
