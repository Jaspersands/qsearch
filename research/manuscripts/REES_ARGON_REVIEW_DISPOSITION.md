# Disposition of Argon's Rees Review

27 October 2026. Targeted response to `REES_REVIEW_RESPONSE.md`, not a new
complete proof audit, human review, or novelty certificate. The received
review is preserved unchanged, including its qualifications and errors.

## Provenance

All three supplied SHA-256 fingerprints matched the files at intake:

- Manuscript: `dc92967068ef507c48fc5dc9ea8d9e5685d13219920b51df3fc01ba6ad4bb31f`.
- Correctness review: `74a46bd40517fc648c70c48b696b28fdeccd4b67576a7f7133338e6ccb056f24`.
- Prior-art review: `9a9e9d484d091c7a90e88b313d8774f050ca9dc7b9a82d0d63f2d45fe17e2f31`.

The first hash identifies the pre-edit manuscript reviewed by Argon, not
the manuscript after this pass. Historical review evidence is not rewritten.

## Corrections To The Review

### R1: BCH Denominators

Sections 1.1 and 1.3 of the review say BCH denominators divide `c!`.
This is false: at class three the coefficient `1/12` occurs, and 12 does
not divide 6. For example, with `X=E12+E23`, `Y=E34`, the `(1,4)` entry of
`log(exp(X) exp(Y))` is exactly `1/12`.

The needed statement is weaker: denominator prime factors are at most c,
or equivalently the coefficients lie in `Z[1/c!]`. That suffices for
reduction modulo p when `p>c`. The manuscript already states this correctly;
do not replace it with the review's stronger assertion. The new exact
rational-matrix control independently evaluates the truncated exp/log.

### R2: Sufficient Arity Is Not A Lower Bound

The review correctly notes that `dim(H)<=1` leaves central character support
dimension at least `r_d-1`. This does not prove its next assertion that the
labels "still require" the full `B_d(r_d)` batch size. A finite random batch
also need not span its support. The conclusion justified here is only that
the order-p reduction does not by itself supply a smaller worst-case
schedule for the existing collision construction.

For a direct countercontrol to rank-based necessity, when
`gcd(d,p-1)=1`, ANY nonzero ordinary linear-kernel vector can be converted
coordinatewise to d-th powers using the inverse exponent. More than r
columns suffice for an r-row system by Gaussian elimination. Full rank r
does not force the much larger collision bound. This is the already-known
exponent reduction, not a new SDE algorithm. The tests use full-rank systems
and the production witness-lifting routine.

Likewise Section 2.2 changes a published `O` parameter guarantee to
`Omega` runtime language. The cited paper's remark supplies
`p^{O(p^2 log p)} n^{O(p log p)}`, not a lower bound on all algorithms.
The uniform worst-case binary zero-sum length obstruction is a separate
statement; it does not establish that SDE or HSP requires the displayed
runtime. See [Imran--Ivanyos, Theorem 2 and following remark](https://arxiv.org/html/2304.08376v1).

### R3: Classical Filters Have Promises

Section 3.1's blanket wording about succinct polynomial-circuit stabilizers
is too broad. `POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md` pays the orbit
rank; polynomial input time follows when that rank is polynomial.
`MOORE_GRADIENT_CLASSICAL_FILTER.md` recognizes a specified semantic family
and explicitly excludes a universal high-degree stabilizer algorithm.
Neither establishes that every arbitrary succinct circuit case is easy.
Conversely, escaping those filters establishes neither hardness nor a
useful native reduction. Those application questions remain open.

### R4: Formal Coverage Must Follow Compilation And Assumptions

The interpolation draft was explicitly unverified at intake. Merely moving
it into the default build does not certify the Rees theorem. Its tuple
theorem assumes evaluation homomorphisms and their coefficient identity.
Those must still be derived from the concrete Lie/BCH construction.

For the central step, the intended advance is to divide the projected
coefficient by the cardinality of `embed^-1(H)`, not just remove a
transversality hypothesis from the old trace-one theorem. Allowed characters,
nonempty active tensors, source independence, support preservation and
phase cancellation remain separate obligations. Full projector physics,
Lazard transport, SDE runtime, recursive clocks and the whole HSP theorem
are not made kernel-verified by these interface identities.

## Accepted Manuscript Changes

1. Explain that base-two sample slack is a conservative prime-independent
   replacement for base-p slack.
2. Identify the scalar Fact 2 solver as deterministic, so the ring branch
   does not silently omit a solver-failure budget. This matches the
   [primary statement](https://arxiv.org/html/1503.09016v2).
3. Distinguish making an abelianization elementary abelian from restricting
   a local order-p problem to its exponent-p subgroup. Keep the latter
   public algorithm as an explicit imported obligation. Lazard additive
   coordinates can expose p-torsion when actually available; they are not
   free for a general-exponent black-box input. See
   [Ivanyos--Sanselme--Santha, Lemma 3](https://arxiv.org/html/0707.1260v1).

For the third point, exact controls at p=3 and p=5 use
`C_(p^2) semidirect C_p`, with action `a -> a^(1+p)`. It has central
commutator subgroup of order p and elementary abelian abelianization, but
contains an element of order p^2. Its order-dividing-p subgroup is proper.

## Research Decision

Use the review to improve precision and formal coverage. Do not promote
the claim to proved, novel, practical, or human-reviewed. The core proposed
composition remains worth specialist scrutiny; this pass does not repeat
the entire correctness or literature audit. No one was contacted.

Random-column SDE improvements are a legitimate separate research question,
but the first gates are the effective degree `gcd(d,p-1)`, actual measured
label rank, and a paid constructive algorithm. Existing exponent-one cases
and easy cancellation controls must not be presented as new discoveries.

## Executed Checks

From the repository root, with the existing Anaconda Python 3.13.5:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-argon-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py
```

**121 selected tests passed in 11.65 seconds**, including six new controls.
An earlier five-file subset also passed all 82 tests. These counts are not
a claim that the entire repository test suite was run.

```text
env PYTHONPYCACHEPREFIX=/tmp/qsearch-argon-review-pycache /opt/anaconda3/bin/python -m py_compile tests/test_rees_review_controls.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-argon-review-pycache /opt/anaconda3/bin/python qsearch.py validate
git diff --check
```

These checks passed. Registry validation returned `valid: true`, `issues: []`
with 8 candidates, 796 experiments, 807 results and 973 negative results.
No registry evidence status was promoted. The desktop LaTeX compiler
returned `kind: success` for the updated manuscript; no PDF was exported.
No UI/JavaScript was changed, so no Node check is claimed.

Intake review SHA-256, preserved unchanged:
`78a1ce07a17bf5bb2d6fdd0ddc72c2eaa3983dbe5f7d856da901094825b73aac`.
Updated manuscript SHA-256:
`5a03d7f15fbd319ab11efd888c044f1b97d8cb46bbeaf9503f3acbdc6b9042d0`.
New countercontrols SHA-256:
`9e3457ff152207ef12601845c480294dcc9bd718d45e2d5a6d9849fb4315aeb7`.

## Completed Formal Integration

One delegated implementation pass was restricted to `formal/`; the parent
reviewed the resulting definitions, assumptions and proof composition.
The former draft is now `formal/Formal/ReesHomogenization.lean`, imported
by the default library. Nine promoted theorems and eleven new
central-descent theorems are explicitly included in the global axiom audit.

The main new specialization is `normalized_descent_output`. It uses
`normalized_source`, whose denominator is the actual projected branch
trace, and `normalized_correlation_at`, which cancels the full preimage
multiplicity. It does not assume trace one for the old unnormalized kernel.
See `formal/README.md` for the full theorem list and remaining premises.

From `formal/`, using the pinned toolchain's `lake` executable, all passed:

```text
lake --no-cache build Formal.ReesHomogenization Formal.CentralCharacterDescent --wfail
lake --no-cache env lean -DwarningAsError=true Formal/ReesHomogenization.lean
lake --no-cache env lean -DwarningAsError=true Formal/CentralCharacterDescent.lean
lake --no-cache env lean -DwarningAsError=true Formal/Audit.lean
lake --no-cache build --wfail
```

The parent independently repeated the final default build: exit 0,
`Build completed successfully (3473 jobs)`. This count includes cached
dependencies; it is not a count of new proofs. Local and global guards
permit only `propext`, `Classical.choice`, and `Quot.sound`, with no
`sorryAx` or additional axioms in the guarded dependencies. No toolchain
installation or dependency update was needed. The delegated agent is closed.

Final formal-source SHA-256 fingerprints:

```text
680b9adde996e4d8b0d99d3f1fc0e9cad3ed892f92373e1f2c45960cb6c10220  Formal/ReesHomogenization.lean
b986537de027db95b63969b68cbfcc4f87182683daf3098a3ce1011acf4b7251  Formal/CentralCharacterDescent.lean
ec15366f54900de192a59432e3799f26c002ea98459439a189c2de4a4d267a79  Formal/Audit.lean
```

## Changed Files

| Path | Change |
| --- | --- |
| `formal/drafts/ReesHomogenization.lean` | Removed after promotion; no duplicate unverified draft remains. |
| `formal/Formal/ReesHomogenization.lean` | Promoted, repaired import/proof elaboration, added axiom guards. |
| `formal/Formal/CentralCharacterDescent.lean` | Added allowed-label normalization and nontransverse channel specialization. |
| `formal/Formal.lean`, `formal/Formal/Audit.lean` | Default-build import and guards for all new theorems. |
| `formal/README.md` | Documents exact formal scope and checks. |
| `tests/test_rees_review_controls.py` | Six exact countercontrols for the review's overstatements. |
| `research/manuscripts/rees_hsp_review.tex` | Three exposition clarifications; no new theorem claim. |
| `research/manuscripts/REES_ARGON_REVIEW_DISPOSITION.md` | This intake, correction and verification record. |
| `research/manuscripts/REES_REVIEW_BRIEF.md`, `REES_REVIEW_VERIFICATION.md` | Link later changes without rewriting historical review evidence. |
| `research/REES_HSP_REDUCTION.md`, `research/AGENT_HANDOFF.md` | Replace stale formal status and record the checkpoint. |

Argon's original review is unchanged. No commit, push, outreach, UI change,
or registry claim promotion was performed in this pass.

## 28 October Follow-Up: Cubic Arity

The random-column suggestion led to a constructive all-input cubic result:
[two-level curve contraction](../CUBIC_TWO_LEVEL_CONTRACTION.md) uses
`(r+1)(2r+1)` public columns. It combines the first two levels of the
published cubic scaffold with a genus-one scalar equation, and does not
assume IID labels. One independent automated reviewer found no algebraic
flaw and tightened the second-level rank bound. Exact controls and source
replays are recorded in the linked note. General degree, total clock,
formal policy construction, human review and novelty remain unresolved.
This does not retrospectively turn the review's asserted arity lower bound
into a valid statement; Argon's supplied document remains untouched.

## 28 October Follow-Up: General Fixed Degree In Large Fields

The [symmetric contraction](../POWER_SDE_SYMMETRIC_CONTRACTION.md) now gives
`(r+1)*((d-1)*r+1)` columns for ANY fixed reduced degree d>=2, including
even d, when `d | p-1` and `p>=16*d^(2*d+2)`. It does not need the IID-label
promise suggested by the review. Both axes of a two-level collision tensor
are annihilated using a symmetric coefficient matrix of nonzero dth powers;
a prescribed-coset character-sum bound supplies the scalar coefficients.
The [odd exterior method](../ODD_POWER_EXTERIOR_SDE.md) remains a lower-field
fallback. This is not a general-prime quadratic solver or a novelty claim.

One independent automated reviewer checked both mathematical constructions
and then the symmetric implementation, finding no defect under the stated
promises. The parent executed exact arithmetic and weighted-phase controls.
The unresolved total-clock/aborting-policy, general receiver, native hard
application, human review and novelty obligations remain. No one was
contacted; the reviewed source document and historical snapshots are unchanged.
