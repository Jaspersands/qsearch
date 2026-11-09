# Rees core paper: hostile STOC/QIP referee pass (9 Nov 2026)

AI-written (Claude Opus 5.5), pending human review. This is an attack on the integrated core
paper. It is not an endorsement, and nothing here promotes a claim gate.

**Object reviewed.** `research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/core/main-core.tex`,
with the pending paper pass applied (black-box corollary, citation fixes), plus `numbers.tex` and
`references.bib` in the same folder. 774 lines, read in full. Context: `research/STATE.md` "Now",
`research/TRAPS.md`, the prep `README.md`, and the sibling note `rees_r4_06_check_core.md`.

**Sources checked against local texts.**
- Ivanyos–Santha, arXiv:1503.09016v2 (`2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`):
  Theorem 3, Theorem 5, Proposition 7, Corollary 8, §3 (including Lemma 12 and Theorem 11), §3.3, §5.
- Imran–Ivanyos, arXiv:2304.08376v1 (same folder): Theorem 1, Proposition 3, §1, §6.
- Kothari–Metger–O'Donnell–Shutty–Wu, arXiv:2609.40321 (same folder): Problem 1.9 and Theorem 1.11.
- Ettinger–Høyer–Knill (`2026-11-02-rees-classical-lower-bound/refs/quant-ph_0401083.txt`):
  Theorems 1 and 2.
- Nayak (`refs/2104.14436.txt`): Corollary 4.2.
- Childs' lecture notes (`refs/childs_qa.txt`): Theorem 5.1 and eq. (10.10).
- FIMSS abstract (`audits/sources/legendre_prf/fimss_hidden_translation.txt`).

**Exact checks.** Scripts are in the session scratchpad (`ref/`), not in the repo. All runs used
`nice -n 19`, about 15 core-minutes in total. Results are in §3.

## 1. Verdict: MINOR revision (correctness); significance risk at STOC

I found **no counterexample or proof gap that breaks** Theorem `thm:main`, Corollary
`cor:black-box` or Proposition `prop:classical-query`. Every proof in the core was read line by
line, and the import `thm:is-import` matches the Ivanyos–Santha proof text (finding 1). The
findings below are accuracy, rigour-of-wording and presentation problems. Each has a concrete fix.

A hostile STOC PC would still attack **significance**, and revisions cannot fix that (finding 12).
The new ingredient is one interpolation lemma (`lem:homogeneous`). The descent is Ivanyos–Santha's
own degree-by-degree elimination. The query separation is not new (EHK). The time bound is
astronomically non-uniform in c (exponent 145 at c = 9). No application is known. For QIP, or for
a journal such as Quantum or TQC, the correctness case looks sound, but the novelty claim ("what
may be new is the use of the cover") still needs an expert prior-art check (§4, item 7).

## 2. Findings

Severity scale: MAJOR (the claim as stated is not supported), MINOR (needs a fix, the claim
survives), NIT (editorial).

### F1. `thm:is-import` against the source: **no gap**; two wording points (MINOR)

*Where:* Theorem `thm:is-import`, the paragraph after it, Remarks `rem:is-import` and
`rem:is-printed`.

*Check.* In IS v2:
- §3.2, Theorem 11 (p. 8) gives colliding representations from G(d,m) = d^{d(d−1)/2}(m+1)^d
  vectors when d | q−1. Lemma 12's recursion B_{ℓ+1} = d^ℓ(m+1)B_ℓ gives B_d = G(d,m).
- The sign identity (13) gives I = ∪_{a even} J_a ≠ ∅, since J_{(1..d)} ≠ ∅ and the identity is
  even.
- §3.3 iterates this: G^ℓ vectors give 2^ℓ representations with pairwise disjoint supports and
  explicit d-th-power coefficients. Fact 2 (van de Woestijne) is applied once 2^ℓ ≥ d+1, and the
  section ends with C(d,m) ≤ G(d,m)^{⌈log₂(d+1)⌉} ≤ d^{d² log d}(m+1)^{d log d}.

So B_d(a) = G(d,a)^{⌈log₂(d+1)⌉} is exactly what the proof establishes, and the paper's
`rem:is-printed` is right that the second inequality fails for d ≥ 2 (with log = log₂, ln or
log₁₀). The source supports three other points:
- The output scalars are explicit field elements (products of β_i, γ(k), z_i), so
  `rem:is-import`(a) holds.
- §3.1 is deterministic: Pohlig–Hellman in the π-part, at most log q restarts. Only
  Propositions 9 and 10 use randomness.
- The d ∤ q−1 reduction in §3 is the paper's Lemma `lem:bezout`.

Nontriviality also holds. IS's "we are done if this is the zero vector" step stops the iteration
whenever a common vector is zero. Every later representation therefore has a nonempty support, and
Fact 2's nonzero z gives a nonzero solution. I checked this step because a careless iteration
would allow empty supports.

*Wording points.*
- (a) IS's Theorem 3 *statement* says only "time polynomial in n and log q". Determinism comes from
  the prose ("the existence of a deterministic algorithm") and from the proof. The paper's import
  says "deterministic". **Fix:** add "(deterministic by the proof in §3; the statement of
  Theorem 3 does not say so)".
- (b) The paragraph after the theorem says that IS's last step solves z₁^d+…+z_{d+1}^d = 0 "by
  writing −1 as a sum of at most d d-th powers". That is a reformulation, not van de Woestijne's
  method. **Fix:** "(equivalently, by writing −1 as a sum of at most d d-th powers)".
- Also unverified: "the accepted journal version" (v2 equals the TCS 2017 version). The bib entry
  is TCS 2017; theorem numbering there was not checked. **Fix:** check it, or drop the claim and
  say "numbering of arXiv v2".

### F2. The abstract's motivating inference is a non sequitur as written (MINOR)

*Where:* abstract, sentence 2: "…needs automorphisms that preserve H and scale the centre, and
such automorphisms need not exist: the eight-dimensional class-three Dixmier–Lister algebra has no
positive grading over F_p for any p > 3". Intro item (1) has the same logic.

*Argument.* Having no positive grading rules out a *dilation family* (a torus). It does not by
itself rule out automorphisms that scale the centre, and the elimination needs automorphisms of
G, one per returned scalar s, that preserve H and scale Z by s^d. A semisimple automorphism of
order dividing p−1 gives a Z/(p−1)-grading, which `sec:dixmier-lister` does not exclude: its
argument uses the Z-grading derivation x_k ↦ k x_k.

The conclusion is very likely true for large p, by the following argument. All derivations are
nilpotent (the certificates), so the reduced identity component of Aut(L_DL) is unipotent and
acts trivially on Z. The scalars on Z then come from a finite component group, while
{s^3 : s ∈ F_p^×} grows with p. The paper does not state this argument. The computation I ran on this question (§3, item 3)
was inconclusive.

**Fix (any one):**
- (i) Weaken the abstract to "…needs a family of automorphisms of G that scale the centre and
  preserve H; for the Dixmier–Lister algebra no grading supplies one (it has no positive grading
  over F_p, p > 3)".
- (ii) Add the unipotence argument above as a remark.
- (iii) Add the exact computation as an exact-computation item.

### F3. Related work misattributes the mechanism of IS Corollary 8 (MINOR)

*Where:* `sec:related`, sentence 4: "Ivanyos and Santha [Cor. 8] remove the restriction on m when
the nilpotency class is constant, for the same hidden subgroups, by a reduction [Prop. 7] to a
hidden polynomial graph problem that Decker, Høyer, Ivanyos and Santha had solved for constant m
and degree."

*Argument.* In IS v2, Corollary 8 is Proposition 7 plus Corollary 6. Corollary 6 is IS's own
Theorem 5 (the §5 elimination of all degree-d terms at once) fed by Theorem 3. DHIS [9] solved
only constant m, so the sentence as written suggests that the reduction alone removes the
restriction. The paper later uses "the proof of Theorem 5, Section 5" correctly.

**Fix:** "…by a reduction [Prop. 7] to the hidden polynomial graph problem HPGP′, which they solve
for non-constant m [Thm. 5, Cor. 6] by extending the constant-m algorithm of DHIS with Theorem 3".

Related point. The parenthesis "(for p at most the class, [IS] uses [FIMSS])" is imprecise. IS §5
says "a solution for constant p is given in [10]", where [10] is Decker–Ivanyos–Santha–Wocjan
(SICOMP 2013), and that solution goes through FIMSS. IS then assume p > d. **Fix:** "for p at most
the class, IS use the constant-p algorithm of Decker, Ivanyos, Santha and Wocjan, which relies
on FIMSS". The DISW reference would have to be added to the bib.

### F4. The core cites a "full version" that is not public (MINOR for submission)

*Where:* `\fullv` is used 7 times: in the `cor:black-box` proof, `rem:black-box-scope` (×3), the
artifact remark, the `thm:uniform-compilation`(iii) proof and the Outlook. Appendix A, "Full
version" and "Number macros", gives `docs/papers/rees-hsp/main.tex` and `make_numbers.py`.

*Argument.* `.gitignore` line 17 makes `docs/papers/rees-hsp/` local-only, so a referee who follows
the pointer finds nothing. No core proof depends on it; I checked each use. The one near-dependence
is `thm:uniform-compilation`(iii): it rests on an unverified Kitaev locator, with the full version
as the fallback.

**Fix:**
- Release the full version (arXiv companion) before submission, or remove `\fullv` from all proof
  text.
- For (iii), cite a standard approximate QFT over Z_N with a stated gate bound instead of relying
  on the Kitaev locator. Hales–Hallgren (FOCS 2000) and Mosca–Zalka (2004, exact QFT over Z_p
  with arbitrary one-qubit gates) are candidates; a human must check the exact statements.
- Make the appendix's repository paths point to public files only.

### F5. The gate item of `thm:main` leaves classical time unbounded in the statement (MINOR)

*Where:* `thm:main`(5): "Besides the queries, it uses classical operations and
poly_c(m, log p, w, log(1/ε)) gates…".

*Argument.* As written, the polynomial bound attaches to "gates" only. The informal statement
and the proof's "Running time" paragraph bound the classical work too (Schedule 1 runs in
poly(M_d, log p)), but the theorem does not.

**Fix:** "Besides the queries, it uses poly_c(m, log p, w, log(1/ε)) classical operations and
gates…".

### F6. The black-box scope remark's exponent test presumes the identity (NIT)

*Where:* `rem:black-box-scope`: "G has exponent p exactly when every g_i^p = 1 (O(s log p)
multiplications)".

*Argument.* The equivalence is right: class < p gives a regular p-group, so Ω₁ = {x : x^p = 1}.
But the oracle model supplies no encoding of 1, and the corollary's proof defines enc(1) as
g₁^p only under the promise. The 11-09 corollary referee (finding 9) gave the idempotent test,
but the integrated text dropped it.

**Fix:** "…every e_i = g_i^p satisfies e_i e_i = e_i and e_i = e_1 (O(s log p) multiplications)".
The idempotent test identifies 1 under unique encoding.

### F7. Corollary statement: "a bound polynomial in ℓ" also depends on ε (NIT)

*Where:* `cor:black-box`: "c(L+τ)∏B_d(L) … a bound polynomial in ℓ and independent of s".

*Argument.* τ = ⌈log_p(6/ε)⌉. **Fix:** "polynomial in ℓ and log(1/ε), and independent of s".

### F8. "One evaluation is not enough" is method-relative (NIT)

*Where:* abstract and §1.2.

*Argument.* Proposition `prop:single-evaluation` proves that the single pullback is not
dilation-invariant unless [G,G] ≤ H. It does not prove that no one-evaluation algorithm exists.

**Fix:** "a single evaluation does not give a dilation-invariant hidden subgroup".

### F9. Visible source comments and internal meta-text (MINOR for submission)

*Where:* LaTeX comments throughout. Examples: `% NEEDS HUMAN VERIFICATION` (×3), `% AI-checked
exactly…`, `% CicaloDeGraafVaughanLee2012: AI-read…`, and repository paths.

*Argument.* arXiv serves the .tex source, so every comment ships. Also:
- The author line ("Quantum Algorithm Search Project") is not a human author. STOC and QIP
  require accountable human authors and an AI-use disclosure.
- The `\date` still says 5 November 2026 although the corollary is from 9 November.

**Fix:**
- Strip comments in the submission copy.
- Add human authors with an AI-use statement.
- Update the date.
- Move the "AI-checked" status text into one disclosure paragraph.

### F10. Minor bibliographic consistency (NIT)

- The key `ImranIvanyos2023` has `year = 2024` (QIP journal). KMOSW cite it as [II24]. This is
  harmless but confusing.
- `rem:is-import`(e) and `rem:is-printed` cite `research/audits/reviews/2026-11-05-rees-is2015-second-reading.md`
  inside the paper. A submitted paper should not cite an internal file. **Fix:** move it to the
  disclosure.

### F11. Claims checked and found correct (no action)

Listed so that a human can see what was attacked.

**Cover and interpolation.**
- `thm:rees-cover`(i)–(iii): class equality, top grade central, E_s∘δ_θ = E_{θs}, and the
  Z[1/c!] specialization.
- `lem:homogeneous`: Vandermonde argument, needing p > c for distinct nonzero points; the second
  expression needs p − 1 ≥ c.
- `prop:single-evaluation`, and the F_3 Heisenberg example.

**Central descent.**
- `lem:instrument`. `lem:central`: the probability |K|/|Z|, ρ_λ, and the trace formula with the
  inversion g = (hz)^{-1}.
- `prop:descent`, entrywise. `rem:product-channel`, recomputed with SUM(|χ_a⟩|χ_b⟩) =
  |χ_{a−b}⟩|χ_b⟩.
- `lem:copy-lift`, with R_g R_h = R_{gh} and tr(ρ_H R_g) = 1_H(g).

**Solver.**
- `lem:bezout`, including the edge case u = 0, which forces κ = p−1.
- `rem:zero-sum`, including B_4(2) ≈ 3.65·10^16.

**Compilation and errors.**
- `thm:uniform-compilation`(i): recurrence, Bernoulli signs, bracket count.
- `thm:uniform-compilation`(ii): four evaluations, namely compute–copy–uncompute, then compute,
  subtract, uncompute.
- `thm:uniform-compilation`(iv): register bound.
- `lem:hybrid`, the canonical-subspace argument, and the inequality
  √(1−|⟨φ|φ′⟩|²) ≤ ‖φ−φ′‖.

**Main proof.**
- The N_QFT count, including N_d = ∏_{d′<d} M_{d′}.
- Error budget ε/3 + ε/3.
- Q_q and its explicit bound.

**Classical queries.**
- `lem:collision` (i) and (ii): the coupling, and the identical fresh labels before divergence.
- `prop:classical-query` (i)–(v), re-derived, including:
  - the two Chernoff cases of (v);
  - p^{k−1}(τ+1) ≥ k+τ;
  - (Q−s) − M/2 ≥ (Q−s)/2;
  - the Θ statement, via m ≤ 2p^{(m−1)/2}.

**Black-box corollary.**
- Witt dimension formula and the Lyndon basis.
- Kernel hiding and the hyperplane bound ε/8.
- 2dt transforms at η = ε/(16dt), giving ε/8.
- Both public checks, and the K′ ⊊ K branch: E′ = Φ∘ι′ is a surjective homomorphism, so the
  output still generates H.
- Chart isomorphism, since the projection along K commutes with φ.
- Worst-case query bound, and union bound 3ε/4.
- The inverse-BCH justification: weight-by-weight correction in the central factors γ_k/γ_{k+1}.
  The coefficients stay in Z[1/c!] by the same induction, so the denominator claim follows from
  the sketch itself as well as from the citation.
- (A)(a): N^p = 0 for n ≤ p, class and exponent, log/exp; (A)(a) for F_p ⋉ F_p^m: N^{c+1} = 0 by
  the block computation E_jE_k = E_jT̂ = 0 and T̂^c = 0.

**Related work.**
- Related-work claims on Imran–Ivanyos (Theorem 1 scope, black-box unique-encoding model,
  Proposition 3, §6 open problem, the "class greater than two" automorphism remark in §1),
  BCvD (as described by IS), KMOSW Theorem 1.11, EHK Theorems 1–2, Nayak Corollary 4.2 and
  Childs eq. (10.10): all match the local texts.
- Morales' families exclude the free 2-generator class-3 group: no abelian maximal subgroup, and
  ⟨exp x⟩⟨exp y⟩ has p² < p⁵ elements.

### F12. Significance (referee opinion, not a defect)

- The query separation is acknowledged as not new.
- There is no application, and no speedup is claimed.
- The exponent of m is about c² log c, polynomial only for fixed c.
- The input model is an explicit Lazard chart, or, via the corollary, black boxes of exponent p
  only.
- The technical core beyond IS is `lem:homogeneous` plus the observation that `prop:descent`
  works branch by branch.

A STOC referee could call this an "elegant but incremental extension of [IS15, Cor. 8] from
F_p ⋉ F_p^m with order-p complements to arbitrary H in arbitrary Lazard groups". The paper's
hedged novelty sentence is appropriate. Strengthening it needs an expert prior-art search
(§4, item 7). The best pitch, already in the text, is that the corollary answers part of the
Imran–Ivanyos §6 question for exponent-p black-box p-groups at every p > c, with bounded error.

## 3. Exact checks run (falsification only; TRAPS rule 7)

1. **Table `tab:query-crossover` and the c = 9 macros.** Recomputed independently:
   - log₂ Q_q = 9.00, 27.76, 33.19, 35.06 and 1572.66.
   - LB primes 443, 337 853, 92 107 and 997.
   - (v) thresholds 84.0, 119 670.9, 42 289.6 and 637.7 with 8ℓ → 15, and 85.9, 121 496.2,
     42 772.4 and 641.9 with 8ℓ exact.
   - Copies 81, 301, 407 and 644; 2^{174.72} and 2^{174.47}.
   - Exponent 1 + Σ_{d=2}^{9} d⌈log₂(d+1)⌉ = 145, which matches `\ReesClassNineQueryExp`.
   - Q_q ≤ C_c c (m+τ)(m+1)^{…} holds for every row.

   **All match.**
2. **Dixmier–Lister algebra (Sage, over Q, F_5, F_7, F_11).**
   - Jacobi holds.
   - Lower central dimensions are (8, 4, 2, 0); the centre has dimension 2.
   - The derivation system has 224 equations, rank 52 and solution space of dimension 12.
   - Every derivation maps L into span(e_5..e_8), and the basis and a generic derivation are
     nilpotent.

   **Matches `sec:dixmier-lister`.** This only confirms the bracket table *as printed*. That it is
   the table of Dixmier–Lister 1957 is not checked (§4, item 6).
3. **Automorphism scalars on Z(L_DL)** (finding F2). **INCONCLUSIVE.** Gröbner computations in
   26 variables on the ideal of automorphisms α with α|_{γ_3} = λ both hit their timeouts with
   no output:
   - elimination to λ over F_7, timeout 600 s;
   - unit-ideal tests at fixed λ ∈ {6, 2} over F_7 and λ = 5 over F_13, timeout 420 s.

   A side result (Sage, exact) shows why the cheap argument is not enough. The degree-0
   derivations of the associated graded algebra gr L_DL form a 4-dimensional Lie algebra with
   3-dimensional derived algebra. A generic element is semisimple with irrational eigenvalues
   over Q, so it is gl₂-like. Aut(gr L) therefore has a rank-2 torus, not only the dilations.
   The short argument "a semisimple lift of a dilation μ with μ, μ², μ³ distinct would give a
   positive grading" thus covers only part of the cases. The question stays UNKNOWN here. The
   fix in F2(i) does not need it.
4. **DL cover over F_5** (independent Python).
   - E_s for s = 0..4 and δ_θ for θ = 1..4 are group homomorphisms for BCH₃ on the 14-dimensional
     cover (300 random pairs).
   - For 120 random subalgebras h: {C : E_s(C) ∈ h, s = 1,2,3} = ⊕ t^k(h ∩ γ_k), with the same
     result at s = 1..4.
   - δ₂ preserves E₁^{-1}(h) exactly when γ₂ ⊆ h (16 positive cases).

   **0 failures** for `lem:homogeneous` and `prop:single-evaluation` on a non-gradable algebra.
5. **BCH recurrence of `thm:uniform-compilation`(i).** Over Q, on random strictly upper triangular
   (d+1)×(d+1) matrices, the recurrence equals log(e^X e^Y) for d = 2..6. The bracket counts are
   3, 12, 30, 60 and 105, equal to (d−1)d(d+1)/2.
6. **(A)(a) logarithm.** In UT₅(F₅), log(gh) = BCH₄(log g, log h) mod 5 for 200/200 random pairs,
   using the truncated matrix log.

## 4. What a human expert must still check

1. **IS15/17, §3.3 and Theorem 11 (load-bearing).** Confirm C(d,a) ≤ G(d,a)^{⌈log₂(d+1)⌉} and
   that the printed Theorem 3 bound does not follow from the proof. Confirm determinism, explicit
   scalars, and the zero-vector stop that ensures a nonzero output. Check the TCS 2017 numbering
   against arXiv v2. Ideally get confirmation from the authors; note the rule on naming private
   correspondence in the prep README §4.
2. **van de Woestijne Fact 2 locator** (ISSAC 2005 or thesis, "Section 6").
3. **ISS 2012, Theorem 2** (classical reduction for constant class to exponent p and |H| ≤ p). No
   local copy was checked here.
4. **The QFT compilation citation** (Kitaev 1995 §5, Theorem 2, eq. (25)), or a replacement
   standard reference (F4).
5. **Khukhro locators** (Lemma 10.7, §10.2, Example 10.24, Remark 9.17). Check the claim that the
   inverse-BCH words have exponents in Z[1/c!], for the corollary.
6. **The Dixmier–Lister table** against Dixmier–Lister 1957. Otherwise call it "a
   characteristically nilpotent algebra"; its properties are verified independently, so the
   theorem does not depend on the name.
7. **Prior art for the cover and interpolation trick** in HSP and hidden-shift work, and in group
   isomorphism (Lazard/Baer gradings), beyond the citation crawl of 2 November. A specialist
   search changes the novelty sentence most.
8. **The 2026 preprints with no local text checked here:** Morales 2026, Holt–Subramanian 2026,
   Boucher–Fouque–Shen 2026 (scope sentences only).
9. **The oracle model for black-box groups** (unitary on non-encodings, unique encoding, no
   inverse oracle) against Imran–Ivanyos's model, which includes the inverse of the
   state-creating oracle.
10. **Venue compliance:** authorship, AI disclosure, stripped source comments (F9), and a public
    full version (F4).

## 5. Scope of this pass

- No file was edited except this new report.
- No git command was run, no claim gate was touched, and no one was contacted.
- Compute: about 35 core-minutes at `nice -n 19`, most of it in the two timed-out Gröbner runs.
- Scripts and outputs are in the session scratchpad `ref/`: `table.py`, `dl.sage`,
  `dlaut.sage`, `dlfix.sage`, `grder.sage`, `dlcover.py` and `bch.py`. They are not part of the
  repo. Rerun them from there, or copy them in, if they are needed as artifacts.
- Every check in §3 is a finite falsification attempt. None is evidence for the general theorems.
