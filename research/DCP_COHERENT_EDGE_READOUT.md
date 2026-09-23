# A List-Free DCP Edge Readout

Status: DERIVED / REVIEW PENDING. No independent review, novelty, gate export,
polynomial decoder, or new asymptotic speedup is claimed. Implemented in
`core/dcp_coherent_edge_sampling.py`, through the existing
`python qsearch.py dcp-coherent-matching` and experiment
`EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE`. The artifact uses
`pairing_programs.coherent_edge_sampler`. This is a different readout from
the deterministic-partner compiler, not a faster implementation of that oracle.

## The Computational Question

The preceding capped balanced-support construction has useful natural-source
coverage, but its sorted join materializes exponentially many records. Can
we retain enough interference WITHOUT identifying a unique partner or storing
those lists? The construction below answers yes, with polynomial workspace.
It still takes O(2^(n/2)*poly(n)) time. Removing lists is not removing search.

Let N=2^n, m phase qubits, f_a(b)=sum_i a_i b_i mod N, and M=2^m. The clean
source is M^(-1/2) sum_b exp(2 pi i d f_a(b)/N)|b>. Labels a_i are independent
uniform residues. The prior random gauge gives matrix elements proportional
to this phase times a NONNEGATIVE survival factor w(b xor c), under the
stated prelabel classical fault-mask model. If each fault marginal is <=1/n,
w(S)>=max(0,1-|S|/n), even with within-batch classical correlations. This
is not an arbitrary quantum-noise promise or an independent-batch theorem.

Use the same fixed capped support family: each of two equal coordinate
blocks supplies its first L=ceil(sqrt(N)) lexicographic weight-k supports,
with k the first weight having C(m/2,k)>=L. The full family has D=L^2
supports S_j of width 2k. There is NO affine vertex marking in this route.
The implicit edge predicate is f_a(b xor S_j)-f_a(b)=N/2. It is symmetric
between b and b xor S_j. Let q_b be its degree. No algorithm below computes
q_b; degrees are used only in the analysis and finite diagnostics.

## Actual List-Free Procedure

Pad the support-index domain to P=2^ceil(log2(D)); padding indices never
accept. A support can be recovered from its index using division by L and
lexicographic combination unranking, with polynomial integer arithmetic and
workspace. The code checks this against independent combinations, including
a 128-bit rank without constructing its prefix list. Uniform preparation
on P indices uses Hadamards. No explicit list or QRAM is supplied.

1. Choose one public iteration count t, independently of the source, from
   the clipped geometric law specified below. A tail draw gives output zero.
2. Append a uniform support-index register. Repeat t times: phase-flip the
   valid edge indices conditioned on the unchanged source b, then reflect
   the index register about its PUBLIC uniform state. Predicate arithmetic
   and unranking workspace are uncomputed on each use.
3. Coherently verify the edge and measure the valid flag. Failure gives zero;
   its probability is not divided out of the signal or resource accounting.
4. On success retain the support index j. Choose the least set coordinate
   of S_j as a pivot, compute e=b_pivot, and XOR S_j into b iff e=1.
   The remaining source register is now a common representative r with pivot
   bit zero. Both endpoints have the same (r,j), but opposite e.
5. Measure X on e. The result is +/-1. All other outcomes count as zero.

Step 4 is a reversible orientation map: a controlled copy followed by a
controlled XOR. It does not erase an endpoint label or assume an inverse
partner oracle. Measuring the common label (r,j) is harmless to this X
statistic. In particular, j can be measured after the search: the problem
with generic witness measurements is endpoint-specific information, not
measurement of every common label. Measuring b itself would destroy the
desired coherence. No reflection about the unknown DCP source is used.

## Why A Fixed Search Time Can Fail

Write theta_q=arcsin(sqrt(q/P)). After t standard Grover iterations, each
marked index at source b has real amplitude

    g_t(q_b) = sin((2t+1)*theta_(q_b))/sqrt(q_b).

This multiple-solution formula is prior work; see
[Boyer et al., sections 2-4](https://arxiv.org/pdf/quant-ph/9605034).
The output's signed, UNCONDITIONAL parity bias is

    G_t(a) = (1/M) sum_b sum_(j valid at b)
               w(S_j) g_t(q_b) g_t(q_(b xor S_j)).

This counts oriented edges. It is NOT a sum of individual search-success
probabilities: endpoint amplitudes must interfere. For N=4, labels
(0,1,1,1), one coordinate from each two-coordinate block, P=4 and t=2,
all nonzero edges connect degree-one and degree-two vertices. Their marked
amplitudes are 1/2 and -1/2. The total clean signed bias is -1/4. Running
Grover for a seemingly reasonable fixed time can reverse the desired bit.
The implementation verifies this with the complete postselected density
matrix, not just the amplitude formula.

## A Positive Shared-Time Kernel

Let h=ceil(log2(P)/2), p=2^-h and rho=1-p. Use the SAME t across the whole
source, with probability p*rho^t for t>=0. Define

    K(q,r) = sum_(t>=0) p*rho^t g_t(q)g_t(r),
    F(x) = p^2 cos(x)/(p^2+4rho sin^2(x)).

Geometric summation and the sine product identity give

    K(q,r) = [F(theta_q-theta_r)-F(theta_q+theta_r)]/(2sqrt(qr)).

F is even and decreasing on [0,pi], since

    F'(x) = -p^2 sin(x)[p^2+4rho sin^2(x)+8rho cos^2(x)]
            /[p^2+4rho sin^2(x)]^2.

As |theta_q-theta_r|<=theta_q+theta_r<=pi, K(q,r)>=0 for all positive
degrees. Thus varying degrees cannot create negative contributions AFTER
this average. This elementary kernel argument is locally derived; its
novelty is unestablished. Ordinary randomized search-success bounds alone
do not establish this cross-endpoint statement.

There is also an exact rational form, implemented without trigonometric
rounding. Put x=q/P, y=r/P, A=p^2 and B=A+4rho(x+y-2xy). Then

    K(q,r) = (A/P)[A+8rho-4rho(x+y)]
             /[B^2-64rho^2 xy(1-x)(1-y)].

The denominator is the product of two positive trigonometric denominators.
For 1<=q,r<=C and P>=2C, use 1/(2P)<=A<=1/P, rho>=1/2, and
B<=(1+8C)/P to obtain K(q,r)>=1/(1+8C)^2.

## Constant Signal Without Isolation Or Degree Classification

For each fixed b and support S, the signed modular sum is uniform. Any two
distinct supports have a coefficient minor of determinant +/-1, so their
half-period events are pairwise independent even modulo 2^n. Therefore

    E_a q_b = lambda=D/N,
    E_a q_b^2 = lambda^2+lambda(1-1/N).

For ANY undirected graph, the number of oriented edges incident to an endpoint
of degree >C is at most 2 sum_b q_b*1_(q_b>C), at most (2/C) sum_b q_b^2.
Hence the expected oriented edge mass with BOTH degrees <=C is at least
lambda-(2/C)[lambda^2+lambda(1-1/N)]. Take C=8. Since capped lists give
1<=lambda<2, this is >=lambda(3-lambda)/4>=1/2.

We do not identify or postselect those bounded-degree vertices. They certify
a lower bound; every other edge contributes nonnegatively by the kernel.
For n>=6 and m=2n, the earlier binomial argument gives 2k<=2n/3. Prelabel
fault marginals <=1/n therefore give w(S)>=1/3. Since P>=16, the average
signed bias of the infinite schedule is at least

    (1/2)*(1/65^2)*(1/3) = 1/25350.

This is a deliberately conservative bound, not a practical sample estimate.
It is averaged over the full natural label law and public time coins. No
per-label success, independent-batch concentration, or full-secret decoder
follows without additional work. Finite controls exhaust all label tuples
in their stated small domain and separately test the graph inequality.

## Finite Runtime, Polynomial Space, Exponential Time

Set T=B_tail*2^h and abort if the geometric draw reaches T. The tail mass
rho^T<=exp(-B_tail)<2^-B_tail. Each physical outcome has magnitude <=1,
so clipping changes the signed expectation by at most this tail probability.
There is NO renormalization or free rejection of long draws. At B_tail=16,
the preceding signal lower bound remains positive after subtracting 1/65536.

Mean untruncated iterations are rho/p=2^h-1. Counting a reversible Boolean
predicate compute/uncompute pair per phase oracle and a final heralding query
gives mean <=2^(h+1)-1 and worst-case <=2T-1 predicate calls. The exact
coin sampler also costs expected O(2^h) classical draws; this is charged time,
not a free exponential-size random integer. Predicate arithmetic, coherent
unranking, reflections, preparation and measurement add polynomial factors.

Only source, index, orientation and reusable polynomial arithmetic registers
are required. No Grover history is stored: each iterate is a known unitary
with cleaned predicate scratch. The circuit uses reversible Boolean arithmetic
and uniform-index reflections, not rotations requiring knowledge of q_b.
The code executes dense small-state diagnostics; those diagnostic arrays
are explicitly NOT the scalable circuit's memory requirement. Gate export
is not implemented.

P is N or 2N in the capped family, so time remains O(2^(n/2)*poly(n)) and
space polynomial. This is not claimed to improve the known DCP
[time/query tradeoffs](https://arxiv.org/abs/2206.14408). Generic search
lower bounds do not rule out exploiting the explicit modular arithmetic:
the predicate is not an arbitrary unknown oracle in this research problem.

## What Could Still Be Wrong Or Fail

- Quantum faults with negative/complex coherences are outside the noise
  argument. Within-batch classical mask correlations are checked explicitly;
  they are not replaced by independent eta^width attenuation.
- An endpoint-dependent time distribution or retained endpoint-specific work
  changes the interference kernel. All oracle scratch is cleaned and t is
  one independent public draw. No success-probability normalization is free.
- Enlarging lists, adding controlled powers or calling a fast-forwarded Grover
  iterate does not by itself remove time: the physical implementation and
  all query/gate costs must be supplied.
- The exact rational kernel and finite unitary checks are not independent
  mathematical review. Related constructions may already be known.

NEXT: exploit arithmetic structure to replace the exponentially long Grover
evolution, or develop another collective measurement. Exponential storage,
vertex isolation, unique partners and degree estimation are no longer
necessary requirements for this route. They must not be reintroduced as
universal blockers in candidate mutation or proof tracking.
