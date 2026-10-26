# Native Inverse-Trace Search As A Classical Sampling Problem

Status: conditional classical attack reduction, LOCAL DERIVATION REVIEW-PENDING.
Character orthogonality and the MDS weight enumerator are known mathematics.
This is not a new sampler or an established dequantization. The additional
small-block result below is a WORST-START MIXING LOWER BOUND, not a
first-witness hitting bound from an unconditioned uniform start.

## Question And Native Input

Can a classical algorithm find a word x with Hx=0 and
Tr(inv0(x_i))=b_i for EVERY i, for the SAME explicit input as
BALANCED_CODEWORD_FILTER.md? Work over the public F_(2^n), with distinct
public alpha_i, H[j,i]=alpha_i^j, 0<=j<K, and C=ker H.
The input has polynomial size when N=n^2, K=floor(N/8).
No hidden oracle, source samples, point counter, decoder, supplied witness,
or target-dependent advice is needed to EVALUATE the target below.

Classical access to the Fourier source did not settle this question.
The direct positive target below avoids needing to simulate coherent erasure.
It converts a proved sampling guarantee into success on the original search
problem, not merely a high optimization score.

## Uniform Fiber Counts, Including Arbitrary Syndromes

Put q=2^n. For any b in F_2^N and s in F_q^K let

    M(b,s) = #{x: Hx=s, Tr(inv0(x_i))=b_i for all i},
    M0 = q^(N-K) / 2^N.

Each predicate is balanced, including inv0(0)=0. If
B_b(u)=sum_{Tr(inv0(x))=b} (-1)^Tr(ux), then B_b(0)=q/2.
Let beta bound |2 B_b(u)/q| uniformly for u!=0 and both targets.
Character orthogonality gives

    M(b,s)/M0 = 1 + sum_{lambda != 0}
        (-1)^Tr(lambda dot s) product_i [2 B_b_i((H^T lambda)_i)/q].

Thus |M(b,s)/M0-1| <= sum_{d in RS[N,K], d!=0} beta^wt(d).
This is a worst-case bound for EVERY target and syndrome, not a random-target
average. It remains valid after fixing some coordinates, provided the
remaining length m exceeds K: restrict H to its remaining distinct columns,
use their induced syndrome, and replace N by m.

For an MDS evaluation code the sum is exactly

    E = sum_{t=0}^{K-1} binom(N,t) (1-beta)^t beta^(N-t) (q^(K-t)-1).

Proof: expand beta^wt(d) as product_i[beta+(1-beta)1_{d_i=0}]
and interchange sums. Any t<K selected zeros leave q^(K-t)-1 nonzero
polynomials; t>=K leave none. This positive expression avoids cancellations.
It has the two sufficient upper bounds

    E <= (q^K-1) beta^(N-K+1),
    E <= q^K [beta+(1-beta)/q]^N.

Use their minimum. The second bound retains the MDS structure lost in the
minimum-distance union bound. For inverse trace,

    beta <= min(1, (1+2 ceil(sqrt(q)))/q).

The +1 is essential because the inverse is extended at zero. As n grows
with N=n^2, the closed bound vanishes at every fixed K/N<1/2.
In particular, every target has solutions in the proposed K/N=1/8 regime.
This is a counting/existence conclusion, NOT an efficient witness algorithm.
It neither supplies exact conditional counts nor stays small when arbitrary
pinning leaves too few coordinates; do not invoke free counting-to-search.

## A Positive Target With Constant Native Success

Let d_b(x) be the number of violated trace constraints. For x in C define

    pi_M(x) = M^(-d_b(x)) / Z,   M = 2^ceil(log2 N) >= N.

This has strictly positive weights. Let eta be either sufficient fiber bound
above. Summing over the 2^N possible output patterns gives

    M0(1-eta)(1+1/M)^N <= Z <= M0(1+eta)(1+1/M)^N,
    pi_M[d_b=0] >= max(0,(1-eta)/(1+eta)) (M/(M+1))^N.

For eta<=1/4 this is greater than 1/5, since (1+1/M)^N<=e<3.
Any sampler within total variation <=1/10 of pi_M consequently returns a
native witness with probability greater than 1/10. Its distribution is on
C union {ABORT}, while pi_M gives ABORT zero mass: clock/precision failures
are included in the TV budget, not conditioned away. Always verify Hx=0 and
every original trace constraint before accepting an output.

The n17/n31/n61 artifacts give exact outward rational lower bounds using
the closed MDS bound. They are mathematical budgets, NOT executed native
sampler runs. They are valid for all targets, unlike testing one selected b.

The normalizer is not needed for local weight ratios. The integer equivalent
weight M^(N-d_b(x)) has O(N log N) bits. Both predicate evaluation and the
integer arithmetic are polynomial in the explicit input size. Efficient
evaluation, high-dimensional solution density, and constant stationary
success do not establish a polynomial hitting time or mixing time.

## Costed Move And Exact Finite Control

Choose K public pivot columns. Each nonpivot field coordinate has a native
codeword direction supported on itself and the pivots. The existing
support_word function constructs it by barycentric weights, normalized to
one at the free position. Expand those N-K field directions into
n(N-K) binary directions using the PUBLIC field basis. This is a bijective
systematic parametrization of C, and changing a free bit preserves Hx=0.

For a uniformly chosen k-bit block, enumerate its 2^k settings and sample
with weights M^(N-d_b(x)). The reference checks every row and exact detailed
balance, including self-loops. Because all weights are positive, every
single-bit neighbor has positive transition probability even for k>1;
the finite chain is irreducible and aperiodic.

These are k BITS, not k field elements. A k-field-element block costs
q^k=2^(nk); calling it a constant-size polynomial update is incorrect.
A bit-block proposal changes at most K+k field positions (and no more than
N). Full recomputation costs O(2^k N) field operations, or update only the
affected positions; count inversions and bit costs too. An integer categorical
draw costs O(N log N + k) random bits in expectation via standard rejection
from a power-of-two envelope. A fixed retry cap introduces an explicit ABORT
that must be charged. No free real-number categorical sampler is assumed.

The transition reference enumerates at most64 states. The independent fiber
reference enumerates at most65536 field words, and checks EVERY target and
syndrome for those controls. Neither reference is a scalable native sampler.

## Decisive Next Experiment For Gemini

The derivation below rules out a polynomial WORST-INITIAL-STATE TV guarantee
for fixed small binary blocks in the native regime. Do not pursue that
guarantee for this kernel. A uniform-start first-hitting pilot remains a
different, open question: sticky solutions can help witness retention.

Build only the matrix-free native bit-block sampler and verifier, reusing
support_word and the public field implementation. No new general framework.

1. Freeze points, field moduli, targets, basis choice, seeds and work limits
   BEFORE running. Use independently generated target bits, not only the
   existing popcount targets. Keep zero-target and existing verified n17/n31
   inputs as controls, never as random-hardness evidence.
2. Start from an unconditioned uniform codeword (uniform systematic bits),
   never a known solution or an accepted-flat witness. Compare k=1,2,3 with
   identical charged candidate-evaluation budgets. Preserve every failure.
3. Compare a matched systematic root/Prange proposal: generate each free
   coordinate uniformly from its allowed roots by inverse-mapping a uniform
   trace hyperplane, then solve the K pivots and test all constraints. Also
   retain the existing accepted-flat baseline where applicable.
4. Record first FULL-native-witness hitting time, total field inversions,
   candidate evaluations, restarts, rejection/ABORT counts and censored runs.
   Also record defect histories and mobility. Do not call an improved score
   success or call first hitting time a TV mixing measurement.
5. Basis changes and parallel tempering are legitimate subsequent attacks,
   but must keep the same native target and charge setup and swap/update work.
   A failure of the original basis is not a failure of all MCMC.
6. Stop a bounded pilot that exhibits freezing without full witnesses. Before
   expanding seed counts, identify a justified move or a mixing/hitting-time
   argument. Polynomial-looking finite scaling is not an asymptotic theorem.

This is an implementation specification, not authorization to create an
automation, run in the background, alter registries/UI, or commit/push.

## Small Binary Blocks: A Worst-Start Mixing Obstruction

This is a local derivation from standard character bounds, pending independent
review. It applies uniformly to all target vectors and all distinct public
evaluation points. It does not require a random-code assumption.

Put f(x)=Tr(inv0(x)), chi(x)=(-1)^Tr(x), r=1/M, and
A={x in C: f(x_i)=b_i for every i}. Let eta be the native fiber-error bound
above, and assume eta<1. Then A is nonempty, and pi_M conditioned on A is
uniform on A. We first bound a FIXED codeword displacement v, not an adaptive
one chosen by examining x.

### Two-Pole Character Accounting

For a nonzero scalar v define

    a_v = sum_x chi(inv0(x)+inv0(x+v)),
    d_v(u) = sum_x chi(inv0(x)+inv0(x+v)+u*x).

On x not in {0,v}, the rational function 1/x+1/(x+v) has two distinct simple
poles. Its Artin-Schreier curve has genus one, with one point above each
pole and TWO points above infinity. If S is the sum excluding 0,v, its
projective point count is q+2+S, so |S+1|<=2 sqrt(q). Restoring the two
totalized endpoints adds 2 chi(1/v). Consequently

    |a_v| <= 2 sqrt(q)+3.

For u!=0, adding u*x introduces a third simple pole at infinity. The genus
is two; the point count is q+1+S_u and |S_u|<=4 sqrt(q). The endpoint
correction is chi(1/v)*(1+chi(u*v)), of magnitude at most two. Thus

    |d_v(u)| <= 4 sqrt(q)+2,   u!=0.

Simple poles preclude the degenerate form h^2+h+c, including over the
algebraic closure. These are genus/Weil bounds, not an independence heuristic.
The standard result is stated in Carmon, Theorem3.1 and equation3.6,
[characteristic-two character sums](https://arxiv.org/abs/1409.3694).
All zero-extension and infinity corrections are explicit above.

Let L=1+2 ceil(sqrt(q)) and delta=min(1,(3+2 ceil(sqrt(q)))/q).
For either target b define

    h_v,b(x) = 1_{f(x)=b} [r+(1-r)1_{f(x+v)=b}].

Because f and its translate are balanced, for v!=0 its mean is

    mu_v = [1+r+(1-r)*a_v/q]/4,
    mu_min = [1+r-(1-r)*delta]/4 <= mu_v,
    2*mu_v <= theta = [1+r+(1-r)*delta]/2 <= 1.

At nonzero frequency the intersection of the two target sets has Fourier
magnitude at most (2L+(4 ceil(sqrt(q))+2))/4=L. Combining it with the single
target indicator bounds h's Fourier magnitude by (1-r/2)L. Therefore a
uniform normalized nonzero Fourier bound is

    beta_pair = min(1, (1-r/2)L/(q*mu_min)).

For v=0, h is just a single target indicator with mean1/2 and normalized
bound min(1,L/q), which is no larger than beta_pair. Notice mu_min>0 even
when delta=1, because r>0. No zero denominator is discarded.

### From Scalar Correlations To Native Displacements

The same MDS character expansion works for arbitrary nonnegative local
functions with positive means and the above normalized Fourier bound. Let
eta_pair be mds_character_bound(n,N,K,beta_pair). Applying the expansion
to product_i h_v_i,b_i and dividing by the LOWER bound on |A| gives

    E_{x uniform A} r^d_b(x+v)
      <= (1+eta_pair)/(1-eta) * theta^wt(v)
      <= (1+eta_pair)/(1-eta) * theta^(K+1),   v in C, v!=0.

Here the displacement code C=ker H has minimum distance K+1. The Fourier
enumerator uses C^perp=RS[N,K], whose distance is N-K+1. Confusing these two
distances would give an invalid, much stronger mixing claim.

Consider an exact heat-bath update on x+B for a binary subspace B of C of
dimension at most k. For x in A the denominator includes the self weight1,
so its probability of choosing a given nonzero v in B is at most
r^d_b(x+v). Sum over at most2^k-1 offsets and then average over uniform A:

    E_{pi|A} P(x,A^c) <= E,
    E = min(1, (2^k-1)*(1+eta_pair)/(1-eta)*theta^(K+1)).

Counting also moves to OTHER solutions only enlarges the bound. It is
uniform over B, hence applies to any state-independent random mixture of
these blocks, even in many different public bases. State-dependent block
selection is NOT covered by this argument. Nor are tempering or nonlocal
proposals that do not fit the stated kernel. The bound also holds for a
fixed time-dependent schedule of such pi-stationary updates.

### Worst-Start TV Lower Bound, Not Search Hardness

The fiber bounds give the upper bound

    p = pi(A) <= p_upper
      = min(1, (1+eta)/(1-eta)*(M/(M+1))^N).

Start from mu_0=pi conditioned on A. A stationary path conditioned on its
initial state being in A has probability at most t*E to leave A by time t:
union-bound the t boundary-crossing events, upper-bound each UNCONDITIONAL
stationary probability by Q_pi(A,A^c), and divide by pi(A). This does NOT
assume the chain stays uniform on A after conditioning on non-exit. Thus

    TV(mu_t, pi) >= 1-p_upper-t*E.

Since mu_0 is a mixture of individual starting states, at least one valid
starting state has TV at least this large. For the homogeneous mixture,

    t_mix^worst(1/4) >= ceil(max(0, 3/4-p_upper)/E).

When eta>=1 or the mass bound is vacuous, the implementation returns a
vacuous result, never a claimed positive certificate. All reported bounds
are rounded outward using rational arithmetic; no floating exponential
fit or native chain simulation is involved.

At N=n^2, K=floor(N/8), fixed k (or k=O(log n)), beta_pair=O(q^-1/2), both
MDS errors vanish, and theta=1/2+o(1). The escape bound is 2^(-Omega(K)).
Also p_upper is eventually below3/4: M<2N bounds the ideal mass away from
that threshold. Hence worst-start mixing takes 2^(Omega(n^2)) updates.
This conclusion is already meaningful for the n17/n31/n61 certificates.

For k=3 the current exact rational calculation gives these conservative
worst-start TV1/4 update-count lower bounds (not elapsed times):

| n | N | K | Mean solution escape upper | Worst-start updates, at least |
| --- | --- | --- | --- | --- |
|17|289|36|2^-33|2,695,231,160|
|31|961|120|2^-118|1.20 * 10^35|
|61|3721|465|2^-463|8.42 * 10^138|

The integer update bounds in the artifact use the sharper rational escape
bound, not its displayed power-of-two rounding. The scientific assumptions
and local proof still need independent review.

Crucial limitation: the obstructing starts ARE SOLUTIONS. No lower bound
on first-witness hitting from an unconditioned uniform codeword follows.
Rapidly reaching a sticky solution could be useful for search while failing
to sample the stationary law from every possible start. No classical
hardness, quantum advantage, or failure of all MCMC is established here.
Indeed b=0 has the immediate classical witness x=0, while the SAME
worst-start mixing bound applies. That concrete easy native instance already
refutes interpreting this obstruction as a general search-hardness claim.

### Executable Falsifiers

- Enumerate every nonzero scalar displacement and every Fourier frequency
  in bounded fields; check both Hasse inequalities as squared integers,
  both excluded endpoints, and the weighted mean/Fourier inequalities for
  both targets and several rational temperatures.
- Independently compare the complete native weighted sum with its dual
  Fourier expansion for every displacement and target on a bounded code.
- Retain exact finite transition matrices, detailed balance and explicit
  mean escape from the solution set. An empty solution set yields no escape
  statistic, not a fabricated zero-escape certificate.
- Check vacuous regimes, block-size growth and both code distances. Tests
  must not turn the worst-start bound into a uniform-start hitting claim.

## Attempts To Disprove This Direction

- The derived fixed-small-block worst-start mixing obstruction defeats one
  proposed sampler guarantee. It does not defeat uniform-start first hitting;
  that requires a different proof or the bounded, honestly censored pilot.
- A full-field update can hide exponential work in q. The bit-block protocol
  removes that accounting error, not necessarily the energy barriers.
- Arbitrary pinning changes the code's effective rate. The uniform fiber
  estimate eventually becomes vacuous; approximate global counting cannot
  be treated as a free exact conditional sampler.
- Fast native witnesses would refute hardness for the tested instances.
  A general polynomial sampler/hitting-time proof would dequantize this
  candidate family; it would not invalidate unrelated DQI applications.
- Slow pilots would only falsify the specified kernel/budget, not classical
  solvability. They are not evidence for quantum advantage.
- The codeword-filter quantum construction itself still needs independent
  proof review and a costed coherent decoder. This classical reduction does
  not validate that construction or establish its novelty.

## Literature And Scope

Gil-Fuster et al., [Approximate sampling from decoded quantum interferometry
via Markov chain Monte Carlo methods](https://arxiv.org/abs/2607.28120), use
evaluable DQI output weights and block Gibbs experiments. Their OPI scaling
is empirically exponential, and their optimization results do not establish
all-constraint success on this inverse-trace problem. The present Gibbs
target is chosen to solve the native relation, not to reproduce the exact
DQI output distribution. Existing BALANCED_MPI_PRODUCT_TARGET.md concerns
a different cosine/MPI target; its transfer and freezing results do not
automatically apply here.

Marwaha et al., [On the Complexity of Decoded Quantum Interferometry](https://arxiv.org/abs/2509.14443),
connect DQI and classical coding identities while showing why standard
simulation arguments need care. Source sample/query access alone is not
a claim of an efficient native witness sampler.

Replay: `python -m theorems.inverse_trace_gibbs_target --write`, with
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache in this workspace.

### Validation Availability, 2026-10-22

The workspace is on an iCloud-managed Desktop. The user intends to move it
after downloads finish; do not relocate it or repair cloud/cache settings.
The shared native finite-field backend currently has the macOS dataless
flag, and bounded imports stall on its source read. The negative-result
registry also remains dataless. These are availability limits, not passing
integration tests or a reason to replace the shared backend.

`--skip-native-controls --write` explicitly emits the exact rational budgets
and independent FLINT scalar controls without pretending to execute the
unavailable native-backend replays. `--bounds-only` omits even those scalar
controls. The JSON records both scopes separately. The standalone scalar
reference uses and records its own public field modulus; its basis-independent
identities are not native-input experiments. Once the files are local, rerun
the full standalone workflow and the full connected test set.
