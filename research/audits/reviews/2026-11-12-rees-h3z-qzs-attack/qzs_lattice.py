"""QZS attack, two-variable relaxation: find integers (mu1, mu2) != 0 with
|| theta1*mu1^2 + theta2*mu2^2 || <= 2^-K, theta_i = rho_i/M exactly uniform (M = 2^m).

Method SDA-ISO (this note, Sec. 2):
  1. simultaneous Diophantine approximation (3-dim LLL): q, c_i with |q theta_i - c_i| <= eps;
  2. keep q prime with -c2/c1 a square mod q (try small combinations of the reduced basis);
  3. r = sqrt(-c2/c1) mod q; Gauss-reduce {(mu1,mu2): mu1 = r mu2 mod q} (det q) -> mu.
  Then theta1 mu1^2 + theta2 mu2^2 = (c1 mu1^2 + c2 mu2^2)/q + (e1 mu1^2 + e2 mu2^2)/q,
  first term an integer, second <= 2 eps * (4/3)^(1/2).
Baseline LIN (Coppersmith-style linearization): LLL on {(A,B,m): theta1 A + theta2 B ~ m},
  enumerate small combinations, success iff A, B are both perfect squares (not both 0).
Every success is verified with exact rational arithmetic.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python qzs_lattice.py [trials] [seed]
"""
import itertools, math, random, sys, time
from fractions import Fraction
from fpylll import IntegerMatrix, LLL
from sympy import isprime, sqrt_mod

def dist_int(fr):  # ||fr|| for a Fraction
    f = fr - math.floor(fr)
    return min(f, 1 - f)

def lll_rows(rows):
    A = IntegerMatrix.from_matrix(rows); LLL.reduction(A)
    return [[int(A[i, j]) for j in range(A.ncols)] for i in range(A.nrows)]

def combos(basis, R):
    n = len(basis)
    for co in itertools.product(range(-R, R + 1), repeat=n):
        if all(c == 0 for c in co): continue
        yield [sum(co[i] * basis[i][j] for i in range(n)) for j in range(len(basis[0]))]

def gauss_reduce(u, v):
    def n2(a): return a[0]*a[0] + a[1]*a[1]
    if n2(u) > n2(v): u, v = v, u
    while True:
        d, nn = u[0]*v[0] + u[1]*v[1], n2(u)
        m = (2*d + nn) // (2*nn)          # exact nearest integer
        v = [v[0] - m*u[0], v[1] - m*u[1]]
        if n2(v) >= n2(u): return u
        u, v = v, u

def sda_iso(rho, M, K, R=5, slack=4):
    """returns (mu1, mu2, q, tries) or None"""
    eps_bits = K + 2 + slack               # basis eps = 2^-(K+2+slack); combos cost <= 2^slack
    W = M >> (3 * eps_bits)                # W = M eps^3
    assert W >= 1
    B = lll_rows([[W, rho[0], rho[1]], [0, M, 0], [0, 0, M]])
    seen, tries = set(), 0
    for vec in sorted(combos(B, R), key=lambda v: max(abs(x) for x in v)):
        if vec[0] == 0: continue
        if vec[0] < 0: vec = [-x for x in vec]
        q = vec[0] // W
        if q in seen: continue
        seen.add(q); tries += 1
        if not isprime(q): continue
        c1, c2 = [(q * rho[i] - vec[i + 1]) // M for i in range(2)]
        # vec[i+1] = q rho_i - c_i M  -> e_i = vec[i+1]/M, need |e_i| small
        if max(abs(vec[1]), abs(vec[2])) * (1 << (K + 2)) > M: continue   # |e_i| <= 2^-(K+2)
        if c1 % q == 0:
            continue
        t = (-c2 * pow(c1, -1, q)) % q
        if t != 0 and pow(t, (q - 1) // 2, q) != 1: continue
        r = int(sqrt_mod(t, q))
        mu = gauss_reduce([q, 0], [r, 1])
        assert (c1*mu[0]**2 + c2*mu[1]**2) % q == 0
        return mu[0], mu[1], q, tries
    return ('fail', tries)

def lin_baseline(rho, M, K, R=3):
    """Coppersmith-style linearization: short (A,B,m) with theta1 A+theta2 B - m small."""
    W = M >> (2 * K // 3 + 1) if M >> (2 * K // 3 + 1) else 1
    # vector = (A W', B W', A rho1 + B rho2 - m M): balanced at |A| ~ 2^{K/3}
    S = 1 << (K // 3 + 1)
    B = lll_rows([[1, 0, rho[0]], [0, 1, rho[1]], [0, 0, M]])
    B = lll_rows([[S * r[0], S * r[1], r[2]] for r in B])
    best = None
    for vec in combos(B, R):
        A, Bv = vec[0] // S, vec[1] // S
        if A < 0 or Bv < 0 or (A == 0 and Bv == 0): continue
        a, b = math.isqrt(A), math.isqrt(Bv)
        if a * a == A and b * b == Bv:
            d = dist_int(Fraction(rho[0] * A + rho[1] * Bv, M))
            if d <= Fraction(1, 1 << K):
                return a, b
    return None

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    print('| K | m=log2 M | first pair ok | SDA-ISO success (<=3 pairs) | max log2|mu| | max log2 dist | mean candidates q tried | mean time (s) | LIN success |')
    print('|---|---|---|---|---|---|---|---|---|')
    for K in [20, 30, 40, 50, 60, 80, 100, 150, 200, 300]:
        m = 3 * (K + 6) + 40
        M = 1 << m
        ok = lin_ok = 0; mumax = -1; dmax = -1e9; tt = 0.0; tries_l = []; fails_tries = []; first_ok = 0
        for _ in range(trials):
            t0 = time.time()
            for attempt in range(3):              # up to 3 fresh sample pairs (6 coset states)
                rho = [rng.randrange(M), rng.randrange(M)]
                res = sda_iso(rho, M, K)
                if res[0] != 'fail': break
            tt += time.time() - t0
            if res[0] != 'fail' and attempt == 0: first_ok += 1
            if res[0] == 'fail':
                fails_tries.append(res[1])
            else:
                mu1, mu2, q, tries = res; tries_l.append(tries)
                d = dist_int(Fraction(rho[0] * mu1 * mu1 + rho[1] * mu2 * mu2, M))
                if (mu1, mu2) != (0, 0) and d <= Fraction(1, 1 << K):
                    ok += 1
                    mumax = max(mumax, math.log2(max(abs(mu1), abs(mu2))))
                    dmax = max(dmax, math.log2(d) if d else -9999)
            if K <= 40 and lin_baseline(rho, M, K):
                lin_ok += 1
        lin = f'{lin_ok}/{trials}' if K <= 40 else 'not run'
        mt = sum(tries_l)/len(tries_l) if tries_l else float('nan')
        print(f'| {K} | {m} | {first_ok}/{trials} | {ok}/{trials} | {mumax:.1f} | {dmax:.1f} | {mt:.1f} | {tt/trials:.3f} | {lin} |')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
