# Rees HSP paper: unanchored referee report (round 2, item 2)

Date: 2026-11-02. Reviewer: one AI session (Claude Opus 5.5) acting as a referee for a
top theory venue (QIP, STOC or SICOMP). **AI-checked, pending human review.** No claim
gate changes because of this report.

Object: `docs/papers/rees-hsp/main-full-draft.tex` (782 lines), read in full once, top to
bottom. I wrote my own findings before grepping the round-1 reports. Only after that did I
grep them for overlap, and each issue below says whether round 1 already knew it. I read
no round-1 report as a whole. I fetched four primary sources from arXiv and grepped them:
Ivanyos–Santha (IS17) arXiv:1503.09016v2, Imran–Ivanyos (II23) arXiv:2304.08376,
Ivanyos–Sanselme–Santha (ISS12) arXiv:0707.1260, and Ivanyos–Magniez–Santha (IMS)
arXiv:quant-ph/0102014. Line numbers refer to the draft.

Evidence labels: **proved** (by me, written out here), **exact computation**, **float
check**, **argued**, **literature** (read in the primary source).

## 0. Summary for the editor

The paper proposes a quantum algorithm for the HSP in a finite p-group G of class
c < p, given by an explicit Lazard Lie algebra L ≅ F_p^m, for an arbitrary hidden
subgroup H. It runs in time polynomial in m and log p for every fixed c. The idea is to
query f at c points of the positive lower-central Rees cover A = ⊕ t^k γ_k(L). The pulled-back
hidden subgroup is then homogeneous, so the torus of dilations preserves it. That supplies
the scalar weights s^d for the degree-by-degree SDE elimination of IS17 §5, which
Imran–Ivanyos observe are unavailable on G itself beyond class two.

**I found no error in the core argument.** I re-derived each step of the main line myself:
Thm 2.1, Lemma 2.2, Lemma 2.5, Lemma 3.1, Prop 3.2, the recursion of §3.2 and the Schedule 1
arity. Exact or float checks reproduce each one (§3 below). I found the core idea correct
and, as far as I know, new. The paper is still **not reviewable in its present form**, and
the reasons are structural:

- It reads as a project log. It has a status box, about fifteen "the previous version
  claimed…" passages, AI-provenance notes and repository file paths in place of proofs.
- About half of its stated results are "restated from the project notes; proof not
  reproduced here."
- Its strongest consequence is never stated.
- The proof of the main theorem's complexity bound is spread over Sections 3–4 and an
  external note.

**Recommendation:** major revision. For a conference it would be a reject in the current
form, with resubmission strongly encouraged as a focused paper (see §5).

## 1. Fatal issues

### F1. The manuscript is not self-contained: several theorems' proofs are not in the paper (fatal as submitted; fixable)

- **Location.** Status box (l. 62–88). Abstract, last three sentences (l. 99). Thm 3.4(ii)
  and the paragraph after it (l. 440–450: "its proof is not reproduced here"). Prop 3.5 and
  the paragraph after it (l. 452–457). Thm 3.7 (l. 467–476: "restated from the project
  notes"). Cor 5.1, IS-branch charges (l. 563–572). Cor 5.2(ii) (l. 579). Thm 5.4 (l. 601–613).
  Prop 6.1 (l. 631–639: "comes from project notes still under review"). Thm 6.2 and
  Cor 6.3 (l. 648–682). Remark 7.2 (l. 712–721).
- **Why.** A referee can check only what is in the paper. "An AI session proved this,"
  "checked in writing by an AI session," and a file path are not proofs. In a venue
  submission they are reasons to desk-reject. The "previous version" passages document a
  draft history the reader never saw: l. 63–72, 161, 210, 284, 305, 363, 397–401, 431,
  476, 591, 637, 684, 693, 732. Some of them are mathematically useful, notably Prop 2.3
  and Remark 3.3, and those should stay as stated facts. As a narrative they undercut
  confidence.
- **Fix.**
  1. The core paper consists of §2 (minus Prop 2.6), §3.1–3.2 with Schedule 1 only, the
     compilation theorem, and a "Proof of Theorem 1.2" subsection (text in P5–P6). Each of
     these gets a complete proof.
  2. Each conditional result either gets a journal-level appendix proof (items 14–18 are
     writing them) or moves to a short "Outlook and conditional extensions" section,
     stated in prose with no theorem environment.
  3. Delete the status box and all draft history from the body. Withdrawn claims belong in
     the change log, not the paper.
  4. Replace file paths with an "Artifacts" appendix.
- **Known in round 1?** Partly. The integration log (I3, I4) edits the status box rather
  than removing it, and the campaign's appendix items address the missing proofs. No
  round-1 report states that the paper is unreviewable in this form.

No issue is mathematically fatal. I looked hard for one in the main line and found none
(§3).

## 2. Major issues

### M1. The strongest consequence is never stated (positioning)

- **Location.** Related work (l. 123); §6.1 (l. 629–639); the outer-envelope paragraph
  (l. 554).
- **Why.** II23 §6 (literature, read) asks for an efficient, possibly non-exact, HSP
  algorithm for nilpotent groups of bounded class and smooth order. A positive answer
  would follow from a randomized zero-sum finder (their Prop 3). Thm 1.2 gives a non-exact
  polynomial-time algorithm for explicit Lazard p-groups of class c < p, for every p > c,
  including p far from smooth. Prop 6.1(ii) composes the free-Lie pullback with Thm 1.2
  (e = 1) or with the ring-to-field recursion (e > 1, route R1, using Thm 1.2 on each
  socle section). Add the Sylow split of l. 629 and II23 Thm 1 for p ≤ c, and the draft is
  one composition away from claiming a non-exact polynomial-time HSP algorithm for every
  black-box nilpotent group of bounded class with unique encoding. That would be the
  headline of the paper. The draft instead hedges four times ("If Theorem 1.2 is
  correct…") and leaves the composition to a table row and a numeric paragraph. A referee
  will ask one of two things: (a) state and prove it, or (b) say plainly that it is not
  claimed and name the missing step, which campaign item 7 calls gap C6. The current
  middle course invites the suspicion that the authors could not make it work.
- **Fix.** Add a "Consequences" paragraph after Thm 1.2 stating exactly which open question
  is resolved, and for which input model. If item 7 closes the envelope, state the
  black-box theorem as Corollary 1.3, with its own proof.
- **Known in round 1?** Partly. The priority check §5b discusses II23 §6, and round-2
  item 7 is assigned the composition. The framing problem itself is not raised.

### M2. Related-work misstatements and omissions

- **Location.** l. 117 and l. 123.
- **Why.**
  1. *Bacon–Childs–van Dam (FOCS 2005) is missing.* IS17 p. 4 (literature) says that
     Bacon, Childs and van Dam found the efficient algorithm for F_p ⋉ F_p^m with hidden
     subgroups of order p outside F_p^m when m is constant. It also says that
     Decker–Ivanyos–Santha–Wocjan [10] sketched the translation to a hidden polynomial
     graph problem. The draft credits the constant-m case to
     Decker–Høyer–Ivanyos–Santha 2014 alone and never cites BCvD. II23 also cites
     "[DHIS14, IS17]" for higher-class HSP, so DHIS is not wrong to mention, but the
     original HSP credit belongs to BCvD.
  2. "These results are special cases of its regime" needs the qualifier "for p > c." IS17
     Cor 8 covers p ≤ class through FIMSS (IS17 §5, Proof of Thm 5).
  3. Abelian HSP is credited to ISS12 (l. 117). Cite Kitaev, or Shor and Kitaev.
  4. Ettinger–Høyer–Knill (IPL 2004) is missing. The quantum query complexity of every HSP
     is poly(log|G|), so the "c queries per lifted source" is not the contribution. The
     contribution is running time, and the paper should say so.
  5. ISS12 Thm 2 (literature) reduces the HSP in any constant-class family closed under
     subgroups and quotients to exponent p with |H| ≤ p. It is the obvious alternative
     route to the prime-power and black-box extensions of §5.2 and §6.1. The paper should
     either use it or say why not. For example, ISS12's reduction produces black-box
     exponent-p sections, not explicit Lazard charts, and Prop 6.1(i) might supply those
     charts.
- **Checked correct (literature):** ISS12 Thm 2 as quoted at l. 123; IS17 Cor 8; IS17 §§3.1–3.3
  and Thm 11; IMS Thm 11 ("time polynomial in the input size + |G′|," black box with unique
  encoding); II23 Thm 1, Prop 3 and §6, and the §1 remark about automorphisms beyond class
  two.
- **Fix.** Proposed text P1 and P2; add bib entries.
- **Known in round 1?** (1) Partly: the priority check l. 172 quotes IS17's sentence on
  BCvD, but the draft never acted on it. (2) Not raised. (3) Not raised. (4) Not raised as a
  positioning point; EHK appears only in a search table. (5) Yes: priority check item 8,
  "a second look at ISS Thm 2," which remains open.

### M3. Theorem 1.2 has no single proof, and its quantitative claims are implicit

- **Location.** Thm 1.2 (l. 176–179). Error budget (l. 413–419): "A hybrid bound over
  complete instruments … controls the total" is asserted, not proved. Thm 4.1(iii)
  (l. 493: "by the restricted-domain hybrid of the note").
- **Why.**
  - The theorem says "polynomial" without the exponent or the c-dependence. The exponent
    appears only at l. 431, for c = 9. The dependence is m^{1+Σ_{d≤c} d⌈log₂(d+1)⌉} times a
    constant C_c, so the algorithm is polynomial at fixed c and non-uniform in c. The title
    word "Uniform" suggests otherwise.
  - The error composition across adaptively chosen instruments is a standard telescoping
    argument, but it must appear.
  - The QFT error rests on an external note.
- **Fix.** Proposed text P5 (explicit count), P4 (hybrid lemma) and P6 (proof assembly). In
  Thm 4.1(iii), state and prove the restricted-domain hybrid, or cite a standard source.
- **Known in round 1?** Partly. The compilation-filters report fixed q_max and the
  citations, but no report asked for an assembled proof or an explicit exponent in the
  statement.

### M4. Theorem statements use objects the paper never defines

- **Location.**
  - Prop 3.5 (l. 452–454): "universal two-level contraction of the decoupled form
    C_ij = z_i z_j(α_j+β_i)" is never defined. T_S(κ) has no definition. The sets E_2(κ)
    (l. 457) are reported from computations with no method given.
  - Thm 3.4(ii) (l. 440): "the two-level symmetric construction of [file]." The algorithm
    is not described.
  - Thm 3.7(i): "fair-bit field sampling capped …" is undefined.
  - Prop 6.1(i): the constants m_+, q_+, m_[], q_[] are undefined.
- **Why.** A theorem whose objects are undefined cannot be checked, and readers will take it
  as a claim, not a result.
- **Fix.** Define the contraction (a half page) and give the E_2 computation in an
  appendix, or remove Prop 3.5 and Thm 3.4(ii) from theorem environments. Neither is used
  by Thm 1.2.
- **Known in round 1?** No. The small-prime and Weil reports define these objects
  internally, but the draft does not carry the definitions over.

### M5. A hypothesis is stated in terms of hidden data

- **Location.** Thm 3.7: "a_d ≤ u−1 for every d" (l. 468). Table 1, random-column row:
  "u > max_d a_d" (l. 201).
- **Why.** a_d = g_d − dim(h ∩ γ_d) depends on H. As stated, the algorithm needs a quantity
  it cannot know. The uses in Cor 5.1 (u = r+1 ≥ g_d+1) and Cor 5.2 (a_d ≤ k by the
  codimension promise) are fine, but the theorem itself must quantify over a public bound
  or a promise. The abort rule at l. 476 ("observed rank exceeds the supplied bound")
  already assumes this.
- **Fix.** Proposed text P7.
- **Known in round 1?** Not as a hidden-assumption issue.

## 3. Spot checks of the most suspicious claims

All scripts are in
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/47273003-b9d0-49f7-9562-0ceaaa7afd1b/scratchpad/scripts/`,
with outputs in `…/scratchpad/out/`. They are independent of the repo code. The
interpreter is `/opt/anaconda3/bin/python -I`. My row lists no folder of my own, so they
stay in the scratchpad. They are short and can be rerun from the descriptions below.

### S0. Literature: the IS17 Theorem 3 threshold (§3.3, l. 431)

The draft claims the printed threshold of IS17 Thm 3 is not implied by its own proof. This
is the boldest claim in the paper, since it says a published theorem is misstated.

- IS17 v2 p. 3 prints "n > d^{d² log d}(m+1)^{d log d}." The end of §3.3 reads
  "C(d,m) ≤ G(d,m)^{⌈log₂(d+1)⌉} ≤ d^{d² log d}(m+1)^{d log d}," with
  G(d,m) = d^{d(d−1)/2}(m+1)^d (Thm 11).
- The (m+1)-exponents are d⌈log₂(d+1)⌉ and d log d. Since ⌈log₂(d+1)⌉ > log₂ d for every
  d ≥ 2, and a natural log only lowers the right side, **the second inequality is false for
  every d ≥ 2 once m is large.** At d = 2 the exponents are 4 and 2.
- The first inequality is exactly what the iteration gives: 2^ℓ representations from G^ℓ
  vectors, then Fact 2 once 2^ℓ ≥ d+1. The draft's B_d(a) is therefore correct, and so is
  its refusal to use the printed bound. **Literature, confirmed.**
- Also confirmed: the algorithm is deterministic. §3.1 avoids nonresidues by a Pohlig–Hellman
  classification with restarts, and Fact 2 (van de Woestijne) is deterministic. Only the
  warm-up Props 9 and 10 are randomized. The Bezout reduction to κ = gcd(d, q−1) is in IS17
  §3. **Literature.**
- One correction: Thm 1.2 says its "only non-elementary dependency" is IS17. IS17 itself
  depends on van de Woestijne's thesis, which should be named.

### S1. The core line, independently re-implemented (float check, tolerance 1e-9)

I re-implemented the main line on Heis(F_p) for p = 3 (all 19 subgroups), with explicit
right-regular-representation matrices on the cover group (order 81) and the true BCH group
law. I checked:

- (a) The fibres of the tuple oracle at points 1 and 2 are the left cosets of exp(h~), at
  group level.
- (b) The copy-only lift from two explicit copies of ρ_H equals ρ_{exp h~} (Lemma 2.5).
- (c) The complete central instrument, built as explicit projectors Π_λ, gives a label law
  uniform on K^⊥ and satisfies tr(ρ_λ R_g) = χ_λ(z) on HZ and 0 off it (Lemma 3.1).
- (d) Prop 3.2 with three targets, for every label tuple in (K^⊥)³, with up to two random
  nonzero witnesses of Σ s_i²λ_i = 0 per tuple. I used two sections: the zero section, and
  a random nonhomomorphic section. The output must equal ρ_{HZ/Z} on Q = (tL, +).
- Negative control: a non-witness must give an output different from ρ_{HZ/Z}.

Result for p = 3: `{'H': 19, 'a': 19, 'b': 19, 'c': 19, 'd': 19, 'dneg': 18, 'cases': 1428}`.
All 1428 witness cases pass. The negative control fails to separate in exactly one subgroup,
H = 1, and that is expected rather than a defect: when H = 1, ρ_{HZ/Z} is the diagonal state,
and any s produces it. The control separates in the other 18 subgroups. The p = 5 run did not finish (§3.1). **Float check: reproduces Lemma 2.2, Lemma 2.5, Lemma 3.1 and
Prop 3.2.**

### S2. The Dixmier–Lister table and non-gradability (§2.3)

This is the paper's motivating example, and the previous version printed a table that fails
Jacobi. **Exact computation**, from the printed brackets:

- The Jacobi identity holds over ℤ on all 56 basis triples.
- For p = 5, 7, 11, 13, 17: lower central dimensions (8, 4, 2), dim Der = 12, every
  derivation maps L into [L, L], and every derivation is nilpotent.

This confirms class 3, cover dimension 14, and the no-grading argument of l. 285.
The paper should print the derivation computation, or a reference valid over F_p, rather
than point to an artifact. DL57 works in characteristic 0.

### S3. The worst-case exponent in Remark 3.6 (l. 461)

**Exact computation.** I took the per-grade exponent rule (linear 1, two-level 2,
otherwise κ⌈log₂(κ+1)⌉). It is non-increasing in p within each residue class modulo
lcm(2..c), so the maximum over p > c is attained at the least prime in some class. The
script finds:

| c | Schedule 1 exponent | Combined, maximum over p > c | Attained at p |
|---|---|---|---|
| 2 | 5 | 5 | 3 |
| 3 | 11 | 11 | 7 |
| 4 | 23 | 23 | 13 |
| 5 | 38 | 38 | 61 |
| 6 | 56 | 56 | 61 |
| 7 | 77 | 77 | 421 |
| 8 | 109 | **107** | 2521 |
| 9 | 145 | **143** | 2521 |

This matches the draft: unchanged for c ≤ 7, a drop of two at c = 8 and 9, and 143 against
`\ReesClassNineQueryExp` = 145.

### S4. The zero-moment design bound M ≤ (c+1)! (§6.2 step 1, l. 667)

The bound is stated as a parenthetical with no proof. The polynomiality claim of Cor 6.3 in
log p needs M to be bounded independently of p.

- **Exact computation (minimal M by dynamic programming over all multisets):**
  - c = 2, all primes p ≤ 47: M ≤ 6.
  - c = 3, p ≤ 31: M ≤ 6.
  - c = 4, p ≤ 17: M ≤ 20 (at p = 5).
  - c = 5, p ≤ 11: M ≤ 10.
  - At p = c+1 the minimum is c(c+1), because every multiplicity must be divisible by p.
- No violation. I then **proved** the bound: an inductive Chevalley–Warning construction
  gives M ≤ (c+1)! for every p > c, deterministically in poly(log p) at fixed c (Lemma in
  P3).
- **Exact computation** of that construction: it passes all tested pairs (c ≤ 5, the first
  twelve primes > c; the Chevalley–Warning branch is exercised for c ≤ 3). Script
  `s6_design_construction.py`.

### S5. The conjugation-filter claim (§7, l. 693)

The claim is that truncated exp(ad_x) differs from conjugation "exactly when
N ≤ p ≤ 2N−2," with witness J_N and E_{N1}. **Exact computation**, N = 2..6 and every prime
N ≤ p ≤ 2N+3: the witness differs exactly in the predicted range. For p ≥ 2N−1, 30 random
pairs (x, M) per case show no disagreement, as the series argument implies. Confirmed.

### Checked by hand (proved, not just plausible)

- Lemma 2.2 (Vandermonde).
- Prop 2.3.
- Lemma 2.5 entry formula.
- Prop 2.6 counterexample: all entries 1/p.
- Lemma 3.1, including the inversion g = h^{-1}(−z).
- Prop 3.2.
- Rank bound 1/((p−1)p^t).
- Thm 3.4(iii): Davenport D(C₅²) = 9; B₄(2) = 331776³ ≈ 3.65·10¹⁶.
- Thm 3.7(i): μ ≥ 2^{12u}u^{2u+1} ≥ the stated 2^{8u+1}u^{2u+1}; acceptance ≥ (E/2)/p^{M−a}
  with Chebyshev variance ≤ hE, giving the 4/μ term.
- Thm 3.7(ii): Pr[Bin(4m′, 15/16) < m′] ≤ 2^{4m′}·16^{−3m′} = 2^{−8m′} ≤ 2^{−2m′}.
- Cor 5.1: c ≤ r+1.
- Cor 5.2 steps: dim(h ∩ I) ≥ a−k; h ⊆ N(h ∩ I); dim ≤ a(a+1)/2 and class ≤ 2a−1.
- Remark 5.3 example.
- Thm 5.4(i) and (iii), including the "≤ b calls" count.
- The quotient-oracle coset identity x*I = x+I.
- Prop 6.1(iii) metacyclic example.
- Thm 6.2(i): TD = (1/r)Σ sin θ_i, overlap Π cos θ_i, AM–GM bound.
- Thm 6.2(ii): p_k and the coupon comparison.
- Steps (2) and (3) of §6.2: the phase cancellation, and TD ≤ √(p^n)(1−γ)^ℓ/2.
- Prop 7.1.
- The free-Lie example in related work: no abelian maximal subalgebra; ⟨exp x⟩ and
  ⟨exp y⟩ do not permute.

**Coset conventions.** Every use is consistently "f(x) = f(y) ⟺ x^{-1}y ∈ H," that is, left
cosets xH (Lemma 2.2, Lemma 2.5, Lemma 3.1, Prop 3.2, §6.2 step 1, the Cor 5.2 birthday
learner, the ring quotient oracle). IS17 Def 4 uses Hx = Hy. That is harmless (invert), but
the paper should state the convention once and note it where it cites IS17 Cor 8.

### 3.1 p = 5 run of S1

Not completed. The same script at p = 5 (cover of order 625, 39 subgroups) hit its 40-minute time limit, exit 124, before printing a result, so S1 covers p = 3 only. The project's exact simulator covers p = 5 (`theorems/rees_end_to_end_sim.py`), but it is not independent of the project. To finish this check, vectorize the trace computations in `s4_core_descent.py` and rerun it.

## 4. Minor issues

| # | Location | Issue | Fix |
|---|---|---|---|
| m1 | throughout | **Notation clashes** inside the core proofs. λ is both the dilation scalar (Thm 2.1(ii), Lemma 2.2, Prop 2.3) and the central label (Lemma 3.1, Prop 3.2). δ is dilation and TD gap. r is derived dimension, a register index in the proof of Prop 3.2, the subspace rank in §6.2, and a composition length (l. 554). d is SDE degree, ambient dimension ℂ^d, rank F_{s,c}, and the Möbius divisor. B is the arity B_d, the input bit length (§5.2), the trial count (Thm 3.7), B = ⌈log₂(rT/β)⌉ and B_leaf. R is the right regular representation, the cyclic rank and the representation of §6.2. K is H∩Z, a generated subgroup (l. 411), h∩I and a stabilizer. N is N_solver, N_instr, N_G(H₁), the attempt cap and the matrix size. σ is a section and a density. t is the Rees variable, the sample surplus and the zero-sum length. h is a group element and (p−1)/κ. G(d,a) collides with the group G. γ is the lower central series and an average of sin². μ is Möbius and an expectation. E is evaluation, side information and E_2(κ). Round 1 fixed only C8 and C14. | Add a notation table. Rename the dilation scalar u ∈ F_p^×, the central labels y_i, the gap Δ, the subspace rank ϱ, the rank of F_{s,c} D, the bit length β_in, h = (p−1)/κ as η, and G(d,a) as G_IS(d,a). |
| m2 | l. 178 | "Only non-elementary classical dependency is IS17": IS17 rests on van de Woestijne's deterministic solver. | Add "(which uses van de Woestijne's deterministic solver for one diagonal equation)." |
| m3 | l. 285 | Non-gradability is justified by "integer row certificates" in an artifact. | Print the derivation computation (S2) or a proof. |
| m4 | §2.4, Prop 2.6 | Not used by Thm 1.2 or any corollary. | Cut, or attach it to the coset-copy discussion. |
| m5 | §4.2, tables | Padded resource counts for a class-12 profile at a 128-bit prime, plus artifact names. These are not referee material. | Move to an artifact appendix and keep one sentence. |
| m6 | §7 | Classical filters for hypothetical applications are off-topic for the result. | Cut, or move to an appendix. |
| m7 | §8 | Guard counts, build dates and "five files outside formal/" are artifact bookkeeping. | Reduce to one paragraph: what is kernel-checked and what is not. |
| m8 | title | "Uniform Compilation" suggests uniformity in c, which is not claimed. | E.g. "Grading a Cover: A Quantum Algorithm for the Hidden Subgroup Problem in Lazard p-Groups of Fixed Class." |
| m9 | l. 491 | "exactly (d−1)d(d+1)(d+2)/6 bracket evaluations" in an "unoptimized schedule" from a note. | "at most," with a two-line derivation. |
| m10 | bib | IMS cited only as arXiv. Khukhro's book is cited inline, not in the bib. | Use the journal version of IMS (Int. J. Found. Comput. Sci. 14 (2003); confirm the theorem number there) and add Khukhro. |
| m11 | l. 274 | The negative-control paragraph concedes that the test cannot detect the failure. | Keep Prop 2.3 and its one-line example; drop the artifact paragraph. |
| m12 | §1 | No classical baseline or lower bound, so "speedup" is never argued. That is fine for an algorithm paper, but say so. | One remark citing a classical query lower bound for the family, once item 9 supplies it. |
| m13 | Cor 6.3 | The (c+1)! design bound is unproved (S4). | Proposed text P3. |
| m14 | l. 173 | The subgroup form of the Lazard correspondence for F_p-Lie algebras is cited inline. | Fine. Give the Khukhro theorem number in the bib entry. |
| m15 | §3.2, l. 411 | "K = ⟨exp b_i⟩ … log K ⊇ h": correct, but the step "log K is a Lie subalgebra containing every b_i" uses the Lazard correspondence for subgroups. | Say so. |

## 5. Recommendation and the three things most likely to sink the paper

**Recommendation: major revision** (reject in current form, encourage resubmission). The
core contribution is a clean idea with, as far as I can tell, a correct proof: homogenize
an arbitrary hidden subgroup by querying at c points of the lower-central Rees cover, then
run the IS17 degree-by-degree elimination on the cover. If it survives human review, it
merits a top venue, especially with the black-box consequence of M1. The paper around it is
not yet a paper.

1. **Form.** It reads as a lab notebook. A status box, draft history, AI provenance and file
   paths stand in for proofs, and half the stated results have their proofs outside the
   manuscript. A PC will stop reading at the status box. (F1, M4)
2. **Positioning.** The mechanism is IS17 §5 plus a cover. An expert will ask three things
   in the first paragraph. Why does this not contradict II23's remark that suitable
   automorphisms do not exist beyond class two? The answer is that they exist on the cover,
   and the paper should say so up front. What exactly is solved: II23 §6 for explicit
   Lazard p-groups, or the black-box bounded-class case? And why is BCvD missing? Unless
   the paper answers these crisply, referees will read it as an input-model-specific
   variant of known work. (M1, M2)
3. **Main theorem accounting.** The main bound depends on a corrected reading of IS17 Thm 3
   (S0, which I confirmed) and on a complexity proof assembled across Sections 3–4 and a
   note, with the hybrid lemma asserted rather than proved. A referee will want one
   self-contained proof with the explicit bound c(m + log_p(3/ε))·C_c·(m+1)^{Σ d⌈log₂(d+1)⌉}.
   (M3)

## 6. Exact statement that now holds; what is missing; claim gates

**Holds** (AI-checked, pending human review):

- Under Definition 1.1, the procedure of §§2–3 with Schedule 1 returns h with probability at
  least 1−ε using c(m + ⌈log_p(3/ε)⌉)·Π_{d=2}^c B_d(g_d) oracle queries (or as many coset
  copies, times c).
- The running time is polynomial in that count and in m, log p, the label width and
  log(1/ε). For fixed c this is polynomial. Status: argued from the lemmas, which I
  re-derived and float-checked (S1). The compilation step rests on Thm 4.1, whose part (iii)
  cites a note.
- The IS17 arity B_d(a) = G(d,a)^{⌈log₂(d+1)⌉} is what IS17's proof gives. The printed
  Thm 3 bound is not implied. (Literature, S0.)
- Zero-moment designs with M ≤ (c+1)! exist for every p > c and are computable
  deterministically. (Proved here; P3; exact computation S4.)
- The Dixmier–Lister table as printed is a Lie algebra of class 3, with all derivations
  nilpotent at p = 5..17. (Exact computation, S2.)

**Missing:**

- Self-contained proofs of Thm 3.4(ii), Prop 3.5, Thm 3.7, Cor 5.1, Cor 5.2(ii), Thm 5.4,
  Prop 6.1, Thm 6.2 and Cor 6.3 inside the paper.
- The restricted-domain QFT hybrid of Thm 4.1(iii).
- The black-box composition theorem (M1, item 7).
- Human review of everything.

**Claim gates that must stay false:** every Rees gate, in particular
`speedup_claim_allowed` in `rees_hsp_reduction.json` (including
`copy_only_outer_envelope`), `rees_subspace_source.json` and `random_column_rees.json`
(`hsp_claim`, `speedup_claim`), plus the STATE.md row "Rees nilpotent HSP cover reduction."
This report flips nothing.

## 7. Proposed paper text

Status label for every item: **AI-checked, pending human review.** The integrator places
these.

### P1. Related work, BCvD and the "p > c" qualifier

Target: §1.1 "Related work," replacing the two sentences from "Ivanyos and
Santha~\cite[Corollary~8]..." through "...special cases of its regime, and the growing-prime,
fixed-class feature is not new by itself."

```latex
Bacon, Childs and van Dam~\cite{BaconChildsVanDam2005} solve the HSP in the groups $\Fp \ltimes \Fp^m$ with $m$ constant, for hidden subgroups of order $p$ not contained in $\Fp^m$. Ivanyos and Santha~\cite[Corollary~8]{IvanyosSantha2015} remove the restriction on $m$ when the nilpotency class is constant, by a reduction~\cite[Proposition~7]{IvanyosSantha2015} to a hidden polynomial graph problem that Decker, H{\o}yer, Ivanyos and Santha~\cite{DeckerHoyerIvanyosSantha2014} had solved for constant $m$ and degree. Once $p$ exceeds the class, these groups are Lazard groups of class below $p$ whose Lie algebra the matrix logarithm gives explicitly, and their hidden subgroups are a special case of an arbitrary $H$. So, if Theorem~\ref{thm:main} is correct, these results are special cases of its regime when $p > c$ (for $p$ at most the class,~\cite{IvanyosSantha2015} uses~\cite{FIMSS2014}, which is not covered here), and the growing-prime, fixed-class feature is not new by itself.
```

New bib entry (arXiv id confirmed from the abs page, 2026-11-02):

```bibtex
@inproceedings{BaconChildsVanDam2005,
  author    = {Bacon, Dave and Childs, Andrew M. and van Dam, Wim},
  title     = {From Optimal Measurement to Efficient Quantum Algorithms for the Hidden Subgroup Problem over Semidirect Product Groups},
  booktitle = {46th Annual IEEE Symposium on Foundations of Computer Science (FOCS)},
  pages     = {469--478},
  year      = {2005},
  note      = {arXiv:quant-ph/0504083}
}
```

### P2. Abelian credit and query complexity

Target: l. 117, replacing "Abelian groups and nilpotent groups of class two admit
polynomial-time quantum algorithms~\cite{IvanyosSanselmeSantha2012}."

```latex
Abelian groups admit polynomial-time quantum algorithms (Kitaev, \arxivid{quant-ph/9511026}), and so do nilpotent groups of class two~\cite{IvanyosSanselmeSantha2012}. The quantum query complexity of the HSP is polynomial in $\log|G|$ for every finite group~\cite{EttingerHoyerKnill2004}, so the question for nilpotent groups is running time, not queries.
```

(arXiv id confirmed from the abs page.)

```bibtex
@article{EttingerHoyerKnill2004,
  author  = {Ettinger, Mark and H{\o}yer, Peter and Knill, Emanuel},
  title   = {The Quantum Query Complexity of the Hidden Subgroup Problem is Polynomial},
  journal = {Information Processing Letters},
  volume  = {91},
  number  = {1},
  pages   = {43--48},
  year    = {2004},
  note    = {arXiv:quant-ph/0401083}
}
```

### P3. Zero-moment designs (proved here)

Target: §6.2. Insert before the four-step enumerate, and replace "($M \le (c+1)!$)" in step (1)
with "(Lemma~\ref{lem:zero-moment})".

```latex
\begin{lemma}[Zero-moment designs]
\label{lem:zero-moment}
For every prime $p > c$ there is a multiset $S$ of $M \le (c+1)!$ nonzero elements of $\Fp$, with at least $c$ distinct elements, such that $\sum_{s\in S}s^j = 0$ for $j = 1,\dots,c$. For fixed $c$ it can be computed deterministically in time $\poly(\log p)$.
\end{lemma}

\begin{proof}
If $p \le (c+1)!$, take every element of $\Fp^\times$ once when $c < p-1$, and $p$ times when $c = p-1$. Since $\sum_{s\in\Fp^\times}s^j = 0$ for $1 \le j < p-1$, this works; its size is $p-1$ or $p(p-1) = c(c+1)$, both at most $(c+1)!$, and it has $p-1 \ge c$ distinct elements.

Now let $p > (c+1)!$ and put $S_0 = \{1\}$. For $j = 1,\dots,c$, the form $x_0^j + \cdots + x_j^j$ has $j+1 > j$ variables, so by the Chevalley--Warning theorem it has a nonzero zero $(x_0,\dots,x_j) \in \Fp^{j+1}$, and van de Woestijne's algorithm finds one deterministically in time polynomial in $j$ and $\log p$~\cite[Fact~2]{IvanyosSantha2015}. Let $S_j$ be the multiset union of the dilates $x_iS_{j-1}$ over the indices $i$ with $x_i \ne 0$. Its elements are nonzero, $|S_j| \le (j+1)|S_{j-1}|$, and for $1 \le k \le j$
\[
  \sum_{s\in S_j}s^k = \Bigl(\sum_{i} x_i^k\Bigr)\sum_{s\in S_{j-1}}s^k ,
\]
which vanishes for $k < j$ by induction and for $k = j$ by the choice of $x$. So $S = S_c$ has the required power sums and size at most $(c+1)!$. Suppose $S$ had at most $c$ distinct elements $v_1,\dots,v_e$, with multiplicities $\mu_1,\dots,\mu_e$. The equations for $k = 1,\dots,e$ have the invertible matrix $(v_i^k)_{i,k\le e}$, so every $\mu_i \equiv 0 \pmod p$. That is impossible, since $0 < \mu_i \le (c+1)! < p$. Hence $S$ has at least $c+1$ distinct elements.
\end{proof}
```

### P4. Sequential hybrid lemma

Target: §3.2. Insert before "A hybrid bound over complete instruments, with their records and
abort outcomes, controls the total", and change that sentence to "Lemma~\ref{lem:hybrid}
controls the total; no division by small branch probabilities occurs."

```latex
\begin{lemma}[Sequential hybrid]
\label{lem:hybrid}
Let an ideal procedure apply quantum instruments $\mathcal{I}_1,\dots,\mathcal{I}_N$ in sequence, each possibly chosen from the earlier classical records, and let the implemented procedure apply $\widetilde{\mathcal{I}}_j$ in place of $\mathcal{I}_j$. View each instrument as a channel whose output is its quantum output together with a classical record register, and suppose $\frac12\|\widetilde{\mathcal{I}}_j - \mathcal{I}_j\|_\diamond \le \eta_j$ for every possible choice. Then the joint distributions of all classical records, including abort flags and the final output, of the two procedures differ by at most $\sum_{j=1}^N \eta_j$ in total variation distance.
\end{lemma}

\begin{proof}
Write the two procedures as compositions $\Phi_N\circ\cdots\circ\Phi_1$ and $\widetilde\Phi_N\circ\cdots\circ\widetilde\Phi_1$ of channels on the joint quantum--classical system, where each step first dephases the classical registers it reads and then applies the instrument selected by their values. A channel controlled by a dephased classical register is within the largest of its branch distances in diamond norm, so $\frac12\|\widetilde\Phi_j - \Phi_j\|_\diamond \le \eta_j$. Then
\[
  \widetilde\Phi_N\cdots\widetilde\Phi_1 - \Phi_N\cdots\Phi_1 = \sum_{j=1}^N \widetilde\Phi_N\cdots\widetilde\Phi_{j+1}\,(\widetilde\Phi_j - \Phi_j)\,\Phi_{j-1}\cdots\Phi_1 ,
\]
and channels do not increase the trace norm. Measuring the classical registers is a channel, and on diagonal states the trace distance equals the total variation distance.
\end{proof}
```

### P5. Explicit count in Theorem 1.2

Target: immediately after Theorem~\ref{thm:main}.

```latex
Explicitly, with Schedule~1 the procedure makes at most
\[
  c\,\bigl(m + \lceil\log_p(3/\eps)\rceil\bigr)\prod_{d=2}^{c} B_d(g_d)
  \;\le\; C_c\, c\,\bigl(m+\lceil\log_p(3/\eps)\rceil\bigr)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil}
\]
oracle queries (or that many copies of $\rho_H$), where $C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}$ depends only on $c$. The running time is polynomial in this count and in $m$, $\log p$, the label width and $\log(1/\eps)$. The exponent of $m$ grows like $c^2\log c$, so the bound is polynomial for each fixed $c$ and is not uniform in $c$.
```

(Check: B_d(g_d) = [d^{d(d−1)/2}(g_d+1)^d]^{⌈log₂(d+1)⌉} ≤ d^{d(d−1)⌈·⌉/2}(m+1)^{d⌈·⌉}, because g_d ≤ m.)

### P6. Proof assembly for Theorem 1.2

Target: the end of §3.2 (after the error bullets and P4).

```latex
\paragraph{Proof of Theorem~\ref{thm:main}.}
By Lemma~\ref{lem:homogeneous}, or Lemma~\ref{lem:copy-lift} for coset-copy input, each lifted source is exactly $\rho_{\exp(\hlift)}$ on $\widetilde G = G_c$, at the cost of $c$ queries or copies. Fix $d \in \{c,\dots,2\}$ and suppose the stage-$d$ inputs are independent copies of $\rho_{H_d}$, where $H_d = \exp\bigl(\bigoplus_{k\le d}t^k(\hh\cap\gamma_k(\mathcal{L}))\bigr) \le G_d$. The dilations $\delta_s$, $s \in \Fp^\times$, preserve $H_d$ and act on the central subgroup $Z_d$ by $s^d$. Apply the complete central instrument to $M_d = B_d(g_d)$ inputs. Schedule~1 returns a nonzero witness of~\eqref{eq:sde-target} for every label tuple, deterministically. By Proposition~\ref{prop:descent} the output is exactly $\rho_{H_dZ_d/Z_d} = \rho_{H_{d-1}}$ for every label tuple, so the outputs of disjoint input blocks are independent. Induction from $d = c$ down to $d = 2$ gives independent exact copies of $\rho_{t\hh}$ on the additive group $t\mathcal{L} \cong \Fp^m$, each made from $\prod_{d=2}^c M_d$ lifted sources. Fourier sampling on $m + \lceil\log_p(3/\eps)\rceil$ of them gives independent uniform elements of $\hh^\perp$, which span $\hh^\perp$ except with probability at most $\eps/3$, and a nullspace computation returns $\hh$. All of this is exact for ideal instruments. Implementing each of the $N_{\mathrm{instr}}$ instruments to error $\eps/(3N_{\mathrm{instr}})$ (Theorem~\ref{thm:uniform-compilation}) changes the output distribution by at most $\eps/3$, by Lemma~\ref{lem:hybrid}. So the total error is at most $2\eps/3$. The query count is the one displayed after Theorem~\ref{thm:main}, and each step runs in time polynomial in its input size.
\hfill$\square$
```

### P7. Public bound in Theorem 3.7

Target: Thm~\ref{thm:random-column}, first sentence. Replace "Choose an integer $u \ge 2$ with
$c \le u$ and $a_d \le u-1$ for every $d$, and suppose $p \ge 16u^2$." with:

```latex
Choose an integer $u \ge 2$ with $c \le u$, and suppose that a public bound $a_d \le u-1$ holds for every $d$ (for example $g_d \le u-1$, or a promise on $\codim\hh$ as in Corollary~\ref{cor:codim}), and that $p \ge 16u^2$. A node whose observed label rank exceeds $u-1$ aborts.
```

Table~\ref{tab:main-regimes}, random-column row, prime-condition cell: replace
`$p \ge 16u^2$, $u \ge c$, $u > \max_d a_d$` with
`$p \ge 16u^2$, $u \ge c$, public bound $u > \max_d a_d$`.

### P8. The IS17 Theorem 3 sentence

Target: §3.3 Schedule 1, replacing "The threshold printed in its Theorem~3 has $(a+1)$-exponent
$d\log d$, … We therefore use the proof's count~\eqref{eq:is-arity}."

```latex
Its proof closes with the chain $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil} \le d^{d^2\log d}(a+1)^{d\log d}$, and Theorem~3 prints the last bound. The second inequality fails for every $d \ge 2$ once $a$ is large, because $d\lceil\log_2(d+1)\rceil > d\log_2 d$; for $d = 2$ the exponents of $a+1$ are $4$ and $2$. The first inequality is what the proof gives, and we use it as~\eqref{eq:is-arity}.
```

Also at l. 178, append to "the fixed-degree diagonal-equation algorithm of Ivanyos and
Santha~\cite{IvanyosSantha2015}": ", which itself uses van de Woestijne's deterministic solver
for a single diagonal equation".
