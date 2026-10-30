# Mersenne Reciprocal: Classical Access And Reduction Audit

2026-10-29. Continues the SAME new relation in
[the research target](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md), not the old
d1 inverse-trace problem. This pass asks whether easy quadratic pieces
actually give a classical sampler or a meaningful reduction. A positive
oracle-relative result reduces APPROXIMATE local Fourier sampling to exact
Walsh evaluation with polynomial query overhead. A subsequent
[carry construction](MERSENNE_CARRY_WALSH_DRAFT.md) now supplies a reviewed
polynomial-time written evaluator and a bounded reference implementation.
This closes the theoretical LOCAL access gap, not native completion.
Its conservative O(n^45) bound is not a practical-runtime claim; no
full-precision native execution has completed. Other deductions remove specific shortcuts and provide a
conditional-completion guarantee. No classical hardness,
novelty, implemented quantum algorithm, or quantum advantage is claimed.

Throughout q=2^n, n is odd, gcd(s,n)=1, d=2^s-1,
F(x)=inv0(x)^d, chi(z)=(-1)^Tr(z), and f_s=Tr(F). The canonical regime
has odd prime n>=17, N=n^2, K=floor(N/8), s=floor((n-3)/4), arbitrary
distinct public points alpha_i, and H[j,i]=alpha_i^j. Public target bits
b_i are unchanged. Native witnesses obey Hx=0 and f_s(x_i)=b_i.

## 1. Easy Quadratic Blocks Do Not Give A Fourier Sampler

Let W(a)=sum_x chi(F(x)+a*x). Balance gives W(0)=0 and Parseval gives
sum_a W(a)^2=q^2. Fourier transforming the normalized uniform accepted
set for bit b gives amplitude

    A_b(a)=(q*[a=0]+(-1)^b*W(a))/(sqrt(2)*q),
    mu_b(a)=1/2*[a=0]+1/2*P(a),   P(a)=W(a)^2/q^2.

Both bits have the same measured distribution; the signs remain important
to coherent use. Uniform local ROOT generation is already efficient and
does not supply the nonzero Fourier branch P.

Set h=2^(s-1) and Q_b(x,v)=v^2+x^h*v+b*x^(2h)+x. The exact lift count is

    m_b(x)=#{v:Q_b(x,v)=0}
          =1+(-1)^b*chi(F(x))-(-1)^b*[x=0].

This last correction is essential: the unguarded lift has exactly one
zero branch for either bit. For fixed multiplier t define the binary
quadratic Gauss block

    G_t(a)=sum_(x,v) chi(t*Q_b(x,v)+a*x).

Summing v uses Tr(t*v^2)=Tr(t^(q/2)*v). At t!=0 it forces
t*x^h=t^(q/2), hence uniquely x_t=t^(-2^(n-s)). Since
t*x_t^(2h)=1, substitution gives

    G_0(a)=q^2*[a=0],
    G_t(a)=q*chi(b+(t+a)*x_t) for t!=0.

Every block is polynomial-time evaluable. But applying character
orthogonality and the zero correction yields

    W(a)=1+sum_(t!=0) chi((t+a)*t^(-2^(n-s))).

The substitution t=x^(-2^s) is a permutation of nonzero field elements
and turns the summand back into chi(F(x)+a*x). Thus the proposed Gauss
reduction merely reindexes the ORIGINAL q-term sum. It has not reduced
its evaluation cost to polynomially many blocks.

### The Missing Interference Has A Paid Cost

Extend x_0=0 and put

    phi_t(a)=q^(-1/2)*chi(F(x_t)+a*x_t).

These q vectors are orthonormal characters with signs. Each alone, and
ANY incoherent mixture of them, has the uniform measurement law on a.
The t=0 vector here is an ADDED zero-extension character, not normalized
G_0, which is supported only at a=0. For t!=0 remove the common (-1)^b
phase from G_t BEFORE combining it with that added vector; otherwise the
b=1 sum would be 2-W(a), not W(a).
The desired distribution instead is

    P(a)=|q^(-1/2)*sum_t phi_t(a)|^2.

In the normalized latent-register state q^(-1/2)*sum_t |t> phi_t,
projection of the first register onto its uniform vector succeeds with
probability EXACTLY1/q and produces P conditionally. Discarding that
probability would conceal an exponential cost. This excludes this
particular projection, not a lower bound on coherent preparation. Indeed,
inverse Fourier transform exposes x_t, the invertible map t<->x_t lets
one erase t coherently, and a final Fourier transform prepares the usual
signed source deterministically. That known quantum construction does
not supply a classical probability sampler.

Even granting an exact Walsh evaluator, the specified uniform proposal
with B=1+2^s*ceil(sqrt(q)) and acceptance W(a)^2/B^2 has expected
B^2/q proposals, by Parseval. In the canonical family that is
Theta(2^(2s)). This is only the cost of that EXACT envelope method.
The approximate sampler below supersedes it once Walsh access is granted;
no all-classical lower bound follows.

## 2. Genuine Polynomial Differential Access, With A Boundary

Trace invariance gives f_s(x)=Tr(x^E), where E=2^(n-s)-1, including zero.
For the VECTOR power function x^E define

    D(c)=#{x:(x+1)^E+x^E=c},
    L_c(X)=X^(2^(n-s))+c*X^2+(c+1)*X.

Multiplying by x(x+1) at x!=0,1 gives L_c(x)=0. Both0 and1 are
always roots of L_c, but satisfy the original derivative equation only
at c=1. Consequently

    D(c)=2^(dim_F2 ker L_c)-2+2*[c=1].

Binary matrix construction and rank compute ONE D(c) in polynomial time
and space. This is the existing linearized-trinomial mechanism of
[Blondeau--Canteaut--Charpin, Theorem1](https://arxiv.org/html/1108.4753v2#S3.SS1),
not a new theorem. The vector power above is trace-equivalent to F, not
identical to F; confusing the two vector derivative tables would be wrong.

The derivative oracle does not yet yield Fourier sampling. With

    C(z)=sum_x chi(F(x)+F(x+z)),

we still have

    C(0)=q,
    C(z)=sum_c D(c)*chi(z^E*c) for z!=0,
    W(a)^2=sum_z C(z)*chi(a*z).

Thus one pointwise rank oracle leaves signed Fourier sums. More precisely,
for an affine frequency space a0+U, with trace-orthogonal complement U^perp,

    P(a0+U)=|U|/q^2 * sum_(z in U^perp) C(z)*chi(a0*z).

These are the conditional masses a sequential exact sampler would need.
No polynomial algorithm for them is supplied by the rank identity alone.
A claimed dequantization must give a positive sampling construction with
its normalization, errors and discarded proposals charged.

### Constant Differential Bound In The Canonical Regime

Write r=n-4s in {3,5} and rho=Frobenius^(n-s). Every root of L_c obeys
rho(x)=c*x^2+(c+1)*x. Four iterations, applying rho to the coefficients
as well as x each time, yield rho^4(x)=R_(4,c)(x), with degree at most16.
But rho^4=Frobenius^r on F_q. If r=3 and c!=0, R_(4,c) has nonzero
degree16 coefficient, so R_(4,c)(X)+X^8 is nonzero of degree16. If r=5,
the degree32 term cannot cancel. For c not in {0,1}, remove the two
extraneous roots to get D(c)<=14 or30 respectively.

At c=0 the kernel is F_2 because gcd(n-s,n)=1. At c=1 it is F_2
because gcd(n-s-1,n)=1 for prime n and s+1<n. Thus D(0)=0, D(1)=2,
and a uniform analytic bound is

    delta=14 if r=3; delta=30 if r=5; D(c)<=delta for every c.

These are upper bounds, not claims about the exact differential spectrum.
The bounded n17 control has observed maximum6, below its bound30.

### Constructive Approximate Sampling Given Walsh Access

Let U(x)=x^E and W_lambda(a)=sum_x chi(lambda*U(x)+a*x). Since U is
a permutation monomial, all nonzero lambda components have the same
Walsh spectrum up to permutation: choose k^E=lambda and scale x by k.
Additive-character orthogonality gives

    sum_(lambda,a) W_lambda(a)^4
      =q^2*(q^2+(q-1)*sum_c D(c)^2).

Subtracting the lambda=0 contribution q^4 and dividing by q-1 yields

    sum_a W(a)^4=q^2*sum_c D(c)^2<=delta*q^3,
    sum_a P(a)^2<=delta/q.

This gives a positive construction, not a lower-bound argument. For an
exact rational 0<epsilon<=1/2 set T=ceil(delta/epsilon), and define

    m(a)=min(P(a),T/q), Z=sum_a m(a), Q(a)=m(a)/Z.

The discarded mass satisfies

    L=1-Z=sum_a (P(a)-T/q)_+
      <=(q/T)*sum_a P(a)^2<=delta/T<=epsilon.

Since P=Z*Q+L*R for a probability law R (unless L=0, when P=Q),
TV(P,Q)<=L, with NO extra 1/Z loss. Draw a uniformly from F_q, obtain
exact W(a), and accept with probability min(W(a)^2,T*q)/(T*q).
This uses exact integer rejection, has acceptance Z/T, and outputs
exactly Q on success. It needs neither Z nor a field-sized table.
Expected oracle calls are at most T/(1-epsilon)=O(1/epsilon).

For confidence kappa>=1 cap the independent trials at

    J=ceil(T*kappa/(1-epsilon)).

The ABORT probability is at most exp(-kappa)<=2^(-kappa). Conditional
on any success before the cap the law is still Q, not P. Including
ABORT as an additional output, total variation from P with zero ABORT
mass is at most epsilon+2^(-kappa). The overhead is polynomial in n,
1/epsilon and kappa; the oracle's entire evaluation cost is additional.
Exact W^2 would suffice; the implementation accepts signed W for existing
controls and checks only shape, magnitude, parity and balance, not oracle
correctness. It requires independent uniform randomness as a premise.

To sample the accepted-root measured law mu_b, first obtain the capped
phase sample, retain ABORT, and AFTER success flip a fair coin between
zero and that sample. Conditional error is at most epsilon/2. This is
only a measured probability distribution: it neither supplies coherent
signs nor solves native parity completion. Product sources require an
explicit combined error budget; per-coordinate error is not free.

The scientific consequence is precise: polynomial exact Walsh evaluation
implies polynomial approximate local Fourier sampling. The reviewed carry
construction now instantiates that implication at the written-algorithm
level, with O(n^45/epsilon) expected evaluator work and O(n^45*kappa/epsilon)
evaluator work under a proposal cap. Exact rational random draws have an
expected polynomial bit cost; a strict clock additionally requires the
random-draw cutoff and extra ABORT allowance in the carry note, Section 10.
This is not practical execution. The reference evaluator's computational
work cap raises an error, unlike the sampler's bounded-probability ABORT.
No exact target sampler, coherent classical simulation, or native classical
solver follows merely by replacing the local oracle.

## 3. Any Accepted Half-Assignment Can Be Completed

For the canonical family, fix any coordinate set I of size t and ANY
accepted values a_i in S_(b_i)={x:f_s(x)=b_i}. There is no assumed hidden
witness. Let M=N-t. The remaining M coordinates have the same distinct
Vandermonde points, now with the explicitly prescribed syndrome

    H_remaining*x_remaining = -H_I*a.

Put beta=min(1,B/q) with the B from Section1, and

    gamma=beta+(1-beta)/q,
    eta_M=min((q^K-1)*beta^(M-K+1), q^K*gamma^M).

For M>K, character orthogonality gives the completion count

    Z_I(a)=q^(M-K)*2^(-M)*(1+epsilon_a), |epsilon_a|<=eta_M.

Here the nonzero dual polynomials have degree<K. Summing their weights
uses the exact positive MDS expression

    sum_(r=0)^(K-1) binom(M,r)*beta^(M-r)*(1-beta)^r*(q^(K-r)-1),

which is bounded by both expressions in eta_M. A nonzero syndrome only
multiplies character terms by unit signs; the same bound holds uniformly.

For n>=17 and s<=(n-3)/4, the rounded gamma obeys

    gamma*q^(1/4)
      <=2^(-3/4)*(1+2^(-n/2))+2^(1-3n/4)<5/8.

Therefore M>=4K implies eta_M<(5/8)^(4K)<1. EVERY accepted assignment
on t<=N-4K=(N+1)/2 coordinates extends to at least one full native
witness. This is an existence/counting theorem, not an efficient
classical method to find the completion.

Let eta_N be the full-fiber bound. A uniform native witness has marginal
on I within eta_M/(1-eta_N) total variation of independent uniform local
roots (clip at1 if needed). Indeed its density relative to that product
law is (1+epsilon_a)/(1+epsilon_total); averaging gives the stated bound,
using eta_N<=eta_M. Accepted partial assignments are never silently
replaced by unconditioned random field elements.

### A Conditional Quantum Completion Guarantee

This existence theorem also supports the already established paid
quantum construction on the residual problem, not only the initial
homogeneous one. Given the actual fixed values, solve for one public
particular vector x0, translate local roots by -x0, and charge this
linear solve, translation and its Fourier phase. Complete decoding is
on the M-coordinate dual Reed-Solomon code with dimension K.

At the boundary M=4K choose w=2K. Then

    (M-w)^2-M*(K-1)=M>0,
    tau=2^(-M)*sum_(j<=w) binom(M,j)>=1/2,
    list cap=K+1, P=next_power_of_two(K+1).

The exact predicate-channel law gives ideal native completion probability
at least (1-eta_M)*tau^2/P, hence order1/K rather than exponentially
small. Conditional successful output is uniform over completions of the
FIXED assignment. A constant-mass truncated source is legal here because
the exact channel identity and native verification retain all rejection
costs; a small-tail approximation is not being silently invoked.

This is an ideal polynomial-time conditional extension of existing
machinery. Clean source preparation, complete reversible list decoding,
one public padding size, erasure and implementation precision remain
charged premises. No residual decoder or circuit is implemented here.

### Consequence For Reductions

Even allowing all remaining coordinates as auxiliaries, one cannot
enforce a proper relation on up to(N+1)/2 designated coordinates beyond
their individual accepted-set membership: the projection is their
ENTIRE Cartesian product. This rules out pinning a field value within
its accepted set, equality wires, or nontrivial arithmetic gates through
such coordinate projections. Other bits and points may be chosen
adaptively as part of the instance; the conclusion holds for every
valid final instance. Count ALL fixed coordinates, including pinned
auxiliaries, in t; do not recompute K after removing them or add extra
constraints absent from the native relation. Arbitrary global witness decoders and nonlocal
encodings are outside this obstruction.

The exact useful coding equivalence is narrower than general list
recovery. Let A(T)=product_i(T-alpha_i), h_i=A'(alpha_i). Then

    Hx=0 iff x_i=P(alpha_i)/h_i with deg P<N-K.

Lagrange interpolation makes this a bijection, preserving uniform
witness distributions and failure flags. The lists are the succinct sets
h_i*S_(b_i), equivalently

    Tr(h_i^d*inv0(P(alpha_i))^d)=b_i.

Straightforward conversion costs O(N^2+N*n) field operations, with field
bit costs charged. The rate is about7/8, each list has density1/2,
and its multiplier is determined by the evaluation points. This is NOT
a reduction from arbitrary list recovery or Reed-Solomon decoding.
[Guruswami--Vardy's decoding hardness reduction](https://www.cs.cmu.edu/~venkatg/pubs/papers/mldrs.pdf)
has different degree/redundancy parameters, a nonzero target syndrome
and a weight condition; those cannot be replaced by these fixed
half-field predicates without an actual reduction. In particular,
unproved value-pinning gadgets do not fix that mismatch.

## 4. Why The Old Rational Conic Identity Cannot Transfer

There is an explicit elementary countercontrol. For odd n,

    R(t)=1/(t^2+t+1)

is finite, nonzero and accepted by f_1 for EVERY t in F_q. The new
predicate rejects it already at n17,s3,t6, where R(t)=39667 in the
recorded polynomial basis. The old norm construction cannot use its
trace identity unchanged.

A stronger statement applies to nonconstant rational R of map degree D,
not to all small arithmetic circuits. For d>=3 the base curve

    y^2+y=x^(-d)

has positive genus (d-1)/2. Its pullback by x=R(t) is geometrically
connected: geometric splitting would give a nonconstant rational map
from the projective line to a positive-genus curve, contrary to
[Luroth's theorem, Milne Theorem9.19](https://jmilne.org/math/CourseNotes/FT.pdf),
including inseparable maps. Reduce the pullback poles modulo
Artin-Schreier differences. Their orders sum to at most dD, there are
at most D geometric poles, and its genus G obeys

    2G <= (d+1)*D-2.

These pole/genus and Weil ingredients are standard; see
[Carmon, Section3](https://arxiv.org/html/1409.3694v1#S3).
Let T be the finite parameters where R is finite and nonzero. At most
E<=2D+1 points of the projective base are excluded. Counting the smooth
degree-two cover over T, including the possible omitted fibers, gives

    |sum_(t in T) chi(R(t)^(-d))| <=2G*sqrt(q)+E.

If EVERY parameter in T has the same target bit, then |T|>=q-2D gives
the following weaker necessary bound:

    D >= (q-1)/((d+1)*sqrt(q)+4).

For the canonical s this grows as q^(1/4). Thus a polynomial-DEGREE
rational all-accepted family cannot replace the old genus-zero identity
asymptotically. This does not exclude isolated good parameters, adaptive
choice of coefficients, large-degree power maps evaluated by small
circuits, or a factorization algorithm that constructs one point directly.
The already efficient finite-field root bijection is not a contradiction:
its rational-map degree is large. No generic norm-factorization impossibility
or classical hardness is asserted.

## 5. Decision And Next Decisive Task

Retain the relation for bounded constructive triage, not promotion.
The positive constructions are a polynomial differential rank oracle,
approximate Fourier sampling REDUCED TO exact Walsh evaluation, and a
conditional-completion guarantee. None solves native classical sampling.
The elementary quadratic-source, low-degree rational
identity, and coordinate-gadget shortcuts do not establish the desired
algorithm or relevance.

The local Walsh task is now closed at the reviewed-construction level.
The next useful construction must charge what remains: choose target-adaptive
auxiliary values satisfying global parity; solve the quartic partial-norm
system without changing H; establish that a dequantization theorem transfers
this local sample/query access through the actual coherent decoder and
postselection; or provide a genuinely nonlocal reduction from a meaningful
problem. Local sampling alone is not an end-to-end dequantization theorem.
A [subsequent independently reviewed deduction](MERSENNE_GLOBAL_FOURIER_ACCESS.md)
now samples the complete-list coalesced Born law in polynomial time at the
written-construction level, retaining signed cancellations. The remaining
unresolved operation is the FINAL inverse-Fourier output, not list-sum
sampling itself. This is still not an implemented native classical solver.
Do not replace those missing steps with another exponent sweep, more
small successes, or an all-classical hardness claim.

## 6. Executable Scope

`theorems/mersenne_reciprocal_access.py` provides polynomial pointwise
differential counts, individual quadratic Gauss blocks, the explicit
oracle-relative clipped sampler, partial-completion certificates, and a
capped full-field Walsh reference. Its report is reproduced with:

```sh
python -m theorems.mersenne_reciprocal_access --output research/classical_baselines/mersenne_reciprocal_access.json
```

The n17 Fourier/differential reference is EXPONENTIAL in field degree,
including its table construction. It checks exact normalization, the
fourth-moment identity, clipping and spectrum hashes, not an asymptotic
algorithm. The n17/31/61 completion and oracle-query bounds use exact
rational arithmetic with outward rounding on serialization. The report
binds source hashes and never treats the reference table as polynomial
Walsh access. Automated adversarial reviews checked the deductions;
no human peer review or proof-assistant certification is claimed.
