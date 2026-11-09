# s2a: independent check of every FEASIBLE witness printed by e2search (modes 0/1/2/3).
import sys, re, sympy
def check_line(line):
    m = re.match(r'k=(\d+) p=(\d+) mode=(\d+) xi=(\d+) FEASIBLE', line)
    if not m: return None
    k, p, mode, xi = map(int, m.groups())
    h = (p-1)//k
    zeta = pow(xi, h, p)
    assert all(pow(zeta, k//q, p) != 1 for q in sympy.primefactors(k)), "xi not a coset generator"
    pw = {pow(zeta, j, p): j for j in range(k)}
    def ind(x):
        x %= p
        return None if x == 0 else pw[pow(x, h, p)]
    z = [pow(xi, j, p) for j in range(k)]
    if mode in (0, 1):
        beta = list(map(int, re.search(r'beta=([\d,]+)', line).group(1).split(',')))
        alpha = list(map(int, re.search(r'alpha=([\d,]+)', line).group(1).split(',')))
        C = [[z[i]*z[j]*(alpha[j]+beta[i]) % p for j in range(k)] for i in range(k)]
    else:
        t = list(map(int, re.search(r't=([\d,]+)', line).group(1).split(',')))
        C = [[z[i]*z[j]*(t[i]+t[j]) % p for j in range(k)] for i in range(k)]
    ok = C[0][0] != 0 and all((C[i][j] == 0 and mode in (0, 2)) or ind(C[i][j]) == 0 for i in range(k) for j in range(k))
    # annihilation of W (x) W: C_ij = z_i z_j (alpha_j + beta_i) has the normal form by construction;
    # test on a random element of W (x) W as well
    import random
    W = []
    for _ in range(2):
        w = [random.randrange(p) for _ in range(k)]
        w[0] = (-sum(z[m]*w[m] for m in range(1, k))) % p   # z_0 = 1
        W.append(w)
    X = [[W[0][i]*W[1][j] % p for j in range(k)] for i in range(k)]
    ok = ok and sum(C[i][j]*X[i][j] for i in range(k) for j in range(k)) % p == 0
    return ok
n = bad = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        r = check_line(line)
        if r is None: continue
        n += 1
        if not r: bad += 1; print("BAD", fn, line.strip()[:100])
print("witnesses checked:", n, "bad:", bad)
