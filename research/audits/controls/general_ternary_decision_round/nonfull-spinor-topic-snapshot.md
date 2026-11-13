# Nonfull spinor image forces a two-move ternary transporter

2026-11-13. Reviewed WRITTEN local theorem and general native DECISION
composition under the retained complete GRH arithmetic assumptions. Full
195-line independent local proof and both returned paid reports parent-read;
all changed interfaces and actual source inequalities checked below.
This targets the native indefinite ternary integral-isometry DECISION gate.
It does not claim universal bounded BONG connectivity or a global witness.

## Contract and source check

Input: expanded totally real number field K with its full maximal-order
basis/table, and nonsingular integral ternary Gram matrices, indefinite at
some real embedding. No transporter, spinor offset, class/unit basis or
support advice is supplied. Retain the reviewed complete GRH quantum
arithmetic backends from SPLIT_DYADIC_TERNARY_DECISION.md. The proposed
mechanism is to compute the local stabilizer spinor image FIRST. A full
image makes its relative-offset quotient trivial; a nonfull image forces
a short actual transporter by the theorem below. This directly removes
the growing-ramification seed requirement for DECISION.

Expected upper bound: polynomial quantum bit complexity in native input
and log(1/error), under precisely the retained arithmetic assumptions.
No separation or novelty is asserted. Strongest classical competitor is
the SAME reduction with classical class/unit/norm arithmetic; supplied
quadratic towers retain the stronger ERH reduction to integer factoring.
Local work is classical polynomial arithmetic, with no residue-field,
squareclass, or growing-precision enumeration. No quantum code is proposed.

Corpus been-tried/baselines and Beli/Kirschmer sources checked before this
construction. The newly inspected actual Magma package has a Boolean
IsLocallyIsometric and stabilizer SpinorNorm, not a nonnested transporter.
Its OnePlusPowerOfP enumerates squareclasses; do NOT import a polynomial
runtime claim from that implementation. Use the already charged native
filtration/Hilbert basis algorithms instead. Sources retained under
sources/dyadic_seed_selection/kirschmer_code/ with archive provenance.

Critical primary source: Beli thesis, sources/spinor_genus_admission/.
Printed pp67-69 (PDF78-80), Definition9 and Lemma1.4.11, use INCLUSIVE
low-defect cutoff d<=e-gap/2. Actual PDF pages79,123 were visually checked;
the OCR incorrectly loses the equality bars. Lemma1.7.1(i) characterizes
binary G contained in units; Section1.7 says a lattice without property A
has spinor image either all squareclasses or precisely the unit classes.
Theorem3 at printedp112/PDF123 gives its exact test. PropertyA for an actual
ternary good BONG is R1<R3. These are source theorems, not invented oracles.

## Local theorem and proof

Let F/Q2 have growing charged ramification e and residue degree f. Let
L and M be isometric ternary lattices, with actual good BONG norms a_i,b_i,
common R_i=v(a_i)=v(b_i), R1<=R3. Set
 m=R2-R1, n=R3-R2, C=-a1*a2, D=-a2*a3,
 x=b1/a1, z=b3/a3,
 h=min(e+m/2,m+d(C)), k=min(e+n/2,n+d(D)),
 alpha1=min(h,m+k), alpha2=min(k,n+h).
Good-BONG validity gives m,n>=-2e, h,k>=0, m+n>=0. Unit squareclass
filtration U_t has relative defect at least t, square defect infinity;
C,D with even valuation are identified with their unit squareclasses.
Let H=theta(O^+(L)) in F*/F*2.

CLAIM: If H is PROPER, the word 12(x),23(z) is legal, up to final unit
square rescaling. Its actual coordinates are polynomially constructible
using the reviewed quadratic-order unit-norm compiler and sub-BONG lemma.

1. If m>2e, h=e+m/2>2e and m+k>=m>2e, so alpha1>2e.
 Thus x is a square. Also
 n+h>=e+n/2>=k, since m+n>=0, so alpha2=k. The target second-pair
 threshold equals k because x is square. The ternary Hasse identity
 <C,x>+<D,z>+<x,z>=0 gives <D,z>=0, and d(z)>=k. The first move is
 a square rescaling; the second is legal. If n>2e, the symmetric argument
 gives z square and the first move legal. This case does not require H proper.

2. Suppose m,n<=2e and R1<R3. Since H is proper, Beli Lemma1.4.11
 forces property B. Its inclusive short-gap condition then forces m,n even
 and d(C)>e-m/2, d(D)>e-n/2. Therefore h=e+m/2,k=e+n/2,
 alpha1=h, alpha2=k, and alpha1+alpha2=2e+(m+n)/2>2e.
 The reviewed strict high-alpha two-move proof applies: Beli classification
 condition(iv) supplies <C,x>=0; target invariants and Hasse pay the second.

3. Suppose R1=R3, so n=-m and property A fails. The source dichotomy and
 properness imply H is precisely the unit squareclasses. Both adjacent binary
 stabilizer images G are contained in H, as are the target's G images.
 Lemma1.7.1(i) says m,n are even and, for the first pair, either
 a2/a1 lies in -(Delta/4)*O^*2 (m=-2e,d(C)=2e), OR d(C)>e-m/2.
 The analogous condition holds for D and D*x at
 the target. Hence h=e+m/2, k=e-m/2, alpha1=h,alpha2=k; target k(x)=k.
 If h>0, then d(C)>k (including d(C)=2e when k<2e), so d(C)+d(x)>2e
 and <C,x>=0 by Hilbert filtration orthogonality. If h=0, k=2e, and C is
 square or the unramified quadratic class, whose norm character vanishes on
 every unit x. The same conclusion follows. Hasse then gives <D*x,z>=0,
 while d(z)>=k=k(x). Both moves are legal, including h=0,k=0 endpoints.
 The parity clause in Theorem3 is consistent but is not needed for this proof.

After these moves the norms are (a1*x,a2*x*z,a3*z). Determinant-square
matching makes b2/(a2*x*z) a unit square; rescale that vector. Actual binary
lattice reconstruction, order-unit norms, scalar roots and the sub-BONG
replacement pay coordinates; no integral orthogonal summand is assumed.
Use the reviewed finite seed verification/lift and relative trace spinor
formula, with the global rational identification and orientation explicitly.

## General native composition

First check local isometry by the actual Beli invariants. A nonisometric
place rejects. At an isometric dyadic place compute H. If H=F*/F*2, its
relative spinor quotient is zero: record zero there without constructing
any transporter. If H is proper, construct the two-move transporter above
and compute the relative spinor offset modulo H by the retained guarded
formula. Odd places and real signatures are handled as in the reviewed
split/unramified composition. Complete S-unit ray membership then decides
proper spinor genus; indefinite rank3 strong approximation and -I handle
class and properness exactly as before. The dyadic quotient dimension is
at most sum(ef+2)=O([K:Q]), with every precision and capped-root error charged.

This shortcut needs no solution of universal FOUR-word completeness. The
exact three-word falsifier has full stabilizer image, by property A and its
failure of property B (gaps0,3, e2); it contributes no local offset quotient.
No conclusion about a general local transporter algorithm follows from
skipping that quotient. Falsifiers: an isometric pair with proper H and an
illegal proposed move; a source exception to the dichotomy; or an unpaid
native interface in the global composition. General DECISION is reviewed WRITTEN under retained assumptions;
witnesses, practicality, novelty, hardness,
separation and unconditional arithmetic claims stay unclaimed.

## Independent review and exact disposition

The complete 195-line local proof is
audits/reviews/2026-11-13-nonfull-spinor-two-word.md. Every case, source
condition and native interface was parent-checked. Parent additionally viewed
actual thesis PDF79,116,123: propertyB's cutoff is inclusive, Lemma1.7.1's
ordinary clause is STRICT, and its exception is -(Delta/4)*O^*2. The exact
exception above replaces the shorter equivalent defect wording in the draft.

Paid local audit: claude_runs/2026-11-13-nonfull-spinor-local, truncated
NONEMPTY/max_tokens, all4349bytes read, reaped exit1, estimate0.691364USD.
It independently checks Hasse, alpha formulas, large-gap cases and the
full-image quotient, then stops in case2. Its opening verdict is NOT a
complete review of cases2/3. Its requested large-gap justification is now
explicit. Its requested strict source check is resolved by PDF116 and the
complete independent proof. The report mislabels classification condition
(iii) as (ii), and incorrectly says the Section1.7 dichotomy was absent from
the supplied excerpt; it was included and is directly visible on PDF116.
The exact coordinate compiler already fixes each requested norm; arbitrary
extra unit-square factors are not an unpaid assumption. No retry was made.

Paid global audit: claude_runs/2026-11-13-nonfull-spinor-global, completed/
end_turn, all11908bytes read, reaped exit0, estimate0.457496USD. Its actual
new proof verifies zero-quotient sufficiency and finds no full-image
transporter dependency. Its remaining O1--O7 concern omitted context
locators, resolved as follows (not by the report's verdict):

* O1--O3 and O5: audits/reviews/2026-11-07-spinor-genus-sources.md,
  sections Good BONG, Compile norm/subunit groups, Native boundary and
  Retained errata. Full source compilation re-read: at most3 Beli repairs,
  exact original-K heights, O(ef) unit generators, HNF finite quotients,
  prime/uniformizer/residue construction, and actual Voight6.1 uniform-BIT
  Hilbert algorithm. Prime decomposition/factoring is charged, with capped
  error where randomized; no requirement of deterministic preprocessing.
* O4: actual Beli classification Theorem3.1, physicalLF680--686, accepts
  actual good BONGs over arbitrary dyadic F. Evaluate determinant/Hasse,
  common R/alpha, prefix defects and the sole rank3 representation Hilbert
  condition exactly with O1--O3. No transporter or precision search needed.
* O6: DYADIC_QUADRATIC_ORDER_NORMS.md and full174-line
  audits/reviews/2026-11-13-dyadic-seed-construction.md, sections1--2, give
  actual sub-BONG coordinates and final norm rescaling. The full178-line
  audits/reviews/2026-11-13-local-offset-verifier.md pays finite verification,
  lift, orientation, and four-chart extraction. Diagonalize A exactly overK
  to W; set beta to the sum of nonnegative denominator-valuation bounds of
  W^-1,F^-1,W. Retain Y through N=beta+4e+1 digits, using the larger of the
  seed modulus s_B+2e+3 and N plus binary/root/basis denominator guards.
  Norms of all explicit denominators bound these valuations polynomially.
  Two binary moves and one final unit root add only polynomial losses.
* O7: every modulus exponent/guard is polynomial in expanded native bits;
  sum_{P|2} e_P f_P=[K:Q], and at most[K:Q] dyadic places occur. The clock
  is polynomial in the NUMERICAL precision, not logarithmic in requested
  precision as one report bullet incorrectly suggests. Thus it is polynomial
  in native bits. All capped randomized arithmetic budgets share eta.

At a full-image place, any proper local transporter exists by verified local
isometry and odd-rank -I; its coset modulo H is the unique zero coordinate.
Omitting that coordinate leaves EXACTLY the same S-unit membership problem.
No ray relation, outside-support condition, sign condition or constructive
strong approximation is assumed away. The global rational map, exceptional
support, complete S-units and indefinite class theorem are precisely those
in the reviewed177-line split composition; they were never restricted to
split dyadic auxiliary fields. Therefore the general native DECISION
endpoint is reviewed WRITTEN under those retained GRH hypotheses.

The two new audit estimates total1.148860USD, not invoices or balances.
The prior distinct four-word request ended EMPTY at2.587180USD and supplied
no evidence. OpenAI is disabled. No new test or quantum implementation was
needed: the decisive result is the all-input source-checked proof, not the
finite negative-gap searches. Universal four-word completeness stays OPEN
and is no longer a blocker for this decision algorithm.
