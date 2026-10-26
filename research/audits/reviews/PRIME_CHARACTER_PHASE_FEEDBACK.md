# Referee review: PRIME_CHARACTER_PHASE_FEEDBACK

Note: `research/PRIME_CHARACTER_PHASE_FEEDBACK.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges found one headline-scope gap, but in different places: A in the decision's 'What survived' sentence, B in the title's 'Physical Rescue'. I keep A's gap. That sentence presents the restoration as 'verified on full native states and locally bounded' without saying that full-state verification exists only at p7/11,N4,K2,ell1, and that the N127 bound is an analytic certificate assuming exact native-state reflections. I drop B's title gap as a separate finding: the title pairs the rescue with 'Exponential Construction', the status line directly states review pending, and the scope omission is already recorded through the decision sentence. The trace-distance bound, the reflection-count lower bound (recomputed as 408774727362072591332623950512), the Chebyshev mask bound and the 3.726e-9 certificate all hold and match the artifact.

## Claims

### 1. gap

> There is a concrete interference-restoring action, verified on full native states and locally bounded without selecting fortunate outcomes

- Step: Adversarial Decision And Next Experiment
- Finding: Full native-state verification exists only for the four two-row controls at p7/11, N4, K2, ell1, plus one three-row test. At N127, K39, ell32 the restoration is an analytic certificate that 'additionally assumes exact native-state reflections' and rests on frame/rank/feedback proofs awaiting review. The sentence merges the two scopes and names neither the certified instances nor the exact-reflection assumption.
- Conceded by the note's own self-check: no

### 2. holds

> the normalized corrected branch has trace distance at most

- Step: Why Feedback Can Restore The State
- Finding: Multipliers lie in [B^-1/2,B^1/2], giving F^2>=4B/(1+B)^2 and trace distance (B-1)/(B+1). With R=(p+1)/(p-1), I recomputed 1/7 at p7 and 1/11 at p11, matching the artifact, and the large values 5.552e-17/9.715e-17 also match.
- Conceded by the note's own self-check: no

### 3. holds

> Every nonzero mask needs at least408774727362072591332623950512 reflections

- Step: Executed Results
- Finding: Recomputed sum_(j<32)C(126,j)=408774727362072591332623950512 and 127 times that =51914390374983219099243241715024, matching the artifact. The pairing argument is correct, and the note limits the count to this factorization.
- Conceded by the note's own self-check: no

### 4. holds

> Chebyshev gives Pr[z=0]<=(1-nu)/(N*nu), WITHOUT a full-binomial assumption

- Step: A Real Phase Action, Not A Free Oracle
- Finding: The indicators are pairwise independent for K>=2. With nu about 1/2 the bound gives 1-1/127=0.99212598, which matches the artifact's nonzero-mask lower bound and expected calls >4.0555e29.
- Conceded by the note's own self-check: no

### 5. holds

> Distance to the original native single-copy state <=3.726e-9, including

- Step: Executed Results
- Finding: sqrt(32/(2^61-2))=3.7253e-9, matching corrected_vs_original_single_copy_TV_upper. The rank-herald term dominates, as stated. The mean .90285 and tail .31458 are explicitly conditional on transferring the previous proof.
- Conceded by the note's own self-check: no
