# Verification: 2026-10-26

Workdir: /Users/jaspersands/Developer/qsearch-research-work.
Python3.13.5, python-flint0.9.0. This is an isolated non-Git research
workspace. The intended main local checkout was checked and remains absent.

## Observed Checks

- Initial focused suite:27 passed in0.93s.
- Final eight-bundle regression including29 new tests:264 passed in5.62s,
  warnings treated as errors, no skips. Suites: new tower; preceding AG
  affine sampler; USD; Schur; inverse-trace local-list, modular-norm,
  norm-transfer and residual-SAT.
- py_compile: tower_seed.py, elementary_cover.py, test_tower_source.py,
  verify_tower.py, exit0.
- verify_tower.py --write generated source certificate, actual two parity
  matrices, points, analytic residues and original-relation witness runs.
  Initial receipt SHA256:
  88c4db0e53f35c1eb0b5233ef139a8053b062a0f2f4b602bdd8ed791a24b624d.
- Earlier affine nine-hash and USD six-hash receipts replay unchanged.

All test commands disable external pytest plugin autoload and pytest's
cache provider, use -W error, and place bytecode under /tmp/qsearch-tower-pycache.
No full-repository tests, main qsearch validate, JavaScript check, main UI or
registry update, commit, or push was performed. Higher class fields and
their parity matrices were not generated.

## Exact Scope

Verified the143 square-root witnesses and22 finite base points, the
51887-step discovery replay, source-prime check, and exact sufficient
class-field criterion. Forged roots, targets, rank/margin claims and
admission metadata are rejected. The infinity, unramified-extension and
infinite-tower steps are written mathematics invoking the stated theorem,
not claims proved by unit tests.

The actual degree-eight near-canonical input is43-by-176, with square126,
cube173 and annihilator3. Native witnesses pass for54 test syndromes;
the receipt also replays six targets with both analytic and matrix-only
annihilators. These sets overlap. The original affine fiber and all176
nonzero constraints are verified, not merely an objective score.

The one-point83R control is constructed independently with624 monomials
and581 jet constraints. Its cube also has dimension173, and its original
matrix admits the same known solver. Neither test establishes asymptotic
one-point coverage or uniform sampling.

The function cancellation is checked over exact rationals and F100003,
with leading coefficient -27/32. The persistent higher-cover attack and
93-section bounded-mutation obstruction are written deductions; no scaling
experiment is substituted for those proofs.

## Independent Reviews

The user authorized independent reviewers whenever useful during this pass.
Two separate reviewers completed their work: one for the preceding USD
reduction, one for this tower/source/classical argument.

- tower-independent-review-2026-10-26/REVIEW.md accepts the scoped tower
  existence and deterministic classical solver. Independent checks recover
  the43-by-176 matrix, square126, cube173, annihilator3, dimension209 of
  L(3G), evaluation rank173 and kernel36. A separate solver verified546
  witnesses across78 targets and7 annihilators. The93-function section
  control and one-point83R control also passed. The reviewer shares the
  FLINT backend, generated no higher tower matrices, and did not independently
  repeat the entire264-test regression. The indexed Schoof primary text was
  checked; the direct PDF host timed out.
- usd-independent-review-2026-10-26/REVIEW.md accepts the exact ideal USD
  transfer and unique-decoder argument. Its workspace and restart-cost
  qualifications are incorporated in a NEW sidecar,
  usd-review-resolution-2026-10-26. Old USD files/receipt remain frozen.
  Current paper v2 was checked. No general decoder was compiled, and no
  exhaustive novelty conclusion follows.

TOWER_SOURCE.md and HANDOFF.md were updated after review, so the current
tower receipt is regenerated separately from the initial hash above.
No formal proof-assistant verification is implied by these reviews.

After the two reviewed documentation clarifications, the ten-hash tower
receipt replays with SHA256:
8c4914a390aed1c47ce1b7bb19f03692c5281a366786fab77266db5e27e3edf8.
Subsequent eleven-bundle regression including new review/class controls:
303 passed in5.62s. Earlier frozen USD, affine and Schur receipts remain
unchanged. This does not enlarge any of the geometric claim scopes above.
