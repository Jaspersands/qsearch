# Rees paper: check of the notation tables (2026-11-04)

Scope: `docs/papers/rees-hsp/main.tex`, `\subsection{Notation}` (`sec:notation`),
Tables `tab:notation-instance`, `tab:notation-sde`, `tab:notation-bb`
(main.tex lines 238-337). Each row was checked against the `\label` it cites
(grep across `docs/papers/rees-hsp/*.tex`, excluding the unbuilt
`main-full-draft.tex`) and against the first place the symbol is defined.
No .tex file was edited. AI check only.

Verdicts: **correct**; **wrong meaning**; **wrong formula**; **wrong place**
(the cited label does not contain the definition, or the body defines the
symbol before the cited appendix). "Optional" marks a row that is right but
could also name an earlier first statement in the same part of the paper.

All cited labels exist and resolve. `sec:intro` is the label of Section 1
("Introduction, Input Contract, and Main Results", main.tex:107). That section
contains the background subsection, where rho_H is defined (main.tex:114), and
the core-idea subsection, where gamma_k, g_k, n, r, A, E_s, delta_lambda and
hlift are defined (main.tex ~150-170). It also contains
Def. `def:input-contract`, Thm. `thm:main` and Tab. `tab:main-regimes`. So
"Sec.~\ref{sec:intro}" is right for rho_H and gamma_k.

## Table 1 (`tab:notation-instance`)

1. `$p$`: correct (Def. input-contract (i): prime p > c).
2. `$c$`: correct (Def. input-contract (i), "class c"; c < p).
3. `$m$`: correct (Def. input-contract (i), m = dim L).
4. `$\mathcal{L}$, $G$`: correct (Def. input-contract (i)-(ii), G = (L, *) with truncated BCH).
5. `$H$, $\hh$`: correct (Def. input-contract (iii) and following text: hh = log H is an F_p-Lie subalgebra).
6. `$f$, $w$`: correct (Thm. main: f : G -> {0,1}^w). f appears earlier in Sec. 1 with codomain S, and w is first defined in Thm. main.
7. `$\eps$`: correct (Thm. main, eps in (0,1)).
8. `$Q$`: correct (Thm. main, Q = c(m + ceil(log_p(3/eps))) prod_d B_d(g_d), queries or copies).
9. `$\rho_H$`: correct. Formula |G|^{-1} sum_{h in H} R_h with R_g|x> = |x g^{-1}> is at main.tex:114, inside Sec. sec:intro.
10. `$\gamma_k(\mathcal{L})$, $g_k$`: correct (Sec. 1 core-idea subsection: gamma_1 = L, gamma_{k+1} = [L, gamma_k], g_k = dim gamma_k, g_1 = m; Thm. main restates g_d).
11. `$r$`: correct (Sec. 1: r := g_2 = dim[L,L]; restated in Cor. fpt-r).
12. `$\A$, $n$`: correct; optional. Thm. rees-cover restates A and gives dim n <= cm, but the first definition (A = R_+(L) = sum_k t^k gamma_k(L) in L[t], n := dim A = sum_k g_k <= cm) is in Sec. 1. Optional cell: `Sec.~\ref{sec:intro}; Thm.~\ref{thm:rees-cover}`.
13. `$t$`: **wrong place**. Thm. rees-cover uses t but does not introduce it. t comes in at Sec. 1 ("subset L[t]", with the bracket [t^i x, t^j y] := t^{i+j}[x,y]).
    Replacement: `$t$ & formal variable of $\mathcal{L}[t]$ (Rees grading) & Sec.~\ref{sec:intro}; Thm.~\ref{thm:rees-cover} \\`
14. `$E_s$, $\delta_\lambda$`: **wrong place**. Thm. rees-cover(ii) states only properties (homomorphism, surjective for s != 0, E_s o delta_lambda = E_{lambda s}) and gives no formula. The definitions E_s(sum_k t^k x_k) = sum_k s^k x_k (s in F_p) and delta_lambda(sum_k t^k x_k) = sum_k lambda^k t^k x_k (lambda in F_p^x) are in Sec. 1. The meaning text is right.
    Replacement: `$E_s$, $\delta_\lambda$ & evaluation homomorphism $\A \to \mathcal{L}$; dilation automorphism of $\A$ & Sec.~\ref{sec:intro}; Thm.~\ref{thm:rees-cover}(ii) \\`
15. `$\hlift$`: correct; optional. Lem. homogeneous restates the formula and adds the intersection form; first defined in Sec. 1. Optional cell: `Sec.~\ref{sec:intro}; Lem.~\ref{lem:homogeneous}`.
16. `$Z$, $K$`: correct (Sec. instrument: Z <= Z(G) elementary abelian p-group, K = H ∩ Z).
17. `$\lambda$ (label)`: correct; optional. The characters chi_lambda and the projectors Pi_lambda are defined in the opening text of Sec. instrument, and Lem. central gives the law of lambda. Optional cell: `Sec.~\ref{sec:instrument}; Lem.~\ref{lem:central}`.
18. `$G_d$, $Z_d$`: correct (Sec. recursion: A^{(d)} = A / sum_{k>d} A_k, G_d = (A^{(d)}, *), Z_d = t^d gamma_d(L), central, elementary abelian of rank g_d).
19. `$H_d$, $K_d$`: correct. K_d = t^d(hh ∩ gamma_d(L)) is in the Sec. recursion text. H_d = exp(sum_{k<=d} t^k(hh ∩ gamma_k(L))) is named in the proof of Thm. main, which sits inside Subsec. sec:recursion.
20. `$a_d$`: correct (Sec. recursion: a_d := dim K_d^perp = g_d - dim(hh ∩ gamma_d) <= g_d).
21. `$M_d$`: correct. First use is Thm. main (M_d = B_d(g_d)). The general meaning ("if stage d uses arity M_d") is in Sec. recursion. Optional cell: `Thm.~\ref{thm:main}; Sec.~\ref{sec:recursion}`.
22. `$P$`: correct (Sec. recursion: P = prod_{d=2}^c M_d lifted sources per terminal sample).
23. `$S$`: correct (Sec. recursion: S = m + t, t = ceil(log_p(3/eps)); the same S is used in Thm. free-coordinate(iii) and in tau_d). This S is for Schedules 1 and 2 and Thm. free-coordinate(iii). Schedule 3 (Thm. random-column(ii), Thm. free-coordinate(ii)) uses m' = m + ceil(log_2(3/eps)) trees instead. App. schedule3 uses S for the solution set P_kappa^M \ {0}.

## Table 2 (`tab:notation-sde`)

24. `$\kappa_d$`: correct (main.tex:188: "Here kappa_d := gcd(d,p-1)", in Sec. 1 just before Tab. main-regimes).
25. `$B_d(a)$, $G(d,a)$`: **wrong meaning** (and the place is incomplete). The meaning cell calls both symbols the arity. Only B_d(a) = G(d,a)^{ceil(log_2(d+1))} is the arity. G(d,a) = d^{d(d-1)/2}(a+1)^d is the collision count of [IvanyosSantha2015, Thm. 11] (Thm. is-import; Schedule 1 text after Eq. is-arity). The formulas in the cited places are right. B_d(a) is first defined at main.tex:190, in Sec. 1 before Tab. main-regimes; Thm. main says "B_d as in Theorem is-import".
    Replacement: `$B_d(a)$, $G(d,a)$ & Ivanyos--Santha arity $B_d(a) = G(d,a)^{\lceil\log_2(d+1)\rceil}$ for $a$ equations of degree $d$ (Schedule~1); collision count $G(d,a) = d^{d(d-1)/2}(a+1)^d$ of~\cite[Theorem~11]{IvanyosSantha2015} & before Tab.~\ref{tab:main-regimes}; Thm.~\ref{thm:is-import}; Eq.~\eqref{eq:is-arity} \\`
26. `$h$`: correct; optional. h = (p-1)/kappa_d = |Q_0| is the order of the group of nonzero d-th powers, which by Lem. app-s2-gcd(a) is also the group of nonzero kappa_d-th powers. Both cited places define h. The first statement is earlier, in the Schedule 2 "Terms" paragraph of Sec. sde (main.tex:596). Optional cell: `Sec.~\ref{sec:sde} (Schedule~2); Sec.~\ref{app:s2-gcd}; Thm.~\ref{thm:random-column}`.
27. `$Q_0$, $Q_m$, $\xi$, $z_m$`: **wrong place**. The meaning is right: Q_0 = {x^kappa : x in F_p^x}, Q_m = z_m Q_0 = xi^m Q_0, xi a coset generator (xi^h of exact order kappa), z_m = xi^m. All four are first defined in the body, in the Schedule 2 "Terms" paragraph of Sec. sde (main.tex:596), before the appendix the row cites.
    Replacement: `$Q_0$, $Q_m$, $\xi$, $z_m$ & subgroup of $\kappa$-th powers, its cosets $Q_m = z_mQ_0$, coset generator, $z_m = \xi^m$ & Sec.~\ref{sec:sde} (Schedule~2); Sec.~\ref{app:s2-gcd} \\`
28. `$W$`: **wrong place**. The formula is right. It is first defined in the Schedule 2 "Terms" paragraph of Sec. sde (main.tex:596); App. s2-tensor restates it and adds dim W = kappa - 1.
    Replacement: `$W$ & $\{w \in \Fp^\kappa : \sum_m z_mw_m = 0\}$ & Sec.~\ref{sec:sde} (Schedule~2); Sec.~\ref{app:s2-tensor} \\`
29. `$M_d^{\mathrm{sym}}$`: correct (Eq. power-arity: (a+1)((kappa-1)a+1)). The Terms paragraph of the same section states it first, so no change is needed.
30. `$E_2(\kappa)$`: correct. Prop. decoupled-sde: the primes at which no universal two-level contraction of the decoupled form exists. Lem. app-s2-normal shows every contraction is decoupled, so this agrees with the Terms paragraph definition ("primes p = 1 mod kappa with no two-level contraction"). Same section, so no change is needed.
31. `$T_S(\kappa)$, $T_A(\kappa)$`: correct. App. s2-TA defines T_A = inf{p > kappa+1 : Delta(p) <= 1/2, U_kappa(p) < kappa/(kappa-1)} and T_S = inf{... U_kappa(p) <= 1 + 1/(8 kappa)} from the second-moment bound U_kappa(p). Prop. app-s2-TA(i) gives p > T_A => p not in E_2(kappa), and (iii) gives the sampler cost for p > T_S.
32. `$u$`: correct (Thm. random-column: integer u >= 2, c <= u, public a_d <= u-1, p >= 16u^2). The row leaves out u >= 2, which is harmless.
33. `$P_\kappa$, $D$, $q$`: **wrong place**, and the row hides a clash of conventions. The formulas are right for the body and for App. free-coordinate: P_kappa = {x^kappa : x in F_p^x}, D = P_kappa ∪ {0}, q = (h+1)/p >= 1/kappa. They are first defined in the body, in the "Schedule 3 with a free-coordinate sampler" paragraph of Sec. sde (main.tex:670), and App. fc-setting says it "follows the body". App. schedule3 (Sec. app:s3-setting) defines P_kappa = {0} ∪ {x^kappa}, i.e. it uses P_kappa for the set called D here, and App. fc-setting itself notes this. The same nonzero set is also Q_0 in Schedule 2 / App. schedule2 and P in Prop. triangular-sde.
    Replacement: `$P_\kappa$, $D$, $q$ & nonzero $\kappa$-th powers (equal to $Q_0$); $D = P_\kappa \cup \{0\}$; $q = (h+1)/p$. Appendix~\ref{app:schedule3} writes $P_\kappa$ for $D$ & Sec.~\ref{sec:sde}, before Thm.~\ref{thm:free-coordinate}; Sec.~\ref{app:fc-setting} \\`
34. `$n_0$`: correct (Sec. sde free-coordinate paragraph and Thm. free-coordinate(i): the node aborts if n' = M - p_r < n_0).
35. `$\beta(M,n_0;a)$`: **wrong place**. The formula 4/(h^{n_0-1} q^a) + (p^a-1)/((p-1)p^L), L = M - n_0, is first displayed in Thm. free-coordinate(i) in the body, written there as beta. Eq. fc-beta is the appendix restatement with the arguments (M, n_0; a).
    Replacement: `$\beta(M,n_0;a)$ & bank-failure bound of the free-coordinate sampler & Thm.~\ref{thm:free-coordinate}(i); Eq.~\eqref{eq:fc-beta} \\`
36. `$\tau_d$`: correct (Thm. free-coordinate(iii): tau_d = eps/(9(c-1) S n_d), with S = m + ceil(log_p(3/eps))). Optional precision: tau_d is the per-node bound required of the bank event beta, not of the random steps, which are capped separately at 2^{-B}. A tighter cell would read "per-node bank-failure budget".
37. `$n_d$`: correct (Thm. free-coordinate(iii): n_d = prod_{2<=d'<d} M_{d'}; App. fc-mixed (R3): a tree "has n_d nodes of grade d").
38. `$B$`: **wrong place**. The meaning is right. The cap exponent is first used in Thm. random-column(i), where the trials, root extraction and field sampling fail with probability <= 2^{-B} each, and (ii) sets B = ceil(log_2(64(4u)^{c-1})). Both come before Thm. free-coordinate(iii), which sets B = ceil(log_2(27N/eps)). App. s3-setting ("Fix B >= 1") is the appendix definition.
    Replacement: `$B$ & cap exponent: each random step fails with probability $\le 2^{-B}$ & Thm.~\ref{thm:random-column}(i); Thm.~\ref{thm:free-coordinate}(iii); Sec.~\ref{app:s3-setting} \\`
39. `$\Gamma_0$, $\Gamma_1$, $\Gamma_{\mathrm F}$`: correct (App. fc-mixed: Gamma_F = {d : 2 <= kappa_d < p-1}, Gamma_1 = {d : kappa_d = 1}, Gamma_0 = {d : kappa_d = p-1 >= 2}; the row lists them in that order of meanings).
40. `$\Gamma_2$, $\Gamma_3$`: correct (Prop. mixed-schedule in App. s3-mixed: the grades of type (S2) and (S3)).
41. `$N_{\mathrm{instr}}$`: correct (Sec. recursion: N_instr = S(P + sum_{d=2}^c prod_{d'=2}^{d-1} M_{d'} + 1)).

## Table 3 (`tab:notation-bb`)

42. `$k$`: correct (Cor. codim: codim_{F_p} hh <= k, k given). Note that the table lists k twice, here and in the `$A_c$, $k$` row, with different meanings.
43. `$R$`: correct (Thm. ring-to-field: R = dim_{F_p}([L,L]/p[L,L]), the cyclic rank of the derived ring; it is introduced in words just before the theorem, in Sec. ring).
44. `$b$`: correct (Sec. ring: L = ⊕_i Z/p^{e_i}Z, b = sum_i e_i = log_p|G|).
45. `$\Omega_1(G)$, $H_1$`: correct (Thm. ring-to-field(i)-(ii): Omega_1(G) = {g : g^p = 1} = exp L[p]; H_1 = H ∩ Omega_1(G)).
46. `$Q_f$, $T_f$`: correct (Sec. ring: Q_f the number of queries, T_f the internal cost of one query).
47. `$s$, $g_1,\dots,g_s$`: correct (Sec. black-box-groups: generators g_1,...,g_s). Note that this g_1 clashes with g_1 = m in Table 1. The clash is in the paper, not in the table.
48. `$F_{s,c}$, $\Phi$, $d$`: correct (Prop. black-box(i): the free nilpotent Lie ring of class c on s generators over Z/p^eZ, the BCH map Phi : (F_{s,c}, *) -> G with x_i -> g_i, d = rank F_{s,c}). Note that this d clashes with the grade index d, which Thm. bb-envelope uses in the same display (K_c = prod_{d=2}^c ...).
49. `$A_c$, $k$`: correct (Prop. black-box(iv): A_c = m_+ + 2 b_M q_+, which bounds the multiplications of one Lazard addition, m_+ products plus q_+ powers at <= 2b_M each; k = floor(ell/log_2 p) + ceil(log_p(8 ell/eps)) kernel-step samples).
50. `$\ell$`: **wrong place**. The meaning is right. The encoding length is first defined in Prop. black-box(iv) ("let ell be the encoding length", used in k), and it is already used in Prop. black-box(ii) ("ell-bit encodings"), before Thm. bb-envelope.
    Replacement: `$\ell$ & encoding length of the black-box group & Prop.~\ref{prop:black-box}(iv); Thm.~\ref{thm:bb-envelope} \\`
51. `$N$`: correct (Thm. bb-envelope, closing paragraph inside the theorem: N = s ell + w + log(1/eps)).
52. `$n_p$, $e_p$, $M$, $b_M$`: correct; optional. Thm. bb-envelope: n_p = log_p|G_p|, p^{e_p} = exp G_p, M = p^{e_p}, b_M = ceil(log_2 M). M and b_M are first defined in Prop. black-box(iv), with M = p^e. Optional cell: `Thm.~\ref{thm:bb-envelope}; $M$, $b_M$ also Prop.~\ref{prop:black-box}(iv)`.
53. `$L$, $t$, $K_c$`: correct (Thm. bb-envelope: L = sum_{p>c} n_p, t = ceil(log_2(12 ell/eps)), K_c = prod_{d=2}^c d^{d(d-1) ceil(log_2(d+1))/2}). Note that K_c is the same constant the paper calls C_c in Sec. 1 (the Schedule 1 query display after Thm. main). The table could say so, but no change is needed.
54. `$E_W(c)$, $e_d(p)$`: correct (Thm. bb-envelope: E_W(c) = max_{p>c}(1 + sum_{d=2}^c e_d(p)), with e_d(p) = 1, 2 or kappa_d ceil(log_2(kappa_d+1)) for a linear, two-level or Ivanyos--Santha grade of the combined rule).
55. `$V$, $\Omega_V$, $\delta$`: **wrong meaning** (Omega_V). Thm. subspace-source defines Omega_V = u_1 ∧ ... ∧ u_r for an orthonormal frame of V. That is a unit vector spanning the top exterior power ∧^r V, not the top exterior power itself. V (r-dimensional subspace of C^d) and delta (TD(rho, R(g) rho R(g)^†) >= delta for g not in H) are defined in the Sec. subspace text, before the theorem. Here r and d are the dimension of V and of the ambient space, not g_2 or a grade; the table introduction does not list r and d among the reused letters.
    Replacement: `$V$, $\Omega_V$, $\delta$ & promised $r$-dimensional subspace of $\mathbb{C}^d$ (this $r$ is not $g_2$); its unit top wedge $u_1\wedge\cdots\wedge u_r$ for an orthonormal frame; gap promise & Sec.~\ref{sec:subspace}; Thm.~\ref{thm:subspace-source} \\`
56. `$B_{\mathrm{leaf}}$`: correct (Def. app-sub-core: B_leaf(eps_0) inputs of the core, = (m+t) prod_{d'} M_{d'} under Schedule 1 with t = ceil(log_p(3/eps_0)); Cor. subspace-hsp uses B_leaf = B_leaf(eps/4)). Optional cell: `Def.~\ref{def:app-sub-core}; Cor.~\ref{cor:subspace-hsp}`.

## Checks asked for

- Formulas: S, tau_d, n_d, q, h, M_d^sym, E_W(c), A_c, K_c, t (both meanings), N, B_leaf, T_S/T_A, E_2 and all Gamma sets match the source exactly. No row has a wrong formula.
- P_kappa vs D: the table is right for the body and App. free-coordinate. App. schedule3 uses P_kappa for D. See row 33 for the fix.
- Sec.~\ref{sec:intro}: right for rho_H (main.tex:114) and for gamma_k and g_k (core-idea subsection of Section 1).

## Rows to change (10 of 56)

1. Row 13, `$t$` (Tab. 1): wrong place.
2. Row 14, `$E_s$, $\delta_\lambda$` (Tab. 1): wrong place.
3. Row 25, `$B_d(a)$, $G(d,a)$` (Tab. 2): wrong meaning for G(d,a); add the first place.
4. Row 27, `$Q_0$, $Q_m$, $\xi$, $z_m$` (Tab. 2): wrong place.
5. Row 28, `$W$` (Tab. 2): wrong place.
6. Row 33, `$P_\kappa$, $D$, $q$` (Tab. 2): wrong place; add the App. schedule3 convention.
7. Row 35, `$\beta(M,n_0;a)$` (Tab. 2): wrong place.
8. Row 38, `$B$` (Tab. 2): wrong place.
9. Row 50, `$\ell$` (Tab. 3): wrong place.
10. Row 55, `$V$, $\Omega_V$, $\delta$` (Tab. 3): wrong meaning for Omega_V.

Optional (correct as is; an earlier first statement could be added): rows 12, 15, 17, 21, 26, 36, 52, 56.

Optional fix to the table introduction (main.tex:241). Besides N, ell, t, u, Q and K, these letters also carry several meanings: S (rows 23, and the solution set in App. schedule3), B, k (twice in Tab. 3), d, r, g_1 and P_kappa.
