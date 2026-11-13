"""Exact finite native controls, with Fock normalization cancelled symbolically.

D=L*A*L^-1 is the physical orthogonal rotation; G=L^2 is diagonal.
No normalized radicals need materialization. This is not a CDF algorithm.
"""
from pathlib import Path
import json
from sage.all import QQ, CyclotomicField, PolynomialRing, matrix, diagonal_matrix, binomial, factorial, vector

field = CyclotomicField(168)
zeta = field.gen()
z8, z12, z7 = zeta**21, zeta**14, zeta**24
cb = (z8+z8**-1)/2
ring = PolynomialRing(field, 'x')
x = ring.gen()
counts = {'prefixes': 0, 'offdiagonal_entries': 0, 'diagonal_entries': 0}
non_low_rank = False
for K in (2, 3, 5, 9):
    G = diagonal_matrix(field, [factorial(m)*factorial(K-m) for m in range(K+1)])
    for c, s in ((cb, cb), ((z12+z12**-1)/2, field(1)/2)):
        A = matrix(field, K+1, K+1, lambda y, m:
            ((c*x+s)**m * (-s*x+c)**(K-m))[y])
        assert A.transpose()*G*A == G
        inverse = A.inverse()
        N = diagonal_matrix(field, list(range(K+1)))
        R = A*N*inverse
        assert all(R[i,j] == 0 for i in range(K+1) for j in range(K+1)
                   if abs(i-j) > 1)
        polynomials = [ring.lagrange_polynomial(
            [(m, A[y,m]/A[0,m]) for m in range(K+1)])
            for y in range(K+1)]
        assert all(p.degree() == j for j,p in enumerate(polynomials))
        state = vector(field, [binomial(K,m)*cb**K *
                               z7**(m*(m-1)//2) for m in range(K+1)])
        assert sum(state[m].conjugate()*G[m,m]*state[m]
                   for m in range(K+1)) == G[K,K]
        out = A*state
        for t in range(K):
            Pi = diagonal_matrix(field, [int(y<=t) for y in range(K+1)])
            P = inverse*Pi*A
            r = R[t,t+1]
            assert N*P-P*N == inverse*(R*Pi-Pi*R)*A
            assert (N*P-P*N).rank() == 2
            non_low_rank |= P.rank() > 2
            p, q = polynomials[t], polynomials[t+1]
            ratio = p.leading_coefficient()/q.leading_coefficient()
            assert ratio == r
            for m in range(K+1):
                diagonal = G[t,t]*A[0,m]**2/G[m,m]*ratio*(q.derivative()(m)*p(m)-p.derivative()(m)*q(m))
                assert P[m,m] == diagonal
                counts['diagonal_entries'] += 1
                for n in range(K+1):
                    if m == n:
                        continue
                    assert (m-n)*P[m,n] == G[t,t]*r/G[m,m]*(A[t+1,m]*A[t,n]-A[t,m]*A[t+1,n])
                    counts['offdiagonal_entries'] += 1
            cdf = sum(out[y].conjugate()*G[y,y]*out[y] for y in range(t+1))/G[K,K]
            assert cdf == sum(state[m].conjugate()*G[m,m]*P[m,n]*state[n]
                              for m in range(K+1) for n in range(K+1))/G[K,K]
            counts['prefixes'] += 1
assert non_low_rank
result = {'scope': 'Exact finite algebra only; no efficient CDF evaluation or sampler.',
          'controls': counts, 'projector_not_low_rank': non_low_rank,
          'arithmetic': 'Exact cyclotomic field; Fock normalization cancels by G-conjugacy.',
          'prior_attempts': ['Initial symbolic QQbar coercion failed before tests.',
                             'Normalized-radical run terminated after five minutes without result; not a failed identity.']}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
