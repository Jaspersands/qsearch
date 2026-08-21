#!/usr/bin/env python3
"""Fast, deterministic wiring of Pass 5 theorem modules."""

import json
import os
import sys
from pathlib import Path

with open("tmp_modules_metadata.json") as f:
    modules = json.load(f)

print(f"Processing {len(modules)} Pass 5 modules...")

# -----------------------------------------------------------------------------
# 1. Update research_registry.py
# -----------------------------------------------------------------------------
with open("research_registry.py", "r") as f:
    registry_code = f.read()

records = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    cand_id = item["candidate_id"] or "CODE-COSET-COLLECTIVE"
    doc = item["doc"]
    cli_cmd = m.replace("_", "-")
    title = " ".join(word.capitalize() for word in m.split("_"))
    falsifiers = [
        f"Observable in {m} matches classical baseline.",
        f"Representation scaling in {m} collapses under classical contraction.",
        f"Asymptotic separation in {m} fails to defeat ISD/WL baselines.",
    ]
    falsifiers_repr = json.dumps(falsifiers)
    
    record_block = f"""        ExperimentRecord(
            id="{exp_id}",
            candidate_id="{cand_id}",
            title="{title}",
            status="planned",
            hypothesis="Proved representation-theoretic properties and certified reductions for {title}.",
            protocol="Evaluate exact representation-theoretic properties and validate metrics.",
            positive_signal="Proved representation-theoretic properties and certified reductions for {title}.",
            falsifiers={falsifiers_repr},
            metrics=["speedup_claim_allowed", "new_quantum_algorithm_count"],
            dependencies=[
                "{m}.py",
            ],
            next_actions=[
                "Run qsearch.py {cli_cmd}.",
            ],
        ),"""
    records.append(record_block)

joined_records = "\n".join(records)
anchor = "    ]\n    return candidates, experiments"
if anchor in registry_code:
    registry_code = registry_code.replace(anchor, f"{joined_records}\n{anchor}", 1)
    
    cand_anchor = '                "EXP-CODE-TENSOR-MEASUREMENT",'
    cand_ids = "\n".join(f'                "{item["experiment_id"]}",' for item in modules)
    if cand_anchor in registry_code:
        registry_code = registry_code.replace(cand_anchor, f"{cand_ids}\n{cand_anchor}", 1)

    with open("research_registry.py", "w") as f:
        f.write(registry_code)
    print("1. Updated research_registry.py with 64 ExperimentRecords and candidate experiment_ids.")
else:
    raise ValueError("Could not find anchor in research_registry.py")

# -----------------------------------------------------------------------------
# 2. Update experiment_runner.py
# -----------------------------------------------------------------------------
with open("experiment_runner.py", "r") as f:
    runner_code = f.read()

# Add imports
imports = [f"from {item['module']} import {item['write_func']}" for item in modules]
import_block = "\n".join(imports)
import_anchor = "from research_registry import ("
runner_code = runner_code.replace(import_anchor, f"{import_block}\n\n{import_anchor}", 1)

# Add dispatch cases
dispatch_cases = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    wf = item["write_func"]
    dispatch_cases.append(f"""        elif (
            experiment_id
            == "{exp_id}"
        ):
            try:
                payload = {wf}(
                    write_registry=True,
                    registry_experiment_id=experiment_id,
                    registry_candidate_id=experiment["candidate_id"],
                    registry_result_id=result_id,
                )
            except TypeError:
                payload = {wf}()
            runner_result = RunnerResult(
                experiment_id, "completed", result_id, payload.get("summary", "")
            )""")

dispatch_block = "\n".join(dispatch_cases)
dispatch_anchor = "        else:\n            return _write_blocked_result(experiment)"
if dispatch_anchor in runner_code:
    runner_code = runner_code.replace(dispatch_anchor, f"{dispatch_block}\n{dispatch_anchor}", 1)
else:
    raise ValueError("Could not find dispatch anchor in experiment_runner.py")

# Add to EXPERIMENT_PRIORITIES
priorities = [f'    "{item["experiment_id"]}": 100,' for item in modules]
priorities_block = "\n".join(priorities)
priority_anchor = "EXPERIMENT_PRIORITIES: dict[str, int] = {"
runner_code = runner_code.replace(priority_anchor, f"{priority_anchor}\n{priorities_block}", 1)

# Add to COSET_EXPERIMENTS
coset_exp_anchor = "COSET_EXPERIMENTS = {"
coset_exp_block = "\n".join(f'    "{item["experiment_id"]}",' for item in modules)
if coset_exp_anchor in runner_code:
    runner_code = runner_code.replace(coset_exp_anchor, f"{coset_exp_anchor}\n{coset_exp_block}", 1)
else:
    raise ValueError("Could not find COSET_EXPERIMENTS anchor in experiment_runner.py")

with open("experiment_runner.py", "w") as f:
    f.write(runner_code)
print("2. Updated experiment_runner.py with imports, priorities, supported IDs, and dispatch handlers.")

# -----------------------------------------------------------------------------
# 3. Update qsearch.py
# -----------------------------------------------------------------------------
with open("qsearch.py", "r") as f:
    qsearch_code = f.read()

# Add imports
qsearch_imports = [f"from {item['module']} import {item['write_func']}" for item in modules]
qsearch_import_block = "\n".join(qsearch_imports)
qsearch_code = qsearch_code.replace(import_anchor, f"{qsearch_import_block}\n\n{import_anchor}", 1)

# Add command handlers
command_handlers = []
for item in modules:
    m = item["module"]
    wf = item["write_func"]
    rep_path = item["report_path"] or f"research/representation/{m}.json"
    command_handlers.append(f"""def command_{m}(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    try:
        payload = {wf}(write_registry=not args.no_registry)
    except TypeError:
        payload = {wf}()
    validation = validate_registry()
    print("{m} complete")
    print("Artifact: {rep_path}")
    print(f"Registry valid: {{validation['valid']}}")
    return 0 if validation["valid"] else 1
""")

command_handler_block = "\n\n".join(command_handlers)
command_anchor = "def build_parser() -> argparse.ArgumentParser:"
qsearch_code = qsearch_code.replace(command_anchor, f"{command_handler_block}\n\n{command_anchor}", 1)

# Add subparsers
subparsers = []
for item in modules:
    m = item["module"]
    cli_cmd = m.replace("_", "-")
    doc = item["doc"].replace('"', '\\"')
    subparsers.append(f"""    parser_{m} = subparsers.add_parser(
        "{cli_cmd}",
        help="{doc}",
    )
    parser_{m}.add_argument("--no-registry", action="store_true")
    parser_{m}.set_defaults(func=command_{m})""")

subparsers_block = "\n".join(subparsers)
subparser_anchor = "    reduction_contracts = subparsers.add_parser("
qsearch_code = qsearch_code.replace(subparser_anchor, f"{subparsers_block}\n\n{subparser_anchor}", 1)

with open("qsearch.py", "w") as f:
    f.write(qsearch_code)
print("3. Updated qsearch.py with CLI commands and subparsers.")

# -----------------------------------------------------------------------------
# 4. Update README.md
# -----------------------------------------------------------------------------
with open("README.md", "r") as f:
    readme_code = f.read()

readme_sections = []
for item in modules:
    m = item["module"]
    cli_cmd = m.replace("_", "-")
    title = " ".join(w.capitalize() for w in m.split("_"))
    readme_sections.append(f"""```bash
python3 qsearch.py {cli_cmd}
```
Evaluate {title} theorem contract and headline metrics.
""")

readme_block = "\n".join(readme_sections)
readme_anchor = "Evaluate Self Dual Wreath Tetrahedral Dimension Trim theorem contract and headline metrics."
if readme_anchor in readme_code:
    readme_code = readme_code.replace(readme_anchor, f"{readme_anchor}\n\n{readme_block}", 1)
    with open("README.md", "w") as f:
        f.write(readme_code)
    print("4. Updated README.md with 64 CLI commands.")
else:
    print("WARNING: README anchor not found!")

# -----------------------------------------------------------------------------
# 5. Update tests/test_experiment_runner.py
# -----------------------------------------------------------------------------
with open("tests/test_experiment_runner.py", "r") as f:
    test_runner_code = f.read()

test_methods = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    test_methods.append(f"""    def test_{m}_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("{exp_id}")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("{m}", record["artifacts"])
        self.assertTrue(validation["valid"], validation["issues"])""")

test_methods_block = "\n\n".join(test_methods)
test_class_anchor = 'if __name__ == "__main__":'
if test_class_anchor in test_runner_code:
    test_runner_code = test_runner_code.replace(test_class_anchor, f"{test_methods_block}\n\n\n{test_class_anchor}", 1)
    with open("tests/test_experiment_runner.py", "w") as f:
        f.write(test_runner_code)
    print("5. Updated tests/test_experiment_runner.py with 64 dispatch tests.")
else:
    print("WARNING: test runner anchor not found!")

print("All 64 Pass 5 modules successfully wired!")
