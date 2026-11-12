# Cyclotomic specialization for full sparse constant relations

## Bottom line

- **Proved (pending review):** the correctness side of the operation. Once a torsion point `t` passes an exact check, `Rel = Alg ∩ Rel_E(u(t))` holds. Every downstream cost is polynomial in `q`, `δ` and the native bits. Neither the discriminant nor étaleness is needed.
- **Proved for explicit sparse factors:** a short exponent-difference prime lemma gives explicit polynomial bounds on `q` for every explicitly sparse factor.
- **Proved consequence, a restricted face only:** classical polynomial sparse-bit FULL Rel for every fixed `δ`, uniformly in growing `s` and `k`. The prior rational-specialization falsifier family is also handled for every `δ`.
- **Open:** the native growing-`δ` case. I found neither a proof nor a compact family forcing superpolynomial cyclotomic degree. Below I reduce the missing step to one exact statement, list the properties any falsifier must have, and record a barrier.
- **Not claimed:** no full classical solver, no hardness, no speedup.

## 1. Correctness of the operation (deduction)

**Setup.** Let
`A = Q[T, 1/Den][Y]/(f) [u_1^{-1}, …, u_k^{-1}] ⊂ F`, and let `C_A` be its algebraic-over-Q elements. `C_A` is a field, as noted in `SPARSE_CHARZERO…§1`. Every `u^e` with `e ∈ Alg` lies in `C_A`.

Fix a prime `q`, an exponent vector `a ∈ (Z/q)^s`, and the point `t = ζ_q^a`. Require `Den(t) ≠ 0`. Compute over `Q(ζ_q)`:
- `r = rad(f_t)`, using `gcd(f_t, f_t')`;
- `g` = the largest factor of `r` coprime to `P = ∏_i u_i(t)`, obtained by repeated gcd removal;
- `E'' = Q(ζ_q)[Y]/(g)`.

**Acceptance condition.** Accept iff `deg g ≥ 1`. Then:
- `Q[T, 1/Den][Y]/(f) → E''` is a ring homomorphism, because `g` divides `f_t`.
- Each `u_i(t)` is a unit in `E''`, so the map extends to `A`.
- `C_A → E''` is a homomorphism from a field into a nonzero ring, hence injective.

**Consequence.** `Rel = Alg ∩ Rel_{E''}(u_1(t), …, u_k(t))`.
- (⊆) is immediate.
- (⊇): if `e ∈ Alg` and `u(t)^e = 1`, then `u^e ∈ C_A` maps to 1, so by injectivity `u^e = 1`.

Three properties follow:
- **No discriminant needed.** `disc_Y(f)` can be dropped from `H`.
- **Weaker requirement than `Norm(u_i)(t) ≠ 0`.** It suffices that *some* branch over `t` avoids every `u_i`. Since `X → G_m^s` is finite flat, hence open, the bad locus `B` is closed and contained in `V(∏ Norm(u_i))`.
- **Las Vegas point selection.** Acceptance is checked exactly, so a wrong point is never used. Only the existing Alg step carries error `η`.

**Cost given `q`.**
- Reducing binary `T` exponents mod `q` costs `O(bits)` per monomial.
- Coefficients of `f_t` and `u_i(t)` are short in the basis of `Q(ζ_q)`. Inverting `b_j(t)` inside a degree `q − 1` field costs height `poly(q, bits)`.
- `E''` has Q-dimension at most `δ(q − 1)`, with polynomial-height structure constants. These come from the basis `ζ^i Y^j` reduced mod `g`.
- LS Theorem 1.11 (supplied excerpt) is deterministic polynomial time. *Unverified here:* that LS's "Q-algebra" input is a finite commutative structure-constant presentation. `E''` is reduced in any case.
- Lattice intersection with Alg uses HNF. Original small `u_i` only; no Alg-basis powers are formed.

## 2. Lemma: explicit sparse factors (proved, self-contained)

**Statement.** Let `P = Σ_{k ≤ K} c_k T^{e_k}`, with `c_k ∈ Q*`, distinct `e_k ∈ Z^s`, and every coordinate `|·| < 2^{β'}`. Let `q` be prime with `q > K`. Suppose that for every pair `k ≠ l` the vector `e_k − e_l` is not `≡ 0 (mod q)`. Then:

`Pr_{a ∈ (Z/q)^s}[ P(ζ_q^a) = 0 ] ≤ C(K, 2)/q`.

**Proof.**
1. Each pair collides, i.e. `⟨e_k − e_l, a⟩ ≡ 0`, with probability `1/q`.
2. Off collisions, `P(ζ^a) = R(ζ_q)`, where `R = Σ c_k x^{r_k}` has distinct `r_k < q` and `K < q` nonzero terms.
3. `Φ_q` is irreducible of degree `q − 1`. Since `deg R ≤ q − 1`, the only way `Φ_q | R` is `R = cΦ_q`, which would need `q` terms. Hence `R(ζ_q) ≠ 0`.

**Bad primes.** A pair difference has a nonzero coordinate below `2^{β'}`, so it has fewer than `β'/log_2 X` prime divisors `≥ X`. Rosser–Schoenfeld (already sourced in the notes) gives more than `3X/(5 ln X)` primes in `[X, 2X]`.

**Probability budget.** Protect a list 𝒫 of nonzero polynomials. Set `Π = Σ_{P∈𝒫} C(|supp P|, 2)` and choose
`X ≥ max(21, max|supp P| + 1, 5Π(β' + 1))`.
For uniform `q ∈ [X, 2X]` and uniform `a`, the failure probability is at most `2.2 Π(β' + 1)/X < 1/2`. This is the "prime divisibility of exponent differences" route. Mann's theorem (external, unverified here) would extend it to composite orders but is not needed.

**Scope.** The support is used only as a proof object; nothing is expanded. Denominators (`L` polynomials with `≤ m` terms each) are always covered this way.

## 3. Fixed `δ` and other covered classes (proved consequences)

### Norms via Sylvester structure

Clear denominators:
- `F̂ = β_f f` with `β_f = ∏_j b_j`;
- `Û = β_u u_i` with `β_u = ∏_r d_r`.

Each Sylvester entry then has at most `m^δ` terms. The matrix has size `n_S ≤ 2δ − 1`. Hence

`Res_Y(F̂, Û) = β_f^{d} · β_u^{δ} · (±Norm(u_i))`

has at most `K_δ = (2δ − 1)! · m^{δ(2δ − 1)}` terms. Exponents gain at most `log_2(2δ²)` bits.

For fixed `δ` this is a genuinely polynomial support, not an exponential expansion. With `Π ≤ L·m² + k·K_δ²`:
- `q = poly`;
- every factor of `H` is protected by the Section 2 lemma;
- Sections 1–2 together give a classical polynomial sparse-bit FULL Rel for every fixed `δ`, extending the reviewed `δ ≤ 2` cases. With polynomial-coefficient inputs, `K_δ ≤ (2δ)^{2δ} m^{2δ}`.

### The existing rational-specialization falsifier is handled for all `δ`

In `A = 2 + T^M`, `f = ∏_j (Y − jA) − B`, we have `Norm(u_j) = f(T, jA)` up to sign, which is `±B = ±T^M (T^M − 1)(2 + T^M)`. This is explicitly sparse.
- Take any prime `q ∤ M` and `a ≠ 0`.
- `f_t` has coefficients `2 + ζ^{aM mod q}` of tiny height.
- So roots of unity are not killed, as the contract anticipated.

### `T`-free `u` (or `T`-free `f`), polynomial coefficients, any `δ`

`Norm(U(Y))(t) = 0` iff `f(t, β) = 0` for some root `β` of `U`. Here `f(T, β)` has at most `m_f` terms over `Q(β)`.

The lemma holds over `K_0 = Q(β)` whenever `q ∤ disc(K_0)`. In that case `K_0 ∩ Q(ζ_q) = Q`, because every nontrivial subfield of `Q(ζ_q)` ramifies at `q`, so `Φ_q` stays irreducible over `K_0`. The union bound over fewer than `δ` roots gives `Pr ≤ δ·m_f²/q`.

## 4. Growing `δ`: exact remaining statement (open)

### Exact criterion

A prime `q` admits a good `a` iff

`ρ_q := Res_Y( f mod (T_j^q − 1), u mod (T_j^q − 1) )` (in the branch-weakened, all-`u_i` version)

is nonzero in the group ring `Q[(Z/q)^s] ≅ ∏_{μ_q^s} C`.

This holds because resultants commute with the homomorphism (`f` is monic). So the operation succeeds iff some exponent-reduced instance, whose numerical degree is below `q`, keeps a nonzero norm. Good `a` form unions of `F_q^*`-orbits.

### Missing lemma

There exist `q = poly(bits, δ, k, s)` and a sampler such that `Pr_a[t ∉ B ∪ V(Den)] ≥ 1/poly`. This must hold for every compact native `(f, u)`.

### Counting view

By Laurent's torsion-coset theorem (external, unverified), the torsion points of `B` lie in finitely many maximal torsion cosets. Each such coset meets `μ_q^s` in at most `q^{s−1}` points. Hence `B ⊇ μ_q^s` forces at least `q` cosets meeting `μ_q^s`. A raw coset count `C(B)` is too weak a measure: `T^{2^b} − 1` has `2^b` cosets yet is harmless for `q ∤ 2^b`. A bound must therefore be **per-`q`**, not global.

### Necessary properties of any falsifier (all deduced above)

1. **`δ` must grow** with `δ² log m + δ log δ = ω(log n)`, otherwise `K_δ` is polynomial.
2. **Both `f` and `u_i` must be mixed** in `(T, Y)`. Neither may have `T`-free coefficients, and no `Norm(u_i)` may be poly-sparse.
3. **The bad locus `B` must be large:** it must contain `μ_q^s` for every prime `q ≤ Q` with `Q` superpolynomial. To defeat the composite-`N` variant, it must contain all `μ_N^s` with `φ(N) ≤ P`.
4. **Common zeros with `y` torsion are probably insufficient (speculative):** such zeros lie in torsion cosets of `V(f) ∩ V(u)`, and sparse-term arguments apply there. The needed common roots `y` must be non-torsion, which is an unlikely-intersection regime. Known results there are non-quantitative for binary exponents; this is speculation, not a theorem.
5. **Search done here:** binomial denominators, Kummer `f`, compositions `Norm(Y − g)` with bounded-term `g`, and cyclotomic-constant `f` all fail to falsify. This is a finite search, not evidence of a theorem.

### Barrier on proof shape (deduction plus the supplied source; not hardness)

By Oki's Remark 12, Kronecker substitution maps Edmonds' symbolic determinants to univariate determinants with sparse binary-exponent entries. For `s = 1`, enumerating all `q ≤ poly` is deterministic.

So a cyclotomic hitting lemma for *general* sparse-entry determinants would derandomize Edmonds' problem. Oki's introduction states this would imply circuit lower bounds.

A proof must therefore use the monic-irreducible Sylvester/norm structure. I know no compact embedding of general determinants as native norms: charpoly coefficients are not compact. This shows only that the wrong lemma is out of reach. It does not show the operation fails.

## 5. Falsifiers and cheapest disproofs

- **Section 1:** a native instance with accepted `t` but `Alg ∩ Rel_{E''} ≠ Rel`. This is impossible unless `C_A` fails to be a field or LS's input scope excludes `E''`. Checking the LS definition is the cheapest audit.
- **Section 2 lemma:** a polynomial with fewer than `q` terms and distinct exponents mod `q` vanishing at `ζ_q`. This is impossible by the degree argument.
- **Fixed-`δ` claim:** an error in the `K_δ` count or in the clearing identity `Res(F̂, Û) = β_f^d β_u^δ Norm`.
- **General operation (decisive disproof target):**
  - an explicit polynomial-size native family with growing `δ` such that `ρ_q = 0`, i.e. every branch is killed, for all primes `q ≤ Q(n)` with `Q` superpolynomial;
  - verify it symbolically in `T^M`, without expanding `M`.
  - A finite control for `s = 1`: test `Res(f_{ζ_q}, u_{ζ_q})` for `q ≤ 10³` on candidate mixed families. This is a control only, not a theorem.
- **Positive closure:** prove the per-`q` torsion-avoidance lemma for Sylvester norms of compact mixed `(f, u)` with growing `δ`.

**Disposition.** The cyclotomic route removes the height obstruction exactly and closes every fixed `δ`, pending independent review. The native FULL classical counterpart remains open at the growing-`δ` torsion-avoidance lemma for mixed Sylvester norms.