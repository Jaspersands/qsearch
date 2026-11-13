# Completely split dyadic places: native ternary decision

2026-11-13. Independent source/composition review. No tests, API, network,
Git, archives, or shared-note edits. Physical source locators count LF.

**Disposition.** The restricted DECISION endpoint closes under the already
reviewed GRH arithmetic backends, after the elementary rank-three local
repair below. Dubey--Holenstein's printed sign-walking rule cannot itself be
imported without qualification. No general-K dyadic compiler, integral
witness, novelty, classical separation, or implementation follows.

## 1. Exact contract and source qualification

Input: an expanded totally real degree-n field K with its charged maximal
order basis/table, and integral nonsingular symmetric ternary Gram matrices
A,B, indefinite at some real embedding. Require 2 to split completely in K;
this restriction is verified below, not supplied local-field advice. Decide
whether U^t A U=B for U in GL_3(O_K), with error at most eta and quantum
BIT/gate cost polynomial in all input bits and log(1/eta).
The general number-field contract in INDEFINITE_TERNARY_SPINOR_ADMISSION
remains open. Its old GLOBAL-open paragraph is superseded by the expanded
construction in EXPANDED_NORM_TERNARY_TRANSPORT, not by this restriction.

Primary: audits/sources/dyadic_seed_selection/dubey_holenstein.txt.
Its LF664–666 states a transformation-producing
2-adic algorithm; LF675–1097 explicitly treats binary blocks, mixed ternaries,
sign walking, and oddity fusion. LF257–269 measures RING operations; finite
integer residues would convert its stated polynomial counts to BIT counts.
However LF524–530's unrestricted train rule has a concrete defect:
for diag(3,10), the two unary signs are minus and compartment oddity is 0.
Flipping both would require two plus unary units with total oddity 4 mod 8.
Plus units are 1 or 7 mod 8, whose pair sums are only 0,2,6. Thus that
claimed move has no resulting lattice. Lemma17's constructive list also
omits adjacent Type-I/Type-I walking. This is a source-proof qualification,
not a counterexample to polynomial local transport. We bypass that step.
The elementary minimum-pivot block diagonalization in Theorem5/AppendixA
(LF297–300,1158–1230) is valid and suffices for the following independent repair.

## 2. A complete fixed-rank Q2 seed algorithm

Exact symmetric elimination over Q produces a Z_2-unimodular basis and
blocks 2^a U_a with U_a unimodular, of rank one or two. A minimum diagonal
entry splits a line; otherwise a minimum off-diagonal pair has an odd
normalized determinant and splits a binary block. There are at most three
pivots, so rational coordinate heights are polynomial. The sorted scales,
with their multiplicities, are the Smith elementary divisors and are invariant.
Reject unequal lists. Cluster successive occupied scales with gap at most 2.
Each cluster in rank three has scale diameter at most 4.

Here is the necessary separation proof, without classification tables.
Write A=diag(A1,2^h A2), B=diag(B1,2^h B2), with A2,B2 integral and
v_2(A1^-1),v_2(B1^-1)>=-a entrywise, where h-a>=3. Suppose an integral
isometry U=[[X,Y],[Z,T]] exists. From AU=U^-t B we get
A1 Y=2^h (U^-t)12 B2, so Y is divisible by 2^(h-a). Consequently X,T are
invertible over Z_2. The first-block equation gives
X^t A1 X=B1-2^h Z^t A2 Z. Its B1-relative error has valuation at least 3,
so the convergent inverse-square-root correction gives an integral A1/B1
isometry. Cross-orthogonality gives Y=-2^h A1^-1 X^-t Z^t A2 T, whence
B2=T^t A2(I+E)T, E=2^h Z X^-1 A1^-1 X^-t Z^t A2.
Here v_2(E)>=3 and E is A2-self-adjoint. Thus (I+E)^(1/2)T is an integral
A2/B2 isometry. This bound DOES NOT subtract the scale width of A2.
Conversely the direct sum of two integral isometries works. Iteration proves
that the clusters match independently, including every cross-scale case.

Divide a cluster by its lowest power of 2. Its inverse has poles at most 4.
Enumerate matrices in Mat_r(Z/512), r<=3, retaining invertible solutions
X^t C X=D mod 512. The loop has at most 2^81 entries, an ABSOLUTE constant,
not 2^growing_precision or 2^[K:Q] work. If none exists, the cluster is not
isometric. A retained seed lifts: E=D^-1(X^t C X-D) has valuation >=5;
X(I+E)^(-1/2) is an exact integral isometry. The existing local-offset-verifier
Section2 bounds the series tail and computes any polynomial precision in
polynomial BIT time. Hence this deliberately impractical constant search
and polynomial lifting give a complete local compiler, without Dubey's
uncorrected canonical-symbol step or an unproved BONG state-graph search.

## 3. Native embeddings, precision, and odd places

Compute O_K/2O_K from the table. The condition b_i^2=b_i for every F2-basis
element is equivalent to this algebra being a product F2^n, hence to complete
splitting. Repeatedly split an idempotent e into e*b_i and e*(1-b_i), discarding
zero parts. At most n-1 genuine splits produce all n primitive idempotents;
no 2^n enumeration occurs. Lift them modulo 2^M by e -> e^2(3-2e).
Uniqueness of idempotent lifts preserves orthogonality and their sum 1.
Each component is rank one over Z/2^M. Choose an odd coordinate e_j; the map
phi_e(b)=(eb)_j/e_j mod 2^M is its canonical ring projection. These compatible
maps supply the required K_P -> Q2 approximations, and their mod-2 kernels
give the prime ideals. They avoid a false monogenic-mod-2 assumption.

For integral A,B, compute s=max_P(v_P(det A),v_P(det B)) and use M>=s+5.
These valuations are bounded by the logarithms of their nonzero integral
absolute norms, themselves polynomial in the native expanded input bits.
The integer residue matrices A0,B0 modulo 2^M are nonsingular and have the
same determinant valuations as the originals. Each is integrally isometric
to its original local matrix by the identity-seed square-root lemma.
Apply Section2 to A0,B0 and compute its answer to M bits; it is a seed for
the actual A,B. Rational evaluations add their known denominator valuations
to working precision. All ring operations involve polynomial-bit integers.

At odd P, use exact minimum-pivot Jordan diagonalization over K. Match ranks
and determinant unit squareclasses at each scale. Over the residue field
F_q, a nonsingular binary form represents every nonzero target; random first
coordinates followed by a quadratic root find a representation with constant
success probability (there are q-1 or q+1 solutions). Finite-field factoring
and capped repetition cost poly(log q,log(1/eta)). Extend a primitive vector,
remove its orthogonal complement, and repeat in rank <=3. Lift each matched
unimodular block using the matrix square-root correction (2 is a unit).
At odd places the separation proof also works across every positive scale gap.
This gives all odd-place transporters, including ramified/nonunimodular ones,
without enumerating F_q or invoking the narrower First unimodular theorem.

## 4. Global support, offsets, and the ray obstruction

First test rational invariants/signatures; the reviewed expanded norm and
quaternion construction returns F with F^t A F=B when possible. Its auxiliary
fields need NOT satisfy split-at-2: the global norm backend already handles
them. Factor expanded coordinate denominators/numerators and determinants,
using the denominator-plus-integral-norm cover, not a cancellable absolute
norm alone. Include 2 and det A,det B. This yields polynomially many bad
prime ideals E; outside E, F and F^-1 are integral and both lattices unimodular.
Check the local genera at E with Sections2–3. Different genera mean NO.

For each needed local seed compute Y to the precision in the reviewed
local-offset-verifier: with W^t A W diagonal and
beta=s(W^-1)+s(F^-1)+s(W), take P=beta+4v_P(2)+1, where s bounds pole order.
Correct orientation using det(Y)/det(F), replacing Y by -Y if necessary.
For h=W^-1 YF^-1 W, one of the four proper diagonal signs S satisfies
v_P(1+tr(Sh))<=2v_P(2), since these four traces plus ones sum to 4.
Its squareclass, multiplied by theta(S), gives the offset modulo H_P=
theta(SO(A,O_P)). This is relative to F, never a spinor norm of a raw map
between forms. The already reviewed Beli/Voight compiler supplies H_P at 2;
Kirschmer5.4.4 supplies the odd groups. Outside E the offset is 1 and
H_P=O_P^* K_P^{*2}. All precision/pole bounds are polynomial.

For completeness, there is a direct paid realization of the full RAY test.
Enlarge E to T by all primes above rational primes <=48*max(1,bitlen|disc K|)^2.
Under the same class-generator GRH, Cl(O_K,T)=0. Biasse--Song Theorem1,
Theorem5 and compact-output proof, with the already reviewed error accounting,
return COMPLETE compact T-unit generators; include -1. Verify zero valuations
outside T by factoring their small atoms and summing binary exponents. Map to
V=(direct_sum_{P in T} K_P^*/(K_P^{*2} H_P)) direct_sum F2^{definite real places}.
Include the offset j on the finite coordinates and zero sign bits. Decide
whether it lies in the binary span of the generator images. At extra good
places H_P is the unit subgroup, so this coordinate merely tests valuation parity.

Proof of equivalence: Kirschmer5.4.5 requires j=c*h with c positive at the
definite real places and h in the local stabilizer spinor groups. Necessarily
v_P(c) is even outside T. As Cl(O_K,T)=0, choose d with
v_P(d)=v_P(c)/2 outside T; u=c/d^2 is a T-unit with exactly the same local
squareclasses and signs. Conversely any such T-unit solves the idele test.
Thus this binary computation is the quotient of Theorem5.4.6, NOT the ordinary
class-group shortcut refuted by the retained p17 neighbor. Its dimension is
at most 3|T|+n. Compute compact-unit images atomwise, reducing binary powers
mod 2; do not expand units. Signs of expanded atoms and local squareclasses
have polynomial exact precision. Corollary5.4.10 identifies the spinor genus
with the class because of indefiniteness, and odd rank removes properness.
Primary locators: spinor_genus_admission/kirschmer.txt LF4439–4615; retained
arxiv_2510_02280v2.txt LF103–121,1576–1588,1654–1759,1784–1818.

## 5. Clock and classical comparison

All supports, numerical precision bounds, subgroup dimensions and backend
call counts are input polynomials. Split a total eta across complete units,
global norm calls, factoring and residue algorithms; impose their reviewed
finite clocks and output-size caps. Local certificates and returned global
maps are checked exactly. Incomplete arithmetic output may cause false NO
or ABORT within the error budget; it never certifies completeness by itself.
No isometry-class enumeration or integral-isometry WITNESS is constructed.

The strongest general classical comparator is this SAME spinor/norm/S-unit
reduction with classical arithmetic. The local repair is wholly classical.
For a SUPPLIED quadratic tower, the closed ERH/factoring reduction computes
complete K(T,2) and expanded conics (enlarge T by tower ramification). Its
basis replaces T-units in the same
local/sign test, and its conics pay global transport. Thus that subfamily has
a classical polynomial reduction to integer factoring, under its stated
relevant-Hecke ERH. General totally real split-dyadic fields need not carry
such a tower. No advantage beyond those explicitly separated backends is claimed.
