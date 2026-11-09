# Kuga--Satake: classical baseline and spin readout audit

2026-11-07. CLOSED narrow source/representation review, not closure of every
possible Kuga--Satake algorithm. STATE/TRAPS, the focused corpus been-tried and
baseline queries, and the actual primary passages below were read. No network,
API, implementation or numerical scan. Source URLs/hashes are in
audits/sources/surface_torsion_selection/ks_source.json.

## What the actual sources establish

1. Pila, Theorem A, requires an EXPLICIT projective abelian variety and explicit
   addition laws. The exponent and constant depend on embedding dimension,
   equation counts and degrees, including the addition laws. Fixed abelian
   dimension alone is not its stated input guarantee. The actual surface-P1
   paper's introduction and conclusion leave P2 uncomputed; they neither supply
   nor rule out a Kuga--Satake reduction.

2. Madapusi Pera, Theorem5, gives an algebraic integral period map from the
   orientation cover of degree-2d K3 moduli to the orthogonal integral model
   over Z[1/2]. Section3.4 gives a finite etale GSpin cover carrying a Clifford-
   equipped abelian scheme; §3.7 extends this cover and abelian scheme integrally.
   Section3.4 also supplies the distinguished motivic idempotent whose image is
   the standard orthogonal local system. Proposition4.6 identifies the ell-adic
   local systems, and Theorem4.17 gives the primitive-H2 embedding in the
   Clifford-linear endomorphisms of H1 over a finite separable extension.
   The theorem is stronger than an unrelated existential association for each
   individual surface. It is not presented as a bit-complexity algorithm.

3. Rizov's introduction theorem gives, for FIXED polarization and level data,
   a KS morphism over O_(E_n)[1/N]. The number field E_n, excluded integer N,
   polarization type and dimension g=2^19 are fixed by those data. Proposition
   2.5.3 and the surrounding constructions describe the algebraic moduli maps.
   Remark2.5.7 explicitly discusses the further descent from the level cover;
   it is not legitimate to assume that an arbitrary quartic over F_p directly
   gives the required polarized KS model over F_p itself.

4. Hassett--Kresch--Tschinkel is genuinely EFFECTIVE, but with an explicit
   hypothesis and different endpoint. Its Assumption18 requires an effective
   construction of the degree-2d period/moduli space and an effective map from
   the input K3 to that space. Section5 uses rigidity and Hilbert schemes to
   obtain a finite list of KS morphisms. Proposition19 uses bounded-precision
   complex/homology computations to select the associated abelian variety and
   recover Picard data. Remark9 supplies the required moduli effectivity for
   degree TWO. Remark10 discusses degree FOUR as an additional effectivity
   step to be achieved from its GIT analysis. Remark11 explains the degree-bound
   issue in the Baily--Borel construction. No polynomial(log p) quartic P2
   theorem is stated. These are exact scopes of this source, not a claim that
   no later construction exists.

Costa's thesis pp42--44 accurately points to that degree-two effective result
and describes the then-uncontrolled general construction. Its historical
statement must not be promoted into a current universal no-effectivity theorem.

## Fixed precomputation is a serious possibility

Historical attribution: this is already an explicit PUBLISHED suggestion in
Noam D. Elkies, *Elliptic and modular curves over finite fields and related
computational issues* (March1997), p15 footnote10. The parent independently
opened and checked the actual primary web PDF; this reviewer read only the
parent's audited `elkies_scope.md` receipt, not a local PDF. The receipt and
its provenance/hash are recorded in `elkies_source.json`; direct PDF downloads
returned HTTP403, so that hash is not a PDF hash. The footnote proposes KS as
a probable affirmative route for general quartic point counting using its
spin/abelian realization and algebraic equations, while expressly distinguishing
that possibility from exhibiting and analyzing the algorithm. Its further
weight-two suggestion is speculative, and the further example is a quintic
THREEFOLD. This is an old algorithmic lead, not a new repository proposal or
a proved polynomial-time classical theorem. It strengthens the requirement
to retain the marked/descent KS comparison before any priority claim.

Do NOT dismiss the classical route solely because the papers do not print
enormous equations. For a FIXED quartic family, fixed level, and fixed
polarization, the algebraic schemes, finite covers, morphisms and polarized
abelian scheme above have finite presentations independent of p and of the
quartic coefficients. Pulling everything back to the explicit parameter space
of smooth quartics gives fixed algebraic data over a fixed arithmetic base.
After choosing finite affine charts and a relative projective embedding, both
the defining equations and group-law formats have fixed bounds.

If those finite presentations are hard-coded, a fiber over a supplied quartic
has bounded degree. Fixed-dimensional elimination/factorization can find a
point over an extension of uniformly bounded degree, and specialization gives
an abelian variety in a bounded presentation format. Pila then has polynomial
dependence on log p for that supplied variety. Finitely many excluded rational
primes can be handled separately. This is a legitimate EXISTENTIAL fixed-data
argument for supplying a KS variety, not input-dependent advice. Even without
an executable precomputation in hand, existence of the fixed finite data is
stronger than saying that an arbitrary amount of new information is needed for
each p. It is not yet a concrete implemented or fully specified uniform KS/P2
algorithm; HKT's effectivity hypothesis identifies what its constructive
procedure additionally needs.

Most importantly, this supply argument alone does not compute the Frobenius
characteristic polynomial on the MARKED primitive-H2 subspace, nor does a
calculation over F_(p^a) automatically recover the original F_p Frobenius.

## Generic spectral inversion and an exact nongeneric collision

For GSpin(2m+1), write standard torus eigenvalues as

    1, lambda_1,lambda_1^-1,...,lambda_m,lambda_m^-1.

The irreducible spin eigenvalues have the form

    c * product_(i in S) lambda_i,    S subset {1,...,m},
    similitude = c^2 * product_i lambda_i.

On the explicit generic locus with no relation product lambda_i^a_i=1 for
nonzero a in {-2,-1,0,1,2}^m, the spin spectrum DOES determine the standard
spectrum. An eigenvalue ratio with exponent vector a in {-1,0,1}^m occurs
2^(m-|support(a)|) times. Thus the nonidentity ratios of greatest multiplicity
are exactly lambda_i and lambda_i^-1. The central scalar cancels. Known repeated
copies of the spin representation multiply all these ratio multiplicities by
the same factor. At fixed m this is an exact algebraic-number computation of
fixed degree and polynomial coefficient-bit cost. This is a generic-FROBENIUS
condition; a generically polarized quartic does not promise it at every prime.

There is no universal spin-spectrum inversion of this form. The following
rank10 specialization verifies the parent's rational example. Let

    lambda = (-1, i, zeta_3, 1,1,1,1,1,1,1),
    lambda'= (-1, i,-zeta_3, 1,1,1,1,1,1,1),
    c=sqrt(q)*zeta_24^-1,             c'=i*c.

The first product is (-i)*zeta_3=zeta_24^2. Therefore both
c^2*product(lambda) and (c')^2*product(lambda') equal q. The first two subset
coordinates give mu_4; multiplication by the third gives mu_4 union zeta_3*mu_4.
After multiplication by zeta_24^-1 these are exactly the eight primitive 24th
roots. Changing zeta_3 to -zeta_3 does not change that subset spectrum, and
the additional central factor i also permutes mu_4. The remaining seven unit
coordinates repeat every eigenvalue 128 times. Both monic spin polynomials are

    (X^8-q^2*X^4+q^4)^128.

They have the same similitude q. Passing to the fixed repeated spin module
used by a KS construction preserves this equality.

The standard normalized traces, however, are

    1-2+0-1+14=12,       1-2+0+1+14=14.

Taking q=p and adding the polarization gives the two formal full-H2 polynomials

    (1-pT)^16*(1+pT)^2*(1+p^2*T^2)*(1+pT+p^2*T^2),
    (1-pT)^16*(1+pT)^2*(1+p^2*T^2)*(1-pT+p^2*T^2).

These are degree22 integral Weil polynomials, with traces 13p and 15p. They
are an exact representation/Weil-spectrum falsifier for universal recovery
from the spin characteristic polynomial ALONE. This review does NOT exhibit
two actual quartic K3 surfaces realizing them, and does not claim that no
additional geometric constraint could distinguish them.

## The stronger marked-torsion repair remains a serious candidate

The collision does NOT refute a KS algorithm that recovers the marked H2
module from generic monodromy. At a fixed universal KS dimension, constructing
an ell-frame cover, enumerating a finite matrix group or subspaces, and taking
a bounded-level normal closure may all cost ell^C with C a fixed enormous
constant. It is therefore invalid to reject those operations solely because
their dimensions or degrees are impractical.

Two exact interfaces must nevertheless be accounted for:

- H1 of the full KS variety is a large MULTIPLE of the spin representation.
  End(H1) therefore has many standard 21-dimensional copies. A proposed
  uniqueness argument must first impose the known algebraic RIGHT even-
  Clifford action, or provide equivalent grading/component data. In the
  irreducible spin endomorphism representation, the standard constituent can
  be distinguished using full generic Spin monodromy for suitable ell; the
  required finite-characteristic uniqueness and bad-prime bound must actually
  be proved or checked, not assumed for every ell.
- The KS point lies over a finite level/orientation cover. Frobenius of a
  quartic over F_p may move that point to another fiber. A geometric-monodromy
  invariant subspace over its field of definition gives F^a data, not by itself
  the original F. One must compute the full arithmetic descent/transport on
  the composed frame cover and identify the descended standard local system.
  This need not entail a factorial-degree obstruction: if the initial level
  cover has FIXED degree D, the normal-closure group of its frame covers lies
  in a fixed-fold wreath-product bound, polynomial in ell at fixed dimension.
  But degree bounds alone do not supply the descent computation or identify
  the correct arithmetic twist.

A concrete universal model, marked Clifford actions, generic monodromy and
arithmetic descent could plausibly pay these steps. The cited KS and Pila
statements alone do not constitute that full algorithm. No counterexample
to this stronger repair is established here, and no claim of its impossibility
or current literature absence follows.

**Disposition:** the unmarked spin-polynomial shortcut is insufficient in full
generality; the stronger fixed-family classical KS route remains a material
unresolved comparator. Its existential fixed-precomputation potential must
be retained before any unmatched quantum upper-bound claim. The selected
surface torsion-cover proposal is still separately conditional on its native
construction and source gates.
