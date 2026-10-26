# Unconditional Ternary Decoding To Constrained-Product Sampling

2026-10-20. LOCAL REDUCTION DERIVATION / INDEPENDENT REVIEW PENDING.
Known Fourier/coherent-decoding paradigm, not a novelty or speedup claim.
This pass implements the full bounded gate sequence and supplies an explicit
general error argument. The growing random-LDPC receiver remains uncompiled.

## Scientific Question

The signed-trine BPQM certificate supplies a concrete success-region premise
for a known q-ary decoder. Does a small decoding error actually give a sampler
for the ORIGINAL ternary sparse-constraint input, without postselecting labels,
changing the source, granting its inverse, or normalizing an impossible target?

Answer: the following unconditional construction does, in average total
variation over independent uniform offsets, IF the required known coherent
decoder is implemented. A bounded actual qutrit BPQM decoder executes the
construction below. This is not yet a large-instance implementation.

The paradigm is related to the existing
[binary DQI sampling reduction](https://arxiv.org/html/2609.40345v1#S3) and
the repo's ternary decoder/filter audit. The binary theorem is not itself a
theorem about our signed q-ary source. The local argument below makes that
connection directly, with a conservative constant and explicit empty targets.

## Problem And Circuit

Let H in F_q^(V x M) be public, q prime, and let C=ker H have dimension k.
Rows of G are a public basis of C; d_u=uG for u in F_q^k. No independence or
full row rank of H is required. Use a KNOWN normalized product amplitude
phi(y)=product_e sqrt(mu_(e,y_e)), with easily prepared local distributions.
The implementation specializes to q=3 and equal local mu.

Given original public J in F_q^M, the target spin law is

    P_J(x) proportional to p(J+H^T x),    p(y)=|phi(y)|^2.

For mu=(0,1/2,1/2), this is UNIFORM over the original solutions with every
entry of J+H^T x nonzero. For the dv3/dc6 socket ensemble, each constraint has
at most three nonzero terms, M=2V. Parallel sockets and zero/dependent rows
remain. This is not a changed dense IID matrix or a graph-cycle ensemble.

Write psi_u=sum_y phi(y)*chi(d_u.y)|y>, N=q^k. A known UNITARY circuit A acts
on data, a k-trit estimate R, and optional workspace W initialized to zero.
The SAME A depends on H and mu but is INDEPENDENT of the offset J. This is
essential for the character average below; a J-adaptive receiver needs a
different analysis. The implemented BPQM decoder is built once before the
offset loop and meets this condition. Its mean word error is
delta=E_u Pr[estimate !=u]. If a decoder instead
outputs a full codeword, take its information coordinates reversibly; correct
whole-word decoding implies correct information-word decoding.

1. Prepare the normalized physical input

       N^(-1/2) sum_u chi(-d_u.J)|u>_L |0>_R |psi_u>_D |0>_W.

   This uses local product rotations, Fourier gates on L, and PUBLIC
   bilinear controlled phases from G. No coset mass, unknown parameter,
   normalized conditional state or source-preparation oracle is used.
2. Apply A to D,R,W. Subtract the estimate from L MODULO q. Apply the ACTUAL
   circuit adjoint A-dagger to D,R,W. Retain EVERY work/label register.
3. Measure data y. If p(y)=0, abstain. Otherwise solve H^T x=y-J by public
   Gaussian elimination. If inconsistent, abstain; otherwise lift uniformly
   over its affine kernel and return x. Never repeat a failed branch for free.

The implementation includes the actual polynomial FLINT Gaussian chart and
the explicit uniform gauge coins. It handles dependencies and zero columns.
An abstention is NOT a certificate of UNSAT. The algorithm never asks whether
the original nonlinear problem is satisfiable before executing these steps.

## Error Proof, Including Empty Inputs

For each fixed u, let v_u be the output of A/subtract/A-dagger starting from
|u>_L|0>_R|psi_u>|0>_W, and let
t_u=|0>_L|0>_R|psi_u>|0>_W. Both have norm one. Their inner product is the
decoder's REAL correct-estimate probability: projecting the subtracted L onto
zero selects exactly estimate u, and A-dagger cancels A in the overlap.
Therefore, EXACTLY,

    ||v_u-t_u||^2 = 2*delta_u.

For the offset-dependent actual state a_J and comparison vector b_J,

    a_J=N^(-1/2) sum_u chi(-d_u.J)*v_u,
    b_J=N^(-1/2) sum_u chi(-d_u.J)*t_u.

The first is normalized by the unitary preparation/circuit. The second is
generally NOT normalized. Distinct d_u give orthogonal characters over
UNIFORM ORIGINAL J in F_q^M, hence Parseval gives

    E_J ||a_J-b_J||^2 = 2*delta.                       (1)

No IID columns of H, rerolled right-hand side or favorable code instance is
needed. Only the stated independent uniform offsets are averaged.

Character orthogonality in u also gives the explicit comparison vector

    b_J=|0,0,0_W> sqrt(N) sum_(Gy=GJ) phi(y)|y>.
    z_J=||b_J||^2=N sum_(Gy=GJ) p(y).

This vector is an ANALYSIS object. It is NOT supplied as a prepared input.
The bounded checks include z=0,9/8,9/4 for the native source. Replacing it by
a normalized input would silently manufacture the sampler being sought.

If z_J>0, its normalized data law is p conditioned on y in J+rowspan H.
Every y has q^(V-rank H) spin lifts. The same uniform Gaussian lift therefore
gives exactly P_J. Set d_J=||a_J-b_J||. Reverse triangle bounds
|sqrt(z_J)-1|<=d_J, so

    ||a_J-b_J/sqrt(z_J)|| <= 2*d_J.

Measurement and classical postprocessing contract trace distance. Thus the
unconditional output TV, including its abstention outcome, is at most
min(1,2*d_J). If z_J=0, no supported y can lift, so the actual algorithm
abstains with probability one; for bookkeeping the empty target is also
ABSTAIN. This does NOT give an UNSAT oracle, since nonempty targets can also
produce abstentions. Cauchy--Schwarz and (1) yield

    E_J TV(actual_J,P_J_extended) <= min(1,2*sqrt(2*delta)).       (2)

The same proof bounds the empty-offset probability by 2*delta, though that
is not the sharp rank bound. The guarantee is average-J, NOT worst-case J.
Markov gives Pr_J[TV>epsilon]<=2*sqrt(2*delta)/epsilon. If a code ensemble
has E_H delta_H->0, Jensen extends (2) to that ensemble with E_H delta_H.

Source-preparation trace error eta_source, operator-norm decoder error
eta_A (and the adjoint of that SAME approximate circuit), and TV gauge-lift
error eta_lift add at most eta_source+2*eta_A+eta_lift to the bound. These
are TOTAL errors of the relevant subroutines, not per-gate allowances.
No finite-block error or angle-precision budget is claimed from the examples.

## Actual Bounded Coherent Receiver

The calibration code is the native three-wire single-check code, not a
proposal for a toy algorithm. It is trivially solvable classically. Its role
is to audit the general circuit and phases before attempting a large receiver.

For each information coordinate, the reference actually compiles:

- Public coefficient-frequency permutations, then the two-qutrit SUM-check
  gate on the other two physical outputs. The herald stays coherent.
- A herald-controlled same-symbol Householder compression using the exact
  conditional spectrum. Even impossible source heralds get a TOTAL unitary
  completion on the dark subspace; they are not removed from the circuit.
- An inverse F_3 on the root, a MODULAR SUM copying its estimate, followed by
  the root-transform adjoint. Sequential coordinate instruments form A.
- A, source-label subtraction, and A-dagger are then executed in the complete
  sampling circuit. No Helstrom/PGM table, orbit reflection or coset-probability
  oracle provides this receiver. Dense matrices are the bounded compilation
  of those listed local gates, not a scalable simulator.

Source preparation itself is executed from a blank with local rotations,
label Fourier gates and public G-controlled phases. Tests separately compare
it to the independent formula. The target/coset census is never an input to
the circuit. The finite histogram over all gauge coins/targets is exponential
verification; the actual affine point lift is polynomial and also tested at
32 spins/64 equations, independently of the quantum-reference cap.

## Results And Attempts To Disprove It

Seven correct-adjoint cases retain ALL27 original offsets each. Native,
unequal full-support and perfect sources, signed checks, dependencies, zero
rows/columns, and a product/no-decoder reference are included. These are
finite controls, NOT source selection or experiments on large LDPC instances.

- Native BPQM: word error about0.43704639; average TV about0.19444444,
  or0.25 over NONEMPTY targets. Empty fraction is2/9. Unconditional valid
  native-output probability is7/12. The generic word-error TV bound is
  VACUOUS here, despite the exact error identity. No reliable decoder claim.
- A known constant shift of the decoder output raises word error to about
  0.96679827 but preserves the ENTIRE measured-data distribution. The source
  label absorbs the shift. Word error is sufficient, NOT necessary for useful
  sampling; do not use it as a universal obstruction.
- A deliberately WRONG adjoint preserves total probability but violates (1)
  by about0.98093635. Norm/herald checks alone would miss this error.
- Full-support mu=(1/4,3/8,3/8) is a DIFFERENT target. Its small-control word
  error is positive while readout matches the weighted target numerically.
  This is a nonvacuous-bound calibration, not free extra copies or a rescue
  of the original zero-temperature problem. The perfect channel is likewise
  only a classically easy control.

## Classical Competitors And Scope

Do not compare only against the weaker no-decoder baseline. Both of these
public proposals are polynomial per attempt and exactly correct CONDITIONED
on acceptance, but this does not make their acceptance free:

1. Sample product y~p and Gaussian-lift y-J if consistent. This is EXACTLY
   the entire no-decoder circuit's output law. Mean acceptance over uniform
   J is q^(-k). The native bounded case has probability1/9.
2. Sample ORIGINAL spins x uniformly and accept with probability
   p(J+H^T x)/max(p). Its mean acceptance is (1/(q*max(mu)))^M for our equal
   local source, which is (2/3)^M natively. The same bounded case has8/27,
   stronger than1/9. Its accepted native samples are genuinely uniform.

At M=2V both elementary native acceptance rates are exponential, but this
is NOT a classical lower bound. SAT search, local/block Gibbs, algebraic
solvers and tensor-network/approximate counting methods remain serious
competitors. The earlier native Z3 witness/timeout results remain calibrations,
not sampling guarantees or hardness evidence. No DCP, LWE or cryptographic
attack follows from this sparse ternary ensemble.

## What This Removes And What Remains

Classical follow-up: TERNARY_CLASSICAL_SAMPLING.md now solves uniform sampling
on both saved native16/32 inputs by complete SAT enumeration, while retaining
the UniGen timeout. It also derives the conditional annealed-count predictor
and explains why quiet planting is not a prescribed-input sampler. These
finite inputs cannot support an advantage claim. The general asymptotic
conditional-sampling question is not settled by their finite exact pools.

The missing Fourier/sampling connection now has an explicit all-input-matrix,
average-offset argument and an actual bounded gate implementation. Combined
with the signed-trine convergence premise and the cited q-ary block theorem,
it identifies a CONDITIONAL asymptotic sampler for the stated sparse ensemble.
All local derivations and the use of the preprint theorem need independent
review. Known DQI/Regev methods may already imply the same consequence; no
novelty claim is made.

The algorithm wrapper uses polynomial public linear algebra, O(kM) public
source-phase operations, one A and one A-dagger, a k-trit subtraction and a
polynomial affine lift. It has no herald-retry loop. Data/label/estimate size
is M+2k plus the receiver's workspace. A growing, precision-paid A is still
the principal implementation obligation, not a source/coset oracle.

NEXT: first audit stronger classical UNIFORM samplers and approximate counting
on the same native ensemble before spending a pass on a large receiver.
The constructive implementation task is coherent reliability/receiver
arithmetic without huge angle tables and with paid precision. Do not collect
more small success curves, finer DE plots or
generic Gram-access variants. No candidate/proof/negative/preprint promotion
is authorized by these bounded checks.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python theorems/ternary_decoded_sampler.py --write
    python -m pytest -q tests/test_ternary_decoded_sampler.py

Live artifact: research/reductions/ternary_decoded_sampler.json. CLI exposure
and routine registry wiring remain Gemini tasks in the mechanical handoff.
