# Two-Level Cubic SDE Contraction

28 October 2026. Constructive mathematical argument and exact arithmetic
implementation. Not a novelty certificate, a quantum speedup, or a
kernel-verified replacement for the supplied policies in ReesMeasuredReceiver.

## Decision And Input

Argon's review asks whether IID measured character labels admit a smaller
diagonal-equation batch. The first necessary comparator was already in
this repository: Ivanyos--Santha Proposition 10 uses
`(r+1)(3r+1)(9r+1)` columns, not the larger general-degree collision bound.
The question pursued here is constructive and stronger than an average-case
experiment: can the third collision level be removed for ANY public labels?

Given a prime p>3 and columns v_i in F_p^r, find a nonzero scale vector s
with `sum_i s_i^3 v_i = 0`. The matrix is the actual saved public character
record. There is no hidden-subgroup input, supplied solution, or permission
to replace a difficult label tuple. Row compression is allowed, but the
output is checked on the original equations and every input index retained.

For p=2 mod3 the existing inverse-cubing linear solver already needs only
r+1 columns. For p=1 mod3 the following construction needs

    M_3(r) = (r+1)(2r+1).

It uses randomized expected-polynomial finite-field arithmetic and a
constant-success scalar sampler. Capped sampling can return explicit
failure; this is not a deterministic total witness policy at that cap.

## Two Collision Levels

Use the first two levels of the existing construction from
[Ivanyos--Santha, Proposition 10](https://arxiv.org/html/1503.09016v2).
Let z1,z2,z3 represent the three nonzero cube cosets. Each block of r+1
input columns has a nonzero linear relation. Classifying its coefficients
by cube coset writes three vectors w_i as disjoint cube-weighted sums,
with `sum_i z_i w_i=0`. Multiply the relation by a nonzero scalar so its
first coset cell is nonempty.

Take 2r+1 such disjoint blocks. Their concatenated triples lie in the kernel
of `(u1,u2,u3) -> z1*u1+z2*u2+z3*u3`. This map is surjective onto F_p^r,
so its kernel has dimension 2r. Thus take another nonzero linear dependence,
classify its coefficients by
cube coset, and normalize a nonzero coefficient to the second coset.
This produces nine vectors w_ij with pairwise disjoint original supports,
each represented with nonzero cubic coefficients, satisfying

    sum_i z_i w_ij = 0 for each j,
    sum_j z_j w_ij = 0 for each i.

The cell w_12 has NONEMPTY REPRESENTATION SUPPORT. Its vector value need
not be nonzero. This distinction is sufficient and essential below.

Define D_ij=w_ij-w_ji for i<j. Subtracting corresponding row and column
relations gives

    z2 D_12 + z3 D_13 = 0,
   -z1 D_12 + z3 D_23 = 0.

Consequently, for any scalars a,b,c,

    z3 (a^3 D_12 + b^3 D_13 + c^3 D_23)
      = (z3 a^3-z2 b^3+z1 c^3) D_12.

The tests verify the stronger polynomial identity with the two row/column
defects retained; it does not rely on numerical matrix examples.

## Scalar Curve And Constructive Clock

Consider the projective plane cubic

    z3 a^3 - z2 b^3 + z1 c^3 = 0.

All coefficients are nonzero and p>3, so its three partial derivatives
cannot vanish simultaneously at a projective point. It is a smooth,
geometrically integral plane cubic of genus one. Apply the curve version
of Hasse--Weil, not an elliptic-curve theorem that first assumes a rational
base point: it has N>=p+1-2 sqrt(p) rational points. See
[Poonen, Corollary 7.2.1 and Corollary 5.12.22](https://math.mit.edu/~poonen/papers/Qpoints.pdf).

Every nonzero solution has a,b,c all nonzero. Otherwise a ratio between
two distinct cube cosets would be a cube; the minus sign cannot help,
because -1 is itself a cube. Thus ALL N projective points have a unique
representative with a=1, and each successful b has exactly three c roots.

Draw b uniformly from F_p. Test whether `(z2*b^3-z3)/z1` is a nonzero cube
using modular exponentiation; when it is, extract and verify a cubic root
c. A draw succeeds with probability

    N/(3p) >= (p+1-2 sqrt(p))/(3p) >= 1/9,

because p=1 mod3 and p>3 imply p>=7. For the last inequality, write
t=sqrt(p): `2t^2-6t+3>=0` for t>=sqrt(7).

After K independent draws, scalar sampling exhaustion has probability at
most (8/9)^K. The separate nonresidue sampler fails with probability at
most 3^(-J) after J independent uniform nonzero draws. A union bound is
`3^(-J)+(8/9)^K`; this holds conditional on every input label matrix.
Seeded controls are reproducible tests, not evidence of independence.

FLINT's degree-three root computation remains an expected-time dependency.
The wrapper's primality check and uniform-integer random source are also
not individually clocked or complexity-certified here.
These caps are NOT a total wall-clock, bit-complexity clock, or a formal
proof of the backend's runtime. No field scan, discrete logarithm,
factorization of p-1, or genus-one point-counting algorithm is required.
The point bound proves the simple sampler's success; the algorithm does
not compute N. Arithmetic retries operate on saved labels, not new sources.

## Returning A Nonzero Witness

Multiply the original root weights in cells 12,21,13,31,23,32 by
`a,-a,b,-b,c,-c`, respectively; all diagonal cells get zero. Cubing these
scales implements the skew contraction. The scalar curve equation and
the two axis relations imply the desired zero moment.

Nontriviality follows from the nonempty support of cell 12, a=1, nonzero
root weights, and pairwise disjoint supports. It does NOT require D_12 or
any cell vector to be nonzero. Unused inputs keep zero scales and remain
charged to the acquired quantum bank.

## What This Changes

The new alternative reduces the cubic-stage label budget from O(r^3) to
O(r^2), without assuming random columns. For example, rank 8 needs 153
columns rather than 16425. This is a constructive answer to the quadratic
arity target for degree three, subject to the proof/dependency scope above.

It is classical arithmetic used INSIDE a quantum source-conversion step.
It neither obtains those sources nor dequantizes the full receiver.
General-degree arity, original input preparation, arbitrary native hard
applications, gate complexity, noise, and human validation remain open.
The existing global resource reports are conservative and were not
silently rewritten; no practical or cryptanalytic claim is enabled.

The old three-level construction remains as a published comparator.
The existing Bezout/weighted-erasure controller now dispatches reduced
exponent three to the two-level method and budgets `(r+1)(2r+1)` inputs.
Degrees 3,9,15 and the original degree-d moment are regression-tested.
This does not expand the controller's unsupported higher-coset or
p=1 mod4 quadratic regimes.
Novelty of this two-level composition has not been established by the
targeted literature search. Its ingredients are standard. Do not describe
it as a new published theorem or a Shor-level discovery.

## Falsifiers And Controls

- Exact symbolic identity with explicit row/column defects.
- Exhaustive scalar success and coordinate-boundary checks for all
  noncube representatives at ten primes from 7 to 97.
- Full-rank matrices through rank 8 and a 127-bit three-coset prime;
  every returned witness checked against its original matrix.
- Degenerate/zero/repeated columns, rank compression and unused indices.
- Wrong field/coset promises, corrupt roots, invalid randomness, and
  exhausted scalar sampling fail closed.
- Existing F7 full regular-operator descent and Fourier readout with the
  new witness: six cubic inputs rather than eighty, then nine quadratic
  inputs, for the nonnormal lines X+W and Z+W. These selected legal records
  are not IID success statistics, a new source oracle, or all-record tests.

Run `python qsearch.py cubic-sde --write` for both arithmetic comparators,
and `python -m theorems.rees_complete_instrument --write` for source controls.
The standalone outputs remain research evidence, not promoted candidates.

## Review And Verification

One independent read-only reviewer found no algebraic flaw. They checked
the contraction signs, nonempty-support invariant, genus-one point bound,
absence of coordinate-axis points, retry probabilities and the published
comparator. They also supplied the rank-2r argument tightening the parent's
initial `(r+1)(3r+1)` bound to `(r+1)(2r+1)`; the parent incorporated and
independently tested it. Their separate scalar enumeration covered 1,352
noncube representatives at eligible primes through 199 without a failure.
That is an automated review and a bounded check, not human validation.

The reviewer emphasized the unclocked root/primality/random-source
dependencies and the need to include BOTH sampling-abort terms. No direct
subsuming theorem was found in the inspected sources, but novelty remains
unestablished. No external outreach is authorized or performed.

Final verification used `/opt/anaconda3/bin/python` with pytest plugin
autoload disabled and an external bytecode-cache prefix:

```text
python -m pytest -q -p no:cacheprovider -W error \
  tests/test_cubic_two_level_contraction.py tests/test_cubic_diagonal_solver.py \
  tests/test_weighted_two_erasure_cascade.py tests/test_central_quotient_receiver.py \
  tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py \
  tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py \
  tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py \
  tests/test_prime_power_rees_descent.py
```

**209 selected tests passed in 14.78 seconds.** The final suite follows a
failed intermediate run whose one failure was a stale test expectation
of 21 columns instead of the refined 15 at rank two. The expectation and
fixture were corrected and the entire selected suite rerun, not ignored.
Separately, `tests/test_cli_parser_integrity.py` and
`tests/tools/test_split_cli.py` passed all **54 tests in 20.47 seconds**.
These are 263 selected tests, not the entire repository suite.

Python syntax checks passed for all eight new/modified Python files.
All twelve actual `site/js/*.js` files passed `node --check`; none changed.
All three live workflows above (including the weighted-cascade workflow
`python -m theorems.weighted_two_erasure_cascade --write`) passed and
regenerated their existing reduction JSON artifacts. `qsearch.py validate`
returned `valid: true, issues: []`. No registry claim status was promoted.
Whitespace checks passed. No Lean file changed or Lean verification was
claimed for this contraction. No Git commit/push or external contact.

Changed code: `theorems/cubic_diagonal_solver.py`,
`theorems/weighted_two_erasure_cascade.py`,
`theorems/rees_complete_instrument.py`, `qsearch.py`,
`qsearch_cli/registry.py`, and new `qsearch_cli/commands/sde.py`.
Tests: new `tests/test_cubic_two_level_contraction.py` and one updated
controller-budget assertion in `tests/test_cubic_diagonal_solver.py`.
Documentation: this note, README, the original cubic note, Argon review
disposition and agent handoff. The three regenerated artifacts are
`research/reductions/{cubic_diagonal_solver,rees_complete_instrument,weighted_two_erasure_cascade}.json`.
Argon's original review retains SHA-256
`78a1ce07a17bf5bb2d6fdd0ddc72c2eaa3983dbe5f7d856da901094825b73aac`.

Final algorithm SHA-256:
`9bbe4b908a8208f1fec7df333c7d91552596f1196bc446871c417325c277b093`.
New tests SHA-256:
`c54461326d534c9f2c7b8c8d167afd2d660260560eb7c34e4aef93fa103d6db1`.

## Next Scientific Gates

1. Obtain specialist scrutiny and finish a broader prior-art search; the
   independent automated mathematical check above is complete, not human review.
2. If it survives, connect a properly clocked randomized solver to the
   formal receiver's total-policy premise. A success-only identity cannot
   silently erase abort branches.
3. Compare a linear-arity constructive method against this all-input
   quadratic comparator. Random-kernel rejection or a point-count
   existence argument alone is not such a method.
4. Reassess a meaningful native hard application before more nearby
   implementation or formalization. Improved arithmetic is not that application.
