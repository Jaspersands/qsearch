# Referee report: `2026-11-08-rees-sde-near-linear.md` (dead-pair padding, Theorem H)

AI-only adversarial referee, 8 November 2026, one Claude Code session. Not human-reviewed. Only
this file and `2026-11-08-rees-sde-near-linear-referee/` were written. No `.tex`, STATE, handoff
or git edits, no network, `make_numbers.py` not run. Read: the report, `appendix-sde-side.tex`
lines 1–90, `main.tex` prop:triangular-sde, report B §4 (Assumption LP), `STATE.md`,
`TRAPS.md`. The derivations below are mine. The code (`referee_check.py`, output
`referee_check.out`) is new and shares nothing with the author's scripts.

## Verdicts

| Item | Verdict |
|---|---|
| H.1 Dead pairs unused (Lemma D, step (ii)) | CONFIRMED |
| H.2 Padding keeps the hard block's solution set | CONFIRMED |
| H.3 m = 2a − M + 4, range a+2 ≤ M ≤ 2a+4−⌈log_κ p⌉−λ | CONFIRMED |
| H.4 Failure ≤ 2κ^{1−λ}, p ≥ 4κm | CONFIRMED WITH CORRECTION (bookkeeping) |
| H.5 Solver → key recovery (union bound, shifted pattern) | CONFIRMED |
| H1 "M = O(a^{1+ε'}), O(a polylog a) … excluded" | REFUTED as written |
| H1 core statement M ≤ (2−ε)a at log_κ p ≈ εa | CONFIRMED WITH CORRECTION |
| H1 "any solver whose prime range contains some p ≤ κ^{εa−λ+4} is covered" | REFUTED |
| H2 | CONFIRMED WITH CORRECTION (stronger shift-invariant assumption; prime range bounded) |
| Prop. L | CONFIRMED WITH CORRECTION (for κ = 2 the counting step is argued; only the direct-sum shape is proved) |
| Paper cross-reference "rem:sde-worst-case(b)" | WRONG LABEL: the a+2 PRF reduction is rem:sde-subquadratic(b) (`appendix-sde-side.tex` l. 44) |
| Bearing on the total regime M ≥ κa+1 | None (§4) |

## 1. Theorem H, checked independently

**Kernel picture.** ker Λ = im Φ, where Φ(s, t₀, t) = (η_i(s + c_i t₀))_{i≤m} ⊕ t ⊕ d·t and
d ∉ P. The kernel is a direct sum: the block coordinates depend only on (s, t₀) and pair j only
on t_j. So a vector of P₀^M lies in the kernel iff its block part and each pair part are
separately in P₀. If t_j ≠ 0, then t_j ∈ P and d t_j ∈ P, so d ∈ P, a contradiction.
Hence every solution has t = 0, and the solutions of the padded bank are exactly the
embedded solutions of the hard block (H.1, H.2). In column language the pair is
(μ, cμ) with c = −1/d, and −c = 1/d ∉ P ⇔ d ∉ P, which matches Lemma D. The proof of Lemma D
needs μ outside the span of the columns *other than the pair*. The construction meets this
because each μ_j is a fresh coordinate vector.

**Counts (H.3).** Take k pairs and an m-column block in m − 2 dimensions. Then a = m + k − 2
and M = m + 2k, so 2a − M = m − 4 and k = M − a − 2. Both are integers for every (a, M), so
there is no parity restriction. k ≥ 0 ⇔ M ≥ a + 2, and m ≥ ⌈log_κ p⌉ + λ ⇔
M ≤ 2a + 4 − ⌈log_κ p⌉ − λ. Correct.

**Key extraction (H.5).** Write x = Φ(s, t₀, 0).
- If t₀ = 0, all ε_i equal cos(s). θ + c_i is uniform on F_p^× (the ⊥ branch is excluded), so
  this has probability exactly κ^{1−m}. The report's bound κ^{1−m}(1+κ/(p−1))^m is loose but
  valid.
- If t₀ ≠ 0, put K = s/t₀ and σ = cos t₀. For each i, either K = −c_i or
  cos(K + c_i) − ε_i = −σ.
- Conversely, every such (K, σ) gives (p−1)/κ solutions (choose t₀ in the coset σ). So the
  set of keys *any* solver can return is exactly the set of consistent (K, σ). A worst-case
  solver gains nothing by its choice, and the union bound over K ≠ θ and σ ∈ Z_κ is the
  right event.
- The per-query bound uses the bijection c ↦ (K + c)/(θ + c) from F_p ∖ {−θ} onto F_p ∖ {1}.
  It gives Pr ≤ 1/κ + 1/(p−1), independently over i. Correct.

**Failure bound (H.4), correction.** The two terms as written are κ^{1−m}(1+κ/(p−1))^m and
κ^{1−m}p(1+κ/(p−1))^m. With m ≥ log_κ p + λ and (1+κ/(p−1))^m ≤ 2, their sum is
≤ 2κ^{1−λ}(1 + 1/p), not ≤ 2κ^{1−λ}. Corrected statement: use the exact κ^{1−m} for (iii)
and p − 1 wrong keys in (v). Then

  Pr[fail] ≤ κ^{1−m} + 2κ^{1−m}(p−1) ≤ 2κ^{1−λ}.

Two further bookkeeping points:
- "Redraw if all c_i are equal" conditions the queries away from i.i.d. Either add
  (p−1)^{1−m} to the bound (the paper's choice) or count the redraws as extra queries.
- The λ fresh checks are not used in the bound, because λ already sits inside m.

The arithmetic behind p ≥ 4κm is correct: κm/(p−1) < 1/3 < ln 2.

**Hidden parameter assumptions.** Neither changes the reduction.
- The reduction needs the PRF's coset labelling, i.e. the generator g (or the root of unity),
  to pick η_i ∈ g^{−ε_i}P. This is a public parameter.
- The hardness conclusion needs p/κ superpolynomial. One query fixes θ + c_1 to a coset of
  size (p−1)/κ, so the PRF falls in time O((p/κ)·m), and is trivial at κ = p − 1. Under
  H1's linkage p ≈ κ^{εa+O(1)} this holds for a ≥ 3/ε, but "for every κ ≥ 2" needs this
  caveat in any hardness reading.

**Computations** (`referee_check.py`, [exact]):
- (A) For each sampled (θ, c), every consistent (K, σ) was listed by scanning all of F_p.
  This was done for κ ∈ {2, 3, 4} and p ∈ {2003, 3001, 20011}. The frequency of "some wrong
  key consistent" was 0.62/0.20/0.38/0.12/0.45/0.31, against union bounds of
  0.99/0.25/0.46/0.15/0.74/0.31. The bound is nearly tight, and 2κ^{1−λ} is vacuous at λ = 1.
- (B) Banks were built in column form, with my own nullspace routine, and the whole kernel
  (up to 37⁴ vectors) was enumerated. This covered 13 dead-pair instances with
  κ ∈ {2, 3, 4, 6} and p ∈ {29, 37, 41}:
  - The number of P₀-solutions equals the count predicted from (A)'s (K, σ) list exactly,
    and no solution touches a pair.
  - In 13 live-pair controls (−c ∈ P), thousands of solutions use the pairs.

## 2. Corollary H1 and the scope question

**What the hard set is.** Let L = ⌈log_κ p⌉ + λ. Theorem H plus zero-row embedding (an
instance at (a', M) is an instance at (a, M) for every a ≥ a'; take a' = min(a, M − 2)) gives
hard pairs exactly on

  L ≤ M ≤ 2a + 4 − L  (and p ≥ 4κL).

This handles ε = 1 cleanly: take a ≥ L and the k = 0 block in M − 2 of the a dimensions, not
a = ⌈(L−4)/ε⌉.

**Moves available, and why none crosses M = 2a.**
- Dead-pair padding maps (a, M) → (a+k, M+2k) and keeps 2a − M fixed.
- Embedding maps (a, M) → (a+j, M) and increases 2a − M.
- Deleting columns does not preserve solvability.
- Adding a column that is not dead changes the solution set. For κ = 2, adding live columns
  until M ≥ 2a + 1 makes every bank solvable (Chevalley–Warning), whatever θ is.

So nothing in the report converts a solver at a larger arity M' (a^{1.5}, a·polylog a, 2a+1,
κa+1) into a solver at a hard arity. For κ = 2 and M' ≥ 2a + 1, the promise problem *is* the
total problem. Such a conversion would be a PRF-hardness proof for the total problem, which is
exactly the open question.

**Refutation of the scope sentence.** "M = O(a^{1+ε'}), O(a polylog a) … are excluded for the
promise problem" is false as written. Counterexample: take ε' = 1 and
M = (a+1)(a+2)/2 = O(a²). The paper's own prop:triangular-sde solves *every* bank with that
many columns deterministically in poly(a, log p) for p ∉ E₂(κ). For any ε' > 0 and κ = 2,
M = a^{1+ε'} ≥ 2a + 1 is a total arity, which H does not touch. Correct statement: only
solvers that must handle banks with M ≤ 2a + 4 − L columns are excluded, e.g. every
M ≤ (2−ε)a at log_κ p ≈ εa. This includes an "M = O(a^{1+ε'}) algorithm" only in the
degenerate sense of an algorithm that accepts *any* number of columns up to that bound.

**Prime range.** The second refutation is the sentence "any solver whose prime range contains
some p ≤ κ^{εa−λ+4} is covered". Under the paper's stated assumption (key recovery needs time
superpolynomial in log p), a solver that works only at p = poly(a) yields a PRF attack in
time poly(a) = p^{O(1)}. Brute force over θ costs p·m anyway, so this is no contradiction.
The report's "for p = poly(a) the band is O(log a) columns wide" also fails under the paper's
assumption: at polynomial primes Theorem H gives nothing.

Corrected statement:
- Under the superpolynomial-in-log p assumption, H excludes poly(a, log p) promise solvers at
  primes with a ≤ (log p)^{O(1)}. The corollary's choice log_κ p = Θ(εa) is such a prime, so
  H1's displayed implication is right.
- Under the stronger exponential assumption (time p^{Ω(1)}, consistent with the known attacks
  in §3), a solver of running time (a log p)^c is excluded at primes p ≥ a^{C(c)}, at
  deficiency 2a − M ≥ C(c)·log_κ a. Only then does an "O(log a)-wide band at polynomial
  primes" appear, with a width that depends on the solver's exponent.

**H2.** Two corrections.
- (i) **Shift invariance.** Building the bank from ε and from ε + τ gives the same bank up to
  rescaling each column by an element of P. A common scalar g^{−τ} on all η_i moves each to
  the right coset, and P-rescaling of columns bijects the solution sets (checked in (C)).
  So the "extra loop over σ" is vacuous: every run returns some solution of *some* shift of
  ε, chosen by the solver. At p ≥ m²κ^{2m} all κ shifts have ~p/κ^m solutions; in (C) both
  σ = 0 and σ ≠ 0 are nonempty in every sample. A worst-case solver can therefore always
  return σ ≠ 0. H2 needs the shift-invariant assumption LP~: "find (s, σ) with
  cos(s + c_i) = ε_i + σ", allowing one erased condition when s = −c_i. LP~ hard ⇒ LP hard,
  so LP~ is the stronger (or equal) assumption. It is no less plausible, but it is not
  report B's Assumption LP.
- (ii) **Prime range.** κ^{Ω(m)} contradicts poly(a, log p) only if m = ω(log a + log log p).
  So "p ≥ 2^{poly(a)}" is fine, but "unbounded above" is not: at p = 2^{2^a}, poly(log p)
  exceeds κ^m.

**Prop. L.**
- The proved part (κ = 2) is: dead weight D has no solution of its own, so CW gives
  |D| ≤ 2·dim span D. *If D's span is complementary to the block's span*, this gives
  M ≤ 2a − n + 2r + 2. If the spans overlap, the bound weakens by 2·dim(overlap), and overlap
  is not excluded by the argument.
- The step "n ≥ r log_κ p − O(1)" is a counting heuristic for blocks whose planted solution is
  unique among ~p^r candidates. Hardness reductions with many key-revealing solutions are not
  covered. So the final "cannot reach 2a + 1" is [argued], within a narrow reduction shape.
- For κ ≥ 3, the density-2 claim genuinely needs large p. (D) found 1008 five-column banks in
  F₇² with no nonzero P₀-solution at κ = 3 (dead density 5/2), which agrees with the paper's
  N(3,2,7) = 5. This is no refutation of anything claimed, since the report says
  p ≥ κ^{O(a)} and the PRF is trivial at p = 7, but "κ ≥ 3 argued" should stay argued.

## 3. Is the hardness assumption reasonable? (from memory; nothing fetched)

The paper already uses exactly this assumption. rem:sde-subquadratic(b), not
rem:sde-worst-case(b), takes "recovering θ from O(log p) values at random points takes
classical time superpolynomial in log p" and draws the conclusion for M = a + 2 at
p ≈ κ^{a+O(1)}. H1 uses the same assumption at p ≈ κ^{εa+O(1)}; H2 uses a different one
(LP~).

Known classical attacks on the Legendre PRF, from memory:
- Khovratovich (2019): a birthday-type attack, about √p·polylog time with about √p queries.
- Beullens–Beyne–Udovenko–Vitto (2020): about p·polylog(p)/M² time with M queries, extended
  to power-residue PRFs.
- Kaluđerović–Kleinjung–Kostić (2020): table-based improvements. They solved the
  Ethereum-bounty instances at the smallest prime sizes (64/74 bits, as I recall).
- May–Zweydinger: preprocessing trade-offs.

With only O(log p) queries, all of these degrade to roughly p/polylog p, i.e. exponential in
log p. Van Dam–Hallgren–Ip needs superposition queries. So "superpolynomial in log p from
O(log p) random queries" is far weaker than the conjectured exponential security and is
reasonable. It is still a young, lightly studied cryptographic assumption, not a standard
complexity one, and it needs p/κ superpolynomial (§1).

## 4. Bearing on the total regime M ≥ κa + 1 (the actual open question)

None. Every instance in the report has M ≤ 2a + 4 − L < 2a + 1 ≤ κa + 1. The padding keeps
2a − M fixed, and no step moves a hard instance to a total arity. Prop. L (κ = 2, a narrow
reduction shape, partly argued) only says this technique cannot get there. The slogan
"near-linear algorithms must use totality" is near-tautological for algorithms run at a total
arity. Its non-trivial content is narrower: a procedure whose correctness uses only the
existence of a solution, and that is polynomial at primes with a ≤ (log p)^{O(1)}, cannot
exist at arity ≤ 2a + 4 − L.

What remains open:
- Whether diagonal SDE is solvable in poly(a, log p) time with o(a²/log a) columns, or with
  near-linear ones, in the total regime M ≥ κa + 1 (for κ = 2, at 2a + 1). The density remark
  suggests 2a + 1 might suffice for existence for all κ at large p; it is argued, not proved.
- There is neither an algorithm nor a hardness result there, under any assumption.
- Proved algorithmic arities stay at (a+1)(a+2)/2 for arbitrary banks and O(a²/log a) in
  general position.
- At polynomial primes, under the paper's own assumption, even the *promise* problem below 2a
  has no hardness from this report.
- The plausible routes to hardness are reductions from a believed-hard total problem:
  pigeonhole/ternary SIS-type problems, which are PPP-like; mod-p Chevalley–Warning search,
  which is PPA_p-like (classification of the diagonal case not checked); or F₃ zero-sum
  subset at p = 3, which the paper already notes. None is in hand, and Prop. L says dead
  padding cannot supply one.

## 5. Recommendations

- Correct the cross-reference: "rem:sde-worst-case(b)" → rem:sde-subquadratic(b), in §0.1, §3
  Scope and §5. The proposed one-sentence strengthening targets that remark.
- Replace the H1 scope sentence by the hard set L ≤ M ≤ 2a + 4 − L at primes with
  a ≤ (log p)^{O(1)}. Delete "O(a^{1+ε'}), O(a polylog a)" and "any p ≤ κ^{εa−λ+4} is
  covered".
- Restate H2 under LP~ with m = ω(log a + log log p).
- Label Prop. L [argued] beyond the direct-sum CW count.
- Use the corrected failure bound from H.4.
- Gates that must stay false: "total problem hard", "near-linear arity excluded", "uniform in
  p", "H unconditional".

## Files

- `2026-11-08-rees-sde-near-linear-referee/referee_check.py`: parts A–D as above.
  Run: `/opt/anaconda3/bin/python -B referee_check.py` (about 3.5 min, mostly part B).
- `2026-11-08-rees-sde-near-linear-referee/referee_check.out`: recorded output.
