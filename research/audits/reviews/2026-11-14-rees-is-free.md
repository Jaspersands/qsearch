# 2026-11-14 Rees core: Theorem main without the Ivanyos–Santha import for c ≤ 9

AI helper report. Everything here is AI-checked and pending human review. Nothing has been refereed.
Folder: `research/audits/reviews/2026-11-14-rees-is-free/`. The core `docs/papers/rees-hsp/core/main-core.tex` was not edited (md5 `71743611d8b66af3e0d485110953a9e1`, before and after).

## Verdict

**PROVED given the cited theorems and an exact computation (AI-only, unrefereed).** For every class c ≤ 9 and every prime p > c, Theorem main of the core holds as stated, with the same Q_q, the same bounds (3)–(5) and headline exponent E_+(9) = 20, with no use of thm:is-import, Lemma rounds (Schedule 1), IS Theorem 11 or the zero sums of lem:zero-sum-length(iv).

The reason is a dominance statement. In Definition def:plus-schedule, candidate (a) (S1) **never attains** the least arity at any (p, κ ≤ 9), at any a ≥ 0, at any depth L ≥ 1 (with one exception at the depth L = 1 only, (p,κ) = (5,4), where the actual depth L = 3 is used), inner solvers included. So deleting (a) leaves every arity A^+_κ(a) unchanged, and Schedule 1H+ as written already never runs it.

The cited theorems are Weil's bound for diagonal equations, Rabin root finding and Chevalley–Warning. They are used through the existing lemmas of sec:halving and sec:plus.

## New statements (fragment.tex)

- **Lemma lem:plus-free-const** (fragment.tex:12–19). Every candidate other than (a) has constant K ≤ (κ−1)^{f(e)}, with f(x) = x(x−1)/2. So if e_Z ≤ κL and K_Z < κ^{κ(κ−1)L/2}, in particular if e_Z ≤ κ, then arity_Z(a) < G(κ,a)^L for all a.
  - The proof uses: chains (TL, TW, Tier B, nodes f2/f3, chain finishes; constant ∏(|Δ_t|−1), Corollary plus-chain) satisfy f(e_0+L') − f(e_0) ≥ L'; the ℓ-level candidates have constant (κ−1)^{f(ℓ)} by definition; plans follow from the superadditivity of f.
  - Status: **PROVED**.
- **Theorem thm:plus-free** (fragment.tex:21–46).
  - (i) The IS-free solver H°_κ has a candidate at every (p, κ ≤ 9), and e° = e^+.
  - (ii) A° = A^+ < G^L for all a, so (a) is never run.
  - (iii) Theorem plus(ii)–(iv) hold for H°, with at most 12 Las Vegas preprocessing tasks.
  - Status: **PROVED given cited theorems**. For p < 2·10^6, (i) and (ii) are **PROVED given an exact computation**.
- **Remark rem:plus-free-ten** (fragment.tex:48–53, optional).
  - The same holds at c = 10 (κ = 10: the (f1) plans over H°_5).
  - Corollary utz then extends to n = 11.
  - For c ≥ 11, at p ≡ 1 (mod 11), κ = 11 has only candidate (a), so the import is still used there.
  - Status: **PROVED given an exact computation** for p < 4·10^4, and by Lemma two-term above that. Unrefereed and lower priority.
- **Corollary cor:main-free** (fragment.tex:55–62, inserted before rem:oblivious).
  - Theorem main for c ≤ 9 with thm:is-import removed from the hypotheses.
  - It also covers Corollaries black-box, black-box-pe and nilpotent for c ≤ 9, and Corollary utz for n ≤ 10.
  - Corollary nilpotent still imports Imran–Ivanyos Theorem 1, which is a different import.
  - Status: **PROVED given cited theorems + exact computation**.

## Obligation 1: a solver at every grade without the import

The proof is by induction on κ over its divisors.

**Large p (p ≥ 2·10^6).** Every Table tab:plus-thresholds step is available (Lemma plus-sm(i)), and plan (1,F1) is admissible by Lemma two-term. The candidates other than (a), each of degree ≤ κ, are:

| κ | candidate | degree |
|---|-----------|--------|
| 2 | plan over GE | 2 |
| 3–6 | TL_κ | 2 |
| 7 | plan over (GE; U_m) | 3 |
| 8 | plan over H°_4 | 3 |
| 9 | TW over H°_3 | 3 |

Lemma plus-free-const then gives strict dominance. Status: **PROVED**.

**Small p (p < 2·10^6).** The exact computation finds a candidate at every pair (check A = 0 failures). Every pair has a candidate of degree ≤ κ, except (5,4).

At (5,4): t_{5,4} = 5, so L = 3. The plan (H°_2, s = 2, F1) is admissible because P = {1}, ξ = 2, ε = 1 and T_2 = F_5^×. Its degree is 5 ≤ 12 = κL, and its constant 1 < 4^18. Status: **PROVED by hand**, in fragment.tex, Small-primes paragraph.

**Halving stages and finishes.** Stages (lem:stage, lem:plus-stage) call the inner node and the finish. Finishes F0, F1 and fΩ call H°_D, Gaussian elimination or chains, never (a). The inner solvers are IS-free by induction, so the recursion never bottoms out in S1.

**Lemmas used:**
- the sec:plus lemmas: plus-refine, plus-sm, plus-tensor, plus-ell-node, plus-stage, plus-finish, Proposition plus-tables;
- lem:stage, lem:finish, lem:two-term and rem:kappa-two;
- the first sentence of lem:bezout (Gaussian elimination at κ = 1);
- Rabin root finding and Weil;
- the exact computations, re-run with (a) deleted.

**Not used:** thm:is-import, lem:rounds, Theorem halving(ii) for candidate (a), the zero-sum computation of lem:zero-sum-length(iv), cor:hcd and van de Woestijne.

t_{p,κ} enters only through L in the comparison. That comparison is a proof that (a) loses, not a use of (a).

## Obligation 2: the computation with S1 forbidden

All runs used `nice -n 19` and stayed within the caps. The largest run took 136 s.

| run | scope | result |
|---|---|---|
| `isfree_check.py 2000000` → `isfree_2e6.out` | 148,932 primes < 2·10^6, 496,058 (p,κ) pairs | full and IS-free E(c), c = 2..9: **3,5,9,10,14,16,18,20**; 266 attainers at c = 9 (non-2520: 37, 43, 73, 127, 181, 631). Checks: A 0, B 0 (per-pair e° = e^+), C 0, D 0; D1 (L = 1) fails only at (5,4) |
| `isfree_check.py … tail` → `isfree_tail.out` | 1152 primes > 2·10^6, one per unit class mod 5040 | all checks pass, D1 included; tail E = 3,5,7,9,11,14,17,20 |
| `ref20_copy/run2.py` (20-referee's code, copied) → `run2_allB_noS1_rerun.out` | p < 2·10^6, S1 off | identical to the original `run2_allB_noS1.out` apart from the time line; E = {2:3,…,9:20}; no-plan primes [] |
| `ref20_copy/dump_noS1.py` + `compare_degs.py` → `compare_degs.out` | per-pair degrees from the two programs | same 496,058 keys, **0 disagreements**; only e° > κ pair: (5,4) = 5 in both; max e° per κ: {2:2,3:2,4:5,5:4,6:6,7:5,8:6,9:4} |
| `kappa10_check.py`, `kappa10_indep.py` | 1044 primes < 4·10^4 with 10 \| p−1 | no prime lacks a plan; no dominance failure; histogram {3:1026, 4:9, 6:8, 16:1}; both programs identical |

The smallest dominance margins K_S1/K_Z, over all primes, per κ, are:

| κ | margin |
|---|--------|
| 2 | 2 |
| 3 | 13.5 |
| 4 | 4.1e3 |
| 5 | 6.1e5 |
| 6 | 2.35e11 |
| 7 | 7.76e15 |
| 8 | 6.45e24 |
| 9 | 1.41e33 |

At κ = 2, S1 ties the least degree at 74,416 pairs, but its constant is always strictly larger.

**No prime needs S1, and no exponent changes.**

## Obligation 3: other parts of thm:main

| part | finding |
|---|---|
| Polynomiality | Unchanged: the arity is unchanged, and Theorem plus(iii) is per-candidate. |
| Determinism / Las Vegas | 1H+ was already Las Vegas. Deleting (a) removes the one deterministic-given-zero-sums path, which was never selected. The wording "Schedule 1 alone … deterministic given its zero sums" (main-core.tex:210) stays true as a remark about Schedule 1, not about the solver used. |
| Error budget, rem:is-import(d) | n_pre ≤ 12 ≤ 2(c−1)+12: one ξ choice for p ≥ 2·10^6, plus at most 11 contraction searches. Failure probability 0, with a Markov cut-off. Unchanged. |
| Arity computability | A^+_d(g_d) is computed from (p, d, g_d) by the same recursion, minus one branch. |
| Class-3 and Heisenberg examples | At c ≤ 3, κ ∈ {1,2,3}, with GE, the κ = 2 plan and TL3, of degree 2 at p ≥ 2·10^6. Small p by the computation. No IS. |

## Obligation 4: what still needs the import, and the text edits

**Still needs thm:is-import:**
- the class c ≥ 11, at primes p ≡ 1 (mod 11) (and similarly at κ = 11..c), where only candidate (a) exists;
- class c = 10, unless PART 2 is adopted;
- Schedule 1 / Schedule 1H stated alone (exponents 53 and 31), Lemma exponent and Lemma halved-exponent;
- rem:is-printed and the full-depth values 145 and 95.

The fragment and `edits.py` change these places, conservatively (c ≥ 10 keeps the import):
- the abstract (E1);
- the informal statement (E2);
- the thm:main hypothesis: "if c ≥ 10, assume thm:is-import" (E3);
- the paragraph after the theorem (E4);
- rem:main-solver (E5a–c);
- the imports sentence (E6);
- the black-box paragraph (E7);
- related work (E8);
- what is new (E9);
- the Verification Status sentence (E10);
- a new rem:is-import item (f) (E11; it references rem:plus-free-ten, so drop it with PART 2);
- rem:proof-uses (E12);
- rem:black-box-scope and rem:nilpotent-scope (E13);
- Outlook, "Halving at the confirmed depth" (E14);
- the Artifacts item (E15);
- R1: replace rem:plus-is (main-core.tex:1007–~1020) with PART 1, and PART 2 if used;
- R2: insert PART 3 before rem:oblivious (main-core.tex:1103).

Ivanyos is cited only for the full-depth bound. All the "AI-checked, pending human review" labels are kept.

**How to apply.** `python edits.py check` verifies that every one of the 25 old strings occurs exactly once in the current core. `python edits.py apply OUTDIR` writes a patched copy, and refuses any OUTDIR under the core directory. The scratch compile of the patched copy gives 71 pages, 0 undefined references and 0 overfull boxes (`compile_check.log`, `main-core-applied.tex`). The integrator is slimming the core, so re-anchor the old strings after that.

## Caveats

- main-core.tex:257 and :787 say the merged write-up of sec:plus "has not itself been refereed". The core-plus referee (`2026-11-14-rees-core-plus-referee`) has refereed it since, so this is stale. E10 does not fix it; the integrator should.
- The arities rest on Theorem plus as written. Its own status is AI-refereed only.
- For c = 10, the remark relies on H°_5 values from the κ ≤ 9 computation, and on plan (1,F1) for p ≥ 4·10^4.

## Adversarial self-check

1. **Shared code.** `isfree_check.py` reuses the referee's `plus_mine.py` helpers: availability, T_sets, chains and t_value. It is independent of the authors' code only in the sense that the referee wrote `plus_mine.py` from the text. The second program, `ref20_copy/run2.py`, is the 20-referee's code, a different lineage. The per-pair degrees agree at all 496,058 pairs. The two programs may share misreadings of the text.
2. **Certificates and rc caches.** These are the authors' data. All 75,391 were re-checked (0 bad), but availability for p ≤ DFS bound uses a DFS with caps. Three capped DFS runs at p = 307 (κ = 9 Tier B steps) were treated as unavailable. That is conservative for existence: if one were available, the IS-free arity could only drop, and so could A^+, symmetrically. The core-plus referee showed them NONE with a 3·10^10 cap.
3. **Shared method at κ = 10.** `kappa10_check.py` and `kappa10_indep.py` share their method, and the second takes e°_5 from the first program family's dump. So PART 2 is weaker than PART 1.
4. **Strictness.** Dominance was tested numerically with ≤, and the fragment states it strictly. The smallest margin is 2 > 1, and at (5,4) the margin is 4^18. The lemma gives strictness whenever e ≤ κ. So strictness holds, but it was checked by reading the margins, not by a separate test.
5. **Tail limits.** The tail run covers one prime per residue class mod 5040, which only falsifies. The large-p claim rests on the proof (Lemma plus-sm(i), two-term), not on the tail.
6. **Proof gaps.** The proof of Lemma plus-free-const treats TW as a one-step chain (|Δ| = 3, factor 2) and takes the ℓ-level constants from Definition plus-schedule. This was checked by hand against the constants in the code (`isfree_check.py:56–67`), not by a separate referee. A hostile referee should re-derive K for each candidate type.
7. **Review status.** Nothing in fragment.tex has been refereed. All of it is AI-checked, pending human review.
