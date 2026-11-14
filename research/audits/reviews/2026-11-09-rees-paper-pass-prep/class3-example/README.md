# Class-three worked example (filiform n4): claims and checks

Drop-in text: `example.tex` (`\subsection{Example: a Class-Three Group}`,
`\label{sec:example-class3}`, about 1.2 pages; the end of the file has, in comments, a
3-sentence version for the end of the "Why interpolation works" paragraph of Section 1.3).
It was compiled in a scratch copy of `core/main-core.tex`, inserted just before
`\section{Black-Box Groups and Other Presentations}`: 39 pp., no undefined references, no new
overfull boxes. The core paper itself was NOT edited.

Scripts (run with `nice -n 19 /opt/anaconda3/bin/python`, from this folder):

| script | output | what |
|---|---|---|
| `verify_class3.py` | `verify_class3.out` | 91 tagged checks [C1]-[C6], p = 5 and 7 (about 7 min); `FAILURES: none` |
| `check_two_points_all.py` | `check_two_points_all.out` | [C4h], every subalgebra, p = 5, 7 |
| `run_sim.py 5`, `run_sim.py 7` | `run_sim_5.out`, `run_sim_7.out`, `run_sim_*.json` | full descent with `theorems/rees_end_to_end_sim.py` (ExactBackend), 2 seeds per H |
| `gap_aut_make.py` → `gap_aut_p5.g`, `gap_aut_p7.g` | `gap_aut_p5.out`, `gap_aut_p7.out` | GAP 4.15 + autpgrp on the group G itself (permutation group by right BCH multiplication) |

## Claim → check

| claim in `example.tex` | check |
|---|---|
| gamma_2 = span(x3,x4), gamma_3 = Z(L) = F_p x4; Jacobi | C1c, C1e |
| cover basis X_i, Y_3, Y_4, W; brackets [X1,X2]=Y3, [X1,X3]=Y4, [X1,Y3]=W (= polynomial bracket of L[t] restricted to A) | C1a, C1b |
| A has class 3; centre span(X4, Y4, W) | C1f, C1d |
| E_s formula; E_s Lie hom, delta_theta Lie aut, E_s o delta_theta = E_{theta s} | C1g |
| E_s and delta_theta are homomorphisms for the class-3 BCH product (x*y = x+y+1/2[x,y]+1/12([x,[x,y]]+[y,[y,x]])) | C2a, C2b symbolic over Q (only denominators 2, 12, so valid for p > 3); C2c associativity; C2d 20000 random pairs mod 5, 7 |
| H = exp(F_p v), v = x1+x2+x3+x4: subalgebra, f hides H | C3a, C3c |
| non-normal, order p | `run_sim_*.out` flags (normal=False, order=p); [x2,v] = -x3 by hand |
| hlift = F_p(X1+X2+X3+X4) | C3b (from the definition sum_k t^k (h cap gamma_k)) |
| tuple-oracle fibres = left cosets a*exp(hlift) | C3d: ALL 78125 points (p=5) and ALL 823543 points (p=7): 15625 / 117649 fibres of size p; also `run_sim` (fibres=15625, lifted_order=5 at p=5) |
| u = 2X4-3Y4+W: E_s(u) = s(s-1)(s-2)x4, E_1(u)=E_2(u)=0, E_3(u)=6x4 not in h | C4d |
| with points 1,2 only: pullback = exp(hlift + F_p u) | C4c (p^2 points of the p^7); two-point oracle fibres have size p^2 (printed after C3d) |
| E_1(delta_theta u) = theta(theta-1)(theta-2)x4; only theta = 1 preserves the two-point pullback | C4e, C4f |
| for every H: points 1,2 give hlift + F_p u if x4 not in h, hlift if x4 in h; they suffice iff gamma_3 in h | C4h (all 220 subalgebras over F_5, all 516 over F_7; dilations theta != 1 preserve P_12 iff x4 in h) |
| three points: pullback = hlift = intersection over all s in F_p^x | C4a, C4b |
| |Aut(L)| = (p-1)^2 p^5, acts on centre by every scalar | C5a, C5b, C5b2 (exhaustive over images of x1, x2); GAP on G: 50000, 605052, scalars all of F_p^x |
| only the identity of the torus diag(a,b,ab,a^2b) preserves h | C5d |
| phi(x1) = v is an automorphism; psi_theta = phi delta_theta phi^-1 has the displayed formula, preserves h, scales x4 by theta^3 | C5e |
| stabilizer of h acts on the centre by all of F_p^x | C5c (|Stab| = 400 at p=5, 1764 at p=7); GAP agrees (same orders, same scalars) |
| over F_5, F_7 the stabilizer of EVERY subgroup acts on the centre by all of F_p^x | C5f (p=5: direct, all 220 subalgebras; p=7: every one of 516 is Aut-conjugate to one of 12 coordinate subalgebras, which the 2-torus preserves) |
| automorphisms preserving every line F_p(x1+x2+w), w in gamma_2, fix the centre | proof in text; C5h (5 resp. 7 such automorphisms, scalar 1 only); GAP joint stabilizer: order 5 resp. 7, scalars [1] |
| stage 3: Z_3 = F_p W, K_3 = 0, labels uniform on F_p | C6g (support); exact uniform law: `run_sim` stage 3 `law_exact_uniform=True`, |K_3^perp| = p |
| Chevalley-Warning: 4 labels; exact minimum 3 at p=7, 2 at p=5; s1^3+2s2^3=0 only trivial at p=7 | C6c, C6e (exhaustive over all label tuples) |
| B_3(1) = 216^2 = 46656 | C6a |
| Lemma bezout at p=5, d=3 (kappa=1) | C6f |
| stage 2: A^(2) brackets; Z_2 = span(Y3,Y4) central in A^(2) (Y3 not central in A) | C6i, C1d |
| K_2 = 0, labels uniform on F_p^2 | C6g; `run_sim` stage 2 |K_2^perp| = p^2, law exact |
| 5 labels suffice (CW); (1,0),(-nu,0),(0,1),(0,-nu) fail for nonsquare nu | C6d (nu = 2 at p=5, nu = -1 at p=7); the argument is one line for every odd p |
| B_2(2) = 18^2 = 324 | C6a |
| grade one: samples uniform on {y : y1+y2+y3+y4 = 0}; null space = F_p v | C6j; `run_sim` recovered basis [[1,1,1,1]] |
| Q_q = 3(4+tau) 324 46656 = 226,748,160 = 2^27.7565 at tau = 1 (Table 1 row) | C6b |
| simulator recovers F_p v at p = 5, 7, label laws exactly uniform on K_d^perp, every intermediate source exactly rho_{H_d} | `run_sim_5.out`, `run_sim_7.out`: `ALL RUNS OK: True` (4 runs each; arities 2/4 at stage 3, 5 at stage 2, i.e. kappa_d g_d + 1, not B_d) |
| centre: hlift = span(X4,Y4,W); stage-3 labels all 0; K_2 = F_p Y4, labels in F_p(1,0); t h = F_p X4 | C3b, C3d, C4g, C6h; `run_sim` (|K_3^perp| = 1, |K_2^perp| = p, recovered [[0,0,0,1]]) |

## Choice of H (why this line)

* H must avoid x4 (otherwise two points suffice, C4h).
* Subalgebras inside the abelian ideal V = span(x2,x3,x4) are a poor example: the public map
  tau_b = diag(1,b,b,b) is an automorphism (C5i) preserving every subspace of V and scaling the
  centre by b. A first draft used h = span(x2+x4, x3+x4); C5d then showed tau_b preserves it, so
  it was dropped.
* In n4 every subalgebra not inside V and not containing x4 is a line F_p v with v1 != 0. The line
  v = x1+x2+x3+x4 has no torus symmetry (C5d).

## Caveats

* This instance is not new territory. n4 is F_p ⋉ F_p^3, and H is a subgroup of order p outside
  F_p^3, so it is in the family of Bacon-Childs-van Dam and Ivanyos-Santha Cor. 8. The example
  only illustrates the mechanism.
* For n4, obstacle (2) concerns whether the automorphisms are public, not whether they exist.
  Every subgroup has automorphisms that preserve it and scale the centre (C5f).
* The simulator uses brute-force solutions at the Chevalley-Warning arity. It does not run the
  Ivanyos-Santha solver or B_d.
