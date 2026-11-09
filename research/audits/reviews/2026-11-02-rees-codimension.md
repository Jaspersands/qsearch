# Rees item 4: the hidden-codimension bound (`rem:codim`)

Date: 2026-11-02. Reviewer: Claude Code (Opus 5.5), side session, AI only. **No human
review.** Brief: item 4 of `research/REES_FULL_CAMPAIGN.md`. I take the core (steps 1–5 of
Thm `thm:main`, Schedule 1) as checked, per `2026-11-01-rees-core-proof-check.md`, and
Cor `cor:fpt-r` as checked, per `2026-11-02-rees-fpt-torsion-check.md`. The only files I wrote
are this report and `2026-11-02-rees-codimension/`. `git status --short` was the same before
and after, apart from untracked files of the parallel sessions and my own two paths.

Text read: `docs/papers/rees-hsp/main.tex` lines 156–212, 356–455 and 534–555;
`research/BOUNDED_CODIMENSION_HSP_REDUCTION.md` in full (§§1–5, baselines);
`research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md` in full (§6 is the target);
`research/BOUNDED_CODIMENSION_HYBRID_BOUND.md` lines 1–120 (premises, split and §2, the
classical collision learner); `audits/reviews/2026-10-30-codimension-hybrid-review.md` lines
1–60. No literature verdict is needed: every ingredient is either elementary or is a result of
the paper that has already been checked.

Scripts (new; they import nothing from the repo), in `research/audits/reviews/2026-11-02-rees-codimension/`:

| Script | Checks | Output |
|---|---|---|
| `codim_lib.py` | exact F_p linear algebra; Lie algebras from structure constants; §1 ideal construction with random choices; normalizer; quotient with a random section; BCH product for class ≤ 4 | (library) |
| `filiform_check.py` | every claim of the `rem:codim` counterexample, m = 4..14, two primes each | `filiform_check_out.txt` |
| `reduction_check.py` | §§1–4 on 5,666 pairs (L, h), 22,664 runs, at the Lie-algebra level | `reduction_check_out.txt` |
| `group_check.py` | §§2–3 on the group: 400 brute-force groups (|G| ≤ 16,807), the oracle transported through nonlinear non-homomorphic sections, recursion run on the transported oracle | `group_check_out.txt` |
| `section6_bounds.py` | §6 inequalities in exact integers, worst profile, k = 2..40, 60, 100, 150, 200; the classical branch exponent | `section6_bounds_out.txt` |

Reproduce (about 50 s, a few minutes, about a minute and 25 s):

```bash
cd research/audits/reviews/2026-11-02-rees-codimension && /opt/anaconda3/bin/python filiform_check.py
```
```bash
cd research/audits/reviews/2026-11-02-rees-codimension && /opt/anaconda3/bin/python reduction_check.py 3000
```
```bash
cd research/audits/reviews/2026-11-02-rees-codimension && /opt/anaconda3/bin/python group_check.py 400
```
```bash
cd research/audits/reviews/2026-11-02-rees-codimension && /opt/anaconda3/bin/python section6_bounds.py
```

## 0. Verdicts

| Q | Verdict | Evidence |
|---|---|---|
| F. Filiform counterexample of `rem:codim` | **Correct as stated.** It refutes only the *direct* descent; the reduction solves it in one abelian call | proved + exact computation |
| R1. Maximal abelian ideal (§1) | **Holds**: A is a self-centralizing abelian ideal; dim L ≤ a(a+1)/2, class ≤ 2a−1 | proved; exact checks on 19,940 constructions |
| R2. Learning K = h ∩ A and normalizing (§2) | **Holds** | proved; exact (Lie and group) |
| R3. Oracle transport without a homomorphic section (§3) | **Holds**, for any section, even nonlinear | proved; brute force on 198 transports, 596,801 parent queries |
| R4. Completeness and error (§4) | **Holds**: ≤ m steps; terminal dim ≤ k(k+1)/2, class ≤ 2k−1, every a_d ≤ k | proved; 0 violations in 6,063 nonabelian terminals |
| R5. Cost section (§5, 2^{O(k³ log k)}) | Superseded, not needed. Holds only as a weaker bound | — |
| S6. §6 corollary, 2^{O(k log(k+2))} | **Holds**, conditional on Thm `thm:random-column`, for oracle input (not coset copies) | proved; exact integers, 86 cases |
| S6′. Fixed k, no Schedule 3 | **Holds**, conditional only on the checked core: polynomial time for every fixed k, with the class unbounded | proved |

**No counterexample was found, and no gap breaks the bound.** The withdrawn claim (a direct
descent with Σ_d a_d = k) stays withdrawn. The bound itself is restored by the
abelian-ideal reduction, with the same conditional status as Cor `cor:fpt-r`. There are two
scope conditions that the paper should state: the input must be an ordinary oracle, and k
must be given. Neither is verified by a human.

---

## 1. The filiform counterexample (`main.tex:553`)

L has basis x = e_0, e_1, …, e_{m−1}, with [x, e_i] = e_{i+1} for 1 ≤ i < m−1, and
h = span(e_1, …, e_{m−2}).

*Proof.* Jacobi holds because every bracket has x as one argument, and [e_i, e_j] = 0. Next,
γ_d = span(e_d, …, e_{m−1}) for d ≥ 2, so the class is m−1 and p > m−1 is needed. h is abelian,
so it is a subalgebra; its codimension is 2 (x and e_{m−1} are missing), so k = 2. For
2 ≤ d ≤ m−2, h ∩ γ_d = span(e_d, …, e_{m−2}), so a_d = (m−d) − (m−1−d) = 1. At d = m−1,
γ_{m−1} = span(e_{m−1}) and h ∩ γ_{m−1} = 0, so a_{m−1} = 1. Hence a_d = 1 at every grade
d = 2, …, m−1. Grade 1 has a_1 = 2, and the homogeneous lift has hidden codimension
Σ_d a_d = m, whereas the filtration quotients of the pulled-back subgroup telescope to k = 2.
At grade d, one label λ is uniform on a line K_d^⊥. A witness s ≠ 0 with s^d λ = 0 exists iff
λ = 0, which has probability exactly 1/p. So every grade needs arity at least 2, and a
fixed-arity direct descent has at least 2^{m−2} leaves per terminal sample. ∎

*Exact check* (`filiform_check.py`, m = 4..14 at the least prime > m−1 and at p = 101). Every
assertion above passed, including the 1/p count, obtained by enumerating all p labels against
all s ∈ F_p^*. Two labels do not always suffice either: the least exact success probability
over grades was 0.118–0.225, because −t_2/t_1 need not be a κ_d-th power. The remark says only
"at least two", which is correct.

*The same instance under the reduction.* In every random run, §1 returned
A = span(e_1, …, e_{m−1}) with a = m−1 > 2. Then K = h ∩ A = h and S = N_L(h) = A, since
[x, e_{m−2}] = e_{m−1} ∉ h. S/K is 1-dimensional with trivial hidden subalgebra, so one
abelian HSP call on F_p^{m−1} and one on F_p suffice. The counterexample therefore kills the
direct descent but not the reduction route.

## 2. Reduction §1: the maximal abelian ideal

**Holds.** Step: given an abelian ideal A_j, solve [x, A_j] = 0 and [e_b, x] ∈ A_j for every
basis vector e_b. Both are linear in x, and the second is w·[e_b, x] = 0 for w in a basis of
A_j^⊥. The solution space V contains A_j, because A_j is abelian and an ideal. If V ≠ A_j,
adjoin any x ∈ V \ A_j. Then A_j + F_p x is abelian, and it is an ideal because
[L, x] ⊆ A_j. Each new basis vector satisfies [L, x_i] ⊆ A_{i−1}.

At termination, C = C_L(A) = A. C is an ideal, because
[[y, c], a] = [y, [c, a]] − [c, [y, a]] = 0, using [y, a] ∈ A. If C/A ≠ 0, then L acts on it
nilpotently, since c brackets with L land in γ_{c+1} = 0. The last nonzero term of
C/A ⊃ ([L, C] + A)/A ⊃ ⋯ then lifts to x ∈ C \ A with [L, x] ⊆ A and [x, A] = 0, which
contradicts termination. So L/A ↪ gl(A) faithfully, with image strictly upper triangular in
the flag basis. Hence dim L ≤ a + a(a−1)/2 = a(a+1)/2. Since n_a has class a−1, γ_a(L) ⊆ A;
then γ_{a+j}(L) ⊆ A_{a−j}, so γ_{2a}(L) = 0 and the class is at most 2a−1. Only nilpotence
over F_p is used, never characteristic 0.

*Exact check* (`reduction_check.py`): 19,940 constructions with random choices, on random
subalgebras L ≤ n_N(F_p) (N ≤ 7, p ∈ {7, 11, 13}) and on filiform algebras up to class 11. All
of the following held every time: A abelian, the flag property, C_L(A) = A, both size bounds.
Zero failures.

## 3. Reduction §2: learning K and normalizing

**Holds.**
- *K ≠ 0 when a > k.* dim(h ∩ A) ≥ dim A − codim h ≥ a − k > 0.
- *The restricted oracle is an abelian HSP oracle.* For x, y ∈ A, BCH(−x, y) = y − x, because A
  is abelian. So f restricted to exp(A) has level sets exactly x + (h ∩ A); in Lazard terms,
  exp(h) ∩ exp(A) = exp(h ∩ A), since exp is a bijection. The *complete* K is learned, not a
  verified subset of it; the note's §4 counterexample explains why a subset is not enough.
- *h ≤ S = N_L(K).* For y ∈ h and x ∈ K, [y, x] ∈ h (h is a subalgebra) and [y, x] ∈ A (A is
  an ideal), so [y, x] ∈ K. K is an ideal of S by definition. exp(S) is a subgroup, exp(K) is
  normal in it, and exp(S)/exp(K) ≅ exp(S/K) by naturality of BCH (Lazard), with
  class(S/K) ≤ class(L) < p.
- *Codimension.* codim_{S/K}(h/K) = dim S − dim h = codim_L h − (m − dim S) ≤ k, and
  dim S/K < m.

*Exact check.* At the Lie level, 13,877 steps: dim K ≥ a − k, h ≤ N(K), K an ideal of S, the
codimension identity, Jacobi for S/K, class(S/K) ≤ class(L). Zero failures. At the group level
(`group_check.py`, 198 restrictions), K was read from the oracle alone. Its level set in exp(A)
was a subspace of size p^{dim K} equal to h ∩ A, there were exactly p^{a − dim K} labels, and
the labels were invariant under every K basis vector. exp(K) was normal in exp(S) on sampled
conjugates. Zero failures.

## 4. Reduction §3: oracle transport without a homomorphic section

**Holds, and more generally than stated.** Let τ: S/K → exp(S) be *any* map with
π∘τ = id, where π: exp(S) → exp(S/K) is the quotient homomorphism. It need not be linear or a
homomorphism. Put f_new = f∘τ. If f(τq_1) = f(τq_2), then τ(q_1)^{-1}τ(q_2) ∈ H, so
q_1^{-1}q_2 ∈ π(H). Conversely, q_1^{-1}q_2 ∈ π(H) gives
τ(q_1)^{-1}τ(q_2) ∈ π^{-1}π(H) = H·exp(K) = H, because exp(K) ⊆ H. One f_new query costs one f
query, plus reversible evaluation and uncomputation of τ. Composed sections stay linear maps
on coordinates, and h = σ(h/K) + K unwinds the recursion. ∎

*Exact check* (`group_check.py`, 400 groups with BCH for class ≤ 4 at p ∈ {5, 7}). At level 0,
BCH agreed with log(exp X · exp Y) of the matrix realization in 3,920 checks. The quotient law
q_1·q_2 := π(σq_1 · σq_2) did not depend on the representatives σq + K, and it equaled BCH on
the computed structure constants of S/K (2,970 checks). The oracle was transported through
τ(q) = σ(q) + κ(q), with κ a random *function* into K. That τ is neither linear nor
homomorphic, yet f_new had exactly p^{codim} labels and was constant on every left coset
q·exp(h/K). The recursion ran on the transported oracle (596,801 parent queries). At each
terminal, the hidden subgroup was read from the transported oracle by brute force; this
stands in for the terminal solver, which is not under audit here. The unwound span equaled
h in all 800 runs. One bug, in my own coset-labelling code, produced 4 spurious failures; it
was fixed before the recorded run.

## 5. Reduction §4: completeness and error

**Holds.**
- *Termination.* Each step lowers the dimension by at least dim K ≥ 1, so there are at most m
  steps and at most m abelian calls. The loop stops when the remainder is abelian (abelian
  HSP), when k = 0 (h = whole algebra), or when a ≤ k.
- *Terminal size.* If a ≤ k, then dim ≤ k(k+1)/2 and class ≤ 2k−1, by §2. In addition, every
  Rees label rank satisfies a_d = dim γ_d − dim(h ∩ γ_d) ≤ codim h ≤ k, because γ_d/(h ∩ γ_d)
  injects into L/h. The actual class c* ≤ c < p is used for Lazard; the bound 2k−1 is not.
- *Error.* T exact Fourier samples are uniform in K^⊥ and fail to span it with probability at
  most p^{r−T}. The span of the samples always satisfies K̂ ⊇ K. The split used by the hybrid
  review (ε/4 for rank and ε/4 for approximation over the abelian calls, ε/2 for the terminal)
  is valid.

*Exact check.* 6,063 nonabelian terminals, with the promise k both fixed and updated to
k − (m − dim S). There were zero violations of dim ≤ k(k+1)/2, class ≤ 2k−1 or a_d ≤ k, no
recovery mismatches, and never more than m steps. The largest terminals observed were
(dim, class) = (3, 2) at k = 2 and **(6, 3) at k = 3**, so the dimension bound is attained at
k = 3. The observed class never exceeded k. That suggests class ≤ a may hold, but it is not
proved, and the bound 2k−1 is all §6 uses.

## 6. Reduction §5 (cost) and the hybrid note

§5's bound 2^{O(k³ log k)} uses the earlier scalar-line terminal solver.
`BOUNDED_CODIMENSION_HYBRID_BOUND.md` improves it to 2^{O(k² log k)}: Schedule 2 above
P_k = 16(2k)^{4k+2}, classical collisions below. §6 improves it again by lowering the threshold
to 64k². None of these three is needed once §6 holds. The classical collision learner of the
hybrid note (§2: label-only pair selection, x^{-1}y exactly uniform in H, capped batches)
is the small-prime branch below. Its error accounting was reviewed on 10-30 and is consistent
with my reading.

## 7. The §6 corollary

**Holds, conditional on Thm `thm:random-column`.** Apply Schedule 3 to the terminal with
u = 2k and M = 8k. Its hypotheses hold for every k ≥ 2: u ≥ 2, c* ≤ 2k−1 ≤ u,
a_d ≤ k ≤ u−1, and p ≥ 16u² = 64k². (u = 2k−1 also works.) The terminal's sources come from
the Rees tuple lift applied to the transported oracle, which is a genuine coherent hiding
oracle for H_T on G_T. So Lemma `lem:central` gives the i.i.d. uniform label law that
Schedule 3 uses, exactly as in Cor `cor:fpt-r` A2. Each lifted source costs c* terminal
queries, and each of those costs one original query plus poly(m) section arithmetic.

*Exact check* (`section6_bounds.py`) at the worst profile, c = 2k−1 and a_d = k at every grade,
with the true κ_d, for the least prime ≥ 64k² and for 2^61−1. In all 86 cases (k ≤ 200):
μ ≥ 2^{8u+1}u^{2u+1}, acceptance ≥ 1/(4κ^M), bank sum ≤ 1/64 (log₂ ≤ −83) and tree abort
≤ 1/16. log₂(queries per tree)/(k log₂(k+2)) ≤ 3.31, and log₂(classical trials per tree) over
the same scale is ≤ 12.74.

*Small primes, p < 64k².* The classical collision learner runs on the original instance. Its
batch size is B = ⌊√(2p^k)⌋ + 2, and log₂ B/(k log₂(k+2)) ≤ 2.34 for k ≤ 200; in general
log₂ B ≤ k(3 + log₂ k) + 2. So this branch costs 2^{O(k log(k+2))}·poly(m, log p, w, log(1/ε)).
It is classical, it needs Lazard log only (so c < p), and it makes ordinary oracle queries.

*k ≤ 2.* For k = 1 the terminal is abelian. For k = 2 it has dim ≤ 3 and class ≤ 2, so Thm
`thm:main` at c = 2 (Schedule 1, the checked core) applies for every p > 2, and Schedule 3 is
not needed.

*Fixed k (S6′).* The terminal class is at most 2k−1, a constant, so Thm `thm:main` (Schedule 1)
on the terminal gives polynomial time for every p > c. This version depends only on the
checked core and this reduction, not on Schedule 3, but the exponent grows with k. I did not
check whether Ivanyos–Santha's running time is uniform in d, so this route gives no FPT
statement.

## 8. Falsifier hunt

- The filiform family, m ≤ 14: the counterexample holds exactly against the direct descent and
  fails against the reduction (§1).
- 5,666 random (L, h) pairs, codim 0..11, class up to 11, both promise policies, random flag
  choices and random complements: no violation of any bound in §§2–5, and h was always
  recovered.
- 400 brute-force groups at p = 5 and 7, the smallest primes the BCH check allows: the
  transport was exact through nonlinear sections, and the recursion ran on the transported
  oracle.
- §6 inequalities at the worst admissible profile, k ≤ 200: no failure.
- Smallest instance that would matter: none exists. Finite checks only falsify (TRAPS 7); the
  bound rests on the written proofs in §§2–7.

## 9. What now holds, what is missing, gates, text fixes

**Exact statement (surviving).** Let p be prime and L ≅ F_p^m an explicit F_p-Lie algebra of
class c < p, with c **not** fixed. Let G = (L, ∗), let H ≤ G be any subgroup with
codim_{F_p} log H ≤ k, where k is **given**, and let f be an **ordinary** coherent left-coset
hiding oracle of label width w and cost T_f. Coset-copy input is not covered, because the
restriction to exp(A) and the classical branch both query f. Then:

1. *(Every fixed k; conditional only on the checked core.)* A bounded-error quantum algorithm
   returns a basis of log H with probability ≥ 1−ε in time poly(m, log p, w, log(1/ε)), plus
   Q·T_f. The exponent depends on k.
2. *(FPT; additionally conditional on Thm `thm:random-column`, AI-checked only.)* The same holds
   in non-oracle time 2^{O(k log(k+2))}·poly(m, log p, w, log(1/ε)), with
   Q = 2^{O(k log(k+2))}·poly(m, w, log(1/ε)) oracle queries. The O(·) constants are absolute.
   Routes: for k = 0, no query is needed; for p ≥ 64k², at most m abelian HSP calls and
   transports, then Schedule 3 on the terminal with u = 2k, M = 8k; for p < 64k², the
   classical collision learner, with cost p^{k/2}·poly; for k ≤ 2, the terminal has class
   ≤ 2 and the checked core suffices.

This is a gap between upper bounds, not a separation. At fixed k and polynomial-size p the
classical p^{k/2} learner is also polynomial.

**Still missing.** Human review. An independent proof check of Thm `thm:random-column` (same
status as for Cor `cor:fpt-r`). A priority assessment of the composite: the abelian-ideal and
normalizer steps are standard, and a normalizer recursion of this kind appears in
Ivanyos–Sanselme–Santha, as the paper already cites for `thm:ring-to-field`. I did not
assess novelty. Also open, and optional: a proof of class ≤ a for self-centralizing abelian
ideals, which would improve only constants.

**Claim gates that must stay false.**
- `research/reductions/codimension_hybrid_budget.json`: `proof_promotion`,
  `candidate_promotion`, `quantum_receiver_implemented`, `native_application_established`,
  `speedup_claim_allowed`, every case's `growing_class_pointwise_correctness_certified`,
  `hidden_intersection_completeness_certified`, `solver_implemented`, `novelty_established`.
- `research/reductions/random_column_rees.json`: `whole_rees_correctness_certified`,
  `joint_source_law_verified`, `fixed_bank_success_guaranteed`, `intrinsic_rank_promise_verified`,
  `quantum_receiver_implemented`, `novelty_established`, `speedup_claim_allowed`.
- `research/reductions/rees_hsp_reduction.json`: `independent_review`, `novelty_established`,
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`,
  `formal_compiler_checked`. `normalizer_recursion_required` stays false: the *core* needs no
  normalizer recursion. Only this corollary uses one.

**Text fixes for `main.tex` (ranked; listed, not applied).**
1. **`main.tex:551–554`.** Replace Remark `rem:codim` with a corollary plus a remark:

   > **Corollary (hidden codimension; conditional).** Let $\codim_{\Fp}\hh \le k$ with $k$
   > given, $c<p$ not fixed, and let $f$ be an ordinary coherent hiding oracle (coset-copy
   > input is not covered). (i) For each fixed $k$ the HSP is solvable with bounded error in
   > time $\poly(m,\log p,\text{label width},\log(1/\eps))$. (ii) Conditional also on
   > Theorem~\ref{thm:random-column}, it is solvable in time
   > $2^{O(k\log(k+2))}\cdot\poly(m,\log p,\text{label width},\log(1/\eps))$, plus the
   > oracle's internal cost.
   >
   > *Proof.* Build a maximal abelian ideal $A$ by adjoining any $x$ with $[x,A]=0$ and
   > $[\mathcal{L},x]\subseteq A$. Then $C_{\mathcal{L}}(A)=A$, so
   > $\mathcal{L}/A$ embeds in strictly triangular $\mathfrak{gl}(A)$, giving
   > $\dim\mathcal{L}\le a(a+1)/2$ and class at most $2a-1$, where $a=\dim A$. If $a>k$,
   > $K=\hh\cap A\neq 0$ is found by abelian HSP on $\exp A$. Next, $\hh\le S=N_{\mathcal{L}}(K)$,
   > and for any section $\sigma$ of $S\to S/K$, $f\circ\exp\circ\sigma$ hides $\exp(\hh/K)$ in
   > $\exp(S/K)$ at one query per query. Recurse; after at most $m$ steps the remainder is
   > abelian, or it has dimension $\le k(k+1)/2$, class $\le 2k-1$ and
   > $a_d\le\codim\hh\le k$ at every grade. (i) follows from Theorem~\ref{thm:main} at class
   > $\le 2k-1$. For (ii), when $p\ge 64k^2$ use Theorem~\ref{thm:random-column} with
   > $u=2k$; when $p<64k^2$, $p^{k/2}=2^{O(k\log(k+2))}$, so the classical birthday learner
   > (uniform $x^{-1}y$ from label collisions) suffices. Unwind with
   > $\hh=\sigma(\hh/K)+K$.

   Keep the filiform paragraph as a remark explaining why the *direct* descent cannot give
   this bound. Add one sentence saying the reduction disposes of it in one abelian call
   ($A=\Span(e_1,\dots,e_{m-1})=N(\hh)$).
2. **`main.tex:201`.** "is withdrawn; see Remark" → "now follows from an abelian-ideal
   reduction instead (Corollary …)". Keep the sentence saying the pulled-back proof is
   withdrawn.
3. **Table `tab:main-regimes`.** Add the row: "Hidden codim. $k$ | all $p>c$ (oracle input) |
   abelian-ideal reduction, then random column ($p\ge 64k^2$) / classical birthday
   ($p<64k^2$) | $2^{O(k\log(k+2))}\cdot\poly$ total".
4. **`main.tex:208`.** No change needed, since "treats … hidden codimension" becomes true again.
5. **The reduction note §5 (not `main.tex`; for the parent to fold in).** Mark its
   2^{O(k³ log k)} terminal cost as superseded by `RANDOM_COLUMN_REES_PARAMETER_BOUND.md` §6,
   and record that the (6, 3) terminal at k = 3 attains the dimension bound.
