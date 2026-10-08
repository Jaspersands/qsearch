# A General Proper-Marginal And Pair-PSD Gap

LOCAL DERIVATION / REVIEW PENDING. Elementary representation counterexample,
NOT a novelty claim, native-source hardness theorem or quantum algorithm.
This is a proof control, never an oracle algorithm candidate or benchmark.

## Statement

For every odd M>=5, there exists a projectively consistent family of genuine
Boolean distributions on EVERY subset of size at most M-1, with pair moments
having a PSD moment matrix, but no global M-event distribution with those
pair moments. Thus pair PSD plus even all proper native marginal tables
does not guarantee global realizability. This does not address higher-order
moment PSD with all conditioned equations or any particular quantum source.

Use Boolean native events X_i taking values+1/-1, not qubits or oracle values.
Their target moments are

```
E[X_i] = 0
E[X_i X_j] = -1/(M-1), i!=j.
```

## Genuine Proper Marginals

Let U_N be the uniform distribution on balanced +/-1 words of EVEN length N.
It is invariant under coordinate permutations and global sign reversal.
Since the total spin is identically zero,

```
0 = E[(sum_i X_i)^2] = N + N*(N-1)*E[X_1 X_2]
E[X_1 X_2] = -1/(N-1).
```

For any k<=M-1, take the k-coordinate marginals of U_(M-1) and U_(M+1),
with weights

```
w_minus = (M-2)/(2*(M-1))
w_plus  = M/(2*(M-1)).
```

Both are genuine native probability laws, so their convex combination is
nonnegative, normalized and projectively consistent on every proper subset.
Exchangeability makes subset names immaterial; restricting one coordinate
commutes with the same two-component mixture at every k.

For a PARTICULAR ordered k-word with h positive signs, its probability is

```
p_N(k,h) = binom(N-k, N/2-h) / binom(N, N/2)
p_M(k,h) = w_minus*p_(M-1)(k,h) + w_plus*p_(M+1)(k,h).
```

Use zero for out-of-range binomial lower arguments. This is per WORD, not
the probability of the Hamming-weight class; the latter multiplies by
binom(k,h). Normalization follows by partitioning balanced N-words according
to the chosen k coordinates. Projective consistency follows from Pascal:

```
p_N(k,h) = p_N(k+1,h) + p_N(k+1,h+1).
```

The mixture is unbiased and has the desired pair correlation:

```
-w_minus/(M-2) - w_plus/M = -1/(M-1).
```

For M=5, every triple has per-word probabilities1/32 on the two all-equal
patterns and5/32 on the six mixed patterns. Every quadruple ALSO has a
genuine distribution consistent with those triples. Tables on proper subsets
therefore cannot repair the pair-level global contradiction on their own.

## Exact Pair PSD

The sign correlation matrix is

```
R = M/(M-1)*I - 1/(M-1)*J
v^T R v = sum_(i<j) (v_i-v_j)^2 / (M-1) >= 0.
```

The constant/sign moment matrix is diag(1,R). The native binary indicator
matrix follows by congruence, since D_i=(1+X_i)/2 and1-D_i=(1-X_i)/2.
Thus the complete pair indicator matrix is PSD, without numerical spectra.
The displayed sum-of-squares identity provides a general rational proof;
exact LDL on selected M values is an additional implementation control.

## Global Native Contradiction

At the proposed pair moments,

```
E[(sum_i X_i)^2] = M + M*(M-1)*(-1/(M-1)) = 0.
```

For odd M, every native word has an ODD integer total spin, whose square
is at least ONE. No positive global distribution can have this expectation.
The gap is therefore strict even though every proper marginal table exists
and the pair matrix is PSD.

In binary native indicators, one can retain the primitive quadratic inequality

```
Phi = (M^2-1)/8 - (M-1)/2 * sum_i E[D_i]
      + sum_(i<j) E[D_i D_j] >= 0.
```

Pointwise Phi=((2*number_of_positive_signs-M)^2-1)/8 is a nonnegative INTEGER.
At the proposed moments E[D_i]=1/2 and E[D_i D_j]=(M-2)/(4*(M-1)),
Phi is EXACTLY -1/8 for every odd M. All coefficient bit sizes are logarithmic
in M. This is a native integrality constraint, not merely a PSD square.

## Why This Is Not Source Hardness Or An Algorithm Result

This construction concerns consistency representations, not the random
ternary label population. It deliberately exposes an odd-cardinality parity
contradiction. If the same odd-sum equation is explicitly presented as a
native constraint, a modulo-two test may reject it immediately. It must not
be promoted as a hard source instance or evidence against algorithms using
integer/parity constraints, higher-order PSD, full conditioned equations,
branching or a different quantum receiver.

The useful conclusion is architectural: neither a positive pair matrix nor
consistent proper marginals certifies a global native distribution. The
existing actual-source prefix experiments remain separate and scope-limited.
No generic quantum lower bound follows from a classical relaxation gap.

## Implemented Compressed Proof Control

The implementation supplies an exact compressed native-event marginal schema
(not CandidateRecord) in `theorems/ternary_proper_marginal_gap.py`.
For M=5,7,15,31,63, retain all k/h class probabilities, normalization sums,
projective Pascal identities, exact pair moments, the PSD sum-of-squares
identity and strict odd-native quadratic certificate. O(M^2) class records
replace exponentially many words; table compression does not create a global
distribution or a source sampler.

Independent verification checks complete k/h schedules, exact binomial
counts, probability nonnegativity/normalization, all projective identities,
pair moments, PSD factor identity and Phi=-1/8. Use EVEN M balanced-word
distributions as honest controls: the odd-native inequality is NOT valid
there, and no false global contradiction may be claimed. Individual k-word
probabilities differ from Hamming-class masses and must not be confused.

This general falsifier may be more useful than endlessly growing selected
local cuts. Keep theorem/novelty review pending and prohibit candidate or
population-hardness promotion. Follow it by the receiver obligation audit:
which construction needs classical witness finding, and which coherent
measurement architectures might bypass that sufficient helper?

## Durable Controls Executed

The live report `research/phase_workbench/ternary_proper_marginal_gap.json`
retains five odd controls at M=5,7,15,31,63 and five honest even controls at
M=4,6,16,32,64. Together they check5,577 class records,5,329 projective
identities,248 normalization sums, ten exact matrix LDLs and42,628 indicator
entries, without enumerating native words or calling an LP. Every odd native
Hamming weight satisfies the parity inequality; every even full law is truly
global and rejects transplanting that inequality. The standalone BigInt
checker independently verifies the entire compressed certificate:

```
python theorems/ternary_proper_marginal_gap.py --write
node research/certificates/ternary_proper_marginal_gap_crosscheck.js
```

Twenty-one focused tests cover probability/class-mass confusion, omitted
classes, noncanonical rationals, corrupted positivity factors, scope flags
and complete preflight unknowns. The receiver audit now proceeds in
`research/TERNARY_COHERENT_EDGE_RECEIVER.md`, rather than treating classical
witness finding as a necessary interface for every measurement.
