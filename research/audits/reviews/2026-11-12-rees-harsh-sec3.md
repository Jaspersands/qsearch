# 2026-11-12 Harsh referee: core Section 3 (Rees cover, tuple oracle, coset-copy input, Dixmier–Lister)

**AI-run hostile referee report, pending human review.** Target:
`docs/papers/rees-hsp/core/main-core.tex` §3 (ll. 268–405: `thm:rees-cover`, `lem:homogeneous`,
`lem:lifted-source`, `prop:single-evaluation` and its example, `rem:fewer-points` and the text after
it, `lem:copy-lift`, the Terminology paragraph, §3.4 and `prop:dl-central-scalars` with the
paragraph after it), plus what it uses from §1.3 (the "Why interpolation works" paragraph, l. 143),
§1.4 (`def:input-contract`, the Lazard sentence l. 162) and §2 (BCH, Lazard dictionary, coset
states, `lem:fourier`). I edited no paper, STATE, handoff or reductions file. No git, no network,
no API calls. Scripts and outputs: `2026-11-12-rees-harsh-sec3/` (Python scripts run with
`nice -n 19 /opt/anaconda3/bin/python`, the Sage script with `$E/sage`). Finite checks only falsify.

**Order of work.** I re-derived every statement of §3 by hand and wrote and ran all scripts except
the last two (`dl_aut_p5.py`, `check_lazard_subgroups.py`, written for gaps I noticed myself) before
opening any earlier referee report. Afterwards I read, by grep plus the relevant sections,
`2026-11-04-rees-referee-9-core.md`, `-3-body.md`, `2026-11-05-rees-referee-17-core.md`, `-18-core.md`,
`2026-11-03-rees-referee-2.md`, `2026-11-03-rees-check-core.md`, `2026-11-02-rees-referee.md`,
`2026-11-01-rees-core-proof-check.md`, `2026-11-09-rees-dl-scalars-schedule2-referee.md` and the row
of `2026-11-12-rees-full-version-sync.md` on `rem:fewer-points`. §5 says what is new.

## 0. Overall verdict

**CORRECT WITH FIXES (all minor; no GAP, nothing WRONG).** Every numbered statement of §3 is
proved as stated, for every subgroup H, every prime p > c and every admissible point set. I found
no counterexample in exhaustive checks (every Lie subalgebra of the Heisenberg algebra over F_3, F_5, F_7, the free
2-generator class-3 algebra and the 5-dimensional filiform algebra over F_5, every point set and
dilation) or in sampled group-level and state-level checks. The tuple oracle is
computable from f and public data alone, costs exactly c queries, and hides exactly
exp(h̃), h̃ = ⊕ t^k(h ∩ γ_k), whether or not H is normal or graded. The fixes are about precision:

1. `lem:homogeneous` proves that h̃ is a Lie subalgebra, but the statement and `lem:lifted-source` /
   `lem:copy-lift` use exp(h̃) as a **subgroup** (its coset state). That follows, but the paper
   never says so; one sentence fixes it (F1).
2. `rem:fewer-points` is correct, but "k points suffice" is undefined. It means "give a
   dilation-invariant pulled-back subgroup"; it is not a query lower bound. The word "every" is
   essential: for k ≥ 2 a single dilation θ ≠ 1 can preserve P_k although γ_{k+1} ⊄ h (for example
   the point set {1,−1} and θ = −1, for every H; over all point sets, 3724 triples (h, S, θ) with
   γ_{k+1} ⊄ h for the free class-3 algebra over F_5, exhaustive).
   The k = 1 statement (`prop:single-evaluation`) is the only one that holds for a single θ (F2).
3. Notation: the symbol q is used for both the polynomial T∏(T−s_i) and an element of γ_3 in the
   sentence after `rem:fewer-points` (F3). "Exactly c fresh copies" in `lem:copy-lift` reads as a
   lower bound that is not proved (F4).

The §3.4 facts and `prop:dl-central-scalars` check out (Jacobi, γ dims (8,4,2), centre = γ_3,
224 × 64 system of rank 52 over Q and modulo every prime 5 ≤ p ≤ 29, the printed 12-parameter
family is exactly the derivation space, least row-certificate multipliers {1,3,6}, u-basis table
over Q(i), sign automorphism). An independent exhaustive count over F_5 gives |Aut| = 4·5^12 and a central image {±I, ±(e_7 ↔ e_8)} of order 4 with scalars ±1, as the paper says. A Gröbner check of the proposition (ζ as a variable, or ζ fixed) did not finish and is NOT computed; the hand proof, which I re-derived, carries it.

## 1. Table of verdicts

| Statement | Verdict | Fix or counterexample |
|---|---|---|
| §3.1 preamble: Gaussian elimination gives bases of γ_k and structure constants of A in poly(m, log p) | CORRECT | — (γ_{k+1} is spanned by [e_i, y_j] over a basis y_j of γ_k; the text says "y ∈ γ_k", read as "y in a basis of γ_k") |
| `thm:rees-cover`(i) A positively graded nilpotent, class(A) = class(L), dim n ≤ cm, A_c central | CORRECT | — |
| `thm:rees-cover`(ii) E_s Lie hom for every s ∈ F_p, onto for s ≠ 0; δ_θ automorphism; E_s∘δ_θ = E_{θs} | CORRECT | — |
| `thm:rees-cover`(iii) BCH groups for c < p; every E_s (s = 0 included) and δ_θ a group hom | CORRECT | — (class "at most c": one line, raised before as I8 of referee 9, applied) |
| `lem:homogeneous` (iff, both expressions of h̃, subalgebra, δ-invariance for every θ ≠ 0) | CORRECT WITH FIXES | F1: say that exp(h̃) = ∩_i E_{s_i}^{-1}(H) is a subgroup of G̃ |
| `lem:lifted-source` (exact ρ_{exp h̃}, c queries, no information on H) | CORRECT | exactness is for an exact uniform superposition; the approximation is §6's job (it prepares it by QFT) |
| Remark after it (uncomputation essential) | CORRECT | control C3: an uncleaned E_1(a) workspace changes the state |
| `prop:single-evaluation` (single θ ≠ 1, single s) | CORRECT | — |
| Heisenberg F_3 example after it | CORRECT | — |
| `rem:fewer-points` (every dilation preserves P_k ⇔ γ_{k+1} ⊆ h, then P_k = h̃) | CORRECT WITH FIXES | F2: define "suffice"; say "every" is needed for k ≥ 2 |
| Text after `rem:fewer-points` (u = 2tq − 3t²q + t³q; finite checks) | CORRECT WITH FIXES | F3: rename the element of γ_3 |
| §1.3 example (H = exp(F_p(x+z+u)) passes s = 1,2, fails s = 3) | CORRECT | — |
| `lem:copy-lift` | CORRECT WITH FIXES | F4: "Using c fresh copies" instead of "Exactly c" |
| Terminology paragraph | CORRECT | — |
| §3.4 derivation facts, no positive grading for p > 3, dims, cover 14, class 3 | CORRECT | — (mod 2 and mod 3 the derivation space is larger, 14 and 16: consistent with "p > 3") |
| `prop:dl-central-scalars` | CORRECT | — |
| Paragraph after it (GAP orders 4·5^12, 12·7^12; central images of order 4, 12) | CORRECT at p = 5 (independent count); p = 7 not recomputed | — |
| §2 dependencies (BCH, Lazard dictionary, ρ_H entries, `lem:fourier`) | CORRECT | — |

## 2. Re-derivations (independent of earlier reports)

### 2.1 The cover (`thm:rees-cover`)

*Well defined.* A ⊂ L ⊗ tF_p[t] is the span of t^kγ_k, k = 1..c. For x ∈ γ_i, y ∈ γ_j,
[x,y] ∈ γ_{i+j}, which is 0 when i + j > c; so the bracket of L[t] maps A × A into A and
nothing nonzero is dropped by the truncation at c (asserted in `lie.py`, `Cover.br`).
Antisymmetry and Jacobi are inherited.

*(i).* A left-normed k-fold bracket of homogeneous elements t^{i_1}x_1, … has degree Σi_l ≥ k and
value in γ_{Σi_l}; for k = c'+1 (c' the class of L) the value lies in γ_{≥c'+1} = 0. Some
left-normed c'-fold bracket of elements of L is nonzero, and the same bracket of the t-lifts is
t^{c'} times it. So class(A) = c'. [t^iy, t^cz] ∈ t^{i+c}γ_{i+c} = 0. n = Σg_k ≤ cm.

*(ii).* ev_s : x ⊗ f ↦ f(s)x is a Lie hom of L[t] (bilinear, [x,y]f(s)g(s)); E_s is its
restriction, for every s, including s = 0, where E_0 = 0. E_s(tx) = sx gives surjectivity for
s ≠ 0. δ_θ multiplies grade k by θ^k, so it respects [A_i,A_j] ⊆ A_{i+j}; inverse δ_{θ^{-1}};
E_s(δ_θ a) = Σ(θs)^ka_k.

*(iii).* Each Dynkin term of total degree N has denominator n·N·∏r_i!s_i! with n ≤ N, all factors
≤ N, so BCH_c has coefficients in Z[1/c!]. The group identities hold in the free class-c Lie
algebra over Q (Mal'cev), both sides are Z[1/c!]-Lie polynomials, the free class-c Lie ring over
Z[1/c!] is free on a Hall basis and embeds in its Q-form, and c! is a unit mod p. Lie homs commute
with Lie polynomials. All correct. Inverse is −x because every bracket of x and −x vanishes.

### 2.2 Homogenization (`lem:homogeneous`)

With C = a^{-1}∗b = Σt^kC_k: f̂(a) = f̂(b) ⇔ ∀i E_{s_i}(a)^{-1}∗E_{s_i}(b) ∈ H ⇔ ∀i E_{s_i}(C) ∈ h
(E_{s_i} is a hom; H = exp h). The c × c matrix V = (s_i^k) has det ∏s_i∏_{i<j}(s_j − s_i) ≠ 0
iff the s_i are distinct and nonzero, which needs p − 1 ≥ c, i.e. p > c. Then C_k = Σ_i(V^{-1})_{ki}
E_{s_i}(C) ∈ h because h is a subspace; conversely C_k ∈ h ∀k gives every E_s(C) ∈ h. Hence the
iff, and the intersection over all of F_p^× gives the same set. Collisions s_i^k = s_j^k (e.g.
s_j = −s_i, k even) are irrelevant: only det V matters; checked with {1, p−1, …}.

*Subgroup (F1).* The lemma's proof shows h̃ is a subalgebra; it does not say exp(h̃) is a
subgroup, which `lem:lifted-source` needs (ρ_{exp h̃} is defined for subgroups). Two one-line
proofs: exp(h̃) = ∩_i E_{s_i}^{-1}(H) is an intersection of preimages of a subgroup under group
homs; or a Lie subalgebra is closed under the Z[1/c!]-Lie polynomial BCH_c and under negation.
Checked (L3): closure of exp(h̃) under the cover product for every subalgebra of the Heisenberg
algebra over F_3 (all pairs) and 40 random subalgebras of free(2,3) over F_5.

*Dilations.* E_{s/θ}(δ_θ a) = E_s(a), so δ_θ(E_s^{-1}h) = E_{s/θ}^{-1}h and δ_θ permutes
{E_s^{-1}h : s ∈ F_p^×}. Also immediate from homogeneity. δ_0 is not an automorphism, and §4
(l. 470) never applies it.

*Every H.* Nothing above uses normality, grading, or any property of H beyond h being a
subspace; that h = log H is a subspace and subalgebra for every subgroup is the subgroup form of
Lazard (cited; the additive part is the nontrivial direction). Checked (L1, L2): every
two-generator subgroup of the Heisenberg group over F_3, and 60 + 40 random subgroups of the
Heisenberg and free(2,3) groups over F_5, equal exp of the Lie closure of the generators.

### 2.3 Lifted source (`lem:lifted-source`), query and gate count

After computing E_{s_i}(a) into a workspace (a public linear map with entries s^k in the graded
basis, O(mn) field operations), querying U_f into a fresh w-bit register and uncomputing, the
state is |G̃|^{-1/2}Σ_a|a⟩|f̂(a)⟩; tracing the labels gives entries |G̃|^{-1}[f̂(a) = f̂(b)] =
|G̃|^{-1}1_{exp h̃}(a^{-1}∗b), which are those of ρ_{exp h̃} (§2's convention ⟨x|ρ_J|y⟩ =
|G|^{-1}1_J(x^{-1}y)). Exactly c queries; nothing about H is used: f̂ needs only the public bases
of γ_k and the fixed points. "Exactly" assumes an exact uniform superposition; §6 compiles it.

### 2.4 Single pullback (`prop:single-evaluation`) and fewer points (`rem:fewer-points`)

*Prop.* For z ∈ γ_2, u = s·tz − t²z ∈ A, E_s(u) = 0, E_s(δ_θu) = s²θ(1−θ)z with nonzero
coefficient for θ ∉ {0,1}; so invariance forces γ_2 ⊆ h. Conversely, if γ_2 ⊆ h, E_s(a) ∈ h ⇔
x_1 ∈ h, a condition δ_θ preserves. Correct for every single θ ≠ 1. The F_3 example:
δ_2(tz − t²z) = 2tz − 4t²z = 2tz − t²z, E_1 = z. Correct.

*Remark.* (⇐) If γ_{k+1} ⊆ h, grades > k impose nothing and the k × k matrix (s_i^j) is invertible,
so P_k = h̃. (⇒) For z ∈ γ_{k+1}, q(T) = T∏(T − s_i) has degree k+1, u = Σq_jt^jz ∈ A (z ∈ γ_j for
j ≤ k+1), E_s(u) = q(s)z, u ∈ P_k; F_p^× has p − 1 ≥ c > k elements, so some θs_1 ∉ {s_i}, and
E_{s_1}(δ_θu) = q(θs_1)z with q(θs_1) ≠ 0 forces z ∈ h. Correct.

*What "suffice" means (F2).* The remark proves that with k < c' points the pulled-back subgroup is
not invariant under all dilations for H = 1 (or any H with γ_{k+1} ⊄ h); it does not prove that no
algorithm with fewer queries per source exists, and it does not claim to. The sentence should say
which property fails. Note also that the "every dilation" quantifier cannot be weakened for k ≥ 2:
P_{{1,−1}} is preserved by δ_{−1} for every H, since δ_{−1} swaps E_1^{-1}h and E_{−1}^{-1}h. The
exhaustive count H7 finds 3724 triples (h, S, θ ≠ 1) for free(2,3) and for filiform(5) over F_5,
261 / 260 / 160 / 114 in the sampled runs, with θ preserving P_S although γ_{k+1} ⊄ h. The
descent uses δ_θ for arbitrary solver outputs θ, so "every" is what is needed, and that is what
the remark states; nothing in the paper relies on a single-θ form for k ≥ 2.

*Is "c distinct nonzero points" necessary and sufficient?* Sufficient: `lem:homogeneous`.
Necessary, for the property "dilation-invariant for every H": with fewer distinct nonzero points,
H = 1 fails when the class is exactly c (remark); a point 0 contributes nothing (E_0 = 0) and a
repeat contributes nothing (negative control H6: with {0,1,…} or {1,1,…} the pullback for H = 1
has dimension 1–3 instead of 0). If the true class c' < c, c' points suffice, consistent with the
remark ("only when γ_{k+1} = 0"). Edge p = c + 1 (points 1..c are all of F_p^×): checked with
filiform(5) over F_5 (class 4) exhaustively and filiform(7) over F_7 (class 6) sampled, plus the
Heisenberg algebra over F_3. For p ≤ c both the BCH group (Dynkin denominators) and the existence
of c nonzero points fail, so the hypothesis p > c is used twice and cannot be dropped.

### 2.5 Coset-copy input (`lem:copy-lift`)

R is a homomorphism (R_gR_h|x⟩ = |xh^{-1}g^{-1}⟩ = R_{gh}|x⟩), R_g^† = R_{g^{-1}},
tr(ρ_HR_g) = |G|^{-1}Σ_{h∈H}tr R_{hg} = 1_H(g). The controlled unitary Σ_a|a⟩⟨a| ⊗ ⊗_iR_{E_{s_i}(a)}
followed by tracing the copies gives entries |G̃|^{-1}∏_i tr(ρ_H R_{E_{s_i}(b)}^{-1}R_{E_{s_i}(a)}) =
|G̃|^{-1}∏_i1_H(E_{s_i}(b^{-1}∗a)) = |G̃|^{-1}1_{exp h̃}(b^{-1}∗a), which equals the ρ_{exp h̃} entry
because exp h̃ is a subgroup (F1 again). Correct. The statement "Exactly c fresh copies" is true as
a count of what the procedure uses; with k < c copies the same construction gives ρ_{exp P_k},
which by the remark is not dilation-invariant for H = 1, but that is a statement about this
construction, not a lower bound (F4).

### 2.6 Dixmier–Lister (§3.4) and `prop:dl-central-scalars`

Re-derived by hand: γ_2 = span(e5..e8), γ_3 = span(e7,e8), γ_4 = 0, [γ_2,γ_2] = 0; the centre is
γ_3 (brackets with e1 kill c2..c5, with e2 kill c1, c6). The grading argument: a positive grading
gives the derivation D|_{L_k} = k; dividing the degrees by their gcd keeps a grading with some
degree prime to p, so D is not nilpotent; all derivations are nilpotent for p > 3; contradiction.
Correct. The proof of the proposition, line by line: the rank-one locus of x ↦ ([x,L]+γ_3)/γ_3 is
(U_+ ∪ U_−) \ 0, so A preserves or swaps U_±; keep case P = μ, Q = ν, μ³ = ν³ = ζ, and the e_7
coefficient of [φu_1, φu_3] (corrections lie in Ke_8 because [U_+,v_−] = [U_−,v_+] = 0) gives
ζ = μν, so ζ = ζ² = 1; swap case ψ_−^{-1}ψ_+ has determinant −1, α³ = β³ = −ζ, ζ = −αβ, so
ζ³ = −ζ² and ζ = −1; the sign map works. Correct, in every characteristic other than 2.

Computer checks (`dl_checks.sage`, `dl_checks.out`):
| Item | Result |
|---|---|
| Jacobi over Z on all basis triples | holds |
| centre | span(e7,e8) over Q and mod 3, 5, 7, 11, 13 |
| derivation system | 224 equations, 64 unknowns; rank 52 over Q and mod every prime 5 ≤ p ≤ 29; rank 50 mod 2 and 48 mod 3 (derivation spaces of dimension 14 and 16, outside the paper's p > 3) |
| printed 12-parameter family | rank 12, satisfies all 224 equations, equals the kernel over Q |
| row certificates | for each of the 32 coefficients (e_1..e_4 parts of De_1..De_8) the least N with N·(unit vector) in the Z-row lattice is 1, 3 or 6, exactly the multipliers the paper names, so all 32 vanish in every characteristic p > 3 |
| u-basis table | all 13 displayed identities hold over Q(i) |
| sign automorphism | preserves all ten brackets, acts as −1 on γ_3 |
| Aut over F_5 (`dl_aut_p5.py`) | rank-one locus = (U_+ ∪ U_−)\0, 48 vectors; |Aut| = 5^8·2500 = 4·5^12; image on centre of order 4, scalars ±1 |
| Gröbner form of the proposition, p = 5 | NOT computed (elimination killed after 30 min; fixed ζ = 1 timed out at 300 s) |

## 3. Finite checks (scripts in `2026-11-12-rees-harsh-sec3/`)

All checks below agree with the paper; none can prove anything.

| Script | What | Result |
|---|---|---|
| `check_structure.py` | `thm:rees-cover` (i)–(iii): Jacobi, lower central series, A closed, class(A) = class(L), top grade central, E_s Lie and group hom for every s ∈ F_p incl. 0, onto for s ≠ 0, δ_θ automorphism, E_s∘δ_θ = E_{θs}, BCH associativity and inverses (own Dynkin implementation). Heisenberg F_3, F_5; free(2,3) F_5, F_7; free(3,2) F_3, F_5; filiform(5) F_5 (c = 4 = p−1); filiform(7) F_7 (c = 6 = p−1); DL F_5, F_7 | 0 failures |
| `check_homogenization.py` | Lemma, Prop and Remark at Lie level for every subalgebra: Heisenberg F_3, F_5, F_7 (19, 39, 67), free(2,3) F_5 (1901), filiform(5) F_5 (1901), exhaustive; every c-subset and k-subset of F_p^×, every θ. Sampled (≈200 adversarial and random subalgebras): free(3,2) F_3, F_5; free(2,3) F_7; filiform(7) F_7; DL F_5, F_7 | 0 failures; H7 single-θ counts as in §2.4; negative controls H6 behave as predicted |
| `check_oracle.py` | Group-level f̂ with an honest coset oracle (min over the coset, built by BCH, used as a black box): exhaustive Heisenberg F_3 (19 subgroups × 6561 pairs); sampled ~1000 pairs per algebra on Heisenberg F_5, F_7, free(2,3) F_5, F_7, free(3,2) F_5, filiform(5) F_5, DL F_5, F_7, with point sets {1..c}, random, and sets containing ±s; pairs b = a∗u with u ∈ h̃, u ∈ P_{c−1}\h̃, random. Query count c per f̂. Paper examples. Negative control with 2 points at class 3 | 0 mismatches; examples as printed; control finds equal labels off exp(h̃) |
| `check_copylift.py` | State-level simulation: copy lift (each copy a mixture of normalised coset states, controlled R_{E_s(a)}, partial trace) and oracle lift, vs ρ_{exp h̃}: Heisenberg F_3 (all 19 H), F_5 (7 H); tr(ρ_HR_g) = 1_H(g) with explicit permutation matrices | max entry error 2e−17; one-point and dirty-workspace controls differ from the target |
| `check_lazard_subgroups.py` | Subgroup form of Lazard (samples) and closure of exp(h̃) under the cover product | 0 failures: all 729 two-generator subgroups of the Heisenberg group over F_3, 100 random subgroups over F_5 equal exp(Lie closure); exp(h̃) closed (all pairs, F_3; random, free(2,3) F_5). A first run reported 575 failures from a bug in my test (random coefficients drawn per coordinate, not per basis vector); after the fix, 0 |
| `dl_checks.sage` | §3.4 and `prop:dl-central-scalars` | see §2.6 |
| `dl_aut_p5.py` | independent count of Aut(L_DL ⊗ F_5) and its image on the centre | rank-one locus of x ↦ [x,L] mod γ_3 is exactly (U_+ ∪ U_−)\0 (48 vectors); summing affine solution counts over all 460800 block maps gives \|Aut\| = 5^8 · 2500 = 4·5^12 (matches the paper); image on the centre has 4 elements {±I, ±(e_7↔e_8)}, scalars only ±1 (matches) |

## 4. Replacement text (do not apply without the owner; line numbers of main-core.tex today)

**F1, `lem:homogeneous` (l. 302).** Replace "This is a Lie subalgebra, and every $\delta_\theta$
with $\theta \ne 0$ preserves it." by

```latex
This is a Lie subalgebra, and every $\delta_\theta$ with $\theta \ne 0$ preserves it. In
particular $\exp(\hlift) = \bigcap_{i=1}^c E_{s_i}^{-1}(H)$ is a subgroup of $\widetilde G$.
```

and append to the proof (after l. 307):

```latex
The intersection of the preimages $E_{s_i}^{-1}(H)$ of the subgroup $H$ under the group
homomorphisms $E_{s_i}$ (Theorem~\ref{thm:rees-cover}(iii)) is a subgroup, and by the first
part it equals $\exp(\hlift)$.
```

**F2, `rem:fewer-points` (l. 334).** Replace "So $k$ points suffice for every $H$ only when
$\gamma_{k+1}(\mathcal{L}) = 0$." by

```latex
So $k$ points give a dilation-invariant pulled-back subgroup for every $H$ only when
$\gamma_{k+1}(\mathcal{L}) = 0$; this concerns the pullback construction, not the number of
queries any algorithm needs. For $k \ge 2$ the quantifier over all $\theta$ cannot be
weakened: for $\{s_1,s_2\} = \{1,-1\}$ the single dilation $\delta_{-1}$ exchanges
$E_1^{-1}(\hh)$ and $E_{-1}^{-1}(\hh)$, so it preserves $P_2$ for every $H$.
```

**F3, l. 341.** Replace "the element $u$ of the proof is $2tq - 3t^2q + t^3q$ with
$q \in \gamma_3(\mathcal{L})$" by "the element $u$ of the proof is $2tz' - 3t^2z' + t^3z'$ with
$z' \in \gamma_3(\mathcal{L})$" (q already names the polynomial T∏(T − s_i)).

**F4, `lem:copy-lift` (l. 347).** Replace "Exactly $c$ fresh copies of $\rho_H$ produce" by
"Using $c$ fresh copies of $\rho_H$, one for each point, the following procedure produces".

**Optional, §3.1 preamble (l. 274).** "$y \in \gamma_k(\mathcal{L})$" → "$y$ in a basis of
$\gamma_k(\mathcal{L})$".

## 5. What is new compared with earlier referee reports

Earlier reports (referee 9 I7/I8/S6; referees 2, 3-body, 17, 18; check-core; core-proof-check;
the 11-09 DL-scalars referee) found `thm:rees-cover`, `lem:homogeneous`, `prop:single-evaluation`,
`lem:copy-lift`, §3.4 and `prop:dl-central-scalars` correct, and their fixes (points named in
`lem:copy-lift`, the class sentence, the corrected DL table, the printed row certificates) are in
the current text. New here:

- `rem:fewer-points` and the §1.3 class-three example (added 12 November) had only the author's
  finite check; this is their first independent referee. Verdict CORRECT WITH FIXES (F2, F3),
  including the observation that the single-θ version is false for k ≥ 2 (exhaustive counts).
- F1 (exp(h̃) is a subgroup, never stated) was not raised before.
- F4 (wording "Exactly c") was not raised; referee 9's I7 fixed a different defect of the same
  sentence.
- The group-level tuple oracle was checked here with an honest coset oracle built from H by BCH
  and used as a black box, and the copy lift by a state-level simulation with each copy a
  mixture of coset states; earlier checks used the Lie-level criterion or the closed-form entry.
- Remark checks at p = c + 1 (filiform class 4 over F_5, class 6 over F_7) and with point sets
  containing ±s.
- DL: derivation-space dimensions mod 2 and 3 (14, 16) recorded; row certificates re-derived as
  least multipliers in the Z-row lattice; an independent exhaustive automorphism count at p = 5 that reproduces the GAP order 4·5^12 and the central image without GAP (earlier checks used `autpgrp`).

## 6. Adversarial self-check

- *Could my scripts share an error with the paper?* They were written from the tex, with my own
  Dynkin BCH (checked by associativity on random triples in every algebra), my own linear algebra
  and my own coset oracle; I imported nothing from the repo. A shared misreading of a definition
  (for example the left/right coset convention) would make both agree wrongly; I re-derived the
  convention chain by hand (f(x)=f(y) ⇔ x^{-1}y ∈ H, ⟨x|ρ_H|y⟩ = 1_H(x^{-1}y)/|G|, R_g|x⟩ = |xg^{-1}⟩)
  and the simulation uses explicit permutation matrices, so a convention slip would have shown
  as a nonzero error.
- *My own test bugs.* One script (`check_lazard_subgroups.py`, L3) first reported 575 failures;
  the cause was in the test (it drew random coefficients per coordinate instead of per basis
  vector, so its "elements of h̃" were not in h̃). I fixed the test, not the claim, and the rerun
  gives 0; the exhaustive F_3 part, which enumerates h̃, never failed. The elimination-ideal form
  of the Gröbner check (ζ as a variable) did not finish in 30 minutes at p = 5 and was killed:
  NOT computed; the fixed-ζ form replaced it.
- *Exhaustive only on tiny cases.* Exhaustive coverage is for 5 algebras of dimension ≤ 5 at
  p ≤ 7; the larger ones are sampled (~200 subalgebras each, biased toward 1–3 generators). The
  proofs, not the checks, carry the claims; the checks would catch a wrong statement only if a
  small counterexample existed.
- *Did I miss a non-subalgebra H?* No: Lazard makes every log H a subalgebra; L1/L2 confirm this on
  samples, and the proofs use only that h is a subspace.
- *Is F1 a real gap?* No, it is a missing sentence with a one-line proof; I rate it a fix, not a GAP.
- *Is "every dilation" really what §4 needs?* The descent applies δ_{s_i} for whatever nonzero s_i
  the solver returns, so invariance under all θ ∈ F_p^× is required, and `lem:homogeneous` gives it.
  I did not re-referee §4 (see the sibling report `2026-11-12-rees-harsh-sec4.md`).
- *Citations.* I could not check Khukhro's locators (Remark 9.17, §10.2, Example 10.24) offline;
  the arguments do not depend on the locators. Identity of the printed table with Dixmier–Lister
  1957 was not checked against the source (no network); the paper proves all properties it uses
  from the printed table.
- *Unverified by me.* The GAP orders at p = 7 (12·7^12, central image of order 12) were not recomputed; my count covers p = 5 only; the
  Lean claims of Appendix A; the uniform-superposition preparation and gate counts (§6).
- Everything here is AI-checked and pending human review.
