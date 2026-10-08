# Exact Finite CVP Certification Or Explicit Unknown

The orthogonal-dead compiler exactly eliminates some integer coefficients
but does not solve the resulting periodic objective. A finite beam can miss
the global optimum and cannot declare an approximation factor. This separate
subsystem distinguishes finite proof from capped failure through a COMPLETE
sphere search, rather than silently restricting every branch to plus/minus1.

## Exhaustive Radius Argument

Start with the best public training proposal from the previous attack,
including its inherited proposals, and its CANONICAL wrapped-residual
full-lattice point, with squared distance U. Convert that point into exact
integer reduced-basis coordinates through GS back-substitution, checking
integrality at EVERY step. Its live coefficients have exactly this point
as their conditional minimum: the code-zero dead directions preserve the
secret, and the canonical point already minimizes distance in its code class.
This avoids starting from a worse, noncanonical lift of a known proposal.
All globally better points have distance<=U.
At any descending live-coefficient prefix, the accumulated cost contains
the processed live GS terms and each dead term whose live dependencies are
ALL assigned. Every unaccounted term is nonnegative, so this is an admissible
exact lower bound. A branch with partial cost>U is impossible for an optimum
within the current radius. All comparisons use exact rationals.

For the next live coefficient i, center z and norm D_i>0, enumerate EVERY
integer from nearest(z) outward on both sides. A value with

    partial_cost + D_i*(z-a)^2 > U

is excluded by the same lower-bound argument. Once both outward fronts
exceed U, monotonic distance from z excludes ALL further integers. Costs
from newly determined dead directions may prune additional extensions.
This yields a finite complete search because every D_i is positive. An
improved full point can shrink U without excluding a global optimum: U always
comes from a verified valid lattice point.

If all branches within the shrinking valid radius are exhausted, the final
point is a GLOBAL closest vector for the represented finite input. Ties need
not be exhaustively retained: any minimum suffices. If the precommitted4096
tested-extension cap is reached while an admissible branch remains, status
is `UNKNOWN_NODE_CAP_EXHAUSTED`, never a proof of optimum, approximate factor,
classical hardness or efficient quantum recovery. The cap is checked before
processing a viable coefficient extension; pruned-by-GS integers are not
charged as visited nodes. Newly completed dead terms and all full points
are included in the exact accounting and deterministic replay.

## Scope And Self-Critique

This is standard branch-and-bound lattice enumeration applied to the
derived source-specific periodic objective, not a new enumeration paradigm
or a Shor-level mechanism. General closest-vector search still has large
worst-case cost. Projection or enumeration alone cannot be assumed efficient;
see the exponential-time general approximation construction of
[Dadush and Kun, Lattice Sparsification and the Approximate Closest Vector
Problem](https://arxiv.org/abs/1212.6781). That result does not prove hardness
of these particular source-generated inputs, and no such transfer is used.

The full cohorts and inherited beam results are pinned by hashes. No labels,
secret digits or fresh outcomes are selected for certification. No new
original qutrits or LLL reductions are generated. All eight cohorts stay in
the report, including cap failures. Posthoc planted-secret comparisons are
diagnostics only. Changed candidates are NOT assigned predecessor holdout
scores or false-acceptance bounds: this certification pass generates NO new
validation batch and makes NO empirical recovery claim for a changed point.

The independent JS checker replays BOTH parent reports, then the entire exact
enumeration for every capped or complete control: coefficient tests, valid
incumbent improvements, counters, cap status and final full points. Small
brute-force arithmetic controls check that completion really finds the
minimum and that a zero node cap remains unknown even on an easy instance.

Next useful evidence would be sharp lower bounds on the periodic objective
that accelerate complete search, a source-specific active-dimension/cost
theorem, or a genuinely collective quantum recovery mechanism. Increasing
the cap indefinitely is not itself a research strategy.
