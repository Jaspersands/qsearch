# Finding 1 Follow-Up: Proposed Native Preprocessing Repair

The independent review is unchanged. Its scope warning was correct: a
supplied global dictionary and full reference order are extra data. This
subsequent parent-authored repair is not a second independent review.

New bundle: native-suborder-preprocessing-2026-10-26.

The proposed construction recovers the target algebra from small-torsion
traces, constructs a full evaluable reference order, computes the rational
dictionary using the fixed-dimension algebra-isomorphism theorem, and clears
denominators in the original native basis. No unknown End(E), connecting
isogeny, large-prime target torsion or order-preserving algebra map is input.

Two distinctions matter:

- Rational tensor splitting uses charged factoring, with Q as a FIXED number
  field. It is not the maximal-order-given shortcut from a later paper. The
  implemented controls only extract dictionaries from supplied split modules.
- The general reference construction retains GRH. Its full-order recovery
  saturates only the small-CM SOURCE index, never the target's potentially
  large index. A discriminant argument supplies the needed Frobenius relation
  when p>4*q^2; the asymptotic theorem has a finite exceptional fallback.

For p=3 mod 4, an explicit y^2=x^3-x reference and half-Frobenius basis avoid
the reference GRH assumption. A regression rejects copying that basis to
y^2=x^3+x merely because it has the same j-invariant.

Disposition: WRITTEN CONDITIONAL REPAIR PROVIDED, NOT INDEPENDENTLY REVIEWED.
Native end-to-end execution is still absent. The conditional theorem imports
the prior source/receiver arguments and published PPAV/endomorphism-division
algorithms; it is not an unconditional new speedup. Novelty remains unproven.

26 new tests; final focused seven-bundle regression 221 PASS, syntax and
separate replay PASS. Exact commands and execution boundaries are recorded
in the new bundle's VERIFICATION.md. Do not merge these finite results into
the independent reviewer's findings or test counts.
