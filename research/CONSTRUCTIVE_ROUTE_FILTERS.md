# Two Constructive Route Filters

29 October 2026. Written deductions checked by the parent and independently
reviewed by Huygens. The reviewer found no algebraic counterexample, but
required the unconditional sampling and formal-polynomial qualifications
below. This is automated mathematical review, not human review, formal
verification, a novelty claim, a speedup, or a hardness result.

The two conclusions reject specific proposed ways of manufacturing a
useful application. They do not rule out other samplers or other succinct
polynomial families. No new algorithmic machinery is introduced here.

## 1. Full-Support Norm Relaxation

### Native Problem And Proposal

Keep the original all-one inverse-trace relation, with q=2^n, odd n,
distinct supplied alpha_i in F_q, and 1<=K<N<=q:

```
Omega = {x : sum_i alpha_i^j*x_i=0 for 0<=j<K,
             Tr(inv0(x_i))=1 for every i},    inv0(0)=0.
```

Every valid coordinate is nonzero. Assume Omega is nonempty when discussing
its uniform distribution. No points, targets, or parity equations change.
The [earlier norm attack](INVERSE_TRACE_NORM_ATTACK.md) restricts both
polynomial components to the code degree bound. That gives a classical
search route, but its entire output family has very small uniform native
mass at n17. Here we relax ONE component to restore full support.

Put

```
beta_i = sqrt(alpha_i),   P(X) = product_i (X-beta_i),
D = P',                  L = N-K-1,       R = D^2 mod P.
```

Distinctness gives gcd(D,P)=1. Consider ordered pairs (A,B) satisfying

```
deg A < N,      deg B <= L,      B(beta_i) != 0 for every i,
F = A^2 + A*B + B^2,            F mod P = R.
```

Their native output is x_i=(B(beta_i)/D(beta_i))^2. The proposal draws
F=R+P*T with EVERY coefficient of T of degree at most N-2 independently
uniform in F_q, including a possibly zero leading coefficient. Thus

```
Q = q^(N-1)
```

is the exact number of equiprobable proposals. They have degree at most
2N-2 and are nonzero, since R is a unit modulo P. A monic or exact-degree
proposal is a different law.

### Exact Lift Count

For x in Omega, set b_i=sqrt(x_i). Squaring the beta-code parity equations
gives the original alpha-code equations, so there is a unique B of degree
at most L with B(beta_i)/D(beta_i)=b_i. This is the usual weighted
Lagrange parametrization of the Vandermonde kernel.

Write a_i=A(beta_i)/D(beta_i). The local norm equation is
a_i^2+a_i*b_i+b_i^2=1. Since b_i!=0, it is equivalent to

```
z_i^2 + z_i = 1 + 1/x_i,       z_i = a_i/b_i.
```

Its right side has trace zero: Tr(1)=1 because n is odd, and the target
trace is one. It has exactly two distinct roots. Independent choices at
all N coordinates interpolate a unique A of degree less than N.
Conversely, every valid pair gives a native word by the same equations.
Therefore EVERY native word has exactly 2^N ordered lifts.

Let Z(F) count the valid ordered lifts of a proposal, including BOTH
degree restrictions and all nonvanishing restrictions. Then

```
sum_F Z(F) = 2^N * |Omega|.
```

The involution (A,B)->(A+B,B) preserves F and its output and has no valid
fixed point. In particular, every productive F has Z(F)>=2. Hence

```
pi := Pr_uniform_F[Z(F)>0] <= min(1,u),
u  := 2^(N-1)*|Omega| / q^(N-1).
```

This is an upper bound on productivity even if complete factorization,
all norm allocations, and perfect recognition of valid lifts were free.
It is not an equality for pi.

### Comparison With Accepted-Free Prange

Choose an information set of N-K positions, sample their values uniformly
from the trace-one alphabet of size q/2, and solve the K parity pivots.
The Vandermonde property makes the pivot solve unique. Checking the pivot
traces gives exact single-trial success probability

```
p_Pr = |Omega| / (q/2)^(N-K),
u    = p_Pr * (2/q)^(K-1).
```

The existing uniform fiber bound gives
|Omega| <= (1+eta)*q^(N-K)/2^N, so

```
u <= (1+eta)/(2*q^(K-1)).
```

The bound is implemented by `reciprocal_bound` in
[inverse_trace_gibbs_target.py](../theorems/inverse_trace_gibbs_target.py).
For n17,N289,K36, the ratio u/p_Pr is EXACTLY 2^-560, and u<2^-595.
For example, its distance bound uses
beta=(1+2*ceil(sqrt(2^17)))/2^17=727/131072<2^-7, giving
eta<2^(17*36-7*(289-36+1))=2^-1166<1. Thus the rarity statement does
not depend on an unverified finite success rate.

This particular full-support repair is much worse per raw proposal than
the existing classical information-set baseline. The comparison does
not claim Prange is optimal; the earlier norm method already solves the
dense-target SEARCH task efficiently in its stated regime.

### Envelope And Exact Reweighted Law

Let E=F_(q^2) and rho^2+rho+1=0. Since n is odd, rho is not in F_q,
and h=B+rho*A has norm F. Factor a nonzero F over F_q as
u_0*product_f f^(v_f). Odd-degree irreducibles remain irreducible over E;
their multiplicities must be even and are allocated equally. Every
even-degree irreducible splits into a conjugate pair, with v_f+1 choices
of allocation. The leading unit has q+1 norm preimages. Consequently the
number of ALL polynomial norm representations, before imposing validity,
is zero if an inert multiplicity is odd, and otherwise is

```
(q+1) * product_(even-degree f) (v_f+1)
  <= (q+1)*2^(deg F/2)
  <= M := (q+1)*2^(N-1).
```

This includes repeated factors, nonmonic polynomials, and nonzero
constants. It follows that Z(F)<=M. Grant exact Z(F) and exact uniform
selection of a valid ordered lift. Draw uniform F, accept with probability
Z(F)/M, and on acceptance choose that lift. Every native word then has
the same UNCONDITIONAL probability

```
Pr[out=x] = 2^N/(Q*M),
s_accept  = 2*|Omega| / ((q+1)*q^(N-1)).
```

Conditional on success the output is exactly uniform on Omega; otherwise
the output is ABORT. This corrects the law, not the cost. Computing Z(F),
enumerating or sampling valid allocations, and all failed proposals remain
charged. Polynomial-time factorization alone does not establish efficient
valid-lift counting or sampling. The productivity upper bound already
applies even with these operations granted for free.

### Finite-Trial And Mixture Scope

Let S_old be the whole earlier norm output family and let
zeta=Uniform_Omega(S_old), NOT an algorithmic mixing weight. Suppose output
outside S_old requires at least one productive proposal among at most t
fresh uniform raw draws of F. Adaptation and screening must charge every
discarded draw. A union bound gives, on Omega union {ABORT},

```
TV(mu, Uniform_Omega) >= max(0, 1-zeta-t*u).
```

This applies unconditionally, including abort mass, or when failures fall
back to the old family. At n17 the earlier note supplies zeta<=2^-70.
It does NOT survive arbitrary conditioning on success: the reweighted
sampler above has conditional TV zero. Unlike the old support-only bound,
the finite-trial bound cannot silently be transferred to that conditional
law. Independent postprocessing that leaves the specified families is
outside the argument.

A proposal law bounded pointwise by C/Q has productivity at most C*u;
the same applies conditionally at each adaptive trial if the bound holds
for every history. A polynomially bounded density tilt cannot remove the
n17 loss. An unrestricted, highly concentrated proposal is not ruled out,
but constructing and accounting for it is a different unresolved task.
Conditioning on maximal degree changes Q to (q-1)*q^(N-2) and permits a
q/(q-1) factor in the productivity upper bound; the constant 2^N lift
count per word need not survive that restriction.

## 2. Arbitrary-Degree Scalar Postcomposition

### Formal Stabilizer Equality

Let k be ANY field of characteristic p and Gamma a finite p-subgroup of
GL(D,k), acting by coefficient-fixing linear substitutions. For any formal
polynomial F in k[x_1,...,x_D] and any NONCONSTANT R in k[T],

```
Stab_Gamma(R(F)) = Stab_Gamma(F).
```

There is no restriction on deg R, no perfectness assumption on k, and no
separability assumption on R. Constants F are immediate. For nonconstant
F, put J=R(F) and H=Stab_Gamma(J).

The primary algebraic input is
[Arzhantsev--Petravchuk, Proposition 1](https://arxiv.org/pdf/math/0608157):
the integral closure of k[J] inside the polynomial ring is k[h] for one
polynomial h. Each element of H preserves this ring and acts on h by
h->a*h+b, with a in k^* and b in k. Normalize h(0)=0. A linear action
fixes the origin, forcing b=0. Every element has p-power order, whereas
k^* has no nontrivial p-power torsion in characteristic p. Thus a=1.

Dividing R(T)-J by its nonzero leading coefficient gives a monic equation
for F over k[J]. Therefore F belongs to k[h] and is fixed by H. The
reverse inclusion is immediate. The same paper's Theorem 4 gives the
related invariant-ring saturation perspective. Its characteristic-zero
computational discussion is NOT an algorithm for extracting h or F from
a succinct circuit in characteristic p.

This strengthens the rejection of exposed scalar wrappers to arbitrary
degree for this group action. It does not assert an efficient procedure
to discover such a decomposition in an arbitrary public circuit. Nor
does it address general multivariate iteration followed by a scalar
readout, which need not be a scalar postcomposition of an exposed inner
polynomial. Compare the existing, distinct Frobenius and derivative
filters in the [succinct stabilizer audit](SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md).

### Necessary Boundaries

- **Formal polynomials, not functions.** Over F_p, the linear shear
  (x,y)->(x+y,y) does not preserve F=x. With R(T)=T^p-T, R(F) is the
  zero FUNCTION on F_p^2, but not the zero formal polynomial. Its formal
  transform differs by y^p-y. Function equality would invalidate the
  conclusion; evaluating only base-field points is insufficient.
- **Origin-fixing action.** The affine translation x->x+1 preserves
  x^p-x but not x. It is a p-group action, but not linear in these
  coordinates.
- **p-group premise.** In characteristic five, x->-x has order two and
  preserves x^2 but not x. Nontrivial multiplicative characters are the
  obstruction in this example.
- **Nonconstant outer polynomial.** A constant R erases every distinction,
  including a nontrivial linear p-group shear of F=x.

## 3. Exposed Iterated Quadratics Remain Classically Solvable

Consider the proposed family Gamma=UT_5(F_p)^m acting block-diagonally on
D=5m variables, with p>5. Supply an explicit quadratic

```
Q(x) = x^T*B*x + b^T*x + c,      B=B^T,
F_T  = R iterated T times on Q,   R(U)=U^p+U^2.
```

Take T in unary and the composition exposed in the public input. For
degree-two Q, the formal degree is 2*p^T, while repeated squaring gives
a circuit with O(D^2+T*log p) arithmetic gates. Such large degree is
not a hardness argument: the preceding equality gives
Stab_Gamma(F_T)=Stab_Gamma(Q), so the classical algorithm discards the
exposed wrapper.

For completeness, even a fixed extension-field fingerprint can be costed
without expanding F_T. Since |Gamma|=p^(10m), field size at least
2*p^(T+20m)/delta bounds all false orbit collisions by delta using one
fixed random evaluation point and a union bound. This makes the proposed
oracle inexpensive in bit length; it does not remove the following
classical attack on the SAME public input.

Let J be the 10m-dimensional block-strictly-upper-triangular matrix
algebra. It satisfies J^5=0. Solve the linear system for A in J:

```
A^T*B + B*A = 0,      b^T*A = 0.
```

Exponentiate a basis of its solution space to obtain subgroup generators.
The exp/log polynomials truncate after degree four, and all denominators
are invertible for p>5. The exact finite-to-infinitesimal equivalence
does not require the general audit's stronger degree/dimension guard:

1. If g preserves Q, then g^T*B=B*g^-1 and b^T*g=b^T. Applying the
   truncated logarithm gives (log g)^T*B=-B*log g and b^T*log g=0;
   use log(g^-1)=-log g in the nilpotent algebra.
2. Conversely, A^T*B=-B*A implies (A^T)^i*B=(-1)^i*B*A^i.
   The truncated exp identities therefore give
   exp(A)^T*B*exp(A)=B, and b^T*A=0 gives b^T*exp(A)=b^T.
3. The kernel is a Lie subalgebra; the class is at most four, less than
   p. Lazard correspondence identifies its exponential with the whole
   finite stabilizer, and exponentials of a basis generate it.

There are O(m^2) scalar equations and 10m unknowns. Straight dense
elimination costs O(m^4) field operations; input processing and the
truncated exp/log arithmetic remain polynomial in m,T,log p. There is
no enumeration of Gamma, coefficient expansion of F_T, or assumption
p>D. This is a written classical baseline, not a newly implemented
production stabilizer backend. An unexposed arbitrary circuit remains
outside this extraction argument.

## 4. Evidence And Research Decision

Huygens independently reviewed both core deductions and their boundaries,
but executed no tests. The parent ran all15 controls in
[test_constructive_route_filters.py](../tests/test_constructive_route_filters.py)
successfully in3.36s after replacing slow symbolic powering with exact
Frobenius arithmetic. They cover68 native words and4352 ordered lifts over
F8,1418 productive polynomials, the exact corrected law, the n17 ratio,
and1500 formal UT_3 stabilizer comparisons plus premise counterexamples.
Those controls do not establish an asymptotic theorem on their own.

Primary dependencies were checked in the parent investigation, not newly
fetched for this documentation-only assignment. The earlier search route
uses [Sawin, Lemma 8.15](https://arxiv.org/pdf/2102.09730); that search
bound does not supply a uniform sampler. The fiber estimate and its
characteristic-two source are recorded in the earlier norm note. The
scalar closure uses the Arzhantsev--Petravchuk result cited above.

Do not invest in enumerating all norm allocations merely to repair the
old support restriction: the stated uniform full-support proposal is
already rejected by its productive-mass bound. Do not promote an
exposed iterated quadratic because its written degree is exponential:
its formal stabilizer has the explicit classical reduction above.
Neither conclusion settles unrestricted native uniform sampling,
general succinct circuit stabilizers, prior-art novelty, or quantum
advantage. A surviving replacement must change the actual constructive
step and supply its output law and paid classical comparison.
