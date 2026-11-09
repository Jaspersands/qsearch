# Referee C: F_q nest note (2026-11-08-rees-sde-fq-nest.md), §§1, 2, 4, 5

AI-only adversarial referee, 9 November 2026, one Claude Code subagent; not human-reviewed. No git,
no network. The only files written are this report and `2026-11-09-rees-sde-fq-nest-referee-C/`
(scripts and outputs). Interpreter `/opt/anaconda3/bin/python -B`, CaDiCaL plus the scratchpad
`lrat-check`. Total CPU is about 15 minutes. [9 Nov correction: that build was unsound (it accepted an
empty clause without a conflict). All 64 UNSAT runs of this report were re-run on 9 Nov with the fixed
build `2026-11-09-lrat-checker-fix/`: output lines identical apart from timings (verdicts, variable and
clause counts; for the three gadget_cnf5 reruns also CNF hashes and proof sizes), every proof VERIFIED
(`2026-11-09-lrat-checker-fix/recheck/refC_compare.out`). The split files that `split_coverage.py`
counts were not re-checked: CaDiCaL UNSAT, not independently proof-checked. The k = 3, p = 7 and (11, 2)
cells were re-verified separately, case by case without the γ_(1,1) split
(`2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`, `cases11_cases.out`, `cases11_c10.out`).]

## Verdicts

| item | verdict |
|---|---|
| A. Theorem C | **ACCEPT WITH FIXES** (minor: hypotheses and wording) |
| B. Lemmas R, Q, U and `cases_cover.py` | **ACCEPT WITH FIXES**. R is exact. Q's written proof shows the wrong direction; the claim holds for S = P ∪ {0} by Lemma N below. U is a complete cover, proved for every p. |
| C. k = 3, p = 7 two-case first slot | **ACCEPT**: a complete cover, proof below. It is also the right cover for any k ≥ 2 (k = 4: two cases). |
| D. CNF encoding, γ_(1,1) split, scope | **ACCEPT WITH FIXES** for the S = P ∪ {0} cells. **GAP** for the (b) q = 11 interval cell (Finding 2). There is also a scope overclaim in §4 (Finding 3). |
| E. Lemma Z | **ACCEPT** (minor wording) |

## Findings

**1. [material] Lemma Q (§1) proves only the easy direction.** The proof shows that a P-equivariant
solution on the orbit representatives extends to the P-closure. The UNSAT verdicts need the
converse. With one column per label, Φ(ℓ) and Φ(λℓ) are independent. A free solution's
rescaled choices ψ_λ = λ^{-1}Φ(λℓ) are each feasible for ℓ, but weak nondegeneracy is a
disjunction over columns, so one equivariant choice per orbit could in principle lose it.

- In general this can fail. Let W(Φ) = {α : ℓ ↦ ⟨α, Φ(ℓ)⟩ is linear on the columns}. W is a
  subspace, and a direction is degenerate iff it lies in W (see the remark after Lemma N). A free
  solution can have W = {0} while every equivariant selection has W equal to a line.
- **Repair (Lemma N, proved here).** Let S = P ∪ {0} with κ ≥ 2, fix r ∉ P, and let L span
  F_p^k with no nonzero linear functional S-valued on L. The nested set F_p^*×F_p^{k−1} and
  F_p^k∖0 qualify for every k. Then in every *feasible* (Φ, γ), and for any column multiplicities,
  the direction [α] is degenerate iff γ_{rα} = rγ_α. So nondegeneracy depends on γ alone.
- *Proof of Lemma N, forward direction.* If γ_{rα} = rγ_α, then y_{rα} = r·y_α, so
  y_α ∈ S ∩ r^{-1}S = {0}. Then y_{λα} = ⟨γ_{λα} − λγ_α, ℓ⟩ is a linear functional that is
  S-valued on L, hence 0, for every λ.
- *Converse.* If the direction is degenerate, then 0 = y_{rα} − r·y_α = ⟨γ_{rα} − rγ_α, ℓ⟩ on a
  spanning L. ∎
- Hence Lemma Q is exact for S = P ∪ {0}: restrict to the representatives and extend
  equivariantly. This keeps γ, so it keeps nondegeneracy.
- *Independent confirmation.* `free_cnf.py` is a new encoding without Lemma Q (and optionally
  without Lemma R). It gives UNSAT at p = 7, κ = 2: 19/19 Lemma U cases for the nested set,
  19/19 for all 48 patterns, and 19/19 nested without Lemma R. It also gives UNSAT at p = 7,
  κ = 3 unsplit. All 58 runs are LRAT-verified [re-verified with the fixed checker, 9 Nov].
- *Sampled check.* `lemma_n_check.py` tested the equivalence on 120 feasible models with
  nondegeneracy dropped, at p = 5 and p = 7, κ = 2 and 3. There were 82 degenerate directions
  and 0 violations.

**2. [material] The (b) q = 11 cell (S = {0,±1,±2}, k = 2, nested, "UNSAT (581 s)", §2 and §0.4)
is not established.** Here P = {±1} but S ∩ 2S = {0,±2} ≠ {0}, so Lemma N's proof does not apply.
The verdict covers only the P-equivariant problem.

- The general fact (proved, using the W-subspace remark) is weaker: a free solution yields an
  equivariant one on the representatives plus **at most two extra columns**. Each added column
  strictly shrinks W, and d = 2.
- Fix: rerun without the label reduction (about 19M clauses), or with "representatives + 2 free
  extra columns" (one-hot label choice). Otherwise mark the cell as a verdict for the
  equivariant problem.
- The interval cells k = 1, d = 2 at q = 11, 13 and the k = 2 nested cell at q = 7, 5 were
  re-run without Lemma Q: they give UNSAT, UNSAT, UNSAT and SAT, agreeing with the note
  (`free_interval.out`).

**3. [material, scope] The §4 sentence "Any piece gaining 2 from two dependencies therefore needs a
missing pattern … This closes the k = 2 route at these p" overstates what is proved.**

- Lemma 2(B) is stated for one column per label, but real pieces have multiplicities. Lemma N
  gives the multiset extension for S = P ∪ {0}: the feasibility constraints are per label given γ,
  and nondegeneracy depends on γ only. The note should state this.
- Even so, what is proved is a property of one label set (and of its supersets, since
  infeasibility is inherited upward). The note constructs no instance family on which every
  two-dependency piece that a selection rule can choose has the full nested pattern set.
- "Closes the route" should be labelled [argued]. The exact claim is the per-label-set
  infeasibility. The gate "not an algorithmic lower bound" (§7) is correctly stated.

**4. [minor] Theorem C hypotheses and wording.**

- (i) For κ = 3, "every odd p" must read p ≡ 1 (mod 3). Otherwise (F_p^*)^3 = F_p^* and the
  problem is trivial.
- (ii) E_2(2) = ∅ is elementary. Take α = (1, 0), β = (0, x) with x ∈ P and x + 1 a non-residue.
  Such an x always exists, because 1 is a residue and not all of 1..p−1 are.
- (iii) E_2(3) = ∅ is imported from the paper (exact search below T_A(3) plus the T_A bound;
  AI-checked, not human-reviewed). `contraction_check.py` found a normalised contraction at every
  p < 1000 for κ = 2 and κ = 3.
- (iv) "Deterministically" should read "deterministic given g and (α, β)", as in the paper's
  proposition. A non-residue is not found deterministically in poly(log p) unconditionally.
- (v) State the running time. Enumerate the dependency space projectively:
  (p^r − 1)/(p − 1) < 1.5(l + 1) codewords per round, so the time is poly(a, log p).
- (vi) The gain over (a+1)(a+2)/2 is a²/(2p) − O(a log a), which is positive only when
  a ≫ p log a. For r = 1 the round cost equals the paper's l + 1, so Theorem C is never worse.

**5. [minor] Lemma U's orbit claim is shown only by computation at p = 7, 11, 13. A general proof
for every p:**

- The transpose action on functionals is σ^T(w_a, w_b) = (λw_a + νw_b, μw_b). Its orbits are
  {w_b = 0} ∋ a and {w_b ≠ 0} ∋ b.
- Stab(a) is {λ = 1}. It sends w_2 = (x, y) to b if y ≠ 0, and to x·a otherwise.
- Stab(b) is {ν = 0, μ = 1}. It sends (x, y) to (λx, y), giving a, a + gb or gb. The swap
  identifies (b, a) with (a, b).
- Total: 1 + 3(p − 1) = 3p − 2 cases. The cases are redundant, which is harmless: at p = 7 the
  19 cases meet all 13 pair-orbits (`orbit_k.out`, an independent union-find computation).
- The symmetries preserve the problem. Both σ (a bijection of the nested set and of F_p^2∖0) and
  the swap preserve feasibility, weak nondegeneracy, the Lemma R form, P-equivariance and the
  normalisation γ_{e_j} = 0.
- `cases_cover.py` checks the right object: pairs of functionals under σ^T together with the
  swap.

**6. [minor] Lemma Z wording.** "with 2 among them" is garbled. The precise statement is:

- The allowed nonzero values of ⟨γ, ℓ⟩ are {−2, −1, 1}, which is 3 values.
- A nested or full label set gives a functional (g, 0, …) at least p − 1 ≥ 4 nonzero values, and
  gives any other nonzero functional all p values.
- The last sentence ("no polynomial of degree below q − 1 from this framework") is [argued].

**7. [minor] Certificates.** The κ = 3, p = 13 cells rest on PicoSAT without a certificate and
should be labelled as a solver verdict. The (7, 2) unsplit 1436 s run was not re-verified here.

**8. [minor] The `cases7k3.txt` cover was unjustified in the note.** The proof is supplied under C.

## C. The k = 3 first-slot cover (derivation)

- **Lemma U holds for every k ≥ 2.** If γ_{(r,0)} = 0, then rΦ_1 ∈ S ∩ rS = {0}. The realizers of
  [(1,0)] are then linear functionals that are S-valued on F_p^*×F_p^{k−1}, so they are 0.
  Hence γ_{(r,0)} ≠ 0.
- **Symmetries.** σ(a, b) = (λa, Mb + av), with M ∈ GL_{k−1} and v ∈ F_p^{k−1}, preserves the
  nested set. Its transpose action is σ^T(w_a, w_b) = (λw_a + ⟨w_b, v⟩, M^T w_b).
- **Orbits.** If w_b ≠ 0, choose M with M^T w_b = e_1 and v with ⟨w_b, v⟩ = −λw_a; the image is
  b = (0, 1, 0). If w_b = 0, the image is a = (1, 0, 0). So there are exactly two orbits, and
  γ_{(3,0)} ∈ {3a, 3b} up to symmetry.
- **The file matches.** These are the two lines of `cases7k3.txt` (r = 3 = creps[1] at p = 7,
  κ = 2).
- **Sanity checks.**
  - `orbit_k.py` gives 2 orbits at (p, k) = (7, 3), (7, 4) and (11, 3).
  - The forced case γ_{(3,0)} = 0 is UNSAT in 9.7 s, LRAT-verified [re-verified with the fixed checker, 9 Nov].
  - Two sub-cases were re-run and agree with the original CNFs byte for byte (same sha256):
    `3,0,0;1,1,0:2,5,1` and `0,3,0;1,1,0:4,0,6` (`rerun_k3_7.out`).
  - For k = 4 use `1,0,1:3,0,0,0` and `1,0,1:0,3,0,0`.

## D. Encoding and split

`gadget_cnf4/5.solve4` encodes the problem exactly, given Lemmas R and Q:

- Φ ∈ S^2 one-hot per representative label.
- One γ slot per (projective direction, coset representative), with γ = 0 at the unit
  directions of coset 0.
- A binary or ternary clause forbids each pair with r⟨α_D, φ⟩ + ⟨γ, ℓ⟩ ∉ S.
- Nondegeneracy is a per-direction OR over cosets and representatives.

So it is exact for S = P ∪ {0} (Finding 1), and not shown to be exact for interval S at q = 11
(Finding 2). The split and the certificates check out:

- `run_split.sh` and `run_split_k.sh` enumerate all p^k values of γ_(1,1). That is an exact cover.
- `split_coverage.py` (independent parser) found cases11 3751/3751, cases13 6253/6253 and k3_7
  686/686, with 0 missing, 0 extra, 0 duplicated, and every line UNSAT with LRAT VERIFIED [9 Nov: those
  strings came from the unsound build; CaDiCaL UNSAT, not independently proof-checked (checker was unsound,
  9 Nov)].
- `cases{7,11,13}.txt` and `cases13k3.txt` equal the `cases_gen.py` output.
- The acceptance test `'c VERIFIED' in stdout` rejects a truncated proof and a proof against a
  weakened CNF: lrat-check prints "c NOT VERIFIED" for both, and that line does not contain the
  substring "c VERIFIED". [9 Nov: but that build printed "c VERIFIED" for a one-line proof of the empty
  clause without hints, on any CNF; see `2026-11-09-lrat-checker-fix/controls.out`.]

## A. Theorem C (checked steps)

- **Averaging bound.** For an r-dimensional code, a coordinate that is not identically zero is
  nonzero in a fraction (p^r − p^{r−1})/(p^r − 1) of the nonzero codewords. So
  min wt ≤ (1−1/p)(l + r)/(1 − p^{−r}). This is correct and self-contained, with no KOW import
  needed. l + r columns at codimension l give a dependency space of dimension ≥ r.
- **Contraction.** The paper's proof of prop:triangular-sde sets x_i = 0 where δ_i = 0 and never
  uses full support. Each round realizes ζv + U for every ζ ∈ F_p^*, with weights in P ∪ {0}.
- **Termination.** The round stops with the weight α_0 + β_0 = 1 on the scaled entry. Supports
  are disjoint, and back substitution works unchanged.
- **Recursion and sum.**
  w_l ≤ (1−1/p)(l + r) + (l + r)/(p^r − 1) ≤ (1−1/p)l + 2r + 2, because p^r − 1 ≥ l and r ≤ l.
  Then m_a ≤ (1−1/p)a(a+1)/2 + Σ(2r + 2) + O(a) = (1−1/p)a²/2 + O(a log a), uniformly in p.
- **Scope.** The bound holds in the worst case, with no general position.

## E. Lemma Z (checked)

- **Normalisation.** Φ = y_1 gives γ_1 = 0.
- **The α = 2 realizer.** y_2 = 2Φ + ⟨γ_2, ℓ⟩ ∈ {0, 1}. Hence ⟨γ_2, ℓ⟩ ∈ {0, 1} when Φ = 0 and
  ⟨γ_2, ℓ⟩ ∈ {−2, −1} when Φ = 1.
- **Φ ≡ 0 is excluded.** Then every y_α is linear and {0,1}-valued on the nested set, hence 0,
  which is degenerate. So γ_2 ≠ 0.
- **Infeasibility.** The value count of Finding 6 rules out the nested and full sets for every
  k and every p ≥ 5. Correct.

## Re-verified (in `2026-11-09-rees-sde-fq-nest-referee-C/`)

| script | output | result |
|---|---|---|
| `free_cnf.py` (encoding without Lemma Q, optionally without R) | `free_p7_k2.out`, `free_p7_k2_noR.out`, `free_p7_k3kappa.out`, `free_interval.out` | p = 7 κ = 2 nested and all: 38/38 UNSAT, LRAT (re-verified with the fixed checker, 9 Nov). Without R: 19/19 UNSAT. κ = 3 unsplit: UNSAT. Interval k = 1 at q = 11, 13: UNSAT. p = 5 nested: SAT (model checked). |
| `lemma_n_check.py` | `lemma_n_check.out` | Lemma N equivalence on 120 feasible models, 0 violations. The p = 11 run was stopped and not tested. |
| `orbit_k.py` | `orbit_k.out` | Lemma U and the k ≥ 3 covers complete. |
| `split_coverage.py` | `split_coverage.out` | All three split files are exact covers, all LRAT-verified [9 Nov: by the unsound build; CaDiCaL UNSAT, not independently proof-checked (checker was unsound, 9 Nov)]. |
| `contraction_check.py` | `contraction_check.out` | Contraction exists at κ = 2, 3 for every p < 1000. |
| gadget_cnf5 re-runs | `rerun_k3_7.out` | Matching sha256; Lemma U forced case UNSAT. |

## Claims I consider proved

1. **Theorem C.** Let κ = 2 and p odd, or κ = 3 and p ≡ 1 (mod 3) (the latter assuming the
   paper's E_2(3) = ∅). Then every instance in F_p^a with
   m ≥ (1−1/p)a²/2 + O(a log a) columns (the explicit recursion m_a) has a nonzero
   (P ∪ {0})-solution, found by an algorithm that is deterministic given g and (α, β) and runs
   in poly(a, log p) time. This holds in the worst case.
2. **Lemmas 2, R, N and Q (Q for S = P ∪ {0}), and Lemma U with its 3p − 2 cases for all p.**
   The two-case first-slot cover holds for every k ≥ 2.
3. **The obstruction, as a property of label sets.** For S = P ∪ {0} at (p, κ) = (7, 2), (7, 3),
   (11, 2) and (13, 2), and at k = 3 for (7, 2): no 2-dimensional realization with weak
   nondegeneracy exists for any column multiset whose label set contains the nested set. This
   rests on the LRAT-verified split runs plus Lemmas R, N, Q, U; the p = 7 cells are also
   confirmed without Lemma Q. [9 Nov: the split runs for (11, 2), (13, 2) and k = 3 at (7, 2) are CaDiCaL
   UNSAT, not independently proof-checked (checker was unsound, 9 Nov). Re-verified with the fixed
   checker: the p = 7, k = 2 cells (this report's runs and the (7, 2) unsplit run); the k = 3 cell at
   (7, 2), given the two-case first-slot cover, and the (11, 2) cell, given Lemma U's 31 cases, by
   solving each case as one CNF (`2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`,
   `cases11_cases.out`, `cases11_c10.out`). (13, 2) is not re-verified.]
   - Hence a piece with dim D(X) = 2 and full nested patterns gains no plane and has no witness.
   - This is not an algorithmic lower bound, and not a proof that the k = 2 framework fails on
     some instance.
4. **Lemma Z.**

Not proved: the (b) q = 11 nested cell (Finding 2), and the κ = 3, p = 13 cells (no certificate).
