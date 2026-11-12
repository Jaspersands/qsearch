# 2026-11-12 Rees main theorem: which exponent of m can be proved now

**AI-checked, pending human review.** Written by one Claude session. I edited no paper,
STATE, handoff or reductions file. No git, no network, no Claude API calls.

Scripts and outputs are in `research/audits/reviews/2026-11-12-rees-exponent-discharge/`:
- `exponents.py` → `exponents.out`: the exponent tables.
- `two_register_reuse.py` → `two_register_reuse.out`: the reuse check of section 5.2.
- `witness_support.py` → `witness_support.out`: the support measurements of section 5.1.

All three are finite computations. They prove no asymptotic statement.

**Labels.** "PROVED" means there is a complete argument from results the paper already
proves, all of which are at the paper's own standard (AI-checked, pending human review).
The core theorem itself rests on the AI-checked reading of Ivanyos–Santha
(rem:is-import(e)). Nothing here has been read by a human.
**Relabelling after the referee (2026-11-12).** The paper's status convention calls a claim
*conditional* if it depends on thm:power-sde(ii) or prop:decoupled-sde (unread by a human)
or on finite AI computations. Under that convention T2 and T3 are **CONDITIONAL**, and so
are T4 and T5 (they depend on appendix-free-coordinate and Theorem A, unread). Only T1 has
the status of thm:main. Read every "PROVED" below as "complete argument from the cited
unread results", not as the paper's own "proved" label.

## 0. Setting and notation

The query count of thm:main is

  Q = c(m+τ) ∏_{d=2}^c M_d,

where M_d is the arity at grade d and g_d ≤ m. The exponent of m is

  E = 1 + Σ_d e_d,   with M_d = O(g_d^{e_d}).

Other notation:
- κ = κ_d = gcd(d, p−1).
- G(κ,a) = κ^{κ(κ−1)/2}(a+1)^κ.
- t = t(p,κ) is the least length of a zero sum of nonzero κ-th powers in F_p.

The exponents in the tables are maxima over primes p > c. They were computed exactly for
every prime p ≤ 30000 and, for c = 9, for every prime p ≤ 3·10^6. Above those ranges they
rest on the analytic arguments given with each claim.

## 1. Where each faster solver is still conditional (step 1)

| solver (locator) | per-grade arity | prime range | label law? | Las Vegas? | what keeps it conditional |
|---|---|---|---|---|---|
| Schedule 1 (core thm:is-import, lem:bezout) | B_κ(a) = G(κ,a)^{⌈log2(κ+1)⌉} | all p > c | no | deterministic (no solver failure) | IS reading AI-checked only (rem:is-import(e)) |
| Schedule 1, zero-sum depth (main.tex sec:schedule1; IS audit 11-02, deviation (c)) | G(κ,a)^{⌈log2 t⌉} | all p > c | no | Las Vegas (finding the shortest zero sum; the arity is public in advance), charged ε/3 via rem:is-import(d) (T1) | as above, plus the audit's claim "Any t ≤ 2^L works" |
| Schedule 2 (appendix-schedule2 thm:app-s2-main) | (a+1)((κ−1)a+1) | p ≥ 16κ^{2κ+2} as stated; 4κ^{2κ+2} in the proof (rem:app-s2-four) | no (worst case) | Las Vegas, never wrong | only review: thm:power-sde(ii) "stays conditional" because no human has read it; the Weil-bound locator |
| triangular / decoupled (prop:triangular-sde, prop:decoupled-sde) | (a+1)(a+2)/2 | p ∉ E_2(κ) (finite tables; above T_A(κ) by prop:app-s2-TA) | no | Las Vegas | review, and the E_2 tables are finite AI computations; κ = 9 is undecided on (20000, T_A(9) = 3.10e9) |
| tower / union chains (rem:app-s2-tower-scope, app:s2-chains) | degree Ω(κ)+1, or 3 (4 for some κ = 7 primes) | every p ≡ 1 mod κ outside NOSTD(κ) | no | Las Vegas | review and finite searches |
| Theorem A (audit 2026-11-07-rees-sde-subquad-A, refereed CORRECT) | D_J(a)+O(Ja) = O(a²/log a) | p ≥ max(8κ^{2E}E², 2Eaκ^E), about 72κ²a^6J² | no | Las Vegas | review, and a range that grows with a, i.e. with m |
| block-steered (rem:combined-schedule, option) | still quadratic | (G1)–(G3): p large compared with g_d² and n_d | yes | Las Vegas | law, plus a range that grows with m; never lowers E |
| Schedule 3(iii), weight-doubling (thm:free-coordinate(iii), rem:fc-witness-h3) | O((2log2 p+6)^{j*} g^{1+j*} log(1/τ)) | all p; j* = 1 once √p > (κ−1)(κ−2)+3 | yes | Las Vegas with bounded abort | law and review; polylog factors |
| Schedule 3, free-coordinate nodes | linear | all p | yes | — | classical time 2^{O(g log κ)}: fails the poly-gate requirement of thm:main |

Each hypothesis named in the task, checked against core/main-core.tex (the core):

- **Interface with prop:descent and lem:central.** No condition. prop:descent needs
  explicit scalars s_i (rem:is-import(a)). Every solver above returns either s_i
  directly or x ∈ (P_κ ∪ {0})^M. The latter is converted by lem:bezout (s_i = x_i^u),
  after Las Vegas κ-th roots where needed. Slots with weight 0 are inactive: the
  translation is the identity on them (thm:uniform-compilation(ii)). Only the label
  columns enter the solver, and the scalars act on the centre through lem:central exactly
  as for Schedule 1. **PROVED.**
- **Las Vegas versus bounded error.** No condition. rem:is-import(d) handles any solver
  that either reports failure or returns a solution, and whose output is checked. It
  needs a failure rate ≤ 1/4 and an explicit expected time. The call count N_solver is
  fixed in advance, retries run on the same saved labels, and the abort costs ε/3.
  Schedule 2, triangular, Theorem A and towers all meet this. **PROVED.**
  The bounded-abort nodes of Schedule 3 need their own error split (thm:free-coordinate);
  this note does not re-check it.
- **Worst-case versus average banks; label distribution.** Schedule 2, triangular,
  towers, chains and Theorem A are worst-case, so they need no law. Schedule 3 and the
  block-steered option need the law of lem:s3-law. That law is the measured-label law on
  the i.i.d. supply that thm:main's ideal procedure provides: fresh oracle samples, fixed
  public arities, exact intermediate sources ρ_{H_d}. The implemented procedure is within
  ε of the ideal one by the hybrid lemma, so a law-derived bound transfers with that
  error.
  - **PROVED for the oracle model of thm:main**, at the paper's standard.
  - **Not valid** when banks are adversarial or reused (see 5.1).
- **Independence across merges.** In the ideal procedure each bank is a fresh product of
  i.i.d. labeled sources, so independence holds (above). Independence fails for pooled
  leftovers (5.1). That is harmless for worst-case solvers and fatal for law-derived ones
  unless re-proved.
- **Prime range.** This is the only mathematical (non-review) obstruction. It is
  quantified in section 2.

**Conclusion (CONDITIONAL on human review and on the finite computations named in the Labels paragraph).**
The worst-case solvers carry no hidden hypothesis beyond their stated prime ranges. The
law-derived solvers carry the label law, which holds for thm:main's input model.

## 2. Discharged statements (step 2)

**T1 (PROVED given the IS reading; status of thm:main, rem:is-import(e)).**
- *Statement.* Schedule 1 alone (no Schedule 2) at degree κ_d, using the shortest zero sum
  of κ_d-th powers, has arity G(κ_d, g_d)^{⌈log2 t_d⌉}. Here t_d = 2 for odd κ_d, and
  t_d = p when κ_d = p−1. With this arity, the query count of thm:main holds for every
  prime p > c and every H. Its exponent is E_S1t(c) = 5, 8, 16, 19, 35, 36, 44, 53 for
  c = 2..9, maximized over all primes p > c.
- *Finding the zero sum.* Las Vegas, in poly(κ, log p) time:
  - t = 2: a κ-th root of −1 by Rabin root finding.
  - t = 3 (guaranteed by Weil once p + 1 − (κ−1)(κ−2)√p > 3κ): pick a random x, test
    whether −1 − x^κ ∈ P_κ, and take its root.
  - t ≥ 4: occurs only for p below a bound depending on κ; there use exhaustive search
    in O_κ(1) time.

  The solver is then Las Vegas, and rem:is-import(d) applies.
- *Why the shortest zero sum is allowed.* The IS audit 2026-11-02, deviation (c), states
  "Any t ≤ 2^L works" in the final step. main.tex sec:schedule1 already states the count
  G(κ_d, a)^{⌈log2 ℓ_d⌉} for the computed zero sum ℓ_d. Using the shortest one is my step.
  The referee confirmed it against IS §3.3 (iterating Theorem 11 L times gives one vector with
  2^L representations with disjoint supports; scale representation j by z_j, where
  Σ_{j≤t} z_j^d = 0, and give the others weight 0), and an exact simulation gave 60/60
  verified witnesses. Two additions: (i) Theorem 11 allows J = ∅; in that case stop at once,
  since a solution is already found. (ii) The depth ⌈log2 t⌉ is public before the run: t = 2
  iff (p−1)/κ is even; otherwise ⌈log2 t⌉ = 2 once p+1−(κ−1)(κ−2)√p > 3κ; exhaustive search
  below that. Only finding the length-3 or length-4 zero sum is Las Vegas, so the core's
  "deterministic, no solver failure to budget" becomes rem:is-import(d) with ε/3.
  Ivanyos's confirmation covers C ≤ G^{⌈log2(d+1)⌉}, not this t-depth variant, which is an AI
  reading of the same proof (rem:is-import(e) standard).
- *Why 53 holds for all p > 9.* The exact scan covers p ≤ 3·10^6. Above that, t ≤ 3, so
  e_d ≤ 2κ_d. For even κ, t = 2 whenever (p−1)/κ is even. At c = 9, having 8 | p−1 forces
  (p−1)/2, (p−1)/4 and (p−1)/6 to be even. So only κ = 8 can cost 2κ, and
  E ≤ 1 + 2+3+4+5+6+7+16+9 = 53. This value is attained at p = 2521.
- *Comparison.* This lowers the core theorem's own bound from 145 to 53 at c = 9, with no
  Schedule 2 input. It is conditional only on the IS import, like the core theorem.

**T2 (CONDITIONAL, law-free; on thm:power-sde(ii) / prop:app-s2-TA, which main.tex keeps conditional, and below T_A on finite E_2 computations).**
- *Statement.* For every p ≥ 4c^{2c+2}, and also for every p ≥ 16c^{2c+2} as printed,
  Q = O_c((m+τ) m^{2(c−1)}), so **E = 2c−1** (17 at c = 9).
- *Sharper range via the triangular solver.* For every prime p > c with p ∉ ⋃_{d≤c}
  E_2(κ_d), the count is

    Q ≤ c(m+τ) ∏_{d=2}^c (g_d+1)(g_d+2)/2,

  which again gives E = 2c−1.
- *Explicit ranges.* The E_2 tables are finite computations, AI-checked.
  - For c ≤ 8 this holds for every p > 14281 (max E_2(8) = 14281).
  - For c = 9 it holds for every p > 14281 except primes p ≡ 1 mod 9 in E_2(9):
    - decided for p ≤ 20000: 342 members among the 372 primes p ≡ 1 mod 9 in that range
      (30 non-members), max 19963; decided to 25000 with 414 members;
    - explicit contractions cover every prime in (20000, 9^9/2] except 1373 listed
      primes; 78 of those (those below 25000) are decided (72 members, 6 non-members). The
      undecided set is the 1295 listed primes in (25000, 424549] together with
      (9^9/2, T_A(9)];
    - none above T_A(9) = 3.10e9.
  - So E = 17 holds unconditionally on the prime for p > 3.10·10^9.
- *Cost of the contraction search.* In the bands T_A(κ) < p ≤ T_S(κ) and p ≤ T_A(κ) the
  contraction, and E_2 membership, are found by exhaustive search. That is O_κ(1), but at
  κ = 9 it is about p^κ with p up to 2.8·10^10, so "polynomial time" holds there only with an
  astronomically large constant.
- *At the undecided κ = 9 primes,* grade 9 costs 3 instead of 2, so E = 18:
  - by the 3·3 tower (law-free, degree 3): in closed form for p > 2125764, and for
    p > 1.347·10^5 via the numerical T_R(9,3) (a numerical evaluation of a proved criterion);
    complete searches cover p ≤ 135000 (rem:app-s2-tower-scope);
  - by union chains in between (rem:app-s2-tower-scope).

**T3 (CONDITIONAL, law-free, all primes; finite tables, NOSTD/E_2/chain data quoted, not re-run).** The best per-grade combination,
chosen from public (p, d, g_d), uses:
- linear arity at κ = 1;
- the two-level / triangular arity when p ∉ E_2(κ);
- otherwise the cheaper of Schedule 1 with zero-sum depth (T1), the tower, a union chain,
  and the κ = 7 three-step chain.

Its exponent, maximized over p > c, is E_R5 = 3, 5, 16, 14, 28, 29, 36, 37 for c = 2..9.
- c = 9: maximum 37, attained at p = 41 and p = 73.
- c = 9, p > 20000: ≤ 18.
- c = 9, p > 3.10e9: 17.

The rule uses no law and no information about H. This is valid because every component is
worst-case and Las Vegas.

**T4 (CONDITIONAL; up to polylog factors, law-derived; on thm:free-coordinate(iii) and the ideal i.i.d. label supply of thm:main only).**
- Weight-doubling nodes give Q = O_c(m^{2c−1} polylog m) for every p > ((c−1)(c−2)+3)²,
  where j* = 1 at every grade. At c = 9 that range is p > 3481.
- Over all p > c the exponent is 3, 6, 8, 10, 13, 14, 16, 19 (the paper's table,
  reproduced). Mixing in the law-free rule of T3 lowers c = 3 to 5 and c = 4 to 7.
  At c = 9 the value is 19, attained at p = 19.
- The polylog factor is log(1/τ_d) with τ_d ~ ε/poly(m) nodes. The factor (2log2 p + 6)^{j*}
  does not depend on m.

**T5 (CONDITIONAL, law-free, prime range growing with m; on Theorem A, refereed CORRECT but unread by a human).**
- Theorem A gives Q = O_c(m^{2c−1}/(log m)^{c−1}) for p ≥ about 72c² m^6 log² m.
- The uniform-p version gives F = O(a²/min(log a, log(p/a))). It gains only a power of
  log, never a power of m.

**Best proved exponent.** E = 2c−1 (17 at c = 9):
- law-free for p > 3.10·10^9 (and for p > 14281 when 9 ∤ p−1 or p ∉ E_2(9));
- up to polylog factors and using the oracle-model label law for p > 3481.

Over all primes p > c at c = 9:
- 19 law-derived (the paper's LAW table; O(m^19 polylog m), not m^19; ideal i.i.d. supply only,
  not pooled leftovers or the black-box corollaries);
- 37 law-free: a finite computation over the quoted NOSTD/E_2/chain lists (at p = 41, κ_8 = 8,
  the 8th powers are μ_5, t = 5, and that grade costs 24); NOT re-run here;
- 53 with Schedule 1 alone (verified independently by the referee: E_S1t = 5, 8, 16, 19, 35, 36,
  44, 53, Weil tail max 53).

Each of these is CONDITIONAL. The conditions are human review of the AI-checked inputs (the IS
reading, appendix-schedule2, appendix-free-coordinate), and also the finite AI computations
(E_2 tables, NOSTD lists, chain searches), the numerical thresholds (T_R(9,3), Θ_2, Θ_3) and
the O_κ(1) exhaustive-search constants. More than review remains.

**Other rule rows (exponents.out, c = 2..9), for reference.**

| rule | values for c = 2..9 |
|---|---|
| S1ONLY (core) | 5, 11, 23, 38, 56, 77, 109, 145 |
| PAPER (rem:combined-schedule) | 5, 11, 23, 38, 56, 77, 107, 143 |
| R1 (threshold 4κ^{2κ+2}) | 143 at c = 9 (c = 7 becomes 75) |
| R1t (R1 + zero-sum depth) | 53 |
| RTAt (threshold T_A + zero-sum depth) | 50 |
| R2 (E_2 tables only, full-depth fallback) | 99 |
| R3 = R4 (+ zero-sum depth, + tower) | 40 |
| R5 (+ chains) | 37 |
| LAWMIX | 19 |

## 3. Why the paper's figure at c = 9 is 143 (step 3)

At p = 2521 = 1 + 2520, κ_d = d for every d ≤ 9. Schedule 2's threshold
16κ^{2κ+2} ≤ 2521 holds only for κ = 2. The other grades fall back to Schedule 1 at full
depth ⌈log2(κ+1)⌉:

e = [2, 6, 12, 15, 18, 21, 32, 36], so E = 1 + 142 = 143.

Charging ⌈log2 t⌉ instead of ⌈log2(κ+1)⌉ gives e = [2, 3, 4, 5, 6, 7, 16, 9], so E = 53
(T1). Odd κ has t = 2. Even κ = 2, 4, 6 has t = 2 because (2520/κ) is even. κ = 8 has
2520/8 = 315 odd, so t = 3 or 4.

The E_2 tables alone do NOT make 2521 quadratic at grades 8 and 9: 2521 ∈ E_2(8) and
2521 ∈ E_2(9) (dfs2b tables; `in_E2` agrees). At p = 2521 the E_2-only rule (R2) gives 81,
R3 gives 38 and R5 gives 20 (grades 8 and 9 cost [16, 9] under R3 and [4, 3] under R5),
not 17 (recomputed with exponents.py). So **the 143 is an artefact of Schedule 1 being
charged at full depth and of the coarse 16κ^{2κ+2} threshold at a small prime ≡ 1 mod 2520**,
but the E_2 tables alone do not repair it; the zero-sum depth (T1, 53), then towers and chains
(R3, R5), do.

At primes where every arity is quadratic (not 2521), E = 1 + 2(c−1):
- the product of the c−1 grade arities, m^{2(c−1)}, dominates;
- the remaining factor m is the c(m+τ) terminal samples.

In the law-free all-prime worst case (T3, 37 at c = 9) the dominating term is instead a
single bad grade: κ_8 = 8 at p = 41. The 8th powers there are μ_5, the shortest zero sum
is 1+10+18+16+37 = 82 ≡ 0 (t = 5), and no two-level, tower or chain construction exists
there (41 ∈ NOSTD(8)). That grade costs 8·3 = 24 of the 37.

## 4. Lowering the dominating term (step 4)

**4.1 Grade order (REFUTED as a source of gain).** The grades are the lower-central
quotients. The merge at grade d acts on a source in which grade d is the central top layer
(lem:central), and that source exists only after the grades below d have been resolved. A permutation of grades is therefore
unavailable. A coarser filtration merges grades and raises κ, so the arity only increases.
This is not a theorem about all algorithms, only about this recursion: I found no
alternative order compatible with prop:descent.

**4.2 Lower floor for this architecture (PROVED).** Suppose a bank of M ≥ a+1 columns is in
general position, meaning every a columns are independent. Then every nonzero solution of
Σ s_i^d λ_i = 0 has support ≥ a+1. Hence any architecture that consumes the active targets
of each witness pays ≥ g_d+1 per merge. That gives E ≥ 1 + (c−1) = c, provided g_d = Θ(m)
at some grades. Uniform labels are in general position with probability 1 − O(M^a/p), so
the floor also applies on average.

The existence threshold is κa+1 columns (Chevalley–Warning: a forms of degree κ in M > κa variables), still linear. So
the gap from 2c−1 down to c is purely an SDE-*finding* gap: no poly-time law-free finder
with linear support is known.

## 5. Label reuse (step 4, continued)

**5.1 Pool lemma (PROVED, mathematically sound per the referee; no exponent gain with current solvers; keep out of the core).**
- *Statement.* In prop:descent the targets with s_i = 0 are untouched: the translation is
  the identity on those slots. They remain in their post-measurement states ρ_{λ_i}, with
  known labels, in tensor product with everything else. So they may be returned to the
  grade-d pool and used in a later merge at the same grade. The amortized consumption per
  merge is then |supp s|, not M_d.
- *Core-procedure caveat (referee).* The lemma changes the core procedure, which "consumes and
  discards" weight-0 targets, and makes the tree adaptive; N_QFT would need a public upper
  bound. Since it gives no gain, keep it out.
- *Caveat (adversarial).* A leftover's label was an input to the witness choice, so the
  pool's labels are not i.i.d. uniform. The lemma is valid with worst-case solvers only,
  not with Schedule 3 or the block-steered option, unless their law is re-proved for
  biased pools.
- *Finite measurement (witness_support.out, 40 samples each, sampled, not exact).* The
  Schedule 2 two-level witness support on uniform columns tends to the full arity:

  | κ, a | support / arity |
  |---|---|
  | κ = 3, a = 6 | 91/91 |
  | κ = 3, a = 8 | 153/153 |
  | κ = 4, a = 8 | 224.93/225 |
  | κ = 2, a = 8 | 80.97/81 |

  Small-a dips come from blocks whose level-two coefficient vanishes.
- *Conclusion.* Generic supports are ≈ M_d. **UNKNOWN** whether any existing solver has
  support o(M_d) generically. The IS witness support was not measured.

**5.2 Two address registers on one set of targets (REFUTED as a free reuse).**
- *Idea.* Apply two independent merges, with rank-2 scalar matrix [s; s'], to the same
  targets, hoping for ρ_{H̄} ⊗ ρ_{H̄}.
- *Exact check* (two_register_reuse.out, Heisenberg over F_3, all label pairs, all
  rank-2 solution pairs).
  - The single-register descent matches ρ_{H̄} to 1.2e−16 in every case.
  - With two registers and overlapping supports, H = ⟨x⟩ and H = ⟨x+y⟩ fail in 16 of 56
    pairs, at trace distance 0.6667. Example: labels (1,2), s = (1,1), s' = (1,2).
  - For H ⊇ Z and for H = 1 all pairs succeed.
- *Conclusion.* Reuse fails exactly in the nonnormal case H ∩ Z = 1 that the descent
  exists for. Disjoint supports are just two merges.
- *Not run.* p = 5 was stopped as too slow in pure Python, so this is a single-field
  counterexample, which suffices for refutation.

**5.3 Net effect of step 4.** Neither reuse nor reordering lowers the exponent with the
current solvers. Lowering 2c−1 toward the floor c requires a new SDE finder (section 7).

## 6. Gate count (UNKNOWN beyond a sketch)

- Referee's bound (check 4), adopted: controlled translations number ≤ (c−1)·#sources = O(Q),
  each 4·(d−1)d(d+1)/2 brackets × O(D³) = O_c(m³) field operations. QFTs: O(Q·m), each
  poly(log p, log(m/ε)). Classical solver work per merge (triangular: O(a) eliminations of size
  a×(a+1), plus O(M) coset tests and roots; Schedule 2: N nullspaces plus one of size
  (κ−1)a×N) is O(a² + poly(κ, log p)) per column and does not dominate.
- Total: O_c(Q·m³·poly(log p, log(m/ε))) + O(Q·w), plus the O_c(1) contraction-search
  constants: gate exponent E+3 = 2c+2 (20 at c = 9), up to polylog factors and the w term.
  CONDITIONAL, as T2. (Replaces my earlier "UNKNOWN".)

## 7. Adversarial self-check

1. *Is T1 really free of Schedule 2?* Yes. It uses only thm:is-import, lem:bezout,
   rem:is-import(d) and the audit's deviation (c). Risk: the claim "any t ≤ 2^L works"
   is an AI audit statement. If the IS final step needed the vdW zero sum specifically,
   T1 would revert to ℓ_d, the computed length. The deterministic count would then rise
   at primes where vdW returns t > shortest.
2. *The zero-sum length table* is exhaustive for p ≤ 30000 and uses the Weil shortcut
   above. The Weil inequality used is the standard Fermat-curve bound; I did not re-derive
   its constant.
3. *E_2 data are finite AI computations.* κ = 9 above 20000 is treated as a member
   (conservative). If a listed non-member were in fact a member, T2's range would shrink
   at that prime, not its exponent. T3 would cost at most 1 more there via chains/towers,
   and more only at a NOSTD prime.
4. *NOSTD completeness* (rem:app-s2-tower-scope) is quoted, not re-run. A missed NOSTD
   prime could raise T3 above 37: for instance a κ = 8 prime with t ≥ 5 would cost 24.
5. *Law-derived claims (T4)* depend on the oracle-model i.i.d. supply. They are invalid
   with pooled leftovers (5.1) and for the black-box-group variants that do not supply
   fresh i.i.d. labels. I did not check those variants.
6. *Polylog factors* in T4 and Theorem A are not powers of m. They affect "exponent"
   claims only if one insists on exact m^E.
7. *E counts m.* Using g_d instead gives the sharper ∏(g_d+1)(g_d+2)/2. All tables use
   the worst case g_d ~ m at every grade.

## 8. Strongest counterexample attempt

I tried to show that 2c−1 is not provable law-free for all primes, i.e. that some prime
forces a super-quadratic grade for every listed construction. Result: at c = 9, p = 41,
κ_8 = 8, all listed law-free constructions fail (NOSTD), and Schedule 1 needs t = 5. That
pins the law-free all-prime value at 37 for these tools. It is not a lower bound for
algorithms: at fixed p = 41 the equation has a solution at 8a+1 columns
(Chevalley–Warning), so only *finding* is in question.

I tried to beat the floor c by reuse: refuted (5.2). I tried to get sub-quadratic
supports: not with the current solvers (5.1).

## 9. Next hard question

Give a poly(a, log p)-time, law-free (worst-case bank) Las Vegas algorithm that finds a
nonzero solution of Σ s_i^κ λ_i = 0 over F_p^a from O_κ(a) columns, for one fixed κ ≥ 2,
even at a single fixed small prime. Test case: κ = 8, p = 41, where the 8th powers are μ_5.
An equivalent form is the linear-arity weighted zero-sum finding problem over F_41^a with
weights in μ_5 ∪ {0}. Any κ = 2 analogue at a fixed p would already lower one grade from 2
to 1.

**Next command.**

    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-12-rees-exponent-discharge/exponents.py

**Expected artifact.** `exponents.out` unchanged.

**Acceptance test for any new finder.**
- It returns verified witnesses at M = O(a) on adversarial banks for κ = 8, p = 41,
  a ≤ 40.
- Its running time is polynomial in a.

## Cleanup (2026-11-12)

Applied per `2026-11-12-rees-exponent-discharge-referee.md`. Pre-cleanup copy:
`2026-11-12-rees-cleanups/exponent-discharge-pre-cleanup.md`. Numbers re-verified by me:
E_2(9) ≤ 20000 has 342 members, 30 non-members, 0 undecided (372 primes ≡ 1 mod 9; json
count), E_2(8) has 293; 2521 is a member of both (json); per-rule exponents at p = 2521 from
`exponents.e_grade`: R2 81, R3 38, R5 20 (R4 26, R1t 53). The 414/25000 and 1373/78/1295
figures are copied from 2026-11-10-rees-dfs2b-queue-final.md l. 90–91 (not recomputed); T_A
values, E_S1t and the Weil tail are from referee_checks.out (not recomputed).

1. Labels paragraph: added relabelling (T2, T3, T4, T5 CONDITIONAL; only T1 has thm:main status).
2. §1 table, Schedule 1 zero-sum row: "deterministic" replaced by Las Vegas / public arity / ε/3 via rem:is-import(d); Schedule 1 row clarified.
3. T1: heading status; J = ∅ sentence; public-arity rule; Las Vegas charge; Ivanyos coverage caveat; referee's confirmation of IS §3.3.
4. T2: heading CONDITIONAL; "414 members for p ≤ 20000" replaced by 342 of 372 (414 only for ≤ 25000); undecided set restated (1373/78/1295, plus (9^9/2, T_A(9)]); added the O_κ(1) search-cost caveat; tower status (1.347·10^5 numerical, 2125764 closed form, searches to 135000).
5. T3, T4, T5 headings relabelled CONDITIONAL, with their conditions named.
6. "Best proved exponent" block: 19 is O(m^19 polylog m) under the label law only; 37 is a finite computation over quoted lists, not re-run; 53 verified; "exactly one thing" replaced by the fuller list of conditions.
7. §3: removed the false "2521 ∉ E_2(κ) for κ ≤ 9"; restated the artefact paragraph with R2 81, R3 38, R5 20; changed "every arity is quadratic" to "at primes where every arity is quadratic (not 2521)".
8. §5.1: added referee's core-procedure caveat; kept out of the core.
9. §6: UNKNOWN gate count replaced by the referee's bound, O_c(Q·m³·polylog)+O(Q·w), exponent 2c+2 (20 at c = 9), CONDITIONAL.
Not applied (not in the note's scope): core/paper edits (already dispositioned by the integrator); §7 and §8 text untouched.
