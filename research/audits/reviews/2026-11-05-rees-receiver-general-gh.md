# Rees HSP: the coherent witness circuit at every fixed κ, and the (G, H) the coherent generator covers

5 November 2026. This is an AI-only pass (Claude Code). **Status: AI-checked, pending human review.** Nothing here is Lean.
No paper, `theorems/` module, registry, `STATE.md` or handoff file was edited, and git was not used. The outputs are:
- this report;
- the folder `research/audits/reviews/2026-11-05-rees-receiver-general-gh/` (scripts, JSON and logs);
- `tests/test_rees_receiver_general_gh.py`.

Labels:
- **[proved]**: a written proof here, not machine-checked;
- **[finite computation]**: exhaustive over a stated finite set;
- **[sampled]**: exact on a stated subset;
- **[argued]**: reasoning that is not machine-checked and is not a complete proof.

Companion reports:
- `2026-11-05-rees-receiver-general-lemma.md` (the "receiver lemma": shape (S1)–(S6), hypotheses (KS), (INST), (D1), (D2a–c), (CLEAN), Theorem 2, Corollary 3, Proposition 4);
- `2026-11-05-rees-kappa2-circuit-proof.md` (the κ = 2 proof, whose Theorems A and B and Section 4 this report follows);
- `2026-11-04-rees-coherent-sde-k3.md` (the "κ report": the definition of the canonical witness at any κ, its Theorem 2, Lemma 1 and Lemma 4′);
- `2026-11-04-rees-coherent-sde.md` (κ = 1).

## 0. Verdict

**(A) [proved, given the macro contract (M) and the comparator contract (M′) of §1.2].** For every odd prime p, every d with κ = gcd(d, p−1) ≥ 2 and p ∉ E_2(κ), and every a ≥ 1, `CoherentSDEKappa(p, a, d)` writes its witness on every canonical input. It maps |λ⟩|0⟩_S|0⟩_work to |λ⟩|s(λ)⟩_S|0⟩_work, where s(λ) is that module's canonical witness, s(λ) ≠ 0 and Σ s_i^d λ_i = 0. The labels are only ever controls or operands, never targets.
- This covers the default `stop="power"` variant, the one the receiver builds.
- The written proof is general in κ, and κ = 3 is one instance of it.
- It holds for **every** valid normalised contraction, not only the lexicographically least one.
- This upgrades Theorem 6 of the κ report from "[argued] step-by-step correspondence" to a written proof. So (D2a) holds at every grade with κ_d ≥ 3 and p ∉ E_2(κ_d), given (M) and (M′).
- The controls run here all pass:
  - exhaustive at κ = 3 (p = 7, 13, 19, 37; u = 1, 3, 5) and κ = 4 (p = 41);
  - sampled up to a = 4 and at κ = 5 (p = 191) and κ = 6 (p = 229);
  - every alternative contraction at p = 7, 13 and six of the 42 at p = 19;
  - 5 of 5 mutants detected.
- No bug was found. The `stop="general"` variant is not covered (the receiver does not use it).

**(B) [proved, conditional as stated in Theorem B].** Let L be a Lie algebra over F_p of class c < p, G = (L, ∗) the Lazard group and H ≤ G any subgroup. Suppose every grade d of the Rees cover with κ_d = gcd(d, p−1) ≥ 3 has p ∉ E_2(κ_d). Then the generator TerminalSampleK(coherent_config_k(L)), which is `rees_circuit_coherent_k3` over the fourth backend, returns a program with these properties:
- it has the shape (S1)–(S6) and satisfies (KS), (INST), (D1), (D2) and (CLEAN);
- its readout law, conditioned on every label tuple of positive probability, is uniform on h^⊥;
- its X/CX/CCX/SWAP count is poly_c(log|G|, log p): O_c((n^{2c+1} + n^{2c−2}b²)·b²) with n ≤ cm and b = ⌈log₂ p⌉.

Otherwise the generator refuses with `ValueError`; it never returns a wrong circuit.

The conditions are:
- (M) for p > 127 (exhaustive here for 17 ≤ p ≤ 127, and in the repo for p ≤ 13);
- the paper's `lem:central`, `prop:descent` and `lem:homogeneous`;
- exact QFT_p calls;
- E_2(2) = E_2(3) = ∅ as stated in `prop:decoupled-sde` (AI-checked there), used only to say that c ≤ 3 is never refused.

Consequences:
- **Every class-two and class-three Lazard group, every H, every p > c** is covered.
- In class c ≥ 4 a grade is refused exactly when κ_d ≥ 4 and p ∈ E_2(κ_d), for example p ∈ {5, 13, 17, 29, 37, 53} at κ_4 = 4.

What Theorem B does not give:
- an implemented receiver with the arities, query count or error budget of `thm:main`: the coherent arities are larger;
- a polynomial-time *generator*: the classical canonical-contraction and coset-generator searches have no proved polynomial bound;
- explicit transforms beyond F_3 and F_5;
- anything at grades with p ∈ E_2(κ_d).

The claim gate `coherent_receiver_implemented` stays FALSE (§5).

**Strongest remaining gap.** Grades with κ_d ≥ 4 and p ∈ E_2(κ_d) have no coherent solver. They need a coherent Schedule-1 (Chevalley–Warning / `thm:is-import`) witness circuit, which exists only as the existence statement `prop:coherent-receiver`. Next in line is a proved polynomial bound for the classical constant search.

## 1. Setting

### 1.1 What was read

Code (read only):
- `theorems/rees_coherent_sde_kappa.py`: `CoherentSDEKappa._forward`, `_class_flags`, `_qroot_chain`, `_root_chain`, `_copy_stage`, `_less_into`, the constants (`coset_generator`, `bezout_exponent_kappa`, `root_params`, `canonical_contraction`, `_canonical_contraction_lazy`, `contraction_valid`) and the closed forms;
- `theorems/rees_coherent_sde_k2.py`: `_fd`, `_copy`, `_load_const`, `_eq_const_into`, `_pow_reg`, `first_dependency`;
- `theorems/rees_coherent_sde.py`: `Macro`, `Prog`, `_pow_copy`, `BitSim`;
- `theorems/rees_circuit_arith.py`: contract (A1)–(A4), `add_ext`, `sub_ext`;
- `theorems/rees_circuit_coherent.py`: `remap`, `flatten`, `targets`, `touched`, `MergeBlock`, `TerminalSample`, `prove_controlled_merge`, `block_structure`, `sde_exhaustive`, `block_sampled`;
- `theorems/rees_circuit_coherent_k3.py`: `sde_circuit_k`, `kappa_dispatch`, `coherent_config_k`, `MergeBlockK`, `TerminalSampleK`;
- `theorems/rees_circuit_general.py`: `bch_nodes`, `Config._grade_nodes`, `sym_bch_reference`;
- `theorems/rees_end_to_end_sim.py`.

Paper (read only), `docs/papers/rees-hsp/main.tex`:
- `thm:rees-cover`, `lem:homogeneous`, `lem:central`, `prop:descent`, `prop:decoupled-sde`, `prop:triangular-sde`;
- `lem:coherent-linear-sde`, `lem:coherent-quadratic-sde`, `lem:coherent-power-sde`, `prop:coherent-receiver`.

Also `appendix-backends.tex`, whose subsections `app:backends-coherent` and `app:backends-scope` now hold the "Coherent-label backends" and "Scope" text (it moved there from main.tex).

### 1.2 Contracts assumed

- **(M) Macro contract** (rees_circuit_arith (A1), (A4)).
  - Statement: on canonical words with the 3b+5 shared ancillas at 0, `add_product(t, a, b, κ)` is t ← t + κab mod p and `add_scaled(t, a, κ)` is t ← t + κa. Operand wires are never targets of a gate and the ancillas return to 0. This includes the aliased squaring `add_product(t, a, a, κ)`.
  - **[finite computation]** on all canonical words and **every** coefficient κ ∈ [1, p−1] for every prime 17 ≤ p ≤ 127. This pass ran `macro_check.py`: 25 primes, 75 rows, all four properties hold, 206 s. The repo had already checked p ≤ 13.
  - **[argued]** beyond (standard ripple-carry modular arithmetic).
- **(M′) Comparator** (`CoherentSDEKappa._less_into`).
  - Statement: f ^= [x < y] on b-bit words x, y, with both restored and the ancillas e, c0 returned to 0. It is built from `sub_ext` and `add_ext` of rees_circuit_arith.
  - **[finite computation]** for b = 2..8 on all 2^{2b} pairs (`kappa_trace_check.py`, `comparator`).
  - **[argued]** beyond: Cuccaro subtraction with borrow out, the borrow copied, then addition back.

## 2. (A) The witness circuit at every fixed κ ≥ 2

### 2.1 Statement

Fix an odd prime p, κ ≥ 2, d with gcd(d, p−1) = κ, a ≥ 1 and M = (a+1)(a+2)/2. Let P = (F_p^×)^κ, h = (p−1)/κ, b = ⌈log₂ p⌉. Let g be the least generator of F_p^×/P, ω = g^h, cos(y) = ν iff y ∈ g^ν P, and u ≥ 1 with u·d/κ ≡ 1 (mod h). Let (α, β) be any **normalised contraction**: α_0 = 1, β_0 = 0 and α_j + β_i ∈ g^{−(i+j)}P ∪ {0} for all i, j ∈ Z/κ. For such (α, β) let s^{α,β}(λ) be the witness of the κ report §1 (rounds, weights, back substitution, s_i = ρ(x_i)^u, ρ the least κ-th root), computed with (α, β) in place of the canonical contraction.

**Theorem A_κ [proved, given (M) and (M′)].** Let U = `CoherentSDEKappa(p, a, d, contraction=(α, β)).prog` (`stop="power"`). For every canonical λ ∈ (F_p^a)^M,

  U |λ⟩_L |0⟩_S |0⟩_work = |λ⟩_L |s^{α,β}(λ)⟩_S |0⟩_work,

with s^{α,β}(λ) ≠ 0, every entry canonical, and Σ_i s_i^d λ_i = 0. No flattened gate of U has a label wire L as target. The label wires enter only as CX controls of `_copy` and as macro operands.

Specialisations:
- With `contraction=None` the module uses the lexicographically least contraction (κ report Lemma 3). This is the only form `sde_circuit_k`, `MergeBlockK` and `TerminalSampleK` build.
- The module constructs the circuit iff such a contraction exists, i.e. iff p ∉ E_2(κ), and raises `ValueError` otherwise.
- For p > 2·10⁶ the lazy search raises `RuntimeError` if its α-scan cap is hit; it never returns a non-contraction, because `contraction_valid` is asserted on every contraction used.

### 2.2 Theorem A: the algorithm is correct for every normalised contraction [proved]

This is the κ report's Lemma 1, Theorem 2 and Lemma 4′, re-read here. Their proofs use the contraction **only** through the conditions α_0 = 1, β_0 = 0, α_j + β_i ∈ g^{−(i+j)}P ∪ {0}, and the consequence β_ν ≠ 0 for ν ≠ 0. That consequence is the j = 0 condition: 1 + β_ν ∈ g^{−ν}P ∪ {0} with 1 ∉ g^{−ν}P. Leastness is never used. So, for every normalised (α, β) and every λ:

- (i) The rounds stop at some K ≤ a. In round a the list v_1..v_a, λ_{B_a} has a+1 vectors of F_p^a with v_1..v_a independent, so v_{a+1} ∈ U_a = F_p^a.
- (ii) Every first dependency is that of the genuine list.
- (iii) Lemma 4′ holds: v_{k+1} ∈ U_k ⟺ every nonzero δ_i lies in P ⟺ v_{k+1} = 0. Its proof needs only that δ is a minimal dependency with δ_{j*−k} = 1, and β_0 = 0, β_ν ≠ 0.
- (iv) x ∈ (P ∪ {0})^M, x ≠ 0 (x_{i*} = 1) and Σ x_i λ_i = 0.
- (v) s_i = ρ(x_i)^u satisfies s_i^d = x_i, so s ≠ 0 and Σ s_i^d λ_i = 0.

At the stop round:
- τ_l = y^{(K)}_{l−1} for l ≤ K (y′ = (0, …, 0, 1));
- the round-K weights are x_i = δ_i (bd_i = β_{cos δ_i}δ_i = 0).

### 2.3 Theorem B: the gate list computes the algorithm [proved, given (M), (M′)]

**Induction hypothesis along F** (as in the κ = 2 report §3), on a canonical input:
- every b-wire register holds a canonical word;
- every flag wire is 0/1 with its stated meaning;
- the arithmetic ancillas and the ladder temporaries are 0 between macros and ladders;
- every register and bit in the pools `free`, `free_bits` is 0.

The building blocks preserve it, word for word as in the κ = 2 report §3:
- CX copies (`_copy`);
- XOR loads of constants under one-hot flags (`_load_const`);
- equality flags (`_eq_const_into`: X on the zero bits of the constant, AND ladder, X back);
- AND ladders (`_and_into`);
- square-and-multiply chains computed, used and reversed (`_pow_copy`, `_pow_reg`);
- the macros, by (M).

**C1 (first dependency).** `_fd` on n = a+1 columns of F_p^a (R = a rows) returns one-hot flags dep and Z = −FD(list) on every canonical list, genuine or not. This is the κ = 2 report's B1 verbatim: `CoherentSDEKappa` inherits `_fd` from `CoherentSDEK2` unchanged. The input columns are read only through `_copy` (CX controls) into fresh workspace columns W, and all row operations act on W.

**C2 (coset flags).** `_class_flags(F, y)` computes y^h by `_pow_copy` and tests it against ω^ν, ν = 1..κ−1. Since ω has order κ:
- y ≠ 0: y^h = ω^{cos y}, so exactly one flag is set iff cos y ≠ 0;
- y = 0: y^h = 0 ≠ ω^ν, so no flag is set.

The flags therefore set flag_ν = [cos y = ν] for ν ≠ 0, all 0 on P ∪ {0}, with y restored and the chain reversed.

**C3 (rounds, one-hot stop).** Claim: run_k = 1 and V holds the genuine v_1..v_k for k ≤ K; run_k = 0 for k > K; exactly one F_k is 1, at k = K. By induction on k with run_0 = 1 (X), in round k ≤ K:
- C1 gives the genuine Z^{(k)}. δ_i = −Z^{(k)}[k+i] = y^{(k)}_{k+i} (`add_scaled` −1 into a zero register).
- C2 gives the flags of δ_i. breg = Σ_ν flag_ν β_ν = β_{cos δ_i} (β_0 = 0; 0 when δ_i = 0), and bd_i = δ_i·breg.
- nq_i = ⊕_ν flag_ν = [δ_i ∉ P ∪ {0}] (the flags are one-hot).
- vnew[r] = Σ_i bd_i λ_i[r] = v_{k+1}[r].
- stop_k = AND_i ¬nq_i = [every nonzero δ_i ∈ P] = [v_{k+1} ∈ U_k] by Lemma 4′ (§2.2 (iii)).
- F_k = run_k ∧ stop_k (CCX into a fresh bit) and run_{k+1} = run_k ⊕ F_k (two CX into a fresh bit). So F_k = 1 iff k is the first stop round, and run_{k+1} = 1 iff no stop yet.
- If round k does not stop, v_{k+1} ∉ U_k, so V stays genuine and independent.

Rounds k > K run on whatever V holds: V contains v_{K+1} = 0 and then garbage. They are still canonical-word computations (C1 applies to any list), but every one of their registers enters later gates only under F_k = 0 or multiplied by a zero register (C4–C6). By §2.2 (i), K ≤ a.

**C4 (τ).** τ_l = −A1_l, where A1_l = ⊕_{k ≥ l} (F_k ? Z^{(k)}[l−1] : 0) by CCX per bit. With F one-hot at K:
- A1_l = Z^{(K)}[l−1] for l ≤ K and 0 for l > K;
- so τ_l = y^{(K)}_{l−1} (= τ_l of the definition by §2.2) for l ≤ K, and 0 for l > K.

**C5 (back substitution, l = a..1).** At step l:
- ζ := the current τ_l; τ_l receives updates only from steps l′ > l, which are already done.
- C2 gives its flags. areg = 1 (one X on bit 0), then ⊕_ν flag_ν(1 ⊕ α_ν), so areg = α_{cos ζ} if ζ ∉ P ∪ {0}, else 1 = α_0.
- za_l = ζ·areg = ζ α_{cos ζ}: 0 if ζ = 0, ζ if ζ ∈ P.
- For j < l: τ_j += −za_l · Z^{(l−1)}[j−1] = ζ α_{cos ζ} y^{(l−1)}_{j−1} (`add_product` with coefficient −1, target τ_j, operands za_l and Z; no aliasing, since j ≠ l).

For l > K, τ_l = 0 (C4, and no later step writes τ_l), so za_l = 0 and nothing is added. For l ≤ K this is the definition's step with the genuine y^{(l−1)} (round l−1 < K). After step l, τ_l is never written again. At the weights stage, τ_{k+1} = ζ_{k+1} of the definition and za_{k+1} = ζ_{k+1}α_{cos ζ_{k+1}}.

**C6 (weights).** For block k < a, ga = za_{k+1} and gz = τ_{k+1}. The program applies CX(F_k → bit 0 of ga), then X[col] += ga·δ_i, then CX(F_k → bit 0 of ga) again, then X[col] += gz·bd_i. For k = a, ga = z0 (a dedicated zero register) and there is no gz term. Cases:
- k = K: F_K = 1 and za_{K+1} = 0 (C5: τ_{K+1} = 0; for K = a, z0 = 0). Toggling bit 0 makes ga = 1, so x_i = δ_i + ζ_{K+1}·bd_i = δ_i + 0 = δ_i. This is the definition's weight by §2.2.
- k < K: F_k = 0, so x_i = ζ_{k+1}α_{cos ζ_{k+1}}δ_i + ζ_{k+1}β_{cos δ_i}δ_i = ζ_{k+1}δ_i(α_{cos ζ_{k+1}} + β_{cos δ_i}), Lemma 1's weight. It is 0 when ζ_{k+1}δ_i = 0, which the definition skips.
- k > K: F_k = 0 and τ_{k+1} = za_{k+1} = 0 (C4, C5), so x_i = 0.

The second CX restores ga, because XOR of bit 0 is an involution and ga is not a target in between (it is an operand of the product). So X holds x(λ), and at the end of F every pool register is 0.

**C7 (q-th root, `_qroot_chain`).** Let q be a prime, q | κ′ | p−1 and x ∈ (F_p^×)^{κ′} ∪ {0}. Write p−1 = q^S Q with q ∤ Q and q e_1 ≡ 1 (mod Q), let z = g^Q and w_q = z^{q^{S−1}}.

z generates the q-Sylow subgroup, because g is not a q-th power. The function `coset_generator` asks for g^{(p−1)/q} ≠ 1 for every prime q | κ, which is exactly that. w_q has order q.

The chain computes:
- r = x^{e_1} (r = x if e_1 = 1);
- if S ≥ 2, t = x^{q e_1 − 1} (as x^{q−1} if e_1 = 1, else r^{q−1}·x^{e_1−1}).

Then r^q = x·t. For x ≠ 0, x = w^q, and t = (w^{q e_1 − 1})^q with Q | q e_1 − 1, so w^{q e_1 − 1} lies in the q-Sylow subgroup and t = z^{q k} for some 0 ≤ k < q^{S−1}.

Round j = 0..S−2:
- u_j = t_j^{q^{S−2−j}} (repeated q-th powers);
- flag_ν = [u_j = w_q^ν];
- t_{j+1} = t_j·z^{−q^{j+1}k_j} (omitted at j = S−2);
- r_{j+1} = r_j·z^{−q^j k_j}.

The constants are loaded as 1 ⊕ (1 ⊕ c) under one-hot flags, so the register is 1 when no flag is set.

Invariant: t_j = z^{q^{j+1}⌊k/q^j⌋}. Then u_j = z^{q^{S−1}⌊k/q^j⌋} = w_q^{k_j}, with k_j the j-th base-q digit of k, so exactly flag_{k_j} is set (none if k_j = 0). Moreover t_{j+1} = z^{q^{j+2}⌊k/q^{j+1}⌋}, and every update multiplies r by c and t by c^q, so r^q = x·t is preserved. At the end r = x^{e_1}z^{−k} and r^q = x^{q e_1}z^{−qk} = x·t_0·t_0^{−1} = x.

Edge cases:
- S = 1: the Sylow subgroup is μ_q and t ∈ ⟨z^q⟩ = {1}. The code returns r = x^{e_1} and r^q = x·t = x.
- x = 0: every power is 0, no flag is set, and r = 0.

**C8 (κ-th root and least root, `_root_chain`).** The q-chains run over the prime factors q of κ with multiplicity, κ = q_1⋯q_t. A q-th root of a κ′-th power (q | κ′ | p−1) is a (κ′/q)-th power: every q-th root of w^{κ′} is w^{κ′/q}ζ with ζ ∈ μ_q, and μ_q = ⟨γ^{(p−1)/q}⟩ ⊂ (F_p^×)^{κ′/q} because (p−1)/q = (κ′/q)·((p−1)/κ′). So, inductively with κ′ = κ, κ/q_1, …, the chain ends with r_0^κ = x.

Then:
- c0 = copy(r_0).
- For t = 1..κ−1: ct = ω^t r_0 (`add_scaled` from the fixed r_0), f = [ct < c0] by (M′), then a Fredkin swap c0 ↔ ct under f. After step t, c0 = min(c0, ω^t r_0).
- Since ω is a primitive κ-th root of unity, {ω^t r_0} is the set of all κ-th roots of x, so c0 = ρ(x) for x ≠ 0. All candidates are 0 at x = 0.
- res = ρ^u by square-and-multiply (an alias if u = 1).

**C9 (copy stage and Bennett).** The copy stage is C = Π_i (P_i ; A_i ; P_i^{−1}), with A_i = `add_scaled(S_i, res_i, 1)` and P_i the root chain plus ρ^u of column i.
- P_i touches no S wire. All its registers come from the pool or are fresh, and S is allocated before F.
- Since P_i neither reads nor writes S, P_i^{−1} undoes P_i on every basis state that differs from P_i's output only on S. So (P_i; A_i; P_i^{−1}) changes exactly S_i ← S_i + ρ(x_i)^u and restores every other wire, including the pool registers that later columns reuse.
- Hence C maps F(λ, 0) to F(λ, 0) with S = s(λ) (S was 0).
- F touches no S wire at all, so F^{−1}, the exact inverse permutation (every gate is an involution, and macros are inverted by reversing their gate lists), returns the non-S wires to (λ, 0).
- Hence U|λ⟩|0⟩|0⟩ = |λ⟩|s(λ)⟩|0⟩. ∎

**Labels as controls inside U [proved, given (M)].** Every gate that reads an L wire is one of:
- a CX control in `_copy` (C1);
- an operand of `add_product(vnew[r], bd_i, λ_i[r])` (C3), whose operands are never targeted by (M).

No `_eq_const_into`, `_pow_copy` or Fredkin touches L: they act on δ, τ, chain and copy registers only. So no flattened gate of U targets L. This is the property (D1) needs inside the block.

### 2.4 Checks run (controls for the proof; all pass)

`kappa_trace_check.py` (31 s, about 150 MB). This is an **independent reference**: its own primitive root and discrete logs, its own coset map, its own lexicographic contraction search, and a paper-faithful stop test (second elimination). It runs the circuit's F, reads the registers named in C3–C6 at the end of F, then C and F^{−1}.

Tests on every input:
- T1: F_k is one-hot at the reference K;
- T2: the δ of genuine rounds;
- T3: the final τ and za;
- T4: X = the reference weights;
- T5: C changes only S (snapshot of all other wires);
- T6: S equals the reference witness, labels restored, workspace 0, s ≠ 0, Σ s_i^d λ_i = 0, canonical output;
- L4: Lemma 4′ on every genuine round.

| (p, a, d) | κ | u | inputs | mode | K histogram | branch signatures / (cos ζ, cos δ) pairs | gates of U |
|---|---|---|---|---|---|---|---|
| (7, 1, 3) | 3 | 1 | 343 | exhaustive | 175 / 168 | 11 / 9 | 135 024 |
| (13, 1, 3) | 3 | 1 | 2 197 | exhaustive | 949 / 1 248 | 11 / 9 | 340 106 |
| (19, 1, 3) | 3 | 1 | 6 859 | exhaustive | 2 755 / 4 104 | 11 / 9 | 575 146 |
| (13, 1, 9) | 3 | 3 | 2 197 | exhaustive | | 11 / 9 | 371 114 |
| (19, 1, 15) | 3 | 5 | 6 859 | exhaustive | | 11 / 9 | 645 418 |
| (37, 1, 3) | 3 | 1 | 50 653 | exhaustive | 18 685 / 31 968 | 11 / 9 | 1 082 474 |
| (41, 1, 4) | 4 | 1 | 68 921 | exhaustive | 19 721 / 49 200 | 18 / 16 | 1 433 630 |
| (7, 2, 3) | 3 | 1 | 3 179 | structured + degenerate | 2 036 / 955 / 188 | 274 / 12 | 402 726 |
| (13, 2, 3) | 3 | 1 | 1 679 | sampled | 1 017 / 506 / 156 | 209 / 12 | 945 140 |
| (19, 2, 3) | 3 | 1 | 979 | sampled | 607 / 295 / 77 | 144 / 12 | 1 550 430 |
| (7, 3, 3) | 3 | 1 | 884 | sampled | 477 / 264 / 109 / 34 | 237 / 12 | 912 108 |
| (7, 4, 3) | 3 | 1 | 563 | sampled | 231 / 124 / 107 / 55 / 46 | 233 / 12 | 1 793 382 |
| (109, 1, 3) | 3 | 1 | 3 098 | sampled | 2 156 / 942 | 11 / 9 | 2 110 606 |
| (41, 2, 4) | 4 | 1 | 779 | sampled | 453 / 246 / 80 | 165 / 20 | 3 561 616 |
| (191, 1, 5) | 5 | 1 | 2 098 | sampled | 1 296 / 802 | | (`kappa56_check.py`) |
| (191, 2, 5) | 5 | 1 | 291 | sampled | 156 / 93 / 42 | | |
| (229, 1, 6) | 6 | 1 | 2 098 | sampled | 1 302 / 796 | | |
| (229, 2, 6) | 6 | 1 | 291 | sampled | 142 / 107 / 42 | | |

Notes on the table:
- "All 12 (cos ζ, cos δ) pairs" at κ = 3 and a ≥ 2, and 20 at (41, 2, 4), means every branch of the weight case table and of the α/β loads was exercised.
- p = 191 and p = 229 are the least primes ≡ 1 mod 5 and ≡ 1 mod 6 outside E_2(5) and E_2(6). The module refuses every smaller such prime, which is consistent with the paper's E_2(5) list. κ = 6 is composite, so two AMM chains (q = 2, 3) run there.
- In every row with the default contraction, the module's contraction equals the reference's own lexicographic search.

Other controls:
- **Every normalised contraction** (exhaustive inputs, a = 1): p = 7 (both of 2), p = 13 (both of 2) and p = 19 (6 spread over the 42; `contraction_valid` counts 42 normalised contractions at p = 19, 24 of them with all entries nonzero). All pass. *Note:* the κ report §10 quotes "40" contractions at p = 19 from its reviewer. That was not reconciled here and affects nothing.
- **Mutants** at (13, 1, 3), all detected:
  - β_1 + 1: fails T3/T4/T6;
  - α_2 + 1: fails T3/T4/T6;
  - least-root step skipped: fails T6 only;
  - τ coefficient +1: fails T3/T4/T6;
  - output coefficient 2: fails T6.
- **Static scans** at (7,1,3), (7,2,3), (13,2,3), (19,1,3), (7,3,3), (41,1,4) and (109,2,3):
  - F touches no S wire;
  - C touches S only through M `add_scaled` with coefficient 1;
  - no macro target aliases an operand (aliased squarings occur 32–340 times and are covered by (M));
  - no flattened gate of U targets a label wire;
  - the raw gates of C are x/cx/ccx.
- **(M)**: all 17 ≤ p ≤ 127, every coefficient (`macro_check.py`). **(M′)**: b ≤ 8.

### 2.5 Bugs and unproved branches

No bug was found in the power-mode circuit. Four items are noted and not papered over:
1. **`stop="general"` is not covered** by the written proof. It has a second `_fd` per round, and its weights use CX toggles on both ga and gz. The receiver never builds it.
2. **Padding words**: nothing is claimed for non-canonical inputs. The receiver lemma's (CLEAN) excludes them.
3. **Leastness of the contraction is not needed** for (D2a). The FFT-pruned search (p ≤ 2·10⁶, float correlations rounded with `rint`) is exact only up to floating-point error [argued]. If it ever pruned a valid branch it would return a valid but non-least contraction, and Theorem A_κ would still hold. The circuit and its classical reference would then both use that contraction, since `kappa_constants` is shared. The word "canonical" in the κ report's Theorem 6 depends on this; (D2a) does not.
4. **Search time**: see §4, gap G2.

## 3. (B) Which (G, H) the coherent generator covers

### 3.1 Statement

Let L be a Lie algebra over F_p of nilpotency class c with 2 ≤ c < p, given by structure constants in a basis. Let G = (L, ∗) and H = exp(h) ≤ G any subgroup (Lazard: every subgroup is of this form), with the hiding oracle f. Let A be the positive Rees cover (`thm:rees-cover`): dim A = n ≤ cm, m = dim L, grades A_d of dimension g_d, G_d = A/A_{>d} of dimension w_d, and κ_d = gcd(d, p−1). Let cfg = coherent_config_k(L) and Coh = TerminalSampleK(cfg). Write N_d = Π_{e=2}^{d} M_e with the coherent arities M_d = g_d + 1 (κ_d = 1) and M_d = (g_d+1)(g_d+2)/2 (κ_d ≥ 2).

**Theorem B.**
- **(R) [proved from the code].** Coh is constructed iff every grade d ∈ [2, c] with κ_d ≥ 3 has p ∉ E_2(κ_d). Otherwise construction raises `ValueError` (or `RuntimeError` for p > 2·10⁶ if the α-scan cap is hit). The only raising branch reachable from `TerminalSampleK` is `CoherentSDEKappa → kappa_constants` (`sde_circuit_k`). κ_d ≤ 2 never raises: CoherentSDE and CoherentSDEK2 exist for every odd p, and the arity check in `MergeBlock` cannot fail because the config arities are `coherent_arity_k`. By the paper's `prop:decoupled-sde` (AI-checked), E_2(2) = E_2(3) = ∅, so **c ≤ 3 is never refused**.
- **(S) [proved].** If constructed, Coh has the shape (S1)–(S6) and satisfies (KS), (INST), (D1), (D2) and (CLEAN). This is conditional on (M) for p > 127 and on `lem:homogeneous` for (KS).
- **(L) [proved, conditional].** Consequently, by receiver-lemma Theorem 2, Corollary 3 and Proposition 4, the readout of Coh run with exact QFT_p is uniform on h^⊥ conditioned on every positive-probability label tuple, and hence also unconditionally. This holds for every H. It is conditional on `lem:central` and `prop:descent` (paper; AI-checked, pending human review) and on exact QFT_p.
- **(C) [proved].** One terminal sample has:
  - c·N_c oracle calls;
  - N_c·w_c + Σ_{d=2}^{c} 2N_d g_d + Σ_{d=1}^{c−1} N_d w_d + w_1 exact QFT_p calls;
  - at most (158b² + 46b)·#macros + R gates, where #macros is given exactly by §3.3 and R, the raw X/CX/CCX/SWAP gates outside macros (first-dependency pivoting, coset-flag ladders, comparators, Fredkins), is of lower order by the closed-form Toffoli counts of the three SDE modules (O(g³b + κ M b) per SDE);

  in total O_c((n^{2c+1} + n^{2c−2}b²)·b²) = poly_c(log|G|, log p).

What this covers explicitly:
- **c = 2, 3:** every L, every H, every prime p > c.
- **c = 4:** p ≡ 3 (mod 4) always (κ_4 = 2). If p ≡ 1 (mod 4), κ_4 = 4: refused exactly for p ∈ E_2(4) = {5, 13, 17, 29, 37, 53}. κ_2 = 2, κ_3 ∈ {1, 3}.
- **c = 5:** additionally κ_5 = 5 when p ≡ 1 (mod 5): refused for p ∈ E_2(5) = {11, 31, 41, 61, 71, 101, 131, 151, 181}.
- **c = 6:** additionally κ_6 = 6 when p ≡ 1 (mod 6): refused for the 53 primes of E_2(6), the largest 859.
- **c ≥ 7:** κ_d ∈ divisors of d ≤ c. The refused primes are the union of E_2(κ) over the κ ≤ c that occur. These sets are known exactly only for κ ≤ 7; for κ ≥ 8, `prop:decoupled-sde` gives bounds and the generator decides each p by search.

For every fixed c all but finitely many p are covered, *conditionally*: p ≥ κ^{κ+1} implies p ∉ E_2(κ) for κ ≥ 3 by `prop:decoupled-sde` (AI-checked, pending human review).

The generator itself is H-independent: H enters only through the oracle table.

### 3.2 Proof of (S)

**(S1)–(S6).** These are read off `TerminalSample._emit` (inherited unchanged by `TerminalSampleK`, which only scopes the dispatch). [proved from the code; finite computation of `structure()` on the 10 constructed configurations of §3.4, §3.5]
- The recursion `_emit(d)` for d < c emits M_{d+1} subtrees, a fresh Q (QFT on every digit), the block and the instrument (d ≥ 2), so the tree has arities M_d (S1).
- A leaf emits the address QFTs and, per evaluation point s, the evaluation w += E_s a, the oracle (w → fresh y) and w −= E_s a (S2).
- `_instrument` emits QFT on the fresh label digits, `add_scaled(top coordinate of X, z_j, −1)` and QFT^† (S3).
- The block is emitted as remap(U), then per child remap(ctrl_i), remap(bch_i), remap(ctrl_i)^{−1}, then remap(U)^{−1} (S4).
- garbage_after records the subtree registers, and the final items are QFT on the root Q and one measurement (S5).
- The shared w, the arithmetic ancillas and one block-workspace pool are reused (S6).

**(KS) [proved, given (M) and `lem:homogeneous`].** By (M), the evaluation macros compute w = E_s(a) in coordinates and uncompute it. E_s is a Lie homomorphism, hence a group homomorphism (`thm:rees-cover` (ii), (iii)), and is linear in Lazard coordinates. So after the c oracle calls the state is p^{−n/2} Σ_a |a⟩|f̂(a)⟩ with f̂ the tuple oracle, and w = 0. By `lem:homogeneous`, f̂(a) = f̂(b) iff a^{−1}∗b ∈ exp(h̃) (distinct points s_1..s_c ∈ F_p^×, which needs c ≤ p−1). These are the left cosets of exp(h̃), with distinct values on distinct cosets.

**(INST) [proved, given (M)].** At a node of grade d, X holds an element of G_d, whose top grade d is central (`thm:rees-cover` (i), applied to the quotient). For central z, BCH(x, −z) = x − z, because every bracket containing z vanishes. So `add_scaled(top, z, −1)` is |x⟩|z⟩ ↦ |x z^{−1}⟩|z⟩.

**(D1) [proved from the code, given (M) and Theorem A_κ; finite computation on the 10 constructed configurations of §3.4].** A label register z of a grade-d node is created by `_instrument`. Its first items are QFT, then the instrument macro, where z is an operand, then QFT^†. Afterwards it is touched only by:
- the parent's block, through blk.lam ↦ z in remap(U) and remap(U)^{−1}. There the label wires are only CX controls and macro operands: Theorem A_κ (κ ≥ 3); the κ = 2 report Section 4 and its test `test_inputs_never_targeted_and_copy_stage_footprint`; the κ = 1 report's `test_inputs_never_targeted_and_copy_stage_writes_only_output`. Macro operands are never gate targets by (M).
- Nothing in ctrl_i or bch_i: block footprint, below.
- Nothing after the block: (S5).

The oracle outputs y are written only by their oracle call. They are not in any block's wire map and not in any later item.

**(D2a) [proved, given (M)].**
- κ_d = 1: the κ = 1 report's Theorem ("[proved + proof-by-computation, given macros]").
- κ_d = 2: the κ = 2 proof report's Theorem.
- κ_d ≥ 3: Theorem A_κ.

The block's U is `remap(sde.prog, wmap)` with wmap injective by allocation: labels → blk.lam, S → blk.S, anc → blk.anc, the rest → fresh `sde_work`. A wire bijection preserves the action. U touches only labels, S and SDE workspace.

**(D2b) [proved, given (M) and `thm:rees-cover` (iii)].** This is a general proof; the repo's `prove_controlled_merge` is a per-configuration symbolic replay. Fix a child i with registers x (w_d coordinates), its witness s = S_i and the parent Q = q (w_{d−1} coordinates). Let G := −δ_s(σ(q)) ∈ G_d, where σ pads the top grade with 0. In Lazard coordinates δ_s multiplies a grade-k coordinate by s^k (`thm:rees-cover` (ii)), and the inverse is negation (BCH(y, −y) = 0, (iii)).

- *ctrl_i.* It computes pw_k = s^k for k = 2..d−1 by a chain whose first step `add_product(pw_2, s, s)` is the aliased squaring covered by (M). Then G_j = −s^{deg j} q_j for j < w_{d−1}. So G holds −δ_s(σ(q)) on its w_{d−1} coordinates, with top coordinates 0.
- *bch_i* = four passes on the bracket registers bws[w] (one per pruned node w of `bch_nodes(d)`, with support supp(w)) and the w_d-coordinate register W, all starting at 0:
  1. *bracket pass (x, G, +).* Nodes in order (suffixes first): bws[w] += [w](x, G), where "xy" is [x, G] and a·w′ is [a, [w′]], with a ∈ {x, G} as the first letter. By multilinearity, each G-letter contributes the factor sign_g (here +1).
  2. *linear pass (+).* W += x + G + Σ_{α_w≠0} α_w [w](x, G). By `bch_nodes` (checked exactly inside the function against log(e^x e^y) in the free algebra, raising otherwise) and because G_d has class ≤ d, this is BCH_d(x, G) = x ∗ G.
  3. *bracket pass (x, G, −)* in reverse order. When node w is uncomputed its suffix registers still hold their values, so bws returns to 0.
  4. *swapreg(x, W).* Now x = x∗G and W = x_old.
  5. *bracket pass (x′, −G, +)*, with sign_g = −1, giving [w](x′, −G).
  6. *linear pass (−).* W −= BCH_d(x′, −G) = (x∗G)∗G^{−1} = x_old, by associativity and G^{−1} = −G (`thm:rees-cover` (iii); denominators invertible since c < p, enforced by `_mod_fraction`). So W = 0.
  7. *bracket pass (x′, −G, −).* bws returns to 0.
- *Support pruning (`Config._grade_nodes`) is exact.* supp(w) is the set of coordinates k with T[i, j, k] ≠ 0 for some i in the left support and j in the right support. Here G has support in the first w_{d−1} coordinates and x has full support. So every dropped coordinate of a node is identically 0, a node with empty support is identically 0 (as are all its parents, which are skipped), and dropped intermediates with α = 0 and no kept descendant are not needed.
- *ctrl_i^{−1}* returns pw and G to 0. They are operands only in bch_i, never targets.

Net effect: x ← x ∗ (−δ_s(σ(q))) and every merge register is 0. Footprint: reads x_i, S_i, Q and the merge workspace; writes x_i, W, bws, G and pw. `block_structure` confirms this on every configuration below.

**(D2c) [proved from the code; finite computation].** `MergeBlock.prog` is U + Σ_i (ctrl_i + bch_i + ctrl_i^{−1}) + U^{−1}, and `_emit` emits exactly remap of these segments under one wmap. The wmap is injective: its images are the children's fresh label and group registers, the fresh Q, the shared ancillas and the pool, all pairwise disjoint. Any shortfall of the pool would be a `KeyError`, not a silent overlap, and pool size = max over blocks. The merge workspace (G, pw, W, bws) is allocated on the SDE workspace wires, which are 0 between U and U^{−1} by (D2a), or on fresh wires. It is disjoint from the labels, S, the children and Q. So Proposition 4's footprint hypotheses hold.

**(CLEAN).** This follows from (KS), (INST), (D2) and (S6) by the induction stated in the receiver lemma §1.3: every macro restores its ancillas (M), every block returns S and its workspace to 0 (Proposition 4), the oracle writes fresh registers, and the QFTs act on canonical digit registers.

Then Theorem 2 (deferred measurement over the labels, using (D1) and (D2)) and Corollary 3 (with (KS), (INST), `lem:central`, `prop:descent` and the coherent arities, for which `prop:descent` holds as for any arity) give (L). ∎

### 3.3 Proof of (C): what one terminal sample costs

Exact macro count, in the notation of §3.1, verified against the emitted program in §3.5:

| component | macros |
|---|---|
| source evaluation | N_c · 2 · Σ_s nnz(E_s) ≤ 2c·m·n·N_c |
| instruments | Σ_{d=2}^{c} N_d g_d |
| SDE (U and U^{−1}) at grade d | 2 N_{d−1} · SDE_d |
| witness control at grade d | 2 N_{d−1} M_d · ((d−2) + w_{d−1}) |
| BCH merge at grade d | N_{d−1} M_d · (4 BR_d + 2 LIN_d) |

In the table:
- BR_d = Σ_{pruned nodes w} Σ_{k ∈ supp w} #{(i, j) : T_d[i, j, k] ≠ 0, i, j in the left and right supports} ≤ 2^{d−1}·nnz(T_d) ≤ 2^{d−1} n³;
- LIN_d = w_d + w_{d−1} + Σ_{α_w ≠ 0} |supp w| ≤ 2n + 2^{d−1} n;
- SDE_d is the closed form of the κ_d module (`closed_form_macros` of `rees_coherent_sde`, `_k2`, `_kappa`, each equal to the emitted count in those reports):
  - κ_d = 1: g³ + O(g²) + O(g b) products;
  - κ_d = 2: O(g⁴ + g² b²);
  - κ_d ≥ 3: 2n_F + 2M(T + ℓ(u)) + O(κM) with n_F = ½(a⁴ + …) + O(a² b) and T = O_κ(b²). Each AMM chain has S_q ≤ b rounds of at most S_q q-th powers.

  So SDE_d = O_κ(g_d⁴ + g_d² b²).

Bounds. With M_d ≤ (n+1)(n+2)/2 =: μ, N_d ≤ μ^{d−1}, every macro ≤ 158b² + 46b gates (rees_circuit_arith `formula_counts`) and raw gates of lower order:
- #macros = O_c(μ^{c−1}(cmn + 2^c n³) + μ^{c−2}(n⁴ + n²b²)) = O_c(n^{2c+1} + n^{2c−2}b²);
- gates = O_c((n^{2c+1} + n^{2c−2}b²) b²);
- QFT_p calls = O_c(n^{2c−1}).

Since n ≤ cm, m = log_p|G| ≤ log₂|G| and b ≤ log₂ p + 1, this is poly(log|G|, log p) for fixed c. The degree grows with c (2c+3 in n), as for every receiver of this tree shape (N_c is the source count).

Qubits: there is no reuse of garbage. The count is O(N_c·(n b + c·label_bits)) + (pool) + 3b+5 = poly_c as well.

**Not included, and not shown polynomial:**
- (i) The explicit QFT_p: `lem:qft-mod` gives poly(b, log 1/η) gates per transform with a hybrid total-variation bound, wired only in `rees_circuit_full` at F_3 and F_5.
- (ii) The classical generator time (§4 G2).
- (iii) The number of terminal samples per run, which is that of `thm:main` but at the coherent arities.

### 3.4 Checks run (controls; all pass)

**`gh_structure_check.py`** reads the program emitted by TerminalSampleK and checks:
- D1, item by item, for every label register: QFT, instrument operand, QFT^†, then never a target, never in a swap, transform, oracle or measurement; oracle outputs written once and never touched;
- `structure()` (garbage never touched again, single measurement at the end, of the root Q);
- D2c: every block occurrence equals remap(block.prog) under an injective, role-consistent wire map, the occurrence count equals N_{d−1}, and the block's U equals remap(sde.prog) injectively;
- `block_structure` footprints;
- `prove_controlled_merge` (symbolic over F_p[s, q, x] against `sym_bch_reference`);
- children i > 0 equal to child 0 under the S/x renaming;
- simulation: U on all label tuples when p^{Mg} ≤ 7·10⁴, else the whole block on 192 sampled inputs.

Results (every flag true in every constructed configuration) [finite computation for the structural rows; sampled where marked]:

| config (dims of the cover) | κ_d by grade d | arities M_d | items | label registers | D1, S5, D2c, footprints, D2b | simulation |
|---|---|---|---|---|---|---|
| Heisenberg F_3 (3,1) | 2:2 | 3 | 781 | 3 | all true | U on all 27 tuples |
| Heisenberg F_5 (3,1) | 2:2 | 3 | 1 125 | 3 | all true | U on all 125 tuples |
| n4(F_5) (4,2,1) | 2:2, 3:1 | 6, 2 | 6 459 | 24 | all true | grade 3 U on all 25; grade 2 block on 192 [sampled] |
| n4(F_7) (4,2,1) | 2:2, 3:**3** | 6, 3 | 19 787 | 30 | all true | grade 3 U on all 343; grade 2 block 192 [sampled] |
| n4(F_13) (4,2,1) | 2:2, 3:**3** | 6, 3 | 24 919 | 30 | all true | grade 3 U on all 2 197; grade 2 block 192 [sampled] |
| f(2,3) over F_7 (5,3,2) | 2:2, 3:**3** | 10, 6 | 79 351 | 150 | all true | blocks 192 each [sampled] |
| f(2,3) over F_13 (5,3,2) | 2:2, 3:**3** | 10, 6 | 98 987 | 150 | all true | blocks 192 each [sampled] |
| n5(F_7) (5,3,2,1) | 2:2, 3:**3**, 4:2 | 10, 6, 3 | 181 231 | 330 | all true | grade 4 U on all 343; grades 2, 3 blocks 192 [sampled] |
| n5(F_41) (5,3,2,1) | 2:2, 3:1, 4:**4** | 10, 3, 3 | 276 031 | 180 | all true | grade 4 U on all 68 921; grades 2, 3 blocks 192 [sampled] |
| n6(F_7), class five (6,4,3,2,1) | 2:2, 3:**3**, 4:2, 5:1 | 15, 10, 6, 2 | 2 157 766 | 4 110 | all true (900 grade-5, 150 grade-4, 15 grade-3 block occurrences) | grade 5 U on all 49; grades 2–4 blocks 192 each [sampled] |

The class-five terminal sample over F_7 has 1 474 970 960 gates, 299 922 qubits, 52 632 transforms and 9 000 oracle calls (893 s and 1.05 GB to build and check).

f(2,3) is the free nilpotent Lie algebra of rank 2 and class 3 (x, y, [x,y], [x,[x,y]], [y,[x,y]]), a new instance not run before; n4(F_13), f(2,3) and n5(F_41) (κ_4 = 4, the first κ = 4 grade in an assembled program) are new configurations. n5(F_7) is the paper's coherent class-four circuit over F_7: with Theorem A_κ its grade-three witness circuit is now covered by a proof, and its footprints are read off the program (the D2c role check and `block_structure`), the two items the Scope paragraph lists as missing.

Refusals, as predicted by (R):
- n5(F_13) and n5(F_5) are refused ("p = 13 / 5 lies in E_2(4)"; κ_4 = 4);
- f(2,3) over F_7 and F_13 (κ_3 = 3), n4(F_13) (κ_3 = 3) and n5(F_41) (κ_4 = 4, p ∉ E_2(4)) are constructed.

**`gh_count_bound.py`** checks:
- the exact macro formula of §3.3 against the emitted counts on every configuration;
- a scaling table over p for n4(F_p).

The exact formula equals the emitted macro count, component by component, on the nine constructed configurations above other than n6(F_7) (not run through this script) and on every scaling row [finite computation]; the per-child BCH macro count is below its coarse bound in every row. Totals (one terminal sample; gates exclude the oracle and the exact transforms) reproduce the paper's figures where they exist (115 282, 2 694 596, 4 832 806 and 83 492 540 gates for Heisenberg F_3, n4(F_5), n4(F_7), n5(F_7)):

| config | n | m | b | N_c | macros | gates | qubits | QFT calls | oracle calls |
|---|---|---|---|---|---|---|---|---|---|
| Heisenberg F_3 | 4 | 3 | 2 | 3 | 239 | 115 282 | 182 | 24 | 6 |
| Heisenberg F_5 | 4 | 3 | 3 | 3 | 315 | 344 834 | 263 | 24 | 6 |
| n4(F_5) | 7 | 4 | 3 | 12 | 2 616 | 2 694 596 | 1 198 | 176 | 36 |
| n4(F_7) | 7 | 4 | 3 | 18 | 4 426 | 4 832 806 | 1 629 | 230 | 54 |
| n4(F_13) | 7 | 4 | 4 | 18 | 5 138 | 9 903 076 | 2 105 | 230 | 54 |
| f(2,3) F_7 | 10 | 5 | 3 | 60 | 19 306 | 21 058 880 | 5 986 | 990 | 180 |
| f(2,3) F_13 | 10 | 5 | 4 | 60 | 21 722 | 41 378 508 | 7 765 | 990 | 180 |
| n5(F_7) | 11 | 5 | 3 | 180 | 77 806 | 83 492 540 | 20 566 | 3 330 | 720 |
| n5(F_41) | 11 | 5 | 6 | 90 | 50 188 | 204 993 304 | 20 528 | 1 740 | 360 |

Scaling in p at fixed algebra n4 (arities 6, 3 at every p ≡ 1 mod 3; κ_3 = 3): p = 7, 13, 19, 31, 37, 43, 61, 67 (b = 3..7) give macros 4 426, 5 138, 5 418, 6 218, 6 202, 6 338, 6 786, 6 746 (growth O(b) from the exponentiation chains) and gates 4.83, 9.90, 15.98, 20.05, 26.70, 28.03, 31.19, 39.67 million; gates/macro rises from 1 092 to 5 881, below 158b² + 46b (1 560 at b = 3, 8 064 at b = 7). This is the poly(b) behaviour of (C) on one family, a control, not an asymptotic test.

## 4. Gaps (strongest first)

- **G1 (strongest): grades with p ∈ E_2(κ_d).** There is no coherent solver for them. The circuit family needs a coherent witness circuit for Schedule 1 (the Chevalley–Warning / `thm:is-import` solver at arity κ_d g_d + 1) or for another universal solver of `eq:sde-target`. `prop:coherent-receiver` gives only existence (Pippenger–Fischer plus Bennett on the classical solver of running time T^{IS}_d). Such grades exist for every κ ≥ 4: line 1376 of main.tex says every p ≡ 1 (mod κ) with p ≤ κ² − 3κ + 3 lies in E_2(κ). So **class ≥ 4 is not covered at every p**. Larger κ (≥ 8) is covered wherever the search finds a contraction, which is decided per p.
- **G2: generator time.** These classical steps have no proved poly(log p) bound:
  - the least generator g of F_p^×/P: deterministic scan, poly under GRH only [argued];
  - the lexicographically least contraction: DFS over β ∈ [0, p)^{κ−1}, or FFT pruning in O(p log p) for p ≤ 2·10⁶. The paper's `lem:coherent-power-sde` says the deterministic choice "is not claimed to be polynomial".

  Theorem A_κ holds for every normalised contraction, so a **Las Vegas** search for any contraction (`prop:decoupled-sde`: O(κ^{κ+2} log κ) coset tests per success for p > T_S(κ), AI-checked) would give an expected-poly generator. That would also need a randomized g, and it is not implemented. The circuit size bound (C) is unaffected.
- **G3: (M) beyond p = 127** is [argued]; it is exhaustive for p ≤ 127 and every coefficient. (M′) beyond b = 8 is [argued].
- **G4: exact transforms.** (L) is for exact QFT_p. Explicit transforms with a total-variation bound exist only at F_3 and F_5.
- **G5: arities and query count differ from `thm:main`.** The coherent arities are (g+1)(g+2)/2 at κ ≥ 2, against κ g + 1 for Chevalley–Warning: 6 instead of 5 at g = 2, κ = 2, and 10 instead of 7 at g = 3. So Coh is a correct receiver with its own, larger query count. It is not the receiver of `thm:main` / `prop:coherent-receiver`.
- **G6: the `stop="general"` variant and padding words** are not covered (§2.5). Neither is used.
- **G7: the paper lemmas** `lem:central`, `prop:descent` and `lem:homogeneous` are AI-checked, pending human review. Everything here inherits that.

## 5. Claim gates that stay false

- `coherent_receiver_implemented` (research/reductions/rees_hsp_reduction.json; not edited) stays **false**: G1, G2, G4 and G5. In particular it is not the receiver of `thm:main`, and it does not cover all p.
- `general_sde_implemented` stays **false**: no coherent solver at p ∈ E_2(κ).
- `speedup_claim_allowed` stays **false**.
- `independent_review` stays **false**: AI only, no human.
- `wired_into_generated_receiver` in the `rees_coherent_sde_kappa` STATUS dict is false there, but `TerminalSampleK` does wire the module at κ ≥ 3 grades. This flag is not touched (it is in a `theorems/` module); see §7.3.

## 6. Next hard question, next command, acceptance test

**Next hard question.** Is there a coherent witness circuit, of size poly(g, b) for fixed κ, for `eq:sde-target` at a grade with p ∈ E_2(κ)? Two routes: the Chevalley–Warning solver of `thm:is-import` made reversible, or a three-level contraction that exists at the exceptional primes. Without it, class ≥ 4 is covered only off E_2(κ_d).

**Next command (cheapest step that closes G2 for the circuit family).** Add a seeded Las Vegas contraction search as a *new* script (not a `theorems/` edit) and rerun Theorem A_κ's controls with the contraction it finds:

    nice -n 10 /opt/anaconda3/bin/python research/audits/reviews/2026-11-05-rees-receiver-general-gh/kappa_trace_check.py --out <new>.json

The script needs a `--contraction random:<seed>` option to be added. Expected artifact: a JSON with the random contraction's rows at κ = 3, 4, 5, 6.

Acceptance test:
- every T1–T6 and L4 flag is true for each contraction drawn;
- the number of coset tests per success is recorded and is within the `prop:decoupled-sde` estimate;
- `contraction_valid` holds for every drawn contraction.

## 7. Proposed replacement text (not applied; quoted exactly from `docs/papers/rees-hsp/appendix-backends.tex`)

The "Coherent-label backends" and "Scope" text is now in `appendix-backends.tex`, subsections `app:backends-coherent` and `app:backends-scope`; it moved there from main.tex.

### 7.1 Scope, paragraph 2, last two sentences

Current (line 45):

> For the coherent class-four circuit over $\mathbb{F}_7$ the proof is still conditional: the witness circuit is proved at the $\kappa = 2$ grades two and four but checked on samples only at grade three, and the footprints of the class-four program are not read off it. The proof concerns these generated programs; no generator of coherent receivers for general $(G,H)$ exists.

Proposed:

> The same written argument, with the coset flags, the two-level contraction and one Adleman--Manders--Miller extraction per prime factor of $\kappa_d$ in place of the sign test and Tonelli--Shanks, proves that the witness circuit of Lemma~\ref{lem:coherent-power-sde} writes a valid witness on every canonical label tuple at every $\kappa_d \ge 3$ with $p \notin E_2(\kappa_d)$, for any normalised contraction, again assuming only the two macros and a comparator, checked exhaustively for $p \le 127$ and $b \le 8$ (AI-written and AI-checked, pending human review; not machine-verified). With it, the deferred-measurement proof applies, for every subgroup $H$, to the program that the coherent generator \texttt{rees\_circuit\_\allowbreak coherent\_k3.py} emits for every Lie algebra over $\mathbb{F}_p$ of class $c < p$ at which every grade with $\kappa_d \ge 3$ has $p \notin E_2(\kappa_d)$, in particular to every class-two and class-three instance and to the class-four instance over $\mathbb{F}_7$; the generator refuses every other instance, and its program has $\poly_c(\log|G|, \log p)$ gates, excluding the transforms. This is not the receiver of Theorem~\ref{thm:main}: its merge arities are the coherent ones, it uses exact transforms, it does not cover the primes in $E_2(\kappa_d)$, and the classical search for its constants is not shown to run in polynomial time.

### 7.2 Scope, paragraph 3, the sentence "None of these circuits …"

Current (line 47):

> None of these circuits is a coherent receiver for general $(G,H)$, and they test no asymptotic cost.

Proposed:

> The coherent generator covers the $(G,H)$ stated in the preceding paragraph, conditionally on Lemma~\ref{lem:central}, Proposition~\ref{prop:descent} and exact transforms; it is not a coherent receiver for general $(G,H)$, since grades with $p \in E_2(\kappa_d)$ have no coherent solver, and the runs test no asymptotic cost.

The last sentence of that paragraph ("That is a statement of existence: no circuit generator for it has been implemented.") stays true and is kept: `prop:coherent-receiver` has the arities of `thm:main`, which Coh does not.

### 7.3 Code doc (described, not applied: `theorems/` is not edited)

In `theorems/rees_coherent_sde_kappa.py`, STATUS `"wired_into_generated_receiver": False` and the docstring line "Does NOT: wire into the generated receiver" are out of date: `rees_circuit_coherent_k3.sde_circuit_k` wires it. Proposed diff:

```
-          "wired_into_generated_receiver": False,
+          "wired_into_generated_receiver": True,   # via rees_circuit_coherent_k3.sde_circuit_k
```

Also proposed: point the docstring's report reference to this report for the general-κ proof. No functional change is proposed; no bug was found.

## 8. Files

- `research/audits/reviews/2026-11-05-rees-receiver-general-gh/kappa_trace_check.py`, with `.json` and `.log`: (A) controls.
- `.../kappa56_check.py`, with `.json` and `.log`: κ = 5 at p = 191 and κ = 6 at p = 229.
- `.../macro_check.py`, with `.json` and `.log`: (M) for 17 ≤ p ≤ 127, every coefficient.
- `.../gh_structure_check.py`, with `.json` and `.log`: (B) structural checks.
- `.../gh_count_bound.py`, with `.json` and `.log`: (B) exact counts and scaling.
- `tests/test_rees_receiver_general_gh.py`: quick regression controls (about 10 s).

Interpreter `/opt/anaconda3/bin/python`; every run used `nice -n 10`, at most 2 processes, peak RSS 1.05 GB (the class-five check).
