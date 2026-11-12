# Gaudin low-locality joint-generator test: the at-most-3-site hypothesis is falsified at N=4, M=2

## Verdict

**The hypothesis is false at N=4, M=2, for every set of distinct sites.**

- **Already falsified, independent of g=1/3.** Every path [0,G] contains small g>0. For each such g, the unique admissible real generator has a nonzero matrix element between complementary basis states. No operator supported on at most 3 sites has such an element.
- **Not yet established: the sign or vanishing of that element exactly at g=1/3.** I could not settle this analytically. It is a 15-unknown exact rational solve, specified in section 4.
- **Status of the arithmetic.** It is hand-derived, and the general formula was proved symbolically. A cheap exact CAS recheck is still owed.

## 1. Gauge reduction (deductions; they hold whenever the joint spectrum is simple in the sector)

**(a) The admissible generator is unique.** The condition [Q_j, V_i−[K,Q_i]]=0 for all i,j says that V_i−[K,Q_i] commutes with every charge. With simple joint spectrum this forces K's off-diagonal part, in the joint eigenbasis, to equal that of K* = Σ_branches ψ′ψᵀ. Here ψ are the real normalized joint eigenvectors and K* is real antisymmetric. Then V_i−[K*,Q_i] = Σ q′_{vi}P_v.

**(b) Gauge freedoms do not help.**
- Let K be any generator, not necessarily anti-Hermitian or real. Re K = K* + D_r and Im K = D_i, where D_r and D_i are in the commutant. The commutant consists of functions of the Q's, which are real symmetric.
- Taking transposes preserves operator support. Therefore K local implies that the antisymmetric part of Re K, which is K*, is local.
- Branch phases e^{iφ_v} only add i·Σφ′_v P_v, which lies in the commutant.
- Commuting additions to a real antisymmetric K are zero.

**(c) Sector restriction is enough.** The charges are block-diagonal in M. So only K's (M=2 → M=2) block enters the M=2 conditions. Components that change M, or act in other sectors, are irrelevant.

**(d) Support lemma (exact).** An operator supported on a site set T has ⟨w|O|v⟩=0 unless w and v agree outside T. In the M=2 sector at N=4, complementary pairs {12|34}, {13|24}, {14|23} differ on all 4 sites. So every operator on at most 3 sites has zero complementary elements there, with no Hermiticity or M-preservation assumption.

**Conversely**, span{C_ab, Z_c C_ab} restricted to M=2 realizes all 12 single-hop elements independently. On the relevant subspace Z_d = −Z_c, so C_ab ± Z_c C_ab select the spectator. This gives an exact criterion:

> At N=4, M=2, sector-restricted, a K on at most 3 sites exists at g ⇔ the three complementary elements of K*(g) vanish.

## 2. Coefficient equations

Use H = Σ_i ε_i Q_i = E + gτ (constant dropped). Here:
- E = diag(e_S), with e_S = Σ_{i∈S} ε_i.
- τ = T/2, and T is the adjacency matrix of the Johnson graph J(N,M).
- dH/dg = const + τ, because Σ_i ε_i(P_ij−I)-terms reduce to ½Σ_{i<j}(P_ij−I), whose diagonal is constant in a fixed sector.

When H is simple in the sector, the joint condition is equivalent to

  **[H,[H,K]] = [τ,E]** (antisymmetric K, 15 unknowns at N=4, M=2).

Expand K = K0 + gK1 + g²K2 + …. Write CN(m,n) for the common neighbours of states m and n.

- **K0:** K0_mn = τ_mn/(e_n−e_m). This is 2-local. Note [E,K0] = −τ.
- **K1:** K1_mn = [τ,K0]_mn/(e_n−e_m). For adjacent m,n:
  [τ,K0]_mn = ¼ Σ_{t∈CN(m,n)} [1/(e_n−e_t) + 1/(e_m−e_t)].
- **Order g¹ complementary elements cancel identically.** Each element reduces to Σ_{x∈v,y∈w}[1/(ε_x−ε_y) + 1/(ε_y−ε_x)] = 0. So the obstruction first appears at g².
- **Complementary element (w = v^c), with Δ = e_w−e_v and u over the 4 middle states:**
  Δ²K2_wv + ½Σ_u[(e_w+e_u−2e_v)K1_uv + (e_u+e_v−2e_w)K1_wu] + ½Σ_u(K0_uv+K0_wu) = 0.
  The term τK0τ drops out by antisymmetry over the middle states.

**Symbolic solution.** Let v={a,b} and w={c,d}, with
- p=a−c, q=a−d, r=b−c, s=b−d,
- κ=c−d, λ=a−b,
- Π=pqrs = Π_{x∈v,y∈w}(ε_x−ε_y).

The constraint p+s = q+r = −Δ holds. The key identity is κ²+λ²+2ps+2qr = Δ². Substituting gives

  **⟨w|K*|v⟩ = −(3/4)·(e_w−e_v)/Π · g² + O(g⁴).**

The absence of a g³ term is a deduction from the complement symmetry, which exists because M=N−M. Complementation C satisfies C·H(g)·C = Σε − H(−g). This gives K(−g) = −C K(g) C, so complementary elements are even in g.

**At least two of the three complementary pairs have a nonzero coefficient for any distinct sites.** If e_v = e_{v^c} held for all three pairs, then b=c, a contradiction. The formula has only site-difference denominators, so by continuity it also holds where E is accidentally degenerate.

## 3. Exact certificate for ε=(0,1,3,7)

Pair sums: e(12)=1, e(34)=10, e(13)=3, e(24)=8, e(14)=7, e(23)=4. These are distinct, so H is simple near g=0.

The g² coefficients of ⟨w|K*|v⟩:

| v → w | Δ | Π | g² coefficient |
|---|---|---|---|
| 12 → 34 | 9 | 252 | **−3/112** |
| 13 → 24 | 5 | −56 | **15/224** |
| 14 → 23 | −3 | 72 | **1/32** |

**Independent check of the first entry.** I evaluated it directly from the explicit K1 entries: 7/32, −3/112, 13/224, −1/112 for (C,D,E,F → A) and 3/112, −7/32, 1/112, −13/224 for (B → C,D,E,F). The sum is 81·K2 = −243/112, giving −3/112.

**Second instance.** ε=(0,2,3,7) gives −2/35 by direct evaluation, matching the formula.

**What this proves.** Each complementary element is real-analytic in g wherever the joint spectrum is simple, and it is not identically zero. Therefore:
- no K on at most 3 sites exists for any g in (0, g_*), and
- elsewhere, existence can hold only at isolated values of g.

## 4. What is still unpaid at g=1/3

The perturbative radius is not certified: ‖gτ‖ = 2/3 exceeds half the minimum gap of E, which is 1/2. Exact recipe:

1. Basis (12, 34, 13, 24, 14, 23).
2. H = diag(1,10,3,8,7,4) + T/6, where T has 1 everywhere except the diagonal and complementary pairs.
3. Certify that H is simple using the discriminant or a Sturm sequence. If it is not simple, use Σ c_i Q_i instead.
4. Solve [H,[H,K]] = [τ,E] over ℚ.
5. Report K_{34,12}, K_{24,13}, K_{23,14}. Any nonzero entry certifies failure at g=1/3. If all are zero, g=1/3 is an isolated exception, and the "always" hypothesis still fails.

## 5. Scope

**What this shows:**
- Only that an exact-transport generator supported on at most 3 sites fails.
- The hypothesis also fails for non-anti-Hermitian or complex K and arbitrary branch phases (section 1b).

**What this does not show:**
- **No preparation no-go.** At N=4, K* is just a 6×6 matrix.
- **Nothing about k-local generators for fixed k≥4.**
- **Nothing about polynomial-term non-local representations.** Examples are products like C_ab C_cd, or Gaudin-algebra or MPO forms.
- **Nothing about approximate counterdiabatic driving, other parameter paths, or the joint-dephasing route.**

**For growing N:** the support lemma generalizes, since a k-site operator has zero elements at Hamming distance >k. The order-g² double-hop element in J(N,M) gains spectator terms that do not appear at N=4, including CN size N−2 and K1 at Hamming distance 4. I did not derive these. Whether Hamming-2m elements first appear at order g^{2(m−1)} is speculation.

## 6. Next cheapest decisive falsifiers

1. **CAS recheck** of the identity κ²+λ²+2ps+2qr = Δ², and of K2 for both site sets above.
2. **The exact g=1/3 solve** from section 4.
3. **Bounded-support test at N=6, M=3.** Compute the leading nonzero order of ⟨456|K*|123⟩, which has Hamming distance 6. This tests whether any operator on at most 5 sites, or any pair-product ansatz, could survive. It is needed before claiming that the required support grows with N.