#!/usr/bin/env python3
r"""Label-set feasibility over F_p^d: CNF encoder, CaDiCaL driver, LRAT check,
and an independent plain-arithmetic model checker.

Copied verbatim (2026-11-11) from the final message of cloud session
claude.ai/code/session_01B1JoCiWoB7SSi6bhNMLfEj ("p = 5, k = 3 gadgets: exhaustive small and large
sets"); only the CADICAL / LRATCHECK defaults were changed to this machine's paths.

Problem.  L subset of F_p^d \ 0 spanning F_p^d.  L is feasible if there are
Phi: L -> S^d and gamma_alpha in F_p^d (alpha != 0) with
  y_alpha(l) = <alpha, Phi(l)> + <gamma_alpha, l>  in S   for all alpha, l,
and for each projective direction [alpha] some lambda in F_p^*, l in L with
y_{lambda alpha}(l) != 0.
Reductions used by the encoder (both exact):
  (R) if S = -S: gamma_{-alpha} = -gamma_alpha (one alpha per +-pair; y_{-alpha} = -y_alpha).
  (N) gamma_{e_j} = 0 for the unit vectors (optional; Phi_j := y_{e_j}).
check_model never uses the CNF and re-verifies the original conditions for all alpha, lambda.
"""
import itertools, os, subprocess, sys, tempfile, time

_HERE = os.path.dirname(os.path.abspath(__file__))
CADICAL = os.environ.get('CADICAL', 'cadical')
LRATCHECK = os.environ.get('LRATCHECK', os.path.join(_HERE, '..', '2026-11-09-lrat-checker-fix', 'lrat-check'))

def vecs(p, d): return [v for v in itertools.product(range(p), repeat=d)]
def nonzero(p, d): return [v for v in vecs(p, d) if any(v)]
def dot(a, b, p): return sum(x * y for x, y in zip(a, b)) % p
def scal(l, v, p): return tuple((l * x) % p for x in v)

def rank(vs, p, d):
    rows = [list(v) for v in vs]; r = 0
    for c in range(d):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p); rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]; rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
    return r

def canon_dir(v, p):
    f = next(x for x in v if x); return scal(pow(f, p - 2, p), v, p)

def encode(L, p=5, d=3, S=(0, 1, 4), use_R=True, use_N=True, gamma_amo=False, guards=False):
    """Return (nvars, clauses, info).  guards=True adds selector sel[l] ("l removed"):
    S-membership clauses of l are relaxed by sel[l], nz_{alpha,l} -> not sel[l],
    sel[l] -> Phi(l) = 0  (universal complement CNF, cover.py)."""
    S = set(x % p for x in S)
    L = sorted(set(tuple(x % p for x in l) for l in L)); assert all(any(l) for l in L)
    if use_R: assert all((-s) % p in S for s in S) and p % 2 == 1
    NZ = nonzero(p, d)
    if use_R:
        reps, seen = [], set()
        for a in NZ:
            if a in seen: continue
            reps.append(a); seen.add(a); seen.add(scal(p - 1, a, p))
    else:
        reps = list(NZ)
    rep_index = {a: i for i, a in enumerate(reps)}
    PHIV = list(itertools.product(sorted(S), repeat=d)); GAMV = vecs(p, d)
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    cl = []
    phi = [[new() for _ in PHIV] for _ in L]
    for li in range(len(L)):
        cl.append(list(phi[li]))
        for i, j in itertools.combinations(phi[li], 2): cl.append([-i, -j])
    sel = [new() for _ in L] if guards else None
    if guards:
        z0 = PHIV.index(tuple([0] * d))
        for li in range(len(L)): cl.append([-sel[li], phi[li][z0]])
    unit = [tuple(1 if k == j else 0 for k in range(d)) for j in range(d)]
    gam = []
    for a in reps:
        g = [new() for _ in GAMV]; gam.append(g); cl.append(list(g))
        if gamma_amo:   # not needed: decode takes any true gamma (its g-values are forced)
            for i, j in itertools.combinations(g, 2): cl.append([-i, -j])
        if use_N and a in unit: cl.append([g[GAMV.index(tuple([0] * d))]])
    A, G, NZv = {}, {}, {}
    bad = [(u, w) for u in range(p) for w in range(p) if (u + w) % p not in S]
    for ai, a in enumerate(reps):
        for li, l in enumerate(L):
            av = [new() for _ in range(p)]; gv = [new() for _ in range(p)]
            A[ai, li] = av; G[ai, li] = gv
            for k, f in enumerate(PHIV): cl.append([-phi[li][k], av[dot(a, f, p)]])
            for k, c in enumerate(GAMV): cl.append([-gam[ai][k], gv[dot(c, l, p)]])
            for i, j in itertools.combinations(range(p), 2):
                cl.append([-av[i], -av[j]]); cl.append([-gv[i], -gv[j]])
            for u, w in bad: cl.append([-av[u], -gv[w]] + ([sel[li]] if guards else []))
    for dv in sorted(set(canon_dir(a, p) for a in NZ)):      # nondegeneracy per direction
        lits = []
        mult_reps = sorted(set(rep_index[scal(lam, dv, p)] for lam in range(1, p) if scal(lam, dv, p) in rep_index))
        for ai in mult_reps:
            for li in range(len(L)):
                if (ai, li) not in NZv:
                    z = new(); NZv[ai, li] = z
                    for u in range(p): cl.append([-z, -A[ai, li][u], -G[ai, li][(-u) % p]])
                    if guards: cl.append([-z, -sel[li]])
                lits.append(NZv[ai, li])
        cl.append(lits)
    info = dict(p=p, d=d, S=sorted(S), L=L, reps=reps, PHIV=PHIV, GAMV=GAMV, phi=phi, gam=gam,
                use_R=use_R, sel=sel, A=A, G=G)
    return nv[0], cl, info

def write_cnf(path, nvars, clauses):
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(clauses)))
        f.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses))

def decode(model, info):
    p = info['p']; Phi = {}; gamma = {}
    for li, l in enumerate(info['L']):
        Phi[l] = info['PHIV'][[k for k, v in enumerate(info['phi'][li]) if model.get(v)][0]]
    for ai, a in enumerate(info['reps']):
        g = info['GAMV'][[k for k, v in enumerate(info['gam'][ai]) if model.get(v)][0]]
        gamma[a] = g
        if info['use_R']: gamma[scal(p - 1, a, p)] = scal(p - 1, g, p)
    return Phi, gamma

def check_model(L, Phi, gamma, p, d, S):
    """Independent plain-arithmetic check of the ORIGINAL conditions (gamma over all alpha)."""
    S = set(x % p for x in S); L = sorted(set(tuple(x % p for x in l) for l in L))
    if rank(L, p, d) != d: return False, 'L does not span'
    for l in L:
        if len(Phi[l]) != d or any(x % p not in S for x in Phi[l]): return False, 'Phi(%s) not in S^d' % (l,)
    alphas = [a for a in itertools.product(range(p), repeat=d) if any(a)]; y = {}
    for a in alphas:
        g = gamma[a]
        for l in L:
            v = (sum(a[j] * Phi[l][j] for j in range(d)) + sum(g[j] * l[j] for j in range(d))) % p
            if v not in S: return False, 'y_%s(%s)=%d not in S' % (a, l, v)
            y[a, l] = v
    seen = set()
    for a in alphas:
        if a in seen: continue
        line = [tuple((lam * x) % p for x in a) for lam in range(1, p)]; seen.update(line)
        if not any(y[b, l] for b in line for l in L): return False, 'direction %s degenerate' % (a,)
    return True, 'ok'

def run_cadical(cnf, timeout, lrat=None):
    args = [CADICAL, '-q', cnf] if not lrat else [CADICAL, '-q', '--lrat=true', '--binary=false', cnf, lrat]
    try: r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired: return 'TIMEOUT', None
    out = r.stdout
    if 's SATISFIABLE' in out:
        model = {}
        for line in out.splitlines():
            if line.startswith('v '):
                for t in line[2:].split():
                    x = int(t)
                    if x: model[abs(x)] = x > 0
        return 'SAT', model
    if 's UNSATISFIABLE' in out: return 'UNSAT', None
    return 'ERROR:' + out[-300:] + r.stderr[-300:], None

def solve(L, p=5, d=3, S=(0, 1, 4), use_R=True, use_N=True, timeout=900, workdir=None, keep=False,
          tag='inst', gamma_amo=False):
    """status = SAT (model re-checked) | UNSAT_VERIFIED (lrat-check 'c VERIFIED') | UNSAT_UNVERIFIED | TIMEOUT"""
    t0 = time.time()
    nvars, clauses, info = encode(L, p, d, S, use_R, use_N, gamma_amo)
    wd = workdir or tempfile.mkdtemp(); cnf = os.path.join(wd, tag + '.cnf'); write_cnf(cnf, nvars, clauses)
    st, model = run_cadical(cnf, timeout); res = dict(L=info['L'], nvars=nvars, nclauses=len(clauses))
    if st == 'SAT':
        Phi, gamma = decode(model, info); ok, msg = check_model(info['L'], Phi, gamma, p, d, S)
        res.update(status='SAT' if ok else 'SAT_CHECK_FAILED:' + msg, Phi=Phi, gamma={a: gamma[a] for a in info['reps']})
    elif st == 'UNSAT':
        lrat = os.path.join(wd, tag + '.lrat'); st2, _ = run_cadical(cnf, timeout, lrat=lrat)
        if st2 != 'UNSAT': res.update(status='UNSAT_UNVERIFIED(' + st2 + ')')
        else:
            r = subprocess.run([LRATCHECK, cnf, lrat], capture_output=True, text=True, timeout=timeout)
            res.update(status='UNSAT_VERIFIED' if 'c VERIFIED' in r.stdout else 'UNSAT_UNVERIFIED', lrat_out=r.stdout[-200:])
        if not keep and os.path.exists(lrat): os.remove(lrat)
    else:
        res.update(status=st)
    if not keep: os.remove(cnf)
    res['time'] = time.time() - t0
    return res

def brute(L, p, d, S):
    """Exhaustive over Phi; gamma independent per alpha; no reductions.  True iff feasible."""
    S = sorted(set(x % p for x in S)); L = sorted(set(L)); alphas = nonzero(p, d); gams = vecs(p, d)
    dirs = {}
    for a in alphas: dirs.setdefault(canon_dir(a, p), []).append(a)
    Sset = set(S)
    for Phis in itertools.product(list(itertools.product(S, repeat=d)), repeat=len(L)):
        okall = True; nzalpha = set()
        for a in alphas:
            base = [dot(a, f, p) for f in Phis]; feas = False
            for g in gams:
                ys = [(b + dot(g, l, p)) % p for b, l in zip(base, L)]
                if all(v in Sset for v in ys):
                    feas = True
                    if any(ys): nzalpha.add(a); break
            if not feas: okall = False; break
        if okall and all(any(a in nzalpha for a in line) for line in dirs.values()): return True
    return False
