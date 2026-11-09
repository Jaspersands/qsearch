# Rees HSP paper: referee 11, subspace source, classical filters, Lean and reproducibility

Date: 2026-11-04. Referee: one AI session (Claude Code). Not a human review.
Target, as on disk on 4 November 2026 (`main.tex`, 1343 lines):

- `main.tex` Section 7, flat-subspace part only: l. 1070–1128 (`thm:subspace-source`, the
  four steps, `cor:subspace-hsp`, `rem:mixed-source`, the budget paragraph). The black-box
  part (l. 1024–1068) was refereed earlier today and is skipped.
- `main.tex` Section 8, "Classical Filters for Natural Algebraic Actions", l. 1131–1259.
- `main.tex` Section 9, "Mechanical Verification in Lean 4 and Reproducibility", l. 1262–1331.
- `appendix-subspace.tex`, in full (424 lines).

Work was local only: no git, no network, no `.tex` edits. Interpreter
`/opt/anaconda3/bin/python`; Lean via `~/.elan/bin/lake` in `formal/`.

## 0. Verdict and counts

**Error 1, Gap 2, Imprecision 13, Style 8.**

The one Error and one of the Gaps are in `formal/README.md`, which the paper names as the
scope document for its Lean table. They are not in the `.tex` files. In the `.tex` scope I
found no false statement and no wrong count. Everything I checked agrees with the artifacts:
the exterior-state theorem, the streaming preparer, the `M·ℓ` lift cost, the `T(N+1)` copy
bound, the hybrid in `thm:app-sub-hsp`, the design lemma, the profile numbers, the
conjugation proposition, the collision lemma, all five parts of `prop:classical-query`, the
query table rows and the Lean claims. The findings are underspecified statements, small
mismatches between paper and Lean, labels and notation.

Top five:
1. E1 + G2 (`formal/README.md` l. 392 and its tables): README still says "No group law is
   constructed for `c ≥ 5`" and has no rows for the three class-five modules. The paper's
   Table `tab:lean-modules` cites README for scope.
2. I1 (l. 1108): `cor:subspace-hsp` uses `N` without fixing `β` (so without fixing `B`), and
   it omits the `rT·G_R(ε/(16rT))` term and the precision allocation that
   `thm:app-sub-hsp` needs.
3. I13 + I8 (l. 1077, 1022, 1135): `thm:subspace-source` has no "AI-checked, pending human
   review" label, and "re-audited on 31 October" does not say who did it. It was AI
   referees, per STATE.md.
4. I9 (l. 1197): in `prop:classical-query`(iii), "the same holds with `p^{m-k}` replaced by
   `p^{z_k}`" also carries over the "hence `q > sqrt(2(1-δ)|G|/|H|)`" clause, which is false
   in the normal case.
5. I10 + I11 + I12, and G1: three places where the paper says more than the Lean statement or its
   source. `E_s` maps onto `γ_{k+1}` only for a unit `s` (Lean `IsUnit s`). The group-law
   condition is three Lean hypotheses, not one. The Lean triangular theorem assumes `g`
   generates `F_p^×`. Separately, G1: the paper says the recovery step `W†` is the cited
   Bene Watts et al. algorithm, which nobody has checked.

## 1. What was checked and found correct

### 1.1 Flat subspace source (main l. 1075–1128, appendix)

- `lem:app-sub-angles`. I checked the trace-norm, Frobenius and `|det|` identities, and the
  chain `∏cos θ_i ≤ (1-μ)^{r/2} ≤ (1-δ²)^{1/2} ≤ 1-δ²/2` (Cauchy–Schwarz plus AM–GM).
- `prop:app-sub-ray`: (a) the converse direction is fine; (b) `χ^p = 1`.
- `lem:app-sub-character`. All four steps are fine. In Step 3 the degree in each variable is
  at most `c' ≤ p-1`, and the `st` coefficient is `[x,y]`.
- `cor:app-sub-cancel` and the Heisenberg counterexample: for `C = t²z` and `S = (1,2)` the
  product is `χ(exp z)^{1+4} = χ(exp z)^2 ≠ 1` over `F_3`.
- `lem:app-sub-antisym`(a)–(c), `lem:app-sub-growth`(a)–(c), `lem:app-sub-lcu`:
  - The accept Kraus operator is `P_{k+1}` on `range(P_k⊗I)`.
  - The reject branch with `W†` gives `|0⟩⊗(I-P_{k+1})ψ`.
  - The procedure uses `2k` controlled swaps and two applications each of `J` and `J†`.
  - This gives "at most `2(r-1)` swaps and four `J^{±1}`" in `thm:app-sub-hsp`(ii).
- `prop:app-sub-stream`:
  - Coupon domination works: `Σ_{k=1}^{r-1} Geom(p_k)` with `p_k ≥ (r-k)/r²` is dominated
    by `Σ_{j=0}^{r-1} Geom((r-j)/r²)`.
  - `Pr(Y > N) ≤ r e^{-B} ≤ r 2^{-B}`, and the union bound gives `β`.
  - Copies: one per output plus one per attempt, so at most `T(N+1)`.
  - `∏ p_k = r^{-r}`, which matches the probability of projecting `r` raw copies.
- `lem:app-sub-design`:
  - (a) is the root-of-unity sum.
  - (b): the moments factor, `M ≤ (c+1)!`, and both coverage cases work. The `c = p-1` case
    works because `S ⊇ xS'`.
  - (c) is the Vandermonde argument.
  - The 14-point design mod 43 in `rees_subspace_source.json` has 14 distinct 14th roots of
    unity. Moments 1–10 vanish (exact check).
- `lem:app-sub-lift`:
  - Entry formula: each slot multiplies the `(a,b)` entry by `φ(E_s(b^{-1}∗a))`.
  - Off `H̃`, some `E_s(g) ∉ H` because `S` has `c` distinct nonzero points.
  - `TD ≤ ½ p^{n/2}(1-γ)^ℓ` through `‖X‖_1 ≤ p^{n/2}‖X‖_F`.
  - The cost is `Mℓ` states and `rMℓ` controlled `R` calls per lifted source, which gives
    `T = MℓB_leaf` and at most `rT` controlled `R` calls.
- `thm:app-sub-hsp`:
  - `b`, `ℓ`, `B` and `β = ε/8` agree.
  - Run 1: `B_leaf·½p^{n/2}·p^{-n}ε/(8B_leaf) = εp^{-n/2}/16`.
  - Run 3: `ε/8 + ε/16 + ε/16 = ε/4`.
  - The total is `11ε/16 < ε`.
  - The "precision against the circuit, not against `G_k`" argument is sound: Run 2
    compares exact circuits on their reachable domain, and Run 3 uses the diamond norm on
    the whole space.
- `rem:app-sub-profile`, recomputed from the stated formulas:
  - `b = 526 + 1 + 1575 = 2102`, `ℓ = 420400` and `T ≈ 2^{1591.98}`.
  - `B = 1598, 1600, 1602` and `N = 6392, 102400, 1640448`.
  - Raw copies `2^{1604.62}, 2^{1608.62}, 2^{1612.62}`, rounded up to the macros
    `1592, 1605, 1609, 1613`.
  - `Mℓ = 5,885,600`, `43·9777 = 420411` and `9·420411 = 3,783,699`.
  - The artifact's abort budget is `1/24 = ε/8`, so it uses the same `B`. Its total error
    bound is at most 0.185 for every rank.
- `rem:mixed-source`(i), the argued part:
  - The rounding lies in `(λ-2w, λ]`, `tr(ρ-ρ̃) < 2w r̄ = δ/8`, and `> 7δ/8` passes to
    one `Q_l/r_l`.
  - This gives `1-(7δ/8)²/2 ≤ 1-δ²/8`.
  - `Σ r_l ≤ 1/w = 16r̄/δ`.
  - The bad-offset probability is at most `r̄/M_0`: each window of width `w/(2M_0)` holds at
    most one grid point.
- `rem:app-sub-sharper`: `γ_r ≥ min{rδ²/4, 1/2}` and the ratio `min{r/2, 1/δ²}`.

**"Product design with M ≤ 1890 at c = 9"**: this is not stated anywhere in the paper. The
paper gives only the general `M ≤ (c+1)! = 3,628,800` (Lemma (b)) and uses `M = 14` from
Lemma (a). For reference, I took the smallest possible supports at `p = 43, c = 9`. Odd `j`
uses `(1,-1)`, and even `j` needs 3 terms. The Lemma (b) product then has
`M = 2·3·2·3·2·3·2·3·2 = 2592` (exact search, scratchpad). Lemma (b) does not promise
smallest supports, so `(c+1)!` is the right stated bound.

### 1.2 Classical filters (l. 1131–1259)

- Opening paragraph:
  - `ad_x^p = 0` holds, because `(L_x-R_x)^p = L_{x^p}-R_{x^p}` in characteristic `p` and
    `x^p = 0`.
  - The truncated `exp(ad_x)` differs from conjugation exactly when some term
    `x^iM(-x)^j` with `i+j ≥ p` and `i,j ≤ N-1` survives, that is, when `p ≤ 2N-2`.
  - The witness `J_N, E_{N1}` is correct: `x^iE_{N1}x^j = E_{N-i,1+j} ≠ 0`.
- `prop:conjugation`: the proof is correct (`x ∈ F_p[exp x]` and `exp x ∈ F_p[x]`, so the
  commutants are equal). The transporter equation is correct.
- `lem:collision`: the coupling argument is correct, including that runs with the same
  fresh-label stream agree until an `H∖K` collision.
- `prop:classical-query`:
  - (i) `q² > 2(1-δ)p^{m-1}`.
  - (ii) `z ≤ m-2` and `p^{m-2}(p+1) ≥ p^{m-1}+1`.
  - (iii) the counting and the central one-dimensional ideals.
  - (iv) checked.
  - (v) the Burnside bound, the Bernoulli coupling `e ≥ X` on `{e < s}`, both cases of `μ_X`,
    and `p^{k-1}(t+1) ≥ k+t`.
  - The `Θ` statement is correct; `m ≤ 2p^{(m-1)/2}` holds.
- `tab:query-crossover`, Heisenberg row, recomputed:
  - LB: `q = 508` suffices at `p = 439` and `q ≥ 513` at `p = 443`, against `Q_q = 512`.
  - Birthday: `Q = 52 + ⌈√30·p⌉ = 507 < 512` at `p = 83`; with `8ℓ` itself the threshold is
    also 83.
  - Copies: `⌈4log_2(3·393388)⌉ = 81`.
  - The filiform thresholds `2^{16.87}` and `≈337k` agree with `birthday_crossover.json` and
    with a direct estimate.
- `rem:query-separation`: limits (a)–(c) are present, and "We claim no speedup for any
  concrete problem" is present.

### 1.3 Lean (Section 9)

See Section 3 below. Every guard count in `tab:lean-modules` is exact. No `sorry`, `admit`
or custom `axiom` appears, and the build succeeds. The statements match the paper, apart from
I10, I11, S6 and the README issues E1 and G2.

### 1.4 Reproducibility (l. 1320–1331)

- `numbers_map.json` has 163 entries. 148 come from 9 reports, matching the 9 regeneration
  steps in `reproduce.sh` plus `compare`. 15 come from 4 saved files in
  `2026-11-02-rees-e2e-scale/`. This matches "148" and "15".
- `numbers.tex` defines 163 macros.
- I did not run `reproduce.sh`; the paper says some steps take an hour. I did not run
  `make_numbers.py`, because its default mode rewrites `numbers.tex`.

## 2. Findings

Line numbers are those of `main.tex` unless prefixed `app` (`appendix-subspace.tex`).

### Errors

**E1 (Error; artifact `formal/README.md` l. 392, not `.tex`).**
Quote: "No group law is constructed for `c ≥ 5`."
Reason: This is false since 4 November. `ReesGeneralLawClassFive.bchLaw : NilpotentGroupLaw F 5`
exists, and README's own introduction (l. 17–19) says so. The paper's Lean section (l. 1316)
says correctly that the class-five hypotheses are discharged. But Table `tab:lean-modules`
says "scope in `formal/README.md`", so the paper sends readers to a contradicting sentence.
Fix (Markdown, README l. 391–392):
```text
supplied copies; no solver, circuit, runtime or error bound is extracted. Class five is
covered by `BCHClassFive`, `BCHClassFiveSubgroups` and `ReesGeneralLawClassFive`
(2026-11-04); no group law is constructed for `c ≥ 6`.
```

### Gaps

**G1 (Gap; l. 1086, l. 1091, app l. 257).**
Quotes: "The streaming antisymmetrization instrument of Bene Watts et al. ... instead adds one
fresh copy"; "Rejection must apply the inverse of the instrument's
linear-combination-of-unitaries preparation before the fresh register is discarded"; app:
"This is the growth measurement of~\cite[Algorithms~1--2]{BeneWatts2026}".
Reason: The paper shows that without `W†` the invariant fails (weight 1/2 outside `∧²V` at
`d = r = 3`). It then calls the corrected procedure "the growth measurement of" the cited
algorithms. Nothing in the paper or the cited-notes report says whether those algorithms
include the recovery step. If they do not, the attribution overstates the source. If they do,
the main-text "must" reads as a correction that is not one. I could not check this offline.
Drop-in (main l. 1086, replacing the first two sentences of (ii) after the first):
```latex
The streaming antisymmetrization instrument of Bene Watts et al.~\cite{BeneWatts2026}, with the recovery step of Lemma~\ref{lem:app-sub-lcu}, instead adds one fresh copy to a retained state in $\wedge^k V$.
```
Drop-in (app l. 257, last sentence):
```latex
This is the growth measurement of~\cite[Algorithms~1--2]{BeneWatts2026}; Lemmas~\ref{lem:app-sub-growth} and~\ref{lem:app-sub-lcu} prove the properties used here, including the recovery $W^\dagger$ on rejection. We have not checked line by line whether~\cite{BeneWatts2026} states that recovery step.
```

**G2 (Gap; artifact `formal/README.md`, section "General-Class Layer And Class Four").**
Reason: The paper's table caption says the scope of every module is in README. README has
module tables for every other paper module, but no row for `BCHClassFive`,
`BCHClassFiveSubgroups` or `ReesGeneralLawClassFive`. Only the introduction (l. 17–19)
mentions them. I checked their statements directly (Section 3).
Fix (Markdown rows to add to the README table after `ReesGeneralMeasuredReceiver`):
```text
| `BCHClassFive` | 8 | Quintic BCH group (degree-5 terms with 1/720, 1/360, 1/120) from Jacobi and `lowerCentralSeries F L L 5 = ⊥`, over any field with 2, 3, 5 nonzero; Lie maps give group maps; powers are scalar multiples. |
| `BCHClassFiveSubgroups` | 8 | Every subgroup of the prime-field class-five BCH group (`p > 5`) is a Lie subalgebra, with both round trips. |
| `ReesGeneralLawClassFive` | 5 | The quintic law satisfies all three hypotheses at `c = 5` over `ZMod p`, `p > 5`; tuple hiding, terminal source and measured terminal source for arbitrary `H` at points `1,...,5`. |
```

### Imprecisions

**I1 (Imprecision; l. 1108, `cor:subspace-hsp`).**
Quote: "It uses at most $T(N+1)$ raw copies, at most $TN$ growth instruments, at most $rT$
controlled-$R$ calls and polynomial public arithmetic, where $T = M\ell B_{\mathrm{leaf}}$,
..."
Reason: `N = r²B` with `B = ⌈log₂(rT/β)⌉`, but the corollary never fixes `β`. The error
`ε` depends on `β = ε/8` (`thm:app-sub-hsp`). The corollary also leaves out the
implementation accuracy of `R` and the `rT·G_R(ε/(16rT))` gate term of
`thm:app-sub-hsp`(iii). "Efficiently controlled" covers polynomiality, but the stated counts
are incomplete without these.
Drop-in (replace that sentence):
```latex
It uses at most $T(N+1)$ raw copies, at most $TN$ growth instruments, at most $rT$ controlled-$R$ calls, each implemented within $\eps/(16rT)$ in diamond norm, and polynomial public arithmetic, where $T = M\ell B_{\mathrm{leaf}}$, $\ell = O\bigl((n\log p + \log(B_{\mathrm{leaf}}/\eps))/\delta^2\bigr)$, $N = r^2\lceil\log_2(8rT/\eps)\rceil$ (Theorem~\ref{thm:subspace-source}(ii) with $\beta = \eps/8$; $N = 0$ if $r = 1$), and $B_{\mathrm{leaf}}$ is the core's lifted-source count at error $\eps/4$; Theorem~\ref{thm:app-sub-hsp} gives the precision allocation.
```

**I2 (Imprecision; l. 1086, `thm:subspace-source`(ii)).**
Quote: "Put $B = \lceil \log_2(rT/\beta)\rceil$ and allow at most $N = r^2B$ growth attempts
per output, never resetting the clock."
Reason: For `r = 1` this gives `N = B > 0`, but no growth step exists. The appendix sets
`N = 0` (Prop. `app-sub-stream`), and `thm:app-sub-hsp`(ii) says "exactly $T$ if $r = 1$".
The main-text bound `T(N+1)` is valid but loose and inconsistent with the appendix.
Drop-in:
```latex
Put $B = \lceil \log_2(rT/\beta)\rceil$ and allow at most $N = r^2B$ growth attempts per output ($N = 0$ if $r = 1$, when no growth step is needed), never resetting the clock.
```

**I3 (Imprecision; l. 1128).**
Quote: "$\ell = 420400$ blocks (this $\ell$ comes from the artifact's generic transfer bound
and is larger than step~(3) requires)".
Reason: `rem:app-sub-profile` says `ℓ = 420400` is the parameter `⌈b/γ⌉` of
`thm:app-sub-hsp`, not an artifact-only bound. The real slack is in that proof:
`(1-γ)^ℓ ≤ e^{-b}` is then weakened to `2^{-b}`. Step (3) alone would already hold with
`⌈b ln2/γ⌉ = 291,384` blocks.
Drop-in:
```latex
$\ell = 420400$ blocks (this is $\ell = \lceil b/\gamma\rceil$ of Theorem~\ref{thm:app-sub-hsp}; its proof weakens $(1-\gamma)^\ell \le e^{-b}$ to $2^{-b}$, so step~(3) alone would allow about $\ell\ln 2$ blocks)
```

**I4 (Imprecision; l. 1128, and app `rem:app-sub-multiple-p` l. 351).**
Quote: "for $p \gg \ell$ the design is far cheaper."
Reason: The multiple-of-`p` route costs `cp⌈ℓ/p⌉ ≥ cp` states per source and the design
costs `Mℓ`. So the design is cheaper as soon as `p > Mℓ/c`. Without `M/c`, "`p ≫ ℓ`" is not
the right threshold, because `M` can be as large as `(c+1)!`.
Drop-in:
```latex
which at this profile gives $3{,}783{,}699$ exterior states per source. That route costs at least $cp$ exterior states per source and the design costs $M\ell$, so the design is cheaper as soon as $p > M\ell/c$.
```

**I5 (Imprecision; l. 1108 and app l. 284, `lem:app-sub-design`(a)).**
Quote: "the cyclic design of Lemma~\ref{lem:app-sub-design}(a) needs a Las Vegas search for a
generator".
Reason: A divisor `e > c` of `p-1` exists exactly when `p ≥ c+2`, since `e = p-1` works.
The case `e = p-1` is `S = F_p^×`, which needs no generator: `Σ_{s≠0} s^j = 0` for
`1 ≤ j ≤ p-2`. So (a) also gives a deterministic design, of size `p-1`. The statement as
written suggests that every cyclic design needs randomness.
Drop-in (app l. 284):
```latex
\item If $e \mid p-1$ and $e > c$, then the group $\mu_e$ of $e$-th roots of unity in $\Fp^\times$ is a design with $M = e$ distinct points. Such an $e$ exists exactly when $p \ge c+2$, and $e = p-1$ gives the design $S = \Fp^\times$ deterministically. For other $e$, a generator of $\mu_e$ is found by a Las Vegas search: for uniform $x \in \Fp^\times$, the element $y = x^{(p-1)/e}$ generates $\mu_e$ if and only if $y^{e/q} \ne 1$ for every prime $q \mid e$, which happens with probability $\varphi(e)/e$.
```
Drop-in (main l. 1108 parenthetical):
```latex
(Lemma~\ref{lem:app-sub-design}(b) constructs one deterministically, with $M \le (c+1)!$; for $p \ge c+2$, Lemma~\ref{lem:app-sub-design}(a) gives $S = \Fp^\times$ deterministically, and a smaller cyclic design needs a Las Vegas search for a generator)
```

**I6 (Imprecision; l. 1103, step (4)).**
Quote: "its label law is covered by the complete-instrument hybrid for any schedule that
consumes at most a fixed number of sources (Definition~\ref{def:app-sub-core})".
Reason: Definition `app-sub-core` is about Schedule 1 only. The sentence about other
schedules is the remark after it (app l. 105). That remark says "The argument never uses the
law of the labels", which is a different and clearer claim than "its label law is covered".
Drop-in:
```latex
  \item \emph{Hybrid.} A hybrid bound over the $B_{\mathrm{leaf}}$ lifted sources of the core replaces each by $\sigma$. The core's descent consumes only sources and public right actions, and never queries an oracle. The bound uses only that the core is a fixed instrument on a fixed number of sources, not the law of its labels, so it applies to any schedule with a deterministic cap on the sources consumed (the remark after Definition~\ref{def:app-sub-core}); Theorem~\ref{thm:app-sub-hsp} is stated for Schedule~1.
```

**I7 (Imprecision; app l. 417, `rem:app-sub-scope`).**
Quote: "\emph{Flatness} gives Lemma~\ref{lem:app-sub-growth}(a). For $\diag(3/4,1/4,0)$, the
swap of the first two basis vectors fixes the support but not the state."
Reason: The example shows that the support's stabilizer can be larger than the state's, so
the exterior state of the support has the wrong ray stabilizer. That concerns
`prop:app-sub-ray` and the identity `H = stab(V) = stab(ρ)`, not the
state-independent acceptance probability of Lemma `app-sub-growth`(a).
Drop-in:
```latex
  \item \emph{Flatness} gives Lemma~\ref{lem:app-sub-growth}(a) and the identity $H = \{g : R(g)V = V\} = \{g : R(g)\rho R(g)^\dagger = \rho\}$. For $\diag(3/4,1/4,0)$, the swap of the first two basis vectors fixes the support but not the state, so the exterior state of the support has a larger ray stabilizer than $\rho$.
```

**I8 (Imprecision; l. 1135 and l. 1022).**
Quotes: "This section was re-audited on 31 October."; "Both subsections were re-audited on 31
October."
Reason: Claim discipline. The audit was done by automated referees (STATE.md l. 200–204:
"re-audited by automated referees ... No human review"). As written, it can be read as a
human audit.
Drop-ins:
```latex
This section was re-audited by AI sessions on 31 October; no human has reviewed it.
```
```latex
Both subsections were re-audited by AI sessions on 31 October.
```

**I9 (Imprecision; l. 1197, `prop:classical-query`(iii)).**
Quote: "Under the further promise that $H$ is normal, the same holds with $p^{m-k}$ replaced
by $p^{z_k}$ when $z_k \coloneqq \dim Z(\mathcal{L}/\mathfrak{k}) \ge 2$."
Reason: "The same" also covers the preceding "hence
$q > \sqrt{2(1-\delta)\,|G|/|H|}$". With `p^{z_k}` that becomes `p^{z_k-1}`, which differs
from `|G|/|H| = p^{m-k-1}` when `z_k < m-k`. The proof gives only the binomial bound.
Drop-in:
```latex
Under the further promise that $H$ is normal, it still needs $\binom q2 \ge (1-\delta)(p^{z_k}-1)/(p-1) - 1$, hence $q > \sqrt{2(1-\delta)\,p^{z_k-1}}$, when $z_k \coloneqq \dim Z(\mathcal{L}/\mathfrak{k}) \ge 2$.
```

**I10 (Imprecision; l. 1316, Lean boundary).**
Quote: "$E_s$ maps the grades above $k$ onto $\gamma_{k+1}$".
Reason: Lean `ReesGeneralCover.evaluation_image_tail` assumes `hs : IsUnit s`. For `s = 0`
the image is `0`. The unconditional Lean fact (`evaluation_mem_gamma_of_tail`) is "into".
Drop-in:
```latex
$E_s$ maps the grades above $k$ into $\gamma_{k+1}$, and onto it when $s \ne 0$,
```

**I11 (Imprecision; l. 1316).**
Quote: "Conditionally on an explicit natural group-law hypothesis, which the Lazard
correspondence supplies for $c<p$".
Reason: The Lean general-class theorems take three separate hypotheses:
`NilpotentGroupLaw F c` (naturality, associativity, zero, inverse), `AdditiveOnCommuting law`
and `SubgroupsAreSubalgebras law`. README says "all three hypotheses". The singular form
hides the third one, the subgroup direction of Lazard. That one is the hard part at `c = 4, 5`
(42 and 8 guards).
Drop-in:
```latex
Conditionally on three explicit hypotheses that the Lazard correspondence supplies for $c<p$ (a natural nilpotent group law, additivity on commuting pairs, and the statement that every subgroup is a Lie subalgebra),
```

**I12 (Imprecision; l. 1308 and l. 1317, `ReesSdeTriangular`).**
Quote (l. 1308): "Proposition~\ref{prop:triangular-sde}: from a normalised contraction
$(\alpha,\beta)$ (a hypothesis), a nonzero solution among any $(a+1)(a+2)/2$ columns; algebra
only".
Reason: `triangular_sde_of_contraction` and `triangular_sde_zmod` assume
`hgen : ∀ y ≠ 0, ∃ n, g ^ n = y`, so `g` generates `K^×`. `prop:triangular-sde` allows any
coset generator `g` ("for κ = 2 any quadratic non-residue can serve as g"). The general case
reduces to the Lean case, because every generating coset of `P` contains a generator of
`F_p^×` and the hypothesis depends only on `gP`. That reduction is not formalized, so the
Lean statement is a special case of the proposition.
Drop-in (l. 1308, third column):
```latex
Proposition~\ref{prop:triangular-sde} with $g$ a generator of $\Fp^\times$: from a normalised contraction $(\alpha,\beta)$ (a hypothesis), a nonzero solution among any $(a+1)(a+2)/2$ columns; algebra only
```
Drop-in (l. 1317, end of the triangular clause):
```latex
the construction yields a nonzero solution from any $(a+1)(a+2)/2$ columns. Lean takes $g$ to generate $\Fp^\times$; the reduction from an arbitrary coset generator is not formalized.
```

**I13 (Imprecision; l. 1077, `thm:subspace-source`).**
Quote: "\begin{theorem}[Exterior-state source for flat subspace symmetry; proof in
Appendix~\ref{app:subspace}]".
Reason: Claim discipline. Every other proved result in scope carries its status in the title
(`prop:conjugation`, `prop:classical-query`: "AI-checked, pending human review";
`cor:subspace-hsp`: "proposed, conditional"; `rem:mixed-source`: "argued, AI-checked only").
This theorem's status is given only two paragraphs later.
Drop-in:
```latex
\begin{theorem}[Exterior-state source for flat subspace symmetry; AI-checked, pending human review; proof in Appendix~\ref{app:subspace}]
```

### Style

**S1 (Style; l. 1091).** Quote: "With $\gamma = \frac1r\sum_i \sin^2\theta_i \ge \delta^2$".
In step (3) and throughout the appendix, `γ = δ²/2`. The appendix calls this quantity `μ`.
Drop-in:
```latex
With $\mu = \frac1r\sum_i \sin^2\theta_i \ge \delta^2$, the AM--GM inequality gives $\prod_i\cos\theta_i \le (1-\mu)^{r/2} \le \sqrt{1-\delta^2} \le 1-\delta^2/2$.
```

**S2 (Style; app l. 383–400).** Quote: "Let $\mathsf{F}$ be the event that the output is not a
basis of $\hh$." The house style avoids `\mathsf`. Replace every `\mathsf{F}` in the proof of
`thm:app-sub-hsp` (l. 383, 385, 389, 393, 397, 400) by `\mathcal{E}`:
```latex
Let $\mathcal{E}$ be the event that the output is not a basis of $\hh$.
```

**S3 (Style; l. 1172–1225, notation clashes inside Section 8).** These are reused with a
different meaning from the subspace section next to them: `ρ` (collision parameter vs
density), `q` (queries vs qubits), `ℓ = ln(2/ε)` (vs blocks), `M = p^{m-k}` (vs design size),
`k` (ideal dimension, then `|H| = p^k`). The most confusing one is `ℓ`, which also appears in
the table caption. Drop-in for (v):
```latex
  \item Conversely, let $0<\eps<1$, $t = \lceil\log_p(2/\eps)\rceil$, $u = \ln(2/\eps)$ and
  \[
    Q = 5(m+t) + 16\lceil u\rceil + \Bigl\lceil\sqrt{2p^{m-1}\max(2t+2,\,8u)}\,\Bigr\rceil .
  \]
```
Then replace `\ell` by `u` in the proof of (v) and in the table caption
(`$8u = 8\ln 6 \approx 14.33$`, "with $8u$ itself"). For `lem:collision`, rename
`\rho` to `\tau`: "Put $\tau = \max_{g \in G\setminus K}\Pr_{H\sim\mu}[g\in H]$". Do the same
in the proof of `prop:classical-query`(i)–(iii).

**S4 (Style; l. 1230 caption and l. 1253).** Quotes: "with $r$ the number of subspaces of
$\Fp^m$"; "In the input length $n = m\log_2 p$ this is $2^{\Omega(n)}$". Here `r` is the
subspace rank and `n` the cover dimension elsewhere.
Drop-ins:
```latex
$\lceil 4\log_2(3N_{\mathrm{sub}})\rceil$, obtained from~\cite[Eq.~(10.10)]{ChildsQA} with fidelity at most $1/\sqrt2$ and error $1/3$, with $N_{\mathrm{sub}}$ the number of subspaces of $\Fp^m$
```
```latex
In the input length $L_{\mathrm{in}} = m\log_2 p$ this is $2^{\Omega(L_{\mathrm{in}})}$,
```
The same applies at l. 1160 (`$\ell = \sum_i u_i$`, use `$\ell_u$`) and l. 1165 (orbit rank
`$b^m$`, where `m` is not the Lie dimension; use `$b^{m'}$`).

**S5 (Style; l. 1135).** Quote: "The truncated series $\exp(\ad_x)$ is defined, since
$\ad_x^p = 0$". The reason `ad_x^p = 0` is not obvious (it needs characteristic `p`;
`2N-1 > p` in general).
Drop-in:
```latex
The truncated series $\exp(\ad_x)$ is defined, since $\ad_x^p = \ad_{x^p} = 0$ in characteristic $p$,
```

**S6 (Style; l. 1300–1301, 1316).** "($p>3$)" for the class-four subgroups and "($p>4$)" for
the points describe the same primes. Lean uses `NeZero 2, NeZero 3` and `hp : 4 < p`. Write
"($p \ge 5$)" in both places, and "($p \ge 7$)" for class five.

**S7 (Style; l. 1268, 1272, 1277, caption of `tab:lean-modules`).** The paper writes
`\file{Formal/Audit.lean}` (relative to `formal/`) next to `\file{formal/README.md}`
(relative to the repo root). Drop-in:
```latex
\file{formal/Formal/Audit.lean}
```

**S8 (Style; l. 1128, l. 1230, app l. 405, and 12 others).** Bare-name `\file` arguments
resolve only by searching the repo. See Section 4 for the full list. The in-scope drop-ins:
```latex
\file{research/reductions/rees_subspace_source.json}
```
```latex
\file{research/audits/reviews/2026-11-02-rees-classical-lower-bound/birthday_crossover.json}
```
Also `lem:collision` (l. 1172) has no status tag, unlike `prop:classical-query`. Optional:
`\begin{lemma}[Collision bound; standard, AI-checked]`.

## 3. Lean audit

**Escape hatches.** I grepped `formal/Formal/*.lean` and `formal/Formal.lean` for
`sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `implemented_by`, `unsafe` and `opaque`.
None appears as code. The only hits are the English word "admit" in three docstrings
(`ReesSdeTriangular.lean` l. 250, 315, 338; `ReesSdeWitness.lean` l. 95;
`BalancedSigned.lean` l. 205).

**Guards.** `Formal/Audit.lean` has 455 `#print axioms` guards under `#guard_msgs`. Every
printed list is a subset of `[propext, Classical.choice, Quot.sound]`: 426 print all three,
23 print `[propext, Quot.sound]` and 6 print `[propext]`. I mapped each guarded constant to
its defining module with `Lean.Environment.getModuleIdxFor?`; the script is in the
scratchpad, not the repo. Every per-module count in `tab:lean-modules` is exact, and the total
is 417. The other 38 guards cover modules unrelated to this paper: `BalancedSigned` 9,
`CycleIndicator` 8, `FieldThreshold` 7, `CrossCheck` 4, `PermTrace` 4, `CoeffList` 3,
`StdRepExterior` 3. The grand total is 455, as stated. The class-five modules have
8 + 8 + 5 = 21 guards, as stated.

**Build (today).** In `formal/` I ran three builds, all with exit 0:
- `~/.elan/bin/lake build Formal.Audit`: "Build completed successfully (3490 jobs)", 6.7 s.
- `lake build --wfail Formal.Audit`: same result.
- `lake build --wfail` of the whole project: "Build completed successfully (3514 jobs)".

All jobs were replayed from the existing `.lake` cache. Lake re-hashes sources, so the cached
results correspond to the current (modified) working-tree sources. This was not a clean
build, and no warning was emitted. The only message was `info: Formal/CrossCheck.lean:90:0: true`.
Toolchain `leanprover/lean4:v4.35.0`; Mathlib `v4.35.0`, rev `56a0058`, as stated.

**Statements against the paper.**
- `ReesGeneralCover`: holds for any commutative ring `R`.
  - Class transfer: `rees_class_exact`.
  - Central top grade: `top_grade_central`.
  - `E_s∘δ_u = E_{us}`: `evaluation_comp_dilation`.
  - Tail into `γ_{d+1}` (`evaluation_mem_gamma_of_tail`), and onto it for a unit `s`
    (`evaluation_image_tail`; see I10).
  - `h̃ = ⊕ t^r(h∩γ_r)` (`mem_hiddenCover_iff_graded`) `= ∩_s E_s^{-1}(h)`
    (`mem_hiddenCover_iff_forall_eval`), independent of admissible points (`hiddenCover_eq`).
  - Over a field, any `c` distinct nonzero points are admissible (`field_points_isUnit`).
  - Matches l. 1290 and 1316.
- `BCHClassFive.bch` matches the standard BCH series through degree 5, including the
  `1/720`, `1/360` and `1/120` terms. Hypotheses: `NeZero 2, 3, 5` over any field, and
  `lowerCentralSeries F L L 5 = ⊥`, which in Mathlib indexing means class at most 5. Matches
  l. 1316 ("over any field in which 2, 3 and 5 are invertible").
- `BCHClassFiveSubgroups.toLieSubalgebra` works over `ZMod p` with `NeZero 2, 3, 5`, that is
  `p > 5`. Matches.
- `ReesGeneralLawClassFive`:
  - `classFive_tuple_hides_coeff` (`hp : 5 < p`, arbitrary `H`, points `1..5`).
  - `classFive_terminal_source`.
  - `classFive_measured_terminal_source`, which takes the `policy`, `active` and `sde`
    hypotheses as inputs and starts from the exact top coset source.
  - These match "tuple hiding theorem and the measured terminal source hold for an arbitrary
    subgroup H at the points 1,…,5" and "their other stated inputs, such as the SDE
    policies, remain".
  - Note: the `active ∧ sde` policy hypothesis quantifies over all label tuples. It is
    satisfiable by `ReesSdeWitness.exists_witness_gcd` once `|I d| ≥ gcd(d+1,p-1)·dim γ_{d+1} + 1`,
    but that link is not formalized. The paper says so: "wiring of SDE witnesses ... outside".
- `ReesGeneralLawClassFour` and `ReesGeneralMeasuredReceiver.classFour_measured_terminal_source`:
  `NeZero 2, 3` and `hp : 4 < p`. Match (S6).
- `ReesSdeGcd`: `range_pow_units_eq` is `lem:app-s2-gcd`(a), and `pow_bezout_exponent` with
  `bezout_witness` is (b). `ReesSdeWitness.exists_witness_gcd` gives `gcd(d,p-1)·a < M`
  columns, and `exists_witness_linear` is (c), existence only. Match. `ReesSdeTriangular`:
  see I12.
- `ReesPrimePowerInterpolation`: `evaluation_det_unit` (`c < p`, modulo `p^e`) and the
  `ZMod 9` counterexample `bad_points_*`. Match.
- No Lean module formalizes anything in `appendix-subspace.tex`, and the paper claims none.
  `StdRepExterior` is unrelated.
- README is stale for class five (E1, G2).
- `Formal.lean` imports every module except `PlantedMISPairClosure`, which is unrelated and
  not in the table.

No claim in the scope is stronger than its Lean statement, apart from I10, I11 and I12.

## 4. `\file{...}` paths: whole paper

Script: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/check_files.py`
(full TSV in `files.tsv` next to it). It extracts every `\file{...}` from every `.tex` under
`docs/papers/rees-hsp/`, including `core/`, `archive/` and `main-full-draft.tex`. It resolves
each argument against the repo root, the paper directory and `formal/`, and otherwise searches
for a unique repo path ending in the argument. Core logic:

```python
for m in re.finditer(r"\\file\{([^{}]*)\}", line): hits.append((lineno, m.group(1)))
for base in (REPO, PAPER, REPO + "/formal"):
    if os.path.exists(os.path.join(base, arg)): status = "exact"
# else: unique repo path ending with "/" + arg  -> "by-suffix", otherwise "MISSING"
```

Results: 333 citations in all .tex files: 281 exact, 51 by-suffix, 1 missing.
- **Paper proper** (`main.tex` + the six input appendices): 189 citations, 131 distinct.
  167 resolve exactly and 22 only by suffix. **None is missing.**
- **Missing (whole tree):** `core/main-core.tex` l. 694, `docs/papers/rees-hsp/appendix-*.tex`.
  This is a glob, not a path. Matching files exist, but `\nolinkurl` will print the glob
  literally.
- **Bare names in the paper proper** (each resolves to exactly one file):
  - `rees_nongradable_control.json`, `rees_complete_instrument.json`, `power_sde.json`,
    `rees_full_grade_budget.json` (×2), `rees_uniform_instrument.json` (×2),
    `random_column_rees.json` (×2), `rees_hsp_reduction.json` (×3),
    `ring_to_field_rank_reduction.json` (×2), `rees_subspace_source.json` (main l. 1128 and
    app l. 405) → all in `research/reductions/`.
  - `birthday_crossover.json` (l. 1230) → `research/audits/reviews/2026-11-02-rees-classical-lower-bound/`.
  - `dfs2b_k9_rerun_low.out` (`appendix-schedule2.tex` l. 470) → `research/audits/reviews/2026-11-02-rees-schedules/small-prime/`.
  - `filiform_check.py`, `reduction_check.py`, `group_check.py`, `section6_bounds.py`
    (`appendix-codimension.tex` l. 327) → `research/audits/reviews/2026-11-02-rees-codimension/`.
  - `make_numbers.py`, `numbers.tex` and `main.tex` resolve relative to the paper directory.
  - `Formal/Audit.lean` resolves relative to `formal/` (S7).
- Every path cited in the scoped sections exists. This includes all 7 review reports of the
  Lean section, `theorems/rees_mixed_source_sim.py`, `research/REES_MIXED_SPECTRAL_SOURCE.md`,
  the six filter notes and `tests/test_rees_single_evaluation_falsifier.py`.

## 5. Claim discipline

- **Present:**
  - "AI-checked, pending human review" on `prop:conjugation` and `prop:classical-query`.
  - "proposed, conditional" on `cor:subspace-hsp`.
  - "argued, AI-checked only" on `rem:mixed-source`.
  - "conditional on the cited notes" on `rem:filters`.
  - "conditional on Theorem~\ref{thm:main}" on `rem:query-separation`.
  - "Proofs checked by AI sessions, pending human review" heading the subspace appendix.
  - "These checks are AI-run and pending human review" in the Lean section.
  - "no human has read it" and "nothing here has had human review" in the subspace text.
- **Missing or weak:** I13 (`thm:subspace-source` title) and I8 ("re-audited", agent not
  named).
- **No novelty claim** in scope. `rem:query-separation`(a) says the separation "is not new".
- **No speedup claim**: "We claim no speedup for any concrete problem"; "Failing one filter
  is not evidence of hardness. No application of the Rees composition is known." The
  artifact also sets `speedup_claim_allowed: false` and `novelty_established: false`.
- **No human-review claim** anywhere in scope.

## Applied (11-04)

Applied by one AI session (Claude Code), local only: no git, no network, no `.lean`
edits, no claim-gate changes. Backups of the edited files are in the session
scratchpad (`bak-i185/`). Edits were exact-string replacements, each asserted to
match once, with a check that the file had not changed between read and write.
Another agent was editing "Parameterized Regimes" and several appendices at the
same time; its edits are kept.

Counts: 24 findings. Applied 19, modified 5 (G1, I8, I10, S4, S8), skipped 0. Within
S8, 6 of the 22 bare names were skipped, see below.

- **E1** applied (`formal/README.md`): the "No group law ... `c ≥ 5`" sentence now
  names the three class-five modules and says no law is constructed for `c ≥ 6`.
- **G1** modified. Integrator wording instead of the referee's: main (ii) now says
  "A streaming antisymmetrization instrument, following Bene Watts et al., with the
  recovery step on rejection added here (Lemma app-sub-lcu)". The proof sentence
  "Rejection must apply ..." now reads "On rejection, the procedure applies ... (the
  recovery step of Lemma app-sub-lcu)". The appendix says "This follows the growth
  measurement of [Algorithms 1--2], with the recovery W† on rejection added here; ...
  whether or not [BeneWatts2026] states that recovery step." `% NEEDS HUMAN
  VERIFICATION` comments are in both places. For consistency,
  `rem:mixed-source`(ii) now adds "with the recovery step of Lemma app-sub-lcu".
- **G2** applied (README): three rows after `ReesGeneralMeasuredReceiver`, plus a short
  note under the section intro. Module names, theorem names (`bchLaw`,
  `bchLaw_additive`, `bchLaw_subgroups`, `toLieSubalgebra`,
  `classFive_tuple_hides_coeff`, `classFive_terminal_source`,
  `classFive_measured_terminal_source`) and guard counts 8/8/5 were checked by grep in
  `formal/Formal/` and `Formal/Audit.lean`.
- **I1** applied, with a further clause: the gate count is "plus `rT` times the gate
  cost of one controlled-R call at precision `ε/(16rT)`".
- **I2** applied.
- **I3** applied.
- **I4** applied in main and in `rem:app-sub-multiple-p` (appendix wording: "...as soon
  as `p > Mℓ/c`, in particular for `p` of cryptographic size").
- **I5** applied in main and appendix.
- **I6** applied.
- **I7** applied.
- **I8** modified: the wording is "re-audited by AI referees on 31 October; no human
  has reviewed it/them" (integrator: "AI referees"), at both l. 1022 and l. 1135.
- **I9** applied after an independent check of the proof of (iii). The normal-case
  measure is uniform on the `(p^{z_k}-1)/(p-1)` normal choices, with `τ = π` equal to
  one over that number. So Lemma collision(i) gives only
  `C(q,2) ≥ (1-δ)(p^{z_k}-1)/(p-1) - 1`, and the arithmetic of (i) gives
  `q > sqrt(2(1-δ)p^{z_k-1})`. This is not `sqrt(2(1-δ)|G|/|H|) = sqrt(2(1-δ)p^{m-k-1})`
  unless `z_k = m-k`. The referee is right. The statement now gives the binomial bound
  and `q > sqrt(2(1-δ)p^{z_k-1})`. The proof now says so, and notes that the bound is
  weaker when `z_k < m-k`.
- **I10** modified: "into `γ_{k+1}`, and onto it when `s` is a unit (over F_p, when
  `s ≠ 0`)". This matches Lean `IsUnit s` over a general commutative ring.
- **I11** applied, and "remain conditional on it" became "on them".
- **I12** applied (table row and l. 1317).
- **I13** applied.
- **S1** applied (`γ → μ` in the proof of `thm:subspace-source`).
- **S2** applied: 9 occurrences of `\mathsf{F}` became `\mathcal{E}`.
- **S3** applied. `ρ → τ` in `lem:collision` and the proof of (i)--(iii), 9
  occurrences. `ℓ → u` in (v) and its proof, 9 occurrences, and in the table caption.
- **S4** modified. Applied: `N_sub` in the caption, `L_in` in `rem:query-separation`
  and `ℓ_u` at l. 1160. At l. 1165, `b^m` became `b^{m'}` with the definition "for `m'`
  blocks of `UT_b(F_p)`", taken from `MOORE_GRADIENT_CLASSICAL_FILTER.md` §7. A bare
  `m'` would have been undefined.
- **S5** applied.
- **S6** applied (table and l. 1316): class four `p ≥ 5`, class five `p ≥ 7`.
- **S7** applied: 4 occurrences in Section 9 became `formal/Formal/Audit.lean`.
- **S8** modified, partly skipped.
  - Applied: 16 of the 22 bare `\file{}` names were replaced by full repo-relative
    paths. That is 14 in `main.tex` outside "Parameterized Regimes", 1 in
    `appendix-subspace.tex` and 1 in `appendix-schedule2.tex`. Each path was checked
    with `ls`.
  - Skipped: 6 names in regions reserved for the other agent. These are
    `ring_to_field_rank_reduction.json` ×2 in "Parameterized Regimes" and the 4 scripts
    in `appendix-codimension.tex` l. 327. They still resolve by suffix (not missing).
  - Applied: the `lem:collision` label, as "Collision bound; AI-checked, pending human
    review". "standard argument" was dropped because the longer title caused an
    overfull line.
  - `core/main-core.tex` is untouched.

Build (scratchpad copy, `latexmk -g -pdf`): 148 pages, no "Float too large", no
undefined references or citations. Two Overfull hboxes remain: 7.1 pt at
`thm:random-column` (main l. 690) and 19.9 pt at `cor:codim` (main l. 974). Both
come from title changes the other agent made during this pass. Neither is in this
pass's regions, so this pass left them alone. `tests/tools/test_rees_paper_numbers.py`:
2 passed. Path checker (`check_files.py`, unchanged) for `main.tex` and the
appendices: 191 citations, 185 exact, 6 by-suffix (the skipped ones), 0 missing.
