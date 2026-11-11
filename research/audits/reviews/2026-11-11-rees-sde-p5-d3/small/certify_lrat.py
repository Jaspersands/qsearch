#!/usr/bin/env python3
"""LRAT certification of infeasible label sets with labelsat.solve (CaDiCaL --lrat=true --binary=false,
checked by the FIXED lrat-check of 2026-11-09-lrat-checker-fix; labelsat's LRATCHECK default).
usage: certify_lrat.py WORKDIR TIMEOUT < sets.txt   (one label set per line, digit triples)
Prints one line per set: status, CNF sha256, vars, clauses, proof bytes, seconds, checker tail.
Proofs and CNFs are deleted after checking."""
import sys, os, hashlib, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat
wd, timeout = sys.argv[1], int(sys.argv[2])
chk = labelsat.LRATCHECK
print('# checker %s sha256 %s' % (os.path.normpath(chk), hashlib.sha256(open(chk, 'rb').read()).hexdigest()))
for i, line in enumerate(sys.stdin):
    L = [tuple(int(c) for c in w) for w in line.split('|')[0].split() if len(w) == 3 and w.isdigit()]
    if not L: continue
    tag = 'c%d_%d' % (os.getpid(), i)
    res = labelsat.solve(L, timeout=timeout, workdir=wd, keep=True, tag=tag)
    cnf, lrat = os.path.join(wd, tag + '.cnf'), os.path.join(wd, tag + '.lrat')
    h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest() if os.path.exists(cnf) else '-'
    pb = os.path.getsize(lrat) if os.path.exists(lrat) else 0
    ex = '-'
    if res['status'] == 'UNSAT_VERIFIED':   # re-run the fixed checker to record its exit code too
        r = subprocess.run([chk, cnf, lrat], capture_output=True, text=True)
        ex = '%d%s' % (r.returncode, ' VERIFIED' if 'c VERIFIED' in r.stdout else ' no-VERIFIED-line')
    for f in (cnf, lrat):
        if os.path.exists(f): os.remove(f)
    tail = res.get('lrat_out', '').strip().replace('\n', ' / ')
    print('%s | %s | cnf %s vars %d clauses %d proof_bytes %d time %.1f | recheck exit %s | %s' % (
        res['status'], ' '.join('%d%d%d' % l for l in res['L']), h[:16], res['nvars'], res['nclauses'], pb, res['time'], ex, tail))
    sys.stdout.flush()
