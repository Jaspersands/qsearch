# Referee review: INTERVAL_SOFT_DECODER

Note: `research/INTERVAL_SOFT_DECODER.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Judge A's one gap is in the decision, which cuts superpolynomial separation claims 'at constant full-RS interval width' without the d<L / KV-certified window that the body keeps. I confirmed it, since at constant L with codimension outside that window the DP costs p^d; Judge B instead flagged the title and the receiver table (5 of 8 controls shown); I drop both. The title's 'Actual Receiver' and 'Classical Falsifiers' are accurate names for the executed p=5 receiver and the DP/Babai baselines. The eight-control sentence lists all eight, and the omitted complex and S={0} controls are discussed under 'Decisive controls', with no conclusion resting on the table. The Cauchy ceiling, the 3/2 tuning bound (451/1395, 19/45 recomputed), the pointwise counterexample and the four Babai certificates hold and match the artifact.

## Claims

### 1. gap

> cut claims of a SUPERPOLYNOMIAL quantum-search separation at constant full-RS interval width

- Step: Decision And Next Scientific Question
- Finding: The classical argument behind this cut covers only the KV-certified window d/p<C<=L/p, which forces d<L. At constant L with growing codimension outside that window, the DP costs O(N*L*d*p^d) and is not polynomial, and the body says 'No such conclusion is drawn for growing L or d'. The decision sentence drops that restriction.
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
