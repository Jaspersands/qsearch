# A Constructive BPQM Gibbs-Sampling Frontier

2026-10-16. KNOWN MECHANISM; LOCAL CERTIFICATE DERIVATION REVIEW PENDING.
No novel quantum algorithm, finite-block receiver, classical-hardness theorem,
or Shor-level speedup is claimed. No candidate is admitted automatically.

## Scientific Question and Portfolio Decision

Can an explicit coherent LDPC decoder support natural Gibbs sampling beyond
classical samplers, rather than merely outperform one weak decoder? This
independent route is more constructive than another conditional DCP interface.
It supplies a specified decoder family, public input, rigorous local test and
known sampling reduction. Its largest unresolved issue is the matched classical
sampling frontier and finite-block composition, not a missing oracle.

The repository already has product/block USD and positive affine-erasure
samplers in PARITY_BLOCK_USD_PRANGE.md and LINEAR_ERASURE_PRANGE_DUALITY.md.
Those do not cover all minimum-error quantum message-passing decoders. Do not
call a classical calculation of decoder statistics a simulation of its full
quantum output or a classical Gibbs sampler.

Compared directions: the DCP finder just tested loses coverage and supplies no
new construction; rank-metric DQI already acknowledges that its stated proxy
does not give quantum advantage; general GI/coset work has no efficient joint
receiver. BPQM instead has a concrete literature-backed asymptotic decoder.
This justifies testing it, not assigning a numerical breakthrough probability.

## Problem and Known Mechanism

Input: an explicit binary matrix H drawn from the regular LDPC socket ensemble
with variable degree dv>=3 and check degree dc>dv. Set B=H^T and choose the
clause signs J independently and uniformly. The problem is approximate sampling
in TOTAL VARIATION from

    P(x) proportional to exp(beta * sum_e J_e (-1)^(B_e.x)).

There are M clauses and M*dv/dc spins. Parallel sockets contribute modulo two;
this is not silently identified with the independent-row Erdos-Renyi ensemble.
All input rows, code construction, state preparation and signs are public.
No unknown-secret angle, arbitrary coherent oracle or designed source is free.

[Mandal et al.](https://arxiv.org/abs/2609.05857), Theorem30, give an asymptotic
block-decoding result for random regular LDPC ensembles inside the BPQM tree
success region. [Zhou et al.](https://arxiv.org/abs/2609.40345), Theorem2.4,
relate quantum decoding to Gibbs sampling for uniform random signs. Here the
binary channel overlap is c=tanh(beta); the coherent flip probability is
gamma=(1-sqrt(1-c^2))/2. These source assumptions and asymptotic statements
remain explicit; the code implements neither complete theorem's decoder.

[Piveteau and Renes](https://arxiv.org/abs/2109.08170) distinguish an efficient
message-passing implementation from an exponentially sized global-control
description. Generic angle tables, cloned tree leaves and a dense Helstrom
matrix are not acceptable substitutes for the actual algorithm.

Internal heralds/reliability records must remain COHERENT when synthesizing a
root measurement and its adjoint for sequential use. Reading and discarding
them can strongly disturb a fixed codeword even when they are harmless in its
averaged bit-channel density matrix. A direct two-wire test shows that loss.
The upper/lower degradation maps here are mathematical comparisons, not a
claim that their environments can be irreversibly discarded inside the final
Gibbs circuit. Original coherent BPQM instruments, not this classical density
evolution, must be used in that composition.

## Exact Binary Tree Calculation

Represent a binary pure-state channel by

    |psi_x(c)> = sqrt((1+c)/2)|0> + (-1)^x sqrt((1-c)/2)|1>, 0<=c<=1.

Equality of two input bits compresses the product states to overlap ab. A
parity node has a PUBLIC herald r with

    p+ = (1+ab)/2,   c+ = (a+b)/(1+ab),
    p- = (1-ab)/2,   |c-| = |a-b|/(1-ab).

The zero-probability branch at a=b=1 is omitted, not divided by zero. A CNOT
in the Fourier basis resolves the two orthogonal parity blocks. The tests
reconstruct both conditional density matrices directly, including the SIGN
of the minus-branch overlap. Absolute overlap suffices for discrimination
statistics; a coherent compiler must retain branch/bit phase gauges and its
adjoints. The density calculation does not clear those registers for free.

For independent heralded inputs, the parity output's mean absolute overlap
is E[max(a,b)] <= E[a]+E[b]. Equality multiplies mean overlaps. For a regular
extrinsic computation tree, with F_l its mean overlap,

    F_(l+1) <= A F_l^p,
    A = c*(dc-1)^(dv-1),    p = dv-1 >=2.                 (1)

This elementary binary bound follows from the two combining identities, not
from fitting a curve. If a finite calculation bounds F_L<=f and

    lambda = A*f^(p-1) < 1,

then induction gives for every r>=0

    F_(L+r) <= f*lambda^((p^r-1)/(p-1)).                 (2)

The unrounded original tree therefore has doubly exponential decay. For
binary PSC mixtures the optimal symbol error is at most F/2. This proves a
SUFFICIENT TREE condition only; it is not an implemented large-graph decoder.

## Certified Degradation Instead of Floating Density Evolution

`theorems/bpqm_gibbs_frontier.py` uses overlaps j/G and EXACT integer masses
w_j/2^b. It never rescales a drifting floating distribution to sum to one.
Every combination first verifies its exact total mass.

Two enclosing channels are maintained. Rounding overlap upward makes states
less distinguishable; downward makes them more distinguishable. A binary PSC
with overlap a can be transformed to one with overlap b>=a by a channel whose
environment has overlap a/b (the zero case is handled by continuity). Thus
these directions have a physical information order, not just a numerical one.

Masses are rounded DOWN to dyadic integers. All leftover mass is redirected
to a completely uninformative channel for the upper-error model, and a perfect
channel for the lower-error model. Both are legitimate information comparisons
with their flags retained. Node combination preserves this order. Consequently
the original tree's fidelity and optimal error are enclosed. Integer square
roots give rational endpoints for (1-sqrt(1-c^2))/2. No numerical eigenvalue is
used as a proof certificate; dense physical matrices are independent controls.

Only the degraded upper model can certify convergence via (1). A lower bound
of zero does NOT certify success. Once a sufficient finite bound is obtained,
(2) applies to the original unrounded recursion; no finite precision floor is
extrapolated to zero. This local degradation argument remains review pending.

## Executed Result and Full Resource Warning

Default settings: (dv,dc)=(3,6), G=128, mass precision96 bits.

- c=1/2: sufficient contraction is reached at level4.
- c=13/20: level12 bounds F below0.024 and A*F below0.383, strictly below1.
  Hence the sufficient tree condition holds beyond the product-USD/Prange
  rank ceiling c=dv/dc=1/2.
- c=4/5: no sufficient certificate in24 levels; status is UNKNOWN, not a
  theorem that no decoder works.

The unfolded channel count is U_0=1 and U_(l+1)=1+(dv-1)(dc-1)U_l. At
level12 it is **1,111,111,111,111 distinct original outputs**. A finite
cycle-free neighborhood must contain them, and typical local treeness needs
additional ensemble control. This counts the extrinsic message tree, not a
complete block decoder; a full-degree root or repeated bit tests cost more.
The cheap scalar calculation is NOT a trillion-
qubit quantum execution. There is no free cloning when neighborhoods overlap.

The asymptotic two-stage decoder uses growing depth, gentle sequential
measurements and erasure recovery. An end-to-end proposal must pay code
linear algebra, all neighborhood operations, reliability-register precision,
rotation synthesis, accumulated decoding error and graph exceptions. A
polynomial asymptotic existence result is not a practical finite-size gate
estimate. The complete coherent circuit and finite-block error ledger remain
unimplemented here. No exponentially small finite error is inferred from the
single level12 point.

2026-10-17 follow-up: the [bounded coherent erasure stage](COHERENT_BPQM_ERASURE.md)
is now implemented, including exact public restriction-rank tests, an actual
coherent linear left inverse and retained-record sampling composition on a
cyclic graph. It is NOT the missing uniform reliability-register compiler,
and its full-root policy must not inherit the paper's extrinsic constants.
The finite Gibbs readout is not exact. Raw native rank failures and single-copy
word-error floors are retained, but a duplicate-unary example has an exact
classical factor reduction and cannot be called a sampling obstruction.

## Classical Competitors That Must Not Be Omitted

**Product USD / full-rank Prange.** Retain every clause with probability c.
Full row rank requires |S|<=M*dv/dc regardless of the instance. For c>dv/dc,
Hoeffding gives

    Pr(full rank) <= exp(-2M(c-dv/dc)^2).

At M=4096 and c=13/20, the conservative power-of-two upper bound is 2^-184.
This excludes THIS one-shot proposal as a reliable polynomial-cost method;
it does not exclude all classical samplers or rank-dependent corrections.
The illustrative M4096 bound is not a same-size comparison to an executed
quantum decoder: even the displayed extrinsic tree does not fit in4096 wires.

**Rank-aware affine-cluster sampler (implemented).** Let c=tanh(beta) and
p=2c/(1+c). From current spin word x, independently retain each SATISFIED
clause with probability p, retain no violated clause, then sample uniformly
from the resulting affine system by Gaussian elimination. Dependent satisfied
rows are legal and kept. This is polynomial work per update, with no partition
oracle and no exponentially sized state table.

To prove the stationary law, use the positive joint weight

    W(x,S) proportional to (2c/(1-c))^|S| * 1[B_S x=v_S].

Summing over S yields a factor ((1+c)/(1-c)) per satisfied constraint, exactly
the Gibbs odds. The two update steps are its two conditional distributions.
Detailed balance follows by summing W(S)W(x|S)W(y|S), symmetric in x,y.
This proof works with frustration and dependent/zero rows. Exact finite
transition matrices and all detailed-balance identities are tested.

The stationary law is NOT a rapid-mixing proof. The empty-selection event
gives only the pessimistic uniform-refresh bound (1-p)^M; it can be
exponentially small. Neither irreducibility nor a few stable energy traces
certifies total-variation mixing. This stronger competitor remains live.

**Turbo Prange and other optimizers.**
[Shutty et al.](https://arxiv.org/abs/2604.24633) give a classical enhancement
matching their locally-quantum optimization results. Their target is approximate
optima, not automatically Gibbs sampling with correct relative probabilities.
Its relevance must be checked, not ignored or upgraded to a sampling theorem.
Parallel tempering, BP-guided decimation, tensor/factor contraction and
problem-specific sampling also need comparisons. No general classical gap is
established by beating one rank threshold.

## How This Direction Could Fail

1. The local degradation proof or the external finite-graph theorem could
   have a scope/error; independently verify both before candidate admission.
2. A coherent finite-block implementation may require prohibitive constants,
   uncontrolled histories or precision. A tree certificate is not a compiler.
3. The affine-cluster or another classical sampler may mix polynomially in
   precisely this temperature range, killing the proposed separation.
4. Existing BPQM/DQI work may already contain every useful composition.
   Mechanism and published ensemble theorems are explicitly prior art; the
   local parameter certificate is not claimed novel without a literature check.
5. Gibbs sampling at only selected signs or hand-designed graphs might look
   good while the actual random regular signed ensemble fails. Do not select
   favorable code instances or import ER shattering results to regular graphs.

## Next Decisive Work

First attack the stronger classical sampler on the ACTUAL random socket
ensemble, alongside parallel tempering, and investigate structural mixing or
slow-mode certificates. Average energy is not the sampling task. In parallel,
extract finite-block constants and a phase-correct local BPQM instrument from
the literature; the trillion-output tree cost must stay visible. Do not launch
larger quantum statevectors, relabel this known mechanism as a breakthrough,
or automatically add more density-evolution parameter scans.

Run `python theorems/bpqm_gibbs_frontier.py --write`. The source-bound artifact
is `research/classical_baselines/bpqm_gibbs_frontier.json`. The focused tests
are `tests/test_bpqm_gibbs_frontier_physics.py`; optional production CLI/registry
integration belongs to Gemini and must preserve all non-admission flags.
