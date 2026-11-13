# Referee: the κ = 9 bottleneck report (R7 25 → R8 21) (2026-11-13)

AI only (one Claude Code referee subagent), pending human review. Referees
`2026-11-13-rees-k9-bottleneck.md` and its folder. No other file was edited; no Git, no network,
no API calls. Every run used `nice -n 19`, one process at a time, RSS < 100 MB. Scripts and outputs:
`research/audits/reviews/2026-11-13-rees-k9-bottleneck-referee/`.

Labels: PROVED, PROVED given cited results, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite
checks can only falsify.

Primary sources read: `appendix-schedule2.tex` 482–660 (def. RC, lem:app-s2-refine,
thm:app-s2-tower, the RC(D;R→K) paragraph, chain definition, thm:app-s2-chain and its proof,
prop:app-s2-union-step, cor:app-s2-union-chain, rem:app-s2-chains-scope);
`2026-11-12-rees-exponent-k8-attack.md` §§0–5 (Lemmas S/F, Theorem HC, Proposition F);
`exponents_r7.py`, `exponents_hcd.py`, `exponents_r7_u3.py`, `exponents_r8.py`, `chains_all.py`,
`rc.py`; R5 in `2026-11-12-rees-exponent-discharge/exponents.py` (`e_grade`, `NOSTD`).

## 0. Verdict: CORRECT WITH FIXES

The three mechanisms hold, and my independent code reproduces every number that matters:
R8(9, p) = 5 at 37 and 73, 4 at 109–433, 6 at 19, R8(7, 29) = 5, and the class-c maxima
3, 5, 9, 10, 14, 16, 19, 21 (my rule, p ≤ 3000; c = 9 attained at exactly 13, 19, 37, 73, as in the report). The 21 stays CONDITIONAL exactly as R7's 25 was
(other grades use R5). The fixes are about wording and scope, not numbers (§6).

## 1. Is a chain ending at K a K-node? (task 1; PROVED from the proof of thm:app-s2-chain)

The proof of thm:app-s2-chain proves, by induction on t, the claim

> C(t): for every subspace U ≤ F_p^a of codimension m, P_t uses at most f_t(m) = C(m+t+1, t+1)
> fresh columns and returns weights w with Σ w_b λ_b ∈ U, every nonzero w_b of D_t-class in K_t,
> and w_{b*} = 1 for some b*.

I re-derived each step.
- C(0) has no class condition.
- The step t ≥ 1 uses three facts. (a) The chain condition R_t ⊇ {x : x mod D_{t−1} ∈ K_{t−1}} puts every
  input class i(b) in R_t, so β_{i(b)} is defined. (b) The cell condition gives class n + i + (k − i − n) = k ∈ K_t
  for every nonzero weight γ c_b(α_n + β_{i(b)}). (c) The normal form α_0 + β_0 = 1 gives the designated
  weight 1 at the stop round.
- None of these uses K_L = {0} or D_L = κ. Those two conditions enter only in the theorem's last
  sentence, which reads off P_L at U = 0, m = a.

What is proved, exactly: for any sequence of steps that satisfies the chain condition and has
RC(D_t; R_t → K_t) contractions in normal form, P_L at U = 0 gives, from any C(a+L+1, L+1)
columns of F_p^a, a nonzero x with Σ x_b λ_b = 0. Every nonzero x_b has D_L-class in K_L,
equivalently κ-class in lift_κ(K_L), and one x_b equals 1. The procedure is deterministic, and its
arity has degree L+1 in a.

So a chain is a K-node, with K = lift_κ(K_L), of degree L + 1. This includes chains with D_L < κ;
`chains_all.py` uses those too, for example (3,{0}) as a {0,3,6}-node of degree 2.

Two side remarks:
- **Q_0 at (0,0) matters only at steps t < L.** A last step whose (0,0) cell has class k ∈ K would
  still give a nonzero K-relation, but the next step's designated column would then have class
  k ≠ 0. `exponents_hcd.union_step_exists` (used by R7 for the 'u' stages and F3) admits any class
  of K at (0,0). That is valid, because every such use is a last step, and it is equivalent to
  RC(K − k) in normal form followed by multiplying the output by g^k.
- **Shift invariance.** A K-node times g^c is a (K + c)-node. R8 uses deg[{0,m}] but not
  deg[{0,−m}] for the stage cost. The κ = 9 tables are symmetric under m ↦ −m (last line of
  `ref_rule_3000.out`), and my shift-closed rule equals R8 at all 27 pairs, so this changes
  nothing here.

Status: PROVED (given the proof as written, AI-checked). The paper states only K_L = {0}, so any
use of the R8 nodes in the paper needs a stated corollary (§6, item 1).

## 2. Degree bookkeeping and the R7 → R8 diff (task 2)

**Degrees.**
- Chain node: length L gives arity C(a+L+1, L+1), degree L + 1.
  - The κ = 9 chain (1,{0}) → (3,{0}) → (9,{0,m}) → (9,{0}) at 127, 181 and 433 has L = 3, so
    degree 4. This is thm:app-s2-chain as stated, with K_L = {0}.
  - The stage (1,{0}) → (3,{0}) → (9,{0,m}) has L = 2, so degree 3.
- Theorem HC gives arity N'(a)·∏ N_j(a), so degrees add.
  - At 37 the arity is C(a+3,3)·C(a+2,2) = (a+1)²(a+2)²(a+3)/12, degree 5. This is correct.
  - At 73 it is C(a+3,3)·C(a+2,2), where the finish is the two-level κ = 3 contraction, a D' = 3
    solver whose 9-classes are {0,3,6}. Degree 5, correct.
- Lemma S needs only that the node's nonzero output classes lie in {0, m}, and Lemma F needs only
  that they lie in K. Both are supplied by §1.

**Diff of `exponents_r8.py` against `exponents_r7.py`.** Every change, and its effect:
1. `deg()` reads `chains_all.json`, which holds chains of length ≤ 3 from `rcdfs.c`, for the 27
   pairs with R5 ≥ 5 at p ≤ 30000. Every pair that R7 rescans has data, and none is marked
   "[no chain data]".
2. **Base.** `min(R5, deg[{0}])` is new. It is a chain {0}-node, valid by thm:app-s2-chain as
   stated.
3. **Stage options.**
   - R7's options are reused: 'half' at cost r8(κ/2), and 'u' at cost 2. The 'half' cost now
     recurses through r8 instead of r7. That is monotone, and no κ/2 changed, so it has no effect.
   - New ('ch', m) options cost deg[{0,m}] with the same ε = −g^{−m}. They are valid by §1 and
     Lemma S.
   - Some 'u' and 'ch' options with the same m are duplicates. This only enlarges the enumeration.
4. **Pruning.** `c0 + 0 >= best` became `c0 >= best`. They are identical.
5. **F2** recurses through r8, as R7's F2 recursed through r7. Monotone.
6. **F3.**
   - R7 tried one union step (cost 2) per shift and stopped at the first shift that worked. R8
     loops over all shifts c ∈ C and charges deg[C − c], which includes length-1 chains = union
     steps in normal form. It keeps the R7 union-step test only where `deg` is missing, which never
     happens.
   - R7's (0,0)-any-class union steps are covered by the loop over shifts (§1).
   - So F3 is never worse than in R7 and adds chain finishes of degree 3–4.
7. **Unchanged:** the sumset recursion for T and Tn, ≤ 4 stages, F0, F1, the `R5 < 5 → R5` cut-off,
   and E(c,p) = 1 + Σ_{d=2}^{c} r(gcd(d,p−1), p). The grades are combined exactly as in R7.

**Against `exponents_r7_u3.py`.** R8 does not contain the 'u3' option (cost-3 three-level stages,
CONDITIONAL on IS Lemma 12 at ℓ = 3). So, as the report says, R8 uses no ℓ = 3 object. Correct.

## 3. Independent verification of the witnesses (task 3)

**Witness checks** (`ref_common.py`, `ref_witness.py` → `ref_witness.out`). This is my own
discrete-log table, my own complete DFS in normal form (bitset, no cap), and my own chain BFS run to
a fixpoint. None of it shares code with `rc.py`, `rcdfs.c` or `chain_exec.py`.
- All 18 witnesses of `witness_dump.out` (at 37, 73, 19, 127, 181 and 433) pass a cell-by-cell
  check of the definition. Each chain condition holds.
- **Two-level union steps.** RC(9; Z_9 → {0,m}) is infeasible for every m = 1..8 at 19, 37 and 73
  (complete). This agrees with "no two-level {0,m} step".
- **Tower step.** RC(9; {0,3,6} → {0}) is infeasible at 19, 37 and 73.
- **Stage steps.** RC(9; {0,3,6} → {0,m}) is feasible exactly for:
  - m ∈ {4, 5} at 37;
  - m ∈ {1, 4, 5, 8} at 73;
  - m ∈ {1, 8} at 19.

  This is the report's deg[{0,m}] = 3 pattern.
- **E_2 membership.**
  - 37 ∈ E_2(4), E_2(6), E_2(9), and 37 ∉ E_2(2), E_2(3).
  - 73 ∈ E_2(6), E_2(8), E_2(9), and 73 ∉ E_2(4).
  - All by my complete RC(κ; Z_κ → {0}) search.
- **Complete reachability (no length cap).** (9,{0}) is not reachable at 19, 37 or 73.
  - At 37 the fixpoint has level 4. Chains of length 4 to {0,2} and {0,7} exist (degree 5). The
    report's table shows "–" because it caps at L ≤ 3. Harmless, since a degree-5 stage is never
    useful, but the table should say "none with L ≤ 3" (§6, item 4).
- **Tn after one stage.** The sizes and classes match `one_stage_tn.out` exactly:
  - at 37, m = 4: |Tn∖0| = 16, classes {0,2,3,5};
  - at 73, m = 1: |Tn∖0| = 48, classes {0,2,3,4,6,8};
  - max |Tn∖0| is 24 at 37 and 56 at 73.

**Independent end-to-end executor** (`ref_exec.py` → `ref_exec.out`), written from the proof of
thm:app-s2-chain and Lemmas S and F.
- It asserts C(t) at every call: value in U, classes in K_t, designated weight 1. It also asserts every
  rep value c_k u (resp. ε c_k u), and checks the final output: weights in P_9, nonempty, Σ = 0.
- It uses my own witnesses, and at 37 it uses the report's actual finish target {0,2,5}. The
  report's executor used {0,2,3,5} instead (§6, item 3).
- Plans: 37, 73, 19, and the direct {0}-chains at 127 and 181. Sizes a = 1, 2, 3; banks uniform,
  repeated and low-rank. Two modes: normal, and forced, where one-sided stage outputs are discarded
  until enough two-sided objects reach the finish.
- Result: **720/720 verified** (`ref_exec.out`). Every forced cell reached the finish with the full C(a+2,2) objects. A spot run at a = 4 (p = 37, 525 columns) also verified.
- Negative controls (`ref_exec_neg_*.out`):
- Perturbing α_2 of the stage witness: 105/180 caught by the class-in-K_t assertion. The rest never used the bad cell and gave valid outputs.
- Declaring the 37 stage a {0,5}-node: 165/180 caught. The 15 uncaught runs ended on an all-class-0 stage output, which is a genuine solution.

**The report's own controls, rerun once** (`rerun_negctl.out`, `rerun_chain_exec.out`):
`negctl.py` reproduces `negctl.out` exactly (9/20, 20/20, 4/20 caught). `chain_exec.py 30` gives **3150/3150 verified**; the argument 30 gives 150 runs per cell, against 30 in the report's own run.

## 4. Recomputed maxima (task 4)

`ref_rule.py` reimplements the rule from scratch. Its only input is R5 = `e_grade('R5', ·)`, the
base grade both R7 and R8 start from.

Its node menu is a superset of R8's:
- chains to a fixpoint (no length cap);
- D'-solvers;
- Gaussian elimination;
- shift-closed node costs;
- ≤ 4 stages, as in R7/R8.

Result (`ref_rule_3000.out`, p ≤ 3000, 15.7 min, no undecided RC test):
- The pairs with R5 ≥ 5 are the same 27 as in `exponents_r8.out`. All lie at p ≤ 433.
- At every one of the 27 pairs my value equals R8. In particular:
  - (9,19) = 6, (9,37) = 5 and (9,73) = 5;
  - (9,p) = 4 for p = 109, 127, 163, 181, 199, 307, 433;
  - (7,29) = 5;
  - every other pair equals R7.
- The maxima for c = 2..9 are **3, 5, 9, 10, 14, 16, 19, 21**, the same as R8 (whose run went to 30000).

  | c | maximum | attained at |
  |---|---|---|
  | 7 | 16 | 43 |
  | 8 | 19 | 13 |
  | 9 | 21 | {13, 19, 37, 73} |

  The next c = 9 value below 3000 is 20, at 2521.
- The e_d vectors at 13, 19, 37, 73, 127, 181 and 433 equal the report's.
- My superset menu (fixpoint chains, shift closure) lowers nothing. In particular, the length-4 chains
  at 37 (degree 5) are never useful.
- deg[{0,m}] = 3 for all m at 109–433, as in the report.

## 5. The floor at 37 (task 5)

Claim: within the calculus, E(37) ≥ 21, hence the class-9 maximum of the calculus is ≥ 21.
Status: PROVED given the finite searches (re-done independently in §3).

**Grade κ = 9 at 37.** The menu is:
- {0}-nodes: chains (none at any length, complete), the two-level contraction (37 ∈ E_2(9)),
  R5 = 9;
- two-class nodes: two-level union steps (none), chains (degree ≥ 3), the 'half' option (κ odd:
  none);
- D' = 3 solver: three classes, so not a stage.

So every stage costs ≥ 3. After one stage, F0 is excluded by Proposition F, and F1 by
|Tn∖0| ≤ 24 < 36. Every other finish has degree ≥ 2. Hence one stage costs ≥ 5, and ≥ 2 stages
cost ≥ 6. So 5 is the minimum, and my exhaustive rule gives exactly 5.

I also checked robustness to a generalization the report does not consider: "two-class plans",
that is, a Lemma F variant whose result has classes in {0,m}. Building a two-class node of degree
2 that way would need a stage of degree ≤ 1 or a K-node with |K| ≤ 2 on columns. Neither exists.
So the floor is not an artefact of stating Lemma S only for primitive two-class nodes.

**The other grades at 37.**
- κ = 2, 3: cost 2, which is Proposition F's floor.
- κ = 4, 6: cost 3. Since 37 ∈ E_2(4) ∩ E_2(6) (my complete searches), the only degree-2 {0}-node
  of the menu, the two-level contraction, is absent. A chain of length 1 to (D, {0}) with D < κ has
  more than one κ-class. Any plan costs ≥ 2 + 1.
- κ = 1: cost 1.

So E(37) = 1 + 2+2+3+1+3+1+3+5 = 21 is the least value of this calculus at 37. **CORRECT**, with
the report's own caveat: only within the calculus. Degree-4 {0}-nodes from outside it, such as a
four-level joint contraction, are UNKNOWN.

## 6. Issues (numbered)

1. **(Statement gap, material for any paper use.)** The K_L ≠ {0}, D_L ≤ κ version of
   thm:app-s2-chain is the proof's induction claim, not a stated result. Before R8's 21 replaces
   R7's 25 in the Outlook, the paper needs a one-line corollary: a chain whose last step is
   (D_L, K_L) gives, from C(a+L+1, L+1) columns, a nonzero relation with κ-classes in
   lift_κ(K_L) and one coefficient 1.
   - The proof is unchanged, with "K_L = {0}, D_L = κ" dropped.
   - The stage-plus-finish node also needs Lemmas S and F and Theorem HC, which are not in the paper
     at all (they live in the 11-12 note).
   - The report's proposed paper text (only the 4 for 127/181/433, which needs neither) is the safe
     part. The 21 needs the corollary plus HC.
2. **(Accounting gap confirmed.)**
   - R5 charges 9 at every κ = 9 prime of `NOSTD`, the list of rem:app-s2-tower-scope, although
     rem:app-s2-chains-scope already asserts chains at 109, 127, 163, 181, 199, 307 and 433.
   - The degree of those chains (4) is not recorded in the remark. The report's paper proposal to
     record it is right.
   - The same applies to κ = 8 at 89, 137 and 233 (deg[{0}] = 4), but R7 already reached 4 there.
3. **(Minor, executor.)**
   - The report's `chain_exec.py` plan p37 finishes with a K-node for {0,2,3,5}. §3 of the report
     and `witness_dump.out` describe RC(9; Z_9 → {0,2,5}). Both are valid (both lie in Tn's classes
     with ρ = 1), but the verified object is not the one printed.
   - My executor used {0,2,5}.
4. **(Minor, table.)**
   - In §2 of the report, "–" for deg[{0,2}] and deg[{0,7}] at 37 means "none with L ≤ 3".
     Length-4 chains exist, of degree 5.
   - The "none (any length)" entries for {0} are correct.
5. **(Scope.)**
   - R8 (like R7) is applied only at pairs with R5 ≥ 5, so its values elsewhere are R5 upper bounds,
     not calculus optima.
   - This cannot affect the class-9 maximum, because 37 binds with a matching floor. The c < 9 rows
     are upper bounds of the rule, for p ≤ 30000 only, as the report says.
6. **(Wording.)** §1 of the report says "−1 ∈ P_9 at every p ≡ 1 (mod 18)". That is every odd
   p ≡ 1 (mod 9), so all the relevant primes. True, but the condition is automatic.

None of these changes a number.

## 7. Adversarial self-check

- **Shared assumptions.**
  - My witness and DFS code is independent of the report's, but it shares the definition of
    classes (least primitive root). That is also the paper's convention (the existence of union
    steps depends on ξ).
  - A different ξ relabels classes by a unit u. The degrees then come from the uK tables, not
    recomputed here.
- **R5 imported.** My rule takes R5 as given. Any error in the E_2 tables or in NOSTD would
  propagate to both. This is why the 21 stays CONDITIONAL.
- **Executor coverage.**
  - a ≤ 3 and three bank shapes only.
  - A passing executor cannot prove C(t). C(t) is proved from the text (§1), and the executor only
    guards against a misreading of the proof.
- **What I did not check.**
  - The tail argument above 30000 (R7 ≤ R5 ≤ 18 above 20000) is cited from the k8 note.
  - My rule ran to p ≤ 3000 only. Between 3000 and 30000 I rely on `exponents_r8.out`, which
    lists no pair with R5 ≥ 5 above 433. There both rules reduce to R5, so no new mechanism is
    involved.
  - The SAT timeout at 73 and the certified UNSAT at 37 (three-level joint) were not rerun.
    Neither is needed for the in-calculus floor.
- **Am I anchored on the report?** The checks most likely to have found a flaw were:
  - the diff (a change in grade combination);
  - the shift-invariance and (0,0)-class questions (§1);
  - complete reachability with no length cap.

  None did.
