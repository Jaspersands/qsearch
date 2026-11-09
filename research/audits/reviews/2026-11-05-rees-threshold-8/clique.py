"""Transversal Paley cliques (threshold-8, Corollary 3).

C_kappa(p): exist y_1..y_{kappa-1}, y_i in Q_i (Q_i = g^i Q_0, g a primitive root),
with y_i - y_k in Q_0 for all i != k.  Needs -1 in Q_0.  By Corollary 3 of the
report such a set gives the two-level contraction
    beta_i = 1/(g y_{i-1})  (i != 1),  beta_1 = 0,  alpha_j = -beta_{j+1},
which is re-checked here on all kappa^2 cells with pow() (independent of the search).

Usage: python clique.py KAPPA PMIN PMAX [--all]
Prints one line per prime p = 1 mod kappa with -1 in Q_0:
  CLIQUE k= p= y=...      (witness found and contraction verified)
  NOCLIQUE k= p= nodes=   (complete search, none exists)
and SKIP lines for primes with -1 not in Q_0 (h odd, kappa even).
"""
import sys
from sympy import primerange, primitive_root

def setup(p, k):
    g = primitive_root(p)
    cls = [0]*p
    x = 1
    for e in range(p-1):
        cls[x] = e % k
        x = x*g % p
    cls[0] = -1
    return g, cls

def masks(p, k, cls):
    C = [0]*k
    for x in range(1, p):
        C[cls[x]] |= 1 << x
    return C

def rot(M, y, p, full):
    # bitmask of {x + y mod p : x in M}
    return ((M << y) | (M >> (p - y))) & full

def search(p, k, cls, g):
    full = (1 << p) - 1
    C = masks(p, k, cls)
    Q0 = C[0]
    nodes = 0
    # scaling by Q_0 preserves everything: fix y_1 = g (coset 1)
    y1 = g
    rem = {i: C[i] & rot(Q0, y1, p, full) for i in range(2, k)}
    chosen = {1: y1}
    def dfs(rem):
        nonlocal nodes
        nodes += 1
        if not rem:
            return True
        # pick coset with fewest candidates
        i = min(rem, key=lambda t: rem[t].bit_count())
        cand = rem[i]
        if cand == 0:
            return False
        while cand:
            low = cand & -cand
            y = low.bit_length() - 1
            cand ^= low
            N = rot(Q0, y, p, full)
            new = {}
            ok = True
            for t, M in rem.items():
                if t == i: continue
                M2 = M & N
                if M2 == 0:
                    ok = False; break
                new[t] = M2
            if not ok: continue
            chosen[i] = y
            if dfs(new):
                return True
            del chosen[i]
        return False
    found = dfs(rem)
    return (dict(chosen) if found else None), nodes

def contraction_from_clique(p, k, g, y):
    # y: dict i -> y_i in Q_i, i = 1..k-1, differences in Q_0.
    # shift by g: yh_{i+1} = g*y_i in Q_{i+1}; yh defined on Z_k \ {1}; u_i = 1/yh_i; u_1 = 0.
    u = [0]*k
    for i, yi in y.items():
        kk = (i + 1) % k
        u[kk] = pow(g*yi % p, p-2, p)
    beta = u[:]                     # beta_1 = 0
    alpha = [(-beta[(j+1) % k]) % p for j in range(k)]
    return alpha, beta

def check(p, k, g, alpha, beta):
    # independent check with pow: (alpha_j+beta_i) * g^{i+j} must be a kappa-th power or 0
    h = (p-1)//k
    for i in range(k):
        for j in range(k):
            c = (alpha[j] + beta[i]) % p
            if c == 0:
                if i == 0 and j == 0: return False
                continue
            if pow(c * pow(g, i+j, p) % p, h, p) != 1:
                return False
    return (alpha[0] + beta[0]) % p != 0

def main():
    k = int(sys.argv[1]); lo = int(sys.argv[2]); hi = int(sys.argv[3])
    for p in primerange(lo, hi+1):
        if (p-1) % k: continue
        h = (p-1)//k
        if k % 2 == 0 and h % 2 == 1:
            print(f"SKIP k={k} p={p} h_odd", flush=True); continue
        g, cls = setup(p, k)
        y, nodes = search(p, k, cls, g)
        if y is None:
            print(f"NOCLIQUE k={k} p={p} nodes={nodes}", flush=True)
        else:
            a, b = contraction_from_clique(p, k, g, y)
            ok = check(p, k, g, a, b)
            print(f"CLIQUE k={k} p={p} g={g} nodes={nodes} verified={ok} "
                  f"y={','.join(str(y[i]) for i in sorted(y))} alpha={','.join(map(str,a))} beta={','.join(map(str,b))}", flush=True)
            if not ok:
                print("ERROR verification failed", flush=True)

if __name__ == '__main__':
    main()
