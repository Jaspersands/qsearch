# Copy-Only Principal-State Preparation With Polynomial Gap Cost

2026-10-23. Written composition of known quantum PCA and density-matrix
exponentiation, with explicit caps and finite channel checks. Not a novel
purification algorithm, independently certified theorem, executed HSP receiver,
or classical-input quantum speedup. The original repository remains unchanged
while its Desktop-to-local migration is active.

## Research Decision

The existing `research/REES_NOISY_STATE_SOURCE.md` correctly charges its
recursive symmetric-SWAP purifier, but that particular bound is exponential
in the inverse principal spectral gap. Its constant-gap sufficient regime
is not a necessary limitation of copy-only principal-state preparation.

Known quantum PCA gives an alternative. The derivation below prepares a batch
of T approximate principal-state copies with a deterministic raw-copy cap
polynomial in T, 1/Delta, and 1/epsilon, using only fresh IID mixed copies and
known controlled partial SWAPs. It does not request a preparation inverse,
tomography, a principal-state reflection, classical matrix entries, or a known
top eigenvalue. The one-shot calibrated threshold and complete-output error
accounting are made explicit to prevent free postselection or inverse access.

This removes a source-contract restriction, not the application's missing
hard family. The polynomial-stabilizer application was rechecked first:
derivative, exposed Frobenius, orbit-module, and semantic Moore filters already
rule out the tempting structured constructions. No surviving useful family was
identified in this pass. Do not create more such examples as candidates.

## Prior Art

- [Lloyd, Mohseni, Rebentrost, quantum PCA](https://arxiv.org/abs/1307.0401)
  supplies the basic idea of using copies to reveal eigenvectors as states.
- [Kimmel et al., Appendices B-D](https://arxiv.org/html/1608.00281)
  explicitly treat sample-based evolution, its controlled version, and phase
  estimation. None is claimed as a new mechanism here.
- [Go et al.](https://arxiv.org/html/2412.02134v2) provide non-asymptotic
  channel-error bounds and discuss composition. Our conservative constants
  below follow a separate elementary second-derivative bound, with full versus
  normalized diamond distance distinguished.
- [Grier et al.](https://arxiv.org/html/2503.22644) analyze recursive SWAP
  purification for general spectra. Its shrinking-gap cost should not be
  mistaken for a lower bound on every physical preparation method.

No novelty or optimality claim is made for the following bookkeeping.

## 1. Input, Output, And Promises

Input: fresh jointly IID copies of an unknown d-dimensional density rho;
a supplied rational Delta in (0,1] with lambda_1-lambda_2 >= Delta; a positive
integer T; error epsilon in (0,1/2]. The top eigenvalue is nondegenerate, and
its normalized eigenvector is psi. In particular lambda_1 >= Delta. Supply
known operations on the encoded registers, including controlled register
SWAPs. The cost of obtaining a raw copy is additional to the copy count.

Output: T registers, or an explicit ABORT flag. After discarding all internal
records, the complete output is within trace distance 5 epsilon/8 of
`OK tensor (|psi><psi|)^tensor T`, including the ABORT probability, with the
gate allowance below. This statement concerns the retained batch. It is not
a certificate that an arbitrary correlated source has become independent or
that the discarded environment has any stronger specified state.

The supplied gap is not verified by a successful run. All parameter dependence
is polynomial in 1/Delta, NOT its bit length. Exponentially small Delta still
costs exponentially many copies. Arbitrary pre-noise pure states need not equal
psi, and exact conjugation symmetries of rho are a different target.

## 2. A Legal Controlled Evolution

For control C, target A, and a fresh program E in rho, let P=|1><1| and
S=SWAP_(A,E). Apply exp(+ih P tensor S), then discard E. For every operator
on C,A and any retained reference, its derivative at h=0 is the commutator
with +i(P tensor rho). Thus this channel and conjugation by
`exp(+ih P tensor rho)` have equal zeroth and first derivatives.

Both underlying Hamiltonians have operator norm at most one. A commutator
superoperator has diamond norm at most two, so each second derivative is at
most four. Taylor's integral remainder gives at most 2h^2 per channel and
therefore a difference at most 4h^2 in FULL diamond norm. Tensoring a reference,
appending rho, and tracing E preserve these bounds. This argument does not
require h to be infinitesimal or the target to be an eigenstate.

N fresh collisions of angle t/N implement controlled exp(+it rho) with

    full diamond error <= 4 t^2/N.

This is a consumed-copy channel, not a reusable unknown unitary oracle.
Controls apply to known SWAP gates, not to an unspecified black box.
Negative angles are equally implementable without an inverse source.

For a single control and reference R, write an input in control blocks
[[A,B],[C,D]], let Q=I_R tensor rho, and c=cos h, s=sin h. The actual channel is

    A -> A;
    B -> c B - i s B Q;
    C -> c C + i s Q C;
    D -> c^2 D + s^2 (Tr_target D tensor rho) + i cs [Q,D].

`spectral_source.py` implements this linear map. An independent full dilation
checks all complex matrix units with a retained reference. Merely checking
diagonal control inputs would miss the essential relative phase.

## 3. A Bounded Nondemolition Eigenvalue Estimator

First consider exact evolution; all its replacements are paid in Section 5.
Perform standard phase estimation on

    U = exp(2 pi i (I+rho)/4).

The known scalar phase is applied to the control and must NOT be discarded.
Eigenphase theta=(1+lambda)/4 lies in [1/4,1/2], away from wraparound.
Choose power-of-two L >= 256/Delta. Decode y as
`clip(4y/L-1,0,1)`. One QPE has error greater than Delta/8 with probability
at most 1/4 for every eigenvalue.

For completeness, the QPE probability at circular grid distance z from
L theta is at most 1/(4z^2). Bad decoded estimates require z>=L Delta/32>=8.
There are at most two grid points in each unit-distance shell, so the tail
is at most `(1/2) sum_(j>=8) j^-2 <= 1/14 < 1/4`. Clipping is nonexpansive;
the phase offset prevents wraparound from invalidating this implication.

Repeat QPE an odd R times on the SAME target and take the median. Conditional
on its eigenvalue, these exact QPEs are independent and nondemolition.
Hoeffding bounds the median failure by exp(-R/8). It is wrong to replace the
target with a different raw copy at each repetition: those eigenvalues need
not agree. Only the DME program registers are refreshed at every collision.

## 4. Calibrate Without Knowing lambda_1; Retain Every Failure

Let `ell(x)=ceil(log2 x)`, used only with x>=1, and set

    M = ceil(ell(8/epsilon)/Delta),
    B = ceil(ell(8T/epsilon)/Delta),
    J = M + T B,
    R = 8 ell(8J/epsilon) + 1.

1. Measure M independent raw targets using the median estimator. Let v be
   the largest reported eigenvalue and freeze `threshold = v-Delta/2`.
   Discard all calibration targets. Do not repeatedly recalibrate until a
   favorable answer appears.
2. For each of T output positions, try at most B fresh raw targets. Apply
   the median estimator; retain the target iff its estimate exceeds the
   fixed threshold. Every rejection consumes its target and program copies.
3. If an output position exhausts B attempts, discard all retained outputs
   and return ABORT. Otherwise discard internal records and return the batch.

An exact-QPE analysis can regard each input rho as a classical mixture of
its eigenvectors; this is a proof decomposition, not an available sampler.
With probability at least 1-epsilon/8 a principal target occurs among the M
calibration draws, since lambda_1>=Delta and (1-Delta)^M<=exp(-Delta M).
All at most J median estimates are accurate except with probability epsilon/8.
On these events

    lambda_1-5 Delta/8 <= threshold <= lambda_1-3 Delta/8.

A principal target's good estimate exceeds the threshold, whereas every
other target's good estimate is below it, even at the smallest promised gap.
The probability some output slot's B underlying draws miss the principal
index is at most T exp(-Delta B)<=epsilon/8. Hence all outputs are exactly
psi on a good event of probability at least 1-3 epsilon/8 in the ideal process.

This yields a bound on the COMPLETE retained output, not a bound obtained by
renormalizing a rare accepted branch. Bad events include false accepts,
calibration errors, missing top draws, and explicit aborts. The same bound
applies to a downstream circuit by trace-distance contractivity.

## 5. Charge All Controlled Calls And Gate Precision

One QPE uses m=log2 L controlled times `t_j=(pi/2) 2^j`, j=0,...,m-1.
Use the rational upper bounds b_j=2*2^j and

    W = J R sum_j b_j = 2 J R (L-1),
    N_j = ceil(16 b_j W / epsilon).

Every occurrence of power j uses N_j FRESH program copies. A full-channel
hybrid over at most JR QPEs gives

    sum_calls 4 t_j^2/N_j <= epsilon/4 (FULL diamond norm),

or epsilon/8 in trace distance, including entangled references, measurement
records, adaptive acceptance, and aborts. Clocks apply to every history; no
correct-history-only runtime assumption is used. This also avoids treating
an approximate density-matrix simulation as exact nondemolition evolution.

The deterministic raw-copy cap is

    N_raw = J + JR sum_j N_j
          <= J + 16 W^2/epsilon + JRm.

The first J term counts target registers separately from programs. Thus

    N_raw = O(T^2 Delta^-4 epsilon^-1
              log^2(T/epsilon) log^2(J/epsilon)).

This is a loose constructive upper bound, not optimal sample complexity.
There is no exponential factor in 1/Delta or d. If raw-copy acquisition has
cost C, multiply by C. Known controlled partial SWAPs use O(log d) gates
plus a synthesized angle: a SWAP-eigenvalue ancilla, controlled whole-register
SWAPs, a phase rotation and uncomputation suffice. Add the QFT, median and
comparison costs. Reserving epsilon/8 total trace distance for all gate
errors gives at most 5epsilon/8 overall. Divide that allowance by a hard
gate-count bound; no individual gate receives an uncharged fixed error.

Programs are streamed and consumed; retaining a batch requires T log d
output qubits, plus target, program and phase-estimation workspace. There is
no exponential-dimensional state table in the proposed physical algorithm.
The NumPy verification DOES use small dense tables and is not that algorithm.

## 6. Composition With The Research Receiver

Given a hard bound T on the entire receiver's ideal principal-state demand,
prepare the batch using a separate source-error allocation. Add its complete
output error to the receiver error. T must include all moment-design blocks,
discarded erasure-tree leaves, adaptive calls and known-character learning.
The existing ray-stabilizer orbit-gap gamma is still required and is distinct
from Delta. Neither source preparation nor this composition proves it.

For inverse-polynomial Delta this removes the earlier fixed-Delta sufficient
restriction. The original recursive SWAP route may have much smaller costs
at constant gap; this new loose bound is not a universal numerical improvement.
The Rees whole proof remains under review. Principal-state preparation is
useful without that theorem, but importing standard qPCA is not a new HSP
algorithm or an established Shor-level contribution.

## 7. Attempts To Falsify The Route

- CORRELATED PROGRAMS: a target and program jointly in a mixture of |00>
  and |11> have the expected marginals, yet controlled SWAP gives a different
  phase than independent programs. The exact finite countercontrol passes.
- DEGENERACY: filtering equal top eigenvalues does not select an unknown pure
  eigenvector. Flat coset projectors, including the noisy-coset/LPN source,
  are not repaired. Existing hardness boundaries are unchanged.
- FORGOTTEN OUTCOME: unconditioned ideal QPE leaves rho, not psi. The retained
  filter has success below one, and all attempts are paid.
- PHASE CONTROL: measuring/dephasing the control destroys its useful relative
  phase. Correct target marginals are not a valid controlled-channel test.
- CONDITIONING ERROR: a per-call approximation cannot simply be divided out
  after postselection. The complete instrument hybrid avoids that step.
- LOW GAP: exponential inverse gap still makes this inefficient. The planner
  does not convert log(1/Delta) input bits into cheap preparation.
- WRONG TARGET: coherent noise can change the principal vector and its exact
  symmetry. This does not recover an arbitrary unknown pre-noise state.
- CLASSICAL COMPARISON: explicit table, sparse, tableau, tensor-network or
  sample-and-query descriptions need their appropriate classical algorithms.
  Copy-only quantum data are not automatically comparable to a classical
  matrix input, nor do they establish a classical-input exponential speedup.

## 8. Verification And Handoff

Code implements exact rational budgets and finite physical channel/QPE checks,
NOT a full calibrated physical source or the HSP algorithm. `replay.py` emits
the actual scope, hashes, convergence controls and conservative budget examples.
Finite ideal QPE spectra are verifier inputs only, not promised online advice.

Verified: 42 new tests PASS; the combined normalizer, quotient, inverse-trace
residual and spectral-source suite has 140 tests PASS in 15.85 seconds. All
three new Python files pass py_compile, all receipt source hashes match, and
the whitespace check is clean. No full-repository suite, qsearch validation,
or UI check was run during the active migration; these results do not imply
that unrelated concurrent changes pass.

The physical three-dimensional QPE control uses a complex rotated eigenbasis.
For 224, 896 and 3584 consumed program copies, the complete instrument trace
distances from exact QPE are respectively 0.06160855, 0.01667134 and 0.00425667.
All target outcomes, including rejected ones, are included in that comparison.
This tiny experiment does not execute the conservative full source schedule.
For T=8, epsilon=0.01 and Delta=1/32 that schedule caps raw copies at
179023489419758823018048. Polynomial asymptotic dependence is not practical
performance; this bound is deliberately unsuitable as a hardware forecast.

Reproduction, from this folder with the local Anaconda Python:

```
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q test_spectral_source.py
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile spectral_source.py test_spectral_source.py replay.py
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py --output spectral_source_receipt.json
```

After migration is verified complete, Gemini can place this note with the
existing noisy-source audit, integrate the budget as an ALTERNATIVE source,
and port tests. Do not replace the constant-gap route blindly. No CLI, UI,
registry, Git or original-source changes are needed before that point.

The next scientific task is not a larger purification sweep. It is an actual
nonabelian principal-state task with proved spectral AND orbit gaps, or
independent review of the proposed Rees theorem. No new candidate should be
admitted solely because this preparation contract is now broader.
