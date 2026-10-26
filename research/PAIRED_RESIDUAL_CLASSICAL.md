# Classical Search Inside The Paired Information Manifold

2026-10-20. Local derivations REVIEW PENDING. Known interpolation, quadratic
Gauss sums and greedy coordinate search. No novelty, classical lower bound
or quantum speedup is claimed.

Producer: `theorems/paired_residual_classical.py`.
Artifact: `research/classical_baselines/paired_residual_classical.json` (schema v2).
This tests the SAME changed paired instance as `PAIRED_RESIDUAL_DECODER.md`.
It does not reuse scores from the original overlapping chain.

## Question And Prior Art

Does the decomposition P(X)=E(X^2)+X O(X^2) expose a cheap classical attack
that defeats the proposed paired quantum score? The previous single
information-set witness was too weak to say anything.

The [authors' nonlinear-chain portfolio](https://github.com/dsfranca/RDQINumerics/tree/v1.0.0)
already includes residual-preserving intrinsic coordinates. We inspected
`residual_manifold_interval_values` and `residual_manifold_coordinate_scan`
before deriving the disjoint-pair version. This is an adaptation to a different
explicit problem, not invention of residual-preserving search. No external
author code was imported or copied into the repository.

The existing `EXPLICIT_QUADRATIC_OPI.md` affine-flat attack and
`MOMENT_TARGET_MASKING.md` norm/masking attack were also checked. Their field,
target-set and linear-moment assumptions do not simply hold here. They remain
competitors to generalizations, not automatic algorithms for random halfsets
on the paired polynomial code.

## Feasible Intrinsic Coordinates

There are M pairs a_i,-a_i, n=2K coefficients, nonzero b_i, and explicit
halfsets F_i. Choose K distinct information pairs I. Let z_i=a_i^2 and let
l_j(z) be the ordinary degree<K Lagrange basis on z_j,j in I.

At each information pair choose

    x_j=P(a_j) in F_p,
    r_j=P(-a_j)+b_j x_j^2 in F_j,
    y_j=P(-a_j)=r_j-b_j x_j^2.

These values determine exactly one degree<n original polynomial. Conversely,
EVERY original polynomial passing all predicates in I has exactly one such
coordinate tuple. The space has (p*(p-1)/2)^K elements. Uniform independent
x_j and uniform r_j in F_j sample the uniform ORIGINAL-code law conditioned
on those K passes, not a relaxed source distribution.

Write

    A_ij = l_j(z_i)/2 * (1+a_i/a_j),
    B_ij = l_j(z_i)/2 * (1-a_i/a_j).

Then x_i=sum_j(A_ij x_j+B_ij y_j) and
y_i=sum_j(B_ij x_j+A_ij y_j). At an information position the expected identity
block appears. At any outside pair, every individual two-by-two block is
invertible:

    A_ij^2-B_ij^2 = l_j(z_i)^2 a_i/a_j != 0.

The producer builds these field maps without a lifted Q=P^2 variable.
Final witnesses are reconstructed by interpolating E and O and interleaving
their coefficients. Independent Horner evaluation rechecks every original
pair and the full score.

## Exact Root And Residual Moves

A root move x_j -> x_j+d preserves r_j by setting

    delta x_j=d,
    delta y_j=-b_j(2 x_j d+d^2).

Through A/B, every outside x_i and y_i is quadratic in d, and its residual
y_i+b_i x_i^2 is a QUARTIC in d. All forced information residuals remain
exactly unchanged. Dropping the d^2 term is not a valid tangent approximation:
it changes the supposedly preserved constraint. A countercheck rejects that
mistake.

A residual move r_j -> r_j+d with the new r_j still in F_j leaves x_j fixed
and changes y_j by d. Every outside residual is quadratic in d. Other
information predicates are unchanged; the updated one still passes.

The implemented algorithm scans every field value for each root coordinate
and every actually allowed value for each residual coordinate. It uses exact
modular Horner evaluation of these quartic/quadratic curves. A state update
requires a strict full-score improvement; ties keep the current state.
All candidates, including unchanged/repeated ones, and all M predicate
lookups per candidate are charged. No incomplete scan is used to update.

An uncapped sequence of complete passes terminates at an intrinsic-coordinate
fixed point in at most M-initial_score+1 passes, because every nonterminal
pass makes a strict integer improvement. Each pass is polynomial work,
O(K M p) field operations in this reference model. This proves only
termination at this LOCAL fixed point, not useful approximation quality or
a global optimizer. The live experiment has a predeclared two-pass cap.

## Why Uniform Conditioning Alone Is Weak, For Fixed Inputs

This is a statement about the uniform component above, NOT the adaptive
greedy algorithm.

Condition on any particular allowed information residual vector r_I.
The roots x_j remain independent uniform. For an outside pair i and a
nonzero dual vector (u,v), its characteristic function factors into sums of
the form

    E_(x_j) exp(2 pi i [c_j x_j+d_j(r_j-b_j x_j^2)]/p),
    c_j=u A_ij+v B_ij, d_j=u B_ij+v A_ij.

Invertibility of each A/B block implies (c_j,d_j)!=(0,0). If d_j=0 the
factor is zero. Otherwise b_j d_j!=0 and the quadratic Gauss sum has
magnitude p^(-1/2). Thus every nontrivial characteristic function of the
outside PAIR has magnitude at most p^(-K/2). Averaging any residual-vector
law independent of the free roots preserves the bound; in particular it
holds for the actual fixed halfsets.

Parseval and Cauchy-Schwarz give

    chi_square(law(x_i,y_i), uniform F_p^2) <= (p^2-1) p^(-K),
    TV <= epsilon = min(1, sqrt((p^2-1) p^(-K))/2).

The outside predicate passes with probability at most rho+epsilon. Hence
the uniform component's normalized score mean is at most

    K/M + (1-K/M) * min(1, rho+epsilon).

This holds for EVERY fixed collection of public nonzero multipliers and
halfsets and EVERY information-pair set I. No random-instance assumption is
needed. If only k<K predicates are conditioned, each outside pair is exactly
uniform by n-coordinate RS independence, so its mean is exactly
k/M+(1-k/M)rho.

Arbitrary input-dependent POSITIVE mixtures of these uniform components
inherit the maximal mean bound. A target algorithm that adaptively changes
the roots, selects high-score samples, retries on a score event, or conditions
on more predicates is NOT such a mixture. Our greedy search is explicitly
outside the comparison class.

At the native parameters, the upper mean is below0.55. Exact rational
arithmetic and an outward square-root enclosure are saved; a tiny bound is
never rounded to zero. Conditional on the paired quantum derivation, its
larger mean forces a positive TV gap from this particular mixture class.
This is not a bound on arbitrary classical optimization.

The p7,n4 control enumerates all2401 original polynomials. Conditioning on
one selected pass retains1029 words and makes the outside pair exactly
uniform. Conditioning on two passes retains441 words and has a nonuniform
outside pair, with its actual distribution, exact TV and chi-square energy
recorded. This checks the boundary case instead of extrapolating exact
independence past the RS dimension.

## Why The Earlier Affine-Flat Attack Does Not Directly Apply

For a local accepted set y+b x^2 in F with |F|=(p-1)/2, restrict to any
nonconstant F_p-affine line. If its x-direction vanishes, the residual is
a nonconstant linear polynomial and visits all p values. Otherwise it is
quadratic and has exactly(p+1)/2 distinct values. Neither image fits inside F.
Therefore no complete nonconstant F_p-affine line is accepted.

This rules out reusing a larger local accepted F_p-flat of the kind exploited
in the earlier binary quadratic target. Fixing both local values remains
possible. It is not a lower bound against nonlinear paths, integer/bit
methods, dependent global constraints or any other classical algorithm.
The parabolic intrinsic moves above deliberately exploit a NONLINEAR
accepted path, so this observation does not forbid our own search.

## Evidence, Portfolio Extensions, And Remaining Threats

The live run starts from the exact saved536/1026 information-set polynomial,
uses the same author-derived fixed tables, the same n204 problem and the
first102 information pairs. It performs at most two complete greedy passes,
with no random restart or post-hoc choice of input. The artifact stores
every coordinate scan, the final original coefficients and full work counts.
No quantum circuit is run and no matched quantum wall-time comparison is
supplied.

Completed native run (`native_search`):536 ->632 passing predicates out of1026,
with three strict improvements. The second complete pass makes no improvement,
so this is a fixed point for the implemented single-root/single-residual moves
on $I_0 = (0, \dots, 101)$, not just exhaustion of the two-pass budget. Charged
work:628,116 proposals,644,447,016 predicate lookups,408 complete coordinate
scans, zero restarts.

In `schema: paired-residual-classical-v2`, `portfolio_campaign` adds four
predeclared portfolio stages with full work accounting and retention of all
trajectories (including non-improving and lower-scoring runs):

| Portfolio Stage (`run_label`) | Initial $\to$ Final Score | Candidate Evaluations | Predicate Lookups | Wall Seconds | Outcome Summary |
|---|---|---|
| `reanchored_information_set_escape` | $632 \to 633 / 1026$ | $314{,}058$ | $322{,}223{,}508$ | $7.49\text{ s}$ | Pivots to $K=102$ passing pairs of $c_{632}$; escapes $I_0$ fixed point |
| `independent_information_set_restart` | $564 \to 629 / 1026$ | $314{,}058$ | $322{,}223{,}508$ | $7.85\text{ s}$ | Fresh feasible witness on distinct $I_{\text{fresh}}$; retained below $633$ |
| `two_coordinate_block_move_search` | $633 \to 633 / 1026$ | $2{,}048$ | $2{,}101{,}248$ | $0.33\text{ s}$ | Simultaneous 2-anchor root/residual displacements (`block_move`) |
| `intrinsic_simulated_annealing` | $633 \to 633 / 1026$ | $1{,}024$ | $1{,}050{,}624$ | $0.21\text{ s}$ | Metropolis cooling ($T: 1.2 \to 0.15$) with single & 2-anchor moves |

Pivoting to a new information set $I_{\text{reanchored}} \subseteq \{i : r_i(c_{632}) \in F_i\}$
preserves the polynomial $c_{632}$ while changing the pinned anchor set, allowing
single-coordinate intrinsic moves in the new chart to escape the $I_0$ fixed
point and reach $633/1026$ (verified by independent Horner replay). `full_classical_portfolio_complete`
remains `False`.

## Reproduction

```sh
python theorems/paired_residual_classical.py --reference /path/to/RDQINumerics/data/reference --max-sweeps 2 --write
python -m pytest -q tests/test_paired_residual_classical.py -W error::RuntimeWarning
```
