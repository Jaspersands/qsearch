# Native classical quintic reconstruction: written composition

2026-11-12. Reviewed WRITTEN bounded-error classical polynomial-BIT algorithm
for EVERY native smooth quintic over every prime field. The complete
356-line independent review, audits/reviews/2026-11-12-native-surface-
composition.md, was parent-read against the established interface/source
proofs. No further supplied-input condition remains in this written
composition. This is not an implementation, practical runtime, novelty,
human/formal verification, hardness, separation or quantum-execution claim.
The concrete numerical-majorant ledger is now checked at its specified
geometry/local-residue scope, including the nonbranch-value and arity guards.
The full composition separately pays those geometric and computational inputs.

## Scientific question and native contract

Input: a prime p and coefficients of a smooth homogeneous quintic in four
variables over F_p, in binary, length B=O(log p). Output the exact integral
degree-53 polynomial P2(T)=det(1-T Frob_geom | H2), hence the point count
1+p^2-[T]P2. No pencil, Jacobian, torsion basis, cover, number field, height
bound, cohomology, or target Frobenius is supplied. Fixed degree is essential.

Established written classical randomized bit complexity poly(B,log(1/eta)), with explicit
failure probability eta and astronomically large constant exponents. It
matches the established native quantum polynomial upper bound. It says
nothing about practical cost or growing-degree input. The relevant classical
baseline is the actual small-prime torsion/lifting method, not direct point
enumeration at large p. Corpus lookups: audits/selection/2026-11-12/
accelerated_portfolio/native_composition_{been_tried,baselines}.txt.

Primary-source checks include Couveignes, Lauder-Wan, Mascot, Anderson,
Buchmann-Lenstra, Pila2005, and actual Lefschetz/monodromy source passages.
The previously quoted ordinary compact Hom=parabolic assertion is false;
the present composition uses OPEN cohomology and an explicit boundary quotient.

## 1. Fixed native geometry

Choose two cubic forms giving a transverse Lefschetz pencil. This is the
3-Veronese pencil, not a hyperplane pencil in the original P3. Fixed-degree
elimination certifies 45 transverse basepoints, distinct critical values,
and exactly one ordinary double point in each singular fibre. The bad
parameter locus has bounded degree independent of p and the input coefficients;
at sufficiently large p random choices succeed with constant probability.
Small p is handled by direct counting below. Lift surface/pencil coefficients
to integers in [0,p-1]; verified good reduction preserves these properties
over Q and Z_p. Their heights and all fixed-format elimination costs are poly(B).

Adjunction gives genus g0=31 and n=2g0=62. The Euler characteristic of the
quintic is55; blowing up45 points gives100. Thus r=100-2(2-62)=220 nodes.
The vanishing-cycle sheaf has full rank62 because H1(X)=0. Integral singular
cohomology of the complex smooth quintic is torsion-free; comparison/smooth
proper base change pays the same mod-ell statements. Full Sp_n for every
odd ell!=p is now independently source-checked in
audits/reviews/2026-11-12-native-pencil-monodromy.md (entirely parent-read).
Deligne WeilII4.3.3 works in finite Z/m coefficients: the orthogonal to ALL
path-transported vanishing cycles is image H1(X)=0. Every nodal irreducible
fibre has a primitive nonzero cycle. Deligne4.2.7(i) applies to EVERY such
pencil, since its extra genericity condition is only p=2 with EVEN fibre
dimension; ours is1. Its parameterized inertia homomorphisms are conjugate
in the actual integral monodromy group, and4.2.8/torsion-free H1 gives exact
integral ±cycle equality, hence exact mod-ell conjugacy. This plus spanning
proves irreducibility. Actual Hall3.1 applies with drop bound1 and empty S0;
there is no separate primitivity premise. No rational Zariski-density shortcut,
unspecified exceptional ell, generic-pencil advice or computed cycle basis.

The partial Claude geometry report correctly requested a source for this
all-pencil assertion, but stopped at generic-only Deligne4.2.6. Its conjectured
remaining gap and extra Hall-premise claim are rejected by the actual later
statements, including rendered primary PDFpage86/printed221. Its local-cycle,
section/Leray and Hodge-index checks agree with the independently proved proof.

One-node fibres are irreducible: if A+B=3H with A.B=1, select H.A=a<=7.
Then A^2=3a-1 but Hodge index gives A^2<=a^2/5, impossible for1<=a<=7.
This argument uses geometric intersection numbers and handles each fibre.
For a safe large-prime regime impose p>|GSp_n(F_ell)|; prime-to-p tame
specialization then transfers the characteristic-zero monodromy. All failures
of this numerical inequality trigger the direct-count branch, not a promise.

## 2. Genuine frame cover and a small auxiliary prime

SURFACE_NATIVE_COVER_CONSTRUCTION.md constructs the complete native
fixed-format Jacobian atlas for the (5,3) fibre over Q(t), its actual
principal-polarization Weil pairing, and the full similitude-frame torsor.
Write Gamma=GSp_n(F_ell), d=|Gamma|. The full cover has d sheets and ell-1
geometric components; its selected Sp component has polynomial genus/plane
degree/height in numerical ell and B. Right deck maps and the actual evaluation
frame are constructed; no unknown arithmetic scalar is substituted.

SURFACE_TORSION_NUMERICAL_LIFT.md and its normalization-lattice review give
the native curve normalization, RR lattices, faithful auxiliary model, and
explicit nonzero integer M excluding bad auxiliary primes. Their coefficient
bits, including inverse-Newton and original-lattice bases, are polynomial.
Choose a prime P different from p and ell, not dividing M|Gamma|, and above
the explicit polynomial bad-parameter counts for the later choices. The
NUMBER P, not only log P, is polynomial in ell and B: a polynomial-size
prime search suffices since log|M| is polynomial. Include curve/deck/branch
witnesses needed by the comparison in M. Later b-dependent RR must instead
be constructed with saturated integral lattices at the ALREADY chosen P;
do not create a circular instruction to exclude new primes after choosing b.

## 3. Complete small-prime module, not ambient torsion

Let S=Ndual be the constant natural Gamma module. SURFACE_NATIVE_TORSION_MODULE.md
constructs W0=Hom_Sp(S,J_C[ell]) over the auxiliary residue field with
m=(r-2)n=13516, using actual Lauder-Wan zeta computation, all degree<=m
Frobenius factors with full multiplicities, one polynomial-degree field,
Couveignes torsion extraction, and a Weil-pairing rank certificate. Pairing
certifies completeness; a returned subgroup alone does not. All costs are
poly(ell,NUMERICAL P,presented bits), with n,r fixed.

Choose multiplier representatives g_a and P(g) the right deck pushforward.
From phi in W0 form the full-Gamma intertwiner by component formula

    phi_full,a(v)=P(g_a) phi(g_a^(-T) v).

For one fixed nonzero s0 in S, evaluation at s0 embeds W=Hom_Gamma(S,J_full[ell])
as an ACTUAL subgroup U of J_full[ell], rank m. Injectivity follows from
simplicity of S: a nonzero intertwiner has zero kernel. Galois equivariance
follows because S and s0 are constant. U is Galois-stable, but generally
NOT Gamma-stable. Thus its actual Frobenius is directly F_W. Deck maps are
used to build component tuples, not asserted to preserve U.

Fallback full natural socle E has rank nm=837992 and also polynomial size
at fixed n,r; the smaller U avoids a final Hom calculation and an nth root
of a characteristic polynomial. Never concatenate ell-1 independent
copies of either dimension.

## 4. Numerical classes to certified rational group algebra

Enumerate U (ell^m points, polynomial in numerical ell at fixed m). Choose
a common regular rational fibre B_a of the full frame cover and b in B_a
so ALL classes and deck-translated component divisors have residue h0(t+g b)=1
and avoid the finite plane-coordinate bad set. The proved bad count is
polynomial in |U|,d,g and chart degrees. Test a bounded grid at P. B_a is
a constant-Gamma torsor: one point generates a splitting field of degree<=d,
computable from its fibre algebra with polynomial presentation height.
Closed canonical divisors are defined over the class/basepoint field by
uniqueness; their support roots are never split.

Lift the prime-to-P torsion points by Mascot's square-zero method on the paid
good model. Canonical extraction is now paid explicitly by the source-checked
Section7 of the numerical-closed-algebra review. Start KM with D0=d0*b,
d0=2g+1, E1=(d0-g)b and x=-t. Mascot Algorithm7 through line5 returns
W0=L(B0-D_t), B0=(d0+g)b. Enlarge the known pole divisor A so deg(A-B0)>=2g+1.
The section-product theorem gives L(A-D_t)=span L(A-B0)*W0 using all products
and residue-selected unit pivots. Only known b-jets enter L(A-B0); no unknown
divisor ideal is queried. Enlarge the evaluation ambient or use paid coefficient
multiplication. A second direct construction is available: with background
D0=A+gb and E1=A, Algorithm7 yields Wplus=L(A+2gb-D_t), and

    W=L(A-D_t)={f in L(A): f L(2g b) subset Wplus}.

O(2g b) is globally generated. The first, independently source-checked product
construction suffices. Exact known RR, residue h0=1 and fixed rank/base change
certify its steps; the unique torsion lift can be rerun under the new background.

The numerical-closed-algebra review constructs V/W=H0(D_t,O_D_t), then
multiplication by plane x,y and the A_t,B_t,C_t closed encoding via unit
linear solves. It handles multiplicity/nonsplit support and loses no P-adic
precision. SURFACE_TORSION_HEIGHT_CHAIN.md bounds canonical support heights
and all closed encoding coefficients by poly(ell,B). This uses the specific
semistable model, proved vertical pole budget, global Green lower bound,
theta/Faltings/discriminant estimates, and paid inverse confluent Vandermonde
heights. It is not inferred from intrinsic theta height alone.

Encode ALL pairs (b,t) in B_a x U, with cyclotomic component coordinate and
all deck-indexed canonical divisors using the constructed global rational
plane coordinate. This is globally Galois-equivariant, not just stable under
auxiliary Frobenius. Choose one separating linear combination at P by the
polynomial bad-pair count. Global height bounds give certified e with
P^e>2T^2 for every rational coefficient of product polynomial and operation
interpolation tables. Their coefficients are rational by equivariance.

Reconstruct A_Q=Q[B_a x U], generally a NONSPLIT finite etale Q-algebra.
Interpolate r(s,t)=1 precisely when the two pairs have equal U-label; labels
are known from local group operations, not globally supplied. The equalizer

    C=ker[f -> r*(f tensor1-1tensor f)]

is Q[U]. Addition, zero, inverse and scalars descend from the auxiliary
tables. All linear systems, coefficient heights and tensor ranks are polynomial.
The splitting degree is bounded by d|GL_m(F_ell)|, not the splitting field
of full growing-genus torsion. Only the quotient C must be unramified at p;
therefore B_a need not be target-regular, though a charged a=a0+pk also works.

## 5. Recover the ORIGINAL-prime arithmetic action

The intrinsic genuine frame extends etale over the complement of disjoint
Z_p branch sections. Tame local Abhyankar plus purity gives a smooth proper
compactification over Z_p; J_full[ell], and hence U, is unramified at p.
This is false for an arbitrary ramified constant twist.

SURFACE_FINITE_ETALE_RECONSTRUCTION.md applies Buchmann-Lenstra's actual
known-prime maximal-order algorithm to C. It is polynomial in rank, coefficient
bits and log p without factoring an unknown discriminant. The terminal order
has unit discriminant at p. Group maps extend p-locally, and powering a->a^p
on its reduction gives actual ARITHMETIC Frobenius on U. This repairs the
counterexample Q(T)=T(T-p); direct reduction of numerical coordinates is
not used. Extract F_U=F_W either over one bounded-degree finite field or via
kernel cardinalities of u(F) computed with the identity idempotent and group
algebra operations. Do not invert arithmetic/geometric Frobenius accidentally.

## 6. Determinant boundary, final surface polynomial and CRT

SURFACE_BOUNDARY_DETERMINANT.md proves W=H1(U_base,R1 f_*F_ell)(2).
For each closed singular-fibre value z, f=deg z, let P_norm,z be the
genus30 normalization's geometric H1 polynomial over F_(p^f), and
epsilon_z=+1/-1 for split/nonsplit node. The DIRECT arithmetic boundary factor is

    B_W,z(T)=(1-epsilon_z T^f) P_norm,z(T^f).

Pila2005's uniform fixed-family all-field theorem computes these bounded-degree
curve polynomials in poly(log p); Pila1990's fixed-Q-family statement alone
would not pay this interface. The normalized curve has an explicit bounded
embedding obtained by blowing up its unique node. Tangent splitting and
closed basepoint degrees are native finite-field computations.

The parabolic pairing identifies arithmetic Par(2) with geometric Par-dual,
giving the exact polynomial quotient

    P_par(T)=det(1-T F_W)/product_z B_W,z(T),
    P2_X(T)=(1-pT)^2 P_par(T) /
             product_(closed basepoints b)(1-p^(deg b) T^(deg b)).

Degrees are 13516 ->96 ->53. No explicit parabolic subspace, semisimplicity,
Frobenius eigenbasis, rational section, or splitting of closed basepoints is
needed. Quotients can be checked exactly modulo ell.

Use primes ell>53, ell!=p, with product>2^54 p^53. Weil coefficient bounds
then give unique integral reconstruction; largest ell=O(log p). Whenever
p is below ANY required fixed polynomial Q(ell), directly count the surface
over F_(p^j), 1<=j<=53, and use Newton identities. Cost p^O(1) in this branch
is <=Q(ell)^O(1), so it is polynomial in ell; no unspecified finite exception.
Cap verified random searches with an explicit eta allocation. A failed
certificate is FAIL, never a partial module promoted to complete.

## Decisive falsifiers and current gates

Most serious whole-composition falsifiers: an input-dependent exceptional
monodromy prime not paid by torsion-freeness; an exponential coordinate-bit
growth hidden behind polynomial field degree; missing numerical canonical
RR; one-component arithmetic scalar ambiguity; unequal or non-equivariant
global encodings; a target-ramified orbit; a fixed-family theorem with an
unpaid Jacobian; or a determinant sign/Tate-twist error. These are mathematical
obligations, not requests for finite examples. These interfaces and their whole composition have now survived independent
review and parent source checking, at the WRITTEN mathematical level. A future
counterexample or source correction must reopen the exact affected claim.

## Whole paid review: dispositions and the explicit precision follow-up

Parent fully read all536lines of the completed OpenAI whole-composition report.
Its conditional composition checks agree on U, full-Galois encoding, quotient
before maximalization, actual Frobenius, boundary/Tate factors, Leray/CRT and
the small-p fallback. Its primary OPEN was effective height transfer whose
upstream uniform-height/Merkl derivations were OMITTED from that packet. It
correctly refuses to infer those inputs from labels. The existing source
derivations were subsequently checked as a whole, and the new
SURFACE_RECONSTRUCTION_PRECISION_LEDGER.md spells out computable majorants.
Two distinct paid follow-ups tested its analytic constants and arithmetic/
closed-coordinate precision with the actual previously omitted proof inputs.
The completed arithmetic report is parent-checked; the partial analytic
report supplied a valid nonbranch-domain correction, not a complete audit.

Its warning about reusing KM data after changing background is accepted and
already resolved by the source-checked reinitialization/product construction.
Its proposed alternative line W_D intersect L(2D0-A)=L(2D0-D_rep-A) is
REJECTED without a disjointness hypothesis: intersections take the maximum
of the two vanishing divisors, not their sum. The actual Mascot DivAdd/DivSub
prefix used here does not use that invalid shortcut. Report agreement does
not establish the theorem, and a missing packet is not a counterexample.

## Whole review disposition

The final independent review checks native pencil existence for every input,
all-pencil finite-coefficient monodromy, fixed versus growing dimensions,
complete auxiliary module, numerical auxiliary P, post-P known-b RR, actual
canonical divisor conversion, effective logarithmic heights, global descent,
quotient-first target maximalization, arithmetic Frobenius, boundary/Leray,
CRT and capped finite clocks. Parent checked the complete argument, rather
than promoting its ACCEPT label. The exact contract is C(1+B+log(1/eta))^c
bit operations, absolute computable C,c, exact P2 with probability >=1-eta,
otherwise FAIL. Small characteristic is paid by the polynomial-threshold
direct-count branch. The source compact-Hom=parabolic assertion remains
REFUTED; this construction uses open cohomology and determinant division.

Research action: this exact fixed-degree quantum endpoint now has a matching
classical polynomial upper bound. Stop surface variants and independently
reselect an externally valuable native mechanism. Finish the already running
precision audit; do not build the astronomically impractical algorithm.
