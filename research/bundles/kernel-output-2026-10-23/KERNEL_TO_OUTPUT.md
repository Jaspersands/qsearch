# From An Abstract Kernel To Full Algebraic Output

2026-10-23. Constructive deduction with exact arithmetic controls.
Independent mathematical and prior-art review pending. This is classical
postprocessing of a supplied, correct kernel, NOT a way to recover that
kernel, an executed geometric algorithm, or a new quantum speedup.

## Decision

The proposed surface receiver need not stop at an abstract Lagrangian.
Its output determines the FULL Hermitian Hom module and the FULL transported
endomorphism order in polynomial bit complexity. In particular, a
generic abstract-order-to-module conversion, principal ideal solver, or
GRH is unnecessary for these algebraic outputs. A simpler direct module
construction supersedes the initially considered order-first approach.

There are two independently implemented reconstructions of the order:
prime-square block congruences, and the left order of the module. They
agree in the tested cases. No large-prime torsion points are constructed.
The surface source and the complete quantum composition remain proposals.

## 1. Input And Output Contract

Let A=E^g and let phi:A->B be an ell-polarized isogeny of PPAVs, where
ell is an odd prime different from the characteristic p. Thus

    phi^dagger phi = ell,     phi phi^dagger = ell.

Use geometric endomorphisms throughout, over an algebraic closure of the
paid field of definition. Do not silently replace them by endomorphisms
over a smaller field. To use the maximal-supersingular module conversion
literature over F_(p^2), impose its field and reference-curve hypotheses
separately. The current geometric-source proposal has g=2 and odd p.

Inputs beyond the modeled original A,B and weak evaluator are:

- The FULL O=End(E), as a rank-four integral quaternion order, including
  multiplication, conjugation, and its specified action on E. Put R=M_g(O).
- The specified split O/ell O -> M_2(F_ell), extended to R. This identifies
  A[ell] abstractly with F_ell^(2g). It is not a point basis on A[ell].
- The CORRECT kernel K, as g independent columns in that representation.
  It must be Lagrangian for the product alternating form. The proposed
  quantum receiver must certify K using the real source oracle first.

The algebraic algorithms output an integral basis and O action for the
full Hom(E,B), its quaternion-valued Hermitian form, a basis/multiplication/
involution for the full End(B) inside End^0(A), and the abstract morphism
corresponding to phi. These descriptions have polynomial bit length.
Full geometric evaluation at arbitrary points is a separate conversion
task. Auxiliary prime-to-ell evaluations of End(B) follow directly below.

Any Lagrangian produces internally consistent outputs. Algebraic tests
cannot tell whether it is the secret kernel of the supplied weak phi.

## 2. Direct Full Hom Module: Only Modulo ell Is Needed

View a column a in O^g as a morphism E->A. Define the integral right module

    J_K = {a in O^g : image(a on E[ell]) is contained in K}.

Then the correspondence

    a |-> eta_a = phi a / ell

is an isomorphism J_K -> Hom(E,B) of right O-modules.

Proof of integrality: phi a kills E[ell], hence factors uniquely through
the separable multiplication map [ell]:E->E. Its quotient is eta_a. This
is a morphism, not merely a rational quasi-morphism. Conversely, for EVERY
eta:E->B, set a=phi^dagger eta in O^g. Then phi a=ell eta, so a(E[ell]) is
contained in K and eta=eta_a. This also proves fullness and injectivity.

Pull back Hom(E,B) into D^g, D=O tensor Q, by phi^(-1):

    M_K = J_K / ell,       h(x,y)=ell x^dagger y.

For numerator columns a,b this means h(a/ell,b/ell)=a^dagger b/ell.
The norm is positive definite. Integrality follows either geometrically
from eta_a^dagger eta_b or from the isotropy of K modulo ell.

The module is Hermitian unimodular, not necessarily unimodular as an
ordinary trace lattice. Indeed O^g subset M_K subset ell^(-1)O^g. Taking
the h-dual preserves those bounds. A candidate a/ell belongs to that dual
exactly when a^dagger b=0 mod ell for every b mapping into K. The full
split matrix algebra makes this equivalent to image(a) subset K^perp.
Consequently

    M_K^# = M_(K^perp) = M_K.

This gives a direct proof without computing a free O-basis or invoking a
module equivalence algorithm. For the Hurwitz fixture the rank-eight
trace Gram determinant is 16, NOT 1. For characteristic-p fixtures it is
p^4. Treating those determinants as a failed polarization would be wrong.

### Computation and size

The reduction O^g/ell -> M_(2g,2)(F_ell) is an isomorphism of vector spaces.
Matrices with both columns in K form a space of dimension 2g. Lift a basis,
adjoin ell times the 4g standard integer basis vectors, and take column HNF.
This computes a basis J with

    [O^g:J_K] = ell^(2g),       rank_Z(J_K)=4g.

Right O-action and h are exact multiplication followed by basis change.
All matrix dimensions are polynomial in g, all entries have polynomial
bit length in the supplied algebra and log ell. Fixed g is the current
geometric application; no polynomial-in-g theta algorithm is inferred.

The known source module O^g maps into M_K by inclusion. This is precisely
the abstract phi because phi^(-1) phi y=y. Its Hermitian multiplier is
ell. In integral coordinates its matrix is ell*J^(-1), with integral
entries and determinant of absolute value ell^(2g).

The literature often uses LEFT modules Hom(B,E), not our right modules.
Take adjoints: represent this left module by rows J_K^dagger, with form
(r,s) |-> r s^dagger/ell. The contravariant morphism induced by phi is the
inclusion J_K^dagger -> O^g (rows). Mixing the two conventions changes the
action and is not an innocuous transpose.

## 3. Full Transported Endomorphism Order

Let R_B=phi^(-1) End(B) phi. Every x in R_B satisfies

    a=ell*x=phi^dagger beta phi in R,

so R_B is contained in (1/ell)R. At ell, write Lambda=T_ell(A) and identify
phi^(-1)T_ell(B) with

    L = Lambda + (1/ell)*K_tilde.

Here K_tilde consists of any lifts of K. Their choice is irrelevant to L.
For x=a/ell, the condition xL subset L is exactly

    a Lambda subset ell Lambda + K_tilde,
    a K_tilde subset ell^2 Lambda + ell K_tilde.

In a basis whose first g vectors lift K, write a=[[A,B],[C,D]]. Then

    A = D = 0 mod ell,    C = 0 mod ell^2,    B unrestricted.

Let I_K be the preimage of these congruences in R. Then

    R_B = I_K/ell,       [R:I_K]=ell^(4g^2).

Necessity follows from the displayed lattice action. For sufficiency,
gamma=phi a phi^dagger is an actual endomorphism of B. The lattice
condition says gamma T_ell(B) subset ell^2 T_ell(B), so gamma kills
B[ell^2]. Factoring through [ell^2] gives the genuine endomorphism
beta=gamma/ell^2. There is no unproved global saturation oracle here.
At primes different from ell, the original lattice remains unchanged.

The Rosati involution on this transported algebra is the source adjoint:
phi^dagger=ell phi^(-1) makes the multipliers cancel. For Lagrangian K the
order is adjoint-stable. A non-Lagrangian control violates this and the
Hermitian integrality test, although an unpolarized lattice still exists.

Two tempting shortcuts fail: a preserving K modulo ell does NOT imply
a/ell is in R_B; even imposing A,D,C divisible by ell misses the second
power needed in C. The tests include both failures.

### Compatible splitting modulo ell^2

The block formula must not assume a secret geometric ell^2-point basis.
Lift E11 through the known order presentation to e0, and set

    e = 3 e0^2 - 2 e0^3 mod ell^2.

Since e0^2-e0 is divisible by ell, e is an idempotent. The left ideal Oe
has rank two over Z/ell^2, with basis e and t*e, where t lifts E21.
Left multiplication on this basis produces a split O/ell^2 -> M_2(Z/ell^2)
that reduces to the specified split. Solve using a coordinate minor that
is a unit modulo ell and verify all coordinates and multiplication.

Different compatible split lifts differ by inner conjugacy congruent to
a scalar modulo ell. After scaling, their conjugator is I+ell X; it
preserves both Lambda and L. Therefore it does not change I_K. The tests
vary idempotent lifts, compatible inner conjugacies, kernel lifts, bases
and complements, obtaining identical integer HNF lattices.

### Independent route: no prime-square splitting

Use the module left order instead. For each basis element a of R, let L_a
be its rational 4g-by-4g left action. The numerator lattice J contains
ell O^g and is contained in O^g, so

    F_a = ell J^(-1) L_a J

has integer entries. The condition (a/ell) M_K subset M_K is precisely
F_a=0 mod ell^2. Flatten the matrices into columns of an integral F and
compute the congruence kernel {c:F c=0 mod ell^2}. One exact implementation
uses lattice duality: this kernel is the dual of

    Z^(4g^2) + (F^T/ell^2) Z^((4g)^2).

Column HNF and rational inversion suffice. This supplies an independent
check of the block formula and removes any need to use the ell^2 split in
a future production postprocessor. Both routes are implemented here.

## 4. Evaluating Target Endomorphisms Without Recovering Weak Scalars

For a basis numerator a in I_K and beta=phi(a/ell)phi^(-1), take accessible
auxiliary torsion of order r coprime to p*ell. Let W=u_r*phi_r be the
supplied weak action matrix, with ONE unit u_r for the full basis. Then

    beta_r = ell^(-1) W a_r W^(-1).

The weak unit cancels. The source order evaluates a_r; paid small-level
torsion coordinates and discrete logarithms give evaluations on B[r].
The same identity works at prime powers coprime to ell. Independent masks
on different basis vectors do not cancel, and tests detect the failure.

This is a full order with a specified auxiliary evaluation correspondence,
not merely an isomorphic abstract order. It still does NOT evaluate
arbitrary points, handle inaccessible ell-torsion, or directly expose an
explicit large-prime kernel. Those stronger outputs are not implemented.
The construction does not strengthen a classical adversary before K is
known. Granting this full order as input would be circular: the existing
transport/divisibility attack already recovers K from it.

## 5. Complete Surface Candidate: What Is Now Connected

The proposed composition has three stages:

1. The smooth-repolarization bundle supplies a proposed exact marked oracle
   for m in Sp_4(F_ell), with equality exactly when mK=nK. Its geometry is
   stabilized to dimension 16, but the acting group remains Sp_4.
2. The field-chart reduction uses two degree-two, three-output-coordinate
   prime-field HPGP learners, followed by the global unipotent certificate.
   Odd ell makes degree two valid. It is not a general nonabelian HSP solver.
3. The present classical postprocessor returns the full module/order above.

For the receiver's ideal oracle, a bounded attempt succeeds with probability
at least 3/8. R attempts have failure at most (5/8)^R, with separate budgets
for source errors, field arithmetic, learner cutoffs and circuit error.
Do not assume an adaptive stochastic oracle is automatically coherent.
The source still needs uniform public lift bounds and a single bounded
coherent implementation with consistent canonical labels. Correctness on
an observed finite sweep is insufficient.

The published HPGP dependency is [Ivanyos--Santha, Theorem 5 and Corollary 6](https://arxiv.org/html/1503.09016).
The local tests do not run that learner. The opaque-label classical query
lower bound in the receiver note does NOT establish classical hardness
of theta/geometric labels, or hardness of the weak-isogeny input.

## 6. Existing Literature And Stronger Output

Kernel ideals and Hom-module transport are established mathematics; this
note claims a missing project-specific output contract, not novelty for
those correspondences. The [Hurwitz order](https://jvoight.github.io/quat/quat-book-v0.9.14.pdf)
is a maximal order at discriminant 2; the odd-p fixtures use
Z[1,i,(1+j)/2,(i+ij)/2] in (-1,-p), p=3 mod 4, with trace discriminant p^2.

[Chen et al.](https://arxiv.org/html/2305.19897) already study weak isogeny
representations and polynomial quantum IsERP algorithms in dimension one.
The possible contribution here is the dimension-two source/receiver
composition, not the premise that weak evaluation can expose an
endomorphism ring quantumly. This does not solve bare-curve isogeny search,
general DCP, or generic lattice cryptography. No cryptosystem break follows
without checking that system's exact public input against the contract.

[Page--Robert--Soumier, 2026/276](https://eprint.iacr.org/2026/276), Section 6.3,
gives module-to-geometric conversion and explicit Hom actions in Theorem 6.9.
The direct module above avoids the separate abstract-order standardization
and PIP step. This is a plausible route to stronger output on the original
model: convert the module, align the resulting polarized model to B, and
transport the resulting maps. Its exact reference-curve, finite-field,
input-height, and correspondence requirements still need a composition
audit. No geometric converter was executed here. In particular do not
blanket-import the GRH-qualified unpolarized-isomorphism Corollary 6.11
when a different module-output theorem is sufficient.

## 7. Adversarial Review And Next Decisive Work

- **Not the right kernel:** every Lagrangian yields a valid module. Only the
  actual oracle's final certificate links it to the secret phi.
- **Only a source suborder:** the preimage no longer proves full Hom or End.
  Full O and compatible geometric evaluation are essential input promises.
- **Only mod-ell saturation:** explicitly falsified by the lower-left block.
- **Incorrect polarization or adjoint:** non-Lagrangian controls fail. The
  module is Hermitian self-dual, not trace-unimodular over Z.
- **Wrong weak interface:** independent point masks and ell-primary levels
  invalidate the auxiliary evaluator. These are rejected, not averaged out.
- **Hidden cost:** the 127-bit test only checks fixed-rank algebra. It says
  nothing about theta geometry cost; stabilization has enormous constants.
- **Classical recovery:** full target-ring advice already destroys the
  intended secrecy. The new postprocessor does not provide that advice
  without K. Classical attacks on the real source remain unresolved.
- **Prior art:** the elliptic analogue is already known. The surface
  composition needs a full novelty comparison and external mathematical
  review before being described as a new algorithm.

Next highest-value work is an adversarial review of the source lemma and
the exact label construction, then an access-matched classical attack on
those labels. Do not spend another pass enlarging output schemas. An honest
small geometric equality check would validate a missing layer, but it must
not be advertised as quantum advantage or evidence of classical hardness.

## 8. Verification Scope

See VERIFICATION.md and kernel_output_receipt.json for actual runs.
Fixtures include full quaternion orders, a global algebraic norm-13
isogeny with independently known transported lattices, wrong-saturation
countercontrols, and a 127-bit prime. No curve-point or theta backend was
used. No moving repository file, registry, CLI or UI was edited.
