# Cassels–Tate global descent (Shukla thesis, Alg. 1 steps 13–20): compression report

**Labels.** [SRC] = read from the attached excerpt. [DED] = my deduction, with a checked sketch. [OBL] = unproved proof obligation. [SPEC] = speculation.

## 0. Verdict

- **No exact compression is found for the native, no‑promise task.**
- **Good elements (Assumption 4.4.3):** §4.4 already supplies a polynomial‑degree compression. The global object is one conic point over the ordered‑pair étale algebra, of degree 2g(2g+1). This conditional endpoint is polynomial in (g,B) modulo the obligations in §4 below.
- **Non‑good elements:** the missing map can be stated exactly. One must explicitly split a corestriction of a quaternion algebra over a degree‑2g étale algebra. Its natural expanded form has dimension 4^{2g}·[k(θ₁):Q]. The CSA solver interface cannot accept it, and "index = period" gives only existence.
- **Local readout:** Eq. 4.3.7 carries a separate, unresolved superpolynomial‑in‑g risk, even for good elements.
- **Scope:** none of this is a lower bound against other algorithms.

## 1. Cheapest decisive attack: where steps 13–20 really pay

Write l = 2g+1. Work over L = k(θ₁) (loop at line 14, at most l factors). Let A′ = L[y]/(f(y)/(y−θ₁)), which has degree n = 2g.

| Step | Object | Size | Status |
|---|---|---|---|
| 13 | K = L(√d₁,…,√d_l). Since d_i ∈ k(θ_i), K contains k(J[2]). Gal ⊆ C₂^{l−1}⋊S_{l−1} [SRC §4.3.4]. | up to 2^{2g}(2g)! | exponential |
| 17 | E₁, E₁,g: 2‑cocycles on Gal(F/K′), values in K^× | same domain | exponential as tables |
| 18 | e₁, e₁,g with ∂e = E ("bottleneck", Magma generic) [SRC end §4.3.1] | crossed product over F | exponential |
| 19 | t₁,g ∈ F^× via Prop 4.3.8: φ = Σ_{τ∈H} … over H = Gal(F/K′) | |H| terms in F | exponential |
| 20 | c₁,g ∈ F^× via Remark 4.3.12 | same | exponential |

Lemma 4.3.16 / Remark 4.3.17 [SRC] reduce step 18 to N = Gal(F/K′(J[2])) ≅ C₂^{l−1} (generic case) with S_{l−1}‑equivariance. This shrinks the domain to 2^{2g} points. The values still lie in K, and "symbolic definition and specialisation" still names the full field. So the reduction alone does not compress.

Cor. 4.3.14 [SRC] is also not a shortcut. It says ε′₁ = s∪2a′₁ + f∪a′₁ exists once α lifts to β ∈ Z¹(G_k, J[4]). Ш²(J[2]) = 0 (Prop 4.3.13) guarantees existence only. Computing β is an explicit lift through the J[4]‑extension, i.e. a 4‑descent‑type trivialisation over k(J[4]). Using it here would be circular [DED].

## 2. What Eq. 4.3.7 actually consumes

γ₁,v = (a_v − ∂b_v)∪a′₁,v − b_v∪∂a′₁,v − ε₁,v [SRC §4.3.3].

- ε₁ is trivial when χ′₁(ρ) = 1 (Prop 4.3.6, Eq. 4.3.3).
- The readout uses only ε₁(σ,−1) and ε″₁(σ,−1), for σ in a decomposition group.

So the global data needed is:

- an H‑equivariant 1‑cochain e: N → K^× with ∂e = res_N E₁;
- e₁,g, t₁,g, c₁,g (or §4.4's replacement for them);
- all of it evaluable at places in S_{a,a′} to polynomial v‑adic precision.

Two constraints follow:

- **No local substitute.** Replacing the global ε₁ by independent local trivialisations shifts each local invariant by an arbitrary element of Br(k_v). That destroys the reciprocity the pairing relies on [DED].
- **Compression needed.** A compressed representation must be a small circuit n ↦ (product of elements from polynomial‑degree étale algebras, with known embeddings into K).

## 3. Brauer bookkeeping: per‑pair quaternions and a corestriction

**Per‑pair quaternions [SRC + DED].** §4.4 defines conics C₁ⱼ: d_j u² − d₁ v² + θ_j − θ₁ = 0 over k(θ₁,θ_j). Homogenising and scaling by d_j shows C₁ⱼ has a point iff

  Q_j := (d₁d_j, d_j s₁ⱼ) = (d₁d_j, −d₁ s₁ⱼ) = 0 in Br(k(θ₁,θ_j)), with s₁ⱼ = θ₁ − θ_j.

(The two symbols differ by (d₁d_j, −d₁d_j) = 0.)

**Pair‑algebra form [DED].** Choosing compatible points (Assumption 4.4.3, Galois clause) is the same as one point over the ordered‑pair algebra A⁽²⁾ = (A⊗A)/(diagonal), of degree l(l−1). Hence:

  d good ⇔ Q := (d(x)d(y), −d(x)(x−y)) = 0 in Br(A⁽²⁾).

**Cocycle check [SRC + DED].** With p₁ⱼ = √d₁u_j + √d_jv_j, the source has g_j(p₁ⱼ)p₁ⱼ = s₁ⱼ and g_k(p₁ⱼ) = −p₁ⱼ for k ≠ j (§4.4). I recomputed that a b_j with the anti‑invariance demanded by Lemma 4.4.1 exists in the right eigenspace iff Q_j splits. The relevant eigenspace is the fixed field of ⟨g_k : k≠j⟩, which is k(J[2])(√(d₁d_j)).

**Obligation [OBL‑P1].** The total class satisfies [res_N E₁] = Σ_{j≥2} Q_j|_{k(J[2])}, and Σ_j Q_j = 0 after the restriction the algorithm needs. The source gives triviality in Br(K′) (Props 4.3.2, 4.3.13, Cor 4.3.14). The identification with Σ Q_j, and its sign conventions, are my derivation and not checked:

- E₁|_N is symmetric with values in k(J[2])^× [SRC]. So the extension is abelian, and its class is a sum of cyclic pieces along the dual characters ψ_j ↔ √(d₁d_j).
- Consistency check: Σ_j(d₁d_j, s₁ⱼ) and Σ_j Q_j differ by (d₁^{l−2}∏d_i, −d₁) = (d₁, −d₁) = 0. This uses ∏d_i ∈ k^{×2} [SRC §4.3.4] and l odd.

**Corestriction form [DED, given P1].** Q_j are the conjugates of one quaternion Q_{θ₁} over A′. So the global constraint reads Cor_{A′/L}(Q_{θ₁}) = 0, or is killed by L → K′. Since Q_j = (d₁, s₁ⱼ) + (d_j, −d₁s₁ⱼ), the projection formula gives

  Cor(d₁, s₁ⱼ) = (d₁, f′(θ₁)),

a single polynomial‑size L‑quaternion. The residual obstruction is therefore Cor_{A′/L}(d(y), −d(θ₁)(θ₁−y)).

**Dichotomy (conditional on P1).**
- Good means each tensor factor splits with S_{l−1}‑compatible data.
- Non‑good means only the tensor‑induced product ⊗_j Q_j splits.

## 4. Conditional endpoint: good elements

**Construction.** This is §4.4 with explicit costs.

1. **Small representative mod squares [OBL‑REP].** The Selmer interface returns compact (S‑unit‑product) representatives. Expanding them can cost exponential bits, for example a fundamental unit of height around √disc. Replace d by d̃ = dγ², with γ found by lattice reduction in Minkowski space against the compact log‑embedding. Minkowski/LLL heuristics give coefficients of poly(g,B) bits. This needs a proof, including the precision of the compact log‑embedding. Otherwise the conic coefficients d₁, d_j are not legal expanded input to the CSA solver.
2. **Pair algebra.** Factor f(y)/(y−x) over each k(θ) to get the fields E of A⁽²⁾. Each has [E:Q] ≤ 2g(2g+1). This is classical polynomial time.
3. **Goodness test.** Test whether Q splits by Hilbert symbols at places of E over 2·∞·disc·N(d̃) (quantum factoring). Alternatively, the CSA solver decides it directly.
4. **Conic point.** Pass Q, expanded over Q with dimension 4[E:Q] = O(g²), to the CSA solver. Take a primitive idempotent, then a nilpotent pure quaternion, then an isotropic vector, then (u_j, v_j) with u_j v_j ≠ 0 and W ≠ 0 via a line through the point. The output is an arithmetic DAG. **[OBL‑CON]** The DAG must evaluate at places of S_{a,a′} to polynomial precision without dividing by elements of large v‑valuation.
5. **Global cochain.** e₁ comes from Lemma 4.4.1:
   e₁(g_{i₁}⋯g_{i_t}) = ±∏p₁ᵢₘ / ∏E(…),
   and ε₁ from Eq. 4.4.1, including the 1/p₁ branch. This replaces steps 17–20 entirely; no t₁,g, c₁,g or global H90 is needed (Prop 4.4.4 [SRC]). The circuit size is O(l) pair‑algebra elements per evaluation.

**Cost.** This is polynomial in (g,B) given OBL‑REP, OBL‑CON and the CSA solver contract, for each good d. Prop 4.4.4 assumes the generic group (C₂^{l−1}⋊S_{l−1})×C₂ and K∩K′ = k; the general case is restriction [SRC]. No cost is claimed beyond that.

**Local readout obligation [OBL‑L1].** This sits outside steps 13–20 but is needed for compatibility with Eq. 4.3.7.
- ω₁,w lies in K_w, the completion of the field containing all roots (Alg. 2 line 32).
- At an unramified p, the decomposition group is cyclic of order lcm(residue degrees), with residue degrees summing to ≤ 2g+1. That order can exceed any polynomial in g (standard Landau‑function growth; not from the attachment).
- Remark 4.3.12's H90 sum has that many terms.
- A polynomial endpoint must therefore compute the invariant of γ₁,v without expanding K_w. One option is to express it as Hilbert symbols over local pair fields using the product form of ε₁ [SPEC]. The source gives no complexity bound.

The local points b_v (Alg. 1 lines 3–12) are also outside this scope. They must come from the LOCAL_KUMMER interface, and their cost must be charged.

## 5. Native endpoint: the exact missing map

**MAP‑NG.**
- **Input:** L = k(θ₁); A′; Q_{θ₁} over A′, polynomial size; the guarantee from P1.
- **Output:** a poly(g,B)‑size representation of an H‑equivariant e: N → K^× with ∂e = res_N E₁, plus the analogous e₁,g, t₁,g, c₁,g in F. It must be locally evaluable as in §2.

**Why the CSA solver does not supply MAP‑NG [DED]:**

1. **Q over A′ is non‑split by definition here.** Fed to the solver, Q yields a 2‑dimensional module over a quaternion division algebra. That certifies non‑goodness and nothing more.
2. **The algebra whose splitting encodes e is too large.** It is res Cor_{A′/L}(Q) ≅ ⊗_{j=2}^{l} Q_j, a crossed‑product‑type algebra of degree 2^{2g} over L, i.e. expanded dimension 4^{2g}[L:Q].
   - The solver needs expanded structure constants, which is exponential.
   - A tensor‑induced or norm‑form description is exactly the "succinct tensor product" input the interface excludes.
3. **Pure‑tensor splittings are exactly the good case.** A pure‑tensor rank‑one idempotent ⊗_j e_j, Galois‑compatible, descends to a splitting of Q over A′. So non‑good means every equivariant splitting is non‑product across the 2g factors. No polynomial bound on the "tensor rank" of such a splitting is known to me.
4. **Index = period helps only along an ordering.** Over a global field every nonzero 2‑torsion class has index 2. So P_k := Q₂+…+Q_k has a quaternion representative over a field containing θ₂…θ_k. That gives a sequential splitting, matrix‑product‑state‑like with bond dimension 2: at each step, split P_k ⊗ Q_{k+1} ⊗ P_{k+1}^op ≅ M₄(L_k), whose data has bounded dimension over L_k. But:
   - P_k lives on ordered prefixes, with algebra degree (2g)!/(2g−k+1)!, or on unordered k‑subsets, degree C(2g,k);
   - S_{2g}‑equivariance (Lemma 4.3.16, property 2) prevents choosing a prefix order inside a polynomial algebra.

   So index 1 of the total gives existence; bounded per‑step data still sits over exponential‑degree subset algebras. This pinpoints the gap. It is not a lower bound.
5. **Steps 19–20 are a second, dependent gap.** In the good case §4.4 eliminates t₁,g and c₁,g. Without a product‑form e₁, Prop 4.3.8 requires an H90 element of F built as a sum over Gal(F/K′). Whether t₁,g has a compressed norm‑form representation once e₁ is compressed is unproved [OBL‑H90].

**Strongest candidate repair [SPEC, unproved].** Seek a swap‑symmetric class R over the ordered‑triple algebra (degree O(g²) over A′) with Cor_{A″/A′}(R) = Q_{θ₁}. Symmetry makes the double transfer vanish mod 2, giving a "pairwise" certificate of Σ Q_j = 0.

- **Local feasibility looks plausible [DED sketch].** At a place where the root orbits carry invariants q_a with Σ q_a = 0, the q_a can be matched by symmetric pair‑orbit invariants, as for even‑degree vertices in a graph.
- **R1 [OBL]:** global realisation with explicit symbols, Grunwald‑type, needing auxiliary primes.
- **R2, the decisive one [OBL]:** cochain‑level realisation.
  - Cor_{A″/A′} of a quaternion is again a degree‑2^{2g−1}‑type object unless R has projection form res(x)∪y. Then Cor(R) = (x, N(y)) is polynomial‑size.
  - Swap symmetry and projection form conflict in the obvious ansätze.
  - Until R2 is resolved there is no construction.

## 6. Certifying a good generating basis

**Goodness is a quadratic condition [DED, unchecked].** Define q(d) = Q over A⁽²⁾, mapped to the vector of local invariants at relevant places, an element of F₂^m with m = poly. Expanding,

  q(dd′) = q(d) + q(d′) + b(d,d′), where b(d,d′) = (d(x)d(y), d′(x)) + (d′(x)d′(y), d(x)).

b is bilinear, so q is a quadratic map Sel → F₂^m.

**Consequences:**
- Good elements are the zero set of a system of m quadratic forms in r = dim Sel variables. They are generally not a subgroup.
- Certifying "good elements plus the image of J(k)/2J(k) have index ≤ 2" (Def. 4.4.5) means finding zeros spanning a hyperplane: an MQ‑type search. The attached material gives no method avoiding 2^r enumeration.
  - If b vanishes on Sel, q is linear and linear algebra suffices.
  - Chevalley–Warning guarantees zeros when r > 2m, but not efficiently or with spanning.
- The J(k)/2J(k) term needs Mordell–Weil data the native input does not provide.

**Enough goodness for the full matrix [SRC + DED].** Testing one element is polynomial. The pairing is alternating because T₀ is rational (PS99, cited by the source). So if good elements span a subgroup H of index ≤ 2, the full matrix follows: for x, y ∉ H, ⟨x,y⟩ = ⟨x+y, y⟩ with x+y ∈ H.

**Empirical scope [SRC finite control].** LMFDB genus‑2 counts, |A| ≤ 2000 for y² = x⁵+A, and Theorem 4.4.6 cover special cases only. The source reports good curves becoming scarce: about 74% at g = 3, about 30% at g = 4, none found at g = 5 in C_{p,g}. This is evidence that the conditional endpoint misses much of the native task as g grows. It is not a proof of anything.

## 7. Falsifiers and next checks (no computation performed)

- **F1, P1 control, cheapest.** The source lists two index‑2 genus‑2 curves. They are non‑monic, so convert them to a monic integral model first. For a non‑good element, check Q_{θ₁} non‑split over A′ while Σ_j Q_j = 0. Failure falsifies the corestriction reformulation in §3/§5.
- **F2.** Exhibit a non‑good d with a poly‑size equivariant e satisfying ∂e = res_N E₁. This would falsify the claim that MAP‑NG is the gap, and would answer the question positively.
- **F3.** If b in §6 is not bilinear (for example, the sign conventions break it), the MQ framing fails.
- **F4.** Show that Eq. 4.3.7 can be read from pair‑field Hilbert symbols in the good case. That would close OBL‑L1.

**Proof obligations, in order:** P1; OBL‑REP; OBL‑CON; OBL‑L1; OBL‑H90 (native only); R1, R2 (speculative route).