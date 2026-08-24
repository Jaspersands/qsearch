#!/usr/bin/env python3
"""Wire Pass 6 theorem modules cleanly into research registry, experiment runner, CLI, README, and tests."""

import json
import os
import sys
from pathlib import Path

with open("tmp_unwired_pass6.json") as f:
    modules = json.load(f)

print(f"Processing {len(modules)} Pass 6 modules...")

# -----------------------------------------------------------------------------
# 1. Update core/research_registry.py
# -----------------------------------------------------------------------------
with open("core/research_registry.py", "r") as f:
    registry_code = f.read()

records = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    cand_id = "CODE-COSET-COLLECTIVE"
    doc = item["doc"]
    cli_cmd = item["cli_cmd"]
    title = " ".join(word.capitalize() for word in m.split("_"))
    falsifiers = [
        f"Observable in {m} matches classical baseline.",
        f"Representation scaling in {m} collapses under classical contraction.",
        f"Asymptotic separation in {m} fails to defeat ISD/WL baselines.",
    ]
    falsifiers_repr = json.dumps(falsifiers)
    
    if f'"{exp_id}"' not in registry_code:
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

if records:
    joined_records = "\n".join(records)
    anchor = "    ]\n    return candidates, experiments"
    if anchor in registry_code:
        registry_code = registry_code.replace(anchor, f"{joined_records}\n{anchor}", 1)
        
        cand_anchor = '                "EXP-CODE-TENSOR-MEASUREMENT",'
        cand_ids = "\n".join(f'                "{item["experiment_id"]}",' for item in modules if f'"{item["experiment_id"]}"' not in registry_code[:registry_code.find(cand_anchor)])
        if cand_anchor in registry_code and cand_ids:
            registry_code = registry_code.replace(cand_anchor, f"{cand_ids}\n{cand_anchor}", 1)

        with open("core/research_registry.py", "w") as f:
            f.write(registry_code)
        print(f"1. Updated core/research_registry.py with {len(records)} ExperimentRecords and candidate experiment_ids.")
    else:
        raise ValueError("Could not find anchor in core/research_registry.py")
else:
    print("1. core/research_registry.py already has all records.")

# -----------------------------------------------------------------------------
# 2. Update core/experiment_runner.py
# -----------------------------------------------------------------------------
with open("core/experiment_runner.py", "r") as f:
    runner_code = f.read()

# Add imports
imports = [f"from {item['module']} import {item['write_func']}" for item in modules if f"from {item['module']}" not in runner_code]
if imports:
    import_block = "\n".join(imports)
    import_anchor = "from research_registry import ("
    runner_code = runner_code.replace(import_anchor, f"{import_block}\n\n{import_anchor}", 1)

# Add _latest_result_id_for_experiment fallback mapping
wreath_fallback_anchor = '    return f"RESULT-{experiment_id}-BLOCKED"'
wreath_fallback = """    if experiment_id.startswith("EXP-CODE-SELF-DUAL-WREATH-"):
        return f"RESULT-{experiment_id}"
"""
if wreath_fallback.strip() not in runner_code:
    runner_code = runner_code.replace(wreath_fallback_anchor, f"{wreath_fallback}{wreath_fallback_anchor}", 1)

# Add dispatch cases right before the final `else:\n            return _write_blocked_result(experiment)`
dispatch_cases = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    wf = item["write_func"]
    if f'"{exp_id}"' not in runner_code:
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

if dispatch_cases:
    joined_dispatch = "\n".join(dispatch_cases)
    final_else = "        else:\n            return _write_blocked_result(experiment)"
    if final_else in runner_code:
        runner_code = runner_code.replace(final_else, f"{joined_dispatch}\n{final_else}", 1)
    else:
        raise ValueError("Could not find final else in core/experiment_runner.py")

# Add to supported_experiment_ids
supported_ids = "\n".join(f'        | {{"{item["experiment_id"]}"}}' for item in modules if f'| {{"{item["experiment_id"]}"}}' not in runner_code)
if supported_ids:
    supported_anchor = '        | DCP_RECURSIVE_DECODER_EXPERIMENTS'
    runner_code = runner_code.replace(supported_anchor, f"{supported_ids}\n{supported_anchor}", 1)

with open("core/experiment_runner.py", "w") as f:
    f.write(runner_code)
print(f"2. Updated core/experiment_runner.py with imports, result IDs, dispatchers, and supported experiment sets.")

# -----------------------------------------------------------------------------
# 3. Update qsearch.py
# -----------------------------------------------------------------------------
with open("qsearch.py", "r") as f:
    qsearch_code = f.read()

# Add imports to qsearch.py
q_imports = [f"from {item['module']} import {item['write_func']}" for item in modules if f"from {item['module']}" not in qsearch_code]
if q_imports:
    q_import_block = "\n".join(q_imports)
    q_import_anchor = "import argparse"
    qsearch_code = qsearch_code.replace(q_import_anchor, f"{q_import_block}\n\n{q_import_anchor}", 1)

# Add command handlers
command_handlers = []
for item in modules:
    m = item["module"]
    wf = item["write_func"]
    func_name = f"command_{m.replace('self_dual_wreath_', 'sdw_')}"
    item["cli_func_name"] = func_name
    if f"def {func_name}(" not in qsearch_code:
        command_handlers.append(f"""
def {func_name}(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    try:
        payload = {wf}(write_registry=not args.no_registry)
    except TypeError:
        payload = {wf}()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {{}})
    print("{m} complete")
    print(f"Speedup claim allowed: {{payload.get('claim_gate', {{}}).get('speedup_claim_allowed', False)}}")
    print(f"Registry valid: {{validation['valid']}}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0
""")

if command_handlers:
    joined_handlers = "\n".join(command_handlers)
    handler_anchor = "def command_audit(args: argparse.Namespace) -> int:"
    qsearch_code = qsearch_code.replace(handler_anchor, f"{joined_handlers}\n\n{handler_anchor}", 1)

# Add subparsers
subparsers_entries = []
for item in modules:
    cli_cmd = item["cli_cmd"]
    func_name = item["cli_func_name"]
    doc = item["doc"]
    if f'"{cli_cmd}"' not in qsearch_code:
        subparsers_entries.append(f"""    p_{item['module'][:25]} = subparsers.add_parser(
        "{cli_cmd}",
        help="{doc.replace('\"', '')}",
    )
    p_{item['module'][:25]}.add_argument("--no-registry", action="store_true")
    p_{item['module'][:25]}.set_defaults(func={func_name})
""")

if subparsers_entries:
    joined_subparsers = "\n".join(subparsers_entries)
    subparser_anchor = '    subparsers = parser.add_subparsers(dest="command")'
    qsearch_code = qsearch_code.replace(subparser_anchor, f"{subparser_anchor}\n{joined_subparsers}", 1)

with open("qsearch.py", "w") as f:
    f.write(qsearch_code)
print(f"3. Updated qsearch.py with CLI imports, command handlers, and subparsers.")

# -----------------------------------------------------------------------------
# 4. Update tests/test_experiment_runner.py
# -----------------------------------------------------------------------------
with open("tests/test_experiment_runner.py", "r") as f:
    test_code = f.read()

test_cases = []
for item in modules:
    m = item["module"]
    exp_id = item["experiment_id"]
    if f"def test_{m}_dispatches_from_clean_registry(" not in test_code:
        test_cases.append(f"""    def test_{m}_dispatches_from_clean_registry(self):
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
        self.assertTrue(validation["valid"], validation["issues"])
""")

if test_cases:
    joined_tests = "\n".join(test_cases)
    test_anchor = 'if __name__ == "__main__":'
    test_code = test_code.replace(test_anchor, f"{joined_tests}\n\n{test_anchor}", 1)

    with open("tests/test_experiment_runner.py", "w") as f:
        f.write(test_code)
    print(f"4. Updated tests/test_experiment_runner.py with {len(test_cases)} dispatch unit tests.")
else:
    print("4. tests/test_experiment_runner.py already has all tests.")

print("All Pass 6 wiring complete!")
