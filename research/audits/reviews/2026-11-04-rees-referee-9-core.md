# Rees HSP paper: referee 9, the core (Sections 2–4 and `thm:main`)

Date: 2026-11-04. Referee: one AI session (Claude Code). Not a human review.
Target: `docs/papers/rees-hsp/main.tex` as on disk on 4 November 2026 (1341 lines),
lines 248–587. That is the notation tables, Section 2 (`thm:rees-cover`, `lem:homogeneous`,
`prop:single-evaluation`, the Dixmier–Lister paragraph, `lem:copy-lift`, `prop:refresh`),
Section 3 (`lem:central`, the finite-control paragraphs, `rem:premature`), and Section 4 up to
the SDE schedules (`prop:descent`, `rem:product-channel`, `sec:recursion`, `lem:hybrid`, the
proof of `thm:main`). Restatements I also checked: abstract (l. 100–102), intro l. 150–200,
`tab:main-regimes`, Contributions, `rem:is-import`, `thm:uniform-compilation`(iii),
`prop:coherent-receiver`, `cor:fpt-r`, `cor:codim`, `thm:bb-envelope`,
`rem:query-separation`. Work was local only: no git, no network, no `.tex` edits.

## 0. Verdict and counts

**Error 0, Gap 1, Imprecision 10, Style 8.**

I found no false statement and no wrong count in the core. I re-derived P, S, Q, n_d, N_instr,
q_max, the rank bound and the ε/3 split, and they agree with each other and with
`prop:coherent-receiver`, `thm:uniform-compilation`(iii) and `thm:bb-envelope`. The proof of
`thm:main` closes, at total error 2ε/3, with one gap. On the explicit route
(`lem:qft-mod`), the compilation to a *fixed finite* gate set needs Solovay–Kitaev synthesis
of the dyadic rotations. The core gives that synthesis no error budget and does not list it
among the imported ingredients (G1). The appendix (`prop:tb-count-gates`, (H1)) already has
the fix, but the core does not. The other findings are hidden or loose hypotheses, a
misworded remark (I9) and labeling.

Top five:
1. G1 (l. 739, 188, 586): rotation synthesis is unbudgeted and Solovay–Kitaev is not listed
   as an imported ingredient.
2. I1 (l. 185): "a fixed finite universal gate set" hides the hypothesis that X, CNOT and
   Toffoli are exact gates. The error budget charges only the transforms.
3. I10 (l. 1044): `thm:bb-envelope` calls "Theorem main" with the arities of the combined
   rule, but `thm:main` fixes Schedule 1 at M_d = B_d(g_d).
4. I9 (l. 505): `rem:premature` calls exp(⊕_{d≥2} t^d γ_d) abelian for every L. That holds
   only when [γ_i, γ_j] = 0 for i, j ≥ 2, as in the filiform case of the source note.
5. I3 + I4 (l. 739, 558): the proof of `thm:main` relies on "The artifacts take η = …",
   which describes the artifacts, not the algorithm; and N_solver is never defined.

Claim discipline: I saw no speedup, novelty or human-review claim. The front matter and the
sentences after `thm:main`, `lem:hybrid` and the Contributions carry the AI-only status. S4
and S5 list the places where the label is weaker or missing.

## 1. Findings

### G1. Gap: the explicit-transform route has no synthesis budget, and Solovay–Kitaev is not listed

Lines 739, 188, 586.

l. 739 (`thm:uniform-compilation`(iii)): "dyadic rotations $R_k^{\pm1}$, $\mathrm{C}R_k^{\pm1}$
with $k = O(\log((\log N+\log(1/\eta))/\eta))$; over a fixed finite gate set each rotation is
further synthesized, for example by~\cite{DawsonNielsen2006}."

l. 188: "Its only imported ingredients are Theorem~\ref{thm:is-import} (...), the subgroup form
of the Lazard correspondence, and a compilation of the quantum Fourier transform over $\Fp$
(...), either imported from~\cite{Kitaev1995} or given explicitly by Lemma~\ref{lem:qft-mod}".

l. 586: "Theorem~\ref{thm:uniform-compilation}, all proved here and checked by AI sessions
only; ... the compilation of the quantum Fourier transform, imported as stated after
Theorem~\ref{thm:main} or supplied by Lemma~\ref{lem:qft-mod}".

Reason. `thm:main` promises gates "from a fixed finite universal gate set". `lem:qft-mod`
reaches error η only with exact rotations R_k, k ≤ max(r, τ) = Θ(log(1/η)), and these are not
in any fixed finite set. The core then synthesizes them but never charges the synthesis
error, so the per-transform error η of the approximation third is not met as written. Both
routes import Solovay–Kitaev: Kitaev's route says "with finite-gate synthesis", and the
explicit route needs it too. Yet l. 188 and l. 586 call the listed items the only imports and
say that `lem:qft-mod` "supplies" the compilation. Also, `thm:uniform-compilation`(iii) is
not "proved here", since it imports Kitaev. The appendix has the repair
(`appendix-torsion-blackbox.tex` l. 1441): run the lemma at η/2 and synthesize each rotation
to (η/2)/N_rot. The core lacks it.

Fix, l. 739: replace the clause after "with $k = O(\log((\log N+\log(1/\eta))/\eta))$;" by

```latex
over a fixed finite gate set, run Lemma~\ref{lem:qft-mod} at $\eta/2$ and replace each of its
$N_{\mathrm{rot}} = O\bigl((b+\log(1/\eta))(\log(1/\eta)+\log(b+\log(1/\eta)))\bigr)$ rotations
by a Solovay--Kitaev approximation~\cite{DawsonNielsen2006} within operator norm
$\eta/(2N_{\mathrm{rot}})$, at a factor $\operatorname{polylog}(b/\eta)$ in size; by the
triangle inequality over the replaced gates, the result is within $\eta$ of
$\mathrm{QFT}_{\Fp}$ on its canonical subspace with clean workspace. For $p = 2$, which occurs
only when $c = 1$, $\mathrm{QFT}_{\mathbb{F}_2} = H$ is exact.
```

Fix, l. 188: replace "or given explicitly by Lemma~\ref{lem:qft-mod} (AI-checked, pending
human review)." by

```latex
or given explicitly by Lemma~\ref{lem:qft-mod} (AI-checked, pending human review), together,
on either route, with the Solovay--Kitaev synthesis of single-qubit rotations over a fixed
finite gate set~\cite{DawsonNielsen2006}.
```

Fix, l. 586: replace "Proposition~\ref{prop:descent} and Theorem~\ref{thm:uniform-compilation},
all proved here and checked by AI sessions only; the subgroup form of the Lazard
correspondence and the compilation of the quantum Fourier transform, imported as stated
after Theorem~\ref{thm:main} or supplied by Lemma~\ref{lem:qft-mod};" by

```latex
Proposition~\ref{prop:descent} and Theorem~\ref{thm:uniform-compilation}(i), (ii) and~(iv),
all proved here and AI-checked, pending human review; the subgroup form of the Lazard
correspondence; the compilation of the quantum Fourier transform of
Theorem~\ref{thm:uniform-compilation}(iii), imported from~\cite{Kitaev1995} or supplied by
Lemma~\ref{lem:qft-mod}, with the Solovay--Kitaev synthesis~\cite{DawsonNielsen2006} on
either route;
```

### I1. Imprecision (hidden hypothesis): the gate set must implement the permutation blocks exactly

Line 185: "and $\poly_c(m,\log p,w,\log(1/\eps))$ further gates from a fixed finite universal
gate set and classical operations."

Reason. The approximation third charges error only to the single-coordinate transforms
(l. 563, l. 739). The proof treats the BCH passes, evaluations, controlled dilations and
central translations as exact permutations. That holds only if X, CNOT, Toffoli and SWAP are
exact in the chosen gate set, as in Clifford+T. For an arbitrary finite universal set,
for instance one with an irrational rotation and no exact Toffoli, those blocks also carry
synthesis error, and the budget omits it. `prop:coherent-receiver`(i) inherits the same
wording.

Fix, l. 185:

```latex
and $\poly_c(m,\log p,w,\log(1/\eps))$ further gates from a fixed finite universal gate set
that contains $X$, $\mathrm{CNOT}$ and Toffoli, for example Clifford$+T$, and classical
operations.
```

### I2. Imprecision: at p = 2 the explicit route fails

Lines 188 and 739. `lem:qft-mod` needs N odd, N ≥ 3. `thm:main` allows c = 1 < p = 2, so "or
given explicitly by Lemma~\ref{lem:qft-mod}" does not cover p = 2. The fix is the last
sentence of the G1 replacement for l. 739.

### I3. Imprecision: the proof of `thm:main` rests on a sentence about artifacts

Line 739: "The artifacts take $\eta = \eps/(3N_{\mathrm{instr}}q_{\max})$".

Reason. The proof of `thm:main` (l. 583) cites `thm:uniform-compilation`(iii) as "which allots
each of its at most $q_{\max}$ transforms the error $\eta = \eps/(3N_{\mathrm{instr}}q_{\max})$",
and `prop:coherent-receiver`(iii) does the same. The cited sentence describes what the
artifacts do, not what the algorithm does.

Fix, l. 739:

```latex
The algorithm of Theorem~\ref{thm:main}, and the artifacts, take
$\eta = \eps/(3N_{\mathrm{instr}}q_{\max})$,
```

### I4. Imprecision: N_solver is never defined

Line 558: "Each of the $N_{\mathrm{solver}}$ classical solver calls is capped at abort
probability $\eps/(3N_{\mathrm{solver}})$."

Reason. The solver count is needed under Schedule 2 and the combined rule (it is the number of
merge nodes), but the paper never states it.

Fix, l. 558:

```latex
Each of the $N_{\mathrm{solver}} = (m+t)\sum_{d=2}^{c}\prod_{d'=2}^{d-1}M_{d'}$ classical
solver calls, one per merge node, is capped at abort probability
$\eps/(3N_{\mathrm{solver}})$.
```

### I5. Imprecision: "canonical" excludes the oracle label registers

Line 563: "Call a state \emph{canonical} if every register holds field elements below $p$ and
every workspace is clean". Line 578 says the same: "(field elements below $p$)".

Reason. The label registers of U_f in case (a) hold strings in {0,1}^w, not field elements.
Read literally, the ideal lifted-source step leaves the canonical subspace, and
`lem:hybrid` is applied with S_j that the step does not preserve.

Fix, l. 563:

```latex
Call a state \emph{canonical} if every $\Fp$ register holds a value below $p$, every label
register holds a string in $\{0,1\}^w$, and every workspace is clean;
```

At l. 578, make the same change: "(field elements below $p$)" becomes "(values below $p$ in
$\Fp$ registers, arbitrary strings in label registers)".

### I6. Imprecision: `lem:central` does not name its input state

Line 478: "The label $\lambda$ has probability $|K|/|Z|$ for each $\lambda \in K^\perp$".

Reason. The probability is the one for measuring {Π_λ} on ρ_H, and the proof uses that.
Neither the statement nor the paragraph before it says that the input is ρ_H.

Fix, l. 478:

```latex
Measure $\{\Pi_\lambda\}$ on $\rho_H$. The label $\lambda$ has probability $|K|/|Z|$ for each
$\lambda \in K^\perp$, and probability zero otherwise.
```

### I7. Imprecision: `lem:copy-lift` does not fix its points

Line 435: "Exactly $c$ fresh copies of $\rho_H$ produce $\rho_{\exp(\hlift)}$ on
$\widetilde{G}$, without any oracle."

Reason. The proof uses distinct points s_i ∈ F_p^× through `lem:homogeneous`. The statement
names none.

Fix, l. 435:

```latex
Let $s_1,\dots,s_c \in \Fp^\times$ be distinct. Exactly $c$ fresh copies of $\rho_H$ produce
$\rho_{\exp(\hlift)}$ on $\widetilde{G}$, without any oracle.
```

### I8. Imprecision: the class of the group in `thm:rees-cover`(iii) is asserted, not proved

Line 372: "the truncated BCH product makes $\widetilde{G} = (\A, \ast)$ and
$G = (\mathcal{L},\ast)$ groups of the class of $\mathcal{L}$, at most $c$."

Reason. The proof (l. 379) proves the group axioms and the homomorphism property. For the
class it says only "This is the standard Lazard setting". The bound "at most c" has a
one-line proof. Equality needs γ_k(G) = γ_k(L), which `prop:single-evaluation` also uses
(γ_2(L) = log[G,G]), and that is part of Lazard's theorem. Khukhro's theorem number is the
known open item. I could not check it offline.

Fix: append to the proof at l. 379:

```latex
For $x \in \gamma_i(\mathcal{L})$ and $y \in \gamma_j(\mathcal{L})$, the group commutator
$x^{-1}\ast y^{-1}\ast x\ast y$ is a Lie series in $x,y$ that vanishes at $x = 0$ and at
$y = 0$, so each of its terms is a bracket containing both $x$ and $y$ and lies in
$\gamma_{i+j}(\mathcal{L})$. Since each $\gamma_k(\mathcal{L})$ is an ideal, hence a normal
subgroup, the lower central series of $G$ satisfies $\gamma_k(G) \subseteq
\gamma_k(\mathcal{L})$, and the class of $G$ is at most that of $\mathcal{L}$. Equality, with
$\gamma_k(G) = \gamma_k(\mathcal{L})$ as sets, is part of the Lazard
correspondence~\cite{Lazard1954} (see~\cite[Chapter~10]{Khukhro1998}).
```

### I9. Imprecision: `rem:premature` calls a nonabelian subgroup abelian

Line 505: "In it, the character of the abelian normal, noncentral subgroup
$\exp(\bigoplus_{d \ge 2} t^d\gamma_d(\mathcal{L}))$ of the cover is measured on every lifted
source".

Reason. [t^iγ_i, t^jγ_j] ⊆ t^{i+j}γ_{i+j}, so the ideal ⊕_{d≥2} t^dγ_d is abelian exactly when
[γ_i(L), γ_j(L)] = 0 for all i, j ≥ 2. That fails in general. For example, in the free
class-four nilpotent Lie algebra on x, y, z, [[x,y],[x,z]] ≠ 0, so
[t^2[x,y], t^2[x,z]] = t^4[[x,y],[x,z]] ≠ 0. The source note
(`research/REES_PREMATURE_GRADE_MEASUREMENT.md`, l. 30–45) defines the interface only for the
filiform algebra, where all of γ_2 lies in span(Y_j). The derivation is unaffected; the
general wording is wrong.

Fix, l. 505:

```latex
In it, for the filiform algebras below (for which $[\gamma_2(\mathcal{L}),\gamma_2(\mathcal{L})]
= 0$, so that $\bigoplus_{d \ge 2} t^d\gamma_d(\mathcal{L})$ is an abelian ideal; in general it
need not be abelian, since $[t^2\gamma_2(\mathcal{L}),t^2\gamma_2(\mathcal{L})] \subseteq
t^4\gamma_4(\mathcal{L})$), the character of the normal, noncentral abelian subgroup
$\exp(\bigoplus_{d \ge 2} t^d\gamma_d(\mathcal{L}))$ of the cover is measured on every lifted
source,
```

### I10. Imprecision (cross-section): `thm:bb-envelope` names `thm:main` for a different procedure

Line 1044: "Sylow subgroups with $e_p = 1$ use one call of Theorem~\ref{thm:main} on the chart,
of dimension $n_p$. Those with $e_p > 1$ use the recursion of
Theorem~\ref{thm:ring-to-field}(iii) on the chart, with Theorem~\ref{thm:main} on each socle
section".

Reason. `thm:main` fixes Schedule 1 with M_d = B_d(g_d), with exponent 1 + Σ d⌈log₂(d+1)⌉
(145 at c = 9). `thm:bb-envelope` uses the arities of `rem:combined-schedule` (exponent E_W(c),
143 at c = 9). Under that rule the Schedule-2 grades spend the solver third, which the proof of
`thm:main` sets to zero. The procedure is correct by `rem:combined-schedule` and
`sec:recursion` (AI-checked only), not by `thm:main` as stated. The conditionality sentence
of `thm:bb-envelope` already lists `thm:power-sde`(ii), so only the name of the called
object is wrong. The proof sketch has the same wording ("Each core call").

Fix, l. 1044:

```latex
Sylow subgroups with $e_p = 1$ use one run of the recursion of Section~\ref{sec:recursion} on
the chart, of dimension $n_p$, with the arities of Remark~\ref{rem:combined-schedule} in place
of the Schedule~1 arities of Theorem~\ref{thm:main} and with the error split of
Section~\ref{sec:recursion}, whose solver third is now used at the Schedule~2 grades. Those
with $e_p > 1$ use the recursion of Theorem~\ref{thm:ring-to-field}(iii) on the chart, with
that run on each socle section
```

### S1. Style: the dilation's bijectivity is not stated (l. 378)

"The dilation satisfies $\delta_\lambda([t^i x, t^j y]) = \dots$" proves the homomorphism
property only. Append: `and it is bijective, with inverse $\delta_{\lambda^{-1}}$.`

### S2. Style: reused letters (known item m1 of the 2 November referee, still open)

λ is the dilation scalar at l. 371, 386–402 and the central label at l. 470–532. Q is G/Z at
l. 520 and also the query count. t is the Rees variable, the sample excess (l. 557) and the
Bezout exponent (l. 600). n is the cover dimension and the input length at l. 1251. No proof
confuses them, and the notation paragraph (l. 252) warns. The cheapest fix is at l. 520:
`Let $\bar G = G/Z$`, with $\bar G$ in place of $Q$ through the proof of `prop:descent`.

### S3. Style: the m in q_max is redundant (l. 739)

n = Σ g_k ≥ g_1 = m, so max(n, m, …) = max(n, …). You can keep m for readability (the final
readout is the only m-term). Otherwise add `(note $m \le n$)`.

### S4. Style (claim discipline): l. 586 uses a weaker status phrase

"all proved here and checked by AI sessions only". `thm:rees-cover`, `lem:homogeneous`,
`lem:copy-lift`, `lem:central` and `prop:descent` carry no status in their headers, unlike
`prop:single-evaluation` and `prop:refresh` in the same sections. This sentence is their only
label. The G1 replacement for l. 586 changes it to "AI-checked, pending human review".

### S5. Style (claim discipline): two artifact paragraphs lack the label

l. 499 ("Finite control") and the first artifact of l. 501
(`theorems/rees_end_to_end_sim.py`) carry no "AI-checked, pending human review", while the
second artifact of l. 501 does. Insert `(finite computation, AI-checked, pending human
review)` after each artifact's report path.

### S6. Style: the proof of `thm:main` does not cite how the lifted source is prepared (l. 583)

"By Lemma~\ref{lem:homogeneous}, ... each lifted source is exactly $\rho_{\exp(\hlift)}$". The
lemma gives the fibers. The state comes from the preparation paragraph at l. 398. Replace the
opening with `By Lemma~\ref{lem:homogeneous} and the preparation that follows it, or
Lemma~\ref{lem:copy-lift} for coset-copy input,`.

### S7. Style: "a real ε" (l. 181)

The count ⌈log_p(3/ε)⌉ and the gate bound in log(1/ε) presume ε is given finitely. Use `a
rational $\eps \in (0,1)$` or `$\eps = 2^{-k}$ with $k$ given`.

### S8. Style (claim discipline): "The new item to scrutinize" (l. 188)

Read alone, it can sound like a novelty claim. Suggest: `The step that is not a standard
ingredient, and so needs the closest scrutiny, is the composition of homogenization with
all-record central descent.` l. 126 already says that novelty has not been established.

## 2. Re-derivations (all hold)

- `thm:rees-cover`(i)–(iii). The bracket of k homogeneous elements lies in t^jγ_j, j ≥ k. The
  class is exactly c'. The top grade is central. E_s∘δ_λ = E_{λs}, so δ_λ maps E_s^{-1}(h)
  onto E_{s/λ}^{-1}(h), which `lem:homogeneous` uses. Dynkin denominators divide products of
  integers ≤ N ≤ c, so the identities descend from Q through Z[1/c!] to F_p.
- `lem:homogeneous`. det(s_i^k) = ∏ s_i ∏_{i<j}(s_j − s_i). The c conditions are equivalent
  to C_k ∈ h for each k, because h is a subspace. The intersection formula and δ-stability
  hold.
- `prop:single-evaluation`. u = s·tz − t²z gives E_s(δ_λu) = s²λ(1−λ)z. The converse holds,
  and the F_3 Heisenberg example is correct (δ_2(u) = 2tz − t²z, E_1 = z).
- `lem:copy-lift`. R_gR_k = R_{gk} and tr(ρ_H R_g) = 1_H(g). The entry at (a,b) is
  |G̃|^{-1}∏_i 1_H(E_{s_i}(b^{-1}a)) = |G̃|^{-1}1_{exp(hlift)}(b^{-1}a), the coset density.
- `prop:refresh`, and the C_p bank: the lift (R_a, R_{2a}) gives the phases ω^{k(a−b)}ω^{−k(a−b)}
  = 1, hence |G⟩⟨G|.
- `lem:central`. Π_λ is a projector. The probability is |Z|^{-1}Σ_{z∈K}χ_λ(−z) = |K|/|Z| on
  K^⊥. In tr(ρ_λR_g), hzg = 1 forces g = h^{-1}(−z), with |K| decompositions.
- `prop:descent`. The output entry is |Q|^{-1}∏_{s_i≠0}tr(ρ_{λ_i}R_{δ_{s_i}(g)}), with
  g = σ(r)^{-1}σ(q) and π(g) = r^{-1}q, so it is exactly ρ_{HZ/Z}. The witness enters only
  through Σ s_i^dλ_i = 0, and the active set is nonempty.
- `rem:product-channel`. SUM(χ_a⊗χ_b) = χ_{a−b}⊗χ_b, and the p = 5 example holds.
- Recursion. G_d/Z_d = G_{d−1}, H_dZ_d/Z_d = H_{d−1}, and σ is H-independent. The generator
  argument K = ⟨exp b_i⟩ = H holds.
- Counts. A grade-d node consumes M_d sources on G_d. There are n_d = ∏_{2≤d'<d}M_{d'}
  grade-d nodes per terminal sample and n_cM_c = P leaves. Hence N_instr = S(P + Σ_d n_d + 1),
  and Q = cSP, as in `thm:main`, `prop:coherent-receiver` and `rem:query-separation`. The
  transform counts n, 2M_dg_d + D_{d−1} and m match the instrument grouping of l. 559. The
  approximation total is N_instr·q_max·η = ε/3.
- Rank: P(fail) ≤ ((p^a−1)/(p−1))p^{−(m+t)} < 1/((p−1)p^t) ≤ ε/3 for a ≤ m. Total error:
  ε/3 + ε/3 = 2ε/3 ≤ ε, with the solver third zero under Schedule 1. B_{κ_d}(g_d) ≤ B_d(g_d),
  and the Bezout identity u^{td} = u^κ holds for all u (t ≥ 1).
- `lem:hybrid`. The telescoping sum holds, and the suffix is contractive.
  √(1−|⟨φ|φ'⟩|²) ≤ ‖φ−φ'‖, via 1−x² ≤ 2(1−x) ≤ 2(1−Re⟨φ|φ'⟩). Convexity over purifications
  holds.
- `prop:coherent-receiver`(iv). Sn_d = (Q/c)/∏_{d'≥d}M_{d'} and Sn_dM_d ≤ Q/c. The labels
  satisfy Σ_d n_dM_dg_d ≤ Pn and SPn ≤ Qm. The quotient addresses use n_d ≤ P/2. The qubit
  total is (2 + (c−1)/2)Qmb + Qw = ((c+3)/2)Qmb + Qw.
- Exponents. Σ_{d=2}^9 d⌈log₂(d+1)⌉ = 144, so the Schedule-1 exponent is 145. E_W(c) =
  5, 11, 23, 38, 56, 77, 107, 143 is reproduced by p = 3, 7, 13, 61, 61, 421, 2521, 2521 (at
  p = 2521 ≥ 1024 grade 2 becomes two-level). log₂(9K_9) ≈ 1206.0.
- Numeric macros. DL: dims (8,4,2), cover 14, C(14,2) = 91, 273 = 3·91, C(56,2)·3 = 4620,
  224 equations in 64 unknowns. Finite control: 5^6 and 5^5 fibers, arities 2 and 5, 10 sources
  and 30 queries. ReesScale: B_2(3) = 1024, B_2(1) = 64, B_2(2) = 324, B_3(1) = 46656,
  G(3,2) = 729, B_3(2) = 531441. Query totals: 7,077,888 = 786432·9; 1,146,617,856 =
  4·6·1024·729·64; ≈1.25·10^12 = 4·9·1024·531441·64.
- Dixmier–Lister, recomputed in scratch:
  `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/dl.py`.
  Jacobi holds on all triples. The derivation system has rank 52 over Q and modulo every
  prime 5 ≤ p ≤ 31 (50 at p = 2, 48 at p = 3). The printed 12-parameter family satisfies all
  224 equations.

Not re-raised (known, owner decision): B_d(0) > 1 at empty grades g_d = 0 (referee-3 decision
2). It wastes sources, but the bound "at most Q" and the proof stay valid, because any nonzero
s works when Z = 0.

## 3. Citations I could not verify offline

- `Khukhro1998`: chapter numbers 9–10 are plausible. The theorem number (10.13, in the
  comment of `appendix-codimension.tex`) is the known open item.
- `Kitaev1995`: "Section 5, Theorem 2 and eq. (25)".
- `CleveWatrous2000`: "arXiv version, Section 7.1".
- `IvanyosSantha2015`: all internal numbers (Thm 3, Thm 5 and §5, Prop 7, Cor 8, Props 9–10,
  Thm 11, Lemma 12, §§3.1–3.3). `rem:is-import`(e) says these were checked by AI sessions
  only. The arithmetic of `rem:is-import`(c) is right as a statement about what the proof
  gives.
- `vandeWoestijne2005`: "Section 6" and "Section 6.1" in a six-page ISSAC paper (pp. 348–353).
  These may point to the thesis of the same title. Check which one is meant.
- `Lazard1954` and the subgroup form; `Trappeniers2024` Thm 2.3; `EttingerHoyerKnill2004`
  Thm 2; `IvanyosSanselmeSantha2012` Thm 2; `ImranIvanyos2023` Thm 1, Prop 3, §1 and §6.

I found no citation that is clearly misused. `PippengerFischer1979` (an oblivious simulation
in O(T log T) and circuits of that size), `Bennett1973`, `DawsonNielsen2006`
(Solovay–Kitaev) and `DixmierLister1957` are used for what they contain.

## 4. Claim gates

All must stay false: `independent_review`, `novelty_established`, `speedup_claim_allowed`,
`coherent_receiver_implemented`, `general_sde_implemented`, `formal_compiler_checked`. Nothing
here changes any status. The core result stays "AI-checked, pending human review",
conditional on `thm:is-import`.

## 5. Next step

Integrator: apply G1 (three drop-ins), then I1–I10. Build with `latexmk` in
`docs/papers/rees-hsp/`. Acceptance: 0 undefined references, and `grep -n 'artifacts take
\$\\eta' main.tex` returns nothing.

## Applied (11-04)

Applied by one AI session (Claude Code) to `docs/papers/rees-hsp/main.tex`, matched by quote.
Backup of the previous file:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i184/main.tex`.
The checking script cited in Section 2 (Dixmier–Lister) is archived at
`research/audits/reviews/2026-11-04-rees-referee-9-core/dl.py`; the scratch path above it no
longer applies. Counts: 19 findings, 13 applied as written, 6 applied with modifications, 0 skipped.

- **G1** modified. `thm:uniform-compilation`(iii): the rotations are now "counted as single
  gates", followed by the appendix wording of (H1) in `prop:tb-count-gates`: run
  `lem:qft-mod` at η/2 and synthesize each of its N_rot rotations "to operator-norm error η/2
  divided by their number", for example by `DawsonNielsen2006`, at a factor polylog(b/η),
  with b = ⌈log₂ N⌉ defined in place (the core states the lemma's size in log N), plus the
  report's triangle-inequality sentence and the p = 2 sentence. "QFT_{F_2} = H" became "is the
  Hadamard gate", since H is the hidden subgroup. l. 188: added as proposed, with "of the
  rotation gates" in place of "of single-qubit rotations" (CR_k is a two-qubit gate). l. 586:
  applied as written. The existing key `DawsonNielsen2006` is used; no bib entry was added.
  The Kitaev route keeps its "with finite-gate synthesis" clause; its synthesis budget is
  not split separately (the report gave no drop-in for it).
- **I1** modified. "that implements X, CNOT and Toffoli exactly, for example Clifford+T": Toffoli
  is an exact Clifford+T circuit, not a gate of that set. The same hypothesis was added to
  `prop:coherent-receiver`(i) ("as in Theorem main"), which the report says inherits the
  wording.
- **I2** applied through the p = 2 sentence of G1.
- **I3** applied. The acceptance grep `artifacts take \$\\eta` now returns nothing.
- **I4**, **I5** (both places), **I6**, **I7** applied as written.
- **I8** modified. The drop-in was appended to the proof of (iii), plus one sentence: "The same
  argument applies to A, whose class equals that of L by (i)", since (iii) also states the
  class of G̃. No Khukhro theorem number was added.
- **I9** modified. The restriction is the report's, split into sentences: the interface is
  "defined there only for the filiform algebras below"; for these [γ₂, γ₂] = 0, so the ideal is
  abelian, but not in general, since [t²γ₂, t²γ₂] ⊆ t⁴γ₄ can be nonzero.
- **I10** modified. Applied the report's wording, with "(a *core call*)" added so that "core call"
  in (iii), (iv) and the proof sketch keeps a referent. Error budget checked: each core call
  receives ε/(4ℓ) under (iv) and splits it into the thirds of `sec:recursion`, now with the
  solver third used at the Schedule 2 grades. So each call is within ε/(4ℓ), at most ℓ calls
  give ε/4, and the four quarters sum to ε. The rank count t = ⌈log₂(12ℓ/ε)⌉ ≥ ⌈log_p(3/(ε/(4ℓ)))⌉
  is unchanged. The conditionality sentence ("conditional on Theorem main, on
  Theorem power-sde(ii) through the combined rule") was left as is.
- **S1**, **S2** (Q → Ḡ in the setup of `prop:descent`, its statement and its proof), **S3**
  ("here m ≤ n; the term m is listed for the final readout"), **S4** (through G1, l. 586),
  **S5** (both artifacts), **S6**, **S7** ("a rational ε"), **S8** applied.

Citation locators (Kitaev Section 5, Theorem 2, eq. (25); Cleve–Watrous Section 7.1; van de
Woestijne "Section 6" and "Section 6.1"; Khukhro) were not changed: no number was added or removed,
and the printed text was not softened. The only safe step taken was a source comment
`% NEEDS HUMAN VERIFICATION (referee 9, 2026-11-04)` after each of the two van de Woestijne
locators (`rem:is-runtime` and the paragraph after its equation), asking whether they point to
the six-page ISSAC paper or to the thesis. It does not change the PDF. Claim gates are unchanged.
"AI-checked, pending human review" labels: all kept; three added (l. 586 and the two artifacts
of S5).

Build: all `*.tex` and `references.bib` copied to the scratchpad build directory, `latexmk -g
-pdf`: 147 pages, 0 Overfull, no "Float too large", no undefined references or citations, no
LaTeX warnings. `tests/tools/test_rees_paper_numbers.py`: 2 passed.
