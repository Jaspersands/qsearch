# Mechanical Follow-Up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the two new theorem modules
(`self_dual_wreath_pair_core_carrier_factorization.py` and
`self_dual_wreath_multistar_degree_obstruction.py`) into the seed registry,
the `qsearch.py` CLI, the `experiment_runner.py` dispatcher, the literature
index, and the README, then refresh downstream artifacts — without changing
any mathematics.

**Architecture:** Every theorem module in this repository is reachable four
ways: as a script, as a `qsearch.py` subcommand, as a
`python qsearch.py run <EXPERIMENT-ID>` dispatch, and as a seeded
`ExperimentRecord` in `research_registry.py`. This plan adds those four
hookups for two modules by copying the
`EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT` pattern verbatim, then
runs the standard downstream refresh.

**Tech Stack:** Python 3.13, `numpy`, `pytest`, stdlib `argparse`/`json`.
No new dependencies. Node is used only for `node --check site/progress.js`.

## Global Constraints

- Work from the repository root: `/Users/jaspersands/Desktop/quantum algorithm search`.
- Branch is `main`. There is a large uncommitted research pass in the
  worktree. **Do not** run `git reset`, `git checkout -- .`, `git stash`, or
  `git clean`. Do not discard or revert anything you did not write.
- **Do not touch anything under `ag-remote/`.** Those deletions are
  user-owned.
- **Do not change any mathematics.** Do not edit formulas, thresholds,
  tolerances, control lists, sample counts, screen caps, theorem contracts,
  proof obligations, adversarial audits, falsifier strings, or the wording of
  any `reason` field. If a test fails because a number changed, you have
  broken something — revert your edit, do not adjust the expected value.
- **Never set `speedup_claim_allowed` to `true`.** It stays `false` in every
  artifact, every registry record, and every README sentence.
- **Never promote an artifact because tests pass.** Passing tests are a
  precondition for wiring, not evidence for a claim.
- Preserve every existing negative result. Do not delete registry rows.
- Do not run the full repository suite (about 1,494 tests, multi-hour). Run
  only the focused tests named in each task.
- Do not commit after every task. Make exactly one commit, in Task 8.
- Python invocation is plain `python` from the repository root.

### The two modules being wired

| | Module A | Module B |
| --- | --- | --- |
| file | `self_dual_wreath_pair_core_carrier_factorization.py` | `self_dual_wreath_multistar_degree_obstruction.py` |
| experiment id | `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION` | `EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION` |
| CLI name | `code-wreath-pair-core-carrier-factorization` | `code-wreath-multistar-degree` |
| artifact | `research/representation/self_dual_wreath_pair_core_carrier_factorization.json` | `research/representation/self_dual_wreath_multistar_degree_obstruction.json` |
| report writer | `write_pair_core_carrier_factorization_report` | `write_multistar_degree_obstruction_report` |
| test file | `tests/test_self_dual_wreath_pair_core_carrier_factorization.py` | `tests/test_self_dual_wreath_multistar_degree_obstruction.py` |
| candidate id | `CODE-COSET-COLLECTIVE` | `CODE-COSET-COLLECTIVE` |

---

## File Structure

- `self_dual_wreath_pair_core_carrier_factorization.py` — Module A. Task 1
  adds registry-writing parameters to its `write_*_report` function only.
- `self_dual_wreath_multistar_degree_obstruction.py` — Module B. Same, Task 2.
- `research_registry.py` — holds every seeded `ExperimentRecord`. Task 3 adds
  two records next to the fusion-moment record near line 7534.
- `experiment_runner.py` — holds the `COSET_EXPERIMENTS` id set (line ~820),
  the `priority` dict inside `select_next_experiment()` (line 1853), and the
  `run` dispatch chain (line ~3894). Task 4 edits all three.
- `qsearch.py` — holds module imports (line ~530), `command_*` functions
  (line ~6892), and `subparsers.add_parser` blocks (line ~13014). Task 5
  edits all three.
- `research/literature_index.json`, `research/literature_records.json` —
  Task 6 adds the Sellke record.
- `README.md` — Task 7 adds one command block per module.

---

### Task 1: Give Module A a registry-writing report function

**Files:**
- Modify: `self_dual_wreath_pair_core_carrier_factorization.py` (imports block near line 84; `write_pair_core_carrier_factorization_report` at the end of the file)
- Test: `tests/test_self_dual_wreath_pair_core_carrier_factorization.py`

**Interfaces:**
- Consumes: `run_pair_core_carrier_factorization(*, s5_control_cap=40, s6_control_cap=120, repeated_control_cap=40, disjoint_control_cap=40)` — already exists, do not change it.
- Produces: `write_pair_core_carrier_factorization_report(path=REPORT_PATH, write_registry=True, registry_experiment_id=DEFAULT_EXPERIMENT_ID, registry_candidate_id=DEFAULT_CANDIDATE_ID, registry_result_id=None, **kwargs) -> dict[str, Any]`. Tasks 4 and 5 call it with all four registry keyword arguments.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_self_dual_wreath_pair_core_carrier_factorization.py`:

```python
def test_report_writer_can_skip_the_registry(tmp_path) -> None:
    from self_dual_wreath_pair_core_carrier_factorization import (
        write_pair_core_carrier_factorization_report,
    )

    path = tmp_path / "carrier.json"
    payload = write_pair_core_carrier_factorization_report(
        path=path,
        write_registry=False,
        s5_control_cap=4,
        s6_control_cap=4,
        repeated_control_cap=4,
        disjoint_control_cap=4,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"]["screened_star_failure_count"] == 0
```

- [ ] **Step 2: Run the test and confirm it fails**

Run: `python -m pytest tests/test_self_dual_wreath_pair_core_carrier_factorization.py::test_report_writer_can_skip_the_registry -v`

Expected: FAIL with `TypeError: write_pair_core_carrier_factorization_report() got an unexpected keyword argument 'write_registry'`.

- [ ] **Step 3: Add the registry imports**

In `self_dual_wreath_pair_core_carrier_factorization.py`, find this line:

```python
from research_registry import utc_now
```

Replace it with:

```python
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
```

- [ ] **Step 4: Replace the report writer**

In the same file, find this function:

```python
def write_pair_core_carrier_factorization_report(
    path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_pair_core_carrier_factorization(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
```

Replace it with exactly:

```python
def write_pair_core_carrier_factorization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_pair_core_carrier_factorization(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-SINGLE-RECIPROCAL-PAIR-CORE-LAW",
                source=str(path),
                claim=(
                    "Every off-common pair-core overlap is a single "
                    "reciprocal irrep dimension 1/d_alpha."
                ),
                reason_invalid=(
                    "The exact shared-vertex overlap is a two-carrier "
                    "product 1/(d_beta d_p). Finite screens saw single "
                    "reciprocals only because their membership blocks were "
                    "singletons, which forces the second carrier to be one "
                    "dimensional."
                ),
                lesson=(
                    "Use the closed-form carrier factorization rather than "
                    "measured reciprocal spectra, and do not treat a small "
                    "per-block correlation as evidence of conditioning "
                    "without counting adjacency."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
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
                artifacts={
                    "self_dual_wreath_pair_core_carrier_factorization": str(
                        path
                    )
                },
            )
        )
    return payload
```

- [ ] **Step 5: Run the focused tests and confirm they pass**

Run: `python -m pytest tests/test_self_dual_wreath_pair_core_carrier_factorization.py -q`

Expected: `11 passed`. If any of the original 10 tests now fails, you changed
mathematics — undo and redo Steps 3 and 4 exactly as written.

---

### Task 2: Give Module B a registry-writing report function

**Files:**
- Modify: `self_dual_wreath_multistar_degree_obstruction.py` (imports block near line 72; `write_multistar_degree_obstruction_report` at the end of the file)
- Test: `tests/test_self_dual_wreath_multistar_degree_obstruction.py`

**Interfaces:**
- Consumes: `run_multistar_degree_obstruction(*, sampled_degrees=(7, 8, 9, 10, 11, 12), sample_count=40)` — already exists, do not change it.
- Produces: `write_multistar_degree_obstruction_report(path=REPORT_PATH, write_registry=True, registry_experiment_id=DEFAULT_EXPERIMENT_ID, registry_candidate_id=DEFAULT_CANDIDATE_ID, registry_result_id=None, **kwargs) -> dict[str, Any]`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_self_dual_wreath_multistar_degree_obstruction.py`:

```python
def test_report_writer_can_skip_the_registry(tmp_path) -> None:
    from self_dual_wreath_multistar_degree_obstruction import (
        write_multistar_degree_obstruction_report,
    )

    path = tmp_path / "multistar.json"
    payload = write_multistar_degree_obstruction_report(
        path=path,
        write_registry=False,
        sampled_degrees=(7, 10),
        sample_count=8,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"][
        "laplacian_equivalence_failure_count"
    ] == 0
```

- [ ] **Step 2: Run the test and confirm it fails**

Run: `python -m pytest tests/test_self_dual_wreath_multistar_degree_obstruction.py::test_report_writer_can_skip_the_registry -v`

Expected: FAIL with `TypeError: ... unexpected keyword argument 'write_registry'`.

- [ ] **Step 3: Add the registry imports**

In `self_dual_wreath_multistar_degree_obstruction.py`, find this line:

```python
from research_registry import utc_now
```

Replace it with:

```python
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
```

- [ ] **Step 4: Replace the report writer**

Find this function:

```python
def write_multistar_degree_obstruction_report(
    path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_multistar_degree_obstruction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
```

Replace it with exactly:

```python
def write_multistar_degree_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_multistar_degree_obstruction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-SIGN-BLIND-MULTISTAR-CERTIFICATE",
                source=str(path),
                claim=(
                    "Block Gershgorin on absolute pair-core overlap weights "
                    "can certify the residual pair quotient at all depth."
                ),
                reason_invalid=(
                    "The crossing graph of a sibling merge is complete "
                    "bipartite and Sellke covering saturates the off-common "
                    "weight at 1/(n-1), so the weighted degree grows like "
                    "2^(j-1)/(n-1) and the certificate is already vacuous at "
                    "n=8 on natural threshold portfolios."
                ),
                lesson=(
                    "Only a phase-sensitive argument can survive. Bound the "
                    "positive spectrum of the projector-weighted orientation "
                    "Laplacian Delta = D - A, whose nonzero spectrum equals "
                    "that of the existing relation Gram."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
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
                artifacts={
                    "self_dual_wreath_multistar_degree_obstruction": str(path)
                },
            )
        )
    return payload
```

- [ ] **Step 5: Run the focused tests and confirm they pass**

Run: `python -m pytest tests/test_self_dual_wreath_multistar_degree_obstruction.py -q`

Expected: `9 passed`.

---

### Task 3: Seed both experiment records

**Files:**
- Modify: `research_registry.py` (immediately after the `ExperimentRecord` whose `id="EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT"`, which begins at line 7534)

**Interfaces:**
- Consumes: the `ExperimentRecord` dataclass already imported in that file. Its fields, in the order used below, are `id`, `candidate_id`, `title`, `status`, `hypothesis`, `protocol`, `positive_signal`, `falsifiers`, `metrics`, `dependencies`, `next_actions`.
- Produces: two seeded records that Task 4 and Task 8 read by id.

- [ ] **Step 1: Locate the insertion point**

Run: `grep -n 'EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT' research_registry.py`

Expected: one line number near 7535. Scroll from there to the closing `),`
of that `ExperimentRecord(` call — it is the line after the `next_actions=[...]`
list closes. Insert the two new records immediately after that `),`.

- [ ] **Step 2: Insert both records**

```python
        ExperimentRecord(
            id="EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Exact pair-core carrier factorization",
            status="planned",
            hypothesis=(
                "The overlap operator of two exact orientation pair cores "
                "has a closed form in representation-ring data, so its "
                "off-common contraction can be proved for all n instead of "
                "measured on finite screens."
            ),
            protocol=(
                "Grade every tensor factor of a three-orientation family by "
                "its membership pattern, show both pair cores are graded by "
                "every block isotypic label, contract the forced carrier "
                "pairs in each of the two clusters, and validate the "
                "resulting two-carrier reciprocal spectrum against dense "
                "ambient singular values on S5, S6, and repeated-label "
                "controls."
            ),
            positive_signal=(
                "Every dense singular value, rank, and multiplicity is "
                "reproduced exactly, and every off-common correlation is at "
                "most 1/(n-1) for n>=5."
            ),
            falsifiers=[
                "A dense ambient singular value is missing from the closed form.",
                "An off-common correlation exceeds 1/(n-1).",
                "The closed form needs the collision-free sector.",
                "A shared-vertex overlap requires nontrivial multiplicity-space 6j data.",
                "A per-block contraction bound is described as all-depth conditioning.",
            ],
            metrics=[
                "exact_star_carrier_factorization_theorem_count",
                "all_n_off_common_star_bound_theorem_count",
                "disjoint_pair_waist_bound_theorem_count",
                "degenerate_racah_block_identification_count",
                "selected_star_control_count",
                "selected_star_failure_count",
                "screened_star_control_count",
                "screened_star_failure_count",
                "screened_off_common_violation_count",
                "maximum_spectrum_residual",
                "disjoint_waist_control_count",
                "disjoint_waist_violation_count",
                "disjoint_waist_tight_count",
                "repeated_label_star_control_count",
                "repeated_label_star_failure_count",
                "all_depth_multistar_conditioning_bound_count",
                "new_quantum_algorithm_count",
            ],
            dependencies=[
                "self_dual_wreath_pair_core_carrier_factorization.py",
                "self_dual_wreath_common_core_atomization.py",
                "self_dual_wreath_orientation_pair_angle_spectrum.py",
                "self_dual_wreath_orientation_triple_range.py",
                "symmetric-group representation ring",
            ],
            next_actions=[
                "Run qsearch.py code-wreath-pair-core-carrier-factorization.",
                "Derive the exact vertex-disjoint grid overlap or exhibit a strictly smaller grid.",
                "Feed the exact weights into the orientation Laplacian gap question.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Sign-blind multistar degree obstruction",
            status="planned",
            hypothesis=(
                "Exact pair-core weights plus the complete bipartite crossing "
                "graph decide whether any absolute-weight comparison can "
                "certify the residual pair quotient at natural depth."
            ),
            protocol=(
                "Compute exact off-common weights from the carrier "
                "factorization, count adjacency exactly on a sibling merge, "
                "sample natural high-dimension collision-free threshold "
                "portfolios from n=7 to n=12, and verify that the relation "
                "Gram and the projector-weighted orientation Laplacian have "
                "the same positive spectrum."
            ),
            positive_signal=(
                "A phase-sensitive lower bound on the positive Laplacian "
                "spectrum survives where the absolute-weight bound does not."
            ),
            falsifiers=[
                "Absolute-weight comparison is reintroduced as an all-depth argument.",
                "A vacuous certificate is described as a proof that the quotient gap fails.",
                "Sampled saturation is described as a proved asymptotic theorem.",
                "The Laplacian reformulation is described as supplying a gap.",
                "Shrinking per-block correlations are cited as evidence of conditioning.",
            ],
            metrics=[
                "exact_off_common_weight_law_count",
                "sign_blind_route_asymptotic_kill_count",
                "subspace_graph_laplacian_equivalence_theorem_count",
                "finite_merge_control_count",
                "finite_merge_certificate_available_count",
                "natural_sample_count",
                "natural_sample_vacuous_count",
                "first_vacuous_degree",
                "maximum_projected_weighted_degree_log2",
                "maximum_saturation_ratio",
                "weighted_degree_is_monotone_in_n",
                "laplacian_equivalence_control_count",
                "laplacian_equivalence_failure_count",
                "maximum_laplacian_spectrum_residual",
                "phase_sensitive_quotient_gap_theorem_count",
                "new_quantum_algorithm_count",
            ],
            dependencies=[
                "self_dual_wreath_multistar_degree_obstruction.py",
                "self_dual_wreath_pair_core_carrier_factorization.py",
                "self_dual_wreath_common_core_atomization.py",
                "self_dual_wreath_subgroup_twirl_reduction.py",
                "Sellke, Covering Irrep(S_n) With Tensor Products and Powers",
            ],
            next_actions=[
                "Run qsearch.py code-wreath-multistar-degree.",
                "Bound the smallest positive eigenvalue of the orientation Laplacian.",
                "Classify higher Cech homology on the vertex side of the duality.",
            ],
        ),
```

- [ ] **Step 3: Verify the file still parses**

Run: `python -c "import research_registry; print('ok')"`

Expected: `ok`.

- [ ] **Step 4: Verify both records are seeded**

Run:

```bash
python -c "
from research_registry import seed_candidate_records
_candidates, experiments = seed_candidate_records()
ids = {record.id for record in experiments}
for wanted in ('EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION','EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION'):
    print(wanted, wanted in ids)
"
```

Expected: both print `True`. `seed_candidate_records()` is defined at
`research_registry.py:298` and returns
`(list[CandidateRecord], list[ExperimentRecord])`.

---

### Task 4: Register both ids in the experiment runner

**Files:**
- Modify: `experiment_runner.py` — imports near line 171, `COSET_EXPERIMENTS` near line 862, `priority` dict inside `select_next_experiment()` at line 1853, dispatch chain near line 3894

**Interfaces:**
- Consumes: `write_pair_core_carrier_factorization_report` and `write_multistar_degree_obstruction_report` from Tasks 1 and 2, both accepting `write_registry`, `registry_experiment_id`, `registry_candidate_id`, `registry_result_id`.
- Produces: `python qsearch.py run <either id>` executes the module.

- [ ] **Step 1: Add the imports**

Find in `experiment_runner.py`:

```python
from self_dual_wreath_orientation_fusion_moment import (
    write_orientation_fusion_moment_report,
)
```

Insert immediately after it:

```python
from self_dual_wreath_pair_core_carrier_factorization import (
    write_pair_core_carrier_factorization_report,
)
from self_dual_wreath_multistar_degree_obstruction import (
    write_multistar_degree_obstruction_report,
)
```

- [ ] **Step 2: Add both ids to `COSET_EXPERIMENTS`**

Find the line `    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT",` (about
line 862, inside the `COSET_EXPERIMENTS = {` set that starts at line 820).
Insert immediately after it:

```python
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION",
```

- [ ] **Step 3: Add both ids to the `priority` dict**

Find the line `        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT": 99,`
(about line 2047, inside `priority = {` at line 1853). Insert immediately
after it:

```python
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION": 119,
        "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION": 120,
```

Values 119 and 120 are unused; the current maximum is 118. Do not renumber
anything else.

- [ ] **Step 4: Add both dispatch branches**

Find this block (about line 3894):

```python
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT"
        ):
            payload = write_orientation_fusion_moment_report(
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
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION"
        ):
            payload = write_pair_core_carrier_factorization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
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

- [ ] **Step 5: Verify the module imports and the runner tests pass**

Run:

```bash
python -c "import experiment_runner; print('ok')" && python -m pytest tests/test_experiment_runner.py -q
```

Expected: `ok`, then all tests in that file pass.

---

### Task 5: Add both `qsearch.py` subcommands

**Files:**
- Modify: `qsearch.py` — imports near line 530, new `command_*` functions after `command_code_wreath_orientation_moments` (starts line 6892), new `add_parser` blocks after the `code_wreath_orientation_moments` block (line 13014)
- Test: `tests/test_experiment_runner.py` (two new methods after line 330)

**Interfaces:**
- Consumes: the two report writers from Tasks 1 and 2, and the dispatch branches from Task 4.
- Produces: subcommands `code-wreath-pair-core-carrier-factorization` and `code-wreath-multistar-degree`, each with a `--no-registry` flag, plus two clean-registry dispatch tests.

- [ ] **Step 1: Add the imports**

Find in `qsearch.py`:

```python
from self_dual_wreath_orientation_fusion_moment import (
    write_orientation_fusion_moment_report,
)
```

Insert immediately after it:

```python
from self_dual_wreath_pair_core_carrier_factorization import (
    write_pair_core_carrier_factorization_report,
)
from self_dual_wreath_multistar_degree_obstruction import (
    write_multistar_degree_obstruction_report,
)
```

- [ ] **Step 2: Add both command functions**

Scroll to the end of `def command_code_wreath_orientation_moments(` (it starts
at line 6892 and ends with `return 0`). Insert both functions immediately
after that `return 0`, separated by two blank lines:

```python
def command_code_wreath_pair_core_carrier_factorization(
    args: argparse.Namespace,
) -> int:
    initialize_seed_registry(overwrite=False)
    payload = write_pair_core_carrier_factorization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Pair-core carrier factorization complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_pair_core_carrier_factorization.json"
    )
    print(
        "Selected/screened star controls and failures: "
        f"{metrics['selected_star_control_count']}/"
        f"{metrics['screened_star_control_count']}/"
        f"{metrics['selected_star_failure_count']}/"
        f"{metrics['screened_star_failure_count']}"
    )
    print(
        "Max spectrum residual / off-common violations: "
        f"{metrics['maximum_spectrum_residual']:.6g}/"
        f"{metrics['screened_off_common_violation_count']}"
    )
    print(
        "Disjoint waist controls/violations/tight: "
        f"{metrics['disjoint_waist_control_count']}/"
        f"{metrics['disjoint_waist_violation_count']}/"
        f"{metrics['disjoint_waist_tight_count']}"
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


def command_code_wreath_multistar_degree(
    args: argparse.Namespace,
) -> int:
    initialize_seed_registry(overwrite=False)
    payload = write_multistar_degree_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Multistar degree obstruction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_multistar_degree_obstruction.json"
    )
    print(
        "Natural samples/vacuous/first vacuous degree: "
        f"{metrics['natural_sample_count']}/"
        f"{metrics['natural_sample_vacuous_count']}/"
        f"{metrics['first_vacuous_degree']}"
    )
    print(
        "Max projected weighted degree log2 / saturation ratio: "
        f"{metrics['maximum_projected_weighted_degree_log2']:.6g}/"
        f"{metrics['maximum_saturation_ratio']:.6g}"
    )
    print(
        "Laplacian controls/failures/max residual: "
        f"{metrics['laplacian_equivalence_control_count']}/"
        f"{metrics['laplacian_equivalence_failure_count']}/"
        f"{metrics['maximum_laplacian_spectrum_residual']:.6g}"
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

- [ ] **Step 3: Add both subparser blocks**

Find this block (line 13014):

```python
    code_wreath_orientation_moments = subparsers.add_parser(
        "code-wreath-orientation-moments",
        help=(
            "Compute exact pairwise orientation-projector overlaps and "
            "class-algebra second moments through the copy threshold."
        ),
    )
    code_wreath_orientation_moments.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_moments.set_defaults(
        func=command_code_wreath_orientation_moments
    )
```

Insert immediately after it:

```python
    code_wreath_pair_core_carrier_factorization = subparsers.add_parser(
        "code-wreath-pair-core-carrier-factorization",
        help=(
            "Derive and validate the exact two-carrier reciprocal spectrum "
            "of shared-vertex pair-core overlaps."
        ),
    )
    code_wreath_pair_core_carrier_factorization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_core_carrier_factorization.set_defaults(
        func=command_code_wreath_pair_core_carrier_factorization
    )

    code_wreath_multistar_degree = subparsers.add_parser(
        "code-wreath-multistar-degree",
        help=(
            "Measure the exact sign-blind weighted degree of the crossing "
            "pair-core graph on natural threshold portfolios."
        ),
    )
    code_wreath_multistar_degree.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_multistar_degree.set_defaults(
        func=command_code_wreath_multistar_degree
    )
```

- [ ] **Step 4: Verify both subcommands are registered**

Run:

```bash
python qsearch.py --help | grep -E "code-wreath-pair-core-carrier-factorization|code-wreath-multistar-degree"
```

Expected: both names appear.

- [ ] **Step 5: Run both subcommands end to end**

Run:

```bash
python qsearch.py code-wreath-pair-core-carrier-factorization
```

Expected, in this order: the completion line, the artifact path,
`Selected/screened star controls and failures: 3/168/0/0`,
`Max spectrum residual / off-common violations: 5.82867e-16/0`,
`Disjoint waist controls/violations/tight: 40/0/40`,
`Speedup claim allowed: False`, `Registry valid: True`. Exit code 0.
Runtime is about 7 seconds.

Run:

```bash
python qsearch.py code-wreath-multistar-degree
```

Expected: `Natural samples/vacuous/first vacuous degree: 6/5/8`,
`Laplacian controls/failures/max residual: 2/0/<about 4e-14>`,
`Speedup claim allowed: False`, `Registry valid: True`. Exit code 0.
Runtime is about 36 seconds.

If either prints `Registry valid: False`, stop and report the printed issues.
Do not edit the registry by hand to make validation pass.

- [ ] **Step 6: Run both dispatch paths**

Run:

```bash
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION
```

Expected: both exit 0 and report a result row written.

- [ ] **Step 7: Add the two clean-registry dispatch tests**

In `tests/test_experiment_runner.py`, find
`def test_orientation_fusion_moment_dispatches_from_clean_registry(self):`
(line 308) and insert these two methods immediately after that method's final
`self.assertTrue(validation["valid"], validation["issues"])` line, keeping the
same four-space class indentation:

```python
    def test_pair_core_carrier_factorization_dispatches_from_clean_registry(
        self,
    ):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION"
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
            "self_dual_wreath_pair_core_carrier_factorization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_multistar_degree_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"
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
            "self_dual_wreath_multistar_degree_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])
```

- [ ] **Step 8: Run the two new dispatch tests**

Run:

```bash
python -m pytest tests/test_experiment_runner.py -q -k "carrier_factorization_dispatches or multistar_degree_obstruction_dispatches"
```

Expected: `2 passed`. Each takes under a minute.

---

### Task 6: Add the Sellke literature record

**Files:**
- Modify: `research/literature_index.json`
- Modify: `research/literature_records.json`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: a literature record that the Plancherel block obstruction and the
  multistar degree obstruction both cite.

- [ ] **Step 1: Check whether the paper is already present**

Run: `grep -c "2004.05283" research/literature_index.json research/literature_records.json`

If both counts are nonzero, mark this task complete and move to Task 7.

- [ ] **Step 2: Append the seed-paper entry**

`research/literature_index.json` is an object with keys `arxiv_metadata`,
`seed_papers`, `tag_index`. `seed_papers` is a list of 43 objects with
exactly the fields `id`, `tags`, `title`, `url`, `why_it_matters`, `year`.
Append this object to that list:

```json
{
  "id": "sellke-2020",
  "tags": [
    "symmetric-group",
    "representation-theory",
    "plancherel",
    "tensor-covering"
  ],
  "title": "Covering Irrep(S_n) With Tensor Products and Powers",
  "url": "https://arxiv.org/abs/2004.05283",
  "why_it_matters": "A fixed absolute number C of arbitrarily coupled Plancherel irreps of S_n tensor together to cover every irrep with probability 1-o(1), which supplies the block-covering step used by the Plancherel block obstruction and the multistar degree obstruction.",
  "year": 2020
}
```

- [ ] **Step 3: Append the full literature record**

`research/literature_records.json` is a flat list of 43 objects with exactly
the fields `abstract`, `id`, `mechanism`, `no_go_barrier`, `open_question`,
`problem_family`, `proof_technique`, `reduction`, `reusable_abstraction`,
`source`, `tags`, `title`, `url`, `year`. Append this object:

```json
{
  "abstract": "Theorem 1.2 shows that a fixed absolute number C of arbitrarily coupled Plancherel-distributed irreducible representations of S_n has a tensor product containing every irreducible representation with probability 1-o(1).",
  "id": "sellke-2020",
  "mechanism": "Plancherel-typical tensor products cover the whole dual of S_n after a bounded number of factors.",
  "no_go_barrier": "None on its own. The covering statement bounds no operator norm and supplies no convergence rate.",
  "open_question": "What quantitative rate does the covering event have, and does it survive conditioning on a fixed target constituent?",
  "problem_family": "Symmetric-group representation theory used inside hidden-subgroup and graph-isomorphism reductions.",
  "proof_technique": "Plancherel measure concentration plus character estimates on tensor product multiplicities.",
  "reduction": "Divide the natural k=ceil(log2 n!) labels into C-sized blocks so that both the left and right block products cover every irrep on all but an o(1) fraction of blocks; Markov applied to the expected bad-block fraction needs no convergence rate.",
  "reusable_abstraction": "Bounded-depth tensor covering of Irrep(S_n), used by EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION and EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION.",
  "source": "seed",
  "tags": [
    "symmetric-group",
    "representation-theory",
    "plancherel",
    "tensor-covering"
  ],
  "title": "Covering Irrep(S_n) With Tensor Products and Powers",
  "url": "https://arxiv.org/abs/2004.05283",
  "year": 2020
}
```

Do not add the new tags to `tag_index` by hand. If a test requires them,
regenerate the index with `python literature_pipeline.py` and inspect the
diff before keeping it.

- [ ] **Step 4: Verify both files still parse and the record is found**

Run:

```bash
python -c "
import json
for path in ('research/literature_index.json','research/literature_records.json'):
    json.load(open(path)); print(path, 'parses')
" && grep -c "2004.05283" research/literature_index.json research/literature_records.json
```

Expected: both parse, and each file reports at least 1.

- [ ] **Step 5: Run the literature tests**

Run: `python -m pytest tests/ -q -k "literature"`

Expected: all selected tests pass.

---

### Task 7: Refresh downstream artifacts and the README

**Files:**
- Modify: `README.md` (insert after the `code-wreath-orientation-moments` block, which ends around line 2224)
- Regenerated by commands: `research/dequantization_report.json`, `research/proof_status_report.json`, `research/query_model_ledger.json`, `research/frontier_map.json`, `research/conjecture_report.json`, `research/mutation_report.json`

**Interfaces:**
- Consumes: the two subcommands from Task 5.
- Produces: refreshed downstream artifacts and two README command blocks.

- [ ] **Step 1: Add the README blocks**

Find in `README.md` the sentence ending
`Growing orientation moments or a direct operator-valued Gram contraction remain necessary.`
Insert the following immediately after that paragraph:

````markdown
Factor the pair-core overlap operator exactly:

```bash
python qsearch.py code-wreath-pair-core-carrier-factorization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION
```

For two pair cores sharing an orientation, the overlap is exactly a direct
sum of `1/(d_beta d_p)` times partial isometries, with one carrier per
membership cluster and exact representation-ring multiplicities. The
conjectured single-reciprocal `1/d_alpha` law is therefore false in general;
finite screens saw single reciprocals only because their membership blocks
were singletons. Because a correlation equals one exactly when both carriers
are one dimensional, every off-common correlation is at most `1/(n-1)` for
`n>=5`. There is no nontrivial multiplicity-space 6j block at a shared
vertex; genuine Kronecker content first appears for vertex-disjoint cores,
where a waist bound applies. All 168 screened controls, three named
`d=5,9,10` controls, 40 repeated-label controls, and 40 disjoint controls
agree with the closed form to `5.83e-16`.

Measure the crossing-graph weighted degree:

```bash
python qsearch.py code-wreath-multistar-degree
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION
```

Block Gershgorin on the crossing relation Gram needs the absolute weighted
degree to stay below two. A sibling merge has a complete bipartite crossing
graph, and Sellke covering saturates the off-common weight at `1/(n-1)` as
the label count grows, so the degree grows like `2^(j-1)/(n-1)`. On natural
threshold portfolios the certificate is already vacuous at `n=8` and reaches
about `2^25.5` at `n=12`. No absolute-weight comparison can certify the
residual quotient at natural depth. The surviving object is the
projector-weighted orientation Laplacian `Delta = D - A`, whose positive
spectrum equals that of the relation Gram; no gap is proved for it.
````

- [ ] **Step 2: Refresh the downstream workflows**

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

Expected: every command exits 0 and `validate` reports no registry issues.
If `mutate` proposes anything that would enable a speedup claim, do not
accept it — report it and stop.

- [ ] **Step 3: Confirm no claim gate flipped**

Run:

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

Expected: `speedup gates open: []`. If the list is non-empty, stop and report.

---

### Task 8: Final verification and one commit

**Files:**
- No new edits. This task only verifies and commits.

- [ ] **Step 1: Run the focused test set**

Run:

```bash
python -m pytest tests/test_self_dual_wreath_pair_core_carrier_factorization.py tests/test_self_dual_wreath_multistar_degree_obstruction.py tests/test_self_dual_wreath_pair_core_recoupling_boundary.py tests/test_self_dual_wreath_common_core_atomization.py tests/test_self_dual_wreath_pair_quotient_overlap.py tests/test_experiment_runner.py -q
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
`research_registry.py`, the two module files, the two test files, the
literature files, and refreshed `research/**` artifacts. There must be **no**
change under `ag-remote/` beyond the pre-existing deletions.

- [ ] **Step 4: Commit once**

```bash
git add -A -- . ':!ag-remote'
git commit -m "Wire pair-core carrier factorization and multistar degree modules

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Do not push. Do not create a pull request.

---

### Task 9: Apply the same recipe to the wiring backlog

**Files:**
- Modify: `research_registry.py`, `experiment_runner.py`, `qsearch.py`, `README.md`

Tasks 1 through 5 are a repeatable recipe. Apply it, one module at a time, to
the experiment ids listed under "Mechanical Follow-Up For Antigravity /
Gemini 3.6 Flash" item 2 in `research/AGENT_HANDOFF.md` that are not yet
wired. As of this plan the following have modules and artifacts but no CLI or
dispatch entry — verify each with
`grep -c "<EXPERIMENT-ID>" qsearch.py experiment_runner.py` before starting,
and skip any that already returns a nonzero count in both files:

- `EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP` → CLI `code-wreath-pair-quotient-overlap`
- `EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION` → CLI `code-wreath-recursive-pair-generation`
- `EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH` → CLI `code-wreath-augmented-common-core-cech`
- `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN` → CLI `code-wreath-common-core-cech`
- `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY` → CLI `code-wreath-pair-core-recoupling`
- `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION` → CLI `code-wreath-common-core-atomization`

For each one:

1. Read its module docstring and its `theorem_contract`, `claim_gate`, and
   `falsifiers_triggered` fields in its artifact JSON.
2. Write the `ExperimentRecord` using **only** wording taken from those
   fields. Do not invent a hypothesis, a positive signal, or a falsifier.
3. Take the `metrics` list verbatim from the artifact's `headline_metrics`
   keys.
4. Use the next unused integer in the `priority` dict.
5. Follow Tasks 1, 4, and 5 for that module.
6. Re-run Task 7 Step 2 and Task 8 Steps 1 and 2.
7. Commit once per module.

Stop and report if any module's `run_*` function takes longer than five
minutes at its default arguments — say so rather than reducing its control
counts.

---

## What you must not do

- Do not change any formula, tolerance, control count, sample count, seed,
  ambient cap, or screen limit.
- Do not set `speedup_claim_allowed` to `true` anywhere.
- Do not delete or weaken a negative result, a proof obligation, an
  adversarial-audit entry, or a falsifier string.
- Do not reintroduce tiny-circuit or toy-oracle search.
- Do not describe a finite screen as an asymptotic theorem in any README or
  registry text you write.
- Do not mark an experiment `status` as anything other than `planned` in the
  seed record; the runner sets the live status.
- Do not attempt any of the eleven items in the "Highest-Value Open
  Derivation" section of `research/AGENT_HANDOFF.md`. Those need mathematical
  judgment and are explicitly out of scope for this plan.
