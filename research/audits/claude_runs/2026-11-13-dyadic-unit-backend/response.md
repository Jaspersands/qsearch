# Audit: dyadic unit-filtration labels and square-root backend

## Verdict

**The group theory holds.** I found no counterexample to the unit-filtration presentation, the square-class coordinates, the Teichmüller step, or the "solve 2x=c, then Hensel near 1" square root. I prove these below for arbitrary wild ramification.

**The setup does not hold as written.** Four parts are unsupported or need repair:

1. **The OM provenance of O_E, π and β_j.** The supplied excerpts do not prove what the note attributes to them.
2. **How the "actual factor" is named.** The note does not specify this.
3. **The branch-divisor label formula.** As written it implicitly needs an exact gcd, i.e. an exact-zero decision.
4. **The root-naming precision condition.** It is never stated.

A deterministic, self-certifying repair of item 1 and item 2 is given below. It removes the OM dependence, removes all p-adic factor approximants, and removes randomness from the backend.

Notation: write f_E for the residue degree and q = 2^{f_E}. This avoids the collision with the polynomial f. Let d = e·f_E.

## 1. Proved core (given O_E, a uniformizer π, and lifts β_j of an F₂-basis of F_q)

**(a) U_N ⊆ E*² for N = 2e+1.**
- Take u = 1+π^N y and h(z) = z²−u.
- Then v_π(h(1)) ≥ 2e+1 > 2·v_π(h′(1)) = 2e.
- Hensel's lemma gives a root z ≡ 1. So U_N ⊆ U₁².

**(b) Surjectivity of the generators.**
- For i ≥ 1, the map U_i/U_{i+1} → F_q, 1+π^i x ↦ x̄, is a group isomorphism.
- Also ∏_j (1+π^iβ_j)^{a_j} ≡ 1+π^i Σ_j a_jβ_j (mod π^{i+1}).
- Greedy level-by-level cancellation therefore writes every element of U₁/U_N as a word in the generators g_{ij} with exponents in {0,1}.
- There are M = (N−1)·f_E = 2e·f_E = 2d generators.
- |U₁/U_N| = q^{N−1} = 2^M. Since the 2^M binary words map onto a set of 2^M elements, the binary normal form is unique.

**(c) Relations.**
- (1+π^iβ)² = 1 + 2π^iβ + π^{2i}β² lies in U_{min(2i, i+e)} ⊆ U_{i+1}.
- Collecting this square with higher-level generators gives a relation 2ε_{ij} − (higher-level 0/1 vector) ∈ ker(Z^M → U₁/U_N).
- The relation matrix R is triangular with diagonal 2, so |Z^M/RZ^M| = 2^M.
- Since RZ^M ⊆ ker and both quotients have order 2^M, R presents U₁/U_N exactly.

**(d) Square classes.**
- E* = π^Z × μ_{q−1} × U₁, and q−1 is odd.
- If x² ∈ U₁ with x = πᵃζw (ζ ∈ μ_{q−1}, w ∈ U₁), then a = 0 and ζ² = 1, so ζ = 1. Hence E*² ∩ U₁ = U₁².
- By (a), U₁/U₁² = F₂^M / rowspace(R mod 2).
- So E*/E*² ≅ F₂ (valuation parity) × U₁/U₁². This is canonical once π and the β_j are fixed for the whole run.
- Free runtime check: since μ₂ ⊆ E, dim U₁/U₁² = d+1 and dim E*/E*² = d+2. A computed value different from d+1 falsifies the implementation.
- I hand-checked E = Q₂(√2), with e=2, N=5, M=4. The relations are 2ε₁ = ε₂+ε₃, and 2ε₂ = 2ε₃ = 2ε₄ = 0. This gives dimension 3 = d+1.

**(e) Teichmüller removal.**
- Newton's method on z^q − z has derivative q·z^{q−1} − 1 ≡ −1 (mod 2), a unit.
- So the iteration converges quadratically from any lift.
- Evaluating z^q takes f_E squarings, so the cost is poly(f_E, precision).
- Simpler alternative: q−1 is odd, so u ≡ u^{q−1} mod squares and u^{q−1} ∈ U₁. This avoids Teichmüller entirely for labels.
- For square roots: √u = u^{q/2} / √(u^{q−1}).

**(f) Square root of an actual square x.**
- The valuation v is even. Set u = x/π^v = ω·u₁.
- √ω = ω(ū^{q/2}), i.e. the Teichmüller lift of the inverse Frobenius of ū.
- u₁ ∈ U₁², so its coordinate c satisfies c ∈ 2(Z^M/R). Solve 2ξ = c + Ry over Z; this is triangular back-substitution.
- Set v₀ = ∏ g^{ξ}. Then w = u₁/v₀² ∈ U_N (the note's "v₀²/u" must mean u₁, not u).
- √w comes from (a).
- Root: π^{v/2} · ω(ū^{q/2}) · v₀ · √w.
- Squareness is decided exactly from x mod π^{v+N}, because U_N ⊆ U₁².

**(g) Uniformizer sampling claim.** True.
- A uniform element of m/2m pushes forward uniformly onto m/m², since 2m = m^{e+1} ⊆ m².
- So P(v=1) = 1 − 1/q ≥ 1/2, and ⌈log₂(1/η′)⌉ draws give failure ≤ η′.
- **Repair (no randomness needed):** the images of a Z₂-basis of m span m/m², so some basis vector has valuation 1. Test each one exactly via v₂(N(x)) = f_E, or via x ∉ m², where m² is an exact lattice.

## 2. Breaks and gaps

**B1 — Source hypotheses not established by the excerpts.**
- The excerpts never construct π, β_j, or a reduction map. The claim "OM valuation/reduction data provide them" is unsupported.
- The precision improvement to 2v(D)+1 appears only in an organisation paragraph (integral_bases lines 166–167). It is not a checked theorem.
- Theorem 5.18 requires condition (12) and faithful representation, which are not shown.
- Lemma 5.2 is an expected-time bound, not labelled as such.
- integral_bases Section 2 assumes f irreducible over K (line 179), but the input f is only squarefree. Line 150's dynamic evaluation is unexamined.
- Proposition 1 gives a basis for the exact factor F_s. The note uses approximants P_s ≡ F_s (mod m^ν). Transferring an Okutsu frame from P_s to F_s, and identifying α′ ↦ α, needs a stability lemma that is not supplied.
- Conclusion: the OM route is unproven here.

**R1 — Deterministic repair (I prove the reduction, but cite one standard external theorem).**
- Use Round 2 on Z₂[θ] = Z₂[x]/f. The 2-radical I/2O is ker(Frob^k) on O/2O with 2^k ≥ n; this is exact linear algebra because Frobenius is additive in characteristic 2. Pass to the multiplier ring {x : xI ⊆ I}.
- Stop when the order is unchanged. Each step doubles the index, so there are at most v₂(index) ≤ D/2 steps.
- The maximality criterion is the standard Pohst–Zassenhaus theorem. It was not supplied, so it must be checked from its primary text.
- The output O_L is an exact finite object: a rational basis with denominators ≤ 2^{D/2}.
- O_L/rad = ∏ F_{q_i}. The local factors correspond to the primitive idempotents of the Frobenius-fixed subalgebra ≅ F₂^k. These are found deterministically, because every element of that subalgebra is idempotent: refine by products e·b and e(1−b).
- Lift idempotents with x ↦ 3x² − 2x³. Idempotent lifts are unique.
- The **actual** factor E_i is named exactly as e_i·L, where e_i is the unique idempotent with prescribed reduction mod 2. Mod 2^c, everything is exact finite data.
- An exact global uniformizer: π = Σ ẽ_i·b_i, where ẽ_i ∈ O_L is an idempotent mod 2^c (c ≥ 2), b_i ∈ m_i \ m_i², and 2^c ∈ m_i². Then v_i(π) = 1 for every i, and π is exactly rational.
- The β_j are exact lifts.
- No polynomial factorization, no Las Vegas step, and no factor approximant is needed.

**B2 — Exact-zero leak in the branch formula.**
- Stoll's (−1)^{deg a}(a − a₁f₁) is correct; I checked it componentwise for reduced divisors, where gcd(a₁, d) = 1.
- But it needs d = gcd(a, f) exactly.
- It may only be used for points whose branch support is certified by construction (initial torsion, named via idempotents).
- For computed points: if Res(a, f) is not visibly nonzero below its cap, the algorithm must ABORT or re-randomize. It must never call an approximate gcd.

**B3 — Root naming is unstated. Required certificate per component:**
- (i) A DAG-certified bound v_π(ũ − u) > 2e + v.
- (ii) v_π(r̃² − ũ) > 2e + v.
- Then u has a unique root in the ball {z : v_π(z − r̃) > e + v/2}. The other root −r lies at distance exactly e + v/2.
- Refinement must be Newton iteration z ← (z + u/z)/2 inside this ball. It must **never** recompute from a fresh solution of 2ξ = c, because that solution is non-unique and can flip the sign.

**B4 — "Unit precision 2e+1" is π-adic.** In 2-adic terms the requirement is ⌈(v_i + 2e_i + 1)/e_i⌉ plus guards.

## 3. Precision ledger (2-adic digits on O_L coordinates)

| Source of loss | Guard |
|---|---|
| Power basis ↔ O_L basis, including CRT idempotents (which lie in O_L) | ≤ v₂(index) ≤ D/2 |
| Valuation of component i | v_i ≤ V_i, from V_i·f_i ≤ v₂(Res(a, f)) + Σ_{j≠i} f_j·(pole bound)·e_j; requires a *visible* nonzero resultant below its cap, else ABORT |
| Label of component i | ⌈V_i/e_i⌉ + 3, plus division by π^v (≤ ⌈v/e⌉ + 1) |
| Teichmüller / q−1 power | 0 (unit derivative) |
| Square root | certificate (B3), then a fixed loss of 1 + ⌈v/(2e)⌉ per Newton step; non-accumulating under standard Hensel precision tracking |

All guards are polynomial in (g, B), given the caps.

## 4. Costs and ABORT clock

- Every residue-field operation is linear algebra over F₂ in dimension f_E ≤ n, or exponentiation by q using f_E squarings. Cost is poly(log q); there is no dependence on q itself.
- Round 2, collection (2e levels, each an F₂ solve), triangular solves and SNF on M ≤ 2n: poly(n, D, P) bit operations.
- The repaired backend is deterministic. Only optional sampling would add log₂(1/η′) draws.

## 5. Proof obligations and falsifiers

**Obligations:**
1. Primary-text check of the Round-2 maximality criterion (if using R1), or of every OM hypothesis in B1 (if keeping OM).
2. Visible-cap tests for all component valuations.
3. The B3 certificate on every root node.
4. π and β_j fixed once for the entire run.

**Falsifiers:**
- Computed dim U₁/U₁² ≠ d+1.
- A root that flips sign under refinement.
- Any label computed via an approximate gcd.

## Uncertainties

- The Pohst–Zassenhaus criterion is recalled from memory, not taken from supplied sources.
- DAG error certification for ũ and the resultant caps are outside this audit.
- I have not checked the matrix review's claim that "any root choice works".