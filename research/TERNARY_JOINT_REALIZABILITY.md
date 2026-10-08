# Joint PSD And Selected Native Local Cuts

LOCAL DERIVATION / REVIEW PENDING. One finite relaxation gap, no novelty,
native decoder, source-population theorem or quantum speedup claim.

## Finding

The original target11366831/winding3 moment model with ALL37 saved
three-block native inequalities admits an exact PSD continuation even
though the original prefix contains no native word. The positive witness
therefore survives BOTH complete degree-two PSD and those selected local
inequalities. It does not establish full three-block realizability.

The follow-up [event audit](TERNARY_EVENT_TRIANGLES.md) rejects this new witness
on14 triples. Seven were already obstructed in the old witness, and seven
were previously extendable. A single inequality per previously failing
triple is not closure of the local marginal polytope.

## Exact Mixed Model

Rebuild all original equations and37 local inequalities from the hash-pinned
local/source reports. The initial898-variable,855-equation primal is replayed
exactly. Local slacks are nonnegative variables, NEVER indicators. A bounded
three-cut PSD loop adds primitive square inequalities; every coefficient on
every old local/PSD slack is ZERO. Every primal and signed dual checks the
whole current mixed model, not only the original p/J coordinates.

All four resulting points are indefinite. Three valid square cuts and three
LP re-solves stop at an explicit cap, which by itself proves nothing about
the full joint cone. A denominator8 four-point hull search makes165 floating
eigenvalue proposals and eight exact negativity checks. An exact positive-SOS
separator excludes this SUPPLIED hull, not the full joint model.

Its principal vectors are zero-embedded into the original indicator space.
The whole898-variable support LP has zero objective coefficients on local
slacks, retaining ALL37 necessary inequalities. One exact base escape proves
the separator does not exclude the full joint relaxation. The saved primitive
objective has16,357-bit coefficients; normalization and unscaling never pass
those integers through floating conversion.

One bounded five-point hull refinement makes495 proposals and finds an exact
PSD mixture on its first exact check. Weights `[3/8,0,1/8,0,1/2]`; exact native
face dimension16. The retained full898-moment/slack array satisfies every
original and local-cut row, and a separate full43-dimensional exact LDL
verifies original-coordinate PSD. Independently replayed native emptiness
establishes a gap at this ONE prefix/winding.

Total four LP calls, nine hull positivity checks,660 numerical proposals.
Recorded audit approximately11.5seconds, excluding original source compilation
and rebuild. No new global dual, whole-prefix exclusion or native pair.

## Implementation And Verification

```sh
python theorems/ternary_joint_realizability.py --write
node research/certificates/ternary_joint_realizability_crosscheck.js
PYTHONPATH=theorems python -m pytest -q tests/test_ternary_joint_realizability.py
```

The report pins local, support, prefix and fixture SHA256 values. Initial
primal arrays are referenced rather than duplicated. The BigInt checker
first replays ALL upstream certificates; it then checks mixed slack ordering,
all square/resolve ledgers, both hull faces, exact support escape and the
whole original-coordinate PSD gap. Passing old mixtures into the joint
model without checking all37 local inequalities is explicitly forbidden.

`sos_objective` accepts slack-augmented support ONLY with explicit
`allow_slacks=True` and model-scope metadata. Default original-model behavior
remains strict; unknown variable kinds are rejected. The joint audit rejects
preexisting PSD cuts, avoiding ambiguity or overrunning the new cut budget.
Nine focused tests include honest controls, invalid old mixtures, slack-zero
objectives, false positive hull flags, mixed cuts, winding tampering and caps.

## Why This Does Not Solve The Research Goal

Selected local inequalities plus PSD are necessary, not sufficient, native
conditions. The new gap already fails other cheap inequalities. Iterating
selected empty-prefix classifications can consume unlimited time without
ever constructing two witnesses or proving population performance. This
experiment justifies a stronger and cheaper separation vocabulary, not a
larger blind square-cut budget or generic moment hierarchy.

See `TERNARY_EVENT_TRIANGLES.md` and
`NATIVE_TERNARY_EVENT_FAMILY_TARGET.md`. Do not silently treat the ordinary
classical two-witness helper as necessary for EVERY possible quantum receiver;
it is a missing primitive in this construction. Reassessing that design
assumption may have greater upside than more conditional pruning.
