# Binary-Fock passive/Kerr circuits: core composition and classical scope

2026-11-07. CLOSED mathematical composition review, conditional on the
explicit uniform QHT/chirp source guarantee identified below. Read current
STATE/TRAPS and actual retained Iyer Lemma3.1/Theorem4.2 and Prakash
Section2.2/Theorems2.1--2.2/Corollary2.3. No network/API/Git or finite
control was run. A separate source audit must close those source gates;
this review does not substitute an ACCEPT label for that audit.

## Disposition and precise endpoint

No additional mathematical or binary-resource obstruction was found in
the NUMBER-CONSERVING composition. Once the source guarantee is accepted,
the native written algorithm follows without a gap, state-preparation,
normalization, postselection or inverse-oracle promise.

Input: m explicit modes, binary nonnegative occupations n_i with total K,
a list of L two-mode passive gates/one-mode phase gates and onsite gates

    exp(2 pi i (a/b) binom(n_i,2)),  b>0,

with binary rational angles and 0<epsilon<1. All angle/denominator bit
lengths count. The output sampler returns a valid m-tuple summing to K,
within TV epsilon of the ideal number measurement. The stronger endpoint
is a clean-ancilla approximate isometry for the entire fixed-total-K
Hilbert space, including an arbitrary reference, not an assertion that
the finite implementation preserves that subspace exactly.

The gate and classical construction cost is polynomial in m,L, all input
bit lengths, log(K+2), and log(1/epsilon), given the cited uniform source
circuits. Initialization/output alone cost O(m log(K+2)). A claim involving
only L and log K must not omit the rational-angle encoding length.

## 1. One common two-mode transform pays every total sector

Use the physical convention

    B(theta)=exp(theta(a_1^dagger a_2-a_1 a_2^dagger)).

An alternative is fine only with its generator and phase convention stated.
B(2pi)=I, whereas B(pi)=(-1)^(n_1+n_2). Thus reducing modulo pi or using a
fixed-sector circuit only up to its sector-dependent global phase is
UNSOUND when the pair total is superposed. A fixed global K does not fix
every pair total. One-mode number phases are implemented separately.

Let P_pair project onto n_1+n_2<=K. Its dimension is
D=(K+1)(K+2)/2. Apply the SAME product QHT, on a common grid, to the two
number registers for all these inputs. The physical oscillator chirp
factorization is independent of the pair total. The cited Iyer Lemma3.1
gives a basis-vector discretization error zeta at every total <=K once its
grid condition holds; its constant number of factors is fixed for n=2.
Therefore the error operator on P_pair is bounded by sqrt(D) zeta. This
dimension factor is paid by taking zeta<=delta/(2sqrt(D)), not ignored.

More explicitly, let E map number states to the specified sampled Hermite
functions and V be the actual product-QHT clean-ancilla isometry. If each
single-mode QHT has operator error eta, then ||V-E tensor E||<=3eta for
eta<=1. If U_grid is the chirp circuit and B the exact number-basis gate,

    ||(U_grid V-V B)P_pair|| <= 6eta+sqrt(D)zeta.

Choose eta<=delta/12 and the preceding zeta. Decode with the actual inverse
QHT unitary. This yields the desired operator error <=delta, including
ancillary leakage. Sampled Hermite functions need not be treated as exactly
orthonormal: their comparison to V already pays that issue.

Iyer Theorem4.2 explicitly covers arbitrary superpositions of all levels
below its cutoff, and its following phase paragraph fixes the Hermite
phase convention. Its grid is polynomial in K and 1/delta, so its register
and circuit costs are polynomial in log(K+2),log(1/delta). The additional
sqrt(D) factor changes only those logarithms. A sufficiently large common
grid also meets Lemma3.1's exponentially small discretization error.
The physical continuum identities, common grid, phase convention and
uniform constructive QHT are the precise SOURCE interface still requiring
the separate audit; fixed-M Theorem1.1 alone would not justify this join.

Binary rational theta*pi may first be reduced modulo2pi. Its approximation
must be accurate to O(delta/(K+1)), since the fixed-total generator norm is
O(K). This takes O(log(K+2)+log(1/delta)) additional bits. The bounded
chirp decomposition must avoid an artificial tangent singularity; the
source's fixed-range factorizations provide the required interface.

## 2. Kerr and one-mode phases are paid binary arithmetic

Compute the integer t=n(n-1)/2 exactly and r=a t mod b reversibly. This
costs polynomial time in log(K+2) and the input coefficient lengths.
Division by2 is performed on the even integer product, not by assuming2
invertible modulo b. On the residue register, implement

    |r> -> exp(2 pi i r/b)|r>

using O(log(b+1)) binary-controlled one-qubit phase rotations, then
uncompute the arithmetic. Allocate synthesis error over those rotations.
Signed a and nonminimal fractions are harmless after exact normalization.
No factorial, expanded occupation list, b-term lookup or b-branch sum is
required. One-mode rational number phases use the same procedure with a
linear, rather than quadratic, integer argument.

## 3. Full-circuit error and valid sampling

Every exact native gate preserves total number K, hence each mode is at
most K before and after every ideal gate. Assign each passive/Kerr/phase
gate clean-input isometry error at most epsilon/[4(L+1)], including all
arithmetic rotation and QHT errors. Telescoping against IDEAL prefixes
gives total operator error <epsilon/4 on the entire native input subspace.
Earlier leakage is propagated by unitary suffixes; it does not require
assuming that approximate intermediate states satisfy a fresh cutoff.
The same bound holds with a reference. Tracing ancillary registers and
measuring occupations gives TV error <=epsilon/4.

If a finite implementation measures an invalid tuple (an occupation beyond
the register cutoff or a total different from K), replace it deterministically
by the initial valid tuple. This map fixes the ideal distribution and cannot
increase TV distance. No rejection/retry clock is needed. K=0 and L=0 are
handled directly. Fresh ancillary workspaces suffice; no squeezed-state
tail estimate is used in this number-conserving contract.

## 4. Strong classical comparisons and an exact universality check

The following restricted counterparts remain valid:

* Purely passive evolution from a single occupied input mode gives a
  multinomial output law; this is not the arbitrary-Fock-input law.
* Terminal diagonal Kerr/number phases leave number probabilities unchanged.
* Restricted tensor width, fixed small TOTAL photon count or short depth
  can permit classical methods. Their resource parameters must be retained;
  a per-mode occupation cap2 alone does not suffice, as the universal
  gadget below already obeys that cap.
* For Kerr coefficient a/b, the number-dependent phase has period dividing
  2b, hence is a linear combination of at most2b ordinary number rotations.
  The coefficients are complex amplitudes, not mixture probabilities.
  Interleaving t such gates produces a coherent branch expansion whose
  size can grow exponentially in t even when b is a fixed small constant.

An exact native falsifier of the classical-mixture interpretation uses

    K(n)=exp(pi i binom(n,2))
        = ((1-i)/2) exp(pi i n/2)
          + ((1+i)/2) exp(-pi i n/2).

On a one-photon dual-rail superposition, K on one rail acts as the identity.
The mixture of the two rotations with their squared coefficient magnitudes
instead destroys its rail coherence. A subsequent balanced mixer detects
the difference. Thus the Fourier identity cannot be used as a sampler by
choosing branches classically.

There is also a complete elementary universal-circuit embedding. On the
two-mode subspace spanned by |00>,|10>,|01>,|11>, take B balanced. It sends
|11> to a NOON vector supported on |20>,|02>. K is +1 on occupations0,1
and -1 on2, so

    B^dagger (K tensor K) B = diag(1,1,1,-1)

on that subspace. The total0/1 sectors see K tensor K=I; the image of |11>
gets a common minus sign and is mapped back exactly. Applied to the
selected rails of two dual-rail qubits, this is controlled-Z without
leakage. Internal-rail passive gates give arbitrary single-qubit rotations;
Hadamard and the pi/4 number phase, together with this controlled-Z,
embed the usual universal gate set with constant overhead. The initial
occupations can all be0/1 and every Kerr denominator can equal2.

Consequently a uniform polynomial-time classical approximate sampler for
ALL native circuits at a sufficiently small constant TV error would
simulate ordinary bounded-error quantum decision circuits. This is the
conditional implication BQP subseteq BPP, NOT an unconditional hardness
proof, separation, or new optical-universality claim. It is stronger than
inferring difficulty merely from the numeric-K dependence of familiar
boson-sampling algorithms. It also explains why a small Kerr denominator
alone cannot justify a full classical counterpart.

## 5. Direct published scope and remaining claim gates

Actual Prakash Section2.2 explicitly discusses binary Fock encoding and
diagonal Kerr gates. Its Corollary2.3 explicitly claims digital simulation
of Gaussian-plus-Kerr CIRCUITS with an operator-norm input-subspace
guarantee. Thus the present endpoint is already within a published claimed
corollary, rather than an unsuspected composition of isolated gate results.
This review does not adopt that corollary's broader non-number-conserving
cutoff propagation: exact total-number conservation pays our narrower
native contract independently.

After the separate uniform source audit closes, this is an unconditional
written number-conserving digital simulation upper bound under that
published circuit model. Until then retain the explicit source gate.
No novelty, classical separation, physical preparation of exponentially
many photons, practical resource estimate, or full/quantum execution is
established. The quantum output lives in binary qubit registers; the
algorithm does not supply an exponentially large physical photonic state.
