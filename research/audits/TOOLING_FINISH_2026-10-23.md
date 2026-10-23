# Tooling audit continuation — 2026-10-23

Round-three findings recovered from Claude's saved workflow have been adjudicated and
the fixes integrated on `codex/finish-agent-tools`, starting at round-two head
`5b95375e`. The interrupted workflow's empty verification votes represented unfinished
work, not rejected findings. No round-three fixers had completed before the handoff.

Work was completed in a full local clone outside iCloud. The Desktop source, its four
historical worktrees, and the in-progress project migration were preserved. The migration
worker was paused while making the local clone, then resumed. At completion of the local
audit, the branch had not been merged or pushed. The user subsequently approved both;
publication checks are recorded below.

## Scope and disposition

| Area | Result |
|---|---|
| DQI screener | Exact Griesmer bound; saturation follows the source equation; stable finite packing; exact decimal-string integer inputs; bounded expensive inputs; general-density subfield checks; CLI overrides and input documentation. |
| Preflight | Linked-worktree index isolation; accurate source error paths; generated-table mutation checks including eager definitions; package resolution; controlled import output/SystemExit; explicit JSON/import scope. The single invalid LaTeX JSON escape was repaired without changing the decoded mathematical claim. |
| arXiv watch/judge | API completeness, retries, persistent gaps and track checkpoints; full abstracts for new records and conservative legacy handling; quote case/sign/prime/product integrity; export receipts and directory reuse refusal; reviewer/action provenance; offline render and broader number-theory vocabulary. |
| Corpus | Filed-ID/list limitations are explicit; no-match duplicate results include advisory neighbours; baseline vocabulary/citation fixes; complete JSON diagnostics; controlled held-out input failures; corrected historical calibration table. |
| Referee | Unclear reviews remain selectable; source qualifiers survive quote normalization; explicit cuts; smaller packets; truthful queue ordering; explicit stale-note exports; historical regressions no longer pin the mutable live review store. |
| Agent brief | Separate human decisions, judge proposals and actions needing clarification; expose watch checkpoints/gaps; prioritize old open kills; count actual registry rows and report duplicate IDs; report incomplete duplicate checks; reject invalid roots. |
| Integration | CI runs on research corpus changes; CLI verification avoids stale bytecode and rejects another checkout's loaded package; digest/queue/brief regenerated together. |
| Stored reviews | Audited the recovered reviews of all 28 previously flagged and six sound notes. Seven append-only correction rows were imported; the store now has 27 flagged and seven sound reviews, with no stale entries. |

The stored corrections are in
[`reviews/corrections/2026-10-23-r3.jsonl`](reviews/corrections/2026-10-23-r3.jsonl).
The source passages and artifacts were checked before changing them. Independent review
verified all 42 quotes, content hashes and overall verdicts in those seven rows. In
particular, the unit-orbit note's withdrawn gap concerned a sentence whose surrounding
paragraph already specified the saved native d64 scope; no general obstruction was inferred.

Duplicate raw findings were consolidated. Mutation-survival observations without an
incorrect result were checked directly rather than counted as product defects. The
PRIMAL_BABAI wording issue was already recorded in the review summary, so no duplicate
gap was introduced. Historical commit-prefix/style observations did not justify rewriting
existing history. The brief's quarantine issue filter was already present and retained.

## Additional independent review

Reviewers checked areas they did not implement. Newly reproduced defects received
regressions before their fixes:

- Finite packing at `m=2^53, n=36000, q=3` incorrectly returned radius 1263 instead of
  the exact 1264. Cancellation-resistant logarithms fixed the decision; independent
  exact integer comparisons and high-precision log checks were also run.
- Class bodies, decorators and function-default expressions could mutate generated
  tables while escaping the static guard; deferred function bodies remain out
  of scope.
- A fresh global watch date hid missing configured track checkpoints, and falsey invalid
  coverage metadata was silently defaulted away. Both now produce explicit diagnostics.
- Later valid referee imports still invalidated some historical claim assertions. Those
  assertions now use archived source rows and notes.
- A valid timestamp-based `.pyc` could hide an equally sized source edit during CLI
  verification. A fresh temporary cache prefix forces current source reads, with no
  bytecode writes. A separate path-prefix bug accepted sibling/nested checkouts.
- Repeated arXiv pages could falsely complete coverage; truncated stored abstracts could
  not recover from a matching full fetch; render-only rewrote JSON; quote normalization
  could erase subtraction. These paths now have regressions and scoped fixes. The final
  quote checks cover explicit and bare mathematics, unary signs, named operands and
  Markdown boundaries: 403 focused tests and 115 independently selected math/prose cases
  pass. Quote matching remains a lexical guard with documented prose ambiguity.

The first integrated run exposed five test-maintenance failures from combining the
changes (README section/provenance expectations and the removed broken-contract fixture).
They were fixed before final verification; the audit does not count that run as passing.

## Validation

- `python -m pytest -q tests/tools --durations=10`: **1,515 passed in 96.20 seconds**
  on local-audit code head `da26d045`, including the regenerated outputs. No test was
  skipped or left failing in that run.

- `python tools/preflight/preflight.py --imports --validate --json`: zero problems.
- Full lexical corpus rebuild: 2,233 source files and 10,614 documents; held-out retrieval
  18/20 in the top five, meeting `--min 16`, with no index issues.
- `python tools/arxiv_watch/watch.py --replay-seeds`: 52/52 seed consistency checks.
- Live CLI checks: radius-19 OPI remains unknown with its classical-witness warning;
  radius-32 is not viable; an exact copied negative returns exit 2 and its original ID;
  a Babai graph-isomorphism query does not acquire a lattice baseline merely from the name.
- Generated digest equals the render of stored state and verdicts; the brief records six
  adopted open actions and three actions awaiting clarification. Referee state is
  34 reviewed, 27 flagged, seven sound, zero stale.
- `git diff --check`: clean. Remote main was fetched at `f18baf61` and is an ancestor
  of this branch. The 261 commits from main through round-two head are preserved.

## Publication checks

The user approved merging and pushing. Main was fast-forwarded to `d07413aa` and the
remote ref was verified. The first push's CLI checks and Pages deployment passed, but
its Tools and research-snapshot jobs exposed two additional integration issues:

- The unconstrained `mcp>=1.16` dependency installed MCP 2, which removes the FastMCP v1
  import used by the server. `requirements-tools.txt` now constrains the supported major
  version to `mcp>=1.16,<2`. A new Python 3.13 environment installed MCP 1.30.0 and the
  latest compatible dependencies for verification; the earlier local environment had 1.16.0.
- `research/progress_snapshot.json` still counted 976 negative results. Regenerating it
  gives the current 975. Repeated snapshot/site generation reproduces the saved files.

The clean tools-only environment passes 1,511 tests in 92.00 seconds with four existing
optional-dependency skips; the full research environment passed all 1,515 earlier.
Its fresh corpus rebuild also retains 18/20 held-out retrieval with no index issues.
The website's 25 Python tests and seven JavaScript tests pass, JavaScript syntax checks
pass, and `tools/check_site.py` passes. Remote CI is checked again after publication of
this correction rather than inferred from the local results.

The next push passed snapshot validation and deployment, but Linux exposed five
platform-dependent test failures after collection succeeded:

- Three report comparisons required bit-for-bit floating-point reproduction. Measured
  Linux/amd64 versus macOS/arm64 differences were at most `3.35e-14` for capacity-source
  floats and `6.67e-16` for polar controls. The recursive comparison now allows absolute
  and relative float tolerances of `1e-13`, while requiring exact types, structure,
  integers, strings and finite values. Finite-readout eigenvector proposals differed by
  at most `1.55e-15`; they are checked against that same tolerance before replaying the
  saved exact radial weights. Every resulting rational certificate is still compared
  exactly. Adversarial checks reject a `1e-10` proposal change and even a `1e-60` change
  to an exact Rayleigh bound. Scientific source and saved reports are unchanged.
- Two spend tests assumed a small command must have a small process-lifetime RSS. Linux
  can include memory inherited from the launcher before exec. Measurement still uses
  `wait4` for the specific child; the documentation now states this limit. The regression
  against earlier-child contamination runs in a light subprocess. Both tests pass with
  a 350 MiB launcher, and a deliberately incorrect cumulative accounting control still
  fails the regression bound (330.3 MB versus 17.9 MB with correct accounting).

The numerical reproduction and comparator checks pass all 49 tests on macOS and Linux
amd64. The native Linux arm64 spend suite passes 60 tests with one existing optional
`zstandard` skip. Emulated amd64 produced a separate ENOEXEC/ENOENT discrepancy for a
plain-text executable, so native Linux and the actual GitHub runner are used for the
complete suite rather than changing command-error handling to accommodate emulation.

After integration, the complete tools suite passes **1,537 tests in 118.78 seconds**
on macOS with the full research environment, and **1,533 tests in 82.41 seconds** on
native Linux arm64 with four existing optional-dependency skips (NetworkX and
zstandard). These runs include the new comparator regressions. The final remote CI
result is retained with the publication evidence after pushing this report.

## Remaining scope limits

- The 27 flagged research notes remain research work. This audit fixes tools and review
  records; it does not establish the underlying algorithms or their claimed advantages.
- Three existing human arXiv actions name absent notes. Their original decisions and
  provenance are preserved and marked `action_pending_clarification`; they cannot be
  marked done until their targets are clarified.
- The watch was relabelled and rendered offline. Seven records changed label/tracks;
  saved fetch dates and abstract text were preserved. The 282 legacy cut abstracts remain
  visibly incomplete until actual matching-version text is fetched. No fresh arXiv
  coverage or paper-level judgment is claimed.
- The duplicate gate is lexical, and nearest neighbours are advisory. A multi-filed-ID
  batch may hide comparisons and reports that limitation. Passing it is not a novelty proof.
- Preflight's default JSON check parses its four documented directories; it is not a
  repository-wide schema validator. Import validation resolves generated lookup tables
  without executing every research command.

Recovery inputs, red/green logs, per-finding dispositions and independent-review evidence
are retained locally in `~/Developer/qsearch-finish-evidence/`, outside temporary scratch
storage. The regenerated [agent brief](AGENT_BRIEF.md), [referee queue](REFEREE_QUEUE.md),
and [arXiv digest](ARXIV_WATCH.md) describe the saved state.
