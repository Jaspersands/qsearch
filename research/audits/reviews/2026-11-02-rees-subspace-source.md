# Rees flat subspace source: check and completion (item 5), 2026-11-02

AI session only; human review still required. Scope: `main.tex` §`sec:subspace` (lines
603–631), Theorem `thm:subspace-source`, `research/REES_SUBSPACE_SYMMETRY_SOURCE.md`,
`theorems/rees_subspace_source.py`, and `research/REES_PROJECTIVE_STATE_SOURCE.md` §§3–5 (the
only part main.tex relies on). `REES_NOISY_STATE_SOURCE.md` is not cited by main.tex, so I did
not check it. `REES_MIXED_SPECTRAL_SOURCE.md` is cited as "not re-audited" and stays out of scope.

Script and output: `2026-11-02-rees-subspace-source/exact_checks.py` and `exact_checks.out`
(about 30 s). `tests/test_rees_subspace_source.py`: 48 passed. Neither file was edited.

## Verdict

**No counterexample.** Theorem `thm:subspace-source` (i)–(ii) is correct as stated. The
composition with the Rees core in the notes is also correct: the exterior state, the zero-moment
design, amplification, and then Lemma `lem:copy-lift`-style lifting.

The paper's section is **incomplete**, though. It stops at "T copies of Ω_V". It never states that
H is recovered, and it never says how many copies a lifted source costs. It defers the
determinant-character step to a note "not reproduced here". The budget paragraph's numbers match
the code exactly, but the text omits the hypothetical promises behind them and the per-source
factor M·k. A complete statement and the text fixes are below.

## 1. Part (i): exterior state, stabilizer, gap. Proved, float check

- Ω_V is decomposable, so V = {v : v ∧ Ω_V = 0}, and R(g)^{⊗r}Ω_V = det(R(g)|_V)·Ω_{R(g)V}.
  The ray stabilizer is exactly H = {g : R(g)V = V}, a subgroup, with character χ = det(R|_V).
  Since G has exponent p, χ takes values in the p-th roots of unity.
- TD(Π_V/r, Π_{UV}/r) = (1/r)Σ sin θ_i. By the CS decomposition, P−Q has eigenvalues ±sin θ_i.
  |⟨Ω|U^{⊗r}|Ω⟩| = |det(Q†UQ)| = Π cos θ_i. Cauchy–Schwarz gives γ := (1/r)Σ sin²θ_i ≥ δ².
  AM–GM gives Π cos θ_i ≤ (1−γ)^{r/2} ≤ √(1−δ²) ≤ 1−δ²/2. All steps are valid.
- Float check (Part B): 400 random (d ≤ 7, r ≤ d) cases, including 2r > d and r = d. All three
  identities and both bounds hold. The δ²/2 gap is tight to second order at r = 1.
  It is loose by about a factor r/2 for large r, since overlap ≤ (1−δ²)^{r/2} also holds.

## 2. Part (ii): streaming growth, copy count, clock. Proved, float + exact check

- Success probability. Let σ be any state in ∧^k V and ρ = Π_V/r. Then
  Tr(A_{k+1}(σ⊗ρ)) = Tr(σ·Tr_{k+1}P^V_{k+1})/r = (r−k)/(r(k+1)), which does not depend on σ.
  So the number of attempts is **exactly** a sum of independent Geom(p_k), k = 1..r−1. The
  product of the p_k is r^{−r}, which matches the naive one-shot projection. Both are verified.
- Rejection invariant. A_k⊗I commutes with A_{k+1}, so the Lüders complement
  (I−A_{k+1})(σ⊗ρ)(I−A_{k+1}) stays in range(A_k⊗I) on V^{⊗(k+1)}. Tracing out the fresh register
  leaves a state in ∧^k V.
- Implementation check (Part A, d ∈ {3,4}, r ∈ {2,3}). Take W = F†·(Σ_j |j⟩⟨j| ⊗ ±SWAP_{j,k+1})·F
  and the "0 vs. not 0" outcome. Applying W† on rejection returns the ancilla to |0⟩ exactly
  (leak ≤ 2e−17) and leaves the registers in the exact Lüders complement. This matches the
  paper's p_k, and the top state is |Ω_V⟩⟨Ω_V|.
  **Smallest falsifier of the shortcut that omits recovery:** d = 3, r = 3, k = 2. The kept
  2-register state has weight 0.093 outside ∧²V. At k = 1 the shortcut cannot fail, because
  ∧¹V = V.
- Clock. p_k ≥ (r−k)/r², so the attempt count is stochastically dominated by a coupon
  collector with r coupons of probability 1/r² each. That gives r·e^{−N/r²} ≤ r·2^{−B} per
  output; a union bound over T outputs gives ≤ β. Exact Fraction tails for r = 2..8, B = 1..6
  never exceed r·2^{−B}; the largest ratio is 0.34 (Part D). Raw copies are ≤ T(N+1) and growth
  instruments ≤ TN.
- Citation. I read Bene Watts et al., arXiv:2610.06737v1, first 100k characters of the HTML.
  Algorithms 1–2 are the growth measurement and the streaming loop; failure returns k
  antisymmetric registers. Theorem 5's failure bound r(1−λ_min/r)^n, at λ_min = 1/r, is exactly
  the paper's bound. Remark 6 covers known rank. The attribution is consistent.
  (The source also has a copy-reuse variant with fewer copies. It is not used here.)

## 3. From Ω_V to a source the Rees core accepts. Argued from proved pieces, float check

The core accepts fresh copies of the left-coset density ρ_{H̃} on G̃ = (A,∗), with
H̃ = exp(hlift) (Lemma `lem:homogeneous`, Lemma `lem:copy-lift`). Ω_V is not ρ_H: overlaps
off H are nonzero (at most 1−γ), and the phase χ on H is nontrivial. The notes repair both:

1. **Design.** Take a public multiset S of M nonzero points with Σ_{s∈S} s^j = 0 mod p for
   j = 1..c and at least c distinct points (projective note §3; M ≤ (c+1)!). Use k blocks.
   On the address a ∈ G̃, apply controlled R^{⊗r}(E_s(a)) to a fresh Ω_V for each s and each
   block, then discard the copy. The address density is
   σ[a,b] = (Π_s ⟨Ω|R^{⊗r}(E_s(b^{-1}∗a))|Ω⟩)^k / p^n.
   It depends only on b^{-1}∗a, so the cosets are **left** cosets aH̃. That is the same
   convention as f̂ in Lemma `lem:homogeneous` and the density in Lemma `lem:copy-lift`.
2. **Phase.** On H̃, χ(exp v) = ω^{ℓ(v)}, where ℓ is F_p-linear on h and kills [h,h]. This uses
   Lazard and exponent p. Then Σ_s ℓ(E_s C) = Σ_j (Σ_s s^j) ℓ(C_j) = 0, so the in-coset entries
   are exactly 1/p^n.
3. **Separation.** Outside H̃, Lemma `lem:homogeneous` (c distinct points) puts some E_s(C)
   outside H, so |entry| ≤ (1−γ)^k / p^n with γ = δ²/2. This gives ‖σ−τ‖_F ≤ (1−γ)^k and
   TD(σ, ρ_{H̃}) ≤ √(p^n)·(1−γ)^k/2.
4. **Hybrid.** A hybrid bound over the B_leaf lifted sources of the core gives the receiver.
   Labels, including Schedule 3's uniform-label law, are covered by the complete-instrument
   hybrid. The core's descent consumes only sources and public right actions; it never queries f.

Exact simulation (Part C). The group is Heis(F_p) for p = 3 and 5, with the left-regular R
(d = p³), r = 2, and a random V inside an H-isotypic component, so det|_H = χ² ≠ 1. The hidden
subgroups are ⟨exp X⟩ (nonnormal), ⟨exp X, exp Z⟩ and Z(G). The checks:
- stab(V) and the ray stabilizer of Ω both equal H.
- hlift equals ∩_s E_s^{-1}(h).
- In-coset phases equal 1 to 1e−14 with the zero-moment designs (1,1,1,2,2,2) at p = 3 and
  (1,2,3,4) at p = 5.
- The exact TD(σ,τ) obeys the bound for k = 1 and 3.
- τ equals the mixture of left cosets |aH̃⟩.

**Falsifier for skipping the design** (feeding Ω_V to the c-point lift of Lemma
`lem:copy-lift`). The smallest instance is Heis(F_3), H = Z(G), r = 2, points (1,2), k = 1.
The in-coset phase is χ^{1+4} ≠ 1, with |F−1| = 1.732, so the density is wrong. At p = 5 the
same happens with H = ⟨exp X⟩, nonnormal (|F−1| = 1.902). Points (1,2) happen to work at p = 3
for H = ⟨exp X⟩, because 1+2 ≡ 0 and h ∩ γ₂ = 0. Any design also works when k ≡ 0 mod p, but
that costs a factor p.

## 4. Total charged cost and budget match. Exact computation

The ideal source budget is `projective_source_budget` at gap δ²/2 and error ε/2. It gives
T = M·k·B_leaf exterior states, where B_leaf is the core's lifted-source count at ε/4 and
k = ⌈b/γ⌉ with b = bitlen(p^n) + ⌈log₂(8B_leaf/ε)⌉. The code's per-leaf deviation
(p^n−1)/2^b dominates √(p^n)(1−γ)^k/2, so it is conservative.

Error split: receiver ε/4, source replacement ε/8, copy and action ε/8, timeout β = ε/8, and
growth/acquisition instruments ε/8 (in diamond norm, per call ε/(8C) with C = T(N+1)+TN).
The total is ≤ 3ε/4 ≤ ε. The quantities charged:

- raw copies ≤ T(N+1), with N = r²⌈log₂(8rT/ε)⌉;
- growth instruments ≤ TN, each with ≤ 2(r−1) controlled q-qubit register swaps, plus a
  (k+1)-level uniform-ancilla preparation in W and again in the recovery W†;
- controlled base-R calls ≤ rT, each at error ≤ ε/(8rT), on reversibly computed E_s(a) with
  cleaned workspace;
- live preparer memory: r input registers plus ⌈log₂ r⌉ ancilla qubits, on top of the core's
  registers;
- plus all of the core's own classical and quantum work.

Paper versus code versus my independent re-derivation from T (Part E): all agree.
The profile is p = 43, c = 9, n = 97, hypothetical δ = 1/10, ε = 1/3. T has 1592 bits.

| r | B | N | raw copies ≤ 2^x |
|---|---|---|---|
| 1 | 0 | 0 | 1592 |
| 2 | 1598 | 6392 | 1605 |
| 8 | 1600 | 102400 | 1609 |
| 32 | 1602 | 1640448 | 1613 |

The design moments at p = 43 are exactly zero for j = 1..9, with 14 distinct points. **Per
lifted source the route spends M·k = 14 × 420400 = 5,885,600 exterior states**, against c = 9
copies for the coset-copy lift. The paper does not say this.

Mechanical note: `rees_subspace_source.json` has stale source hashes for
`tests/test_cli_parser_integrity.py` and `qsearch_cli/registry.py`. A regenerated report gives
identical numbers.

## Exact statement that now holds (proposed corollary; argued from proved lemmas)

**Setting.** L is an explicit m-dimensional Lie algebra over F_p of class c < p, and
G = exp(L) has exponent p. A is the positive Rees cover, of dimension n ≤ cm.

**Access.** The algorithm receives:
- fresh IID copies of ρ = Π_V/r, with r supplied;
- an efficiently controlled linear unitary representation R of G on q qubits;
- a promised δ with TD(ρ, R(g)ρR(g)†) ≥ δ for all g ∉ H = {g : R(g)V = V};
- a public certified zero-moment design S (M points, at least c distinct). Generating it has
  its own abort, charged separately.

**Conclusion.** With the parameters above, the Rees core (Schedule 1) returns generators of
log H with error ≤ ε. It uses ≤ T(N+1) raw copies, ≤ TN growth instruments, ≤ rT controlled-R
calls and polynomial public arithmetic, where T = M·k·B_leaf and k = O((n log p + log(B_leaf/ε))/δ²).

**Scope.** For fixed c this is polynomial in m, log p, r, q, 1/δ and log(1/ε). It is not
polynomial when r is exponential in q. It does not cover nonflat ρ, unknown r, non-IID copies,
projective R, exponent p^e, or black-box G.

## Still missing

- No explicit efficiently controlled family with polynomial r, a proved global δ, nontrivial
  nonnormal H and a matched classical access analysis.
- No quantum backend for the growth instrument or the receiver.
- The extensions (black-box, exponent p^e, Cor fpt-r) are not composed with this source.

## Claim gates that must stay false

`speedup_claim_allowed`, `novel_antisymmetrization_primitive`, `novelty_established`,
`nonflat_conjugation_symmetry_covered`, `preparer_quantum_backend_implemented`,
`quantum_receiver_implemented`, `natural_hard_state_family_established`, and every Rees
candidate or proof promotion.

## Text fixes for main.tex (listed, not applied)

1. L608: state the setting: "G = exp(L) explicit over F_p, class c < p (so exponent p), as in
   Theorem `thm:main`". The character cancellation uses χ = ω^ℓ with ℓ F_p-linear on log H.
   Black-box and exponent-p^e groups are not covered.
2. Proof of (ii): add one sentence. p_k does not depend on the retained state, so the attempt
   count is exactly a sum of independent Geom(p_k), dominated by the coupon collector.
   Rejection must apply the inverse LCU (W†) before the fresh register is discarded. This gives
   the Lüders complement, which preserves ∧^k V because A_k⊗I commutes with A_{k+1}. Without
   recovery the invariant fails at d = r = 3, k = 2.
3. Replace "which is not reproduced here" (L627) with the four-step composition of §3 above
   (design, phase cancellation, separation and TD bound, hybrid), and add the corollary
   statement above as `cor:subspace-hsp`. Also say that the plain c-point lift is wrong for ray
   stabilizers (Heis(F_3), H = Z(G), r = 2).
4. L629: name the hypothetical promises (δ = 1/10, ε = 1/3) and T ≈ 2^1592 exterior states.
   State M = 14 and k = 420400 per lifted source, against c = 9 for coset copies. Call all
   counts sufficient bounds. Drop or explain `\SubQubits` (None: no input width, so no gate count).
5. Table at L184/L194: add a "flat subspace copies" row, or a caption sentence: M·k exterior
   states per lifted source, each costing ≤ N+1 raw copies.
6. Optional: overlap ≤ (1−δ²)^{r/2} gives gap 1−(1−δ²)^{r/2} ≥ min{rδ²/4, 1/2}. This cuts k by
   about r/2 when rδ² is small. Code and numbers would change.
