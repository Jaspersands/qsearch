"""Independent verifier for Mobius-orbit witnesses (t, z) printed by mobius_orbit.c.

Rebuilds alpha/beta from (p, kappa, t, z), finds labels by an independent method
(brute force over the kappa choices of which alpha-point gets label 0 and which beta-point
gets label 0, then labels read from coset tests), and checks every one of the kappa^2 cells
against the definition: alpha_j + beta_i in Q_{-(i+j)} u {0}, alpha_0 + beta_0 != 0,
where x in Q_m iff (x * g^{-m})^((p-1)/kappa) == 1, g the least primitive root.
Usage: python verify.py kappa file
"""
import sys


def primroot(p):
    n, f, d = p - 1, [], 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        f.append(n)
    g = 2
    while any(pow(g, (p - 1) // q, p) == 1 for q in f):
        g += 1
    return g


def coset(x, p, k, g):
    h = (p - 1) // k
    gi = pow(g, p - 2, p)
    for m in range(k):
        if pow(x * pow(gi, m, p) % p, h, p) == 1:
            return m
    raise ValueError


def verify(k, p, t, z):
    g = primroot(p)
    zeta = pow(g, (p - 1) // k, p)
    S = [pow(zeta, j, p) for j in range(k)]
    T = [t * s % p for s in S]
    if z < 0:
        a = S[:]
        b = [(-x) % p for x in T]
    else:
        a = [pow((s - z) % p, p - 2, p) for s in S]
        b = [(-pow((x - z) % p, p - 2, p)) % p for x in T]
    return verify_sets(k, p, a, b)


def verify_sets(k, p, a, b):
    """True iff some labelling of the values a (alphas) and b (betas) is a contraction."""
    g = primroot(p)
    assert len(set(a)) == k and len(set(b)) == k
    # try every choice of (alpha point labelled 0, beta point labelled 0)
    for x0 in range(k):
        for y0 in range(k):
            c00 = (a[x0] + b[y0]) % p
            if c00 == 0 or coset(c00, p, k, g) != 0:
                continue
            # labels: index(a_x + b_y) = -(la[x] + lb[y]); la[x0] = lb[y0] = 0
            la, lb = {x0: 0}, {y0: 0}
            for _ in range(2 * k):
                for x in range(k):
                    for y in range(k):
                        c = (a[x] + b[y]) % p
                        if c == 0:
                            continue
                        e = coset(c, p, k, g)
                        if x in la and y not in lb:
                            lb[y] = (-e - la[x]) % k
                        elif y in lb and x not in la:
                            la[x] = (-e - lb[y]) % k
            if len(la) != k or len(lb) != k:
                continue
            if len(set(la.values())) != k or len(set(lb.values())) != k:
                continue
            alpha = [None] * k
            beta = [None] * k
            for x in range(k):
                alpha[la[x]] = a[x]
            for y in range(k):
                beta[lb[y]] = b[y]
            good = (alpha[0] + beta[0]) % p != 0
            for i in range(k):
                for j in range(k):
                    c = (alpha[j] + beta[i]) % p
                    if c != 0 and coset(c, p, k, g) != (-(i + j)) % k:
                        good = False
            if good:
                return True
    return False


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "twoprog":
    k = int(sys.argv[1])
    n = bad = 0
    for line in open(sys.argv[2]):
        f = line.split()
        if len(f) >= 5:
            p, rho, t = int(f[0]), int(f[3]), int(f[4])
            a = [pow(rho, j, p) for j in range(k)]
            b = [(-t * pow(rho, i, p)) % p for i in range(k)]
            n += 1
            if not verify_sets(k, p, a, b):
                bad += 1
                print("FAIL", line.strip())
    print("verified", n - bad, "of", n, "witnesses")
elif __name__ == "__main__":
    k = int(sys.argv[1])
    n = bad = 0
    for line in open(sys.argv[2]):
        f = line.split()
        if len(f) >= 9:
            p, t, z = int(f[0]), int(f[7]), int(f[8])
            n += 1
            if not verify(k, p, t, z):
                bad += 1
                print("FAIL", line.strip())
    print("verified", n - bad, "of", n, "witnesses")
