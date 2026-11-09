# Square gap, round 11: a cubic lower bound on E_2 (twisted Stepanov) and the literature comparison

AI-only report (2026-11-09), pending human review. No paper file was edited. Scripts and outputs
are in `2026-11-09-rees-square-gap-stepanov/` (all run with `nice -n 19 /opt/anaconda3/bin/python`,
seconds to minutes each). Setting and notation as in `2026-11-05-rees-square-gap-attack.md` §1:
$\kappa \ge 2$, $p \equiv 1 \pmod\kappa$, $h = (p-1)/\kappa$, $Q_m = \xi^m Q_0$, $\zeta = \xi^h$, a two-level
contraction is $(\alpha,\beta)$ with $\alpha_j + \beta_i \in Q^\circ_{-(i+j)}$ and $\alpha_0 + \beta_0 \ne 0$; $\varepsilon = \operatorname{ind}(-1)$.

## 0. Verdict

- **Square gap: still open.** Nothing here lowers $T_A$ or any threshold, and no exponent below
  $\kappa$ is proved.
- **Upper side (§3).** A $\mathrm{PGL}_2$ normal form, and a separable-type certificate that none of
  O1, O2 or Chebotarev excludes.
  - At κ = 4 its pair-signed form certifies from $p = 137$ (plain form: $181$, then every
    tested prime from $197$), below the O1 barrier $203$.
  - Rigorously, with Weil only, it reaches just $\approx T_A^2$.
  - Under the open hypothesis OSC it would give $\kappa^{(\kappa+1)/2+o(1)}$.
  - Its heuristic threshold is about $\kappa^{\kappa/2+9/4}$.
  - Its missing input, square-root cancellation of type sums over (C1) orbits, is open.
  - This is the first identified proof route not excluded by a known barrier. It is not a
    proof.
  - **κ = 5 (§8, exact computation at single primes).** PW_pair < 1 at every tested prime
    821–2311 (first at 641), PW < 1 at every tested prime 1231–2311, all far below the O1
    barrier 2628 and $T_A(5) \approx 1.25\cdot10^4$. (N) and (L) look bounded. **(H) as stated is
    contradicted by the data:** the $m = 6$ classes (3,3) and (2,4) carry a $c/p$ bias rather
    than square-root cancellation, so $B_H$ grows like $p^{2.3}$.
  - **OSC′ made precise (§11).** The $c/p$ bias is not a boundary term (exact decomposition; it
    sits in the complete-sum part). OSC′ is stated per class and per group (§11.8: $m_0 = 6$ at
    κ = 4, 5, 6, decay $\le B_D\kappa^2/p$ above). Either form gives the exponent
    $(1/2+o(1))\kappa < \kappa$, namely
    $\kappa/2 + \kappa/(2\ln\kappa) + \log_\kappa\max(B_L,\sqrt{B_D}) + O(1)$. It stays below κ
    unless $B_L \ge \kappa^{(1/2-o(1))\kappa}$ or $B_D \ge \kappa^{(1-o(1))\kappa}$ (κ! is enough),
    or the constants grow faster than any power of $1/\lambda$, or $m_0$ grows past ≈ κ. This is
    conditional: OSC′ is unproved for every κ, and
    its bounded-support reading is false. At typical primes the group constants do not grow with
    κ (κ = 4–6 at equal p). Spike primes are the live obstruction: at κ = 6, $p = 1933$ the
    estimated certificate value is 7.2, with $B_L = 1.2$ and $B_D = 3.7$, 3–11× the typical
    values.
  - **(N) (§9).** Proved without Weil: (C1) configurations exist from $p \approx \kappa^\kappa/(2e)$
    asymptotically (Theorem C; first certified κ = 5: 1451, κ = 6: 20233, below pigeonhole).
    Full-space term-by-term certificates for (N) are barred up to $(\kappa-1)\kappa^\kappa$ (O1-N).
    A κ = 7 Monte Carlo in the OSC regime ($\lambda = 0.15$–$0.31$) gives $N_1/\mu_1 = 0.62$–$1.07$,
    consistent with the 4-cycle heuristic.
- **Proved (new in this form; refereed by an independent AI agent, verdict CORRECT, pending human
  review): Proposition 1.** If a contraction has $z$ zero cells then
  $\kappa(\kappa-1) - z \le h + \kappa - 2$. Hence every prime $p \equiv 1 \pmod\kappa$ with
  $p \le \kappa^3 - 3\kappa^2 + 2\kappa$ lies in $E_2(\kappa)$. This replaces the quadratic lower end
  $\kappa^2 - 3\kappa + 3$ of `prop:app-s2-cyclotomic`(ii) by a cubic one. It bounds $E_2(\kappa)$ from
  below only.
- **Proved (Lemma 2, zero cells).** Two distinct zero cells $(i,j),(i',j')$ satisfy
  $(i-j)-(i'-j') \equiv \varepsilon$; so $z \le 2$ when $\varepsilon \ne 0$, and then $h \ge \kappa^2 - 2\kappa$.
- **Tightness [finite computation].** Equality holds at $(\kappa,p) = (4,41)$ (all four normalised
  contractions have $z = 0$ and $F = c\prod_i(x-\beta_i)^3$), at $(3,7)$ with $z = 3$, and at $(2,3)$.
  So the constant and the coefficient of $z$ cannot be improved, and a Hanson-Petridis-strength
  twisted bound $\kappa^2 \le h + z$ is false (it would exclude $p = 41$, which has contractions).
- **Literature (§4).** The best comparison to cite is the $n$-e.c. (adjacency-pattern) threshold
  of Paley graphs: Weil gives $q > n^2 2^{2n-2}$, counting suggests $\approx 2^n$, and no result
  lowering the base $4$ was found. This is the same first-moment versus square-root shape as the
  square gap.

## 1. Proposition 1 (twisted Stepanov bound) [proved]

**Statement.** Let $(\alpha,\beta)$ be a two-level contraction at $(p,\kappa)$, $\kappa \ge 2$, with $z$ zero
cells. Then $\kappa(\kappa - 1) - z \le h + \kappa - 2$. Since $z \le \kappa$ (`lem:app-s2-two-rows`: the
$\alpha_j$ are distinct and the $\beta_i$ are distinct, so each row has at most one zero cell),
$p \ge \kappa(\kappa^2 - 2\kappa + 2 - z) + 1 \ge \kappa^3 - 3\kappa^2 + 2\kappa + 1$.

**Proof.** A nonzero cell lies in $Q_{-(i+j)}$, so $(\alpha_j + \beta_i)^h = \zeta^{-(i+j)}$. The point
is that the pattern is separable: $\zeta^j(\beta_i + \alpha_j)^h = \zeta^{-i}$ does not depend on $j$
(the earlier dismissal of Hanson-Petridis in TH3 §5 treated the cosets as unrelated). Put
$m = \kappa - 1$, $N = h + m - 1$, and $c_j = 1/\prod_{j' \ne j}(\alpha_j - \alpha_{j'})$, so every
$c_j \ne 0$ and $\sum_j c_j\alpha_j^s = 0$ for $0 \le s \le \kappa - 2$. Let
$F(x) = \sum_j c_j\zeta^j(x + \alpha_j)^N$.

(i) Row $i$ without a zero cell. For $k \le m - 1$, $N - k = h + (m-1-k)$ and
$F^{(k)}(\beta_i) = N^{(k)}\zeta^{-i}\sum_j c_j(\beta_i + \alpha_j)^{m-1-k} = 0$, since the last sum is a
polynomial in the moments $\sum_j c_j\alpha_j^s$, $s \le \kappa - 2$.

(ii) Row $i$ with its zero cell in column $j_0$. The $j_0$ term is $0$ in every derivative of order
$k \le m - 1$ (because $N - k \ge h \ge 1$); in the formula of (i) it would contribute $0^{m-1-k}$,
which matters only at $k = m - 1$. So $F^{(k)}(\beta_i) = 0$ for $k \le m - 2$ and
$F^{(m-1)}(\beta_i) = -N^{(m-1)}\zeta^{-i}c_{j_0} \ne 0$ (the factors of $N^{(m-1)}$ lie in $[h, N]$, and
$N < p$).

(iii) Since $m < p$, vanishing of $F, \dots, F^{(k-1)}$ at $b$ means $(x - b)^k \mid F$. $F \not\equiv 0$:
$N < p$ makes every $\binom{N}{s}$ nonzero mod $p$, the vector $(c_j\zeta^j)$ is nonzero, and the
Vandermonde rows $s \le \kappa - 1 \le N$ are independent. The $\beta_i$ are distinct. Counting roots
with multiplicity, $m\kappa - z \le \deg F \le N = h + \kappa - 2$. $\square$

The condition $\alpha_0 + \beta_0 \ne 0$ is used only through `lem:app-s2-two-rows` (distinct
$\alpha_j$, needed for $c$, and distinct $\beta_i$). The choice of $\xi$ does not matter: another
generator relabels rows and columns and replaces $\zeta$ by a power.

## 2. Lemma 2 (zero cells) [proved]

Let $(i,j)$ and $(i',j')$ be distinct zero cells, so $i \ne i'$ and $j \ne j'$, $\alpha_j = -\beta_i$ and
$\alpha_{j'} = -\beta_{i'}$. Then cell $(i,j') = \beta_i - \beta_{i'} \ne 0$ lies in $Q_{-(i+j')}$, and cell
$(i',j) = -(\beta_i - \beta_{i'})$ lies in $Q_{\varepsilon - (i+j')}$ and in $Q_{-(i'+j)}$. So
$(i-j) - (i'-j') \equiv \varepsilon$. With three zero cells of diagonal indices $d_1,d_2,d_3$, the pairs
give $d_1 - d_3 \equiv 2\varepsilon \equiv 0$ and $d_1 - d_3 \equiv \varepsilon$, so $\varepsilon = 0$. Hence $z \le 2$
when $\varepsilon \ne 0$ (that is, $\kappa$ even and $h$ odd), and when $\varepsilon = 0$ all zero cells
lie on one diagonal $i - j \equiv \mathrm{const}$. With Proposition 1: for $\varepsilon \ne 0$,
$h \ge \kappa^2 - 2\kappa$. At $\kappa = 4$ this adds $29$ to the primes $5,13,17$ certified by the
cubic bound. $37$ and $53 \in E_2(4)$ stay unexplained by these arguments.

## 3. Upper-side attack this round

From an independent AI attack agent; scripts and outputs in
`2026-11-09-rees-square-gap-stepanov/types/`. The parent re-derived Theorem A and Proposition B and
reran `sep_types.py 4 193 197 229`, which reproduced the κ = 4 ratios. Everything else is the
agent's report and has had no second check. These results concern $E_2'(\kappa)$, contractions
with every cell nonzero, which is a subset of the contractions counted by $E_2$, so
$E_2(\kappa) \subseteq E_2'(\kappa)$. Write $s_j = \alpha_j$, $t_i = -\beta_i$.

- **Theorem A (PGL$_2$ normal form) [proved; parent re-derived].** $(\alpha,\beta)$ is an
  all-nonzero contraction iff (C1) $\chi(s_j - t_i) = \varphi_j\psi_i$ factors, equivalently every
  mixed cross ratio $\frac{(s-t)(s'-t')}{(s-t')(s'-t)}$ is a $\kappa$-th power, and (C2) $\varphi$, $\psi$
  are bijections onto $\mu_\kappa$. Because $gs - gt = \det g\,(s-t)/((cs+d)(ct+d))$, (C1) is
  $\mathrm{PGL}_2(\mathbb{F}_p)$-invariant, and changing the chart only twists $\varphi,\psi$ by
  $1/\chi(\cdot - z)$. So the problem is: $2\kappa+1$ points $(S,T,z)$ on $\mathbb{P}^1(\mathbb{F}_p)$ with
  $(S,T)$ in (C1) and a bijective ("rainbow") chart type at $z$. Counts agree between two
  independent parametrizations at eight $(\kappa,p)$ with $\kappa \in \{3,4\}$ (`orbit_check.out`).
- **Proposition B (pigeonhole) [proved; parent re-derived].** (C1) configurations exist for
  $p > (\kappa-1)\kappa^{\kappa-1} + \kappa - 1$. Put one $\alpha$-point at $\infty$; then $\kappa$ points $t$
  sharing one index profile over the other $\kappa-1$ points suffice. This does not give a
  contraction.
- **Proposition D (type reduction) [proved].** Since $-(i+j)$ is separable, the
  contraction count depends on the $\kappa^{\kappa^2-1}$ frequency sums only through $\kappa^{2\kappa-2}$
  separable-type sums $\hat F(\rho)$, and these are averaged over the row-column orbit of the
  bijective type with permanent weights.
  - On the full space O1 still applies, since the overfull row-constant pattern is separable.
  - On the open stratum (distinct $\alpha$, distinct $\beta$, no zero cell) the certificate is
    not a function of at most $\kappa-1$ column counts, so O2 does not apply, and Theorem 2 is
    irrelevant.
  - **It is the first certificate class found that none of O1, O2 or Theorem 2 excludes.**
- **κ = 4 certificate values [finite computation; parent reran five primes].** The
  permanent-weighted ratio PW is $1.652, 0.906, 1.013, 0.827, 0.613$ at
  $p = 137, 181, 193, 197, 229$. The correction from `types-proof/REPORT.md` stands: PW first
  certifies at $p = 181$, fails at $193$, and holds at every tested prime from $197$ to $509$.
  The pair-signed version PW_pair, proved valid in `types-proof/REPORT.md` §3, certifies at every
  tested prime from $p = 137$. Both are below the O1 barrier $2^{-1/3}4^4 \approx 203$. The full-frequency hybrid certificate
  of `app:sde-side-barrier` still fails at $1009$. At κ = 3 the certificate fires from $p = 43$.
  These are exact values at those primes, not an asymptotic statement, and $E_2(4)$ is already
  known exactly.
- **Heuristic threshold of the type certificate [heuristic].** Low-support classes have
  $|\hat F|/\hat F(0) \approx \kappa/p$, which costs only $\mathrm{poly}(\kappa)$. Generic classes sit at the
  random-phase-over-orbits size. Together these suggest about $\kappa^{\kappa/2+9/4}$, near the
  observed scale. The missing input is square-root cancellation of $\hat F(\rho)$ over (C1)
  orbits, and that is open. κ = 5 data in the relevant range was not obtained (machine load
  near 300).
- **Angle (a), cohomology [proved in part; argued in part].**
  - [proved] The twisted covers are geometrically isomorphic, so any certificate built from
    twist-invariant cohomological data (Betti numbers, weights, monodromy, eigenvalue moduli)
    gives every pattern the same bracket. That is O1 again, but covering all such data.
  - [argued] Using $|\chi| = (n-3)!$ for tame Kummer sheaves on $M_{0,n}$ (cited, not
    re-derived), the total Betti number is at least $\kappa^{\kappa^2-1}(2\kappa-2)!$. Deligne's bound
    is then weaker than the trivial bound across the whole gap.
- **Angles (b), (c) [argued negative].**
  - Exact multiplicative factorisations of the cells are impossible.
  - Brownawell-Masser excludes positive-dimensional families with all cross ratios $\kappa$-th
    powers.
  - Every structured law for $\beta$ that was tried ends either in the O2 regime or in a rainbow
    step costing at least $T_A$.
  - Proposition C: a single (C1) configuration plus a one-variable Weil bound certifies a
    rainbow chart only at about $1.2\cdot10^7$ for κ = 4.
- **Strongest limitation.** Even the existence of (C1) configurations is unproved below the
  pigeonhole bound $(\kappa-1)\kappa^{\kappa-1}$. Expanding (C1) back into characters brings back
  the $\kappa^{\kappa+1}$-type loss.
- **κ = 5 sweep [finite computation; `types/orbit_k5.out`, `types/orbit_k5_sweep.out`].**
  - PW values:

    | p | 271 | 311 | 401 | 521 |
    |---|---|---|---|---|
    | PW | 18.1 | 9.34 | 4.49 | 1.95 |

  - Mean bucket size $p/5^4$ is below 1 at all four primes.
  - Between 401 and 521, PW decays roughly like $p^{-3}$. If that continues, PW < 1 near
    $p \approx 640$ [heuristic extrapolation], against the O1 barrier 2628 and $T_A(5) \approx 1.25\cdot10^4$.
  - Superseded by §8, which extends the sweep to 2311 with a validated C kernel.
- **Second agent pass (`types-proof/REPORT.md`).**
  - [proved] The certificate is valid (Theorem 1 there; the identity is checked to $10^{-11}$).
  - [proved] Pair classes satisfy $n\hat F/\hat F(0) = -\kappa - R$ with $|R| \le \kappa - 2$ (exact
    two-point bijection).
  - [proved mod Weil] Every class satisfies $|\hat F|/\hat F(0) \le ((m-2)\sqrt p + 2\kappa - m)/n$.
  - [proved mod Weil] Hence the certificate is rigorous for $p \ge T_{\mathrm{abs}}(\kappa) \approx T_A^{2+o(1)}$,
    which covers nothing new. The loss is the permanent weight $\approx (e\kappa)^\kappa$.
  - The clean open hypothesis is **OSC(B)**: a (C1)-count lower bound (N), a $1/p$ bias for
    low-support classes (L), and square-root cancellation over (C1) orbits (H). It would give
    $T = \kappa^{(\kappa+1)/2+o(1)}$, for example $3450$ at κ = 5 against $T_A(5) = 1.25\cdot10^4$.
  - The κ ≤ 4 data have mean bucket size $\gtrsim 0.3$, so they do not test OSC in its regime.
- **Next hard question (updated after §11).** The boundary-term route is closed: there is no
  boundary term to prove (§11.1). Prove (L′) of OSC′ for the (2,2) classes at one κ: an
  $O(1)$ bound for the (C1)-average of complete character sums of size $O(\sqrt p)$. On the data
  side, decide whether the spike-prime constants stay $\kappa^{o(\kappa)}$ (or grow at most
  like a fixed power of $1/\lambda$) as λ falls to $\lambda_T$; for κ ≥ 8 that needs a sampler
  that builds (C1) configurations directly (§11.9). (C1) existence for $p = o(\kappa^\kappa)$ is
  proved down to $\kappa^\kappa/(2e)$ only, which is still $\Theta(\kappa^\kappa)$.

## 4. Literature (web; sources seen by a literature agent, extracts in its scratch folder)

- Paley clique number, all $p$: still $(1/2 + o(1))\log_2 p$ (Cohen 1988; Magsino-Mixon-Parshall
  arXiv:1907.05971 eq. (1); Kunisky arXiv:2303.16475 §1.7). Infinitely many $p$: Graham-Ringrose
  $c\log p\log\log\log p$ (seen only as cited). No almost-all-$p$ improvement found.
- Residue patterns: Peralta (Math. Comp. 58 (1992)) counts $x$ with a prescribed quadratic pattern on
  $x + a_1, \dots, x + a_t$ as $p/2^t \pm t(3 + \sqrt p)$, so existence from $p \gtrsim t^2 4^t$. No
  peer-reviewed improvement to $C^t$ with $C < 4$ was found (two unvetted arXiv claims, Carella
  arXiv:2011.11054 and Shivarajkumar arXiv:2111.05219, are not relied on).
- Paley $n$-e.c. property: Weil gives $q > n^2 2^{2n-2}$ (Bonato survey Thm 4, citing
  Bollobás-Thomason and Blass-Exoo-Harary); no lowering of the base $4$ found. Best comparison.
- Hanson-Petridis arXiv:1905.09134 Thm 1.2 covers one coset only; no published twisted
  (separable-pattern) version was found. Proposition 1 is the basic constant-coefficient Stepanov
  bound in a twisted setting; it may be folklore, and no priority is claimed.
- Unverified inference by the literature agent, recorded and not used: the new Ramsey bounds
  ($R(k) \le 3.8^{k+o(k)}$, arXiv:2407.19026) give $\omega(P_p) \ge (0.52 - o(1))\log_2 p$ for all $p$ by
  self-complementarity, beating the Weil base by combinatorics. No analogue for prescribed
  (non-monochromatic) patterns such as (R) is known.

## 5. Data check [finite computation]

`e2dfs.py` (normalised DFS, $\beta_0 = 0$, $\alpha_0 = 1$) reproduces $E_2(4) = \{5,13,17,29,37,53\}$ and
$E_2(5) = \{11,\dots,181\}$, and finds that every prime $p \equiv 1 \pmod\kappa$ up to $180$ ($\kappa = 6$) and
up to $270$ ($\kappa = 7$) lies in $E_2(\kappa)$; the cubic bounds $120$ and $210$ sit inside these
ranges. `stepanov_check.py` checks, for every normalised contraction with $\kappa \le 6$ and
$p \le 200$ ($\kappa \le 4$: $p \le 120$), the moment identities for $c$, the exact root orders of $F$
(at least $\kappa - 1$ in rows without a zero cell, exactly $\kappa - 2$ in rows with one), and the
inequality: no failure. `zero_structure.py` checks Lemma 2 on all contractions found.

## 6. Claim gates that stay false

- Square gap closed, or any threshold $o(\kappa^\kappa)$ proved: **false**.
- Proposition 1 changes $T_A$, $T_S$, Table `tab:app-s2-thresholds`, $E_W(c)$ or Table
  `tab:main-regimes`: **false** (it only enlarges the proved part of $E_2(\kappa)$).
- Proposition 1 is human-reviewed: **false**.
- The type certificate (§3) is proved for any infinite family of $(\kappa,p)$, or its heuristic
  $\kappa^{\kappa/2+9/4}$ is proved: **false**. O1 or O2 is refuted: **false** (the type
  certificate lies outside their hypotheses).
- OSC or OSC′(B) is proved for any κ, or (H) is disproved in general: **false** (finite data at
  κ = 4–7 only).
- Any exponent below κ is proved: **false** (§11.8 derives $(1/2+o(1))\kappa$ from OSC′(B), which
  is unproved).
- The threshold model `osc-mc/model_threshold.py`, or any finite crossing, is a proof: **false**.
- A Monte Carlo PW_pair below 1 is a certificate: **false** (sampling estimates only).
- Pre-fix Monte Carlo values of weak (high-support) bins are measurements: **false** (upper
  estimates, §11.3).
- Per-class κ = 6 or κ = 7 OSC′ constants are bounds: **false** (not resolved, §11.6).
- A spike-prime invariant is known: **false** (§11.5, §11.6).
- PW_pair < 1 for every $p \ge 821$ at κ = 5, or any statement for $p \in [2311, 2628]$: **false**.
- The κ = 5 numbers have a second independent implementation beyond the exact F-array match
  with `orbit_types_fast` and `sep_types`: **false**.
- Theorem C gives contractions: **false** (it gives (C1) configurations only).

## 7. Proposed paper text (NOT applied; the integrator owns `main.tex`)

`appendix-schedule2.tex`, after Proposition `prop:app-s2-cyclotomic`, add a proposition with the
statement and proof of §1 and the zero-cell lemma of §2, and change the sentence in
`appendix-sde-side.tex` "every prime $p \equiv 1 \pmod\kappa$ with $p \le \kappa^2 - 3\kappa + 3$ lies in
$E_2(\kappa)$" to "with $p \le \kappa^3 - 3\kappa^2 + 2\kappa$", citing the new proposition (AI-checked,
pending human review).

## 8. κ = 5 certificate values (added later in the same pass) [computed]

`types/orbit_types.py 5 p`, run under `nice -n 19`, gave the output in `types/orbit_k5_sweep.out` (plus `types/orbit_k5.out`). Each prime took 0.5–1.2 h at a load average near 300.

| p | 271 | 311 | 401 | 521 |
|---|---|---|---|---|
| permanent-weighted PW | 18.1 | 9.34 | 4.49 | 1.95 |
| contraction count (Rees) | 50 | 1450 | 12700 | 38800 |

- PW is falling roughly like p^{-3} over 401–521. Extrapolating that **[heuristic]**, PW < 1 near p ≈ 650. That would be well below the O1 barrier 2628 and T_A(5) ≈ 1.25·10⁴.
- **Update (same pass): the extrapolation held.** A compute agent wrote a C kernel
  (`osc-k5/osc_kernel.c`, driver `osc-k5/osc_k5.py`; full report `osc-k5/REPORT.md`). It
  enumerates S modulo PGL₂ and never enumerates T, so p = 271 takes 0.03 s instead of 34 s.
  - Validation [computed]: the full $5^{10}$ F array equals `types/orbit_types_fast.py` exactly at
    p = 271, 311; at κ = 4 it equals `sep_types` at p = 61, 149, 197, 229, 509 and reproduces
    `cert_k4.out`; it reproduces Rees and PW at 401 and 521. Internal checks (orbit sizes sum to
    $(p-2)(p-3)$, $N_1 = \hat F(0)/\kappa^2$, integrality) hold at every prime.
  - Coverage: 56 primes, 181–2311 (`osc-k5/summary.out`). p = 2521 was killed at a 1 h cap
    without output; 2711–3461 were not run.

  Selected rows [computed]:

  | p | λ = p/625 | Rees | PW | PW_pair | $N_1/\mu_1$ | $B_L$ | $B_H$ |
  |---|---|---|---|---|---|---|---|
  | 401 | 0.64 | 12700 | 4.49 | 3.37 | 0.80 | 1.01 | 67 |
  | 521 | 0.83 | 38800 | 1.94 | 1.47 | 0.33 | 0.26 | 77 |
  | 641 | 1.03 | 246750 | 1.30 | 0.985 | 0.44 | 0.31 | 89 |
  | 661 | 1.06 | 338625 | 0.947 | 0.696 | 0.55 | 0.36 | 123 |
  | 821 | 1.31 | 2349425 | 1.14 | 0.908 | 0.60 | 0.50 | 212 |
  | 1201 | 1.92 | 70370125 | 1.13 | 0.967 | 0.79 | 0.40 | 999 |
  | 1231 | 1.97 | 63222310 | 0.296 | 0.200 | 0.71 | 0.39 | 154 |
  | 2311 | 3.70 | 12417441600 | 0.177 | 0.128 | 0.85 | 0.39 | 3440 |

  - **Crossings [computed, single primes].** PW_pair < 1 first at 641 and at every tested prime
    821–2311. PW < 1 first at 661 and at every tested prime 1231–2311. Over $p \ge 421$ both
    decay like $p^{-1.85}$ with prime-dependent spikes (1201, 1301, 1361). Rees = 0 only at
    181, 211, 251 (191 and 241 have no (C1) configuration).
  - **(N) [computed].** $N_1/\mu_1 \in [0.27, 0.87]$ for $p \ge 401$, slowly rising.
  - **(L) [computed].** $B_L = \max_{m\le5} n|\hat F|/(\kappa\hat F(0)) \in [0.22, 0.70]$ for $p \ge 421$.
  - **(H) [computed; contradicts the hypothesis as stated].** $B_H = \max_{m\ge6} |\hat F|/(\sqrt{m/N_1}\,\hat F(0))$
    grows from 56 to 3440 over 421–2311 (log-log slope +2.26). The maximiser is always the
    (3,3) class with r and c of equal value multiset (e.g. {0,0,1,2,2}/{0,0,1,2,2}); (2,4)
    reaches ≈1200. Class decay of $n|\hat F|/\hat F(0)$: (2,2), (2,3), (3,3) flat (so $|\hat F|/\hat F(0)\sim c/p$);
    (4,4) $\approx p^{-2.8}$; (5,5) $\approx p^{-3.5}$. $\sqrt{m/N_1}$ is reached only near $m = 10$.
  - **Probable mechanism [heuristic; refuted in §11.1].** A boundary term as in Theorem 3: the
    z-sum runs over $\mathbb P^1 \setminus (S \cup T)$, and the $2\kappa$ excluded points give $O(\kappa)/n$
    terms that do not cancel over (C1) orbits when the r- and c-patterns align. The exact
    decomposition of §11.1 puts the bias in the complete-sum part instead.
  - **Revised hypothesis OSC′(B) [conjecture].** Every non-pair class satisfies
    $|\hat F(\rho)| \le B\kappa\hat F(0)/n$ for support $m \le m_0(\kappa)$, with faster decay beyond. At κ = 5
    the data give $m_0 = 6$ and $B_{\rm all} \le 0.71$ for $p \ge 421$. Moving $m = 6$ into (L)
    raises the low weight from 698 to ≈1798 and the leading term of $T_{\rm strong}(B)$ to
    ≈$9\cdot10^3 B$ [estimate], still below $T_A(5)$ for $B = 1$. How $m_0(\kappa)$ grows decides
    whether OSC′ still gives an exponent below κ. Superseded by the precise form in §11.8 (there
    $B$ is in units of 1, so $B_{\rm all} \le 0.71$ here reads $B_{\rm low} \le 3.5$), where the
    exponent is determined conditionally.

## 9. Part (N): the (C1) count (`osc-N/REPORT.md`, independent AI referee in `osc-N/referee/`)

- [proved; referee CORRECT WITH FIXES, fixes applied] **Theorem C.** By double counting
  $\Lambda_M$ against balanced splits (no Weil needed for κ ≤ 6), (C1) configurations exist at
  κ = 3 from 19 (tight), κ = 4 from 137, κ = 5 from 1451, κ = 6 from 20233, against pigeonhole
  31, 197, 2521, 38891. Asymptotically [argued at leading order] from $(1+\varepsilon)\kappa^\kappa/(2e)$.
  Quantitative (N): $B \le 2.05$ at (4, 641), $\le 8.6$ at (5, 3461), $\le 9.9$ at (6, 50023).
- [proved; referee CORRECT] **O1-N barrier.** Any certificate bounding every $e \ne 0$ kernel
  frequency by its modulus fails up to $P_N \approx (\kappa-1)\kappa^\kappa$, above pigeonhole. Signed
  certificates such as PW_pair escape it.
- [proved, narrow] **Moment-only barrier.** Certificates using only $\Lambda_1..\Lambda_{\kappa-1}$ fail
  near $\lambda \approx 1$; the broad "≤ κ−1 rows" version is a conjecture only (referee).
- [computed, Monte Carlo] **κ = 7 in the OSC regime** (`osc-N/mc_N1.py`, `osc-N/mc_N1_k7.out`):

  | p | λ | samples | $R = N_1/\mu_1$ | 4-cycle heuristic $e^{-n_4/(p-2)}$ |
  |---|---|---|---|---|
  | 36037 | 0.306 | 10⁴ | 1.07 ± 0.18 | 0.93 |
  | 23549 | 0.200 | 1.5·10⁵ | 0.62 ± 0.12 | 0.89 |
  | 17669 | 0.150 | 10⁶ | 0.85 ± 0.15 | 0.86 |
  | 12041 | 0.102 | 2·10⁴ | 0 hits (uninformative) | 0.80 |

  All informative rows are within 2σ of the heuristic; nothing suggests (N) fails at λ ≈ 0.15.
  This is sampling evidence, not a bound.

## 10. Next

- Run κ = 5 at p = 2521 and 2621 as single uncapped runs (≈1.0–1.2 core-h each on an unloaded
  machine) with `osc-k5/osc_k5.py`. Acceptance: PW_pair < 1 at both, closing the range up to the
  O1 barrier 2628.
- Done or superseded by §11: there is no boundary term (§11.1), and $m_0(6) = 6$ from Monte
  Carlo (§11.6). The current next steps are in §11.9.

## 11. OSC′ made precise, and its exponent (follow-up, same day)

Scripts and outputs are in `osc-bdry/` (decomposition; exact class values κ ≤ 5) and `osc-mc/`
(Monte Carlo, noise law, fits, thresholds). Every run used `nice -n 19 /opt/anaconda3/bin/python -I`
and took at most ≈ 1 core-h. An independent AI review of the derivation and the estimators (9 Nov)
found five errors in the first draft of this section, all corrected below: per-class κ = 6 constants
that were not bounds, the range of OSC′, the null mean, the cluster fraction, and a limit formula.
The decision is in §11.8.

### 11.1 The c/p bias is not a boundary term [identity proved; computed]

- [proved, identity] By Theorem A, a (C1) configuration has chart-z types U_i(z) = ψ_i − ind(t_i − z)
  and V_j(z) = φ_j − ind(s_j − z). Put h_r^T(x) = Π_i χ^{r_i}(x − t_i) and
  h_c^S(x) = Π_j χ^{c_j}(x − s_j). Under (C1), h_r^T is constant on S and h_c^S is constant on T.
  So each permutation term of Σ_z Sym_R(U(z)) Sym_C(V(z)) is a complete one-variable character sum
  in z, minus its values at the 2κ excluded points z ∈ S ∪ T.
  - At z = s_j only coordinates with c_j = 0 survive, since χ^{c_j}(0) = 0 otherwise.
  - Hence V(R,C) = A(R,C) − b(R) − b(C), where A is the complete-sum part and b the one-sided
    boundary function (the same function on both sides, by S ↔ T symmetry).
  - One-sided form: V(0,C) = a(C) − κ − b(C).
  - `osc-bdry/bdry_terms.py` checks the identity and its label-independence to 1e−14 at κ = 4, 5.
- [computed] At κ = 5 the boundary part is the minority and decays (`osc-bdry/bdry_k5.out`).
  - Matched (3,3) classes: rms |b| = 0.44 → 0.15 from p = 401 to 641, against rms |V| = 0.635 → 0.495
    and |A| = 1.045 → 0.646.
  - (2,4) class 14/1234 at 641: |V| = 0.096, |b| = 0.230, |A| = 0.326.
  - So the bias sits in the complete-sum part A, and the "probable mechanism" of §8 is refuted.
    There is no boundary term to prove.

### 11.2 Mechanism: size-biased completion [exact at κ = 3; heuristic for κ ≥ 4]

- A full S-bucket of size b carries weight (b)_κ. Refine it by one more coordinate (a third
  S-point, or the chart point). The sub-class that holds T then has probability ∝ (A_k)_κ, a
  size-biased law, not a uniform one.
- For a one-sided class supported on three S-points with values (a, b, −a−b), the sub-classes are
  the cyclotomic classes of order κ (A_ij = #{w : (ind w, ind(w−1)) ≡ (i,j)}). This gives
  V(0,c) ≈ Σ_ij (A_ij)_κ Σ_{i′j′} A_{i′j′} ζ^{a(i′−i)+b(j′−j)} / Σ_ij (A_ij)_κ − κ − b(c).
- [computed] At κ = 3 (support 3 = κ, b = 0) this equals the exact values to 1e−14
  (`osc-mc/cyclo_model.py`).
- At κ = 4, 5 the other profile coordinates are treated as uniform, so it is a heuristic. Median
  error 0.10 against median |V| 0.76 (κ = 4), and 0.5 against 1.05 (κ = 5).
- [argued] Linear response in the cyclotomic deviations gives κ|Ŝ_c|²/p − κ. For support 3 this is
  ≈ 0 because |Jacobi sum|² = p, which explains the missing −κ offset. The second-order term is
  ~κ³/√p, which matches the observed slopes near −0.5.

### 11.3 Monte Carlo of class values, and how to read it [computed]

- `osc-mc/mc_classes.py` samples S uniformly and takes every T in a full S-bucket. For all class
  pairs it accumulates Q(R,C) = Σ_z Sym_R(U(z)) Sym_C(V(z)) over z ∈ P¹ ∖ (S ∪ T), with Sym given
  by orbit permanents (Glynn). Batch splitting gives split-batch estimates of |V|².
- Validation at κ = 5, p = 401 (10⁵ configurations, against the exact `osc-k5` arrays):
  - PW 4.499 vs 4.486; PW_pair 3.383 vs 3.373; N₁/μ₁ 0.802 vs 0.80.
  - |MC − exact|/se over the 676 class pairs: median 0.83, max 3.83 (`osc-mc/compare_exact.py`).
- **Batching defect, fixed 9 Nov 22:20.** Earlier runs assigned batches round-robin by
  configuration; their npz files have equal batch counts.
  - [derived] This is not harmless. A bucket of size b > κ gives C(b,κ) configurations that share
    S. With Poisson(λ) bucket sizes a fraction 1 − e^{−λ} of all configurations comes from such
    buckets (λe^{−λ} from size κ+1): 0.26 at λ = 0.3, 0.39 at λ = 0.5, 0.78 at λ = 1.5.
    Round-robin spreads each cluster over several batches, so the split-batch |V|² keeps a
    positive bias of order se².
  - Effect: a class whose true value is below about one se reads as ≈ se. Strong signals are
    unaffected.
  - Same-seed reruns (identical configurations, only the batching changed): PW_pair 0.303 → 0.258
    at κ = 6, p = 3877 (λ = 0.5), and 0.206 → 0.127 at p = 11677 (λ = 1.5). At 3877 nine of the
    eleven m ≥ 7 bins read z_jk = 3.3–9.3 before the fix; after it only (3,4) is above 2.5
    (z_jk = 3.2).
  - So every pre-fix high-support value that is not far above its se is an upper estimate only.
    This includes the first κ = 7 run (§11.7).
- **Estimators.**
  - Even with S-batching, the per-class √max(sq, 0) has mean 0.34·se_b when V = 0 (se_b is the
    standard error of the batch-mean average; 16 batches; 0.33 as B → ∞). So the "debiased"
    PW_pair keeps a null floor: 0.09–0.23 in the typical S-batched κ = 6 runs, 0.50 at 1933, and
    0.59 and 0.45 at κ = 7, p = 58787 and 47041.
  - The weighted bin sum Σ_bin w·sq without clipping is unbiased for Σ_bin w|V|². A jackknife over
    batches gives its z_jk; it recomputes the whole bin, so it handles sq(R,C) = sq(−R,−C) and
    correlations between classes. Cauchy–Schwarz turns the sum into an upper estimate of
    Σ_bin w|V| (`pw_bin_cs.py`).
  - Per class, the Monte Carlo resolves only classes far above se_b. `osc_prime_B_mc.py` (which
    refuses pre-fix files) therefore prints a lower estimate (the largest class significant at
    3σ) and the per-class 2σ upper end, and the bin-level values with jackknife limits.
  - The per-configuration se printed by `bins_report.py` understates the error when
    configurations cluster.

### 11.4 Finite-ensemble noise law [computed]

- Per (C1) configuration, Var Q(R,C) = c·n/(orb_R orb_C) (`noise_law_c.py`, `noise_law_c.out`;
  median over two-sided class pairs, with the 5–95% range):
  - κ = 5, p = 401: 1.008 (0.87–1.24);
  - κ = 6, the five typical S-batched primes: 0.94–1.00 (all pairs within 0.91–1.09);
  - κ = 7: 1.008 (0.99–1.03) at p = 58787 and 0.995 (0.98–1.01) at p = 47041.
  One configuration's z-sum behaves like a sum of n independent uniform types.
  - Exception: the κ = 6 spike prime 1933 has median c = 1.34 (5–95%: 1.00–2.15), so there the
    types along z are correlated and the noise-only values below are underestimates.
- So a class with no systematic part has E|V| = (√π/2)√(n/(orb_R orb_C N_unl)), where N_unl is the
  number of unlabelled (C1) PGL₂-orbits. Its total PW_pair contribution is
  (√π/2)A′²/√(n N_unl), with A′ = Σ_R √orb_R W_R (`osc-mc/weights_k.py`).
- Noise-only crossings (`osc-mc/model_threshold.py`, N₁/μ₁ = 0.8):

  | κ | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |---|---|---|---|---|---|---|---|
  | p_noise | 112 | 425 | 1746 | 8135 | 39729 | 202353 | 1081631 |
  | λ | 1.75 | 0.68 | 0.225 | 0.069 | 0.019 | 0.0047 | 0.0011 |
  | log_κ p_noise | 3.40 | 3.76 | 4.17 | 4.63 | 5.09 | 5.56 | 6.03 |

  So p_noise ≈ 3.3κ^{(κ+1)/2}, and log_κ p_noise − (κ+1)/2 = log_κ(3.3–3.5). The κ = 5 and κ = 6
  values agree with the crossings computed from the measured σ_RC (`noise_pw.py`: 427–442 and
  1654–1808).
- Weights (`weights_k.out`): W_tot = 575, 1.21e4, 2.54e5, 1.12e7, 4.72e8, 2.24e10, 1.11e12 for
  κ = 4..10, about 0.55κ^{κ−2}e^κ. The per-side sum A(j) peaks at full support j = κ, and the
  one-sided total is 2(√(W_tot+1) − 1 − C(κ,2)).
- [proved] Rigorous weight bound. Over sum-zero r ∈ (ℤ/κ)^κ, Σ_r |per(ζ^{r_i l})|² = κ^κ κ!. (Expand
  |per|² over pairs of permutations σ, τ; the character sum over the sum-zero subgroup is κ^{κ−1}
  when σ(i) − τ(i) is constant mod κ and 0 otherwise, and κ!·κ pairs qualify.) With
  P_r = per/κ! and Cauchy–Schwarz over the κ^{κ−1} sum-zero r, W_tot + 1 = (Σ_r |P_r|)² ≤ κ^{2κ−1}/κ!.
  Checked numerically at κ = 4, 5, 6 (576 ≤ 683, 1.21e4 ≤ 1.63e4, 2.54e5 ≤ 5.04e5). The bound is
  1.19, 1.35 and 1.98 times the measured W_tot + 1 there (≈ 0.7√κ asymptotically, if W_tot ≈
  0.55κ^{κ−2}e^κ). Since also |P_r| ≤ 1, every group weight in §11.8 is bounded rigorously, so the
  weight side of the threshold is a theorem, not a fit.

### 11.5 κ = 5 exact: the systematic part per support [computed]

- `osc-mc/exact_sys_k5.py` compares the exact values at all 54 primes with the noise law. The
  excess sqrt(rms² − noise²) estimates the systematic part; `decay_fit.py` fits its decay in p
  (upper envelope over primes).

  | bin (two-sided) | m | p-decay exponent of the excess, κ = 5 | κ = 4 |
  |---|---|---|---|
  | (2,2) | 4 | 0.21 (flat) | 0.12–0.13 (flat) |
  | (2,3) | 5 | 0.71 | 1.0–1.5 |
  | (2,4), (3,3) | 6 | 1.03, 0.57 | 1.07–1.25, 0.47–0.52 |
  | (2,5), (3,4) | 7 | 1.80, 1.23 | —, 0.92–1.09 |
  | (3,5), (4,4) | 8 | 1.65, 1.54 | —, 1.35–1.50 (noise level) |
  | (4,5) | 9 | 1.87 | — |
  | (5,5) | 10 | 2.27 | — |

  κ = 4 uses p ∈ [157, 593] and κ = 5 uses p ∈ [401, 2311]. The κ = 4 noise is calibrated by
  `mc_k4_p197_s3.npz`. §8's steeper class decays ((4,4) ≈ p^{−2.8}, (5,5) ≈ p^{−3.5}) are for the
  raw values, which include the fast-falling finite-ensemble noise.
- The m ≥ 7 systematic part is nonzero at every κ = 5 prime from 401 on (e.g. (3,4): 1.16κ²/p
  with z ≈ 400 at 2311; `equal_p_chain.out`). So above m₀ the values decay; they are not
  pure noise.
- **Spike primes.** At 1201, 1291, 1301, 1361, 1381 (and 491, 691, 811) every bin rises at once,
  and the high-support bins by 5–15×.
  - At 1201 the rms over (4,4) is 65× the noise level, and over (5,5) 4.7×.
  - So at these primes the systematic part is not confined to bounded support.
  - No pattern in arg g^5, 5th-power residuosity of 2–13, or the Jacobi-sum phases separates them
    (`spike_k5.py`).
  - The spike score does correlate with the 4th-moment ratio K = κ²ΣD⁴/(ΣD²)² of the order-5
    cyclotomic numbers (D = deviation from the mean; Parseval fixes ΣD²): Spearman 0.63 over 47
    primes. The top spikes have K = 3.3–4.2 against a median of 2.54, but 691 has 1.64
    (`cyclo_spike.py`). At κ = 6 the three spikes have the three largest K of 15 primes (§11.6).
    This is a lead, not a law. It fits §11.2, where the configuration weights are κ-th factorial
    moments of sub-bucket sizes, so a lumpy cyclotomic structure strengthens the size bias.
  - On the envelope the spikes still decay in p: the (4,4) envelope falls from 0.13 at 491 to
    0.009 at 2111.
- **Per-class constants** (`osc_prime_B.py`, `osc_prime_B_k5.out`):
  - max |V| over two-sided m ≤ 6 and one-sided non-pair classes: ≤ 3.5 for p ≥ 421 and 5.0 at
    p = 401 (class 11111/0, 5.6 noise rms, so a real value). At p = 181–331, below the noise
    crossing 425, it is 4.0–24.9. Those maxima sit on orbit-1 full-support one-sided classes and
    are within 2.7 noise rms of zero, so they are finite-ensemble noise.
  - max over two-sided m ≥ 7 of (|V| − 2·noise)₊/(κ²/p), for p ≥ 401: median 2.5, 90th
    percentile 6.2, max 8.4 (32 at p = 271). The maxima are orbit-1 classes such as 11111/11111,
    which have weight 1.
- **Group constants** (`equal_p_chain.py`; weighted rms over the (L′) and (D) groups of §11.8,
  noise removed in quadrature). For p ≥ 431 (45 primes): B_L median 0.37, max 0.79 (491); B_D
  median 0.85, max 3.04 (1201). B_L is below 2 at 2σ at every prime from 181 on. B_D falls from
  ≈ 2.2 at p = 311–331 to ≈ 0.5 at 2011–2311, so at fixed κ the D group decays like p^{−1.7}.

### 11.6 κ = 6 Monte Carlo [computed, sampling estimates, not certificates]

`mc_classes.py 6 p N --seed 11` (seed 1 for one 3889 run). "S" = S-batched (valid), "rr" = pre-fix
round-robin (weak values are upper estimates, §11.3). PW_pair is the debiased MC estimate, an upper
estimate because of the null floor. "Noise" is the noise-only PW_pair from the noise law, part of
the true value at that prime. |L|/(2√p) is for 4p = L² + 27M² (`cubic_LM.py`), K is as in §11.5.

| p | λ | batching | configs | PW_pair | noise | \|L\|/(2√p) | K | note |
|---|---|---|---|---|---|---|---|---|
| 1933 | 0.25 | S | 2·10⁴ | 7.17 | 0.385 | 0.705 | 5.47 | spike; N₁/μ₁ = 2.63; c = 1.34 |
| 1951 | 0.25 | rr | 2·10⁴ | 1.087 | 0.418 | 0.011 | 4.32 | spike |
| 2347 | 0.30 | S | 2·10⁴ | 0.754 | 0.232 | 0.661 | 2.19 | m ≥ 7 bins nonzero; CS upper 1.02 |
| 2719 | 0.35 | rr | 3·10⁴ | 0.629 | 0.107 | 0.968 | 2.08 | |
| 3079 | 0.40 | rr | 3·10⁴ | 0.486 | 0.053 | 0.712 | 2.72 | |
| 3571 | 0.46 | S | 3·10⁴ | 0.294 | 0.031 | 0.008 | 4.11 | |
| 3877 | 0.50 | rr / S | 5·10⁴ | 0.303 / 0.258 | 0.017 | 0.281 | 2.32 | same configurations |
| 3889 | 0.50 | rr | 10⁵ | 0.832 | 0.017 | 0.016 | 4.92 | spike |
| 3907 | 0.50 | rr | 5·10⁴ | 0.373 | 0.015 | 0.488 | 3.86 | (0,3) elevated |
| 3931 | 0.51 | rr | 5·10⁴ | 0.294 | 0.017 | 0.710 | 2.67 | |
| 4111 | 0.53 | rr | 5·10⁴ | 0.28 | 0.014 | 0.850 | 2.09 | |
| 4219 | 0.54 | S | 3·10⁴ | 0.299 | 0.010 | 0.008 | 4.28 | (0,3) 2× typical |
| 5839 | 0.75 | rr | 10⁵ | 0.188 | 0.002 | 0.700 | 2.09 | |
| 7789 | 1.00 | rr | 10⁵ | 0.182 | 0.001 | 0.946 | 1.70 | upper estimate |
| 11677 | 1.50 | rr / S | 5·10⁴ | 0.206 / 0.127 | 0.000 | 0.976 | 1.71 | same configurations |
| 15559 | 2.00 | rr | 5·10⁴ | 0.213 | 0.000 | 0.978 | | 81 S only; upper estimate |

- **Where the systematic part sits.** In every S-batched run with λ ≥ 0.46 (3571, 3877, 4219,
  11677) the only bins with |z_jk| > 3 are (0,3), (0,4), (2,2), (2,3), (2,4) and (3,3), all with
  m ≤ 6 (at 11677 only (2,2) and (3,3)). At 3877 (3,4) is borderline (0.63κ²/p, z_jk = 3.2). So
  m₀(6) = 6, as at κ = 4, 5.
- **At λ = 0.30 (2347)** the m ≥ 7 bins are nonzero: (3,4) 1.37κ²/p (z_jk = 15.8), (4,4) 0.67
  (z_jk = 6.4), (4,5) 0.33 (4.9), (2,5) 0.91 (3.3), (3,5) 0.38 (3.0); (5,5) 0.24 has z_jk = 2.7
  only. The two-sided low bins are about 2× their λ ≈ 0.5 values. (3,4) grows 3.6× from 3877 to
  2347, like p^{−2.6} at fixed κ.
- **Constants (S-batched runs, `osc_prime_B_mc.out`, `equal_p_chain.out`).**
  - Per class, κ = 6 is not resolved. The largest low class significant at 3σ is 2.1–2.8 at the
    five primes with λ ≥ 0.30, with per-class 2σ upper ends 2.4–8.0. For m ≥ 7 classes the 2σ upper
    ends are 60–617κ²/p, because the low-orbit classes have se_b ≥ 21κ²/p (3877). So no per-class
    B_hi can be quoted for κ = 6.
  - Group level (noise-subtracted): B_L = 0.27–0.41 at the five primes with λ ≥ 0.30, and B_D =
    0.34 at 2347 (z = 2.9), ≤ 0.40–0.58 (2σ) at 3571, 3877 and 4219, unresolved at 11677 (< 3.2).
  - Bin level: the worst m ≥ 7 bin has a 2σ limit of 1.2–2.7κ²/p at λ = 0.30–0.54.
  - At the spike 1933: B_L = 1.20, B_D = 3.67 (z = 12.3), and every bin significant up to full
    support, with (3,4) at 11.4κ²/p (z_jk = 19.8) and the largest one-sided bin (0,3) at w-rms 6.9.
- **Spike primes.** 1933, 3889 and 1951 (3907 mildly) rise in all bins at once. Two primes at the
  same λ = 0.25 differ by 12× in the m ≥ 7 bins (1933 against 1951), so this is a property of the
  prime, not of λ.
  - |L|/(2√p) ≈ 0 does not predict spikes: 3571 and 4219 have |L| = 1 and are typical. Neither
    does the Eisenstein angle (4111: φ = 28°, typical).
  - K ranks the three spikes first (5.47, 4.92, 4.32 of 15 primes). But 4219 and 3571, chosen
    for |L| = 1 (which correlates with K), have K = 4.1–4.3 and are typical apart from (0,3) at
    4219. So high K looks necessary, not sufficient.
  - Roots-of-unity test (`struct_c1.py`, `struct_c1_k6.out`; rates against the uniform-S rate
    of the Monte Carlo run). At 1933, 6-point subsets S of μ₁₂ give ≈ 57× the uniform rate of
    (C1) configurations (μ₁₆₁: 9×, μ₈₄: 3×), although T never lies in μ₁₂. At 3889, μ₁₈ gives 5×.
    At 1951, 2347 and 3877 no divisor gives more than 2×.
  - Up to PGL₂ such S are ≈ 4·10⁻⁶ of all S, far too few to explain N₁/μ₁ = 2.6 directly. So this
    shows structured (multiplicative) correlations at the spike primes, not the mechanism.
- **How the constants depend on κ (`equal_p_chain.py`, κ = 4, 5 exact, κ = 6, 7 S-batched).**
  - Equal p, κ = 4 against κ = 5 at the five common primes 401, 421, 461, 521, 541: B_D(5)/B_D(4)
    = 0.76–2.26 (absolute D-group rms ratio 1.2–3.5), B_L ratio 1.3–2.4.
  - Equal p, κ = 5 against κ = 6: B_D(6)/B_D(5) = 0.64 (2σ < 0.83) for 2311/2347 and 0.55 for
    2111/2347, while the absolute D-group rms agrees within 0.7–0.9. Against the spike, κ = 5 at
    1801 vs κ = 6 at 1933 gives 11.7.
  - Equal λ = 0.50, κ = 6 at 3877 against κ = 5 at 311: absolute D-group rms ratio 0.007 (2σ
    < 0.020); per bin (3,4) 0.032, (4,4) 0.024, (2,5) 0.019, (4,5) 0.015, (3,5) < 0.013,
    (5,5) < 0.014. A λ-law (values set by the bucket occupancy) would give 1, and a constant-B
    p-law 0.12. So the values are not a function of λ, and at fixed λ they fall with κ.
  - So at typical primes there is no κ!-like growth (which would give factors 5 and 6 per step at
    equal p). The κ = 5 → 6 step rests on one κ = 6 prime, and the per-prime scatter at fixed κ is
    up to 10× (spikes), so this bounds the growth only loosely.
- **Crossing.** The debiased PW_pair is below 1 at every tested prime from 2347 up (14 primes,
  including the spike 3889). At 2347 the CS upper estimate is 1.02, and 3889 and the other rr
  primes are pre-fix upper estimates. Below that, 1933 (7.17, S-batched) fails, and so does the
  pre-fix estimate for 1951 (1.087). The noise-only crossing is λ ≈ 0.22. At κ = 5 the
  corresponding numbers are λ 1.31 (all tested primes pass) against 0.68.

### 11.7 κ = 7 [computed]

- **p = 58787 (λ = 0.50), 10⁴ configurations.** The pre-fix run gave debiased PW_pair 0.836, with
  every m ≥ 7 bin significant at 5–60κ²/p. The same-seed S-batched rerun (identical
  configurations) gives debiased 0.591, which equals its null floor 0.587, and a CS upper
  estimate of 0.104. Every m ≥ 7 bin is consistent with zero; only (2,2) is significant (w-rms
  1.88, z_jk = 9.6).
  - So the pre-fix signal was entirely the batching artefact. Noise law: c = 1.008. B_L = 0.27
    (z = 6.1).
  - The run cannot resolve the κ²/p level: the 2σ bin limits are 3.1–42κ²/p, or 0.0026–0.035 in
    absolute terms, and B_D < 5.2 (2σ) (`bin_limits.out`, `equal_p_chain.out`). At equal λ that
    is 0.024× κ = 5 at 311 (2σ), above the constant-B p-law prediction 0.010.
  - So at λ = 0.5 it does not distinguish a p-law from a λ-law.
- **p = 47041 (λ = 0.40), 2·10⁴ configurations, seed 12, S-batched** (`mc_k7_p47041.log`,
  ≈ 0.8 core-h). λ = 0.40 is just below λ_T(7) = 0.44 for the typical group constants (§11.8).
  - N₁/μ₁ = 0.97 and noise law c = 0.995 (0.98–1.01): not a spike.
  - Debiased PW_pair 0.470 against its null floor 0.454; CS upper estimate 0.200.
  - Only (2,2) is significant (w-rms 1.65, z_jk = 15.2). (3,3) (z_jk = 2.8) and (0,3) (2.3) are
    borderline, and no m ≥ 7 bin has |z_jk| > 2.
  - Group constants: B_L = 0.22 (z = 12.0); B_D = 1.06 (z = 0.4), < 2.6 at 2σ. The 2σ bin limits
    are 1.6–23κ²/p (0.0017–0.024 absolute).
  - So at κ = 7, λ = 0.4 the D group is bounded at the level of the κ = 4–6 typical constants
    (medians 0.34–1.03, maxima 2.1–3.7), with no sign of growth. A typical B_D of 0.3–1 predicts
    an absolute D rms of 0.0004–0.001, below the 2σ limit 0.0027, so this run cannot separate a
    p-law from a λ-law either.

### 11.8 OSC′ stated precisely, and the exponent it gives [conditional; computed]

- **Two precise forms [conjectures].** Fix κ and m₀ (= 6, below). Let L be the one-sided non-pair
  classes together with the two-sided classes with m = m_R + m_C ≤ m₀, and D the two-sided
  classes with m > m₀. Let w be the permanent weights, W_G = Σ_G w, ρ_G = (Σ_G w|V|²/W_G)^{1/2}
  the weighted rms over a group, and ν_G the same rms of the noise σ_RC/√N_unl, where
  σ_RC² = n/(orb_R orb_C) (§11.4). For primes p ≡ 1 (mod κ) with p ≥ p₀(κ):
  - **OSC′(B), per class:** (N) N₁ ≥ μ₁/B; (L′) |V(R,C)| ≤ B on L; (D) |V(R,C)| ≤ Bκ²/p +
    2σ_RC/√N_unl on D. In F̂ terms, |F̂(ρ)|/F̂(0) ≤ B/n on L and ≤ Bκ²/(pn) + 2σ_RC/(n√N_unl)
    on D.
  - **OSC′_rms(B_L, B_D), per group:** (N) as above; (L′) ρ_L ≤ B_L + ν_L; (D) ρ_D ≤ B_Dκ²/p + ν_D.
    It is weaker than the per-class form (OSC′(B) implies OSC′_rms(B, B)), and it is all the
    threshold uses: by Cauchy–Schwarz Σ_G w|V| ≤ W_G ρ_G.
  - **Range.** The certificate needs p₀ ≤ T (below). Neither form holds from the bottom of the
    (C1) range: at κ = 5, p = 181–331 single low classes reach 4.0–24.9 (finite-ensemble noise,
    §11.5), and at p = 401 one class is 5.0. The group form with the noise allowance holds there
    (B_L < 2 at 2σ).
  - Both replace the §8 draft (whose B_all ≤ 0.71 was in units of κ). The bounded-support reading
    (pure noise above m₀) is false at every κ = 5 prime from 401 on, and at κ = 6 at 2347 and
    1933 (S-batched).
- **The constants in the data [computed; κ = 6, 7 are Monte Carlo estimates].**

  | κ | primes (p range) | B_L median / max | B_D median / max | per class (L′), (D) |
  |---|---|---|---|---|
  | 4 | 31 (197–593) | 0.33 / 0.46 | 1.03 / 2.07 | — |
  | 5 | 45 (431–2311) | 0.37 / 0.79 (491) | 0.85 / 3.04 (1201) | ≤ 3.5 (p ≥ 421), ≤ 8.4 |
  | 6 | 6 (1933–11677) | 0.34 / 1.20 (1933) | 0.34 / 3.67 (1933) | not resolved |
  | 7 | 2 (47041, 58787) | 0.22 / 0.27 | unresolved: < 2.6 and < 5.2 (2σ) | not resolved |

  m₀ = 6 at κ = 4, 5, 6, with no growth seen. The κ = 6 sample includes one prime chosen as a
  spike, and B_D at κ = 6 is resolved only at 1933 and 2347.
- **What OSC′ gives [derived; `osc_prime_T.py`, `osc_prime_T.out`].** With the noise law,
  PW_pair ≤ (W_L/n)ρ_L + (W_D/n)ρ_D + noise. Asking each term to be < 1/3 gives T = max(T₁, T₂, T₃):
  - T₁ = 3B_L·W_L. The one-sided weight 2√(W_tot+1) = κ^{κ/2+κ/(2 ln κ)−1+O(1)} dominates the
    poly(κ) two-sided part.
  - T₂ = κ√(3B_D·W_D) = κ^{κ/2+κ/(2 ln κ)+O(1)}·√B_D.
  - T₃ = the noise crossing ≈ 3.3κ^{(κ+1)/2}, which never dominates for κ ≥ 4.
  - So T = κ^{κ/2+κ/(2 ln κ)+O(1)}·max(B_L, √B_D). With log_κ B_L, log_κ B_D = o(κ) this is
    **exponent (1/2+o(1))κ, below κ**. The weight inputs are bounded by §11.4's theorem; the only
    unproved input is OSC′.

  | κ | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |---|---|---|---|---|---|---|---|
  | log_κ T, per class B = 3 | 5.79 | 6.02 | 6.14 | 6.33 | 6.54 | 6.92 | 7.50 |
  | log_κ T, per class B = 8.5 | 6.54 | 6.67 | 6.72 | 6.86 | 7.04 | 7.35 | 7.77 |
  | log_κ T, group (0.5, 1.6) | 4.50 | 4.91 | 5.14 | 5.57 | 6.18 | 6.78 | 7.36 |
  | log_κ T, group (1.2, 3.7) | 5.13 | 5.45 | 5.62 | 5.85 | 6.38 | 6.97 | 7.54 |
  | λ at T, group (0.5, 1.6) | 8.1 | 4.3 | 1.3 | 0.44 | 0.18 | 0.069 | 0.023 |
  | κ/2 + κ/(2 ln κ) | 3.44 | 4.05 | 4.67 | 5.30 | 5.92 | 6.55 | 7.17 |

  The group constants are the typical values (0.5, 1.6) and the largest values at any tested
  prime above the noise crossing (1.2, 3.7). With them T < κ^κ from κ = 5 (typical) or κ = 6
  (largest) on; the per-class B = 3 bound needs κ ≥ 7. The measured crossings are lower still
  (κ = 5: p ≈ 820 = 5^{4.2}; κ = 6: p ≈ 2347 = 6^{4.3}), since each step above is an upper bound.
- **How much room there is [derived].**
  - B_L may grow while log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1), and B_D while
    log_κ B_D < (1 − 1/ln κ)κ − O(1). Growth like c^κ is harmless (log_κ c^κ = o(κ)). Growth
    like κ! is fatal for either constant: log_κ κ! = κ − κ/ln κ + O(log_κ κ) gives T = κ^{κ+O(1)}
    through T₂, and worse through T₁.
  - The decay in (D) may be slower: with |V| ≤ Cp^{−a} on D the D term gives
    log_κ T = (κ + κ/ln κ + log_κ C + O(1))/(1+a). That is below κ once
    a > 1/ln κ + (log_κ C + O(1))/κ, so a > 1/ln κ + O(1/κ) when log_κ C = O(1). The measured
    fixed-κ slopes are 1.2–2.6 (κ = 5 envelopes, κ = 5 D group 1.7, κ = 6 (3,4)).
  - m₀ may grow, but each unit of m₀ adds ≈ 0.6 to log_κ T at κ = 7–9. If that rate persists,
    the exponent (1/2+o(1))κ needs m₀ = o(κ). With B = 3, T < κ^κ survives while m₀ ≤ 7, 8, 9, 11
    for κ = 7, 8, 9, 10 (Table 2 of `osc_prime_T.out`), roughly m₀ ≲ κ at these κ.
  - The constants may grow as λ falls. If B_L ∝ λ^{−b} and B_D ∝ λ^{−a} at fixed κ, with a, b
    fixed, then solving T = T(λ_T) with λ_T = T/κ^{κ−1} gives
    log_κ T = max((1/2+b)/(1+b), (1+a)/(2+a))·κ + o(κ) < κ. So polynomial growth in 1/λ still
    gives an exponent below κ, though not κ/2. Read as λ-growth, κ = 5 between λ = 3.7 and 0.5
    gives b ≈ 0.4, a ≈ 0.7, i.e. at most 0.64κ. The equal-λ comparison (§11.6) says these are
    not λ-laws.
- **Decision.** OSC′, in either precise form, gives an exponent below κ: (1/2+o(1))κ, namely
  κ/2 + κ/(2 ln κ) + log_κ max(B_L, √B_D) + O(1), with the one-sided classes and the m ≥ 7
  classes as joint bottleneck. The noise alone would allow (κ+1)/2 + log_κ 3.3. The exponent stays
  below κ under c^κ growth of the constants, under growth like a fixed power of 1/λ, and for any
  decay exponent a > 1/ln κ + O(1/κ). It is lost if B_L ≥ κ^{(1/2−o(1))κ} or
  B_D ≥ κ^{(1−o(1))κ} (κ! is enough for either), if the constants grow faster than any power of
  1/λ, or if m₀ grows past ≈ κ (κ = 7–10). Whether OSC′ holds with constants κ^{o(κ)} where the
  exponent needs it is undetermined. The live obstruction candidate is the spike primes
  (item (c) below).
- **What would be an obstruction, and what the data say.**
  - (a) m₀(κ) growing like κ. Not seen: m₀ = 6 at κ = 4, 5, 6.
  - (b) Constants growing like κ! with κ, or values set by λ rather than p. Not seen at typical
    primes: at equal p the per-step factors are 0.55–2.3, and at equal λ = 0.5 the κ = 6 values
    are 0.007× the κ = 5 ones. κ = 7 at λ = 0.4 bounds B_D < 2.6 (2σ), inside the κ = 4–6 range,
    but cannot separate the two laws.
  - (c) Spike constants growing like κ^{cκ}, or super-polynomially in 1/λ. **Live.**
    - Spikes multiply the constants by 3–11 (κ = 6, 1933: B_L 1.2, B_D 3.7, against medians 0.34;
      κ = 5, 1201: B_D 3.0 against 0.85). The largest values grow slowly with κ: B_L 0.46, 0.79,
      1.20 and B_D 2.07, 3.04, 3.67 for κ = 4, 5, 6.
    - At κ = 6 spike amplitude rises steeply as λ falls (3889 at λ = 0.5: PW_pair 0.83, pre-fix;
      1933 at λ = 0.25: 7.17, with N₁/μ₁ = 2.6 and the noise law broken).
    - The exponent needs OSC′ at λ_T ≈ 0.44, 0.18, 0.07, 0.02 for κ = 7, 8, 9, 10, and at
      λ ≈ κ^{−κ/2+o(κ)} asymptotically. Only one κ = 6 prime (λ = 0.25) and the κ = 7 run at
      λ = 0.40 come close; the κ = 7 prime is typical (B_L 0.22, B_D < 2.6, CS-upper PW_pair 0.20).
      At smaller λ a structured minority of (C1) configurations could dominate.
  - (d) One-sided values growing with κ. Not seen at typical primes: B_L medians 0.33, 0.37,
    0.34 at κ = 4, 5, 6, and 0.22–0.27 at κ = 7 (two primes).

### 11.9 Next

- Spike primes are now the deciding question. Characterise them at κ = 6 near λ = 0.25–0.5:
  frequency, amplitude (B_L, B_D), N₁/μ₁, K and the μ_d test. The target is a law, or a bound, for
  the share of (C1) configurations that structured families carry as λ falls.
- Prove (L′) for the (2,2) classes at one κ. By §11.1 their value is the (C1)-average of complete
  one-variable character sums of size O(√p), so the target is an O(1) bound on that average: a
  square-root saving against the (C1) measure, not over a box.
- κ = 7 at a second λ = 0.5 prime (58913) and at λ ≈ 0.3 (p ≈ 35099), S-batched, 2–4·10⁴
  configurations each. Acceptance: B_D resolved or bounded ≤ 5 (2σ). The λ ≈ 0.3 run costs
  ≈ 2 core-h with uniform-S sampling.
- The κ = 7 threshold regime (λ ≈ 0.4–1.9, p ≈ 5·10⁴–2·10⁵) is within reach of uniform-S
  sampling (0.037 configurations per S at λ = 0.4, against the predicted Mλ^κ/κ! = 0.038). κ ≥ 8
  is not: at κ = 8, λ = 0.18 the rate is ≈ 6·10⁻⁵ per S, at p ≈ 4·10⁵. Testing those needs a
  sampler that builds (C1) configurations directly; that is the main gap between the data and
  the regime the exponent statement needs.
- κ = 5 at p = 2521, 2621 (§10), deferred until the machine is unloaded.
