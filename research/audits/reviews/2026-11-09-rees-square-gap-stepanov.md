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
  - **Spike primes (§12; κ = 6 survey of 89 primes, complete; Monte Carlo and heuristic).**
    - At λ ≤ 0.25 (29 primes) spikes reach $B_L = 1.88$ (1657) and $B_D = 14.8$ (1789), 4× and 18–25× the band
      medians. 9 of the 29 primes are spikes.
    - Over all 89 primes (λ 0.2–0.55) 21 are spikes, and spike amplitude falls as λ rises (largest $B_D$ 14.8, 6.6
      and 1.4). Pre-registered (§12.10): "value spikes only at p ≡ 1 (mod 12)" is refuted by 2143, and the shift of
      $B_D$ towards that class held.
    - At λ ≈ 0.21, 71–88% of (C1) configurations are 2+2 involution-structured, at spike and typical primes alike.
      What separates the four split spike primes from the typical 1621 is a large family factor $F$ (2.3–4.4, against
      0.3) and large class values of that family. The rest of the measure is lifted too.
    - Over all 29 primes with λ ≤ 0.25 (§12.11), F is 0.24–4.41, maximum 1789. F carries N₁/μ₁'s ranking (Spearman
      0.98), so a large F and a large N₁/μ₁ are the same observation. The 2+2 share falls with λ, to 0.50.
    - An elementary bound (§12.12): the family can move the exponent only if $G = s/R_{2+2} = \kappa^{\Omega(\kappa)}$,
      where $s$ is its share and $R_{2+2}$ its heuristic weight. This needs no (N) and is asymptotic only. Measured G
      is 0.5–2 at κ = 7; nothing bounds G in general.
    - κ = 4 in closed form (§12.13): each S has 1 or 3 split involutions, according to η(r) and η(1 − r) for its
      cross-ratio r, and G(S) → (2/3)·#split. G(p) = 1 + O(p^{−1/2}) by Weil at fixed κ, which certifies only from
      p ≈ 3·10⁶; the exact counts go 1.52 → 1.003 for p = 101–32009. At every fixed κ, G → 1, and Weil's range is
      p ≥ κ^{(4+o(1))κ}, against thresholds κ^{(1/2+o(1))κ}. κ = 5's pre-registered shape held at six primes.
    - At κ = 7, λ = 0.2 (one prime) the family weight is 0.055 μ₁, which rejects a weight depending on λ alone.
    - At κ = 7, λ ≈ 0.3, 36037 (picked on symR) has the highest B_L of nine primes. Its B_L is 0.635, 2.6× the median
      of seven primes not picked on symR (mechanical item 6, pre-registered). Against those seven it is not shown to
      be a spike: 34259 reaches 0.519 (2σ 0.41–0.61), and the seven span 0.131–0.519 (4.0×). The earlier call, a spike
      against two equal-λ primes (35099 and 34847), stands as scored, but only as a two-prime statement. The κ = 6
      calibration does not transfer: 3 of the 7 exceed κ = 6's unflagged maximum of 1.54× the band median.
    - The 36037 lift is not carried by the 2+2 family: without its 2+2 configurations (3.1%) $B_L$ is still 0.57. What
      carries it is unexamined.
    - 34693, with 36037's symR, scored INCONCLUSIVE by a rule written first: B_L 0.386 (2σ 0.374–0.398), between the
      comparison primes and 36037. The nine primes at λ ≈ 0.3 sit at four or more levels separated at 2σ; symR does not fix B_L (ρ 0.35,
      inconclusive).
    - 34259, the band's high prime, splits like 36037 (mechanical item 7, pre-registered): its B_L is not carried by
      the 2+2 family. The rest is 0.499 (0.459 without one batch), its 2+2 share 3.2% is typical, and the rest is
      not separated from the band's upper pair. This describes two primes selected high; it is not a class.
    - Obstruction (c) is now a question about the spread of B_L across primes, not about isolated spikes (§12.14). At
      κ = 6, σ_L = sd(ln B_L) grows as λ falls (0.49 → 0.24 from λ ≈ 0.2 to 0.5, about 3.8σ). The next test is
      pre-registered: σ_L at κ = 7, λ ≈ 0.3 on 24 primes against κ = 6's 0.352 (mechanical item 8, not started).
    - The square gap stays open.
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

**Update (2026-11-10) [computed]:** `types/orbit_types_fast.py 5 641` (output in `types/orbit_k5_fast_641.out`; the fast script reproduces PW = 4.486 at p = 401) gives PW = 1.296 and a contraction count (Rees) of 246750.

- The decay has slowed. From 521 to 641 the local exponent is about 2, against about 3 from 401 to 521.
- Extrapolating [heuristic], PW < 1 near p ≈ 750–800. That is still far below the O1 barrier 2628.
- No κ = 5 prime has yet been certified by PW.
- Next run: `orbit_types_fast.py 5 761` and `5 881`.

## 12. Spike primes at κ = 6: survey, partial involution structure, and the threshold path (follow-up, 10 Nov)

Question (mechanical plan item 1, §11.9): does OSC′ hold at λ ≤ 0.25 at spike primes, and what are spikes made of?
Everything here is Monte Carlo or heuristic unless marked otherwise; nothing is a certificate. Code and outputs are in
`osc-mc/`.

An independent AI referee checked the section in nineteen passes. Rounds 1–2, with the author's disposition of each
point, are in `osc-mc/review-2026-11-10/REPORT.md`; rounds 3, 3b, 3c, 4, 4b–4g, 4h-a, 4h-b, 4i, 4j, 4k-a and 4k-b (parts 1 and 2) and their dispositions
are in `ROUND3.md`. Its corrections are applied:
- a factor 2 in the heuristic at even κ;
- an undercount in the first `pairsym.py`;
- a misattributed cyclotomic correlation, and a false identification of |a|/√p with §11.6's |L|/(2√p);
- overstated readings of the mechanism and of what it implies;
- a stale survey snapshot, and a spike (1627) missing from the F table;
- an over-read of the N₁/μ₁ prediction at λ ≈ 0.5, and two threshold cases counted as refutations of H1;
- a wrong "median symR" for 35099, and missing 2σ ranges on the bin ratios. The author replaced a knife-edge pairwise
  calibration of 36037 with the ratio to the band median, and the referee confirmed it;
- 36037's F taken from pairsym's clustered sample (2.3; its split gives 1.6), "a not-2+2 effect" for what the split
  only refutes, and a two-prime mean called "typical" and set against all-prime band medians (rounds 4d–4e);
- a backwards sentence in §12.11 that read "F bounded" as "(N)'s B bounded at spike primes", §12.5 item 6's
  illustrations about 4.5× too large (N₁/μ₁ taken as 1), and overstated proof-obstacle wording (rounds 4f–4h-a).

### 12.1 Survey design [computed]

- **Primes and runs.** Every p ≡ 1 (mod 6) in [1500, 2400] and [3800, 4300]: 89 primes.
  - 29 have λ ≤ 0.25, 31 have λ in (0.25, 0.31], and 29 have λ ≈ 0.49–0.55.
  - Each runs `mc_classes.py 6 p N --seed 13`, S-batched. N is 5000 configurations below 1700, 10⁴ up to 2400 and
    2·10⁴ above.
  - The prime list and driver are `survey/k6_survey_primes.txt` and `survey/run_k6_survey.sh` (nice 19, four at a
    time).
- **Analysis.** `k6_spike_survey.py` prints, per prime:
  - N₁/μ₁ with its S-batch se;
  - the debiased PW_pair with its null floor and the CS upper estimate;
  - B_L and B_D with jackknife z and 2σ upper end (the `equal_p_chain.py` estimators);
  - the noise law c, the cluster-corrected B^cl, K and max|D|/√p;
  - ind(−1), ind(2), ind(3), ind(−3) mod 6;
  - symR (§12.3).
- **Spike flags, per λ band.**
  - sD: the 2σ lower end of B_D is above twice the band median.
  - sPW and sN: the debiased PW_pair, or N₁/μ₁, is above twice the band median. These two flags use the point
    value, with no se, as `k6_spike_survey.py` defines them; the H file defines sN the same way.
  - In a band that is not yet complete the medians, and so the flags, are provisional.
- **Status: complete.** §12.2–12.8 were written from the 35-prime snapshot of 03:45 on 10 Nov
  (`review-2026-11-10/survey_snapshot.out`). The final run (04:49, all 89 primes, `k6_spike_survey.out`) changes
  nothing at λ ≤ 0.25. The completed bands are in §12.2's table, and the scored predictions in §12.10. Rerunning
  `k6_spike_survey.py` rebuilds every table.

### 12.2 Results [computed]

| λ band | primes | median B_L / B_D / PW_pair / N₁/μ₁ | max B_L, B_D (p) | flagged |
|---|---|---|---|---|
| 0.197–0.218 | 14 | 0.50 / 0.82 / 2.81 / 0.97 | 1.88, 10.5 (1657) | 6: 1531 sN; 1597 sD sPW sN; 1627 sN; 1657 sD sPW sN; 1669 sD; 1693 sD sPW |
| 0.222–0.249 | 15 | 0.55 / 0.59 / 1.77 / 0.82 | 1.77, 14.8 (1789) | 3: 1759 sN; 1789 sD sPW sN; 1933 sD sPW sN |
| 0.251–0.307 | 31 | 0.45 / 0.44 / 1.04 / 0.81 | 1.16, 6.59 (2113) | 8: 2053 sD sPW; 2113 sD sPW sN; 2137 sD; 2143 sD sPW sN; 2179 sD; 2221 sD sPW; 2269 sD sPW; 2341 sD sPW sN |
| 0.492–0.553 | 29 | 0.33 / 0.24 / 0.32 / 0.80 | 0.63, 1.42 (3889) | 4: 3823 sD sPW; 3889 sD sPW; 4057 sPW; 4129 sD sPW |

- **Largest spike: 1789.**
  - B_L 1.77, B_D 14.8 (z 9.2, 2σ upper 16.4), PW_pair 31.7, N₁/μ₁ 4.50, c 2.66.
  - This is the largest B_D measured at any κ; the κ = 4 and 5 maxima are 2.07 and 3.04. It is 25× its band median
    and 18× the λ < 0.22 median.
  - Next is 1657: B_L 1.88, B_D 10.5, PW_pair 30.1, N₁/μ₁ 4.47.
- **Typical primes.**
  - At λ ≈ 0.21 they have B_L 0.32–0.54, B_D 0.38–0.93 and N₁/μ₁ 0.39–1.15.
  - The noise level there is ν_D 0.69–1.18, so most of these B_D values are noise.
  - N₁/μ₁ goes as low as 0.37 (1741), so (N) of OSC′ needs B ≈ 2.7 at these primes. (N) enters only the noise term
    of §11.8, which never dominates.
- **Count spikes without value spikes.** 1531, 1627 and 1759 have N₁/μ₁ 4.11, 2.64 and 1.89 but B_D only 0.63, 1.00
  and 0.49. All three are ≡ 7 (mod 12) (§12.7).
- **N₁/μ₁ is heavy-tailed at spike primes.**
  - Single S with buckets of 10–12 points carry much of the count. At 1933, 71% of the configurations of a 3·10⁶-S run
    come from the top 0.1% of S (`buckets/bucket_k6_p1933.out`).
  - Samples of the same prime differ by up to 1.8×, in no consistent direction. At 1789 the pairsym sample gives 2.53
    and the survey 4.50. At 1933 the largest sample (3·10⁶ S) gives the lowest value, 2.55, against 2.63–3.07
    elsewhere.
  - So the S-batch se understates the uncertainty at spike primes, by a factor of about 2 or more.
- **What "holds" means here.**
  - At fixed κ any finite set of primes satisfies OSC′ with some constants, so the survey measures their size.
  - PW_pair is above 1 at every prime with λ ≤ 0.25; the lowest is 1.14, at 1879. The κ = 6 threshold of §11.8 is
    λ_T = 1.3, so none of these primes is in the range a κ = 6 certificate would use.
  - The first value below 1 is at 2011 (λ 0.259, PW_pair 0.92). At λ ≈ 0.5 the debiased PW_pair is below 1 at all 29
    primes (28 of 29 by the CS upper estimate; §12.10).

### 12.3 symR, a cheap spike indicator [computed]

- **The script.** `sym_rate.py k nS p…` samples the S that are unions of κ/2 pairs of a split involution. Every
  split involution is conjugate to x ↦ −x, so these are S = {±r₁, ±r₂, ±r₃}. It prints:
  - symR, their configurations per S relative to Poisson;
  - the share of those configurations that come from involution-fixed buckets (0.69–0.99 at κ = 6, λ ≤ 0.31);
  - the share f ≈ 7.5/p of such S;
  - C_sym = f·symR.

  10⁵ symmetric S per prime cost about 1% of a survey run.
- **What it omits.** S symmetric under a non-split involution (x ↦ ε/x) are left out. They have no fixed buckets
  and a small rate: 0.56 and 0.89 × Poisson at 1621 and 1657, but 26 ± 13 at 1531. So C_sym is a lower estimate.
- **N₁/μ₁ tracks symR.**
  - Spearman 0.92 over the 29 survey primes with λ ≤ 0.25.
  - N₁/μ₁ ≈ 0.038·symR at λ < 0.22 (log-sd 0.17 over 14 primes, about the size of the sampling errors), and 0.051·symR
    at 0.22–0.25 (log-sd 0.25 over 15 primes).
  - symR also ranks B_L (0.92) and B_D (0.77).
- **Prospective test.**
  - The fit log N₁/μ₁ = −0.14 + 0.98 log symR + 1.93 log λ, on 14 primes, was used to predict every unfinished prime
    (`survey/predictions_N1mu1.txt`).
  - The file's header says 01:20, and its mtime is 01:48. 1699 finished at 01:33, between the two. The fit does not
    use 1699, and the error there is −0.15.
  - The 15 primes with λ ≤ 0.25 that finished since (1699–1879, λ 0.218–0.242) came in with rms log error 0.24 (mean
    +0.04, largest 0.37 at 1879). That is close to the in-sample residual sd of 0.20.
    - They include the largest spike, 1789: 4.50 against a predicted 5.25.
  - At the snapshot, the 6 primes above λ = 0.25 had rms 0.25 (mean +0.06). The largest error is +0.44, at 1951: 1.42
    against 0.91.
  - Final (§12.10): rms 0.19 over all 31 primes in (0.25, 0.31] and 0.13 over the 28 at λ ≈ 0.5. At λ ≈ 0.5 the level
    holds, but the slope is rejected (0.40 ± 0.07 within the band), so there the law has no predictive power.
  - The λ-term rests mostly on the one λ = 0.5 prime 3877. Without it, the λ coefficient is −2.06 instead of +1.93.
    - The prospective primes test it weakly. They sit 0.10 higher in log λ, and they reject the fit without 3877 (mean
      error +0.42, rms 0.47). The referee estimates that they need a coefficient of 2.0 ± 0.6.
    - They do not separate a λ-term from a flatter symR slope. Also, the configuration count changes at p = 1700.
- **symR is not the mechanism.** The fully symmetric S carry C_sym ≈ 1/9 of N₁/μ₁ (median ratio 9.35, quartiles
  7.8–12.4, λ ≤ 0.25). symR measures a property of the prime that also drives the rest of the measure (§12.4).

### 12.4 Partial involution structure of (C1) configurations [computed]

- **Definitions.**
  - A Möbius involution ι is determined by two of its 2-cycles. A κ-set S has N_inv = C(κ,2)C(κ−2,2)/2 pairs of
    disjoint pairs (45 at κ = 6, 105 at κ = 7). Each pair of pairs determines the involution that swaps both, so N_inv
    bounds the number of distinct such involutions.
  - A configuration (S, T) is **2+2 structured** if one of these ι also has two ι-pairs {t, ι(t)} inside T.
  - Over F_p, involutions are split (conjugate to x ↦ −x, two fixed points in P¹(F_p)) or non-split (conjugate to
    x ↦ ε/x, ε a non-square), about half of each.
- **Exact count.** `pairsym.py k p nS` counts, for every full S-bucket, the k-subsets T that are 2+2 structured.
  - It takes the union over ι; a first max-over-ι version undercounted by up to 16 points.
  - `--null` replaces the bucket by a random b-set.

  | p | λ | kind | N₁/μ₁ (same sample) | 2+2 share | 2+2 counting ι-fixed points |
  |---|---|---|---|---|---|
  | 1597 | 0.205 | sD spike | 3.97 | 0.875 | 0.915 |
  | 1621 | 0.208 | typical | 0.42 | 0.741 | 0.786 |
  | 1627 | 0.209 | sN spike | 2.05 | 0.780 | 0.826 |
  | 1657 | 0.213 | sD spike | 3.71 | 0.830 | 0.886 |
  | 1789 | 0.230 | sD spike | 2.53 | 0.736 | 0.805 |
  | 1933 | 0.249 | sD spike | 2.72 | 0.700 | 0.774 |
  | 2347 | 0.302 | typical | 0.80 | 0.444 | 0.514 |
  | 3877 | 0.499 | typical | 0.84 | 0.167 | 0.192 |
  | random b-sets | | null | | ≈ 0.002 (b = 6) | |

  Samples are seed 5 with 3·10⁵ S, except 6·10⁴ at 3877, 1.5·10⁶ at 1621 and 10⁵ at 1789 (the referee's run,
  `review-2026-11-10/scratch/pairsym_k6_p1789_1e5.out`).
- **Only split involutions occur.** At κ = 6 no structured T comes from a non-split ι (0 of 845–1459 per prime;
  §12.5 item 1).
- **Split of the class values.** `mc_split.py` draws the same random stream as `mc_classes.py` and reproduces it
  configuration by configuration; its parts sum to the total. `split_report.py` gives the constants per part, seed 13.

  | p | part | share | N₁/μ₁ | PW_pair | B_L | B_D (z) | c |
  |---|---|---|---|---|---|---|---|
  | 1657 | all | 1 | 4.47 | 30.1 | 1.88 | 10.5 (10.6) | 2.50 |
  | | 2+2 | 0.833 | 3.72 | 33.0 | 2.00 | 11.6 (12.0) | 2.60 |
  | | not 2+2 | 0.167 | 0.75 | 15.9 | 1.35 | 5.8 (3.8) | 2.00 |
  | 1597 | all | 1 | 4.36 | 10.9 | 1.20 | 4.00 (7.4) | 1.53 |
  | | 2+2 | 0.860 | 3.75 | 11.5 | 1.25 | 4.28 (7.9) | 1.57 |
  | | not 2+2 | 0.140 | 0.61 | 7.6 | 0.93 | 2.59 (4.5) | 1.29 |
  | 1933 | all | 1 | 3.07 | 7.25 | 1.24 | 3.84 (7.4) | 1.36 |
  | | 2+2 | 0.762 | 2.34 | 8.23 | 1.32 | 4.42 (7.4) | 1.39 |
  | | not 2+2 | 0.238 | 0.73 | 4.76 | 1.00 | 2.28 (8.2) | 1.25 |
  | 1789 | all | 1 | 4.50 | 31.7 | 1.77 | 14.8 (9.2) | 2.66 |
  | | 2+2 | 0.804 | 3.62 | 36.7 | 1.97 | 17.3 (11.7) | 2.84 |
  | | not 2+2 | 0.196 | 0.88 | 11.9 | 1.06 | 5.5 (3.5) | 1.81 |
  | 1621 | all | 1 | 0.42 | 2.32 | 0.34 | 0.38 (2.4) | 1.03 |
  | | 2+2 | 0.708 | 0.30 | 2.81 | 0.38 | 0.44 (1.7) | 1.07 |
  | | not 2+2 | 0.292 | 0.12 | 3.33 | 0.32 | 0.76 (1.6) | 0.90 |

  Runs have 5000 configurations, except 10⁴ at 1789.
  - The 1597, 1657 and 1621 runs, and the 10⁴-configuration 1789 run, reproduce the survey runs. The 1933 run is the
    first 5022 configurations of the survey's seed-13 stream; the full survey run there has N₁/μ₁ 2.66 and B_D 3.66.
  - At 1789 the split's 2+2 share, 0.804, is higher than the 0.736 of the smaller pairsym sample (heavy tails, §12.2).
- **What the split shows.**
  - The 2+2 share is high at spike and typical primes, and separates them only modestly.
    - At λ ≈ 0.21 it is 0.83–0.88 at the sD spikes 1597 and 1657, and 0.78 at the sN spike 1627. At 1621, the one
      typical prime measured there, it is 0.71–0.74 (se ≈ 0.01).
    - At the spikes 1789 and 1933 (λ 0.23–0.25) it is 0.70–0.80.
  - What separates the four split spike primes from 1621 strongly:
    - the family's weight factor F (§12.5 item 3): 2.3–4.4, against 0.30. Over the survey F carries N₁/μ₁'s
      ranking (Spearman 0.98; §12.11), so a large F and a large N₁/μ₁ are the same observation at κ = 6;
    - the 2+2 part's class values: B_D 4.3–17.3, against 0.44 (z 1.7, 2σ < 0.65).
  - The not-2+2 part is lifted at those spike primes as well: rate 0.61–0.88 μ₁ against 0.12 at 1621, and B_D 2.3–5.8
    (z 3.5–8.2).
  - At 1597, 1657 and 1933 the referee also found the following (not computed at 1789):
    - 39–48% of the not-2+2 part lies in buckets that also hold 2+2 T's.
    - As a whole it points the same way as the 2+2 part, at 0.55–0.73 of the size (weighted cosine 0.97–0.98 over L
      and 0.59–0.92 over D).
    - It carries 1–3% of the total weighted |V|².
  - The data fit one S- and bucket-level property of a spike prime that raises the count and the class values of the
    whole measure. The 2+2 flag marks most of the configurations it acts on. Why some primes have this property is open
    (§12.7).

### 12.5 Weight of involution families [heuristic, except item 3 (a definition) and item 6 (an elementary bound)]

1. **The 4×4 block.**
   - Normalise a split ι to x ↦ −x, with rows (a, −a, b, −b) and columns (x, −x, y, −y). Let h = ind(−1),
     P = ind(r − x) and Q = ind(r + x).
   - Then M[r, x] = P, M[r, −x] = Q, M[−r, x] = h + Q and M[−r, −x] = h + P.
   - Rank 1 holds iff P − Q ≡ c on the whole block, with 2c ≡ 0, and P itself is rank-1.
   - That has probability 2κ⁻⁵ at even κ (c ∈ {0, κ/2}) and κ⁻⁵ at odd κ, against κ⁻⁹ for a generic 4×4 block.
   - Non-split ι(x) = ε/x: each 2×2 pair block needs 2(ind(a − x) − ind(ax − ε)) ≡ −ind ε (mod κ). At even κ there is
     no solution, because ind ε is odd. At odd κ there is exactly one.
   - Averaged over the two kinds, the enhancement is κ⁴ at every κ.
   - Checks:
     - The referee measured the 2×2 rate at κ = 6 as 0.332 for split and 0 for non-split involutions, and 0.143 for
       both at κ = 7.
     - `block_rate.py` (split only, 11 primes, 4·10⁶ samples each) finds 0.87–1.03 of 2κ⁻⁵.
     - Three primes sit 3.3–4.6σ low. The largest deficit is 13.2%. The ratio has rank correlation 0.78 with N₁/μ₁
       (10 primes).
2. **The 2+2 weight.**
   - For a fixed ι, a uniform T contains two ι-pairs with probability ≈ N_inv/p².
   - If the other (κ−1)² − 9 conditions behave independently, the structured rate relative to μ₁ is
     R₂₊₂(κ, p) = N_inv(κ)²·κ⁴/p².
   - κ = 6: R₂₊₂ = 2.62·10⁶/p². That is 1.03 at 1597, 1.00 at 1621, 0.96 at 1657, 0.82 at 1789, 0.70 at 1933, 0.48 at
     2347 and 0.17 at 3877.
   - κ = 7: R₂₊₂ = 2.65·10⁷/p², 0.020–0.023 at the six κ = 7 primes at λ ≈ 0.3.
   - At fixed λ = 0.2 it is 1.1, 0.048 and 0.0010 at κ = 6, 7, 8.
3. **The arithmetic factor F.**
   - Definition: F(p) is the measured 2+2 rate (2+2 share × N₁/μ₁) divided by R₂₊₂(κ, p). So w := F·R₂₊₂ is the
     measured weight, by definition. The heuristic of item 2 predicts F ≈ 1.
   - At κ = 6:

     | p | kind | F |
     |---|---|---|
     | 1597 | sD | 3.4–3.7 |
     | 1627 | sN | 1.6–2.1 |
     | 1657 | sD | 3.2–3.9 |
     | 1789 | sD | 2.3–4.4 |
     | 1933 | sD | 2.5–3.3 |
     | 1621 | typical | 0.30–0.31 |
     | 2347 | typical | 0.7 |
     | 3877 | typical | 0.8 |

     - Each range takes the share and N₁/μ₁ from the pairsym sample, or from the survey, split or largest runs.
     - The largest value, 4.4, is the 1789 split: share 0.804 × N₁/μ₁ 4.50, over R₂₊₂ = 0.82.
     - Between runs F differs by up to 1.9×, in no consistent direction (heavy tails, §12.2).
   - At κ = 7:
     - F is 1.8 at 35281, 0.5 at 35099, 1.6 at 36037 and 0.9 at 34693.
       - The 36037 value comes from its split (§12.6): 185 structured configurations among 6000, S-batch se 0.14.
         pairsym gave 2.3 there, from 28.
       - The others are pairsym's, from 19, 5 and 9 structured configurations.
     - The pairsym counts are clustered: a b = 8 bucket gives up to 8 configurations, and 12 of the 19 at 35281 come
       from b = 8 buckets. So their relative errors exceed the 23–45% of 1/√n.
     - At λ = 0.2, F is 1.16 at 23549 (exact Poisson 95% range 0.4–2.7), from 5 unclustered configurations (§12.6).
   - Across κ = 6 and 7 at λ ≈ 0.3:
     - The 2+2 rate falls from 0.34–0.36 (2347) to 0.010–0.039 (κ = 7; 36037's 0.033 from its split), a drop of
       9–35×.
     - R₂₊₂ predicts 22–23×, and a λ-law predicts none.
     - So the 2+2 baseline weight is not a function of λ alone, and it falls as R₂₊₂ does.
   - At fixed κ the p⁻² fall-off is not visible.
     - At the typical κ = 6 primes 1621, 2347 and 3877, the structured rate is 0.30, 0.34 and 0.14, about p^{−0.9}.
     - Over the same primes R₂₊₂ falls 6×, and F rises from 0.3 to 0.8.
   - F is not predicted by the heuristic, and its maximum over primes is unknown.
4. **General families.**
   - Take g ∈ PGL₂ of order m, with a g-orbits in S and b in T, and set x = am/κ and y = bm/κ.
   - The codimension in (S, T) is c = (a+b)(m−1) − 2. The rank-1 deficit is E = (m−1)(abm − a − b): E = 4 for the 2+2
     block, and κ²/2 − κ for full involution symmetry.
   - With κ^{O(κ)} placements and an O(1) solvability factor, at p = κ^{γκ}:
     log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ).
   - Since xy ≤ (x + y)/2, every family with x + y bounded below is negligible once γ > 1/2 + O(1/κ). Families with
     x + y = O(1/κ) satisfy E/c ≤ κ/2 + O(1), which gives the same conclusion.
   - This assumes that each family's analogue of F is O(1), with no arithmetic enhancement. That is unmeasured.
   - Full involution symmetry (even κ, averaged over the two kinds) has R_full = ((κ−1)!!)²κ^{κ²/2−κ}p^{2−κ}
     (κ = 6: 4.9·10¹¹/p⁴). This is < 1 once p > κ^{κ/2+1−1/ln κ+o(1)}.
5. **Along the threshold path.**
   - The exponent needs OSC′ at T(κ) = κ^{κ/2+κ/(2 ln κ)+O(1)} (§11.8).
     - λ_T is 0.433, 0.182, 0.0685 and 0.0229 for κ = 7–10, from §11.8's log_κ T = 5.57, 6.18, 6.78 and 7.36.
   - There R₂₊₂ = κ^{12−κ−κ/ln κ+O(1)} and R_full = κ^{−κ²/(2 ln κ)+O(κ)}.
   - At the typical-constant thresholds of §11.8, R₂₊₂ is:
     - 0.026 at κ = 6 (p ≈ 10⁴);
     - 0.010 at κ = 7 and 0.0012 at κ = 8;
     - 1.1·10⁻⁴ at κ = 9 and 7.6·10⁻⁶ at κ = 10.
   - With the largest measured G (about 2, κ = 7; §12.12), the share s = G·R₂₊₂ at the thresholds is about 2% at κ = 7
     and 0.24% at κ = 8.
6. **The family's effect on the constants** [elementary, given the definitions; restated in G on 10 Nov, §12.12].
   - Let the family have share s of the (C1) measure and noise-subtracted absolute D-group rms v.
     - V is linear in the measure, and the weighted rms is a norm. So, for population quantities,
       ρ_D ≤ (1 − s)ρ_rest + s·v.
     - Write s = G·R₂₊₂, with G = s/R₂₊₂ = F·μ₁/N₁ (§12.12). An earlier version wrote s = F·R₂₊₂/(N₁/μ₁) and took
       N₁/μ₁ = 1. That applied N₁/μ₁ = 1 to κ = 6 data where it is up to 4.5, so its illustrations were about 4.5× too
       large; they are corrected below.
   - So the family adds at most G·v·N_inv²κ²/p to B_D (units κ²/p).
     - At T(κ), N_inv²κ²/p is 10.6, 7.4, 3.9 and 1.7 for κ = 7–10.
     - It tends to 0 like κ^{10−κ/2−κ/(2 ln κ)+O(1)}.
   - G·v at the five split primes (v from the 2+2 part's B_D; 1933's v is from its earlier split, so approximate):
     - 0.007 at 1621 and 0.10 at 1933;
     - 0.08 at 1597 and 0.22 at 1657;
     - 0.34 at 1789.

     That is about a 50× spread. At κ = 6, G is capped by s ≤ 1 (§12.12), so these are illustrations.
   - What the family would add at T(κ) depends on how v scales from p ≈ 1800 to T(κ):
     - If its absolute D-rms v keeps 1789's value, it would add about 3.6, 2.4, 1.3 and 0.7 at κ = 7–10. Its B_D in
       κ²/p units then grows about 21× by T(7).
     - If its B_D keeps 1789's 17.3 (in κ²/p units, as a constant-B law would have it), it would add s·17.3: about 0.17
       at κ = 7 and 0.02 at κ = 8.
     - With 1621's values (2σ, absolute v fixed), it adds at most about 0.12, 0.07, 0.05 and 0.02.
     - OSC′ is stated for every p ≥ p₀, so what matters is the largest G·v over primes near T(κ). That is not measured
       at any κ ≥ 7. These scale 1789's capped κ = 6 G; at κ = 7 the measured G reaches 2.
   - **Without v.**
     - |Q| ≤ n, because each symmetrised character has modulus ≤ 1. So v ≤ n.
     - The family then adds at most G·N_inv²κ²·(n/p) to B_D and G·N_inv²κ⁴·n/p² to B_L. Both are G·κ^{O(1)}.
     - Tolerances (§11.8): an exponent below κ survives while log_κ B_D < (1 − 1/ln κ)κ − O(1) and
       log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1). The exponent (1/2+o(1))κ needs both to be o(κ). The family adds to both.
     - So the 2+2 family can spoil the (1/2+o(1))κ exponent only if G = κ^{Ω(κ)} at some p ≥ p₀ near the threshold
       path. This step needs no (N). (It replaces the earlier "F·B = κ^{Ω(κ)}", which is never stronger: G ≤ F·B
       under (N).) The bound is asymptotic only: at κ = 7–10 it certifies nothing (§12.12).
     - This needs no independence assumption, since G is defined from the measured share.
   - The L group gains about s·v_L ≈ 0.02 at κ = 7 with the 1789 values.
7. **What this does not say.**
   - Items 2, 4 and 5 are first-moment counts with an independence assumption. Item 6 does not need it, but it bounds
     the family's effect only in terms of G, which nothing beyond the trivial cap 1/R₂₊₂ bounds.
   - It concerns projective families of bounded orbit type.
   - It says nothing about the not-2+2 part at spike primes, or about structure that is not projective.

### 12.6 κ = 7 [computed]

- **Runs.** `bucket_stats.py 7 p 2·10⁵ --seed 21` gives configurations per S against Poisson, the occupancy law and
  its tail, from uniform S. `pairsym.py 7 p 10⁵` gives the 2+2 share.

  | p | λ | symR | N₁/μ₁ | var/mean | b = 7, 8 vs Poisson | 2+2 share |
  |---|---|---|---|---|---|---|
  | 35281 | 0.300 | 15.8 | 0.90 ± 0.05 | 0.999 | 0.95, 0.92 | 0.043 |
  | 34469 | 0.293 | 16.7 | 0.91 | 0.999 | 0.88, 1.15 | |
  | 35099 | 0.298 | 21.3 | 0.96 | 0.999 | 0.93, 1.07 | 0.011 |
  | 34259 | 0.291 | 22.1 | 1.11 ± 0.08 | 0.999 | 1.06, 1.07 | |
  | 36037 | 0.306 | 44.2 | 1.09 ± 0.06 | 0.999 | 1.01, 1.42 | 0.045 |
  | 34693 | 0.295 | 44.2 | 0.89 ± 0.05 | 0.999 | 0.91, 0.97 | 0.021 |
  | 23549 | 0.200 | 67.4 | 0.84 ± 0.09 | 0.999 | 0.91, 0.54 (2 buckets) | 0.063 |

  The se include the bucket clustering. 23549 used 6·10⁵ S.
- **Carry-over test at λ ≈ 0.3.**
  - The two primes with the largest symR (44, against 9.4–22 at eleven others at λ ≈ 0.3) have N₁/μ₁ 1.09 and 0.89.
  - Over the six primes N₁/μ₁ = 0.89–1.11. There is no detectable rank relation to symR: n = 6, and Spearman is 0.09,
    or 0.31 if the two near-equal symR values are swapped.
  - The κ = 6 proportionality would give about 2.5 at symR 44. At κ = 7 symR no longer predicts the measure, as
    expected when the 2+2 weight is 2%.
  - This tests carry-over of the κ = 6 behaviour, not §12.5. The 2+2 weight F·R₂₊₂ ≈ 0.02·F (measured 0.010–0.048)
    moves N₁/μ₁ by that much, below these se. The informative κ = 7 number is F (§12.5 item 3).
- **λ = 0.2.**
  - 23549 has the highest symR of the κ = 7 primes sampled (67), and R₂₊₂ = 0.048 there.
  - Measured N₁/μ₁: 0.84 ± 0.09 (0.12 with Poisson bucket sizes), from 151 configurations in 6·10⁵ S (135 from b = 7
    buckets, 16 from two b = 8 buckets; `buckets/bucket_k7_p23549.out`). The pairsym sample gives 0.88; together,
    0.85 ± 0.08.
    - So the κ = 6 proportionality (about 2.5 at symR 67) fails at λ = 0.2 as well.
    - N₁/μ₁ alone is consistent with the R₂₊₂ reading but does not discriminate. The 2+2 count does.
  - Measured 2+2 share: 0.063 (`pairsym/pairsym_k7_p23549.out`, `pairsym.py 7 23549 300000`: 5 of 79 configurations,
    all from b = 7 buckets, so unclustered).
    - The R₂₊₂ law at F = 1 gives 5.4–5.7%.
    - F(23549) = 1.16 (1.1–1.2 with either N₁/μ₁). The exact Poisson 95% range is 0.4–2.7.
  - **The test is the weight, not the share.**
    - The share also depends on the not-2+2 rate. That is (1 − 0.063)·(0.84–0.88) = 0.79–0.82 μ₁ here, against 0.12
      at 1621. A λ-only weight on top of 23549's not-2+2 rate would give a share of 0.28, not 0.7–0.9.
    - The 2+2 weight here is w = 0.055 μ₁. At κ = 6, λ ≈ 0.21 it is 0.31 at 1621 (the smallest measured) and 1.6–3.5
      at the spikes 1627, 1657 and 1597.
    - With a weight depending on λ alone, this run would have about 28 (1621's weight) to 314 2+2 configurations. It
      has 5. The Poisson probability is about 10⁻⁷ even at 28, and buckets with b ≥ 8 are too rare to hide the
      difference in clusters.
  - So at λ = 0.2 the 2+2 weight drops from κ = 6 to κ = 7 by 5.6× against 1621 and 29–63× against the spikes. R₂₊₂
    predicts 20–22×. That is "as R₂₊₂ predicts, up to F": F(23549) lies inside κ = 6's 0.3–4.4 and κ = 7's 0.5–2.3.
  - The run rejects a λ-only weight. It does not distinguish R₂₊₂ from other κ-scalings within about 10×. It is one
    prime and 5 events.
- **Class values at 36037** [computed]. The run is `mc_classes.py 7 36037 10⁴ --seed 13`, 1.57·10⁶ S.
  - The analysis is in `review-2026-11-10/scratch/k7_class_values.out` and `pw_bin_cs_k7.out`, and the referee's check
    in `r3c_checks.out` (round 3c of `ROUND3.md`).
  - 36037 was picked on symR (the highest at λ ≈ 0.3, with 34693) before its F or class values were known. Its F is
    1.6 (split, below). pairsym's 2.3, from 28 clustered configurations, was 1.5× too high. 35281's pairsym 1.8 is
    within that error, so the κ = 7 ranking by F is not resolved.
  - N₁/μ₁ is 1.08, so it is not a count spike.
  - **B_L.**
    - It is 0.635 (z 6.9, 2σ 0.54–0.72). At 47041 and 58787 (λ 0.40, 0.50) the same estimators give 0.22 and 0.27.
    - Every resolved L bin is lifted against 47041: (0,3) 3.70 against 0.44, (2,2) 3.78 against 1.65, (2,3) 0.53
      against 0.03, (3,3) 0.25 against 0.02. (2,2) and (0,3) carry 63% and 19% of B_L².
    - The lift is not a heavy-tail or cluster effect. All 16 S-batches contribute positively to B_L, and leaving out
      any two keeps it ≥ 0.58 (checked). The referee also finds every half-sample of 8 batches ≥ 0.51, and z 4.8–9.8 on
      8 super-batches.
  - **B_D.**
    - It is 9.4 (z 1.6), < 14.1 at 2σ, so its size is not resolved.
    - Its sign is consistent (checked). It is positive in every batch, the exact sign-flip test gives p ≈ 3·10⁻⁵, and
      it stays ≥ 5.6 leaving out any one or two batches.
    - But two batches carry 45% of it. All 17 m ≥ 7 bins have positive z (0.6–2.2), yet their batch profiles correlate
      at 0.97 (referee), so this is one effect.
    - At 47041 and 58787, B_D is < 2.6 and < 2.1 at 2σ.
  - L and D share these batches (profile correlation 0.94, referee), so they are not independent evidence.
  - PW_pair is 2.71 (null floor 1.00, CS upper 3.08). 92% of it is D-group weight, so it repeats the B_D excess. At
    47041 and 58787 PW_pair sits at its null floor.
  - **Comparison.**
    - From λ 0.4–0.5 to 0.31, B_L rises 2.4–2.9×. At κ = 6 it rises 1.1–1.5× from λ ≈ 0.5 to 0.30 (2347, B_L 0.41,
      against 0.27–0.37).
    - In the complete κ = 6 survey the median B_L is 0.45 in (0.25, 0.31] and 0.33 at λ ≈ 0.5, a rise of 1.4×. The
      band maximum is 1.16, at the spike 2113 (§12.10).
  - **The equal-λ comparison 35099** (λ 0.298; `mc_classes.py 7 35099 6000 --seed 13`, 1.29·10⁶ S; the 17 MB npz is
    kept outside the repo). The checks are in `review-2026-11-10/scratch/r4b_checks.out` (referee rounds 4b and 4c).
    - It was picked as the middle symR of the table above: 21.3, 10th of the 13 λ ≈ 0.3 primes in
      `sym/sym_rate_k7_lam03.out`, whose median is 16.3.
    - Its F, 0.5, the lowest at κ = 7, was known when it was picked. F rests on 5 configurations, so its Poisson 95%
      range is about 0.16–1.2. At κ = 6 rates the above-median symR would raise its B_L, and the low F might lower it.
    - B_L is 0.237 (z 8.2, 2σ 0.21–0.26). It is stable: all 16 batches contribute positively, leaving out any two
      keeps it ≥ 0.225, and half-samples range over 0.18–0.30.
    - B_D is 1.76 (z 0.7, < 3.4), with no consistent sign (sign-flip p 0.12). N₁/μ₁ is 0.95 ± 0.02. PW_pair sits at
      its null floor (0.93 against 0.90; CS upper 0.53).
    - Its L bins match 47041's: (2,2) 1.67 against 1.65, and (0,3) 0.65 against 0.44.
  - **Against 35099, 36037 is a spike in B_L by the test set in §12.9.** 34847 (below) confirms it under a rule
    written before its run.
    - Its B_L is 2.7× 35099's at nearly equal λ (0.306 against 0.298). 35099's 2σ upper end, 0.264, is less than
      half of 36037's 2σ lower end, 0.535. 36037's smallest half-sample value, 0.51, is 1.7× 35099's largest, 0.30.
    - Every resolved L bin is lifted. The central ratios are given first, then 36037's 2σ lower end over 35099's 2σ
      upper end:
      - (2,2) 2.3× (≥ 1.9×);
      - (0,3) 5.7× (≥ 3.4×);
      - (2,3) 13× (≥ 6.0×);
      - (3,3) 12× (≥ 5.6×).
    - (0,4) and (2,4) are resolved at 36037 (z 3.8 and 2.6) and are noise at 35099 (≥ 2.9× and ≥ 4.2×).
    - (2,2) and (0,3) carry 81% of the rise in B_L².
    - At κ = 7, B_L at the comparison primes does not rise from λ 0.5 to 0.3: it is 0.27, 0.22 and 0.24 (35099 and
      34847) at λ 0.5, 0.4 and 0.3. At κ = 6 the band medians rise 1.4× (0.33 to 0.45).
    - 36037's D excess has a consistent sign, which 35099's does not, but its size is unresolved.
    - F is 1.6 against 0.5 (0.16–1.2). The split (below) shows that the B_L lift does not come from the 2+2
      configurations, so a large F does not explain it here.
    - 36037 is neither sD nor sN, and B_L is not one of the κ = 6 flags. Its PW_pair (2.71, against 0.93–0.96 at the
      comparison primes) would raise sPW by the κ = 6 rule. PW_pair reads the same class values as B_L, so that is not
      independent evidence, but "neither sD nor sN" does not mean unflagged.
  - **The calibration was the weak point** (referee round 4c), until 34847.
    - At κ = 6, two unflagged primes at equal λ differ by as much: 2281 (λ 0.293, B_L 0.663) and 2293 (λ 0.295, B_L
      0.248), 2.67×. So a ratio to one comparison prime cannot separate a spike from the two ends of a wide typical
      spread.
    - The better reference is the band median. Unflagged κ = 6 primes reach at most 1.08, 1.22, 1.46 and 1.54× their
      band median, from λ ≈ 0.21 to λ ≈ 0.5. Spikes reach 3.74, 3.25, 2.56 and 1.94×.
    - 36037 is 2.6× the mean of the three κ = 7 comparison primes measured before 34847, one per λ. That makes it a
      spike if they sit near the κ = 7 median at λ ≈ 0.3.
    - If 35099 sat at the bottom of a κ = 6-like spread (0.55× the median), the median would be about 0.43. 36037 would
      then be 1.47× it, at the top of the unflagged range.
    - That worst case is extreme. It needs 35099 below 0.58× the κ = 7 median, and at κ = 6 only 2 of the 68
      unflagged primes are (1741 and 2293). If 35099 sat at the 5%, 10% or 25% point of the unflagged ratios, 36037
      would be 1.74×, 1.83× or 2.27× the median.
    - A second equal-λ prime was run to decide this: 34847, the median symR of the 13 (16.3), with its F and class
      values unknown. Its rule was written before the run (`predictions_k7_p34847.txt`, 05:48):
      - a spike if B_L(34847) ≤ 0.41 and its 2σ upper end is below 0.535;
      - not shown to be a spike if B_L(34847) ≥ 0.43;
      - otherwise inconclusive.
    - An addendum (05:52, result unknown) asks for both 2σ ranges to be reported. The call is marked "close" if the 2σ
      range of B_L(34847) crosses 0.41 or 0.43.
  - **34847** (λ 0.296; `mc_classes.py 7 34847 6000 --seed 13`, 1.38·10⁶ S; the 17 MB npz is kept outside the repo).
    It is scored by `review-2026-11-10/scratch/score_k7_34847.py` (written 05:56, before the result) → `.out`. Bins and
    robustness are in `k7_34847_bins.out`; referee round 4e is in `r4e_checks.out`.
    - B_L is 0.245 (z 9.4, 2σ 0.218–0.270). **By the rule, 36037 is a spike in B_L against two equal-λ primes.** The
      call is not close, and the prediction (B_L in 0.20–0.32) held.
    - **Superseded as a spike claim by the seven-prime band (mechanical item 6, below): not shown.** The
      ratio-to-median argument above, and the 0.1% / 1.2% probabilities and "2.4× the implied band median against
      ≤ 1.46×" below, assume that the κ = 6 spread carries over. At κ = 7, λ ≈ 0.3 it does not.
    - It is stable: all 16 batches contribute positively, leaving out any two keeps it ≥ 0.233, and half-samples range
      over 0.18–0.30. 36037's smallest half-sample, 0.51, is 1.7× 34847's largest.
    - 36037 is 2.6× it (2σ 2.1–3.1 by the delta method, 2.0–3.3 from the ends). Every resolved L bin is lifted against
      34847 too. Central ratios, then 36037's 2σ lower end over 34847's 2σ upper end:
      - (2,2) 2.0× (≥ 1.6×);
      - (0,3) 9.6× (≥ 4.2×), though (0,3) is unresolved at 34847 (0.39, z 0.9, against 0.65 at 35099);
      - (2,3) 16× (≥ 6.0×);
      - (3,3) 11× (≥ 4.2×);
      - (0,4) and (2,4) are noise at 34847, and 36037 is ≥ 2.5× and ≥ 3.8× its 2σ upper ends.
    - Otherwise it matches 35099: B_L 1.03× (0.245 against 0.237), and (2,2) 1.93 against 1.67. B_D is 0 (z −0.7,
      < 2.3), N₁/μ₁ is 0.93 ± 0.04, and PW_pair sits at its floor (0.955 against 0.930; CS 0.20).
    - So the round-4c worry is answered as far as two primes can answer it (wording of referee round 4e).
      - The worry was that 35099 might sit at the bottom of a κ = 6-like spread. 34847 was picked at the median symR,
        with its F and class values unknown. Its B_L, 0.245, is 1.03× 35099's.
      - All three κ = 7 runs use seed 13 and so share their S positions, but their class values are uncorrelated at
        batch and cell level, so this is not a seed artifact. Future comparison primes get distinct seeds.
      - The agreement itself is weak evidence: at κ = 6, 10% of unflagged same-band pairs agree to within 1.03×. What
        counts is that both primes are low.
      - [Superseded by the band, below.] If 36037 were at most the κ = 6 unflagged maximum (1.54× the band median), both comparison primes would have to
        lie below 0.6× the κ = 7 median. At κ = 6, 2.9% of unflagged primes do, so for two independent primes the
        chance is about 0.1%, or 1.2% with 36037 at its 2σ lower end. This assumes that the κ = 6 spread carries over
        and that picking by symR does not bias B_L.
      - The two primes average 0.241, and 36037 is 2.6× that. Both look unflagged, and at κ = 6 the unflagged median is
        about 10% below the all-prime median in (0.25, 0.31] (0.413 against 0.454). So 36037 is about 2.4× the implied
        band median, against at most 1.46× for unflagged κ = 6 primes in that band and 2.56× for its largest spike.
  - **The 2+2 split of 36037** (`mc_split.py 7 36037 6000 --seed 13`: the first 6000 of the run's 10⁴
    configurations, 9.5·10⁵ of its 1.57·10⁶ S; npz outside the repo). It is analysed in
    `review-2026-11-10/scratch/split36037_decomp.py` → `.out`, with referee round 4d in `r4d_checks.out` and
    `r4d_k6_align.out`.
    - The split's all part is the run's prefix: B_L 0.623 (z 5.4), against 0.635 for all 10⁴ configurations.
    - The 2+2 share is 3.1% ± 0.3% (185 configurations; the S-batch se includes the bucket clustering), so F is
      1.6 ± 0.14. pairsym's 4.5% (28 of 624) is 1.7 binomial se above it, and less with its clustering; the split
      supersedes it.
    - Without the 2+2 configurations B_L is 0.573 (z 6.6, 2σ 0.48–0.65), 2.4× 35099's (≥ 1.8× at the 2σ ends). All 16
      batches contribute positively, and its smallest half-sample, 0.45, is above 35099's largest, 0.30.
    - With c_q,b = S1_q,b/cnt_all,b, X_L(all) splits exactly into 2+2 alone 1.5 ± 0.7%, rest alone 79 ± 5% and cross
      19 ± 4% (jackknife), so the 2+2 configurations account for 21 ± 5%. The two parts are in phase (cos 0.89). In
      amplitude, removing the 2+2 configurations lowers B_L from 0.62 to 0.56.
    - In every lifted L bin the rest alone is lifted against 35099's whole run: (2,2) 2.1×, (0,3) 5.1×, (2,3) 10.7×,
      (3,3) 10.0×, and 1.7×, 3.1×, 4.6×, 3.8× from the 2σ ends. (0,4) and (2,4) are noise at 35099 but resolved in the
      rest (≥ 2.7× and ≥ 2.0×). In these bins the rest alone makes 57–85% of the bin's X and the cross term 15–37%.
    - 35099 is not split. Its own 2+2 part cannot plausibly close the gap. At pairsym's 1.1% share it would need an
      own-scale B_L ≥ 19 pointing against the rest; 36037's is 2.2 (< 3.1 at 2σ). In all 17 splits on file the two
      parts point the same way in L (cos +0.68 to +0.99).
    - **Hence "the lift is a 2+2 effect" is refuted for B_L at 36037, against 35099.** The 2+2 configurations (3.1%)
      add about 0.07, in phase with the rest. "Not 2+2" means mc_split's flag, and other structure in the rest (one
      ι-pair, involutions of other cycle types, order-3 symmetry) is unexamined. B_D is not covered: it stays
      unresolved, and about half its X involves the 2+2 configurations.
    - The 2+2 part alone is unresolved: 185 configurations, own-scale B_L 2.2 at z 2.0 (< 3.1 at 2σ). Across the 17
      splits on file its own-scale L amplitude is 1.1–2.0× the rest's at κ = 6 and 3.8× at 36037. So in L it carries
      nearly the rest's profile, amplified. That describes 17 runs; it is not a mechanism.
- **34693, the other prime with 36037's symR** [computed; pre-registered; referee round 4h-b]. Mechanical item 5. The
  rule was written at 10:59:29, before the run (`predictions_k7_p34693.txt`); `mc_split.py 7 34693 6000 --seed 17`
  gave 6007 configurations. Scored by `review-2026-11-10/scratch/score_k7_34693.py` → `.out`; referee checks in
  `scratch/r4hb_checks.out`.
  - **Call: INCONCLUSIVE.** Its not-2+2 B_L is 0.386 (2σ 0.374–0.398). That is above the comparison primes (upper
    ends ≤ 0.270) and below the LIFTED threshold 0.40. It is not close by the rule's definition, but the upper end is
    only 0.002 below 0.40. The prediction (0.22–0.35) failed.
  - The whole run gives 0.387 (2σ 0.375–0.398): 1.60× the comparison mean, and 36037's whole run is 1.64× it. So the
    four κ = 7 primes at λ ≈ 0.3 sit at three separated levels (≤ 0.270; 0.374–0.398; ≥ 0.535 at the 2σ ends). With
    the band below, the nine primes sit at four or more levels, and 34693 is inside the band.
  - The narrow range is real: 95% of X_L is in the (2,2) bin, spread evenly over six cells that agree from batch to
    batch (y_b > 0 in 16 of 16, cv 0.05; half-samples 0.363–0.410). se/X is 0.03, against 0.11–0.15 at the other three.
  - The excess is mostly in (2,2). (0,3), (3,3) and (0,4) are also above the comparison primes. Less of X lies
    outside (2,2) than at 36037 (5% against 37%).
  - The 2+2 share is 0.023 (139 configurations), so G is 1.05 (pairsym 0.96) and F 0.95.
  - B_D is noise-level (X_D −80 ± 69; < 1.6 at 2σ in κ²/p units). 36037's is unresolved too (z 1.6), so the D group
    separates neither from the comparison primes. PW_pair is at its floor (0.94 against 0.90), against 2.71 at 36037;
    this is not decomposed.
  - Post hoc: the two equal-symR primes differ 1.64× in B_L, though both sit above both low-symR primes (35099 21.3,
    34847 16.3), an ordering of probability 1/6 at random. symR does not fix B_L at κ = 7, and four primes support
    no correlation.
  - Gates stay false: 34693 lifted or 34693 like the comparison primes; a spike/typical dichotomy at κ = 7, λ ≈ 0.3;
    any symR–B_L relation at κ = 7.
- **The κ = 7 band at λ ≈ 0.3** [computed; pre-registered; referee round 4j]. Mechanical item 6. The rules were
  written at 12:24:39 (`predictions_k7_lam03_band.txt`), and the runs started at 12:24:45–46: `mc_classes.py 7 p 6000`
  at seeds 19–27, with npz files outside the repo. The scorer `review-2026-11-10/scratch/score_k7_band.py` → `.out` was
  saved at 15:26:46, after the results. It applies the rules as written, and the referee reproduced the calls by an
  independent path (`scratch/r4j_checks.out`).

  | p | λ | symR | N₁/μ₁ | B_L (2σ) | B_D (< 2σ) | PW_pair [floor] |
  |---|---|---|---|---|---|---|
  | 34259 | 0.291 | 22.05 | 1.045 | 0.519 (0.412–0.608) | 1.79 (< 3.33) | 1.17 [1.02] |
  | 34273 | 0.291 | 9.43 | 0.964 | 0.236 (0.199–0.268) | 0 (< 2.81) | 0.96 [0.93] |
  | 34469 | 0.293 | 16.69 | 0.947 | 0.131 (0.096–0.158) | 1.57 (< 3.57) | 0.93 [0.92] |
  | 34847 | 0.296 | 16.26 | 0.934 | 0.245 (0.218–0.270) | 0 (< 2.33) | 0.96 [0.93] |
  | 35099 | 0.298 | 21.33 | 0.950 | 0.237 (0.206–0.264) | 1.76 (< 3.38) | 0.93 [0.90] |
  | 35281 | 0.300 | 15.79 | 0.943 | 0.392 (0.373–0.410) | 1.06 (< 2.95) | 0.96 [0.91] |
  | 36541 | 0.311 | 15.32 | 0.951 | 0.393 (0.366–0.419) | 0 (< 1.83) | 0.97 [0.92] |
  | 34693 (picked on symR) | 0.295 | 44.22 | 0.906 | 0.387 (0.375–0.398) | 0 (< 1.61) | 0.94 [0.90] |
  | 36037 (picked on symR) | 0.306 | 44.19 | 1.080 | 0.635 (0.535–0.721) | 9.4 (< 14.1) | 2.71 [1.00] |

  - **The band** is the seven primes not picked on symR. Its median is 0.245 and its range 0.131–0.519 (4.0×).
    Ratios to the median run 0.53–2.12, so 3 of the 7 exceed κ = 6's unflagged maximum of 1.54×, and 34259's 2.12× is
    inside κ = 6's spike range. At 2σ the band splits into at least three separated levels.
  - **R1: NOT SHOWN.** 36037's 2σ lower end, 0.535, is below 34259's upper end, 0.608, and 34259's point value 0.519 is
    ≥ 0.50. 36037 is still 2.6× the band median. R1 rests on 34259 alone: without it, 36037 would score SPIKE (0.535
    against 0.419). The rule text lists SPIKE before NOT SHOWN while the scorer tests NOT SHOWN first; that is
    immaterial here, because SPIKE fails. Future rules should say which clause wins.
  - **R2: INSIDE.** 34259, 35281 and 36541 are all at or above 34693's 0.387.
  - **R3: inconclusive.** Spearman ρ(symR, B_L) is 0.350 over the nine primes, and 0.18 over the seven band primes (not
    pre-registered).
  - **Predictions:** "each new prime in 0.18–0.35" failed (4 of 5 outside), and so did "R1 SPIKE" and "R2 ABOVE". The
    band median (0.22–0.30) and R3's ρ range held.
  - **Credibility (referee):** at 34259 every batch contributes positively, leave-one-out gives 0.471–0.527,
    half-samples 0.432–0.605, and no single cell carries it (14%). 34469 is noisier, but its 2σ upper end (0.158) is
    below the lower ends of 34273, 34847 and 35099, so it is genuinely low.
  - **Post hoc, not a claim:** 34259 looks like a milder 36037. 0.78 of its X_L is in (2,2) and 0.15 in (0,3). It has
    N₁/μ₁ 1.045, PW_pair 1.17 and the highest symR in the band.
  - **The 34259 split** (mechanical item 7; rule `osc-mc/predictions_k7_p34259_split.txt`, written before the run;
    `mc_split.py 7 34259 6000 --seed 19`; scored by `review-2026-11-10/scratch/score_k7_34259.py` → `.out`; referee
    round 4k-b part 2).
    - The 'all' part is identical to the band run (B_L 0.519), so the calls stand.
    - **Q1: REST-LIFTED (close).** Without its 193 2+2 configurations, B_L is 0.499 (2σ 0.41–0.58). Q1 was nearly
      implied once the share was typical.
    - **Q2: TYPICAL.** The 2+2 share is 3.2% (batch se 0.5%; the batch counts are over-dispersed, so the binomial se
      is not used). G = 1.43, F = 1.49.
    - **Decomposition of X_L:** 2+2 alone 0.6%, rest alone 85.9%, cross term 13.5% (aligned with the rest). Removing
      the 2+2 part lowers B_L by 3.9% on the own scale (36037: 8.1%).
    - **One batch** holds 41 of the 193 2+2 configurations and ranks first for the rest too. Without it the rest is
      0.459 (2σ 0.43–0.49), the share 2.75% and G 1.22. Both calls are unchanged.
    - **Reading:** 34259's high B_L is not carried by the 2+2 family, as at 36037. Its rest is 2.1× the low band
      prime 35099 (≥ 1.55× at 2σ), but only 1.27× the band's upper pair 35281 and 36541, from which it is not
      separated. Both primes were selected high, so this describes two primes; it is not a class.
    - All three predictions held: REST-LIFTED with 0.42–0.55, share 1.5–4% with G 0.6–2, and 2+2 under 40% of X_L.
    - **Gates stay false:** "a κ = 7 not-2+2 spike class" or "a not-2+2 mechanism"; "34259's rest lifted against
      the band"; "34259 is a spike"; robustness to its largest batch beyond the stated leave-out values; "high-B_L
      primes at κ = 7 have typical 2+2 shares".
  - **What it means for obstruction (c):** neither resolved nor made worse. A 4.0–4.85× spread is 0.71–0.81 in
    log₇, against the κ = 7 L tolerance of 1.70. One κ cannot measure growth with κ. What changes is the framing: at
    κ = 7, λ ≈ 0.3 large B_L values are not isolated spikes against a tight typical level, so the question becomes
    controlling the spread, or its upper tail.
  - **Gates stay false:** "36037 is a spike" in any form beyond the two-prime call; "34259 is a spike"; "κ = 7 spikes
    are rarer, or more common, than κ = 6's"; "symR predicts B_L at κ = 7".
- **Generic rate.**
  - The not-2+2 rate is 0.86–1.04 μ₁ at κ = 7, λ ≈ 0.3 (bucket_stats rates at the four primes with a share), and
    0.79–0.82 μ₁ at 23549 (λ = 0.2).
  - At κ = 6 it is 0.44 at λ ≈ 0.3 (2347), and 0.12 and 0.70 at λ = 0.21 and 0.50 (1621 and 3877). That is one
    prime each, and 1621 is in the bottom third of its band.
  - So the κ = 6 shortfall of generic configurations is not a function of λ alone: at λ ≈ 0.3, and at λ = 0.2 on one
    κ = 7 prime.

### 12.7 Arithmetic of spike primes [computed; post hoc]

- **B_D > 2 occurs only at p ≡ 1 (mod 12)** (h = ind(−1) ≡ 0 mod 6).
  - At λ ≤ 0.25 (complete) that is 6 of the 15 primes ≡ 1 (mod 12): 1597, 1657, 1669, 1693, 1789 and 1933. It is 0 of
    the 14 primes ≡ 7 (mod 12), where the largest B_D is 1.00 (1627).
  - Over all 89 primes it is 8 of 43 against 0 of 46 (post hoc; §12.10).
  - The post hoc evidence at λ ≤ 0.25 is weak:
    - H was formed on 17 survey primes, plus earlier S-batched runs (1933 at seed 11 among them).
    - With the cut at 2, the one-sided probability at λ ≤ 0.25 is 0.011 (C(15,6)/C(29,6)). With the residue
      partitions looked at and the cut chosen, it was 0.14–0.25 at n = 25 (referee, round 2).
    - An exact rank test of B_D by class gives one-sided 0.018 at λ ≤ 0.25 (n = 29).
    - At the 35-prime snapshot (the final scoring is in §12.10): H was pre-registered for the primes that finish after
      02:16, less 1933's rerun (known), which were 16 primes at the snapshot. 1759 (file written at 02:14–02:16, not looked at) is in neither the formation set nor the test set.
      On the 16 the same test gives 0.010. But h = 3 primes are 4 of the 6 above λ = 0.25 there. Restricted to the 10
      at λ ≤ 0.25 it gives 0.057.
  - Class medians (λ ≤ 0.25): B_D 0.93 against 0.56; N₁/μ₁ 1.16 against 0.67.
  - Pre-registered predictions (`survey/predictions_hclass.txt`), scored in §12.10: (H1) is refuted by 2143 (≡ 7 mod
    12, sD). (H2) held as pre-registered, and (H3) holds. So the data support a shift of B_D towards p ≡ 1 (mod 12),
    not value spikes only there.
  - The count spikes without value spikes (1531, 1627 and 1759) are all ≡ 7 (mod 12).
- **No mechanism is known.**
  - For a configuration fully symmetric under x ↦ −x, z and −z contribute equally whatever h is. This is because the
    class modes are sum-zero and taken up to cyclic shifts of the values.
  - For 2+2 configurations only the paired coordinates are shifted copies.
  - So this excludes h acting through the z ↔ −z pairing, not h acting at all. The order-6 cyclotomic numbers remain a
    route.
  - At odd κ, h = 0 for every p.
- **What ranks symR.**
  - Write p = a² + 3b², with a ≡ 1 mod 3. Log symR, detrended by a log–log fit in p on all 89 primes, rises with
    |a|/√p.
    - Spearman is 0.53 at h = 0 and 0.47 at h = 3 (30 primes each, λ ≤ 0.31), and 0.50 over all 60.
    - At h = 0 this holds whether or not 2 is a cubic residue (0.64 and 0.62). At h = 3 it sits in the cube subclass:
      0.79 (n = 13), against 0.19 (n = 17).
  - |a|/√p is |cos| of the argument of the associate a + b√−3 of the cubic Jacobi sum.
    - It equals §11.6's |L|/(2√p) (4p = L² + 27M²) only when 2 is a cubic residue, which holds at 25 of the 60 primes.
      Otherwise |L| = |a ± 3b|.
    - |L|/(2√p) itself has Spearman 0.09 with the residual, consistent with its failure as a predictor in §11.6.
  - At h = 0 the residual is also higher when 2 is a cubic residue: median +0.57 against −0.05. At h = 3 there is no
    such effect (−0.30 against −0.38).
  - The fixed cyclotomic cell combines both effects at h = 0.
    - When 2 is a cube, 36A(0,0) = p − 17 − 20a exactly (a ≡ 1 mod 3, checked at 17 primes). So
      |A(0,0) − mean|/√p = |20a + 15|/(36√p) ≈ (5/9)|a|/√p.
    - Otherwise it is ≤ 0.25.
    - Hence its Spearman of 0.81, against 0.27 for A(0,3).
  - All of this is post hoc.
- **Other statistics** (λ ≤ 0.25, n = 29): K has Spearman 0.78 with N₁/μ₁ and 0.56 with B_D; max|D|/√p has 0.46 with
  B_D.
- **Prospective tests.** `survey/predictions_hclass.txt` (02:16; mechanism retracted at 02:24) and
  `survey/predictions_N1mu1.txt` (01:20) are scored in §12.10.

### 12.8 Answer, and what it changes

- **Answer [computed at κ = 6, 7; heuristic beyond].**
  - At κ = 6, λ ≤ 0.25 (29 primes, complete), the constants are finite at every prime, as any finite sample must be at
    fixed κ. Their size is the information.
  - Spike primes reach B_L 1.88 (1657) and B_D 14.8 (1789). These are 4× and 18–25× the band medians.
  - 9 of the 29 primes are spikes by some flag, 6 of them by sD.
  - Over all 89 primes (§12.10), 21 are spikes. Spike amplitude falls as λ rises: the largest B_D is 14.8, 6.6 and
    1.4, and the largest PW_pair 32, 11 and 0.89, at λ ≤ 0.25, in (0.25, 0.31] and at λ ≈ 0.5. At λ ≈ 0.5 the
    debiased PW_pair is below 1 at every prime (28 of 29 by the CS upper estimate).
- **What spikes are.**
  - At λ ≈ 0.21, 71–88% of (C1) configurations are 2+2 involution-structured. This holds at the spike primes and at
    the one typical prime measured there (1621).
  - At the four split spike primes, this family's weight factor F and its class values are both large: F 2.3–4.4
    against 0.3 at 1621, and B_D 4.3–17.3 against 0.44. The not-2+2 part is lifted too.
  - Over the survey (§12.11) F carries N₁/μ₁'s ranking (Spearman 0.98) and is N₁/μ₁ rescaled by a share of 0.50–0.86,
    so F is not a separate factor at κ = 6.
  - The sN spike 1627 has F 1.6–2.1 without a value spike.
  - Why some primes are like this is not explained. |a|/√p and the cubic character of 2 rank it in part (§12.7).
- **p against λ.**
  - Across κ = 6 and 7, at λ ≈ 0.3 and at λ = 0.2, the 2+2 baseline weight falls as R₂₊₂ = N_inv²κ⁴/p² does (up to
    F), not as a function of λ.
  - The spike excess is F, which the heuristic does not model.
  - At fixed κ the two cannot be separated.
  - At κ = 7, λ = 0.2 there is one prime, 23549, the highest symR sampled.
    - Its 2+2 weight is 0.055 μ₁ (5 of 79 configurations), against 0.31–3.5 at κ = 6, λ ≈ 0.21. A weight depending on
      λ alone would give at least 28 such configurations (P ≈ 10⁻⁷).
    - Its share is 6.3%, against 5.4–5.7% from R₂₊₂ at F = 1 (F 1.16, 95% range 0.4–2.7).
    - Its N₁/μ₁ is 0.84 ± 0.09, against about 2.5 for the κ = 6 proportionality.
  - This rejects a weight depending on λ alone. It does not distinguish R₂₊₂ from other κ-scalings within about 10×.
- **κ = 7.**
  - At λ ≈ 0.3 the 2+2 share is 1.1–4.3% at four primes (36037: 3.1% by its split), against an expected 1.9–2.4%.
    At 23549 (λ 0.2) it is 6.3%, against an expected 5.4–5.7%.
  - N₁/μ₁ is 0.84–1.11 at seven primes (six at λ ≈ 0.3, and 23549), with symR 16–67.
  - Class values at λ ≈ 0.3: at 36037, picked on symR, B_L is 0.635. That is 2.4–2.9× the λ = 0.4–0.5 values, against
    1.1–1.5× for the same step at κ = 6. N₁/μ₁ there is 1.08, and the D excess has a consistent sign but an unresolved
    size.
  - Against the equal-λ comparison primes 35099 and 34847 (B_L 0.237 and 0.245) it was scored a spike in B_L (2.7×
    and 2.6×, every resolved L bin lifted; §12.6). Against the seven-prime band it is not shown (2.6× the median, with
    34259 at 2.1×; §12.6, mechanical item 6). The probability and "2.4× the implied band median" arguments assumed the
    κ = 6 spread carries over, and are superseded.
  - The lift is not carried by the 2+2 family. Without its 2+2 configurations (3.1%, F 1.6) B_L at 36037 is 0.57,
    2.4× 35099's; they add about 0.07, in phase with the rest (§12.6). What carries it is unexamined.
- **What changes.** Obstruction (c) of §11.8 narrows to three questions:
  1. Is G(p) = s/R₂₊₂ = κ^{o(κ)} uniformly over p ≥ p₀ near the threshold path (§12.12)?
     - This is the only way the 2+2 family can spoil the (1/2+o(1))κ exponent (§12.5 item 6), and this step needs no
       (N).
     - It needs no independence assumption, since G is defined from the measured share.
  2. The same question for the arithmetic factors of the other bounded-orbit families of §12.5 item 4.
  3. What are the not-2+2 part at spike primes, and any non-projective structure at κ ≥ 7?
     - At κ = 7: the B_L lift at 36037 sits in the not-2+2 part (its split), and so does 34259's (§12.6, mechanical
       item 7). Two primes selected high; not a class. In spread form this question becomes §12.14's.

  With the largest measured G·v (1789), the family would add B_D ≈ 3.6 at κ = 7 if its absolute D-rms did not fall
  with p. It would add about 0.17 if its B_D in κ²/p units stayed constant, and at most about 0.12 with typical values.
  These are illustrations (1789's G is capped at κ = 6). Either way it falls to 0 as κ grows, so it is harmless for the
  exponent if G stays κ^{o(κ)}.
- **Claim gates that stay false.**
  - OSC′ in either form at any κ.
  - Any rigorous bound on spike constants.
  - R₂₊₂ or the family estimate as a theorem. Item 6's bound is elementary, but it bounds the family's effect only in
    terms of F.
  - Threshold certificates at κ ≥ 6.
  - An unconditional exponent statement.
  - G(p) bounded, or κ^{o(κ)}, over p ≥ p₀.
  - Obstruction (c) resolved.
  - Hypothesis H (refuted in its strict form; the class shift of B_D held prospectively (H2) but has no mechanism),
    or the |a|/√p and cubic-character correlations, as claims.
  - "κ = 7 has no spike primes". Undecided: no prime at λ ≈ 0.3 is separated from the seven-prime band at 2σ, and
    that band spreads 4×.
  - The κ = 7 spread at λ ≈ 0.3 beyond seven primes. The κ = 6 calibration transfer is refuted there (3 of 7
    unselected primes exceed κ = 6's unflagged 1.54×). How common spikes are at κ = 7; 36037's B_D size.
  - "36037 is a spike" in any form beyond the two-prime call; "34259 is a spike"; "κ = 7 spikes are rarer, or more
    common, than κ = 6's"; "symR predicts B_L at κ = 7".
  - The B_L lift at 36037 explained. The split refutes it as a 2+2 effect (a 6000-configuration prefix, against
    35099), but other structure in the rest is unexamined.
  - The 2+2 family's class values at κ ≥ 7, or v falling with p.
  - The not-2+2 part at spike primes under control.

### 12.9 Next

- **Finish the survey.** Done (§12.10).
  - Done: 2143 at seed 14 replicates its D excess and all three flags (§12.10).
- **F over the survey.** Done (§12.11). It ran from 06:00 to 10:53 in an adapted form, pre-registered in `survey/predictions_F.txt`
  (05:59:59; an erratum at 06:04 fixes two shares quoted from the wrong sample and changes no prediction).
  - `mc_split.py 6 p nconf --seed 13` at the 25 survey primes with λ ≤ 0.25 that have no seed-13 split
    (`survey/run_k6_split.sh`, outputs `split/split13_k6_p*`). It reproduces the survey run, so the share, N₁/μ₁ and
    each part's class values come from one sample. Scored by `survey/score_F.py`.
  - It replaces `pairsym.py 6 p 300000`, which would give the share from a second, smaller sample.
  - Acceptance: the distribution of F and its maximum, and Spearman with |a|/√p and with the cubic class of 2.
  - A model for F in terms of the cubic Jacobi sum is the first step towards bounding its maximum, which is question 1
    of §12.8.
- **κ = 7 at λ ≈ 0.3 comparison primes.** Done (§12.6). 35099 and 34847 give B_L 0.237 and 0.245. By the rule
  written before the 34847 run, 36037 is a spike in B_L against both, and the call is not close.
  - Done: the 2+2 / not-2+2 split of the 36037 run. Its 2+2 share is 3.1% (the 4.5% was pairsym's), and it does not
    carry the (2,2) and (0,3) lift: the rest alone makes 85% and 75% of those bins' X.
- **What carries the κ = 7 lift** (34693 done, §12.6: INCONCLUSIVE, an intermediate level 0.386; neither "36037 alone"
  nor "symR predicts it").
  - The five other primes are done (§12.6, mechanical item 6): the band spreads 4×, and 36037 is not shown to be a
    spike against it.
  - Done (§12.6, mechanical item 7): the not-2+2 split of 34259. REST-LIFTED (close) and TYPICAL, like 36037. A
    second seed at 34259 and 34469 would still test whether the 4× spread belongs to the primes or to the S draws.
  - Next, in spread form (§12.14, mechanical item 8, pre-registered, not started): σ_L at κ = 7, λ ≈ 0.3 on 24
    primes, against κ = 6's frozen 0.352 (rule T1′), about 22 core-h.
  - Then split 36037's rest by other structure: one ι-pair, other involution cycle types, order-3 symmetry.
- **The direct test of (c)** still needs κ = 8 at λ ≈ 0.18 (p ≈ 3.8·10⁵), with a sampler that builds (C1)
  configurations directly (§11.9). That sampler is the main gap.
- **Bounding G** (§12.12).
  - By §12.5 item 6, the 2+2 family's effect on the exponent is controlled by G. So the proof target is the share:
    #2+2 ≤ κ^{o(κ)}·R₂₊₂·N₁. A bound O(κ^{o(κ)}·N_inv²κ⁴p⁻²μ₁) on the 2+2 count suffices only together with (N) at
    B = κ^{o(κ)}.
  - The block conditions are explicit. The rest is an upper bound for a (C1) count on a codimension-2 family, which
    §9's existence proof does not give.
  - Weil's relative error is about κ^{O(κ²)}/√p, useless at the thresholds p = κ^{(1/2+o(1))κ}. So no method is in hand.

### 12.10 Final survey and the scored predictions (10 Nov, 04:49) [computed; the scoring is pre-registered]

- **Reviewed** by an independent AI referee: round 4 of `review-2026-11-10/ROUND3.md`, with the author's disposition.
  Its checks are `review-2026-11-10/scratch/r4_checks.py` and `.out`.
- **Run.** All 89 primes had finished by 04:49 (`k6_spike_survey.out`). The scoring script is
  `survey/score_predictions.py`, with output in `survey/score_predictions.out`. It uses the flags and bands of
  `k6_spike_survey.py`. Nothing changes at λ ≤ 0.25. The completed bands are in §12.2's table.
- **Spikes.** 21 of the 89 primes are flagged.
  - Amplitude falls as λ rises. The largest B_D is 14.8, 6.6 and 1.4 at λ ≤ 0.25, in (0.25, 0.31] and at λ ≈ 0.5.
    The largest PW_pair is 32, 11 and 0.89.
  - In (0.25, 0.31] the largest spikes are 2113 (B_D 6.6, z 3.7; PW_pair 11.1; N₁/μ₁ 2.06) and 2269 (B_D 5.4, z 3.3;
    PW_pair 8.0; N₁/μ₁ 0.87).
  - The debiased PW_pair is below 1 at none of the 29 primes with λ ≤ 0.25, at 13 of the 31 in (0.25, 0.31] and at
    all 29 at λ ≈ 0.5. By the CS upper estimate the counts are 0, 7 and 28. The exception at λ ≈ 0.5 is 3889
    (debiased 0.89, CS 1.01). These are Monte Carlo estimates, not certificates.
  - The smallest N₁/μ₁ in the survey is 0.37 (1741), so B ≈ 2.7 in (N) covers all 89 primes.
- **Replication.** The four primes run at two seeds (1933, 2347, 3877 and 4219) agree on B_D within 0.8 combined
  jackknife se, and on B_L within 2.0. At 1933, N₁/μ₁ is 2.66 against 2.63. This is the only between-seed check of
  the B_D se.
- **N₁/μ₁ predictions** (`survey/predictions_N1mu1.txt`, 01:20; §12.3).
  - Log errors at the 74 later primes:

    | primes | n | rms | mean | largest |
    |---|---|---|---|---|
    | later primes, λ ≤ 0.25 | 15 | 0.24 | +0.04 | +0.37 (1879) |
    | (0.25, 0.31] | 31 | 0.19 | +0.04 | +0.44 (1951) |
    | λ ≈ 0.5 | 28 | 0.13 | +0.05 | −0.26 (3889) |

  - Over all 74 the rms is 0.18 (mean +0.04 ± 0.02), and 8 of the 74 are off by more than 0.3. The in-sample residual
    sd was 0.20 with n in the denominator, or 0.22 with n − 3.
  - 2347 and 4219 had been seen at seed 11. Without them nothing changes (rms 0.19 and 0.13 in their bands).
  - At λ ≤ 0.31 this is real prediction: the spreads of log N₁/μ₁ among the predicted primes in the first two rows
    are 0.65 and 0.40.
  - At λ ≈ 0.5 the errors confirm the level that 3877 alone had set (mean +0.05 ± 0.02). Without 3877 the fit misses
    by 3.8× in (0.25, 0.31] and by 52× at λ ≈ 0.5.
  - But they reject the symR slope there. Within the band it is 0.40 ± 0.07, against 0.98, and a constant does as
    well (rms 0.12–0.13). So within the λ ≈ 0.5 band the law has no predictive power.
  - Post hoc:
    - The within-band slope falls with λ: 1.00 ± 0.06, 0.86 ± 0.09, 0.73 ± 0.07 and 0.40 ± 0.07. symR's own sampling
      error does not explain this, since its sample is larger at λ ≈ 0.5.
    - Given symR, N₁/μ₁ is about 15% higher at p ≡ 7 (mod 12), in every band (Mann–Whitney 0.0002).
- **Hypothesis H** (`survey/predictions_hclass.txt`, 02:16; §12.7).
  - The sets:
    - test set: the 70 primes whose npz was written after 02:16, less 1933, whose value was known from seed 11;
    - formation set: the 17 primes written by 02:16 (1531–1753, less 1741);
    - 1759 is in neither (§12.7);
    - the file's own wording gives 71, with 1933;
    - a strict set of 66 also drops 2347 and 4219 (seen at seed 11), 3877 (seen in an earlier S-batched run) and
      3889 (named in the file).

    All three test sets give the same verdicts.
  - **(H1)**, that every new sD prime is ≡ 1 (mod 12), is **refuted by 2143** (≡ 7, λ 0.276, npz written at 03:56).
    - 2143 is sD as registered: B_D 1.28, z 6.4, 2σ lower end 1.07 (jackknife se) against the threshold 0.89, twice
      the band median.
    - The flag survives leaving out any one of the 16 batches with the jackknife redone (16 of 16). It would fall
      only if the jackknife se were understated by more than 1.68×.
    - 2179 (≡ 7) and 3823 (≡ 7, λ 0.49) are also flagged, but at the threshold: their se margins are 1.00 and 1.02,
      and they lose the flag with one batch left out in 12 and 10 of 16 cases. They are threshold cases, not
      refutations.
    - The B_D point values of all three stay above the threshold with any two batches left out, and every batch
      contributes positively (`review-2026-11-10/scratch/leaveout_BD.py`). That tests B_D, not the flag, which is
      defined by the lower end.
    - Heavy tails. §12.2's factor of about 2 was measured on N₁/μ₁. Inflating the B_D se after the fact cannot enter
      the scoring, which fixed the jackknife se. At 2× it would leave 4 class-1 flags and no class-7 flag, so it would
      rescue H. The seed pairs above give no basis for it.
    - The refuting excess is moderate. 2143's B_D is 2.9× its band median, like the weakest class-1 flags (2053 and
      2137).
    - It replicates (referee round 4b). A second-seed run (`mc_classes.py 6 2143 10000 --seed 14`,
      `survey/mc_k6_p2143_s14.npz`) gives B_D 1.29 (z 7.2, 2σ lower end 1.09), B_L 0.90 and N₁/μ₁ 1.99. At seed 13
      they were 1.28 (z 6.4, 1.07), 0.91 and 2.08. All three flags (sD, sPW, sN) recur against the seed-13 band
      medians.
    - The seeds differ by 0.03 combined se on B_D, 0.47 on B_L and 0.84 on N₁/μ₁. The se is that of the
      noise-subtracted X, the scale of the jackknife z. This matches the four seed pairs above, so the jackknife se is
      borne out at 2143 too.
    - So the refutation of H1 is not a seed artefact (one replication). This informs the reading, not the score.
  - **(H2) held as pre-registered** in both bands that qualify. The registered statistic is the class medians of B_D:
    - (0.25, 0.31]: 0.92 against 0.34 (15 and 16 primes);
    - λ ≈ 0.5: 0.36 against 0.12 (13 and 16 primes).

    Added summaries, one-sided Mann–Whitney: 0.006 and 0.012 (0.006 and 0.025 on the strict 66). Stratified by band
    it is 0.0001 on the 70 (0.0002 on the 66).
  - **(H3) holds.** The new sN spikes are 1789, 2113 and 2341 (≡ 1) and 2143 (≡ 7).
  - So H is refuted in its strict form, value spikes only at p ≡ 1 (mod 12). H2 held, so the data support a shift of
    B_D towards p ≡ 1 (mod 12). No mechanism is known.
  - Post hoc:
    - The shift does not come from the noise subtraction: unsubtracted values give 0.0001 on the 70.
    - It survives adjusting for N₁/μ₁ within bands (0.001). Given symR it weakens to 0.016; symR is itself shifted
      towards p ≡ 1 (mod 12) (stratified 0.005).
    - B_D > 2 still occurs only at p ≡ 1 (mod 12): 8 of 43 primes against 0 of 46 (P = 0.002). Three of the 8 are
      test primes (1789, 2113 and 2269); on their own P = 0.11. The largest B_D at p ≡ 7 (mod 12) is 1.28 (2143).
    - The count spikes without value spikes are still 1531, 1627 and 1759, all ≡ 7 (mod 12). 1951 is not flagged once
      its band is complete (N₁/μ₁ 1.42 against the threshold 1.62).
    - At λ ≤ 0.31 the class medians are N₁/μ₁ 1.04 against 0.67 and B_D 0.93 against 0.47 (30 primes each).
- **For the question asked.** The completed bands leave §12.8's answer and its three questions as they were. Spikes
  are frequent at κ = 6 (21 of 89), and their amplitude falls as λ rises.

### 12.11 F over the survey (mechanical item 2; 10 Nov, 10:53) [computed; the scoring is pre-registered]

- **Reviewed.** Referee round 4f (`review-2026-11-10/ROUND3.md`, `scratch/r4f_checks.out`): every prediction is scored
  as written, with the stated scopes, and every number and arithmetic column reproduces by independent code. The
  interpretation below is the referee's.
- **Run.** `mc_split.py 6 p nconf --seed 13` at the 25 survey primes with λ ≤ 0.25 that had no seed-13 split
  (`survey/run_k6_split.sh`; outputs `split/split13_k6_p*`, npz gitignored), plus the four earlier splits. Each run
  reproduces its survey run array for array (nS, cnt, S1, S2, N1; referee), and the parts add up at all 29. Scored by
  `survey/score_F.py` (written 06:03, before the first result) → `survey/score_F.out`, against
  `survey/predictions_F.txt` (05:59:59; erratum 06:04, before any result, no prediction changed).
- **F per band** (F = share × N₁/μ₁ × p²/2,624,400):

  | λ | n | share median (range) | F median | F min–max |
  |---|---|---|---|---|
  | 0.197–0.218 | 14 | 0.71 (0.61–0.86) | 0.67 | 0.24–3.89 (1657) |
  | 0.222–0.249 | 15 | 0.62 (0.50–0.80) | 0.64 | 0.26–4.41 (1789) |

  The four largest are the sD spikes 1789 (4.41), 1657 (3.89), 1597 (3.64) and 1933 (2.80), then the count spike 1531
  (2.63).
- **The predictions, as scored (wording of referee round 4f).**
  - (F1) **refuted**: shares of the 25 new primes span 0.496–0.792. Six are below 0.60 (1723, 1747, 1759, 1783, 1867,
    1879), all at λ 0.22–0.25. The share falls with λ (Spearman −0.41 over the 29).
  - (F2) kept automatically: even at share 1 no new prime could exceed F = 3.79 (1933), so this prediction could not
    fail. The largest new F is 2.80 (1933); the maximum stays at 1789 (4.41).
  - (F3) kept, near-automatically: 0.982. It is 0.969 at any constant share and ≥ 0.90 in 99.9% of share permutations,
    since log N₁/μ₁ carries 0.37 of the 0.47 variance of log F. F is N₁/μ₁ rescaled by a share that moves by about
    ±12%; it is not a factor separate from N₁/μ₁.
  - (F4) kept: 0.52 (0.51 with the scorer's tie handling). The share's elasticity in N₁/μ₁ is 0.10 (0.04–0.17).
  - (F5) kept, automatically in rank: 0.845, and ≥ 0.5 in every share permutation. Its content is that the rest's
    count grows with N₁/μ₁ (elasticity 0.79, 0.64–0.91; the 2+2 count 1.10).
  - (F6) kept: at the sD primes 1669, 1693 and 1933 the 2+2 part's B_D (2.8, 4.0, 4.3) is 2.0–3.0× the rest's (1.1,
    1.3, 2.1). These are point values, and 1933's run contains the 5022 configurations of its earlier split.
  - (F7) all three directions held (Spearman(F, |a|/√p) 0.49; at h = 0 median F 2.80 when 2 is a cube against 0.72;
    Spearman(F, |A(0,0) − mean|/√p) 0.79 at h = 0), but they were already fixed by the known N₁/μ₁: with F at share
    0.8 all three held before the runs. No claim.
- **Exploratory (not pre-registered).** Spearman(F, symR) 0.92 is N₁/μ₁'s (0.92). Post hoc: the share is higher at
  p ≡ 1 than p ≡ 7 (mod 12), median 0.71 against 0.62, in both λ bands (permutation p 0.054 and < 0.001), with λ
  balanced across classes. To be pre-registered before use.
- **What this changes.**
  - At κ = 6, λ ≤ 0.25, F lies in 0.24–4.41 at all 29 primes, and its maximum is the 1789 already known. But F is not
    independent information: a large F and a large N₁/μ₁ are the same observation. At κ = 6 F's size is N₁/μ₁'s,
    since G = 0.58–1.05 and s ≤ 1 caps it at 1.42. A large count does not stress (N), and the family's effect runs
    through G (§12.12). (An earlier version of this sentence said the question was "(N)'s constant B"; that was
    backwards.)
  - The informative results are F1 (the share is not a near-constant 0.6–0.9: it falls with λ to 0.5), F4 (the share
    rises only weakly with N₁/μ₁), F6 (the 2+2 part carries the larger D excess at the sD spikes) and the post hoc
    class difference of the share.
  - Claim gates stay false: G(p) bounded or κ^{o(κ)}; the share-by-class difference as a claim; any F7 correlation as
    a claim.

### 12.12 What controls the 2+2 family's effect: G, not F·B (10 Nov) [elementary; computed; referee round 4g]

- **Correction to §12.11.** §12.11 first said that at κ = 6 "is F bounded?" is the question whether (N)'s B is
  bounded at spike primes. That was backwards. (N) is the lower bound N₁ ≥ μ₁/B, so B controls μ₁/N₁, which is small
  at spike primes: N₁/μ₁ is 1.3–4.5 at the six sD spikes with λ ≤ 0.25 (2.7–4.5 at the four with the largest F).
  Spike primes do not stress (N). Its worst case in the survey is 1741 (N₁/μ₁ 0.37).
- **The parameter.** Let s be the 2+2 share of the (C1) measure, and G := s/R₂₊₂ = F·μ₁/N₁, the family's share over
  its heuristic weight R₂₊₂ = N_inv²κ⁴/p². Then F = G·N₁/μ₁ exactly.
- **§12.5 item 6 without (N)** [elementary; for population quantities, which the Monte Carlo estimators satisfy only
  approximately].
  - V is linear in the measure, so V_all = s·V_fam + (1 − s)·V_rest. For each group (L or D) the weighted rms is a
    norm, so ρ ≤ (1 − s)ρ_rest + s·v. The noise allowance carries through, since (1 − s)ν_rest ≤ ν_all.
  - |Q| ≤ n, so v ≤ n; and s = G·R₂₊₂ by definition.
  - Hence the family adds at most G·R₂₊₂·n·p/κ² = G·N_inv²κ²·(n/p) < G·N_inv²κ² to B_D (κ²/p units), and at most
    G·R₂₊₂·n < G·N_inv²κ⁴/p to B_L.
  - N_inv = κ(κ−1)(κ−2)(κ−3)/8 < κ⁴/8, so N_inv²κ² = κ^{O(1)}. It is κ^{6.8}, κ^{7.1}, κ^{7.4} and κ^{7.6} at κ = 7–10.
  - So the 2+2 family can spoil the (1/2+o(1))κ exponent only if G = κ^{Ω(κ)} at some p ≥ p₀ near the threshold path.
    This step needs no (N); OSC′ itself still contains (N) through the noise term. It replaces item 6's
    "F·B = κ^{Ω(κ)}" and is never weaker, since G = F·μ₁/N₁ ≤ F·B under (N).
  - **It is asymptotic only.** The D addition κ^{6.8–7.6} exceeds the D tolerance of 3.4–5.7 in log_κ at every
    κ = 7–10, and the L addition at T(κ), G·κ^{3.2, 3.0, 2.6, 2.2}, exceeds the L tolerance (1.7, 2.1, 2.5, 2.8) at
    κ = 7–9. So finite κ still needs the family's v, as in item 6.
  - **Nothing elementary excludes G = κ^{Ω(κ)}.** The only cap is s ≤ 1, i.e. G ≤ 1/R₂₊₂. At the §11.8 thresholds that
    is κ^{2.4}, κ^{3.2}, κ^{4.2} and κ^{5.1} at κ = 7–10, and κ^{κ+κ/ln κ−12+O(1)} in general.
  - The rest still enters through (1 − s)ρ_rest, which this does not bound.
- **G in the data** [computed; `survey/score_F.out`, §12.6; referee `scratch/r4g_checks.out`].
  - κ = 6, λ ≤ 0.25 (29 primes): G is 0.58–1.05 (median 0.74). This is no test: R₂₊₂ is 0.70–1.12 there, so s ≤ 1
    already caps G at 0.89–1.42, and G over its cap is just the share.
  - κ = 7: G is 2.0 (35281), 0.51 (35099), 1.5 (36037, from its split), 1.05 (34693, from its split) and 1.3 (23549), against
    trivial caps of 21–49. These rest on 19, 5, 185, 139 and 5 structured configurations; the pairsym values are clustered.
  - So wherever it can be tested (κ = 7, five primes, one of them the spike 36037), the family's share is its heuristic
    weight to within about 2× (point values; 35099 and 23549 rest on 5 configurations each). F's large values at the κ = 6 spikes are N₁/μ₁'s.
- **What a proof would need.**
  - The target is the share: #2+2 ≤ κ^{o(κ)}·R₂₊₂·N₁. A bound on the 2+2 count relative to μ₁ suffices only together
    with (N) at B = κ^{o(κ)}.
  - Both counts are counts of configurations defined by κ-th power residue conditions on the κ² differences t_i − s_j
    of 2κ variables (the profile of each t_i in the κ shifts s_j). The thresholds are T = κ^{(1/2+o(1))κ} (log_κ T is
    5.57–7.36 at κ = 7–10), so the pattern length is κ ≍ log p/log log p.
  - [Superseded by §12.13: for fixed S these are polynomials in one-variable counts, and Weil's range starts at
    κ^{(4+o(1))κ}, still far above the thresholds.] Weil's one-variable bound gives these counts with relative error about κ^{O(κ²)}/√p. That exceeds the main term
    unless p ≥ κ^{cκ²}.
  - Weil-type square-root bounds are the general tool for such counts, and they fail here. Short-interval methods
    (Burgess; Graham–Ringrose) and sumset bounds in multiplicative subgroups (Hanson–Petridis) address other questions
    and give nothing at set sizes κ ≍ log p. No formal reduction to a named conjecture is claimed.
  - κ = 3 has no 2+2 family (two disjoint pairs need κ ≥ 4), so §11.2's exact method says nothing about G.
  - At κ = 4 each pairing of S has one involution, which preserves S and permutes the bucket keys (checked in 300
    cases, `scratch/r4g_checks.out`). So the 2+2 count is a sum over ι-invariant buckets. §12.13 closes it: it reduces
    to the quadratic characters of r and 1 − r (r the cross-ratio) and to bucket sizes, and G → 1 by Weil. That is a
    fixed-κ result, not a bound uniform in κ.
  - No counterexample family is known: no measured prime has G above about 2 (κ = 7's 2.0 is a pairsym value from 19
    clustered configurations; κ = 6 values cannot exceed 1.42).
- **Consequence.** Unless G grows like κ^{Ω(κ)}, the 2+2 family is harmless for the exponent asymptotically, and
  obstruction (c) is the rest: ρ_rest at spike primes, the part that 36037 shows lifted at κ = 7. That is OSC′ itself
  for the not-2+2 part, and nothing here bounds it.
- **Claim gates stay false:** G bounded or κ^{o(κ)}; any bound on ρ_rest; obstruction (c) resolved; any certificate
  at κ = 7–10 from the elementary bound; the κ = 4 2+2 count in closed form (now given in §12.13, at fixed κ).

### 12.13 κ = 4 in closed form, and what its shape predicts for κ = 5 (10 Nov) [derived; computed exactly; referee round 4i]

Scripts: `osc-mc/k4_22.py` (κ = 4, exact per S; all S at p ≤ 401) and `osc-mc/k5_22.py`; outputs
`osc-mc/k4/k4_22_series.out` and `osc-mc/k4/k5_22_series.out`. The κ = 5 predictions were written before any κ = 5
run (`osc-mc/k4/predictions_k5_22.txt`, 12:30:32; `k5_22.py` saved 12:31:12, first κ = 5 output 12:37:18). Referee
checks: `review-2026-11-10/scratch/r4i_checks.py`, `r4i_pole.py` and their `.out`, written independently of these
scripts.

- **Transport identity** [elementary]. For g = (a b; c d) ∈ PGL₂(F_p), g(x) − g(y) = det g·(x − y)/((cx + d)(cy + d)).
  Let ι be an involution swapping s_i ↔ s_j and s_u ↔ s_v, and P(t) ∈ (Z/κ)^κ the profile P(t)_l = ind(s_l − t) mod κ.
  - At a swapped point, P(ιt)_{ι(l)} = P(t)_l + α_l + β(t), with α_l = −ind(c s_l + d) depending only on S and ι, and
    β(t) = −ind(ct + d) not depending on l. Constants such as ind(det) and ind(−1) are absorbed.
  - So on the four swapped coordinates ι carries normalized partial keys by a fixed affine map σ_ι, the same for
    every t.
- **Fixed partial keys** [elementary]. Take ι with trace 0, so d = −a. Then ι(s_i) = s_j gives
  (c s_i + d)(c s_j + d) = −det ι, and likewise for (s_u, s_v). So α_i + α_j = α_u + α_v = −ind(−det ι).
  - σ_ι fixes a partial key iff 2C ≡ −ind(−det ι) (mod κ) has a solution C.
  - At odd κ there is exactly one C, for every ι. At even κ there are two if −det ι is a square, i.e. ι is split
    (its fixed-point discriminant is 4·(−det ι)), and none otherwise.
  - So c_ι, the number of such C, is 1 at odd κ and 2·[ι split] at even κ. A split ι is as likely as a non-split one
    up to O(1/p), so E[c_ι] = 1 + O(1/p) (exactly 1 − 1/(p − 2) at κ = 4).
  - The referee enumerated all κ³ partial keys for 840 involutions at κ = 4–7 and found c_ι·κ fixed ones every time. This is the factor 2κ⁻⁵ (split, even κ) against κ⁻⁵ (odd κ) of §12.5.
- **κ = 4: everything is a bucket-size count** [derived; checked exactly].
  - At κ = 4, S has three involutions (its Klein group V₄), each preserving S. So σ_ι acts on full keys. It has 8 fixed
    keys if ι is split and 0 if not.
  - Every point of a σ_ι-fixed bucket is paired with its ι-image in the same bucket, apart from at most 3 exceptional
    points: the two fixed points of ι and the pole t₀ = −d/c (= ι(∞), since d = −a).
  - Hence the 2+2 count of S is a function of bucket sizes alone:
    #2+2(S) = Σ_{ι split} Σ_{K fixed} C(m_K, 2) − 2·#(free V₄-orbits inside one bucket), with m_K = (b_K − e_K)/2 and
    e_K the exceptional points in K. A free V₄-orbit is two ι-pairs for all three ι, so it is counted three times.
  - **The cross-ratio.** Normalize S to {0, ∞, 1, r}. The three involutions are x ↦ r/x, x ↦ (rx − r)/(x − r) and
    x ↦ (x − r)/(x − 1), and their −det are r, r(r − 1) and 1 − r. Their product −r²(r − 1)² is a square because
    p ≡ 1 (mod 4), so #split ∈ {1, 3}, with #split = 1 + 2·[η(r) = η(1 − r) = 1], η the quadratic character.
  - §12.12's "order-4 character sums over the cross-ratio" therefore reduce to two quadratic characters. Exactly
    (p − 5)/4 of the p − 2 values r ∉ {0, 1} have both η(r) and η(1 − r) equal to 1, so E[#split] = 1 + (p − 5)/(2(p − 2)).
    This matches the all-S counts at p = 101, 197 and 401 exactly (0.2424, 0.2462, 0.2481 of S have three).
  - **Checks** (`k4/k4_22_series.out`).
    - No bucket is partially paired.
    - Every split ι has exactly 8 σ-fixed keys and every non-split ι none (enumerated by the referee). When all 64
      buckets are nonempty, each fixed key is witnessed by a non-exceptional point or a fixed point of ι. The
      exception is a fixed bucket consisting of the pole alone (2 of 452 split ι at p = 401 in the referee's sample).
      `k4_22.py`'s "8th key witnessed only by the pole" counter does not check fixedness and is mostly inapplicable;
      no reported number depends on it.
    - The #split formula holds for every S.
    - The formula equals a brute force over all 4-subsets of every bucket in 200 S at each of p = 101, 197 and 401.
    - A 4-set that is a 2+2 for two involutions is invariant under all three, so it is a free orbit (counted three
      times) or a union of two fixed-point pairs (a 2+2 for one involution only). Hence the −2.
- **κ = 4: G is bounded, by Weil** [proof sketch; fixed κ].
  - The leading terms are N₁(S) ≈ μ₁ := 64·λ⁴/4! and #2+2(S) ≈ #split(S)·8·(λ/2)²/2 = #split(S)·λ², with
    λ = p/64. So G(S) → (2/3)·#split(S) ∈ {2/3, 2}, and G(p) → (2/3)·E[#split] → 1.
  - Exactly, G = (2/3)·E[#split]·(N₂₊₂/μ₂₊₂)/(N₁/μ₁), with the Poisson moments μ₁ = 64λ⁴/24 and μ₂₊₂ = E[#split]·λ²
    per S.
  - Each b_K counts t with prescribed quartic characters of (s_l − t)/(s_1 − t), l = 2, 3, 4. Orthogonality and
    Weil (a rational function with at most 4 zeros and poles, not a 4th power) give |b_K − (p − 4)/64| ≤ (63/64)·3√p + O(1)
    for every S and K.
  - So ε := 192/√p bounds the relative error of b_K, and uniformly in S
    G(S)/((2/3)·#split(S)) ∈ [(1 − ε)²/(1 + ε)⁴, (1 + ε)²/(1 − ε)⁴]·(1 + O(1/λ)). The same holds for G(p). The O(1/λ)
    covers the falling factorials, the e_K and the free-orbit correction (≈ 0.34/λ in the data).
  - Hence **G(S) = (2/3)·#split(S)·(1 + O(p^{−1/2})) and G(p) = 1 + O(p^{−1/2}) as p → ∞**. G(S) ≤ 2 + o(1) is
    asymptotic: at p = 101 the 3-split class has G = 2.21.
  - Weil's relative error on b_K is below 1 only for p ≳ 4·10⁴, and it brackets G within a factor 2 only for
    p ≳ 3·10⁶ (factor intervals [0.32, 3.3], [0.52, 1.97] and [0.89, 1.12] at 10⁶, 3·10⁶ and 10⁸). κ = 4's thresholds
    are near p ≈ 100–200. There Weil certifies nothing, but the exact counts do.
- **κ = 4 in the data** (exact; all S at p ≤ 401, sampled S above).

  | p | λ | N₁/μ₁ | N₂₊₂/μ₂₊₂ | G | G, 1-split S | G, 3-split S | overlap correction |
  |---|---|---|---|---|---|---|---|
  | 101 (all S) | 1.6 | 0.257 | 0.393 | 1.52 | 1.32 | 2.21 | 0 |
  | 197 (all S) | 3.1 | 0.525 | 0.614 | 1.16 | 1.02 | 1.51 | 0 |
  | 401 (all S) | 6.3 | 0.720 | 0.796 | 1.10 | 0.79 | 1.85 | 5.4% |
  | 1009 | 15.8 | 0.872 | 0.911 | 1.04 | 0.71 | 2.01 | 2.2% |
  | 2017 | 31.5 | 0.939 | 0.957 | 1.017 | 0.681 | 2.011 | 1.1% |
  | 4001 | 62.5 | 0.968 | 0.978 | 1.008 | 0.671 | 2.013 | 0.5% |
  | 8009 | 125 | 0.984 | 0.989 | 1.005 | 0.671 | 2.004 | 0.3% |
  | 16001 | 250 | 0.992 | 0.996 | 1.008 | 0.668 | 2.007 | 0.1% |
  | 32009 | 500 | 0.996 | 0.998 | 1.003 | 0.668 | 2.002 | 0.07% |

  Sampled S: 40000 at 1009, 20000 at 2017–8009, 10000 above. The predicted per-S classes are 2/3 and 2.

  - At small p, G exceeds 1 (1.52 at p = 101) because N₁/μ₁ is depressed (0.26) more than N₂₊₂/μ₂₊₂ (0.39): bucket
    sizes are under-dispersed, and that cuts C(b, 4) more than C(b/2, 2). G falls to 1 as p grows.
- **What changes at κ ≥ 5: the shape** [derived].
  - S is no longer ι-invariant: κ − 4 points are not swapped. For each such s_l, t and ιt share a bucket only if also
    ind(ι(s_l) − t) − ind(s_l − t) ≡ ω_l(K) := K_j − K_i + ind(c ι(s_l) + d) − ind(c s_j + d) (mod κ), where
    ι(s_i) = s_j. This is a one-variable condition of density 1/κ; the referee checked it against actual pairing at
    κ = 5, 6 and 7 with no mismatch.
  - So for each ι there are c_ι·κ^{κ−3} partial-fixed keys. Within them a point is paired with probability about
    κ^{−(κ−4)}, so m_K ≈ b_K·κ^{4−κ}/2. The 2+2 count of S is Σ_ι Σ_K C(m_K, 2)·C(b_K − 4, κ − 4).
  - Leading terms: with b_K ≈ λ = p/κ^{κ−1}, s = E[c_ι]·N_inv²κ⁴/p²·(1 + O(1/λ) + O(κ^{O(1)}/p)) =
    E[c_ι]·R₂₊₂·(1 + …). So R₂₊₂ is the leading term, and **G → E[c_ι] = 1 at every fixed κ as p → ∞**.
  - The lower-order pieces are: T with three or more ι-pairs (possible from κ = 6), which the sum counts more than
    once; T that is a 2+2 for two involutions; and ι with a third swapped pair or a fixed point inside S, where an
    l-condition degenerates (probability O(κ²/p) per ι).
  - For fixed S both N₁(S) = Σ_K C(b_K, κ) and the 2+2 count are polynomials in one-variable counts. b_K involves κ
    points and m_K involves 2κ − 4 points with 2κ − 5 conditions. Weil bounds each with error O(κ√p) against main
    terms p/κ^{κ−1} (b_K) and p/(2κ^{2κ−5}) (m_K). So b_K is controlled from p ≥ κ^{(2+o(1))κ} and m_K from
    p ≥ κ^{(4+o(1))κ}. With relative errors ε_b and ε_m, G = 1 + O(ε_m + κε_b). **So Weil gives G = 1 + o(1) once
    p ≥ κ^{(4+o(1))κ}.**
  - This corrects §12.12's "relative error κ^{O(κ²)}/√p, useless unless p ≥ κ^{cκ²}", for N₁ as well as for the 2+2
    family. The referee withdrew its round-4g endorsement of that wording.
  - The thresholds are κ^{(1/2+o(1))κ}, so Weil still misses by a factor κ^{(3.5+o(1))κ} in p. There m_K's main term
    is far below 1: the family consists of rare coincidences of a one-variable pattern of length 2κ − 5.
  - Bounding G near the thresholds is therefore a question about the joint factorial moments of (b_K, m_K) at
    λ ≈ 1: do the sparse patterns cluster in buckets by more than κ^{o(κ)} over Poisson? No method is in hand.
- **κ = 5, pre-registered and scored** (`k4/predictions_k5_22.txt`; `k4/k5_22_series.out`).

  | p | λ | S | N₁/μ₁ | witnessed partial-fixed keys | paired fraction | pairs per ι, split / non-split (main) | G |
  |---|---|---|---|---|---|---|---|
  | 1451 | 2.3 | 4000 | 0.75 | 11–25 | 0.195 | 5.64 / 5.68 (5.80) | 1.17 |
  | 2521 | 4.0 | 4000 | 0.86 | 17–25 | 0.197 | 9.93 / 10.00 (10.08) | 1.06 |
  | 5011 | 8.0 | 3000 | 0.93 | 23–25 | 0.199 | 19.85 / 19.97 (20.04) | 1.05 |
  | 20011 | 32 | 1500 | 0.98 | 25 | 0.1995 | 79.84 / 79.85 (80.04) | 1.011 |
  | 50021 | 80 | 600 | 0.99 | 25 | 0.1998 | 199.9 / 200.0 (200.1) | 1.002 |
  | 100151 | 160 | 300 | 1.00 | 25 | 0.1998 | 399.8 / 400.7 (400.6) | 0.999 |

  - P1 held: every ι has exactly 25 partial-fixed keys (a count of keys; the referee enumerated it for 270 ι). No
    paired point lay outside them in 201,000 involutions. At small λ only 11–25 of the 25 buckets hold a witnessing
    point.
  - P2 held: 0.195–0.1998 against 1/5.
  - P3 held: split and non-split agree within 1% at every p. There is no dichotomy, unlike κ = 4.
  - P4 held: G is 1.17 and 1.06 at the threshold-size primes 1451 and 2521 (band 0.4–3), and 1.011, 1.002 and 0.999 at
    p ≥ 20011 (band 0.75–1.33).
  - P5 is a statement: no tested p is in Weil's range for κ = 5.
  - At 1451 a partial-fixed bucket holds about 0.23 ι-pairs on average, so m_K ≪ 1, yet G is 1.17. In this one case
    the sparse patterns do not cluster much. That is an observation at κ = 5, not a bound.
  - G is computed without the overlap correction (T a 2+2 for two involutions), which at κ = 4 was 0 to 5.4%.

- **Consistency with κ = 6 and 7.**
  - Even κ predicts only split involutions in the family. That is what §12.4 found at κ = 6 (0 of 845–1459
    structured T per prime from a non-split ι).
  - G → 1 is consistent with the measured 0.58–1.05 (κ = 6, capped) and 0.5–2 (κ = 7). Those are threshold-range values, which do not test
    the theory: it gives no bound there.
- **What is and is not shown.**
  - Shown at κ = 4 (fixed κ, by Weil; a sketch with explicit constants): G(S) = (2/3)·#split(S)·(1 + O(p^{−1/2})),
    and G(p) = 1 + O(p^{−1/2}). Exact counts and their closed form are checked at p ≤ 32009.
  - Shown at every fixed κ (sketch): G(p) → 1, and Weil gives it from p ≥ κ^{(4+o(1))κ}.
  - Not shown: any bound on G at the thresholds, at κ ≥ 5 or uniformly in κ; anything about ρ_rest.
- **Claim gates stay false:** G bounded near the thresholds; G bounded uniformly in κ; obstruction (c) resolved;
  the fixed-κ sketch as a theorem without a written proof and a human check; "Weil controls G at κ = 4 for
  p ≳ 4·10⁴"; "the pole witnesses the 8th key in about 19% of split ι at p = 401".

### 12.14 Obstruction (c) as a tail question, and its next test (11 Nov) [heuristic; computed; pre-registered; referee rounds 4k-a and 4k-b]

- **Why the spread, not single primes.** OSC′ is a statement for every p ≥ p₀, so §11.8's exponent uses the sup of
  B_L and B_D over the primes near the threshold T(κ), not a typical value.
  - There are N_T ≈ T/(φ(κ) ln T) primes p ≡ 1 (mod κ) in [T, 2T], so log_κ N_T = (1/2 + o(1))κ. It is 3.42 at κ = 7
    and 4.29, 4.74 and 5.53 at κ = 8–10.
  - Write X = B/median(B) across primes at the relevant λ. Under a power tail P(X > x) ≈ x^{−1/γ}, the sup is about
    median·N_T^γ. Under a lognormal tail with log-sd σ, it is about median·exp(σ√(2 ln N_T)).
  - **Finite κ.** Against the rooms log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1) and log_κ B_D < (1 − 1/ln κ)κ − O(1), a
    power tail uses the whole L room at γ_L ≈ 0.50, 0.48, 0.52 and 0.51 for κ = 7–10, and the whole D room at
    γ_D ≈ 0.99, 0.97, 1.04 and 1.02. Both ignore the O(1)s: an O(1) of 1 would be 60% of κ = 7's L room of 1.70.
  - **Asymptotically** the thresholds become γ_L → 1 and γ_D → 2, since log_κ N_T grows like κ/2 while the L and D
    rooms grow like κ/2 and κ.
  - **Obstruction (c) in spread form: is the tail heavy enough that the sup over N_T primes fills the room?** This is
    a heuristic. It extrapolates a tail fitted on tens of primes out to quantile 1/N_T, and Hill > 0 does not show a
    power tail: a lognormal with σ = 0.45 gives Hill ≈ 0.28.
- **The κ = 6 reference** [computed; `osc-mc/tail_index.py` → `review-2026-11-10/scratch/tail_k6.out`, rerun 09:51]. The table gives
  the spread scale σ_L = sd(ln B_L) and Hill estimates on the top quarter, each with a 95% bootstrap range over primes.

  | λ band | N | σ_L | γ_L (Hill) | γ_D (Hill) | primes with X > 2, L / D | max ratio B_L / B_D |
  |---|---|---|---|---|---|---|
  | [0.19, 0.25] | 29 | 0.49 (0.35–0.60) | 0.46 (0.19–0.68) | 1.43 (0.42–1.89) | 4 / 6 | 3.5 / 23 |
  | (0.25, 0.31] | 31 | 0.35 (0.25–0.43) | 0.33 (0.11–0.49) | 0.83 (0.25–1.26) | 3 / 11 | 2.6 / 15 |
  | [0.49, 0.56] | 29 | 0.24 (0.18–0.29) | 0.23 (0.08–0.32) | 0.73 (0.15–0.99) | 0 / 5 | 1.9 / 5.9 |

  - **The B_L spread grows as λ falls at κ = 6** [computed]. σ_L falls from 0.49 to 0.24 between λ ≈ 0.2 and 0.5,
    with disjoint ranges (about 3.8σ). The tail indices rise only at about 1.1σ (not shown), and the B_D count of
    X > 2 does not rise (6, 11, 5).
  - The threshold path has λ_T(κ) → 0 (0.43, 0.18, 0.07 and 0.02 at κ = 7–10), so the live form of (c) is whether
    the spread keeps growing along the path.
  - Against the finite-κ rooms, κ = 6's γ_L of 0.46 at λ ≈ 0.2 is near the L room, and γ_D of 1.43 is above the D
    room. κ = 6's own log₆ N_T is not computed, and κ = 6's λ_T lies above these bands, so this is an indication,
    not a call.
  - At κ = 7, λ ≈ 0.3, the seven band primes give σ_L 0.46 (0.23–0.60), 1.30× κ = 6's at equal λ (0.61–2.02). Their
    lognormal extrapolation gives log₇ sup B_L ≈ 0.14 (power form −0.23), against the room of 1.70 before the O(1).
    It has two parts: log₇ median = −0.72, measured below λ_T and the same size as the unknown O(1); and the part that
    grows with κ, log₇(sup/median) = 0.86 (power form 0.49), which is half the room. Seven primes are too few to use.
- **The next test** (mechanical item 8; `osc-mc/predictions_k7_tail.txt`, revision 1 after referee round 4k-a,
  written before any run).
  - **Quantity:** σ_L(7) at λ ≈ 0.3, from N = 24 primes. These are the 7 band primes plus 17 drawn as
    `default_rng(2026).choice(pool, 17, replace=False)` from the 30 not yet run, never selected on symR or B_L.
    36037 and 34693 enter only a secondary analysis. 7 of the 24 values were known when the rule was written.
  - Each prime gets `mc_classes.py 7 p 6000` at seeds 31–63 (odd), about 22 core-h in all.
  - **Rule T1′:** take the ratio σ_L(7)/σ_L(6, λ (0.25, 0.31]) = σ_L(7)/0.352, with a 95% range from 2000 independent
    bootstrap pairs. WIDER if the lower end is above 1, NARROWER if the upper end is below 1, otherwise COMPATIBLE.
    σ_L is about 2.7× sharper than Hill (referee simulation), but the power is modest: a spread 1.25×, 1.5× or 2×
    wider is called WIDER about 21%, 53% or 91% of the time.
  - **Reported only:** Hill and the count of X > 2; the extrapolated log₇ sup under the lognormal and power forms,
    against 1.70; γ_D if the top 7 B_D values are resolved.
  - **Predictions:** σ_L(7) in 0.35–0.55, ratio 1.0–1.6, T1′ COMPATIBLE, lognormal log₇ sup below 0.6. The last
    is not independent: it follows from the σ_L prediction unless the median moves (it needs only σ_L < 0.70).
  - **What it decides.** WIDER would be the first evidence that the spread grows with κ at equal λ. COMPATIBLE or
    NARROWER would say it does not between κ = 6 and 7, at this λ only.
  - One κ step cannot measure growth with κ. The decisive version is the same quantity at κ = 8 near
    λ_T(8) = 0.18, which needs the (C1) sampler of §11.9.
- **Limits.**
  - Measurement noise in each B moves Hill by under 2% and does not make the test conservative. It adds to σ_L in
    quadrature. The band primes' per-prime log-sd 1/(2z) is 0.024–0.115 (rms 0.071), which moves 0.352 to 0.359;
    κ = 6's rms is 0.025. So the ratio is inflated by about 1.8%.
  - For outlier-prone values (t₄-like), the percentile bootstrap of an sd gives a false NARROWER about 8% of the time.
  - The 7 band primes came from the symmetric-S table, not from B_L.
  - The λ ≈ 0.3 window is below κ = 7's λ_T = 0.43.
  - The tail form is an assumption: it could be capped (|V| ≤ n), or heavier far out.
- **Claim gates stay false:**
  - obstruction (c) resolved in either direction, and any extrapolated sup as a bound;
  - "κ = 7's tail is no heavier than κ = 6's", or "its spread is no wider", from a COMPATIBLE;
  - "within budget at κ = 7" from any extrapolation;
  - "the κ = 6 tail index grows as λ falls" as a fact (the σ_L rise is resolved; the Hill rise is not);
  - "γ > 0 shows a power tail".
