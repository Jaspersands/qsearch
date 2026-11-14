# Class-three worked example on the free two-generator class-three algebra

The filiform files (`example.tex`, `README.md`, `verify_class3.py` and the rest) are kept
unchanged. The coordinator ruled filiform n4 out as the showcase, because it is
F_p ⋉ F_p^3 and so falls inside the Ivanyos-Santha Cor. 8 family.

Deliverables:
* `example_free.tex`: drop-in `\subsection{Example: a Class-Three Group}`,
  `\label{sec:example-class3}`. It uses `\ref{rem:fewer-points}` from `fixes.tex` (b). A short
  version for Section 1.3 is in the comments at the end.
* `fixes.tex`:
  * (a) obstacle (2) wording, "public, independent of H";
  * (b) `rem:fewer-points`, with its proof;
  * (c) Section 7.1 renamed from Z_1, Z_2 to tz, t^2z, as replacement lines.
* Compile test: all of the above were merged into a scratch copy of `core/main-core.tex`. It
  gives 40 pp., no undefined references and no new overfull boxes. The example runs
  pp. 23-25, about 1.7 pages. The paper itself was NOT edited.

## Scripts

All scripts are run with `nice -n 19 /opt/anaconda3/bin/python` from this folder.

| script | output | what |
|---|---|---|
| `verify_free.py` | `verify_free.out` | tags F1-F6, at p = 5 and 7 (fibres and Aut at p = 5 only) |
| `verify_free_rerun.py` | `verify_free_rerun.out` | re-runs F1e and F5h. In the first run their *expected values* were wrong (Z(A) also contains t^2u, t^2w; psi_theta(x) has a w-term). The script was corrected and both now PASS. All other FAILs in `verify_free.out` are these two. |
| `gap_free_make.py` → `gap_free_p5.g` | `gap_free_p5.out` | GAP 4.15 + autpgrp on the group G itself (a permutation group of degree 3125, by right BCH multiplication) |
| `run_sim_free.py` | `run_sim_free_5.out`, `run_sim_free_5.json` | full descent at p = 5 with `theorems/rees_end_to_end_sim.py` (ExactBackend, cover of order 5^10) |

`run_sim_free.py` uses a copy of `run_rees` that drops the simulator's per-label cache of
conditioned top-level states (it would need about 10 GB). Nothing else is changed.

## Claim → check

| claim | check |
|---|---|
| gamma_2 = span(z,u,w), gamma_3 = Z(L) = span(u,w), (g2,g3) = (3,2), n = 10 | F1c, F1d |
| cover brackets (the five displayed), Jacobi, class 3 | F1a, F1b, F1g |
| E_s Lie homomorphism; E_s, delta_theta homomorphisms for the class-3 BCH product | F1f; F2a, F2b, F2c (symbolic over Q, denominators 2 and 12 only); F2d (random pairs mod 5 and 7) |
| Related Work: no abelian subgroup of index p (6 maximal subgroups, none abelian) | GAP: `maximal subgroups: 6 ... abelian ones: 0` |
| not abelian-by-cyclic | GAP: `abelian N with G/N cyclic: 0` (all 16 normal subgroups) |
| <exp x><exp y> has 25 elements, not a subgroup (so G is not quasi-Hamiltonian) | GAP: `|<exp x><exp y>| = 25, |<exp x, exp y>| = 3125` |
| H = exp(F_p(x+z+u)): subalgebra, not normal, hlift = F_p(tx+tz+tu) | F3a, F3b, F3c |
| tuple-oracle fibres = left cosets of exp(hlift) | F3d: EXHAUSTIVE over all 9,765,625 points of A, for both H and H'. hat f is invariant under right multiplication by the generators of hlift, and every fibre has exactly \|hlift\| points, so the fibres are exactly the cosets. F3e: the fibre over 0 equals hlift. Also the simulator's coset-partition check (`fibres: 1953125, lifted_order: 5`). |
| xi_q = 2tq-3t^2q+t^3q: E_s(xi_q) = s(s-1)(s-2)q; E_3(xi_u) = 6u | F4c |
| with points 1, 2: pullback = hlift + span(xi_u, xi_w), dim 3 vs 1; no theta != 1 preserves it | F4b, F4d (p = 5, 7, both H) |
| three points: pullback = hlift | F4a |
| rem:fewer-points (k = 1, 2, 3) | F4e: all 1901 subalgebras over F_5. Filiform, k = 2: C4h in `check_two_points_all.out` (all subalgebras, p = 5, 7). |
| \|Aut(L)\| = \|GL_2\| p^6 | F5a (exhaustive over images of x, y); GAP: 7500000 |
| action on the centre is det(A) A; a scalar iff A = aI, and then a^3 | F5b, F5c |
| no torus element x->ax, y->by except the identity preserves h | F5e |
| graded automorphisms preserving h: x->x, y->y+beta x; unipotent on the centre | F5f (5 of the 480) |
| phi(x) = v, phi(y) = y is an automorphism with z -> z-w | F5g |
| psi_theta formula; preserves h; central scalar theta^3 | F5h (`verify_free_rerun.out`) |
| Stab(h) acts on the centre by every cube | F5d (\|Stab\| = 10000 for H, 300000 for H'); GAP agrees (same orders, scalars [1..4]) |
| over F_5 the stabilizer of every subgroup acts by every cube | F5j (`verify_free.out`) |
| automorphisms preserving every line F_p(x+c), c in gamma_2, fix the centre | proof in text; F5i (joint stabilizer of order 25, one matrix on the centre = identity); GAP: \|S\| = 25, acts trivially on Z(G) |
| same for the p^2 conjugates of H; lines F_p(v+q), q central: only ±1 | F5i: conjugates give 25 automorphisms, scalar [1]; central-coordinate family gives 250 automorphisms, scalars [1, 4] = ±1 |
| stage 3: Z_3 = span(t3u,t3w), K_3 = 0, labels uniform on F_p^2 | F6e; exact uniform law: `run_sim_free_5.out` stage 3, \|K^perp\| = 25, `law_exact_uniform=True` |
| minimum arity at stage 3: 3 at p = 5; 6 at p = 7 (5-label counterexample); CW gives 7 | F6d (exhaustive DFS over all label multisets) |
| B_3(2) = 729^2 = 531441, B_2(3) = 32^2 = 1024, Q_q = 2^33.19 at tau = 1 | F6a, F6b |
| A^(2) brackets; Z_2 central in A^(2), t^2z not central in A | F6g, F1e |
| stage 2: K_2 = 0, labels uniform on F_p^3; 6 labels eps_i, -nu eps_i fail; 7 suffice | F6e, F6c; `run_sim` stage 2, \|K^perp\| = 125 |
| grade one: samples uniform on {y_x+y_z+y_u = 0}; image of H in G/[G,G] is F_p x | F6h; `run_sim` recovered [[1,0,1,1,0]] |
| simulator at p = 5: recovers F_p v, label laws exactly uniform, every intermediate source exactly rho_{H_d} | `run_sim_free_5.out` (arities 3 and 7, 9 trees, 567 queries) |
| H' = exp(F_p(z+u)): not normal; hlift' = span(tc, t^2c); K_3 = 0; K_2 = F_p t^2c, labels in {lambda_z + lambda_u = 0} | F3a, F3b, F6f, F4b; `run_sim_free_5.out` (second run) |

## Caveats

* The claim that this group lies outside every prior family holds only as p grows. At fixed p,
  Friedl-Ivanyos-Magniez-Santha-Sen (bounded exponent) and Imran-Ivanyos (bounded p) cover it.
  This matches the paper's own Related Work wording.
* At p ≡ 1 mod 3, every automorphism of G that acts on the centre by a scalar acts by a cube
  (F5c). The dilations of the cover also act on the top grade by cubes θ^3, so this is not an
  obstacle. The obstacle is only that the automorphisms must preserve H and be public.
* The simulator uses brute-force witnesses at the Chevalley-Warning arity. It does not run the
  Ivanyos-Santha solver or B_d.
