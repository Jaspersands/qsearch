"""Count Mobius maps preserving the projective point set {inf} u Y for clique witnesses
(Y = y_1..y_{k-1} from clique_k*.out). Observation only [computed]."""
import re, sys, itertools
from probe_mobius import run, INF
k = int(sys.argv[1]); lim = int(sys.argv[2])
rows = []
for l in open(f'clique_k{k}.out'):
    m = re.match(r'CLIQUE k=\d+ p=(\d+) .* y=([\d,]+) ', l)
    if m: rows.append((int(m.group(1)), [int(x) for x in m.group(2).split(',')]))
from collections import Counter
cnt = Counter()
for p, Y in rows[:lim]:
    pts = [INF] + Y
    n = len(run(p, pts)) + 1
    cnt[n] += 1
    print(p, 'stabiliser order', n, flush=True)
print('distribution of stabiliser orders:', dict(cnt))
