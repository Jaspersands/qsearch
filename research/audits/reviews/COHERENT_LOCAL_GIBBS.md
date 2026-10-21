# Referee review: COHERENT_LOCAL_GIBBS

Note: `research/COHERENT_LOCAL_GIBBS.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges rated the note sound with identical holds verdicts, and I found no disagreement to resolve. I rederived the coset-PGM factorisation: substituting t=u+d splits the sign into s_J.t and s_J.d, so the data factor is v_{s_J}, and Z^J, H^M and uniform fiber lifting give the exact Gibbs law. I recomputed the H=(111) coset masses 0.566875 and 3x0.144375, which give word success 0.895685 and error 0.104315. The linear-mode classical sampler gives Pr(x=0)=(1+(-1)^J_2 c)/2, which reproduces the worst TV 0.65 at J=(1,1,0), c=13/20. The headline keeps the inefficiency caveat, and the status block keeps the review-pending scope.

## Claims

### 1. holds

> YES for an exact global coset PGM. This does not make that measurement efficiently implementable

- Step: Scientific Question And Prior Art
- Finding: This follows from the factorisation in 'Why Global PGM Can Work Despite Word Errors', which needs q_s>0 (true for 0<=c<1 because every per-bit Fourier mass (1+-c)/2 is positive). The efficiency caveat is stated.
- Conceded by the note's own self-check: no

### 2. holds

> Translation by G u sends mu_d to mu_(d+u), and

- Step: Why Global PGM Can Work Despite Word Errors
- Finding: X^(Gu) multiplies the coset-s Fourier component by (-1)^(s.u), shifting the character index, so <mu_d|psi_Gu>=a_(d+u), and sum_t|a_t|^2=sum_s q_s=1 by Parseval.
- Conceded by the note's own self-check: no

### 3. holds

> For the exact nondemolition rank-one measurement, A/copy/A^dagger clears R and subtracts d from C

- Step: Why Global PGM Can Work Despite Word Errors
- Finding: A|mu_d>|0>=|mu_d>|d>, so A^dagger clears R after the XOR. With t=u+d, J.G(t+d)=s_J.t+s_J.d gives the stated product, whose data factor 2^-k sum_d sum_s (-1)^((s+s_J).d) v_s equals v_{s_J}.
- Conceded by the note's own self-check: no

### 4. holds

> Uniform affine-fiber lifting gives EXACT Gibbs probabilities. Word success is only |a_0|^2

- Step: Why Global PGM Can Work Despite Word Errors
- Finding: After Z^J and H^M, y'=y+J lies in ker G^T=im H^T with weight prod(1+c(-1)^(y'_j+J_j)), and every legal y' has the same number of preimages x, so uniform lifting is exact.
- Conceded by the note's own self-check: no

### 5. holds

> The three-bit PGM word error is about 0.104315, while unconditional sampling is numerically exact and data purity is one

- Step: Decisive Finite Controls
- Finding: For H=(111) at c=13/20 the coset masses are 0.566875 and 3x0.144375, so |a_0|^2=(sum sqrt q_s)^2/4=0.895685. This matches the artifact's acceptance 0.895685 and word error 0.104315, with TV below 3e-15 and purity 1.
- Conceded by the note's own self-check: no

### 6. holds

> Draw independent b_j with Pr(b_j=1)=(1-(-1)^J_j c)/2, then set y=(I-GF)^T b and solve H^T x=y uniformly

- Step: Try To Kill It: Matched Classical Laws
- Finding: For H=(111) with systematic coordinates 0 and 1, y=(b2,b2,b2), so Pr(x=0)=(1+(-1)^J_2 c)/2. This reproduces the artifact's 0.6/0.4 at c=1/5, J=0 (TV 0.1714) and the worst TV 0.65 at J=(1,1,0), c=13/20.
- Conceded by the note's own self-check: no
