"""Mechanical test of Lemma 5's restriction map: each FEASIBLE kappa-witness of dfs2b, restricted
to indices in m*Z (m = kappa/D, gcd(D,m)=1), must be a D-contraction for the generator g^m."""
import re, sys
K, D = int(sys.argv[1]), int(sys.argv[2]); m = K//D
n = 0
for l in open(f'dfs2b_k{K}.out'):
    r = re.match(r'FEASIBLE k=\d+ p=(\d+) g=(\d+) .*beta=([\d,]+) alpha=([\d,]+)', l)
    if not r: continue
    p, g = int(r.group(1)), int(r.group(2))
    beta = [int(x) for x in r.group(3).split(',')]; alpha = [int(x) for x in r.group(4).split(',')]
    gp = pow(g, m, p); e = (p-1)//D; z = pow(gp, e, p)
    ok = (alpha[0] + beta[0]) % p != 0
    for i in range(D):
        for j in range(D):
            c = (alpha[m*j] + beta[m*i]) % p
            if c and pow(c, e, p) != pow(z, (-(i+j)) % D, p): ok = False
    # and the full kappa-witness itself
    h = (p-1)//K; zk = pow(g, h, p)
    for i in range(K):
        for j in range(K):
            c = (alpha[j] + beta[i]) % p
            if c and pow(c, h, p) != pow(zk, (-(i+j)) % K, p): ok = False
    n += 1; print(p, 'restriction is a D-contraction:', ok)
print('tested', n)
