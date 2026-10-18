# Clean First: Pay The Source Tradeoff Before Demanding A Noise Decoder

CONDITIONAL RESOURCE TRANSFER / REVIEW PENDING. No predictor, new reduction,
novelty, hardness certificate or accepted algorithm. Run
`python theorems/dcp_clean_source_budget.py --write`; live output is
`reductions/dcp_clean_source_budget.json`, with matching contract/tests.

## Priority Revision

The preceding error-frame work shows that multimode correction is possible in
principle but provides no efficient circuit. It must NOT become a new mandatory
obstacle before considering a clean breakthrough algorithm. The existing
source/reduction already allows a tunable smaller failure budget, at a worse
gap and precision cost. Preserve high-noise work as an optional lower-gap
direction, not the definition of the entire search space.

This principle is OLD: Regev explicitly observes that a coset-sampling algorithm
using polynomially many registers can take the failure exponent large enough
that all required registers are good with high probability. See Theorem1.1
and the following corollary in the cached primary source
`literature_cache/cs_0304005_source/quantum_average.tex`, especially lines125-140.
The improved-source proof also charges tensor preparation error against the
algorithm's success margin. This planner makes those requirements operational
for the current native-bit and sine-window experiments, not newly discovered.

## 1. A Costed Generic Transfer

Assume an ACTUAL bounded clean predictor uses at most K original phase qubits
and has average useful-bit success>=1/2+epsilon. In the original product input,
let noise be a classical mixture of original Z masks. For each fixed secret,
allow arbitrary mask correlations, but bound the source-average probability
of a Z on each original qubit by gamma/2. Labels must retain their declared
full joint law. Then

```text
E_A trace_distance(noisy_CQ_input, clean_CQ_input)
 <= Pr[at least one Z] <= K*gamma/2.
```

This need not assume independent masks. Contractivity and the variational
measurement bound transfer the same unconditioned success probability, even
for adaptive quantum processing on the given bounded input. All rejected
outcomes must remain paid. Add REAL joint-CQ or uniform-channel preparation
error and adapter channel error; do not divide by a rare-label probability.

The explicit allocation is

```text
gamma = epsilon/(2K)                     -> loss<=epsilon/4,
joint preparation error per call<=epsilon/(8K) -> loss<=epsilon/8,
all added adapter-channel error<=epsilon/8     -> loss<=epsilon/8.
```

Thus noisy advantage>=epsilon/2. At most2K known adapter rotations can each
have error<=epsilon/(16K). Their finite-gate synthesis/precision must actually
be charged; the planner does not certify the existing float compiler meets it.
The clean predictor's own algorithm/circuit error belongs in its assumed clean
guarantee, not an unallocated final margin.

If faults correlate ACROSS repetitions, do not infer independent majority
votes from this single-invocation guarantee. Apply the budget to the ENTIRE
bounded amplified algorithm or prove the fresh product-source independence
used by the existing bit-recursion/majority reduction.

### Why Local Visibilities Alone Are Not Enough

The actual state sqrt(1-eta^2)|++>+eta|--> has one-qubit trace error eta^2
but joint trace error eta. At eta1/8, the sum of local errors is1/32 while
the joint error is1/8. It is not a classical Z-mask mixture. The workbench
replays this counterexample and three actual original Z-mixture laws, including
correlated shared faults. The stronger noise model is not inferred merely
from the same measured local marginals.

## 2. Solve The Source-Modulus Fixed Point

Use public row basis B and a declared interval
ell_lower^2<=||u||^2<=ell_upper^2. The shortest vector is NOT an input.
Exact B^-1 gives conservative coefficient bounds

```text
c_j = ceil sqrt(ell_upper^2 * sum_i B^-1[i,j]^2).
```

For every split coordinate and residue1<=g<p, the parent displacement satisfies
sum|h_j|<=C=sum c_j+1. This bound is independent of privately known coordinates
and of which residue/coordinate trial will work.

Let parent box M=2^m, lattice dimension d, and actual CYCLIC phase bits
t=d*(m+1). Declare a polynomial copy model K(t)=c*t^b and advantage
epsilon(t)=a/t^r, with fixed b,r. This is a hypothetical resource declaration,
not an implemented predictor. Choose m so

```text
C/M <= gamma(t)/2,
gamma(t)=epsilon(t)/(2*K(t)).
```

Increasing M changes t and therefore BOTH K and epsilon. The exact monotone
iteration recomputes them until the final inequality closes; it never uses
the old smaller modulus to justify the final noise budget. Caps return UNKNOWN,
not a hardness or impossibility claim.

Reject impossible useful-bit declarations using
(2^K-1)/(2*q^rank)<epsilon. This comparison avoids allocating rank*t bits of
integers. Scalar rank1 and lifted native rank(t-8) are distinct options: a
linear-in-t copy model can be information-legal for the former but impossible
for the latter. Neither a sufficient copy count nor a predictor is supplied.

Choose dyadic sine packet side S satisfying

```text
(242/49)*ell_upper^2/S^2 <= gamma(t)/2.
```

Then choose sufficient gap G and splitting prime p with STRICT

```text
G^2*ell_lower^2 > d*S^2,
(p-1)^2*ell_lower^2 > d*S^2.
```

The p-1 cross-colour condition cannot be replaced by p. Parent boundary plus
packet loss is<=gamma at the actual final modulus. The live integration
materializes a certified splitting prime, constructs the existing typed
SineWindowSource, and crosschecks its promise_budget and symbolic resources.
It does NOT simulate a large source or certify arbitrary lattice/norm/trial promises.
The live integration calibration is stronger than an assumed-gap ledger: a
public unimodular row transformation maps its basis to diag(1,D), with D above
the required gap. This certifies that EASY family's norm, gap and nonzero parent
shift(0,-1); it supplies no hard instance or generic shortest-vector oracle.
No short-vector coordinates enter the planner or source constructor.

## 3. What The Tradeoff Does And Does Not Buy

Ignoring dyadic constants, the source's sufficient gap scales as

```text
sqrt(d*K(t)/epsilon(t) * ell_upper^2/ell_lower^2).
```

For fixed polynomial K and inverse-polynomial epsilon, bounded norm ratio and
log C polynomially controlled, this remains polynomial. It may be a WORSE
gap than a robust decoder could tolerate, but it need not erase the value of
a clean polynomial DCP algorithm. This is why the search must keep clean
scalar/native finders ahead of routine high-noise error-correction repairs.

Do not silently claim a dimension-only gap exponent from arbitrary input bit
length. Large norm intervals or unbounded coefficient bit lengths can worsen
the parameterization. Appropriate preprocessing/family assumptions and length
guessing are separate obligations. Public packet/parent magnitudes can be
exponential while their BIT WIDTHS remain polynomial; source circuit resources
must be evaluated on those widths, not treated as free.

Every coordinate/residue trial costs resources: d*(p-1), multiplied by all
length guesses and bounded decoder attempts. Wrong trials do not provide a
correct-trial flag; they require the existing reconstruction/public verification
logic. Full end-to-end composition and actual joint source/finite-gate
precision remain missing. The easy diagonal/sheared planning bases are not
hard lattice families, and a higher gap is not a hardness certificate.

## Revised Next Experiment

The actual missing research object is still a UNIFORM clean arithmetic finder,
phase-aligned sampler, useful-bit decoder or nonmonomial receiver with proved
source-average advantage and costs. Test it against the useful-bit copy gate
and matched classical algorithms. If one exists, first use this planner to see
whether stronger source promises suffice before requiring a noise-tolerant
multimode implementation. Robustness work matters when it demonstrably lowers
the necessary gap or addresses a source whose noise cannot be tuned cheaply.

Primary context: [Regev, Quantum Computation and Lattice Problems](https://arxiv.org/abs/cs/0304005).
This is an integration/priority correction to existing reductions, not a new
theorem of equivalent scientific significance and not an algorithm result.
