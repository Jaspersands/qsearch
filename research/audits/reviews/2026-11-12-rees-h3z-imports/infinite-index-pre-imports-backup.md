# HSP for arbitrary subgroups of H_3(Z) = UT_3(Z), and what carries to UT_n(Z) (2026-11-12)

**Status: AI-checked, pending human review.** One Claude Code helper session wrote the
derivations, plus one independent AI referee pass (§8). The finite checks in
`2026-11-12-rees-h3z-infinite-index/` are exact or numerical simulations. They can only
falsify (TRAPS 7). No paper, `STATE.md`, handoff or registry file was edited, and no git
command was run. Claim gates are unchanged: `speedup_claim_allowed` and `novelty_established`
stay false. There is no application: f is an arbitrary oracle.

**Verdict.**
* Every subgroup H with H ∩ Z(G) ≠ 1 is found in quantum polynomial time (Theorem A, proved
  given Kuperberg Thm 1.5/7.1 and cor:utz; AI-checked and refereed twice by AI, pending human
  review).
* The only remaining case is H = ⟨h⟩ with h non-central and H ∩ Z = 1, or H = 1. This case
  reduces in polynomial time to a classical **zero-sum problem over R/Z at precision
  2^{-Θ(b)}** for exactly uniform samples (Theorem B1, CONDITIONAL on Kuperberg's Z^2 step
  accepting state-valued labels). It is solvable in time 2^{O(√(b + log 1/ε))} (Theorem B2,
  CONDITIONAL on the same import and on the standard uniform BKW sieve analysis).
* Polynomial time is UNKNOWN. Within the central-character twist template (ISS-type), success
  **requires solving a quadratic zero-sum problem QZS** (Proposition N, PROVED for that
  template; sufficiency of QZS is argued, not proved).
  No polynomial algorithm is known to us for QZS.
* HSP(UT_3(Z)) reduces to HSP(UT_n(Z)) for every n ≥ 3 (Proposition U1, PROVED). So the open
  case persists for every n. Subexponential time for UT_n(Z) is a sketch only (UNKNOWN).
* So the survey's open problem 5 (ePrint 2026/2678 §10) is **not solved in polynomial time
  here**. It is reduced to one explicit classical problem, plus a subexponential algorithm.

## 0. Model and conventions

G = H_3(Z). Elements are (a,b,c), meaning the matrix [[1,a,c],[0,1,b],[0,0,1]], with
(a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab'). So x = (1,0,0), y = (0,1,0), z = (0,0,1) = [x,y],
(a,b,c)^t = (ta, tb, tc + C(t,2)ab), and Z = Z(G) = ⟨z⟩. π: G → Z^2 is the projection to (a,b),
and ω(u,v) = u_1v_2 − u_2v_1.

The oracle is f with f(g) = f(g') ⟺ g^{-1}g' ∈ H (left cosets, as in cor:utz), labels of width
w, coherent on the matrices with entries in (−2^B, 2^B). B = poly(b) is chosen by the algorithm.

**Deviation from cor:utz.** The corollary uses the box [0,2^B). For infinite-index H, signed
entries are needed. For example, H = ⟨(−1,2,0)⟩ has no generating set with non-negative
entries, since every non-trivial element (−t, 2t, −t(t−1)) has a negative entry (referee fix:
an earlier draft wrongly said its only generators are h^{±1}). The size parameter b bounds the entries
(|·| < 2^b) of some generating set of H, and the output is generators of H.

Every statement below is for every H ≤ G satisfying this bound, unless noted.

## 1. Structure

**Lemma C (PROVED).** If H ∩ Z = 1, then H is trivial or infinite cyclic, and H ⊆ A_v :=
π^{-1}(Zv) for a primitive v ∈ Z^2.

*Proof.* [H,H] ⊆ H ∩ Z = 1, so H is abelian, and π|_H is injective. If π(H) had rank 2, then two
elements u, u' with independent projections would give [u,u'] = z^{ω(πu,πu')} ≠ 1, a
contradiction. So π(H) ≅ H is cyclic or trivial, and it lies on a line Zv. ∎

A_v = ⟨g_v, z⟩ with g_v = (v_1,v_2,0) is abelian and isomorphic to Z^2 via
(t,s) ↦ g_v^t z^s. In coordinates, (tv, c) ↦ (t, c − C(t,2)v_1v_2).

**Lemma E (PROVED).** If H ∩ Z = ⟨z^e⟩ with e ≥ 1, then e ≤ 2^{3b+1}.

*Proof.* Let rk denote rk π(H).
* rk 0: e is the gcd of the central generators, so e < 2^b.
* rk 2: two generators have independent projections, and their commutator is z^d with
  1 ≤ |d| ≤ 2^{2b+1}. So e ≤ 2^{2b+1}.
* rk 1: π(H) ⊆ Zv with v primitive. A generator (t_iv, c_i) has A_v-coordinates
  (t_i, c_i − C(t_i,2)v_1v_2). Here |t_i| < 2^b, and |C(t_i,2)v_1v_2| ≤ |t_i|(|t_i|+1)|v_1v_2|/2
  ≤ (2^b − 1)^2 (this also covers negative t_i). So the first coordinate is below 2^b and the
  second below 2^{2b}. H is a rank-2 lattice in
  A_v ≅ Z^2 (it contains z^e and some element with t ≠ 0). Its index is at most |det| of two
  independent generators, which is < 2·2^b·2^{2b}. The index equals d·e, where dZ is the
  projection to the t-axis. So e ≤ 2^{3b+1}. ∎ (Referee tightened the constant from 4b+1 to
  3b+1.)

[computed] `h3z_struct.py` builds an induced polycyclic basis for 4,000 random generating sets
(b ≤ 5, a third of them forced to rank-1 projection). It found:
* every instance with H ∩ Z = 1 is cyclic (1,297/1,297);
* e ≤ 2^{4b+3} (the script's test, weaker than the proved 2^{3b+1}) in 2,703/2,703, with
  max bitlen(e)/b = 2.4, inside the proved 3 + 1/b;
* 20 random words per instance sift correctly (0 failures).

Output: `h3z_struct.out`.

The constant in Lemma E is sharp up to a factor 2. For v = (1,1), t_1 = 2^b − 1 and
t_2 = −(2^b − 2), e ≈ 2^{3b}, with e/2^{3b+1} → 1/2 (second referee, `struct_referee.py`;
exhaustive two-generator search agrees for b ≤ 3). The ratio 2.4 above reflects random
sampling only, so Step 1 really needs Q ≈ 2^{6b+3}.

## 2. Theorem A: H ∩ Z ≠ 1 is polynomial

**Theorem A (proved given cited theorems: Kuperberg 2025 Thm 1.5 via its Thm 7.1, and cor:utz,
itself AI-checked, pending human review; second referee 2026-11-12-rees-h3z-referee.md).**
There is a quantum algorithm with the following guarantee. Input: b ≥ 1, ε ∈ (0,1), and an
oracle for f as in §0, coherent on matrices with entries in (−2^B, 2^B), where
B = B(b) = max(20b+11, 2P_K + 3b + 3) = poly(b) and 2^{P_K} bounds the entries of Kuperberg's
query vectors at answer size n_L = O(b). Promise: H has a generating set with all entries of
absolute value < 2^b. If H ∩ Z ≠ 1, the algorithm returns generators of H, with entries of
bit size poly(b), with probability ≥ 1 − ε. It decides whether H ∩ Z = 1, and the answer
"H ∩ Z ≠ 1" is always correct. It uses poly(b, log 1/ε) queries and poly(b, w, log 1/ε) gates.
b must be given: doubling is sound for Step 1 alone, not for the whole theorem (a failed run
returning too small an S cannot be detected, and with H ∩ Z = 1 doubling never stops).

Imported results:
* Kuperberg 2025, arXiv:2507.18499v1, Thm 1.5 (HSP in Z^k for arbitrary hidden subgroups,
  poly(k, n) with n the bit complexity of the answer, elements of Z^k in binary) and its proof
  Thm 7.1 / Algorithm A (§7.1, read in the PDF on 2026-11-12). Algorithm A applies the
  hiding function only on the cube ‖x‖_∞ < Q/2, with Q, R, S, T of order exp(poly(n)), and
  Thm 7.1 says it "succeeds with good probability". Thm 1.8 is the one labelled outlined;
  Thm 7.1 is proved in §§7.4–7.8 (not checked here). Cor 1.7 pulls back to Z^k, as below.
* Shor/Kitaev period finding (Mosca–Ekert §§2, 4.2, not re-read).
* cor:utz / rem:utz-scope(b) for finite index in H_3(Z): ISS 2012 for q ≥ 3 and
  Imran–Ivanyos 2023 Thm 1 for q = 2.

*Algorithm and proof.*
1. **Detection.** Run period finding on t ↦ f(z^t), t ∈ [0, 2^{6b+3}). Accept a candidate r
   with 1 ≤ r ≤ 2^{3b+1} only if f(z^r) = f(1). This test holds iff e | r, so every accepted
   value is a positive multiple of e. A run whose outcome is close to jQ/e with gcd(j,e) = 1
   returns exactly e (Q = 2R^2, R = 2^{3b+1}), with probability Ω(1/log log e). Other outcomes
   may return proper multiples of e: e = 3, b = 1, outcome 34 of Q = 512 gives the convergent
   1/15 and r = 15, which passes (second referee, `step1_sim.py`; recomputed). Let ê be the
   **gcd** of all values accepted in O(log b · log 1/ε) runs. Then e | ê, and ê = e with
   probability ≥ 1 − ε/4. If H ∩ Z = 1, nothing is accepted. So "H ∩ Z ≠ 1" is always
   certified, and "H ∩ Z = 1" is wrong with probability ≤ ε/4. Queries: z^t, 0 ≤ t < 2^{6b+3}.
   (An earlier draft took the lcm and said only e passes; both wrong.)
2. **Abelian layer.** Let A = ⟨x^e, y, z⟩ = π^{-1}(eZ × Z), a subgroup of index e. Modulo
   ⟨z^e⟩ it is abelian, since [x^e, y] = z^e. The map x^{eα}y^βz^γ = (eα, β, γ + eαβ) ↦
   (α, β, γ mod e) is an isomorphism A/⟨z^e⟩ → Z^2 × Z_e (checked in `h3z_struct.py` and the
   referee's `struct_referee.py` on random signed pairs). Since z^e ∈ H, F̃(α,β,γ) =
   f(x^{eα}y^βz^γ) on Z^3 hides the lattice L = ψ^{-1}(S) ∋ (0,0,e), S = (H∩A)/⟨z^e⟩. This is
   Kuperberg's proof of Cor 1.7. L has a basis with entries < 2^{4b+2}: in rk 2,
   [Z^3:L] = [A:H∩A] ≤ [G:H] < 2^{4b+2}; in rk 1 the basis is (u'_1, u'_2, γ_0), (0,0,e) with
   |u'_2| < 2^{4b+1}; in rk 0 it is (0,0,e). So the answer size is n_L = O(b). Run Algorithm A
   at that n_L. Its queries have entries < 2^{P_K}, P_K = poly(n_L), so the matrix entries are
   < e·2^{2P_K} + 2^{P_K} < 2^B. Repeat O(log 1/ε) times and keep the vectors v with
   F̃(v) = F̃(0); every kept vector lies in L, and the lattice they generate is L with
   probability ≥ 1 − ε/4. (Assumes Thm 7.1 holds when run with an upper bound on n, and that
   "good probability" means a constant; not checked in §§7.4–7.8.)
3. **Rank of S** (it equals rk π(H), since π(h^e) ∈ eZ × Z for every h ∈ H):
   * rk 0: π(H∩A) = 0, so π(H) = 0 since eπ(H) ⊆ π(H∩A), and H = ⟨z^e⟩.
   * rk 2: [G:H] = [Z^2:π(H)]·e ≤ d^2 < 2^{4b+2}, where d = ω(πg,πg') for two generators
     with independent projections (e | d). Apply cor:utz with index parameter b' = 4b+2 and
     error ε/2. Its box [0, 2^{20b+11}) lies inside the signed box, and the coset convention
     matches. For n = 3 it uses ISS 2012 (q ≥ 3) and Imran–Ivanyos 2023 Thm 1 (q = 2), and not
     Thm is-import. cor:utz is AI-checked, pending human review.
   * rk 1: π(H∩A) = π(H) ∩ (eZ × Z) = Zu with u ≠ 0, so the primitive direction v = u/gcd(u)
     is read off any element of L with (α,β) ≠ 0, and H ⊆ A_v. Restrict f to A_v via
     ι(t,s) = g_v^t z^s = (tv_1, tv_2, s + C(t,2)v_1v_2). Then f∘ι hides L_v = ι^{-1}(H), of
     index d·e < 2^{3b+1}. The HNF row (u'_1, u'_2, γ_0) of L gives
     (eu'_1, u'_2, γ_0 + eu'_1u'_2) ∈ H, with A_v-coordinates (t_0, s_0), |t_0| < 2^{4b+1}. So
     N = e|t_0| < 2^{7b+2} satisfies NZ^2 ⊆ L_v. Finite abelian HSP in Z_N^2 (Kitaev /
     Mosca–Ekert), queried on [0,N)^2, returns L_v with error ε/2; the matrix entries are
     < 2^{16b+5}. Output ι of an HNF basis of L_v.

   [computed] For 661/661 rank-1 instances, H ∩ A contains h^m, the direction v is correct,
   and every basis element lies in A_v. The referee's check regenerates H from ι(basis) and
   z^e on 357 instances.

The outputs generate H itself: z^e (rk 0), ι(HNF basis of L_v) (rk 1), cor:utz's output (rk 2).
Every step except Kuperberg's queries the box of exponent max(6b+4, 16b+6, 20b+11) = 20b+11;
Kuperberg's step needs 2P_K + 3b + 3 = poly(b). So B = poly(b), not O(b) as an earlier draft
said. Errors: ε/4 + ε/4 + ε/2 = ε. ∎

*Remark (Kuperberg Cor 1.9 is not enough here).* G/⟨z^e⟩ is virtually abelian, and f descends
to it, so the reduction to it is legitimate once e is known. But Cor 1.9 gives only
2^{O(√n)}, and it is stated for a fixed group. Its dependence on the index e of the abelian
subgroup, which can be exponential here, is not stated in what I read (UNKNOWN). Theorem A
instead uses the specific abelian subgroup A, whose index e enters only through bit sizes.

## 3. The open case: H = ⟨h⟩, h = (a,b,c) non-central, H ∩ Z = 1

Write w = (a,b) = π(h) and K = HZ. K is abelian and **normal**, since K ⊇ Z ⊇ G'. If H has a
generating set of bit size b, then |a|,|b| < 2^b and |c| < 2^{2b+1}, because h^k = (ka, kb,
kc + C(k,2)ab).

**Central-character states.**
1. Measure f on Σ_g|g⟩|f(g)⟩ to get |aH ∩ box⟩.
2. Apply the QFT to the central coordinate and measure ρ. This leaves the chirp line state
   Σ_t e^{2πiθ c_t}|π(ah^t)⟩, with θ = ρ/N_0 known.
3. Re-append Σ_{r<N} e^{-2πiθr}|r⟩.

The result is ψ_θ(a) = Σ_{r<N} e^{−2πiθr}|a z^r H⟩, truncated in r and in t. It is the ISS
Lemma 4 state for the infinite centre. **θ is exactly uniform** on (1/N_0)Z/Z for every h.
The points π(ah^t) are distinct basis states, so P(ρ) = Σ_t (1/T)(1/N_0) = 1/N_0 (referee
correction: an earlier draft wrongly claimed concentration when ab = 0). If x'x^{-1} = h^τz^σ, then right translation gives
ψ·x' = e^{2πiθσ} ψ·x, up to a truncation error O(|σ|/N + |τ|/T).

[computed] On explicit truncated vectors (`twist_check.py` Part B, N = 4000, 36 pairs):
* the phase error is ≤ 6e-14;
* the overlap equals 1 − |σ|/N to within 1e-13;
* the overlap across different K-cosets is 0.

**The twisted product.** Ψ(g) = ⊗_{i} ψ_{θ_i}(a_i)·φ_i(g).
* For φ_i = id, factors for different K-cosets are orthogonal, because a_iKg ≠ a_iKg'.
* For g' = gk, k = h^tz^s ∈ K, Ψ(gk) = e^{2πiΘ(s + tΩ(g))}Ψ(g). Here Θ = Σ_iθ_i mod 1 and
  Ω(g) = ω(π(g), w).

So Ψ hides K exactly when Θ ∈ Z. When ‖Θ‖ ≤ δ, it hides K up to errors δ·(|s| + |tΩ|).
Fourier sampling of u ↦ Ψ((u,0)) over [0,M)^2 then sees the rank-1 lattice Zw. The phase
e^{2πiΘtc}, from the section's central offsets, is negligible once δ·M·|c| is small.

**Required precision.**
* To find w with entries up to 2^b, the box needs M ≥ 2^{b+Ω(1)}.
* The relevant |s| + |tΩ| reach M^2|w| + M|c|.

So δ = 2^{−K} with K = Θ(b + log 1/ε) in the worst case. This is the cost driver. If δ were
1/poly, then prefix-sum pigeonhole on poly many θ's would finish in poly time.

[computed] `e2e_fourier.py` (h = (2,3,5), M = 18; Gram matrix from the Part-B law): the
Fourier mass on ‖⟨y,w⟩/M‖ ≤ 0.1 is
| setting | mass |
|---|---|
| Θ ≈ 1e-6 (2 or 3 factors) | 0.657 |
| one factor | 0.115 |
| Θ = 0.37 | 0.149 |
| uniform baseline | 0.167 |

**Problem BZS(n, K).** Given n i.i.d. central characters θ_i ∈ R/Z, find disjoint nonempty
subsets S with ‖Σ_S θ_i‖ ≤ 2^{−K}. (Precision 2^{-K-n} on the θ_i is free, since N is ours.)

**Theorem B1 (CONDITIONAL on import I1: Kuperberg Thm 1.5 is single-query Fourier sampling
plus classical LLL, so its analysis depends only on the Gram matrix of the labels).** The HSP
for H ∩ Z = 1 reduces, with poly(b, log 1/ε) overhead, to the following: given n exactly
uniform samples θ_i, solve BZS(n, K) for poly(b) disjoint subsets, with K = O(b + log 1/ε).
The quantum cost is n coset states, plus memory for the largest subset.

The final step proceeds as follows:
* By a hybrid argument, Ψ is η-close to an exactly coset-constant Ψ'.
* The Fourier distribution depends only on the Gram matrix ⟨Ψ(u)|Ψ(u')⟩, so Kuperberg's Z^2
  analysis applies to state-valued labels. This holds if his algorithm uses f only for
  Fourier sampling plus LLL, as his §1 states; §7 is not read, which is the CONDITION.
* Fourier sampling gives the direction v of w.
* Restrict f to A_v and run Kuperberg Thm 1.5. A wrong v gives H ∩ A_v = 1 by Lemma C, so a
  **non-trivial** output is never wrong.
* "H = 1" is reported when no candidate yields a non-trivial subgroup; this report is wrong
  with probability ≤ ε.

**Theorem B2 (CONDITIONAL on I1 and on Sieve Lemma S).** The case H ∩ Z = 1 is solved with
2^{O(√(b + log 1/ε))} queries, time and quantum memory.

*Sieve Lemma S.* From 2^{O(√K)} i.i.d. uniform samples on (1/N_0)Z/Z, the BKW-type
pairing sieve finds poly(b) disjoint subsets of size 2^{O(√K)} with sums within 2^{−K}. The
sieve uses ℓ ≈ √K levels; at each level it pairs x with y in the opposite bucket, using sums
only, as the twist requires.
This is the standard BKW / Kuperberg-type analysis, which is not re-derived here. Since θ is
exactly uniform (above), no distribution-robust version is needed.

[computed] `sieve_demo.py` (uniform θ):
| K | samples | subset size | log2‖Θ‖ |
|---|---|---|---|
| 16 | 2^11 | 16 | −21.3 |
| 32 | 2^15 | 64 | −44.0 |
| 48 | 2^17 | 128 | −55.7 |

This is a demo of the scaling, not of the lemma.

## 4. Proposition N: the twist template needs a quadratic zero-sum (PROVED for the template)

**Template.**
* Factors ψ_{θ_i}(a_i) as above.
* Right-translation maps φ_i: G → G, chosen independently of H. They must keep supports
  matched for every possible K: φ_i(gk)φ_i(g)^{-1} ∈ K for k ∈ K.
* An arbitrary H-independent phase function Φ̃ on the sampling register.
* Required outcome: Ψ(gk) = e^{2πiχ(k)}Ψ(g) up to δ on the box, for k ∈ K, with χ a character
  trivial on Z.
  *Why χ|_Z ≈ 0 is the right target (referee gap, now justified).* If χ(z) ∉ Z, then Ψ does not
  descend to G/Z. It is then an object of exactly the original type: a central-character
  state with character χ(z). A single factor is the case χ(z) = θ_1. Example: φ_i = g^{-1}
  for every i gives Ψ(gk) = e^{−2πiΘs}Ψ(g), a genuine character of K for every Θ (Part A:
  α = −1, β = 0). On the section r = 0, the offsets s(u,t) contain C(t,2)ab and b·u_1·t, so
  the abelian sampling on Z^2 sees a chirp, not a lattice. The template's goal is to descend
  to the abelian G/Z, and that is what χ|_Z ≈ 0 encodes.

**Claim.** In this template, φ_i induces u ↦ μ_iu + c_i on G/Z with μ_i ∈ Z, and success for
both H = ⟨x⟩ and H = ⟨y⟩ forces ‖Σ_iθ_iμ_i²‖ ≤ 5δ.

*Proof.*
1. **Shape of φ_i.** The support condition for every line gives Φ(u+v) − Φ(u) ∥ v for all
   u, v ∈ Z^2. Then Φ(v) − Φ(0) = λ(v)v, and comparing with u, v independent forces λ to be
   constant. So φ(g) = δ_μ(g)·c̃·z^{F(g)}, where δ_μ(p,q,r) = (μp, μq, μ²r) is an injective
   endomorphism.
2. **Per-factor law.** φ(gk)φ(g)^{-1} = δ_μ(gkg^{-1})·z^{F(gk)−F(g)}, and
   δ_μ(h) = h^μ z^{(μ²−μ)c'} with c' = c − ab/2. So the factor phase is
   θ[μ²(s + tΩ(g)) + (μ²−μ)c't + F(gk) − F(g)]. The last term is a coboundary and the middle
   one a character.
3. **Commutator loop.** Collect Θ = Σθ_iμ_i² and all coboundaries into one real function
   P(g). Write the conditions for k = x (when H = ⟨x⟩), k = y (when H = ⟨y⟩) and k = z. Sum
   them around the loop g → gx → gxy → gxyx^{-1} → gz. The increments of P give
   P(gz) − P(g) ≡ −2Θ, while the central condition gives P(gz) − P(g) ≡ χ(z) − Θ ≡ −Θ.
   Hence Θ ≡ 0, with five δ-errors. ∎

[computed] `twist_check.py` Part A fits σ = αs + βtΩ + γt for 10 maps:
* the maps are id, g^{-1}, δ_2, δ_3, δ_2^{-1}, g^3, g^{-2}, δ_1δ_2, δ_2δ_3^{-1}, δ_3g^2;
* this covers 40 random h, with 30 (g,k) each;
* the residual is ≤ 2e-11, and the invariant 2β − α = μ² holds in every case, with 0 failures.

So within the template, solving **QZS** is necessary. Sufficiency is argued, not proved. If
Σθ_iμ_i² ∈ Z, then with φ_i = δ_{μ_i} the leftover phase is the character e^{2πiAc't},
A = Σθ_i(μ_i²−μ_i). This character is trivial on Z. Fourier samples (y, A/2) then annihilate
(a, b, 2c'), and the product hides a lattice with the direction of K; with a common factor m
of the μ_i, the lattice is larger, which is harmless.

QZS:
* Find μ ∈ Z^n∖0 with |μ_i| ≤ 2^{poly} and ‖Σθ_iμ_i²‖ ≤ 2^{−K}.
* The virtual phase removes the linear ISS equation; only the quadratic one remains.
* Binary μ is BZS.
* In the finite Heisenberg group over F_p, QZS is easy: θ_1μ_1² + θ_2μ_2² ≡ 0 is solved by a
  square root mod p half the time, and three variables always suffice.
* Over Z, the truncation forces |μ| ≪ √N. So the infinite case is hard exactly where the
  finite case was easy.

Attempts that did not give poly time (all UNKNOWN, not hardness, TRAPS 8):
* Coppersmith/LLL linearization in μ_i²: it finds only unusually short solutions, of size
  δ^{-1/(2n)}, whereas generic solutions need δ^{-1/n}.
* Simultaneous Diophantine approximation followed by squaring: residual q·‖qθ‖ ~ 1.
* Products of maps δ_{m_1}δ_{m_2}: they give W_s = m_1² + m_2² but keep the invariant μ².
* Non-scalar endomorphisms: different factors then hide different lines, so the product
  hides only Z.
* Restricting to Lie-coordinate planes: f is injective off one unknown line.
* The matrix plane r = 0: it hides an affine reflection, which is dihedral-like.

Outside the template, and not excluded: entangled or adaptive measurements, BCvD-type PGM
on several copies, and H-dependent maps.

## 5. UT_n(Z), n ≥ 4, and nilpotent groups

**Proposition U1 (PROVED).** For every n ≥ 3, the HSP in UT_3(Z) reduces to the HSP in UT_n(Z),
with one query per query and bit sizes preserved.

The top-left 3×3 block ρ: UT_n(Z) → UT_3(Z) is a surjective homomorphism. It is the identity
on the corner copy, and ker ρ is generated by the x_ij with j ≥ 4 (peel the entries). f∘ρ
hides ρ^{-1}(H), whose generators are corner lifts of the generators of H plus the x_ij,
j ≥ 4. Applying ρ to the output recovers H. So the open case of §3 persists for every n.
Polynomial time for all subgroups of UT_n(Z) would solve QZS-type instances only if the
template were forced; it is not, so that implication is not claimed.

**Known positive pieces.**
* Finite index: cor:utz, conditional on is-import for n ≥ 4.
* H ⊇ [G,G]: f descends to Z^{n−1}, then Kuperberg Thm 1.5 (PROVED, trivial).

**Sketch U2 (UNKNOWN; not proved).** For G f.g. torsion-free nilpotent of class c, the
right-coset form of §3 gives the following:
* Ψ(kg) = e^{2πiΘ s(k)}Ψ(g) for k ∈ HZ, with **no normality needed**: φ = id and
  ψ·kg = phase·ψ·g.
* So the binary sieve hides HZ(G) in G/Z(G), with a state-valued oracle.
* Recursion then yields HZ in 2^{O(c√K)}.
* Finally, H ⊴ HZ with abelian quotient. Restricting f, a hidden-shift-as-abelian-HSP step
  F(z,j) = f(g^jz) gives h_0 = gz_0^{-1} ∈ H for each generator g of HZ.

Open details: robustness of every level with approximate quantum labels; bit bounds for the
generators of HZ; H ∩ Z ≠ 1 with torsion in Z/(H∩Z); and Sieve Lemma S at each level. This is
consistent with the repo's Prop T (2026-11-12-rees-direct-twist-class3.md): route B with all
s_i = 1 is exactly the binary zero-sum.

## 6. Prior art

| Source | Read | What it covers |
|---|---|---|
| Kuperberg, arXiv:2507.18499v1 | [read] HTML §1 statements and input model; §7 not read | Thm 1.5: Z^k, arbitrary H, poly(k,n). Cor 1.7: f.g. abelian. Cor 1.9: virtually abelian, 2^{O(√n)}. Thm 1.8 (outlined): poly space. Nothing on nilpotent groups or H_3(Z) in the part read. H_3(Z) is not virtually abelian. |
| Di Concilio–Flores–Kahrobaei–Noce, ePrint 2026/2678 | [read] §9–10 via pdftotext | Restates Kuperberg Theorems 4–5. §10 item 5: "open whether the HSP in the discrete Heisenberg group H_3(Z) can be solved efficiently". Nothing beyond Kuperberg on infinite groups. |
| ISS 2012 (arXiv 0707.1260); IS 2015; II 2023 | via repo notes (direct-twist-class3, utz) | Finite nil-2: twists φ_j, system Σu_ij_i = Σu_ij_i² = 0, solved by Chevalley–Warning over F_p; binary zero-sum open for large p. §3–4 is their mechanism transplanted. Over R/Z with the truncation, the easy F_p step turns into QZS. |
| BCvD 2005 | [not re-read] | Finite Heisenberg over Z_p (and Z_p^r ⋊ Z_p): PGM on several coset states reduces to quadratic equations mod p in measurement variables, the finite analogue of QZS. |
| RRS 2005 | [not re-read] | Finite Heisenberg: random-basis strong Fourier sampling (a different mechanism). |
| Wagner 2002, BKW, Lyubashevsky 2005 (subset sum) | [not re-read; recalled] | Random subset sum / k-list in 2^{O(K/log K)} or 2^{O(√K)}-type time. No poly(K)-sample poly-time algorithm known to me. Specialist check needed. |
| Repo corpus `been-tried` | [run] | No H_3(Z) infinite-index record. NEG-NILPOTENT-CENTRAL-DESCENT-BARRIER (dihedral 2-groups) is consistent with §5: central descent needs a sieve. |

New relative to the sources read (pending specialist check):
* Theorem A, the use of A = ⟨x^e,y,z⟩, which gives poly time where Cor 1.9 gives 2^{O(√n)};
* the reduction B1 to BZS;
* Proposition N;
* Proposition U1, which is elementary.

## 7. Adversarial self-check

* **Is e (or the bound) circular?** No. Lemma E bounds e by the generator bit size, and the
  algorithm uses only bounds derived from b (e < 2^{3b+1}, [G:H] < 2^{4b+2} in rank 2), so
  there is no circularity.
* **Kuperberg Cor 1.7 in step 2 needs the answer's bit size.** L has a basis with entries
  < 2^{4b+2} (index bound in rank 2, explicit basis in rank 1), so n_L = O(b). Kuperberg's
  query box is exp(poly(n_L)) (Algorithm A), so B = poly(b), not O(b).
* **Signed box.** Required (§0); with [0,2^B) the model cannot express some cyclic H.
* **Does Ψ hide K or only K's direction?** With φ = id, it hides exactly K = HZ.
  Orthogonality across cosets is exact (Part B: overlap 0).
* **Hidden normality use.** K is normal because G' ⊆ Z, which is used in the left form. The
  right form avoids it (§5).
* **Precision claim K = Θ(b).** The upper bound is proved. The claim that no smaller box or
  smarter sampling can avoid 2^{-Ω(b)} precision is argued only; it is not a lower bound.
* **Could QZS be easy?** Not excluded; see §4. Proposition N is a template statement, not
  hardness (TRAPS 8).
* **Finite checks.** All are falsification tools. Part B checks the law that e2e_fourier.py
  then uses, so e2e is not independent of Part B.
* **Theorem B2's dependence on Lemma S.** The θ-distribution is exactly uniform (referee
  correction), so only the textbook uniform-sieve analysis is assumed.

## 8. Referee (independent AI pass, no files edited)

| Item | Verdict | Disposition |
|---|---|---|
| Lemma C | CORRECT | — |
| Lemma E | CORRECT with small gaps (negative t, constant) | Fixed; e ≤ 2^{3b+1} |
| §0 | false reason given | Fixed |
| Thm A isomorphism, rank, A_v | CORRECT | — |
| Detection | GAP (divisors, not multiples; r = 0; success probability Ω(1/log log e)) | Partly fixed; the second referee found that accepted multiples were not handled (gcd fix) |
| §3 phase law and state preparation | CORRECT | — |
| D_h non-uniform | WRONG: θ is exactly uniform | Fixed; Lemma S simplified, next command redirected |
| Prop N | CORRECT given χ on Z trivial, but that assumption was unjustified (counterexample g ↦ g^{-1}) | Justification added: χ(z) ≠ 0 does not descend to G/Z |
| Prop N sufficiency | Only necessity proved | Relabelled; sufficiency argued |
| U1 | CORRECT | — |
| B1 label | Overclaimed as PROVED | Relabelled CONDITIONAL on I1 |
| RRS description | Wrong | Fixed |
| ISS/IS description | Not checked by the referee (from repo notes) | Stays as cited from repo notes |

Every material referee point was checked by re-derivation: uniformity of P(ρ), the 3b+1
bound, Shor returning divisors, and the inverse-map character. They were accepted as stated.

## 9. Next hard question

Is QZS(n = poly, K, X = 2^{poly}) solvable in time poly(K)? Equivalently, can one efficiently
find a nonzero integer vector making the diagonal real quadratic form Σθ_iμ_i² integral to
precision 2^{-K}, for random θ_i? The alternative is to show that a non-template measurement,
for example a BCvD-style PGM on two chirp-line states, needs only poly precision.

* **Next command:** attack the two-variable relaxation |θ_1μ_1² + θ_2μ_2² − m| < 2^{-K} with
  Coppersmith-style lattices in fpylll (BKZ), for K = 20..60. There is no linear lattice
  encoding of μ ↦ μ².
* **Artifact:** `qzs_lattice.py` with a table of success rate against K.
* **Acceptance test:** a method that succeeds at precision 2^{-K} with |μ| ≤ 2^{K} in time
  poly(K) for K ≥ 60 on random θ would reopen poly time. Failure is only an UNKNOWN, not
  hardness. In parallel, write out the BCvD two-copy PGM for the infinite chirp-line states
  and test whether it needs only poly precision.

Scripts (all run with `nice -n 19 /opt/anaconda3/bin/python`) are in
`research/audits/reviews/2026-11-12-rees-h3z-infinite-index/`:

| Script | Output |
|---|---|
| `h3z_struct.py 4000 5 1` | `h3z_struct.out` |
| `twist_check.py 7` | `twist_check.out` |
| `e2e_fourier.py` | `e2e_fourier.out` |
| `sieve_demo.py` | `sieve_demo.out` |
