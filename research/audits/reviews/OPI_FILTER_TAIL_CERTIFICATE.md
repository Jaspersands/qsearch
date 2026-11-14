# Referee review: OPI_FILTER_TAIL_CERTIFICATE

Note: `research/OPI_FILTER_TAIL_CERTIFICATE.md`. Reviewed 2026-11-14 by claude-subagent-refresh-2026-11-14. Overall: **sound**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges agree that the K-wise moment argument, the 2ell+r<=K cutoff and the table hold; I reproduce 0.0307255 and 0.105285 from the degree-19 mean, and the artifact's degree-18/16 tails at 104 are 0.00448 and 9.84e-5. Both flag the closing 'Thus ... do NOT kill the quantum tail' sentence, and the gap is confirmed: on seed 29 (classical 105) every certified lower tail at 105 is 0. The summary also omits the six smaller artifact instances (N7 at 7/7, N31 at 27/31 and 30/31), where every certified quantum lower tail at the classical score is 0. They disagreed on 'Pr[S>=104]>=0.0307255 for EVERY balanced input' (A holds, B gap). I keep B's gap but narrow it: the universality across inputs is valid because the moments do not depend on the input (identical means for seeds 29/71), but neither the sentence nor the status block says the probability is for the ideal filtered state with an exact coherent decoder.

## Claims

### 1. holds

> Thus classical105/127 (seed 29, where the certified quantum lower tail at 105 is 0) and104/127 (seed 71, where positive ideal-filter lower tails are certified at 102 and 104) remain verified witnesses; a finite classical witness does not upper-bound the ideal quantum tail, although positive quantum lower bounds are certified only up to threshold 104 on N=127

- Step: Live Findings, closing paragraph
- Finding: Live Findings now distinguishes seed 71 (positive ideal lower tail at 104) from seed 29 (certified lower tail 0 at 105) and the six smaller N=7,K=3 and N=31,K=9 instances (certified lower tail 0 at the classical best scores).
- Conceded by the note's own self-check: no

### 2. holds

> For degree19, under the ideal filtered distribution P(S)^2 of an exact coherent decoder/filter with balanced predicates, Pr[S>=104] >=0.0307255 for EVERY balanced input of the stated RS form

- Step: Live Findings
- Finding: Live Findings now explicitly states that Pr[S>=104] >= 0.0307255 holds under the ideal filtered distribution P(S)^2 of an exact coherent decoder/filter with balanced predicates.
- Conceded by the note's own self-check: no

### 3. holds

> Consequently E[Q(S)] equals the Binomial(N,1/2) expectation for every polynomial Q of degree at most K

- Step: Exact Moment Argument
- Finding: Q(S) expands into products of at most K distinct acceptance bits. Any K RS positions are independent uniform, and balanced predicates make each bit fair. The K=1 identical-predicate countercontrol correctly shows the cutoff is needed.
- Conceded by the note's own self-check: no

### 4. holds

> score moment are therefore exactly known whenever 2 ell+r <= K

- Step: Exact Moment Argument
- Finding: P(S)^2*S^r has degree 2ell+r. At K=39 this gives 7, 3 and 1 certified moments for degrees 16, 18 and 19, matching certified_moment_order in the artifact.
- Conceded by the note's own self-check: no

### 5. holds

> At105 (the classical best-of-four score on seed 29), and at the classical scores 7/7, 27/31 and 30/31 on the six smaller N=7,K=3 and N=31,K=9 controls, the implemented moment certificates give zero as the lower bound

- Step: Live Findings
- Finding: For instance 6 (seed 29), all three filters have tail lower bound 0 at 105, with upper bounds 0.254/0.752/0.988. The note correctly labels this UNKNOWN.
- Conceded by the note's own self-check: no

### 6. holds

> Degree18 (0.004480) and degree16 (9.84e-5) also give positive lower bounds at104

- Step: Live Findings
- Finding: The artifact's instance 7 gives 0.004480 for degree 18 at 104. Degree 16 is also positive there (9.84e-5); the note does not mention it, but this does not contradict the note.
- Conceded by the note's own self-check: no
