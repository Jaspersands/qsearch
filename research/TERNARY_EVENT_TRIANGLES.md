# Exact Native Boolean-Event Triangle Separator

LOCAL DERIVATION / REVIEW PENDING. Elementary classical inequalities, not
an algorithmic novelty claim, complete marginal-polytope solver or speedup.

## Mathematical Representation

For three distinct native blocks, choose nonempty proper subsets of their
retained digits. Let X,Y,Z be the corresponding zero/one event indicators.
Pointwise on EVERY original native assignment,

```
T(X,Y,Z) = X - X*Y - X*Z + Y*Z = (X-Y)*(X-Z) >= 0.
```

The value is one on100 and011, zero on the other six Boolean patterns.
Its expectation is therefore the sum of two genuine triple probabilities.
It need not be a PSD square: continuous real coordinates do not satisfy
this pointwise native sign property.

Expand E[T] directly in ORIGINAL p/J coordinates, with p coefficients+1
on the center event, cross-pair coefficients-1 on incident event pairs,
and+1 on the other event pair. No hull zeros, native lift choices or hidden
phase information enter the inequality. Every retained proof recomputes
both its exact original-moment value and its coefficient expression on
every local original digit assignment (at most27).

Complementing ALL three events leaves T unchanged. Restrict the center
event to contain the first retained native digit; this halves enumeration
without omitting any member of the inequality family. Each three-digit
triple has324 canonical combinations;14 blocks give117,936 combinations.
At a fixed alphabet, the arithmetic-operation count is cubic in block count.
Rational bit complexity is additional and explicitly recorded.

## Exact Classical Separation

`ternary_event_triangles.py` verifies the full original point, clears its
moment denominators EXACTLY, caches every event marginal and pair-event
sum, and evaluates the complete preflight-approved family in integer
arithmetic. It retains the most-negative inequality per failing triple.
There is NO LP, eigenvalue test or floating tolerance in this separator.

Failure to find a violated event triangle does NOT prove three-block
extendability. An exceeded whole-family preflight yields UNKNOWN, not a pass.
All honest native distributions obey these inequalities, but native
realizability is not proved from their satisfaction.

## Actual Source Findings

Two mathematically certified PSD continuations of the SAME empty native
prefix are tested, never synthetic oracle algorithm candidates:

| Source point | Triples tested | Violated event triples | No event violation |
| --- | --- | --- | --- |
| Original PSD gap | 364 | 37 | 327 |
| PSD plus37 selected local cuts | 364 | 14 | 350 |

For the original point, ALL37 exact local-LP obstructions are detected.
NONE of327 independently certified triple distributions is contradicted.
This is complete agreement on this finite source point, NOT a proof that
Boolean-event triangles characterize arbitrary three-digit marginals.

For the second point, seven failures occur on formerly obstructed triples
and seven on previously extendable triples. It satisfies all37 saved
inequalities but not this broader family. The other350 triples have not
been proved extendable for the second point.

Each scan computes3,276 cached pair-event sums and117,936 exact event
combinations, with ZERO LP calls. Recorded scans approximately1.2seconds
and0.6seconds include full original-point rechecks and selected native truth
tables, but exclude source compilation. The earlier original-point local
LP scan used401 LP calls and approximately10.7seconds. These are separate
observational kernel timings, not a controlled benchmark or decoder speedup.

## Reproduce And Independently Check

```sh
python theorems/ternary_event_triangles.py --write
node research/certificates/ternary_event_triangles_crosscheck.js
PYTHONPATH=theorems python -m pytest -q tests/test_ternary_event_triangles.py
```

Report pins joint, support, local, prefix and fixture SHA256 values. The
BigInt checker first replays the complete source/gap/cut proof chain, then
independently enumerates ALL235,872 event combinations across728 triples,
derives all51 retained original-coordinate inequalities, checks every native
assignment value, and reproduces agreement with the exact local-LP reference.
It verifies rational bit costs and full source-point recheck counts too.

Fifteen focused tests cover zero-LP separation, all27 honest native words,
mixtures, global-complement invariance, original block/event tampering,
singleton domains, preflight unknowns and invalid moments.

## Failure Analysis And Next Decision

This improves classical falsification of fake moment witnesses. It does
not construct a native solution, improve measured larger-root pair recovery,
or supply a new quantum receiver. Classical native-valid constraints are
dequantization baselines, not quantum signals.

The obvious trap is appending one violated cut after another to one known
empty prefix. First challenge completeness of the inequality vocabulary
with a bounded exact categorical-polytope counterexample search. Keep the
full local LP as proof authority if the event family is incomplete. Then
demand fully charged fresh-target decoder leverage before further integration.
Finally distinguish the current classical helper's sufficiency from necessity
for the quantum goal; an alternative direct quantum receiver may be a higher
upside direction. See `NATIVE_TERNARY_EVENT_FAMILY_TARGET.md`.
