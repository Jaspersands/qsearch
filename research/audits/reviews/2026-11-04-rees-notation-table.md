# Rees HSP paper: notation table (referee item m1), 2026-11-04

Scope: `docs/papers/rees-hsp/main.tex` and `appendix-{schedule2,schedule3,free-coordinate,subspace,torsion-blackbox,codimension}.tex`.
Line numbers are those of the files on disk on 2026-11-04. No `.tex` file was edited. Every `\ref` label in the block below was
checked against `\label{...}` in those seven files (see "Verification" at the end).

## 1. Proposed LaTeX block

Uses only packages and macros already in the preamble (`booktabs`, `array`, `\Fp`, `\A`, `\hh`, `\hlift`, `\eps`, `\codim`).
Three small tables, each short enough to sit on one page at `\small`. Column widths total 15.9 cm; `\textwidth` is 16.5 cm.

```latex
\subsection{Notation}
\label{sec:notation}

Tables~\ref{tab:notation-instance}--\ref{tab:notation-bb} list the symbols that occur in more than one section, with the place
where each is defined. The last column gives a label, not a page. A letter that is reused with a different meaning inside a
single proof or appendix is redefined there. The tables give the global meaning only.

\begingroup\small
\renewcommand{\arraystretch}{1.08}

\begin{table}[htbp]
\centering
\caption{Notation, part 1: the instance, the Rees cover and the recursion.}
\label{tab:notation-instance}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.5cm}>{\raggedright\arraybackslash}p{8.6cm}>{\raggedright\arraybackslash}p{4.8cm}@{}}
\toprule
\textbf{Symbol} & \textbf{Meaning} & \textbf{Defined in} \\
\midrule
$p$ & prime, $p > c$ & Def.~\ref{def:input-contract} \\
$c$ & nilpotency class of $\mathcal{L}$, $c < p$ & Def.~\ref{def:input-contract} \\
$m$ & $\dim_{\Fp}\mathcal{L}$ & Def.~\ref{def:input-contract} \\
$\mathcal{L}$, $G$ & Lazard Lie algebra; the group $(\mathcal{L},\ast)$ with the truncated BCH product & Def.~\ref{def:input-contract} \\
$H$, $\hh$ & hidden subgroup; $\hh = \log H$, an $\Fp$-Lie subalgebra & Def.~\ref{def:input-contract} \\
$f$, $w$ & hiding function $G \to \{0,1\}^w$; label width & Thm.~\ref{thm:main} \\
$\eps$ & allowed failure probability & Thm.~\ref{thm:main} \\
$Q$ & number of oracle queries (or copies of $\rho_H$) of Theorem~\ref{thm:main} & Thm.~\ref{thm:main} \\
$\rho_H$ & mixed coset state $|G|^{-1}\sum_{h\in H}R_h$ & Sec.~\ref{sec:intro} \\
$\gamma_k(\mathcal{L})$, $g_k$ & lower central series; $g_k = \dim_{\Fp}\gamma_k(\mathcal{L})$, $g_1 = m$ & Sec.~\ref{sec:intro}; $g_d$: Thm.~\ref{thm:main} \\
$r$ & $g_2 = \dim_{\Fp}[\mathcal{L},\mathcal{L}]$ & Sec.~\ref{sec:intro}; Cor.~\ref{cor:fpt-r} \\
$\A$, $n$ & positive Rees cover $\bigoplus_{k=1}^c t^k\gamma_k(\mathcal{L})$; $n = \dim\A \le cm$ & Thm.~\ref{thm:rees-cover} \\
$t$ & formal variable of $\mathcal{L}[t]$ (Rees grading) & Thm.~\ref{thm:rees-cover} \\
$E_s$, $\delta_\lambda$ & evaluation homomorphism $\A \to \mathcal{L}$; dilation automorphism of $\A$ & Thm.~\ref{thm:rees-cover} \\
$\hlift$ & $\bigoplus_k t^k(\hh \cap \gamma_k(\mathcal{L}))$, the homogeneous hidden subalgebra of $\A$ & Lem.~\ref{lem:homogeneous} \\
$Z$, $K$ & central elementary abelian subgroup; $K = H \cap Z$ & Sec.~\ref{sec:instrument} \\
$\lambda$ (label) & character of $Z$ measured by the central instrument & Lem.~\ref{lem:central} \\
$G_d$, $Z_d$ & stage-$d$ quotient $\A/\bigoplus_{k>d}\A_k$ and its central top grade, of rank $g_d$ & Sec.~\ref{sec:recursion} \\
$H_d$, $K_d$ & homogeneous hidden image in $G_d$; its central intersection $t^d(\hh\cap\gamma_d(\mathcal{L}))$ & Sec.~\ref{sec:recursion} \\
$a_d$ & label rank $\dim K_d^\perp \le g_d$ & Sec.~\ref{sec:recursion} \\
$M_d$ & arity (number of sources merged) at grade $d$ & Thm.~\ref{thm:main} \\
$P$ & $\prod_{d=2}^c M_d$, lifted sources per terminal sample & Sec.~\ref{sec:recursion} \\
$S$ & $m + \lceil\log_p(3/\eps)\rceil$, number of terminal samples & Sec.~\ref{sec:recursion} \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[htbp]
\centering
\caption{Notation, part 2: the diagonal-equation (SDE) schedules.}
\label{tab:notation-sde}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.5cm}>{\raggedright\arraybackslash}p{8.6cm}>{\raggedright\arraybackslash}p{4.8cm}@{}}
\toprule
\textbf{Symbol} & \textbf{Meaning} & \textbf{Defined in} \\
\midrule
$\kappa_d$ & $\gcd(d,p-1)$ & before Tab.~\ref{tab:main-regimes} \\
$B_d(a)$, $G(d,a)$ & Ivanyos--Santha arity for $a$ equations of degree $d$ (Schedule~1) & Thm.~\ref{thm:is-import}; Eq.~\eqref{eq:is-arity} \\
$h$ & $(p-1)/\kappa_d$, the order of the group of nonzero $d$-th powers & Sec.~\ref{app:s2-gcd}; Thm.~\ref{thm:random-column} \\
$Q_0$, $Q_m$, $\xi$, $z_m$ & subgroup of $\kappa$-th powers, its cosets, coset generator, $z_m = \xi^m$ & Sec.~\ref{app:s2-gcd} \\
$W$ & $\{w \in \Fp^\kappa : \sum_m z_mw_m = 0\}$ & Sec.~\ref{app:s2-tensor} \\
$M_d^{\mathrm{sym}}$ & two-level arity $(a+1)((\kappa-1)a+1)$ & Eq.~\eqref{eq:power-arity} \\
$E_2(\kappa)$ & primes without a universal decoupled two-level contraction & Prop.~\ref{prop:decoupled-sde} \\
$T_S(\kappa)$, $T_A(\kappa)$ & thresholds from a second-moment bound: $p > T_A(\kappa)$ gives $p \notin E_2(\kappa)$; $p > T_S(\kappa)$ gives the stated sampling cost & Sec.~\ref{app:s2-TA}; Prop.~\ref{prop:app-s2-TA} \\
$u$ & public integer, $c \le u$, $a_d \le u-1$, $p \ge 16u^2$ (Schedule~3) & Thm.~\ref{thm:random-column} \\
$P_\kappa$, $D$, $q$ & nonzero $\kappa$-th powers; $D = P_\kappa \cup \{0\}$; $q = (h+1)/p$ & Sec.~\ref{app:fc-setting} \\
$n_0$ & least number of columns after the last pivot; a node aborts below it & Thm.~\ref{thm:free-coordinate} \\
$\beta(M,n_0;a)$ & bank-failure bound of the free-coordinate sampler & Eq.~\eqref{eq:fc-beta} \\
$\tau_d$ & per-node failure budget $\eps/(9(c-1)Sn_d)$ & Thm.~\ref{thm:free-coordinate}(iii) \\
$n_d$ & $\prod_{2 \le d' < d} M_{d'}$, number of grade-$d$ nodes in one tree & Thm.~\ref{thm:free-coordinate}(iii) \\
$B$ & cap exponent: each random step fails with probability $\le 2^{-B}$ & Thm.~\ref{thm:free-coordinate}(iii); Sec.~\ref{app:s3-setting} \\
$\Gamma_0$, $\Gamma_1$, $\Gamma_{\mathrm F}$ & grades with $\kappa_d = p-1 \ge 2$; $\kappa_d = 1$; $2 \le \kappa_d < p-1$ & Sec.~\ref{app:fc-mixed} \\
$\Gamma_2$, $\Gamma_3$ & grades run by the Schedule-2 and Schedule-3 node types & Sec.~\ref{app:s3-mixed} \\
$N_{\mathrm{instr}}$ & number of approximated instruments in one run & Sec.~\ref{sec:recursion} \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[htbp]
\centering
\caption{Notation, part 3: parameterized regimes, black-box groups and subspace sources.}
\label{tab:notation-bb}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.5cm}>{\raggedright\arraybackslash}p{8.6cm}>{\raggedright\arraybackslash}p{4.8cm}@{}}
\toprule
\textbf{Symbol} & \textbf{Meaning} & \textbf{Defined in} \\
\midrule
$k$ & bound on $\codim_{\Fp}\hh$ & Cor.~\ref{cor:codim} \\
$R$ & cyclic rank $\dim_{\Fp}([\mathcal{L},\mathcal{L}]/p[\mathcal{L},\mathcal{L}])$ of the derived ring & Thm.~\ref{thm:ring-to-field} \\
$b$ & $\sum_i e_i = \log_p|G|$ for a ring $\bigoplus_i\mathbb{Z}/p^{e_i}$ & Sec.~\ref{sec:ring} \\
$\Omega_1(G)$, $H_1$ & elements of order dividing $p$; $H \cap \Omega_1(G)$ & Thm.~\ref{thm:ring-to-field} \\
$Q_f$, $T_f$ & number of queries to $f$; internal cost of one query & Sec.~\ref{sec:ring} \\
$s$, $g_1,\dots,g_s$ & number and list of black-box generators & Sec.~\ref{sec:black-box-groups} \\
$F_{s,c}$, $\Phi$, $d$ & free class-$c$ nilpotent Lie ring on $s$ generators; BCH map $F_{s,c} \to G$; $d = \rank F_{s,c}$ & Prop.~\ref{prop:black-box} \\
$A_c$, $k$ & $m_+ + 2b_Mq_+$, cost of one Lazard addition in group multiplications; number of samples in the kernel step & Prop.~\ref{prop:black-box}(iv) \\
$\ell$ & encoding length of the black-box group & Thm.~\ref{thm:bb-envelope} \\
$N$ & input size $s\ell + w + \log(1/\eps)$ of Theorem~\ref{thm:bb-envelope} & Thm.~\ref{thm:bb-envelope} \\
$n_p$, $e_p$, $M$, $b_M$ & $\log_p|G_p|$; $p^{e_p} = \exp G_p$; $M = p^{e_p}$; $\lceil\log_2 M\rceil$ & Thm.~\ref{thm:bb-envelope} \\
$L$, $t$, $K_c$ & $\sum_{p>c}n_p$; $\lceil\log_2(12\ell/\eps)\rceil$; $\prod_{d=2}^c d^{d(d-1)\lceil\log_2(d+1)\rceil/2}$ & Thm.~\ref{thm:bb-envelope} \\
$E_W(c)$, $e_d(p)$ & query exponent $\max_{p>c}(1 + \sum_{d=2}^c e_d(p))$; per-grade exponent of the combined rule & Thm.~\ref{thm:bb-envelope} \\
$V$, $\Omega_V$, $\delta$ & promised $r$-dimensional subspace; its top exterior power; gap promise & Thm.~\ref{thm:subspace-source}; Sec.~\ref{sec:subspace} \\
$B_{\mathrm{leaf}}$ & number of lifted sources the core consumes in the subspace reduction & Def.~\ref{def:app-sub-core} \\
\bottomrule
\end{tabular}
\end{table}
\endgroup
```

Notes on the block:

* `$k$` appears twice in Table 3 (codimension bound; kernel-step sample count) on purpose, because that is what the paper does
  (see collision C17). If the collisions of Section 3 are fixed first, drop the second row.
* The sentence "A letter that is reused ... is redefined there" is true only after the collisions below are fixed or each is
  locally redefined. Several are not (C1, C6, C12). Either fix those or soften the sentence.
* `Def.~\ref{def:app-sub-core}` and the `Sec.~\ref{app:...}` rows point into appendices. The body does the same in Remark
  `rem:two-level-threshold-size` and Schedule 2 "Terms", so no new forward-reference style is introduced.
* `\ref{app:...}` labels are on `\subsection`/`\section`, so `Sec.~` is the right prefix. `Sec.~\ref{sec:intro}` for `\rho_H`
  and for `\gamma_k, g_k, r` is correct because both are defined in unlabeled subsections of Section 1.
* `\ref{tab:main-regimes}` is used only to say where `\kappa_d` is defined (the paragraph just before the table). There is no
  label on that paragraph.

## 2. Where to insert it

Insert the block as a new `\subsection{Notation}` (label `sec:notation`) at the end of Section 1, immediately after the
"Organization" paragraph, which ends at `main.tex:234` ("... pending human review."), and before the `%====` rule at
`main.tex:236` that opens `\section{The Positive Lower-Central Rees Cover ...}` (`sec:rees-cover`).

Reasons: the tables contain `\kappa_d`, `B_d`, `M_d`, `a_d`, `u`, `\tau_d`, which Table `tab:main-regimes` (`main.tex:203-229`)
already uses before they are defined. A notation table at the end of Section 1 is the first place a reader who stops at the table
can find them. Putting it before Table `tab:main-regimes` would split the sentence "Table~\ref{tab:main-regimes} summarizes
the regimes" (`main.tex:188`) from its table.

Two one-line edits to go with it (not made):

* append to the Organization paragraph: "Section~\ref{sec:notation} collects the notation.";
* in the table caption of `tab:main-regimes` (`main.tex:202`), add "Symbols are listed in Tables~\ref{tab:notation-instance}--\ref{tab:notation-bb}."

The unused macro `\phis` (`main.tex:45`) has no occurrence outside its definition and could be removed. Not part of m1.

## 3. Collisions (one letter, two or more meanings)

Each entry gives the meanings with `file:line` (first occurrence of that meaning). `m` = `main.tex`, `s2` = `appendix-schedule2.tex`,
`s3` = `appendix-schedule3.tex`, `fc` = `appendix-free-coordinate.tex`, `sub` = `appendix-subspace.tex`, `tb` = `appendix-torsion-blackbox.tex`,
`cd` = `appendix-codimension.tex`. "Hard" means two meanings occur in the same section or proof chain, so a reader can mix them up
within one argument. "Soft" means the meanings live in different sections and are each locally defined.

### Hard (fix these)

C1. **`N`** (hard; 9 meanings). m:258 BCH degree `N <= c`; m:446 number of channels `Phi_1..Phi_N` in Lemma `lem:hybrid`;
   m:579 and fc:203 number of sampler nodes (`B = ceil(log2(27N/eps))`); m:618 odd modulus of `QFT_N` (`lem:qft-mod`);
   m:791 normalizer `N = N_G(H_1)`; m:837 and tb:1246 black-box input size `N = s*ell + w + log(1/eps)`; m:864 growth attempts `N = r^2 B`;
   s3:63 `N(Lambda) = |ker Lambda cap S|`; m:202 (Table `tab:main-regimes` caption) uses `N` for both the raw-copy count `N+1` (subspace row, from m:864) and the
   black-box input size, in one caption. Suggested: keep `N` for the black-box input size only; rename the others (`N_sol`, `J` for the channel count, `n_*` for the node count, `N_mod` for the QFT modulus).

C2. **`ell`** (hard; 8 meanings). m:202 and m:874 number of design blocks (sub:80); m:830 and m:822 encoding length;
   m:977 `ell = ln(2/eps)` (classical lower bound); m:938 `ell = sum_i u_i` (orbit-sum family); s3:66 bit count `ceil(log2 p)`;
   s2:116 prime divisor of `kappa`; s2:198 number of points `r_1..r_ell` in the Weil-count lemma; sub:310 index of `Lambda_{S,ell}`.
   The caption of Table `tab:main-regimes` (m:202) uses `M ell` (blocks) and, a few lines later in the same caption, `N` (whose definition in Theorem `thm:bb-envelope` contains the encoding length `ell`).

C3. **`t`** (hard; 6 meanings). m:249 Rees variable `t` (`t^k gamma_k`); m:436 and fc:202 `t = ceil(log_p(3/eps))` (Section 4 uses both within ten lines: `Z_d = t^d gamma_d` at m:428 and `t = ...` at m:436); m:489 `t <= kappa_d+1` (length of a zero sum); s2:103 Bezout exponent `t d' = 1 mod q'`;
   s3:56 (`if t^kappa = y`, Bezout root); m:830 `t = ceil(log2(12 ell/eps))`; m:620 `t = ceil(log2(36N/eta^2))` in the QFT lemma.

C4. **`beta`** (hard; 6 meanings). m:493, m:527, s2:173 contraction vector `(alpha,beta)`; m:575, fc:57 bank-failure bound `beta(M,n_0;a)`;
   fc:54 `beta = alpha'` (Bezout coefficient), three lines above the definition of `beta(M,n_0;a)` at fc:57; m:641 rotation angle `R(beta)`;
   m:864 and sub:261 timeout probability `beta`; m:897 failure level `beta` with `M_0 >= 8 rbar/beta`.
   Related: `alpha` is a contraction vector (m:493), a Bezout exponent (fc:54, s3:58) and a numeric constant `alpha = (1+2 log2 c) r + ...` (m:750).

C5. **`H_1`** (hard; 2 meanings, both for a hidden-subgroup object). m:790 `H_1 = H cap Omega_1(G)` (Theorem `thm:ring-to-field`);
   fc:266 and s3:46 `H_1 = t*hh`, the homogeneous hidden subgroup at grade 1 of the recursion. Theorem `thm:ring-to-field`(ii) hands `H_1` (first meaning) to the Rees composition, whose own grade-1 hidden group is `H_1` (second meaning).

C6. **`u`** (hard in the appendices; 8 meanings). m:557 public bound (Schedule 3); m:285 the element `u = s t z - t^2 z` in `lem:homogeneous`;
   s2:103 vector `u in F_p^M`; s2:160 exponent in a coset generator `xi^u q`; tb:109 Lie element `u in T_Q`; tb:709 digits `u_j` of an exponent;
   sub:180 element `u in k` (Lie algebra); m:938 `u_i` (orbit-sum variables); m:857 `u_1..u_r` orthonormal frame. Also `u_d` (s3:353, per-grade bound) and `u_Delta` (s2:410).
  

C7. **`Q`** (hard; 6 meanings). m:181 oracle queries `Q = c(m+...)prod B_d`; m:399 quotient `Q = G/Z`;
   s3:75 `Q = G_d/Z_d`; fc:285 and fc:437 `Q = c S prod M_d` queries; m:493 and s2:96 `Q_0, Q_m` cosets; m:781 `Q_f` queries to `f`;
   m:897 `Q_1,...` thresholds in the subspace design. The quotient `Q` (m:399) and the query count `Q` of the theorem it is used to prove (m:181) meet in the proof of Theorem `thm:main`. The task brief lists `Q_j`; the paper has no `Q_j`, only `Q_0` and `Q_m` (index `m in Z/kappa`).

C8. **`h`** (hard). m:114 and m:359 element `h in H`; m:493, m:559, fc:44, s2:96 `h = (p-1)/kappa`. `h in H` and `h = (p-1)/kappa` are both in Section 4 (m:411 `delta_{s_i}(h)`; m:493, Schedule 2 "Terms").

C9. **`q`** (hard). m:399 and m:411 element of the quotient `q in Q`; m:567, fc:46 `q = (h+1)/p`; s2:103 `q'` (`p-1 = kappa q'`);
   cd:180 `q, q'` elements of `s/k`; m:819 `q_+, q_{[ ]}`, power counts. m:399 and m:567 are in the same Section 4.

C10. **`P` and `P_kappa`** (hard). m:438 `P = prod M_d` (lifted sources per terminal sample); m:527 `P = (F_p^x)^kappa` (nonzero kappa-th powers, triangular solver);
    m:567 and fc:46 `P_kappa = {x^kappa}` (excluding 0) and `D = P_kappa cup {0}`; **s3:52 `P_kappa = {0} cup {x^kappa}` (including 0)**.
    fc:48 already notes the s3/fc discrepancy ("Appendix s3 writes `P_kappa` for the set called `D` here"), so it is known but not fixed. fc:204 uses `P = prod M_d` in the appendix whose setting (fc:46) defines `P_kappa`.

C11. **`K`** (hard). m:349 `K = H cap Z`; m:432 `K = <exp b_1,...,exp b_k>` (generated subgroup; four lines after `K_d` at m:428); m:897 `Q_1..Q_K` thresholds (number `K`);
    m:768 `K = hh cap I`; s3:68 and s3:181 `K = 4 kappa^M B` (trial count); m:830 `K_c` constant; m:791 `S/K` quotient section.
    `K_d` (central intersection at stage d) and `K` (group generated by a basis of `hh`) sit in one paragraph (m:428-432).

C12. **`L`** (hard). m:573 and fc:54 `L = M - n_0`; m:830 and tb:1101 `L = sum_{p>c} n_p`; s3:68 `L = max(1, ceil(log2 kappa))`; m:617 `L = log2(1/eta)` (QFT lemma).
    fc:70 renames the s3 quantity to `L_kappa` (and `R` to `R'`) to avoid the clash with its own `L = M - n_0`, so s3 and fc disagree on the name of the same quantity.

C13. **`R`** (hard; 8 meanings, all uppercase R). m:115 right-regular action `R_g`; m:539 realization `R` in the triangular solver proof; m:567 reduced row echelon form `R` (`R_{ij}`; same paragraph as `D`, `q`, `P_kappa`); m:631 and m:641 phase gates `R_k`, `R(beta)`, `R_y`; m:787 and tb cyclic rank `R`; m:853 unitary representation `R(g)` (subspace sources, with the
    right regular `R` of m:874 `R^{otimes r}(E_s(a))`, so `R` is both the regular and the unitary representation in one line); s3:73 and fc:70 round cap `R = 2(B + ...)`; s2:212 point set `R = {r_1..r_ell}`.

C14. **`S`** (hard). m:438, m:579, fc:202 terminal samples `S = m + t`; m:446 subspaces `S_j`; m:535 column set `S`; m:874 design multiset `S`; m:768 `S = N_L(K)`;
    s3:54 `S = P_kappa^M \ {0}`; s2:128 column sets `S_ij`. fc starts "Keep the setting of Section app:s3-setting" (fc:41) and then sets `S = m + t` (fc:202), so `S`
    changes meaning inside the same chain of appendices.

C15. **`T`** (hard). s3:82 number of tree nodes `T`; m:493 and s2:128 array `T_{ij}`; m:515, s2:376 thresholds `T_S`, `T_A`, `T_W`; m:587 and fc:325 number of candidates `T` (`T q^a`);
    m:781 `T_f`; m:864 and sub:261 number of output copies `T`; m:886 and sub:400 `T = M ell B_leaf`; m:938 `T = p` iterations.

C16. **`E`** (hard-ish). m:249 `E_s` evaluation; m:335 `E_a` projector sum (the coset-copy lift, `E_{bf a}`); m:513 `E_2(kappa)`; m:830 `E_W(c)` (the subscript `W` is never defined and clashes with `W` of m:493 and `T_W` of s2:272); s2:202 `E_kappa(ell,p)` error term; s2:410 `E_max`. m:513 and s2:379 pair `E_2` with `T_A`, `T_S`.

C17. **`k`** (hard). m:759 hidden codimension `k`; m:432 basis size `b_1..b_k` of `hh`; m:506 abort probability `2^{-k}`; m:590 number of blocks; m:822 `k` samples (and `k`, `A_c`, `d` imported
    by Theorem `thm:bb-envelope`, m:830); m:864 index `k` in `wedge^k V` and `p_k`; m:631 `k <= max(r, tau)`; also the running index `k` of `gamma_k`/`t^k`. Theorem `thm:bb-envelope` (m:830) imports `k` "as in Proposition `prop:black-box`" (m:822), one section after Corollary `cor:codim` (m:759) used `k` for codimension.

C18. **`b`** (hard). m:432 basis `b_1..b_k`; m:768 `b = dim I`; m:781 `b = sum e_i = log_p|G|`; m:822 and m:830 `b_e, b_M` bit lengths; m:618 `b = ceil(log2 N)`;
    s2:90 column index `b` (sums over `b = 1..M`).

C19. **`B`** (hard). m:188 `B_d(a)` (arity); m:579, s3:68, fc:203 cap exponent; m:781 `B` input bit length (ring section); m:864 `B = ceil(log2(rT/beta))`;
    m:881, m:886 `B_leaf`. fc:202-203 has `M_d = B_d(g_d)` and `B = ceil(log2(27N/eps))` in adjacent items.

C20. **`n`** (hard). m:249 `n = dim A <= cm`; m:822 `n = log_p|G|`; m:845 `|G| = p^n` (same meaning as m:822, different from m:249); m:886 `n log p` (`dim A`);
    m:567 `n' = M - p_r`; m:535 `n` coset index (`cos(zeta) = n`, triangular proof); m:579 `n_d`; m:570 `n_0`; m:830 `n_p`; m:845 `n_i`.
    The family `n_0`, `n_d`, `n'`, `n_p` is four unrelated quantities.

C21. **`d`** (hard). m:116 grade/degree `d` everywhere; m:819 `d = rank F_{s,c}` (Prop `prop:black-box`) and, in the same item, `d | k` as a divisor with `mu(d)`; m:853 `C^d` ambient dimension;
    Theorem `thm:bb-envelope` (m:830) says "`A_c, d, k` as in Proposition `prop:black-box`" and also uses `d` for grade in `K_c = prod_{d=2}^c` and `e_d(p)` in the same sentence.

C22. **`M`** (hard). arity `M_d`/`M` (m:441, m:502, s2:82, ...); m:335 bank size in coset-copy lift (`rho_H^{otimes M}`); m:822 and m:830 `M = p^e`/`M = p^{e_p}` (modulus);
    m:874 and sub:80 design size `M <= (c+1)!`; m:897 `M_0`. Theorem `thm:bb-envelope` uses `M = p^{e_p}` (m:830) and the arity `M_d` (m:834).

C23. **`r`** (hard). m:145, m:739 `r = g_2 = dim [L,L]`; m:567 and fc:128 observed rank `r`; m:853 `r = rank V` (subspace source); m:618 `r = ceil(log2(...))` (QFT);
    s2:198 points `r_1..r_ell`; m:411 element `r in Q` in the proof of Prop `prop:descent` (`sigma(r)^{-1} sigma(q)`).

C24. **`g`** (hard). `g_d` dimension (m:178, used at m:430); m:411 group element `g = sigma(r)^{-1}sigma(q)`; m:527 `g` generator of `F_p^x` in the triangular solver; m:813 `g_1..g_s` black-box generators;
    cd:188 `g` element of `s`.

C25. **`a`** (hard). `a_d` (m:430); `a` as the generic equation count in `B_d(a)`, `G(d,a)` (m:471) and `M_d^{sym}` (m:503); m:874 `a in A` address register; m:821 `a` generator of `C_{p^2}`.
    The thing `beta(M,n_0;a)` takes `a` as a rank, consistent with `a_d`.

C26. **`tau`** (hard). m:579, fc:202 `tau_d`; m:539 `tau = -R` (triangular proof); m:622 `tau = ceil(log2(3 pi (b+3)/eta))` precision; m:768 and cd:184 section `tau` of `S -> S/K`. The QFT lemma (m:618-622) alone defines `N, b, L, t, r, tau`, each of which has a second meaning elsewhere (C1, C3, C12, C18, C23).

C27. **`Gamma`** (hard in subscripts). fc:195-197 `Gamma_1 = {kappa_d = 1}`, `Gamma_0 = {kappa_d = p-1}`, `Gamma_F`; s3:333 `Gamma_2`, `Gamma_3` = grades of type (S2), (S3).
    `Gamma_1` is *not* "Schedule 1" while `Gamma_2`, `Gamma_3` are Schedule 2/3 types, and Schedule 1 itself (Ivanyos--Santha) is run on `Gamma_0` and as the fallback. Suggested: `Gamma_lin`, `Gamma_zs`, `Gamma_FC` and `Gamma_{S2}`, `Gamma_{S3}`.

C28. **`lambda`** (hard). m:120 and m:249 dilation parameter `delta_lambda`, `lambda in F_p^x`; m:359 and Sections 3-4 label/character `lambda`, `lambda_i`, `chi_lambda`.
    Section 4 switches to `delta_s` for the dilation (m:394), which avoids the clash there, but `delta_lambda` (Theorem `thm:rees-cover`) and `chi_lambda` (Lemma `lem:central`) are adjacent sections.

### Soft

C29. **`H`**: hidden subgroup vs Hadamard `H^{otimes b}` (m:641); also `H_d`, `H_1` (see C5). **`G`**: the group vs the function `G(d,a)` (m:471, same line as `B_d(a)` and `d`); `G_d`, `G_p`.
C30. **`mu`**: expected solution count (m:559); Mobius function (m:819); `mu_X` (m:999); `mu_kappa` roots of unity (s2:116).
C31. **`A`**: `\A` the cover (m:249); `A_c` (m:822); `A_kappa` (s2:279); `A(vartheta)` (m:641).
C32. **`Phi`**: channels `Phi_j` (m:446); BCH map `Phi` (m:819); `Phi = p^{m-1} max(...)` (m:999).
C33. **`zeta`**: root of unity (s2:116); scalar `zeta in F_p^x` (m:535); `zeta_l` coefficients.
C34. **`delta`**: dilation `delta_lambda`, `delta_s`; gap `delta > 0` (m:853); vector `delta in F_p^S` (m:535); `delta = eps/(4 ell)` (m:822). **`chi`**: character of `Z` (m:359) vs determinant character `chi` (m:872). **`rho`**: `rho_H` (m:114) vs `rho = Pi_V / r` (m:853).
C35. **`c`** (class): also `c_i` coefficients (s2:293, s2:198), `c_j` (m:643), `C_c` (m:198); `C_c` and `K_c` are two different class-dependent constants.
C36. **`e`**: `e_i` exponents (m:781); `e_p` (m:830); `e_d(p)` (m:830, same sentence); `e` (m:819).
C37. **`m`** (dimension): also `m in Z/kappa` coset index (m:493, `z_m`, `Q_m`); `m'` (m:560); `m_+` (m:819); order `2m` of moments (m:522).
C38. **`D`**: `D = P_kappa cup {0}` (m:567); `D_d = sum g_k` (m:605); `D = F_p \ R` (s2:212). **`W`** (see C16).
C39. **`p`** as prime vs pivot columns `p_1 < ... < p_r` (m:567) vs `p_k` success probability (m:864) vs `p_i`.
C40. **`s`**: scalars `s_i` in the SDE; evaluation points `s_1..s_c` (m:150); number of generators `s` (m:813); `s` in `E_s`.

Count: **40** entries, of which **28 are hard** (C1-C28) and 12 soft (C29-C40). Of the 28 hard ones, C1, C2, C3, C4, C6, C7 and C13 have six or more meanings.
The symbols in the brief with a collision: `c` (C35), `p` (C39), `m` (C37), `g_d` (C24), `a_d` (C25), `h` (C8), `q` (C9), `Q_j` (C7), `T_A`/`T_S` (C15),
`B_d(g)` (C19), `n_d` (C20), `u` (C6), `S` (C14), `tau_d` (C26), `beta` (C4), `Gamma_*` (C27), `rho_H` (C34, minor), `H_d`/`K_d` (C5, C11), `eps` (none), `ell` (C2), `N` (C1), `E_W(c)` (C16).
Symbols with no collision found: `kappa_d`, `eps`, `E_2(kappa)`, `tau_d` (but see C26 for bare `tau`), `Gamma_0` alone (but see C27 for its siblings).

## 4. Symbols defined only in appendices (or only later) but used in the body

"Used" means the symbol appears in `main.tex` at the line given, with no definition at that point in the body.

| Symbol | First body use | Where it is defined | Remark |
| --- | --- | --- | --- |
| `\Gamma_0` | m:752 (proof of Cor `cor:fpt-r`(ii): "`\Gamma_0 = \{c\}`") | fc:195-197 (`app:fc-mixed`) | The only body use. No definition and no `\ref`. Add "(the grades with `\kappa_d = p-1`, Section~\ref{app:fc-mixed})" or write it in words. |
| `t_{\mathrm{S1}}` | m:750 ("`t_{\mathrm{S1}} = 0` in Prop `prop:fc-uniform`(b)") | fc:287-289 | Defined only as "the time of one Schedule 1 call at grade `d = p-1`" in the appendix. |
| `T_A(\kappa)`, `T_S(\kappa)` | m:493 (Schedule 2 "Terms"), then m:515, m:518, m:522 | s2:303-376 (`app:s2-TA`, Prop `prop:app-s2-TA`) | m:493 defines them in words and cites `app:s2-TA`, so adequate. The formal definition `\inf\{p > \kappa+1 : \Delta(p) \le 1/2,\ U_\kappa(p) < \kappa/(\kappa-1)\}` (and `\le 1+1/(8\kappa)` for `T_S`) is at s2:376 only. |
| `B_{\mathrm{leaf}}` | m:881, m:886 (subspace construction, step (4)) | sub:101-102 (`def:app-sub-core`), sub:378 | m:881 cites `def:app-sub-core` only at the end of the sentence, after the first use. |
| `\beta(M,n_0;a)` | not used by name in the body; the body writes the formula at m:575 | fc:57 (`eq:fc-beta`) | Fine. The body then uses bare `\beta` (m:578-579); `\beta_d` is appendix-only (fc:126). |
| `Q_0, Q_m, \xi, z_m, W, \zeta` | m:493 ("Schedule 2: Terms") | s2:96-120 (`app:s2-gcd`, `app:s2-tensor`) | The body recalls them in one paragraph and cites Appendix `app:schedule2`. Fine. |
| `\nu_d`, `L_\kappa`, `R'`, `n_0^{(d)}`, `\tau_{d,j}` | not used in the body | fc:70, fc:202, fc:437 | Appendix-only; no action. |
| `u_d`, `N(\Lambda)`, `\Gamma_2`, `\Gamma_3` | not used in the body | s3:50-63, s3:333, s3:353 | Appendix-only; no action. |

Symbols used in Table `tab:main-regimes` (m:203-229) before their first definition in the text: `u` (row "Random column", m:212-213; defined m:557),
`a_d` (m:212; defined m:430), `\tau_d` (m:213; defined m:579), `n_p`, `e_p`, `E_W(c)`, `N` (m:218; defined m:830), and `M\ell`, `N+1` (caption m:202; defined m:864-874).
`M_d` (defined m:178) and `\kappa_d`, `B_d` (defined m:188) are fine. The new Notation subsection comes after the table, so the caption
should point to it.

## Verification

Every `\ref{...}` and `\eqref{...}` in the block of Section 1 was extracted by script and compared with the set of `\label{...}` in the seven `.tex` files
(215 labels). Result: 36 distinct references (including the 3 table labels cited in the block), none missing among existing labels. The four new labels (`sec:notation`, `tab:notation-instance`, `tab:notation-sde`,
`tab:notation-bb`) do not collide with an existing label. The block was not compiled (no `.tex` edit was allowed, and the block depends on the paper's preamble).
Meanings in the table were read from the cited definitions. Line numbers in Sections 3-4 were taken from the files as of 2026-11-04 and will move after any edit.
