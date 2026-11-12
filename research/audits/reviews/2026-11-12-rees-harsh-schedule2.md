# 2026-11-12 Harsh referee: Schedule 2, the triangular variant, E_2(κ) and the conditional exponents of the core Outlook

**AI-run referee (one Claude session), pending human review.** Target: core
`docs/papers/rees-hsp/core/main-core.tex` l. 909, paragraph "Smaller arities" (Section
"Outlook: Conditional Extensions"). Proofs read in `appendix-schedule2.tex` (ll. 7–400) and
`main.tex` (thm:power-sde l. 754, prop:decoupled-sde l. 771, prop:triangular-sde ll. 783–800,
rem:combined-schedule l. 811). I edited no paper, STATE, handoff or reductions file; no Git, no
network, no API calls. Every computation ran under `nice -n 19`, one heavy process at a time, each
well under 2 h and 1.5 GB (largest RSS about 120 MB).

Scripts and outputs: `research/audits/reviews/2026-11-12-rees-harsh-schedule2/` (file list in
section 7). All my search code was written before I opened any repo E_2 script or table; repo
data were read only afterwards, for comparison and for witness checking with my own checker.

## 0. Verdict

**The two proofs are correct as far as an AI referee can tell; every finite input of the 2c−1
claims is confirmed; the "37" sentence is wrong as worded.**

- Schedule 2 (thm:app-s2-main) and the triangular solver (prop:triangular-sde) are **CORRECT**.
  I re-derived each lemma and found no gap. Neither proof uses any law on the columns. Both
  return the scalars and meet the four properties of rem:main-solver, with Las Vegas
  allowed by rem:is-import(d).
- T_A(κ) (prop:app-s2-TA) is **CORRECT**. Its closed form, recomputed with my own code,
  gives the table values: T_A(8) = 117441562.03 and T_A(9) = 3099365718.7 < 3.10·10⁹.
- The E_2 sets the claims use:
  - E_2(2), …, E_2(6): **recomputed independently and completely**.
  - E_2(7): **recomputed independently and completely**: 56 primes, the largest 3221, and
    empty on (3221, ⌈T_A(7)⌉].
  - E_2(8): membership is recomputed only up to 4400. Non-membership on (14281, T_A(8)] is
    **confirmed**: every one of the 1,675,111 primes p ≡ 1 mod 8 there has a stored
    witness, and my own checker accepts each one.
  - E_2(9): membership is recomputed only up to 6000. In (6000, 9⁹/2], the primes without a
    verified witness are exactly the repo's members and undecided primes.
- The two known corrections hold:
  - 2521 ∈ E_2(8) and 2521 ∈ E_2(9), by my own exhaustive search.
  - "342 rather than 414" is right as a count of primes ≤ 20000: 342 = 123 (mine, ≤ 6000)
    + 219 (repo, unverified). 414 is the count ≤ 25000 (342 + 72).
- Exponents recomputed from the definitions:
  - 2c−1 above T_A(c) (3.10·10⁹ at c = 9): **CORRECT**.
  - 2c−1 at p > 14281 for c ≤ 8: **CORRECT**. For κ ≤ 7 this rests on my own searches; for
    κ = 8 it rests on stored repo witnesses that my checker accepts.
  - 143 at p = 2521 for the Schedule 1 / Schedule 2 rule: **CORRECT**.
  - **"37" is REFUTED as worded.** "Taking the best of these solvers" (the paragraph names
    Schedule 1, Schedule 2 and the triangular variant) gives **99**, attained at p = 1009.
    Adding the core's own "Shorter zero sums" fallback gives **40**, at p = 73. The value 37
    needs the full version's coset-refinement towers and union chains. The core never names
    them, and I did not check them.

**Can the conditional label be lifted to "AI-checked, refereed by AI"?** Partly. It can be
lifted for:
- the Schedule 2 arity at p ≥ 16κ^{2κ+2};
- the triangular arity outside E_2(κ);
- 2c−1 above T_A(c);
- 143 at p = 2521.

It can also be lifted for 2c−1 at p > 14281 (c ≤ 8). There the finite input is fully checked:
for κ ≤ 7 by my own searches, and for κ = 8 by my own checker on the repo's stored witnesses,
which are not my own searches. It cannot be lifted for the 37 sentence until that sentence is reworded (section 5).
In every case a human still has to read the proofs. Nothing here promotes a theorem; the
finite checks can only falsify.

## 1. Table

| item (locator) | claim | my verdict | basis |
|---|---|---|---|
| lem:app-s2-gcd (app-s2 l.25) | reduction to exponent κ, Bezout t, κ = 1 linear | CORRECT | re-derived |
| lem:app-s2-tensor (l.52) | M = (a+1)((κ−1)a+1) columns give cells S_ij, values in W⊗W, S_00 ≠ ∅ | CORRECT | re-derived, every column tuple (repeats, zeros allowed) |
| lem:app-s2-witness, -normal (l.88, 97) | contraction ⇒ witness; annihilator = {z_iz_j(α_j+β_i)} | CORRECT | re-derived, dimension count 2κ−1 checked |
| lem:app-s2-weil-count (l.123) | count of prescribed cosets, error E_κ(ℓ,p) | CORRECT (Weil statement = L–N Thm 5.41 form; locator still needs a human) | re-derived incl. closed form |
| lem:app-s2-stage + thm:app-s2-main (l.155–190) | Phase 0 succeeds for p ≥ 4κ^{2κ+2}; abort < 2^{-k}; never wrong; cost (1+κ^κ)poly | CORRECT | re-derived |
| prop:triangular-sde (main l.783–800) | (a+1)(a+2)/2 arbitrary columns, p ∉ E_2(κ) | CORRECT | re-derived rounds and back substitution |
| prop:app-s2-TA (l.244–345) | R ≤ U_κ(p); p > T_A(κ) ⇒ p ∉ E_2(κ) | CORRECT | re-derived; T_A recomputed (thresholds.out) |
| threshold 16κ^{2κ+2} | Schedule 2 hypothesis | CORRECT (4κ^{2κ+2} suffices) | stage lemma |
| T_A(9) < 3.10·10⁹ | threshold at c = 9 | CORRECT: 3099365718.7 | thresholds.out |
| E_2(2..6) | ∅, ∅, {5,…,53}, 9 primes ≤181, 53 primes ≤859 | CONFIRMED independently (complete) | exhaustive ≤3000 + verified certificates to T_A |
| E_2(7) | 56 primes, max 3221 | CONFIRMED independently (complete to ⌈T_A(7)⌉) | exhaustive ≤6000, hunt + resolve to 10⁶, scan to T_A(7) |
| E_2(8) | 293 primes ≤ 20000, max 14281, empty above | members CONFIRMED only ≤4400 (138, equal to repo); empty on (14281, T_A(8)] CONFIRMED by my checker on stored witnesses | ex_k8, wcheck_k8_repo.out |
| E_2(9) | 342 ≤ 20000, 414 ≤ 25000, undecided band | members CONFIRMED only ≤6000 (123, equal to repo); witness coverage of (6000, 9⁹/2] equals repo's member + undecided lists exactly | ex_k9, wcheck_k9_repo.out |
| 2521 ∈ E_2(8), E_2(9) | referee correction | CONFIRMED | own exhaustive |
| exponent 2c−1 for p > T_A(c) | Outlook | CORRECT (CONDITIONAL on review) | arithmetic + T_A |
| 2c−1 for p > 14281, c ≤ 8 | Outlook | CORRECT (CONDITIONAL on review) | E_2 checks above; exponents_2cminus1_check.out |
| 143 at c = 9 (p = 2521) | Outlook | CORRECT for the Schedule 1/2 rule only | exponents_own |
| 37 at c = 9 "taking the best of these solvers" | Outlook | REFUTED as worded: 99 (named solvers), 40 (+ zero-sum depth); 37 needs full-version towers/chains, NOT checked | exponents_own |

## 2. Proof review (obligation 1)

### 2.1 Schedule 2 (thm:app-s2-main), lemma by lemma

- **gcd reduction.** The image of x ↦ x^d is Q_0: same order h, and contained in Q_0 because κ | d.
  With d = κd′ and p−1 = κq′, choose t with td′ ≡ 1 (mod q′). Then u^{tκd′} = u^κ for u ≠ 0,
  because tκd′ ≡ κ (mod p−1). Supports are preserved. CORRECT.
- **Two-level tensor; totality for every label tuple.**
  - *Level one.* Each block of a+1 columns has a nonzero dependence c, normalised so that
    c_{b*} = 1. Write c_b = z_{ind(c_b)}ω_b^κ; the κ-th root exists because
    c_b/z_{ind} ∈ Q_0. Then Σ_i z_iT_i^ν = Σ_b c_bλ_b = 0, and b* ∈ S_0^ν.
  - *Level two.* There are N = (κ−1)a+1 vectors (T_1^ν,…,T_{κ−1}^ν) in dimension (κ−1)a,
    so they have a nonzero dependence η. The i = 0 relation follows by linearity from
    T_0 = −Σ_{i≠0}z_iT_i (z_0 = 1).
  - Both contractions of (T_ij) vanish, and S_00 ∋ b* of block ν*. Nothing assumes the
    columns are distinct, nonzero or independent. CORRECT.
- **Normal form and witness.**
  - W⊗W = {X : Xz = 0, Xᵀz = 0} has dimension (κ−1)², so its annihilator has dimension
    2κ−1.
  - The map (α,β) ↦ z_iz_j(α_j+β_i) has kernel {(c𝟏,−c𝟏)}, so its image has dimension 2κ−1
    and is the whole annihilator.
  - The witness is u_b = θ_ijω′_b with θ_ij^κ = C_ij ∈ Q_0°, and Σu_b^κλ_b = Σ C_ijT_ij = 0.
    It is nonzero on S_00 because C_00 ≠ 0. CORRECT.
- **Weil count.**
  - The indicator expansion is right.
  - f_e = Π_{k∈S}(X−r_k)^{e_k} with 1 ≤ e_k ≤ κ−1 is not a κ-th power, so the
    Lidl–Niederreiter bound (s−1)√p applies.
  - The points r_k with k ∉ S contribute at most 1 each.
  - The closed form, and the bound E ≤ (ℓ−1)√p+1 for ℓ ≤ κ, are right. CORRECT.
- **Stage lemma.** The roots 0, −t_0, …, −t_{j−1} are distinct, because the accepted t_i are
  nonzero and distinct (2z_j²t ∈ Q_0 forces t ≠ 0, and t_0 = 1/2). Each inequality step
  checks: ℓ/κ^ℓ ≤ 1, √p ≥ 2κ^{κ+1} ≥ ℓ+1, and ℓκ^ℓ ≤ κ^{κ+1}. Only p ≥ 4κ^{2κ+2} is used
  (rem:app-s2-four is right). CORRECT.
- **Scalars returned.** s_b = u_b^t, with u_b a product of explicit field elements and
  Las Vegas κ-th roots. CORRECT.
- **Las Vegas / determinism.**
  - The output is checked before release and is never wrong.
  - The abort probability is at most (1−1/κ)^{κ(k+3)} + κ2^{−τ} + 2^{−k−1} < 2^{−k}. The
    coset-generator probability φ(κ)/κ ≥ 1/κ, and each stage succeeds with probability at
    least 1/(2κ^{j+1}) given any prefix.
  - The running time is worst-case bounded: Phase 1 is cut off at 2T_1 and repeated k+1
    times.
  - So with k = 2 it meets rem:is-import(d): failure ≤ 1/4 and an explicit time bound.
  - CORRECT.
- **Running time.** (1+κ^κ)·poly(a,κ,log p,k). For fixed c this is polynomial. CORRECT.
- **Publicity of the arity.** M = (g+1)((κ−1)g+1) and the test p ≥ 16κ^{2κ+2} depend only on
  (p,d,g_d). CORRECT.

### 2.2 Triangular solver (prop:triangular-sde)

- **Realisation.** For cos(ζ) = n, x_i = ζδ_i(α_n+β_{cos δ_i}) lies in P∪{0}, because
  α_n+β_{cos δ_i} ∈ g^{−(n+cos δ_i)}P∪{0} and ζδ_i ∈ g^{n+cos δ_i}P. Its value is
  ζα_n e + ζv. CORRECT.
- **Rounds.**
  - In round k, a−dim U_k+1 columns have a dependence modulo U_k.
  - Scaling one entry of δ to 1 makes R nonzero: the weight there is α_0+β_0 = 1.
  - If v ∉ U_k, the dimension grows by one. So dim U_k = k, and the count is
    Σ_{k=0}^{a}(a−k+1) = (a+1)(a+2)/2.
  - Round a has U_a = F^a and a single column, so it always stops.
  - Totality holds for every tuple: repeated and zero columns are handled, since only
    dependences modulo U_k are used. CORRECT.
- **Back substitution.**
  - Each step keeps τ ∈ U_{l−1}, because e_l ∈ U_{l−1}.
  - The added weights' values cancel −ρ, and the supports are disjoint.
  - The result is a nonzero x ∈ (P∪{0})^M with Σx_iλ_i = 0. CORRECT.
- **Scalars and determinism.**
  - κ-th roots and the Bezout exponent give s. The run is deterministic given g, (α,β) and
    the roots.
  - Side remark (not an error): given a coset generator g, which is a non-q-th power for every
    prime q | κ, Adleman–Manders–Miller extracts κ-th roots deterministically in
    poly(κ, log p). So the root step could be deterministic too.
  - Finding (α,β):
    - above T_S(κ), Las Vegas (prop:app-s2-TA(iii));
    - otherwise, exhaustive search, which is O_κ(1) but of order p^{2κ−2} (at κ = 9 up to
      T_S ≈ 2.8·10¹⁰); "polynomial" holds only formally. The earlier referee already says so.
  - CORRECT.
- **Publicity of the arity.**
  - The arity is public whenever membership of p in E_2(κ) is known from (p, κ).
  - For κ = 9 on the undecided band, the rule must fall back to Schedule 1 (or to an
    exhaustive search). It stays a function of public data, but the authors cannot currently
    evaluate it there. This does not affect any Outlook claim, because the c = 9 claim is
    stated above T_A(9).

### 2.3 Thresholds

- **T_A (prop:app-s2-TA).** I re-derived each step:
  - the exact moments, including the reindexing m − c′ = −(i+c), which misses only −c;
  - the cyclotomic expansions: the K(s,0), K(0,t) and K(s,−s) values, the (κ−1)(κ−2) Weil
    pairs, and the constant |2 − κ[b=0] − κ[b=ε]| ≤ 2(κ−1);
  - the factor L = ((p−κ−1)/(p−1))^κ(p/(p−1))^{κ−1} ≤ 1;
  - the inequality log(1+x) ≤ x − x²/2 + x³/3 for x > −1 (the fourth derivative is
    negative);
  - the identity (1+δ′)/(1+δ) = 1 + (δ′−δ) + (δ²−δ′δ)/(1+δ), and Cauchy–Schwarz;
  - the second-moment step Pr[n_j = 0] ≤ 1 − 1/R, and the union bound;
  - monotonicity: Δ decreases, u_Δ decreases in Δ and v_Δ increases, so E_max is
    nondecreasing in Δ.

  CORRECT. `thresholds.py` (mpmath, 50 digits) reproduces every entry of
  tab:app-s2-thresholds and the three margins at κ = 3, 4, 5 (0.0158, 0.0540, 0.0476). A grid
  check of monotonicity on (κ+2, 10¹²) found no violation.
- **16κ^{2κ+2}.** Valid; the proof needs only 4κ^{2κ+2}. Since 16κ^{2κ+2} > T_A(κ) for every
  κ ≥ 2, p ≥ 16κ^{2κ+2} implies p ∉ E_2(κ), as rem:triangular-scope says.
- **T_A(c) for "2c−1 above an explicit threshold".**
  - T_A(κ) increases with κ for every κ ≥ 2, so max_{κ≤c} T_A(κ) = T_A(c) for every c.
    For c ≥ 4 this follows from prop:app-s2-TA(ii):
    T_A(c) > (c−1)c^c > (c−1)^c ≥ T_A(c−1). The small cases are numerical: T_A(2) = 8.4,
    T_A(3) = 79, T_A(4) = 869.
  - At c = 9 the value is 3.0994·10⁹ < 3.10·10⁹. CORRECT.
- **14281.**
  - The c ≤ 8 claim needs only E_2(κ) ∩ (14281, T_A(κ)] = ∅ for κ ≤ 8. It does not need
    14281 ∈ E_2(8). That membership I could not recompute (about 10¹⁰ search nodes; NOT
    computed).
  - Status of the band for each κ is in section 3.

## 3. E_2(κ) recomputed (obligation 2)

### 3.1 Method (own code)

**Reformulation.** Put x_j = α_j and y_i = −β_i. A two-level contraction exists if and only if
some (x,y) ∈ F_p^{2κ}, not all 2κ values equal, satisfies x_j − y_i ∈ Q°_{−(i+j)} for all i, j.

Why "not all equal" suffices:
- If the entry (r,s) is nonzero, move it to (0,0): set x′_j = λx_{j+r} and y′_i = λy_{i+s},
  with λ ∈ Q_{r+s}.
- Then translate and scale by an element of Q_0, so that x_0 = 1 and y_0 = 0.

**Search.**
- `e2dfs.c` is a complete depth-first search over the 2κ−2 free values. It uses bitset
  domains, forward checking and smallest-domain-first branching. It has no symmetry breaking
  and no other prunes.
- It prints MEMBER, or a certificate (x,y).
- `verify_cert.py` re-checks every certificate from the definition, using pow() and no
  tables. It checks every coset condition, C_00 ≠ 0, that every entry is a κ-th power or 0,
  and that C kills a basis of W⊗W.
- `wcheck.c` is a second checker in C. It reads the repo's stored witnesses (format
  k, p, g, β, α) and my own certificates, and checks the definition with the witness's
  coset generator g, including that g^h has exact order κ. It then reports which primes of a
  range lack a verified witness.
- `e2scan.c` is the sampler of prop:app-s2-TA(iii): draw a random y, then scan F_p.

**Results** (all certificates verified, 0 bad):

| κ | exhaustive range (own) | members found | certificates beyond | status |
|---|---|---|---|---|
| 2, 3 | p ≤ 3000 | 0 | T_A(2) = 8.4, T_A(3) = 79 | E_2 = ∅ CONFIRMED |
| 4 | p ≤ 3000 | {5,13,17,29,37,53} | T_A(4) = 869 | CONFIRMED |
| 5 | p ≤ 3000 | {11,31,41,61,71,101,131,151,181} | all 278 primes in (3000,13000] ⊃ (3000,T_A(5)] | CONFIRMED |
| 6 | p ≤ 3000 | 53 primes, max 859 (= repo xval_k6 set) | all 10147 primes in (3000,234000] ⊃ (3000,T_A(6)] | CONFIRMED |
| 7 | p ≤ 6000 | 56 primes, max 3221 (= repo E2_k7.txt) | (6000,10⁶]: all 12937 primes certified (hunt + resolve); (10⁶, ⌈T_A(7)⌉]: all 44335 primes certified by e2scan | CONFIRMED |
| 8 | p ≤ 4400 | 138 (= repo json, no disagreement); 2521 member | (14281, T_A(8)]: 1,675,111 of 1,675,111 primes have a verified stored witness | members in (4400, 14281] NOT computed |
| 9 | p ≤ 6000 | 123 (= repo json, no disagreement); 2521 member | (6000, 9⁹/2]: 1,789,776 of 1,791,362 verified; the 1586 without are exactly repo members (219 in (6000,20000], 72 in (20000,25000]) and the 1295 undecided | membership above 6000 NOT computed |

- Also reproduced: "82 of the 83 primes below 2442 (κ = 8) and below 3584 (κ = 9) are
  exceptional".
- The κ = 8 witnesses in (4400, 20000] are consistent with the repo: the primes lacking a
  verified witness are exactly the 155 json members, the largest 14281.
- Not computed:
  - membership of the 155 primes in (4400, 14281] for κ = 8, of the 291 primes in
    (6000, 25000] for κ = 9, and of every prime in the undecided κ = 9 band;
  - in particular, 14281 ∈ E_2(8) and the counts 293, 342 and 414 beyond my exhaustive
    ranges.

  Each would need about 10¹⁰ or more search nodes per prime with my code.
- The κ = 8 and κ = 9 certificate hunts with a node limit were stopped early. Stored repo
  witnesses checked by `wcheck` made them redundant.

### 3.2 κ = 7 above 6000

- **(6000, 10⁶].** The node-limited DFS hunt (limit 2·10⁴) certified 12927 of the 12937
  primes. The 10 primes it left undecided (6007, 6091, 6217, 7253, 7477, 7673, 7687, 8527,
  8807 and 10039) were then decided by the complete search (`resolve_k7.out`), all as
  NONMEMBER. `wcheck 7 6000 1000000`: 12937 of 12937 covered, 0 bad. So
  E_2(7) ∩ (6000, 10⁶] = ∅ is **independently confirmed**.
- **(10⁶, ⌈T_A(7)⌉].** The repo's "exact search below 5·10⁶" (2026-11-02-rees-threshold-2,
  `k7_*.out`) stored only counts, not witnesses, so there was nothing to re-check. Instead
  I ran the second-moment sampler `e2scan` over the band:
  - draw a random y, scan F_p, up to 400 draws per prime;
  - check every witness with `wcheck`.
  
  Result (`scan_k7_1e6_TA7.out`, `wcheck_k7_scan.out`): every one of the 44335 primes
  p ≡ 1 mod 7 in (10⁶, 4941831] got a witness. `wcheck` accepted all of them; 0 bad, 0 missing.
  So E_2(7) ∩ (6000, ⌈T_A(7)⌉] = ∅ is **independently confirmed**, and with the exhaustive
  range E_2(7) is the 56-prime set of the paper.

  A 60-prime random sample of the band (`sample_k7.*`, DFS) also gave 60 of 60 verified
  certificates. Other samples:
  - κ = 8 on (10⁵, 1.2·10⁷]: 60 of 60 verified.
  - κ = 9 on (10⁵, 5·10⁶]: 37 of 60 certified by DFS with a 2·10⁴-node limit. The other 23
    all have stored repo witnesses that my checker accepts; none is in the repo's undecided
    list.

## 4. Exponents (obligation 3)

**Definition used.** The exponent is
E(c,p) = 1 + Σ_{d=2}^c e_d, where e_d is the degree in g_d of the arity chosen at grade d and
κ = gcd(d, p−1). The leading 1 comes from c(m+τ). The per-grade options are:

| option | available | degree e_d |
|---|---|---|
| linear | κ = 1 | 1 |
| Schedule 1 | always | κ⌈log₂(κ+1)⌉ (B_κ) |
| Schedule 1 at zero-sum depth | always | κ⌈log₂ t⌉, where t = least length of a zero sum of nonzero κ-th powers |
| Schedule 2 | p ≥ 16κ^{2κ+2} | 2 |
| triangular | p ∉ E_2(κ) | 2 |

How t is computed:
- t = 2 iff (p−1)/κ is even.
- Otherwise t = 3 once p+1−(κ−1)(κ−2)√p > 3κ (Weil bound on the Fermat curve).
- Otherwise t comes from a breadth-first search.

**Results** (`exponents_own.py`, every prime ≤ 10⁶; worst case over p > c, c = 2..9). Unknown
E_2 membership is evaluated both ways (unknown = member / unknown = non-member). Both give
identical rows.

| rule | c = 2..9 | c = 9 attained at |
|---|---|---|
| Schedule 1 only, published depth, per grade (PAPER = rem:combined-schedule) | 5, 11, 23, 38, 56, 77, 107, 143 | p = 2521 |
| + zero-sum depth (core "Shorter zero sums") | 5, 8, 16, 19, 35, 36, 44, 53 | p = 2521 |
| Schedule 1 + Schedule 2 + triangular (the solvers "Smaller arities" names) | 3, 5, 17, 22, 40, 48, 79, **99** | p = 1009 |
| the same + zero-sum-depth fallback | 3, 5, 16, 14, 30, 31, 38, **40** | p = 73 |

These match the repo's own rows PAPER (143), E_S1t (53), R2 (99) and R3 (40) in
`2026-11-12-rees-exponent-discharge.md`. Those rows were computed independently of mine.

- **143 at p = 2521.** At p = 2521, p−1 = 2520 and κ_d = d for all d ≤ 9. Only κ = 2 satisfies
  16κ^{2κ+2} = 1024 ≤ 2521. So e = [2, 6, 12, 15, 18, 21, 32, 36] and E = 143.
  - No prime gives more. 145 would need Schedule 1 at grade 2, and with κ_d = d for all d,
    that is p ≡ 1 (mod 2520), so p ≥ 2521 > 1024.
  - CORRECT, for the Schedule 1/2 rule.
  - With the triangular variant, p = 2521 gives 81: e = [2, 2, 2, 2, 2, 2, 32, 36], because
    2521 ∈ E_2(8) ∩ E_2(9) and 2521 ∉ E_2(κ) for κ ≤ 7. That is not 17.
- **99 at p = 1009.** Here p−1 = 1008 = 2⁴·3²·7, so κ = (2,3,4,1,6,7,8,9) for d = 2..9.
  - 1009 lies in E_2(7), E_2(8) and E_2(9); all three are my own exhaustive verdicts.
  - So e = [2, 2, 2, 1, 2, 21, 32, 36] and E = 99.
  - Above 10⁶ nothing exceeds this. Grades with κ ≤ 6 are quadratic, and the κ = 8 grade is
    quadratic above 14281. For κ = 9 the only undecided primes above 424549 lie in
    (9⁹/2, T_A(9)], where κ = 7 is above T_A(7). So the tail is at most
    max(1 + 2·7 + 36, 1 + 2·7 + 21) = 51, even if every κ = 7 prime in (10⁶, T_A(7)] counted
    as a member.
  - So 99 is the worst case over all p > 9. That claim is CONDITIONAL on the E_2 inputs of
    section 3.
- **40 at p = 73.** Here κ = (2,3,4,1,6,1,8,9).
  - 73 lies in E_2(6), E_2(8) and E_2(9); all are my own verdicts.
  - t(73,8) = 3, so e = [2, 2, 2, 1, 6, 1, 16, 9] and E = 40.
  - In the tail (p > 10⁶, unknown = member) E ≤ 1 + 2·6 + 7 + 9 = 29.
- **p = 41.** Here κ_8 = 8, the 8th powers are μ_5 and t(41,8) = 5.
  - With the zero-sum-depth fallback, 41 gives 39: e = [2,1,2,5,2,1,24,1], since 41 ∈ E_2(5)
    and 41 ∈ E_2(8).
  - The repo's 37 at p = 41 additionally lowers the κ = 5 grade from 5 to 3 by a union chain
    (app:s2-chains). That construction is not in the core, and I did not check it (NOT
    checked).
- **2c−1.**
  - Above max_{κ≤c} T_A(κ) = T_A(c), every grade with κ ≥ 2 has arity (g+1)(g+2)/2, and
    grades with κ = 1 have g+1. So E ≤ 1 + 2(c−1) = 2c−1.
  - Equality holds at the infinitely many primes p ≡ 1 (mod lcm(2..c)). At c = 9 this is 17.
  - Sharper at c = 9 (verified witnesses): 2c−1 = 17 already holds at every prime p > 424549,
    except primes p ≡ 1 (mod 9) in (9⁹/2, T_A(9)] = (1.94·10⁸, 3.10·10⁹], which are undecided.
- **Block-steered variant.** Excluded from every row. Its prime range grows with g_d², so at a
  fixed p it fails for large m, and it needs the label law.

**Conclusion of obligation 3.**
- 2c−1 (above T_A(c); above 14281 for c ≤ 8) and 143 are right.
- "taking the best of these solvers at each grade, the largest exponent at c = 9 over all
  primes p > 9 is 37" is **not** right for the solvers the core names. It is 99, or 40 with
  the zero-sum depth of the next paragraph. 37 is a figure for a larger toolbox (towers,
  union chains and the κ = 7 three-step chain of the full version). The core does not
  mention that toolbox, and its correctness is not checked here.

## 5. Replacement text (for the integrator; I did not edit the paper)

Replace, in core l. 909, from "with these thresholds as stated, a per-grade choice of solver"
to "(finite computation over the exceptional primes)." by:

> with these thresholds as stated, choosing between Schedule~1 and Schedule~2 at each grade
> lowers the exponent of $m$ at $c = 9$ only from $\ReesClassNineQueryExp$ to $143$, because at
> primes such as $p = 2521$ every $\kappa_d$ equals $d$ and only the grade with $\kappa_d = 2$
> meets the Schedule~2 threshold. With the triangular variant the exponent of $m$ would be
> $2c-1$ at every prime $p > T_A(c)$, an explicit threshold ($3.10\cdot 10^9$ at $c = 9$), and at
> every prime $p > 14281$ when $c \le 8$. Taking the best of Schedule~1, Schedule~2 and the
> triangular variant at each grade, the largest exponent at $c = 9$ over all primes $p > 9$ is
> $99$, at $p = 1009$, which lies in the exceptional sets for $\kappa = 7, 8, 9$; with
> Schedule~1 charged at the zero-sum depth of the next paragraph it is $40$, at $p = 73$, and
> further constructions of the full version (coset-refinement towers and chains) would lower
> it to $37$ (finite computations over the exceptional primes).

Optional addition after "$c \le 8$": "(at $c = 9$, at every prime $p > 424549$ outside
$p \equiv 1 \pmod 9$ in $(9^9/2, T_A(9)]$)". The status sentence at the end of the paragraph
can stay "conditional; AI-checked, pending human review". If the owner wants, the parts listed
as liftable in section 0 can be relabelled "AI-checked, refereed by AI, pending human review".

## 6. Adversarial self-check

1. **Is my reformulation of E_2 the paper's definition?** The paper asks for a contraction
   with C_00 ≠ 0, normalised to α_0 = 1 and β_0 = 0. My search uses exactly that
   normalisation (x_0 = 1, y_0 = 0). The "not all equal" equivalence is used only to explain
   it.
   - The search agrees with the repo's sets for κ = 4, 5, 6 and 7 (≤ 6000), 8 (≤ 4400) and
     9 (≤ 6000), with no disagreement.
   - Those repo sets come from different programs. Agreement is evidence, not proof.
2. **Could my DFS wrongly report MEMBER?** It prunes only on empty domains, and it branches
   over every value of the chosen variable, so it is complete if the code is right.
   - The risk is a bit-shift bug in `and_shift` that drops candidates.
   - Mitigation: verdicts match independent repo data on 600+ primes, including the
     non-members found deep in the tree (1553, 3089, 3121, 3361, 4177 for κ = 8).
   - A full human audit of e2dfs.c has not been done.
3. **Witness checks use the repo's coset generator g.** wcheck checks that g^h has exact
   order κ, so the cosets are labelled consistently. Existence does not depend on g
   (paper, app:s2-contraction; I re-derived the transport).
   - 8 κ = 8 lines did not parse and were counted "bad". They are truncated lines in the
     inputs. Coverage was complete without them, so they do not matter.
4. **The κ = 8 conclusion "empty above 14281"** rests on stored witnesses plus prop:app-s2-TA.
   My checker accepts the witnesses. The step above T_A(8) is the proof, which is correct as
   far as I can tell, but no human has read it.
5. **Exponent tables.**
   - The tail argument above 10⁶ is by hand (section 4).
   - The worst-case primes (1009, 73, 2521) use only my own exhaustive verdicts.
   - A bug in `zero_sum_len` would change only the zero-sum rows. Those match the earlier
     referee's E_S1t row (5, …, 53) and t(41,8) = 5.
6. **Did I read "these solvers" too narrowly?** The sentence lists Schedule 2, the triangular
   variant and the block-steered variant. The block-steered variant cannot enter a
   fixed-prime worst case, since its prime range grows with m. The zero-sum depth comes only
   in the next paragraph, and towers and chains are absent from the core.
   - If the integrator intends the full version's toolbox, 37 may be right. But then the
     core must name that toolbox, and 37 inherits the unreviewed tower and chain proofs and
     the NOSTD/chain searches, which I did not re-run.
7. **Weil locator.** The form used matches Lidl–Niederreiter Theorem 5.41 as I recall it. I
   did not see the book, so the locator still needs a human.
8. **What I did not do:**
   - check the block-steered variant, Schedule 3, the towers, the chains, or the 145 → 53
     paragraph (beyond reproducing its 53);
   - decide 14281 ∈ E_2(8);
   - decide any prime in the κ = 9 undecided band.

## 7. Files (`research/audits/reviews/2026-11-12-rees-harsh-schedule2/`)

- `e2dfs.c`: complete E_2 decision search (own).
- `verify_cert.py`, `wcheck.c`: two certificate checkers (own).
- `e2scan.c`: second-moment sampler (own).
- `thresholds.py` → `thresholds.out`: T_W, T_A, T_S, monotonicity grid.
- `ex_k*_*.out`: exhaustive verdicts. `hunt_k*_*.out`: node-limited certificate hunts; the
  κ = 8 and κ = 9 hunts were stopped early as redundant. `resolve_k7.out`: exhaustive
  resolution of the κ = 7 hunt's undecided primes.
- `scan_k7_1e6_TA7.out` + `wcheck_k7_scan.out`: the complete κ = 7 band (10⁶, ⌈T_A(7)⌉]. `sample_k*.txt` / `sample_k*.out`: random-prime samples.
- `wcheck_k8_repo.out`, `wcheck_k8_low.out`, `wcheck_k9_repo.out`: stored-witness verification
  and coverage. `repo_witnesses_json.txt`: the repo's json witnesses, converted.
- `compare_repo.out`: own versus repo membership comparison.
- `exponents_own.py` → `exponents_own_1000000.out`: exponent tables. `exponents_2cminus1_check.out`: maximum of the triangular rule over primes in (14281, 10⁶] for each c.
- `bench_raw.out`: first benchmark (κ = 8 on 4000–4300, 2521 for κ = 8, 9).
- `run_*.sh`: drivers.
