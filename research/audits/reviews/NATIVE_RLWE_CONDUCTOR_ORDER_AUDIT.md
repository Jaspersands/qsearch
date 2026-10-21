# Referee review: NATIVE_RLWE_CONDUCTOR_ORDER_AUDIT

Note: `research/NATIVE_RLWE_CONDUCTOR_ORDER_AUDIT.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The principality gate, the contained-lattice index Norm_K(beta), the local-certificate probability 1-(q^(d/2)-1)/q^d and the saturation O_0*Lambda_M=O_0 all check, and I reproduced the bounded d4 count (48 units, 0 mixed). Judge A rated the note sound; judge B raised two gaps, a missing trace normalization in the metric sentence and a title that states nonprincipality without the M=0 exception. I dropped the normalization gap: the note uses the coefficient (constant-term) trace, under which nrd's trace equals ||g||^2+||f||^2 exactly, so the 'exactly' is not shown false. I kept the title gap, since Section 3 proves Lambda_0=O_q*j is principal and the nonprincipality rests on a review-pending proof that uses a published theorem.

## Claims

### 1. gap

> Native RLWE: Exact Metric, Nonprincipal Quaternion Ideal

- Step: Title (headline scope)
- Finding: The title asserts nonprincipality without conditions. Section 3 proves nonprincipality only for M!=0 mod q: the zero ratio gives Lambda_0=qR+Rj=O_q*j, which is principal and has source probability q^(-d). The global proof also depends on the cited DDK Proposition 3 and is review pending. The title needs 'for M!=0 mod q'.
- Conceded by the note's own self-check: no

### 2. holds

> Lambda_M is principal over THIS O_q if and only if M=0 modq

- Step: 3. Global Principality Gate: Only The Zero Ratio
- Finding: Equal covolumes force |Norm_K(nrd alpha)|=1; the totally positive unit is v^2; alpha/v has reduced norm one, so its constant coefficient ||g||^2+||f||^2=1 forces a signed monomial in one block. A first-block unit would need g=0 mod q; a second-block unit needs Mf=0 mod q with f invertible, so M=0. The converse Lambda_0=O_q*j is direct. Artifact principal probability 1/9 at d2,q3 matches q^(-d).
- Conceded by the note's own self-check: no

### 3. holds

> every totally positive unit of O_F is a square of a unit

- Step: 3. Global Principality Gate, cited dependency
- Finding: Full circular-unit signature rank implies a surjective signature map from O_F^*, and O_F^*/(O_F^*)^2 has order 2^[F:Q], so the kernel (totally positive units) equals the squares. This depends on DDK Proposition 3 as cited; neither judge nor I checked the paper itself.
- Conceded by the note's own self-check: no

### 4. holds

> The original reduced-norm trace is exactly ||g||^2+||f||^2

- Step: 1. The Metric Obstruction Is Not Universal
- Finding: Judge B called this a gap because Tr_{K/Q} carries a factor d. The note uses the coefficient (constant-term) trace, as in Section 3's 'coefficient trace', and the constant coefficient of g*bar(g)+f*bar(f) is exactly ||g||^2+||f||^2 in the power-of-two coefficient embedding. Under any reading the difference is a uniform scale, so no weighted metric is introduced. Dropped as a gap.
- Conceded by the note's own self-check: no

### 5. holds

> the local certificate covers probability 1-(q^(d/2)-1)/q^d on the full IID source

- Step: 2. Locally Principal Does Not Mean Globally Principal
- Finding: R_q=E x E with conjugation swapping the factors, so M*bar(M)=-1 holds in both factors or neither; that happens for x-1 of the x^2 residues with x=q^(d/2), and nonunit M give a unit beta in the relevant factor. The stated probability follows for uniform M.
- Conceded by the note's own self-check: no

### 6. holds

> Hence the sum is the WHOLE O_0

- Step: 4. What Survives The Critique
- Finding: Lambda_M+j*Lambda_M contains qO_0 and the columns (C_M;I) and (-I;C_M^T) with determinant Norm_K(beta), coprime to q, so the sum has index coprime to q and contains qO_0, hence equals O_0. The d4 example v=1+sqrt2=(1,1,0,-1) with reduced norm 3+2sqrt2 and the bounded d4 check (48 units, 0 mixed, artifact bounded_d4_unit_check) also reproduce.
- Conceded by the note's own self-check: no
