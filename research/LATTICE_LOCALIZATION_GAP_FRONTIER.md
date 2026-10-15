# Public Localization Noise/Gap Frontier

This is a conditional source-planning theorem and public classical attack
experiment, not a quantum solver or a claim of a new lattice reduction.
The localization architecture already appears in the cached Regev paper;
see LATTICE_SINE_WINDOW_SOURCE.md for the implemented finite instrument.

Run `python qsearch.py lattice-localization-gap-frontier`.
Artifact: `research/classical_baselines/lattice_localization_gap_frontier.json`.

## Public Family and Trial Selection

Assume a planted primitive vector u has ALL n coordinates in {-1,+1}, in a
public q-ary kernel with m constraints. Its norm squared is n. In the public
centered-RREF row basis, EVERY free basis coefficient is +/-1. Therefore
the first free basis row j=m is a public hitting coordinate. With recovery
up to sign, residue g=1 needs one trial, not a private hitting-coordinate
selector. This statement does not extend to arbitrary sparse plants.

Write r=n-m and let B(r) be the modulus-uniform ternary pivot envelope from
PLANTED_QARY_CUBE_BASIS_COORDINATE_BRIDGE.md. On this trial, the parent
displacement satisfies |h_j|=0 and

    ||h||_1 <= L = r-1 + m B(r).

Use public dimensions alone to schedule M=2^b. For constant noise set
epsilon=1/8; for inverse-log noise set epsilon=1/[n(b+1)]. Increase b from
one until L/M<=epsilon/2. The search terminates because exponential M
dominates the linear b term. This same M is used for both localization
comparators; there is no private norm/support estimate in the schedule.

## Matched Cube and Sine Budgets

Cube localization has intended-partner loss at most n/W. Choose dyadic
W>=2n/epsilon. Sine localization has loss at most
(pi^2/2)n/K^2 < (242/49)n/K^2. Choose dyadic
K^2 >= (484/49)n/epsilon. Adding L/M gives total loss at most epsilon.
The rational pi upper bound uses pi<22/7; exact packet validation is separate.

For dense ternary u, the sufficient relative nonparallel gap G=side gives
lambda2>side*sqrt(n) under the uniqueness promise. Prime p=nextprime(side+1)
also satisfies p-1>side, excluding the unwanted collinear aliases using the
conservative sine-window conditions. These are CONDITIONAL implications;
parameter arithmetic does not certify a lattice's successive minima.

At constant epsilon, sine requires sufficient gap O(sqrt(n)) versus the
cube bound O(n). At epsilon=1/log(N), b=O(log n), giving sine sufficient
gap O(n sqrt(log n)) versus cube O(n^2 log n). These compare these specific
product localization budgets, not optimal known lattice reductions. Rounding,
public arithmetic widths and original-source preparation costs remain paid.

Constant noise is NOT silently substituted for the inverse-log bad-register
promise. It still needs a robust EFFICIENT unknown-copy receiver. Existing
information-theoretic or exponential likelihood decoders do not supply one.

## Kill the Apparent Signal First

Generate dense-ternary q-ary instances with the sine schedule's smaller gap.
Use the existing exact field/rank/index generator and its distributional
uniqueness ledger. Do not filter seeds on recovery or uniqueness outcomes.
Give only PublicQaryLattice to sparse-column and exact-Gram FLINT LLL attacks.
Only afterward compare their outputs with the private plant, up to sign.

Each recovered control produces a scoped finite classical falsifier with the
public problem fingerprint. Non-recovery is unresolved, not hardness. A
distributional gap estimate is not individual-instance certification. BKZ,
general SIS attacks, asymptotic hardness and an efficient receiver remain
unresolved. The public source resource estimates are NOT compiled or sampled
large quantum circuits. No source preparations or quantum solver calls occur
in this experiment.

The sweep covers n=16,32,64, both noise modes, and a second independent n32
seed. A separate parameter-only table extends to n512. Do not mistake that
table for executed classical attacks or quantum simulations.

## Executed Result

All eight controls were recovered by public FLINT LLL. The sine versus cube
side/gap schedules at n64 are128 versus1024 for constant noise and1024
versus262144 for inverse-log noise. This substantial conditional improvement
in source parameters did NOT make the tested instances classically resistant.
The exact independent JavaScript checker verifies the public field/RREF/kernel
index and unimodular LLL certificates, then checks the private recovery
calibration separately. This is a finite hardness falsifier, not a theorem
that every lower-gap lattice family is easy.

Next research must address the source distribution/classical attack boundary
or the efficient unknown-copy receiver. Merely increasing dimension, retaining
more trials, or adding another known-phase Fourier mixer does not resolve
either obligation. Central experiment/proof/negative-ledger integration and
full production regressions remain mechanical Gemini/Antigravity follow-up;
the standalone CLI, live artifact and targeted tests are implemented here.
