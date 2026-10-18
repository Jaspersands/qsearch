# Coherent Coset Readout: Word Accuracy Is Not The Sampling Objective

2026-10-16. Known PGM/coset mechanism, locally derived composition identities
REVIEW PENDING, with actual gate-level finite controls. No new quantum
algorithm, classical-hardness proof, accepted candidate or active negative.

## Scientific Question And Prior Art

Can a public coherent decoder yield the Gibbs distribution without recovering
the entire transmitted codeword with high probability? YES for an exact global
coset PGM. This does not make that measurement efficiently implementable.

[Garrido-Chailloux Section 6, Proposition 8 and Theorem 12](https://arxiv.org/html/2605.03972v1#S6)
give the known normalized-coset PGM and its generally inefficient use in Regev's
reduction. Their stated construction postselects the cleared label. The local
character-source calculation below additionally factors the residual label,
so this binary positive-amplitude control does NOT require that postselection.
This calculation is not claimed novel or a new general sampling theorem.
[Zhou et al., discussion after Eq. 2.13](https://arxiv.org/html/2609.40345v1)
also warn that reliable-decoding/Holevo limits are not universal DQI limits.
Do not turn a sufficient codeword-error guarantee into a necessary gate on
every Gibbs algorithm, or transfer this observation to DCP secret recovery.

## Input, Mechanism And Costs

Public binary checks H have M columns, rank r and code C=ker H of dimension
k=M-r. G maps information words u to C, and public coordinate extraction F
satisfies FG=I. Spins x have one bit per row of H; energy is
T(x)=sum_j (-1)^(J_j+(H^T x)_j), with explicit sign vector J. Set c=tanh(beta)
in [0,1) and gamma=(1-sqrt(1-c^2))/2.

The actual source, on data Q, original label C and new record R, is

    2^(-k/2) sum_u (-1)^(J.G u) |psi_(G u),gamma>_Q |u>_C |0>_R.

It uses Ry, H, Z and generator CNOT gates. No sample/preparation oracle is
assumed. A public nondemolition decoder A acts only on Q,R. The conversion is

    A -> XOR R into original C -> A^dagger -> Z^J on Q -> H^M on Q.

Every register and every branch remains present. Measure the Fourier data,
solve H^T x=y, and sample uniformly over the affine solution fiber. The code
uses FLINT for that solve. Dependent checks, zero rows and gauge bits are not
rejected or projected away. Illegal Fourier support is counted as an abort
in total variation (TV). No resetting C or R is licensed by partial success.

Implemented decoder modes:

- `linear`: copy systematic information coordinates, an exact fully classical
  output-law baseline. This is NOT reliable decoding at arbitrary temperature.
- `local_pgm`: for each information coordinate choose the smallest containing
  check, use its public Fourier quotient and controlled Ry compression, copy
  the estimated bit, then undo the check transform. Repeat on the ACTUAL
  disturbed data, retaining every record; no independent fresh copies.
  Bounded check degree d gives public O(k poly(d) 2^d) primitive gates. This is
  NOT BPQM, an optimal global decoder, or its tree-to-block compilation.
- `global_pgm_reference`: compute all 2^M exact positive Fourier masses,
  change coordinates to (G^T y,y_pivots), unprepare each conditional pivot
  distribution using explicitly controlled Ry, Fourier-transform the syndrome,
  coherently record it, and reverse the transform. It is exponential, capped,
  and uses standard gates, not an opaque dense measurement or free PGM oracle.

Resource ledgers charge source, record/XOR/adjoints, final sign and Fourier
gates, M+2k wires, and the global mass table. Rotation angles are evaluated in
binary64 and decomposed into ideal Euler gates/CNOTs. Neither a fault-tolerant
gate count nor certified synthesis error is claimed. Simulations are capped
at M<=8, row count<=8 and M+2k<=20; a cap is UNKNOWN, not hardness.

## Why Global PGM Can Work Despite Word Errors

Let w_s be the Fourier part of the product amplitude in syndrome coset
G^T y=s, q_s=||w_s||^2>0, and v_s=w_s/sqrt(q_s). The known PGM basis is

    mu_d=2^(-k/2) sum_s (-1)^(s.d) v_s.

These vectors are orthonormal. In the original data basis include H^M on
each mu_d. Translation by G u sends mu_d to mu_(d+u), and

    <mu_d|psi_(G u)> = a_(d+u),
    a_t=2^(-k/2) sum_s sqrt(q_s) (-1)^(s.t),  sum_t |a_t|^2=1.

For the exact nondemolition rank-one measurement, A/copy/A^dagger clears R
and subtracts d from C. Write residual t=u+d. The resulting state factors:

    [2^(-k/2) sum_d (-1)^(s_J.d) mu_d]_Q
      tensor [sum_t a_t (-1)^(s_J.t) |t>]_C tensor |0>_R,
    s_J=G^T J.

The data bracket is H^M v_(s_J). After Z^J and H^M its positive amplitude
law is the product Fourier weight on y=J+H^T x, normalized over that coset.
Uniform affine-fiber lifting gives EXACT Gibbs probabilities. Word success
is only |a_0|^2 and need not be near one; it controls optional label
postselection, not this unconditional data law.

This argument uses a CHARACTER source, the exact orbit span, covariant
orthonormal projectors and their coherent implementation. It is not licensed
by a decoder's classical output probabilities, an arbitrary POVM dilation,
arbitrary phases, or correct one-bit marginals. Overlapping local projectors
need not realize that basis, and their disturbance must be executed.

More generally, a covariant orthonormal basis within this orbit span can give
the same data law up to syndrome phases even if it is not word-optimal. This
is a representation identity, not an efficient method for finding that basis.

## Decisive Finite Controls

Run `python theorems/coherent_local_gibbs.py --write`. The artifact is
`phase_workbench/coherent_local_gibbs.json`, bound to source/helper hashes and
Qiskit/NumPy versions. Every sign J is enumerated, without favorable selection.

At c=13/20:

| Public checks | Decoder | Mean TV | Worst TV |
| --- | --- | --- | --- |
| H=(111), M=3 | linear | 0.203886 | 0.650000 |
| H=(111), M=3 | local PGM | below 3e-15 | below 3e-15 |
| H=(00111,11100), M=5 | linear | 0.335946 | 0.668192 |
| H=(00111,11100), M=5 | sequential local PGM | 0.156530 | 0.339807 |
| H=(00111,11100), M=5 | exponential global reference | below 6e-15 | below 6e-15 |

The three-bit PGM word error is about 0.104315, while unconditional sampling
is numerically exact and data purity is one. Optional C=R=0 acceptance is
about 0.895685, explicitly NOT used. Thus requiring high word accuracy would
reject a correct sampling mechanism. Conversely, local measurements fail to
compose into the exact global measurement on the overlapping example.

Controls check full-Hilbert-space covariance, source amplitudes, every sign,
gauge/dependent rows, actual primitive gate counts, actual codeword errors,
and retained-workspace purity. Omitting the second sign phase or the adjoint
is an executed falsifier, even at gamma=0. These are small physical calibration
circuits for real explicit XOR Gibbs models, NOT oracle search candidates.

## Try To Kill It: Matched Classical Laws

The linear mode has a polynomial exact classical sampler for its ENTIRE
output. Draw independent b_j with Pr(b_j=1)=(1-(-1)^J_j c)/2, then set
y=(I-GF)^T b and solve H^T x=y uniformly. The finite exact rational shadow is
independently compared to the actual quantum joint output, not just a score.

The global reference is also classically matched: condition the independent
positive Fourier bits on G^T y=G^T J. The SAME explicit prefix-mass ratios
used for its controlled rotations sample that conditional distribution
classically, then solve H^T x=y+J. The implementation includes exact rational
random draws, plus an independent integer-factor Gibbs reference. No advantage
survives when those tables are materialized or freely supplied to both sides.
This refutes an advantage claim for THIS construction, not all PGMs or DQI.

## Revised Constructive Target And Falsifiers

The unresolved question is an efficient coherent normalized-coset transform
on a classically difficult explicit family, NOT universally vanishing whole-
codeword error. A meaningful candidate must specify its public gate program,
native family, all-sign or stated random-sign guarantee, data fidelity/TV,
precision, total source/measurement work, and an asymptotic cost argument.
No such new candidate has been found in this pass.

1. Implement a genuine finite-block BPQM/coherent reliability-register circuit
   and test its unconditional coset readout, not only bit error. Keep the
   existing exact factor, affine-cluster and tempering baselines live.
2. Ask whether a phase-aware quantum transform can approximate the normalized
   coset vectors without computing positive classical prefix partition sums.
   Merely calling a generic PGM, matrix inverse square root, or Gibbs-state
   preparation routine assumes the missing algorithm.
3. If a circuit compiles from tractable positive prefix masses or low-width
   sum-product messages, immediately implement the matched classical sampler.
   Exactness on independent checks or Tanner trees is not a separation.
4. Falsify a proposed composition by retained-workspace mixedness, nonvanishing
   unconditional TV on its actual ensemble, exponential lookup/precision/
   repetition cost, or an equally fast sampler for its complete output law.

Do not extend this into a blind sweep of local measurement orders, bigger
dense PGMs or another catalogue of barriers. An overlap-aware construction
needs a reason it removes the observed composition error before more scans.
