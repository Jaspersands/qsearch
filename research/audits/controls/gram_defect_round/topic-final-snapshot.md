# Arbitrary-Gram positive boson sampler: bounded proof obligation

Native input is an explicit rational-complex m by N isometry U, N distinct occupied input modes, and an explicit Hermitian PSD rational-complex N by N Gram G with unit diagonal. Internal input is a PRODUCT of PURE states with that Gram; detection ignores internal modes and retains all spatial collisions. Output the FULL N-photon occupation law within TV epsilon by a fixed finite BIT clock. No loss/postselection, hidden purification, random-U promise, or probability oracle. Let d be a certified rational 0<=d<=lambda_min(G), within1/N of lambda_min; rho=1-d, R=N*rho. G=I handled separately. Proposed clock exp(O(R))*poly(full input length,m,N,1/epsilon). Expected advantage: none; this is a rigorous classical comparator for a restricted noisy-photonics regime. No novelty/hardness/quantum speedup claim.

Prior corpus looked up before actual literature. Moylett 2019/2020 section3 already gives positive binomial subset mixture for uniform G=(1-x)I+x11^T, and section5 gives worst-case trace/TV bound for EVERY U. Renema2018 formal Theorems1/2 use uniform overlaps and average random network error. van den Hoven et al2406.17682v2 general formula(11) is Haar/Gaussian interference truncation; evaluated bound(17) uses generalized orthogonal bad-bit model(12),(13), shared rank1 plus diagonal. Do not call their positive mixture or chain-rule sampling new. Arbitrary complex G and full bit clock are the remaining checked question, not literature-wide novelty. Clifford-Clifford/ordered-prefix contractions are strong existing classical baselines.

Mechanism: G=dI+H. Realize phi_i=sqrt(d)e_i+h_i, with all private e_i orthonormal and orthogonal to shared h-space, <h_i|h_j>=H_ij. Private occupation sectors commute with U. Trace internal modes gives an exact positive mixture of independent shared-inclusion coins rho, active S with normalized Gram Gamma=H_SS/rho, and private photons independent categorical |U_yi|^2. This claim must preserve complex Gram cycles, not replace overlaps by magnitudes.

Proposed active prefix DP: s=|S|, fixed ordered prefix y_1...y_r. D_0(empty,empty)=1. For subsets A,B of equal size r, update for i notin A,j notin B:
 D_(r+1)(A+i,B+j) += D_r(A,B) U_(y,i) conjugate(U_(y,j)) Gamma_(j,i).
Then p_r=(s-r)!/s! sum_A D_r(A,A). Unobserved spatial sums should force equality of unused bra/ket indices by isometry. At most4^s states, polynomial transitions per candidate next output and per position. Conditional ratios p_(r+1)/p_r are exact rational and nonnegative. Need rigorous normalization, bit growth and zero handling.

Scalar d via O(log N) exact rational PSD-bisection in[0,1]; no spectral-gap/eigenvector advice. Choose s_max=min(N,ceil(8R+2log2(4/epsilon))). MGFBernoulli E2^|S|<=(exp R) bounds tail. Tail branch returns fixed legal occupation, total TV bounded by tail. Approximate all N inclusion and N spatial categorical coins with fixed b=ceil(log2(16Nm/epsilon)) bits using exact rational cumulative-floor endpoints; no infinite rejection, no tiny-mass cutoff. Zero probabilities must remain zero. Bound common denominator arithmetic by poly(inputbits,s); show all branch clock and all accuracy dependence. No coherent/quantum build.

Cheapest exact Sage falsifier already run: N=m3, real Householder H=I-2vv^T/9,v=(1,2,2); also U=H diag(1,i,1) H. Two Grams diag1, G12=G13=1/8, G23=1/8 or i/8. d1/2. All40 occupation probabilities match exact double-permutation versus positive mixture. All active-prefix normalization/DP identities tested for selected subsets. Triangle phase changes P111 from76804/177147 to76766/177147 for H. PASS is finite consistency only, not theorem. Strong falsifier: ANY valid U,G for which mixture/DP fails, any factorial dependence or reciprocal tiny prefix mass in bit clock. No full theorem from an ACCEPT label.

## Current disposition
Written derivation under independent audit. Exact finite control is audits/controls/gram_defect/{control.py,result.json}, Sage process71448 exited0. Primary PDFs/text/URL hashes are audits/sources/2026-11-13-gram-defect/. No sampler implementation or general proof admitted from controls. Two distinct paid obligations queued: law/phase attack, fixed-bit endpoint.

Paid status checkpoint: Claude process25779 remains in flight. OpenAI process29879 returned terminal APIError with empty response and UNKNOWN billing, reaped exit1; no retry and no mathematical evidence. Initial local import error before this actual request made no API call. Distinguish this new UNKNOWN from the seven old unknown bills.

## Parent derivation: exact law and finite-bit endpoint

For s active photons, use the normalized first-quantized state
(1/sqrt(s!))*sum_sigma tensor_j (u_sigma(j) tensor h_sigma(j)).
The spatial columns u_i are orthonormal, so normalization is independent
of their internal overlaps. Tracing the last s-r spatial outcomes enforces
sigma(j)=tau(j) at each unobserved position. Thus both observed index sets
are the same r-subset A, and each pair of prefix bijections has (s-r)!
completions. This proves the proposed prefix identity, including repeated
output modes and Gamma_(bra,ket) orientation. D_r computes these bijection
sums in the algebra with x_i^2=y_i^2=0; retaining unequal A,B intermediate
coefficients is essential. Sum_r binom(s,r)^2=binom(2s,s)<=4^s bounds all
subset-pair states. For each selected prefix, evaluate all m next outputs
and retain its selected successor table; O(m*s^3*4^s) rational operations
is a conservative full sample bound.

The private-sector expansion is an orthogonal direct sum indexed by which
private internal modes are occupied. Each term has norm1 because input
spatial modes are distinct. Its squared weight is d^(N-s)*rho^s. Spatial U
commutes with each private occupation and detectors are insensitive to
internal mode, so cross-sector coherences cannot affect the output. Inside
a sector, shared and private internal subspaces are orthogonal Fock factors,
with each private species containing one photon. They evolve independently
and their spatial counts add. This proves the positive mixture for every
valid U,G, without assuming a supplied internal realization. The physical
realization proves an identity; the algorithm uses rational G only.

Promise or verify exactly U*U=I and G=G*>=0, diagG=1. The tests have
polynomial rational-bit cost. Exact Hermitian PSD testing uses rational
Schur complements: a negative diagonal rejects; zero diagonal with nonzero
row rejects by its2x2 minor; otherwise remove zero rows or pivot a positive
diagonal. Fraction-free elimination/minor bounds keep polynomial bit size.
Since traceG=N, lambda_min<=1. Bisect [0,1] for ceil(log2 N) steps using
PSD(G-tI), retaining the lower certified endpoint d; bracket width<=1/N.
Treat N=0 and G=I directly. No spectral gap or eigenvector is needed.

Let Q be a common positive integer denominator of all Gaussian-rational
z_yij=U_yi*conj(U_yj)*Gamma_ji, obtained from products of input denominators.
Its bit size is polynomial in the explicit input and N, including division
by the nonzero rational rho. The scaled DP entries E_r=Q^r D_r are Gaussian
integers of magnitude at most (r!)^2 Q^r, since |z_yij|<=1. Their bit size is
O(r(log Q+log r)). Define P_r=(s-r)!*sum_A E_r(A,A), a nonnegative REAL
integer by the prefix probability proof. Then p_r=P_r/(s!*Q^r), and
sum_y P_(r+1)(y)=Q*P_r. Positive-prefix conditional CDFs have denominator
Q*P_r with polynomial BIT size, however small the prefix probability.
No runtime scales with its reciprocal.

Use b fixed fair bits at each categorical call. Floor each cumulative
probability times2^b (including exact endpoints0,1), and select its interval.
Zero probabilities have equal adjacent endpoints and remain impossible.
For M categories the single-step TV error is at most M*2^-b by telescoping
CDF differences. At most N Bernoulli inclusion and N spatial draws are
used. Taking2^b>=16*N*max(m,2)/epsilon pays at most epsilon/8 total via
sequential coupling; choose the integer b by binary comparisons, not a
real logarithm oracle. This slight constant repair covers N=m=1.

For ideal inclusion S, E[2^|S|]=(1+rho)^N<=exp(R). Choose the integer
K=min(N,ceil(8R)+2*ceil(log2(4/epsilon))). Thus Pr(|S|>K)<=epsilon/4
(in fact the displayed choice is more conservative). The tail branch
returns a fixed legal N-photon occupation. No rejection or separate ABORT
event is needed; tail and finite coins contribute less than epsilon TV.
For retained s<=K,4^s<=exp(O(R))*poly(1/epsilon). All exact arithmetic,
validation, certificate extraction, input/output costs, and random coins
therefore fit exp(O(R))*poly(full input bits,N,m,1/epsilon). Because
R<=N(1-lambda_minG)+1, the same clock holds for the exact spectral defect.
This is polynomial for defect O(log input length), not a claim for all
constant-noise devices. No claim of polylog(1/epsilon) dependence.

A separate demand that truncation ABORT probability be at most eta would
require K=O(R+log1/eta), hence generally polynomial1/eta overhead. Do NOT
assert the selection note's stronger polylog1/eta all-branch clock. The
fixed legal-output TV contract above has no separate failure parameter.

This derivation awaits the stable independent proof and paid disposition
before changing the row to Closed. No production sampler was implemented.

## Final scoped disposition, 13 November 2026

CLOSED WRITTEN: the promised explicit rational isometry and product-pure
Gram admit the always-legal full-occupation TV sampler proved above, with
worst-branch exp(O(N(1-lambda_minG))))*poly(inputbits,m,N,1/epsilon).
Independent full proof: audits/reviews/2026-11-13-gram-defect-prefix.md (219LF) was fully
parent-read, and its derivation independently checked in the parent proof.
The source-scope review gram-defect-literature.md (130LF) was fully read;
actual Moylett3/5, Renema2017/2018 model/results, heterogeneous III, and
Senellart main/S9 scope text were parent checked. This is a direct extension
of established positive-mixture methods, not a new mixture principle or a
literature-wide novelty claim. The five inspected sources do not themselves
state this complete arbitrary-Gram endpoint; that is a scoped observation.

Exact controls retain4 cases/40 occupation probabilities plus prefix
normalization. They test algebra only and do not prove the all-N clock.
The analytical magnitude-only falsifier changes an all-in-one-output
probability by49/531441; the tested P111 also distinguishes the phase.
The written algorithm has no implementation, practical benchmark, human
or formal proof certificate, quantum advantage, hardness, general noisy-
photonics, mixed/correlated internal input, repeated input or loss extension.
The parameter is sufficient, not necessary: one identical pair can force
lambda_min=0 even though the rest are distinguishable and easy.

Paid reports contribute NO mathematical evidence in this pass. Claude25779
terminated max_tokens with EMPTY response, reaped exit1, estimate0.988120USD.
OpenAI29879 terminated APIError with EMPTY response, reaped exit1, charge
UNKNOWN. Neither was retried. Local initial import-path failure made no API
request. Owner now reports OpenAI exhausted and Anthropic20.59remaining;
no more paid OpenAI calls. These balances are separate from runner estimates.
Expected frozen cumulative known estimates311.641198/239priced, Anthropic
173.521118/OpenAI138.120080, withEIGHTUNKNOWN bills excluded. Freeze only
stable new material once from community_recovery_round.

Next scientific action: independent high-upside selection, not another
Gram/noise variant. LWE/Hubbard/rawhomology screen has no constructive
operation yet; hiddenClifford cubic-learning suggestion exactly repeats
the parked HIDDEN_CUBIC_PHASE_LEARNING.md and the six-copy processor
falsifier, so it is not reopened. Next paid research must target an actual
new operation that can change a full algorithm; do not buy repeated
confirmations or infer a survivor from an empty/failed call.
