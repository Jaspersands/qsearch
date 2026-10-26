# Exact Classical Babai Test

## Scientific Question

Can a public classical lattice basis already meet the near-vector target,
either on the frozen native input or for every center at those parameters?
This is a test of the candidate, not another quantum source refinement.

The input is the complete J16 integer-character instance from
INTEGER_CHARACTER_NEAR_VECTOR.md. No row subset, reduced modulus, planted
target or rerolled center is substituted. LLL is run once on the full
1024-dimensional numerator lattice with delta=0.99 and eta=0.51.
The source artifact charges public-label generation; this producer records
basis reduction and exact verification separately.

## Native Result

The frozen 1024-coordinate, 1119-bit J16 instance is CLASSICALLY solved
at its declared mean-square threshold 13/200:

| Method | Exact mean square, shown as decimal | Meets 0.065 |
|---|---:|---|
| Original x=0 integer-rounding control | 0.08417206568 | No |
| Full-basis ordinary Babai | 0.06884104458 | No |
| Bounded last-plane search, offset -17 | 0.06266165019 | Yes |

All 65 prescribed branches were evaluated; they produced 65 distinct
assignments and exactly one threshold success. No IID or success-rate
claim is made. Exact fractions, assignments, basis coefficients and the
winning lattice point are in classical_baselines/integer_character_babai.json.
The complete reduced basis occupies 31,035,167 compressed bytes.

Paid LLL took 1232.23 seconds. Using that saved basis, the final exact
verification took 10.29 seconds and the 65-branch search took 8.15 seconds;
basis loading took 0.56 seconds. The earlier interrupted verification is
also accounted for below.

The trace of normalized squared GS lengths is about 845.452669. Its
all-target mean-square upper bound is 0.206409343, so NO all-target
classical certificate follows. The continuous-Haar Babai mean is about
0.068803114, not a discrete-input success guarantee.

This is a finite threshold falsifier, not asymptotic dequantization.
It does not match the quantum expected-distance upper bound 0.05949507,
falsify the quantum construction, establish a classical runtime scaling
law, or say anything about general CVP. Do not retune the target or modulus
post hoc to turn this failed benchmark gap into another positive signal.

[Babai's nearest-plane algorithm is standard](https://cims.nyu.edu/~regev/teaching/lattices_fall_2004/ln/cvp.pdf).
The contribution here is a matched exact test, with a structured
fraction-free calculation that avoids unmanageable powers of N in the
Gram determinants. It is not a new lattice-reduction algorithm.

## Two Different Falsifiers

Let b_i be a basis for the normalized dual lattice Gamma, and b_i* its
Gram--Schmidt vectors. Exact Babai rounding returns a residual

```
r = sum_i u_i*b_i*,  |u_i|<=1/2.
```

Orthogonality therefore gives, for every target,

```
||r||^2/m <= (1/(4m))*sum_i ||b_i*||^2.
```

A basis whose right side is at most 13/200 would CLASSICALLY meet the
quantum grid-distance target for every center at the tested parameters.
A failed bound says nothing about better bases, other algorithms or the
lattice's true covering radius. In particular, it is an upper bound,
not a lower bound proving a hard target.

Separately, the producer computes the exact Babai witness on the frozen
center vector. It extracts x from the numerator vector, independently
checks all modular membership equations, and then centers every
coordinate. This last operation can only improve distance, and is a legal
classical operation since Gamma contains Z^m. A successful native witness
falsifies that particular benchmark gap, not an asymptotic separation.

Neither criterion presumes that floating-point LLL actually returned an
LLL-reduced basis. The exact membership and determinant-index checks are
sufficient for the geometric bound. LLL quality only affects how useful
the resulting bound is.

## Why Normalized Elimination Is Exact

Write B for the integer numerator basis, so its rows belong to

```
Lambda = a*Z + N*Z^m,  a_1=1.
```

Every row has the form x*a+N*z. In a k-by-k minor, multilinearity permits
at most one row from the rank-one x*a part. Hence each such minor is
divisible by N^(k-1), including for composite N.

Cauchy--Binet then shows that each k-by-k minor of B*B^T is divisible by
N^(2k-2). For the leading Gram determinant Delta_k define

```
p_(k-1) = Delta_k / N^(2k-2).
```

These are integers, not rounded approximations. The normalized squared
Gram--Schmidt lengths of B/N are

```
p_0/N^2,  p_1/p_0, ..., p_(m-1)/p_(m-2).
```

In the usual fraction-free Schur recurrence, divide the FIRST update by
N^2 instead of 1, then divide each later update by the previous normalized
pivot. This exactly removes the known factors at every step. The producer
uses FLINT integer matrix arithmetic and exact division; a nonintegral
step is an error, not a tolerated numerical residual.

To incorporate the target c, append the vector N*c BEFORE forming the
Gram matrix. This vector also belongs to Lambda, so the same divisibility
argument holds for every cross minor. The resulting last-column/pivot
ratio is N times the target's orthogonal coordinate. Divide by N when
performing backward nearest-plane rounding. All rounding is done by
integer quotient and remainder, including ties.

Each row is checked to belong to Lambda. The final normalized pivot is

```
(det B)^2 / N^(2m-2).
```

Requiring it to equal 1 proves that the rows span the FULL lattice rather
than a proper sublattice. No unproved unimodularity from the basis
generator is assumed. Small prime/composite/large-integer controls
cross-check both the profile and final point against the repository's
independent ordinary Bareiss and Fraction nearest-plane implementation.

## Exact Coordinate Elimination

The saved native basis starts with 834 signed coordinate vectors N*e_j.
After a coordinate permutation, a basis with r such leading rows has block
form [N*D,0; C,E], where D is a diagonal sign matrix. The first r normalized
Gram--Schmidt squared lengths are exactly 1. Orthogonal projection of every
remaining row simply deletes those r coordinates, leaving E.

Thus det(B)=+/-N^r*det(E), and the normalized remaining Gram pivots are
exactly those of E with the SAME denominator convention above. The producer
performs exact elimination on this 190-dimensional core, then recovers
every one of the 834 other coefficients by signed integer rounding.
ALL 1024 coordinates contribute to the final distance and membership
checks. This is not a projected-objective or row-subset attack.

Small controls compare this transformation to unmodified exact Bareiss and
nearest-plane calculations, including negative coordinate rows, arbitrary
coordinate order and elimination of the coordinate whose public label is 1.

## Bounded Last-Plane Enumeration

Ordinary Babai uses one nearest integer for the last orthogonal coordinate.
The stronger attack adds each offset in the predeclared sequence
0,+1,-1,...,+32,-32 to that integer, and redoes exact backward rounding for
EVERY other coordinate. This is a bounded classical nearest-plane tree
search, not a new quantum primitive or a claim of independent samples.
All 65 assignments and exact scores are retained, as is the best full
lattice witness.

Only the last orthogonal residual can exceed half a cell. If g_last is
its normalized squared Gram--Schmidt length, the displaced branch obeys

```
D_raw <= trace(GS)/(4m) + (offset^2+abs(offset))*g_last/m.
```

For this basis g_last is about 1.94893e-7. Even offset 32 increases the
rigorous all-target bound by only about 2.00983e-7. This does NOT prove
the scores improve or decorrelate; the native witness is tested directly.
The branch radius was fixed after inspecting the ordinary Babai result
and its profile, before evaluating the additional branches. This is a
sequentially designed falsifier, not a held-out scaling campaign.

## Rounding Bounds And Evidence

Each normalized squared length is enclosed outward by 96-bit dyadic
rationals. Their sum therefore gives a rigorous interval and a covering
upper bound. This avoids writing an enormous common denominator formed
by summing all the exact fractions. The integer pivots are saved.

The full reduced basis is saved as deterministic gzip-compressed JSON,
with a SHA256 hash. The report also saves the full integer basis
coefficients, Babai point and scalar assignment. Thus the final witness
can be replayed independently without rerunning LLL or trusting a float.
The exact profile itself is regenerated by the producer; merely checking
an artifact hash is not a proof of the profile calculation.

For reference, a uniform CONTINUOUS Haar target has mean squared Babai
error sum_i ||b_i*||^2/12. The report records this quantity separately.
It is NOT treated as a theorem about the discrete center vector in the
native artifact, nor as a mixing or randomized-search guarantee.

## Interpretation Rules

- A native success is a concrete classical witness on one fixed input.
- An all-target covering certificate covers the stated fixed lattice,
  not every length in the asymptotic quantum family.
- Failure of this one LLL basis is not classical hardness. BKZ, randomized
  rounding, adaptive bases, local repair and p-adic methods remain open.
- An expensive preprocessing step is never a free oracle. Both its
  complexity and its measured execution cost must remain visible.
- Do not compare the saved 1119-bit J16 instance to the older 924-bit
  first-moment instance.
- The quantum procedure and its reduction remain independently
  review-pending. This classical test does not certify their correctness.

## Reproduction

```
python theorems/integer_character_babai.py
python -m pytest -q tests/test_integer_character_babai.py -W error::RuntimeWarning
```

The native test replays the complete baseline and winning witnesses and
all 65 scalar assignments, reconstructs bound arithmetic, checks every
eliminated coordinate row, and independently checks the first eight
original and first eight nontrivial core Gram pivots. It does not
independently recompute the entire profile. The producer performs that
more expensive full-lattice check; no reduced-dimensional proxy certifies
the native result.

Verification: 10 tests for this module and 287 connected tests passed
with RuntimeWarning fatal (32.47 seconds for the connected run).
Python compilation, all 12 site JavaScript syntax checks, site checks,
registry validation (valid:true, issues:[]) and git diff whitespace checks
passed. This is not a claim that the entire repository test suite ran.

For exact profile and search replay using the saved paid basis:

```
python theorems/integer_character_babai.py --reuse-basis
```

The basis provenance records its input hash and 1232.23-second LLL run.
The first generic verifier was stopped after 64 reported elimination rows,
at an observed process elapsed time of at least 1507 seconds INCLUDING LLL
and basis serialization. That unfinished verification produced no result.
The saved basis was retained unchanged before implementing the analytic
coordinate elimination. Do not omit this cost or add LLL twice to that
observed elapsed total. Subsequent basis-load, exact-verification and search
times are reported separately.
The completed ordinary-Babai-only replay used during attack design also
took 10.81 seconds of exact verification and 0.57 seconds of basis loading;
it preceded the final extended replay and is not an additional LLL run.
