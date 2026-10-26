# Ternary BPQM On Natural Shifted Graph Coloring

2026-10-20. Local derivations and bounded reference checks; independent review
pending. No efficient cyclic decoder, quantum coloring algorithm or speedup.

## Scientific Question

Can q-ary belief propagation with quantum messages (BPQM) decode a graph cycle
code well enough, coherently and at polynomial cost, to solve a natural search
problem beyond known classical methods? This is a different source from the
positive binary Gibbs channel. It is not another generic Gram inversion.

Input: a connected simple graph with V vertices, M oriented edges (u<v), and
public offsets J in F_3^M. Find colors x, with x_0=0 fixing the global gauge,
such that every y_e=x_v-x_u+J_e is nonzero. J=0 is ordinary three-coloring.
Uniform random offsets and ordinary coloring are DISTINCT input models.
No hidden advice, oracle problem, promise of colorability, or free copies.

Let B be reduced incidence and let the rows of G span C=ker B. Then
k=dim C=M-V+1, C-perp=rowspan B, and

    valid colorings <-> y in {1,2}^M with Gy=GJ.

The bijection is after the stated gauge fixing. Empty targets remain empty.
A polynomial coherent receiver plus a scope-matched successful reduction
would be interesting, but neither is currently supplied. Classical hardness
on any proposed random graph/offset ensemble is NOT established.

## The Physical Source And Actual Local Gates

Use psi_x=sum_j sqrt(mu_j)*omega^(xj)|j>, omega=exp(2*pi*i/3), with
mu=(0,1/2,1/2). Distinct symbols have overlap -1/2, NOT +1/2. The Gram
matrix has rank two; taking absolute overlaps changes its rank and the
three-state Bargmann product. It is not a harmless phase convention.

The existing signed native source shift_x(0,1,-1)/sqrt(2) maps to psi_x
by the FIXED public unitary diag(1,-i,i) times the positive-sign F_3 Fourier
transform. All three complex-amplitude identities are executed. No copy or
postselection is used. Two copies instead have normalized spectrum
(1/2,1/4,1/4), allowing zeros in the Fourier word and changing the target.

[Mandal and Pfister](https://arxiv.org/abs/2601.21330) already give q-ary BPQM
node operations and a density-evolution framework for circulant pure-state
channels. These local operations are prior art, not a discovery here. Our
reference derives its SUM-check convention independently; the paper uses a
difference convention. Its threshold estimates do not prove our loopy decoder.

The reference executes actual nine-dimensional public gates:

- Same-symbol node: SUM relabel (i,j)->(i+j,j), followed by controlled
  three-level Householders. Output spectrum is cyclic convolution mu*nu.
- SUM-check node: (i,j)->(h=i-j,j). Branch probability is
  p_h=sum_j mu_(j+h)*nu_j and conditional spectrum is mu_(j+h)*nu_j/p_h.
  The COMPLEX herald factor omega^(xh) is retained for inputs x,y.
- Exactly zero heralds are omitted without division; zero compression blocks
  use identity. No small nonzero probabilities are discarded.

Tests compare full amplitudes for 16 channel pairs and independently compare
the physical mixed-state check blocks. A deliberately dropped herald phase
has correct probabilities but the WRONG coherent state. Cyclic spectrum
gauges used for density statistics are NOT a coherent compiler.

The broader decode/uncompute reduction is motivated by existing
[ternary subset-sum work](https://arxiv.org/html/2609.40321v1) and the repo's
TERNARY_DECODER_FILTER.md. Here only the source/reduction identities and local
gates execute. No global zero-temperature sampler is claimed. In particular,
an unnormalized comparison vector is not permission to postselect a target.

## Global Checks And Two Decisive Falsifiers

For uniform codeword messages d in C, the actual physical product-state Gram is

    Gamma_(d,e)=(-1/2)^wt(d-e).
    lambda_s=3^k*N_s/2^M,

where N_s counts ALL y in {1,2}^M with Gy=s. Thus the exact Gram rank is
the number of nonempty shifted-coloring sectors. Both the physical source
matrix and its independent Fourier diagonalization are checked. Bounded
enumeration is exponential, never described as a quantum decoder.

Triangle: all three sectors are nonempty, with counts 2,3,3. K4: 26 of 27
are nonempty; the ordinary-coloring sector is empty. Its optimal numerical
collective word error is about 0.060867, and ANY uniform word decoder has
error at least 1/27. All sectors and representative original offsets remain
in the report; tests separately check every original offset on these graphs.

**The binary root-gap repair does not transfer.** On K4, let v_s be the
normalized uniform supported word vector in a NONEMPTY sector. For a public
physical edge shift X_e, there are 12 cases where both s and s+Ge are
nonempty but P X_e P v_s=0. Actual full 3^6 vectors verify this. Each edge
extends to a valid systematic information-coordinate set, so it is not an
irrelevant wire. The positive binary gap lemma cannot supply this qutrit PGM
even conditional on a span reflection. This does NOT exclude other receivers.

**Reliable six-regular word decoding is impossible for this single-copy
source.** Every product output lies in a 2^M-dimensional support, while there
are 3^k equally likely messages. The elementary POVM trace bound gives

    word success <= min(1,2^M/3^k).
    d=6: word success <= (1/3)*(8/9)^V -> 0.

This is an all-size discrimination bound, not dimension-to-gate hardness.
Reliable word recovery is sufficient for some reductions but not necessary
for every search/sampling algorithm. No general coloring no-go follows.

There is also a distinct INPUT-distribution consequence: uniform original
offsets have uniform syndrome, so their exact colorability probability is
rank(Gamma)/3^k. Their expected gauge-fixed coloring count is 2^M/3^k.
Markov's inequality gives the same six-regular upper bound. Thus almost all
uniform-offset six-regular inputs are empty, independently of decoder design.
This says NOTHING analogous about an arbitrary fixed offset or planted/SAT
ensemble. Conditioning on colorability would change the task distribution.

The numerical word-optimum formula used here does not assume a receiver.
Twirl any uniform-message POVM under the abelian code action; its seed has
diagonal 1/3^k in the nonempty-sector basis. Positivity bounds each seed
off-diagonal magnitude by 1/3^k. Therefore success is at most
(sum_s sqrt(N_s/2^M))^2/3^k, attained by the Fourier/PGM seed. Computing that
seed by enumerating sectors is still exponential.

## Exact Tree Probe And Classical Competitor

Exact rational EXTRINSIC density evolution uses distinct tree outputs, dv=2,
and preserves all branch mass. PGM symbol-error square roots get outward
64-bit rational bounds. Approximate error values, solely for readability:

| Graph/check degree | Level 1 | Level 2 | Level 3 |
|---|---:|---:|---:|
| 3 | 0.180964 | 0.069925 | 0.024793 |
| 4 | 0.257149 | 0.195224 | UNKNOWN |
| 5 | 0.295241 | 0.274526 | UNKNOWN |
| 6 | 0.314287 | 0.308148 | UNKNOWN |

UNKNOWN means an explicit exact-support/pair-work cap, not failure or success.
No pruning, renormalization, asymptotic threshold, channel cloning, cyclic
receiver or finite-block error theorem is inferred. Degree six illustrates
why local improvement alone is insufficient: its word bound tends to zero.

Z3 one-hot SAT on the ORIGINAL shifted constraints is the implemented classical
baseline; every SAT witness replays independently. Four public seeded regular
graphs retain their complete edge/offset input and no colorability filtering:
d4,V16 and d4,V32 are SAT; d5,V16 is solver-UNSAT; d5,V32 is SAT. Timeout or
missing solver means UNKNOWN, not quantum advantage. Solver-UNSAT alone is
not an independently checked proof. K4 UNSAT also has exhaustive verification.
These few outcomes imply neither asymptotic hardness nor dequantization.

Ordinary degree-three coloring is low-ceiling: the
[constructive Brooks theorem](https://arxiv.org/abs/1401.8023) supplies a
classical route outside its exceptional graphs. Do not transfer this statement
to arbitrary shifted offsets without an argument. Do not turn the improving
degree-three tree control into a major quantum candidate.

## All-Depth Support Calculation Without Larger Message Tables

This follow-up resolves a narrower question constructively: does the LOCAL
source remain rank deficient forever at degree four/five? No. It does not
establish decoding reliability, but stops a false universal singularity claim.

After every physical same-symbol node, output probabilities are
mu_j=(1-nu_j)/2. A rank-deficient output can therefore ONLY be a rotated
(0,1/2,1/2) trine: it occurs precisely when the incoming check message is a
point mass. All other output channels have strictly positive spectra.

Take r=d-1 independent child messages and suppose s are singular. Each such
message excludes one of three frequencies. Conditional check support is the
intersection after herald relabeling; full-rank inputs impose no support
restriction. The s exclusion locations all coincide with probability
2^(1-s), because their actual two supported frequencies are independently
uniform. Otherwise exactly two distinct locations are excluded, leaving one
point. Three exclusions cannot occur on an actual positive-probability branch.
For s=0 there is no singular output. Thus, with p the singular child mass,

    p_next = 1 - 2*(1-p/2)^r + (1-p)^r,   p_0=1.       (S)

Twenty actual spectral-branch controls cover EVERY s at r=1,...,5, with
nonuniform full-rank inputs. Independent tests rotate the singular inputs.
The scalar recursion also matches every available FULL exact-density level.
Nothing assumes the unspecified full-rank message probabilities are uniform.

(S) is monotone: its derivative is
r*((1-p/2)^(r-1)-(1-p)^(r-1))>=0. Exact upward dyadic rounding therefore
gives upper bounds for the original unrounded tree. A conflicting pair of
singular exclusions occurs with probability p^2/2, so the union bound gives
p_next<=A*p^2 with A=r*(r-1)/4. Once A*f<1, induction yields

    p_(L+t) <= f*(A*f)^(2^t-1).

The report certifies this at levels 0,2,10 for d=3,4,5 respectively, without
enumerating the level-ten density law or its roughly 1.4 million distinct
original outputs. Those outputs are NOT constructed or cloned by the producer.

There is also an elementary global geometric guarantee for d=5, not a fit.
Here p_next/p=3p-3p^2+7p^3/8. For p<=1/2, use p^3<=p^2/2; the resulting
increasing quadratic is at most 55/64. For p>=1/2, use
p^3<=3p^2/2-p/2, obtaining (41p-27p^2)/16<=1681/1728<1 by completing the
square. For d=3,4 the factors 1/2 and 3/4 suffice. Hence singular mass
really vanishes in these ideal trees, not merely in ten numerical iterations.

For d=6, (S) maps p=1/2 to 285/512>1/2. Monotonicity implies p_l>=1/2
for every depth from p_0=1. This is consistent with the global six-regular
word obstruction. Neither this rank-two mass nor its disappearance is a
word-error or symbol-error identity. FULL RANK DOES NOT MEAN distinguishable
states, an efficient measurement, a small condition number or a finite-block
theorem. No coherent loopy receiver has been supplied by this calculation.

## Decision And Re-entry Gates

No candidate admission. Stop degree-six reliable word-decoder work and the
binary-gap transplant. Do not spend the next pass making larger density bags.
Degrees four/five remain unresolved, not promising by default. Re-entry needs:

1. An ACTUAL phase-correct whole-input receiver or a new construction avoiding
   reliable word recovery, with polynomial gate, precision and source costs.
2. A proof connecting its unconditional output to the ORIGINAL target; retain
   empty inputs and state any satisfiability or average-input assumptions.
3. A finite-block guarantee on a specified graph ensemble, not an extrinsic
   tree statistic; no silent reuse or cloning of quantum channel outputs.
4. Matched classical search/sampling and algebraic/tensor-network attacks on
   that same ensemble. SAT seeds are calibration, not a separation.

If none is available, pivot instead of generating adjacent conditional notes.
The source singularity, rank obstruction and negative overlap must survive
any routine CLI/registry integration. Keep speedup/candidate admission false.

## Reproduce

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python theorems/ternary_coloring_bpqm.py --write
    python -m pytest -q tests/test_ternary_coloring_bpqm.py

Optional classical dependency: requirements-research-optimization.txt. Exact
report: research/phase_workbench/ternary_coloring_bpqm.json. This reference is
standalone; normal split-CLI wiring belongs to the mechanical handoff.
