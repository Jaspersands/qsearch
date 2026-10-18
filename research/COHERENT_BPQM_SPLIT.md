# Cyclic BPQM With Paid State Splitting

2026-10-16. Known ENU/computation-tree mechanism executed on a native cyclic
code. Finite physical falsifier, not a new algorithm or general impossibility
result. No accepted candidate, central negative or proof-status promotion.

## Hypothesis And Prior Art

**Question:** can an actual split-channel computation tree fix cyclic-code
coset readout, rather than treating duplicated outputs as fresh inputs?

**Problem/input:** explicit binary checks H, signs J and overlap c=tanh(beta),
with the actual coherent codeword source and Gibbs task from
[coherent coset readout](COHERENT_LOCAL_GIBBS.md). No secret-dependent unitary,
quantum sample oracle, repeated unknown-state preparation or fiber advice.

**Mechanism:** unroll the native Tanner graph to a finite tree per information
coordinate. When a native coordinate occurs m times, unitarily split its
received channel into m weaker outputs with conserved product overlap. Apply
the known BPQM tree circuit with those weaker reliabilities, copy the root,
and reverse both tree and splitting. Compose on the actual disturbed joint
state and execute the full decoder/XOR/adjoint Gibbs readout.

[Piveteau-Renes Section 6](https://arxiv.org/pdf/2109.08170) already introduce
the equality-node-unitary (ENU) splitter, computational unrolling and reduced
quality with deeper cloning. Their comparison is decoding a supplied CQ
channel, not a proof of superiority over classical Gibbs samplers. Here the
known mechanism is tested in the repository's complete sampling circuit.

**Desired advantage, NOT established:** polynomial total native-source/gate
cost and vanishing unconditional sampling error on a cyclic family beyond
strong matched classical sampling methods. This pass establishes no scaling
law or numerical probability that this target will be achieved.

## Legal Splitting, Not Free Copies

For the Fourier-basis pure-state pair

    |s_x(c)>=sqrt((1+c)/2)|0>+(-1)^x sqrt((1-c)/2)|1>,

the adjoint equality-compression circuit maps

    |s_x(ab)>|0> -> |s_x(a)>|s_x(b)>.

This is an isometry on the WHOLE input qubit, not a separately phased map
for two basis labels. Inner products are conserved: overlap a*b on the output
equals the input overlap. Two same-quality NONORTHOGONAL copies would instead
have overlap c^2 and are not supplied. Orthogonal known-pair states at c=0
may be copied; that is not arbitrary-state cloning.

For rational c and m>1, choose a dyadic upper m-th root a by exact integer
comparison. The first m-1 outputs have overlap a; the final one has overlap
c/a^(m-1). Their product is EXACTLY c, and every output overlap is >=c, so
none is more informative than the input. This avoids silently rounding an
irrational root into an impossible isometry. At very coarse resolution, some
outputs may be wholly uninformative with overlap1; those are not fresh inputs.
The finite circuit handles that endpoint explicitly. Do not apply the earlier
finite-log arithmetic contract to atanh(1) without a separate endpoint encoding.

Public two-qubit controlled-Ry/CNOT equality adjoints implement each split.
The tree compiler now accepts heterogeneous signed overlaps and an explicit
already-Fourier-input flag. Its finite compile cap is10 physical tree outputs;
the native readout still caps8 original outputs and20 total retained qubits.
Caps yield UNKNOWN, not a hardness claim. Angles are binary64, not certified
fault-tolerant synthesis.

## Workspace And Native Correlations

Each information-root measurement has PRIVATE split ancillas initially zero.
Undoing its unitaries around a recorded root estimate need not restore those
ancillas to zero. They remain in the joint state, and later roots receive
different fresh ancillas. The final decoder adjoint uses every retained one.
No reset, garbage erasure, hidden postselection or fresh-native-copy claim.

The readout engine now traces all split work only at the END. It reports
native data purity, split-zero probability, full label/work-zero acceptance
and unconditional TV including illegal-support aborts. Gate ledgers include
all split operations and inverses, source, records, sign and Fourier gates.

Duplicated variable labels remain equal in the actual native source. The
native code embeds into a PROPER SUBCODE of the relaxed unrolled tree code.
Known BPQM is optimal for the full tree ensemble; it is not automatically
optimal for that native subcode. Fixed-codeword bit-error guarantees can still
be valid by covariance, but do not establish native orbit-span preservation
or the correct Gibbs law. Restoring every equality between repeated variable
labels generally reintroduces the loops that unrolling removed.

## Decisive All-Sign Experiment

Run `python theorems/coherent_bpqm_split.py --write`.
Artifact: `phase_workbench/coherent_bpqm_split.json`, source/helper/version
bound, including every sign case and exact native classical target laws.

Native H=(0111,1101), M=4, rank2, has a genuine Tanner cycle. There are two
Gibbs spins. It is deliberately a tractable physical calibration, not a toy
oracle problem or evidence about the random regular(3,6) hard regime.

| c | Depth | Mean TV over all16 signs | Worst TV | Word error |
| --- | --- | --- | --- | --- |
| 1/5 | 0 | 0.107102 | 0.130909 | 0.020102 |
| 1/5 | 1 | 0.018305 | 0.024845 | 0.001156 |
| 1/5 | 2 | 0.021795 | 0.044470 | 0.007715 |
| 13/20 | 0 | 0.303722 | 0.536250 | 0.225658 |
| 13/20 | 1 | 0.083148 | 0.153685 | 0.099105 |
| 13/20 | 2 | 0.160201 | 0.227198 | 0.198709 |

Depth0 reproduces the linear baseline. Depth1 gives a finite improvement;
depth2 makes both tested temperatures WORSE on average. Deeper unrolling is
not a convergence argument. No favorable sign/source selection was used.

At all-positive J,c13/20, split-zero probability falls from0.996849 at depth1
to0.885821 at depth2; data purity falls from0.931232 to0.795529. This is actual
retained workspace, not a freely cleared register. Legal native Fourier
support is preserved numerically, but support alone does not imply Gibbs.

| Depth | Retained qubits | Ideal one-qubit gates | CNOTs |
| --- | --- | --- | --- |
| 0 | 8 | 50 | 11 |
| 1 | 9 | 1834 | 951 |
| 2 | 16 | 13170 | 8035 |

Counts are the complete all-positive-sign source/decoder/XOR/adjoint/readout,
unsimplified, with no universal-gate synthesis certificate. Depth2 allocates
5 and3 private ancillas to the two roots, not one reused5-qubit pool.

For comparison, the existing exponential global PGM reference on this native
code has word error about0.069481 at c13/20 and numerically correct Gibbs
readout. Calling that measurement an oracle would assume the hard step; it
materializes16 masses here and does not give a scalable algorithm.

## Try To Kill It: Strong Classical And Physical Controls

The original native Gibbs family is classically EASY. Its exact integer-factor
sampler uses at most4 entries per factor,21 cumulative entries and2 uniform
integer draws per output in this example. Every quantum output is compared
against the original native distribution, not an easier relaxed tree target.
The artifact includes the full exact classical probabilities for both
temperatures and all16 signs. No quantum advantage survives this comparator.

Independent tests verify exact rational overlap conservation, actual two-qubit
isometry/covariance, coherent complex superpositions, every lifted native
codeword's parity constraints, and agreement of native split circuits with
the properly CORRELATED lifted product states. They check private workspace,
its nonzero population after readout, gate/wire counts and full artifact replay.
The ordinary tree still refuses uncharged repeated quantum inputs.

## Targeted Mutation: Does Spectral Sharpening Repair The Receiver?

A plausible public-access variation is to compress the actual split root
reflection into its initial-zero workspace:

    O_eff=<0_split| U_root^dagger Z_root U_root |0_split>.

The root circuit and zero-workspace projector are public, so this supplies a
legitimate block encoding without a secret-dependent measurement oracle.
[Quantum singular value transformation](https://arxiv.org/abs/1806.01838)
provides a framework for polynomial spectral transformations. A sign-based
variation would also need gap, approximation, controlled-call and clean-work
resource arguments. None are granted as an implemented algorithm here.

Before building it, we grant the STRONGER, counterfactual perfect sign(O_eff)
and test whether its native eigenvectors are even right. This is a capped
dense diagnostic, explicitly NOT a QSVT circuit or a usable ideal decoder.
The independent tests are in `tests/test_coherent_bpqm_split_sharpening.py`.

At c13/20, depth1:

- Root2 has min absolute eigenvalue0.787670, so its finite spectral gap is
  benign. Sharpening improves bit error0.060529->0.058799, but the norm of
  leakage out of the native code orbit INCREASES0.207057->0.215216. These
  are Frobenius norms on an orthonormal orbit basis, not probabilities.
- Root3 is ALREADY a reflection: sign changes it only by numerical roundoff.
  Its orbit-leakage norm remains0.692074 and bit error0.069544, versus the
  native Helstrom optimum0.027579. Eigenvalue-only sharpening does not rotate
  its incorrectly aligned subspaces.
- Granting BOTH perfect sharp reflections and executing the full coherent
  source/XOR/adjoint readout over ALL16 signs gives meanTV0.089723 and
  worst0.157143, slightly WORSE than the actual depth1 mean0.083148.

Thus accurate sign approximation alone does not repair this receiver: its
intended perfect-sign limit is still biased. The failure is not explained
by a tiny finite gap or inadequate sign-polynomial precision. This does NOT
exclude different operators, loop-aware eigenvector construction, joint
noncommutative transformations, other cloners or QSVT-based algorithms.
Do not implement a sign compiler for this specific receiver on the assumption
that it supplies the missing native coset transform.

## Revised Decision And Remaining Obligations

The tested shortcut is not an exact cyclic coset transform. More unrolling
at the same fixed temperature is not justified as a monotone improvement.
This is a falsifier for THAT expectation and those specified instances, not
a no-go for other cloners, schedules, BPQM families or quantum algorithms.
Do not turn it into a broad registered negative or extend into blind depth,
allocation or sign scans. Low fixed-size bit error is not an asymptotic result.

A new constructive variation needs a reason it preserves/approximates the
NATIVE normalized coset orbit despite the relaxed-tree embedding, a total
error bound after all measurements and reversals, and a paid scaling argument.
It must also survive the original factor/cluster/tempering baselines. The
explicit herald-angle tables remain an exponential implementation issue;
the log-reliability contract does not itself compile them away.

Next research should compare an explicit overlap-aware rule with independent
high-upside mechanisms before returning here. Gemini may integrate the
standalone producer into CLI/EXP and perform bulk regression, preserving all
scope/cost/UNKNOWN flags. No GPT commit or push is part of this pass.
