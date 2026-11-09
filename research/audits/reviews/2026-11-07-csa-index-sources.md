# CSA Schur index: source and classical-baseline closure

2026-11-07. Read STATE/TRAPS and the retained actual sources. Interpreter
`/opt/anaconda3/bin/python`; no Git/network/API or new tests. This review
concerns INDEX only, not constructing a division algebra, minimal module,
primitive idempotent, or explicit noncommutative Wedderburn isomorphism.

**Verdict:** the Schur-index endpoint has a classical randomized polynomial
BIT algorithm given integer factoring. The fixed-S Amitsur period-lattice
route is unnecessary for this output. No GRH, class-group or S-unit advice
is needed for this classical baseline. “Deterministic polynomial with integer
factoring alone” would overstate the actual source: finite-field polynomial
factoring is a second oracle in its deterministic theorem.

## Actual maximal-order theorem

`audits/sources/csa_minimal_module/voight.txt`1487–1492, Theorem7.2, states
that a SEMISIMPLE F-ALGEBRA B admits maximal-order computation in
deterministic polynomial time given integer factoring AND finite-field
polynomial factoring. Although most of the surrounding paper treats
quaternions, this theorem explicitly treats general semisimple algebras.
F is a number field (1471); expanded number-field and multiplication-table
encodings are specified at131–136,148–165. No fixed algebra or field degree
restriction appears in Theorem7.2. The theorem is attributed to
Ivanyos–Ronyai, Theorem5.3; reference[16] at1971–1972 identifies their1993
paper. That original proof was NOT locally read in this review. Voight's
actual theorem statement, rather than a conjecture inferred from the title
of the original, is the present source authority.

Uniformity can also be made unambiguous by restricting A/K to Q: its
dimension becomes `[K:Q] n^2`, and its expanded rational structure table has
polynomial input size. Apply the theorem with F=Q. A maximal Z-order
automatically contains O_K: adjoining central integral O_K elements produces
an order containing it, so maximality forces their inclusion. It is therefore
a maximal O_K-order. No growing-field constants are hidden in this route.
Randomized polynomial finite-field factoring removes that oracle in
randomized polynomial time; integer factoring remains the sole external
classical oracle. Certified factors/irreducibility and capped randomized
clocks can make exhaustion an ABORT. Quantum integer factoring consequently
also pays this INDEX calculation without adding GRH.

## General-index formulas, not the character-specific shortcut

`audits/sources/division_algebra_selection/nebe_steel.txt`44–48 accepts a
general semisimple rational algebra in regular representation, obtainable
from structure constants. Section3.1,78–145, applies to an arbitrary simple
algebra with number-field center. Corollary3.4 at128–140 recovers each
finite local index s_q from the maximal-order DISCRIMINANT IDEAL:
`v_q(discid(A)) = n(n-n/s_q)`, hence
`s_q=n^2/(n^2-v_q(discid(A)))`.
The global index is the lcm of the finite and real indices (137–145).
Theorem3.5,151–163, distinguishes real split/quaternionic cases from the
signature of the reduced-trace form. Complex places contribute1.

The rational-discriminant shortcut in Theorem3.12,249–270, REQUIRES uniformly
distributed invariants (in particular the stated Galois-center/local-index
condition). It cannot recover arbitrary K-place indices from one rational
discriminant exponent. Use the discriminant IDEAL/general formulas instead.
This distinction does not restrict maximal-order construction itself.

The ideal computation is paid with expanded lattices. Reduced trace is
`(1/n)` times regular K-trace. From a Z-basis of the maximal order Lambda and
an integral basis of O_K, exact rational/integer linear algebra computes
`Lambda*={x:Trd(x Lambda) subset O_K}` and its finite O_K-module
`M=Lambda*/Lambda`. Its cardinality has polynomial bit length. Factor it and
decompose each relevant rational prime in K (finite-field factoring).
To obtain the length at q, let `E=v_p(|M|)` and compute the Z-lattice
`Lambda+q^E Lambda*`. The quotient of Lambda* by this lattice is precisely
the q-primary component of M; its order is `Norm(q)^length_q(M)`.
HNF indices recover the exponent above. E is polynomial NUMERICALLY in
the input/output bit length, so these ideal powers and lattices stay within
polynomial BIT bounds. This avoids assuming a free O_K-basis or an uncharged
principal-generator/ideal-class computation. Real signatures use exact
diagonalization and algebraic root/sign isolation on expanded data.

## What Nebe–Steel alone did and did not establish

Its radical-idealizer chain is166–191; hereditary-to-maximal enlargement is
194–225 and takes exactly k-1<=n-1 local steps. The implemented routine
273–309 uses finite-algebra maximal TWO-SIDED ideals, not a global minimal
left ideal. It asserts finite-field linear-equation implementation at185–186
but contains no standalone uniform polynomial-BIT theorem. Theorem7.2 above
supplies the missing complexity authority. There is no intrinsic iteration
or height obstruction here: all overorders lie between an initial integral
order and its trace dual, giving a polynomial-log discriminant bound on
strict enlargements; HNF in that fixed rational lattice bounds coefficient
sizes. Thus the paper's lack of a complexity paragraph is not evidence of
a remaining quantum opportunity or of an exponential algorithm.

## Fixed-S Amitsur period lattice: valid reuse, redundant endpoint

`audits/sources/global_isotropy/amitsur.txt`1070–1097, Theorem4.11/proof,
requires ramification places, class-group-generating places and the finite
support of the coboundary. For the presentation cocycle c, choose S once
containing ramification, class generators and Supp(D(c)). Every c^e has
support inside that same set. Therefore, whenever c^e is a coboundary,
Theorem4.11 gives a trivializing cochain among the units over S in the
DOUBLE tensor algebra. Conversely a differential-lattice solution proves
it is a coboundary. Complete S-unit data and exact relations consequently
recover the order of [c] without constructing tensor powers of A.

This is a legitimate consequence of KM's bounded-tensor machinery, not a
new paid primitive: Algorithm2/Theorem4.12 are1103–1163 and the split-only
Theorem4.13 is1164–1173. Period=index over number fields gives the same
integer that the classical maximal-order/local-index method already pays.
It does not construct the division presentation or minimal A-module. Any
new candidate using the computed index must earn that separate constructive
endpoint; this review does not validate the proposed follow-on construction.
