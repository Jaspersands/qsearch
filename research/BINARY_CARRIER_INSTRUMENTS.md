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

For fixed-point-free involutions, `core/involution_character_arithmetic.py`
now supplies polynomial-time **exact** scoring of given one/two-copy labels.
Pad lambda to an even number of rows and split beta numbers
`lambda_i + length - i` (one-based i) onto even/odd abacus runners. Equal
runner populations mean empty two-core. If not empty, chi_lambda(2^m)=0.
If empty, let alpha,beta be the two-quotient partitions. Then

    chi_lambda(2^m) = (-1)^(lambda_2+lambda_4+...)
                     * binomial(m, |alpha|) f_alpha f_beta.

The quotient bijection maps successive domino removals to interleaved
standard tableaux of alpha and beta. The sign is path-independent: a
horizontal domino changes the sum of zero-based cell-row indices by an even
number, a vertical one by an odd number. Thus recursive path enumeration is
unnecessary. The equivalent even-hook formula is established prior art; see
[Swanson, Theorem 8](https://arxiv.org/html/1701.04963).
The implementation is checked against independent exhaustive domino recursion
on every even-degree partition through n=20, conjugate-partition signs and
the actual complete S4 two-copy physical outcome law.

Hook products, factorials and rational comparison use polynomially many
operations on O(n log n)-bit integers. Label scoring through degree 4096
requires no enumeration of the group, all partitions, tableaux, or the
Kronecker joint law. Those large-label regressions do NOT certify natural
source coverage. The generic partial-matching character routine still uses
recursion; no polynomial claim is made for that implementation. An exact
`sign(r_lambda+r_mu+r_nu)` score is cheap classical postprocessing of quantum
labels, not a classical sampler of those labels, a higher-copy classifier,
or a scalable two-copy speedup.

## Clean Label Access Is Not Reference Discard

`core/isotypic_instruments.py` makes the assumed instrument operational.
Let U_g be a supplied unitary representation of a finite group, and use the
Fourier convention F_(lambda,i,j),g=sqrt(d_lambda/|G|) conjugate(rho_lambda(g)_ij).
Uniform group preparation, controlled U_g and this QFT form a unitary W.
On a clean reference its isometry V has data Kraus operators

    A_(lambda,i,j) = sqrt(d_lambda)/|G|
                     sum_g conjugate(rho_lambda(g)_ij) U_g.
    P_lambda = d_lambda/|G| sum_g conjugate(chi_lambda(g)) U_g.

Matrix coefficient orthogonality gives

    sum_(i,j) A_(lambda,i,j)^* A_(lambda,i,j) = P_lambda,
    Pi_(reference,lambda) V = V P_lambda.

Consequently W, **copy only lambda to a fresh output**, W^* gives

    |0>_reference |psi> -> |0>_reference
                           sum_lambda |lambda>_output P_lambda |psi>.

The equality holds as an operator, including on entangled inputs; no branch
is postselected. It does not depend on how W is extended off the clean-input
subspace. Measuring the copied output implements the desired Luders map.
Neither the Fourier row indices nor a Kronecker multiplicity basis need be
decoded. The finite evaluator independently checks the character formula,
the intertwining identity, full compute-uncompute matrices and a complex
character convention control. These are regression checks, not a formal proof.

For S_n physical regular registers, controlled known group multiplication is
an explicit efficient primitive. A subset of b registers uses b such actions
per forward GPE call. Each clean label query uses two QFT/adjoint calls, two
uniform-preparation/adjoint calls and 2b controlled single-register actions.
For q queries with forward-unitary operator error at most delta, the complete
channel diamond distance is at most min(2,4q delta), including adaptive use.
The inverse must be the adjoint of the same implemented approximate circuit.
This follows by telescoping W/copy/W^* (operator error at most 2delta), then
the unitary-channel bound and channel composition. Charge uniform preparation
and coherent arithmetic as well; there is no enumeration of n! permutations
in this **conditional reduction**. The dense verification code is not a
gate-level S_n QFT backend. Efficient QFT construction is established context,
not a new result of this repository; see
[Moore, Rockmore and Russell](https://arxiv.org/abs/quant-ph/0304064).

Discarding the reference after reading lambda is a different channel:

    E_lambda(X) = sum_(i,j) A_(lambda,i,j) X A_(lambda,i,j)^*.
    sum_lambda E_lambda(X) = |G|^-1 sum_g U_g X U_g^*.

The first-label probabilities agree with P_lambda X P_lambda, but the group
twirl destroys carrier coherences within that label. The test with an
entangled two-dimensional carrier and multiplicity register has a certain
label: the clean instrument leaves the pure state intact, whereas discard
outputs I/4 and loses 3/4 trace distance. This is a channel counterexample,
not a proposed search problem.

For the physical binary model, pair-local conjugation of the three-input
alternative averages the hidden h in the pair independently from the h in
the spectator. More generally, on a proper partition A,B,

    Twirl_A[avg_h rho_h^tensor k]
      = [avg_h rho_h^tensor |A|] tensor [avg_h rho_h^tensor |B|].

For a two-input pair, its source-conditioned class average is scalar inside
each target label: its likelihood ratio is 1+r_left+r_right+r_target.
The spectator contributes 1+r_unused. Thus after pair-reference discard,
each full source/target branch satisfies alternative=LR*null. Given that
first label, no hypothesis-dependent quantum state remains. This argument
does not need the rank-one multiplicity condition of the finite HMM below.
For larger partitions internal information can remain; do not assert that
every local twirl destroys all binary information. One **global diagonal**
twirl preserves the entire binary mixture and is explicitly tested separately.

All 152 physical S3/S4 source triples obey these identities. In S4, clean L
retains 59/96 trace distance, while discarded reference rows retain only
27/64, exactly the first-label transcript distance. The additional loss is
37/192. Following with a clean R measurement cannot restore it. This is a
failure of one implementation, not a no-go for clean isotypic measurements,
an end-to-end classical algorithm, or a new speedup. The clean primitive
removes an access ambiguity; the growing-copy program and its outcome
classifier are still open.

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

## Task-Correct Search Direction

The typed mechanism factory previously required every route to end in
hidden-element identification. It now distinguishes identification from
binary detection, including the terminal type, copy bound, missing
capabilities and rejection filters. The binary route remains a research
proposal, never an accepted algorithm candidate.

`MECH-CLEAN-SUBSET-BINARY-DETECTION` asks for a growing-copy program built
with clean subset-label access, an efficient classifier of its actual
outcomes and a promise-preserving natural-problem reduction. All three
capabilities are explicitly missing. It does not require a full Kronecker
multiplicity basis or hidden-element output merely to formulate the binary
task. The proof gate must still reject an unidentified collective-effect
box, uncharged preparation, a free hypothesis-dependent sampler, or a
constant-copy experiment presented as asymptotic evidence.

For binary equal-prior advantage epsilon, the necessary copy count is
`ceil(log2(1+16 epsilon^2 M))`; identification has its separate Holevo/Fano
bound. The old binary report is reconciled with the already-implemented
support-rank proof: `T>=max(0,1-M/2^k)`. Information availability at
logarithmic copy count is known, not a target for rediscovery. The bound
does not implement the support projector, and clean subset labels plus
exact two-copy scoring do not implement the growing-copy sign operator.

The next substantive experiment should specify a uniform family of
coherent/adaptive programs, its complete outcome law and classical
contraction cost. Do not enumerate all 2^k subsets, merely tune longer S4
sequences, or infer binary usefulness from noncommutation alone. A cheap
class function of a single subset label can be coherently evaluated; this
does not fast-forward a noncommuting sum over exponentially many subsets.
That aggregation and source-weighted readout remain unresolved.
