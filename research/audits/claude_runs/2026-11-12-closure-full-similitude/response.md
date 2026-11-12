# Review: full GSp_n(F_ell) similitude-frame torsor as the arithmetic repair

Scope: I attack/prove the module identities, the Galois conventions, the disconnected-cover bookkeeping, and the polynomial overhead of running the already-reviewed one-component extraction on this torsor. I have no tools; costs of Couveignes / Lauder–Wan / Kozen / RR are inherited from the supplied notes and not re-verified here. The native construction of the frame scheme is NOT claimed; its equations, GSp-action and evaluation map are an assumed, charged input.

## 0. Fixed conventions (everything below depends on these)

- U = P^1 minus r points over F_q, pi: X -> U the family, L := J_fibre[ell] = R^1 pi_* mu_ell (Kummer), geometric monodromy Sp_n(F_ell), transvection inertia T_i at every puncture.
- Gamma := GSp_n(F_ell), lambda: Gamma -> F_ell^* the multiplier, Sp := ker lambda. N := F_ell^n with the natural LEFT action rho_N(g)v = gv. S := N^dual, rho_S(g) = rho_N(g^{-1})^T. Since g^T J g = lambda(g) J, one has S ≅ N ⊗ lambda^{-1} as Gamma-modules (via J); S|_Sp ≅ N|_Sp.
- Frame scheme Ũ -> U: points (c, zeta), c: N -> L_t iso with e(cu,cv) = zeta^{u^T J v}, zeta primitive. RIGHT action (c,zeta)·g := (c∘g, zeta^{lambda(g)}); check: e(cgu, cgv) = zeta^{(gu)^T J (gv)} = (zeta^{lambda(g)})^{u^T J v}. Write R_g for this automorphism.
- chi: Gal(F_qbar/F_q) -> F_ell^* mod-ell cyclotomic character, chi(sigma_q) = q; sigma_q the ARITHMETIC Frobenius. On F_qbar-points it coincides with the q-power Frobenius endomorphism, i.e. with what the extraction note computes on divisors ("F_q(D)").
- d := order of q in F_ell^*. Geometric components Ũ_zeta (zeta primitive, ell-1 of them), each an Sp-torsor over U_bar; C_zeta their compactifications; C_full their disjoint union; V := H^1(C_full,bar, mu_ell) = ⊕_zeta J_{C_zeta}[ell]; V_0 := J_{C_{zeta0}}[ell].
- Cohomology actions: pullback A(g) := R_g^* is a LEFT action on H^1(Ũ_bar, F_ell) and on V (because R_{gh} = R_h ∘ R_g). Pushforward on divisors P(g) := (R_g)_* = A(g)^{-1} = A(g^{-1}) is a RIGHT action. A(g) maps V_{zeta^{lambda(g)}} -> V_zeta; P(g) maps V_zeta -> V_{zeta^{lambda(g)}}.

## 1. Proved statements

### P1. The constant Gamma-action is F_q-rational and commutes with Frobenius; the arithmetic image does not restrict it.
sigma_q acts on F_qbar-points of Ũ by sigma·(c,zeta) = (sigma_L ∘ c, zeta^q) (c is a map out of the constant group N, on which Galois acts trivially; the pairing is Galois-equivariant so the new root is zeta^q). Then sigma·((c,zeta)·g) = (sigma c g, zeta^{q lambda(g)}) = (sigma·(c,zeta))·g. So every R_g is defined over F_q and commutes with sigma_q. The arithmetic monodromy image is Gamma_q := lambda^{-1}(<q>), of index (ell-1)/d in Gamma; it only controls the F_q-connected components (Frobenius orbits of the zeta's, each of size d, each geometric component defined over F_{q^d} = F_q(mu_ell)). The simply transitive Gamma-action on fibres is a property of the torsor, not of the monodromy image. Answer to "does arithmetic image smaller than GSp prevent full torsor action": NO.

### P2. L = Ũ ×^Gamma N with N CONSTANT over F_q (this is the exact content of "A = I").
Evaluation (c,zeta; v) -> c(v) descends to Ũ ×^Gamma N -> L (since (cg, zeta^{lambda(g)}; g^{-1}v) -> c(v)), is bijective on stalks (c is an isomorphism), and is Galois-equivariant: sigma(c(v)) = (sigma_L∘c)(v) with v fixed, which is exactly the point sigma·(c,zeta) evaluated at the SAME v. Hence Galois acts trivially on the coefficient module N. No intertwiner A has to be chosen; no scalar, no sign. (Contrast: a single component Ũ_{zeta0} with an abstract identification of its deck group with Sp only determines L up to a twist by Hom(Gal, Z(Sp)) = ±1 and, when d>1, up to the coset choice that produced the old A. The genuine frame scheme with evaluation kills both; the full torsor additionally makes the d>1 case canonical, see P6.)

### P3. Hochschild–Serre on the DISCONNECTED torsor; permutation modules do not break it.
For the finite étale Gamma-torsor Ũ_bar -> U_bar (connectedness of Ũ_bar is not needed; Cartan–Leray), with L = Ũ ×^Gamma N:
 E_2^{p,q} = H^p(Gamma, H^q(Ũ_bar, F_ell) ⊗ N) => H^{p+q}(U_bar, L),
Gamma acting on H^q by A(g) and on N by rho_N(g) (diagonal; sign of the action checked on H^0: invariant sections are f with f(x·g) = g^{-1}f(x), i.e. invariants of g: f -> rho_N(g) R_g^* f).
The components form the transitive Gamma-set Gamma/Sp (stabilizer of a component under R is lambda^{-1}(1) = Sp). Hence
 H^0(Ũ_bar, F_ell) ≅ Ind_Sp^Gamma F_ell, H^1(Ũ_bar, F_ell) ≅ Ind_Sp^Gamma H^1(Ũ_{zeta0}, F_ell).
Projection formula (finite index): Ind_Sp^Gamma F_ell ⊗ N ≅ Ind_Sp^Gamma(N|_Sp). Shapiro: E_2^{p,0} = H^p(Sp, N). Since -I is central in Sp of order 2 (invertible mod ell, ell odd) and acts on N by -1: H^q({±I}, N) = 0 for all q (averaging over a group of order TWO — not Maschke over Gamma), and the Z -> Sp -> Sp/Z spectral sequence gives H^p(Sp, N) = 0 for all p. So E_2^{1,0} = E_2^{2,0} = 0 and the edge map is an isomorphism
 H^1(U_bar, L) ≅ E_2^{0,1} = (H^1(Ũ_bar, F_ell) ⊗ N)^Gamma = Hom_Gamma(S, H^1(Ũ_bar, F_ell)). (I)
Galois-equivariant: sigma_q acts on Ũ_bar commuting with Gamma (P1) and trivially on N (P2), and the spectral sequence is functorial. Answer: the H^0 permutation modules contribute exactly H^p(Sp, N) = 0; nothing breaks. (No exactness of Hom_Gamma or of Ind is used anywhere; only the identifications.)

### P4. Open = compact for the Gamma-Hom.
Restriction H^1(C_full,bar, F_ell) -> H^1(Ũ_bar, F_ell) is componentwise, injective, Gamma- and Galois-equivariant. By Shapiro both Hom_Gamma(S, ·) sides reduce to Hom_Sp(S|_Sp, H^1(C_{zeta0})) -> Hom_Sp(S|_Sp, H^1(Ũ_{zeta0})), and the supplied review's lemma (A) (norm N_i = 1 + T_i + ... + T_i^{ell-1} = 0 for transvections, H^1(Sp,N) = H^2(Sp,N) = 0) shows this is an isomorphism. Hence
 W_F := Hom_Gamma(S, H^1(C_full,bar, F_ell)) ≅ H^1(U_bar, L), dim = (r-2)n = m. (II)
This is OPEN cohomology; the parabolic part H^1(P^1, j_*L) (dim r-2n) is the kernel of the residue map to ⊕_i N/(T_i - 1)N and must still be filtered separately — as the task states.

### P5. Exact identity of the mu_ell-coefficient output and the twist table.
Gamma acts trivially on mu_ell, so V = H^1(C_full,bar, F_ell) ⊗ mu_ell and
 W := Hom_Gamma(S, V) = W_F ⊗ mu_ell ≅ H^1(U_bar, L)(1) as Galois modules. (III)
The rank-one local system attached to lambda^k via the torsor is mu_ell^{⊗k} (sections (zeta, a) -> zeta^a; Galois: zeta -> zeta^q), so Hom_Gamma(S ⊗ lambda^k, ·) shifts the twist by k. Table (all for ARITHMETIC sigma_q; geometric Frobenius is the inverse matrix):
- Hom_Gamma(N^dual, J_{C_full}[ell]) = H^1(U_bar, L)(1): Frob_{H^1(U,L)} = q^{-1} · Frob_W. (the proposal's convention)
- Hom_Gamma(N, J_{C_full}[ell]) = H^1(U_bar, L)(-1)(1) = H^1(U_bar, L): no twist.
- Hom_Gamma(N^dual, H^1(C_full,bar, F_ell)) = H^1(U_bar, L): no twist.
- For L' = R^1 pi_* F_ell = L(-1): H^1(U_bar, L') = q^{-2} · Frob_W in the proposal's convention.
Every twist is by an explicit power of chi; none is unknown. Answer to "do dual/Tate conventions reintroduce an unknown scalar": NO, provided S and the coefficient sheaf are declared; an UNDECLARED swap of N vs N^dual is an error of exactly one factor q, which is NOT detectable by dimension or by W-preservation (both choices give m-dimensional, Frobenius-stable spaces). Declare it.

### P6. Shapiro transport to one component, and independence of the lifting element.
V ≅ Ind_Sp^Gamma V_0 (transitive Gamma-set with stabilizer Sp), so phi -> phi_1 := pr_{zeta0} ∘ phi is an isomorphism W -> W_0 := Hom_Sp(S|_Sp, V_0). The other components are recovered by phi(s)_{zeta0^a} = A(g_a)^{-1} phi_1(g_a s) for any g_a with lambda(g_a) = a. Transporting post-composition by sigma_q (which maps V_{zeta} -> V_{zeta^q}) gives, for ANY g_q in Gamma with lambda(g_q) = q,
 (sigma_W phi)_1 = A(g_q) ∘ sigma_q ∘ phi_1 ∘ rho_S(g_q^{-1}) = P(g_q^{-1}) ∘ sigma_q ∘ phi_1 ∘ rho_N(g_q)^T. (IV)
Replacing g_q by h g_q (h in Sp, including h = -I) changes A(g_q) by A(h) and rho_S(g_q^{-1}) by rho_S(h^{-1}); Sp-equivariance of phi_1 and [A(h), sigma_q] = 0 cancel these. So (IV) is independent of the choice: the old "A up to scalar / sign" ambiguity does not exist here. (The old residual sign was an artifact of treating "F_q on a component" as a fixed operator; on a component defined only over F_{q^d} there is no such operator, only the pair (sigma_q, g_q).)

### P7. Multidegree is automatic.
Pic(C_full)[ell] = ⊕ J_{C_zeta}[ell]: a class with ell·D ~ 0 has ell·deg_zeta(D) = 0 for each component, so deg_zeta D = 0. Verified ell-torsion needs no separate per-component degree constraint. With the Shapiro implementation all divisor arithmetic lives on component zeta0 anyway.

### P8. Intertwiner equations in pushforward matrices (contravariance check).
phi_1 in W_0 iff phi_1 ∘ rho_S(g) = A(g) ∘ phi_1 for g in Sp iff
 phi_1 · rho_N(g)^T = P(g) · phi_1 for a generating set of Sp. (V)
Both sides of (V) are anti-homomorphic in g, so generators suffice. Using rho_N(g^{-1})^T with P(g) (i.e. mixing a left and a right convention) is WRONG: it forces A(gh)phi = A(hg)phi, so the image lies in V_0^{[Sp,Sp]} and the true W_0 is lost; on a generating set alone it yields an unrelated subspace. This is a checkable obligation, not a cosmetic one.

## 2. End-to-end procedure on this torsor (polynomial overhead)

Input (assumed, charged): F_q-model of the frame scheme with R_g for generators of Gamma and the zeta-coordinate; the evaluation map is used only to JUSTIFY P2, not in the computation.

1. Factor Phi_ell over F_q: (ell-1)/d factors of degree d; an F_q-component of Ũ is the fibre over one factor; the geometric component C_0 := C_{zeta0} is that scheme viewed over F_{q^d} = F_q[zeta]/(factor). Certify geometric irreducibility of C_0 by computing the constant field of its function field (must equal F_{q^d}) — this is the only place the "full Sp monodromy" promise enters computationally. Degree over P^1: |Sp_n(F_ell)| <= ell^{n(n+1)/2}; genus g = O(r |Sp|) by Riemann–Hurwitz; both poly(ell) at fixed n, r.
2. Compactify/normalize C_0 (Kozen), Lauder–Wan zeta of C_0 over F_{q^d}: poly(deg, NUMERICAL P, d log q). All other components are sigma^i-conjugates of this model (same zeta); no second zeta computation.
3. Choose O: one closed place on C_0 over a regular fibre, residue degree <= |Sp| over F_{q^d}; k0 = F_{q^b} with d | b, b <= d·|Sp| (deck maps already over F_q, so no deck-field factor). F0 := sigma^b preserves every component since d | b, commutes with Gamma, and q^b ≡ 1 mod ell, so Weil duality on V_0 is lambda -> lambda^{-1} (same irreducible degree).
4. On V_0 (dim 2g): factor chi_{F0}, a(X) = product of all irreducible factors of degree <= m with multiplicity, V_small,0 = ker a(F0), nondegenerate pairing by the orthogonality of generalized eigenspaces lambda, mu with lambda·mu ≠ 1. H = ell^{ceil(log_ell 2g)} · prod_{j<=m}(ell^j - 1) (the task's "2·sum genera" is a safe overestimate; per component 2g suffices). Since ell-1 | H, d | H and mu_ell ⊂ K := F_{q^{bH}}. bH = poly(ell) with fixed exponent <= 1 + n(n+1) + m(m+1)/2 + O(1).
5. Couveignes over K on C_0 with the computed zeta and O; CRT-project to V_small,0; pairing-rank certificate = dim V_small,0; basis by a nonsingular pairing minor. Unchanged from the reviewed note.
6. Solve (V) for Sp generators: W_0, check dim = m. E_0 = S ⊗ W_0 embedded by evaluation (injective: S absolutely simple, End = F_ell; no averaging).
7. Frobenius: fix one g_q with lambda(g_q) = q (any; P6). For each basis element phi_1^{(k)} and each basis vector e_j of S, compute the divisor class P(g_q^{-1})(sigma_q(phi_1^{(k)}(rho_N(g_q)^T e_j))): sigma_q = q-power on ideal coordinates (lands on the conjugate model f^{sigma}), then the F_q-rational deck map R_{g_q^{-1}} (lands back on C_0; verify on O that the zeta-coordinate returns to zeta0 — this certifies lambda(g_q) = q and not q^{-1}). The result lies in V_small,0 because A(g_q)sigma_q commutes with F0; take pairing coordinates; express in the W_0 basis. Certify sigma_W(W_0) ⊂ W_0. Output the m×m matrix Frob_W(sigma_q) and the twist table of P5.

Overhead versus the reviewed single-component extraction: a factor d <= ell-1 inside every field degree (log-size terms only), one component instead of ell-1 (the rest are formal conjugates), one additional F_q-rational deck-map application per Frobenius entry (n·m applications). No lcm, no compositum, no full torsion splitting, no dependence of the field on the (ell-1)/d orbit structure. Total: poly_{n,r}(ell, NUMERICAL P, presented size, log(1/eta)) — same shape as before. NOT poly(log P).

## 3. The four requested obstruction tests

- Arithmetic image < GSp: no obstruction (P1). Only connectedness over F_q changes.
- H^0(C_full) permutation modules: no obstruction (P3); they contribute H^p(Sp, N) = 0 for p = 1, 2.
- Dual/Tate conventions: no unknown scalar (P2, P5, P6); only declared twists by chi. The old sign/scalar ambiguity is proved absent in (IV).
- Disconnected RR: no hidden lcm/compositum (P7 + step 3); the single enlargement is d | b.

I found no decisive obstruction to the module/Frobenius identification. The construction as formulated is correct conditional on the assumptions listed next.

## 4. Assumptions, proof obligations, falsifiers

Assumptions (charged inputs, not proved here):
A1. The presented frame scheme is literally Isom-with-pairing over F_q with the F_q-rational action (c,zeta)·g = (cg, zeta^{lambda(g)}) and the evaluation map. P2 is an identity about THIS scheme; an abstract cover "isomorphic to it" with geometric-link advice is not sufficient (sign twist possible).
A2. Geometric monodromy = Sp_n(F_ell), all inertia nontrivial transvections (used in P3/P4 via H^p(Sp,N) = 0 and norm-zero). Not certified by the algorithm beyond the constant-field check and dim W_0 = m.
A3. The reviewed single-component extraction (Couveignes/Lauder–Wan/Kozen/RR costs and the pairing-rank certificate) holds over F_{q^d} as base. I cannot re-audit those sources here.

Obligations to discharge in writing before use:
O1. Declare S (N vs N^dual) and the coefficient sheaf; apply the twist table. (A silent swap = factor q, undetectable by any stability test.)
O2. Use (V) with pushforward matrices (or rho_S with pullback matrices); never mix.
O3. Use rho_S(g_q^{-1}) = rho_N(g_q)^T on the S side of (IV); the mixed-up operator A(g_q)sigma phi_1 rho_S(g_q) fails to preserve W_0 unless g_q^2 is central — so the preservation certificate catches it generically but not when q is a square represented by a scalar g_q; the convention must be PROVED (it is, in P6), not tested.
O4. Check lambda(g_q) = q by the zeta-coordinate of R_{g_q^{-1}}(sigma(O)) (decisive when q^2 ≢ 1 mod ell).

Falsifiers (cheap, exact; any failure refutes the pipeline, success proves nothing beyond consistency):
F1. dim Hom_Sp(S, V_small,0) ≠ (r-2)n with pairing rank = u certified.
F2. sigma_W(W_0) ⊄ W_0, or (sigma_W)^d computed by iterating (IV) ≠ the direct sigma^d action on W_0 (sigma^d preserves C_0 and needs no g).
F3. Characteristic polynomial of q^{-1}·Frob_W restricted to the (separately filtered) parabolic subspace not closed under lambda -> lambda^{-1} (Poincaré duality H^1(P^1,j_*L)⊗H^1(P^1,j_*L) -> H^2(P^1, mu_ell) = F_ell with trivial action); this tests the twist convention only on the parabolic part and only if that multiset is not accidentally symmetric.
F4. Constant field of the F_{q^d}-component model strictly larger than F_{q^d} (promise A2 false).

## 5. What is and is not established

PROVED (under A1–A3): W = Hom_Gamma(N^dual, H^1(C_full,bar, mu_ell)) ≅ H^1(U_bar, L)(1) as Gal(F_qbar/F_q)-modules, dim m = (r-2)n; the constant Gamma-torsor action is F_q-rational and Frobenius-commuting irrespective of the arithmetic image; the H^0 permutation terms vanish in Hochschild–Serre; the Frobenius on W is computable on one geometric component by (IV) with no scalar/sign ambiguity; the extraction runs with poly(ell) overhead over one field F_{q^{bH}}, d | b.
ASSUMED: genuine presented frame scheme, full-Sp/transvection promise, inherited subroutine costs.
NOT CLAIMED: native construction of the frame scheme, parabolic filtering (separate, still needed since W is open cohomology), characteristic-zero lifting, uniform heights, full point counting, poly(log P) complexity, any hardness or quantum speedup. No finite example was used as evidence; the Legendre data in the supplied review would serve only as a mechanical consistency check of F1/F2 at ell = 3, q ≡ 2 mod 3 (d = 2).