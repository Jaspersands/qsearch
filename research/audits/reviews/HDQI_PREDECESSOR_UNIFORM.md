# Referee review: HDQI_PREDECESSOR_UNIFORM

Note: `research/HDQI_PREDECESSOR_UNIFORM.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note sound with identical holds on the radius recurrence, the symmetric spectrum, the outward-rounding width bound, the recursive ground circuit and the dependence counterexample, so there was no disagreement. I re-derived fact 1 (P_j times any product of earlier labels is a nonidentity, traceless Pauli) and fact 2 (an all-anticommuting Q exists by full row rank). The commuting and anticommuting radius updates and the lower-eigenvector angle also check out. The artifact's 512-term certificate has width 165/2^79=330*2^-80 against 341 anticommuting root steps, within the stated bound. ZZI+IZZ+ZIZ has minimum -1, and the falsifier is scoped to ground energy only.

## Claims

### 1. holds

> Each eigenspace of H_(j-1) therefore has equal +1/-1 multiplicities for P_j

- Step: Local Radius Derivation, fact 1
- Finding: Spectral projectors of H_(j-1) are polynomials in earlier labels; independence makes P_j times each product a nonidentity Pauli, so P_j is a traceless involution on each eigenspace.
- Conceded by the note's own self-check: no

### 2. holds

> Thus every H_j has a spectrum symmetric about zero

- Step: Local Radius Derivation, fact 2
- Finding: The symplectic map to syndromes is surjective for independent labels, so a Q with all-one syndrome exists and QHQ=-H; hence E_min=-R_m.
- Conceded by the note's own self-check: no

### 3. holds

> R_j = sqrt(R_(j-1)^2 + c_j^2)

- Step: Local Radius Derivation
- Finding: Anticommutation with all predecessors cancels the cross terms, giving H_j^2=H_(j-1)^2+c_j^2 I.
- Conceded by the note's own self-check: no

### 4. holds

> so interval width is at most (number of root steps)*2^(-b)

- Step: Local Radius Derivation
- Finding: Commuting additions shift both endpoints equally and keep the width a grid multiple; each 1-Lipschitz outward-rounded root adds at most one grid step. Artifact: width 165/2^79=330*2^-80 with 341 root steps.
- Conceded by the note's own self-check: no

### 5. holds

> applies exp(-i theta Z_<j Y_j/2), theta=-atan2(c_j,R_(j-1))

- Step: Constructive Native Ground-State Check
- Finding: On the block [[-R,c],[c,R]], tan(theta/2)=-c/(R+sqrt(R^2+c^2)) gives the lower eigenvector.
- Conceded by the note's own self-check: no

### 6. holds

> Dependence matters: ZZI+IZZ+ZIZ has ground energy-1, not-3

- Step: Evidence And Scope Falsifiers
- Finding: The product of the three Ising terms is the identity, so they cannot all be -1; the minimum is -1 and the labels sum to zero.
- Conceded by the note's own self-check: no
