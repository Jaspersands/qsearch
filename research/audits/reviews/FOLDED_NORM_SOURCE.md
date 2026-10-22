# Referee review: FOLDED_NORM_SOURCE

Note: `research/FOLDED_NORM_SOURCE.md`. Reviewed 2026-10-22 by audit-correction-2026-10-22. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agree on the two gaps, and I confirmed each. The title says 'Matched Attacks' although the body states the budgets are 'deliberately EXPLICIT but NOT MATCHED'. The Result table's 'Classical Best' column (21/53/99) is superseded by the same note's norm-pencil scores 25/57/104 (folded_norm_attacks.json best_score 25/57/104, two inputs with norm_pencil_word_exceeds_conditional_quantum_mean_lower_bound=true). The Gauss phase, the collision bound, the fixed-input factorial-moment bound and the uniform-family arithmetic hold, and I recomputed 0.0444336, 0.000569869 and 36384099/40000000. Judge A's side remark that the decoder dimension constants (1860t, 2800t, 188t) are asserted rather than derived was not raised as a claim, and I could not confirm a defect, so it is dropped.

## Claims

### 1. gap

> Folded Norm Source: Phases, Scalar Rank And Matched Attacks

- Step: Title
- Finding: The norm-pencil section states that the budgets are 'deliberately EXPLICIT but NOT MATCHED' (96 full interpolations against 8192 scored line parameters), and that 'No matched quantum wall-clock/gate comparison is claimed'. The attacks are matched only in using the same input, so the title implies a cost-matched comparison that the body disclaims.
- Conceded by the note's own self-check: no

### 2. gap

> Each classical record uses32 complete-block fits plus64 repair proposals

- Step: Same-Input Classical Results And Limits (table)
- Finding: The 'Classical Best' column (21/53/99) omits the norm-pencil results the note reports later (25/57/104, matching folded_norm_attacks.json). Those results solve the 25-block input and put the 65-block input at 57, above its 56.698728 floor. Read alone, the table suggests the classical baseline lies below every quantum floor, which holds only at 127 blocks.
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
