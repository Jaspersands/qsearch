# Verification Milestone

## Current: Complete Central Instrument

2026-10-24. The verifier now compiles FOUR modules and audits **99
declarations: 75 theorems and 24 definitions/instances/structures**. The new
ReesCentralInstrument module contributes 31 theorems and nine definitions
or structures. All diagnostics are empty; only propext, Classical.choice
and Quot.sound occur. The final four-module rebuild and full audit replayed
byte for byte, with all 18 source/config/document hashes checked.

Current formal receipt SHA256:
`c34bb0de2a1c17f4d340556b56114c39fe9ed0f8e74913ee298396dcae1d4427`

The new theorem starts with two-sided central measurement operators on
independent coset sources. It handles nontrivial hidden central
intersections, forbidden outcomes, adaptive records, inactive targets,
and arbitrary address/reference matrices. The explicit group support and
phase-cancellation certificate is still a hypothesis, not an implemented
solver. Read REES_CENTRAL_SCOPE.md before interpreting the result.

The rank-two central control executed all 729 records, including 702
zero-mass records. Its maximum record-entry error was 8.10e-17; complete
channel error was below 1.67e-15. All actual matrices were evaluated in
floating point. This does not substitute for the separately checked
universal Lean statements. The generated control receipt also replayed
byte for byte, with SHA256:
`8ce4da97f87cc57a7dcea01556359551f11e5ee7f2ef9593cd59966df408e0f6`

**852 external regression tests passed in 20.29s**, warnings as errors,
plugin autoload disabled, no skips. This is the previous 826-test selection
plus two audit tests, 12 new central controls, and 12 existing physical
central-channel controls including target reuse and correlated sources.
After final verifier/config edits, the 29 local tests passed again in
1.19s. All four local Python files passed py_compile after final edits.
No build/test process remains running.

New files: ReesCentralInstrument.lean, central_controls.py,
test_central_controls.py, REES_CENTRAL_SCOPE.md, CENTRAL_HANDOFF.md and
central_control_receipt.json. Updated: Audit.lean, verify.py, test_verify.py,
lakefile.toml, README.md, receipt.json and this verification note, plus the
parent research checkpoint. Earlier Lean modules, source snapshot,
lean-toolchain and dependency manifest were not edited. The pinned mathlib
source tree is clean. Generated local Lean/Python caches are not research
artifacts to integrate. This note and the checkpoint are outside the
receipt manifest to avoid circular hashing.

During development, Lean caught finite-sum reindexing/simplification and
conjugation-order proof-shape errors. They were repaired without weakening
the desired statement. The final theorem composes the physical source and
discard lemmas, rather than assuming an already ideal normalized channel.

This is not full algorithm verification or a speedup result. BCH/Lazard
group compatibility, efficient public action/cancellation construction,
recursive recovery, precision and gate costs, and a natural hard application
remain outside scope. The earlier independent reviewer was not reused.

The verified main Developer destination was checked and remains absent.
No Desktop/staging, registry, CLI, UI or main Git edits; no full-repository
tests, qsearch validation, Node checks, commit or push. Follow
CENTRAL_HANDOFF.md only after migration verification.

## Historical: Dilation Milestone

The following counts and receipt describe the preceding milestone only;
the current receipt above supersedes them for the expanded proof scope.

2026-10-24. The isolated verify.py workflow now compiles THREE modules:
ReesHomogenization.lean, ReesLie.lean and ReesDilation.lean. All59 declared
items (44 theorems,15 definitions/instances) pass the axiom audit. Only
standard propext, Classical.choice and Quot.sound occur; no sorryAx or
additional axiom is accepted. No compile warnings or errors were emitted.

The dilation pass adds13 theorems and5 definitions, including actual LieHom
and LieEquiv constructors, both inverse laws, hidden-membership invariance,
the top central grade's scaling and universal invalid-scaling controls.
See REES_DILATION_SCOPE.md for the exact assumptions and remaining gaps.

A second COMPLETE three-module compilation and59-item axiom audit produced
a byte-identical receipt; all13 source/config hashes matched. Receipt SHA256:

`6a8ce8028cae54874d379938752e4599769718129724c38ac4185a7c3b12c325`

The external regression selection passed **826 tests in19.14s**, with
warnings as errors, no skips and pytest plugin autoload disabled. This
includes15 audit/manifest controls (two added in this pass) and811 other
research controls, including the preceding fixed-sign HDQI bundle. Both
Python verifier files pass py_compile. These Python tests do not substitute
for the separately executed Lean kernel check. No owned build/test process
is left running.

This pass created ReesDilation.lean and REES_DILATION_SCOPE.md and updated
Audit.lean, verify.py, test_verify.py, lakefile.toml, README.md,
REES_LIE_SCOPE.md, receipt.json and this file. The parent research checkpoint
was updated separately. ReesHomogenization.lean, ReesLie.lean, the frozen
original source, lean-toolchain and pinned dependency manifest were not
edited in this pass. The mathlib source checkout remained clean at the
pinned revision. Generated local build/cache files are not research changes
to port. The verification note/checkpoint are outside the receipt manifest
to avoid circular hashing.

Initial compiler feedback caught a dependent rewrite of the dimension and
minor simplification/proof-shape issues; these were repaired without
weakening any theorem premise or conclusion. The final proof and all source
hashes were checked after those edits.

This does not formalize the full HSP algorithm, its claimed complexity or
any natural-problem speedup. The actual Lie cover, evaluation maps,
nilpotency and graded Lie automorphisms ARE now checked. BCH/Lazard groups,
normalized quantum instruments, fresh-copy adaptive composition, SDE and
resource bounds remain outside scope. The toolchain and imported mathlib
binaries remain trusted. The one prior independent AI reviewer did not
review this new formalization; no additional reviewer was used.

The intended main Developer checkout was rechecked and remains absent.
Desktop, staging, registry, CLI, UI and main Git were not modified.
Whole-repository tests, qsearch.py validate, Node checks, commits and pushes
were NOT run. Follow the bounded handoff only after migration is verified.

History: the first milestone checked16 theorems and584 external tests;
the next constructed the Lie cover and checked41 declarations and586
tests. Those older receipts/counts are superseded by the current manifest,
not evidence for its additional claims.
