"""Independent cross-check of famsym's 'complete' mode: decide by plain backtracking (pure
Python, no shared code) whether the T1 family has a strict solution, i.e. gamma in F_p^K,
b in Z_K, gamma distinct, gamma_j + gamma_k in Q_{b-(j+k)} for all j <= k, and compare with
famsym's COMPLETE_EMPTY / FOUND lines.  Usage: python xcheck_t1.py K PMAX famsym_output"""
import re
import sys
from sympy import primerange, primitive_root

K, PMAX, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]


def t1_feasible(p):
    g = primitive_root(p)
    ind = [None] * p
    x = 1
    for e in range(p - 1):
        ind[x] = e % K
        x = x * g % p
    inv2 = (p + 1) // 2
    for b in range(K):
        gam = [pow(g, b, p) * inv2 % p]          # 2 gamma_0 = g^b in Q_b (scaling by Q_0)

        def ok(x, k):
            v2 = 2 * x % p
            if v2 == 0 or ind[v2] != (b - 2 * k) % K:
                return False
            for j, y in enumerate(gam):
                v = (x + y) % p
                if x == y or v == 0 or ind[v] != (b - (j + k)) % K:
                    return False
            return True

        def rec(k):
            if k == K:
                return True
            for x in range(p):
                if ok(x, k):
                    gam.append(x)
                    if rec(k + 1):
                        return True
                    gam.pop()
            return False

        if rec(1):
            return True
    return False


st = {}
for line in open(out):
    m = re.match(r"(FOUND|NOTFOUND) k=\d+ p=(\d+)", line)
    if m:
        st[int(m.group(2))] = "FOUND" if m.group(1) == "FOUND" else (
            "COMPLETE_EMPTY" if "COMPLETE_EMPTY" in line else "OTHER")
agree = dis = 0
for p in primerange(3, PMAX):
    if p % K != 1 or p not in st:
        continue
    f = t1_feasible(p)
    a = st[p]
    if (f and a == "FOUND") or (not f and a == "COMPLETE_EMPTY"):
        agree += 1
    else:
        dis += 1
        print("DISAGREE", p, f, a)
print(f"K={K} p<{PMAX}: agree={agree} disagree={dis}")
