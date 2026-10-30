# Quadratic Cancellation At Every Odd Prime

## Established Scope

`quadratic_cancellation.py` implements the published quadratic SDE construction
over every odd prime field. Its input is an explicit public moment matrix;
its output is a nonzero, exactly checked vector of square-root coefficients.
This is classical arithmetic for the proposed Rees receiver, not an algorithmic
discovery or evidence of classical hardness.

The actual gap was narrower than initially stated: the repository ALREADY has
`nil3_guarded_cyclic_dispatch.square_weights_capped` for `p = 3 mod 4`, with
the same polynomial bank size. The new coverage is `p = 1 mod 4`, where
`weighted_two_erasure_cascade.required_bezout_arity` currently rejects degree
two. No arity improvement is claimed over that existing specialized solver.

The local implementation now supplies both the missing coverage and an
explicit pre-observation rank-cap contract. It does not modify the migrating
checkout or its existing dispatchers.

## Construction And Checks

The construction is [Ivanyos--Santha, Proposition 9](https://arxiv.org/html/1503.09016#S2.SS1).
Split a linear dependence into square and nonsquare coefficient classes using
a nonsquare `zeta`. Disjoint represented vectors then obey `w1=-zeta*w2`.
Repeat on `r+1` groups, then on their first representatives. The four cells
satisfy `w11=zeta^2*w22` and `w12=w21=-zeta*w22`. A ternary quadratic
`zeta^2*a^2-2*zeta*b^2+c^2=0` combines them with square coefficients.
Empty-class cases return a nonempty zero representation before this last step.
All supports are disjoint, so the final nonzero scalar witness cannot cancel
its own support. This uses at most `(r+1)^2` original columns.

The implementation checks each represented vector by expansion, all four
cell identities, and every original equation after undoing rank compression.
It reuses the existing smooth-power root and bounded scalar backends. A
generator of the 2-primary subgroup is a nonsquare, so full factorization of
`p-1`, a full-field root table, and FLINT polynomial roots are unnecessary.

## Resource Contract

For security parameter `s`, root setup has at most `s+1` field draws and
conditional failure probability at most `2^(-s-1)`. If the four-cell branch
is reached, its scalar backend has failure allowance `2^(-s-1)`. The union
bound is at most `2^-s`, including adaptive public coefficients. This bound
requires independent uniform field draws; deterministic seeds only replay
arithmetic. At most `7*s+13` field draws are requested by the entire solve.

These are bounds on the explicit algorithm's field-draw loops, NOT a wall-clock
deadline for Python, FLINT primality preflight, or `SystemRandom.randrange`'s
internal bit rejection. The prime is an input promise for the mathematical
complexity claim. A fully clocked bit-level implementation must budget those
operations separately. The small-field scalar branch enumerates only
`p <= 256`; the large-field branch never enumerates the field.

Admission requires `(rank_cap+1)^2` already acquired columns. The observed
rank may reduce the selected prefix, but never reduces the acquired-copy bill.
`used_prefix_columns` records the allocated prefix, not necessarily nonzero
support or the number of groups inspected before an early return. Zero scales
and unused suffix columns remain charged. No labels are resampled.

| Rank | This bank | Scalar-recursive bank |
|---:|---:|---:|
| 1 | 4 | 3 |
| 2 | 9 | 9 |
| 8 | 81 | 6,561 |
| 16 | 289 | 43,046,721 |
| 64 | 4,225 | 3^64 |

The comparison is against the local scalar-recursive fallback, NOT against
the previous best mathematical SDE bound. At rank one the scalar solver is
strictly cheaper. A dispatcher should choose the public budget before source
acquisition instead of blindly replacing every specialized path.

## What This Unblocks

Together with the existing cubic implementation, the required degree-two and
degree-three arithmetic has polynomial-in-rank implementations at every
Lazard-valid class-three prime (`p>3`). If the two public caps are `R2,R3`,
the cancellation bank multiplier is

`(R2+1)^2 * (R3+1)*(3*R3+1)*(9*R3+1)` when `p=1 mod3`,
or `(R2+1)^2 * (R3+1)` when `p=2 mod3`.

These are multiplier bounds, not a complete query/gate bound: terminal
samples, each source's oracle cost, reversibility, precision, and outer
reduction costs must still be composed. The cubic backend uses expected-time
polynomial roots; this pass does not silently clock that backend. Degrees
with reduced power index above three remain unsupported by this pair.

## Falsification And Remaining Risks

- Exact arithmetic success could conceal an all-zero certificate: explicitly
  rejected, including an injected zero scalar result.
- Compression could discard a real equation: an injected false rank-zero
  result is rejected on the original matrix.
- Ordinary dependence could be mistaken for a square witness: an explicit
  F3 counterexample is tested.
- Large-prime success could exercise only the old regime: 127-bit primes
  `2^127-295` and `2^127-39`, both `1 mod4`, are included; the former is
  also `1 mod3`, where the cubic stage is nonbijective.
- Empty supports could invalidate the proof: both early exits and eleven
  forced four-nonempty-cell controls pass.
- RNG failure could silently fall back to enumeration: capped nonsquare and
  conic failures raise; bad roots and out-of-range RNG values also raise.
- A valid arithmetic primitive could still sit inside a false quantum proof:
  independent complete-reduction review and physical instrument integration
  remain open. Passing this suite cannot resolve either issue.

The next scientific task is not more random matrix sweeps. It is independent
review of the complete Rees reduction and a natural source with a genuinely
nontrivial matched classical baseline. Routine dispatcher integration is
specified separately for Gemini, after migration completes.
