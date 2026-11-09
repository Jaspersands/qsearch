# Global isotropy: bounded actual-source and resource audit

7 November2026. Read STATE/TRAPS, the compact-output native contract,
the retained primary texts, and the earlier Amitsur audit. No Git/network/
API or implementation. PDF pp21--22 were visually checked for the literal
AppendixC formulas. **No source-only polynomial-BIT endpoint is established
by these papers together; this does not refute the proposed composition.**

## Versions and existing algorithmic scope

`audits/sources/global_isotropy/vectors.txt` is explicitly
2111.08569v2,12March2025 (line6), not the old v1. Its algorithms cover
global fields of characteristic not2 (10--17), but Section3 at145--162
ASSUMES ideal factorization, norm-equation solving and full S-singular
squareclass bases. AppendixA at793--804 calls its analysis crude and
explicitly says not all invoked subroutines have rigorous complexity
analyses. Implementation or finite tests do not close these gates.

Algorithm1 at360--399 takes an ALREADY ISOTROPIC4-form. It repeatedly
enlarges S until the squareclass/sign/Hilbert-symbol linear system becomes
solvable, then solves two ternary norm problems. Proposition4.5/Remarks2--3
at404--421 prove existence/positive density and describe exhaustive or
random prime search. These are correctness/termination mechanisms, not
yet a native capped polynomial-BIT clock.

## AppendixA: exactly what its bounds pay

Lines805--825 discuss ideal factoring via integer factoring and real-root
isolation; native Shor factoring can replace the former, with its own
error budget. Lines827--838 identify the first squareclass basis/S-unit
computation and an incremental-update dependence on the CLASS NUMBER.
That numerical class-number parameter is not free polynomial input size.
Lines842--846 cite polynomial Hilbert-symbol arithmetic and F2 solving;
these still require polynomial-size supplied local/global data.

The good-prime density lower bound at847--857 is
`product_(p in P(q) union {p0}) (Norm p)^(-1-ord_p4)`.
Lines858--866 infer polynomial average iterations from its inverse.
That inference is NOT established in coefficient BIT size: even over Q
a bad prime P of B bits gives a factor P in the inverse bound, which is
exponential in B. A weak exponential upper bound does NOT show the actual
density is small or the actual algorithm takes exponential time. Nor does
positive asymptotic density by itself specify an effective finite sampler.
The deterministic discussion at867--879 is polynomial in the NUMERICAL
discriminant, not log discriminant, and likewise does not pay this native
BIT claim. Do not substitute a new prime heuristic for either missing bound.

Norm-equation discussion at880--904 explicitly retains unresolved general
number-field complexity and expanded fundamental-unit-size dependence.
These are obligations to replace with a stronger paid interface, not a
proof that every compact norm/isotropy method is slow.

## Weak approximation and the revised local construction

Algorithm2 at517--548 forms local binary values, then uses weak
approximation to obtain s,t and reduce5 dimensions to4. Proposition4.8
at462--473 states finite congruence and real precision conditions. Their
existence is sufficient for correctness, but this paper does not prove a
uniform polynomial-BIT height/precision bound for all growing fields and
chosen local representatives. Lines595--602 explicitly warn of expression
swell. Algorithm4 at626--656 uses only REAL approximation for dimension
>=6 and reduces dimension by one recursively; it does not itself give the
candidate's proposed single paid5-dimensional restriction. In non-real
fields any5-dimensional subform is already isotropic (630--632).

AppendixC is NOT an exhaustive dyadic squareclass algorithm. Algorithms5/6
at1083--1141 directly construct a binary value outside one forbidden class
using uniformizers, local-square tests, a root step, and a nonsquare
sum-of-two-squares subroutine (reference13). Enumerating the entire dyadic
group would cost `2^([K_p:Q_2]+2)` entries (the formula at557--560), hence
can be exponential, but THIS source does not require that enumeration.
The random alternative at549--594 expressly lacks a rigorous general
probability analysis and discusses severe local-squareclass sampling bias.

Two literal AppendixC qualifications must not be silently imported:

- Algorithm5(3a),1092--1096, requests exact `a=b*u^2` from a LOCAL square
  premise while its stated output lies in K. For Q,p=3,a=d=1,b=13, the
  local premise holds but no rational u exists. A local-root approximation
  interpretation needs its own finite precision and global representative;
  an exact global square root is not supplied by the premise.
- Algorithm6(2)/(3),1129--1138, uses `2k>v(a)+v(b)`. For arbitrary K*
  inputs with negative valuations this does not ensure its claimed
  dominance. E.g. Q,p=3,a=1,b=1/27,d=1/3,k=1 is allowed, yet s=1,t=3
  gives `a+b*t^2=4/3=d*2^2`, the FORBIDDEN class. Nonnegative-valuation
  preprocessing or a corrected dominance condition needs explicit payment.

These are source-interface limitations, not a general local-construction
impossibility. Proposition4.8's congruence modulus also needs the actual
valuation normalization when data are fractional. A separate polynomial
local value/precision argument may replace these source instructions.

## Classification and anisotropic-part sources

`classification.txt` is1304.0708v2(2016), lines7--22. It gives local/global
isotropy, signatures, Hilbert invariants and anisotropic dimension, taking
local-square procedures as prerequisites at76--92. Its abstract speaks of
a fixed number field; do not infer a whole growing-degree BIT theorem from
that phrasing or implementation. The finite local criteria are useful
decision ingredients, distinct from construction of a point.
`anisotropic.txt` is2109.04172v1(2021), and80--108 explicitly assumes
principal generators, ideal factorization, S-class groups/S-units, root
isolation and Hilbert symbols. Its Algorithm1 at177--225 constructs
S-singular classes using class2-torsion and principal generators. Algorithms
2--4 at236--308 give sign/CRT/local-square recipes; they are not a theorem
that arbitrary compact-input repeated Witt reductions preserve polynomial
BIT size. The current native contract correctly does NOT claim that output.

## Existing compact splitting: retain GRH and output interface

Actual Kutas--Montessinos2307.00261v3 was extracted from the cached primary
PDF to `audits/sources/global_isotropy/amitsur.txt`; parent will record its
hash. Theorem3.10 at727--744 gives the probabilistic polynomial Amitsur
presentation over an efficiently computable field. Algorithm2 at1100--1132
uses COMPLETE S-unit coordinate maps in bounded tensor powers. Theorem4.12
at1135--1163 supplies GRH quantum-polynomial2-coboundary trivialization;
Theorem4.13 at1164--1173 gives splitting for a PROMISED split CSA. Its
etale algebra need not be an irreducible extension; no IRR heuristic or
factorial normal closure is needed. GRH class support and complete-unit
arithmetic are genuine assumptions, not free advice or removable wording.

The earlier `AMITSUR_ARITHMETIC_REUSE_AUDIT.md` supplies explicit compact
cochain-to-matrix formulas. Compact arithmetic-circuit splitting coordinates
are compatible with THIS native output; the old huge expanded-ideal gauge
example is not an output-size blocker here. Subsequent circuit zero tests,
compact linear algebra, quaternion descent and bounded-error verification
are separate proof obligations. Splitting only after a paid isotropy/local
decision also respects the source's promised-split input. No expanded
isotropic-point bound, full Witt decomposition, novelty or separation is
established by this scoped source review.

## Added Voight primary and uniform-degree clarification

Actual `voight.txt` uses BIT encodings at109--136: a number field is given
by its defining polynomial and power-basis coordinates. A finite place
is specified by a prime ideal, with uniformizer/valuation/reduction data
discussed at1144--1155. Proposition5.8 at1207--1211 and Theorem6.1 at1226--1228
state deterministic polynomial-time local Hilbert-symbol evaluation for
a number field F, WITHOUT a fixed-field restriction. This is usable for
growing-degree expanded native data, not just a constant-field assertion.

The dyadic proof supports that reading: Algorithms6.2/6.5/6.6 at1235--1349
use e=ord_p2 and residue degree f, both at most[F:Q]. The valuation lift
increases precision through at most2e levels; residue square roots in
characteristic2 use Frobenius, not enumeration of2^f elements. The residue
quadratic/root tests can be implemented by finite-field linear algebra.
The modulus size is polynomial because `log Norm(p^(2e))=2e log Norm(p)`.
Given the supplied maximal order, HNF/CRT arithmetic in these finite rings
does not require listing their elements. Do not replace this explicit
local polynomial procedure by the numerical size of a squareclass group.

Distinguish decisions and roots. Section4.9 at921--931 explicitly gives
deterministic finite-field square roots in characteristic2, probabilistic
polynomial roots in odd characteristic. Odd-place square decision is
explicit at1038--1067,1192--1197. Full dyadic square decision also needs
the finite-precision lifting argument; it does not follow merely from
a Hilbert-symbol decision theorem. The local-root paragraph1150--1153
asserts computability and invokes Hensel, not a separate explicit theorem
of uniform polynomial-BIT output to arbitrary requested precision. Theorem6.1
is a Hilbert-symbol theorem, not itself such a root-output contract.
For an invoked finite local square-root APPROXIMATION, specify the seed,
Hensel/Artin--Schreier lifts, precision loss from v_p2, and a global residue
representative. Charge requested precision m by `m log Norm(p)`, rather
than only log m, and cap any odd-residue randomized root routine. This
short finite-precision conversion remains a separate derivation if needed;
there is no evidence here of an exponential root-construction obstruction.

For ideals, Lemma7.16 at1689--1703 explicitly covers an ARBITRARY number
field and gives randomized polynomial ideal factorization with integer
factoring, retaining finite-field factorization randomness. Ring-of-integers
computation at1477--1482 reduces to the largest square divisor. Theorem7.2
at1489--1492 gives a general maximal-order forward algorithm using integer
AND finite-field polynomial factoring oracles; Theorem7.14 at1674--1678
gives the quaternion-order forward reduction to ideal factoring. The
factoring EQUIVALENCE Theorem7.15 at1685--1686 expressly says FIXED F;
do not use its converse/field-dependent constants as a uniform theorem.

`voight_errata.txt` at12--29 replaces Algorithm3.22 by an orthogonal-
complement/direct-sum test followed by HNF. It does not amend Theorem6.1
or the local algorithms above. Use the corrected algorithm if that optional
order-decomposition operation is invoked.

Amitsur's base-field degree is likewise not fixed: `amitsur.txt` at228--233
explicitly distinguishes old bounded-degree algorithms from arbitrary-
number-field algorithms. Theorem4.13 at1164--1173 takes the number field
as input; its structure-constant model is at165--192, and Facts2.1/2.2
at197--210 pay maximal orders/ideal factoring. This supports uniform field
degree in its GRH quantum-polynomial statement. The compact-output issue
is resolved for THIS contract by the existing reuse audit's explicit DAG
cochain-to-splitting formulas plus compact unit output, not by assuming
an expanded matrix-height bound from the theorem's word "explicit".
Compact later linear algebra and its charged circuit tests remain distinct.
