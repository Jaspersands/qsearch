# Good-dyadic growing-Selmer review dispositions

2026-11-06. Final scope: the written bounded-error quantum polynomial-BIT
composition in GOOD_DYADIC_GROWING_SELMER.md. Exact promised inputs only;
no full implementation, novelty, separation or Mordell--Weil rank claim.

## Independent review and parent verification

- Core derivation and final adversarial local review: growing_degree_mechanism.
  Parent rechecked Lang's constant etale Z/2 quotient in characteristic2,
  geometric connectedness via based Abel--Jacobi, Frobenius telescoping,
  two Weil bounds, and shallow formal generation. Accepted, with the
  integral differential-basis repair: independence of reductions (x is
  separating) plus Nakayama, not only characteristic-zero independence.
- Global/source audit: superlattice_source_scope. Accepted after adding
  SEPARATE -1 in each field component and a shared complete-source failure
  budget. Parent read actual Biasse--Song v2 Theorem5 (PDF26), Proposition2/
  Algorithm3 (PDF15--16), Definition8 and denominator correction (PDF28),
  Proposition7 (PDF29). Full lattice generation has adjustable error mu;
  subsequent sufficiently precise basis/compact recovery is deterministic.
  Proposition2's mu is a DIFFERENT shortest-vector bound, not failure rate.
- Family and independent integrated endpoint attack:
  independent_direction_selection. Accepted the odd-cyclic Grunwald/CRT
  construction after using the actual section2.1 paragraph, NOT the later
  theorem excluding primes dividing the group order. The p=m exclusion
  is supplied by t^m-t outside F_m. No input-generation height bound claimed.
- Strongest exact classical simplification: Q x K x K global norm-kernel
  is K(S_K,2)^2. Reuse K computation. The exact virtual-unit sequence still
  includes U_S/U_S^2 and Cl_(K,S)[2]; no cancellation or polynomial classical
  counterpart follows. Same descent with classical class/unit arithmetic
  remains the baseline, including its actual rigorous/heuristic scope.
- Linear Q components are explicit: trivial class group and S-unit primes
  plus -1. No log-discriminant generator bound is applied at disc(Q)=1.
- Parent read actual growing-degree integral-basis Theorem1, A=Z clause,
  including small residual characteristic. The quantum factored discriminant
  pays its input. Source/finite-algebra decomposition uses no free uniformizer
  or factor field; explicit idempotent and unit-minor coordinates suffice.
- Small representatives are not necessarily T-units. ORIGINAL valuations
  supply global parity. Clear coordinate denominators by rational squares;
  each atom's own log absolute norm bounds all local valuations. Precision
  maxima are chosen BEFORE fixing the common local frame. No enormous
  original unit product is expanded.

## Claude findings and dispositions

Run directories under audits/claude_runs/ with prefixes 2026-11-06-:

1. good-dyadic-trace-opus: empty provider refusal, 5375 input/142 output
   tokens, estimated USD0.02434. No mathematical findings; no retry.
2. dyadic-coordinates-opus: completed, 1412 input/9685 output tokens,
   estimated USD0.199348. Proof obligations verified independently:
   U1 intersect E*^2=U1^2; U_(3e) subset squares; full integer filtration
   kernel; quotient by R+2Z^k; mixed-characteristic carries handled by actual
   products; HNF entries polynomial from bounded index; finite-ring ideal
   division gives unique residue digits. No enumeration/DLog is hidden.
   The proposed f*m Cramer loss is conservative, not the optimal ceil(m/e).
   Keep the conservative bound and use component/table precision Q=2dV+10,
   exceeding the report's sufficient P+f*m assumption. Check each basis
   product belongs to the current U_j. No source correctness inferred from
   Claude's acceptance label.

Total estimated USD0.223688. Usage estimates are neither an invoice nor an
exact remaining balance. Requests/context snapshots retained unchanged.

## Exact finite falsifiers

`audits/controls/good_dyadic_selmer/exact_control.py` ran with
`/opt/anaconda3/envs/qsearch-cas/bin/python`; JSON is adjacent.

- Native genus3 G=x^3-22x^2-25x-1: disc559^2, irreducible modulo2,3,5,7,
  scaled branch factors1,3,3, affine smoothness gcd1 modulo2 and good
  odd3,5,7. Infinity follows directly from the monic odd model equation.
- Sufficient residue field q=32768 has16683 allowed distinct x and
  tangent rank3. This is not a Jacobian-order or complete local-image test.
- Exact O/8 for Q2(sqrt2): relation indices2,4,8,16,32;32 units,4 unit
  squares, unit class dimension3, full local dimension4. All1024 unit
  products obey the coordinate homomorphism and all squares map to0.
  Saturating the integer lattice would wrongly give unit dimension0.
- No Selmer dimension or quantum algorithm was executed. No asymptotic
  claim follows from these finite controls.

## Source scope and retained unknowns

Primary files in audits/sources/good_dyadic_selmer/source.json; source hashes
retained. Milne AV Remark8.12, Frobenius proof in ChapterII Theorem1.1,
Jacobians Propositions2.2 and6.1, and Theorem11.1 were read. Debes--Ghazi
section2.1 supplies the cited odd-cyclic Grunwald existence theorem.
Morgan16.4--16.5 already gives related good-ordinary product families;
no construction novelty claim. Stoll section4 permits reducible odd-degree
polynomials; Corollary4.7 and Lemmas4.4--4.5 give the global/local scope.
The scanned Milne Jacobian PDF was not used as readable text.

The draft irreducible-family genus obstruction has an unverified p-rank
source step and is NOT promoted or used. General wild bad dyadic models,
even/non-Galois branch fields, arbitrary hyperelliptic Selmer computation,
MW rank/points/covers and a classical separation remain outside this result.
No adjacent implementation queued; independently rank the next native
mechanism under STATE/TRAPS before new work.
