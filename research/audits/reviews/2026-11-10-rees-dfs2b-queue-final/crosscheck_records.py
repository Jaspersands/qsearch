"""Cross-checks against records (AI-written 10 Nov 2026): (a) the 145-prime constraint-solver
verdicts of 2026-11-04-rees-cloud-e2k8low.md against the final kappa = 8 verdicts; (b) plain-mode
coverage of members in (7577, 10753] (kappa = 8) and (11593, 14149] (kappa = 9) by the local queue
and the late cloud file. Run from this folder after collect.py: python -I crosscheck_records.py"""
import re, json
s = open('../2026-11-04-rees-cloud-e2k8low.md').read()
v = {}
for m in re.finditer(r'\b(INFEASIBLE|FEASIBLE) k=8 p=(\d+)', s):
    v.setdefault(int(m.group(2)), set()).add(m.group(1))
d = json.load(open('E2_k8_le20000.json'))
fin = {p: 'INFEASIBLE' for p in d['members']}; fin.update({p: 'FEASIBLE' for p in d['nonmembers']})
sel = [p for p in v if 9769 < p <= 20000]
print('(a) e2k8low verdicts in (9769,20000]:', len(sel), 'conflicts:', [p for p in sel if v[p] != {fin[p]}],
      'members/non-members:', sum(fin[p] == 'INFEASIBLE' for p in sel), sum(fin[p] == 'FEASIBLE' for p in sel))
q = [l.split() for l in open('../2026-11-07-rees-dfs2b-local-queue/queue.txt')]
late = [l.split() for l in open('../2026-11-07-rees-cloud-late-results.txt') if l[:2] in ('D ', 'E ')]
for k, lo, hi in ((8, 7577, 10753), (9, 11593, 14149)):
    m = json.load(open(f'E2_k{k}_le20000.json'))['members']
    seg = [p for p in m if lo < p <= hi]
    pq = {int(x[1]) for x in q if int(x[0]) == k and x[2] == 'plain'}
    pl = {int(x[3].split('=')[1]) for x in late if int(x[2].split('=')[1]) == k}
    print(f'(b) kappa={k}: members <= {lo}: {len([p for p in m if p <= lo])}; members <= {hi}: {len([p for p in m if p <= hi])};'
          f' members in ({lo},{hi}]: {len(seg)}, plain-checked locally {len(set(seg) & pq)}, in late cloud file {len(set(seg) & pl)},'
          f' missing {sorted(set(seg) - pq - pl)}')
