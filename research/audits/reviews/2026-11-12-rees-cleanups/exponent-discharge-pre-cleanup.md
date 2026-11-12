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
| Schedule 1 (core thm:is-import, lem:bezout) | B_κ(a) = G(κ,a)^{⌈log2(κ+1)⌉} | all p > c | no | deterministic | IS reading AI-checked only (rem:is-import(e)) |
| Schedule 1, zero-sum depth (main.tex sec:schedule1; IS audit 11-02, deviation (c)) | G(κ,a)^{⌈log2 t⌉} | all p > c | no | deterministic for the computed zero sum; Las Vegas for the shortest one (T1) | as above, plus the audit's claim "Any t ≤ 2^L works" |
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

**Conclusion (CONDITIONAL only on human review, at the same standard as thm:main).**
The worst-case solvers carry no hidden hypothesis beyond their stated prime ranges. The
law-derived solvers carry the label law, which holds for thm:main's input model.

## 2. Discharged statements (step 2)

**T1 (PROVED).**
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
- *Why 53 holds for all p > 9.* The exact scan covers p ≤ 3·10^6. Above that, t ≤ 3, so
  e_d ≤ 2κ_d. For even κ, t = 2 whenever (p−1)/κ is even. At c = 9, having 8 | p−1 forces
  (p−1)/2, (p−1)/4 and (p−1)/6 to be even. So only κ = 8 can cost 2κ, and
  E ≤ 1 + 2+3+4+5+6+7+16+9 = 53. This value is attained at p = 2521.
- *Comparison.* This lowers the core theorem's own bound from 145 to 53 at c = 9, with no
  Schedule 2 input. It is conditional only on the IS import, like the core theorem.

**T2 (PROVED, law-free, at the standard of thm:power-sde(ii)).**
- *Statement.* For every p ≥ 4c^{2c+2}, and also for every p ≥ 16c^{2c+2} as printed,
  Q = O_c((m+τ) m^{2(c−1)}), so **E = 2c−1** (17 at c = 9).
- *Sharper range via the triangular solver.* For every prime p > c with p ∉ ⋃_{d≤c}
  E_2(κ_d), the count is

    Q ≤ c(m+τ) ∏_{d=2}^c (g_d+1)(g_d+2)/2,

  which again gives E = 2c−1.
- *Explicit ranges.* The E_2 tables are finite computations, AI-checked.
  - For c ≤ 8 this holds for every p > 14281 (max E_2(8) = 14281).
  - For c = 9 it holds for every p > 14281 except primes p ≡ 1 mod 9 in E_2(9):
    - decided (414 members) for p ≤ 20000;
    - undecided on (20000, 3.10e9);
    - none above T_A(9) = 3.10e9.
  - So E = 17 holds unconditionally on the prime for p > 3.10·10^9.
- *At the undecided κ = 9 primes,* grade 9 costs 3 instead of 2, so E = 18:
  - by the 3·3 tower (law-free, degree 3) for p > 2125764;
  - by union chains in between (rem:app-s2-tower-scope).

**T3 (PROVED, law-free, all primes, finite tables).** The best per-grade combination,
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

**T4 (PROVED up to polylog factors, law-derived; at the standard of
thm:free-coordinate(iii)).**
- Weight-doubling nodes give Q = O_c(m^{2c−1} polylog m) for every p > ((c−1)(c−2)+3)²,
  where j* = 1 at every grade. At c = 9 that range is p > 3481.
- Over all p > c the exponent is 3, 6, 8, 10, 13, 14, 16, 19 (the paper's table,
  reproduced). Mixing in the law-free rule of T3 lowers c = 3 to 5 and c = 4 to 7.
  At c = 9 the value is 19, attained at p = 19.
- The polylog factor is log(1/τ_d) with τ_d ~ ε/poly(m) nodes. The factor (2log2 p + 6)^{j*}
  does not depend on m.

**T5 (PROVED, law-free, prime range growing with m).**
- Theorem A gives Q = O_c(m^{2c−1}/(log m)^{c−1}) for p ≥ about 72c² m^6 log² m.
- The uniform-p version gives F = O(a²/min(log a, log(p/a))). It gains only a power of
  log, never a power of m.

**Best proved exponent.** E = 2c−1 (17 at c = 9):
- law-free for p > 3.10·10^9 (and for p > 14281 when 9 ∤ p−1 or p ∉ E_2(9));
- up to polylog factors and using the oracle-model label law for p > 3481.

Over all primes p > c at c = 9:
- 19 law-derived;
- 37 law-free;
- 53 with Schedule 1 alone.

Each of these is CONDITIONAL on exactly one thing: human review of the AI-checked inputs,
namely the IS reading, appendix-schedule2 and the E_2 tables, and for T4 also
appendix-free-coordinate.

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

Using the E_2 tables makes 2521 quadratic at every grade, since 2521 ∉ E_2(κ) for κ ≤ 9 by
the tables and the scan. So **the 143 is an artefact of two things**: Schedule 1 charged at
full depth, and the coarse 16κ^{2κ+2} threshold, at a small prime ≡ 1 mod 2520.

Once every arity is quadratic, E = 1 + 2(c−1):
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

**5.1 Pool lemma (PROVED; no exponent gain with current solvers).**
- *Statement.* In prop:descent the targets with s_i = 0 are untouched: the translation is
  the identity on those slots. They remain in their post-measurement states ρ_{λ_i}, with
  known labels, in tensor product with everything else. So they may be returned to the
  grade-d pool and used in a later merge at the same grade. The amortized consumption per
  merge is then |supp s|, not M_d.
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

- Each merge applies M_d controlled translations. By thm:uniform-compilation(i)–(ii) each
  costs O(c³ D_d³) field operations, where D_d ≤ m. The QFTs are poly(log p, log 1/η).
- So the quantum gates are Q · O_c(m³ polylog), which gives a gate exponent ≤ E+3, plus
  classical solver time.
- The classical solver times of Schedule 2, triangular and Theorem A are polynomial. I did
  not pin down their degrees in g_d, and they could dominate. This is an upper-bound
  sketch, not a proved gate exponent.

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
