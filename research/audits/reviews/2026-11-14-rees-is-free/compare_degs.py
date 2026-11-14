"""Compare per-(p,kappa) IS-free degrees of two independently written programs (p < 2e6):
isfree_check.py (on plus_mine.py helpers, core-plus referee) and ref20_copy/dump_noS1.py
(plus2.py, 20-referee).  Also list the pairs with e° > kappa (where Lemma plus-free-const alone
does not give dominance over candidate (a))."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(H, 'degs_isfree_2000000.json')))
b = json.load(open(os.path.join(H, 'ref20_copy', 'degs_ref20_noS1_2000000.json')))
print('pairs:', len(a), len(b), 'same key set:', set(a) == set(b))
diff = [(k, a[k], b.get(k)) for k in a if a[k] != b.get(k)]
print('degree disagreements:', len(diff), diff[:20])
for name, d in (('isfree_check', a), ('ref20', b)):
    big = sorted((tuple(map(int, k.split(','))), v) for k, v in d.items() if v > int(k.split(',')[1]))
    print(name, 'pairs with e° > kappa:', big)
mx = {}
for k, v in a.items():
    kk = int(k.split(',')[1]); mx[kk] = max(mx.get(kk, 0), v)
print('max e° per kappa:', dict(sorted(mx.items())))
