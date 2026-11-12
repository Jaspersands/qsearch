# wave-lattice-shell: coherent preparation of the m=1 lattice Lorentzian Fourier state

## 0. Result

**Theorem (proved below, modulo the standard finite-precision arithmetic obligation PO-A in §6).** Let L = 2^n with n ≥ 4, θ = 2πk/L, and

- D(k) = 1 − λ(k) = 2cos θx + 2cos θy − 3,
- a(k) = D(k) + iη, with η = 1/L,
- Z = Σ_k |a(k)|^−2.

There is a reversible circuit V and a flag projector Π_good such that the following hold.

1. **Exact good branch.** Π_good V|0⟩ = M^−1 Σ_k a(k)^−1 |k⟩|0_anc⟩, with M² = 320 L³ a fixed public number. This holds in exact arithmetic, with no shell list, no lattice-point count, and no knowledge of Z.
2. **Success bound.** The heralded success probability is P = Z/M² ≥ 1/77760, for every n.
3. **Normalizer bounds.** L³/243 ≤ Z ≤ 320 L³. Equivalently, Z0 = ||A^−1 δ0||² = Z/L² lies in [L/243, 320 L].
4. **Precision and cost.** With p = n + log2(1/ε) + O(1) bits, the normalized output is within ε in 2-norm of |ψ⟩ = Z^−1/2 Σ_k a(k)^−1 |k⟩.
   - Gates per attempt: poly(p).
   - Repeat-until-success: expected ≤ 77760 attempts.
   - Alternatively, fixed-point amplitude amplification uses O(√77760 · log(1/ε)) calls.
   - Total cost is poly(n, log(1/ε)), better than the requested poly(1/ε).
5. **Spatial sample.** A source at x0 costs one phase e^{−iθ·x0}. Then one inverse QFT gives one spatial sample with TV ≤ ε + (QFT synthesis error) from |G(x − x0)|²/Z0.

**Two points to keep separate from the theorem.**
- The continuum ring/arctan formula of the primary (Eq. 26, A20) is not used anywhere. All constants here are discrete and finite-n.
- The theorem says nothing about advantage. §5 shows the Fourier-basis law is classically samplable by the same envelope. The classical status of the spatial m=1 law is open.

## 1. Construction

**Charts.** Use centered representatives in (−L/2, L/2].
- Chart A: |ky| ≥ |kx| (ties go to A). Chart B: otherwise.
- Sign σ: in chart A, σ = sign(ky) with ky ∈ [0, L/2] counted as +. Chart B is the same with x and y swapped.
- Precision: D̃(k) is a fixed p-bit reversible evaluation with |D̃ − D| ≤ δ ≤ η/12. This needs cos to absolute error ≤ 1/(48L), i.e. n + 6 bits for the labels.

**Shells.**
- t_j = 2^j η for j = 0..J, with J = n − 2, so t_J = 1/4.
- Label b(k) = (chart, σ, j) if |D̃| ≤ η (j = 0) or t_{j−1} < |D̃| ≤ t_j (j ≥ 1).
- b(k) = F ("far") if |D̃| > 1/4.
- b is a deterministic function of k, so the labels partition the torus exactly. Ties, ky = 0, and θ = π all receive exactly one label.

**Windows (chart A, σ = +; other branches by symmetry).** For column kx, set c0 = 3/2 − cos θx and s = t_j + 3δ. Clip:
- c_hi = min(c0 + s/2, 13/16 + δ),
- c_lo = max(c0 − s/2, 3/8 − δ).

Compute θ̃_lo ≈ arccos(c_hi) to absolute error ≤ 2π/L, and set the start S_b(kx) = ⌊L θ̃_lo/2π⌋ − 1.

The window length is W_j = 2^{r_j}, where r_j = ⌈log2(0.35·2^j + 4)⌉. This gives:
- W_0 = W_1 = W_2 = W_3 = 8, W_4 = W_5 = 16, …;
- W_j ≤ 8·2^j, and W_j ≤ L for n ≥ 4.

**Branch weights.**
- Shells: q_{(·,·,j)} = 2^−j for each of the 4 (chart, σ) pairs.
- Far: q_F = 1/L.
- Normalization: Q = Σ q = 8 − 15/L < 8, and p_b = q_b/Q.
- The branch state Σ_b √p_b |b⟩ has O(n) labels with closed-form amplitudes. Prepare it with O(n) precomputed rotations.

**Circuit V.**
1. Prepare Σ_b √p_b |b⟩. Prepare kx uniform over Z/L with n Hadamards.
   - If b ≠ F: prepare o uniform on [0, W_b) (Hadamards on r_b qubits controlled by b), and set ky = σ(S_b(kx) + o) mod L, with x and y swapped for chart B.
   - If b = F: prepare ky uniform over Z/L.
   - Envelope amplitude on (b, k): e_b = √(p_b/(L·W_b)), with W_F := L.
2. Compute b(k), set the flag g = [b(k) = b], then uncompute b(k).
3. Conditioned on g, rotate an ancilla to amplitude r(k) = C_b/(M a(k)), where C_b = √(L W_b Q/q_b) and a is computed from D̃. Apply the magnitude by R_y and the phase −arg(D̃ + iη) by a phase gate.
4. On g = 1 we have b = b(k) and o = σ ky − S_b(kx) mod L. Erase o, then erase b by XORing with b(k).

The final good branch is g = 1, ancilla in its good state, and all other registers 0.

**No multiplicity.** Each k has exactly one surviving path (b(k), kx, o). Its amplitude is e_b · C_b/(M a) = (1/M)·(1/a(k)), because e_b·C_b = 1. This is claim 1, provided every k lies in its own label's window (L2) and |r| ≤ 1 (L3). Rejected paths only lower P; they never bias amplitudes.

## 2. Lemmas

**L1 (regular charts).** Suppose b(k) = (A, σ, j). Then |D| ≤ 1/4 + δ and |θy| ≥ |θx|, so cos θy ≤ cos θx. It follows that
- 2cos θy ≤ (13/4 + δ)/2, i.e. cos θy ≤ 13/16 + δ/4;
- cos θy ≥ 11/8 − δ/2 − 1 = 3/8 − δ/2.

On cos θy ∈ [3/8 − δ, 13/16 + δ] we have |sin θy| ≥ 0.57. This is the regular level-curve parameterization: in chart A the curve is a graph over kx with bounded slope. The tangency at (±π/3, 0) lies in chart B.

**L2 (window containment and width).** For b(k) = (A, +, j), cos θy lies in the clipped interval [c_lo, c_hi], because |D| ≤ t_j + δ, the cos θx error is ≤ δ/2, and L1 applies.
- Cos is monotone on [0, π], so θy ∈ [arccos c_hi, arccos c_lo] =: [θ_lo, θ_hi].
- By the mean value theorem, θ_hi − θ_lo ≤ (1.25 t_j)/0.57 ≤ 2.2 t_j.
- Arccos is 1.75-Lipschitz on the clipped range, so it is well conditioned there.

From |θ̃_lo − θ_lo| ≤ 2π/L:
- S ≤ Lθ_lo/2π ≤ ⌈Lθ_lo/2π⌉;
- S + W_j − 1 ≥ Lθ_lo/2π − 4 + W_j ≥ Lθ_hi/2π, because W_j ≥ 0.35·2^j + 4 ≥ (θ_hi − θ_lo)L/2π + 4.

So every lattice θy in the interval lies in the window. W_j ≤ L makes o unique mod L. ∎

**L3 (ratio bound, M² = 320 L³).**
- j ≥ 1: |D| ≥ t_{j−1} − η/12 ≥ (11/24) t_j, so |a|^−2 ≤ 4.77 L² 4^−j. Then |a|^−2 · L W_j/q_b ≤ 4.77 · 8 · L³ = 38.2 L³.
- j = 0: |a|^−2 ≤ L², so |a|^−2 · 8L/1 = 8 L³.
- F: |D| > 0.24, so |a|^−2 ≤ 17.4, and 17.4 · L²/(1/L) = 17.4 L³.

Hence |r|² = |a|^−2 L W_b Q/(q_b M²) ≤ 40 Q L³/M² ≤ 1. ∎

**L4 (Z lower bound).** Take a column with |kx| < L/6, so cos θx > 1/2.
- D(kx, 0) = 2cos θx − 1 > 0 and D(kx, L/4) = 2cos θx − 3 < 0.
- D decreases monotonically in ky on [0, L/4], with steps ≤ 2·(2π/L).
- So some ky has |D| ≤ 2π/L, giving |a|^−2 ≥ L²/(4π² + 1).

There are ≥ L/3 − 1 ≥ L/6 such columns (L ≥ 8), so Z ≥ L³/(6(4π² + 1)) ≥ L³/243. ∎

**L5.** Since the good vector has norm² Z/M² ≤ 1, we get P = Z/M² ≥ 1/(243·320) = 1/77760 and Z ≤ M² = 320 L³. ∎

**L6 (precision).** Suppose every implemented ratio satisfies |r̃ − r| ≤ ξ. The envelope amplitudes have squared norm ≤ 1, so the unnormalized good-vector error is ≤ ξ, and the normalized error is ≤ 2ξ/√P ≤ 558ξ.
- From |1/ã − 1/a| ≤ |D̃ − D|/(|a||ã|), C_b/(M|a|) ≤ 1, and |ã| ≥ η, it suffices to take |D̃ − D| ≤ ξ/(2L) and rotation error ≤ ξ/2.
- Set ξ = ε/600. Then p = n + log2(1/ε) + O(1) bits suffice.
- Labels use the same D̃ circuit forward and backward, so the partition and uncomputation are exact.
- Clipping |r̃| to ≤ 1 costs at most ξ.

## 3. Corollaries

**C1 (Z0 bounds).** Z0 = Z/L² ∈ [L/243, 320 L]. Amplitude estimation of P gives Z0 to relative error ξ' in O(1/ξ') calls.

**C2 (five-source LCU is Θ(2^−n); conditional on the contract's LCU success formula Z/(||w||₁² Z0)).** Take f = (I − K)δ0, so ||w||₁ = 7.
- ||u||² = L^−2 Σ_k D²/(D² + η²).
- Points with |D| < η number ≤ 4L. Per (chart, σ, column) the count is ≤ 0.28 + 1, so at most 1 point, using L1's range, which holds since η ≤ 1/4.
- All other points contribute ≥ 1/2, so ||u||² ≥ 1/2 − 2/L.

The LCU success therefore lies in [(1/2 − 2/L)/(49·320 L), 243/(49 L)] = Θ(1/L). This rigorously confirms contract attack 3: source-LCU on top of this primitive is exponentially small for that family. The family itself is classically easy.

## 4. Reading the primary
Nothing in the primary is used as verified input. Its finite-n issues therefore do not affect the theorem, but they are worth recording:
- Eq. 26/A20/A21 are continuum heuristics.
- Truncating to a ring of width n_r loses the tail mass. That loss is not negligible at fixed n_r: by L2–L3, each dyadic shell holds O(L³ 2^−j), so a width-T cut keeps a 1 − O(1/T) mass fraction.
- The present construction has no truncation. All L² modes are covered, including the far region, whose mass fraction is ≤ 17.4·L²/(L³/243) = O(1/L).

## 5. Classical comparison (no advantage claimed)

- **Proved.** The Fourier law |a(k)|^−2/Z is classically sampled by the same envelope in O(77760·poly(p)) expected time. Draw b, kx, o and accept with probability |r|². So the Fourier state is not itself quantum-specific; only the inverse QFT is.
- **Sketch (unverified obligation PO-C).** The mixed laws (x1, ky) and (kx, x2) look classically samplable in poly(n). The plan:
  - The ky-marginal is the Fourier ky-marginal, sampled as above.
  - Given ky, H(x1, ky) = (z^{x1} + z^{L−x1})/((1 − z^L)(z − 1/z)), where z + 1/z = 3 − 2cos θy − iη and |z| < 1. This is the exact 1-D cycle resolvent.
  - |H|² partial sums are geometric, so inverse-CDF sampling over x1 takes n bisection steps, subject to a cancellation/precision audit.
  - This would also give exact sampling of the x1-marginal of the spatial law, by Parseval in y.
- **Open: the exact missing classical operation.** Sampling x2 | x1 from |Σ_ky e^{iθy x2} H(x1, ky)|², or evaluating G(x1, x2), at poly(n) cost. The integrand's analyticity strip has width ~η, so naive quadrature costs ~L. This gives O(L·polylog) per sample, which is sublinear in the L² grid but exponential in n.

No lower bound is asserted. A poly(n) classical solution to this 1-D conditional step is the decisive falsifier of any m=1 advantage claim.

## 6. Proof obligations and finite controls

- **PO-A.** Reversible p-bit cos(2πk/L) and arccos on [0.37, 0.82] with certified absolute errors 2^−p, at poly(p) gates. This is standard (polynomial or CORDIC with interval bounds); the explicit error certificate is not written out here.
- **PO-B.** Branch-state preparation over 4(n − 1) + 1 labels with O(n) rotations, at error ≤ ξ.
- **Finite controls (checks, not proofs; exact arithmetic for L = 16..2^12).**
  - Verify Z ≥ L³/243.
  - Verify max_k |r(k)| ≤ 1.
  - Verify every k with b(k) ≠ F lies in its window.
  - Verify P = Z/320L³.
- **Falsifiers of the theorem.**
  - Any k outside its label's window.
  - Any k with |r| > 1.
  - Any n with Z < L³/243.

Out of scope, as requested: arbitrary sources. Note that the envelope trick fails exactly where f̂ vanishes on the resonant curve, as in C2.