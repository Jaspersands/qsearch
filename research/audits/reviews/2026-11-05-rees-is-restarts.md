# Rees Schedule 1: collapsing the ν+1 restarts of the Ivanyos–Santha classifier

5 November 2026 (session dated 4 November). AI-only pass, one session. No human review.
Labels: **[proved]** (written argument here), **[source]** (cited, not re-proved),
**[exact]** (complete finite computation), **[grid]** (numerical supremum on a finite grid).

Target: `docs/papers/rees-hsp/main.tex`, Remark `rem:is-runtime` (with `thm:is-import`,
`rem:is-import`). The remark bounds the Schedule 1 solver by at most ν+1 whole runs. Here ν is
the number of prime factors, with multiplicity, of n_π, the largest divisor of p−1 whose prime
factors all divide κ. This factor ν+1 ≤ b is why the bound has b³ and not b².

Inputs: `2026-11-04-rees-is-runtime.md` (operation count (F) and the per-run estimates),
`2026-11-04-rees-is-runtime-tm.md` (TM layout), IS arXiv:1503.09016v2 §3.1–3.3 (local copy
`research/audits/reviews/2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`), and
`theorems/rees_is_sde_solver.py`.

Changes made: `theorems/rees_is_sde_solver.py` got a new keyword `collapse=False`, two helpers
and a defaulted field `SDEWitness.collapsed`. `tests/test_rees_is_sde_solver.py` got 22 new
test cases. No `.tex` was edited, nothing was committed, and no network was used.
`research/reductions/rees_hsp_reduction.json` was not touched.

## 0. Answer

1. **Prime-power κ: the restarts collapse [proved].** Lemma 1 is a deterministic variant that
   uses the same columns and arity. Let κ = ℓ^e. The variant makes **at most e = Ω(κ) ≤ log₂κ
   runs**, independently of p. For prime κ it makes **one run and never restarts**.
   - The idea is to keep the first level-1 kernel relation as an *anchor*. This relation does not
     depend on the classifier.
   - Each restart trigger enlarges ⟨η⟩ by a factor of at least ℓ. After e enlargements, every
     coefficient of the anchor is a κ-th power with a computable root.
   - At that point the anchor itself is a witness, supported on the first a+1 columns.
2. **New runtime [proved, with the TM layout of the -tm note].** For prime-power κ_d, the
   variant runs within
   **T^{IS,col}_d = C₁ d³ (1+log₂ d) M_d b² (g_d² + b²) + C₂ d⁴ b⁵** multitape-TM steps.
   - For fixed d this is O(M_d b²(g_d²+b²) + b⁵), against O(M_d b³(g_d²+b²)) before. So one
     factor of b is gone whenever M_d ≥ b, and the new bound is never larger than the old one,
     up to constants.
   - The factor ν+1 became the constant Ω(κ_d) ≤ log₂ d. The zero sum, which does not depend on
     the columns, became an additive b⁵ term.
   - This covers every d ≤ 5, hence every grade of class c ≤ 5, and every prime-power d.
3. **Precomputing the final subgroup without the columns is blocked [proved].** The idea was
   to find a generator of the relevant Sylow parts in advance.
   - There are columns that force the final subgroup to be all of H_π (Proposition 2). A
     column-independent precomputation would therefore construct an ℓ-th-power nonresidue for
     every ℓ | κ, and a quadratic nonresidue for even κ.
   - No deterministic unconditional polynomial-time method for that is known.
   - Under ERH, a search over small integers does it, and gives one run for every κ
     (Remark 4, conditional).
4. **κ with two or more distinct primes: no improvement [proved limitation of this argument].**
   - When only the ℓ-part of ⟨η⟩ grows and the anchor has a nontrivial ℓ′-part, the anchor
     test fails at every trigger (Proposition 3).
   - So the argument gives nothing better than the old bound of ν+1 runs (ν runs, in fact). It is
     not known whether IS inputs realise such trajectories.
   - The first affected grade is d = 6, when 6 | p−1.
5. **Implementation and tests [exact].** `is_sde_solve(..., collapse=True)` passes:
   - the 152 existing tests (default behaviour unchanged);
   - 22 new tests;
   - the scripts in `2026-11-05-rees-is-restarts/`.
   On 528 random runs, the default restarted 608 times and the variant 0 times (§6).

## 1. Setting and notation

Notation follows the -runtime note.
- κ = gcd(d, p−1) ≥ 2 and a = rank (the `reduced` columns lie in F_p^a). b = ⌈log₂p⌉.
- π is the set of primes of κ. F_p^* = H_π × H_π′ with |H_π| = n_π and ν = Ω(n_π).
- Every α ∈ F_p^* splits as α = γγ′, with γ ∈ H_π and γ′ ∈ H_π′. γ′ has a unique κ-th root in
  H_π′, computed by one power (IS §3.1).
- The classifier holds η ∈ H_π. It writes α = ζ_r β^κ with ζ_r = η^r and β = η^f·(γ′)^{1/κ},
  using a Pohlig–Hellman logarithm e = log_η γ = fκ + r. If γ ∉ ⟨η⟩, it raises a *trigger*.
- At a trigger, IS replace η by a generator of ⟨η, γ⟩ (`PiParts.join`) and rerun everything from
  scratch (a *restart*).
- **Why the default needs restarts [proved].** Let ⟨η⟩ ⊊ H′ be cyclic π-groups. The index
  [H′ : ⟨η⟩] is divisible by some ℓ ∈ π, so η ∈ H′^ℓ.
  - So the list (η^r)_{r<κ} is no longer a complete system of representatives of H′/H′^κ.
  - Every earlier classification is still valid, but it uses a list that later classifications
    cannot use.
  - All nodes of IS Lemma 12 and Theorem 11 must use one common list, because the sign identity
    (13)–(15) cancels ζ_s across different positions.

**Anchor.** Let λ_0, …, λ_a be the first a+1 (reduced) columns. Let α = (α_0, …, α_a) ≠ 0 be
the kernel vector that `_kernel_vector` returns for them (the same `spread` as the run).
- α is the kernel of the first level-1 node of the first Theorem 11 call. It is computed from
  the columns alone, before any classification, so it does not depend on η.
- Let K = {k : α_k ≠ 0} ≠ ∅, α_k = γ_kγ′_k, H_1 = ⟨γ_k : k ∈ K⟩ ≤ H_π, and h_1 = |H_1|.

**The variant `collapse=True`.**
- (V0) Compute α. Set η := η_1, a generator of H_1 (|K| − 1 joins).
- (V1) **Anchor test** T(η):
  - Let h = |⟨η⟩| and g = gcd(κ, h). Compute e_k = log_η γ_k for k ∈ K. This always succeeds,
    because H_1 ≤ ⟨η⟩.
  - If e_k ≡ e_{k₀} (mod g) for all k, with k₀ = min K, output for each k ∈ K
    u_k = η^{x_k}·(γ′_k)^{1/κ}, where x_k = ((e_k − e_{k₀})/g)·(κ/g)^{−1} mod h/g
    (x_k = 0 if h = g), and stop.
  - Otherwise return "fail".
- (V2) Run IS Steps 1–4 with the classifier started at η (the zero sum, Step 1, is computed
  once, as before).
- (V3) At a trigger with element γ, set η := join(η, γ) and apply T(η). If T succeeds, stop
  with its output. Otherwise restart (V2) with the new η.
- (V4) Output s_k = u_k^t on k ∈ K (or the IS output), and 0 elsewhere. Here t is the Bezout
  exponent of `rem:is-import`(b).

## 2. Lemma 1 (restart collapse) [proved]

**Lemma 1.** Let p be an odd prime, κ | p−1 with κ ≥ 2, and a ≥ 1. Let λ_1, …, λ_M ∈ F_p^a be
any columns with M ≥ N = G(κ,a)^L, the arity of the default run. Then:

- **(i) Correctness and determinism.** The variant is a deterministic algorithm, with no
  randomness, nonresidue or field enumeration. It always halts with s ≠ 0 and
  Σ_i s_i^d λ_i = 0. When it stops in T, supp(s) ⊆ {0, …, a}.
- **(ii) Prime-power κ.** If κ = ℓ^e, the variant makes at most e runs of (V2). In
  particular, it makes at most one run, and no restart, when κ is prime. It makes no run at all
  if h_1 = 1, or more generally if T(η_1) succeeds.
- **(iii) General κ.** Every restart strictly enlarges ⟨η⟩ ≤ H_π, starting from H_1. So there
  are at most ν − Ω(h_1) restarts, and at most ν runs, since a run occurs only when h_1 > 1.

**Proof of (i).**
- *Termination.* Each restart strictly enlarges ⟨η⟩ inside the finite group H_π. If no test
  succeeds, the last run completes exactly as in IS. Its correctness is IS §3.2–3.3, with the
  reading of `rem:is-import`. IS do not require the initial η to be 1: their argument holds for
  any η whose list (η^r) is used consistently in one run, and any start η makes the list
  "possibly redundant but complete" for ⟨η⟩.
- *Validity of the test output.* Let h = |⟨η⟩| and g = gcd(κ,h). Since gcd(κ/g, h/g) = 1, the
  inverse exists and κx_k ≡ e_k − e_{k₀} (mod h). So η^{κx_k} = γ_k γ_{k₀}^{−1}. Hence

  u_k^κ = η^{κx_k}·γ′_k = γ_k γ_{k₀}^{−1} γ′_k = α_k / γ_{k₀}.

  Then Σ_{k∈K} u_k^κ λ_k = γ_{k₀}^{−1} Σ_k α_k λ_k = 0. Dependencies of the reduced columns are
  those of the original columns, because `_row_reduce` applies an invertible row operation.
  Every u_k is nonzero and K ≠ ∅.
- *Bezout step.* s_k = u_k^t satisfies s_k^d = u_k^κ (`rem:is-import`(b), `ReesSdeGcd`). So s
  is a nonzero solution supported in {0, …, a} ⊆ {1, …, M}, since a+1 ≤ G ≤ N ≤ M.
- *Determinism.* Every step is a fixed deterministic computation:
  - Gauss–Jordan with the first-free-column rule;
  - `split`, `join` and `order`, which are powers and comparisons;
  - Pohlig–Hellman over the primes of κ;
  - the IS run itself.
  So the output is a fixed function of (p, d, columns).

**Proof of (ii).**
- **Base case.** If h_1 = 1, every γ_k = 1. The test succeeds at η_1 = 1, with g = 1 and all
  e_k = 0, before any run.
- **Setup.** Otherwise h_1 = ℓ^{j₁} with j₁ ≥ 1. Let η^{(0)} = η_1, and let η^{(i)} be the
  value after the i-th trigger, with h_i = |⟨η^{(i)}⟩|.
  - A trigger element γ is not in ⟨η^{(i−1)}⟩. So ⟨η^{(i)}⟩ = ⟨η^{(i−1)}, γ⟩ strictly contains
    ⟨η^{(i−1)}⟩.
  - Both are subgroups of the cyclic ℓ-group H_π, so h_i ≥ ℓ·h_{i−1}, and h_e ≥ ℓ^e h_1 = κh_1.
- **The e-th trigger succeeds.** In the cyclic group ⟨η^{(e)}⟩ of order h_e:
  - H_1 is the unique subgroup of order h_1, namely ⟨(η^{(e)})^{h_e/h_1}⟩.
  - κ | h_e/h_1, so H_1 ≤ ⟨(η^{(e)})^κ⟩ = ⟨(η^{(e)})^{g}⟩, with g = gcd(κ, h_e) = κ.
  - Hence every e_k ≡ 0 (mod g), and the test succeeds at the e-th trigger at the latest.
- **Counting runs.** Triggers 1, …, e−1 can cause restarts, so there are at most e−1 restarts
  and at most e runs. A run that completes without a trigger ends the algorithm.
- **Prime κ.** For e = 1, the first trigger always collapses, so the single run (V2) is never
  repeated.

**Proof of (iii).** The chain H_1 ⊊ ⟨η^{(1)}⟩ ⊊ … in the cyclic group H_π of order n_π has
length at most Ω(n_π) − Ω(h_1). □

**Remarks on the lemma.**
- Only the anchor is needed. A *completed node of the current run* would also collapse once its
  list generator becomes a κ-th power, but that happens later than for the anchor, because its
  group contains H_1.
- The test uses the weaker condition "one common coset of ⟨η⟩^κ", not H_1 ≤ ⟨η⟩^κ. It can
  therefore succeed earlier than the proof requires. For example, on random inputs the variant
  collapsed in 172 of 528 runs (§6).
- (V0) uses the same `spread` as the run, so the first node of the run never triggers. Only
  later nodes can trigger. This is not needed for the bound.
- **Order of evaluation.** The anchor is computed before the run and does not depend on the
  node order, so (ii) and (iii) hold for depth-first evaluation (the code) and for the
  level-by-level evaluation of the -tm note alike.
- **G1 of `prop:coherent-receiver`.** The variant returns a different, but fixed, witness from
  the default. G1 only uses that F_d is a fixed deterministic map to nonzero solutions.

## 3. The new runtime statement [proved; constants partly grid]

**Field operations.** Take κ = ℓ^e, so ω = 1. The per-run cost is the run term of (F) in the
-runtime note §3:

  run ≤ I(Λ + Φ + Θ·C_cls) + (L+1)N.

The terms are those of that note: I ≤ (8/7)N, Λ ≤ a²+κ²a+2κ³+2, Φ ≤ a+2.5κ+10.5β_κ+23 and
Θ ≤ 1.65. With ω = 1 and ν ≤ b−1, C_cls ≤ 4b²+14b+2κ²+1.

Put X = a²+b², and use a ≥ 1, b ≥ 2, κ ≥ 2 and β_κ ≤ κ. The term estimates are:

| quantity | bound |
|---|---|
| Λ | ≤ 1.075 κ³X |
| Φ | ≤ 1.35 κ³X |
| Θ·C_cls | ≤ 2.66 κ³X |
| (L+1) | ≤ 0.375 κ³X |
| run | ≤ 6.2 κ³NX |

The extra work of the variant is the anchor kernel (a²(a+1)+a), ≤ a+1 splits and joins, ≤ e+1
anchor tests (each ≤ 2b(ν+1) + (a+1)(C_cls+4b+1)), and ≤ e trigger joins (each
4b+4b(ν+1)+1). This is bounded as follows.
- Use a+1 ≤ N/2, since N ≥ G ≥ 2(a+1)².
- Use join ≤ 6.25b².
- Then the extra work is at most 3.7 eκ³NX.

The Bezout step costs ≤ 2bN ≤ κ³NX/8. Hence, at prime-power κ,

  **F^col ≤ 11 · Ω(κ) · κ³ · N · (a² + b²) + Z(κ, b)  (+ agM + a for the optional row
  reduction),**

with Z = O(κ³b² log κ + κ²b³ log κ) = O(κ³b³) the zero sum (-runtime note §4), which is
unchanged.

- [grid] On p ≤ 2¹²⁷, prime-power κ ≤ 32 and a ≤ 1000, the main term is ≤ 3.49 Ω(κ)κ³NX.
  Z ≤ 54.7 κ³b³, and Z ≤ 11.6 κ³b³ once b ≥ 8 (`collapse_bound.out`).
- [exact] On 84 instrumented runs of the variant (§6), the measured field operations are
  ≤ 0.42 of the explicit bound F^col.
- For comparison, the default bound is 40κ³Nb(a²+b²). The b there is the factor ν+1 ≤ b.

**TM steps.** Arithmetic is c_a b² per counted operation, and there are at most twice as many
additions (-runtime note §3; per run this is unchanged, and the anchor's eliminations add at
most as many additions as multiplications). Head movement comes from the -tm note §4–5:
- per run: ≤ c·κ³Nb²(a²+b²);
- the zero sum: O(κ⁴b³β_κ);
- setup: O((ν+ω+1)b²β_κ + poly(κ, log N)).

The anchor adds one (a × (a+1)) elimination and ≤ (e+1)(a+1) classification-type passes on
≤ a+1 records. These are dominated by one run's level-1 pass. Reading the input costs M_d g_d b.

Using N ≤ M_d, κ ≤ d, Ω(κ) ≤ log₂ d and β_κ ≤ b, one fixed multitape machine computes the
witness of the variant within

  **T^{IS,col}_d = C₁ d³ (1 + log₂ d) M_d b² (g_d² + b²) + C₂ d⁴ b⁵**

steps whenever κ_d is a prime power (C₁, C₂ absolute, not computed). The second term is the
zero sum, κ³b⁵ for arithmetic and κ⁴β_κb³ for movement. It depends only on (p, κ_d).
- For fixed d this is O(M_d b²(g_d²+b²) + b⁵).
- With ν bounded it is O(M_d b²(g_d²+b) + b⁴), unchanged from the remark.
- For κ_d with ≥ 2 distinct primes, the remark's T^IS_d = C₁d³M_db³(g_d²+b²) stands. The
  variant is never worse, because (iii) gives at most ν runs.

**Where this applies.** κ_d | d. So κ_d is a prime power whenever d is (d ∈ {2,3,4,5,7,8,9,11,
13,16,…}), and for every d ≤ 5. Every grade of a class c ≤ 5 is therefore covered, whatever p is.

## 4. Proposition 2: the final subgroup cannot be precomputed from (p, κ) [proved]

**Proposition 2.** Let κ ≥ 2 divide p−1, let a ≥ 1, and let g be a generator of F_p^*. Take
λ_0 = e_1, λ_1 = −g e_1, λ_2, …, λ_a = e_2, …, e_a, followed by any nonzero columns. Then, in
the default algorithm and in the variant, every run that completes uses an η with ⟨η⟩ = H_π.

*Proof.*
- The reduced matrix of the first a+1 columns has pivots in columns 0, 2, …, a and free
  column 1. So `_kernel_vector` returns α = (g, 1, 0, …, 0).
- In the default algorithm, every run first classifies this vector (the first level-1 node).
  A completed run classified α_0 = g, so the π-part of g lies in ⟨η⟩. The π-part of a generator
  generates H_π, so ⟨η⟩ = H_π.
- In the variant, H_1 = ⟨π-part of g⟩ = H_π already, so η_1 generates H_π. □

**Consequence.** Let P be a procedure that, from (p, κ) alone, outputs an η₀ such that runs
started at η₀ never restart, for all columns. By Proposition 2, η₀ generates H_π. Then, for
every ℓ | κ:
- ord η₀ = n_π contains the full ℓ-part of p−1;
- so η₀^{(p−1)/ℓ} ≠ 1, that is, η₀ is an ℓ-th-power nonresidue;
- for even κ, η₀ is a quadratic nonresidue.

Deterministic unconditional polynomial-time construction of such elements is a well-known open
problem; IS §3.1 says the same. So the suggested precomputation ("trial division for n_π, then an
element generating the Sylow parts") fails at its second step. Trial division gives n_π in
O((ν+ω)bβ_κ) bit operations. A generator is what is missing.

The variant precomputes the part of the final subgroup that the columns determine without
classification, namely H_1. Lemma 1 shows that this is enough for prime-power κ.

**Remark 4 (conditional on ERH; not implemented).** [source, from memory; not re-checked in
this pass] Bach (Math. Comp. 55, 1990) shows, under ERH, that every proper subgroup of F_p^* omits
a positive integer below 2(ln p)².
- So for each ℓ | κ, some q < 2(ln p)² is an ℓ-th-power nonresidue. Its ℓ-component generates
  the ℓ-Sylow subgroup.
- Joining these components gives a generator of H_π. This costs O(ωb³) field multiplications
  (testing q^{(p−1)/ℓ} ≠ 1), which is O(ωb⁵) TM steps.
- Started at it, the solver never restarts, whatever κ is. Whether the search succeeded can be
  checked (ord η = n_π), so correctness stays unconditional; only the one-run guarantee depends
  on ERH.

## 5. Proposition 3: why the argument stops at two primes [proved]

**Proposition 3.** Let ℓ ≠ ℓ′ be primes dividing κ. Suppose that the anchor has two
coefficients whose π-parts differ in their ℓ′-components by a non-ℓ′-th power of H_1^{(ℓ′)}.
Suppose also that every trigger enlarges only the ℓ-Sylow part of ⟨η⟩. Then the anchor test
fails at every trigger.

*Proof.*
- The ℓ′-Sylow part of ⟨η⟩ stays equal to H_1^{(ℓ′)} = ⟨η_1⟩^{(ℓ′)}.
- A common coset of ⟨η⟩^κ would put the ratio of the two anchor coefficients' ℓ′-components in
  (H_1^{(ℓ′)})^{ℓ′^{e′}} ⊆ (H_1^{(ℓ′)})^{ℓ′}, which the hypothesis excludes. □

**What this means.**
- In the same situation, IS restarts at each such trigger, because the new element has a
  nontrivial ℓ-class while the old list's ℓ-classes have collapsed. That gives up to ν_ℓ
  restarts.
- A trigger that enlarges the ℓ-part puts η in H′^ℓ. So the old classes are merged by the
  non-injective map s ↦ cs mod κ (c = log_{η′}η, with ℓ | c).
  - The node identities Σ_s ζ_s w_{a(j,s)} = 0 survive this relabelling. One checks it position
    by position, with the κ-th-power rescaling λ_a = ∏_j η′^{κ⌊c a_j/κ⌋}.
  - But the permutation key (0, 1, …, κ−1), the one nonempty key Theorem 11 needs, is mapped to a
    tuple with repeats. So the old run cannot be continued.
- At prime-power κ, the merge eventually kills the anchor's classes entirely, which is
  Lemma 1. With two primes, an ℓ′-class can survive indefinitely.
- [exact] At p = 43777 (p−1 = 2⁸·3²·19, κ = 6), with a 3-part anchor of order 9 and 8
  two-part triggers, the anchor test never succeeds
  (`test_anchor_collapse_on_worst_case_enlargement_chains`).
- Not known: whether IS inputs actually realise such trajectories, and whether a different
  deterministic method avoids them.

## 6. Tests [exact]

Code: `theorems/rees_is_sde_solver.py`, keyword `collapse` (default `False`), helpers
`_anchor_split` and `_anchor_witness`, and field `SDEWitness.collapsed` (default `False`). With
`collapse=False` the code path is the old one: the loop now reads
`while combination is None:`, with combination initialised to None.

- **Existing tests.** `nice -n 10 python -m pytest -q tests/test_rees_is_sde_solver.py`: 152
  passed with the modified solver before the new tests were added.
- **New tests** (in the same file; 22 cases, 6.7 s):
  - `test_collapse_variant_on_random_columns`, over all 19 `CASES`, spread × early_exit. It
    checks:
    - that the witness verifies;
    - that the variant is deterministic;
    - restarts ≤ Ω(κ)−1 at prime-power κ;
    - support ⊆ {0..rank} when collapsed;
    - that the default never reports `collapsed`.
  - `test_collapse_variant_on_adversarial_anchors`:
    - κ = 2 with anchor (−1, 1) at p ∈ {13, …, 65537}, so ⟨η_1⟩ = {±1} and restarts are
      possible;
    - p ≡ 3 (mod 4) with a square anchor: zero runs and zero classifications;
    - κ = 3 with anchor (ω, 1) at p ≡ 1 (mod 9).
    It checks 0 restarts and at least 10 collapses.
  - `test_anchor_collapse_on_worst_case_enlargement_chains`: worst-case chains (index ℓ per
    trigger) at p = 65537 (κ = 2, 4, 8, 16) and p = 1459 (κ = 3, 9). The test succeeds
    **exactly** when |⟨η⟩| ≥ κ|H_1|, which is at trigger e = Ω(κ). This is Lemma 1(ii) made
    exact, including tightness of the stopping point. The κ = 6 stall of §5 is checked here too.
  - `test_collapse_variant_quartic`: κ = 4, p = 17, 65536 random columns; restarts ≤ 1.
- **Scripts** (`research/audits/reviews/2026-11-05-rees-is-restarts/`; run with `nice -n 10`):
  - `collapse_stress.py`, without `-O`:
    - 120 worst-case chains collapse exactly at trigger e;
    - adversarial anchors: 75 of 76 collapsed; the default restarted 167 times in total and the
      variant 0;
    - random runs: 528 (22 instances × 6 seeds × spread × early_exit). The default restarted
      608 times and the variant 0. The variant collapsed 172 times. All witnesses verify.
    - Prints `ALL OK`.
  - `collapse_bound.py`, with `-O`. It reuses the instrumentation of the 2026-11-04 note
    (unchanged):
    - 84 instrumented variant runs, all ≤ F^col (maximum ratio 0.42), restarts ≤ e−1;
    - the grid suprema of §3 (`collapse_bound.out`).
- **Not checked:** κ ≥ 5 runs (too many columns), κ = 4 beyond p = 17 in the new tests, and the
  TM layout, which is taken from the -tm note.

Full-file run: `nice -n 10 python -m pytest -q tests/test_rees_is_sde_solver.py
tests/test_rees_end_to_end_ext.py` gives **216 passed** in 110 s (174 solver tests, of which 152
are old and 22 new, plus 42 end-to-end tests).

## 7. Claim gates

These must stay false: `general_sde_implemented`, `coherent_receiver_implemented`,
`independent_review`, `formal_compiler_checked`, and every Rees novelty, priority or
receiver-execution gate. This pass changes the run-count bound of a classical solver. It
implements no SDE step beyond κ ≤ 4, and it makes no quantum claim.

## 8. Proposed LaTeX for `rem:is-runtime` (not applied; AI-checked, pending human review)

**(A)** Replace the sentence "The algorithm of Theorem~\ref{thm:is-import} makes at most
$\nu+1$ runs, since each restart of \cite[Section~3.1]{IvanyosSantha2015} strictly enlarges a
subgroup of a cyclic group of order dividing $p-1$." with:

```latex
The algorithm of Theorem~\ref{thm:is-import} makes at most $\nu+1$ runs, since each restart of
\cite[Section~3.1]{IvanyosSantha2015} strictly enlarges a subgroup of a cyclic group of order
dividing $p-1$. When $\kappa = \ell^e$ is a prime power, the following deterministic variant
makes at most $e = \Omega(\kappa) \le \log_2\kappa$ runs, and a single run, with no restart,
when $\kappa$ is prime (AI-checked, pending human review). Before the first run it computes the
kernel vector $\alpha$ of the first $a+1$ columns, which is the kernel of the first node of
\cite[Lemma~12]{IvanyosSantha2015} and does not depend on the classifier, and it starts the
classifier at a generator $\eta_1$ of the group $H_1$ generated by the $\pi$-parts of the
nonzero $\alpha_k$. Whenever a restart enlarges $\eta$, it first checks whether these
$\pi$-parts lie in one coset of $\langle\eta\rangle^{\kappa}$. If they do, discrete logarithms in
$\langle\eta\rangle$ write $\alpha_k = \gamma_0 u_k^{\kappa}$ with $u_k \ne 0$, so
$\sum_k u_k^{\kappa}\lambda_k = 0$ is a witness on the first $a+1$ columns, and the variant
stops. Each restart multiplies $|\langle\eta\rangle|$ by at least $\ell$, so after $e$ of them
$|\langle\eta\rangle| \ge \kappa|H_1|$, hence $H_1 \subseteq \langle\eta\rangle^{\kappa}$ and the
check succeeds. A generator of all of $H_\pi$ cannot be fixed in advance instead: for suitable
columns every completed run uses one, and it is an $\ell$-th-power nonresidue for every
$\ell \mid \kappa$, which no known deterministic polynomial-time method constructs
(\file{research/audits/reviews/2026-11-05-rees-is-restarts.md}).
```

**(B)** Replace the sentence "The order in which the nodes are evaluated affects neither
correctness nor the bound $\nu+1$ on the number of runs." with:

```latex
The order in which the nodes are evaluated affects neither correctness nor the bounds $\nu+1$
and $\Omega(\kappa)$ on the number of runs; the kernel vector $\alpha$ of the variant is computed
before the first run in either order.
```

**(C)** Replace the closing sentence "For fixed $d$ this is
\[O\bigl((g_d+1)^{d\lceil\log_2(d+1)\rceil}\, b^3 (g_d^2+b^2)\bigr),\]and
$O\bigl(M_d b^2(g_d^2+b)+b^4\bigr)$ when $\nu$ is bounded; the term $b^4$ is the zero sum, which
depends only on $p$ and $\kappa_d$." with:

```latex
For fixed $d$ this is\[O\bigl((g_d+1)^{d\lceil\log_2(d+1)\rceil}\, b^3 (g_d^2+b^2)\bigr),\]and
$O\bigl(M_d b^2(g_d^2+b)+b^4\bigr)$ when $\nu$ is bounded; the term $b^4$ is the zero sum, which
depends only on $p$ and $\kappa_d$. When $\kappa_d$ is a prime power, in particular for every
$d \le 5$, the variant described above computes a witness of Schedule~1 within
\[
  T^{\mathrm{IS},\ast}_d = C_2\, d^3 (1+\log_2 d)\, M_d\, b^2\,(g_d^2 + b^2) + C_3\, d^4 b^5
\]
steps of one fixed multitape Turing machine, for absolute constants $C_2, C_3$ that are not
computed. This is $O\bigl(M_d b^2(g_d^2+b^2) + b^5\bigr)$ for fixed $d$, and the term
$C_3 d^4 b^5$ is again the zero sum. When $\kappa_d$ has two distinct prime factors, the argument
gives no bound better than $\nu+1$ runs, and the bound displayed above stands (AI-checked,
pending human review; \file{research/audits/reviews/2026-11-05-rees-is-restarts.md}, which also
records the tests of the variant, \texttt{collapse=True} in
\file{theorems/rees_is_sde_solver.py}).
```

Integrator notes:
- (C) gives a second bound, T^{IS,∗}_d, at prime-power κ_d (a new symbol, so that the
  displayed T^IS_d keeps its meaning). If `prop:coherent-receiver` is to use
  it, its machine 𝓜_d must be the variant's machine. The variant is deterministic and total at
  the same arity, so G1 is unaffected.
- The ERH remark (§4, Remark 4) is deliberately left out of the LaTeX.
- The sentence "Counting all of this … gives at most 40κ³Nb(a²+b²) multiplications" is still
  correct for the default algorithm and needs no change. Its variant analogue,
  11Ω(κ)κ³N(a²+b²) + O(κ³b³), is in §3 here.

## 9. Next

- **Hard question.** κ with two distinct primes (first case d = 6). Can a run be continued
  after an ℓ-part enlargement by reusing the surviving ℓ′-class structure, without raising the
  arity M_d? §5 shows that relabelling alone cannot work. Alternatively, can one prove that IS
  inputs cannot realise the stalling chains?
- **Mechanical.** Apply §8 (A)–(C), which is the integrator's call.
  - Acceptance test: `nice -n 10 /opt/anaconda3/bin/python -m pytest -q
    tests/test_rees_is_sde_solver.py` passes.
  - `collapse_stress.py` prints `ALL OK`, and `collapse_bound.py` (with `-O`) prints "simple
    form … OK".
