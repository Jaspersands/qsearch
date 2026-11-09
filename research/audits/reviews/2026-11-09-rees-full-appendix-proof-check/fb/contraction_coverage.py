"""fb check 7: the coverage/refusal sentence of app:backends-scope (appendix-backends.tex:45).

Re-runs, read-only, the repo's contraction search theorems/rees_coherent_sde_kappa.canonical_contraction
(the one kappa_constants uses, exact DFS for p <= 2e6) and compares with the paper:
  E_2(3) = {} (cor:app-s2-small), E_2(4) = {5,13,17,29,37,53} (main.tex text after lem:coherent-power-sde),
  every kappa = p-1 grade with p >= 5 lies in E_2 (same text);
and checks that the generator's kappa >= 3 path refuses p in E_2(kappa) with ValueError
(CoherentSDEKappa -> kappa_constants).  Each returned contraction is re-validated by contraction_valid.
Run from the repo root.  Finite checks only (can falsify, cannot prove)."""
import sys, time
sys.path.insert(0, '.')
from sympy import primerange
import theorems.rees_coherent_sde_kappa as K

def none_set(kappa, pmax):
    out, n = [], 0
    for p in primerange(3, pmax):
        if (p - 1) % kappa:
            continue
        n += 1
        g = K.coset_generator(p, kappa)
        c = K.canonical_contraction(p, kappa, g)
        if c is None:
            out.append(p)
        else:
            assert K.contraction_valid(p, kappa, g, c[0], c[1]), (p, kappa, c)
    return out, n

t0 = time.time()
for kappa, pmax in [(3, 3000), (4, 1100), (5, 700), (6, 400)]:
    s, n = none_set(kappa, pmax)
    print(f"kappa={kappa}: primes p = 1 mod kappa below {pmax}: {n}; no normalised contraction at {s}", flush=True)
for p in [5, 7, 11, 13]:
    c = K.canonical_contraction(p, p - 1)
    print(f"kappa = p-1 = {p-1}, p = {p}: contraction {'NONE (in E_2)' if c is None else c}", flush=True)
for (p, d) in [(13, 4), (5, 4), (17, 4), (7, 6)]:
    try:
        K.kappa_constants(p, d)
        print(f"kappa_constants(p={p}, d={d}): returned constants (NOT refused)")
    except ValueError as e:
        print(f"kappa_constants(p={p}, d={d}): refused: {e}")
print(f"time {time.time()-t0:.1f}s")
