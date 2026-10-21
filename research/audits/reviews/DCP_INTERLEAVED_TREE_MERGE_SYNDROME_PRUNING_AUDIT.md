# Referee review: DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT

Note: `research/DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agreed that P_acc=1-2p+3p^2/2, the visibility-gain factorisation, the telescoping 2^L-moment survival and SNR<=survival<=1 hold. I rechecked them and found agreement with the unreferenced producer artifact research/phase_workbench/dcp_interleaved_tree_merge_syndrome_pruning_audit.json (survival 19/32, 649/2048 at q8,p1/4). Both judges flagged the Theorem 1 'Purification Threshold' heading and 'strictly purifies the phase error' bullet as dropping the conditional-classical-access scope, conceded in the status block. I confirmed it as a gap: the algebra is right, but Section 3 says these are not channels on phase qubits. The judges differed only on side remarks: A said no artifact backs the diagnostics, while one exists but is not named in the note, and neither raised a claim on it, so I added none.

## Claims

### 1. gap

> coincidence pruning strictly purifies the phase error

- Step: Theorem 1 heading and item 2, first bullet
- Finding: The sign statement is algebraically correct: the numerator p(1-p)(2-3p)(1-cos(2pi/q))/2 is positive for 0<p<2/3. It is, however, a statement about the conditional posterior of classical latent errors under assumed exact equality access. The status block says no phase-qubit equality instrument exists and that this is not quantum purification, and Section 3 says these are not a derived error channel on phase qubits. Calling p*=2/3 a 'Purification Threshold' and the result purification of 'the phase error' drops that condition from the theorem statement.
- Conceded by the note's own self-check: yes

### 2. holds

> Post-selecting two independent copies $e_1, e_2 \stackrel{\text{i.i.d.}}{\sim} K_\eta$ on exact coincidence $e_1 = e_2$ succeeds with probability

- Step: Theorem 1, item 1
- Finding: For q>=3 the points +1 and -1 are distinct, so sum K^2=(1-p)^2+2(p/2)^2=1-2p+3p^2/2. The gain (1-c)p(P-p/2)/P with P-p/2=(1-p)(2-3p)/2 reproduces item 2. At p=1/4 this gives 19/32, matching the producer artifact. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Conditional coincidence probability is the squared-weight sum, updating the retained-error posterior

- Step: Theorem 2
- Finding: Given that earlier checks succeeded, the two subtrees are independent with law K^(l-1), so P_acc^(l)=sum K^(l-1)(e)^2, and by induction K^(L) is proportional to K_eta^(2^L). Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> The joint probability that all $2^L - 1$ internal binary coincidence checks across layers

- Step: Theorem 2 proof
- Finding: P_acc^(l)=S_{2^l}/S_{2^(l-1)}^2, and each intermediate S cancels with matching exponents, leaving S_{2^L}/S_1^(2^L)=sum K_eta(e)^(2^L). The artifact's moment and telescoping survivals agree exactly (19/32, 649/2048, ...). Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> The useful content is the classical posterior identity, its telescoping probability and the proxy bound SNR<=survival<=1

- Step: Theorem 3
- Finding: |lambda_1^(L)|<=1 as a convex average of cosines, so SNR=P_surv*lambda^2<=P_surv=S_{2^L}<=S_1=1. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> At q3,p2/3 the kernel is uniform, both visibilities and both proxies are EXACTLY zero at every depth

- Step: Theorem 3 discussion
- Finding: On Z_3 the support {-1,0,1} is the whole group, so K=1/3 everywhere, every power stays uniform, and sum cos(2pi e/3)=0. Both judges agree.
- Conceded by the note's own self-check: no
