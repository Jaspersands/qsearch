r"""Per-direction line data for the d = 2, k = 2 nested realization problem with interval S
(2026-11-11-rees-sde-interval-s.md, section 3, Lemma L).

For a direction D (normalised so that gamma_D is the value at coset rep 1) the line data are
c_r = gamma_{rD} - r gamma_D in F_p^2 for coset reps r = 2..m (m = (p-1)/2, P = {+-1}).
For a label l the realizers on the line are y_{lam D}(l) = lam f + <c_lam, l>, f = y_D(l) in S.
Necessary condition: for every l in L = F_p^* x F_p the tuple t(l) = (<c_r, l>)_{r=2..m} lies in
T = {t : exists f in S with t_r + r f in S for all r}.  With c_r = (u_r, v_r), t((a,b)) = a u + b v;
labels scale, so the condition is  u + b v in T* := {t : a t in T for all a != 0}  for all b in F_p,
and (u, v) != 0 (else the direction is degenerate, Lemma N').
Symmetries: Aut(L): (u,v) -> (lam u + nu v, mu v); rebasing rho_s: t -> (t_{rs} - r t_s)_r
(t_1 = 0, t_{-x} = -t_x).
Two independent enumerations of the admissible set: (1) brute force over all (u, v) with u in T*
(numpy, membership by integer codes); (2) projective: rank <= 1 data plus projective lines with >= p
points in Q = P(T* \ 0).  They must agree.  Then orbits; output linedata_p{p}_K{K}.json.
usage: linedata.py p K [--no-brute]   (S = {-K..K})
"""
import argparse, itertools, json, sys
import numpy as np


def compute_T_and_Tstar(p, R, S, no_brute):
    Sset = set(S)
    m = (p - 1) // 2
    if not no_brute:
        T = set()
        for f in S:
            for t in itertools.product(*[[(s - r * f) % p for s in S] for r in R]):
                T.add(t)
        Tstar = {t for t in T if all(tuple((a * x) % p for x in t) in T for a in range(1, p))}
        return len(T), Tstar
    # Coordinate-by-coordinate pruned enumeration of projective P(T* \ 0):
    # t in T* iff for every a in 1..m (using S = -S), some f_a in S has (a*t_r + r*f_a) in S for all r in R.
    n = len(R)
    tables = []
    for r in R:
        per_val = []
        for val in range(p):
            amasks = []
            for a in range(1, m + 1):
                bm = 0
                for fi, f in enumerate(S):
                    if (a * val + r * f) % p in Sset:
                        bm |= 1 << fi
                amasks.append(bm)
            per_val.append(tuple(amasks))
        tables.append(per_val)
    proj_pts = []
    for idx0 in range(n):
        ms = list(tables[idx0][1])
        for j in range(idx0):
            zm = tables[j][0]
            ms = [ms[a] & zm[a] for a in range(m)]
        if any(x == 0 for x in ms):
            continue
        states = [((0,) * idx0 + (1,), tuple(ms))]
        for idx in range(idx0 + 1, n):
            tbl = tables[idx]
            nxt = []
            for pref, cur_ms in states:
                for val in range(p):
                    vm = tbl[val]
                    new_ms = []
                    ok = True
                    for a in range(m):
                        nm = cur_ms[a] & vm[a]
                        if nm == 0:
                            ok = False
                            break
                        new_ms.append(nm)
                    if ok:
                        nxt.append((pref + (val,), tuple(new_ms)))
            states = nxt
        for pref, _ in states:
            proj_pts.append(pref)
    Tstar = {(0,) * n}
    for q in proj_pts:
        for c in range(1, p):
            Tstar.add(tuple((c * x) % p for x in q))
    return None, Tstar


ap = argparse.ArgumentParser()
ap.add_argument('p', type=int)
ap.add_argument('K', type=int)
ap.add_argument('--no-brute', action='store_true')
args = ap.parse_args()
p, K, no_brute = args.p, args.K, args.no_brute
S = sorted({x % p for x in range(-K, K + 1)})
m = (p - 1) // 2
R = list(range(2, m + 1)); n = len(R)
def scal(a, t): return tuple((a * x) % p for x in t)
nT, Tstar = compute_T_and_Tstar(p, R, S, no_brute)
t_str = f'{nT} of {p**n}' if nT is not None else 'skipped(--no-brute)'
print(f'p={p} S={S} n={n} |T|={t_str}; |T*|={len(Tstar)}', flush=True)
if not no_brute:
    W = p ** np.arange(n)
    def code(arr): return (arr % p) @ W
    Tcodes = np.array(sorted(code(np.array(t)) for t in Tstar))
    allv = np.array(list(itertools.product(range(p), repeat=n)), dtype=np.int64)
    # (1) brute force
    adm1 = set()
    for u in sorted(Tstar):
        ua = np.array(u, dtype=np.int64)
        ok = np.ones(len(allv), dtype=bool)
        for b in range(p):
            ok &= np.isin(code(ua + b * allv), Tcodes)
        for v in allv[ok]:
            if any(u) or v.any():
                adm1.add((u, tuple(int(x) for x in v)))
    print(f'(1) brute force: admissible (u,v) != 0: {len(adm1)}', flush=True)
else:
    adm1 = None
    print('(1) brute force: skipped (--no-brute)', flush=True)
# (2) projective
def proj(t):
    lead = next(x for x in t if x); inv = pow(lead, p - 2, p)
    return tuple((x * inv) % p for x in t)
Q = {proj(t) for t in Tstar if any(t)}
adm2 = set()
for u in Tstar:
    if not any(u):
        for v in Tstar:
            if any(v): adm2.add((u, v))
    else:
        for c in range(p): adm2.add((u, scal(c, u)))
Ql = sorted(Q); lines = set()
for i in range(len(Ql)):
    for j in range(i + 1, len(Ql)):
        P1, P2 = Ql[i], Ql[j]
        pts = {P1} | {proj(tuple((a * P1[k] + P2[k]) % p for k in range(n))) for a in range(p)}
        if sum(x in Q for x in pts) >= p:
            lines.add(frozenset(pts))
print(f'(2) |Q| = {len(Q)} projective points; lines with >= p points in Q: {len(lines)}', flush=True)
for Lam in lines:
    pts = sorted(Lam)
    for vpt in pts:
        if all(x in Q for x in pts if x != vpt):
            for c in range(1, p):
                v = scal(c, vpt)
                for upt in pts:
                    if upt == vpt: continue
                    for a in range(1, p):
                        for b in range(p):
                            u = tuple((a * upt[k] + b * v[k]) % p for k in range(n))
                            adm2.add((u, v))
if adm1 is not None:
    print(f'(2) projective: admissible (u,v) != 0: {len(adm2)}; agree with (1): {adm1 == adm2}', flush=True)
    assert adm1 == adm2
else:
    # (3) cross-check v in T* - u directly when brute force (1) is skipped
    adm3 = set()
    for u in Tstar:
        for t in Tstar:
            v = tuple((t[i] - u[i]) % p for i in range(n))
            if (any(u) or any(v)) and all(tuple((u[i] + b * v[i]) % p for i in range(n)) in Tstar for b in range(p)):
                adm3.add((u, v))
    print(f'(2) projective: admissible (u,v) != 0: {len(adm2)}; agree with (3): {adm2 == adm3}', flush=True)
    assert adm2 == adm3
adm = adm2
def full(t):
    d = {1: 0, p - 1: 0}
    for i, r in enumerate(R):
        d[r] = t[i] % p; d[p - r] = (-t[i]) % p
    return d
def rho(s, t):
    d = full(t); return tuple((d[(r * s) % p] - r * d[s % p]) % p for r in R)
def act(g, uv):
    lam, mu, nu, s = g; u, v = uv
    u2 = tuple((lam * u[i] + nu * v[i]) % p for i in range(n)); v2 = tuple((mu * v[i]) % p for i in range(n))
    return (rho(s, u2), rho(s, v2))
def prim(p):
    for g in range(2, p):
        if len({pow(g, e, p) for e in range(p - 1)}) == p - 1: return g
g0 = prim(p)
gens = [(g0, 1, 0, 1), (1, g0, 0, 1), (1, 1, 1, 1), (1, 1, 0, g0)]
for uv in adm:
    for g in gens: assert act(g, uv) in adm, (uv, g)
seen = {}; orbits = []
for uv in sorted(adm):
    if uv in seen: continue
    orb = {uv}; stack = [uv]
    while stack:
        x = stack.pop()
        for g in gens:
            y = act(g, x)
            if y not in orb: orb.add(y); stack.append(y)
    for x in orb: seen[x] = len(orbits)
    u, v = uv
    rank = np.linalg.matrix_rank(np.array([u, v]))  # over Q, only a label
    orbits.append((uv, len(orb)))
print(f'orbits under Aut(L) x rebasing: {len(orbits)}; sizes sum {sum(s for _, s in orbits)}', flush=True)
for i, (uv, sz) in enumerate(orbits):
    u, v = uv
    kind = 'v=0' if not any(v) else ('u=0' if not any(u) else 'u,v!=0')
    print(f'  orbit {i}: size {sz} rep u={u} v={v} ({kind})')
with open(f'linedata_p{p}_K{K}.json', 'w') as f:
    json.dump({'p': p, 'K': K, 'R': R, 'n_adm': len(adm),
               'orbits': [[list(uv[0]), list(uv[1]), sz] for uv, sz in orbits],
               'adm': sorted([list(u), list(v)] for u, v in adm)}, f)
