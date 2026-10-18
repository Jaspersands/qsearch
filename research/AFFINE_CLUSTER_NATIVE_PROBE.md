# Strong Classical Tests of the BPQM Gibbs Hypothesis

2026-10-16. Local identities REVIEW PENDING; standard sampling/contraction
mechanisms, not novel algorithms. No quantum advantage or general classical
mixing/hardness theorem is established.

## Question, Source and Costs

The [BPQM frontier](BPQM_GIBBS_FRONTIER.md) crosses a product-USD/Prange rank
ceiling. That is insufficient evidence for quantum advantage. The immediate
question is whether stronger, legally available classical methods remove the
apparent sampling opportunity on the SAME public input ensemble.

`affine_cluster_native_probe.py` constructs the actual binary (3,6) socket
ensemble: M=2n clause vertices with3 sockets each, n spin vertices with6 sockets
each, and a uniformly shuffled socket matching. Repeated endpoints XOR modulo
two, and every clause sign is drawn independently. Raw degrees and all parallel
cancellations are retained. There is NO rejection for rank, girth, signs or
observed success. Seeds give deterministic replays, not IID confidence claims.
This is not a hand-designed circulant ensemble or the independent-row ER model.

All experiments use c=tanh(beta)=13/20. Exact finite transition controls use
two unfiltered four-spin/eight-clause instances. Larger seeded trajectories
use16,32,64 spins, two graphs each, zero/all-one starts,512 updates and128
discarded-but-charged warmup updates. No stationary oracle is used there.
The methods' work counts differ; an affine solve is not one heat-bath proposal.

The quantum route's asymptotic upside remains conditional polynomial Gibbs
sampling through the known LDPC decoder. The present goal is to FALSIFY a
separation before implementing more quantum machinery. Its >10^12-output
extrinsic tree is not an executed decoder on these finite graphs.

## Exact Nullspace Instrument

Given current x, retain its satisfied constraints with probability
p=2c/(1+c), then uniformly sample y from their affine solution space. Since
x satisfies every selected row,

    y = x XOR z,          z uniform in ker(B_S).          (1)

Consequently, with r=rank(B_S),

    Pr(y=x | S) = 2^(r-n).                              (2)

For a Walsh character chi_a(x)=(-1)^(a.x),

    E[chi_a(y) | S,x] = chi_a(x) * 1[a in rowspace(B_S)]. (3)

A coordinate v is fixed exactly when e_v belongs to that row space. For a
REDUCED row basis this is equivalent to the presence of its unit row. Thus

    E[HammingDistance(x,y) | S,x]
        = (n - number_of_fixed_coordinate_characters)/2. (4)

The old sampler now optionally returns these exact instrument statistics from
its EXISTING FLINT solve, without another elimination or another random draw.
The RREF structure/rank are validated. Current x being a solution is an
explicit precondition, automatically true for the selected satisfied rows.

Countercontrol: a16-variable equality chain has rank15 but nullspace
{0,111...111}. A uniform affine update holds with probability1/2 and has
expected Hamming jump8, NOT1/2. It resets every individual spin character
while retaining the all-spin parity. Neither nullity nor a large Hamming jump
alone certifies thermal mixing. This is a control, not a candidate problem.

## Exact Finite Spectral and TV Controls

Let pi be the actual Gibbs law. From (3), a character's Dirichlet energy is

    <chi_a,(I-K)chi_a>_pi
        = 1 - E_(X~pi,S|X) 1[a in rowspace(B_S)].         (5)

Its variance is 1-(E_pi chi_a)^2. Dividing (5) by that variance gives an
UPPER bound on the spectral gap by the variational principle. A small quotient
can witness a slow mode; a large quotient does NOT certify rapid mixing.
Trajectory averages without stationary initialization do not certify (5).
Tests verify (5) using independently enumerated transition matrices.

For the four-spin controls, all Gibbs probabilities, kernel entries and powers
K,K^2,K^4,K^8,K^16 are exact Fractions. The maximum row TV distance to pi is
therefore a genuine worst-start finite-instance bound. After16 updates it is
about0.01102 for seed29 and0.10586 for seed71. These are not asymptotic bounds
for the graph ensemble. No eigenvalue computed in floating point is used as a
mixing certificate; a dense spectrum is an independent small-instance test of
the Rayleigh-bound direction only.

Related [Swendsen-Wang/heat-bath comparison work](https://arxiv.org/abs/1105.3665)
concerns Potts models under its own assumptions. It motivates operator-level
checks, not an automatic mixing theorem for signed three-body XOR factors.

## Try Harder Before Interpreting a Slow Trace

The32-spin seed29 graph showed different short-run scores from two starts.
The follow-up was SELECTED AFTER that diagnostic, not represented as an
unbiased ensemble estimate. Two8192-update cluster replays discard4096 updates
but charge all work. Their mean signed clause scores move from about46.14
and39.93 in the short runs to45.50 and44.58. The initial discrepancy shrinks;
it does not prove exponential classical slowdown.

A stronger replica-exchange baseline uses exact rational transitions. For
r(c)=(1+c)/(1-c), a spin with d incident clauses, s currently satisfied, flips
under heat bath with probability

    r(c)^(d-2s) / (1+r(c)^(d-2s)).                      (6)

For replica scores T_i,T_j, exchanging configurations is accepted with

    min(1, (r(c_i)/r(c_j))^((T_j-T_i)/2)).              (7)

The score difference is even. Tests verify single-spin and swap detailed
balance against the actual Gibbs weights, including the acceptance sign.
Random-order sweeps and adjacent swaps preserve the product stationary law,
but their composition is not claimed reversible or rapidly mixing.

The targeted replay uses ladder c=(0,1/5,2/5,11/20,13/20),1024 sweeps and256
discarded-but-charged sweeps. Each run pays163,840 spin proposals and4096 swap
proposals. It is a finite fixed ladder, not an optimized asymptotic algorithm.
No claim follows from matching average energy or from nonzero swap acceptance.

## A More Decisive Classical Reference

`xor_factor_reference.py` supplies CAPPED exact integer factor elimination
for this public XOR Hamiltonian. It uses NetworkX's min-fill tree decomposition,
not an optimal-width oracle. For c=a/b, each clause factor is b+a when satisfied
and b-a otherwise. These integer factors differ from exp(beta*T) only by a
configuration-independent multiplier, so their normalized law is exactly Gibbs.

For variable v, multiply its bucket factors to F_v(v,later), sum over v to
form a message, and retain F_v. Eliminate every variable. Backward sampling
uses the two positive conditional entries

    Pr(x_v=1 | later) = F_v(1,later)/(F_v(0,later)+F_v(1,later)).

Messages telescope, giving the product-of-factors law divided by the exact
integer partition sum. Tests compare EVERY output-word probability with an
independent full Gibbs sum on small actual-source instances. Free spins,
constant/frustrated/duplicate factors and huge integer coefficients are kept.
No floating contraction, truncation, hidden partition oracle or MCMC mixing
assumption is used. Uniform random integer draws are an explicit sampling
assumption; seeded tests are replays, not randomness certificates.

The targeted32-spin graph contracts with largest bucket19 variables, peak
single-factor size524,288 entries and2,544,101 cumulative allocated factor/
message entries. These are entries, NOT peak memory bytes. Fresh sampling
then needs32 uniform-integer calls, with a conservative12,764 expected uniform
bit upper bound for rejection-based draws. Preprocessing and large integer
arithmetic are not free. The method is exponential in elimination width, not
a polynomial algorithm for arbitrary graphs. A cap failure returns UNKNOWN,
never a hardness conclusion. The reported heuristic width is an upper bound,
not a lower bound on every classical contraction order.

Keeping spin0 last gives its EXACT parity mean:

    E_pi[(-1)^x0] = -0.5507663992648691...                (8)

The four reported empirical means are approximately:

| Trace | Empirical spin0 parity mean |
| --- | --- |
| Long cluster, zero start | -0.75684 |
| Long cluster, all-one start | -0.49170 |
| Tempering, zero start | -0.75521 |
| Tempering, all-one start | -0.52344 |

The first cluster and tempering traces agree closely WITH EACH OTHER while
both disagree with the exact reference. Agreement between methods, like energy
agreement, is insufficient. These are autocorrelated empirical means, not
proved biases of the terminal output distribution or TV/mixing certificates.
Conversely, an exact classical sampling algorithm exists for THIS finite
graph within the stated contraction cost. That rules out presenting it as a
finite demonstration of sampling beyond classical reach, but proves no
asymptotic dequantization of BPQM.

## Decision and Remaining Falsifiers

The BPQM tree certificate survives, but a classical separation is STILL
UNESTABLISHED. No graph used here is presented as a quantum success. Do not
convert short-run sticking, differing energies or factor-cap failures into
classical hardness. Do not start another parameter sweep by inertia.

Next high-value work is finite-block, phase-correct quantum decoder/reduction
composition or a genuinely structural classical mixing argument, with stronger
classical contractions/tempering retained. Any novel proposed quantum change
must beat these baselines on the same source and measured task. The quantum
mechanism itself and standard classical methods are prior art; tests are not
novelty evidence. No new accepted candidate or active negative is registered.

Run `python theorems/affine_cluster_native_probe.py --write`. The source-bound
artifact records full input masks/signs, work, exact controls and diagnostic
caveats. Production CLI/registry wiring remains optional Gemini work, not a
reason to promote an advantage or regenerate adjacent barrier modules.
