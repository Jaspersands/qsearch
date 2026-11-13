# Rees exponent: the κ = 9 bottleneck of R7 (2026-11-13)

AI only (one Claude Code subagent), pending human review. No paper, STATE, handoff, registry or
reductions file was edited. No Git, no network, no API calls. Every run used `nice -n 19`, with one
heavy process at a time; the largest RSS was about 0.6 GB (kissat at p = 73). Scripts and outputs are in
`research/audits/reviews/2026-11-13-rees-k9-bottleneck/`. CNFs were written to the session
scratchpad (`.../scratchpad/k9bn/`); they can be regenerated.

Labels: PROVED, PROVED given cited results, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite
checks can only falsify.

Inputs read:
- `2026-11-13-rees-k9-sat.md`, whole;
- `2026-11-12-rees-exponent-k8-attack.md` §§0–5, 9, 11;
- `appendix-schedule2.tex` lines 482–660 (tower, chains, union targets);
- `2026-11-05-rees-threshold-7-check/` (`reach.py`, `rc.py`, `rcdfs.c`, `reach_89.out`).

## 0. Verdict

1. **The class-9 maximum of the R7-type rule drops from 25 to 21.**
   - Status: CONDITIONAL, exactly as R7 is, because the other grades still use the R5 inputs.
   - The new κ = 9 nodes themselves are PROVED, given thm:app-s2-chain, Lemmas S and F and Theorem HC
     of the 11-12 note, and finite witnesses checked by two programs.
   - New rule R8 (`exponents_r8.py` → `exponents_r8.out`, primes ≤ 30000). The maxima for c = 2..9 are
     **3, 5, 9, 10, 14, 16, 19, 21**. R7 gave 3, 5, 9, 10, 14, 17, 20, 25.
   - At c = 9 the 21 is attained at **p = 13, 19, 37, 73**. The next value is 20, at 7561, 2521, 2017,
     1009, 673, 631, 433, 181, 127 and 43.
2. **New κ = 9 nodes at the five R7-binding primes.**

   | p | R7 degree | new degree | node |
   |---|---|---|---|
   | 37 | 9 | **5** | stage, then finish |
   | 73 | 9 | **5** | stage, then finish |
   | 127, 181, 433 | 9 | **4** | one chain |

   - At 127, 181 and 433 the node is a single flexible-line chain (1,{0}) → (3,{0}) → (9,{0,m}) → (9,{0}),
     of arity C(a+4,4). The paper's rem:app-s2-chains-scope already lists these chains, but R5 and R7
     never charged their degree (an accounting gap; §2).
   - At 37 and 73 the node is a "third-degree collision" (§3): a κ = 3 relation refined to a two-class
     9-relation (degree 3), used as a Lemma S stage, then a degree-2 finish.
   - Also new, all at the same standard: (19, 9) 9 → 6, unconditional (it replaces the ℓ = 3-conditional
     6 of the k9-sat note); 109, 163, 199, 307 → 4; κ = 7 at p = 29: 7 → 5.
3. **Within the current descent calculus, 21 cannot be lowered (PROVED by exhaustion, given the
   finite searches).**
   - p = 37 and 73: no plan has degree ≤ 4.
   - p = 19: no plan has degree ≤ 5.
   - At p = 13 the 21 comes from the grades κ = 4 and κ = 6, not from κ = 9, and is unchanged from R7.
   - What lies outside the calculus and would be needed (§5):
     - at 37 and 73, a degree-4 {0}-node (for example a four-level joint contraction; UNKNOWN);
     - at 73, also a three-level joint contraction (run here: NOT computed, timeout);
     - at 19, a three-level IS {0,m} stage with m ∈ {2..7} (UNKNOWN; conditional on IS Lemma 12 at
       ℓ = 3);
     - at 13, the ℓ = 3 joint contractions at (13,4) and (13,6), which the k9-sat scan reports SAT.
       They are conditional on ℓ = 3 and would give E(13) = 18.

   Even granting every ℓ = 3 object, **37 and 73 keep 21**.
4. **Routes 1 and 2 of the brief (three-level {0,m} SAT at 73/127/181/433, split search at 37) were
   NOT computed.** They are PROVED unable to lower R8 at those primes (§4). The only SAT run that
   could still matter was the three-level *joint* (K = {0}) search at 73. It timed out (§4).

## 1. Units, P_9 and P_3 (`units_check.out`, exact)

| p | g | ind mod 9 of −1, 2, 3 | in P_9 | in P_3 |
|---|---|---|---|---|
| 19 | 2 | 0, 1, 4 | −1 | −1 |
| 37 | 2 | 0, 1, 8 | −1 | −1 |
| 73 | 5 | 0, 8, 6 | −1 | −1, 3 |
| 127 | 3 | 0, 0, 1 | −1, 2 | −1, 2 |
| 181 | 2 | 0, 1, 2 | −1 | −1 |
| 433 | 5 | 0, 6, 4 | −1 | −1, 2 |

- −1 ∈ P_9 at every p ≡ 1 (mod 18), so these rows are no surprise. It is why two identical stages
  followed by F0 always work.
- At 37, P_9 = {±1, ±6} = μ_4 (6² = −1, the units of Z[i] mod 6+i) and P_3 = μ_12. Also
  F_37^× = μ_4 × μ_9, so the 9-class of x is its μ_9-component.
- I found no direct use of this structure that beats the plan of §3. The plan does not use it.

## 2. Chains to every target (`chains_all.py` → `chains_all_{a,b,c}.out`, `chains_all.json`)

**What was computed.** For each (κ, p) with R5 ≥ 5 (27 pairs, p ≤ 433), a BFS from (1,{0}) over the
nodes (D, K) with D | κ and 0 ∈ K ⊆ Z_D. An edge (D,K) → (D₂,K₂) means that RC(D₂; lift(K) → K₂) is
feasible.
- The feasibility test is the complete DFS `rcdfs.c` of the 11-05 check, copied here.
- Every witness is re-checked by `rc.check`.
- All edge tests were decided: none was undecided at node limit 10⁹.

**What a chain gives.** By the induction in the proof of thm:app-s2-chain, a chain of length L that
ends at (D_L, K_L) is a law-free deterministic node:
- its arity is C(a+L+1, L+1), so its degree is L+1;
- its nonzero weights have κ-class in lift(K_L), with one weight equal to 1.

The theorem is stated for K_L = {0}, but the claim C(t) in its proof is for an arbitrary K_t. I
re-derived that the last step never uses K_L = {0}. So a chain to K_L is a K_L-node: a two-class node
when |K_L| = 2, and a finish (Lemma F) otherwise.

deg[K] = least degree of a chain whose final class set lies in K, with L ≤ 3.

| κ, p | deg[{0}] | deg[{0,m}], m = 1..8 |
|---|---|---|
| 9, 19 | none (any length) | 3, –, –, –, –, –, –, 3 |
| 9, 37 | none (any length) | 4, –, 4, **3**, **3**, 4, –, 4 |
| 9, 73 | none (any length) | **3**, 4, 4, **3**, **3**, 4, 4, **3** |
| 9, 109 / 127 / 163 / 181 / 199 / 307 / 433 | **4** | all 3 |
| 7, 29 | none | all 3 |

- "None (any length)" agrees with the complete reachability search of `reach_89.out` and with
  rem:app-s2-chains-scope.
- No two-level {0,m} union step exists at 19, 37 or 73. Two codes agree on this: `rcdfs.c`, here,
  and `union_step_exists` in R7, whose stage options at these primes are empty.

## 3. The degree-5 nodes at 37 and 73 (PROVED given thm:app-s2-chain, Lemmas S/F, Theorem HC and the witnesses)

**p = 37, g = 2, ε = −2^{−4} (mod 37).** Witnesses (`witness_dump.out`; α₀ = 1, β₀ = 0 normal form):
- RC(3; Z₃ → {0}): α = (1, 0, 12), β = (0, 2, 1).
- RC(9; {0,3,6} → {0,4}): α = (1, 0, 17, 10, 36, 34, 0, 10, 32), β₃ = 1, β₆ = 27.
- RC(9; Z₉ → {0,2,5}): α = (1, 35, 8, 24, 20, 21, 30, 0, 26),
  β = (0, 11, 36, 2, 29, 13, 17, 16, 7).

The plan:
1. **Stage.** The chain (1,{0}) → (3,{0}) → (9,{0,4}) is a {0,4}-node of arity C(a+3,3). Its first
   step is a κ = 3 relation, whose coefficients lie in P_3, with 9-classes {0,3,6}. The second step
   refines it to the classes {0,4}. By Lemma S each group gives either a solution, or a vector with
   two disjoint P_9-weighted representations of ratio ε.
2. **Finish.** After the stage, Tn(1,ε)∖0 has 16 elements, with classes {0,2,3,5}
   (`one_stage_tn.out`). The union step to {0,2,5} ⊆ {0,2,3,5} is a K-node of arity C(a+2,2), and
   Lemma F with ρ = 1 finishes.
3. **Arity.** C(a+3,3)·C(a+2,2) = (a+1)²(a+2)²(a+3)/12, so degree 5 (was 9).

This is the κ = 9 analogue of Theorem HC at (8,41). It needs one extra degree because P_3 has three
9-classes, so a bare κ = 3 solver is not a two-class node. A refinement step RC(9; {0,3,6} → {0,m})
makes it one.

**p = 73, g = 5.**
- The stage is the chain (1,{0}) → (3,{0}) → (9,{0,1}), with RC(9; {0,3,6} → {0,1}):
  α = (1, 0, 0, 43, 67, 28, 45, 48, 34), β₃ = 6, β₆ = 25.
- The finish is F2: Tn has classes {0,2,3,4,6,8} ⊇ {0,3,6}, so a κ = 3 solver of degree 2 finishes
  (R8(3,73) = 2).
- Degree 5 (was 9).

**Checks (finite; they can only falsify):**
- `witness_dump.out`: every cell is re-checked by the power-character test y^{(p−1)/D}. The test uses
  no discrete-log table, and the witnesses come from a pure-Python DFS independent of `rcdfs.c`.
  Result: ALL OK.
- `chain_exec.py` → `chain_exec.out`: an executor written from the definitions. It runs the proof of
  thm:app-s2-chain (rounds, back-substitution, subspace annihilators), then Lemma S, then Lemma F.
  - Result: 630/630 outputs verified (x ∈ (P_9∪0)^M, x ≠ 0, Σxλ = 0) at a = 1, 2, 3, on five bank
    types.
  - Plans covered: 37, 73, 19, the κ = 7 plan at 29, and the chains at 127, 181, 433.
  - Most uniform banks exit early (a one-sided stage output is already a solution).
- `chain_exec_forced.py` → `chain_exec_forced.out`: forces the full path. Groups are drawn until the
  stage output is two-sided; the discarded one-sided outputs are verified as solutions.
  - Result: 288/288 full-path runs verified, for p = 37, 73, 19 and (29, κ = 7), a = 1..3, on three
    bank types.
- `negctl.py` → `negctl.out`: negative controls.
  - Perturbing one α of the stage witness is caught 9/20 times. Only the runs that use the bad cell
    can be caught.
  - Declaring the stage a {0,5}-node is caught 20/20 times.
  - A finish K-node whose classes are not in Tn is caught 4/20 times, which is every run that reaches
    the finish.

## 4. Rerun of the rule, and the routes of the brief

**R8 = R7 plus chain nodes** (`exponents_r8.py`). R7 is imported read-only. R8 adds:
- base min(R5, deg[{0}]);
- stage options ('ch', m) of cost deg[{0,m}];
- finish F3' of cost deg[C − c].

It uses no ℓ = 3 object. The per-pair changes are in `exponents_r8.out`:
- κ = 9: 19 → 6; 37, 73 → 5; 109, 127, 163, 181, 199, 307, 433 → 4;
- κ = 7, p = 29: 7 → 5.

Nothing else changes.

| c | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| R7 | 3 | 5 | 9 | 10 | 14 | 17 | 20 | 25 |
| R8 | 3 | 5 | 9 (5, 13) | 10 | 14 | 16 (43) | 19 (13) | **21 (13, 19, 37, 73)** |

e_d at c = 9 (d = 2..9):
- 37: [2,2,3,1,3,1,3,5], E = 21;
- 73: [2,2,2,1,3,1,4,5], E = 21;
- 19: [2,2,2,1,4,1,2,6], E = 21;
- 13: [2,2,4,1,4,1,4,2], E = 21;
- 127, 181, 433: E = 20.

Tail: R8 ≤ R7, and the k8 note gives R7 ≤ R5 ≤ 18 above 20000, so the c = 9 maximum over all p > 9
is 21. The rows for c < 9 cover p ≤ 30000 only, as in R7.

**Route 1: three-level {0,m} union steps at 73, 127, 181, 433. NOT computed; PROVED unable to lower R8.**
- One stage followed by F0 is impossible (Proposition F).
- At 73, |Tn∖0| ≤ 56 < 72 for every m (`one_stage_tn.out`), so F1 is impossible too. A degree-3
  stage then costs ≥ 3 + 2 = 5 = R8.
- At 127, 181 and 433 a degree-3 stage costs ≥ 3 + 1 = 4 = R8.

**Route 2: split search at 37. NOT computed; moot for the same reason.** |Tn∖0| ≤ 24 < 36, so any
{0,m} stage of degree 3 gives ≥ 5 = R8. The three-level *joint* K = {0} search at 37 is certified
UNSAT (k8 §9, item 8). Regression here: same CNF (sha256 c00a76cec23e16d2), UNSAT in 35 s
(`sat_runs.log`). No local-search solver was used.

**The joint K = {0} search at 73.** `run_sat73.sh 73 0` (sat3_stream CNF, kissat, 1500 s):
- CNF: 70,956 variables, 7,863,193 clauses, sha256 prefix 0c60db036737cf36.
- Result: **timeout** after 1504 s, max RSS 240 MB. NOT computed.

A SAT answer would give a degree-3 κ = 9 node at 73, CONDITIONAL on IS Lemma 12 at ℓ = 3. That would
make E(73) = 19, but 37 would still bind at 21. So the class-9 maximum does not depend on this
search.

**Route 3 (algebraic).** Done; see §3. HC itself needs κ even, so a direct "κ/3 collision" does not
exist. The chain step RC(9; {0,3,6} → {0,m}) is the substitute.

## 5. Why 21 is the floor of the current calculus (PROVED by exhaustion, given the finite searches)

**Menu of nodes.**

| kind | degree |
|---|---|
| Gaussian elimination | 1 |
| two-level contractions and union steps (length-1 chains) | 2 |
| chains | L + 1 |
| D'-solvers | recursive (R8) |
| half-degree solver | n/a for odd κ |
| stages (Lemma S) with two-class nodes, ≤ 4 of them, then F0/F1/F2/F3 (Lemma F) | — |

Plans with ≥ 4 stages cost ≥ 12, and chains of length ≥ 4 cost ≥ 5 and are never useful below 6. So
R8's enumeration is complete for degrees ≤ 6.

**p = 37.**
- A {0}-node: no chain to {0} at any length (complete); 37 ∈ E_2(9); the ℓ = 3 joint contraction is
  UNSAT (certified).
- One stage: no two-class node of degree 2 exists, so the stage costs ≥ 3. F0 is excluded by
  Proposition F; F1 is excluded since |Tn∖0| ≤ 24 < 36. So the cost is ≥ 5.
- Two stages: ≥ 6.

Hence 5 is optimal at 37. The only possible exception is a degree-4 {0}-node outside the menu (a
four-level joint contraction, UNKNOWN: the k9-sat note sized it at about 25 M clauses and did not
run it).

The other grades at 37 are at their floors too.
- κ = 2 and κ = 3 cost 2, which is the bound of Proposition F.
- κ = 4 and κ = 6 cost 3. The R5 tables put 37 in E_2(4) and in E_2(6), so the menu has no degree-2
  {0}-node there, and no degree-1 two-class node exists.
- κ = 1 costs 1.

So E(37) = 1+2+2+3+1+3+1+3+5 = 21 is the least value of the calculus at 37, given the E_2 tables. That
alone pins the class-9 maximum of the calculus at ≥ 21.

**p = 73.** The same argument applies, with |Tn∖0| ≤ 56 < 72. The exceptions are a degree-4
{0}-node, or the three-level joint contraction (degree 3), which §4 left undecided.

**p = 19.**
- After a stage with m = 1 or 8 (the only degree-3 two-class nodes), Tn has three classes. No shift
  of {0,3,8} or {0,1,4} admits a degree-2 K-node (exact), and F1 is excluded since |Tn| ≤ 8 < 18.
  So the cost is ≥ 6.
- Exception: a three-level IS {0,m} stage with m ∈ {2..7} would give 3 + 2 = 5, because a degree-2
  finish exists for every such m (exact). These are CONDITIONAL on ℓ = 3. The k9-sat runs at
  m = 2, 3, 4 timed out.

**p = 13.** The κ = 9 grade is not involved there. κ = 4 and κ = 6 each cost 4, as in R7.

**Conclusion.** The class-9 value 21 can drop only if 37 and 73 both gain a degree-4 node from
outside this calculus. A finite search cannot exhibit such a node at practical cost, and nothing here
suggests one exists.

## 6. Adversarial self-check

- **Is a chain to K_L ≠ {0} really a K_L-node?** The proof of thm:app-s2-chain proves the claim for
  every t and every K_t: P_t returns weights in U with D_t-classes in K_t and one weight equal to 1.
  K_L = {0} enters only in the last sentence, which reads off P_L at U = 0. The generalization is
  therefore the proof's own induction claim, but the theorem's statement does not record it. A
  referee should confirm this reading. The executor asserts the output classes, and they passed.
- **Same coset generator everywhere?** Yes, the least primitive root: in `rc.py`, `exponents_hcd`
  and `chain_exec`. The executor checks classes end to end with its own generator, so a mismatch would
  have failed.
- **Search completeness.** The optimality claims of §5 rely on non-existence results:
  - no two-level {0,m} step at 19, 37, 73: two independent codes agree;
  - no chain to {0}: agrees with the 11-05 complete search;
  - |Tn| counts: exact.

  They do not cover nodes outside the menu. "21 is optimal" is claimed only for the calculus.
- **The 21 is still CONDITIONAL.** The grades other than κ = 9 use R5 (Schedule 2, E_2 tables, the
  NOSTD lists), exactly like R7's 25. The κ = 9 nodes at 37 and 73 do not use E_2.
- **The c < 9 rows** cover primes ≤ 30000 only. That is the same scope as R7; no separate tail
  argument is made for c < 9.
- **Executor coverage.** Uniform banks rarely reach the finish, so `chain_exec_forced.py` was added.
  The negative controls show the checks are live. Sizes tested: a ≤ 3 only.
- **Cost of finding the scalars.** All witnesses are constants for fixed (p, κ). Nothing
  asymptotic is claimed.
- **Not done:** LMAX > 3 (not needed below degree 6); LRAT certification (no new UNSAT); a
  four-level search at 37.

## 7. Next question and command

The new binding set is {13, 19, 37, 73}. The cheapest decisive question is whether a degree-4
law-free {0}-node exists at (37, 9). For example: a four-level joint contraction, or a chain
generalization whose step is three-level.

Next command, which is not expected to terminate within 2 h, so try a symmetry ansatz first:

    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-k9-sat/sat3_ansatz.py  # adapt to l = 4

Acceptance: a verified model gives E(37) = 20, still CONDITIONAL on IS Lemma 12 at ℓ = 4. UNSAT
leaves 21.

Paper text (proposal only, not edited): rem:app-s2-chains-scope could record that the listed κ = 9
chains have length 3, so degree 4. The conditional Outlook value 25 would then become 21.
