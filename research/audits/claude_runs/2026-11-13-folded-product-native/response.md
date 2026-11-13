# Attack report: homogeneous folded-chain product quench, projected-Gaussian sampler, and coherent Pfaffian amplitudes

## 0. Verdict

I found no counterexample.

**Proved by the symbolic checks below.** These hold for all N, in exact arithmetic:

- Every label block has constant physical magnetization.
- The homogeneous-product state, conditioned on a label, is exactly |D_{ell,m}⟩. There are no residual signs or phases.
- The spectator-assisted Gaussian projects exactly onto |D_{ell,m}⟩.
- The acceptance bound 1/[ell(ell+1)] holds and is unchanged by evolution.
- The Majorana covariance formula and the prefix-Pfaffian probability formula are correct under the stated conventions.
- The coherent amplitude formula is an exact algebraic identity, valid for every matrix U, not only unitary ones.

**Not established here.** The fixed polynomial-bit clock for the sampler is the separate precision obligation. Under exact or real-RAM arithmetic, the sampler is polynomial. The bit-model claim stands or falls with that separate audit.

**Coherent formula.** It can retain all cross-fragment phases. This requires a fixed ordering convention, unnormalized Pfaffians, and a finitely specified φ. Below I also give a simplification (take z = 1) that removes the z-division and the m = ell exception.

**Necessary corrections (detailed in §4).** They concern convention traps and scope, not the core mathematics:

- The spectator ordering must agree between the Pfaffian and the Fock identification.
- The coherent formula must use unnormalized Gaussians.
- The input format for φ must be specified.
- The Majorana sign convention must be fixed.
- The spectator test is redundant.

Nothing here supports novelty, hardness or a speedup. If the sampler is completed, it removes a candidate full-output sampling advantage for this input family.

---

## 1. Native reduction: attacks and results

### 1a. Magnetization constancy (cheapest falsifier first)

Take the term (1+Z_jZ_{j+3})(X_{j+1}X_{j+2}+Y_{j+1}Y_{j+2}).

- It is nonzero only if s_{j+1} ≠ s_{j+2} and s_j = s_{j+3}.
- It flips s_{j+1} and s_{j+2}, exchanging 01 ↔ 10.
- So **every nonzero off-diagonal matrix element preserves physical Hamming weight M**.

In bonds, the condition is b_{j+1} = 1 and b_j ⊕ b_{j+1} ⊕ b_{j+2} = 0, i.e. the triple is 011 or 110. The flip exchanges b_j and b_{j+2}, so the move is exactly 011 ↔ 110, as stated.

The matrix element is −(1/8)·2·2 = −1/2, with no diagonal term.

### 1b. Connectivity

Within a label, the closed bijection identifies the block with all weight-m words q ∈ {0,1}^ell. Each adjacent q-transposition (A/C or A/B exchange) is one nonzero matrix element, as the closed proof states and as I re-traced for CA ↔ AC and BA ↔ AB.

Weight-m words are connected under adjacent transpositions (bubble sort). Hence M is a function of the label alone.

Even without connectivity, invariance plus the bijection would fail only if some block contained words not reachable by moves. That is excluded.

### 1c. Explicit check (N = 3, five spins, L = 4 bonds, s0 = 0)

| Label | Words | Physical strings | M |
|---|---|---|---|
| w = CC, d = 0, m = 1 (ell = 3) | ACC, CAC, CCA | 01000, 00100, 00010 | 1 |
| w = B, d = 0, m = 1 (ell = 2) | AB = 1110, BA = 1011 | 01011, 01101 | 3 |
| w = C, d = 1, m = 1 (ell = 2) | ACD = 1101, CAD = 0111 | 01001, 00101 | 2 |

For the AB ↔ BA pair, the move flips sites 2 and 3, and s1 = s4 = 1 as required. No falsifier appears.

### 1d. Conditional state

The product amplitude is c(x) = (√(1−p))^{N+2−M}(e^{iφ}√p)^M. This depends only on M, which is constant on the block. So the label-conditioned state is

  C(ell,m)^{−1/2} Σ_{|q|=m} |q⟩ = |D_{ell,m}⟩

exactly, up to the label's global factor.

- The label law is C(ell,m)|c_λ|². Sampling an IID Bernoulli(p) word and encoding it reproduces this law exactly. Rational p gives exact coins.
- The cases p ∈ {0,1} are trivial basis inputs.
- For a fixed physical y, ⟨y|e^{−itH}|ψ⟩ receives contributions only from y's own label, because the evolution is block diagonal. So the output Born law equals the label-dephased mixture.
- Dephasing is therefore legal for full computational-basis output. φ drops out because it enters only as a per-label global phase.

### 1e. Effective chain and Jordan–Wigner

H_ell = −(1/4)Σ(X_rX_{r+1} + Y_rY_{r+1}) is an open nearest-neighbour chain. Its Jordan–Wigner image has no string signs, and no constant or diagonal term.

So the fermionic image of |D_{ell,m}⟩ is Σ_{|T|=m} c†_{t1}⋯c†_{tm}|0⟩ in increasing order, with all signs +. Its time evolution is the Fock lift Γ(U) with vacuum phase 1, with no label-dependent phase.

---

## 2. Spectator Gaussian: attacks and results

### 2a. Pfaffian of J

The first-row expansion is Pf(J_{2k}) = Σ_{j=2}^{2k}(−1)^j Pf(J_{2k−2}). This is an alternating sum of 2k−1 terms starting with +1, so it equals 1. Pf(J_2) = 1, so the induction closes.

Principal submatrices of J are again J. Using the standard expansion exp(½c†Zc†)|0⟩ = Σ_T Pf(Z_T) c†_T|0⟩ (increasing order, Z_ij = z for i < j), the amplitude on every even T is z^{|T|/2}. This exponent is an integer, so it is rational for rational z. **Confirmed.**

### 2b. Projection onto the Dicke state

Put the spectator last (index ell+1), so in Jordan–Wigner order c†_S c†_{spec}|0⟩ = |S⟩⊗|1⟩ with sign +.

Conditioning on physical count m (spectator parity s = m mod 2) leaves z^{(m+s)/2} Σ_{|S|=m} |S⟩⊗|s⟩. After normalization this is exactly |D_{ell,m}⟩⊗|s⟩.

Small checks:

- ell = 2, m = 1, z = 1: the projection is (|10⟩+|01⟩)|1⟩.
- ell = 3, m = 2, z = 2: the coefficient on every pair is 2.
- ell = 4, m = 3: the coefficient on every {i,j,k,spec} is z²·Pf(J_4) = z².

**Confirmed.**

### 2c. z, q, and normalization

The weight is z^{|T|}, so the occupation law is Bernoulli(z/(1+z))^{⊗(ell+1)} conditioned on even parity. With z = m/(ell−m), this gives q = m/ell. **Confirmed.**

### 2d. Acceptance bound

Pr[accept] = q^s(1−q)^{1−s} · Pr[Bin(ell,q) = m] / Pr[even].

- Pr[even] ≤ 1.
- min(q, 1−q) ≥ 1/ell for 0 < m < ell.
- The mode of Bin(ell, m/ell) is ⌊(ell+1)m/ell⌋ = m, since m < ell. Its probability is at least 1/(ell+1).

Hence Pr[accept] ≥ 1/[ell(ell+1)] ≥ 1/[(N+1)(N+2)], using ell ≤ L = N+1 (all-C words).

Check at ell = 2, m = 1: the exact acceptance is 1/2 ≥ 1/6.

### 2e. Invariance under evolution

Γ(U') ⊗ I_spec commutes with physical number and with spectator number. With the spectator last, the physical hopping Jordan–Wigner strings do not touch it.

This holds for the exact U and also for any approximation U' that preserves particle number. So acceptance is invariant, and the accepted law is exactly the Born law of Γ(U')|D_{ell,m}⟩. **Confirmed.**

### 2f. Redundancy (minor correction)

The Gaussian is parity-even and the evolution preserves parity. So physical count = m already forces spectator = m mod 2. The spectator test is automatically satisfied in exact arithmetic.

Keep it only as a numerical sanity check. Do not count it as a separate acceptance factor.

### 2g. Pairing evolution

Use the convention Γ(U)c†_kΓ(U)† = Σ_i U_ik c†_i, with U = e^{−iht}. This matches the Slater convention ⟨i|U|k⟩ = U_ik.

Then Z' = Ũ Z Ũ^T with Ũ = diag(U,1). **Confirmed.**

### 2h. Field

- sin(πrk/(ell+1)) lies in Q(ζ_{2(ell+1)}, i) ⊆ Q(ζ_{4(ell+1)}).
- S² entries carry 2/(ell+1), so the √ cancels in U' = S diag(d) S, with S real symmetric orthogonal.
- d_j ∈ Q(i).
- Complex conjugation preserves the cyclotomic field, so Z'† and M stay inside it.
- The degree is φ(4(ell+1)) = O(ell).

Height bounds belong to the separate audit.

---

## 3. Covariance and prefix formula (convention check)

### 3a. Annihilators

Since a_i e^{½a†Za†}|0⟩ = (Za†)_i e^{…}|0⟩, the state is annihilated by b = a − Za†.

With c_o = a + a† and c_e = i(a − a†), we have a = (c_o − i c_e)/2 and a† = (c_o + i c_e)/2. This gives b = A c with A = ((I−Z), −i(I+Z))/2. **Confirmed.**

The CAR consistency check AA^T = ¼[(I−Z²) − (I−Z²)] = 0 holds. AA† = (I + ZZ†)/2 ≥ I/2, so the inverse always exists. No conditioning promise is needed at this step.

### 3b. Covariance

Define G = ⟨cc^T⟩ = I − iM, with M = (i/2)⟨[c,c]⟩ real antisymmetric and M² = −I.

- ⟨ψ|b†_i = 0 gives Ā G = 0, so G/2 = I − P, where P = A^T(ĀA^T)^{−1}Ā.
- Since conj(P) = A†(AA†)^{−1}A = I − P = (I − iM)/2, we get −i(I − 2A†(AA†)^{−1}A) = M. **The stated formula is correct.**

Vacuum check (Z = 0, one mode): A = (½, −i/2) gives M = [[0,1],[−1,0]], so M_{2j−1,2j} = +1 as claimed.

### 3c. Prefix formula

From the Majorana definitions, i c_{2j−1}c_{2j} = 1 − 2n_j. The projector onto outcome s_j is therefore (1 + s_j·i c_{2j−1}c_{2j})/2.

Expanding and applying Wick (off-diagonal G = −iM, so i^r Pf(−iM_T) = Pf(M_T)):

  Pr = 2^{−k} Σ_{T⊆[k]} Π_{j∈T} s_j Pf(M_T).

The block-diagonal minor expansion Pf(M + ⊕_j s_j J2) = Σ_T Pf(M_T) Π_{j∉T} s_j has all signs + for interleaved 2×2 blocks. I checked k = 1 and k = 2 explicitly. Multiplying by Π s_j gives the stated formula. **Confirmed** under:

- interleaved ordering, and
- the stated Majorana convention.

**Convention trap.** Bravyi's text conventionally uses a c_{2j} differing in sign; the excerpt supplied does not show it, so this is not taken from the excerpt. If that convention is mixed with the stated A-formula, the vacuum gives M_{2j−1,2j} = −1. Then M → −M, and Pf(−M + ⊕sJ2) = (−1)^k Pf(M − ⊕sJ2). The formula would return the probability of the *complemented* occupation string.

Cheapest guard: at k = 1 on the vacuum, s(1+s)/2 must give 1 for "empty" and 0 for "occupied".

The direct prefix formula also avoids Bravyi's M^{−1} and the ±1 ambiguity of squared traces (Eqs. 46–47). That is the right choice.

---

## 4. Coherent output-amplitude formula

### 4a. Independent proof

For an antisymmetric n×n matrix A and a 2r×n matrix B, the minor-summation identity is

  Pf(BAB^T) = Σ_{|I|=2r} det(B_{:,I}) Pf(A_I).

This is standard, and it also follows from the Fock argument in §2b itself.

Apply it with A = zJ and R = S ∪ {spec}^s. Take B = rows R of Ũ, so that Z'_R = BAB^T.

- Ũ's spectator row is e_{ell+1}, and its physical rows vanish in the spectator column.
- So I contributes only if I = T ∪ {spec}^s with |T| = m.
- In that case det(B_{:,I}) = det(U_{S,T}) (block-diagonal, spectator last in both rows and columns).
- Pf(zJ_I) = z^{(m+s)/2}.

Therefore

  Pf(Z'_{S∪spec^s}) = z^{(m+s)/2} Σ_{|T|=m} det U_{S,T},

for **every** matrix U and every z ≠ 0. Since Σ_T det U_{S,T} = Σ_{x∈λ} ⟨S|Γ(U)|x⟩, the effective amplitude is

  ψ(y) = c_λ · Σ_T det U_{S,T} = c_λ · z^{−(m+s)/2} Pf(Z'_{S∪spec^s}).

**The formula is correct**, including for the exact cyclotomic U'. It needs no sampling and no label dephasing.

### 4b. Correction: take z = 1 for amplitudes

The formula holds for any z ≠ 0; z = m/(ell−m) only matters for sampler acceptance. With z = 1:

- ψ(y) = c_λ Pf((ŨJŨ^T)_{S∪spec^s}), with no division;
- the case m = 0 gives the empty Pfaffian, equal to 1;
- the case m = ell gives det U', with no z = ∞ exception.

This applies to the coherent formula only.

At m = ell, det U' = Π d_j, which approximates the exact value e^{it·Σcos} = 1. This must be charged in the same η ledger, not set to 1 by hand in some labels and computed in others.

### 4c. Cross-fragment phases: can they be retained?

Yes. The sources of relative phase and magnitude between labels λ ≠ λ' are:

1. c_λ/c_λ' = (e^{iφ}√(p/(1−p)))^{M−M'}. This is kept explicitly.
2. Evolution-induced label phases. There are none: H_N has zero diagonal, H_ell has no constant, and Γ(U') has vacuum phase 1. The determinant/Pfaffian formula builds this in automatically, unlike an uncorrected per-length Rz synthesis.
3. Normalization. The formula uses **unnormalized** Gaussians.

Combined with the dephased sampler, which supplies exactly the Born law Van den Nest's estimator needs, this gives the "computationally tractable state" pair: sampling plus amplitudes. That covers additive estimation of efficiently computable sparse bounded observables, for example X_j or Pauli strings. For X_j, the estimator must re-encode y' = f(y) to obtain its label.

### 4d. Conditions and traps the coherent claim must state

1. **Fixed ordering.** The spectator must sit in the same position in the Pfaffian index order and in the Fock/qubit identification. Mixing them (e.g. spectator first in the Pfaffian, last in c†_S c†_spec) multiplies every odd-m label by (−1)^m = −1.
   - This is a **label-dependent sign that the Born sampler and any diagonal test cannot detect**.
   - It corrupts ⟨X_j⟩-type estimates between labels of opposite m-parity.
2. **No per-label normalization.** Using the normalized |G_z⟩ inserts N_z(ell,m)^{−1/2}. With label-dependent z this distorts cross-label magnitudes.
3. **φ must be an input.** The current contract states only rational p, and says φ is irrelevant (true only for the Born law). Coherent amplitudes need e^{iφ} as a specified finite object, e.g. a binary rational or an exact unit-circle point, with its bits charged.
4. **Irrational, possibly exponentially small c_λ.** √p and √(1−p) are generally irrational, and |c_λ| can be 2^{−Θ(N)}. The guarantee is exponentially fine *additive* accuracy, not relative accuracy. The observable estimate costs poly(1/ε) samples, not polylog(1/ε).
5. **Consistent error ledger.** Sampler and amplitude oracle must each be within their stated error of the ideal state. Pfaffian zero tests in the field are exact, but the c_λ prefactor is not algebraic over that field. The precision proof (separate) must cover it.

Scope of 4c: additive-error sparse-observable estimation for this exact family. It does not cover relative-error readout, dense or non-sparse observables, unknown quantum input, inhomogeneous products, or perturbed Hamiltonians.

---

## 5. Status ledger

| Item | Status |
|---|---|
| Moves preserve M; label blocks connected; M constant per label | Proved (§1a–b) |
| Conditional state exactly \|D_{ell,m}⟩; dephasing legal for basis output | Proved (§1d) |
| Pf(J_{2k}) = 1; amplitudes z^{\|T\|/2}; spectator-last sign + | Proved (§2a–b) |
| q = m/ell; acceptance ≥ 1/[ell(ell+1)]; invariant under number-preserving U' | Proved (§2c–e) |
| Spectator test redundant given parity | Proved (§2f) |
| A, AA† ≥ I/2, M formula, vacuum +1, prefix Pfaffian formula | Proved under stated convention (§3) |
| Coherent amplitude identity, any U, any z ≠ 0 | Proved (§4a) |
| Real-RAM polynomial sampler: O(ell²) expected attempts × O(ell) prefixes × poly Pfaffians | Follows from the above |
| Fixed polynomial-bit clock, heights, zero/tiny prefixes, capped coins, TV allocation | **Open; separate audit** |
| Coherent observable estimation with paid precision | Conditional on §4d items and the precision audit |
| Finite controls (N = 3 table, small ell) | Only falsification attempts; not proof |

---

## 6. Necessary corrections (summary)

1. Fix one Majorana convention: c_{2j−1} = a+a†, c_{2j} = i(a−a†), M = (i/2)⟨[c,c]⟩, interleaved order. State the k = 1 vacuum check. Do not import Bravyi's formulas without re-signing them.
2. Fix the spectator as the last index everywhere: in Z, in the Pfaffian rows, and in the Jordan–Wigner/Fock identification.
3. Declare the spectator test redundant, or keep it only as a numerical guard. The acceptance factor is Pr[count = m].
4. For the coherent formula, use the unnormalized Pfaffian with z = 1. Treat m = ell via det U' inside the same error budget.
5. Add an e^{iφ} input format and its bit cost to any coherent-amplitude or observable claim. Keep the statement that φ is irrelevant only for the Born-law sampler.
6. In the sampler's error budget, the conditional TV error after rejection scales like (proposal TV)/Pr[accept] ≤ ell(ell+1)·δ, up to a constant. So choose δ ≤ ε/(c·N²), and separately bound the cap-failure probability: (1 − 1/[ell(ell+1)] + δ)^K.
7. Keep the scope wording: homogeneous (identical p and φ on all N+2 sites), the exact H_N, open boundaries, binary rational t. A site-dependent product breaks §1d immediately, because amplitudes then depend on more than M.

---

## 7. Cheapest symbolic falsifiers (each would kill a specific claim)

1. **Reduction.** For N = 3, enumerate one label per (w, d, m) class and check the physical weight M on the block (§1c pattern). Any variation kills §1d.
2. **Pfaffian identity.** For a symbolic generic 3×3 (or 4×4) matrix U, with ell = 3 (or 4) and m = 1, 2, 3, compare Pf((ŨJŨ^T)_{S∪spec^s}) with Σ_T det U_{S,T}. Any mismatch, including a sign on odd m, kills §4a. The ell = 2, m = 1 case already reduces to U_i1 + U_i2 on both sides.
3. **Convention.** One mode, vacuum, k = 1: the formula must return Pr(empty) = 1. One mode, Z = 0, after a(t) = e^{−iθ}a: M must be unchanged.
4. **Cross-fragment coherence.** For N = 2 or 3, compare the dense exact ⟨ψ(t)|X_j|ψ(t)⟩ for a homogeneous product (symbolic p, φ; small rational t; exact evolution in a finite field extension, or interval arithmetic) against the label-wise Pfaffian amplitude assembly.
   - This is the only finite check sensitive to the §4d(1)–(2) traps.
   - Born-law comparisons cannot detect them.
5. **Acceptance.** Exact Pr[count = m] for ell ≤ 4 against the bound 1/[ell(ell+1)].

Passing these only fails to falsify. The all-N claims rest on the symbolic proofs in §§1–4.

---

## 8. Remaining proof obligation (not attempted here)

State the finite-bit sampler theorem, with the following conditions charged:

- uniform polynomial heights for M and for prefix Pfaffians in Q(ζ_{4(ell+1)});
- exact zero tests, and handling of tiny prefixes without a covariance-conditioning promise;
- rational ratio coins with capped bit budgets;
- the δ/acceptance allocation in correction 6;
- the label-sampling coins.

Its conclusion must be TV ε in poly(N, bits(p), bits(t), log 1/ε) time.

Falsifier for that obligation: a family of (ell, m, t) where some nonzero conditional prefix ratio requires super-polynomially many bits to separate from zero, or to round within the allotted share.