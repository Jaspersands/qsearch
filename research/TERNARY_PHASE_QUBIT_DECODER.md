# Copy-Only Ternary Phase-Qubit Base Decoder

LOCAL CONSTRUCTION AND RANK DERIVATION / EXTERNAL REVIEW PENDING.
This is an executable fixed-exponent hidden-translation baseline and a sieve
endpoint. It is NOT a new polynomial growing-depth algorithm, a robust noisy
decoder, an oracle separation or a Shor-level candidate.

## Existing Source And Purpose

The preceding native-to-generalized-dihedral bridge supplies paid qubits

    |psi_k^s>=(|0>+exp(2*pi*i*sum_j k_j*s_j/m_j)|1>)/sqrt2.

At the ORDER3 character subgroup, k_j is a multiple of m_j/3 for each nontrivial
cyclic factor. With row u_j=k_j/(m_j/3), the unknown phase is omega^(u.s),
omega=exp(2*pi*i/3), and only s mod3 is probed. Trivial factors are dropped.
The terminal adapter checks actual public divisibility in powers of3; it
does not replace arbitrary high-root inputs by fictitious ternary samples.
Uniform independent terminal rows are a source/sieve output promise, not
proved by observing a finite batch of labels.

Polynomial algorithms for fixed-prime elementary abelian hidden translation
are established by [Friedl, Ivanyos, Magniez, Santha and Sen, Section3,
Theorem3.5](https://arxiv.org/abs/quant-ph/0211091). Their linear-inequation
lifting is the relevant known mechanism. This pass spells out a copy-only
three-outcome endpoint with affine quadratic lifting; no algorithmic novelty
is claimed. The paper's oracle-based zero/scalar checks are NOT imported as
free operations on our copy-only source.

The live original-source controls use native level1 qutrits projected through
the existing costed bridge, not a new hiding oracle. On that calibration source
direct qutrit Fourier measurement is STRONGER: it gives an exact linear
equation per copy. The present decoder is useful for binary phase inputs
emitted by a generalized-abelian sieve, not an improvement over that easier
native calibration. It must not enter candidate search as a new toy algorithm.

## Actual Fixed Measurement

For b inF3 define the anti-trine effects

    E_b=(1/3)*[[1,-omega^-b],[-omega^b,1]].

They are positive rank1, sum to I_2, and have a literal isometry

    V[b,:]=(1,-omega^-b)/sqrt3, V^dagger V=I_2.

Embed the supplied qubit in qutrit basis{0,1}, apply diag(1,-1,1), apply
inverse_F3, and measure b. This completes V to a known qutrit unitary, without
unknown preparation, inverse, cloning or extra secret-dependent gate settings.
For input phase omega^j, the probability of b is0 when b=j and1/2 otherwise.
Every paid copy gives an excluded value b DIFFERENT from u.s; no desired
measurement outcome is postselected or retried.

This receiver computes its actual Born law from the supplied density in the
reference simulator. Numerical amplitudes are not free classical input
access; the specified physical operation is the fixed isometry/measurement.

## Polynomial Classical Reconstruction

OverF3, exclusion means(u.s-b)^2=1. Let pairs(i,j) run over i<=j, and lift
unknowns to X_ij=s_i*s_j plus the linear secret entries s_i. The equation is

    sum_i u_i^2*X_ii + 2*sum_(i<j) u_i*u_j*X_ij
      + b*sum_i u_i*s_i = 1-b^2 mod3.

There are D=d*(d+1)/2+d lifted unknowns. Solve the resulting finite linear
system using exact F3 arithmetic, require FULL rank, require consistency,
and check every X_ij=s_i*s_j. The linear entries give s without enumerating
3^d hypotheses or resolving a scalar ambiguity with hidden oracle values.
Zero secret is handled by the same measurement/system, without an oracle test.

Insufficient finite inputs, deficient rank, contradictory exclusions and a
non-rank-one lifted answer return explicit NO RECOVERY statuses. A uniquely
consistent rank-one solution under violated source promises is not an external
verification of the true secret. The success statement below is CONDITIONAL
on the ideal source; the code does not prove that promise from its own data.

## Conditional Rank-Failure Proof

A nonzero dual of a lifted coefficient row has the polynomial

    Q(u)+b*w.u,

where Q is a homogeneous quadratic. If w!=0, uniform u has w.u!=0 with
probability2/3. Given such u, the two equally likely allowed b values are
distinct, and at most one makes the polynomial zero. Thus escape probability
is at least1/3. If w=0, Q is a NONZERO polynomial of total degree2 overF3;
the degree2 zero-count bound gives escape probability at least1/3. Diagonal
quadratics are not collapsed to linear functions overF3. Both arguments
apply for every unknown secret, including0.

For M independent ideal labelled measurements, each proper dual hyperplane
captures every row with probability at most(2/3)^M. There are(3^D-1)/2
projective dual hyperplanes. Therefore

    Pr[rank<D] <=(3^D-1)/2*(2/3)^M.

With M=3D+2h this is less than

    (1/2)*(8/9)^D*(4/9)^h <=2^(-h-1).

The report encodes the exact large expression compactly, not as a fitted
scaling curve or a floating approximation. Finite complete censuses cover
all nonzero dual polynomials and all nine secrets at dimension2. These check
the derivation, but do not replace the general polynomial-count proof.

Classical exact elimination has conservative O(M*D^2) field operations and
O(M*D) matrix storage. Logical quantum operations are one fixed measurement
per supplied binary packet. Hardware synthesis/error budgets are separate.
The native projection cap adds its own original copies and failure budget.

## Exact Noise Falsifier For THIS Decoder

Take independent phase-dephased inputs

    rho=gamma*|psi_j><psi_j|+(1-gamma)*I_2/2.

The anti-trine Born law is(1-gamma*cos(2*pi*(j-b)/3))/3. A FORBIDDEN outcome
b=j now appears with probability(1-gamma)/3. Such a row is false at the true
secret, because its quadratic left side is0 rather than1. Hence this strict
exact-equation decoder cannot correctly output the true secret if ANY
forbidden outcome appears, whether it aborts or finds another solution.

For fixed M, uniform independent equal-contrast inputs, define

    p_clean=((2+gamma)/3)^M.

Correct recovery is bounded ABOVE by p_clean and BELOW by
p_clean*(1-rank_failure_upper). Conditioned on all exclusions being valid,
the label law is still uniform and the two allowed b values are equiprobable:
the probability of being valid does not depend on u or the secret. No error
correction is silently claimed. Actual mixed-density countercontrols exercise
contradictory equations instead of assuming ideal residuals after noise.

This need not destroy the BASE case when1-gamma=O(d^-2), sinceM=O(d^2).
It pinpoints a more important issue: merging many original ancestors can
make gamma tiny before the endpoint, as shown by the preceding transport
audits. The bound is specific to this strict decoder, not a no-go theorem
for robust decoding, collective measurements or quantum hidden shift.

## Falsifiers And Next Work

- Literal qutrit isometry/measurement differs from the claimed exclusions.
- The linearized row uses a field shadow or wrong off-diagonal factor.
- The general rank escape probability fails, or rows are not IID as promised.
- An unknown secret/scalar check or unused fresh copy enters reconstruction.
- Original ancestors are measured twice or accepted without source budget.
- Contradictory/noisy equations are promoted to certified recovery.

NEXT: connect this endpoint to a PAID streaming generalized-abelian sieve,
track actual measured signs and source-law preservation, then compose packet
ancestry/noise rather than restarting ideal input at every level. A large
endpoint copy count or plausible rank behavior is not the missing breakthrough.

```
python theorems/ternary_phase_qubit_decoder.py --write
node research/certificates/ternary_phase_qubit_decoder_crosscheck.js
python -m pytest -q tests/test_ternary_phase_qubit_decoder.py
```
