# Referee review: BPQM_LOG_RELIABILITY

Note: `research/BPQM_LOG_RELIABILITY.md`. Reviewed 2026-10-23 by codex-audit-correction-2026-10-23-r3. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Every load-bearing step checks: the gradient l1-norm equals max(|tanh(x+y)|,|tanh(x-y)|) <= 1, the (2n-1)eta induction closes, ||Ry(t)-Ry(t')|| <= |t-t'|/2 gives the half-angle multiplexer bound, and 4 occurrences x E x (2L-1)eta/2 gives 2E(2L-1)2^-b. The five-channel numbers match the artifact (27/32768 < 1/1000 at b=17, b=16 fails; 21-bit register). The judges disagreed only on the illustrative 2^60-root bullet: A held it, B called it a gap because E and the leaf overlap are not restated. I drop B's gap: E <= 2^60*(L-1) is forced because a binary tree on at most L outputs has at most L-1 merges, so 152 bits suffice for every admissible E at the 1/1000 target of the bullet above (151 bits give 0.00199), and 193 = 152 + 41 integer bits matches the c=13/20 leaf stated in that same preceding bullet. The conditional scope (uniform per-branch guarantee, no overflow, disjoint subtrees, exact uncomputation, review pending) is kept in the title, status and conclusion.

## Claims

### 1. holds

> Their absolute values sum to max(|tanh(x+y)|,|tanh(x-y)|)<=1

- Step: Uniform Stability Derivation
- Finding: With a=tanh(x+y), b=tanh(x-y): |a-b|/2+|a+b|/2 = max(|a|,|b|) <= 1, so f is 1-Lipschitz in the infinity norm globally. Both judges agree.
- Conceded by the note's own self-check: no

### 2. holds

> Induction bounds the log error at a subtree of n original outputs by (2n-1)eta

- Step: Uniform Stability Derivation, induction
- Finding: Leaf eta; parity (2n1-1)+(2n2-1)+1 = 2n-1; equality max(.)+1 <= 2n-2; angle (2n1-1)+(2n2-1)+1 = 2n-1 using |d/dt[-2atan(e^t)]| = sech t <= 1. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> Its operator error is bounded by HALF the maximum branch angle error

- Step: Uniform Stability Derivation, multiplexer paragraph
- Finding: For Ry(t)=exp(-itY/2), ||Ry(t)-Ry(t')|| = 2|sin((t-t')/4)| <= |t-t'|/2, and a block-diagonal multiplexer over orthogonal herald branches has error equal to the maximum block error. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> algorithm is at most 2 E (2L-1) 2^-b + epsilon_source

- Step: Uniform Stability Derivation, whole-program bound
- Finding: Hybrid sum 4 x E x (2L-1)eta/2 = 2E(2L-1)eta, and pure-state TV <= ||psi-psi'||. Conditional on the stated uniform per-branch guarantee, which the note says selected checks cannot replace. Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> ideal source, b=17 suffices under the stated assumptions

- Step: Range, Examples And What Changed
- Finding: 2*6*9*2^-17 = 27/32768 ~ 8.24e-4 < 1/1000, equal to the artifact's logical_rotation_readout_TV_perturbation_upper; b=16 gives 27/16384 > 1/1000. Register 5*25405/32768 + 4*2^-17 = 63513/16384 is below 4, so 3 signed integer bits would suffice. The producer's conservative rule allocates 4 signed integer bits plus 17 fractional bits, matching the note's sufficient 21-bit register. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> 2^60-root budget uses152 fractional bits and193 bits per message

- Step: Range, Examples And What Changed, illustrative bullet
- Finding: Judge B's gap (E and leaf overlap unstated) dropped on recomputation. E <= 2^60*(L-1) follows from L outputs per root (at most L-1 binary merges), and the producer uses exactly that worst case; 2E(2L-1)2^-152 = 0.000997 <= 1/1000 while 2^-151 gives 0.00199, so 152 is sufficient for every admissible E at the target stated in the preceding bullet. 193 = 152 + 41 signed integer bits, matching L*atanh(13/20) ~ 8.6e11 with the c13/20 leaf named in that preceding bullet. Restating target and leaf overlap in the bullet would be clearer, but the figures are reproducible from the text.
- Conceded by the note's own self-check: no
