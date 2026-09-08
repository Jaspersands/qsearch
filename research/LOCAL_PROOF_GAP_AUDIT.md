# Local Proof Gap Audit

The full-suite failures exposed a false dependency claim in
`self_dual_wreath_systematic_stopping_core_no_go.py`: it asserted that every
nonempty high-codimension face had primitive/quadratic loss, although
`self_dual_wreath_high_codimension_face_word_frontier.py` explicitly leaves
cubic-overlap words open. Worse, its universal gate remained true when its
own finite audit failed.

Among 512 normalized colorings with information width 2 and check width 3,
four proper colorings lack the claimed local loss certificate. One table,
indexed by binary integer information coordinates, is

    (000, 110, 011, 111).

Its canonical relator is `(-3,-2,-1,2,3,1,2)` with occurrence profile (2,2,3).
This is a missing proof case, NOT a counterexample to the desired group-word
bound. Finite Whitehead primitivity cannot supply a growing-width theorem.

## Independent Route

The repository already has a stronger, separate single-fiber BABA argument.
Full codeword identities plus the suffix entropy lemma eliminate at least r
appended generators. A Nielsen substitution absorbs the residual coefficient
into a fixed genus-two relation, giving the bound d+4 without classifying
local cubic words. All four missing local examples pass its explicit
suffix-elimination and coefficient-absorption checks. This does not replace
independent mathematical review of the general argument.

The repair therefore withdraws the old local proof, not the independently
supported global research exclusion. Reports retain all four colorings and
their global checks; the negative registry records the invalid inference.
No speedup gate opens.

## Research Consequence

Do not spend more search on local cubic escape words for this already covered
single-fiber BABA scope. The broader lesson is that report gates need explicit
evidence dependencies, not hardcoded booleans or summary text. A next
high-leverage infrastructure pass should validate such dependency contracts
and distinguish a failed diagnostic, an unresolved proof case, and an actual
counterexample. Existing record counts and registry validity do not establish
mathematical consistency.

## Dependency Contract for the Next Pass

Implement the following semantics before bulk wiring more theorem records:

- A claim has an explicit domain, quantifier, input model and conclusion.
  A finite diagnostic and a uniform theorem are different claim IDs.
- Proof routes are alternatives (OR); premises within one route are required
  together (AND). A broken local route cannot invalidate an independent global
  route. Conversely, an independent global route cannot retroactively validate
  a false statement about the local proof.
- Evidence levels are distinct: observed, exact-finite, derived-review-pending,
  and machine-checked with a named checker. Passing numerical controls never
  raises a universal claim's evidence level.
- Dependencies reference explicit claim IDs and source/artifact hashes, not
  status substring matches or counts of successful experiments. Changed
  provenance makes a route stale until rechecked.
- An unresolved premise blocks that route. A counterexample requires a
  replayable witness to the stated conclusion. A failed search supplies neither.
- Audit contradictions without silently rewriting scientific conclusions.
  Reports must preserve both the original claimed gate and the reason it is
  not justified, then an explicit repair supersedes the invalid record.

Acceptance fixtures: the historical systematic local gate must be flagged;
its four cubic words must remain unresolved locally; the independent global
BABA route must not be invalidated by that gap; the encoded isometry must
not imply a decoder; and the fixed-reference identification bound must not
transfer to binary decision. These are semantic tests, not merely JSON-shape
checks. Start with these live routes before any broad automatic migration.
