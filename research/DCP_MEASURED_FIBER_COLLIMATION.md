# Measured-Fiber Collimation: An Ordinary Two-Witness Interface

Status: LOCAL DERIVATION / REVIEW PENDING, 2026-09-24. No independent review,
formal verification, novelty, implemented fast solver, or speedup is claimed.
This is a theory specification and a handoff, not a production subsystem.

## 1. Research Decision And Prior Art

Do not universally require a coherent witness sampler, uniform fiber state,
reciprocal witness mass, or erased solver history. Those are requirements of
particular earlier constructions, not every information-preserving readout.
An alternative measures a COMMON low-sum syndrome first. An ordinary classical
or quantum algorithm can then find two witnesses in SEPARATE workspace, with
measurements and nonuniform outputs, while the source register is retained.

The core operation is established prior art: [Regev, Section 3, pp. 5-6](https://arxiv.org/pdf/quant-ph/0406151)
measures a low subset sum, classically enumerates a bounded fiber, projects
onto two members, and compresses them to a phase qubit. The earlier
[subset-sum reduction](https://arxiv.org/abs/cs/0304005) also compresses known
endpoints, but its general average-case matching construction has a different
access/source contract. [Kuperberg's collimation sieve](https://arxiv.org/abs/1112.3333)
is another required comparator. This note is NOT a discovery of collimation.

The local refinements below make the interface easier to audit: use an
underfull fiber, avoid counting it, prove constant natural two-element mass,
and derive an EXACT transfer from uniform-target two-witness success. A
one-shot noisy parity readout needs only a small positive bias, not purified
recursive output. This removes unnecessary interface demands, not arithmetic
hardness. A constant-factor change to a known sieve is not the research goal.

## 2. Physical Construction

Let N=2^n, Q=2^r, 2<=r<n, m=r-1 and M=2^m=Q/2. Take m independent uniform
public labels a_i in Z_N and ideal phase states with common unknown d:

    |psi_d> = M^(-1/2) sum_b exp(2*pi*i*d*f_a(b)/N)|b>,
    f_a(b) = sum_i a_i*b_i mod N.

Write l_i=a_i mod Q and F_y={b: sum_i l_i*b_i=y mod Q}, D_y=|F_y|.
Compute this LOW sum and measure y. Its probability is D_y/M. The remaining
state is the equal-amplitude phased superposition over F_y, not a measured
individual assignment. Retain that register throughout the next step.

Run a bounded-runtime solver R(l,y) on ordinary classical input in fresh
workspace. It may use classical randomness or quantum computation, including
intermediate measurements. Require two verified DISTINCT outputs u,v in F_y.
Failure, timeout, duplicate answers and invalid congruences abort this attempt.
The solver may use l,y and fresh randomness, but not the source assignment,
the secret, discarded gauge coins, or the unused high label bits.

If a pair is returned, measure the binary projector onto span{|u>,|v>} in the
RETAINED register. Two equality tests suffice; no fiber-size oracle is used.
Acceptance is 2/D_y, even when D_y>2. Reject the other outcome. On success:

    ( exp(2*pi*i*d*f_a(u)/N)|u>
      + exp(2*pi*i*d*f_a(v)/N)|v> ) / sqrt(2).

Let S=u xor v and choose a pivot j with S_j=1. XOR u into the register, then
CNOT from j to every other coordinate where S has a 1. This is an invertible
map on the WHOLE computational basis. It sends u to 0 and v to the unit vector
at j. All nonpivot bits are zero on the accepted branch. The output is

    (|0> + exp(2*pi*i*d*delta/N)|1>)/sqrt(2),
    delta=f_a(v)-f_a(u) mod N,  delta=0 mod Q.             (1)

The solver's measured transcript is not an endpoint tag: conditional on l,y,
its complete state was initially a tensor factor of the retained register.
Its chosen pair and history can be recorded/discarded. This does NOT authorize
measuring a solver controlled by the unknown b in the earlier edge construction.
Measuring which endpoint survived would destroy the phase.

All measurements, aborted attempts, retained-source storage time and solver
work are charged. There is no amplitude amplification about an unknown state.

## 3. Constant Two-Element Mass Without A Fiber Counter

For a uniform source assignment b define q_b=D_(f_l(b))-1. For fixed b and
nonempty S, the neighbor event is

    sum_(i in S) (1-2*b_i)*l_i=0 mod Q.

It has probability 1/Q. Two distinct nonempty supports have a coefficient
matrix with a 2-by-2 minor of determinant +/-1, including nested supports.
The two equations are therefore independent over Z_Q, despite Q not being
prime. Consequently, over uniform l and b,

    E q_b = (M-1)/Q,
    E q_b*(q_b-1) = (M-1)*(M-2)/Q^2.                    (2)

For every nonnegative integer q, 1[q=1]>=q-q*(q-1). Hence the natural
Born-weighted mass of two-element fibers obeys

    E_l sum_(y:D_y=2) D_y/M
      >= (M-1)/Q - (M-1)*(M-2)/Q^2
       = 1/4 + 1/(2Q) - 2/Q^2 >= 1/4.                (3)

This is a SOURCE AVERAGE, not a claim that every label list is good. Favorable
syndromes are not selected for free. The real procedure never tests D_y=2;
the event is used only in this proof. Larger fibers can contribute positively.

### A Sufficient Worst-Case Solver Contract

An ordinary bounded-error subset-sum witness finder with a pointwise success
guarantee >=2/3 on every satisfiable instance gives R as follows. Find one
witness u. To find another, partition all strings other than u according to
their first differing bit j: fix earlier bits to u, flip bit j, and solve on
the remaining variables with the adjusted target. There are at most m cases.
If another witness exists, at least one case is satisfiable. Verify all answers;
unsatisfiable calls cannot produce a falsely accepted witness. With fresh
solver randomness, the two stages succeed with probability at least 4/9.
This is a polynomial number of calls, not a uniform sampler or a counter.

For integer rather than modular subset sum, try the possible integer targets
t+cQ for c=0,...,m with coefficients in [0,Q). This adds only polynomial
overhead and O(r+log m)-bit targets. Search can also be obtained by ordinary
decision self-reduction, with its error amplification and calls charged.

Equations (2)-(3) then give natural merge success >=1/9. A merely average-case
finder on the original distribution does NOT automatically satisfy the
pointwise guarantees on adaptively fixed-variable subinstances.

## 4. Exact Average-Case Contract And Runtime Transfer

Let tau_(l,y) be the probability that R returns a verified distinct pair,
including its own failures. Necessarily tau=0 when D_y<2. For EACH fixed l,
the physical merge probability, averaged over the measured y and R, is

    p(l) = sum_y (D_y/M)*tau_(l,y)*(2/D_y)
         = (2/M) sum_y tau_(l,y).                       (4)

Zero fibers contribute zero. Define beta=E_(l,y uniform)[tau_(l,y)], with
independent uniform coefficients AND a uniform target in Z_Q. Then

    p = E_l p(l) = (2Q/M)*beta = 4*beta.               (5)

No assumption of uniform answers, uniform physical syndromes, or fiber
counting is hidden in this cancellation. A classical benchmark can evaluate
the correct arithmetic target distribution without simulating quantum states.
It must include empty and singleton targets, failures and verification cost.
Conditioning on a planted known witness without correcting the distribution
is NOT that benchmark. In particular, the physical syndrome is size-biased
even though equation (5) uses a uniform-target arithmetic average.

Expected runtime needs separate treatment. For a variable-runtime solver,

    E_(physical l,y)[T(l,y)] = (Q/M)*E_(uniform l,y)[D_y*T(l,y)],

where T is conditional expected solver time. Its unweighted uniform average
is not automatically the physical average. If uniform-target expected time
is at most C and pair success at least beta_*>0, cap every invocation at
2*C/beta_*. Markov's inequality under the uniform law loses at most beta_*/2
success. The capped solver has merge success >=2*beta_* and a pointwise
runtime bound. Both C and beta_* must be justified, not estimated from only
successful trials. This supplies a charged reduction from average runtime.

### Two-Witness Success Is A Real Additional Requirement

Two independent calls to a canonical single-witness finder can always return
the SAME answer, even when its one-witness success is perfect. More generally,
if one call has answer probabilities p_b, two calls return a distinct pair
with probability (sum_b p_b)^2-sum_b p_b^2, not the square of total success.

There is also a natural-source counterexample to transferring one-witness
average coverage directly. A reference routine that returns a witness ONLY
on singleton fibers has

    Pr_(l,y uniform)[D_y=1]
      >= E[D_y]-E[D_y*(D_y-1)]
       = 1/4+1/(2Q),                                  (6)

using E D_y=M/Q and E D_y*(D_y-1)=M*(M-1)/Q^2. Yet it NEVER returns a pair.
Enumeration constructs this logical countercontrol; it is not an efficient
algorithm. This refutes a naive same-target coverage implication, NOT Regev's
different average-case reduction or every possible reduction using this oracle.

## 5. Fresh High Labels And The One-Shot Parity Route

Write a_i=l_i+Q*h_i. All selection probabilities above depend only on l,y and
solver randomness. For each fixed returned pair, u!=v implies some coefficient
v_i-u_i is +/-1. Thus

    delta/Q = (sum_i l_i*(v_i-u_i))/Q
                + sum_i h_i*(v_i-u_i) mod (N/Q)       (7)

is uniform over Z_(N/Q), conditional on the low transcript. The integer carry
is well defined because u,v have equal low sums. Membership acceptance is
independent of h and d. After obsolete records are discarded, fresh disjoint
batches give fresh uniform quotient labels for fixed d. Conditioning on old
high labels, or choosing pairs/acceptance by those bits, invalidates THIS
uniformity argument. It does not invalidate the physical pair projection.

For a one-shot parity readout choose r=n-1, m=n-2, n>=3. Then delta is 0 or
N/2 with equal probability. Discard delta=0, charging that factor two. X
measurement on the other outputs gives d mod 2 exactly for ideal inputs.
The ideal useful success is p/2=2*beta. An inverse-polynomial beta with
polynomial charged arithmetic therefore suffices for an efficient parity
routine, without recursive compression. Such an arithmetic solver is NOT
supplied by this note.

Full-secret recovery uses fresh states and previously recovered bits: if
d=d0+2^k*d', remove the known phase a*d0/N, then use label a mod (N/2^k) for
the smaller modulus. Include all parity stages, repetitions, small-modulus
base cases and gate-precision errors. The solver guarantee must hold uniformly
across the required input lengths. Do not claim recovery from one batch.

## 6. Inverse-n Basis Faults Need Bias, Not Purified Outputs

Use the precise prelabel classical-fault model and random X/sign gauge from
`research/DCP_PAIRING_PROGRAMS.md`. A classical mask J specifies faulty
pre-Fourier computational-basis registers. The mask and bad bits precede
independent uniform Fourier labels. Apply independent X gauges, negate the
corresponding labels, and discard original labels/gauge coins BEFORE solver
selection. For mixtures of these product inputs the resulting source is

    rho_(b,c) = exp(2*pi*i*d*(f_a(b)-f_a(c))/N)*Gamma(b xor c)/M,
    Gamma(S) = Pr[J has no coordinate in S].           (8)

This includes arbitrary within-batch CLASSICAL fault correlations, not
arbitrary entangled corruption, label-adaptive faults or an adversarial
quantum channel. With marginal fault probability <=1/n, the union bound gives

    Gamma(S)>=1-|S|/n>=2/n,   since |S|<=m=n-2.        (9)

The diagonal remains uniform, so every Born weight and equation (5) is
unchanged. Conditional on a selected pair, the output off-diagonal is
attenuated by Gamma(S); ordinary independent dephasing visibility nu instead
gives nu^|S|. High-bit uniformity in (7) also remains valid under this source
model. No inaccessible noise environment is uncomputed or reordered.

Record X=0 on any failure or delta=0; otherwise record the +/-1 X outcome.
Combining (5), the charged half-label probability and (9),

    E[(-1)^d X] >= p/n = 4*beta/n.                     (10)

For the pointwise witness-finder construction this is at least 1/(9n).
Independent batches give bounded-error parity using O(n^2*beta^-2*log(1/eta))
attempts for error eta by a conservative Hoeffding bound. Suitable conditional
drift guarantees could replace independence; marginal promises alone do NOT
prove concentration across arbitrary correlated batches. Smaller-modulus
stages retain the original fault bound and need the same source audit.

This is a scoped conditional noisy-parity reduction, not a promoted solution
of the complete lattice reduction promise. It does not repair the earlier
recursive visibility failure: that construction changes many original
coordinates over many levels. Here there is only ONE full-width projection.
Constant noise is outside (9); no robust constant-noise decoder follows.

## 7. Resource And Research Consequences

Polynomial-time worst-case subset sum would be far stronger than needed.
The useful target is instead inverse-polynomial DISTINCT-pair success beta
on the explicit uniform (l,y) distribution near density one, with every
runtime, data structure and failure charged. Ordinary quantum arithmetic
may be used without compiling its outputs into a source-controlled unitary.

This permits correctly scoped existing baselines, not a new speedup. For
example, [Chukhin et al., Corollary 1.3](https://arxiv.org/html/2608.07309v1)
states a worst-case O*(2^(2m/7)) quantum subset-sum algorithm. Its Section 2.3
assumes coherent read-write QRAQM. The seven-block construction stores
exponentially large quantum-addressable dictionaries; those do not disappear
because the outer input is classical. Pointwise self-reduction and integer
quotient enumeration preserve this exponential scale up to polynomial factors.
The direct full-width DCP use is exponential, worse asymptotically than known
sieves. Random-instance exponents require their own source-transfer proof.

With smaller block r, a constant-success ordinary Grover finder has
O(2^(r/2)*poly(n,r)) work and polynomial workspace. Fresh-batch recursion costs
at least the explicitly charged renewals, bounded above using p0=1/9 by

    S_i <= (r_i-1)*S_(i-1)/p0,
    W_i <= ((r_i-1)*W_(i-1)+C_i)/p0.

For r=Theta(sqrt(n*log n)), this is the already known
2^O(sqrt(n*log n)) class. Plugging in an exponential-space arithmetic routine
does not preserve a polynomial-space claim. No new asymptotic algorithm is
being proposed. Under noise, do not attach the one-shot bound (10) to this
recurrence without a separate composition proof.

Adversarial priorities:

- A global short-relation finder is not automatically a target-conditioned
  pair finder. Keep the existing explicit-dictionary coverage obstruction in
  `theorems/dcp_partial_relation_coverage.py`; its scope does not ban implicit
  target-dependent solvers. Do not build another duplicate obstruction module.
- The hard work is arithmetic at near-unit density, not manufacturing more
  named phase families or displaying full fiber tables.
- A classical pair solver would already be a major arithmetic development.
  Its existence would not classically simulate the unknown DCP phase source.
  A quantum pair solver must face charged classical baselines on the SAME
  target distribution, not easier planted or favorable-fiber benchmarks.
- Repeated canonical answers, subgroup samples, uncharged precomputed lists,
  and untested average-to-conditioned reductions are immediate falsifiers.
- Abort this line as a purported breakthrough if the only change is a known
  exponential exponent or a constant sieve success improvement. Retain it
  only as a baseline/access-contract correction.

## 8. Executed Mathematical Controls

Only bounded independent probes ran in this pass. No production implementation,
full suite, registry refresh or scalable solver was run.

Exhaustive natural low-label ensembles gave:

| r | m | Label tuples | Two-element Born mass | Perfect-pair acceptance | Bound (3) |
|---|---|---|---|---|---|
| 2 | 1 | 4 | 1/4 | 1/4 | 1/4 |
| 3 | 2 | 64 | 21/64 | 43/128 | 9/32 |
| 4 | 3 | 4096 | 357/1024 | 6007/16384 | 35/128 |

Both factorial moments (2) matched exact fractions on all 4164 label tuples.
Across every target in those ensembles, 66064 target-law controls verified
(4)-(5) for a deliberately nonuniform pair-success rule
tau=(1+(sum(l)+y) mod 5)/6 on D>=2. First-differing-bit self-reduction found a
second witness exactly when one existed in 26497 nonempty instances. The
singleton-only solver's uniform successes were 3/8, 21/64 and 1267/4096,
while its pair success was zero. Perfect repeated canonical calls also fail
the distinctness requirement by construction.

Full sum/low-measurement/pair-projection/bit-compression checks used
(N,r,a)=(8,2,(0)), (8,2,(1)), (16,3,(1,1)), (16,3,(1,7)),
(32,4,(1,1,2)), (32,4,(3,5,8)), (32,3,(0,8,16)),
(32,3,(1,1,1,1)). The last two deliberately test LARGER fibers outside
m=r-1. All 176 secret-instance cases and 656 accepted pair branches matched
the physical map, including reversed endpoint ordering; maximum amplitude
residual was 1.27e-14. The same branches matched mixed-state attenuation
nu^|S| at nu=.8. Five complete high-lift ensembles gave exactly uniform
quotient labels. Fifty-six which-endpoint dephasing controls gave fidelity
1/2, distinguishing a pair-subspace projection from reading the assignment.

Separate explicit fault-mask AND gauge enumeration constructed the source
without reusing (8) as the simulated state. Cases were
(n,a)=(3,(4)), (4,(1,7)), (4,(0,8)), (5,(3,5,8)),
(5,(0,16,0)), (5,(1,2,13)). The fault law has no fault with probability 2/n
and each singleton fault with probability 1/n, so the faults are correlated
and Gamma(S)=1-|S|/n. All 136 secret-instance checks matched (8) and the
pairwise attenuation used in (9)-(10), with
maximum density-matrix residual 2.34e-15. Natural parity signal averaged over
all low labels and the independent high bit was respectively .08333333,
.1123046875 and .1211669921875 for n=3,4,5, above the p/n bounds.

A separate 65536-row runtime control at r=4 assigned cost 10000 to D>=4
and cost 1 otherwise, with perfect pair answers when D>=2. It verified the
different uniform and physical expected costs and the charged truncation
inequality. A high-label-dependent rejection control on low labels (1,7),
Q=8, N=16 changed quotient counts from (2,2) to (2,0), retaining half the
mass. This deliberately defeats an overbroad high-label uniformity claim.

These finite controls check normalization, signs, source weighting, distinct
answers and fault scope. They are not proofs of asymptotic arithmetic speed,
novelty, independent review, or the complete DCP/lattice promise.

## 9. Gemini Handoff And Next Theory Target

1. Add this as a measured-common-syndrome mode of the EXISTING DCP matching
   experiment, not a new promising candidate. Keep the coherent edge mode and
   its distinct requirements intact. This mode is not implemented by a
   Python witness returned while the source is secretly already measured.
2. Implement a bounded small-instance physical reference with a retained
   source density matrix, a separate classical pair-selector interface,
   pair-subspace projection and invertible bit compression. Reproduce the
   input cases and exact fractions above; independently test failures,
   duplicates, D>2, reversed orientation and which-endpoint measurement.
3. Benchmark arithmetic on independent uniform coefficients/targets, reporting
   beta, charged runtime INCLUDING failures, memory/addressing model, and
   the exact predicted physical success 4*beta. Separately sample physical
   syndromes with Born weights and verify the prediction. Never expose a
   planted witness to the solver or silently substitute a legal-only score.
4. Test distinct-witness self-reduction and modular/integer conversion. A
   pointwise baseline can certify the 1/9 bound; an average-case heuristic
   must earn its own two-witness coverage. Test the variable-runtime cap and
   keep the source-weighted cost distinct from the uniform-target average.
5. Test high-label uniformity and a deliberate high-bit-dependent rejection
   countercontrol. Apply the existing prelabel gauge, test correlated faults,
   and expose parity bias separately from output purity. Do not auto-promote
   f=1 compatibility, full-secret recovery or cross-batch concentration.
6. Keep all access, source, asymptotic and review claim gates literal. Existing
   QRAQM/exponential baselines are controls, not discoveries. Run the ordinary
   focused/full validation workflow after implementation. Report mathematical
   discrepancies rather than loosening assertions; commit infrequently.

Next main-model work should attack the specified TWO-witness arithmetic
distribution or find a genuinely different collective operation. More
workspace symmetrization is not a universal prerequisite. Conversely, this
correction does not make generic subset sum easy, and no further solver
wrapper should be counted as algorithmic research progress.
