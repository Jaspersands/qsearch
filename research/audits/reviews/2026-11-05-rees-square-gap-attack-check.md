# Check and integration: square-gap attack (Theorems 1, 2, Proposition 3)

AI-only check (2026-11-05), pending human review. Input:
`2026-11-05-rees-square-gap-attack.md` (the "attack report") and its folder. Paper context read:
`appendix-schedule2.tex` (subsections `app:s2-contraction`, `app:s2-weil`, `app:s2-TA`,
`app:s2-local`, `app:s2-scope`), `main.tex` Remark `rem:two-level-threshold-size`,
TH3 §§0, 3 (`2026-11-03-rees-threshold-3.md`), TH9 Remark 5 and its check §3.
Own script: `2026-11-05-rees-square-gap-attack-check/sqg_check.py` (`.out`), written
separately (no code reused), about 1.5 s under `nice -n 19`. The attack report's two scripts
were also re-run; their outputs match the stored ones, apart from the last digits of round-off residues (~1e-13).

Only `docs/papers/rees-hsp/appendix-schedule2.tex` was edited. No git, no network,
`make_numbers.py` not run, `main.tex` and `core/main-core.tex` not touched.

## 0. Verdicts

| Result | Verdict | Main reason |
|---|---|---|
| Theorem 1 (explicit law) | **accept with rewording** | (i)-(iii) correct. It is the same law as TH3 §3 and BGP Prop. 26, not a new one. (iv) overstates: for the joint-moment brackets, condition (b) is not automatic. It needs the bracket-containment step (TH9 Remark 5, step 4). |
| Theorem 2 (Chebotarev) | **accept with rewording** | Correct. The proof can be shortened with `lem:app-s2-two-rows`, and the statement extended to rescaling by any λ ∈ F_p^×. The scope must say it restricts fixed algebraic data only and says nothing about E_2(κ). |
| Proposition 3 (4-cycle sums) | **accept** | Re-derived, and brute force over *every* admissible tuple matches. Do not identify these sums with the "2×2-block sums" of `rem:two-level-threshold-size`, which are TH4's stratified sums S^D_e. |
| (not in scope) (F2) "iff", Proposition 6 "exactly when" | **error noted** | P(all n_j > 0) = 0 does not imply p ∈ E_2(κ). Counterexample: κ = 4, p = 61. |

**Does Theorem 1 upgrade the argued κ^κ/2 barrier to a proved one?** In part. Precisely:

- **O1 and O2 in the text.** The barriers called O1 and O2 in the report are TH3 §2 and §3.
  - O1 is the `main.tex` sentence "Bounding the full character expansion ... term by term cannot certify any p ≤ 2^{-1/(κ-1)}κ^κ". It is not affected.
  - O2 is the `main.tex` sentence "If p ≤ κ^κ/2, no argument that averages over β and uses only statements about at most κ−1 of the column counts ..., each true when the columns are independent, can prove p ∉ E_2(κ) ... (BGP, Prop. 26)". It is also the last part of `rem:app-s2-joint-moments`, as specialised to the TH9 brackets.
- **Theorem 1 alone** proves O2 in its exact form, with no citation needed. Fix a set of statements, each about the joint law of at most κ−1 of the n_j and each true for independent copies of the true marginal 𝒩. If p ≤ κ^κ/2, the set does not imply P(all n_j > 0) > 0.
  - This was already proved in TH3 §3 (with the same law), but the paper cited BGP and called it "argued in the reports".
  - The word "argument" in the paper's sentence must be read as "a set of such statements, from which P(all n_j > 0) > 0 is to be deduced". "Every argument that averages over β" names no class of proofs.
- **The joint-moment barrier.** This is `rem:app-s2-joint-moments` and the `main.tex` sentence "It is also argued, and not proved here, that this method cannot push below κ^κ/2".
  - The brackets for |S| ≥ 2 are statements about several columns. Theorem 1 gives the law the independent-copy values of these moments.
  - That those values lie inside the brackets is a separate inequality: TH9 Remark 5, step 4. The attack report's (iv) passes over this. It lists "every joint factorial moment ... with m ≤ κ−2" among the facts of type (a)-(b), but (b) for a bracket *is* step 4.
  - Step 4 is elementary and has a complete proof in TH9 Remark 5. It is re-derived in TH9-check §3 and again below (§1.4), and now in the paper.
- **Status after integration.** Theorem 1 and step 4 together are now Proposition `prop:app-s2-barrier` of the appendix. So the κ^κ/2 barrier is **proved in the paper** (AI-checked, pending human review) for exactly this class: lower bounds for P(all n_j > 0) that are valid for every law on ℕ^κ satisfying
  - (a) any statements that each involve at most κ−1 of the n_j and hold for independent copies of 𝒩, and
  - (b) the two-sided brackets of `rem:app-s2-joint-moments`, for all S ⊆ ℤ_κ (including |S| = κ) and all m with η_m < 1,
  - with κ ≥ 3 and p ≤ κ^κ/2. (For κ = 2 there is no prime p ≡ 1 mod 2 with p ≤ 2.)
- **Still not covered (unchanged):**
  - the one-sided upper brackets with η_m ≥ 1 (the gap noted in TH9-check);
  - any use of all κ columns jointly in another way, for example E∏_j n_j, which is p^{1-κ} times the number of normalised contractions with every entry nonzero;
  - averaging over α or (α,β), and per-prime constructions;
  - "every β-averaging method" in general.

The square gap is **not** closed, and no threshold, table or number in the paper changes.

## 1. Theorem 1

### 1.1 The law

P(x) = q^{|x|}(1-q)^{κ-|x|} − (−1)^{κ-|x|} q^κ = I_q(x) − (−1)^κ q^κ W(x), where W(x) = (−1)^{|x|}.

- **Marginals.** Summing W over any coordinate gives 0. So W has total 0 and zero marginal on every proper set of coordinates, and P has the total and the proper marginals of I_q.
- **P(1,…,1) = 0.** At x = (1,…,1), P = q^κ − q^κ = 0.
- **Nonnegativity.** If κ−|x| is odd, P = I_q + q^κ > 0. If κ−|x| = 2r ≥ 2, P = q^{|x|}((1−q)^{2r} − q^{2r}) ≥ 0 exactly when q ≤ 1/2.
- **Converse.** Let f have zero marginal on each (κ−1)-set. Write f = Σ_T f̂(T) W_T. The marginal on the complement of {j} is 2Σ_{T∌j} f̂(T)W_T. So f̂(T) = 0 for every T ≠ [κ], and f = tW. Then P(all) = 0 forces t = −(−1)^κ q^κ. For q > 1/2, the atom with |x| = κ−2 has mass q^{κ−2}(1−2q) < 0.
- **Script check.** The kernel of the (κ−1)-marginal map was computed and has dimension 1 for κ = 2..8 (`sqg_check.out` T1).
- **Same law as TH3.** TH3's construction puts mass w_z/C(κ,z) on each x with |x| = z, where w_z = C(κ,z)q^z[(1−q)^{κ−z} − (−q)^{κ−z}]. That gives the same P. So the law is not new. The new item is the five-line Walsh proof, which is now in the paper (`lem:app-s2-kwise`). The BGP citation is kept for attribution.
- **Exact check.** In exact rationals, κ = 2..8 and q = 1/40..39/40, all of the following held, with 0 failures: total 1, P(all) = 0, every proper marginal correct, nonnegative iff q ≤ 1/2, and the (κ−2)-atom negative for q > 1/2.

### 1.2 Lifting to ℕ^κ (part iii)

Put n_j = B_j m_j, with B ~ P and the m_j i.i.d. from 𝒩(·|n>0), independent of B.

- On a proper set S of coordinates, the B_j are i.i.d. Bernoulli(q). So the n_j on S are i.i.d. with law (1−q)δ_0 + q𝒩(·|n>0) = 𝒩.
- All n_j > 0 forces B = (1,…,1), which has probability 0.
- The case q = 0 needs a point mass instead. It does not occur here, since q > 0 by the argument of Prop. 6.
- Every n_j has law 𝒩, because X_j(y) = ξ^{−j}X_0(ξ^j y). I checked this identity.

### 1.3 Part (iv) and the condition p ≤ κ^κ/2

q ≤ E n_0 = h^κ/p^{κ−1} = (p−1)^κ/(κ^κ p^{κ−1}) < p/κ^κ ≤ 1/2. Correct.

- **Rewording needed (1): the "iff" in (F2).** The report's (F2) says "p ∉ E_2(κ) iff some y has every X_j(y) ≠ ∅". Only "if" holds. A contraction with a zero cell gives no such y. At κ = 4, p = 61, TH3's exact joint law has P(all) = 0, but 61 ∉ E_2(4) (`app:s2-scope`: requiring nonzero entries enlarges E_2(4) by {61}).
  - The barrier itself is unaffected, because β-averaging certifies through P(all n_j > 0) > 0, which is the event the barrier is about.
  - The same error is in Proposition 6: "Pr_y[all n_j > 0] = 0 exactly when p ∈ E_2(κ)". Its conclusion, that there is no FKG-type inequality, survives, since E_2(κ) ⊆ {P(all) = 0}.
- **Rewording needed (2): the joint factorial moments in (iv).** See §0. Condition (b) for the brackets is step 4 (§1.4). It is not a consequence of Theorem 1.
- **Rewording needed (3): Remark (2), "κ^κ/2 is sharp ... which is why TH9's certificate can fire only above κ^κ/2".**
  - The inequality P(all) ≥ q^κ − min_x I_q(x) is true but weak. The exact bound is q^κ − q^{κ−d}(1−q)^d, with d the largest even number ≤ κ, which is the minimum over x with κ−|x| even.
  - "q > 1/2" is a statement about 𝒩, not about p. The "which is why" is heuristic. In the paper it is replaced by the plain converse plus "this does not show that any certificate works there".

### 1.4 Step 4 (bracket containment): re-derived here, now in the paper

Notation: E_κ(m,p) = c_m√p + d_m, with c_m = m(1−1/κ) − 1 + κ^{−m} and d_m = m/κ − mκ^{−m}.

- **Monotonicity.**
  - c_{m+1} − c_m = (1−1/κ)(1−κ^{−m}) ≥ 0.
  - d_{m+1} − d_m = 1/κ + κ^{−m−1}(m(κ−1) − 1) ≥ 0.
  - Hence η_m is nondecreasing, and η_1 = 0.
- **Only m ≤ κ−2 has η_m < 1.** η_{κ−1} ≥ κ^{κ−1}c_{κ−1}/√p ≥ √2 κ^{κ/2−1}(1−1/κ)² ≥ √2·√3·4/9 = 1.089 > 1 for p ≤ κ^κ/2 and κ ≥ 3. Numerically, the minimum over 3 ≤ κ ≤ 40 is 1.626, at κ = 3 (T1b').
- **Reduction by Vandermonde.** Each term of the Vandermonde expansion of C(M_S,m) involves at most m ≤ κ−2 coordinates. So the expectation under ℒ is Σ_comp Π_j e_{m_j}, and Σ_comp Π_j C(h,m_j) = C(rh,m).
- **Merge inequalities.** For a, b ≥ 1 with m' = a+b ≤ m:
  - c_{m'} − c_a − c_b = (1−κ^{−a})(1−κ^{−b});
  - d_{m'} − d_a − d_b = a(κ^{−a}−κ^{−m'}) + b(κ^{−b}−κ^{−m'}) ≥ 0;
  - hence η_a + η_b ≤ η_{m'}/κ;
  - ρ_aρ_b/ρ_{m'} = 1 + ab/(p(p−m'));
  - lower bound: (1−η_a)(1−η_b) ≥ 1 − η_{m'};
  - upper bound: (1+η_a)(1+η_b) ≤ 1 + 13η_{m'}/36.
  - The ρ excess is ab/(p(p−m')) ≤ η_{m'}·(9/16)m'²κ^{−m'}p^{−3/2} ≤ 0.0135η_{m'} for p ≥ 7. The paper says 0.02 and TH9 says 0.023; both are valid.
  - Total: (1 + 0.361η)(1 + 0.02η) ≤ 1 + 0.388η ≤ 1 + 0.4η.
- **Numerical checks.** 91 merge pairs (κ = 3..12, four p each near κ^κ/2, /16, /128, /1024) gave 0 failures. The largest (ratio−1)/η is 0.067, the same as TH9-check found.
- **Real instance.** κ = 4, p ∈ {101, 109, 113}: all three are ≤ 128 = 4^4/2, and η_2 < 1 at each. The exact law of n_0 was computed over all p³ values of y. The one-column brackets for a = 1, 2 hold for the true moments, and the m = 2 brackets hold for |S| = 1..4 under independent copies (T1b). (This is a mechanical check; it is not needed for the proof.)

## 2. Theorem 2

- **Meaning of "reduce to a contraction".**
  - Fix a number field K and a finite set 𝒞 ⊆ K^{2κ} of pairs (α,β). Take a prime 𝔭 of K above p, with O_K/𝔭 = F_p. The claim is about whether the reduced pair (ᾱ, β̄) satisfies the normal-form conditions of `lem:app-s2-normal`: α_j+β_i ∈ Q°_{−(i+j)} and α_0+β_0 ≠ 0.
  - The proof shows that every cell of the reduction lies in Q_0 ∪ {0}.
  - I extended the statement to λ times any row/column permutation, for any λ ∈ F_p^×. All cells then lie in a single coset Q_c ∪ {0}, and the argument is unchanged. Translations (α+c, β−c) change no cell. So the result is robust to the normal-form normalisations.
- **Proof check.**
  - Every cell u is integral at 𝔭 (no denominators).
  - If u ≠ 0 and v_𝔭(u) = 0, then w = u^{1/κ} ∈ L has v_𝔓(w) = v_𝔓(u)/κ = 0 (e = 1), and ū = w̄^κ ∈ Q_0.
  - Otherwise ū = 0.
  - The Latin-pattern argument is correct. A shorter route, now in the paper: row 0 needs cell (0,j) ∈ Q°_{−j}, and −j ≡ c for only one j. So κ−1 ≥ 2 cells of row 0 vanish, which gives two equal α'_j. `lem:app-s2-two-rows` forbids this, for any coset generator.
- **Brute-force check (T2).** At (κ,p) = (3,7), (3,13), (4,13), (4,17), (5,11), (6,13) (composite κ included), no single-coset configuration with a nonzero cell satisfies the pattern.
- **Edge cases.**
  - *κ = 3.* Works: κ−1 = 2 forced zeros.
  - *κ = 2.* Excluded rightly: only one forced zero, and the argument fails.
  - *Composite κ.* Nothing uses primality. Kummer theory only needs ζ_κ ∈ L, which holds by construction.
  - *p | κ.* Excluded automatically for κ ≥ 3. Such a p ramifies in Q(ζ_κ), except p = 2 with κ = 2κ', κ' ≥ 3 odd, where Q(ζ_κ) = Q(ζ_{κ'}) and 2 ≢ 1 mod κ' (added to the proof).
  - *Ramified primes.* They never split completely, so they are excluded.
  - *Primes dividing a denominator.* Excluded by hypothesis; there are finitely many.
  - *Primes dividing a cell.* They give zero cells, which the argument handles.
- **Density.**
  - Complete splitting in L is equivalent to complete splitting in the Galois closure L̃, which has density 1/[L̃:Q] (Chebotarev).
  - The report's Galois claim is correct when K is Galois and 𝒞 is Galois-stable: L is then the compositum of K(ζ_κ) and the splitting field of Π(X^κ − u) ∈ Q[X]. The degree bound [K:Q]φ(κ)κ^{|D|κ²} is also correct.
  - The "relative density φ(κ)/[L:Q]" needs [L̃:Q] in general. The paper says only "positive natural density".
- **Illustration figures.**
  - At 4·10^5, the fraction of primes with 2, 3, 5 all quartic residues is 0.0136 against 1/64 = 0.0156, about 2σ low. At 10^7 it is 0.01538 (5108 of 332180 primes), so the figures are consistent with Chebotarev.
  - p = 196681 is prime and ≡ 1 mod 8, and every u with 1 ≤ |u| ≤ 16 is a fourth power mod p (checked). This example is in the paper.
- **Scope rewording.** The paper says that the result:
  - covers constructions from finitely many fixed algebraic configurations, rescaled and permuted per prime;
  - fails at a positive-density set of primes;
  - does not put those primes in E_2(κ);
  - does not cover per-prime solving (Prop. `prop:app-s2-TW`).

  The report's "kills the Graham-Ringrose route" and the Paley comparison are left out of the paper. They are an uncited classical gloss, and the comparison was not checked against a source.

## 3. Proposition 3

- **(a) Degree-one row or column.** Summing over that β_i gives Σ_u χ^{e}(u) = 0 (convention χ^0 ≡ 1, χ^s(0) = 0).
- **(b) Σe ≢ 0.** Scaling by λ multiplies S_e by χ(λ)^{Σe}, which is ≠ 1 for a suitable λ.
- **(c) 4-cycle supports.** Re-derived:
  - For A ≠ B, the substitution b + A = (A−B)w gives χ^{e1+e2}(A−B)χ^{e2}(−1)J(χ^{e1},χ^{e2}).
  - The two powers of χ(A−B) multiply to χ^{Σe}(A−B) = 1.
  - The diagonal A = B gives Σ_{u≠0}χ^{e1+e2}(u).
  - J(χ^a, χ^{−a}) = −χ^a(−1).
  - Result: S_e = p^{2κ−3}(p−1)χ^{e2+e4}(−1)JJ, or p^{2κ−2}(p−1), and |S_e| = p^{2κ−2}(p−1) in both cases.
- **(d) Total.** At most C(κ,2)²(κ−1)³p^{2κ−1} = κ²(κ−1)^5 p^{2κ−1}/4 < κ^7 p^{2κ−1}/4.
- **Brute force (P3).** The four cycle variables, against the closed forms, for **every** admissible (e1..e4): (3,7): 6, (3,13): 6, (4,13): 21, (5,11): 52, (6,13): 105 tuples. The maximum error is 2.8·10^{−12}, with 0 modulus failures. The report's script stopped at 6 tuples per pair.
- **Caveat for the paper.** `rem:two-level-threshold-size` speaks of "2×2-block sums, each of size about p^{2κ−1}". Those are TH4's sums S^D_e on the distinct stratum, a different object. The appendix remark therefore says only "four-cycle sums of this expansion". The weight κ^{−z} for configurations with z zero cells is stated, since χ^0(0) = 1 gives 1/κ per zero cell.

## 4. What was integrated (`appendix-schedule2.tex`)

- **Tail of `rem:app-s2-joint-moments` rewritten.** The text from "The method cannot go much lower, granting one step argued in the reports" to the end now:
  - states the barrier for κ ≥ 3, p ≤ κ^κ/2;
  - points to the new proposition, "which proves this";
  - adds "restricts a class of proofs; does not bound E_2(κ), changes no threshold, does not close the square gap".
  - The text "this step is not proved here" and "granting it" is removed, because step 4 is now proved.
- **New block** after Table `tab:app-s2-thresholds`, before `\subsection{A tower ...}`. It starts with a status sentence citing the attack report and this check (AI-checked, pending human review) and saying that the square gap stays open.
  - `lem:app-s2-kwise`: the law P_θ, its converse, and the full Walsh proof. BGP Prop. 26 and TH3 §3 are cited for attribution.
  - `prop:app-s2-barrier`: the κ^κ/2 barrier, parts (i)-(iii) plus the "does not imply" consequence, with a full proof (Theorem 1 lift and step 4).
  - `rem:app-s2-barrier-scope`: what the result covers (one-column facts, Prop. TA's union bound, the central-moment bound; 6κ^κ+1 within about a factor 12) and what it does not (upper brackets with η_m ≥ 1, E∏n_j). It also states the q > 1/2 converse, with "does not show any certificate works there".
  - `prop:app-s2-chebotarev`: the proposition with full proof (two-rows shortcut, p | κ edge case, Chebotarev).
  - `rem:app-s2-chebotarev-scope`: the scope, and the 196681 example (finite computation).
  - `rem:app-s2-four-cycle`: Proposition 3, a labelled proof sketch, the brute-force note, and a `% NEEDS HUMAN VERIFICATION` comment for |J| = √p.
- **Not integrated.** Propositions 4-6 and Lemma 5 were not in scope. Proposition 6 needs the fix in §1.3 before any use.
- **LaTeX constraints.** No `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni` in the added text. A `\not\ni` was replaced by `j \notin T`. Only existing environments and macros are used.

## 5. Proposed `main.tex` update (NOT applied; for the parent)

Replace the sentence "It is also argued, and not proved here, that this method cannot push below
$\kappa^\kappa/2$, since below $\kappa^\kappa/2$ no lower bound valid for every law of the column
counts that satisfies the same Weil-controlled moment brackets is positive
(Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review)." by:

> This method cannot push below $\kappa^\kappa/2$: for $\kappa \ge 3$ and $p \le \kappa^\kappa/2$, an explicit law of the column counts agrees with independent copies on every $\kappa-1$ columns, satisfies the same Weil-controlled moment brackets and gives probability $0$ to every column being nonempty, so no lower bound valid for every law satisfying those brackets is positive (Proposition~\ref{prop:app-s2-barrier}; proved, AI-checked, pending human review).

Optional, same remark. The sentence "If $p \le \kappa^\kappa/2$, no argument that averages over $\beta$ and uses only statements about at most $\kappa-1$ of the column counts ..." sits under "The rest of this remark summarizes arguments made only in the cited reports, not proved here". It is now proved. After its BGP citation, add "; proved in Proposition~\ref{prop:app-s2-barrier}, AI-checked, pending human review". Optional, `core/main-core.tex`: "(... the reports also argue that the method behind it cannot go below $\kappa^\kappa/2$)" could become "(...; the full version proves that the method behind it cannot go below $\kappa^\kappa/2$)".

## 6. Build and test

- Built from a fresh copy of `docs/papers/rees-hsp/*.tex` and `references.bib` in `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build_sqg`, with `PATH=/Library/TeX/texbin:$PATH nice -n 19 latexmk -g -pdf -interaction=nonstopmode main.tex`.
  - Exit 0, 181 pages.
  - 0 Overfull, no undefined references or citations, no "Float too large", no multiply defined labels.
  - Two overfull lines from the first draft of the four-cycle remark were fixed.
- `/opt/anaconda3/bin/python -m pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed.

## 7. Claim gates that stay false

- The square gap is closed; a threshold o(κ^κ) is proved; 6κ^κ+1 is unconditional: **false**.
- The barrier covers every β-averaging argument, the upper brackets with η_m ≥ 1, or arguments using E∏_j n_j: **false**.
- Proposition `prop:app-s2-chebotarev` bounds E_2(κ), or covers per-prime constructions: **false**.
- Any number, threshold or table changed: **false**.
- Priority for the law (BGP/TH3) or for Chebotarev-type arguments: **not claimed**.

## 8. Proposed log row (for `2026-11-02-rees-integration-log.md`; NOT added)

> | I2xx | 2026-11-05 | appendix-schedule2.tex | Square-gap barriers (`2026-11-05-rees-square-gap-attack.md`, checked in `2026-11-05-rees-square-gap-attack-check.md`). New Lemma `lem:app-s2-kwise` (explicit law, independent on every κ−1 coordinates, with full proof replacing reliance on BGP Prop. 26). New Proposition `prop:app-s2-barrier` (the κ^κ/2 barrier for the joint-moment method, now proved; it includes TH9 Remark 5's bracket containment). New Remark `rem:app-s2-barrier-scope`. New Proposition `prop:app-s2-chebotarev` (no fixed algebraic construction; Chebotarev). New Remark `rem:app-s2-chebotarev-scope`. New Remark `rem:app-s2-four-cycle` (exact four-cycle sums, proof sketch). The tail of `rem:app-s2-joint-moments` was reworded from "argued, not proved here" to a pointer to the proposition. No number, threshold or table changed; the square gap is not closed. main.tex sentence on κ^κ/2 to be updated by the integrator (text in the check, §5). AI-checked, pending human review. |
