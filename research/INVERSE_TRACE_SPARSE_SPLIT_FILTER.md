# Sparse Inverse Trace: A Split-Norm Proposal Filter

29 October 2026. Narrow mathematical deduction and executable controls;
independent automated review completed by Kierkegaard, accepting the stated
mathematical scope. Not human-reviewed or proof-assistant/kernel-verified.
No sparse-target solver or classical hardness claim. The count adapts the
[full-support counting filter](CONSTRUCTIVE_ROUTE_FILTERS.md#exact-lift-count),
not a new classical lower bound. No novelty claim.

## Contract And Proposal

Let q=2^n with odd n>=3, ell>=2, 1<=K<ell, and **L=ell-1**. Keep the
supplied field and arbitrary distinct zero-target points alpha_i. Put

```
P = product_i (X-alpha_i),  D=P',  R=D^2 mod P.
```

For the singleton result, the one-target point a is outside this set and
is fixed to x_a=1. Its ACTUAL syndrome is s_j=a^j, with s_0=1, and
P_one'/P_one=1/(X-a). A pair is valid exactly when

```
deg U, deg V <= L,
UV = D^2 mod P,
W=U+V,  W/P = 1/(X-a) + O(X^(-K-1)) at infinity.
```

The last condition prescribes K leading coefficients of W; in particular
deg W=L and its leading coefficient is 1. It leaves ell-K coefficients
free. The [native reduction](INVERSE_TRACE_NORM_ATTACK.md#sparse-targets-exact-remaining-problem-and-a-failed-extension)
has n odd prime, N=n^2, K=floor(N/8), and ell=N-1 for a singleton.
No arbitrary-syndrome solver is required here.

The bounded proposal is to draw F=R+P*T with deg T<=ell-2, factor F,
and seek an EXACT polynomial factorization F=UV with the required sum
tail, using local lifting or Pade reconstruction at infinity. There are
q^(ell-1) raw proposals. Call F productive if any such pair exists.

## 1. Monic Leading-Coefficient Obstruction

**Theorem.** No ordinary monic polynomial F of degree 2L is productive
when s_0=1 and n is odd.

**Proof.** A factorization F=UV with both degrees at most L forces both
degrees to equal L. Their leading coefficients c,d satisfy cd=1 and
c+d=1. Thus c^2+c+1=0, impossible because Tr(1)=1 for odd n. This is
ordinary monicity, not monicity after a free scalar normalization:
rescaling factors changes the fixed product residue or prescribed sum.

This FIRST obstruction also holds for any odd number of one-targets
fixed to 1, since s_0=1. The probability bound below is stated only for
the singleton syndrome, not generalized to arbitrary target patterns.

## 2. Formal Lifting Is Not Exact Reconstruction

Keep deg F=2L, but replace monicity by a nonzero leading coefficient
lambda with Tr(lambda)=0. For ANY completion W of the prescribed tail,
put t=X^(-1), y=t^L*U, w=t^L*W, f=t^(2L)*F. Then

```
y^2+w*y+f=0,  w(0)=1,  f(0)=lambda.
```

The constant equation y_0^2+y_0=lambda has two roots. Every later
coefficient y_r is determined linearly: its coefficient from w*y is 1,
while the square term uses only y_(r/2) when r is even. Thus both formal
roots exist to arbitrary precision. This local test imposes no additional
condition on F beyond its leading trace, even with the known singleton
tail. Lifting through r=L takes O(ell^2) field operations.

An EXACT rational Pade root cannot avoid polynomial termination. Writing
U=A/B in lowest terms in U^2+W*U+F=0 gives A^2=0 mod B, so B is
constant. A polynomial root has degree at most L, by comparing leading
degrees. Finite-precision matching alone does not give such a root.
This statement concerns this fixed quadratic, not all Pade/Pell methods.

## 3. Singleton Productivity Bound

**Theorem.** Sample the leading coefficient of T uniformly among the
q/2-1 nonzero trace-zero elements and its other ell-2 coefficients
independently uniformly. Then

```
Pr[F productive] <= (1+eta) q^(2-K)/(q-2),
eta = (q^K-1) beta^(ell-K+1),
beta = min(1, (1+2*ceil(sqrt(q)))/q).
```

The bound may be replaced by its minimum with 1. It is uniform in the
original distinct points, including the singleton location a.

**Proof.** Let M_s count zero-alphabet words with Hx=s for THIS singleton
syndrome. The existing [MDS/character-sum bound](INVERSE_TRACE_GIBBS_TARGET.md#uniform-fiber-counts-including-arbitrary-syndromes)
gives M_s<=(1+eta)q^(ell-K)/2^ell. We use that bound at the specified
native syndrome, not as an additional algorithmic requirement.

For each such word, z_i+z_i^(-1)=x_i has one nonzero root when x_i=0
and two otherwise. Each choice uniquely interpolates degree-<ell
polynomials U(alpha_i)=D(alpha_i)z_i and
V(alpha_i)=D(alpha_i)/z_i. Conversely every valid pair arises this way.
Hence there are at most 2^ell*M_s ordered valid pairs, including ALL
lower coefficients of W. The swap (U,V)->(V,U) preserves F and has no
fixed point, since U=V would give W=0, contradicting s_0=1. Therefore
the number of productive F is at most

```
2^(ell-1)*M_s <= (1+eta)q^(ell-K)/2.
```

The conditioned proposal space has exactly
(q/2-1)q^(ell-2) elements. Division proves the claim. The unconditioned
raw proposal bound is (1+eta)/(2*q^(K-1)). Both bounds grant complete
factor allocation and recognition for free; factorization alone does not
establish that those operations are efficient.

When eta is bounded, independent trials require Omega(q^(K-1)) expected
proposals, even under that free-recognition grant. Polynomial-cost formal
lifting and expected-polynomial finite-field factorization do not remove
this rejection cost. A proposal law bounded pointwise by C times the raw
uniform law has success at most C*(1+eta)/(2*q^(K-1)). No such density
bound is assumed for an arbitrary target-dependent construction.

## Exact Native n17 Control

For n=17, N=289, K=36, ell=288, L=287, q=131072:

```
beta = 727/131072 < 2^(-7),
eta = (q^36-1)*(727/q)^253 < 2^(-1159),
B17 = (1+eta)/((q-2)*q^34) < 2^(-594).
```

These are exact rational inequalities, not floating-point estimates or
observed success rates. Thus the specified repaired rejection sampler
needs more than 2^594 expected proposals if run until success.

The following self-contained command uses the already-installed
python-flint, explicit irreducible moduli, and polynomial-basis arithmetic
(FQ_NMOD, not Zech/logarithm tables). It has no repository imports and
writes no files. For n=5,7,17 it uses native points 0,...,n^2-1 in
polynomial-basis encoding, singleton target at 0, c equal to the field
generator, lambda=c^2+c, and T=lambda*X^(ell-2). W is the quotient P/X:
W/P=1/X+P(0)/(X*P), so its singleton tail is correct. These particular
lower coefficients of W are a control choice, not a theorem restriction.

```sh
/opt/anaconda3/bin/python -B - <<'PY'
from fractions import Fraction
from flint import fq_default_ctx, fq_default_poly_ctx, fmpz_mod_poly_ctx

for n, modulus in ((5, 0x25), (7, 0x83), (17, 0x20009)):
    k = fq_default_ctx(modulus=fmpz_mod_poly_ctx(2)(
        [(modulus >> j) & 1 for j in range(n+1)]), fq_type='FQ_NMOD')
    ring = fq_default_poly_ctx(k)
    X, P = ring.gen(), ring.one()
    N, q = n*n, 1 << n
    K, ell, L = N//8, N-1, N-2
    for raw in range(1, N):
        P *= X + k([(raw >> j) & 1 for j in range(n)])
    D = P.derivative()
    R = D*D % P
    W, remainder = divmod(P, X)
    assert remainder.degree() == 0 and X*W+remainder == P
    c = k([0, 1])
    lam = c*c+c
    assert lam != 0 and int(lam.trace()) == 0
    assert int(k.one().trace()) == 1 and W[L] == k.one()
    F = R + P*(lam*X**(ell-2))
    w = [W[L-j] for j in range(L+1)]
    f = [F[2*L-j] for j in range(L+1)]
    y = [c]
    for j in range(1, L+1):
        v = f[j] + (y[j//2]**2 if j % 2 == 0 else k.zero())
        for i in range(1, j+1):
            v += w[i]*y[j-i]
        y.append(v)
    U = ring(list(reversed(y)))
    V = W+U
    error = F+U*V
    assert U+V == W and F.degree() == 2*L
    assert not error.is_zero() and error.degree() < L
    assert U*V % P != R
    print(n, 'L=', L, 'matched product degrees=', (L, 2*L),
          'error degree=', error.degree(), 'global congruence fails')
    if n == 17:
        eta = (q**K-1)*Fraction(727, q)**(ell-K+1)
        bound = (1+eta)/((q-2)*q**(K-2))
        assert eta < Fraction(1, 2**1159)
        assert bound < Fraction(1, 2**594)
        print('exact n17 rational bounds PASS')
PY
```

Executed controls: error degrees 22,46,286 respectively, strictly below
L=23,47,287. The product matches degrees L through 2L, NOT all
nonnegative degrees. Its nonzero error has degree below ell and therefore
cannot vanish modulo P. These examples falsify naive formal-lift
truncation; they do not prove general search hardness.

## Review And Verification

Kierkegaard independently checked the zero-aware lift count: the GF(8)
example has 6*2^3+8*2^5=304 ordered lifts, not the loose upper bound
14*2^5=448. The reviewer also verified 36 productive proposals out of 192
in a SEPARATE fixture and checked the native bounds. These finite counts
are controls, not the proof of the asymptotic productivity bound.

The parent successfully replayed the inline FQ_NMOD command and reported
15 passing production-backed parameterized cases in
[test_inverse_trace_sparse_route_filters.py](../tests/test_inverse_trace_sparse_route_filters.py).
That combined sparse-route file includes the odd/even-field leading-term
controls, formal-lift failures, and exact n17/n31/n61 proposal bounds,
alongside controls for other sparse routes. This is automated verification,
not human or kernel verification; the mathematical scope above is unchanged.

## Scope And Remaining Obligation

The leading-coefficient obstruction and local-lifting distinction add
specific filters beyond the inspected notes. The counting argument is an
adaptation of existing counting, not an algorithmic advance or a new
classical complexity lower bound. No high-genus rejection argument is used.

This does NOT exclude another product degree, a specially coupled F,W
construction exploiting P_one'/P_one, or a sufficiently concentrated
Pade/Pell proposal. Even singleton native SEARCH remains unresolved by
this investigation. A surviving mechanism must construct the global
factor pair and charge its success probability, not merely its formal
expansion at infinity. Automated review is complete; handoff integration
remains with the parent. No general solver/module is introduced here.
