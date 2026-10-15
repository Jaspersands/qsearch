# Dense-Free Two-Call Banded-QFT Classical Sampling

## Research Decision

The former transfer-matrix audit counted local contractions for ONE outcome,
while its verifier enumerated every outcome and allocated length-3^M root
arrays. That is useful finite validation, not a scalable sampling baseline.
This subsystem computes joint prefix masses, actually samples without dense
word/state/root tables, and pays both integer precision and random bits.

CLI: `python qsearch.py native-banded-qft-baseline`.
Artifact: `research/classical_baselines/native_banded_qft_baseline.json`.
Independent checker: `research/certificates/native_banded_qft_baseline_crosscheck.js`.
The classical solver input is the SAME public per-site response phases, obtained
from the original observations and public mask. No hidden shift, secret, errors,
preimage table, extra original samples or oracle is granted.

## Scope And Unitarity

Let q >= 2, M sites, D=3^M, digit phases eta_j(t) and b in [1,M]. Use
the banded Fourier kernel with positive phase
sum_k v_(M-1-k) sum_(ell=k..min(M-1,k+b-1)) w_ell/3^(ell-k+1),
and normalization D^-1/2. Input and output digits are MSB first.
Both call signs (+,+) and (+,-) are supported.

This IS unitary: for two distinct output rows, let k be the first differing
reversed output digit. The phase difference involving w_k has only that
digit's nonzero coefficient divided by 3; summing w_k over {0,1,2} vanishes.
Equal rows have norm one. This also fixes the b=1 reversal convention.

Eliminate each intermediate digit t independently, giving

    L_k(w_window,x_window) = (1/3) sum_t exp(2 pi i [
        (eta_k(w_k)+sign*eta_(M-1-k)(t))/q
        + t sum_j (w_(k+j)-x_(k+j))/3^(j+1)]).

The output amplitude is D^-1/2 sum_w product_k L_k. The structural amplitude
contraction has 3^(b-1) boundary states. That alone does NOT prove sampling.

## Prefix Mass Contraction

For a fixed leading output prefix, sum unspecified x digits as well as w,w'
in |sum_w product L_k|^2. Each site variable is (w_j,w'_j,x_j), with 9
possibilities when x_j is fixed and 27 otherwise. Its local factor is
L_k(w_window,x_window) conjugate(L_k(w'_window,x_window)).

Sweep k FORWARD. The table before step k is indexed by sites k..k+b-2.
Enumerate the window k..k+b-1, multiply by the local factor, sum the earliest
site variable, and retain sites k+1..k+b-1. Near the right end, shrink the
window. Start with one for each initial boundary assignment; finish at the
empty boundary. This is ordinary variable elimination on a window chain.

Boundary <=27^(b-1), windows <=M*27^b per prefix. At most 3M+1 contractions
produce one sample, so <=(3M+1)M*27^b windows, not O(M*3^b) sampling.
Local factors are cached in at most M*9^b entries, separately from the
27^(b-1) live boundary; cached prefix weights also consume charged storage.
Actual window counts, peak boundaries, root calls, integer bit lengths and
random bits are recorded. For b=O(log M), this structural cost is polynomial.
For b=M this exact-bandwidth contraction is exponential. That does NOT mean
approximate sampling of the FULL cyclic transform is hard; see below.
More calls/entangling schedules are not covered by this implementation.

## Global Precision Without Rare-Prefix Normalization

Choose a phase grid of denominator 2^P. Arb encloses every needed unit root
from an exact rational turn and certifies that its dyadic complex approximation
has absolute error <=epsilon=4*2^-P, using the stronger L1 component bound.
All roots are certified BEFORE sampling. Only O(M*9*3^b) possible roots are
needed; duplicates are shared. No array of size q or 3^M is constructed.
The implementation trusts FLINT/Arb enclosures. The stored live controls also
have independent JS rational Machin-pi/Taylor verification of those roots.
This does not certify an arbitrary hardware implementation.

Each L has magnitude <=1 and approximation error <=epsilon. If M epsilon<=1/2,
telescoping gives local-product error <=M epsilon(1+epsilon)^(M-1)<=2M epsilon.
There are D summed paths and D outputs, hence the complete unnormalized vector
error E<=2 D M epsilon. Since E<1, the approximate vector is nonzero; normalizing
it changes its distance from the true unit vector by at most another E.
Pure-state measurement TV is therefore <=2E, without assuming any prefix has
large mass or precision proportional to its conditional probability.

For failure target 2^-f choose

    P = f + ceil(log2(32 M 3^M))
    K = f + ceil(log2(4M)).

Then phase TV <=16 M 3^M 2^-P<=2^(-f-1). A K-bit uniform grid compared to
the two exact ternary CDF thresholds contributes <=2*2^-K per digit and
<=2M*2^-K<=2^(-f-1) per sample. Sequential coupling sums the losses.
The TOTAL TV <=2^-f under independent ideal bit draws. Injected PRNG controls
test the algorithm, not the IID premise. Batch loss is <=count*2^-f.

The factor 3^M in this conservative ERROR bound costs only O(M+f+log M)
BITS, not an exponential table. Each local factor numerator is the sum of
three Gaussian integers. Its common denominator is 3*2^P. The doubled network
uses only exact Gaussian integers; every prefix has the SAME denominator,
so normalization and CDF comparison cancel it. Intermediate integer bit
length is O(M(P+1)); big-integer arithmetic and root evaluation costs are
NOT unit cost. No unconditional ideal-root exact sampler is claimed.

## Operational Failure And Falsifiers

Width, root entries, enclosure bits and an entire batch's worst-case work are
preflighted before drawing random output bits. A cap returns explicit UNKNOWN,
not hardness. No unresolved prefix is replaced by a guessed conditional law.
If a preflight fails, there is NO certified completed sampling workflow for
that configuration. Limits can be raised; exhausting them is not advantage.

Falsifiers: any small exact/numerical full-circuit distribution disagrees
beyond the global TV budget; prefix children do not sum exactly to their
parent; root errors exceed epsilon; measured work exceeds declared bounds;
or a sampler accesses hidden calibration information. Tests cover each.

## Full Cyclic QFT At Inverse-Polynomial Accuracy

A qutrit controlled rotation between digits at distance d has denominator
3^(d+1) and digit product at most4. Omitting it changes the gate in operator
norm by at most8*pi/3^(d+1). There are M-d such gates. Telescoping the SAME
qutrit Fourier circuit, including unchanged digit reversal and local F3
gates, gives

    ||F_full-F_band|| <= (176/7) sum_(d=b..M-1) (M-d)/3^(d+1)
                     <= (88/7) M/3^b.

To identify the kernels with the truncated circuit explicitly: process input
sites k in increasing order, apply F3 at site k, then apply the retained
controlled phases between its new output digit and still-unprocessed input
sites ell>k. Reverse output digits at the end. Its path phase is exactly
sum_k v_(M-1-k) sum_ell w_ell/3^(ell-k+1). Dropping ell-k>=b therefore gives
the kernel used by the baseline, not a merely similar unitary matrix.

The schedule uses BOTH a forward Fourier transform and its adjoint. Their
joint state error is bounded by twice this quantity; complete Born TV is
at most that state error. Choose

    b = min(M, ceil(log3(64 M 2^f)))

with exact integer comparisons. The joint truncation TV is <=2^(-f-1).
Run the banded sampler at failure_bits=f+1, contributing another <=2^(-f-1).
Total TV to the FULL ideal two-call distribution is <=2^-f. A full-cyclic
wrapper executes this construction when its work/precision caps permit.
The ledger and independent checker charge both transforms and the combined
loss; matrix operator-norm tests verify the truncation formula at small M.

For target delta=2^-f, 27^b=O((M/delta)^3), so the structural sample cost
is O(M^5/delta^3), with polynomial-size integers and paid public input/root
arithmetic. For inverse-polynomial delta this is a POLYNOMIAL classical
sampling construction. Its degree/constants can be enormous: the default
caps cannot execute many moderate full-cyclic profiles. That is operational
UNKNOWN, NOT a falsification of the constructive polynomial bound. There
is no claim of practical dominance over the quantum circuit. Exponentially
small delta also makes this construction exponential.

Thus full twiddle bandwidth does NOT rescue an exponential sampling advantage
for this TWO-CALL public product-phase schedule at inverse-polynomial
resolution. A putative distinguisher with inverse-polynomial advantage must
face this paid classical simulation. Exact sampling, more calls, different
mixers and COPY-ONLY unknown coset states are separate questions. Public
classical phase access is essential and must NOT be silently transferred to
those other models. No general LWE/DHSP or quantum-algorithm no-go is inferred.

The same pass corrects the older Fourier note: data-phase cancellation on
w=v leaves quadratic Fourier phases, not a probability floor. The written
single-call conditionals required 1/3 normalization, not 1/sqrt(3).

This is a serious classical baseline for a narrow schedule family, NOT
a recovered secret, new speedup, general quantum lower bound, EXACT
full-bandwidth sampler or new active negative result. Next useful experiments must
beat this baseline on public input and complete sampling costs, not selected
outcome amplitudes, private errors, or brute-force caps.
