# Addressed trilinear quadratures from native S and N pulses: explicit compiler with poly(D, 1/ε) operator-norm error

## 1. Verdict

**Yes, under the stated hypotheses.** There is a uniform, explicit classical compiler that emits only actual S and N pulses with signed binary-rational times. It approximates the addressed trilinear quadrature for any selected product P in operator norm on the whole momentum-D sector. The pulse count is O(D^8/ε) per gate under a crude rigorous norm bound, and each time has O(log(D/ε)) bits.

- **Both quadratures (real and imaginary) work.** Arbitrary phase φ is obtained from the same pulse pattern.
- **No linear combination of unitaries (LCU), no averaging oracle, no deep commutators.** The "average" is a first-order product formula over N-conjugated S pulses. The Fourier identity behind it is exact.
- **A second result removes the main stated blocker (parent item 5).** The same filtered pair Hamiltonian, run to a full 2π auxiliary-level rotation, gives an exact encoded CZ. No group commutator is needed.
- **Status.** The lemmas below are proved deductions, given these hypotheses:
  - the contract's S and N exactly as written;
  - exact pulse access;
  - mode-distinctness (Sidon) assumptions;
  - distinct odd primes with pq ≥ D and p+q ≤ D.
- **Not proved here.** The prime/Sidon construction (assumed, as instructed). I also did not verify the MM spectral normalization; the compiler does not use it.

## 2. Conventions

- **Operators.**
  - C_ij = a_i† a_j† a_{i+j}.
  - S = Σ over ordered (i,j) with i,j ≥ 1 and i+j ≤ D of s_ij (C_ij + C_ij†), where s_ij = √(ij(i+j)).
  - N = Σ k² n_k.
- **Sector.** H_D is the span of occupation vectors with Σ k n_k = D. All norms are on H_D.
- **Pulses.**
  - The N-pulse e^{-iτN} has τ ∈ 2π·2^{-b}ℤ.
  - The S-pulse e^{-iηS} has η ∈ 2π·2^{-b}ℤ.
  - N has integer spectrum, so e^{-2πiN} = I. Every N-conjugation can therefore use a nonnegative time.

## 3. Lemmas (proved)

### Lemma A (frequency)

[N, a_k†] = k² a_k†, so e^{iθN} a_k† e^{-iθN} = e^{iθk²} a_k†. Therefore

S(θ) := e^{iθN} S e^{-iθN} = Σ s_ij ( e^{-2iθ·ij} C_ij + e^{+2iθ·ij} C_ij† ),

because i² + j² − (i+j)² = −2ij.

### Lemma B (exact discrete Fourier filter, aliasing, both quadratures)

Definitions:

- M = 2^{⌈log₂(D²+1)⌉}, so D² < M ≤ 2D².
- θ_k = 2πk/M.
- f_k = 2cos(4πkP/M + φ), which is real.
- H_{P,φ} := Σ over ordered (i,j) with ij = P of s_ij ( e^{iφ} C_ij + e^{-iφ} C_ij† ).

**Identity.** (1/M) Σ_k f_k S(θ_k) = H_{P,φ}.

*Proof.* The coefficient of C_ij is (1/M) Σ_k (e^{i(2θ_kP+φ)} + e^{-i(2θ_kP+φ)}) e^{-2iθ_k ij}. This equals e^{iφ}·[M divides 2(P−ij)] + e^{-iφ}·[M divides 2(P+ij)].

In the sector, ij ≤ D²/4 and P ≤ D²/4. So |2(P−ij)| ≤ D²/2 < M and 0 < 2(P+ij) ≤ D² < M. Hence:

- the first bracket is 1 iff ij = P;
- the second bracket never holds.

The C† coefficient is the complex conjugate. ∎

**Corollaries.**

- **No aliasing.** M > D² suffices; the parent's M > 2D² is more than needed.
- **φ = 0** gives the real quadrature X_op = C + C†.
- **φ = −π/2** gives i(C† − C), the parent's Y_op. φ = +π/2 gives its negative.
- **Equal weights vanish exactly.** 0 < 2ij < M, so no zero frequency exists, and (1/M) Σ_k S(θ_k) = 0. Consequently the shifted weights g_k = f_k + 2 ≥ 0 give the same H_{P,φ}. Signed S-times are therefore not even required.

### Lemma C (cutoff is automatic; fiber; ordered-pair factor)

**Cutoff.** On H_D, any term with i+j > D vanishes:

- a_{i+j} annihilates, because n_{i+j} = 0;
- C† needs n_i, n_j ≥ 1, which forces i+j ≤ D.

So the global cutoff is not an extra assumption.

**Fiber for a semiprime.** For P = pq with distinct odd primes, the ordered pairs are exactly (p,q), (q,p), (1,pq), (pq,1).

- C_pq = C_qp, which gives the factor 2.
- The terms for (1,pq) vanish on H_D when 1+pq > D, i.e. when pq ≥ D.

Hence

H_{pq,φ} = 2√(pqc) ( e^{iφ} a_p† a_q† a_c + h.c. ), with c = p+q ≤ D.

**Refinement.** pq ≥ D is sufficient but not necessary for code-level addressing. The alias term acts only on states with mode 1+pq occupied, or with modes 1 and pq both occupied. Mode 1 and the odd composite pq are never code modes. So it is enough that 1+pq is never an occupied code or auxiliary mode.

### Lemma D (norm, rigorous, independent of MM)

C_ij maps occupation basis vectors injectively to occupation basis vectors. It is therefore a weighted partial permutation, and its norm equals its largest weight.

- For i ≠ j the weight is √(n_{i+j}(n_i+1)(n_j+1)).
- In-sector constraints give n_{i+j} ≤ D/(i+j), n_i+1 ≤ D/i and n_j+1 ≤ D/j. The case i = j is analogous.
- So s_ij ‖C_ij‖ ≤ D^{3/2}, and ‖s_ij(C_ij + C_ij†)‖ ≤ 2D^{3/2}.
- There are D(D−1)/2 ordered pairs.

Therefore ‖S‖ ≤ D^{3/2}·D(D−1) ≤ D^{7/2}.

If the contract's spectral claim (eigenvalues 2Σ contents, under this exact normalization) holds, then ‖S‖ ≤ D(D−1). The excerpt does not show the V_k normalization, so I do not use this.

### Lemma E (product formula)

For Hermitian A and B:

‖e^{-iτ(A+B)} − e^{-iτA} e^{-iτB}‖ ≤ (τ²/2) ‖[A,B]‖.

*Proof.* Use variation of constants on V(s) = e^{-isA} e^{-isB}, together with ‖e^{-isA} B e^{isA} − B‖ ≤ s‖[A,B]‖. Then peel off terms one by one.

Apply this with A_k = (f_k/M) S(θ_k), Λ = Σ‖A_k‖ ≤ 2‖S‖, and r steps:

‖e^{-itH} − (Π_k e^{-i(t/r)A_k})^r‖ ≤ t²Λ²/(2r) ≤ 2t²‖S‖²/r.

Two facts make this a pulse sequence:

- e^{-i(t/r)A_k} = U_k e^{-iη_k S} U_k†, with U_k = e^{iθ_kN} and η_k = t f_k/(rM).
- θ_k is a binary rational, so the N-conjugations are exact native pulses.

### Lemma F (time rounding)

‖e^{-iηS} − e^{-iη'S}‖ ≤ |η − η'|·‖S‖. The θ_k are exact, so only the S-times incur error.

## 4. Explicit compiler QUAD(D, P, φ, t, ε)

1. Set M = 2^{⌈log₂(D²+1)⌉} and r = ⌈4t²D⁷/ε⌉.
2. Set b = ⌈log₂(8π r M D^{7/2}/ε)⌉ + 1.
3. For k = 0..M−1, compute η_k = 2t·cos(4πkP/M + φ)/(rM) to precision π·2^{-b}. Round it to η̃_k ∈ 2π·2^{-b}ℤ.
4. Emit, in application order, the following block r times. For k = 0..M−1:
   - N-pulse, time 2πk/M;
   - S-pulse, time η̃_k;
   - N-pulse, time 2π(M−k)/M.

   Adjacent N-pulses merge, since each U_k† U_{k+1} is a single N-pulse of time 2π(M−1)/M. The merged list has at most 2rM+1 pulses.

**Theorem.** The emitted unitary W̃ satisfies ‖W̃ − e^{-itH_{P,φ}}‖ ≤ ε on H_D.

- Trotter error is at most ε/2 (Lemma E).
- Rounding error is at most 2π·2^{-b}·rM·D^{7/2} ≤ ε/2 (Lemma F).

**Cost.**

- Pulses: O(D²·(1 + t²D⁷/ε)).
- Bits per time: O(log(Dt/ε)).
- Classical work: polynomial, since cosines are computed to b bits.

For the code gates below, t² ≤ π²/(4D·c), so the pulse count is O(D⁸/ε). If ‖S‖ ≤ D(D−1) holds, this becomes O(D⁵/ε). A symmetric (second-order) formula would improve the 1/ε dependence; I do not rely on it.

## 5. Action on the code

### Local quadrature (exact invariant two-level code)

Assume all code modes {p_k, q_k, c_k} are distinct. On the code, H_{p_iq_i,φ} restricted equals:

2√(p_i q_i c_i) (cos φ X_i + sin φ Y_i) ⊗ I_rest,

with |0⟩ = 1_c and |1⟩ = 1_p 1_q. The matrix element ⟨1_p1_q|a_p† a_q† a_c|1_c⟩ = 1, and n_p − n_q and n_c + n_p are conserved. The code is therefore exactly invariant under the target e^{-itH}.

- Choosing t = α/(2√(p_i q_i c_i)) gives exp(−iα(cos φ X + sin φ Y)).
- Leakage comes only from the compiled error and is at most ε.

### Encoded CZ (removes the item-5 group-commutator blocker)

Take P = p_i p_j and r = p_i + p_j ≤ D. Assume p_i p_j ≥ D, and that r is distinct from all code modes. Then:

H_{P,0} = 2√(p_i p_j r)(a_{p_i}† a_{p_j}† a_r + h.c.).

- It annihilates the code states |00⟩, |01⟩ and |10⟩.
- On |11⟩ it couples only to the auxiliary state |L⟩ = |q_i, q_j, 1_r⟩, with matrix element 1.

At t = π/(2√(p_i p_j r)), the target e^{-itH} acts as e^{-iπX_eff} = −I on span{|11⟩, |L⟩}, and as identity on the other code states. This is exactly CZ ⊗ I, with zero ideal leakage. It is compiled by QUAD with error ε.

The parent's cross-Kerr group commutator, and its O(a³) leakage, are therefore unnecessary.

### End to end

1. Start from occupation μ = (c_1, …, c_n), which is explicit.
2. Compile each gate with error ε/G.
3. Decode: qubit k reads 0 if n_{c_k} = 1, reads 1 if n_{p_k} = n_{q_k} = 1, and otherwise flags.

Total variation distance to the ideal is at most G·(ε/G) = ε. The total pulse count is O(G²D⁸/ε). D is polynomial whenever the assumed prime/Sidon selection yields polynomial R.

## 6. Limits and counterexamples (what does not work)

- **Composite products cannot be addressed by this mechanism.** For example, P = 12 with D ≥ 8: H_{12,φ} necessarily contains both (2,6) and (3,4). N-conjugation sees only ij. Whether higher-order words could separate them is not addressed, and no impossibility claim is made.
- **Square products are also unaddressable here.** For P = i², the term C_ii shares its fiber with every other factorization of i².
- **The alias condition is a real constraint.** If 1+pq equals an occupied mode (some c_k or an r used in a CZ), the alias (1,pq) splits that boson and the gate leaks. pq ≥ D excludes this; with primes in [R, 2R] and R ≥ 4n, D ≤ 4nR ≤ R² ≤ pq.
- **Time grids.** If pulse times were restricted to a fixed non-dyadic grid, or to times bounded away from 0, the construction would need rework. With only nonnegative S-times allowed, Lemma B's shifted weights g_k still work.

## 7. Remaining proof obligations and falsifiers

**Obligations.**

1. An explicit polynomial-size Sidon prime family, with an elementary prime-count bound. Assumed here, not proved.
2. Mode-distinctness of all p_k, q_k, c_k and all used r_ij. Assumed here.
3. Confirmation that the contract's S matches the intended physical control. My bounds use only the S written in the contract, not MM's normalization.

**Falsifiers.** Any one of the following would break the result:

- a pair (i,j) with ij ≠ P, i+j ≤ D, and M dividing 2(P ∓ ij) (impossible if M > D²);
- an occupied mode equal to 1+pq;
- a code-mode collision with some r_ij;
- a numerically computed ‖W̃ − e^{-itH}‖ exceeding the stated bound at small D. This would indicate an error in Lemma D or Lemma E.

Finite numerical checks can falsify these statements but cannot establish them.