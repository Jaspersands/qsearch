# Constructive unit norms in dyadic quadratic orders

2026-11-13. Reviewed WRITTEN classical unit-norm construction. This pays a
specific binary BONG operation; it does NOT prove a complete ternary transporter.
The full174-line independent coordinate/word proof and all nonempty paid
report text were parent-read. Exact finite controls passed; scope repairs below.

## Native contract and why this operation

Let F be a finite extension of Q2, O its valuation ring, pi a uniformizer,
e=v(2), and residue field k=F_(2^f). Local arithmetic comes from the charged
expanded number-field/maximal-order input at a specified prime. Both e,f
grow. Input T,N in O and the free quadratic algebra
 R=O[theta]/(theta^2-T theta+N),
with separable generic algebra F tensor R (field OR split), and eta in O^*.
Decide whether eta is the norm of a UNIT OF THIS ORDER and, if yes, produce
a preimage to arbitrary absolute precision L, in polynomial BIT cost in
input,e,f,L. Supply T,N,eta and working ring products to at least
max(2e+1,L+e) absolute digits, plus charged coordinate denominator guards.
No maximal order, unit group, norm preimage or residue enumeration
is supplied. An exact infinite p-adic expansion is not the output.

This is a classical operation required by coupled BONG transformations in
the native indefinite ternary integral-isometry route. Beli's actual2009
classification source Section5.1 and Lemma5.1 give allowed binary scaling
via g(a), but membership alone is not a computed lattice isometry. The
separate growing-degree ternary seed and bounded coupled word remain OPEN.
Corpus been-tried/baselines were checked; the catalogue points to ordinary
class/unit and lattice algorithms, with no matching theorem implied. A
primary-source search found mostly GLOBAL quadratic-order unit algorithms,
which are not imported as local bounds. The proof below is elementary local
unit filtration, with no novelty, speedup or absence-of-prior-art claim.

## Explicit generators with recorded preimages

Write U_j=1+pi^j R. For every j>=1,
 U_j/U_(j+1) is the additive group R/piR.
Choose an F2 basis beta_1,...,beta_f of k and arbitrary integral lifts. Include
 1+pi^j beta_i and 1+pi^j beta_i theta,
for 1<=j<=2e and 1<=i<=f. Every listed element is a unit.

The tail U_(2e+1) consists of squares INSIDE R. For X in pi^(2e+1)R,
(1+X)^(1/2) converges in R by its binomial series: the j-th term has valuation
at least j(2e+1)-(2j-1)e=j+e. This uses the free complete O-module R and
integral multiplication, and remains valid for a nonmaximal order or a split
algebra. It does not assume an integral basis of the maximal order.

The residue algebra is either a separable quadratic field, k times k, or
k[epsilon]/epsilon^2. In the separable cases its unit group has odd order,
so squaring is onto and no residue-unit squareclass generators are required.
In the double-root case, find r in k with X^2-Tbar X+Nbar=(X-r)^2,
put epsilon=theta-r modulo pi, and add the units
 1+beta_i (theta-r_tilde), 1<=i<=f.
Modulo pi these generate the factor 1+k epsilon; the scalar k^* factor again
has odd order. Frobenius inversion computes r without residue enumeration.

These <=(4e+1)f explicit units generate R^*/R^*2. Indeed first remove the
residue-unit class, then remove the successive additive filtration layers;
the remaining tail is a square in R. We need a generating set, not an
independent basis or a discrete logarithm in an odd-order residue group.
The same argument gives a finite matrix construction modulo pi^L; all
filtration indices are O(e), not exponential in the residue-field size.

## Norm-image membership and a preimage

The algebra norm is N_R/F(p+q theta)=p^2+T p q+N q^2. Compute the norms of the
listed units. Using the already paid local squareclass/Hilbert-pairing basis,
represent these and eta in F^*/F^*2 and solve one F2 linear system. The local
Hilbert algorithm is paid by Voight Theorem6.1 and the existing review
`audits/reviews/2026-11-07-spinor-genus-sources.md`; no squareclass enumeration.

If eta is outside the span, it is not a norm of an R-unit. If it is inside,
multiply the recorded selected generators to obtain u in R^* with
Norm(u)/eta=z^2 in F. Because Norm(u),eta are units, z is an O-unit. Thus
 u/z is an R-unit and Norm(u/z)=eta.
This scalar correction preserves the ORDER, unlike an arbitrary fractional
global norm witness. At finite precision output coefficients modulo pi^L.
Only polynomially many ring operations and O(e f) generators are involved.

The scalar root is constructive. Start with a unit y whose residue is the
Frobenius square root of c=Norm(u)/eta. If j=v(c-y^2)<2e, squarehood forces
j=2r even; cancel the leading error by y+=pi^r d using one residue Frobenius
root. Cross term valuation e+r>2r, so the error valuation increases. At j=2e,
solve d^2+(2y/pi^e)d=(c-y^2)/pi^(2e) in k by F2 linear algebra and update
y+=pi^e d. Squarehood guarantees solvability. Above2e, ordinary Newton
iteration gives any requested precision, with e guard digits for division
by2. At most O(e) initial lifts and polynomially many finite-precision
operations are needed. If the requested precision is already reached, stop.
All unit inversions preserve precision except the explicit division-by2
guard; no unknown local inverse is assumed.

## Binary lattice realization

Use q(x)=B(x,x), not half that bilinear value. In a rank2 integral lattice
choose a primitive norm generator x with q(x)=a,
and extend it to a basis x,y. Put c=B(x,y)/a and b=q(y)-a c^2. Since a
generates the norm ideal, T=2c and N=q(y)/a are integral. The quadratic order
above has theta=c+sqrt(-b/a), trace T, norm N, and
 q(p x+q y)/a=Norm(p+q theta).
Hence an order-unit norm preimage of eta yields an integral primitive vector
v of norm a eta. Primitivity follows because a unit norm cannot arise from
piR. Extend v to a determinant-one lattice basis v,w using whichever of its
two coordinates is a unit. Its orthogonal projection w_perp has norm b/eta;
eta w_perp then has norm b eta and is a valid BONG vector (unit rescaling).
Thus the permitted binary BONG replacement can be realized with coordinates,
not merely recognized from a Hilbert symbol.

For an ADJACENT sub-BONG in a ternary lattice this is not an asserted
orthogonal integral direct summand. The sub-BONG replacement lemma and its
coordinate lifting must be applied explicitly. A bounded complete sequence
of replacements remains a separate obligation. Beli's actual final remark
asserts binary connectivity for residue size>2, without a polynomial word
bound, and gives a RANK4 obstruction for residue F2. That rank4 example does
not settle ternary completeness in either direction.

## Claim gates and next experiment

No full native integral-isometry algorithm, all-rank constructor, quantum
execution, separation or hardness result is established by this note.
The exact control audits/controls/dyadic_order_norms/check.py passed all unit
norm-image classes and in-order deep square roots in six tiny quadratic rings,
including split, ramified and nonmaximal orders. It also checks the actual
binary move diag(1,4) ->diag(5,20), and an unramified residue-degree2 root
boundary example. These are falsifiers, not the proof of polynomial cost.

The exact local solution u/z exists in the completion. A finite output vector
lifted to K has norm a*eta_prime with eta_prime=eta modulo the stated digits;
it need not have EXACT norm a*eta in K. With precision at least2e+1 the unit
squareclass agrees. Downstream finite-seed congruences carry the guards and
are explicitly verified; no exact global element is invented.

The independent word proof is audits/reviews/2026-11-13-dyadic-seed-construction.md.
It constructs the adjacent binary lattice and applies actual thesis1.4.9(ii),
LF2151–2188, not an assumed orthogonal summand. Two three-move words have an
exact polynomial affine-Hilbert feasibility test with one forbidden filtration
coset. The 23/12/23 word is complete for e=1 and equal BONG valuations, at
arbitrary residue degree. The full general ramified completeness claim remains
OPEN; failure of either word is UNKNOWN. Parent checked the complete174LF.

Paid attack2026-11-13-dyadic-order-norm-attack is truncated NONEMPTY at24000,
reapedexit1; ALL9858responsebytes parent-read, including the incomplete BIT
section. EstimatedUSD0.508108, not invoice/balance. Core proofs check, with
precisions explicitly added above. Two report errors are NOT imported:
for alpha=p+q theta the conjugate is p+q(T-theta), NOT T-alpha in general;
and the j=2e root branch can occur at e=1 when f>1. Exact example: unramified
F=Q2(w), w^2+w+1=0, (1+2w)^2=-3, and starting y=1 has error valuation2.
The residue equation d^2+d=1 is solvable in F4. The paid text's suggested
need for e>=2 is therefore false. Generic separability was unnecessary for
the norm lemma but the present nondegenerate lattice contract is retained.

The DISTINCT general seed Fable/max request2026-11-13-coupled-dyadic-seed is
terminal EMPTY/max_tokens at48000, reapedexit1; estimatedUSD2.937300, no findings,
no retry. The two round estimates sumUSD3.445408; owner20.59 remains a separate
balance anchor. No paid OpenAI call. No full algorithm follows from either
report label. Next hard question: bound the coupled word in the ramified
case, or replace the finite seed search with a paid algebraic operation.

