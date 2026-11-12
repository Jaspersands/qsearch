"""Group the rows of a 'table' output of hpgp2_free23.py by label class; print min/max of each column.
usage: python summarize.py table_5_all.out"""
import sys, re, collections
rows = collections.defaultdict(list)
pat = re.compile(r'lam1=\((\d+), (\d+)\) lam2=\((\d+), (\d+)\) (.*?)\s+\| HYP1 chi=(\S+) S=(\S+) \| HYP2 chi=(\S+) S=(\S+) \| known: (\S+) (\S+) \| tr_err=(\S+) off=(\S+)')
for line in open(sys.argv[1]):
    m = pat.search(line)
    if not m: continue
    g = m.groups(); cls = re.sub(r'c=\d+ \(=-1.*', 'c=-1 (binary zero-sum)', g[4].strip())
    cls = re.sub(r'^c=\d+$', 'c not in {0,-1}', cls)
    rows[cls].append([float(x) for x in g[5:]])
print('%-26s %5s | %-17s | %-17s | %-17s | %-17s | %-15s | %-15s | max tr_err, off' % ('class', '#', 'HYP1 chi', 'HYP1 meanS', 'HYP2 chi', 'HYP2 meanS', 'known HYP1 chi', 'known HYP2 chi'))
for cls, v in sorted(rows.items()):
    cols = list(zip(*v))
    rng = lambda c: '%.4f..%.4f' % (min(c), max(c))
    print('%-26s %5d | %-17s | %-17s | %-17s | %-17s | %-15s | %-15s | %.0e %.0e' % (cls, len(v), rng(cols[0]), rng(cols[1]), rng(cols[2]), rng(cols[3]),
          rng(cols[4]), rng(cols[5]), max(cols[6]), max(cols[7])))
