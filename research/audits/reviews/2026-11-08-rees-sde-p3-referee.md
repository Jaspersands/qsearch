# Referee report: `2026-11-08-rees-sde-p3.md` (worst-case F_3^n subset sum, piece-scheme barrier)

This is an AI-only adversarial referee pass from 8 November 2026. No human has reviewed it. I
used my own derivations and wrote my own code; I did not rerun the author's scripts. The scripts
and outputs are in `2026-11-08-rees-sde-p3-referee/`, run with `/opt/anaconda3/bin/python -B`
(the SAT runs use pycosat). I wrote only this file and that folder, made no git or network calls
and did not run `make_numbers.py`.

## Verdicts

| item | claim | verdict |
|---|---|---|
| 1a | Lemma 2: a t-dimensional subspace of F_3^N has at most 2^t vectors in {0,1}^N; more than (3/4)2^t forces a partition subspace | **CONFIRMED** |
| 1b | Theorem 2: \|E_2\| = 240, E_2 ⊂ F_3^6 contains no 2-dimensional linear subspace, so a covering bundle gains ≤ 1 | **CONFIRMED WITH CORRECTION**: the shipped artifact says the opposite |
| 2a | Theorem 3: two dependencies never realize 3 dimensions | **CONFIRMED** |
| 2b | Theorem 4: the nested-support gadget | **CONFIRMED WITH CORRECTION**: degenerate empty classes |
| 2c | Theorem 5: the exact classification (subsets of T_1..T_4 with \|T\| ≥ 4; 130 feasible; four maximal sets) | **REFUTED** |
| 3a | Theorem 6(i): pieces with ≤ 2 dependencies need n²/3 − O(n^{3/2} log m) in Model A, and KOW is tight there | **REFUTED**: a Model-A algorithm uses about n²/4 |
| 3b | Theorem 6(ii): ≥ 0.195 n² for any number of dependencies per piece | **REFUTED as a proof** (the derivation fails); the statement is open |
| 3c | KOW lies inside Model A | **CONFIRMED** for the randomized version (sampling replaces enumeration) |
| 4 | Small cases: m = 6 at n = 2; 53 of the 1287 multisets at m = 5 defeat KOW; failures found at m = 8 (n = 3) and m = 12 (n = 4) | **CONFIRMED WITH CORRECTION**: these counts depend on the input order and on tie-breaking |

## 1. Lemma 2 and Theorem 2

**Lemma 2 [proved; exact check].** The pivot proof is correct: projecting onto t pivot
coordinates is injective and sends 0/1 vectors into {0,1}^t.

The (3/4) step also holds. For a non-copy coordinate ℓ = c_i z_i + c_j z_j + b, the four values
b, b+c_i, b+c_j, b+c_i+c_j cannot all lie in {0,1}. Lying in {0,1} would force c_i = c_j, and
then b − c_i is the third element of F_3.

`structure_checks.py` §A enumerates every subspace of F_3^N for N ≤ 5 and every subspace with
t ≤ 3 for N = 6, 48,162 subspaces in all. There are 0 violations of the 2^t bound, and every
subspace with more than (3/4)2^t zero-one points is a partition subspace. Lemma 3 (3^d ≤ 2^t,
dim K = t − d) follows directly. **CONFIRMED.**

**Theorem 2 [proved + exact].** My independent computation gives:
- \|E_2\| = 240.
- 0 ∈ E_2, reached only by y = 0.
- 28 lines {e, 2e} lie in E_2.
- **0 independent pairs** span a 2-dimensional subspace of E_2.

A direct brute force on the generic 8-class piece (one column per nonzero pattern, D(X) exactly
2-dimensional) finds 0 pairs (y_e1, y_e2) that give a 2-dimensional realization. The same holds
for k = 3: SAT reports UNSAT for d = 2 with all 26 patterns (`sat_gadget.out`). The proof (rank C
≤ 1, then nine distinct 0/1 points in a space of dimension ≤ 3) is correct.

*Correction.* The artifact the paper cites does not say "0 independent pairs".
`generic_piece.out` prints "2-dim subgroup inside class-union image: YES (28 pairs)" and "max
dim … 2; witness [(1,2,2,2,2,1),(2,1,1,1,1,2)]". The witness has b = 2a. `max_subspace_in` and
`direct_k2` never check that a and b are independent. The theorem is right, but its cited
evidence is a buggy output that literally contradicts it. Fix the script and regenerate the
output.

## 2. Theorems 3, 4 and 5

**Theorem 3.** By RREF enumeration, none of the 1210 two-dimensional subspaces of F_3^5 is
0/1-complete; 60 of the 130 for t = 4, 0 of 13 for (3,1) and 2 of 4 for (2,1) are
(`structure_checks.py` §C). The SAT formulation independently gives UNSAT for d = 3 from k = 2,
both for all 8 patterns and for T_1. The reduction to t = 5 and a partition subspace is correct.
**CONFIRMED.**

**Theorem 4.**
- All eight union identities hold modulo ⟨δ, δ′⟩, checked by a different method: indicator
  minus α·h lies in the relation span.
- h_1 and h_2 are independent modulo the relations.
- An exhaustive class-level search finds 120 pairs (y_e1, y_e2) that realize T_1.

*Correction.* The dichotomy "either 2-dimensional or one of the eight unions is a zero-sum set"
needs the listed union to be nonempty. There are 16 emptiness patterns (δ′ independent of δ)
that empty a listed union; for example, only P_21 and P_22 nonempty empties U_(1,0). In all 16
cases some nonempty class union is identically zero-sum (§E). So the corrected statement is:
"R(X) ⊇ ⟨h_1, h_2⟩, and if dim < 2 then some nonempty union of classes is a zero-sum set."

**Theorem 5: REFUTED.**
- Counterexample: T = {(0,1),(1,1),(1,2),(2,0),(2,1)}.
- It meets all four lines of F_3^2, so it lies in none of T_1..T_4.
- No combination aδ + bδ′ is {0,1}-valued on it, so no zero-sum set is available for free.
- Yet a 2-dimensional realization exists for every column set with these dependencies. Explicit
  C and local assignments are in `thm5_counterexample.out`, and 29 of 29 random instances with
  D(X) = ⟨δ, δ′⟩ exactly were verified by direct summation.

Exhaustively (`structure_checks.py` §D, cross-checked by SAT):
- 218 pattern sets are feasible. 136 of them are "trivial", meaning some dependency is
  {0,1}-valued.
- 82 are non-trivial: the 58 non-trivial subsets of the four 6-sets with \|T\| ≥ 4, plus
  **24 five-element sets that meet every line**.
- The author's "130" is the number of distinct per-C maximal sets G(C) in `confined_k2.py`. The
  author's own output lists 32 maximal 5-sets and "58 feasible T containing a full cylinder",
  both of which contradict the stated theorem.

Structural remark: T_1..T_4 are exactly the complements of the four lines. T_3 and T_4 are T_1
in the bases (δ+δ′, δ′) and (δ−δ′, δ′). So the "prescribed 0/1 pattern" case is the nested case
in another basis: both mean "some dependency has full support on X".

## 3. Theorem 6 and Model A

**3a. Counterexample to (i): the algorithm NEST, inside Model A.**

At codimension q:
1. Take F = the first ⌈1.5(q+2)⌉ + 3 unused columns.
2. Draw uniform samples of D(F) (P = ∅, τ = 0). Keep the smallest-support sample δ with
   \|supp δ\| ≥ rank(supp δ) + 2. Any sample with \|supp δ\| ≥ q + 2 qualifies automatically,
   because rank ≤ q.
3. Set X = supp δ. Draw a uniform sample δ′ of D(X) outside ⟨δ⟩.
4. The pattern set lies in T_1, so Theorem 4 realizes 2 dimensions at cost \|X\| ≈ q.
5. Return F ∖ X to the front of the pool, exactly as KOW does.

`nested_sampler.out` shows the result on uniformly random instances. Every witness was verified
by summation, and m_used counts every column ever pulled into the pool.

| n | KOW m_used/n² | NEST m_used/n² |
|---|---|---|
| 60 | 0.280–0.286 | 0.252–0.253 |
| 90 | 0.285–0.290 | 0.249–0.252 |
| 120 | 0.287 | **0.2506–0.2508** |

Per-round cost at n = 120 is \|X\| = q ± 2 for 2 dimensions. NEST uses exactly two sampled
dependencies per piece and only Model A operations. So "n²/3 − O(n^{3/2} log m)" is false in
Model A, and "the first bound is tight: KOW …" is false. The corrected heuristic statement for
≤ 2-dependency pieces is n²/4 − o(n²) [argued]: any 2-dimensional gain needs dim D(X) ≥ 2, hence
\|X\| ≥ rank(X) + 2, and NEST attains this.

**Where the proof breaks (T_1 case).** The proof derives that a T_1 piece costs ≥ q for
2 dimensions, which is below 4q/3. It then dismisses this with "probability ≤ 4(3/4)^{|F|} of
full support on a defect-2 set". That probability concerns a *pre-chosen* set. A sampled δ always
has full support on its own support, and that support has defect ≥ 2 as soon as it has ≥ q + 2
elements. The same error is in §4(a) ("3^{−Ω(q)} per candidate set") and in §0 item 1 ("not a
general-position event … no averaging method produces"). Averaging, that is a random element of
D(F) with \|F\| ≈ 3q/2, produces the event with constant probability.

**Other defects in the proof:**
- **Lemma 6.1 is wrong for KOW's own spaces.** With \|F\| = q + r and r = ⌈log_3(q+1)⌉, the
  coordinate functionals of D(F) are q + r vectors in F_3^r, which have at most (3^r−1)/2
  projective classes. The measured fraction ρ of proportional coordinates is 0.65–0.86 for
  q = 20..240 (`lemma61_rho.out`), not o(1).
- Chebyshev also cannot be union-bounded over poly(m) samples: λ = q^{3/4} gives a per-sample
  failure probability of q^{−1/2}.
- Even as stated, a per-piece loss of O(q^{3/4} log m) sums to O(n^{7/4} log m), not
  O(n^{3/2} log m).
- **Lemma 6.2** union-bounds "over the polynomially many sets the run touches". Those sets are
  chosen adaptively from the pool, so this is invalid. The general-position property it needs is
  also false for some sets: m = Θ(q²) random columns contain dependencies of weight O(q/log q).
  The statement itself is garbled ("− O(1)… more precisely").
- **T_3/T_4 case.** The 3^{w−q} bound is valid only when W consists of fresh columns chosen
  without looking at their values. Model A allows choices to "depend on everything seen", and it
  allows reused leftovers.
- The case list T_1..T_4 is incomplete anyway: Theorem 5 is refuted.

**3b. Part (ii).** Arithmetically, (log₂3 − 1)/3 = 0.19499, so "≥ 0.195 n²" is off in the fourth
digit. The real problem is the derivation:
- It charges each sample fresh weight ≥ (2/3)(q − d). That bound is vacuous when d is close to q.
- Lemma 6.2 gives nothing once S_old ≥ q. Later samples inside an earlier support cost zero
  fresh columns, and that is exactly NEST's mechanism.
- Lemma 3 plus fresh-weight counting therefore does not bound such pieces. Theorem 2 cannot
  replace it for large k, because 3^k − 1 patterns cannot all appear on \|X\| columns once
  k > log_3\|X\|.

I tested the obvious attack, k = 3 nested (δ_1 full support, all 18 patterns with π_1 ≠ 0). SAT
says it does **not** realize 3 dimensions (UNSAT, `sat_gadget.out`). So I have no counterexample
to the number 0.195; only the proof fails. The d = 4, k = 4 run was stopped unfinished after
about 6 minutes of CPU time.

**3c. How restrictive Model A is.** The model is not stated precisely enough to be a theorem's
hypothesis:
- "y − y′ ∈ span(samples) whenever φ(y) = φ(y′)" is garbled. Samples with τ ≠ 0 are not
  dependencies.
- It does not say whether F, c and τ may be computed from the column values, or how much
  computation is allowed.

The possible readings:
- **With unbounded computation**, Theorem 6 is false. Find a minimum-weight dependency (weight
  O(q/log q)), set F = its support and sample D(F). That gives O(n²/log n).
- **With polynomial time and choices computed from the columns**, an unconditional proof would
  imply P ≠ NP. If P = NP, that same algorithm runs in polynomial time.
- **"Oracle-only" access is no restriction on information.** Samples of D([m]) reveal the
  kernel and hence the instance up to GL_q.

So Model A restricts nothing except computation, and its only enforceable content is
syntactic: oblivious F, fresh columns. NEST satisfies even that strict reading.

Natural algorithms outside the model (or simulable inside it only by choosing F after the fact):
- information-set and Stern-type decoding;
- BKW/Wagner collision merging;
- column selection by value (subspaces, repeated vectors; KOW itself wins on structured families
  by grabbing short dependencies, `nested_families.out`);
- KOMSW-style adaptive gadget selection;
- deterministic enumeration (KOW's derandomized form).

KOW is in the model as a randomized algorithm. Polynomially many samples exhaust \|D(F)\| ≤ 3(q+1),
and the relation y_{2u} − 2y_u = δ is certified.

## 4. Small cases

`kow_small.py` is an intrinsic, coordinate-free implementation that branches over all sparsest
dependencies. Results:
- n = 2, m = 6: 0 failures over all 531,441 ordered sequences. The recursion m_1..m_8 =
  3, 6, 9, 13, 18, 24, 30, 37 is reproduced.
- n = 2, m = 5: in the author's sorted input order, 53 of the 1287 multisets fail, independently
  of tie-breaking. All 1287 have a zero-sum subset (Davenport constant 5). The example
  {(0,1),(1,0),(1,1),(1,2),(1,2)} fails.
- *Correction:* **no** multiset fails in every order. 232 multisets fail in some order, and
  2592 of the 59,049 ordered sequences fail.
- The reported n = 3 (m = 8) and n = 4 (m = 12) failure instances fail only under the author's
  tie-break. Another sparsest choice solves them.

## 5. Consequences, gates, next question

- §0 items 1 and 2, the Theorem 5 interpretation, and §4(a) must be rewritten. The 2-dependency
  "precondition" is cheap. What remains of the worst-case question is computational, not
  combinatorial.
- Gates that must stay false:
  - "a worst-case c < 1/3 is obtained";
  - "NEST's n²/4 is a worst-case or novel result". It is random-instance and sampled up to
    n = 120. KOMSW claim 0.1022 on average, which is unverified;
  - "Theorem 6 is proved in any reading".
- **Next hard question.** Lemma 1 and Theorem 4 are deterministic: any dependency δ with
  \|supp δ\| ≥ rank(supp δ) + 2, i.e. whose support is not a circuit, gains 2 dimensions at cost
  \|supp δ\|. So a worst-case constant below 1/3 follows if, in every pool of poly(q) vectors in
  F_3^q, one can find in polynomial time a dependency with non-circuit support of size
  ≤ (4/3 − ε)q. Every dependency of weight ≥ q + 2 qualifies, so this asks for a codeword of D(F)
  in the weight window [q + 2, (4/3 − ε)q]. The adversary would have to force a weight gap
  around q in every shortened code.
- **Next command.**
  `cd research/audits/reviews/2026-11-08-rees-sde-p3-referee && /opt/anaconda3/bin/python -B nested_families.py`,
  extended with a hill-climb that maximizes, over pools of ≤ 3q/2 + 3 vectors at n = q ∈ {8..14},
  the least non-circuit-support dependency weight.
  - Expected artifact: `nested_worstcase.out`.
  - Acceptance: either an explicit family where that weight is > 4q/3 (a worst-case obstruction
    to NEST), or no pool exceeding q + O(log q) after 200 climbs per q, recorded as [sampled].
