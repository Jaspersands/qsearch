# Referee review: PRIME_CHARACTER_INTERLEAVED_PROBE

Note: `research/PRIME_CHARACTER_INTERLEAVED_PROBE.md`. Reviewed 2026-11-14 by codex-audit-correction-2026-10-23-r3. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Each judge found one scope gap the other missed: A in the Result's 'each original polynomial is nearly uniformly distributed', B in the title. I keep both. Near-uniformity is shown only at the p=2^61-1, N127 instance under a review-pending, rank-heralded bound, while the executed p7/11 controls have only the density-error bounds 1/6 and 1/10 (their individual means, .553571 and .534091, do fall to near the uniform 4/7 and 6/11). The title attributes the failure to 'A Fast Interleaved Decoder', but the note shows that the decoder works, that only the separate-readout/original-row receiver fails at one parameter set, and that 'Do NOT infer that all interleaved sources or joint quantum processing fail'. The decoder argument, the Schwartz-Zippel rank bound and the best-of-rows tail hold; I recomputed the order-38 tail as 4.8521e-14, which with the union bound gives 1.863e-8 and 2.981e-8.

## Claims

### 1. holds

> Interleaved Separate-Readout DQI Probe: Working Classical Decoder, Failed Separate-Row Quantum Readout At N=127, K=39

- Step: Title
- Finding: The title now distinguishes the working classical collaborative decoder from the failed separate-row quantum readout at N=127, K=39.
- Conceded by the note's own self-check: no

### 2. holds

> The joint product correlation is enhanced, but at `p=2^61-1, N=127, K=39, ell=32` under the review-pending rank-heralded bound each original polynomial is nearly uniformly distributed (row TV `<= 3.726e-9`, while the small `p=7, 11` controls have density-error bounds `1/6` and `1/10`)

- Step: Candidate And Decision
- Finding: Candidate And Decision now scopes near-uniformity to p=2^61-1, N=127, K=39, ell=32 under the review-pending rank-heralded bound (row TV <= 3.726e-9) and discloses the 1/6 and 1/10 density-error bounds on the p=7, 11 controls.
- Conceded by the note's own self-check: no

### 3. holds

> four rows give only28 equations, five give35

- Step: Actual Syndrome-Only Decoder
- Finding: c(K-ell)=7c gives 28 and 35, and at least 32 equations are needed. The artifact shows rank 32 (VERIFIED) for 5 and 8 independent rows, rank 14 for two rows, and rank 7 for identical rows.
- Conceded by the note's own self-check: no

### 4. holds

> The cap-rank check certifies uniqueness against the WHOLE burst ball

- Step: Actual Syndrome-Only Decoder
- Finding: Rank d makes the cap solutions the multiples of the degree-d locator. Every root is nonzero, so a competing locator is divisible by Lambda. Column independence of at most ell<K columns then forces e=e'.
- Conceded by the note's own self-check: no

### 5. holds

> Schwartz-Zippel on Fp* gives rank-failure probability at most

- Step: Local Fixed-Support Rank Guarantee
- Finding: The block-Vandermonde assignment gives a nonzero degree-j minor, so failure is at most j/(p-1)<=ell/(p-1), consistent with the artifact's 32/(p-1).
- Conceded by the note's own self-check: no

### 6. holds

> Best of five original rows: probability<=1.863e-8

- Step: Selecting The Best Row Does Not Repair It
- Finding: Recomputed the order-38 central moment bound for Bin(127,rho) at 110: 4.8521e-14. Then 5*(4.852e-14+3.7253e-9)=1.8627e-8 and 8 rows give 2.9803e-8, matching the artifact. No row independence is used.
- Conceded by the note's own self-check: no
