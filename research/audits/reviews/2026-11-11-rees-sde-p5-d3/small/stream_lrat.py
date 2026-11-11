#!/usr/bin/env python3
"""Streamed LRAT certification of infeasibility of one label set (proof never written to disk).
MODE plain: the CNF of labelsat.encode(L) (exactly the CNF labelsat.solve writes; (R), (N)).
MODE lex3 : sbsat.build3(L) = that CNF + the three-level support order (proof of validity in the note;
            soundness control sb_sanity.py).
CaDiCaL --lrat=true --binary=false writes the proof into a named pipe; a reader thread hashes it and
feeds it to the FIXED lrat-check (2026-11-09-lrat-checker-fix/lrat-check CNF, proof on stdin).
Certified iff CaDiCaL prints s UNSATISFIABLE, lrat-check exits 0 and prints 'c VERIFIED'.
MODE msfinal:M0: the final case of msplit.py; msfinalR:M0 adds msplit.minrep_supp.
usage: stream_lrat.py MODE TIMEOUT WORKDIR < oneset.txt"""
import sys, os, hashlib, subprocess, threading, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat, sbsat
CHK = os.path.normpath(labelsat.LRATCHECK)
mode, timeout, wd = sys.argv[1], int(sys.argv[2]), sys.argv[3]
L = sorted(set(tuple(int(c) for c in w) for w in sys.stdin.read().split('|')[0].split() if len(w) == 3 and w.isdigit()))
assert labelsat.rank(L, 5, 3) == 3
assert not [g for g in itertools.product(range(5), repeat=3) if any(g) and all(sum(a * b for a, b in zip(g, l)) % 5 in (0, 1, 4) for l in L)]
if mode == 'plain': nv, cl, info = labelsat.encode(L)
elif mode == 'lex3': nv, cl, info = sbsat.build3(L)
elif mode.startswith('msfinal'):     # final case of msplit.py: base + |supp y_alpha| >= M0 for all alpha
    import msplit
    M0 = int(mode.split(':')[1]); nv, cl, info, Z = msplit.base(L); cl = cl + msplit.minsupp(info, Z, M0, len(L))
    if mode.startswith('msfinalR'): cl = cl + msplit.minrep_supp(info, M0, len(L))   # min-support representatives
else: raise SystemExit('unknown mode')
tag = '%s_%d' % (mode.replace(':', ''), os.getpid()); cnf = os.path.join(wd, tag + '.cnf'); fifo = os.path.join(wd, tag + '.fifo')
labelsat.write_cnf(cnf, nv, cl); hc = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
os.mkfifo(fifo)
print('# %s | %s | cnf sha256 %s vars %d clauses %d | checker %s sha256 %s' % (mode, ' '.join('%d%d%d' % l for l in L), hc, nv, len(cl),
      CHK, hashlib.sha256(open(CHK, 'rb').read()).hexdigest())); sys.stdout.flush()
t0 = time.time()
solout = open(os.path.join(wd, tag + '.out'), 'w+')   # file, not a pipe: SAT models are long
sol = subprocess.Popen(['cadical', '-q', '--lrat=true', '--binary=false', cnf, fifo], stdout=solout, stderr=subprocess.DEVNULL)
chk = subprocess.Popen([CHK, cnf], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
h = hashlib.sha256(); nbytes = [0]
def pump():
    with open(fifo, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 22), b''):
            h.update(blk); nbytes[0] += len(blk)
            try: chk.stdin.write(blk)
            except BrokenPipeError: pass
    try: chk.stdin.close()
    except BrokenPipeError: pass
th = threading.Thread(target=pump, daemon=True); th.start()
st = None
while sol.poll() is None:
    time.sleep(1)
    if time.time() - t0 > timeout:
        st = 'TIMEOUT'; sol.kill(); break
sol.wait(); solout.seek(0); out = solout.read(); solout.close(); os.remove(os.path.join(wd, tag + '.out'))
th.join(timeout=60)
if st is None: st = 'UNSAT' if 's UNSATISFIABLE' in out else ('SAT' if 's SATISFIABLE' in out else 'ERR')
t1 = time.time()
if st != 'UNSAT':
    chk.kill()
cout = chk.stdout.read().decode(errors='replace'); chk.wait()
ok = st == 'UNSAT' and chk.returncode == 0 and 'c VERIFIED' in cout and 'NOT VERIFIED' not in cout
os.remove(fifo); os.remove(cnf)
print('%s | %s | solver %s %.0fs | proof %d bytes sha256 %s | lrat-check exit %s: %s | total %.0fs' % (
    'INFEASIBLE_CERTIFIED' if ok else 'NOT_CERTIFIED', ' '.join('%d%d%d' % l for l in L), st, t1 - t0, nbytes[0], h.hexdigest(),
    chk.returncode, ' / '.join(x for x in cout.splitlines() if 'VERIFIED' in x or 'fail' in x.lower())[-200:], time.time() - t0))
