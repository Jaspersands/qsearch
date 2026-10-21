# Referee review: AFFINE_CLUSTER_NATIVE_PROBE

Note: `research/AFFINE_CLUSTER_NATIVE_PROBE.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The nullspace identities (1)-(4), the Dirichlet-form identity (5) with its Rayleigh upper bound on the gap, and the heat-bath and swap rules (6)-(7) all check, as does the 16-spin equality-chain countercontrol. The artifact matches every quoted number I checked: worst-start TV 0.0110235 (seed 29) and 0.105855 (seed 71), scores 46.14/39.93 to 45.50/44.58, exact spin0 mean -0.5507664, bucket 19, peak 524,288 entries, 4096 swap proposals and 12,764 bits. The two judges agreed on every claim, including the single gap: the decision says the BPQM tree certificate 'survives' although no experiment here tests it, and the sentence drops that the certificate is a review-pending tree condition certified only at c=13/20. I confirm that gap and find nothing wrong.

## Claims

### 1. gap

> The BPQM tree certificate survives, but a classical separation is STILL UNESTABLISHED

- Step: Decision and Remaining Falsifiers
- Finding: Headline scope (both judges). Every experiment in this note is a classical sampler or exact contraction on finite graphs; none tests the tree certificate, so 'survives' reports no evidence. The decision also drops the certificate's conditions from BPQM_GIBBS_FRONTIER: a review-pending degradation argument, an extrinsic-tree condition only, a single certified point c=13/20, and no finite-graph decoder.
- Conceded by the note's own self-check: no

### 2. holds

> Consequently, with r=rank(B_S), Pr(y=x | S) = 2^(r-n

- Step: Exact Nullspace Instrument, (1)-(4)
- Finding: y = x XOR z with z uniform on ker(B_S) of size 2^(n-r), so Pr(y=x|S) = 2^(r-n); E[chi_a(z)] = 1[a in rowspace], and in RREF e_v is in the rowspace iff it is a row, giving (4). The countercontrol (rank 15, nullspace {0,1^16}) gives hold 1/2 and jump 8. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Dividing (5) by that variance gives an UPPER bound on the spectral gap by the variational principle

- Step: Exact Finite Spectral and TV Controls
- Finding: K chi_a(x) = chi_a(x) Pr_S(a in rowspace(B_S) | x), so <chi_a,(I-K)chi_a>_pi is (5); K is reversible, so the Rayleigh quotient upper-bounds the gap and does not certify mixing, as stated. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> After16 updates it is about0.01102 for seed29 and0.10586 for seed71

- Step: Exact Finite Spectral and TV Controls
- Finding: Artifact worst_start_TV_exact at 16 steps: 0.0110235 (seed 29) and 0.1058554 (seed 71). Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> For replica scores T_i,T_j, exchanging configurations is accepted with

- Step: Try Harder Before Interpreting a Slow Trace, (6)-(7)
- Finding: Flip ratio r^(d-2s) with d counted after mod-2 cancellation; swap ratio (r_i/r_j)^((T_j-T_i)/2) with even score differences. Work 1024*5*32 = 163,840 spin and 1024*4 = 4096 swap proposals match the artifact. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> The first cluster and tempering traces agree closely WITH EACH OTHER while both disagree with the exact reference

- Step: A More Decisive Classical Reference
- Finding: Zero-start cluster -0.75684 and tempering -0.75521 against exact -0.5507664; the all-one starts (-0.49170, -0.52344) are also reported, and the note calls these autocorrelated means rather than proved biases. Both judges agree.
- Conceded by the note's own self-check: no
