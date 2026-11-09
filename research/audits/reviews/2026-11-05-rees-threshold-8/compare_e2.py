"""Compare clique.py verdicts with the dfs2/dfs2b verdicts (INFEASIBLE = member of E_2)."""
import re, glob, sys
k = int(sys.argv[1])
base = '2026-11-02-rees-schedules/small-prime/'
inf, fea = set(), set()
for f in glob.glob(base + f'*_k{k}*.out'):
    for line in open(f):
        m = re.match(r'(INFEASIBLE|FEASIBLE) k=(\d+) p=(\d+)', line)
        if m and int(m.group(2)) == k:
            (inf if m.group(1) == 'INFEASIBLE' else fea).add(int(m.group(3)))
cl, nocl, skip = set(), set(), set()
for line in open(f'2026-11-05-rees-threshold-8/clique_k{k}.out'):
    m = re.match(r'(CLIQUE|NOCLIQUE|SKIP) k=\d+ p=(\d+)', line)
    if m:
        {'CLIQUE': cl, 'NOCLIQUE': nocl, 'SKIP': skip}[m.group(1)].add(int(m.group(2)))
    if 'ERROR' in line: print('VERIFY ERROR', line)
print(f'k={k}: dfs INFEASIBLE {len(inf)}, FEASIBLE {len(fea)}; clique: CLIQUE {len(cl)}, NOCLIQUE {len(nocl)}, SKIP {len(skip)}; max scanned', max(cl|nocl|skip))
print(' contradictions (INFEASIBLE but CLIQUE):', sorted(inf & cl))
print(' in both FEASIBLE and INFEASIBLE in dfs data:', sorted(inf & fea))
print(' FEASIBLE with clique:', len(fea & cl), ' FEASIBLE without clique:', sorted(fea & nocl), ' FEASIBLE skipped (h odd):', len(fea & skip))
und = sorted(cl - inf - fea)
print(' clique-certified primes not decided by dfs data (<=20000):', [q for q in und if q <= 20000])
print(' largest NOCLIQUE:', sorted(nocl)[-8:])
