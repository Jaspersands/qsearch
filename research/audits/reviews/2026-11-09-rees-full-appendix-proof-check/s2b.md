# s2b: Schedule 2 tower, chains, local obstructions and scope; the 9 Nov worst-case claim

Checker s2b, 2026-11-09. AI check only; nothing here is human review.

## Header

**Scope**

- `T/appendix-schedule2.tex`:
  - 483-729: app:s2-tower, the chains subsection, the local obstructions and app:s2-scope;
  - 151-199: thm:app-s2-main, its proof and rem:app-s2-four.
- `T/main.tex`:
  - 164-172: def:input-contract;
  - 608-644: sec:recursion;
  - 690-763: Schedule 2 and the combined rule;
  - 1035-1051: the proof of Theorem main and rem:oblivious;
  - 1206-1226;
  - 1282-1334: cor:black-box-pe, thm:bb-envelope and its status line.
- `T/appendix-torsion-blackbox.tex`, read only as far as part (2) needs it: 392-450, 789-800, 834-910, 1018-1036, 1180-1218, 1300-1332, 1384-1392, 1436-1448, 1576-1584.
- Diffs: `O/diffs/appendix-schedule2.diff`, `O/diffs/patch9nov-appendix-schedule2.tex.diff`, `O/diffs/patch9nov-main.tex.diff`. I grepped these, and `O/diffs/patch9nov-appendix-torsion-blackbox.tex.diff`, for the regions above.
- Earlier reports: read only after my own pass.

**shasum**

- `appendix-schedule2.tex` 8abf0e08ebeb059ba862bf7b0c905e38b1ae3624
- `main.tex` 0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4
- `appendix-torsion-blackbox.tex` 0f89bd2386391c0277f5396de97f51d8cc0919ed

**Verdict: GAPS (fixable; statements survive).**

There is one GAP: Theorem bb-envelope makes calls of Theorem main on erroneous chart branches, and those calls are outside the input contract. Remark oblivious does not cover them. A polynomial-time input check repairs this. There are also two ERRORs in the E_2(8)/E_2(9) sentences that are marked for the E2-UPDATE pass, and seven MINOR items.

I tried to construct a bad oracle `f` and found none. The trouble comes from the computed chart, not from `f`.

**Compute and scripts.** About 18 of the 25 core-minutes were used, single-threaded, under `nice -n 19 timeout`. All scripts and outputs are in `O/s2b/`:

- `numerics.py`, `cyclo.py`, `rcsearch.py`, `counts.py`, `k10w.py`, `chart_example.py`;
- outputs `*.out`, `e2-run.log` and `rcsearch-k10.TIMEOUT`.

Finite checks can only falsify. Nothing below that passed a finite check counts as proved.

## Findings

### 1. GAP. Theorem bb-envelope: calls on erroneous charts are outside Definition input-contract, and Remark oblivious covers only in-contract inputs

**Location**

- `main.tex`:
  - 1329, the status line: "The primes with $e_p > 1$ add no condition: … Remark oblivious bounds each call with the combined rule on every oracle, as in Corollary black-box-pe";
  - 1310, thm:bb-envelope(i), whose counts hold "on every branch";
  - 1049, rem:oblivious;
  - 1225.
- `appendix-torsion-blackbox.tex`: 402-404, 442-446, 838-840, 1203-1207, 1308, 1328-1331 (lem:tb-count-grade), 1387 and 1445.

**Argument**

(a) What Remark oblivious covers. Remark oblivious (main.tex:1049, added on 9 Nov) bounds $Q_{\mathrm q}$ and the running time "for every function $f : G \to \{0,1\}^w$ with its standard oracle $U_f$". Here $G$ is the input of Definition input-contract. Part (i) of that definition, "genuine structure constants of a nilpotent Lie algebra … of class at most $c$", is a promise (main.tex:167: it "can be checked", not "is checked"). Theorem main's input is "an instance of Definition input-contract" (main.tex:190). The paper says nothing about what Theorem main does on constants that violate (i). The field-solver dispatch covers only "a socle of class $c' < c$" (torsion:402-404).

(b) How bb-envelope builds its chart. bb-envelope uses route (R2) (torsion:1306-1311). The chart is built by Lemma tb-chart from the sample matrix $Y$ of Lemma tb-kernel.

- On the failure event of Lemma tb-kernel (probability at most $\delta$), the rows of $Y$ generate a proper subgroup of $(\ker\pi)^\perp$. So $\ker Y \supsetneq \ker\pi$ need not be an ideal.
- The bracket $[Yu,Yv] := Y[u,v]$, computed through the lifts of tb-chart(b) and (d), then depends on the lifts. It need not have class at most $c$ and need not be nilpotent.
- For $e_p = 1$, where no check is made, it need not satisfy the Jacobi identity either.
- Lemma tb-chart makes "no evaluation of $\Phi$" (torsion:885-900), so nothing detects $\ker Y \ne \ker\pi$. The two size checks (torsion:1311-1315) only bound the chart sizes: at most $\lfloor\ell/\log_2 p\rfloor$ columns, and $\prod_q q^{n'_q} \le 2^\ell$. My example passes both.

(c) Explicit instance (`O/s2b/chart_example.py`, `chart_example.out`).

- Take $c = 2$, $s = 2$, and $F = F_{2,2}$ over $\mathbb{F}_p$ with Lyndon basis $x, y, z = [x,y]$.
- Let $G$ be the Heisenberg group of order $p^3$. It has class 2 and exponent $p$, so $e_p = 1$, and $\ker\pi = 0$.
- Suppose the samples span only the hyperplane $(z-x+y)^\perp$. Then $\ker Y = \langle z-x+y\rangle$, which is not an ideal, since $[x, z-x+y] = z$.
- The column scan keeps $x$ and $y$. Lemma tb-chart(d) gives $[\varepsilon_1,\varepsilon_2] = Y z = \varepsilon_1 - \varepsilon_2$.
- This algebra is antisymmetric and satisfies the Jacobi identity. But $\gamma_n = \langle\varepsilon_1-\varepsilon_2\rangle \ne 0$ for every $n \ge 2$, so it is not nilpotent. I checked this for p = 3, 5 and 7.
- Theorem bb-envelope then makes "one call of Theorem main on the chart" (torsion:1308) on an input outside Definition input-contract(i).

For $e_p > 1$, by hand only: take $G = \mathrm{Heis}_p \times \mathbb{Z}/p^2$ with the same failure. This gives the chart $(\mathbb{Z}/p)\varepsilon_1 \oplus (\mathbb{Z}/p)\varepsilon_2 \oplus (\mathbb{Z}/p^2)\varepsilon_3$, with the same bracket and $\varepsilon_3$ central.

- It passes the Lie-ring check of torsion:1196-1200: $c_{ii} = 0$, antisymmetry, torsion compatibility and Jacobi.
- Its socle $A[p] \supseteq \langle\varepsilon_1,\varepsilon_2\rangle$ carries the same non-nilpotent bracket.
- The paper itself says that this chart is "possibly of class above $c$" (torsion:1204).

(d) Why "as in Corollary black-box-pe" does not carry over.

- Before 9 Nov, the running time of these calls for $e_p > 1$ was bounded by RtF's time-out (torsion:1206: "the class bound enters only the correctness of the calls, whose running time the time-out bounds").
- The 9 Nov text deletes the time-out on the strength of Remark oblivious (torsion:444-446 and 838-840; main.tex:1296 for cor:black-box-pe).
- That is valid for cor:black-box-pe. Its chart $\mathcal{C} = F/K'$ passes the check "$K'$ is an ideal of $F$" (main.tex:1294), so the chart and all its subquotients have class at most $c$ on every branch.
- It is not valid for bb-envelope's chart. Lemma tb-count-grade assumes class at most $c$ (torsion:1330). Torsion:1387 ("For $e_p = 1$ the chart $\mathcal{L}_G = F/\ker\pi$ … class at most $c$") holds only on the success event.

So the counts of bb-envelope(i) "on every branch", and the claim that the time-out is not needed, are missing a step on these branches. For $e_p = 1$ the gap predates 9 Nov: no check or time-out ever covered that call, and "on every branch" appears on both sides of the 9 Nov diff. For $e_p > 1$ the 9 Nov change opened the gap. Even before it, the time-out bounded time and not the query formula used by torsion:1445.

**Fix** (either option is a line or two; the statements survive).

(A) Global fix. In rem:oblivious, after "whether or not $f$ hides a subgroup.", insert:

> "Before the recursion the algorithm checks Definition~\ref{def:input-contract}(i) on its input (antisymmetry, the Jacobi identity and $\gamma_{c+1}(\mathcal{L}) = 0$, at $O(c\,m^5)$ operations in $\Fp$) and returns the empty output if a check fails; so these bounds hold for every input of the format of Definition~\ref{def:input-contract}, including the calls on erroneous branches in Corollary~\ref{cor:black-box-pe} and Theorem~\ref{thm:bb-envelope}."

Then make three follow-on edits:

- torsion:1206-1207: replace "(the class bound enters only the correctness of the calls, whose running time the time-out bounds)" with "(the class bound enters only the correctness of the calls; a call on a socle of class above $c$ fails the input check of Remark~\ref{rem:oblivious} and returns nothing, within the bounds stated there)".
- torsion:1445: replace "the per-call time-out of Proposition~\ref{prop:tb-recursion}" with "the input check and the bounds of Remark~\ref{rem:oblivious}".
- torsion:1387: add "on the success event of Lemma~\ref{lem:tb-kernel}; on other branches the input check of Remark~\ref{rem:oblivious} applies".

(B) Local fix. Add "$\gamma_{c+1}(\mathcal{L}) = 0$" to the chart check at torsion:1196-1201, and apply the same check, Jacobi included, to the chart for $e_p = 1$. Every chart that reaches a call is then a Lie ring of class at most $c$, its sections and socles have class at most $c$, and Remark oblivious applies as stated. At torsion:1204, "possibly of class above $c$" becomes "of class at most $c$".

**Cost of either fix.** The check takes $O(c\,m^5)$ ring operations, with $m \le n'_p$ and at most $\sum_p n'_p \le \ell$ calls. That is $O_c(\ell^6)$ ring operations in all, below the $O(\ell^8)$ normalizer term of bb-envelope(iii). On the success event of Lemma tb-kernel the check never fires, so the error split is unchanged.

### 2. ERROR. Stale "by separate runs above the decided ranges, 14281 ∈ E_2(8)"

**Location**

- `appendix-schedule2.tex:723` (app:s2-scope, the E_2 item);
- `main.tex:721` ("by separate runs above these ranges").

**Argument**

- $14281 < 16993$, so 14281 lies inside the decided κ = 8 range.
- The phrase comes from the earlier text. There the κ = 8 range ended at 13873: "up to $13873$ … by separate runs above the decided ranges, $14281 \in E_2(8)$ and $18199 \in E_2(9)$" (`O/diffs/appendix-schedule2.diff`, hunk at its line 252). When the range was raised to 16993, the phrase was left in place.
- The κ = 9 half is still right ($20107 > 16633$).
- The E2-UPDATE (2) and (5) comments list these numbers but not this logical slip, so it could survive the update.
- The ratio $14281/8^{4.5} = 1.2327$ is correct (`counts.out`).

**Fix** (if the final numbers keep these values): "… decides every prime $p \equiv 1 \pmod 8$ up to $16993$, so that $14281 \in E_2(8)$, and every prime $p \equiv 1 \pmod 9$ up to $16633$, and shows, by a separate run above the $\kappa = 9$ range, $20107 \in E_2(9)$." Make the same change in main.tex:721.

### 3. ERROR. The independent-solver sentence contradicts four other sentences

**Location.** The sentence at appendix:723 reads: "… and the $145$ primes $p \equiv 1 \pmod 8$ in $(9769, 20000]$ that the pruned search had not decided on 4~November 2026 by a constraint solver with arc consistency …". It conflicts with:

- appendix:723: "For $\kappa = 8$ and $9$ the exceptional sets are not known exactly"; "In $(16993, 20000]$ only some primes are decided"; "Above those ranges most verdicts rest on a single run of the pruned search";
- appendix:728: "does not determine $E_2(\kappa)$ for $\kappa \ge 8$";
- main.tex:695: "so only $[3,20000]$ remains open";
- main.tex:721: "not known exactly".

**Argument**

- There are 265 primes $p \equiv 1 \pmod 8$ in $(9769, 20000]$, and 77 of them lie in $(16993, 20000]$ (`counts.out`).
- Suppose the 145 primes that the pruned search had not decided by 4 Nov were all decided by the constraint solver. Then every prime $p \equiv 1 \pmod 8$ up to 20000 has a verdict. Since $E_2(8) \subseteq [3, 20000]$ (proved in the same item), $E_2(8)$ is determined. Then "not known exactly", "only some primes are decided" and "does not determine $E_2(\kappa)$ for $\kappa \ge 8$" are all false.
- If they were not all decided, the sentence has to say which were.
- "Re-decided, with the same verdicts" also has no meaning for primes that had no earlier verdict.

This is already partly flagged. E2-UPDATE (5) (appendix:717-722) calls the sentence "new (2026-11-09 prep)" and says it "must be reconciled". E2-UPDATE (6) flags line 728, and main.tex E2-UPDATE (1) flags line 695. The sentence "Above those ranges most verdicts rest on a single run" is not flagged.

**Fix.** In the E2-UPDATE pass, change all five places together. For example, if every prime up to 20000 is decided:

- "For $\kappa = 8$ the exceptional set is known; for $\kappa = 9$ it is not known exactly";
- "In $(16993, 20000]$ the verdicts rest on the constraint solver only";
- line 728: "for $\kappa \ge 9$";
- main.tex:695: state that κ = 8 is closed.

Also separate the 145 primes from the re-decided exceptions: "… and the constraint solver … decided the $145$ primes … that the pruned search had not decided on 4~November 2026".

### 4. MINOR. Existence-only T and T_1, and the draw model of thm:app-s2-main

**Location**

- main.tex:620 (cut-off at 4T) and 1049 (rem:oblivious);
- appendix-schedule2.tex:189 (proof of thm:app-s2-main: "Let $T_1$ be an upper bound on its expected running time. Run it with a cut-off at $2T_1$ steps") and 162-163 (Phase 0 draws).

**Argument**

- Remark oblivious says, correctly, that the cut-off needs $T$ explicitly and that only a bound for a fixed implementation is shown. That is enough for the existence statements, because the constant is hard-wired into the implementation. The same holds for $T_1$, but the proof does not say so.
- Phase 0 draws "uniform elements of $\Fp^\times$" and "uniform $t \in \Fp$". With fair coins, each draw is a rejection loop with no worst-case bound. So "runs in time $(1+\kappa^\kappa)\cdot\poly(a,\kappa,\log p,k)$" is a worst-case bound only if a uniform draw counts as one step.
- Inside the recursion, the cut-off at 4T covers Phase 0 (rem:app-s2-four). So Theorem main's worst-case bounds do not depend on this.

**Fix.** At 189, after the $T_1$ sentence, add "(for a fixed implementation, as in Remark~\ref{rem:oblivious}; its constant is not computed)". In Cost, add:

> "A uniform draw counts as one step; with fair coins, cap each rejection loop at $k+2+\lceil\log_2 N_0\rceil$ tries, where $N_0 \le \kappa(k+4)+4\tau\kappa^\kappa$ is the number of draws, and abort if all fail."

Each try succeeds with probability at least 1/2, so the cap adds at most $2^{-k-2}$. The total is $2^{-k}(1/8+1/8+1/2+1/4) = 2^{-k}$, so the abort probability is still at most $2^{-k}$.

### 5. MINOR. "the Schedule 2 calls are not bounded here"

**Location.** main.tex:1312 (thm:bb-envelope(iii)) and torsion:1581 (rem:tb-count-envelope).

**Argument.** After 9 Nov, Remark oblivious bounds each Schedule 2 attempt by 4T, with $T = (1+\kappa_d^{\kappa_d})\cdot\poly(g_d,\kappa_d,\log p)$ for a fixed implementation. What is missing is only the exponent.

**Fix.** "the Schedule 2 calls are bounded only by the unspecified polynomial of Remark~\ref{rem:oblivious}, so $\hat\beta_c$ is not computed."

### 6. MINOR. N_instr is "fixed before the run under Schedule 1"

**Location.** main.tex:625.

**Argument.** Under the combined rule the arities are also fixed. The Schedule 2 retries are classical retries on fixed columns, and Remark oblivious says "there are no restarts". So $N_{\mathrm{instr}}$ is fixed there too. Restricting the sentence to Schedule 1 suggests otherwise.

**Fix.** "… fixed before the run under Schedule 1 and under the combined rule, whose arities are fixed and which have no restarts."

### 7. MINOR. κ = 7 is missing from the "1 < D_1 < κ" sentence

**Location.** appendix-schedule2.tex:647 (rem:app-s2-chains-scope, Small primes).

**Argument**

- The list in rem:app-s2-tower-scope for κ = 7 is {29, 43, 71, 113}.
- After removing the no-chain primes 29 and 71, "the other primes" 43 and 113 cannot have $1 < D_1 < 7$, because 7 is prime. Their chains are the three-step chains $\mathbb{Z}_7 \to u\{0,1,2\} \to u\{0,1\} \to \{0\}$ of the same paragraph.
- Chain-graph search (`rcsearch-chains.out`):
  - at 43: $\mathbb{Z}_7\to\{0,1,2\}\to\{0,2\}\to\{0\}$;
  - at 113: $\mathbb{Z}_7\to\{0,1,2\}\to\{0,1\}\to\{0\}$.
- `rcsearch-k7.out` reproduces the failure sets for u = 1 and u = 2 below 3300.

**Fix.** "… and finds chains at the other primes of those lists: the chains above at $p = 43, 113$ for $\kappa = 7$, and chains with $1 < D_1 < \kappa$ at $p = 67$ for $\kappa = 6$, $89, 137, 233$ for $\kappa = 8$, and $109, 127, 163, 181, 199, 307, 433$ for $\kappa = 9$."

### 8. MINOR. Typo: ρ for ρ_2

**Location.** appendix-schedule2.tex:541 (proof of prop:app-s2-step-threshold(ii)).

**Fix.** "$\Pr[n_j = 0] \le 1 - 1/\rho_2$".

### 9. MINOR. k is overloaded in the chains subsection

**Location.**

- 487 declares $k = |K|$;
- 563 and 573 use $k \in K$ inside $\bigcup_{k\in K}Q^{(D)}_{k-i-j}$;
- 591 (proof of thm:app-s2-chain) uses $k$ as the round index ($V_k$, $c^{(k)}$, $k^\ast$, $\tau_k$, $\gamma_k$).

**Fix.** Write $\bigcup_{h\in K}Q^{(D)}_{h-i-j}$ at 563 and 573, and rename the round index at 591 to $s$.

## Checked and correct

### Part 1: appendix-schedule2.tex 483-729

- **Notation (487) and def RC(D;R) (490).** Coset notation $P_D$ and $Q^{(D)}_m$; with $R = \mathbb{Z}_D$ the definition gives the two-level normal form of Lemma normal.
- **lem:app-s2-refine (494).** Proof read: the $(r-1)a \times N$ elimination, the coset tests and the class bookkeeping. No issue.
- **thm:app-s2-tower (509).** The arity $(a+1)\prod_t((r_t-1)a+1)$ follows by induction over refine. For $t = 1$, "$p \notin E_2(D_1)$" is correct. No issue.
- **prop:app-s2-step-threshold (522).**
  - (i) $W(4,2) = 96.34$, $W(6,2) = 648.78$ and $W(8,2) = 2432.89$, each below $((D-1)^2+1)^2$.
  - (ii) Sweep over D = 4..60 and r = 2..D at $p_0 = \max(4D^{r+1},4r^2D^5)$: no failure. The largest value of $(\text{first}+E_r)(D-1)$ is 0.335 < 1. The constant $1.1251\,e^{0.2502}/2 = 0.7225$ is correct (`numerics.py` §1).
  - Only issue: finding 8.
- **cor:app-s2-tower (545).** Read; no issue.
- **rem:app-s2-tower-scope (560).** Every list was reproduced by complete searches:
  - κ = 4 below 97: {5, 13};
  - κ = 5 at the primes of E_2(5): {11}, for every u, hence for every ξ;
  - κ = 6 below 649: {7, 13, 19, 31, 43, 67};
  - κ = 8 below 2433: {17, 41, 73, 89, 137, 233};
  - κ = 9: the tower 1|3|9 fails below 135000 exactly at the 10 listed primes and at 271, 379, 487, 523, and a union chain exists at each of those four;
  - no listed construction exists at 19, 37, 73, 109 or 127 for κ = 9 (complete search; `rcsearch-tower*.out`, `-k9-phase1.out`, `-k9b.out`, `-k9c.out`).

  The degree L+1 and "quadratic only for L = 1" are correct. "All listed primes lie in $E_2(\kappa)$" is consistent.
- **thm:app-s2-chain (584).** The round construction at 591 is correct:
  - the codimension drops by one per round, so $k^\ast \le m$;
  - $\sum_{j\le m}\binom{j+t}{t} = f_t(m)$;
  - the class identity $n + i(b) + (K - i(b) - n) = K$ holds;
  - the back-substitution through $\tau_k$ ends with value $-\tau_0 \in U$ and designated weight 1.

  Only issue: finding 9.
- **prop:app-s2-union-step (597).**
  - $\Delta_U$ follows from the Weil bound: $|N_{ij}(c) - c_0^2(p-2)| \le 2c_0G + G^2\sqrt p$, and $c_0^2(p-1)^2/p - c_0^2(p-2) = c_0^2/p$.
  - The second moment and the Cauchy–Schwarz step are correct.
  - (ii) Over 60,923 cases of (D, K, r): no failure, and the largest $\Psi_U(p_0)$ is 0.491 < 0.73. The interval bounds on G and H hold (`numerics.py` §2).
  - Note on 620: the factor $(p/(p-1))^2 \le 1.0203$ needs p ≥ 101, since $(100/99)^2 = 1.020304$. p is prime, so p ≥ 100 forces p ≥ 101 and the bound holds. Writing "Since $p \ge 101$" would make this explicit.
- **cor:app-s2-union-chain (624).**
  - $\min_k\Theta^{\mathrm{cf}}_2$ recomputed: $2.205\cdot10^5$ at κ = 5 and $1.681\cdot10^6$ at κ = 7. These match main.tex:726 ("about $2.2\cdot10^5$ and $1.7\cdot10^6$").
  - At κ = 16, 17, 18, 19, 20, 25, 30 and 40:
    - $\Theta^{\mathrm{cf}}_2 \le 4.05\kappa^2(\ln\kappa)^\kappa$ holds;
    - the proof's inequality $\ln(2.9\kappa)+8\ln(1.2+\ln\kappa) \le \kappa\ln\ln\kappa$ holds (at 16: 14.873 ≤ 16.317);
    - the bound is below $\kappa^{\kappa/2}$ from κ = 19 on (27.806 < 27.972 in logarithms) and fails at κ = 16 to 18, as the text says. For κ ≥ 19 the log-difference is increasing.
- **rem:app-s2-chains-scope (636).**
  - Values check:
    - $\Theta_2$ = 3781, 30823, $1.16\cdot10^6$, $7.42\cdot10^6$ and $\Theta_3$ = 1217, 15133, $3.80\cdot10^5$, $1.06\cdot10^6$ for κ = 5, 7, 11, 13;
    - the binding step at κ = 5 and 7 is $T_R(\kappa,3)$;
    - $(\kappa-1)\kappa^\kappa$ is correct;
    - $T_R(9,3) = 1.3472\cdot10^5 < 135000$ (floating point) and $W(9,3) = 1.479\cdot10^6$;
    - the logarithmic-derivative monotonicity argument for $T_R$ is correct.
  - Small primes:
    - BFS finds no chain at 5, 13 (κ = 4), 11 (κ = 5), 7, 13, 19, 31, 43 (κ = 6), 29, 71 (κ = 7) and 17 (κ = 8);
    - chains exist at 67 (κ = 6, with $D_1 = 2$) and at 43 and 113 (κ = 7);
    - the u-failure sets for κ = 7 are reproduced below 3300.
  - The barrier bound first drops below 1 at a' = 146 (κ = 4, p = 17, h' = 2; the value at 145 is 1.2447).
  - Only issue: finding 7.
- **lem:app-s2-two-rows (662).** Read; no issue.
- **prop:app-s2-cyclotomic (671).**
  - (i) The sets were recomputed from the cyclotomic numbers for κ = 3..16: κ = 3 empty; κ = 4 {5, 13, 29}; κ = 5 {11}; κ = 6 largest 223; κ = 7 {29, 43, 71}; κ = 8 largest 761; κ = 9 largest 163.
  - Every set lies below 15κ² (closest: κ = 14, 2927 < 2940). Each contains the primes of (ii) and the no-chain primes.
  - (iii) The bound is never violated. The κ = 7 threshold of 940 is correct (−0.29 at 939, +0.22 at 940; `cyclo.py`).
- **lem:app-s2-divisor (693).** Correct.
- **rem:app-s2-local-scope (704).** Consistent with the sets above. The κ = 10 exceptions 3361, 3761 and 5821 have verified contractions (`k10w.out`).
- **app:s2-scope (711).**
  - $E_2(4) = \{5,13,17,29,37,53\}$ and $E_2(5) = \{11,31,41,61,71,101,131,151,181\}$, complete up to $\lceil T_A\rceil$. With nonzero entries required, they grow by {61} and by {191, 211, 241, 251}.
  - $E_2(6)$ has 53 primes, the largest 859, complete up to $\lceil T_A(6)\rceil = 233578$ (`rcsearch-e2.out`).
  - The symmetric form for κ = 3 fails exactly at {7, 13, 19, 61} below 400, with or without zero entries.
  - $T_A(3..9)$ checks: $\lceil T_A(8)\rceil = 117441563$ and $T_A(7) = 4.94\cdot10^6 < 5\cdot10^6$. $T_S(3..8)$ also checks.
  - Every quoted prime is a prime ≡ 1 (mod κ).
  - The counts 83/83, 137/122, 1534715 and 1791117, and the ratios 1.23 and 0.34, are correct (`counts.out`).
  - Only issues: findings 2 and 3.

### Part 2: the 9 Nov worst-case claim

- **Per attempt (main.tex:620).**
  - Markov at the 4T cut-off gives probability at most 1/4 of exceeding it.
  - thm:app-s2-main at k = 2 aborts with probability at most 1/4.
  - By the union bound an attempt fails with probability at most 1/2.
  - An abort or cut-off costs only probability, because the output is checked exactly before it is returned (appendix:187).
- **Independence across attempts.** Each attempt uses fresh coins and runs Phase 0 inside it (rem:app-s2-four), so given the node's columns the attempts fail independently.
  - This is necessary. A Phase 0 shared by the attempts would cause a common failure of up to $2^{-k-2} = 1/16$.
  - With $\lceil\log_2(3N_{\mathrm{solver}}/\eps)\rceil$ attempts each node fails with probability at most $\eps/(3N_{\mathrm{solver}})$, and the union over nodes gives $\eps/3$, the solver third.
- **Fixed before the run.** The recursion tree, the arities $M_d$, the number of Fourier transforms, $N_{\mathrm{solver}}$ and $N_{\mathrm{instr}}$ are fixed by $(p, m, g_d, \eps)$. There are no restarts: the Schedule 2 retries are classical and run on fixed columns.
- **Hiding is needed only for correctness.**
  - The rank steps use a fixed number of samples.
  - Schedule 1 returns scalars for every label tuple, since is-import holds for arbitrary $\lambda_i$.
  - Schedule 2 accepts any columns.
  - Labels ≥ p are reduced mod p, so every column lies in $\Fp^a$.
  - The block-steered and mixed option with restarts (prop:mixed-schedule) is not part of the claim.
- **Oracle attacks tried, none successful.**
  - label values ≥ p;
  - degenerate or adversarial columns: zero, repeated, rank-deficient;
  - a non-hiding $f$ in the rank steps;
  - an $f$ that makes RtF's stop rules fire as late as possible (at most b calls).

  No $f$ gives an unbounded or uncounted cost.
- **cor:black-box-pe (main.tex:1292-1296).** Deleting its time-out is valid: $K'$ is ideal-checked, so every chart and every section has class at most c on every branch.
- **Explicit T.** It is not available, and rem:oblivious says so honestly (see finding 4 for $T_1$).
- **thm:bb-envelope.** After the repair of finding 1, (i) and the status line follow. The same holds for main.tex:1225: bb-envelope then needs, beyond Theorem is-import, only power-sde(ii) through the combined rule, and not ring-to-field(iii), for $e_p > 1$.

## Not checked / UNKNOWN

- **κ = 9 small primes.**
  - At 163 and 181 the search was partial: 15 and 12 of 37 constructions hit the node limit.
  - 199, 307 and 433 were not run (time cap).
  - The chains with $1 < D_1 < \kappa$ for κ = 9 (109..433) and κ = 8 (89, 137, 233) were not searched.
  - No chain-graph search was run at 41 or 73 (κ = 8) or at 19, 37, 73 (κ = 9). At 19, 37 and 73 none of the 37 constructions exists, but BFS over all chains was not run.
- **κ = 7.** The list {29, 43, 71, 113} needs $E_2(7)$ (56 primes, largest 3221) and union chains with |K| up to 4 at every one of those primes. Neither was run. $E_2(7)$ itself was not reproduced.
- **E2-UPDATE numbers.** The E_2(8) and E_2(9) verdicts were not re-derived, as instructed; only counts and residues were checked.
- **E_2(10) and E_2(12) (line 707).** Only the three κ = 10 exceptions were checked. The exhaustive κ = 10 and κ = 12 runs timed out at 200 s (`rcsearch-k10.TIMEOUT`), so the result is UNKNOWN.
- **Symmetric form, κ = 3.** Not searched for p ≥ 400. If the text means "exactly these four primes", the range up to $4\cdot3^8 = 26244$ is unchecked here.
- **T_R(9,3).** Evaluated in floating point only. It sits 277 below 135000.
- **Cited bounds.** Not re-proved:
  - the Weil bound for $X^s(X+c)^t$;
  - the cyclotomic-number and Jacobi-sum bounds;
  - the argument of prop:app-s2-barrier (line 417, outside my range; only its number at 653 was checked);
  - the Lean module ReesS2Local;
  - the provenance items.
- **Part 2.** I did not check the internals of Prop tb-recursion and Lemma tb-section-rank beyond the call count and stop rules, or the full proof of Lemma tb-chart. The $e_p > 1$ variant of the finding-1 example was checked by hand, not by script.

## For the human expert

1. **Finding 1.** Should the input check go into Theorem main (rem:oblivious) or into bb-envelope's chart step? And does any other caller feed Theorem main out-of-contract inputs on erroneous branches?
2. **Existence-only cut-offs.** Is a bound T (and $T_1$) known to exist for a fixed implementation, but not computed, acceptable for the cut-offs in the stated theorems? I think it is for existence statements.
3. **Randomness model.** Should a uniform draw from $\Fp$ count as one primitive step, or are coins fair (finding 4)?
4. **Weil bound.** The bound for multiplicative character sums of $X^s(X+c)^t$ (union-step, step-threshold) and the bounds behind prop:app-s2-cyclotomic(iii).
5. **Thresholds close to search limits.** $T_R(9,3) \approx 134723$ against the search bound 135000 (margin 0.2%). An interval-arithmetic evaluation is advisable.
6. **Finite computations.** The final E_2(8) and E_2(9) computations, including the 145-prime constraint-solver run, after the E2-UPDATE pass.

## Comparison with the earlier report(s)

**2026-11-03 app-a report** (it covered the earlier 474-line appendix).

- Its P2 and P4 fixes are present and correct.
- Its E_2(6) check covered [13, 571]. My complete run to 233578 confirms the full 53-prime set, including the 11 primes from 577 to 859.
- Its remark that reusing Phase 0 is harmless concerns output correctness only. A Phase 0 shared by a node's attempts would correlate their aborts. The current text runs Phase 0 inside every attempt, which avoids this.

**2026-11-09 referee report** (its Schedule 2 / Task 3 part).

- Its fixes G2.1-G2.4 and the explicit-T note are present and correct: main.tex:620, rem:oblivious, rem:app-s2-four, and the 4T cut-off at k = 2.
- It missed finding 1. Its row "every section met … socle … class ≤ c" and its §2.3 point on cor:black-box-pe hold for $F/K'$, but not for bb-envelope's (R2) chart.

**README 328-407.** Its "exactly as cor:black-box-pe argues" inherits the gap of finding 1. The rest agrees with the tree.
