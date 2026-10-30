# Framed Polarizations For An Additive Endomorphism-Lattice HSP

2026-10-26. NEW, UNREVIEWED CONSTRUCTION. This is a proposed alternative to
the reference-curve/nonabelian source, not an established algorithm or novelty
claim. Its algebra and exact framing must be attacked before promotion.
No geometric labels, coherent source or unknown endomorphism ring have run.

## The Scientific Question

Can rational endomorphisms be labeled canonically modulo integral ones,
using only native evaluable maps and fixed-dimensional PPAV algorithms?
If yes, full-suborder EndRing reduces directly to an ABELIAN hidden subgroup
problem. No reference curve, rational quaternion dictionary, primitive hidden
isogeny, large-prime source split or Borel receiver is needed.

The published isogeny-division algorithm gives only an integrality predicate.
The existing NATIVE_MEMBERSHIP.md already proves that the Boolean line-test
interface can require square-root quantum search. That result is reused, not
duplicated. The construction below seeks genuine COSET LABELS, not a renamed
membership bit. It must be evaluated on the same native full-rank input.

## 1. Input And The Finite Abelian Group

Let E be a supersingular elliptic curve in characteristic p>3, and let
alpha_1,...,alpha_4 be genuine efficiently evaluable maps forming a Z-basis
of a full-rank unital suborder R of O=End(E). Include binary degree bounds
B>=deg(alpha_i), evaluation costs and compatible finite-field representations.
The original maps, not their unknown target order, are the computational input.

The small-torsion trace reconstruction from native-suborder-preprocessing
gives the positive trace-norm Gram matrix G. Since disc(O)=p^2,

    d = [O:R] = sqrt(det(G))/p

is an exact positive integer. No quaternion reference is used. d=1 is already
the full-order case. Suppose d>=2. The additive quotient O/R has order d,
so d*O is contained in R. Define

    A = (Z/dZ)^4 = R/dR,
    beta_u = sum_i u_i alpha_i,  0<=u_i<d,
    gamma_u = beta_u/d,
    H = d*O/d*R <= A.

Thus |H|=d and gamma_u-gamma_v is integral exactly when u-v belongs to H.
Changing the chosen residues adds an element of R, so the desired label is
well defined on A. Only the numerators beta_u are native maps; division by d
is NOT performed or assumed integral during source evaluation.

## 2. An Explicit Integral Quadratic Principal Polarization

Write n=d for the denominator and beta=beta_u. On E^2 define

    U_gamma = [[1,gamma],[0,1]],
    L_beta = n^2 U_gamma^dagger U_gamma
           = [[n^2, n*beta],
              [n*beta^dagger, n^2+Norm(beta)]].

All entries of L_beta are actual integral maps available from beta and its
canonical dual beta^dagger=Trd(beta)-beta. It is positive, has Moore
determinant n^4 and trace

    t = 2*n^2+Norm(beta),
    L_beta^2-t*L_beta+n^4*I = 0,
    adj(L_beta) = t*I-L_beta = n^4*L_beta^-1.

Choose ONCE four integers a,b,c,e with a^2+b^2+c^2+e^2=n^4-1. Their
Hamilton multiplication matrix T satisfies T^T*T=T*T^T=(n^4-1)I4.
This is ordinary integer matrix arithmetic, not access to quaternion units
in End(E). Let L4=I4 tensor L_beta, J4=I4 tensor adj(L_beta), and K=T tensor I2.
On E^16 define the Hermitian matrix

    Z_beta = [[L4,K],[K^T,J4]].

Because the tensor factors commute,

    Z_beta^2-t*Z_beta+I16 = 0.

The Schur complement of L4 is I4 tensor L_beta^-1, so Z_beta is positive.
Its inverse is t*I-Z_beta, which is integral. Therefore it defines a
PRINCIPAL polarization on the existing unpolarized E^16. This is an explicit
Zarhin-style matrix construction; no novelty is claimed for stabilization.

For all queries, Norm(beta) <=16*d^2*B. The public uniform bound

    T_max = (2+16*B)*d^2

therefore bounds t, both the largest eigenvalue of Z_beta and the reciprocal
of its smallest eigenvalue. It has polynomial bit length in the native input.

## 3. Integral Translations Give Polarized Isomorphisms

For delta in O, set W=U_delta and V=(W^dagger)^-1. Then

    L_(gamma+delta) = W^dagger L_gamma W,
    adj(L_(gamma+delta)) = W^-1 adj(L_gamma) (W^dagger)^-1.

Consequently diag(I4 tensor W,I4 tensor V) carries Z_gamma to
Z_(gamma+delta) by Hermitian congruence. This gives the required forward
direction of coset equality, but NOT its converse: unframed polarized
isomorphisms can mix factors or change coordinates in additional ways.

## 4. The Frame That Forces The Converse

First state the frame at dimension 16; the implemented converter below
stabilizes eight times, giving dimension g=128.

For each of the two 8-dimensional blocks, distinguish its projection and
ALL matrix units acting on its four-copy multiplicity space, with identity
on the two E coordinates. At dimension 128, replace the multiplicity space
by its 32 copies, including matrix units mixing the eight stabilizing copies.
Label each matrix unit separately; do not allow permutations of frame labels.

An integral automorphism commuting with these operators has exactly the form

    w = diag(I32 tensor W, I32 tensor V),   W,V in GL2(O).

Also fix POINTWISE the inclusion of E into the first E coordinate of one
copy in the first block and the second E coordinate of one copy in the
second block. Hence W*e1=e1 and V*e2=e2.

If w is a polarized isomorphism between Z_gamma^8 and Z_gamma'^8, its
off-diagonal block equation gives W^dagger*V=I. Here T is invertible over Q
because n>=2; its norm is n^4-1. Thus V=(W^dagger)^-1. The two fixed
inclusions force

    W = [[1,delta],[0,1]],   delta in O.

The upper-left block of the polarization equation gives
L_gamma'=W^dagger L_gamma W=L_(gamma+delta), and its (1,2) entry gives
gamma'=gamma+delta. Conversely this same w respects the entire frame when
delta is integral. Thus EXACT framed polarized isomorphism is precisely
equality modulo O. No cancellation of unmarked product factors is assumed.

## 5. Finite Torsion Frames Must Be Relations, Not Ordered Bases

There is a crucial encoding distinction. To specify an operator e without
fixing every point of E^g, mark the UNORDERED relation

    Graph_r(e) = {(P,e(P)): P in E^g[r]}.

Use one separately labeled relation for each frame operator. A common map
w sends this graph to itself iff w*e=e*w modulo r. Marking all P as an
ORDERED tuple would instead force w=I modulo r and destroy the desired
translation invariance. Full graph enumeration costs r^(2g), still polynomial
in a small r at fixed g, but it is an immense cost and must be charged.

For the two fixed inclusions, ordered images of a fixed basis of E[r] ARE
appropriate: they force pointwise agreement on the original E source.
There are no unknown scalar masks in this construction.

Choose separate small marking primes avoiding p and the quotient multiplier,
with product Rmark satisfying

    Rmark^2 > 8*g*T_max^2,   g=128.

If w is any polarized isomorphism between the two stabilized polarizations,
their eigenvalue bounds imply ||w||_op<=T_max in the standard positive
quaternion realization. For a matrix-unit operator e, ||e||_op=1, so

    sum_ij Norm((w*e-e*w)_ij) <= 4*g*T_max^2.

The analogous squared norm for w*iota-iota is <=(T_max+1)^2. If either
integral map vanishes at every marking level, it is divisible by [Rmark].
A nonzero entry of the quotient has positive integer degree, making the
squared norm at least Rmark^2. The bound therefore forces exact commutation
and exact inclusion fixing. Conversely exact agreement holds at all levels.
The finite frame consequently has the same equivalence relation as Section 4.

This uses ONE common polarized isomorphism across all relations, points and
levels. Independent isomorphisms per graph or per level are not permitted.

## 6. Construct The Model Instead Of Assuming It

The previous smooth-repolarization construction applies to ANY positive
integral principal endomorphism Z satisfying Z^2-tZ+I=0. Its algebra does
not require original dimension two once that identity has been established.

Choose a fixed even squarefree D>T_max+2 from small primes away from p.
The nonnegative coin identity

    (t+2)X+(t-2)Y = D^2

and two four-square representations give eight commuting polynomial
coefficients in Z. Their eight-square matrix C satisfies

    C^dagger*C=C*C^dagger=D^2*Z8,
    F=Z8^-1*C^dagger,
    F^dagger*Z8*F=D^2*I,   F*C=C*F=D^2*I.

F is integral. On the OLD product model E^128, calculate its kernel at each
small r^2 dividing D^2. The full primary kernel list has r^(2g) elements.
The direct A26 quotient at N=r^2 is a valid fallback. Prefer the already
proved algebraic refinement in PRIME_SQUARE_FLAGS.md: for a maximal
isotropic primary kernel G, choose a Lagrangian J with rG contained in J
contained in G[r]=(rG)^perp. Quotient first by J, then by the image of G.
Each list has r^g elements. Taking J=rG without checking its dimension is
INVALID for nonfree kernels, including G=E^g[r]. Scalar Frobenius makes
the chosen flag descend; no rational-flag assumption is added here.
Composing the coprime-primary quotients gives q:E^g->Y_gamma and a
proof-only polarized isomorphism

    u_gamma:Y_gamma -> (E^16,Z_gamma)^8,   u_gamma*q=F.

To transport any marking point at prime s not dividing D, evaluate

    tau_gamma(P) = q([D^-2 mod s] C(P)).

This is u_gamma^-1(P) on s-torsion. The underlying isomorphism u_gamma is
not supplied to the algorithm. Transport BOTH entries of every graph pair,
and the ordered inclusion points, by this same tau_gamma.

Canonicalize Y_gamma using the published theta model, transport all marks
by a computed polarized isomorphism to the canonical model, and minimize
the entire ordered collection over ONE automorphism of that model. Within
each graph, sort the pairs as a SET in fixed field coordinates. Retain the
operator labels and the fixed inclusion ordering. Published A7/A22/A25
provide the finite isomorphism/automorphism operations at fixed dimension.

The intended result is now a concrete candidate equality:

    f(u)=f(v)  iff  gamma_u-gamma_v in End(E)  iff  u-v in H.

This equality is the central unreviewed claim, not something established
by checking a matrix identity or by an opaque-label simulation.

## 7. Fields, Uniform Clock And Receiver

Use the same explicit elliptic normalization and genus-one theta conversion
as earlier: one constant-degree base extension with scalar Frobenius and
rational 8-torsion. All original native maps and all constructed operators
are defined there. Auxiliaries use separate extensions: degree <=r(r-1)
for r^2 torsion, <=s-1 for marking s torsion. Temporary joint fields are
polynomial-sized and must be descended after each stage. No giant CRT
torsion compositum or Galois minimization is allowed.

Dimension g=128 is fixed, not input-dependent. Object coordinates, full
kernel lists, full graph relations, quotient encodings and all field degrees
have a uniform polynomial-size bound, with an enormous exponent/constant.
The same fixed-tape argument applies to a complete always-correct expected
label algorithm: cap at twice a uniform expected bound B(L), repeat
h>=ceil(4*log2(d)+log2(1/epsilon)), and freeze one tape. A union bound over
d^4 queries controls all labels together. Reversible evaluation must erase
all root choices, graph enumeration, sorting, field and quotient workspace.
No such circuit has been compiled.

The 32-copy frame has 2*32^2=2048 separately labeled graph relations. At a
marking prime s each graph has s^256 pairs, and each represented point has
4^128 field coordinates in the level-four theta model. These constants and
exponents make the construction impractical. They are not omitted from the
formal polynomial bound. The existing normalization and source-field
arguments must be instantiated at g=128, not quoted with dimension-16
resource numbers. Field encodings preserve the fixed base embedding;
minimizing over Frobenius conjugates would change the equivalence relation.

Source evaluation calls the four native alpha_i maps and group operations
to evaluate beta_u, at a cost polynomial in log(d) and the paid evaluator
costs. Norms and duals are obtained from the trace table, not by finding a
kernel of exponential degree. C and F have entries that are polynomials in
Z with polynomial-bit coefficients. Keep quotient compositions as flattened
lists or bounded straight-line evaluators; expanding rational functions of
their exponentially large degrees is not a polynomial implementation.

Standard finite-abelian HSP sampling on (Z/d)^4 then gives characters in
H^perp. Modular linear algebra recovers H, with repetition and precision
costs charged. The receiver does not need large geometric torsion or a
nonabelian Fourier transform. This is the familiar abelian HSP algorithm,
not a new quantum measurement claim.

If h_j are recovered generators represented in Z^4, form the integer lattice
Gamma generated by d*e_i and h_j. Then (1/d)*Gamma in the alpha basis is O.
For exact recovery, det(Gamma)=d^3 because |H|=d. Incomplete annihilator
sampling gives a supergroup of H and can be detected by this index check.
Also verify integrality of the four proposed output maps using the published
isogeny-division algorithm. Together with the exact index/discriminant,
integrality certifies the full order, rather than merely a subgroup size.

## 8. Strongest Attacks And The Scope Limit

- Prove the frame centralizer and congruence converse in the FULL unknown
  maximal order, not just in scalar or Gaussian matrices.
- Try to produce framed-isomorphic gamma,gamma' with nonintegral difference.
  Unframed collisions are expected and do not suffice to falsify the framed
  construction. Pointwise graph encoding that kills legal translations is
  equally fatal and must have a negative control.
- Check the quadratic principal polarization, positivity and integrality
  before applying any formal eight-square certificate.
- Audit small-prime-square quotient handling and separate-field descent.
  The dimensions/kernel lists cannot be hidden as constant-cost oracles.
- Match classical access to the original curve, all native maps and the
  entire computed label, not merely equality bits. A Boolean-interface
  lower bound is NOT a lower bound for this native problem.
- Check the latest full-suborder literature. Heuristic quantum-polynomial
  solutions already exist. A potentially heuristic/GRH-free additive
  construction would be a different source argument, not a first solution.
- The input still requires FULL RATIONAL RANK. From one endomorphism only
  the quadratic subalgebra is accessible; this cannot manufacture a second
  noncommuting map. For that restricted span the construction would at most
  recover its integral saturation, closely related to known primitivisation.
- No Shor-level result or practical cryptographic attack follows from the
  current finite controls or from the availability of a polynomial receiver.

## 9. Dependencies And Status

Core imported results: the represented-PPAV algorithms of
[Corte-Real Santos--Piasecki--Wesolowski](https://eprint.iacr.org/2026/1142),
unconditional expected-polynomial four-square algorithms, finite-abelian
HSP, and [isogeny division](https://arxiv.org/html/2309.11912v4#S4).
The endpoint conversion and generic quadratic norm certificate are existing
local constructions; their general field/backend integration is unexecuted.

Comparison: [Chen et al.](https://arxiv.org/abs/2305.19897) and
[Chen--Petit](https://research.birmingham.ac.uk/en/publications/computing-the-endomorphism-ring-of-a-supersingular-elliptic-curve/)
already provide quantum isogeny/full-suborder results. No claim of absence
from their work or subsequent literature follows from a keyword search.

This note records a new proposed source mechanism. It is not a repaired or
independently reviewed version of the earlier Sp4 theorem. No new reviewer
has been authorized for it. Keep all proof and execution claims provisional.
