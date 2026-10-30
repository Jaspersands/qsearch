# Small-Prime Regular Subset Completion

**Later 30 October review:** [uniform ring-to-field reduction](UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md)
gives a stronger conditional rank-only end-to-end route using the existing
field theorem. The direct construction below remains valid, but its small-
prime input regime can already be reached by exponent reduction followed
by the published small-commutator algorithm. Do not infer new HSP coverage
merely from avoiding enumeration of the ORIGINAL prime-power module.

30 October 2026. Constructive public-label arithmetic and a conditional
source-tree bound. Independent automated mathematical review completed;
implementation review found a rank-budget mismatch, corrected below. This is not
a new subset-sum or Hensel primitive, a novelty certificate, a complete ring
HSP theorem, or a quantum execution. The scientific question is whether the
large-prime restriction in UNIT_POWER_MODULE_CANCELLATION.md can be removed
without an exponential dependence on the additive exponent of the module.

## Decision And Input

The earlier spanning-block construction works with an imported arbitrary-
input SDE solver, but its sufficient source count can be enormous. For
example SPANNING_BLOCK_REGULAR_SDE.md records over 7e18 raw sources for its
general p5/d4/r2 bound, with that backend unimplemented. The unit-kernel
method instead gives a useful parameter dependence but assumes a large
prime for its source guarantee.

The new small-prime branch uses exact Boolean subset-sum dynamic programming
over the RESIDUE field. It enumerates at most p^a states, not p^(aE) module
elements. It reserves a spanning prefix so every accepted residue witness
is regular, and lifts only active variables. The construction addresses
every original degree 1<=d<p, including p5/d2 and p5/d4.

Let C be the unknown character-support subgroup of an explicitly presented
finite abelian p-group. Its cyclic rank is at most a supplied R. Work at
one Rees central grade of original exponent d<p. The required inputs are
fresh independent ideal coset sources whose measured labels are uniform
in C, conditional on all preceding required successes. This source contract
and the hidden subgroup's invariance under UNIT dilations are inherited
from PRIME_POWER_REGULAR_SDE.md, not inferred from successful arithmetic.

## 1. Separate The Prefix From The Completion

First suppose C is supplied in intrinsic coordinates
direct_sum_(j=1..a) Z/p^e_j, a>0. Acquire a prefix of P0 labels whose
residues span F_p^a. Select a basis of a columns using only this prefix.
Assign initial coefficient one to each basis column, zero to every other
prefix column. Put t equal to minus the sum of the chosen basis residues.

Acquire an INDEPENDENT suffix v_1,...,v_L. Find z in {0,1}^L with

    sum_i z_i*v_i = t in F_p^a.

Exact dynamic programming starts with the zero residue and, once per
suffix column, appends the old reachable residues plus that column. Store
one predecessor mask per residue. Each update reads a snapshot of the
previous states, so no column is used twice. Stop on finding t; otherwise
report a scoped failure. There are at most p^a states, O(L*p^a) transitions,
and polynomial work per transition in a,log p,L. No field-size iteration
is hidden inside a large-prime polynomial-in-log-p claim.

The resulting full coefficient vector u is Boolean and nonzero, and

    sum_i lambda_i*u_i^d = sum_i lambda_i*u_i = 0 mod p.

Thus it already solves the ORIGINAL degree; no reduced-degree root or
Bezout conversion is required. The a reserved basis columns have
Jacobian columns d*lambda_i, so the active Jacobian has rank a. Its
regularity does not depend on the support found in the suffix.

Use the existing regular mixed-order Hensel lift. Fix all zero variables
to EXACT zero, choose active Jacobian pivots, and lift through max(e_j).
Active coefficients remain units, and inactive coefficients remain zero.
Consequently every final scale is a legal unit dilation or the exact-zero
identity branch. Updating a zero to a nonzero multiple of p would be
invalid and is expressly forbidden. Verify the original mixed-modulus
equations after lifting.

The algorithm is not guaranteed to succeed on every bank. For example
over F7 the columns 1,5 admit the regular square witness (1,2), but with
the first column reserved there is no Boolean suffix completion. Failure
does not establish SDE unsatisfiability. An observed spanning prefix is
also not an IID certificate.

## 2. Suffix Success For Every Fixed Target

Fix t before seeing the suffix. Distinct nonzero Boolean vectors z,w are
linearly independent over F_p: proportional nonzero Boolean vectors must
have the same support and scalar one, hence be equal. For an IID uniform
a-by-L matrix A, their images Az,Aw are therefore independent uniform
vectors. If X counts nonzero Boolean z with Az=t, exactly

    mu = E X = (2^L-1)/p^a,
    Var X = mu*(1-p^(-a)).

Chebyshev gives Pr[X=0] <= min(1,1/mu). This is uniform in t, not a
uniform-target premise. It remains valid conditional on the entire
successful prefix and its selected basis. Selecting the basis using
suffix labels instead would invalidate this argument.

If t=0, the empty subset is also available; omitting it in this counting
argument only weakens the success bound. For a genuine positive-rank basis
the sum of its columns is nonzero, so the reserved target is nonzero.

The DP has no internal randomized search or root-extraction failure.
A caller-supplied state cap below p^R can interrupt it. Such an execution
may still return a verified witness, but its reported episode failure
bound is set to one rather than silently inheriting the complete-DP bound.

## 3. Paid Pilots And An Episode Bound

For integer b>=1 set

    P = P0 = R+b+2,
    L = R*ceil(log2 p)+b+2,
    W = P+P0+L.

Acquire P fresh pilot labels and compile their EXACT generated subgroup
C' with the existing certified Smith/Hermite coordinate maps. Then acquire
a fresh bank of P0+L labels, preserving its prefix/suffix split. Membership
is tested in C' BEFORE intrinsic reduction modulo p. In particular,
p Z/p^E is not mistaken for the zero module.

Incomplete pilots have probability at most
p^(R-P)/(p-1) <= 2^(-b-2). Conditional on complete pilots, the prefix rank
failure has the same bound. The suffix moment formula with a<=R gives
Pr[X=0] <= p^R/(2^L-1) <= 2^(-b-1). Hence a complete-state-cap episode
aborts with probability at most 2^-b. These are conditional ideal-source
bounds; no independence between all failure events is asserted.

On incomplete pilots, a nonmember bank aborts. A member bank may safely
succeed: decode the proposed cancellation into the ORIGINAL ambient module
and verify it there before operating on sources. Correctness never depends
on a claim that the pilot subgroup equals C. For C'=0, accept only a fresh
zero bank and use one nonzero scale. Charge every acquired slot, including
all discarded pilots and every unused coefficient-zero source.

The implementation fixes acquisition at W slots even if the prefix will
fail. Malformed data/backend failures remain errors, not statistical aborts.
The episode accepts the SAME supplied support-rank bound R as the planner;
omitting it conservatively uses the ambient factor count. A pilot frame
of rank greater than R aborts with both banks charged. Passing this check
does not certify the rank of unseen support. In particular a rank-one
support in a two-factor ambient module may use the rank-one budget without
silently acquiring the rank-two number of sources.
Source callbacks and the normal-form backend are not locally wall-clocked.
The mathematical bit complexity pays their standard polynomial costs and
the FULL max(e_j)*log p precision, not log(max(e_j)).

## 4. All-Prime Conditional Source Trees

Keep u>=max(c,R+1,2) as an EXPLICIT parameter, with c<p. Do not replace
c by R: the existing ring counterexample has derived cyclic rank one and
class equal to its additive exponent.

For p>=16u^2 use the existing large-prime unit-kernel source tree. For
3<=p<16u^2 set

    ell = ceil(log2(16u)), b=4u*ell,
    W = 2(R+b+2) + R*ceil(log2 p)+b+2.

Then ceil(log2 p)<=2ell, so

    W <= 16u*ell <= 2^(2ell).

Use this SAME arity W at each grade, including smaller actual ranks. A
one-output depth-(c-1) tree has W^(c-1) leaves and at most that many
internal nodes. Union-bound the episode failures conditional on the
preceding successful children. Pointwise source decoupling is essential:
accepted child states must be the same target coset state independently
of their complete records. Under that inherited Rees premise,

    Pr[tree abort] <= W^(c-1)*2^(-b)
                   <= 2^(-2u*ell-2ell) < 1/64.

The DP costs at most p^R <= (16u^2)^R states per node. Therefore its total
arithmetic and source-tree size are 2^O(u log(u+2)), times polynomial
explicit-module/exponent costs. DP work is summed over nodes; it is not
multiplied recursively into the quantum source branching factor.

This supplies BOTH prime regimes for a conditional mixed-order SOURCE
tree with c<p. The small-prime branch has abort bound 1/64, the large-prime
branch 1/16, so the UNIFORM two-branch bound is 1/16, not 1/64.
It does not import the field small-commutator fallback, whose cost
p^(sum e_j) would defeat the claimed exponent dependence. It also does not
by itself account for all original-oracle evaluations, the complete ring
receiver/readout, or accumulated quantum approximation error. Report fields
therefore keep all_prime_ring_hsp_bound=false. No full HSP complexity claim
is promoted by this pass.

## 5. Implementation And Falsifiers

Field primitive: theorems/regular_subset_sum.py. Mixed-order/pilot wrapper
and branch planner: theorems/small_prime_module.py. Run

    python qsearch.py prime-power-sde --subset-kernel --write

The producer writes research/reductions/small_prime_module.json. Its three
predeclared seeded CLASSICAL controls are p3/d2 on a subgroup invisible
modulo ambient p, and p5/d2 plus p5/d4 on oblique mixed-order subgroups.
These are arithmetic controls, not physical measurements or evidence for
an IID source law. A separate resource calculation covers p5/class4/rank2
and p1009/class3/rank2; neither is an executed source tree.

Tests cover exact DP versus subset enumeration, the projective Boolean
moment count, original degrees, active regularity, frozen zeros, incomplete
pilots, fresh zero-bank handling, deficient prefixes, state caps, strict
encodings, corrupt backends, ambient verification, and the tree ledger.
The complete-state cap is an explicit exponential parameter cost, not an
unrestricted polynomial solver. No new input family, candidate, quantum
speedup, classical-hardness assertion, or practical cryptanalytic claim is
created by these controls.

## 6. Review And Executed Controls

Laplace implemented the field primitive and exhaustive controls. Goodall
independently reviewed the argument and then the integration. The reviewer
accepted the conditional construction, requiring the explicit zero-rank
branch, INTERNAL node count, c<p promise, and uniform two-branch 1/16
bound. Its implementation review found that the episode originally used
ambient rank even when the planner used a smaller support bound. This was
fixed, regression-tested, and independently re-reviewed with no remaining
finding in that fix-only review. These are automated reviews, not external
human review or a proof-assistant certificate.

Parent inspection of the initial live artifact found the proposed p5
control generators were dependent. The final controls use (1,5),(0,25)
in Z/25 x Z/125, with respective orders25,5 and exactly125 distinct sums.
Their intrinsic exponents are (1,2), not a single cyclic factor. A
regression checks this cardinality and rank instead of merely checking
that the report returns success.

Final live command: python qsearch.py prime-power-sde --subset-kernel --write.

| Public-label control | Paid labels | Intrinsic exponents | DP states | DP transitions | Lift steps |
| --- | ---: | --- | ---: | ---: | ---: |
| p3, d2, ambient-mod-p-zero | 34 | (3) | 2 | 2 | 2 |
| p5, d2, rank-two oblique | 40 | (1,2) | 11 | 13 | 1 |
| p5, d4, rank-two oblique | 40 | (1,2) | 15 | 25 | 1 |

All three verify cancellation in the ORIGINAL ambient module. Separately,
the p5/c4/R2/u4 tree budget has arity304 and28,094,464 leaves; the
p1009/c3/R2/u3 budget has arity24 and576 leaves. Neither tree was executed.
The exponent128 regression performs127 lifting steps with a five-state
residue cap; it does not enumerate the group of order5^128.

Final connected validation: 528 tests across the following13 files, all
passing in8.65s under /opt/anaconda3/bin/python -B -m pytest -q
-p no:cacheprovider -W error:

- tests/test_regular_subset_sum.py
- tests/test_small_prime_module.py
- tests/test_cli_parser_integrity.py
- tests/test_prime_power_rees_descent.py
- tests/test_pilot_submodule.py
- tests/test_pilot_module_descent.py
- tests/test_pilot_receiver_policy.py
- tests/test_unit_power_kernel.py
- tests/test_unit_power_module.py
- tests/test_span_regular_sde.py
- tests/test_random_regular_sde.py
- tests/test_random_column_power_sde.py
- tests/test_random_column_rees_budget.py

The six changed Python files pass py_compile; all12 site JavaScript files
pass node --check; qsearch.py validate returns valid=true, issues=[].
This is NOT the full repository suite, Lean checking, quantum execution,
or independent novelty verification. The generated JSON binds eight
implementation/proof/test sources by SHA-256. No central candidate or
proof status was promoted.

The original next task was complete direct receiver/readout accounting.
The subsequent ring-to-field review supersedes that priority: its stronger
conditional rank-only bound uses the existing field receiver instead.
Direct mixed-order receiver costs remain debts for anyone pursuing that
alternative, not prerequisites for the preferred reduction. Do not infer
that this arithmetic result alone removes those debts.
