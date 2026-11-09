# Rees paper, referee 2 items 2.5 / P10: proof of the counts of Theorem bb-envelope

**Date.** 2026-11-03/04. **AI session only; no human review.** Nothing here changes a claim
gate, a registry, `STATE.md`, `main.tex` or any `appendix-*.tex`; the integrator owns those.

**Read.** `research/STATE.md`, `research/TRAPS.md`; referee 2 items 2.5 and P10
(`research/audits/reviews/2026-11-03-rees-referee-2.md`, lines 196-204 and 520-528);
`docs/papers/rees-hsp/main.tex`: `thm:main` and its displayed count (lines 178-200),
`sec:recursion` (426-467), `thm:is-import` (470-489), `thm:power-sde` (497-507),
`rem:combined-schedule` (548-550), `thm:uniform-compilation` (602-620), `thm:ring-to-field`
(737-750), `prop:black-box` (767-776), `thm:bb-envelope` and its sketch (780-794);
`docs/papers/rees-hsp/appendix-torsion-blackbox.tex` in full (the Lazard toolkit, `app:tb-ring`
with `prop:tb-recursion`, `app:tb-blackbox` with `lem:tb-sylow`, `lem:tb-small-primes`,
`lem:tb-kernel`, routes (R1)/(R2), the new `lem:tb-chart` (lines 833-1007, added by the
integrator during this pass, with its "Ring operations" paragraph and its closing count
paragraph), `tab:tb-steps`); the chart-lemma report
`research/audits/reviews/2026-11-03-rees-chart-lemma.md` (header and verdict only); the report
the sketch cites,
`research/audits/reviews/2026-11-02-rees-bb-envelope.md`, Sections 2.5-2.9, 3, 4, and its
script `bb_envelope_check.py`.

**Lettering.** `appendix-torsion-blackbox.tex` is the fifth `\input` after `\appendix`
(schedule2, schedule3, free-coordinate, subspace, torsion-blackbox, codimension), so it is
Appendix E, as the referee writes; the brief's "Appendix D" is off by one. Below it is called
"the black-box appendix" and cited by its label `app:torsion-blackbox`.

**Script.** `research/audits/reviews/2026-11-03-rees-bb-envelope-counts/ew_exponent_check.py`
(exact integers; output in `ew_exponent_check.out`, "ALL CHECKS PASSED"). Run from the repo
root with `/opt/anaconda3/bin/python -B <path>`.

**Labels.** Every claim below is marked **[proved]** (follows from results stated in the paper,
with the derivation written here), **[exact computation]** (a finite exact calculation, in the
script), or **[argued]** (a step that uses a standard fact or an exponent the paper does not
state). Hypotheses the paper does not state are called out as **[extra hypothesis]**.

## 0. Verdict

| Item of `thm:bb-envelope` | Status | Where |
|---|---|---|
| (i) large-prime query count `c K_c (L+t)(L+1)^{E_W(c)}`; per-prime call structure; `p <= c` term | **proved**, conditional only on the results it cites (`thm:main`, `rem:combined-schedule`, `thm:ring-to-field`(iii)/`prop:tb-recursion`, `lem:tb-kernel`, `lem:tb-sylow`, `lem:tb-small-primes`) | Section 3 |
| Exponents `E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143` and Schedule-1 value `145` | **proved for all primes** (not a scan) and **exact computation** | Section 3.2 |
| (ii) `4 n_p (2 b_M + A_c)` per local query; preprocessing count | **proved** | Section 4 |
| (ii) chart-acquisition count | the cost bound is **proved**, but the displayed inequality `n_p^2(...) <= k d (...)` is **false**: smallest example `G = C_27`, `s = 1`, `c = 2`, `eps = 1/2` (`n_p^2 = 9 > k d = 7`). Correct term: `min(d, n_p)^2 (2 b_M + A_c)` | Section 4.2 |
| (iii) gates `O_c(Q_f (l^3 + w) polylog(l/eps))` | **not derivable as stated**; two defects. (a) It needs an **extra hypothesis** on the degree of the single-coordinate `QFT_p` cost, which `thm:uniform-compilation`(iii) states only as `poly`; example `G = C_p` with an `l`-bit prime. (b) It **omits the chart-acquisition gates** (`k d` transforms over `Z/p^{e_p}` and `2 k d (2 b_M + A_c)` oracle calls per prime), which grow like `s^c` and are not bounded by `Q_f (l^3 + w)`; example `G = C_3`, `c = 2`, `s` redundant generators. With both fixed, the bound is **argued** (standard per-field-operation gate cost) | Section 5.1 |
| (iii) classical time for charts `O_c(s^c l^5 + l^6)` | **proved** from `lem:tb-chart` (`O_c(d k^2 + k^4)` ring operations, `O(b_M^2)` bit operations each), under the theorem's own condition `log_2(8 l/eps) <= l`; the sharper total is `O_c(s^c l^4 + l^6)`; in general `l` must be read as `Lambda = l + log_2(8 l/eps)` in the `k`-terms | Section 5.2 |
| Which counts the condition `log_2(8 l/eps) <= l` affects | only the `l`-only forms of the chart terms: the classical chart time in (iii) and the chart-gate term that (iii) must add; **not** (i), (ii), (iv), the core gate and solver terms, or any `N`-form | Section 7b |
| (iii) solver time `Q_f l^{beta_c} poly(log p)` | **argued**, with `beta_c` as defined there (an imported, unstated exponent) | Section 5.3 |
| (iv) four-way error split | **proved** | Section 6 |
| Closing paragraph: `O_c(N^{E_W+1})` queries, independent of `s`; exponent `E_W(c)` when all `e_p = 1` | **proved** | Section 3.5-3.6 |
| Closing paragraph: gates `O_c(N^{E_W+4+o(1)})`, time `O_c(N^{E_W+1+max(3,beta_c)+o(1)})` | **argued**, under the extra hypotheses of Section 5.1 (QFT degree at most 3, field operation `O(log^2 p)` gates, Shor order finding/factoring `O(l^3)` gates per run) | Section 7 |

A refutation is a result: items (ii) and (iii) need the corrections stated in Section 9.3 before
the subsection of Section 9.1 proves them.

## 1. What is to be proved, and what it may use

**Access model and quantifiers** (from `thm:bb-envelope` and `app:tb-blackbox`). `c` is fixed.
`G` is a black-box group with unique `l`-bit encodings, so `|G| <= 2^l`, with a coherent
multiplication oracle (counted as one gate per call), generators `g_1, ..., g_s`, promised
nilpotent of class at most `c`; `f` is a coherent hiding oracle of label width `w` for an
arbitrary `H <= G`; `eps` in `(0,1)`. For a prime `p` write `G_p` for the Sylow subgroup,
`n_p = log_p |G_p|`, `p^{e_p} = exp G_p`, `M = p^{e_p}`, `b_M = ceil(log_2 M)`,
`d = rank F_{s,c} <= sum_{k<=c} s^k`, `A_c = m_+ + 2 b_M q_+` (word constants of
`lem:tb-words`), `k = floor(l / log_2 p) + ceil(log_p(8 l/eps))` (chart samples,
`prop:black-box`(iv)), `L = sum_{p>c} n_p`, `t = ceil(log_2(12 l/eps))`,
`K_c = prod_{d=2}^c d^{d(d-1) ceil(log_2(d+1))/2}`, `kappa_d = gcd(d, p-1)`,
`e_d(p) = 1, 2, kappa_d ceil(log_2(kappa_d+1))` for the linear, two-level and Schedule-1
grade of `rem:combined-schedule`, and `E_W(c) = max_{p>c} (1 + sum_{d=2}^c e_d(p))`.
`N = s l + w + log(1/eps)`.

**Algorithm whose counts are claimed** (the composition proved correct in `app:tb-blackbox`):
1. Sylow split by `lem:tb-sylow`, with error share `eps/4`.
2. `G_{<=c}` by `lem:tb-small-primes` (Imran-Ivanyos), error share `eps/4` for gate synthesis.
3. For each prime `p > c`: pullback `Phi : F_{s,c} -> G_p` (`prop:black-box`(i)); chart
   acquisition by `lem:tb-kernel` at `delta = eps/(4 l)` and the Howell/Smith arithmetic of
   route (R2); then, if `e_p = 1`, one call of `thm:main` on the chart `L_G = F/ker pi`
   (dimension `n_p`), and if `e_p > 1`, Algorithm `RtF` of `prop:tb-recursion` on the chart with
   `thm:main` as the field solver, each call at error `eps/(4 l)`. The arities are those of
   `rem:combined-schedule` (combined rule), or of `thm:main` (Schedule 1 alone).
4. Push a basis of `log(H cap G_p)` through the chart-to-group words; output the union over `p`.

**Results used, and exactly what is taken from each.**
- `thm:main` (statement): one call on an `F_p`-Lie algebra of dimension `m`, class at most `c`,
  with grade dimensions `g_d`, error `eps'`, makes at most
  `Q_core = c (m + ceil(log_p(3/eps'))) prod_{d=2}^c M_d` queries, `M_d = B_d(g_d)`, where
  `B_d(a) = [d^{d(d-1)/2} (a+1)^d]^{ceil(log_2(d+1))}` (`thm:is-import`). Its proof in
  `sec:recursion` fixes the recursion tree: `S = m + ceil(log_p(3/eps'))` terminal samples,
  `P = prod_d M_d` lifted sources per terminal sample, `c` queries per lifted source,
  `N_instr = S (P + sum_{d=2}^c prod_{d'<d} M_{d'} + 1)` instruments.
- `rem:combined-schedule`: `M_d = g_d + 1` if `kappa_d = 1`; `M_d = (g_d+1)((kappa_d-1) g_d + 1)`
  if `kappa_d >= 2` and `p >= 16 kappa_d^{2 kappa_d + 2}` (`thm:power-sde`(ii)); otherwise
  `M_d = B_{kappa_d}(g_d)`. The count `Q_core` has the same form with these `M_d`.
- `prop:tb-recursion`: on a ring with `b = log_p |.|`, at most `b` calls on every branch, none on
  a trivial section; `K_0 = 0 < K_1 < ...` with `|K_j| >= p^j`; failure at most `b eta` for
  per-call error `eta`; `poly(B)` public arithmetic; one `f` query per local query
  (`lem:tb-quotient-oracle`); every socle has class at most `c` (`lem:tb-section-rank`).
- `lem:tb-kernel`: `ker pi` with failure `delta` from
  `min(d, floor(l/log_2 p)) + ceil(log_p(2/delta)) <= k` coherent evaluations of `Phi`, no `f`
  query.
- `lem:tb-chart` (proved in `app:tb-blackbox`, AI-checked): from the `k x d` sample matrix
  `Y`, with `n = log_p |G| <= floor(l/log_2 p) <= k`, it computes a set `J` of `r <= n` kept
  columns, a basis `epsilon_1, ..., epsilon_m` of `L_G` with `m <= r`, `sum_i e_i = n`, lifts
  supported on `J`, the coordinate map and the structure constants, in `O_c(d k^2 + k^4)` ring
  operations modulo `M` (each `O(b_M^2)` bit operations by its "Ring operations" paragraph),
  with no evaluation of `Phi` and no `f` query; the images `Phi(tilde epsilon_i)` cost at most
  `n (2 b_e + m_+ + 2 b_e q_+)` multiplications each. Its closing paragraph: the count is
  `O_c(s^c l^2 + l^4)` ring operations when `log_2(8 l/eps) <= l`, and `O_c(s^c N^2 + N^4)`
  without that condition.
- `prop:black-box`(i): precomputation `(d - s)(m_[] + 2 b_e q_[])` multiplications; one
  evaluation of `Phi` at most `d (2 b_e + m_+ + 2 b_e q_+)` multiplications, doubled for
  reversible cleanup.
- `lem:tb-sylow`(d): `O(s l^2 + s l log(s/eps_pre))` multiplications and
  `poly(s, l, log(1/eps_pre))` further gates, detected failure at most `eps_pre`.
- `lem:tb-small-primes`: `poly(l)` operations and `poly(log |G_{<=c}|)` calls, one `f` query per
  call (imported from Imran-Ivanyos, Theorem 1).
- `thm:uniform-compilation`: (i) one BCH evaluation at stage `d` uses
  `(d-1)d(d+1)(d+2)/6 <= c^4` brackets of `O(D_d^3) <= O(n^3)` field operations,
  `n <= c m` the cover dimension; (ii) a clean controlled right translation is four BCH
  evaluations; (iii) a single-coordinate `QFT_p` to isometry error `eta` costs
  `poly(log p + log(1/eta))` gates, with `q_max = max(n, m, max_d(2 M_d g_d + D_{d-1}))`
  transforms per instrument, `n` per lifted source, `2 g_d` per complete central instrument,
  `D_{d-1}` per merge node, `m` per readout; `lem:hybrid` adds the errors.

Two elementary facts are used throughout.

**Fact E1 [proved].** `L = sum_{p>c} n_p <= l / log_2(c+1)`, and the number `r` of primes
`p > c` dividing `|G|` is at most `L`. Proof: `prod_{p>c} p^{n_p} <= |G| <= 2^l`, so
`sum_p n_p log_2 p <= l`, and `p >= c + 1` for every such prime; `n_p >= 1` for each of them,
since `p | |G|` forces `G_p != 1` (`lem:tb-sylow`(b)).

**Fact E2 [proved].** For integers `E >= 1`, `t >= 0`, the function
`phi(x) = x (x + t)(x + 1)^{E-1}` is superadditive on `x >= 0`: `phi(a) + phi(b) <= phi(a+b)`.
Proof: `phi` is a polynomial with nonnegative coefficients and `phi(0) = 0`; such a function is
convex on `[0, inf)`, and a convex `phi` with `phi(0) = 0` satisfies
`phi(a) = phi((a/(a+b))(a+b) + (b/(a+b)) 0) <= (a/(a+b)) phi(a+b)`, likewise for `b`; add.
(Checked exactly for `E in {1,2,5,11,143}`, `t in {0,1,7,50}`, `a, b < 30`; script Section C.)

## 2. Notation for one core call

Fix a prime `p > c` and a core call on an explicit `F_p`-Lie algebra `Omega` of dimension
`m`, class `c' <= c`, grade dimensions `g_2, ..., g_{c'}` (`g_d = 0` for `d > c'`), with
per-call error `eps' = eps/(4 l)`. Write `t_p = ceil(log_p(3/eps')) = ceil(log_p(12 l/eps))`.
Then `t_p <= t = ceil(log_2(12 l/eps))` because `p >= 2`. **[proved]**

A socle of class `c' < c` is processed by `thm:main` at `c'`, whose count is at most the count
at `c` because every arity is at least `1` and `c' <= c` (`app:tb-ring`, paragraph before
`prop:tb-recursion`); so it suffices to bound the count at class `c`. **[proved]**

## 3. Proof of (i)

### 3.1 One core call

**Lemma A [proved].** Under the combined rule, for every prime `p > c` and every grade `d`,
`M_d <= C_d (g_d + 1)^{e_d(p)}` with `C_d <= d^{d(d-1) ceil(log_2(d+1))/2}`. Hence, since
`g_d <= m`,
```
prod_{d=2}^c M_d <= K_c (m + 1)^{sum_{d=2}^c e_d(p)} <= K_c (m + 1)^{E_W(c) - 1}.
```
Under Schedule 1 alone the same holds with `e_d = d ceil(log_2(d+1))`.

Proof. Linear grade: `M_d = g_d + 1`, `C_d = 1`, `e_d = 1`. Two-level grade (`kappa_d >= 2`):
`(kappa_d - 1) g_d + 1 <= (kappa_d - 1)(g_d + 1)` because `kappa_d - 1 >= 1`, so
`M_d <= (kappa_d - 1)(g_d + 1)^2`, `C_d = kappa_d - 1 <= d - 1`, `e_d = 2`. Schedule-1 grade at
degree `kappa = kappa_d <= d`: `B_kappa(g_d) = kappa^{kappa(kappa-1) ceil(log_2(kappa+1))/2}
(g_d + 1)^{kappa ceil(log_2(kappa+1))}`, so `C_d = kappa^{kappa(kappa-1) ceil(log_2(kappa+1))/2}`,
`e_d = kappa ceil(log_2(kappa+1))`; `x -> x^{x(x-1) ceil(log_2(x+1))/2}` is nondecreasing on
`x >= 1`, so `C_d <= d^{d(d-1) ceil(log_2(d+1))/2}`. In every case `C_d <= d^{d(d-1)ceil(log_2(d+1))/2}`
(for the first two cases because that number is at least `d`). A grade with `g_d = 0` gives
`M_d <= C_d`, consistent with the bound. Multiply over `d` and use `g_d + 1 <= m + 1`; the last
step is the definition of `E_W(c)` as a maximum over `p`. (Exact check on 2064 profiles, script
Section B.)

**Corollary A' [proved].** One core call of dimension `m` at error `eps/(4 l)` makes at most
```
Q_core(m) := c (m + t) K_c (m + 1)^{E_W(c) - 1}
```
queries to `f`, and `Q_core` is nondecreasing in `m`. (From `thm:main`'s count, Lemma A and
`t_p <= t`. Monotonicity: every factor is nondecreasing.) The count is fixed by public data,
so it holds on every branch, including branches after an erroneous earlier call.

### 3.2 The exponents `E_W(c)` for `c = 2, ..., 9` [proved for all primes; exact computation]

Let `E_1(c) = 1 + sum_{d=2}^c d ceil(log_2(d+1))`. Then `E_1(2..9) = 5, 11, 23, 38, 56, 77, 109, 145`.

**Lemma B [proved].** For every prime `p > c` and every `d >= 2`:
`e_d(p) <= d ceil(log_2(d+1))`, with equality if and only if `kappa_d = d` (that is,
`d | p - 1`) and `p < 16 d^{2d+2}`. Moreover the loss `d ceil(log_2(d+1)) - e_d(p)` is at least
`2` whenever it is positive.

Proof. `1 <= 2 <= 4 <= d ceil(log_2(d+1))` for `d >= 2`, and
`kappa ceil(log_2(kappa+1)) <= d ceil(log_2(d+1))` for `kappa <= d`, with equality iff
`kappa = d`. The Schedule-1 value is taken exactly when `kappa_d >= 2` and
`p < 16 kappa_d^{2 kappa_d + 2}`; so equality needs `kappa_d = d` and `p < 16 d^{2d+2}`. The
loss is `d ceil(log_2(d+1)) - 2 >= 2` at a two-level grade, `>= 3` at a linear grade, and
`>= 2` at a Schedule-1 grade of degree `kappa_d < d` (since `kappa ceil(log_2(kappa+1))` is
strictly increasing in `kappa`; at `d = 2` the only alternative is two-level, loss 2).

**Proposition B' [proved].** `E_W(c) = E_1(c)` if some prime `p < 1024` satisfies
`lcm(2, ..., c) | p - 1`; otherwise `E_W(c) = E_1(c) - 2`. Consequently
`E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143` for `c = 2, ..., 9`.

Proof. The thresholds `16 d^{2d+2}` are `1024` at `d = 2` and exceed `1024` for `d >= 3`. So
`1 + sum_d e_d(p) = E_1(c)` iff `d | p - 1` for all `2 <= d <= c` and `p < 1024`. If such a
prime exists, `E_W(c) = E_1(c)`. If not, every prime loses at least `2` (Lemma B), and the
loss `2` is attained by any prime `p >= 1024` with `lcm(2..c) | p - 1`: at grade 2 it is
two-level (`kappa_2 = 2`, `p >= 1024`), at every grade `d >= 3` it has `kappa_d = d` and
`p < 16 d^{2d+2}` provided `p < 16 * 3^8 = 104976`; such a prime exists (e.g. `p = 2521` for
`c = 8, 9`). Since `E_W(c)` is a maximum over the finitely many values of
`1 + sum_d e_d(p)`, this determines it exactly. Witnesses: `p = 3, 7, 13, 61, 61, 421` attain
`E_1(c)` for `c = 2, ..., 7` (`421 = 420 + 1`, `420 = lcm(2..7)`); for `c = 8`, `lcm = 840` and
`841 = 29^2` is the only candidate below `1024`, not prime; for `c = 9`, `lcm = 2520 > 1023`.
Hence `E_W(8) = 107`, `E_W(9) = 143`, attained at `p = 2521`. The script (Section A) confirms
each value both by this rule and by a scan over every prime `c < p < 2 * 10^5`.

This upgrades the earlier report's finite scan to a statement about all primes: the maximum in
the definition of `E_W(c)` is attained, and its value is known exactly for `c <= 9`.

**Constant [exact computation].** `log_2 K_c = 2.0, 11.5, 47.5, 117.2, 233.5, 410.4, 746.4, 1202.8`
for `c = 2..9`, and `log_2(9 K_9) = 1206.0`, as the theorem states.

### 3.3 One Sylow subgroup, `p > c`

**Lemma C [proved].** Let `p > c` with `n_p >= 1`. The queries to `f` spent on `G_p` after chart
acquisition satisfy
- if `e_p = 1`: `Q_p <= Q_core(n_p)`;
- if `e_p > 1`: `Q_p <= sum_{j=0}^{n_p - 1} Q_core(n_p - j) <= n_p Q_core(n_p)`.
In both cases `Q_p <= c K_c n_p (n_p + t)(n_p + 1)^{E_W(c) - 1} = c K_c phi(n_p)`.

Proof. `e_p = 1`: the chart `L_G = F/ker pi` is an `F_p`-Lie algebra of dimension
`n_p = log_p |G_p|` and class at most `c`, with oracle `f o bar Phi` at one `f` query per query
(route (R2), `e = 1` paragraph of `app:tb-blackbox`); one call of `thm:main` with error
`eps/(4 l)`, so Corollary A' applies with `m = n_p`. `e_p > 1`: Algorithm `RtF` on the chart,
with `b = log_p |L_G| = n_p`. By `prop:tb-recursion`, the `j`-th call (`j = 0, 1, ...`) is made
only if `S_j != K_j`, and `|K_j| >= p^j`; the call runs on the socle of `S_j / K_j`, whose
dimension is the number of cyclic factors of `S_j / K_j`, at most
`log_p |S_j / K_j| <= log_p(|L_G| / |K_j|) <= n_p - j`. So at most `n_p` calls are made
(`j <= n_p - 1`), on every branch, the `j`-th of dimension at most `n_p - j`, each at error
`eps/(4 l)`; `prop:tb-recursion` also gives that every local query is one `f` query
(`lem:tb-quotient-oracle`), and the chart acquisition makes none (`lem:tb-kernel`). Sum
Corollary A' and use monotonicity. The last display uses `n_p >= 1` in the `e_p = 1` case.

The sharper per-prime form `sum_j Q_core(n_p - j)` is the one to quote when `n_p` is known;
the earlier report measured its ratio to `n_p Q_core(n_p)` as about `1/(E_W + 1)`.

### 3.4 Sum over the primes `p > c` [proved]

By Lemma C and Fact E2,
```
Q_{>c} = sum_{p>c} Q_p <= c K_c sum_{p>c} phi(n_p) <= c K_c phi(L)
       = c K_c L (L + t)(L + 1)^{E_W(c) - 1} <= c K_c (L + t)(L + 1)^{E_W(c)},
```
the last step because `L <= L + 1`. This is (i)'s displayed bound. The primes `p <= c` add the
`poly(log |G_{<=c}|)` calls of `lem:tb-small-primes`, each one `f` query; no other step
queries `f` (`lem:tb-sylow`(d), `lem:tb-kernel`, route (R2) arithmetic). **This proves (i).**

### 3.5 The `N`-form of the query count [proved]

`L <= l <= N` (Fact E1, `s >= 1`), and `t <= log_2(12 l/eps) + 1 <= log_2 l + log_2(1/eps) + 5
<= N + 5` because `N >= l + log_2(1/eps) >= log_2 l + log_2(1/eps)`. So
`(L + t)(L + 1)^{E_W(c)} <= (2N + 5)(N + 1)^{E_W(c)} = O(N^{E_W(c) + 1})`, with a constant
depending on `c` only through `c K_c`. Nothing in `Q_{>c}` depends on `s`: `s` enters only
through `d`, which appears in chart acquisition (no `f` queries).

### 3.6 The clause "if every Sylow subgroup for `p > c` has exponent `p`, the large-prime query exponent is `E_W(c)`" [proved]

Then `Q_p <= c K_c (n_p + t)(n_p + 1)^{E-1}` for each `p`, `E = E_W(c) >= 2` (for `c >= 2`).
Put `x_p = n_p + 1 >= 2` and `X = sum_p x_p = L + r <= 2L` (Fact E1). Since `x -> x^k` is
superadditive on `x >= 0` for `k >= 1`,
```
sum_p (n_p + t)(n_p + 1)^{E-1} <= sum_p (x_p + t) x_p^{E-1}
   = sum_p x_p^E + t sum_p x_p^{E-1} <= X^E + t X^{E-1} = X^{E-1}(X + t)
   <= (2L)^{E-1}(2L + t) <= 2^E (L + 1)^{E-1}(L + t).
```
So `Q_{>c} <= 2^{E_W(c)} c K_c (L + t)(L + 1)^{E_W(c) - 1} = O_c(N^{E_W(c)})` by Section 3.5.
(Exact check on 900 random partitions, script Section D.) The naive route via Fact E2 does not
apply here because `psi(x) = (x + t)(x + 1)^{E-1}` has `psi(0) = t > 0`; the argument above is
what gives the clause.

## 4. Item (ii): group-oracle calls

### 4.1 Per local query [proved]

Let `n' <= min(d, n_p)` be the number of chart basis elements `epsilon_1, ..., epsilon_{n'}`
(route (R2): at most `n_p` kept columns, and at most `d` columns exist). A local query to the
section oracle `f o sigma o iota_M` (or `f o bar Phi` when `e_p = 1`) computes, into a clean
register, `exp(sum_i x_i epsilon_i) = Pi_+(... Pi_+(h'_1^{x_1}, h'_2^{x_2}) ..., h'_{n'}^{x_{n'}})`
from the precomputed images `h'_i = Phi(epsilon_i)`, with `0 <= x_i < p^{a_i} <= M`: at most
`n'` powers of `2 b_M` multiplications each and `n' - 1` programs `Pi_+` of `m_+ + 2 b_M q_+`
each, so at most `n'(2 b_M + A_c)` multiplications as a straight-line program; Bennett
compute-copy-uncompute doubles it (`prop:black-box`(i), coherence item); the query then applies
`U_f` once and runs the evaluation backwards. Total at most `4 n'(2 b_M + A_c) <= 4 n_p (2 b_M + A_c)`
multiplication-oracle calls and one `f` query. The maps `iota_M` and `sigma` are public
normal-form arithmetic on coordinates (`lem:tb-quotient-oracle`, (M1), (M3)) and use no oracle.

### 4.2 Chart acquisition: the cost bound holds, the displayed inequality does not

**Cost [proved from `prop:black-box`(i), `lem:tb-kernel` and `lem:tb-chart`].** Per prime
`p > c`: precomputation of the Hall images `h_j`: `(d - s)(m_[] + 2 b_M q_[])` multiplications;
`k` coherent evaluations of `Phi` with cleanup: at most `2 k d (2 b_M + A_c)`; images of the
chart basis, classically: by `lem:tb-chart`(b) there are `m <= r` basis elements whose lifts are
supported on `J`, `|J| = r <= n_p` and `J` a subset of `{1, ..., d}`, so `r <= min(d, n_p)`; each
image is a `Pi_+`-chain over at most `r` Hall indices, at most `r (2 b_M + A_c)` multiplications,
so at most `r m (2 b_M + A_c) <= min(d, n_p)^2 (2 b_M + A_c)` in all (the lemma itself states the
looser `n^2 (2 b_e + m_+ + 2 b_e q_+)`).
Since `min(d, n_p)^2 <= d n_p <= d k` (as `n_p <= floor(l/log_2 p) <= k`, Fact E1), the total is
at most `(d - s)(m_[] + 2 b_M q_[]) + 3 k d (2 b_M + A_c)`, which is the right-hand side the
theorem displays. **[proved]**

**Defect in the displayed chain [exact computation].** The theorem writes the middle term as
`n_p^2 (2 b_M + A_c)` and then asserts `... + n_p^2(2 b_M + A_c) <= ... + 3 k d (2 b_M + A_c)`,
that is, `n_p^2 <= k d`. This is false in general. Smallest example: `G = C_27` (so `p = 3`,
`e_p = 3`, class `1 <= c = 2`), one generator `s = 1`, `eps = 1/2`. Then `F_{1,2} = Z/27` has
`d = 1`, `n_p = 3`, `l = 5` (unique 5-bit encodings of 27 elements),
`k = floor(5/log_2 3) + ceil(log_3(80)) = 3 + 4 = 7`, and `n_p^2 = 9 > 7 = k d`. The same
happens for `C_125` (`9 > 6`) and `C_81` (`16 > 9`); script Section E. The cost itself is
`min(d, n_p)^2 (2 b_M + A_c) = 2 b_M + A_c` there, far below either side. Fix: replace `n_p^2`
by `min(d, n_p)^2` in (ii); the chain then holds by the display above. Not a patch around the
problem: `n_p` counts cyclic factors of `log G_p`, which is **not** bounded by `d` (the brief's
own `prop:black-box`(iv) says `k` "bounds the number of cyclic factors of `log G`, which is not
bounded by `s`"); the support of each `epsilon_i` is bounded by the number of kept columns,
`<= min(d, n_p)`.

### 4.3 Preprocessing [proved]

`lem:tb-sylow`(d) with `eps_pre = eps/4` gives `O(s l^2 + s l log(4 s/eps))
= O(s l^2 + s l log(s/eps))` multiplications (`log(4s/eps) <= log(s/eps) + 2` and
`2 s l <= 2 s l^2`).

## 5. Item (iii): gates and classical time

### 5.1 Quantum gates for the core calls

Fix a core call of dimension `m <= n_p` on a cover of dimension `n <= c m <= c n_p`, with
`Q_f^{call} = c S P` queries (`S = m + t_p`, `P = prod_d M_d`). Count gates per `sec:recursion`'s
tree, each oracle call (to `f` or to the multiplication) counted once.

**Tree size [proved].** The tree of one terminal sample has `P` leaves (lifted sources); the
merge nodes at stage `d` number `prod_{d'<d} M_{d'}`, each with `M_d` child slots; the total
number of slots is `sum_{d=2}^c prod_{d'<=d} M_{d'} <= (c - 1) P`, and the number of merge nodes is
at most `(c - 1) P`. Over `S` terminal samples: at most `(c - 1) S P < Q_f^{call}` slots, `S P`
leaves, `S` readouts.

**Arithmetic per slot [argued: standard per-field-operation gate cost].** Each slot is one
clean controlled right translation `x -> x * (-delta_s(sigma(u)))`: four BCH evaluations
(`thm:uniform-compilation`(ii)), each at most `c^4` brackets of `O(n^3)` field operations
(`thm:uniform-compilation`(i)), plus `O(n^2)` field operations for the public linear maps
`sigma`, `delta_s`. So `O(c^5 n^3) = O_c(n_p^3)` field operations. A field operation modulo
`p` costs `O(log^2 p)` gates by schoolbook reversible arithmetic with clean workspace (standard;
**the paper states this nowhere**, it speaks of "field operations"). With `n_p log_2 p <= l`
(Fact E1), the slot costs `O_c(n_p^3 log^2 p) <= O_c(l^3 / log p) <= O_c(l^3)` gates.

**Per leaf [proved given 4.1].** `c` queries, each `O_c(n_p (2 b_M + A_c)) = O_c(l)` oracle
calls (Section 4.1, `b_M <= e_p log_2 p + 1 <= 2 l`), `O(w)` gates to route the `w` label bits,
and `O(n)` field operations for the evaluation maps `E_s`: `O_c(l + w)` per query.

**Transforms [proved count; cost needs an extra hypothesis].** Per `thm:uniform-compilation`(iii):
`n <= c n_p` transforms per leaf, `2 g_d <= 2 n_p` per slot, `D_{d-1} <= n` per merge node, `m`
per readout: `O_c(n_p)` single-coordinate `QFT_p`'s per slot or leaf, so at most
`O_c(n_p) Q_f^{call}` in all. Each is compiled to isometry error
`eta = eps'/(3 N_instr q_max)`, where `log(1/eta) = O_c(log(l/eps))` because
`N_instr <= 2 Q_f^{call} <= 2 c K_c (l + t)(l + 1)^{E_W(c)}` and `q_max <= poly_c(l)`. The paper
gives the cost of one transform only as `poly(log p + log(1/eta))`. Write it as
`O((log p + log(1/eta))^{a})`. Then the transforms cost
`Q_f^{call} O_c(n_p (log p)^a + n_p polylog^a(l/eps)) <= Q_f^{call} O_c(l (log p)^{a-1} + l polylog(l/eps))`.
This is within `O_c(l^3) polylog(l/eps)` **if and only if `a <= 3`** uniformly in `p`, because
`log p` can be as large as `l`.

**[extra hypothesis]** The bound `O_c(Q_f (l^3 + w) polylog(l/eps))` therefore needs: *a
single-coordinate `QFT_p` to isometry error `eta` compiles into `O((log p)^3 polylog(1/eta))`
gates* (equivalently `a <= 3` above). `thm:uniform-compilation`(iii) does not state a degree.
Smallest example where it matters: `G = C_p` with `p` an `l`-bit prime, `c = 2`, `s = 1`. Then
`n_p = 1`, the chart is `F_p`, the one core call is abelian Fourier sampling with
`Q_f = 2 (1 + ceil(log_p(12 l/eps)))` queries, each followed by one `QFT_p` on an `l`-bit
coordinate; the gates are `Theta(Q_f T_QFT(l))`, against the claimed `O(Q_f (l^3 + w) polylog)`.
If `T_QFT(l) = l^a` with `a > 3` the claim fails. I cannot settle `a` from the paper, and the
cited constructions (Kitaev; Cleve-Watrous) were not opened in this session, so the question is
left as a hypothesis to be stated, not assumed. With `a <= 3` stated, the core gate bound reads
```
gates(core calls) <= Q_f * O_c(l^3 + w) * polylog(l/eps)      [argued]
```
summing over primes (each prime's `Q_f^{call}`'s add up to `Q_f`, and `l` is global).

**Second defect: the chart-acquisition gates are omitted [exact computation].** Item (iii)
lists, besides the core term, only the gates of Imran-Ivanyos and of order finding and
factoring. Chart acquisition for a prime `p > c` costs, as gates: `2 k d (2 b_M + A_c)`
multiplication-oracle calls plus `(d - s)(m_[] + 2 b_M q_[])` for the Hall images (if those are
done coherently; classically they are classical time), and `k d` single-coordinate transforms
over `Z/p^{e_p}` on `b_M <= l` bits in `lem:tb-kernel`. These are `Theta_c(d k b_M)` oracle
calls and `k d` transforms, with `d = rank F_{s,c} = Theta(s^c)`: they grow with `s`, while
`Q_f (l^3 + w)` does not. Smallest example: `G = C_3`, `c = 2`, `l = 2`, `w = 1`, `eps = 1/2`,
and `s` generators all equal to one generator (the theorem allows any generating list). Then
`Q_f = 2(1 + ceil(log_3 48)) = 10`, `Q_f (l^3 + w) = 90`, `k = 1 + 4 = 5`, `d = s(s+1)/2`, and
already with the word constants at their smallest conceivable value `1` the chart step makes at
least `275, 5175, 479250` oracle calls for `s = 2, 10, 100`, plus `k d = 15, 275, 25250`
transforms (script Section F). So (iii) as a total of "gates for `p > c`" is false; the closing
paragraph of the theorem, which says "for the primes `p > c`, and for order finding, factoring
and the charts, the number of gates is `O_c(N^{E_W(c)+4+o(1)})`", is the statement that is
true (Section 7). Fix: add to (iii) the term
`sum_{p>c} [ 2 k d (2 b_M + A_c) + (d - s)(m_[] + 2 b_M q_[]) ]` oracle calls and
`sum_{p>c} k d` transforms over `Z/p^{e_p}` on at most `l` bits.

### 5.2 Classical time for the charts [proved]

`lem:tb-chart` gives `O_c(d k^2 + k^4)` ring operations modulo `p^{e_p}` per prime, each
`O(b_M^2)` bit operations (its "Ring operations" paragraph; schoolbook arithmetic, extended
Euclid and at most `e` trial divisions). Put `Lambda = l + log_2(8 l/eps)`. For each prime
`p > c`: `k = floor(l/log_2 p) + ceil(log_p(8 l/eps)) <= (l + log_2(8 l/eps))/log_2 p + 1
<= 2 Lambda / log_2 p` (as `log_2 p <= l <= Lambda`), and `b_M <= e_p log_2 p + 1 <= 2 e_p log_2 p`.
Hence `k^2 b_M^2 <= 16 Lambda^2 e_p^2` and `k^4 b_M^2 <= 64 Lambda^4 e_p^2 / log_2^2 p <= 64 Lambda^4 e_p^2`.
Summing over the primes, with `sum_p e_p^2 <= (sum_p n_p)^2 = L^2 <= l^2` (Fact E1):
```
time(charts) <= O_c( d Lambda^2 l^2 + Lambda^4 l^2 )  bit operations.
```
If `log_2(8 l/eps) <= l` (that is, `eps >= 8 l 2^{-l}`), `Lambda <= 2 l` and this is
`O_c(s^c l^4 + l^6)`, which is within the stated `O_c(s^c l^5 + l^6)`. **[proved]** (The
lemma's own closing paragraph gives the per-prime count `O_c(s^c l^2 + l^4)` ring operations
under the same condition; the summation over primes above is what keeps the total at
`l^6` rather than `l^7`.) Without that condition the stated `l`-only bound fails (take `eps = 2^{-l^2}`;
then `k = Theta(l^2 / log p)` and the `k^4` term alone is `Theta(l^8 l^2/log^4 p)` per prime
for small `p`), but the `N`-form of Section 7 is unaffected since `Lambda <= 2N + 4`.

### 5.3 Classical time for the solvers and the normalizer steps [argued]

**Solvers.** `thm:is-import` (Ivanyos-Santha) and `thm:power-sde`(ii) give the solver time
only as polynomial in the arity and `log p` (and `log(1/abort)`). Define `beta_c` as the least
`beta` such that every solver call at a grade with `g_d <= a` and arity `M_d` runs within
`M_d (a + 1)^{beta} poly(log p) polylog(l/eps)` (the last factor covers the capped retries of
`sec:recursion`'s solver third; it is `1` at Schedule-1 grades, whose solver is deterministic).
Such a `beta_c` exists because the solver is polynomial in `M_d` and `M_d <= K_c (a+1)^{e_d}`; its
value is imported and not explicit, which is what the theorem says. A core call has at most
`S sum_d prod_{d'<d} M_{d'}` solver calls, and `sum_d (prod_{d'<d} M_{d'}) M_d <= (c-1) P`, so the
solver time of a call is at most `(c - 1) S P (n_p + 1)^{beta_c} poly(log p) polylog(l/eps)
<= Q_f^{call} l^{beta_c} poly(log p) polylog(l/eps)` (using `n_p + 1 <= l` for `l >= 2`, Fact E1).
Summing over primes gives the stated `Q_f l^{beta_c} poly(log p)` up to the `polylog(l/eps)`
retry factor, which the theorem's display omits; it is absorbed by the `o(1)` in Section 7.

**Normalizer steps.** `prop:tb-recursion`: `poly(B)` deterministic normal-form arithmetic per
round, at most `n_p <= l` rounds per prime, `L <= l` rounds in all. The degree of this
polynomial (Hermite/Smith forms of `O(n_p) x O(n_p^2)` integer matrices with `O(l)`-bit entries,
Kannan-Bachem/Storjohann) is not stated in the paper; it is a fixed constant, so the term is
`poly(l)` and absorbed in Section 7 only if that constant is at most `E_W(c) + 1 + max(3, beta_c)`,
which is at least `9` for `c >= 2`.

## 6. Item (iv): the error split [proved]

The algorithm runs its steps one after another with fresh randomness; a step's failure
probability bound is conditional on correct inputs from earlier steps. A first-error union bound
(`Pr[output wrong] <= sum_i Pr[step i is the first to fail] <= sum_i Pr[step i fails | earlier
steps correct]`) therefore bounds the total by the sum of the shares:
- preprocessing: `eps_pre = eps/4`, `lem:tb-sylow`(d), failure detected;
- primes `p <= c`: the Imran-Ivanyos algorithm is exact; compiling its exact small-prime
  transforms into the finite gate set, each gate to precision `eps/(4 N_II)` for `N_II` gates,
  costs at most `eps/4` by `lem:hybrid` (every `S_j` the whole space);
- charts: at most `r <= L <= l` primes `p > c`, each `lem:tb-kernel` at `delta = eps/(4 l)`
  (which is the sample count `k` of `prop:black-box`(iv): `ceil(log_p(2/delta)) = ceil(log_p(8 l/eps))`),
  total at most `eps/4`;
- core: at most `sum_{p>c} n_p = L <= l` calls in all (one per prime with `e_p = 1`, at most
  `n_p` per prime with `e_p > 1`, Lemma C), each at error `eps/(4 l)`, total at most `eps/4`. For a
  prime with `e_p > 1` this is `prop:tb-recursion` with per-call error `eta = eps/(4 l)` and `b = n_p`,
  failure at most `n_p eps/(4 l)`.
Inside a core call, `eps/(4 l)` is split into the thirds of `sec:recursion`. The stop rules and
the per-call time-out make the counts (i)-(iii) hold on erroneous branches as well
(`prop:tb-recursion`, "Well-definedness"); the query count is fixed by public data in any case.

## 7. The closing paragraph of the theorem

- Queries `O_c(N^{E_W(c)+1})` for `p > c`, independent of `s`: **proved** (Section 3.5).
- Primes `p <= c`: `poly(log |G|)` queries of Imran-Ivanyos, exponent not bounded here:
  **proved** as stated (imported).
- Exponent `E_W(c)` when all `e_p = 1`: **proved** (Section 3.6).
- `E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143` and `145` for Schedule 1 at `c = 9`: **proved and
  exact** (Section 3.2).
- Gates `O_c(N^{E_W(c)+4+o(1)})` for `p > c`, order finding, factoring and the charts:
  **argued**, under three facts the paper does not state: (H1) `QFT` over `F_p` or `Z/p^{e}` on at
  most `l` bits costs `O(l^3 polylog(l/eps))` gates (Section 5.1, `a <= 3`); (H2) a field
  operation costs `O(log^2 p)` gates; (H3) one run of Shor's order finding or factoring on
  `O(l)`-bit integers costs `O(l^3)` gates. Then: core gates `Q_f O_c(l^3 + w) polylog
  <= O_c(N^{E_W+1} N^3 N^{o(1)})` (with `Q_f = O_c(N^{E_W+1})`, `l^3 + w <= N^3`,
  `polylog(l/eps) <= polylog(2N) = N^{o(1)}` since `log(1/eps) <= N`); chart oracle calls
  `sum_p 2 k d (2 b_M + A_c) <= O_c(d Lambda sum_p e_p) <= O_c(s^c Lambda l) <= O_c(N^{c+2})`
  and chart transforms `sum_p k d l^3 <= O_c(s^c Lambda l^3 ... )`, more carefully
  `d l^3 sum_p k_p <= d l^3 2 Lambda sum_p 1/log_2 p <= 2 d l^3 Lambda L = O_c(s^c l^5)
  <= O_c(N^{max(c,5)})`; order finding and factoring `O(s l^3 log(s/eps)) = O(N^4)`. All exponents
  are at most `E_W(c) + 4` because `E_W(c) >= c` (every `e_d >= 1`) and `E_W(c) >= 5` for
  `c >= 2`.
- Time `O_c(N^{E_W(c)+1+max(3,beta_c)+o(1)})`: **argued** under the same facts plus the
  unstated normal-form degree (Section 5.3): `Q_f l^{max(3, beta_c)} polylog` from gates and
  solvers, `O_c(s^c Lambda^2 l^2 + Lambda^4 l^2) <= O_c(N^{max(c,6)})` for the charts, `poly(l)`
  normalizer arithmetic.
- "Its constants are astronomical (`log_2(9 K_9) ~ 1206`)": **exact**.

## 7b. Which counts the condition `log_2(8 l/eps) <= l` affects

The theorem's status sentence now attaches `log_2(8 l/eps) <= l` to "the `l`-only form" of
the chart arithmetic. Going through every count, with `Lambda = l + log_2(8 l/eps)`
(`k <= 2 Lambda / log_2 p`):
- (i): **unaffected.** `eps` enters only through `t = ceil(log_2(12 l/eps))`, which the bound
  carries explicitly; no `l`-only form is claimed.
- (ii): **unaffected.** The chart-acquisition count is stated in `k` itself, exactly; the
  per-query and preprocessing counts do not involve `k`.
- (iii), classical chart time `O_c(s^c l^5 + l^6)`: **affected.** Proved under the condition
  (Section 5.2, in fact `O_c(s^c l^4 + l^6)`); in general `O_c(s^c Lambda^2 l^2 + Lambda^4 l^2)`.
- (iii), the chart-gate term that must be added (Section 5.1): **affected** in its `l`-only
  form `O_c(s^c l^5)`; in general `O_c(d Lambda l^3 L) <= O_c(s^c Lambda l^4)` transforms-gates
  plus `O_c(d Lambda l)` oracle calls.
- (iii), core gates `Q_f (l^3 + w) polylog(l/eps)`, solver time `Q_f l^{beta_c} ...`,
  normalizer arithmetic: **unaffected** (`eps` enters only via `Q_f` and the explicit
  `polylog(l/eps)`).
- (iv): **unaffected.**
- All `N`-forms (`O_c(N^{E_W+1})`, `O_c(N^{E_W})`, `O_c(N^{E_W+4+o(1)})`,
  `O_c(N^{E_W+1+max(3,beta_c)+o(1)})`): **unaffected**, because `Lambda <= 2N + 4`
  (`log_2(8 l/eps) <= 3 + log_2 l + log_2(1/eps) <= N + 4`), matching the lemma's own
  `O_c(s^c N^2 + N^4)`.
So the condition can be dropped from the theorem entirely by stating the chart terms of (iii) in
`Lambda`, or kept exactly where the status sentence now puts it; nothing else in the theorem
depends on it.

## 8. What now holds, what is missing, gates

**Exact statement that now holds** (conditional exactly as the theorem says: on `thm:main`, on
`thm:power-sde`(ii) through the combined rule, and for `e_p > 1` on `thm:ring-to-field`(iii)
with its stop rules; AI-checked only):

> Items (i) and (iv) of `thm:bb-envelope`, with the per-prime refinement
> `Q_p <= Q_core(n_p)` (`e_p = 1`) and `Q_p <= sum_{j=0}^{n_p-1} Q_core(n_p - j)` (`e_p > 1`),
> `Q_core(m) = c (m + t) K_c (m+1)^{E_W(c)-1}`; the values `E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143`
> for `c = 2..9`, as maxima over all primes `p > c`, attained at `p = 3, 7, 13, 61, 61, 421, 2521, 2521`;
> the `N`-forms `O_c(N^{E_W(c)+1})` and, when every `e_p = 1`, `O_c(N^{E_W(c)})` for the
> large-prime queries. Item (ii) with `n_p^2` replaced by `min(d, n_p)^2`. Item (iii)'s classical
> chart time under `eps >= 8 l 2^{-l}`, and in general as `O_c(s^c Lambda^2 l^2 + Lambda^4 l^2)`.

**Still missing.**
1. The gate counts of (iii) and of the closing paragraph: they need the three standard facts
   (H1)-(H3) of Section 7 to be *stated* in the paper (with (H1) the one that carries weight:
   the degree of the `QFT_p` compilation in `log p`), and (iii) must add the chart-acquisition
   term. Until then (iii) is **argued**, not proved.
2. `beta_c` is a definition, not a number; the normal-form degree is unstated. Both are
   constants at fixed `c` and do not affect polynomiality.
3. (Closed during this pass.) The ring-operation count of the chart is now `lem:tb-chart`, proved
   in `app:torsion-blackbox`; the chart time of Section 5.2 is therefore proved, under the
   condition `log_2(8 l/eps) <= l` for its `l`-only form (Section 7b).
4. Human review of everything above, including `lem:tb-chart`.

**Claim gates that must stay false** (`research/reductions/rees_hsp_reduction.json` and the
registry): `speedup_claim_allowed`, `independent_review`, `novelty_established`,
`coherent_receiver_implemented`, `general_sde_implemented`, `formal_compiler_checked`. Nothing
here is a speedup, an implementation, a novelty claim or a formal check; it is bookkeeping for a
conditional polynomial bound at fixed class whose constants exceed `2^{1200}`.

**Next hard question.** State and prove, inside `thm:uniform-compilation`(iii), an explicit gate
bound for the approximate `QFT_p` with its degree in `log p` (and the same for `Z/p^e`), so that
(iii) becomes proved rather than argued; the acceptance test is that Section 5.1's `a` is a stated
number at most `3`.

## 9. Proposed paper text

**Status label for all of it: "AI-checked, pending human review."** Every `\ref` below points to
a label that exists in `main.tex` or `appendix-torsion-blackbox.tex` today. The subsection
introduces five new labels of its own (`app:tb-counts`, `lem:tb-count-grade`,
`lem:tb-count-exponent`, `lem:tb-count-prime`, `prop:tb-count-gates`), used only inside it and in
the one-line pointer of Section 9.2. `\operatorname{polylog}` is written out because the paper
defines no `\polylog`. The text proves (i), (ii) (in its corrected form, Section 9.3), (iv) and the
chart time, and proves the gate and time counts under three hypotheses that it states explicitly
(the integrator may instead move those hypotheses into `thm:uniform-compilation`(iii) and
`lem:tb-sylow`(d), where they belong).

### 9.1 New subsection at the end of `appendix-torsion-blackbox.tex`, after `rem:tb-scope` (AI-checked, pending human review)

```latex
%----------------------------------------------------------------------------
\subsection{Proof of the counts of Theorem~\ref{thm:bb-envelope}}
\label{app:tb-counts}
%----------------------------------------------------------------------------

Throughout, $c$ is fixed, $p > c$ is a prime dividing $|G|$, and $n_p$, $e_p$, $M$, $b_M$,
$A_c$, $d$, $k$, $L$, $t$, $K_c$, $e_d(p)$ and $E_W(c)$ are as in Theorem~\ref{thm:bb-envelope}.
The algorithm is the composition of Section~\ref{app:tb-blackbox}: Lemma~\ref{lem:tb-sylow} with
error share $\eps/4$; Lemma~\ref{lem:tb-small-primes}; and, for each $p > c$, the pullback of
Proposition~\ref{prop:black-box}(i), the chart of route~(R2) acquired by Lemma~\ref{lem:tb-kernel}
at $\delta = \eps/(4\ell)$, and then one call of Theorem~\ref{thm:main} on the chart if $e_p = 1$,
or Algorithm~$\mathsf{RtF}$ of Proposition~\ref{prop:tb-recursion} on the chart with
Theorem~\ref{thm:main} as the field solver if $e_p > 1$, every call at error $\eps/(4\ell)$ and
with the arities of Remark~\ref{rem:combined-schedule}. Two elementary facts are used
repeatedly. First, $\prod_{p>c}p^{n_p} \le |G| \le 2^\ell$ with $p \ge c+1$ and $n_p \ge 1$
gives $L = \sum_{p>c} n_p \le \ell/\log_2(c+1)$, $n_p \le \lfloor \ell/\log_2 p\rfloor \le k$, and at
most $L$ such primes. Second, for integers $E \ge 1$ and $t \ge 0$ the polynomial
$\varphi(x) = x(x+t)(x+1)^{E-1}$ has nonnegative coefficients and $\varphi(0) = 0$, so it is
convex on $[0,\infty)$ and therefore superadditive: $\varphi(a)+\varphi(b) \le \varphi(a+b)$ for
$a, b \ge 0$.

\begin{lemma}[Per-grade arity bound]
\label{lem:tb-count-grade}
Under the combined rule of Remark~\ref{rem:combined-schedule}, at every grade $d$ and every
prime $p > c$, $M_d \le C_d\,(g_d+1)^{e_d(p)}$ with $C_d \le d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}$.
Hence, on an $\Fp$-Lie algebra of dimension $m$ and class at most $c$,
$\prod_{d=2}^c M_d \le K_c\,(m+1)^{E_W(c)-1}$, and one call of Theorem~\ref{thm:main} with
error $\eps/(4\ell)$ makes at most
\[
  Q_{\mathrm{core}}(m) \coloneqq c\,(m+t)\,K_c\,(m+1)^{E_W(c)-1}
\]
queries, a bound fixed by public data and nondecreasing in $m$. With Schedule~1 alone the same
holds with $e_d = d\lceil\log_2(d+1)\rceil$.
\end{lemma}

\begin{proof}
Linear grade: $M_d = g_d+1$, $C_d = 1$. Two-level grade, $\kappa_d \ge 2$:
$(\kappa_d-1)g_d + 1 \le (\kappa_d-1)(g_d+1)$, so $M_d \le (\kappa_d-1)(g_d+1)^2$ and
$C_d = \kappa_d - 1 \le d-1$. Schedule~1 at degree $\kappa = \kappa_d \le d$:
$B_\kappa(g_d) = \kappa^{\kappa(\kappa-1)\lceil\log_2(\kappa+1)\rceil/2}(g_d+1)^{\kappa\lceil\log_2(\kappa+1)\rceil}$,
and $x \mapsto x^{x(x-1)\lceil\log_2(x+1)\rceil/2}$ is nondecreasing on $x \ge 1$. In all three cases
$C_d \le d^{d(d-1)\lceil\log_2(d+1)\rceil/2}$, which is at least $d$. Since $g_d \le m$,
$\prod_d M_d \le K_c (m+1)^{\sum_d e_d(p)} \le K_c (m+1)^{E_W(c)-1}$ by the definition of $E_W(c)$.
The call makes at most $c(m + \lceil\log_p(12\ell/\eps)\rceil)\prod_d M_d$ queries by
Theorem~\ref{thm:main} with $\eps' = \eps/(4\ell)$, and $\lceil\log_p(12\ell/\eps)\rceil \le t$
because $p \ge 2$. A socle of class $c' < c$ is processed at $c'$, with a count at most that at
$c$ (Section~\ref{app:tb-ring}). Nothing in the count depends on the oracle's answers.
\end{proof}

\begin{lemma}[The exponents $E_W(c)$]
\label{lem:tb-count-exponent}
Let $E_1(c) = 1 + \sum_{d=2}^c d\lceil\log_2(d+1)\rceil$. For every prime $p > c$ and every
$d \ge 2$, $e_d(p) \le d\lceil\log_2(d+1)\rceil$, with equality if and only if $d \mid p-1$ and
$p < 16\,d^{2d+2}$; when the inequality is strict the difference is at least $2$. Consequently
$E_W(c) = E_1(c)$ if some prime $p < 1024$ satisfies $\operatorname{lcm}(2,\dots,c) \mid p-1$,
and $E_W(c) = E_1(c) - 2$ otherwise. In particular $E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143$
for $c = 2,\dots,9$, attained at $p = 3, 7, 13, 61, 61, 421, 2521, 2521$, against
$E_1(c) = 5, 11, 23, 38, 56, 77, 109, 145$.
\end{lemma}

\begin{proof}
$e_d(p) \in \{1, 2, \kappa_d\lceil\log_2(\kappa_d+1)\rceil\}$ with $\kappa_d \le d$, and
$x \mapsto x\lceil\log_2(x+1)\rceil$ is strictly increasing with value $4$ at $x = 2$; this gives
the inequality, the equality case (Schedule~1 at degree $\kappa_d = d$, which the rule selects
exactly when $p < 16\kappa_d^{2\kappa_d+2}$), and the loss of at least $2$ (two-level loses
$d\lceil\log_2(d+1)\rceil - 2 \ge 2$; a reduced degree $\kappa_d < d$ loses at least
$d\lceil\log_2(d+1)\rceil - (d-1)\lceil\log_2 d\rceil \ge 2$; linear loses at least $3$). The
thresholds $16\,d^{2d+2}$ equal $1024$ at $d = 2$ and exceed $104976$ for $d \ge 3$, so
$1 + \sum_d e_d(p) = E_1(c)$ exactly when $\operatorname{lcm}(2,\dots,c) \mid p-1$ and $p < 1024$.
If no such prime exists, every prime loses at least $2$, and the loss $2$ is attained by any
prime $p \ge 1024$ with $\operatorname{lcm}(2,\dots,c) \mid p-1$ and $p < 16\cdot 3^8$, for
example $p = 2521$ when $c \in \{8, 9\}$; such primes exist by Dirichlet's theorem, and
$E_W(c)$, a maximum of finitely many values, is therefore $E_1(c) - 2$. The listed witnesses are
checked directly: $421 = \operatorname{lcm}(2,\dots,7) + 1$ is prime and below $1024$;
$841 = 29^2$ is the only candidate below $1024$ for $c = 8$; $\operatorname{lcm}(2,\dots,9) = 2520$.
\end{proof}

\begin{lemma}[One Sylow subgroup]
\label{lem:tb-count-prime}
Let $p > c$. After chart acquisition, the queries to $f$ spent on $G_p$ satisfy
$Q_p \le Q_{\mathrm{core}}(n_p)$ if $e_p = 1$, and
$Q_p \le \sum_{j=0}^{n_p-1} Q_{\mathrm{core}}(n_p - j) \le n_p\,Q_{\mathrm{core}}(n_p)$ if $e_p > 1$.
In both cases $Q_p \le c\,K_c\,\varphi(n_p)$ with $E = E_W(c)$. Every local query is one query
of $f$, at most $4\min(d,n_p)(2b_M + A_c)$ multiplications are spent per local query, and at most
$n_p$ core calls are made on every branch.
\end{lemma}

\begin{proof}
For $e_p = 1$ the chart $\mathcal{L}_G = F/\ker\pi$ is an $\Fp$-Lie algebra of dimension $n_p$
and class at most $c$ with oracle $f\circ\bar\Phi$ at one query of $f$ per query
(Section~\ref{app:tb-blackbox}, route~(R2)), and one call of Theorem~\ref{thm:main} is made;
apply Lemma~\ref{lem:tb-count-grade}. For $e_p > 1$, Algorithm~$\mathsf{RtF}$ runs on the chart
with $b = n_p$. By Proposition~\ref{prop:tb-recursion}, the $j$th call ($j = 0, 1, \dots$) is
made only if $S_j \ne K_j$, where $|K_j| \ge p^j$; it runs on the socle of $S_j/K_j$, whose
dimension is the number of cyclic factors of $S_j/K_j$, at most
$\log_p(|\mathcal{L}_G|/|K_j|) \le n_p - j$. So at most $n_p$ calls are made, the $j$th of
dimension at most $n_p - j$, on every branch; each local query is one query of $f$ by
Lemma~\ref{lem:tb-quotient-oracle}. Sum Lemma~\ref{lem:tb-count-grade} and use monotonicity. The
last inequality uses $n_p \ge 1$. For the multiplication count, Lemma~\ref{lem:tb-chart}(b)
gives $n' \le r \le n_p$ chart basis elements with $r = |J| \le d$, so $n' \le \min(d, n_p)$. A local query
computes $\exp(\sum_i x_i\varepsilon_i)$ from the precomputed $\Phi(\tilde\varepsilon_i)$ as $n'$ powers
with exponents below $M$ and $n'-1$ programs $\Pi_+$, at most $n'(2b_M + A_c)$ multiplications as a
straight-line program, doubled for reversible cleanup (Proposition~\ref{prop:black-box}(i)), and
then applies $U_f$ once and runs the evaluation backwards: at most $4n'(2b_M + A_c)$
multiplications. The section $\sigma$ and the socle map $\iota_M$ are public coordinate
arithmetic.
\end{proof}

\begin{proof}[Proof of Theorem~\ref{thm:bb-envelope}(i), (ii) and (iv)]
\emph{(i).} By Lemma~\ref{lem:tb-count-prime} and superadditivity,
\[
  \sum_{p>c} Q_p \le c\,K_c\sum_{p>c}\varphi(n_p) \le c\,K_c\,\varphi(L)
  = c\,K_c\,L\,(L+t)(L+1)^{E_W(c)-1} \le c\,K_c\,(L+t)(L+1)^{E_W(c)} .
\]
The primes $p \le c$ add the $\poly(\log|G_{\le c}|)$ calls of Lemma~\ref{lem:tb-small-primes},
one query of $f$ each. Lemma~\ref{lem:tb-sylow}(d), Lemma~\ref{lem:tb-kernel} and the chart
arithmetic make no query to $f$. If every $e_p = 1$, put $x_p = n_p + 1$ and
$X = \sum_p x_p \le 2L$; superadditivity of $x \mapsto x^j$ ($j \ge 1$) gives
$\sum_p (n_p+t)(n_p+1)^{E-1} \le \sum_p (x_p+t)x_p^{E-1} \le X^E + tX^{E-1} \le 2^E (L+t)(L+1)^{E-1}$,
so the large-prime count is then $2^{E_W(c)}c\,K_c\,(L+t)(L+1)^{E_W(c)-1}$. With $L \le \ell \le N$
and $t \le N + 5$, these are $O_c(N^{E_W(c)+1})$ and $O_c(N^{E_W(c)})$ respectively, and neither
depends on $s$.

\emph{(ii).} The per-query count is Lemma~\ref{lem:tb-count-prime}. Chart acquisition for one
prime costs $(d-s)(m_{[\,]} + 2b_Mq_{[\,]})$ multiplications for the Hall images
(Proposition~\ref{prop:black-box}(i)), $2k\,d\,(2b_M + A_c)$ for the $k$ coherent evaluations of
$\Phi$ with cleanup (Lemma~\ref{lem:tb-kernel}, with $k \ge \min(d,\lfloor\ell/\log_2 p\rfloor) + \lceil\log_p(8\ell/\eps)\rceil$),
and, by Lemma~\ref{lem:tb-chart}(b), for the $m' \le r \le \min(d,n_p)$ chart basis elements, whose
lifts $\tilde\varepsilon_i$ are supported on the $r$ kept indices, at most $r(2b_M + A_c)$
multiplications each, at most $\min(d,n_p)^2(2b_M + A_c)$ in all. Since
$\min(d,n_p)^2 \le d\,n_p \le d\,k$, the total is at most
$(d-s)(m_{[\,]} + 2b_Mq_{[\,]}) + 3k\,d\,(2b_M + A_c)$. Preprocessing is
Lemma~\ref{lem:tb-sylow}(d) at $\eps_{\mathrm{pre}} = \eps/4$.

\emph{(iv).} The steps run in sequence with fresh randomness, and each failure bound is
conditional on correct inputs, so a first-error union bound gives total failure at most the sum
of the shares: $\eps/4$ for Lemma~\ref{lem:tb-sylow}(d); $\eps/4$ for compiling the exact
small-prime transforms of Lemma~\ref{lem:tb-small-primes} into the finite gate set, by
Lemma~\ref{lem:hybrid} with every $S_j$ the whole space; at most $L \le \ell$ charts, each
$\delta = \eps/(4\ell)$ by Lemma~\ref{lem:tb-kernel}; and, by Lemma~\ref{lem:tb-count-prime}, at
most $\sum_{p>c} n_p = L \le \ell$ core calls in all, each at error $\eps/(4\ell)$, which for a
prime with $e_p > 1$ is Proposition~\ref{prop:tb-recursion} with per-call error $\eps/(4\ell)$
and $b = n_p$. The stop rules and the per-call time-out of Proposition~\ref{prop:tb-recursion}
make the counts above hold on erroneous branches as well.
\end{proof}

\begin{proposition}[Gates and classical time; proof of Theorem~\ref{thm:bb-envelope}(iii)]
\label{prop:tb-count-gates}
Assume, in addition to the results cited by Theorem~\ref{thm:bb-envelope}:
\textup{(H1)} a single-coordinate quantum Fourier transform over $\Fp$, or over $\mathbb{Z}/p^e$ on
at most $\ell$ bits, to isometry error $\eta$ compiles into $O(\ell^3\operatorname{polylog}(1/\eta))$
gates (this fixes the degree left open in Theorem~\ref{thm:uniform-compilation}(iii));
\textup{(H2)} a field operation modulo $p$ costs $O(\log^2 p)$ gates; \textup{(H3)} one run of
Shor's order finding or factoring on $O(\ell)$-bit integers costs $O(\ell^3)$ gates. Then, with
every oracle call counted once:
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item the core calls use $O_c\bigl(Q_f(\ell^3 + w)\operatorname{polylog}(\ell/\eps)\bigr)$ gates,
  where $Q_f$ is the number of queries of~(i) for the primes $p > c$;
  \item chart acquisition uses, summed over $p > c$,
  $\sum_{p>c}\bigl[(d-s)(m_{[\,]} + 2b_Mq_{[\,]}) + 2k\,d\,(2b_M + A_c)\bigr]$ multiplication
  calls and $\sum_{p>c} k\,d$ transforms over $\mathbb{Z}/p^{e_p}$, that is
  $O_c(s^c\ell^5)$ gates when $\log_2(8\ell/\eps) \le \ell$;
  \item order finding and factoring use $O(s\ell^3\log(s/\eps))$ gates;
  \item classical time is $O_c(s^c\Lambda^2\ell^2 + \Lambda^4\ell^2)$ bit operations for the
  charts, where $\Lambda = \ell + \log_2(8\ell/\eps)$ (so $O_c(s^c\ell^4 + \ell^6)$ when
  $\Lambda \le 2\ell$), plus $\poly(\ell)$ normal-form arithmetic per normalizer step with at most
  $L \le \ell$ steps, plus $Q_f\,\ell^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$
  for the diagonal-equation solvers, where $\hat\beta_c$ is the least exponent with every solver
  call at arity $M_d$ and at most $a$ equations running within
  $M_d(a+1)^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$ (it exists because the
  solvers of Theorems~\ref{thm:is-import} and~\ref{thm:power-sde}(ii) are polynomial in
  $M_d \le K_c(a+1)^{e_d}$).
\end{enumerate}
In the input size $N = s\ell + w + \log(1/\eps)$, (a)--(c) are $O_c(N^{E_W(c)+4+o(1)})$ and the
total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$, provided the degree of the
normal-form arithmetic is at most $E_W(c)+1+\max(3,\hat\beta_c)$.
\end{proposition}

\begin{proof}
\emph{(a).} Fix a core call of dimension $m \le n_p$, cover dimension $n \le c\,n_p$, with
$S$ terminal samples and $P = \prod_d M_d$ leaves per sample, so $Q^{\mathrm{call}}_f = cSP$
(Section~\ref{sec:recursion}). The tree of one terminal sample has $P$ leaves,
$\prod_{d'<d}M_{d'}$ merge nodes at stage $d$, and $\sum_{d}\prod_{d'\le d}M_{d'} \le (c-1)P$ child
slots. A slot is one clean controlled right translation: four BCH evaluations
(Theorem~\ref{thm:uniform-compilation}(ii)) of at most $c^4$ brackets of $O(n^3)$ field
operations each (Theorem~\ref{thm:uniform-compilation}(i)), plus $O(n^2)$ field operations for
$\sigma$ and $\delta_s$: $O_c(n_p^3)$ field operations, which by~(H2) and $n_p\log_2 p \le \ell$
is $O_c(\ell^3)$ gates. A leaf makes $c$ queries, each with $O_c(n_p(2b_M + A_c)) = O_c(\ell)$
multiplication calls (Lemma~\ref{lem:tb-count-prime}), $O(w)$ gates for the label register and
$O(n)$ field operations for $E_s$. Transforms: $n$ per leaf, $2g_d \le 2n_p$ per slot, $D_{d-1} \le n$
per merge node and $m$ per readout (Theorem~\ref{thm:uniform-compilation}(iii)), so $O_c(n_p)$
per slot or leaf, each at error $\eta = \eps/(12\ell N_{\mathrm{instr}}q_{\max})$ with
$\log(1/\eta) = O_c(\log(\ell/\eps))$, since $N_{\mathrm{instr}} \le 2Q_f^{\mathrm{call}}$ is
$\ell^{O_c(1)}(\ell+t)$ and $q_{\max} \le \poly_c(\ell)$. By~(H1) and $n_p \le \ell/\log_2 p$ a
transform over $\Fp$ costs $O((\log p)^3\operatorname{polylog}(\ell/\eps))$, so the transforms of
a slot cost $O_c(\ell(\log p)^2\operatorname{polylog}(\ell/\eps)) \le O_c(\ell^3\operatorname{polylog}(\ell/\eps))$.
Slots and leaves number at most $Q_f^{\mathrm{call}}$ each; sum over calls and primes.
\emph{(b).} The multiplication calls are those of~(ii); the transforms are the $k$ samples of
Lemma~\ref{lem:tb-kernel}, $d$ coordinates each, on $b_M \le \ell$ bits. With
$k \le 2\Lambda/\log_2 p$, $b_M \le 2e_p\log_2 p$ and $\sum_p e_p \le L \le \ell$:
$\sum_p k\,d\,b_M \le 4d\Lambda\ell$ multiplication calls and, by~(H1),
$\sum_p k\,d\,\ell^3 \le 2d\Lambda\ell^3\sum_p 1/\log_2 p \le 2d\Lambda\ell^4$ gates; with
$d \le c\,s^c$ and $\Lambda \le 2\ell$ this is $O_c(s^c\ell^5)$.
\emph{(c).} Lemma~\ref{lem:tb-sylow}(d) runs $O(\log(s/\eps))$ order-finding pairs and one
factorization per generator; apply~(H3).
\emph{(d).} Lemma~\ref{lem:tb-chart} uses $O_c(dk^2 + k^4)$ ring operations modulo $p^{e_p}$ per prime, each
$O(b_M^2)$ bit operations; with the bounds on $k$ and $b_M$ above, $k^2b_M^2 \le 16\Lambda^2e_p^2$
and $k^4b_M^2 \le 64\Lambda^4e_p^2$, and $\sum_p e_p^2 \le L^2 \le \ell^2$. Normalizer steps:
Proposition~\ref{prop:tb-recursion}, at most $n_p$ rounds per prime. Solvers: a core call has at
most $S\sum_d\prod_{d'<d}M_{d'}$ solver calls and $\sum_d(\prod_{d'<d}M_{d'})M_d \le (c-1)P$, so
its solver time is at most $(c-1)SP(n_p+1)^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)
\le Q_f^{\mathrm{call}}\ell^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$, using
$n_p + 1 \le \ell$. \emph{Exponents.} $Q_f = O_c(N^{E_W(c)+1})$ by~(i), $\ell^3 + w \le N^3$,
$\operatorname{polylog}(\ell/\eps) = N^{o(1)}$ since $\log(1/\eps) \le N$; $s^c\ell^5 \le N^{\max(c,5)}$,
$s\ell^3\log(s/\eps) \le N^4$, $s^c\ell^4 + \ell^6 \le N^{\max(c,6)}$, $\Lambda \le 2N+4$; and
$E_W(c) \ge \max(c, 5)$ for $c \ge 2$ because every $e_d \ge 1$.
\end{proof}
```

### 9.2 One-line replacement for the sketch's pointer in `main.tex` (AI-checked, pending human review)

Replace, in the `Proof sketch` of `thm:bb-envelope`, the sentence
```latex
The full accounting and an exact check of the exponents are in \file{research/audits/reviews/2026-11-02-rees-bb-envelope.md}.
```
by
```latex
Appendix~\ref{app:tb-counts} proves the counts: Lemmas~\ref{lem:tb-count-grade}--\ref{lem:tb-count-prime} give~(i), (ii) and~(iv), Lemma~\ref{lem:tb-count-exponent} the values of $E_W(c)$ for every prime, and Proposition~\ref{prop:tb-count-gates} the gate and time counts of~(iii) under the three stated compilation hypotheses.
```
and, in the theorem's last paragraph, replace the current status sentence
```latex
The chart arithmetic in~(ii)--(iii) is Lemma~\ref{lem:tb-chart} of Appendix~\ref{app:torsion-blackbox}, under $\log_2(8\ell/\eps) \le \ell$ for its $\ell$-only form, and the summation into~(i), the gate and time counts of~(iii) and the exponents above are \emph{argued} in the proof sketch below, not proved in this paper.
```
by
```latex
The chart arithmetic in~(ii)--(iii) is Lemma~\ref{lem:tb-chart} of Appendix~\ref{app:torsion-blackbox}, under $\log_2(8\ell/\eps) \le \ell$ for the $\ell$-only form of the chart terms of~(iii) (no other count depends on this condition); the summation into~(i), the exponents and the error split are proved in Appendix~\ref{app:tb-counts}; the gate and time counts of~(iii) are proved there under the compilation hypotheses (H1)--(H3) of Proposition~\ref{prop:tb-count-gates}, which this paper states but does not prove.
```

### 9.3 Corrections to the statement that the proof requires (AI-checked, pending human review)

Without these two changes the subsection of Section 9.1 does not prove the theorem as printed.

**(ii), middle term.** Replace
```latex
+ n_p^2(2b_M + A_c) \le (d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 3k\,d\,(2b_M + A_c)
```
by
```latex
+ \min(d,n_p)^2(2b_M + A_c) \le (d-s)(m_{[\,]}+2b_Mq_{[\,]}) + 3k\,d\,(2b_M + A_c)
```
(the printed inequality fails for $G = C_{27}$, $s = 1$, $\eps = 1/2$: $n_p^2 = 9 > kd = 7$).

**(iii), first sentence.** Replace
```latex
Quantum gates number $O_c\bigl(Q_f(\ell^3 + w)\,\poly\log(\ell/\eps)\bigr)$, plus the gates of~\cite{ImranIvanyos2023} and of order finding and factoring, with each oracle call counted once.
```
by
```latex
Under the compilation hypotheses (H1)--(H3) of Proposition~\ref{prop:tb-count-gates}, the core calls use $O_c\bigl(Q_f(\ell^3 + w)\operatorname{polylog}(\ell/\eps)\bigr)$ gates, chart acquisition uses the multiplication calls of~(ii) and $\sum_{p>c}k\,d$ transforms over $\mathbb{Z}/p^{e_p}$, in all $O_c(s^c\ell^5)$ gates when $\log_2(8\ell/\eps) \le \ell$, and order finding and factoring use $O(s\ell^3\log(s/\eps))$; the gates of~\cite{ImranIvanyos2023} are added separately, and each oracle call is counted once.
```
(the printed sentence omits the chart gates, which are $\Theta_c(s^c)$ and exceed
$Q_f(\ell^3+w)$ already for $G = C_3$ with $s \ge 2$ redundant generators, and it needs (H1),
whose degree Theorem~\ref{thm:uniform-compilation}(iii) does not state).

If the owner prefers not to add hypotheses to a theorem statement, the alternative is referee
P10's: keep (iii) qualitative ("polynomial in $N$ for fixed $c$") and move the exponents
$E_W(c)+4$ and $E_W(c)+1+\max(3,\hat\beta_c)$ to a remark headed "Computed exponents", citing
Proposition~\ref{prop:tb-count-gates}. Items (i), (ii) (corrected) and (iv) need no such retreat:
they are proved.

## Next

- Integrator: insert Section 9.1 at the end of `appendix-torsion-blackbox.tex`, apply 9.2 and
  9.3, rebuild, and check that every `\ref` resolves (`grep -c 'tb-count' main.pdf.log` or the
  `.aux`); acceptance: no undefined references and the five new labels defined once each.
- Owner decision: whether (H1)-(H3) go into `thm:uniform-compilation`(iii) and `lem:tb-sylow`(d)
  (preferred; then `prop:tb-count-gates` needs no hypotheses of its own) or stay in the appendix.
- Open: an explicit degree for the approximate `QFT_p` in `log p` from the cited constructions
  (Kitaev; Cleve-Watrous), read from the sources, not assumed; until then (iii) is argued.


