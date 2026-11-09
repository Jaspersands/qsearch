# Check of the class-seven Rees Lean modules, and integration (I217)

AI-only check, 2026-11-05. Independent checker and integrator. The object is
`2026-11-05-rees-lean-c7.md`, its folder `2026-11-05-rees-lean-c7/`, and the modules
`formal/Formal/BCHClassSeven.lean`, `BCHClassSevenSubgroups.lean` and
`ReesGeneralLawClassSeven.lean`, together with their wiring. Nothing was committed.
There was no network access and no full `lake build` (another agent was building
`ReesSdeSolver`). Claim gates were not touched, and `formal_compiler_checked` stays
false. Every Lean statement below is machine-checked in Lean, AI-run, and pending human
review.

**Verdict: no Error, no Gap.** Three Imprecisions were found, none of them in the Lean
content (§6). The report's §7 replacement texts were applied to `main.tex`, and the
matching Lean-boundary change was made in `core/main-core.tex` (§7).

## 1. Statement fidelity

I read the main statements directly in the source, and printed their elaborated types
with `#check`.

- **`BCHClassSeven.bch_assoc`.** The hypotheses are `lowerCentralSeries F L L 7 = ⊥`
  and `(2 : F) ≠ 0`, `(3 : F) ≠ 0`, `(5 : F) ≠ 0`, `(7 : F) ≠ 0`, with `F` an arbitrary
  field. The conclusion is associativity of `bch`. Mathlib's term 7 consists of brackets
  of length 8, so the bound means class at most 7, the same convention as class six
  (`... 6 = ⊥`). `instGroup` uses exactly this `bch`, with `one = 0` and `inv = neg`.
- **`BCHClassSevenSubgroups.toLieSubalgebra`.** It is stated for `ZMod p` under
  `[Fact p.Prime]` and `[NeZero 2/3/5/7]`, for an arbitrary `Subgroup (BCH ..)`. The
  carrier is `{x | BCH.mk x ∈ H}`. Closure under `+`, `•` and `⁅⁆` is derived from
  `addWord`, `powerScalar` and `bracketWord`, all of which are group words. Both round
  trips (`toSubgroup_toLieSubalgebra`, `toLieSubalgebra_toSubgroup`) are proved, so
  every subgroup is the image of a Lie subalgebra. `neZeroTwo` … `neZeroSeven`
  (`hp : 7 < p`) install the instances.
- **`ReesGeneralLawClassSeven`.**
  - `bchLaw : NilpotentGroupLaw F 7`, `bchLaw_additive` and `bchLaw_subgroups` are the
    three group-law hypotheses at `c = 7`.
  - `classSeven_tuple_hides_coeff` gives tuple hiding for an arbitrary `H` at
    `canonicalPoints p = 1..7`, with `hp : 7 < p`.
  - `classSeven_terminal_source` and `classSeven_measured_terminal_source` are stated
    for an arbitrary `H`. They start from stage 7, compose six measured stages, and end
    at the additive coset source of all of `h`.
  - The SDE policies (`policy`, `active`, `sde`) are explicit inputs, exactly as at
    class six.
  - A normalised diff against `ReesGeneralLawClassSix.lean` shows only the class-index
    substitutions and the added `NeZero 7`.

**Non-vacuity, instantiated in Lean** (scratch file
`$SCRATCH/c7check/C7Check.lean`, run with `lake env lean`). At `p = 11` with
`L = ZMod 11`, using the commutator Lie ring, which is abelian:

- `Fact (Nat.Prime 11)` holds, and the four `NeZero` instances come from
  `neZeroTwo … neZeroSeven (by norm_num)`.
- `hnil11 : lowerCentralSeries (ZMod 11) (ZMod 11) (ZMod 11) 7 = ⊥` is proved via
  `trivial_iff_lower_central_eq_bot` and antitonicity.
- `Group (BCH (ZMod 11) (ZMod 11) hnil11)` is found by `inferInstance`.
- `toSubgroup_toLieSubalgebra H` and `classSeven_terminal_source … hnil11 ⊤` are
  applied.
- `classSeven_tuple_hides_coeff` is applied with `f` constant and `H = ⊤`, and the
  `hides` hypothesis is discharged.

All of this compiled with no error. So neither the instance assumptions nor the class
bound is unsatisfiable. The policy hypotheses of the measured theorem are the same
inputs as at class six, and I did not re-instantiate them.

## 2. No sorry or axiom hacks; `#print axioms`

`grep -n "sorry|admit|^axiom| axiom |native_decide|implemented_by|extern|unsafe|opaque"`
finds nothing in the three files. The only `set_option`s are
`linter.unusedSimpArgs false` and `maxHeartbeats 0`; the class-six files use the same
ones.

The `.olean` files are newer than their sources. For example, `BCHClassSevenSubgroups`
was built at 04:05 and its source dates from 03:58; `Audit`/`Formal` were built at
04:08 and their sources date from 03:50. So `lake env lean` used current builds.

`#print axioms` from the scratch file (56 s, no rebuild):

- `bch_assoc`, `instGroup`, `toLieSubalgebra`, `val_bracketWord`, `val_addWord`,
  `toSubgroup_toLieSubalgebra`, `bchLaw`, `bchLaw_subgroups`,
  `classSeven_tuple_hides_arbitrary_subgroup`, `classSeven_tuple_hides_coeff`,
  `classSeven_step_output`, `classSeven_terminal_source` and
  `classSeven_measured_terminal_source` all give `[propext, Classical.choice, Quot.sound]`.
- `classSeven_of_lowerCentralSeries` gives `[propext, Quot.sound]` (from the Audit guard).

The 21 class-seven guards in `formal/Formal/Audit.lean` are the same set as the 21
module-local guards (sorted `diff`). There are no duplicate guards in `Audit.lean`.

## 3. Generators reproduce the Lean files

Both folders, `-lean-c7/` and `-lean-c6/`, were copied to scratch.
`gen_subgroups7.py` imports `rules2` from `../2026-11-05-rees-lean-c6`, so both are
needed. Each generator was run with an explicit output path into scratch:

- `gen_bch7_lean.py` writes 952 lines, and `cmp` finds them identical to
  `formal/Formal/BCHClassSeven.lean`.
- `gen_subgroups7.py` writes 4598 lines, and `cmp` finds them identical to
  `formal/Formal/BCHClassSevenSubgroups.lean`.

## 4. Independent BCH coefficient recomputation

I wrote my own script, `$SCRATCH/c7check/bchcheck/indep_bch7.py`. It does not reuse
the c7 scripts. It extracts `def bch` from the Lean file by regex and translates it
mechanically into Python (`(n : F)⁻¹ •` → `Q(1,n)*`, `⁅a, b⁆` → `br(a, b)`).

- **Free truncated associative algebra on `x, y`, words of length ≤ 7.** I compared the
  Lean text with `log(exp x exp y)` word by word. They are equal in degrees 1–7, with
  2, 2, 6, 4, 30, 28 and 126 words. Sample coefficients:

  | Word | Coefficient (series and Lean) |
  |---|---|
  | `xxxxxxy` | 1/30240 |
  | `yxxxxxx` | 1/30240 |
  | `xyyyyyy` | 1/30240 |
  | `xyxyxyx` | −1/140 |
  | `xxxyyyx` | −1/1512 |

  The 1/30240 coefficients agree with `B_6/6!`, which is also the coefficient of
  `ad_x^6 y` in `ad_x/(1−e^{−ad_x}) y`.
- **Exact rational 8×8 strictly upper triangular matrices**, 4 random pairs:
  `log(exp X exp Y)` equals the Lean `bch(X, Y)` exactly.
  - Generic superdiagonal entries make the corner entry injective on degree-7 words, so
    this test sees every degree-7 coefficient.
  - Negative control: changing one `1/1120` to `1/1121` is detected.
- **Denominators.** The degree-7 denominators are 1120, 2520, 5040, 10080 and 30240,
  and 30240 = 2^5·3^3·5·7, as the report says.
- **Word counts.** The Witt formula gives 312 three-letter words in degree 7, 116 in
  degree 6, and 18 two-letter words in degree 7. All three match the report.

I did not check the report's side finding about Sage's `bch_iterator`.

## 5. Guard count and split

- `grep -c "#print axioms" formal/Formal/Audit.lean` gives **509**.
- I counted the guards by namespace and compared each count with the 35 rows of
  `tab:lean-modules` before the edit, which sum to 450. Every row matched exactly.
- The class-seven namespaces add 8 + 8 + 5 = 21, so 450 + 21 = **471**.
- The unrelated guards come to **38**: 25 top-level `QSearch.*` lemmas, 9
  `BalancedSigned` and 4 `CrossCheck`.
- 471 + 38 = 509, which confirms the report's split.

## 6. Imprecisions (none affects the Lean content)

1. **Hazard: the generators write into the repository by default.** Without an
   argument, `gen_bch7_lean.py` and `gen_subgroups7.py` overwrite the live
   `formal/Formal/*.lean` files. Run them with an explicit output path.
2. **Reproducibility: `gen_subgroups7.py` needs the sibling class-six folder.** It
   reads `-lean-c6/rules2.py` through `sys.path`. The report's §1 does not say so.
3. **Not re-run here: the default `lake build --wfail` (3522 jobs).** The report's
   result was not repeated, because a full build was forbidden. The evidence is
   indirect: the oleans are fresher than their sources, and a file importing
   `Formal.ReesGeneralLawClassSeven` compiles cleanly. No clean-copy build exists, as
   the report states.

Also noted, not new: the class-six docstring in `ReesGeneralLawClassSix.lean` reads
"`p > 5`, i.e. `p > 6`".

## 7. Integration

Backups are in `$SCRATCH/c7check/backup/`. Every edit was an exact-string replacement
with its count asserted to be 1, and the file was re-read before each edit.

**`docs/papers/rees-hsp/main.tex`** (14 edits, §7 (a)–(g) of the report):

- **(a) Version note:** the class-six and class-seven modules, and both reports.
- **(b) Abstract:**
  - "class-three to class-seven … (class seven over $\mathbb{F}_p$ with $p \ge 11$)";
  - "$c \ge 8$".
- **(c) Build paragraph:**
  - the class-seven sentence inserted, with its 21 guards, the in-place `--wfail`
    build, no clean-copy build, and the label "machine-checked in Lean; AI-run, pending
    human review";
  - 450 → 471;
  - "class-six, class-seven and SDE modules";
  - 488 → 509;
  - the false README / not-imported / no-guards / no-report sentences deleted, with no
    trace sentence.
- **(d) `tab:lean-modules` Part 2:**
  - three rows inserted after `ReesGeneralLawClassSix`;
  - the `ReesGeneralMeasuredReceiver` row now reads "at $c=5$, $6$ and $7$";
  - Total 471.
- **(e) Boundary paragraph:**
  - "$c=3$, $4$, $5$, $6$ and $7$";
  - the class-seven sentence inserted. It describes the cross-check as "by exact
    computation (AI-run)", so that it is not read as Lean-checked;
  - "$c \ge 8$".
- **(f)** One clause added: "Lean states no class-seven instance of this receiver."
- **(g)** "$c\ge 8$".

**`core/main-core.tex`:**

- "discharged in Lean for $c = 3$, $4$, $5$, $6$ and $7$ (at $c = 7$ over $\Fp$ with
  $p \ge 11$)";
- "Outside … for $c \ge 8$".

This resolves referee-14 G8 (the README class-seven modules): they are now imported,
guarded, reported and in the table.

**Builds**, in scratch copies under `$TMPDIR/c7check-build-53737`, with
`latexmk -g -pdf`:

| Paper | Exit | Pages | Overfull | Undefined refs/cites | Float too large |
|---|---|---|---|---|---|
| full | 0 | 171 | 0 | none | none |
| core | 0 | 27 | 0 | none | none |

Part 2 of the table, all three new rows included, sits on page 170.

**Tests:**

- `tests/tools/test_rees_paper_numbers.py`: 2 passed.
- `tests/test_rees_circuit_round2.py`, the only test that reads `formal/Formal`: 20
  passed, 1 skipped.
- The `lean|formal|audit` test sweep: 1089 passed and 4 failed. Three of the failures
  are listed in `tests/KNOWN_FAILURES.txt`. The fourth,
  `test_native_refresh_crossover_scope_audit::test_independent_js_replays_all_current_audit_records`,
  rejects the 11-01 working-tree change to
  `research/reductions/native_refresh_lottery_crossover.json`. It is unrelated to this
  pass, and no registry file was modified.

`make_numbers.py` was not run.

**Other files:** item 8 of `research/REES_FULL_CONTINUATION.md` was updated, and row
I217 was added to `2026-11-02-rees-integration-log.md`.

## 8. Next

- A clean-copy `lake --no-cache build --wfail` of a copy of `formal/`. The acceptance
  test is the same 3522 jobs with no warning. Expect about 2 h for `BCHClassSeven`.
- Human review of the Lean statements against the paper.
