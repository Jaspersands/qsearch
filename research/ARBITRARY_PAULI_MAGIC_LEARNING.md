# Learning one arbitrary Pauli rotation of extensive magic

Started 2026-11-06; derivation completed 2026-11-07. WRITTEN polynomial-time
copy learner for the exact native family. Core, endpoint and actual-source
and final integrated reviews complete.
No executed full learner, novelty, classical separation or hardware claim.

## Native question and selection

Input: fresh exact copies of psi=C exp(-i*pi*P/8)|H>^n, with arbitrary unknown
n-qubit Clifford C and arbitrary signed Hermitian Pauli P, including partial
support. H=cos(pi/8)|0>+sin(pi/8)|1>. No circuit, source inverse, evaluator,
conjugate source, chosen-state query or hidden Pauli axes are supplied.
Output: a polynomial-size preparation within trace distance epsilon, with
failure at most eta, in poly(n,1/epsilon,log(1/eta)) time and copies.

This includes C2 T_j C1 H^n: commute C1 through T_j and absorb C2 C1 into C.
It asks whether one interleaved non-Clifford operation on an extensive magic
product remains learnable. The earlier Z^n theorem leaves a substantive
relative-orientation promise; removing it gives this natural circuit class.

Independent comparison first revisited growing-degree Legendre decoding,
bare supersingular isogeny inputs and graph-state permutation transporters.
None supplied a new paid decoder beyond the previously recorded obstructions.
Galois norm equations already appear in Biasse-Song2510.02280 and the S-unit
literature; no nearby extension was admitted. Corpus been-tried and baseline
lookups for the precise present family returned the canonical learner and
standard tensor-network simulation, not a proof of new coverage or hardness.

Strongest applicable baseline: actual Haug2609.27128 and Aguilar2609.27565
Clifford-product learners; actual source snapshots are in
`audits/sources/one_rotation_learning/`. Known-coordinate bond2 tensor
contraction does not supply an unknown Clifford decoder. The Haug classical
Bell sampler in Appendix I assumes the representation and Clifford are given.
All algebraic processing of the measured Bell labels is classical. The target is
an efficient quantum-copy learner, not a classical-input exponential speedup.
The exact source baseline's active-block tomography costs exponentially in
that block's width; the cubic receiver aims to remove that specific step.

## Bell interference and a uniform large-support lemma

Use labels v=(x,z), q(v)=sum x_i z_i, p the Pauli label, and
ell(v)=q(p)+[p,v]. Let w=weight(p), k=#Y factors, r=w-k. The base Bell law
mu is a product with local masses I:1/2,X:1/4,Z:1/4,Y:0 and support B.
For U=exp(-i*pi*P/8), P^T=(-1)^q(p) P. Direct multiplication gives

    U^T W_v U = W_v                              if ell(v)=1,
    U^T W_v U = (W_v - i W_v P)/sqrt2            if ell(v)=0.

The sign of P changes interference signs only. Define the normalized
ENVELOPE law rho by mu(v) on ell=1 and (mu(v)+mu(v+p))/2 on ell=0.
Its support is S_p=(B union(B+p)) intersect {q=0}. Indeed
q(v+p)=q(v)+ell(v), and ell(v+p)=ell(v). Odd-swap amplitudes vanish.
If q(p)=0 the two real base amplitudes enter in quadrature, so nu=rho.
If q(p)=1 they can interfere. All interference lies in

    O=B intersect(B+p),   mu(O)=(1/2)^k (3/4)^r <=(3/4)^w.

O is invariant under p and has ell=0. Consequently rho(O)=mu(O), and
nu=rho outside O, regardless of constructive/destructive phases.

For any degree<=D Boolean f nonzero on S_p, rho[f=1]>=2^(-2D-3):
if f is nonzero on B, use rho>=mu/2 there and product anti-concentration
4^-D. Otherwise (1+ell(u))f(u+p) is a nonzero degree<=D+1 function on B;
its mu mass transfers with factor1/2. Therefore

    nu[f=1] >= 2^(-2D-3) - (3/4)^w.

For w>=25, 1024*3^25<4^25, so the complete degree<=3 vanishing kernel
of nu EQUALS that of S_p, and its support gap is at least1/1024. This
is an all-n proof, including arbitrarily many inactive H sites. No lower
bound on individual probabilities or approximately noncancelling outcomes
is required. At w=1,P=Y the state is |+> (opposite sign gives |0>), so
an unconditional all-weight equality with the envelope is FALSE.

## Affine normal form and candidate physical axes

On one Bell plane, affine permutations fixing Y preserve q and B.
For p_i=X use (x,z)->(z,x); for Z use identity; for Y use

    (x,z)->(x+z+1,z).

The latter's LINEAR part sends Y to Z; its affine map fixes Y. It is
essential to transform translation directions by the linear part A, not
by the full affine map g. Thus g(B)=B and
 g(B+p)=B+A p,
with A p equal to Z on active sites and0 on inactive sites. The envelope
is exactly affine-equivalent to the previous canonical active-block support.
Every such local affine map is induced by a single-qubit Clifford Bell
relabeling; the algebra only needs its symplectic linear part.

For w>=25 the canonical active K2=<q_active>, K1=0, and the reviewed cubic
Lie/square-zero/Macaulay method from ONE_ROTATION_MAGIC_LEARNING.md applies
to its K3. With unknown observed linear frame F, its w+1 physical candidate
axes include F p: pull the canonical all-Z direction back by A^-1, then
forward by F. No hidden coordinate frame or coefficient search is supplied.
The source/block composition and small-weight resource bound are given below.

## Uniform small-weight gap, including stabilizers

At every nonzero base Bell label, mu(v)=2^(-w-j) for an integer0<=j<=w.
Every positive base mass is therefore at least4^-w, and two unequal base
amplitude magnitudes differ by a ratio of at least sqrt2. An interfering
nonzero destructive pair has probability

    (a-b)^2/2 >= (sqrt2-1)^2 min(a^2,b^2)/2 > 4^-w/12.

Equal destructive amplitudes give exactly zero, which is allowed; equal
constructive, quadrature, single-amplitude and unchanged outcomes satisfy
the same lower bound. For w<=24 every nonzero core Bell probability is
at least c=4^-24/12. No finite enumeration, gap oracle or source advice is used.

Treat the entire active core as ONE finite variable and inactive qubits as
independent variables of smallest mass1/4. The product anti-concentration
lemma applies to arbitrary bases of functions on each support. A Boolean
quadratic has degree at most2 in these block variables. Since there is only
one rare core variable, every nonzero quadratic on the WHOLE support has
probability at least c/4. Explicitly: if a surviving degree2 inactive
coefficient is nonzero, it is constant in the core and each core restriction
has violation at least1/16. Otherwise the inactive degree is at most1;
one core value of mass at least c has a nonzero restriction, giving c/4.
The w=0 case is an ordinary H product with quadratic gap at least1/16.
Global Clifford Bell relabeling preserves degrees and probabilities.

Thus the known absolute bound

    gamma_* = 4^-24/48

is valid for every n and arbitrary signed P. For w>=25 the much stronger
1/1024 bound above applies. The universal constant is deliberately crude:
its inverse is about1.35e16. Polynomial asymptotics do NOT make this a
practical sample bound. The tighter proof replaces a valid but much weaker
cyclotomic-integer norm estimate; no optimization claim is made.

## Complete algorithm and resource/error accounting

Assume n>=1 and 0<epsilon,eta<1. All symbolic operations and branch clocks are capped.
Malformed dimensions, tableaux or algebra structures return ABORT.

1. Run actual Haug Theorem2/AlgorithmS1 with gap gamma_* and failure eta/4.
   It learns the exact Clifford decoder D and irreducible pure blocks using
   O(gamma_*^-1*(n^2+log(1/eta))) Bell samples and polynomial classical time.
   It removes stabilizers and reads their signs on a fresh decoded copy.
   If no residual qubits remain, output the known stabilizer preparation.
   No block-size exponential enters this structural step. The source's
   uniform quadratic-kernel event pays adaptive projections too.
2. If all recovered blocks have size at most24, use source AppendixE block
   tomography with GLOBAL trace target epsilon/2 and failure eta/4. Allocate
   block infidelity (epsilon/2)^2*d_alpha/sum_beta d_beta and confidence
   eta/(4r), where r is the number of blocks. Pure constant-size block
   descriptions and known D give a preparation. Reserve epsilon/2 for
   normalization, finite-description and gate-synthesis errors, allocating
   vector error epsilon/(2r) to each block. Output it DIRECTLY. The source
   guarantee and triangle inequality give error<=epsilon, failure<=eta/2.
   Do not use the exact-candidate all-zero verifier on this approximate branch.
3. Otherwise, on the exact-structure event there is one active block of
   size w>=25, no stabilizers, and inactive H singletons. This follows from
   K1=0 and K2=span(q_active,q_inactive_i): full affine spans exclude mixed
   equations. Source uniqueness leaves only a local Clifford in the active
   block. Apply known D to fresh copies and retain that pure block; no
   postselection or unknown inverse is used.
4. Learn its complete degree<=3 kernel with failure eta/4, using

       ceil(1024*(D3(w)*ln2+ln(4/eta))) Bell samples,
       D3(w)=1+2w+binom(2w,2)+binom(2w,3).

   Invoke the already proved polynomial cubic Lie/square-zero/degree3
   Macaulay extraction. The local affine normal form is proof coordinates
   only. The R=w+1 physical candidate axes include the true rotation axis.
5. For each candidate, correct that Pauli on FRESH decoded n-qubit copies,
   and run the capped finite-H product learner with failure eta/(4R).
   On the true axis, either sign leaves exactly C' H^n. Validate each
   returned Clifford tableau and finite-H labels; wrong branches may return
   ABORT or arbitrary valid preparation circuits. Undo the correction and D
   in each returned known preparation V, thereby targeting the ORIGINAL state.
6. Test each V on fresh ORIGINAL copies by applying its known inverse and
   accepting only if every measurement is zero, with

       m=ceil(epsilon^-2*ln(4R/eta))

   tests. A state farther than epsilon has zero-outcome probability
   F<1-epsilon^2 and passes with probability at most eta/(4R). This remains
   valid conditionally on all previous adaptive choices, because tests are
   fresh. The successful true finite-H branch returns an exact preparation
   and passes certainly. Return an accepted V, or ABORT if none passes.

The large-branch total failure is bounded by
 eta/4 + eta/4 + eta/(4R) + eta/4 < eta.
The small branch needs no candidate verification and its failure is at most
eta/2. This distinction avoids incorrectly assuming F^m is close to1 for
merely approximate tomographic candidates.

Copies are bounded by the sum of the structural term above, O(n^3+log(1/eta))
active cubic samples, O(n*(n^2+log(n/eta))) capped product-learning samples,
O(n*epsilon^-2*log(n/eta)) verification samples, and (on the small branch)
O(n*2^24*epsilon^-2*log(n/eta)) tomography copies. All other processing has
polynomial matrix sizes and bit precision. Pauli corrections use O(n)
Clifford gates and one T; finite-H states are exactly Clifford+T preparable.
Bounded-block approximate preparation uses polynomially many gates to the
stated accuracy. Ideal gate operations and exact fresh copies are promises.

## Baselines, falsifiers and remaining boundaries

The actual source already learns logarithmic Clifford-product width with
an inverse-polynomial gap; small support alone is not a new result. The
present class also contains the previously proved full-width all-Z states,
so its unbounded-width endpoint requires the cubic operation. This is a
source-applicability statement, not a complexity lower bound. Random doped
states from stabilizer inputs and process/Choi learners do not automatically
supply this worst-case one-output-copy contract.

The main falsifiers were destructive interference causing extra low-degree
relations at growing w, affine-point rather than physical-axis transport,
unpaid small-core gap, unavailable hidden block coordinates, and a false
completeness argument for approximate candidates. These are addressed by
explicit proofs and the actual source composition; finite controls only
check selected algebra/phase mistakes. No noisy/approximate source promise,
arbitrary-angle, two-rotation, arbitrary MPS, channel-identification,
classical separation, novelty or practical implementation claim follows.

No adjacent extension or larger implementation is queued. The next scientific
pass must independently rank native end-to-end mechanisms by external value.

## Evidence and review dispositions

Core algebra reused unchanged from ONE_ROTATION_MAGIC_LEARNING.md and its
closed cubic-axis review. New reviews:
`audits/reviews/2026-11-06-arbitrary-pauli-gap.md`,
`audits/reviews/2026-11-06-arbitrary-pauli-endpoint.md`, and
`audits/reviews/2026-11-06-arbitrary-pauli-block-source.md`, plus final
`audits/reviews/2026-11-07-arbitrary-pauli-integrated.md` (accepted after
the zero-residual stabilizer guard and quantum-processing prose fixes).
Primary Haug2609.27128 and Aguilar2609.27565 snapshots/hashes are retained
under audits/sources/one_rotation_learning/. Parent checked Haug's actual
Theorem2, AlgorithmS1, LemmaS5, AppendixE and finite-H identification scope.

Claude packets/runs: audits/claude_inputs/2026-11-06-arbitrary-pauli/ and
corresponding audits/claude_runs/2026-11-06-arbitrary-pauli-* directories.
Both terminated end_turn with reports. Opus Bell audit used1209 input and
17015 output tokens, estimate USD0.345136. Its gap/deletion proof is verified.
Correct its P=Y example to |+> for the stated positive sign (negative gives
|0>); the extra affine-equation counterexample survives. Its affine-measure
warning is accepted: only the envelope's SUPPORT algebra is transported.
The cutoff25 is sufficient, not necessary; no optimal-cutoff claim is used.

Fable small-core audit used1312 input and21488 output tokens, estimate
USD1.08752. Its independent Q(zeta16) integer-norm proof of the weaker
2^-2368 quadratic bound is valid: conjugate rotations remain unitary,
nonzero norm is an integer, and product regrouping is paid. The elementary
amplitude proof above supplies the stronger bound actually used. Correct
its closing hypothesis-count wording: the polynomial space has D2 dimensions
but 2^D2 hypotheses; the logarithm of that count is O(n^2). The source and
our cubic sample bound use the correct union bound. Total estimated charge
USD1.432656, not an invoice or exact remaining balance. No retries.

Exact control: audits/controls/arbitrary_pauli_learning/interference_control.py
and .json. In Q(zeta16), four deliberately selected cases check every Bell
label: Y (support2 versus envelope3); YZZZ (106/106); partial YZZZI
(318/318, two quadratic factors); YZZZZ (327/333, six destructive zeros).
All verify exact off-overlap law, overlap mass, normalization and correction.
The existing n4 decoder is reused on affine-scrambled YZZZ labels, returning
five axes including physical axis81, quotient dimension6 and ZERO coefficient
assignments searched. Treating an affine point as a direction is rejected.
The script's initial Sage rational-constructor call was repaired before the
successful run; no mathematical assertion was weakened. It is a finite
identity/extraction control, not the full copy learner or an asymptotic test.
