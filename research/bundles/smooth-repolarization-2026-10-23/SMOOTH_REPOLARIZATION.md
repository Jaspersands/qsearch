# A Smooth Stabilized Repolarization For The Surface Source

2026-10-23. PROPOSED SOURCE LEMMA; INDEPENDENT REVIEW PENDING.
Exact algebraic certificates are implemented. Geometric quotients, theta
canonicalization and a quantum receiver have NOT been executed. No novelty,
cryptanalytic success, or quantum speedup is admitted.

## Decision

There is a constructive candidate for the model-conversion blocker in
`SIEGEL_ELEMENTARY_REPOLARIZATION.md` when the original dimension is TWO.
It does not directly produce a new surface model. Instead it produces a
model of eight copies of the changed-polarization surface, with correctly
transported weak markings. That suffices for the existing marked-kernel
separation argument, with dimension increased from 2 to 16.

The new ingredient is an explicit smooth-denominator sum-of-squares identity.
It avoids supplying End(B), Hom(A,B), secret ell-torsion, a square root of a
polarization, or a pre-existing model of the changed polarization. This is a
proposed mathematical bridge, not a finished implementation of that bridge.

## 1. Source Contract

Use the repository's source, specialized to A=E^2:

- Odd characteristic p and a distinct odd prime ell. E is supersingular;
  its full endomorphism order O, involution and efficient evaluators are known.
- A and the ORIGINAL (B,lambda_B) are modeled PPAVs. A genuine polarized
  ell-isogeny phi:A->B has a weak evaluator. At each requested auxiliary
  order n, it supplies ONE common unit scalar times the images of a full
  ordered basis. The same underlying phi must apply at every order.
- All public maps, phi and polarizations are defined over a paid common
  finite field F_q, with compatible embeddings for separately represented
  auxiliary extensions. An unknown enormous common definition field is not
  permitted. Geometric isomorphisms may require the model's bounded extensions.
- Auxiliary access includes n=r^2 for selected small primes r, including 4,
  as well as the separate odd prime marking levels. Prime-only cached data
  must NOT be silently promoted to this stronger interface.
- Points, arithmetic, field construction and quotient evaluations are paid.
  No field containing the entire D^2-torsion is constructed by CRT compositum.

For each m in Sp_4(F_ell), the existing elementary lift supplies a degree-one
automorphism sigma of A reducing to m. Set

    S = sigma^dagger sigma = I + ell T0,
    psi = phi sigma^(-1),
    H = phi S phi^(-1) = I + phi T0 phi^dagger.

The existing argument proves H is an integral positive symmetric unit,
lambda_B H is principal, and psi is ell-polarized for that NEW polarization.
Its kernel is mK. H is computable on accessible auxiliary torsion by
conjugating S through the weak image basis; the common scalar cancels.

In dimension two write the quaternion-Hermitian matrix S as

    [[a, z], [bar(z), d]],   a,d in Z.

Its positive Moore determinant is ad-nrd(z)=1, since sigma has degree one.
Direct matrix multiplication gives

    S^2 - t S + I = 0,       t=a+d >= 2.

Thus H obeys the same identity and H^(-1)=tI-H. This is NOT an assumption
about arbitrary higher-dimensional polarizations. At t=2, positivity makes
H=I; simply use the old product model and unchanged transport. Below t>=3.
The implementation's formal ring intentionally excludes t=2 rather than
treating the nonreduced ring Z[h]/(h-1)^2 as a geometric polarization.

## 2. Smooth Denominators Without Factoring t+2 Or t-2

Choose a PUBLIC bound t_max on every lift trace over the finite query domain.
The elementary lift word and coefficient bounds give polynomial bit length
for such a bound; use a worst-case bound, not a maximum over observed queries.
Choose one even squarefree D>t_max+2, made of successive small primes excluding
p and ell. This D is shared by all queries. Its bit length and largest prime
are polynomial in the input size. We do not need any smoothness of t+-2.

Let c=gcd(t+2,t-2), which divides 4, and define

    a0=(t+2)/c,  b0=(t-2)/c,  n=D^2/c.
    X = n*a0^(-1) mod b0,  0 <= X < b0,
    Y = (n-a0 X)/b0.

For b0=1 take X=0. Since D is even, c divides D^2. Since
D^2 >= (t+2)(t-2), Y is nonnegative. Therefore

    (t+2)X + (t-2)Y = D^2,       X,Y >= 0.

Compute four-square representations X=sum a_i^2 and Y=sum b_i^2. The
unconditional randomized algorithms discussed by
[Pollack and Trevino](https://math.colgate.edu/~integers/sjs15/sjs15.pdf)
give expected polynomial bit cost; use an unconditional version, not merely
the fastest ERH-conditional variant. The local control uses SymPy to find
and verify witnesses, without claiming its implementation has this bound.

The quadratic identity yields

    (H+I)^2 = (t+2)H,      (H-I)^2 = (t-2)H.

The eight COMMUTING symmetric endomorphisms

    a_1(H+I),...,a_4(H+I), b_1(I-H),...,b_4(I-H)

therefore have sum of squares D^2 H. Apply the classical eight-square norm
identity, equivalently left multiplication in the octonion composition
algebra. It produces an 8-by-8 matrix C over Z[H] satisfying BOTH

    C^dagger C = C C^dagger = D^2 diag(H,...,H).

The coefficient ring is commutative, so the norm identity applies. We never
use associative multiplication of arbitrary octonions or arbitrary
noncommuting endomorphism coefficients. The controls verify both identities
in the exact quadratic quotient ring, as well as evaluated matrix examples.

## 3. A Quotient Whose Codomain Is The Desired Stabilized PPAV

Write H8=diag(H,...,H), let X0=(B,lambda_B)^8, and define the integral map

    F = H8^(-1) C^dagger.

Every entry is a polynomial in H with integer coefficients. Importantly,

    F^dagger H8 F = D^2 I,       F C = C F = D^2 I.

Consequently F, viewed as X0 -> (B,lambda_B H)^8, is a D^2-polarized
isogeny. Its kernel G is maximal isotropic in X0[D^2], has order D^32,
and is killed by D^2. Positivity and principality are supplied by Section 1,
not inferred from the formal matrix identity alone.

For each prime r|D, compute the matrix of H on B[r^2] from S and the weak
phi images. Compute ker(F mod r^2) over Z/r^2 Z, or enumerate it. Turn
those coordinates into actual points using the known weak image basis.
This obtains G_r=G intersect X0[r^2] WITHOUT computing phi on ell-torsion.

Use the DIRECT quotient primitive A26 of
[Corte-Real Santos, Piasecki and Wesolowski](https://eprint.iacr.org/2026/1142)
with order r^2 and the complete G_r list. Compose these quotients over the
distinct primes r, pushing the remaining kernels and required marking points
through each quotient. Earlier quotient degrees are coprime to later r.
Each G_r has r^32 elements, polynomial in r for this fixed dimension, albeit
completely impractical at many parameters. G_r is defined over the common
base field because F is; the quotient primitive preserves this definition
field. Separately represented torsion fields do not accumulate into a giant
compositum. Products use A27. No interpolation of F is required.

We obtain q:X0->Y with exactly ker(q)=G and the same multiplier D^2.
The quotient universal property supplies a polarized isomorphism

    u:Y -> (B,lambda_B H)^8,       u q = F.

The algorithm does NOT compute or assume u. Its existence proves the output
has the right meaning. We do NOT call A3 representability a converter.

### Why Not Blindly Use The Published CRT Loop?

The displayed Algorithm 1 in the reviewed 2026/1142 version starts a
prime-square stage by multiplying the supplied generators by r. For a
general maximal isotropic G in X[r^2], rG need not be a maximal isotropic
subgroup of X[r]. The simplest example is X an elliptic curve and G=X[r]:
then rG=0, although |G|=r^2 as required. The next A26 call is not an
r-isogeny in that case. This exposes an omitted non-free-kernel case in
that displayed algorithm, not a disproof of the existence of a CRT quotient
algorithm or of the paper's squarefree interpolation use case.

Our explicit t=7,D=30 Gaussian matrix control exhibits this issue at r=2,
and genuine r^2-order kernel elements at r=3,5. The proposed construction
therefore calls A26 directly with N=r^2. A later optimized implementation
may use a correctly proved isotropic flag refinement; it cannot simply
reuse the displayed loop unchanged.

## 4. Point Transport Without A New-Polarization Model

Choose fixed, separate small odd prime marking orders s avoiding p*ell*D,
with product R such that

    R^2 > 8*16^3*ell^2.

Use full ordered bases of A^8[s]. First obtain weak psi^8 images Z in the
OLD B^8 coordinates, using the original phi images and the known action
of sigma^(-1). Reuse the same four basis images for all eight copies, so
one common scalar applies to the ENTIRE tuple. For each such point compute

    q( [D^(-2) mod s] C(H) Z ).

All operations inside q take place in the OLD modeled B^8 on accessible
s-torsion. Since F^(-1)=C/D^2, these are exactly the same unknown scalar
times the images under

    theta_m = u^(-1) psi^8 : A^8 -> Y.

This map is ell-polarized, with kernel (mK)^8. It exists as an integral
map even though the transport formula evaluates a rational inverse only
on torsion coprime to D. No division of arbitrary geometric points occurs.

Now jointly canonicalize Y and ALL ordered markings using one polarized
isomorphism and one shared automorphism across the levels; allow one common
unit per level. A7/A22/A25 and the preceding PPAV audit give this procedure.
The repository's projective marked rigidity lemma in dimension 16 implies

    label(m)=label(n) iff (mK)^8=(nK)^8 iff mK=nK.

The converse uses the polarized isomorphism of equal-kernel quotients.
This also removes dependence on four-square witnesses, quotient coordinate
choices and lift choices. We do not assume that unmarked products cancel,
that factor decompositions have canonical order, or that an isomorphism
preserves the eight factors. Full markings and rigidity do the work.

The original acting group remains Sp_4(F_ell), NOT Sp_32(F_ell).
Stabilization changes the oracle-output geometry, not the hidden subgroup.

## 5. Resources And Coherence

The proposed classical label computation is expected polynomial in the
paid input length at fixed original dimension two, conditional on the
stated geometric source promises and published model primitives. This is
not uniformly polynomial in a growing geometric dimension. Level-4 theta
coordinates in dimension 16 alone number 4^16; canonicalization may be far
more expensive. The present objective is a theoretical source lemma, not
a claim of near-term practical execution.

Prime-square access is essential. Taking D=2^k with k growing would make
the required torsion order and potentially its field degree enormous.
Squarefree smooth D instead needs only orders r^2 at individually small r.
Their point field degrees are polynomial in r for fixed dimension, using
the finite Frobenius action; no assertion that smooth order implies short
point representations is being made.

All required weak phi images and auxiliary bases can be precomputed
classically ONCE at the globally fixed orders. The subsequent label oracle
uses these fixed points and public arithmetic. It need not make coherent
calls to a possibly randomized weak evaluator. This does not remove the
need to coherently compile the geometric label computation itself.

For verified Las Vegas subroutines with a uniform expected clock B, cap each
attempt at 2B and repeat independently k times. Failure at each fixed group
element is at most 2^-k. Fix the random tapes once and union bound over
|Sp_4(F_ell)|=ell^4(ell^2-1)(ell^4-1), and over the polynomially many
subroutines. Taking k=O(log ell+log(1/epsilon)+log(subroutine count)) makes
the fixed circuit compute the correct canonical function on every input
with high probability. Retain a failure flag; uncompute workspace. This
argument requires verified successes and uniform bounds, not an average
over a favorable distribution of queries. No such circuit is implemented.

## 6. Adversarial Review And Classical Baselines

The strongest current challenge is NOT a larger numerical benchmark. It is
an independent audit of this source construction and of the already proposed
Sp_4 hidden-stabilizer receiver, followed by a matched classical attack.

- Wrong orientation: C^dagger alone is not the map from the old to the new
  polarization. Dropping H^(-1) gives the wrong pullback. A test falsifies it.
- Wrong kernel representation: prime-only bases and free prime-square kernel
  assumptions fail explicit Smith-form controls. Direct r^2 quotients avoid
  this shortcut but charge much more work.
- Hidden model/field advice: no full End(B), Hom module or target model may
  enter the converter. A missing efficient common definition field would
  invalidate the stated complexity conclusion.
- False auxiliary promise: compatible pairings at each level do not certify
  a single global phi. The reduction is a promised weak-isogeny result, not
  a validator for arbitrary fabricated torsion tables.
- False extension in dimension: the quadratic identity is special here.
  Higher-degree characteristic polynomials require a different construction.
- False hardness: full Hom/End advice already classically dequantizes the
  stronger source. The new label must be attacked using only the stated
  weaker source, not defended by an opaque-oracle lower bound.
- Known algorithms: the elliptic weak-isogeny result of
  [Chen et al.](https://arxiv.org/abs/2305.19897) remains prior art. This pass
  does not claim to break generic supersingular isogeny search, solve DCP,
  or recover an ECDSA private key.
- The earlier weak-scalar baseline reconstructs a compact isogeny by
  exp(O(log ell/log log ell)) sign assignments and interpolation. The
  descent-membership test is polynomial for supplied polarized maps. Neither
  is yet shown to recover this source's abstract hidden kernel in polynomial
  classical time. That is a knowledge gap, NOT a lower bound.

There is another mandatory classical capability, stronger than merely storing
weak local action tables. For any supplied polarized a:A->A of multiplier N,
the INTEGRAL map b=phi a phi^dagger is polarized of multiplier ell^2 N.
On the weak image basis Q_r it acts by the known matrix ell*A_r. The common
scalar cancels. With sufficiently large smooth auxiliary product M coprime
to p*ell*N, the old-model interpolation theorem therefore constructs b in
expected polynomial time, without supplying End(B). The multiplier is
ell^2 N, not N. This is a deduction from the prior audit's interpolator,
not an executed geometric workflow. Any hardness comparison must allow this
transport of known polarized maps. Turning a collection of such maps into a
FULL, ell-saturated End(B) lattice is a separate task; assuming that task
solved would reintroduce the already-dequantized stronger input.

The construction is influenced by Robert's real-multiplication/sum-of-squares
approach in [2024/406](https://eprint.iacr.org/2024/406), Section 4. Its
correction to Lemma 4.2 explicitly warns about integral square decompositions
and denominator costs. Here the two-coefficient identity supplies bounded
dimension and chosen smooth denominators in the special quadratic-unit case.
Targeted searches did not establish novelty; a full comparison with modern
higher-dimensional module conversion remains required.

Source version record: the retained Robert PDF is the 128-page March 5,
2024 ePrint version (CC BY, author Damien Robert), SHA256
`84a16373a8d7da78cf990511d5232e976b65996adf76e4f878cf24973793edf5`.
Complete relevant pages 9-12 and 14-18 were read; page 17 was rendered and
visually checked. The author's website currently exposes a later 146-page
version; those are not interchangeable page-number references. The PPAV
framework is the previously retained 44-page version, with pages 16-17
newly inspected here for the CRT-kernel issue.

### Closest Conversion Results Checked

Selected complete pages 1-4, 24-26 and 31-33 of
[Page--Robert--Soumier, 2026/276](https://eprint.iacr.org/2026/276) were also
read; page 33 was visually checked. Definition 5.2 and Theorem 5.8 require
generators of the ENTIRE Hom group, not an unsaturated sublattice. Theorem
6.9 starts from Hermitian modules. Corollary 6.11 obtains an unpolarized
isomorphism from that module representation under GRH. These input
requirements cannot be replaced by weak phi evaluations without a separate
reduction. This comparison does not establish our construction's novelty.
The retained 48-page CC BY PDF has SHA256
`7c5bf9474b8e2589ffb84b089320790f83a8bc4c14aa3d1e4f7ed64a29033486`.

[Montessinos, 2601.18050](https://arxiv.org/html/2601.18050), Sections 1.1-1.2,
likewise discusses reductions using IKO matrices or endomorphism-ring data.
It is not an unconditional algorithm to obtain an unpolarized isomorphism
from only a surface model. A headline about computing isomorphisms must not
be read as granting that stronger input conversion. Only these stated input
requirements were checked here, not every proof in that paper.

## 7. What Was Actually Verified

The isolated controls check the exact quadratic-ring identities, the integer
coin decomposition, octonion norm multiplication, a 61-isogeny Gaussian
surface identity, the wrong-orientation falsifier, prime-square Smith forms,
transport at an auxiliary order, and resource plans through a 1024-bit trace
bound. They do not execute point generation, geometric quotient/canonical
algorithms, or the quantum receiver. The Gaussian example uses characteristic
103 (3 mod 4), where the j=1728 curve is supersingular. The earlier note's
characteristic-101 curve is ordinary; its endomorphism counterexample remains
valid because that argument does not require supersingularity. That wording
has been corrected in the prior isolated bundle.

Decision revision: for this surface source, replace "no constructive model
conversion proposed" with "explicit stabilized conversion proposed; review
and geometric validation pending." Do not mark a speedup proved, grant an
unconditional cryptanalytic result, or generalize to all dimensions.
