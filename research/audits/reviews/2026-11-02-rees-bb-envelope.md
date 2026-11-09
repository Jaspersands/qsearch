# Rees round 2, item 7: total cost envelope for black-box nilpotent HSP (gap C6)

Date: 2026-11-02. AI session (Claude Code, Opus 5.5), item 7 of `research/REES_FULL_CAMPAIGN_2.md`.
**No human review.** Nothing here changes a claim gate, a registry, `STATE.md` or the paper.

**Read.** `research/STATE.md`; `research/TRAPS.md`; round-1 reports
`2026-11-02-rees-black-box-check.md` (all), `-fpt-torsion-check.md` (all),
`-prime-power-compiler.md` (all), `-combined-schedule.md` §§1–3, `-is-solver.md` §7;
`docs/papers/rees-hsp/main.tex` lines 174–216, 405–556, 595–640;
`research/REES_WHOLE_PROOF_SCOPE_AUDIT.md` lines 225–290; `theorems/rees_hsp_reduction.py`
(`recovery_budget`, `black_box_large_prime_budget`). **Full text** of Imran–Ivanyos,
arXiv:2304.08376v1, fetched from arxiv.org and read in Thm 1 (p. 4), Prop 1 with Algorithm 1
and its count (pp. 9–10), Lemma 2 and Props 2–3 (p. 12), Lemma 3, Props 4–5 and Thm 2
(pp. 13–16, page 16 rendered and read as an image).

**Scripts** (folder `research/audits/reviews/2026-11-02-rees-bb-envelope/`):

- `bb_envelope_check.py` → `bb_envelope_check.out`. Exact integers; imports the repo's
  `black_box_large_prime_budget` and `sde_arity` read-only to cross-check. About 1 min.
  `/opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-bb-envelope/bb_envelope_check.py`
- `word_counts.py` → `word_counts.out`. Compiles and exactly verifies the inverse-BCH word
  certificates for c = 2..9 and prints their (mul, pow) counts.

`git status --short` before and after differs only by this report and its folder.

## 0. Verdict

- **The gap closes, conditionally.** One theorem (§3) now charges every stage of the
  black-box route: Sylow split, Imran–Ivanyos (II) on primes p ≤ c, the free pullback and its
  word evaluation mod p^e, ker Φ as an abelian HSP, the explicit chart, the core per F_p
  section under the combined Schedule 1/2 rule, the e > 1 whole-socle recursion with its stop
  rules, gates, classical arithmetic and every error share.
- **The free pullback should be used only to acquire the chart (route R2).** The query
  count is then independent of s. Running the core on F_{s,c} itself costs exponent c·E in s
  (1287 at c = 9 under rule W) instead of E in ℓ (§2.7, exact check).
- **f-query exponent in ℓ at fixed c: E_W(c) + 1.** This is 144 at c = 9 (146 with
  Schedule 1 alone), against the withdrawn 147. The +1 comes from the e > 1 recursion
  (≤ n_p calls); Sylows of exponent p cost only E_W(c) = 143. The old b(b+1) call cap, which
  belongs to a chain-pass scan, is replaced by the whole-socle recursion's ≤ n_p calls.
- **Gate exponent: E_W(c) + 4 + o(1)** (147 + o(1) at c = 9; the number coincides with the
  withdrawn query exponent but is a different count). Classical SDE time has exponent
  E_W(c) + 1 + β̂_c, where β̂_c is the excess time exponent of the Ivanyos–Santha solver,
  which [IS15] states only as polynomial. **So the total-time exponent is not explicit;
  the query exponent is.**
- **Imran–Ivanyos at p ≤ c is much cheaper in queries.** Read from their proofs, their
  query exponent in n = log_p|G_p| is 2 + (c−1)σ_p + α_22: 10, 18, 50, 50 for p = 2, 3, 5, 7 at
  c = 9. So the large primes set the all-prime exponent. α_22 (the query exponent of their
  exact abelian subroutine [II22]) was not read, so it stays UNKNOWN.

## 1. Setting and access model

- **Group.** G is a finite group, promised nilpotent of class ≤ c (c fixed). Elements have
  unique ℓ-bit encodings, so |G| ≤ 2^ℓ. Access is by the identity, generators g_1, …, g_s, and
  coherent multiplication U_G|x⟩|y⟩ = |x⟩|xy⟩ with its inverse (the IMS black-box model).
  Inverses are powers.
- **Hiding function.** f is coherent, with label width w and internal cost T_f, for an
  **arbitrary** H ≤ G: f(x) = f(y) ⟺ x⁻¹y ∈ H.
- **Output.** Generators of H, with probability ≥ 1 − ε.
- **Input size.** N = sℓ + w + ⌈log₂(1/ε)⌉.
- **Notation.** For p | |G|, G_p is the Sylow subgroup, n_p = log_p|G_p| and p^{e_p} = exp G_p.
  L := Σ_{p>c} n_p ≤ ℓ/log₂(c+1). κ_d = gcd(d, p−1), and e_d(p) ∈ {1, 2, κ_d⌈log₂(κ_d+1)⌉} is
  the grade exponent of rule W (Remark `rem:combined-schedule`). E_W(c) = max_{p>c}(1 + Σ_{d=2}^c e_d(p))
  and E_1(c) = 1 + Σ_{d=2}^c d⌈log₂(d+1)⌉.
- **Conditional on:** Thm `thm:main` (steps 1–5, AI-checked); Schedule 2 (Thm
  `thm:power-sde`(ii), AI-only) through rule W; for e_p > 1, Thm `thm:ring-to-field`(iii)
  (idealizer, quotient oracle, termination, stop rules: AI-checked in the fpt-torsion check
  B3); the prime-power word lemma (prime-power-compiler §2, AI proof). **Imported:** II Thm 1;
  Shor order finding and factoring; [IS15]; Lazard/Khukhro/Trappeniers.

## 2. Stage-by-stage costs

Labels: **[proved]** a written proof here or in the cited report; **[argued]** a standard
argument, not written out; **[imported]** a published theorem; **[exact]** a script check.

### 2.1 Sylow split (preprocessing, share ε/4)

**[proved, black-box check C1]**

- Run quantum order finding on each g_i, then Shor factoring of each o_i < 2^ℓ.
- Certify each order classically: g^{o} = 1, g^{o/q} ≠ 1 for every prime q | o, with the
  primes certified by deterministic primality testing. A wrong run is therefore detected,
  and the step is Las Vegas. Cap the repetitions at O(log(s/ε)) per generator.
- The primes of |G| are exactly the primes of the o_i. |G| is not needed.
- The CRT powers g_i^{(p)} generate G_p.
- e_p = max_i v_p(o_i) for p > c, because groups of class < p are regular. The loose
  M = p^{⌊ℓ/log₂ p⌋} is also valid and costs only b_M = ⌈log₂ M⌉ ≤ ℓ.
- **Cost:** O(sℓ log(s/ε)) controlled group multiplications for order finding, Õ(sℓ⁴)
  gates to factor s numbers below 2^ℓ completely (at most ℓ splits each, Õ(ℓ³) per Shor
  run), and O(sℓ²) multiplications for the projections. **Zero f queries.**
- H = ∏_p (H ∩ G_p), and f|_{G_p} hides H ∩ G_p.

### 2.2 Primes p ≤ c: Imran–Ivanyos Thm 1 (share ε/4)

**[imported]**, composition **[proved, C2]**.

- Apply II Thm 1 to G_{≤c} = ∏_{p≤c} G_p. This is a black-box subgroup with the same
  encoding, generated by the projections, of class ≤ c, and its primes are ≤ c. Prop 1's
  "prime factors given as input" is supplied by §2.1.
- One "call" is one f query plus one uniform-superposition preparation over G_{≤c}, or
  its inverse (II §2.2–2.4).
- II is exact in a gate model with exact QFTs modulo bounded primes. Here each such gate is
  synthesized approximately, and the synthesis error is charged to this ε/4. The count is
  poly(ℓ) gates with a c-dependent exponent that II does not make explicit, so the precision
  bits are O(log ℓ + log(1/ε)).
- **Query count read from II's proofs [argued, full text]:**
  - Prop 1 (p. 10) makes at most n² HSMC calls when |G_p| = p^n.
  - Each HSMC (proof of Prop 2, p. 12) converts ∏_{i=2}^c S(p, n_i) copies into one abelian
    oracle call, and the exact abelian algorithm [II22] then makes n^{α_22} such calls, with
    α_22 unknown.
  - Props 4–5 give S(p, n) = S_±(p, n)^{⌈log₂ p⌉}. The induction in Prop 4's proof runs
    ⌊log₂ d₀⌋ halvings (d₀ = (p−1)/2), so S_± ≤ C_p (n+1)^{2^{⌊log₂ d₀⌋}}.
  - Hence the n-exponent of S is σ_p = 2^{⌊log₂((p−1)/2)⌋}·⌈log₂ p⌉ for odd p, and σ_2 = 1.
  - II's printed display on p. 16 writes ⌈log⌉ in this exponent and then an equality with
    (n+1)^{⌈(p−1)/2⌉}. Under the ⌈⌉ reading, σ_7 would be 12 instead of 6, and the printed
    "=" would be false for p = 7. This does not affect II's O(p) claim.
  - Total f queries for G_p: O_{c}(n^{2 + (c−1)σ_p + α_22}).
- **Time:** poly(T(p,n)^{O(c)} ℓ), with T = poly(S). The exponent is not explicit in II.

### 2.3 Primes p > c: pullback and word evaluation mod p^{e_p}

**[proved, prime-power compiler §2; exact checks there]**

- Φ : (F_{s,c}(Z/M), ∗) → G_p, with x_i ↦ g_i^{(p)} and M = p^{e_p}, is a surjective
  homomorphism.
- It is evaluated by the certified inverse-BCH words, with rational powers a/b taken as
  a·b⁻¹ mod M. This is valid for every c < p and every e.
- d = rank F_{s,c} = Σ_{k≤c} W(s,k) ≤ Σ_{k≤c} s^k.
- **Precomputation:** ≤ (d−s)(m_[] + 2b_M q_[]) multiplications.
- **One coherent evaluation:** ≤ d(2b_M + m_+ + 2b_M q_+) multiplications, at most doubled
  by Bennett cleanup.
- (m_+, q_+) / (m_[], q_[]) are exactly verified here (`word_counts.out`): c = 5: 118/44,
  116/42; c = 6: 230/88, 228/86; c = 7: 498/184, 496/182; c = 8: 978/368, 976/366. These match
  the prime-power report. **New: c = 9: 2026/752 and 2024/750** (verified in 132 s and
  118 s). So A_9(M) = 2026 + 1504·b_M.

### 2.4 ker Φ and the chart (R2; share ε/4; zero f queries)

**[proved, black-box check C5, plus the corrections below]**

- **Fibres.** x ↦ Φ(x) is constant exactly on the additive cosets of ker π in
  (F, +) ≅ (Z/M)^d. This holds because Φ = exp∘π, exp is a bijection, and the encoding is
  unique.
- **Abelian HSP.** Each sample is uniform on (ker π)^⊥, a group dual to the additive group
  of L(G_p).
- **Correction to C5's sample count.** That dual has module rank r = number of cyclic
  factors of L(G_p), which is n_p when e_p = 1. It is **not** bounded by s: Lie generation by
  s elements does not bound module rank. C5's "O(d + log 1/ε)" is valid but loose. The right
  count is k = r + t′ samples; k uniform samples fail to generate with probability
  < p^{r−k}/(p−1). Since n_p is unknown before the chart, take k = ⌊ℓ/log₂ p⌋ + t′, with
  t′ = ⌈log_p(8ℓ/ε)⌉.
- **Per-sample cost:** one coherent Φ evaluation and d approximate QFTs over Z/M.
- **Readout.** The k×d sample matrix Y gives ker π = ker Y (Howell form over Z/M,
  O(k²d) ring operations) and the chart F/ker π ≅ im Y.
- **Verification (optional, makes the step Las Vegas).** Check Φ(x) = 1 on the returned
  kernel generators.
- **Structure constants [argued].**
  - Choose ≤ r Hall (Lyndon) basis elements whose Y-columns span im Y mod p. By Nakayama,
    they generate L(G_p) as a module.
  - Expand their ≤ r² brackets in the truncated free associative algebra, with triangular
    Lyndon coordinate extraction, at O_c(s^c) operations each, and map them by Y.
  - Take the Smith form of the generator matrix, then change basis.
  - Total O_c(s^c ℓ³ + ℓ⁴) ring operations mod M, each O(b_M²) bit operations.
- **Chart-to-group map.** Precompute E_i = Φ(σ(ε_i)) for the chart basis, at
  ≤ n_p² (2b_M + A_c) multiplications. After that, exp(Σ x_i ε_i) = ADD-fold of the E_i^{x_i},
  at **T_Φ ≤ 4n_p(2b_M + A_c(M)) multiplications per coherent use, including Bennett.
  T_Φ does not depend on s.** Here A_c(M) = m_+ + 2b_M q_+.

### 2.5 Core per F_p section, combined rule W

**[conditional, Thm main + rem:combined-schedule]**

- For an explicit F_p-Lie algebra of dimension m, class ≤ c and grade dimensions g_d ≤ m:
  - Q_core(m) = c(m + t)∏_{d=2}^c M_d, where M_d ∈ {g_d+1, (g_d+1)((κ_d−1)g_d+1), B_{κ_d}(g_d)};
  - a grade with g_d = 0 is skipped;
  - t = ⌈log_p(3/ε′)⌉ for the call's error ε′.
- **[exact]** ∏_d M_d ≤ K_c (m+1)^{Σ_d e_d(p)}, with K_c = ∏_{d=2}^c d^{d(d−1)⌈log₂(d+1)⌉/2}.
  Checked for c ∈ {3, 5, 9}, every prime c < p < 6000 and two large primes, at
  g ∈ {0, 1, 19, 104}. log₂K_9 = 1202.8.
- **Original queries.** Each local query is one f query at the group element produced by the
  chart-to-group map of §2.4. So it costs T_f + T_Φ·T_mult, where T_mult is the cost of one
  call to the multiplication oracle.

### 2.6 e_p = 1 and e_p > 1

- **e_p = 1 [conditional on Thm main].** One core call on the chart, of dimension n_p:
  Q_p ≤ Q_core(n_p).
- **e_p > 1 [conditional on Thm ring-to-field (iii) with its stop rules].**
  - Run the whole-socle recursion on the chart, with Thm main as the core on each socle
    section Ω_1(S/K). Each section is an explicit F_p algebra of class ≤ c. Cor fpt-r is not
    used.
  - At call j, |K| ≥ p^j, so the socle has dimension ≤ n_p − j. The stop rules (no call on a
    trivial section; reject a non-subalgebra or one that does not strictly grow) give ≤ n_p
    calls on every branch.
  - So Q_p ≤ Σ_{j=0}^{n_p−1} Q_core(n_p − j) ≤ n_p·Q_core(n_p).
  - **[exact]** The exact sum divided by n_p·Q_core(n_p) tends to 1/(E+1): 0.0848 against
    0.0833 at c = 3, n = 400. **The exponent is E+1 either way.**
  - Each call gets error ε/(4ℓ), so t = ⌈log_p(12ℓ/ε)⌉.
  - Public HNF/SNF arithmetic for the idealizer and quotient sections costs poly(ℓ) per
    call.

### 2.7 Why not the direct free route (no chart)

**[exact]**

- On F_{s,c} itself, every lower-central dimension is Θ(s^c). So one core call costs
  Θ(s^{c·E}) queries: the measured slope is 1303.6 (S1) and 1285.6 (W) against
  c·E = 1305 and 1287 at c = 9.
- R1 for e > 1 adds e·d calls of dimension ≤ d.
- On the class-9 profile itself as a black box (p = 43, s = 2, d = rank F_{2,9} = 127, chart
  dimension 19): log₂Q is 2149.8 directly against 1572.7 on the chart under S1 (a factor
  2^577), and 757.5 against 519.0 under W.
- **Prop `prop:black-box`(ii) currently presents the direct route (e = 1) and R1 first. The
  theorem should be stated for R2.**

### 2.8 Error budget

The total ε is split into four quarters:

- **Preprocessing:** ε/4, Las Vegas with capped repetitions.
- **Small primes:** ε/4, gate synthesis only, since II is exact.
- **Charts:** ε/4, over ≤ ℓ large primes. Each prime gets ε/(8ℓ) for rank failure and
  ε/(8ℓ) for approximation.
- **Core:** ε/4, over ≤ L ≤ ℓ calls of ε/(4ℓ) each. Inside a call, the thirds of
  `sec:recursion` apply: rank, then solver (zero at Schedule-1 and linear grades), then
  approximation.

A first-error union bound in execution order covers the adaptive calls, as in II §3 and the
torsion check B3.

### 2.9 Gates and classical time [argued]

- **Quantum gates.**
  - Each lifted source or merge slot costs ≤ 4 BCH evaluations on the cover (n ≤ c·n_p):
    O(c⁴n³) field operations at Õ(log²p) gates each (Thm `thm:uniform-compilation`(i)–(ii)).
  - Each also costs ≤ max_d g_d approximate QFT_p's, at poly(log p + log(1/η)) gates, with
    log(1/η) = O(E log ℓ + log(1/ε)).
  - Slots number ≤ (c−1)·S·P per core call, so gates ≤ Q_f·O_c(n_p³ log²p + w + polylog).
    Since n_p log₂p ≤ ℓ, this is O_c(Q_f·(ℓ³ + w)·polylog).
- **Classical SDE time.**
  - Write T_d(M, a) ≤ C·M·(a+1)^{β̂}·poly(log p) for a merge at grade d.
  - β̂ = 2 for linear grades (nullspace). For Schedule-1 grades, [IS15] gives only
    "polynomial", so β̂_c is not explicit; the same holds for Schedule 2's poly(a, κ, log p, k).
  - With merges at stage d numbering S·n_d, where n_d M_d ≤ P, classical time ≤ Q_f·ℓ^{β̂_c}·poly(log p).
- **Group-oracle calls:** Q_f·T_Φ + Σ_p [(d−s)B_c(M) + 2kd(2b_M + A_c)] + preprocessing,
  where T_Φ = O_c(n_p b_M) ≤ O_c(ℓ²).

## 3. The theorem

**Theorem (all-prime black-box HSP at fixed class; conditional, AI-checked only).**

Fix c ≥ 1. Let G be a black-box group with unique ℓ-bit encodings, coherent multiplication
and its inverse, identity, and generators g_1, …, g_s, promised nilpotent of class ≤ c. Let
f be a coherent hiding function of label width w for an arbitrary H ≤ G, and let ε ∈ (0,1).

A quantum algorithm outputs generators of H with probability ≥ 1 − ε. Write
L = Σ_{p>c} n_p ≤ ℓ/log₂(c+1) and t = ⌈log₂(12ℓ/ε)⌉. Then:

1. **f queries.** Q_f ≤ Q_≤c + Q_>c, where
   - Q_>c ≤ c·K_c·(L + t)(L + 1)^{E_W(c)}, with E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143 for
     c = 2, …, 9;
   - the sharper per-Sylow form is Q_>c ≤ Σ_{p>c, e_p=1} Q_core(n_p) + Σ_{p>c, e_p>1} Σ_j Q_core(n_p − j);
   - Q_≤c is II's count for G_{≤c}, poly(log|G|) by II Thm 1, and O_c(n_p^{2+(c−1)σ_p+α_22})
     per prime as read from II's proofs.
2. **No other f queries.** Preprocessing and chart acquisition make none.
3. **Group-oracle calls.** At most Q_f·4n_p(2b_M + A_c(M)) for local queries, plus
   Σ_{p>c} [(d−s)B_c(M) + 2(⌊ℓ/log₂p⌋ + t′)·d(2b_M + A_c(M))] for charts, plus
   O(sℓ² + sℓ log(s/ε)) for preprocessing, plus II's poly(ℓ). Here d = rank F_{s,c} ≤ Σ_{k≤c} s^k.
4. **Quantum gates** (each oracle call counted once): O_c(Q_f·(ℓ³ + w)·polylog(ℓ/ε)), plus
   II's poly(ℓ), plus Õ(sℓ⁴ log(1/ε)) for order finding and factoring.
5. **Classical time:** O_c(s^c ℓ⁵ + ℓ⁶) bit operations for charts, plus poly(ℓ) per
   normalizer step, plus Q_>c·ℓ^{β̂_c}·poly(log p) for the SDE solvers.
6. **Exponents of the input size at fixed c.** With N = sℓ + w + log(1/ε):
   - f queries: O_c(N^{E_W(c)+1}). That is 144 at c = 9; 146 with Schedule 1 alone; E_W(c) on
     inputs whose large-prime Sylows all have exponent p. The query count does not depend
     on s.
   - Group-oracle calls: O_c(N^{E_W(c)+3}).
   - Quantum gates: O_c(N^{E_W(c)+4+o(1)}).
   - Total time: O_c(N^{E_W(c)+1+max(3, β̂_c)+o(1)}), with β̂_c imported from [IS15] and not
     explicit.
   - Each oracle call is unit cost; add Q_f T_f and (group calls)·T_mult.

The constants are astronomical: log₂(c K_c) = 1206 at c = 9. This is a polynomial bound at
fixed class, not a practical algorithm, and it is bounded-error, not exact.

*Proof.* §§2.1–2.9: compose the stages, using H = ∏_p(H ∩ G_p), surjectivity of Φ, Lazard
for generators (`exp` of a basis of log(H ∩ G_p), mapped to the black box by the chart words),
and a first-error union bound over the four shares. For the f-query sum, x ↦ x(x+t)(x+1)^{E−1}
is superadditive on n_p ≥ 1, so Σ_p n_p(n_p+t)(n_p+1)^{E−1} ≤ (L+t)(L+1)^E. ∎

**Not covered:** copy-only input (II Prop 3 plus `REES_COPY_ONLY_OUTER_REDUCTION.md`, not
re-checked); growing c; non-unique encodings; a synthesized circuit; an explicit β̂_c; α_22.

## 4. Exponent arithmetic against the class-9 profile (`bb_envelope_check.out`)

**A. Reproduction.**
- Core: S = 20 and ⌈log₂Q⌉ = 1573, matching the recorded `recovery_budget` convention
  t = ⌈log_p(3/ε)⌉.
- Old envelope: b = 104, b(b+1) = 10920, slack 19, ⌈log₂Q⌉ = 2194, exponent 147.
- Both agree with the repo's `black_box_large_prime_budget(104, 9)` and `sde_arity`.

**B. Worst-case exponents.** Every prime c < p < 2·10⁵ was scanned:
- E_1 = 5, 11, 23, 38, 56, 77, 109, 145;
- E_W = 5, 11, 23, 38, 56, 77, 107, 143, with c = 8, 9 attained first at p = 2521.

This matches the combined-schedule report. The leading slope of one core call between
m = 2²⁰ and 2²¹ is 145.0 (S1) and 143.0 (W) at c = 9, p = 2521.

**C. Sylow envelope.** The slope of n·Q_core(n) is 146.0 (S1) and 144.0 (W) at c = 9.

| class 9 | calls | log₂ Q (simple n·Q) | log₂ Q (exact Σ) | exponent |
|---|---|---|---|---|
| old envelope, n ≤ b = 104, cap b(b+1) | 10920 | 2194 (recorded) | — | 147 |
| new, S1, n ≤ 104, p = 43 | ≤ 104 | 2186.4 | 2180.1 | 146 |
| new, W, n ≤ 104, p = 43 | ≤ 104 | 764.6 | 759.0 | 144 |
| new, W, n ≤ 104, p = 2521 (worst p) | ≤ 104 | 2171.0 | 2164.7 | 144 |
| actual n_p ≤ ⌊104/log₂43⌋ = 19, e = 1, S1 / W | 1 | 1572.8 / 519.1 | — | 145 / 143 |
| n_p ≤ 19, e > 1 (flat worst case), S1 / W | ≤ 19 | — | 1832.8 / 602.5 | 146 / 144 |

The old envelope replaced n_p by ℓ. With n_p ≤ ℓ/log₂p, the realistic numbers are much
smaller.

**D. Free pullback vs chart:** see §2.7. Chart acquisition at p = 43 uses 19 + 3 samples,
each with one coherent Φ evaluation on F_{2,9} (d = 127), and no f queries.

**F. Constant.** log₂K_c = 2.0, 11.5, 47.5, 117.2, 233.5, 410.4, 746.4, 1202.8 for c = 2..9.

## 5. Comparison with Imran–Ivanyos's bounded-prime cost

| c | II n-exponent at p = 2 / 3 / 5 / 7 (+α_22) | Rees large-prime f-query exponent E_W+1 (E_1+1) |
|---|---|---|
| 3 | 4 / 6 / — / — | 12 (12) |
| 5 | 6 / 10 / 26 / — | 39 (39) |
| 7 | 8 / 14 / 38 / 38 (74 under the ⌈⌉ reading) | 78 (78) |
| 9 | 10 / 18 / 50 / 50 (98) | 144 (146) |

- **Small primes are cheaper.** At bounded p, II's zero-sum layer costs n^{σ_p}, with σ_p
  depending on p only. The Rees grade d costs (a+1)^{e_d}, with e_d up to d⌈log₂(d+1)⌉. For
  p ≤ c, σ_p ≤ ((c−1)/2)⌈log₂ c⌉. So unless α_22 > 94 at c = 9, the all-prime query exponent
  is set by the large primes.
- **The comparison is scope, not improvement.** If II's layer were used at the first prime
  above c, it would cost exponent (c−1)σ_p = 12, 24, 128 at c = 3, 5, 9, against
  Σ_d e_d ≤ 10, 37, 144: the same order, c² log c. II's exponent grows with p, while Rees's
  depends only on c. That is the whole point of the large-prime route: II needs bounded p,
  Rees needs p > c.
- **Remaining differences:**
  - II is exact and charges no gate error; this theorem is bounded-error.
  - II's time exponent is not explicit; neither is β̂_c here.
  - II makes ≤ n² HSMC calls per Sylow; the whole-socle recursion makes ≤ n_p core calls,
    and none at e_p = 1.

## 6. What now holds, what is missing, gates

**Exact statement now holding.** The theorem of §3. It is conditional on Thm main (steps
1–5), Schedule 2 (through rule W; with Schedule 1 alone the exponents are E_1 and E_1 + 1),
Thm ring-to-field (iii) with stop rules for e_p > 1, and the prime-power word lemma, all
AI-checked only. II, Shor, IS15 and Lazard are imported.

- The f-query exponent of the input size at fixed c is E_W(c) + 1 (144 at c = 9). It is
  explicit, checked by script, and independent of s.
- The gate exponent is E_W(c) + 4 + o(1).
- The total-time exponent is E_W(c) + 1 + max(3, β̂_c) + o(1), with β̂_c not explicit.

**Missing:**
- (1) An explicit time exponent for the IS solver (β̂_c) and for Schedule 2's poly. This is
  open item 11-01 §5.3, unchanged.
- (2) α_22 from [II22], which was not opened, so it stays UNKNOWN.
- (3) Human review of the chart structure-constant step (§2.4, argued), the sample-count
  correction to C5, and the reading of II's Props 4–5.
- (4) The copy-only variant.

**Claim gates that must stay false** (`research/reductions/rees_hsp_reduction.json`):

- **Top level:** `independent_review`, `novelty_established`, `speedup_claim_allowed`,
  `coherent_receiver_implemented`, `general_sde_implemented`, `formal_compiler_checked`.
- **`large_prime_outer_envelope`:** `outer_reduction_implemented`,
  `covers_small_prime_queries`, `covers_group_preprocessing_cost`, `is_total_gate_bound`.
  This report charges these in prose, but the JSON block still computes only the old
  b(b+1) core-query envelope, and no algorithm is executed.
- **`copy_only_outer_envelope`:** all of its false flags.

**Suggested artifact follow-up (not done; the integrator or Codex should do it).** Change
`black_box_large_prime_budget` in `theorems/rees_hsp_reduction.py` to the ≤ n call cap with
the exact sum Σ_j Q_core(n−j). Record exponent E+1 (146 for Schedule 1), and E_W + 1 = 144
under rule W, then regenerate the JSON and `numbers.tex`. Until then, the paper's \ReesOuter*
numbers describe the withdrawn envelope.

## 7. Proposed paper text

**Status label for all of it:** "conditional; AI-checked, pending human review". Only
macros already in `main.tex` are used, and no new bib entry is needed.

### 7.1 Replace `main.tex` §`sec:black-box-groups` (the paragraph "Let $G$ be a black-box nilpotent group…" through the end of Proposition `prop:black-box`, currently lines 629–640)

```latex
Let $G$ be a black-box group with unique $\ell$-bit encodings, coherent multiplication and its inverse, and generators $g_1,\dots,g_s$, promised nilpotent of class at most $c$. Let $f$ be a coherent hiding function of label width $w$ for an arbitrary $H \le G$. Write $G_p$ for the Sylow subgroups, $n_p = \log_p|G_p|$ and $p^{e_p} = \exp G_p$. Since $H = \prod_p (H\cap G_p)$ and $f$ restricted to $G_p$ hides $H \cap G_p$, the problem splits by primes. The split needs only the orders of the generators and their prime factorizations (quantum order finding and factoring, certified classically, so the step is Las Vegas); $|G|$ itself is not needed. For $p > c$, $e_p$ is the largest $p$-part of the generator orders, because groups of class below $p$ are regular. The primes $p \le c$ are covered by the exact bounded-prime algorithm of Imran and Ivanyos~\cite[Theorem~1]{ImranIvanyos2023}, with the subgroup-state unitary built from one query of $f$ and its inverse. The primes $p > c$ use the free pullback below, but only to acquire an explicit chart of $G_p$.

\begin{proposition}[Free pullback and chart acquisition; conditional]
\label{prop:black-box}
Let $p > c$, $M = p^{e_p}$, $b_M = \lceil\log_2 M\rceil$, and let $F_{s,c}$ be the free nilpotent Lie ring of class $c$ on $s$ generators over $\mathbb{Z}/M\mathbb{Z}$, of rank $d = \sum_{k=1}^c \frac{1}{k}\sum_{j \mid k}\mu(j)s^{k/j} \le \sum_{k \le c} s^k$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item By Lazard functoriality, the map $\Phi : (F_{s,c},\ast) \to G_p$ with $x_i \mapsto g_i^{(p)}$ is a surjective homomorphism, and $\Phi = \exp\circ\pi$ for a Lie ring surjection $\pi$ onto $\log G_p$. The certified inverse-BCH words of \file{research/UNIVERSAL_LAZARD_WORD_COMPILER.md} are identities over $\mathbb{Z}[1/c!]$. Evaluated with each rational power $a/b$ taken as $ab^{-1} \bmod M$, they compute the Lazard addition and bracket in every finite $p$-group of class at most $c < p$, for every $e_p$ (Trappeniers, \arxivid{2406.02475}, Theorem~2.3). After $(d-s)(m_{[\,]} + 2b_M q_{[\,]})$ group multiplications of precomputation, one evaluation of $\Phi$ costs at most $d(2b_M + A_c)$ multiplications, where $A_c = m_+ + 2b_M q_+$ and $m_+, q_+, m_{[\,]}, q_{[\,]}$ depend only on $c$. It makes no query to $f$.
  \item The map $x \mapsto \Phi(x)$ is constant exactly on the cosets of $\ker\pi$ in $(F_{s,c},+) \cong (\mathbb{Z}/M\mathbb{Z})^d$. One abelian hidden-subgroup computation on this group, with $k = \lfloor \ell/\log_2 p\rfloor + \lceil\log_p(8\ell/\eps)\rceil$ samples, each one coherent evaluation of $\Phi$, recovers $\ker\pi$ with error at most $\eps/(4\ell)$ and no query to $f$. Here $k$ bounds the number of cyclic factors of $\log G_p$; it is not bounded by $s$. Howell and Smith normal forms over $\mathbb{Z}/M\mathbb{Z}$ then give the explicit chart $F_{s,c}/\ker\pi \cong \log G_p$, with structure constants, in $O_c(s^c\ell^3 + \ell^4)$ ring operations. After precomputing the images of the chart basis, the map $x \mapsto \exp x$ from chart coordinates to black-box elements costs at most $4n_p(2b_M + A_c)$ multiplications per coherent use, independent of $s$.
  \item In general $\Phi(\Omega_1(F_{s,c})) = \mho_{e_p-1}(G_p)$, which can be a proper subgroup of $\Omega_1(G_p)$. In the metacyclic group $C_{p^2} \rtimes C_p = \langle a,b \mid a^{p^2}=b^p=1,\ bab^{-1}=a^{1+p}\rangle$, $\Omega_1(G) = \langle a^p, b\rangle$ has order $p^2$, but $\Phi(\Omega_1(F_{2,2})) = \langle a^p\rangle$. No step below restricts to $\Omega_1$ of the cover and pushes forward.
\end{enumerate}
\end{proposition}

Running Theorem~\ref{thm:main} on $F_{s,c}$ itself, with oracle $f\circ\Phi$, is also correct for $e_p = 1$, and so is the outer recursion of Theorem~\ref{thm:ring-to-field}(iii) on $F_{s,c}$ for $e_p > 1$. But every lower-central dimension of $F_{s,c}$ is $\Theta(s^c)$, so these routes cost $s^{c\cdot E}$ queries, where $E$ is the core exponent; at $c = 9$ that is $s^{1287}$ under the combined rule. The chart makes the query count independent of $s$.

\begin{theorem}[All-prime black-box HSP at fixed class; conditional]
\label{thm:black-box}
Fix $c$. Under the input model above, a quantum algorithm returns generators of $H$ with probability at least $1-\eps$. Put $L = \sum_{p>c} n_p \le \ell/\log_2(c+1)$, $t = \lceil\log_2(12\ell/\eps)\rceil$, $K_c = \prod_{d=2}^c d^{d(d-1)\lceil\log_2(d+1)\rceil/2}$, and let $E_W(c) = \max_{p>c}\bigl(1 + \sum_{d=2}^c e_d(p)\bigr)$, where $e_d(p)$ is $1$, $2$ or $\kappa_d\lceil\log_2(\kappa_d+1)\rceil$ for the linear, two-level or Ivanyos--Santha grade of Remark~\ref{rem:combined-schedule}. Then:
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item The queries to $f$ for primes $p > c$ number at most $c\,K_c\,(L+t)(L+1)^{E_W(c)}$. Sylow subgroups with $e_p = 1$ use one call of Theorem~\ref{thm:main} on the chart, of dimension $n_p$. Those with $e_p > 1$ use the recursion of Theorem~\ref{thm:ring-to-field}(iii) on the chart, with Theorem~\ref{thm:main} on each socle section and at most $n_p$ calls. The primes $p \le c$ add the queries of~\cite[Theorem~1]{ImranIvanyos2023}, $\poly(\log|G|)$. No other step queries $f$.
  \item Each local query also costs at most $4n_p(2b_M + A_c)$ group multiplications. Chart acquisition costs $(d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 2k\,d\,(2b_M + A_c)$ multiplications per prime $p > c$. Preprocessing costs $O(s\ell^2 + s\ell\log(s/\eps))$ multiplications.
  \item Quantum gates number $O_c\bigl(Q_f(\ell^3 + w)\,\poly\log(\ell/\eps)\bigr)$, plus the gates of~\cite{ImranIvanyos2023} and of order finding and factoring, with each oracle call counted once. Classical time is $O_c(s^c\ell^5 + \ell^6)$ bit operations for the charts, polynomial normal-form arithmetic per normalizer step, and at most $Q_f\cdot\ell^{\hat\beta_c}\poly(\log p)$ for the diagonal-equation solvers. Here $\hat\beta_c$ is the excess time exponent of the solver of~\cite{IvanyosSantha2015} over its arity, which that paper states only as polynomial.
  \item The error is split into four quarters: preprocessing, the primes $p\le c$ (gate synthesis only), chart acquisition, and the at most $\ell$ core calls, each core call receiving $\eps/(4\ell)$.
\end{enumerate}
For fixed $c$ and input size $N = s\ell + w + \log(1/\eps)$, the number of queries to $f$ is $O_c(N^{E_W(c)+1})$, and it does not depend on $s$. The number of gates is $O_c(N^{E_W(c)+4+o(1)})$, and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$. Here $E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143$ for $c = 2,\dots,9$; with Schedule~1 alone, $E_W$ is replaced by $1 + \sum_{d=2}^c d\lceil\log_2(d+1)\rceil$, which is $145$ at $c=9$. If every Sylow subgroup for $p > c$ has exponent $p$, the query exponent is $E_W(c)$. The result is conditional on Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule, and, for $e_p > 1$, on Theorem~\ref{thm:ring-to-field}(iii) with its stop rules. Its proof has been checked by AI sessions only. It is bounded-error, not exact, and its constants are astronomical ($\log_2(9K_9) \approx 1206$).
\end{theorem}

\begin{proof}[Proof sketch]
The Sylow split, the composition with~\cite{ImranIvanyos2023} and the pullback are as above. Within the chart, Lazard's correspondence turns a basis of $\log(H\cap G_p)$ into generators, and the chart-to-group words map them into the black box. For $e_p > 1$, call $j$ of the recursion acts on a section $S/K$ with $|K| \ge p^j$, so its socle has dimension at most $n_p - j$; the stop rules give at most $n_p$ calls on every branch. Each core call of dimension $m$ makes at most $c(m+t)\prod_{d=2}^c M_d \le c\,K_c\,(m+t)(m+1)^{E_W(c)-1}$ queries. The function $x \mapsto x(x+t)(x+1)^{E-1}$ is superadditive, which gives~(i). Gates are dominated by the at most $4$ BCH evaluations per merge slot, each $O(c^4 n^3)$ field operations on a cover of dimension $n \le c\,n_p$, with $n_p\log_2 p \le \ell$. A first-error union bound over the four shares controls the error. The full accounting and an exact check of the exponents are in \file{research/audits/reviews/2026-11-02-rees-bb-envelope.md}.
\end{proof}

\begin{remark}[Comparison with the bounded-prime algorithm]
For a $p$-group of order $p^n$ and class $c$, the proofs of~\cite[Propositions~1,~2,~4,~5]{ImranIvanyos2023} give at most $n^2$ calls of the hidden-subgroup-membership routine, each converting $\prod_{i=2}^c S(p,n_i)$ copies, where $S(p,n) = O_p\bigl(n^{\sigma_p}\bigr)$ with $\sigma_p = 2^{\lfloor\log_2((p-1)/2)\rfloor}\lceil\log_2 p\rceil$ for odd $p$ and $\sigma_2 = 1$. At $c = 9$ the resulting query exponents in $n$ are $10, 18, 50, 50$ for $p = 2,3,5,7$, plus the exponent of their exact abelian subroutine, against $E_W(9)+1 = 144$ for $p > c$. So the large primes determine the exponent of Theorem~\ref{thm:black-box}. The zero-sum exponent $\sigma_p$ grows with $p$, whereas $E_W(c)$ does not depend on $p$.
\end{remark}
```

Consistency notes for the integrator:

- The existing Prop (i) sentence about the implemented compiler (`theorems/universal_lazard_words.py`
  "still works modulo p") is out of date. The prime-power report §6 records that the
  evaluator now takes `modulus=p^e`, so that sentence should be dropped or updated.
- Appendix item 17 (`appendix-torsion-blackbox.tex`) proves the pieces. This text only
  needs to cite it, if it exists.

### 7.2 Replace the envelope sentences at `main.tex:554`

Replace the text from "The separate conditional black-box outer envelope is for groups with…"
through "…Small-prime calls and preprocessing are not counted." with:

```latex
For black-box input, Theorem~\ref{thm:black-box} gives the total bound. Its query exponent in the input size is $E_W(c)+1$, which is $144$ at $c = 9$ ($146$ with Schedule~1 alone). It charges every query, gate and error term of the Sylow split, the bounded-prime algorithm of~\cite{ImranIvanyos2023}, the free pullback and chart acquisition, and the core calls. The envelope recorded in \file{rees_hsp_reduction.json}, with $b = \ReesOuterEncBits$-bit encodings, call cap $b(b+1) = \ReesOuterCallCap$ and exponent $\ReesOuterQueryExp$, is superseded. It counts only large-prime core queries on an acquired chart, and it uses a chain-pass scan of up to $b(b+1)$ calls where the whole-socle recursion of Theorem~\ref{thm:ring-to-field}(iii) needs at most $n_p \le b$. On the class-$\ReesClassNineClass$ profile with $b = 104$ and Schedule~1, the new count is about $2^{2186}$ against $2^{\ReesOuterOrigQueriesBits}$. With the true composition length $n_p \le \lfloor 104/\log_2 43\rfloor = 19$ it is about $2^{1833}$, and under the combined rule $2^{603}$. Three call counts appear in this paper, for three recursions: at most $b$ for the whole-socle recursion of Theorem~\ref{thm:ring-to-field}(iii); $b(b+1)/2$ for the central-flag scan of the ring-to-field note (Section~\ref{sec:ring}); and $b(b+1)$ for the superseded chain-pass envelope.
```

The \ReesOuter* macros stay valid until `make_numbers.py` is updated. The numbers 2186, 1833
and 603 are in `bb_envelope_check.out`, section C: the simple n·Q bound at p = 43, S1, n ≤ 104
(2186.4), and the exact sum at n_p ≤ 19 under S1 (1832.8) and W (602.5).

### 7.3 Optional table row (`tab:main-regimes`)

```latex
Black-box, unique encoding (Thm.~\ref{thm:black-box}) & all primes ($p \le c$ via~\cite[Thm.~1]{ImranIvanyos2023}) & combined rule on an acquired chart; $\le n_p$ socle rounds if $e_p > 1$ & $O_c(N^{E_W(c)+1})$ queries, $O_c(N^{E_W(c)+4+o(1)})$ gates \\
```

## Next

- **Hard question:** an explicit time exponent β̂_c for the IS solver, which is the only
  non-explicit exponent left in the total time. Separately, whether Σ_j over the socle calls
  is really Θ(n·Q_core(n)) in the worst case, or whether a better potential argument gives
  exponent E for e > 1.
- **Next command:** update `black_box_large_prime_budget` as in §6 and re-run
  `python -m theorems.rees_hsp_reduction`.
- **Acceptance test:** the JSON records call cap n, exponent 146 (S1), and log₂ of the exact
  sum equal to 2180.1 at b = 104; this report's script still passes.
