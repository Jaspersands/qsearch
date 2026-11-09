# Rees HSP paper, referee 13: the overnight text (integration rows I190-I206)

5 November 2026. AI-only adversarial referee pass (Claude Code). Not a human review. No file
other than this report was edited. No git, no network, `make_numbers.py` not run.

Scope: the text named in rows I190-I206 of `2026-11-02-rees-integration-log.md`:
`rem:premature`, `rem:mixed-source`, "Terminology and status labels", `prop:triangular-sde` and
`rem:triangular-scope`, `rem:is-runtime`, the merged `thm:free-coordinate` (preamble and (iv)),
`rem:fc-zero-sum-sis` and the SIS sentence in main, the Lean version note, Lean paragraph,
`tab:lean-modules` and boundary, `rem:sde-subquadratic`, `rem:sde-block-steered`, the K30
exact-exponent clause, the application-3 paragraph, the tower sentence in
`rem:two-level-threshold-size`, and `app:s2-tower`.

**Build** (scratch copy of `docs/papers/rees-hsp/*.tex` and `references.bib`, `latexmk -g -pdf`):
exit 0, 159 pages, 0 Overfull, 3 Underfull, no undefined references or citations, no "Float
too large".

**Counts:** 4 Error, 4 Gap, 13 Imprecision, 7 Style.

## What was re-derived and holds

These were checked by hand. No finding unless listed below.

- `prop:triangular-sde`: the weight identity, the normalisation (the definition requires
  C_00 != 0, so alpha_0 + beta_0 is in P after translation), dim U_k = k, the column count
  sum_{k=0}^a (a-k+1), the closing identity, 3(a+1) eliminations and M + a coset tests.
- `rem:sde-subquadratic`(a): the no-plane argument, the line criterion (both directions,
  including that a nonconstant beta is the same as C_00 != 0 after reindexing), and the count
  a(a+3)/2 + 1 = (a+1)(a+2)/2. (b): the instance construction, the bijection
  c -> (t+c)/(K+c), the per-index bound 1/kappa + 1/(p-1), the union bound, and the bound for
  k = ceil(log_kappa p) + m.
- `rem:sde-block-steered`: dim Omega = E - 1, the form of all weights with value in Omega, the
  Weil bound (LN Thm 5.41), M_E(a) at E = 2 and E = 3, the a^2/(2(E-1)) asymptotics, and the
  1/16 and 1/8 numerics with C(3,2) = 3 (they hold at a = 2, 3 and beyond with the report's
  G_3 >= p/10 and p/54).
- `rem:is-runtime` variant: pi'-parts are kappa-th powers; after e restarts
  |<eta>^kappa| >= |H_1|; total order of subgroups gives H_1 in <eta>^kappa; at most e runs;
  and T^{IS,*} matches e <= log_2 kappa runs times kappa^3 N b^2(a^2+b^2), plus
  kappa^3 log kappa b^5 for the zero sum.
- `rem:fc-zero-sum-sis`: the filiform direct sum has class p-1 and g_c = g; preparation of
  rho_lambda; the block reduction (b); the MP13 condition q >= beta n^delta with
  beta = sqrt(M); the exclusion of arity C g^e p^j (j < 2) via p in [g^k, 2g^k] with k large;
  and the scope argument (d).
- `thm:free-coordinate`(iv): mu >= 2^{8u+1} u^{2u+1} (in fact >= 2^{12u} u^{2u}); and the 1/16
  tree bound (3/64 plus a negligible bank term).
- Tower: `lem:app-s2-refine` (classes j - (i+j) + i = 0, c'_{b*} = alpha_0 + beta_0);
  `thm:app-s2-tower`; `prop:app-s2-step-threshold`(i) (A = (D-1)^2 at r = 2, and the
  reduction to D^2 - 4D + 2 > 0); every constant of (ii) (1.0005, 0.5003, 0.2502, 0.1251,
  0.7225, 0.1809, 0.4312); `cor:app-s2-tower` (including 4 kappa^{max(q+1,7)} and 36 kappa^5);
  A + rD^{r-1} = (r-1)D^r + 1 in "Finding the scalars"; W(8,2) = 2432.9 and W(9,3) = 1.48e6.
- Lean: the kappa = 2 contraction ((1,0),(0,nu-1)) satisfies all four cells (the cell (1,1) is
  nu - 1, a nonzero residue, since nu is the least non-residue). `formal/Formal/Audit.lean` has
  488 `#print axioms` lines, and by namespace 8, 8, 5, 6 and 6 for the five 5-November modules
  (33), so 417 + 33 = 450. Both parts of `tab:lean-modules` sum to 180 + 270 = 450. The sextic
  coefficients in the text match `BCHClassSix.lean`.
- K30: the clause now matches the exact path described in `2026-11-04-rees-k30-exact-exponents.md`,
  except for the normalisation (I4).

---

## Errors

**E1. The tower threshold is not polynomial in kappa.**
`appendix-schedule2.tex:467`, `:526`, `:543`; `main.tex:670`.

Current text:
- (467) `Its prime threshold is polynomial in $\kappa$, but its arity has higher degree in $a$.`
- (526) `\begin{corollary}[polynomial thresholds for composite $\kappa$]`
- (543) `For composite $\kappa$ it is an alternative construction, with a polynomial threshold at a higher arity;`
- (main 670) `This arity has degree $L+1 \ge 3$ in $a$, so the construction is an alternative with a polynomial threshold at higher arity:`

Why this is wrong: `cor:app-s2-tower` needs p > max(4 kappa^{q_1+1}, 4 q_1^2 kappa^5), and also
p > T_A(q_1) when q_1 >= 5, where q_1 is the largest prime factor of kappa. This is polynomial in
kappa only when q_1 is bounded. For kappa = 2q with q prime it is at least 4(2q)^{q+1}, that is
kappa^{kappa/2 + O(1)}, about the square root of the two-level threshold (the tower check, I5,
records the same). For prime kappa the tower is the two-level construction, and the threshold
stays T_A(kappa). The text claims "polynomial" unconditionally in four places.

Replacement:
- (467) `Its prime threshold is $\kappa^{q_1+O(1)}$, where $q_1$ is the largest prime factor of $\kappa$, so it is polynomial in $\kappa$ when $q_1$ is bounded (for example $36\kappa^5$ when $\kappa = 2^i3^j$); its arity has higher degree in $a$.`
- (526) `\begin{corollary}[thresholds for composite $\kappa$]`
- (543) `For composite $\kappa$ it is an alternative construction, at a higher arity, with threshold $\kappa^{q_1+O(1)}$, which is polynomial in $\kappa$ when the largest prime factor $q_1$ of $\kappa$ is bounded;`
- (main 670) `This arity has degree $L+1 \ge 3$ in $a$, so the construction is an alternative at higher arity whose threshold, $\kappa^{q_1+O(1)}$, is polynomial in $\kappa$ when $q_1$ is bounded:`

**E2. The terminology paragraph says the combined rule uses Schedule 3.**
`main.tex:364`.

Current text: `The \emph{combined rule} chooses among Schedules~1--3 grade by grade from public data (Remark~\ref{rem:combined-schedule}).`

Why this is wrong: `rem:combined-schedule` chooses among the linear solver of
`thm:power-sde`(i), Schedule 2 and Schedule 1 at degree kappa_d. It states "The rule itself uses
no label law and does not mix in Schedule~3." `tab:main-regimes` agrees.

Replacement: `The \emph{combined rule} chooses grade by grade, from public data only, among the linear solver of Theorem~\ref{thm:power-sde}(i), Schedule~2 and Schedule~1 at degree $\kappa_d$; it does not use Schedule~3 (Remark~\ref{rem:combined-schedule}).`

**E3. The Lean boundary gives the wrong rank.** `main.tex:1366`.

Current text: `These policies are chosen by the axiom of choice, not computed, and the bound uses $\dim\gamma_{d+1}$ rather than the label rank $g_d$.`

Why this is wrong: the paper defines g_d = dim gamma_d(L) (statement of Theorem main;
`tab:notation`), and the label rank is a_d = dim K_d^perp <= g_d. So dim gamma_{d+1} is
g_{d+1}, not a different quantity from "g_d", and g_d is not the label rank. A reader comparing
this with B_d(g_d) is misled.

Replacement: `These policies are chosen by the axiom of choice, not computed, and the bound uses $g_{d+1} = \dim\gamma_{d+1}(\mathcal{L})$ rather than the label rank $a_{d+1} \le g_{d+1}$.`

**E4. The black-box p-group claim leaves out the class < p restriction.** `main.tex:1197`.

Current text: `In black-box $p$-groups with unique encoding, centralizers, normalizers, intersections and conjugacy search reduce, after abelian quantum subroutines~\cite{IvanyosMagniezSantha2001}, to linear algebra in the Lie ring.`

Why this is wrong: the source, `2026-11-05-rees-application-3.md` (summary item 1 and Lemma E),
proves this only for black-box Lazard groups, that is class c < p. For class >= p there is no
Lazard Lie ring, and no argument is given. Conjugacy search uses the 11-02 Lemma B, not
Lemma E.

Replacement: `In black-box $p$-groups of class less than $p$ with unique encoding, centralizers, normalizers, intersections, automorphism fixed points and homomorphism kernels reduce, after abelian quantum subroutines~\cite{IvanyosMagniezSantha2001}, to linear algebra in the Lazard Lie ring, and conjugacy search reduces to the same data.`

## Gaps

**G1. The kappa = 9 coverage rests on a threshold the paper does not state.**
`appendix-schedule2.tex:545`.

Current text: `At every other prime $p \equiv 1 \pmod\kappa$ one of these constructions applies: above the proved thresholds by Propositions~\ref{prop:app-s2-TA} and~\ref{prop:app-s2-step-threshold}, and below them by complete searches with checked witnesses.`

Why this is a gap: for kappa = 9 the only tower is 1 | 3 | 9. Its second step RC(9;{0,3,6}) is
covered by `prop:app-s2-step-threshold` only for p > min(W(9,3), 4r^2D^5) = W(9,3) = 1.48e6, and
the two-level threshold T_A(9) is 3.1e9. The searches stop at 135000 (tower check §3.3,
E(9;{0,3,6})). They close the range only via the computed second-moment threshold
T_R(9,3) = 134723 of `2026-11-05-rees-threshold-6.md`, Prop. 3.2, which is not in the paper. So
the primes p = 1 (mod 9) in (1.35e5, 1.48e6) are covered by no stated result. (kappa = 4, 6
and 8 are fine: W(4,2) = 96, W(6,2) = 649 and W(8,2) = 2433 are below their search ranges.)

Replacement: `At every other prime $p \equiv 1 \pmod\kappa$ one of these constructions applies: above the proved thresholds by Propositions~\ref{prop:app-s2-TA} and~\ref{prop:app-s2-step-threshold}, and below them by complete searches with checked witnesses, except that for $\kappa = 9$ the searches stop at $135000$, so the primes between $1.35\cdot10^{5}$ and $W(9,3) \approx 1.48\cdot10^{6}$ are covered only by a numerically computed second-moment threshold of the cited report ($T_R(9,3) \approx 1.35\cdot10^{5}$), which is not proved here. No list is given for $\kappa = 7$.`

**G2. `rem:triangular-scope` overstates `rem:sde-subquadratic`.** `main.tex:694`.

Current text: `Remark~\ref{rem:sde-subquadratic} (AI-checked, pending human review) shows that schemes enlarging the realizable space one circuit at a time cannot reach such an arity for columns in general position, and that, under a cryptographic assumption, no classical polynomial-time algorithm solves every solvable instance at arity $a+2$;`

Why this is a gap: part (a) proves the bound only for schemes that meet no circuit whose
dependency lies in one coset before F_p^a is realizable (such a circuit finishes the scheme at
once). Part (b) is stated for primes of size kappa^{a+O(1)}. The summary drops both
conditions.

Replacement: `Remark~\ref{rem:sde-subquadratic} (AI-checked, pending human review) shows that, for columns in general position, schemes that enlarge the realizable space one circuit at a time and meet no circuit whose dependency lies in one coset need $(a+1)(a+2)/2$ columns, and that, under a cryptographic assumption, no classical polynomial-time algorithm solves every solvable instance at arity $a+2$ for primes of size $\kappa^{a+O(1)}$;`

**G3. The cyclotomic coset problem is undefined and uncited.** `main.tex:1197`.

Current text: `The cyclotomic coset problem has class $t(p-1)$ or a cyclic hidden subgroup.`

Why this is a gap: the problem is not defined in the paper, t is undefined, and there is no
citation. The "or" is also wrong. By the report (§5.1), the group R_q^n x| F_p with
q = p^t always has class t(p-1) and always has a cyclic hidden subgroup of order p. For
t >= 2 the class is at least p. For t = 1 the instance is Ivanyos-Santha Cor. 8.

Replacement: `The cyclotomic coset problem of Boucher, Fouque and Shen (an arXiv preprint cited in the report, not checked offline) lives in $(\mathbb{Z}_q[\zeta_p])^n \rtimes \Fp$ with $q = p^t$; its class is $t(p-1)$, which is at least $p$ for $t \ge 2$, and for $t = 1$ its hidden subgroup is cyclic of order $p$ outside the normal part, a case covered by~\cite[Corollary~8]{IvanyosSantha2015}.`

(The paper already cites `\cite[Corollary~8]{IvanyosSantha2015}` for this case at main.tex:130.)

**G4. The terminology paragraph drops a condition on the coherent receiver.** `main.tex:364`.

Current text: `Proposition~\ref{prop:coherent-receiver} proves that one exists, and no complete one is built here.`

Why this is a gap: `prop:coherent-receiver` is conditional on `thm:is-import` and imports the
oblivious simulation of PippengerFischer1979, as its header and the intro (line 237) say. The
terminology paragraph is where a reader looks up status, and here it states the result
unconditionally.

Replacement: `Proposition~\ref{prop:coherent-receiver} proves, conditionally on Theorem~\ref{thm:is-import}, that one exists; none is built or implemented here.`

## Imprecisions

**I1. `rem:is-runtime` writes Omega(kappa) for the number of prime factors.** `main.tex:618`, `:623`, `:627`.

Current text:
- (618) `the following deterministic variant makes at most $e = \Omega(\kappa) \le \log_2\kappa$ runs,`
- (623) `affects neither correctness nor the bounds $\nu+1$ and $\Omega(\kappa)$ on the number of runs;`
- (623) `When $\kappa_d$ is a prime power, in particular for every $d \le 5$,`
- (627) `the argument gives no bound better than $\nu+1$ runs, and the bound displayed above stands`

Why this is imprecise: the paper uses Omega for big-Omega elsewhere (`rem:premature`, and
kappa^{a - Omega(a)} in Schedule 3). "The bounds nu+1 and Omega(kappa) on the number of runs"
therefore reads as a lower bound. kappa_d = 1, which occurs for d <= 5, is not a prime power,
and the variant needs e >= 1. "Displayed above" now points at T^{IS,*}, the nearest display,
not at T^{IS}.

Replacement:
- (618) `the following deterministic variant makes at most $e \le \log_2\kappa$ runs,`
- (623) `affects neither correctness nor the bounds $\nu+1$ and $e$ on the number of runs;`
- (623) `When $\kappa_d = 1$ or $\kappa_d$ is a prime power, in particular for every $d \le 5$,`
- (627) `the argument gives no bound better than $\nu+1$ runs, and the bound $T^{\mathrm{IS}}_d$ stands`

**I2. The nonresidue sentence needs "unconditionally".** `main.tex:618`.

Current text: `and it is an $\ell$-th-power nonresidue for every $\ell \mid \kappa$, which no known deterministic polynomial-time method constructs`

Why this is imprecise: under GRH such an element is found deterministically in polynomial time
(Ankeny and Bach bounds). The claim holds only unconditionally.

Replacement: `and it is an $\ell$-th-power nonresidue for every $\ell \mid \kappa$, which no known deterministic polynomial-time method constructs unconditionally (under the generalized Riemann hypothesis one is found by search)`

**I3. Off-by-one in the back substitution of `prop:triangular-sde`.** `main.tex:687`.

Current text: `if $\zeta_l\neq0$, add the weights of round $l$ for $\zeta=\zeta_l$`

Why this is imprecise: round k produces e_{k+1} and v_{k+1} ("In round k ... e_{k+1} ... form
v_{k+1}"), so (e_l, v_l) come from round l-1. With round l the update
tau - zeta_l(alpha e_l + v_l) does not match the weights added.

Replacement: `if $\zeta_l\neq0$, add the weights of round $l-1$ (the round that formed $e_l$ and $v_l$) for $\zeta=\zeta_l$`

**I4. The K30 clause leaves out the QFT normalisation.** `main.tex:815`.

Current text: `by evaluating the gate list in $\mathbb{Z}[\zeta_p]$ with integer coefficients, each $\mathrm{QFT}_p$ gate taken as the exact transform,`

Why this is imprecise: the exact QFT_p carries the factor p^{-1/2}, so the amplitudes are not in
Z[zeta_p]. The code keeps integer coefficient vectors in Z[zeta_p] times p^{-k/2}, with k the
number of QFT gates in the block (K30 report, §0.2).

Replacement: `by evaluating the gate list exactly, as integer coefficient vectors in $\mathbb{Z}[\zeta_p]$ times $p^{-k/2}$ for a block with $k$ $\mathrm{QFT}_p$ gates, each $\mathrm{QFT}_p$ gate taken as the exact transform $|v\rangle \mapsto p^{-1/2}\sum_w \zeta_p^{vw}|w\rangle$,`

**I5. The kappa = 2 range in `rem:sde-block-steered` also uses a finite computation.** `main.tex:715`.

Current text: `(the second range uses an exhaustive computation of $G_3(p)$ for $p\le11000$)`

Why this is imprecise: the kappa = 2 bound p >= 64a^2 uses G_3(p) >= p/10 for p >= 256. That is
exact computation up to 5000, and the Weil bound only from p >= 4930 (block check, Corollary C).
The status of the first range is not given.

Replacement: `(both ranges use exhaustive computations of $G_3(p)$, for $p\le5000$ at $\kappa=2$ and for $p\le11000$ at $\kappa=3$; finite computations, AI-checked, pending human review)`

**I6. "Both conditions" after four hypotheses, and E >= kappa is not explained.** `main.tex:711`.

Current text: `Both conditions concern the forward pass, including its choice of blocks,`

Why this is imprecise: the sentence before lists four hypotheses (E >= kappa, p not in E_cg,
the circuit condition, the steering condition). "Both" means the last two. Nothing says why
E >= kappa is needed: a round's dependency meets at most kappa classes, so E >= kappa blocks
always suffice.

Replacement: `The circuit and steering conditions concern the forward pass, including its choice of blocks (the hypothesis $E\ge\kappa$ ensures that every round, whose dependency meets at most $\kappa$ cosets, can be split into at most $E$ blocks),`

**I7. "No o(a^2) method" now conflicts with `rem:sde-block-steered`.** `main.tex:694`.

Current text: `No polynomial-time method at arity $o(a^2)$ is known for any fixed $\kappa\ge2$.`

Why this is imprecise: `rem:sde-block-steered` (two remarks later) gives a randomised
polynomial-time procedure with O(a^2/log a) columns for i.i.d. uniform columns at p >= poly(a).
The sentence is true only for arbitrary columns.

Replacement: `No polynomial-time method at arity $o(a^2)$ is known for arbitrary columns and any fixed $\kappa\ge2$ (Remark~\ref{rem:sde-block-steered} gives one for i.i.d.\ uniform columns at primes $p \ge \poly(a)$).`

**I8. `rem:sde-subquadratic`(b): the recovery claim needs m and fresh samples.** `main.tex:704`.

Current text: `So $K$ is recovered in expected time $T+\poly(k,\log p)$ from the values of $c\mapsto\chi(K+c)$ at $k$ uniformly random points.`

Why this is imprecise: the bound above it is at least 1 when m <= 1, and repeating the
procedure needs fresh random points, which are checked by the candidate K.

Replacement: `So, for a constant $m\ge3$ and $p\ge4\kappa k$, $K$ is recovered in expected time $T+\poly(k,\log p)$ from an expected $O(k)$ values of $c\mapsto\chi(K+c)$ at uniformly random points, each candidate being checked on fresh points.`

**I9. `rem:sde-subquadratic`(c): the CHMT threshold is cited from a secondary source and overstates scope.** `main.tex:706`.

Current text: `The best polynomial-time threshold known for underdetermined quadratic systems over fields of odd characteristic is again quadratic, $n\ge m(m+1)/2$ variables for $m$ equations~\cite{ChengHashimotoMiuraTakagi2014},`

Why this is imprecise: the subquadratic check (row 7) read the threshold from Hashimoto's 2023
survey, not from CHMT. CHMT solves "a class of" systems. If it solved every system, at kappa = 2
it would give a(a+1)/2 + 1 < (a+1)(a+2)/2 columns, which would contradict the rest of the
paragraph.

Replacement: `A polynomial-time algorithm for a class of underdetermined quadratic systems over fields of odd characteristic, with $n\ge m(m+1)/2$ variables for $m$ equations, is due to~\cite{ChengHashimotoMiuraTakagi2014} (threshold as listed in a 2023 survey by Hashimoto; whether it covers every diagonal system is not checked here), so the known thresholds are again quadratic,`

**I10. The version note understates the 5 November changes.** `main.tex:91-94`.

Current text: `The version of 5 November 2026 adds the class-six Lean modules and two Lean modules on the SDE step (\file{research/audits/reviews/2026-11-05-rees-lean-c6.md}; machine-checked in Lean; AI-run, pending human review); these are not a human review either.`

Why this is imprecise: the same version merges the two Schedule 3 theorems and adds the
coset-copy extension, `rem:fc-zero-sum-sis`, `rem:sde-subquadratic`, `rem:sde-block-steered`,
`app:s2-tower`, the restart variant of `rem:is-runtime`, the exact K30 exponents and the
application-3 paragraph.

Replacement: `The version of 5 November 2026 adds the class-six Lean modules and two Lean modules on the SDE step (\file{research/audits/reviews/2026-11-05-rees-lean-c6.md}; machine-checked in Lean; AI-run, pending human review), merges the two Schedule~3 theorems into Theorem~\ref{thm:free-coordinate}, and adds Remarks~\ref{rem:fc-zero-sum-sis}, \ref{rem:sde-subquadratic} and~\ref{rem:sde-block-steered}, Appendix~\ref{app:s2-tower}, the restart variant in Remark~\ref{rem:is-runtime} and the exact instrument exponents, all from AI-only reports of 4--5 November; these are not a human review either.`

**I11. The union-chain list skips kappa = 7 without saying so.** `appendix-schedule2.tex:545`.

Current text: `$\{17,41,73,89,137,233\}$ for $\kappa = 8$ and $\{19,37,73,109,127,163,181,199,307,433\}$ for $\kappa = 9$.`

Why this is imprecise: the list jumps from kappa = 6 to kappa = 8. The tower check says the
kappa = 7 run was incomplete (`v_u7_step1A.out` empty).

Replacement: `$\{17,41,73,89,137,233\}$ for $\kappa = 8$ and $\{19,37,73,109,127,163,181,199,307,433\}$ for $\kappa = 9$; the search for $\kappa = 7$ was not completed.`

(G1 offers a combined replacement for the next sentence.)

**I12. The main-text SIS consequence leaves out the quantum qualifier and the polynomial arity.** `main.tex:748`.

Current text: `would approximate worst-case lattice problems in dimension $g_d$ within polynomial factors`

Why this is imprecise: `rem:fc-zero-sum-sis`(c) concludes this in quantum polynomial time when
the node is quantum, and only for abort probability at most 1 - 1/poly. A Rees node is quantum.

Replacement: `would, with abort probability at most $1-1/\poly(g_d)$, approximate worst-case lattice problems in dimension $g_d$ within polynomial factors, in quantum polynomial time if the method is quantum`

**I13. No source is given for the per-module guard counts of the 5 November modules.** `main.tex:1300`.

Current text: `for the class-five modules, a count by namespace in \file{formal/Formal/Audit.lean} on 4 November 2026)`

Why this is imprecise: the 33 new guards have no stated count source. This pass recounted them
by namespace: 8, 8, 5, 6 and 6.

Replacement: `for the class-five modules, a count by namespace in \file{formal/Formal/Audit.lean} on 4 November 2026, and for the class-six and SDE modules one on 5 November 2026)`

**I14. The ternary extension of `rem:fc-zero-sum-sis` keeps the binary Schedule 1 arity.** `appendix-free-coordinate.tex:286`.

Current text: `Parts~(a)--(c) hold with $\{0,\pm1\}$ in place of $\{0,1\}$ at a free-coordinate grade with $h = 2$,`

Why this is imprecise: the last sentence of (c) ("Schedule~1 has arity $B_{p-1}(g_d)$") becomes
B_{(p-1)/2}(g_d) there.

Replacement: `Parts~(a)--(c) hold with $\{0,\pm1\}$ in place of $\{0,1\}$, and with $B_{(p-1)/2}(g_d)$ in place of $B_{p-1}(g_d)$ in the last sentence of~(c), at a free-coordinate grade with $h = 2$,`

## Style

**S1. Notation clashes in the new text.**
- P means prod_d M_d in `tab:notation`, (F_p^x)^kappa in `prop:triangular-sde` (main.tex:675)
  and its two remarks, and P_kappa in the Schedule 3 paragraph (main.tex:729).
  Add to `prop:triangular-sde` after `where $P=Q_0=(\Fp^\times)^\kappa$`:
  ` (the $P_\kappa$ of Schedule~3, not the product $\prod_d M_d$ of Table~\ref{tab:notation})`.
- nu means the prime-factor count (main.tex:618), the coset index g^nu P (main.tex:675), the
  least quadratic non-residue (main.tex:1366) and the relation index of `lem:app-s2-refine`.
  At main.tex:1366 replace `with $\nu$ the least quadratic non-residue and $\mu = \nu - 1$` by
  `with $n_0$ the least quadratic non-residue and $\mu = n_0 - 1$`.
- In `rem:sde-block-steered` (main.tex:711) the blocks G_1, ..., G_E sit next to G_E(p), and
  G already names the group, G_d and G(kappa,a). Rename the blocks:
  `split $S$ into blocks $S_1,\dots,S_E$` and `$W_b=\sum_{i\in S_b}\delta_i\lambda_i$`,
  `$x_i=\delta_i(\beta_b+s)$, $i\in S_b$`.
- In the proof of `prop:app-s2-step-threshold`(i) (appendix-schedule2.tex:515), r is |R| and
  r_i are roots. Replace `with the $r$ distinct roots $r_i = 1 - \xi^{-i}$` by
  `with the $r$ distinct roots $\theta_i = 1 - \xi^{-i}$`, and `$x - r_i$` by `$x - \theta_i$`.
- At appendix-schedule2.tex:532, u clashes with the Schedule 3 u. Replace
  `If $\kappa = 2^u3^v$` by `If $\kappa = 2^i3^j$`.
- In `rem:sde-subquadratic`(b) (main.tex:704), chi duplicates cos. Replace
  `Let $\chi(y)\in\mathbb{Z}_\kappa$ be the coset of $y\ne0$` by
  `Write $\chi(y)=\mathrm{cos}(y)\in\mathbb{Z}_\kappa$ for $y\ne0$`.

**S2. Status labels in headers do not follow the new convention.** The Terminology paragraph
promises one convention.
- main.tex:1148: `[Nonflat sources by spectral flags; argued, AI-checked only]` should be
  `[Nonflat sources by spectral flags; argued; AI-checked, pending human review]`.
- main.tex:513: `[Premature measurement of lower grades]` should be
  `[Premature measurement of lower grades; argued; AI-checked, pending human review]`.

**S3. x is undefined in `rem:premature`.** main.tex:515 uses `$\exp(\Fp\, tx)$`, but the
filiform basis x, e_i is introduced only at main.tex:1015. After `For the filiform algebra of
class $c$ with $3 \le c < p$` insert `, with basis $x, e_1, \dots, e_c$ and $[x,e_i] = e_{i+1}$ for $i < c$,`.

**S4. Ambiguous antecedent after the tower insertion.** main.tex:670: `By them, closing it needs`
should be `By them, closing the square gap needs`.

**S5. Pre-merge wording survives.** main.tex:106 `random-column and free-coordinate schedules
that exploit` should be `a random-column schedule (Schedule~3), with uniform-kernel and
free-coordinate samplers, that exploits`. Line 236 `random-column and free-coordinate` should be
`random-column (both samplers)`.

**S6. A redundant hypothesis.** appendix-schedule2.tex:508: `If $D \ge 4$ and $r \le D$, an`
should be `If $D \ge 4$, an`, since r = |R| <= D always.

**S7. The bibliography uses `{\aa}`.** references.bib:452 has `Damg{\aa}rd`. If the house rule
against `\aa` covers sources, use `Damg{\r{a}}rd`.

## Top three

1. E1: the tower's "polynomial threshold" is false whenever kappa has a large prime factor
   (kappa = 2q gives kappa^{kappa/2+O(1)}). It is stated in four places, including main.tex.
2. E2: the Terminology paragraph says the combined rule chooses among Schedules 1-3, against
   `rem:combined-schedule` ("does not mix in Schedule~3").
3. E4 and G1, tied: the application paragraph claims Lie-ring reductions for all black-box
   p-groups, but the source proves them only for class < p. The tower coverage at kappa = 9
   rests on an unstated computed threshold T_R(9,3).

Claim gates checked: no new text claims a speedup, novelty, independent review, an implemented
coherent receiver, a general SDE solver or a checked formal compiler. The block-steered remark
says "no worst-case improvement". The Lean boundary says "no formally checked compiler is
claimed".
