# Five-source (non-radiating) counterfamily on the native lattice: all-L theorem, source-register success, and the uncompute defect

## 0. Decisive result

The counterfamily holds for every L = 2^n ≥ 4, with explicit constants and no fitting. Take

f = (I−K)δ₀ = −3δ₀ + δ_(1,0) + δ_(−1,0) + δ_(0,1) + δ_(0,−1),  ‖w‖₁ = 7.

Write η = 1/L, G = A⁻¹δ₀, Z₀ = ‖G‖² and u = A⁻¹f = δ₀ − iηG. Then:

1. **Z₀ grows linearly.** (L/3 − 1)/(4π² + 1) ≤ Z₀ ≤ 16L. In particular Z₀ ≥ L/486.
2. **The exact field has bounded norm.** ‖u‖² = 1 − Z₀/L² lies in [max(0.248, 1 − 16/L), 1). It tends to 1.
3. **The Born law is almost a point mass at the origin.** P_f(0) ≥ ‖u‖² ≥ 1 − 16/L.
4. **The ring holds almost none of u.** Let R_C = {k : |1−λ(k)| ≤ C/L} with C ≤ L/2. The fraction of u's Fourier norm in R_C is at most (C+3)/(L‖u‖²). That is ≤ 4.04(C+3)/L for all L ≥ 4, and ≤ 2(C+3)/L for L ≥ 32.
5. **Full-domain source LCU succeeds with probability Θ(1/L) = Θ(2^{−n}).** Exactly, P_src = (1 − Z₀/L²)/(49 Z₀). This lies in [3.1·10⁻⁴/L, 9.92/L] (lower bound for L ≥ 32), despite only five sources.
6. **The ring-restricted pipeline fails worse.** With correct left/right source preparations, the source-register success is at most C²/(49L²). Any ring-supported output has overlap ≤ √(4.04(C+3)/L) with u. Its Born law is at total-variation distance ≥ 1 − (C+19)/L from P_f.
7. **The paper's literal circuit cannot produce this source at all.** Uncomputing with the same weighted preparation produces source weights |α_j|² ≥ 0. No phase choice yields weights proportional to (−3, 1, 1, 1, 1).

This falsifies only:
- the "constant ring width, success ~1/N_s" mechanism as a universal claim for sparse sources, and
- the same-ket uncompute step.

It says nothing about wave algorithms in general. The family is classically trivial: always output x = 0, with TV ≤ 16/L. When ε < 16/L, a full FFT on L² ≤ (16/ε)² points costs poly(1/ε). So this is an interface falsifier, not an application.

## 1. Conventions and exact identities (Theorem 0, proved)

**Fourier conventions.** Use the unitary DFT ĝ(k) = L⁻¹ Σ_x g(x) e^{−iθ·x}, with θ = 2πk/L ∈ (−π,π]². Inversion is g(x) = L⁻¹ Σ_k ĝ(k) e^{iθ·x}.

**Symbols.** λ(k) = 4 − 2cos θ_x − 2cos θ_y. Write d(k) = 1 − λ(k) = 2cos θ_x + 2cos θ_y − 3 and a(k) = d(k) + iη.

**Transforms.**
- δ̂₀ = 1/L
- f̂ = d/L
- Ĝ = 1/(L a)
- û = d/(L a)

**Norms.**
- Z₀ = L⁻² Σ_k 1/(d² + η²)
- ‖u‖² = L⁻² Σ_k d²/(d² + η²) = 1 − η² Z₀

**Ward identity.**
- A − A* = 2iηI and A is normal.
- Hence A⁻¹ − A⁻* = −2iη A⁻¹A⁻*, so Im G(0) = −η Z₀.
- Equivalently, Im(1/a) = −η/|a|².

**Value at the origin.** u(0) = 1 − iηG(0), so Re u(0) = 1 − η²Z₀ = ‖u‖². Therefore

P_f(0) = |u(0)|²/‖u‖² ≥ (Re u(0))²/‖u‖² = ‖u‖².

## 2. Counting lemma on the lattice curve λ = 1 (proved)

Let N(t) = #{k ∈ (ℤ/L)² : |d(k)| ≤ t}.

**(U) Upper bound: N(t) ≤ tL² + 3L for 0 ≤ t ≤ 1/2, hence N(t) ≤ 2tL² + 3L for all t ≥ 0.**

Proof:
1. Since |2c_x + 2c_y − 3| ≤ t ≤ 1/2 and each cosine is ≤ 1, we get c_x, c_y ≥ 1/4. Also c_x + c_y ≤ 7/4, so min(c_x, c_y) ≤ 7/8.
2. Consider the region where c_y ≤ 7/8, with k_x fixed. The y-condition is c_y ∈ J = [3/2 − c_x − t/2, 3/2 − c_x + t/2] ∩ [1/4, 7/8], an interval of length ≤ t.
3. On J, |sin θ_y| ≥ √15/8. So the preimage of J in θ_y ∈ (−π, π] is two intervals, each of length ≤ 8t/√15 by the mean value theorem.
4. Each interval contains at most 8tL/(2π√15) + 1 grid points. So each admissible k_x contributes at most 0.6575·tL + 2 values of k_y.
5. Admissible k_x satisfy |θ_x| ≤ arccos(1/4) < 1.32, so there are at most 0.42L + 1 ≤ 0.67L of them (L ≥ 4).
6. The region c_x ≤ 7/8 is symmetric. The total is ≤ 2·0.67L·(0.6575·tL + 2) ≤ tL² + 3L.
7. For t > 1/2, use N ≤ L² ≤ 2tL².

**(L) Lower bound: N(2π/L) ≥ L/3 − 1.**

Proof:
1. Fix k_x with cos θ_x > 1/2. There are 2⌈L/6⌉ − 1 ≥ L/3 − 1 such k_x.
2. Set g(k_y) = d(k_x, k_y). Then g(0) = 2c_x − 1 > 0 and g(L/2) = 2c_x − 5 < 0.
3. Consecutive grid values satisfy |g(a) − g(a+1)| ≤ 4π/L.
4. At a sign change, one of the two neighbouring points has |d| ≤ 2π/L. Distinct k_x give distinct points.

**Ring containment.** Any geometric θ-ring of width n_r grid spacings around the curve λ = 1 lies inside R_C with C = 4√2·π·n_r. This follows from |∇_θ λ| ≤ 2√2.

## 3. Theorems (proved here; parent should re-verify)

### Theorem 1: (L/3 − 1)/(4π² + 1) ≤ Z₀ ≤ 16L

**Lower bound.** Each of the ≥ L/3 − 1 points from (L) contributes at least L⁻²/((2π/L)² + L⁻²) = 1/(4π² + 1).

**Upper bound.** Split frequencies into dyadic shells and apply (U):

| Shell | Condition on \|d\| | Contribution to Z₀ |
|---|---|---|
| S₀ | \|d\| ≤ η | ≤ N(1/L) ≤ 4L |
| S_j (j ≥ 1) | 2^{j−1}η < \|d\| ≤ 2^jη | ≤ N(2^j/L)/4^{j−1} ≤ 8L/2^j + 12L/4^j |

Summing over j ≥ 1 gives ≤ 12L. The total is 16L.

The asymptotic constant πρ(1)L, where ρ is the density of states, is plausible but not proved here. It is labelled speculation.

### Theorem 2: max(0.248, 1 − 16/L) ≤ ‖u‖² < 1 and P_f(0) ≥ 1 − 16/L

1. The upper bound and the 1 − 16/L bound follow from Theorem 0 and Theorem 1.
2. For the uniform bound, take the ≥ (L/2 + 1)² frequencies with c_x, c_y ≤ 0. There d ≤ −3, so each term is ≥ 144/145. This gives ‖u‖² ≥ 0.248.
3. P_f(0) follows from Theorem 0.

### Theorem 3: shell fraction of u

φ_C = ‖P_{R_C} u‖²/‖u‖² ≤ L⁻² N(C/L) · [C²/(C² + 1)] / ‖u‖² ≤ (C+3)/(L‖u‖²).

This tends to 0 at rate 1/L for fixed C. Even C = o(L) suffices.

**Contrast with G.** The fraction of G outside R_C is ≤ (16L/C + 16L/C²)/Z₀ ≤ 15552/C for C ≥ 1 (crude constant). So the ring captures a single source well but not this source combination.

### Theorem 4: source-register success

**(a) Full-domain LCU with exact single-source states.** Use correct left/right preparations: V_R|0⟩ = Σ_j √(|w_j|/7) |j⟩, and V_L carries the phases of w_j. The post-selected vector is u/(7√Z₀).

P_src = ‖u‖²/(49 Z₀) = 1/(49 Z₀) − 1/(49 L²)

**Upper bound, all L ≥ 4:** ≤ 12(4π² + 1)/(49L) ≤ 9.92/L.

**Lower bound:** ≥ (1 − 16/L)/(784 L), which is ≥ 3.1·10⁻⁴/L for L ≥ 32. For 4 ≤ L < 32, use ‖u‖² ≥ 0.248 instead: P_src ≥ 0.248/(784 L) ≥ 3.1·10⁻⁴/L.

**Repetition cost.** Amplitude amplification still needs Θ(√L) = Θ(2^{n/2}) rounds.

The general form is the Gram form P_src = w*Γw/(‖w‖₁² Z₀), with Γ_jl = ⟨T_{x_j}G, T_{x_l}G⟩. It is not 1/m.

**(b) Ring-restricted pipeline (lattice analogue of Eqs. 23–25).** Let ψ_res be any normalized resonant state supported on R_C. For example, ψ_res ∝ (η/a)·1_R with |q| ≤ 1.

- The correct LCU multiplies amplitude k by Σ_j (w_j/7) e^{−iθ·x_j} = d(k)/7.
- So the source-register success is Σ_{k∈R} |ψ_res|² d²/49 ≤ C²/(49 L²).
- Multiplying by P_res ≤ 1 gives a total of ≤ C²/(49 L²).
- On success with the q-weighted ψ_res, the output is exactly P_R u/‖P_R u‖. Its overlap with u/‖u‖ is √φ_C ≤ √(4.04(C+3)/L). So the paper's Eq. 29 error tends to 1.

**Total-variation bound for any R-supported state ψ.**
- |ψ(0)|² = |L⁻¹ Σ_{k∈R} ψ̂(k)|² ≤ |R|‖ψ‖²/L² ≤ (C+3)‖ψ‖²/L.
- Hence TV(Q, P_f) ≥ P_f(0) − Q(0) ≥ 1 − (C+19)/L.

## 4. Weighted-source uncompute error in the supplied primary equations (proved)

The text (LF 236–450 and the Fig. 3 caption) describes these steps:
1. Prepare V|0⟩ = Σ α_j |j⟩.
2. Apply controlled phases Φ_j = diag(e^{−iθ·x_j}).
3. Apply the inverse preparation V†.
4. Post-select the source register on |0⟩.

The result is

⟨0|V† (Σ_j |j⟩⟨j| ⊗ Φ_j) V|0⟩ = Σ_j |α_j|² Φ_j.

**Consequences:**
- **Eq. 24 is not what the circuit makes.** Eq. 24 claims arbitrary complex w_j. The circuit produces only w_j ∝ |α_j|² ≥ 0; phases on α_j cancel.
- **The five-source weights are unreachable.** No global phase makes (−3, 1, 1, 1, 1) nonnegative.
- **The realized source differs on the curve.** The realized source f_α has Re(L f̂_α) ≥ |α₀|² + ½ Σ_e |α_e|² ≥ ½ on λ = 1, because c_x, c_y ≥ ½ there. So it is a genuinely radiating source with a different field. Any ring output still obeys the total-variation bound of Theorem 4(b).
- **Eqs. 28/31 (P = 1/N_s) do not follow from this calculation.** With equal weights, the success probability is
  N_s⁻² Σ_{j,l} Σ_k |ψ_res(k)|² e^{−iθ·(x_j − x_l)}.
  This equals 1/N_s only if the ring autocorrelation vanishes at every nonzero source difference. That is not shown, and for unit-spaced sources the ring cosines are ≥ ½. The 1/N_s value appears to be a random-phase heuristic.
- **Padding labels (implementation-dependent caveat, not verified).** Hadamard on ⌈log N_s⌉ qubits creates unused labels. If those labels receive the identity phase, they act as extra sources at x = 0.
- **Repair.** Use distinct left/right preparations, as in standard LCU. The success is then the Gram form above, and Theorem 4 applies.
- **Minor.** The Fig. 3 caption uses e^{+i(…)} while the text uses e^{−i(…)}.

## 5. Continuum paper claims versus the discrete counterexample

**Paper claims (continuum or numerical; not verified here):**
- Eqs. 26/27/30/A20/A21: a constant P_res, from a continuum radial integral.
- Figs. 4–5: a constant ring width suffices. This rests on 64×64-style numerics with point or two-emitter sources.
- Eqs. 28/31: source success ~1/N_s.

I did not check the lattice validity of the A21 factors.

**Our result (native discrete; exact identities and all-L inequalities):** The lattice symbol and the curve λ = 1 are used directly; the continuum circle is not imported. The counterexample shows that the claimed ring accuracy and the 1/N_s success claim are source-dependent and fail for a fixed 5-site integer-weight source.

**Speculation, not claimed:** The continuum analogue is the standard non-radiating-source phenomenon, where f = (Δ + k²)h gives a localized u. This suggests the same failure in the paper's own setting, but I have not proved it.

## 6. Finite control (hand calculation, L = 4; illustration only)

The d-multiplicities are:

| d | +1 | −1 | −3 | −5 | −7 |
|---|---|---|---|---|---|
| Points | 1 | 4 | 6 | 4 | 1 |

From these:
- Z₀ = 5/17 + 6/145 + 4/401 + 1/785 ≈ 0.34675
- ‖u‖² ≈ 0.97833
- P_src ≈ 0.0576

This is consistent with Theorems 1–4 but has no asymptotic force. Note that the S₀ shell is d = ±1 here, since η = 1/4.

## 7. What remains open, falsifiers of this report, and restricted endpoints

**Not falsified:**
- Single-source ring preparation.
- Generic sparse sources.
- Any classical hardness claim. None is implied.
- Any quantum advantage claim. None is implied.

**Falsifiers of this report:** The parent should check:
- the arithmetic and arccos bounds in (U);
- the sign-change argument in (L);
- the dyadic sums;
- the Ward identity.

Any error there would change only the constants unless the counting lemma itself fails.

**Possible RESTRICTED endpoint (not universal).** One could promise that |d(k) f̂-ratio| is spectrally non-vanishing on R, for example |L f̂(k)| ≥ γ‖w‖₁ for k ∈ R. This would still have to address:
- Gram-form success;
- off-ring tails;
- finite-bit trigonometry;
- readout.

None of these are paid here.

**Missing operation for the general problem (unchanged).** A paid lattice resonant-state preparation on R_C, with proven P_res and ring error for arbitrary sparse signed sources.