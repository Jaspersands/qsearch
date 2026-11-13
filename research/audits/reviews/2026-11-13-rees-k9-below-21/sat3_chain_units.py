#!/opt/anaconda3/bin/python
"""Decompose a 3-level table B (JSON) into sat3.py's gauge F1(j,l)+F2(i,l)+F3(i,j) with F2(0,.)=F3(0,.)=F3(.,0)=0
and print unit clauses fixing the F-variables of the sat3.py / sat3_stream.py CNF (layout: t=1,2,3; a; b; value).
usage: sat3_chain_units.py p k table.json > units.txt"""
import sys, json, itertools
p, k = int(sys.argv[1]), int(sys.argv[2])
B = {tuple(int(c) for c in key): v for key, v in json.load(open(sys.argv[3])).items()}
F1 = {(j, l): B[(0, j, l)] for j in range(k) for l in range(k)}
R = {x: (B[x] - B[(0, x[1], x[2])]) % p for x in B}
F2 = {(i, l): R[(i, 0, l)] for i in range(k) for l in range(k)}
F3 = {(i, j): (R[(i, j, 0)] - R[(i, 0, 0)]) % p for i in range(k) for j in range(k)}
for i, j, l in itertools.product(range(k), repeat=3):
    assert (F1[(j, l)] + F2[(i, l)] + F3[(i, j)]) % p == B[(i, j, l)], 'not in the sat3 span'
assert all(F2[(0, l)] == 0 for l in range(k)) and all(F3[(0, j)] == 0 for j in range(k)) and all(F3[(i, 0)] == 0 for i in range(k))
v = 0
for t, Ft in ((1, F1), (2, F2), (3, F3)):
    for a in range(k):
        for b in range(k):
            print(v + Ft[(a, b)] + 1, 0)
            v += p
