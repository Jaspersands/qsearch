# Referee review: INTERVAL_SOFT_DECODER

Note: `research/INTERVAL_SOFT_DECODER.md`. Reviewed 2026-10-22 by audit-correction-2026-10-22-r2. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Judge A's one gap, that the decision cuts superpolynomial separation claims 'at constant full-RS interval width' without the d<L, KV-certified window the body keeps, was confirmed on 2026-10-21 and reversed by the 2026-10-22 audit: every quantum guarantee the note cites (d/p<C<=L/p, and rate+density>1) needs d<L at constant L, where the DP is polynomial, so outside that window there is no quantum claim for the cut to remove. Judge B flagged the title and the receiver table (5 of 8 controls shown), and both were dropped. The title's 'Actual Receiver' and 'Classical Falsifiers' are accurate names for the executed p=5 receiver and the DP/Babai baselines, and the omitted complex and S={0} controls are discussed under 'Decisive controls', with no conclusion resting on the table. The Cauchy ceiling, the 3/2 tuning bound (451/1395, 19/45 recomputed), the pointwise counterexample and the four Babai certificates hold and match the artifact.

## Claims

### 1. holds

> cut claims of a SUPERPOLYNOMIAL quantum-search separation at constant full-RS interval width

- Step: Decision And Next Scientific Question
- Finding: A separation needs an efficient quantum algorithm with a guarantee, and every guarantee the note cites lies inside d<L at constant L: Chailloux-Tillich needs d/p<C with C<=L/p for any complex profile, and Sun-Wootters needs rate+density>1, i.e. (1-d/p)+L/p>1, so d<L (and applies only at fixed rates). There the O(N*L*d*p^d) DP is polynomial. Outside d<L the DP costs p^d, but none of the guarantees the note cites applies there (both need d<L), so the cut removes only separation claims the note has no basis for. Carrying 'certified' over from the body would be wording only.
- Conceded by the note's own self-check: no

### 2. holds

> For ANY complex a supported on L elements, Cauchy gives |f(e)|^2<=L/p

- Step: Problem, Mechanism And Ceiling
- Finding: |f(e)|^2<=(sum|a|)^2/p<=L/p, and C<=max|f|^2*sum|f|^2<=L/p, so d/p<C implies rate+density>1. This agrees with the artifact's ceiling 3/5 at p5.
- Conceded by the note's own self-check: no

### 3. holds

> Consequently ANY amplitude tuning changes the real KV codimension cutoff by a factor LESS than3/2 over that simple profile

- Step: Problem, Mechanism And Ceiling
- Finding: Without wraparound, C_uniform=(2L^2+1)/(3pL)>2L/(3p), so (L/p)/C_uniform<3/2. Recomputed 451/1395 at p31,u7 and 19/45 at p5,u1, matching the artifact.
- Conceded by the note's own self-check: no

### 4. holds

> valid probability.722780 and squared fidelity.719020 are BOTH below P_dec=.770203

- Step: Actual Finite Quantum Receiver
- Finding: The artifact's d2 (4,5,4) receiver has worst_fixed_target_conditional_valid_probability 0.7227800 and decoder_success_probability 0.7702026. The one-attempt average .6146>=P_dec^2=.5932, so the counterexample is correctly confined to pointwise use.
- Conceded by the note's own self-check: no

### 5. holds

> Thus the ENTIRE certified constant-width full-RS SEARCH window has a polynomial classical uniform coset sampler

- Step: Classical Baselines And Stronger Certificates
- Finding: d/p<C<=L/p forces d<L, so for constant L the O(N*L*d*p^d) DP is polynomial in N=p. 'Certified' correctly restricts to the KV sufficient window.
- Conceded by the note's own self-check: no

### 6. holds

> The first four are finite all-syndrome classical certificates, not just selected witnesses

- Step: Classical Baselines And Stronger Certificates
- Finding: Babai residuals have GS coordinates in [-1/2,1/2], so the norm bounds hold for every target. The integer bounds 6/5/14/7 are at most u=7/5/15/7, and the p127 bounds 63>31 and 12>11 are correctly reported as inconclusive.
- Conceded by the note's own self-check: no
