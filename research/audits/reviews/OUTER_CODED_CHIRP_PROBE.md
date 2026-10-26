# Referee review: OUTER_CODED_CHIRP_PROBE

Note: `research/OUTER_CODED_CHIRP_PROBE.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The formal-square-root completion holds: I recomputed it for every target at p=5,7,11 and a sample at p=13 for all 1<=r<N/2 with no failure, and only r=N/2 targets fail, including the stated p7,N6,r3,b=(0,0,1) countercontrol. Both judges flagged the 3.34e-16 summary number, and I confirmed it: the artifact's p=11 actual_diagonal_probability_max_error is 4.44e-16. The judges disagreed on the decision sentence 'solves EVERY target ... and beyond' (A holds, B gap). I side with B, because that sentence gives no upper limit on the rate and no review-pending status, while the method provably fails at r=N/2. The dense-puncturing extension and the average coherent-erasure identity hold and match the artifact.

## Claims

### 1. gap

> a deterministic classical construction below solves EVERY target in the entire proposed useful rate range, and beyond

- Step: Scientific Question And Portfolio Decision
- Finding: The algebra behind it holds, but the decision sentence states no limit for 'and beyond'. The construction is proved only for full support N=p-1 with 1<=r<N/2 strictly, and it fails at r=N/2: the note's own p7,N6,r3,b=(0,0,1) countercontrol fails, and so does every failing target in my replay. The sentence also omits that the derivation is review pending and that the task is zero-allowed search, not nonzero-coordinate search or weighted sampling.
- Conceded by the note's own self-check: no

### 2. gap

> Local physical unitarity error is at most2.23e-16 and predicted probability error at most3.34e-16

- Step: Costs, Tests And Research Decision
- Finding: The artifact's local_physical_controls give actual_diagonal_probability_max_error=4.440892e-16 at p=11 (3.33e-16 at p=7), above the stated 3.34e-16 ceiling, and normalized_output_max_error reaches 6.66e-16 at p=7. The unitarity bound 2.22e-16 holds for p=5,7,11,13. The difference is at machine precision and does not affect the conclusion, but the stated maximum does not match the saved report.
- Conceded by the note's own self-check: no

### 3. holds

> The strict inequality r<N/2 ensures N-r+1>d, so no prescribed coefficient is touched

- Step: Deterministic Classical Completion For EVERY Target
- Finding: N-r+1>N/2+1 iff r<N/2. Removing R0(0) changes R^2 by degree <=d. deg(X^k R^2)=k+N+2<2N for k<r<N/2, so the only alias exponents are 0 and N. I replayed the construction for all targets at p=5,7,11 and sampled targets at p=13: 0 failures for r<N/2, and failures appear only at r=N/2.
- Conceded by the note's own self-check: no

### 4. holds

> p7,N6,r3,b=(0,0,1), F=X^8-X^4 is an explicit countercontrol

- Step: Deterministic Classical Completion For EVERY Target
- Finding: R0=X^4-1/2 and R=X^4, so [X^4]R^2=0, not -1. My replay confirms that this target fails the original equations, so the strict rank guard is necessary for this construction.
- Conceded by the note's own self-check: no

### 5. holds

> Now deg(R^2-F)<=d+M<N-r+1 by exactly the stated strict inequality

- Step: Dense Puncturing Does Not Automatically Rescue It
- Finding: d+M<N-r+1 is equivalent to r<L-N/2. With r>=1 the gate gives deg W=M+1<=d, so R stays monic of degree d. The artifact's punctured records (100,24) at p127 and (800,190) at p1021 satisfy the gate and save omitted points as forced zeros.
- Conceded by the note's own self-check: no

### 6. holds

> P_b[zero residual label]=q, for every Fourier target b

- Step: Average Identity, Not A Worst-Target Theorem
- Finding: |alpha_b|^2=1/M is independent of b, so the identity is pointwise in b, and Fourier orthonormality gives a mean squared error of 2(1-q). The values 1.161221, 1.101202 and 0.344470 equal 2(1-q) for the artifact's q values. The note scopes this as a mean identity, and the 17-dimensional rotation counterexample (62/289, 1/227) matches the artifact.
- Conceded by the note's own self-check: no
