# Paired partition DPP: actual classical baseline scope

2026-11-13. Bounded primary-source screen following the scoped Gaussian
feedback falsifier. General native projected-Slater sampling remains OPEN;
no new quantum correction, novelty, hardness or separation is admitted.
STATE/TRAPS were read first; corpus been-tried and baselines for partition
DPPs, size-two parts and rank-two mixed discriminants preceded the literature.
The catalogue had no direct match; that is not evidence of classical hardness.

## The exact native bridge, without a normalization convention ambiguity

Let V be the native 2s-by-s complex rational isometry, and write its two
rows in pair j as v_(j,0),v_(j,1). Define s-by-s PSD matrices

    A_j=v_(j,0)^* v_(j,0)+v_(j,1)^* v_(j,1),
    rank A_j<=2, sum_j A_j=I.

Cauchy-Binet applied to det(V^* diag(x_pair) V) proves

    Z = [x_1...x_s] det(sum_j x_j A_j)
      = sum_z |det V_(I(z),:)|^2.

This defines our coefficient normalization explicitly; no factorial convention
for the phrase mixed discriminant is imported. The constrained L-ensemble
with L=VV^* has exactly these weights on one-per-pair subsets, since those
subsets have size s. Z is the Slater projection probability, not the full
L-ensemble partition function det(I+L). A hardness statement about exact
normalizers does not by itself imply approximate sampling hardness.

## Actual general partition algorithm: growing parts remain unpaid

Celis-Deshpande-Kathuria-Straszak-Vishnoi, APPROX/RANDOM2017, actual
Corollary5 and its interpolation proof bound runtime polynomially in the
PRODUCT of (||c_j||_1+1). Corollary10 is explicitly for CONSTANTLY MANY
partition parts. For s size-two parts, the displayed product is 3^s.
Thus this theorem does not give the desired polynomial native-input clock.
Small unary entries in each constraint do not make the product polynomial.
The actual AppendixB Theorem21 is a counting/sampling reduction with
evaluation access to the generating polynomial and suitable counting or
sampling oracles across the self-reduction; it does not supply those
conditional counts from one partition-function estimate.

Source: https://drops.dagstuhl.de/storage/00lipics/lipics-vol081-approx-random2017/LIPIcs.APPROX-RANDOM.2017.36/LIPIcs.APPROX-RANDOM.2017.36.pdf .
The downloaded text LF245-260,435-465,1072-1115 was read. Exact counting
claims or introductory beliefs about FPRAS are not transferred to our
promised isometry/TV endpoint.

## Actual small-norm approximation: a restricted normalizer comparator

Barvinok arXiv:1806.05105v2 Theorem1.8 approximates the logarithm of
sum_(S) (det B_SS)^m in quasi-polynomial n^{O_(rho,m)(log n-log epsilon)}
time, for FIXED m and rho<1 and ||B||<rho. Theorem1.4 instead assumes each
matrix near identity; Theorem1.6 applies to identity-shifted/contracted
versions of a doubly stochastic tuple, not an arbitrary original tuple.
Rank-two matrices in dimension>2 cannot be near the identity in operator
norm: a nonzero null vector gives ||A-I||>=1. Adding an identity changes
the target weights.

For a REAL native input and any valid transversal row matrix R, right
multiply all rows by R^-1. Baseline rows become the identity; let B collect
the alternative rows. Expansion along unaltered identity rows proves

    det V_(I(z)) = det(R)*det B_SS,
    Z = det(R)^2 * sum_S (det B_SS)^2.

This is a proof identity, not a supplied-chart oracle. It makes Theorem1.8
a normalizer comparator only IF a chart with the strict norm promise is
paid. Complex native inputs have squared MODULI, which are not automatically
the displayed square-power theorem. A single normalizer approximation is
also not a full conditional sampler; closure of its promises through
self-reduction must be proved before invoking that reduction.

The literal introduction on PDF page4 identifies B here with the GRAM
matrix of the alternative vectors. That printed identification fails the
one-dimensional check x=2: the mixed coefficient is 1+2^2=5, while using
the Gram scalar4 in 1+B^2 gives17. The correct B in our identity is the
COORDINATE row matrix, established directly above. This does not refute
Theorem1.8 itself, whose matrix input is explicitly B. The actual PDF page4
was visually inspected; this is not an OCR inference.

Source: https://arxiv.org/pdf/1806.05105v2 . Actual Theorems1.3-1.8 and
page4 were read; PDFs/text/URL and SHA256 metadata for both sources are in
`audits/sources/paired_partition_dpp/`. The author's redirect returned403;
the public arXiv version supplied the full primary text.

## Exact operation falsifier for an automatic contraction chart

The real rational isometry

    V=(1/2)*[[1,1],[1,-1],[1,1],[1,-1]]

has pairs (rows0,1),(rows2,3). There are exactly two valid transversal
bases. In either associated chart B=[[0,1],[1,0]], so ||B||=1. Its native
projection probability is1/2. Direct sums give arbitrarily large even s;
every valid transversal is assembled blockwise and its chart remains an
orthogonal block permutation, with norm1. Therefore no uniform rho<1
chart promise follows from the native input, even after choosing the best
valid transversal. The target family itself is classically trivial; this
is not a sampling lower bound or failure of every approximation method.

One exact Sage base-block check is saved in
`audits/controls/paired_dpp_chart/`, verifying V^T V=I, coefficient Z=1/2
and BOTH chart matrices/norms. An initial Sage row/matrix shape error was
corrected before the successful exact run. The all-size assertion follows from the
block-diagonal argument, not extrapolation from this control.

## Disposition and next concrete gate

The two actual published algorithms do not close the general native
classical sampler. This says nothing about algorithms not checked here.
The general quantum sampler also remains unconstructed. No new paid call
or quantum implementation was justified by the source audit.

Before returning to this line, require a concrete operation beyond the
refuted same-mode Gaussian architecture. One precisely scoped remaining
classical source check is whether newer fractional-log-concavity or
principal-minor-power samplers cover NON-HERMITIAN coordinate B and the
actual conditioned family, rather than only PSD B or fixed partitions.
Next command: corpus been-tried for that exact operation, then inspect its
primary theorem. Expected artifact is an explicit native-input theorem
mapping or a stated unmet premise. Do not infer hardness from an unmet
premise, and compare independent directions before another construction pass.
