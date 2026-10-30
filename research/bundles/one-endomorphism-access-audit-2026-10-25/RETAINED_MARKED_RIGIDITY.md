# Marked Quotients: A Constructive Repair With Explicit Limits

2026-10-23. Proposed source-separation lemmas, independent review pending.
These are applications of standard polarized-isogeny rigidity, NOT a new
isogeny evaluator or a cryptanalytic result. They repair the injectivity
and unknown-scalar parts of a possible source contract. Efficient action
evaluation and JOINT canonicalization remain unimplemented/unproved here.

Follow-on: SIEGEL_ELEMENTARY_REPOLARIZATION.md gives a proposed constructive
action/evaluator and transported-polarization formula for A=E^g,g>=2 with
known End(E). Efficient conversion to the changed polarized model and
joint canonical labels is still not supplied; see its2026 prior-art audit.

## Decision

SIEGEL_NATURAL_SOURCE_AUDIT.md correctly rules out unmarked quotient
codomains as universally valid coset labels. Suitable auxiliary torsion
markings do repair that specific problem without requiring access to the
secret large-prime torsion. Unknown invertible evaluation scalars can also
be removed, but require a stronger rigidity bound and careful joint labels.

The most important negative control is not a failed benchmark: exact
61-isogeny endomorphism identities show that both an insufficient marking
bound and separate canonicalization at each torsion level can identify
different kernels. The latter error persists even ABOVE the stronger bound.

This narrows the next constructive task to building a real transformed
polarized-isogeny evaluator and one canonicalizer for the ENTIRE marked
object. Do not present the numerical bound checker as either algorithm.

## 1. Mathematical Input And Label Contract

Work over an algebraic closure of a field of characteristic p. Let A,B,C
be principally polarized abelian varieties of the same dimension g. An
isogeny phi:A->B has polarization multiplier d if

    phi^* lambda_B = d lambda_A,
    phi^dagger phi = [d]_A,    phi phi^dagger = [d]_B.

The geometric degree is d^g, NOT d for g>1. All adjoints here use the
specified principal polarizations, so they are integral homomorphisms.
For a Siegel application d=ell is a prime different from p, and ker(phi)
is a Lagrangian in A[ell], abstractly F_ell^(2g). No assumption that its
torsion basis is accessible is made in these lemmas.

Choose pairwise coprime orders r_1,...,r_s, each coprime to p*d, and let
M=product(r_i). Fix a FULL ORDERED basis of A[r_i] for every i; bases of
these auxiliary torsion groups, unlike A[ell], would need to be accessible
to a source implementation. Mark each B with the images of those fixed
domain points under phi. Two labels are equivalent ONLY when ONE polarized,
origin-preserving codomain isomorphism u:B->C takes all the markings of one
to the other, over a fixed coefficient-field embedding. Do not additionally
quotient by translations or independent Frobenius conjugacies.

In projective mode, for each order r_i a single unit a_i modulo r_i may
multiply its entire ordered basis tuple. Different orders may use different
units; different points in one basis may NOT. The codomain isomorphism u
must still be the SAME across every order. This allows weak evaluation
whose scalar varies with the order, representation and query, but is common
and invertible on the complete tuple. Nonunit/zero scalars are not covered.

The arithmetic foundation is the integral Tate-module trace and positivity
of the Rosati trace pairing; see [Milne, Chapter I, Theorems 10.9 and 14.3,
and Proposition 10.20](https://www.jmilne.org/math/CourseNotes/AV.pdf).
We use Tr([1])=2g. A nonzero integral homomorphism between principally
polarized varieties has positive INTEGRAL squared Rosati norm, hence at
least one. Apply positivity on A x B for the Hom-space version. These are
standard facts; the source-specific deductions follow below.

## 2. Exact Markings: M^2 > 8*g*d Suffices

Let phi:A->B and psi:A->C both have multiplier d. Suppose a polarized
isomorphism u:B->C makes u phi and psi agree on every auxiliary torsion
basis. Their difference Delta=u phi-psi kills all A[r_i], hence A[M].
It factors through [M]: Delta=[M] theta for an integral homomorphism theta.
This follows from the quotient by A[M], not an assumed coordinate matrix
or an available representation of the hidden homomorphism lattice.

In the positive Rosati norm on Hom(A,C),

    ||u phi||^2 = ||psi||^2 = 2g d,
    ||Delta||^2 <= (||u phi||+||psi||)^2 = 8g d.

If theta!=0, integrality and positivity give

    ||Delta||^2 = M^2 ||theta||^2 >= M^2,

a contradiction when M^2>8g d. Therefore u phi=psi, so their kernels
coincide. Conversely identical kernels induce a polarized quotient
isomorphism carrying all exact markings. Exact marked labels therefore
classify kernels under this sufficient bound. The constant is conservative;
no optimality or novelty claim is intended.

## 3. Unknown Scalar Markings: M^2 > 8*g^3*d^2 Suffices

Now suppose that for a SINGLE polarized u:B->C and units a_i modulo r_i,

    psi(P) = [a_i] u phi(P)   for every P in A[r_i].

We cannot subtract phi from psi and apply Section 2: the scalars differ.
Instead form, only in the proof,

    alpha = phi^dagger u^(-1) psi in End(A).

It satisfies alpha^dagger alpha=[d^2]. Modulo r_i End(A) it is the scalar
[a_i d]. The congruence follows by factoring the vanishing difference
through [r_i]. Put t=Tr(alpha), an integer, and remove the scalar component:

    beta = (2g) alpha - [t].

Then beta is divisible by every r_i in End(A), hence by M. This uses
pairwise coprimality and the torsion-free integral endomorphism group.
The trace-free projection has squared norm

    ||beta||^2 = (2g)^2 ||alpha||^2 - (2g)*t^2
               = 8g^3 d^2 - 2g*t^2
               <= 8g^3 d^2.

If M^2>8g^3 d^2, a nonzero beta would contradict the same positive-integer
norm argument. Thus alpha is a rational scalar. Its norm equation forces
alpha=[d] or [-d]. Multiplying on the left by phi and using that Hom(A,C)
has no integer torsion gives psi=+u phi or -u phi. In particular their
kernels coincide. The converse again holds when kernels coincide.

Thus JOINT projectively marked polarized quotients are injective labels
of kernels at total level M>sqrt(8*g^3)*d, even with unknown invertible
scalars at the individual auxiliary orders. No computation of alpha, beta,
u, End(A), or a secret kernel is part of this proof's proposed evaluator.
Treating those proof objects as free computational inputs would be circular.

## 4. Why The Weaker Bound Fails For Unknown Scalars

Take E:y^2=x^3-x in characteristic 101 and its automorphism i with i^2=-1.
Let A=E^g with product principal polarization and consider the two scalar
Gaussian-integer endomorphisms, acting in each factor,

    phi_+ = 6+5i,       phi_- = 6-5i.

Both have multiplier d=61. Their actions on 61-torsion have different
kernels: the two Gaussian conjugates have distinct one-dimensional kernels
in each E[61]. This can also be checked by the explicit 2-by-2 matrices.

At orders 4 and 3 the two maps differ by -1; at order 5 they agree. Therefore
their projective markings coincide at (4,3,5), whose product is M=60. For
g=2, M^2=3600 exceeds the EXACT threshold 8g d=976, but is below the
PROJECTIVE threshold 8g^3 d^2=238144. Applying the exact threshold to these
weak marks would falsely certify separation.

The norm calculation is explicit as well. For g=2,

    alpha = phi_+^dagger phi_- = 11-60i,
    Tr(alpha)=44,
    beta=4alpha-44 = -240i,
    ||beta||^2 = 230400,
    beta/60 = -4i != 0.

So the weaker total level genuinely leaves a nonzero integral remainder.
This is a falsifier of one proof shortcut, not a synthetic oracle-search
problem and not an isogeny hardness benchmark.

## 5. Why Canonicalizing Each Order Separately Also Fails

Add order 11 to that same example, giving M=660. Now M^2 exceeds even the
stronger g=2 bound. At order 11,

    i phi_+ = -5+6i = 6-5i = phi_- (mod 11).

At the earlier orders the identity codomain isomorphism already works up
to scalar. Hence a procedure that independently minimizes over codomain
automorphisms at EACH order merges the two entire labels. There is no
contradiction to Section 3: it has selected incompatible isomorphisms.

For the four Gaussian automorphisms, orders 3 and 11 respectively require
real and imaginary phase, so there is no common choice. The theorem rules
out any common polarized isomorphism, since the kernels differ and the
bound is satisfied. The test explicitly enumerates these four known
automorphisms as a countercontrol, not a general automorphism-group solver.

A correct conceptual label has the form

    Canon( B, lambda_B, ( [phi(P_(i,1)),...,phi(P_(i,2g))]_common-unit )_i ).

The outer Canon acts on the WHOLE marked object with one isomorphism. If a
fixed model for B and its polarized automorphisms are already available,
one can minimize over one automorphism applied to all orders together;
within each order, minimization over units is independent. Minima in the
opposite nesting order are unsound. This prescription does not provide the
missing variety-model canonicalization algorithm for arbitrary inputs.

### Dropping The Polarization Defeats Arbitrarily Large Exact Marks

There is a separate failure even with one common isomorphism and EXACT
markings, if it need not preserve the polarization. On E^2 use

    s=6+5i,  t=6-5i,
    Phi=diag(s,t),   Psi=diag(t,s).

Both have multiplier 61 and different 61-torsion kernels. Let M be ANY
integer coprime to 61*101. In Z[i]/M put z=t/s=t^2/61 and w=s/t=s^2/61.
They are inverse units. Choose any Gaussian-integer lifts z0,w0 and set

    U = E12(z0) E21(-w0) E12(z0) [[0,-1],[1,0]].

Every factor is an invertible Gaussian-integer matrix, so U is an actual
automorphism of E^2, not just a modular matrix. Its reduction is diag(z,w),
and therefore U Phi-Psi is divisible by M in End(E^2). Thus U makes all
EXACT markings agree on A[M]. For M above the rigidity threshold it cannot
preserve the product polarization, since the kernels differ. The tests
also check U^T U!=I in the Gaussian real-lattice model.

For example M=660 or 1001 exceeds the projective g=2,d=61 threshold. A
canonicalizer for unpolarized varieties with even these exact marks will
merge the inputs. Increasing the mark budget alone cannot repair it.
Including the polarization in the equivalence relation is essential, not
an optional metadata field. This also warns against using arbitrary
degree-one action lifts while silently retaining an unchanged polarization.

## 6. Cost, Classical Baselines, And Remaining Gaps

The total level may be large while the mark data remain small. Use CRT
bases at separate small auxiliary orders; do not construct their sum in
one possibly huge compositum field. For fixed g,d, the arithmetic checker
requires only products and exact integer comparisons. To scale with d,
one can grow a product of small primes avoiding p*d until the inequality
holds. The log of the required product is O(log(g)+log(d)); standard prime
estimates give polynomially many small primes. This is a mark-size fact,
NOT a theorem that the corresponding geometric points are cheaply available.

Field representation, torsion basis construction, each weak evaluation,
unit arithmetic, polarized codomain models, joint canonicalization and
coherent reversible workspace must all be charged. At fixed dimension a
small-prime Frobenius order bound is polynomial in that prime, but the crude
bound |GL_(2g)(F_r)|<r^(4g^2) is not polynomial uniformly in g. Do not erase
that dimension dependence or infer point-construction algorithms just from
the existence of a suitable finite extension.

Relevant prior work and baselines:

- [Chen et al.](https://arxiv.org/html/2305.19897), Sections 2.4 and 4,
  separate weak representations, group-action evaluation and hidden Borel
  recovery in the elliptic setting. Those algorithms do not automatically
  give the needed higher-dimensional evaluator or labels.
- [Robert, Corollary 5.22 and Appendix A](https://eprint.iacr.org/2024/1071.pdf)
  describe accessible CRT torsion and conversion to higher-dimensional
  representations for elliptic isogenies. Constructing an evaluator from
  auxiliary torsion is therefore not itself a new quantum algorithm.
  Such a representation is NOT automatically an explicit basis of a
  large-prime kernel over a small field; do not equate these output tasks.
- If the secret ell-torsion basis and coherent evaluation are accessible,
  the direct abelian HSP from SIEGEL_NATURAL_SOURCE_AUDIT.md is already a
  quantum baseline. The marking lemmas never grant that access.
- The random-label classical lower bound in SYMPLECTIC_FIELD_CHART_REDUCTION.md
  does not prove hardness for these structured geometric labels. A matched
  classical attack remains obligatory if an actual source is built.

In particular, a claimed source needs a uniform procedure which, from
real public data and any queried Sp matrix g, constructs a d-isogeny with
kernel gK as a polarized quotient and evaluates it on the marks. A formal
action on K is not this procedure. It must then implement the joint Canon
with controlled errors and no encoding-dependent residual work registers.
Only AFTER those two tasks are established does the marking theorem supply
the exact oracle promise needed by the field-chart reduction.

## 7. Artifacts, Falsifiers And Next Decision

theorems/siegel_marked_source.py computes exact sufficient level budgets
for the two lemmas. It checks coprimality and prevents double-counting
overlapping orders. It does NOT verify principal polarizations, true
isogenies, available torsion, invertible weak scalars, canonicalization or
source complexity. strict_separation is an arithmetic predicate, not an
accepted-candidate flag. Falling below a sufficient bound is not a no-go.

tests/test_siegel_marked_source.py uses exact FLINT integer and finite-field
linear algebra for the Gaussian controls, integral norms, separate-level
canonicalization failure, non-polarized isomorphisms, nonunit weak scalars,
and whole-basis versus per-point scalar ambiguity.
Small complete Gaussian families test joint labels only in that fixture.
No actual quotient, torsion point, quantum circuit or natural-input solver
is executed, and no finite success is used to prove the lemmas.

The next high-value question is specific: for a fixed-dimensional weak
isogeny input not already covered by abelian recovery, can the required
transformed polarized quotient and ONE jointly marked canonical label be
computed from accessible public data in polynomial time? First audit any
suggested action lift for changed polarization and any suggested label for
the explicit counterexamples above. If no such construction is available,
do not keep extending marking bounds. Return to an independent constructive
algorithm direction rather than turning these conditional lemmas into an
application claim or a new infrastructure campaign.
