# Referee review: PRIME_CHARACTER_EXTERIOR_BOUND

Note: `research/PRIME_CHARACTER_EXTERIOR_BOUND.md`. Reviewed 2026-11-14 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agree that the cycle-indicator identity, the S_(n-1) invariant argument, the tame Hc1 dimension, the I/p bound and the 1/(2n) field condition hold. Recomputation confirms A=4986819005910345345662844 (16A^2 is 169 bits against the 756-bit twist threshold), 333/4036 and 3941/20014, D_bad=55440, and a 1672-fiber failure of 1.6e-5. The judges disagreed only by each flagging a different headline sentence, and both findings survive my check. A: the Outcome calls the 192-bit result a 'genuinely enlarged fixed-input guarantee' although item 4 says the trace-formula application still needs review; B: 'expected-polynomial ... in this promised regime' follows a requirement list that omits the p>=max(16A^2,4(R+A)) and p>=2D_bad field conditions, which the 61-bit inputs fail. Both are kept as gaps that the self-check covers, because the not-claimed line disclaims all-field dequantization and any independently accepted proof.

## Claims

### 1. holds

> Conditional on independent review of the local compact-support trace/weight application, this is a genuinely enlarged fixed-input guarantee, not an empirical seed-success estimate

- Step: Scientific Question And Outcome
- Finding: Scientific Question And Outcome now explicitly qualifies the guarantee with independent review of the local compact-support trace/weight application.
- Conceded by the note's own self-check: yes

### 2. holds

> when the degree-slack and large-field thresholds p>=max(16A^2,4(R+A),2D_bad) also hold (about 169 bits at n=76, which the 61-bit inputs fail), an expected-polynomial classical solver removes that opening in this promised regime (subject to review of the local trace application)

- Step: Problem And Mechanism
- Finding: Problem And Mechanism now states the full large-field threshold p>=max(16A^2,4(R+A),2D_bad) (noting ~169 bits at n=76 and 0 on the 61-bit fields) and the review-pending trace application.
- Conceded by the note's own self-check: yes

### 3. holds

> For degree76, modulus degree58, the sufficient field threshold falls from 756 bits to169 bits

- Step: Scientific Question And Outcome
- Finding: Recomputed: R=134 and A=132*(2^75-1)=4986819005910345345662844 make 16A^2 a 169-bit number, with 4(R+A) at 85 bits. The twist threshold 64G^2 for n76,b58 is 756 bits. 2^192-2^64-1 exceeds 16A^2.
- Conceded by the note's own self-check: no

### 4. holds

> therefore gives the EXACT identity n*1_(n-cycle)(sigma) = sum_(j=0)^(n-1) (-1)^j chi_j(sigma)

- Step: Exact Cycle Indicator
- Finding: det(1-t*sigma|V)=prod(1-t^l_i)/(1-t) is n at t=1 for an n-cycle and 0 otherwise. Expanding det(1-M) as sum (-1)^j Tr(wedge^j M) gives the identity. The stored character sums satisfy n*I: 101+1+39+19=160=4*40 and 10005+1+107-1=10112=4*2528.
- Conceded by the note's own self-check: no

### 5. holds

> A = (R-2)*(2^(n-1)-1), I/p >= max(0, (p+1-R-A*ceil(sqrt(p)))/(n*p))

- Step: Trace Bound And Its Dependencies
- Finding: Summing (R-2)C(n-1,j)sqrt(p) over j>=1 gives A*sqrt(p), and #U(Fp)>=p+1-R. Recomputed: p1009 gives 333/4036 and p10007 gives 3941/20014, matching the artifact and below the observed 264/1009 and 2528/10007. This holds under the imported cohomological facts, which the note flags as review pending.
- Conceded by the note's own self-check: no

### 6. holds

> A sufficient condition for the new fiber success rate>=1/(2n) is

- Step: Uniform Field Regime And Cost
- Finding: p>=16A^2 gives A*ceil(sqrt p)<=p/4+A, and R+A<=p/4, so the numerator is at least p/2+1. Unlike the Morse note's condition, the +A term from the ceiling is explicitly absorbed by the 4(R+A) term.
- Conceded by the note's own self-check: no
