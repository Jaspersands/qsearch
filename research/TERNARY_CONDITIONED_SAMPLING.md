# Stronger Classical Conditional Samplers

2026-10-20. Two known classical mechanisms, with native output-law accounting.
Local reductions and bounds are REVIEW PENDING. No asymptotic dequantization
or quantum advantage is established. These methods improve the comparison,
not the novelty of the project.

Producer: `python theorems/ternary_conditioned_sampling.py --timeout 30 --write`.
Report: `research/classical_baselines/ternary_conditioned_sampling.json` (schema v2).
Tests: `tests/test_ternary_conditioned_sampling.py`.

## Scientific Question

Can the same count-concentration premise used by the quantum route support a
strong classical sampler without expensive prefix-conditioned counting?

Yes at the ORACLE-REDUCTION level: a global count window suffices for random
hash isolation and exact cell solving. This corrects the overly narrow next
step of requiring prefix counters. It does NOT establish polynomial classical
time: finding and proving the unique solution of a randomly hashed instance
is the paid computational bottleneck. We implement that test with actual SAT
calls, not a unit-cost oracle.

Separately, maximal-rank affine conditioning gives an exact rejection sampler
with substantially better acceptance than plain spin rejection. Both operate
on the original sparse affine-exclusion constraints

    y = J + H^T x in {1,2}^N,   x in F3^V.

All original spins, gauge freedom, parallel-socket cancellations, offsets and
empty instances remain. The source is not conditioned on satisfiability.

## Rank-Conditioned Exact Rejection

Let r=rank(H), g=V-r. Choose r independent columns indexed by I. Exact Gaussian
elimination gives H=H_I R, with R_I=I_r. Every affine word is determined by
its selected coordinates:

    y = beta + s R,   beta = J - J_I R.

Here row/column transposes follow the implementation's explicit array layout.
Choose s uniformly from {1,2}^r. The selected constraints are satisfied by
construction. Reject if any other y coordinate is zero. If accepted, solve
H^T x=y-J with the prior exact Gaussian lift and g independent uniform trits.

For EACH fixed original input, every valid native x has exactly one preimage
(s,gauge-coins). Thus the proposal domain has size D=2^r 3^g and, writing Z
for the native solution count,

    p_rank = Z/(2^r 3^g),
    p_spin = Z/3^V,
    p_rank/p_spin = (3/2)^r                 when Z>0.

Acceptance produces EXACT uniform native samples. No solution pool, model
counter, prefix oracle or preferred gauge representative is used. The code
computes batches of proposals and charges the whole batch, including entries
after the first success. It never conditions on solver runtime.

With a fixed T-proposal cap, the unconditional output is

    (1-f) Uniform(S) + f ABSTAIN,   f=(1-p_rank)^T.

For nonempty S its TV distance to Uniform(S) is exactly f. Empty S always
produces ABSTAIN. `power_interval` encloses f with outward dyadic arithmetic;
an enormous exact numerator/denominator is not materialized. Fair independent
coins are an assumption of the distributional theorem; a saved PRNG seed is
only a reproducible test trace.

For uniform original offsets, E p_rank=(2/3)^(N-r), compared with(2/3)^N for
plain spin rejection. This is NOT a bound on E(1/p_rank); unsatisfiable inputs
would make an uncapped rejection loop infinite. Under the same count-
concentration premise as before, it describes the typical acceptance scale.
For full-rank N=2V inputs the rejection exponent is halved. The method is still
exponential there. When N-r=O(log input size) and count concentration holds,
this baseline can instead be polynomial and must be checked before claiming
an advantage in a higher-rate variant.

This is an affine version of the repo's existing linear-erasure projection,
and a standard Gaussian/Prange mechanism, not a new algorithm. Tests match
the two implementations on nonzero targets and exhaust every offset, chart
ordering and gauge coin on bounded degenerate controls.

## Global Count To Sampling Without Prefix Counts

Let S be the ORIGINAL native solution set, |S|=Z, and assume a positive count
window L<=Z<=U. Independently draw every entry of A in F3^(h x V) and b in
F3^h uniformly. Put M=3^h and consider the cell

    S_(A,b) = {x in S: A x=b}.

Keep zero rows, dependent rows and contradictory hash equations. Resampling
only full-rank hashes would change the distribution used in the proof. For
each x, membership has probability1/M; for distinct x,z, simultaneous
membership has probability1/M^2. Therefore, if rho=(U-1)/M<1,

    (1-rho)/M <= Pr[S_(A,b)={x}] <= 1/M,
    Pr[unique cell] >= (L/M)(1-rho).

Conditioning on a unique cell gives a distribution nu obeying the conservative
bound TV(nu,Uniform(S))<=rho/(1-rho). To see this, write each point's isolation
probability as M^-1(1-e_x), with0<=e_x<=rho, and normalize the weights. This
bound is elementary universal hashing, in the tradition of
[Jerrum--Valiant--Vazirani](https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/ConvergeRates/RandomizedAlgs/JerrumValiantVaziraniTCS1986.pdf),
not a novelty claim.

Choose the least h with U/3^h <= epsilon/(1+epsilon). Then the conditional TV
bound is <=epsilon. After K independent hash attempts, return ABSTAIN if none
is unique. The full output bound is

    TV <= rho/(1-rho) + [1-(L/M)(1-rho)]^K,

capped at1. With a constant-factor count window, this uses polynomially many
exact cell solves in1/epsilon and log(1/failure). Those solves can still take
exponential time. They are not supplied by the global count estimate.

The implementation derives L=floor(Zbar/2), U=ceil(2 Zbar), with L at least1,
from Zbar=3^V(2/3)^N. It does NOT read the old exact counts to choose hashes.
Under the earlier Hellinger/count premise, the probability that the continuous
window [Zbar/2,2 Zbar] fails is at most

    min(1, (12+8 sqrt(2)) E_H delta_H).

This follows from the nearest endpoint distance1-1/sqrt(2) in sqrt(Z/Zbar).
The integer window only enlarges the event of success. Thus the same proposed
quantum premise supplies a useful classical hash-size estimate on most inputs.
There remains no finite-size count-window guarantee from that theorem. In
these two finite experiments the independently completed earlier counts
verify the window AFTER sampling, not as sampler advice.

## Actual Cell Solver And Failure Discipline

The original native CNF encoding is bijective. Dense F3 hash equations are
added through ternary SUM chains, not an exponential table over all variables.
Every auxiliary qutrit has exactly one Boolean one-hot encoding, and every
native x has exactly one auxiliary extension. Addition uses nine implications
per gate plus one-hot constraints. Coefficients2 permute the input flags.

PicoSAT is asked for at most two models. One found model is NOT a unique cell:
the iterator must then exhaust, establishing no second native model under the
backend's correctness assumption. Two models reject the cell. Empty cells
are normal failed attempts, not proofs that the original input is UNSAT.
Every model is independently replayed against CNF, original constraints and
the original F3 hash. No propagation limit is used.

These finite cells do not supply independently checked UNSAT proof logs.
The mathematical law assumes exact cell solving. The experiment's outer
30-second watchdog is a separate limitation: runtime can depend on A,b and
the isolated solution. Consequently EVEN A COMPLETED TRACE does not certify
the wall-capped sampler's TV bound. A timeout returns UNKNOWN and no partial
sample; slow cells are never skipped while retaining a sampling claim. Any
bounded-runtime theorem must additionally bound that timeout/failure mass.

Two complete tiny hash-family censuses test the law. For
S={(0,0),(0,1),(0,2),(1,0)} and two hash rows, the isolation counts are
64,64,64,56 out of729 hashes. Conditional TV is3/124, NOT zero. Keeping the
first witness without uniqueness is another biased law. Pairwise hashing
provides the stated approximation bound, not exact uniformity.

## Same-Input Live Results

No native input was regenerated or SAT-filtered. Both methods produced one
verified native sample on each saved input without using a complete pool.

| Input | Rank proposal result | Hash isolation result |
|---|---|---|
| V16,N32,seed711 |215 proposals to first success; ~0.05s |11 cells, ~0.46s |
| V32,N64,seed712 |23,883 proposals to first success; ~0.03s |3 cells, ~2.44s |

These are SINGLE reproducible traces, not runtime fits or representative means.
The expected proposal counts from the independently completed counts are
65536/67 (about978) and1073741824/2523 (about425,581). In particular, the saved
32-spin trace was much luckier than its mean. Matrix preparation and unused
batch proposals are included in the recorded costs.

The fixed rank budget is2^24 proposals. Assuming those complete counts and
independent fair coins, its nonempty-input TV is at most2.94e-39 on V16 and
about7.57e-18 on V32. This guarantee is an output-law calculation, not an
empirical histogram claim. It does not make the growing-instance cost
polynomial. One sample uses polynomial memory, unlike complete pool storage.

Both predetermined hash count windows are verified by the old counts: [49,200]
contains67; [4977,19910] contains10092. The uncapped exact-solver TV upper bounds
at256 hash attempts are about0.03156 and0.06041. The timeout mass is NOT included
in those numbers. Prior SAT enumeration cost is not used inside either new
sampler; its old result is used only for these independent finite certificates.

## Entropy-Rank Hashed-SAT Scaling Campaign (Schema v2)

`entropy_rank_hashed_campaign` evaluates exact native $(3,6)$ socket-ensemble
instances across $V \in \{16, 20, 24, 28, 32\}$ (matching the saved inputs at
$(16, 711)$ and $(32, 712)$ and saving every intermediate input without SAT
filtering or seed selection). For each instance with annealed mean
$\bar{Z} = 3^V (2/3)^{2V} = (4/3)^V$, it tests a deterministic budget of
`cells_per_rank = 4` independent random hashes $(A, b)$ (retaining rank-deficient
and zero rows) at three canonical hash ranks:

1. `entropy_floor`: $h_{\text{floor}} = \lfloor \log_3 \bar{Z} \rfloor$ ($1 \le \bar{Z}/3^h < 3$),
2. `entropy_ceil`: $h_{\text{ceil}} = \lceil \log_3 \bar{Z} \rceil$ ($1/3 < \bar{Z}/3^h \le 1$),
3. `isolation_target`: $h_{\text{iso}}$ chosen from `isolation_shape(U, "1/4")` ($U / 3^{h_{\text{iso}}} \le 1/5$),

and compares hashed-cell costs directly against an unconditioned 1-model SAT
check (`unconditioned_first_witness_control`) on the same instance, while
keeping deterministic cell budgets separate from the per-cell wall-clock
watchdog (`experimental_cell_wall_budget_seconds = 10.0`):

| Instance ($V$, seed) | Unconditioned 1st-Witness SAT | `entropy_floor` ($h$, E/U/M, mean wall) | `entropy_ceil` ($h$, E/U/M, mean wall) | `isolation_target` ($h$, E/U/M, mean wall) | Hashed / Unconditioned Wall Ratio |
|---|---|---|
| $V=16$, seed 711 | $0.00011\text{ s}$ | $h=4$: $1/1/2$, $0.0012\text{ s}$ | $h=5$: $4/0/0$, $0.0010\text{ s}$ | $h=7$: $4/0/0$, $0.0011\text{ s}$ | $8.5\times\text{–}11.1\times$ |
| $V=20$, seed 713 | $0.00032\text{ s}$ | $h=5$: $1/1/2$, $0.0115\text{ s}$ | $h=6$: $2/2/0$, $0.0146\text{ s}$ | $h=8$: $4/0/0$, $0.0152\text{ s}$ | $35.6\times\text{–}47.2\times$ |
| $V=24$, seed 714 | $0.00016\text{ s}$ | $h=6$: $0/3/1$, $0.0242\text{ s}$ | $h=7$: $2/1/1$, $0.0275\text{ s}$ | $h=9$: $4/0/0$, $0.0266\text{ s}$ | $153.1\times\text{–}174.0\times$ |
| $V=28$, seed 715 | $0.00019\text{ s}$ | $h=7$: $2/1/1$, $0.2227\text{ s}$ | $h=8$: $2/2/0$, $0.3650\text{ s}$ | $h=10$: $4/0/0$, $0.6025\text{ s}$ | $1{,}165\times\text{–}3{,}153\times$ |
| $V=32$, seed 712 | $0.00058\text{ s}$ | $h=8$: $2/0/2$, $0.6433\text{ s}$ | $h=9$: $4/0/0$, $1.6768\text{ s}$ | $h=11$: $4/0/0$, $1.2895\text{ s}$ | $1{,}101\times\text{–}2{,}871\times$ |

Here `E/U/M` counts `EMPTY` (exhausted UNSAT proof), `UNIQUE` (1st model plus
exhausted 2nd-model search), and `MULTIPLE` (early stop at 2nd model) cells.
Unconditioned SAT finishes in $< 0.6\text{ ms}$ because $\bar{Z} = (4/3)^V \gg 1$
solutions exist, whereas hashed cell solving near the entropy and isolation
ranks is dominated by exhausting the search tree on `EMPTY` and `UNIQUE` cells
($> 1{,}000\times$ slower than unconditioned SAT by $V=28\text{–}32$). Any cell
hitting the wall budget is recorded as `UNKNOWN_CELL_TIMEOUT` (`unknown_timeout_fraction_exact`)
without salvaging partial witnesses or certifying the capped distribution.

## Full-Weight Coding Connection And Scope

Compute a basis G of ker(H), and s=GJ. Then

    y in {1,2}^N and G y=s

is equivalent to the native task up to exactly3^(V-r) uniform gauge lifts.
This connects to full-weight ternary syndrome decoding. Relevant competitors
include Gaussian elimination, subset-sum/dissection and representations:
[Bricout et al.](https://arxiv.org/html/1903.07464v2) and
[Karpman--Lefevre](https://eprint.iacr.org/2022/128). Their search algorithms
are not automatically uniform samplers; representation multiplicities and
output bias must be audited. The simple rank baseline is not asserted to be
the best classical method from that literature.

Crucially, ker(G)=rowspan(H) is an LDGM code with public generator rows of
weight at most6 on our source. It is NOT a uniform random code. For a uniform
r-dimensional subspace D of F3^N,

    Pr[D has a nonzero word of weight<=6]
      <= sum_(w=1..6) binom(N,w) 2^(w-1) * (3^r-1)/(3^N-1).

This unions over low-weight projective lines. At N64,r32 the bound is about
1.36e-6; our supplied H explicitly exhibits such words. At rate1/2 the bound
vanishes asymptotically. Even if H were hidden, constant-weight enumeration
tests the property in polynomial time, though with a very large finite cost.
Generic dense-code/Wave hardness cannot be imported into this distribution.
This is a distribution mismatch, not a runtime lower bound for either source.

Similarly, [Ivanyos's random linear disequation algorithm](https://arxiv.org/abs/0704.2988)
has a different sample-access promise: sufficiently many nearly uniform
characters excluding a fixed unknown element. Our one prescribed sparse
instance does not supply those additional dense samples. Neither positive
nor negative results transfer merely because both use disequations.

## Decision And Next Falsifier

Keep the conditional quantum route, but discard any finite advantage narrative
based on the old SAT or UniGen timeout. The original16/32 inputs now admit a
low-memory exact conditional classical sampler and a native hash-isolation
implementation, and the entropy-rank campaign quantifies the >1,000x gap between
unconditioned 1st-witness SAT and hashed empty-cell/uniqueness exhaustion at
$V=28\text{–}32$.

The quantum side still needs useful finite-N guarantees and independent review
of the conditional construction. No search-time separation, classical lower
bound, cryptanalytic application or central candidate promotion follows from
this pass.
