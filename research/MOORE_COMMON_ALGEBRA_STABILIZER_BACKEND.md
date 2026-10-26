# Common Matrix-Algebra ($J^\nu = 0, \nu \le p$) Moore-Form Stabilizer Backend & Polynomial-Graph Prior-Art Audit

## 1. Scope & Guard Contract

- **Elementary Common-Algebra Stabilizer Backend (`recover_common_algebra_moore_stabilizer`)**: Given an accepted `MooreRecognition` row space $W \subseteq \mathbb{F}_p^D$ and public matrix generators $g_1, \dots, g_s \in \text{GL}(D, p)$, forms the **common nonunital associative matrix algebra** $J = \text{Alg}_{\mathbb{F}_p}(g_1 - I, \dots, g_s - I) \subseteq M_D(\mathbb{F}_p)$, verifies $J^\nu = 0$ with $\nu \le p$, closes the $\mathbb{F}_p$-span of truncated matrix logarithms $\log(g_i)$ under matrix commutators $[A, B] = AB - BA$ to obtain $L = \log(\Gamma)$, solves the linear system $W A N = 0$ ($W N = 0$) for $A \in L$, and exponentiates a basis of the kernel $\mathfrak{h} = \{A \in L : W A \subseteq W\}$ to recover exact group generators of $\text{Stab}_\Gamma(F)$.
- **Commuting Order-$p$ Guard Falsifier ($p = 5, D = 25$)**: On $g = I + J_5 \otimes I_5$ and $h = I + I_5 \otimes J_5$, both generators commute (`generators_commute = True`), satisfy $g^5 = h^5 = (gh)^5 = I$ (`all_generators_order_dividing_p = True`), and have individual nilpotency index $5 \le p$, yet the common algebra $J$ has dimension `24` and nilpotency index $\nu = 9 > p = 5$, causing individual truncated matrix logs to fail additivity (`individual_truncated_logs_additive = False`). The common-$J$ guard fails closed (`solver_fails_closed = True`).

## 2. Stabilizer Generator Recovery Controls

- **$\text{UT}_3(\mathbb{F}_5)$ ($D = 3, p = 5$)**: $\nu = 3$, $\dim L = 3$, $\dim \mathfrak{h} = 1$, recovered subgroup order `5` matching exact stabilizer across all `125` group elements (`matches_exact_stabilizer_subgroup = True`).
- **Conjugated $\text{UT}_4(\mathbb{F}_7)$ ($D = 4, p = 7$)**: Under a dense basis change $C \in \text{GL}(4, 7)$ not supplied to the recognizer or solver, recovers $\dim \mathfrak{h} = 2$ (`stabilizer_lie_is_subalgebra = True`, subgroup order `49`, `all_recovered_elements_fix_moore_form = True`).
- **Two-Block $\text{UT}_3(\mathbb{F}_5)^2$ ($D = 6, p = 5$, orbit rank $9$)**: Recovers $\dim \mathfrak{h} = 2$ and exact subgroup of order `25` inside $|\Gamma| = 15625` (`matches_exact_stabilizer_subgroup = True`).
- **Class-9 $\text{UT}_{10}(\mathbb{F}_{43})^m$ Controls**: For $m = 2$ ($D = 20$, orbit rank $100$), closes $J$ of dimension `90` ($\nu = 10 \le 43$) and recovers $\dim \mathfrak{h} = 72`; for the live $m = 5$ ($D = 50$, proved orbit rank $10^5 = 100{,}000$) canonical basis of $\mathfrak{ut}_{10}(\mathbb{F}_{43})^5$ ($\dim L = 225$), $W A N = 0$ and matrix exponentiation recover all `180` stabilizer generators (`all_180_exponentiated_generators_fix_moore_form = True`).

## 3. Abelian Hidden Polynomial-Graph Tuple Evaluation vs Nonabelian Positive Rees Cover

- On $\mathfrak{ut}_4(\mathbb{F}_7)$ ($c = 3$), naive scalar dilation $X \mapsto 2 X$ fails the Lie homomorphism identity $[2X, 2Y] = 2[X, Y]$ on `8` basis pairs (`naive_dilation_is_lie_automorphism = False`).
- All three Rees evaluation maps $E_s : A \to \mathfrak{ut}_4(\mathbb{F}_7)$ ($s \in \{1, 2, 3\}$) satisfy $[E_s(a), E_s(b)]_L = E_s([a, b]_A)$ across all $100$ basis pairs (`rees_evaluations_are_exact_lie_homomorphisms = True`).
- Both the non-homogeneous line $\mathfrak{h}_{\text{line}} = \mathbb{F}_7(E_{01} + E_{03})$ and the pure central line $\mathfrak{h}_{\text{central}} = \mathbb{F}_7 E_{03}$ are preserved in grade 1 of the positive Rees cover (`nonhomogeneous_line_recovered_in_rees_grade1 = True`, `central_line_rees_grade1_dim = 1`), whereas the associated graded grade-1 quotient $L / \gamma_2(L)$ collapses $\mathfrak{h}_{\text{central}}$ to dimension `0`.
