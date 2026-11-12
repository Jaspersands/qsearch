# Local Q2 ONE-HALF: whether a reachable coset can force superpolynomial Stoll loss for every representative

## Verdict

**No falsifier, and no unconditional bound.** I could not construct a native family f and reachable coset h for which every admissible representative forces superpolynomial Smith or monic-normalization loss. I also did not prove a full conditioning bound.

What I did prove is one exact calculation. Every coset of E=2L has the same Haar volume, 2^-(D0+g), and D0 is polynomial in the inputs. So the obstruction you asked for cannot be specific to a coset. It exists only if the loss superlevel set in J(Q2) has measure at least 2^-(D0+g) at a superpolynomial level.

The same identity gives an explicit randomized finite choice rule. It works only under two named obligations, (S) and (M) below, which remain open. ONE-HALF modulo E therefore stays **OPEN**.

## Inputs used and their status

The following come from the repository ledger. They are reviewed there; I did not re-derive them.

- **R1.** L is the closed Z2-span of the seeds P_i. These are given by t_i=2^N·i with N≥2, and they lie in the torsion-free formal group K2.
- **R2.** log: K2 → Q2^g is an injective homomorphism, because K2 is torsion-free. Its components satisfy d log_k = ω_k.
- **R3.** v2 det(L_k(t_i)) = D0 = Ng² + Σ_i v2(i) + Σ_{i<j} v2(j²−i²).

I checked the following myself from the stated series. In each L_k(t_i) term, v2(c_m)≥−2m, the denominator is odd, and the power t^(2(k+m)+1) contributes at least N(2(k+m)+1). The total valuation is therefore at least N(2k+1)+m(2N−2) ≥ N, so log L ⊂ 2^N Z2^g.

Each P_i is Q2-rational. The reason is that F(t_i²) ≡ 1 mod 16 (since v2(t_i²) ≥ 4), so its square root lies in Z2. No extension fields, charts or field types enter the algorithm below.

## The calculation

Let μ be Haar measure on G for the form |ω_0∧…∧ω_{g−1}|. Define the loss functional β: G → Z≥0∪{∞} by

β(P) = the infimum, over all admissible representation data at P, of the total ledger requirement M_out + (entry losses) + K(M_j) + 2K(B_j).

"Admissible representation data" means:
- a non-reduced Mumford pair (a,b) with deg a ≤ 2g+1;
- the Stoll identity [c−2hb−h²a, −b−ha]=[a,b] for any h;
- any choice of s with s² ≡ ε(a−a1f1) mod f.

Loss from computing s and from the label step is included in β. β is required to be Borel.

**Lemma (proved).** μ(L)=2^-D0 and μ(E)=2^-(D0+g). Moreover E ⊇ J_{D0+1} := L ∩ log^-1(2^(D0+1) Z2^g).

*Proof.*
1. log L is a subgroup of Z2^g of index 2^D0, so it contains 2^D0 Z2^g.
2. log is injective on L and has unit Jacobian with respect to ω, so change of variables gives μ(L) = Haar(log L) = 2^-D0.
3. L ≅ Z2^g, so [L:2L]=2^g. Translation invariance then gives μ(2L) = 2^-(D0+g).
4. Since log is an injective homomorphism, log(2L) = 2·log L ⊇ 2^(D0+1) Z2^g, hence J_{D0+1} ⊂ 2L. ∎

**Theorem (coset-volume transfer, proved).** For every h ∈ G and every K ≥ 0,

  μ({P∈h+E : β(P)≥K}) / μ(h+E) ≤ 2^(D0+g) · μ({P∈G : β(P)≥K}).

*Proof.* The numerator is at most μ{β≥K}, and the denominator is 2^-(D0+g) by the Lemma. ∎

**Corollary 1 (shape of any falsifier).** Suppose that for some native family (f_g, h_g), every P ∈ h_g+E has β(P) ≥ K_g. Then

  μ{β≥K_g} ≥ 2^-(D0+g).

In particular:
- **No small reachable coset.** Reachability of h is irrelevant beyond this volume, because every nonzero h has h+E ∩ J_{D0+1} = ∅ and the same measure.
- **What is excluded.** Measure-zero degeneracy loci, one representative, or a single unlucky Mumford chart cannot be falsifiers. These include W_{g−1}, branch or ∞ support, and proper rank-drop subvarieties. Their 2^-K tubes are also excluded unless those tubes have volume at least 2^-poly.
- **What a falsifier must produce.** It must give an open set of points with superpolynomial loss and volume at least 2^-(D0+g).

**Corollary 2 (conditional finite choice).** Suppose:

- **(S)** μ{β≥K} ≤ 2^(A−K/D) for all K, with A and D polynomial. Necessarily A ≥ log2 μ(G); the ledger's volume cover gives μ(G) ≤ 2^(3g+gM+2gN_c).
- **(L)** If β(P) ≤ K, then β(P') ≤ K+c for all P' ∈ P+J_{K+c'}.

Set K* = D(A+D0+g+σ) and R ≥ K*+c'. Then a sample P' = P + 2Σ n_i P_i, with n uniform in (Z/2^R)^g, has β(P') ≤ K*+c with probability at least 1−2^-σ.

Given that event, run Stoll at precision N ≥ K*+c+1. All nonzero Smith invariants are then visible below N, so by the accepted kernel lemma the exact rank decides j. The B_j bound pays normalization. This is Monte Carlo with failure probability 2^-σ, not a certified result.

**Why this obeys the contract.** The shift 2Σ n_i P_i lies exactly in E, so it is not an arbitrary Kummer-preserving shift. Any materialization error that stays inside J_{D0+1} is also an admissible E-shift.

**Why naive shifting is useless.** Stoll's composite trick halves [a1²a2] through [a2], and half(P+2e) = half(P)+e. So shifting changes nothing unless P' is genuinely recomputed as a reduced representative.

## Cheapest attack tried first

The seed-coset attack takes h = [P_1] ∈ L/E. Seeds have Kummer label zero, so this coset is reachable at the first step. Every representative of it lies in L ⊂ K2, so the whole coset is forced near the origin: its support points sit near ∞ and its Mumford coefficients are non-integral.

The attack fails at the group level. For P ∉ 2L we have log P ∉ 2^(D0+1) Z2^g, so the minimum coordinate valuation of log P is at most D0. Halves Q ∉ L+G[2] likewise satisfy Q ∉ J_{D0}+G[2]. Forced formal depth is therefore polynomial.

This does not bound β. A conversion lemma from depth to Mumford coefficients is still needed, because odd power sums of the t_i degenerate at t_i ≈ −t_j, which is the near-ι locus.

## Open obligations

1. **(S) for the actual β.**
   - *Proved template.* Let f be monic of degree n, E/Q2 of degree e, and μ(O_E)=1. If v2(f(x)) ≥ K, some root α has v2(x−α) ≥ K/n. Hence μ{x∈O_E : v2(f(x)) ≥ K} ≤ n·2^(−eK/n).
   - *Still needed.* Similar bounds for Smith minors of M_j and B_j and for the computation of s, uniformly over the scaled Hensel and ∞ charts of the volume cover. The scales there are A0=D+2 and N_c, with D=v2 disc f.
   - *Falsifier.* A native family with μ{β≥K_g} ≥ 2^-(D0+g) for superpolynomial K_g.
2. **(L)**, local stability of β. *Falsifier:* β jumps unboundedly inside J_{K+c'}-balls.
3. **(M)**, materialization.
   - Compute e = exp(2Σ n_i log P_i) in Mumford form. This means inverting the odd-power-sum-type map t ↦ (Σ_i L_k(t_i)).
   - Then perform one Cantor reduction of P+e, with error confined to J_{D0+1}.
   - *Falsifier:* superpolynomial loss on a set of n of probability above 2^-σ.
4. **Label precomputation.** Local factorization of f over Q2 and square roots in Q2[x]/f, with a paid precision charge. This step is independent of P.

## Status

| Item | Status |
|---|---|
| Coset-volume transfer theorem and the two corollary reductions | Proved |
| (S), (L), (M), label precomputation | Assumptions, still open |
| Finite examples | None used |
| Hardness, speedup, or a full local Kummer algorithm | None claimed |