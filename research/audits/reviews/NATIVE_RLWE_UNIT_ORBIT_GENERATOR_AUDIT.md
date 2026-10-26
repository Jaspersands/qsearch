# Referee review: NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT

Note: `research/NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT.md`. Reviewed 2026-10-23 by codex-audit-correction-2026-10-23-r3. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The prior scope gap is withdrawn after checking the full surrounding passage: the unit-wrapper sentence follows the explicit saved native d64 scope and fixed-line conditions. The zero-label countercontrol remains, so no ensemble obstruction is claimed. The unchanged algebraic claims concern the determinant multiplier, common-unit invariance and fixed-line AM-GM bounds, with the two saved d64 obstructions. This corrects the review's reading of scope; it is not a new formal proof or a claim of general hardness.

## Claims

### 1. holds

> A quantum unit wrapper around the unmodified native generators would be solving the wrong search space

- Step: 3. Stronger Fixed-Native-Line Obstruction (final paragraph)
- Finding: The surrounding passage explicitly starts 'On the saved native d64 kernel, both lanes pass the EXACT obstruction'. The preceding paragraph states the required fixed-line lower-bound conditions, and Section 7 retains the easy zero-label countercontrol. Within that stated saved-instance scope, units cannot escape the two obstructed native lines. The earlier review incorrectly demanded a qualifier already supplied by the paragraph; this does not certify an ensemble obstruction.
- Conceded by the note's own self-check: no

### 2. holds

> This is the MINIMAL positive constant determinant multiplier for that fixed relation within K

- Step: 1. Correct The Completion Ideal First
- Finding: fG-gF=q(fz-kF) with z,F ranging over R, so constant determinants are exactly q times integers in (f,k); the least positive is q*delta_K and the HNF/Bezout witness attains it. (f,g)=(f,qk) lies in (f,k), and lift invariance k->k-Hf checks.
- Conceded by the note's own self-check: no

### 3. holds

> The projective direction `[g:f]` is unchanged, as is the coefficient metric's geometric mean a_geo

- Step: 2. A Common Unit Cannot Change The Line Or Its Volume
- Finding: C_(ug)=C_g C_u, so A->C_u^T A C_u and det(A) scales by Norm(u)^2=1; u*v1 spans the same R-line.
- Conceded by the note's own self-check: no

### 4. holds

> AM-GM gives, for EVERY common unit and every completion preserving that first block's volume

- Step: 2. A Common Unit Cannot Change The Line Or Its Volume
- Finding: The first-block squared GS product is det(A) and the full product is Q^(2d), so AM-GM on each block gives d*a_geo+d*Q^2/a_geo>=2dQ. This takes Gamma as the sum of squared GS lengths, as defined in the companion balanced-relation and subfield notes; this note does not restate it.
- Conceded by the note's own self-check: no

### 5. holds

> ANY nonzero field scalar u that sends the first vector to an integer point IN K must have u in R

- Step: 3. Stronger Fixed-Native-Line Obstruction, Including S-Units
- Finding: u(q,0) in the kernel needs uq in qR, so u is in R; u(-m,1) integral needs u in R. For the m-line, trace/d of C_u^T A C_u is at least det(A)^(1/d)|Norm u|^(2/d)>=det(I+M^TM)^(1/d).
- Conceded by the note's own self-check: no

### 6. holds

> On the saved native d64 kernel, both lanes pass the EXACT obstruction

- Step: 3. Stronger Fixed-Native-Line Obstruction, Including S-Units
- Finding: From research/certificates/native_rlwe_scalar_orbit_d64.json (q, E=4351/4545, labels, 2800-digit centered m-line Gram determinant) I recomputed q^2E^2>=t^2 and det*(E^2)^64>=t^128 exactly: both hold in both lanes (log10 det^(1/d)=43.74 against log10(t^2/E^2)=30.94/30.84). Seed 290955, counts 144/16/3/6 and ratio 665857 match the note.
- Conceded by the note's own self-check: no
