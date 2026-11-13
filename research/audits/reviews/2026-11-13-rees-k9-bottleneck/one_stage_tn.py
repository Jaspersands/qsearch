#!/opt/anaconda3/bin/python
"""After one {0,m}-stage the type is (1, eps), eps = -g^{-m}; Tn = {y1 + eps*y2 : (y1,y2) in (P u 0)^2 \\ 0}.
Prints |Tn \\ 0|, whether 0 in Tn (F0), whether Tn \\ 0 = F_p^* (F1), and the class set of Tn (exact).
Also two stages (types (1,e1,e2,e1e2)).  Usage: one_stage_tn.py p kappa"""
import sys, itertools
p, k = int(sys.argv[1]), int(sys.argv[2])
fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))]
g = next(g for g in range(2, p) if all(pow(g, (p - 1) // f, p) != 1 for f in fs))
L = {pow(g, e, p): e for e in range(p - 1)}
P = [x for x in range(1, p) if L[x] % k == 0]
D = [0] + P
print(f'p={p} kappa={k} g={g} |P|={len(P)} -1 in P: {L[p-1] % k == 0}')
for m in range(1, k):
    eps = (-pow(pow(g, m, p), p - 2, p)) % p
    Tn = {(y1 + eps * y2) % p for y1 in D for y2 in D if y1 or y2}
    C = sorted({L[x] % k for x in Tn if x})
    print(f'  m={m}: |Tn\\0|={len(Tn - {0})} F0={0 in Tn} F1={len(Tn - {0}) == p - 1} classes={C}')
