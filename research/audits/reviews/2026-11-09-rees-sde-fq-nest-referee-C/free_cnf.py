"""Referee C: independent re-encoding of the d = 2 realization problem of the F_q nest note,
WITHOUT the label-scaling reduction (Lemma Q): every label of L gets its own Phi(l) in S^2
(one column per label, as in Lemma 2(B)).  Optionally also without the coset reduction (Lemma R):
then gamma_alpha is free for every alpha != 0 except the unit vectors (gamma = 0).

Problem: Phi: L -> S^2, gamma_alpha in F_p^k, such that for all alpha != 0 and l in L
    y_alpha(l) = <alpha, Phi(l)> + <gamma_alpha, l>  in S,
and weak nondegeneracy: for every projective direction [alpha] some lambda alpha (lambda in F_p^*)
has y_{lambda alpha} != 0 at some label.

With Lemma R (default): gamma is a variable only for alpha = r_c * D (D projective rep with leading
coordinate 1, r_c coset reps of P = stabiliser of S); gamma_{lam alpha} := lam gamma_alpha for lam in
P is implied (the constraints at lam*alpha are those at alpha since lam S = S).

CLI: p S k L [--noR] [--fix 'D1,D2,c:x,y;...'] [--proof] ; S as in gadget_sat.parse_S
Every SAT model is re-verified over ALL alpha and ALL labels by the independent check below.
"""
import sys, os, itertools, subprocess, tempfile, time, argparse, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '2026-11-08-rees-sde-fq-nest')
sys.path.insert(0, SRC)
from gadget_sat import parse_S, parse_L  # parsing only

# 9 Nov: the default was an unsound upstream build in a session scratchpad; now the fixed build.
LRAT = os.environ.get('LRAT_CHECK', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-09-lrat-checker-fix', 'lrat-check')))


_LRAT_SOUND = {}


def lrat_check_is_sound(checker):
    """Preflight added 9 Nov 2026 (research/audits/reviews/2026-11-09-lrat-checker-fix/): the upstream
    lrat-check accepted an empty clause without a conflict, so any CNF 'verified' with a one-line proof.
    True iff `checker` rejects two such proofs of a satisfiable CNF and verifies a correct proof of an
    unsatisfiable one. Cached per checker path."""
    if checker not in _LRAT_SOUND:
        d = tempfile.mkdtemp()

        def verified(cnf, prf):
            a, b = os.path.join(d, 'c.cnf'), os.path.join(d, 'c.lrat')
            with open(a, 'w') as f:
                f.write(cnf)
            with open(b, 'w') as f:
                f.write(prf)
            r = subprocess.run([checker, a, b], capture_output=True, text=True)
            return r.returncode == 0 and 'c VERIFIED' in r.stdout.splitlines()
        try:
            _LRAT_SOUND[checker] = (not verified('p cnf 1 1\n1 0\n', '2 0 0\n')
                                    and not verified('p cnf 1 1\n1 0\n', '2 0 1 -1 0\n')
                                    and verified('p cnf 1 2\n1 0\n-1 0\n', '3 0 1 2 0\n'))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return _LRAT_SOUND[checker]


def require_sound_lrat_check(checker):
    if not lrat_check_is_sound(checker):
        raise RuntimeError(f'{checker} failed the lrat-check negative control (it verifies a bogus proof); '
                           'use the fixed build, research/audits/reviews/2026-11-09-lrat-checker-fix/build.sh')


def stab(p, S):
    Ss = set(S)
    P = [l for l in range(1, p) if {(l * s) % p for s in S} == Ss]
    reps, seen = [], set()
    for x in range(1, p):
        if x not in seen:
            reps.append(x); seen |= {(x * l) % p for l in P}
    return P, reps


def build(p, S, k, L, useR=True, fix=None):
    Ss = set(S)
    P, creps = stab(p, S)
    dirs = [a for a in itertools.product(range(p), repeat=2) if any(a) and a[0 if a[0] else 1] == 1]
    unit = {(1, 0), (0, 1)}
    if useR:
        slots = [(D, r) for D in dirs for r in creps]
    else:
        slots = [(D, r) for D in dirs for r in range(1, p)]
    alpha = {s: ((s[1] * s[0][0]) % p, (s[1] * s[0][1]) % p) for s in slots}
    n = [0]; cl = []
    def var():
        n[0] += 1; return n[0]
    def onehot(m):
        vs = [var() for _ in range(m)]
        cl.append(vs[:])
        for i in range(m):
            for j in range(i + 1, m):
                cl.append([-vs[i], -vs[j]])
        return vs
    phis = list(itertools.product(S, repeat=2))
    gv = list(itertools.product(range(p), repeat=k))
    phi = {l: onehot(len(phis)) for l in L}
    g = {s: onehot(len(gv)) for s in slots if alpha[s] not in unit}
    nzd = {D: [] for D in dirs}
    for s in slots:
        a = alpha[s]
        for l in L:
            nz = var(); nzd[s[0]].append(nz)
            for pi, ph in enumerate(phis):
                base = (a[0] * ph[0] + a[1] * ph[1]) % p
                if a in unit:
                    if base not in Ss: cl.append([-phi[l][pi]])
                    elif base == 0: cl.append([-nz, -phi[l][pi]])
                    continue
                for gi, gg in enumerate(gv):
                    v = (base + sum(gg[i] * l[i] for i in range(k))) % p
                    if v not in Ss: cl.append([-phi[l][pi], -g[s][gi]])
                    elif v == 0: cl.append([-nz, -phi[l][pi], -g[s][gi]])
    for D in dirs:
        cl.append(nzd[D])
    if fix:
        for (D, ci), val in fix.items():
            s = (D, creps[ci])
            cl.append([g[s][gv.index(val)]])
    return n[0], cl, dict(phi=phi, g=g, phis=phis, gv=gv, slots=slots, alpha=alpha, P=P, unit=unit)


def check(p, S, k, L, Phi, gamma):
    Ss = set(S); ok_dir = {}
    for a in itertools.product(range(p), repeat=2):
        if not any(a): continue
        anynz = False
        for l in L:
            y = (a[0] * Phi[l][0] + a[1] * Phi[l][1] + sum(gamma[a][i] * l[i] for i in range(k))) % p
            if y not in Ss: return False, ('notS', a, l, y)
            anynz |= y != 0
        lead = a[0] if a[0] else a[1]
        key = tuple((x * pow(lead, -1, p)) % p for x in a)
        ok_dir[key] = ok_dir.get(key, False) or anynz
    if not all(ok_dir.values()): return False, ('degenerate', ok_dir)
    return True, None


def run(p, S, k, L, useR=True, fix=None, proof=False, work=None):
    n, cl, M = build(p, S, k, L, useR, fix)
    work = work or tempfile.mkdtemp()
    tag = hashlib.sha1(repr((p, S, k, len(L), useR, sorted((fix or {}).items()))).encode()).hexdigest()[:12]
    cnf = os.path.join(work, tag + '.cnf'); prf = os.path.join(work, tag + '.lrat')
    with open(cnf, 'w') as f:
        f.write(f'p cnf {n} {len(cl)}\n')
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    cmd = ['cadical', '-q'] + (['--lrat=true', '--binary=false', cnf, prf] if proof else [cnf])
    t = time.time(); r = subprocess.run(cmd, capture_output=True, text=True); dt = time.time() - t
    info = f'{n} vars {len(cl)} clauses {dt:.1f}s'
    if r.returncode == 20:
        if proof:
            require_sound_lrat_check(LRAT)
            ch = subprocess.run([LRAT, cnf, prf], capture_output=True, text=True)
            ok = ch.returncode == 0 and 'c VERIFIED' in ch.stdout and 'failed' not in ch.stdout
            info += ' LRAT ' + ('VERIFIED' if ok else 'FAILED')
            os.remove(prf)
        os.remove(cnf)
        return 'UNSAT', info, None
    assert r.returncode == 10, r.stderr
    os.remove(cnf)
    pos = set()
    for line in r.stdout.splitlines():
        if line.startswith('v '):
            pos |= {int(x) for x in line[2:].split() if int(x) > 0}
    Phi = {l: M['phis'][[i for i, v in enumerate(M['phi'][l]) if v in pos][0]] for l in L}
    gamma = {}
    for s in M['slots']:
        a = M['alpha'][s]
        val = (0,) * k if a in M['unit'] else M['gv'][[i for i, v in enumerate(M['g'][s]) if v in pos][0]]
        lams = M['P'] if useR else [1]
        for lam in lams:
            gamma[((lam * a[0]) % p, (lam * a[1]) % p)] = tuple((lam * x) % p for x in val)
    assert len(gamma) == p * p - 1
    ok, why = check(p, S, k, L, Phi, gamma)
    assert ok, why
    return 'SAT', info, (Phi, gamma)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int); ap.add_argument('L')
    ap.add_argument('--noR', action='store_true'); ap.add_argument('--fix', default='')
    ap.add_argument('--proof', action='store_true'); ap.add_argument('--show', action='store_true')
    A = ap.parse_args()
    fix = {}
    for item in filter(None, A.fix.split(';')):
        lhs, rhs = item.split(':'); *dv, ci = [int(x) for x in lhs.split(',')]
        fix[(tuple(dv), ci)] = tuple(int(x) for x in rhs.split(','))
    S = sorted(parse_S(A.p, A.S)); L = parse_L(A.p, A.k, A.L)
    res, info, sol = run(A.p, S, A.k, L, not A.noR, fix, A.proof)
    print(f'p={A.p} S={S} k={A.k} L={A.L} |L|={len(L)} noQ{" noR" if A.noR else ""} fix={A.fix or "-"}: {res} [{info}]', flush=True)
    if sol and A.show:
        Phi, gamma = sol
        for l in sorted(Phi): print('  ', l, Phi[l])
        for a in sorted(gamma): print('  ', a, gamma[a])
