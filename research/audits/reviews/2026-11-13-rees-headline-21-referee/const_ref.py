"""Referee: constants K+_kappa (least constant among degree-optimal candidates, thm:halving(iii) style:
A(a) <= K (a+1)^e) for Schedule 1H+, and comparison with c_kappa = kappa^{kappa(kappa-1)ceil(log2(kappa+1))/2}
of thm:main(4).  Chain constant: K_0 * prod(|R_t|-1); plan (s, F_K): K_T^s * K_F."""
import math, sys
import rule_ref as R
from paths_ref import chains_paths, path
def cK(k): return k ** (k * (k - 1) * math.ceil(math.log2(k + 1)) // 2)
def best(c): return min(c)          # (deg, const, name)
def degrees_c(p):
    cyc = R.Cyc(p) if p < R.SMALL else None
    e = {}
    for kap in range(1, 10):
        if (p - 1) % kap: continue
        if kap == 1: e[1] = (1, 1, 'GE'); continue
        t = R.t_len(cyc, kap) if p < R.SMALL else (2 if ((p - 1) // kap) % 2 == 0 else 3)
        L = math.ceil(math.log2(t))
        cands = [(kap * L, kap ** (kap * (kap - 1) * L // 2), 'S1')]
        two, kn = [], [(frozenset(range(kap)), 1, 1)]
        if kap % 2 == 0: two.append((kap // 2, e[kap // 2][0], e[kap // 2][1]))
        for Dp in range(2, kap):
            if kap % Dp == 0: kn.append((frozenset(range(0, kap, Dp)), e[Dp][0], e[Dp][1]))
        if kap in (3, 4, 5) and R.avail(f'TL{kap}', p): cands.append((2, kap - 1, 'TL'))
        if kap == 9 and R.avail('TW9', p): cands.append((e[3][0] + 1, e[3][1] * 2, 'TW'))
        if kap == 7:
            a = R.avail('U7', p)
            if a is True: two.append((1, 2, 6))
            elif a: two.append(([x for x in a if x][0], 2, 6))
        if p in R.TB_PRIMES and kap >= 4:
            ee = {k: v[0] for k, v in e.items()}
            b = chains_paths(p, kap, ee)
            for node, (dg, _) in b.items():
                if node[0] != kap: continue
                pth = path(b, node); const = 1
                for st in pth:
                    if st[0] == 'GE': const = 1
                    elif st[0] == 'solver': const = e[st[1]][1]
                    else: const *= len(st[1]) - 1
                K = node[1]
                if K == frozenset([0]): cands.append((dg, const, 'chain0'))
                if len(K) == 2: two.append((max(K), dg, const))
                kn.append((K, dg, const))
        for m, em, cm in two:
            if p >= 4 * kap ** 4: cands.append((em + 1, cm, 'plan')); continue
            epscl = ((p - 1) // 2 - m) % kap
            for s, T in enumerate(R.T_list(cyc, kap, epscl), start=1):
                if T[1]: cands.append((s * em, cm ** s, 'F0'))
                for K, dk, ck in kn:
                    if any(all((u + k) % kap in T[0] for k in K) for u in range(kap)):
                        cands.append((s * em + dk, cm ** s * ck, 'FK'))
        e[kap] = best(cands)
    return e
worst = {}
for p in R.sieve(int(sys.argv[1])):
    if p < 3: continue
    e = degrees_c(p)
    for k, (dg, cst, nm) in e.items():
        if k > 1:
            r = cst / cK(k)
            if r > worst.get(k, (0,))[0]: worst[k] = (r, p, dg, cst, nm)
print('max over p of K+_kappa / c_kappa:', worst)
