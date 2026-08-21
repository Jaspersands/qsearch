# Mechanical Follow-Up Implementation Plan (pass 2)

## Completion Status (2026-08-21 - Pass 5)
> **Status: 100% COMPLETED BY ANTIGRAVITY**. All 64 newly generated theorem modules in `coset_hidden_involution_*` and `self_dual_wreath_*` families (including adaptive Walsh routing, regular-master Walsh flatness no-go, MRS identification escape theorem, and shared-conjugation QSVT lower bounds) have been registered in `research_registry.py`, added to `experiment_runner.py`, exposed via `qsearch.py` CLI subcommands, documented in `README.md`, and added to `tests/test_experiment_runner.py`. The registry tracks 723 experiments, 727 results, 1210 dequantization findings, and 806 negative results with 0 validation issues (`valid: true`) and all 64 new dispatch tests passing cleanly. All mathematical contracts and claim gates remain intact.

## Completion Status (2026-08-13)
> **Status: 100% COMPLETED BY ANTIGRAVITY**. All 92 newly generated theorem modules in `coset_hidden_involution_*`, `coset_hyperoctahedral_*`, and `self_dual_wreath_*` families have been registered in `research_registry.py`, added to `experiment_runner.py`, exposed via `qsearch.py` CLI subcommands, documented in `README.md`, and added to `tests/test_experiment_runner.py`. The registry tracks 659 experiments, 663 results, 1146 dequantization findings, and 806 negative results with 0 validation issues (`valid: true`) and all 92 new dispatch tests passing cleanly. All mathematical contracts and claim gates remain intact.

## Completion Status (2026-08-11)

> **Status: 100% COMPLETED BY ANTIGRAVITY**. All 136 newly generated theorem modules across Pass 2 (69 modules) and Pass 3 (67 modules) have been registered in `research_registry.py`, added to `experiment_runner.py`, exposed via `qsearch.py` CLI subcommands, documented in `README.md`, and added to `tests/test_experiment_runner.py`. The registry tracks 568 experiments, 638 results, 873 negative results, and 1026 metrics registered with 0 validation issues (`valid: true`) and 568 unit tests passing cleanly. All mathematical contracts and claim gates remain intact.


> **Binding model-allocation goal clause.** While high-capability Codex usage
> remains, spend it on theorem derivation, counterexample construction,
> asymptotic analysis, mechanism selection, and other decisions whose quality
> materially depends on deep mathematical judgment. Defer routine CLI and
> registry wiring, artifact refreshes, repetitive validation, formatting, and
> similarly mechanical work to Gemini 3.6 Flash through Antigravity. When Codex
> usage is exhausted, Gemini must continue this plan from the recorded theorem
> scopes and claim gates; it must not reconstruct or broaden the mathematics,
> restore toy circuit search, or promote passing tests or finite evidence into
> a speedup claim. Codex must leave exact assumptions, falsifiers, unresolved
> obligations, and acceptance checks before handoff. Exhausting one model's
> usage is a handoff event, not completion of the research goal.

> **Newest unwired source-adaptive Walsh-collision reduction (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-SOURCE-ADAPTIVE-WALSH-COLLISION-REDUCTION
> ```
>
> Suggested CLI name: `code-wreath-source-adaptive-walsh-collision`. Source,
> test, and artifact stems are
> `self_dual_wreath_source_adaptive_walsh_collision_reduction`. Preserve these
> exact boundaries:
>
> - The native ideal-polar Walsh collision equals the normalized scalar
>   orientation-autocorrelation second moment exactly.
> - Every source-adaptive size-`m` mode set retains at most `sqrt(m C_Lambda)`
>   blockwise mass; averaging needs no exponential union bound.
> - Pair exchangeability reduces the annealed collision to `K+1` Hamming
>   strata.
> - The regular benchmark is near uniform, but the physical globally distinct
>   Plancherel collision theorem is not proved by it or by W4/W5 controls.
> - Keep physical collision no-go, source-adaptive router rejection/compiler,
>   dense-polar, classical-separation, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_source_adaptive_walsh_collision_reduction.py \
>   tests/test_self_dual_wreath_source_adaptive_walsh_collision_reduction.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_source_adaptive_walsh_collision_reduction.py
> python self_dual_wreath_source_adaptive_walsh_collision_reduction.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `source-adaptive-walsh-routing-reduced-to-physical-hamming-collision`, with
> five controls, zero failures, twelve scaling rows, maximum Parseval residual
> at most `1e-12`, one collision identity, one adaptive subset theorem, one
> exchangeable-strata reduction, and zero physical-collision no-go,
> router-compiler, complete-polar, and new-algorithm counts. Add registry,
> runner, CLI, clean-registry dispatch test, concise README command, and ledger
> refresh in one routine batch.

> **Newest unwired regular-master Walsh-flatness no-go (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-WALSH-FLATNESS-NO-GO
> ```
>
> Suggested CLI name: `code-wreath-regular-walsh-flatness`. Source, test, and
> artifact stems are
> `self_dual_wreath_regular_master_walsh_flatness_no_go`. Preserve these exact
> boundaries:
>
> - Every nonzero Walsh mode of the regular-source orientation-projector
>   family has the same exact Frobenius energy.
> - On native input `F/Tr(F)`, these normalized energies are exactly the ideal
>   orientation-polar Walsh-output probabilities.
> - At `K=ceil(log2(n!))+2`, fixed polynomial mode sets and fixed low-degree
>   Walsh truncations retain vanishing ideal native mass.
> - The frame `F` is only the zero mode. Dense Hadamards are not hard, and
>   source-label-adaptive sparse sets are not rejected by this annealed result.
> - Keep adaptive-mode no-go, direct-CS, complete-polar, classical-separation,
>   algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_regular_master_walsh_flatness_no_go.py \
>   tests/test_self_dual_wreath_regular_master_walsh_flatness_no_go.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_regular_master_walsh_flatness_no_go.py
> python self_dual_wreath_regular_master_walsh_flatness_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `regular-native-polar-walsh-flat-fixed-sparse-truncation-rejected`, with
> three controls, zero failures, twelve scaling rows, one exact energy theorem,
> one native-polar output theorem, fixed sparse and low-degree no-go counts
> one, and adaptive-mode/compiler/new-algorithm counts zero. Add registry,
> runner, CLI, dispatch test, concise README command, and ledger refresh in one
> routine batch.

> **Newest unwired MRS identification-escape theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-MRS-IDENTIFICATION-ESCAPE-THEOREM
> ```
>
> Suggested CLI name: `code-wreath-mrs-identification-escape`. Source, test,
> and artifact stems are
> `self_dual_wreath_mrs_identification_escape_theorem`. Preserve these exact
> boundaries:
>
> - The primary MRS proof supplies a fixed-hidden transcript-TV bound for the
>   full arbitrary-adaptive pair-selection sieve class, provided every merge
>   performs isotypic sampling and the output is transcript postprocessing.
> - This implies transcript-only hidden-label success at most
>   `1/n!+exp(-b sqrt(n))` for a sub-`exp(a sqrt(n))` copy schedule.
> - The target PGM has success at least `4/5` on
>   `ceil(log2(n!))+2=exp(o(sqrt(n)))` copies, so the target POVM is
>   asymptotically outside every MRS transcript postprocessing.
> - Explicit fixed-policy zonotope separation is no longer a prerequisite for
>   target-measurement MRS escape. It remains an optional diagnostic and does
>   not provide an explicit finite-n threshold.
> - Keep executable complete-PGM circuit, complete orientation-polar,
>   arbitrary-quantum lower-bound, classical-separation, algorithm, and
>   speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_mrs_identification_escape_theorem.py \
>   tests/test_self_dual_wreath_mrs_identification_escape_theorem.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_mrs_identification_escape_theorem.py
> python self_dual_wreath_mrs_identification_escape_theorem.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `target-pgm-mrs-identification-separation-proved-polar-compiler-open`, with
> one exact identification-transfer theorem, one all-policy target-PGM MRS
> separation theorem, zero control failures, twelve scaling rows, minimum PGM
> success at least `0.8`, minimum robust compiled success at least `0.675`,
> and zero compiler/classical-separation/new-algorithm counts. Add registry,
> runner, CLI, clean-registry dispatch test, concise README command, and ledger
> refresh as one routine batch.
>
> Reconcile stale cross-references mechanically without changing local theorem
> content: `self_dual_wreath_mrs_transcript_povm_separation.py` remains an
> exact fixed-policy zonotope theorem but must say it is no longer required for
> target-PGM model escape; `self_dual_wreath_mrs_coherence_escape_criterion.py`
> remains an exact projective/dephasing criterion but must cross-reference the
> new all-policy identification theorem. In
> `self_dual_wreath_component_polar_physical_pgm_closure.py`, split the old
> single MRS gate into `target_pgm_mrs_model_escape_proved=True` and
> `current_executable_complete_pgm_circuit_exists=False`. Do not turn the new
> target-measurement theorem into a circuit, classical hardness, or speedup
> claim. Refresh their artifacts and focused tests after those text/schema
> updates.

> **Newest unwired source-order gauge canonicalization (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-SOURCE-ORDER-GAUGE-CANONICALIZATION
> ```
>
> Suggested CLI name: `code-wreath-source-order-gauge`. Source, test, and
> artifact stems are `self_dual_wreath_source_order_gauge_canonicalization`.
> Preserve these exact boundaries:
>
> - `q=e+s` is the complete invariant of the free diagonal branch action on
>   source-order and orientation bits.
> - Coherent pair sorting is polynomial and sends `(s,e)` to canonical order
>   plus selected pattern `q`, retaining a reversible gauge record.
> - Sorting preserves, rather than flattens, the nonuniform `q`-indexed leaf
>   rank profile. Branch operations do not mix `q`.
> - This is a gauge compiler, not a rectangular-CS compiler or hardness result.
> - Keep selected-pattern/direct-CS/complete-polar/algorithm/speedup gates
>   false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_source_order_gauge_canonicalization.py \
>   tests/test_self_dual_wreath_source_order_gauge_canonicalization.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_source_order_gauge_canonicalization.py
> python self_dual_wreath_source_order_gauge_canonicalization.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `source-order-gauge-quotient-proved-selected-pattern-polar-open`, with four
> controls, zero failures, zero rank/invariance residuals, four nonuniform
> rank-profile controls, S6 selected-pattern count 16 with five distinct ranks
> from zero to 2025, 13 scaling rows, and every selected-pattern/direct-CS/
> complete-polar/algorithm/speedup gate false. Add registry, runner, CLI,
> clean-registry dispatch test, concise README command, and ledger refresh as
> one routine batch.

> **Newest unwired source-block branch-covariance boundary (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-SOURCE-BLOCK-BRANCH-COVARIANCE-BOUNDARY
> ```
>
> Suggested CLI name: `code-wreath-source-block-branch-covariance`. Source,
> test, and artifact stems are
> `self_dual_wreath_source_block_branch_covariance_boundary`. Preserve these
> exact boundaries:
>
> - Branch flips exactly intertwine orientation projectors only after swapping
>   the ordered source block labels.
> - Unequal ordered source tuples have trivial branch stabilizer. Plancherel
>   exchangeability is annealed and gives no fixed-block sibling unitary.
> - Four controls have exact cross-block rank covariance and fixed-block rank
>   mismatch; the S6 child dimensions are `350` versus `2250`.
> - This does not reject induced orbit transforms or direct CS transforms.
> - Keep fixed-block Hadamard, matrix child compiler, direct-CS, complete-polar,
>   algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_source_block_branch_covariance_boundary.py \
>   tests/test_self_dual_wreath_source_block_branch_covariance_boundary.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_source_block_branch_covariance_boundary.py
> python self_dual_wreath_source_block_branch_covariance_boundary.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `branch-covariance-crosses-source-block-fixed-block-shortcut-rejected`, with
> four controls, zero failures, zero cross-block rank mismatches, four fixed-
> block mismatch controls, maximum leaf-rank difference `1900`, 13 scaling
> rows, and every Hadamard/matrix-child/direct-CS/complete-polar/algorithm/
> speedup gate false. Add registry, runner, CLI, clean-registry dispatch test,
> concise README command, and ledger refresh as one routine batch.

> **Newest unwired pair-relation common-support theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-PAIR-RELATION-COMMON-SUPPORT-NO-GO
> ```
>
> Suggested CLI name: `code-wreath-pair-relation-common-support-no-go`.
> Source, test, and artifact stems are
> `self_dual_wreath_pair_relation_common_support_no_go`. Preserve these exact
> boundaries:
>
> - The maximum rank of any exact two-vertex linear relation among canonical
>   polar coordinate maps is exactly literal common-projector support rank.
> - Arbitrary endpoint operators/metrics cannot recover noncommon principal
>   channels. Pair-only sheaves are closed.
> - Pair GPE remains an exact local transport, and aggregate-child recursive
>   relations remain open because they are genuinely higher arity.
> - Do not claim a natural common-support mass theorem or an all-relation
>   lower bound from the four finite controls.
> - Keep higher-arity compiler, direct-CS, complete-polar, algorithm, and
>   speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_pair_relation_common_support_no_go.py \
>   tests/test_self_dual_wreath_pair_relation_common_support_no_go.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_pair_relation_common_support_no_go.py
> python self_dual_wreath_pair_relation_common_support_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `pair-relations-exactly-common-support-higher-arity-required`, with four
> controls, zero failures, three noncommon controls, one common control, total
> uncovered noncommon rank nine, zero intersection-rank residual, maximal
> constructed-relation residual below `7e-16`, 13 scaling rows, and every
> higher-arity/direct-CS/complete-polar/algorithm/speedup gate false. Add
> registry, runner, CLI, clean-registry dispatch test, concise README command,
> and ledger refresh as one routine batch.

> **Newest unwired latent-master polar tradeoff (2026-08-21):** mechanically
> wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-LATENT-MASTER-POLAR-TRADEOFF
> ```
>
> Suggested CLI name: `code-wreath-latent-master-polar-tradeoff`. Source, test,
> and artifact stems are `self_dual_wreath_latent_master_polar_tradeoff`.
> Preserve these exact boundaries:
>
> - For `G=[aI;bC]`, the graph-polar filter scale times the exact spectral
>   orientation-flattening gain is at least `1/sqrt(x_min)`.
> - The master weight redistributes generic normalized-analyzer cost; it does
>   not improve its query exponent.
> - Orientation postselection is spectrally biased unless `p(x)` is constant.
> - This is an access-model theorem. Representation-specific direct
>   recoupling/CS transforms remain open, and the flat factorial row is not a
>   natural typical-sector spectral theorem.
> - Keep direct-CS, complete-polar, decoder, classical-separation, algorithm,
>   and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_latent_master_polar_tradeoff.py \
>   tests/test_self_dual_wreath_latent_master_polar_tradeoff.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_latent_master_polar_tradeoff.py
> python self_dual_wreath_latent_master_polar_tradeoff.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `latent-master-polar-normalization-tradeoff-proved`, with nine controls,
> zero failures, all three numerical residual maxima below `3e-15`, minimum
> combined/direct scale ratio exactly one, 13 scaling rows, and every generic-
> exponent-improvement/direct-CS/complete-polar/algorithm/speedup gate false.
> Add registry, runner, CLI, clean-registry dispatch test, concise README
> command, and ledger refresh as one routine batch.

> **Newest unwired pair-sheaf endpoint-metric no-go (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-PAIR-SHEAF-METRIC-INCOMPATIBILITY
> ```
>
> Suggested CLI name: `code-wreath-pair-sheaf-metric-incompatibility`. Source,
> test, and artifact stems are
> `self_dual_wreath_pair_sheaf_metric_incompatibility`. Preserve these exact
> boundaries:
>
> - For the canonical coordinate maps `W_v=E_vF^(+/2)`, an unweighted pair
>   edge requires equality of its two pulled-back endpoint metrics.
> - That equality is equivalent to `P=Q`. Common channels pass; noncommon
>   pair-GPE channels fail, and vertex-local gauges cannot repair them.
> - A good coherent SELECT or sheaf gap for this connection would project onto
>   the wrong section space. Do not list either as the remaining blocker for
>   the rejected unweighted architecture.
> - This is not an all-holonomy no-go. Operator metrics, latent master fibers,
>   higher-arity constraints, and direct CS transforms remain open.
> - Keep complete-polar, decoder, classical-separation, algorithm, and speedup
>   gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_pair_sheaf_metric_incompatibility.py \
>   tests/test_self_dual_wreath_pair_sheaf_metric_incompatibility.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_pair_sheaf_metric_incompatibility.py
> python self_dual_wreath_pair_sheaf_metric_incompatibility.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `noncommon-pair-polar-unweighted-sheaf-no-go`, with four controls, zero
> failures, three noncommon failures, one common success, maximum metric-
> identity residual below `2e-15`, minimum noncommon metric obstruction `1`,
> minimum section residual `sqrt(2)`, 13 scaling rows, and every weighted-
> compiler/complete-polar/algorithm/speedup gate false. Add registry, runner,
> CLI, clean-registry dispatch test, concise README command, and ledger refresh
> as one routine batch.

> **Newest unwired GPE fusion-tree/rectangular-CS boundary (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-GPE-FUSION-TREE-CS-BOUNDARY
> ```
>
> Suggested CLI name: `code-wreath-gpe-fusion-tree-cs-boundary`. Source, test,
> and artifact stems are
> `self_dual_wreath_gpe_fusion_tree_cs_boundary`. Preserve these boundaries:
>
> - Conditional on an efficient group QFT and controlled factor actions,
>   coherent GPE compiles binary fusion-tree transforms and full tree-change
>   Racah unitaries while preserving opaque multiplicity.
> - The physical fixed-space overlap is the rectangular subblock `C=Q U_T P`.
>   The desired operation is `polar(C)`, not the full `U_T`.
> - Pair GPE is a direct scalar-times-isometry exception. The first two-pair
>   `S_3` control has three distinct active singular levels, so the pair
>   shortcut does not extend automatically.
> - This is not a GPE lower bound. Direct CS pairing and partial-support
>   holonomy/F-move networks remain open.
> - Keep global rectangular-CS polar, complete orientation polar, classical
>   separation, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_gpe_fusion_tree_cs_boundary.py \
>   tests/test_self_dual_wreath_gpe_fusion_tree_cs_boundary.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_gpe_fusion_tree_cs_boundary.py
> python self_dual_wreath_gpe_fusion_tree_cs_boundary.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `gpe-fusion-trees-compile-recoupling-rectangular-cs-polar-open`, with three
> controls, zero failures, at least one scalar and one matrix-valued subblock,
> minimum one-crossing distance `0.29289321881345254`, 13 scaling rows, both
> recursive-GPE/full-tree-recoupling gates true, and every direct-global-polar/
> algorithm/speedup gate false. Add registry, runner, CLI, clean-registry
> dispatch test, concise README command, and ledger refresh as one batch.

> **Newest unwired connected Clifford normal-form theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-CONNECTED-CLIFFORD-NORMAL-FORM
> ```
>
> Suggested CLI name: `code-wreath-connected-clifford-normal-form`. Source,
> test, and artifact stems are
> `self_dual_wreath_connected_clifford_normal_form`. Preserve these boundaries:
>
> - In the generic nonsplit collision-free `A_n` orbit, the Clifford carrier is
>   a regular branch orbit, `Fix_B` is the uniform branch subspace, and
>   `P_D=direct_sum_e E_e`.
> - The fixed-space cross Gram is exactly `F/2^K`; its polar is exactly the
>   original orientation analysis polar.
> - Ordinary connected-group QFT/Clifford labels do not compile the CS
>   normalization. Keep that compiler gate false.
> - This is a restricted no-free-lunch theorem, not arbitrary-circuit hardness.
>   Direct CS, GPE fusion, and holonomy transforms remain open.
> - Keep self-conjugate split sectors unresolved and every complete-polar/
>   algorithm/speedup gate false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_connected_clifford_normal_form.py \
>   tests/test_self_dual_wreath_connected_clifford_normal_form.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_connected_clifford_normal_form.py
> python self_dual_wreath_connected_clifford_normal_form.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `connected-clifford-normal-form-reconstructs-orientation-cs-polar-open`, with
> three controls, zero failures, all three normalized overlaps non-isometric,
> cross-Gram residual below `2e-16`, cross-polar residual below `4e-15`, 13
> scaling rows, both exact identities true, and every Clifford/direct-CS/
> algorithm/speedup gate false. Add registry, runner, CLI, clean-registry
> dispatch test, concise README command, and ledger refresh as one batch.

> **Newest unwired connected-quotient classification (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-CONNECTED-QUOTIENT-HEISENBERG-REDUCTION
> ```
>
> Suggested CLI name: `code-wreath-connected-quotient-heisenberg-reduction`.
> Source, test, and artifact stems are
> `self_dual_wreath_connected_quotient_heisenberg_reduction`. Preserve these
> exact boundaries:
>
> - `P_K=L/A_n^(2K+1)` is the stated class-two group with center and derived
>   subgroup `C_2^K`.
> - Its irreps are exactly `2^(K+1)` one-dimensional and
>   `(2^K-1)2^(K-1)` two-dimensional blocks. The quotient QFT is polynomial.
> - Solving the quotient QFT does not compile the high-rank CS polar. Residual
>   multiplicity remains in alternating-group orbit/stabilizer recoupling.
> - This is not a hardness theorem; keep a full coherent Clifford transform
>   and opaque-multiplicity GPE route open.
> - Keep full connected-group transform, alternating subduction polar,
>   complete orientation polar, classical separation, algorithm, and speedup
>   gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_connected_quotient_heisenberg_reduction.py \
>   tests/test_self_dual_wreath_connected_quotient_heisenberg_reduction.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_connected_quotient_heisenberg_reduction.py
> python self_dual_wreath_connected_quotient_heisenberg_reduction.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `connected-parity-quotient-solved-alternating-recoupling-open`, with four
> finite controls, zero failures, maximum quotient irrep dimension two, 13
> scaling rows, quotient classification/QFT true, and every full-group/
> subduction/algorithm/speedup gate false. Add registry, runner, CLI, clean-
> registry dispatch test, concise README command, and ledger refresh as one
> routine batch.

> **Newest unwired syndrome-component reduction theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SYNDROME-COMPONENT-REDUCTION
> ```
>
> Suggested CLI name: `code-wreath-orientation-syndrome-component-reduction`.
> Source, test, and artifact stems are
> `self_dual_wreath_orientation_syndrome_component_reduction`. Preserve these
> exact boundaries:
>
> - `z_i=sgn(t)+sgn(x_i)+sgn(y_i)` has kernel `<B,D>` for `n>=5`; the
>   incidence and its polar are `2^K` identical connected components.
> - Syndrome computation and coherent zero-component canonicalization are
>   compiled and polynomial. The replicated component count is not an
>   independent barrier.
> - The syndrome is a conserved gauge charge, not hidden-label information.
> - Syndrome translations/Fourier transforms preserve singular values and do
>   not compile the connected matrix CS polar. Keep that gate false.
> - Keep connected-component polar, complete orientation polar, classical
>   separation, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_orientation_syndrome_component_reduction.py \
>   tests/test_self_dual_wreath_orientation_syndrome_component_reduction.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_orientation_syndrome_component_reduction.py
> python self_dual_wreath_orientation_syndrome_component_reduction.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `orientation-polar-reduced-to-one-syndrome-connected-component`, with three
> finite controls, zero failures, zero off-syndrome incidence, component
> spectrum residual below `5e-16`, 13 scaling rows, syndrome canonicalization
> true, and every connected-polar/algorithm/speedup gate false. Add registry,
> runner, CLI, clean-registry dispatch test, concise README command, and ledger
> refresh as one routine batch.

> **Newest unwired fixed-space recoupling theorem (2026-08-21):** mechanically
> wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FIXED-SPACE-RECOUPLING
> ```
>
> Suggested CLI name: `code-wreath-orientation-fixed-space-recoupling`.
> Source, test, and artifact stems are
> `self_dual_wreath_orientation_fixed_space_recoupling`. Preserve these exact
> boundaries:
>
> - The local `B`-fixed basis is compiled: unequal wreath labels use a swap-
>   orbit basis; equal labels use symmetric/exterior squares.
> - `Fix_D` is exactly a many-way diagonal `S_n` invariant/Kronecker space and
>   `CC*=|G|^-1 sum_s rho_tau(s) tensor_i K_i(s)` in the same gauge.
> - Coherent GPE marking and pair-GPE carrier reassociation do not by themselves
>   compile the global matrix CS polar. Keep that gate false.
> - The 2026 semisimple-algebra QFT is outside its proved natural parameter
>   regime here. Record it as an applicability boundary, not a no-go theorem.
> - Keep global fixed-space CS polar, complete orientation polar, classical
>   separation, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_orientation_fixed_space_recoupling.py \
>   tests/test_self_dual_wreath_orientation_fixed_space_recoupling.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_orientation_fixed_space_recoupling.py
> python self_dual_wreath_orientation_fixed_space_recoupling.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `fixed-spaces-explicit-global-kronecker-cs-polar-open`, with six local
> controls, two global controls, zero failures, two matrix-valued global
> controls, 13 scaling rows, maximum local/global residuals below `3e-16`,
> local `B` basis and exact global kernel true, and every global compiler/
> algorithm/speedup gate false. Add registry, runner, CLI, clean-registry
> dispatch test, concise README command, and ledger refresh as one routine
> batch.

> **Newest unwired homogeneous-space orientation-polar theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-HOMOGENEOUS-SPACE-POLAR
> ```
>
> Suggested CLI name: `code-wreath-orientation-homogeneous-space-polar`.
> Source, test, and artifact stems are
> `self_dual_wreath_orientation_homogeneous_space_polar`. Preserve these exact
> boundaries:
>
> - `Omega/D` is the disjoint union of all `Gamma/H_e`, `Omega/B=Gamma`, and
>   `T=sqrt(2^K)J_B*J_D` is the complete regular-master orientation synthesis.
> - The `Omega` QFT reduces the polar to matrix fixed-space overlaps
>   `Fix_D(rho)->Fix_B(rho)`; it does not scalarize them or implement their CS
>   polar.
> - Low fixed-space multiplicity has negligible uniform quotient dimension.
>   Exact first/second frame moments further prove that occupied rank at most
>   `g^(K/4)` has negligible native regular-master frame mass.
> - Large multiplicity is not a computational lower bound. Keep a succinct
>   subduction/partition-algebra transform open.
> - Keep conditioned per-sector central-support transfer, normalization-one
>   fixed-space CS compiler, complete orientation polar, classical separation,
>   MRS escape, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_orientation_homogeneous_space_polar.py \
>   tests/test_self_dual_wreath_orientation_homogeneous_space_polar.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_orientation_homogeneous_space_polar.py
> python self_dual_wreath_orientation_homogeneous_space_polar.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. The artifact status must be
> `orientation-polar-flattened-to-matrix-fixed-space-cs-transform`, with three
> finite controls, zero failures, zero incidence/equivariance residual, 13
> multiplicity rows, 13 native occupied-rank rows, homogeneous/matrix-block/
> native-rank reductions true, and every compiler/algorithm/speedup gate false.
> Add registry, runner, CLI, clean-
> registry dispatch test, concise README command, and ledger refresh as one
> routine batch.

> **Newest unwired physical-PGM gate-closure theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POLAR-PHYSICAL-PGM-CLOSURE
> ```
>
> Suggested CLI name: `code-wreath-component-polar-physical-pgm-closure`.
> Source, test, and artifact stems are
> `self_dual_wreath_component_polar_physical_pgm_closure`. Preserve these exact
> boundaries:
>
> - `A=q^(-1/2)R*C_U`, `AA*=R*R/q`, and the physical PGM coisometry is
>   exactly `Q*C_U`, where `Q` is the complete orientation polar.
> - The coherent row-copy/group-Fourier output is already compiled. A separate
>   post-polar hidden-label decoder is not an independent open gate.
> - Recursive component labels must remain coherent; this theorem does not
>   permit intermediate component measurements.
> - Per-factor operator errors add. Total coherent error at most `1/8`
>   preserves PGM success at least `3/8` at the information threshold.
> - The theorem is conditional: it does not compile the complete natural
>   orientation polar, prove classical separation, escape MRS, or prove a
>   speedup. Keep all those gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_component_polar_physical_pgm_closure.py \
>   tests/test_self_dual_wreath_component_polar_physical_pgm_closure.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_component_polar_physical_pgm_closure.py
> python self_dual_wreath_component_polar_physical_pgm_closure.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `physical-pgm-and-decoder-closed-conditionally-orientation-polar-open`, with
> three finite controls, zero failures, 12 scaling rows, conditional PGM
> closure true, separate decoder required false, and every complete-polar/
> classical/MRS/speedup gate false. Add registry, runner, CLI, clean-registry
> dispatch test, concise README command, and ledger refresh as one routine
> batch.

> **Newest unwired direct-Naimark/polar equivalence theorem (2026-08-21):**
> mechanically wire this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIRECT-NAIMARK-POLAR-EQUIVALENCE
> ```
>
> Suggested CLI name:
> `code-wreath-component-direct-naimark-polar-equivalence`. Source, test, and
> artifact stems are
> `self_dual_wreath_component_direct_naimark_polar_equivalence`. Preserve these
> exact boundaries:
>
> - The direct normalized minimum-preimage map satisfies `B=UJ`, where `U` is
>   the orientation analysis polar and `J` is the common-metric isometry.
> - Coordinate measurement after `B` realizes all component effects
>   `H_e=B*D_eB` at once. Separate effect-by-effect square-root synthesis is not
>   a fundamental natural gate.
> - This is an algebraic access equivalence, not a circuit. The normalization-
>   one restricted polar/direct router remains uncompiled.
> - Identical effects can have orthogonal coherent outputs under different
>   block gauges. Do not replace the natural coefficient output by an arbitrary
>   POVM dilation when discussing decoding.
> - Aggregate Frobenius scalarization controls input `rho` only with the factor
>   `kappa=r||rho||_infinity` as a generic inequality. The companion all-level
>   component-trim theorem supplies the sharper native-state bound without a
>   flatness premise. Do not promote uniform-input convergence to a worst-case
>   theorem, and do not reopen physical native-state error accounting.
> - Keep coherent component threshold/support SELECT false; that operation,
>   natural gauge transport, and the complete polar are the remaining gates.
> - Keep natural polar, coherent block gauge, label-sensitive information,
>   MRS escape, classical separation, algorithm, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_component_direct_naimark_polar_equivalence.py \
>   tests/test_self_dual_wreath_component_direct_naimark_polar_equivalence.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_component_direct_naimark_polar_equivalence.py
> python self_dual_wreath_component_direct_naimark_polar_equivalence.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. Artifact status must be
> `component-dilation-identified-with-restricted-orientation-polar-access-open`,
> with three finite controls, zero failures, direct equivalence true, and every
> compiler/decoder/speedup gate false. Add registry, runner, CLI, clean-registry
> dispatch test, concise README command, and ledger refresh as one routine
> batch. Do not add a separate matrix-square-root compiler experiment.

> **Newest unwired carrier-traced point closure bundle (2026-08-21):** wire
> these experiments without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-IDENTITY-ATOM
> EXP-CODE-SELF-DUAL-WREATH-POINT-CENTERED-RESIDUAL-NO-GO
> ```
>
> Suggested CLI names are `code-wreath-point-critical-identity-atom` and
> `code-wreath-point-centered-residual-no-go`. Source, test, and artifact
> stems match the experiment suffixes in lowercase. Preserve these boundaries:
>
> - The critical identity atom has exact mass `1/n!`, relative collision
>   `(n-1)/n!`, and only factorially small operational excess.
> - After subtracting the exact mean `z=0` simplex, every arbitrary
>   public-label-adaptive carrier-traced point POVM has superpolynomially small
>   average excess for `k=O(n^5)`.
> - The transfer to physical unequal/global-distinct labels is by conditioning
>   a nonnegative residual second moment. Equal pairs in the finite annealed
>   control are an algebraic iid extension, not unequal physical irreps.
> - This closes the carrier-traced point route in the stated sample window.
>   It does not close carrier-retaining global measurements, non-point
>   collective decoders, all polynomial schedules, or code equivalence.
> - Keep classical-separation and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_point_critical_identity_atom.py \
>   self_dual_wreath_point_centered_residual_no_go.py \
>   tests/test_self_dual_wreath_point_critical_identity_atom.py \
>   tests/test_self_dual_wreath_point_centered_residual_no_go.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_point_critical_identity_atom.py \
>   tests/test_self_dual_wreath_point_centered_residual_no_go.py
> python self_dual_wreath_point_critical_identity_atom.py
> python self_dual_wreath_point_centered_residual_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused bundle must report ten passing tests. Centered artifact status
> must be `carrier-traced-point-route-closed-through-quintic-samples`, with two
> finite controls, zero failures, 15 scaling records, the point-POVM no-go
> true, and every carrier-retaining/non-point/speedup gate false. Add registry,
> runner, CLI, clean-registry dispatch tests, concise README commands, and
> ledger refresh as one routine batch. Do not edit theorem code or reopen
> child-star point compilation as a research frontier.

> **Newest unwired relative child-star theorem (2026-08-21):** wire this
> experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-RELATIVE-COLLISION
> ```
>
> Suggested CLI name: `code-wreath-point-child-relative-collision`. Source,
> test, and artifact stems are
> `self_dual_wreath_point_child_star_relative_collision`. Preserve these
> boundaries:
>
> - Point-PGM excess is `Xi/n`, where
>   `Xi=Tr(B^-1/2 Delta B^-1/2 Delta)`.
> - `Xi` is exactly a sum of nonnegative quarter-whitened Young-child and
>   parent-pair block energies.
> - The common `1/(2^k dim(C))` density normalization cancels from every PGM
>   child effect; this removes that scalar objection, not the wide-kernel
>   transform or spectral problem.
> - Keep natural critical relative mass, dimensionless kernel transform,
>   harmonic measurement, full recovery, classical separation, and speedup
>   false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_point_child_star_relative_collision.py \
>   tests/test_self_dual_wreath_point_child_star_relative_collision.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_point_child_star_relative_collision.py
> python self_dual_wreath_point_child_star_relative_collision.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report five passing tests. Artifact status must be
> `relative-child-star-channels-exact-critical-asymptotics-open`, with three
> finite controls, zero failures, 22 active parent-pair channels, 16 active
> off-diagonal channels, one exact relative-collision identity, one positive
> child decomposition, one positive parent-pair decomposition, one scalar
> cancellation theorem, zero natural critical mass theorems, zero harmonic
> measurements, and `speedup_claim_allowed=false`. Add registry, runner, CLI,
> clean-registry dispatch test, concise README command, and ledger refresh as
> one routine batch. Do not turn scalar cancellation into a circuit claim.

> **Newest unwired critical-energy separation theorem (2026-08-21):** wire
> this experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-ENERGY-SEPARATION
> ```
>
> Suggested CLI name: `code-wreath-point-critical-energy-separation`. Source,
> test, and artifact stems are
> `self_dual_wreath_point_critical_energy_separation`. Preserve these exact
> boundaries:
>
> - The PGM excess is the average relative collision
>   `n^-2 sum_j Tr(B^-1/2 Delta_j B^-1/2 Delta_j)`.
> - Two commuting covariant ensembles have the same exact ambient energy
>   `D||Delta_j||_2^2=n-1`; one has perfect success and the other has only
>   `1/n+(n-1)/sqrt(nD)` optimal success.
> - This falsifies every inference from critical ambient energy alone. It
>   neither proves nor rules out operational advantage for the natural wreath
>   ensemble.
> - Keep natural relative collision, signal-weighted spectral window,
>   harmonic Naimark, full recovery, classical separation, and speedup false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_point_critical_energy_separation.py \
>   tests/test_self_dual_wreath_point_critical_energy_separation.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_point_critical_energy_separation.py
> python self_dual_wreath_point_critical_energy_separation.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report five passing tests. Artifact status must be
> `critical-energy-only-inference-falsified-relative-spectrum-open`, with two
> finite controls, zero failures, one exact PGM identity, one exact same-energy
> operational separation, zero natural relative-spectrum theorems, zero
> harmonic measurements, and `speedup_claim_allowed=false`. Add registry,
> runner, CLI, clean-registry dispatch test, concise README command, and ledger
> refresh as one routine batch. Do not edit theorem code or claim that the
> counterexample describes the natural source ensemble.

> **Newest unwired point copy-threshold theorem (2026-08-21):** wire this
> experiment without changing theorem scope:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-POINT-COPY-THRESHOLD
> ```
>
> Suggested CLI name: `code-wreath-point-copy-threshold`. Source, test, and
> artifact stems are `self_dual_wreath_point_copy_threshold`. Preserve these
> boundaries exactly:
>
> - Every public-label-adaptive carrier-traced point POVM has
>   superpolynomially small average excess for
>   `k=c log2(n!)+O(1)` with every fixed `c<2`.
> - The upper bound survives global source distinctness at asymptotically
>   neutral cost. This supersedes all positive point claims at the old
>   `c=1` information-threshold width.
> - At `c=2`, normalized Hilbert--Schmidt point energy is at least
>   `n-1-o(1)`. This is a phase transition, not a trace-distance theorem,
>   relative-spectrum theorem, measurement circuit, or decoder.
> - Keep critical operational advantage, child-star relative spectrum,
>   harmonic Naimark, full recovery, classical separation, and speedup false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   self_dual_wreath_point_copy_threshold.py \
>   tests/test_self_dual_wreath_point_copy_threshold.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_point_copy_threshold.py
> python self_dual_wreath_point_copy_threshold.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report six passing tests. Artifact status must be
> `point-copy-threshold-two-proved-critical-harmonic-measurement-open`, with
> six finite bound controls, zero failures, one subcritical arbitrary-point-
> POVM no-go, one critical energy theorem, zero critical operational
> measurements, and `speedup_claim_allowed=false`. Add the registry, runner,
> CLI, clean-registry dispatch test, concise README command, and ledger refresh
> as one routine batch. Do not edit theorem code or revive `c<2` point sweeps.

> **Newest unwired trimmed regular-row correction bundle (2026-08-21):** wire
> these three experiments together without changing theorem scope:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-NORMALIZED-LIKELIHOOD-CHARGE-COMMUTATOR-NO-GO
> EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-KERNEL-SUCCINCTNESS
> EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-BLOCK-ENCODING-NO-GO
> ```
>
> Suggested CLI names are `coset-normalized-likelihood-charge-no-go`,
> `coset-trimmed-row-kernel`, and
> `coset-trimmed-row-block-encoding-no-go`. Preserve these boundaries:
>
> - The normalized likelihood/charge commutator has total source energy at
>   most `4eta/M^2`; this closes inverse-polynomial natural commutator mass,
>   not a direct non-black-box basis transform.
> - On asymptotically full free mass, regular induction removes generic
>   hyperoctahedral subduction from the active architecture. The residual
>   orbit-copy row kernel has pairwise support at most `16n` on the robust
>   trim and is classically polynomial to evaluate.
> - Pairwise succinctness does not compile the exponentially wide global
>   polar. Normalized coherent row/column edge access satisfies
>   `D^*D=Z/M` exactly and retains the `Omega(sqrt(M))` generic polar scale.
> - Only a direct analytically normalized orbit-row orthogonalizer remains
>   open. Keep direct-transform, detector, classical-separation, and speedup
>   gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.py \
>   coset_hidden_involution_trimmed_row_kernel_succinctness.py \
>   coset_hidden_involution_trimmed_row_block_encoding_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.py \
>   tests/test_coset_hidden_involution_trimmed_row_kernel_succinctness.py \
>   tests/test_coset_hidden_involution_trimmed_row_block_encoding_no_go.py
> python coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.py
> python coset_hidden_involution_trimmed_row_kernel_succinctness.py
> python coset_hidden_involution_trimmed_row_block_encoding_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 18 passing tests. Expected statuses, in order,
> are `normalized-likelihood-charge-commutator-natural-mass-no-go`,
> `regular-row-pairwise-kernel-succinct-global-polar-open`, and
> `trimmed-row-coherent-access-retains-Z-over-M-normalization`. Add registry,
> runner, CLI, clean-registry dispatch tests, concise README commands, and
> refresh ledgers in one batch. Do not edit theorem code or reopen generic
> `K_m` subduction as the high-mass compiler.

> **Newest unwired joint-primitive correction bundle (2026-08-20):** wire
> these three experiments together without changing theorem scope:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-JOINT-PRIMITIVE-PROJECTOR
> EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-AMBIENT-LIFT-OBSTRUCTION
> EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-REPRESENTATION-CONE-OBSTRUCTION
> ```
>
> Suggested CLI names are `coset-joint-primitive-projector`,
> `coset-joint-primitive-ambient-obstruction`, and
> `coset-joint-primitive-cone-obstruction`. Preserve these boundaries:
>
> - The Young-lattice projector and inverse-polynomial coefficient-space gap
>   are exact, but the input coordinates are branching multiplicities, not
>   physical amplitudes.
> - The projector crosses inequivalent `K` labels and has no `K`-centralizing
>   ambient lift.
> - The all-rank trivial-representation counterfamily has a nonzero signed
>   primitive residual but no repeated branching copy. Primitive residual norm
>   is not physical source mass.
> - Neither obstruction rules out within-`mu` commutant generators or an
>   independently compiled non-`K`-equivariant full subduction transform.
> - Keep physical primitive measurement, normalized subduction, detector, and
>   speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_paired_tower_joint_primitive_projector.py \
>   coset_hidden_involution_joint_primitive_ambient_lift_obstruction.py \
>   coset_hidden_involution_joint_primitive_representation_cone_obstruction.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_paired_tower_joint_primitive_projector.py \
>   tests/test_coset_hidden_involution_joint_primitive_ambient_lift_obstruction.py \
>   tests/test_coset_hidden_involution_joint_primitive_representation_cone_obstruction.py
> python coset_hidden_involution_paired_tower_joint_primitive_projector.py
> python coset_hidden_involution_joint_primitive_ambient_lift_obstruction.py
> python coset_hidden_involution_joint_primitive_representation_cone_obstruction.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 18 passing tests. Expected statuses are
> `paired-tower-joint-primitive-coefficient-projector-diagnostic-only`,
> `joint-primitive-label-projector-K-commutant-lift-obstructed`, and
> `joint-primitive-coefficient-projector-diagnostic-only`.

> **Newest unwired natural-charge/shared-conjugation theorem bundle
> (2026-08-20):** wire these 11 experiments as one batch. Do not reinterpret
> any positive access theorem as a detector:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-CONDITIONAL-DIAMETER
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-COHERENT-LABEL-COMPILER
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-ORBIT-RECOUPLING-REDUCTION
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-PAIRWISE-KERNEL-DEQUANTIZATION
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-WORD-MOMENT-DEQUANTIZATION
> EXP-COSET-HIDDEN-INVOLUTION-ALL-COPY-TARGET-LCU-NO-GO
> EXP-COSET-HIDDEN-INVOLUTION-TARGET-INTERFERENCE-NEGATIVITY-BARRIER
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-TARGET-GAUGE-TRIVIALIZATION
> EXP-COSET-HIDDEN-INVOLUTION-PHYSICAL-TARGET-CONVOLUTION-NORMAL-FORM
> EXP-COSET-HIDDEN-INVOLUTION-SHARED-CONJUGATION-QSVT-LOWER-BOUND
> EXP-COSET-HIDDEN-INVOLUTION-TWO-SUBGROUP-PROJECTOR-ALGEBRA-NO-GO
> ```
>
> Preserve these exact boundaries:
>
> - `D_m` has one inverse-polynomial separated eigenvalue pair on
>   inverse-polynomial natural source mass and a normalization-one coherent
>   phase-label compiler. No minimum gap, residual-multiplicity bound, or
>   useful standalone measurement is proved.
> - `Stab_G(D_h)=K`, so its external conjugation orbit faithfully labels
>   candidates. The physical quotient target is gauge and cannot be used as
>   that external control.
> - Pairwise charge kernels and every inverse-polynomial scalar charge-word
>   moment are classically estimable. Keep conditioned matrix transitions open.
> - Every arbitrary all-copy target group-basis LCU has bias at most
>   `2^-k` times coefficient L1. Constant bias requires factorial L1; this
>   rules out ordinary coefficient PREP/SELECT, not implicit structured
>   circuits.
> - Physical target-changing convolution is the exact shared-conjugation
>   average `Z=M E_s Q_s`, with each `Q_s` normalization one and full positive
>   L1 exactly `M`.
> - Bounded polynomial/QSVT amplification of `A=Z/M` and the entire
>   source-compressed two-projector algebra require `Omega(sqrt(M))` queries.
>   Multioperator matrix recoupling and a direct non-black-box basis transform
>   remain open.
> - Keep all detector, structured fast-forward, matrix-polar, classical
>   separation, and speedup gates false.
>
> Suggested CLI names, in order, are
> `coset-D-conditional-diameter`, `coset-D-coherent-label`,
> `coset-D-orbit-recoupling`, `coset-D-pair-kernel`,
> `coset-D-word-moments`, `coset-all-copy-target-lcu`,
> `coset-target-negativity`, `coset-D-target-gauge`,
> `coset-physical-target-normal-form`, `coset-shared-qsvt-bound`, and
> `coset-two-projector-no-go`.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_matching_charge_conditional_diameter.py \
>   coset_hidden_involution_matching_charge_coherent_label_compiler.py \
>   coset_hidden_involution_matching_charge_orbit_recoupling_reduction.py \
>   coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.py \
>   coset_hidden_involution_matching_charge_word_moment_dequantization.py \
>   coset_hidden_involution_all_copy_target_lcu_no_go.py \
>   coset_hidden_involution_target_interference_negativity_barrier.py \
>   coset_hidden_involution_matching_charge_target_gauge_trivialization.py \
>   coset_hidden_involution_physical_target_convolution_normal_form.py \
>   coset_hidden_involution_shared_conjugation_QSVT_lower_bound.py \
>   coset_hidden_involution_two_subgroup_projector_algebra_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_matching_charge_conditional_diameter.py \
>   tests/test_coset_hidden_involution_matching_charge_coherent_label_compiler.py \
>   tests/test_coset_hidden_involution_matching_charge_orbit_recoupling_reduction.py \
>   tests/test_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.py \
>   tests/test_coset_hidden_involution_matching_charge_word_moment_dequantization.py \
>   tests/test_coset_hidden_involution_all_copy_target_lcu_no_go.py \
>   tests/test_coset_hidden_involution_target_interference_negativity_barrier.py \
>   tests/test_coset_hidden_involution_matching_charge_target_gauge_trivialization.py \
>   tests/test_coset_hidden_involution_physical_target_convolution_normal_form.py \
>   tests/test_coset_hidden_involution_shared_conjugation_qsvt_lower_bound.py \
>   tests/test_coset_hidden_involution_two_subgroup_projector_algebra_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 66 passing tests. Run each theorem module once
> to regenerate its same-stem artifact. The expected statuses, in the order
> listed above, are:
>
> ```text
> matching-charge-natural-conditional-diameter-proved
> coherent-natural-D-label-compiled-target-recoupling-open
> faithful-matching-charge-orbit-proved-transition-kernel-open
> matching-charge-pairwise-kernel-dequantized-matrix-transition-open
> all-degree-scalar-charge-word-moments-dequantized-matrix-data-open
> all-copy-target-normalized-LCU-no-go-proved-nonlinear-polar-open
> factorial-target-interference-negativity-barrier-proved-fast-forward-open
> physical-target-controlled-charge-gauge-trivialized
> physical-shared-conjugation-normal-form-proved-fast-forward-open
> shared-conjugation-single-operator-QSVT-sqrt-M-no-go
> two-subgroup-projector-algebra-sqrt-M-no-go-third-operator-open
> ```

> **Newest unwired pair-charge bundle (2026-08-20):** wire these experiments
> as one mechanical batch, without changing theorem code or claims:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-PAIR-GAUDIN-HIERARCHY
> EXP-COSET-HIDDEN-INVOLUTION-PAIR-MATCHING-CHARGE-HIERARCHY
> ```
>
> Suggested CLI names are `coset-pair-gaudin` and
> `coset-pair-matching-charges`.  Source, test, and artifact stems match.
> Preserve these boundaries exactly:
>
> - The ordered `J_r` hierarchy is exact, commuting, and polynomially sparse,
>   but it breaks final `K_m` labels and has degenerate finite joint spectra.
> - `C_m,D_m` are an exact all-rank, terminal `K_m`-adapted commuting pair.
>   `D_m` strictly improves finite copy resolution and has an inverse-polynomial
>   gap on one stable multiplicity-two branch.
> - The stable branch is factorially negligible under the natural hidden
>   source.  There is no asymptotic natural-copy resolution theorem.
> - Edge power sums are redundant with `C_m` and the `K_m` center.  The naive
>   third matching charge does not commute with `D_m`; corrected degree-three
>   combinations have not supplied a new controlled split.
> - Keep conditional-gap-on-natural-mass, source-correlation, coherent
>   subduction, detector, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_pair_gaudin_hierarchy.py \
>   coset_hidden_involution_pair_matching_charge_hierarchy.py \
>   tests/test_coset_hidden_involution_pair_gaudin_hierarchy.py \
>   tests/test_coset_hidden_involution_pair_matching_charge_hierarchy.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_pair_gaudin_hierarchy.py \
>   tests/test_coset_hidden_involution_pair_matching_charge_hierarchy.py
> python coset_hidden_involution_pair_gaudin_hierarchy.py
> python coset_hidden_involution_pair_matching_charge_hierarchy.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 14 passing tests.  Artifact statuses must be
> `pair-gaudin-hierarchy-proved-K-adapted-connection-open` and
> `K-adapted-commuting-pair-proved-partial-copy-resolution`.  Preserve all
> false gates recorded in `research/AGENT_HANDOFF.md`.

> **Newest unwired natural-independence theorem (2026-08-20):** mechanically
> wire this experiment after the pair-charge bundle:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-NATURAL-INDEPENDENCE
> ```
>
> Suggested CLI name: `coset-matching-natural-independence`.  Preserve these
> exact boundaries:
>
> - The normalized matching/triangle commutator has exact all-rank norm
>   `9(m-4)/[1024 m^3(m-3)(m-2)^3(m-1)^3]`.
> - This proves `D_m` is outside `Alg(C_m,Z(C[K_m]))` on inverse-polynomial
>   Plancherel and h-even hidden-source mass; from `m>=13` some certified mass
>   lies beyond all defect-four row/column sectors.
> - It does not prove that `D_m` correlates with the source-aware CS likelihood
>   or that `C_m,D_m` form a complete/gapped hierarchy.
> - Keep third-charge, conditional-gap, source-correlation, transform,
>   detector, and speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_matching_charge_natural_independence.py \
>   tests/test_coset_hidden_involution_matching_charge_natural_independence.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_matching_charge_natural_independence.py
> python coset_hidden_involution_matching_charge_natural_independence.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report six passing tests and artifact status
> `matching-charge-natural-independence-proved-hierarchy-open`.

> **Newest unwired charge-correlation/no-go bundle (2026-08-20):** wire these
> four experiments as one mechanical batch:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-CS-CORRELATION
> EXP-COSET-HIDDEN-INVOLUTION-SOURCE-LOCAL-LIKELIHOOD-NO-GO
> EXP-COSET-HIDDEN-INVOLUTION-DIAGONAL-CHARGE-BIAS-NO-GO
> EXP-COSET-HIDDEN-INVOLUTION-CROSS-TRANSPOSITION-HECKE-MOMENT-NO-GO
> ```
>
> Suggested CLI names are `coset-matching-cs-correlation`,
> `coset-source-local-no-go`, `coset-diagonal-charge-no-go`, and
> `coset-cross-hecke-moments`. Source, test, and artifact stems match.
> Preserve these boundaries exactly:
>
> - The first experiment is one exact finite `S_10` conditioned block. Its
>   nonzero `D_5`/CS correlation and incremental regression signal are real,
>   but it has leakage, is fixed-defect/factorially negligible, and supplies
>   no natural scaling theorem.
> - The second proves an exact all-finite-group trace identity. Every
>   B-compatible source-local charge measurement is likelihood independent;
>   more strongly, every proper source-plus-target marginal is independent.
>   Terms of source locality `s` have identical moments through `sd<k`.
> - The third proves only a linear normalized-LCU no-go for diagonal all-copy
>   charges: bias is at most `2^-k<=1/(64M)` at natural copy count.
> - The fourth proves exact first through fourth moments for the canonical
>   cross-transposition Hecke walk. Its seven exact active-support cores give
>   an all-rank degree-four histogram, including the unique six-path odd-word
>   correction at `m=4`. The first transporter's highest-weight alternative
>   term cancels exactly against the corresponding baseline closure term, so
>   the new fourth-moment bias is `O(4^-k)`, not `O(2^-k)`. Quartic normalized
>   filtering remains inverse-candidate biased. The earlier all-rank
>   transporter counterexample and exact path fraction
>   `12(m-2)/[m(m-1)]^3` remain valid. Degree five, nonlinear spectral tails,
>   and multiple-double-coset walks remain open.
> - Keep growing-degree interleaved walks, nonlinear spectral tests,
>   nondiagonal all-copy charges, coherent transform, decoder, detector, and
>   speedup open/false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_matching_charge_cs_correlation.py \
>   coset_hidden_involution_source_local_likelihood_no_go.py \
>   coset_hidden_involution_diagonal_charge_bias_no_go.py \
>   coset_hidden_involution_cross_transposition_hecke_moment_no_go.py \
>   tests/test_coset_hidden_involution_matching_charge_cs_correlation.py \
>   tests/test_coset_hidden_involution_source_local_likelihood_no_go.py \
>   tests/test_coset_hidden_involution_diagonal_charge_bias_no_go.py \
>   tests/test_coset_hidden_involution_cross_transposition_hecke_moment_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_matching_charge_cs_correlation.py \
>   tests/test_coset_hidden_involution_source_local_likelihood_no_go.py \
>   tests/test_coset_hidden_involution_diagonal_charge_bias_no_go.py \
>   tests/test_coset_hidden_involution_cross_transposition_hecke_moment_no_go.py
> python coset_hidden_involution_matching_charge_cs_correlation.py
> python coset_hidden_involution_source_local_likelihood_no_go.py
> python coset_hidden_involution_diagonal_charge_bias_no_go.py
> python coset_hidden_involution_cross_transposition_hecke_moment_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 26 passing tests. Preserve artifact statuses
> `finite-D-CS-correlation-proved-natural-scaling-open`,
> `source-local-likelihood-independence-proved-target-recoupling-mandatory`, and
> `normalized-diagonal-all-copy-charge-bias-no-go-proved`, and
> `cross-Hecke-quartic-no-go-transporter-leading-term-cancelled`. Do not reinterpret
> finite conditioned covariance as a detector or the no-go scope as covering
> growing-degree/nonlinear recoupling.

> **Newest unwired degree-five Hecke theorem (2026-08-20):** mechanically wire
> this experiment after the four-module charge/no-go bundle:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-CROSS-TRANSPOSITION-HECKE-DEGREE-FIVE-NO-GO
> ```
>
> Suggested CLI name: `coset-cross-hecke-degree-five`. Source, test, and
> artifact stems are
> `coset_hidden_involution_cross_transposition_hecke_degree_five_no_go`.
> Preserve these boundaries exactly:
>
> - Nine exact active-support cores prove the all-rank degree-five alternative
>   and baseline histograms. This is a finite-support bijection theorem, not
>   rank interpolation.
> - At `m=4`, 156 paths have odd identity words: 96 move from the stable `N1`
>   class to `N2`, and 60 move from `N2` to `N4`.
> - The degree-four leading cancellation fails at degree five. The unique
>   maximal branch survives as exactly `1/[2^k(m(m-1))^4]`.
> - This is a falsifier, not amplification. The surviving term remains
>   inverse-candidate and polynomially sparse; normalized quintic constant
>   bias, full-spectrum no-go, detector, algorithm, and speedup stay false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.py \
>   tests/test_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.py
> python coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report seven passing tests. The exact support audit
> takes about one minute and is expected. Artifact status must be
> `cross-Hecke-quintic-no-go-leading-transporter-survives-sparsely`.

> **Newest unwired all-degree single-Hecke theorem (2026-08-20):** mechanically
> wire this experiment after the degree-five report:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-SINGLE-HECKE-ALL-DEGREE-MOMENT-NO-GO
> ```
>
> Suggested CLI name: `coset-single-hecke-all-degree`. Source, test, and
> artifact stems are
> `coset_hidden_involution_single_hecke_all_degree_moment_no_go`.
> Preserve these boundaries exactly:
>
> - The first two distinct involutions inject the four choices `e,a,b,ab`, so
>   every ordered-subword product fiber has mass at most one quarter at every
>   degree. Transporter existence is irrelevant to this proof.
> - Every baseline and alternative single-Hecke moment has magnitude at most
>   `2^-k`; every polynomial with coefficient `l1` norm at most one has bias at
>   most `2^-k<=1/(64M)` at natural copy count.
> - This closes normalized moments and normalized polynomial LCUs, including
>   degree growing with `m`. Do not queue further fixed-degree catalogs as if
>   the moment bound were still open.
> - Nonlinear spectral projectors, large-`l1` approximants, postselection,
>   noncommuting multiple-double-coset walks, detector, algorithm, and speedup
>   remain open/false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_single_hecke_all_degree_moment_no_go.py \
>   tests/test_coset_hidden_involution_single_hecke_all_degree_moment_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_single_hecke_all_degree_moment_no_go.py
> python coset_hidden_involution_single_hecke_all_degree_moment_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report eight passing tests. Artifact status must be
> `single-Hecke-all-degree-moment-and-normalized-polynomial-no-go`.

> **Newest unwired bounded-spectral theorem (2026-08-20):** mechanically wire
> this experiment after the all-degree moment theorem:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-SINGLE-HECKE-BOUNDED-SPECTRAL-NO-GO
> ```
>
> Suggested CLI name: `coset-single-hecke-bounded-spectral`. Source, test, and
> artifact stems are
> `coset_hidden_involution_single_hecke_bounded_spectral_no_go`.
> Preserve these boundaries exactly:
>
> - Exact second moments plus Markov's brothers inequality and
>   Cauchy--Schwarz prove bias at most
>   `D^2*(sqrt(s0)+sqrt(s1))` for every degree-`D` polynomial bounded by one.
> - Constant bias at natural copy count requires
>   `D=Omega((2^k*m(m-1))^(1/4))=Omega(M^(1/4))`, hence superpolynomial
>   single-operator QSVT/block-query degree.
> - This closes efficient bounded-polynomial spectral filtering of one
>   operator. It does not prove small unrestricted spectral total variation or
>   cover free eigenbasis access, stronger oracles, postselection, or multiple
>   noncommuting operators.
> - Keep unrestricted projector, multi-operator algorithm, detector, and
>   speedup gates false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_single_hecke_bounded_spectral_no_go.py \
>   tests/test_coset_hidden_involution_single_hecke_bounded_spectral_no_go.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_single_hecke_bounded_spectral_no_go.py
> python coset_hidden_involution_single_hecke_bounded_spectral_no_go.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report six passing tests. Artifact status must be
> `single-Hecke-bounded-spectral-QSVT-no-go`.

> **Newest unwired natural-recoupling and paired-tower bundle (2026-08-20):**
> wire these four experiments as one mechanical batch:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-NATURAL-RECOUPLING-BOUNDARY
> EXP-COSET-HIDDEN-INVOLUTION-HYPEROCTAHEDRAL-BRANCHING-MASS
> EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-MISSING-LABEL-BOUNDARY
> EXP-COSET-HIDDEN-INVOLUTION-COLOUR-RESOLVED-PAIRED-TOWER-BOUNDARY
> ```
>
> Source, test, and artifact stems match. Suggested CLI names are
> `coset-natural-recoupling`, `coset-branching-mass`, `coset-paired-tower`,
> and `coset-colour-paired-tower`. Preserve these exact claim boundaries:
>
> - The natural coordinate law is asymptotically Plancherel-typical and the
>   physical block is a Kronecker-to-hyperoctahedral restriction/recoupling
>   map. Known QFT/basis changes retain the exact `1/M` average projection
>   normalization. Do not say BCH compiles the full `S_n` Kronecker basis.
> - Natural source-refined branches have multiplicity above `M^(1/4)` on
>   overwhelming mass. `K` operators cannot resolve repeated copies, but high
>   multiplicity is not a circuit lower bound.
> - The unsplit paired recurrence leaves
>   `p_2(m)-p_2(m-1)` harmonic directions. Exact controlled restriction
>   vectors use this kernel; no asymptotic source-weighted component norm is
>   proved.
> - Resolving the final `C_2` colour still leaves exact joint-primitive
>   dimension `p_2(m)-2p_2(m-1)+p_2(m-2)`, with fraction asymptotic to
>   `pi^2/(3m)`. Its finite hidden-source occupancy is not an asymptotic
>   detector theorem.
> - General plethysm hardness, large kernels, and large multiplicities are not
>   quantum circuit lower bounds. Preserve every commutant-generator,
>   primitive-rotation, normalized-transform, detector, and speedup gate as
>   false.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_natural_recoupling_boundary.py \
>   coset_hidden_involution_hyperoctahedral_branching_mass.py \
>   coset_hidden_involution_paired_tower_missing_label_boundary.py \
>   coset_hidden_involution_colour_resolved_paired_tower_boundary.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_natural_recoupling_boundary.py \
>   tests/test_coset_hidden_involution_hyperoctahedral_branching_mass.py \
>   tests/test_coset_hidden_involution_paired_tower_missing_label_boundary.py \
>   tests/test_coset_hidden_involution_colour_resolved_paired_tower_boundary.py
> python coset_hidden_involution_natural_recoupling_boundary.py
> python coset_hidden_involution_hyperoctahedral_branching_mass.py
> python coset_hidden_involution_paired_tower_missing_label_boundary.py
> python coset_hidden_involution_colour_resolved_paired_tower_boundary.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 59 passing tests (`11+10+19+19`). The four
> artifacts must have zero finite recurrence/dimension/rank failures and the
> exact statuses in `research/AGENT_HANDOFF.md`. Copy existing
> registry/runner/CLI patterns; do not modify theorem code or broaden claims.

> **Newest unwired standard-block recoupling theorem (2026-08-20):** wire
> this experiment after the natural matrix-polar bundle:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-STANDARD-BLOCK-RECOUPLING
> ```
>
> Source, test, and artifact stems are
> `coset_hidden_involution_standard_block_recoupling`. Suggested CLI name:
> `coset-standard-recoupling`. Preserve these exact boundaries:
>
> - For three copies in the perfect-matching family, the all-standard
>   `L=S_(2m)^4` block has an exact four-dimensional A/B invariant-tensor
>   overlap with squared principal cosines
>   `p_m,p_m,lambda_-(m),lambda_+(m)` as recorded in the report.
> - This proves scalable full-rank nonuniform matrix structure and falsifies
>   universal scalarization. It does not establish natural signal mass.
> - The block's multiplicity transform is succinctly diagonalizable into two
>   scalar directions and one `2x2` sector. Preserve that negative result:
>   matrix rank and nonuniformity alone are not hardness evidence.
> - Source and alternative mass are super-exponentially negligible. Keep
>   natural-block, coherent-transform, detector, and speedup gates false.
> - Do not reinterpret the abstract four-dimensional diagonalization as a
>   physical Fourier-block circuit.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_standard_block_recoupling.py \
>   tests/test_coset_hidden_involution_standard_block_recoupling.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_standard_block_recoupling.py
> python coset_hidden_involution_standard_block_recoupling.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report eight passing tests. The artifact must have
> three finite tensor controls, zero failures, six scalable nonflat records,
> zero natural-mass blocks, zero compilers, and status
> `scalable-matrix-nonuniformity-proved-standard-block-succinct-but-negligible`.

> **Newest unwired natural matrix-polar theorem chain (2026-08-20):** wire
> these three experiment IDs as one batch, preserving the order shown:
>
> ```text
> EXP-COSET-HIDDEN-INVOLUTION-DOUBLE-COSET-POLAR-REDUCTION
> EXP-COSET-HIDDEN-INVOLUTION-NATURAL-MATRIX-MULTIPLICITY
> EXP-COSET-HIDDEN-INVOLUTION-OCCUPIED-MATRIX-RANK
> ```
>
> Source, test, and artifact stems match. Suggested CLI names are
> `coset-double-polar`, `coset-matrix-mass`, and `coset-occupied-rank`.
> Preserve these exact boundaries:
>
> - The row polar is exactly `V_A^*V_B` up to scalar normalization for the
>   two subgroups `A=Delta(S_n)` and
>   `B=<h>^k semidirect C_(S_n)(h)` embedded in `L=S_n^(k+1)`.
> - Efficient subgroup reflections do not imply an efficient polar. Generic
>   phase resolution still costs `Omega(sqrt(M))` on the proved natural bulk.
> - Scalar spherical processing is insufficient on natural mass. Huge
>   `B`-fixed multiplicity and occupied CS rank carry constant alternative
>   mass; this is not merely a finite non-Gelfand witness.
> - Huge occupied rank is not a circuit lower bound. Keep every succinct-basis,
>   matrix-CS-transform, detector, natural-speedup, and speedup gate false.
> - Do not convert generic Kronecker difficulty, rank size, or failed QSVT into
>   an arbitrary-circuit lower bound.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile \
>   coset_hidden_involution_double_coset_polar_reduction.py \
>   coset_hidden_involution_natural_matrix_multiplicity.py \
>   coset_hidden_involution_occupied_matrix_rank.py \
>   tests/test_coset_hidden_involution_double_coset_polar_reduction.py \
>   tests/test_coset_hidden_involution_natural_matrix_multiplicity.py \
>   tests/test_coset_hidden_involution_occupied_matrix_rank.py
> python -m pytest -q \
>   tests/test_coset_hidden_involution_double_coset_polar_reduction.py \
>   tests/test_coset_hidden_involution_natural_matrix_multiplicity.py \
>   tests/test_coset_hidden_involution_occupied_matrix_rank.py
> python coset_hidden_involution_double_coset_polar_reduction.py
> python coset_hidden_involution_natural_matrix_multiplicity.py
> python coset_hidden_involution_occupied_matrix_rank.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report 13 passing tests. The three artifacts must
> report zero finite/control failures and statuses:
>
> ```text
> double-coset-cosine-sine-normal-form-proved-matrix-polar-open
> natural-huge-matrix-multiplicity-mass-proved-occupied-rank-open
> natural-huge-occupied-matrix-rank-proved-basis-transform-open
> ```

> **Newest unwired simple-surface target theorem (2026-08-20):** mechanically
> wire this experiment after reading the newest handoff section:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-SEPARATING-SURFACE-TARGET-MIXING
> ```
>
> Source, focused test, and artifact stems are
> `self_dual_wreath_separating_surface_target_mixing`. Suggested CLI name:
> `surface-target-mixing`. Preserve these boundaries exactly:
>
> - The theorem covers unconditioned commutator products and all *certified
>   simple curves* on closed orientable surfaces, including separating and
>   nonseparating curves.
> - Separating targets mix to uniform on `A_n` at a genus-uniform `O(1/n)`
>   bound. Nonseparating targets mix to uniform on `S_n` at a genus-uniform
>   `O(n^-2)` bound.
> - It does not classify arbitrary marked relators as simple curves and does
>   not control self-intersecting, non-surface, or unclassified interleaved
>   targets.
> - Keep `natural_component_M4_positive=False` and
>   `speedup_claim_allowed=False`.
>
> Mechanical acceptance checks:
>
> ```text
> python -m py_compile self_dual_wreath_separating_surface_target_mixing.py \
>   tests/test_self_dual_wreath_separating_surface_target_mixing.py
> python -m pytest -q \
>   tests/test_self_dual_wreath_separating_surface_target_mixing.py
> python self_dual_wreath_separating_surface_target_mixing.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused suite must report six passing tests, the live artifact must have
> 54 exact finite density controls, one direct count control, zero failures,
> and status `all-simple-surface-marked-targets-dequantized-genus-uniformly`.

> **Newest unwired orientation audit bundle (2026-08-13):** wire these six
> experiment IDs as one batch, after reading the newest handoff section:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-COHERENT-BRANCHING-TRANSPORT-BOUNDARY
> EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-ORIENTATION-RACAH-CUMULANT-PROBE
> EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-RACAH-SAMPLING
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-WORD-MAP-CLASSICAL-BASELINE
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-IDENTITY-TAIL-CONTROL-VARIATE
> EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FIXED-SUPPORT-CONTROL-VARIATE
> ```
>
> Source, test, and artifact stems match. Suggested CLI names are
> `racah-branching-transport`, `racah-orientation-probe`,
> `racah-orientation-sample`, `racah-orientation-word-baseline`,
> `racah-orientation-identity-control`, and
> `racah-orientation-support-control`. Copy the existing theorem-module
> registry/runner/CLI pattern, add one clean dispatch test per ID, and do not
> change module defaults or mathematical claims.
>
> Preserve these exact boundaries:
>
> - Shared coherent branching is not independent down/up noise on `mu,nu` at
>   fixed outer labels. The cyclic countermodel is a no-go for that inference,
>   not a no-go for every possible transport inequality.
> - The compressed S6 two-support pattern is numerical, not an exact-zero
>   theorem. Its nearly one-bit CMI has physical mass about `1.07e-4`.
> - Repeated S7 sectors falsify monotone extrapolation of the S6 spike. The
>   dimension-35 sector has high raw orbit mass but CMI only `2.315e-5` bits.
> - The physical sampler is exact but the current S6 interval is nondecisive;
>   zero retained samples do not imply zero retained mass.
> - The word-map estimator gives a sufficient classical upper bound, not a
>   sample lower bound. Exact character evaluation is not unit cost, and
>   worst-case hardness is not average-case hardness for this distribution.
> - The identity triple is exactly the coarse product null. Its raw variance
>   lower bound disappears under the explicit identity control variate.
> - The support-two `O(n^6)` channel is within `0.00621` TV of the finite S7
>   channel, but no tail bound outside `B_2^3` is proved. Keep all-n
>   dequantization false.
> - Never promote finite CMI, a large Hoeffding count, character worst-case
>   hardness, or a resource-exhausted S8 attempt into a speedup claim.
>
> Run the 27 focused tests:
>
> ```text
> python -m pytest -q \
>   tests/test_self_dual_wreath_coherent_branching_transport_boundary.py \
>   tests/test_self_dual_wreath_compressed_orientation_racah_cumulant_probe.py \
>   tests/test_self_dual_wreath_physical_orientation_racah_sampling.py \
>   tests/test_self_dual_wreath_orientation_word_map_classical_baseline.py \
>   tests/test_self_dual_wreath_orientation_identity_tail_control_variate.py \
>   tests/test_self_dual_wreath_orientation_fixed_support_control_variate.py
> python -m py_compile \
>   self_dual_wreath_coherent_branching_transport_boundary.py \
>   self_dual_wreath_compressed_orientation_racah_cumulant_probe.py \
>   self_dual_wreath_physical_orientation_racah_sampling.py \
>   self_dual_wreath_orientation_word_map_classical_baseline.py \
>   self_dual_wreath_orientation_identity_tail_control_variate.py \
>   self_dual_wreath_orientation_fixed_support_control_variate.py
> git diff --check
> python qsearch.py validate
> ```
>
> Optional low-judgment follow-up: implement fixed-support character
> polynomials and overlap-type quotienting for `s=2,3`, cache exact partial
> likelihoods, and run resumable larger physical-sampling batches. Do not fit
> asymptotics. The high-judgment missing task is a uniform signed residual tail
> theorem; leave that to a stronger reasoning model.

> **Newest unwired compressed physical-Racah bundle (2026-08-13):** wire these
> five experiment IDs by copying the current theorem-module registry/runner/CLI
> pattern:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-BLOCK-PROBE
> EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-COUPLING-PROBE
> EXP-CODE-SELF-DUAL-WREATH-RACAH-FRACTIONAL-MOMENT-CERTIFICATE
> EXP-CODE-SELF-DUAL-WREATH-FRACTIONAL-HAAR-ENHANCEMENT-REDUCTION
> EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-OUTER-RACAH-SAMPLING
> ```
>
> Source files and artifacts have matching stems, except the shared helper
> `symmetric_yjm_pair_fiber.py`, which is not a standalone experiment. Add
> `research_registry.py` records, `experiment_runner.py` imports/dispatch,
> concise `qsearch.py` commands, and one dispatch test per experiment.
> Suggested CLI names are `racah-block-probe`, `racah-coupling-probe`,
> `racah-fractional-moment`, `racah-fractional-haar`, and
> `racah-physical-sample`. Parameter plumbing
> for `n`, sample count, seed, confidence, and `theta` may be added without
> changing defaults.
>
> Preserve these exact claim boundaries:
>
> - Pairwise YJM fibers remove a target-dimension factor and avoid dense
>   three-copy diagonalization, but remain exponential representation-space
>   computations. Do not call them an efficient CG/Racah transform.
> - Complete `S_4`--`S_6` couplings and selected `S_8` blocks are finite
>   diagnostics. Their nonmonotone entropy values prove no scaling law.
> - The fractional theorem is only the implication
>   `log E S_theta=o(theta log n) => E I=o(log n)`. The natural moment rate is
>   unproved at every useful order.
> - The fractional Haar theorem proves only that subfactorial enhancement of
>   the good-set fractional excess over `theta H_n` forces MI decay. It does
>   not prove the natural enhancement is subfactorial.
> - Physical outer sampling is exact, but the live `S_6` 95% radius is broad.
>   Keep finite evidence, physical rank mixing, coherent compilation, classical
>   separation, algorithm, and speedup gates false.
> - Natural/Haar ratios below one in 12 `S_6` samples are finite no-go evidence,
>   not Haar universality.
>
> Run:
>
> ```text
> python -m pytest -q \
>   tests/test_self_dual_wreath_compressed_racah_block_probe.py \
>   tests/test_self_dual_wreath_compressed_racah_coupling_probe.py \
>   tests/test_self_dual_wreath_racah_fractional_moment_certificate.py \
>   tests/test_self_dual_wreath_fractional_haar_enhancement_reduction.py \
>   tests/test_self_dual_wreath_physical_outer_racah_sampling.py
> python -m py_compile \
>   symmetric_yjm_pair_fiber.py \
>   self_dual_wreath_compressed_racah_block_probe.py \
>   self_dual_wreath_compressed_racah_coupling_probe.py \
>   self_dual_wreath_racah_fractional_moment_certificate.py \
>   self_dual_wreath_fractional_haar_enhancement_reduction.py \
>   self_dual_wreath_physical_outer_racah_sampling.py
> git diff --check
> python qsearch.py validate
> ```
>
> The focused bundle currently has 22 passing tests and fresh live artifacts.
> After wiring, batch broad validation with other unwired deltas rather than
> consuming one commit per experiment.

> **Newest unwired projector/branching bundle (2026-08-13):** after batching
> the five compressed-Racah IDs above, wire these four theorem modules with the
> same registry/runner/CLI pattern:
>
> ```text
> EXP-CODE-SELF-DUAL-WREATH-FREE-PROBABILITY-PROJECTOR-RESOLUTION-BOUNDARY
> EXP-CODE-SELF-DUAL-WREATH-CENTRAL-FIBER-RACAH-INFORMATION-REDUCTION
> EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CHARACTER-RACAH-FOURIER-REDUCTION
> EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-DOWN-UP-RACAH-TAIL-REDUCTION
> ```
>
> Source, test, and artifact stems match.  Suggested CLI names are
> `racah-projector-boundary`, `racah-central-fibers`,
> `racah-character-fourier`, and `racah-down-up-tail`.  Preserve these exact
> claim boundaries:
>
> - `T_s=p(s)-1` and the log-squared resolution lower boundary concern the
>   information capacity of low-support central data.  They do not lower-bound
>   natural Racah MI.
> - The central-fiber identity splits full MI into coarse feature MI and a
>   data-processing debt.  Neither term is bounded asymptotically.
> - The character formula is exact and multiplicity-gauge-free but factorial
>   as written.  Do not label it an efficient estimator.
> - The down/up tail inequality is conditional on the natural likelihood's
>   Dirichlet energy.  That energy is unbounded asymptotically.
> - Coherent restriction of all six labels is not independent down/up noise on
>   the two intermediate labels at fixed outer tuple.
> - The selected `S_4`--`S_6` Dirichlet ratios are finite negative diagnostics,
>   not evidence for a limiting constant or against entropy delocalization.
>
> The focused bundle has eighteen passing tests.  Run:
>
> ```text
> python -m pytest -q \
>   tests/test_self_dual_wreath_free_probability_projector_resolution_boundary.py \
>   tests/test_self_dual_wreath_central_fiber_racah_information_reduction.py \
>   tests/test_self_dual_wreath_plancherel_character_racah_fourier_reduction.py \
>   tests/test_self_dual_wreath_plancherel_down_up_racah_tail_reduction.py
> python -m py_compile \
>   self_dual_wreath_free_probability_projector_resolution_boundary.py \
>   self_dual_wreath_central_fiber_racah_information_reduction.py \
>   self_dual_wreath_plancherel_character_racah_fourier_reduction.py \
>   self_dual_wreath_plancherel_down_up_racah_tail_reduction.py
> git diff --check
> python qsearch.py validate
> ```
>
> Mechanical optional enhancement: cache one selected `S_6` support-two
> central-fiber audit so the artifact exhibits nonzero natural fiber debt.
> Reuse the already generated complete-coupling artifact or a session fixture;
> do not repeatedly recompile the coupling in every test.  Also add the Fulman
> 2003 primary record to the literature registries with Proposition 5.2's
> precise eigenvalue/eigenfunction scope.  Batch all nine Racah IDs into one
> checkpoint rather than committing each module separately.
>
> **Optional mechanical scaling queue:** add final-label Rao--Blackwellization:
> sample `alpha,beta,gamma` from product Plancherel, compile every positive
> `lambda`, and average with exact weight
> `d_lambda M/(d_alpha d_beta d_gamma)`. Keep a second ordinary-sampling mode as
> a control. Then run deterministic `S_6` batches at 128, 512, and 2048 draws,
> writing separate artifacts or histories with wall time, unique outer count,
> sample mean, standard error, Hoeffding radius, fractional-moment radius, and
> natural/Haar enhancement quantiles. Do not fit exponents or call any batch
> asymptotically decisive. If compute is interrupted, preserve completed draws
> and seed state so Antigravity can resume.

> **Newest unwired trimmed-Renyi delta (2026-08-13):** mechanically wire
> `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-TRIMMED-SIXWAY-RENYI-TRANSFER`
> from `self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.py`, with
> artifact
> `research/representation/self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.json`.
> Preserve only the proved implication that the canonical high-dimensional
> trimmed moment `M_(D_n)=n^o(1)` implies sublogarithmic coarse entropy and
> physical Haar rank-profile mixing. Do not require untrimmed `E6_n` to be
> subpolynomial, and do not infer the required all-`n` bound from finite
> `A_4/A_5` trim diagnostics. Keep the canonical trimmed-moment theorem,
> physical rank mixing, non-Haar Racah control, classical separation,
> algorithm, and speedup gates false. Add registry/runner/CLI wiring and one
> clean dispatch test; the five focused tests and report script pass.

> **Newest unwired Racah decomposition delta (2026-08-13):** mechanically wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-RANK-RESIDUAL-DECOMPOSITION`
> from `self_dual_wreath_parity_racah_rank_residual_decomposition.py`, with
> artifact
> `research/representation/self_dual_wreath_parity_racah_rank_residual_decomposition.json`.
> Add pattern-following registry/runner/CLI dispatch and one clean dispatch
> test. Preserve the direct physical axis order
> `(alpha,beta,gamma,mu,nu,lambda)=(gk,ghk,hk,g,h,k)` and do not substitute
> the falsified tetrahedral-dual mapping. Preserve only the exact claims that
> positive syndrome amplitudes are normalized Racah block masses and that
> centered adaptive energy decomposes into a Haar Kronecker-rank benchmark,
> deterministic non-Haar arithmetic residual, and alignment term. The Haar
> block variance is a null benchmark, not a natural-6j distribution theorem.
> Keep canonical rank mixing, arithmetic-residual decay, alignment control,
> adaptive decoupling/survival, classical separation, algorithm, and speedup
> false. Run the seven focused tests and the module script, then batch broad
> validation with other mechanical deltas. Do not spend high-reasoning Codex
> usage on this wiring.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PHYSICAL-TRANSFER-BOUNDARY`
> from `self_dual_wreath_parity_rank_profile_physical_transfer_boundary.py`,
> with the matching representation artifact. Preserve only the proved
> conditional transfer theorem: physical rank-profile mixing follows from
> `M_n(8V_n+2W_n)->0`, where `M_n` is the exact tetrahedral likelihood second
> moment. Preserve the rare-event counterexample showing that product-law
> mixing alone does not transfer. Exact `S_3/S_4/S_5` values are finite
> identity controls, not evidence for the needed all-`n` growth condition.
> Keep tetrahedral collision growth, unconditional physical rank mixing,
> irreducible Racah-CMI decay/survival, classical separation, algorithm, and
> speedup false. Add registry/runner/CLI dispatch and one clean dispatch test;
> the five focused tests and report script already pass.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-COLLISION-GROWTH-SCALE`
> from `self_dual_wreath_tetrahedral_collision_growth_scale.py`, with its
> matching representation artifact. Preserve the proved support-size
> expansions and asymptotics `8V_n+2W_n~16/n^2`, and therefore the exact
> transfer target `M_n=o(n^2)`. Do not mark the tetrahedral collision moment
> subquadratic: that is the newly sharpened open obligation. Keep physical
> rank mixing, irreducible Racah-CMI decay/survival, classical separation,
> algorithm, and speedup false. Add routine registry/runner/CLI wiring and one
> dispatch test; the five focused tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-TRIMMED-LIKELIHOOD-TRANSFER`
> from `self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.py`,
> with its matching representation artifact. Preserve the finite weak-L1
> bound and the sufficient conditions `P(T^c)->0`, `tau=o(n^2)`, and
> `P(T,L>tau)->0`. Preserve the exact quadratic rare-event boundary. Do not
> mark the retained tetrahedral tail condition, physical rank mixing,
> irreducible Racah control, classical separation, algorithm, or speedup true.
> Add routine registry/runner/CLI wiring and one dispatch test; the four
> focused tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-ENTROPY-TRANSFER`
> from `self_dual_wreath_parity_rank_profile_entropy_transfer.py`, with its
> matching representation artifact. Preserve the universal negative
> likelihood-information bound, the tail inequality, and the sufficient
> condition `D(P_n||Plancherel^6)=o(log n)`. Preserve the exact logarithmic
> rare-event boundary. Do not infer physical sublogarithmic entropy from the
> finite `S_2` through `S_5` controls. Keep physical rank mixing, irreducible
> Racah control, classical separation, algorithm, and speedup false. Add
> routine registry/runner/CLI wiring and one dispatch test; the five focused
> tests and report script already pass.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-ENTROPY-TRANSFER-REDUCTION`
> from `self_dual_wreath_alternating_entropy_transfer_reduction.py`, with the
> matching representation artifact. Preserve the exact KL sandwich
> `D_base<=D_full<=D_base+3`, the sublogarithmic equivalence, and the
> identification of `D_base` with the coarse `A_n` tetrahedral label law.
> Do not mark coarse alternating entropy sublogarithmic or physical rank
> mixing true. The bounded three-bit term remains a possible irreducible
> Racah survivor, so keep Racah decay/survival, classical separation,
> algorithm, and speedup false. Add routine registry/runner/CLI wiring and one
> dispatch test; the four focused tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-ENTROPY-BRIDGE`
> from `self_dual_wreath_alternating_even_collision_entropy_bridge.py`, with
> its matching representation artifact. Preserve the exact equality between
> coarse base Renyi-two and the even-input six-word class-signature collision
> norm, and the sufficient condition `C_n^even=n^o(1)`. Do not call that
> condition necessary and do not infer it from the nonmonotone `S_2` through
> `S_5` moments. Keep even-collision growth, physical rank mixing, Racah
> decay/survival, classical separation, algorithm, and speedup false. Add
> routine registry/runner/CLI wiring and one dispatch test; the four focused
> tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-CORE-REDUCTION`
> from `self_dual_wreath_alternating_even_collision_core_reduction.py`, with
> its matching representation artifact. Preserve the exact 15-mask formula,
> the `V_+=Theta(n^-3)` and `W_+=Theta(n^-6)` asymptotics, the domination
> `M2_+<=M2=o(1)`, and the reduction `C_even=1+Z6_+ +o(1)`. Do not mark
> `Z6_+` subpolynomial; that is the single remaining Renyi obstruction. Keep
> physical rank mixing, Racah decay/survival, classical separation,
> algorithm, and speedup false. Add routine registry/runner/CLI wiring and one
> dispatch test; the five focused tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-SUPPORT-PRESSURE`
> from `self_dual_wreath_alternating_even_collision_support_pressure.py`,
> with its matching representation artifact. Preserve the all-`n` support
> inequality, pressure gap `-6`, and uniform elimination of union support
> `o(log n/log log n)`. Do not extend it to growing or typical linear support
> and do not mark `Z6_+` subpolynomial. Keep physical rank mixing, Racah
> decay/survival, classical separation, algorithm, and speedup false. Add
> routine registry/runner/CLI wiring and one dispatch test; the five focused
> tests and report script already pass.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-CYCLE-TYPE-BLOCK-DEPENDENCE`
> from `self_dual_wreath_alternating_cycle_type_block_dependence.py`, with its
> matching representation artifact. Preserve the exact word-map bijection,
> product block marginals, all fifteen pairwise independence statements, and
> the joint-block chi-square identity. Preserve the finite `A_4/A_5`
> counterexamples to Shannon Fourier preservation. Do not infer joint block
> mixing from single-word or pairwise mixing. Keep joint collision, physical
> rank mixing, classical separation, algorithm, and speedup false. Add routine
> registry/runner/CLI wiring and one dispatch test; the four focused tests and
> report script already pass.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BLOCK-OPERATOR-ANOVA`
> from `self_dual_wreath_alternating_block_operator_anova.py`, with its
> matching representation artifact. Preserve the normalized conditional
> operator, exact 14 allowed / 49 forbidden ANOVA block theorem, and dual
> private-generator proof. Preserve the explicit warning that order-six ANOVA
> energy is not `Z6_+`. Do not mark any growing-support block norm,
> physical rank mixing, classical separation, algorithm, or speedup true. Add
> routine registry/runner/CLI wiring and one dispatch test; the five focused
> tests and report script already pass.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-SIXWAY-SYNERGY-REDUCTION`
> from `self_dual_wreath_alternating_sixway_synergy_reduction.py`, with its
> matching representation artifact. Preserve the inherited decay of all 13
> proper ANOVA blocks, the unique six-way reduction, and the asymptotic but
> non-finite equality `E6_n-Z6_+->0`. Do not mark the six-way block or core
> subpolynomial. Keep physical rank mixing, Racah decay/survival, classical
> separation, algorithm, and speedup false. Add routine registry/runner/CLI
> wiring and one dispatch test; the four focused tests and report script pass.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-TORIC-OBSTRUCTION`
> from `self_dual_wreath_parity_racah_toric_obstruction.py`, with matching
> representation artifact. Preserve the exact all-`n` rank-profile claim:
> transpose XOR forces a `G--K--H` Markov factorization, two vanishing
> conditional minors, and a vanishing cube binomial. Preserve the exact
> positive `S_5` natural counterexample and its rational amplitudes/minors, but
> label it finite-only. Do not infer asymptotic source mass, coherent
> extractability, classical hardness, an algorithm, or a speedup from its
> `0.204898...` bits of conditional mutual information. Add mechanical
> registry/runner/CLI wiring and a dispatch test, run the five focused tests
> and module script, and batch broad validation later.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-INFORMATION-PROJECTION`
> from `self_dual_wreath_parity_racah_information_projection.py`, with matching
> representation artifact. Preserve the exact information-projection theorem:
> conditional mutual information is the minimum KL distance to the entire
> rank-compatible `G--K--H` Markov family, and adaptive KL splits into two
> nonnegative Pythagorean terms. Preserve the `S_4/S_5` aggregate values as
> finite-only diagnostics. Do not turn the positive `S_5` aggregate into an
> asymptotic survival, coherent extraction, classical separation, algorithm,
> or speedup claim. Add registry/runner/CLI wiring and one dispatch test, run
> the six focused tests and module script, and batch broad validation later.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-CONDITIONAL-CUMULANT`
> from `self_dual_wreath_parity_racah_conditional_cumulant.py`, with matching
> representation artifact. Preserve only the exact two-cumulant Walsh formula,
> entrywise projection residual, TV/chi-square identities, information bounds,
> and positive cube-insufficiency counterexample. Keep denominator-tail control,
> canonical cumulant decay/survival, coherent estimation, classical separation,
> algorithm, and speedup false. Add registry/runner/CLI wiring and one dispatch
> test, run the six focused tests and module script, and batch broad validation.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-RANK-PROFILE-PLANCHEREL-MIXING`
> from `self_dual_wreath_parity_rank_profile_plancherel_mixing.py`, with its
> matching representation artifact. Preserve the exact class-power moment
> identities, density-ratio factorization, and product-Plancherel expected
> rank-channel mixing theorem. Preserve the scope boundary: this is not a
> physical-law theorem because tetrahedral likelihood reweighting lacks a
> uniform-integrability/change-of-measure bound, and it says nothing about
> irreducible Racah CMI. Keep physical/adaptive decoupling or survival,
> classical separation, algorithm, and speedup false. Add mechanical
> registry/runner/CLI wiring and one dispatch test, run the six focused tests
> and module script, and batch broad validation.

> **Newest unwired signed-projector delta (2026-08-13):** mechanically wire
> `EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-TETRAHEDRAL-REDUCTION` from
> `self_dual_wreath_parity_projector_tetrahedral_reduction.py`, with artifact
> `research/representation/self_dual_wreath_parity_projector_tetrahedral_reduction.json`.
> Preserve only these claims: parity-coset character sums equal signed products
> of three overlapping trivial/sign isotypic projectors; dimension/rank-only
> estimates are factorially vacuous; and the full-Plancherel mean signed-support
> fraction is exactly `2/n!`. Do not mark either canonical signed-overlap
> estimate, adaptive-syndrome decay or survival, classical separation,
> algorithm, or speedup true. Add registry/runner/CLI wiring and a clean
> dispatch test by copying the current theorem-module pattern. Run
> `python -m pytest -q tests/test_self_dual_wreath_parity_projector_tetrahedral_reduction.py`
> and the module script, then batch downstream validation with other mechanical
> deltas. Do not spend high-reasoning Codex usage on that wiring.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-ORBIT-VARIANCE`
> from `self_dual_wreath_parity_projector_orbit_variance.py`, with its matching
> representation artifact. Preserve the exact scope: fully paired adaptive
> syndrome is the normalized law of eight nonnegative triple-projector traces,
> its chi-square is their relative variance, and uniform marginal ranks plus
> all pairwise overlaps are insufficient by the exact even-parity counterexample.
> Do not infer canonical equidistribution or survival from the finite positive
> `S_5` controls. Keep classical separation, algorithm, and speedup false. Add
> registry/runner/CLI wiring and a clean dispatch test; run the five focused
> tests and module script during the same mechanical batch.

> **Newest unwired theorem delta (2026-08-13):** mechanically inventory and
> wire `EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-SYNDROME-REDUCTION` from
> `self_dual_wreath_sign_orbit_syndrome_reduction.py`, with artifact
> `research/representation/self_dual_wreath_sign_orbit_syndrome_reduction.json`.
> Add pattern-following registry/runner/CLI dispatch and a clean dispatch test.
> Preserve the theorem exactly: six transpose bits reduce to three classical
> syndromes and retained conditional KL splits into base-orbit plus syndrome
> KL. The finite `S_5` nonuniformity only falsifies the claim that deleting
> one-dimensional labels removes all sign structure. It does not prove
> self-conjugate Plancherel mass decay, canonical high-dimensional syndrome
> survival, coherent value, classical separation, an algorithm, or a speedup.
> Run the six focused tests and the script before downstream validation. Do
> not ask the high-reasoning pass to spend time on this wiring.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-SIGN-SYNDROME-UNCONDITIONAL-DECOUPLING`
> from `self_dual_wreath_sign_syndrome_unconditional_decoupling.py`, with the
> matching representation artifact. Preserve the exact scope: the fair-lifted
> raw syndrome has chi-square at most `4V_n+3V5_n` and decouples without a
> self-conjugate-mass assumption. Orbit-adaptive syndrome mutual information,
> base-orbit dependence, coherent phases, classical separation, algorithms,
> and speedup remain open/false. Add mechanical wiring and dispatch tests, run
> the five focused tests and script, and do not broaden the result.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-KL-CHAIN-REDUCTION`
> from `self_dual_wreath_sign_orbit_kl_chain_reduction.py`, with the matching
> representation artifact. Preserve the lossless decomposition into base
> sign-orbit KL plus conditional three-bit syndrome KL. Do not infer that
> either term vanishes from finite controls. Base-orbit asymptotics,
> orbit-syndrome mutual information, coherent phases, classical separation,
> algorithms, and speedup remain open/false. Add mechanical wiring and clean
> dispatch tests; run the five focused tests and script.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BASE-ORBIT-REDUCTION`
> from `self_dual_wreath_alternating_base_orbit_reduction.py`, with the
> matching representation artifact. Preserve the exact claim that base sign
> orbits are coarse `A_n` weak-Fourier labels and the input word map restricts
> to `g,h,k in A_n`. Do not infer trimmed mixing or survival. The trivial
> coarse label still creates a rare tail; dimension-trimmed `A_n` KL,
> classical separation, coherent phases, algorithms, and speedup remain
> open/false. Add mechanical wiring/dispatch tests and run the five focused
> tests plus the script.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-PARITY-COSET-CHANNEL`
> from `self_dual_wreath_alternating_parity_coset_channel.py`, with the
> matching representation artifact. Preserve only the exact reduction:
> conditional sign syndrome has Walsh coefficients `F_x/F_0` for the eight
> input-parity cosets, and tetrahedral symmetry reduces the seven nonzero
> sectors to four face twists and three opposite-complement twists. The `S_5`
> annealed ratio moments are finite diagnostics and may be dominated by
> low-dimensional tails. Do not mark either dimension-trimmed mixing gate,
> adaptive survival, coherent value, classical separation, algorithm, or
> speedup true. Add mechanical registry/runner/CLI wiring and a clean dispatch
> test; run the five focused tests and the script.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-CHARACTER-TRIANGLE-BARRIER` from
> `self_dual_wreath_character_triangle_barrier.py`, with the matching
> representation artifact. Preserve its narrow scope: even the idealized
> assumption `|chi|<=1` leaves a divergent canonical bound after termwise
> triangle inequality, so that proof strategy is eliminated. This does not
> prove adaptive energy decay or survival and does not invalidate
> cancellation-preserving uses of Teyssier--Thevenin or Lifschitz--Marmor.
> Keep all research claim gates false except the proof-strategy no-go. Add
> mechanical wiring and a clean dispatch test; run the five focused tests and
> the script.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-PROJECTED-PARITY-COSET-KERNEL` from
> `self_dual_wreath_projected_parity_coset_kernel.py`, with the matching
> representation artifact. Preserve the exact same-parity sign-orbit collapse,
> projected class-kernel contraction, and all-irrep class-collision identity.
> Tiny finite trims that make an energy zero are not asymptotic results. Keep
> both canonical kernel estimates, adaptive decay/survival, classical
> separation, algorithm, and speedup false. Add mechanical wiring and a clean
> dispatch test; run the five focused tests and the script.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-ADAPTIVE-SYNDROME-TRIM-TRANSFER`
> from `self_dual_wreath_adaptive_syndrome_trim_transfer.py`, with the matching
> representation artifact. Preserve the exact denominator-free TV transfer
> and the identity `S_B=M_full-M_base=C_full-C_base`. The canonical face and
> opposite-complement energy estimates are not proved, and the finite `S_5`
> retained energy/TV do not establish survival. Coarse `A_n` base mixing,
> coherent signal, classical separation, algorithm, and speedup remain
> false/open. Add mechanical registry/runner/CLI wiring and a clean dispatch
> test; run the five focused tests and the script.

> Also wire
> `EXP-CODE-SELF-DUAL-WREATH-DENSE-AUTOMATON-FIBER-DYADIC-BOUNDARY`
> from `self_dual_wreath_dense_automaton_fiber_dyadic_boundary.py`, with the
> matching representation artifact. Preserve the exact boundary: dense fibers
> have `floor(log2(1/delta))` rank and non-dyadic uniformly mixed classes have
> a scalar pressure gap. Exact balanced dyadic full fibers are also eliminated
> by the target/scalar dichotomy now recorded in the module. Near-uniform
> dyadic fibers, growing-state automata, interleaved leaves, natural `M4`,
> algorithms, and speedup remain open/false.
> Add only mechanical registry/runner/CLI/tests and run the six focused tests;
> do not broaden the theorem.

> Also wire `EXP-CODE-SELF-DUAL-WREATH-DYADIC-MODULAR-FIBER-TORSION-NO-GO`
> from `self_dual_wreath_dyadic_modular_fiber_torsion_no_go.py`, with its
> matching representation artifact. Preserve the all-width statement
> `P(U_(m,u))=C_m` and the `S_n` exponent `1-1/m`. It kills only fixed cyclic
> dyadic Hamming-modulus fibers. Nonabelian dyadic automata, near-uniform
> fibers, growing modulus, interleaved leaves, natural `M4`, algorithms, and
> speedup remain open/false. Add mechanical dispatch/registry/tests, run the
> five focused tests and script, and do not generalize the theorem.

> **Current user policy overrides older commit instructions below.** Do not
> commit each task or subsystem. Batch the mechanical backlog into one large,
> coherent checkpoint, and push only after that checkpoint passes focused
> validation. Leave all user-owned `ag-remote/` deletions untouched.

> **Newest binary hidden-involution handoff delta (2026-08-11).** Mechanically
> inventory and wire these eight completed theorem reports without changing
> formulas or claim gates:
>
> - `EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION` from
>   `coset_hidden_involution_binary_decision_reduction.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD` from
>   `coset_hidden_involution_fourth_moment_threshold.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY` from
>   `coset_hidden_involution_query_separation_boundary.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY` from
>   `coset_hidden_involution_threshold_compiler_boundary.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION` from
>   `coset_hidden_involution_support_span_reduction.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION` from
>   `coset_hidden_involution_orbit_hull_twirl_reduction.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION` from
>   `coset_hidden_involution_multiplicity_support_obstruction.py`;
> - `EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO` from
>   `coset_hidden_involution_support_filter_no_go.py`.
>
> Artifacts use matching basenames under `research/representation/`, except
> the query-separation artifact under `research/classical_baselines/`. Add
> pattern-following runner/CLI dispatch, registry records, concise README
> exposure, and clean dispatch tests. Then run the eight scripts, affected
> tests, downstream registry refreshes, syntax checks, and
> `python qsearch.py validate`. Preserve these boundaries:
>
> - `Theta(log M)` sample complexity and polynomial finite-HSP quantum query
>   complexity are prior art, not discoveries here.
> - The classical `Omega(sqrt(M))` bound is for the opaque random-label oracle,
>   not a natural-input time lower bound.
> - Finite proper multiplicity support is not an all-`n` theorem.
> - The newest no-go covers globally bounded scalar polynomial/QSVT effects of
>   the normalization-one `A_k` encoding. It does not cover sector-conditioned
>   normalization, direct branching transforms, arbitrary circuits, graph
>   isomorphism algorithms, or dequantization.
> - Keep efficient binary algorithm, graph-isomorphism algorithm, new quantum
>   algorithm, and speedup gates false.
> - Verify the exact moment identity and the `Omega(sqrt(M))` distributional
>   degree argument; do not substitute a finite spectral trend.

> **Newest DCP affine-flat handoff delta (2026-08-11).** Mechanically wire
> `EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO` from
> `dcp_linear_reparameterization_affine_flat_no_go.py`, with artifact
> `research/phase_workbench/dcp_linear_reparameterization_affine_flat_no_go.json`.
> Add the pattern-following runner/CLI/registry entries, a negative-result
> record for adaptive affine-product preparation, and clean dispatch tests.
> Preserve these gates exactly: every adaptive `GL(m,2)` large-affine-component
> route and every polynomial cancellation-free support-contained affine cover
> are false; arbitrary linear-split MPS with cancellation, stabilizer rank with
> cancellation, nonlinear tensorization, general circuits, polynomial subset-
> sum solvers, and speedup remain open/false as recorded. The theorem is the
> parity-feature Smith/Hadamard bound plus the all-flat union count, not a
> finite random search. Run the module's 7 focused tests and the 29-test
> affected chain before downstream validation.

> **Newest DCP compact-CNOT handoff delta (2026-08-11).** Mechanically wire
> `EXP-DHS-DCP-CNOT-LINEAR-SPLIT-ENTANGLEMENT-NO-GO` from
> `dcp_cnot_linear_split_entanglement_no_go.py`, with artifact
> `research/phase_workbench/dcp_cnot_linear_split_entanglement_no_go.json`.
> Add runner/CLI/registry inventory, a scoped negative-result record for
> compact adaptive linear MPS/QTT preparation, and dispatch tests. Preserve
> the corrected side moment `E[(X)_k]<=2^(dk+1)` for `q+d` side variables and
> the explicit union over every CNOT sequence, output-coordinate split,
> row/column coset, and target. Preserve these gates: the
> `G=o(q^(4/3)/(log q)^(4/3))` balanced linear-split route is closed even with
> matrix cancellation; dense `Theta(q^2)`/all-`GL` transforms, nonlinear maps,
> unbalanced tensor contractions, general circuits, decoding, a DCP speedup,
> and a new quantum algorithm remain open/false. Run the module's 6 focused
> tests and the 35-test affected theorem chain before downstream validation.

> **Newest natural component-commutator handoff delta (2026-08-09):** inventory
> and mechanically wire these eighteen completed theorem reports:
>
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER`
>   from `self_dual_wreath_component_commutator_collision_free_transfer.py`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY`
>   from `self_dual_wreath_component_green_ridge_stability.py`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION`
>   from `self_dual_wreath_component_hamming_orbit_reduction.py`;
> - `EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE`
>   from `self_dual_wreath_natural_leaf_commutator_trace_profile.py`;
> - `EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM`
>   from `self_dual_wreath_leaf_marked_green_word_normal_form.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY`
>   from `self_dual_wreath_marked_relation_topology.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH`
>   from `self_dual_wreath_marked_pressure_obstruction_search.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS`
>   from `self_dual_wreath_mixed_split_target_genus.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION`
>   from `self_dual_wreath_relative_surface_factorization.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE`
>   from `self_dual_wreath_two_partition_ribbon_surface.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY`
>   from `self_dual_wreath_support_affine_rank_entropy.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE`
>   from `self_dual_wreath_linear_code_support_pressure.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY`
>   from `self_dual_wreath_frame_subword_entropy.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE`
>   from `self_dual_wreath_contiguous_all_a_support_pressure.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION`
>   from `self_dual_wreath_contiguous_frame_target_factorization.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED`
>   from `self_dual_wreath_target_survival_surface_seed.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY`
>   from `self_dual_wreath_periodic_frame_fiber_counterfamily.py`.
> - `EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE`
>   from `self_dual_wreath_periodic_frame_rank_collapse.py`.
>
> Suggested CLI names are respectively
> `code-wreath-component-commutator-conditioning`,
> `code-wreath-component-green-ridge`,
> `code-wreath-component-hamming-profile`,
> `code-wreath-natural-leaf-trace-profile`,
> `code-wreath-leaf-marked-green-words`,
> `code-wreath-marked-relation-topology`,
> `code-wreath-marked-pressure-obstructions`,
> `code-wreath-mixed-split-target-genus`, and
> `code-wreath-relative-surface-factorization`, and
> `code-wreath-two-partition-ribbon-surface`, and
> `code-wreath-support-affine-rank-entropy`, and
> `code-wreath-linear-code-support-pressure`, and
> `code-wreath-frame-subword-entropy`,
> `code-wreath-contiguous-all-a-support-pressure`, and
> `code-wreath-contiguous-frame-target-factorization`, and
> `code-wreath-target-survival-surface-seed`,
> `code-wreath-periodic-frame-fibers`, and
> `code-wreath-periodic-frame-rank-collapse`. Copy an existing theorem-report
> dispatch/runner/registry pattern, add clean dispatch tests, and expose the
> artifacts without altering formulas or claim gates. Run the eighteen scripts
> first, then their focused tests. Preserve these scope rules exactly:
>
> - Sharp conditioning transfer preserves a separately proved independent
>   inverse-polynomial `M4`; it does not prove that signal exists. Its finite
>   `P_cf` rows are preasymptotic.
> - Green/ridge stability is conditional on a positive ridge gap and a small
>   average trace-weighted polar ratio. Neither natural premise is proved.
> - The Hamming theorem reduces pair enumeration; symmetry does not make a
>   typical pair gap positive.
> - The natural leaf trace profile is uncompressed. Generic Green whitening
>   and common compression can erase it.
> - The leaf-marked theorem is an exact word-map and sibling-frame-algebra
>   reduction. It does not prove growing-word rigidity or a positive Green
>   pair gap. The literature entries explicitly say no cited paper covers the
>   required regime.
> - The marked-relation theorem removes copy-depth growth at fixed degree and
>   certifies every pressure profile through two frame tokens. Its four
>   degree-three rows are selected adversarial controls, not an exhaustive
>   degree-three or growing-degree theorem. Preserve the 116 unclassified
>   two-token residual topologies, the false
>   `degree_three_complete_pressure_separation_proved` flag, and all mixed
>   target-character gates. Do not replace leading `|S_n|` exponents by
>   finite uniform constants.
> - The pressure-obstruction search visits deterministic all-`A` beams through
>   degree six plus positive-genus, support-uncancelled mixed `A/B` beams
>   through degree six and stores exact finalist presentations. All current
>   scalar-pressure finalists are certified with at least one extra exponent
>   of margin, but beam coverage is not a theorem. Preserve
>   `asymptotic_counterexample_count=0`,
>   `growing_degree_pressure_theorem_count=0`, and the false universal claim
>   gate. The constant-zero trailing lift is an exact free-product theorem;
>   constant-one/interior lifts and irreducible support cores remain open.
>   The `EFAEFBBB` target control is resolved exactly, not by extrapolating
>   its `S3`-`S5` screens. The target is `q^-1*r4^-1*q` for the fourth
>   residual relator and `q=(-5,-8,7,8,4,5)`. Preserve the exact cyclic-word
>   verifier and the finite fingerprints, but remove the obsolete
>   finite-residual conjecture. This proves only that retained row; it must
>   not flip the universal mixed target-character claim gate.
> - The split-target theorem proves genus `r-1` and character factor
>   `d_nu^-2(r-1)` only under the two split relations. Additional support
>   relations remain the open relative-surface problem.
> - The `EFBEBFB` relative-surface factorization proves one exact disjoint
>   commutator row, with count `|G|^3 k(G)` and character factor `d_nu^-2`.
>   It does not classify all positive-genus profiles or prove the growing-word
>   component moment.
> - The two-partition ribbon theorem classifies one split/support assignment
>   pair exactly and is used in pressure scoring. It does not pay for the
>   entropy of a full multi-assignment support; preserve the false
>   `full_support_profile_ribbon_complex_theorem_proved` gate.
> - The affine-rank theorem proves
>   `R>=2+0.5log2|S|+0.5log2|D|` only for rational exponent-sum rank. It does
>   not lift rank to `S_n` solution loss. Preserve the false nonabelian-lift
>   and final-crossing gates. The marked primitive-cube row is exactly
>   `(C_3*Z)xZ`, has `S3` count 42 and leading `S_n` exponent `5/3`; it does
>   not force the cube generator to identity.
> - The linear-code theorem proves growing-degree crossing pressure only for
>   `E A^u F E F` with both supports binary linear subspaces. Preserve the
>   exact `F_(u-r)*Z^2` selected-presentation proof and pressure
>   `-1-|dim(S)-dim(D)|/2`. Do not extend it to affine cosets, arbitrary
>   supports, B frames, interleaved leaves, or mixed target characters.
> - The frame-subword theorem gives the exact conditional reduction
>   `P(S union D)*Z^2` for `E A^u F E F` with `0 in D`, and now proves for
>   every zero-containing `U` and every finite group `G` that
>   `#Hom(P(U),G)<=|G|^(u-log2|U|)`. It now also proves the stronger integer
>   generator bound `floor(u-log2|U|)` using suffix-branch anchors and the
>   conditional-entropy chain rule. The proofs are the explicit triangular XOR
>   re-rooting automorphism plus last-coordinate/suffix elimination. Preserve the true
>   `growing_width_frame_subword_entropy_proved` gate. Width-four exhaustion
>   and width-five stress are implementation controls, not the proof.
> - The contiguous all-A theorem removes the zero-base and linear-support
>   restrictions. Same cells form an identity fiber, different cells a common-
>   value fiber, and fixed frame assignments leave at most `|G|k(G)` outer
>   solutions. Preserve the exact arbitrary-support scalar pressure `<=-1`,
>   but keep every target-character and speedup gate false.
> - The contiguous mixed-frame theorem extends scalar pressure to arbitrary
>   A/B frame types and reduces the full target exactly to the frame character
>   of `R=w_A^-1(x_1...x_u)` under a centralizer-weighted measure. Pressure
>   saturation under the strengthened bound requires equal power-of-two support
>   sizes and forces target identity. The exact identity-frame `S3` lift only
>   makes the obsolete real entropy margin tend to zero; the integer suffix-
>   branch bound raises its actual certified margin toward one. Preserve the
>   false weighted-character theorem, false asymptotic `S_n` lower-bound gate,
>   false global uniform-gap gate, and false speedup gate. A genuine uniform-gap
>   falsifier now needs a structurally valid target-surviving profile on the
>   opposite side of a power-of-two boundary.
> - The surface-seed theorem closes that exact identity-frame lift. Every
>   appended generator is forced to identity, leaving a four-generator genus-
>   two surface presentation and one handle-commutator target. Preserve the
>   exact standard-character formula, its
>   `2/(n-1)^2+O(n^-5/2)` asymptotic, and the `O(1/n)` uniform decay for every
>   nontrivial nonsign irrep. Trivial/sign targets equal one. Do not extend the
>   result to nonidentity-frame lifts or other surface seeds. The same module
>   now classifies the pruned power-boundary supports `2^k-1,2^k`: the generic
>   integer-certificate margin tends to zero, but the exact presentation is a
>   genus-two surface group with one free generator, has `S3` count `2916`,
>   preserves the handle target law, and has true scalar pressure margin above
>   one. Preserve the distinction between generic-certificate falsification and
>   actual-presentation survival.
> - The periodic-fiber report proves an exact nonidentity `S3` support family
>   with support-only margin `Theta(32^-k)`. Its companion rank-collapse theorem
>   now closes, rather than promotes, the family. The neutral six-period block
>   and exact suffix witnesses leave at most three frame generators for every
>   `k=6m+1`; the mixed outer equation gives at most `|G|^4 k(G)` full solutions.
>   Preserve the exact fiber formula
>   `(16*2^(30m)+8*2^(24m)-4*2^(6m)-2)/9`, the uniform pressure-margin lower
>   bound `1-0.5*log2(3/2)`, the false leading-mass and speedup gates, and the
>   distinction between falsifying a support-only certificate gap and finding
>   a surviving channel. The four materialized presentations are controls, not
>   the all-period proof; the suffix-branch concatenation certificate is the
>   proof.
> - Keep `natural_positive_green_pair_gap_theorem_count`,
>   `natural_component_M4_positive`, `new_quantum_algorithm_count`, and every
>   speedup gate false.
>
> The next mathematical task is **not** mechanical and must not be attempted
> by changing a flag after finite screens: generalize the suffix-branch rank
> argument to dense fixed-state frame automata, or construct a precise
> counterexample with growing suffix-branch dimension. Then bound or construct
> asymptotic `S_n` mass for the centralizer-weighted frame character problem in
> `self_dual_wreath_contiguous_frame_target_factorization.py` outside the now-
> closed identity-frame genus-two seed and the now-closed periodic `S3` family,
> then connect it
> to the growing-degree partially pinned `Q_0,Q_1` rigidity problem in
> `research/AGENT_HANDOFF.md`. The exact `S3` identity-frame lift no longer
> proves the strongest scalar margin nonuniform. Gemini may add plumbing,
> refresh downstream registries, and run repetitive validation, but must leave
> the weighted-character and `S_n` asymptotic gates unresolved.

> **Newest unwired theorem modules:** also inventory and mechanically wire
> `EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER`,
> `EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION`,
> `EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION`,
> `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS`, and
> `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE`,
> `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS`,
> `EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE`,
> `EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM`,
> `EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER`,
> `EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE`, and
> `EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN`, and
> `EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT`, and
> `EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE`,
> `EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK`,
> `EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER`, and
> `EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO`,
> `EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY`,
> `EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION`,
> `EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION`,
> `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY`,
> `EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD`,
> `EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION`, and
> `EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW`, and
> `EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK`, and
> `EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET`, and
> `EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM`,
> `EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT`,
> `EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY`, and
> `EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO` by copying an
> existing theorem-report dispatch pattern. Do not alter their mathematics,
> claim gates, control parameters, or artifacts. The Jacobi module is only a
> Gaussian surrogate: never describe it as natural-frame conditioning or an
> algorithm. The affine common-outlier theorem excludes only exact
> width-sized eigenvalues, not near-outliers or the natural edge. The
> pair-angle module refutes only an unrefined full-regular angle criterion; it
> is not a physical typical-block no-go. The Kronecker positivity and
> multiplicity theorems require independent Plancherel factors and are
> pointwise in a fixed target or fixed pair; never rewrite them as arbitrary
> coupling, uniform-partition, all-target, or all-pair theorems. The Hamming
> result is a density-one stratum theorem, not simultaneous control of every
> pair. None of these results proves coherent incidence or a node-frame edge.
> The natural pair-carrier module proves an exact multiplicity-weighted
> `d_alpha^4` law and asymptotic quenched convergence, but its basic Markov/TV
> finite bound is loose. Do not convert its tiny low-dimensional carrier mass
> into a PGM state-mass, full-frame-edge, or algorithm claim.
> The return-walk module removes explicit coloring enumeration but does not
> prove a growing-order collision-free return bound. Preserve its negative
> conclusion that a coarse global gap is insufficient.
> The hierarchy pair-common rank module proves only a probabilistic
> ambient-relative rank trim for exact singular-value-one common directions.
> Its all-target quantity is an unweighted Markov/union budget, not PGM mass,
> a naturally weighted direct-sum rank, an operator-norm bound, a noncommon
> edge theorem, or an algorithm. Preserve the root antipodal target exception
> and keep every noncommon/near-outlier/speedup gate closed.
> The hierarchy low-carrier module proves a rank--correlation tradeoff after
> trimming both endpoint singular spaces. Its conditioned all-target trim is
> an unweighted Markov/union budget, not accepted state mass. The residual
> pair bound does not prove a row-sum, frame-edge, Racah-incidence, decoder,
> or algorithm theorem; preserve all of those open gates and the statement
> that the elementary quarter exponent is not known optimal.
> The complete S6 audit is finite and restricted to the eight source irreps
> of dimension at most nine. The scalar holonomy theorem applies only to one
> multiplicity-scalar affine-plane channel. The support-pressure theorem then
> falsifies extrapolating those finite disjoint triangles into orthogonal
> all-depth atoms. Do not describe the pressure no-go as a bad-frame theorem:
> overlapping positive channels may remain well conditioned. Keep matrix
> traffic, association-scheme, frame-edge, PGM-mass, decoder, and speedup gates
> closed.

> **Newest high-reasoning handoff delta (2026-08-08):** inventory and wire the
> following five modules after regenerating the stale unwired count in this
> plan:
> `EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE`,
> `EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY`,
> `EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY`,
> `EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT`, and
> `EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION`.
> Their scripts, focused tests, and live JSON artifacts already exist. Copy
> dispatch/registry patterns only; do not edit their mathematics. Preserve
> these scope rules exactly:
>
> - A rescaled orientation-frame cutoff `tau` corresponds to raw physical PGM
>   cutoff `tau/2^k`. Never apply the same absolute cutoff to both frames.
> - The flat-frame `Theta(sqrt(2^k))` result is a generic normalized-access
>   boundary, not an arbitrary quantum-circuit lower bound.
> - The `d_alpha^4` law is exactly native trace mass only after conditioning on
>   the active pair node. It is not complete many-orientation PGM mass.
> - Normalized cross-overlap QSVT is superpolynomial on natural active pair
>   mass, but coherent GPE implements the pair polar directly and polynomially.
>   Do not report inverse carrier dimension or a full Kronecker transform as a
>   surviving pair-transport requirement.
> - The GPE theorem proves pair transport, not a complete PGM polar or hidden
>   permutation decoder. Different edge decompositions retain nontrivial Racah
>   holonomy.
> - The holonomy theorem is an exact flat equal-rank fixed-space reduction. A
>   polynomial resolver is conditional on coherent generator SELECT and an
>   inverse-polynomial natural frustration gap. Partial supports, emergent
>   child-span dependencies, the complete relative polar, decoder, and speedup
>   remain open.
>
> Suggested CLI names are `code-wreath-trace-weighted-pgm-bridge`,
> `code-wreath-native-frame-access-boundary`,
> `code-wreath-pair-transport-native-mass`,
> `code-wreath-gpe-pair-polar`, and `code-wreath-gpe-holonomy-resolver`.
> Add clean dispatch tests, preserve `speedup_claim_allowed=false`, refresh
> downstream workflows, and batch all five into the next large checkpoint.

> **Recursive-node compiler handoff delta (2026-08-08):** also inventory and
> wire `EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER` with suggested
> CLI name `code-wreath-gpe-recursive-node-compiler`. Its script, focused test,
> and live JSON artifact already exist. Preserve these scope rules exactly:
>
> - The exact recursive relation factorization separates normalized
>   minimum-energy child embeddings from a short-metric endpoint mixer.
> - Equal short metrics give an exact signed Hadamard. Noncommuting metrics can
>   require a matrix-valued mixer, and exponentially imbalanced metrics can
>   retain an exponentially small endpoint gap even when pair GPE is available.
> - A flat affine child embedding needs only affine dimension many controlled
>   transport stages and no square-root support-size amplification.
> - The selected W3/W5 controls have finite GPE compiler certificates because
>   the existing affine-bundle and pair-path controls match. This is not an
>   all-n affine decomposition or uniform coherent path/SELECT theorem.
> - Keep `all_n_structured_child_embedding_proved`,
>   `polynomial_uniform_generator_select_proved`,
>   `natural_recursive_endpoint_gap_proved`,
>   `recursive_orientation_polar_proved`, and `speedup_claim_allowed` false.
>
> Add only copied registry/runner/CLI dispatch and clean dispatch tests. Do not
> alter the theorem, counterfamilies, finite controls, or claim gates.

> **Partial-support falsifier handoff delta (2026-08-08):** also inventory and
> wire `EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING` with
> suggested CLI name `code-wreath-partial-support-child-embedding`. Preserve
> these scope rules exactly:
>
> - Sparse leaf block Grams exactly reconstruct the finite normalized child
>   embeddings and their component POVMs; this avoids dense ambient projectors.
> - The globally source-distinct S6 control retains affine masks but falsifies
>   scalar full-fiber effects. It requires matrix partial support and has a
>   nonzero cross-child effect commutator.
> - This falsifies a universal scalar coefficient-affine theorem. It does not
>   prove that matrix partial-support nodes have positive asymptotic native PGM
>   mass and does not kill the collective PGM architecture.
> - Keep `matrix_partial_support_gpe_compiler_proved`,
>   `positive_native_mass_partial_support_obstruction_proved`,
>   `recursive_orientation_polar_proved`, and `speedup_claim_allowed` false.
>
> Wire by copying dispatch patterns only. Do not soften the S6 negative result
> and do not promote its finite spectrum into an asymptotic no-go.

> **Partial-support source-mass handoff delta (2026-08-08):** also inventory
> and wire `EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY`
> with suggested CLI name `code-wreath-partial-support-source-mass`. Preserve
> these scope rules exactly:
>
> - The direct S6 mechanism requires trivial and sign source irreps and has
>   conditioned mass at most `m(m-1)/(n!)^2/P_cf`.
> - Any polynomial-dimensional source anchor has conditioned union mass at
>   most `m p(n)L^2/(n! P_cf)`, hence is superpolynomially small.
> - This makes the known S6 mechanism asymptotically negligible but does not
>   restore universal scalar affine fibers. Matrix partial supports formed
>   entirely from typical high-dimensional sources remain uncontrolled.
> - Keep `scalar_affine_behavior_holds_on_positive_native_bulk`,
>   `high_dimension_matrix_partial_support_mass_controlled`,
>   `matrix_partial_support_gpe_compiler_proved`,
>   `recursive_orientation_polar_proved`, and `speedup_claim_allowed` false.
>
> Wire only dispatch/registry/CLI and focused clean-dispatch tests. Do not
> change the asymptotic theorem or reinterpret finite benchmark crossings as
> premises of the proof.

> **Matrix-POVM compiler handoff delta (2026-08-08):** also inventory and wire
> `EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER` with suggested CLI
> name `code-wreath-matrix-povm-recursive-compiler`. Preserve these scope rules:
>
> - Every normalized child embedding has an exact component-POVM Naimark
>   factorization followed by component partial isometries, even when effects
>   do not commute.
> - The parent relation is the composition of endpoint and child POVM
>   dilations followed by support transport. This has no intrinsic square-root
>   outcome-count loss.
> - This is an algebraic compiler normal form, not a natural circuit. Pair GPE
>   can supply compatible support polars but does not prepare `sqrt(H_e)`.
> - The `Omega(delta^-1/4)` degree statement is a generic bounded-polynomial
>   block-encoding boundary, not an arbitrary quantum-circuit lower bound.
> - Keep `natural_component_povm_dilation_compiled`,
>   `all_n_component_support_polars_gpe_compatible`,
>   `high_dimension_partial_support_native_mass_controlled`,
>   `recursive_orientation_polar_proved`, and `speedup_claim_allowed` false.
>
> Add copied dispatch/registry/CLI wiring only. Do not claim that the Naimark
> factorization itself is an efficient implementation.

> **MRS model-scope handoff delta (2026-08-08):** also inventory and wire
> `EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION` with suggested CLI
> name `code-wreath-mrs-coherence-escape`. Preserve these scope rules exactly:
>
> - The primary-source MRS sieve measures an irrep at every pairwise combine
>   step and uses the classical irrep-labeled forest transcript.
> - `M=Delta(M)` characterizes invariance under early measurement, not
>   simulation from the classical transcript. For a fixed projective
>   transcript, transcript-only simulation requires the block-scalar condition
>   `M=C(M)`. Off-diagonal coherence is sufficient but not necessary.
> - For the full adaptive transcript POVM `{E_t}`, the physical effect must be
>   separated from `{sum_t f_t E_t:0<=f_t<=1}` on positive accepted mass.
>   Deferred measurement alone is insufficient.
> - Pair GPE is carrier-label block diagonal and does not alone prove escape.
> - The finite abstract coherence controls and S6 noncommutativity are not a
>   physical PGM witness. Keep `current_physical_pgm_outside_mrs_transcript_postprocessing`,
>   `complete_recursive_compiler_outside_mrs_class_proved`,
>   `mrs_lower_bound_avoided`, and `speedup_claim_allowed` false.
>
> Wire only copied dispatch/registry/CLI paths and focused tests. Do not change
> the literature scope or paraphrase the criterion as a lower-bound escape.

> **Newest component-effect theorem deltas (2026-08-08):** inventory and wire
> these reports by copying an existing theorem-report dispatch pattern:
>
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY`, suggested
>   CLI name `code-wreath-component-sparse-support`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION`, suggested
>   CLI name `code-wreath-component-regular-master`;
> - `EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION`, suggested CLI
>   name `code-wreath-mrs-transcript-povm`.
>
> Preserve these gates exactly. The Jacobi module is a Haar benchmark, not a
> natural-frame theorem. Small component trace does not prove a small positive
> edge. The regular-master module identifies center-valued source/common mass
> observables but proves no high-dimensional bound; its S3 control has repeated
> sources. The MRS zonotope solver proves separation only from one specified
> transcript POVM, not from every adaptive policy in the MRS class. Keep all
> natural-universality, support-SELECT, physical-PGM, all-policy MRS, decoder,
> and speedup gates false. Routine registry/dequantization/proof/frontier/CLI
> wiring and artifact refreshes belong to Gemini 3.6 Flash.

> **Final-root component-geometry theorem deltas (2026-08-08):** inventory and
> wire these reports by copying an existing theorem-report dispatch pattern:
>
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE`, suggested CLI
>   `code-wreath-component-defect-gap`;
> - `EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE`, suggested CLI
>   `code-wreath-final-root-leverage-edge`;
> - `EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN`, suggested CLI
>   `code-wreath-final-root-natural-common-span`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS`, suggested CLI
>   `code-wreath-component-defect-rank-mass`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM`, suggested CLI
>   `code-wreath-component-povm-spectral-trim`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY`, suggested
>   CLI `code-wreath-component-effect-algebra-boundary`;
> - `EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS`, suggested CLI
>   `code-wreath-natural-leaf-commutator`;
> - `EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO`, suggested CLI
>   `code-wreath-leaf-whitening-no-go`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO`,
>   suggested CLI `code-wreath-common-span-component-universality`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE`,
>   suggested CLI `code-wreath-component-commutator-trace-mass`;
> - `EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK`,
>   suggested CLI `code-wreath-component-commutator-haar`.
>
> Preserve the theorem scopes exactly. The defect bridge is deterministic and
> conditional on an actual retained minimum positive component edge. Coordinate
> block rank removes a separate trace-balance premise but does not prove that
> edge. The leverage theorem is explicitly Haar/Gaussian; its schedule claim
> has been renamed as a **surrogate** aspect claim. The natural-common-span
> theorem independently proves, on globally distinct conditional mass
> `1/9-o(1)`, common relative rank `19/128-o(1)`, child fiber aspect
> `19/520-o(1)`, and `b_max/r<=(520/19+o(1))/q`. It does not transfer the Haar
> positive edge. The defect-rank theorem then proves asymptotically full defect
> rank on the same source event and conditioned expected physical support mass
> `19/1152-o(1)` without a positive-edge premise. This resolves center-valued
> support mass, not spectral conditioning. Keep natural component-edge,
> coherent child-pseudoinverse,
> component-support SELECT, recursive-polar, decoder, and speedup gates false.
> The component spectral-trim theorem proves the state-weighted bound
> `failure<=kappa tau B/r`; it does not prove polynomial natural input
> flatness. Preserve the concentrated-state unit-failure countercontrol and
> keep coherent threshold/support compilation false.
> The effect-algebra boundary retracts any inference from full-rank
> nonscalarity to noncommutativity. Preserve the orthogonal-PVM counterexample,
> keep natural commutator central/physical mass false, and do not describe the
> finite trine or S6 controls as asymptotic evidence.
> The natural leaf theorem proves density-one inverse-polynomial commutators
> only for the original orientation projectors. The whitening no-go gives an
> exact integer-degree independent-set characterization of commuting canonical
> projection frames and a bounded-condition, duplicate-free counterfamily. It
> kills every generic full-support transfer based only on leaf commutators,
> conditioning, aspect, relative rank, distinctness, or nonscalarity. The
> common-span universality theorem then proves every POVM can arise after
> proper sibling compression; its structured counterfamily also has constant
> common rank, positive component edge, and commuting non-reciprocal spectrum.
> Neither module is a natural wreath commutativity theorem. Keep direct natural
> compressed `D_com` support, coherent simultaneous-basis/component
> compilation, MRS separation, decoder, and speedup gates false.
> The trace-mass bridge proves the exact noncrossing-minus-crossing fourth-
> moment identity and `D_com<=2I`, so a natural physically normalized scalar
> gap `M_4` would imply physical and central support at scale `M_4/2`. It does
> not prove `M_4>0`; never substitute uncompressed sibling-frame moments, Haar
> surrogates, finite S6 evidence, or nonscalarity rank for that missing result.
> The Haar benchmark has an exact finite Weingarten formula and sparse-block
> limit `alpha^2(1-alpha)`, but remains a surrogate. Preserve every
> `natural_*_proved=false` gate and the one-dimensional/two-outcome boundary
> controls.
> The finite rows through `S_48` are deliberately vacuous for common-span rank
> because the exact global-distinct probability is tiny; do not call them
> finite confirmation or contradiction of the asymptotic theorem.
>
> Add clean dispatch tests, refresh standard downstream workflows, and use the
> new natural theorem to supersede any registry text saying natural final-root
> block/fiber aspects are wholly unidentified. Do not mark the positive-edge
> obligation resolved.

> **Additional theorem artifacts from the signed-Steiner/coverage pass:**
> mechanically wire these without changing their claim gates:
> `EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY`,
> `EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY`,
> `EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE`,
> `EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM`,
> `EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE`,
> `EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION`, and
> `EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE`, and
> `EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK`. The random-gauge module
> is only an independent surrogate. The deterministic bulk theorem supersedes
> any suggestion that scalar gauge randomness is needed for a vanishing
> outlier-rank fraction. The nullity theorem controls exact scalar zero modes,
> and the bulk theorem controls per-channel coefficient rank, not PGM state
> mass. The operator theorem is conditional on diagonal coverage; the Welch
> module proves pressure forces overlap but does **not** prove tight natural
> coverage. Preserve `speedup_claim_allowed=false` throughout.
> The weighted-relation module includes every rich and non-rich orientation
> signature class and proves only a collision-free coefficient-rank bulk edge
> around relation eigenvalue two. Preserve its exact use of the prior
> relation-cokernel theorem: trimming relation image has zero ideal PGM signal
> loss, but retained relations are not proved to exhaust the synthesis
> cokernel. Do not advertise an untrimmed edge, complete projector, coherent
> decoder, or speedup.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the new theorem module
`self_dual_wreath_orientation_laplacian_gap.py` (Tasks 1-6), then clear the
real wiring backlog — a direct scan finds **57 unwired modules**, not the six
the handoff names by hand (Tasks 7-9) — and add four repository hygiene
deliverables: a claim-gate guard test, an artifact schema inventory, a runtime
budget, and README coverage (Tasks 10-14).

**Measured starting state** (regenerate rather than trust these numbers):

| quantity | value |
| --- | --- |
| modules with a `DEFAULT_EXPERIMENT_ID` | 264 |
| of those, unwired (registry and runner both absent) | 57 |
| unwired but ready (writer + test + artifact) | 56 |
| ready modules that already have `write_registry` kwargs | 15 |
| unwired and not ready | 1 (`self_dual_wreath_global_collision_free_mass`) |
| research artifacts outside the registry | 316 |
| artifacts missing `theorem_contract` | 208 |
| artifacts missing `claim_gate` | 53 |
| artifacts missing `falsifiers_triggered` | 12 |
| artifacts with `speedup_claim_allowed: true` | 0 |
| repository-wide claim-gate guard test | none exists |

**Architecture:** Identical to pass 1, which is already complete. Every
theorem module is reachable four ways: as a script, as a `qsearch.py`
subcommand, as `python qsearch.py run <EXPERIMENT-ID>`, and as a seeded
`ExperimentRecord`. This plan copies the
`EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION` wiring verbatim,
since that module was wired in pass 1 and its `write_*_report` already has the
registry keyword arguments this one needs.

**Tech Stack:** Python 3.13, `numpy`, `pytest`, stdlib `argparse`/`json`.
No new dependencies.

## Global Constraints

- Work from the repository root: `/Users/jaspersands/Desktop/quantum algorithm search`.
- Branch is `main`. **Do not** run `git reset`, `git checkout -- .`,
  `git stash`, or `git clean`. Do not discard work you did not write.
- **Do not touch anything under `ag-remote/`.**
- **Do not change any mathematics.** Do not edit formulas, thresholds,
  tolerances, control lists, sample counts, screen caps, workload caps,
  theorem contracts, proof obligations, adversarial audits, or falsifier
  strings. If a test fails because a number changed, revert your edit; do not
  adjust the expected value.
- **Never set `speedup_claim_allowed` to `true`.**
- **Never describe the new floor as an algorithm, a conditioning proof, or a
  speedup.** It is a metric lower bound conditional on an unproved vertex
  trivialization. Copy the wording from the module's `theorem_contract` and
  `adversarial_audit`; do not paraphrase it into something stronger.
- Preserve every existing negative result. Do not delete registry rows.
- Do not run the full repository suite in one go. Run only the focused tests
  named in each task. Task 12 walks the wreath tests one file at a time on
  purpose; that is measurement, not a suite run.
- Tasks 1-6 end in exactly one commit. Tasks 7-14 commit per batch as stated.
- Python invocation is plain `python` from the repository root.

### The judgment boundary

Several tasks stop deliberately short of finishing a job. That is the design,
not an oversight. **Never write new content that asserts what a module proved,
refuted, or left open.** Specifically, do not author:

- a `theorem_contract`, a `claim_gate`, or a `reason` string;
- a `NegativeResultRecord` claim, `reason_invalid`, or `lesson`;
- a `hypothesis`, `positive_signal`, or `falsifiers` entry that is not a
  phrase copied from the module's own docstring or artifact;
- a README sentence comparing two results or characterizing progress;
- a test assertion whose expected value you chose yourself.

Where a task hits that boundary it says so and tells you to record and report
instead. The list of things you declined to write is the most valuable output
of this plan — it becomes the next high-reasoning pass's work queue.

### The module being wired

| | value |
| --- | --- |
| file | `self_dual_wreath_orientation_laplacian_gap.py` |
| experiment id | `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP` |
| CLI name | `code-wreath-orientation-laplacian-gap` |
| artifact | `research/representation/self_dual_wreath_orientation_laplacian_gap.json` |
| report writer | `write_orientation_laplacian_gap_report` |
| test file | `tests/test_self_dual_wreath_orientation_laplacian_gap.py` |
| candidate id | `CODE-COSET-COLLECTIVE` |
| runtime | about 48 seconds at default arguments |

The report writer **already** accepts `write_registry`,
`registry_experiment_id`, `registry_candidate_id`, and `registry_result_id`,
and already upserts `NEG-CODE-WREATH-WEIGHTED-DEGREE-METRIC-COLLAPSE`. There
is no Task-1-style module edit in this pass.

---

## File Structure

- `research_registry.py` — Task 1 adds one `ExperimentRecord` after the
  multistar record whose `id=` line is at line 7661.
- `experiment_runner.py` — Task 2 edits three places: the imports beside the
  multistar import, the `COSET_EXPERIMENTS` set (the multistar id is at line
  888), the `priority` dict inside `select_next_experiment()` (the multistar
  entry is at line 2081), and the dispatch chain (the multistar branch is at
  line 3956).
- `qsearch.py` — Task 3 edits three places: the imports beside the multistar
  import, a new `command_*` function after
  `command_code_wreath_multistar_degree` (line 7009), and a new
  `add_parser` block after the `code_wreath_multistar_degree` block
  (line 13342).
- `tests/test_experiment_runner.py` — Task 3 adds one dispatch test.
- `README.md` — Task 4 corrects the multistar paragraph and adds one block.
- Downstream `research/**` artifacts — Task 5 regenerates them.

---

### Task 1: Seed the experiment record

**Files:**
- Modify: `research_registry.py` (immediately after the `ExperimentRecord` whose `id="EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"`, whose `id=` line is at line 7661)

**Interfaces:**
- Consumes: the `ExperimentRecord` dataclass already imported in that file. Its fields, in the order used below, are `id`, `candidate_id`, `title`, `status`, `hypothesis`, `protocol`, `positive_signal`, `falsifiers`, `metrics`, `dependencies`, `next_actions`.
- Produces: a seeded record that Tasks 2 and 3 read by id.

- [ ] **Step 1: Locate the insertion point**

Run: `grep -n 'EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION' research_registry.py`

Expected: one line number near 7661. Scroll down from there to the closing
`),` of that `ExperimentRecord(` call — the line after its `next_actions=[...]`
list closes. Insert the new record immediately after that `),`.

- [ ] **Step 2: Insert the record**

```python
        ExperimentRecord(
            id="EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Width-independent orientation Laplacian floor",
            status="planned",
            hypothesis=(
                "Keeping the incidence signs of the pair-core relation "
                "complex gives a smallest positive eigenvalue that does not "
                "degrade with merge width, so the vacuous absolute-weight "
                "certificate did not imply bad conditioning."
            ),
            protocol=(
                "Prove the Dirichlet form and kernel of the projector-"
                "weighted orientation Laplacian, split the commuting case "
                "into scalar complete-graph Laplacians over Boolean atoms on "
                "affine supports, derive the exact p-star spectrum, and screen "
                "the resulting 2-2gamma floor on full live graphs while "
                "measuring how many distinct residual correlations survive on "
                "natural threshold portfolios."
            ),
            positive_signal=(
                "The atom prediction reproduces exact spectra, the p-star law "
                "matches the known S6 noncommuting counterexample, no full "
                "live graph violates the floor, and the residual correlation "
                "collapses to a single value at the largest sampled degree."
            ),
            falsifiers=[
                "A full live graph has a smallest positive eigenvalue below 2-2gamma_max.",
                "A star subgraph evaluation is presented as evidence about a merge.",
                "The measured single residual correlation is described as a proof of vertex trivialization.",
                "A metric floor is described as all-depth conditioning, a graded-defect bound, or an algorithm.",
                "Vertex-disjoint core overlaps are inserted into the relation Gram, which has no such blocks.",
            ],
            metrics=[
                "dirichlet_form_theorem_count",
                "commuting_atom_splitting_theorem_count",
                "exact_p_star_spectrum_theorem_count",
                "uniform_transport_width_independent_floor_theorem_count",
                "commuting_atom_control_count",
                "commuting_atom_failure_count",
                "star_law_control_count",
                "star_law_failure_count",
                "maximum_star_law_residual",
                "screened_full_graph_control_count",
                "screened_workload_skipped_control_count",
                "screened_nontrivial_correlation_control_count",
                "screened_floor_violation_count",
                "minimum_observed_positive_eigenvalue",
                "degrees_with_single_residual_correlation",
                "residual_correlation_count_is_collapsing",
                "largest_degree_distinct_correlation_count",
                "largest_degree_uniform_transport_floor",
                "largest_degree_sign_blind_floor",
                "vertex_trivialization_proof_count",
                "all_depth_conditioning_theorem_count",
                "new_quantum_algorithm_count",
            ],
            dependencies=[
                "self_dual_wreath_orientation_laplacian_gap.py",
                "self_dual_wreath_multistar_degree_obstruction.py",
                "self_dual_wreath_pair_core_carrier_factorization.py",
                "self_dual_wreath_common_core_atomization.py",
                "signed subspace incidence and graph Laplacian duality",
            ],
            next_actions=[
                "Run qsearch.py code-wreath-orientation-laplacian-gap.",
                "Construct the vertex isometry factorization or refute it on a natural adjacent pair.",
                "Repeat the star and atom calculations with the J grading to bound the graded defect.",
            ],
        ),
```

- [ ] **Step 3: Verify the file parses and the record is seeded**

```bash
python -c "
import research_registry
from research_registry import seed_candidate_records
_c, experiments = seed_candidate_records()
ids = {r.id for r in experiments}
print('EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP' in ids)
"
```

Expected: `True`.

---

### Task 2: Register the id in the experiment runner

**Files:**
- Modify: `experiment_runner.py` — imports beside the multistar import, `COSET_EXPERIMENTS` (multistar id at line 888), `priority` dict (multistar entry at line 2081), dispatch chain (multistar branch at line 3956)

**Interfaces:**
- Consumes: `write_orientation_laplacian_gap_report(write_registry, registry_experiment_id, registry_candidate_id, registry_result_id)`, already present in the module.
- Produces: `python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP` executes the module.

- [ ] **Step 1: Add the import**

Find in `experiment_runner.py`:

```python
from self_dual_wreath_multistar_degree_obstruction import (
    write_multistar_degree_obstruction_report,
)
```

Insert immediately after it:

```python
from self_dual_wreath_orientation_laplacian_gap import (
    write_orientation_laplacian_gap_report,
)
```

- [ ] **Step 2: Add the id to `COSET_EXPERIMENTS`**

Find the line
`    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION",`
(about line 888). Insert immediately after it:

```python
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP",
```

- [ ] **Step 3: Add the id to the `priority` dict**

Find the line
`        "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION": 120,`
(about line 2081). Insert immediately after it:

```python
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP": 127,
```

127 is unused; the current maximum is 126. Do not renumber anything else.

- [ ] **Step 4: Add the dispatch branch**

Find this block (about line 3956):

```python
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"
        ):
            payload = write_multistar_degree_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
```

Insert immediately after it:

```python
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP"
        ):
            payload = write_orientation_laplacian_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
```

- [ ] **Step 5: Verify the module imports and the runner tests pass**

```bash
python -c "import experiment_runner; print('ok')" && python -m pytest tests/test_experiment_runner.py -q
```

Expected: `ok`, then all tests in that file pass.

---

### Task 3: Add the `qsearch.py` subcommand and its dispatch test

**Files:**
- Modify: `qsearch.py` — imports beside the multistar import, a new `command_*` function after `command_code_wreath_multistar_degree` (line 7009), a new `add_parser` block after the `code_wreath_multistar_degree` block (line 13342)
- Test: `tests/test_experiment_runner.py` (one new method)

**Interfaces:**
- Consumes: the report writer and the Task 2 dispatch branch.
- Produces: subcommand `code-wreath-orientation-laplacian-gap` with a `--no-registry` flag, plus one clean-registry dispatch test.

- [ ] **Step 1: Add the import**

Find in `qsearch.py`:

```python
from self_dual_wreath_multistar_degree_obstruction import (
    write_multistar_degree_obstruction_report,
)
```

Insert immediately after it:

```python
from self_dual_wreath_orientation_laplacian_gap import (
    write_orientation_laplacian_gap_report,
)
```

- [ ] **Step 2: Add the command function**

Scroll to the end of `def command_code_wreath_multistar_degree(` (it starts at
line 7009 and ends with `return 0`). Insert this function immediately after
that `return 0`, separated by two blank lines:

```python
def command_code_wreath_orientation_laplacian_gap(
    args: argparse.Namespace,
) -> int:
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_laplacian_gap_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation Laplacian floor complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_laplacian_gap.json"
    )
    print(
        "Atom/star controls and failures: "
        f"{metrics['commuting_atom_control_count']}/"
        f"{metrics['star_law_control_count']}/"
        f"{metrics['commuting_atom_failure_count']}/"
        f"{metrics['star_law_failure_count']}"
    )
    print(
        "Screened full graphs / skipped / floor violations: "
        f"{metrics['screened_full_graph_control_count']}/"
        f"{metrics['screened_workload_skipped_control_count']}/"
        f"{metrics['screened_floor_violation_count']}"
    )
    print(
        "Largest-degree distinct correlations / uniform floor / sign-blind floor: "
        f"{metrics['largest_degree_distinct_correlation_count']}/"
        f"{metrics['largest_degree_uniform_transport_floor']:.6g}/"
        f"{metrics['largest_degree_sign_blind_floor']:.6g}"
    )
    print(
        "Vertex trivialization proved: "
        f"{payload['claim_gate']['vertex_trivialization_proved']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0
```

- [ ] **Step 3: Add the subparser block**

Find this block (line 13342):

```python
    code_wreath_multistar_degree = subparsers.add_parser(
        "code-wreath-multistar-degree",
```

Scroll to the end of that block — the line
`        func=command_code_wreath_multistar_degree` followed by `    )`.
Insert immediately after that closing `    )`:

```python

    code_wreath_orientation_laplacian_gap = subparsers.add_parser(
        "code-wreath-orientation-laplacian-gap",
        help=(
            "Compute the width-independent floor of the projector-weighted "
            "orientation Laplacian and measure residual-transport uniformity."
        ),
    )
    code_wreath_orientation_laplacian_gap.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_laplacian_gap.set_defaults(
        func=command_code_wreath_orientation_laplacian_gap
    )
```

- [ ] **Step 4: Verify the subcommand is registered and runs**

```bash
python qsearch.py --help | grep code-wreath-orientation-laplacian-gap
```

Expected: the name appears.

```bash
python qsearch.py code-wreath-orientation-laplacian-gap
```

Expected, in this order: the completion line, the artifact path,
`Atom/star controls and failures: 2/2/0/0`,
`Screened full graphs / skipped / floor violations: 270/0/0`,
`Largest-degree distinct correlations / uniform floor / sign-blind floor: 1/1.81818/-4.88064e+07`,
`Vertex trivialization proved: False`, `Speedup claim allowed: False`,
`Registry valid: True`. Exit code 0. Runtime about 50 seconds.

If it prints `Registry valid: False`, stop and report the printed issues. Do
not edit the registry by hand to make validation pass.

- [ ] **Step 5: Run the dispatch path**

```bash
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP
```

Expected: exit 0 and a result row written.

- [ ] **Step 6: Add the clean-registry dispatch test**

In `tests/test_experiment_runner.py`, find
`def test_multistar_degree_obstruction_dispatches_from_clean_registry(self):`
and insert this method immediately after that method's final
`self.assertTrue(validation["valid"], validation["issues"])` line, keeping the
same four-space class indentation:

```python
    def test_orientation_laplacian_gap_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_laplacian_gap",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])
```

- [ ] **Step 7: Run the new dispatch test**

```bash
python -m pytest tests/test_experiment_runner.py -q -k "orientation_laplacian_gap_dispatches"
```

Expected: `1 passed`, in about a minute.

---

### Task 4: Correct the README paragraph the new result supersedes

**Files:**
- Modify: `README.md`

The pass-1 README block for `code-wreath-multistar-degree` currently ends by
saying the surviving object is the orientation Laplacian and that no gap is
proved for it. That sentence is now out of date in one direction: a
width-independent floor is proved under an explicit hypothesis. Fix that
sentence and add the new block.

- [ ] **Step 1: Correct the closing sentence of the multistar block**

Find this sentence in `README.md`:

```
The surviving object is the
projector-weighted orientation Laplacian `Delta = D - A`, whose positive
spectrum equals that of the relation Gram; no gap is proved for it.
```

Replace it with:

```
The surviving object is the
projector-weighted orientation Laplacian `Delta = D - A`, whose positive
spectrum equals that of the relation Gram. The next section shows that a
vacuous absolute-weight certificate does not imply bad conditioning.
```

- [ ] **Step 2: Add the new block immediately after that paragraph**

````markdown
Compute the width-independent metric floor:

```bash
python qsearch.py code-wreath-orientation-laplacian-gap
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP
```

The relation Gram is the Gram of a signed subspace incidence map, so
`<x, Delta x> = sum_e ||P_(K_e)(x_a - x_b)||^2`. When the live pair-core
projectors commute, the complex splits into scalar graph Laplacians over
Boolean atoms, and the affine-support theorem makes every atom support a
complete graph, so the smallest positive eigenvalue is at least two no matter
how many cores meet one orientation. For a `p`-star with residual correlation
`gamma` the spectrum is exactly `2-gamma` with multiplicity `p-1` together
with `2+(p-1)gamma`, so the smallest eigenvalue does not move as `p` grows;
this reproduces the S6 noncommuting counterexample (`17/9`, `20/9` at
`gamma=1/9`) to `2.7e-15`. If the residual overlaps factor through vertex
isometries with one common `gamma`, then `lambda_min(M) >= 2-2gamma`,
independent of merge width and at least `2-2/(n-1)`. At `n=12` that floor is
`1.8182` where the sign-blind estimate for the same merge was `-4.88e7`. No
full live graph among 270 controls violates the floor, and the number of
distinct residual correlations per sampled star collapses to one at `n=12`.

The vertex trivialization is a hypothesis, not a theorem. Only its
single-correlation half is measured, the graded defect is unbounded, and no
circuit follows. Two traps are worth recording: the floor is a statement about
the full live graph, since a star subgraph deletes edges and drops the minimum
to one; and vertex-disjoint pair cores overlap geometrically but contribute no
off-diagonal block to the relation Gram at all.
````

---

### Task 5: Refresh downstream artifacts

- [ ] **Step 1: Run the standard downstream workflows**

Run these one at a time, in this order, and check each exits 0:

```bash
python qsearch.py dequantize
```

```bash
python qsearch.py proofs
```

```bash
python qsearch.py query-models
```

```bash
python qsearch.py frontiers
```

```bash
python qsearch.py conjectures
```

```bash
python qsearch.py mutate
```

```bash
python qsearch.py validate
```

Expected: every command exits 0 and `validate` reports no registry issues. If
`mutate` proposes anything that would enable a speedup claim, or anything that
upgrades the conditional floor into an unconditional conditioning claim, do
not accept it — report it and stop.

- [ ] **Step 2: Confirm no claim gate flipped**

```bash
python -c "
import glob, json
bad = []
for path in glob.glob('research/**/*.json', recursive=True):
    try:
        data = json.load(open(path))
    except Exception:
        continue
    gate = data.get('claim_gate') if isinstance(data, dict) else None
    if isinstance(gate, dict) and gate.get('speedup_claim_allowed'):
        bad.append(path)
print('speedup gates open:', bad)
"
```

Expected: `speedup gates open: []`.

- [ ] **Step 3: Confirm the new gate stayed conditional**

```bash
python -c "
import json
d = json.load(open('research/representation/self_dual_wreath_orientation_laplacian_gap.json'))
g = d['claim_gate']
assert g['vertex_trivialization_proved'] is False
assert g['all_depth_conditioning_proved'] is False
assert g['grading_defect_bounded'] is False
assert g['speedup_claim_allowed'] is False
print('gates correct')
"
```

Expected: `gates correct`.

---

### Task 6: Final verification and one commit

- [ ] **Step 1: Run the focused test set**

```bash
python -m pytest tests/test_self_dual_wreath_orientation_laplacian_gap.py tests/test_self_dual_wreath_multistar_degree_obstruction.py tests/test_self_dual_wreath_pair_core_carrier_factorization.py tests/test_self_dual_wreath_common_core_atomization.py tests/test_self_dual_wreath_pair_core_recoupling_boundary.py tests/test_experiment_runner.py -q
```

Expected: all pass. Do not run the full suite.

- [ ] **Step 2: Run the standard static checks**

```bash
python -m compileall -q . && node --check site/progress.js && git diff --check && echo "checks ok"
```

Expected: `checks ok`.

- [ ] **Step 3: Confirm the working tree contains only intended changes**

Run: `git status --short`

Expected: modifications to `README.md`, `qsearch.py`, `experiment_runner.py`,
`research_registry.py`, `tests/test_experiment_runner.py`, and refreshed
`research/**` artifacts, plus the new module, artifact, and test file if they
are still untracked. No change under `ag-remote/` beyond the pre-existing
deletions.

- [ ] **Step 4: Commit once**

```bash
git add -A -- . ':!ag-remote'
git commit -m "Wire the orientation Laplacian floor module

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Do not push. Do not create a pull request.

---

### Task 7: Build the real wiring-backlog inventory

Pass 1's plan named six backlog modules, taken from a hand-written list in the
handoff. Those six are now wired. A direct scan of the repository shows the
actual backlog is **57 modules**, of which the Laplacian gap module handled in
Tasks 1 through 6 is one. Do not work from a hand-written list again; generate
the inventory and work from it.

**Files:**
- Create: `research/wiring_backlog.json`

- [ ] **Step 1: Generate the inventory**

```bash
python - <<'PY'
import json, re, pathlib
root = pathlib.Path(".")
registry = pathlib.Path("research_registry.py").read_text()
runner = pathlib.Path("experiment_runner.py").read_text()
tests = {p.name for p in pathlib.Path("tests").glob("*.py")}
artifacts = {p.name for p in root.glob("research/**/*.json")}
rows = []
for path in sorted(root.glob("*.py")):
    text = path.read_text()
    match = re.search(r'DEFAULT_EXPERIMENT_ID\s*=\s*\(?\s*"([A-Z0-9-]+)"', text)
    if not match:
        continue
    experiment_id = match.group(1)
    if registry.count(experiment_id) or runner.count(experiment_id):
        continue
    writers = re.findall(r'^def (write_\w+)\(', text, re.M)
    rows.append({
        "module": path.stem,
        "experiment_id": experiment_id,
        "report_writer": writers[0] if writers else None,
        "has_registry_kwargs": "write_registry" in text,
        "has_test": f"test_{path.stem}.py" in tests,
        "has_artifact": f"{path.stem}.json" in artifacts,
    })
pathlib.Path("research/wiring_backlog.json").write_text(
    json.dumps({"unwired_module_count": len(rows), "modules": rows}, indent=2, sort_keys=True)
)
ready = [r for r in rows if r["report_writer"] and r["has_test"] and r["has_artifact"]]
print("unwired:", len(rows), "ready to wire:", len(ready),
      "already have kwargs:", sum(r["has_registry_kwargs"] for r in ready))
print("not ready:", [r["module"] for r in rows if r not in ready])
PY
```

Expected, as of this plan: `unwired: 57 ready to wire: 56 already have kwargs: 15`,
and `not ready: ['self_dual_wreath_global_collision_free_mass']`.

If your numbers differ, that is fine — the generated file is authoritative,
not this paragraph. Use it. Report the difference in your summary.

- [ ] **Step 2: Record the one incomplete module**

`self_dual_wreath_global_collision_free_mass.py` has a
`write_global_collision_free_mass_report` function but **no artifact and no
test**. Do not wire it and do not write a test for it: deciding what that
module should assert is mathematical judgment. Note it in your summary as
needing a high-reasoning pass, and skip it everywhere below.

---

### Task 8: Retrofit registry keyword arguments where they are missing

41 of the 56 ready modules have a `write_*` report function with **no**
registry parameters. Wiring needs them. This is a pure copy edit with no
mathematical content.

**Files:**
- Modify: each module listed by Task 7 with `"has_registry_kwargs": false`

**Interfaces:**
- Produces, for every such module: `write_<name>(path=REPORT_PATH, write_registry=True, registry_experiment_id=DEFAULT_EXPERIMENT_ID, registry_candidate_id=DEFAULT_CANDIDATE_ID, registry_result_id=None, **kwargs) -> dict[str, Any]`, consumed by Tasks 9 and 10.

- [ ] **Step 1: Work one module at a time, in the order the inventory lists**

For module `<name>` with writer `write_<w>` and report function `run_<r>`,
first read its current writer. It will look like this:

```python
def write_<w>(path: Path = REPORT_PATH) -> dict[str, Any]:
    payload = asdict(run_<r>())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
```

- [ ] **Step 2: Add the registry imports if absent**

If the module does not already import them, replace

```python
from research_registry import utc_now
```

with

```python
from research_registry import (
    ExperimentResultRecord,
    upsert_experiment_result,
    utc_now,
)
```

Do **not** add `NegativeResultRecord` or `upsert_negative_result` here.
Authoring a negative-result claim requires deciding what was refuted and why,
which is mathematical judgment. Only the experiment-result upsert is
mechanical.

- [ ] **Step 3: Replace the writer**

```python
def write_<w>(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_<r>(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"<name>": str(path)},
            )
        )
    return payload
```

Replace `<w>`, `<r>`, and `<name>` with the real names. Keep the module's
existing `if __name__ == "__main__":` block exactly as it is.

If `run_<r>()` takes no arguments, `**kwargs` is still correct and harmless.
If the module's `DEFAULT_CANDIDATE_ID` does not exist, add
`DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"` beside `DEFAULT_EXPERIMENT_ID`.

- [ ] **Step 4: Verify the module still imports and its test passes**

```bash
python -c "import <name>; print('ok')" && python -m pytest tests/test_<name>.py -q
```

Expected: `ok`, then all tests in that file pass. If the module has no
`falsifiers_triggered` or `headline_metrics` key in its payload, the upsert
will raise a `KeyError` at run time — do **not** invent those fields. Record
the module as blocked and move on.

- [ ] **Step 5: Commit after every ten modules**

```bash
git add -A -- . ':!ag-remote'
git commit -m "Add registry keyword arguments to wreath report writers

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 9: Wire the backlog in batches of ten

**Files:**
- Modify: `research_registry.py`, `experiment_runner.py`, `qsearch.py`, `tests/test_experiment_runner.py`

Apply Tasks 1 through 3 as the recipe, ten modules per batch.

- [ ] **Step 1: For each module, read its own words first**

Open the module docstring and its artifact's `theorem_contract`,
`claim_gate`, `adversarial_audit`, and `falsifiers_triggered`. Every field you
write into the `ExperimentRecord` must be a phrase taken from one of those.
**Do not invent a hypothesis, a positive signal, or a falsifier.** If the
artifact has no `theorem_contract`, use the module docstring's first paragraph
for `hypothesis` and its last paragraph for `positive_signal`, and take
`falsifiers` verbatim from `falsifiers_triggered`.

- [ ] **Step 2: Take the metrics list verbatim**

```bash
python -c "
import json
print(json.dumps(sorted(json.load(open('research/representation/<name>.json'))['headline_metrics']), indent=2))
"
```

Paste that list into the record's `metrics=[...]`.

- [ ] **Step 3: Choose the CLI name and priority**

The CLI name is the module stem with `self_dual_wreath_` replaced by
`code-wreath-` and underscores replaced by hyphens, truncated to something
already used in the handoff if one is listed there. Check it is free:

```bash
python qsearch.py --help | grep -c "<cli-name>"
```

Expected: `0`. For the priority integer, use the next unused value:

```bash
python -c "
import re
src = open('experiment_runner.py').read()
values = [int(m) for m in re.findall(r'\"EXP-[A-Z0-9-]+\":\s*(\d+),', src)]
print('next free:', max(values) + 1)
"
```

- [ ] **Step 4: Apply Tasks 1, 2, and 3 verbatim for that module**

Same four edit sites, same dispatch-test template. Use the module's own
`write_*` name, artifact path, and metric keys in the `command_*` print block;
print at most four metric lines and always print the `speedup_claim_allowed`
line.

- [ ] **Step 5: After each batch of ten, verify and commit**

```bash
python -m pytest tests/test_experiment_runner.py -q && python -m compileall -q . && python qsearch.py validate
```

Expected: tests pass, compile clean, `validate` reports no registry issues.

```bash
git add -A -- . ':!ag-remote'
git commit -m "Wire wreath theorem modules batch <k>

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Stop and report if `validate` fails, if a module takes longer than five
minutes at default arguments, or if wiring a module would require you to write
a mathematical claim that is not already in its docstring or artifact.

---

### Task 10: Add a repository-wide artifact invariant guard

There is no test that checks the claim gates across all artifacts. Every gate
is currently correct; this task freezes that.

**Files:**
- Create: `tests/test_research_artifact_invariants.py`

- [ ] **Step 1: Write the test**

```python
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _artifacts():
    for path in sorted(ROOT.glob("research/**/*.json")):
        if "registry" in path.parts:
            continue
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not valid JSON")
        if isinstance(payload, dict):
            yield path, payload


def test_every_research_artifact_parses() -> None:
    assert list(_artifacts())


def test_no_artifact_opens_the_speedup_gate() -> None:
    opened = [
        str(path.relative_to(ROOT))
        for path, payload in _artifacts()
        if isinstance(payload.get("claim_gate"), dict)
        and payload["claim_gate"].get("speedup_claim_allowed")
    ]

    assert opened == []


def test_no_artifact_claims_a_new_quantum_algorithm() -> None:
    claimed = [
        str(path.relative_to(ROOT))
        for path, payload in _artifacts()
        if isinstance(payload.get("headline_metrics"), dict)
        and payload["headline_metrics"].get("new_quantum_algorithm_count")
    ]

    assert claimed == []


KNOWN_GATE_WITHOUT_REASON = "research/classical_baselines/character_shift_complexity.json"


def test_every_claim_gate_carries_a_reason() -> None:
    """One legacy artifact predates the reason convention and is exempted.

    Its claim_gate has no `reason` key at all. Writing one means deciding what
    that module concluded, which is a mathematical judgment, so the exemption
    stays until a high-reasoning pass authors it.
    """
    missing = [
        str(path.relative_to(ROOT))
        for path, payload in _artifacts()
        if isinstance(payload.get("claim_gate"), dict)
        and not payload["claim_gate"].get("reason")
    ]

    assert missing == [KNOWN_GATE_WITHOUT_REASON]
```

- [ ] **Step 2: Run it**

```bash
python -m pytest tests/test_research_artifact_invariants.py -q
```

Expected: `4 passed`, over 355 artifacts.

The exemption above is exact as of this plan: `character_shift_complexity.json`
is the **only** artifact whose `claim_gate` lacks a `reason` key. If the test
fails because the list is longer, a new artifact was added without a reason —
report the extra names, add them to the exemption list, and flag them. If it
fails because the list is empty, someone authored the missing reason; delete
the exemption and assert `missing == []`. Either way, do **not** write a
`reason` string yourself.

- [ ] **Step 3: Commit**

```bash
git add tests/test_research_artifact_invariants.py
git commit -m "Guard research artifact claim gates repository wide

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 11: Generate the artifact schema inventory

316 research artifacts exist outside the registry. A scan shows 208 lack
`theorem_contract`, 53 lack `claim_gate`, and 12 lack `falsifiers_triggered`.
**Do not author any of that missing content** — writing a theorem contract or
a claim gate means deciding what a module proved and what it did not, which is
exactly the mathematical judgment this plan is scoped to avoid. Generate the
inventory so a later high-reasoning pass can work from it.

**Files:**
- Create: `research/artifact_schema_inventory.json`

- [ ] **Step 1: Generate**

```bash
python - <<'PY'
import json, pathlib
REQUIRED = [
    "claim_gate", "theorem_contract", "headline_metrics",
    "status", "summary", "falsifiers_triggered",
]
rows = []
for path in sorted(pathlib.Path("research").rglob("*.json")):
    if "registry" in path.parts:
        continue
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError:
        rows.append({"artifact": str(path), "unparseable": True})
        continue
    if not isinstance(payload, dict):
        continue
    if "headline_metrics" not in payload and "claim_gate" not in payload:
        continue
    missing = [key for key in REQUIRED if key not in payload]
    if missing:
        rows.append({"artifact": str(path), "missing_fields": missing})
summary = {}
for row in rows:
    for key in row.get("missing_fields", []):
        summary[key] = summary.get(key, 0) + 1
pathlib.Path("research/artifact_schema_inventory.json").write_text(
    json.dumps(
        {
            "artifacts_with_gaps": len(rows),
            "missing_field_counts": summary,
            "artifacts": rows,
        },
        indent=2,
        sort_keys=True,
    )
)
print("artifacts with gaps:", len(rows), summary)
PY
```

Expected, as of this plan: about 208 missing `theorem_contract`, 53 missing
`claim_gate`, 12 missing `falsifiers_triggered`.

- [ ] **Step 2: Commit the inventory only**

```bash
git add research/artifact_schema_inventory.json
git commit -m "Inventory research artifact schema gaps

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Do not modify any artifact in this task.

---

### Task 12: Record a runtime budget for every wired module

One module in this repository silently took 37 minutes of wall time at 1
percent CPU because it thrashed memory on dense bases. That is why the
Laplacian gap module now has a `workload_cap`. Measure the rest so nobody
stalls on an unknown.

**Files:**
- Create: `research/module_runtime_budget.json`

- [ ] **Step 1: Time each wired module's focused test, not the module**

Running a module directly writes to the registry as a side effect. Time its
test instead.

```bash
python - <<'PY'
import json, pathlib, subprocess, time
rows = []
for path in sorted(pathlib.Path("tests").glob("test_self_dual_wreath_*.py")):
    start = time.time()
    done = subprocess.run(
        ["python", "-m", "pytest", str(path), "-q"],
        capture_output=True, text=True,
    )
    rows.append({
        "test": path.name,
        "seconds": round(time.time() - start, 2),
        "passed": done.returncode == 0,
    })
    print(rows[-1])
slow = [r for r in rows if r["seconds"] > 300]
pathlib.Path("research/module_runtime_budget.json").write_text(
    json.dumps({"slow_threshold_seconds": 300, "slow": slow, "all": rows},
               indent=2, sort_keys=True)
)
print("slow modules:", [r["test"] for r in slow])
print("failing tests:", [r["test"] for r in rows if not r["passed"]])
PY
```

This walks every wreath test file one at a time. Expect it to take a while in
total; that is the point of measuring. Let it finish.

- [ ] **Step 2: Report, do not fix**

If any test fails, record it and report — do **not** change its expected
values. If any exceeds 300 seconds, record it; adding a workload cap to a
module changes what it screens, which is a mathematical decision.

- [ ] **Step 3: Commit**

```bash
git add research/module_runtime_budget.json
git commit -m "Record per-module test runtime budget

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 13: Audit README and CLI coverage

**Run this after Task 9, not before.** As of this plan the scan below reports
`wired wreath experiments: 40  absent from README: 0` — coverage is complete
for what is currently wired. It only becomes real work once Task 9 has wired
the backlog, at which point roughly 56 new ids will appear with no README
block. If you run it early and get zero, that is correct; come back later.

- [ ] **Step 1: Find wired experiments with no README command block**

```bash
python - <<'PY'
import json, pathlib, re
readme = pathlib.Path("README.md").read_text()
runner = pathlib.Path("experiment_runner.py").read_text()
ids = sorted(set(re.findall(r'"(EXP-CODE-SELF-DUAL-WREATH-[A-Z0-9-]+)"', runner)))
missing = [i for i in ids if i not in readme]
print(f"wired wreath experiments: {len(ids)}  absent from README: {len(missing)}")
for i in missing:
    print("  ", i)
PY
```

- [ ] **Step 2: Add one command block per missing id**

Use the same shape as the existing blocks: a one-line lead-in, a fenced `bash`
block with the `qsearch.py <cli-name>` and `qsearch.py run <ID>` lines, then a
short paragraph. **Take every sentence of that paragraph from the module's
artifact `summary` and `theorem_contract`.** Do not write new claims, do not
compare modules, and do not describe anything as an algorithm or a speedup.

- [ ] **Step 3: Verify and commit**

```bash
python -m pytest tests/ -q -k "readme or documentation" && git diff --check && echo ok
```

```bash
git add README.md
git commit -m "Document wired wreath experiments in the README

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 14: Final sweep

- [ ] **Step 1: Re-run the downstream workflows**

Repeat Task 5 in full, then Task 6 Steps 1 through 3.

- [ ] **Step 2: Confirm the backlog shrank**

Re-run Task 7 Step 1. Expected: `unwired` is now `1`
(`self_dual_wreath_global_collision_free_mass`, deliberately skipped).

- [ ] **Step 3: Report**

Write a short summary listing: modules wired, modules blocked and why, tests
that failed, artifacts over the runtime threshold, and every place you
declined to write content because it required mathematical judgment. That last
list is the input to the next high-reasoning pass and is the most valuable
thing you produce.

---

## What you must not do

- Do not change any formula, tolerance, control count, sample count, seed,
  ambient cap, workload cap, or screen limit.
- Do not set `speedup_claim_allowed` to `true` anywhere.
- Do not upgrade `vertex_trivialization_proved`, `all_depth_conditioning_proved`,
  or `grading_defect_bounded` to `true`. The floor is conditional.
- Do not write, in any README or registry text, that the hierarchy is well
  conditioned, that the polar tree is efficient, or that the sign-blind result
  has been reversed into a positive conditioning theorem. What was withdrawn is
  the *inference* from a vacuous certificate to bad conditioning.
- Do not delete or weaken a negative result, proof obligation, adversarial-audit
  entry, or falsifier string. In particular keep
  `NEG-CODE-WREATH-SIGN-BLIND-MULTISTAR-CERTIFICATE`; it is still correct.
- Do not describe a finite screen as an asymptotic theorem.
- Do not attempt any of the twelve items in the "Highest-Value Open Derivation"
  section of `research/AGENT_HANDOFF.md`. Those need mathematical judgment and
  are out of scope for this plan.

---

## 2026-08-13 Binary Hidden-Involution Wiring Delta

Gemini 3.6 Flash through Antigravity should mechanically wire these seventeen
completed theorem modules.  Each has focused tests and a same-stem live JSON
artifact under `research/representation/`:

1. `coset_hidden_involution_source_deflation_no_go.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-SOURCE-DEFLATION-NO-GO`
   - Suggested CLI: `coset-hidden-involution-source-deflation-no-go`
   - Writer: `write_source_deflation_no_go_report`
   - Preserve true gates for weak-source-test and exceptional-source-deflation
     no-gos.  Keep coherent within-block rescaling, fused multiplicity support,
     classical separation, arbitrary-circuit lower bound, and speedup false.
2. `coset_hidden_involution_isotypic_support_no_go.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-ISOTYPIC-SUPPORT-NO-GO`
   - Suggested CLI: `coset-hidden-involution-isotypic-support-no-go`
   - Writer: `write_isotypic_support_no_go_report`
   - This **does** supersede the older registry phrase that scalable proper
     support is unproved: proper nonzero multiplicity support is now proved for
     fixed-point-free `S_n`, every even `n>=6`, at
     `k=ceil(log2(4(n-1)!!))`.  It does not refute commutant-side compilers.
3. `coset_hidden_involution_multiplicity_hard_mass.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-HARD-MASS`
   - Suggested CLI: `coset-hidden-involution-multiplicity-hard-mass`
   - Writer: `write_multiplicity_hard_mass_report`
   - Preserve the all-n `5/18` proper-sector mass and `1/36` simultaneous
   proper/low-spectrum mass as theorem constants.  Do not replace them with
   the stronger finite scaling values or claim a fused-transform lower bound.
4. `coset_hidden_involution_orbit_synthesis_flatness.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-ORBIT-SYNTHESIS-FLATNESS`
   - Suggested CLI: `coset-hidden-involution-orbit-synthesis-flatness`
   - Writer: `write_orbit_synthesis_flatness_report`
   - Preserve the relative, size-biased spectral theorem and its `29/32`
     retained-mass constant at six-copy overhead.  Do not infer standard
     access to unnormalized synthesis or a compiled polar.
5. `coset_hidden_involution_common_outlier_deflation.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-COMMON-OUTLIER-DEFLATION`
   - Suggested CLI: `coset-hidden-involution-common-outlier-deflation`
   - Writer: `write_common_outlier_deflation_report`
   - Record the exact `S_n/A_n` normal-closure split and coherent trivial/sign
     flag.  Keep post-deflation operator norm, pair-intersection control, label
     erasure, global polar, and speedup false.
6. `coset_hidden_involution_pair_polar_phase_compiler.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-PHASE-COMPILER`
   - Suggested CLI: `coset-hidden-involution-pair-polar-phase-compiler`
   - Writer: `write_pair_polar_phase_report`
   - Record the exact dihedral spectrum and logarithmic phase compiler.  Scope
     the generic `Omega(r)` statement to uniform gap-dependent bounded-
     polynomial polar approximation.  Do not claim global consistency.
7. `coset_hidden_involution_pair_polar_holonomy_no_go.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-HOLONOMY-NO-GO`
   - Suggested CLI: `coset-hidden-involution-pair-polar-holonomy-no-go`
   - Writer: `write_pair_polar_holonomy_report`
   - Preserve the exact `{1,-1,-1}` regular-`S_3` loop spectrum, all-even-`n`
     fixed-point-free embedding, and tensor negative multiplicity formula.
     This refutes only path-independent pair alignment; keep holonomy-aware
     global polar, MRS escape, an algorithm, and speedup false.
8. `coset_hidden_involution_s3_chart_gram_compiler.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-S3-CHART-GRAM-COMPILER`
   - Suggested CLI: `coset-hidden-involution-s3-chart-gram-compiler`
   - Writer: `write_s3_chart_gram_report`
   - Preserve the exact defect-weight spectrum, rank
     `3^(k+1)-2(k+1)`, and nonzero Gram interval `[3/4,3]` for `k>=2`.
     This is a polynomial compiler only for the constant three-branch chart.
     Keep matching-scheme transform, global chart gluing, branch erasure,
     full-class polar, hidden-involution algorithm, and speedup false.
9. `coset_hidden_involution_induced_source_bundle_reduction.py`
   - ID: `EXP-COSET-HIDDEN-INVOLUTION-INDUCED-SOURCE-BUNDLE-REDUCTION`
   - Suggested CLI: `coset-hidden-involution-induced-source-bundle-reduction`
   - Writer: `write_induced_source_bundle_report`
   - Preserve the induced-bundle/Frobenius normal form, the distinction between
     pair-polar holonomy and the stabilizer cocycle, and the exact `S_3`
     multiplicity ranks.  Branch-labeled covariance is resolved; physical-
     source lifting, multiplicity support/polar, full synthesis, an algorithm,
     and speedup remain false.
10. `coset_hidden_involution_matrix_hecke_transfer_reduction.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-TRANSFER-REDUCTION`
    - Suggested CLI: `coset-hidden-involution-matrix-hecke-transfer-reduction`
    - Writer: `write_matrix_hecke_transfer_report`
    - Preserve the normalized transfer and exact group-sum Gram formulas, plus
      the `S_3` commutant dimension `(3*9^k+1)/2`.  Keep scalar spherical
      sufficiency, uniform matrix-Hecke basis, structured polar, physical lift,
      an algorithm, and speedup false.  Large dimension is not a lower bound.
11. `coset_hyperoctahedral_cg_kronecker_reduction.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-CG-KRONECKER-REDUCTION`
    - Suggested CLI: `coset-hyperoctahedral-cg-kronecker-reduction`
    - Writer: `write_hyperoctahedral_cg_kronecker_report`
    - Preserve the exact inflation/tensor-product reduction and exponentially
      small regular trivial-color mass.  Keep natural-source hard mass,
      source-specific fusion obstruction, quantum lower bound, algorithm, and
      speedup false.
12. `coset_hyperoctahedral_trivial_color_mass_no_go.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-TRIVIAL-COLOR-MASS-NO-GO`
    - Suggested CLI: `coset-hyperoctahedral-trivial-color-mass-no-go`
    - Writer: `write_trivial_color_mass_report`
    - Preserve the exact Burnside formula, `2^(1-m)` source bound, and the
      Cauchy--Schwarz frame-second-moment transfer to alternative mass.  This
      closes the generic embedded Kronecker sector only; keep colored sectors,
      colored fusion, full polar, algorithm, and speedup false.
13. `coset_hyperoctahedral_color_weight_concentration.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-COLOR-WEIGHT-CONCENTRATION`
    - Suggested CLI: `coset-hyperoctahedral-color-weight-concentration`
    - Writer: `write_color_weight_concentration_report`
    - Preserve the exact Krawtchouk law and the source/alternative balanced-
      color concentration.  Keep residual little-group fusion and polar false.
14. `coset_hyperoctahedral_source_plancherel_typicality.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-SOURCE-PLANCHEREL-TYPICALITY`
    - Suggested CLI: `coset-hyperoctahedral-source-plancherel-typicality`
    - Writer: `write_source_plancherel_report`
    - Preserve the normalized character and wreath-Plancherel TV bound.  QFT
      label access does not compile typical internal multiplicities.
15. `coset_hyperoctahedral_free_orbit_canonicalization_boundary.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-FREE-ORBIT-CANONICALIZATION-BOUNDARY`
    - Suggested CLI: `coset-hyperoctahedral-free-orbit-canonicalization-boundary`
    - Writer: `write_free_orbit_canonicalization_report`
    - Preserve the exact free regular-module decomposition and alternative-
      mass transfer.  This boundary alone does not construct a canonicalizer.
16. `coset_hyperoctahedral_trimmed_orbit_canonicalizer.py`
    - ID: `EXP-COSET-HYPEROCTAHEDRAL-TRIMMED-ORBIT-CANONICALIZER`
    - Suggested CLI: `coset-hyperoctahedral-trimmed-orbit-canonicalizer`
    - Writer: `write_trimmed_canonicalizer_report`
    - Preserve the transitive-seed BFS construction, four seed orientations,
      disjoint-pair failure amplification, and free-set transporter uniqueness.
      A gate-level reversible ledger remains false, as does the transfer polar.
17. `coset_hidden_involution_regular_orbit_row_reduction.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-REGULAR-ORBIT-ROW-REDUCTION`
    - Suggested CLI: `coset-hidden-involution-regular-orbit-row-reduction`
    - Writer: `write_regular_orbit_row_report`
    - Preserve `Ind_K^G C[K]=C[G]`, matrix group convolution, and the removal
      of generic wreath CG from trimmed mass.  Keep orbit-row polar, label
      erasure, full synthesis, algorithm, and speedup false.
18. `coset_hidden_involution_incidence_walk_boundary.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-INCIDENCE-WALK-BOUNDARY`
    - Writer: `write_incidence_walk_report`
    - Preserve the exact biregular incidence identities and generic
      `Omega(sqrt(M))` interval-QSVT obstruction. Structured Fourier/row access
      is not ruled out.
19. `coset_hidden_involution_common_factor_trim.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-COMMON-FACTOR-TRIM`
    - Writer: `write_common_factor_trim_report`
    - Preserve exact integer overlap numerator/denominator fields. Do not
      replace the strict rational `<1/2` gate with rounded float comparison.
20. `coset_hidden_involution_subgroup_outlier_hierarchy.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-SUBGROUP-OUTLIER-HIERARCHY`
    - Writer: `write_subgroup_outlier_report`
    - Preserve the exact hyperoctahedral incident count and superpolynomial
      post-trim frame-norm lower bound. It refutes global interval conditioning,
      not structured blockwise inversion.
21. `coset_hidden_involution_spherical_outlier_deflation.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-SPHERICAL-OUTLIER-DEFLATION`
    - Writer: `write_spherical_outlier_report`
    - Preserve the Thrall even-row conjugate-span identity and vanishing
      all-register mass bound. Other subgroup strata remain open.
22. `coset_hidden_involution_subgroup_support_dichotomy.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-SUBGROUP-SUPPORT-DICHOTOMY`
    - Writer: `write_subgroup_support_dichotomy_report`
    - Preserve `[G:N_G(L)]` as the conjugacy-orbit count and `[G:L]` as the
      induced dimension; never conflate them. Efficient support membership is
      not proved for arbitrary subgroups.
23. `coset_hidden_involution_imprimitive_plethysm_boundary.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-IMPRIMITIVE-PLETHYSM-BOUNDARY`
    - Writer: `write_imprimitive_plethysm_report`
    - Preserve the exact wreath incidence and two-row subset-orbit formulas.
      Odd two-row survivors are negligible; higher-row plethysm remains open.
24. `coset_hidden_involution_foulkes_support_mass_probe.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-MASS-PROBE`
    - Writer: `write_foulkes_support_mass_report`
    - The default live run includes expensive `h_10[h_3]`. Do not put it in a
      repeated broad dispatch loop. Preserve `k(1-w)` as an unresolved
      asymptotic criterion and all coherent-projector gates as false.
25. `coset_hidden_involution_foulkes_support_projector_no_go.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-PROJECTOR-NO-GO`
    - Writer: `write_foulkes_support_projector_report`
    - Preserve the exponential generic conjugate-twirl threshold no-go and the
      direct-label/structured-transform escape. This is not a circuit lower
      bound for every Foulkes support projector.
26. `coset_hidden_involution_bulk_conditioning_normalization_no_go.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-BULK-CONDITIONING-NORMALIZATION-NO-GO`
    - Writer: `write_bulk_conditioning_normalization_report`
    - Preserve the exact size-biased bulk bound, constant unnormalized
      condition number, and inherited `Omega(sqrt(M))` QSVT normalization
    obstruction. This report explicitly deprioritizes support-only screens;
    do not rewrite it as a residual frame-norm theorem or arbitrary-circuit
    lower bound.
27. `coset_hidden_involution_branch_erasure_normalization_no_go.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-BRANCH-ERASURE-NORMALIZATION-NO-GO`
    - Writer: `write_branch_erasure_normalization_report`
    - Preserve the exact labelled Stinespring isometry, coefficient-row
      `alpha>=sqrt(M)` theorem, and `Theta(1/M)` success on the conditioned
      bulk.  The scope is one clean branch-only success row.  Joint
      candidate/physical multiplicity transforms, multi-round relocation,
      large retained Fourier sectors, direct row polars, and arbitrary
      natural-input circuits remain open.
28. `coset_hidden_involution_fourier_coefficient_normalization_no_go.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-FOURIER-COEFFICIENT-NORMALIZATION-NO-GO`
    - Writer: `write_fourier_coefficient_normalization_report`
    - Preserve the exact regular Fourier identity
      `W_nu=sqrt(|G|/d_nu) I tensor A_nu` and the universal
      `Omega(|G|^(1/4))` generic-QSVT bound for normalization-one raw
      coefficient access.  Do not turn it into a lower bound for direct
      sector-normalized block encodings, structured fast-forwarding,
      recoupling networks, or arbitrary circuits.
    - Preserve
      `research/representation/coset_hidden_involution_foulkes_support_mass_h12_diagnostic.json`
      as an expensive standalone diagnostic.  Do not add `h_12[h_3]` to a
      repeated default workflow.
29. `coset_hidden_involution_binary_identification_self_reduction.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-BINARY-IDENTIFICATION-SELF-REDUCTION`
    - Writer: `write_binary_identification_self_reduction_report`
    - Preserve the exact left-coset dephasing lemma, matching-edge membership
      reduction, simultaneous `C_2^t` character filter with total success
      `1/2`, and `m^2-1` edge-test count.  Cite Fenner--Zhang
      `arXiv:cs/0610086`; the general permutation-group decision/search
      equivalence is prior art.  Keep efficient detector, GI reduction,
      classical separation, algorithm, and speedup false.
30. `coset_hidden_involution_rigid_gi_bridge.py`
    - ID: `EXP-COSET-HIDDEN-INVOLUTION-RIGID-GI-BRIDGE`
    - Writer: `write_rigid_gi_hidden_involution_bridge_report`
    - Preserve the rigid-graph promise, structured `S_n wr C_2` involution
      class, exact wreath-to-`S_(2n)` maximally mixed transversal lift, and
      random full-conjugation symmetrization.  The construction and sampling
    equivalence are prior art from `arXiv:quant-ph/0501056`, not a new
    reduction.  Keep nonrigid/general GI, detector, algorithm, classical
    separation, and speedup false.
31. `self_dual_wreath_disjoint_grid_recoupling_falsifier.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-DISJOINT-GRID-RECOUPLING-FALSIFIER`
    - Writer: `write_disjoint_grid_recoupling_falsifier_report`
    - Preserve the explicit finite `S_6` counterexample: nine occupied
      multiplicity-free grid cells, core ranks `1` and `81`, best waist bound
      `1/5`, observed norm reconstructed as `1/15`, and squared norm `1/225`.
      This falsifies exact one-waist saturation and carrier-dimension-only
      formulas. It does not prove an all-`n` 9j formula, a uniform residual
      gap, a coherent recoupling compiler, an algorithm, or a speedup. Keep
      those gates false and retain `1/15` as a finite rational reconstruction,
      not a symbolic theorem.
32. `self_dual_wreath_grid_quantum_marginal_boundary.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-GRID-QUANTUM-MARGINAL-BOUNDARY`
    - Writer: `write_grid_quantum_marginal_boundary_report`
    - Preserve the exact basis/projector norm identity identifying disjoint
      pair-core overlap as a generalized symmetric-group recoupling block.
      Preserve the Christandl--Sahinoglu--Walter and Keyl--Werner literature
      links. The published asymptotic theorem is fixed-row only: keep
      `published_fixed_row_proof_covers_plancherel_regime`, the
      dimension-uniform bound, natural-source marginal classification,
      coherent compiler, uniform gap, algorithm, and speedup false. The Weyl
      prefactor calculation is a scope audit, not a lower bound on the true
      recoupling coefficient.
33. `self_dual_wreath_recoupling_dimension_certificate.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-DIMENSION-CERTIFICATE`
    - Writer: `write_recoupling_dimension_certificate_report`
    - Preserve the exact rank-aware tetrahedral bound, all 51 complete `S_6`
      controls, zero violations, 24 nontrivial certificates, and the selected
      exact squared bound `25/81` versus actual norm `1/3`. This theorem is
      dimension-uniform for one 6j block. Keep natural Plancherel rank pressure,
      generalized 3nj contraction, coherent compilation, uniform gap,
      algorithm, and speedup false.
34. `self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-RANK-PRESSURE-NO-GO`
    - Writer: `write_plancherel_recoupling_rank_pressure_no_go_report`
    - Preserve the independent six-label theorem, failure bound
      `6/n+16V_n`, and raw squared-bound lower margin
      `n!/(4 n^(7/2) p(n)^(7/2))`. Keep the physical path, true norm,
      coherent 3nj, algorithm, and speedup gates false; module 35 resolves
      only the physical rank-certificate question, not the true norm.
35. `self_dual_wreath_physical_recoupling_rank_pressure_no_go.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-RECOUPLING-RANK-PRESSURE-NO-GO`
    - Writer: `write_physical_recoupling_rank_pressure_no_go_report`
    - Preserve the exact trace-mass six-label law, exact Plancherel edge
      marginals, local density `1+X`, physical failure bound `6/n+8V_n`, and
      vanishing mass of blocks where the rank certificate is nontrivial. This
      is not a lower bound on the true norm and does not control coherent 3nj
      interference.
36. `self_dual_wreath_plancherel_marginal_compatibility_no_go.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-MARGINAL-COMPATIBILITY-NO-GO`
    - Writer: `write_plancherel_marginal_compatibility_no_go_report`
    - Preserve the normalized Young-diagram symmetric-difference identity,
      VKLS external input, diagonal tripartite compatibility witness, and
      conclusion `D_n=o_p(1)`. Do not claim a rate, a growing-row compatible
      lower bound, a true norm bound, or that shrinking-gap suppression is
      impossible.
37. `self_dual_wreath_recoupling_channel_flatness_boundary.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-CHANNEL-FLATNESS-BOUNDARY`
    - Writer: `write_recoupling_channel_flatness_boundary_report`
    - Preserve the physical/product channel laws, likelihood ratio,
      mutual-information and chi-square identities, plus the complete `S_6`
      finite values. Exact flatness is falsified only at finite size. Keep both
      asymptotic alternatives, coherent-phase leverage, classical separation,
      algorithm, and speedup unresolved.
38. `self_dual_wreath_recoupling_haar_gap_reduction.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-HAAR-GAP-REDUCTION`
    - Writer: `write_recoupling_haar_gap_reduction_report`
    - Preserve the exact orthogonal-Haar channel chi-square, physical
      four-label density and `V4_n` identity, multiplicity lower bound, and
      factorial Haar-gap reduction. Keep natural Racah universality,
      enhancement control, measured-channel independence, algorithm, and
      speedup false. The theorem says factorial enhancement is necessary for
      a nonvanishing signal, not that such enhancement is absent.
39. `self_dual_wreath_physical_recoupling_tetrahedral_synergy.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-RECOUPLING-TETRAHEDRAL-SYNERGY`
    - Writer: `write_physical_recoupling_tetrahedral_synergy_report`
    - Preserve exact independence of all 15 edge-label pairs and the four
      fusion-face chi-square identities `V_n`. Keep the full six-label product
      law, source/final-conditioned channel information, coherent-phase no-go,
      algorithm, and speedup false. Vanishing local face dependence does not
      exclude parity-like tetrahedral synergy.
40. `self_dual_wreath_source_conditioned_channel_decoupling.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-SOURCE-CONDITIONED-CHANNEL-DECOUPLING`
    - Writer: `write_source_conditioned_channel_decoupling_report`
    - Preserve the exact five-character conditional law, annealed chi-square
      `2V_n+E_Pl[T_lambda^2]`, class-convolution identity, Young contraction,
      and moved-support proof that the half-reciprocal class sum vanishes.
      This proves five-label product convergence only after summing the final
      label. Keep final-label-conditioned information, six-label product,
      coherent multiplicity phase, algorithm, and speedup false. Do not infer
      that the finite `S_6` conditioned correlations disappear.
41. `self_dual_wreath_tetrahedral_chi_square_tail_no_go.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-CHI-SQUARE-TAIL-NO-GO`
    - Writer: `write_tetrahedral_chi_square_tail_no_go_report`
    - Preserve class-signature duality, the exact 15-mask decomposition, and
      the trivial/sign parity contribution
      `8-16/(n!)^3+64/(n!)^6`. Preserve its physical mass `8/(n!)^3` and the
      `12/n!` one-dimensional union bound. Keep positive-mass TV/KL,
      final-conditioned information, coherent phase, algorithm, and speedup
      false. This rejects raw chi-square as a metric; it does not certify a
      useful parity signal.
42. `self_dual_wreath_tetrahedral_dimension_trim.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-DIMENSION-TRIM`
    - Writer: `write_tetrahedral_dimension_trim_report`
    - Preserve `D_n=floor(sqrt(n!)/(p(n)log2(n!)))`, removed mass/TV bound
      `6/[p(n)log2(n!)^2]`, and removed positive-KL bound
      `36/[p(n)log2(n!)]`. Keep retained-bulk decay/survival, coherent trim,
      algorithm, and speedup false. This is an information-theoretic trim,
      not a compiled projector.
43. `self_dual_wreath_projected_tetrahedral_word_map.py`
    - ID: `EXP-CODE-SELF-DUAL-WREATH-PROJECTED-TETRAHEDRAL-WORD-MAP`
    - Writer: `write_projected_tetrahedral_word_map_report`
    - Preserve the exact `m_R,K_R,q_R` projected-kernel identity and retained
      TV upper bound. Preserve the finite S5 post-one-dimensional-trim values
      as controls only. Keep canonical projected-norm decay and survival,
      retained positive KL, classical separation, coherent compiler,
      algorithm, and speedup false. Add the four literature records/links only
      with the scope boundaries stated in the report; fixed-cycle/stable-
      character theorems do not solve the high-level projection.

Mechanical actions:

- Add `ExperimentRecord` entries using only each module's theorem contract,
  summary, proof obligations, falsifiers, and claim gates.
- Add imports, supported-ID entries, priority values, dispatch branches, CLI
  parsers/handlers, clean-registry dispatch tests, and concise README command
  blocks by copying the existing hidden-involution theorem pattern.
- Refresh `dequantize`, `proofs`, `query-models`, `frontiers`, `conjectures`,
  `mutate`, the progress snapshot, and `validate` after wiring all forty-three as one
  batch.
- Repair the pre-existing clean-registry defect in
  `write_complete_racah_control_report`: it currently accepts
  `write_registry`/result IDs but never calls the registry upsert helpers, so
  `tests/test_coset_complete_racah_control.py::CompleteRacahControlTests::test_writer_runner_and_ledgers_record_finite_uniform_boundary`
  fails when `experiment_runner` appends the missing result. Copy a neighboring
  report writer's result/negative upsert pattern without changing Racah claims.
- Run the forty-three focused test files first, then adjacent hidden-involution
  tests, `python -m compileall -q .`, `node --check site/progress.js`,
  `git diff --check`, and `python qsearch.py validate`.
- Make no separate commit per theorem.  Include these in the next rare coherent
  checkpoint only after the batch is fully validated.

Do not ask Gemini to derive the Foulkes support deficit, higher-row support
predicate, subgroup-incidence classification, relative block spectrum, global
connection quotient, holonomy resolver, or fused polar compiler. Those are
high-judgment tasks in
`research/AGENT_HANDOFF.md`.
