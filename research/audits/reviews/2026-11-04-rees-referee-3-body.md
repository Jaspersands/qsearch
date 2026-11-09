# Rees HSP paper: referee pass 3 (body only), 2026-11-04

Scope: `docs/papers/rees-hsp/main.tex`, lines 1-1106 (front matter through
Section 10; appendices consulted only to check cited statements). Unanchored:
no earlier check/referee reports or integration log were read. AI referee,
not a human review. Findings are appended section by section.

Classes: **error** (a false statement or a proof that does not give the
stated claim), **gap** (a step missing or a cited result used outside its
stated scope, claim may be true), **imprecision** (wording, quantifiers,
stale reference, unstated convention), **fine** (checked, no issue).

## Section 1 (Introduction, contract, thm:main, Table 1)

- **fine** - `eq` for the query bound after `thm:main`: `B_d(g_d) \le
  d^{d(d-1)\lceil\log_2(d+1)\rceil/2}(m+1)^{d\lceil\log_2(d+1)\rceil}` since
  `g_d \le m`; `C_c` as stated; exponent sum ~ `c^2\log c/2`, so "grows like
  `c^2\log c`" is right up to the constant. Statement "not uniform in `c`"
  is correct and honest.
- **fine** - Related work, free 2-generator class-3 example: dim 5, order
  `p^5`; maximal subgroups are `\Fp(ax+by)+[\mathcal L,\mathcal L]`, all
  non-abelian; `|\langle e^x\rangle\langle e^y\rangle| = p^2`.
- **imprecision** - Related work, "So $G$ has no abelian subgroup of index
  $p$ and is not abelian-by-cyclic." The step from "no abelian subgroup of
  index `p`" to "not abelian-by-cyclic" needs `\exp G = p` (a cyclic quotient
  of an exponent-`p` group has order `\le p`). Replacement: "Since $G$ has
  exponent $p$ (as $c<p$), every cyclic quotient of $G$ has order at most
  $p$, so $G$ has no abelian normal subgroup with cyclic quotient: it is
  not abelian-by-cyclic."
- **imprecision** - `def:input-contract`(i) "a nilpotent Lie algebra
  $\mathcal{L} \cong \Fp^m$ of class $c$" vs `thm:main` "with
  $\gamma_{c+1}(\mathcal{L}) = 0$" (class at most `c`). `thm:rees-cover`(i)
  then claims "class exactly $c$", whose proof uses `\gamma_c \ne 0`. Harmless
  (grades with `g_d = 0` cost `B_d(0)` sources and are trivial), but the three
  statements disagree. Replacement in `def:input-contract`(i): "of class at
  most $c$" and in `thm:rees-cover`(i): "of class equal to the class of
  $\mathcal{L}$ (so at most $c$)". Note also `B_d(0) = d^{d(d-1)\lceil\log_2(d+1)\rceil/2} > 1`:
  `thm:main` as stated charges sources at empty grades; one could set
  `M_d = 1` when `g_d = 0`. Not an error.
- **fine** - `thm:main` at `c = 1`: `p > 1` admits `p = 2`; the product is
  empty, `Q = m + \lceil\log_2(3/\eps)\rceil`, abelian Fourier sampling over
  `\mathbb F_2^m`. Consistent.
- **imprecision** - abstract, "polynomial in $m$, $\log p$, the oracle
  label width and $\log(1/\eps)$ for every fixed $c$". Correct, but the
  abstract should say "with exponent depending on $c$" (as the text after
  `thm:main` does), since the `m`-exponent is `\Theta(c^2\log c)`.

## Section 2 (Rees cover, tuple lift, DL control, copy lift)

- **fine** - `thm:rees-cover`: closure, class, top-grade centrality,
  `E_s\circ\delta_\lambda = E_{\lambda s}`, and the `\mathbb Z[1/c!]`
  specialization argument for the BCH group law are correct.
- **fine** - `lem:homogeneous`: needs `c` distinct nonzero points, which
  exist exactly because `p-1 \ge c`; the Vandermonde inversion uses only that
  `\hh` is a subspace. `\delta_\lambda(E_s^{-1}\hh) = E_{s/\lambda}^{-1}\hh`
  checked.
- **fine** - `prop:single-evaluation`: `u = s\,tz - t^2z`, `E_s(\delta_\lambda u)
  = s^2(\lambda-\lambda^2)z`; converse correct. Heisenberg/`\mathbb F_3`
  example: `\delta_2(u) = 2tz - 4t^2z = 2tz - t^2z`, `E_1 = z`. Correct.
- **fine (recomputed)** - Dixmier-Lister table: Jacobi holds on all 56
  triples; LCS dims `(8,4,2)`; `C(8,2)\cdot 8 = 224` equations in `64`
  variables; rank `52` over `\mathbb Q`; Smith invariant factors are only
  `{1,3,6}`, so the rank is `52` modulo every prime `p > 3` (this replaces the
  finite check `5 \le p \le 23` by a proof; suggest saying so). The 12-dim
  nullspace: every derivation maps `\mathcal L` into `\gamma_2`, `\gamma_2`
  into `\Span(e_7,e_8)`, and `D^3 = 0`. Cover dims `14`, `C(14,2) = 91`,
  `91\cdot 3 = 273`; `4` copies: `32`, `56`, `C(56,2)\cdot 3 = 4620`. All
  reproduce. Suggested replacement for "the coefficient matrix of the system
  has rank $52 = 64-12$ modulo every prime $5 \le p \le 23$": "its Smith
  normal form over $\mathbb{Z}$ has invariant factors in $\{1,3,6\}$, so the
  coefficient matrix has rank $52 = 64-12$ modulo every prime $p > 3$".
- **fine** - `lem:copy-lift`: `R_gR_h = R_{gh}`, `\tr(\rho_H R_g) = 1_H(g)`,
  and the entry formula gives the coset density of `\exp(\hlift)`.
- **fine** - `prop:refresh` and the `C_p` counterexample: Fourier states
  are translation eigenvectors, product of phases `\omega^{kg}\omega^{-kg} =
  1`, so the two-point lift yields `|G\rangle\langle G|`. Note the example uses a
  two-point lift on an abelian group, where `thm:main` would use `c = 1`; it
  illustrates the lift map, not the algorithm. **imprecision**: say "the
  two-target lift map $a \mapsto (R_a, R_{2a})$" to make clear it is not an
  instance of the `c = 1` algorithm.

## Section 3 (complete central instrument, finite controls)

- **fine** - `lem:central`: probability `|K|/|Z|` on `K^\perp`, normalized
  state and `\tr(\rho_\lambda R_g) = \chi_\lambda(z)` for `g = hz` all
  rederived; centrality is used exactly where stated.
- **fine (recomputed)** - Finite control: `|G| = 5^4`, cover dim `4+2+1 = 7`,
  order `5^7 = 78125`; line `X+W` (in `\gamma_1\setminus\gamma_2`) gives
  `\dim\hlift = 1`, fibers `5^6 = 15625`; line `Z+W` (in
  `\gamma_2\setminus\gamma_3`) gives `\dim\hlift = 2`, fibers `5^5 = 3125`. Both
  lines are nonnormal. `\gcd(3,4) = 1` gives arity `g_3+1 = 2`; two quadratics in
  5 variables by Chevalley-Warning; `2\cdot 5 = 10` sources, `30` queries.
  `16\cdot 3^8 = 104976 \gg 7`.
- **fine (recomputed)** - End-to-end extension counts: over `\mathbb F_{11}`,
  class-four filiform `g = (5,3,2,1)`: `\kappa = (2,1,2)`, `M = (B_2(3), 3,
  B_2(1)) = (1024, 3, 64)`, and `4\cdot 9\cdot 1024\cdot 3\cdot 64 = 7{,}077{,}888`
  (so `m+t = 9`); over `\mathbb F_7` class three: `(B_2(2), B_3(1)) = (324,
  46656)`, `3\cdot 8\cdot 324\cdot 46656 = 362{,}797{,}056`; reduced counts
  `(G(2,3)^2, G(3,2)^1, G(2,1)^2) = (1024, 729, 64)` and `4\cdot 6\cdot\ldots =
  1{,}146{,}617{,}856`; `B_3(2) = 729^2 = 531441`; `4\cdot 9\cdot 1024\cdot 531441\cdot 64
  \approx 1.254\cdot 10^{12}`; Heisenberg/`\mathbb F_{1031}`: `1031 \ge 1024`,
  `M = 2\cdot 2 = 4`. All reproduce.
- **imprecision** - Section 3, "At the smaller count
  $G(\kappa_d,g_d)^{\lceil\log_2 t\rceil}$ that the deterministic solver
  consumes". The symbol `t` is not defined here (it is defined only in
  Section 4, Schedule 1 paragraph, as the length of the computed zero sum),
  and `t` already denotes the Rees variable and, in Section 4, the rank slack
  `\lceil\log_p(3/\eps)\rceil`. The exponent differs across grades (`2` at
  `\kappa = 2`, `1` at `\kappa = 3`, `p = 7`), which the reader cannot reconstruct
  from this sentence. Replacement: "At the smaller count
  $G(\kappa_d,g_d)^{\lceil\log_2 \ell_d\rceil}$ that the deterministic solver
  consumes, where $\ell_d \le \kappa_d+1$ is the number of terms of the zero sum
  of $\kappa_d$-th powers that it computes (Section~\ref{sec:sde})". Rename
  `t` to `\ell_d` in the Schedule 1 paragraph too.
- **imprecision** - Section 3, "beyond the simulation; class four over
  $\mathbb{F}_5$". "the charged count" here is the combined-rule count, not the
  `thm:main` count, which at `d = 4`, `p = 7` charges `B_4(1) = 65536^3`, not
  `B_2(1)`. Say "the count charged by Remark~\ref{rem:combined-schedule}".
- **fine** - `rem:premature`: `(c-1)(c-2)/2 = 55` at `c = 12`. Correctly
  scoped as an interface obstruction, not a lower bound.

## Section 4 (quotient conversion, recursion, proof of thm:main, Schedules)

- **fine** - `prop:descent`: entry formula, vanishing off `HZ` (uses that
  `\delta_{s_i}` preserves `H` and `Z`, hence `HZ`), character product
  `\chi_{\sum s_i^d\lambda_i}(z) = 1`. Correct branch by branch.
- **fine** - `rem:product-channel`: `\mathrm{SUM}(|\chi_a\rangle|\chi_b\rangle) =
  |\chi_{a-b}\rangle|\chi_b\rangle`; `p = 5, a = 1, b = 4` gives output character `4`.
- **fine** - Recursion: `K_d`, `a_d`, the `H`-independent section, the
  terminal group `t\mathcal L`, and the generator argument (`\log K \supseteq
  \hh` because `\log K` is a subspace containing every `b_i`).
- **fine** - Rank item: `(p^k-1)/((p-1)p^{m+t}) < 1/((p-1)p^t) \le \eps/3`.
  `N_{\mathrm{instr}}` formula counts merge nodes `\prod_{d'<d}M_{d'}` at grade
  `d` correctly.
- **fine** - `lem:hybrid` and its application (telescoping, contractivity
  of the implemented suffix, pure-to-mixed by convexity, dephased control).
- **gap** - Proof of `thm:main`, "Schedule~1 returns a nonzero witness
  of~\eqref{eq:sde-target} for every label tuple, deterministically."
  `thm:is-import` is stated only for `d \mid p-1`, but `thm:main` runs Schedule
  1 at every grade for every `p > c`, including grades with `d \nmid p-1`
  (e.g. `d = 3`, `p \equiv 2 \bmod 3`; `d = 4`, `p \equiv 3 \bmod 4`). There the
  proof needs the reduction to exponent `\kappa_d` and the Bezout lift of
  `rem:is-import`(b), which the proof does not cite and which `thm:main`'s
  hypothesis ("assume Theorem~\ref{thm:is-import}") does not cover. The
  lift itself is correct (I checked: for `y = u^\kappa`, `y^{t d/\kappa} = y`
  because `td/\kappa \equiv 1` modulo the order `(p-1)/\kappa` of `Q_0`), and
  `B_{\kappa_d}(a) \le B_d(a)`, so this is a citation gap, not a false claim.
  Replacement in the proof: "Schedule~1, run at exponent $\kappa_d =
  \gcd(d,p-1)$ (which divides $p-1$) and converted by the Bezout exponent of
  Remark~\ref{rem:is-import}(b), returns a nonzero witness ... at any arity
  $M_d \ge B_{\kappa_d}(g_d)$, in particular at $M_d = B_d(g_d)$."
- **imprecision (dependency bookkeeping inconsistent)** - Three places treat
  the Bezout lift differently: `rem:combined-schedule` "conditional on the
  steps behind Theorem~\ref{thm:main}, on part~(ii) above and on the Bezout
  lift" (as if it were an extra condition beyond `thm:main`); the paragraph
  after `thm:free-coordinate`, "It uses no Schedule~2 node and no Bezout
  lift"; whereas the free-coordinate node itself "converts by a Bezout
  exponent", the `\Gamma_1` grades use `s_l = y_l^e` with `ed \equiv 1`
  (Appendix, `lem:fc-forest`(a)), and `thm:main` needs the lift whenever `d
  \nmid p-1` (previous item). Since the lift is a two-line proved fact, it
  should not be a condition anywhere. Replacements: delete ", and on the
  Bezout lift" in `rem:combined-schedule`; in the paragraph after
  `thm:free-coordinate` replace "It uses no Schedule~2 node and no Bezout
  lift, because" by "It uses no Schedule~2 node, because"; promote
  `rem:is-import`(b) to a numbered lemma with its proof.
- **fine** - `thm:is-import` / `rem:is-import`(c): for `d = 2` the exponents
  of `a+1` are `4` vs `2`; `d\lceil\log_2(d+1)\rceil > d\log_2 d` for every `d \ge
  2`. I could not check the arXiv text (no network); the reading is as
  stated in the paper.
- **fine** - Schedule 1 paragraph: "-1 is a sum of at most `d` `d`-th powers"
  follows from Cauchy-Davenport (`|k(P\cup 0)| \ge \min(p, k(p-1)/d+1)`).
  Exponent claim `1+\sum_{d=2}^9 d\lceil\log_2(d+1)\rceil = 1 + 144 = 145`. Correct.
- **fine (recomputed)** - `rem:combined-schedule`, "unchanged for $c \le 7$,
  and it falls by two for $c = 8$ and $c = 9$, to $143$". Maximizing
  `1+\sum_d e_d(p)` over primes (Schedule 1 at `\kappa_d` below
  `16\kappa_d^{2\kappa_d+2}`, exponent `2` above, `1` when `\kappa_d = 1`), with every
  prime below `2\cdot 10^6` and a prime in every residue class mod
  `\mathrm{lcm}(1..c)` above each threshold: maxima `5, 11, 23, 38, 56, 77,
  107, 143` for `c = 2..9` against Schedule 1 bounds `5, 11, 23, 38, 56, 77,
  109, 145` (attained at `p = 421` for `c = 7`, `p = 2521` for `c = 8, 9`).
  Reproduces.
- **fine** - `thm:power-sde`(iii): `e_1^{\times 4}, e_2^{\times 4}` has no
  zero-sum subset; `D(C_5^2) = 9`; `G(4,2)^3 = 331776^3 \approx 3.65\cdot 10^{16}`.
- **imprecision** - After `thm:power-sde`, "verified exactly, for every
  strictly decreasing profile with $r \le 14$, that ... $\le
  (c-1)!\,[(r+1)!/(r-c+2)!]^2 \le r!\,((r+1)!)^2$". This holds for every `r`
  by a two-line argument, so the finite verification undersells it:
  `(\kappa_d-1)g_d+1 \le (d-1)(g_d+1)` and `g_d \le r-d+2` for a strictly
  decreasing profile `r = g_2 > g_3 > \dots > g_c \ge 1` (so `c-1 \le r`).
  Replacement: "Since $(\kappa_d-1)g_d+1 \le (d-1)(g_d+1)$ and $g_d \le r-d+2$,
  $\prod_{d=2}^c M_d^{\mathrm{sym}} \le (c-1)!\prod_{d=2}^c(r-d+3)^2 =
  (c-1)!\,[(r+1)!/(r-c+2)!]^2 \le r!\,((r+1)!)^2$ for every strictly decreasing
  profile."
- **fine (recomputed)** - `E_2` sets: my own exhaustive search (normalize
  `\beta_0 = 0`, `\alpha_0 = 1`, enumerate `\alpha_j \in z_j^{-1}Q_0^\circ`, then
  intersect the admissible `\beta_i` sets) gives `E_2(2) = \emptyset` (`p <
  400`), `E_2(3) = \emptyset` (`p < 1000`), `E_2(4) = \{5,13,17,29,37,53\}`
  (`p < 1500`), `E_2(5) = \{11,31,41,61,71,101,131,151,181\}` (`p < 400`).
  Ratios `0.69`, `0.29`, and "below `1.7\kappa^{(\kappa+1)/2}` for `\kappa \le 7`"
  (max ratio `1.66` at `\kappa = 4`) reproduce. `T_A(\kappa) < \kappa^{\kappa+1}` for
  `3 \le \kappa \le 9` from the appendix table; the claim "when $\kappa \ge 3$
  and $p \ge \kappa^{\kappa+1}$" for *all* `\kappa \ge 3` rests on
  `cor:app-s2-decoupled`, outside my scope.
- **fine** - `prop:triangular-sde` proof checked line by line: realization
  weights lie in `P\cup\{0\}`; rounds use `(a+1)(a+2)/2` columns; the stopping
  realization has weight `1` on the column with `\delta_i = 1`; back
  substitution keeps `\tau \in U_{l-1}`; supports disjoint. Correct.
- **imprecision** - `prop:triangular-sde`, "where $P=(\Fp^\times)^\kappa$ and
  $g$ generates $\Fp^\times$". Only the coset of `g` in `\Fp^\times/P` is used
  (as the statement itself later says), and a generator of `\Fp^\times` is not
  known to be computable in deterministic polynomial time without factoring
  `p-1`. Also the algorithm is given the contraction `(\alpha,\beta)`, whose
  cost is in `prop:decoupled-sde`, but the statement says only "an
  algorithm that is given $g$". Replacement: "where $P=(\Fp^\times)^\kappa$
  and the image of $g$ generates $\Fp^\times/P$ ... an algorithm that is
  given $g$ and $(\alpha,\beta)$ ...".
- **fine (recomputed)** - `thm:random-column`(i) `\mu \ge
  2^{8u+1}u^{2u+1}`: exact rational check at the least admissible prime for
  every `2 \le u \le 12`, `1 \le \kappa \le u`, `a = u-1`. (ii): nodes per tree
  `\le (4u)^{c-1}/7`; `\Pr[\mathrm{Bin}(4m',1/16) > 3m'] \le 2^{-8m'}`.
- **fine** - `thm:free-coordinate`(ii) `\beta` bound: `h \ge 15u`, `q^a \ge
  u^{-(u-1)}`, `(p^a-1)/(p-1) \le 2p^{a-1}`, `L = 2u-1`. (iii): `n_0`, `M_d`, the
  `\tau_d` union bound (`\eps/9`), the cap (`\eps/9`), rank (`\eps/3`),
  approximation (`\eps/3`): total `8\eps/9`.
- **imprecision** - `thm:free-coordinate` preamble, "Assume the labels at a
  stage-$d$ node are independent and uniform ..., and $\kappa_d < p-1$."
  Part (iii) is a statement about the whole procedure "for every prime
  $p > c$", including grades with `\kappa_d = p-1`, and the label law there is
  derived (Lemma `lem:s3-law`), not assumed. As written, the preamble's
  hypothesis formally excludes the case `p = c+1` that (iii) and Table 1
  ("with the zero-sum node at $p = c+1$") use. Replacement: "Parts~(i) and~(ii)
  concern a node at a grade with $\kappa_d < p-1$ whose labels are independent
  and uniform on a subspace of dimension $a \le g_d$; part~(iii) concerns the
  whole recursion on the i.i.d. supply of Theorem~\ref{thm:main}, for which
  this law is derived in Lemma~\ref{lem:s3-law}."

## Section 5 (uniform compilation, resource tables)

Note: `main.tex` changed while this review was in progress (a new
`\subsection{Notation}`, `sec:notation`, appeared after the Organization
paragraph; file timestamp 12:54). Findings quote phrases, not line numbers.

- **fine (recomputed)** - `thm:uniform-compilation`(i): `(d-1)\sum_{j<d}(j+1)(j+2)/2
  = (d-1)d(d+1)(d+2)/6`. ODE `Z' = [\ad_Z/(1-e^{-\ad_Z})]Y` is the correct
  derivative of `\log(e^Xe^{tY})`. Von Staudt-Clausen gives denominators
  with primes `\le j+1 \le c`. Filiform/`\mathbb F_5` control: `40` grade-3 passes
  `\times 20 + 20` grade-2 passes `\times 4 = 880`. Correct.
- **imprecision** - `thm:uniform-compilation`(i), "solving $Z' =
  [\ad_Z/(1-e^{-\ad_Z})]\,Y$, $Z(0) = X$, coefficientwise in $t$". Here `t` is
  the ODE time, but `t` is the Rees grading variable throughout (the notation
  table lists `t` as "formal variable of $\mathcal{L}[t]$"), and on `\A` both
  expansions are present. Replacement: "coefficientwise in an auxiliary
  variable $\theta$ (with $Z(\theta) = \BCH(X,\theta Y)$)".
- **fine (recomputed)** - `lem:qft-mod`: `\sin^2\theta \in (1/4,1/2)`,
  `\alpha(\theta) = \pi/6`, `d\alpha/d\vartheta \le 1` (iff `\rho \le 1`), prep error
  `3\pi2^{-\tau}`; phase error `\pi b2^{-\tau}`; bad-set mass `\le (1/a+1/a^2)/2`;
  `\eps_{\mathrm{aq}} \le 2\pi t2^{-r}`; the three choices give `\eta/3` each.
  Gate total: `b^2`: `316+12 = 328`; `bt`: `80+12 = 92`; `b`: `39+92+70+38+1 =
  240`; constant `30-8+26+12 = 60`; asymptotic form `420, 187, 4` and `t < b+2L+6.2`,
  `r < L+\log_2 t+5.8`, `\tau < L+\log_2(b+3)+4.3`. Qubits `8b+2t+6`. All check.
- **imprecision** - `lem:qft-mod` reuses `t`, `r`, `\tau`, `a`, `M`, `W`, `Z`, `K`,
  `L`, `S`, `Q`, `E` locally (e.g. `a` is both a qubit and `2^{t-1}/N`; `Q` is the
  Grover iterate, also the query count). Not wrong, but a referee will ask for
  local names (e.g. `\mathsf{a}` for the qubit, `A_{\mathrm{pe}} = 2^{t-1}/N`).
- **fine (recomputed)** - Gate-level control: Heisenberg/`\mathbb F_3`: arity `3`,
  `6` calls, `12` passes; filiform `\mathbb F_5`: `M = (2,5)`, `30` calls, `60` passes;
  class-four `\mathbb F_5`: CW arities `(\kappa g+1) = (5,3,7)`, `|G_4| = 5^{11}`.
- **fine (recomputed)** - Table `tab:full-grade-budget`, class 3 `(6,3,1)`,
  `p = 65537`: `M = (16,2)`, `32` leaves, `54` scalar-flag leaves (`3^3\cdot 2`),
  `S = 10`, `960` queries, `N_{\mathrm{instr}} = 10(32+17+1) = 500`, `480` right
  actions, `1920` passes, `25600+2560 = 28160` brackets, QFT calls
  `3200+2080+1020+60 = 6360`, `q_{\max} = 102`, `\lceil\log_2(9\cdot500\cdot102)\rceil = 19`
  bits, depth-first `2+15+1 = 18`. Class 12, profile `(13,11,10,\dots,1)`,
  `p = 2^{127}-1`: arities `(144,231,100,9,288,259,36,165,16,3,12)`, product
  `7{,}640{,}436{,}342{,}325{,}248{,}000`; queries `12\cdot17\cdot P` exact; scalar
  `3.712\cdot10^{38}`; `N_{\mathrm{instr}} \approx 1.42\cdot10^{20}`. All reproduce. I did not
  recompute the two "Total failure bound" entries.
- **imprecision** - Table `tab:full-grade-budget`: the scientific entries
  are rounded *up* (`3.712\cdot10^{38} \to 3.8\cdot10^{38}`, `7.64\cdot10^{18} \to 7.7\cdot10^{18}`,
  `1.42\cdot10^{20} \to 1.5\cdot10^{20}`). Consistent with "upper bounds", but
  the caption should say "rounded up to two significant figures"; a reader
  checking `3.71` against `3.8` will otherwise flag an error. Also the
  artifact records `profile_existence_certified: false`; the class-12 profile
  is realized by the standard filiform algebra and `(6,3,1)` by a quotient of
  the free 3-generator algebra, which the caption could say.
- **fine (recomputed)** - Table `tab:random-column-budget`: `u = 2,4,12,6`;
  leaves `8 = 8^1`, `256 = 16^2`; caps `28\cdot8\cdot2 = 448`, `40\cdot256\cdot3 = 30720`,
  `68\cdot12\cdot48^{11} \approx 2.6\cdot10^{21}`, `40\cdot5\cdot24^4 = 66{,}355{,}200`;
  `p \ge 16u^2` holds in all four cases (`577 \ge 576`).
- **fine (recomputed)** - Table `tab:fcs-budget`, all six primes: combined
  `Q` = `202.1, 167.3, 852.3, 944.9, 555.4, 61.5`; (iii) `Q` = `42.3, 36.6, 39.1,
  35.9, 34.1, 34.0`; (iii) trials `28.3, 33.4, 33.8, 31.0, 33.5, 31.0`; (iii)
  total `47.0, 50.8, 52.2, 49.8, 51.0, 49.5`, all from my own implementation
  of the least public `M_d` with `\beta \le \tau_d` at `a = g_d`. Uniform-kernel
  columns not recomputed.
- **fine (recomputed)** - Class-nine Schedule 1 profile at `p = 43`: `n = 97`,
  `S = 20`, `\log_2 Q = 1572.66 \to 1573`; exponent `145`.
- **imprecision** - Resource-profile paragraph, "this is $144$ at $c = 9$
  ($146$ with Schedule~1 alone)". "this" refers to `E_W(c)+1`, not to
  `E_W(c)` (which is `143` by my maximization, matching
  `rem:combined-schedule`). Replacement: "so $E_W(9) = 143$ and the query
  exponent $E_W(9)+1$ is $144$ ($146$ with Schedule~1 alone)".

## Section 6 (parameterized regimes)

- **fine** - `cor:fpt-r`(i): `p \ge c+2` excludes `\kappa_d = p-1`; `\alpha` matches
  `prop:fc-uniform`(b) at `\eps = 1/3` (`8/\tau_d = 216(c-1)Sn_d`); `2^\alpha \ge
  16(216cS)^3c^2` and monotonicity of `2^t/(4t)` give `\log_2(4\alpha c) \le \alpha`;
  induction `M_d \le (1+3c)\alpha \le 4\alpha c`; the inequality `x^r \le
  \max(r^{2r},2^{16},2^x)` is true (split at `x = r^2` and `x = 16`); Hoeffding
  `e^{-2R/36}`. The proof gives the stated bound.
- **fine** - `cor:fpt-r`(ii): for `d < c = p-1`, `\gcd(d,c) \le c/2`; zero-sum node
  arity `g_cc+1 \le r^2+r+1`; search cost `(c+1)^{g_c} \le (r+2)^r`. IMS alternative:
  `|G'| = p^r \le (r+2)^r`; certification by `f(x) = f(1)` and order comparison is
  sound.
- **fine (recomputed)** - Paragraph after `cor:fpt-r`: filiform `r = 3,5,9`
  at `p = c+1`: `\log_2 Q = 13.2, 24.3, 42.3` (zero-sum node) and `58.9, 155.8,
  676.8` (Schedule 1 at `d = c`), from my own least-arity computation. Scalar-flag
  factor `\le (r+2)^{r(r+1)/2}` correct.
- **fine** - `cor:codim`: `C_{\mathcal L}(\mathcal I) = \mathcal I`; `\dim \le b(b+1)/2`;
  class `\le 2b-1` (I re-proved it: with `I_j = \phi(\mathcal L)^jI`, `\gamma_b \subseteq
  \mathcal I` and `\gamma_{b+j} \subseteq I_j`); `\dim(\hh\cap\mathcal I) \ge b-k`;
  section independence; codimension preserved in `S/K`; `p \ge 2k+1 \Rightarrow`
  class `\le p-2`; random-column alternative `u = 2k` satisfies `c \le u`, `a_d \le
  u-1`, `p \ge 16u^2 = 64k^2`. I did not verify "both attained at $b = 3$".
- **imprecision** - `cor:codim` proof, "For $k \le 2$ the remainder has class
  at most two". The bound `2k-1` gives `3` at `k = 2`; the claim is true only via
  the dimension bound (`\dim \le 3`). Replacement: "For $k \le 2$ the remainder
  has dimension at most $3$, hence class at most two".
- **fine** - `rem:codim` example: `a_d = 1` at every grade `2..m-1`; `\mathcal I =
  \Span(e_1,\dots,e_{m-1}) = N_{\mathcal L}(\hh)`; remainder one-dimensional.
- **fine** - `thm:ring-to-field`: socle is an ideal; `\exp\mathcal L[p] =
  \Omega_1(G)`; `[\mathcal L[p],\mathcal L[p]] \subseteq [\mathcal L,\mathcal L][p]`
  of dimension `R`; idealizer criterion via `\log\exp(\ad_x)` with denominators
  `< c < p`; rank monotone under sections; `b+1` example for `\mathbb Z/p^b`.
  Quotient-oracle coset claim holds because the idealizer condition puts every
  BCH correction term in `\log H_1`.
- **fine (recomputed)** - Ring examples: `[x,y] = py` on `(\mathbb Z/p^e)^2` has
  class `e`, `R = 1`, abelian socle; `\mathbb Z/3\times\mathbb Z/9` readout orders
  `9` and `3`; call caps `b(b+1)/2 = 21, 36, 32896, 10` for `b = 6, 8, 256, 4`.

## Section 7 (black-box groups, flat subspace sources)

- **fine** - Sylow split; "exponent of $G_p$ is the largest $p$-part of the
  generator orders" (regularity: `\Omega_k` is a subgroup); Witt rank formula;
  `\Phi` a surjective homomorphism by Lazard functoriality; fibers of `\Phi` are
  additive cosets of the ideal `\ker\Phi` (BCH corrections lie in the ideal).
- **fine** - `prop:black-box`(iii): `\Omega_1(F) = pF` for `e = 2`, `\Phi(pF) =
  \mho_1(G) = \langle a^p\rangle \not\ni b`; general `\Phi(p^{e-1}F) = \mho_{e-1}(G)`;
  `\Phi^{-1}(\Omega_1(G)) = \{x : px \in \ker\Phi\}`.
- **imprecision (stale notation)** - `prop:black-box`(iv), "recovers
  $\ker\pi$, as the solution set of $k$ linear congruences" and "the explicit
  chart $F_{s,c}/\ker\pi \cong \log G$". The map `\pi` is never defined in the
  body (it is defined only in Appendix `lem:tb-kernel`, where `\Phi = \pi` as sets);
  items (i)-(iii) and the theorem use `\ker\Phi`. Replacement: `\ker\Phi` in both
  places, or "where $\pi : F_{s,c} \to \log G$ is the Lie ring homomorphism
  underlying $\Phi$".
- **fine** - `prop:black-box`(iv) and `thm:bb-envelope`(ii): `\min(d,n_p)^2 \le
  dn_p \le dk` since `n_p\log_2 p \le \ell`; `k = O(\ell)` under `\log_2(8\ell/\eps) \le
  \ell`, giving `O_c(s^c\ell^2+\ell^4)` ring operations and `O_c(s^c\ell^4+\ell^6)` bit
  operations.
- **fine** - `thm:bb-envelope`(i): per core call `\prod_d M_d \le K_c(m+1)^{E_W(c)-1}`
  holds for all three node types (Schedule 2: `(g+1)((\kappa-1)g+1) \le
  (\kappa-1)(g+1)^2`, and `\kappa-1 \le d^{d(d-1)\lceil\log_2(d+1)\rceil/2}`); core rank slack
  `\lceil\log_p(12\ell/\eps)\rceil \le t`; superadditivity summation; `L \le
  \ell/\log_2(c+1)`. `E_W(c) = 5,11,23,38,56,77,107,143` reproduces (Section 4
  item); `\log_2(9K_9) = 1202.9 + 3.17 \approx 1206` reproduces; `9\cdot 143 = 1287`.
- **fine** - `thm:bb-envelope`(iii)-(iv) error split: the chart transforms
  (`2kd` at `\eps/(16\ell kd)`, i.e. `\eps/(8\ell) = \delta/2` per prime) are inside the
  kernel share `\delta = \eps/(4\ell)` by `lem:tb-kernel` ("total precision
  $\delta/2$"), so the four quarters close.
- **fine (recomputed)** - Remark comparing with Imran-Ivanyos: `\sigma_3 = 2`,
  `\sigma_5 = \sigma_7 = 6`; `2 + 8\sigma_p = 10, 18, 50, 50`.
- **fine** - `thm:subspace-source`(i): `\mathrm{TD} = \frac1r\sum\sin\theta_i`,
  overlap `\prod\cos\theta_i`, `\gamma \ge \mathrm{TD}^2 \ge \delta^2` by Jensen, AM-GM,
  `(1-\gamma)^{r/2} \le \sqrt{1-\delta^2}`. (ii): `\tr P_\wedge(\Pi_V/r)^{\otimes r} = r^{-r}`;
  `p_k = (r-k)/(r(k+1))`; coupon domination `re^{-N/r^2} \le r2^{-B}` and the union
  bound give `\beta`.
- **fine** - Design steps: in-coset phase `\sum_j(\sum_s s^j)\lambda(C_j) = 0`;
  separation `\|\cdot\|_1 \le \sqrt{p^n}\|\cdot\|_F \le \sqrt{p^n}(1-\gamma)^\ell`.
  Heisenberg/`\mathbb F_3` phase `\chi^{1+4} = \chi^2 \ne 1`.
- **fine (recomputed)** - Subspace artifact (`rees_subspace_source.json`):
  `14\cdot 420400 = 5{,}885{,}600`; leaves `2^{1569.49}`, `T = 2^{1591.98}`; raw-copy caps
  `\lceil\log_2\rceil = 1592, 1605, 1609, 1613`; `N = r^2B` with `B = 1598, 1600, 1602`
  gives `6392, 102400, 1640448`; total error bounds `0.153`-`0.184 \le 1/3`;
  multiple-of-`p` route `9\cdot 43\cdot 9777 = 3{,}783{,}699`.
- **imprecision** - Subspace artifact paragraph: `\ell = 420400` is not the
  value the displayed bound of step (3) gives; with `\sqrt{p^n}(1-\gamma)^\ell/2` per
  source and `B_{\mathrm{leaf}} = 2^{1569.5}` leaves, `\ell \approx 2.6\cdot 10^5` already reaches
  error `\eps/4`. The artifact uses a more conservative generic transfer plan
  (`plan_orbit_state_transfer` in `theorems/rees_projective_source.py`). So
  the count is valid but not the one the text derives; add "($\ell$ from the
  artifact's generic transfer bound, larger than step~(3) requires)".
- **fine** - `rem:mixed-source`(i): eigenvalue rounding into `(\lambda-2w,\lambda]`,
  `\tr(\rho-\tilde\rho) < 2w\bar r = \delta/8`, `\sum_lr_l \le \min(\bar r(\bar r+1)/2, 1/w)` (as
  `\tr\tilde\rho \le 1`), convexity gives a factor moved by `> 7\delta/8`, and
  `1-(7\delta/8)^2/2 \le 1-\delta^2/8`. (ii) offset bound `\bar r/M_0` (one bad offset
  per eigenvalue). Growth acceptance uses `k\gamma_\psi \le I`. Correct.

## Section 8 (classical filters, query complexity)

- **fine (recomputed)** - `prop:conjugation`: the `\exp(\mathrm{ad})` witness
  agrees with conjugation for `p > N` and differs from it exactly in the
  window `N \le p \le 2N-2` on every case I tested, as the proposition says.
- **fine** - Collision lemma (the proof around "Realize $Y_j = [U_j <
  D_{j-1}/M]$"): the coupling gives `e \ge X`; `\mu_X \ge (Q-s)^2/(2M)` when
  `Q-s \le M`; `p^{k-1}(t+1) \ge k+t`; and the Chernoff threshold `\mu_X \ge
  \max(2s,8\ell)` gives failure at most `\eps`. The bound holds.
- **fine** - `prop:classical-query`(i)-(v): the arithmetic checks.
  `rem:query-separation` cites EHK Theorem 2 correctly, and the claim "it does
  not lower the query count" is accurate.
- **fine (recomputed)** - Table `tab:query-crossover`: `\log_2 Q_q = 9.00,
  27.76, 33.19, 35.06, 1572.66`; the LB column `443, 337{,}853, 92{,}107, 997`;
  the copies column `81, 301, 407, 644`; and the class-nine thresholds
  `2^{174.72}` and `2^{174.47}`. All reproduce.
- **imprecision** - Table `tab:query-crossover`, column "(v) $< Q_{\mathrm q}$
  for $p <$": the source script
  (`2026-11-02-rees-classical-lower-bound/birthday_crossover.py`) uses
  `w = max(2*(1+t), 15)`. That is, it rounds `8\ell \approx 14.33` up to 15,
  but the displayed `Q` (eq. at "Q = 5(m+t) + 16\lceil \ell\rceil") uses
  `\max(2t+2,8\ell)`. With the displayed `Q` the largest qualifying primes are
  `83, 121{,}493, 42{,}767, 641`, where the paper has `84, 119{,}671, 42{,}290,
  638`. The paper's entries are therefore conservative and still true as "for
  $p <$" thresholds, but they are not what the displayed formula gives.
  Replacement (caption addition): `The column (v) is computed with $8\ell$
  rounded up to $15$, which only enlarges $Q$; with $8\ell$ itself the
  thresholds are the primes up to $83$, $121{,}493$, $42{,}767$ and $641$.`

## Section 9 (formalization, reproducibility)

- **fine (recomputed)** - Table `tab:lean-modules`: the per-module rows sum
  to `396`. The subalgebra counts "$19$, $39$, $220$ and $6453$" reproduce
  (exhaustive enumeration, scratchpad `sub.py`). `numbers.tex` has 163 macros
  (148 + 15), and none is undefined in the body.
- **imprecision (stale against the repository)** - abstract, "BCH and Lazard
  transport for class $c \ge 5$, solvers and running time lie outside that
  boundary". `formal/Formal/Audit.lean` now imports `BCHClassFive`,
  `BCHClassFiveSubgroups` and `ReesGeneralLawClassFive`. It has `455`
  `#print axioms` guards, against the paper's `396`, and `formal/README.md`
  line 17 says "Since 2026-11-04 the same holds at class five". The paper's
  `396` is scoped to "the modules of Table~\ref{tab:lean-modules}" and stays
  literally true, but the abstract's boundary sentence and Table
  `tab:lean-modules` no longer describe the formal tree. I did not build
  these modules. Replacement, once a build is confirmed: `BCH and Lazard
  transport for class $c \ge 6$, solvers and running time lie outside that
  boundary; class five is covered by three modules added on 4 November 2026
  (Section~\ref{sec:formalization}).` Add the three rows to
  `tab:lean-modules` with their guard counts (`455-396 = 59` in all, if
  every new guard belongs to them). Until then, add `as of 3 November 2026`
  to the abstract sentence.
- **tool note (not a paper finding)** - The documented command
  `python docs/papers/rees-hsp/make_numbers.py --check` writes
  `numbers.tex` before it checks, so a "check" modifies a tracked file. I
  ran it once during this review. The regenerated file has the same 163
  macros and values (compared by inspection), and the check reported no
  undefined macro. A read-only `--check` should compare in memory and exit
  nonzero on a difference.

## Cross-reference sweep (body)

Script check over the body (up to `\appendix`) against labels in `main.tex`
and every `appendix-*.tex`: no `\ref` or `\eqref` target is missing, and no
"Lemma/Proposition/Theorem/Corollary/Remark~\ref" names the wrong environment
type. The stale references I found are semantic, not broken labels: the
`prop:black-box`(iv) notation (Section 7) and the class-five boundary above.

## Ranked summary

Counts over the body: **0 errors, 1 gap, 19 imprecisions**, plus one tool
note. The remaining items are fine, and the cheap numbers were recomputed.

Gaps and errors, ranked:

1. **gap** - Proof of `thm:main`, Schedule 1 at grades with `d \nmid p-1`.
   The proof runs Ivanyos-Santha at `\kappa_d = \gcd(d,p-1)` through the
   Bezout exponent, but `thm:is-import` is stated only for `d \mid p-1`, and
   the proof does not cite the Bezout reduction (`x \mapsto x^{u}`, `ud \equiv
   \kappa_d \bmod p-1`, a bijection on the label equations) at the point of
   use. The claim is true, and the fix is a one-sentence citation (Section 4
   entry). Because this sits inside the main theorem's proof, it ranks first.

Imprecisions, ranked by consequence (each is detailed in its section):

2. Bezout-lift dependency bookkeeping is inconsistent: `rem:combined-schedule`
   says "and on the Bezout lift", while the text after `thm:free-coordinate`
   says "no Bezout lift" (Section 4).
3. The `thm:free-coordinate` preamble hypothesis "$\kappa_d < p-1$" conflicts
   with part (iii), which treats `p = c+1` where `\kappa_c = p-1` (Section 4).
4. The undefined `t` in Section 3's `G(\kappa_d,g_d)^{\lceil\log_2 t\rceil}`
   (Section 3).
5. The abstract's "polynomial in $m$, $\log p$, ..." does not say that the
   degree depends on `c` (`E_W(c)`), so the bound is not uniform in `c`
   (Section 1).
6. `def:input-contract`(i) access-model wording (Section 1).
7. The stale class-five Lean boundary in the abstract and
   `tab:lean-modules` (Section 9).
8. The `tab:query-crossover` column (v) uses 15 for `8\ell` (Section 8).
9. The remaining 12 wording and notation items in Sections 1-7: Related-work
   "no abelian subgroup of index", the Section 3 "beyond the simulation"
   charged count, "verified exactly, for every" after
   `thm:power-sde`, the definition of `P` in `prop:triangular-sde`, solving
   `Z'` in `thm:uniform-compilation`(i), the reused symbols in
   `lem:qft-mod`, the scientific entries of `tab:full-grade-budget`, "this is
   $144$ at $c = 9$", the `k \le 2` remainder class in `cor:codim`, the
   `prop:black-box`(iv) notation, the subspace `\ell = 420400`, and the
   copy-lift illustration wording.

Process disclosures: `main.tex` was edited concurrently during this pass (a
`sec:notation` subsection was added after Organization), so locations are
given by label and quoted phrase, not line number. `make_numbers.py --check`
rewrote `numbers.tex` with identical content.
