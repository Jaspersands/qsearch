# Next Target: Source-Native Coupled Moments

IMPLEMENTED: see `TERNARY_PREFIX_MOMENTS.md`. The complete 16-prefix pilot
records 73 exact winding obstructions and eight exact pairwise continuations;
only two prefixes are eliminated at every winding, and 105 branches are unknown.
The next target is `NATIVE_TERNARY_MOMENT_PSD_TARGET.md`.

Original specification follows. Mathematical research, not an accepted candidate.
Read `TERNARY_PREFIX_INTEGRALITY.md` and `TERNARY_PREFIX_MODULAR.md` first.

## Selection Rationale

The same 16 false native prefixes admit exact fixed-winding real solutions and
concrete modulo-two native words. Independent-block convexity and modulo-two
prefix feasibility both miss their obstruction. Increasing generic iteration
budgets does not change those certificate facts.

Test the next qualitatively different POLYNOMIAL-SIZE representation: pairwise
native digit distributions coupled to all original assigned-span equations.
This is a classical falsifier of a proposed arithmetic primitive, not a new
quantum algorithm. Stop expanding this hierarchy unless evidence justifies it.

## Exact Rank-Two Model

Use digit indicators `X_(j,d)` with one-hot and retained-domain constraints.
Introduce first moments `p_(j,d)` and cross-block joint probabilities
`J_(i,d;j,e)`. Same-block products are exact: `X_(j,d)X_(j,e)=0` for d!=e
and `X_(j,d)^2=X_(j,d)`. Every J is nonnegative with consistent marginals.
Keep the assigned GS projection equations in ORIGINAL integer coordinates,
not a float surrogate. For each exact equation

```text
sum_(j,d) a_(j,d) X_(j,d) = B,
```

retain both its expectation and EACH conditioned identity

```text
a_(i,d) p_(i,d) + sum_(j!=i,e) a_(j,e) J_(i,d;j,e)
  = B*p_(i,d).
```

An actual native word ALWAYS supplies these moments. Include every original
fixed integral winding and excluded digit; do not count only a favorable lift.
Use numerical LP solely to propose primal or Farkas data. Every final proof
must reconstruct rational moments/multipliers and verify all original rows.
Pairwise consistency is not existence of a global native distribution.

## Highest-Value Experiment

1. Replay the existing 16 exact fixed-winding gaps, not newly planted successes.
2. Preflight variable/row counts and rational storage before expensive solving.
3. Determine whether EVERY allowed winding of a false prefix is eliminated,
   or give exact consistent pairwise fractional certificates for surviving ones.
4. Independently replay a useful subset in a second arithmetic implementation.
5. Check all tiny-source true words; any rejection invalidates the model.
6. Charge model building, exact reconstruction and failed proposal attempts.
   Keep LP unknown separate from both primal feasibility and dual infeasibility.
7. Only if the coupled model removes substantially more prefixes at defensible
   cost, test a matched source decoder or seek a source-law theorem. No further
   generic search inflation or automatic candidate acceptance.

## Why It Is Likely To Fail

Locally consistent pairwise moments can represent no global native word.
Dense random arithmetic may require growing hierarchy rank; fixed-degree
relaxations then fail while growing rank is exponential. The finite selected
prefixes may be especially easy for pairwise cuts yet atypical under the true
source law. Thousands of dense rows with huge integer coefficients may make
even polynomial-size optimization prohibitively expensive. Eliminating empty
prefixes need not locate TWO witnesses in nonempty fibers or improve total
Born-weighted receiver cost.

Falsification: exact coupled-moment continuations on the known false prefixes,
no larger-root recovery improvement after charging costs, or hierarchy rank
that grows without a structural theorem. If this happens, deprioritize this
lattice relaxation family and revisit collective source receivers that avoid
ordinary pair finding. Do not call failure an HSP lower bound.

Separate higher-power ternary modular decoding remains open. Modulo-two
elimination cannot be copied to F3, and digit constraints cover only three
of nine possible (u,v) points. No cheap mixed-modulus solver is assumed.

The decisive result is still a proved nonnegligible source-law pair finder
with polynomial total work, or a different efficient physical receiver.
