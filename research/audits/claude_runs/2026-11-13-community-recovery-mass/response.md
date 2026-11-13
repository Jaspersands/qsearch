# Audit: all-label high-energy ⇒ one-particle planted-span operation (contract.md)

## Verdict

I found no counterexample to the set-space operation on the native multi-community mean. The candidate constants check out, except for one claim that is not established.

- **Set-space chain (proved below):** a set Rayleigh quotient of at least cεD/2 forces one-body mass on L of at least 1/(16k^(p+1)). This holds for:
  - arbitrary complex states,
  - mixed states,
  - states that depend on the graph,
  - unbalanced labels.

  The only randomness needed is the noise event (5).
- **λ_min(A) ≥ −cεD/4 is a consequence, not an extra assumption.** It follows from the same three conditions. Plain integer powers then give a checkable vector with t=O(ell·log n), not O(log n).
- **Not established:** "ordered noise d!·T". It holds on the symmetric collision-free subspace Ran W. As a norm bound on the whole ordered space, neither the supplied premises nor this audit prove it. The non-symmetric isotypic blocks are unbounded here.

  Consequence: the classical endpoint should work in SET space and use the deletion isometry. Any ordered quantum route must either prove its states lie in Ran W, or prove its own ordered trace bound. Its acceptance threshold must also be d!·cεD/2, not cεD/2. A d!-mismatched threshold makes the bound vacuous.
- **Balance:** IID balance enters only at the frame/rounding step, never at the energy step.

## Cheapest attacks tried, all failed

1. **Factorial direction.** If W*K_xW equalled M_x instead of d!M_x, or if D ≈ Λ instead of Λ/d!, the chain would lose a factor d!. Recounting below confirms that both factors are d! and cancel: d!D/Λ → 1.
2. **Collision remainder.** The bound row-sum ≤ binom(ell,d)·d²·n^(d−1)·(per-entry bound) is correct. The per-entry bound is actually ≤ Σ_a|w_a(v)| = 2(k−1)/k < 2, so k is a valid but loose constant.
3. **Products of projections.** For commuting projections, Q_1⋯Q_d ≤ Q_j for each j, so the product is ≤ (1/d)ΣQ_j. This is exact.
4. **Vacuous mass via the all-ones direction.** This is possible only under heavy imbalance. It is a frame-step issue (see the section on balance), not an energy-step issue.
5. **Negative spectrum spoiling power iteration.** This is excluded: λ_min(M_x) ≥ −r/d! (see the spectral section).

## Scope, access and resources (classical endpoint)

**Input.** The complete binom(n,p) array Y. A rank/unrank index E↦position costs poly(p log n) per lookup. Nothing else is used: no labels, projector, gauge, second instance or oracle.

**Matrix.** A(S,T) = Y_E − q for |S|=|T|=ell, |S∩T|=ell−d, E=SΔT. N=binom(n,ell), and each row has D nonzeros. With q=1/4, 4A has integer entries in {−1,3}. Write ε=a/b in lowest terms.

**Arithmetic.**
- The entries of (4A)^t g satisfy |·| ≤ (3D)^t, so each needs ≤ t·log2(3D)+1 = O(ell log² n) bits.
- One matvec costs N·D·poly(ell log n).

**Procedure POWER** (all integer, exact):
1. Set t=⌈4 ln(8N)⌉ = Θ(ell log n) and R=⌈24 ln n⌉.
2. For r=1..R:
   - draw g∈{±1}^N;
   - compute v=(4A)^t g;
   - ACCEPT v iff b·k^p·⟨v,(4A)v⟩ ≥ a·D·‖v‖².

   This test is exactly Rayleigh(A) ≥ cεD/2 with c=1/(2k^p).
3. Output the first accepted v, else FAIL.

**Costs.**
- Time is R(t+1)·N·D·poly(ell log n) = n^(ell+d)·polylog(n).
- Space is O(N·ell log² n) bits.
- Randomness is R·N bits.

**One-particle state** (exact rational, no normalization needed). Accumulate:
- Off-diagonal: for every S, i∈S, j∉S, add ρ_ij += v_S·conj(v_{S−i+j}).
- Diagonal: ρ_ii = Σ_{S∋i}|v_S|².
- Divide all entries by ell‖v‖².

This costs N·ell·n big-integer products, i.e. n^(ell+1)·polylog(n). Trace = 1 exactly.

Total: n^(ell+O_p(1))·poly(input bits), as the contract targets. Eigen-decomposition and rounding precision are not charged here; that is a later obligation.

## Imported hypotheses (not reproved)

- **(I1) Trace bound.** From the checked premises, eq. (5): for SET Kikuchi matrices with independent fair signs on any support, Pr(‖·‖ > C√(D·ell)) ≤ 2n^(−2ell), with C=2^300. It needs the explicit large-n scalar conditions that depend on d.
- **Uniformity over supports.** Expanding E Tr(Σ s_E A_E)^(2t) gives a sum of traces of products of nonnegative matrices. Shrinking the support therefore only lowers the moment. I checked this sign structure.
- **(I2) Symmetrization (6).** Tr(X^(2t)) is convex on Hermitian X and E[Y'] = θ, so Jensen gives the bound for H = Σ(Y_E−θ_E)A_E. This holds for every fixed x, every θ_E∈[0,1], and every ε, with no balance needed.
- **Event E_H:** ‖H‖ ≤ T := C√(D·ell), probability ≥ 1−2n^(−2ell) for each x. Since A = εM_x + H exactly, where M_x(S,T) = f_x(SΔT), nothing else about the noise is used.

## Proof of the mass bound (all labels, set space)

**Notation.**
- w_a(i) = 1[x_i=a] − 1/k, W_a = w_a w_aᵀ, and L = span{w_a}.
- Λ = binom(ell,d)·n^d and r = k·d²·binom(ell,d)·n^(d−1) = k d² Λ/n.
- K_x is the ordered native matrix. Π is the collision-free projection.
- W is the set→ordered isometry: W|S⟩ = (ell!)^(−1/2) Σ_orderings |ordered S⟩.

**L1 (operator inequality, deterministic, every x).**
1. ‖w_a‖² ≤ n because |w_a(i)| ≤ 1. Hence W_a ≤ n·P_{w_a} ≤ n·P_L.
2. Each slot j lies in binom(ell−1,d−1) = (d/ell)·binom(ell,d) of the sets J.
3. Combining with attack 3: B := Σ_J Σ_a ⊗_{j∈J} W_a^(j) ≤ (kΛ/ell)·Σ_j P_L^(j).

For any density σ on the ordered space, ⟨B⟩_σ ≤ kΛ·Tr(P_L ρ̄_σ), where ρ̄ is the slot-averaged one-particle state. All operators are real symmetric, so this holds for complex σ.

**L2 (collision remainder, deterministic).** ‖ΠBΠ − K_x‖ ≤ r. This is eq. (8), re-derived:
- Entries with exactly d changed slots and 2d distinct changed vertices have J = (changed set) as the unique contributor, so they agree exactly.
- Every other entry has, for some J, a new vertex equal to an old J-vertex. There are ≤ d²·n^(d−1) such τ_J per (σ,J).
- The Schur row-sum test finishes the bound.

**L3 (exact set↔ordered identity).** W*K_xW = d!·M_x.
- Fix S, T with |SΔT| = 2d and an ordering σ of S.
- A τ with K_x(σ,τ) ≠ 0 must keep the ell−d common vertices in place. A moved common vertex would repeat among the changed labels.
- τ then places T\S into the d vacated slots in exactly d! ways.
- So the sum is ell!·d!·f_x(E), and dividing by ell! gives d!·f_x(E).
- K_x commutes with slot permutations, so K_x restricted to Ran W equals W(d!M_x)W*. The same holds for the noise part.

**Theorem (mass).**

Assume:
- E_H holds;
- (H1) T ≤ cεD/8;
- (H2) r/d! ≤ cD/8;
- (H3) d!D/Λ ≥ 1/2.

Then every density σ on the ell-set space, pure or mixed, complex, possibly depending on Y, with Tr(Aσ) ≥ cεD/2 satisfies Tr(P_L ρ_σ) ≥ 1/(16k^(p+1)). Here ρ_σ is the deletion-isometry one-particle state.

Proof. Let φ = WσW*, which is collision-free, so ⟨B⟩_φ = ⟨ΠBΠ⟩_φ. Then:
1. Tr(M_xσ) ≥ (Tr(Aσ) − T)/ε ≥ 3cD/8, by (H1).
2. Tr(K_xφ) = d!·Tr(M_xσ) ≥ 3d!cD/8, by L3.
3. ⟨B⟩_φ ≥ 3d!cD/8 − r ≥ d!cD/4 ≥ cΛ/8, by L2, (H2) and (H3).
4. L1 then gives Tr(P_L ρ̄_φ) ≥ c/(8k) = 1/(16k^(p+1)).

Every step is linear in σ. ρ̄_φ equals the contract's set formula; recomputed, each slot gives (ell−1)!/ell! = 1/ell. Real parts are harmless because Tr(P_L ρᵀ) = Tr(P_L ρ). ∎

**Explicit finite-n sufficient conditions.**
- (H1) ⟺ ε²D ≥ 256·k^(2p)·C²·ell. This is a known constant multiple of the frontier and must survive the (1−2t) attenuation.
- (H3) holds if n ≥ 2d(ell+d), since d!·binom(n−ell,d) ≥ (n−ell−d)^d.
- (H2) holds if n ≥ 32·k^(p+1)·d² and ell+d ≤ n/(2d). The second gives (n−ell−d)^d ≥ n^d/2.

## Spectral side and power iteration (proved, given E_H and H1–H3)

**Top eigenvalue.** By witness (11): (9)'s bracket is ≥ k^(−2d)/2 if n ≥ 64·k^(4d+4)·ell² and n ≥ 4d²·k^(2d+1). I re-derived (9):
- ‖v−v0‖² ≤ 2(1−‖Πv0‖²) ≤ ell²k²/n;
- ‖B‖ ≤ kΛ, so the perturbation is ≤ 2kΛ·‖v−v0‖;
- D ≤ Λ/d!.

Hence λ_1(A) ≥ cεD − T ≥ (7/8)cεD.

**Bottom eigenvalue.** For any unit u:
- ⟨u,M_xu⟩ = ⟨Wu,K_xWu⟩/d! ≥ (⟨Wu,BWu⟩ − r)/d! ≥ −r/d!, because B ⪰ 0.
- So λ_min(A) ≥ −εr/d! − T ≥ −cεD/4.

The negative side is thus bounded by the planted PSD structure, with no shift and no gap.

**Power bound.**
1. For v = A^t g, Rayleigh(v) = Σλ_i·π_i with π_i ∝ λ_i^(2t)·g_i². The parity of t is irrelevant.
2. Split the spectrum at 3cεD/4. The bad part has |λ| ≤ 3cεD/4 and λ ≥ −cεD/4.
3. Hence Rayleigh ≥ cεD·(3/4 − π_bad).
4. π_bad ≤ (6/7)^(2t)·N/⟨u_1,g⟩², where u_1 is any real top unit eigenvector.
5. Paley–Zygmund with E⟨u,g⟩² = 1 and E⟨u,g⟩⁴ ≤ 3 gives Pr(⟨u_1,g⟩² ≥ 1/2) ≥ 1/12.
6. t ≥ ln(8N)/ln(49/36) gives π_bad ≤ 1/4, so Rayleigh ≥ cεD/2.

Result: a single start passes the exact test with probability ≥ 1/12, so FAIL has probability ≤ (11/12)^R ≤ n^(−2).

**Certificate logic.** Correctness does not depend on POWER having converged. On E_H, every accepted vector satisfies the mass theorem, even an adversarially chosen one. POWER only affects the probability of acceptance.

## Where IID balance is first needed

- **Not needed in L1–L3 or the theorem.** The witness also uses only ‖w_c‖² ≥ n/k², which is true for every x.
- **Frame step.** The nonzero spectrum of Σ_a W_a equals the Gram form Σ_a n_a·u_a² on 1^⊥. So P_L ≤ (1/min_a n_a)·Σ_a W_a. On the event n_a ≥ n/(2k), mass η gives max_a ⟨w_a,Rw_a⟩ ≥ η·n/(2k²). Without balance this factor degrades as min n_a shrinks.
- **Rounding baseline.** The term (1−n_a/n)/(k−1) uses balance.
- **Why balance matters here** (an example against "mass ⇒ informative direction", not against the operation). If all x_i = a, then L = span(1), and the uniform one-particle state has mass 1 while carrying no information. Near-imbalance makes L nearly contain 1. Balance must therefore be invoked before converting mass into correlation.

## Status ledger

| Claim | Status |
|---|---|
| L1, L3, the theorem, λ_min bound, power bound, exact test, costs | PROVED here |
| (5), (6), witness (9)–(11) | IMPORTED / re-derived; (9) re-derived above |
| Ordered noise d!·T beyond Ran W | OPEN |
| Frame/rounding, validation, clone χ², quantum composition | Not audited; contract marks them pending |

No speedup, novelty or hardness inference is made.

## Proof obligations and falsifiers remaining

- **O1.** For any ordered/quantum route: either show the accepted-band states lie in the symmetric collision-free subspace Ran W, or bound the ordered noise on every isotypic block by a separate trace argument. The acceptance threshold must be d!·cεD/2 on the ordered scale.
  - Falsifier: an ordered non-symmetric state whose noise Rayleigh exceeds d!·T.
- **O2.** Attenuation and cloning must keep (H1) for the matrix array. The effective ε_eff = ε·(1−2t), and ε_eff²D must stay above 256·k^(2p)·C²·ell.
- **O3.** Rounding must take as input the exact rational ρ above. The precision of the approximate eigen-decomposition must be charged without gap promises.
- **O4.** Union of events: E_H (≥ 1−2n^(−2ell)), POWER (≥ 1−n^(−2)), and the balance event are all needed before the frame step.
- **O5.** Report constants honestly. C_{p,k} ≥ 2^608·k^(2p) from C = 2^300. These are asymptotic statements only.

## Minimal next step

Write community-recovery-mass.md as exactly the theorem plus POWER above, set-space only. Then attack O1 only if the quantum route keeps ordered slots. Otherwise switch the quantum route to the set deletion isometry, which needs no new noise bound.