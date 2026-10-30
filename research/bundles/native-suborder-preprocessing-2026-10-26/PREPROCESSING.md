# Native Full-Suborder Preprocessing: A Proposed Theorem Repair

2026-10-26. This is a written reduction, with exact interface controls, not
an executed native EndRing algorithm or a proof of novelty. No new independent
review was performed. The earlier reviewer did not inspect this repair.

## Decision

The reference curve, full source order and rational dictionary need not remain
unexplained advice. A proposed preprocessing construction is given below.
It uses quantum factoring and established rational-algebra algorithms; general
characteristic retains a GRH-dependent small-CM construction. The downstream
geometric source and its uniform-clock proof remain imported obligations.

The useful potential contribution is an assumption-removing construction for
an ALREADY STUDIED quantum full-suborder problem. It is not the first quantum
algorithm for that problem, an algorithm from one endomorphism, or evidence
of classical hardness. Do not create a breakthrough claim from this bundle.

## 1. Native Input And Exact Output

Input consists of p>3, an explicit finite field k of characteristic p, a
supersingular E/k, and four actual efficiently evaluable endomorphisms
alpha_i forming a Z-basis of a full-rank unital suborder R of geometric
End(E). Include a binary upper bound B>=1 on all deg(alpha_i), together with
the evaluator encodings and their polynomial evaluation bounds. The input
length L includes log(B), field representations, and those encodings.

An arbitrary program's length does NOT certify its degree or running time.
Genuine geometric maps, full rank, the degree bound, and efficient evaluation
are promises of this mathematical input model. Finite matrix transcripts
cannot authenticate those promises for an arbitrary adversarial program.

Wanted preprocessing output:

- An explicit reference E0 and full evaluable O0=End(E0), with its table.
- The table of R and a unital rational algebra map
  theta:O0 tensor Q -> R tensor Q=End^0(E).
- A positive N and integral coordinates of theta(N*b_i) in the alpha basis.
- Explicit compatible fields and charged evaluators for the four maps.

Neither End(E), a connecting isogeny, its kernel, a weak-isogeny oracle nor
large-prime target torsion is an input or an intermediate preprocessing call.

## 2. Recover The Target Algebra From Small Torsion

At primes r!=p, generate E[r], choose a basis, and evaluate the four original
alpha_i on its two points. Obtain four 2x2 matrices A_i(r). All coordinate
tables have size r^2, used ONLY at small auxiliary r.

For a word w in the basis of length at most three, matrix trace modulo r is
the reduced trace of the corresponding geometric endomorphism. Norm
multiplicativity and definiteness give

    |Trd(alpha_i1 ... alpha_it)| <= 2 sqrt(B^t) <= 2 B^2,  1<=t<=3.

Use distinct small primes whose product M>4 B^2. CRT centered in (-M/2,M/2]
then recovers these INTEGER traces uniquely. Only O(log B) bits of combined
modulus are needed; the largest chosen prime is polynomial in L. Excluding
p changes no asymptotic bound. Even when r divides the suborder discriminant,
the trace equation remains valid; no split inverse at such a level is used.

Write t_i=Trd(alpha_i), T_ij=Trd(alpha_i alpha_j), and
u_ijk=Trd(alpha_i alpha_j alpha_k). T is nonsingular because the four maps
span the quaternion algebra. The coefficients c of alpha_i alpha_j satisfy

    T c = (u_ij1,...,u_ij4)^T.

Similarly the unit coordinates solve T*one=t. Canonical conjugation is
alpha_i^*=t_i*one-alpha_i. This recovers the whole multiplication, unit and
involution table without dual-map evaluators or an unknown maximal order.
The implementation checks integer coordinates, associativity, the positive
trace-norm form, basis degree bounds and agreement with every transcript.

Field cost is real. First place the native maps over their declared common
field, then use the existing elliptic-field-normalization argument. Under
scalar Frobenius, separate r-torsion fields have degree <=r-1. Do not form
their compositum. Root finding, point generation, matrix coordinates and
each original evaluator are charged. Standard rational linear algebra in
fixed dimension has polynomial output height and bit cost.

## 3. A Fully Specified Reference When p=3 Mod 4

Take E0:y^2=x^3-x over F_p, NOT an arbitrary same-j curve with a basis copied
unchanged. Over F_(p^2), let zeta^2=-1, i(x,y)=(-x,zeta*y), and pi be p-power
Frobenius. Then

    i^2=-1,  pi^2=-p,  pi*i=-i*pi.

All three nonzero 2-torsion points have x=0,+1,-1 over F_p. Therefore
1+pi annihilates E0[2], and h=(1+pi)/2 is an integral endomorphism. The maps

    1, i, h, i*h

generate an order of discriminant p^2. Since E0 is supersingular and its
geometric endomorphism ring has that same discriminant, this is the full O0.
Closure and discriminant follow directly from the displayed quaternion
relations. This is the order in the existing odd_maximal_order(p) fixture.

Evaluation is constructive. For an input P, find any Q with 2Q=P by
constant-degree polynomial equations over a bounded-degree extension, then
return Q+pi(Q). Changing Q by T in E0[2] changes this by T+pi(T)=0. The
result descends to the field of P, because h is defined over F_p. Fixed-degree
root finding, Frobenius, field embeddings and descent have polynomial cost.
General field-extension evaluation is a written algorithm, NOT implemented
by the finite reference_half_frobenius control.

Counterexample: on y^2=x^3+x at p=7, the 2-torsion point (zeta,0) is sent by
pi to (-zeta,0); their sum is nonzero. Consequently 1+pi does not annihilate
E[2] and that same half-Frobenius formula is not integral. Geometric
isomorphism of curves does not transport a Frobenius-labeled order for free.

## 4. General Reference Via Small CM: Retain GRH Explicitly

The following is a composition argument, not a claim that the curve-only
constructor supplies a full endomorphism basis automatically.

Use Bröker's Algorithm 2.4 to choose an imaginary quadratic field of small
discriminant D<0, inert at p, with odd class number, and a CM j-invariant in
F_p. Its published polynomial bound uses GRH. In the general branch
D=-q for a prime q=3 mod 4 with (-q/p)=-1 and q=O(log^2 p) under GRH.
The polynomial H_D, its finite-field root and a supersingular E0/F_p are
computable in polynomial time under that bound.

For sufficiently large p, require the checkable inequality p>4*q^2. This
also implies q<p and p does not divide D or c=(q+1)/4. Under the effective
GRH bound q<=C*log^2(p), failure of this inequality occurs in only finitely
many effectively bounded characteristics. A finite exhaustive EndRing
fallback suffices there for the asymptotic theorem; it is not a practical
algorithm and is not implemented. Without the small-q bound, do not describe
that fallback as polynomial in log p.

Additional construction of the CM map:

1. A reduction embedding gives omega=(1+sqrt(-q))/2 in End(E0), with
   omega^2-omega+c=0. The Frobenius relation is a SEPARATE requirement;
   the argument immediately below proves it for p>4*q^2. Test both
   relations, not an arbitrary orientation label from H_D.
2. Find such an omega by enumerating all degree-c isogenies from E0 and
   endpoint isomorphisms back to E0. All subgroup kernels of E0[c] may be
   enumerated; a cyclic-kernel shortcut is not needed. E0[c] has c^2 points,
   scalar Frobenius gives an extension of degree <=phi(c), and subgroup
   enumeration in a rank-two module is polynomial in c. Enumerating every
   pair of generators and retaining groups of order c is one crude bound.
   Include the at most six endpoint isomorphisms over bounded extensions.
   Use explicit maps or sufficiently large paid torsion to check the stated
   polynomial identities with a degree bound. An actual CM embedding
   guarantees a successful candidate. This enumeration is polynomial in
   the VALUE of c, which is polynomial in log p only under the small-q bound.
   In particular, the quadratic relation has norm O(c^2), and, once it
   holds, the Frobenius commutation difference has norm <=4*p*c. Vanishing
   on all two-dimensional torsion at distinct small levels with product
   squared exceeding those bounds certifies a zero map. It does not require
   listing a subgroup of order proportional to p.
3. S=Z[omega]+Z[omega]*pi is a known full-rank evaluable suborder of index
   |D| in End(E0): the trace discriminant is D^2*p^2. We still have not
   assumed that S is maximal.
4. Saturate its LATTICE using only small-prime native divisibility tests.
   If the remaining index d>1, choose ell|d. Enumerate nonzero coefficient
   vectors a modulo ell in the current four-element lattice basis. The
   quotient a/ell is integral exactly when a kills E0[ell], since ell!=p.
   Some such class must exist because End(E0)/L has ell-torsion. Adjoin it
   and use HNF; the lattice index drops by ell. Repeat until d=1. Intermediate
   lattices need not be closed orders. The final lattice is the full ring.

All tested primes are <=|D|. There are <=log2|D| enlargements; each has at
most ell^4 tests on ell^2 points. Degrees, coefficient heights and field
costs are polynomial in |D| and log p. For evaluation, flatten the final
basis into a numerator in S divided by a divisor of |D|; use a single
division-preimage calculation and descent. Do not recursively accumulate
one extension per saturation operation.

This construction does NOT saturate the large-index target R by enumeration.
It saturates ONLY the small-index, specially constructed source order.

### Why Frobenius Anticommutes: The Additional Self-Review Repair

Let I=2*omega-1 and J=pi*I*pi^-1. Because E0 is defined over F_p, conjugation
by its Frobenius is the Galois action on geometric endomorphisms. Thus J is
integral despite the rational inverse in this notation. Both I and J have
trace zero and norm q.

If they do not commute, the lattice Z[1,I,J,IJ] is a rank-four order. Put
t=Trd(IJ). Its relations are I^2=J^2=-q and IJ+JI=t. The trace-pairing
determinant is -(4*q^2-t^2)^2; hence its reduced discriminant is

    d = 4*q^2-t^2,    0<d<=4*q^2.

An order contained in End(E0) has reduced discriminant a positive multiple
of p. Therefore noncommutation would imply p<=4*q^2, contrary to the
chosen inequality. They commute. The centralizer of I is its quadratic
field, so the trace-zero, norm-q element J in that field is either I or -I.
The plus sign would put I in the centralizer Q(pi)=Q(sqrt(-p)); this is
impossible because q and p are distinct primes. Consequently J=-I and
pi*omega=(1-omega)*pi as required.

This avoids assuming that an arbitrary same-j model carries a particular
CM orientation from a class-polynomial label. The small-characteristic
condition is essential to this proof. The controls at p=7,11,23 construct
noncommuting pure equal-norm pairs whose reduced discriminant is exactly p;
one cannot remove the inequality using the discriminant formula alone.

For p=3 mod 4, Section 3 avoids GRH entirely. Other small fixed-CM branches
can also avoid it, but the theorem below claims the unqualified restricted
branch only for p=3 mod 4. Without GRH or a supplied small-CM certificate,
the general bound is polynomial in q and log p, not proven polynomial in
log p. Finding a curve is not enough: constructing its full evaluable order
was an essential separate step above.

## 5. Rational Dictionary Without A Norm-Distribution Heuristic

Let A=O0 tensor Q and B=R tensor Q, both isomorphic to B_(p,infinity).
Apply Ivanyos--Ronyai--Schicho, Theorem 1 and Corollary 10, with ground
field Q and fixed degree. These give an explicit isomorphism using integer
factorization and finite-field polynomial-factorization oracles. Shor handles
the former; randomized polynomial-time finite-field methods handle the
latter. All calls and input lengths are charged. No GRH is needed here.
The theorem's fixed discriminant is that of the NUMBER FIELD Q, namely 1;
it is not a requirement that the quaternion discriminant p be bounded.

One realization splits C=A tensor B^op as M4(Q). If L_a,R_b are its commuting
actions on V=Q^4, choose v!=0. Both a->L_a*v and b->R_b*v are invertible:
A,B are division algebras and a nonzero element cannot kill v. Therefore

    theta = [R_b1*v ... R_b4*v]^-1 [L_a1*v ... L_a4*v]

is a unital algebra map A->B. Right actions have REVERSED multiplication;
using ordinary left actions is wrong. The implementation checks this and
faithfulness. It implements extraction from supplied actions, not the tensor
splitter. This supplies no small norm, ideal generator or target maximal order.

The EHLMP Algorithm 6 discussion names a quadratic-form runtime assumption
in addition to the factorization heuristics. Rather than silently resolve
that wording via Chen--Petit's Remark 17, this argument uses the explicit
fixed-dimension algebra theorem above. This is a citation/assumption repair,
NOT a new algebra-isomorphism algorithm.

## 6. Clear Denominators And Freeze Native Evaluators

Write theta(b_j)=sum_i C_ij*alpha_i. Let N be the lcm of all denominators of
C. Then NC is integral and theta(N*b_j) is a known integer combination of
the ORIGINAL maps. Binary scalar multiplication, curve addition and the
original evaluators implement it. The same holds for N*b_j at E0.

Rational fixed-dimensional arithmetic gives polynomial log N and coordinate
lengths; N itself may be exponentially large. No step enumerates N-torsion.
The inclusion need not be primitive, and N may contain p. Factor N using
charged quantum factoring; set m=N/p^v_p(N). The earlier primitive global
map argument gives D_psi|p*m, regardless of the chosen dictionary.

Construct a common base field for E and E0 with explicit embeddings. The
constant-degree elliptic normalization and theta normalization from the
preceding bundles apply. Preprocessing randomness is sampled and verified
before the coherent source is frozen. The uniform whole-label clock still
has to be the one in UNIFORM_SOURCE_CLOCK.md, not a test runtime estimate.

## 7. End-To-End Conditional Statement

PROPOSED COMPOSITION, not independently reviewed after these repairs:

For the native input in Section 1, assuming GRH in the general-reference
branch and the stated published represented-PPAV algorithms with the uniform
contracts used by the preceding source construction, the preprocessing above
reduces native full-suborder EndRing to the augmented-input problem in
SUBORDER_TRANSCRIPT.md in quantum polynomial time in L. For p=3 mod 4 the
reference construction does not require GRH.

Composing with the earlier argument gives a proposed bounded-error quantum
polynomial-time algorithm for a full basis of End(E), with efficient native
evaluators under the published endomorphism-division interface. The steps are:

1. This preprocessing gives E0,O0,theta,N and small-level native actions.
2. Source-algebra splitting and the 2m lift construct the query coordinates.
3. The dimension-16 prime-only polarization construction and JOINT marked
   canonicalization give the exact hidden-stabilizer fibers, on a good frozen
   random tape. Marking bounds use p*m, not m. Fields are kept separate.
4. Unknown local depths and ring-Fourier recovery determine the separable
   kernel. Small-prime cases also have the existing classical prefix attack.
5. The annihilator ideal gives the exact pulled-back target order. Apply
   theta and the published division algorithm to obtain native evaluators.

If m=1 there is no separable hidden kernel to recover: the unique ramified
local maximal order and the unramified local equality already imply
theta(O0)=End(E). The procedure must bypass, not instantiate, a nontrivial HSP.

The conditional source theorem is a necessary premise here. This note does
not independently prove every geometric or Fourier lemma in that chain.
Full theta-quotient/canonical-label execution and general field-tower
integration still have not occurred. A mathematical reduction using imported
algorithms need not implement them, but its finite receipts must not be
reported as their execution.

## 8. Attempt To Falsify The Improvement

- Prior art already solves full-suborder EndRing heuristically in quantum
  polynomial time: Chen--Petit, EUROCRYPT 2025, Theorems 1 and 3. The potential
  improvement here is removing particular norm-solving/powersmooth heuristics
  through a different source, not introducing the problem or its quantum HSP.
- The reference remains GRH-dependent in general. A statement that all
  heuristic/conditional inputs disappeared is false. Even in the restricted
  branch, later proof errors remain possible; the source is not formally checked.
- Tensor splitting is algebraic preprocessing, not a hidden target-order
  oracle. It need not map O0 to End(E); precisely the resulting large-index
  mismatch is what remains for the quantum algorithm. If an implementation
  used an order-preserving isomorphism instead, it would be circular.
- Target lattice saturation by enumerating large ell would be exponential
  in log ell. This argument restricts enumeration to the small-CM reference.
- Four maps generating only a commutative quadratic algebra fail the rank-four
  gate. Nothing here constructs a second noncommuting target endomorphism.
- The single geometric dictionary is essential. Independent local changes
  without a global theta do not satisfy the primitive-isogeny lemma.
- Finite trace consistency is not provenance. Fake locally consistent maps
  or a false degree bound are outside the promised input; a real ingestion
  layer must not bless arbitrary evaluator code because these tests pass.
- Classical competitors should receive the same factorizations and reference
  data. Any benefit that vanishes under that matching is factoring access,
  not a new hidden-stabilizer advantage. No native classical lower bound is
  established, even when the kernel modulus has a large prime factor.
- The r^16 subgroup lists and enormous fixed-dimensional constants remain.
  The asymptotic argument is not a useful cryptographic runtime estimate.

Falsifiers for the proposed repair: a legal full-rank native input for which
the trace reconstruction differs from the actual composition table; a failure
of the small-CM orientation or source saturation with the stated bounds; an
input-size-dependent field/algebra dimension hidden in the cited theorem; or
a failure to compose the geometric routines with a uniform polynomial clock.
The supplied tests address only selected finite versions, not all these claims.

## 9. Actual Execution And Next Research Decision

Implemented: trace-to-order reconstruction, exact rational dictionary checks,
extraction from a SUPPLIED split tensor representation, denominator clearing,
and a finite native half-Frobenius control. Tests include changed bases,
opposite-algebra direction, insufficient CRT precision, corrupted transcripts,
rank-two rejection and the same-j reference trap.

Not implemented: the cited rational tensor splitter, general CM map search
and source saturation, general field towers, a native end-to-end label,
coherent recovery, or any quantum hardware experiment.

Next reasoning priority: put the combined theorem into one independently
checkable manuscript and compare the exact assumption improvement against
current literature. Do not add another easy supplied-map sweep. The broader
OneEnd/EndRing barrier is still obtaining native noncommutative information;
neither a full-rank suborder theorem nor a polarization control resolves it.

## Primary Sources Retained Or Checked

- [Chen--Petit, accepted manuscript](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/259384467/suborder_to_endomorphism_ring_2_.pdf):
  Sections 2.2--2.3, Remark 17, Theorems 1 and 3; retained in the earlier
  large-prime-source-audit bundle. Novelty comparison is not exhaustive.
- [EHLMP, 2018](https://pure-oai.bham.ac.uk/ws/files/47705132/Supersingular.pdf):
  Algorithm 6, Lemmas 4--7, Proposition 6 and the paragraph immediately
  following it; retained here. The PDF includes a repository cover sheet.
- [Ivanyos--Ronyai--Schicho, arXiv:1106.6191v3](https://arxiv.org/pdf/1106.6191):
  Theorem 1, Section 4 and Corollary 10; retained here. K=Q and n=2 are fixed;
  the tensor matrix size is 4, not an input-dependent dimension.
- [Csahok--Kutas--Montessinos--Zabradi, 2022](https://link.springer.com/article/10.1007/s40993-022-00380-3):
  Section 4 confirms the rational factoring-oracle route. Its Proposition 4.1
  requires maximal orders and is NOT applied directly to the target R.
- [Bröker, Constructing supersingular elliptic curves](https://gkorpal.github.io/files/broker-supersingular.pdf):
  Theorems 1.1 and 2.1, Lemmas 2.3 and 2.5, Algorithm 2.4; retained here.
- [Corte-Real Santos--Piasecki--Wesolowski, 2026/1142](https://eprint.iacr.org/2026/1142):
  represented-PPAV primitives, retained in ppav-source-2026-10-23. This note
  imports the same version as the combined-source review, not a new backend.
