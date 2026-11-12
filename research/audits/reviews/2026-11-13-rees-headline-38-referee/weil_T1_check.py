# Referee: falsifier for lem:two-term: T_1 = F_p^x (and 0 not in T_1) at every prime p in [4k^4, LIM], k = 2,4,6,8;
# also the count bound #{u : eta - u^k in eps P} >= p/(2k) for every eta, at primes in [4k^4, 4k^4+3000].
import sys, json, numpy as np
sys.path.insert(0, '.')
import s1h_referee as R
LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
fails, cnt_fail, n, ncnt = [], [], 0, 0
for p in R.primes_upto(LIM):
    for k in (2, 4, 6, 8):
        if p < 4 * k ** 4 or (p - 1) % k: continue
        F = R.Field(p); add0, m1 = R.coset_data(F, k)
        T, e = R.T_sets(F, k, add0, m1, 1)
        n += 1
        if not (len(T[1][0]) == k and not T[1][1]): fails.append((p, k))
        if p < 4 * k ** 4 + 3000:
            ncnt += 1
            h = (p - 1) // k
            if h % 2: q = p - 1
            else:
                th = next(x for x in range(2, p) if pow(x, (p - 1) // 2, p) == p - 1); q = pow(th, k // 2, p)
            eps = (-pow(q, p - 2, p)) % p
            u = np.arange(1, p, dtype=np.int64)
            uk = np.array([pow(int(x), k, p) for x in u], dtype=np.int64)
            einv = pow(eps, p - 2, p)
            for i in range(k):                       # one eta per coset suffices (T stable under P)
                eta = int(F.pw[i])
                z = (eta - uk) % p * einv % p
                ok = (z != 0) & (F.dl[z] % k == 0)
                if ok.sum() < p / (2 * k): cnt_fail.append((p, k, eta, int(ok.sum())))
print(json.dumps({"LIM": LIM, "pairs_checked": n, "T1_failures": fails, "count_pairs": ncnt, "count_failures": cnt_fail}))
