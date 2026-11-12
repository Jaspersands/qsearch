# Review: encoded qubits and cross-Kerr entangler in the native S/N model

## Verdict

- **Commutator identity:** correct.
- **Guarded CZ:** correct, and I found no counterexample to it. With the guards in place, the CZ is exact within an invariant two-level sector, with no leakage beyond the ancilla and no energy growth.
- **Group commutator:** not needed. A single 2π pulse gives an exact CZ.
- **The assumed compiler:** it is provable by an elementary first-order product formula, given one correction to how the averaging is weighted.
- **Where the parent fails:** several statements are false as written (uniform averaging, normalization), and two guards are genuinely necessary. Below I give exact counterexamples showing that dropping either guard causes order-one leakage.
- **One external input remains:** an explicit prime-density bound, which must be cited.

Everything below is my own hand derivation. I could not run code or check it mechanically. Please verify the 3-mode algebra and the two counterexamples symbolically before relying on them.

## 1. Commutator algebra (cheapest attack)

Let C = a_a† a_b† a_c with a, b, c pairwise distinct. Because different modes commute:

- C C† = n_a n_b (n_c + 1)
- C† C = (n_a + 1)(n_b + 1) n_c

Subtracting gives **[C, C†] = n_a n_b − n_c (n_a + n_b + 1)**, with the sign as stated. This requires a ≠ b, which holds because the p_i are distinct primes.

For the quadratures X = C + C† and Y = i(C† − C), we get [X, Y] = 2i[C, C†].

## 2. Exact invariant sectors (leakage and energy)

C conserves two quantities: K1 = n_a + n_c and K2 = n_b + n_c. Code states have n_a, n_b ∈ {0,1} and n_c = 0.

- **Sectors (0,0), (1,0), (0,1):** these each contain a single state, and C and C† vanish on it. So X and Y act as 0.
- **Sector (1,1):** this contains only {|110⟩, |001⟩}. Here C = |110⟩⟨001| with matrix element exactly 1. So X = σ_x, Y = σ_y, and [C, C†] = σ_z.

Every word in X and Y therefore acts as the identity on three code states and as an SU(2) element on the pair. No other states are reachable, so there is no energy growth.

In addition, the whole Hilbert space is the momentum-D sector:
- N ≤ D².
- Directly from the definition of S, each term satisfies sqrt(ij(i+j))·sqrt((n_i+1)(n_j+1)n_{i+j}) ≤ 2D^{3/2}. Hence ||S|| ≤ 4D^{7/2}.

This bound does not depend on the Schur-spectrum claim, which is not in the excerpt and is not used anywhere here.

**Exact CZ.** Apply e^{−iπσ_x} = −I on the (1,1) sector. This multiplies |11⟩_L by −1 and leaves the other three code states unchanged, which is exactly CZ on any superposition.

A controlled phase of angle α can be built exactly as e^{−i(π/4)σ_y} e^{iασ_x} e^{i(π/4)σ_y}. The resulting phase on the unoccupied state |001⟩ is irrelevant.

The parent's group-commutator route also works with polynomially many steps (O(s³) error per step), but it adds avoidable error.

## 3. Compiler: correcting the averaging step (cheap counterexample)

Under conjugation, e^{iθN} C_ij e^{−iθN} = e^{−2iijθ} C_ij.

**Counterexample to step 1 as written.** The uniform average (1/M) Σ_k U_k† S U_k is exactly 0. Every term of S has a nonzero frequency, so nothing survives. Plain averaging isolates nothing; the weights must be signed and modulated.

**Fix.** Take M to be a power of 2 with M > D², angles θ_k = 2πk/M, and weights w_k = cos(2Pθ_k)/M.

- Σ_k w_k e^{−2iijθ_k} = ½ δ_{ij,P}. This holds because 2|P − ij| < M and 0 < 2(P + ij) ≤ D² < M.
- Two ordered pairs (p,q) and (q,p) contribute. Their factor 2 cancels the ½.
- Result: H_eff = sqrt(P(p+q)) · X. Using sin weights instead gives sqrt(P(p+q)) · Y.
- Equivalently, Y can be obtained by conjugating with an N pulse at θ = π/4, which is dyadic. This gives (−i)^P C, so the result is ±Y depending on P mod 4.

**Implementation.** Use a first-order product formula over the M conjugated pulses, with negative times for negative weights. Adjacent N pulses merge, and the net N rotation is exactly the identity.

**Error.** Per slice, the error is at most δ²||S||². Over K slices, the total is at most τ²||S||²/K. This uses Σ|w_k| ≤ 1 and the standard commutator bound for first-order product formulas.

**Precision.** Pulse times must be rounded to binary rationals. Each rounding costs ||S|| · 2^{−b′}.

**Counts.**
- Each encoded gate needs constant total time τ = O(1).
- Pulses: O(M · K · G) with K = O(τ² D⁷ G/ε).
- Bits per time: b′ = O(log(D G/ε)).

These are polynomial for inverse-polynomial ε. Note that TV error 2^{−b} costs poly(2^b) pulses, so b must be O(log n). The BQP reduction only needs constant ε.

## 4. Guards: two exact counterexamples showing necessity

**Alias guard (P > D needed).** Assign qubits 1, 2, 3 the prime pairs (3, 11), (7, 13), (5, 17).

- Then c = 14, 20, 22 and D = 56.
- The cross gate for qubits 1 and 2 uses P = 21, with ancilla 10 (unoccupied).
- The factorization 1·21 survives, because 1 + 21 = 22 ≤ D. So H_eff gains the term sqrt(462)(a_1† a_21† a_22 + h.c.).
- Mode 22 = c_3 is occupied when qubit 3 is |0⟩.
- During the CZ pulse t = π/sqrt(210), that component rotates by π·sqrt(2.2) ≈ 1.483π.
- Resulting leakage probability: sin²(1.483π) ≈ 0.997.

**Ancilla-collision guard (Sidon or a weaker condition needed).** Assign qubits 1, 2, 3 the prime pairs (3, 7), (13, 17), (5, 11).

- Then c = 10, 30, 16 and D = 56. The cross ancilla is r = 16 = c_3.
- The alias 1·39 is harmless here, because mode 40 is empty.
- Take qubit 1 = |1⟩, qubit 2 = |0⟩, qubit 3 = |0⟩. On the cross modes this is the state |1,0,1⟩. Here C|101⟩ = √2 |210⟩.
- The 2π pulse therefore rotates by √2·π.
- Resulting leakage probability: sin²(√2π) ≈ 0.93.

**Sufficient conditions.** In fact you only need:
- the c_k are distinct, and
- no p_i + p_j equals any c_k.

Parity already separates even sums from odd primes. Shared cross ancillas (r_ij = r_kl) are harmless as long as each one is returned before the next gate.

**Greedy construction.** Choose 2n primes forming a Sidon set in [R, 2R]. Each new prime must avoid at most (2n)³ + 2n forbidden values, so it suffices that the number of primes in [R, 2R] exceeds 8n³ + 2n. A sieve over [R, 2R] runs in polynomial time.

**Proof obligation:** cite an explicit lower bound on primes in [R, 2R], for example a Chebyshev/Rosser–Schoenfeld-type bound. With such a bound, R = Θ(n³ log n) works. This gives R > 4n, hence P ≥ R² > 4nR ≥ D, and D = O(n⁴ log n).

## 5. Error budget and decoding

- **Per-gate error:** the operator-norm errors over the full D-sector add up to ε_tot ≤ Σ_g ε_g.
- **Total variation:** TV ≤ ||ψ − ψ′|| ≤ ε_tot.
- **Bad-code probability:** at most ε_tot². This is because the ideal state has zero bad-code amplitude.
- **Decoding:** for each qubit i, (n_{c_i}, n_{p_i}, n_{q_i}) must equal (1,0,0) or (0,1,1), and every other mode must be 0. Anything else is flagged as bad.
- **Initial state:** the occupation μ with parts c_1, …, c_n. These are distinct.

## 6. Classical-simulation attacks

**Bosonic Gaussian simulation** does not apply, because S is cubic in the bosonic modes.

**Free-fermion simulation** does not apply, for three reasons. Under the boson–fermion correspondence (a standard fact, not in the excerpt):
- S becomes a fermion bilinear,
- but N = Σ k² a_k† a_k becomes quartic in fermions, and
- the input |μ⟩ and the occupation readout are not Gaussian in the fermionic picture.

Separately, the contract's claim that "S alone is easy" from |μ⟩ is unverified. Its amplitudes are character sums. It is not needed for this argument.

**Small classical representations:** none exist in the naive sense. The code space is 2^n-dimensional and is acted on by CZ together with arbitrary single-qubit SU(2).

**Consequence.** Assuming the prime bound in section 4 and the compiler of section 3, a classical polynomial-time sampler achieving constant TV error would place BQP in BPP.
- This is conditional hardness only.
- It is not an unconditional result and not a speedup claim.
- The argument is an explicit construction, not an appeal to Lie-algebra rank or finite simulations.

## 7. Remaining proof obligations and falsifiers

1. **Prime density.** Supply an explicit citation for the bound used in section 4.
2. **Symbolic checks.** Verify the cos/sin weight identity and the commutator bound for the product formula.
3. **Normalization.** The excerpt's T3 matches S at ε = 0 under the identification V_k = √(ℏk) a_k†, up to an overall ℏ^{3/2}. That identification is my assumption, not something in the excerpt. It does not affect the construction, which uses S exactly as defined in the contract.
4. **Time format.** Confirm whether "binary rational" means dyadic. M is chosen as a power of 2, so dyadic times are already accommodated.
5. **Falsifier.** The construction is refuted by any surviving factorization ij = P with i + j ≤ D whose modes intersect the occupied set, or by any r_ij ∈ {c_k}. The guards in section 4 exclude both.