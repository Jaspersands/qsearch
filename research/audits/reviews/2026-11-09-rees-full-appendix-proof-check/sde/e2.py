"""Independent exact search for two-level contractions (definition of main.tex 695).

A contraction at (p,kappa) exists iff there are alpha, beta in F_p^kappa with
alpha_j + beta_i in Q^o_{-(i+j)} for all i,j and alpha_0 + beta_0 != 0.
Normalise beta_0 = 0, alpha_0 = 1 (translation; scaling by Q_0).
Then beta_i in Q^o_{-i} - 1 (row j=0), alpha_j in Q^o_{-j} (row i=0) and
alpha_j + beta_i in Q^o_{-i-j} for i,j >= 1.
DFS over beta_1, beta_2, ... with bitset intersections for each column j >= 1.

Mode 'allnz': require every entry nonzero (alpha_j + beta_i in Q_{-i-j}).
Usage: python e2.py
"""
import sys, time
import sympy

def setup(p, kappa, nonzero=False):
    g = sympy.primitive_root(p)
    h = (p - 1) // kappa
    cos = [None] * p
    x = 1
    for e in range(p - 1):
        cos[x] = e % kappa
        x = x * g % p
    # Qo[c] bitset of elements in coset c union {0} (or without 0)
    Q = [0] * kappa
    for y in range(1, p):
        Q[cos[y]] |= 1 << y
    Qo = [q | (0 if nonzero else 1) for q in Q]
    return cos, Qo

def shift(bits, b, p):
    """bitset {y} -> {y - b mod p}"""
    b %= p
    mask = (1 << p) - 1
    return ((bits >> b) | (bits << (p - b))) & mask

def has_contraction(p, kappa, nonzero=False, want_witness=False):
    cos, Qo = setup(p, kappa, nonzero)
    K = kappa
    # candidate sets for beta_i: 1 + beta_i in Qo[-i]  -> beta_i in Qo[-i] - 1
    cand = []
    for i in range(1, K):
        bits = shift(Qo[(-i) % K], 1, p)
        cand.append([y for y in range(p) if bits >> y & 1])
    # initial column sets for alpha_j, j>=1: Qo[-j]
    init = [Qo[(-j) % K] for j in range(1, K)]
    # precompute S[i][j](b) lazily: {alpha: alpha + b in Qo[-i-j]} = shift(Qo[-i-j], b)
    sys.setrecursionlimit(10000)
    nodes = [0]
    def dfs(i, cols, betas):
        nodes[0] += 1
        if i == K:
            return betas
        for b in cand[i - 1]:
            new = []
            for jj, cset in enumerate(cols):
                j = jj + 1
                s = cset & shift(Qo[(-i - j) % K], b, p)
                if not s:
                    break
                new.append(s)
            else:
                r = dfs(i + 1, new, betas + [b])
                if r is not None:
                    return r
        return None
    r = dfs(1, init, [])
    return r, nodes[0]

def E2_upto(kappa, pmax, nonzero=False, pmin=3):
    out = []
    for p in sympy.primerange(pmin, pmax + 1):
        if (p - 1) % kappa:
            continue
        r, n = has_contraction(p, kappa, nonzero)
        if r is None:
            out.append(p)
    return out

if __name__ == "__main__":
    t0 = time.time()
    print("E_2(2) up to 200:", E2_upto(2, 200))
    print("E_2(3) up to 400:", E2_upto(3, 400))
    print("E_2(4) up to 2000 (T_A(4)=869):", E2_upto(4, 2000), f"[{time.time()-t0:.1f}s]")
    print("E_2(5) up to 13000 (T_A(5)=1.27e4):", E2_upto(5, 13000), f"[{time.time()-t0:.1f}s]")
    sys.stdout.flush()
    # cyclotomic two-row obstruction: p = 1 mod kappa, p <= kappa^2-3kappa+3 => p in E_2(kappa)
    for kappa in range(2, 13):
        bound = kappa * kappa - 3 * kappa + 3
        ps = [p for p in sympy.primerange(3, bound + 1) if (p - 1) % kappa == 0]
        mem = [p for p in ps if has_contraction(p, kappa)[0] is None]
        print(f"kappa={kappa}: primes p=1 mod kappa, p<={bound}: {ps}; in E_2: {mem}; claim holds: {mem == ps}")
        sys.stdout.flush()
    # divisor inclusion E_2(D) subset E_2(kappa) on p = 1 mod kappa
    for kappa, D, ps in [(8, 4, [17]), (10, 5, [11, 31, 41, 61, 71]), (12, 4, [13, 37]), (12, 6, [13, 37])]:
        res = {p: has_contraction(p, kappa)[0] is None for p in ps}
        print(f"E_2({D}) -> E_2({kappa}) at {ps}: in E_2({kappa}): {res}")
        sys.stdout.flush()
    print(f"total {time.time()-t0:.1f}s")
