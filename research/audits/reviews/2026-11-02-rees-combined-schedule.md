# Rees composition: combined per-grade SDE schedule (valid for every p > c)

AI session only (Claude Code, 2026-11-02). No human review. This note edits nothing else.
It builds on `2026-11-01-rees-core-proof-check.md` (steps 1–5 proved under Schedule 1;
§4 handoff, §5.1–5.5 schedule checks, §6 envelope) and `docs/papers/rees-hsp/main.tex`
lines 394–456 and Table `tab:main-regimes` (line 184).

Script and output: `2026-11-02-rees-schedules/combined/combined_budget.py`,
`combined_out.txt`. Reproduce (about one minute):

```bash
cd research/audits/reviews/2026-11-02-rees-schedules/combined && /opt/anaconda3/bin/python -u combined_budget.py > combined_out.txt
```

## 0. Verdict

- **Rule W (worst-case combined rule): holds.** It is valid for every prime p > c and every
  H, uses no label law and no hidden quantity, and takes its arity per grade from public
  (p, d, g_d). Its proof only puts together pieces already checked on 11-01. The query
  count at the class-9 profile drops from 2^1572.7 (Schedule 1 as written) to anywhere
  between 2^1562.3 and 2^61.5, depending on p (§3).
- **Most of the saving at small p comes from the gcd reduction, not from Schedule 2.**
  Running Schedule 1 at the reduced degree κ_d (arity B_{κ_d}(g_d), and g_d + 1 when κ_d = 1)
  is already valid for every p > c (11-01 §5.3, Bezout runs). main.tex allots B_d(g_d)
  instead. Schedule 2 adds savings only from p ≥ 1024 on (the κ = 2 threshold).
- **The worst case over primes barely moves.** At fixed c, the exponent of m in the query
  count, maximised over all p > c, is unchanged for c ≤ 7. For c = 8 and c = 9 it falls by 2
  (109 → 107, 145 → 143), because no prime ≡ 1 mod lcm(2..c) lies below 1024 (§3.3). The
  paper's "exponent at most 145" stays true; 143 is the sharp worst case under W.
- **Rule W+3 (adds Schedule 3 per grade): holds as a query/time trade, not as a
  polynomial-time algorithm.** At the class-9 profile it brings queries down to about 2^46–2^53
  for p ≥ 5281, but needs up to 2^128 classical rejection trials per node (§3.2). In a mixed tree, the
  paper's arity 4u_d must sometimes be raised (from public data) because lower grades
  multiply the node count (§2.4).
- **Not given:** small arity at primes below the thresholds. At κ_d = p − 1 (only possible
  when d = c = p − 1), every worst-case schedule needs at least a_d(p−1)+1 columns
  (Davenport/Olson; thm:power-sde (iii)). This was checked by brute force (§4).

## 1. The combined theorem

**Setting and access model** (unchanged from main.tex Theorem main and 11-01 §4). G is a
finite p-group of class c < p, given as the Lazard Lie algebra L over F_p (structure constants
known, so m = dim L and every g_d = dim γ_d(L) are public), with a hiding oracle f for an
arbitrary H ≤ G (or coset-copy input). One lifted source costs c queries. κ_d := gcd(d, p−1).
Hidden and never used to choose anything: H, h, K_d, a_d = g_d − dim(h ∩ γ_d).

**Rule W.** Before any quantum step, set for each grade d = 2..c:

| condition (public) | schedule | arity M_d | solver |
|---|---|---|---|
| κ_d = 1 | linear (thm:power-sde (i); also B_1 = a+1) | g_d + 1 | deterministic: nullspace, then s_i = y_i^t with t·d ≡ 1 mod p−1 |
| κ_d ≥ 2 and p ≥ 16κ_d^{2κ_d+2} | Schedule 2 | (g_d+1)((κ_d−1)g_d+1) | Las Vegas, abort ≤ 2^{−k} |
| κ_d ≥ 2 and p < 16κ_d^{2κ_d+2} | Schedule 1 at degree κ_d | B_{κ_d}(g_d) (≤ B_d(g_d)) | deterministic (IS §3.1–3.3), Bezout lift x ↦ x^t, t·d ≡ κ_d |

Theorem W (conditional only on the 11-01 checks of steps 1–5, Schedule 2, and the Bezout
lift; all AI-only). For every prime p > c, every H ≤ G and every ε ∈ (0, 1), the composition
of main.tex §sec:recursion with arities M_d from Rule W outputs h with probability ≥ 1 − ε,
using

- S = m + t terminal samples, t = ⌈log_p(3/ε)⌉; P = Π_{d=2}^c M_d sources per sample;
  Q = c·S·P oracle queries (or c·S·P coset copies);
- N_merge = S·Σ_d n_d merges, with n_d = Π_{2≤d'<d} M_{d'}; N_S2 = S·Σ_{d∈S2} n_d Las Vegas
  calls, each capped at abort 2^{−k}, k = ⌈log₂(3N_S2/ε)⌉, at cost (1+κ_d^{κ_d})·poly(g_d, κ_d, log p, k);
- N_instr = S·P + N_merge + S complete instruments, each within ε/(3N_instr);
- classical time per S1 merge poly_{κ_d}(B_{κ_d}(g_d), log p), and per linear merge
  O(g_d M_d²) field operations plus one exponentiation per coordinate.

The error is rank + solver + approximation ≤ ε/3 + N_S2·2^{−k} + ε/3 ≤ ε. If there is no S2
grade, the solver term is 0 and the total is ≤ 2ε/3. At fixed c, Q is polynomial in
(m, log(1/ε)) with m-exponent 1 + Σ_d e_d(p), where e_d = 1 (κ_d = 1), 2 (Schedule 2) or
κ_d⌈log₂(κ_d+1)⌉ (Schedule 1). This is at most 1 + Σ_d d⌈log₂(d+1)⌉ for every p, and
at most 143 at c = 9. No step is polynomial in p.

**Rule W+3 (optional).** Additionally let grade d use Schedule 3 with
u_d = max(2, κ_d, g_d+1) when p ≥ 16u_d² and 4u_d < the Rule-W arity. Run tree restarts as in
thm:random-column (ii): 4m' trees, m' = m + ⌈log₂(3/ε)⌉, keep the first m' successes. This
needs the label law (supplied, §2.3), and costs 4κ_d^{M_d}·B rejection trials per S3 node:
classical time 2^{O(u_d log u_d)}, not polynomial unless every g_d = O(log m / log log m).
Use W+3 only when its public Q is smaller than W's. It is not always: c = 3, p = 1031 gives
2^12.8 against 2^10.6, because 4m' trees replace m + t samples.

## 2. Proof

### 2.1 The choice uses public data only (question 1)

κ_d is a function of (p, d). The thresholds 16κ^{2κ+2} and 16u_d² depend on (p, d, g_d).
The arities use g_d, which is an upper bound on the observed rank a ≤ a_d ≤ g_d. Every
schedule's guarantee is stated for columns in F_p^r with r = g_d, so no a_d is needed:

- Schedule 1 (IS) and the linear case are worst-case for all columns in F_p^{g_d}.
- Schedule 2's construction (11-01 §5.4) runs on any (r+1)((κ−1)r+1) columns in F_p^r; take
  r = g_d.
- Schedule 3 needs a_d ≤ u_d − 1 and κ_d ≤ u_d; u_d = max(2, κ_d, g_d+1) gives both. The
  "observed rank exceeds the bound → abort" branch of main.tex never fires, since rank ≤ g_d.
  The paper's tree-wide choice u = max(c, max_{d≥2} g_d + 1) = max(c, g_2 + 1) is also
  public (u = 18 at class 9).

The arities have to be fixed before the bank is prepared, which is why g_d is used rather than
the observed rank. The tree shape under W is a deterministic function of (p, c, g, ε).

### 2.2 Each grade's schedule is valid on its own

- Linear (κ_d = 1): g_d + 1 columns have a nonzero dependence y; s_i = y_i^t with td ≡ 1 mod
  p−1 gives s_i^d = y_i. Deterministic.
- Schedule 1 at degree κ_d: κ_d | p−1, so IS §3 applies at degree κ_d with B_{κ_d}(g_d)
  columns. The lift s_i = y_i^t, td ≡ κ_d (mod p−1), gives s_i^d = y_i^{κ_d} for y_i ≠ 0 and
  keeps zeros, so a nonzero witness stays nonzero. 11-01 §5.3 checked this exactly
  ("Bezout: … M = 64 (B_d = 2.8e14)"). B_κ(a) ≤ B_d(a) for κ | d (`arity_order_check`).
- Schedule 2: 11-01 §5.4 (written check, no gap), under p ≥ 16κ_d^{2κ_d+2}.
- Schedule 3: 11-01 §5.5. Per node, the bank is bad (N < EN/2 or rank < a_d) with probability at most
  4/μ_d + 2p^{a_d−M} ≤ q_d := 4h p^{g_d}/((h+1)^M − 1) + (p^{g_d}−1)/((p−1)p^M). Here h =
  (p−1)/κ_d, and the bound is increasing in a, so q_d is a public bound. Outside the bad event,
  acceptance is ≥ 1/(4κ_d^M), which needs only p ≥ 2κ_d.

Rule W never picks Schedule 1 where Schedule 2 is allowed, because (a+1)((κ−1)a+1) < B_κ(a)
for every κ ≥ 2 (checked for κ ≤ 12, a < 200; in general B_κ(a) ≥ κ^{κ(κ−1)}(a+1)^{2κ} > κ(a+1)² ≥ the Schedule-2 arity).

### 2.3 Mixed trees: the channel guarantee and the label law per grade (question 2)

Fix a stage-d node. Its M_d inputs are the outputs of M_d distinct stage-(d+1) nodes (or
fresh lifted sources if d = c), prepared from disjoint fresh sources.

1. *Inputs are exact.* By 11-01 §4 / (2c)–(2d), a stage-(d+1) node that accepts *any*
   nonzero witness outputs exactly ρ_{H_d} on G_d, for every label tuple, every witness and
   every record. This holds whichever schedule produced the witness: the channel only sees
   s. A Schedule-2 or Schedule-3 node that aborts outputs nothing, and the run (W) or tree
   (W+3) aborts.
2. *Conditioning is harmless.* The output state equals ρ_{H_d} conditioned on every record
   value, so conditioning on any event of the records (no abort so far, a particular witness,
   the Las Vegas trial count, a Schedule-3 acceptance) leaves the joint input state
   ρ_{H_d}^{⊗M_d}, independent of all earlier classical data. Different children use
   disjoint sources, so the product form holds (no correlated banks; Prop. 299 is avoided
   because independence comes from disjoint fresh preparation).
3. *Label law at grade d.* Measuring Z_d on ρ_{H_d}^{⊗M_d} gives labels i.i.d. uniform on
   K_d^⊥ (11-01 §4), independent of all records at grades > d. Schedule 3 at grade d needs
   exactly this, so it is valid at grade d whatever grades > d used. Schedules 1 and 2 and
   the linear case need no law.
4. *Classical retries* (Schedule-2 Las Vegas restarts, Schedule-3 rejection trials) reuse
   the saved labels of the same node and consume no sources ("Classical retries reuse
   measured labels, not consumed quantum copies"). No dilation is applied before a witness is
   accepted.

So every grade's guarantee holds in a mixed tree. Item 2 is the only new step. It is
the same argument 11-01 §5.5 uses for "kept trees still output i.i.d. ρ_{th}".

### 2.4 Error budget for mixed trees (question 3)

*W.* Hybrid over complete instruments, as in main.tex §sec:recursion. The ideal process
(exact instruments, uncapped solvers) is exactly correct by 2.3. The real process differs
from it only on (i) rank failure ≤ (p^m − 1)/((p−1)p^S) ≤ ε/3; (ii) some S2 abort, ≤ N_S2·2^{−k}
≤ ε/3; (iii) approximation ≤ N_instr·ε/(3N_instr) = ε/3. S1 and linear grades contribute 0
to (ii). The Markov route of main.tex (expected time T, cutoff 2T, ⌈log₂(3N_solver/ε)⌉ attempts)
applies equally, because Schedule 2's time bound is worst case over column tuples.

*W+3.* Per tree, abort ≤ (3n_S3 + n_S2)·2^{−B} + Σ_{d∈S3} n_d q_d, with
n_S3 = Σ_{d∈S3} n_d and B = ⌈log₂(64(3n_S3 + n_S2))⌉. The first term is ≤ 1/64. **New
point:** in a mixed tree, n_d at a Schedule-3 grade includes the arities of all lower grades,
which can be huge (at class 9, p = 2521, grade 6 sits above Schedule-1 grades 3–5 with
arities up to 2^125). With M_d = 4u_d the bank term can then exceed 1/64. thm:random-column (ii)'s
bound "≤ 2^{−6u} over ≤ (4u)^{c−1} nodes" assumes a uniform 4u tree and does not transfer.
Fix: raise M_d one column at a time (public data: q_d is computed with a_d → g_d) until
Σ n_d q_d ≤ 1/64. The script does this; at p = 2521 grades 6 and 7 go from 40 to 43 and from 28 to 41.
Then tree abort ≤ 1/16, Hoeffding on 4m' trees gives < m' successes with probability
≤ e^{−3.78m'} ≤ 2^{−2m'} ≤ ε/3, rank ≤ ε/3 with m' ≥ m + t samples, and approximation ε/3
spread over trees·(P + Σ n_d + 1) instruments. Kept trees are i.i.d. by 2.3 item 2.

## 3. Recomputed budget (exact; `combined_out.txt`)

Check first: Schedule 1 as written reproduces main.tex at the class-9 profile (S = 20,
⌈log₂Q⌉ = 1573, ⌈log₂N_instr⌉ = 1570, η bits 2066).

### 3.1 Class-9 profile g = (19, 17, 16, 14, 12, 9, 6, 3, 1), ε = 1/3 (t = 1, S = 20)

log₂Q. "S1-gcd" = Schedule 1 at B_{κ_d}. "W+3 trials" = max log₂ rejection trials per S3 node.

| p | κ_2..κ_9 | S1 (paper) | S1-gcd | **W** | W schedules | W+3 (trials) | S3-tree (u = 18) |
|---|---|---|---|---|---|---|---|
| 11 | 2,1,2,5,2,1,2,1 | 1572.7 | 202.1 | **202.1** | S1 lin S1 S1 S1 lin S1 lin | = W | n/a (p < 5184) |
| 13 | 2,3,4,1,6,1,4,3 | 1572.7 | 401.2 | **401.2** | S1 S1 S1 lin S1 lin S1 S1 | = W | n/a |
| 31 | — | 1572.7 | 407.4 | **407.4** | — | = W | n/a |
| 1031 | 2,1,2,5,2,1,2,1 | 1572.7 | 202.1 | **167.3** | S2 lin S2 S1 S2 lin S2 lin | = W | n/a |
| 2521 | 2,3,4,5,6,7,8,9 | 1572.7 | 1572.7 | **1562.3** | S2, then S1 at 3..9 | 281.4 (2^127) | n/a |
| 5281 | — | 1572.7 | 862.7 | **852.3** | — | 50.3 (2^128) | 59.1 (2^224) |
| 105019 | — | 1572.7 | 286.0 | **222.0** | — | 46.3 (2^115) | 59.1 (2^194) |
| 2^31−1 | — | 1572.7 | 995.9 | **944.9** | — | 50.9 (2^122) | 59.1 (2^236) |
| 2^61−1 | 2,3,2,5,6,7,2,9 | 1572.7 | 1117.4 | **555.4** | S2 at 2..8, S1 at 9 (κ = 9 needs 1.9e20) | 52.9 (2^128) | 59.1 (2^236) |
| 194522647344910884721 (≡ 1 mod 2520, > 16·9^20) | 2..9 | 1572.7 | 1572.7 | **71.1** | S2 everywhere | 52.9 (2^128) | 59.1 (2^236) |
| 2^127−1 | — | 1572.7 | 995.9 | **61.5** | — | 49.9 (2^115) | 59.1 (2^236) |

W error split, for example at p = 2^61−1: rank 1.9e−37, solver 0.108 (N_S2 = 6.2e16,
k = 59), approximation 0.111; total ≤ ε. At ε = 10^{−6}: k = 78, solver 2.1e−7, η bits 1067.
Every row passes total ≤ ε (asserted in the script).

### 3.2 Small cases (log₂Q, ε = 1/3)

| (c; g) | p | S1 (paper) | W | saving | note |
|---|---|---|---|---|---|
| 2; (4,3) | 3, 5, 7 | 13.6 | 13.6 | 0 | κ_2 = 2 < 1024; p = 3 is the zero-sum case |
| 2; (4,3) | 1031 | 13.3 | 7.3 | 6.0 | S2 at grade 2 |
| 3; (6,4,2) | 5 / 11 | 34.9 / 34.7 | 17.5 / 17.3 | 17.4 | κ_3 = 1 (linear) |
| 3; (6,4,2) | 7 / 13 | 34.9 / 34.7 | same | 0 | κ_d = d, p < 1024 |
| 3; (6,4,2) | 1031 / 105019 | 34.7 | 10.6 / 12.9 | 24.1 / 21.8 | W+3: 12.8 / 14.8 (worse) |
| 4; (8,5,3,1) | 5 / 7 / 13 / 1033 | 87.2 / 87.2 / 87.0 / 87.0 | 67.7 / 45.2 / 87.0 / 79.8 | 19.5 / 42.0 / 0 / 7.2 | p = 13: κ = (2,3,4) |
| 5; (10,7,5,3,1) | 7 / 11 / 31 / 1031 | 189.6 / 189.4 / 189.5 / 189.4 | 55.9 / 117.0 / 139.5 / 103.0 | 133.7 / 72.4 / 50.0 / 86.4 | |

### 3.3 Where W saves nothing

- **Over Schedule 1 as written (B_d):** exactly when κ_d = d for every d ≤ c (that is,
  lcm(2..c) | p−1) and p < 1024. Examples: c = 2, every p < 1024; c = 3, p ≡ 1 mod 6 below
  1024 (82 primes ≤ 3000, all < 1024); c = 4, p = 13. At c = 9 this never happens, since the
  first prime ≡ 1 mod 2520 is 2521 > 1024: every prime saves something, from 10.3 bits
  (p = 2521) up.
- **Over S1-gcd:** for every p < 1024 (κ = 2 is the smallest threshold, 16·2^6 = 1024).
  Scan: no saving at all 168 primes 11 ≤ p ≤ 1021 for class 9; the first saving is at 1031.
  From p ≥ 1031 on, grade 2 always uses Schedule 2 (κ_2 = 2 for odd p).
- **Worst-case m-exponent over p** (g_d = m at every grade): paper 5, 11, 23, 38, 56, 77, 109,
  145 for c = 2..9. Under W the worst prime is the least prime ≡ 1 mod lcm(2..c), and the
  exponents are 5, 11, 23, 38, 56, 77, 107, 143. Checked against every prime < 2·10^5; above
  that, κ_2 and κ_3 are both past their thresholds and the exponent is smaller.

## 4. What the combination does not give (question 4)

Below the thresholds, W falls back to IS arity B_{κ_d}(g_d) = 2^{Θ(κ log κ · log g)}. It
does not give polynomially small arity there. That is the parallel session's question, and
this note does not answer it. One part of it is a genuine obstruction:

**Zero-sum obstruction (thm:power-sde (iii)).** κ_d = p−1 needs (p−1) | d with d ≤ c < p,
so it happens only at d = c = p−1. There every nonzero s^d equals 1, and a witness is a
nonempty zero-sum subsequence of the columns in F_p^{a_d} ≅ C_p^{a_d}. The multiset
{e_j repeated p−1 times : j ≤ a} has none, so every worst-case schedule needs
M ≥ a(p−1)+1 = D(C_p^a) (Olson's theorem for p-groups gives equality). Brute force
(`zero_sum_obstruction`) confirms no witness for (p, a) = (3,1..3), (5,1..2), (7,1..2), including
the paper's p = 5, a = 2 example (8 columns, 9 suffice). Rule W uses B_{p−1}(g_c) there
(2^48 at p = 5, a = 1). Worst-case arity cannot go below a(p−1)+1 = κa+1, the
Chevalley–Warning count. Whether a zero-sum subsequence can be *found* in polynomial time
from a(p−1)+1 columns is left UNKNOWN here.

**Remark for the parallel session (not part of either rule).** The Schedule-3 second-moment
step (Var N ≤ h·EN, by pairwise independence of non-proportional kernel vectors under a
uniform label matrix) holds at every prime. p ≥ 16u² is used only to make μ large at the fixed
arity M = 4u. With M chosen from the exact public bound q_d ≤ 1/64, a single node works at small
primes (`s3_without_prime_condition`): p = 5, κ = 4, g = 3 needs M = 15 (worst-case floor 13);
p = 7, κ = 6, g = 2 needs M = 14 (floor 13). The per-trial acceptance is only
((h+1)^M − 1)/(2p^M), so classical time is exponential in M. This gives small *query* arity
at small primes only for i.i.d. banks and only at exponential classical cost. It is not a
polynomial-time route, and the tree budget of §2.4 would still have to be redone.

## 5. Table `tab:main-regimes` wording that would match

Replace the first two rows by one row (and keep the random-column row):

| Regime | Prime condition | SDE schedule | Sources per terminal sample |
|---|---|---|---|
| Fixed class c (combined) | all p > c | per grade: linear if κ_d = 1; two-level symmetric (Thm power-sde) if κ_d ≥ 2 and p ≥ 16κ_d^{2κ_d+2}; else Ivanyos–Santha at degree κ_d | Π_{d=2}^c M_d with M_d = g_d+1, (g_d+1)((κ_d−1)g_d+1) or B_{κ_d}(g_d) respectively; ≤ Π B_d(g_d) |
| Random column | p ≥ 16u², u ≥ c, u > max_d a_d (u = max(c, g_2+1) suffices) | kernel rejection; fresh i.i.d. banks | (4u)^{c−1} per tree attempt |

The caption should then say that the combined row is a schedule choice made from public
(p, d, g_d), with Schedule 2 still "checked only by automated review".

## 6. Claim gates that must stay false

In `research/reductions/rees_hsp_reduction.json`: `novelty_established`,
`speedup_claim_allowed`, `independent_review`, `general_sde_implemented`,
`coherent_receiver_implemented`, `formal_compiler_checked`, and every `is_total_gate_bound`.
STATE.md: "All Rees claim gates stay false". Also keep these false: any claim of polynomial
arity or polynomial time at primes below the thresholds; any claim that Schedule 3 (or W+3)
is polynomial time; any claim that Schedule 2 is human-checked. The TRAPS wording
"proposed fixed-class, growing-prime polynomial-time composition, pending independent
correctness and priority review" still applies word for word.

## 7. Text fixes (listed, not applied)

1. main.tex Schedule 1 paragraph (≈ line 420): "solve with exponent κ_d and convert by a
   Bezout exponent; the displayed d-bound remains sufficient". Add that B_{κ_d}(g_d) (and
   g_d + 1 when κ_d = 1) is also sufficient and is the arity the reduced solver uses. The
   query count Π B_d(g_d) is then an upper bound, not the count.
2. main.tex after thm:power-sde: state the combined per-grade rule and that its choice uses
   only (p, d, g_d). Say that Schedule 1's fallback makes it valid for all p > c.
3. thm:random-column (ii): the abort bound assumes every grade uses 4u columns. A mixed tree
   needs the node-count-weighted bank bound of §2.4. Say so if mixing is ever stated.
4. Table `tab:main-regimes`: as §5. The "Large field" row's sources column should use the
   κ_d = 1 value g_d + 1 explicitly (its formula already gives (g_d+1)·1).
5. Abstract/intro wording on the exponent: "at most 145" stays correct. If a sharp worst case
   is quoted, it is 143 at c = 9 under the combined rule (§3.3).

## 8. Reviewer items

- Human check of 2.3 item 2 (conditioning on record events does not disturb ρ_{H_d}). It is
  the same fact as 11-01's "kept trees i.i.d.", but here it is used for Las Vegas aborts across
  grades.
- Human check of the Schedule-2 Weil step (still AI-only, 11-01 §5.4).
- The IS time bound at degree κ_d: poly(B_{κ_d}(g_d), log p) with a κ_d-dependent exponent
  (11-01 §5.3 open item, unchanged).

## Next

Hard question: polynomial worst-case arity at κ_d ≥ 2 with p < 16κ_d^{2κ_d+2} (the parallel
session's topic). Command: the script above. Acceptance test: every row asserts
total ≤ ε, and the S1 row reproduces 1573/1570.
