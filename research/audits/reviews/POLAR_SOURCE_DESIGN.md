# Referee review: POLAR_SOURCE_DESIGN

Note: `research/POLAR_SOURCE_DESIGN.md`. Reviewed 2026-10-22 by claude-opus-5.5-subagent-2026-10-21-calibration-r2-judge-d. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The recursion, the PSC-degradation argument for rounding up overlaps, and the TV=sum_F m_i accounting are consistent. The artifact's TV bounds equal the sums of the retained per-coordinate upper bounds over the smallest-mean sets. The reported numbers match the artifacts: 16/78/361/1614, the 3/8 follow-up at 0.0234306, and N32768 at 0.0102208 with 65534 combinations and 1,008,335,816 visits. The headline and the half-rate sentence present a single certified length (N32768 on one grid) as a family construction. Half-rate fails at every coarse length N<=4096, and the certificate rests on review-pending degradation/hybrid derivations. The outcomes table also drops the N16 row that the artifact reports.

## Claims

### 1. holds

> The preceding hybrid argument gives average uniform-sign Gibbs TV at most

- Step: The Direct Decoder-Sampler Link
- Finding: Consistent with the hybrid in POLAR_CONDITIONAL_SAMPLER: epsilon_F there is sum|P-1/2|=(1/2)sum m_i, and the average conditional TV is <=2 epsilon_F. Artifact check: uniform_sign_average_Gibbs_TV_upper equals the sum of all_source_mean_absolute_bias_upper over the frozen set (=2x frozen_prefix_bias_sum_upper), e.g. N32768.
- Conceded by the note's own self-check: no

### 2. holds

> Product and averaged channel combinations preserve this order, and root fidelity cannot decrease under degradation

- Step: Certified Finite Construction
- Finding: The Gram identity <psi_0(d)|psi_1(d)>*<psi_0(a/d)|psi_1(a/d)>=a gives the isometry. Discarding the environment degrades the channel, and any degrading map on one input system commutes with the BPQM combinations. Fidelity is monotone under CPTP maps, so rounded-up overlaps upper-bound m_i. The derivation is stated as review pending.
- Conceded by the note's own self-check: no

### 3. gap

> Largest set certified at average TV<=0.1

- Step: Live Outcomes table
- Finding: The rows shown match the artifact (16/64, 78/256=0.304688, 361/1024=0.352539, 1614/4096=0.394043, with TV uppers 0.0826, 0.0935, 0.0998, 0.0995). However, the artifact also has an N16 instance (max 2 constraints, rate 1/8, TV upper 0.0599) that the table omits, so the table is not 'all coarse controls'.
- Conceded by the note's own self-check: no

### 4. gap

> This finite result removes the missing public-set construction premise for the stated half-rate family

- Step: Live Outcomes, N32768 paragraph
- Finding: Only one half-rate length is certified (N32768, G256, r3: 0.0102208<0.010221, matching the artifact). Every coarse half-rate target at N16..4096 is UNKNOWN, and no other length or grid is certified at half rate, so no family over N is constructed. The bound also depends on the review-pending degradation/hybrid derivations. The next sentence concedes that there is no fixed-grid asymptotic theorem.
- Conceded by the note's own self-check: yes

### 5. gap

> This pass removes that blocker for concrete non-prefix families

- Step: Question And Decision (headline)
- Finding: The headline drops conditions stated elsewhere. The guarantee is average over uniform signs only, and the certified instances are finite: rates up to 1614/4096 at TV<=0.1, the post-exploration 3/8 at N4096, and half rate only at N32768. The certificates rest on review-pending degradation/duality derivations. 'Families' is not established by these finite certificates.
- Conceded by the note's own self-check: no

### 6. holds

> rate3/8 follow-up at N4096 has certified average TV<=0.023431

- Step: Live Outcomes
- Finding: Artifact explicit_three_eighths_rate_followup: 1536 constraints, 2560 spins, TV upper 0.0234306<=0.023431, rate_chosen_after_exploratory_bound_budget flagged. 3/8=0.375>1-c=0.35 as stated. The TV equals the sum of the N4096 per-coordinate upper bounds over the listed frozen set.
- Conceded by the note's own self-check: no
