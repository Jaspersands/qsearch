# What The Current Binary Tree Certificate Can And Cannot Establish

Status: LOCAL UNREVIEWED deduction using established binary channel algebra.
This is not a new general channel-duality theorem, a finite-graph Gibbs sampler,
an independently reviewed proof, or a quantum advantage result.

## Decision

Stop using parameter scans of the current vanishing-tree-error BPQM certificate
to search for a crossing of the corresponding free-boundary reconstruction
threshold. Its success condition is exactly the opposite side of that threshold.
Keep the decoder result, but remove this proposed justification for a glassy
advantage. Global decoders, code-aware affine filtering and outer erasure recovery
not requiring vanishing local tree error are NOT ruled out.

At the existing binary (clause arity k=3, spin degree D=6), c=tanh(beta)=13/20
point, exact directed density evolution proves tree nonreconstruction. The earlier
affine-cluster small-step certificate remains valid; small steps alone did not
prove slow mixing. The next constructive question must concern a mechanism
beyond this local success criterion, not another scan of nearby parameters.

## Native Model And Message Meaning

The native Gibbs weight is proportional to

    product_a [1 + c J_a product_{i in a} sigma_i],

with sigma_i,J_a in {-1,+1}, no external field, k spins per clause and D clauses
per spin. This note treats its independent computation TREE with free Gibbs
boundary law, not a finite graph with cycles. Signs on a tree can be gauged away.
Reconstruction reveals the distant boundary drawn from that Gibbs law and asks
whether it informs the root. It does not condition on a worst-case boundary.

A canonical binary memoryless symmetric (BMS) channel is a flagged mixture of
binary symmetric channels: flag r in [0,1], crossover (1-r)/2. Its flag law is
independent of the input. r is posterior magnetization magnitude, not the signed
planted magnetization. A flagged symmetric pure-state channel (PSC) instead uses
r as the magnitude of its two-state overlap. These use the SAME number with
OPPOSITE information meanings. r=1 is perfect BMS observation but useless PSC;
r=0 is useless BMS but perfectly distinguishable PSC.

For flagged parameters a,b there are two numerical operations:

    product: r = a b;
    parallel: (p+,r+) = ((1+ab)/2, (a+b)/(1+ab)),
              (p-,r-) = ((1-ab)/2, |a-b|/(1-ab)).

The zero-probability minus branch at a=b=1 is omitted. Product is BMS noisy XOR
but PSC same-bit combination. Parallel is BMS independent same-bit observations
but PSC parity combination, with orthogonal heralds. For the latter, negative
odd-sector overlap is a known state-pair phase convention. This magnitude
description is NOT permission to erase a phase from a coherent implementation.
The independent density-matrix tests retain the signed branch before squaring.

These identities belong to known channel duality; see
[Renes, Duality of channels and codes](https://arxiv.org/abs/1701.05583).

## Exact Intertwining

Let A(W) parallel-combine D-1 independent messages with law W. Let B(W)
product-combine k-1 independent W messages and the physical constant c.
The present binary BPQM extrinsic recursion is

    U_0 = point(c),       U_(t+1) = B(A(U_t)).

The classical free-boundary reconstruction recursion, starting with perfectly
revealed boundary spins, is

    V_0 = point(1),       V_(t+1) = A(B(V_t)).

Why this is the native reconstruction process: child messages combine through a
parity clause as an XOR channel of reliability c times their reliabilities.
Distinct branches then provide conditionally independent observations of the
root. Marginalizing the boundary over the free Gibbs law supplies the BMS flag
weights, including both relative signs. This is not the ferromagnetic all-plus
recursion. Direct enumeration of a finite factor tree checks this identification.

Since B(point(1))=point(c), induction gives the exact distributional identities

    U_t = B(V_t),         V_(t+1) = A(U_t).

Let F_t=E[U_t] and q_t=E[V_t^2]. For independent parallel BMS observations,

    E[r_parallel^2] = (a^2+b^2-2a^2b^2)/(1-a^2b^2) <= a^2+b^2.

The inequality follows after subtracting the left side: the numerator is
a^2 b^2 (2-a^2-b^2), which is nonnegative. At ab=1 the channel is perfect and
the inequality holds directly. Iterating and averaging over independent flags,

    q_(t+1) <= (D-1) E[U_t^2] <= (D-1) F_t,
    F_t = c (E[V_t])^(k-1) <= c q_t^((k-1)/2).

Consequently F_t -> 0 IF AND ONLY IF q_t -> 0. There is no approximation,
population-dynamics assumption or sharp-threshold assumption in this statement.
For uniform binary input the PSC Helstrom error is
E[(1-sqrt(1-U_t^2))/2], bounded between E[U_t^2]/4 and E[U_t^2]/2.
Thus its vanishing is equivalent to F_t -> 0 as well. Classical reconstruction
advantage E[V_t]/2 vanishes iff q_t -> 0. Replacing D-1 by D at the root does
not change vanishing: the same parallel moment bound applies.

This concerns this exact initialized local recursion. It does not equate the
performance of every classical and quantum block decoder or every Gibbs sampler.

## Exact Certificate At The Existing Point

The code uses a rational grid of size 128 and exactly normalized dyadic masses
with 96 bits. At every operation it rounds r UP, floors each output mass, and
puts all discarded mass at r=1. This upgrades the BMS observation channel and
degrades the PSC channel. Each step has a physical stochastic degradation
witness: reduce reliability within a flag, or replace a perfect observation by
the discarded flagged channels. Both combining operations preserve channel
degradation order. Second moments of BMS posterior magnetization are monotone
under this order by conditional Jensen. The classical q values are UPPER bounds.

The existing frontier module used these same directed numerical operations.
The new module replays ALL twelve saved quantum mean-overlap bounds exactly,
not just their displayed decimal approximations. `reference_frontier.json`
records the resident source and artifact hashes checked when extracting them.
The laws at finite grid are bounds; the intertwining theorem applies to the
unrounded process, and also algebraically to the two identically rounded maps.

An independent moment estimate gives, with a=(D-1)c^2,

    q_(t+1) <= a q_t^(k-1).

For (k,D,c)=(3,6,13/20), a=169/80. The rounded upper bound first enters the
sufficient contraction basin at t=8. At t=12 it satisfies

    q_12 < 9/200,       (169/80)(9/200)=1521/16000 < 1/10.

Hence the ORIGINAL tree recursion obeys for all integers s>=0

    q_(12+s) <= (80/169) (1/10)^(2^s).

This is an exact rational certificate plus an analytic induction, not an
extrapolation of rounded iteration below its numerical floor. It proves no
finite-block error rate for a quantum decoder and no finite-graph mixing rate.

For context only, [Zhou et al., Appendix D](https://arxiv.org/html/2609.40345v1#A4)
defines a planted reconstruction recursion and estimates the (3,6) regular
threshold as beta_dyn=0.920(1). Our beta=atanh(.65) is approximately .7753.
That numerical threshold is not used as proof. Their large-k Erdos-Renyi
shattering result must not be imported to this fixed regular ensemble.

## Adversarial Countercontrol: Worst Boundaries Survive

In the ferromagnetic gauge, identical child magnetization m at an all-plus
boundary updates as

    T(m)=tanh((D-1) atanh(c m^(k-1))).

Using rational powers rather than transcendental numerics, the code verifies
T(99/100)>99/100 for c=13/20,k=3,D=6. T is increasing and T(1)<=1, so the
iteration from m=1 remains >=99/100 at every depth. Thus typical-boundary
nonreconstruction here coexists with strong worst-boundary influence.
This blocks an immediate inference of uniqueness or strong spatial mixing.
It is not a finite-graph slow-mixing proof either.

## What Was Tried To Falsify The Argument

- Derive the classical mixture from Bayes' rule, rather than reusing PSC code.
- Derive the quantum mixture from explicit parity-conditioned density matrices;
  include perfect/zero channels and negative odd-sector overlap.
- Enumerate a native finite parity-factor tree independently of either combiner.
- Test directed rounding with all stop-loss thresholds on a finer grid and
  keep exact mass normalization. Finite tests support the implementation; the
  physical degradation construction above supplies the general argument.
- Run the AB and BA streams independently, for multiple degrees and both bound
  directions. Replaying one stream alone would not test the index shift.
- Distinguish E[r], E[r^2] and planted E[m]. An erasure mixture and a BSC can have
  equal E[r] but different E[r^2]. The Nishimori identity is E[m]=E[m^2],
  not E[|m|]=E[m^2].
- Keep the explicit worst-boundary counterexample, which defeats the tempting
  but unjustified conclusion that the finite native Gibbs problem is solved.

Remaining failure modes: the imported tree-to-block decoder theorem could have
separate issues; nonbinary/signed phase families need their own channel algebra;
correlated branches, cycles, fields, adaptive reuse or different decoders can
invalidate these recursions. None is silently included. No second reviewer was
used; the authorized independent Rees review is unrelated to this local proof.

## Next Constructive Test

Examine a genuinely global code-aware affine-filter decoder whose success is
rank recovery from partially informative outcomes, not F_t -> 0. First compare
against existing repository parity-block USD and its classical dequantization
before building anything. [Mandal et al.](https://arxiv.org/abs/2606.07852)
already supply affine-filter measurement optimization and local-code decoding;
implementing that paper alone is not a new algorithm.

The decisive target is a charged end-to-end quantum block-success guarantee
outside both this local tree region and the matched positive classical
filter/Prange sampler. Prove the exact classical simulation where possible;
otherwise exhibit the precise nonpositive or coherent step it cannot reproduce.
An LP score, finite decoding success or better local rank yield is insufficient.
Stop or pivot if the same output law has an efficient positive decomposition.
