# Native finite-gate simulation and reflection compiler for the Jack transform: a coherent construction with no measurement, abort, or discard

## 0. Verdict

**This obligation is proved, conditional on the supplied native facts F1–F3 and, for corner rotations only, interface F4 (all in §1).**

The construction gives each of the following as a coherent unitary circuit:

- controlled `exp(itL_d)` for every `|t| ≤ 8`;
- the content reflection `2Q_{c*} − I`, with `c*` either classical or held in a register;
- the marker-zero reflection `2P_0 − I`;
- input-dependent rotations, including corner-probability trees.

Every circuit uses only the gates `{H, S, CNOT, Toffoli}`. There is no mid-circuit measurement, no abort, no discard, no unit-cost real rotation, no QFT phase rotation, and no sparse-matrix oracle. Each circuit's actual inverse is usable as stated in Lemma 2.

Error is measured in the clean-isometry sense. This is uniform over:

- all register contents, valid or invalid;
- every reference system;
- both branches of any control.

The cost is `poly(d, log 1/η)` gates, workspace, and classical bit operations. For example, one content reflection uses
`O((d+1)^2 Λ (d log(d+1) + Λ^2))` gates, where `Λ = log2((d+1)/η)`. That bound comes from the construction below and is deliberately loose.

**Structural fact that makes squared tolerances cheap.** No half-block gadget is ever placed inside the `W` of another half-block. Only the leaves (simulation segments and rotation gadgets) suffer the square-root loss, and they suffer it once. Everything above the leaves, including the proposal's polar amplification, composes errors linearly through the telescoping lemma.

**Not proved here:**

- F1–F4 themselves;
- the polar approximation and its call count;
- stage composition;
- H1–H2 from the earlier report.

No speedup, novelty or hardness claim follows.

---

## 1. Model, inputs, and what is assumed

**Data register.** The registers hold `m_1, …, m_d` and `ℓ`, each with `⌈log2(d+1)⌉ + 1` bits. The valid set `V_d` is the set of basis states with `Σ k m_k + ℓ = d` and no overflow. Every other basis state is invalid. The degree `d` is classical for each call.

**Supplied facts used, not re-derived:**

- **F1 (from the earlier report §5.1).** In the normalized basis on `V_d`, `L_d` has:
  - diagonal entries `2ℓ`;
  - off-diagonal entries `√(3k m_k)` between `(m, ℓ)` and `(m − e_k, ℓ + k)`, where `m_k` is read at the upper endpoint;
  - no other entries.
- **F2.** The spectrum of `L_d` on `V_d` lies in the integers in `[−d, 3d]`.
- **F3.** The marker projector satisfies `P_0 = π_0 = 1{ℓ = 0}` on `V_d`.
- **F4 (interface for corner rotations only).** Each needed probability `p(x)` has a reversible classical circuit `C_p(b')`. On a basis input `x`, it outputs an integer `P(x)` with `|P(x) − 2^{b'} p(x)| ≤ 1`, at size `poly(d, b')`.
  - The native-isometry tree weights `k m_k / n` satisfy F4 exactly.
  - Whether the B/C corner probabilities `p_{λ,s}` have such a formula is **not** in the supplied evidence. If not, that component stays open.

**Ideal targets.**
- `L̂' := (L_d − c* I)|_{V_d} ⊕ 0_{invalid}`. Here `c* = 0` for plain simulation, and `c*` is zeroed by a range flag whenever `c* ∉ [−d, 3d]`.
- Reflections act as the identity on invalid states and on out-of-range `c*`.

**Metric.** A unitary `A` on (workspace `a`) ⊗ (system) ⊗ (reference) **η-implements** a unitary `U` if
```
‖A(|0_a⟩ ⊗ I) − |0_a⟩ ⊗ (U ⊗ I_ref)‖ ≤ η.
```

**Exactness convention.** Every circuit below equals its stated matrix exactly, not up to a global phase. Specifically:
- `−I` is `(XZ)^2` on a pool qubit.
- `Z = S^2` and `CZ = (I⊗H) CNOT (I⊗H)`.
- A phase `i` applied conditionally on a flag is `S` on that flag.

---

## 2. Four compiler lemmas

**Lemma 1 (telescoping).** Suppose a circuit is a sequence of:
- exact gates that never touch the pool `a`, and
- subroutine instances `A_i`, each `η_i`-implementing `U_i`.

Then the circuit `Ση_i`-implements the ideal product, even if the pool is reused sequentially.

*Proof.* Write the actual product as `Π A_i` and the ideal as `Π Â_i`, where `Â_i := I_a ⊗ U_i`. Use
```
Π A_i − Π Â_i = Σ_i (A_N … A_{i+1}) (A_i − Â_i) (Â_{i−1} … Â_1).
```
The ideal prefix maps `|0_a⟩ ⊗ ·` into `|0_a⟩ ⊗ ·`. The actual suffix is unitary. ∎

**Lemma 2 (actual inverse).** If `A` η-implements `U`, then `A†` η-implements `U†`.

*Proof.* For a unit vector `φ`, set `u := U†φ`. Then
```
‖A†|0, φ⟩ − |0⟩ U†φ‖ = ‖|0⟩ U u − A|0, u⟩‖ ≤ η. ∎
```

**Lemma 3 (half-block, clean form).** This replaces the abort in report §4.3 and the discard in BCCKS.

- Let `W` be a unitary, `P = |0⟩⟨0|` on a signal set, `R = I − 2P`, and `B = ⟨0|W|0⟩`.
- Assume `‖B − U/2‖ ≤ ρ ≤ 1/8` for some unitary `U`.
- Let `O = −W R W† R W`, as in BCCKS.

Then `O` `√(6ρ)`-implements `U`.

*Proof.* By BCCKS eq. (13)–(14) in the supplied source, `⟨0|O|0⟩ = 3B − 4BB†B`. Put `B = U/2 + E`. Direct expansion gives
```
3B − 4BB†B = U + E − U E† U − 2(U E† E + E U† E + E E† U) − 4 E E† E,
```
so its distance from `U` is at most `2ρ + 6ρ^2 + 4ρ^3 ≤ 3ρ`.

For a unit vector `Ψ` on system ⊗ reference, let `v = O|0, Ψ⟩` and `w = |0⟩ UΨ`. Both are unit vectors, and
```
‖v − w‖^2 = 2 − 2 Re⟨w, v⟩ = −2 Re⟨UΨ, (⟨0|O|0⟩ − U)Ψ⟩ ≤ 6ρ. ∎
```
The off-clean component is kept coherently. Nothing is measured.

**Lemma 4 (control folding).** The cases below are those used in this report.

- **Form of gadgets.** Each gadget has the form `Had · CORE · Had`. The Hadamard layers act only on seed or signal registers. `CORE` is a reversible permutation together with phases in `{±1, ±i}`, applied through Toffoli-computed flags.
- **Controlled core.** Folding a control `κ` into every flag gives `c-CORE`.
- **Controlled gadget.** `Had · c-CORE · Had` equals `c-(Had · CORE · Had)`, because `Had^2 = I`.
- **Controlled half-block.** `c-O` is obtained by controlling:
  - all three `W` cores;
  - both reflections, as `I − 2P ⊗ |1⟩⟨1|_κ`;
  - the scalar `−1`, which becomes `Z` on `κ`.
- **Errors.** The off branch is exactly the identity. Since the operator is block-diagonal in `κ`, the error is the on-branch error, not a sum.

Controlled-`H` is never needed.

---

## 3. Exact native block encoding `U_L` (no rotations, no oracle)

**Constants.**
- `B_0` = least power of two `≥ 4(d+1)`.
- `M_0` = least power of two `≥ 2d+1`.
- `Γ = M_0 B_0 ≤ 32(d+1)^2`.

**Terms.**
- `j = 0`: the diagonal `2ℓ − c*`, with `|·| ≤ 3d ≤ B_0`.
- `(k, a)` for `1 ≤ k ≤ d`, `a ∈ {0,1}`: the edges of F1 whose upper endpoint has `m_k ≡ a (mod 2)`.
- Zero padding up to `M_0` terms.

**Each `(k, a)` class is a matching.**
- A vertex with `m_k ≡ a` can only be an upper endpoint. Its unique possible partner is `(m − e_k, ℓ + k)`, which exists iff `m_k ≥ 1`.
- A vertex with `m_k ≢ a` can only be a lower endpoint. Its unique possible partner is `(m + e_k, ℓ − k)`, which exists iff `ℓ ≥ k`. Then `k(m_k + 1) ≤ d`, so no overflow occurs.
- Edges preserve degree.

**Canonical involution and its uncomputation.** Let `τ_{k,a}` be the partner map. It is the identity on unmatched and invalid states, and it is an involution. Implement controlled `τ` as follows:
1. Compute `s = τx` into scratch. Reading `m_k` at a quantum index `k` uses an `O(d log(d+1))` multiplexer.
2. Compute the pair-symmetric integer
   `N = round(2^b √(3k m_k^{upper}) / B_0)` from whichever of `x`, `s` is upper, using integer square root. Set `N = 0` if the pair is unmatched or invalid.
3. Compute the label flag `f`.
4. Controlled on `f`, swap the system register with `s`.
5. The registers now hold `(z, τz)` with `z ∈ {x, τx}`. Since `N` is symmetric in the pair, recomputing it reproduces the same value, so `f` and `N` uncompute exactly.
6. XOR `τ(z)` into `s`, which returns `s` to zero because `τ` is an involution.

All scratch returns exactly to zero.

**Dyadic coefficients.** Use a seed `y ∈ [0, 2^{b+1})` and a term entry `v ∈ [−1, 1]` with `N = round(2^b v)`.
- Labels `y < 2^b + N` apply `+op`; the other labels apply `−op`, with the sign being `Z` on a flag.
- The block is then `(N / 2^b) · op`.
- Unmatched states have `op = I` and `N = 0`, so they contribute a zero block.
- Rounding error is at most `2^{−b−1}`. The diagonal term is exact, because `B_0 ≤ 2^b` is a power of two.

**Result.** Define `U_L = Had · SEL · Had` over the selector (`log2 M_0` qubits) and the seed (`b+1` qubits). Its clean block is exactly `L̃'/Γ`, where:
- `L̃'` is real symmetric (Hermitian);
- `‖L̃' − L̂'‖ ≤ Γ 2^{−b−1}`;
- `L̃'` vanishes on invalid states;
- `L̃'` preserves `V_d` exactly. Hence every circuit below commutes exactly with the validity flag.

**Cost.** `G_L = O(d log(d+1) + (b + log(d+1))^2)` gates.

---

## 4. Controlled `exp(itL)`, `|t| ≤ 8`

**Segment construction.** Let `R = max(1, ⌈8Γ|t|⌉) ≤ 2^{12}(d+1)^2`, `x = Γ|t|/R ≤ 1/8`, and `σ = sgn t`.

**Seed labels.** Use a seed `z ∈ [0, 2^{c+1})`.
- `n_k = round(2^c x^k / k!)` labels are assigned to clock value `k = 0..K`, with phase `(iσ)^k`.
- The remainder is split evenly between `±I`. If parity forces it, adjust `n_0` by one.
- The `n_k` are hard-wired classical constants. When `t` involves `π`, compute `π` to `c + O(log K)` bits.

**Clock control.** Using `K` fresh copies of `U_L` on signals `s_1, …, s_K`, apply `c-U_L^{(j)}` controlled on `u_j = [k(z) ≥ j]`. The flag `u_j` is computed from `z` and then uncomputed.

**Clean block of the segment walk `W_seg`.** On the signal set
```
𝒫_seg = (z, s_1, …, s_K),   of size (c+2) + K(log2 M_0 + b + 2),
```
the clean block is
```
B = (1/2) Σ_k a_k (iσ L̃'/Γ)^k,    |a_k − x^k/k!| ≤ 2^{1−c}.
```

**Block error.** With `U = e^{itL̃'/R}`,
```
‖B − U/2‖ ≤ 8^{−(K+1)} + (K+1) 2^{−c} =: ρ.
```
This uses `‖L̃'/Γ‖ ≤ 1` and `Σ_{k>K} x^k/k! ≤ (8/7) 8^{−(K+1)}`.

**Assembly.** Let `O_seg = −W R W† R W`. By Lemma 3, each segment `√(6ρ)`-implements `U`. Composing `R` segments with a reused pool gives, by Lemma 1 and Duhamel's formula, an `η`-implementation of `e^{itL̂'}` with
```
η ≤ R √(6ρ) + |t| Γ 2^{−b−1}.
```

**Parameters (squared internal tolerance).** For `0 < η ≤ 1`:
```
b = ⌈log2(8Γ/η)⌉
K = ⌈log_8(48 R^2/η^2)⌉
c = ⌈log2(48 (K+1) R^2/η^2)⌉
```
These give `ρ ≤ η^2/(24 R^2)`, so `R√(6ρ) ≤ η/2`. All three parameters are `O(Λ)`.

**Resources.**

| Quantity | Bound |
|---|---|
| Gates | `G_exp = R · O(K(G_L + c)) = O((d+1)^2 Λ (d log(d+1) + Λ^2))` |
| Workspace | `O(d log(d+1) + Λ^2)`: `𝒫_seg`, the τ copy, sqrt scratch, flags; reused across segments |
| Classical bit operations | `O(K(c + log K)^2 + c^3)` |

- **Control.** Apply Lemma 4.
- **Inverse.** `O_seg†` serves by Lemma 2, or rerun the construction with `−t`.
- **Special cases.** `t = 0` and `d = 0` (where `L_0 = 0`) are implemented exactly as the identity.

---

## 5. Reflections (exact involutions, no QFT, no flag measurement)

### 5.1 Content reflection `2Q_{c*} − I`

Let `M` = least power of two `> 4d`, and `q = log2 M`.

**Ideal construction.** `A := Π_j c_{y_j}-exp(i t_j L̂')`, preceded by `Had^{⊗q}` on `y`. Here `t_j = 2π 2^j/M ≤ π`, and the Hamiltonian is the shifted `L̂' = L − c*`.
- On an eigenvector with eigenvalue `μ = c − c*`, the `y`-register holds the state `χ_μ`.
- Since `|μ| ≤ 4d < M`, `χ_0` is uniform and `χ_{μ≠0}` is orthogonal to it.
- Then `C := A† · Had^{⊗q} · Z[valid ∧ in-range ∧ y ≠ 0] · Had^{⊗q} · A` equals `(2Q_{c*} − I) ⊕ I_invalid` exactly. Degenerate eigenspaces need no special handling, because the construction is linear.

**Actual circuit.** Take `η_j = η/(2q)` for each controlled evolution. Then `A` is `η/2`-close, and `C` is `η`-close. The proof writes `A†FA − Â†FÂ = A†F(A − Â) + (A† − Â†)FÂ` and bounds the second term by Lemma 2.

Further properties:
- **Involution.** `C` is an exact involution, since `(A†FA)^2 = I`. Hence the actual `W† = C · (marker reflection)` holds exactly.
- **Controlled version.** Control only `F`. With the control off, `A†A = I` exactly.
- **Cost.** Using `Σ_j R_j ≤ 16πΓ + q`:
  - gates `O((d+1)^2 Λ (d log(d+1) + Λ^2))`;
  - workspace `O(d log(d+1) + Λ^2)`.

### 5.2 Marker reflection `2P_0 − I`

Apply `Z` to the flag `[valid ∧ ℓ ≠ 0]`.

- The circuit is exact and is an involution.
- It acts as `+I` on invalid states.
- It costs `O(d log(d+1))` gates and `O(log d)` scratch.

---

## 6. Input-dependent rotations (the only other leaf)

**Target.** For the rotation `G(θ(x)) = cI + sJ` with `J = XZ`, `c = √p(x)`, and `s = √(1 − p(x))`:

**Construction.**
1. Compute `P(x)` with `b' = 2b` (F4).
2. Use integer square roots to get dyadic `c̄, s̄`, each accurate to within `2^{−b} + 2^{−b'/2}` of the true value.
3. Use a seed `y ∈ [0, 2^{b+2})`: `≈ 2^{b+1}c̄` labels apply `I`, `≈ 2^{b+1}s̄` labels apply `J`, and the remainder is split between `±I`.
4. All arithmetic uncomputes exactly, because `x` is unchanged.

**Error.** The clean block satisfies `‖B − G/2‖ ≤ 4·2^{−b}`. By Lemma 3, the half-block `η_rot`-implements the full unitary `G(θ(x))` on every target input, with `η_rot ≤ 5·2^{−b/2}`.

**Corner trees.**
- Use integer weights `W_s = round(2^{b'} p_s)` and exact ratios of their integer sums.
- There are `⌈log2 r⌉` levels, controlled on the prefix bits.
- Out-of-range prefixes get `p = 1`, which is the identity.
- The total error is `⌈log2 r⌉ η_rot + O(√(r 2^{−b'}))`, the latter being the Hellinger term.

**Cost.**
- Gates: `O(|C_p(2b)| + b^2)`.
- Workspace: seed (`b+2` qubits) plus arithmetic scratch.

The polar clock-prep and dilution rotations are fixed-angle instances of the same leaf.

---

## 7. Signal spaces and nesting ledger

| Leaf or composite | Signal projector `P` | Nested gadgets inside its `W` |
|---|---|---|
| Rotation gadget | seed (`b+2` qubits) | none (exact arithmetic) |
| Taylor segment | `z` and `s_1, …, s_K` | `U_L` only, an exact block encoding |
| `exp(itL)` | none (sequence of segments) | — |
| Content reflection | none (`y` is QPE workspace) | — |
| Proposal's polar `V` | its own selector/clock signals; disjoint from the pool `a` | treated by Lemma 1, not as nested blocks |

The total fresh pool for any single call is `O(D log(D+1) + Λ^2)` qubits, reused throughout.

---

## 8. Noncircular precision allocation

The allocation proceeds in four steps.

1. **Choose the polar defect.** Pick `δ` so that the ideal transform, with all leaves exact, has clean error `≤ ε/2`. This uses the external polar and stage proof. It fixes:
   - `K_pol = ⌈64N^2 ln(64N^2/δ)⌉`;
   - `m = 4(K_pol + 1)`.
2. **Count the calls.** These counts depend on `(D, δ)` only. Per stage, using the proposal's description:
   - `V` uses at most `2K_pol + 1` controlled W-type calls;
   - the amplification uses `2m + 1` `V`-type calls.
   With `S = O(D)` stages:
   - content reflections: `N_C ≤ S(2m+1)(2K_pol+1)`;
   - marker reflections: also `N_C`, all exact;
   - rotations: `N_rot` (polar prep and dilution, isometry trees, corner trees);
   - other controlled evolutions: `N_E`.
   The per-stage counts of rotations and other evolutions are themselves an external obligation.
3. **Set the per-subroutine tolerance.** Each subroutine instance gets `η = ε / (2(N_C + N_E + N_rot))`. By Lemma 1, the total error is at most `ε`.
4. **Derive the internal parameters.** `b, c, K, b'` follow from `η` by the formulas in §§4–6. They enter gate counts only. They never change any call count, and `R` does not depend on `η`. Hence the allocation is noncircular.

**Resulting bound.** If `δ = Θ(ε/D)`, which is external, then:
- `N_C = O(D^5 log^2(D/ε))`;
- `Λ = O(log(D/ε))`;
- total gates `O(N_C (D+1)^2 Λ (D log D + Λ^2) + N_rot (|C_p| + Λ^2))`, which is `poly(D, log 1/ε)`.

The final pool is left in place, unmeasured, and is within `ε` of `|0⟩`.

---

## 9. Remaining obligations and falsifiers

**Obligations.**
- F1–F4.
- The proposal's polar call counts and clean `O(δ)` error.
- The per-stage counts of rotations and other controlled evolutions.

**Exact falsifiers to check by brute force at small `d`:**
- a valid state where `τ` fails to be an involution, or where `N` differs between the two endpoints of a pair (this would make `L̃'` non-Hermitian);
- an eigenvalue outside `[−d, 3d]`, or a non-integer eigenvalue (this would cause aliasing in the content reflection);
- a controlled leaf whose off branch is not exactly the identity;
- a segment whose measured clean error exceeds `√(6ρ)`;
- any omitted controlled `−1` or `(iσ)^k`.

**Changes relative to the earlier report.**
- **§4.3 measurement and abort.** The end-of-gadget signal measurement and abort are removed. The cruder bound `‖POP − U‖ ≤ 15ρ` is replaced by `3ρ`, which yields `√(6ρ)`.
- **§5.2 signal-qubit rotations.** These are replaced by dyadic ±-label LCU, which removes a nesting level.
- **§5.4 inverse Fourier transform and flag measurement.** These are replaced by the shifted-Hamiltonian Hadamard reflection.

None of these changes implies a speedup, novelty, or hardness result.