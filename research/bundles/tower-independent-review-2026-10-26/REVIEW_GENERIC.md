# Bounded Independent Review: Generic Divisor Classes

Date: 2026-10-26. This is a sidecar review, not a repeat of the tower review.

## Verdict and Precise Findings

**ACCEPT the stated per-curve existence and uniform-class measure result.
No substantive mathematical error or false sampler inference was found.**

For each specified curve and its fixed evaluation divisor, the displayed
upper bound correctly bounds the fraction of rational degree-`10e+3` classes
whose complete AG evaluation code has a nonzero same-code cube annihilator.
The bound is strictly below one for every allowed `e`, so classes with
`V^{*3}=F_p^m` exist while retaining the same square-dimension and conditional
quantum sufficient upper bound. This proves neither a construction nor
classical hardness.

Qualifications worth retaining explicitly:

1. **The dimension identity needs a zero residue kernel.**
   [GENERIC_CLASSES.md:26](/Users/jaspersands/Developer/qsearch-research-work/generic-divisor-class-2026-10-26/GENERIC_CLASSES.md:26)
   is correct here because `3d>2g-2`. In general the differential-space
   formula has a subtraction of `ell(K-3G)`. It vanishes here, so no
   correction to the claimed result is needed.
2. **A disjoint representative is not necessarily effective.** The moving
   step at
   [GENERIC_CLASSES.md:77](/Users/jaspersands/Developer/qsearch-research-work/generic-divisor-class-2026-10-26/GENERIC_CLASSES.md:77)
   is valid with general rational divisors. It must not silently become an
   assertion that every class has an *effective*, degree-`d` representative
   avoiding all of `D`. An implementation restricted to that representation
   would need another argument. Effectiveness is not needed by the present
   evaluation-code proof.
3. **The probability is about uniform classes, not a proposal procedure.**
   The note correctly distinguishes this at lines 69-80. Approximate
   sampling in total variation `epsilon` changes the guarantee to at most
   `min(1,b_e+epsilon)`. No such sampler or error bound is supplied here.
4. **Existence is per level, not compatibility across levels.** There is no
   requirement, and no proof, that good classes at successive tower levels
   can be chosen by pullback from one fixed class. This does not weaken the
   explicitly stated per-curve result.

These are proof-explicitness and implementation-scope cautions, not failed
claims in the current note. No parent-bundle edit was made or is required
for the scoped conclusion. In particular, the decimal `5.49e-130` is a
rigorous upper bound's approximation, **not a computed actual bad-class
probability**.

## 1. The Exact Cube Identity

Fix the smooth geometric curve `X/F_p`, `p=100003`, and the reduced divisor
`D` of its `m=22e` rational evaluation places. Choose a rational divisor
representative `G` of degree `d=10e+3=2g+1`, disjoint from `D`.

At this endpoint, normal generation gives
`V^{*3}=ev_D L(3G)`. The degree criterion includes equality, not only
`d>2g+1`. [Couvreur-Marquez-Corbella-Pellikaan, Theorem 5 and Corollary 6](https://arxiv.org/html/1401.6025v3#S2.SS2).

An independent Riemann-Roch derivation makes the potentially missing kernel
term explicit:

```text
dim V^{*3} = ell(3G)-ell(3G-D),
ell(3G) = 3d+1-g,                         since 3d>2g-2,
ell(3G-D) = 3d-m+1-g+ell(K-3G+D).
```

Subtracting yields

```text
dim ((V^{*3})^perp) = m-dim V^{*3} = ell(K-3G+D).
```

Equivalently, residue duality identifies the annihilator with the image of
`Omega(3G-D)`; its kernel is `Omega(3G)`, whose dimension
`ell(K-3G)=0`. There is no assumption that evaluation on `L(3G)` is
injective. It generally is not in these parameters.

The residual degree and the exponent in the later bound are exactly

```text
a = (2g-2)-3d+m = 2e-9;
g-a-1 = (5e+1)-(2e-9)-1 = 3e+9.
```

For `e>=8`, `0<a<g-1`. At `e=8`, these are `g=41,d=83,m=176,a=7`.
Thus annihilator dimension zero is exactly full cube rank `m`, not merely
the absence of one particular explicit residue witness.

## 2. Rational Classes and Counting Fibres

There is a rational place `Q` above the base infinity. Translation by `[dQ]`
identifies `Pic^d(F_p)` with `J(F_p)`, so the domain has exactly `h` elements.
The rational point also removes the possible distinction here between a
rational Picard point and a line bundle defined over `F_p`: the rigidified
Picard functor identifies them. On a smooth curve such a line bundle has a
rational meromorphic section, hence a divisor over `F_p`.
[Stacks Project, Section 44.6](https://stacks.math.columbia.edu/tag/0B9R).

Here a rational divisor means a Frobenius-stable divisor, or a sum of closed
places with integer coefficients. Its support need not consist of rational
points. Restricting to sums of rational points would change the sample space.

The residual-class map

```text
phi: Pic^d(F_p) -> Pic^a(F_p),   [G] |-> [K+D-3G]
```

becomes an affine translate of `[-3]` on the finite group `J(F_p)` after
choosing origins. Every nonempty fibre has cardinality
`t=|J(F_p)[3]|`, and the image is one coset of `3J(F_p)`.
Surjectivity on rational points is neither assumed nor needed.

Let `B_a` be the set of rational degree-`a` classes with a nonzero global
section. Any such section, over `F_p`, gives a rational effective divisor
in its class. Hence `|B_a|<=A_a`, where `A_a` counts **all effective rational
divisors of degree a**, including closed places of higher degree. Counting
domain points gives the sharper exact expression and its bound:

```text
Pr_uniform(bad) = t * |B_a intersect im(phi)| / h
               <= t * A_a / h.
```

No assertion that a uniform input class produces a uniform element of all
`Pic^a(F_p)` is involved. The output is uniform only on the image coset.
The kernel of `[-3]` is the same as the kernel of `[3]`.
Because `p!=3`, rational 3-torsion is a subgroup of geometric 3-torsion of
order `3^(2g)`. Thus `t<=9^g` is valid, although usually quite loose.

As a concrete falsifier for dropping `t`, I enumerated the smooth elliptic
curve `y^2=x^3+2` over `F_7`. It has nine rational points, all killed by 3.
For tripling and a bad set consisting of the zero class, the actual
preimage fraction is 1, whereas the incorrect torsion-free estimate is
`1/9`. This is a genuine curve example, not only a hypothetical finite group.

## 3. Effective-Divisor Estimate and Arithmetic

The cited primary source states, for genus `g>=1` and `0<=a<=g-1`,

```text
A_a/h <= g / (p^(g-a-1) (sqrt(p)-1)^2).
```

Its RR-system criterion includes the relevant torsion factors. The hypotheses
and exponent in the sidecar agree with those statements.
[Cascudo-Cramer-Xing, Theorem 3.2 and Proposition 3.4, version 2](https://arxiv.org/html/1207.2936v2#S3).

Combining the independently counted fibres with this estimate gives

```text
Pr_uniform(bad)
 <= 9^(5e+1)(5e+1) / (100003^(3e+9)(sqrt(100003)-1)^2)
 <  9^(5e+1)(5e+1) / (100003^(3e+9)*315^2) = b_e.
```

The rounding is in the conservative direction: `316^2<100003<317^2`, so
`sqrt(100003)-1>315`. The note's non-strict upper inequality is therefore
safe. The code's `isqrt(prime)-1` makes the same conservative replacement
without floating point.

Independent rational arithmetic gives

```text
b_8 = 41*9^41 / (100003^33*315^2)
    = 5.49130657987067477016897203908428029915058012... * 10^-130.
```

For integer `e>=1`, the ratio of consecutive formula values is

```text
b_(e+1)/b_e = (9^5/100003^3) * (5e+6)/(5e+1)
           < 2*9^5/100003^3 < 1.
```

This is a proof for all allowed degrees, not an extrapolation from the
finite checks. Since `b_8<1`, every permitted level has a nonempty set of
good rational classes. No exact class number, exact torsion count, or
effective-divisor enumeration is claimed.

## 4. Moving Representatives and the Square Bound

Write the coefficient of an initial rational representative `G0` at each
evaluation point `P_i` as `n_i`. Weak approximation in the function field
supplies a rational function `f` with `v_(P_i)(f)=-n_i` simultaneously.
Then `G=G0+div(f)` has coefficient zero at every evaluation place and still
has degree `d`. Extra zeros and poles elsewhere are allowed. This is why no
effectiveness assertion should be added to this step without proof.

Changing representatives does not affect `ell(K-3G+D)`, because the residual
divisors change by `-3 div(f)`. Between two disjoint representatives,
evaluation codes differ by an invertible diagonal coordinate scaling;
their cube ranks and zero patterns are preserved. Full-support feasibility
also respects the inverse scaling of the output coordinates. This does not
change the native constraint into a different predicate.

For every class, not just an effective chosen representative,

```text
ell(G)=d+1-g=5e+3;
ell(2G)=2d+1-g=15e+6;
2d<m.
```

These give injectivity of both relevant evaluations and the same square
dimension after normal generation. For a nonzero section with zero divisor
`Z` on the evaluation set, `deg Z<=d` follows from the effective divisor
`div(f)+G` of degree `d`. Also `deg(2G-Z)>=d>2g-2`, so the shortened-square
dimension is `ell(2G)-deg Z`. Thus the same **sufficient** symbolic quantum
upper bound holds for every class. The exact failure expression can depend
on the class, and USD correctness remains outside this review.

## 5. Distribution and Scope Stress Test

The statements at lines 69-87 correctly avoid turning an abstract uniform
measure into an algorithm. Sampling points, coefficients, or representatives
in some convenient family needs a proof about its induced class law.
Randomizing representatives of one fixed class does not randomize the class.
An arbitrary proposal could be supported entirely on bad classes even when
their uniform measure is tiny.

If a sampler's induced distribution on the entire `Pic^d(F_p)` is within
total variation `epsilon` of uniform, then the bad probability is at most
`min(1,b_e+epsilon)`. The error is additive, not multiplied by the torsion
factor. A finite example in the independent checker attains the additive
TV increase exactly. Therefore a tiny `b_e` cannot compensate for a poor or
unproved sampling distribution. The primary source itself separates this
counting result from the required sampling and matrix-construction inputs.
[Cascudo-Cramer-Xing, Remark 3.5](https://arxiv.org/html/1207.2936v2#S3.R5).

One useful distinction: an oracle uniformly sampling **all effective rational
divisors of degree d** would induce the uniform class law here, since each
class contains exactly `(p^(d+1-g)-1)/(p-1)` effective representatives.
That is not the same as taking a random short sum of rational points, and
no such oracle or efficient implementation is established by the sidecar.
Likewise conditioning a representative sampler on avoiding `D` requires
rechecking its induced class distribution.

Full cube rank removes the particular method requiring a nonzero vector in
`(V^{*3})^perp`. It says nothing about hardness of full-support search or
absence of other algorithms. As requested, I did not investigate the varying
auxiliary divisor `F`, its selection, or the auxiliary product/rank attack.
I also did not undertake a novelty audit of the contextual COFI-DQI citation.

## 6. Code and Executed Checks

`class_bound.py` implements the claimed conservative bound correctly:

- Rejects nonprime fields, invalid types, nonpositive genus, and residual
  degrees outside the cited upper range.
- Returns zero for negative residual degree, where the RR space is zero.
- Caps a vacuous probability upper bound at one.
- Uses exact integers and `Fraction`; the decimal conversion is display only.
- Counts preimages with the kernel factor and an appropriate probability cap.
- Does not construct a divisor, a sampler, or a matrix; the flags say so.

The provenance flag `source_is_certified_in_preceding_tower_note` refers to
the prior written result; this helper does not itself verify or construct a
curve. Its output must continue to be read under the note's hypotheses.

Executed results:

| Check | Result |
| --- | --- |
| Current focused source tests | 14 passed |
| Independent tower arithmetic | Passed at e=8,16,32,64,128 |
| Degree and conservative square-root checks | Passed |
| Affine multiplication-by-three fibre/subset cases | 144,258 passed |
| Actual elliptic rational-torsion countercontrol | Passed |
| Biased sampling / tight TV countercontrol | Passed |
| Negative-degree and vacuous-bound endpoints | Passed |

The finite group checks enumerate all offsets and all bad subsets in the
listed small cyclic/product groups. They test the counting logic; they do
not enumerate this tower's Jacobians. No generic divisor class, RR basis,
or native matrix was generated, and no empirical bad-class frequency was
measured on a tower curve.

Review artifacts, all in the authorized review directory:

- `independent_generic_checks.py`
- `independent_generic_results.json`
- `snapshot/generic-divisor-class-2026-10-26/`

Reproduce from this directory:

```sh
/opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=pytest-generic-tmp snapshot/generic-divisor-class-2026-10-26/test_class_bound.py
/opt/anaconda3/bin/python -B independent_generic_checks.py
```

The independently computed expressions and finite group/curve checks are
compared against the snapshotted arithmetic helpers. These are bounded
checks, not formal verification of the function-field theorems.

Reviewed source SHA-256 values:

```text
GENERIC_CLASSES.md
74d98136a2084b7e90c4156325eeb2cd549bf45a351871c815617433f338584b
class_bound.py
fd244f147fe58d0d890bb4b6bbabe08adb530c6857ccb7926aa38ab0222c0303
test_class_bound.py
a158a2bb049e39f64836d2582df87581212e9dd72a0c8fd3edcd04d43307e8df
```

**Final scope:** a valid, sharply quantified uniform-class existence result
for escaping the same-code cube-annihilator obstruction. No sampler,
efficient matrix generator, compatible cross-level class sequence, hardness
theorem, uniform full-support witness sampler, or advantage follows from it.
Existing parent bundles, Git, and UI were untouched.
