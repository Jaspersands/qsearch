# Three-Block Native Realizability Beyond PSD

LOCAL DERIVATION / REVIEW PENDING. Scoped exact classical inequalities,
not a scalable native decoder, source-population theorem or quantum speedup.

## Decision

The retained PSD/native relaxation gap is NOT even three-block realizable.
All364 triples of its14 original blocks were tested:327 have exact local
extensions and37 have exact non-PSD obstructions, with ZERO unknowns.
This explains one defect of the degree-two PSD model without attributing
native realizability to a positive moment matrix.

Every discovered inequality simplifies to coefficients -1,0,1 in the
original pair variables. The37 cuts have167 nonzero original coefficients
in total. They reject the saved PSD witness, but adding all37 in one bounded
re-solve still yields an exact fractional continuation, now indefinite.
The intersection of these local constraints with full PSD remains UNKNOWN.
No whole-prefix elimination or witness recovery was obtained.

## Derivation And Scope

For each sorted triple of original blocks, enumerate its retained digit
assignments (at most27). Let t be a probability table on those assignments.
The three pair tables extracted from the exact full p/J witness form b;
the 0/1 marginalization matrix is A. A necessary native condition is

```
A*t=b, t>=0, sum(t)=1.
```

Pair normalization follows from the original verified model. Exact primal
certificates nevertheless check total probability one explicitly.
An exact signed marginal dual with A^T*y>=0 and b^T*y<0 proves no triple
distribution exists. Crucially, A^T*y is checked on EVERY local native
assignment; the induced inequality y.b>=0 is therefore valid for every
original native word and any genuine global distribution. It is not another
PSD square cut and imposes no hull-specific zero constraint.

Feasible distributions on327 separate triples do not form a global native
distribution. Thirty-seven failed triples reject ONE supplied PSD point,
not all feasible moment points or the whole SDP. No skipped/reconstruction
unknown triple is counted as feasible.

The proof control uses three binary blocks with pair correlation -2/5.
Their degree-two indicator matrix is PSD, but every binary assignment obeys
the triangle correlation sum >=-1, whereas these marginals sum to-6/5.
This is only a verifier control, never an oracle algorithm candidate.

## Live Experiment

Source: the exact full moment array retained by
`ternary_psd_support_lift.json` at target11366831/winding3. Its PSD mixture,
original source/domain/winding equations and native emptiness are independently
replayed by the upstream checker before local certificates are accepted.
The new report pins the full support-report SHA256.

Complete schedule:364 triples,327 exact extensions,37 exact dual obstructions,
401 tiny LP calls. The recorded complete scan takes approximately10.7seconds,
including repeated original-point rechecks; source compilation is additional.
All row/column certificates are exact FLINT rationals. HiGHS proposes only.

One explicitly capped re-solve (budget64,37 actual cuts) appends nonnegative
slacks for all discovered inequalities. The whole model has898 nonnegative
variables,855 equations and9,402 nonzero entries. One LP and one exact primal
reconstruction yield a valid continuation; exact positivity auditing finds
it indefinite. Recorded analysis approximately0.96seconds, excluding scan,
source preparation and positivity audit. No global dual was obtained.

Local slacks are not indicator variables. `word_moments` supports them so
every honest native-word control still satisfies every appended inequality.
The independent BigInt checker rebuilds the entire triple schedule and
marginalization matrices, checks all327 normalized distributions, all37
strict duals, primitive integer inequalities, full strengthened primal array
and its negative quadratic form. No floating tolerance has proof authority.

## Reproduce

```sh
python theorems/ternary_local_marginals.py --write
node research/certificates/ternary_local_marginals_crosscheck.js
PYTHONPATH=theorems python -m pytest -q tests/test_ternary_local_marginals.py
```

Sixteen focused tests cover PSD/nonlocal-realizability controls, exact local
extensions, all honest local assignments, local-slack/matrix compatibility,
strict rational violations, winding/index/model tampering, fake numerical
success, honest full-model continuations, explicit cut caps and rejection
of transplanted assignment tables or pair-column indices.

## Critique And Research Budget

The cheap inequalities are useful structural information. Their discovery
does not yet justify runtime decoder integration: dense conditional moment
construction is still substantially more expensive than evaluating a cut,
and the selected prefix was already known empty by an exponential reference.
Rejecting its fake witness is not evidence of source-law pair finding.

The next diagnostic may combine these local inequalities with PSD while
preserving EVERY row/slack/winding. It must be a bounded test of a distinct
joint constraint system, not unlimited square-cut inflation. A further exact
joint continuation would be a stronger scoped gap; a full fixed-winding dual
still would not establish whole-prefix exclusion or a decoder speedup.

Before expanding to generic higher-degree moments, demand evidence that the
constraint family improves actual native search per fully charged unit of work
on fresh targets and larger roots. Otherwise divert effort to the missing
source-law two-witness mechanism rather than repeatedly classifying this prefix.
See `NATIVE_TERNARY_JOINT_REALIZABILITY_TARGET.md`.
