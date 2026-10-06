# Direct Full-Secret Readout From A Purified Arithmetic Finder

LOCAL DERIVATION / REVIEW PENDING. No independent theorem review, novelty,
polynomial witness finder, complete lattice reduction or accepted candidate.

## Revised Target

Self-critique of `DCP_PARTIAL_WITNESS_READOUT.md` removes another unnecessary
restriction: filter the ORIGINAL phase assignments. This avoids parity
measurement, binary-rank rejection, target alignment and top-bit completion.
The previous parity route remains a verified source/covariance calibration,
not the preferred default interface for a general arithmetic finder.

A KNOWN quantum arithmetic finder need not have deterministic output, canonical
witnesses, uniform fiber amplitudes or target-independent garbage. An accessible
purified circuit AND its inverse suffice for a weighted compute-uncompute
projection. An output-only measured black box does not supply that access.

Prior-art scope: [Regev](https://arxiv.org/pdf/cs/0304005) already establishes
the partial-subset-sum connection. The repo's `dcp_symmetric_relation_lift.py`
already removes determinism by two endpoint evaluations and symmetric pairing,
with a conservative seventh-power global matching coverage ledger. This direct
full-group-QFT interface gives a square coverage law under its explicit
accessible-INVERSE contract. It is not a universal comparison, a refutation of
matching, or an independently novel result. The existing arbitrary-measurement
to-witness compute-copy-uncompute reduction runs in the OPPOSITE direction;
its legal/planted averages are not independent uniform full-target averages.

## Conditional Theorem

Let q=2^L, m=nL+Delta, Delta>=0, G=q^n, N=2^m. On native IID Fourier labels
A modulo q, the ORIGINAL product input is

    |psi_s> = N^(-1/2) sum_(x in {0,1}^m) chi_s(A*x)|x>.

Write F_A(x)=A*x mod q. A known target-controlled unitary U_t, with unchanged
public target t and blank workspace, produces

    U_t|0> = sum_(w,h) alpha_(t,w,h)|w,h>.

w is a witness word; h includes arbitrary history, seed and measurement records.
Include efficient verification and invalid-output flags. Define

    p_t(x) = sum_h |alpha_(t,x,h)|^2 if F_A(x)=t, else0,
    a_t = sum_x p_t(x), beta_A = (1/G)sum_t a_t.

a_t is ordinary verified arithmetic-solver success on target t. No complex-phase,
history-overlap, witness-uniformity or canonicalization assumption is needed.

The actual known circuit on the supplied unknown phase input:

1. Compute F_A(x) into a blank target register.
2. Apply U_t to blank solver workspace, preserving t.
3. XOR a flag when output is verified AND its witness equals x.
4. XOR that solver witness into the ORIGINAL word register.
5. Apply U_t dagger to ALL solver workspace, preserving t and flag.
6. Measure flag/workspace; retain ONLY flag1 and ALL solver workspace0.
7. Inverse-QFT the n target coordinates modulo the FULL q.

All premeasurement steps are unitary on the complete space. The XOR operation
has an explicit inverse. U_t dagger reverses a known arithmetic computation,
NOT the unknown phase-input preparation. One forward and one inverse arithmetic
circuit call, every workspace projection and every failed attempt are charged.

On flag1 the original word is0. For input x, target t=F_A(x), the cleaned
workspace0 amplitude is

    <0|U_t dagger P_(w=x) U_t|0> = p_t(x).

The heralded Kraus block is therefore the CONTRACTION

    K = sum_x p_(F_A(x))(x)|F_A(x)><x|.

Rows have disjoint fibers and squared norm<=1: this is not an unphysical
many-to-one unitary. On the unknown input, its successful target state is

    K|psi_s> = N^(-1/2) sum_t a_t chi_s(t)|t>.

For EVERY fixed full secret s, character orthogonality gives EXACTLY

    P(herald) = (1/N)sum_t a_t^2,
    P(correct full s AND herald) = (sum_t a_t)^2/(N*G)
                                 = 2^(-Delta)*beta_A^2,
    P(correct full s | herald) = (mean_t a_t)^2/mean_t a_t^2.

Conditional correctness is at least beta_A when positive, but need not be high.
Jensen over native A and independent public randomness gives unconditional
original-attempt success>=2^-Delta*beta^2, beta ordinary native FULL-target
verified solver coverage. No good matrices need be identified, no binary-rank
loss is incurred, and no secret modulus bit is lost.

Measuring/tracing the solver output rather than uncomputing leaves orthogonal
target supports: its witness itself determines F(w). Correct probability then
falls to (sum_t a_t)/(N*G). The cleanup workspace-zero projection is NOT free:
its a_t^2 Born weights are the herald probability above. No reflection about
unknown inputs, amplitude amplification or success estimation is used.

## Access Gates

A bounded uniform classical randomized program can be purified with coherent
randomness and reversible records. A bounded known quantum program can defer
internal measurements into ACCESSIBLE records and reverse the enlarged circuit.
Both need actual uniform program/circuit access and polynomial overhead.
Unretained environments, noisy external output devices, unknown quantum advice
and unavailable oracle inverses do not pass. Target-controlled circuit generation
and all preprocessing must themselves be efficient, not exponential advice.

Arithmetic inputs are A,q,t. No hidden-secret evaluator, unknown phase resource,
chosen native labels, fiber/reflection oracle or same-label copies are supplied
to the solver. Any such dependency requires a separate access/source proof.

Independent uniform FULL targets are essential. The global legal-pair coverage
transfer in `DCP_PARTIAL_WITNESS_READOUT.md` applies, but planted/per-label/favorable
coverage does not transfer for free. Even perfect solver coverage pays2^-Delta;
large density is not a free escape for this contraction. Small QR matrices below
are circuit calibration, NOT uniform algorithms or candidate oracle problems.

## Faults And Full-Secret Verification

Use the earlier SCOPED product-state prelabel gauge: fault status/basis-bit data
precede ALL fresh labels and solver randomness, old labels/coins are discarded,
and conditional fair physical Z coins are independent. Statuses across blocks
may correlate. Entangled, label-adaptive and raw unbalanced faults are not covered.
A block with b bad states has ideal-component weight2^-b, which transfers ideal
filter success by POVM positivity.

The full-q QFT already proposes the FULL secret; there is no binary completion.
Commit it before v fresh verification labels. Each fixed nonzero error passes
all-plus tests with source-average probability2^-v. Fresh balanced basis faults
also give plus with probability1/2. True completeness is used only on the ideal
component, not on every noisy branch.

Each block has M=nL+Delta+v original states. A fixed-secret marginal prelabel
fault promise gamma=1/(nL) gives expected faults<=M/(nL). Use the aggregate
Markov/conditional-independence amplification ledger in the earlier module,
with ideal success2^-Delta*beta^2 and no rank/completion losses. Five recorded
n8/16/32, Delta0/16 controls ASSUME MISSING beta1/n^2; with R=2^(40+Delta)*n^4,
v=ceil(log2 R)+32 and Markov factor4, all charged failure bounds are below1/3.
These huge constant allocations are conditional ledgers, not practical executions.

Actual native lattice preparation, coordinate phase law, conditional fault
lineage and total gate/state approximation still need full composition proof.
The conditional numerical ledger certifies no natural lattice algorithm.

## Self-Critique And Next Work

- **Hardness moved:** this may be only a standard consequence of known
  reductions. No efficient native finder exists here. Seek independent review
  and literature comparison, not a discovery announcement.
- **Inverse access:** a known arithmetic program inverse is essential;
  the inverse witness RELATION is not. Losing program environment invalidates K.
- **Wrong source:** native IID full targets, growing n,L and unconditional
  verified coverage are required. Planted, fixed-q and selected-source tests fail.
- **Hidden cost:** charge coherent preprocessing, heralds, quantum advice and
  oracle calls. High conditional fidelity is not high unconditioned throughput.
- **Noise/composition:** label-dependent faults can anticorrelate coverage and
  survival. Marginals alone do not prove generic robustness or a lattice speedup.

GPT NEXT: construct or falsify an ACTUAL uniform classical OR accessible quantum
arithmetic finder on this growing-modulus source. Canonicalization, matching,
parity charts and clean affine tails are NOT prerequisites. Use the existing
terminal subset-sum catalogue and conditional carry audits to choose a genuinely
new structural primitive. Charge every enumeration and preprocessing cost.
A polynomial finder with inverse-polynomial beta is the missing result now,
not another interface layer.

Gemini NEXT: expose this as the preferred sufficient arithmetic interface in
CLI/proof/experiment registries, retaining all assumed-coverage/no-acceptance
gates and the scoped earlier routes. Run full production regressions and repair
the separately observed subset-sum bridge registry-writer omission. No UI polish.

## Artifacts And Verification

- `theorems/dcp_direct_witness_filter.py`: declaration gate, explicit bounded
  gate-sequence simulation, exact conditional resource ledger and live report.
- `tests/test_dcp_direct_witness_filter.py`:13 cases, orthogonal target histories,
  complex phases, fractional/zero/perfect outputs, actual rank-deficient labels,
  full vector secrets, fair physical dephasing, invalid circuits and resource accounting.
- `research/reductions/dcp_direct_witness_filter.json`:3 actual purified-circuit
  controls and5 conditional scaling ledgers; no fast-finder claim.
- `research/certificates/dcp_direct_witness_crosscheck.js`: independent output
  amplitude/contraction, source Fourier and exact rational resource checks.

    PYTHONPATH=theorems python -m pytest -q tests/test_dcp_direct_witness_filter.py
    python theorems/dcp_direct_witness_filter.py --save
    node research/certificates/dcp_direct_witness_crosscheck.js

Independent code controls are NOT independent mathematical review. Full
production/qsearch validation is not claimed.

Independent Node checks512 output amplitudes,320 contraction entries,24 fixed
secrets,5 exact resource ledgers and4 dependency hashes. The combined focused
regression passed137 tests in30.22s, with5 writer integration tests deliberately
deselected. Python/JS syntax, JSON and whitespace checks pass. An earlier run passed118
and failed the existing subset-sum bridge result-registration test at line69;
this production failure was not hidden or repaired by theory changes.
