# Inverse Trace: A Polynomial-Norm Classical Attack

28 October 2026. Proposed mathematical deduction from a published uniform
distribution bound, with exact native witnesses and a completed independent
automated adversarial review. Not a human-reviewed theorem, novelty claim, uniform
sampler, or quantum algorithm. This is a classical falsifier, not a reason
to promote the quantum candidate.

## Decision

The all-one prime-degree search instances are no longer supported merely
by failed SAT or affine attacks. A constructive norm route returns a native
word on the SAME n17 instance that the preceding SAT run left UNKNOWN.
More importantly, an explicit published bound supplies a checkable success
certificate uniform in the public evaluation points, not just a heuristic
about random polynomial factorization.

The deduction covers every input passing that integer certificate. It
also gives expected polynomial-time SEARCH asymptotically when the number
of one-target positions is at least 3K+3 in the native family. It does NOT
give a uniform sampler, solve all sparse-one target patterns, or turn the
current seeded/finite-cap implementation into a hard-clock algorithm.
The mathematical algorithm uses fresh uniform random bits and standard
expected-polynomial finite-field factorization. The implementation records
these distinctions explicitly.

## Input And Support Restriction

Keep q=2^n with odd n, N=n^2, K=floor(N/8), arbitrary distinct public
alpha_i, and the original relation

```
sum_i alpha_i^j x_i = 0,  0 <= j < K,
Tr(inv0(x_i)) = b_i,      inv0(0)=0.
```

Let S={i:b_i=1}, m=|S|. We set x_i=0 outside S. This is a declared
restriction, not a new promise that the other coordinates are unavailable.
It succeeds on a useful input class but can lose valid answers elsewhere.
All-zero targets have the immediate zero solution. The implemented
progression branch requires m>=2K+2 and m<q; failure of either guard is
NOT an unsatisfiability result. The theorem below is more conservative.

Put beta_i=sqrt(alpha_i) on S, and form

```
P(X) = product_(i in S) (X-beta_i),  D=P',  R=D^2 mod P,
d = 2(m-K-1),   u=d-m=m-2K-2.
```

P is squarefree and gcd(D,P)=1. Draw a uniform MONIC degree-u polynomial T,
and set F=R+P*T. This is exactly the uniform distribution on monic degree-d
polynomials congruent to R modulo P. No original point, target, or hidden
witness is resampled. The n17 all-one input has m289,K36,d504,u215.

## Norm Factorization Gives A Codeword Family

Take rho satisfying rho^2+rho+1=0 in F_(q^2). Odd n ensures this polynomial
is irreducible over F_q and conjugation sends rho to rho+1.

A nonzero F in F_q[X] is a norm from F_(q^2)[X] exactly when every
odd-degree irreducible factor has even multiplicity. Indeed, odd-degree
irreducibles stay irreducible in the constant quadratic extension; even
degrees split into two conjugate factors. Split multiplicities of the
former in half and choose one member of each latter pair. The leading
coefficient has a square root in F_q. This constructs h=B+rho*A with

```
h*bar(h) = B^2+A*B+A^2 = F,
max(deg A,deg B) <= d/2 = m-K-1.
```

The code verifies this exact base-field identity. It constructs an explicit
embedding of the ORIGINAL polynomial-basis F_q into F_(q^2), including the
inverse binary basis map; it does not confuse two field encodings or
enumerate either field. FLINT supplies polynomial factorization.

Define a_i=A(beta_i)/D(beta_i), b'_i=B(beta_i)/D(beta_i). Lagrange
interpolation gives sum_i beta_i^j a_i=sum_i beta_i^j b'_i=0 for j<K:
each numerator degree after multiplying by X^j is at most m-2, so its
X^(m-1) interpolation coefficient vanishes. The norm congruence gives

```
(b'_i)^2+a_i*b'_i+a_i^2 = 1.                              (1)
```

For a public parameter t, set

```
Q(t)=t^2+t+1,
x_i(t)=(a_i*t+b'_i)^2/Q(t), i in S;   x_i(t)=0 otherwise. (2)
```

The parity equations follow by SQUARING the two beta-code identities;
using alpha instead of beta when constructing the code would be wrong.

For the trace condition, first suppose a_i!=0 and put L=a_i*t+b'_i.
By (1),

```
Q(t)/L^2 = 1/a_i^2 + 1/(a_i*L) + 1/(a_i*L)^2.
```

Also (1)/a_i^2 says
1/a_i^2=(b'_i/a_i)^2+(b'_i/a_i)+1, whose trace is one. The other two
terms have trace zero together. If a_i=0, then b'_i=1 and Tr(Q(t))=1.
Thus every nonzero L gives the REQUIRED target-one value.

Q has no base-field roots. Each L forbids at most one parameter, and
(1) prevents L being identically zero. Testing any m+1 distinct field
values therefore finds a legal t. This paid deterministic scan matters:
totalizing an inverse at a forbidden L would output an invalid zero.
Finally, the existing independent verifier checks ALL original equations.

## A Uniform Success Bound, Not A Random-Polynomial Heuristic

Import [Sawin, Lemma 8.15, pages 67-69](https://arxiv.org/pdf/2102.09730).
For squarefree degree-m modulus, d>=m>=2, and a coprime residue, it bounds
the von Mangoldt sum's deviation from its coprime average by

```
E = A0*q^((d-m)/2) + B0*q^((d+1-m)/2),
A0 = sum_(r=0)^(m-2) 2^(m-1-r) binom(d+m-r,2m-r),
B0 = 2^(m-1) binom(d+m,2m-1).
```

This primary statement has no odd-characteristic condition or unknown
degree-dependent big-O constant. Here P splits into m distinct linear
factors, so phi(P)=(q-1)^m and its coprime Mangoldt average is
(q^d-m)/phi(P): exactly m excluded linear prime powers contribute one each.
The implementation uses this explicit inequality, NOT only the paper's
asymptotic introduction. The imported algebraic-geometric proof is not
reproved or formally verified in this repository.

Our key consequence: EVERY prime power of EVEN total degree d is a norm.
If its prime factor has odd degree, its exponent must be even. Consequently
the number of accepted F is at least the Mangoldt sum divided by d, since
each Mangoldt value is at most d. There is no need to discard prime powers
or assume a squarefree F. The number of trial polynomials is q^(d-m).

Use integer ceilings for the two square roots and compute

```
E_scaled = m + (q-1)^m *
  (A0*ceil(sqrt(q^(d-m))) + B0*ceil(sqrt(q^(d+1-m)))).
```

If 2*E_scaled<=q^d, then a fresh uniform trial succeeds with probability
at least 1/(2d). Expected trial count is at most 2d. A cap of 2d*B trials
has failure probability at most exp(-B)<=2^(-B). This pays for failed
polynomials; a certificate failing its guard is inconclusive, not hardness.
Factorization and field construction costs remain paid separately.

At n17,m289,K36 the integer guard passes, yielding the conservative bound
1/1008. It is not inferred from the observed success on trial48. Earlier
Bank--Bary-Soroker--Rosenzweig fixed-degree equidistribution alone would
not justify this growing-degree conclusion.

## Asymptotic Dense-Target Consequence

For native n>=31 and m>=3K+3, u>=m/3 and d<2m. Bound each of the m
terms in A0+B0 by 2^(d+2m-1). Thus 2(A0+B0)<=m*2^(4m), and using
ceil(sqrt(q^v))<=2*q^(v/2) gives

```
E_scaled/q^d <= m*2^(-n*d) + m*2^(4m-n*(u-1)/2).
```

Here m>=3n^2/8, m<=n^2 and log2(m)<=n/2. The second term is at most
2^(-7m/6+n) for n>=31, and the first is smaller than 1/4. The second is
also below 1/4, so the exact half-main-term guard holds throughout this
regime. Each field operation, polynomial degree, coefficient bit length,
root-avoidance scan, and expected number of trials is polynomial in n.
With standard expected-polynomial factoring this is an expected-polynomial
CLASSICAL SEARCH algorithm on this input class. Smaller cases may already
pass the exact guard; n17 does.

For ALL-ONE targets there is a sharper clean threshold: every odd n>=11.
Here m=n^2, d=7(n^2-1)/4. Bounding successive summands by a geometric
series gives A0<(4/3)*2^(d+2m-1), B0<=2^(d+2m-1). The second relative
error term is at most (7/3)*2^E, where
E=(-3n^3+30n^2+11n-14)/8. At n11, E=-32; its derivative is negative
thereafter. The first term m*2^(-nd) is smaller still. Thus the guard
passes uniformly in every distinct point set, without finite extrapolation.

Under independent uniform target bits and n>=31, 3K+3<=0.4N. A standard
binomial Chernoff bound gives Pr[m<3K+3]<=exp(-N/100). Thus the route also
covers almost all such target patterns for EVERY distinct point set.
This is an input-distribution statement, not an assertion that the OUTPUT
is uniformly distributed on the native solution set.

In fact, if any target is zero, this output always has a zero in that
position. The earlier [conic review's fiber count](independent_review_2026_10_22/CONIC_REFORMULATION.md)
bounds the same event under a uniform native witness by
(2/q)*(1+eta_(N-1))/(1-eta_N), when that count bound applies. The output
can therefore be nearly maximally far from uniform. This is a deliberate
search restriction, not a nearly uniform sampling method awaiting cleanup.

## Whole-Family Output Law And An Efficient Distinguisher

The all-one case has a stronger obstruction, even though the preceding
zero-coordinate event is unavailable. This covers ALL pairs a,b in the
beta-code satisfying b_i^2+a_i*b_i+a_i^2=1, not just the implemented monic
progression, selected factor allocation, seed, or public parameter scan.

Write L=N-K-1, d=2L and suppose d>=N. The map
A -> (A(beta_i)/D(beta_i)) from degree-at-most-L polynomials onto the
beta-code is bijective: interpolation gives containment, evaluation is
injective, and both spaces have dimension N-K. Thus every pair determines
a polynomial norm F=B^2+AB+A^2 of degree at most d, with F=D^2 mod P.
There are exactly q^(d-N+1) such candidate F, including nonmonic and
smaller-degree polynomials. None is zero, since gcd(D,P)=1.

For a fixed F, an odd-degree prime factor must have even multiplicity,
then its norm allocation is forced. A degree-2e prime of multiplicity v
has v+1 allocations between its conjugate factors. The leading unit has
q+1 norm preimages. Therefore the number of pairs over any F is at most

```
(q+1) * product_(even-degree factors f) (multiplicity(f)+1)
  <= (q+1) * 2^(deg(F)/2) <= (q+1)*2^L.
```

Do NOT multiply by q+1 again for the projective parameter. For finite t,
put s=sqrt(t^2+t+1). Norm-one multiplication gives another valid code pair

```
a' = ((1+t)*a+t*b)/s,   b' = (b+t*a)/s.
```

Its t=0 output b'^2 is exactly the old output x(t). At infinity use
(a',b')=(a+b,a). Thus every output occurs at t=0 already. Other trace-one
conic constants c do not enlarge the family either: c=1+u^2+u, and the
changes b -> b+u*a and t -> t+u reduce them to c=1.

Let S_norm be this entire valid output set. Then

```
|S_norm| <= (q+1) q^(N-2K-1) 2^(N-K-1).
```

The existing exact MDS/character-sum bound gives native fiber size at least
(1-eta)q^(N-K)/2^N when eta<1. The character input is the genus-one
Kloosterman bound; [Carmon's characteristic-two curve theorem](https://arxiv.org/html/1409.3694v1#S3)
supplies the underlying Weil estimate. The curve for a*x+1/x has two
rational ramified points over its poles, yielding the usual 2*sqrt(q)
bound on the sum over nonzero x. Totalizing inv0 contributes the extra 1.
The implementation uses (1+2*ceil(sqrt(q)))/q and exact rational arithmetic.
Consequently

```
Uniform_native(S_norm) <=
  (q+1) q^(-K-1) 2^(2N-K-1)/(1-eta).
```

For ANY output distribution supported on S_norm union {ABORT}, its total
variation distance from uniform native witnesses is at least one minus
this mass. Rejection, arbitrary biased norm sampling, adaptation and
mixtures do not enlarge support. This includes conditioning on success.
Postprocessing which leaves S_norm and other classical samplers are NOT
covered. Exact conservative dyadic bounds at n17,n31,n61 are respectively
`2^-70`, `2^-1918`, `2^-21388`; these are not floating-point extrapolations.

There is also an exact deterministic polynomial-time membership test.
For a VALID native all-one word x, set b_i=sqrt(x_i). Squaring shows that
b belongs to the beta-code. Every possible t=0 lift is

```
w_i = 1/x_i+1,
z_i = HT(w_i) = sum_(j=0)^((n-1)/2) w_i^(2^(2j)),
a_i = b_i*z_i + epsilon_i*b_i,   epsilon_i in F_2.
```

Because Tr(w_i)=0, HT(w_i)^2+HT(w_i)=w_i; these are exactly the two roots,
not a subset. Code membership becomes an nK-by-N BINARY linear system
M*epsilon=r. A consistent system gives the complete lift a. An inconsistent
one gives a dual certificate lambda with lambda^T*M=0, lambda^T*r=1.
The certificate verifier reruns no solver. No field table, parameter
enumeration, or exponential root-choice search occurs. M*1=0, so every
positive lift has the distinct partner a+b; a unique lift would be a bug.

The independent automated reviewer checked the count, parameter absorption
and membership equivalence. Parent controls exhaust all 68 native words
in a GF(8) six-coordinate case: 62 are in the family and 6 are outside,
matching direct enumeration of ALL local lifts. This is a correctness
control, not an asymptotic experiment.

On the SAME n17 native instance as the previous SAT and norm reports, the
existing dimension-three flat solver (fixed seed1030) returns a verified
word OUTSIDE the entire norm family. The report retains the original input,
all flats, binary system, word and negative dual certificate. The norm word
has a positive certificate. Both membership matrices have rank288 out of
289 variables and 612 equations. The flat result is finite evidence only:
no general flat full-rank bound or near-uniform output law has been proved.

## Sparse Targets: Exact Remaining Problem And A Failed Extension

A separate constructive investigation did not find a sparse-target solver.
It did establish that arbitrary completion is not an existence obstruction.
For odd n>=7 and m<=3K+2, fix every one-target coordinate to x_i=1. Let Z
be the zero-target coordinates, ell=|Z|>=5K-1, and
s_j=sum_(i notin Z) alpha_i^j. Every such fixed choice admits a completion:
the all-syndrome character bound has relative error at most

```
q^K (3/sqrt(q))^(ell-K+1) <= (81/q)^K < 1.
```

This proves existence uniformly in the original points, NOT a procedure
for finding the completion. The parametrization x=z+z^-1, z nonzero,
covers exactly the zero-target alphabet, including x=0 at z=1. Thus the
missing constructive problem is

```
sum_(i in Z) alpha_i^j (z_i+z_i^-1) = s_j,   0<=j<K.
```

Equivalently, for P_Z=prod_(i in Z)(X-alpha_i), D_Z=P_Z', find U,V of
degree less than ell satisfying UV=D_Z^2 mod P_Z and prescribed Laurent
tail (U+V)/P_Z=sum_(j=0)^(K-1) s_j X^(-j-1)+O(X^(-K-1)). Splitting an
arbitrary polynomial does not enforce this tail. Calling that missing
step a routine would simply rename the unresolved coupled solver.

One natural nonconstant-norm extension is specifically falsified. Interpolate
the target bits by B(alpha_i)=b_i and Artin-Schreier-reduce B to C=B+G^2+G
of odd degree 2g+1. The local traces are unchanged. Consider norms
F=U^2+UA+C*A^2, with deg A<=r=N-K-1, in Y^2+Y=C. For monic degree
d=2r+2g+1 and g>=K, uniform trial polynomials F=D^2 mod P are accepted
with probability at most

```
Pr[polynomial norm] <= 2^N q^(-g).
```

Proof: even/odd leading degrees cannot cancel, so deg A=r with its leading
coefficient fixed, and deg U<=r+g. There are q^r choices of A; at each
point the quadratic for U has at most two roots; each of the at most 2^N
residue tuples has q^(g-K) polynomial lifts. Divide this upper count by
the q^(d-N) trial polynomials. A norm oracle would not fix the rejection
probability, and inert-prime tests alone are not polynomial principality.

There is an explicit native singleton-target counterfamily: polynomial-basis
points alpha_i=i, 0<=i<N, with b_0=1 and all other targets zero. Here
B=P/(X*D(0)). Its X^(N-2) coefficient is nonzero because the binary XOR
of 1,...,N-1 equals N-1 (N=n^2=1 mod8). Reducing the leading even degree
cannot change this highest odd term. Therefore g=(N-3)/2. At n17 this
gives g143,d791 and trial success at most `2^-2142`. Exact polynomial and
trace controls reproduce the premises at n5 and n17. This rules out that
particular rejection strategy, not all nonconstant norms or sparse search.

Follow-up deductions preserve this native problem rather than requiring an
arbitrary-syndrome solver. The [affine singleton classification](INVERSE_TRACE_SPARSE_POLYNOMIAL_FILTER.md)
constructs a witness exactly when its centered-moment criterion holds; its
exclusion certificates concern only that polynomial family. The
[split-norm filter](INVERSE_TRACE_SPARSE_SPLIT_FILTER.md) rules out monic
maximal-degree proposals for an odd number of fixed one-sites and bounds
the repaired singleton proposal law. Local formal lifting is not global
factor reconstruction. The [ray-class audit](INVERSE_TRACE_RAY_CLASS_SCOPE.md)
reformulates the exact remaining selection task and shows why ordinary
principality and the direct multiplicative-syndrome HSP invocation do not
solve it. None of these establishes a general sparse solver or sampler.

## Attempts To Break It And Remaining Scope

- Omitting the square-root point change fails the parity argument.
- Arbitrary F need not be a norm; all rejected trials remain charged.
- A full field-table embedding would be exponential; the implemented
  embedding uses polynomial degree roots and binary linear algebra.
- A norm identity without its degree bound does not place residues in
  the code. Both are checked before using a certificate.
- A zero numerator at a one-target position is invalid; the scan excludes
  it, with a regression requiring two excluded parameters before success.
- Fixed-degree equidistribution and an opaque O_d constant cannot certify
  the native growing-degree regime. The explicit Sawin inequality is vital.
- Random(seed) fixtures are reproducible probes, not mathematical IID
  guarantees for their deterministic streams. FLINT randomness and total
  wall time are not capped by the outer polynomial-trial limit.
- Sparse-one patterns outside the guard may still have native solutions
  using nonzero zero-target coordinates. No general impossibility follows.
- The construction is a biased search procedure. Uniform sampling and the
  remaining quantum sampling proposal are not dequantized by this proof.
- No novelty is claimed for norm splitting, RS residues, conic identities,
  or the imported analytic theorem. The repository's odd-prime norm attack
  was a useful precedent but did not solve this characteristic-two relation.

## Replay And Status

The independent reviewer checked the construction, the primary lemma's
hypotheses and constants, the prime-power observation, and the n17 integer
guard. No mathematical counterexample was found. The reviewer did not
verify the live witness or certify novelty; the parent recomputed the
original witness checks. The review also obtains the stronger all-one
threshold n>=11 by bounding the geometric sum in A0. The conservative
dense-target theorem above does not rely on that sharper threshold.

Initial controls, input seed1028 and polynomial seed1029, before the
output-law and optional flat-comparison extension:

| Input | Result | Trials | Time | Analytic lower bound |
| --- | --- | ---: | ---: | --- |
| n5, all ones | Verified native word | 2 | 0.035s | Inconclusive |
| n17, all ones | Verified native word | 48 | 95.59s | 1/1008 |
| n17, independent random targets (146 ones) | Verified native word | 20 | 9.51s | 1/436 |

Times are finite observations, not a controlled scaling study. The all-one
n17 digest is `9a909ce6e7afc2a5668da53fa183efa7a137bec1e744c71b657df9ac9f54fcff`,
identical to the prior SAT input. No claim that SAT decided it unsatisfiable
was made or is being reversed.

```
python qsearch.py inverse-trace-norm --bits 17 --compare-flat-dimension 3 --flat-seed 1030 --write --output research/classical_baselines/inverse_trace_norm_n17.json
python qsearch.py inverse-trace-norm --bits 17 --target-mode random --write --output research/classical_baselines/inverse_trace_norm_n17_random.json
```

Use --input for a standalone original-instance JSON, not a solver report.
Successful reports retain P,D,R,T,F,A,B, the chosen parameter, original
instance/digest, and the full checked word. Failed trials retain their
factor degrees, T digests, seed and elapsed times. The live n5 control
uses the same independent verification and has no analytic guarantee from
this conservative bound. Registry claims are not automatically promoted.

The sampling-audit pass regenerated all three reports and replayed their
original words, polynomial certificates, output-law bounds, and applicable
positive/negative membership certificates. The saved flat witness also
passed the separate binary-arithmetic native verifier. The connected
12-file selection passed 356 pytest cases in 42.42s; six Python syntax
checks, all 12 existing site JavaScript syntax checks, registry validation
and tracked whitespace checks passed. This is not a full-repository test,
new Lean build, human review, or quantum-advantage claim.
