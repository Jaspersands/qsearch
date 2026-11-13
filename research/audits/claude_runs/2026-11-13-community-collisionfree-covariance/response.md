# Operation 2: exact conditional covariance of Π A^{⊗λ}

## 0. Verdict

**The proposed bound is correct and essentially tight**, given three hypotheses (H1–H3 below). The most important is H1: Π must exclude repeated **edge indices** within a tuple.

- **Without H1 the bound is false.** If Π only excludes vertex repeats inside each p-set, but lets the same edge index appear twice in a tuple, explicit counterexamples exist:
  - λ = 3: any variance-v law gives a violation by a factor of order N.
  - λ = 2: the bound fails when the fourth moment exceeds 3v².
- **This is the partial-transpose trap.** Edge-distinctness is exactly what removes it.
- **Only second moments enter.** With H1 and independence, Cov(U) depends only on the means m_e and variances v_e. This holds because each edge index appears at most once per row tuple and once per column tuple.
- **Directional Chebyshev is valid** for a projector P that is independent of A given the latent parameters.
  - It yields a label-free one-sided lower bound ‖PU‖ ≥ (1−η)‖PV‖.
  - It does **not** control ‖P(U−V)‖ or the overlap. Those require Tr(P Cov P), which costs rank(P)·‖Cov‖.

Status labels used throughout:
- **[P]** proved here.
- **[A]** assumption, or an obligation imported from elsewhere.
- **[F]** finite control or counterexample.

## 1. Setup and hypotheses

Notation:
- Index set E with |E| = N. In the native model E = binom([n], p) and N = binom(n,p).
- θ denotes the latent parameters (labels x, plus a mask or anything else P depends on).
- A ∈ ℝ^E, with A_e = m_e(θ) + ξ_e.
- Tuples I = (I_1, …, I_λ) ∈ E^λ.
- Let 𝒟 = {I : I_s ≠ I_t for all s ≠ t} be the edge-distinct tuples.

Hypotheses:
- **H1 [A].** Π is diagonal on (ℝ^E)^{⊗λ}, Π = diag(π_I), with π_I ∈ {0,1} and π_I = 0 for I ∉ 𝒟.
  - Any stronger restriction is allowed, e.g. pairwise vertex-disjoint edges.
  - Nothing below uses π_I ∈ {0,1} beyond |π_I| ≤ 1, so diagonal weights in [−1,1] also work.
- **H2 [A].** Conditional on θ, the coordinates (ξ_e) are mutually independent, with E[ξ_e | θ] = 0 and v_e := E[ξ_e² | θ] < ∞.
  - Only 2λ-wise independence is used. **Pairwise independence is not enough**, because products over up to 2λ distinct coordinates must factor.
- **H3 [A].** v ≥ max_e v_e, computed conditionally on θ.
  - In the native normalization A_e = (Y_e − q)/√(q(1−q)), the variance is v_e = r_e(1−r_e)/(q(1−q)) with r_e = q + εf.
  - This can exceed 1, so the honest constant is v = max_e v_e, not 1.

Definitions: U = Π A^{⊗λ}, V = Π m^{⊗λ}, D = diag(v_e), and ‖·‖ is the operator norm (Euclidean norm for vectors). All statements are conditional on θ.

## 2. All moments [P]

For I ∈ 𝒟, U_I = π_I ∏_t A_{I_t}. The I_t are distinct, so H2 gives:

- **First moment:** E U_I = π_I ∏_t m_{I_t} = V_I. So E U = V.
- **Second moment:** for I, J ∈ 𝒟, view I and J as sets of λ distinct edges. Each edge occurs at most twice in the product U_I U_J (once from I, once from J). Hence
  E[U_I U_J] = π_I π_J ∏_{e∈I∩J}(m_e² + v_e) · ∏_{e∈IΔJ} m_e.
- **Covariance:**
  Cov(U)_{IJ} = π_I π_J [∏_{e∈I∩J}(m_e²+v_e) − ∏_{e∈I∩J} m_e²] ∏_{e∈IΔJ} m_e
  = π_I π_J Σ_{∅≠T⊆I∩J} ∏_{e∈T} v_e ∏_{e∈(I∩J)∖T} m_e² ∏_{e∈IΔJ} m_e.   (★)

Consequences:
- Only m_e and v_e = E ξ_e² appear. Third and fourth moments of ξ_e cannot appear: a ξ_e-power above 2 would need e twice in one tuple, which H1 forbids.
- All signs of m are retained. Nothing is dropped:
  - Pairs I, J that share labels or vertices but no edge index contribute exactly via (★).
  - Pairs with I ∩ J = ∅ have Cov = 0 exactly. Conditional on θ, label sharing induces no coordinate covariance.
- Directional moments: for u independent of A given θ, E⟨u,U⟩ = ⟨u,V⟩ and Var(⟨u,U⟩ | θ,u) = uᵀ Cov(U) u.
- **Moments not provided.** Fourth moments of U, needed for Var‖PU‖² or for null-threshold concentration, are not given by (★). They involve each edge up to four times across four tuples, hence E ξ³ and E ξ⁴. See §6.

## 3. Matching decomposition [P]

**Partial matchings.** A partial matching is a triple (S, T, σ):
- S ⊆ [λ] is a set of row positions;
- T ⊆ [λ] is a set of column positions, with |S| = |T| = j ≥ 1;
- σ : S → T is a bijection.

Define the operator K_{S,T,σ} on (ℝ^E)^{⊗λ} by
(K_{S,T,σ})_{IJ} = ∏_{s∈S} D_{I_s, J_{σ(s)}} · ∏_{s∉S} m_{I_s} · ∏_{t∉T} m_{J_t}.

**Lemma 1 (structure).** K_{S,T,σ} = P_α (D^{⊗j} ⊗ m^{⊗(λ−j)} (m^{⊗(λ−j)})ᵀ) P_βᵀ, where P_α and P_β are tensor-factor permutation unitaries.
- α lists S in increasing order, then [λ]∖S.
- β lists σ(S) in the same order, then [λ]∖T.

Proof:
- Reordering factors by α and β places matched pairs (s, σ(s)) in the first j slots. Each such slot carries D_{I_s,J_{σ(s)}}, which is exactly D^{⊗j}.
- The remaining row factors give ∏ m_{I_s} and the remaining column factors give ∏ m_{J_t}. This is the rank-one block m^{⊗(λ−j)}(m^{⊗(λ−j)})ᵀ.
- How unmatched row positions pair with unmatched column positions is irrelevant, because the block is rank one. ∎

Hence ‖K_{S,T,σ}‖ = ‖D‖^j ‖m‖^{2(λ−j)} ≤ v^j ‖m‖^{2λ−2j}.

**Lemma 2 (exact identity).** Let K = Σ_{j≥1} Σ_{|S|=|T|=j, σ} K_{S,T,σ}. Then under H1, Cov(U) = Π K Π.

Proof. Fix I, J ∈ 𝒟 (other entries are killed by Π on both sides). A term (S, T, σ) is nonzero only if I_s = J_{σ(s)} for all s ∈ S, since D is diagonal.
- Every edge e ∈ I ∩ J occupies a unique row position a(e) and a unique column position b(e), because both tuples are distinct.
- So nonzero terms correspond bijectively to nonempty T′ ⊆ I ∩ J, via S = a(T′), σ = b∘a⁻¹. Each such term equals ∏_{T′} v_e ∏_{I∖T′} m_e ∏_{J∖T′} m_e.
- Since ∏_{I∖T′} m · ∏_{J∖T′} m = ∏_{(I∩J)∖T′} m² · ∏_{IΔJ} m, the sum equals (★). ∎

Without H1, two different σ can select the same edge set, so the bijection fails. That is precisely the overcounting and partial-transpose failure in §5.

**Exact matching count.** The number of (S, T, σ) of size j is C(λ,j)² j!. Including j = 0 (the subtracted VVᵀ term), the total is the λ×λ rook number Σ_j C(λ,j)² j!.

## 4. Uniform bound

**Theorem 1 [P].** Under H1–H3, since ‖Π‖ ≤ 1:
‖Cov(U)‖ ≤ ‖K‖ ≤ Σ_{j=1}^{λ} C(λ,j)² j! v^j ‖m‖^{2λ−2j}.

For m ≠ 0, using C(λ,j) ≤ λ^j/j! so that C(λ,j)² j! ≤ λ^{2j}/j!:
‖Cov(U)‖ ≤ ‖m‖^{2λ} (exp(λ² v/‖m‖²) − 1).

For m = 0 the bound is λ! v^λ; the exponential form is not defined there.

**Tightness and cheapest counterexample attempts [F].**
- **λ = 1.** Cov = Π D Π, with norm ≤ v. The bound is v. Tight; no counterexample.
- **λ = 2.** I checked (★) against direct computation in every case:
  - Disjoint tuples: 0.
  - One shared edge (a=c): v_a m_b m_d.
  - (a,b) = (c,d): v_a m_b² + v_b m_a² + v_a v_b.
  - The swapped case is analogous via the cross matchings.
  - The bound is 4v‖m‖² + 2v².
- **m = 0, any λ (exactly attained).** Fix distinct a_1, …, a_λ and v_e ≡ v. Take x = (λ!)^{-1/2} Σ_{π∈S_λ} e_{a_π(1)} ⊗ ⋯ ⊗ e_{a_π(λ)} ∈ 𝒟.
  - Then ⟨x,U⟩ = √(λ!) ∏ ξ_{a_i}, with variance λ! v^λ.
  - The factor j! cannot be dropped. Already at λ = 2, N = 2 one gets 2v².
- **General m, v_e ≡ v (attained up to collision loss).** Take u = m^{⊗λ}/‖m‖^λ.
  - Each matching contributes exactly (mᵀDm)^j ‖m‖^{4λ−4j}/‖m‖^{2λ} = v^j ‖m‖^{2λ−2j}.
  - So without Π, uᵀKu equals the bound. With Π, the deficit is controlled by §7.
  - This is exactly the direction V used in §8.

**No counterexample to Theorem 1 exists:** it is proved. The only slack is in the exponential step.

## 5. The partial-transpose flaw: absent under H1, fatal without it

Each matched noise index in K couples a **row** position to a **column** position. That gives D^{⊗j}, with norm v^j. The dangerous alternative pairs two positions on the same side, which gives the vector vec(D) = Σ_e v_e e_e ⊗ e_e of norm ≈ v√N.

The partial-transpose pair makes this concrete:
- δ_{ac}δ_{bd} (row-to-column pairing) has norm 1.
- δ_{ab}δ_{cd} (same-side pairing) has norm N.

The two have the same entries up to index regrouping, but very different operator norms.

Under H1 a same-side pairing requires I_s = I_t, which is excluded. If Π permits repeated edge indices, the trap appears even after centering:

**Counterexample A (λ = 3, any law) [F].**
- Setup: Π = identity on E³, m = 0, v_e ≡ v, x = N^{-1/2} Σ_a e_a ⊗ e_a ⊗ e_1 (unit norm).
- Then ⟨x,U⟩ = N^{-1/2}(S ξ_1 + ξ_1³), where S = Σ_{a≠1} ξ_a².
- Cov(Sξ_1, ξ_1³) = E[S] μ_4 ≥ 0.
- Hence Var ≥ N^{-1} E[S²] v ≥ (N−1)² v³ / N.
- For a Rademacher variable this is exactly N v³ (with v = 1).
- This exceeds the bound 3! v³ = 6v³ once N ≥ 8.
- The covariance contains vec(D) ⊗ D ⊗ vec(D)ᵀ-type terms, with norm ≈ N v³.

**Counterexample B (λ = 2) [F].**
- Take x = e_1 ⊗ e_1. Then Var(ξ_1²) = μ_4 − v², which violates the bound 2v² iff μ_4 > 3v².
- For normalized centered Bern(q), μ_4 − v² = (1−2q)²/(q(1−q)). This exceeds 2 iff q < (3−√3)/6 ≈ 0.211.
- Example: q = 0.1 gives 7.1 > 2. At q = 1/4 there is no λ = 2 violation, but Counterexample A still applies.

**Conclusion.** "Remove repeated vertices within each p-edge" alone is insufficient. Π must be supported on edge-index-distinct tuples. A stronger vertex-collision restriction is fine, since it is a sub-projection.

## 6. Do only second moments suffice?

| Use | Only m_e, v_e needed? | Reason |
|---|---|---|
| Cov(U) | **Yes** (H1 + 2λ-wise independence) | Each edge appears ≤ 2 times in U_I U_J |
| Directional Chebyshev (§8) | **Yes** | Uses only Var⟨u,U⟩ = uᵀCov u |
| Var‖PU‖², null threshold for ‖PU‖², any high-probability or quadratic-statistic concentration | **No** | Four tuples share edges up to 4 times, so E ξ³ and E ξ⁴ enter; sparse Bernoulli has μ_4 ≈ 1/q after normalization |
| Without H1, even Cov(U) | **No** | Counterexamples A and B |

Independence must be at least 2λ-wise, conditional on everything P depends on.

## 7. ‖V‖ versus ‖m‖^λ (collision loss) [P]

We have ‖m^{⊗λ}‖² − ‖V‖² = Σ_{I∉supp Π} ∏_t m_{I_t}². A union bound over the position pair (s,t) at which a tuple is "bad" gives
‖V‖² ≥ ‖m‖^{2λ} (1 − C(λ,2) B/‖m‖⁴),
where B = Σ_{bad (e,e′)} m_e² m_{e′}².

- **Edge-distinct Π:** B = ‖m‖_4⁴.
- **Vertex-disjoint Π:** B ≤ (max m²)² · #{(e,e′) : e ∩ e′ ≠ ∅} ≤ (max m²)² · N p C(n−1, p−1).
  - Since ‖m‖⁴ = (avg m²)² N², the loss fraction is ≤ C(λ,2) (max m²/avg m²)² p²/n ≤ (ℓ²/2n) · R_x², where R_x = max f²/avg_S f_x(S)².

Native application, as an obligation **[A]**:
- |f| is bounded by a constant depending on (k,p), so max f² = O(1).
- avg f_x² must be bounded below. For uniformly random labels, E f² = k((k−1)/k²)^p + k(k−1)k^{−2p} > 0. Concentration over typical or balanced x must still be proved; it is not proved here.
- Given that, ‖V‖² ≥ (1 − O(ℓ²/n)) ‖m‖^{2λ}. This confirms the contract's ℓ²/n.

## 8. Directional Chebyshev for P independent of A [P, with obligations]

**Hypothesis H4 [A].**
- (θ, P) is such that, conditional on (θ, P), A satisfies H2 with mean m(θ).
- In particular P ⟂ A | θ, where θ includes every latent quantity P is built from.
- **Mask caveat.** If a mask or clone split is used, θ must include the mask, and m must be the mask-conditional mean. The parent falsifier shows independence fails when conditioning on x alone. That is a statement about the wrong conditioning, not about this lemma.
- Whether operation 1 delivers H4 exactly, or up to a TV coupling that must then be added, is outside scope and is an open obligation.

**Theorem 2.** Let P be an orthogonal projector with PV ≠ 0, and set u = PV/‖PV‖ ∈ range P. Then u is (θ,P)-measurable, and for any η ∈ (0,1):

Pr(‖PU‖ < (1−η)‖PV‖ | θ, P) ≤ Pr(⟨u,U⟩ < (1−η)‖PV‖ | θ, P) ≤ ‖Cov(U)‖ / (η² ‖PV‖²).

Proof:
- ⟨u,U⟩ = ⟨u,PU⟩ ≤ ‖PU‖.
- E⟨u,U⟩ = ⟨u,V⟩ = ‖PV‖.
- Var = uᵀ Cov u ≤ ‖Cov‖.
- Apply Chebyshev. ∎

Unconditional version. Let G be the event {‖PV‖ ≥ c‖V‖, ‖V‖² ≥ γ ‖m‖^{2λ}, m ≠ 0}. Then

Pr(‖PU‖ < (1−η)‖PV‖) ≤ Pr(Gᶜ) + sup_G (exp(λ²v/‖m‖²) − 1)/(η² c² γ).

Remarks on Theorem 2:
- The statistic ‖PU‖ is label-free, even though u depends on x. No averaging of label-dependent directions occurs, and Lemma 58 is not used.
- **Threshold arithmetic [A on β, κ_x].**
  - ‖m‖² = β² Σ_S f_x(S)² ≈ β² κ_x N, where κ_x is the average of f_x², N ≈ n^p/p!, and β ~ n^{−p/4} ℓ^{1/2−p/4} (up to logarithms).
  - Then λ² v/‖m‖² ≈ λ² v p!/(κ_x n^{p/2} ℓ^{1−p/2}) = O(ℓ^{p/2+1}/n^{p/2}) = O((ℓ/√n)^p · ℓ^{1−p/2}).
  - This → 0 for ℓ = o(√n), fixed p ≥ 4. It matches the contract's λ²/(β² n^p) up to the constants p!, κ_x, and v.
  - The j = λ term λ! (v/‖m‖²)^λ is dominated by this and is harmless.

**What Theorem 2 does NOT give:**
1. **No two-sided or norm control.**
   - E[‖P(U−V)‖² | θ,P] = Tr(P Cov P) ≤ rank(P) · ‖Cov‖.
   - Moreover Tr Cov ≈ |supp Π| ((1+β²f²)^λ v^λ − …) ≈ N^λ ≫ ‖V‖² ≈ (β² κ N)^λ.
   - So ‖U‖ ≫ ‖V‖: the raw overlap ⟨U,V⟩/(‖U‖‖V‖) is tiny.
   - A lower bound on the cosine ⟨PU,u⟩/‖PU‖ needs Markov on the trace. Requirement: rank(P) · ‖Cov‖ ≪ c² ‖V‖², i.e. rank(P)(e^{λ²v/‖m‖²} − 1) ≪ c²γ.
2. **No detection by itself.** One must compare with the null (m = 0):
   - There E‖PU‖² = Tr(P Π K₀ Π P) ≤ rank(P) λ! v₀^λ, where K₀ is the λ-matching part.
   - On symmetric directions the null fluctuation is ≈ λ! v₀^λ per direction, i.e. an ordered-encoding λ! inflation.
   - So the condition needed is ‖PV‖² ≫ rank(P) λ! v₀^λ, plus fourth-moment concentration of ‖PU‖² (§6).
3. **The hypothesis ‖PV‖ ≥ c‖V‖ for a P independent of A is the actual crux** (spectral, out of scope). Theorem 2 only transfers it to U. Failed attacks here do not imply it holds.

## 9. Proof obligations and falsifiers

**Obligations:**
- **O1.** Π ⊆ edge-index-distinct tuples. Exhibit the support explicitly in the ordered tensor encoding.
- **O2.** Conditional mutual (≥ 2λ-wise) independence of A given (θ, mask, P), with m defined as that conditional mean.
- **O3.** v = max of conditional variances. This is not 1 in the native normalization.
- **O4.** A lower bound on κ_x over the label set used, to get ‖V‖² ≥ (1 − O(ℓ²/n)) ‖m‖^{2λ} and ‖m‖² ≫ λ² v.
- **O5.** ‖PV‖ ≥ c‖V‖ with Pr(Gᶜ) → 0, for P built only from data independent of A given θ.
- **O6.** For overlap or detection claims, a rank(P)-paid trace bound plus a fourth-moment null concentration.

**Falsifiers:**
- **F1.** Any admissible Π that contains a tuple with a repeated edge index. Counterexample A then gives Cov norm ≳ N v³ at λ = 3.
- **F2.** A P that depends on A given θ, e.g. through a shared mask without conditioning on it. Theorem 2's conditional mean and variance then no longer apply.
- **F3.** A label configuration with κ_x small or ‖V‖ ≪ ‖m‖^λ.
- **F4.** rank(P)(e^{λ²v/‖m‖²} − 1) ≳ c² for any claimed overlap or cosine statement.

**Summary.** Operation 2's covariance bound is a correct finite-dimensional theorem under O1–O3, and essentially tight. It is a single-direction second-moment fact; it does not establish any spectral overlap or detection guarantee.