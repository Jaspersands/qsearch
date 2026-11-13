# Quartic-surface P2 from explicit torsion-cover twists

Nov14 current comparator: SURFACE_CLASSICAL_QUARTIC_SPECIALIZATION.md gives
the reviewed WRITTEN native classical polynomial-BIT match for this SAME
all-smooth-quartic exact P2 endpoint. It specializes the later repaired
Nov12 native pipeline, including the (4,3) atlas and boundary4940->56->22.
The earlier native-classical OPEN statements below are superseded; the
quantum G0/Euler theorem remains unchanged.

Historical 2026-11-12 comparator audit: see SURFACE_CLASSICAL_HEIGHT_UNIFORMITY.md.
Saxena--Venkatesh2511.05272 claims a classical fixed-characteristic-zero
surface algorithm. Native coefficient-height uniformity is not established
by its cited bounds; a reviewed modular compact/open/parabolic dimension
obstruction refutes its displayed Theorem4.1 identification. Constructive
repair is under review. This does NOT prove classical hardness or separation,
and does not affect the written quantum G0/Euler-induction route below.

2026-11-07. CLOSED reviewed WRITTEN bounded-error quantum reduction for EVERY
smooth quartic overFp, polynomial(logp,log(1/eta)) BIT/gate time at FIXED degree.
Independent geometry, readout and full-composition reviews are closed. No novelty, speedup, practical-cost,
human/formal verification, full implementation or quantum-execution claim.
The separate Kuga–Satake construction remains OPEN, but is no longer needed
for a classical match of this endpoint.

## Scientific question and exact contract

For EVERY smooth quartic X in P3/Fp, given only the prime p and its homogeneous
coefficients in binary, can one compute the FULL degree22 integer polynomial
P2(X,T) in bounded-error quantum polynomial(logp) time? Quartic degree and
ambient dimension are FIXED; growing genus/degree is excluded. Output has
O(logp) bits and gives #X(Fp)=1+p^2-[T]P2. No Jacobian, torsion, monodromy,
cohomology, cover, local Frobenius or short verification certificate is input.
Integrality, Weil bounds and functional equations alone do not certify P2.
No GRH or Tate-conjecture promise is introduced.

The mechanism uses a fixed-genus Lefschetz pencil, explicit small-ell torsion
covers, modular character induction, and known quantum CURVE zeta computation.
The latter is the only substantive quantum primitive. Cover genus and field
extension degrees grow polynomially in ell; their construction is charged.
Expected advantage is ONLY a possible polylogp endpoint where familiar
p-adic point counts retain p-dependence. Classical Kuga–Satake may match it;
no unmatched asymptotic upper bound or classical hardness is established.

Selection started from STATE/TRAPS matching Two Gaussian Channel Diamond
Learner. Corpus been-tried preceded actual literature. Integral-matrix
similarity is already covered by BHJ2202.03526v3 Theorem9.14/Corollary9.16;
general class generation still has its unpaid exceptional-zero source;
quaternion principalization has an unpaid metric oracle; actual1503.09016v2
HPGP fixesdegree and supplies no growing-degree readout. Actual2511.02262
computes surfaceP1 and expressly leavesP2. This independently motivated task
was selected over those directions, not inherited from the Gaussian pass.
Exact torsion-cover corpus lookup found only nearby character-sector/zeta
barriers. Its baseline lookup returned unrelated KLPT records, not applicable
attacks. The Kuga–Satake lookup likewise returned no exact prior result.

## Construction and proof ledger

Full arguments live in the CLOSED narrow reviews:
- audits/reviews/2026-11-07-surface-torsion-geometry.md;
- audits/reviews/2026-11-07-surface-torsion-induction.md;
- audits/reviews/2026-11-07-kuga-satake-classical-baseline.md;
- audits/reviews/2026-11-07-surface-torsion-composition.md.

1. **Uniform safe-characteristic branch.** Let Q(ell) be one explicit polynomial
   dominating the fixed-variable elimination dimension bound, its trace-radical
   guard, frame/twist ranks, primitive-element sampling discriminant degrees,
   group order and fixed pointed-pencil thresholds. Require p>Q(ell).
   If this fails for a needed ell=O(logp), direct counts overFp^j,1<=j<=22,
   and integer Newton identities computeP2 in polynomiallogp: p is then bounded
   by a FIXED polynomial inlogp. This is a uniform complexity implication,
   not a constant-characteristic promise. Constants/exponents are enormous.

2. **Actual pencil input.** Use the source-paid cubic-Veronese pencil, D=3H:
   genus19, reduced base36, and132 nodal fibers. A rational surface point P0
   is found by random line intersection/quartic factoring, with constant
   success for largep. Fixed-degree pointed-pencil incidence, bad-locus bounds
   and exact transversality/node tests pay the pencil throughP0. No rational
   basepoint is supplied. Every singular fiber is geometrically irreducible:
   a reducible one-node D=A+B would have A.B=1, hence A^2=3a-1 for
   1<=a=H.A<=6, contradicting Hodge index A^2<=a^2/4.

3. **Finite torsion coordinates, not nonunique divisors.** OverFp(t), construct
   L=O(117P0) section/multiplication spaces as complete-intersection kernels.
   Genus19 makes all initial dimensions, variable counts and t-heights fixed.
   KM3.14/4.5/5.5 provide divisor membership, addition and Riemann-Roch.
   Canonicalize every class to UNIQUE E-mP0, minimalm<=19, h0(E)=1, P0 notinE;
   encode D=E+(39-m)P0. This removes positive-dimensional representative fibers.
   Fixed finite rational charts compose [ell] in O(logell) steps. Flatten
   formulas in the ORIGINAL fixed coordinates; both chart paths and degrees/
   t-heights are ell^O(1). Eliminate only that fixed-coordinate system.
   The finite cell algebras may have nilpotents; the safe-p trace-pairing
   quotient removes them. Residue fields are separable: pointed Picard classes
   and their unique reduced divisors have the same field of definition, and
   J[ell] is etale. The resulting algebra A has rankell^38.

4. **Full arithmetic torsor and twists.** Build A^tensor38, rankell^1444,
   and impose every nonzero Fell^38 linear-combination test by idempotents in
   the fixed ambient algebra. Flatten each relation before evaluation; avoid
   repeated basis/inverse nesting as a height argument. The surviving algebra
   is the full right GL38(Fell) frame torsor, possibly disconnected. No exact
   monodromy image is needed. All deck maps are explicit overFp. For each
   needed h and j, construct the twist OVERFp^j by semilinear fixed algebra
   after the constant extension of degreeord(h). Invert the descent cocycle
   to obtain cohomological geometric Frobenius hF^j. A twist overFp alone would
   instead give h^jF^j and is insufficient. Factor/normalize explicit plane
   equations, compute full constant fields and rebase geometric components.
   Charge the given model degree before any low-degree Riemann-Roch conversion
   for Kedlaya's input; genus0 components giveq+1 directly. Kozen's actual
   bounded local-parameter output computes deck/boundary actions. Common
   residue extension degree is bounded using the Galois torsor structure,
   not the potentially exponential lcm of arbitrary factor degrees.

5. **Correct modular representation.** V=R1 pi_*Fell is the DUAL of rawJ[ell].
   Arithmetic sigma acts by rho_J(sigma)^(-T); geometric Frobenius sigma^-1
   acts by rho_J(sigma)^T. Keep the Tate information; choose no free root of
   unity. For fixed rankr=38 put s=lcm(1,...,r), e=ell^s-1. Both e and |GLr|
   are NUMERIC polynomialell, with huge fixed exponents. Exact Brauer-character
   linear algebra inQ(zeta_e) computes
       m[V]=sum_i a_i[Ind_(H_i)^Gamma chi_i], m>0, a_i integers,
   with cyclic ell-prime H_i. Cyclic Fourier restriction plus the actual Brauer
   basis theorem proves rational span; integral composition multiplicities
   give rational solutions. Coefficient BIT lengths are polynomial; numericm
   is not a loop bound and may be divisible byell.

   General cohomological descent is DERIVED: it is FALSE to replace it by
   ordinary Gamma-invariants for arbitraryV whenell divides|Gamma|. The
   algorithm uses G0/Euler multiplicativity forV. Ordinary sector invariants
   are used only for Ind_H chi, by Shapiro and exact invariants underell-primeH.
   With right torsor/deck PULLBACK, that module corresponds to the chi^-1 sector,
   projector |H|^-1 sum_h chi(h)h. This orientation must be kept consistently.

6. **Exact readout before modular reduction.** Quantum curve zeta for the
   explicitly constructed twists gives Tr(hF^j) after explicit component/H2
   and boundary corrections. Fourier project overQ(zeta_e), then Newton
   through the polynomial genus bound. Divide byj in CHARACTERISTIC ZERO,
   even whenell dividesj; only then reduce via the specified prime overell.
   Curve integral compact-support cohomology is torsion-free, and theell-prime
   projector is an integral direct summand, so reduction gives the intended
   finite-coefficient sector. With
       L_U(M)=product_i det(1-FT|H_c^i(Ubar,M))^((-1)^(i+1)),
   exact sequences give L_U(V)^m=product_i L_U(Ind chi_i)^a_i.
   Factor the individual reduced polynomials, combine BINARY exponents and
   divide their integer multiplicities bym. The power map is injective only
   on rational functions regular at0 normalized to1, not on arbitraryconstants.
   This also works whenell dividesm; do not expand degree-m products.

7. **Boundary, surface and finite clocks.** Primitive nonseparating nodal
   cycles give R1 pi_*Fell=j_*V over everyell!=p; the integral nearby-cycle
   sequence and the one-component H2 isomorphism justify reduction. R0 is
   constant and R2 is Tate. Euler Leray, without degeneration, gives
       P2(X,T) P_B(pT)=(1-pT)^2 L_P1(j_*V,T),
       L_P1(j_*V)=L_U(V) product_s det(1-F_s T^deg(s)|V^I_s)^(-1).
   B is the actual degree36 Frobenius permutation scheme, not36 rationalpoints.
   Inertia/decomposition matrices come from the normalized explicit cover.
   Before any expansion, reject inconsistent multiplicities/descent and
   numerator degree>4978 or denominator degree>38 forL_U(V). These bounds
   follow from rank38 and132 tame punctures (Hc1-Hc2=4940, Hc2<=38).
   Thus erroneous quantum output cannot trigger exponential exponent expansion.
   These checks are NOT an exact-output certificate. All randomized routines
   are capped with restart/error budgets; failed clocks returnABORT. Amplify
   the known bounded-error curve algorithm and union-bound allcalls.

8. **CRT and output.** Smooth quartics lift smoothly in characteristiczero;
   H2 has torsion-free rank22 and the integral Frobenius polynomial reduces
   correctly for everyell!=p. Weil gives |c_i|<=binom(22,i)p^i. Collect primes
   ell>22,ell!=p until their product exceeds2^23p^22. Elementary Chebyshev
   bounds put the largestell atO(logp); no unknown exceptional-prime set is
   excluded. Recover coefficients by centered CRT, checking the required
   fixed-degree output before further processing. All constructions, genera,
   extension degrees, output sizes and call counts are polynomiallogp at
   FIXED degree. Nothing here is polynomial in growingr or practically small.

## Classical comparisons and decisive falsifiers

Untwisted rational PERMUTATION induction is FALSE. ForSL2(F7), the element
[[0,-1],[1,3]] has order8 and its natural Brauer trace has minpolyx^2-2.
Permutation characters are rational-valued; no nonzero rational multiple of
this module lies in their rational span. This killed the original Claude
identity and motivated character twists, not a generic quantum implementation.

Actual controlled_reduction.txt24–45 gives classical polylogq at fixed genus/
abelian dimension, exponential in growing genus; its hypersurface method has
quasi-linear p dependence. Specialized CM/Jacobi and average-prime methods
have different promises. They do not immediately match this arbitraryquartic
input, but no strongest-possible classical lower bound follows.

Kuga–Satake is a MATERIAL OPEN classical comparator. Actual MP/Rizov sources
give fixed integral family morphisms; finite presentation/precomputation can
supply an existential bounded-format KS family. Missing printed equations is
not a no-go. Actual HKT Assumption18/Remarks10–11 leave the effective quartic
period-map step conditional. Unmarked spin spectra alone are not universal:
rank10 torus lambda=(-1,i,zeta3,1^7) versus(-1,i,-zeta3,1^7), with central
scalar changed byi, have the same spin polynomial(X^8-q^2X^4+q^4)^128 and
similitudeq but standard traces12 versus14. Adding polarization gives formal
integral degree22 Weil polynomials with traces13p versus15p. NO actual pair
of quartic K3s is exhibited. Clifford-marked generic monodromy plus full
arithmetic descent could repair the classical route and remainsVIABLE.

Exact CLASSICAL control source and artifact were inspected:
audits/controls/surface_torsion_cover/control.py and control.json.
- SL2F7 irrational Brauer trace confirms the permutation falsifier.
- Formal C8/64D commuting matrices check Fourier/Newton through8, including
  division7 before reduction. This toy is not a curve-Frobenius realization.
- A smooth non-diagonal F7 quartic has62 points, base2 rationalpoints and
  fiber counts8,6,12,12,12,12,6,8; sum76=62+7*2 checks blowup normalization.
All finite-control algorithm/speedup/novelty/quantumexecution gates stayFALSE.

## Sources, paid agents and next question

Ten new primary PDF snapshots/hash records are in
`audits/sources/surface_torsion_selection/{source,ks_source,kozen_source}.json`;
the retained actual Kedlaya source is math/0411623 under sources/legendre_prf.
Pila ASSUMES explicit abelian model/additionlaw; our constructor is the new
written chart argument. KM's nonunique divisor representation alone is not
an etale torsion algebra. Kozen supplies local parameters, not just genus.
Kedlaya's geometric-irreducibility/model-input requirements are explicitly paid.

Five terminal Claude requests thispass estimateUSD4.303624. Reselection-native
Fable completed and supplied the concrete lead; its false permutation identity
was rejected and construction claims independently repaired. Reselection-hidden
and local-corrections refused with no findings. Jacobian-construction and
KS-marking exhausted their token limits with no report. No empty report is
evidence, no retry is queued and no APIcall is live. Aggregate63 nonpartial
usage estimatesUSD48.928686/32 completed reports is NOT accountbalance; a prior
partialtimeout has UNKNOWNbilling. The owner's spend-before-expiry instruction
remains active; use future calls for distinct useful obligations.

Late actual-primary check: Elkies1997 page15 footnote10 already suggested the
classical KS route as a probable affirmative answer, while distinguishing the
existence of algebraic equations from exhibiting/analyzing the algorithm.
Parent read the actual web PDF; elkies_scope.md/elkies_source.json records that
scope. Its hash is a RECEIPT hash, not a PDF snapshot (local fetchHTTP403).
The old suggestion is not a proved matching algorithm or a universal weight2
reduction. It further lowers the case for extending this example by inertia.

Next hard question: can the stronger fully arithmetic, Clifford-marked KS
route CLASSICALLY match the same arbitrary-quartic input? Compare its expected
value against independent directions at the next STATE/TRAPS selection. No cover backend,
quantum circuit or wider finite sweep is authorized by a passing control.
