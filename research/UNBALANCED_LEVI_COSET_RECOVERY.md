# Unbalanced two-block Levi recovery from native coset queries

2026-11-06. Constructive WRITTEN quantum oracle algorithm. Independent
derivation AND actual-note core review accepted; one algebra control complete.
No novelty, non-oracle application, practical speedup or quantum execution
claim. The ambient additive-Fourier mechanism is published prior art.

## Native problem and selection

Public input is a prime p, integers r>s>=1, n=r+s, and coherent evaluation
of a fixed-width classical function f on GL_n(Fp), with the exact promise

    f(x)=f(y) iff x^-1 y belongs to H,
    H=S (GL_r(Fp) direct-sum GL_s(Fp)) S^-1.               (1)

S is unknown. Labels are opaque; only their equality is promised. Output
bases for the ordered complementary spaces U=S(Fp^r+0), W=S(0+Fp^s),
or ABORT. No generators/samples from H, algebra basis, idempotent matrix,
additive-coset oracle or particular coset representative are supplied.
Every oracle call below is on an invertible matrix. Matrix inversion is
public reversible arithmetic, not an oracle inverse.

For p>=128n and0<eta<1 the construction uses O(n log(1/eta)) coherent f calls and
O(n^2 log(1/eta)) total f evaluations, with polynomial(n,logp,label width,
log(1/eta)) other work. Every accepted output is EXACT; ABORT probability
is at most eta. This is a theorem about the stated oracle model. A useful
native non-oracle problem supplying this oracle is not established.

Independent direction selection supplied this operation after the RSK
proposal failed. Corpus been-tried and baselines searches preceded
admission; no exact match was found. The arithmetic/orthogonal comparison
found the apparent alternative already covered by
bundles/orthogonal-general-rank-2026-10-27/RESULT.md. No new arithmetic
uniform-target subset-sum finder was supplied. These comparisons do not
establish classical hardness or priority of the present result.

Primary texts checked: [Ivanyos,1105.4416, Sections3.1--3.3](https://arxiv.org/pdf/1105.4416)
already embeds Borel cosets into the full matrix space and applies its
additive Fourier transform. [DIKQS,1406.6511v2, Theorems1--2](https://arxiv.org/pdf/1406.6511)
treat parabolic and full-unipotent subgroups; their stated input is not
the present block-diagonal group. The actual scope of
[2610.28368v1](https://arxiv.org/html/2610.28368v1) is parabolics over finite
chain rings. These checks found no exact Levi theorem, but are not a
novelty certificate. The new calculation here is the off-diagonal kernel
geometry and its paid composition, using the known ambient-QFT mechanism.

## 1. Exact native Fourier distribution

Define the UNKNOWN algebra A=S(M_r(Fp) direct-sum M_s(Fp))S^-1. It is used
only in the proof. Its units are exactly H. For a_k=product_(j=1)^k(1-p^-j),

    beta=|H|/|A|=a_r a_s >=1-2/(p-1).                    (2)

Use the nondegenerate trace pairing tr(BX). A coordinatewise additive QFT
outputs the dot-product frequency Y; set B=Y^T to obtain this convention.
With Z ranging uniformly over all off-diagonal block matrices,

    A^perp={S Z S^-1 : Z=[[0,C],[D,0]]},
    C in Fp^(r by s), D in Fp^(s by r).                  (3)

For a left coset gH, the virtual subspace gA has annihilator A^perp g^-1.
For its matrix-wise inversion H g^-1, the virtual subspace A g^-1 has
annihilator g A^perp. Never invert a virtual singular-matrix state.

For any frequency in either annihilator, every native coset summand has
phase1. Its exact probability is |H|/p^(n^2). Since there are
p^(n^2-r^2-s^2) such frequencies, their total probability is beta, and
their conditional distribution is uniform. Consequently the ACTUAL
measurement distribution is exactly beta times this uniform law plus a
nonnegative residual law supported outside the annihilator. There is no
unpaid projection onto A or hidden postselection. The algorithm does not
recognize which component produced a frequency.

## 2. Public kernels recover the ordered summands

With probability at least1-2/[p(p-1)], C has full column rank and D has
full row rank: each rectangular rank failure is bounded by
sum_(i=0)^(s-1)p^(i-r) <=1/[p(p-1)], using r-s>=1.
On this event Z has rank2s, and

    ker Z=ker D direct-sum 0,

a uniformly random (r-s)-dimensional subspace of Fp^r+0. For an inverted
coset frequency B=g S Z S^-1, left multiplication by g does not change
the kernel, so ker B is a uniform (r-s)-subspace of U.

For an uninverted frequency B=S Z S^-1 g^-1, take ker(B^T). It is a
uniform (r-s)-subspace of S^-T(Fp^r+0)=W^perp, where the final perpendicular
uses the PUBLIC coordinate dot product. Neither g nor S is computed.

Use r independent samples in each orientation. Reject the attempt if any
frequency has rank different from2s. Span the r kernels to obtain U', and
span the r transpose-kernels to obtain Z'; set W'=(Z')^perp. Require
dim U'=r, dim W'=s, and U' direct-sum W'=Fp^n.

Conditional on full rectangular ranks and the annihilator components,
the sampled kernels are independent uniform t-subspaces, t=r-s>=1.
For any proper current span R, put it inside a hyperplane of its ambient
r-space. The probability that the next kernel fails to enlarge R is at most

    [r-1 choose t]_p/[r choose t]_p
       =(p^s-1)/(p^r-1) < p^-t <=1/p.                  (4)

If each step enlarges an incomplete span, r samples suffice. The two span
failures cost at most2r/p. The2r rectangular rank failures cost at most
4r/[p(p-1)]<=2r/p. The probability that any sample comes from the residual
component is at most2r(1-beta)<=4r/(p-1). Thus an ideal attempt fails with
probability at most

    4r/p+4r/(p-1) <=12r/p <=3/32,                       (5)

under p>=128n. Rejecting by observed rank does not justify treating all
remaining frequencies as clean; the residual-component term pays for them.

## 3. Exact certificate from elementary transvections

Given a complementary candidate pair, form S' from its basis columns.
Compare f(I) with f(S'(I+E_ij)S'^-1) for every i!=j WITHIN each block.
Accept only if every equality holds. These matrices are always invertible.
No primitive element, factorization of p-1 or determinant generator is used.

To prove soundness, let A'=S'(M_r direct-sum M_s)S'^-1. If all tests pass,
all displayed transvections lie in H, hence in A. Their differences from I
give the within-block E_ij. Products E_ij E_ji give diagonal matrix units
in every block of size at least2. Since r>=2, a size-one second-block
projector is I minus the larger-block projector. Thus the associative
Fp-algebra they generate with I is ALL A', proving A' subset A. Both
algebras have dimension r^2+s^2, so A'=A and their unit groups are equal.
The two central primitive summands have distinct ranks r,s, identifying
U'=U and W'=W. Conversely the true pair passes every test.

This proves exact-on-success output even for arbitrary bad Fourier labels.
It is an equality certificate, not just a returned valid subspace.

## 4. Finite source clocks and gate precision

Prepare a uniform matrix and reversibly compute invertibility. Its success
probability a_n>1/2 for the stated primes; after heralding, the matrix state
is uniform on GL_n. Query f and measure its label to obtain a fresh coset.
For the inverted orientation, reversibly invert this ACTUAL matrix state.
All source labels/registers are measured or uncomputed as specified; no
copy is reused and no selected coset can be requested for free.

Take L=ceil(log2(2/eta)) independent attempts, each with2r samples. Cap
each matrix-preparation clock at K=ceil(log2(16rL/eta)) tries. Ideal source
clock exhaustion has probability at most2rL*2^-K<=eta/8. Uniform field
preparation and additive QFTs can use standard approximate prime-modulus
circuits, with their TOTAL full-protocol trace/diamond error bounded by
eta/8; composing the finite instruments pays the error before conditioning.
There are only polynomially many gates/calls, and the required individual
precision has polynomial logarithmic bit cost. Explicitly measure an
entry-range-and-invertibility validity flag before EVERY oracle call:
reject every encoding outside Fp and every singular matrix. This enforces
the oracle domain even under approximate field preparation; ideal valid
states are unchanged. The oracle and classical
verification queries use their exact promised semantics.

On the ideal uncapped process, (5) gives failure at most2^-L<=eta/2.
Adding source-clock and compilation errors leaves total ABORT below eta.
Compilation error cannot create a falsely certified classical candidate.
Arithmetic, rank, nullspace, span, matrix inversion and certificate work
are polynomial in the public parameters. No full algorithm was executed.

## 5. Strong classical comparators and falsifiers

The oracle gives A-membership: for any explicit X find a nonzero t with
det(I+tX)!=0 (at most n roots, and p>n+1), then

    f(I+tX)=f(I) iff X belongs to A.                     (6)

This is a legal classical attack, but not a basis sampler. Uniform A
membership has density p^(-2rs). A stronger structured search samples a
nonzero u and nonzero phi with phi(u)=0, and tests T=I+u phi. Its exact
membership probability is

 [(p^r-1)(p^(r-1)-1)+(p^s-1)(p^(s-1)-1)]
       /[(p^n-1)(p^(n-1)-1)],                           (7)

as u must lie in one summand and phi annihilate the other. For n3,r2,s1,
this is1/(p^2+p+1). Full-label collisions among structured queries may
improve on membership-only search, as the following complete WRITTEN
competitor demonstrates. No optimal classical exponent or new query lower
bound is claimed. Explicit H generators/algebra elements would
enable ordinary commutant/module algorithms; they are not this input.

### A bounded classical collision-and-membership algorithm

Set Q=p^s. Cache f(I). In each of8Q independent trials choose uniform
nonzero v, and draw M=2ceil(sqrt Q) independent uniform rows phi with
phi(v)=0. Query the legal transvection I+v phi and store its label. These
matrices form the abelian group N_v under row addition. Stop at a label
collision between DISTINCT rows; delta=phi_j-phi_i is nonzero and
v delta belongs to A. Otherwise ABORT after the prescribed trial count.

A nonzero rank-one block-diagonal operator is supported on just one block.
Thus a collision gives either v in U and delta in Wperp, a large-block
seed, or v in W and delta in Uperp, a small-block seed. If v is in neither
summand, the restricted oracle is injective and supplies no such collision.

For v in U, the kernel in N_v has dimension r-1 and its label quotient has
Q elements. The probability of a genuine collision is at least

  1-exp[-M(M-1)/(2Q)]-M(M-1)/(2p^(n-1)) >=1/2.          (8)

The last term removes repeated INPUTS, which are not useful collisions.
Pr[v in U]=(p^r-1)/(p^n-1)>=(3/4)/Q, so the probability of missing every
large-block seed in8Q potential independent trials is at most exp(-3).
For v in W, the label quotient has p^r elements. Using M<=3sqrt Q and
Pr[v in W]<=2p^-r, a union bound over all8Q potential trials puts the
probability of ANY small-block seed at most72p^(-2(r-s))<=72/p^2.
This argument accounts for stopping at the first collision.

Given a seed(v,delta), use two independent stages, each capped at8rQ
queries. First draw uniform u in Fp^n, choose t=1 unless delta(u)=-1,
in which case choose t=2, and test f(I+t u delta)=f(I). The determinant
is nonzero in either case. For a large-block seed, acceptance holds
EXACTLY when u is in U. Keep the first r accepted vectors. Second draw
uniform rows psi, use the same t=1/2 rule with psi(v), and test I+t v psi.
For a good seed this accepts exactly Wperp; keep its first r vectors.

Each stage has acceptance probability1/Q and uniform accepted vectors.
Its expected time to r acceptances is rQ; Markov bounds each clock failure
by1/8. Each r-vector spanning failure is at most1/(p-1). Form U' and
W' from these spans, check dimensions/complementarity, and apply Section3's
exact certificate. Wrong seeds can cause ABORT, never a false output.
One full ideal attempt therefore succeeds with probability at least

    1-exp(-3)-72/p^2-1/4-2/(p-1)>2/3.                   (9)

The worst-case query count per attempt is

    16Q ceil(sqrt Q)+16rQ+O(n^2).

Lc=ceil(log_3(2/eta)) repetitions make ideal ABORT<=eta/2. All uniform
coordinate/nonzero-vector rejection draws can be capped with union budget
eta/2 over the explicitly bounded total draw count, preserving exact
uniforms on success. Total queries are
O((p^(3s/2)+r p^s+n^2)log(1/eta)), with this count times polynomial
arithmetic/label overhead; per-star storage is O(p^(s/2)) labels and
their explicit rows. The exponent, table, initialization and bad-seed
costs are charged. This baseline was independently derived and checked by
the parent, not executed end to end. It replaces naive full-group birthday
search as the explicit comparator; it is not an optimality claim.

Likewise a label exposing gPg^-1 for the hidden idempotent P leaks P at
the identity. The theorem supplies no opaque-label implementation from a
hard explicit problem. This SOURCE/APPLICATION requirement remains a
blocker to a non-oracle algorithm, not an implementation task.

One bounded p3,n3 exact control is COMPLETE and parent-inspected in
classical_baselines/levi_coset_fourier_control.py/.json. It checks native
coset Fourier amplitudes, both kernel orientations, residual mass,
classical algebra-membership and the certificate. H is enumerated only
for the diagnostic. Both annihilator laws have exact mass32/81; their
conditional fullrank probability is64/81 and jointmass2048/6561. An
outside frequency has positive mass, retaining the residual component.
Explicit wrong-orientation kernels violate the claimed containment.
Six fixed rank-one membership cases pass; the true certificate accepts
and one wrong complementary pair is rejected. p3 is below the theorem
threshold; no scaling or native recovery follows.
Balanced r=s has generically zero kernels and is outside this algorithm;
small p, other Levi types and applications require new arguments.

## Next hard question

Does an externally motivated explicit input provide this SAME coset oracle
without exposing the decomposition classically? Compare that source
question with independent constructive directions before developing any
extension or compiler. No generic matrix-HSP infrastructure is admitted.
