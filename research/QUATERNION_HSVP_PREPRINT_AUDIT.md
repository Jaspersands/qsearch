# Quaternion HSVP Preprint: Version-Scoped Audit

Date: 2026-10-30. Status: two exact counterexamples, independently checked
by a second automated reviewer; no author contact or human peer review.
This audits one cached public preprint, not all quaternion algorithms and
not an uninspected later publisher version.

## Sources And Provenance

Ling--Mendelsohn--Porter, *Dimension-Reducing Algorithms for Quaternion
Ideal-SVP*, [ePrint 2025/1448](https://eprint.iacr.org/2025/1448), public
version `20260213:120553`. [Versioned PDF](https://eprint.iacr.org/archive/2025/1448/1770984353.pdf).
Cache: `literature_cache/eprint_2025_1448_20260213.pdf`, 35 pages, 537416
bytes, SHA-256
`6fd5bb9f8f6e2279594e0617d973b1f8b4bd3a29938833b11b9d848b105d58dc`.
Page numbers below are printed PDF pages. The later
[Eurocrypt publisher chapter](https://link.springer.com/chapter/10.1007/978-3-032-25327-9_2),
pp32--61, was not available in full. Do not attribute these findings to
that text without checking it.

Limbrey--Ling--Porter, *QuaILLL: Quaternion Ideal LLL and BKZ*,
[ePrint 2026/1755](https://eprint.iacr.org/2026/1755), version
`20260820:215335`. [Versioned PDF](https://eprint.iacr.org/archive/2026/1755/1787262815.pdf).
Cache: `literature_cache/eprint_2026_1755_20260820.pdf`, 40 pages, 755237
bytes, SHA-256
`ba618e98df5f3ae354fa8e6dd7e9c5920e5bf77e5159da35158a71726a2d0a35`.
No counterexample to this second paper is asserted here.

## Finding 1: Covolume Does Not Scale As Printed

Let O be an order in a quaternion algebra with center degree n, I an
integral full ideal, and nu(I) the absolute reduced ideal norm. The cached
2025/1448 preprint p15 uses

```text
covol(I) = sqrt(nu(I)^2 * disc_Z(O)).
```

Definition 14 p16 therefore sets a length target proportional to
`nu(I)^(1/(4n))`. But for ANY fixed linear lattice embedding,

```text
covol(I) = [O:I] * covol(O).
```

For the maximal-order ideals in question, [O:I]=nu(I)^2. The definitions
and Lemmas 3 and 7 distinguish this index/algebraic norm from nu; silently
reinterpreting nu as the index is incompatible with the paper's other
identities. The simplest decisive check is I=tO, positive integer t:

```text
nu(tO)=t^(2n),       [O:tO]=t^(4n),
covol(tO)=t^(4n)*covol(O).
```

The printed formula scales by t^(2n), and its HSVP threshold by sqrt(t),
whereas actual lengths scale by t. This check is independent of the
normalizing constant for the chosen embedding. Use the index universally;
replace it by the squared reduced ideal norm only where that identity is
established. In particular, Definition 14 allows arbitrary orders.

For the explicit Hamilton Hurwitz order
`O=Z[1,i,j,(1+i+j+ij)/2]`, Definition 12's embedding has squared length
`2*nrd(x)` and covolume 2. For I=9O:

```text
nu(I)=81, index=6561, actual covolume=13122,
printed covolume=162.
```

The exact Gram determinant certifies the actual value. This invalidates
the interpretation of the displayed normalization as ordinary HSVP. It
does not prove all later statements irreparable; their constants and
hypotheses must be rederived under a consistent normalization.

## Finding 2: Theorem 8 Can Return An Element Outside I

Theorem 8, p19, assumes a two-sided integral ideal I of a maximal order,
unramified prime support, and `I intersect O_K = J^2`. It states that a
suitable short x in the descended J also solves HSVP in I. Its proof
embeds the SAME x and compares lengths, without proving membership.

Take K=Q, L=Q(i), the Hamilton algebra `(L/K, conjugation, -1)`, the
Hurwitz maximal order above, and I=9O. All stated hypotheses hold:

- I is integral, full and two-sided.
- The algebra parameter -1 is a unit in O_L.
- `I intersect Z=9Z=(3Z)^2`; take J=3Z.
- Prime 3 avoids the order discriminant support 2.
- The decomposition field is Q, and x=3 solves 1-HSVP in J.

But x=3 is NOT in 9O: its coordinates in the 9O basis are
`(1/3,0,0,0)`. It therefore cannot solve ANY short-vector problem in I,
regardless of the approximation factor. Correcting Finding 1 cannot fix
this independent membership failure. Unramified support does not mean a
squarefree ideal; the square ideal in this counterexample is permitted.

### A Scoped Repair, Not A Rescue Of The Printed Statement

Put a=I intersect O_K. Under the two-sided, maximal-order and unramified
support hypotheses, local matrix-order classification gives I=aO.
Solve the number-field short-vector problem in a, not its ideal square
root. Then membership is automatic. With actual covolumes Delta_K and
Delta_O and an embedding bound `||x||_A <= c*||x||_K`, the resulting
standard HSVP factor is

```text
gamma_A = c*gamma*Delta_K^(1/n)/Delta_O^(1/(4n)).
```

Indeed covol(aO)=Norm(a)^4*Delta_O, so the ideal norm cancels. Any
number-field descent adds its own factor and requires its own ramification
and effective-input hypotheses. J and J^2 have the same automorphism
stabilizer, so using the squared ideal need not lose that decomposition
field. This observation does NOT supply a polynomial-time constant-factor
number-field HSVP solver. Squaring x is another membership repair, but
needs a different length analysis, generally quadratic in gamma.

## What The Quantum Label Does And Does Not Supply

The public preprint's Algorithm 3 p27 uses quantum factoring in its
arithmetic preprocessing and still requires a number-field ideal-HSVP
oracle. Its other reductions have explicit two-sidedness, hereditary-order,
intersection, and ramification promises; these have not been established
for arbitrary native Hawk instances. Output is a short nonzero element,
not an exact reduced-norm generator. Published efficient number-field PIP
and unit algorithms are not, without another argument, constant-factor
HSVP algorithms. Keep this distinction even after repairing the two errors.

## The Correct Comparison To A Norm Target

Read [QUATERNION_NORM_SLICE_AND_LOCAL_FLAGS.md](QUATERNION_NORM_SLICE_AND_LOCAL_FLAGS.md).
In its target metric Q_q, let `Delta_q=sqrt(det(G_q))`. On an exact-q YES
instance, lambda_1=sqrt(d). A genuine standard gamma-HSVP output in THAT
metric guarantees relative length at most

```text
gamma*h_q, where h_q=Delta_q^(1/(4d))/sqrt(d).
```

The preprint's coefficient/canonical embedding is generally not Q_q:
even for the Hamilton CM presentation, Q_q introduces embedding weights
`1/sigma(q)`. An untwisted guarantee cannot simply be transferred.

Even optimistically granting a correct weighted analogue, the displayed
structured losses do not certify the exact target. For the natural
power-of-two cyclotomic Hamilton order Lambda=O_L+u O_L, Q_1 has Gram
`d*I_(4d)` in its cyclotomic coefficient basis, so h=1. For a maximal
overorder O of index C, h=C^(-1/(4d)); norm-exact multiplication pulls this
metric back to the order. Set c=C^(1/(4d)). Factors 2c or sqrt(2)c would
thus yield relative factors 2 or sqrt(2), before multiplying by the
number-field solver's gamma>=1. Neither is strictly below sqrt(2).

This is only an optimistic interface comparison, NOT validation of the
preprint's affected bounds and NOT proof actual outputs always fail.
A sharper guarantee or a successful norm check could still matter.

## Stronger Matched Classical Baseline

QuaILLL develops structure-aware classical LLL/BKZ for quaternion module
lattices, using natural orders inside rational norm-Euclidean quaternion
orders. Its cyclotomic applications include conductors divisible by 3 or
4. Quaternion rank d represents real dimension 4d, not constant dimension.
Its Table 2 p38 compares quaternion block size beta to real block size
4*beta. Section 7 retains order and module-basis hypotheses. Short
sublattice output and full-basis recovery have different bounds.

Theorem 5 p18 uses an HKZ-reduced over-lattice and exponential recovery;
it is not a polynomial exact-SVP result. The paper leaves a numerical
comparison for future work. An implementation should use the SAME Q_q
metric, certify its input module basis, and independently verify every
output's membership and reduced norm. Neither the present repo nor these
controls implement that baseline.

## Reproduction And Scope

`tests/test_quaternion_hsvp_source_scope.py` contains 9 exact controls:
Hurwitz norm/Gram normalization, five scalar homogeneity cases, the 9O
membership counterexample, a bounded square-root-ideal family and the
repaired center-ideal scaling. Together with the other three quaternion
test files, 72 controls are provided. They are
small falsifiers of universal statements, not quantum benchmark instances.

No registry negative against general quaternion algorithms is justified.
No external report was sent. Before any communication, check the full
publisher text for corrections and prepare a narrowly versioned note.
Research priority remains a constructive mechanism for the actual norm
target, not an extended campaign against approximation constants.
