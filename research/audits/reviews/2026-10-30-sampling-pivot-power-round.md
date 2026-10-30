# Sampling And Pivot-Power Review Round

30 October 2026. A mathematical and bounded-arithmetic pass, not a
Shor-level result, human peer review or a formal proof-assistant check.
The previous general-native-search review is a separate round.

## Assignments

| Agent | Scope | Outcome |
| --- | --- | --- |
| Pauli the 2nd | Classical search-to-sampling transfer; binary-rank proof and implementation | Proved the balanced-block support defect and checked the efficient kernel diagnostic. Existing flat witnesses pass; no hardness candidate follows. |
| Euclid the 2nd | Primary-source comparison, native utility and independent pivot probability audit | Known full-list primitive; no useful exact-law reduction established. Confirmed pivot moment calculation and found the nonregular mod25 counterexample. |
| Maxwell the 2nd | Independent arbitrary-syndrome trace-sum and adaptive-transcript audit | Checked all expansion regimes and additive twists. Caught the empty-fiber zero-query guard and a vacuous adaptive-branch fixture; both corrected and replayed. |
| Popper the 2nd | Constructive pivot-power algorithm and bounded implementation | Replaced bank-width power rejection by rank-dependent pivot testing, with original-ambient verification, paid failure components and live arithmetic artifacts. |
| Ramanujan the 2nd | Independent final implementation/accounting audit | No concrete findings. Replayed 66 focused tests plus 1,000 rank/span/accounting cases, 3,304 sampler/lifting cases and 87 root-interruption points. |

Agent IDs in that order:

```text
01a18b59-2e7a-7513-ae8a-5fe3245c33d6
01a18b59-2f59-7a61-87ac-ab041aa4c289
01a18b60-486e-7e51-885f-eebfcaa23050
01a18b59-303b-7cb0-b84c-2248d2a75114
01a18b73-242c-70d3-8d89-52548c89b266
```

Popper's write scope was exactly the pivot module, test, proof note and
artifact. Other agents were read-only. Parent owns the two sampling
modules, tests, note, artifact and integration/handoff documents. None
was authorized to change Git state, registry claims or outreach files.
All five agents completed and were closed. Their reviews are AI-agent
checks, not human peer review or independent proof of imported geometry.
Concurrent docs/outreach/04-rees-hsp.md, docs/papers/rees-hsp/ and
tests/tools/test_rees_paper_numbers.py belong to another process and were
not changed by this pass.

## Surviving Results And Corrections

PIVOT_POWER_SDE.md gives the full conditional proof. A fixed independent
pilot supplies rank-a coordinates. Sample anchored free coefficients
uniformly from the power alphabet INCLUDING zero; only a pivot values
need power tests. Distinct anchored candidates give pairwise-independent
uniform images for an IID suffix. Exact first/second moments yield a
good-bank allowance proportional to d^a, not d^M. Repeated classical
attempts consume no additional measured labels.

The algorithm pays for all original slots, root extraction, finite random
bit rejection and explicit attempt caps. It verifies the original exponent
equation, does not enumerate the field, and does not certify the IID source.
The analytic all-prime/large-prime tree inequalities are not finite-sweep
extrapolations. Their inherited receiver, source, accepted-state and
flagged-channel hypotheses remain outside this implementation.

Euclid's counterexample is important: p5, exponent2, pilot (1,0),(0,1),
suffix (1,0) gives a valid coefficient vector (4,0,1) with active rank1,
not2. Lifting the suffix to (1,5) mod25 makes support-preserving Hensel
lifting impossible. Tests enforce prime-field-only/nonregular flags.
No nonzero-pivot regular variant is implemented.

INVERSE_TRACE_SAMPLING_DECISION.md proves a total-variation defect for
ANY law supported on balanced zero-syndrome block assemblies. The
efficient binary-kernel observable detects the new two-block examples,
but both matched classical flat witnesses pass. The implementation uses
independent binary-field multiplication, not only the production backend.
The parent added a 512-word, K2/GF8 exhaustive control and replayed all
32 subsets per word after review requested a multicheck control.

The every-syndrome count error is E_m=24^m*q^((K+1-m)/2), using the
explicit short-trace-sum theorem and additive-twisted Kloosterman sheaves.
This is an imported-theorem deduction, not formalization of that geometry.
For a classical adaptive partial observer, the exact transcript density
ratio is g_remaining/g_full. It gives a classical simulation through
3161 of3721 coordinates at n61, with TV below2^-299, not the remaining
560 symbols or a coherent query oracle.

Maxwell found that returning zero for a zero-query transcript before
checking E_N<1 would silently speak of a uniform law on possibly empty
fibers. The guard now runs first; the GF4 empty-fiber control is retained.
The first adaptive fixture selected a branch by parity although all its
nonzero accepted symbols were odd. It now exercises both second-coordinate
choices and early stopping. These were actual review corrections.

The new bound is vacuous at the previous near-minimal residual size.
No saved UNKNOWN is promoted. The wiretap comparator changes the decoder;
it removes an application-level rationale, not the exact native sampling
problem. Full sampling complexity and novelty remain unresolved.

## Artifacts And Verification

New parent files:

```text
theorems/inverse_trace_binary_rank.py
theorems/inverse_trace_syndrome_counts.py
tests/test_inverse_trace_binary_rank.py
tests/test_inverse_trace_syndrome_counts.py
research/INVERSE_TRACE_SAMPLING_DECISION.md
research/classical_baselines/inverse_trace_sampling_controls.json
```

New worker files:

```text
theorems/pivot_power_sde.py
tests/test_pivot_power_sde.py
research/PIVOT_POWER_SDE.md
research/classical_baselines/pivot_power_sde.json
```

Final parent combined replay: 328 tests passed in6.85s with warnings as errors,
pytest plugin autoload disabled, and no bytecode/pytest-cache writes. The
ten test files are pivot_power_sde, bounded_power_roots, power_sde_budget,
random_column_power_sde, weighted_two_erasure_cascade,
inverse_trace_binary_rank, inverse_trace_syndrome_counts,
inverse_trace_short_sums, inverse_trace_affine_partition and
inverse_trace_genus_zero. Both stored artifacts are bound to source hashes
and recomputed results. The pivot's 261-test receipt is Popper's earlier
connected checkpoint; Ramanujan independently reran only its66 focused
tests, not that larger checkpoint. His additional checks were read-only.

After adding the final independent-review attribution to the pivot proof
note, the parent regenerated all five pivot cases. Only that note's hash
changed; mathematical outputs and counters were identical. The final
328-test replay above includes this regenerated artifact. SHA256 values:

```text
pivot_power_sde.json
907dba9b05f3df2183a1fc3609f6eb8430b51c456b121a95ce7f7b35747bc84c
inverse_trace_sampling_controls.json
8c38451b6b3674f1595c22730a4ffc8095615699c66c82b96f3127988d5e9eef
```

Six new Python syntax checks,12siteJS syntax checks and qsearchvalidate
(validtrue,issues[]) passed. This is not the full repository suite or a
Lean rebuild. The pre-existing SMT CLI --write omission still fails its
isolated regression (FileNotFoundError); it is not waived. Preserve its
repair handoff rather than reporting all repository tests green.

All13registryJSON files retain aggregate SHA256
79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd
(sorted basenames then file bytes). No candidate, speedup status, registry
or Git write is made by this pass. Follow-up wiring belongs to the explicit
contract in MECHANICAL_FOLLOW_UP_PLAN.md, not an invented new subsystem.

Residual assumptions: supplied primes, IID source labels, fresh fair bits
and trusted arithmetic backends. Statistical loop caps are not wall-clock
deadlines. No native large-n factorization, quantum receiver execution,
coherent-query simulation or regular mixed-order lift was performed.
