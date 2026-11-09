# Rees Schedule 3: the witness sampler at FCS grades with h ≥ 3 (2026-11-05)

**Status: AI-checked, pending human review.** Overnight AI-only pass, no owner input. No `.tex`
file, registry/JSON claim gate, `AGENT_HANDOFF.md` or `STATE.md` was edited; nothing committed;
no git, no network. Code and outputs: `research/audits/reviews/2026-11-05-rees-s3-witness-h3/`.

Labels: **[proved]** full proof here (or by label from the paper or the two 11-05 arity
reports); **[computed]** exact or Monte Carlo computation in the folder, every algorithmic output
checked exactly; **[cited]** outside result, from memory, **NEEDS HUMAN VERIFICATION**;
**[conjecture]** not proved.

## Summary

Setting: a grade d ∈ Γ_F, κ = κ_d = gcd(d, p−1) with 2 ≤ κ < p−1, h = (p−1)/κ ≥ 2, digit set
D = P_κ ∪ {0} = μ_h ∪ {0}. Witness problem W(h; n, M, p): given i.i.d. uniform columns of F_p^n,
find y ∈ D^M, y ≠ 0, with Σ y_i v_i = 0. At h = 2 it is ternary SIS (A5 of the 11-04 report),
at h = 1 binary SIS (Γ_0, rem:fc-zero-sum-arity).

1. **(A) achieved, in this form [proved]: Theorem H.** The weight-doubling recursion of
   rem:fc-zero-sum-arity works for every digit set μ_h ∪ {0}. Put D_0 = D, D_{j+1} = D_j − D_j,
   and let **j\*_h = j\*_h(p)** be the least J with D_J = F_p. The level-0 solver reads
   E[R] = N_0(n) columns, a polynomial in n of **exact degree 1 + j\*_h** (leading coefficient
   s_p^{j\*_h}/(1+j\*_h)!), returns an exactly checked witness, and runs in time
   O(R(n² + p) + j\*_h p²). The fixed-arity node at an FCS grade (Cor. H.6) has arity
   M_d = Θ_p(g_d^{1+j\*_h} log(1/τ)), aborts with probability ≤ τ (+ the usual capped steps), and
   converts as in (F4)–(F6). The node was run at h = 3 (p = 7, 13, 19, 31) and h = 4
   (p = 13, 17; p = 5 is κ = 1): 7046 node trials, 9 aborts (all span failures), no wrong output.
2. **The depth [proved + computed].**
   - j\*_h ≤ ⌈log₂ κ⌉ always (Cauchy–Davenport). So at every FCS grade the degree is
     ≤ 1 + ⌈log₂ κ_d⌉ ≤ 1 + ⌈log₂ c⌉, for every p and h.
   - j\*_h = 1 (quadratic arity) whenever √p > (κ−1)(κ−2) + 3 (Jacobi sums). In that range a
     scaled variant (switches scaled to β = 2^k, random splitting) runs in time
     poly(n, κ, log p) (Thm H′); it was run at p = 2^31−1 (κ = 3) and p = 2^61−1 (κ = 6).
   - For fixed h, writing φ = φ(h): **j\*_h = log₂ p / φ(h) + O_h(1)**, with explicit lower and
     upper bounds from the ring Z[ζ_h] (Lemma J(iii)–(iv)). Computed for all primes
     p ≡ 1 (mod h) below 6·10⁴ (h = 3, 4, 6) or 2–3·10⁴ (h = 5, 7, 8, 10, 12):
     j\*_3 − (log₂ p)/2 ∈ [−0.85, 0.60] over 3014 primes.
   - Test primes: j\*_3 = 1, 1, 2, 2 at p = 7, 13, 19, 31; j\*_4 = 1, 2 at p = 13, 17. So the
     node has degree 2 or 3 there, against Schedule 1's κ⌈log₂(κ+1)⌉ = 4, 12, 18, 40 and 6, 12,
     and against 1 + ⌈log₂(p−1)⌉ = 4, 5, 6, 6 and 5, 5 for Theorem P applied through {0,1} ⊆ D.
3. **(B) barriers [proved].**
   - **B0, existence (any algorithm, any time).** Here arity means the total number of labels
     read, the labels being i.i.d. uniform on a space of dimension a. At arity M a witness
     exists with probability ≤ ((h+1)^M − 1)/p^a < (h+1)^{M−a} q^a. So at arity a + O(1) every
     method succeeds with probability ≤ (h+1)^{O(1)} q^a. **In the regime h < κ^{o(a)}, the
     paper's open question "time κ^{a−Ω(a)} at arity a + O(1)" has a negative answer as
     literally stated.** When log h ≳ a log κ (large p at fixed κ), arity a + O(1) is at or
     above the threshold and B0 says nothing. It
     should be posed near the existence threshold a·log_{h+1} p, which the FCS arity of
     lem:fc-choice already matches up to log h versus log(h+1) (Imprecision in main.tex; text
     proposed in Part F).
   - **B5_h, depth.** Every switch hierarchy (any number of options per switch, any scalar
     rescaling per level) with a linear-algebra base has depth ≥ j\*_h(p), and
     j\*_h(p) ≥ log₂((p^{1/φ} − 1)/(2c_h)) with c_h = max_t ‖ζ_h^t‖₁ in the power basis. So for
     fixed h ≥ 3 the *depth* of every such recursion grows like log₂ p/φ(h), and the degree of
     Theorem H's own template, 1 + j\*_h, does too. That the *degree* of every switch hierarchy
     grows with its depth is **[conjecture]** (B5_h, "Per level").
   - **B2_h.** The level-0 switch-recursion bound Ω_p(n²/log n) of the arity report holds for
     μ_h-digits with 2M replaced by |D_1|·M. At j\*_h = 1 the sampler is therefore within a
     log factor of optimal for its template.
   - **Lattice form (exact).** W(h) on a uniform bank is exactly Module-SIS over R = Z[ζ_h]
     modulo the degree-one prime 𝔭 = (p, ζ_h − ω), with solutions in μ_h ∪ {0}. For even h,
     by Kronecker's theorem, this is exactly M-SIS_𝔭 with canonical-embedding ℓ∞ bound 1. So a
     solver for W(h) solves that M-SIS_𝔭 instance (W(h) is at least as hard). I know no
     worst-case hardness theorem for this modulus; hardness stays **[conjecture]**.
     Conversely, W(h) is no harder than ternary SIS (h even) or binary SIS (h odd) at the same
     parameters.
4. **Consequence for thm:free-coordinate(iii) at fixed c [proved, conditional as (iii) is;
   computed exponents].** With these nodes at every grade of Γ_F, and rem:fc-zero-sum-arity at
   Γ_0, (iii) holds with polynomial classical time at fixed c for every prime p > c. The FCS
   nodes need 2^{O(g_d log κ_d)} trials. The exponent of m in the query count, maximized over
   all p > c, is at most **19 at c = 9** (25 at c = 12). The combined rule, which needs no
   label law, has 143 at c = 9. FCS nodes give exponent ≈ c but exponential time. Owner
   decision only; nothing is adopted, and no table or gate changes.
5. **Not reached.** A sampler whose degree is bounded for fixed h uniformly in p; any o(g²)
   arity; the κ^{a−Ω(a)} question at threshold arity; hardness of M-SIS_𝔭.

**Claim gates that must stay false:** all Rees gates, including "polynomial-time Schedule 3"
(the query count stays ≥ 2^{c−1}; item 4 is fixed-c only, where Theorem main is already
polynomial), "hardness of the witness problem", "o(a²) SDE solver", and any novelty claim.

## 0. Problem, quantifiers, access model

- **W(h; n, M, p), average case.** v_1, …, v_M i.i.d. uniform in F_p^n. Output y ∈ D^M \ {0}
  with Σ y_i v_i = 0, D = μ_h ∪ {0}. Success probability is over the columns and coins.
- **Node at d ∈ Γ_F.** The bank is i.i.d. uniform on the unknown K_d^⊥ of dimension a ≤ g_d
  (`lem:fc-forest`(a)). The node may abort and never returns a wrong witness. A witness y
  becomes s with s_i^d = y_i by (F4), is checked by (F5) and converted by (F6).
- **Classical access.** All algorithms are classical. B0 and B5_h hold for unbounded
  computation. B2_h holds within its model.

## H. The μ_h-digit weight-doubling sampler

### H.1 Digit chain

Fix p, h | p−1, κ = (p−1)/h. D_0 = μ_h ∪ {0} ⊂ F_p and D_{j+1} = D_j − D_j. Fix public tables
x_j, x'_j : D_{j+1} → D_j with x_j(α) − x'_j(α) = α and x_j(0) = x'_j(0) = 0. In the code, the
least x ∈ D_j with x − α ∈ D_j.

**Lemma 0 [proved].** 0, 1 ∈ D_j and D_j ⊆ D_{j+1} for all j. Also
|D_j| ≥ min(p, 2^j h + 1). Hence j\*_h exists and j\*_h ≤ ⌈log₂ κ⌉, with j\*_h = 0 iff κ = 1.

*Proof.* 0, 1 ∈ D_0. Then a = a − 0 gives D_j ⊆ D_{j+1}. By Cauchy–Davenport,
|A − B| ≥ min(p, |A| + |B| − 1) [cited, classical], so |D_{j+1}| ≥ min(p, 2|D_j| − 1). With
|D_0| = h+1, induction gives |D_j| ≥ min(p, 2^j h + 1). Finally 2^J h + 1 ≥ hκ + 1 = p iff
2^J ≥ κ. ∎

Consistency [computed, `run_depth.py`, 163 cases]: the FFT and set computations agree.
j\*_1(p) = ⌈log₂(p−1)⌉, the j\* of rem:fc-zero-sum-arity, and
j\*_2(p) = ⌈log₂(p−1)⌉ − 1 = ⌈log₂ κ⌉, so Cauchy–Davenport is tight at h = 2.

### H.2 Algorithm 𝒜_j(d, y) (level j ≤ j\*_h, dimension d, target y ∈ F_p^d)

This is rem:fc-zero-sum-arity(a) / Theorem P of the arity report, with D^{(j)} → D_j,
j\* → j\*_h, and the halving split → the tables.
- **j = j\*_h** (only y = 0). Read d+1 fresh columns and return the nonzero entries of a nonzero
  kernel vector of their first d coordinates (entries in F_p = D_{j\*_h}). At d = 0: one
  column, weight 1.
- **j < j\*_h, d = 0.** One fresh column, weight 1.
- **j < j\*_h, d ≥ 1.** Let π drop coordinate d.
  1. *Switches.* Repeat: run 𝒜_{j+1}(d−1, 0) on fresh columns, giving (I_k, α_k). Put
     β_k = Σ_i α_{k,i} v_{i,d}, x_k = x_j(α_k), x'_k = x'_j(α_k). Stop at the first K such
     that the subset sums of β_1..β_K (empty sum included) cover F_p, and record T_a for each a.
  2. u = Σ_k Σ_{i∈I_k} x'_{k,i} v_i[1..d].
  3. *Recurse:* 𝒜_j(d−1, π(y − u)) on fresh columns, giving (I', w').
  4. a = (y − u − Σ_{I'} w'_i v_i)_d. Return w' on I', and on each block I_k either x_k
     (k ∈ T_a) or x'_k. Drop zero weights.

### H.3 Theorem H and proof

**Theorem H [proved].** For every prime p, every h | p−1 and every n ≥ 0, the following hold.
- 𝒜_0(n, 0) halts with probability 1.
- It returns distinct indices and nonzero weights in D_0 with Σ w_i v_i = 0.
- Its read count R satisfies E[R] = N_0(n), where N_{j\*_h}(d) = d+1 and
  N_j(d) = 1 + s_p Σ_{e<d} N_{j+1}(e). Here s_p is the expected number of uniform draws until
  their subset sums cover F_p, the same s_p as in Theorem P.
- N_0(n) ≤ (s_p+1)^{j\*_h} C(n+j\*_h+1, j\*_h+1) and
  N_0(n) = s_p^{j\*_h} n^{1+j\*_h}/(1+j\*_h)! + O(n^{j\*_h}).
- Time: O(R(n²+p)) field operations, plus O(j\*_h p²) once for the tables.

*Proof.* By induction on (j\*_h − j, d), every call 𝒜_j(d, y) has the following properties.
- **(P1)** It reads only coordinates 1..d of its columns, and its stopping decisions depend on
  those coordinates alone.
- **(P2)** It returns a nonempty index set and nonzero weights in D_j with weighted sum y.
- **(P3)** Its read count does not depend on y, and its expectation is N_j(d).

The base cases are clear.

- **Weights.** x_k and x'_k lie in D_j by the tables. w' lies in D_j by induction.
- **Nonempty.** The recursion's output is nonempty. At d−1 = 0 it is one column with weight 1,
  and 1 ∈ D_j. It is disjoint from the switch blocks, since all reads are fresh.
- **Sum.** Σ_i (x_k − x'_k)_i v_i[1..d] = Σ_i α_{k,i} v_i[1..d] = β_k e_d, because α_k is a
  relation on coordinates 1..d−1. So the output sum is Σ w'v + u + a e_d.
  - Its π-part is π(y − u) + π(u) = π(y).
  - Its d-th coordinate is y_d, by the choice of a.
- **Law of β.** Let F_{k−1} be everything read before block k. Block k is a fresh call, so its
  columns are i.i.d. uniform given F_{k−1}. By (P1) for 𝒜_{j+1}(d−1, ·), the outputs (I_k, α_k)
  and the read count C_k are functions of coordinates 1..d−1 of block k. Given F_{k−1} and
  those coordinates, the d-th coordinates of block k are still i.i.d. uniform. α_k is a
  nonzero vector by (P2). So β_k is uniform and independent of (F_{k−1}, C_k, α_k).
- **Termination.** Let R ≠ F_p be the current set of subset sums and β ≠ 0. If R + β = R, then
  R is a union of cosets of ⟨β⟩ = F_p, which is impossible. So R ∪ (R + β) ⊋ R, and K is a.s.
  finite with E[K] = s_p ≤ p.
- **Wald.** {K ≥ k} ∈ σ(β_1..β_{k−1}), which is independent of block k, hence of C_k. Wald's
  identity gives that the switches read s_p N_{j+1}(d−1) in expectation.
- **(P1).** The switches use coordinates ≤ d. The final choice reads only already-read
  columns. The recursion reads coordinates ≤ d−1 of fresh columns.
- **(P3).** The switch loop ignores y. The recursion's count does not depend on its target, by
  induction. So N_j(d) = N_j(d−1) + s_p N_{j+1}(d−1) with N_j(0) = 1, which telescopes to the
  stated recursion.
  (`wh_lib.solve` recomputes sums in the backward pass, costing O(j\*_h R n²); the stated time
  needs running sums.)
- **Closed form.** Identical to Theorem P (v), with j\* → j\*_h.
- **Leading term.** By induction, N_{j\*_h−k}(d) = s^k d^{k+1}/(k+1)! + O(d^k).
- **Time.** As in Theorem P (vii). Building a table costs O(p·|D_j|) per level. ∎

Comment. Theorem P is the case h = 1. The h = 2 case is its level-1 solver, which has degree
⌈log₂(p−1)⌉.

### H.4 Bounds on j\*_h

Let ω ∈ F_p have order h. Put R = Z[ζ_h], φ = φ(h) = [Q(ζ_h):Q], and let ψ : R → F_p,
ζ_h ↦ ω. This is well defined because Φ_h(ω) = 0 in F_p, and it is surjective. 𝔭 = ker ψ is a
prime of degree one, and R ≅ Z^φ via the power basis 1, ζ, …, ζ^{φ−1}. Let
c_h = max_{0≤t<h} ‖ζ^t‖₁ in power coordinates; c_2 = c_4 = 1, c_3 = c_6 = 2, c_5 = 4. Let
S_k ⊂ F_p be the set of signed sums of at most k elements of μ_h.

**Lemma J [proved].**
- **(i)** j\*_h ≤ ⌈log₂ κ⌉ (Lemma 0).
- **(ii) Weil range.** If √p > (κ−1)(κ−2)+3, then D_0 − D_0 = F_p, so j\*_h ≤ 1. Moreover, for
  y ≠ 0, the number of pairs (u, v) ∈ μ_h² with u − v = y is at least
  (p − (κ−1)(κ−2)√p − 3κ + 1)/κ². If √p ≥ 2(κ−1)(κ−2)+4, a uniform u ∈ μ_h satisfies
  u − y ∈ μ_h with probability ≥ 1/(2κ).
- **(iii) Lower bound, for every switch hierarchy.** Suppose E_0 ⊆ D_0 and
  E_{j+1} ⊆ γ_j(E_j − E_j) with γ_j ∈ F_p^×. Then |E_j| ≤ |D_j| ≤ #{m ∈ Z^φ : ‖m‖₁ ≤ c_h 2^j}
  ≤ (2c_h 2^j + 1)^φ. So E_J = F_p forces J ≥ j\*_h ≥ log₂((p^{1/φ} − 1)/(2c_h)).
- **(iv) Upper bound.** j\*_h ≤ [h odd] + ⌈log₂(c_h φ² p^{1/φ}/2)⌉.
- Hence **j\*_h = log₂ p/φ(h) + O_h(1)** for fixed h.

*Proof of (ii).* Let N(y) = #{(x,z) ∈ F_p² : x^κ − z^κ = y} with y ≠ 0.
- **Characters.** #{x : x^κ = b} = Σ_{χ^κ=1} χ(b), with ε(0) = 1 and χ(0) = 0 for χ ≠ ε, so
  N(y) = Σ_{χ,ψ} Σ_b χ(b)ψ(b−y).
- **Trivial characters.** The term with χ = ψ = ε is p. Terms with exactly one of them
  trivial vanish.
- **Both nontrivial.** Substitute b = yt: the term equals χψ(y)ψ(−1)J(χ,ψ). Here
  |J(χ,ψ)| = √p if χψ ≠ ε, and |J(χ,χ̄)| = 1 [cited: Ireland–Rosen, ch. 8; NEEDS HUMAN
  VERIFICATION of the numbering]. So |N(y) − p| ≤ (κ−1)(κ−2)√p + κ − 1.
- **Pairs.** At most 2κ points have x = 0 or z = 0. The others map κ²-to-1 onto pairs
  (x^κ, z^κ) ∈ P_κ² = μ_h² with u − v = y. This gives the count.
- **Positivity.** With A = (κ−1)(κ−2) and √p > A+3: p − A√p > 3√p > 3(A+3) ≥ 3κ − 1, using
  3(κ−2)² + 4 > 0. So the count is positive, and y = 0 is u − u.
- **Probability.** If √p ≥ 2A+4, then p − A√p − 3κ + 1 ≥ (p−1)/2, and the probability equals
  count/h ≥ ((p−1)/(2κ²))/h = 1/(2κ). ∎

*Proof of (iii).*
- **The sets S_k.** D_0 ⊆ S_1, and S_k − S_k = S_{2k}. So D_j ⊆ S_{2^j}.
- **Scalars do not help.** Induction gives E_j ⊆ Γ_j D_j for Γ_j = γ_0⋯γ_{j−1}, so
  |E_j| ≤ |D_j|.
- **Counting.** S_k = ψ(T_k), where T_k ⊂ R is the set of signed sums of ≤ k powers of ζ.
  Every element of T_k has power-coordinate ℓ₁-norm ≤ c_h k, which gives the count. ∎

*Proof of (iv).*
- **Short vector.** 𝔭 has index p in R ≅ Z^φ. By Minkowski's theorem [cited, classical], the
  cube of side 2p^{1/φ} contains some v ∈ 𝔭 \ {0}, so ‖v‖₁ ≤ φ p^{1/φ}.
- **Sublattice.** vR ⊆ 𝔭 has full rank and basis ζ^t v (t < φ), with
  ‖ζ^t v‖₁ ≤ c_h ‖v‖₁.
- **Short representatives.** Rounding the coordinates of x ∈ R in that basis gives a
  representative of x mod vR (hence mod 𝔭) of ℓ₁-norm ≤ ρ = c_h φ² p^{1/φ}/2. Its power
  coordinates (m_t) satisfy Σ|m_t| ≤ ρ, so F_p = S_{⌊ρ⌋}.
- **Depth.** D_1 ⊇ S_1, and D_1 is symmetric. So D_j ⊇ S_{2^{j−1}} for j ≥ 1, and
  D_j ⊇ S_{2^j} when h is even, since then −μ_h = μ_h. ∎

**[computed]** `run_depth.py` → `depth.json`. Every prime p ≡ 1 (mod h) with p < 60000
(h = 3, 4, 6), p < 30000 (h = 5) and p < 20000 (h = 7, 8, 10, 12) was checked. The bounds
(i)–(iv) held at every prime, and the Weil range always gave j\*_h = 1. The excess
j\*_h − log₂p/φ(h) ranged as follows:

| h | φ | primes | j\*_h − log₂p/φ | j\*_h values (first prime with that value) |
|---|---|---|---|---|
| 3 | 2 | 3014 | [−0.85, 0.60] | 1 (7), 2 (19), 3 (61), 4 (151), 5 (523), 6 (1879), 7 (7207), 8 (28549) |
| 4 | 2 | 3017 | [−0.85, 0.98] | 1 (13), 2 (17), 3 (37), …, 8 (16901) |
| 6 | 2 | 3013 | [−1.12, 0.40] | 1 (13), 2 (31), …, 8 (37663) |
| 5 | 4 | 808 | [0.11, 1.47] | 1 (11), 2 (31), 3 (181), 4 (1361), 5 (17921) |
| 7 | 6 | 377 | [0.10, 1.90] | 1 (29), 2 (71), 3 (379), 4 (6301) |
| 8 | 4 | 556 | [−0.02, 1.66] | 1 (17), …, 5 (10601) |
| 10 | 4 | 562 | [−0.34, 1.21] | 1 (31), …, 4 (2311) |
| 12 | 4 | 554 | [−0.30, 1.14] | 1 (37), …, 4 (2797) |

**Per κ, exhaustive below the Weil range [computed].** For each κ the scan covers every prime
p ≡ 1 (mod κ) with h ≥ 2 up to ((κ−1)(κ−2)+3)²; beyond that, j\*_h = 1 is proved. The table
lists the largest prime with j\*_h ≥ 2 and the histogram of j\*_h:

| κ | Weil range starts | largest p with j\*_h ≥ 2 | histogram {j\*_h: count} |
|---|---|---|---|
| 2 | 9 | none | {1: 2} |
| 3 | 25 | 7 (h = 2) | {1: 2, 2: 1} |
| 4 | 81 | 17 (h = 4) | {1: 7, 2: 1} |
| 5 | 225 | 61 | {1: 7, 2: 3, 3: 1} |
| 6 | 529 | 109 | {1: 38, 2: 6, 3: 1} |
| 8 | 2025 | 337 | {1: 62, 2: 6, 3: 1} |
| 10 | 5625 | 641 | {1: 167, 2: 14} |
| 16 | 44100 | 2593 | {1: 566, 2: 18, 3: 1} |
| 20 | 119025 | 3361 | {1: 1368, 2: 26, 3: 1, 5: 1} |

All rows for κ = 2..20 are in `depth.json`. In these rows the largest p with j\*_h ≥ 2 is at
most 15κ² (the maximum ratio is 14.1, at κ = 15, p = 3181), far below the proved κ⁴ range. **[conjecture]** j\*_h = 1 for p ≥ Cκ² log κ.

At the paper's exceptional primes for two-level contractions:
- E_2(4) = {5, 13, 17, 29, 37, 53}: j\*_h = 2 (at h = 1, p = 5, which is Γ_0), 1, 2, 1, 1, 1.
- E_2(5): j\*_h = 3 at p = 11 (h = 2), 2 at 31, 41, 61, and 1 at 71..181.
- 11689 ∈ E_2(8) and 17911 ∈ E_2(9): j\*_h = 1.

So at most of these primes, where no two-level contraction exists, the sampler has quadratic
average-case arity.

### H.5 The scaled variant at j\*_h = 1 (any size of p)

**Theorem H′ [proved].** Suppose D_0 − D_0 = F_p (for example √p > (κ−1)(κ−2)+3). Let
K = bitlength(p−1). Here is the variant at dimension dd. For k = 0..K−1, draw dd fresh columns
until the kernel vector α of their first dd−1 coordinates has β ≠ 0. Rescale α by 2^k/β, which
is allowed since D_1 = F_p. Split every entry into x − x' with x, x' ∈ D_0, by the table or by
random search: u = b^κ for uniform b ∈ F_p^×, accept if u − α_i ∈ μ_h.
- The backward choice at dd uses the binary digits of the residual a ∈ [0, p). This is
  correct because the subset sums of 2^0..2^{K−1} cover [0, 2^K) ⊇ [0, p).
- The expected read count is exactly 1 + K·(p/(p−1))·n(n+1)/2. Each switch at dd reads dd
  columns per attempt, and an attempt fails only when β = 0, which has probability 1/p.
- With search caps ⌈2κ ln 2 (B + ⌈log₂ M⌉)⌉ and √p ≥ 2(κ−1)(κ−2)+4, all splits succeed except
  with probability 2^{−B} (Lemma J(ii)). The time is poly(n, κ, log p).
- One root per nonzero entry of a split is known: x = b^κ. The other needs lem:s3-root.

*Proof.* Correctness is as in Theorem H, with deterministic covering in place of the covering
loop. The read count follows from geometric redraws, since β is uniform given the first dd−1
coordinates. ∎

**[computed]** `run_misc.py` → `misc.json`, scaled rows:
- **Primes.** (κ, p) ∈ {(4, 101), (3, 2^31−1), (6, 2^61−1), (8, 11689), (10, 6151), (3, 13)},
  with n ≤ 10 and 6–20 runs per row.
- **Correctness.** Every output was checked exactly: weights in μ_h, and the sum is 0. The
  conversion s_i^κ = y_i was checked with sympy's `nthroot_mod`.
- **Reads.** The mean reads equal the exact expectation: 1706 at (3, 2^31−1, n = 10) and 2197
  at (6, 2^61−1, n = 8). There were 0 zero-β events at the large primes.
- **Splitting.** It took 3.01, 6.06, 8.18 and 10.2 trials per search at κ = 3, 6, 8, 10, about
  κ, as predicted.
- **Time.** 0.39 s per run at p = 2^61−1, n = 8.

### H.6 The node at an FCS grade

**Corollary H.6 [proved].** Let d ∈ Γ_F and 0 < τ ≤ 1. Put t = g_d + ⌈log_p(2/τ)⌉,
k = ⌈log₂(2/τ)⌉ and L = ⌈2N̄_0(g_d)⌉. N̄_0 is N_0 with the public bound
σ̄_p = min(p, ⌈2log₂(p−1)⌉+4) in place of s_p, or the exact count of Theorem H′. j\*_h is public:
it is 1 in the Weil range, and otherwise p ≤ ((κ−1)(κ−2)+3)², so the chain is computed in
poly(κ) time. The node proceeds as follows.
1. Span W by the first t labels.
2. Write later labels in the echelon basis, and abort on a label outside W.
3. Run 𝒜_0 on up to k disjoint blocks of L labels, until one run ends inside its block.
4. Extract roots (F4), check (F5) and convert (F6).

Then the node never returns a wrong witness, and it aborts with probability ≤ τ + 3·2^{−B}.
The 3·2^{−B} covers the capped root extractions, field draws and (in H′) splits, as for an FCS
node. Its arity is M_d = t + kL = Θ_p(g_d^{1+j\*_h} log(1/τ)), with
M_d = O((2log₂p+5)^{j\*_h} g_d^{1+j\*_h} log(1/τ)) uniformly. Its time is
poly(M_d, κ, log p) · (1 + p²·[√p < 2(κ−1)(κ−2)+4]). The bracket covers table building, which
is needed whenever the random split of Theorem H′ is not proven (this includes every prime
with j\*_h ≥ 2), and then p² = poly(κ).

*Proof.* As in Cor. P.4 / rem:fc-zero-sum-arity(b):
- **Span.** Pr[W ≠ K_d^⊥] ≤ τ/2 by `lem:s3-moment`(d).
- **Coordinates.** Outside that event the coordinates are i.i.d. uniform in F_p^a, so
  Theorem H applies.
- **Overruns.** N_0 is increasing in the dimension, so by Markov's inequality each run overruns
  with probability ≤ 1/2. The blocks are disjoint, so all overrun with probability ≤ τ/2.
- **Conversion.** The witness y ∈ D^M is converted by (F4): σ_i^κ = y_i, s_i = σ_i^α. Then
  s_i^d = y_i by `eq:s3-bezout`, and (F5) checks this exactly. ∎

**[computed]** `run_node.py` → `node.json`.
- **Grid.** 52 rows: (h, p, d) ∈ {(3,7,2), (3,13,4), (3,13,8), (3,19,6), (3,31,10), (4,13,3),
  (4,13,9), (4,17,4)}, g from 2 to 12, τ ∈ {0.05, 0.5}, a uniform in [0, g], and 7046 trials
  in total.
- **Outputs.** No wrong output. Every witness was converted at the actual grade d and checked
  with Σ s_i^d λ_i = 0 in F_p^g.
- **Aborts.** 9 aborts, all span failures; the maximum abort rate was 1/150. No run overran.
- **Arity.** At τ = 0.05, the arity slopes (log M vs log g, last step) are 1.90 at p = 7 and 13
  (j\*_h = 1, degree 2), and 3.05–3.06 at (3,19), (3,31) and (4,17) (j\*_h = 2, degree 3).

**[computed]** `run_solver.py` → `solver.json`.
- **Rows.** 42 rows over h = 3 (p = 7, 13, 19, 31) and h = 4 (p = 5, 13, 17), with n up to 39
  (j\*_h = 1) or 13 (j\*_h = 2).
- **s_p.** Exact for p ≤ 17 (1127/243, 4154499115/725594112, 434896500819017/2^46), and Monte
  Carlo from 2·10⁵ draws at 19 and 31 (6.364, 7.197).
- **Reads.** Every output was checked exactly. The mean reads match N_0 with max |z| = 3.04,
  at (3, 19, n = 11) with only 13 runs. A rerun with 120 runs and a fresh seed gave z = −0.03
  (`recheck.json`).
- **Targets.** Inhomogeneous targets at every level j < j\*_h: 140/140 exact.
- **Degree.** The exact slopes of log N_0 from n to 2n at n = 128 are 1.994 (j\*_h = 1) and
  3.000 (j\*_h = 2). At h = 4, p = 5 (κ = 1) the reads are exactly n+1.

**Negative controls** (`misc.json`).
- **Biased columns.** With entries uniform on {0,1}, the mean reads miss N_0 by z = 47.9 and
  45.2. Uniformity is needed for the expectation, and the outputs are still exact.
- **Hyperplane bank.** With coordinate n equal to coordinate 1, every top-level β vanishes. All
  120/120 capped runs exhausted, with 0 wrong outputs. The node is not total.

### H.7 Consequence for thm:free-coordinate(iii) at fixed c

**Corollary H.7 [proved, conditional exactly as (iii) is; AI-checked, pending human review].**
In (R1)–(R3), use the Cor. H.6 node at every d ∈ Γ_F, the rem:fc-zero-sum-arity(b) node at
Γ_0 and the linear node at Γ_1, all with τ_d = ε/(9(c−1)Sn_d). Then the conclusion of (iii)
holds: the recursion returns 𝔥 with probability ≥ 1 − ε from c S ∏_d M_d queries. At fixed c
the classical time is poly(m, log p, log 1/ε) for every prime p > c.

*Proof (changes to the proof of (iii)).*
- **lem:fc-forest(a).** The new node reads only its own bank, checks exactly and converts by
  prop:descent pointwise in the record. It is therefore a further case like the zero-sum node,
  with output ρ_{H_{d−1}} in product on non-aborting records.
- **lem:fc-forest(b).** Each such node contributes ≤ τ_d + 3·2^{−B} in place of
  β_d + 3·2^{−B}. Σ_d S n_d τ_d ≤ ε/9 as before. N in (R2) counts the Γ_F nodes as before; the
  Γ_0 doubling node has no capped step besides overrun, which is inside τ_d.
- **Rest of the proof.** Unchanged.
- **Time.** The time bound is Cor. H.6 at each node.
- **Size of τ_d.** log(1/τ_d) = O_c(log(m/ε) + log log p), because n_d = ∏_{d'<d} M_{d'}. ∎

**Exponent [computed, `run_exponent.py` → `exponent.json`].** Write
E_new(c) = max_{p>c} [1 + Σ_{d=2}^c (1 + j_d)]. Here j_d = 0 at Γ_1, j_d = ⌈log₂(p−1)⌉ ≤ ⌈log₂ c⌉
at Γ_0, and
j_d = j\*_{h_d}(p) at Γ_F. This counts the exponent of m with g_d ≤ m and S ~ m. It ignores the
(log p)^{Σ j_d} and log(1/τ) factors. For p beyond max_κ ((κ−1)(κ−2)+3)², every Γ_F grade has
j_d = 1, Γ_0 is empty (it needs p ≤ c+1), and the exponent is ≤ 2c−1. Below that range every prime was scanned:

| c | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E_new(c) | 3 | 6 | 8 | 10 | 13 | 14 | 16 | **19** (p = 19) | 21 | 22 | 25 |
| Schedule 1 at κ_d (reference) | 5 | 11 | 23 | 38 | 56 | 77 | 95 | 145 | 185 | 186 | 247 |

The paper's combined rule has 143 at c = 9 (rem:combined-schedule). Its exponents 145 (Schedule
1 at κ_d, reference row) and 143 (combined rule) measure worst-case rules that need no label
law. E_new measures a Schedule 3 variant: it needs the i.i.d. supply, aborts, and pays
polylogarithmic factors. **This is a comparison of different guarantees, not a speedup claim.**

## B. Barriers and the lattice problem

### B0. Existence threshold [proved]; the paper's "arity a + O(1)" question

Let the labels be uniform on a subspace of dimension a, written λ = Ex with X uniform
a × M. For y ≠ 0, Pr[Xy = 0] = p^{−a}. Hence
Pr[∃ witness] ≤ ((h+1)^M − 1)/p^a < (h+1)^{M−a} q^a, where q = (h+1)/p. Every algorithm, in any
time, outputs only checked witnesses, so its success probability is at most this.
- For success ≥ 1/2: M ≥ a log p/log(h+1) − log 2/log(h+1).
- At M = a + k: success ≤ (h+1)^k q^a. This is exponentially small in a unless
  (h+1)^k ≥ q^{−a}, which needs k ≥ a ln(1/q)/ln(h+1) (with ln(1/q) = ln κ − Θ(1/h)).
- Scope: arity here is the total number of labels read from an i.i.d. uniform supply. The
  conclusion below is meaningful when h < κ^{o(a)}; when log h ≳ a log κ, arity a + O(1) is
  already at the threshold.

[computed] `misc.json` checked this by exhaustive search over D^M on 1400 banks, at
(h, p, a) ∈ {(3,7,2), (3,7,3), (4,13,2), (3,13,2)} with M from a to a+5. Every observed
frequency was below the bound. For example, at (3,7,3,M = 3): 0.065 against 0.18.

**Imprecision in main.tex** (paragraph after prop:rc-lower: "Whether some method finds a
witness in time κ^{a−Ω(a)} at arity a + O(1) is open"). For uniform labels and h < κ^{o(a)},
the answer is no: at arity a + O(1) a witness exists with probability ≤ (h+1)^{O(1)} q^a. The FCS
arity (lem:fc-choice) is n_0 + g_d + O(log 1/τ) with n_0 ≈ g_d log(1/q)/log h. That is already
the existence threshold g_d(1 + log(1/q)/log(h+1)), up to log h versus log(h+1). The question
should be posed at that threshold arity. Replacement text: Part F, item F2.

### B5_h. Depth of switch hierarchies [proved]

This is Lemma J(iii). The model is any hierarchy whose level-(j+1) relations are differences
of level-j weightings, possibly rescaled, with any number of options per switch: all
pairwise differences of options are relations, so they lie in E_j − E_j. Its base must accept
arbitrary kernel vectors (E_J = F_p).
- **Depth.** The depth is ≥ j\*_h(p), and j\*_h(p) is the exact minimum (attained by
  Theorem H).
- **Fixed h.** j\*_h(p) ≥ log₂((p^{1/φ(h)} − 1)/(2c_h)), so the depth j\*_h, and the degree
  1 + j\*_h of Theorem H, are unbounded as p → ∞. For h = 3 this reads
  j\*_3 ≥ log₂ p/2 − 2 − o(1) [proved] with the crude count (2c_h2^j+1)^φ (the exact ℓ₁-ball
  count gives −1.5), and the computed values are log₂ p/2 ± 1.
- **Per level.** Each level of Theorem H multiplies the reads by Θ(s_p n). An analogue of B2 at
  levels j ≥ 1 is not proved. **[conjecture]** Every switch hierarchy of depth J reads
  n^{1+J−o(1)} columns.

### B2_h. Level-0 switch recursion [proved within the model]

This is the FSR model of the arity report (B2), with switches being pairs of D_0-weightings on
fresh disjoint blocks, and the same reading restriction. Then

  M ln(|D_1| M) ≥ ⌈log₂ p⌉·[ln p·L(L−1)/2 − L ln(4n/δ)],  L = n − ⌊log₂(4/δ)/μ_p⌋.

*Proof.* Steps (a), (b) and (d) of B2 are unchanged.
- **(a).** The residual a_d is uniform. The weights chosen below d include the base column with
  weight 1, and coordinate d of those columns is unread. So
  Pr[a_d ∈ subset sums] ≤ 2^{B'_d}/p.
- **(c).** A useful switch at d is a nonzero relation with entries in D_1 = D_0 − D_0 on the
  first d−1 coordinates. For a fixed support of size s and a fixed nonzero pattern the
  probability is p^{−(d−1)}. There are at most 2(|D_1|M)^s choices with support ≤ s. Put
  s_d = ⌊((d−1)ln p − ln(4n/δ))/ln(|D_1|M)⌋; the union over d is then ≤ δ/2. ∎

So M = Ω_p(n²/log n). At j\*_h = 1, Theorem H reads (s_p/2)n² + O(n), so it is optimal in this
template up to the log factor. |D_1| ≤ min(p, h² + 1) for even h and ≤ min(p, h² + h + 1) for
odd h (since −μ_h ≠ μ_h); it is 13 for h = 3, 4 at the test primes.

### B1_h, B3_h

- **B1_h.** The disjoint merging bound B1 holds with μ_h-weighted unions, with the same proof:
  the fan-in count becomes (h(M+1))^F.
- **B3_h.** Bank-oblivious candidates are prop:rc-lower (T q^a), already in the paper.

### Lattice form [proved] and hardness [conjecture]

- **Exact form.** Identify R/𝔭 = F_p via ψ. A uniform bank is a uniform
  A ∈ (R/𝔭)^{n×M}, and W(h) asks for z ∈ (μ_h ∪ {0})^M ⊂ R^M, z ≠ 0, with Az ∈ 𝔭^n.
- **SIS form.** In power coordinates this is SIS modulo p for the structured n × φM matrix
  Â = [A_i ω^t]_{i,t<φ}, with solutions in a fixed finite set of vectors of ℓ∞ ≤ c_h.
- **Kronecker.** The nonzero z ∈ R with all |σ(z)| ≤ 1 are the roots of unity [cited,
  Kronecker 1857]. In R these are ±μ_h. So for h even, W(h) is exactly Module-SIS over Z[ζ_h]
  modulo 𝔭 with canonical ℓ∞-bound 1. For h odd, W(h) is that problem with solutions
  restricted to μ_h (so it is at least as hard as W(2h)).
- **h = 2.** R = Z and this is A5's ternary SIS.
- **Easy direction [proved].** μ_2 ⊆ μ_h for even h, and 1 ∈ μ_h, so W(h) reduces to ternary
  SIS (h even) or BinSIS (h odd) on the same matrix. Both Theorem P and Theorem H apply.
- **No linear embedding of plain SIS (heuristic remark, not proved).** A D-solution is one vector y ∈ F_p^M. Its "Galois
  conjugate" (ω ↦ ω^u applied to the digits) is not an F_p-linear function of y. So no
  F_p-linear embedding of a plain SIS instance obviously makes W(h)-solutions short in Z^M.
  This is an obstruction to the naive reduction only, not a theorem.
- **[conjecture]** For fixed h ≥ 3 and p ≥ poly(n), average-case W(h) at poly(n) columns has no
  polynomial-time algorithm. Worst-case-to-average-case reductions for Module-SIS that I
  recall [cited, Langlois–Stehlé 2015; NEEDS HUMAN VERIFICATION] use the modulus qR, not a
  degree-one prime ideal. I know no such theorem for 𝔭, and did not search.
- **Consistency.** The conjecture is consistent with B5_h: the only polynomial algorithms known
  here have degree growing like log₂p/φ(h).

### The owner's h = 3 hint

μ_3 + μ_3 ⊂ −μ_3 ∪ 2μ_3, and 1 + ω + ω² = 0. Adding two D_0-weightings on the same columns
stays in D_0 (up to sign) only if they have the same support with different entries everywhere,
and such pairs of solutions are rare on uniform banks. The relation 1 + ω + ω² = 0 needs three
equal columns. Theorem H uses disjoint supports and splits relations instead. For h = 3, D_1 is
the 13 Eisenstein integers of norm ≤ 3, read mod 𝔭 (`depth.json` sizes [4, 13, …]).

## C. Comparison at the test grades and for fixed κ

Degree of g in the arity:

| h | p | κ | **ours 1+j\*_h** | Theorem P via {0,1} | Schedule 1, κ⌈log₂(κ+1)⌉ | Schedule 2 (p ≥ 16κ^{2κ+2}) | decoupled (p ∉ E_2(κ)) | FCS |
|---|---|---|---|---|---|---|---|---|
| 3 | 7 | 2 | 2 | 4 | 4 | no | 2 (E_2(2) = ∅) | ≈1, κ^a trials |
| 3 | 13 | 4 | 2 | 5 | 12 | no | none (13 ∈ E_2(4)) | ≈1 |
| 3 | 19 | 6 | 3 | 6 | 18 | no | not checked | ≈1 |
| 3 | 31 | 10 | 3 | 6 | 40 | no | not checked | ≈1 |
| 4 | 13 | 3 | 2 | 5 | 6 | no | 2 (E_2(3) = ∅) | ≈1 |
| 4 | 17 | 4 | 3 | 5 | 12 | no | none (17 ∈ E_2(4)) | ≈1 |

Notes.
- Schedule 1, Schedule 2 and decoupled are worst-case (decoupled is conditional). Ours is
  average-case with abort τ and a log(1/τ) factor.
- For fixed κ, our degree is ≤ 1 + ⌈log₂ κ⌉ at every p, and 2 at every p > ((κ−1)(κ−2)+3)².
  That range starts polynomially in κ; thm:power-sde(ii) needs 16κ^{2κ+2}.
- For fixed h and growing p (so κ, c → ∞), our degree is log₂p/φ(h) + O_h(1).
- Schedule 3 can be polynomial only if c = O(log m) (11-04 report, Z3). Then κ_d = O(log m),
  and the node is polynomial when log g_d · log κ_d = O(log m). That is the window of
  rem:fc-zero-sum-arity, now at every grade.

## D. Strongest counterexamples and limits

- **Not total.** On the hyperplane bank every top-level β vanishes; the node aborts (H.6
  controls).
- **Not uniform in p for fixed h** (B5_h). No switch hierarchy has bounded depth; whether some
  deep hierarchy still has bounded degree is open (conjecturally no).
- **Arity.** The arity is far above the existence threshold a log_{h+1} p. The node trades
  arity for time, the reverse of the FCS sampler.
- **No hardness.** The module-SIS hardness is a conjecture.
- **Smallest failing case of a claim here.** None found. All bounds held on every computed
  prime.

## E. Gates and next step

- **Gates.** All Rees gates stay false. Corollary H.7 is fixed-c. The query count is still
  ≥ 2^{c−1}, so "polynomial-time Schedule 3" in the gate's sense (c growing) is untouched.
- **Owner decision (optional, nothing pending on it).** Should the Cor. H.6 node become a public
  option at Γ_F grades in (R1)/(iii) (Cor. H.7)? That would change theorem text and possibly
  the polynomial-time statement of (iii) at fixed c, but no table.
- **Next hard question.** Does every switch hierarchy of depth J read n^{1+J−o(1)} columns (B2
  at higher levels)? Or does some non-switch structure (e.g. the R-module structure, with
  lattice reduction in dimension φ(h) per step) give degree o(log p) for fixed h?
- **Next command:**
  `cd research/audits/reviews/2026-11-05-rees-s3-witness-h3 && nice -n 10 /opt/anaconda3/bin/python run_solver.py solver.json`
  - Expected: `solver.json` with every `all_checked_ok` true and |z| ≤ 3.1.
  - Acceptance: a human check of Lemma J(ii) (the Jacobi-sum count) and of the Cor. H.7
    changes to lem:fc-forest.
- **Mechanical follow-ups (for the integrator to move into MECHANICAL_FOLLOW_UP_PLAN.md; not
  done here because this pass may not edit the handoff):**
  - (M1) Rerun `run_depth.py` and `run_exponent.py` and diff the JSON.
  - (M2) Check E_2(6) for p = 19, 31 to fill the two "not checked" cells.

## F. Proposed text (AI-checked, pending human review)

**F1.** New remark in `appendix-free-coordinate.tex`, directly after `rem:fc-zero-sum-arity`.
It is also saved as `2026-11-05-rees-s3-witness-h3/proposed_remark.tex`.

```latex
\begin{remark}[A weight-doubling witness sampler at the free-coordinate grades; AI-checked, pending human review]
\label{rem:fc-witness-h3}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-s3-witness-h3.md}, with code in its folder), checked by a second, adversarial AI pass recorded in the same report; no human has checked it, nothing else in the paper uses it, and (R1), Theorem~\ref{thm:free-coordinate} and the tables are unchanged. Let $d \in \Gamma_{\mathrm F}$, write $\kappa = \kappa_d$ and $h = (p-1)/\kappa \ge 2$, and let the labels be independent and uniform on $K_d^\perp$, as in Lemma~\ref{lem:fc-forest}(a). The witness entries lie in $D = P_\kappa\cup\{0\}$, the $h$-th roots of unity together with $0$.

\textup{(a)} \emph{Depth.} Put $D_0 = D$ and $D_{j+1} = D_j - D_j$, and let $j^*_h$ be the least $J$ with $D_J = \Fp$; at $h = 1$ this is the $j^*$ of Remark~\ref{rem:fc-zero-sum-arity}. Then $|D_j| \ge \min(p, 2^jh+1)$ by the Cauchy--Davenport theorem, so $j^*_h \le \lceil\log_2\kappa\rceil$. If $\sqrt p > (\kappa-1)(\kappa-2)+3$, then $D_0 - D_0 = \Fp$ and $j^*_h = 1$: for $y \ne 0$, Jacobi sums show that at least $(p - (\kappa-1)(\kappa-2)\sqrt p - 3\kappa + 1)/\kappa^2$ pairs $(u,v) \in P_\kappa^2$ have $u - v = y$. For fixed $h$, let $\varphi(h)$ be Euler's function and $c_h$ the largest $\ell_1$-norm of a power of $\zeta_h$ in the power basis of $\mathbb{Z}[\zeta_h]$. Then $\log_2((p^{1/\varphi(h)}-1)/(2c_h)) \le j^*_h \le \lceil\log_2(c_h\varphi(h)^2p^{1/\varphi(h)}/2)\rceil + 1$: every element of $D_j$ is the image of a signed sum of at most $2^j$ roots of unity in $\mathbb{Z}[\zeta_h]$, and a Minkowski vector of the prime $(p,\zeta_h-\omega)$ gives short representatives of every residue. So $j^*_h = \log_2p/\varphi(h) + O_h(1)$. Computed values: $j^*_3 = 1,1,2,2$ at $p = 7,13,19,31$, $j^*_4 = 1,2$ at $p = 13,17$, and $j^*_3 - \tfrac12\log_2p \in [-0.85, 0.60]$ for the $3014$ primes $p \equiv 1 \pmod 3$ below $6\cdot 10^4$.

\textup{(b)} \emph{Sampler and node (proved; AI-checked, pending human review).} The level-$j$ solvers of Remark~\ref{rem:fc-zero-sum-arity}(a) work with $D_j$ in place of $D^{(j)}$, with $j^*_h$ in place of $j^*$, and with a fixed table writing each $\alpha \in D_{j+1}$ as $x - x'$ with $x,x' \in D_j$; the proof is unchanged, since it uses only $0,1 \in D_j$, the splitting, and the uniformity of each $\beta_k$. The level-$0$ solver returns a witness $y \in D^R$ with $\mathbb{E}R = N_0(n)$, a polynomial of exact degree $1 + j^*_h$ in $n$, in time $O(R(n^2+p) + j^*_hp^2)$. When $j^*_h = 1$ the $k$-th switch of each coordinate may be rescaled to $\beta_k = 2^k$, so $\lceil\log_2 p\rceil$ switches and the binary digits of the residue replace the covering loop, and entries of $\Fp$ are split into $x - x'$ with $x, x' \in P_\kappa\cup\{0\}$ by random search, which succeeds with probability at least $1/(2\kappa)$ per trial once $\sqrt p \ge 2(\kappa-1)(\kappa-2)+4$; the expected number of columns is then exactly $1 + \lceil\log_2p\rceil\frac{p}{p-1}\frac{n(n+1)}{2}$ and the time is $\poly(n,\kappa,\log p)$. The node at $d$ is that of Remark~\ref{rem:fc-zero-sum-arity}(b), with this solver, followed by (F4)--(F6). It never returns a wrong witness, aborts with probability at most $\tau$ plus the three capped steps of an FCS node, and has arity $M_d = O((2\log_2p+5)^{j^*_h}g_d^{\,1+j^*_h}\log(1/\tau))$, of degree $1 + j^*_h \le 1 + \lceil\log_2\kappa_d\rceil$ in $g_d$, and degree $2$ for $\sqrt p > (\kappa_d-1)(\kappa_d-2)+3$; its time is polynomial in $M_d$, $\kappa_d$ and $\log p$ (so polynomial in $g_d$ at fixed $\kappa_d$), since the tables are needed only when $\sqrt p < 2(\kappa_d-1)(\kappa_d-2)+4$, and then $p^2$ is polynomial in $\kappa_d$. In finite computations (AI-run, pending human review) at $h = 3$ ($p = 7,13,19,31$) and $h = 4$ ($p = 13,17$) every output was checked exactly, mean column counts matched $N_0$, and the node aborted in at most $1/150$ of trials; the rescaled variant ran at $p = 2^{61}-1$ with $\kappa = 6$. For comparison at fixed $\kappa$: Schedule~1 has degree $\kappa\lceil\log_2(\kappa+1)\rceil$ ($12$ against $2$ at $p = 13$, $\kappa = 4$, a prime of $E_2(4)$), and Theorem~\ref{thm:power-sde}(ii) has degree $2$ but needs $p \ge 16\kappa^{2\kappa+2}$; both are worst-case and use no label law.

\textup{(c)} \emph{Consequence at fixed class.} Under the hypotheses of Theorem~\ref{thm:free-coordinate}(iii), with this node at every grade of $\Gamma_{\mathrm F}$, the node of Remark~\ref{rem:fc-zero-sum-arity}(b) at $\Gamma_0$ and $\tau_d$ as in (R1), the proof of Theorem~\ref{thm:free-coordinate}(iii) goes through: each such node is a further case of Lemma~\ref{lem:fc-forest}(a), like the zero-sum node, and contributes at most $\tau_d + 3\cdot2^{-B}$ to Lemma~\ref{lem:fc-forest}(b). At fixed $c$ the classical time is then polynomial in $m$, $\log p$ and $\log(1/\eps)$ for every prime $p > c$, and, counting $g_d \le m$ and ignoring logarithmic factors, the exponent of $m$ in the query count, maximized over $p > c$, is at most $19$ at $c = 9$ (computed), against $143$ for the combined rule of Remark~\ref{rem:combined-schedule}, which needs no label law. This compares different guarantees; it is not adopted here.

\textup{(d)} \emph{Limits (proved; AI-checked, pending human review).} At arity $M$ (labels read from the independent uniform supply) a witness exists with probability at most $((h+1)^M-1)/p^{a_d} < (h+1)^{M-a_d}q^{a_d}$, so no method of any running time succeeds with probability $1/2$ below about $a_d\log p/\log(h+1)$ labels; the arity of Lemma~\ref{lem:fc-choice} is of this order. Every switch hierarchy whose level-$(j+1)$ relations are rescaled differences of level-$j$ weightings and whose base is linear algebra has depth at least $j^*_h$, so for fixed $h \ge 3$ its depth, and the degree $1 + j^*_h$ of the sampler in (b), grow like $\log_2p/\varphi(h)$; whether a deep hierarchy can still have bounded degree is not settled here. On a uniform bank the witness problem is Module-SIS over $\mathbb{Z}[\zeta_h]$ modulo the degree-one prime $(p,\zeta_h-\omega)$, $\omega \in \Fp$ of order $h$, with solutions in $\mu_h\cup\{0\}$; for even $h$ these are, by Kronecker's theorem, exactly the vectors of canonical $\ell_\infty$-norm at most $1$, and at $h = 2$ this is the ternary SIS of Remark~\ref{rem:fc-zero-sum-sis}. No worst-case hardness result for this modulus is used or claimed. Whether some method has degree bounded uniformly in $p$ for fixed $h \ge 3$ remains open.
% NEEDS HUMAN VERIFICATION: Jacobi-sum absolute values (Ireland--Rosen, ch. 8), Kronecker's theorem on algebraic integers with all conjugates of modulus at most 1, and the absence of a worst-case reduction for Module-SIS modulo a degree-one prime ideal (Langlois--Stehle 2015 treat the modulus qR), all from memory; no bib entries are added.
\end{remark}
```

**F2.** `main.tex`, paragraph after `prop:rc-lower`. Current: "Whether some method finds a
witness in time $\kappa^{a-\Omega(a)}$ at arity $a + O(1)$ is open." Replacement:

```latex
For independent uniform labels, at arity $a + k$ a witness exists with probability at most $(h+1)^kq^{a}$, by the first moment, so no method succeeds with constant probability at arity $a + O(1)$ unless $h \ge \kappa^{\Omega(a)}$; the arity of Lemma~\ref{lem:fc-choice} is already within a factor $\log(h+1)/\log h$ of this threshold in its $\log(1/q)$ term. Whether some method finds a witness in time $\kappa^{a-\Omega(a)}$ at arity $O(a\log p/\log(h+1))$ is open; Remark~\ref{rem:fc-witness-h3} gives a method with time polynomial in its arity, which has degree $1 + j^*_h \le 1 + \lceil\log_2\kappa\rceil$ in $g_d$.
```

No bib change.

## G. Independent adversarial check

A fresh general-purpose subagent saw only this report, the code folder and `research/STATE.md`.
It re-derived the proofs and recomputed independently with its own FFT/bitset depth code on
about 1800 primes. It also checked the Jacobi-sum count on 5741 pairs (κ ≤ 12, p ≤ 2·10⁵),
c_h for nine h, E_new(4, 6, 9), and s_7 and s_13. It reran the scaled variant at 2^31−1 and two
solver rows.

**Verdict: no error in Theorems H and H′, Lemma 0, Lemma J or Cor. H.6–H.7, and the exponent
table is confirmed.** Its findings, and how each was handled:

1. **Error (overclaim).** "Degree grows like log₂p/φ(h) for every switch hierarchy"
   (summary 3, §D, remark (d)) went beyond what was proved, which is the depth.
   *Fixed:* only depth is claimed in general; the degree is claimed for Theorem H's template;
   the general degree statement is [conjecture].
2. **Error (minor).** |D_1| ≤ h²+1 is false for odd h. *Fixed:* h²+h+1 for odd h.
3. **Imprecision.** "≤ 10κ²" is contradicted by κ = 15, p = 3181. *Fixed:* ≤ 15κ².
4. **Imprecision.** B0 used ln κ for ln(1/q). *Fixed.*
5. **Imprecision.** The scope of the negative answer to the paper's question was not stated.
   *Fixed:* the summary, B0 and F2 now say uniform labels and h < κ^{o(a)}.
6. **Imprecision.** "Polynomial-time" in the remark title and F2. *Fixed:* "time polynomial in
   its arity; polynomial at fixed κ".
7. **Imprecision.** The Cor. H.6 time missed table building in the gap
   A+3 < √p < 2A+4. *Fixed:* the bracket is now [√p < 2A+4].
8. **Imprecision.** Remark (c) lacked the conditional qualifier. *Fixed.*
9. **Gap.** "No linear embedding of plain SIS" was labelled proved. *Fixed:* relabelled as a
   heuristic remark.
10. **Nits.** All fixed: the probability chain in J(ii); 3(κ−2)²+4; the −2 versus −1.5
    constant; Γ_0 depth ⌈log₂(p−1)⌉; the log log p term in τ_d; and the running-sums remark on
    `wh_lib.solve`'s time.

The referee could not check the macros \file, \Fp, \poly and \eps against the paper; this
pass had read them from `main.tex` before. No claim was withdrawn.
