# Interval S in the F_q nest problem: Lemma Q is exact for every S ≠ F_p; the q = 11 and q = 13 cells are UNSAT for the free problem

AI-only pass, 11 November 2026, one Claude Code subagent; not human-reviewed; no novelty claim.

Inputs:
- `2026-11-08-rees-sde-fq-nest.md`: §0 item 4; §1 Lemmas 2, R, Q, N, U; the §2 table rows
  "(b) q = 11" and "(b) q = 13".
- `2026-11-09-rees-sde-fq-nest-referee-C.md`, finding 2.

Scripts and outputs are in `2026-11-11-rees-sde-interval-s/`. Tools:
- interpreter `/opt/anaconda3/bin/python -I`;
- CaDiCaL 3.0.1 with `--lrat=true --binary=false`;
- proofs are checked only by the fixed build `2026-11-09-lrat-checker-fix/lrat-check`, after its
  `controls.sh` passes (14/14) at the start of every batch.

Proofs were deleted after checking. No git, no network. The fq-nest note, STATE, the handoff,
the mechanical plan and the papers were not edited.

Labels:
- **[proved]** full proof here;
- **[exact]** complete finite computation with a named script: every UNSAT is LRAT-verified with
  the fixed checker, and every SAT model is re-checked by plain arithmetic;
- **[sampled]** falsification test only.

## 0. Verdict

1. **Lemma N′ [proved].**
   - Hypotheses: 0 ∈ S ⊆ F_p with S ≠ F_p; any spanning label set; any column multiplicities.
   - Claim: in every *feasible* (Φ, γ), direction [α] is degenerate iff γ_{λα} = λγ_α for all
     λ ∈ F_p^*. So weak nondegeneracy depends on γ alone.
   - It needs neither S ∩ rS = {0} (Lemma N) nor any condition on S-valued functionals.
2. **Lemma Q is exact for every S ≠ F_p [proved, Corollary Q′].**
   - For a P-closed spanning L, the free problem has a feasible weakly nondegenerate solution iff
     the P-equivariant problem has one. The free problem means one column per label with Φ
     unconstrained, or any column multiset with label set L.
   - So no small analogue can have a free solution without an equivariant counterpart. S = F_p is
     trivially SAT.
   - This closes referee C finding 2 mathematically. The old 581 s run (PicoSAT) had no
     certificate; it is now replaced by LRAT-verified runs (item 3).
3. **q = 11, S = {0,±1,±2}, k = 2, d = 2, labels F_11^*×F_11: no realization with weak
   nondegeneracy, free problem, any multiplicities [exact].** Each of the following is
   independently sufficient:
   - (a) **Free problem, no reduction lemma** (`int_cnf.py free`: Φ free on all 110 labels, γ free
     at all 118 non-unit α). CaDiCaL UNSAT in 760 s; LRAT VERIFIED with the fixed checker.
   - (b) **Lemma R only** (`int_cnf.py freeR`). UNSAT; LRAT VERIFIED.
   - (c) **The P-equivariant problem** (`gadget_cnf5.py`, the note's own encoder, and
     `int_cnf.py equi`). UNSAT; LRAT VERIFIED, both encoders. Corollary Q′ transfers this to the
     free problem.
   - (d) **A SAT-free check** (`rank1_decide_p11.py`). It uses Lemmas R and L and the uniqueness of
     f (§2). All 360,000 pairs of e1/e2 line data were checked: none extends to all 12
     directions, and at most 11 directions are ever consistent (positive control verified by plain
     arithmetic).
4. **q = 13, S = {0,±1,±2,±3}, k = 2, d = 2, labels F_13^*×F_13: same conclusion [exact, given
   the proved split].**
   - **Split.** Lemma L confines the line data of every direction to a set A. A is computed by
     three independent enumerations: 9576 elements, all of rank one, in 26 orbits under
     Aut(L) × rebasing.
   - **Cases.** Each case fixes the five e1 slots to one orbit representative. The coverage check,
     run through the lifted symmetries, reaches 9576/9576 with 0 outside A.
   - **Run 1, equivariant, 26 cases:** all UNSAT, LRAT VERIFIED; 1224 s solving in total, at most
     88 s per case. Corollary Q′ transfers it to the free problem.
   - **Run 2, Lemma R only, 26 cases plus the zero-data case:** all 27 UNSAT, LRAT VERIFIED;
     2900 s. This needs neither Lemma N′ nor Q′.
   - **Cost.** The split costs ≈ 0.4 core-hours (run 1) or 0.85 (run 2), against the note's
     "> 28561 × 9 min".
5. **Consequence for the fq-nest note's §2 table, row (b), column "k=2, d=2 nest" [for the
   integrator; that note was not edited here].**
   - q = 11 can read UNSAT for the free problem, LRAT-verified; the "P-equivariant problem only"
     qualifier can be dropped.
   - q = 13 can read UNSAT, LRAT-verified, via the e1-line-data split (no longer "open").
   - Both remain properties of this label set: referee C finding 3 applies unchanged. Neither is
     an algorithmic lower bound.
6. **CPU used.** About 2.3 core-hours in all, at `nice -n 19` with at most 3 solver processes of
   this pass at a time. The solver runs above total ≈ 1.9 core-hours; the rest is enumerations,
   coverage and the falsification tests.

## 1. Lemma N′ and Corollary Q′

The setting is that of the fq-nest note, Lemma 2.
- Columns i carry labels ℓ_i in a spanning set L ⊆ F_p^k.
- A candidate is (Φ, γ) with Φ_i ∈ S^2 and γ_α ∈ F_p^k for α ∈ F_p^2∖0. Put
  y_α(i) = ⟨α, Φ_i⟩ + ⟨γ_α, ℓ_i⟩.
- The candidate is *feasible* if every y_α(i) ∈ S.
- A direction [α] is *degenerate* if y_{λα} ≡ 0 for all λ ∈ F_p^*. *Weakly nondegenerate* means
  that no direction is degenerate.
- P = {ν : νS = S}.

**Lemma N′ [proved].** Let 0 ∈ S ≠ F_p. In every feasible (Φ, γ), [α] is degenerate iff
γ_{λα} = λγ_α for all λ ∈ F_p^*.

*Proof.* For all λ and i,
y_{λα}(i) − λ y_α(i) = ⟨γ_{λα} − λγ_α, ℓ_i⟩. (∗)

(⇒) If [α] is degenerate, the left side of (∗) is 0 for every i. The ℓ_i span F_p^k, so
γ_{λα} = λγ_α.

(⇐) If γ_{λα} = λγ_α for all λ, then (∗) gives y_{λα}(i) = λ y_α(i), which lies in S for all
λ ∈ F_p^* by feasibility. If y_α(i) ≠ 0, the values λ y_α(i) exhaust F_p^*, so S ⊇ F_p^* and
S = F_p, which is excluded. Hence y_α ≡ 0, and so y_{λα} = λ y_α ≡ 0 for every λ. ∎

Lemma N (fq-nest note) has a single-r criterion, which needs S ∩ rS = {0}. Lemma N′ uses the whole
line, and that is all the reduction needs.

Referee C remarked that a free solution can have W = {0} while every equivariant selection has W
equal to a line. Two feasible solutions with the same γ cannot differ in this way: by Lemma N′
they have the same degenerate directions.

**Corollary Q′ [proved].** Let 0 ∈ S ≠ F_p, and let L be spanning and P-closed. The following are
equivalent:
- (i) the free problem (one column per label, Φ arbitrary) has a feasible weakly nondegenerate
  solution;
- (ii) some column multiset with label set L has one;
- (iii) the P-equivariant problem has one: Φ(νℓ) = νΦ(ℓ) and γ_{να} = νγ_α for ν ∈ P, with
  γ_{e_1} = γ_{e_2} = 0. This is what `gadget_cnf5.py` and `int_cnf.py equi` encode.

*Proof.*
- (iii) ⇒ (i) is trivial.
- (i) ⇔ (ii). Given a solution for a multiset, keep one column per label. This stays feasible, and
  by Lemma N′ its nondegeneracy depends only on γ, which is unchanged. Conversely, copy Φ onto all
  columns that share a label.
- (i) ⇒ (iii), first step. Lemma R (fq-nest note §1, proof by referee B; it uses only νS = S for
  ν ∈ P) yields a feasible weakly nondegenerate solution whose γ is P-equivariant and normalised.
- Second step. Choose one representative ℓ_o in each P-orbit of L and put Φ′(νℓ_o) := νΦ(ℓ_o).
  This is well defined, because νℓ_o = ν′ℓ_o with ν ≠ ν′ forces ℓ_o = 0. Then
  y′_α(νℓ_o) = ν y_α(ℓ_o) ∈ νS = S, so (Φ′, γ) is feasible.
- Third step. Let [α] be nondegenerate for (Φ, γ). By Lemma N′ (⇐) for (Φ, γ), γ is not linear on
  [α]. So by Lemma N′ (⇒) for (Φ′, γ), [α] is not degenerate for (Φ′, γ). ∎

For S = {−K..K} with 2 ≤ 2K < p − 1, P = {±1}; `int_cnf.stabiliser` confirms this for (11, 2) and
(13, 3).

**Falsification checks [sampled]** (`lemma_nprime_check.py`; outputs `lemma_nprime_check.out`,
and `lemma_nprime_check_B11.out` for the p = 11 rerun of test B):
- **A.** Free models (no R, no Q, no nondegeneracy) were sampled for 11 sets S ≠ F_p at
  p = 7, 11, 13. In 70% of the draws a random line was forced to be γ-linear. Over all
  directions, "degenerate" and "γ-linear" always agreed: 0 violations, 49 degenerate directions
  met.
- **B.** Random P-closed spanning label sets: 200 at p = 7 over 8 sets S, and 6 at p = 11 with
  {0,±1,±2}. The free verdict (no R, no Q, original nondegeneracy) equalled the equivariant one
  every time.
- **Encoders.** `encoding_crosscheck.py` → `.out`. Five encoders were run on the same random
  P-closed label sets: int_cnf equi, freeR and free, gadget_cnf5, and free_cnf.
  - p = 7, S = {0,±1}: 15 random sets plus the nested set. Verdicts 6 SAT and 10 UNSAT (nested
    UNSAT); all five encoders agree on all 16.
  - p = 7, S = {0,±1,±2}: 6 random sets plus the nested set. All SAT; all five agree.
  - The run was stopped during p = 7, S = {0,1,2,4}, after one CaDiCaL call ran 8+ minutes; this
    was a time-budget stop, not a disagreement. The p = 11 sets were not reached.
  - p = 11 test B was likewise stopped during S = {0,±1,±3}, after S = {0,±1,±2} had finished.

## 2. q = 11

**Encoder.** `int_cnf.py` is new, written independently of `gadget_cnf5.py` and `free_cnf.py`.
- One at-least-one group per label (Φ(ℓ) ∈ S^2) and one per γ slot (F_p^2).
- Auxiliaries T[D,ℓ,t] ⇐ ⟨D,Φ(ℓ)⟩ = t and U[s,ℓ,u] ⇐ ⟨γ_s,ℓ⟩ = u.
- A binary clause ¬T ∨ ¬U whenever λt + u ∉ S, at slot s = (D, λ).
- The original weak nondegeneracy, through NZ[s,ℓ] variables; never the Lemma N′ criterion.
- Without at-most-one clauses the encoding stays sound. Every clause is an implication from each
  true value, so every true value decodes to a solution, and every solution gives a model.
- Every SAT model is decoded and checked by `check_solution` (all α, all labels, all directions,
  plus normalisation).

| run | assumes | vars / clauses | CaDiCaL | proof (fixed lrat-check) | CNF sha256 |
|---|---|---|---|---|---|
| `int_cnf.py 11 int:2 nest free` | nothing | 187528 / 2604820 | UNSAT 760.5 s | 969 MB, VERIFIED, 24 s | 0a46f0f0…3503 |
| `int_cnf.py 11 int:2 nest freeR` | Lemma R | 101068 / 1297960 | UNSAT 292.0 s | 652 MB, VERIFIED, 16 s | 88fa13b2…7d6c |
| `int_cnf.py 11 int:2 nest equi` | R, Q | 54043 / 649015 | UNSAT 216.1 s | 645 MB, VERIFIED, 14 s | 1df8fe9f…9b37 |
| `gadget_cnf5.py 11 int:2 2 2 nest` | R, Q | 11693 / 6579005 | UNSAT 398.7 s | 2.80 GB, VERIFIED, 45 s | 6e2bbf5d…373e |

Outputs: `c11_free.out`, `c11_freeR.out`, `c11_equi.out`, `eq11_gadget_cnf5.out` (+ `.time`). Full
hashes are in `cnf_sha256.txt`, regenerated by `collect.py`.

**SAT-free check [exact]** (`rank1_decide_p11.py` → `.out`).
- **Uniqueness.** At p = 11, for every admissible line datum (§3: |A| = 600) and every label, the
  value f = y_D(ℓ) with r f + ⟨c_r, ℓ⟩ ∈ S (r = 2..5) is unique. The script asserts this. Hence
  y_D = G_{a_D} is determined by the line datum a_D of D.
- **Reformulation.** The free problem modulo Lemma R is therefore equivalent to: choose a_D ∈ A for
  all 12 directions with G_{a_{(1,d)}} − G_{a_{e1}} − d·G_{a_{e2}} ∈ R|_L for d = 1..10.
  - (⇒) is Lemma L plus uniqueness.
  - (⇐) Set Φ = (G_{a_{e1}}, G_{a_{e2}}), let γ_D be the linear functional, and put
    γ_{rD} = rγ_D + c_r(D). This is feasible, and nondegenerate because a_D ≠ 0.
- **Result.** All 600² pairs (a_{e1}, a_{e2}) were tried, with no symmetry used: 0 pairs work for
  every d. At most 9 of the 10 d's match.
- **Positive control.** The pair (A[0], A[0]) matches d = 1..9. The partial solution it gives on
  11 of the 12 directions passes plain arithmetic over all λ and labels.

## 3. q = 13: an exact symmetry split by line data

**Line data.** Let (Φ, γ) be feasible with γ P-equivariant (P = {±1}); Φ need not be equivariant.
For a direction D (representative with leading coordinate 1) put c_λ := γ_{λD} − λγ_D.
- Then c_1 = 0 and c_{−λ} = −c_λ.
- The data are c_r = (u_r, v_r) for r = 2..m, m = (p−1)/2, and ⟨c_r, (a,b)⟩ = u_r a + v_r b.
- Define T := {t ∈ F_p^{m−1} : ∃ f ∈ S, t_r + r f ∈ S for r = 2..m} and
  T* := {t : at ∈ T for all a ≠ 0}.

**Lemma L [proved].** For L = F_p^*×F_p and every direction D, u + bv ∈ T* for all b ∈ F_p. If the
solution is weakly nondegenerate, then (u, v) ≠ 0.

*Proof.* For ℓ ∈ L let f := y_D(ℓ) ∈ S. Then y_{rD}(ℓ) = r f + ⟨c_r, ℓ⟩ ∈ S, so
(⟨c_r, ℓ⟩)_r ∈ T. For a ≠ 0 the label (a, ab) lies in L and gives a(u + bv) ∈ T. If (u, v) = 0,
then all c_λ = 0, γ is linear on [D], and Lemma N′ makes [D] degenerate. ∎

Run 2 below does not use the second sentence: it includes the zero datum as a case.

**The admissible set A** (`linedata.py` → `linedata_p{11,13}.out`, `.json`; `coverage_e1.py`
part (a)) comes from three independent enumerations, which agree:
- (1) brute force over T* × F_p^{m−1};
- (2) rank ≤ 1 data plus projective lines with ≥ p points of Q = P(T*∖0);
- (3) v ∈ T* − u.

| p, S | \|T\| | \|T*\| | \|Q\| | lines with ≥ p points of Q | \|A\| | orbits |
|---|---|---|---|---|---|---|
| 11, {0,±1,±2} | 3125 of 11^4 | 51 | 5 | 0 | 600 | 2 |
| 13, {0,±1,±2,±3} | 113329 of 13^5 | 685 | 57 | 0 | 9576 | 26 |

Hence every admissible datum is rank one, c_r = t_r w with t ∈ T*∖0 and w ∈ F_p^2∖0 [exact at
p = 11, 13]; 9576 = 684·168/12. The orbits are taken under the group generated by:
- Aut(L) ∋ σ(a,b) = (λa, μb + νa), acting as (u, v) ↦ (λu + νv, μv);
- rebasing ρ_s: t ↦ (t_{rs} − r t_s)_r.

The 26 orbits are 13 Q-orbits under rebasing, times whether w_b = 0. At p = 13 the f of the
uniqueness step is not always unique (576 of 8892 pairs (t, x) allow two values), so the SAT-free
check of §2 does not carry over.

**Symmetries [proved].** Both families below map feasible weakly nondegenerate normalised
solutions with P-equivariant γ to solutions of the same kind. They also preserve label
equivariance of Φ when it holds, so they act on both the freeR and the equi problem.

- **Label side**, σ ∈ Aut(L): Φ′(ℓ) := Φ(σℓ), γ′_α := σ^Tγ_α.
  - Then y′_α = y_α ∘ σ, with σ a linear bijection of L, so y′ stays S-valued.
  - y′_{λα} ≢ 0 iff y_{λα} ≢ 0.
  - Normalisation and oddness are kept.
- **α side**, A ∈ GL_2(F_p): Φ′ := (y_{Ae_1}, y_{Ae_2}) ∈ S^2 and
  γ′_α := γ_{Aα} − α_1γ_{Ae_1} − α_2γ_{Ae_2}.
  - Expanding gives ⟨α,Φ′(ℓ)⟩ + ⟨γ′_α,ℓ⟩ = y_{Aα}(ℓ), which is S-valued.
  - γ′_{e_j} = 0, and γ′ is odd.
  - If Φ is odd in ℓ, so is Φ′.
  - A permutes the directions, so nondegeneracy is kept.

On e1 line data, σ acts as above and A = diag(s, 1) acts as ρ_s. Checks in `coverage_e1.py`:
- Part (b): on 40 SAT models of the solvable cells p = 5 {0,±1} and p = 7 {0,±1,±2}, 1200
  random group elements; every image passes `check_solution` and stays equivariant.

**Case split and coverage.**
- `cases_e1_p13.txt` has 26 lines; case j fixes γ at the slots (e1, r), r = 2..6, to the j-th orbit
  representative. `cases_e1_p13_with0.txt` adds the zero datum.
- `coverage_e1.py` part (c) closes the representatives under the four generators, acting through
  the lifted actions on a full γ. It reaches exactly A: 9576/9576, 0 outside
  (`coverage_e1_p13.out`, "COVERAGE OK"; p = 11: 600/600, `coverage_e1_p11.out`).
- The zero datum is fixed by every linear action.
- Conclusion: by Lemma L, some symmetry maps every solution to one that satisfies a case. If every
  case is UNSAT, there is no solution.

**Runs** (one CNF per case; per-case verdict, times, proof size, check and CNF sha256 in the .out
files and `cnf_sha256.txt`):

| run | mode | cases | vars / clauses per case | CaDiCaL | proofs (fixed lrat-check) |
|---|---|---|---|---|---|
| `run_cases.sh 13 int:3 cases_e1_p13.txt 2 cases_e1_p13.out` | equi | 26 | 121576 / 1717739 | 26/26 UNSAT, 22.9–87.8 s each, 1224 s total | 26/26 VERIFIED, ≤ 128 MB, 64 s total |
| `run_cases_mode.sh 13 int:3 cases_e1zero_p13.txt 1 cases_e1zero_p13_equi.out equi` | equi | zero datum | 121576 / 1717739 | UNSAT 2.1 s | VERIFIED |
| `run_cases_mode.sh 13 int:3 cases_e1_p13_with0.txt 3 cases_e1_p13_freeR.out freeR` | freeR | 26 + zero | 229294 / 3435377 | 27/27 UNSAT, 5.9–293.7 s each, 2900 s total | 27/27 VERIFIED, ≤ 194 MB, 109 s total |

A measurement before the runs, without proofs (`scratch_measure/`): cases 1 and 25 took 68 s and
34 s. The projected total was ≈ 0.5 core-hours, far under the 40-core-hour budget.

What each run needs:
- **Run 2 (freeR)** rests on Lemma R, the first sentence of Lemma L, the symmetry lemma, the
  computed A and the coverage check. It uses neither Lemma N′ nor Corollary Q′.
- **Run 1 (equi)** adds Corollary Q′, and through it Lemma N′.

## 4. What this shows and what it does not

- **Proved:**
  - Lemmas N′, L and Corollary Q′;
  - the two symmetry families;
  - the exactness of the e1-line-data split, given the A enumeration and the coverage
    computation.
- **Exact:** at q = 11 and q = 13 with S = {−⌊q/4⌋..⌊q/4⌋}, k = 2 and label set F_q^*×F_q, no
  realization of a 2-dimensional subgroup with weak nondegeneracy exists, for any column
  multiplicities. Hence by Lemma 2(B) a piece with dim D(X) = 2 whose labels contain the full
  nested set gains no plane and has no witness.
- **Not shown:**
  - label sets with missing patterns;
  - k ≥ 3;
  - q ≥ 17;
  - any lower bound for KOW-type small-coefficient subset sum. Referee C finding 3 (a property of
    label sets, not of instances) applies unchanged.
- **Gates that must stay false:**
  - "the k = 2 piece framework is closed for interval S" (argued only);
  - "this is an algorithmic lower bound";
  - "line data are rank one for every p" (exact at p = 11, 13 only);
  - "q = 13 SAT-free verified" (only q = 11 has the SAT-free check).
- **Next hard question.** The line data are rank one (c = t ⊗ w) at p = 11 and 13, and at p = 11
  y_D is a function of one linear form ⟨w_D, ℓ⟩. Is there a hand proof, for every q ≥ 11, that
  ridge functions G_{a_D}(⟨w_D,·⟩) cannot be linear in D modulo linear functionals? At p = 11 the
  best partial assignment satisfies 11 of the 12 directions.
- **Next command (q = 17, S = {0,…,±4}).** Run `/opt/anaconda3/bin/python -I linedata.py 17 4`,
  then `cases_e1.py 17 4`. Check that `coverage_e1.py 17 4 cases_e1_p17.txt` prints
  "COVERAGE OK". Measure one case with `int_cnf.py 17 int:4 nest equi --fix … --no-proof
  --timeout 1800`, then run `run_cases.sh`.
  - Acceptance: every line LRAT VERIFIED with the fixed checker, or a SAT model with
    "model_check": "OK".
  - The brute-force step (1) of `linedata.py` needs |T*| · 17^7 membership tests, so drop it there
    and keep enumerations (2) and (3).
