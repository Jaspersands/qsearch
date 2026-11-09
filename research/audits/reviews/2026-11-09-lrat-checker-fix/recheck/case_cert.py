"""Re-certify a Lemma U case split with the fixed lrat-check, one CNF per case (no gamma_(1,1) split).

For every case string c of CASEFILE (gadget_cnf5 encoding `p S k 2 nest --fix c`):
  1. write the case CNF (dump_gadget_cnf.py);
  2. tie-in: regenerate the CNF of the first recorded sub-case `c;1,1,0:...` of SPLITFILE; its sha256
     must equal the recorded cnf_sha256, and it must be the case CNF plus trailing unit clauses with
     the same variable count (so every sub-case of the split is the case CNF plus units);
  3. solve the case CNF with CaDiCaL (gadget_cnf5's flags, wall-clock cap --cap seconds);
  4. on UNSAT, check the LRAT proof with ../lrat-check (exit 0 and the line "c VERIFIED"), hash it and
     delete it.
A case counts as certified only if 2 and 4 both pass. Cases are run --jobs at a time; no new case is
started once the CPU of finished cases exceeds --budget seconds (the rest print SKIPPED).
usage: python -I case_cert.py p S k CASEFILE SPLITFILE --work DIR [--cap 600] [--jobs 2] [--budget 4000]
"""
import argparse
import ast
import hashlib
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.normpath(os.path.join(HERE, '..', 'lrat-check'))
CONTROLS = os.path.normpath(os.path.join(HERE, '..', 'controls.sh'))
DUMP = os.path.join(HERE, 'dump_gadget_cnf.py')
PY = sys.executable
LOCK = threading.Lock()
CPU = [0.0]


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 24), b''):
            h.update(block)
    return h.hexdigest()


def timed(cmd):
    """run cmd under nice 19 and /usr/bin/time -p; return (returncode, stdout, CPU seconds of cmd).
    (Per-command timing, so the two worker threads do not count each other's children.)"""
    r = subprocess.run(['/usr/bin/time', '-p', 'nice', '-n', '19'] + cmd, capture_output=True, text=True)
    cpu = 0.0
    for ln in r.stderr.splitlines():
        parts = ln.split()
        if len(parts) == 2 and parts[0] in ('user', 'sys'):
            try:
                cpu += float(parts[1])
            except ValueError:
                pass
    return r.returncode, r.stdout, cpu


def tie_in(case_cnf, sub_cnf, want):
    h = sha_file(sub_cnf)
    with open(case_cnf) as fa, open(sub_cnf) as fb:
        ha, hb = fa.readline().split(), fb.readline().split()
        same_vars = ha[2] == hb[2]
        prefix = True
        for la in fa:
            if fb.readline() != la:
                prefix = False
                break
        tail = fb.read().splitlines()
    units = all(len(t.split()) == 2 and t.split()[1] == '0' for t in tail)
    return h == want and prefix and units and same_vars, (h == want, prefix, len(tail), units, same_vars)


def run_case(i, case, sub, args):
    tag = f'c{i:02d}'
    case_cnf = os.path.join(args.work, tag + '.cnf')
    sub_cnf = os.path.join(args.work, tag + '.sub.cnf')
    prf = os.path.join(args.work, tag + '.lrat')
    with LOCK:
        if CPU[0] > args.budget:
            return f'{case}: SKIPPED (CPU budget {args.budget:.0f} s reached)', 'skipped'
    cpu = 0.0
    rc, out, c = timed([PY, '-I', DUMP, str(args.p), args.S, str(args.k), '2', 'nest', '--fix', case,
                        '--out', case_cnf])
    cpu += c
    m = re.search(r'sha256=(\w+) vars=(\d+) clauses=(\d+)', out)
    if rc != 0 or not m:
        return f'{case}: CNF dump failed: {out[-200:]}', 'fail'
    case_sha, nv, nc = m.group(1), m.group(2), m.group(3)
    subfix, subsha = sub
    rc, out, c = timed([PY, '-I', DUMP, str(args.p), args.S, str(args.k), '2', 'nest', '--fix', subfix,
                        '--out', sub_cnf])
    cpu += c
    ok_tie, detail = tie_in(case_cnf, sub_cnf, subsha)
    os.remove(sub_cnf)
    t0 = time.time()
    rc, out, c = timed(['cadical', '-q', '-t', str(args.cap), '--lrat=true', '--binary=false', case_cnf, prf])
    cpu += c
    solve_cpu, solve_wall = c, time.time() - t0
    res = {20: 'UNSAT', 10: 'SAT'}.get(rc, f'UNKNOWN(rc={rc})')
    line = (f'{case}: cnf {case_sha[:16]} ({nv} vars, {nc} clauses); tie-in {"OK" if ok_tie else "FAIL " + str(detail)} '
            f'[{subfix.split(";")[-1]}]; cadical {res} ({solve_cpu:.0f} s CPU, {solve_wall:.0f} s wall)')
    status = 'fail'
    if rc == 20:
        pb = os.path.getsize(prf)
        rc2, out2, c2 = timed([CHECK, case_cnf, prf])
        cpu += c2
        ver = rc2 == 0 and 'c VERIFIED' in out2.splitlines()
        psha = sha_file(prf)
        line += (f'; proof {pb} bytes sha256 {psha[:16]}; lrat-check {"VERIFIED" if ver else "NOT VERIFIED"} '
                 f'(exit {rc2}, {c2:.0f} s CPU)')
        if ver and ok_tie:
            status = 'certified'
    for f in (prf, case_cnf):
        if os.path.exists(f):
            os.remove(f)
    with LOCK:
        CPU[0] += cpu
    return line + f'; case CPU {cpu:.0f} s', status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int)
    ap.add_argument('casefile'); ap.add_argument('splitfile')
    ap.add_argument('--work', required=True); ap.add_argument('--cap', type=int, default=600)
    ap.add_argument('--jobs', type=int, default=2); ap.add_argument('--budget', type=float, default=4000)
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    r = subprocess.run([CONTROLS, CHECK, '-'], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    print(f'controls: {last}', flush=True)
    if r.returncode != 0:
        print('controls failed; stop'); return 1
    print(f'checker {CHECK} sha256 {sha_file(CHECK)[:16]}; cadical '
          f'{subprocess.run(["cadical", "--version"], capture_output=True, text=True).stdout.strip()}', flush=True)
    cases = [ln.strip() for ln in open(args.casefile) if ln.strip()]
    first_sub = {}
    for ln in open(args.splitfile):
        m = re.search(r'fix=(\S+): UNSAT \[[^\]]*\] (\{.*\})', ln)
        if not m:
            continue
        fix = m.group(1)
        c = fix.rsplit(';', 1)[0]
        if c not in first_sub:
            first_sub[c] = (fix, ast.literal_eval(m.group(2))['cnf_sha256'])
    assert all(c in first_sub for c in cases), 'a case has no recorded sub-case'
    print(f'{len(cases)} cases from {os.path.basename(args.casefile)}; tie-in sub-cases from '
          f'{os.path.basename(args.splitfile)}; cap {args.cap} s wall per case; CPU budget {args.budget:.0f} s',
          flush=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run_case, i, c, first_sub[c], args) for i, c in enumerate(cases)]
        results = []
        for f in futs:
            line, st = f.result()
            print(line, flush=True)
            results.append(st)
    n = len(cases)
    cert = results.count('certified')
    print(f'TOTAL: {cert}/{n} cases certified (tie-in OK, UNSAT, LRAT VERIFIED by the fixed checker); '
          f'{results.count("skipped")} skipped, {results.count("fail")} not certified; '
          f'CPU {CPU[0]:.0f} s', flush=True)
    return 0 if cert == n else 1


if __name__ == '__main__':
    sys.exit(main())
