# Audit: Kutas Theorem 20 as a conditional-on-factoring conic solver over Q(√e)

## 0. Verdict

**The primitive is admissible**, conditional on exactly one imported backend: Fact 1, the Simon result as Kutas asserts it. It is GRH-free and needs no other algorithmic import.

Theorem 20 does not quite go through as printed. It needs five repairs, all constructive:

- **Missing `l'² = 0` case.** Corollary 19 never handles it.
- **Missing `c = 0` case.** Proposition 15's hypothesis `c ≠ 0` is not guaranteed in Corollary 19.
- **Square-`d` case for the conic.** Here the zero-divisor-to-conic map can return (0,0,0).
- **Replace Step 3 by Remark 21.** This removes the unspecified `[13]/[15]` backend and the branch "B is division, conclude", which cannot be certified.
- **Clocked composition of Las Vegas calls.** The paper's "randomized polynomial time" claims do not compose naively.

There is one genuinely uncovered interface: **the exact statement of [23] (Simon).** The excerpt does not give its hypotheses or complexity measure, and does not show that it is a refereed theorem.

There is also one unsupported side claim. Remark 22's "at most two factoring calls" contradicts Proposition 12 and Remark 14, so it must not be used.

Notation: Kutas's `d` is our `e`. Below, `e` is the squarefree non-square defining `F = K = Q(√e)`. `(d, a)` are the conic coefficients in `F*`.

---

## 1. Attacks, cheapest decisive first

### A1. Zero divisor to conic solution (where it fails, then the repair)

Take `A = H_F(d,a)` with basis `1, u, v, uv`, where `u² = d`, `v² = a`, `uv = −vu`.

**Structure constants.** Example 9's matrices were checked entry by entry as left-multiplication matrices, with row i giving the image of basis element i. For example:
- `v·uv = −βu`
- `uv·u = −αv`
- `(uv)² = −αβ`

They are correct. The target needs no Rónyai conversion, because the input is already a quaternion basis.

**The norm form.** For `s = x1 + x2u + x3v + x4uv`, we have `N(s) = x1² − d·x2² − a·x3² + da·x4²`. Over a field, `s` is a zero divisor if and only if `N(s) = 0`, since `s·σ(s) = N(s)`.

**The map.** Set:
- `X = x1x3 − d·x2x4`
- `Y = x2x3 − x1x4`
- `Z = x3² − d·x4²`

Then `X² − dY² = (x1² − d·x2²)(x3² − d·x4²) = a·Z²`. This is the two-square (Brahmagupta) identity.

**If `d` is a non-square in F.** If `Z = 0`, then `x3 = x4 = 0`. Then `x1² = d·x2²` forces `x1 = x2 = 0`, contradicting `s ≠ 0`. So `Z ≠ 0` (proved).

**Falsified as a general map when `d = δ²`.** Take `x3 = x4 = 0` and `x1 = δ·x2 ≠ 0`. Then `(X, Y, Z) = 0`.

**Repair.** First test whether `d` is a square in F. This is deterministic polynomial time with no factoring:
- Write `d = r + t√e`.
- If `t = 0`: test whether `r` or `r/e` is a rational square.
- If `t ≠ 0`: `d` is a square iff `r² − e·t²` equals `m²` for some rational `m`, and `p² = (r ± m)/2` is a rational square for some `p ≠ 0`. Then `δ = p + (t/2p)·√e`.

If `d = δ²`, output `X = (a+1)/2`, `Y = (1−a)/(2δ)`, `Z = 1`. Then `X − δY = a` and `X + δY = 1`. So the output always has `Z ≠ 0`, which is strictly stronger than the requested "Z ≠ 0 if d is a non-square".

### A2. Remark 8 indexing

The text says that if `x1² − αx2² − βx3² + αβx4² = 0`, then `1 + x1u + x2v + x3uv` is a zero divisor.

**False as written.** The correct element is `x1 + x2u + x3v + x4uv`. This is material if implemented literally.

The ternary change of variables in Remark 8 is garbled in the rendering. A direct replacement: if `αx² + βy² = z²` with `(x,y,z) ≠ 0`, put `t = xu + yv`.
- Then `t² = z²`.
- `t ≠ 0`, because otherwise `x = y = 0`, hence `z = 0`.
- Since `t` is non-central, `(t − z)(t + z) = 0` with both factors nonzero.

### A3. Proposition 12 (6-variable form)

I re-derived the algebra.

**Cross terms vanish.** For `l = λ1w + λ2w' + λ3ww'` with `λi ∈ K`, all cross terms cancel. So `l² = λ1²·w² + λ2²·w'² − λ3²·w²·w'²`.

**The √e coefficient.** Write `w² = r1 + t1√e` and `w'² = r2 + t2√e`. Let `R = r1r2 + t1t2·e` and `T = r1t2 + r2t1`. The coefficient of √e in `l²` is form (3), which matches the paper.

**Typo (as rendered).** Gram-matrix entry (2,2) prints as `t2·d`; it should be `t1·e`. The stated determinant `t1²e − r1²` is the correct one, so this is not material.

**Key identity, verified.** `R² − T²·e = (r1² − e·t1²)(r2² − e·t2²)`.

**Indefiniteness, verified.**
- All three 2×2 determinants are nonzero, because `e` is a non-square, `t1, t2 ≠ 0`, and `T ≠ 0` in this branch.
- So the 6-form is nondegenerate.
- The paper's case split forces some block determinant to be negative.

**Isotropy.** A nondegenerate indefinite form of dimension 6 ≥ 5 is isotropic. This is Meyer's theorem, which the paper uses implicitly.

**Nonzero output.** A nonzero zero `(s1, …, s6)` gives `(λ1, λ2, λ3) ≠ 0`, because `1` and `√e` are Q-independent. So `l ≠ 0`.

**Degenerate cases.** If `t1 = 0`, `t2 = 0`, or `T = 0`, take `l = w`, `w'`, or `ww'` respectively. All are correct.

**Scope.** No splitting of `A` is needed (Remark 13 is correct). No GRH is used if Fact 1 is used.

### A4. Proposition 15 and Corollary 19 (gaps found and patched)

**Proposition 15 expansion, verified.**
- `v·(uv) + (uv)·v = 0`.
- After the substitution `x = s1 + f·s2`, `y = s2`, `z = s3 + f·s4`, `w = s4` (unimodular), we get `x² + (e − f²)y² − az² − a(e − f²)w²`.
- This is exactly the norm form of `H_Q(f² − e, a)`.
- `f² − e ≠ 0` because `e` is a non-square, and `a ≠ 0`.

**The equivalence is constructive in both directions.** A nonzero `v'` gives a nonzero zero of (4), and conversely.

**Gap 1: `c = 0`.** Corollary 19 finds `w` anticommuting with `l`, but Proposition 15 assumes `w² = b + c√e` with `c ≠ 0`. If `c = 0`, then `l' := w` already works. If `w² = 0`, output `w` as a zero divisor.

Computing `w` is implicit in the paper. Here is an explicit formula for `l = λ1u + λ2v + λ3uv`:
- If `(λ1, λ2) ≠ 0`: take `w = a·λ2·u − d·λ1·v`.
- Otherwise: take `w = u`.

This works because `lw + wl = 2(d·λ1μ1 + a·λ2μ2 − da·λ3μ3)` for traceless `w = μ1u + μ2v + μ3uv`.

**Gap 2: `l'² = 0`.** Corollary 19 asserts that `H = ⟨1, l, l', ll'⟩` is a quaternion algebra, which needs `l'² ≠ 0`. If `l'² = 0`, output `l'` as a zero divisor.

**Shortcuts.**
- If `l² = c²` with `c ∈ Q*`, output `l − c` directly. The paper instead routes through Proposition 15; this is correct but unnecessary. Its algebra symbols there are also garbled, though the result splits under either sign.
- If `l² = e·c²`, output `l/c − √e`.

**Existence of `l'` when `A` is split.** Use the companion matrix in `M2(Q) ⊂ A`, conjugacy of elements with equal separable characteristic polynomial (this holds even when `x² − l²` splits over K), and transport of an anticommuting element. Verified.

**Fact needed later.** `H ⊗_Q K → A` is an injective homomorphism, because `H ⊗ K` is simple. By dimension it is an isomorphism, so `H ∩ K·1 = Q·1`. This also holds when `A` is a division algebra.

### A5. Theorem 20, Step 3 vs Remark 21

Step 3 needs `[13]/[15]` to decide whether `H` splits. The excerpt never states their interface over Q. **Replace it with Remark 21**, which I verified:

- `H ⊗ K ≅ A`. So `A` is split iff (`H` is split, or `K` embeds in `H`) iff the form `q = αx1² + βx2² − αβx3² − e·x4²` is isotropic. Here `α = l²` and `β = l'²` are in Q*.
- Given a zero of `q`, let `t = x1·l + x2·l' + x3·ll'`.
  - If `x4 = 0`: `t² = 0` and `t ≠ 0`, so `t` is a zero divisor.
  - If `x4 ≠ 0`: `s = t/x4` satisfies `s² = e`, and `s ≠ ±√e` because `H ∩ K = Q`. So `s − √e` is a zero divisor.

**Bonus (my derivation, not stated by Kutas).** Every step except the Fact 1 calls is unconditional. Fact 1 returning "no zero" at Proposition 15 or at Step 4 implies that `A` is not split. So the pipeline also decides solubility, and the promise of solubility can be dropped. The insolubility verdict carries no certificate; it inherits Fact 1's correctness.

### A6. Backend scope and GRH separation

**Fact 1 (Simon [23]).** Imported as Kutas asserts it: randomized polynomial time, factoring oracle allowed, finds a zero or reports none exists, for forms over Q of dimension ≥ 4. The calls here use nondegenerate forms of dimension 6 and 4.
- Pipeline dependency: Steps 1, 2 and 4 (the Proposition 15 equation and Remark 21).
- Unconditional, but only as asserted; see U1.

**Fact 2 (Castel).** GRH-conditional, indefinite forms of dimension ≥ 5.
- Pipeline dependency: none. It is not used.
- Substituting it in Step 1 adds GRH and does not remove factoring, because Steps 2 and 4 are 4-variable. So there is no benefit; do not mix the two.

**[13]/[15], Rónyai [21].** Pipeline dependency: none. They are eliminated, as described above.

**Remark 22's oracle-call count is unsupported.** Proposition 12 and Remark 14 show that Step 1 also needs the factoring oracle via Simon. Use "poly(S) many calls" instead.

### A7. Las Vegas to bounded clock (a real composition gap)

The problem: if stage `i` has expected time `P_i(m)`, the next stage's input size is random. `E[P_{i+1}(size)]` need not be polynomial, because `E[X^k]` is not controlled by `E[X]`.

The fix is to run each Fact 1 call with a clock of `2·P_i(m_i)`.
- Output size is then deterministically at most the clock, so `m_{i+1} = poly(m_i)`.
- By Markov's inequality, each truncated run halts with probability ≥ 1/2.
- Any halted answer is correct, by the Las Vegas property.
- Repeat each stage up to `k` times; the total failure probability is at most `3·2^{−k}`.
- Every positive output is checked exactly: `Tr(l) = 0`, `l² ∈ Q`, anticommutation, zero divisor, and finally `X² − dY² = aZ²`.

---

## 2. The admissible primitive

**CONIC_F(e, d, a; δ)**

**Input.**
- A squarefree integer `e ∉ {0, 1}`.
- `d = d1 + d2√e` and `a = a1 + a2√e` in `F*`, with `di, ai ∈ Q` in binary.
- `S` is the total bit size of the input.

**Output.** One of three answers:
- **(SOL)** `(X, Y, Z) ∈ F³` with `Z ≠ 0` and `X² − dY² = aZ²`. This is exactly verified.
- **(INSOL)** Correct, conditional on Fact 1's negative answers being correct.
- **(FAIL)** Occurs with probability ≤ δ.

**Cost.** `poly(S)·log(1/δ)` bit operations, plus `poly(S)·log(1/δ)` factoring-oracle calls on integers of `poly(S)` bits. Each call is charged its query and answer length.

**Assumptions.**
- Fact 1, read as: Las Vegas, polynomial in the bit size of an integral nondegenerate form of dimension ≥ 4.
- No GRH.

**Procedure (the shortest proof path).**

0. If `d` is a square in F, output the A1 formula.
1. Use the quaternion basis of `H_F(d, a)` with `w = u`, `w' = v`, `r1 = d1`, `t1 = d2`, `r2 = a1`, `t2 = a2`. Run Proposition 12 with the degenerate cases, then one clocked Fact 1 call on the 6-form. This gives `l`.
2. Handle `l` and the anticommuting element:
   - If `l² = 0`, `l` is the zero divisor.
   - If `l²` is a rational square or `e` times one, use the A4 shortcuts.
   - Otherwise compute `w` by the explicit formula. If `w² = 0`, output `w`. If `c = 0`, set `l' = w`. Otherwise make one clocked Fact 1 call on (4). A "no zero" answer means INSOL.
   - If `l'² = 0`, output `l'`.
3. Make one clocked Fact 1 call on `q` (Remark 21). A "no zero" answer means INSOL. Otherwise obtain the zero divisor as in A5.
4. Apply the map from A1 and verify.

**Sizes.**
- All form coefficients are polynomials of degree ≤ 3 in the input data. In particular `e` enters only through arithmetic, so `log|e|` enters polynomially. This uniformity in `e` is what separates Theorem 20 from `[13]/[15]`. The paper supports it through its proof, not through an explicit size parameter in the theorem statement.
- The chain is `S → P(O(S)) → P(poly) → P(poly)`: polynomial, with an unspecified compounded exponent because the excerpt gives no exponent for Fact 1.
- Arithmetic in F is exact. Inversion is `(r − t√e)/(r² − e·t²)`.

**Quantum instantiation.** Replace the oracle by Shor's algorithm. Check the returned factors by multiplication, and check primality with deterministic polynomial-time primality testing. The result is a Las Vegas quantum polynomial-time solver.

No hardness result for the F-conic problem itself follows from the excerpt. Remark 17's hardness concerns the Q-subalgebra subtask only.

---

## 3. Proved, imported, uncovered

**Proved here (from the excerpt plus standard facts: Meyer's theorem, Skolem–Noether conjugacy, simplicity of central simple algebras under tensor products, the embedding criterion for quadratic fields in quaternion algebras):**
- A1, A3, A4, A5.
- The decision bonus in A5.
- The clocked composition in A7.

**Imported, not re-checked:**
- **Fact 1**, as stated in the JSC-published Kutas paper. This is a secondary assertion; I have not checked Simon's proof.

**Uncovered:**
- **U1. The statement of [23].** The excerpt describes [23] as "presented at a conference" and "implemented in MAGMA". The bibliography entry is not supplied. The following must be confirmed against the primary text: that [23] covers dimensions 4 and 6, its time bound in bit size, any nondegeneracy requirement, the absence of GRH or class-group assumptions, and its Las Vegas semantics.
- **U1 consequence.** If [23] is only a talk or preprint, the primitive rests on an unrefereed claim relayed by a refereed paper.
- **Hash.** I could not verify the supplied SHA256.

---

## 4. Falsifiers

1. Simon's actual theorem needs GRH, or is not polynomial in dimension 4 for arbitrary determinants. Then the "GRH-free" claim fails at Steps 2 and 4.
2. Fact 1 is Monte Carlo, with possibly wrong "no zero" answers. Then SOL survives because it is verified, but INSOL loses its guarantee.
3. Any input on which an implementation outputs (0,0,0) indicates a missing A1 square-`d` test.
4. An input reaching Proposition 15 with `c = 0`, or with `l'² = 0`, crashes a literal implementation of Corollary 19.

---

## 5. Finite controls (hand-computed; correctness checks only, not complexity evidence)

**Positive control: `e = −1`, `d = 2`, `a = 1`.**
- `t1 = 0`, so `l = u` and `l² = 2`.
- `w = −2v` and `w² = 4`, so `c = 0` and `l' = w`.
- `q = 2x1² + 4x2² − 8x3² + x4²` has the zero `(2, 0, 1, 0)`. Since `x4 = 0`, `t = 2u − 2uv`, with coordinates `(0, 2, 0, −2)` and `N = −8 + 8 = 0`.
- The map gives `(X, Y, Z) = (8, 0, −8)`, and `64 = 1·64`. ✓

**Negative control: `e = 5`, `d = a = −1`.**
- The conic is `X² + Y² + Z² = 0` over a totally real field, which has no nonzero solution.
- The pipeline must return INSOL at Step 2 or Step 4, not SOL.