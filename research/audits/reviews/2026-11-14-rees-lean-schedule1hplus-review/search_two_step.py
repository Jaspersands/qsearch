"""Find small primes with contractions for a two-step chain (GE; (2,Z2,{0}); (4,{0,2},{0}))
and print one contraction per step (beta_0 = 0), xi = least primitive root.  Exhaustive."""
import itertools, sys
def prim_root(p):
    fs = {q for q in range(2, p) if (p-1) % q == 0 and all(q % r for r in range(2, q))}
    return next(g for g in range(2, p) if all(pow(g, (p-1)//q, p) != 1 for q in fs))
def cl(x, D, p, g):
    t = pow(x, (p-1)//D, p); z = pow(g, (p-1)//D, p)
    return next(i for i in range(D) if pow(z, i, p) == t)
def find(p, D, Delta, Omega):
    g = prim_root(p)
    rest = [i for i in Delta if i != 0]
    for bvals in itertools.product(range(p), repeat=len(rest)):
        beta = {0: 0, **dict(zip(rest, bvals))}
        alpha = []
        ok = True
        for j in range(D):
            cand = None
            for a in range(p):
                if j == 0 and (a == 0 or cl(a, D, p, g) != 0):   # alpha_0 + beta_0 in P_D
                    continue
                if all((a + beta[i]) % p == 0 or (cl((a+beta[i]) % p, D, p, g) + i + j) % D in Omega for i in Delta):
                    cand = a; break
            if cand is None: ok = False; break
            alpha.append(cand)
        if ok: return g, alpha, [beta.get(i, 0) for i in range(D)]
    return None
for p in [5, 13, 17, 29, 37, 41]:
    s1 = find(p, 2, [0, 1], {0}); s2 = find(p, 4, [0, 2], {0})
    print(p, s1, s2, flush=True)
    if s1 and s2: break
