# Target-Adaptive Native Shell Decoder

LOCAL DERIVATIONS / REVIEW PENDING. This is an exact classical enumeration
baseline with native-geometry cuts, NOT a polynomial solver or new quantum
algorithm. The fixed-catalog collision bound does not apply to its
target-dependent repair choices.

## Known Baseline And Native Adaptation

Classical distance-ordered lattice enumeration is established methodology; see
[Schnorr and Euchner's primary paper](https://d-nb.info/1169615635/34).
The repository's local adaptation uses the exact original A2 coset and its
smallest shell. It does not reinterpret enumeration as a breakthrough.

For original native words, every integer coset residual has squared norm at
least R=6M; equality holds precisely at legal original ternary words. Thus
enumerating the entire CLOSED sphere at R finds the complete original fiber,
including empty and singleton fibers. No near-shell tolerance is allowed.

Write the exact GS coordinates at row i as x_i, the chosen integer coefficient
as c_i, and already assigned squared residual norm as S. The next coefficient
satisfies

```text
(x_i-c_i)^2 * ||R_i*||^2 <= R-S.
```

For x=a/b and squared interval radius p/q, compute
s=isqrt(floor(p*b^2/q)). The inclusive coefficient interval is
ceil((a-s)/b) through floor((a+s)/b). Ordering is by exact distance, not a
floating root. Lower coordinates are updated after EVERY branch. A cap counts
all tried coefficient nodes, including pruned branches, not only outputs.

## Necessary Native Cuts

Every native error block is one of (2,-1,-1),(-1,2,-1),(-1,-1,2). Since GS
rows lie in the A2 planes,

```text
3*sum_block min_digit R_i*[digit] <= <e,R_i*>
    <= 3*sum_block max_digit R_i*[digit].
```

This gives an additional exact coefficient interval. Let p be the residual
projection onto assigned higher GS rows, with ||p||^2=S. The remaining
residual u belongs to the unassigned prefix, ||u||^2=R-S. At each block j,
restrict its prefix orthogonal projector to the first two A2 coordinates,
giving G_j. For a possible native digit, r=(e_j-p_j) on those coordinates:

```text
minimum prefix energy compatible with this block = r^T G_j^+ r,
```

provided r is in range(G_j). The code handles rank-zero, rank-one and rank-two
cases exactly. If this minimum exceeds R-S, that digit is impossible. If a
block has no possible digit, the branch is impossible. Different blocks can
constrain the SAME prefix vector: their energy bounds MUST NOT be added.

Finally any true word satisfies <e,p>=S. With the retained block digit domains,
3*sum_block min p[digit] <= S <= 3*sum_block max p[digit] is necessary. Passing
these tests proves neither integrality nor existence; leaves still need exact
original norm and congruence checks.

## Completeness And Costs

`theorems/ternary_adaptive_shell.py` revalidates saved complete bases and uses
one fixed public basis, no public-center perturbation and no word training.
It charges the saved source's original two LLL preparations, GS compilation,
prefix projector compilation, coefficient nodes, triangular updates, native
checks, rational size diagnostics and all failures. It does not assume quantum
access to the unknown word, hidden phase or state inverse.

Wall times measure decoding only, not original LLL or frozen-policy validation
and compilation. Preparation CALLS and compilation sizes are charged, but no
complete physical wall-time or bit-complexity measurement is claimed. The
rational-size diagnostic measures accumulated squared energy, not every
intermediate numerator. Timing differences across shared-load runs are not
evidence of a speedup.

Stopping after two witnesses proves a pair, not the entire fiber. A node cap
returns explicitly incomplete results and can NEVER certify an empty fiber.
Only exhausted, unpruned-by-any-unsafe-rule enumeration certifies the full
fiber. There is no polynomial worst-case or source-average enumeration bound.

Tests exhaust all 81 Q9/M1 label arrays and all 729 targets, across three cut
policies, including nonunit and zero labels. Additional original M2/M3 fibers,
all true-word partial projections, negative half-cell intervals, singular
projectors, cap semantics and correlated-block energy controls are verified.

Run:

```sh
python theorems/ternary_adaptive_shell.py --write
python -m pytest -q tests/test_ternary_adaptive_shell.py
```

## Live Protocol And Falsifiers

The report reuses ALL 120 independently uniform catalog targets across 15
fixed label batches. It compares sphere-only and native-projector policies at
256 and 2048 nodes. These paired comparisons reuse labels/targets deliberately;
480 runs are not 480 independent population samples. Empty targets stay in
the denominator. Meet-in-the-middle half-assignment counts are separately
reported as exponential references, not claims of measured runtime equivalence.

The initial four-target pilot at root16 completed all four fibers with native
cuts at 2048 nodes versus no completions with sphere-only enumeration. All
were empty/singleton: this is a useful decoder control, NOT quantum signal.
Initial root24/32 searches hit their caps without witnesses.

The FINAL 120-target comparison at 2048 nodes is:

| Root digits | Projector pairs / 24 | Completed nonpair fibers | Sphere pairs / 24 |
| --- | ---: | ---: | ---: |
| 8 | 2 | 22 | 2 |
| 12 | 2 | 22 | 2 |
| 16 | 1 | 23 | 0 |
| 24 | 0 | 0 | 0 |
| 32 | 0 | 0 | 0 |

At root16, projector cuts use 15,184 nodes over all 24 targets, versus 49,152
nodes and 24 cap hits for sphere-only enumeration. Completed nonpair fibers
are genuinely empty/singleton, independently checked by bounded original-digit
meet-in-the-middle in `certificates/ternary_adaptive_shell_crosscheck.js`.
The checker also verifies accepted basis traces and strict dual certificates,
but does NOT replay the whole enumeration tree or establish population coverage.

Coupled dual certificate search is implemented separately in
`TERNARY_NATIVE_DUAL_SEPARATION.md`. It finds extra impossible branches but
does not improve large-root pair success in the recorded pilot.

Positive evidence would require inverse-polynomial verified pair coverage with
a polynomial total budget over fresh source labels, followed by a theorem.
Persistent middle-depth branching before any leaf disfavors these continuous
relaxations. Increasing caps alone is not a new direction. The next worthwhile
question is whether coupled discrete/convex prefix constraints yield sound
polynomial-cost separators that individual block tests miss; test those against
exact fibers before proposing a candidate. External review, vector-secret
reduction, source-runtime and full-depth recovery obligations remain open.
