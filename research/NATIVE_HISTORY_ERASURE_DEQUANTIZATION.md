# Phase-Bank History: Universal No-Go Retracted

2026-10-19. The previous "PROVED" trilemma was unsupported. Its active
negative `NEG-NATIVE-PHASE-BANK-HISTORY-ERASURE-DEQUANTIZATION-BARRIER`
is quarantined, with its COMPLETE original record preserved. This correction
does not supply an LWE algorithm or invalidate any correctly scoped reduction.

Run the existing workflow:
`python qsearch.py native-history-erasure-dequantization`.
Its producer now writes the corrected report and idempotently quarantines the
old negative rather than recreating it. `--no-registry` writes only the report.

## The Scientific Question

Does the absence of a clean classical history inverse exclude ALL efficient
quantum phase-bank receivers? NO: the claimed argument does not establish it.
The real open question is whether a constructive receiver on the ACTUAL noisy
source achieves useful, efficiently readable interference with all costs paid.
None of the countercontrols below claims such an algorithm or a speedup.

The native contract has n-dimensional secret, q=3^n, M=n^2 public headers,
and a query budget W=n^2. A phase on a selected wire is exp(2*pi*i*b_j/q),
where b_j=<a_j,s>+e_j. Formal path exponents c can describe query amplitudes,
but are not necessarily physical orthogonal registers in the executed circuit.

## What Remains Correct

For the SPECIFIED tagged state

```text
sum_c alpha_c phase(c) |v(c)> |c>,
```

tracing the orthogonal c register leaves a diagonal frequency marginal.
If alpha_c has a supplied efficient classical sampler, that MARGINAL can be
sampled classically. This is neither a sampler for arbitrary quantum amplitudes
nor a simulation of joint measurements on both registers. The old calibration
constructed its diagonal entries directly; its zero off-diagonals were built
into its state/readout assumptions, not discovered for arbitrary receivers.

For a FIXED exponent vector c, independent unwrapped errors of variance sigma^2
give variance sigma^2*||c||_2^2. If ||c||_1=W, Cauchy-Schwarz gives
||c||_2>=W/sqrt(M). A W-query upper budget does not force net L1 exposure W;
and a data-dependent c cannot automatically be analyzed as fixed independently
of those errors. These identities alone do not rule out an algorithm.

It is also correct that no unitary sends two orthogonal basis states
|v,c1>, |v,c2> to the SAME |v,0> with no other distinguishing output.
That statement is not equivalent to erasing one specified superposition in
each frequency fiber.

## Exact Countercontrols

The corrected producer uses exact matrices in Q(sqrt(-3)), not floating
tolerance flags. They isolate invalid implications, not candidate oracle tasks.

### History Is Not Mandatory

At native q9 use public header e1 and noiseless secret first-coordinate0 or3.
The phases are1 and zeta=(-1+i*sqrt(3))/2. The actual one-qubit circuit
H*diag(1,zeta)*H has probability of output0 equal to1/4, versus1 for phase1.
No query-history register is ever created. Physically adding and discarding a
which-path tag would CHANGE that experiment; it is not a harmless rewriting.
General polynomial-method expansions use amplitude polynomials, not mandatory
orthogonal path storage; see [Beals et al.](https://arxiv.org/abs/quant-ph/9802049).

### A Blind Marginal Does Not Exclude Joint Readout

For the explicitly tagged state (|00>+zeta|11>)/sqrt(2), the frequency marginal
is I/2 for BOTH phases. Nevertheless H on BOTH registers followed by their
classical parity gives even probability1 or1/4. The history has not been cleanly
erased. Discarding it and then claiming to cover ANY measurement was invalid.
These two probabilities are independently reconstructed from complete amplitudes.

### Source-State Erasure Is Not Basiswise Many-To-One Erasure

Let A=[e1,e1,e2,e2] over Z9. The distinct exponent histories (1,0,0,0) and
(0,1,0,0) have common frequency(1,0). With equal amplitudes and zero noise,
their logical history is |+>. H maps this KNOWN source history to |0> while
remaining unitary: the images of the two BASIS histories remain orthogonal.
This does not solve ISIS or erase an arbitrary noisy relative phase. It refutes
the old claimed necessity of a unique basis history for every source eraser.
Nor does an efficient QUANTUM eraser automatically imply an efficient CLASSICAL
inverse; a separate computational reduction would be necessary.

### A Bounded Fiber Is Not A Uniform Full Coset

Apply QFT over Z9^4 to the same normalized two-history source. The Fourier
outcome w=(0,3,0,0) is outside row(A)={(a,a,b,b)}. Its amplitude is
(1+zeta)/(sqrt(2)*9^2), giving EXACT probability1/13122>0.
Thus the old full-coset Fourier support conclusion cannot be applied to this
bounded fiber. The full-uniform-coset identity itself remains valid under its
own premises; truncation and noise weights must be analyzed rather than erased.

## Hardness Claim Removed

The numerical ratio q/W is not a certified GapSVP approximation factor.
The cited [Micciancio--Regev paper](https://cims.nyu.edu/~regev/papers/average.pdf),
Definition5.3 and Section5, treats specified average-case SIS ensembles and
explicit reduction hypotheses. It does not identify every source-dependent
quantum history operation with a classical inhomogeneous solver merely from
that ratio. The previous report assigned hardness booleans from n and q/W,
without implementing or checking such a reduction. Those booleans are removed.
No new claim about the tractability of random SIS/ISIS/LWE is made here.

## Consequences For Research

- Do NOT use this old negative to reject joint readout, unrecorded-history
  circuits, measurement/feedforward, or source-specific erasers automatically.
- Do require a specific source, legal access, circuit, noise analysis, success
  bound and same-input classical competitor for any proposed receiver.
- Do not infer a Shor-level algorithm from these constant-size countermodels.
  A counterexample to a universal inference is not a scaling experiment.
- The more recent explicit prime-character phase compiler remains exponential
  in its own charged model. Retracting this general no-go does not make that
  specific construction efficient.
- Further work should target a concrete structured operation that can be
  compiled, not replace this false trilemma with another unproved barrier.

Original negative evidence is preserved in
`research/registry/quarantined_campaign_negatives.json`. Running the corrected
producer cannot register it again. Changed reintroduced evidence fails closed
and requires review; archival precedes removal and concurrent writes are checked.
