# Ambient Filtration Certifier, Unrolled Solve(L,f) Recursion, Two-Tree Resource Audit, and Class-Four Normal Obstruction

2026-10-21. **Standalone public frontend verifier, normalizer-quotient constructor, unrolled recursion controller, and resource/obstruction audit; not a coherent quantum circuit compiler, general-prime SDE solver, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/class_three_ambient_frontend.py` (`class_three_ambient_frontend_v2`) and `tests/test_class_three_ambient_frontend.py`, addressing the frontend certification, `M/K` normalizer-quotient, unrolled `Solve(L,f)` recursion, and resource-comparison obligations in `research/CLASS_THREE_MONOMIAL_FULL_JET.md` (Sections 2 & 7.1–7.3) and `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Ambient Filtration and Exact Center Certifier (`certify_ambient_class_three_derived`)**:
   - Extracts $N = [L, L]$ and its exact center $C = Z(N)$ via arbitrary-precision `fmpz_mod_mat` linear equations over $\mathbb{F}_p$, rejects proper subspaces $C \subsetneq Z(N)$, certifies $\gamma_{c-1}(L) \subseteq Z(N)$, and constructs the verified `ClassThreeStructure` and `FullTaylorJetChart` for both $\text{class}(N) = 3$ ($B \ne 0$, e.g. $\mathfrak{ut}_7(\mathbb{F}_{19})$ with $(r, s, z) = (9, 2, 4)$) and $\text{class}(N) = 2$ ($B = 0, \beta = (), \delta = ((), \dots, ())$, e.g. $\mathfrak{ut}_6(\mathbb{F}_{17})$ with $(r, s, z) = (6, 0, 4)$).
2. **Legitimate $M/K$ Normalizer-Quotient Constructor & Unrolled `Solve(L,f)` Recursion (`public_normalizer_quotient_algebra`, `unrolled_full_jet_solve`)**:
   - Implements Section 7.1–7.2 without assuming $N \subseteq M = N_L(K)$: on $\mathfrak{ut}_7(\mathbb{F}_{19})$ with $H = \langle E_{12}, E_{13} \rangle$ and $K = H \cap N = \langle E_{13} \rangle$, $N \subseteq M$ is `False` ($E_{35} \in N \setminus M$), yet $S = M/K$ is well-defined and its derived ideal $S' = (M' + K)/K$ lies inside $(N \cap M)/K$.
   - Unrolls `K := Solve(N, f|_{exp(N)})` down to the abelian base case without receiving hidden $K$ as advice, completing inside `5 <= 7` image calls and `3 <= 3` abelian HSP calls.
3. **Two-Tree Resource Audit & Class-Four Normal Subgroup Obstruction**:
   - Computes the Section 7 two-tree resource envelope with Ivanyos–Santha collision recurrences and verifies that class-4 normal groups retain carrier-dependent $B$-Fourier frequency shifts (`11` distinct $\mu_1$ shifts across $x_0 \in \mathbb{F}_{11}$).

## 2. Certified $\mathfrak{ut}_7(\mathbb{F}_{19})$ & $\mathfrak{ut}_6(\mathbb{F}_{17})$ Frontend and Unrolled Recursion

| Metric | Value |
| :--- | :--- |
| $\mathfrak{ut}_7(\mathbb{F}_{19})$ $(c, m, \dim N, \text{class}(N))$ | `(6, 6, 15, 3)` |
| $\mathfrak{ut}_7(\mathbb{F}_{19})$ $(r, s, z)$ / full jet width $J$ | `(9, 2, 4)` / `1080` |
| $\mathfrak{ut}_6(\mathbb{F}_{17})$ unified $B=0$ $(r, s, z)$ / full jet width $J$ | `(6, 0, 4)` / `168` |
| Unrolled `Solve(ut_7)` status / recovered generators | `SUCCESS` / `2` |
| Unrolled `Solve(ut_7)` image calls / abelian HSP calls | `5 / 7` and `3 / 3` |
| `N <= M = N_L(K)` flags across normalizer quotients | `[True, False]` |
| $\log_2$ weighted tree / $\log_2$ ordinary tree ($j=1..4$) | `35748.46` / `779.35` |
| $\log_2$ total matrix leaves $M$ / raw queries upper bound | `36530.82` / `36555.22` |

## 3. Explicit Scope Boundaries

- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
