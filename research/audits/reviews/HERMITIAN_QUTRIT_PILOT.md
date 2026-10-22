# Referee review: HERMITIAN_QUTRIT_PILOT

Note: `research/HERMITIAN_QUTRIT_PILOT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note sound and agreed on every claim, so there was no disagreement to resolve. I re-checked the load-bearing identities numerically for m=4, c=[2,3,5,7]: A^3=503*I, the H^2|0> coefficient matrix at cut 2 has rank 4 while A^2|0> has rank 3, and the minor on rows/columns (0,1,3,6) equals -4200-8400*omega. I also checked E_r|0>=|r> for all 81 labels, and a random entangled pilot gives identical input and output energies (2.6475836 both). The commutation phases follow from U_l U_j=omega U_j U_l for l>j, and Result 4 is scoped to energy estimation under constructibility and controlled-precision premises.

## Claims

### 1. holds

> the one-directional relation gives A^3=(sum c_j^3)I

- Step: Result 1
- Finding: Numerically A^3=503*I for c=[2,3,5,7] (8+27+125+343), matching the artifact.
- Conceded by the note's own self-check: no

### 2. holds

> minor with EXACT determinant -4200-8400*omega, nonzero in Z[omega]

- Step: Result 1
- Finding: H^2|0> reshaped 9x9 at cut 2 has rank 4, its (0,1,3,6) minor is -7274.61i = -4200-8400*omega, and the one-directional A^2|0> has rank 3.
- Conceded by the note's own self-check: no

### 3. holds

> no generator is uniform against all remaining predecessors

- Step: Result 1
- Finding: U_j commutes with U_j^dagger but omega-commutes with every other U_k, and U_k, U_k^dagger carry opposite phases, so for m>=2 no generator can be last.
- Conceded by the note's own self-check: no

### 4. holds

> Thus for ANY normalized pilot, input and output have identical energy expectations

- Step: Result 3
- Finding: With M=sum psi_r E_r, <psi|H|psi>=Tr(M^dagger H M)/Tr(M^dagger M); a random entangled 4-qutrit pilot gives equal values to 1e-15.
- Conceded by the note's own self-check: no

### 5. holds

> It uses m(m-1)/2+2m ideal logical qutrit Clifford gates

- Step: Result 2
- Finding: m(m-1)/2 label SUMs plus m Fourier and m SUM gates; the artifact records 5 for m=2 and 9 for m=3.
- Conceded by the note's own self-check: no

### 6. holds

> bond controlled-precision pilot cannot support an ENERGY-estimation separation here

- Step: Result 4
- Finding: Follows from the intertwiner identity and classical MPS contraction; the premises and the restriction to energy estimation are stated, and the optimum energy is explicitly not claimed easy.
- Conceded by the note's own self-check: no
