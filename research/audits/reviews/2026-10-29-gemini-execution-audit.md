# Gemini Execution Audit: Native Contracts And Receiver Scope

29 October 2026. Independent automated review of the new execution pass,
not human peer review or a new quantum result. Preserve the original
Gemini handoff as provenance; its unqualified completion statement must
be read with this correction. Repair verification is recorded below.

## What Survived Mathematical Review

Cicero checked the subfield construction under its stated promises:
F=F_(2^n), n=e*m, e>=3, |F_(2^m)|>=e, irreducible supplied modulus,
and at least eK DISTINCT zero-target coordinates. The relative trace
pairing, full-degree direction basis, Vandermonde/Rado condition and
augmenting-path interpretation support deterministic search for arbitrary
syndromes. Independent controls included3780 admissible small-field
(theta,beta) pairs,225 seeded syndrome solves, relative degrees7,8,9,
and all128 subfield scalars for m7. These support implementation review;
they are not the proof and do not establish uniform sampling.

Fermat checked the mixed-modulus character pairing and QFT signs. For a
genuine right regular group action and genuine coset density rho_H,

    Tr(rho_H R_z) = 1[z in H],
    Tr(rho_H Pi_y) = |H intersect Z|/|Z| * 1[chi_y trivial on H intersect Z].

Centrality supplies commutation. Independent finite controls used five
subgroups of D8 x C4, including nonnormal ones. This does not give an
algorithm to obtain hidden H intersect Z, construct the required source,
or certify arbitrary user-supplied densities as coset states.

Parent checked the Vandermonde elimination: the coefficient row of the
r-th Lagrange polynomial is the r-th row of the inverse transposed-power
matrix. Applying it to the original syndrome and free columns gives an
exact affine bijection, including zero free coordinates. It reduces
symbolic variables; it does not prove a faster SAT solver or a sampler.

## Reproduced Implementation Defects

- Subfield default K was inferred as N/2 and odd N rejected, instead of
  native floor(N/8). Valid n6,N36,K4 and n9,N81,K10 inputs were affected.
- Negative theta/beta overrides did not terminate in bit arithmetic.
  Noncanonical and repeated selectors could alias a physical coordinate;
  a returned bad witness was caught by verified=False, not falsely certified.
- Necessary elimination operations inside assert vanished under python -O.
  The solver failed rank checks; the greedy diagnostic falsely labelled
  its zero-rank result as the intended obstruction.
- Empty or identity-free subgroup lists made the receiver coset traversal
  repeat forever. Bounded subprocesses reproduced both cases and were reaped.
- The receiver accepted an indefinite trace-one matrix with probabilities
  (2,-1), and an all-NaN matrix, as verified numerical inputs.
- Stage rank/moduli/center contracts were not cross-checked, and a
  fractional copy count was silently truncated.
- Uniform-per-stage error allocation overcharged the final certificate:
  counts(1,2) allocated1/10 but reported3/20. Parent reproduced this too.
- The subgroup argument really described H intersect Z, not arbitrary H.
  Dense PVM tests did not certify freeness, faithfulness or ambient centrality.
- The public Vandermonde helper accepted negative and Boolean indices as
  Python aliases. Parent reproduced both; production calls had already
  validated their ordinary consecutive indices, so this is an API boundary
  defect, not evidence of false native solver results on valid inputs.

## Correct Complete-Channel Accounting

Let stage t make at most M_t measurements, each with COMPLETE-channel
half-diamond error at most

    epsilon_t = 2*sum_j eta_(t,j) + eta_translation,t.

The measurement contribution is S=sum_t M_t*epsilon_t. A telescoping
hybrid uses the bound for each actual call, uniformly over classical
transcripts and arbitrary reference systems. Include joint source error,
other actions, controls and abort probabilities to obtain

    E = delta_input + S + A*eta_action + delta_control
        + delta_ideal_abort + sum_t delta_abort,t.

The total bound is min(1,E), for the complete flagged output. Never divide
by acceptance probability. The weighted average S/sum_t M_t is NOT a
uniform per-call bound. The frozen uniform-bound calculator can validate
fixed overhead; the explicit stage sum is added separately with its own
metadata. Call caps, full-channel errors, source independence and actual
gate/workspace implementations remain premises, not calculator outputs.

## Scalable Compiler Remains Missing

The receiver backend enumerates Z and materializes matrices of dimension
|Z|*|G|, with quadratic storage and dense matrix multiplication. This is
a finite numerical reference instrument, not polynomial-size approximate
gate synthesis. It does not implement reversible valid encodings,
workspace cleanup, a recursive source factory, or bounded end-to-end
execution. Character pairing and conditional rational error accounting
are useful checks, but do not close those obligations. Public matrix
construction uses no hidden-subgroup advice; optional subgroup/density
inputs are validation diagnostics, not an available source oracle.

## Verification Status

Before repair: the subfield suite's4 tests and the receiver's6 tests plus
23 pilot-policy tests passed despite the defects above. Parent's32 SMT
tests passed before API hardening; after strict validation and exhaustive
F4 syndrome/permuted-coordinate controls, all48 passed in4.16s. The
connected five-file SMT/hash/CLI selection then passed303 tests in18.30s.

Euclid repaired the subfield contract and termination checks without
changing the construction. The normal suite passed144 tests; optimized
Python passed143 with the subprocess-wrapper test excluded. Default
N36/N81 inputs now use K4/K10, and the greedy-control ranks stay10 and12
under optimization. Invalid original-equation verification now raises
rather than returning a purportedly completed solve.

Maxwell repaired the receiver validation, renamed the diagnostic input to
central_intersection, validated a free permutation representation, and
recorded finite-reference scope. The weighted hybrid keeps actual stage
counts and adds their error sum to the fixed-overhead calculator without
changing that frozen module. FLINT primality replaces square-root trial
division in the public schedule specification. Its85 backend tests and
three pilot suites passed146 tests with warnings treated as errors.

Parent reran the native N36 default and the unequal-stage1/10 example;
both now pass. The indefinite and NaN densities reject. The frozen pilot
source/tests and hash-quadratic source retain their recorded hashes.
Parent's combined21-file selection passed920 tests in80.44s with warnings
treated as errors. Thirteen changed/new Python files compile; all12 site
JavaScript files pass syntax checks. qsearch validate remains valid with
no issues; no candidate or speedup status was promoted.

Cicero independently rechecked all four subfield findings and found them
fixed. Normal/optimized suites passed144/143 tests. In each mode it also
checked128 syndrome cases across e3 through9,300 full-relative-degree
theta choices, all128 scalars on three m7 lines and a production
augmenting path. The helper deliberately requires K>=1, including for
explicit syndromes; the old degenerate empty-syndrome behavior is not
preserved. This does not exclude the intended native N=n^2 inputs.

Fermat independently rechecked all six receiver findings and found no
remaining actionable defect in that scope. Its108-test selection passed
with warnings as errors. It reconstructed500 exact randomized schedules,
including unequal and huge copy counts and target error one; tested all
216 permutation-valued C3 maps (only the two free representations pass);
and repeated the five D8 x C4 subgroup diagnostics, pairing/sign and
large-prime checks. Call caps, full-channel tolerances, source access and
scalable gate synthesis remain outside this certification.

Final reviewed source hashes:

    subfield: 964c04fae103c91ea51dcd0b969d8fdd1e310aed1fc876cc309a7e6cc30aef68
    receiver: 40a1486829da586f2b2247e3ba36701d1bd9dc8d20e93bdb66fa56b5ce12583b
    SMT:      3c31d0afa756340fba938b215326bb9e941d30641b82fb009b7cd93b63edbed6

Both reviewers are closed. No Git commit/push, installation or external
contact occurred. Unrelated work and the original Gemini handoff remain
preserved; no whole-repository or physical-receiver completion is claimed.
