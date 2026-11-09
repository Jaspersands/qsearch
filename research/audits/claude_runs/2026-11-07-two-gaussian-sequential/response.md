# Audit of the paid sequential endpoint and the bond≤8 model

## Verdict

**The endpoint is correct after one small repair.** The repair is a gap-free selection lemma that the note uses but never states (§2, L4).

- **Conditional proximity.** When actual success is at least 1/2, the conditional state stays within 4·d0 of the conditioned reference.
- **No exponential accumulation.** The induction keeps success at least 1/2. Error grows linearly in the number of steps, because each step is compared against the reference pushed through the *actually applied* gates. Nothing is compared recursively.
- **Requirement on d0.** The endpoint needs d0 ≤ ε²/(32n). Whether the upstream pipeline actually delivers d0 = O(t) has not been audited.
- **Bond≤8 model.** It holds, but only under an ordering condition the note leaves implicit: every recovered pair, and every block of at most 4 modes, must be contiguous in the learned order.

## 1. Bond≤8 model (analysis object only)

**Assumption (upstream, not audited).** The reference is the normalized state φ = (a|B1⟩ + b|B2⟩)/‖·‖. Each branch B_i is, in the learned order, a product of fermion-parity-even factors on contiguous blocks. The possible blocks are:
- recovered pairs;
- blocks of at most 4 modes;
- cat-projected groups;
- fixed-occupation sentinel modes.

**Jordan–Wigner.** Even factors on contiguous blocks map to an exact qubit tensor product. The Schmidt rank of a sum of two states is at most the sum of their ranks. So the rank at each cut is bounded as follows:

| Location of the cut | Rank per branch | Total rank |
|---|---|---|
| Between blocks | 1 | ≤ 2 |
| Inside a pair | ≤ 2 | ≤ 4 |
| Inside a projected cat group (each branch's factor lies in span{\|0^{2k}⟩, \|1^{2k}⟩}) | ≤ 2 | ≤ 4 |
| Inside a low-ν group (J-compatible bases send vacuum/full to vacuum/full up to phase) | 1 | ≤ 2 |
| Inside a 4-mode block, 2\|2 cut | ≤ 4 | ≤ 8 |

The maximum is 8, attained only at the 2|2 cut of a 4-mode block. Normalizing the reference does not change any rank.

**Falsifier for the model.** Suppose the pair modes are interleaved, for example pairs (1,5), (2,6), (3,7), (4,8). Then the middle cut has rank up to 16 per branch, and the model fails.

**Proof obligation.** Order each pair's two modes adjacently and each block contiguously.

**Cat projections.** These are applied only to the model. The endpoint never performs them.

## 2. Endpoint: fully quantitative proof

**Setup.**
- ψ is an n-qubit state. Here ψ means the input after the learned Gaussian rotation, using the same compiled circuit G in both learning and output.
- φ has Schmidt rank at most 8 across every cut (1..j | j+1..n).
- D(ψ,φ) ≤ d0 < 1/2.
- Choose the phase of φ so that ⟨φ|ψ⟩ ≥ 0. Then ‖ψ−φ‖² = 2 − 2|⟨φ|ψ⟩| ≤ 2d0², so ‖ψ−φ‖ ≤ √2·d0.
- There are L = n−3 compression steps.
- After step j, W_j is the product of the applied gates. Each gate is a 4-qubit gate acting on (memory, next qubit) only.
- Π_j projects all qubits discarded so far onto |0⟩.
- Define u_j = Π_j W_j ψ and v_j = Π_j W_j φ, with success probability p_j = ‖u_j‖².

**L1 (invariant, no recursion).** For every j and every realization of adaptively chosen gates:

‖u_j − v_j‖ ≤ ‖ψ − φ‖ ≤ √2·d0.

This holds because Π_j W_j is a contraction. The reference is re-pushed through the *actual* gates at every step, so tomography errors never enter this bound.

**L2 (normalization).** For any vectors u, v:

‖u/‖u‖ − v/‖v‖‖ ≤ 2‖u−v‖/‖u‖.

If p_j ≥ 1/2, then:
- ‖v_j‖ ≥ 1/√2 − √2·d0 > 0, so the conditioned reference is well defined.
- D(û_j, v̂_j) ≤ ‖û_j − v̂_j‖ ≤ 4·d0, using D ≤ Euclidean distance for pure states.

**L3 (rank preservation).** Π_j W_j acts only on qubits 1..j+3. So v_j has Schmidt rank at most 8 across the cut after qubit j+4. The conditioned state is |0…0⟩_disc ⊗ χ, so the reduced state σ_{j+1} on (memory, qubit j+4) has rank at most 8.

**L4 (gap-free top-8 selection; missing from the note).** Let ρ be the true reduced state and ρ̂ a Hermitian, trace-1 estimate with ‖ρ̂−ρ‖₁ ≤ Δ. Let P̂ be the projector onto the top-8 eigenspace of ρ̂. Then the conditional failure is

f = tr((I−P̂)ρ) ≤ τ₈(ρ) + Δ.

Proof: Ky Fan's principle gives tr(P̂ρ̂) ≥ tr(Pρ̂) for any rank-8 projector P. The difference X = ρ−ρ̂ is traceless and Hermitian, so |tr(QX)| ≤ ‖X‖₁/2 for any projector Q. Apply this twice.

Next, τ₈(ρ) ≤ tr((I−P_σ)(ρ−σ)) ≤ D(ρ,σ) ≤ 4·d0, where P_σ is a rank-8 projector containing supp σ.

Two consequences:
- No Schmidt gap or eigenvector stability is needed.
- An unknown true rank below 8 is harmless; the selected space is simply padded.

**L5 (induction).** Suppose L(4d0+Δ) ≤ 1/2 and every tomography succeeds. Then for every j:

p_j = ∏_{i≤j}(1 − f_i) ≥ 1 − Σ_{i≤j} f_i ≥ 1 − j(4d0+Δ) ≥ 1/2.

Each f_i ≤ 4d0+Δ holds because the hypothesis p_{i−1} ≥ 1/2 holds by induction. The base case is p_0 = 1: the first memory is the raw qubits 1–3. The bound is linear in L. Every f_i is bounded by the same global quantity, not by the previous step's error, so nothing accumulates exponentially.

**L6 (output).** Later gates never touch discarded qubits, so sequential conditioning equals a single final projection. The end state is |0…0⟩ ⊗ |m⟩ with |m⟩ pure on 3 qubits. This is the end-memory case: the final cut has rank 1.

Let F = 1 − p_L. Gentle measurement holds exactly here:

D(ψ, W⁻¹û_L) = √F ≤ √(L(4d0+Δ)).

Estimate m̂ as the top eigenvector of a 3-qubit estimate with ‖·‖₁ ≤ γ². By L4 with τ = 0, D(m̂, m) ≤ γ.

**Compilation.** Use the same compiled gates in learning and output, and the exact reversed adjoint circuit for the inverse. Gate compilation then adds no accumulating error. Only the preparation of m̂ and the compiled G count, and G's compilation error is already inside d0.

**Theorem.** Assume d0 ≤ ε²/(32n). Run the endpoint with:
- per-step tomography accuracy Δ = ε²/(8n);
- final accuracy γ = ε/4;
- per-event failure η/(4n).

Then, with probability at least 1−η, the output U_out = G⁻¹W⁻¹(|0⟩⊗|m̂⟩) satisfies:

D ≤ √(ε²/4) + ε/4 = 3ε/4.

Moreover F ≤ ε²/4 < 1/2, so every conditional success is at least 1/2.

## 3. Charged costs

**Per-step tomography (Pauli Hoeffding).**
- Each of the 255 Paulis is estimated to accuracy Δ/16; then ‖·‖₁ ≤ Δ.
- Shots: N ≤ 255·2·(128n)²·ε⁻⁴·ln(2040n/η) ≈ 8.4×10⁶·n²·ε⁻⁴·ln(2040n/η).

**Conditional sampling.**
- Each attempt succeeds with probability at least 1/2.
- Making 4N attempts gives N successes except with probability e^{−N/4} ≤ η/(4n).
- Total learning copies: ≤ 4nN = O(n³·ε⁻⁴·log(n/η)).

**Final 3-qubit tomography.**
- O(ε⁻⁴·log(1/η)) shots, doubled for conditioning.

**Gates and classical work.**
- At most n four-qubit gates per copy.
- Classical work: O(n) eigendecompositions of 16×16 matrices, using O(log(n/ε)) bits.

**Failure budget.** A union bound over the at most 2n+2 events gives total failure ≤ η.

## 4. GHZ-phase check

Take ψ_± = (|0ⁿ⟩ ± |1ⁿ⟩)/√2, with d0 = 0 and bond dimension 2.
- Every 4-qubit reduced state is ½(|0000⟩⟨0000| + |1111⟩⟨1111|), the same for both signs.
- The top-8 space contains that span, so f_j ≤ Δ.
- The memory carries (|a⟩ ± |b⟩)/√2 coherently.
- The final pure-state tomography reads off the sign, and any relative phase e^{iθ}.

So the endpoint does not rely on proper marginals. The two-branch relative phase α/β survives in the same way.

## 5. Necessity of the success hypothesis

Let ψ = √(1−d0²)·φ + d0·φ⊥, where Πφ = 0 and Πφ⊥ = φ⊥. Then:
- the success probability is p = d0²;
- the conditional input state is φ⊥, at distance 1 from any reference;
- the conditioned reference is the zero vector.

Without the induction's p ≥ 1/2, L2 is false. Separately, the linear bound becomes vacuous once d0 ≳ 1/(8n). That is a limit of this proof, not a demonstrated algorithmic barrier.

## 6. Status

| Item | Status |
|---|---|
| L1–L6 | Proved |
| Bond≤8 model | Proved, conditional on contiguous ordering |
| Upstream d0 = O(t) (Candidate 2 chain, the B⁴b/(hτ) bookkeeping, alignment, polar rounding) | Unaudited assumption. Needed with explicit constant: d0 ≤ ε²/(32n) |
| Remaining falsifiers | A learned-order cut of rank > 8; upstream d0 > ε²/(32n) |

**Repairs to the note's wording.**
- "Fail with probability O(d0+t)" should read: f_j ≤ 4·d0 + ‖ρ̂−ρ‖₁, proved via L4.
- "Trace error t" means ‖·‖₁ ≤ 2t.
- The √F identity in L6 is exact.