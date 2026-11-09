# Circuit-model classical filter for F = Q^((p-1)/2):  Q(z) * F(z)^2 = Q^[p](z),
# where Q^[p](z) = sum_a c_a z^(p a).  Linear in the coefficients c_a of Q.
# Evaluate F only as a black box over E = GF(p^K) (as a circuit would allow),
# solve for c, and check that the solution space is E * Q.
# Run: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/sage frobenius_root_filter_check.sage
import itertools, random
random.seed(int(7))
set_random_seed(7)

def mons(n, d):
    return [e for e in itertools.product(range(d + 1), repeat=n) if sum(e) <= d]

def trial(p, n, d, K):
    F0 = GF(p)
    R = PolynomialRing(F0, n, 'x')
    xs = R.gens()
    while True:
        Q = R.random_element(degree=d, terms=Infinity)
        if Q.degree() == d and Q.factor()[0][0] == Q and len(Q.factor()) == 1:
            break
    h = (p - 1) // 2
    E = GF(p**K, 'w')
    M = mons(n, d)
    rows = []
    for _ in range(len(M) + 10):
        z = [E.random_element() for _ in range(n)]
        Fz = Q(*z)**h                       # black-box evaluation of F over E
        row = []
        for a in M:
            za = prod(zi**ai for zi, ai in zip(z, a))
            zpa = prod((zi**p)**ai for zi, ai in zip(z, a))
            row.append(za * Fz**2 - zpa)
        rows.append(row)
    A = matrix(E, rows)
    ker = A.right_kernel()
    truth = vector(E, [Q.monomial_coefficient(prod(x**ai for x, ai in zip(xs, a))) for a in M])
    ok = ker.dimension() == 1 and truth in ker
    print("p=%d n=%d d=%d K=%d unknowns=%d kernel_dim=%d recovers_Q=%s" % (p, n, d, K, len(M), ker.dimension(), ok))

for (p, n, d, K) in [(7, 2, 3, 6), (11, 3, 3, 4), (13, 3, 4, 4), (101, 2, 5, 3)]:
    trial(p, n, d, K)
