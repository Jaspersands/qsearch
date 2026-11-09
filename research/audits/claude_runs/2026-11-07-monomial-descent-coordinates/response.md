# Compact S-unit coordinate obligation: closed, conditional on a complete source basis

## 1. Verdict and decisive falsifier check

**Verdict: closed.** Given a complete, verified compact S-unit basis, exact coordinates (torsion included) of every g(ε_j) and a_gi can be computed. The integer system can then be solved and a compact x output. All of this runs in deterministic or Las Vegas classical polynomial bit time. Quantum resources enter only through the source S-unit routine and Shor factoring.

Two consequences follow:

- **No quantum advantage from this step.** The coordinate step is classical polynomial time given the basis. Classical S-unit baselines with the same support reduction therefore inherit it unchanged. It adds no quantum separation.
- **What NO depends on.** A NO answer still rests on the conditional support lemma (GRH plus class generation for every E^C) and on completeness of the S-unit group.

**Decisive falsifiers examined first.** The coordinate route would fail if any of the following held:

- **(F1) Non-separation.** The S-unit log lattice has λ₁ below 2^(−poly), so polynomial precision cannot separate lattice points.
- **(F2) Ill-conditioning.** The supplied basis has covolume below 2^(−poly), so rounding coordinates needs exponential precision.
- **(F3) Torsion invisibility.** A root of unity ζ^s ≠ 1 cannot be distinguished from 1 without expanding huge products.
- **(F4) Orientation error.** The displayed equations are mis-oriented.

F1–F4 are each refuted below by an elementary proof (Lemmas 1–4). I relied on no source for them.

**F5 remains genuinely open: a coherent source failure.** Suppose every source run returns the same proper g-stable finite-index subgroup. That is undetectable here and would make a NO answer wrong. It is budgeted, not refuted (§5).

## 2. Proved lemmas

**Notation.** Write Φ(γ) = ((log|σγ|)_{σ ∈ places at ∞}, (v_P(γ))_{P ∈ S_E}). Valuations are raw integers. Use the ℓ∞ norm throughout. Then:

- n = r₁ + r₂ − 1 + |S_E|, with |S_E| ≤ N|S|.
- Φ restricted to E_S has kernel μ_E of order w.
- Φ(E_S) has rank n in the product-formula hyperplane.
- Drop one archimedean coordinate to get Φ′ ∈ ℝⁿ. Φ′ is injective on Φ(E_S), because the dropped coordinate is a linear function of the others.

**Lemma 1 (separation).** Let K = N(2·3^N + 1)^N, so log₂K = O(N²). Every non-torsion unit u of E satisfies max_σ log|σu| > ln2/K.

*Proof.*
1. Let α ∈ O_E have all conjugates |σα| ≤ 2. Its characteristic polynomial over ℚ has degree N and integer coefficients bounded by C(N,k)·2^k ≤ 3^N. Each such polynomial has at most N roots. So at most K such α exist.
2. Suppose all |σu| ≤ 2^(1/K). Then u⁰, …, u^K are K+1 algebraic integers with all conjugates ≤ 2.
3. By pigeonhole, u^a = u^b for some a < b. Hence u is a root of unity. ∎

**Corollary.** λ₁(Φ′(E_S)) ≥ η := ln2/(2NK) = 2^(−O(N²)).

*Proof.* Take a nonzero vector.
- If some valuation coordinate is nonzero, its norm is ≥ 1.
- Otherwise the vector comes from a unit. The relation Σ n_σ log|σu| = 0 with n_σ ∈ {1, 2} bounds the dropped coordinate by 2N times the maximum of the others. Apply Lemma 1. ∎

The bound holds for every subgroup of E_S, since λ₁ of a sublattice is at least λ₁ of the lattice.

**Lemma 2 (conditioning).** Let M be the n×n matrix of Φ′ values of any basis of any full-rank subgroup of E_S/μ_E. Then |det M| ≥ η^n.

*Proof.* Minkowski's second theorem for the ℓ∞ unit cube (volume 2^n) gives λ₁⋯λ_n · 2^n ≤ 2^n det. Hence det ≥ ∏λ_i ≥ λ₁^n. ∎

Let 2^B bound the entries of M. This holds with B polynomial: compact atoms have poly-bit size and exponents are binary.

- By Hadamard and the adjugate, ‖M⁻¹‖_∞ ≤ n(√n·2^B)^(n−1)/η^n =: 2^C, with C = O(n(B + log n + N²)).
- For integer c with Mc = t (‖t‖ ≤ 2^B): ‖c‖_∞ ≤ n·2^(C+B).

**Perturbation.** Suppose entries of M and t are known to absolute error δ = 2^(−(2C + B + 2log n + 4)), and we solve M̃c̃ = t̃ exactly over dyadic rationals. Then ‖c̃ − c‖_∞ < 1/4, so rounding returns c exactly.

*Proof.* We have ‖M⁻¹‖·‖E‖ ≤ 2^C·nδ ≤ 1/2. The standard bound gives ‖c̃ − c‖ ≤ 2·2^C(nδ‖c‖ + δ) ≤ 2^(2C+B+2log n+2)·δ ≤ 1/4. ∎

**Lemma 3 (torsion by one good reduction).** Suppose p ∤ w and P | p. Then reduction mod P is injective on μ_w.

*Proof.* Suppose ζ^s ≡ 1 mod P with 0 < s < w. Then 1 − ζ^s ∈ P. But ∏_{s=1}^{w−1}(1 − ζ^s) = w, so p | w, a contradiction. ∎

**Lemma 4 (orientation).** Convention: column j of B_g holds the free coordinates of g(ε_j). Take x_i = ζ^(t_i)·∏_j ε_j^(Z[i,j]).

- The free exponent of ε_m in g(x_j) is Σ_l Z[j,l]·B_g[m,l] = (Z B_gᵀ)[j,m].
- So (g★x) has free part A_g Z B_gᵀ.
- Its torsion part is A_g(k_g t + Z T_g).

Hence a_g = x/(g★x) is equivalent to the displayed system:

- Z − A_g Z B_gᵀ = U_g
- t − A_g(k_g t + Z T_g) ≡ v_g (mod w)

The displayed equations are therefore correctly oriented. Since E_S ≅ μ_w × ℤ^n via complete coordinates, a solution in E_S exists iff this integer system is solvable. ∎

## 3. End-to-end algorithm

**Inputs (all charged):**
- the table for O_E;
- all automorphisms, as matrices on the basis;
- A_g;
- expanded a_gi;
- S built as in the candidate: rational primes ≤ B₀, divisors of D_E, and the denominator/norm supports of a_gi, factored by Shor with deterministic primality certification.

**Step 1. Embeddings (classical).**
- Pick a primitive element θ as a small random combination of basis vectors. Accept it once its characteristic polynomial is squarefree.
- Compute its roots to precision 2^(−L′) with a polynomial-time root finder. Root separation follows from the discriminant, which has poly bits.
- Express the basis in θ.
- For an atom α = β/d: |N(β)| ≥ 1 and the other conjugates are ≤ 2^poly, so |σα| ≥ 2^(−poly). Hence log|σα| to relative precision δ costs poly bits.

**Step 2. Prime data.**
- For each p ∈ S, decompose pO_E by splitting the finite algebra O_E/pO_E (randomized polynomial time).
- Obtain valuation routines for each P ∈ S_E.
- Valuations of poly-bit atoms are exact integers.

**Step 3. Torsion generator (classical).**
- For each m ≤ 2N² with φ(m) | N, decide whether Φ_m has a root in E by polynomial factorization over number fields. *[Source memory, unverified here: Lenstra/Landau polynomial-time factorization over number fields.]*
- This gives w and ζ.
- Compute k_g by comparing g(ζ) with ζ^k for k < w. This is exact, since w = poly.

**Step 4. Source with amplified completeness (F5 control).**
- Run the quantum S-unit routine k times.
- For each returned element, verify it is an S-unit: factor the norms and denominators of all its atoms (Shor, certified). Check that every prime of support lies in S_E, or that the exact valuations sum to zero.
- Discard any run containing a non-S-unit. Valid runs generate subgroups of E_S.
- Form the sum lattice. By Lemmas 1–2 applied to the sum, which is a subgroup of E_S, coordinates of every generator relative to run 1's basis are rationals with denominator ≤ det(L₁)/η^n = 2^poly. Recover them exactly by continued fractions at doubled precision.
- HNF over ℤ of the integer relation module gives a basis of the sum. Each basis vector is an integer combination of generators with poly-bit exponents, so it is a compact product.
- If any run was complete, the sum equals E_S/μ_E. So Pr[incomplete] ≤ 3^(−k) when each run succeeds with probability ≥ 2/3.
- Runs need not agree. A missing-element failure is repaired, and a spurious element is rejected by the S-unit check.

**Step 5. Exact coordinates.**
1. Build M from the Φ′(ε_j), precomputing a dyadic inverse.
2. For each target γ ∈ {g(ε_j), a_gi}, compute Φ′(γ) to precision δ:
   - g(ε_j) is the compact product of g applied to the atoms, which is polynomial via the automorphism matrices;
   - v_P(g(γ)) = v_{g⁻¹P}(γ).
3. Round to the integer vector c (Lemma 2).
4. Form the residual ρ = γ·∏ε_j^(−c_j) as a compact product.
5. Choose a rational prime p among the first poly-many primes that divides none of the atom denominators, atom numerator norms, or w. Each bad prime divides an integer of known poly bit length, so a good p exists among polynomially many candidates. No factoring is needed: test divisibility directly.
6. Take any P | p. Evaluate ρ mod P by square-and-multiply in O_E/P using binary exponents. Match it to ζ^s mod P. By Lemma 3, s is exact.
7. This yields T_g, B_g, v_g, U_g exactly. Entries are ≤ n·2^(C+B), so they have poly bits.

**Step 6. Solve.**
- Stack the system for all N elements g as one integer system. Unknowns: vec Z (rρ), t (r), and slack w·y.
- Equations: ≤ N·r(ρ+1). Entries have poly bits.
- An HNF/Smith computation decides feasibility and gives a poly-bit particular solution.
- If infeasible, answer NO.
- Otherwise output x_i = ζ^(t_i)·∏_j ε_j^(Z[i,j]). This is a compact product with ≤ rρ·(atoms per ε) atoms and exponents e_k·Z[i,j] of poly bits.

**Step 7. Sound positive check (independent of GRH, the support lemma, and completeness).** For every g and i, form ρ_gi = a_gi·(g★x)_i / x_i as a compact product of verified S-units. Then:
- (a) Check exact S_E valuations are 0.
- (b) Check that Φ′ computed to precision < η/4 is below η/2 in ℓ∞. By the Corollary this proves ρ is torsion.
- (c) Check that the reduction mod a good P equals 1. By Lemma 3 this proves ρ = 1.

Each test is a proof, not a heuristic, given correct arithmetic. If any check fails, the run is a detected source or arithmetic fault: repeat.

## 4. Resources and quantifiers

**Quantifiers.** All bounds hold for every N ≥ 1, every r, every |S|, and every compact input size. The only constants are explicit:
- K, η, n, B, C, δ as above;
- B₀ = 48·bitlen(|D_E|)² from the candidate, a premise. *[Source memory, unverified here: the Biasse–Song constant.]*

**Precision.** log(1/δ) = O(n(B + log n + N²)). This is polynomial in:
- N;
- |S_E| ≤ N(B₀ + bits of D_E + bits of the a_gi);
- r;
- atom count and atom bits;
- exponent bits.

**Costs.**

| Item | Cost |
|---|---|
| Classical arithmetic | n×n dyadic inversion at precision δ, plus (Nρ + Nr) matrix-vector products. |
| Per-atom log evaluations | (number of atoms) × N × poly(δ). |
| Torsion reductions | ≤ (Nρ + Nr) square-and-multiply chains in a residue field of degree ≤ N. |
| HNF | Of an O(Nrρ) × O(rρ) poly-bit matrix. |
| Quantum: S-unit source | k runs. |
| Quantum: Shor factoring | Norm/denominator factoring for S (candidate) and for S-unit verification of source atoms. Each integer has poly bits. |
| Quantum: other | None beyond these. |

**Error budget.**
- Shor and the F_p-algebra splitting are Las Vegas with certification. Failure costs time, not correctness. Truncate after a fixed number of repetitions and output FAIL with probability ≤ ε₁.
- Numerical steps are deterministic with proven precision.
- YES answers are certified unconditionally (Step 7).
- NO answers are wrong only if (i) all k source runs are incomplete (≤ 3^(−k)), or (ii) the support lemma or class-generation premise fails. Case (ii) is not a probability but an unproved conditional.

So, conditional on the premise: Pr[error] ≤ 3^(−k) + ε₁. Take k = O(log(1/ε)).

## 5. What is proved, assumed, or open

**Proved here (elementary, self-contained):**
- Lemmas 1–4;
- the perturbation bound;
- the sum-of-runs completeness repair;
- soundness of the compact equality test.

These settle obligations F1–F4 and refute the "exponentially ill-paid coordinates" and "missing torsion" falsifiers listed in the candidate.

**Assumed premises (not verified by me):**
- the support lemma under every-cyclic-E^C class generation;
- GRH and the 48·log² generator constant;
- existence of a polynomial-time quantum S-unit routine returning a complete compact basis with probability ≥ 2/3;
- polynomial-time factorization over number fields, used only for μ_E. If needed, μ_E can be cross-checked from the source's torsion output, since ζ^w = 1 is exactly testable via Lemma 3 plus valuation and log checks.

**Not claimed:**
- novelty of the coordinate method;
- any quantum advantage from this step.

Lemma 1 is a Kronecker-type pigeonhole argument and Lemma 2 is Minkowski; both are standard. The method is the classical log-embedding approach used in S-unit and Galois-cohomology software. I cannot confirm from memory exactly how Magma's SUnitCohomologyProcess or Biasse–Fieker-style compact-representation work handle this, so overlap is plausible but unverified.

**Remaining proof obligations:**

1. **Support lemma (the decisive one).** It is the only route by which NO is meaningful. Its falsifier is an explicit cocycle with a solution in (E*)^r but no solution in (E_S)^r for the paid S. A finite failure to find one proves nothing either way.
2. **Source contract.** State precisely the success probability and output format of the quantum S-unit routine, including that its elements are compact with poly atoms and binary exponents. Step 4 needs only "complete with probability ≥ 2/3, each output element a genuine S-unit or rejectable".
3. **Bit-size accounting written out.** Replace "poly" in B by an explicit expression in input sizes and source output sizes. This is routine but should be stated.
4. **Baseline honesty.** For trivial and permutation actions (Hilbert 90) and quadratic norm tori (conics), the classical baselines already solve the problem. Any end-to-end speedup claim must come from the S-unit and factoring stages, measured against classical subexponential S-unit computation. This step neither strengthens nor weakens that comparison.

**Falsifiers for this report's claims.** Any one would refute it:
- a non-torsion unit with all conjugates ≤ 2^(1/K);
- a full-rank sub-lattice of Φ′(E_S) with covolume < λ₁^n;
- a root of unity ζ^s ≠ 1 with ζ^s ≡ 1 mod P where p ∤ w.

Each contradicts a short proof above. An implementation mismatch would instead indicate an arithmetic or precision bug, not a counterexample.