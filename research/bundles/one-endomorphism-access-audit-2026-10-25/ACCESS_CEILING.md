# Where The Full-Rank Input Matters

2026-10-25. Adversarial scope audit and exact algebraic countercontrols.
This is NOT a no-go theorem for quantum isogeny algorithms, a native hardness
result, or an independently reviewed proof. It blocks particular transfers
of the preceding full-rank-suborder construction to a weaker input.

## Research Decision

Keep the proposed full-rank source as a possible heuristic-removal result,
pending review of its complete geometry. Do not call it a solution from a
bare supersingular curve or one known endomorphism. Further product copies
or natural Frobenius arrows do not supply the missing algebraic information.
The next genuinely higher-ceiling task is a NEW way to remove the remaining
quadratic ambiguity, not another full-rank supplied-map example.

The comparison is substantive: the published one-endomorphism route has
GRH-conditional quantum subexponential complexity in the quadratic
discriminant, whereas the preceding full-rank problem already has a published
heuristic quantum polynomial-time algorithm. These are different input
promises, not interchangeable benchmarks.
[One-endomorphism paper, Theorems 1.1-1.2](https://arxiv.org/html/2309.11912v4)
and [full-rank paper](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/259384467/suborder_to_endomorphism_ring_2_.pdf).

## 1. The Local Ambiguity Is A Torus, Not A Scalar

With the full quaternion action, simultaneous intertwiners form a
one-dimensional space, giving precisely the harmless scalar ambiguity.
With only a nonscalar alpha, if T intertwines its two torsion actions then
every solution has form T*C with C in the centralizer of alpha. At a good
prime r the centralizer algebra is the TWO-dimensional F_r[alpha]. Its
invertible elements modulo scalars have size

    r-1 if the quadratic polynomial splits with distinct roots;
    r+1 if it is irreducible.

At repeated-root primes the nonscalar Jordan case instead has r projective
units; a scalar reduction has a four-dimensional commutant. Tests retain
these boundaries. A one-dimensional uniqueness check MUST reject this input,
not choose the first local solution and reuse the full-rank proof.

For a source Gram matrix S on t copies, replace T by T*C in its transport.
The result is unchanged for all C precisely when S commutes with the
diagonally repeated centralizer. At good odd primes this forces

    S in M_t(F_r[alpha]).

Thus local normalization is not enough to transport arbitrary noncommuting
source queries. Independent choices at different primes are not evidence
for one global isogeny. Even knowledge of the isogeny degree does not fix this.

### Same-degree genuine endomorphism countercontrol

In the known characteristic-11 maximal order let j^2=-11 and h=(1+j)/2.
The maps h and 1-h are integral primitive endomorphisms of degree 3. Both
commute with the SAME known h, but their degree-three kernels differ. They
are not scalar multiples on the tested auxiliary torsion. Their transports
of the transverse source operator i differ.

More directly, use the actual integral automorphism sigma=[[1,6i],[0,1]]
of E0^2. Its Gram matrix is I modulo 6. Transport through h x h or
(1-h) x (1-h) gives two DIFFERENT integral Gram operators, both with
integral (H-I)/2. The problem is not a malformed polarization or a bad norm
certificate. The weaker input really leaves a choice the old proof removed.
The source and maps are supplied controls, not a hard unknown-instance claim.

## 2. A Primitive Map Is No Longer Unique Or Uniformly Bounded

The full-rank proof used a one-dimensional rational intertwiner space. Its
intersection with Hom gives one primitive map up to sign and the degree
envelope D|p*m. For a quadratic input the rational intertwiner space has
dimension TWO. There is no analogous single primitive generator.

For the SAME fixed h above, every h^k is an integral map commuting with h,
of degree 3^k. It is primitive: its norm has only the prime factor 3, and
h modulo 3 is a nonzero idempotent since h^2-h+3=0. Hence h^k is not zero
modulo 3 and cannot be divisible by [3]. No other integer prime can divide
it by its norm. The input h does not change as k increases.

This falsifies a bound on EVERY primitive intertwiner obtained just from
that fixed quadratic input. It does NOT disprove existence of a small
representative, ideal-class bounds, or an algorithm selecting one; those
are different obligations. In this deliberately explicit control, identity
is a small representative. Promoting local choices to such a representative
without an algorithm is exactly the forbidden shortcut.

An upper bound B on an unknown degree alone also does not reproduce the
source's known multiple m. Using lcm(1,...,B) to cover all possible degrees
has bit length Theta(B), exponential when B is exponential in input bits.
No lower bound against cleverer denominator control follows from this fact.

## 3. Stabilization Preserves The Missing Algebra

Let K=Q(alpha) inside the quaternion algebra. From alpha, its adjoint,
addition, composition, all product projections/inclusions and scalar matrix
units on t copies, one generates M_t(K), of rational dimension 2*t^2.
The full endomorphism algebra is M_t(B), of dimension 4*t^2. Its commutant
of the known algebra is the diagonally repeated K, still dimension two.

Adjoints add nothing: alpha^dagger=Tr(alpha)-alpha is already in K.
Allowing rational inverses of invertible known elements also stays in K.
Therefore more copies, by these operations alone, cannot provide the full
rank action required by the previous transcript extractor. This is an
algebraic closure statement, NOT a prohibition on geometric quotient
algorithms that might produce genuinely additional maps.

Exact local controls for t=1,2,3 and r=3,5,7 give dimensions 2*t^2 and
commutant dimension two. A genuinely noncommuting second operator instead
generates the full local M2 and reduces the commutant to scalars. Locally
bad primes must still be checked even when the rational pair generates B.

## 4. Natural Frobenius Arrows Do Not Double The Information

For generic E, p-Frobenius F goes to E^(p), NOT back to E. On E x E^(p),
the correctly typed known endomorphism is diag(alpha,alpha^(p)), with

    F alpha = alpha^(p) F.

Adjoin both product projectors, the off-diagonal F arrow and its dual.
At an auxiliary prime r!=p, change coordinates by diag(I,F). The known
algebra becomes M2(K_r): the twisted diagonal becomes diag(alpha,alpha),
and the arrows become scalar matrix units, one multiplied by p. The same
rational argument applies using quasi-isogenies. Its dimension is eight,
not the full sixteen, and the residual commutant is two-dimensional.

This rejects treating alpha and alpha^(p) as independent endomorphisms of
the SAME curve without a paid isomorphism. The matrix controls use a known
characteristic-11 Frobenius action, not a generic native geometric instance.

Important exception: if E already has a known identification with E^(p),
for example a model over F_p, Frobenius may be a known diagonal endomorphism.
If it genuinely fails to commute with alpha, then it DOES give the missing
operator. That stronger input is not ruled out here. For alpha itself equal
to Frobenius, merely repeating it still adds no information.

## 5. The Gram-Invariant Set Is Not Automatically An HSP Group

Restricting queries to sigma with sigma^dagger sigma in M_t(K) avoids the
local transport ambiguity. But this set need not be closed under products.
In the same genuine source order, take K=Q(j), U=diag(i,1) and
T=[[1,1],[0,1]]. Both U and T are integral automorphisms with Gram matrices
over K. Yet

    (T U)^dagger (T U) = [[1,-i],[i,2]]

is NOT over K. Thus even this apparently useful repair does not supply a
query group with the old hiding relation. One must identify an actual
closed family or a different algorithmic paradigm. The control does not
exclude interesting non-group families or coherent processing of the
remaining centralizer ambiguity.

## 6. What Remains Worth Trying

Highest upside: construct a genuinely new, efficiently evaluable operator
outside Q(alpha), or a method to process the GLOBAL quadratic ambiguity
without supplying a full quaternion dictionary. Either would address the
strong-input bottleneck; producing such an operator is itself a major
algorithmic task, not a preprocessing convenience.

A narrower live lead is a non-group family of gauge-invariant Gram queries.
Before promoting it, exhibit an explicit native parameterization, show
that its labels vary with the desired unknown, give a recovery mechanism
and a matched class-group/isogeny classical baseline. The nonclosure example
above is a required falsifier. Merely choosing arbitrary intertwiners,
averaging labels, or calling a receiver on an assumed source is not progress.

Reject/deprioritize: extra product-copy sweeps, independent Frobenius copies,
degree inference from one-operator intertwiners, or treating a local matrix
solution as an unknown global isogeny. No new CandidateRecord is promoted by
this audit; the missing constructive mechanism remains missing.

## 7. Combined-Source Review Status

This pass reread the existing projective rigidity proof, the stabilized
repolarization and field audits, and the primary PPAV quotient/isomorphism/
canonicalization statements (retained PDF pages 13-14 and 33-35). The
projective rigidity argument uses the polarization MULTIPLIER, not geometric
degree. Its upper bound permits the new p*m marking bound. No contradiction
was found in those inspected implications. This is not an independent
review or proof that every imported clock and implementation is correct.

An additional reviewer was requested asynchronously; no new review was
executed or assumed. The earlier Rees authorization was not reused. The
full native source remains unexecuted and unreviewed. This pass's verified
outcome is the access-boundary falsification above, not a theorem promotion.
