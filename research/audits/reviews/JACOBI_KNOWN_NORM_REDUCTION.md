# Referee review: JACOBI_KNOWN_NORM_REDUCTION

Note: `research/JACOBI_KNOWN_NORM_REDUCTION.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note needs-work on scope only: judge A flagged the bold Decision and judge B the title, and I kept both, since each headline states the classical algorithm or the removal without the status line's condition that the local application is review pending and without saying the Lenstra-Silverberg recovery was never executed. I dropped the part of both findings that ties the headline to the ell=poly(log p) promise, because the Decision says polynomial time in ell and log p, which is what the body proves. The judges agreed that the local steps hold, and I re-derived the conjugation identity I*bar(I)=p^2*A, the trace-Gram bound (Gram ell*I-11^T, eigenvalues ell and 1) and the index p^ell=|v(1)*N(J)|. The artifact records classical_known_norm_recovery_executed=false and independent_or_formal_review_completed=false for the 6 small and 51 large controls.

## Claims

### 1. gap

> Known Relative Norm Removes The Prime-Conductor Quantum Opening

- Step: Title
- Finding: The title states the removal unconditionally. The status line and Next Research Action make it 'subject to independent review of the application', and the Lenstra-Silverberg recovery algorithm was not executed (artifact: classical_known_norm_recovery_executed=false, independent_or_formal_review_completed=false).
- Conceded by the note's own self-check: yes

### 2. gap

> this published theorem plus the Jacobi identities and primary congruence gives classical polynomial-time exact surface counting

- Step: Question And Decision (bold Decision)
- Finding: Read alone, the Decision asserts the classical algorithm outright; it drops the note's own conditions that the local reduction to Theorem 1.3 is review pending and that the imported recovery algorithm was never run. Its complexity scope 'in ell and log p' matches the body, so no promise is missing there.
- Conceded by the note's own self-check: yes

### 3. holds

> Theorem 1.3, gives a deterministic classical polynomial-time decision AND recovery algorithm

- Step: Question And Decision
- Finding: Both judges checked the arXiv statement (CM-order, fractional ideal, totally positive w with I*bar(I)=Aw; decide and compute v; no GRH), and the artifact records the same input/output. I did not re-read the paper, so this rests on their agreement.
- Conceded by the note's own self-check: no

### 4. holds

> Since e_t+e_(-t)=2, we have I*bar(I)=product_t P_t^2=p^2*A

- Step: Direct Reduction To Theorem 1.3, step 3
- Finding: Conjugation maps the kernel of zeta->eta^t to that of zeta->eta^(-t), so I*bar(I)=prod P_t^(e_t+e_(-t)); p splits completely since ell|(p-1), so the product is p^2*A with w=p^2 totally positive.
- Conceded by the note's own self-check: no

### 5. holds

> The trace Gram's smallest eigenvalue is1, so each |a_j|<=sqrt(ell-1)*p

- Step: Direct Reduction To Theorem 1.3
- Finding: Tr(zeta^i zeta^-j) is ell-1 or -1, so the Gram is ell*I-11^T of size ell-1 with eigenvalues ell and 1 (determinant ell^(ell-2), as the note says); a^T G a=(ell-1)p^2 gives sum a^2<=(ell-1)p^2.
- Conceded by the note's own self-check: no

### 6. holds

> Its index is p^(sum e_t+1)=p^ell

- Step: Independent Group-Ring Check
- Finding: sum e_t=ell-1, and |v(1)*Norm_K(J)|=p*p^(ell-1)=p^ell, so containment plus equal index gives equality.
- Conceded by the note's own self-check: no
