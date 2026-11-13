"""Check Lemma W (structure of the level-2 weight variety) against the referee's numerically built K, E.
(AI-written, pending human review.)  Claim: rowspace(K) = rowspace(Lam3), rowspace(E) = rowspace(Lam2), where
Lam_k is the 2x6 matrix whose column j is lam^(k)_j = sum_i s_ji^k lam_ji (s normalised as in the referee code,
s = (s1, s2, 1) with s1 l1 + s2 l2 + l3 = 0).  Input: the referee's curve_<p>.json files."""
import json, sys, numpy as np
REF = '../2026-11-13-rees-free23-triples-referee/'

def rank(M, p):
    M = [list(map(int, r)) for r in M]; r = 0; rows, cols = len(M), len(M[0])
    for c in range(cols):
        q = next((i for i in range(r, rows) if M[i][c] % p), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; iv = pow(M[r][c], -1, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        r += 1
    return r

def det2(a, b): return a[0] * b[1] - a[1] * b[0]

tot = bad = 0
for p in (101, 227, 503, 10007, 30011):
    D = json.load(open(REF + 'curve_%d.json' % p))
    for c in D['configs']:
        L2, L3 = [], []
        for (l1, l2, l3) in c['labels']:
            Dd = det2(l1, l2) % p; iv = pow(Dd, -1, p)
            s = [(-det2(l3, l2) * iv) % p, (-det2(l1, l3) * iv) % p, 1]
            assert all((s[0] * l1[k] + s[1] * l2[k] + l3[k]) % p == 0 for k in range(2))
            ls = (l1, l2, l3)
            L2.append([sum(s[i] ** 2 * ls[i][k] for i in range(3)) % p for k in range(2)])
            L3.append([sum(s[i] ** 3 * ls[i][k] for i in range(3)) % p for k in range(2)])
        L2 = np.array(L2).T.tolist(); L3 = np.array(L3).T.tolist()
        K, E = c['K'], c['E']
        okK = rank(K, p) == 2 and rank(L3, p) == 2 and rank(K + L3, p) == 2
        okE = rank(E, p) == 2 and rank(L2, p) == 2 and rank(E + L2, p) == 2
        tot += 1; bad += int(not (okK and okE))
        print('p=%d: rowspace(K)=rowspace(Lam3): %s   rowspace(E)=rowspace(Lam2): %s' % (p, okK, okE))
print('TOTAL configs %d, mismatches %d' % (tot, bad))
