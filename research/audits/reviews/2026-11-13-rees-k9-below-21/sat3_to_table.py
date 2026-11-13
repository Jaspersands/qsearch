#!/opt/anaconda3/bin/python
"""Decode a sat3.py / sat3_stream.py model (layout: variables 1.. for t = 1,2,3; a, b in Z_k; value 0..p-1) into the
full 3-level table B(i,j,l) = F1(j,l) + F2(i,l) + F3(i,j) and write it as JSON (keys 'ijl').
usage: sat3_to_table.py p k model.txt out.json"""
import sys, json, itertools
p, k = int(sys.argv[1]), int(sys.argv[2])
true = set()
for line in open(sys.argv[3]):
    if line.startswith('v'):
        true |= {int(x) for x in line.split()[1:] if int(x) > 0}
F, v = {}, 0
for t in (1, 2, 3):
    for a in range(k):
        for b in range(k):
            vals = [u for u in range(p) if v + 1 + u in true]; v += p
            assert len(vals) == 1, (t, a, b, vals)
            F[(t, a, b)] = vals[0]
B = {'%d%d%d' % (i, j, l): (F[(1, j, l)] + F[(2, i, l)] + F[(3, i, j)]) % p for i, j, l in itertools.product(range(k), repeat=3)}
json.dump(B, open(sys.argv[4], 'w'))
print('wrote', sys.argv[4])
