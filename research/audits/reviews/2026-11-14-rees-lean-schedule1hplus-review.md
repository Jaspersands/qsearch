# Hostile review of the Lean check of Schedule 1H⁺ (2026-11-14)

AI-checked (Claude, hostile reviewer), pending human review. Under review:
`formal/Formal/Schedule1HPlus/` (7 files, 2092 lines), the seven import lines added to
`formal/Formal.lean`, and the author's report
`research/audits/reviews/2026-11-14-rees-lean-schedule1hplus.md`, against
`docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus` (l. 785-1014; read only).
Precedent: `2026-11-13-rees-lean-schedule1h-review.md`.

## Verdict

**SOUND WITH FIXES.** Every main theorem says what the paper says, for correctness only (no
time, Las Vegas behaviour or determinism is modelled). No hypothesis is vacuous and none
assumes its conclusion: each one was satisfied on a concrete instance, and perturbed
instances are rejected. The fixes are documentation and one small missing glue lemma. No
paper statement was found false.

The author's weakest point is now closed. **All five tables of `prop:plus-tables` satisfy the
Lean `IsEllContraction`** (Definition `def:plus-ell`), checked by `decide +kernel` on the
Lean definition itself, through a reduction lemma proved here:

| table | level | file | status |
|---|---|---|---|
| `(13, 4)`, `B3_13_4.json` | 3 | `EllTable.lean` (`ell3_13_4`) | PROVED (Lean) |
| `(13, 6)`, `B3_13_6.json` | 3 | `EllCheck.lean` (`ell_136`) | PROVED (Lean) |
| `(19, 9)`, `B4_19.json` | 4 | `EllCheck19.lean` (`ell_19`) | PROVED (Lean) |
| `(37, 9)`, `B4_37.json` | 4 | `EllCheck37.lean` (`ell_37`) | PROVED (Lean) |
| `(73, 9)`, `B4_73.json` | 4 | `EllCheck73.lean` (`ell_73`) | PROVED (Lean) |

So candidate (e) of `def:plus-schedule` is non-vacuous in Lean at those pairs, and
`ellSolver_spec` gives a real `κ`-solver there (written out for `(13,4)`:
`ell3_13_4_solver`). What is still not checked in Lean: that `g` is the *least* primitive
root (only that it is a primitive root; the author's Python check covers "least").

Status of the probes: **PROVED (Lean; no `sorry`, no `native_decide`)**. Every probe
depends only on `[propext, Classical.choice, Quot.sound]`; `decide +kernel` adds no axiom
(it is checked by the kernel, not by `Lean.ofReduceBool`). See "Axioms and builds".

## 1. Statement fidelity, per main theorem

For each theorem: does the Lean statement say what the paper says, can its hypotheses be
satisfied, and is a wrong instance rejected?

| Lean theorem | paper | verdict | hypotheses satisfied on | rejected perturbation |
|---|---|---|---|---|
| `refine_spec` (Refine.lean:181) | `lem:plus-refine` | MATCHES | `tl6_chain_229` (author); `chainOK17` (two steps, here) | `chainOK17_bad` |
| `chain_spec` (Refine.lean:325) | `cor:plus-chain` | MATCHES (`⊇` in place of `=` for `Δ_t`, weaker hypothesis) | `chainOK17`: `(GE; (2,ℤ_2,{0}), (4,{0,2},{0}))` over `F_17` | `Δ_2 = {0}` rejected |
| `card_chainIdx` (Refine.lean:336) | arity of `cor:plus-chain` | MATCHES (exact) | `chain17_arity = (a+1)^3` | n/a |
| `card_chainIdx_le` (Refine.lean:349) | degree `e_0+L`, constant `K_0∏(|Δ_t|-1)` | MATCHES | needs `|Δ_t| ≥ 2`, as the paper | n/a |
| `plusStage_spec` (Stage.lean:106) | `lem:plus-stage` | MATCHES | via `step_spec` (Schedule 1H, reviewed) | n/a |
| `plusFinish_spec` (Stage.lean:133) | `lem:plus-finish` | MATCHES | `hfin` is satisfiable by choice (`mem_Tset_iff`) | n/a |
| `plusPlanF0_spec`, `plusPlanFK_spec` (Stage.lean:174, 195) | `def:plus-schedule`(f), run as in `thm:plus`(ii) | MATCHES, given a two-class node **on `Fin A`** (Finding 3) | not instantiated (as the author says) | n/a |
| `tensor_spec` (Tensor.lean:320) | `lem:plus-tensor` | MATCHES | unconditional | n/a |
| `ellNode_spec`, `ellSolver_spec` (Tensor.lean:350, 398) | `lem:plus-ell-node` | MATCHES | the five tables (above) | `*_scaled`, `ell3_13_4_pert` |
| `plus_sm_i` (SecondMoment.lean:295) | `lem:plus-sm`(i) | CONDITIONAL on the pair count `hN` (the Weil step), as the author says | `hN_trivial`: `hN` always holds with `γ_{ij} = |A_{ij}|` | n/a |

Details that I checked against the paper text:

- **Contraction (`IsRC`, Refine.lean:62).** `base : α_0+β_0 ∈ P_D` and
  `cond : ∀ i ∈ Δ, ∀ j, α_j+β_i = 0 ∨ cl_D(α_j+β_i)+i+j ∈ Ω`. This is `def:plus-rc`
  word for word. `0 ∈ Δ`, `0 ∈ Ω` and `D ≥ 2` are not fields. They are not needed:
  `refine_spec` derives `0 ∈ Δ` from `lift_D(Ω') ⊆ Δ` and the inner designated coefficient,
  and `0 ∈ Ω` then follows from `base` at `(i,j) = (0,0)`.
- **Refined weights (`refine`, Refine.lean:167).**
  `w_b = (α_0+β_0)^{-1} η_ν (α_{cl_D η_ν} + β_{cl_D c_b}) c_b`. This is the paper's
  formula, including the final scaling. When `η_ν c_b = 0` the product is `0`, whatever the
  junk value `cl_D(0)`. I checked every use of `cl` at a possibly zero argument (`refine`,
  `tensorStep`, `A0set`/`Aset`, `ellNode`): each one is multiplied by zero or guarded by
  `≠ 0`.
- **Union targets (`A0set`, `Aset`, SecondMoment.lean:245-250).** `A_{00} = Q_0`,
  `A_{0j} = {x : cl x + j ∈ Ω}`, `A_{ij} = {x : cl x + i + j ∈ Ω}`. This equals the paper's
  `⋃_{k∈Ω} Q_{k-i-j}`.
- **Classes (`ClassMap`, Classes.lean:36).** The probes show it is exactly the paper's `cl_D`:
  - `cl_eq_of_xi_eq`: two class maps with the same `ξ` agree on `Kˣ`;
  - `xi_not_mem_pow`: `ξ ∉ P_D` for every `1 < D ∣ N`;
  - `xi_of_classMap7`: over `F_7` with `N = 6`, `ξ ∈ {3, 5}`, the primitive roots;
  - `no_classMap_7_4`: no class map over `F_7` admits the modulus `4`.
- **`ξ^m` representatives.** `xiPow m = ξ^{m.val}` throughout. This is the paper's
  `z_m = ξ^m`, `m ∈ {0,…,κ-1}`. The author's Finding 1 stands. One addition, by hand and not
  in Lean: changing `ε` by a factor in `P` multiplies each entry of `c^{(j)}` by an element
  of `P`, so the sets `T_j`, and with them admissibility and `A^+_κ`, do not depend on the
  representative. Only the stored vectors `y` do.
- **Arity.** A node is a function on a fixed `Fintype ι`, with arity `|ι|`, for each space
  `V` (`a = finrank V`). This covers "for every `a ≥ 0`". `chainIdx` and `tIdx` give
  exactly `N_0∏((|Δ_t|-1)a+1)` and `M_ℓ(a)`.
- **`IsRel` (Refine.lean:52).**
  - The designated coefficient is required: `not_isRel_no_one` rejects `(2, 5)`.
  - Classes are checked: `not_isRel_class` rejects `(1, 6)` for `{0}` at modulus `2` over
    `F_7`, while `isRel_univ` accepts the same vector for `ℤ_2`.

## 2. The ℓ-level tables (the author's weakest point)

`ann_iff_check` (EllTable.lean) proves that condition (iii) of `def:plus-ell` is equivalent
to a finite condition: `∑_y C_y E(y,y') = 0` for every `y'`, where
`E(y,y') = ∏_r e(y_r, y'_r)` and `e(0,m) = -z_m`, `e(m,m) = 1` (`m ≠ 0`), else `0`. The key
lemma is `expand`: every family with the axis relations is `∑_{y'} X_{y'} E(·,y')`. It is
proved with the author's own `axis_zero_of_nz`. This is the remark after `def:plus-ell`,
which the author left unformalized.

`ann_iff_fullContr` (EllCheck.lean) is a faster checker of the same condition. It contracts
the table axis by axis with `x ↦ x_a - z_a x_0` (`sum_E_eq_fullContr`), so each `y'` costs
`2^ℓ` reads. `isEll_zero_iff'` turns `IsEllContraction C ℓ {0}` into three decidable
conditions:

- `C_y^h = 1` for every nonzero `C_y`;
- `C_0 ≠ 0` and `C_0^h = 1`;
- every full contraction at a `y'` with no zero coordinate vanishes.

The tables are read from `research/audits/reviews/2026-11-13-rees-k9-below-21/` (the files
that `v2/verify_ell.py` checks). They are stored as `B(y)` with `C_y = g^{y_1+…+y_ℓ}B(y)`, as
in the proof of `prop:plus-tables`, and transcribed by `gen_ell_lean.py`.

Negative controls (each must fail, and each does):

- `ell3_13_4_pert`: the stored perturbed table `B3_13_4_perturbed.json`;
- `*_scaled`: one nonzero entry multiplied by `3 = 2^4` (at `(13,4)`) or by `-1` (the
  others), a `κ`-th power in each case. This leaves conditions (i) and (ii) intact, and
  condition (iii) fails at an explicit `y'`.

## 3. Material findings

1. **Stale docstring: Tensor.lean:29-31.** It names a lemma `ann_iff_basis` "(condition
   (iii) is equivalent to vanishing on the product basis tensors)". No such lemma exists, and
   the author's report (l. 143) says the remark is NOT formalized.
   - Fix: delete the bullet, or move `ecoefz`, `Ecoefz`, `expand` and `ann_iff_check` from
     `Formal/Schedule1HPlusReview/EllTable.lean` into `Tensor.lean` under that name.
2. **The report understates what is checkable.** Several places say the tables were not
   checked in Lean:
   - report l. 43, l. 143, l. 145, Finding 5, and the self-check bullet "Vacuity of
     `ellNode_spec`";
   - Guards.lean:200-203: "the paper's level-3/4 tables are not checked in Lean".

   Fix: if the integrator adopts the probes, update the rows to "PROVED (Lean, `decide
   +kernel`, via `ann_iff_check`/`ann_iff_fullContr`)" for the tables checked, and keep "the
   least primitive root" as Python-checked only.
3. **Missing glue: the plan theorems take nodes on `Fin A`.** These are `plusPlanF0_spec`
   and `plusPlanFK_spec` (Stage.lean:174-176, 195-202, `nd : (Fin A → V) → Fin A → K`).
   - Chain nodes are indexed by `chainIdx` and ℓ-level nodes by `tIdx`, so the candidates
     (f2) and (f3), and a chain or table node used as `𝒦`, do not plug in directly.
   - The report row for `def:plus-schedule`(f) says "Any two-class node", which is true only
     up to reindexing.
   - Fix: add the review's `isNode_reindex` (Probes.lean; 8 lines, along any
     `ι' ≃ ι`, e.g. `Fintype.equivFin`) and `isRel_mono` (a `{0}`-node is a `{0,m}`-node)
     to `Refine.lean`, and reword the row.
4. **Modelling note: one fixed dependence.** This affects `refine` (Refine.lean:166),
   `tensorStep` (Tensor.lean:181) and `gauss` (Refine.lean:122).
   - Each uses the particular `normalize (depOf ·)` chosen by `Classical.choice`. So
     `refine_spec` and `tensor_spec` are proved for that one `η`/`θ`. The paper says "let
     `η` be nonzero with…", that is, for any dependence.
   - The proofs only use `depOf_spec`/`normalize_spec`, so the statements are true for any
     choice, but as written they do not cover an implementation that uses a different
     elimination.
   - Fix (optional): take the dependence as a parameter `dep` with hypothesis
     `card β > finrank W → dep vs ≠ 0 ∧ ∑ dep vs ν • vs ν = 0`. Or state this limitation in
     the report's modelling choice 5, which currently says only "Correctness does not depend
     on which dependence is chosen".
5. **`plus_sm_i` (SecondMoment.lean:295) is correctly labelled CONDITIONAL.** The hypothesis
   `hN` is not vacuous (`hN_trivial`). But nothing in Lean connects the theorem to the
   paper's `γ`, `μ_0`, `μ_1`, `Φ(p)` or to Table `tab:plus-thresholds`. I agree with the
   author's caveat: it must not be cited for `Φ < 1`.
6. **Minor.** The guards instantiate `ClassMap` with `N = p-1`, not the paper's
   `N_p = gcd(p-1, 2520)`. This is harmless: `ClassMap.restrict` covers divisors. As the
   author says, there is no instance for a non-primitive coset generator.

I re-read the author's Findings 1-4 on the paper and agree with them. On Finding 3, the
artifact path:

- The five ℓ-level tables are cited with their correct folder (`app:artifacts`, l. 1388:
  `2026-11-13-rees-k9-below-21/`).
- The ambiguity concerns only the certificate tables. Those are in
  `2026-11-13-rees-headline-below-38/`, not in the merged draft folder.

## 4. Axioms and builds

Everything below was run from `formal/` with `nice -n 19`, one heavy process at a time.

**The files under review.**

- `grep` finds no `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`,
  `implemented_by` or `extern` in `formal/Formal/Schedule1HPlus/`. The only hits are in
  comments.
- I re-elaborated each of the seven files from source with `lake env lean`
  (`Formal/Schedule1HPlus/<File>.lean`, in import order). Every one exited with 0 and no
  errors, and each peaked at 2.2-2.3 GB.
- This includes the author's `Audit.lean`, whose 52 `#guard_msgs`/`#print axioms` checks
  all pass.
- My own `#print axioms` for the 18 main declarations (`refine_spec` … `plus_sm_i`, the
  guards, `ell1_contraction`, `isRC_zero_iff_check`) gives
  `[propext, Classical.choice, Quot.sound]` for each.
- Log:
  `research/audits/reviews/2026-11-14-rees-lean-schedule1hplus-review/reelaborate_and_full_build.log`.
  Axiom output: `…/print_axioms_main.txt`.

**`lake build Formal`.** `Build completed successfully (9138 jobs)`, exit 0, peak
0.79 GB. The build was up to date, so it replayed the author's build. With the
re-elaboration above, that covers the seven files.

**The `formal/Formal.lean` edit.** I read the diff. Exactly seven lines,
`import Formal.Schedule1HPlus.{Classes,Refine,Stage,Tensor,SecondMoment,Guards,Audit}`, are
inserted after `Formal.Schedule1H.Audit` and before `Formal.Audit`. Nothing else changed.

**The probes.** These are new files, not imported by `Formal.lean`, in
`formal/Formal/Schedule1HPlusReview/`:

| file | contents |
|---|---|
| `EllTable.lean` | `ecoefz`, `Ecoefz`, `axisRel_E`, `expand`, `ann_iff_check`, `isEll_zero_iff`; the class map `C13` (`ξ = 2`); the `(13,4)` table, its two negative controls, and `ell3_13_4_solver` |
| `EllCheck.lean` (generated) | `contr1`, `fullContr`, `sum_pi_succ`, `sum_axis`, `sum_E_eq_fullContr`, `ann_iff_fullContr`, `isEll_zero_iff'`, `forall_fin3/4`; the `(13,6)` table and its control |
| `EllCheck19.lean`, `EllCheck37.lean`, `EllCheck73.lean` (generated) | class maps `C19`, `C37`, `C73` (`ξ = 2, 2, 5`, primitive roots proved by `decide`); the level-4 table split into 9 class lemmas and 64 contraction lemmas; the main theorem and its control |
| `Probes.lean` | class-map probes, `IsRel` probes, `isNode_reindex`, `isRel_mono`, `hN_trivial`, and the two-step chain over `F_17` |
| `Audit.lean` | `#guard_msgs` + `#print axioms` for 25 probe declarations |

Build, one module at a time:

```
nice -n 19 ~/.elan/bin/lake build Formal.Schedule1HPlusReview.<M>
```

with `<M>` = `EllTable`, `EllCheck`, `Probes`, `EllCheck19`, `EllCheck37`, `EllCheck73`, then
`Audit`. Each ended with `Build completed successfully`. Timings and peaks:

| module | time | peak |
|---|---|---|
| `EllCheck19` | 88 s | 2.72 GB |
| `EllCheck37` | 90 s | 2.69 GB |
| `EllCheck73` | 90 s | 2.71 GB |
| `Probes` | 5 s | 2.26 GB |
| `Audit` | 1.8 s | 2.21 GB |

`Audit` built with ✔, so all 25 `#guard_msgs` match `[propext, Classical.choice,
Quot.sound]`.

Do **not** run `lake build Formal.Schedule1HPlusReview.Audit` on a fresh tree without the
earlier modules built. Lake may then build the three level-4 files in parallel, at about
2.7 GB each.

Supporting files are in
`research/audits/reviews/2026-11-14-rees-lean-schedule1hplus-review/`:

- `gen_ell_lean.py`, the table transcriber;
- `search_two_step.py` and `.out`, the exhaustive search for the `F_17` chain;
- `watch_run.sh`, the memory watchdog;
- the build logs and the `print_axioms_*.txt` outputs.

## Adversarial self-check

- **Is `decide +kernel` trustworthy here?** It asks the kernel to reduce the `Decidable`
  instance to `true`. It adds no axiom (`#print axioms` above), unlike `native_decide`.
  Evidence that the checks are not trivially true:
  - every negative control is *proved false* by the same procedure;
  - my own transcription error was caught. The first version of `chainOK17` used the
    `p = 5` certificate `α = (1,0)` at `p = 17`, and `decide` reported the IsRC condition
    false. With the correct `α = (2,0)` from `search_two_step.out` it passes.
- **Is the check about the Lean definition, or about a mirror of it?** It is about the
  definition. `ann_iff_check` and `ann_iff_fullContr` are Lean theorems with
  `IsEllContraction`'s condition (iii) on one side. `isEll_zero_iff'` rewrites the whole
  structure. No unverified Boolean function stands in between.
- **Transcription of the tables.** `gen_ell_lean.py` writes `B(y)` nested by the digits
  `y_1, y_2, …` and reads it as `B[y 0][y 1]…`. This is the convention of the paper and of
  `v2/verify_ell.py`.
  - Weakness: the axis relations are symmetric under permuting axes, so a table transposed
    by mistake would still pass. The check would then concern a permuted table, not the
    stored file. I read the generator to exclude this. A wrong value, or a wrong base `g`,
    would fail (compare the `*_scaled` controls).
- **"Least" primitive root.** Lean proves that `g = 2, 2, 2, 2, 5` are primitive roots of
  `13, 19, 37, 73` and uses them as `ξ`. It does not prove that they are the least ones.
  That rests on the author's Python check (`least_primitive_root_check.py`).
- **What "SOUND" covers.** It covers correctness only, for each candidate type. The recursive
  `𝓗⁺_κ`, the minimum over candidates, `thm:plus`(i), (iii) and (iv), the thresholds, and the
  exponent 20 are not formalized. The finite checks prove availability at those primes
  only, and nothing asymptotic.
- **Fidelity was judged by reading.** I compared each definition with the paper line by line
  and probed it on concrete instances. A mismatch outside the probed instances could remain.
  - The weakest remaining spots are the plan theorems. No full plan was instantiated; the
    author did not instantiate one either.
  - `cTyp`/`Tset` I took from the Schedule 1H review rather than re-deriving them.
- **Statement strength of `refine_spec`/`tensor_spec`** (Finding 4). These are statements
  about one chosen dependence. I did not formalize the "for every dependence" version. I
  believe it holds by the same proof, but that is UNKNOWN in Lean.
- **Resource rule violations (reported, not hidden).**
  - A first version of the `(13,6)` check, which summed naively over all `216 × 216` pairs,
    peaked at **5.9 GB** (`/usr/bin/time -l`). That is above the 4 GB Lean cap. It ran for
    5.7 minutes and was not killed, because I measured it only afterwards.
  - A 15-second test of one level-4 sub-lemma peaked at **4.5 GB**. My watchdog's process
    pattern missed it.
  - Two combined level-4 runs were killed by the watchdog at 4.04 GB and 4.15 GB.
  - The final files split the work into per-`(a, b)` lemmas and peak at **2.73 GB** or less.
- **Not done.** No `#print axioms` sweep beyond the author's 52 declarations and my probes.
  The full build was rerun once (above), not from a clean `.lake`.
