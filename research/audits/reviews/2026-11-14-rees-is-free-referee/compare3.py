"""Compare per-(p,kappa) IS-free degrees: this referee's indep_isfree.py vs the two dumps in
2026-11-14-rees-is-free/ (isfree_check.py and ref20_copy/dump_noS1.py). Read-only on those files."""
import json, os, collections
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(os.path.dirname(H), '2026-11-14-rees-is-free')
a = json.load(open(os.path.join(H, 'degs_indep_2000000.json')))
b = json.load(open(os.path.join(B, 'degs_isfree_2000000.json')))
c = json.load(open(os.path.join(B, 'ref20_copy', 'degs_ref20_noS1_2000000.json')))
for nm, o in [('isfree_check', b), ('ref20 dump_noS1', c)]:
    print(nm, 'keys equal:', set(a) == set(o), len(a), len(o), 'disagreements:', [(k, a[k], o.get(k)) for k in a if a[k] != o.get(k)][:20])
mx = collections.defaultdict(int)
for k, v in a.items():
    kk = int(k.split(',')[1]); mx[kk] = max(mx[kk], v)
print('max e per kappa (indep):', dict(sorted(mx.items())))
print('pairs with e > kappa (indep):', [(k, v) for k, v in a.items() if v > int(k.split(',')[1])])
hist = collections.Counter((int(k.split(',')[1]), v) for k, v in a.items())
print('histogram (kappa, e): count', dict(sorted(hist.items())))
