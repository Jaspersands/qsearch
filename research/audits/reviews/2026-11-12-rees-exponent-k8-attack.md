# Rees exponent of m: attack at κ = 8, p = 41 (2026-11-12)

AI only (one Claude Code session), pending human review. No paper, STATE, handoff,
registry or reductions file was edited; no Git, no network, no API calls. Scripts and
outputs are in `research/audits/reviews/2026-11-12-rees-exponent-k8-attack/` (run with
`nice -n 19 /opt/anaconda3/bin/python`). Finite checks can only falsify; nothing below
is promoted from a passing check.

Inputs read: `2026-11-12-rees-exponent-new-routes.md`, `-discharge.md`, `-discharge-referee.md`,
core `main-core.tex` Outlook, `appendix-schedule2.tex` (tensor, contraction, towers, chains,
union targets), IS §3.2–3.3 (`2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`), and the
heads of the 11-08/11-11 near-linear and bounded-p notes.

Labels: PROVED, PROVED given cited results, CONDITIONAL, REFUTED, UNKNOWN, NOT computed;
"exact" = complete finite computation; "sampled" = random instances.

## 0. Verdict

1. **The law-free node at (κ, p) = (8, 41) drops from degree 24 to degree 4. It is not linear.**
   The new node is deterministic and polynomial-time. It works on arbitrary columns and has
   arity `(a+1)(3a+1)·(a+1)(7a+1)`. It makes one *half-degree collision* stage with a κ = 4
   solver. Since −1 ∈ P_4 ∖ P_8 at p = 41, every 4th-power relation is an 8th-power collision.
   A two-level union-target step to the classes {0,1,2,3} then finishes the job
   (Theorem HC, Corollary 41). This is PROVED given IS Lemma 12 with ℓ = 2 and two explicit
   finite witnesses. Both witnesses can be checked by hand (§3), and the node was run and
   verified on 324 banks (§9).
2. **A linear (O(a)) law-free node at (8, 41): neither constructed nor refuted.**
   - Existence cannot be refuted: by Chevalley–Warning, every 8a+1 columns have a solution.
   - Exact: N(8,1,41) = 5. The only dead 4-banks are four columns of one P_8-class.
   - Hence 4a+1 ≤ N(8,a,41) ≤ 8a+1 (PROVED). The dead family is a blocks of four equal
     columns e_j.
   - At a = 2 no dead bank larger than 8 was found (sampled and capped exact search), so
     4a+1 may be sharp. NOT proved.
   - Finding a solution at linear arity remains UNKNOWN. At fixed p the problem is a
     Chevalley-type total search problem (PPA_41 per GKSZ, as recalled in the 11-11 note).
     Uniform random banks at this arity are a fixed-modulus SIS-type problem with no known
     polynomial algorithm.
3. **The new calculus has a degree floor of 2 per grade (Proposition F, PROVED).** It cannot
   close the factor 2. In the time-unbounded label-combining model of the new-routes note,
   the window is already [c−1, c] (Proposition U). Any lower bound above c therefore needs a
   time-bounded model and a hardness assumption. None is available for the total regime
   (§7).
4. **Recomputed class-9 exponent, worst case over all primes p > 9:**

   | rule | inputs | E at c = 9 (attained at) |
   |---|---|---|
   | S1t (owner's planned headline) | IS import, Weil | 53 (p = 2521) |
   | S1H = S1t + half-degree descent | IS import, Gaussian elimination, Weil | **38** (p ≡ 1 mod 2520, e.g. 2521, 7561, 12601, 20161) |
   | R5 (discharge T3) | conditional (Schedule 2, E_2 tables, chains) | 37 (p = 41, 73) |
   | R7 = R5 + full descent calculus | as R5, plus explicit two-level witnesses | **25** (p = 37, 73, 127, 181, 433) |

   Above T_A(9) = 3.10·10⁹ the value is 17 (unchanged). For c = 2..9:
   - S1H gives 3, 6, 10, 14, 20, 25, 29, 38 (was 5, 8, 16, 19, 35, 36, 44, 53).
   - R7 gives 3, 5, 9, 10, 14, 17, 20, 25 (R5 gave 3, 5, 16, 14, 28, 29, 36, 37).

   The new binding grade is κ_9 = 9 at primes with no chain. There no two-class union step
   exists, so the IS collision of degree 9 remains (§5).

## 1. Setting

The task is SDE(κ, p, a): given λ_1..λ_M ∈ F_p^a, find nonzero x ∈ (P ∪ 0)^M with
Σ x_b λ_b = 0. Here P = P_κ = (F_p^×)^κ and κ | p−1. This is equivalent to Σ s_b^d λ_b = 0
by lem:app-s2-gcd. Fix a primitive root g and write cl(x) ∈ Z_κ for the class of x, so that
x ∈ g^{cl(x)}P; also Q_m = g^m P.

At p = 41 with g = 6:
- P_8 = μ_5 = {1, 10, 16, 18, 37} and D = P_8 ∪ {0};
- −1 has class 4, so −1 ∉ P_8;
- P_4 = P_8 ∪ (−P_8) = μ_10.

Write ℓD for the ℓ-fold sumset of D (exact, in `collision_descent.py` and `witnesses_41.out`):
- |2D| = 21, and 2D∖{0} = Q_0 ∪ Q_1 ∪ Q_2 ∪ Q_3;
- 3D = F_41 ∖ (−P_8);
- 4D = F_41.

So t(41, 8) = 5, the shortest zero sum of nonzero 8th powers.

## 2. The multi-representation descent (PROVED)

**Objects.** A *rep* is (S, w), with S ⊆ [M] and w: S → P. Its value is Σ_{b∈S} w_b λ_b. An
*object of type c = (c_1..c_r)* is a vector v ∈ F_p^a together with r reps that are pairwise
disjoint and nonempty, where rep k has value c_k v. Each column is an object of type (1).
Put Tn(c) = {Σ_k y_k c_k : y ∈ (P∪0)^r, y ≠ 0}. This set is P-invariant.

**Two-class nodes.** For m ≠ 0, an *{0,m}-node* of arity N takes any N vectors of F_p^a and
returns a nonzero x with Σ x_ν v_ν = 0 and every nonzero x_ν of class 0 or m. There are two
examples:
- (i) for even κ, m = κ/2: any law-free solver for exponent D = κ/2, because P_D = Q_0 ∪ Q_{κ/2};
- (ii) a two-level *union step* RC(κ; Z_κ → {0,m}), that is, the tensor of lem:app-s2-tensor
  with a matrix C_ij = z_i z_j(α_j + β_i) whose nonzero entries have classes in {0,m}.

More generally, a *K-node* has its classes in K.

**Lemma S (stage).** Feed N objects of one type c, with disjoint supports, to an {0,m}-node.
The result is either a solution, or one object of type (c, εc) with ε = −g^{−m}. In both cases
the support lies inside the union of the input supports.

*Proof.*
- Let x be the node's output. Put I = {ν : cl(x_ν) = 0} and J = {ν : cl(x_ν) = m}, and for
  ν ∈ J write x_ν = g^m x'_ν with x'_ν ∈ P.
- If J = ∅, then Σ_I x_ν v_ν = 0. The reps "x_ν times rep 1 of o_ν" for ν ∈ I form a solution:
  the weights are P·P = P, the supports are disjoint, and the result is nonempty. The case
  I = ∅ is the same with x'.
- Otherwise put u = Σ_I x_ν v_ν. Then Σ_J x'_ν v_ν = −g^{−m}u.
- For each k, the I-side rep Σ_{ν∈I} x_ν·rep_k(o_ν) has value c_k u. The J-side rep
  Σ_{ν∈J} x'_ν·rep_k(o_ν) has value c_k εu.
- These 2r reps are disjoint and nonempty, and their weights lie in P. ∎

**Lemma F (finish).** Let 𝒩' be a K-node, and suppose some ρ satisfies
K + cl(ρ) ⊆ cl(Tn(c)∖0). Then one call of 𝒩' on objects of type c gives a solution. Also, if
0 ∈ Tn(c), a single object gives a solution.

*Proof.*
- Take Σ x_ν v_ν = 0. Every nonzero ρx_ν lies in Tn(c), so ρx_ν = Σ_k y_{νk}c_k with y_ν ≠ 0.
- The reps Σ_ν Σ_k y_{νk}·rep_k(o_ν) have value ρ Σ x_ν v_ν = 0.
- The weights lie in P, the supports are disjoint, and the sum is nonzero.
- For the F0 case, apply the same argument to one object. ∎

Four finishes are used:
- F0: 0 ∈ Tn;
- F1: Gaussian elimination, with K = Z_κ, which needs Tn ⊇ F_p^×;
- F2: a D'-solver for some D' | κ, with K the classes of P_{D'};
- F3: a union step to a target K.

**Theorem HC.** Take a plan made of stages with {0, m_j}-nodes of arities N_j(a), followed by
a finish of arity N'(a). It is a law-free node of arity N'(a) ∏_j N_j(a). It is deterministic
when the inner nodes are, and Las Vegas when they are Las Vegas. The bookkeeping is
polynomial. The type after the stages is generated by c ↦ (c, ε_j c), so Tn is computed by
sumsets.

Writing y as above costs O(p·r) by a table. At large p it is Las Vegas: pick y_1 ∈ P
uniformly and test η − y_1 ∈ εP. By the Weil bound for u^κ + εv^κ = η, the success
probability is ≥ 1/(2κ) once (κ−1)(κ−2)√p + 3κ ≤ p/2. Below that, p = O(κ⁴) and the
table has bounded size.

*Proof.* Induct on Lemma S, and close with Lemma F. ∎

**Corollary HCD (half-degree collision descent).** Let κ be even, D = κ/2, and let e(·) be
degrees.
- If −1 ∉ P_κ, then ε ∈ P and e(κ) ≤ ⌈log₂ t(p,κ)⌉·e(D).
- If p + 1 − (κ−1)(κ−2)√p > 3κ, then Tn after one stage is F_p^×, so e(κ) ≤ e(D) + 1
  (finish F1).

**Proposition F (degree floor of the calculus; PROVED).** Let κ ≥ 2, and suppose every node
has degree ≥ 1, with degree 1 only for Gaussian elimination. Then every plan has degree ≥ 2.

*Proof.*
- Columns have Tn = P. A finish without a stage needs K + c ⊆ {0}, which is a κ-node itself.
  So s ≥ 1.
- F0 after one stage needs y_1 + εy_2 = 0 with y_i ∈ P, that is −ε ∈ P. But −ε = g^{−m} has
  class −m ≠ 0. So s = 1 forces a finish of degree ≥ 1.
- Hence the degree is ≥ 2 in all cases. ∎

The descent therefore cannot give a linear node, and no plan in it reaches exponent ≈ c.

## 3. Corollary 41: a degree-4 node at κ = 8, p = 41

**Statement (PROVED given IS Lemma 12 with ℓ = 2 and the witnesses below).** From any
N(a) = (a+1)(3a+1)·(a+1)(7a+1) columns in F_41^a, the following plan returns a nonzero
x ∈ (P_8 ∪ 0)^N with Σ x_b λ_b = 0. It uses poly(a) field operations and is deterministic.

1. **Stage.** Split the columns into (a+1)(7a+1) groups of (a+1)(3a+1). On each group, run the
   two-level κ = 4 construction with ξ = 6, α = (10, 7, 21, 24) and β = (0, 1, 10, 9).
   - All 16 entries α_j + β_i lie in Q^{(4)}_{−i−j}, and the (0,0) entry is nonzero.
   - Its coefficients lie in P_4 = Q_0 ∪ Q_4.
   - By Lemma S with m = 4, each group yields a solution or an object of type (1, 18), since
     ε = −6^{−4} = 18 ∈ P_8.
2. **Finish F3.** Here Tn(1, 18) = 2D∖{0} = Q_0 ∪ Q_1 ∪ Q_2 ∪ Q_3. Run the two-level union
   step RC(8; Z_8 → {0,1,2,3}) on the vectors of the (a+1)(7a+1) objects, with ξ = 6,
   α = (26, 30, 30, 27, 35, 25, 2, 2) and β = (0, 0, 0, 1, 1, 1, 2, 2).
   - All 64 entries α_j + β_i are nonzero, with classes in {0,1,2,3} − i − j.
   - Lemma F with ρ = 1 finishes. Each x_ν ∈ 2D∖0 is written as y_1 + 18y_2 from a 21-entry
     table.
3. **Roots.** s_b = x_b^{1/8} by table lookup (P_8 = μ_5).

The degree in a is 4, against 24 for Schedule 1 at depth ⌈log₂ 5⌉ = 3, and 6 for three
collision stages with finish F0. As a check, ((a+1)(3a+1))²(a+1) with finish F1 (4D = F_41)
gives degree 5. All three plans were run (§9).

*Why the earlier searches missed it.* The chain search of rem:app-s2-chains-scope (no chain at
p = 17, 41, 73 for κ = 8) tracks a single relation whose coefficient classes are refined step
by step. Lemma S keeps instead several disjoint representations of one vector, as in the
accumulation of IS §3.3. The class set {0,1,2,3} of 2D cannot arise as K_t in a chain, because
it is a sumset class, not a coefficient class. The union step to {0,1,2,3} itself exists at
41 (exact). Union steps to K ∋ 0 exist exactly for the 10 targets with |K| ≤ 3 listed in
`union_step.py` output, all of which contain a pair {c, c+4}, and for 98 targets of sizes
4–7. Eight of the latter have no antipodal pair, including {0,1,2,3} (exact).

## 4. Other bad pairs (exact plans, all run and verified)

The plans below are from `exponents_r7.out` (pairs where R5 ≥ 5).

| κ, p | R5 | new | plan |
|---|---|---|---|
| 4, 5 | 12 | 5 | 2 HCD stages + F1 |
| 4, 13 | 8 | 4 | HCD + F2(D'=2) |
| 5, 11 | 5 | 4 | union stage {0,1} + F3 {0,2,4} |
| 6, 7 | 18 | 6 | 2 HCD + F2(2) |
| 6, 13 / 19 / 43 | 6 / 12 / 12 | 4 | HCD + F2(3) |
| 6, 31 | 18 | 4 | HCD + F3 {0,1,2} |
| 6, 67 | 12 | 4 | HCD + F2(2) |
| 7, 29 | 7 | 7 | no two-class union step (S1t stays) |
| 7, 71 | 7 | 4 | union stage {0,2} + F3 {0,2,3,4,5,6} |
| 8, 17 | 8 | 5 | HCD (inner κ=4 at 17 ∈ E_2(4): degree 3 by R5) + F3 {0,1,4,5} |
| 8, 41 | 24 | 4 | Corollary 41 |
| 8, 73 / 89 / 137 | 16 | 4 | HCD + F2(4) |
| 8, 233 | 16 | 4 | HCD + F2(2) |
| 9, 19 / 37 / 73 / 109 / … / 433 | 9 | 9 | no two-class union step found (S1t stays) |

For κ = 9 at 307 and 433, and for κ = 8 at 233, some union-step searches hit the node cap.
These were treated as non-existent, which is conservative (`exponents_r7.out` lists them).

## 5. Class-9 exponents (finite exact computation, plus analytic tail)

- **S1H (core standard)** (`exponents_s1h.py`).
  - Scope: every component is the IS import, Gaussian elimination, or the Weil bound for
    diagonal curves. No Schedule 2, no E_2 table, no union step.
  - Results: c = 9 gives 38, attained at p = 2521, 7561, 12601, … (p ≡ 1 mod 2520), with
    e = [2,3,3,5,4,7,4,9].
  - Tail: for p > 30000 every κ ≤ 9 passes the Weil test. S1H(κ,p) then depends only on the
    parities of (p−1)/κ_d, and all residue classes occur below 3·10⁶. The maximum over
    (30000, 3·10⁶] is 38.
  - Status: PROVED at the standard of thm:main (IS reading AI-checked), together with the
    Weil bound, assuming the finite tables are correct.
- **R7 (conditional, like R5)**.
  - Result: c = 9 gives 25, with e = [2,2,3,1,3,1,3,9] at p = 37 and [2,2,2,1,3,1,4,9] at 73.
  - It also holds with the shorter list of rem:app-s2-chains-scope, since 37 and 73 have no
    chain for κ = 9.
  - Removing grade 9 at those primes leaves 16, so κ = 9 is now the bottleneck.
  - Above 20000, R7 ≤ R5 ≤ 18, and above T_A(9) it is 17.
- **The owner's 53.** It survives as a valid bound, but S1H at the same standard gives 38. The
  inner κ = 4 and κ = 8 grades drop from 4 and 16 to 3 and 4 (e_4: S1t 4 → 3; e_8: 16 → 4;
  e_6: 6 → 4).

## 6. Linear arity at (8, 41): what is and is not known

- **N(8,1,41) = 5** (exact, `dead_a1.out`). The dead 4-banks are exactly 4 equal classes.
- **Lower bound 4a+1 ≤ N(8,a,41)** (PROVED). The bank consisting of e_j four times for each j
  is dead, because a nonzero zero sum would need a zero sum of ≤ 4 elements of D, and
  3D ∩ (−P_8) = ∅. The upper bound N ≤ 8a+1 is Chevalley–Warning.
- **a = 2.**
  - The capped exact DFS (`dead_a2.out`) and 66,641 greedy runs (`dead_a2_greedy.out`) found
    dead banks of size 8 and none of size 9.
  - The greedy runs found a dead 8-bank that is not of block form:
    (24,20)×4, (28,39)×3, (27,38), where (27,38) is not a multiple of (28,39).
  - NOT proved that N(8,2,41) = 9.
- **Refutation of a linear node** in the sense "columns admitting only s = 0 at arity c·a" is
  impossible for c ≥ 8 + 1/a.
- **Polynomial-time finding at O(a) columns: UNKNOWN.**
  - The best known is now degree 4.
  - Proposition F excludes the whole descent calculus.
  - A three-level joint contraction (degree 3) at (41, 8) was searched by SAT. The search
    timed out undecided after 1500 s (§9, item 7), so degree 3 there is NOT computed.

## 7. The window [c−1, 2c+o(c)]: what each model gives

**Proposition U (time-unbounded label-combining model; PROVED).** In the model of the new-routes
note §2, single-output trees reach E = c. Each node uses N(κ_d, a_d, p) ≤ κ_d a_d + 1 columns
(Chevalley–Warning) and exhaustive search. So E ≤ c, and Theorem LB(iv) gives E ≥ c, or
E ≥ c−1 with stage-2 multi-output.

So in that model the window is [c−1, c]. Nothing above c can be proved there, and the
remaining gap of 1 is the MO2 question.

**Polynomial-time models.**
- Upper bound: 2c−1 for p > T_A(c), conditional; 25 at c = 9 over all primes (R7,
  conditional); 38 at the core standard. All law-free.
- Lower bound: no polynomial-time lower bound above c−1 exists in any model here. The only
  hardness known is the PRF-conditional Theorem H of 11-08, which covers the promise regime
  M ≤ 2a − log_κ p + O(1). That regime lies below the total regime, where the nodes operate.
- Route toward ≈ c: it needs nodes with arity a^{1+o(1)} at every grade with κ_d ≥ 2. By
  Proposition F, such nodes must lie outside every tensor/stage construction known here,
  including IS Lemma 12, chains, union targets and this descent. UNKNOWN.

## 8. What changes in the paper (proposed text only; nothing was edited)

In core Outlook, "Shorter zero sums in Schedule 1", after "…from \ReesClassNineQueryExp to 53
without Schedule 2 (…)", add:

> A second elementary device lowers it further. If $\kappa_d$ is even and $-1 \notin P_{\kappa_d}$,
> a solution for exponent $\kappa_d/2$ has its coefficients in $P_{\kappa_d}\cup(-P_{\kappa_d})$, so it is a
> collision of two disjoint representations with $\kappa_d$-th-power weights; in general, any
> $\kappa_d/2$-solution gives a vector with two disjoint representations whose ratio is explicit. Once
> $p+1-(\kappa_d-1)(\kappa_d-2)\sqrt p > 3\kappa_d$ every nonzero element is $u^{\kappa_d}+\varepsilon v^{\kappa_d}$, so one
> Gaussian elimination on $a+1$ such vectors finishes, and grade $d$ costs the degree of the
> $\kappa_d/2$-solver plus one. With Schedule~1 as the inner solver this gives the class-nine
> exponent at most $38$ for every prime $p>9$, with equality at $p \equiv 1 \pmod{2520}$ (finite computation
> and the Weil bound; AI-checked, pending human review).

In core Outlook, "Smaller arities" (conditional paragraph), replace "law-free worst case 37" by:

> … the law-free per-grade worst case over $p>9$ at $c=9$ is $25$, attained where $\kappa_9 = 9$ and no
> chain exists ($p = 37, 73$); combining representations as above removes the degree-$24$ grade
> $\kappa_8 = 8$ at $p = 41$, which now costs degree $4$ (conditional; finite computations; AI-checked,
> pending human review).

No change to thm:main, the macros, the abstract or numbers.tex. Making 38 the stated count
is the owner's decision. It would need the proof of Lemmas S and F (≈ half a page) in the
core, and a referee pass first.

## 9. Exact checks

| # | script → output | result |
|---|---|---|
| 1 | `union_step.py 41 8 3` → `union_step_41_8.out`; `41 4 1`; `witnesses_41.out` | union steps at (41,8): exactly 10 targets with \|K\| ≤ 3, each containing an antipodal pair; κ = 4 contraction at 41 |
| 2 | `collision_descent.py 3` → `collision_descent.out`; `collision_descent_paths.py` → `.out` | κ = 8, p = 41, plan "2 stages + F1", a ≤ 3: 54/54 verified; path statistics on 1,470 banks, 0 failures (uniform banks always exit early with a solution; repeated-column banks run the full path) |
| 3 | `mrd_execute.py 3` → `mrd_execute.out` | 14 plans (all of §4 for even κ, including the three (41,8) plans), a = 1, 2 (17,8 at a = 1 only): 324/324 verified |
| 4 | `mrd_execute.py 3 '<plan>'` → `mrd_execute_r7.out` | (11,5) and (71,7) union-stage plans: 48/48 verified |
| 5 | `exponents_hcd.py`, `exponents_r7.py`, `exponents_s1h.py` → `.out` | tables of §0 and §5; R5 reproduces the discharge note (37 at c = 9) |
| 6 | `dead_a1.py` → `dead_a1.out`; `dead_a2.py`, `dead_a2_greedy.py` → `.out` | N(8,1,41) = 5 exact; a = 2: max dead found 8 (capped and sampled) |
| 7 | `sat3.py 41 8 0` + kissat (28,864 vars, 1,735,125 clauses; CNF in the session scratchpad, regenerable) | three-level contraction at (41,8): **NOT computed** (kissat timeout at 1500 s, exit 124). Encoding positive control: (41,4) SAT in seconds, model decoded and verified by `sat3.py --check` (class conditions, B(0) ≠ 0, annihilation of 50 random elements of W^{⊗3}) |
| 8 | `sat3.py 37 9 0` + kissat, CaDiCaL LRAT, fixed `lrat-check` (controls OK first) → `sat3_37_9_lrat.out` | **no three-level contraction at (37, 9)** for g = 2, the least primitive root. kissat UNSAT in 30 s; CaDiCaL UNSAT; 4.7 GB LRAT proof checked by the fixed checker, exit 0 (certified; proof deleted afterwards, regenerable). CNF sha256 prefix c00a76cec23e16d2. The gauge fixing F2(0,·) = F3(0,·) = F3(·,0) = 0 loses no solutions (three slice shifts, applied in that order) |

## 10. Adversarial self-check

- *Is Lemma S really law-free?*
  - The inner node's output must have all its nonzero coefficients in two classes, for every
    input. The D-solver does (P_D = Q_0 ∪ Q_{κ/2}), and so does the union step (checked
    entry by entry).
  - Objects are arbitrary vectors (zero, repeated, dependent), and the inner nodes are
    worst-case.
  - Disjointness holds because different objects have disjoint supports and the reps of one
    object are disjoint.
- *Hidden law or adaptivity?* None. The tree shape is public and fixed. Early exits only
  return a solution sooner, and the arity is the stated product.
- *The κ = 4 inner solver at 41.* It is IS Lemma 12 with ℓ = 2 plus an explicit 4×4
  contraction. Neither power-sde(ii) nor the E_2 tables are needed at this prime. The
  explicit witnesses are 16 + 64 field checks.
- *Status of the union step.* Its use as a node (classes in K) is the "union target" sentence
  of rem:app-s2-tower-scope, which is AI-checked and generalizes lem:app-s2-witness in one
  line. I re-derived it (x_b = C_ij ω'^κ has class cl(C_ij)) and tested it in §9, items 3–4.
- *Could the 38 hide an error in S1t or t?* The t values come from the discharge code
  (independently reproduced by the referee). S1H only adds the HCD branch. Its F1 test at
  large p is the same Weil inequality already used for t ≤ 3. The S1H F1 branch at Weil
  primes was not run in the executor at large p (p ≤ 89 only).
- *Is 25 robust?*
  - It depends on R5's κ = 9 data (no chain at 37 and 73, a quoted finite search).
  - If a degree-≤ 3 construction for κ = 9 at 37 and 73 existed, the max would move to
    p = 19 (24) and then lower.
  - If the quoted no-chain list missed a chain, 25 could only drop.
  - Capped union searches only make R7 larger.
- *Novelty.* The corpus `been-tried` query returned nothing related. The device is in the
  spirit of IS §3.3 (accumulating representations) and of the Davenport-constant doubling
  argument. I claim no priority.
- *Weakest point.* Proposition F concerns only this calculus. It says nothing about
  non-oblivious finders (lattice, Wagner-type or quantum), so "no linear node" is not
  claimed anywhere.

## 11. Next hard question and next command

The new binding case is κ = 9 at p ∈ {19, 37, 73}, odd κ with no two-class union step.

At p = 37 a joint three-level contraction does not exist (certified, §9 item 8). The cheapest
constructions not yet excluded at 37 are:
- a three-level union step to {0,m}, used as a stage: degree 3 + 2 = 5 with finish F3;
- a four-level joint contraction: degree 4.

No count of variables against constraints has been done for these cases (UNKNOWN). The question: is there a law-free node of degree < 9 at (37, 9), and
likewise at (19, 9) and (73, 9)?

Next command (one process, ≤ 25 min; generalize `sat3.py` to a target K):

    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-12-rees-exponent-k8-attack/sat3.py 37 9 0,3 /tmp/l3_37_9_03.cnf && kissat -q /tmp/l3_37_9_03.cnf

Repeat for m = 1..8. `sat3.py` already accepts any K.

Expected artifact: for each m, either a model verified by `sat3.py --check 37 9 0,m model`, or
an UNSAT certified by LRAT.

Acceptance test:
- SAT for some m gives degree ≤ 5 at (37, 9), so c = 9 R7 at 37 drops from 25 to ≤ 21.
  Then run the same at 19 and 73.
- UNSAT for all m, LRAT-checked, closes this route at 37.
- Still open: the (41, 8) three-level search, which timed out at 1500 s. It matters only for
  degree 3 versus 4.
