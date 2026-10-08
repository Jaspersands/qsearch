# Coupled Native Prefix Separation

LOCAL DERIVATIONS / REVIEW PENDING. This is an exact negative-certificate
mechanism for a classical decoder, not a polynomial pair finder or a new
quantum algorithm. Read `TERNARY_ADAPTIVE_SHELL.md` first.

## Exact Integer Certificate

Fix a target T, a complete integer reduced row basis R_0,...,R_(d-1), and
assigned coefficients c_i for i>=b. The still-unassigned rows are i<b. Write

```text
H=T-sum_{i>=b} c_i*R_i.
```

Let h be ANY integer vector in the original blockwise A2 planes, orthogonal to
EVERY unassigned row. Any completion has native residual
e=H-sum_{i<b} c_i*R_i, so <e,h>=<H,h>. Every native error block chooses one
of (2,-1,-1),(-1,2,-1),(-1,-1,2). Therefore

```text
max_native_word <e,h> = 3*sum_block max_digit h[block,digit].
```

If <H,h> strictly exceeds this support, the partial branch cannot contain
any native word. This is a POINTWISE certificate, not a probabilistic fit.
Its verification uses only integer basis rows, target, coefficients and h;
neither GS arithmetic nor an approximate optimizer is trusted. Equality is
not a separator. All unassigned-row orthogonality checks are mandatory.

## Search Versus Verification

Assigned GS projections p must lie in the projection of the product of native
triangles. Any normal h in the assigned span can separate p from that convex
body. The existing radial support cut tries only h=p. The new search considers
other normals by a bounded Frank-Wolfe-style nearest-point iteration:

1. Project a maximizing known native support vertex into the assigned span.
2. Let h=p-current. Test its exact support inequality.
3. Obtain the next maximizing vertex; update the convex combination with a
   bounded dyadic, distance-guided step.
4. Clear h's denominators and verify the resulting integer branch certificate
   before pruning. Otherwise keep the branch.

Dyadic steps bound denominator growth. Four iterations and at most eight
search calls per live target are a recorded finite policy, NOT an exact LP
decision procedure. Exhausting this budget does not prove feasibility; exact
convex membership does not prove native-word membership. A test explicitly
exhibits a fractional native triangle point with no original word.

## Implementation And Evidence

`theorems/ternary_native_dual_separation.py` searches and independently verifies
the strict certificates. `ternary_adaptive_shell.adaptive_pair(...,cut="dual")`
retains all projector cuts, attempts joint separation only at recorded row
boundaries, and charges support/projector/iteration calls. The report retains
full integer directions, coefficients, support values and positive margins.

The matched 24-target pilot uses eight catalog targets on one saved label set
at roots16,24,32, each with 2048 coefficient nodes and eight dual calls:

| Root digits | Projector nodes | Dual nodes | Strict separators | Dual pairs |
| --- | ---: | ---: | ---: | ---: |
| 16 | 6045 | 6028 | 5 | 1 |
| 24 | 16384 | 16384 | 3 | 0 |
| 32 | 16384 | 16384 | 6 | 0 |

There are 192 search calls and 14 independently verified strict certificates.
The reduction in root16 nodes is only 17; the larger roots still hit all
caps. This is NOT sufficient evidence to prioritize bigger generic iteration
budgets. Wall-time variation under shared load does not establish speedup.

Tests verify support over all original small words, a separator the radial
cut misses, all true-word projections at every partial depth, exact fractional
convex membership, adversarial nonorthogonal directions, and full real fibers.
The independent JS checker validates every saved strict certificate directly.

```sh
python theorems/ternary_native_dual_separation.py --write
python -m pytest -q tests/test_ternary_native_dual_separation.py
node research/certificates/ternary_adaptive_shell_crosscheck.js
```

## Attempt To Falsify This Direction

The convex body can contain many fractional continuations with no discrete
native continuation. If p lies in that body, NO assigned-span linear support
separator can remove the branch, even with unlimited optimizer effort.
The current bounded search cannot distinguish this integrality gap from
failing to find an existing separator. That distinction is the next useful
research target in `NATIVE_TERNARY_PREFIX_INTEGRALITY_TARGET.md`.

A source-law distribution theorem is still needed to show whether these
surviving prefixes force exponential work, or whether a new discrete mechanism
can bypass them. One finite fractional witness does not prove a population,
average-case, arbitrary-decoder or quantum-circuit lower bound.
