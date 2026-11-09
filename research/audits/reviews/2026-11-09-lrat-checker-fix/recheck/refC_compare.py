"""Compare referee C's original LRAT runs with the reruns under the fixed lrat-check.

Originals: ../../2026-11-09-rees-sde-fq-nest-referee-C/<name>.out (checked by the unsound upstream build).
Reruns:    refC/<name>.out (refC_rerun.sh, same commands, fixed build ../lrat-check).
A pair of lines matches when they agree after deleting wall-clock times ("0.7s", "[9.5s]") and the
'check_s' field; verdicts, vars/clauses counts, fixes, cnf_sha256 and proof_bytes must be equal.
Prints one line per file and a total; exits 1 on any mismatch.
usage: python refC_compare.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-09-rees-sde-fq-nest-referee-C'))
NEW = os.path.join(HERE, 'refC')
NAMES = ['free_p7_k2', 'free_p7_k2_noR', 'free_p7_k3kappa', 'free_interval', 'rerun_k3_7']


def norm(line):
    line = re.sub(r"'check_s': [0-9.]+, ", '', line)
    line = re.sub(r'\[[0-9.]+s\]', '[Ts]', line)
    line = re.sub(r' [0-9.]+s( |\])', r' Ts\1', line)
    return line.rstrip('\n')


def main():
    bad = 0
    tot = {'lines': 0, 'unsat_verified': 0, 'sat': 0}
    for name in NAMES:
        a = open(os.path.join(ORIG, name + '.out'), encoding='utf-8').read().splitlines()
        b = open(os.path.join(NEW, name + '.out'), encoding='utf-8').read().splitlines()
        mism = [i for i in range(max(len(a), len(b)))
                if i >= len(a) or i >= len(b) or norm(a[i]) != norm(b[i])]
        uv = sum(1 for x in b if ': UNSAT' in x and 'LRAT VERIFIED' in x)
        sat = sum(1 for x in b if ': SAT' in x)
        other = len(b) - uv - sat
        tot['lines'] += len(b)
        tot['unsat_verified'] += uv
        tot['sat'] += sat
        print(f'{name}: orig {len(a)} lines, rerun {len(b)} lines; rerun UNSAT+LRAT VERIFIED {uv}, '
              f'SAT {sat}, other {other}; mismatched lines {len(mism)}')
        for i in mism[:5]:
            print('  orig :', a[i] if i < len(a) else '<missing>')
            print('  rerun:', b[i] if i < len(b) else '<missing>')
        bad += len(mism) + other
    print(f"TOTAL: {tot['lines']} runs, {tot['unsat_verified']} UNSAT with LRAT VERIFIED by the fixed "
          f"checker, {tot['sat']} SAT; {'ALL MATCH' if bad == 0 else 'MISMATCHES: %d' % bad}")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
