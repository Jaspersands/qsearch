# Native joint-charge eigenpath tracking: proof review

## Verdict

I found no fatal counterexample. Under the stated promise, the measurement-driven tracker does remove the need for classical label solving. It outputs the target state to trace error ε with polynomial gates and no postselection. Below, "proved" means derived here from the stated hypotheses.

The sketch needs four repairs:

1. **QPE tails.** Binned QPE has heavy tails, with roughly 1/k probability of being off by k bins. The error bound must hold uniformly over all eigenphases, so use a median of repetitions or windowed QPE. Bin-boundary ambiguity then never matters.
2. **Leakage accounting.** Leakage must be bounded at the amplitude level. A union bound over false-accept *probabilities* (R·m·η) is not justified, because leaked amplitude can coherently re-enter the target branch. The correct requirement is R·√(mη) ≲ ε, so η ~ ε²/(mR²). This is the only place an ε² allocation is needed. The Zeno part stays linear in ε.
3. **Simplicity.** Simplicity is needed only at s=0. The joint gap then forces rank P(s) = 1 for all s.
4. **ABORT.** ABORT is a herald, not a certificate. If the promise is false, the tracker can silently output a wrong state.

## Theorem (proved, modulo standard QPE and simulation facts)

**Hypotheses.**
- Q_i(s) are C¹, commute pairwise, and have ‖Q_i‖ ≤ λ_i.
- Every joint eigenvalue vector q_w(s) ≠ q_v(s) satisfies ‖q_w(s) − q_v(s)‖₂ ≥ κ for all s ∈ [0,1].
- |v(0)⟩ is preparable, with P(0) of rank 1 and q_v(0) known to within κ/10.

**Conclusion.** With:
- R = ⌈max(16L²/(κ²ε), 10L/κ)⌉,
- per-coordinate precision δ = κ/(10√m),
- per-coordinate failure probability η_c = ε²/(64mR²),
- per-step implementation error ε_step = ε/(8R),

the output (state ⊗ flag) is within trace distance

> 4L²/(κ²R) + Rmη_c + 2R(√(mη_c) + ε_step) ≤ ε

of |v(1)⟩⟨v(1)| ⊗ |accept⟩. Any initial-state preparation error is additive.

## Proof

### L1. The branch is well defined, with constant rank 1
Fix c with ‖c − q_v(s₀)‖ < κ/2 and set H_c(s) = Σ_i (Q_i(s) − c_i)².

On joint eigenspace w, H_c takes the value ‖q_w − c‖². Near s₀ this is below κ²/4 only for w = v. So P(s) is the Riesz projector of H_c(s) below κ²/4. This projector is C¹ and has locally constant rank. Open/closed continuation then gives a unique C¹ rank-1 branch on [0,1].

### L2. Label drift (Hellmann–Feynman for a joint branch)
Write q_i(s) = tr(P Q_i). Since [P, Q_i] = 0 and tr(P·dP/ds) = 0:

- tr(Q_i·dP/ds) = 2q_i·tr(P·dP/ds) = 0.
- Hence dq_i/ds = ⟨v|Q_i'|v⟩ and |dq_i/ds| ≤ ‖Q_i'‖.
- Hence ‖q(s+h) − q(s)‖₂ ≤ hL ≤ κ/10.

This holds even when individual Q_i are degenerate.

### L3. Zeno loss per step (your bound, confirmed)
Let A = Σ_i (Q_i(s+h) − q_i(s+h))². On the complement, A ≥ κ²(1 − P(s+h)).

For the old eigenvector v = v(s), each term ‖(Q_i(s+h) − q_i(s+h))v‖ ≤ ‖ΔQ_i‖ + |Δq_i| ≤ 2h·sup‖Q_i'‖. Therefore

> f_k = ‖(1 − P(s+h))v‖² ≤ ⟨v|A|v⟩/κ² ≤ 4h²L²/κ².

Summing over steps gives Σf_k ≤ 4L²/(κ²R).

### L4. The instrument is diagonal in the joint eigenbasis
Ideal QPE uses controlled powers of e^{iQ_i(s_k)t₀}, with t₀ = π/(2λ_i) so there is no aliasing.

- It maps |ψ_w⟩|0⟩ to |ψ_w⟩|φ_i(q_w)⟩.
- Repetitions, the median, and all m coordinates compose the same way.
- So each raw outcome b has Kraus operator M_b = Σ_w c_b(q_w) P_w(s_k).
- On a simple target, M_b acts as a scalar. Measurement does not disturb it (your claim is correct).

**Implementation error.** Approximate simulation (qubitization or LCU with oblivious amplitude amplification, no postselection) gives a dilation within ε_step of ideal in operator norm. Compressing to outcomes is a contraction, so the outcome maps are also within ε_step.

### L5. Good-path telescoping, with no dimension dependence
Define the good outcome set G_k = {b : the estimate is within κ/10 of q_v(s_k) in ℓ₂}.

**Good outcomes keep the tracker on track.** On good histories, ‖est − q̃‖ ≤ 0.3κ < κ/3. So the step accepts, and the new q̃ is again within κ/10. Errors do not accumulate.

**Bound on wrong branches.** For w ≠ v, b ∈ G_k requires an estimation error of at least 0.9κ. That forces some coordinate error above δ, so Σ_{b∈G}|c_b(q_w)|² ≤ mη_c. For the target, Σ_{b∈G}|c_b(q_v)|² ≥ 1 − mη_c.

**Maps compared.** Define V_k: φ ↦ ⊕_{b∈G_k} M_b φ and W_k: φ ↦ ⊕_b c_b(q_v) P_k φ. By orthogonality of the P_w:

> ‖(V_k − W_k)φ‖² = Σ_w (Σ_{b∈G}|c_b(q_w)|²)‖P_w φ‖² ≤ mη_c‖φ‖².

This uses no union bound over the 2^N branches. Both maps are contractions, so telescoping gives ‖V_R⋯V_1 v₀ − W_R⋯W_1 v₀‖ ≤ R(√(mη_c) + ε_step) =: δ_a. History dependence is harmless because the maps are block-diagonal controlled operations.

### Assembly
- Tracing out the classical register: Tr(W⋯v₀) = p_W |v_R⟩⟨v_R|, with p_W ≥ (1 − mη_c)^R(1 − Σf) ≥ 1 − Rmη_c − Σf.
- The good part of the real output, ρ_good, satisfies ‖ρ_good − p_W|v_R⟩⟨v_R|‖₁ ≤ 2δ_a.
- Everything else (aborts, and accepted non-good paths such as a wrong-label accept on the target) has weight ≤ 1 − p_W + 2δ_a.

Hence TD ≤ (1 − p_W) + 2δ_a, which is the stated bound.

The acceptance radius plays no role in this bound. Every non-good path is charged in full. Re-entry of leaked amplitude is handled automatically.

## Resources
**Per step and per coordinate:**
- K = O(log(mR/ε)) QPE runs.
- Each run uses total evolution time O(1/δ) = O(√m/κ) and O(log(λ_i√m/κ)) phase bits.

**Gate count:**

> Õ( R · K · Σ_i (λ_i√m/κ + log(1/ε_step)) · C_BE,i ),

where C_BE,i is the block-encoding cost, about O(J_i·N) gates for J_i Pauli terms.

**Classical cost:**
- Coefficients of Q_i(s_k) are rational. Truncating them to O(log(R·T·ΣJ/ε)) bits is charged inside ε_step.
- Labels need O(log(λ√m/κ)) bits.

Nothing scales with 2^N except through κ, λ_i, and L, all promised polynomial.

## Application check (Q_i(g) = n_i + (g/2)Σ_{j≠i}(P_ij − I)/(ε_i − ε_j))

**Normalization.** Since σ·σ = 2P − 1, this is the source's Q^(k): σ^z/2 + 1/2 + (g/4)Σ(σ·σ − 1)/(ε_k − ε_j).

**Commutation.** This is a source claim, but it is cheaply checkable.
- The cross terms cancel because [S_k^z + S_l^z, S_k·S_l] = 0.
- This holds for either field sign and any g, provided the field coefficient is uniform across i.
- [G_k, G_l] = 0 is the standard Gaudin identity.

**Initial state.** At g = 0, Q_i = n_i. A computational basis bitstring is a simple joint eigenvector with a binary q-vector, and the gap there is at least 1.

**Norms.**
- ‖Q_i'‖ ≤ G·Σ_j 1/|ε_i − ε_j|, since ‖P − I‖ = 2. Your bound on L follows.
- Dropping the known identity shifts, λ_i ≤ 1 + (3G/4)Σ_j 1/|Δ_ij|.
- J_i = O(N) and m = N.

**Not shown.** The path-uniform target gap κ ≥ 1/poly is unproved. The source has only perturbative limits and finite-N numerics suggesting min‖Δq‖₂² ~ 1/N. Those numerics themselves rely on the classical solver. The source's exponentially small Smale bounds (Fig. S9) are lower-bound tools on root separation, not costs of this procedure. This tracker depends on κ, not on σ_min(Df). Make no classical-hardness inference from that.

## Labels learned from the output
On good paths, the transcript gives q_v(s_k) to within κ/10 at every mesh point. The final labels can be refined nondestructively to precision ξ in time O(√m/ξ) per coordinate.

So, under the promise, this procedure is a quantum path-follower for approximate quadratic-Bethe roots. No advice oracle is used: only q_v(0) to κ/10 is required.

## Which assumptions are truly necessary
**Used and essential:**
- Exact commutation, for diagonal Kraus operators.
- The target-versus-all-others gap along the whole path. A brief crossing between mes