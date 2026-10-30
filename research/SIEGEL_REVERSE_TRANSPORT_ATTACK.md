# Reverse Transport From Computable Target Automorphisms

2026-10-30. Exact algebraic deduction and matrix controls, not a geometric
implementation or a uniform classical break of the original weak input.

## Decision And Scope

A full target End/Hom lattice is unnecessary for this conditional attack.
If a polarized automorphism u of the supplied original model (B,lambda_B)
is ACTUALLY computable, reverse transport reconstructs

    beta_u = phi^dagger u phi in End(A).

Its reduction in the public source splitting has image contained in the
secret abstract kernel K. If one image, or the span of several images, has
dimension g, that span equals K. No sign synchronization is necessary.

Unlike the stronger-input attack in
[SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md](SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md),
all integral reconstruction here takes place in the known SOURCE order.
The parent's separate
[SIEGEL_CAYLEY_REPOLARIZATION.md](SIEGEL_CAYLEY_REPOLARIZATION.md) constructs
a repolarization quotient with its own access/cost conditions. Neither
that construction nor the forward-generated subring below automatically
supplies a useful automorphism of the ORIGINAL polarized target here.

The original input does not guarantee a useful u. This note does not grant
one as new advice, construct an automorphism group, or replace the target
polarization. If only scalar automorphisms are available, the test gives
no information. The implementation starts AFTER all point arithmetic:
its inputs are torsion matrices, not curves, points, or geometric maps.
It does not implement the separate Cayley construction or controls.

## Input Contract

Retain the original source in SIEGEL_ELEMENTARY_REPOLARIZATION.md:
A=E^g with known O, odd ell distinct from the characteristic, original
polarized B, and phi^dagger phi=ell, phi phi^dagger=ell. Its geometric
degree is ell^g. The abstract source splitting is public, without forming
geometric ell-torsion.

The matrix-level routines require:

1. An ordered rank-4g^2 integral source lattice basis and its exact positive
   Rosati Gram matrix G. End(A)=M_g(O) is available in the original contract.
   A fixture suborder is also permitted with the EXPLICIT promises that
   every beta_u belongs to it, and that the given actions at each auxiliary
   prime and ell identify its reduction with the full split matrix algebra.
   Successful auxiliary rank checks alone do not prove these promises.
2. Source basis action matrices on full auxiliary torsion bases, and their
   matrices in the public ell-splitting, all in the same lattice-basis order.
3. At each distinct odd auxiliary prime r, r not dividing p*ell, a matrix
   W_r=a_r phi_r, with ONE common nonzero scalar on the entire basis.
4. Exact action matrices of the SAME actually computable target polarized
   automorphisms u_1,...,u_m at every level, in a fixed order. The original
   source and target alternating pairing matrices are supplied too.
   Both pairings use the same primitive r-th root in compatible fields.
5. Every representation, torsion construction, point field, pairing, small
   discrete logarithm, and target-automorphism computation is charged.

No independent target torsion basis is granted or needed. Choose the
supplied weak-image tuple Q_r itself as the target basis. Evaluate u(Q_r)
exactly and recover its coordinates via the original polarized pairing
and paid small-r discrete logarithms. In these coordinates W=I and

    (beta_u)_r = ell * u_(Q_r).

The target form is the pairing form measured in Q_r. The API's arbitrary W
is only a coordinate generalization of this workflow, not extra access.

The lattice and its Gram matrix are on the SOURCE, not a newly discovered
or supplied target lattice. Geometric provenance, actual computability,
characteristic avoidance, and common masks remain external promises.
In particular, finite-level preservation of the supplied target forms is
necessary but does not authenticate a globally polarized automorphism u.
Rank, norm and isotropy checks likewise cannot authenticate the geometry.
A scalar-masked evaluator for u is not enough: replacing u_r by b_r*u_r
multiplies beta_r by b_r, and this new mask does NOT cancel with W_r.

## Exact Reconstruction

On auxiliary torsion, phi^dagger=ell phi^-1. Therefore

    (beta_u)_r = ell W_r^-1 u_r W_r.

Flatten the known source action matrices into columns and solve for the
coefficient column of this matrix in that basis. Their full rank gives
unique residues. If the weak images Q themselves are used as the target
coordinate basis, W=I and the target pairing form is the form in Q; it
must not silently be replaced by a standard symplectic form.

For a polarized automorphism u, u^dagger u=1, so

    beta_u^dagger beta_u = ell^2 I,
    Tr(beta_u^dagger beta_u) = 2g ell^2.

For beta_u=sum c_j b_j in the source basis, positivity gives

    c_j^2 <= 2g ell^2 (G^-1)_jj.

Use reconstruct_integral_transport from
theorems/endomorphism_transport_recovery.py UNCHANGED. Its bounded integer
CRT is generic despite its target-lattice wording. Its coefficient rows
now refer to the source basis, and its columns to the chosen target maps.
With M=product(r), require strictly

    M > 2 max_j floor(sqrt(2g ell^2 (G^-1)_jj)).

The wrapper additionally checks EQUALITY to the exact Rosati norm for
every lifted column. A mere upper bound would incorrectly admit, for
example, zero columns as reverses of polarized automorphisms. Exact norm
equality is necessary, not a proof of the full geometric multiplier identity.

## Abstract Kernel Recovery

The two identities

    phi beta_u = ell u phi,       beta_u(K)=0

imply im(beta_u mod ell) <= K and that every reverse map annihilates K.
Let S be the span of all column images in the public 2g-dimensional split
source module. Under the input promises S <= K, so dim(S)=g implies S=K.

More precisely, let J=im(phi_ell)=ker(phi^dagger_ell). Then

    rank(beta_u mod ell) = g - dim(uJ intersect J).

For several maps, full recovery is equivalent to
J + sum_i u_i J = B[ell]. These are characterizations in the proof, not
requests for geometric ell-torsion. The algorithm tests the equivalent
source-side image span after reconstruction.

The recovery routine checks each rank is at most g, the combined rank is
at most g, S is isotropic, and every reverse map annihilates S. A rank-g
isotropic space is Lagrangian. Its basis is returned as column vectors
listed as rows, in canonical row-reduced form. Kernel coordinates are
abstract source coordinates, not geometric ell-torsion point encodings.

Structural contract errors (bad primes, dimensions, forms or action bases)
raise ValueError. Insufficient CRT level, norms inconsistent with the
promise, zero/insufficient image span, excessive ranks, nonisotropy, and
failure of common annihilation return UNKNOWN with no recovered kernel.
UNKNOWN is neither a hardness result nor proof that other target maps fail.
Algebraically plausible but geometrically false inputs can still pass:
the success status is explicitly RECOVERED_UNDER_INPUT_PROMISES.

## Actual Product Fixture And Multiple Images

Use E:y^2=x^3-x in characteristic 11, the known fixture suborder
Z[i,j] with i^2=-1, j^2=-11, and the product polarization. Its index in
the full order is supported at 2, which all used primes avoid. The reverse
maps below visibly lie in M_g(Z[i,j]); this is not a target-lattice input.

For A=B=E^2 take

    phi = [[6,5],[-5,6]],        u = diag(1,-1),       ell=61,
    beta_u = [[11,60],[60,-11]].

Here u is visible in the supplied product model. The exact multiplier
identities hold; beta_u has Rosati norm squared 14884. Auxiliary primes
(3,5,7,13) give M=1365 and maximum coordinate bound 86 in the fixture
basis. Independent common masks cancel. Recovery returns

    K = span((1,0,11,0), (0,1,0,11)) over F_61.

More generally phi=[[x,y],[-y,x]] with x^2+y^2 an odd prime has the same
rank-two recovery from this involution. This is an original-input easy
family, not a guarantee for an arbitrary polarized model B.

A multiple-image control uses g=3 and phi=diag(s,t,s), where s=6+5i and
t=6-5i. Swapping target factors 1,2 or 2,3 gives polarized automorphisms.
Each reverse map has rank two modulo 61, insufficient individually, but
their images span the full three-dimensional kernel. These are actual
endomorphism identities, not merely arbitrary finite-field matrices.

## Two Exact Obstructions

For u=+1 or -1, beta_u=+ell or -ell, so reduction gives zero. Successful
integer reconstruction does not itself mean any kernel information leaked.
Even u different from both scalars can fail: for phi=diag(6+5i,6-5i) and
u=diag(1,-1), the maps commute and beta_u=ell*u, giving zero modulo ell.
In general this happens whenever u preserves J; a nontrivial target
automorphism is not automatically informative or guaranteed to exist.

Let F_a=phi a phi^dagger. The transported maps satisfy

    F_a F_b = ell F_(ab).

Consequently the ring generated by 1 and all F_a consists of nI+F_a, and

    phi^dagger(nI+F_a)phi = n ell I + ell^2 a = 0 mod ell.

Thus ring operations on this forward-generated algebra cannot make the
reverse image test informative. Its elements need not be polarized
automorphisms; the obstruction controls do NOT apply the fixed automorphism
norm bound to them. Divisions and independent target geometry are not
excluded. This is an identity, not an inference from a failed search.

## Costs And Unimplemented Work

At fixed g, coefficient, Gram-inverse and CRT bit lengths are polynomial
in log(ell) and the charged source representation. Each coordinate solve
has size 4g^2, and final rank/isotropy computations are over F_ell, with
polynomial bit cost in log(ell). No enumeration at the secret prime occurs.
The geometric degree of beta_u is ell^(2g), but expanding its rational map
is unnecessary: the algorithm reconstructs its source-basis coefficients.

Small auxiliary primes can build the required level with polynomially many
bits. For a source elliptic curve, a crude torsion field-degree bound is
|GL_2(F_r)|<r^4. This is not a free torsion-construction theorem. Actual
fields and evaluator outputs must be paid, as must small-order logarithms
(polynomial in r, not automatically in log r). Keep separate auxiliary
fields; do not form a CRT compositum. Nothing constructs target automorphisms,
source/target curves, torsion bases, pairings, new polarizations, or an
endomorphism ring. All geometric claims remain conditional on that input.

## Verification Scope

The focused test file covers exact mask cancellation, target-coordinate
changes, exact and ill-conditioned source Gram forms, insufficient levels,
corrupt residues, the ell=61 product fixture, multiple-map recovery, scalar
zero information, the forward-generated algebra obstruction, malformed
contracts, inconsistent ranks, nonisotropy and common annihilation. A local
127-bit-prime control exercises abstract linear algebra without point fields.
An explicit per-column symplectic tampering control passes the algebraic
checks but changes the recovered kernel, demonstrating why the common-mask
and provenance promises cannot be replaced by those checks.
The small quaternion splitting search belongs only to the fixture helpers;
it is not used by the attack or claimed as a large-prime splitting algorithm.

Verification with /opt/anaconda3/bin/python, bytecode and pytest cache
writes disabled: 56 new tests PASS in 0.41s. The six-file focused suite
passes 212 tests in 1.41s, covering this file plus the existing endomorphism
transport, projective lattice reconstruction, Siegel repolarization,
marked-source, and weak-isogeny-sign suites. Targeted trailing-whitespace
checks pass. The independent math review confirmed the conditional
argument, including the zero-information case for non-scalar commuting
automorphisms; it is not a geometric implementation review.

This work has no CLI, UI, central registry, Git or geometric side effects.
No uniform classical solution, formal proof-assistant verification, novelty
claim, quantum execution or whole-repository validation is asserted.
