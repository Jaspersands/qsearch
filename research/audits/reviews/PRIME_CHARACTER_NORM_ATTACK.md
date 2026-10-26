# Referee review: PRIME_CHARACTER_NORM_ATTACK

Note: `research/PRIME_CHARACTER_NORM_ATTACK.md`. Reviewed 2026-10-22 by audit-correction-2026-10-22. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

The norm criterion, the K>max(|A|,D) budget, the Cayley strict-root rotation, the rho=1 all-parameter counterexample and the IID-shift first-trial bound all check out. I recomputed D0=(0,4,14,16) with roots 0,9,16, and confirmed that Q=13 is strict-perfect with nu=5 a nonsquare. The artifact matches the executed claims: perfect 127/127 in 1 and 15 trials, degrees 69 and 64, sufficient dimensions 70 and 65, and K39 not applicable. The research-decision summary of what the previous experiment left open omits the N31,K16 mixed seed71 source (30/31) and the r=3/r=4 mixed controls, and its 'solved common cosets' passes over the N127,K39 global inputs at 108/127 and 110/127. The norm budget can never hold at N31,K16, so 'does not apply to the saved K39 inputs' is not the full list of inapplicable saved inputs.

## Claims

### 1. holds

> a monic polynomial is a norm exactly when every odd-degree irreducible has even multiplicity

- Step: Classical Norm Construction
- Finding: Correct: an even-degree irreducible splits into conjugates over F_(p^2); an odd-degree one stays irreducible and has norm f^2. Leading constants are norms because N(c)=c^(p+1) is onto Fp^*.
- Conceded by the note's own self-check: no

### 2. holds

> The exact sufficient degree condition is

- Step: Problem And Exact Degree Budget
- Finding: With Q=Q0+R^2, deg Q0=|A| (lambda V_A term) and deg R^2=D (F=rho^2*monic of degree D, so H has degree D/2), the condition is K>max(|A|,D). On B, Q-t_i=R^2-F(a_i)=nu Z^2. Artifact: sufficient_RS_dimension 70 and 65; witness degrees 69 and 64.
- Conceded by the note's own self-check: no

### 3. holds

> has a NONZERO quadratic numerator in s, since the original pair is nonzero

- Step: Strict Roots Without A Field-Size Search
- Finding: alpha_s has norm (1-nu s^2)/(1-nu s^2)=1. R'=0 gives nu R s^2+2nu Z s+R and Z'=0 gives nu Z s^2+2R s+Z, each nonzero when (R,Z)!=(0,0) and p is odd. That gives <=2N bad s, so 2N+1 distinct candidates suffice when p>2N.
- Conceded by the note's own self-check: no

### 4. holds

> NONE of the23 parameters is a norm, although OPI itself is easy

- Step: Try To Disprove The Pencil, Then Repair It
- Finding: Recomputed V_A-V_B over F23: coefficients (0,4,14,16), roots {0,9,16}. Q=13 gives residual 13 (square) on A and 17,14,5,7 (all nonsquares) on B. The moving linear factor can fix at most one odd linear multiplicity. The artifact's expanded repair reaches 8/8 in 5 base factorizations.
- Conceded by the note's own self-check: no

### 5. holds

> so F/rho^2 is a uniform monic degree-D polynomial

- Step: A Rigorous One-Trial Average-Case Statement
- Finding: Conditioned on the A shifts and lambda, rho, the B residuals (plus the auxiliary value) are uniform, and interpolation is a bijection. Irreducibles of even degree are norms with no roots, so success is >=I_p(D)/p^D, about 1/D (D=58 and 64 for the saved patterns, matching norm_target_degree in the artifact). The 1/(2N) claim follows since the budget forces D<K<=N.
- Conceded by the note's own self-check: no

### 6. gap

> solved common cosets classically but left mixed high-rate controls at124/127 and122/127

- Step: Research Decision
- Finding: The previous experiment's artifact also leaves N31,K16 mixed seed71 at 30/31 (r=2, rate 16/31>1/2) and the r=3/r=4 mixed controls below perfect. The norm attack was not run on N31, and its budget K>max(|A|,D) cannot hold there: |A|+|B|=31 forces max(|A|,D)>=16=K. Neither this summary nor 'It does not apply to the saved K39 inputs' reports that case. 'Solved common cosets' also overstates it: they were solved only when K>=(r-1)ceil(N/r), and the N127,K39 global inputs score 108/127 and 110/127 (judge E).
- Conceded by the note's own self-check: no
