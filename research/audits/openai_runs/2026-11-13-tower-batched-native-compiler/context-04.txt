# Parity-constrained descent: exactness proof, coordinate recursion, height reset, and exact clock

## 0. Verdict

**What is proved.** The proposed descent is algebraically exact. The answer to the critical question is yes: the kernel is exactly ⟨([d],0)⟩, even when the first pair space contains pairs (1,c≠0). This requires the norm-compatible space to be given by a basis **of pairs**.

**The coordinate gap.** The descent alone is not a complete basis algorithm. Removing the kernel requires the coordinates of (d,0) in the lower basis. I give a recursive coordinate procedure (two lower coordinate calls per level) that supplies them. It needs no characters, no Chebotarev and no GRH.

**The clock.** Naive charging of heights does not give a polynomial bound. Even with C‑linear conics, the size recurrence squares its slope at every level, so the bound is 2^{Θ(N)} or worse.

Two explicit **height resets** make every node's input and output sizes bounded by a level‑independent polynomial Z(N,B). This uses the charged factoring of polynomial‑bit integers that is already needed to read β‑supports. With 2N−1 nodes, the result is the conditional theorem in §5.

**Remaining gate.** The only unproved ingredient is a uniform polynomial relative-conic oracle on inputs of size ≤ Z. With resets, a generic polynomial conic bound suffices; the C‑linear hypothesis is no longer needed. This is a reduction, not a tower algorithm.

## 1. Notation and representations

- **Fields and sets.** K is a number field, n=[K:Q]. S⊇{dyadic, ramified, real places}. S_K is the set of places of K above S.
- **The task group.** For outside‑S parity divisors J=(J_1..J_r):
  G_K(S;J) = {([x],c) ∈ K*/K*² × F₂^r : v_P(x) ≡ Σ c_i J_i(P) mod 2 for all P∉S_K}.
  This is exactly the output of U_K. The c‑projection is part of each vector.
- **Bit height.** For x = (integer vector)/den in the supplied integral basis ω, set ℓ(x) = log₂ max(den, |coefficients|). The bit size is n·ℓ(x)+O(n).
- **Weil height.** h is the absolute logarithmic Weil height. Let Ω=(σ_i(ω_j)).

**Lemma 0 (conversion).**
- h(x) ≤ ℓ(x) + log(n·max|σ_i(ω_j)|) + 1.
- ℓ(x) ≤ 2n·h(x) + log(n‖Ω⁻¹‖) + 1.
- Σ_{P∈supp(x)} log NP ≤ 2n·h(x).

*Proof.*
- The finite part of n·h is log N(denominator ideal 𝔡), which is ≤ n log den. The archimedean part is ≤ n log⁺max|σ(x)|. This gives the first bound.
- Conversely, N(𝔡)∈𝔡, so den ≤ N𝔡 ≤ e^{nh}. Also |σ(den·x)| ≤ e^{2nh}. Invert Ω to get the second bound.
- The third bound follows from Σ_v |log|x|_v| ≤ n·h(x) + n·h(1/x).

**Consequence for conics.** A conic bound h(β) ≤ C·h(a)+P is, in bit terms, ℓ(β) ≤ 2nC·ℓ(a)+poly. This is a level‑dependent constant.

Projective points (x:y:z) may not have coprime integral coordinates because of class-group obstructions. I therefore only use the affine β = (x+y√d)/z, with h(β) ≤ 2h_proj + ½h(d) + log 2.

Throughout, log‖Ω⁻¹‖ and log|D_{F_j}| ≤ log|D_{F_h}| are poly(B).

## 2. Theorem A (exactness of the descent)

**Setting.** L=F(√d), d∈F*∖F*², J_1..J_r outside‑S parity divisors of L (duplicates allowed). Let NJ_i be the norm parity:
- 0 at inert primes,
- J_i(P)+J_i(P′) at a split prime p = PP′.

Let H = {(a,c) ∈ G_F(S;NJ) : (a,d)_v = 1 for all v ∈ S_F ∪ {real places}}.

**(i) The norm tag lands in H.** (x,c) ↦ (Nx,c) maps G_L(S;J) into H. Every a in H is a norm.

*Proof.*
- At an outside‑S prime p (unramified), the valuation of Nx is 2v_P(x) if p is inert, and v_P(x)+v_{P′}(x) if p splits. So the parity of Nx is Σc_i NJ_i.
- Nx is a local norm everywhere, so the Hilbert symbols vanish.
- For (a,c)∈H at p∉S: if p is inert, v_p(a) ≡ 0, so (a,d)_p = 1. If p splits, d is a local square. (Outside S, v_p(d) is even.)
- So a is a local norm everywhere, and by the Hasse norm theorem (L/F cyclic), a ∈ N(L*).

**(ii) The mismatch descends.** Let (a_k,c_k)_{k≤s} be an F₂‑basis of H **as pairs**, and choose β_k with Nβ_k ∈ a_k F*². Then D_k := div_{∉S}β_k + Σ(c_k)_i J_i is ≡ pullback(R_k) mod 2, for a unique outside‑S parity divisor R_k.

*Proof.*
- At a split p: D_k(P)+D_k(P′) ≡ v_p(a_k) + Σ(c_k)_i NJ_i(p) ≡ 0. So the two parities are equal.
- At an inert prime the single parity is arbitrary.
- Pullback is injective on parities at unramified primes, which gives uniqueness.
- Replacing β_k by β_k·w with w∈F* keeps the norm condition and replaces R_k by R_k + div w.

**(iii) Exact sequence.** Define Φ: G_F(S;R) → G_L(S;J), (γ,u) ↦ (γ·Π β_k^{u_k}, Σ u_k c_k). Then Φ is a surjective homomorphism with kernel exactly {0, ([d],0)}.

*Well defined.* The divisor parity of γΠβ^u is pullback(Σu_kR_k) + Σu_k(D_k + Σ c_kJ) ≡ Σ(Σ_k u_k c_k)J.

*Kernel.*
- Suppose γΠβ^u ∈ L*² and Σu_kc_k = 0. Take norms: γ²·Π(a_k t_k²)^{u_k} ∈ F*², so Π a_k^{u_k} ∈ F*².
- Hence Σu_k(a_k,c_k) = (1,0) in G_F(S;NJ). Independence of the pairs forces u=0.
- Then γ ∈ F*∩L*² = F*² ∪ dF*².
- Since v_p(d) is even outside S, (d,0) ∈ G_F(S;R), and it is nonzero because d∉F*².

*Answer to the critical question.* A basis element (1,c_k) with c_k≠0 cannot enter the kernel because its c‑part is nonzero. The kernel would be larger only if:
- H were replaced by a basis of its a‑projection, or
- the lower outputs were merely spanning sets.

*Surjectivity.*
- Take (α,c) ∈ G_L(S;J). By (i), (Nα,c) = Σu_k(a_k,c_k). Set x = αΠβ_k^{u_k}. Then Nx = σ² with σ∈F*.
- **Trace identity:** (x±σ)² = x(Tr x ± 2σ). If both x+σ and x−σ were 0, then σ=0, which is impossible. So either x=∓σ∈F*, or x ≡ g := Tr x ± 2σ ∈ F* mod L*².
- The parity of div x is Σu_kD_k = pullback(Σu_kR_k). By injectivity of pullback, (g,u) ∈ G_F(S;R).
- Then Φ(g,u) = (α·Πβ^{2u}, c) = (α,c). ∎

**Corollary.** dim G_L(S;J) = dim G_F(S;R) − 1. The norm‑tag image may be a proper subspace of H; the R‑targets absorb this obstruction. The full group F(S∪E,2) is never expanded.

**Finite control (sanity checks, not evidence of correctness).**
- F=Q, L=Q(i), S={2,∞}: H=⟨2⟩, β=1+i, R=0. G_Q = ⟨−1, 2, (1,e₁)⟩ maps to ⟨i, 1+i⟩. The kernel is (−1,0) = (d,0).
- F=Q, L=Q(√−5), S={2,5,∞}: H=⟨5⟩, β=√−5. Images {−1, 2, √−5}, of dimension 3 = dim L(S,2). The kernel is (−5,0).

## 3. Proposition B (exact coordinates; kernel removal)

U_K stores its basis together with all node data. Coord_K(S;J)(x,c) returns the coordinates of (x,c) in that basis.

**Base case.** U_Q(S;J), with J_i given as sets of rational primes outside S with product n_i, has basis:
- (−1,0),
- (p,0) for p∈S,
- (n_i, e_i) for each i.

These are independent because the c‑parts are independent; duplicates are allowed and n_i=1 is allowed. For Coord_Q, divide by Π n_i^{c_i}, then read the sign and the parities v_p for p∈S by trial division. No factoring is needed.

**Level step: Coord_L(x,c).**
1. Compute Coord_F(S;NJ)(Nx, c). Convert to H‑coordinates u by linear algebra.
2. Form x′ = xΠβ_k^{u_k}. Compute σ = √(Nx′) in F. This is deterministic polynomial: factor X²−Nx′ over F, or use Hensel lifting.
3. Set g = x′ if x′∈F; otherwise g = Tr x′ ± 2σ (whichever is nonzero).
4. Compute e = Coord_F(S;R)(g,u).
5. If e_{l₀}=1, replace e by e + e^{(d)}. Here l₀ is the index of the basis vector that was dropped, and e^{(d)} = Coord_F(S;R)(d,0) is stored.

**Correctness.** By Theorem A(iii), Φ(g,u) = (x,c). Since e^{(d)}_{l₀}=1, the dropped vector can be eliminated.

**Kernel removal in U_L.** Compute e^{(d)} with one Coord_F(S;R) call. Pick any l₀ with e^{(d)}_{l₀}=1 and output {Φ(b_l)}_{l≠l₀}. This is a basis, by Theorem A.

**Cost.** Inputs grow as ℓ_{j−1} ≤ 2ℓ_j + poly, so over depth j the size is ≤ 2^j·(ℓ+poly) ≤ N(ℓ+poly). There are 2^j leaves, so one Coord call at level j costs ≤ 2^j·poly(N,B,2^jℓ).

## 4. Height-reset lemmas (unconditional; LLL plus charged factoring)

**Lemma C1 (divisor reset).**
- *Statement.* Given an integral squarefree ideal R of K, LLL in R⁻¹ under the Minkowski embedding gives w∈R⁻¹ with M = wR integral, log NM ≤ Λ_n := n²/2 + ½ log|D_K|, and ℓ(w) ≤ log NR + poly(n,B).
- *Proof.* Minkowski's bound and the LLL factor give |N(w)| ≤ 2^{n²/2}·|D|^{1/2}/NR. Then N(wR)·w‑denominators are controlled by NR. Lemma 0 converts to bit size.
- *Use.* Factor N(M), an integer of poly bits. Replace β_k by β_kw_k, so the new target R′_k is the odd outside‑S part of M. By Theorem A(ii) this is legitimate.

**Lemma C2 (squareclass reset).**
- *Statement.* Suppose the factorization of (z) is known. Write (z) = I·J² with I squarefree; J is fractional. Use the weighted lattice φ(y) = (σ_j(y)/|σ_j(z)|^{1/2})_j on J, which has covolume ≍ |D|^{1/2}·NI^{−1/2}. LLL gives y with Q := ‖φ(y)‖² ≤ 2^{O(n)}|D|^{1/n}.
- *Proof.* Put q_j = |σ_j(y)|²/|σ_j(z)|. Then q_j ≤ Q and Π q_j = NK²/NI ≥ 1/NI, where (y)=JK and K is integral. So for w = z/y²:
  - log max|σ_j(w)| ≤ log NI + (n−1) log Q,
  - log NK ≤ ½ log NI + (n/2) log Q,
  - NK²·w is integral.
- *Conclusion.* ℓ(w) ≤ O(log NI) + poly(n,B), **independent of ℓ(z)**. Factor N(K) so that factorizations propagate.

## 5. Algorithm with resets and Theorem D (clock)

**Node procedure.** U_{F_i}(S;J) with L=F_i, F=F_{i−1}:
1. Compute NJ. One child call U_F(S;NJ).
2. Evaluate Hilbert symbols (·,d_i)_v on the child basis. Compute a basis of H as pairs. Form the products a_k and optionally reset them with C2.
3. One relative conic call per k for β_k. Factor the numerator and denominator norms of β_k. Form R_k and reset it with C1.
4. One child call U_F(S;R′).
5. Form α_l = γ_lΠβ^{u_l} and reset with C2.
6. Remove the kernel via §3.

**Invariant (induction on level, with bounds independent of level).**
- Targets have log‑norm ≤ Λ := N²/2 + ½ log|D_{F_h}|. Norm push‑down does not increase log‑norm, and C1 resets R.
- Along any branch, r ≤ r_max := h·D_max, because r_child ≤ dim G_F(S;NJ) ≤ D_F + r.
- D_max ≤ N(|S_Q|+1) + log₂ h_max = poly(N,B). This uses the standard unconditional class-number bound h ≤ 2^{O(n)}|D|^{1/2}(log|D|)^{n−1}/R together with Friedman's lower bound R > 0.2; both are cited, not reproved here.
- Every output element has ℓ ≤ Z := O(r_max·Λ + N·Σ_{p∈S_Q} log p + N² + log|D_{F_h}| + log‖Ω⁻¹‖). This holds because, by C2, the reset size depends only on the odd support, which lies in S ∪ supp(ΣcJ).
- So each node sees child outputs ≤ Z, conic inputs ≤ g·Z, conic outputs ≤ p_conic(gZ), and factorization inputs ≤ N·p_conic(gZ) bits.

**Theorem D (conditional on oracles).** Assume:
- a factoring oracle for integers,
- a relative conic oracle: on input F_{j−1}, d_j and a with all (a,d_j)_v = 1 and ℓ(a) ≤ gZ, it returns β∈F_j with Nβ ∈ aF*² in time and size p_conic(·), uniformly in j.

Then a basis of F_h(S_h,2), with exact coordinate maps, is computed with bounded error:
- **U nodes:** exactly 2N−1, namely 2 lower U calls per internal node and N leaves U_Q (elementary).
- **Conic calls:** ≤ (2N)·g_max, with g_max ≤ D_max + r_max, each on input of size ≤ gZ.
- **Factorizations:** O(N·g_max), each of ≤ poly(N,B)-bit integers.
- **Coordinate work:** one Coord call per U node, total ≤ Σ_i 2^{h−i}·2^i·poly = O(N log N·poly).
- **Total time:** (2N)·[g·Conic(gZ) + O(g)·Fact(N·p_conic(gZ)) + poly(N,B)] + O(N log N·poly(N,B)), times log(1/η) for amplification.

This is polynomial whenever Conic is polynomial; a generic polynomial bound suffices. The result is unconditional apart from the oracles: no GRH, no auxiliary prime, no class group or units. Randomness enters only through prime decomposition (Las Vegas), the oracles, and LLL precision, which is deterministic.

## 6. Recurrences without resets (bounds only, not runtimes)

Let Σ_j(T) be the output element size at level j, with targets of size T.

**No reset, C‑linear conic.** The second child's targets have size ≈ s·C·g·Σ_{j−1}(T), and that child scales them again:

Σ_j(T) ≤ Σ_{j−1}(T + sCgΣ_{j−1}(T+P) + sP) + sCgΣ_{j−1}(T+P) + …

Write Σ_j(T) ≤ A_jT + B_j. Then:
- A_j ≤ K·A_{j−1}², with K = 1+2sCg (bit‑level C carries a factor 2n).
- So A_h ≤ K^{N−1}.
- The recurrence itself cannot be solved better than A_h ≥ 2^{2^{h−1}} = 2^{N/2}.

**No reset, generic conic p(x) ~ x^k.** The degrees satisfy e_j ≈ k·e_{j−1}², giving sizes up to T^{k^{N−1}}.

**One reset only (either C1 or C2).** Sizes grow multiplicatively along h edges:
- C‑linear conic: (1+sCg)^h = exp(O(log N·log(NB))), quasi‑polynomial.
- Generic conic: log size ~ k^h = N^{log₂k}, so the bound is exponential.

**Both resets.** Sizes are flat at Z, as in Theorem D. The C‑linear versus generic distinction matters only in the tiers above.

## 7. Exact remaining gate, proof obligations, falsifiers

**Gate.** A uniform polynomial oracle Conic_j for x² − d_j y² = a z² over F_{j−1}, on inputs of size ≤ gZ.

This is still Kutas Remark 22 territory. If Conic_j is implemented through the tower itself, so that c_j ≥ k·u_{j−1} (for example via Koprowski's need for complete base squareclasses), then u_j = 2u_{j−1} + g·c_j gives u_h ≥ (gk)^h = N^{log₂(gk)}. That is quasi‑polynomial for g = poly(N), unless gk = O(1). Koprowski's Appendix A height issue would then sit inside the oracle; the resets do not address it.

**Proof obligations to write out.**
1. Numerical-precision analysis for the weighted LLL in C2 and the LLL in C1.
2. Polynomial-time dyadic Hilbert symbols (a,d)_v.
3. Prime decomposition from the supplied maximal orders.
4. HNF of J = ΠP^{⌊e/2⌋} for exponents of poly size.
5. Explicit constants in Z.

**Falsifiers.**
- Any field with nontrivial Cl[2] where dim G_L(S;J) ≠ dim G_F(S;R) − 1. Theorem A is proved, so this would locate an error in the theorem or in an implementation.
- A family where Conic on inputs of size ≤ Z requires superpolynomial output size. This refutes the oracle hypothesis, not the descent.
- A node where C2 fails to bound ℓ by O(log NI) + poly.

Classically this is a polynomial algorithm relative to factoring and the conic oracle. With Shor substituted for factoring it is a quantum composition. It implies no classical hardness and no speedup beyond factoring.