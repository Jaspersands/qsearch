#!/usr/bin/env python3
"""Infeasibility of a label set L by labelsat.encode (with (R), (N)) plus a min-support case split,
each case CaDiCaL UNSAT with an LRAT proof checked by the FIXED lrat-check (exit 0, 'c VERIFIED').

Symmetry (proof in ../2026-11-11-rees-sde-p5-d3.md, small-set section): for a model (Phi, gamma) and
A in GL_3(F_5) with rows a_1, a_2, a_3, Phi'(l)_j := y_{a_j}(l), gamma'_alpha := gamma_{A^T alpha} -
sum_j alpha_j gamma_{a_j} is a model with y'_alpha = y_{A^T alpha}; it keeps (R) and (N).  If L has no
S-functional every y_alpha is nonzero on L, so taking a_1 = an alpha of minimum support m gives a
model with |supp y_{e1}| = m and |supp y_alpha| >= m for all alpha.  Case m adds exactly that.
usage: [PROOF_CAP_GB=4.5] sbsat.py WORKDIR TIMEOUT M_LIST|lex3 < sets.txt   (M_LIST e.g. 1-10; lex3 = build3, one CNF)
"""
import sys, os, itertools, hashlib, subprocess, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat
CHK = labelsat.LRATCHECK
CAP = int(float(os.environ.get('PROOF_CAP_GB', '4.5')) * 2**30)   # kill the solver if its proof exceeds this

def build(L, m):
    nv, cl, info = labelsat.encode(L)
    p = info['p']; n = len(info['L']); reps = info['reps']
    nvar = [nv]
    def new():
        nvar[0] += 1; return nvar[0]
    Z = {}
    for ai in range(len(reps)):
        for li in range(n):
            z = new(); Z[ai, li] = z; A = info['A'][ai, li]; G = info['G'][ai, li]
            for u in range(p):   # z <-> y_alpha(l) = 0  (A, G each exactly one true)
                cl.append([-z, -A[u], G[(-u) % p]]); cl.append([z, -A[u], -G[(-u) % p]])
    e1 = reps.index((1, 0, 0))
    for ai in range(len(reps)):      # |supp y_alpha| >= m: any n-m+1 labels contain a nonzero
        for T in itertools.combinations(range(n), n - m + 1):
            cl.append([-Z[ai, li] for li in T])
    for T in itertools.combinations(range(n), m + 1):   # |supp y_e1| <= m
        cl.append([Z[e1, li] for li in T])
    return nvar[0], cl, info

def build3(L):
    """Three-level support order (one CNF): t-th count bits c_j[t] for y_{e_j} (j = 1,2,3) with
    (y_{e_j} nonzero on some t labels) -> c_j[t], and c_j[t] -> |supp y_alpha| >= t for every rep alpha
    outside <e_1..e_{j-1}>.  Valid by choosing a_1 = argmin |supp y_alpha| over alpha != 0,
    a_2 = argmin over alpha outside <a_1>, a_3 = argmin over alpha outside <a_1,a_2>."""
    nv, cl, info = labelsat.encode(L)
    p = info['p']; n = len(info['L']); reps = info['reps']
    nvar = [nv]
    def new():
        nvar[0] += 1; return nvar[0]
    Z = {}
    for ai in range(len(reps)):
        for li in range(n):
            z = new(); Z[ai, li] = z; A = info['A'][ai, li]; G = info['G'][ai, li]
            for u in range(p):
                cl.append([-z, -A[u], G[(-u) % p]]); cl.append([z, -A[u], -G[(-u) % p]])
    E = [reps.index(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    span = [lambda a: False, lambda a: a[1] == 0 and a[2] == 0, lambda a: a[2] == 0]
    for j in range(3):
        c = {t: new() for t in range(1, n + 1)}
        for t in range(1, n + 1):
            for T in itertools.combinations(range(n), t):     # nonzero on T -> c[t]
                cl.append([Z[E[j], li] for li in T] + [c[t]])
            for ai, a in enumerate(reps):
                if span[j](a): continue
                for U in itertools.combinations(range(n), n - t + 1):   # c[t] -> some nonzero in U
                    cl.append([-c[t]] + [-Z[ai, li] for li in U])
    return nvar[0], cl, info

def sfunc(L):
    return [g for g in itertools.product(range(5), repeat=3) if any(g) and all(sum(a * b for a, b in zip(g, l)) % 5 in (0, 1, 4) for l in L)]

if __name__ == '__main__':
    wd, timeout = sys.argv[1], int(sys.argv[2]); LEX3 = sys.argv[3] == 'lex3'
    a, b = (0, 0) if LEX3 else map(int, sys.argv[3].split('-'))
    print('# checker sha256', hashlib.sha256(open(CHK, 'rb').read()).hexdigest()); sys.stdout.flush()
    for i, line in enumerate(sys.stdin):
        L = [tuple(int(c) for c in w) for w in line.split('|')[0].split() if len(w) == 3 and w.isdigit()]
        if not L: continue
        assert not sfunc(L), 'has an S-functional (feasible)'
        assert labelsat.rank(L, 5, 3) == 3
        Ls = ' '.join('%d%d%d' % l for l in L); allok = True; ttot = 0
        for m in (range(a, b + 1) if not LEX3 else [0]):
            nv, cl, info = build(L, m) if not LEX3 else build3(L); tag = 'sb%d_%d_m%d' % (os.getpid(), i, m)
            cnf = os.path.join(wd, tag + '.cnf'); prf = os.path.join(wd, tag + '.lrat'); labelsat.write_cnf(cnf, nv, cl)
            h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()[:16]; t0 = time.time()
            pr = subprocess.Popen(['cadical', '-q', '--lrat=true', '--binary=false', cnf, prf], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            st = None
            while pr.poll() is None:          # watchdog: wall-clock timeout and proof-size cap
                time.sleep(2)
                if time.time() - t0 > timeout: st = 'TIMEOUT'
                elif os.path.exists(prf) and os.path.getsize(prf) > CAP: st = 'PROOF_CAP'
                if st: pr.kill(); pr.wait(); break
            if st is None:
                out = pr.stdout.read()
                st = 'UNSAT' if 's UNSATISFIABLE' in out else ('SAT' if 's SATISFIABLE' in out else 'ERR')
            t1 = time.time(); ver = '-'; pb = os.path.getsize(prf) if os.path.exists(prf) else 0
            if st == 'UNSAT':
                c = subprocess.run([CHK, cnf, prf], capture_output=True, text=True)
                ver = 'exit %d %s' % (c.returncode, 'VERIFIED' if 'c VERIFIED' in c.stdout and 'NOT' not in c.stdout else 'NOT-VERIFIED')
                if not (c.returncode == 0 and ver.endswith(' VERIFIED')): allok = False
            else:
                allok = False
            for f in (cnf, prf):
                if os.path.exists(f): os.remove(f)
            ttot += time.time() - t0
            print('  %s m=%d %s cnf %s vars %d clauses %d proof %d solve %.1fs check %s' % (Ls, m, st, h, nv, len(cl), pb, t1 - t0, ver)); sys.stdout.flush()
            if st in ('SAT', 'ERR'): break
        print('%s | %s | %.1fs' % ('INFEASIBLE_CERTIFIED' if allok else 'NOT_CERTIFIED', Ls, ttot)); sys.stdout.flush()
