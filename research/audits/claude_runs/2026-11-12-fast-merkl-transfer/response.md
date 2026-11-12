# Review: does the conditional Merkl-atlas Green bound yield a joint-polynomial stable Faltings-height and reconstruction bound in Javanpeykar's proof?

## Verdict

1. **Faltings height: yes, but only under a stronger hypothesis than the headline Green bound.** Assume the full conditional atlas from `MERKL_LOG_COLLISION_ATLAS.md`, not only its headline consequence `sup gr_Y ≤ C_r d³(d+L)`. Then the Javanpeykar route gives a joint-polynomial stable Faltings-height bound:

   h_Fal(Y) ≤ C'_r · d⁵ · (d + 1 + h*_B), where h*_B := max over β ∈ B of the absolute Weil height h(β).

   This is still conditional. It needs:
   - the four Merkl hypotheses with the claimed constants;
   - one extra chart-coordinate property, (H5) below;
   - two source items that are outside the supplied excerpts:
     - the exact statement of Theorem 2.4.1;
     - the definition of H_B in Section 1.3, including how it compares with h*_B.

2. **The headline `sup gr` bound alone is not sufficient.** The Faltings-height chain never uses an upper bound on sup gr. It uses two other things:
   - Merkl's two-sided local chart comparison (second part of Theorem 3.1.2), which gives |log‖dz_j‖_Ar| on inner disks;
   - the density bound c1 on whole charts, which gives the Wronskian bound.

   An upper bound on gr alone gives nothing about −log‖dz‖_Ar(x). That quantity equals lim_{y→x}(gr(x,y) − log|z(x)−z(y)|), and the subtracted term tends to +∞, so a one-sided bound on gr does not control it.

3. **Reconstruction: not closed.** A stable-height bound does not bound supplied-model coordinates; the twist family E_a: y² = a·x(x−1)(x−2) already rules that out.
   - I close the second-coordinate (y) descent below by an elementary derivation, charging the model height h_F.
   - The smallest missing theorems are:
     - an Arakelov-to-base-coordinate height comparison, h(x(P)) versus h_ω(P);
     - a torsion-support-point Arakelov height theorem.
   - No claims are made here about point counting, CRT reconstruction, hardness, or speedup.

## 1. The hypothesis, split into its parts

Here σ ranges over complex embeddings, Y_σ is the corresponding Riemann surface, and L_σ = 1 + log(1/δ_σ).

| Label | Content | Used for | Implied by `sup gr` bound alone? |
|---|---|---|---|
| H1–H4 | Merkl atlas (Definition 3.1.1) for Y_σ: r1 = 3/4, N ≤ C_r d(d+L_σ), c1 ≤ Cd², log M ≤ Cd | Input to Theorem 3.1.2 | — |
| G1 | sup gr ≤ G_σ := 330N(1/4)^{−3/2}·log 4 + 13.2N·c1 + (N−1)·log M = O_r(d³(d+L_σ)) | **Not used** in the h_Fal chain; may enter e/δ bounds (Theorem 2.4.1, unverified) | yes (it *is* this) |
| G2 | \|gr(x,y) − log\|z_j(x)−z_j(y)\|\| ≤ G