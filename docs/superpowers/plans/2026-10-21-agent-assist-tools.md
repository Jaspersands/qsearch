# Agent-Assist Tools Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Run the project's own test command (`python -m pytest -q tests/tools`) before calling any task done.

**Goal:** Seven tools that help the Codex/Gemini agents check their own work: a DQI candidate screener, a pre-commit preflight, arXiv-watch verdicts and citation re-checks, a duplicate-negative warning, a classical-baseline recommender, an independent note referee, and a generated per-session agent brief.

**Architecture:** Every tool is a new directory under `tools/` (or a new module inside `tools/corpus/`) with its own `python tools/<dir>/<script>.py` CLI, built on the existing corpus substrate (`tools/corpus/api.py`), the existing judge batch pattern (`tools/audit/rediscovery.py`) and the existing git-history helpers (`tools/cockpit/build_cockpit.py`). Agent-facing checks are also exposed on the corpus MCP server. Committed outputs go under `research/audits/`.

**Tech Stack:** Python 3.11, numpy/scipy (already present through scikit-learn and `requirements.txt`), scikit-learn TF-IDF via the corpus, `mcp` FastMCP, pytest. No new dependencies. LLM judging only through in-session Claude subagents reading exported batch files; no API key.

**Spec:** The brainstorm in this session (2026-10-21), summarised in **Context** below. There is no separate spec document; this plan carries the decisions.

---

## Context

The Q-Search research loop (Codex and two Gemini agents) proposes quantum mechanisms, attacks them classically and retains negatives. This week's work on the arXiv triage, the preprint and the merge showed that the agents' weak spot is checking, not proposing:

- The low-rate prime-character OPI line spent weeks on a comparison that Mazumder and Niroula's soundness rules (arXiv:2610.06753) settle in one calculation: within licensed Hamming decoding, DQI's margin over Prange completion is capped near 0.861 at this rate, and the classical witness already sits there.
- The merge of 2026-10-19 was blocked by 24 imports of untracked theorem modules and an invalid hypothesis contract (`research/hypotheses/dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge_contract.json`, still broken).
- The arXiv watch flagged 22 papers; 0 were real kills or scoops, 5 were already cited by notes written after the run, and the human verdicts live in a markdown file nothing reads.
- 283 notes are "review pending" by the corpus parser (307 by a looser grep), none independently reviewed; the outreach drafts have to say so.
- The ternary colouring line lacks the obvious classical baseline (the LP decoder of arXiv:2609.40036).
- The three note-level corrections from the triage are addressed to the agents but sit unread in `research/audits/ARXIV_TRIAGE_REVIEWED.md`.

Each project closes one of those gaps. The user's decisions (2026-10-21): execute "as last time" (one implementing session per phase group in parallel, adversarial review at the end), include both referee judging passes (calibration on the four preprint source notes, then the 30 newest review-pending notes), and commit the user's Oct 19 arXiv backfill on main before the work starts. **Execution is to be started by the user in a separate Opus session; this session only sets up.**

## Setup (this session, before execution)

- [x] Commit this plan into the repo as `docs/superpowers/plans/2026-10-21-agent-assist-tools.md` on branch `worktree-corpus-substrate` (6c0e2e26).
- [x] The merge-main session committed the user's backfill, `research/audits/arxiv_collisions.json` and `research/audits/ARXIV_WATCH.md` only, on main as f18baf61 (718 papers) and pushed.
- [x] Merged main into this branch (3896bc00); `python -m pytest -q tests/tools`: 498 passed. Post-merge checks: 718 papers in the branch's collisions file; no CLI import of an untracked module; of the four catalog notes only `FOLDED_NORM_MQ` is on main (the other three are still uncommitted agent edits).
- [x] Hand over: the execution session starts in this worktree (`.claude/worktrees/corpus-substrate`, branch `worktree-corpus-substrate`) and reads this file. Nothing under Phase 1 has been started.

## Global Constraints

- New directories only: `tools/dqi_screen/`, `tools/preflight/`, `tools/referee/`, `tools/brief/`; new modules `tools/corpus/duplicates.py`, `tools/corpus/baselines.py`, `tools/arxiv_watch/verdicts.py`, `tools/arxiv_watch/judge.py`.
- Never edit `core/`, `theorems/`, `research/*.md`, `research/hypotheses/*`, `research/registry/*`, `qsearch.py`, `qsearch_cli/`. The broken contract is reported by preflight, not fixed by us.
- Tools never import `core/` or `theorems/`. They may import other `tools/` modules.
- Committed outputs only under `research/audits/` (new: `arxiv_verdicts.json`, `registry_duplicates.json`, `REGISTRY_DUPLICATES.md`, `reviews/`, `REFEREE_QUEUE.md`, `AGENT_BRIEF.md`, `agent_brief.json`).
- Tests in `tests/tools/test_<tool>.py`; CLIs invoked in-process via `main([...])` with `capsys`; fixtures from `tests/tools/conftest.py` (`fake_repo`, `NEGATIVES`); real temp git repos follow `tests/tools/test_failure_modes.py:150-162`.
- `tests/tools/test_corpus_mcp.py:28` asserts the exact MCP tool-name list; each project that adds a tool updates it. Final list: `["been_tried", "check_duplicate_negative", "classical_baselines", "get_doc", "screen_dqi_candidate", "search_corpus"]`.
- Each new tool directory gets `__init__.py`, `README.md`, and a bullet in `docs/REPOSITORY_MAP.md` (lines 35-45, form `` `tools/<dir>/` - purpose; outputs in `research/audits/...` ``).
- Scripts use the `if __package__ in (None, ""): sys.path.insert(0, parents[2])` idiom from `tools/claim_checker/check.py:28`.
- Git: `git add` own paths only; never `-A`, `reset`, `stash`, `clean`; leave `ag-remote/` alone. Commit subjects `<Tool name>: imperative summary`; bodies say why; end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Judging: export batches → a fresh in-session subagent reads `INSTRUCTIONS.md` + `batch_NN.json` and writes JSONL → import with verbatim-quote verification (≥ 6 words, `_norm`-collapsed whitespace, as in `tools/audit/rediscovery.py`).

## Task protocol (applies to every task below)

1. Write the named test(s) with the assertions given; run `python -m pytest -q tests/tools/<file>::<test> -v`; confirm it fails for the expected reason (ImportError/AttributeError/AssertionError as noted).
2. Implement exactly the signatures listed under **Produces**; nothing more.
3. Run the test; pass. Run the tool's whole test file; pass.
4. Commit the listed paths with the listed message.

Only the test names, assertions, signatures, decisions and commit lines are given per task; the four steps are implied.

## Phase order and sessions

| Phase | Parallel sessions (disjoint files) | Depends on |
|---|---|---|
| 1 | P1 screener · P4 preflight · P6 watch · P7 duplicates | — |
| 2 | P5 baselines · P2 referee | P5 cites P1's `prange.py`; P2 is independent |
| 3 | P3 brief | reads P6, P2, P4, P7 outputs (degrades when absent) |
| 4 | Adversarial review of all seven, fixes, merge to main via the merge-main session, push | all |

P6, P7 and P5 all touch `tools/corpus/cli.py`, `mcp_server.py`, `test_corpus_mcp.py` and `tools/corpus/README.md`: run P7 and P5 in the **same** session (sequentially), and P6 in its own. P1's MCP tool also edits `mcp_server.py`; land P1 first in phase 1, then P7.

---

# Phase 1

## Project 1: DQI candidate screener — `tools/dqi_screen/`

**Files**
- Create: `tools/dqi_screen/__init__.py`, `rules.py`, `screen.py`, `prange.py`, `README.md`, `examples/opi_prime_character_r19.json`, `examples/opi_prime_character_r32.json`, `examples/mpi_signed_cosine.json`, `examples/hermite_half_rate.json`
- Modify: `tools/corpus/mcp_server.py`, `tests/tools/test_corpus_mcp.py:28`, `docs/REPOSITORY_MAP.md`
- Test: `tests/tools/test_dqi_screen.py`

Rules implemented (Mazumder & Niroula, arXiv:2610.06753; α = n/m, ρ = accepted density, λ = ℓ/m, licensed radius means 2ℓ+1 < d):
- Q_Pr = ρ + (1−ρ)α. Q_DQI(λ,ρ) = (√(λ(1−ρ)) + √(ρ(1−λ)))², and 1 when λ > 1−ρ. μ = Q_DQI − Q_Pr.
- λ_crit(α,ρ) = (√((1−ρ)Q_Pr) − √(ρ(1−Q_Pr)))². ρ_crit(α) = ½(1 − √(2(1−α)/(2−α))).
- Reach bounds: Singleton α/2; distance δ/2; sphere packing H_q⁻¹(α); Plotkin (1−1/q)α/2. R1 passes iff every applicable bound exceeds λ_crit.
- Cap: κ(α) = √(u(1−u)) − u, u = α/2; universal (√2−1)/2.
- Cosine objective: 2√(λ(1−λ)) vs α; λ_crit^cos = (1−√(1−2α²))/2 for α < 1/√2, none otherwise.
- Restarts (Thm 10): m ≥ (1−α)R² ln(N/η)/(2μ_m²), R = 1 count / 2 cosine, N = 2⁴⁰, η = 0.05.
- R3: Q* with D_KL(Q*‖ρ) = α ln q when q^α ρ < 1, else 1; encoder known ⇒ margin ≤ 0. R4: α_sub = min(1, bα/c), baseline ρ + (1−ρ)⌊α_sub m⌋/m, blocks at ρ=½ when α ≥ 2c²/(b²+c²).
- Verdict: any hard check false → "not viable" (R1, reach, R2, R3-encoder, R4, cosine α ≥ 1/√2); else any None or soft flag false → "unknown" (witness within 0.01 of cap, restart length > m); else "viable". CLI exit 1 only for "not viable".

### Task 1.1 — objectives and threshold
Produces in `rules.py`: `q_prange(alpha, rho) -> float`, `q_dqi(lam, rho) -> float`, `margin(lam, alpha, rho) -> float`, `lambda_crit(alpha, rho) -> float`, `rho_crit(alpha) -> float`; `ValueError` unless 0 < α, ρ < 1.
Test `test_objective_and_threshold_hand_values`:
```python
a = 39 / 127
assert R.q_prange(a, 0.5) == pytest.approx(0.654, abs=5e-4)
assert R.q_dqi(19 / 127, 0.5) == pytest.approx(0.857, abs=5e-4)
assert R.q_dqi(0.9, 0.5) == 1.0
assert R.lambda_crit(a, 0.5) == pytest.approx(0.024, abs=5e-4)
assert R.lambda_crit(0.5, 0.5) == pytest.approx(0.067, abs=5e-4)
assert R.rho_crit(0.5) == pytest.approx(0.092, abs=5e-4)
```
Commit: `git add tools/dqi_screen/__init__.py tools/dqi_screen/rules.py tests/tools/test_dqi_screen.py` — "DQI screen: add the satisfied-count objectives and the Prange threshold".

### Task 1.2 — reach bounds, caps, cosine, restarts, R3/R4
Produces in `rules.py`: `UNIVERSAL_CAP`, `licensed_radius(min_distance) -> int` (= (d−2)//2), `singleton_reach(alpha)`, `distance_reach(delta)`, `q_ary_entropy(x, q)`, `q_ary_entropy_inverse(y, q)` (bisection on [0, 1−1/q]), `sphere_packing_reach(alpha, q)`, `plotkin_reach(alpha, q)`, `margin_cap(alpha)`, `cosine_objective(lam)`, `lambda_crit_cos(alpha) -> float | None`, `restart_length(alpha, mu, R, N=2**40, eta=0.05)`, `existential_line(alpha, rho, q)` (bisect D_KL on [ρ, 1)), `subfield_rate(alpha, b, c)`, `subfield_baseline(rho, alpha_sub, m)`, `subfield_blocks_at_half(alpha, b, c) -> bool`.
Tests `test_reach_bounds_caps_and_cosine` and `test_restarts_and_subfield_hand_values`:
```python
assert R.licensed_radius(40) == 19
assert R.singleton_reach(a) == pytest.approx(0.154, abs=5e-4)
assert R.sphere_packing_reach(a, 2**61 - 1) == pytest.approx(0.293, abs=5e-4)
assert R.q_ary_entropy(R.q_ary_entropy_inverse(0.3, 7), 7) == pytest.approx(0.3, abs=1e-9)
assert R.plotkin_reach(0.5, 2) == pytest.approx(0.125)
assert R.margin_cap(a) == pytest.approx(0.207, abs=5e-4)
assert R.margin_cap(0.5) == pytest.approx(0.183, abs=5e-4)
assert R.margin_cap(1 - 1 / 2**0.5) == pytest.approx(R.UNIVERSAL_CAP, abs=1e-9)
assert R.cosine_objective(209 / 6000) == pytest.approx(0.367, abs=5e-4)
assert R.lambda_crit_cos(0.07) == pytest.approx(0.00246, abs=5e-6)
assert R.lambda_crit_cos(0.8) is None
assert R.restart_length(a, 0.816830 - R.q_prange(a, 0.5), 1) == pytest.approx(399.2, abs=0.1)
assert R.existential_line(0.5, 0.5, 2**61 - 1) == 1.0
assert R.existential_line(0.2, 0.5, 7) == pytest.approx(0.909, abs=5e-4)
assert R.subfield_rate(0.3, 2, 1) == pytest.approx(0.6)
assert R.subfield_baseline(0.5, 0.6, 100) == pytest.approx(0.8)
assert R.subfield_blocks_at_half(0.5, 2, 1) is True and R.subfield_blocks_at_half(0.3, 2, 1) is False
```
Commit: `git add tools/dqi_screen/rules.py tests/tools/test_dqi_screen.py` — "DQI screen: add reach bounds, margin caps, cosine threshold and finite-length rules".

### Task 1.3 — `Candidate`, `screen()`, examples
Produces in `screen.py`:
```python
@dataclass(frozen=True)
class Candidate:
    name: str; objective: str; q: int; m: int; n: int; rho: float
    radius: int | None = None; min_distance: int | None = None
    decoder_known: bool = False; encoder_known: bool = False
    p: int | None = None; b: int | None = None; c: int | None = None
    classical_witness: float | None = None; finite_dqi_mean: float | None = None
@dataclass(frozen=True)
class Check: rule: str; passed: bool | None; detail: str
@dataclass
class Screen: candidate: Candidate; quantities: dict[str, float | int | None]; checks: list[Check]; verdict: str; reasons: list[str]
def candidate_from_dict(data: dict) -> Candidate     # ValueError on unknown keys / bad objective
def load_candidate(path: Path) -> Candidate
def screen(c: Candidate) -> Screen
```
`quantities` keys: `alpha, lam, delta, q_prange, q_dqi, q_dqi_finite, margin, margin_finite, lambda_crit, radius_crit, licensed_radius, singleton_reach, distance_reach, sphere_packing_reach, plotkin_reach, kappa, q_cap, cosine_objective, lambda_crit_cos, restart_length, existential_line, rho_crit, alpha_sub, subfield_baseline`. Check rules: `R1, reach, R2, R3, R3-encoder, R4, cap, witness, restarts`. R4 detail "not applicable (prime field)" when b/c absent and q prime (`sympy.isprime`), `passed None` with detail "give p, b, c" for a prime power.
Examples: (a) `{"name": "opi-prime-character-r19", "objective": "count", "q": 2305843009213693951, "m": 127, "n": 39, "rho": 0.5, "radius": 19, "min_distance": 40, "decoder_known": true, "classical_witness": 0.8582677165354331, "finite_dqi_mean": 0.816830}`; r32: same with `radius 32`, `finite_dqi_mean 0.902855`; (b) `{"name": "mpi-signed-cosine", "objective": "cosine", "q": 8191, "m": 6000, "n": 420, "rho": 0.5, "radius": 209, "decoder_known": true}`; (c) `{"name": "hermite-half-rate", "objective": "count", "q": 8191, "m": 1000, "n": 500, "rho": 0.5, "radius": 124, "min_distance": 250, "decoder_known": true}`.
Tests (`EXAMPLES = REPO / "tools/dqi_screen/examples"`):
- `test_example_a_radius_19_numbers`: `q_prange ≈ 0.654`, `lambda_crit ≈ 0.024`, `radius_crit ≈ 3.07 (abs 5e-3)`, `licensed_radius == 19`, `kappa ≈ 0.207`, `q_cap ≈ 0.861`, `restart_length ≈ 399.2`; `checks["R1"].passed is True`, `checks["reach"].passed is True`, `checks["witness"].passed is False and "0.01" in detail`; `verdict == "unknown"`.
- `test_example_a_radius_32_is_outside_licensed_reach`: `checks["reach"].passed is False`, `"outside licensed Hamming reach" in detail`, `verdict == "not viable"`.
- `test_example_b_cosine_is_viable`: `lambda_crit_cos ≈ 0.00246`, `cosine_objective ≈ 0.367`, `checks["R1"].passed is True`, `verdict == "viable"`.
- `test_example_c_half_rate`: `lambda_crit ≈ 0.067`, `singleton_reach == 0.25`, `kappa ≈ 0.183`, `checks["R4"].passed is None and "prime field" in detail`.
- `test_encoder_known_caps_margin_at_zero`: `replace(cand, encoder_known=True)` → `checks["R3-encoder"].passed is False`, verdict "not viable".
- `test_prime_power_q_without_subfield_inputs_is_unknown_not_na`: q=4096 → R4 `passed is None`, "give p, b, c" in detail.
- `test_saturated_reach_is_flagged_not_viable`: count objective with λ > 1−ρ → verdict "not viable", a check detail mentioning "saturated".
Commit: `git add tools/dqi_screen/screen.py tools/dqi_screen/examples tests/tools/test_dqi_screen.py` — "DQI screen: screen a candidate against the Mazumder-Niroula soundness rules".

### Task 1.4 — `render` and CLI
Produces: `render(s: Screen) -> str` (title `# DQI screen: <name>`, quantities table, one line per check, verdict and reasons); `main(argv) -> int` with `--params FILE` or `--name/--objective/--q/--m/--n/--rho/--radius/--min-distance/--decoder-known/--encoder-known/--p/--b/--c/--classical-witness/--finite-dqi-mean`, `--json`, `--out PATH`; exit 0 viable/unknown, 1 not viable.
Test `test_cli_json_and_markdown(capsys, tmp_path)`:
```python
assert main(["--params", str(EXAMPLES / "mpi_signed_cosine.json"), "--json"]) == 0
payload = json.loads(capsys.readouterr().out)
assert payload["verdict"] == "viable" and payload["quantities"]["cosine_objective"] == pytest.approx(0.367, abs=5e-4)
out = tmp_path / "s.md"
assert main(["--params", str(EXAMPLES / "opi_prime_character_r32.json"), "--out", str(out)]) == 1
assert "outside licensed Hamming reach" in out.read_text() and "# DQI screen: opi-prime-character-r32" in out.read_text()
assert main(["--objective", "count", "--q", "7", "--m", "100", "--n", "30", "--rho", "0.5", "--radius", "5", "--min-distance", "20", "--decoder-known"]) == 0
```
Commit: `git add tools/dqi_screen/screen.py tests/tools/test_dqi_screen.py` — "DQI screen: render a markdown report and add the command line".

### Task 1.5 — finite-length Prange baseline
Produces in `prange.py`: `prange_restarts(B: np.ndarray, accepted: Sequence[Collection[int]], q: int, restarts: int = 1, seed: int | None = None) -> dict` returning `{"best", "scores", "restarts", "m", "n", "q", "singular"}`. Algorithm: one `np.random.default_rng(seed)`; per restart permute rows, Gaussian-eliminate mod q on Python ints (object dtype, since q up to 2⁶¹−1 overflows int64) to pick the first n independent rows I, draw targets v_i ∈ accepted[i] for i ∈ I, solve, score = fraction of rows whose (Bx)_i mod q is accepted; restarts consume the RNG sequentially; `ValueError` for non-prime q; rank-deficient draws score 0 and count in `singular`.
Tests: `test_prange_full_field_scores_one` (random 6×3 over F_5, `accepted = [range(5)]*6` → `best == 1.0`); `test_prange_more_restarts_never_lower_best` (12×4 over F_7, `accepted = [{0,1,2}]*12`, seed 1: best(3) ≤ best(12) and `scores[:3]` equal); `test_prange_large_prime_field` (q = 2⁶¹−1, 4×2 instance with a planted solution x and accepted sets {Bx mod q} → best 1.0).
Commit: `git add tools/dqi_screen/prange.py tests/tools/test_dqi_screen.py` — "DQI screen: add a best-of-N Prange completion baseline over prime fields".

### Task 1.6 — MCP tool
Produces: `@server.tool() def screen_dqi_candidate(params: dict) -> dict` in `tools/corpus/mcp_server.py` returning `asdict(screen(candidate_from_dict(params)))` or `{"error": str}`; docstring says it is a soundness screen, not a proof.
Tests: update the tool-name assertion to include `screen_dqi_candidate`; `test_screen_dqi_candidate_tool`: the cosine example → `payload["verdict"] == "viable"`; `{"objective": "count"}` → `payload["error"]`.
Commit: `git add tools/corpus/mcp_server.py tests/tools/test_corpus_mcp.py` — "DQI screen: expose screen_dqi_candidate on the corpus MCP server".

### Task 1.7 — README and map
`tools/dqi_screen/README.md` (purpose, each rule with its formula name, CLI examples, the four example outputs, "what it does not prove": asymptotic rules, worst-case Hamming decoding only, no finite certificate); map bullet after `docs/REPOSITORY_MAP.md:45`. Commit — "DQI screen: document the screener and list it in the repository map".

## Project 4: preflight — `tools/preflight/`

**Files**
- Create: `tools/preflight/__init__.py`, `preflight.py`, `README.md`
- Modify: `docs/REPOSITORY_MAP.md`
- Test: `tests/tools/test_preflight.py` with helpers `_git(repo, *args)` (from `test_failure_modes.py:150-162`) and `_repo(tmp_path)` writing a minimal tree (`qsearch.py`, `qsearch_cli/__init__.py`, `qsearch_cli/imports.py` with a literal `IMPORTS`, `qsearch_cli/commands/general.py`, `qsearch_cli/registry.py` with literal `ORDER`/`FUNCTIONS`/`DISPATCH`, `research/audits/cli_manifest.json`), then `git init`, add, commit.

Design: all default checks are static. Module references come from (i) AST `ImportFrom`/`Import` nodes starting with `theorems.`/`core.` in `qsearch.py`, `qsearch_cli/imports.py`, `qsearch_cli/commands/*.py`; (ii) the `IMPORTS` literal (`ast.literal_eval`; bare names map to `theorems/<m>.py` else `core/<m>.py`; skip `sys.stdlib_module_names`); (iii) the module column of `DISPATCH` in `registry.py`. Tracked set from one `git -C root ls-files -z -- theorems core`. `ORDER` is read with `ast.literal_eval`, never imported.

### Task 4.1 — `Problem` and `check_json`
Produces: `JSON_DIRS = ("research/hypotheses", "research/registry", "research/audits", "research/classical_baselines")`; `@dataclass(frozen=True) class Problem: check: str; path: str; message: str` (path root-relative posix); `check_json(root: Path) -> list[Problem]` (rglob, sorted; JSONDecodeError/UnicodeDecodeError/OSError text as message).
Tests: `test_check_json_reports_the_parse_error` (a file with `"bad \x escape"` → one problem, `check == "json"`, message startswith `"Invalid \\escape: line 1 column"`; an `[]` file is fine); `test_check_json_finds_todays_broken_contract` against `REPO` (skip if `research/hypotheses` absent): the dcp_clifford contract is reported with message startswith `"Invalid \\escape: line 7 column 167"` — delete this test once the agents fix the file; `test_problem_paths_are_relative_with_a_relative_root` (`monkeypatch.chdir`, `--root .`).
Commit: `git add tools/preflight/__init__.py tools/preflight/preflight.py tests/tools/test_preflight.py` — "Preflight: report research JSON files that do not parse".

### Task 4.2 — `check_untracked_imports`
Produces: `IMPORT_SOURCES`, `referenced_modules(root) -> dict[str, set[str]]` (module path → source files), `tracked_files(root) -> set[str] | None` (None without git), `check_untracked_imports(root) -> list[Problem]` (check "imports"; messages "missing on disk" | "not tracked by git" | one "git unavailable" problem).
Test `test_untracked_and_missing_theorem_modules`: repo commits `theorems/tracked.py` and `theorems/dispatched.py`; `commands/general.py` has lazy imports of `theorems.tracked`, `theorems.untracked`, `core.gone`; `IMPORTS = {"w": ("table_mod", "w"), "os": ("os", None)}`; `DISPATCH = [("flag", "theorems.dispatched", "gen")]`; after the commit write `theorems/untracked.py` and `theorems/table_mod.py` uncommitted. Assert `{(p.path, p.message)} == {("theorems/untracked.py", "not tracked by git"), ("theorems/table_mod.py", "not tracked by git"), ("core/gone.py", "missing on disk")}`. Also `test_referenced_modules_ignores_stdlib_table_entries`, `test_real_checkout_has_no_untracked_imports` (REPO → `[]`), `test_without_git_reports_one_git_unavailable_problem`.
Commit — "Preflight: flag theorem and core modules the CLI references but git does not track".

### Task 4.3 — `check_manifest`
Produces: `MANIFEST = "research/audits/cli_manifest.json"`, `registry_order(root) -> dict[str, str]`, `check_manifest(root) -> list[Problem]` (check "manifest"; "subcommand X missing from ORDER" | "X: manifest says A, ORDER says B"; a missing/invalid manifest is one problem).
Tests: `test_manifest_subcommand_missing_from_order` (two-entry manifest vs one-entry ORDER → exactly the missing message; module mismatch case → the mismatch message); `test_real_manifest_matches_registry` (REPO → `[]`).
Commit — "Preflight: check every manifest subcommand is still in the registry".

### Task 4.4 — `run`, optional checks, CLI
Produces: `check_imports_resolve(root)` (wraps `tools.split_cli.verify.check_imports` through a lazily imported module-level `_check_imports` indirection; check "resolve"); `check_validate(root)` (subprocess `[sys.executable, "qsearch.py", "validate"]`; check "validate"; message "exit N: <last stderr line>"); `run(root, imports=False, validate=False) -> list[Problem]`; `main(argv) -> int` with `--root --json --imports --validate`; prints `f"{check}: {path}: {message}"` per problem then `f"{n} problems"` (`--json`: `{"root", "problems", "count"}`); returns 1 if any.
Tests: `test_main_prints_problems_and_exits_one` (dirty repo → 1 and the imports line; clean repo `--json` → 0, `count == 0`); `test_validate_flag_reports_nonzero_exit` (`qsearch.py` = `import sys; sys.exit(3)` → a "validate" problem with "exit 3"); `test_imports_flag_uses_split_cli_verify` (monkeypatch `_check_imports` → `(2, ["x: ImportError: y"])` → one "resolve" problem). Then run `python tools/preflight/preflight.py` on the real checkout and confirm exactly one line (the JSON contract).
Commit — "Preflight: add run() and the command line with optional import and validate checks".

### Task 4.5 — README and map
README: what each check catches, the two merge incidents it exists for, the slow flags, exit codes, the one-liner for the agents (`python tools/preflight/preflight.py` before every commit). Commit — "Preflight: document the pre-commit checks".

## Project 6: arXiv watch verdicts, citation re-check, judge — `tools/arxiv_watch/`

**Files**
- Create: `tools/arxiv_watch/verdicts.py`, `judge.py`, `research/audits/arxiv_verdicts.json`
- Modify: `watch.py`, `README.md`, `docs/REPOSITORY_MAP.md:37`
- Tests: append to `tests/tools/test_arxiv_watch.py`; new `tests/tools/test_arxiv_judge.py`

Decisions: `label` stays the machine label; `verdict` is attached from `arxiv_verdicts.json` (source of truth, keyed by arXiv id, independent of stored state); `record["verdict"]` set only when a verdict exists and popped otherwise so unchanged weeks stay byte-identical; the digest's flagged sections skip papers with verdicts and a `## Reviewed` table is driven by the verdicts file (ids absent from state show "not stored"). The weekly workflow will open a PR the first run after seeding because 22 records change; the README says so.

### Task 6.1 — verdict store
Produces in `verdicts.py`: `VERDICTS = ("kill", "scoop", "should-cite", "related-only", "false-alarm")`, `VERDICTS_FILE = "research/audits/arxiv_verdicts.json"`, `load_verdicts(root) -> dict` (`{"verdicts": {}}` when absent), `save_verdicts(root, data)` (sort_keys, indent 2, newline), `set_verdict(root, arxiv_id, verdict, reason, by, action=None, today=None) -> dict`.
Tests: `test_verdict_round_trip` (entry equals `{"verdict": "false-alarm", "reason": "cue spurious", "action": None, "by": "human", "reviewed_on": "2026-10-21"}`); `test_set_verdict_rejects_unknown_value` (`ValueError`).
Commit: `git add tools/arxiv_watch/verdicts.py tests/tools/test_arxiv_watch.py` — "arXiv watch: add a persistent verdict store".

### Task 6.2 — attach verdicts; Reviewed section
Produces: `attach_verdicts(state, verdicts) -> int` (records whose `verdict` key changed); `render_digest(state, per_section=40, verdicts=None) -> str`; `_save` loads verdicts and passes them; `run()` and `relabel()` call `attach_verdicts` after `_load_state`, `changed |= bool(n)`.
Test `test_paper_with_a_verdict_leaves_the_flagged_list`: after a run with the kill paper, `set_verdict(..., "false-alarm", ...)`, run again with the same client → `report.new == 0`, `report.saved`, record `verdict["verdict"] == "false-alarm"`, the "## Possible kills" section lacks the id, "## Reviewed" contains `| 2610.11111 |` and `false-alarm`; a verdict for an id not in state renders "not stored".
Commit — "arXiv watch: verdicts suppress flags and render a Reviewed table".

### Task 6.3 — demote flags cited later
Produces: `recheck_cited(state, corpus, today) -> int`; `RunReport.relabelled: int = 0`; called in `run()` right after `attach_verdicts`; for stored papers with label in {possible-kill, possible-scoop} and no verdict, `corpus.mentions(id)` → label "already-cited", `relabelled_on`, `relabelled_from`; `main()` prints the count.
Test `test_flagged_paper_becomes_already_cited_once_a_note_cites_it`: run (today 2026-10-19); write `research/CITES_KILL.md` mentioning `arXiv:2610.11111v1`; `corpus.refresh()`; run again (2026-10-26) → `report.relabelled == 1`, label "already-cited", `relabelled_on == "2026-10-26"`, `relabelled_from == "possible-kill"`; a verdict-bearing paper is untouched. Plus the performance guard: 30 flagged ids sharing a trailing token complete in under one second on the fake repo.
Commit — "arXiv watch: demote stored flags once a note cites the paper".

### Task 6.4 — `--verdict` CLI and README
Produces: `main(argv)` gains `--verdict ARXIV_ID VERDICT` (nargs=2), `--reason`, `--action`, `--by` (default human); exit 2 on an unknown verdict; no fetch, no Corpus; re-renders the digest.
Test `test_verdict_flag_records_and_rerenders_without_fetching` (`== 0`, file updated, digest has the Reviewed row; unknown verdict → 2). README: replace the "never re-labelled" lines (L24, L29-31) with the two exceptions, document `--verdict`, the five values, the Reviewed table, "labels are triage, verdicts are judgement", and the PR-on-seed note.
Commit: `git add tools/arxiv_watch/watch.py tools/arxiv_watch/README.md tests/tools/test_arxiv_watch.py` — "arXiv watch: --verdict records a reviewed verdict and re-renders the digest".

### Task 6.5 — seed the 22 human verdicts
Write `research/audits/arxiv_verdicts.json` by hand from `ARXIV_TRIAGE_REVIEWED.md`: should-cite (9: 2610.06753, 2610.03566, 2610.00502, 2610.03645, 2609.40036, 2610.03697, 2610.01141, 2609.37636, 2610.16827); related-only (8: 2610.01902, 2609.35101, 2609.40250, 2610.02079, 2609.40260, 2610.04597, 2610.05752, 2610.08714); false-alarm (5: 2609.40302, 2609.35239, 2609.36480, 2610.06781, 2610.06812). `reason` = the review's reason sentence; `action` = its action clause or null; `by "human"`, `reviewed_on "2026-10-21"`; for 2610.06753 and 2610.03566 set `action_done: true` (the preprint citations landed in 709980d0).
Test `test_seeded_verdicts_match_the_reviewed_triage` (real root; skip if the review file is absent): id sets equal; all `by == "human"`; counts `{"should-cite": 9, "related-only": 8, "false-alarm": 5}`.
Commit: `git add research/audits/arxiv_verdicts.json tests/tools/test_arxiv_watch.py` — "arXiv watch: seed the 22 reviewed verdicts".

### Task 6.6 — judge export
Produces in `judge.py`: `pending(state) -> list[tuple[str, dict]]` (flagged, no verdict, sorted by id); `export_batches(root, out_dir, n_batches=3, corpus=None) -> list[Path]` (items `{arxiv_id, title, abstract, label, cues, tracks, nearest: [{doc_id, title, excerpt}]}`, excerpt = `Corpus.get(doc_id).text[:600]`; `batch_NN.json = {"batch", "verdicts", "papers"}` round-robin, empty batches not written); `JUDGE_INSTRUCTIONS` (the five verdicts defined; a `quote` of ≥ 6 verbatim words from the abstract or one nearest excerpt, with `quote_from` = "abstract" or that doc_id, quoted within a single excerpt; one-line `action`; `confidence`; the JSONL row shape).
Test `test_export_lists_unreviewed_flags_with_excerpts`: one flagged paper plus one with a verdict → one batch, one paper, `nearest[0]["excerpt"]` contains "Helstrom", INSTRUCTIONS.md names all five verdicts.
Commit: `git add tools/arxiv_watch/judge.py tests/tools/test_arxiv_judge.py` — "arXiv watch: export judge batches for unreviewed flags".

### Task 6.7 — judge import and CLI
Produces: `import_judgements(root, paths, judge_name, corpus=None, today=None) -> {"imported": [ids], "rejected": [{"arxiv_id", "why"}]}`; `ValueError` on an unknown verdict or missing id; non-verbatim quote → rejected "quote not found"; existing human verdict → rejected "human verdict exists"; otherwise `set_verdict(..., by=f"judge:{judge_name}")` then `attach_verdicts` + `_save`. CLI mirrors `failure_modes.py`: `judge.py --export DIR [--batches 3]`, `judge.py --import FILES... --judge NAME`.
Tests: `test_import_rejects_unknown_verdict_and_non_verbatim_quote`; `test_judge_never_overwrites_a_human_verdict`; `test_quote_crossing_a_chunk_boundary_is_rejected`. README and map bullet name `arxiv_verdicts.json` and the judge loop.
Commit: `git add tools/arxiv_watch/judge.py tools/arxiv_watch/README.md docs/REPOSITORY_MAP.md tests/tools/test_arxiv_judge.py` — "arXiv watch: import judge verdicts with verbatim-quote checks".

## Project 7: duplicate-negative warning — `tools/corpus/duplicates.py`

**Files**
- Create: `tools/corpus/duplicates.py`, `tests/tools/test_corpus_duplicates.py`, `research/audits/registry_duplicates.json`, `research/audits/REGISTRY_DUPLICATES.md`
- Modify: `tools/corpus/api.py` (one method), `cli.py`, `mcp_server.py`, `README.md`, `docs/REPOSITORY_MAP.md:36`, `tests/tools/test_corpus_index.py:114`, `tests/tools/test_corpus_mcp.py`

Pre-measured on the branch index (987 negative-kind docs): pairs ≥ 0.7 / 0.8 / 0.9 / 0.95 = 1283 / 599 / 206 / 67; the top pairs are parameter-sweep siblings with identical text (`...GOPPA-SCALE-M6-T3-N48-0-1` vs `-0-2`).

### Task 7.1 — `near_duplicates`
Produces: `@dataclass(frozen=True) class Pair: a, b, score, title_a, title_b`; `near_duplicates(corpus, kind="negative", threshold=0.8, limit=200, per_family: int | None = None) -> list[Pair]` (`scipy.sparse.triu(sims, k=1).tocoo()`, keep ≥ threshold, sort desc, `a < b`; `per_family` caps pairs whose ids share the prefix before the last `-\d+` segment).
Tests: extend `test_matrix_gives_cosine_similarities_for_one_kind` (symmetry `atol=1e-6`; `len(ids)` equals the count of `negative:`/`quarantined:` docs); `test_near_duplicates_finds_the_planted_pair` (two planted records NEG-DUP-A/B with near-identical claims → first pair is them, score ≥ 0.8, no pair involves the Helstrom record; threshold 1.01 → `[]`); `test_per_family_cap_keeps_a_true_restatement_visible` (30 planted siblings + one restatement pair, `limit=10, per_family=2` → the restatement is present).
Commit: `git add tools/corpus/duplicates.py tests/tools/test_corpus_duplicates.py tests/tools/test_corpus_index.py` — "Corpus: near-duplicate pairs from the TF-IDF cosine matrix".

### Task 7.2 — `Corpus.cosine` and `check_claim`
Decision: `Hit.score` is an RRF fusion score, not a cosine; `TfidfState.scores(text)` is a true cosine. Produces: `Corpus.cosine(self, text, doc_ids) -> dict[str, float]` in `api.py`; `check_claim(corpus, text, threshold=0.6, k=5) -> list[Hit]` (search negatives with `k=max(2k, 10)`, re-score with `cosine`, keep ≥ threshold, sort desc, top k).
Tests: `test_check_claim_returns_cosine_scored_negatives_above_threshold` (Helstrom claim with two words changed → that record, `0.6 ≤ score ≤ 1.0`; "zebrafish migration" → `[]`); `test_cosine_of_a_doc_with_itself_is_one`.
Commit — "Corpus: check a draft claim against negatives by TF-IDF cosine".

### Task 7.3 — CLI `near-duplicates` and `check-new`
Produces in `cli.py`: `cmd_near_duplicates(args)` (`--kind --threshold --limit --per-family --out FILE.json`; writes the JSON `{"kind", "threshold", "pairs", "generated_on"}` and the markdown table at `FILE.with_name(FILE.stem.upper() + ".md")`); `cmd_check_new(args)` (`--text` | `--file`, `--threshold 0.6`; when the file parses as JSON with `claim`, use `claim` + `reason_invalid`; prints matches; returns 2 on any match, else 0; `--json` → `{"matches", "duplicate", **issues}`).
Tests: `test_cli_near_duplicates_writes_json_and_markdown`; `test_cli_check_new_exit_code_gates_on_a_match` (near-claim → 2; zebrafish → 0; `--file` with a full registry record → 2).
Commit — "Corpus CLI: near-duplicates report and check-new gate".

### Task 7.4 — MCP `check_duplicate_negative`
Produces: `check_duplicate_negative(claim: str, threshold: float = 0.6) -> dict` = `{"claim", "threshold", "matches", "duplicate", **issues}`. Update the tool-name assertion; `test_check_duplicate_negative_tool` (near-claim → `duplicate is True`; zebrafish → False).
Commit — "Corpus MCP: check_duplicate_negative tool".

### Task 7.5 — calibration and docs
Run `near-duplicates --json` at 0.7 / 0.8 / 0.9 on the real root; hand-check 10 pairs across the bands (sweep sibling / true restatement / distinct); choose the report default (expected 0.9) and keep 0.6 for `check-new`; write the committed report with `--out research/audits/registry_duplicates.json --per-family 3`. README "Duplicates" section (counts table, the 10-pair check, sweep-sibling caveat, hook exit code, quarantined records included); map bullet.
Commit: `git add tools/corpus/duplicates.py tools/corpus/cli.py tools/corpus/README.md docs/REPOSITORY_MAP.md research/audits/registry_duplicates.json research/audits/REGISTRY_DUPLICATES.md` — "Corpus: calibrate the duplicate threshold and commit the registry report".

---

# Phase 2

## Project 5: classical baseline recommender — `tools/corpus/baselines.py`

**Files**
- Create: `tools/corpus/baselines.py`, `tools/corpus/baselines.json`, `tests/tools/test_corpus_baselines.py`
- Modify: `tools/corpus/cli.py`, `mcp_server.py`, `README.md`, `docs/REPOSITORY_MAP.md`, `tests/tools/test_corpus_mcp.py`

### Task 5.1 — catalog and validation
Schema: `{"baselines": [{"id", "name", "aliases": [], "problem", "mechanisms": [3-6 lowercase keywords], "summary", "references": [{"arxiv": id} | {"note": stem}], "runnable": {"command", "entry"?} | null}]}`. Fourteen entries; note references must exist at the tested root (four stems exist only in the main checkout until the agents commit: BALANCED_SIGNED_MPI, CUBIC_ORBIT_DECODER, TERNARY_COLORING_BPQM, FOLDED_NORM_MQ — list them in the README as "add back when present"):

| id | references |
|---|---|
| prange-isd | PARITY_BLOCK_USD_PRANGE, BPQM_GIBBS_FRONTIER, LINEAR_ERASURE_PRANGE_DUALITY |
| isd-pinning-fft | AGENT_HANDOFF |
| prange-restarts-opi | PRIME_CHARACTER_OPI; runnable `python tools/dqi_screen/screen.py`, entry `tools/dqi_screen/prange.py:prange_restarts` |
| lp-decoding-cycle-codes | TERNARY_PREFIX_INTEGRALITY; arXiv 2609.40036 |
| norm-search-fp2 | PRIME_CHARACTER_NORM_ATTACK |
| power-completion-rth-root | PRIME_CHARACTER_OPI |
| polar-sc-source-shaping | POLAR_CONDITIONAL_SAMPLER, POLAR_SOURCE_DESIGN |
| usd-prange-rejection-sampler | PARITY_BLOCK_USD_PRANGE; arXiv 2610.03566 |
| stochastic-localization-pspin | arXiv 2609.40250; AFFINE_CLUSTER_NATIVE_PROBE |
| tensor-network-simulation | QUANTUM_SIMULATION_TENSOR_NETWORK_BARRIER |
| belief-propagation-ldpc | DCP_SPARSE_PARITY_WITH_NOISE_LDPC_BELIEF_PROPAGATION_BRIDGE |
| lll-babai-dcp | DCP_BABAI_DEVIATION_DEPTH_BARRIER, DCP_BABAI_LATTICE_ROUNDING_WITNESS_OBSTRUCTION, TERNARY_FULL_RECORD_CVP |
| groebner-mq | TERNARY_QUOTIENT_DECODER, CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND |
| sdp-relaxation | QAOA_BOUNDED_DEPTH_OPTIMIZATION_BARRIER |
| index-calculus | ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER |

Produces: `CATALOG = Path(__file__).with_name("baselines.json")`, `load_catalog(path=CATALOG) -> list[dict]`, `validate_catalog(entries) -> list[str]` (duplicate id, missing field, mechanisms outside 3-6, malformed reference).
Tests: `test_catalog_is_well_formed` (`len == 14`, no problems); `test_catalog_note_references_exist` (real root, skip without a registry); `test_runnable_commands_point_at_existing_files` (skip with reason "Project 1 not merged" when `tools/dqi_screen/` is absent).
Commit: `git add tools/corpus/baselines.py tools/corpus/baselines.json tests/tools/test_corpus_baselines.py` — "Corpus: classical baseline catalog with validation".

### Task 5.2 — `recommend`
Produces: `@dataclass class Recommendation: baseline: dict; score: float; matched: list[str]; evidence: list[Hit]`; `recommend(corpus, idea, k=5, catalog=None) -> list[Recommendation]`. Formula: `tokens(t)` = `re.findall(r"[a-z0-9]+", t.lower())` with a trailing "s" stripped from words longer than three letters; a mechanism keyword matches when all its tokens are in `tokens(idea)`; `kw = matched / len(mechanisms)`; `hits = corpus.search(idea, kinds=("note", "negative"), k=10)`; a hit cites the baseline when `name` or any alias occurs (word-boundary, case-insensitive) in `doc.title + doc.text`; `corpus_part = citing / 10`; `score = round(kw + corpus_part, 4)`; return entries with `score > 0` sorted by `(-score, name)`, top k.
Tests: `test_prange_ranks_first_when_a_note_mentions_it` (a fake note "Prange information-set decoding already solves syndrome decoding of this random linear code." → `recs[0].baseline["id"] == "prange-isd"`, `"syndrome decoding" in matched`, evidence doc_id startswith `note:PRANGE_SYNDROME`); `test_recommend_scores_corpus_mentions_without_keyword_overlap` (`matched == []`, still returned).
Commit — "Corpus: recommend classical baselines from keywords and citing notes".

### Task 5.3 — CLI and MCP
Produces: `cmd_baselines(args)` for `baselines IDEA` (name, score, "why: matched ...; cited by ...", summary, references, `run:` command; `--json` → `{"idea", "recommendations": [{"baseline", "score", "matched", "evidence"}], **issues}`); MCP `classical_baselines(idea: str, k: int = 5) -> dict`; `_recommendation_json` beside `_hit_json`.
Tests: `test_cli_baselines_text_and_json`; the MCP tool-name assertion becomes the final six-name list; `test_classical_baselines_tool`.
Commit — "Corpus: baselines command and classical_baselines MCP tool".

### Task 5.4 — docs
README "Baselines" section (catalog location, schema, score formula, how to add an entry, the four stems to add back); map bullet. Run the full `pytest tests/tools`. Commit — "Corpus: document the baseline recommender".

## Project 2: note referee — `tools/referee/`

**Files**
- Create: `tools/referee/__init__.py`, `extract.py`, `referee.py`, `README.md`; `tests/tools/test_referee.py`
- Modify: `docs/REPOSITORY_MAP.md`
- Outputs: `research/audits/reviews/reviews.json`, `research/audits/reviews/<STEM>.md`, `research/audits/REFEREE_QUEUE.md`

Facts: `tools/corpus/sources/markdown.py` has `note_status(lines)` and the private `_sections(lines) -> list[(heading, line_no, body_lines)]` (preamble heading `""`); reuse both (`parse()` loses line structure). Only 283 notes are `review-pending` by `note_status`; two calibration notes say "require review" and classify `unlabelled`, so export accepts explicit `--note STEM`. A date sits in the status block of 75 notes; a producer command appears anywhere in 134 and the theorem source's `REPORT = "...json"` gives the artifact for 108 more; artifact paths come as `research/x/y.json` or `x/y.json`, so resolve `root/p` then `root/research/p`. `_sections` is fence-blind: filter fenced spans first.

### Task 2.1 — `parse_note`
Produces in `extract.py`: `NotePacket` dataclass `{stem, path, title, date, status, not_claimed: list[str], producer: dict | None, result: str, derivations: list[dict], controls: list[dict], self_check: str | None, decision: str | None, content_sha: str, flags: list[str]}`; `parse_note(path: Path) -> NotePacket`; `prose(text) -> str` (drops `#`/`|`/fence/4-space-indented lines, strips list markers); `to_dict(packet) -> dict`. Rules: status block = preamble up to the first blank line after the first non-empty line; `date` = first `20\d\d-\d\d-\d\d` in it; `not_claimed` = preamble sentences/bullets containing `\b(not|no)\b`; `producer` = first ``python (theorems/\w+\.py)([^`\n]*)`` anywhere (whole flag string kept), `artifact` = first `(?:research/)?[a-z_]+/[\w./-]+\.json` in the note, else `REPORT\s*=.*?["']([^"']+\.json)["']` from the theorem source if present under `root = path.parents[1]`; `result` = first section whose heading matches `Result|Question|Claim|Summary`, else the first section; `derivations` headings match `Derivation|Lemma|Proof|Bound|Certificate|^\d+\.`; `controls` match `Controls|Comparison|Classical`; `self_check` matches `Attempts To Prove It Wrong|Try To Kill|Falsifier|Kill`; `decision` matches `Decision|Next`; `content_sha` = sha256 of the bytes; `flags = [f.name for f in check_text(prose(result), title).flags]`.
Tests: `test_parse_note_reads_every_field` (fixture note with status block `2026-10-18. LOCAL APPLICATION REVIEW PENDING. No speedup is claimed. Not a new algorithm.`, a producer line with artifact, `## Question And Result`, `## 1. Lemma: Radial Bound`, `## Decisive Controls`, `## Try To Kill It`, `## Decision And Next`; assert `(stem, status, date) == ("FIXTURE_NOTE", "review-pending", "2026-10-18")`, the producer dict, both not-claimed strings, `"##" not in result`, the derivation heading, `"counterexample" in self_check`, the sha); `test_parse_note_falls_back_to_the_first_section_for_result`; `test_parse_note_reads_producer_from_the_reproduce_block_at_the_end`; `test_parse_note_keeps_fenced_headings_inside_their_section`; `test_parse_note_reads_replacement_bytes_and_long_producer_flags`.
Commit: `git add tools/referee/__init__.py tools/referee/extract.py tests/tools/test_referee.py` — "Referee: parse a review-pending note into a packet".

### Task 2.2 — `artifact_excerpt`
Produces: `artifact_excerpt(root, packet, max_chars=4000) -> str | None`; `_resolve_artifact(root, rel) -> Path | None`. Rendering: `keys: ...` line, depth-first sorted numeric leaves as `path = value` (ints/floats, not bools), strings ≤ 60 chars kept, lists capped at 5 with `... (+N)`, truncated at `max_chars` with `[truncated]`.
Tests: `test_artifact_excerpt_lists_keys_and_numeric_leaves` (`{"status": "ok", "mean": 0.9028, "tail": {"k110": 0.3145, "runs": [1..7]}}` → starts with `keys: mean, status, tail`, contains `mean = 0.9028` and `tail.k110 = 0.3145`, ≤ 5 list elements, length ≤ 4000); `test_artifact_excerpt_is_none_when_missing_or_invalid`.
Commit — "Referee: compact artifact excerpt for the judge".

### Task 2.3 — `select_notes`
Produces in `referee.py`: `REVIEWS = "research/audits/reviews/reviews.json"`; `load_reviews(root) -> dict`; `note_sha(path) -> str`; `select_notes(root, prefixes=(), limit=30, exclude_reviewed=True, reviews=None, statuses=("review-pending",)) -> list[Path]` over `research/*.md` minus `markdown.JOURNALS`, sorted by `(date or "0000", mtime)` descending; excludes notes whose current review has `content_sha == note_sha(path)`.
Test `test_select_notes_orders_by_status_date_then_mtime_and_skips_current_reviews` (dated 18 / dated 10 / undated-older + a superseded note → order and exclusion; a current-sha review excludes, a stale one keeps; `prefixes=("PRIME",)`; `limit`).
Commit — "Referee: select the newest review-pending notes".

### Task 2.4 — `export_batches`
Produces: `REFEREE_INSTRUCTIONS` (adversarial referee; for each note up to 6 claims, each a verbatim quote; per claim a verdict in `CLAIM_VERDICTS = ("holds", "gap", "wrong", "unclear")`, the step at fault, a counterexample or missing condition when gap/wrong, `covered_by_self_check`; overall in `OVERALL = ("sound", "needs-work", "unsound", "unclear")`; must not propose new research; quote from the note text only, never from the artifact excerpt); `build_packet(root, path) -> dict` (`to_dict(parse_note)` + `artifact_excerpt` + full `text`); `export_batches(root, out_dir, notes, batch_size=5) -> list[Path]` (`batch_NN.json = {"batch", "claim_verdicts", "overall_verdicts", "output_format", "notes"}`, newest first, no shuffle).
Test `test_export_writes_instructions_and_batches_with_artifact_excerpts` (6 notes → batches of 5 and 1; INSTRUCTIONS.md contains the eight verdict words, "verbatim", "must not propose"; the note with an artifact has an excerpt, others `None`).
Commit — "Referee: export judge batches".

### Task 2.5 — `import_reviews`
Produces: `import_reviews(root, paths, judge, today=None) -> dict` (rows via `rediscovery._rows`; `ValueError` on a bad claim or overall verdict, a quote under 6 words, or a quote not verbatim in the note (`_norm`); `content_sha` mismatch → stored with `stale: True`; re-import replaces the stem's entry; caps `summary[:1500]`, `finding[:600]`, `quote[:400]`, 6 claims; writes `reviews.json` `{"notes": {stem: {reviewed_on, judge, content_sha, overall, claims, summary, stale}}}` sorted).
Tests: `test_import_rejects_bad_verdicts_and_non_verbatim_quotes_and_marks_stale`; `test_import_rejects_a_quote_from_the_artifact_excerpt`.
Commit — "Referee: import and verify judge reviews".

### Task 2.6 — `render` and `status`
Produces: `WORST = {"wrong": 3, "gap": 2, "unclear": 1, "holds": 0}`; `worst_claim(entry) -> dict | None`; `is_stale(root, stem, entry) -> bool` (recomputes the sha now); `status(root) -> {"available", "reviewed", "flagged": [{stem, overall, reviewed_on, worst_claim}], "stale": [stems]}` (flagged = unsound/needs-work and not stale); `render(root, today=None) -> None` writing `reviews/<STEM>.md` (overall, each claim with quote, verdict, step, finding) and `REFEREE_QUEUE.md` (counts table `| unsound | n |`, flagged notes with worst claim, a "Stale" section, "Next 30" unreviewed).
Tests: `test_render_writes_a_note_review_and_the_queue`; `test_status_returns_only_flagged_non_stale_reviews` (unsound current → flagged; needs-work edited after import → in `stale`; sound → neither; no reviews file → `available False`).
Commit — "Referee: per-note reviews, queue and status".

### Task 2.7 — CLI, README, map
Produces: `main(argv) -> int` with subcommands `select | export | import | render | status`; options `--root`, `--prefix` (repeatable), `--limit`, `--note STEM` (repeatable, export only, bypasses the status filter), `--include-reviewed`, `--out-dir`, `--batch-size`, `--judge NAME`, `--json`.
Test `test_cli_round_trip` (select `--json` → list; export `--out-dir D --limit 2` → prints the instructions path; write a JSONL answer; import with `--judge test-judge`; render; status `--json` has `flagged`). README: purpose, the five commands, the judge loop, outputs, "never edits `research/*.md`", cost ≈ 100k tokens per batch of 5; map bullet.
Commit: `git add tools/referee/referee.py tools/referee/README.md docs/REPOSITORY_MAP.md tests/tools/test_referee.py` — "Referee: CLI, README and repository map entry".

### Task 2.8 — calibration pass (judging; ≈ 100k tokens)
- [ ] `python tools/referee/referee.py export --out-dir research/audits/reviews/calibration --note PRIME_CHARACTER_OPI --note PRIME_CHARACTER_NORM_ATTACK --note POLAR_SOURCE_DESIGN --note POLAR_CONDITIONAL_SAMPLER`.
- [ ] One fresh general-purpose subagent reads `INSTRUCTIONS.md` + `batch_01.json`, writes `out/batch_01.jsonl`; `import ... --judge claude-subagent-<date>`; `render`.
- [ ] Compare with `docs/papers/classical-competitors/README.md` "Review history" (the N=31,K=16 input stopping at 30/31; the fixed-input guarantee stated too broadly; the polar certificate's two review-pending premises; the syndrome conditioning in Result C) and record a table (prior finding → note → found: yes/no/partly) in `tools/referee/README.md` under "Calibration".
- [ ] Commit `tools/referee/README.md research/audits/reviews research/audits/REFEREE_QUEUE.md` — "Referee: calibration against the preprint's review history".

### Task 2.9 — first pass (judging; ≈ 600k tokens)
- [ ] `export --out-dir research/audits/reviews/pass1 --limit 30` (6 batches of 5); six fresh subagents in parallel; `import`; `render`.
- [ ] Read `REFEREE_QUEUE.md`; spot-check two "unsound" claims by hand before committing.
- [ ] Commit the reviews — "Referee: first pass over the 30 newest review-pending notes".

---

# Phase 3

## Project 3: agent brief — `tools/brief/`

**Files**
- Create: `tools/brief/__init__.py`, `build_brief.py`, `README.md`; `tests/tools/test_brief.py`
- Modify: `docs/REPOSITORY_MAP.md`
- Outputs: `research/audits/AGENT_BRIEF.md`, `research/audits/agent_brief.json`

Fact: the cockpit's `allowed_git_args` permits `show <sha>:research/registry/negative_results.json` but no `log --before`, so the brief has its own tiny allow-listed runner in the cockpit's style. Every section returns `{"available": bool, ...}` and is wrapped by `_section(name, fn, *args)` that turns any exception into `{"available": False, "reason": "ExcType: msg"}`.

### Task 3.1 — git runner and `registry_delta`
Produces: `REGISTRY`, `allowed_git_args(args) -> bool` accepting exactly `("log", "-1", "--before=YYYY-MM-DD", "--format=%H<US>%ct")` and `("show", "<40-hex>:" + REGISTRY)`; `git_runner(root)`; `since_commit(root, since_days=7, today=None, git=None) -> tuple[str, str] | None`; `registry_delta(root, since_sha, git=None) -> {available, added, removed, since_sha, since_date, baseline_count, current_count}`; `_ids(data) -> set[str]` tolerant of a list or `{"records": [...]}`.
Tests (real temp git repo with `GIT_COMMITTER_DATE`): `test_registry_delta_lists_added_and_removed_ids_since_the_cutoff` (commits on 2026-10-01 `[A]` and 2026-10-15 `[A, B]`, working copy `[B, C]`, today 2026-10-20, since 7 days → cutoff day 2026-10-01, `added == ["B", "C"]`, `removed == ["A"]`); `test_registry_delta_is_unavailable_outside_git`; `test_registry_delta_reports_a_missing_registry_at_the_cutoff`; parametrized `test_git_runner_refuses_other_argument_shapes`.
Commit: `git add tools/brief/__init__.py tools/brief/build_brief.py tests/tools/test_brief.py` — "Brief: registry delta from git history".

### Task 3.2 — the other sections
Produces: `arxiv_section(root, since_date) -> {available, flagged: [{id, title, label, first_seen, verdict}], reviewed: [{id, verdict, by, reviewed_on}], actions: [{id, action, by}]}` (actions = verdicts with a non-empty `action` and no truthy `action_done`; tolerate verdicts for unknown papers and null `first_seen`); `referee_section(root)` via `tools.referee.referee.status`; `preflight_section(root) -> {available, by_check, total}` via `tools.preflight.preflight.run` imported lazily (ImportError → unavailable "tools/preflight not present"); `inertia_section(root)` from `site/data/cockpit.json` (`inertia.flags`, `warnings`); `duplicates_section(root, added_ids, corpus=None)` via a module-level `_near_duplicates()` indirection, building `Corpus(root)` only when `added_ids` is non-empty, keeping pairs where `a` or `b` (or the part after the last `:`) is in `added_ids`; `commands_section()` (five static entries: oracle, screener, baselines, preflight, duplicates).
Tests: one happy-path test per section with written fixture files or monkeypatched callables, and one `_missing` test per section asserting `available is False` and a `reason`; `test_arxiv_section_tolerates_verdicts_for_unknown_papers_and_null_first_seen`.
Commit — "Brief: arXiv, referee, preflight, inertia, duplicate and command sections".

### Task 3.3 — `build`, `render`, `main`, README, map
Produces: `build(root, since_days=7, today=None, git=None) -> dict` (`generated_on, since_days, registry, arxiv, referee, preflight, inertia, duplicates, commands`); `render(brief) -> str` with fixed headings `## Registry`, `## arXiv watch`, `## Referee`, `## Preflight`, `## Inertia`, `## Possible duplicates`, `## Commands`, unavailable sections printing "Not available: <reason>"; `write(root, brief, out=None)`; `main(argv) -> int` with `--root --since-days --out --json`.
Tests: `test_build_never_fails_when_every_source_is_missing`; `test_render_contains_every_section_heading_and_action_strings`; `test_main_writes_both_files`.
README: build command, the one line for the agents' prompts ("Read research/audits/AGENT_BRIEF.md before choosing a direction"), what each section reads, the degradation rule; map bullet. Two commits: "Brief: build and render the agent brief", then (after running it on the real checkout) "Brief: first generated AGENT_BRIEF.md".

---

# Phase 4: review and merge

- [ ] One adversarial reviewer subagent per project (seven, in parallel), each given the project's README, tests and source, asked for concrete failures with reproduction commands; fix every confirmed finding test-first; commit per project.
- [ ] `python -m pytest -q tests/tools`; `python tools/preflight/preflight.py` (expect only the broken contract); `python tools/brief/build_brief.py` regenerated last.
- [ ] Merge to main through the merge-main session (`git merge --no-ff refs/heads/worktree-corpus-substrate`; stop on any conflict with uncommitted agent edits) and push only when the user says so.

## Review Focus

Inputs no task's tests exercise yet that are most likely to bite a real user; each has its test named in the owning task above:

1. `prange_restarts` with q > 2³¹: int64 overflow would silently corrupt scores (Task 1.5, `test_prange_large_prime_field`).
2. A count-objective candidate with λ > 1−ρ: Q_DQI saturates at 1 and the restart length collapses, reading as "viable" (Task 1.3, `test_saturated_reach_is_flagged_not_viable`).
3. Preflight run without git or from a relative `--root`: every module would be reported, or `relative_to` would raise (Tasks 4.1/4.2).
4. The first weekly watch run after seeding rewrites 22 records and opens a PR with no new papers (Task 6.2 test with an unchanged client; README note).
5. A judge quote that crosses a note chunk boundary or is lifted from the artifact excerpt passes `_norm` but is not evidence (Tasks 6.7, 2.5).
6. Sweep-sibling negatives (identical text, ids differing in a trailing number) crowd true restatements out of the top 200 (Task 7.1, `per_family`).
7. `since_commit` on a shallow clone or when the registry did not exist at the cutoff must say unavailable, not "no change" (Task 3.1).

## Verification (whole portfolio)

- `python -m pytest -q tests/tools` green after every task; `tests/tools/test_corpus_mcp.py` tool list equals the final six names.
- Real-checkout smoke runs, each committed in its README: `python tools/dqi_screen/screen.py --params tools/dqi_screen/examples/opi_prime_character_r32.json` exits 1 with "outside licensed Hamming reach"; `python tools/preflight/preflight.py` prints exactly the broken-contract line; `python tools/arxiv_watch/watch.py --relabel` keeps all 22 verdicts and the digest shows a Reviewed table; `python tools/corpus/cli.py check-new --text "<a claim copied from the registry>"` exits 2; `python tools/corpus/cli.py baselines "sampling the Gibbs law of a signed parity-check code"` lists polar-sc-source-shaping and usd-prange-rejection-sampler; `REFEREE_QUEUE.md` lists 34 reviewed notes; `AGENT_BRIEF.md` has all seven sections populated.
- `git status` before each commit shows changes only under the project's own paths plus the shared allowances (`docs/REPOSITORY_MAP.md`, `tools/corpus/{cli,mcp_server,api,README}`, `tests/tools/test_corpus_mcp.py`, `research/audits/`).
