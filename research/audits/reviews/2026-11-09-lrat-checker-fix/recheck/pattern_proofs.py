"""Re-check the four CaDiCaL LRAT proofs of pattern_sat_k4.py (2026-11-08-rees-sde-p3-nest) with
the fixed lrat-check. The proofs survive only in the temp folders that pattern_sat.cadical_solve
left behind (audit 9 Nov, Open Directions 2). Each leftover p.cnf is tied to its instance by
regenerating the four CNFs from pattern_sat.py (same calls and order as pattern_sat_k4.py) and
comparing sha256. Writes nothing except stdout.
usage: python -I pattern_proofs.py TMPDIR_WITH_THE_FOUR_FOLDERS > pattern_proofs.out
"""
import glob
import hashlib
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-08-rees-sde-p3-nest')))
import pattern_sat as ps                    # noqa: E402
from pattern_sat import feasible, nz        # noqa: E402

CHECK = os.path.normpath(os.path.join(HERE, '..', 'lrat-check'))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 24), b''):
            h.update(block)
    return h.hexdigest()


want = {}


def regen(label, d, k, T):
    def dump(nvars, cl):
        s = f'p cnf {nvars} {len(cl)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cl)
        want[hashlib.sha256(s.encode()).hexdigest()] = (label, nvars, len(cl))
        return 'UNSAT'
    ps.cadical_solve = dump
    feasible(d, k, T, solver='cadical')


regen('k=4, all 80 patterns', 3, 4, nz(4))
regen('k=4, delta_1 full support (54 patterns)', 3, 4, [p for p in nz(4) if p[0] != 0])
regen('k=4, delta_1, delta_2 full support (36 patterns)', 3, 4, [p for p in nz(4) if p[0] != 0 and p[1] != 0])
regen('k=3, delta_1, delta_2 full support (12 patterns)', 3, 3, [p for p in nz(3) if p[0] != 0 and p[1] != 0])
print(f'checker {CHECK} sha256 {sha_file(CHECK)[:16]}', flush=True)
found = set()
verdicts = []
for cnf in sorted(glob.glob(os.path.join(sys.argv[1], 'tmp*', 'p.cnf'))):
    h = sha_file(cnf)
    if h not in want:
        continue
    label, nv, nc = want[h]
    found.add(h)
    prf = os.path.join(os.path.dirname(cnf), 'p.lrat')
    t = time.time()
    r = subprocess.run(['nice', '-n', '19', CHECK, cnf, prf], capture_output=True, text=True)
    dt = time.time() - t
    ok = r.returncode == 0 and 'c VERIFIED' in r.stdout.splitlines()
    verdicts.append(ok)
    stats = [l for l in r.stdout.splitlines() if l.startswith('c Added') or l.startswith('c verification')]
    print(f'{label}: folder {os.path.basename(os.path.dirname(cnf))}, cnf sha256 {h[:16]} ({nv} vars, '
          f'{nc} clauses), proof {os.path.getsize(prf)} bytes sha256 {sha_file(prf)[:16]}: '
          f'{"VERIFIED" if ok else "NOT VERIFIED"} (exit {r.returncode}, {dt:.0f} s wall); {"; ".join(stats)}',
          flush=True)
missing = [v[0] for h, v in want.items() if h not in found]
print('ALL FOUR VERIFIED' if not missing and len(verdicts) == 4 and all(verdicts)
      else f'NOT ALL VERIFIED: missing {missing}, verdicts {verdicts}', flush=True)
