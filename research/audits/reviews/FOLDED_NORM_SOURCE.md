# Referee review: FOLDED_NORM_SOURCE

Note: `research/FOLDED_NORM_SOURCE.md`. Reviewed 2026-11-14 by claude-subagent-refresh-2026-11-14. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agree on the two gaps, and I confirmed each. The title says 'Matched Attacks' although the body states the budgets are 'deliberately EXPLICIT but NOT MATCHED'. The Result table's 'Classical Best' column (21/53/99) is superseded by the same note's norm-pencil scores 25/57/104 (folded_norm_attacks.json best_score 25/57/104, two inputs with norm_pencil_word_exceeds_conditional_quantum_mean_lower_bound=true). The Gauss phase, the collision bound, the fixed-input factorial-moment bound and the uniform-family arithmetic hold, and I recomputed 0.0444336, 0.000569869 and 36384099/40000000. Judge A's side remark that the decoder dimension constants (1860t, 2800t, 188t) are asserted rather than derived was not raised as a claim, and I could not confirm a defect, so it is dropped.

## Claims

### 1. holds

> Each basic fit/repair record uses32 complete-block fits plus64 repair proposals, and the norm-pencil attack below adds four 2048-parameter retained-value lines (solving the 25-block input at 25/25 and reaching 57/65 on the 65-block input, above its 56.698728 floor)

- Step: Same-Input Classical Results And Limits (table)
- Finding: The table and description now explicitly include the norm-pencil attack column (25, 57, and 104 across the three records) alongside the 32 complete-block fits and 64 repair proposals.
- Conceded by the note's own self-check: no

### 2. holds

> Folded Norm Source: Phases, Scalar Rank And Same-Input Attacks

- Step: Title
- Finding: The title now calls the classical comparisons Same-Input Attacks rather than Matched Attacks.
- Conceded by the note's own self-check: no

### 3. holds

> Exact countercontrol p5,n2,m2,K3,ell1: each support has24 nonzero errors

- Step: Correct Whole-Ball Collision Bound
- Finding: Q-1=24, and only j=r=1 is admissible, giving (5-1)/24=1/6. At p7 the same formula gives 8/57 (48/342), and the squared pure-distance bound M*eps/(1-eps+M*eps) with M=3, eps=8/57 gives 24/73; both match physical_controls. Both judges checked the collision bound.
- Conceded by the note's own self-check: no

### 4. holds

> Thus |ghat(xi)|^2=1/(Q-1) when Q3mod4

- Step: Actual Public Field And Fourier Phase
- Finding: For Q=3 mod 4, tau_E=+/-i*sqrt(Q), so |eta+c*tau_E|^2=Q+1 and |ghat|^2=(Q+1)/(Q^2-1)=1/(Q-1). This is consistent with the artifact's canonical_Gauss_unit_i_power=3 and trace_Gram_determinant_character=1.
- Conceded by the note's own self-check: no

### 5. holds

> At127 blocks32 such fits have success upper<=2.789576e-7

- Step: Fixed-Input Sampling Bound
- Finding: Recomputed C(15,9)/C(12,9)/2^9=0.0444336 and C(39,23)/C(31,23)/2^23=0.000569869; the union over 32 fits of 8.717424e-9 is 2.789576e-7. The bound covers fresh full-anchor fits only, as the note says, and not the repairs or the pencil attack.
- Conceded by the note's own self-check: no

### 6. holds

> 36384099/40000000=0.909602475, safely above0.909

- Step: Uniform Growing Family, Not A Finite-Size Extrapolation
- Finding: Recomputed exactly: 999/2000+(31/32)(999/1000)(531/1250)=36424539/40000000, and subtracting 1e-6+1e-5+1e-3 gives 36384099/40000000. g=93n/20-31 gives the exponent -8448 at n=3200. The statement is explicitly conditional on an implementation within the synthesis budget.
- Conceded by the note's own self-check: no
