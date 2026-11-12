# Native small-characteristic natural torsion-module extraction

2026-11-12. Parent construction independently reviewed and source-checked.
Review: audits/reviews/2026-11-12-surface-native-module.md. This removes a
specific supplied-module input in the repaired surface filter; no full native
point count, uniform height, novelty or separation claim.

## Contract and source scope

Fix n,r and odd prime ell. Supply an explicit geometrically connected compact
G=Sp_n(Fell) cover C/P1 with nontrivial transvection inertia at r geometric
punctures, in a separable plane/function-field model. Numerical degree, genus g,
map coordinates and finite-field presentation are charged; in the intended
surface construction they are polynomial inell at fixed n,r. Ground field is
Fq of characteristic P prime toell|G|. Deck generators are supplied over an
explicit charged finite field; a common field for the fixed O(n²) generators
costs at most their fixed-number product. Their minimum common definition
degree also has the bound |AutG|<=|G|^(n+n²), from Frobenius action on deck maps.
Do not take an arbitrary lcm of all separately given map coefficient fields.

Let V=J_C[ell](Fqbar)=H1(Cbar,muell), S=M* natural dimensionn, and
W=Hom_G(S,V). The CLOSED geometric lemma gives m=dimW=(r-2)n. This is the
OPEN-cohomology multiplicity, not the false parabolic stopping target.
No torsion basis, zeta numerator, target eigenvalues or splitting field is advice.

Output: a complete basis of W by rational torsion divisors over ONE explicit
common constant field; the geometric natural isotypic span E and genuine
q-power arithmetic Frobenius on E. The divisors are rational closed-place/ideal
representations; individual geometric support points need not all be rational.
That is sufficient for the RR/Kummer finite filter. If the intended output is
the separate multiplicity-space matrix F_W, the coefficient-module arithmetic
linearization A must be specified/constructed: F_W(phi)=F_q phi A^-1. The
cover's normalizer automorphism alone gives A only up to scalar. This convention
is an actual unresolved input when recovering an ORIGINAL family coefficient
system; choosing an arbitrary intertwiner is not genuine Frobenius advice paid.
With a coefficient module explicitly constant over the working base, A=I
for that base's Frobenius. Making only the deck maps constant is insufficient.
To output F_q on E, certify preservation of the natural representation under
the computed deck automorphism alpha(g)=F_q g F_q^-1: solve
A rho_S(g)=rho_S(alpha(g)) A and verify invertibility, or directly verify
F_q(E)=E in the computed complete space. An arbitrary abstract normalizer
assertion is not this certificate. Failure leaves W and V_small complete but
does not justify a restricted F_E or original-family multiplicity action.

Expected cost poly_(n,r)(ell, NUMERICAL P, presented bits,log1/eta). This is NOT
polylogP. Strongest baseline is the existing classical Couveignes torsion
algorithm, completed by small-characteristic zeta computation; no quantum step.

Primary sources actually read: Couveignes0706.0272 Sections6-8 and Theorem1
(smooth model, degree-one divisor and zeta required; strict-subgroup failure
permitted), plus Lauder--Wan published MSRI44 (2008) Theorems1/37 and the
Corollary3 proof pp610-611. The latter computes the zeta of a plane curve in
poly(degree,NUMERICAL P,logq), with no nonsingularity premise, and extracts the
smooth-model numerator by removing weight-zero factors. Actual source files:
audits/sources/surface_module_2026/{couveignes,lauder_wan_published}.{pdf,txt},
with provenance JSON. The separate author PDF is scanned; the published PDF
is the text source used here. Kozen local resolution and classical RR source
costs are reused from SURFACE_CLASSICAL_HEIGHT_UNIFORMITY.md.

## Simpler common-field construction

1. Work over a charged extension k0=F_(q^b) containing the deck generators
and an actual rational point O of C. Obtain O from ONE closed place above a
regular fibre of the separable degree-D map toP1: avoid denominators and
discriminant over a field larger than their degree, factor the fibre, and adjoin
ONE residue field of degree<=D. No whole irreducible fibre or common support
splitting field is required. Move that fibre to infinity if the RR source's
conventions require one rational infinite place. Normalization is charged by
Kozen. Compute the original smooth-model zeta numerator by Lauder--Wan;
derive extension zeta numerators by exact power sums/resultants. Coefficients
have O(g*b*h*logq+g) bits for extension degree b*h, a paid polynomial size.

2. Write F0=F_q^b. It commutes with G. Evaluation injects S tensor W into V
because S is absolutely simple and End_G(S)=Fell; its image is the semisimple
natural socle E, of dimensionn*m. This does NOT assume V semisimple or average
over G. On E, F0=I_S tensor B for some invertible m-dimensional B. Thus every
irreducible Frobenius factor on E has degree<=m, a fixed bound.

3. Factor chi_(F0) mod ell. Let a(X) be the product, with FULL multiplicities,
of every irreducible factor of degree<=m, and let b(X) be the remaining product.
Define V_small=ker a(F0), dimensionu=deg a. Include all such factors, not just
ones guessed to contain E. The reciprocal-twist partner lambda->q0/lambda
has the SAME irreducible degree, so V_small is closed under Weil duality and
the Weil pairing on it is nondegenerate. It contains E. It is G-stable because
F0 commutes with G, and is also stable under original F_q.

4. Put c=ceil(log_ell(max{1,2g})) and choose the explicit COMMON degree

    H=ell^c * product_(j=1..m)(ell^j-1).

This is polynomial inell andg for fixedm: ell^c<=ell*max{1,2g}, and the
semisimple product has fixed exponent. Every eigenvalue in V_small is killed
by a factor ell^j-1; ell^c kills EVERY ambient primary nilpotent block. Also
ell-1 dividesH, so muell lies in K=F_(q^(bH)). Thus V_small is fully rational
over this ONE field. No lcm over a growing collection of field degrees, no
full ambient torsion splitting and no small-target nilpotence shortcut.

5. Apply Couveignes Theorem1 over K, n_Couv=ell, with computed zeta, smooth
model and rational O. Verify every returned class is actual degree-zero
ell-torsion. Project returned classes by the CRT idempotent p(X) that is1
mod a and0 mod b. Coefficients inFell mean integer multiplication of divisor
classes; reduce divisors after each operation to degree-g effective D-gO.
All projected classes lie in V_small, even in a failed/strict-subgroup trial.
Build their Weil-pairing matrix, using a primitive ell-th root inK and a table
ofell powers for discrete logs. Accept a trial only if pairing rank=u.
This certifies the ENTIRE V_small, whose dimension is independently known
from chi. Select a nonsingular pairing minor as a basis. When Couveignes
succeeds on all rational torsion, this certificate necessarily succeeds.
A strict-subgroup output may pass only if it already contains V_small, which
is sufficient. Failed trials never certify absence.

6. Nondegenerate pairing gives exact coordinates of every deck/Frobenius image
in V_small. Optionally verify each reconstructed divisor equality by RR.
Solve the linear G-generator intertwiner equations to obtain Hom_G(S,V_small).
It equals W because E was contained in V_small; check dimensionm. Compute E
by the span of the n component classes of this Hom basis and restrict the
actual F_q action to E. A supplied genuine A gives F_W by composition; otherwise
return only F_E and the scalar ambiguity, not a falsely normalized W matrix.
Apply the preceding preservation certificate before making this restriction.
Frobenius acts on both parts: F_q(D-gO)=F_q(D)-gF_q(O); O need not be
F_q-rational. Reduce the resulting class back relative to O afterward.

7. Every returned divisor and coordinate identity has a checkable algebraic
certificate. Couveignes success>=1/2 plus an expected-polynomial subroutine
clock can be capped at a fixed multiple of its proved expected bound; retain
a constant joint success probability. Independent O(log1/eta) trials plus
finite-field subroutine error allocation produce bounded time and FAIL<=eta.
No unknown output is silently accepted, and no claim relies on semisimple
Frobenius. Exact exponent/clock constants come from the cited explicit
algorithms, not a finite numerical run.

## Report disposition boundary

OpenAI fast-surface-build completed, estimatedUSD2.268070. Its bounded-degree
primary/Weil-dual certificate and arithmetic-scalar warning motivate this
construction. Parent replaces its separate primary fields/target descent by
the single universal H above. Its optional prime-support representative lemma
and sharper output-field descent are UNNEEDED and not admitted here; closed
place representatives suffice. This avoids importing extra unverified claims.
The report supplied zeta; actual Lauder--Wan now pays it at numerical P cost.

Remaining upstream tasks: native G-cover construction and family coefficient
linearization, the already separate parabolic filter, characteristic-zero
lifting, uniform arithmetic/model heights and CRT recovery. No whole-paper
rehabilitation follows merely from this module. Cheapest falsifiers are the
field-degree bound, reciprocal duality, incomplete-output certificate or a
missing source input; no numerical experiment or quantum implementation is
needed for this exact construction. The independent review checks these
identities and the actual source prerequisites; no numerical control is needed.
