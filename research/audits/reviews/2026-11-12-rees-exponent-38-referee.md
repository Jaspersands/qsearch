# 2026-11-12 Referee: exponent 38 (multi-representation descent, k8 attack)

Hostile referee report. AI only (one Claude Code session), pending human review. I edited no
paper, STATE, handoff, registry or reductions file. No Git, no network, no API calls.

Target: `2026-11-12-rees-exponent-k8-attack.md` and its folder. My own checks are in
`2026-11-12-rees-exponent-38-referee/`. Every script was run with
`nice -n 19 /opt/anaconda3/bin/python`; peak RSS was under 100 MB and the longest run took
about 3 min. I wrote the exponent code and both executors from the definitions alone. I read
the attack's `exponents_s1h.py` only after my numbers were fixed. Finite checks can only
falsify.

## 0. Verdict

**38 may replace 53 as the Outlook bound: CORRECT WITH FIXES.** It would carry the same status
as 53 (AI-proved, AI-refereed, pending human review). It cannot carry a stronger status than
53, for two reasons. First, 38 is built on 53: its inner solvers are Schedule 1 at depth
⌈log₂ t_d⌉, which rests on lem:rounds. Ivanyos did not confirm lem:rounds. Second, the new
nodes add their own AI-only lemmas.

- **Mathematics.** I re-derived Lemmas S and F, Theorem HC, Corollary HCD, Proposition F and
  Corollary 41 line by line and found no gap. All of these nodes work on arbitrary columns.
- **Exponent.** I recomputed the class-9 exponent independently and got **38**. It is attained
  exactly at the primes p ≡ 1 (mod 2520). For p > 30000 this is a **proof**, not a scan: the
  value there is a function of p mod 5040, and I evaluated all 1152 residues.

The fixes are needed before 38 can stand in for 53. The main one is that Theorem HC's
"deterministic" is wrong for unbounded p. The S1H node is Las Vegas inside every merge, and
its scalar output needs root finding. The import list and the error budget must say so. That
is allowed by rem:main-solver and rem:is-import(d), so it is a fix, not a gap.

## 1. Findings (material)

**M1. Theorem HC "deterministic when the inner nodes are" is FALSE as stated for unbounded p.**
The claim holds at fixed p, so Corollary 41 is unaffected. The relabelled form, "Las Vegas,
output checked", is PROVED. Lemma S and Lemma F need four things the attack does not account
for at large p:
- (i) An element q of coset class m = κ/2. The attack uses a primitive root g. No deterministic
  poly(log p) method is known for finding either one; for κ = 2 this is the problem of finding
  a quadratic nonresidue. When −1 ∉ P_κ, q = −1 works.
- (ii) κ-th roots of the node coefficients x_ν and x_ν/q. rem:main-solver requires the
  scalars s_b themselves. An inner D-solver returns σ with σ^D = x_ν, so a κ-th root of x_ν
  needs a square root of σ up to a D-th root of unity.
- (iii) The representation η = y₁ + εy₂, which the attack already says is Las Vegas.
- (iv) κ-th roots of the y_k.

Rabin root finding and random trials make the node Las Vegas with checkable output. rem:is-import(d)
admits that.

So S1H is Las Vegas **per merge**, depending on the labels. By contrast, 53 is Las Vegas only in
its once-per-grade preprocessing.

**M2. Error budget (FIX).** The 53 patch (`2026-11-12-rees-headline-53.md` §3) gives the spare
ε/3 to the per-grade zero-sum preprocessing, so the total is exactly ε. S1H's per-merge Las
Vegas aborts need their own share. Split that third, for example ε/6 for the preprocessing and
ε/6 for N_solver calls at ⌈log₂(6N_solver/ε)⌉ attempts each. Each attempt must also repeat its
internal Las Vegas sub-steps enough times to fail with probability ≤ 1/4. This changes only the
classical attempts, not Q_q or the exponent.

**M3. The import list is incomplete (FIX).** "IS import, Gaussian elimination, Weil" omits:
- everything 53 rests on: lem:rounds, the Las Vegas zero sums, and the exhaustive t-table below
  4κ⁴;
- Rabin root finding;
- random coset representatives;
- the Hasse–Weil bound for the smooth plane curve u^κ + εv^κ = η. This is a different
  statement from the character-sum bound used for t ≤ 3, and its locator is unchecked.

My exact computation covers every p ≤ 30000 without any Weil shortcut. So Hasse–Weil, in any
of its standard forms (the genus form (κ−1)(κ−2)√p plus κ points at infinity, or the
Jacobi-sum form (κ−1)²√p), is needed only for p > 30000, where both forms hold.

**M4. The Corollary 41 union-step witness is not an RC(8; Z₈ → K) contraction in the
appendix's sense (FIX in citation; the mathematics is fine).** Its C₀₀ = α₀ + β₀ = 26 has
class 1, not 0 (`cor41_check.out`). rem:app-s2-tower-scope and the RC definition require
α₀ + β₀ ∈ Q₀. As a K-node it is still valid. The output coefficients are C_ij·ω'^κ_b of class
in K, and the output is nonzero because C₀₀ ≠ 0 and S₀₀ ≠ ∅ (lem:app-s2-tensor(a)). The
citation should be replaced by this one-line argument. This affects only Corollary 41 and R7,
not 38.

**M5. The tail argument is stronger than the attack states.** The attack argues that "all residue
classes occur below 3·10⁶". That step is unnecessary, and it is not printed in their output.
The direct argument:
- For p > 30000, κ_d = gcd(d, p−1) depends on p mod 2520.
- t ∈ {2, 3} by Weil (p ≥ 4κ⁴), and t = 2 exactly when (p−1)/κ is even.
- One stage followed by F1 is valid for every even κ ≤ 8. That gives
  e(κ) = min(κ⌈log₂ t⌉, e(κ/2) + 1). Every other option costs more: F0 after one stage is
  impossible (Proposition F's argument), two or more stages cost ≥ 2e(D), and F2 costs
  ≥ e(D) + 1.

So E is a function of p mod 5040. Over all 1152 units mod 5040 its maximum is 38, at
r ∈ {1, 2521}, that is p ≡ 1 (mod 2520) (`s1h_independent.out`, "tail"). It agrees exactly
with the set computation on every prime in (26244, 30000].

**M6. Separable gain (new information for the owner).** The descent does not need lem:rounds.
With the Ivanyos-confirmed depth ⌈log₂(κ+1)⌉ as the inner IS node, the same device gives
c = 9 → **95**, down from 145, by exact computation to 30000 plus the tail (`pub_hcd.out`).
This is an option if lem:rounds is not accepted. So 38 is 53 combined with the descent.

## 2. Obligation table

| item | law-free (arbitrary columns) | total | returns s_i | arity (exact) | deterministic | imports | verdict |
|---|---|---|---|---|---|---|---|
| Lemma S | yes; inner node worst-case, objects arbitrary (zero/repeated) | yes, given total {0,m}-node | weights in P; roots need M1(i),(ii) | N_j per group, support ⊆ group | only at bounded p | inner node; q ∈ Q_m; κ-th roots | CORRECT |
| Lemma F | yes | yes, given K + cl(ρ) ⊆ cl(Tn∖0) | roots need M1(iii),(iv) | N' objects | only at bounded p | K-node; representation table / Weil; roots | CORRECT |
| Theorem HC | yes | yes | yes, with roots | N'·∏N_j (checked) | **wrong as stated**; Las Vegas | as above | CORRECT WITH FIXES (M1) |
| Cor. HCD (i) −1 ∉ P_κ | yes | yes | yes (q = −1, ε ∈ P; F0 needs 53's zero sum) | N_D^⌈log₂t⌉ | as inner + zero sum | 53's zero sum | CORRECT |
| Cor. HCD (ii) Weil | yes | yes | yes, with roots | (a+1)·N_D, degree e(D)+1 | Las Vegas | Hasse–Weil, Rabin | CORRECT WITH FIXES (M1, M3) |
| Prop. F (floor 2) | n/a | n/a | n/a | n/a | n/a | hypothesis: degree-1 nodes only GE | CORRECT (trivial; calculus-internal; no lower bound outside it) |
| Cor. 41 (8, 41) | yes | yes | yes (tables, P₈ = μ₅) | (a+1)(3a+1)·(a+1)(7a+1) | yes (fixed p) | lem:app-s2-tensor (appendix, AI-checked), two finite witnesses | CORRECT WITH FIXES (M4 citation) |
| S1H = 38 at c = 9 | yes | yes | yes, Las Vegas | 1+Σe_d = 38, e = [2,3,3,5,4,7,4,9] | Las Vegas per merge | 53's inputs + S/F/HCD + Hasse–Weil + Rabin | CORRECT WITH FIXES (M1–M3) |
| R7 = 25 | yes (worst-case nodes) | yes | yes | — | Las Vegas (Schedule 2) | CONDITIONAL, see §5 | condition identified; value not re-derived |
| Prop. U / window [c−1, c] | yes | yes | yes (exhaustive search) | κ_d g_d + 1 (Chevalley–Warning) | yes, but **exponential time** | Thm LB of new-routes (model) | CORRECT in its model; not about thm:main |

## 3. Re-derivations (obligation 1)

- **Lemma S.** Let x be the node output, I its class-0 part and J its class-m part.
  - If J = ∅, then Σ_I x_ν·rep₁(o_ν) has value c₁·0 = 0. The weights lie in P·P = P, and the
    sum is nonempty and disjoint. This is a solution, and it needs no c₁ ≠ 0.
  - If both I and J are nonempty, put u = Σ_I x_ν v_ν. Then Σ_J x'_ν v_ν = εu with
    ε = −q⁻¹. There are 2r reps with values c_k u and εc_k u. They are disjoint because the
    objects are disjoint and so are the reps of each object. u = 0 is harmless.
  - The type is the same for every group because q is fixed for the whole stage.
- **Lemma F.** Tn is P-invariant, so Tn∖0 is a union of classes. Each nonzero ρx_ν is
  Σ_k y_{νk}c_k with y_ν ≠ 0. The combined reps have value ρΣx_νv_ν = 0, and they are nonzero
  because the reps are disjoint and nonempty. The same holds for F0 on a single object.
- **Tn recursion.** Tn_s = Tn ∪ εTn ∪ (Tn + εTn). I implemented it exactly as class sets plus a
  zero flag.
- **HCD (ii).** The curve X^κ + εY^κ = ηZ^κ is smooth (p ∤ κ, εη ≠ 0) and has genus
  (κ−1)(κ−2)/2. It has at most κ points with Z = 0 and at most 2κ with uv = 0. So the 3κ
  condition leaves an affine point with uv ≠ 0. Existence needs only > κ.
- **Prop. F.** With no stage, the finish must be a single-class node, which is not Gaussian
  elimination, so its degree is ≥ 2. One stage with F0 needs −ε ∈ P, but cl(−ε) = −m ≠ 0. So
  every plan has degree ≥ 2.
- **Cor. 41.** I re-checked it (`cor41_check.out`):
  - ξ = 6 is a coset generator, P₈ = {1, 10, 16, 18, 37}, and −1 has class 4;
  - |2D| = 21 and 2D∖0 = Q₀ ∪ Q₁ ∪ Q₂ ∪ Q₃; 3D = F ∖ (−P₈); 4D = F; t(41, 8) = 5;
  - ε = 18 ∈ P₈;
  - all 16 κ = 4 cells lie in Q^{(4)}_{−i−j} (C₀₀ = 10), and all 64 κ = 8 cells are nonzero
    with class + i + j ∈ {0,1,2,3} (C₀₀ = 26, class 1, see M4).
  - My own implementation of lem:app-s2-tensor drove Corollary 41 end to end. It verified
    30/30 at a = 1 (arity 128) and 30/30 at a = 2 (arity 945), on uniform, unit-class (dead-like)
    and all-equal banks; 20 of each 30 reached the union finish.
  - N(8, 1, 41) = 5 holds, and the dead 4-banks are exactly four equal classes
    (`dead_a1_check.out`). The 4a+1 lower bound is checked by hand.
- **Recursive executor** (`hcd_executor.out`, `hcd_fullpath.out`).
  - 1206/1206 adversarial and uniform banks verified, over 35 cells (p, κ, a): κ ∈ {2, 4, 8}
    at p = 13, 17, 29, 41, 61, 73, 1801, 2521, with a ≤ 3 and arity ≤ 4096. Plans were
    1×HCD+F1, F2(2), F2(4) and 2×HCD+F1. Gaussian elimination is the only base solver.
  - Top-level finishes were reached in 6–25 of 36 runs per cell, except (17, 8, 1), where every
    run exited early.
  - κ = 6 was not executed, because its inner κ = 3 node is Schedule 1 (NOT computed).

## 4. Plugging into thm:main (obligation 2)

- **Merge identity.** prop:descent needs only a nonzero scalar solution for the measured
  labels. The node returns one for every label tuple, and an early exit is a smaller support
  with zero insertion. The output is exactly ρ_{H_{d−1}} and does not depend on the record or
  the random bits, so independence holds.
- **Sources.** P = ∏M_d, where M_d is the S1H arity. It is public and computable from
  (p, d, g_d): exact class sumsets below 30000 (a constant for fixed c) and the formula above.
  It is bounded by the published B_d with p-independent constants.
- **Error.** M2.
- **Labels.** No step uses uniform labels. The attack's tests note that uniform banks exit
  early, but the proof never uses that.
- **Explicit bound.** thm:main(3) and (4) change only if the owner adopts the new arities.

## 5. Exponent recomputation (obligation 3)

`s1h_independent.py` computes t by exact class sumsets, the plans by exact Tn sets with no
Weil shortcut for p ≤ 30000, and the residue formula above that.

| rule | c = 2..9 (worst over p > c) | c = 9 attained at |
|---|---|---|
| S1t control | 5, 8, 16, 19, 35, 36, 44, **53** | 2521, 7561, 12601 (matches the headline-53 note) |
| S1H (mine) | 3, 6, 10, 14, 20, 25, 29, **38** | 2521, 7561, 12601, 15121, 20161 (all primes ≡ 1 mod 2520 below 30000) |
| S1H without F2 | identical | — |
| S1H tail, all units mod 5040 | 3, 6, 9, 14, 18, 25, 29, **38** | r ≡ 1 (mod 2520) only |
| published depth + HCD (M6) | 3, 9, 13, 27, 39, 55, 59, **95** | p ≡ 1 (mod 2520) |

Status of 38: PROVED given cited results (IS Theorem 11 as AI-read, lem:rounds, Hasse–Weil,
Rabin), with an exact finite computation, and Las Vegas. Two independently written AI codes
agree on every value in the table. Pending human review.

## 6. R7 = 25 (obligation 4): what the condition is

25 is CONDITIONAL. It inherits R5's conditions:
- thm:power-sde(ii) and prop:decoupled-sde / prop:app-s2-TA, which a human has not read
  (owner policy);
- the finite AI tables for E₂, chains and NOSTD, which are quoted and were not re-run.

It adds:
- the union-step K-node, which needs the one-line lemma of M4, not the RC definition;
- the attack's own union-step and plan searches, which are finite and AI-only.

The binding grade is κ₉ = 9 at Schedule 1 degree 9, at primes with no chain. Union-step
searches that hit the node cap (233 at κ = 8; 307 and 433 at κ = 9) were treated as
non-existent. That is conservative for an upper bound, and the maximum 25 is also attained at
37, 73, 127 and 181, where the searches completed. I did not re-derive 25. It should not enter
the core before a separate referee covers the K-node lemma and the R7 tables.

## 7. Window (obligation 5)

Proposition U is correct in the time-unbounded label-combining model of the new-routes note.
- Chevalley–Warning gives a nonzero solution from κ_d g_d + 1 columns, since there are a
  equations of degree κ.
- Exhaustive search finds it, so E ≤ c.
- Theorem LB(iv) gives E ≥ c, or E ≥ c−1 with stage-2 multi-output, on free algebras as
  r → ∞.

It restates "free-coordinate nodes reach ≈ c in exponential time" and says nothing about
thm:main, which is polynomial-time. The attack's statement that there is no polynomial-time
lower bound above c−1 is an absence claim: UNKNOWN, not hardness.

## 8. Replacement text (core Outlook, "Shorter zero sums in Schedule 1")

After "…from \ReesClassNineQueryExp to 53 without Schedule 2 (…)", insert:

> A second device lowers it further. Let $\kappa = \kappa_d$ be even, $D = \kappa/2$, $P$ the nonzero
> $\kappa$-th powers, and fix $q$ with $q^{(p-1)/\kappa} = -1$; put $\varepsilon = -q^{-1}$. Any solver for
> exponent $D$ returns coefficients in $P \cup qP$, so on each block of its arity it returns either a
> solution or a vector $u$ with two disjoint representations $\sum_{S_1} w_b\lambda_b = u$ and
> $\sum_{S_2} w_b\lambda_b = \varepsilon u$, all $w_b \in P$. If every nonzero element of $\Fp$ is
> $y_1 + \varepsilon y_2$ with $y_1, y_2 \in P\cup\{0\}$ (true once $p+1-(\kappa-1)(\kappa-2)\sqrt p > 3\kappa$, by
> the Hasse--Weil bound for $u^\kappa + \varepsilon v^\kappa = \eta$, and checked exactly below), a
> linear dependence among $g_d+1$ such vectors, rewritten through these representations, is a
> solution for arbitrary label columns, and grade $d$ costs the degree of the $D$-solver plus one.
> Returning the scalars needs $\kappa$-th roots, $q$ and the $y_i$, found by Las Vegas root finding
> and random trials, so this solver is Las Vegas inside each merge and is charged as in
> Remark~\ref{rem:is-import}(d), with the unused third of the error budget split between it and
> the zero-sum preprocessing. With Schedule~1 at depth $\lceil\log_2 t_d\rceil$ as the inner
> solver, the class-nine exponent of $m$ is at most $38$ for every prime $p > 9$, attained by this
> rule exactly at $p \equiv 1 \pmod{2520}$ (exact computation for $p \le 30000$; above that the value
> depends only on $p \bmod 5040$, and every residue was evaluated). With the published depth
> $\lceil\log_2(\kappa+1)\rceil$ instead, the same device gives $95$. Status: AI-proved and AI-refereed,
> pending human review; the value $38$ rests on everything the value $53$ rests on.

In "Smaller arities", leave 37 unchanged for now (§6). If the owner adopts 25, add "and on
finite union-step searches (conditional)".

## 9. Adversarial self-check

- *Did I just confirm the attack?* My code shares no code with the attack. It uses a different
  representation (class sets with a zero flag, numpy) and a different tail argument (direct
  residues rather than primes up to 3·10⁶). The S1t control reproduces 53, and the 145 → 95
  variant is new. A shared conceptual error is still possible. The likeliest is the rule
  definition itself: the cost s·e(D) + e(finish) assumes arities multiply. Lemma S/F give
  exactly N'∏N_j, so this holds.
- *Could the worst case be at a small prime?* The exact range shows the c = 9 maximum only at
  primes ≡ 1 mod 2520. The highest values at other primes are 37 (e.g. 6301, 8821, 16381).
- *Is "Las Vegas" acceptable?* rem:main-solver explicitly allows it. If the owner insists on a
  deterministic algorithm, the large-p S1H node is UNKNOWN deterministic. The fallback 91 of
  the 53 note is unrelated to this device.
- *M4.* Could C₀₀ ∉ Q₀ break the tensor proof? No. lem:app-s2-witness uses C₀₀ ≠ 0 only for
  u ≠ 0. The class-0 normalisation matters only for chaining (refine), and Corollary 41 does
  not use it.
- *Not checked:* the SAT/LRAT items (§9.7–8 of the attack), the counts of 98 union targets, the
  a = 2 dead-bank searches, the R5/R7 tables, and κ = 6 execution.
- *Weakest point.* Everything below 38 inherits lem:rounds, which is AI-proved and unconfirmed
  by Ivanyos. The new lemmas are short, but no human has read them.
