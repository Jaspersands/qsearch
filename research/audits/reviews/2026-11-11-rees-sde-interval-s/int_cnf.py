r"""Compact CNF for the d = 2 realization problem of the F_q nest note (2026-11-08-rees-sde-fq-nest.md,
Lemma 2), written for this note (2026-11-11) independently of gadget_cnf5.py / free_cnf.py.

Problem.  Labels L subset F_p^k, S subset F_p.  Find Phi: L -> S^2 and gamma_alpha in F_p^k
(alpha in F_p^2 \ 0, gamma_{e1} = gamma_{e2} = 0) with
    y_alpha(l) = <alpha, Phi(l)> + <gamma_alpha, l> in S        for all alpha != 0, l in L,
and weak nondegeneracy: every projective direction [D] has some lam*D and l with y_{lam D}(l) != 0.
(One column per label; Lemma 2(B).)

Modes (what is assumed of a solution):
  free  : nothing; gamma_alpha free for every alpha except e1, e2; Phi free on every label.
  freeR : Lemma R only (gamma_{nu alpha} = nu gamma_alpha for nu in P = Stab(S)); Phi free on every label.
  equi  : Lemma R and label P-equivariance Phi(nu l) = nu Phi(l) (one label per P-orbit).
Nondegeneracy is always the ORIGINAL condition (some y != 0), never the Lemma N' criterion,
unless --nondeg gamma is given.

Encoding.  One ALO group per label (Phi value) and per slot (gamma value); aux T[D,l,t] <- <D,Phi(l)> = t,
U[s,l,u] <- <gamma_s, l> = u; a binary clause ~T v ~U for every (t,u) with lam t + u not in S
(slot s = (D, lam), alpha = lam D).  At-most-one is not needed for soundness: every clause is an
implication from each true value, so any true value of each group decodes to a solution (decoding picks
the first), and every real solution gives a model.  --amo adds pairwise AMO anyway.
Every model is decoded, expanded to all alpha and all labels, and checked by check_solution (plain
arithmetic over all alpha, all labels, all directions).

CLI: int_cnf.py p S L mode [--fix 'D1,D2,lam:x,y;...'] [--amo] [--nondeg y|gamma] [--work DIR]
     [--solver cadical|pycosat] [--no-proof] [--keep] [--tag T] [--lines FILE]
S: int:K | set:a,b,..  L: nest | all | file:PATH (one label per line)
"""
import sys, os, itertools, argparse, hashlib, subprocess, tempfile, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
LRAT = os.path.normpath(os.path.join(HERE, '..', '2026-11-09-lrat-checker-fix', 'lrat-check'))


def parse_S(p, spec):
    kind, _, arg = spec.partition(':')
    if kind == 'int':
        K = int(arg); return sorted({x % p for x in range(-K, K + 1)})
    if kind == 'set':
        return sorted({int(x) % p for x in arg.split(',')})
    raise ValueError(spec)


def parse_L(p, k, spec):
    if spec == 'nest':
        return [l for l in itertools.product(range(p), repeat=k) if l[0] != 0]
    if spec == 'all':
        return [l for l in itertools.product(range(p), repeat=k) if any(l)]
    if spec.startswith('file:'):
        with open(spec[5:]) as f:
            return [tuple(int(x) % p for x in line.split()) for line in f if line.strip()]
    raise ValueError(spec)


def stabiliser(p, S):
    Ss = set(S)
    P = [x for x in range(1, p) if {(x * s) % p for s in S} == Ss]
    reps, seen = [], set()
    for x in range(1, p):
        if x not in seen:
            reps.append(x); seen |= {(x * y) % p for y in P}
    return P, reps


def directions(p):
    return [a for a in itertools.product(range(p), repeat=2) if any(a) and a[0 if a[0] else 1] == 1]


def check_solution(p, S, k, L, Phi, gamma):
    """plain arithmetic: Phi[l] in S^2 for all l in L, gamma[alpha] for all alpha != 0; returns (ok, why)"""
    Ss = set(S)
    if set(Phi) != set(L): return False, 'Phi domain'
    for l in L:
        if Phi[l][0] not in Ss or Phi[l][1] not in Ss: return False, ('Phi not in S^2', l)
    if gamma[(1, 0)] != (0,) * k or gamma[(0, 1)] != (0,) * k: return False, 'normalisation'
    nz = {}
    for a1 in range(p):
        for a2 in range(p):
            if a1 == 0 and a2 == 0: continue
            g = gamma[(a1, a2)]
            lead = a1 if a1 else a2
            inv = pow(lead, p - 2, p)
            key = ((a1 * inv) % p, (a2 * inv) % p)
            for l in L:
                y = (a1 * Phi[l][0] + a2 * Phi[l][1] + sum(g[i] * l[i] for i in range(k))) % p
                if y not in Ss: return False, ('y not in S', (a1, a2), l, y)
                if y: nz[key] = True
            nz.setdefault(key, False)
    if len(nz) != p + 1 or not all(nz.values()): return False, 'degenerate direction'
    return True, None


def build(p, S, k, L, mode, fix=None, amo=False, nondeg='y', lines=None):
    Ss = set(S)
    P, creps = stabiliser(p, S)
    dirs = directions(p)
    unit = {(1, 0), (0, 1)}
    if mode == 'free':
        lams = list(range(1, p))
    else:
        lams = creps
    slots = [(D, lam) for D in dirs for lam in lams]
    fixed0 = {(D, 1) for D in unit}
    if mode == 'equi':
        Lv, seen = [], set()
        for l in L:
            if l in seen: continue
            Lv.append(l); seen |= {tuple((nu * x) % p for x in l) for nu in P}
        Lclos = {tuple((nu * x) % p for x in l) for l in L for nu in P}
        assert Lclos == set(L), 'equi mode needs a P-closed label set'
    else:
        Lv = list(L)
    phis = list(itertools.product(S, repeat=2))
    gvals = list(itertools.product(range(p), repeat=k))
    nv = [0]; cl = []
    def var():
        nv[0] += 1; return nv[0]
    def group(m):
        vs = [var() for _ in range(m)]
        cl.append(vs[:])
        if amo:
            for i in range(m):
                for j in range(i + 1, m): cl.append([-vs[i], -vs[j]])
        return vs
    Phv = {l: group(len(phis)) for l in Lv}
    Gv = {s: group(len(gvals)) for s in slots if s not in fixed0}
    T = {}
    for D in dirs:
        for l in Lv:
            ts = [var() for _ in range(p)]
            T[(D, l)] = ts
            for i, ph in enumerate(phis):
                cl.append([-Phv[l][i], ts[(D[0] * ph[0] + D[1] * ph[1]) % p]])
    nzs = {D: [] for D in dirs}
    for s in slots:
        D, lam = s
        for l in Lv:
            ts = T[(D, l)]
            nz = var(); nzs[D].append(nz)
            if s in fixed0:
                for t in range(p):
                    v = (lam * t) % p
                    if v not in Ss: cl.append([-ts[t]])
                    elif v == 0: cl.append([-nz, -ts[t]])
                continue
            us = [var() for _ in range(p)]
            for gi, g in enumerate(gvals):
                cl.append([-Gv[s][gi], us[sum(g[i] * l[i] for i in range(k)) % p]])
            for t in range(p):
                for u in range(p):
                    v = (lam * t + u) % p
                    if v not in Ss: cl.append([-ts[t], -us[u]])
                    elif v == 0: cl.append([-nz, -ts[t], -us[u]])
    if nondeg == 'none':
        pass
    elif nondeg == 'y':
        for D in dirs: cl.append(nzs[D])
    elif nondeg == 'gamma':   # Lemma N' criterion (needs F_p^* not inside S): some gamma_{lam D} != lam gamma_D
        assert mode != 'free' or True
        for D in dirs:
            es = []
            for lam in lams:
                if lam == 1: continue
                e = var(); es.append(e)
                s = (D, lam); s1 = (D, 1)
                for gi, g in enumerate(gvals):
                    if s1 in fixed0:
                        if not any(g): cl.append([-e, -Gv[s][gi]])
                    else:
                        for hi, h in enumerate(gvals):
                            if all((g[i] - lam * h[i]) % p == 0 for i in range(k)):
                                cl.append([-e, -Gv[s][gi], -Gv[s1][hi]])
            cl.append(es)
    for (D, lam), g in (fix or {}).items():
        cl.append([Gv[(D, lam)][gvals.index(tuple(g))]])
    meta = dict(P=P, creps=creps, dirs=dirs, slots=slots, fixed0=fixed0, Lv=Lv, phis=phis, gvals=gvals,
                Phv=Phv, Gv=Gv, lams=lams)
    return nv[0], cl, meta


def decode(p, S, k, L, mode, meta, pos):
    P = meta['P']
    Phi = {}
    for l in meta['Lv']:
        ph = meta['phis'][next(i for i, v in enumerate(meta['Phv'][l]) if v in pos)]
        if mode == 'equi':
            for nu in P:
                Phi[tuple((nu * x) % p for x in l)] = tuple((nu * x) % p for x in ph)
        else:
            Phi[l] = ph
    gamma = {}
    for s in meta['slots']:
        D, lam = s
        g = (0,) * k if s in meta['fixed0'] else meta['gvals'][next(i for i, v in enumerate(meta['Gv'][s]) if v in pos)]
        a = ((lam * D[0]) % p, (lam * D[1]) % p)
        if mode == 'free':
            gamma[a] = g
        else:
            for nu in P:
                gamma[((nu * a[0]) % p, (nu * a[1]) % p)] = tuple((nu * x) % p for x in g)
    return {l: Phi[l] for l in L}, gamma


def solve(p, S, k, L, mode, fix=None, amo=False, nondeg='y', work=None, solver='cadical', proof=True,
          keep=False, tag='case', lines=None, timeout=None):
    t0 = time.time()
    n, cl, meta = build(p, S, k, L, mode, fix, amo, nondeg, lines)
    tb = time.time() - t0
    info = {'vars': n, 'clauses': len(cl), 'build_s': round(tb, 1)}
    if solver == 'pycosat':
        import pycosat
        sol = pycosat.solve(cl)
        if sol == 'UNSAT':
            info['proof'] = 'none (pycosat)'; return 'UNSAT', info, None
        pos = {v for v in sol if v > 0}
    else:
        work = work or tempfile.mkdtemp()
        os.makedirs(work, exist_ok=True)
        cnf = os.path.join(work, tag + '.cnf'); prf = os.path.join(work, tag + '.lrat')
        h = hashlib.sha256()
        with open(cnf, 'w') as f:
            hdr = f'p cnf {n} {len(cl)}\n'; f.write(hdr); h.update(hdr.encode())
            for c in cl:
                line = ' '.join(map(str, c)) + ' 0\n'; f.write(line); h.update(line.encode())
        info['cnf_sha256'] = h.hexdigest()
        del cl
        cmd = ['nice', '-n', '19', 'cadical', '-q'] + (['-t', str(timeout)] if timeout else []) + (['--lrat=true', '--binary=false', cnf, prf] if proof else [cnf])
        t1 = time.time(); r = subprocess.run(cmd, capture_output=True, text=True)
        info['solve_s'] = round(time.time() - t1, 1)
        if r.returncode == 20:
            if proof:
                info['proof_bytes'] = os.path.getsize(prf)
                t2 = time.time()
                ch = subprocess.run(['nice', '-n', '19', LRAT, cnf, prf], capture_output=True, text=True)
                ok = ch.returncode == 0 and 'c VERIFIED' in ch.stdout.splitlines()
                info['check_s'] = round(time.time() - t2, 1)
                info['proof'] = 'LRAT VERIFIED (fixed lrat-check)' if ok else 'LRAT FAILED: ' + ch.stdout[-300:]
            else:
                info['proof'] = 'none'
            if not keep:
                for x in (cnf, prf):
                    if os.path.exists(x): os.remove(x)
            return 'UNSAT', info, None
        if r.returncode == 0 and timeout:
            info['note'] = f'cadical time limit {timeout}s reached'
            for x in (cnf, prf):
                if os.path.exists(x) and not keep: os.remove(x)
            return 'UNKNOWN', info, None
        if r.returncode != 10:
            raise RuntimeError(f'cadical exit {r.returncode}: {r.stderr[-300:]}')
        pos = set()
        for line in r.stdout.splitlines():
            if line.startswith('v '):
                pos |= {int(x) for x in line[2:].split() if int(x) > 0}
        if not keep:
            for x in (cnf, prf):
                if os.path.exists(x): os.remove(x)
    Phi, gamma = decode(p, S, k, L, mode, meta, pos)
    ok, why = check_solution(p, S, k, L, Phi, gamma)
    info['model_check'] = 'OK' if ok else f'FAILED {why}'
    return 'SAT', info, (Phi, gamma)


def parse_fix(s):
    fix = {}
    for item in filter(None, s.split(';')):
        lhs, rhs = item.split(':')
        d1, d2, lam = [int(x) for x in lhs.split(',')]
        fix[((d1, d2), lam)] = tuple(int(x) for x in rhs.split(','))
    return fix


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('L'); ap.add_argument('mode')
    ap.add_argument('--fix', default=''); ap.add_argument('--amo', action='store_true')
    ap.add_argument('--nondeg', default='y'); ap.add_argument('--work', default=None)
    ap.add_argument('--solver', default='cadical'); ap.add_argument('--no-proof', action='store_true')
    ap.add_argument('--keep', action='store_true'); ap.add_argument('--tag', default=None)
    ap.add_argument('--show', action='store_true'); ap.add_argument('--timeout', type=int, default=None)
    A = ap.parse_args()
    S = parse_S(A.p, A.S); L = parse_L(A.p, 2, A.L)
    tag = A.tag or hashlib.sha1(repr((A.p, A.S, A.L, A.mode, A.fix, A.amo, A.nondeg)).encode()).hexdigest()[:12]
    res, info, sol = solve(A.p, S, 2, L, A.mode, parse_fix(A.fix), A.amo, A.nondeg, A.work, A.solver,
                           not A.no_proof, A.keep, tag, timeout=A.timeout)
    print(f'p={A.p} S={S} L={A.L} |L|={len(L)} mode={A.mode} nondeg={A.nondeg} amo={A.amo} fix={A.fix or "-"}: '
          f'{res} {json.dumps(info)}', flush=True)
    if sol and A.show:
        Phi, gamma = sol
        for l in sorted(Phi): print('  Phi', l, Phi[l])
        for a in sorted(gamma): print('  gamma', a, gamma[a])
