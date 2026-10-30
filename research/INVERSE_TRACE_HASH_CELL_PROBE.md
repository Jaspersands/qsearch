# Native Inverse-Trace Complete Hash-Cell Probe

29 October 2026. Bounded classical solver experiment, not a sampler or a
hardness result. The target is the missing complete-enumeration premise in
[the conditional hash heat bath](INVERSE_TRACE_HASH_HEATBATH.md), not a
new general hashing algorithm.

## Frozen Campaign

Keep the original polynomial-basis field, public evaluation points, target
bits, and native verification relation. The principal n17 input is the same
seed1028 all-one instance stored in `classical_baselines/inverse_trace_smt_n17.json`:

```
SHA256(canonical instance JSON)
9a909ce6e7afc2a5668da53fa183efa7a137bec1e744c71b657df9ac9f54fcff
```

Fix the first `m=K+ceil(3K/(2n))` residual indices before any solver outcome.
Draw one accepted complement with prefix seed1029; never restart it on
failure. This is a new, explicitly declared residual restriction of the
original input, NOT the same syndrome as the older45-coordinate SAT probe.
The tighter residual has40 coordinates at n17: K36 pivots,4 free FIELD
variables, B64 accepted-root bits, and28 random binary hash rows.
Full row rank still leaves36 Boolean degrees of freedom, not four.

Predeclare three raw hash matrices and right-hand sides with seed1030.
Each row is an unrestricted uniform B-bit draw in the ideal law; seeded
Python runs are deterministic diagnostics. Retain zero and deficient rows.
The unanchored right-hand side is independent and uniform in the ideal
law. Maximum16 models; one10-second post-setup enumeration deadline per
cell; Z3 resource limit50000000 requested on each check. Setup, extraction,
verification, blocking and finalization are measured. This is not a hard
whole-workflow wall-clock or operation cap.

Run n5/n7 exact calibrations, then n11 with a16-bit independent-reference
cap. At n17 the reference cap prevents a disguised2^36 exhaustive run.
A separate n17 diagnostic takes the already saved norm witness, derives
its complement/syndrome, and sets each hash RHS to the anchor image.
That diagnostic is witness-conditioned, uses a DIFFERENT residual h, and
does not measure unplanted initialization or uniform-syndrome performance.
The anchor's acquisition cost is explicitly not charged in that diagnostic.

For every residual run256 fixed independent accepted-root Prange trials
at exactly the same h. These are not wall-clock-matched benchmarks. The
ideal per-trial success is `g(h)*2^(-K)`; no hits in256 trials cannot support
hardness. No fresh input, convenient syndrome, or successful seed is
substituted after observing outcomes.

## Implementation And Failure Semantics

- `theorems/inverse_trace_hash_cell.py`: binary Gaussian elimination of the
  original hash, exact native field constraints, projected blocking on
  accepted-root coordinates, and independent actual-field model checks.
- `theorems/inverse_trace_hash_probe.py`: frozen prefix/hash campaign,
  original full-word verification, bounded exhaustive hash-slice reference,
  separate anchored diagnostic, and same-residual Prange comparator.
- `qsearch.py inverse-trace-sampling --hash-cells`: executes the campaign;
  the existing no-flag menu audit remains separate.

`COMPLETE` requires a final solver-reported UNSAT after blocking every
verified projected model. It is not a checked UNSAT proof artifact. A
model cap, timeout, resource exhaustion, or backend error leaves PARTIAL
or UNKNOWN and preserves any already verified models. Even a list that
happens to exhaust the cell stays PARTIAL if its final UNSAT was not run.
An UNKNOWN empty list is never called an empty cell. Independent exhaustive
references can settle a bounded cell separately without changing the
solver's recorded outcome. No incomplete list is used to draw a sample.

The fixed h is not certified good by a variance bound over uniform h.
The anchored diagnostic also does not certify every-anchor runtime.
No production heat-bath walk or uniform sampler is run.

## Prior Art And Interpretation

Hashing-based SAT sampling is established prior art. The
[UniGen paper](https://www.cs.rice.edu/~vardi/papers/dac14a.pdf) explicitly
uses independent supports and small hash cells for almost-uniform witness
generation. This implementation is a native-relation diagnostic, not a
claim to that general technique or its guarantees. General SAT calls
are not polynomial-time primitives.

The [CryptoMiniSat implementation](https://github.com/msoos/cryptominisat)
supports incremental SAT with XOR clauses. No XOR-aware external backend
was installed or run here. Z3's bit-blasted encoding may lose useful
structure; failure here does not rule out that alternative, an algebraic
enumerator, or classical sampling.

## Results

The five original campaign artifacts are
`classical_baselines/inverse_trace_hash_cells_n{5,7,11,17}.json` and
`classical_baselines/inverse_trace_hash_cells_n17_anchor.json`.

| Input | K / r / B / k | SAT complete cells | SAT models per cell | Independent reference | Prange hits / 256 |
| --- | --- | --- | --- | --- | --- |
| n5, fixed accepted prefix | 3 / 1 / 4 / 1 | 3/3 | 2,1,1 | exact matching sets | 27 |
| n7, fixed accepted prefix | 6 / 2 / 12 / 6 | 3/3 | 0,2,1 | exact matching sets | 5 |
| n11, fixed accepted prefix | 15 / 3 / 30 / 15 | 0/3 | 0,0,0 | all three cells exhaustively empty | 0 |
| n17, fixed accepted prefix | 36 / 4 / 64 / 28 | 0/3 | 0,0,0 | not run:36 free bits | 0 |
| n17, norm-conditioned h | 36 / 4 / 64 / 28 | 0/3 | 0,0,0 | valid known anchor in every cell | 0 |

Every listed hash had full row rank, as an outcome rather than a selection
rule. The n11 references each examined all32768 hash-slice coordinates.
Their emptiness does not certify that the whole residual fiber is empty.
The SAT outcomes remain UNKNOWN, even though the independent reference
settled those three cells. At n17 the norm-conditioned cells are provably
NONEMPTY from their verified anchor, yet the unseeded solver found none.
The two n17 rows have identical original public instances but different h.

Measured solver totals were0.008--0.035s per n5 cell,0.065--0.121s at n7,
7.46--9.80s at n11,5.17--6.76s at unplanted n17, and5.01--5.60s at
norm-conditioned n17. The n11 references separately cost3.22--3.55s each.
UNKNOWN reasons were backend resource-limit/canceled reports; do not
infer a precise stopping cause beyond the recorded reason/statistics.
These are workload-dependent diagnostic timings, not controlled speedup
comparisons or a fitted scaling law.

### Supplied-Anchor Followup

An anchored transition legitimately knows its current u. The original
norm-conditioned run supplied only M and Mu to the solver, not u itself.
After those results, a separately labeled followup verifies the supplied
anchor, retains it once, blocks its entire projection, and enumerates the
remainder. It uses the SAME original instance, residual h and hash cells
as the preceding anchored run; no seed or matrix is resampled on failure.
Run with `--anchor-report ... --supply-anchor` and save under a distinct
`inverse_trace_hash_cells_n17_anchor_seeded.json` filename.

Externally supplied and solver-found counts and event times are separate.
The supplied witness counts toward the16-model cap. Final UNSAT is still
required; a failed remainder search means PARTIAL with one known member,
not a completed singleton. Any eventual uniform-cell draw must include
the anchor, preserving the heat bath's self-loop.

Outcome: all three seeded n17 calls returned PARTIAL, with exactly one
external seed and ZERO solver-found models, no completion timestamp, and
an UNKNOWN remainder. Whole-call times were6.34,5.35,5.82s. Parent replay
confirmed identical original input, residual descriptor, raw matrices and
RHSs between seeded and unseeded anchored reports. This removes one unfair
first-witness burden without resolving complete enumeration. It does not
prove the anchor is the sole member of any cell.

The original source fingerprints are preserved in
`audits/reviews/inverse_trace_hash_cell_initial.py.txt` and
`audits/reviews/inverse_trace_hash_probe_initial.py.txt`. Their hashes match
all five initial artifacts. They are archival execution provenance, not
imported alternative implementations. Followup artifacts fingerprint the
then-current modules, retained separately in the corresponding
`inverse_trace_hash_{cell,probe}_seeded.py.txt` source snapshots. Never overwrite failed initial runs merely
because a later encoding or budget improves a result.

### Independent Review

Arendt implemented the cell backend and adversarial tests. Maxwell reviewed
the mathematical/measurement contract and implementation. Review exposed
a driver guard omission: the backend stopped on invalid/duplicate models,
but the campaign could continue. Parent reproduced it by injecting a faulty
receipt, then made either counter fatal to the campaign, with regressions.
None of the saved live runs had either fault. This is AI review, not human
endorsement or a checked completeness proof.

Review also reproduced a common-mode limitation: the initial reference
and backend shared binary elimination. Injecting an extra equation into
both could conceal an omitted solution. The repaired checker enumerates
ALL u coordinates when B<=16, before any shared elimination. The updated
n5/n7 calibrations require completed solver results and exact agreement,
not merely valid subsets when a solver happens to complete. Their new
`inverse_trace_hash_cells_n5_reviewed.json` and `..._n7_reviewed.json`
artifacts preserve the same cell sets, but check all16 and4096 coordinates
per cell respectively. A regression now detects the injected shared fault.
Larger bounded slice references, including the original n11 reference,
still share hash elimination; this limitation is explicit, not a claim of
an observed bug in the elimination algorithm.

The current runner fingerprints disk sources before and after execution
and refuses a changed-source run. It does NOT attest already loaded
bytecode. The CLI hashes the exact anchor bytes it consumed, rather than
rereading a possibly replaced file. Regression controls cover both races.
Archived fingerprints describe the historical execution versions, not an
assertion that all old reports came from today's files.

Maxwell independently confirmed these scoped repairs with14 probe tests
and a separate anchor-file replacement countercontrol. Parent's final
connected12-file suite passed454 tests;7 Python and12 JavaScript syntax
checks and `qsearch.py validate` passed. This is not a whole-repository
test claim or an independent re-audit of the entire seeded backend.

## Next Decision, Not Another Infrastructure Layer

The bounded Z3 encoding has not supplied the efficient complete-cell
primitive. Raising caps indefinitely is not a scientific plan. An XOR-aware
backend or a different algebraic elimination can be a matched-input next
test, but must improve empty-cell/completion work, not just first witnesses.

James independently assessed changing coordinates. With original free
symbols z=x_J, x_I=a(h)+Dz is affine and there are nr ambient bits instead
of(n-1)r. Hashing with the SAME k=(n-1)r-K retains the same mean cell size
and collision/minorization proof, but a full-rank slice has K+r bits rather
than K. At n17 this is40 instead of36. Adding r more hash rows to disguise
that difference reduces mean occupancy to g(h)*2^(-r), so initialization
needs at least2^r/g(h) trials in expectation. It is not a free improvement.
Binary hashing does not preserve an F_q-affine slice in either encoding.

A more substantive alternative is exact algebraic counting. For each
coordinate introduce y and impose, in the ORIGINAL field,

```
x^2*y=x, x*y^2=y, Tr(y)=b.
```

These force exactly y=inv0(x), including the legal zero branch. Field
squaring is binary-linear, so the equations become Boolean quadratic
constraints. On all-one targets xy=1 already suffices, so this equation
change alone adds no leverage there. After linear elimination and all
Boolean field equations, the finite Boolean quotient algebra has dimension
equal to the exact cell cardinality. Conditional quotient dimensions allow
uniform bitwise sampling and emptiness detection without listing the cell.
The serious unresolved task is computing those dimensions efficiently;
small final quotient dimension says NOTHING about intermediate degree,
matrix sizes, or time. No such efficient constructor is established here.

For a decisive crossed test, encode each frozen cell both as SAT and as
the quadratic system; independent finite complete sets must match. A new
x-hash family is a DIFFERENT set of cells and must not be silently compared
as an identical input. Record elimination degree, memory, full completion
and empty-cell certification. Stop treating the alternative as promising
if it merely accelerates first witnesses or produces exponential intermediate
tables. Do not promote a candidate or infer classical hardness from the
present negative diagnostic.
