# Rees full campaign, item 7: gate compilation and classical filters

2026-11-02. AI session only, not human review. Scope: `docs/papers/rees-hsp/main.tex`
§`sec:uniform-compilation` (Theorem `thm:uniform-compilation`, lines 456–533) and
§`sec:classical-landscape` (Proposition `prop:conjugation`, Remark `rem:filters`, lines 632–665).
Scripts and their saved outputs are in `2026-11-02-rees-compilation-filters/`:
`bch_compilation_check.py`, `qft_error_check.py`, `classical_filters_check.py` (each writes a
`.out` next to itself; total run time under one minute). Labels: **proved** (written proof
here), **exact** (exact computation mod p or over Q), **float** (floating-point check),
**cited** (primary text read, theorem number given), **argued** (sketch, not a full proof).

## Verdict

- **Theorem uniform-compilation: holds**, with no counterexample and no gap that affects the
  main theorem. Four text defects: (i) states the per-evaluation bracket count with c, but the
  tables charge B(d) at stage d, which is correct; (iii) cites a construction that Cleve–Watrous
  only sketch for arbitrary moduli, and Kitaev 1995 §5 is the citable proof; (iii) leaves q_max
  undefined, and the core check's formula for it undercounts; Bennett, Cleve–Watrous and Kitaev
  are not in `references.bib`.
- **Proposition conjugation: correct as stated** (proved, exact checks). The 10-31 range is
  sharp: the identity fails for **exactly** N ≤ p ≤ 2N−2, with an explicit witness for every such
  pair. But the proposition is a special case of a theorem the paper already cites: Luks 1992,
  Theorem 3.2(5), gives conjugation stabilizers classically for every matrix p-group, every N
  and every p.
- **Remark filters: the direction is honest, but the remark is incomplete and item (ii)
  misstates two hypotheses.** The most general filter, any explicit linear action (Luks
  Thm 3.2(5),(7)), is not named, though items (i) and (iii) rely on it. Item (ii) needs "anchor
  fixed by the group" (counterexample below) and "index ≤ p" (the note proves the
  linear-algebra claim only for UT_5 blocks with p > 5). Its "needs p > max(D,(D−1)Δ)" is a
  sufficient condition, not a necessary one. "Must first be tested" and "at least these filters"
  are honest: the paper claims no completeness and no hardness.

## Part (a): Theorem uniform-compilation

### (i) ODE evaluation of truncated BCH, bracket count

*Claim.* For a Lie algebra of class ≤ c < p, `bch_via_ode` returns log(exp x · exp y) using
exactly B(c) = (c−1)c(c+1)(c+2)/6 bracket calls.

*Proof (proved).* Put Z(t) = BCH(x, ty). Every term with k copies of y has Lie degree ≥ k,
so Z is a polynomial in t of degree ≤ c, and Z(1) = Σ_{k≤c} z_k. From e^{Z(t)} = e^x e^{ty},
the left-trivialized derivative gives Z' = [ad_Z/(1−e^{−ad_Z})] y = Σ_{j<c} b_j ad_Z^j y.
Terms with j ≥ c vanish because ad_Z^c y has degree ≥ c+1. The coefficients are
b_j = (−1)^j B_j/j! (with b_1 = 1/2). By von Staudt–Clausen, the denominator of B_j has only
primes q with (q−1) | j, so q ≤ j+1 ≤ c. The recurrence (k+1) z_{k+1} = [t^k] Σ_j b_j ad_Z^j y
divides only by k+1 ≤ c. So the recurrence has coefficients in Z_(p), its unique solution is
the reduction of the rational one, and the result is the Lazard group law mod p.

*Count (exact; script and code agree).* The loop runs over degree d = 0..c−1, power 1..c−1 and
order 0..d, with order+1 calls each, so it makes (c−1) Σ_{d<c} (d+1)(d+2)/2 = (c−1)·C(c+2,3) = B(c)
calls. There is no early exit. Measured calls equal B(c) for every c = 1..12 (0, 4, 20, 60, …, 4004).
Correctness against matrix log(exp X exp Y) in n_{c+1}(F_p) passes for ten (c, p) pairs,
including the boundary p = c+1 (c = 1, 2, 4, 6). Control: a class-3 algebra evaluated with c = 2
is wrong on 30/40 pairs. So "exactly" is right for this unoptimized schedule (many calls
bracket with zero vectors). It is not a minimum.

*Defect (exact).* Stage d acts on the class-d quotient G_d of dimension D_d, so the artifact
charges B(d) brackets per pass at O(D_d³) each. For (6,3,1), p = 65537, the table's 28160 brackets
equal 1280·B(3) + 640·B(2) = 25600 + 2560. Reading (i) literally, with B(c) per pass over all 1920
passes, gives 38400. The class-12 profile shows the same mismatch. The table is right and the
theorem's wording is wrong.

### (ii) Clean map |u⟩|v⟩ ↦ |u⟩|u∗v⟩ with four evaluations

*Proved.* Start from registers (u, v, 0). The first XOR evaluator computes u∗v with its history
(pass 1), XORs the result into register 3, and uncomputes the history (pass 2). The second
evaluator computes u^{-1}∗(u∗v) = v from registers 1 and 3 (u^{-1} = −u in Lazard coordinates,
a free negation; pass 3), subtracts it from register 2 and uncomputes (pass 4). Relabelling then
gives |u⟩|u∗v⟩|0⟩. Every step is a permutation of canonical triples, and the scratch returns
to 0.

*Exact check.* The map was simulated as a permutation: all 729 pairs in n_3(F_3), all 15625 in
n_3(F_5), and 3000 sampled pairs in n_4(F_5). The scratch always clears, there are always 4
passes, and the map is a bijection on canonical pairs.

*Wording.* The primitive the merges actually use is the right translation of the compilation
note, x ↦ BCH(x, −Δ_s(section(u))): identity on invalid words and on s = 0 slots, with the
scratch swap (x,0)→(x,P_u x)→(P_u x,x)→(P_u x,0). It also costs 4 passes. The section and the
dilation are public linear maps, not BCH passes. The theorem should name that primitive, not
only left multiplication.

### (iii) QFT_{F_p} to isometry error η, hybrid, ε split

*Literature (cited, full texts read).*
- Cleve–Watrous, arXiv:quant-ph/0006004. Their definition after Theorem 1 is the right notion:
  every pure input, ancillas included, ends within Euclidean distance ε, which is clean-workspace
  operator norm. But arbitrary moduli appear only in §7.1, as a sketch with no numbered theorem,
  which ends: "the technical details regarding this method will appear in the final version". It
  is not a citable proof.
- Kitaev, arXiv:quant-ph/9511026, §5. Theorem 2 together with eqs. (22)–(25) builds V_q for
  every modulus q as a partial operator with clean auxiliary register (Definition 4, ω = |0⟩↦|0⟩),
  with precision 2(|Ω|ε')^{1/2}, where Ω has q elements and ε' is the eigenvalue-measurement error.
  To reach η, take ε' = η²/(4p). That costs O(log p + log(1/η)) repetitions, still
  poly(log p + log 1/η). Kitaev's basis Q contains every one-qubit gate (line "the basis
  Q = U(B_1) ∪ {τ, ∧τ}"), so finite-gate synthesis, as in Dawson–Nielsen, adds polylog overhead
  and the note already charges it inside η. Lemma 3 of the same paper (precisions add, also for
  partial operators) is the restricted-domain hybrid.

*Hybrid (proved; float check).* The note's telescoping sum compares each actual stage on an
ideal prefix, so only canonical inputs are needed, and leakage into padding is harmless because
the actual suffix is contractive. An operator-norm error η gives half-trace distance ≤ η. In 200
random trials (QFT_5 in 3 qubits, ideal extended arbitrarily on padding, actual leaking up to
0.18 into padding), ‖(actual − ideal)J‖ ≤ Nη held with a maximum ratio of 1.0000.

*Composition with the core's ε split (exact on the artifacts).* Core check §6.3: rank ≤ ε/3,
solver 0 under Schedule 1, each instrument within ε/(3N_instr). For both artifacts,
η = ε/(3 N_instr q_max) exactly, q_max equals the largest per-instrument count the note charges,
max(D_c, n, max_d(2M_d r_d + D_{d−1})), N_QFT ≤ N_instr q_max and N_QFT·η ≤ ε/3. The
random-column artifact makes the same allocation, with N_instr counted over all attempted trees
(`all_failed_trees_charged`). The (6,3,1) case gives η = 1/459000 and 19 bits, as tabulated;
class 12 gives 83 bits. A sweep of 44 further profiles passed. So the composition holds,
provided the oracle is exact and the reversible arithmetic is exact (NOT/CNOT/Toffoli). An
approximate oracle would need its own charge, as the note says.

*Defect in a cited document (exact).* Core check §6.2 sets q_max = max(m, max_d M_d g_d). That
undercounts the note's per-instrument transforms in all 46 profiles tested: the merge also needs
the inverse transforms and D_{d−1} quotient transforms, and a leaf needs n > m. If that formula
were used in η, the aggregate QFT error would exceed ε/3 for some profiles. The smallest is
g = (3,1) at p = 2^61−1: N_QFT = 210, N_instr = 42, q_core = 4 against an actual 11, so the QFT
share is 1.25·ε/3. Under Schedule 1 the total stays below ε, because the solver third is unused,
but the formula is wrong. main.tex leaves q_max abstract, so the paper is not wrong here; it
should define q_max.

### (iv) Depth-first registers

*Argued and exact.* At any time, the waiting completed siblings along the current root-to-leaf
path number at most Σ_d (M_d − 1). The deepest merge adds its last child and its fresh
address register, giving 2 + Σ(M_d − 1). This reproduces the artifact: 18 for arities [2,16] and
1254 for class 12. At c = 1 the artifact records 1 and the formula gives 2, a loose but valid
bound.

## Part (b): classical filters

### Proposition conjugation

*Proof check (proved).* With N ≤ p, exp(x) − I ∈ F_p[x] and x ∈ F_p[exp x] (log∘exp = t in
Z_(p)[t]/(t^p)). So x and exp x have the same commutant, and the stabilizer is exp(L ∩ ⋂ ker ad_{A_i}).
exp(L) is a group: the truncated identity exp(x)exp(y) = exp(H(x,y)) holds in
Z_(p)⟨x,y⟩/(degree ≥ N), and n_N(F_p)^N = 0. The transporter equation is (I+X)A = B(I+X).

*Exact checks.* Exhaustively over UT_2(F_2) and over UT_3(F_3) with all 3^9 matrices A
(532521 pairs), and on samples at (3,5), (4,5) and (5,5), each with 6 Lie subalgebras L
including random proper ones: brute-force stabilizers equal the formula in every case, and
exp(L) is closed under products. The transporter for L = n_N agrees with the linear system at
(2,2), (3,3) and (3,5).

*The 10-31 range is sharp (exact).* In characteristic p, ad_x^p = ad_{x^p} = 0, so the truncation
Σ_{k<p} ad_x^k/k! is defined. It is missing the terms x^i M (−x)^j/(i! j!) with i+j ≥ p and
i, j < N. Witness: x = J_N (the shift), M = E_{N1}. Those terms land at distinct positions
E_{N−i,1+j}, so the identity fails if and only if some i, j ≤ N−1 have i+j ≥ p, that is, iff
p ≤ 2N−2. Checked for N = 2..7 and every prime in [N, 2N+3]: it fails exactly on [N, 2N−2]
and holds, with 20 random (x, A) each, for p ≥ 2N−1. The smallest case is N = p = 2: x = E12,
M = E21, and the missing term −xMx = E12 is nonzero mod 2. The phrasing "fails for N ≤ p < 2N−1"
is accurate. Better: "the truncated exp(ad_x) is defined but differs from conjugation".

*The proposition is not the strongest classical statement (cited).* Luks, "Computing in
solvable matrix groups" (FOCS 1992), full text at ix.cs.uoregon.edu/~luks/solmatgrp.pdf,
Theorem 3.2: for a solvable G ≤ GL(n,F) given by generators, problems (1)–(10) take time
polynomial in n + log|F| + ν, where ν is the largest prime dividing |G| other than char F. For a
p-group in characteristic p, ν is vacuous. Item (5), a vector stabilizer, applied to the
conjugation action on M_N(F_p)^k (dimension kN²; a unipotent group meets the scalars trivially)
gives the tuple stabilizer for **every** matrix p-group, every N and every p, including
subgroups that are not of the form exp(L) and N > p. Even without Luks, for G = UT_N the
stabilizer is I + (n_N ∩ commutant), which is linear for every N and p: exhaustive checks at
(N,p) = (3,2) and (4,3) passed. A transporter inside a proper subgroup exp(L) is not in Luks's
list; it is irrelevant to the HSP and left UNKNOWN here.

### Remark filters

- **Missing general filter (argued from Luks Thm 3.2(5),(7)).** If f(g) = ρ(g)·v, or the
  stabilizer of a subspace, for an explicit representation ρ of polynomial dimension over F_p
  (dense coefficient vectors, explicit tensors, explicit matrix tuples, explicit subspaces),
  the hidden subgroup is classically computable in polynomial time. All three instantiation
  types the paper names escape this only when the representation space is superpolynomially
  large; items (i)–(iii) are the tools for that case. The orbit-module note already reduces to
  exactly this theorem. Name it as filter 0.
- **Item (ii), anchor (exact counterexample).** K ⊇ H needs an anchor fixed by every element
  of the group, which the note states ("Non-fixed anchors would not justify this containment").
  The paper's "a fixed anchor" can be read as "a chosen anchor". At p = 3, f = u³v − uv³ is
  GL_2(F_3)-invariant, so H = UT_2(F_3) of order 3. At the moved anchor (0,1), its 2-jet is
  2·w_u, whose stabilizer is K = 1, so K would falsely "certify" H = 1.
- **Item (ii), index hypothesis (proved; exact).** The note proves K = exp(L_K), with L_K given
  by linear equations, for UT_5 blocks with p > 5. The argument (g^T B = B g^{-1}, then the
  logarithm truncates) extends to every Lie algebra of nilpotency index N ≤ p, singular B
  included. Checked: N = 3, p = 3, all 729 forms (261 singular) and all 27 X, no mismatch;
  N = 4 and 5 at p = 5 sampled, no mismatch. This includes p < 2N−1, where the naive exp(ad)
  route of Part A fails. For index > p, "computable by linear algebra" is unproved; the
  stabilizer is still classically computable by Luks. "Linear unipotent action" in the
  remark must carry "of nilpotency index ≤ p".
- **Item (ii), linearization sentence (exact).** SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT §3
  proves p > max(D,(D−1)Δ) to be **sufficient** and says "sufficient, not necessary". "Needs"
  should read "is proved under". The Δ < p counterexample checks out: on UT_4(F_5),
  F = x0x1x3 + 2x0x2² − x1²x2, N = E01+E12+E23 gives ∇F·(Nx) = 0 formally, while
  F(exp(N)x) − F(x) = x3³. Over Q the difference is t⁵x3³/6 plus terms divisible by 5.
- **Items (i) and (iii)** agree with their notes' stated access models and with the Luks import
  as far as read here: an extension-field circuit and rank cap; a promised p-group and common
  index ≤ p. They were not reproved; the remark says so.
- **Honesty of "must first be tested".** Honest. The paper claims neither completeness nor
  hardness, says "at least these filters", and says a failed filter is not hardness evidence.
  Known gap: the Moore-form family defeats the orbit-rank cap but falls to a gradient recognizer
  (POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md, follow-up). The remark covers this only through
  "gradient recognizers". The list also omits the derivative/gradient attack of
  SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT §3 as a filter in its own right: it appears only as a
  caveat.

## Exact statement that now holds

For a Lie algebra L over F_p with public structure constants, class c < p, an exact ordinary
coherent hiding oracle (cost T_f, charged separately), and the bounded flagged Rees procedure of
Schedule 1 (or 2, or 3 with all attempted trees charged): every primitive has a uniform
finite-gate circuit.
- Stage-d BCH passes use exactly B(d) brackets of O(D_d³) field operations each.
- Each controlled translation takes 4 passes.
- Each QFT_{F_p} has clean-workspace operator-norm error η = ε/(3 N_instr q_max) at size
  poly(log p + log 1/η) (Kitaev 1995 §5, plus finite-gate synthesis), with
  q_max = max(n, m, max_d(2M_d r_d + D_{d−1})).
- The total QFT contribution is ≤ ε/3 in half-diamond norm, so the core's split
  (rank ε/3, solver 0 or ε/3, approximation ε/3) gives failure ≤ ε.
- Depth-first storage is ≤ 2 + Σ(M_d − 1) cover registers.

Classically, for every matrix p-group G ≤ GL_N(F_p) acting by simultaneous conjugation on k
explicit matrices, the stabilizer is computable in time poly(N, k, log p) (Luks Thm 3.2(5)). For
G = exp(L) with N ≤ p it is exp(L ∩ ⋂ ker ad_{A_i}).

## Still missing

- No emitted circuit or failure-aware formal instrument exists (unchanged).
- The merge's charged QFT count 2M_d r_d + D_{d−1} is the note's schedule; I did not derive a
  minimal instrument.
- Luks's theorem was read in its 1992 extended-abstract form. Its proofs there are sketches, so
  the import rests on that paper as published.
- A transporter inside exp(L) for L ≠ n_N is UNKNOWN; it is irrelevant to the HSP.

## Claim gates that must stay false

`speedup_claim_allowed`, `novelty_established`, `native_application_established`,
`circuit_generator_implemented`, `quantum_receiver_implemented`, `whole_rees_correctness_certified`,
`formal_total_policy_instantiated`, `approximate_oracle_error_included`, and every Rees
candidate/proof promotion. Human review is still required.

## Text fixes for main.tex (listed, not applied)

1. Line 468, (i): "evaluated on a class-d quotient G_d, as at stage d, with exactly
   (d−1)d(d+1)(d+2)/6 bracket evaluations, each O(D_d³) field operations, where
   D_d = Σ_{k≤d} g_k; at d = c this is (c−1)c(c+1)(c+2)/6 on 𝒜". Add "in this unoptimized
   schedule".
2. Line 476, proof of (i): justify the division claim by the recurrence coefficients, not the
   BCH terms. The coefficients of z/(1−e^{−z}) below degree c have denominators with primes ≤ c
   (von Staudt–Clausen), and the recurrence divides by k+1 ≤ c.
3. Line 469, (ii): add that the merge primitive is the controlled right translation
   x ↦ x ∗ (−Δ_s(section(u))), identity on invalid words and on s = 0 slots, with the same four
   passes. The section and Δ_s are public linear maps.
4. Line 470, (iii): replace "following Cleve and Watrous" with "by Kitaev's construction
   [Kitaev 1995, §5, Theorem 2 and eq. (25)], with finite-gate synthesis, or in logarithmic depth
   by the sketch of [Cleve–Watrous 2000, §7.1]". Note that Kitaev's precision 2(pε')^{1/2} is
   met with ε' = η²/(4p). Define q_max = max(n, m, max_d(2M_d g_d + D_{d−1})).
5. references.bib: add Bennett 1973 (Logical reversibility of computation, IBM J. Res. Dev.
   17:525–532), Kitaev quant-ph/9511026, Cleve–Watrous quant-ph/0006004 (FOCS 2000), and
   Dawson–Nielsen quant-ph/0505030. Cite them at lines 469–470. None is cited now.
6. Line 636: "fails" → "the truncated series exp(ad_x) is defined, since ad_x^p = 0, but differs
   from conjugation exactly when N ≤ p ≤ 2N−2 (witness x = J_N, M = E_{N1})".
7. After Proposition conjugation: "By Luks [Luks1992, Thm 3.2(5)], the stabilizer is computable
   classically for every matrix p-group acting by conjugation, for every N and p. The
   proposition gives a self-contained linear-algebra form when G = exp(L) and N ≤ p."
8. Remark rem:filters: add item (0), explicit linear actions (Luks Thm 3.2(5),(7)), as the first
   filter, with the note that items (i)–(iii) treat succinct, superpolynomial representations.
9. Item (ii): "linear unipotent action" → "action of exp(L), L of nilpotency index at most p (the
   note uses UT_5 blocks, p > 5)". "a fixed anchor" → "an anchor fixed by every group element (a
   moved anchor can give K = 1 while H ≠ 1)". "needs p > max(D,(D−1)Δ)" → "is proved under
   p > max(D,(D−1)Δ)"; keep "Δ < p is not enough", which is verified.
10. Line 663: name the derivative/gradient attack (SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT §3) and
    the Moore gradient recognizer explicitly among the "direct structural attacks".

For the parent (not main.tex): core check §6.2's q_max = max(m, max_d M_d g_d) should become
the note's max(D_c, n, max_d(2M_d r_d + D_{d−1})). The smallest failing aggregate is g = (3,1),
QFT share 1.25·ε/3.
