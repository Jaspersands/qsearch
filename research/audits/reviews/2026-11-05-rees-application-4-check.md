# Adversarial check of the Rees application-4 report (Theorem W)

2026-11-05. Claude Code checker, AI only, not human review. Object:
`2026-11-05-rees-application-4.md` as revised after its own referee (§11),
which was not re-checked before this pass. Code:
`2026-11-05-rees-application-4-check/`. Claim gates `speedup_claim_allowed`
and `novelty_established` stay false. Result: **possibly known, NEEDS HUMAN
VERIFICATION.** No speedup or novelty claim.

## 0. Verdict

**No Error survives.** I found two Gaps and five Imprecisions. All are fixed
in the integrated text. The report file itself was not edited; this file
records the corrections.

- Theorem W(a) is **correct** once the class hypothesis is stated properly
  (G1). I checked it line by line (§1). My own implementation agrees with
  exhaustive search in **17 of 17** fresh cases inside the hypothesis, at
  p = 5, 7, 11 and 13. In every case δ̂ is the largest value the guard
  allows (the boundary), and in five H is non-normal and does not contain
  [G,G].
- Outside the hypothesis the method fails on exact instances. At p = 5 it
  under-reports twice and over-reports twice. The guard is not necessary,
  though: on the weight-p Nakajima norm, W is still correct (§3).
- W(b) is correct given the Luks import. The import is the one `main.tex`
  already uses in `rem:filters`(0), and it stays NEEDS HUMAN VERIFICATION
  (§2).
- The S1 residual matches the complement of what is proved in §3 of the
  report. §0 and §7 drop the open branch "D fixed, p superpolynomial" (I3).
- Integrated: a corrected §9 paragraph in `main.tex`, one pointer sentence
  in `core/main-core.tex`, item 9 of `REES_FULL_CONTINUATION.md`, and log row
  I214. No new bib entries were needed. Both builds are clean.

## 1. Theorem W(a), line by line

Notation as in the report: E = F_{p^K} with p^K > Δ, N = DK, u ∈ F_p^N,
z(u) ∈ E^D, and R_F(u) = Σ c_α Π λ_{i,e}(u)^{α_{i,e}}.

- **§2.1, class claim. GAP (G1).** The claim "ν ≤ p, so L has class
  ≤ ν−1" is false. Take left multiplication by Λ^{≥1}(F_p^2) on Λ(F_p^2),
  which is strictly upper triangular in the basis (e1e2, e1, e2, 1). Every
  element squares to 0, so ν = 2. But [e1, e2] = 2e1e2 ≠ 0, so the class is
  2 (`class_vs_nu.py`, p = 5, 7, 11, 13). The proof uses class < p only to
  know that G = exp(L) is a group with unique logarithms, and in Step 7
  (Lazard for log H). In S1, D ≤ p gives class ≤ D−1 < p, so §0 is
  unaffected. **Fix:** assume D ≤ p, or class(L) < p together with ν ≤ p.
  The integrated text assumes G ≤ UT_D(F_p) with D ≤ p. W itself does not
  need ν ≥ class+1: the exterior algebra case is inside the corrected
  hypothesis, and W matches brute force there (`p7-exterior-in`,
  `s2-p7-exterior-in`).
- **Step 0.** ρ is an injective F_p-algebra map, so ρ(exp A) = exp ρ(A).
  This uses ν ≤ p only for the factorials. OK.
- **Step 1 (Weil restriction).** z_i^{p^e} = λ_{i,e}(u) because u ∈ F_p^N.
  So z_i^{α_i} = Π_e λ_{i,e}^{α_{i,e}}, and deg R_F ≤ Σ_{i,e} α_{i,e} = δ(F).
  This is where the digit sum controls the degree. Lucas' theorem in its
  Frobenius form says t^n = t^{s_p(n)} for t ∈ F_p, and that is the
  one-variable shadow of this step. The bound does **not** say that
  t ↦ F(exp(tA)z) has small degree over E. That degree can be (ν−1)Δ. The
  bound holds for P_A(t,u) = R_F(exp(tρA)u), which agrees with
  F(exp(tA)z(u)) for t ∈ F_p. OK.
- **Step 2.** A polynomial of degree < p vanishing on F_p^N is zero. OK.
- **Step 3.** First, |E| > Δ, so formal identity is the same as identity on
  E^D. Second, that is the same as identity on F_p^N after z, by bijectivity.
  Third, both sides are reduced since δ < p. OK.
- **Step 4.** deg_t exp(tρA) ≤ ν−1, so deg_t P_A ≤ (ν−1)δ < p.
  - (⇒) exp(tA) = exp(A)^t for t ∈ F_p. I checked the truncated identity
    for n < ν ≤ p. P_A − R_F has t-degree < p and p roots, so it is 0.
  - (⇐) d/dt exp(tM) = M exp(tM) formally, because M^ν = 0. So
    ∂_t P_A = R_A(exp(tρA)u) = 0. A polynomial of degree < p with zero
    derivative is constant.

  Both directions are correct. This is the exact point where
  p > (ν−1)δ̂ is used: once in each direction.
- **Step 5 (interpolation).** r(σ) = R_F(u + σρ(A)u) has degree ≤ δ̂. For
  σ ∈ F_p it equals F(z + σAz). The nodes 0..δ̂ are distinct since δ̂ < p.
  So r′(0) = R_A(u) exactly, and R_A is linear in A. OK. Each sample costs
  1 + dδ̂ evaluations, so the stated (δ̂+1)d is an upper bound. My count
  matches 1 + dδ̂ exactly, for example 861 = 123·(1 + 3·2).
- **Step 6 (sampling).** If A ∉ log H, then R_A ≠ 0 by Step 4(⇐) and has
  degree ≤ δ̂. Schwartz–Zippel over F_p ⊂ E gives
  Pr[R_A(u) ≠ 0] ≥ 1 − δ̂/p > 1/2, using p > 2δ̂. For the Chernoff bound I
  checked (d+8L)² ≥ 8L(d+4L), so the failure probability is ≤ ε². OK.
  **Imprecision (I1):** T should be ⌈4d + 16 ln(1/ε)⌉. My implementation
  runs the proof's T with ε = 10⁻³, which gives T = 119–127. The report's
  own scripts used d+6 samples.
- **Step 7.** log H is a subspace, and H = exp(log H) as a set. The Lazard
  subgroup correspondence (class < p) gives
  ⟨exp(basis)⟩ = exp(log H) = H. OK, under G1's hypothesis.
- **Evaluation count.** (4d + 16 ln 1/ε)·d·(δ̂+1), plus
  poly(d, K, D, δ̂, log p) arithmetic. Each evaluation runs the circuit over
  E. OK.
- **Remarks.** I checked the weight rules:
  - weight(fg) ≤ weight f + weight g, since s_p(a+b) ≤ s_p(a) + s_p(b);
  - Frobenius invariance;
  - weight(f^n) ≤ s_p(n)·weight f;
  - G-invariance of the weight.

  All are correct.
- **Addition (not in the report).** When p is polynomially bounded, the
  promise "known δ̂" can be dropped. Run W with
  δ̂_max = ⌊(p−1)/max(ν−1,2)⌋. That is correct for every F with
  δ(F) ≤ δ̂_max, at cost polynomial in p. This is used in the residual (§3)
  and in the LaTeX.

**§2.4 table.** Every weight I could check by inspection is right: Moore r,
Hermitian 2, Artin–Schreier and trace ≤ deg Q, linearized ≤ k, B(x, x^{p^k})
2. The orbit-product and Dickson rows are the referee's computations, and I
did not rerun them. **Imprecision (I2):** "covers Hermitian / Artin–Schreier"
holds only under the same p-guard with the weight read off the construction.
The integrated text says so.

**§2.5 and the code.** The counts in the `.out` files match the report:
14/14 inside, 0/14 for naive Lie, both wrong on the UT_4(F_5) cubic,
twisted |H| = 25, 49, 11³, 13³, orbit ranks 36, 75 and ≥ 600. For X1c,
`candidate_filters_p5.out` prints "≥ 42 (700 random orbit reps)" where the
table says "42". This is minor.

## 2. W(b) and the Luks import

The steps check out:
- simplex-grid unisolvence in characteristic > δ̂, via Newton binomials
  whose denominators are ≤ δ̂!;
- π(g)P = P∘ρ(g)^{−1} is a homomorphism;
- π is faithful, since its degree-1 part is the dual of ρ;
- Stab_{π(G)}(R_F) = π(H), by Step 3;
- the dimension K·C(N+δ̂, δ̂) is polynomial for fixed δ̂.

The import is a vector stabilizer in a matrix p-group over F_p, which is
exactly `rem:filters`(0) of `main.tex` (Luks 1992, Thm 3.2(5)). Earlier notes
describe Thm 3.2(5) as polynomial in the dimension, the field size and the
largest non-characteristic prime, and for a p-group that prime is absent.
**Stated correctly as an import. NEEDS HUMAN VERIFICATION** (item numbering
and full text, which is abstract-level only, as in the third pass).

## 3. Implementation and tests

`check_theorem_w.py` is my code, written without reading the report's
scripts beyond their docstrings. It differs from them as follows:
- **Planted F.** F = Q(x, x^p, x^{p²}) with three Frobenius levels. Q is
  invariant under exp(B) for a *random* B ∈ L, plus a random central element
  in set 1.
- **Conjugation.** L is conjugated by a random element of UT_D and handed
  to W through a random basis.
- **Access to F.** W calls only a black-box evaluator on E^D.
- **Ground truth.** It is exhaustive over G. Non-membership is certified by
  a witness point in GF(p⁴)^D. Membership is checked formally through Q,
  which is exact by injectivity of reduced Q ↦ Q(x, x^p, x^{p²}). This was
  cross-checked by direct substitution into F when Δ ≤ 40.
- **Degree check.** The interpolated degree of t ↦ F(exp(tA)z) on F_p is
  compared with (ν−1)δ.

Outputs are `check_theorem_w.out`, `check_theorem_w_set2.out`,
`failure_threshold.out` and `class_vs_nu.out`. All runs used nice and stayed
below 1 GB.

**Inside the hypothesis: 17/17 match.**
- Set 1, with the centre planted, 10 cases:
  - p = 5: n3, δ̂ = 2, the boundary 4 < 5; heis4, δ̂ = 1.
  - p = 7: L4 and heis4, δ̂ = 2, the boundary 6 < 7; the exterior algebra,
    ν = 2, δ̂ = 3.
  - p = 11: n3, δ̂ = 5, the boundary 10 < 11; heis4, δ̂ = 3, the boundary
    9 < 11; two UT_2 blocks, ν = 2 < D = 4, δ̂ = 5.
  - p = 13: heis4, δ̂ = 4, the boundary 12 < 13, with Δ = 676 and K = 3, plus
    a second instance with Δ = 52.
- Set 2, with no centre planted, 7 cases. H is non-normal and does not
  contain [G,G] in 5 of them, at p = 7, 11 and 13 (heis4, L4, the exterior
  algebra, and n3 with δ̂ = 6, the boundary 12 < 13).
- Naive Lie on F is wrong in almost every case, with dimension 0.
- The interpolated t-degree never exceeds (ν−1)δ.

The case labels and their records are in the `.out` files.

**Outside the hypothesis, the method can fail (negative controls).**
- `p5-heis4-{under,over}-out-{d3,l1}`: p = 5, ν = 4, δ = 3, so
  (ν−1)δ = 9 ≥ 5.
  - Under: exp(B) ∈ H but R_B ≠ 0, so W returns dimension 0 while |H| = 5.
  - Over: R_B = 0 but exp(B) ∉ H, so W returns dimension 1 while H = 1.
  - Both with Frobenius levels (Δ = 15) and without (Δ = 3).
- Nakajima norm x_0^p − x_0x_1^{p−1}: weight p, H = G of order p. This was
  meant as a δ ≥ p control, but W with δ̂ = p−1 is **correct** (dimension 1)
  at p = 5 and 7. The reason is that P_A has t-degree 1 and
  R_A = λ_{1,1} − λ_{1,0}^p. That polynomial is nonzero formally but
  vanishes on F_p^N, so sampling sees 0. So the hypothesis is sufficient,
  not necessary. The p = 5 controls above are the real failures.

**Where failure actually starts [computed, not a theorem].**
`failure_threshold.py` searches by exact linear algebra for Lie-test
witnesses on plain forms (F = Q, weight = degree).
- For heis4 (ν = 4), the first δ with a witness is 3, 5, 7 and 9 at
  p = 5, 7, 11 and 13. Each time this is the least δ with
  (ν−1)δ ≥ 2p−1.
- For n3 (ν = 3), no witness appears up to δ = p−1, where
  (ν−1)δ ≤ 2p−2.
- No witness was ever found inside the guard.

So the guard p > (ν−1)δ̂ is sufficient but, on these instances, not sharp.
The data suggest the obstruction starts near (ν−1)δ ≥ 2p−1. That is a
question for a human, not a claim. It does not change the residual.

## 4. The S1 residual against what is proved

What is proved or cited:
- W(a): known poly δ̂ with p > max((ν−1)δ̂, 2δ̂). By the addition in §1, a
  polynomially bounded p needs no promise.
- W(b): fixed δ̂ < p, given Luks.
- Brute force: D fixed and p polynomial.
- FIMSS (quantum): p bounded.

The complement is the following, and it matches §3 of the report:
- δ unbounded, and either max((ν−1)δ, 2δ) ≥ p, that is δ ≥ p/max(ν−1,2),
  or δ is not polynomially bounded, which forces p superpolynomial;
- and D unbounded or p superpolynomial;
- and p unbounded.

Corrections:
- **I3.** §0 item 2 and §7 ("D grows", "D and p growing") drop the branch
  D fixed with p superpolynomial, which §3 itself leaves open. They should
  read "D grows, or p is superpolynomial (open)". The LaTeX now states the
  D condition correctly.
- **I4.** §3 "p grows": FIMSS needs bounded derived length. That follows
  from the fixed class c of the Rees setting, not from bounded p.
- **I5.** §0 "When p is polynomially bounded, the first condition alone
  suffices" means that the condition reduces to δ ≥ p/max(ν−1,2). The
  wording is ambiguous.
- The remaining items, (R2) and the heuristic filters, are contract
  conditions, not complements of theorems. That is acceptable as stated.

**Lemma Z** is re-derived and correct, including S = HN with N normal and the
kernel of φ when N is central. Its negative half is argued, as the report
says.

## 5. What was integrated

- **`main.tex`.** A new paragraph sits directly after the application-3
  paragraph, before `\subsection{Classical Query Complexity…}`. It is the
  corrected §9 text:
  - D ≤ p and the definition of H are stated;
  - s_p is defined;
  - it states why the test is exact;
  - it states the evaluation count with ε;
  - the δ̂_max remark;
  - the Hermitian and Artin–Schreier coverage is conditional;
  - W(b) goes through `rem:filters`(0);
  - the negative-control sentence;
  - the fixed-D clause;
  - statuses (proved, proved given Luks, computed), "AI-checked, pending
    human review", "may be known", and a `% NEEDS HUMAN VERIFICATION`
    comment.

  The edit was one exact-string insertion with count 1, and the file was
  re-read immediately before. The backup is `app4check-backup/` in the
  session scratchpad.
- **`core/main-core.tex`.** One sentence in the Applications paragraph. It
  has no `\ref` to the companion and no `\UT` macro, which core lacks.
- **No bib changes.** Luks1992 is already present.
- **Builds** (scratch copies in `$TMPDIR/app4check-build`):
  - full paper: exit 0, 169 pp.;
  - core: exit 0, 27 pp.;
  - each has 0 Overfull, no undefined references or citations, and no
    "Float too large".
  - A rebuild after another agent's concurrent edits to `main.tex` (about
    20 changed lines elsewhere, e.g. near line 213) shows one "Float too
    large for page by 8.3pt" at input line 233, the regime table. That is
    not from this insertion at line 1224, which built cleanly on the
    earlier state, and I did not touch it.
- **Tests.** `tests/tools/test_rees_paper_numbers.py`: 2 passed.
  `make_numbers.py` not run.
- **Other files.** Item 9 of `REES_FULL_CONTINUATION.md` is updated, and
  log row I214 is added.

## 6. For a human

1. G1: confirm the corrected hypothesis (D ≤ p, or class < p).
2. Luks Thm 3.2(5): full text and numbering.
3. Priority. The algebraic degree s_p of power maps and Kayal-style Lie
   methods are classical, and the combination may be known.
4. Sharpness. Is the true failure threshold (ν−1)δ ≥ 2p−1, as in §3?
