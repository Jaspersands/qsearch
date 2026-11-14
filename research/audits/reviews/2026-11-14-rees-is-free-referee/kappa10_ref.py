"""Referee check of the optional Remark rem:plus-free-ten (kappa = 10), from the text of
Definition plus-schedule: at kappa = 10 the candidates are (a) and the plans over H_5 (node (f1),
m = 5) with finishes F0 or F1; eps = -q^{-1}, q^h = -1 (q = g^5, g the least primitive root).
For p < 4*10^4 admissibility is by class sumsets; for p >= 4*10^4 only (1, F1).
Uses indep_isfree.solve_prime for H_5 (IS-free, kappa <= 9). Usage: python kappa10_ref.py N"""
import sys, math, collections
import indep_isfree as I
N = int(sys.argv[1])
certs = I.load_certs()
ellok = {pk: I.check_ell(pk[0], pk[1], fn) for pk, fn in I.ELL.items()}
nod, nodomk, hist, worst = [], [], collections.Counter(), None
cnt = 0
for p in I.primes_below(N):
    if (p - 1) % 10: continue
    cnt += 1
    rows, _ = I.solve_prime(p, certs.get(p), ellok)
    e5, K5 = rows[5]['e'], rows[5]['K']
    k = 10; h = (p - 1) // k
    P = I.Prime(p, None)
    cands = []
    if p < 4 * k ** 4:
        Ck, Zk = P.setup_small(k)
        t = I.t_value(p, k, Ck, Zk)
        q = pow(P.g, 5, p); assert pow(q, h, p) == p - 1
        eps = (-pow(q, p - 2, p)) % p
        T = I.tsets(k, Ck, Zk, P.C.cl(eps, k), k + 1)
        for s in range(1, k + 2):
            S, z = T[s]
            if z: cands.append((s * e5, K5 ** s, 's%d F0' % s))
            if len(S) == k: cands.append((s * e5 + 1, K5 ** s, 's%d F1' % s))
    else:
        t = 2 if h % 2 == 0 else 3
        cands.append((e5 + 1, K5, 's1 F1'))
    L = math.ceil(math.log2(t))
    if not cands: nod.append(p); continue
    e = min(c[0] for c in cands)
    dom = [c for c in cands if c[0] <= k * L and c[1] < k ** (45 * L)]
    if not dom: nodomk.append((p, e, L))
    hist[e] += 1
    if worst is None or e > worst[1]: worst = (p, e, t, L, min(cands))
print('primes p < %d with 10 | p-1: %d' % (N, cnt))
print('no IS-free candidate at kappa=10:', nod)
print('no dominating candidate:', nodomk)
print('IS-free degree histogram at kappa=10:', dict(sorted(hist.items())))
print('max degree (p, e, t, L, cand):', worst)
