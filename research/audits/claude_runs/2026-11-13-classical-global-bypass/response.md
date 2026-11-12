# Verdict in one line

No classical polynomial-bit bypass was found. Everything in the descent except one object is polynomial (given factoring and the conditional local routine), and that object is forced by the dimension output itself: for each number-field factor K of L = Q[x]/(f) one needs the pair

  D(K) = ( r_K := rank₂ Cl_S(K) ,  Im_K := loc_S(K(S,2)) ⊂ W_K := ⊕_{v∈S_K} K_v^×/K_v^{×2} ).

The mod-2/dimension nature of the output does **not** remove D(K): I prove below that dim Sel² is a polynomial F₂-linear function of {D(K_i)} and, conversely, exhibit an explicit growing-genus family in which dim Sel² pins r_K to within an additive g (to within one bit for elliptic curves). This is a scoped obligation/equivalence, not a hardness claim.

Status labels used: [P] proved here from the attached Stoll text plus standard class field theory / global duality; [A] assumption or imported theorem; [C] finite sanity recollection, not evidence; [S] speculation.

---

## 1. Exact reformulation of the endpoint (proved)

Notation: S_Q = {2, ∞} ∪ {p : p² | disc f} (Stoll Cor. 4.7). L = ∏ K_i. For a field K, S_K = places of K over S_Q (real places included; complex places contribute 0). W_K as above, with dim W_K = Σ_{v|2}([K_v:Q₂]+2) + 2·#{odd finite v ∈ S_K} + r₁(K). W_L = ⊕_i W_{K_i} = ⊕_{v∈S_Q} L_v^×/L_v^{×2}. For v ∈ S_Q let J_v = δ_v(J(Q_v)) ⊂ H_v ⊂ L_v^×/L_v^{×2} (the conditional local routine supplies J_v in explicit coordinates). J_S := ⊕_{v∈S_Q} J_v ⊂ W_L.

**Lemma 1 (norm condition is local) [P].** For ξ ∈ L(S,2): ξ ∈ H ⇔ N(loc_v ξ) = 1 in Q_v^×/Q_v^{×2} for all v ∈ S_Q.
*Proof.* v_q(Nξ) = Σ_{w|q} f_w v_w(ξ) is even for q ∉ S_Q, so Nξ ∈ Q(S,2) = ⟨−1, p ∈ S_Q⟩. The map Q(S,2) → ⊕_{v∈S_Q} Q_v^×/Q_v^{×2} is injective: a class ±∏p^{e_p} that is positive (place ∞) and a square at each p ∈ S_Q has all e_p even and sign +. ∎

Consequently, since J_v ⊂ H_v enforces local norm-triviality,
  Sel²(J/Q) = { ξ ∈ L(S,2) : loc_S(ξ) ∈ J_S }   (Stoll Cor. 4.7 + Lemma 1),
and the "rational norm-square rows" in the proposed quantum chain are redundant (harmless, not wrong).

**Lemma 2 (kernel of localization) [P].** ker(loc_S : L(S,2) → W_L) ⊂ Sel², and dim ker(loc_S) = Σ_i rank₂ Cl_{S}(K_i) (the factor Q contributes 0).
*Proof.* ker ⊂ Sel²: res_v ξ = 0 ∈ J_v and ξ ∈ H by Lemma 1. Componentwise, ξ_i ∈ K_i(S,2) with ξ_i a local square at every v ∈ S_{K_i}. The quadratic (or trivial) extension K_i(√ξ_i) is unramified at every finite prime outside S (even valuation, residue characteristic odd since all primes over 2 lie in S) and split — hence unramified — at every place of S_{K_i}, real places included. By class field theory the compositum of such extensions is the maximal abelian 2-elementary extension unramified everywhere and split at S, dual to Cl_S(K_i)/2Cl_S(K_i), where Cl_S = Cl/⟨classes of primes in S⟩. Kummer theory makes ξ_i ↦ K_i(√ξ_i) injective on square classes. ∎

**Lemma 3 (dimension decomposition) [P].**
  dim Sel² = Σ_i r_{K_i} + dim( Im_L ∩ J_S ),  Im_L = ⊕_i Im_{K_i}.
*Proof.* Sel² = loc_S^{-1}(J_S) inside L(S,2); exact sequence 0 → ker loc_S → Sel² → Im_L ∩ J_S → 0. Localization is componentwise because L_v = ⊕_i K_i ⊗ Q_v. ∎

**Lemma 4 (what is known about Im_K for free) [A, standard global duality].** Im_K is its own orthogonal complement under the sum over v ∈ S_K of local Hilbert pairings (Poitou–Tate for μ₂, valid since S_K ⊇ {v | 2∞}); hence dim Im_K = ½ dim W_K = r₁ + r₂ + |S_{K,fin}|. Consistency check with Lemma 2: dim K(S,2) = r₁ + r₂ + |S_{K,fin}| + r_K (free S-units, μ(K)/μ(K)², and Cl_S[2]), minus dim ker = r_K. ✓

So: given D(K_i) for all i, everything else — the F₂ matrices of loc_S on a basis of L(S,2), the intersection with J_S, the final dimension — is polynomial linear algebra over a common local frame (paid exactly as in the quantum chain). The classical question is therefore: **can D(K) be obtained in polynomial bit time without class/unit machinery?**

---

## 2. Constructive classical attempt and the first blocking step

1. Factor f over Q: polynomial (LLL) [A].
2. Compute S_Q: needs the primes p with p² | disc f. Classically this is integer factorization of disc(f) (bits poly in g,B). Any classical algorithm here is **conditional on supplied factorization** or subexponential. Separable cost; I keep it as a stated condition and do not fold it into the global obstacle.
3. Local images J_v, v ∈ S_Q, in explicit coordinates: the conditional premise [A].
4. Common frames, precision, exponent-parity localization of small representatives: polynomial, as in the chain's own ledger (not re-derived here).
5. Global datum D(K_i) for each non-Q factor. **This is the first exact step needing more than polynomial arithmetic.** Nothing classical known produces r_K or Im_K for an arbitrary field of degree up to 2g+1 in polynomial time, even under GRH and with disc factorization supplied; the known classical routes (index calculus for Cl and U_S, Buchmann-type, or Stoll's own steps 3.2.1–3.2.3) are subexponential at best and carry their own heuristic/rigor hypotheses. I do not infer hardness from this; §3–4 show instead that the dimension output cannot be reached by routes that discard D(K).
6. Given D(K_i): F₂ linear algebra of size poly(g, |S|, log|disc|). Polynomial.

Polynomial subfamily (fully native, conditional on factoring + local routine): if every factor K_i = Q (f splits completely over Q), then D(Q) = (0, loc_S(Q(S,2))) is explicit: Q(S,2) has basis −1 and p ∈ S_Q, dim |S_Q,fin|+1 per copy, loc_S computable by Hilbert-symbol/sign arithmetic in poly bits. Ledger: (2g+1)(|S_Q|+1) generators × dim W_L ≤ (2g+1)(3 + 2|S_Q|) columns; one Gaussian elimination. Decisive falsifier: an input with all roots rational where this procedure disagrees with an independently computed Selmer dimension. This subfamily is exactly where all class/unit data vanish; it does not extend to any factor of degree ≥ 2 (see §3).

---

## 3. Why each proposed shortcut loses D(K) (pointed, not a survey)

- **Genus theory.** Computes rank₂ Cl^± only for quadratic (more generally cyclic prime-degree over a base with known class group) fields via ambiguous classes. Odd-degree non-Galois factors K (the generic case here) have no ramification-data formula for rank₂ Cl_S(K). Even for a quadratic factor, genus theory gives r_K but not Im_K: Im_K contains the S-local square class of the fundamental unit, which genus theory does not supply (the real/2-adic class of ε is the narrow-vs-ordinary 2^∞ problem, not a 4-rank/Rédei computation) [A: no polynomial method known to me; not claimed hard].
- **Quadratic characters / ray-class duality.** Lemma 4 identifies Im_K^⊥ = Im_K = ker(W_K → Cl_𝔪(K)/2Cl_𝔪(K)) for 𝔪 supported on S_K∪∞ sufficiently divisible. Deciding whether a local S-idèle tuple lies in this kernel is the principal-ideal-modulo-squares problem in the ray class group — a reformulation of the same unit/class computation, not a bypass.
- **Reciprocity.** Hilbert's product formula gives Im_K ⊂ Im_K^⊥ and (with Poitou–Tate) equality; this fixes only dim Im_K, not Im_K. Two maximal isotropic subspaces of W_K can intersect in any dimension (already for dim 2: lines in F₂² alternating, equal or not), so dim(Im ∩ J_S) is not determined by dimensions, Arf-type data, or local data.
- **Mod-2 relation lattice.** For the GRH factor base T, the image of U_T in F₂^T is (Λ + 2Z^T)/2Z^T = ker(F₂^T → Cl(K)/2Cl(K)), of dimension |T| − rank₂ Cl(K). Hence the mod-2 lattice (even just its dimension) *contains* rank₂ Cl(K); and partial relations found by sieving give a sublattice, hence only one-sided bounds (lower bound on dim ker loc and on dim(Im∩J_S), i.e. a lower bound on dim Sel²). Completeness certification is the class-group problem (consistent with the chain's "never infer completeness from returned units").
- **Norm-kernel structure.** For odd degree, Q^× splits off: L^×/L^{×2} = H ⊕ Q^×/Q^{×2}. This removes the global norm rows (Lemma 1) but no class/unit data.
- **Global cohomology.** The Greenberg–Wiles/Poitou–Tate dimension formula is vacuous for the self-dual structure J[2] with Lagrangian local conditions (the local offsets at 2 and ∞ cancel: +g, −g). Parity of dim Sel² relates to the root number only via the unproved parity conjecture and gives one bit, not the integer.
- **Analytic shortcuts under GRH [A].** Truncated Euler products give h_K R_K within a constant factor in polynomial time, but this is a product and carries no 2-rank information; it certifies candidate class/unit data only after that data has been found (subexponentially).

---

## 4. Explicit family: the dimension output retains r_K (proved bracket)

**Family F_g.** f irreducible of degree 2g+1 with (i) exactly one real root, (ii) f irreducible over Q₂ (2 has a single prime in K), (iii) for every odd p with p² | disc f, f irreducible over Q_p. These are explicitly checkable local conditions (given the factorization of disc f).

**Local sizes [P, from Stoll's identification].** With n_v = number of Q_v-irreducible factors: dim J_p = n_p − 1 (odd p), dim J_2 = n_2 − 1 + g, dim J_∞ = (n_∞ − 1)/2; dim H_v = 2 dim J_v in all cases (checked: dim L_2^×/sq = (2g+1) + 2n_2, minus dim Q_2^×/sq = 3). In F_g: J_p = 0, J_∞ = 0, dim J_2 = g, dim W_K = 2g + 4 + 2|S_odd|, dim Im_K = g + 2 + |S_odd|.

**Proposition [P].** For f ∈ F_g, with K = L and S_K the primes over S_Q,
  r_K ≤ dim Sel²(J/Q) ≤ r_K + g,  r_K = rank₂ Cl_S(K).
*Proof.* Lemma 3 with J_S = 0 ⊕ J_2 ⊕ 0, dim(Im_K ∩ J_S) ≤ dim J_2 = g. ∎

For g = 1 (E: y² = cubic with one real root, cubic irreducible over Q₂ and over Q_p for p² | disc): dim Sel²(E/Q) ∈ {r_K, r_K + 1}.

Consequence: any procedure that outputs dim Sel² on F_g (even g = 1) computes rank₂ Cl_S(K) up to additive g for every field K satisfying (i)–(iii). So every shortcut of §3 that discards class data (genus/local/discriminant-only, reciprocity-only, partial relation lattices) must fail on F_g unless rank₂ Cl_S is constant on F_g with fixed cheap data; I make no claim either way about that constancy (class-group statistics assert nonconstancy for complex cubic fields, but I cite no source and treat it as unverified). The bracket itself needs no such input.

[C] Sanity recollection, not evidence: f = x³ − 2 is in F_1 (Eisenstein at 2, no cube root of 2 in Q₃, one real root, S_Q = {2,3,∞}); Cl(Q(∛2)) trivial so r_K = 0, and the recollected rank 1 of y² = x³ − 2 (point (3,5)) gives dim Sel² = 1 = r_K + 1, inside the bracket.

---

## 5. What this changes for the quantum endpoint

1. **Minimal global interface.** The chain need not expose a full compact T-unit basis with torsion and class support as the deliverable; the only global data consumed is D(K_i) = (r_{K_i}, Im_{K_i}) per factor. r_K comes from the mod-2 SNF of the valuation matrix of the T-unit generators restricted to Cl_S (Algorithm 5 shape, with the T∖S kernel). Im_K comes from localizing the T∖S-kernelled compact atoms at S_K. This is the same computation, repackaged; it does not reduce the quantum source hypotheses (Theorem 5 failure μ per factor, exact compact recovery, torsion per factor for even-degree factors — odd-degree factors have μ(K) = {±1} since φ(m) | [K:Q] forces m ≤ 2).
2. **Cheap classical certificate for Im_K [P].** If the returned elements are genuine members of K(S,2) (checkable: valuations even outside S via norms/ideal factorization over the maximal order) and their localizations span an isotropic subspace of dimension ½ dim W_K, then that span equals Im_K by Lemma 4. This partially addresses "never infer completeness from returned units": the Im-part is certifiable classically; the kernel part r_K is not (it is the class-group 2-rank) and remains a bounded-error output of the quantum class-group step. Independence of kernel elements mod squares can be certified via GRH-bounded primes outside S (their Kummer extensions are unramified, discriminant Δ_K², so Chebotarev-type bounds of the 48(log)² kind apply), but completeness cannot.
3. **Redundancy.** The rational norm-square rows are implied by J_v ⊂ H_v (Lemma 1); keeping them is harmless.
4. **Comparator statement.** Strongest same-problem classical comparator found: Stoll's descent with classical subexponential class/S-unit computation (plus classical factoring), with the Im-certificate above usable there as well. No polynomial classical counterpart exists in my reconstruction beyond the fully split subfamily. This is not a lower bound and not a speedup claim; Proposition of §4 says only that the Selmer-dimension endpoint classically *subsumes* additive-g approximation of rank₂ Cl_S(K) on F_g.

---

## 6. Obligations and falsifiers

Proof obligations for the statements above:
- O1: Poitou–Tate Lagrangian property of Im_K with real places as F₂ sign classes and complex places zero (Lemma 4) — standard, imported [A].
- O2: identification of ker(loc_S) with the dual of Cl_S(K)/2 (Lemma 2) — standard CFT; needs S ⊇ {v|2} so that even valuation ⇒ unramified, which Stoll's S guarantees.
- O3: the local dimension table in §4 (from Stoll's identification H_v ≅ H¹(Q_v, J[2]) and J(Q_v)/2 sizes) — elementary but should be re-derived by the local audit, especially n_2 = 1 ⇒ dim J_2 = g.
- O4: the conditional local routine must return J_v inside the *same* W_L frame used to localize the global atoms (already a chain obligation).

Decisive falsifiers:
- F1 (kills the structural claim): a classical polynomial-bit algorithm, conditional only on factoring and GRH, computing (r_K, Im_K) for all odd-degree fields K in F_g — equivalently rank₂ Cl_S(K) to within g for F_g. This would also collapse the quantum/classical comparison for this endpoint.
- F2 (kills the bracket): a computed f ∈ F_g with dim Sel² < r_K or > r_K + g.
- F3 (kills Lemma 1 use): an element of L(S,2) with locally square norms at all v ∈ S_Q but globally non-square norm — impossible by the injectivity shown, so this would indicate a misidentified S.
- F4 (kills the Im-certificate): a genuine S-unit family whose localizations have isotropic span of dimension ½ dim W_K yet miss some global class — contradicts Lemma 4.

Not established and not claimed: any superpolynomial separation; nonconstancy of rank₂ Cl_S on F_g with fixed cheap data; polynomial computability of Im_K for quadratic factors.