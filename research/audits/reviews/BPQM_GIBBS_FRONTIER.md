# Referee review: BPQM_GIBBS_FRONTIER

Note: `research/BPQM_GIBBS_FRONTIER.md`. Reviewed 2026-11-14 by claude-subagent-refresh-2026-11-14. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The local mathematics checks: the heralded parity mean overlap is exactly E[max(a,b)] <= E[a]+E[b], recursion (1) with A=c(dc-1)^(dv-1) and the doubly exponential iterate (2) close, the Hoeffding bound exp(-184.32) <= 2^-184 is valid (loose), and the affine-cluster joint weight gives the Gibbs odds (1+c)/(1-c) and p=2c/(1+c). Artifact numbers match (c=13/20 level 12: F_upper 0.023552, A*F 0.382727; c=1/2 at level 4; c=4/5 UNKNOWN after 24 levels; U_12 = 1,111,111,111,111). Both judges flagged the portfolio sentence for calling the test 'rigorous' and the decoder 'specified' while the degradation argument is review pending, only c=13/20 is certified beyond the ceiling, and no decoder is implemented; I confirm it. Only judge A flagged the missing bridge from the finite tree certificate to the hypothesis of Mandal et al. Theorem 30; I keep it as a gap because the note never states that hypothesis or checks the extrinsic-tree certificate against it, but mark it covered by the self-check (failure mode 1). The judges otherwise agree, and nothing is shown wrong.

## Claims

### 1. holds

> It supplies a specified decoder family, public input, rigorous local test and known sampling reduction (where the degradation enclosure is review pending, the extrinsic-tree contraction is certified beyond the rank ceiling only at `(d_v,d_c)=(3,6), c=13/20, G=128` while `c=4/5` is `UNKNOWN`, and the complete coherent block decoder is not implemented)

- Step: Scientific Question and Portfolio Decision
- Finding: The summary now explicitly states the review-pending degradation enclosure, the single certified beyond-rank point (dv,dc)=(3,6), c=13/20, G=128 (with c=4/5 UNKNOWN), and that the complete coherent block decoder is not implemented.
- Conceded by the note's own self-check: yes

### 2. holds

> verifying whether the extrinsic-tree mean-overlap certificate here satisfies every hypothesis of Mandal et al. Theorem 30 and Zhou et al. Theorem 2.4 remains an unverified external-theorem bridge

- Step: Problem and Known Mechanism / Exact Binary Tree Calculation
- Finding: Problem and Known Mechanism now explicitly records that connecting the extrinsic-tree mean-overlap certificate to every hypothesis of Mandal et al. Theorem 30 and Zhou et al. Theorem 2.4 remains an unverified external-theorem bridge.
- Conceded by the note's own self-check: yes

### 3. holds

> the parity output's mean absolute overlap is E[max(a,b)] <= E[a]+E[b]

- Step: Exact Binary Tree Calculation
- Finding: p+c+ + p-|c-| = (a+b)/2 + |a-b|/2 = max(a,b) <= a+b for a,b >= 0; equality multiplies independent means, giving F_(l+1) <= c((dc-1)F_l)^(dv-1) = A F_l^p. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> then induction gives for every r>=0

- Step: Exact Binary Tree Calculation, eq. (2)
- Finding: r=1: A f^p = f*lambda; step A(f lambda^s)^p = f lambda^(1+ps) with 1+p(p^r-1)/(p-1) = (p^(r+1)-1)/(p-1). Helstrom error (1-sqrt(1-a^2))/2 <= a/2 supports 'at most F/2'. Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> Hence the sufficient tree condition holds beyond the product-USD/Prange rank ceiling c=dv/dc=1/2

- Step: Executed Result and Full Resource Warning
- Finding: Artifact frontier c=13/20, level 12: mean_overlap_upper = 0.023552, sufficient_contraction_factor_upper = 0.382727 < 1 (A=16.25), status SUFFICIENT_TREE_CONVERGENCE_CERTIFICATE_REVIEW_PENDING. It is a tree condition at one c, conditional on the review-pending degradation enclosure stated just above. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> Summing over S yields a factor ((1+c)/(1-c)) per satisfied constraint, exactly the Gibbs odds

- Step: Classical Competitors That Must Not Be Omitted
- Finding: 1 + 2c/(1-c) = (1+c)/(1-c) = e^(2beta) for c=tanh(beta); the retention conditional is 2c/(1+c) = p, and sum_S W(S)W(x|S)W(y|S) is symmetric. Both judges agree.
- Conceded by the note's own self-check: no
