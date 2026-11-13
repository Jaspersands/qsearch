# Fixed-length Witt seed for unramified dyadic ternaries

2026-11-13. Reviewed WRITTEN local compiler and restricted native end-to-end
DECISION composition. No general ramified, witness, novelty or speedup claim.
Start STATE/TRAPS at the completed split-dyadic milestone. Corpus been-tried
and baselines for Witt finite-precision seeds were checked before this proposal;
Groebner/finite-field solving is the direct classical baseline and intended
operation, not an alleged source of quantum advantage.

## Native question and single mechanism

Given expanded K/O_K and a prime P above2 with ramification index e=1, residue
field k=F_(2^f), and integral nonsingular ternary A,B, compute a finite local
integral isometry seed or localNO in polynomial BIT time in all input bits,
f, requested precision and log(1/eta). No local map, residue-point oracle,
unit basis, normalized cluster or Witt coordinates are advice. f grows.
This removes the dyadic seed gate for the native indefinite ternary decision
family with2 UNRAMIFIED, not necessarily completely split, with the fully
checked SEARCH construction below.
The global arithmetic backends remain the already stated GRH assumptions.
General growing ramification, witnesses, novelty and speedup stay unclaimed.

The previously parent-checked Jordan cluster separation proof uses e=1,
not f=1: split occupied scales at gaps>=3. Each rank<=3 normalized cluster
has diameter<=4 and inverse poles<=4. Thus an invertible solution
 X^t C X=D modulo2^9
lifts by the existing square-root verifier. The old Q2 algorithm enumerated
at most2^81 matrices; enumeration overk would instead cost2^(81f), forbidden.
The NEW operation expresses this seed as a fixed-dimensional bounded-degree
polynomial system overk, then constructs a k-point using actual finite-field
SEARCH. A decision or approximate-counting oracle alone does not pay X.

## Actual Witt source and polynomial reduction

Primary Rabinoff, The Theory of Witt Vectors, arXiv1409.7445, retained under
sources/dyadic_seed_selection/rabinoff_witt.{pdf,txt,source.json}.
Actual Theorem1.2/Example1.3 give the unramified strict2-ring/Teichmuller
identification; Corollary2.10 and Example2.12 give universal INTEGER addition
and multiplication polynomials; Theorem2.13 gives the explicit isomorphism.
With ordinary zero-based2-typical coordinates, it is
 Phi(a0,...,a8)=sum_(i=0)^8 2^i tau(a_i^(2^(-i))) modulo2^9.       (1)
The vectors whose first9 coordinates vanish map precisely onto2^9 O_F by
the unique Teichmuller expansion, so the isomorphism descends to W_9(k).
The inverse-Frobenius twist is REQUIRED. Untwisted Teichmuller digits are
not Witt coordinates; using them in universal polynomial formulas is false.

Generate the universal polynomials once overZ by ghost recurrences
 w_j(x)=sum_(i=0)^j 2^i x_i^(2^(j-i)),
 w_j(S)=w_j(x)+w_j(y),   w_j(M)=w_j(x)*w_j(y).
Solve for S_j,M_j by subtracting lower components and dividing by2^j OVER Z,
then reduce their integral coefficients modulo2. Do not divide by2 insidek.
There are nine components. Give X coordinatei weight2^i. S_j has weight2^j;
M_j has that weight separately in each of its two inputs. Multiplication by
the constant C preserves X-weight<=2^j, the second X factor gives<=2^(j+1),
and Witt addition preserves this bound. Therefore EACH matrix equation has
total degree<=512, independentoff. The determinant equation has degree<=4.
Dense expansion has an enormous ABSOLUTE size at fixed rank/length; no
practical bound or straight-line-program SEARCH extension is claimed.

Use9r^2 variables for entries of an r-by-r Witt matrix X, r<=3. The six or
fewer upper-triangular congruences each have9 coordinate equations. Add one
scalar variable h with h*det(X_0)-1=0, where X_0 is the matrix of zeroth
components. Thus at most82 variables and55 equations, with degree at most512.
The determinant constraint ensures a unit determinant in the local ring.
Every solution is a genuine mod2^9 seed, and every seed gives a solution.
Singular or reducible seed varieties are permitted; no smoothness promise.

## Paid native coordinates and lifting

Compute O_K/P^L and k from the charged maximal-order/prime data by finite
ring and HNF arithmetic; verify e=1. This quotient is the truncated strict
2-ring with residuek. It has polynomial bit size O(fL) in its local encoding.
Residue field elements have native lifts obtained by linear algebra.
For a in k choose a lift and Hensel-solve t^(2^f)=t moduloP^L. The derivative
is -1 modP. Exponentiation uses f squarings per step, and the number of
Newton precision-doubling steps is O(log L). No enumeration of2^f elements.
Units are inverted by residue-field inversion and Newton lifting.

Extract successive Teichmuller digits c_i by subtracting tau(c_i) and
dividing by2 with a corresponding loss of one known precision digit.
Solve this division in the native finite quotient by HNF; solutions agree
modulo the remaining precision because e=1. Set Witt coordinate a_i=c_i^(2^i).
Conversely inverse Frobenius in (1) uses at mostf squarings per coordinate.
All conversions have polynomial BIT cost. Denominators and normalization
powers from the exact fixed-rank Jordan decomposition are charged as guard
digits before this conversion, not hidden inputs. The input valuations are
polynomially bounded by expanded coefficient norms/heights.

Map a returned k-point through (1), verify detX unit and X^t C X=D mod2^9,
then run the existing matrix square-root lift to the requested precision.
The local congruence is checked before any spinor calculation. A falseNO or
an exhausted finite-field search clock consumes its assigned failure budget;
passing a finite control never proves completeness of SEARCH.

## Complete finite-field SEARCH, not a decision-to-search shortcut

Parent fully read and checked the176-line proof
`audits/reviews/2026-11-13-fixed-finite-field-point-search.md`. It works for
fixed(n,d), arbitrary growingf, and arbitrary singular/reducible/nonreduced
systems. Actual Kayal chapter6 provides reduced hypersurface charts, exact
absolute-Fq-factor detection and singular-locus recursion. The source
Theorem6.3.8 is a DECISION theorem; the following SEARCH adaptation is an
explicit additional construction using its retained maps and bounds.

A positive chart is monic g(t,z)=0 with a computable inverse whose original
coordinates are P_i(t,z)/Delta_i(t). The primitive-element basis matrix is
invertible overFq(t); Cramer's rule gives nonzero base denominators. Monicity
ensures their product b shares no factor withg, even geometrically. Recompute
that representation rather than trusting a composed expression with removable
0/0. The source's displayed point and intersection bounds leave>=q^r/2 usable
smooth points withb!=0 above an explicit computable threshold depending only
on fixedn,d. The whole g is already monic in its last variable, so every
fiber has at mostD=deg g roots and a random base point is useful with
probability>=1/(2D). The optional coordinate change in the review is not needed;
if used, the transformed denominator is evaluated as a polynomial in all its
new coordinates, retaining its coprimality.

Find ALL fiber roots by gcd(g(t,Z),Z^(2^f)-Z), using f modular squarings,
and capped random trace splits overF2. Any two distinct roots separate with
probability1/2. Evaluate inverse maps only at valid roots and verify the
original equations exactly. The review gives explicit trial/splitting caps,
total failure<=eta, POINT/EMPTY/ABORT and polynomial BIT cost. Zero-dimensional
charts use the same root routine. If there is no absolute Fq factor, rational
points lie in the Frobenius-conjugate intersection/singular locus; the source
recursion lowers dimension without dropping isolated points. Smallq is
exhausted only below a fixed computable constant; no growingq enumeration.

Parent checked actual source LF4535–4621 (primitive element/monicity) and
LF4703–4825 (point bounds and recursion). One source sentence is repaired:
squarefree g need not be coprime to a SINGLE partial (g=xy); g and ALL partials
have no common factor over the perfect field. That is exactly what the quoted
intersection theorem needs. No source-by-abstract or smooth-input promise.

## Remaining native charges made explicit

A multiplication-table residue field is converted to F2[T]/(h) by sampling
an element and computing its minimal polynomial by linear algebra. Degreef
certifies a generator; for f>=2 success probability is at least1/2, because
proper subfields contain at most the sum of2^j for j<=floor(f/2) elements
(with f2/3 checked separately). Use a capped log(1/eta) repetition and a
change-of-basis matrix; f1 is immediate. No discrete logarithm is used.
The native global problem supplies the full maximal-order table; prime
factorization of2 and the e=1 test are charged. The local theorem takes its
specifiedP as part of the input, not a secretly selected embedding.

Each minimum-pivot Jordan shear is P-integral: scalar pivot ratios have
nonnegative valuation; a minimal binary pivot has inverse valuation minus
its scale, while every cross-entry has at least that scale. Every shear has
determinant1 and permutations have unit determinant, so the basis change is
P-unimodular. At rank3 there are at most3 pivots and polynomial expanded
K-coordinate heights. Compute needed K-scalars EXACTLY first. Write each as
alpha/d with alpha in the supplied O_K basis and integerd. To reduce it to
precisionL use numerator precisionL+v_P(d), divide the known power of2,
and invert the remaining unit. This charges denominator cancellation even
when the scalar's final valuation is nonnegative. The maximum explicit
integer-denominator valuation over all required basis/cluster/map entries,
plus requested output precision, is a computable polynomial guard. It does
not depend on an unknown local isometry. Normalizing cluster scales is
included in those exact K-scalars. Final basis changes and the four-chart
offset use their already paid pole/precision guards.

For inverse Frobenius use exponent2^((-i) modf), not an expression with a
negative exponent when i>f. The completed paid review wrote2^(f-i) without
this qualification; the implementation/control and this proof use the
mod-f version. Its incidental claim about computing a2-maximal order is
NOT needed or imported: this native contract explicitly supplies O_K.
Its 'upper triangular' mod2 wording should read LOWER triangular whenY=0.
These repairs do not alter the independently checked reduction.

## End-to-end native consequence and classical baseline

For every expanded totallyreal K with maximal-order data and2 UNRAMIFIED,
and nonsingular integral ternary A,B indefinite at a real place, integral
isometry DECISION now has a reviewed WRITTEN quantum polynomial-BIT/gate
composition under the retained complete GRH arithmetic assumptions. Verify
unramifiedness from the native prime decomposition; inputs violating it are
outside this theorem, notNO instances. Reuse the global expanded rational
map/support, all odd-place transport, local Beli stabilizer groups, relative
four-chart spinor offsets, and complete S-unit ray-obstruction proof in
SPLIT_DYADIC_TERNARY_DECISION.md and its full177-line review. The ONLY local
replacement is the now-paid Witt/SEARCH compiler at e=1 and arbitraryf.

The global S-unit test remains polynomial: at a dyadic place the squareclass
space has dimension f+2, and sum_(P|2) f=[K:Q] in the unramified case. Thus
its total dimension is O([K:Q]+|S|), not an uncharged constant3 perplace.
Assign finite field-model, SEARCH, factoring and arithmetic calls their
polynomially divided error budgets and finite clocks. POINT outputs are
verified; exhausted caps areABORT, never spurious certificates. Every
conditional arithmetic backend keeps its exact GRH assumptions.

The local compiler is wholly CLASSICAL. The strongest classical comparator
is the SAME spinor/norm/S-unit reduction with classical arithmetic; supplied
quadratic towers keep the stronger relevant-Hecke-ERH/factoring reduction.
Only the global class/unit/norm backends provide a prospective quantum
resource difference; no unconditional separation or new advantage is inferred.
This does not prove a general growing-ramification algorithm, construct a
global integral witness, assert novelty or practicality, or implement a
quantum circuit. The astronomical fixed dense-algebra constants are explicit.

## Controls and paid disposition

Exact Sage control audits/controls/witt_dyadic_seed/check.py passed: W_3(F4)
bijection with Z8[w]/(w^2+w+1),64 elements and8192 exact addition/multiplication
identities; untwisted Teichmuller interpretation fails as expected. Generated
integer ghost polynomials are checked for divisibility before mod2 reduction.
This finite control tests the coordinate interface, NOT length9 SEARCH or
the asymptotic theorem. No quantum implementation or full-suite claim.

Paid bundle2026-11-13-witt-seed-attack completed/end_turn/reaped0. All report
text parent-read, with repairs above. Input10526/output19484, estimated
USD0.431784, notinvoice/balance. It proves only the conditional Witt implication;
SEARCH is paid by the separately parent-checked176LF proof, not its opinion
label. No newUNKNOWN, retry or OpenAI call. Prior normmilestone55pins remains
frozen; this pass is a separate delta.

Next hard question: compare the full growing-ramification ternary endpoint
with independent high-upside directions before extending by inertia. The
specific current falsifier is whether the two affine-Hilbert three-move words
can fail on a genuinely isometric ramified ternary goodBONG. A verified failure
would reject only those words; an all-input proof would pay the general seed.
