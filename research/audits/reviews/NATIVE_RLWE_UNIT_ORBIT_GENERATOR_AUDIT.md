# Referee review: NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT

Note: `research/NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The algebra holds: the minimal multiplier delta_K of (f,k), the invariance of det(A) under common units, the AM-GM bound on Gamma and the all-scalars bounds on the two fixed native lines, and I reproduced both d64 fixed-line inequalities in both lanes from native_rlwe_scalar_orbit_d64.json. Judge B rated the note sound; judge A raised one scope gap on the sentence that a quantum unit wrapper around the native generators solves the wrong search space. I kept A's gap: that sentence carries no label condition, yet the obstruction is certified only on the saved d64 kernel, and the producer's own easy zero-label control (det(I+M^TM)=1) is there precisely to stop it being read as an ensemble statement. Everything else both judges marked holds survived my check.

## Claims

### 1. gap

> A quantum unit wrapper around the unmodified native generators would be solving the wrong search space

- Step: 3. Stronger Fixed-Native-Line Obstruction (final paragraph)
- Finding: Units cannot leave a native line (Section 2 is general), but whether the two native lines are the wrong search space depends on both fixed-line lower bounds exceeding t^2/E^2. That is checked only on the saved d64 kernel (two lanes). For the zero label the m-line bound is det(I)=1 and the obstruction fails, and Section 2 says units can be 'extremely useful' on a well-scaled orbit. The sentence needs the condition 'on labels where both fixed-line bounds reach t^2/E^2, certified on the saved d64 instance'. Section 7's easy-label control acknowledges the limitation but the sentence does not carry
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
