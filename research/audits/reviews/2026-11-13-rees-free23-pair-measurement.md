# free23 exit (ii): IS-type measurements on dependent pairs and generic triples (2026-11-13)

**Status: AI-checked, pending human review.** One AI session (Claude). The computations are exact up to
float round-off, and finite checks only falsify (TRAPS 7). Scripts and outputs are in
`research/audits/reviews/2026-11-13-rees-free23-pair-measurement/`. No other file was edited.
Context: `2026-11-13-rees-free23-two-copy.md` (all of it), `2026-11-12-rees-entangled-twist-impossibility.md`
§1, §4, §8, §11, and the Ivanyos–Santha text `2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`
(Thm 3, Thm 5 and its §5 proof, Prop 7 and its §4.1 proof, Cor 6, Cor 8).

## Verdict

* **Exit (ii): a CONDITIONAL constant-copy candidate (§9, added in the follow-up).** It is a three-level aligned
  merge of generic triples, with public 2-D cubic and quadratic phase corrections.
  * It turns 54 labelled copies into one Fourier sample z obeying a linear equation in (e, e_3).
  * The exact simulation, with true QFT distributions, recovered the hidden (line of v_1, e_3) uniquely from three such
    equations in 12/12 trials at p = 11, 13 and 17.
  * The curl condition does **not** block the aligned merge for m ≥ 5–6 triples (REFUTED as an obstruction on all
    tested instances). It does block one or two triples on every tested generic instance.
  * Open: a proof that public level-2 weights exist with probability bounded below (UNKNOWN), and a poly(log p) solver
    for them (CONDITIONAL; exhaustive search was used here).
* **First-pass finding (still true for what it covers).** Every *line-merge* IS-type primitive and every pair primitive
  tested falls into one of two cases. Either it loses all information about the generic line of v_1, or it turns the
  information into samples from a known hard problem (dihedral hidden-shift samples, or a hidden-direction problem).
* **Task 1. IS Cor 8 needs one fil4 quotient.**
  * The IS merge (Thm 5) shifts each copy's one-variable register x_i by δ_i·x and measures the residuals. The
    weights must solve a *d-th power* diagonal relation Σ δ_i^d Y^i_d = 0 among the known top-degree labels.
  * All copies must share one chart F_p ⋉ F_p^m. For free23 this means labels on one line F_pλ, i.e. copies of one
    quotient fil4_λ = G/ker λ.
  * With O(1) such copies, IS solves free23 in poly time (§1, PROVED given IS). Uniform labels supply such copies only
    after Θ(√p) samples.
* **Task 2. Pairs (λ, cλ) with c ≠ −1, exact at p = 5, 7, and at p = 11 for c = 2.**
  * **One merge is lossless.** It measures S = x_1 + c·x_2, i.e. IS weights (−c, 1). The off-block norm is ≤ 4e−20.
    This holds for all k copies (Lemma P, PROVED).
  * **Every other merge direction destroys all generic-line information** (post-merge χ = 0 exactly). That includes
    IS's own cubic-cancelling weights d³ = −c (PROVED).
  * **Fourier sampling after the lossless merge decays** like 1/p, like plain Fourier sampling:
    MI = 0.100 / 0.081 / 0.056 bits at p = 5 / 7 / 11.
  * **A Kuperberg-type measurement does not decay.** Measure the two-point orbit, then the X basis:
    MI = 0.286 / 0.326 / 0.366 bits, against χ = 0.640 / 0.735 / 0.826.
  * **Why it works (Lemma K, PROVED, checked exactly).** After averaging over the nuisance e_3, the state is a direct sum
    of pure qubits (|x_0+u⟩ + ω^{βK(u)+K_0(u)}|x_0−u⟩)/√2. Here β is the slope of the line of v_1, and K, K_0 are known.
    That is exactly a dihedral hidden-shift (D_p HSP) sample.
* **Acceptance test: formally passed, substantively failed.** MI stays bounded away from 0, so the brief's "usable"
  branch is met literally. But:
  * the output is a D_p-HSP sample, whose best known quantum processing is Kuperberg's 2^{O(√log p)} sieve (cited,
    not re-read);
  * each dependent pair itself costs Θ(√p) uniform copies, or a ZS(p,1) solve, which is ≡ ZS(p,2).
  So the pair primitive is **not** a poly(log p) route.
* **Triples (generic, pairwise independent labels).**
  * The lossless public merge S = Σ_i n_i x_i leaves a 2-D register. On it, the state is coherent only along a hidden
    direction φ(e), and [e] ↦ [φ(e)] is a bijection from the lines of v_1 onto P¹ (Lemma P(b), PROVED).
  * Every public line merge loses everything except on ≤ 1 guessed line.
  * IS cubic cancellation holds on ≤ k lines for any public weights (Lemma S, PROVED; exact counts for p ≤ 13).
  * The numbers are in §6.
* **Structural reason binary relations are special (Lemma Q, PROVED).** Along a lossless merge direction s ∈ R_Λ, the
  phase's e_3-term is −½·e_3·(Σ_i s_i² λ_i)([e,z])·t². For three pairwise independent labels it vanishes iff s is
  binary up to scale, and for pairs iff c = −1. Binary relations satisfy all the power-sum conditions Σ s_i^j λ_i = 0
  (j = 1, 2) at once.
* **Claim gates stay false:** "exit (ii) closed" and "a poly-time non-binary merge exists" (both pending (b)–(c) of
  §9 and human review); "Kuperberg gives a poly route". "Joint measurements cannot help" is now REFUTED in substance
  by §9 on finite instances; it was never a gate to set true.

## 1. Task 1: what IS Cor 8 applies (from the source)

* **Prop 7 (§4.1).**
  * G = F_p ⋉_B F_p^m has class d, and the hidden H ≰ N = F_p^m has order p.
  * In the chart g = n·B^x (N on the left), a coset uH, u ∈ N, is the level set {(x, u + v(x))}.
  * v(x) has degree ≤ d (Faulhaber), so a coset state is a random level-set state Σ_x |x⟩|u + v(x)⟩.
* **Front end (§5).** QFT over N on the second register. Measure y (uniform). What is left is the pure state
  |ψ_Y⟩ = Σ_x ω^{Σ_j x^j Σ_k Y_jk η_k}|x⟩, with Y known and η hidden. The u-dependence is a global phase.
* **Degree reduction (§5).**
  * Take n states whose phase has degree d.
  * Find δ ≠ 0 with Σ_i δ_i^d Y^i_{dk} = 0 for all k. This is SDE(F_p, n, ℓ, d), solved by Thm 3.
  * Adjoin Σ_x |x⟩, map x_i ↦ x_i − δ_i x, and measure x_1..x_n. This is the same as measuring the coset of the line
    F_pδ in F_p^n.
  * The result has degree ≤ d−1 with known coefficients, and it is nonzero with probability ≥ (p−1)/p.
* **Recursion.**
  * Iterate down to degree 1 (n^{d−1} states), then apply the inverse QFT. This gives one linear equation Σ z_k η_k
    with z known.
  * Substitute and repeat ℓ times. The total is ℓ·n^{d−1} states, with failure probability ℓ·n^{d−1}/p (as stated in
    the source).
* **What it needs.**
  1. All copies are in **one** chart (same N, same x).
  2. The weights solve **d-th-power** relations among the known top-degree labels.
  3. Hidden parameters are fixed across copies and solved as unknowns. Nothing is averaged, so η_c-type parameters
     simply become further unknowns.

**Translation to free23 (PROVED, §2).** A copy with label λ ≠ 0 is a copy of fil4_λ = G/ker λ, which has IS form with
N_λ = exp(F_p g_0 + γ_2)/ker λ. IS Cor 8 therefore solves free23 from O(1) copies **whose labels lie on one line**
F_pλ. The cubic relation is Σ δ_i³ c_i = 0 for labels c_iλ. Its output H̄ ≤ fil4_λ gives K̄ and the line of v_1.

Uniform labels on F_p² hit a common line only after Θ(√p) copies (birthday over p+1 classes), or Θ(p) copies for a
chosen quotient. Manufacturing a dependent pair by binary merges is a ZS(p,1) instance: (Σ_S λ_i) ∥ λ_j iff
Σ_{i∈S} det(λ_i, λ_j) = 0. By the 11-12 note, ZS(p,1) is equivalent to ZS(p,2) up to polynomial factors.

## 2. IS normal form of a labelled free23 copy (PROVED; checked exactly)

**Setup.**
* Fix λ ≠ 0. Take g_0 = (λ_w, −λ_u) ∈ V/D, so that λ([g_0,z]) = 0, and take x' ∉ F_p g_0.
* Define n_λ = λ([x',z]) and f_λ(v) = λ([v,z])/n_λ, so that f(g_0) = 0 and f(x') = 1.
* Write η' = η/f(e) = x' + β g_0 + e_3' z + η_c'. Here β = β_λ(e) is the chart slope of the line [e], e_3' = e_3/f(e)
  and η_c' = η_c/f(e).

**The phase.** If f(e) ≠ 0 (all lines but [g_0]), the IS front-end block y = (j,k) is the pure state ψ_y(x) = ω^{P_y(x)}/√p,
with

P_y(x) = −ỹ(ν(x)), ν(x) = log(exp(xη')·exp(−x x')), ỹ(ν) = j·ν_{g_0} + k·ν_z + λ(ν_{γ_3}).

* P is **affine-linear in (β, e_3', η_c')** with known coefficients. This is IS's |ψ_Y⟩ with ℓ = 4.
* It has degree ≤ 3 and no constant term.
* a_3 = κ_λ·β with κ_λ = det(g_0,x')·λ([x',z])/6.
* η_c enters only a_1, as −λ(η_c')·x.
* The e_3-part of a_2 is −½·n_λ·e_3'.

*Proof.* Use BCH at class 3. The cubic term of ν is −(x³/12)(2β[x',[g_0,x']] + β²[g_0,[g_0,x']]), and
λ([g_0,[g_0,x']]) = det(g_0,x')·λ([g_0,z]) = 0. The quadratic γ_3-term is −½x²e_3'[z,x']. η_c' is central. A base point
u ∈ N_λ gives a global phase, because [N_λ, N_λ] ⊂ ker λ and H is a complement of N_λ. ∎

For f(e) = 0, the block states are diagonal: uniform on {x_0 : ỹ(Ad_{s(x_0)}η) = 0}.

**Checks.**
* `isbasis.out`: the formula blocks equal W†σW for the dense V-picture σ of `hpgp2_free23.py`, to ≤ 1e−17 (four
  labels, 47–48 sampled η each, 11–16 of them with H ⊂ N_λ). W is the IS basis P_jk|x x'⟩ inside ℂ[V].
* `lemma_s.out`: every identity above holds exactly over F_p, with 0 failures in 1800 / 1800 / 900 sampled η at
  p = 5 / 7 / 11, and 0 failures in 1200 / 1200 / 600 checks of the e_3-term.
* **The front end is lossless.** Its blocks are the two-copy report's W_λ blocks. The pair χ values are reproduced:
  0.6362 / 2.2141 (c ≠ −1) and 0.4136 / 2.2711 (c = −1). The independent pair is 0 (`pairctl_5.out`).

## 3. Which merges are lossless (Lemmas P and K)

**Natural coordinates.** Put x̃_i = n_i x_i = λ_i([π(g_i), z]) and f̃_i(e) = λ_i([e,z]). Take k labelled copies,
relation space R_Λ, and generic H (all f̃_i(e) ≠ 0).

**Lemma P (PROVED).** After the front end and the η_c-average, the state is block-diagonal on the cosets of

L(e) = {(s_i f̃_i(e))_i : s ∈ R_Λ}, and L(e) ⊂ {Δ : Σ_i Δ_i = 0}.

So measuring **S = Σ_i x̃_i is lossless for every hypothesis.** It is public, and costs O(k log² p) gates after the
front ends.

*Proof.* The η_c-phase is −(Σ_i (x̃_i/f̃_i(e))·λ_i)(η_c). Averaging uniform η_c ∈ γ_3 keeps the (x, x') coherence iff
((x̃_i − x̃'_i)/f̃_i(e))_i ∈ R_Λ. Moreover Σ_i s_i f̃_i(e) = (Σ s_i λ_i)([e,z]) = 0. ∎

**(a) Dependent pair (λ, cλ).**
* L(e) = F_p(1, −1) in x̃, i.e. the line x_1 = r − c·x_2. This direction is public.
* **Any other line merge d ≠ −c** meets each coherence class in one point. The post-measurement block is then diagonal
  with flat entries, hence H-independent for generic lines, so χ = 0 (PROVED).
* In particular, IS's cubic step d³ = −c destroys everything unless c² = 1.
* The numbers agree: post-merge χ(HYP1g) = 0.0000 for every d ≠ −c at p = 5, 7, 11.

**(b) Generic triple.**
* R_Λ = F_p s with all s_i ≠ 0. The map e ↦ (s_i f̃_i(e))_i is a linear isomorphism F_p² → S^⊥: a kernel vector would
  lie on all three lines [g_0^i].
* So the coherence direction [φ(e)] of the post-S plane runs **bijectively** over P¹ as the line of v_1 varies. The
  information *is* the hidden direction.
* A public line merge inside S^⊥ is lossless only for the one line [e] with [φ(e)] = [δ]. For every other line it gives
  an H-independent state, so χ ≤ h(1/n_gen) = O(log p/p) (PROVED).
* The plane merge with ℓ ∝ (n_i) is the S measurement, so it is lossless.

**Lemma Q (power sums; PROVED from §2).**
* Along a lossless direction Δx_i = t·s_i f_i(e), the e_3-dependent t²-coefficient is −½·e_3·(Σ_i s_i² λ_i)([e,z]).
* For a pair, s = (−c, 1) gives c(c+1)λ, which vanishes iff c = −1.
* For three pairwise independent labels, s^{∘2} ∈ R_Λ = F_p s forces s_i ∈ {0, μ}, i.e. binary up to scale.
* So **only binary relations remove e_3 together with η_c.** This is the mechanism behind Theorem R's binary condition,
  seen from the IS side.

**Lemma K (dependent pair = dihedral qubits; PROVED, checked exactly).**
* Take c ∉ {0, −1} and HYP1 (nuisances e_3', η_c'), after measuring S.
* The e_3'-phase is e_3'(αx² + γx + const), with α = −½n·c(c+1) ≠ 0 and γ known.
* Averaging over e_3' keeps coherence only inside the orbits {x, 2x_0 − x}, where x_0 = −γ/(2α) is known.
* On an orbit, the relative phase Q(x_0+u) − Q(x_0−u) is e_3'-free. It is odd in u and affine in β. So each block is
  the **pure** qubit

  (|x_0+u⟩ + ω^{βK(u) + K_0(u)}|x_0−u⟩)/√2, with K and K_0 known.

* `kuperberg_check.out` checks all of this exactly:
  * every block, every c, at p = 5 and 7: 0 support, centre, modulus or linearity failures;
  * K ≠ 0 on 200/250 orbits at p = 5 and 882/1029 at p = 7, i.e. a fraction (p−1)/p.
* These are exactly the input states of the dihedral hidden-shift problem in Z_p, with hidden shift β.

## 4. Lemma S: IS degree reduction across fil4 quotients (PROVED; exact counts)

**Lemma S.** Take k copies with pairwise non-proportional labels, any charts, and any public weights δ ≠ 0. The IS
top-degree cancellation Σ_i δ_i³ κ_i β_i(e) = 0 holds for at most k lines [e]. With per-copy public cubic phases added,
it holds for at most k+1 lines.

*Proof.*
* β_i = h_i/f_i, with h_i(g_0^i) ≠ 0. Multiply by Π f_j. The result F(e) = Σ_i δ_i³ κ_i h_i Π_{j≠i} f_j is a binary
  form of degree k.
* At e = g_0^{i_0}, where δ_{i_0} ≠ 0, only the i_0 term survives, and it is nonzero. So F ≢ 0, and F has ≤ k roots.
* A public phase τ_i x_i³ shifts a_3 by a constant. A sum of Möbius functions with distinct poles is never constant.
  ∎

**Corollary.**
* When labels share quotients, the condition is H-independent iff, for each quotient Q, Σ_{i∈Q} δ_i³ c_i = 0 (and a
  public constant condition holds).
* So IS merges decompose into per-quotient merges; a cross-quotient relation never helps except on guess events of
  probability ≤ k/(p+1).

**Exact counts** (`lemma_s.out`, p = 5, 7, 11, 13): the maximum number of cancelling lines over all δ is 2 for k = 2
independent labels and 3 for generic triples. "All lines" occurs only for same-quotient pairs with −c a cube, and for
triples that contain such a pair.

## 5. Constructive attempts (Task 3)

| attempt | result | status |
|---|---|---|
| automorphism / dilation sending cλ to −λ while preserving H | Aut(free23) acts on γ_3 by det(A)·A. A label change needs T ≠ id_V on V, and then K̄ ∈ Fix(T) has probability ≤ 1/p (Lemma F of the 11-12 note). T = id_V forces the identity on γ_3. IS's x ↦ δx is a reparametrisation of the post-front-end register, not an automorphism. That is how IS escapes Lemma F, but only inside one chart (Lemma S). | PROVED obstruction (via Lemma F) |
| CG / QFT step isolating t ∈ R_Λ | It is the S measurement: lossless, public, O(k log² p) gates (Lemma P). For pairs it leaves a 1-D cubic state, the η_c-known single copy. This explains the two-copy report's spectral identity in substance: the merged state has no η_c. The unitary equivalence remains unproved. | PROVED (losslessness) |
| IS cubic step on a pair (d³ = −c) | destroys all generic information unless c = ±1 (§3(a)) | PROVED |
| Kuperberg-style sieve over dependent pairs | Lemma K makes each pair a D_p hidden-shift qubit in β, and Kuperberg's sieve then needs 2^{O(√log p)} qubits and time (Kuperberg 2005 / Regev 2004 / Kuperberg 2011, **cited from memory, not re-read**). Each qubit needs a dependent pair: Θ(√p) uniform copies, or a ZS(p,1) solve. The total is ≥ √p. | sieve CONDITIONAL on the citation; cost obstruction PROVED |
| generic triple: public line merges | lossless only for one guessed line (§3(b)) | PROVED |
| generic triple: public cubic phase cancelling the t³-coefficient along the hidden direction | Possible. C(e) = Σ κ_i s_i³ h_i f_i² is a public cubic form and φ is public, so Q_3 = −C∘φ^{−1} cancels it for every H at once. But the e_3-term of Lemma Q stays (non-binary s). The b-dependent t²-terms need ∇(P_3^{(e)} + Q_3)(φ(e)) = 0 for all e: 6 linear conditions on 4 coefficients, generically unsolvable. After cubic cancellation, Fourier on a quadratic chirp is flat. | follow-up (§9): no public Q for one generic triple in 11 of 12 random instances at p = 11, 13 (rank 5 on 5 unknowns). The exceptions are 1/12 at p = 13, 4/12 at p = 5 and 3/12 at p = 7; some of them have a binary relation (E3 holds). Blocked for m = 1 on the instances tested; not proved for all labels |
| aligned triples (A_j = φ_1φ_j^{−1}), then a weighted 2-D merge with Σ u_j² λ'_j = 0, λ'_j = Σ_i s_i^{(j)2} λ_i^{(j)} | This merge is public, and it cancels the e_3-terms (an SDE of degree 2 with m = 2, solvable by IS Prop 9). Follow-up (§9): together with a public 2-D cubic Q_3, it cancels the cubic and the base-point (b)-dependent t² terms for m ≥ 5–6 triples. A third level then gives a plane wave. | curl obstruction REFUTED on finite instances; algorithm CONDITIONAL (§9) |

## 6. Computations (Task 2)

Families:
* HYP1 = the line of v_1 (p+1 hypotheses).
* HYP1g = the generic lines only, excluding the public special lines [g_0(λ_i)], which are detectable but worth only
  O(log p/p) bits.
* HYP2 = the line K̄, and HYP2g its generic part.

MI is in bits, "succ" is the MAP success probability, the prior is 1/#hyp, and PGM is the pretty-good measurement
(not claimed efficient). Files: `pairs_5.out`, `pairs_7.out`, `pairs_11_c2.out`, `kuperberg_check*.out`, `json/`.

**Dependent pairs, HYP1g** (identical for every c ∉ {0, ±1}; c = 1 differs slightly):

| p | χ_2 | PGM MI / succ | S + Fourier MI / succ | 2-D Fourier MI | orbit + X MI / succ | best other merge, post χ | binary c = −1: χ = S+Fourier MI | prior |
|---|---|---|---|---|---|---|---|---|
| 5 | 0.6400 | 0.1443 / 0.328 | 0.1002 / 0.293 | 0.1002 | **0.2856** / 0.316 | 0 | 0.3715 | 0.200 |
| 7 | 0.7347 | 0.1261 / 0.248 | 0.0814 / 0.209 | 0.0814 | **0.3262** / 0.243 | 0 | 0.3438 | 0.143 |
| 11 (c=2) | 0.8264 | 0.0948 / 0.166 | 0.0564 / 0.130 | 0.0564 | **0.3661** / 0.165 | 0 | NOT computed | 0.091 |

* c = 1 (S + Fourier, HYP1g): 0.0794 at p = 5 and 0.0630 at p = 7. IS-cub coincides with S there.
* HYP2g, S + Fourier: 0.566 / 0.572 / 0.632. It is flat, but it is Weyl-sum likelihood information (§7).
* Holevo χ_2 at p = 11 (new; full families): HYP1 0.7938, HYP2 3.3937; mean S = 17.2972 = 5 log₂ 11.

**Triples at p = 5** (`triple_5_a.out`, `triple_5_b.out`, `triple_5_bin.out`). HYP1g has only 3 generic lines at
p = 5 (prior 1/3), so these are small-p falsification checks, not asymptotics. "Lossless plane" means measuring
S = Σ n_i x_i (plane ℓ ∝ n); its post-merge χ equals the full χ in all three cases, and the off-block norm is 0.

| labels | relation | χ HYP1 / HYP1g / HYP2 | PGM MI HYP1g | 3-D Fourier (F3) MI HYP1g | lossless plane + Fourier MI HYP1g | best line merge MI HYP1g (post χ) |
|---|---|---|---|---|---|---|
| (1,0),(0,1),(1,2) | generic | 0.6479 / 0.4997 / 2.2258 | 0.0977 | 0.0031 | 0.0165 (plane 111) | 0.0302 (0.2013) |
| (1,0),(0,1),(1,1) | generic, s = (1,1,−1) | 0.6362 / 0.5593 / 2.2141 | 0.1198 | 0.0031 | 0.0168 (plane 111) | 0.0302 |
| (1,0),(0,1),(4,4) | binary, s = (1,1,1) | 0.4136 / 0.2536 / 2.2711 | 0.0354 | 0.0031 | 0.0160 (plane 114) | 0.0292 |

* The χ values reproduce `multi_5.out` of the two-copy report (0.6479 / 2.2258).
* Every line merge other than the few lines on which one generic hypothesis stays coherent has post-merge
  χ(HYP1g) = 0, as Lemma P(b) predicts. The best line merges keep exactly one HYP1g line coherent.
* Plain Fourier sampling of the triple (F3) gives 0.003 bits, the same order as the brief's 0.013-bit single-copy
  baseline. After the lossless merge, Fourier gives 0.016 bits against χ ≈ 0.5.
* p = 7 triple: computed in the follow-up (§9.5). p = 11, c = 10 pair (a c-independence cross-check): NOT computed
  (stopped at the budget).

## 7. Barrier and what would settle it (Task 4)

1. **Inside IS's own method class, proved here.** Front end, then public line merges with power-relation weights,
   then recursion.
   * Lemma P: the only lossless merges are along L(e).
   * Lemma S: top-degree cancellation never crosses quotients except on ≤ k/(p+1) guess events.
   * Lemma Q: e_3 is removed together with η_c only by binary relations.
   * Together: a cross-quotient IS-type algorithm must guess the line of v_1 at some step, or use only binary
     relations, which is ZS (Theorem R).
   * This is a **model-bound** statement (CONDITIONAL on staying in this class). It is not a lower bound.
   * **Follow-up:** §9 leaves this class. It uses 2-D plane merges with public cubic/quadratic corrections that are
     polynomial identities in e, and it escapes the bound.
2. **Pairs reduce to the dihedral HSP** (Lemma K, PROVED). The best known algorithm is subexponential (Kuperberg; cited,
   not re-read). A poly(log p) algorithm for this pair primitive would therefore give poly-time hidden shift in Z_p on
   these qubit ensembles, which is a long-standing open problem. Producing the pairs already costs ≥ √p.
3. **Information-theoretic arguments cannot settle it.** χ_k > 0 for every k ≥ 3, and the single-pair MI stays
   Θ(1) (Lemma K).
4. **What would settle it.**
   * *Positive:* a poly(log p) measurement on the post-S triple plane (hidden direction φ(e), polynomial phases) whose
     outcomes give algebraic (linear) equations in e. **Found in the follow-up (§9)**, CONDITIONAL on (b)–(c) there.
   * *Negative:* a reduction from dihedral HSP, or from ZS, to the generic-triple problem. Or a proof that every
     measurement made of public QFTs, S-type merges and power-weighted line merges reduces to guess events or binary
     relations (an "SOT+IS" Theorem R).

**Next hard question (first pass; answered in §9).** For aligned generic triples (labels pairwise independent; triples aligned by A_j = φ_1φ_j^{−1}),
can the second-level merge with Σ_j u_j² λ'_j = 0 cancel all t²-terms publicly? If yes, a third level cancels t¹, and
the result is a Kuperberg-free exit (ii) candidate. If no, the obstruction is the curl condition of §5.
* Next command: an exact check, at p = 5, of the curl condition ∇(P_3^{(e)} + Q_3)(φ(e)) = 0, and of the t²-coefficient
  of two aligned merged triples. It is about 30 lines on top of `lemma_s.py` and needs no density matrices.
* Expected artifact: `aligned_triples_5.out`.
* Acceptance test: a public cancelling choice exists for all e, or it does not.

## 8. Adversarial self-check

* **Is "Fourier MI → 0, so no evidence" honest?** No, and the report does not say it. The orbit + X measurement keeps
  Θ(1) bits. The verdict rests on two things instead: the cost of dependent pairs (≥ √p), and the D_p-HSP form of the
  output. The brief's acceptance test is too weak, because it does not price inference or pair production.
* **Lemma K could depend on the model of the nuisances.** HYP1 treats e_3 and η_c as uniform, which is right for
  uniform hard H. For HYP2 (e_3 known), the orbit decoherence disappears and the state is a 1-D cubic chirp. The HYP2g
  MI of 0.57–0.63 bits is likelihood information from cubic Weyl sums, and inverting it costs a search over p²
  hypotheses.
* **Chart dependence.** a_3 and C(e) depend on the chart choices (x'_i). Lemma S allows arbitrary charts and public
  cubic phases. Lemma P is chart-free (natural coordinates). Lemma K's orbit structure comes from the η_c- and
  e_3-averages, which are chart-free.
* **Special lines.** H ⊂ N_λ for e ∝ g_0(λ). These lines are public, give diagonal states, and were excluded in HYP1g.
  Including them adds the visible ≈ 0.02–0.06 bits in HYP1.
* **Numerics.** Rep-orbit reduction was checked (weights sum to p^{2k}, orbit maps verified on fresh samples to
  1e−18). The two-copy report's χ values are reproduced. The independent-pair control is exactly 0. p = 11 is a single
  c; the other c follow by Lemma K's c-independence, but they were NOT computed there.
* **Binary triple.** The binary triple's post-merge Fourier MI (0.016) is no larger than the generic one's. So Lemma Q
  (binary relations kill the e_3-term) is necessary for an IS-style cascade but not sufficient for one-shot Fourier
  extraction. Theorem R's binary route uses many copies and is not tested by this k = 3 run.
* **Citations.** Kuperberg/Regev sieve complexities are quoted from memory (TRAPS 10). Every statement that uses them
  is CONDITIONAL. The IS statements were read from the local source text.
* **Novelty.** Lemmas P, Q, S and K are direct calculations. A pair of fil4-quotient copies reducing to dihedral-type
  qubits is plausibly known in spirit (BCvD / IS literature). Priority is unchecked.

## 9. Follow-up (same day): aligned triples, the curl check, and an end-to-end three-level merge

**Status: AI-checked, pending human review.** Scripts: `aligned_triples.py` (output `aligned_triples_5.out`, which
covers p = 5, 7, 11, 13) and `end_to_end.py` (outputs `end_to_end.out`, `end_to_end_recover11.out`,
`end_to_end_17.out`). All arithmetic is exact mod p.

### 9.1 Setting and the four conditions

**Copies and triples.**
* Triple j consists of three copies with pairwise independent labels and relation s_j (all s_ji ≠ 0).
* After the IS front ends, triple j is coherent (η_c-average) along φ_j(e) = (s_ji f_ji(e))_i, inside the tangent
  plane T_j = {Σ_i n_ji v_i = 0}.
* Let M_j be the matrix of e ↦ φ_j(e) in a basis B_j of T_j. Put L_j = B_j M_j M_ref^{−1}.

**Level-2 merge.**
* Take public scalars u_j and measure the coset of {(u_j L_j w)_j} in the joint register.
* For fixed H, the post-measurement state is pure on w ∈ F_p², with phase Φ(w). Any public binary cubic Q_3(w) may
  be added.
* All triples now share the hidden direction d(e) = M_ref e.

**Only aligned merges qualify (PROVED).** Every 2-D merge that keeps the coherent direction for every line is of this
form. A linear map that is projectively correct on all p+1 lines is a scalar multiple of the alignment.

**Along-line coefficients.** Along w_0 + τ d(e), the phase is c_0 + c_1τ + c_2τ² + c_3τ³. With
G(w) = Σ_j u_j³ P3_j(L_j w) + Q_3(w) and P3_j(x) = Σ_i κ_ji β_ji(e) x_i³:
* c_3 = G(d);
* c_2(w_0) − c_2(w_0') = ∇G(d)·(w_0 − w_0');
* the e_3-part of c_2 is −½e_3(Σ_j u_j² λ'_j)([e,z]), with λ'_j = Σ_i s_ji² λ_ji;
* the w_0-quadratic part of c_1 is ∂_d G(w_0);
* η_c does not enter c_1, c_2 or c_3.

Status: PROVED given §2 (elementary composition of the cubic phases). Checked exactly against the IS phases: 0
failures in 140 trials (`aligned_triples_5.out`, "formula check", p = 7, 11, 13).

**Conditions.** A next level can never cancel a coefficient that depends on the unknown line offset w_0, so a usable
level 2 needs:
* **(W)** ∇G(d(e)) = 0 for all e. This is the curl condition, and it implies G(d) = 0 by Euler's identity.
* **(S)** ∂_{d(e)}G ≡ 0 for all e.
* **(E3)** Σ_j u_j² λ'_j = 0.

After clearing the poles of β, (W) and (S) are each 6 linear equations in (u_j³, Q_3). E3 kills the whole e_3
quadratic along d, since q_2(·, d) is an e-free linear form vanishing on every d(e).

### 9.2 Curl check (`aligned_triples_5.out`; exhaustive over projective u ∈ (F_p^*)^m)

Entries are the number of random label configurations with at least one public solution (u, Q_3) of W+S+E3, then the
range of the solution counts per configuration.

| p | m = 1 | m = 2 | m = 3 | m = 4 | m = 5 | m = 6 |
|---|---|---|---|---|---|---|
| 5 (12 configs) | 2 (binary s) | 0 | 0 | 0 | 3 | 7 (2–16) |
| 7 (12) | 1 (binary s) | 0 | 0 | 2 | 3 | 7 (3–21) |
| 11 (6) | 0 | 0 | 0 | 0 | 1 | 6 (3–9) |
| 13 (6) | 1 (binary s) | 0 | 0 | 0 | 4 | 6 (2–14) |

* (W) and (S) had identical solution sets in every instance. That suggests W ⇔ S, which is not proved.
* For m ≤ 2, (W) has full rank on almost all instances (rank 5 for m = 1, rank 6 for m = 2), so no Q_3 exists.
* The dimension count is m + 4 unknowns against 6 + 2 conditions, so solutions are expected from m ≥ 5. This matches
  the data.

**Verdict on the brief's question.** The curl condition does **not** block the aligned-triples second-level merge:
**REFUTED** as an obstruction for m = 6 aligned triples, on every tested instance at p = 11, 13 and on most at p = 5, 7.
Explicit public solutions exist. Two caveats:
* For m ≤ 2 it does block, on all tested generic instances (finite evidence only).
* That solutions exist for all p with probability bounded below is **UNKNOWN** (the dimension count heuristic only).

### 9.3 Level 3 and the end-to-end simulation (`end_to_end.py`)

**Level 3.**
* Merge m' = 3 level-2 states, with weights u'_l and a public quadratic R.
* Condition: Σ_l u'_l² B_l(w, d(e)) + B_R(w, d(e)) = 0 for all w and e, where B_l is the bilinear form of level-2
  state l's quadratic part.
* This is linear in e (checked: 0 failures). It gives 4 equations in (u'², R), i.e. one diagonal quadratic (a conic) in
  u'.

**Claim.** After level 3, along every line w_0 + τd(e) the phase is c_0(w_0) + μτ, where:
* μ does not depend on w_0;
* μ = a·e + b·e_3 + c, with public a, b, c (obtained by evaluating the public pipeline at trial H);
* μ does not depend on η_c.

So a QFT over F_p² returns z with z·M_ref e = μ, with certainty: one linear equation in (e_1, e_2, e_3).

**Why μ is linear (PROVED given §2, sketch).** Every copy's phase coefficients are affine in (β, e_3/f, η_c/f), and
along d each copy coordinate moves by a multiple of s·f(e). So the τ-coefficient is linear in
(h(e) = βf, f(e), e_3, η_c), and the η_c part is Σ s_i λ_i(η_c) = 0.

**Simulation.** It is an exact, faithful pure-state simulation:
* the front-end blocks, coset outcomes and level-2/3 base points are drawn uniformly, which is their true
  distribution;
* the public choices (u, Q_3, u', R, a, b, c) use only labels, outcomes and trial H;
* the final z is drawn from the exact QFT distribution of the true state.

| check | p = 11 | p = 13 | p = 17 |
|---|---|---|---|
| pipelines (54 copies each) built / level-3 weights found | 3 / 2 | 3 / 3 | 3 / 3 |
| random true H tested: phase exactly c_0 + μτ, μ independent of w_0 and η_c, μ affine in (e, e_3) | 80 / 80 | 120 / 120 | 40 / 40 |
| full recovery: true (line of v_1, e_3) is the unique solution of 3 equations from 3 independent pipelines | 5 / 5 | 5 / 5 | 2 / 2 |

* The first p = 11 recovery batch crashed (KeyError) on a draw with no level-3 weights. It was rerun after
  `recover()` was changed to redraw (`end_to_end_recover11.out`), and the crash is still visible in
  `end_to_end.out`.
* Level-2 redraws (no weights for a 6-triple draw): 1 in 25 draws. Level-3 failures: 1 in about 8 pipelines (`end_to_end.out`).

### 9.4 What this is, and what is still open

**Candidate algorithm for HYP1 and HYP2 from labelled copies with uniform labels.** There is no need for dependent
labels, so no birthday cost.
* 3 runs × 54 copies, plus redraws.
* Per run: IS front ends, two coset measurements, one QFT over F_p², all poly(log p).
* Then solve a 3 × 3 linear system.
* This is constant-copy, and it is not Kuperberg-type.

| item | status |
|---|---|
| (a) along-line formulas, generality of the aligned merge, linearity of μ | PROVED given §2 (sketches here); checked exactly |
| (b) public level-2 weights exist, for generic labels, with probability bounded below as p → ∞ | **UNKNOWN**. Finite evidence: m = 6, p ≤ 17; dimension count m + 3 ≥ 8 |
| (c) poly(log p) solver for level 2. Each instance is 2 diagonal cubic plus 2 diagonal quadratic equations in 6 variables. Fix one variable at random, then use resultants and univariate root finding (Cantor–Zassenhaus). | **CONDITIONAL.** Poly(log p) if the fixed system is 0-dimensional with an F_p-point; not implemented (exhaustive search was used) |
| (d) level 3 = one ternary diagonal quadratic | standard poly time (conic); CONDITIONAL on the rank pattern seen |
| (e) copies whose special line is the true line [e] (diagonal states) | failure probability ≤ 54/(p+1) per run; the simulation drew labels avoiding the test lines |
| (f) consistency with the 11-12 impossibility note (§1, §4, §8, §11) | **NOT checked.** Its model must not contain public 2-D polynomial phase corrections, or one of the two results is wrong |
| (g) novelty / priority | unchecked |

**Claim gates stay false:** "exit (ii) closed" and "poly-time non-binary merge exists" stay false until (b), (c) and
(f) are settled and a human has reviewed the work.

**Next hard question.** Prove (b): for generic labels, does the W+S+E3 variety for m = 6 have an F_p-point with
probability ≥ c > 0? A Lang–Weil count on a geometrically irreducible component would suffice. Also settle (f).
* Next command: `python aligned_triples.py 17,19,23 6` (counts of solution configurations), then a Sage/Singular
  dimension and irreducibility computation of the W+S+E3 ideal over Q(labels) (see `research/TOOLBOX.md`).
* Expected artifact: `aligned_triples_ideal.out`.
* Acceptance test: dimension 1 with a geometrically irreducible component defined over F_p for generic labels;
  otherwise (b) fails.

### 9.5 p = 7 triple (Task 2 extension)

`triple_7_a.out` covers labels (1,0),(0,1),(1,2), without PGM and without post-merge χ. It peaked at 0.43 GB RSS and
took 33 min.

| family | χ | 3-D Fourier (F3) MI | lossless plane 111 + Fourier MI | best line merge MI |
|---|---|---|---|---|
| HYP1 | 0.7230 | 0.0028 | 0.0113 | |
| HYP1g (5 generic lines) | 0.6425 | 0.0014 | 0.0106 | 0.0192 |
| HYP2 | 2.7302 | 0.0261 | 0.0961 | |

* Compared with p = 5, χ rises (0.648 → 0.723) while every Fourier-type single-shot MI falls: F3 0.0031 → 0.0014,
  plane-111 0.0165 → 0.0106, line merges 0.030 → 0.019.
* This fits the first-pass picture: single-shot Fourier extraction decays.
* It says nothing against the multi-copy §9 construction, which extracts linear equations rather than single-copy
  MI.

### 9.6 Adversarial self-check (follow-up)

* **Too good to be true?** The simulation is exact and uses the true per-copy states, validated against the dense σ of
  `hpgp2_free23.py` (§2). It never uses the hidden H in a public choice. But three things limit it:
  * the copy model is the labelled-copy model of the two-copy report (Lemma J); if exit (ii) is meant in another
    access model, this may not apply;
  * the labels were conditioned to avoid 5 test lines;
  * the primes are only up to 17.
* **Possible conflict with earlier notes.** Lemma S and Lemma P(b) concern line merges and stay true. The plane merge
  here is lossy, not lossless; it keeps one coherent direction. Theorem R and the 11-12 impossibility were not
  re-read against this construction. That is item (f), and it is the first thing a reviewer should check.
* **W ≡ S coincidence.** Not proved. Both conditions were checked on every instance, so nothing relies on it.
* **Exhaustive search.** Exhaustive weight search is exponential in log p. Item (c) is the real algorithmic gap.

## Reproduce (from the folder; python = /opt/anaconda3/bin/python, all under nice -n 19)

```
python isbasis.py 5                       > isbasis.out          # IS closed form vs dense sigma, ~10 s
python lemma_s.py                         > lemma_s.out          # exact F_p identities, Lemma S counts, ~10 s
python pairmeas.py 5 pairs                > pairs_5.out          # ~10 s
python pairmeas.py 5 pairctl              > pairctl_5.out        # independent-pair control
python pairmeas.py 7 pairs                > pairs_7.out          # ~1 min
python pairmeas.py 11 pairs 2             > pairs_11_c2.out      # ~12 min, 0.5 GB
python kuperberg_check.py 5,7             > kuperberg_check.out  # Lemma K, exact, ~5 s
python kuperberg_check.py 11 2            > kuperberg_check_11.out
python pairmeas.py 5 triple 1:0,0:1,1:2   > triple_5_a.out       # also 1:0,0:1,1:1 > triple_5_b.out and 1:0,0:1,4:4 > triple_5_bin.out; ~3 min each
./run_triple7.sh                          # p = 7 triple with RSS/time watchdog -> triple_7_a.out (follow-up)
python aligned_triples.py 5,7,11,13       > aligned_triples_5.out    # curl check + formula checks, ~3 s
python end_to_end.py 11 1,2,3; python end_to_end.py 13 1,2,3   > end_to_end.out
python end_to_end.py recover 11 7         # likewise 8..11, and p = 13, 17 -> end_to_end_recover11.out, end_to_end_17.out
```

Acceptance:
* the independent pair gives 0;
* the χ values reproduce the two-copy report;
* the off-r-block norm is ≤ 1e−18;
* post-merge χ(HYP1g) = 0 for every non-lossless merge;
* every Lemma K and Lemma S counter is 0, and the maximum cancelling-line counts are ≤ k.
