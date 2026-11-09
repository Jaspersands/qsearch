# Check of the composite-κ restart count (Rees Schedule 1, `rem:is-runtime`)

5 November 2026. Independent adversarial check and integration; AI only, overnight pass.
**AI-checked, pending human review.**

Object: `2026-11-05-rees-is-restarts-composite.md` (Theorems A and B, Lemmas 2–4, the
Corollary, Remark B.1, §8), its folder `2026-11-05-rees-is-restarts-composite/` and
`tests/test_rees_is_restarts_composite.py`. Context read: `main.tex` `thm:is-import`,
`rem:is-import`, `rem:is-runtime`; `theorems/rees_is_sde_solver.py` (all 650 lines); IS
arXiv:1503.09016v2 §3.1 (local copy in `2026-11-02-rees-linear-arity/lit/`, lines 405–434);
§1–2 of the prime-power note `2026-11-05-rees-is-restarts.md`.

## Verdict

**No Error. No Gap. Seven Imprecisions in the proposed sentence, all fixed in the text that was
integrated.** The ρ bound, both attainment constructions and the Corollary hold as stated.

## 1. What was checked by hand

- **Code-reading lemma (Lemma 3).** Confirmed against the code.
  - `is_sde_solve` computes the zero sum (`zero_sum_of_powers`) before the loop. That step
    builds its own `PiParts` and no `Classifier`. With `collapse=True` it also computes the
    anchor `_kernel_vector(reduced[:rank+1])`. Nothing else is classified before run 1.
  - `_accumulate(levels)` recurses into `children[0]` first. Level 0 returns the column
    unchanged. So the first computation is `theorem11` on columns [0, G), which calls
    `lemma12(level κ)`. Each `lemma12(level ≥ 2)` evaluates its children in index order and
    only then its own merge kernel. Level 1 classifies the kernel coefficients in index order,
    skipping zeros.
  - `_Found` is raised only after a whole `theorem11` call, so it cannot fire before any
    trigger on these families.
  - `Classifier.classify` raises `_Restart(γ)` exactly when `dlog` returns `None`, that is,
    when γ ∉ ⟨η⟩. The loop then sets η := `join(η, γ)`, runs the anchor test, and counts a
    restart only if the test fails. Runs = restarts + 1 whenever the loop is entered.
  - This matches IS §3.1, where η starts at 1, a failure replaces η by a generator of ⟨η, γ⟩,
    and they "restart the whole algorithm with these new data". `_row_reduce` is the
    identity when the first a columns are e₁, …, e_a, which holds for both families.
- **Lemma 2.** Checked the code's test (g = gcd(κ, |η|), all e_k ≡ e_{k₀} mod g) against
  ⟨η⟩^κ = ⟨η^g⟩, then reduced it componentwise to C_ℓ^{ℓ^{e_ℓ}} and to δ_ℓ ≤ max(c − e_ℓ, 0).
  Correct.
- **Theorem A.** The chain S₀ = H₁ ⊊ … ⊊ S_R has T failing at every S_i, so
  R ≤ Σ_ℓ (c_ℓ(S_R) − h_ℓ). Some ℓ* fails at S_R, which gives c_{ℓ*}(S_R) ≤ δ* + e* − 1 and
  δ* ≤ h*. Hence R ≤ e* − 1 + Σ_{ℓ≠ℓ*} ν_ℓ ≤ ρ − 1.
  - The identity ρ = ν − min_ℓ v_ℓ((p−1)/κ) = max_{ℓ*}(e_{ℓ*} + Σ_{ℓ≠ℓ*} ν_ℓ) holds.
  - So do the special cases: κ = ℓ^e gives e, and κ = 6 gives 1 + max(ν₂, ν₃).
  - ρ ≤ ν holds since e_ℓ ≤ ν_ℓ. ρ ≥ 1 + max ν_ℓ holds when ω(κ) ≥ 2.
- **Theorem B, family A.**
  - Blocks: the first-free-column kernel of B(c) is (c, 1).
  - The chain z_i has prime indices and z_{i+1} ∉ Z_i.
  - All triggers fall in level-1 nodes of the first level-2 node, so no merge is evaluated
    at η ≠ H_π before a trigger.
  - The default makes ν restarts and then completes. The variant makes ρ* − 1 counted
    restarts and then collapses at z_{ρ*+1}, or reaches H_π when ν* = e*.
  - The condition (κ(a+1) − 1)a ≥ ν − 1 is exactly the number of slots.
  - With `spread=True` nothing changes, since a rank-a block of a+1 columns has one free
    column.
- **Theorem B, family C.**
  - Lemma 4(a): r_x ≢ 0 mod ℓ*^{e*} while c_{ℓ*}(⟨η⟩) ≤ e*. This works for any generator
    η, not only the one `join` returns.
  - Lemma 4(b): the level-2 kernel is (y, 1, 0, …) because column 1 = −y·column 0 stays
    −y·e₀ under Gauss–Jordan. The shifts are (−r_x) mod κ and (1 − r_x) mod κ, both ≠ the
    target. Free level-2 outputs may vanish, but they are never child 0.
  - Lemma 4(c) and (d) hold, and so does the recursion s_L = (n_L − 1)s_{L−1}.
  - s(6,1) = 70·431·2591·15551 = 1 215 628 978 970.
  - s(κ,a) is increasing in κ and a: there are κ − 2 factors, each increasing. The smallest
    κ with two primes is 6, so ν ≤ 10¹² suffices.
- **Remark B.1 (level-by-level order).** In 𝓜 all level-1 nodes of the first accumulation
  level come first, in column order, and then all level-2 merges in column order.
  - Family A: the triggers are in the first κ(a+1) level-1 nodes.
  - Family C, with chain-free filler: the y's appear in the same column order. Levels ≥ 3 only
    classify x and 1.
  - So both orders give the same counts.
- **Corollary.** Dirichlet residue classes 1 + ℓ^t mod ℓ^{t+1} give v_ℓ(p−1) = t exactly.
  Correct.

## 2. Own computations (`2026-11-05-rees-is-restarts-composite-check/independent_check.py`)

New code; it does not import `composite_restarts.py`. It reuses from the solver only what a
real run executes (`PiParts.split`, `Classifier`, `lemma12`, `_kernel_vector`, `_row_reduce`,
`_Restart`, and `is_sde_solve` for validation). Its own pieces:
- the factorisation and ρ;
- an order-test version of T: x ∈ ⟨η⟩^κ iff x^{|η|/g} = 1;
- η chosen as a power of a fixed H_π generator (checked against `join`);
- fresh family A and C constructions;
- an explicit-set lattice search.

Output: `independent_check.out` (prints `ALL OK`), 52 s under `nice -n 10`.

1. **Closed forms.** The closed form of ρ equals the max form for every p < 3000 and
   κ ∈ {3, 4, 6, 8, 9, 10, 12, 15, 30}. Prime powers give e, κ = 6 gives 1 + max(ν₂, ν₃), and
   1 + max ν_ℓ ≤ ρ ≤ ν.
2. **Brute-force lattice.** At κ ∈ {6, 10, 12} and p < 700, the anchors were every (γ,1),
   plus every (γ,γ′,1) when n_π ≤ 64: 53 796 anchors. In every case the maximum longest
   failing chain is exactly ρ − 1.
3. **Driver against the full solver.** At (p, κ, a) = (1459,3,1), (163,3,1), (7681,2,2) and
   (257,2,2), family A plus random filler at full arity gives the same restarts and the same
   `collapsed` flag as `is_sde_solve`, for both the default and the variant. The counts are
   ν+1 = 7, 5, 10, 9 runs for the default and 1 run for the variant.
4. **Composite κ.** 14 primes, with κ-smooth parts chosen large and unbalanced:
   - κ = 6: ν₂ = 1, ν₃ = 20; 15/15; 40/2; 3/3; 1/1; 2/1;
   - κ = 10: ν₂ = 30, ν₅ = 1; 6/6; 1/20; 1/1;
   - κ = 12: ν₂ = 2, ν₃ = 25; 20/10; 3/3; 2/1.

   Results:
   - Family A gives exactly ρ runs for the variant and ν+1 for the default, using the smallest
     a that fits. For example, κ = 6 at p = 6112404799489 gives 16 and 31, and κ = 12 at
     p = 309586821121 gives 21 and 31.
   - Family C at level 3 (a = 1, and a = 2 at κ = 6) gives exactly ρ for the variant. The
     default makes at least ρ + 1 runs, and at least ρ + 2 when ρ < ν.
   - The counts are the same with the `join` generator and with my generator.
5. **κ = 30, p = 172801.** Family A with ℓ* = 2, 3, 5 gives 6, 11 and 12 runs, and
   ρ = 12.
6. **Random level-2 prefixes.** 450 runs at κ = 6, 10, 12. The variant never exceeds ρ and
   the default never exceeds ν+1.

Tests: `nice -n 10 /opt/anaconda3/bin/python -m pytest -q tests/test_rees_is_restarts_composite.py
tests/test_rees_is_sde_solver.py` gives **196 passed** (127 s).

Not done (as in the report): no full `is_sde_solve` run at composite κ, since
G(6,1) ≈ 3·10¹³. The composite counts rest on Lemma 3, which I re-derived from the code, and
on prefix drivers. The drivers were validated against the full solver at κ ≤ 3.

## 3. Imprecisions in the §8 sentence (fixed in the integrated text)

1. It used ℓ as the prime index. The remark already uses ℓ_d (the number of zero-sum terms)
   and q (for κ = q^e). Changed to q.
2. "Two distinct prime factors" was meant as "at least two" (κ = 30 is covered). Now "at
   least two".
3. "For either node order" did not say which orders. Now "under depth-first and under
   level-by-level evaluation".
4. "The kernel choice" is now "the default kernel vector". Family C needs `spread=False`.
5. It had no status split. Now "(proved; … a finite computation)" for the lattice check, and
   a statement that no full run at composite κ was executed.
6. It dropped the citation of the prime-power note, which records the `collapse=True` tests.
   Restored, together with this check.
7. It added "these are counts of runs, not lower bounds on time", following the report's
   withdrawn §4 claim, so that "cannot remove the factor b" is not read as a time lower
   bound.

## 4. Integration

- **`main.tex`, `rem:is-runtime`.**
  - The sentence "When $\kappa_d$ has two distinct prime factors, the argument gives no bound
    better than $\nu+1$ runs, and the bound $T^{\mathrm{IS}}_d$ stands (…)" was replaced. The
    exact-string count was asserted to be 1. The replacement is the corrected §8 text.
  - In the nearby sentence on evaluation order, "the bounds $\nu+1$ and $e$" became "the
    bounds $\nu+1$, $e$ and $\rho$ (below)".
  - No `\mathsf`, `\mathrel`, `\begingroup` or `\aa` was added.
  - Backup: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/composite-check/main.tex.bak`.
- **`core/main-core.tex`.** It states no restart count; its "there are no restarts" at
  l. 548 concerns the fixed quantum allocation. Unchanged.
- **Builds** (scratch copies under `$TMPDIR/rees-cc.NciK`, `latexmk -g -pdf`):
  - full: exit 0, 173 pp.; core: exit 0, 27 pp.;
  - 0 Overfull, no undefined refs or cites, no "Float too large", no LaTeX warnings in the
    full log.
- **Numbers test.** `tests/tools/test_rees_paper_numbers.py`: 2 passed. `make_numbers.py`
  not run.
- **Not changed.** No claim gate, registry, numbers or bib change. No git, no network.

## 5. Open (unchanged)

- Whether the variant's worst case at fixed (κ, g_d) is bounded at all.
- Whether its total *work* at composite κ obeys a b² bound like T^{IS,∗}_d.
- Whether another deterministic method beats ρ runs.
