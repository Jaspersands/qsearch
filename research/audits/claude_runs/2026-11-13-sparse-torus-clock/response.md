# Verdict on the analytic and bit-clock half of the torus-vertical proposal

**The analytic half holds.** I found no native counterexample to the archimedean claim. The cheapest attacks either fail or only defeat sloppy versions of it:

- **Aliasing at grid roots of unity.** This defeats a dyadic grid whose resolution ignores log-degree. It does not defeat the paid grid.
- **Norm-versus-branch cancellation (the Eisenstein family in the constants note).** Cancellation inside the norm does not hurt individual branches once a Cauchy upper bound is added.
- **Conjugate misalignment (the (c,c) versus (c,c⁻¹) pair).** Joint branch evaluation separates the two tuples correctly.

Below is a quantitative lemma that supplies the arch rows directly, with a self-checking acceptance certificate. Four repairs to the parent wording are needed (§4). The root-finder used for completeness is an unverified import; soundness never uses it.

Unchanged and preserved:
- Finite-place rows are **UNPAID**.
- The root-of-unity phase step is **UNPAID**.
- Arch rows alone cannot solve fullRel (§5).

## 1. Setup

Notation follows GENERAL_SPARSE_CONSTANTS_ATTACK §1, whose bounds I import as previously reviewed repository results:
- Every coefficient of f and of each u_i is written p/D, with ‖p‖₁, ‖D‖₁ ≤ H = 2^b.
- d₀ = (L+1)β, e₀ = (δ+1)d₀.
- M(u_i) = A_i/D^δ and M(f_Y) = J/D^(δ−1).
- Entry, determinant and adjugate norms are bounded by U and V = δ!U^δ.

Let 𝒫 = {D, det J, det A_1, …, det A_k}. These are k+2 polynomials with the following properties:
- Each is a **nonzero integer** polynomial.
- D ≠ 0 trivially; det J ≠ 0 because f is separable in characteristic 0; det A_i ≠ 0 because u_i ≠ 0.
- Each has ‖P‖₁ ≤ V and total degree ≤ Δ := δe₀.
- Exponents are assumed nonnegative. For Laurent inputs, replace degree by Σ|a_j|.

Define:
- t* := 8(k+2)·lnV + 1
- N := ⌈log₂(2πΔV) + t*/ln2⌉
- Λ := t* + ln(2H)
- Λ_u := 2δ²Λ + δ lnδ
- Σ := δ²(Λ+1)

## 2. Lemma (archimedean rows)

Draw φ uniformly from (2^(−N)ℤ/ℤ)^s and set z = exp(2πiφ). This is an explicit dyadic root of unity, not a hidden transcendental point.

**(A) Good point.** With probability at least 7/8, every P ∈ 𝒫 satisfies |P(z)| ≥ e^(−t*).

**(B) Magnitudes on the good event.** Suppose every P ∈ 𝒫 satisfies |P(z)| ≥ e^(−t*). Then:
- f_z has δ simple roots y_j, each with |y_j| ≤ e^Λ.
- Root separation satisfies ln(1/sep) ≤ Σ.
- For all i, j: |ln|u_i(z, y_j)|| ≤ Λ_u.

**(C) Certificate.** A deterministic certified-interval procedure CERT(φ, z_1..z_δ, p) takes dyadic candidate roots and either REJECTs or ACCEPTs.
- *Soundness (unconditional).* On ACCEPT it returns L̃ ∈ ℚ^(δ×k) such that:
  - D(z) ≠ 0;
  - f_z has exactly one root y_j in each of δ disjoint disks;
  - every u_i(z, y_j) ≠ 0;
  - |L̃_ji − ln|u_i(z, y_j)|| ≤ 2^(−p) for every i, j.
- *Completeness.* On the event of (B), CERT accepts whenever every candidate satisfies |z_j − y_j| ≤ ε_p, where ln(1/ε_p) = p·ln2 + O(δ³(Λ+1)).
- *Cost.* The working precision is P = O(p + δ³(Λ+1)) bits. The time is poly(input size, s, δ, k, N, P).

**(D) Joint embeddings.** Suppose CERT accepts, and let C be the algebraic closure of ℚ in F. Then:
- Each branch j gives a field embedding σ_j: C → ℂ such that u^e(z, y_j) = σ_j(u^e) for **all** e ∈ Alg simultaneously.
- Every embedding of C occurs exactly δ/[C:ℚ] times among σ_1..σ_δ.
- Let B_alg be the k×r Alg basis, with entries at most Balg. Then L̃·B_alg approximates (ln|σ_j(c_m)|)_{j,m} entrywise within k·Balg·2^(−p).
- (1/δ)·Σ_j |ln|σ_j(c)|| is exactly the place-weighted archimedean part of the log norm on C (the Weil-height normalization over embeddings). No conjugate grouping, constant-field basis or knowledge of [C:ℚ] is needed.

**(E) Clock.** Take p = p_target + ⌈log₂(k·Balg)⌉ and repeat for ⌈log₈(1/η)⌉ independent trials.
- The procedure outputs the rows or FAIL; FAIL has probability at most η, plus the root-finder's own failure budget if it is randomized.
- It never outputs wrong rows.
- All sizes are polynomial in native bits:
  - lnV = O(δ²(b + log δ + log d₀));
  - t*, Λ and N are O(kδ²(b + log(δd₀)));
  - Λ_u = O(kδ⁴(b + log(δd₀)));
  - P = O(p_target + log(kBalg) + kδ⁵(b + log(δd₀))).
- Degrees enter only through log Δ and the exact reduction of a·φ mod 1. log Balg is polynomial by the constants note.

## 3. Proof

**1. Iterated Jensen, m(P) ≥ 0.** Induct on s.
- *Case s = 1.* m(P) = ln|a_n| + Σ ln⁺|α| ≥ ln|a_n| ≥ 0.
- *Inductive step.* Write P = Σ_{m≤n} c_m(z′)·T₁^m with c_n ≠ 0. For almost every z′ on the subtorus, univariate Jensen gives ∫ln|P(·, z′)| ≥ ln|c_n(z′)|.
- *Integrability.* The inner integral satisfies ∫ln⁻|P(·, z′)| ≤ ln‖P‖₁ − ln|c_n(z′)|. By Tonelli and induction, ln|P| ∈ L¹.
- *Conclusion.* Fubini then gives m(P) ≥ m(c_n) ≥ 0.

**2. Markov tail.**
- Since ln⁺|P| ≤ ln‖P‖₁ on the torus, E ln⁻|P| = E ln⁺|P| − m(P) ≤ ln‖P‖₁.
- Markov's inequality gives Pr_cont[|P| < 2e^(−t)] ≤ ln‖P‖₁/(t − ln2).

**3. Transfer from continuous measure to the grid (repair (i)).**
- *Coupling.* Let ξ be uniform on the cell [0, 2^(−N))^s. Then φ + ξ is uniform on the continuous torus.
- *Lipschitz bound.* |P(e^(2πiφ)) − P(e^(2πi(φ+ξ)))| ≤ ‖P‖₁ · 2π · Δ · 2^(−N) ≤ e^(−t*).
- *Transfer.* Hence Pr_grid[|P| < e^(−t*)] ≤ Pr_cont[|P| < 2e^(−t*)].
- *Union bound.* Summing over 𝒫 gives a total of at most (k+2)lnV/(8(k+2)lnV + 1 − ln2) < 1/8.

**4. Branch magnitudes (repair (ii)).** On the good event:
- *Coefficient sizes.* Every coefficient a_c(z) and u_{i,c}(z) has modulus at most H·e^(t*).
- *Root bound.* By the Cauchy bound, |y| ≤ R := 1 + H·e^(t*) ≤ e^Λ.
- *Upper bound on branches.* |u_i(y_j)| ≤ δ·R^δ.
- *Norm lower bound.* det M(u_i)(z) = det A_i(z)/D(z)^(δ²) = Π_j u_i(y_j), so |Π_j u_i(y_j)| ≥ e^(−t*)·H^(−δ²).
- *Lower bound on each branch.* Dividing the norm by the other δ−1 branch upper bounds gives ln|u_i(y_j)| ≥ −(2δ²Λ + δ lnδ).
- *Discriminant.* det M(f_Y) = det J/D^(δ(δ−1)) = ±disc(f_z), so |disc| ≥ e^(−δ²Λ).
- *Separation.* Isolating one squared root difference in the discriminant product gives sep ≥ √|disc| / (2R)^(δ(δ−1)/2 − 1).

**5. Evaluation and certificate (self-contained Rouché, repair (iv)).**
- *Monomials.* Compute z^a = exp(2πi·{a·φ}), with {a·φ} computed exactly from the binary exponent a. Elementary function evaluation is used for exp, π and ln.
- *Coefficients.* Compute a_c(z) with certified error ε_a. Certify |D(z)| > 0 by an interval enclosure.
- *Rouché test.* Form g = Π(Y − z_l) exactly. On the circle |Y − z_j| = r, bound |f_z − g| ≤ E_j(r) := Σ_c(|ã_c − g_c| + ε_a)(|z_j| + r)^c. Accept the disk if:
  - E_j(r) < r·Π_{l≠j}(|z_j − z_l| − r), and
  - the disks are pairwise disjoint.
- *Bijection.* Rouché then puts exactly one root of f_z in each of the δ disks. This certifies simple roots and gives a bijection between candidates and roots.
- *Value test.* Evaluate u_i(z_j) and enclose |u_i(y_j) − u_i(z_j)| ≤ Lip·r, with Lip ≤ δ²R^(δ+1). Accept if Lip·r ≤ |u_i(z_j)|·2^(−p−2).
- *Logarithm.* Then |ln|u_i(y_j)| − ln|u_i(z_j)|| ≤ 2^(−p−1). Compute ln|·| to 2^(−p−1).
- *Completeness.* With r = (2E/(sep/2)^(δ−1)) and the bounds of step 4, the bound on ε_p in (C) suffices.
- *Root-finding import (UNVERIFIED).* Producing candidates within ε_p in poly(δ, P) time needs a complex root approximation algorithm, for example a splitting-circle or Pan-type method. This is not a supplied source. It affects only completeness and runtime, never soundness.

**6. Joint embeddings (repair (iii)).**
- *Branch germs.* On ACCEPT, D(z) ≠ 0 and the roots are simple. By the implicit function theorem each root extends to a holomorphic germ y_j(T) at z.
- *Field embeddings.* Holomorphic germs in s variables form a domain; let 𝓜 be its fraction field. Y ↦ y_j(T) gives δ **distinct** ℚ(T)-embeddings ψ_j: F → 𝓜, since f is irreducible and the y_j(z) are distinct. These exhaust all δ embeddings.
- *Constants evaluate correctly.* Let c ∈ C have minimal polynomial μ. In the domain 𝓜, Π(ψ_j(c) − α) = 0 over the roots α of μ, so ψ_j(c) is a constant α. For c = u^e this constant equals Π_i u_i(z, y_j)^(e_i), because each u_i is holomorphic and nonzero at z.
- *Multiplicity count.* C(T) = C ⊗ ℚ(T) is a field. Each of its [C:ℚ] embeddings extends to exactly [F : C(T)] = δ/[C:ℚ] of the ψ_j.
- *Single labelling.* One accepted z labels all e at once. Row labels may permute between different z, so all rows must come from the same z.

**Finite control.** Take ℚ(T)[Y]/(Y² − 2T²) with c = 3 + 2Y/T and ℓ = ln(3 + 2√2).
- The tuple (c, c) has rows (ℓ, ℓ) and (−ℓ, −ℓ), whose kernel is ℤ(1, −1) = Rel.
- The tuple (c, c⁻¹) has rows (ℓ, −ℓ) and (−ℓ, ℓ), whose kernel is ℤ(1, 1) = Rel.
- Joint evaluation therefore separates the case where individual characteristic polynomials fail. This is a control only, not a proof.

## 4. Repairs to the parent text

1. **Grid transfer.** The grid argument needs the 2e^(−t) coupling slack, and N must pay log₂Δ (falsifier F2 below).
2. **Branch conditioning.** "Norm nonvanishing" alone does not give per-branch conditioning. One also needs the Cauchy upper bound on the other branches and a separate polynomial det J for separation.
3. **Conjugate grouping.** "Correct conjugate grouping" is **unnecessary** for arch rows. The germ argument gives uniform multiplicity, and 1/δ is the correct weight. Finite rows must later use a normalization compatible with this one; that is part of the unpaid finite half.
4. **Root finding.** Root finding is an imported completeness and runtime assumption. The Rouché test is the visible acceptance certificate.

## 5. Native falsifiers and scope limits

**F1: arch rows alone cannot solve fullRel.** Take f = Y² + 1 over ℚ(T) and u = ((3+4Y)/5, Y, T).
- At every torus point, every arch row is exactly 0: |(3 ± 4i)/5| = |±i| = |z| = 1.
- Alg = ℤ²⊕0, so the arch kernel on Alg is all of Alg, of rank 2.
- But Rel = {(0, 4m, 0)}, of rank 1.
- (3+4i)/5 = (2+i)/(2−i) is detected only at the places over 5, so the **finite rows are unpaid**.
- The order-4 class of Y needs the **root-of-unity phase, which is unpaid**.
- In addition, the nonconstant T has arch row 0, so arch rows cannot replace Alg.

**F2: a grid that ignores degree fails.** Take s = 1, f = Y² − T, u₁ = Y, u₂ = 1/(T^(2^M) − 1).
- Every dyadic grid with N ≤ M bits has D(z) = 0 at **all** points, so every trial aborts.
- The paid N ≥ log₂Δ ≥ M avoids this. The cost is linear in the exponent's bit length, so it is polynomial.

## 6. Unpaid items and remaining obligations

- **Unpaid:**
  - finite or vertical rows, including complete prime support and aligned valuations;
  - the root-of-unity phase step;
  - the downstream all-places lattice algorithm and its height-gap precision.
- **Speculation (unreviewed; does not change the UNPAID status):** given the exact sublattice Λ₀ ⊂ Alg on which c_e is torsion, the phase step might be closed by Farey rounding of arg σ₁(c_e)/2π, using |μ(C)| ≤ 2δ². Λ₀ itself requires the finite rows.
- **Obligations:**
  - re-audit the imported U, V, det J and det A_i bounds and degree bound Δ in this exact use;
  - fix the explicit constant hidden in O(δ³(Λ+1));
  - supply an actual source for polynomial-time root approximation.
- **Not claimed:** no fullRel algorithm, speedup or hardness follows from this lemma.