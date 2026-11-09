# Quintic surface P2: closed integrated written-reduction review

2026-11-07. Read STATE/TRAPS, QUINTIC_SURFACE_P2_ADMISSION.md, the complete
closed quintic geometry review, and the earlier quartic induction/composition
proofs. Rechecked the actual Schnell Proposition6, Lemmas5--7 and Theorem1,
the surface-pencil source, and the retained classical point-counting scope.
No network, API, Git, implementation or finite control was used. In particular,
the concurrently corrected F7 control was not read or run.

**Disposition: CLOSED for the WRITTEN native quantum reduction.** With the
inherited construction and clock guards spelled out below, every smooth
quintic surface X in P3/Fp, given by its coefficients and prime p in binary,
has an exact degree53 integer P2 computable by a bounded-error quantum
algorithm in polynomial(log p, log(1/eta)) BIT/gate time at FIXED degree5.
The total probability of ABORT or an incorrect polynomial is at most eta.
No remaining quintic composition blocker was found. This is not an
implementation, novelty, practical-cost, classical-separation, short-certificate
or growing-degree claim. The Hodge comparator has different quantifiers from
the finite-field algorithm and is not an algorithmic lower bound.

## Native geometry and integral-cohomology joins

For H the hyperplane class, H^2=5 and K_X=H. The Chern calculation gives
e(X)=55. Integral Lefschetz, universal coefficients and Poincare duality give
H1=H3=0 and free rank53 H2 on the complex lift. Any smooth reduction has a
smooth characteristic-zero lift after localizing the coefficient lift at p;
smooth proper base change therefore pays these assertions for every ell!=p.
No conjectural Tate classes or unknown exceptional auxiliary primes enter.

The source-paid cubic-Veronese pencil has D=3H, D^2=45, D.K=15 and genus31.
Blowing up the transverse degree45 base scheme gives Euler number100, so
the number of geometric one-node fibers is 100-2(2-62)=220. For a reducible
one-node fiber D=A+B, choose 1<=a=H.A<=7. Then A.B=1 implies
A^2=3a-1, contradicting A^2<=a^2/5. Thus all these fibers are geometrically
irreducible; the nodal condition excludes nonreduced components.

The rational section is constructed, not supplied. A line on a smooth
quintic has normal bundle O(-3), so the line Hilbert scheme is finite with
uniformly bounded degree. Random-line incidence has expectation
#X(Fp)/(p^2+1)=1+O(1/p); removing contained lines changes this by O(p^-3).
Every remaining intersection has at most five rational roots. Quintic
factorization/root selection consequently has constant success and bounded
bias. The inherited fixed-degree pointed-pencil incidence search and exact
transversality/node tests provide the pencil through the selected point.
The large-p requirement is included in the safe-characteristic envelope.

The generic curve is a complete intersection (5,3). The correct KM parameters
are d0=63, deg L=189, deg D1=126, and deg D2=126-m in [95,126], for m<=31.
The actual KM5.5 upper bound is 189-2*31-1=126. Preprocessing through H0(3L)
uses s<=567 and a hyperplane P0+B with deg B=14. All these dimensions are
fixed constants. Unique minimal representatives E-mP0, with h0(E)=1 and
P0 not in E, commute with field extension; the resulting torsion-coordinate
residue fields are those of the etale J[ell], rather than hidden purely
inseparable extensions.

## Polynomial cover, readout and local correction

Substitute r=62 throughout the prior flattened fixed-coordinate construction.
The torsion algebra has rank ell^62, its 62-fold tensor algebra rank ell^3844,
and the frame locus is the full arithmetic GL62(Fell) torsor of smaller rank.
The ell^62 independence tests are separate idempotent computations in the
fixed ambient algebra, not simultaneous exponential branching. Flattened
addition formulas, fixed-variable elimination and t-height bounds remain
polynomial in numerical ell. No supplied frame or monodromy image is used.

Each geometric cover component has genus at most 1+109*|GL62| by tame
Riemann--Hurwitz. The arithmetic torsor structure bounds the boundary and
constant extensions by lcm(1,...,220)*|GL62|, with the previously proved safe
polynomial enlargement for twists. This is not an arbitrary-factor splitting
field or an exponential lcm of unrelated extension degrees. Normalization,
full constant fields, local parameters, deck actions and model-degree-first
Riemann--Roch preprocessing remain charged. Rebased curve inputs meet the
known quantum curve-zeta protocol; genus-zero components are handled directly.

The closed fixed-rank induction proof applies without change: take
e=ell^lcm(1,...,62)-1 and all cyclic ell-prime character inductions. This is
numerically polynomial in ell only because 62 is FIXED. Rational Brauer
linear algebra yields m[V]=sum a_i[Ind chi_i] with polynomial BIT lengths,
not necessarily polynomial numerical m. Use the natural DUAL of raw
Jacobian torsion, the full arithmetic action, and the established inverse-
character/deck-pullback convention. General Gamma descent remains derived;
ordinary invariants are used only through the ell-prime subgroup projectors.

Twists over F_(p^j) give hF^j, not h^jF^j. Component and boundary corrections,
characteristic-zero Fourier projection and Newton identities precede modular
reduction. Factor multiplicities are combined in binary and divided as
integers by m. Injectivity of the power map is used only on rational functions
regular at zero and normalized to one. No division by m or an ell-divisible
Newton index in characteristic ell, and no degree-m expansion, is introduced.

At every one-component node the integral primitive vanishing-cycle argument
gives H1(special)=V^I after reduction for every ell!=p. Therefore R1=j_*V,
R0 is constant and R2 is Tate. Euler Leray, without a degeneration premise,
gives exactly

    P2(X,T) P_B(pT) = (1-pT)^2 L_P1(j_*V,T).

P_B is the actual degree45 base-scheme permutation polynomial. The resulting
net degree of L_P1 is 53+45-2=96. Boundary inertia and Frobenius are computed
from the normalized arithmetic torsor, with the previous dual/Tate conventions.

## Finite clocks, output sizes and CRT

Recompute a single EXPLICIT fixed polynomial Q_5(ell) from the degree5/rank62
construction. It must dominate the trace-radical guard, every frame/twist rank,
primitive-element sampling discriminant degree, group order and pointed-pencil
threshold. Merely copying a numerical quartic bound would be invalid. The
displayed fixed-coordinate bounds provide this recomputation; no unknown
input-dependent complexity function is being assumed.

If p<=Q_5(ell) for any needed auxiliary prime, directly count X(F_(p^j)) for
1<=j<=53. Since the largest needed ell is O(log p), this branch has
p<=Q_5(O(log p)); enumeration in fixed extension degrees is polynomial(log p)
on this branch. Integer Newton identities use
s_j=#X(F_(p^j))-1-p^(2j). With P2=det(1-FT), the point-count convention is
#X(Fp)=1+p^2-[T]P2. No small-characteristic promise is added to the input.

Before expanding the reconstructed L_U(V), use tame Euler bounds

    Hc0=0, dim Hc1-dim Hc2=62*(220-2)=13516, dim Hc2<=62.

Require reduced numerator degree<=13578 and denominator degree<=62, as well
as exact integer m-divisibility, normalization and coefficient descent. Check
these degrees on binary multiplicities before expansion. After boundary/Leray
correction require a polynomial of degree53 and constant term one. These
guards bound runtime even on erroneous quantum outputs; they do not verify
the answer mathematically.

Weil gives |c_i|<=binom(53,i)*p^i<2^53*p^53. Collect primes ell>53, ell!=p,
until the product exceeds 2^54*p^53. Elementary prime bounds give largest
ell=O(log p), with no unlisted auxiliary-prime exceptions. Centered CRT then
recovers every coefficient uniquely on the joint success event. The fixed
cutoff53 is conservative, not a substitute for characteristic-zero Newton.

All model sizes, genera, field-extension degrees, cyclotomic degrees, bit
lengths and call counts are polynomial in ell,log p with enormous fixed
exponents. Give curve-zeta calls a total error budget at most eta/2 and amplify
independent calls by output majority. Allocate eta/2 to randomized classical
construction: cap each Las Vegas trial at a constant multiple of its proved
expected clock, independently restart logarithmically many times, and ABORT
when exhausted. Cap intermediate/output sizes by the proved bounds. The
joint-event argument yields the stated bounded-error exact-output guarantee,
without an independent exact-output certificate.

## Classical comparator and final scope

Schnell's actual argument applies to V=H2_prim(X,Q)(1), a weight-zero rank52
structure with Hodge multiplicities (4,44,4), for a VERY GENERAL complex
quintic. Algebraic monodromy supplies connected SO52; polarization and
connectedness identify the required orthogonal Lie algebra. Its weight+2 and
weight-2 pieces each have dimension binom(4,2)=6. Lemma5 excludes this for
the category generated by abelian H1 and Tate structures. Using connected
Lie SO avoids the source's loose untwisted/full-O Mumford--Tate wording.
Tate summands have weight-zero Lie action, including the nontrivial Gm case.

This known theorem excludes a Hodge-compatible generic abelian-generated
replacement, including the ordinary KS mechanism. It does not exclude special
quintics of abelian type, unrelated finite-field constructions, an accidental
equality of zeta polynomials, or every classical algorithm. The quantum
algorithm instead covers EVERY promised smooth quintic over EVERY prime field
using its direct-count branch where needed. Neither statement implies a
classical lower bound or a separation.

The retained controlled-reduction and 2026 Newton-strata sources support a
p-dependent practical comparator and genuine quintic applications. They are
not a priority certificate or an exhaustive proof that no classical
polylogarithmic method exists. The substantive quantum primitive is still
the known curve-zeta algorithm; this pass pays a different native cohomology
endpoint rather than proposing a new quantum primitive.

The main note's remaining OPEN/pending/nativealgorithmgateFALSE sentences are
stale workflow statuses after this review. They may now be replaced by the
scoped CLOSED WRITTEN claim above, with explicit links to both delta reviews.
No additional mathematics or control execution is required for that status
change, and no next-degree variant follows from it.
