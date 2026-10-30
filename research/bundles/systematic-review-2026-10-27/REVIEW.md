# Independent Adversarial Review: Systematic Full-Support Sampling

Date: 2026-10-27. All reviewer-created files are confined to
`/Users/jaspersands/Developer/qsearch-research-work/systematic-review-2026-10-27`.
No parent files, Desktop source, Git state, or UI were changed.

## Verdict

**ACCEPT the exact all-syndrome counting identity, the systematic/affine
success probabilities, the ideal conditional-uniform output law, and the
q=100003 tower tail bound.** No sign, normalization, or pivot-choice error
was found under the stated full-row-rank and distance premises.

**QUALIFY the comparative conclusion.** The systematic method has a much
smaller proved exponential trial rate than the four-list bound evaluated
at its worst permitted rank. This is not dominance over the actual
four-list runtime, not a rank lower bound, and not an optimal classical
search theorem. The four-list theorem has additional access costs and its
certified tower range starts at dyadic e>=64, not e>=8.

There is an already-known polynomial cubic/norm solver for a special
near-canonical tower subclass. It must remain in the comparison. It does
not cover all degree-(2g+1) divisor classes. A bounded primary-source check
also identifies a general existence theorem applicable here, but not a
verified polynomial construction for all the promised inputs.

## Findings And Corrections

1. **Comparison scope, not a false counting theorem:**
   [BASELINE.md:83](/Users/jaspersands/Developer/qsearch-research-work/systematic-full-support-2026-10-27/BASELINE.md:83)
   should say explicitly "smaller than the worst-rank specialization of
   the demonstrated four-list upper bound, on the common certified range
   and with all access costs charged." The existing lower-bound warning is
   correct. An upper bound r_2<=10e+2 does not show actual r_2 is linear or
   large. The threshold in lines 90-94 is a comparison of displayed
   exponential terms, not a necessary condition for every improved
   four-list implementation to outperform this sampler.
2. **Preserve the stronger special-case baseline:**
   [BASELINE.md:105](/Users/jaspersands/Developer/qsearch-research-work/systematic-full-support-2026-10-27/BASELINE.md:105)
   should identify the open scope as the arbitrary-admissible-divisor-class
   family, not the already-solved special cofinal tower subclass. See
   Section 6 below. This is a scope clarification, not a generic polynomial
   solver supplied by this review.
3. **Initial cost mismatch, resolved during the review:** the first
   `systematic.py` read recomputed `B_I^{-1}s` inside every proposal, adding
   O(k^2) before verification. The parent independently revised it during
   this review. In the final reviewed version,
   [systematic.py:71](/Users/jaspersands/Developer/qsearch-research-work/systematic-full-support-2026-10-27/systematic.py:71)
   computes this once and `_complete` performs the per-trial completion.
   The stated O(k(m-k)+m) per trial is now consistent, with one O(k^2)
   per-syndrome setup and O(km) final native verification. The public
   `from_free` method still has its own O(k^2) solve, as expected.

No remaining mathematical correction to the sampler or `distance_bound`
is required by this audit. I did not execute the parent implementation:
the parent owns direct implementation tests and the degree-eight replay.

## 1. Independent Counting Derivation

Let B have k independent rows over F_q, k<=m, and let
`F_s={z in (F_q^*)^m : Bz=s}`, with size N_s. For any nontrivial additive
character psi, orthogonality gives

```text
N_s = q^(-k) sum_u psi(-u.s) product_j sum_(a != 0) psi((uB)_j a).
```

The inner sum is q-1 when `(uB)_j=0` and -1 otherwise. Multiplication by
a nonzero field element permutes F_q, including for extension fields;
no prime-field-only trace assumption is hidden here. Isolating u=0 gives

```text
N_s = (q-1)^m / q^k * (1+R_s),
R_s = sum_(u != 0) psi(-u.s) (-1/(q-1))^wt(uB).
```

This proves the proposed sign and normalization for every fixed s. The
row-rank premise makes u->uB injective, so a minimum nonzero rowspace
weight delta gives

```text
|R_s| <= (q^k-1)/(q-1)^delta = alpha.
```

The exact character formula itself still holds for dependent rows, but
the displayed distance bound does not: nonzero u in the left kernel have
weight zero. One must first reduce to independent equations and check
syndrome consistency, or reject such input as the implementation does.

There is an exact rational form useful for an independent audit. Choose
one u per nonzero scalar orbit in F_q^k. Summing over its q-1 multiples,

```text
R_s = sum_[u] (-1/(q-1))^wt(uB) *
                   { q-1, if u.s=0;
                     -1,  otherwise. }
```

Thus R_s is actually rational, not merely real. This formula avoids
floating-point roots of unity. It also exposes a testing trap: reversing
only the phase sign does not change R_s, since u->-u is a bijection with
the same weight. Indeed N_s=N_(-s), and more generally N_s=N_(a s) for
a!=0. A plus-phase version is an equivalent convention here, not a
counterexample. Dropping the phase or the odd-weight minus sign is wrong.

## 2. Proposal And Output Law

For any invertible k-column submatrix B_I, write J=I-complement and n=m-k.
The map

```text
a in (F_q^*)^n  ->  z_J=a, z_I=B_I^(-1)(s-B_J a)
```

is injective. Its accepted image is exactly F_s: every full-support
solution has a unique such restriction to J. Consequently

```text
p_sys = N_s/(q-1)^n = ((q-1)/q)^k (1+R_s),
p_aff = N_s/q^n     = ((q-1)/q)^m (1+R_s).
```

These statements do not assume independent pivot coordinates. They do
not depend on the pivot set, including when pivots are not the leading
columns. The ratio is `(q/(q-1))^n` only when N_s>0; if N_s=0 both
probabilities are zero and their ratio is undefined.

For independent uniform proposals and a fixed cap T>=1, let Q be the
proposal-space size and p=N_s/Q. Every fixed x in F_s has

```text
Pr(first accepted output is x by T)
  = (1/Q) sum_(t=0)^(T-1) (1-p)^t
  = [1-(1-p)^T]/N_s.
```

Dividing by total success probability proves exact uniformity conditional
on success by T. It also proves the unlimited-retry output law when p>0.
For an empty fiber the conditional law is undefined. This is a fixed-s
law, not a claim about an arbitrarily randomized syndrome distribution.

The source correctly distinguishes this ideal law from deterministic
`random.Random(seed)` replay. Neither a seed nor a finite histogram proves
uniformity. The finite seeded implementation has no literal ideal-coins
distribution theorem beyond the stated mathematical model.

For p>=p0>0, the failure bound `(1-p)^T <= exp(-p0*T)` justifies
`T=ceil(bits/p0)` for positive bits: it is conservative because
`exp(-bits)<=2^(-bits)`. The sharper sufficient cap is
`ceil(bits*ln(2)/p0)`. The supplied code implements neither cap helper;
128 is simply its default replay cap, not an all-size tail guarantee.

## 3. Edge Cases And Concrete Falsifiers

- **Odd-weight sign:** over F_3, B=[1,1,1] has counts
  `(N_0,N_1,N_2)=(2,3,3)` and tails `(-1/4,1/8,1/8)`.
  Replacing the weight sign by positive terms fails.
- **Syndrome dependence:** over F_3, B=[1,1] has counts `(2,1,1)`;
  p_sys is `(1,1/2,1/2)`, not a syndrome-independent number.
- **Forced zero:** over F_5, B=[1,0], s=0 forces z_1=0, so N_s=0.
  The true delta is 1 and alpha=1. Supplying the false promise delta=2
  would give the positive formal success bound 3/5 on this empty fiber.
  The helper's unverified-promise warning is necessary, not cosmetic.
- **No forced coordinate need not imply a witness:** over F_3,
  B=[[1,0,1],[0,1,1]], s=(1,2), all coordinates vary over the unrestricted
  affine fiber, yet the two nonzero free assignments yield `(0,1,1)` and
  `(2,0,2)`. Neither is full support. Here delta=2 and alpha=2, so no
  claimed positive guarantee is contradicted. For s=(0,0), both nonzero
  assignments succeed, also refuting independent-pivot reasoning.
- **Rank is essential:** over F_5, let B have two identical rows
  `[1,1,1,1]`. Its nonzero rowspace words have weight 4, but s=(0,1) is
  inconsistent. Incorrectly using k=2 in the distance bound gives
  alpha=3/32<1. The exact character sum includes the left-kernel terms
  and gives N_s=0. `AffineFiber` rejects the dependent rows.
- **Square case:** B=I_2 over F_3 has one deterministic proposal. For
  s=(1,2) acceptance is 1; for s=(1,0) it is 0. Empty J is valid and
  `all(())` must be true. Repeating the same failed proposal is inefficient
  but the returned UNKNOWN is not an incorrect impossibility claim.
- **Zero columns, permutations, scalings:** a zero column is a genuinely
  free nonzero coordinate, not a forced zero. Permuting or multiplying
  columns by nonzero scalars bijects the original full-support fibers and
  preserves the rowspace weight distribution. Invertible row operations
  must also transform s. The implementation's solve uses the original B
  and correctly keeps that distinction.
- **Rank zero / other fields:** the mathematical identity has a trivial
  k=0 extension with R_s=0 and success 1. The API intentionally requires
  nonempty independent rows and odd prime q<2^63; it does not implement
  extension-field arithmetic or q=2. No code coverage for those cases is
  implied by the more general theorem.

## 4. Tower Bound And Genuine Asymptotics

Conditional on the stated complete AG source, disjoint distinct evaluation
points, and its distance bound, substitute

```text
q=100003, m=22e, k=5e+3, delta_0=12e-3.
```

For a nonzero f in L(G), the effective divisor div(f)+G has degree d,
so at most d evaluation coordinates vanish. This argument also works
when the disjoint representative G is not effective. It gives
delta>=m-d and survives monomial equivalence. It does not need a cubic
annihilator. Existence or efficient generation of the tower is not proved
by this substitution and is not re-audited here.

The integer-exponent proof of the claimed loose tail is

```text
(q-1)^(12e-3) = (q-1) * ((q-1)^2)^(6e-2)
              > q^(6e-2),
alpha <= (q^(5e+3)-1)/(q-1)^(12e-3) < q^(5-e).
```

For e>=8 this is <=q^(-3)<1/2. All inequalities have the correct direction;
there is no fractional-exponent rounding issue. The number called alpha
here is a distance-based envelope, not the measured |R_s|.

The stated expected-trial upper bound follows. In fact the identity gives
the two-sided, uniform-in-s conclusion

```text
(q/(q-1))^k/(1+alpha) <= E[ideal trials]
                      <= (q/(q-1))^k/(1-alpha).
```

Since alpha tends to zero, this sampler really does have an exponential
expected trial count at fixed q and unbounded e, not just an exponential
upper bound. Its binary rate is

```text
c_sys = 5*log2(100003/100002)
      = 0.000072132948721331229965940218985... .
```

That statement is about this sampler, not every classical algorithm.
Dense explicit input length is Theta(e^2) at fixed q, so the same trial
growth is exp(Theta(sqrt(input bits))), not exp(Theta(input bits)). It is
still not polynomial in the input length. A growing-q regime with
k/q=O(log m) and a controlled 1/(1-alpha) is different and can be polynomial.

The exact arithmetic controls give, at e=8,

```text
alpha_8=(100003^43-1)/100002^93
       approximately 9.99430161669705192107e-251;
(100003/100002)^43 approximately 1.00043008170890159858.
```

The much looser q^(-3) is approximately 9.9991000539973e-16. These are
analytic trial-factor/envelope calculations, not measured native runtimes.

## 5. Sound Four-List Comparison

The comparison source is
[FOUR_LIST.md](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-2026-10-26/FOUR_LIST.md:5),
with its expected-cost clarification in
[REVIEW_RESOLUTION.md](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-2026-10-26/REVIEW_RESOLUTION.md:24).
Its native guarantee is conditional on geometric, prime-sampling,
class-label, pairing, and rational-halving access. A suitable ledger is

```text
T_pre + (L*sum_i T_prime_class_label(n_i) + O(L*poly(r_2)))/p_* + T_finish,
L=2^ceil(r_2/3), p_*=1/8000.
```

`T_finish` includes moving, Riemann-Roch spaces, residues, common-basis
solving, and original-relation verification. These are not eliminated
by exhibiting a matching class label. The systematic sampler instead
needs just the supplied explicit matrix, polynomial preprocessing,
field draws, completion, and native verification.

The certified worst-rank four-list degree budget holds at the existing
dyadic levels e>=64. It is not certified at e=8,16,32 by that sufficient
bound. The separate small-rank r_2<=2 abstract branch is constant-size;
it is not implemented by the r_2>=3 join helper. This review does not
re-prove or replay the four-list theorem or its backend access contract.

If r_2/e tends to rho and all other charged factors are polynomial, the
displayed four-list term has binary rate rho/3. It beats c_sys precisely
when its rate is smaller, namely

```text
rho < 15*log2(100003/100002)
    = 0.000216398846163993689897820656955... .
```

At equality the leading rate alone is inconclusive. For nonconvergent
rank sequences compare limsup/liminf or the finite log bounds; polynomial
factors contribute O(log e), and ceiling contributes at most one bit.
Nonpolynomial preprocessing can invalidate this rate-only comparison.

At the worst permitted rank r_2=10e+2, the rate is 10/3. At e=64 its list
length is 2^214, while the systematic base trial factor is about
1.00323514106172731. Neither number is a wall-clock benchmark. Only the
first uses worst-rank substitution; actual rank has not been established.

A sound guaranteed search portfolio takes the smaller applicable bound,
including preprocessing and known polynomial special cases. The
four-list construction is a witness algorithm, not a demonstrated uniform
sampler over F_s; the systematic method has the stronger output-law
guarantee under ideal coins. Keep search and uniform-sampling comparisons
separate. A smaller upper bound is neither a runtime lower bound nor a
proof that the other algorithm cannot be improved.

## 6. Bounded Check For Stronger Known Guarantees

**A genuinely stronger solver already applies to a restricted tower
subclass.** The construction in
[TOWER_SOURCE.md:111](/Users/jaspersands/Developer/qsearch-research-work/prime-ag-tower-source-2026-10-26/TOWER_SOURCE.md:111)
exhibits a nonzero Schur-cube annihilator for G=10I+3R on covers containing
the specified degree-eight cover, with R over the specified place. The
quadratic nonsquare construction supplies a polynomial-time, all-syndrome
witness solver given its orthogonality and rank inputs.
[Ragavan-Shutty, Theorem 6.2 and Section 6.2](https://arxiv.org/html/2610.00502v2#S6).

For these complete AG codes, any nonzero cube annihilator has support
at least 3d-2g+2=20e+9>d. Restricting B to that support has full row rank:
otherwise some nonzero rowspace word would vanish on more than d places.
The source computes the annihilator from B and uses this criterion, so
its solver does not need a supplied witness or geometric advice. This
is strictly stronger than exponential rejection for that subclass, but
does not provide uniform samples. The source explicitly excludes arbitrary
degree-(2g+1) divisor classes from this guarantee; such classes can have
full cube rank. I checked the stated reduction and its applicability
conditions, not the tower's geometric construction or its old test receipts.

**An applicable general existence theorem is not a runtime theorem.**
Nagy-Pach's Theorem A permits one forbidden input and output value per
coordinate for every invertible matrix over prime p>61, p!=79.
[Primary paper, Theorem A](https://arxiv.org/html/2107.03956#S1).
Our inference: delta>k implies B contains two disjoint column bases,
since removing k columns cannot destroy row rank. Fix all other variables
to 1, write the residual equation with invertible blocks B_1,B_2, and apply
the theorem to M=B_1^(-1)B_2, forbidding 0 in the input and B_1^(-1)s'
in the output. This yields a full-support solution for every s. The tower
has delta_0>k, and p=100003 satisfies the prime condition. This known
existence result is broader than alpha<1, but I did not verify a
polynomial-time witness extractor from it. Do not substitute existence
for algorithmic cost or for a uniform-sampling law.

The generic random-matrix algorithms summarized in Ragavan-Shutty require
the quadratic-column regime; m=22e and k=5e+3 do not meet m=Omega(k^2)
as e grows. Their extension-field route does not directly apply to this
prime-field input. No obvious stronger generic polynomial construction
for every promised arbitrary-divisor-class input was established in this
bounded check. This is not a literature-completeness or hardness claim.
[Ragavan-Shutty, introduction and Section 6](https://arxiv.org/html/2610.00502v2#S6).

## 7. Exact Verification Evidence

Independent control:
[exact_controls.py](/Users/jaspersands/Developer/qsearch-research-work/systematic-review-2026-10-27/exact_controls.py).
Recorded output:
[exact_controls.json](/Users/jaspersands/Developer/qsearch-research-work/systematic-review-2026-10-27/exact_controls.json).

```sh
/opt/anaconda3/bin/python -B /Users/jaspersands/Developer/qsearch-research-work/systematic-review-2026-10-27/exact_controls.py
```

Exit 0; status PASS. The script uses only Python's standard library and
does not import the parent sampler, FLINT, an AG bundle, or any parent
test. It does not enumerate nonzero free assignments or run seeded replay.
It compares the projective character sum against the independent formula

```text
N_s = sum_(S subset coordinates) (-1)^|S|
      * 1[s in im(B_(S-complement))]
      * q^(m-|S|-rank(B_(S-complement))).
```

Exact totals: 8 fixtures, 128 syndrome comparisons, 285 conditional-cap
mass identities, 128 phase-reversal identities, 100 detected unsigned-
weight mutations, and 116 detected omitted-phase mutations. Integer and
Fraction inequalities check the tower at e=8,16,32,64,128,1024. Decimal
values in the receipt are approximations only; the inequalities are exact.
The all-e proof is Section 4, not extrapolation from these six levels.

The capped-mass controls verify the algebraic law for an injective uniform
proposal. They do not claim to test the parent's mapping implementation.
The edge-case formulas and static code review cover the mathematics;
backend zero-width matrices, input validation runtime, and actual native
replay remain the parent's direct-test responsibility.

### Reviewed Source Identity

`BASELINE.md`, unchanged across the two recorded hashes:

```text
d6a858493c5fb3f60ede1adfc2f794469b0d9acf6ba2c751705738b3d49fbf9e
```

Initial `systematic.py`:

```text
e2556e8e98179ab9c3fd6da71a3ae88d9179f959291a8f52239384d0c88d828b
```

Final statically reviewed `systematic.py`, with cached particular solution:

```text
0bcc4aa03774d9902a48ab846cc319d57dba470e2aed001a17c07bb348676b57
```

Read-only dependency `ag-affine-sampling-2026-10-26/affine_sampling.py`:

```text
8aae8d2ae1b196f21c13cf8e144c6f4c1215ac8bbd0b3789e98ab5647dcc40a0
```

Review control source SHA-256:

```text
74283982999fe15176b80b9d4369f08a845797aab30a89e55d3f93f87edd1128
```

Recorded JSON SHA-256:

```text
8fb7174d849de5299f988040ac24c20a377ed6ab34fbf563e19ca1e5189cdb7b
```

The parent was concurrently active; this verdict is tied to these hashes,
not to any later uninspected revision. No parent test suite or historic
receipt is represented as an independent verification run here.
