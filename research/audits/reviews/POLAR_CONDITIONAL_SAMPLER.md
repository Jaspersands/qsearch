# Referee review: POLAR_CONDITIONAL_SAMPLER

Note: `research/POLAR_CONDITIONAL_SAMPLER.md`. Reviewed 2026-10-22 by claude-opus-5.5-subagent-2026-10-21-calibration-r2-judge-d. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The reverse-order hybrid, the triangle inequalities to 2 epsilon_F, prefix exactness and the source/CQ index-reversal identity check out. The calibration table matches the artifact, and I hand-verified the N2 row (0.08/0.72 conditional TVs, epsilon_F=2/5). I also recomputed that {0,1,2,4} are the four smallest exact prefix biases at N8 under the G^T convention. The weak point is the follow-up header. It says the design note 'resolves' this note's public-set premise, but that premise (epsilon_F->0 with a polynomial construction) is asymptotic, and the design note certifies one half-rate length on review-pending derivations, which the header omits.

## Claims

### 1. holds

> Thus TV(P_U,Qjoint)<=epsilon_F

- Step: Average-Syndrome Guarantee
- Finding: Standard hybrid: replacing each frozen conditional by a fair bit costs E|P(U_i=1|prefix)-1/2| in TV, summed over F. N2 check: epsilon_F=0.82*(1/2-0.01/0.82)+0.18*0=2/5, matching frozen_prefix_bias_sum in the artifact.
- Conceded by the note's own self-check: no

### 2. holds

> is at most that joint discrepancy. Triangle inequalities then give BOTH

- Step: Average-Syndrome Guarantee
- Finding: sum_s Q(s)TV(Q_s,P_s)<=TV(Qjoint,P)+TV(Q_F,P_F)<=epsilon_F+delta, and the same holds with P(s) weights. Full-rank H_F makes uniform J give uniform s. Artifact N2: uniform average 0.4 and native 0.144 are both <=2 epsilon_F=0.8.
- Conceded by the note's own self-check: no

### 3. holds

> For a contiguous initial frozen prefix, however, the remaining chain is already conditioned on every constraint

- Step: Implemented Classical Algorithm
- Finding: Correct, since all constraints precede the sampled coordinates. The artifact rows N4{0,1} and N8{0,1,2} have zero TV for all syndromes.
- Conceded by the note's own self-check: no

### 4. holds

> The last set selects the four smallest EXACT source prefix biases

- Step: Native Results And Falsifiers
- Finding: Recomputed exact prefix biases at N8, p=7/40 with U=G^T E: m=(0.0319,0.1785,0.1785,0.596,0.1785,0.6313,0.7017,0.9581), so {0,1,2,4} is the smallest-4 set. Its half-sum 0.28369 matches 14525010721/51200000000. The table values 0.00416611/0.05596208 match the artifact.
- Conceded by the note's own self-check: no

### 5. holds

> Hence the CQ information at i equals the source conditional entropy at N-1-i

- Step: Why This Is Relevant To The Quantum Proposal
- Finding: For F=[[1,0],[1,1]], F^T=RFR, which extends to tensor powers. The artifact N2/N4 lists are exact reversals (e.g. N4 Holevo [0.2400,0.7018,0.7573,0.9769] vs entropies [0.9769,0.7573,0.7018,0.2400]), with errors ~1e-16. Numerics, as conceded.
- Conceded by the note's own self-check: no

### 6. gap

> It resolves the missing public-set premise below for that finite family

- Step: Header FOLLOW-UP
- Finding: This note's premise is 'epsilon_F->0 with a polynomial construction' for a code family. The follow-up certifies a single half-rate length (N32768) at fixed TV 0.0102; half-rate is UNKNOWN at every coarse N<=4096, so no epsilon_F->0 sequence is given. The header also drops that the certificate rests on POLAR_SOURCE_DESIGN's review-pending degradation/duality derivations.
- Conceded by the note's own self-check: no
