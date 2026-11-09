"""Binary-clause CNF for the d in {1,2} realization problem with the coset reduction (Lemma R)
and the P-scaling label reduction (Lemma Q):

  * phi(l) in S^d is ONE one-hot variable per label (|S|^d values);
  * gamma_{r_c alpha_D} in F_p^k is one one-hot per (direction D, coset c), p^k values
    (gamma = 0 for the unit directions at coset 0);
  * for every slot (D, c), label l, phi value and gamma value with
        r_c <alpha_D, phi> + <gamma, l>  not in S
    a binary clause forbids the pair;
  * labels are taken up to P-scaling (lambda l ~ l, phi ~ lambda phi);
  * weak nondegeneracy: for every direction D, some label l, coset c, with
        r_c <alpha_D, phi(l)> + <gamma_{D,c}, l> != 0.
Every model is expanded to all alpha and all labels and re-verified by gadget_cnf.verify.
CLI: p S k d L [--quiet] [--show]

gadget_cnf5: identical encoding to gadget_cnf4, but the CNF is written as DIMACS and solved by an
external solver (cadical, default, with an LRAT proof checked by lrat-check; or kissat with a DRAT
proof checked by drat-trim). UNSAT answers are accepted only after the proof check passes;
SAT answers are expanded and re-verified by gadget_cnf.verify exactly as in gadget_cnf4.
Extra CLI: --solver kissat|cadical  --work DIR  --no-proof  --keep
"""
import sys, itertools, time, argparse
import os, subprocess, hashlib, tempfile, shutil
from gadget_sat import parse_S, parse_L
from gadget_cnf import CNF, verify
from gadget_cnf3 import cosets


DRAT_TRIM = os.environ.get('DRAT_TRIM', 'drat-trim')
LRAT_CHECK = os.environ.get('LRAT_CHECK', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-09-lrat-checker-fix', 'lrat-check')))   # fixed build (9 Nov); run its build.sh


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


def external_solve(n, clauses, solver='cadical', work=None, proof=True, keep=False, tag='case'):
    """write DIMACS, run the solver, check UNSAT proofs with drat-trim.
    returns ('UNSAT', info) or (model list, info); info records sha256 of the CNF and the proof check."""
    work = work or tempfile.mkdtemp()
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, tag + '.cnf')
    with open(cnf, 'w') as f:
        f.write(f'p cnf {n} {len(clauses)}\n')
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    sha = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
    prf = os.path.join(work, tag + '.drat')
    if solver == 'kissat':
        cmd = ['kissat', '-q', cnf] + ([prf] if proof else ['-n'])
    elif solver == 'cadical':   # text LRAT proof, checked by lrat-check (linear time)
        prf = os.path.join(work, tag + '.lrat')
        cmd = ['cadical', '-q', '--lrat=true', '--binary=false', cnf] + ([prf] if proof else ['-n'])
    else:
        raise ValueError(solver)
    r = subprocess.run(cmd, capture_output=True, text=True)
    info = {'cnf_sha256': sha, 'solver': solver, 'vars': n, 'clauses': len(clauses)}
    if r.returncode == 20:
        if proof:
            t = time.time()
            if solver == 'cadical':
                require_sound_lrat_check(LRAT_CHECK)
                ch = subprocess.run([LRAT_CHECK, cnf, prf], capture_output=True, text=True)
                ok = ch.returncode == 0 and 'c VERIFIED' in ch.stdout and 'failed' not in ch.stdout
            else:
                ch = subprocess.run([DRAT_TRIM, cnf, prf, '-f'], capture_output=True, text=True)
                ok = 's VERIFIED' in ch.stdout
            info['proof'] = ('LRAT' if solver == 'cadical' else 'DRAT') + (' VERIFIED' if ok else ' FAILED')
            info['check_s'] = round(time.time() - t, 1)
            info['proof_bytes'] = os.path.getsize(prf)
            if not ok:
                raise RuntimeError('proof check did not verify: ' + ch.stdout[-500:])
        if not keep:
            for x in (cnf, prf):
                if os.path.exists(x): os.remove(x)
        return 'UNSAT', info
    if r.returncode == 10:
        model = []
        for line in r.stdout.splitlines():
            if line.startswith('v '):
                model += [int(x) for x in line[2:].split() if x != '0']
        if not keep:
            for x in (cnf, prf):
                if os.path.exists(x): os.remove(x)
        return model, info
    raise RuntimeError(f'solver exit {r.returncode}: {r.stderr[-500:]}')


def reduce_labels(p, P, L):
    """one representative per P-orbit of labels"""
    seen, reps = set(), []
    for l in L:
        if l in seen:
            continue
        reps.append(l)
        for lam in P:
            seen.add(tuple((lam * x) % p for x in l))
    return reps


def solve4(p, S, k, d, L, weak=True, verbose=False, fix=None, ext=None):
    """fix: {(direction tuple, coset index): gamma tuple} forced values (case splits)"""
    S = sorted(S); Sset = set(S)
    P, creps = cosets(p, S)
    kappa = len(creps)
    # feasibility (with weak nondegeneracy) of L equals that of its P-closure (Lemma Q)
    Lclos = sorted({tuple((lam * x) % p for x in l) for l in L for lam in P})
    Lred = reduce_labels(p, P, Lclos)
    dirs = []
    for a in itertools.product(range(p), repeat=d):
        if any(a) and a[next(i for i, x in enumerate(a) if x)] == 1:
            dirs.append(a)
    unit = {tuple(1 if i == j else 0 for i in range(d)) for j in range(d)}
    phis = list(itertools.product(S, repeat=d))
    gvals = list(itertools.product(range(p), repeat=k))
    c = CNF()
    phi = {l: c.onehot(len(phis)) for l in Lred}
    slots = [(D, ci) for D in range(len(dirs)) for ci in range(kappa)]
    fixed = {(D, ci) for (D, ci) in slots if ci == 0 and dirs[D] in unit}
    g = {s: c.onehot(len(gvals)) for s in slots if s not in fixed}
    dir_nz = {D: [] for D in range(len(dirs))}
    for (D, ci) in slots:
        a = dirs[D]; r = creps[ci]
        for l in Lred:
            nz = c.var()
            dir_nz[D].append(nz)
            for pi, ph in enumerate(phis):
                base = (r * sum(a[j] * ph[j] for j in range(d))) % p
                if (D, ci) in fixed:
                    if base not in Sset:
                        c.clauses.append([-phi[l][pi]])
                    elif base == 0:
                        c.clauses.append([-nz, -phi[l][pi]])
                    continue
                for gi, gv in enumerate(gvals):
                    val = (base + sum(gv[i] * l[i] for i in range(k))) % p
                    if val not in Sset:
                        c.clauses.append([-phi[l][pi], -g[(D, ci)][gi]])
                    elif val == 0:
                        c.clauses.append([-nz, -phi[l][pi], -g[(D, ci)][gi]])
    for D, nzs in dir_nz.items():
        c.clauses.append(nzs)
    if fix:
        for (dvec, ci), gv in fix.items():
            D = dirs.index(tuple(dvec))
            c.clauses.append([g[(D, ci)][gvals.index(tuple(gv))]])
    if verbose:
        print(f'  P={P} coset reps={creps} |Lred|={len(Lred)}; cnf: {c.n} vars, {len(c.clauses)} clauses', flush=True)
    t0 = time.time()
    sol, info = external_solve(c.n, c.clauses, **ext)
    dt = time.time() - t0
    if sol == 'UNSAT':
        return 'unsat', info, dt
    pos = set(v for v in sol if v > 0)
    Phi_red = {l: phis[[i for i, v in enumerate(phi[l]) if v in pos][0]] for l in Lred}
    grep = {}
    for (D, ci) in slots:
        a = tuple((creps[ci] * x) % p for x in dirs[D])
        grep[a] = (0,) * k if (D, ci) in fixed else gvals[[i for i, v in enumerate(g[(D, ci)]) if v in pos][0]]
    # expand gamma to all alpha and Phi to all labels
    gamma, Phi = {}, {}
    for a, gv in grep.items():
        for lam in P:
            gamma[tuple((lam * x) % p for x in a)] = tuple((lam * x) % p for x in gv)
    for l, ph in Phi_red.items():
        for lam in P:
            Phi[tuple((lam * x) % p for x in l)] = tuple((lam * x) % p for x in ph)
    assert len(gamma) == p ** d - 1 and set(Phi) == set(Lclos)
    Phi = {l: Phi[l] for l in L}
    ok, why = verify(p, S, k, d, L, Phi, gamma, nondeg=True, weak=weak)
    assert ok, why
    return 'sat', (Phi, gamma, info), dt


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int); ap.add_argument('d', type=int); ap.add_argument('L')
    ap.add_argument('--quiet', action='store_true'); ap.add_argument('--show', action='store_true')
    ap.add_argument('--fix', default='', help='D1,D2,c:x,y;...')
    ap.add_argument('--solver', default='cadical'); ap.add_argument('--work', default=None)
    ap.add_argument('--no-proof', action='store_true'); ap.add_argument('--keep', action='store_true')
    A = ap.parse_args()
    fix = {}
    for item in filter(None, A.fix.split(';')):
        lhs, rhs = item.split(':')
        *dv, ci = [int(x) for x in lhs.split(',')]
        fix[(tuple(dv), ci)] = tuple(int(x) for x in rhs.split(','))
    S = parse_S(A.p, A.S); L = parse_L(A.p, A.k, A.L)
    tag = f"p{A.p}_{A.S.replace(':', '')}_k{A.k}_d{A.d}_{A.L}" + ('_' + hashlib.sha1(A.fix.encode()).hexdigest()[:10] if A.fix else '')
    ext = dict(solver=A.solver, work=A.work, proof=not A.no_proof, keep=A.keep, tag=tag)
    r, sol, dt = solve4(A.p, S, A.k, A.d, L, verbose=not A.quiet, fix=fix, ext=ext)
    info = sol if r == 'unsat' else sol[2]
    print(f'p={A.p} S={S} k={A.k} d={A.d} L={A.L} (|L|={len(L)}) [reduced, weak nondeg]{" fix=" + A.fix if A.fix else ""}: {r.upper()} [{dt:.1f}s] {info}', flush=True)
    if sol and A.show:
        Phi, gamma, _ = sol
        for l in sorted(Phi): print('  ', l, '->', Phi[l])
        for a in sorted(gamma): print('  ', a, '->', gamma[a])
