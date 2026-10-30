# Power-Sum Geometry Does Not Yet Improve Rees SDE

30 October 2026. Lagrange the 2nd checked the primary paper and existing
solvers; the parent independently checked the relevant theorem contracts
and added exact countercontrols. This is a transfer audit, not a review
certifying the entire external paper, a new solver, or a lower bound.

## Decision

Do not replace the current power-SDE solver with a generic algebraic
point-finder on the strength of the new power-sum paper. Its equations,
geometric promises, nonzero-output requirement, and complexity parameter
do not automatically match the measured Rees label bank.

The source is [Gimenez et al., arXiv:2610.32056v1, Section 6](https://arxiv.org/html/2610.32056v1#S6).
It treats distinct-degree, coefficient-one power sums. Its constructive
application requires the geometric hypotheses of Theorems 3.4, 3.7 and
3.9 and a field larger than `8*M^2*e_max*Delta^4`, where
`Delta=product_j e_j`. Its success guarantee is at least 2/3. Earlier
existence bounds are not this algorithm's field or runtime guarantee.

The underlying [Cafure--Matera point-finding theorem](https://arxiv.org/abs/math/0406085)
requires a reduced regular presentation and absolute irreducibility.
Geometric degree, not its binary length, enters quadratically up to
logarithms. Evaluation cost and polynomial dimension/maximum-degree
factors are also charged. A small arithmetic circuit alone does not
make this procedure efficient.

## The Actual Rees Equation

After the existing exponent reduction, the task is

```
A * (s_1^g, ..., s_M^g)^T = 0,       s != 0,
g = gcd(original_degree, p-1),       rank(A) = r.
```

The g=1 case is already linear. For g>=2, every equation has the SAME
degree and a different row of vector weights. The external power-sum
system has distinct exponents. Invertible row operations preserve the
common degree. Nonzero variable rescalings preserve coefficient-matrix
rank; they cannot turn rank r>1 into identical coefficient-one rows.
This excludes that direct transfer, not every possible new reduction.

Rank and a large number of nonzero columns do not provide the missing
geometric promises. For r>=2 take

```
A = [e_1, e_2, ..., e_r, e_r, ..., e_r].
```

The matrix has full row rank and no zero column, for arbitrarily large M.
Its equation ideal contains `s_1^g` but not `s_1`: every generator is
homogeneous of degree g>=2, so the ideal has no nonzero linear element.
It is therefore nonradical, even when p>g and M>r*g. This is not a
failure of the SDE task: the existing arbitrary-column solver handles
the example, and the tests check a nonzero witness in the original
weighted equations. It is a failure of an unjustified geometric promise.

Nor does reduced geometry alone give polynomial rank dependence. For
each row take a Fermat sum on its own disjoint block of g+1 variables.
In characteristic greater than g, each projective hypersurface is smooth
and geometrically irreducible, and the product gives a reduced regular
system with no zero coefficient columns. Its geometric degree is `g^r`.
Thus the generic bound contains `g^(2r)` up to polynomial/logarithmic
factors even on this well-behaved family. The field guard also grows
exponentially in r. Taking log(p)=Theta(r) does not absorb this into
polynomial bit complexity. The examples themselves are classically easy;
this is a cost limitation of the proposed transfer, not SDE hardness.

## Nonzero Output And Charts

Zero always solves the homogeneous system. Existence of a nonzero point
does not show that a point-finding algorithm outputs one. A justified
projective chart or other exclusion is needed, with its geometry checked.

One cannot fix an ARBITRARY coordinate to one: in the repeated-basis
example all solutions satisfy s_1=0. At p=7,g=3,r=2,M=7 there is nevertheless
the explicit witness `(0,1,-1,0,0,0,0)`. The first-coordinate chart is
empty; the second is not. A cover by all M charts preserves nonzero
solutions but does not certify reducedness or irreducibility of each
chart. The scalar coefficient-one case allows coordinate permutation;
the arbitrary weighted case does not share that symmetry.

## Existing Comparators

The [whole-grade symmetric construction](REES_FULL_GRADE_PARAMETER_BOUND.md)
already handles arbitrary columns at sufficient arity

```
M = (r+1)*((g-1)*r+1),       p >= 16*g^(2*g+2),
work <= (1+g^g)*poly(r,g,log(p),log(1/error)).
```

For fixed g this is polynomial in growing r. Its roots and random bits
have separately capped budgets. The implementation is
`theorems/power_sde.py`; tree accounting is `symmetric_recovery_budget`
in `theorems/uniform_bch_rees.py`, not a nonexistent standalone
`rees_full_grade_budget.py` module.

The [IID-column construction](RANDOM_COLUMN_REES_PARAMETER_BOUND.md) uses
M=4u, p>=16u^2, and capped kernel rejection on one saved label bank.
Its classical `g^M` retries do not consume additional quantum copies.
An improved geometric solver for suitable random banks is not ruled out,
but it needs a new geometry/failure analysis and a paid nonzero-output
procedure. The external theorem does not supply those premises.

A constructive scalar specialization is possible. When all columns equal
one nonzero vector, impose `sum x_i=1` and `sum x_i^g=0` on g+3 variables.
For g>=2 these have distinct degrees (1,g); Theorems 3.7 and 3.9 apply
under the sufficient guard `p>8*(g+3)^2*g^5`, and the first equation
excludes zero. Applying the general point-finder then costs polynomial
in g and log(p). This is our specialization of the theorem, not a
claim that the paper analyzes Rees.

It does not improve the existing `scalar_fermat_witness`: that needs at
most g+1 slots and has a degree-bounded small-field fallback; odd g
already admits `(1,-1)`. Backend expected runtime versus fully capped
randomness must still be distinguished. No all-rank improvement follows.

## Re-Entry Conditions

Reconsider geometry only after providing one of the following, with its
actual parameter regime and comparison against the current solvers:

- A correctness-preserving reduction of vector-weighted same-degree SDE
  to the covered distinct-degree family, including witness recovery.
- A random-bank theorem giving the requisite geometry, a nonzero point,
  and better TOTAL cost than kernel rejection after bad banks and fields
  are charged.
- A structure-aware algorithm that avoids generic geometric-degree cost.

The current paper offers none of these transfers by itself. No candidate,
registry promotion, quantum speedup, or general impossibility claim is
appropriate. Exact checks are in `tests/test_power_sum_transfer_scope.py`;
they test counterexamples and the existing solver, not the external
point-finding implementation or an asymptotic theorem.
