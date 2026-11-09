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
    than square-root cancellation, so $B_H$ grows like $p^{2.3}$. The revised hypothesis OSC′
    (§8) still predicts a threshold below $T_A(5)$, but its exponent is not yet determined.
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
- **Next hard question (updated after §8–§9).** Prove the $1/p$ boundary term for the matched
  (3,3) classes at κ = 5 (this turns (H) at $m = 6$ into an (L)-type bound), and determine at
  which total support $m(\kappa)$ the $1/p$ bias stops. (C1) existence for $p = o(\kappa^\kappa)$ is
  now proved down to $\kappa^\kappa/(2e)$ only, which is still $\Theta(\kappa^\kappa)$.

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
- OSC or OSC′ is proved, or (H) is disproved: **false** (finite data at κ = 5 only).
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
  - **Probable mechanism [heuristic, unproved].** A boundary term as in Theorem 3: the z-sum
    runs over $\mathbb P^1 \setminus (S \cup T)$, and the $2\kappa$ excluded points give $O(\kappa)/n$ terms that do
    not cancel over (C1) orbits when the r- and c-patterns align.
  - **Revised hypothesis OSC′(B) [conjecture].** Every non-pair class satisfies
    $|\hat F(\rho)| \le B\kappa\hat F(0)/n$ for support $m \le m_0(\kappa)$, with faster decay beyond. At κ = 5
    the data give $m_0 = 6$ and $B_{\rm all} \le 0.71$ for $p \ge 421$. Moving $m = 6$ into (L)
    raises the low weight from 698 to ≈1798 and the leading term of $T_{\rm strong}(B)$ to
    ≈$9\cdot10^3 B$ [estimate], still below $T_A(5)$ for $B = 1$. How $m_0(\kappa)$ grows decides
    whether OSC′ still gives an exponent below κ; that is not determined.

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
- Prove the $c/p$ boundary term for matched (3,3) classes (κ = 5), then test $m_0(6)$ with the C
  kernel at κ = 6 for a few primes near $\lambda \approx 1$ ($p \approx 7800$) if the cost allows.
