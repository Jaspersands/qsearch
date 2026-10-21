# Referee review: COHERENT_BPQM_ERASURE

Note: `research/COHERENT_BPQM_ERASURE.md`. Reviewed 2026-10-22 by claude-opus-5.5-two-judges-reconciled-2026-10-21. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges reached the same verdicts: the erasure rank criterion, the explicit recovery for the M5 control, Gao's union-bound use, the weight-two Helstrom floor and the duplicate-factor identity hold, and every table entry matches the artifact. Both flagged the research-decision sentence as a scope gap, and I confirmed it: amplitudes, workspace and TV were executed only on the single 5-wire, 3-check code with explicit herald tables, while the 128-512 wire rows are rank/topology plans only. The only disagreement was covered_by_self_check (A true, B false). I set it false: the scope is stated in the socket-plan section, but neither the self-check nor the not-claimed line concedes that the decision headline drops it. Judge A's side remark about the rank-deficient 64-spin seed-29 plan was not raised as a claim; the table reports it, so I did not add a finding.

## Claims

### 1. gap

> The coherent erasure stage is now implemented and its phase/workspace composition is checked

- Step: Research Decision And Next Decisive Gate
- Finding: As a headline this drops the scope stated in the body. The phase/workspace composition was executed only on the declared M5 code (checks 25,26,12; 12 qubits; gate-reference cap 10 data wires, statevector cap 18 wires), for two orders and two c values. The root programs use explicit herald tables that can be exponential (artifact explicit_herald_tables_can_be_exponential=true, efficient_approximate_reliability_register_implemented=false). The 128-512 wire inputs have no circuit, decoder error or TV (artifact quantum_circuit_compiled_or_executed=false). The decision should say the composition is
- Conceded by the note's own self-check: no

### 2. holds

> Recovery is possible exactly when rank Q_S=k, equivalently rank H_B=|B

- Step: Exact Public Erasure Criterion
- Finding: Both conditions are equivalent to there being no nonzero codeword supported on B, given that G has full column rank. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> u_0=b_2, u_1=b_0 XOR b_2, so the test genuinely reconstructs erased information

- Step: Executed Cyclic Control
- Finding: Check 25 (bits 0,3,4), check 26 (bits 1,3,4) and check 12 (bits 2,3) give x3=x2 and x4=x0+x3, so u_0=b_2 and u_1=b_0+b_2. Checks 25 and 26 share variables 3 and 4, a four-cycle. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> At c1/5, mean TV is over24 times word error

- Step: Executed Cyclic Control
- Finding: Artifact: 0.02878618/0.00115762=24.87 and 0.02880049/0.00115652=24.90. All four table rows (word errors 0.0011576, 0.0011565, 0.1128592, 0.1082660 and the mean/worst TVs) match the finite_controls entries. Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> Therefore ANY single-copy decoder has uniform-codeword error at least

- Step: Kill The Tempting Overinterpretation
- Finding: The per-coordinate overlap is 2sqrt(gamma(1-gamma))=c, so a weight-w difference has overlap c^w, and the genie pair label only helps. Helstrom gives (1-sqrt(1-c^(2w)))/2, which is 0.0468 at c=13/20, w=2, inside the stated (0.04,0.05). Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> Their product is K*(1+c_eff*(-1)^(a.x)). Opposite copies cancel to a constant

- Step: Kill The Tempting Overinterpretation
- Finding: Evaluating the product at (-1)^(a.x)=+1 and -1 gives A+ and A-, which fixes K and c_eff. Two negative copies give -2c/(1+c^2)=-520/569 at c=13/20, and equal opposite counts give A+=A-, so c_eff=0. Both judges agree.
- Conceded by the note's own self-check: no
