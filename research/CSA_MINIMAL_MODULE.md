# Minimal modules for arbitrary central simple algebras

2026-11-07. REVIEWED WRITTEN quantum polynomial-BIT construction under GRH.
Independent source/full-core reviews, exact classical control and two focused
Claude attacks complete. No human peer review, formal verification, novelty,
classical separation, expanded-output bound or full/quantum execution claim.

## Native question and selection

Given a number field K of growing degree m with expanded defining polynomial,
maximal-order basis and arithmetic, and a promised central simple K-algebra A
of growing degree n given by expanded structure constants and identity, compute
its Schur index d and an explicit primitive idempotent e in A. Output e and a
basis of the minimal left ideal Ae in canonical arithmetic-DAG form, together
with the action of A on it. The target is bounded-error quantum polynomial BIT
time under explicit GRH, polynomial in the full input and log(1/eta). The output
is exact but compact, not an expanded, integral, small or short element.
No splitting field, minimal module, maximal A-order, class/unit group, local
invariant or solution advice is supplied. K/CSA promises are not recognition
tasks. Failure of a finite clock is ABORT. Minimality is part of the mathematical
contract, not inferred from a finite example or an agent's approval.
Here CANONICAL means deterministic reconstruction FROM A RECORDED TRANSCRIPT
(samples, primes and pivot sets). It does not mean a unique input-canonical
idempotent, lexicographically first nonzero minor, or canonical-form algorithm.
Those stronger tasks could require additional compact zero tests.

This is the constructive irreducible-representation step in computational
associative algebra. Selection began with STATE/TRAPS, corpus been-tried
"central simple algebra isomorphism nonsplit minimal module Schur index" and
"Brauer equivalence central simple algebra isomorphism Schur index", then
primary literature. Baselines query: "central simple algebra Schur index
division algebra minimal module". The catalog returned class-group index calculus
and quaternion norm methods, not a matched all-degree solver. Independent
alternatives were general sparse relation descent (no paid constant-map
operation), polynomial-rank stabilizer learning (the last exact-rank falsifier
does not supply a constructive learner), and wild Selmer computation (still
missing a uniform local-image clock). None supplied as direct a constructive
route as the following minimal-module reduction. No new backend is proposed.

Mechanism: CLASSICAL factoring-oracle Schur index -> prescribed degree-d
splitting field F -> EXISTING KM split-algebra quantum algorithm -> simple
A-module F^n -> canonical linear algebra extracting an idempotent inside A.
This directly removes the minimal-module blocker recorded in
MIXED_GAUSSIAN_PAIR_LEARNING.md. A degree-n splitting field alone gives the
regular module and does not remove it. A tensor A^op also only gives a regular
module and is already classically explicit.

Expected asymptotic benefit, if all gates close: polynomial quantum BIT
construction in growing field/algebra degree, reusing known factoring and
complete S-unit algorithms. Strong classical competitors include maximal-order
recognition (already sufficient for d), quaternion/conic algorithms, prescribed
cyclic presentations when genuinely given, and classical S-unit computation
inside the SAME KM reduction. No classical lower bound or separation is known
here; the quantum primitive itself is published. Priority remains UNKNOWN.

Cheapest falsifiers: a classical all-degree matched construction; an uncharged
minimal-field assumption; impossibility of polynomial-height simultaneous
irreducibility/sign constraints; regular rather than simple module; compact
rank/zero testing hiding general arithmetic-circuit identity testing; division
or exponential expansion in the extraction; invalid prime-adaptive sampling.

## 1. Reuse the classical index computation

Nebe--Steel, actual §§3.1--3.2, treats arbitrary number-field CSAs. A maximal
order's RELATIVE REDUCED-TRACE discriminant ideal has q-exponent n(n-n/d_q), giving each
finite local index d_q. The trace-form signatures give the real index 1 or 2;
d=lcm_v d_v. The rational discriminant shortcut in their Theorem3.12 requires
uniformly distributed invariants and is NOT used here. No finite local Hasse
numerator is needed. Actual Voight Theorem7.2 pays a maximal order of a GENERAL
semisimple number-field algebra in deterministic polynomial time with integer
AND finite-field polynomial factoring oracles. Ordinary randomized polynomial
finite-field factoring removes the latter oracle. Thus the classical baseline
is randomized polynomial BIT given integer factoring, without GRH. Do not
claim a new Schur-index algorithm or deterministic factoring-only algorithm.

For explicit uniformity, apply the theorem to Res_(K/Q) A, of rational dimension
m*n². A maximal Z-order contains central O_K (adjoining central integral
elements gives an overorder), hence is a maximal O_K-order. No free O_K-basis
or principal ideal generator is assumed. Write Lambda* for its relative
reduced-trace dual and M0=Lambda*/Lambda. These full Z-lattices are computed
from expanded input using linear algebra/HNF. Factor |M0|. For q above p put
E=v_p(|M0|); Lambda*/(Lambda+q^E Lambda*) is the q-primary part of M0, whose
cardinality is Norm(q)^length_q(M0). This determines the required relative
discriminant exponent. E is polynomial NUMERICALLY in the bit input, so this
uses polynomial-size ideal powers. Never substitute the regular-trace
discriminant used only for a support superset into the local-index formula.

An initial integral order is obtained by clearing multiplication denominators
in a basis including1. All overorders lie in its trace dual. HNF-normalized
lattices therefore have polynomial bit height, and each strict enlargement
reduces a polynomial-bit discriminant by a nontrivial square. Finite-algebra
radicals and maximal TWO-SIDED ideals, rather than minimal LEFT ideals, suffice
in the radical/idealizer process. This distinction prevents circularity.

The expanded maximal order and d also have a deterministic polynomial positive
certificate under the input promises. Check its lattice contains the initial
order, contains O_K and is closed under products. Factor the initial absolute
trace discriminant completely, checking all prime factors and their product;
take all K-primes above these factors. Outside this set the initial order is
already maximal by the nondegenerate trace reduction/dual argument. For each
remaining q, work in the expanded finite algebra C=Lambda/q Lambda. Certify a
two-sided ideal Jbar is nilpotent (its powers vanish within dim C steps) and
that B=C/Jbar is semisimple, as follows. Supply a separability element
z=sum x_i tensor y_i with sum x_i*y_i=1 and

    sum b*x_i tensor y_i = sum x_i tensor y_i*b  for every basis b of B.

These are finite-field linear equations. Such z averages a vector-space
projection into a B-module projection, proving semisimplicity; conversely
finite-field semisimple algebras are separable, so search can solve this system.
Nilpotence and semisimple quotient together prove Jbar is the radical. Compute
the center of B by linear equations, and certify it is a field using a generator
with a full-degree irreducible polynomial. Thus B is SIMPLE. For J the preimage
of Jbar, check the expanded idealizer O_r(J)=Lambda by lattice linear algebra.
Nebe--Steel Theorem3.7 makes the order hereditary at q; its hereditary block
description and Lemma3.10 show simple residue quotient means one block, hence
maximality. These checks use no minimal left ideal or noncommutative splitting
oracle. Recompute the relative discriminant and real trace signatures to verify
d exactly. This certificate is independent of GRH and S-unit completeness.
It is ESSENTIAL for a deterministic primitivity certificate: the compact
module/extraction checks below also work with a larger field degree a that is
a multiple of the true index, and then produce a nonprimitive idempotent.
Finding a full-rank module map never certifies the reported index by itself.

Let S contain all finite ramification places, computed from this discriminant,
and all primes of K above2. Its size and all log norms are polynomial. The
trace-order support construction in REDUCED_NORM_PRESCRIBED_FIELD.md §1 is an
alternative paid superset, not an extra oracle. Real nonsplit places imply
2|d. If d=1 set F=K and proceed directly to §3.

The initially considered alternative was to compute the period from KM's
Amitsur cocycle c without forming A tensor powers: Theorem4.11 uses the SAME
support S for every c^j, and a full S-unit differential lattice determines the
positive generator of {j: c^j is a coboundary}. Over number fields this is d.
This route is unnecessary for the selected algorithm and is not implemented,
promoted as new, or used to replace the stronger classical index baseline.

## 2. An expanded degree-d splitting field

For each q in S choose a monic irreducible degree-d polynomial over O_K/q.
Uniform monic sampling with finite-field irreducibility testing succeeds with
probability at least1/(2d): the number of degree-d elements in F_(q^d) is
q^d minus those in its proper subfields, at least q^d/2, and every irreducible
has d roots. Cap retries polynomially for an aggregate error budget. d=1 was
already separated. All finite field dimensions and log norms are charged.
For clarity, the union bound is <=sum_(j=1)^floor(d/2) Q^j for residue size Q;
this is <=Q^d/2 for d>=2,Q>=2 (check d2,3 directly and use the geometric sum
for d>=4). At most ceil(2d*log(5|S|/eta)) trials per prime suffice.

Put I=product_(q in S) q and M=Norm(I), so M O_K is contained in I. For each
coefficient i<d, use ideal CRT/HNF to choose N_i in O_K congruent to the local
coefficient minus the coefficient of X^d+1. These residues and HNF representatives
have polynomial BIT height. Compute a rational integer U>=1 bounding EVERY
|sigma(N_i)| for real embeddings sigma (a root bound plus the known integral
basis suffices); log U is polynomial. Choose a polynomial-bit positive integer
T=1+M*2^s with T>=4dU. Set

    P(X)=X^d+1+sum_(i=0)^(d-1) (N_i/T) X^i.

T is1 modulo I, so P has the chosen irreducible reduction at each q. It is
q-integral and irreducible over K_q, hence [F_w:K_q]=d for the unique place w
of F=K[X]/P above q. Since S is nonempty, P is irreducible over K. Its expanded
coefficients have polynomial BIT height and [F:Q]=m*d<=m*n. At a real nonsplit
place, d is even and

    sum_i |sigma(N_i/T)*x^i| <= (1/4)*max(1,|x|^d),

so P(x)>0 for all real x. Thus every extension of that real place is complex.
At each finite ramified place d_q|d, so its full local degree d kills the
invariant. Goldstein--Schacher Lemma1 now proves F splits A. At all other
places A was already split. No cyclicity, embedded degree-d field, PIP,
Grunwald--Wang construction or normal closure is required.
Residue maps/lifts come from the expanded prime ideals by HNF/finite-field
linear algebra; they are computed, not supplied as advice. Converting the
relative field to an absolute field is paid: a primitive element beta+t*alpha
with integer t in a grid of size>(m*d)^2 separates embeddings, tested by
squarefreeness of the resultant. Its expanded degree/height and the basis
conversion have polynomial BIT size. Computing its maximal order is a NEW
factoring-paid number-field call, not inherited advice from O_K.

## 3. The minimal module and compact interface

Apply the KNOWN KM split algorithm to A tensor_K F, of degree n over F.
Its compact representation rho into M_n(F) is reconstructed canonically from
a verified expanded Amitsur presentation Phi and a small-atom cochain alpha.
The exact verification/search interface is REDUCED_NORM_PRESCRIBED_FIELD.md §5:
component atoms are lifted by1-e+e*u, all torsion is retained, mapped SMALL
expanded atoms and the expanded cocycle are passed to LS's full integer
relation kernel, and HNF solves the binary exponent equation. No relations
on compact sums, hidden logarithm inverse, arbitrary rho or generic PIT.
The corrected complete S-unit source and explicit GRH support bound remain
charged. New absolute field degree is m*d; the largest etale tensor dimension
is m*d*n^3<=m*n^4. Factoring pays maximal orders of these NEW number fields.

V=F^n has dim_K V=n*d. Write A=M_r(D), deg D=d, r=n/d. Its unique simple
left module has K-dimension r*d^2=n*d. Therefore V is simple. This is a
dimension theorem, not a sampled-rank observation. rho is a finite circuit
over known fields with binary powers and a canonical construction certificate.

For extraction use rational coordinates throughout, avoiding arithmetic over
a possibly split finite K-algebra during modular pivot selection. Put
R=m*n^2=dim_Q A and N=m*n*d=dim_Q V. Let L_b be the expanded left-regular
matrices of a rational basis b of A, including the center, and R_b=rho(b)
on V. An A-linear map f:V->A satisfies

    L_b f = f R_b  for every b.

This is a compact rational homogeneous system on R*N entries. Its kernel
has Q-dimension N: for A=M_r(D) and V simple,
dim_K Hom_A(V,A)=r*d^2=n*d. More generally the equality dim Hom_A(W,A)=dim W
holds for EVERY finite A-module W, so the rank upper bound does not rely on
minimality. Expected rank is R*N-N. A nonzero minor of exactly that size,
certified by modular evaluation, supplies both equality and a canonical Cramer
kernel basis. No arbitrary additive identity test is needed: the upper rank
is a proved consequence of the certified representation and the CSA promise.

Choose a linear combination f of this N-dimensional kernel basis using an
integer grid of size4N. An injective f exists (V embeds in regular A); a fixed
nonzero N-minor is a degree-N polynomial in the sampled coefficients. Thus
f has full column rank with probability>=3/4. Select and certify an N-minor
modulo a FRESH prime after f is fixed. Its image L has dimension N and is a
left ideal. Denote the columns l_j. Solve for e in L with

    l_j e = l_j for every j.

Every left ideal of a semisimple algebra is Ae for some idempotent, so this
affine system is consistent. In M_r(D), L is the column ideal; the linear
map e -> (l_j e)_j on L has rank dim_Q D=m*d^2. More generally a left ideal
of K-dimension n*a has this rank m*a^2, whether or not it is minimal. Certify
a minor of that predicted size, set nonpivot variables to0, and build the
affine solution by Cramer. Consistency plus the proved rank upper bound means
the selected independent rows imply ALL equations. Then e^2=e, L=Ae and
dim_K L=n*d, hence e is primitive. The N columns of f are a Q-basis. Choose the
underlying rational basis of V as omega_a*theta^t*e_i, where (omega_a) is a
Q-basis of K with omega_1=1. The n*d columns with a=1 form a K-basis of L, and A-linearity
makes the other columns their known K-multiples. The certified rho gives the
action on this basis. d=n (division) and d=1 (split) are included.
The general affine-rank formula can be seen without computing a Wedderburn
map: mathematically conjugate an idempotent generating L to diag(I_t,0) in
M_r(D0), with deg D0=d0 and a=t*d0. L consists of matrices with only the first
t columns nonzero. Right multiplication on L by u in L depends exactly on
the first t rows/columns block of u. Its K-rank is t²*d0²=a². This proves
the rank upper bound; that conceptual conjugation is never input or computed.

## 4. Compact clocks and verification obligations

All determinant, adjugate, binary-power and field operations compile into a
polynomial-size rational arithmetic DAG. Determinants use division-free
Berkowitz, not a factorial list. Any inverse introduced in Cramer is a scalar
rational inverse with a certified nonzero denominator. For T0 scalar nodes and
H0-bit leaves, unreduced numerator/denominator sizes are <=2^(T0+2)(H0+1)
bits. Reuse the explicit fresh-prime bound in the reduced-norm note §6.
A fixed nonzero maximal minor is preserved with high probability; Gaussian
elimination modulo that prime discovers a minor without listing all minors.
Successful modular nonzero tests are exact lower-rank certificates. Only
canonical constructions, proved upper ranks and consistent systems support
zero identities. Each stage uses a new prime after its rational circuit is
fixed; earlier random pivots may influence later circuits, but not their new
moduli. A failed pivot search or clock is ABORT, never mathematical NO.

Precisely, the INPUT MATRIX is fixed before its modulus, while the pivot minor
is selected afterwards. This is sound: modular nonzero proves that selected
minor is nonzero over Q. For the probability bound, fix mathematically ANY
nonzero maximal minor of the input matrix, independently of the modulus.
A uniform circuit-size bound for ANY minor of that size bounds its height;
one need not construct it in advance or enumerate all minors. A prime avoiding
the input denominators and this one determinant makes the modular rank correct.
Pad T0 by this worst-case polynomial determinant/inverse budget before choosing
the prime. Rational inverse nodes swap numerator and denominator and satisfy
the same exponential bit-height recurrence. When pivot rank is0, use the empty
minor1 and the obvious full kernel; this covers A=K without a special oracle.

Allocate eta/5 to factoring/index, local irreducible polynomials, KM complete
S-unit calls, injective f sampling, and all modular-prime generation/selection.
There are polynomially many stages and component calls; union-bound their
allocated errors and apply explicit polynomial size caps. Deterministic
primality/factor checks reject invalid support factorizations. Index correctness
uses the checked classical algorithm, not the quantum S-unit completeness.
If source completeness fails, an incorrect alpha cannot pass its exact LS
cochain certificate, so that failure produces ABORT or no result.

The algorithm reconstructs only the specified DAG from the checked transcript.
It does not accept arbitrary purported equal circuits. Positive certificate
soundness is independent of GRH under the field/CSA input promises; GRH and
the quantum arithmetic theorems pay success and polynomial search cost.

## 5. Prior-art scope, reviews and classical control

Eight actual primary snapshots are linked in
audits/sources/csa_minimal_module/source.json. Voight7.2 and Nebe--Steel were
read directly. The original Ivanyos--Ronyai proof cited by Voight was not
separately opened. KM2307.00261v3 actual Theorems3.10/4.11--4.13, LS1509.08843
and corrected complete S-unit2510.02280v2 retain the audited interfaces in
the reduced-norm note. Goldstein--Schacher Lemma1 supplies the exact local
splitting criterion; no explicit embedding of F in A or D is taken for free.

The actual de Graaf--Ivanyos maximal-torus source, printed pages1--2 (PDF
pages2--3 visually read because text extraction is font-garbled), constructs
splittings over an extension generated by a splitting element. That does
not promise the extension has degree equal to the index or a minimal module
over K. Actual Polynomial time algorithms for modules, p4 and pp14--16,
Proposition12, discusses primitive idempotents over the REAL OR ALGEBRAIC
CLOSURE, represented over small-degree extensions. It does not solve the
native K-output task. Fieker2009 is relevant prior art but its full text was
not obtained; no theorem scope or absence of a classical algorithm is inferred
from its abstract. Thus priority and complete all-degree prior-art coverage
remain UNKNOWN. The main construction is explicitly a reduction to published
quantum arithmetic, not a newly invented quantum primitive.

Independent source review: audits/reviews/2026-11-07-csa-index-sources.md,
closed and read. Full updated core/certificate review:
audits/reviews/2026-11-07-csa-minimal-module-core.md,201lines, CLOSED and read.
It verifies the full growing-degree composition, exact index certificate,
relative-discriminant extraction, compact ranks and fresh-prime clock.
Both focused Claude Opus/high reports completed with end_turn and were read:

- audits/claude_runs/2026-11-07-csa-minimal-field: estimatedUSD0.278620,
  5350 input/12861 output tokens. Accepted local CRT, sign and finite-field
  density arguments after checking them, and charged NEW absolute-field and
  residue-map construction. The report's splitting criterion was checked
  against actual Goldstein--Schacher. An abstract embedding in D is NOT a free
  computed embedding. Its final suggestion that an all-degree splitting FIELD
  construction alone removes any potential advantage is rejected: that field
  is already classically constructed here; finding the split map over it is
  the remaining known KM task. Optional numerical examples were not used.
- audits/claude_runs/2026-11-07-csa-minimal-compact: estimatedUSD0.581808,
  5372 input/28016 output tokens. Accepted the rank/consistency proof after
  independent verification. Clarified transcript-relative canonicity, exact
  upstream homomorphism, separate index lower bound, and rejection of every
  modular zero denominator. The report did NOT receive the prior prime-clock
  source; its standalone clock is a cross-check, while the note retains the
  already explicit conservative bound. A minor chosen after a prime is sound;
  an existing fixed minor pays probability. No new PIT oracle is assumed.

Total estimated API usage this pass USD0.860428; no failed/empty run or retry.
These estimates are not an invoice or an account-balance observation.

Exact classical control audits/controls/csa_minimal_module/control.py/.json
is CLOSED. A=M2((-1,-1)_Q), n4,d2, the supplied FIXTURE split representation
over Q(i) passed all256 basis products. Its Hom system has2048 equations,
128 variables, rank120 and nullity8; the selected map hasrank8. The right-
identity system hasrank4, e²=e, Ae=image hasdimension8 and eAe hasdimension4.
The regular-module control yields1=E11+E22, which is nonprimitive; the prior
degree4-field realization was reused without rerun. This checks orientation
and dimensions, not the all-size proof or KM execution.

Actual PARI accepts the integral identity-first expanded multiplication table
but algindex raises "computation of Hasse invariants over table CSA is not yet
implemented". That receipt is UNSUPPORTED, not a failed classical theorem or
hardness result. A SEPARATE cyclic-H input returns index2; the displayed M2(H)
structure certifies this fixture, not a general table-to-cyclic conversion.
No backend repair or quantum implementation followed. Finite success does
not prove the algorithm, its clock, practical value or an asymptotic advantage.

## Next research decision

The stated compact primitive-idempotent/minimal-module endpoint is closed as
a reviewed written composition under the explicit assumptions. No arithmetic
backend, expanded-output, integral or nearby module extension is queued.
The remaining scientific issue for this line is its priority/classical
counterpart, not another numerical fixture. Reopen only for an actual stronger
source or a named flaw in the proof. The next pass should start from updated
STATE/TRAPS and compare independent native algorithm mechanisms, using corpus
been-tried then primary literature and the matching baseline before selecting
one decisive experiment. This is a selection gate, not an algorithm claim.
