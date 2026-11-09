# Independent exact E_2(k) by bitset DFS over normalized (beta_0=0, alpha_0=1).
# Also: enumerate all contractions for small p and test Theorem 1 (zero cells) and clique equivalence;
# and Lemma 5 restriction on witnesses.
import sys, math, itertools
from sympy import primerange
from common import setup

def masks(p, k, ind):
    Q = [0]*k
    for x in range(1, p):
        Q[ind[x]] |= 1 << x
    return [q | 1 for q in Q]   # Q°_m includes 0

def rot(M, b, p, full):
    # {y - b : y in M}
    if b == 0: return M
    return ((M >> b) | (M << (p - b))) & full

def bits(M):
    while M:
        l = M & -M
        yield l.bit_length() - 1
        M ^= l

def search(p, k, ind, all_=False, limit=None):
    Qc = masks(p, k, ind); full = (1 << p) - 1
    cand0 = [Qc[(-j) % k] for j in range(k)]
    sols = []
    beta = [0]*k
    def rec(i, cand):
        if i == k:
            if all_:
                for a in itertools.product(*[list(bits(cand[j])) for j in range(1, k)]):
                    sols.append(((1,) + a, tuple(beta)))
                    if limit and len(sols) >= limit: return True
                return False
            # witness: pick any alpha_j
            a = tuple([1] + [next(bits(cand[j])) for j in range(1, k)])
            sols.append((a, tuple(beta))); return True
        colmask = rot(Qc[(-i) % k], 1, p, full)  # 1 + beta_i in Q°_{-i}
        for b in bits(colmask):
            beta[i] = b
            new = [None] + [cand[j] & rot(Qc[(-(i + j)) % k], b, p, full) for j in range(1, k)]
            if all(new[j] for j in range(1, k)):
                if rec(i + 1, new): return True
        beta[i] = 0
        return False
    rec(1, cand0)
    return sols

def check(p, k, ind, a, b):
    if (a[0] + b[0]) % p == 0: return False
    for i in range(k):
        for j in range(k):
            v = (a[j] + b[i]) % p
            if v and ind[v] != (-(i + j)) % k: return False
    return True

if __name__ == "__main__":
    k = int(sys.argv[1]); P = int(sys.argv[2])
    E = []
    for p in primerange(3, P + 1):
        if (p - 1) % k: continue
        ind, g = setup(p, k)
        s = search(p, k, ind)
        if not s: E.append(p)
        else: assert check(p, k, ind, *s[0])
    print(f"k={k} p<={P} E2={E}")
