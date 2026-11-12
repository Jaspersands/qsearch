# Review: Stoll root-to-half acceptance interface in ONE-HALF

## Verdict

**No native counterexample was found.** For f monic (so Stoll's c = 1), the high-degree representation `[A_u, B_u]` combined with one arbitrary exact root `s² ≡ (−1)^{deg A_u} A_u mod f` meets the hypotheses of Stoll's Proposition 5.1 exactly. I found no missing norm or sign orientation and no missing existence hypothesis.

The interface is sound as stated, with **one gap**: the extraction inverse of U mod W is not an acceptance test. The note says it is "paid" either by the success-event caps or by the review's polynomial certificate (7). Neither works as an acceptance step:

- The caps only bound the precision loss on the good event.
- Certificate (7) defines C, T₀ and Z from R. R is the quantity being extracted, so (7) is circular as an extraction certificate. It is valid only as an analytic bound.

**Fix:** add a guarded visible test of `Res(W,U)`, or equivalently of `Res(W, f·A_u)`, after the solve. With that test added, the short proof below closes the interface. The determinant, mixed-resultant and inverse caps affect only success probability and precision, never soundness.

Also note a naming collision: "u" denotes both the pencil scalar and Stoll's polynomial. Below, Stoll's polynomials are U, V, W.

## Cheapest attacks first

### 1. Sign of ε
The stored label of `[a0, b0]` uses `(−1)^e`, where e = deg a0. The root needed here uses `ε = (−1)^n` with `n = deg A_u = 2g+1−e`, which has the **opposite** parity.

- **Exact transfer.** `a0·A_u = f − B_u²`. If a0 is coprime to f, then `(−1)^n A_u ≡ (−1)^e a0 · (B_u/a0)² mod f`. In general, µ([D − d∞]) = ∏(x_i − θ) is intrinsic to the class, and A_u is certified coprime to f. So a zero label of h, plus 2σ ∈ 2J, makes `(−1)^n A_u` an exact square in L.
- **The wrong sign fails closed (exact lemma).** Suppose an implementation used `s'² ≡ −ε A_u`. Stoll's congruence argument then gives `V² − fU² = −ε A_u W²` identically. When deg W = g, compare leading coefficients:
  - n odd: the odd-degree term fU² dominates, forcing `lc(U)² = −1`;
  - n even: V² dominates, forcing `lc(V)² = −1`.

  Since −1 is not a square in ℚ₂, no full-degree solution exists. Then det B_g = 0 exactly, the test is never visible, and the step ABORTs. A wrong sign costs liveness, never soundness.

### 2. Orientation of B_u
This is the only invisible sign in the interface. `f ≡ B² mod A_u` holds for both ±B_u, so no visible test detects a flip.

- The candidate's `B_u = −b0 − u·a0` (B_u ≡ −b0 mod a0) is correct. From div(y − B_u) = ι(a0, b0) + (A_u, B_u) − (2g+1)∞, it follows that `[A_u, B_u] = [a0, b0]`, as in Stoll's remark.
- A flipped sign would certify a genuine half of −h_z. The recorded relation `2Q = h + 2σ` would then be false.
- **Obligation:** the DAG must derive this orientation from the exact identity. It cannot be checked by a test.

### 3. Kernel dimension and spurious minors (exact lemma)
Let j be the minimal degree of w. If j < g, then x·(U₀, V₀, W₀) also satisfies (5.1)–(5.2). By the parity of the leading term, `2·deg V ≤ n+2j` and `2·deg U + 2g + 1 ≤ n+2j`. So degree headroom remains for u, v and w. Hence:

**dim ker M_g = 1 ⇔ j = g ⇔ rank M_g = m+n ⇔ w_g ≠ 0 on the kernel ⇔ det B_g ≠ 0.**

Consequences:
- If dim ker M_g ≥ 2, every maximal minor of M_g vanishes exactly. Then no minor can be visible.
- Any visible maximal minor certifies the exact kernel line, and j = g. By Cramer's rule, w_g = ±det B_g up to that minor.

Visibility is preserved under approximation. Scale B' = 2^{S_M}·B_g to be integral, with entries correct mod 2^P. If the computed v(det) = δ < P, the exact determinant has valuation exactly δ.

The data form an exactly consistent system. A_u and B_u are exact DAG objects, and s lies in a certified Hensel root ball of the exact element. Therefore **no visible augmented minor can certify a spurious half**.

The one unsound shortcut would be normalizing by a w_g that is not visible. That is a precision failure, not a wrong certificate.

### 4. Extraction
Stoll defines d₁ = gcd(U, W), which divides f·a₁. Only when d₁ = 1 does `Q = [W, −V·U⁻¹ mod W]` hold.

- Off the good event, d₁ can be nontrivial; this happens exactly when W meets A_u. An unguarded approximate inverse could then output an r that names no point.
- A visible `Res(W,U)` certifies d₁ = 1 exactly. With d₁ = 1, `r² ≡ f mod W`, so (W, r) is a general-position reduced pair.
- The required test is not in the note. This is the gap stated in the verdict.

### 5. Uniform payment of the inverse
Identity (8) gives `v Res(U,W) = 2g + v Res(W,A_u) + 2·v Res(W,R) − v Res(W,H)`. Hence

**K_inv = 2g + K_aw + 2·K_wr + g(5g+12)·S.**

This bound holds uniformly over all 2^{t+1} roots, because the good event and the pencil cover every rational half. The mixed term is exactly the right one: a common root of W and A_u forces U to vanish there (Stoll's d_a). So the inverse is uniformly paid by the stated resultants plus the pole cap S. The cap is valid only on the event, so the visible test remains mandatory.

## Exact layers, kept separate

### Source theorem (Stoll Proposition 5.1, k = ℚ₂, c = 1)
Hypotheses: a = A_u is monic, squarefree, of degree ≤ 2g+1; d = gcd(A_u, f) = 1; f ≡ B_u² mod A_u; and `s² ≡ (−1)^n A_u mod f`. Note `a − a₁f₁ = a − af ≡ a mod f`.

Under these hypotheses:
- a minimal solution with deg w ≤ g exists and is unique;
- relation (5.3) holds;
- `Q = [w, r]` satisfies 2Q = P;
- s ≢ ±s′ gives distinct Q, and each half determines s up to sign.

So the 2^{t+1} roots in L, taken up to ±, correspond bijectively to the 2^t rational halves. Both s and −s give (−U, −V, W) and the same r. **Any root choice is valid.** The Stoll W is the reduced Mumford polynomial of its half, so "all halves have degree g" is equivalent to j = g for every s.

### Field arithmetic (assumed per the task)
An exact root lies in a Hensel ball whose precision guard in each component is 2e_i + v_i(A_u). That valuation is bounded via `Res(f, A_u) ≤ K_af` and the CRT index (≤ D). I did not audit the backend itself.

### Finite certificate (all tests guarded for visibility)
1. Visible `Disc(A_u)` and `Res(f, A_u)`. These are needed for **soundness**, not just success: if d ≠ 1, Stoll's system and its required square both change.
2. A certified root ball for s.
3. Visible `det B_g`.
4. Visible `Res(W, U)` (**to be added**).
5. Pole-cap check on W and R. Valuations of visible coefficients are exact.

Conclusion: Q is an exact point named by the DAG, with `2Q = h + 2σ(z)` and `2Q − h = 2σ ∈ E`.

## Precision ledger for one edge (additive)

Constants, using the bridge's notation:
- `S_M = (2g+3)S + 2K_wr`
- `K_B = (m+n+1)·S_M + D_B`, with D_B from (9)
- K_inv as above

To deliver W and R to absolute precision P_out:
- Take s, A_u and B_u to precision **P_out + K_B + S_M + K_inv + c·g²·S**. The last term covers reduction mod the non-integral A_u and W, and the adjugate entry poles. Here c is a fixed small polynomial constant.
- Add the Hensel guard for s, and the D guard for CRT conversion.

Every loss is independent of P_out, which is consistent with the note's additive C_loss. The caps K_B and K_inv set when the step succeeds. Visibility alone sets correctness.

## Checked versus not checked

**Checked here:**
- the algebra from (3) to (9);
- (12): μ_β ≤ 1 + v f(β)/2;
- the grid lemma;
- the leading coefficient of `Disc(A_u)` at e = g (N′ = 1);
- a g = 0 sanity check, where det B = β matches (2).

**Not rechecked:** the confluent-evaluation proof of (5). It affects only the caps.

## Remaining obligations and falsifiers

**Obligations:**
1. Add the visible `Res(W,U)` (or `Res(W, f·A_u)`) acceptance test, ABORTing if it fails.
2. State ε = (−1)^{deg A_u} and B_u ≡ −b0 mod a0 as exact DAG identities.
3. Normalize only by a visible w_g.

**Falsifiers:**
- an exact native input where a visible det B_g coexists with d₁ ≠ 1 and the inverse is unguarded;
- a backend root that lies outside a certified ball;
- any implementation that reuses the parity (−1)^e for A_u, which fails closed, or flips B_u, which fails silently.

## Not established

The good-event probability and materialization, the backend's correctness, the whole-DAG clock, and full dyadic admission all remain open. No speedup or hardness claim follows from this review.