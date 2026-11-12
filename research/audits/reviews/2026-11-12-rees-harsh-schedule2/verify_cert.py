"""Verify NONMEMBER certificates printed by e2dfs / e2rand independently.

For each line "p NONMEMBER ... x=... y=..." it checks, with pow() only (no tables), that
x_j - y_i lies in Qo_{-(i+j)} for all i, j, where Q_m = g^m (F_p^*)^k for a primitive root
g found here by trial, and that x_0 != y_0.  It then builds alpha = x, beta = -y and the
matrix C_ij = z_i z_j (alpha_j + beta_i), z_m = g^m, and checks directly that every entry is
a k-th power or 0, C_00 != 0, and that C annihilates W (x) W (via the normal-form identity,
checked numerically on a basis of W (x) W).  Usage: verify_cert.py kappa file...
"""
import sys


def primroot(p):
    n = p - 1
    fs = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fs):
            return g


def check(k, p, x, y):
    h = (p - 1) // k
    g = primroot(p)
    zeta = pow(g, h, p)
    zp = [pow(zeta, m, p) for m in range(k)]

    def coset(v):
        v %= p
        if v == 0:
            return None
        return zp.index(pow(v, h, p))

    assert len(x) == k and len(y) == k
    assert (x[0] - y[0]) % p != 0
    for i in range(k):
        for j in range(k):
            c = coset(x[j] - y[i])
            if c is not None and c != (-(i + j)) % k:
                return False
    # matrix check
    z = [pow(g, m, p) for m in range(k)]
    alpha = [v % p for v in x]
    beta = [(-v) % p for v in y]
    C = [[z[i] * z[j] * (alpha[j] + beta[i]) % p for j in range(k)] for i in range(k)]
    if C[0][0] == 0:
        return False
    for i in range(k):
        for j in range(k):
            if C[i][j] and pow(C[i][j], h, p) != 1:
                return False
    # annihilation of W (x) W: basis w^(a) = e_a - z_a e_0 (a=1..k-1), since sum z_m w_m = 0
    for a in range(1, k):
        for b in range(1, k):
            # X = w^(a) (x) w^(b): X_ij = w^a_i w^b_j
            wa = [0] * k
            wa[a] = 1
            wa[0] = (-z[a]) % p
            wb = [0] * k
            wb[b] = 1
            wb[0] = (-z[b]) % p
            s = sum(C[i][j] * wa[i] * wb[j] for i in range(k) for j in range(k)) % p
            if s:
                return False
    return True


def main():
    k = int(sys.argv[1])
    ok = bad = 0
    for fn in sys.argv[2:]:
        for line in open(fn):
            if 'NONMEMBER' not in line:
                continue
            parts = line.split()
            p = int(parts[0])
            xs = [int(t) for t in [s for s in parts if s.startswith('x=')][0][2:].split(',')]
            ys = [int(t) for t in [s for s in parts if s.startswith('y=')][0][2:].split(',')]
            if check(k, p, xs, ys):
                ok += 1
            else:
                bad += 1
                print('BAD', p)
    print(f'kappa={k} certificates verified={ok} bad={bad}')


if __name__ == '__main__':
    main()
