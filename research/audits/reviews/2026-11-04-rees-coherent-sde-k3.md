# Rees HSP: a coherent (reversible) SDE solve at kappa_d = 3, and at any fixed kappa_d with p ∉ E_2(kappa_d)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels as in `2026-11-04-rees-coherent-sde.md`:
**[proved]** = written argument here; **[proof-by-computation]** = exhaustive check over ALL
inputs of the stated finite set; **[sampled]** = exact on a stated random subset only;
**[exact count]** = counted from the emitted gate list (or exact per-macro closed forms);
**[argued]** = reasoning, not machine-checked.

Scope: grades d with κ = κ_d = gcd(d, p−1) ≥ 2 and p ∉ E_2(κ), label columns in F_p^a
(a = g_d), target `eq:sde-target`: a nonzero s ∈ F_p^M with Σ_i s_i^d λ_i = 0. The motivating
case is κ = 3 (grade 3 of n4(F_7): class 3, p = 7 ≡ 1 mod 3, a = 1). The construction is
written for every κ ≥ 2; it is checked mostly at κ = 3, with κ = 2, 4, 5 and 6 as controls.
Solver: the triangular two-level solver of `prop:triangular-sde` at M = (a+1)(a+2)/2 columns,
with a canonical contraction, first dependencies, a stop test proved equivalent to a κ-th
power test (Lemma 4′, which generalises the κ = 2 Lemma 4 to every κ), and an oblivious
Adleman–Manders–Miller root. Companion of `2026-11-04-rees-coherent-sde.md` (κ = 1) and
`2026-11-04-rees-coherent-sde-k2.md` (κ = 2).

Module: `theorems/rees_coherent_sde_kappa.py` (new). Tests: `tests/test_rees_coherent_sde_k3.py`
(new). This report is written incrementally; sections are appended as they are finished.

## 0. Correction to the κ = 2 report

The κ = 2 report (§5 item 1 and §9) says Lemma 4 "is special to κ = 2" and that for κ ≥ 3
"the second elimination per round would be needed again". **That is wrong.** Lemma 4′ below
proves the same equivalence (stop test ⟺ every nonzero δ_i is a κ-th power ⟺ v_{k+1} = 0) for
every κ ≥ 2 and every normalised contraction, by a shorter argument that uses only β_0 = 0 and
the minimality of the first dependency. The κ = 2 report's §1 proof is still correct; only its
remark about κ ≥ 3 was wrong. The paper-faithful general stop test (a second first dependency
per round) is also implemented here (`stop="general"`) and checked, so that both variants and
their agreement are on record.

## 1. The canonical witness (definition)

Fix a prime p, κ ≥ 2 with κ | p−1, a ≥ 1 and d with gcd(d, p−1) = κ. Notation:
P = (F_p^×)^κ (index κ), h = (p−1)/κ.

**Constants (depend on p and κ, and u on d; a classical precomputation).**
- g = the least integer ≥ 2 whose image generates F_p^×/P (equivalently g^{(p−1)/q} ≠ 1 for
  every prime q | κ; for κ = 3 the least non-cube, for κ = 2 the least non-residue m).
  ω = g^h, a primitive κ-th root of unity. cos(y) = ν iff y ∈ g^ν P, read off from
  y^h = ω^ν (y ≠ 0); cos(0) is undefined and every weight with a zero factor is 0.
- The **canonical contraction**: (α, β) ∈ F_p^κ × F_p^κ with α_0 = 1, β_0 = 0 and
  α_j + β_i ∈ g^{−(i+j)} P ∪ {0} for all i, j ∈ Z/κ (the normalisation of
  `prop:triangular-sde`), chosen lexicographically least as the integer tuple
  (β_1, …, β_{κ−1}, α_1, …, α_{κ−1}) ∈ [0, p)^{2κ−2}. It exists iff p ∉ E_2(κ).
- u = the least u ≥ 1 with u·(d/κ) ≡ 1 (mod h) (u = 1 for d = κ and when h = 1).
- For each prime q | κ (with multiplicity, ascending): p−1 = q^{S_q} Q_q with q ∤ Q_q,
  e_q ∈ [1, Q_q] with q·e_q ≡ 1 (mod Q_q) (e_q = 1 if Q_q = 1), z_q = g^{Q_q} (a generator of
  the q-Sylow subgroup, since g is not a q-th power), w_q = z_q^{q^{S_q−1}}.

Canonical contractions found by the search (`canonical_contraction`, κ = 3, (α, β) =
((1, α_1, α_2), (0, β_1, β_2))):

| p | g | α | β |
|---|---|---|---|
| 7 | 2 | (1, 0, 5) | (0, 2, 6) |
| 13 | 2 | (1, 0, 10) | (0, 3, 12) |
| 19 | 2 | (1, 0, 5) | (0, 3, 1) |
| 31 | 3 | (1, 13, 19) | (0, 4, 2) |
| 37 | 2 | (1, 0, 12) | (0, 2, 1) |
| 43 | 3 | (1, 0, 5) | (0, 6, 2) |
| 109 | 3 | (1, 21, 58) | (0, 8, 2) |

At κ = 2 the search returns α = (1, 0), β = (0, m−1), the contraction of the κ = 2 report's
Lemma 1 (proof: β_1 must have 1 + β_1 ∈ N ∪ {0}, whose least solution is m−1 < p−1; then
α_1 = 0 works since α_1 + β_1 = m−1 ∈ P by minimality of m). So the κ = 2 module's constants
are the canonical ones of this definition.

**First dependency** FD(w) of a list w_0..w_{n−1} in F_p^a: as in the κ = 2 report (§1):
j* = the first index with w_{j*} ∈ span(w_{<j*}), y_{j*} = 1, y_i = −c_i for i < j*, y_i = 0
beyond. Blocks B_0..B_a of sizes a+1−k at offsets o_k, as there.

**Rounds (k = 0, 1, …).** Given independent v_1..v_k (U_k = span, U_0 = 0):
1. y^(k) = FD(v_1, …, v_k, λ_{o_k}, …, λ_{o_k+a−k}); δ^(k)_i = y^(k)_{k+i} for i ∈ B_k, so
   e_{k+1} := Σ_i δ_i λ_i = −Σ_{l≤k} y^(k)_{l−1} v_l ∈ U_k, δ ≠ 0, δ_{j*−k} = 1.
2. v_{k+1} := Σ_{i: δ_i ≠ 0} β_{cos δ_i} δ_i λ_i.
3. If v_{k+1} ∈ U_k, stop: K := k and y' := FD(v_1, …, v_{K+1}) (dependency at index K).
   Otherwise append v_{k+1}.

**Weights.** x ∈ F_p^M, initially 0.
- Round K at ζ = 1: x_i = δ^(K)_i (1 + β_{cos δ^(K)_i}) for i ∈ B_K (0 if δ_i = 0).
- τ ∈ F_p^K, τ_l := y^(K)_{l−1} + y'_{l−1}.
- Back substitution l = K, …, 1: ζ_l := τ_l. If ζ_l ≠ 0, n := cos ζ_l, x_i = ζ_l δ^(l−1)_i
  (α_n + β_{cos δ^(l−1)_i}) on B_{l−1} and τ_j += ζ_l α_n y^(l−1)_{j−1} for j < l.
- Blocks B_{K+1}..B_a get 0.

**Roots.** ρ(x) := the least integer r ∈ {0, …, p−1} with r^κ ≡ x (ρ(0) = 0). The canonical
witness is s_i := ρ(x_i)^u mod p.

(The κ = 2 module normalises the root to the even one instead; with that one exception, the
definition here at κ = 2 reproduces the κ = 2 definition, which `test_kappa2_weights_match_k2`
checks on the weights x.)

**Lemma 1 (round realisation) [proved].** For a round k, ζ ∈ F_p and
x_i = ζ δ_i (α_{cos ζ} + β_{cos δ_i}) (x_i = 0 if ζ δ_i = 0): every x_i ∈ P ∪ {0}, and
Σ_{i∈B_k} x_i λ_i = ζ α_{cos ζ} e_{k+1} + ζ v_{k+1}.

*Proof.* ζ δ_i ∈ g^{cos ζ + cos δ_i} P and α_{cos ζ} + β_{cos δ_i} ∈ g^{−(cos ζ + cos δ_i)} P ∪ {0}
by the contraction condition, so the product lies in P ∪ {0}. The sum splits into
ζ α_{cos ζ} Σ δ_i λ_i and ζ Σ β_{cos δ_i} δ_i λ_i. ∎

**Theorem 2 (canonical witness) [proved].** For p ∉ E_2(κ) and every tuple of M columns in
F_p^a, the definition is total and deterministic, and s satisfies s ≠ 0, s_i^d = x_i for all i,
and Σ_i s_i^d λ_i = 0; x_{i*} = 1 at i* = o_K + (j*_K − K).

*Proof.* Totality and the equation Σ x_i λ_i = 0 are the κ = 2 report's Theorem 3 word for word,
with Lemma 1 in place of its Lemma 2 (the invariant τ^(l) := Σ_{j≤l} τ_j v_j, step l subtracts
C_l = ζ_l α_{cos ζ_l} e_l + ζ_l v_l, which in coordinates drops τ_l and adds
ζ_l α_{cos ζ_l} y^(l−1)_{j−1} to τ_j; the definition skips ζ_l = 0, where C_l = 0). On B_K,
x_{i*} = 1·(1 + β_0) = 1. Every x_i ∈ P ∪ {0} (Lemma 1), so ρ(x_i) exists. For x ∈ P,
(ρ(x)^u)^d = (ρ(x)^κ)^{u d/κ} = x^{u d/κ} = x · (x^h)^t = x, where u d/κ = 1 + t h and x^h = 1;
x = 0 gives 0. (u exists because gcd(d, p−1) = κ makes d/κ invertible mod h.) Hence s_{i*} =
ρ(1)^u = 1 and Σ s_i^d λ_i = Σ x_i λ_i = 0. ∎

**Lemma 3 (canonical contraction) [proved; proof-by-computation for the search].** The
contraction conditions with i = 0 read α_j ∈ g^{−j} P ∪ {0}; with j = 0 they read
1 + β_i ∈ g^{−i} P ∪ {0}. Given β, the conditions on α_j involve α_j alone, so the lexicographic
search is a DFS over β_1, …, β_{κ−1} in increasing order (each filtered by its j = 0 condition)
followed by the least α_j for each j. `canonical_contraction` implements exactly this; for
p ≤ 2·10^6 it prunes a value of β_i when some α_j has no remaining candidate (counts by FFT
cross-correlation), which removes only branches with no completion, so it returns the same
tuple. Checks: equal to the unpruned DFS for every p ≡ 1 (mod κ) below 200 (κ = 2, 4), 400
(κ = 3) and 250 (κ = 5); equal to the brute-force lexicographic enumeration of all
p^{2κ−2} tuples for (p, κ) ∈ {(7, 3), (13, 3), (19, 3)}; `contraction_valid` re-checks all κ²
conditions on every contraction the circuit uses. Consequence of the j = 0 condition:
β_ν ≠ 0 for every ν ≠ 0 (β_ν = 0 would need 1 ∈ g^{−ν}P). "Exists iff p ∉ E_2(κ)" uses two
elementary steps: a decoupled contraction C_{ij} = z_i z_j(α_j + β_i) of `prop:decoupled-sde`
can be normalised (shift α by c and β by −c with c = β_0, then divide by α_0 + β_0 ∈ P, which
is nonzero since C_{00} ≠ 0), which gives α_0 = 1, β_0 = 0 and the stated coset conditions;
and whether one exists does not depend on the generator g of F_p^×/P (another generator is
g^t P with gcd(t, κ) = 1, and reindexing i ↦ ti, j ↦ tj maps contractions to contractions).
Existence: E_2(3) = ∅ (main.tex,
`prop:decoupled-sde`, from AI-only reports), and the search found a contraction at every
prime p ≡ 1 (mod 3) below 400, a finite confirmation only.

**Lemma 4′ (the stop test is a κ-th-power test, every κ) [proved; also proof-by-computation].**
In round k, with v_1..v_k independent and δ = δ^(k) the first-dependency coefficients:

  v_{k+1} ∈ U_k  ⟺  β_{cos δ_i} δ_i = 0 for every i  ⟺  every nonzero δ_i lies in P  ⟺  v_{k+1} = 0.

Hence at the stop round y' = (0, …, 0, 1), τ_l = y^(K)_{l−1}, and x_i = δ_i on B_K.

*Proof.* Let L = (v_1, …, v_k, λ_{B_k}) be the round's list, j* ≥ k its first dependent index,
y the first dependency (y_{j*} = 1, y = 0 beyond j*). Suppose v_{k+1} = Σ_l c_l v_l. Then the
vector r with entries −c_l on the v_l and β_{cos δ_i} δ_i on λ_{B_k,i} is a linear relation
among L, and it is supported on indices ≤ j* (δ_i = 0 beyond j*). The entries of L before j*
are independent, so the relations supported on indices ≤ j* form the line spanned by y; hence
r = r_{j*} y. But r_{j*} = β_{cos δ_{j*−k}} δ_{j*−k} = β_{cos 1}·1 = β_0 = 0, so r = 0, i.e.
β_{cos δ_i} δ_i = 0 for every i. Since β_ν ≠ 0 for ν ≠ 0 (Lemma 3), this says every nonzero δ_i
has cos δ_i = 0, i.e. δ_i ∈ P; and then v_{k+1} = 0. The converse implications are immediate.
At the stop round v_{K+1} = 0, so FD(v_1, …, v_K, 0) = (0, …, 0, 1), and the round-K weights
are δ_i(1 + β_{cos δ_i}) = δ_i. ∎

The argument needs exactly two properties of δ: it is a minimal dependency (the relations on its
support form a line), and it has a nonzero entry whose class has β = 0. Both hold for the
paper's normalisation "first nonzero entry 1" as well. For κ = 2 this is the κ = 2 report's
Lemma 4, with a different proof; its reviewer's counterexample for a non-minimal δ (p = 5,
δ = (2, 1)) shows minimality is needed. Computational check: on every round of every input of
(p, a) = (7, 1), (13, 1), (19, 1) (κ = 3, exhaustive) and of 20 000 structured inputs at (7, 2),
5 000 at (13, 2), 3 000 at (7, 3), 2 000 at (19, 3), 500 at (7, 4) (κ = 3), 3 000 at (41, 2)
(κ = 4) and 1 000 at (211, 2) (κ = 5), the paper-faithful test "FD(v_1..v_{k+1}) at index k",
"no nonzero δ_i outside P" and "v_{k+1} = 0" agree, and y' = (0, …, 0, 1) at every stop
(0 violations in 47 131 rounds; `test_lemma4prime_on_references`).

**Lemma 5 (row-space invariance) [proved].** For g ∈ GL_a(F_p), the canonical witness of
(gλ_1, …, gλ_M) equals that of (λ_1, …, λ_M). Hence s depends only on the row space of the
a × M matrix [λ_1 … λ_M].

*Proof.* Span membership and dependency coefficients are invariant under an injective linear map
applied to every vector of a list, so every first dependency (y^(k), y') is unchanged; by
induction each v_{k+1} = Σ β δ λ maps to g v_{k+1} (δ unchanged), so every stop test, τ and x
is unchanged, and s depends only on x. Two a × M matrices with the same row space differ by
left multiplication by an element of GL_a. ∎

(Lemma 5 is used only to choose a finite set of representative inputs in §4; it is not a
property of the circuit, which is checked on the representatives themselves.)

## 2. The reversible construction

Module `theorems/rees_coherent_sde_kappa.py`, class `CoherentSDEKappa(p, a, d, stop=…)`.
Encoding, gate set, arithmetic macros (`add_product`, `add_scaled` of
`theorems/rees_circuit_arith.py`), register pool, OR/AND ladders, Fredkin swaps, the coherent
first-dependency machine `_fd` and the simulator `BitSim` are those of the κ = 1 and κ = 2
modules (imported; `CoherentSDEKappa` subclasses `CoherentSDEK2` for its helpers and has its own
`__init__`; no existing file is edited). Two variants:

- `stop="power"` (default): the stop test of Lemma 4′ (no second elimination);
- `stop="general"`: the paper-faithful stop test, a second first-dependency machine per round on
  (v_1, …, v_{k+1}), with τ_l = y_{l−1} + y'_{l−1} and round-K weights δ_i(1 + β_{cos δ_i}).

  U = F · C · F^{−1}, with the Bennett argument of the κ = 1 and κ = 2 reports: C writes only the
outputs S and pool registers that it cleans itself, so F^{−1} returns every non-output wire to 0
[proved: F^{−1}F = id; the simulator checks it anyway].

**Coset flags.** For a register y: y^h by square-and-multiply into pool registers, then the
κ−1 equality tests [y^h = ω^ν] (X on the zero bits of the constant, AND ladder into a flag,
X back), ν = 1..κ−1, and the chain uncomputed. The flags are one-hot on y ≠ 0 with cos y ≠ 0
and all 0 when y ∈ P ∪ {0}. A constant c_{cos y} with c_0 = 0 is loaded into a zero register by
CX gates from the flags (XOR of one-hot loads); one with c_0 = 1 by one X on bit 0 and loads of
1 ⊕ c_ν.

**Forward pass F** (every round runs; nothing is skipped on data):

0. run_0 = 1. Invariant: run_k = [rounds 0..k−1 all continued], and when run_k = 1 the
   registers V hold the genuine v_1..v_k.
1. For k = 0..a:
   a. `_fd` on (v_1..v_k, λ_{B_k}) (a+1 columns in F_p^a), δ_i = −z_{k+i} (`add_scaled`, −1).
   b. Per block column: coset flags of δ_i; B_i = β_{cos δ_i} loaded under them;
      bd_i = δ_i·B_i (`add_product`); in power mode nq_i = ⊕_ν flag_ν = [δ_i ∉ P ∪ {0}]
      (κ−1 CX, one-hot).
   c. v_{k+1}[r] += bd_i·λ_i[r] (a(a+1−k) products).
   d. Stop bit: power mode stop_k = AND_i ¬nq_i (Lemma 4′); general mode stop_k = the dep flag
      at index k of `_fd` on (v_1..v_{k+1}) (k+1 columns; its z gives −y').
      F_k = run_k ∧ stop_k (CCX), run_{k+1} = run_k ⊕ F_k (two CX). Exactly one F_k is 1, at k = K.
   Rounds after K run on garbage; their outputs only enter through F_k = 0 or ζ = 0 below.
2. *Coordinates* τ_l (l = 1..a) = −(XOR-select of z^(k)_{l−1} under F_k, k ≥ l) (`add_scaled` −1),
   and in general mode also −(XOR-select of z'^(k)_{l−1}). τ_l = 0 for l > K.
3. *Back substitution* l = a..1: coset flags of ζ_l = τ_l; A_l = α_{cos ζ_l} loaded (α_0 = 1 by
   default, so ζ = 0 gives A = 1 and za = 0); za_l = ζ_l·A_l (`add_product`); then
   τ_j += −za_l·z^(l−1)_{j−1} for j < l (`add_product`, −1). For l > K, ζ_l = 0 adds nothing.
4. *Weights* on block k: x_i = (F_k + za_{k+1})·δ_i + ζ_{k+1}·bd_i (power mode; k = a has only
   the first term) or x_i = (F_k + za_{k+1})·δ_i + (F_k + ζ_{k+1})·bd_i (general mode). The
   "F_k +" is one CX from F_k onto bit 0 of the za (resp. τ) register around the products and
   one CX back: F_k = 1 only at k = K, where za_{K+1} = ζ_{K+1} = 0, so the register reads 1
   there. This equals the definition: for k < K, x_i = ζ_{k+1} δ_i(α_{cos ζ} + β_{cos δ_i});
   at k = K, x_i = δ_i (power mode, bd_i = 0 by Lemma 4′) or δ_i(1 + β_{cos δ_i}); for k > K, 0.

**Copy stage C** (per column, local compute–copy–uncompute):
- *κ-th root.* For each prime q | κ (with multiplicity), an oblivious generalised
  Tonelli–Shanks (Adleman–Manders–Miller digit extraction) with the fixed z_q = g^{Q_q}:
  r = x^{e_q} (= x when e_q = 1), and, if S_q ≥ 2, t = r^{q−1}·x^{e_q−1} = x^{q e_q − 1}, so that
  r^q = x·t and t ∈ ⟨z_q^q⟩. For j = 0..S_q−2: u = t^{q^{S_q−2−j}} (repeated q-th powers) lies in
  μ_q = ⟨w_q⟩; digit flags f_ν = [u = w_q^ν], ν = 1..q−1; then r ← r·z_q^{−ν q^j} under f_ν
  in every round, and t ← t·z_q^{−ν q^{j+1}} under f_ν in every round but the last
  (constants loaded by one X and CX gates from the one-hot flags; constant 1 when no flag is
  set). Invariant: r^q = x·t,
  t ∈ ⟨z_q^{q^{j+1}}⟩ at round j; at the end t ∈ ⟨z_q^{q^{S_q}}⟩ = 1, so r^q = x [proved below].
  The q-th root of a κ'-th power (q | κ' | p−1) is a (κ'/q)-th power: if x = w^{κ'}, every
  q-th root is w^{κ'/q}ζ with ζ ∈ μ_q, and μ_q ⊂ (F_p^×)^{κ'/q} because
  μ_q = ⟨γ^{(p−1)/q}⟩ for a primitive root γ and (p−1)/q = (κ'/q)·((p−1)/κ'). So the chain over
  the primes of κ ends with r_0^κ = x.
- *Least root.* c_0 = copy of r_0; for t = 1..κ−1: c_t = ω^t·r_0 (`add_scaled` with the
  constant ω^t), f = [c_t < c_0] by a comparator (two Cuccaro adders on the arithmetic ancillas:
  (c_t, e) −= c_0, copy the sign bit e, add back), Fredkin swap c_0 ↔ c_t under f. Then
  c_0 = min over the κ roots r_0 μ_κ = {all κ-th roots of x} = ρ(x) (x ≠ 0; all are 0 at x = 0).
- *Power* ρ^u by square-and-multiply, `add_scaled(S_i, ρ^u, 1)`, then the whole chain reversed;
  registers and flag bits go back to the pools.

*Proof of the root round [proved, standard].* Write t = z^{q^{j+1} m} at round j (z = z_q,
S = S_q). Then u = t^{q^{S−2−j}} = z^{q^{S−1} m} = w_q^{m mod q}, so the flag gives
k_j = m mod q, and t z^{−q^{j+1} k_j} = z^{q^{j+1}(m − k_j)} ∈ ⟨z^{q^{j+2}}⟩, while
(r z^{−q^j k_j})^q = x t z^{−q^{j+1} k_j}. Initially r^q = x^{q e_q} = x·x^{q e_q − 1} = x t, and
t = x^{q e_q − 1} with x = w^q a q-th power and Q_q | q e_q − 1 gives t = (w^{q e_q − 1})^q with
w^{q e_q − 1} in the q-Sylow subgroup, so t ∈ ⟨z^q⟩. If S = 1 the q-Sylow subgroup is
μ_q and t = 1 already (no rounds, t not computed). ∎

**Theorem 6 (coherent SDE at fixed κ) [proved, conditional on the arithmetic macros on
canonical inputs (proof-by-computation for p ≤ 13, argued beyond); proof-by-computation on the
§4 sets; AI-checked].** For every prime p, κ ≥ 2 and d with gcd(d, p−1) = κ and p ∉ E_2(κ),
and a ≥ 1, both variants of `CoherentSDEKappa(p, a, d)` map |λ⟩|0⟩_S|0⟩_work ↦
|λ⟩|s(λ)⟩_S|0⟩_work on every canonical input λ ∈ (F_p^a)^M, M = (a+1)(a+2)/2, with s the
canonical witness of §1; s ≠ 0 and Σ s_i^d λ_i = 0. (Theorem 2, Lemma 4′ for the power variant,
the step-by-step correspondence above, the root proof, and the macros.)

## 3. Gate and qubit counts [exact count]

Notation: b = ⌈log2 p⌉; ℓ(n) = (bitlen(n)−1) + (hw(n)−1) for n ≥ 2, ℓ(1) = 0; I_p = ℓ(p−2)
(Fermat inverse), L_h = ℓ(h), h = (p−1)/κ (coset test), M = (a+1)(a+2)/2, and the κ-th-root
product count T = Σ_{q | κ} T_q (primes with multiplicity), with

  T_q = [e_q > 1](ℓ(e_q−1) + 1) + [S_q ≥ 2]·( ℓ(q−1) + [e_q > 1] + ℓ(q)(S_q−1)(S_q−2)/2 + 2S_q − 3 ).

For κ = 3 (ℓ(3) = 2, ℓ(2) = 1): T = [e > 1](ℓ(e−1)+1) + [S ≥ 2]((S−1)(S−2) + 2S − 2 + [e > 1]),
so T ≤ 2b + S² + 2, where p−1 = 3^S·Q. Values: T = 0 at p = 7, 2 at 13 and 19, 5 at 37,
9 at 109, 12 at 163, 45 at 2³¹−1, 87 at 2⁶¹−1.

**Macros (whole circuit U)** (`closed_form_macros`, `closed_form_products_poly`):

  #add_product = 2n_F + 2M(T + ℓ(u)),
  power mode:   n_F = (a⁴ + 4a³ + 14a² + 17a + 4)/2 + I_p(2a² + 2a) + L_h(a² + 5a + 2),
  general mode: n_F = (4a⁴ + 16a³ + 53a² + 71a + 18)/6 + I_p(3a² + 5a) + L_h(a² + 5a + 2),
  #add_scaled = 2(M + a) + 2M(κ−1) + M   (general mode: 2(M + 2a) + 2M(κ−1) + M).

Breakdown of n_F (power mode): (a+1) first dependencies on a+1 columns in F_p^a, each
a³/2 + a² + 5a/2 + 2aI_p products (the κ = 2 count); 2L_h per coset-flag computation for the M
δ's and a ζ's; M for bd = β_{cos δ}δ; aM for the v's; a for za = ζα_{cos ζ}; a(a−1)/2 for the
back substitution; 2M−1 for the weights. General mode adds Σ_{n=1}^{a+1} fd(a, n) (the stop-test
eliminations; fd(a, n) = n(n+1) + (a−1)n(n−1)/2 + 2nI_p for n ≤ a) and one weight product. Copy
stage: per column T + ℓ(u), computed and uncomputed; the κ−1 root candidates are `add_scaled`
by the constants ω^t.

**Toffoli (exact; `closed_form_toffoli`)**:

  T_CCX = (40b²+2b)·#add_product + Σ_coeff #add_scaled(coeff)·H_coeff
          + 2·[(a+1)·fd_ccx(a, a+1) + (M+a)(κ−1)λ_b + Σ_{k=0}^{a}(and(a+1−k) + 1) + b·a(a+1)/2]
          + 2M·[Σ_{q: S_q ≥ 2}(S_q−1)(q−1)λ_b + 5b(κ−1)],

with λ_b = 2b−3 (b ≥ 3, the AND ladder of an equality test), H_coeff the `add_scaled` CCX count
of `formula_counts` (it depends on the constant: −1, 1 and ω^t occur), fd_ccx and and(n) as in
the κ = 2 report, and 5b(κ−1) the comparators (two Cuccaro adders, 4b) and Fredkin swaps (b) of
the least-root step. (General mode: replace the stop and τ-select terms by
Σ_{n=1}^{a+1} fd_ccx(a, n) + (a+1) + b·a(a+1).) Hence, as at κ = 2,

  **T_CCX = 40a⁴b² + O(a³b² + a²b³ + a²(T + ℓ(u))b²)**, total gates O(a⁴b² + a²b³ + a²Tb²)
  (each product ≤ 158b² + 46b − 4 gates), for fixed κ.

**Qubits (exact; `closed_form_qubits`)**, power mode:

  Q = b(5a³/2 + 11a² + 37a/2 + 10) + (3a³ + (κ+6)a² + (5κ+9)a + 2κ + 20)/2 + max(0, b−2, a−1)
      + b·max(1, I_p, L_h, W) + Σ_{q: S_q ≥ 2}(S_q−1)(q−1) + (κ−1),

where W = Σ_q W_q + κ + ℓ(u) is the copy-stage pool demand (W_q = the T_q registers plus the
2(S_q−1)−1 constant-multiplier registers), so Q = (5/2)a³b + O(a²b + a³ + b·(I_p + T)). At
(p, a) = (7, 1): 126 + 31 + 1 + 9 + 2 = 169.

All three closed forms (and the polynomial form of #add_product) equal the generator on all 100
rows of `run.json` (κ = 3; p ∈ {7, 13, 19, 37, 109, 163, 1009, 65539, 2³¹−1, 2⁶¹−1},
a ∈ {1, 2, 3, 4, 8}, both modes), and `test_closed_forms` keeps 15 rows including κ = 2, 4 and
d = 9 (u = 7). The program-level counts equal the length of the emitted gate list
(`test_emitted_counts_equal_program_counts`).

Selected rows (κ = 3, d = 3, u = 1; "add_p" = #add_product):

| p | b | a | M | mode | I_p | L_h | T | add_p | CCX | all gates | qubits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 3 | 1 | 3 | power | 3 | 1 | 0 | 80 | 32 380 | 135 024 | 169 |
| 7 | 3 | 1 | 3 | general | 3 | 1 | 0 | 118 | 46 590 | 194 438 | 211 |
| 7 | 3 | 2 | 6 | power | 3 | 1 | 0 | 246 | 96 434 | 402 726 | 412 |
| 7 | 3 | 2 | 6 | general | 3 | 1 | 0 | 352 | 135 964 | 568 040 | 550 |
| 13 | 4 | 2 | 6 | power | 5 | 2 | 2 | 350 | 237 480 | 945 140 | 535 |
| 109 | 7 | 2 | 6 | power | 10 | 6 | 9 | 682 | 1 376 082 | 5 307 550 | 960 |
| 109 | 7 | 8 | 45 | power | 10 | 6 | 9 | 12 142 | 2.42·10^7 | 9.39·10^7 | 16 277 |
| 65539 | 17 | 2 | 6 | power | 17 | 21 | 23 | 1 498 | 1.75·10^7 | 6.14·10^7 | 2 432 |
| 2³¹−1 | 31 | 2 | 6 | power | 59 | 43 | 45 | 3 474 | 1.34·10^8 | 5.22·10^8 | 5 370 |
| 2⁶¹−1 | 61 | 1 | 3 | power | 119 | 88 | 87 | 2 922 | 4.36·10^8 | 1.69·10^9 | 9 915 |
| 2⁶¹−1 | 61 | 2 | 6 | power | 119 | 88 | 87 | 6 858 | 1.02·10^9 | 3.96·10^9 | 14 160 |
| 2⁶¹−1 | 61 | 2 | 6 | general | 119 | 88 | 87 | 9 284 | 1.39·10^9 | 5.36·10^9 | 16 618 |
| 2⁶¹−1 | 61 | 8 | 45 | power | 119 | 88 | 87 | 67 938 | 1.01·10^10 | 3.93·10^10 | 139 149 |

Lemma 4′ saves 26–32% of the products against the general stop test at these rows, and 25%
asymptotically (the a⁴ coefficients of n_F are 1/2 and 2/3). At the same p and a the κ = 3 circuit costs about the
same as the κ = 2 one (e.g. 2⁶¹−1, a = 2: 6 858 products against 8 186 for the κ = 2 module;
L_h = ℓ((p−1)/3) is smaller than ℓ((p−1)/2) there, and the extra bd and za products are few).

## 4. Checks

Simulator: `BitSim` (exact bit-sliced basis-state simulation; the circuit is a permutation, so
basis inputs suffice). References: `canonical_witness_kappa` (definition level, paper-faithful
stop test, brute-force least root) and `canonical_witness_kappa_batch` (vectorised, also with the
paper-faithful stop test); they agree on all inputs at (7, 1), (13, 1) and (13, 1, d = 9), and on
structured samples at (7, 2), (13, 2), (7, 3) (κ = 3), (41, 2) (κ = 4) and (211, 1) (κ = 5), where
every witness passes `check_witness` and has x_{i*} = 1 and y' = e_K
(`test_definition_equals_batch_reference`). At κ = 2 the weights equal those of the κ = 2
module's reference on all inputs at (3, 2) and on samples at (5, 2), (7, 2), (13, 3)
(`test_kappa2_weights_match_k2`). The circuit is also compared with the definition-level
reference directly (`test_circuit_equals_definition_reference`).

For every input the circuit check asserts: S = the canonical witness (batched reference);
S canonical (< p); every input wire restored; every workspace wire 0; s ≠ 0;
Σ s_i^d λ_i = 0.

**Exhaustive [proof-by-computation], all p^{aM} canonical inputs, all checks pass** (`run.json`):

| κ | p | a | d | u | mode | inputs | gates | qubits | K = 0, 1 | sim |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 7 | 1 | 3 | 1 | power | 343 | 135 024 | 169 | 175, 168 | 0.146 s |
| 3 | 13 | 1 | 3 | 1 | power | 2 197 | 340 106 | 223 | 949, 1 248 | 0.359 s |
| 3 | 19 | 1 | 3 | 1 | power | 6 859 | 575 146 | 278 | 2 755, 4 104 | 0.616 s |
| 3 | 31 | 1 | 3 | 1 | power | 29 791 | 783 582 | 281 | 11 191, 18 600 | 1.114 s |
| 3 | 37 | 1 | 3 | 1 | power | 50 653 | 1 082 474 | 345 | 18 685, 31 968 | 1.827 s |
| 3 | 43 | 1 | 3 | 1 | power | 79 507 | 1 127 568 | 331 | 28 939, 50 568 | 2.264 s |
| 3 | 61 | 1 | 3 | 1 | power | 226 981 | 1 276 878 | 343 | 80 581, 146 400 | 4.262 s |
| 3 | 67 | 1 | 3 | 1 | power | 300 763 | 1 726 386 | 395 | 106 195, 194 568 | 7.036 s |
| 3 | 73 | 1 | 3 | 1 | power | 389 017 | 1 682 174 | 397 | 136 729, 252 288 | 6.773 s |
| 3 | 79 | 1 | 3 | 1 | power | 493 039 | 1 820 652 | 395 | 172 615, 320 424 | 10.203 s |
| 3 | 97 | 1 | 3 | 1 | power | 912 673 | 1 799 724 | 409 | 316 705, 595 968 | 14.842 s |
| 3 | 103 | 1 | 3 | 1 | power | 1 092 727 | 1 957 774 | 402 | 378 319, 714 408 | 18.594 s |
| 3 | 109 | 1 | 3 | 1 | power | 1 295 029 | 2 110 606 | 441 | 447 445, 847 584 | 33.199 s |
| 3 | 7 | 1 | 9 | 1 | power | 343 | 135 024 | 169 | 175, 168 | 0.124 s |
| 3 | 13 | 1 | 9 | 3 | power | 2 197 | 371 114 | 231 | 949, 1 248 | 0.309 s |
| 3 | 31 | 1 | 9 | 7 | power | 29 791 | 881 886 | 301 | 11 191, 18 600 | 1.011 s |
| 3 | 37 | 1 | 15 | 5 | power | 50 653 | 1 181 330 | 363 | 18 685, 31 968 | 1.714 s |
| 3 | 7 | 1 | 3 | 1 | general | 343 | 194 438 | 211 | 175, 168 | 0.129 s |
| 3 | 13 | 1 | 3 | 1 | general | 2 197 | 481 518 | 278 | 949, 1 248 | 0.428 s |
| 3 | 19 | 1 | 3 | 1 | general | 6 859 | 788 680 | 346 | 2 755, 4 104 | 0.642 s |
| 3 | 31 | 1 | 3 | 1 | general | 29 791 | 1 073 324 | 349 | 11 191, 18 600 | 1.202 s |
| 3 | 37 | 1 | 3 | 1 | general | 50 653 | 1 470 582 | 426 | 18 685, 31 968 | 2.151 s |
| 2 | 3 | 1 | 2 | 1 | power | 27 | 33 246 | 116 | 21, 6 | 0.037 s |
| 2 | 5 | 1 | 2 | 1 | power | 125 | 123 930 | 168 | 85, 40 | 0.104 s |
| 2 | 7 | 1 | 2 | 1 | power | 343 | 165 396 | 164 | 217, 126 | 0.136 s |
| 2 | 11 | 1 | 2 | 1 | power | 1 331 | 355 486 | 214 | 781, 550 | 0.295 s |
| 2 | 13 | 1 | 2 | 1 | power | 2 197 | 391 728 | 223 | 1 261, 936 | 0.297 s |
| 4 | 41 | 1 | 4 | 1 | power | 68 921 | 1 433 630 | 442 | 19 721, 49 200 | 2.456 s |
| 4 | 61 | 1 | 4 | 1 | power | 226 981 | 1 722 978 | 416 | 62 281, 164 700 | 6.525 s |
| 4 | 73 | 1 | 4 | 1 | power | 389 017 | 2 181 166 | 523 | 105 193, 283 824 | 15.695 s |

(30 rows; p = 19, 37, 109 have S_3 = 2, 2, 3, so the AMM rounds are exercised; p = 41, 73 have
S_2 = 3.)

**All row spaces at (p, a) = (7, 2), κ = 3 [proof-by-computation on the representatives;
covers every input of the DEFINITION via Lemma 5, not every input of the circuit]**
(`rref_check`, `rref_p7_a2.json`): the circuit (402 726 gates, 412 qubits) was run on one
representative (the RREF, padded with a zero row) of each of the 6 884 860 subspaces of F_7^6 of
dimension ≤ 2, and every check passed (47 s; stop rounds K = 0, 1, 2: 1 620 496, 2 690 492,
2 573 872). By Lemma 5 the canonical witness of each of the 7^12 ≈ 1.4·10^10 inputs equals that of
its representative; the circuit itself is not proved row-space invariant, so on non-representative
inputs at (7, 2) it is checked only on the samples below. All 7^12 inputs were not run (about a
day at this simulator's speed).

**Sampled [sampled], 8 192 structured inputs each** (`structured_inputs`, columns random, zero,
multiples or combinations of earlier ones, a quarter in a random lower-rank subspace; every K
occurs): κ = 3 at (p, a) = (7, 2), (13, 2), (19, 2), (31, 2), (37, 2), (43, 2), (7, 2, d = 9),
(13, 2, d = 9, u = 3), (7, 3), (13, 3), (19, 3), (7, 4), (13, 4), (7, 5), and general mode at
(7, 2), (13, 3); κ = 4 at (41, 2), (61, 2); κ = 5 at (211, 1), (211, 2); κ = 2 at (5, 2), (7, 2),
(5, 3). All pass. K = a occurs 13–1 036 times per row (13 at (7, 5)).

**Root circuit, exhaustive [proof-by-computation]** (`root_check`: the copy stage alone on every
x ∈ P ∪ {0}; output ρ(x)^u with ρ the brute-force least root; x restored, workspace 0):
κ = 3 at p ∈ {7, 13, 19, 37, 109, 163, 487, 1459} (S_3 up to 6), and with u > 1 at (13, 9),
(31, 9); κ = 4 at p ∈ {41, 97, 193} (S_2 up to 6, two square-root chains); κ = 5 at 211;
κ = 6 at {13, 37, 1009} (a square root then a cube root); κ = 10 at 31. All pass.

**Mutations (the checks are not vacuous)** (`test_*mutations_detected`): changing α_2 at (7, 2)
or α_1 at (13, 2), β_1 or β_2 at (7, 1), the sign of the τ term at (7, 2), the sign of the output
`add_scaled` at (7, 1), or skipping the least-root normalisation at (13, 1) and (19, 1); dropping
the first, middle or 97th-percentile CCX, the 99th-percentile CX or the first X of F, or the last
multiply-accumulate of F, at (7, 1) exhaustively: every mutant fails. **Equivalent mutant
(expected):** in general mode, flipping the sign of the y' term is undetectable exhaustively at
(7, 1), (13, 1) and on 2 048 samples at (7, 2) (`test_lemma4prime_equivalent_mutant_general_mode`),
because y'_{<K} = 0 on every input (Lemma 4′). This is the κ = 3 analogue of the κ = 2 report's
surviving mutants, which led to its Lemma 4.

**Lemma 4′ on the references** (`test_lemma4prime_on_references`, and a larger run in §1).

**Structure.** No gate or macro of U targets an input wire; macros of C target only S or pool
registers; CX/CCX of C never target an x register; X gates of C on x registers come in pairs
(`test_inputs_never_targeted_and_copy_stage_footprint`). κ_d = 1 and p ∈ E_2(κ_d) are refused
(`ValueError`), e.g. (13, d = 6), (5, d = 4), (11, d = 5).

**Exceptional sets reproduced.** The contraction search returns None exactly at
E_2(4) ∩ [5, 200) = {5, 13, 17, 29, 37, 53}, E_2(5) ∩ [11, 400) = {11, 31, 41, 61, 71, 101, 131, 151,
181} and E_2(6) ∩ [7, 1100) = 53 primes, largest 859, as quoted in main.tex (`prop:decoupled-sde`),
and finds a contraction at every p ≡ 1 (mod κ) below 400 for κ = 2, 3. (An independent finite
recomputation of those sets; not a proof for larger p.)

Commands:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde_k3.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde_k3.py -k slow
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_coherent_sde_kappa --out research/audits/reviews/2026-11-04-rees-coherent-sde-k3/run.json   # ~6 min, log run.log
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_coherent_sde_kappa --rref 7,2,3 --out research/audits/reviews/2026-11-04-rees-coherent-sde-k3/rref_p7_a2.json   # ~1 min
```

## 5. What this closes and what it does not

**Closes (every grade with p ∉ E_2(κ_d)).** At every grade d with κ = κ_d = gcd(d, p−1) ≥ 2
and p ∉ E_2(κ), the diagonal-equation solve no longer needs a mid-circuit measurement and
classical feed-forward: for fixed κ, a permutation circuit of 40a⁴b² + O(a³b² + a²b³ + a²Tb²)
Toffoli gates and (5/2)a³b + O(a²b + a³ + b(I_p + T)) qubits maps the labels to the canonical
witness with clean workspace, exactly, on every canonical input (given the macros; item 4 below).
Its constants are g, ω, the canonical contraction (α, β), u and the root parameters
(e_q, z_q = g^{Q_q}) — all column-independent, all a classical precomputation depending on
(p, κ, d) only. The Las Vegas κ-th roots of `prop:triangular-sde` become an oblivious AMM with
S_q − 1 fixed rounds per prime q | κ, and the stop test needs no second elimination (Lemma 4′).
For κ = 3 the canonical contraction was found at every p ≡ 1 (mod 3) below 400 (instantly),
and at 1009, 65539, 2³¹−1 and 2⁶¹−1 (§3 rows; at the last two by the unpruned lexicographic
scan, which raises instead of returning a non-least answer if its α scan is exhausted).

With `lem:coherent-linear-sde` (κ_d = 1), `lem:coherent-quadratic-sde` (κ_d = 2) and the
deferred-measurement argument of the κ = 1 report §5, the SDE solve is coherent, modulo wiring,
at every grade with κ_d ≤ 3 (E_2(2) = E_2(3) = ∅; the latter from AI-only reports, confirmed
here only for p < 400) and at every grade with κ_d ≥ 4 and p ∉ E_2(κ_d):

- **Class 3 (every instance, every prime p ≥ 5): yes, modulo wiring.** Grade 3 has κ_3 ∈ {1, 3}
  and grade 2 has κ_2 = 2. **n4(F_7):** grade 3 at a = 1, κ = 3 (this module, arity 3 against
  the generator's Chevalley–Warning arity κa+1 = 4: `rees_circuit_general.Config(filiform4(7))`
  reports dims (4, 2, 1) and arities {2: 5, 3: 4}; the exhaustive (7, 1, d = 3) row is exactly
  this grade's solver), and grade 2 at a = 2, κ = 2 (κ = 2 module, arity 6 against 5).
- **Class 4: every p except p ≡ 1 (mod 4) with p ∈ E_2(4) = {5, 13, 17, 29, 37, 53}.** Grade 4
  has κ_4 ∈ {2, 4}. So the class-four filiform algebra over F_7 (16 302 qubits per terminal
  sample in the generated circuits) is covered at every grade (κ_4 = 2, κ_3 = 3, κ_2 = 2);
  over F_5 it is not (κ_4 = 4 and 5 ∈ E_2(4)).
- **Class c in general: every grade iff p ∉ E_2(κ_d) for every d ≤ c with κ_d ≥ 4.** By
  `prop:decoupled-sde` this holds whenever p ≥ c^{c+1}; for κ ≤ 7 the exceptional sets are
  known exactly (main.tex; κ = 4, 5, 6 reproduced here).
- **Arity.** At κ = 3 the triangular arity (a+1)(a+2)/2 is at most the generator's 3a+1 for
  a ≤ 3 (3 < 4, 6 < 7, 10 = 10), so wiring it at κ = 3 does not raise any merge arity of these
  instances; in general (a+1)(a+2)/2 ≤ κa+1 iff a ≤ 2κ−3 (strictly below iff a < 2κ−3). (κ = 2 remains the case where the arity
  goes up for a ≥ 2; owner decision, as in the κ = 2 report.)

**Does not close.**

1. **Not wired into the generated receiver** (`rees_circuit_general.py` / `rees_circuit_sparse.py`
   still apply a classical s), and the n4(F_7) end-to-end simulation has not been rerun with a
   coherent witness. `coherent_receiver_implemented` stays false.
2. **Grades with p ∈ E_2(κ_d)** (e.g. grade 4 of the class-four filiform algebra over F_5) stay
   classical: no universal two-level contraction exists there, so the triangular solver does not
   apply; Chevalley–Warning or Schedules 1/3 would need their own coherent versions.
3. **The precomputation is a search.** The lexicographic DFS is exact but its worst-case cost is
   p^{O(κ)} (it took 378 s for all p ≡ 1 (mod 6) below 1100); no bound better than the paper's
   for finding a contraction is claimed, and the canonical choice adds nothing to existence.
4. **Correctness beyond the checked sets is [argued]**: Theorem 2, Lemmas 3–5 and the root proof
   are proved for all p, κ, a. The macro gate lists are proof-by-computation for p ≤ 13 only
   (I146 report). U itself is exhaustive for a = 1 at every p ≡ 1 (mod 3) up to 109 (and the
   κ = 2, 4 and d ∈ {9, 15} rows), on all row-space representatives at (7, 2), and sampled at
   a = 2..5 and for κ = 4, 5.
5. **Canonical inputs only**; padding words in the label registers are not claimed.
6. No QFT_p, oracle, noise, depth or layout work, and no asymptotic claim about the receiver. The
   triangular arity is not adopted by the paper's counts (`rem:triangular-scope`), and this module
   does not change Theorem `thm:main`, Table `tab:main-regimes` or any budget.
7. **The κ = 2 report still carries the wrong remark** (§5 item 1, §9 of
   `2026-11-04-rees-coherent-sde-k2.md`). This pass adds new files only; the integrator should add a
   pointer to §0 here.

## 6. Proposed paper text (not applied; main.tex untouched)

Placement: immediately after the artifact paragraph that follows `lem:coherent-quadratic-sde`
(main.tex, Section `sec:uniform-compilation`). Macros as in the paper (`\Fp`, `\file`).

```latex
\begin{lemma}[Coherent witness at fixed $\kappa_d$; AI-checked, pending human review]
\label{lem:coherent-power-sde}
Let $p$ be a prime, $a\ge1$, and $d$ with $\kappa=\kappa_d=\gcd(d,p-1)\ge2$ and $p\notin E_2(\kappa)$. Let $P=(\Fp^\times)^\kappa$, $h=(p-1)/\kappa$, $g$ the least integer whose image generates $\Fp^\times/P$, and $u\ge1$ with $u\,d/\kappa\equiv1\pmod h$. Let $(\alpha,\beta)$ be the lexicographically least $(\beta_1,\dots,\beta_{\kappa-1},\alpha_1,\dots,\alpha_{\kappa-1})\in\{0,\dots,p-1\}^{2\kappa-2}$ such that, with $\alpha_0=1$ and $\beta_0=0$, $(\alpha,\beta)$ is a universal two-level contraction in the normalisation of Proposition~\ref{prop:triangular-sde}. Run that proposition on $M=(a+1)(a+2)/2$ columns $\lambda_1,\dots,\lambda_M\in\Fp^a$ with this contraction, taking for $\delta$ in round $k$ the first linear dependency (as in Lemma~\ref{lem:coherent-linear-sde} with $e=1$) of the list $v_1,\dots,v_k$ followed by the columns of block $k$, and put $s_i=\rho(x_i)^u$, where $\rho(x)$ is the least $\kappa$-th root of $x$ in $\{0,\dots,p-1\}$. Then the stop test $v_{k+1}\in U_k$ of round $k$ holds if and only if every nonzero $\delta_i$ lies in $P$, if and only if $v_{k+1}=0$; moreover $s\ne0$ and $\sum_i s_i^d\lambda_i=0$. There is a circuit of $X$, CNOT, Toffoli and SWAP gates that maps $|\lambda\rangle|0\rangle|0\rangle$ to $|\lambda\rangle|s(\lambda)\rangle|0\rangle$ for every $\lambda$ with canonical coordinates. It uses $2n_F+2M\bigl(T+\ell(u)\bigr)$ modular multiply-accumulates, where $n_F=\tfrac12(a^4+4a^3+14a^2+17a+4)+(2a^2+2a)\,\ell(p-2)+(a^2+5a+2)\,\ell(h)$, $\ell$ is as in Lemma~\ref{lem:coherent-linear-sde}, and $T$ is the multiplication count of one $\kappa$-th root by an Adleman--Manders--Miller extraction with $S_q-1$ fixed rounds for each prime $q\mid\kappa$, where $q^{S_q}\,\|\,p-1$; for $\kappa=3$, $T\le2b+S_3^2+2$. For fixed $\kappa$ it uses $40a^4b^2+O(a^3b^2+a^2b^3+a^2Tb^2)$ Toffoli gates and $\tfrac52a^3b+O(a^2b+a^3+b\,\ell(p-2)+bT)$ qubits.
\end{lemma}

\begin{proof}[Proof sketch]
Suppose $v_{k+1}\in U_k$. The coefficients $(\beta_{\mathrm{cos}(\delta_i)}\delta_i)_i$, together with the coordinates of $v_{k+1}$ in $U_k$, form a linear relation of the round's list supported on its first $j^*+1$ entries, so it is a multiple of the first dependency; its entry at $j^*$ is $\beta_0\cdot1=0$, so it vanishes. Since $\beta_\nu\ne0$ for $\nu\ne0$ (the condition $1+\beta_\nu\in g^{-\nu}P\cup\{0\}$), every nonzero $\delta_i$ lies in $P$ and $v_{k+1}=0$; the converse is immediate. Proposition~\ref{prop:triangular-sde} gives $x\in(P\cup\{0\})^M$, $x\ne0$ and $\sum_ix_i\lambda_i=0$, and $\rho(x)^{ud}=x^{ud/\kappa}=x$ on $P\cup\{0\}$. The circuit is $F\cdot C\cdot F^{-1}$. $F$ runs all $a+1$ rounds obliviously: first dependencies by the machine of Lemma~\ref{lem:coherent-linear-sde}, coset flags by comparing $y^h$ with the powers of $g^h$, the constants $\alpha_{\mathrm{cos}(\zeta)}$ and $\beta_{\mathrm{cos}(\delta)}$ loaded under them, $v_{k+1}$, one-hot stop flags from the flags of the $\delta_i$, the coordinates selected under the stop flags, the back substitution and the weights. $C$ computes, per column, a $\kappa$-th root by one Adleman--Manders--Miller extraction per prime $q\mid\kappa$ with the fixed generator $g^{Q_q}$ of the $q$-Sylow subgroup (each round $q-1$ equality flags and multiplications by constants loaded under them), replaces it by the least of its $\kappa$ multiples by powers of $g^h$ (comparators and controlled swaps), raises it to the power $u$, adds the result into the output and uncomputes. $C$ leaves every wire of $F$ unchanged, so $F^{-1}$ clears the workspace.
\end{proof}

The artifact \file{theorems/rees_coherent_sde_kappa.py} (report \file{research/audits/reviews/2026-11-04-rees-coherent-sde-k3.md}; finite computation, AI-checked, pending human review) emits this circuit and checks it on every canonical input for $\kappa=3$, $a=1$ and every $p\equiv1\pmod3$ up to $109$, on one input for each row space at $\kappa=3$, $a=2$, $p=7$, and on samples for $a\le5$ and $\kappa\in\{2,4,5\}$; together with Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde} it makes the solve of~\eqref{eq:sde-target} coherent at every grade with $p\notin E_2(\kappa_d)$, in particular at every grade of every class-three instance (for example $\mathfrak n_4(\mathbb F_7)$, whose grade three has $\kappa_3=3$), and it is not wired into the generated circuits.
```

(The final sentence is the "one sentence". If the owner also adopts the correction of §0, the
sentence "Lemma 4 is special to κ = 2" has no counterpart in main.tex to remove: the lemma text of
`lem:coherent-quadratic-sde` makes no such claim.)

## 7. Claim gates

`research/reductions/rees_hsp_reduction.json` untouched. `STATUS` of the new module:
`coherent_receiver_implemented: False`, `general_sde_implemented: False`,
`wired_into_generated_receiver: False`, `independent_review: False` (the §10 review is an AI
subagent, not a human), `speedup_claim_allowed: False`; only `coherent_kappa3_sde_implemented`
and `coherent_fixed_kappa_sde_implemented` are True, scoped to p ∉ E_2(κ_d), the triangular
arity and canonical inputs. No claim of quantum advantage, of an asymptotic receiver cost or of a
native application follows.

## 8. Files

- `theorems/rees_coherent_sde_kappa.py` (new): `CoherentSDEKappa(p, a, d, stop="power"|"general")`,
  constants (`coset_generator`, `Cos`, `canonical_contraction` (pruned) /
  `_canonical_contraction_lazy` / `contraction_bruteforce`, `contraction_valid`, `root_params`,
  `kappa_constants`), references `canonical_witness_kappa`, `canonical_witness_kappa_batch`,
  `check_witness`, closed forms `closed_form_macros / _toffoli / _qubits / _products_poly`,
  `root_circuit` / `root_check`, `exhaustive_check(_chunked)`, `sampled_check`, `rref_check`,
  `count_row`, CLI `main`.
- `tests/test_rees_coherent_sde_k3.py` (new): 87 default tests (≈ 45 s), 27 more with REES_SLOW=1.
- `research/audits/reviews/2026-11-04-rees-coherent-sde-k3/run.json`, `run.log`,
  `rref_p7_a2.json`, `rref_p7_a2.log` (artifacts).
- This report. No existing file edited; nothing committed or pushed.

## 9. Next hard question

Wire the three coherent solvers into the merge and rerun one instance end to end: replace the
classical s of `rees_circuit_general.merge_ops` by the witness register, with the controlled
right translation x ↦ x·(−δ_s(σ(q))) (grade-j coordinates scaled by s^j), for n4(F_7) at grade-3
arity 3 (this module) and grade-2 arity 6 (κ = 2 module). Acceptance: the coherent pipeline's
reduced output equals ρ_{HZ/Z} on every positive-probability label tuple of the existing n4(F_7)
instances, with exact Z[ζ_7] state comparison. (Another agent is writing
`theorems/rees_circuit_coherent.py`; this pass did not touch it.) Separately: the grades with
p ∈ E_2(κ_d) (n5(F_5), grade 4) need a coherent solver that does not use a two-level contraction.

## 10. Independent review (AI subagent, unanchored)

A separate AI agent was given `prop:triangular-sde`, §0–§2 of this report and the code, but not
this session's check results. It wrote its own implementation of the definition from the report
text and its own validity checker and lexicographic search, and ran the circuit through `BitSim`
against its own reference: exhaustive at κ = 3, a = 1 for p = 7, 13, 19, 37 (power mode), p = 13
with d = 9 (u = 3), p = 19 with d = 15 (u = 5, both modes), p = 7 (general mode), and κ = 2 at
p = 7; sampled at κ = 3, a = 2..4 (up to 20 000 inputs at (7, 2)), κ = 4 (41, a = 1, 2), κ = 5
(211, a = 1, 2), κ = 6 (877, a = 1) and κ = 2 (11, a = 2): 0 mismatches, inputs restored,
workspace clean throughout. It tested Lemma 4′ on its own reference over every normalised
contraction at (p, a) = (7, 1), (13, 1), (19, 1) (exhaustive inputs; 2, 2 and 40 contractions),
on random and degenerate inputs at κ = 2..6, and in the paper's "first nonzero entry 1"
normalisation: no violation. It checked Lemma 5 on 1 200 random GL_a transforms, and the root
chain on every κ-th power for κ ∈ {3, 4, 5, 6, 8, 9, 15, 16, 25, 32} at primes up to 509 (S_2 up
to 8, u up to 139). Its own mutations (β, α, τ, output sign, least-root step) were detected; the
general-mode y′ sign mutation was not, as Lemma 4′ predicts.

Verdicts: Lemma 1, Theorem 2, Lemma 3, Lemma 4′ (and the correction of the κ = 2 report),
Lemma 5, the forward pass (one-hot F_k, garbage rounds, F_k toggles, constant loads, Bennett),
the root chain and the comparator are correct; no counterexample. Text fixes it asked for, all
applied: the module docstring still described the general stop test as the only one; two label
references in the code (Theorem 3 → 2, Lemma 6 → 5); §2's root round read as if r were not
updated in the last round; the "q-th root of a κ'-th power" step is now stated with its reason;
Lemma 3 now states the normalisation of a decoupled contraction and the independence of E_2 from
the choice of generator. It also noted that the κ = 2 report itself still carries the wrong remark
(§5 item 7 above). This is not human review.
