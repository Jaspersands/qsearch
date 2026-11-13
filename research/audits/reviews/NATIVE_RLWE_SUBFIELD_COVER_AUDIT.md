# Referee review: NATIVE_RLWE_SUBFIELD_COVER_AUDIT

Note: `research/NATIVE_RLWE_SUBFIELD_COVER_AUDIT.md`. Reviewed 2026-11-14 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The construction, the AM-GM headroom gate, the threshold theta>5/19, the max-density lemma and the leading coefficient (19/2)theta-5/2 all check, and every table value and headroom outcome matches the 54 rows of native_rlwe_subfield_cover_bounds.json. Both judges rated the note needs-work but on different gaps: A on the Section 4 closing sentence, which drops the theta<5/19 condition, and B on the density lemma, which needs every nonzero t invertible mod q while q is introduced only as 'the native modulus'. I kept both. A's gap is mostly conceded by the note's own 'Half-degree density bounds are VACUOUS'. B's gap does not affect the three prime reference moduli. The remaining claims the judges agreed on hold.

## Claims

### 1. holds

> For quarter degree and deeper (theta<5/19, at the stated prime q, P scaling and the three reference moduli), this independent source counting excludes typical successful AFFINE witnesses in the stated restricted output class

- Step: 4. Stronger Source Falsifier (closing sentence)
- Finding: Section 4's closing sentence now explicitly restricts the affine witness exclusion to quarter degree and deeper (theta < 5/19) at the stated prime q, P scaling and the three reference instances.
- Conceded by the note's own self-check: yes

### 2. holds

> has probability at most 1/U, where U=#R_q^*

- Step: 4. Stronger Source Falsifier For Actual Affine Points
- Finding: Section 4 now explicitly states the prime-q hypothesis so every nonzero scalar t mod q is invertible.
- Conceded by the note's own self-check: no

### 3. holds

> This is the FULL kernel in the restricted real subspace

- Step: 2. Explicit Classical Construction, No Missing Oracle
- Finding: H_h B_h=[qI,0]=0 mod q, [I,M E_h] maps onto Z_q^d so the kernel has index q^d=det(B_h), and E_h selects coordinates so E_h^T E_h=I_h.
- Conceded by the note's own self-check: no

### 4. holds

> Writing theta=h/d, the power threshold is theta>5/19

- Step: 3. Exact Necessary Geometric Headroom
- Finding: Gamma>=n q^(2d/n) by AM-GM on the GS product q^(2d). With q=d^12 the left side is d^(24theta/(1+theta)) and the right side is of order d^5 polylog, so the condition is 19theta>5.
- Conceded by the note's own self-check: no

### 5. holds

> Every quarter-degree/deeper reference row fails the necessary gate

- Step: 3-4. Reference tables
- Finding: In the artifact every row with subfield_degree<=d/4 has geometric_headroom_necessary_only=false. The half-degree flags (only d64 hidden_elliptical false) match the table, and the per-support log2 bounds -558/-572, -2806/-2802, -12715/-12236 match the quarter-degree rows exactly. R0=ceil(t_star/(2E)) matches rounded_affine_radius (1478681177790966 at d64 spherical).
- Conceded by the note's own self-check: no

### 6. holds

> At theta=1/4 its first coefficient is -1/8

- Step: 4. asymptotic log-bound
- Finding: With log R0 ~ 10 log d - (5/2) loglog d, log s ~ (1/2) log d, n=(1+theta)d and log U ~ 12 d log d, the exponent is (19/2)theta-5/2 times d log d minus (5/2)(1+theta) d loglog d, which is -1/8 at theta=1/4 under the stated q and P scaling.
- Conceded by the note's own self-check: no
