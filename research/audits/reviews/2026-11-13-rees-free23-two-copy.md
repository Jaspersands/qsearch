# free23 exit (ii): the two-copy (and k-copy) Holevo question (2026-11-13)

**Status: AI-checked, pending human review.** One AI session (Claude). Exact finite computations up
to float round-off; finite checks only falsify (TRAPS 7). Scripts and outputs:
`research/audits/reviews/2026-11-13-rees-free23-two-copy/`. Nothing else was edited. Context: the
2026-11-12 impossibility note (`2026-11-12-rees-entangled-twist-impossibility.md`), §1, §4, §8 (ii),
§11, and its `hpgp_free23.py` / `hpgp_free23.out`.

## Verdict

* **The acceptance test's refutation branch fails.** chi_2 = 0 does *not* hold for all
  (λ_1, λ_2). The two-copy state carries joint information exactly when λ_1, λ_2 are linearly
  dependent over F_p (one is zero, or λ_2 = cλ_1).
* **PROVED (Lemma J, every p > 3, every k).** The η_c-averaged k-copy state for the hard line K̄ is
  the twisted coset state ρ_{J_Λ(K̄), ψ_Λ} of an explicit subgroup J_Λ(K̄) ≤ G^k (§2). It is
  I/p^{3k} on the label sector, so hypothesis-independent, **iff λ_1, …, λ_k are linearly
  independent**. Otherwise the states for distinct hypotheses are distinct, so χ_k > 0, for both the
  hidden line K̄ and the line of v_1.
* **Consequences (PROVED).**
  * k = 2. χ_2 = 0 for every independent pair: the extension of the single-copy refutation to two
    copies holds for these pairs. That is a fraction 1 − (p³+p²−p)/p⁴ ≈ 1 − 1/p of uniform label
    pairs.
  * k = 2, dependent pairs. χ_2 > 0 for all of them. These are exactly the pairs whose labels
    vanish on a common line N = ker λ_1 ⊂ γ_3. Both copies are then copies of the *same* fil4
    quotient G/N.
  * k ≥ 3. dim γ_3 = 2, so the labels are always dependent, and **χ_k > 0 for every label tuple**.
    No information-theoretic refutation of exit (ii) is possible beyond two copies.
* **Computed (exact, p = 5 all 625 pairs; p = 7 a symmetry-reduced complete set).** See §4.
  * For c ∉ {0, −1}, χ_2(λ, cλ) equals the single-copy "η_c known" value: 0.6362 / 2.2141 bits at
    p = 5, and 0.7108 / 2.7180 at p = 7. The per-state and average spectra agree to 2e−19.
  * At c = −1 it equals the λ = 0 value (0.4136 / 2.2711).
  * The c = −1 equality is PROVED: an explicit permutation, the unitary merge, makes the ensembles
    unitarily equivalent (all trace words agree to 1e−14).
  * The c ≠ −1 equality of χ is a **numerical identity at p = 5, 7; its proof is UNKNOWN**. It is
    **not** a unitary equivalence of ensembles under the identity hypothesis matching, or under any
    of the dilation relabelings that were tested. Trace words of length 3 and 4 differ by O(1)
    relative amounts (`words_5.out`, `words2_5.out`).
* **k = 3, computed at p = 5.** For the label triples tested, χ_3 ranges from 0.4136 to 0.6479
  bits (HYP1) and from 2.2141 to 2.2711 bits (HYP2). A generic non-binary relation gives
  0.6479 / 2.2258, slightly more than the two-copy c ≠ −1 value 0.6362 / 2.2141 (`multi_5.out`).
* **Exit (ii) stays UNKNOWN.** The information exists. Whether a poly-time measurement extracts it
  from non-binary relations (c ≠ −1, or generic triples) is the sharpened open question (§5).

## 1. Setting (same as `hpgp_free23.py`)

* **Group and subgroup.** G = free class-3 Lazard group on x, y. V = G/γ_3 ≅ heis_3, D = [V,V],
  γ_3 = ⟨u, w⟩. H = ⟨exp η⟩ is a hard cyclic subgroup: η = η_V + η_c with η_V ∈ span(x,y,z),
  (e_1, e_2) ≠ 0, η_c ∈ γ_3. K = Hγ_3, and K̄ = F_p η_V is a line of V.
* **One copy.** A copy with γ_3-label λ and unknown uniform base point a is
  φ_λ(a) = p^{-1/2} Σ_t ω^{-λ·C_a(t)}|π(a exp tη)⟩ on ℂ[V]. Its a-average is
  σ_{η,λ} = E_a|φ_λ(a)⟩⟨φ_λ(a)|.
* **Two copies.** They come from the same H, so **η, including η_c, is shared**. Base points are
  independent. The state is

  ρ_h(λ_1, λ_2) = E_{η|h} σ_{η,λ_1} ⊗ σ_{η,λ_2}, of dimension p^6.

* **Hypotheses.**
  * HYP1: the line (e_1:e_2) of V/D, p+1 values. Nuisance (e_3, η_c).
  * HYP2: the line K̄ of V, p²+p values. Nuisance η_c.
  * Within a hypothesis the prior is uniform. This is H uniform over the hard cyclic subgroups.
* **Holevo quantity.** χ = S(avg_h ρ_h) − avg_h S(ρ_h), in bits. It bounds the mutual information
  of **any** joint measurement of the two copies.
* **Controls.** "η_c = 0 known" keeps the nuisance η_c fixed at 0.

## 2. Analytic results (PROVED, every p > 3)

**Conventions.** Q is a group, S ≤ Q, and χ is a character of S. Write
ρ_{S,χ} = |Q|^{-1} Σ_{g,g'} 1_S(g'^{-1}g) χ(g'^{-1}g) |g⟩⟨g'|, as in Lemma T of the 2026-11-12 note.
After the γ_3 instrument, a raw copy with label λ is ρ_{K,χ_λ} on ℂ[G], where

χ_λ(exp(tη_V)·z) = ω^{λ(z) − tλ(η_c)}, because exp(tη) = exp(tη_V)exp(tη_c) (η_c is central).

The isometry ψ_q ↦ |q⟩ from the λ-sector of ℂ[G] onto ℂ[V] carries ρ_{K,χ_λ} to σ_{η,λ}. This
is the identification `hpgp_free23.py` uses. It was re-checked here through the left-regular
action U_λ: ‖[σ, U_λ(g)]‖ ≤ 4e−18.

**Lemma J.** Fix k labels Λ = (λ_1, …, λ_k) and a hard line K̄ with representative η_V. Let η_c
be uniform. Then

E_{η_c} ⊗_j ρ_{K,χ_{λ_j}} = ρ_{J_Λ, ψ_Λ} on ℂ[G^k], where

* J_Λ = {(exp(t_j η_V) z_j)_j : t ∈ R_Λ, z_j ∈ γ_3} ≤ K^k;
* R_Λ = {t ∈ F_p^k : Σ_j t_j λ_j = 0 in (γ_3)^*} is the relation space of the labels;
* ψ_Λ((exp(t_jη_V)z_j)_j) = ω^{Σ_j λ_j(z_j)}.

*Proof.* ⊗_j ρ_{K,χ_j} = ρ_{K^k, ⊗χ_j}, and ρ_{S,χ} is linear in the function 1_S χ. The η_c-average
of Π_j χ_j is ω^{Σλ_j(z_j)} · E_{η_c} ω^{−(Σ_j t_jλ_j)(η_c)} = ω^{Σλ_j(z_j)} · [t ∈ R_Λ], since η_c is
uniform on γ_3. J_Λ is a subgroup and ψ_Λ is a character, because K is abelian and
t ↦ exp(tη_V) is a homomorphism. ∎

**Corollary J1 (hypothesis independence).** Suppose R_Λ = 0, that is, the λ_j are linearly
independent. Then J_Λ = γ_3^k and the averaged state is I/p^{3k} on the label sector, for every
hypothesis and every prior on η_V. So χ_k = 0 for HYP1, for HYP2, and for any other function of H.
This needs k ≤ 2 (dim γ_3 = 2). For k = 1 it is the 2026-11-12 single-copy statement. For k = 2 it
covers every pair with λ_1, λ_2 independent.

**Corollary J2 (information whenever the labels are dependent).** Suppose R_Λ ≠ 0. Then:

* **The states are distinct.** By the stabilizer argument, R_g P_{J,ψ} = ψ(g)P_{J,ψ} forces g ∈ J
  (test on a function supported on one coset). So ρ_{J,ψ} determines J. And J_Λ(K̄) determines K̄:
  take t ∈ R_Λ with some t_j ≠ 0, and project to coordinate j. So the HYP2 states are pairwise
  distinct, and χ_k^{HYP2} > 0.
* **HYP1.** One has |tr(ρ_{S,χ} R_g)| = 1_S(g). Take g = (exp(t_j w))_j with w̄ ∈ K̄_{e_3*}. Then
  |tr(ρ_h R_g)| = 1/p for the hypothesis h that is the line (e_1:e_2) under w̄, and 0 for every
  other h'. So ρ_h ≠ ρ_{h'}, and χ_k^{HYP1} > 0.
* **Exact HYP2 data.** ρ_{J_Λ(K̄)} is a normalized projector of rank p^{3k−r}, with
  r = dim R_Λ. Hence S(ρ_h) = (3k − r) log₂ p and χ_k^{HYP2} ≤ r log₂ p. Also
  tr(ρ_h ρ_{h'}) = p^{−3k} for h ≠ h' (J ∩ J' = γ_3^k) and p^{−3k+r} for h = h'.
* **k ≥ 3.** Here r ≥ k − 2 ≥ 1 always. So **every** k-tuple of labelled copies with k ≥ 3 has
  χ_k > 0.

**Corollary J3 (what the dependent pairs are).** Let λ_1 ≠ 0. Then λ_2 ∈ F_p λ_1 exactly when both
labels vanish on the line N = ker λ_1 ⊂ γ_3. In that case both copies are R_N-invariant and can be
promoted (O4) to the same quotient G/N ≅ fil4. So two-copy joint information exists exactly for
pairs of copies of one common fil4 quotient, or when a label is 0. That is the setting of IS Cor 8
for fil4. For uniform labels such a pair has probability (p³ + p² − p)/p⁴ ≈ 1/p.

**Proposition M (c = −1 is the unitary merge; PROVED).** Take Λ = (λ, −λ). The permutation
Φ(g_1, g_2) = (g_2 g_1^{-1}, g_1) of G × G satisfies Φ(g·j) = Φ(g)·j′ for j ∈ J_Λ, where
j = (k z_1, k z_2) with k ∈ K and j′ = (z_2 z_1^{-1}, k z_1). The map j ↦ j′ is an isomorphism
from J_Λ onto γ_3 × K, and it carries ψ_Λ to (−λ) ⊗ 1. Hence

P_Φ ρ_{J_Λ} P_Φ† = (I/p³ on the (−λ)-sector) ⊗ ρ_{K,1}.

ρ_{K,1} is the λ = 0 single copy. So the c = −1 ensemble is unitarily equivalent to the λ = 0
single-copy ensemble ⊗ I/p³, by a hypothesis-independent and efficiently computable permutation,
and χ_2(λ, −λ) = χ_1(0). This is the binary zero-sum merge of Prop B, written as a unitary.

**Not proved: c ∉ {0, −1}.** χ_2(λ, cλ) equals the single-copy "η_c known" value. So do the
spectra of every HYP1 state and of the average state (§4). But the two ensembles are **not**
unitarily equivalent under the identity hypothesis matching: trace words of length 3 and 4 differ,
whereas for c = −1 they agree to 1e−14.
* **What is proved.** R_{(z,z)} commutes with every ρ_{J_c(K̄)}. For K̄ outside the line of g_0,
  ρ_{J_c} is the R_{(z,z)}-twirl of the product of two η_c-known copies. This holds because
  R_z shifts the extension parameter s of a label-λ copy by λ(e_1u + e_2w), and that of a
  label-cλ copy by c times as much.
* **What is open.** Why χ coincides is UNKNOWN. It could be a coincidence of Holevo values, or an
  equivalence under a hypothesis permutation that was not tested.
* **Why Prop M does not extend.** No permutation of G × G of the Prop M type exists: it would need
  k ↦ k^{−c} on the unknown line, and power maps are not homomorphisms.

## 3. Method and validation (`hpgp2_free23.py`)

**The method is exact; no p^6 × p^6 matrix is ever formed.**
* **Symmetry.** σ_{η,λ} commutes with U_λ(G). Here U_λ(g)|q⟩ = e^{−2πiλ·c′/p}|q′⟩, where
  g·exp(q) = exp(q′ + c′).
* **One copy.** Take A_λ = ⟨g_0, z⟩ with λ([g_0, z]) = 0. It is abelian in U_λ. Its joint
  eigenprojectors, built as exact character sums, give a basis W_λ. In W_λ every σ is block
  diagonal, with p² blocks of size p.
* **Two copies.** ρ_h is block diagonal in W_{λ_1} ⊗ W_{λ_2}, with p⁴ blocks of size p². Each block
  is E_η B_1^η[b_1] ⊗ B_2^η[b_2].
* **Representatives.** Blocks in one U(x′)-orbit are unitarily equivalent through an
  h-independent unitary. Mode `rep` keeps one block per orbit pair, with its weight. Mode `full`
  keeps all p⁴ blocks.
* **Cost.** Peak RSS is about 0.4 GB at p = 7. Wall time is about 13 min for all 625 pairs at
  p = 5, and about 25 min for the 51 pairs at p = 7.

**Validation** (`validate_5.out`, plus p = 7 cross-checks):
1. **Basis checks, five labels.**
   * [U_0, U_z] = 0, and W is unitary to 2e−15.
   * [σ, U(g)] ≤ 4e−18 for g = g_0, z, x′.
   * The off-block entries of σ are ≤ 5e−18.
   * The orbit sizes match the theory: five orbits of size 5 for λ ≠ 0. For λ = 0 there are five
     of size 1 (the characters of heis_3) and four of size 5.
2. **Single copy: block vs dense vs `hpgp_free23.out`.**
   * Every row of the old output is reproduced to ≤ 4e−15 (p = 5, labels (0,0), (1,0), (0,1),
     (1,1), plus (2,3)).
   * This includes the nonzero controls: 0.4136, 2.2711, 1.6816, 0.6362, 1.7873 and 2.2141.
   * The "a fixed" controls 2.3063 / 2.0680 are reproduced by the dense path. They are not
     U-invariant, so the block path does not apply to them.
   * p = 7: the table's (λ, 0) row gives 0.3673 / 2.7737, the old λ = 0 values. Its c = 1 row
     gives 0.7108 / 2.7180, the old "η_c = 0 known" values.
3. **Two copies, `rep` vs `full`.** Seven pairs at p = 5 agree to ≤ 4e−15. This checks the
   orbit-weight reduction.
4. **Two-copy moments, with no block basis.** tr(ρ_h ρ_{h'}) is computed from dense σ's by the
   factorization E_{η,η'} tr(σ_1σ_1') tr(σ_2σ_2'), and compared with the block representation. The
   difference is ≤ 5e−18. The values equal Lemma J's predictions exactly:
   * dependent pairs: p^{−5} on the diagonal and p^{−6} off it;
   * independent pairs: p^{−6} everywhere, i.e. I/p^6;
   * (0,0): p^{−4} and p^{−6}.
5. **Trace and block-diagonality.** Every trace is 1 to 1e−15. Off-block entries are ≤ 2e−17.
6. **Analytic entropies.** S(ρ_h^{HYP2}) = (6 − r) log₂ p in every row, with r = 0, 1, 2:
   13.9316 / 11.6096 / 9.2877 at p = 5 and 16.8441 / 14.0368 / 11.2294 at p = 7.

A brute-force p^6 diagonalization was **not** done: at p = 5 a dense 15625² matrix would need
3.9 GB. Checks 4 and 6 are the substitutes. They are independent of the block basis.

## 4. Results

**p = 5, all 625 ordered pairs** (`table_5_all.out`, grouped in `table_5_summary.out`).
Columns 3–6 are in bits. The last two columns are the "η_c = 0 known" controls.

| class | # | HYP1 χ_2 | HYP2 χ_2 | HYP2 mean S | known HYP1 | known HYP2 |
|---|---|---|---|---|---|---|
| independent | 480 | 0.0000 | 0.0000 | 13.9316 = 6 log₂5 | 1.8548 | 4.0371 |
| c ∉ {0,−1} | 72 | 0.6362 | 2.2141 | 11.6096 = 5 log₂5 | 1.776–1.816 | 3.989–4.000 |
| c = −1 (binary) | 24 | 0.4136 | 2.2711 | 11.6096 | 1.8167 | 4.0405 |
| one label 0 | 48 | 0.4136 | 2.2711 | 11.6096 | 1.8376 | 4.0108 |
| both 0 | 1 | 1.8527 | 4.0817 | 9.2877 = 4 log₂5 | — | — |

The maximum over the 480 independent pairs is |χ_2| < 1e−14.

**p = 7** (`table_7.out`, `table_7_summary.out`). The set is λ_1 = (1,0) with all 49 λ_2, plus
(0,0)×(0,0) and (0,0)×(1,0).
* **Why this set is complete.** The graded automorphisms act on γ_3 through
  {det(A)·A : A ∈ GL_2}, which contains SL_2 and so is transitive on nonzero labels. They permute
  the HYP1 and HYP2 hypothesis sets, and they preserve the uniform nuisance. Swapping the copies
  covers λ_1 = 0. The p = 5 all-pairs run confirms that χ_2 depends only on the class.

| class | # | HYP1 χ_2 | HYP2 χ_2 | HYP2 mean S |
|---|---|---|---|---|
| independent | 42 | 0.0000 | 0.0000 | 16.8441 = 6 log₂7 |
| c ∉ {0,−1} | 5 | 0.7108 | 2.7180 | 14.0368 = 5 log₂7 |
| c = −1 | 1 | 0.3673 | 2.7737 | 14.0368 |
| one label 0 | 2 | 0.3673 | 2.7737 | 14.0368 |
| both 0 | 1 | 2.2291 | 4.9791 | 11.2294 |

For comparison, log₂ #hyp is 2.585 / 4.907 at p = 5 and 3.000 / 5.807 at p = 7.

**Spectral identity** (`compare_5.out`, `compare_7.out`).
* For every c ∈ F_p^× \ {−1}, the full weighted spectra are compared: of each HYP2 state, of each
  HYP1 state, and of the average state of the (λ, cλ) ensemble. They are compared against
  [single copy, label λ, η_c = 0 known] ⊗ I/p³. They agree to ≤ 2e−19.
* For c = −1 the same holds against [λ = 0] ⊗ I/p³. That case is Prop M.
* So χ_2(λ, cλ) = χ_1^{known}(λ) to 10 digits: 0.6362151804 / 2.2140790054 at p = 5 and
  0.7107896225 / 2.7180132067 at p = 7.

**Trace words** (`words_5.out`, `words2_5.out`, p = 5).
* **c = −1 against λ = 0 ⊗ I/p³.** All length-3 words and 3000 sampled length-4 words agree to
  ≤ 4e−22 absolute (1e−14 relative). This is consistent with Prop M.
* **c = 1, 2, 3 against η_c-known label (m, 0) ⊗ I/p³, m = 1..4.** The labels (m, 0) are equivalent
  to e_3-dilation relabelings. Sampled words of length 3 and 4 differ with relative size 1 to 10,
  far above round-off.
* So for c ≠ −1, the χ equality is **not** explained by a unitary equivalence under these hypothesis
  matchings. Note: the "typical word size p^-12" printed in `words_5.out` is mislabelled. The actual
  length-3 scale is about p^{-10} ≈ 1e−7, so the 1.8e−8 there is a 18% difference, not round-off.

**Three copies, shared η** (`multi_5.out`, p = 5; S(ρ_h^{HYP2}) = 8 log₂5 = 18.5754 = (9 − r) log₂ p
with r = 1, as Lemma J predicts):

| labels λ_1, λ_2, λ_3 | relation t ∈ R_Λ | HYP1 χ_3 | HYP2 χ_3 |
|---|---|---|---|
| (1,0), (0,1), (4,4) | (1,1,1), binary | 0.4136 | 2.2711 |
| (1,0), (0,1), (1,1) | (1,1,−1) | 0.6362 | 2.2141 |
| (1,0), (0,1), (1,2) | (1,2,−1) | 0.6479 | 2.2258 |
| (1,0), (0,1), (2,3) | (2,3,−1) | 0.6479 | 2.2258 |

The binary triple reproduces the λ = 0 copy, as the merge predicts. Every non-binary triple carries
information. No two of these labels are proportional, so no fil4 quotient is shared.

## 5. What this means for exit (ii)

* **Refuted at two copies.** Two-copy measurements of independently labelled copies cannot learn
  anything: χ_2 = 0, PROVED. That is the generic case, a fraction 1 − O(1/p) of label pairs.
* **Exceptions: pairs on one fil4 quotient.** Two-copy information exists exactly for pairs whose
  labels lie on a common line, i.e. two copies of the same fil4 quotient G/ker λ (Cor J3), or when
  a label is 0.
  * c = −1 is the SOT binary merge (Prop M).
  * c ≠ −1 carries information that the SOT identity-twist merge destroys. The merged label is
    (1+c)λ ≠ 0, and that single-copy information is 0. The same information is carried by a
    single **η_c-known** copy, and in that copy even plain abelian Fourier sampling sees
    0.013 / 0.130 bits (`hpgp_free23.out`).
  * Among N uniform labels, a proportional pair appears only when N ≳ √p, by the birthday bound on
    p+1 projective classes. So two-copy joint measurements alone do not give a poly(log p) route.
* **Not refuted at k ≥ 3: information exists for every label triple.** The refutation **cannot**
  extend to k ≥ 3 copies. By Cor J2, χ_k > 0 for every label k-tuple once k ≥ 3, PROVED. The
  k-copy state is the twisted coset state of J_Λ(K̄) ≤ G^k. It encodes an F_p-weighted relation
  t ∈ R_Λ among the labels. Such relations always exist and are found by linear algebra, unlike
  the binary zero-sums of Theorem R.
* **The sharpened open question (UNKNOWN).** Is there a poly(log p)-time measurement or channel on
  ρ_{J_Λ(K̄)} for a **non-binary** relation t? The simplest instance is two copies with λ_2 = cλ_1
  and c ≠ −1, or three copies with a generic relation. It would have to output the line of v_1.
  * Within SOT(Aut) the answer is no: Theorem R allows only binary relations.
  * A positive answer would be an exit-(ii) mechanism that SOT does not contain.
  * Information-theoretic arguments cannot settle it. Only a computational argument can.
* **Claim gates (stay false).** "Exit (ii) is closed." "Joint measurements cannot help." "A weighted
  merge exists." "The c ≠ −1 equivalence is efficient."

**Next hard question.** For two copies with λ_2 = cλ_1 (c ≠ −1), i.e. two fil4-quotient copies,
is there a poly(log p)-time measurement whose outcome has mutual information Ω(1) with the line of
v_1, uniformly in p? IS Cor 8's HPGP for fil4 is the natural candidate: check whether it uses
pairs of copies with arbitrary central labels. Then ask the same for three copies with a generic
relation, where no fil4 quotient is shared.
* Next command: compute the mutual information of the IS-type pair measurement on ρ_{J_c} at
  p = 5, 7, 11, after reading IS Cor 8 for its exact form. (Source not re-read here.)
* Expected artifact: `pair_measurement_*.out`.
* Acceptance test: MI bounded away from 0 as p grows means a usable non-binary pair primitive.
  MI → 0 like the plain Fourier value (0.013 bits) means no evidence.

## 6. Adversarial self-check

* **Is "shared η" modelled right?** Both copies use the same H, so all of η is shared, including
  e_3 and η_c, while the base points are independent. Sharing a base point is impossible for fresh
  coset copies. The labels are uniform and H-independent, since H ∩ γ_3 = 1. Conditioning on them
  is legitimate.
* **Could the block method hide off-block coherence?** No. It is checked directly (≤ 2e−17), and the
  dense moment check needs no block basis (≤ 5e−18 agreement). Rep-vs-full agreement checks the
  orbit-equivalence step, which is also a theorem: U(x′) commutes with every σ and permutes the
  A-eigenspaces.
* **Float round-off.** Negative entries such as −0.0000 are round-off at 1e−15. χ = 0 for
  independent pairs is a theorem (J1), not an inference from numerics.
* **Does χ_2 > 0 show that exit (ii) works?** No. Holevo information is information-theoretic. EHK
  already implies that poly(log p) copies determine H. The new content is *where* the joint
  information sits: in F_p-weighted label relations, not only in binary ones. Whether it is
  efficiently extractable is UNKNOWN.
* **The spectral identity for c ≠ −1 is numerical only.** It was checked at p = 5, 7 for all c.
  Spectra are compared per state and for the average. Equal spectra do not prove a unitary
  equivalence of ensembles, although equal per-state and average spectra suffice for equal χ.
  The trace-word test shows they are not unitarily equivalent under the identity matching. So the
  χ coincidence is unexplained, and it may hold only at p = 5, 7.
* **Do the k = 3 values generalize?** Only four triples at p = 5 were computed. The positivity
  χ_3 > 0 is a theorem (Cor J2); the numerical values are not.
* **HYP1/HYP2 are not the only hypothesis families.** Lemma J holds for any function of H, but
  Cor J2 was proved only for HYP1 and HYP2. Distinct K̄ give distinct states, so any family that
  separates lines also has χ > 0.
* **Scope.** free23 only. Lemma J's form holds for any class-3 group with K abelian and
  dim γ_3 = g. Then J1 needs k ≤ g, and J2 applies for k > g. This was not checked beyond free23.
  DL (g = 2) is analogous, but NOT computed.
* **Novelty.** Lemma J is a direct calculation in the style of Lemma T. The fil4-quotient reading
  (Cor J3) is standard. Priority is unchecked.

## Reproduce (from the folder)

```
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py validate 5      > validate_5.out    # ~2 min
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py table 5 rep all > table_5_all.out   # ~13 min
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py table 7 rep     > table_7.out       # ~25 min, 0.4 GB
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py compare 5       > compare_5.out     # ~10 s
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py compare 7       > compare_7.out     # ~4 min
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py words 5         > words_5.out       # ~11 min
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py multi 5         > multi_5.out       # ~2 min
nice -n 19 /opt/anaconda3/bin/python hpgp2_free23.py words2 5        > words2_5.out      # ~1 min
/opt/anaconda3/bin/python summarize.py table_5_all.out > table_5_summary.out
```

Acceptance:
* independent pairs: χ_2 = 0;
* dependent pairs: χ_2 > 0 and S(ρ^{HYP2}) = 5 log₂ p;
* rep = full, and dense moments = block moments;
* spectral differences ≤ 1e−15.
