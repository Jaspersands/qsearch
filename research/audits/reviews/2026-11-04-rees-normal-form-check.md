# Referee check: `lem:tb-howell-rounds` (removing the normal-form proviso)

4 November 2026. Independent AI referee pass, local only: no git, no network, no `.tex` file in the repository edited. **AI-checked, pending human review.**

Checked: `2026-11-04-rees-normal-form.md` and its `howell_check.py`, against `appendix-torsion-blackbox.tex` (`lem:tb-chart` Steps 0–6, `prop:tb-recursion`, `prop:tb-count-gates`, `lem:tb-kernel`, "Public module arithmetic", (M1)–(M3)) and `main.tex` (`thm:bb-envelope`, `thm:ring-to-field`).

## Verdict

**Integrate with these fixes.**

| Class | Count |
|---|---|
| Error | 0 |
| Gap | 1 |
| Imprecision | 7 |
| Style | 5 |

The mathematics is correct. The left-kernel fact (P3) is true over Z/p^e, and the proof is complete. The O(m^5) round cost, the b+1 round count, the O(ℓ^8) total and the exponent comparison all check out. The single Gap, G1, is inherited from the existing appendix. The lemma claims its cost "on every branch", but an erroneous chart can carry structure constants that do not define a Lie ring, and then the procedures' preconditions fail. A one-paragraph validity check fixes it at O(m^5). Two fixes are needed for the build to meet the proposal's own acceptance test: G1, and S1 (the lemma adds one Overfull box).

## Checks

### 1. The left-kernel fact (P3)

**Claim.** Let W ⊆ (Z/M)^{n+a} be the row span of the rows (α_i | e_i). Take any Howell sequence of W in the sense of (HF1)+(HF2) of Step 2. Then the rows whose pivot is beyond n have the form (0 | λ), and these λ generate Λ = {λ : Σλ_iα_i = 0}.

**Proof re-derived.**

* The map λ ↦ (Σλ_iα_i | λ) is injective with image W. So W ∩ (0 ⊕ (Z/M)^a) = 0 ⊕ Λ.
* Let w ∈ W vanish in the first n positions. Use the invariant of Step 2's correctness argument: at pivot j_t, w ∈ S_t. Then w_{j_t} = λ_t p^{a_t} = 0, so λ_t ≡ 0 mod p^{e−a_t}. The lift 0 is valid, and λ_t r_t ∈ S_{t+1} by (HF2). Hence w ∈ S_{t+1}.
* After the last pivot ≤ n, w lies in the span of the rows with pivot > n. By (HF1) those rows vanish before their pivot.

Only (HF1) and (HF2) are used: no reduced entries above pivots and no particular construction. **True, and the proof is complete.**

**Independent brute force.** The script is `2026-11-04-rees-normal-form-check/ref_check.py`. It shares no code with `howell_check.py` and was written from the lemma text. Seeds 1–9 pass. Each seed runs:

* **(P3) tests: 420 per seed.** 150 over Z/9, 150 over Z/8, 60 over Z/27 and 60 over Z/25. Each compares the computed kernel span with the full brute-force set {λ ∈ (Z/M)^a : λA = 0}.
  * The inputs include adversarial matrices: entries forced to multiples of p and p^{e−1}, pure prime powers, and dependent rows.
  * The Howell sequences are randomized, to test "(HF2) alone": random tie-breaks among minimal valuations, random lifts of every exact quotient (as the appendix allows), then random additions of later rows to earlier rows. The additions keep (HF1), (HF2) and the span but destroy reducedness.
  * (HF1) and (HF2) are checked by brute force on every sequence.
* **(P4): 240 Smith forms per seed.** For each it checks PCQ diagonal, Q·Q^{-1} = I and (row span C)·Q = ⊕p^{a_t}e_t by brute force.
* **Lie rings.** Nine mixed-exponent rings: Z/9 x+Z/9 y+Z/3 z with [x,y]=z; Z/27+Z/9+Z/3; Z/27 x+Z/9 y with [x,y]=3y; Z/25 x+Z/5 y with [x,y]=5x; Z/25+Z/25+Z/5; Z/8+Z/4+Z/2 and Z/8 x+Z/8 y with [x,y]=2y (p = 2, linear algebra only); Z/9+Z/3+Z/3; and a class-3 ring Z/9^3+Z/3.
  * Each ring is first checked for Jacobi and for well-definedness of its constants.
  * In ψ-coordinates the bracket uses randomly perturbed lifts, to test lift-independence.
* **RtF runs.** RtF runs with (N1)–(N6) against a truth oracle (94 runs per seed) and against a random wrong oracle (94 per seed). Every round checks the following by brute force:
  * (N1) S = K.
  * (N2): |S/K| = Πp^{d_i}·|K|; p^{d_i}u_i ∈ K; no nonzero Σt_iu_i (0 ≤ t_i < p^{d_i}) lies in K; y − σ(coord y) ∈ K for every y ∈ S; and the structure constants modulo K.
  * (N3): the tensor makes σ∘ι_M a Lie map modulo K, and |{y ∈ S : py ∈ K}| = p^{m_0}|K|.
  * (N5): K' = q^{-1}(U).
  * (N6): about 2000 idealizers in all, compared with the brute-force I_S(K').
  * The truth-oracle runs return H every time, within at most b calls and b+1 rounds. The wrong-oracle runs also stay within at most b calls and b+1 rounds.
* **Mutation tests.** The script detects broken variants. Dropping the (HF2) append makes the kernel test fail, for example on A = [[15,9],[9,21]] over Z/27. Dropping the p^{e−b_l} scaling in θ makes the idealizer test fail.
* **Why a Howell form and not an echelon form.** Over Z/9, the echelon form of (3 | 1) has no row in the λ-block, yet Λ = {0,3,6}. The appended row (0 | 3) is what fixes it.
* The proposal's own script passes seeds 1–3.

### 2. Costs per round, and the Step 2 count

* **Per-step counts.**
  * (N1) O(m^3).
  * (N2):
    * (P3) on a+β ≤ 2m rows of width ≤ 3m costs O(m^3).
    * (P4) on an (a+β)×a matrix costs O(m^3).
    * The m^2 brackets cost O(m^3) each, plus (P2) and λQ at O(m^2) each. That totals O(m^5).
  * (N4): m_0^2 brackets from the tensor at O(m^3) each, giving O(m^5) mod p.
  * (N5) O(m^3).
  * (N6):
    * The aγ ≤ m^2 brackets cost O(m^5).
    * θ costs O(m^3) to set up and O(m^4) on all the brackets.
    * (P3) on an a × γm matrix with q_0 = a costs O(a(γm+a)^2) = O(m^5).
  * **Confirmed: O(m^5) per round.** On random dense inputs the observed count of (P3) in (N6) grows more like m^4. The m^5 is an upper bound.
* **(N3).** The O(m^3) holds only if the socle tensor is read off the (N2) constants: p^{d_i+d_j−2}c_{ij}^k mod p^{d_k}, divided by p^{d_k−1}. Computing (M3) "verbatim" by brackets costs O(m^5). Either way it is within O(m^5); see I1.
* **The Step 2 count.** The appendix's O((q_0+k)k^2) is **correct as written**, but loose. At most k vectors are appended, so at most q_0+k vectors are present at any position. The proposal's O(max(q_0,1)n^2) is also correct: each pivot removes one vector and appends at most one, and the script confirms the remaining set never exceeds q_0. This is a sharpening, not a correction.
* **Is the sharpening needed?** With the old count, (N6) costs O(m^6) and the total is ℓ^9. That is still below every τ_c, both as stated and under the 17/2 variant for c ≥ 2, since then τ_c ≥ 9. It would matter only at c = 1 under the unconfirmed 17/2 bound. There the ring is abelian, so (N6) is trivial anyway. The sharpening is convenient but not load-bearing; see I5.

### 3. Round count

* `prop:tb-recursion` gives at most b calls on every branch.
* Every pass through step 1 either stops or makes a call. So the number of passes is at most the number of calls plus one, which is at most b+1.
* A round that stops at stop rule 1 costs only (N1). A round that stops at stop rule 2 costs (N1)–(N4).
* So O((b+1)m^5) is right. The appendix's "at most b ≤ B rounds" in the Cost paragraph is off by one, as 3.4(b) says, and immaterial for poly(B).
* With b = n'_p and m ≤ n'_p: (b+1)m^5 ≤ 2n'^6_p.

### 4. Coverage

* **What the proviso covered.** Only the public arithmetic of RtF: the stop-rule tests, (M1) with section, coordinates and structure constants, (M3) with the matrix of σ∘ι_M, the closure test of U, K' = q^{-1}(U), (M2) at every round, and the output. (N1)–(N6) and "Output" cover all of these.
* **The initial Howell sequence** of ψ(L) is the rows p^{e−e_i}e_i, at O(m).
* **Other time terms.** No other term of (d) depends on the proviso.
  * `lem:tb-kernel`'s normal-form arithmetic is not charged on route (R2); the table row for (R2) kernel lists none.
  * The chart, the solvers, the certificates and the rest of Sylow are explicit.
* **Small unitemized terms.** Three classical terms are not itemized anywhere. None was ever under the proviso. They are listed in I7 and do not block integration.
* **Erroneous branches.** "On every branch" is not covered on branches with an erroneous chart; see G1.

### 5. Exponents

* τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2) ≥ 23/2 > 8 for every c.
* **c ≥ 3:** τ_c ≥ E_W(c)+4 ≥ 15.
* **c = 2:** τ_2 ≥ 23/2.
* **c = 1:** τ_1 = 23/2. The ring is abelian, p = 2 is allowed, and Z/2^e changes nothing in (N1)–(N6).
* **The 17/2 AKS variant:** τ_c ≥ E_W(c)+4 ≥ 9 for c ≥ 2, and τ_1 = 17/2 > 8.
* The bound O(Σ_p n'^6_p (b_M+1)^2) ≤ O(ℓ^2(Σ_p n'_p)^6) ≤ O(ℓ^8) is correct.
  * b_M ≤ ℓ because the computed M = max_i p^{α_i} divides an exact order o_i ≤ 2^ℓ.
  * Σ n'_p ≤ ℓ/log_2(c+1) holds by the size checks.
  * The bound has no s-, w- or ε-dependence, and ℓ ≤ N.
* Removing the proviso removes it from all three clauses (c ≥ 3, c = 2, c = 1), which is right: it governed all three.

### 6. Drop-in LaTeX

* **Occurrences.** In the current files:
  * Each of the six "Replace" strings occurs exactly once: 3.2(a), (b), (d), (e) and 3.3(a), (b).
  * Each anchor occurs exactly once: the insertion point, "We use three instances.", "at most $b \le B$ rounds", the `lem:tb-kernel` phrase, the attribution sentence, and both AKS comment blocks.
  * None of the new strings is present already, and the label `lem:tb-howell-rounds` is new.
* **Build.** I applied 3.1–3.4 to a copy in the scratchpad, not to the repository, and ran `latexmk -pdf`.
  * Exit 0, 146 pages (was 144).
  * 0 undefined references, 0 errors.
  * **1 new Overfull box** (27 pt) in the lemma's first line; see S1. With the S1 fix applied the build has 0 Overfull boxes.
* **Consistency.** The result is consistent. The new item (d), the proof of (d), the exponent paragraph and `thm:bb-envelope`(iii) all say O(ℓ^8), ⊆ N^8 < 23/2. The AKS comments are updated in both files.

## Findings

### Gap

**G1. "On every branch" presupposes a valid Lie ring, which an erroneous chart need not be.**

*The claim.* The lemma and the paragraph after it claim the O((b+1)m^5) cost on every branch. Its procedures assume that L is in the setting of `app:tb-ring`:

* the constants are well defined: p^{e_i}c_{ij}^k ≡ 0 mod p^{e_k};
* the bracket is alternating;
* Jacobi holds.

On the failure event of `lem:tb-kernel`, the rows of Y span a proper subgroup of (ker π)^⊥. Then ker Y can fail to be an ideal, and the constants that `lem:tb-chart` computes need not define a Lie ring.

*Example.* Take F = F_{2,2} over Z/9, G = (F,∗) and ker π = 0. Samples spanning {(a,3b,c)} give a chart with ε_1, ε_2, ε_3 of orders 9, 3, 9 and [ε_1,ε_2] = ε_3. Then 3c_{12}^3 = 3 ≢ 0 mod 9.

* This branch has positive probability: all k samples lie in an index-3 subgroup with probability 3^{−k}.
* It passes both size checks: n' = 5 < 6.
* On this chart, 2 of 400 random-oracle runs of RtF broke the invariant K ⊆ S. Since K' ⊄ I_S(K'), (N1)'s premise and the meaning of (N2) fail.
* On other ill-defined constants, (N2)'s membership test for [u_i,u_j] rejects, so the coordinates are undefined.
* The script is `2026-11-04-rees-normal-form-check/bad_chart.py`.

*Scope.* The call and round counts survive, because |K| ≤ p^b still grows strictly. But the procedures are not defined as written.

*Pre-existing.* The issue predates the proposal. `prop:tb-recursion`'s well-definedness argument and `lem:tb-count-prime`'s erroneous-chart clause have the same dependence. The new lemma makes the claim explicit.

*Fix.* Add after the lemma, at the start of the paragraph "On the chart of route (R2) …":

```latex
Before the recursion the algorithm checks that the computed constants define a Lie ring on
$\bigoplus_i(\mathbb{Z}/p^{e_i})\varepsilon_i$: $c_{ii}^k \equiv 0$,
$c_{ij}^k + c_{ji}^k \equiv 0$ and $p^{e_i}c_{ij}^k \equiv 0 \pmod{p^{e_k}}$ for all $i,j,k$, and
the Jacobi identity on the $m^3$ triples of basis vectors, at $O(m^5)$ ring operations; if a
check fails it stops and reports failure. On the success event of Lemma~\ref{lem:tb-kernel} the
chart is a Lie ring (Step~1 of the proof of Lemma~\ref{lem:tb-chart}), so the check never fires
there and the error split is unchanged; on every branch that reaches the recursion,
$\mathcal{L}$ is then a Lie ring as in Section~\ref{app:tb-ring}, which is all that the lemma and
the call count of Proposition~\ref{prop:tb-recursion} use (the class bound enters only the
correctness of the calls, whose running time the time-out bounds).
```

*Why this suffices.* Alternation plus well-definedness gives an alternating bilinear map on ⊕Z/p^{e_i}, and Jacobi on basis triples suffices by trilinearity. Each triple costs O(m^2) from the constants. The check is dominated by the O(n'^6_p) already charged.

### Imprecision

**I1. (N3) cost.** "(M3) applies verbatim … at O(m^3)" is true only if the tensor is read from the (N2) structure constants. Reword:

> (M3) with a_i = d_i: the coordinate of [p^{d_i−1}u_i, p^{d_j−1}u_j] on u_k is p^{d_i+d_j−2}c_{ij}^k mod p^{d_k}, so the tensor costs O(m^3) from the constants of (N2).

**I2. (N4) adds a rule to RtF.** "A call that returns more than m_0 vectors is treated as a stopped call" is a new rule in step 2 of the algorithm, yet the lemma says `prop:tb-recursion` "holds unchanged". The claims do hold, since a correct call returns at most m_0 vectors. Fix: add the clause to step 2 of Algorithm RtF ("a stopped call, or one returning more than dim Ω vectors, counts as returning nothing"), or say in the lemma statement that the algorithm is used with this rule.

**I3. Ambiguous reference.** "b_e = ⌈log_2(M+1)⌉ … as in the proof of part (i)". The lemma's setting is `app:tb-ring`, whose subsections are "Part (i): the socle" and so on, so "part (i)" reads as `thm:ring-to-field`(i). Write "as in the proof of Proposition~\ref{prop:black-box}(i)". The S1 fix below already does.

**I4. Notation clashes inside the lemma.**

* M = p^e is the modulus, but in the same algorithm M = S/K is the section, and ι_M and σ∘ι_M appear in (N3).
* b_l (the exponents of K') clashes with b = Σe_i and b_e.
* a is the number of S-rows, a generic row count in (P3)–(P4), and a_t the valuations.
* k_j (rows of K) and n (the generic width) clash with k and n of `lem:tb-chart`.

Fix: write the modulus as p^e (or a new symbol) throughout the lemma and keep M for the section, as the surrounding text does. Rename b_l to, say, a'_l.

**I5. "This sharpening matters".** This is overstated, both in the proposal §2.2 and in the closing LaTeX parenthetical. As shown under check 2, ℓ^9 would also be dominated in every stated case. The only exception is c = 1 under the unconfirmed 17/2 bound, where (N6) is trivial. Also state, as above, that the appendix's O((q_0+k)k^2) is a valid bound and not an error.

**I6. Text that goes stale on integration.**

* The appendix table `tab:tb-steps`, row "(R2): recursion", says "poly(ℓ, log p) public arithmetic". Suggest "O(n_p^6 b_M^2) bit operations of public arithmetic (Lemma tb-howell-rounds)".
* The Cost paragraph of `prop:tb-recursion` still says the output is "returned by its Hermite basis". Add a pointer to the lemma there, as 3.4(a) does for "Public module arithmetic".
* `docs/papers/rees-hsp/README.md` (4 November update) says the total time "assumes that the normal-form arithmetic of the normalizer steps stays within that exponent".

**I7. Classical terms that remain unitemized.** These are pre-existing and outside the proviso. Removing the last stated proviso makes "every term of the time is at most N^{τ_c}" rest on these too. All are dominated, but none is itemized:

* the O_c(d+k^2) dictionary operations of `lem:tb-chart`;
* the classical work inside the core calls other than the solvers, which the proposal's §5 already flags;
* the push-forward of the output generators by Φ̄: at most n'_p chart elements, each up to n'_p(2b_M+A_c) multiplications, not counted in `thm:bb-envelope`(ii).

The gate "total time is now fully explicit" must stay false, for these reasons as well as for β̂_c. Suggested follow-up: one sentence in (d) and one in (ii).

### Style

**S1. The new lemma adds an Overfull box (27 pt).** It is in its first line: the title plus the unbreakable inline `$\mathcal{L} = \bigoplus_{i=1}^m(\mathbb{Z}/p^{e_i})\varepsilon_i$`. That fails the proposal's own acceptance test of 0 Overfull boxes. The following replacement was tested in the copy and gives 0 Overfull boxes. It also fixes I3.

```latex
\begin{lemma}[Normalizer steps over $\mathbb{Z}/p^e$; AI-checked, pending human review]
\label{lem:tb-howell-rounds}
Let $\mathcal{L}$ be as in the setting of Section~\ref{app:tb-ring}, with basis
$\varepsilon_1,\dots,\varepsilon_m$ of additive orders $p^{e_1},\dots,p^{e_m}$ and integer
structure constants $c_{ij}^k$, and put $e = \max_i e_i$, $M = p^e$, $b = \sum_i e_i$ and
$b_e = \lceil\log_2(M+1)\rceil$ as in the proof of Proposition~\ref{prop:black-box}(i). The public
```

These lines replace the first five lines of the lemma, through "proof of part~(i). The public".

**S2. 3.3(c) reads awkwardly.** "by Proposition~…, with the normalizer arithmetic by Lemma~…, with no compilation hypothesis" has two "with" phrases. Prefer "by Proposition~\ref{prop:tb-count-gates} (the normalizer arithmetic by Lemma~\ref{lem:tb-howell-rounds}), with no compilation hypothesis:".

**S3. 3.3(a) could be misread.** In "… for the charts when log_2(8ℓ/ε) ≤ ℓ, O(ℓ^8) bit operations for the normalizer steps …" the condition can be read as applying to both terms. Add "(for every ε)" after the normalizer term.

**S4. 3.4(c) anchor.** The anchor "and $\poly(d,e\log p)$ public normal-form arithmetic" is split by a line break in the source, between "normal-form" and "arithmetic". It is unique, but a literal find-and-replace must match the newline.

**S5. Placement and redundancy.**

* The closing LaTeX parenthetical on O(ℓ^9) can be dropped from the paper; see I5.
* Consider giving the lemma its own `\paragraph{Normalizer arithmetic over $\mathbb{Z}/p^e$.}` lead-in. It is about RtF, but it sits inside "Proof of Proposition black-box(ii)".

## Gates that must stay false

* "Lemma tb-howell-rounds is human-checked."
* "Total time is fully explicit." β̂_c is uncomputed, and I7 lists further unitemized terms.
* "The normalizer term changes τ_c."
* "The counts hold on every branch without a chart-validity check." This one stays false until G1 is applied.

## Next step

1. Apply 3.1–3.4 with the G1 paragraph, the S1 replacement, and I1–I4 and S2–S3.
2. Rebuild.
3. Accept if the build has 0 undefined references and 0 Overfull boxes, and `tests/tools/test_rees_paper_numbers.py` passes.
4. Rerun `/opt/anaconda3/bin/python -I research/audits/reviews/2026-11-04-rees-normal-form-check/ref_check.py SEED` (seeds 1–9 pass in about 11 s each) and `bad_chart.py`.

## Applied (11-04)

Integrated locally into `docs/papers/rees-hsp/appendix-torsion-blackbox.tex`, `main.tex` (only `thm:bb-envelope` and its total-time paragraph and comment) and `README.md`. No git, no network, no commit. Backups: the scratchpad folder `bak-i183/`. `references.bib`, `research/reductions/rees_hsp_reduction.json`, `docs/outreach/` and the claim gates are unchanged, and `make_numbers.py` was not run. **AI-checked, pending human review.**

**Proposal sections.**

* 3.1 (the lemma): applied, with G1, S1 and I1–I5 below. It sits after the paragraph that follows `lem:tb-chart`, under a new `\paragraph{Normalizer arithmetic over $\mathbb{Z}/p^e$.}` (S5).
* 3.2(a)–(e): applied. (a) and (e) also carry the I7 additions.
* 3.3(a), (b) and (d): applied. (a) takes the S3 fix.
* 3.3(c): applied in its S2 form.
* 3.4(a): modified. The sentence is inserted *before* "We use three instances.", so that this sentence still leads straight into the list (M1)–(M3).
* 3.4(b): applied. The Cost paragraph says "at most b+1 ≤ B+1 rounds (each round makes one call, except a final round that stops at stop rule 1)" and gains a pointer to the lemma (I6).
* 3.4(c): applied, matched across the line break (S4).
* Citations: Howell (Linear and Multilinear Algebra, 1986) and Storjohann and Mulders (ESA 1998) are cited in running text in (P3), as context only, with no volume or pages. The text says nothing from them is used. Both are listed as suggested keys in the comment header. No `\cite` was added, so no bib entry was added.

**Findings.**

| Finding | Status | Note |
|---|---|---|
| G1 | applied, modified | The paragraph opens the text after the lemma, restricted to primes p > c with e_p > 1, before the recursion on the (R2) chart. Changed "a Lie ring as in Section app:tb-ring" to "a Lie ring of the form of Section app:tb-ring, possibly of class above c": on an erroneous branch the class bound can fail, and the lemma and the call count do not use it. The O(ℓ^8) sentence now reads "the check and the normalizer steps". |
| I1 | applied | (N3) now reads off the tensor as p^{d_i+d_j−2} c̄_ij^k mod p^{d_k} from the (N2) constants. These are named c̄_ij^k so they are not confused with the chart constants. |
| I2 | applied | The rule is added to step 2 of Algorithm RtF itself: "a stopped call, or one that returns more than dim Ω vectors, counts as returning nothing". (N4) cites step 2, so "holds unchanged" is literally true. |
| I3 | applied | Via S1: "as in the proof of Proposition black-box(i)". |
| I4 | applied | The lemma's modulus is written p^e throughout: ring operations modulo p^e, ψ into (Z/p^e)^m, b_e = ⌈log_2(p^e+1)⌉. M is left for the section, as in ι_M. Renamed: b_l to a'_l; the S-row count a to μ; the generic width n to ν; the K and K' rows k_j, k'_l to κ_j, κ'_l. Unit vectors are written 𝐞_i (`\mathbf`), to separate them from the exponents e_i. "M" is kept only outside the lemma, where it means exp G_p. |
| I5 | applied | (P1) says it "sharpens, but does not correct, the valid count O((q_0+k)k^2) of Step 2". The closing parenthetical now says the sharper count is not load-bearing: with the old count the total is O(ℓ^9), still below 23/2 ≤ τ_c. |
| I6 | applied | Table `tab:tb-steps`, row (R2) recursion, now reads "O(n_p^6 b_M^2) bit operations of public arithmetic (Lemma tb-howell-rounds)". The Cost paragraph points to the lemma. The README 4-November sentence no longer states the proviso. |
| I7 | applied, itemized | (d) gains an "\emph{Lower-order classical work}" passage in its proof. The statement adds "plus lower-order classical work, itemized in the proof, of O_c(N^{max(E_W(c)+4,6)+o(1)}) bit operations with N as below". The exponent paragraph bounds this term by max(E_W(c)+4, 6) ≤ τ_c. The three terms are listed below the table. *Caution:* the integrator derived the list in the second term from the proof of `thm:main`; no independent check has confirmed it is exhaustive. The gate "total time is fully explicit" stays false (β̂_c). |
| S1 | applied, modified | The S1 opening is used, but "M = p^e" is dropped (I4) and b_e is written ⌈log_2(p^e+1)⌉. The build has 0 Overfull boxes. |
| S2 | applied | |
| S3 | applied | "(for every ε)" follows the O(ℓ^8) term. |
| S4 | applied | The anchor is matched with its newline. |
| S5 | applied, modified | Paragraph lead-in added. The O(ℓ^9) parenthetical is kept, reworded as the I5 "not load-bearing" sentence, since the instruction asked for that point to be stated. |

The three I7 terms, as itemized in the proof of (d):

1. **Dictionary operations.** O_c(ℓ(s^c+Λ^2) log^2(s+2)) bit operations in all, on a balanced tree with O_c(log(s+2))-bit keys.
2. **Core-call classical work outside the solvers.**
   * The lower central series and the graded-cover constants: O_c(m^5) field operations.
   * The Bezout conversions and dilation constants: O_c(Q_f^call log p).
   * The final nullspace: O((m+t)m^2).
   * In all, O_c(Q_f ℓ^3 + ℓ^6 + ℓ^3(ℓ+t)) bit operations, plus N^{o(1)} per gate of (a) to write the gate lists.
3. **Push-forward by Φ̄.** At most min(d,n_p)^2(2b_M+A_c) multiplications per prime, O_c(ℓ^3) in all. This term is also stated in `thm:bb-envelope`(ii) and in the appendix proof of (ii).

**Verification.**

* Build in the scratchpad `build/` folder with `latexmk -g -pdf`: exit 0, 147 pages, 0 Overfull, no "Float too large", no undefined references or citations.
* `tests/tools/test_rees_paper_numbers.py`: 2 passed.
* `howell_check.py` seeds 1–5: all pass.
* `ref_check.py` seeds 1–9: all OK.
* `bad_chart.py` reproduces the G1 example: 3c_12^3 ≢ 0 mod 9, which the new Lie-ring check rejects.

**Gates that stay false.**

* "Lemma tb-howell-rounds is human-checked."
* "Total time is fully explicit."
* "The normalizer term changes τ_c."

**Not done.**

* The README page count still says 144 (now 147).
* `research/AGENT_HANDOFF.md`, `research/STATE.md` and the integration log were not updated.
