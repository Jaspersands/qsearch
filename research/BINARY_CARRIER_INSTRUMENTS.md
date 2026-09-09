# Binary Carrier Instruments: Outcome Laws Before Scores

This extends the existing collective carrier-instrument calculations to
**binary class-versus-trivial detection**, not hidden-member identification.
It is a calibration and falsification workbench. No three-copy candidate or
new scalable algorithm is proposed.

Run `python qsearch.py coset-binary-carrier-instruments` or
`python qsearch.py run EXP-COSET-BINARY-CARRIER-INSTRUMENTS`.
The artifact is `research/representation/coset_binary_carrier_instruments.json`.

## Physical Evaluation

Three source labels lambda_1,lambda_2,lambda_3 are included in the output.
The unnormalized informative Fourier blocks are

    null: product_i(d_i/|G|) I,
    alternative: product_i(d_i/|G|)
                 * (1/|C|) sum_(h in C) tensor_i(I+rho_i(h)).

The same h occurs in every input. All source triples are enumerated with
their physical weights, including zero-probability outcomes. No block or
measurement branch is renormalized, and no favorable source is postselected.
Nonfinite probabilities, significant negativity and missing outcome mass
cause failure rather than silent normalization.

`L` and `R` are the existing left/right pair-irrep projective measurements.
`T` measures the total three-input irrep. These are representation-theoretic
instruments, not arbitrary tiny-circuit mutations. Each is evaluated by its
Luders map, rho -> P rho P, with outcomes retained. Dense matrices are the
finite evaluator, not a claimed scalable implementation of these primitives.

For every schedule the report separates:

- Total variation of the classical carrier transcript.
- Total variation after a final fixed Young-row readout.
- Trace distance of the still-retained quantum state, with transcript flags.
- Information irreversibly lost from the raw physical binary ensemble.
- A product-basis dephasing/Markov ablation, with dense simulation cost exposed.

The first two scores use an optimal likelihood table unless an explicit
decision rule is supplied. Such a table is NOT automatically an efficient
classifier. Retained quantum trace distance likewise assumes an optimal
future measurement; it is not a readout the program implements.

## One Explicit Decision Rule

Write r_lambda=chi_lambda(h)/d_lambda. After source labels and one `L`
pair label alpha, the exact likelihood ratio on positive null mass is

    (1+r_lambda3) (1+r_lambda1+r_lambda2+r_alpha).

Accept the hidden-class alternative if this exceeds one. The `R` formula
permutes the unused source. This follows by expanding the two coset factors
inside the pair projector and tracing the unused third factor. The evaluator
checks the formula against every physical source/target probability.

Character evaluation and pair-label measurement access remain explicit
resource contracts. This formula does not extend to arbitrary overlapping
sequences by multiplying character ratios.

## Apparent Gain, Then a Stronger Baseline

For S4 perfect matchings with three inputs, raw trace distance is 21/32.
The first `L` measurement reduces retained trace distance to 59/96, losing
1/24 irreversibly. Carrier transcript scores increase with `L`, `LR`, `LRL`:
approximately 0.421875, 0.560764, 0.576534. They beat the deliberately weak
product-dephased ablation. That alone is not useful evidence.

The stronger baseline exactly reproduces **every output probability**, not
just these scores. In all S3/S4 source triples, both coupling trees satisfy

    g(lambda1,lambda2,alpha) g(alpha,lambda3,nu) <= 1

and the analogous right-tree condition. The joint projector
J_(nu,alpha)=P_nu P_alpha therefore has physical rank d_nu whenever nonzero.
Because both binary states commute with the diagonal group action, after
observing alpha and conditioning on latent nu their normalized quantum state
is J_(nu,alpha)/d_nu, independent of the binary hypothesis.

Switching pair bases has transition probability

    Pr(beta | nu,alpha) = Tr(J_(nu,beta) J_(nu,alpha))/d_nu.

The total label nu is a fixed latent variable. All hypothesis dependence is
in the initial distribution over nu and the first pair label. Subsequent
alternation is an ordinary hidden Markov model; final Young-row probabilities
are classical emissions diag(J_(nu,alpha))/d_nu.

The workbench replays all tested L/R transcripts and final row outcomes
under both hypotheses across **all 152 source triples**. Maximum probability
residual is below 1e-15. Measuring `T` after one pair exposes the latent
label directly: `LT` and `RT` attain the entire post-first-measurement
retained distance. The apparent alternation gain is learning a label that
the earlier readout omitted, not evidence of a new scalable mechanism.

This is a **quantum front end plus classical postprocessing** equivalence.
The initial distribution over (nu,alpha) depends on the unknown binary
hypothesis. The replay is given that distribution; operationally the joint
quantum label measurement supplies a sample. No legal classical procedure
for obtaining that initial sample from the original problem input has been
provided. A generative model given the hypothesis is not a classical solver
for an unknown hypothesis. The result removes the need for subsequent
alternating quantum instruments in these finite cases, not the quantum
front end itself.

## Why This Is Not a General Classical Simulation

Transition construction here uses finite dense projectors. Its classical
cost is not asserted polynomial for growing n. More importantly, the rank-one
condition fails: in S6, g((4,2),(4,2),(4,2))=2, giving joint multiplicity four
on a three-source path. A scalar latent-state model then need not capture
the remaining multiplicity density matrix.

This exact nonextension witness is NOT a positive algorithm result. Its
natural source-triple mass for fixed-point-free involutions is only 27/8000;
the actual pair/total target-branch mass is not computed in this certificate.
Neither dimension nor surviving matrix-valued state implies useful binary
signal, an efficient classifier or a quantum-classical separation.

## Uniform Copy-Budget Gate

Let M=(2m-1)!!, and consider at most t fresh b-copy block measurements.
Each complete POVM must commute with simultaneous G conjugation, and only
classical history is retained between blocks. The instruments may be
chosen adaptively from that history.

For every transcript outcome its probability is identical for all h in the
class. Thus the posterior on h stays uniform. The binary block mixture has
chi-squared divergence (2^b-1)/M from the trivial state. Data processing and
relative entropy give at most log(1+(2^b-1)/M) nats per block. The classical
relative-entropy chain rule and Pinsker yield

    T^2 <= min(1, t(2^b-1)/(2M)).

Fixed b and polynomial t cannot provide constant binary advantage. This
written uniform argument is review-pending, not a machine-checked proof.
It does not cover quantum memory across blocks or noninvariant row outputs.
The earlier reference-twirl audit has different channel assumptions; do not
interchange its bounds with this one.

## Research Decision

Keep these schedules as regressions for source weights, task distinctions,
measurement disturbance, classifier cost and baseline strength. Do not
continue fitting longer small-group alternating schedules as a discovery
strategy. A live proposal needs a growing-copy program, a task-relevant
decision rule, non-negligible natural source coverage and a classical
comparison that remains meaningful when multiplicity spaces grow.

Existing machinery reused:
`self_dual_wreath_carrier_noncentral_readout_boundary.py`,
`self_dual_wreath_plancherel_carrier_contextuality.py`,
`self_dual_wreath_physical_frame_blocks.py`, and the physical binary model in
`coset_hidden_involution_binary_decision_reduction.py`.
