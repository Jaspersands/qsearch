# Coherent Erasure Recovery: A Real Cyclic Decoder, Not Exact Gibbs Sampling

2026-10-17. Known BPQM/DQI mechanism; local composition REVIEW PENDING.
No new quantum algorithm, asymptotic advantage or accepted candidate.

## Question And Mechanism Choice

After the [known-norm classical theorem](JACOBI_KNOWN_NORM_REDUCTION.md)
removed the prime-conductor arithmetic opening, we compared constructive
routes. More DCP obstructions do not supply its missing receiver. Explicit
OPI still needs a matched classical/tail/decoder comparison. The LDPC Gibbs
route has a published quantum decoder, but the repo's existing programs
either require every chosen neighborhood to be a tree or pay for approximate
channel splitting. The missing erasure stage is an actual composition gap.

[Mandal et al., Section 4.3 and Theorem 30](https://arxiv.org/html/2609.05857)
give sequential tree BPQM followed by erasure recovery. [Zhou et al.,
Theorem 2.4 and Eq. 3.17](https://arxiv.org/html/2609.40345v1) connect reliable
quantum decoding to average-random-sign Gibbs sampling. These are known
mechanisms, not discoveries by this project. This pass executes the coherent
linear recovery and its actual sampling output before treating the missing
stage as an algorithmic escape.

## Problem, Input And Prospective Advantage

Public binary checks H have M columns, code C=ker H, dimension k, and an
explicit generator G. For signs J_j in {0,1}, sample the classical spin law

    pi(x) proportional to product_j [1+c*(-1)^(J_j+(H^T x)_j)],
    c=tanh(beta), 0<=c<1.

Gauge/dependent check rows are allowed. The quantum channel states are the
actual product states psi_d with coherent flip probability
gamma=(1-sqrt(1-c^2))/2. Ry, generator CNOTs and public sign phases prepare
the source; no ideal decoder, PGM mass table or partition oracle is supplied.

The conditional upside remains polynomial approximate Gibbs sampling for
a difficult explicit/random LDPC family if a uniform reliable coherent
decoder is available. This reference does NOT establish such a classical
separation, a new asymptotic algorithm, or a finite gate advantage. Affine
cluster, tempering, Prange and exact factor methods remain live competitors.

## Exact Public Erasure Criterion

Let S be good coordinates and B its complement. Restrict each generator
column to S, forming Q_S from information words to good-coordinate values.
Recovery is possible exactly when rank Q_S=k, equivalently rank H_B=|B|.
We construct L with L*Q_S=I by public binary elimination. This needs no
minimum-distance oracle. If rank fails, a nonzero codeword supported on B
is returned: zero and that word have identical good-coordinate observations.

For arbitrary erroneous good outcomes b, Lb is a TOTAL linear map. We do not
condition on consistency or postselect favorable branches. On correct good
outcomes it recovers the correct information word. This distinction is
necessary to implement recovery reversibly on a superposition.

The topology checker traverses actual raw edges and preserves parallel-edge
cycles even when their binary coefficients cancel. The random-socket helper
records the original matching before cancellation; every source/sign/rank
outcome is kept. A compilation or precision cap is not a graph-cycle finding.

Our policy uses FULL-root depth neighborhoods, unlike the paper's selected
outgoing-edge/extrinsic dv-1 policy. It is a conservative valid finite
instrument, but Theorem 30's density evolution and constants must NOT be
copied onto this policy without a separate argument.

## Actual Coherent Program And Independent Formula

For every good root i, apply its existing public U_i, copy the root bit into
its own record, and apply U_i^dagger. Other roots operate on the resulting
ACTUAL data, not fresh copies. Internal parity heralds remain coherent.
Write P_(i,b)=U_i^dagger |b><b|_i U_i and

    K_b = P_(last,b_last) ... P_(first,b_first).

The sequence V maps psi to sum_b K_b*psi tensor |b>. Append CNOTs computing
Lb in an information-estimate register E. The full sampling conversion is

    A -> E XOR original_source_label -> A^dagger -> data Z^J -> data H^M.

All good records and original labels remain present. Total qubits are
M+2k+|S|. Information-estimate scratch E clears algebraically, but the good
records and source label need NOT clear at finite error.

An independent whole-state replay checks the data amplitude in retained
record r and residual source label t, before final Z/H:

    1/sqrt(2^k) * sum_b (-1)^(J.G(t XOR Lb))
          * K_(b XOR r)^dagger K_b psi_(G(t XOR Lb)).

Tests compare complex amplitudes, not only decoder success or final energy.
Discarding/resetting work, multiplying independent root-success estimates,
or omitting A^dagger would change this state.

For each original codeword, Gao's noncommutative union bound supplies the
sufficient word-error upper bound min(1,4*sum_i e_i), where e_i are the
root errors on the ORIGINAL state. This does not assume errors stay independent
after previous measurements. The bound and actual errors are numerical
calibrations here, not certified rotation-synthesis/error intervals.

## Executed Cyclic Control

The declared mechanism control has M5 checks (25,26,12). It contains a
four-cycle, not a globally acyclic code. Good coordinates are (0,1,2), while
the systematic information coordinates (3,4) are BOTH erased. Recovery is
u_0=b_2, u_1=b_0 XOR b_2, so the test genuinely reconstructs erased information
rather than copying already-good systematic coordinates.

Both orders, both c values, all32 signs and all4 codewords are retained.
These are bounded mechanism controls, NOT samples of the regular ensemble.

| c | Root Order | Word Error | Mean Gibbs TV | Worst Gibbs TV |
| --- | --- | --- | --- | --- |
| 1/5 | forward | 0.0011576 | 0.0287862 | 0.0311089 |
| 1/5 | reverse | 0.0011565 | 0.0288005 | 0.0305156 |
| 13/20 | forward | 0.1128592 | 0.2126843 | 0.2841351 |
| 13/20 | reverse | 0.1082660 | 0.2162848 | 0.3090401 |

Thus linear erasure recovery does NOT make these cyclic local projectors an
exact normalized-coset transform. At c1/5, mean TV is over24 times word error;
delta itself cannot be used as the TV budget. These finite points do not
refute every possible O(delta) statement with an unspecified constant.
The known square-root comparison is
consistent with these complete finite laws. This is not a proof of an
asymptotic scaling exponent or a rejection of BPQM at growing depth.
At c0 the channel is orthogonal and the unconditional uniform Gibbs control
is correct. All work and leakage remain charged, with no postselection.

Every small Gibbs law is independently matched by exact integer factor
elimination. This is an executed classical sampler/reference for those
graphs, not a polynomial sampler for arbitrary-width LDPC graphs. Primitive
gate counts include the source, linear recovery, every root adjoint, the
full A^dagger, final phases and Fourier gates. The12-qubit calibrations use
floating Euler angles, not certified fault-tolerant hardware gates.

## Unfiltered Native Socket Plans

The same (3,6) socket source as the classical baseline supplies these public
topology/rank checks. Raw edges, signs and failures are retained. No quantum
circuit, decoder error or Gibbs TV is executed/inferred on these large inputs.

| Spins | Clauses/Data Wires | Seed | Good Roots | Erasures Recoverable |
| --- | --- | --- | --- | --- |
| 64 | 128 | 29 | 73 | no |
| 64 | 128 | 71 | 76 | yes |
| 128 | 256 | 29 | 218 | yes |
| 128 | 256 | 71 | 192 | yes |
| 256 | 512 | 29 | 447 | no |
| 256 | 512 | 71 | 443 | yes |

A larger graph does not automatically satisfy the exact erasure condition.
No rank/girth/source rejection is used to make the table look monotone.
Planning at512 data wires is polynomial binary algebra, NOT a512-qubit
simulation. The inherited CodeProblem cap is512; the gate-reference cap is10
data wires and the full-sign statevector cap is18 total wires. The existing
explicit herald tables can be exponential; this does not implement the
uniform approximate reliability-register scheme.

## Kill The Tempting Overinterpretation

At512 wires, seed29, the actual erasure ambiguity has support (160,189).
It is a weight-two codeword. Giving a decoder the pair label of
{d,d+w} only makes decoding easier; the two remaining pure states have
overlap c^wt(w). Therefore ANY single-copy decoder has uniform-codeword error
at least

    (1-sqrt(1-c^(2*wt(w))))/2.

Exact rational square-root enclosures record this floor (between0.04 and0.05
at c13/20). Repeating the local circuit cannot eliminate this intrinsic
single-copy word ambiguity. This says NOTHING comparable about Gibbs TV,
and it does not contradict an ensemble-average vanishing-error theorem:
the frequency of such sampled codes matters.

In fact these two native columns are identical UNARY XOR factors, both
with negative signs. They are classically merged at effective overlap
-2c/(1+c^2). More generally, for identical mask a with n+ positive and n-
negative copies, put

    A+=(1+c)^n+*(1-c)^n-, A-=(1-c)^n+*(1+c)^n-,
    K=(A++A-)/2, c_eff=(A+-A-)/(A++A-).

Their product is K*(1+c_eff*(-1)^(a.x)). Opposite copies cancel to a
constant. A zero mask is wholly constant and handled separately. Exact
rational factor identities are replayed on all small spin words and public
large-word controls. The normalized Gibbs distribution is unchanged, but
the resulting weighted instance is NOT the original common-overlap regular
ensemble; the BPQM theorem cannot silently transfer to it. Other clauses
may still be hard. This reduction is not itself a complete Gibbs sampler.

This is why a rank-failed reliable-word route must not become a false
sampling impossibility or an automatic negative quantum result.

## Research Decision And Next Decisive Gate

The coherent erasure stage is now implemented and its phase/workspace
composition is checked. It is no longer an unspecified Gaussian solve.
It supplies neither exact cyclic sampling nor a new algorithmic speedup.

Do NOT extend this by measurement-order/seed/depth scans or larger controlled
tables. Two research gates actually matter:

1. A uniform, phase-correct reliability-register circuit with charged
   approximation and sequential-error bounds on the ACTUAL full-root or
   extrinsic policy. Existing BPQM_LOG_RELIABILITY.md specifies some arithmetic,
   but this pass does not supply that compiler or claim novelty for compiling
   the published decoder. Such routine implementation can go to Gemini.
2. A genuinely different normalized-coset/readout mechanism that can tolerate
   locally ambiguous modes WITHOUT assuming classical positive prefix masses.
   Duplicate-factor reduction is a baseline, not evidence that one exists.
   Any new proposal must specify its source, full measured law, classical
   comparison and how it changes the asymptotic situation.

Given that the decoder mechanism is prior art and the classical gap remains
unestablished, main-model research should not keep rebuilding this known
algorithm by inertia. A new BPQM variation must remove a named scientific
blocker before further code. No central candidate/negative/proof is promoted.

Reproduce:

```text
python theorems/coherent_bpqm_erasure.py --write
python -m pytest -q tests/test_coherent_bpqm_erasure_physics.py
```
