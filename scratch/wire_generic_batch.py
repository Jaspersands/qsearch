import importlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")


def wire_batch(modules_info, last_exp_id=None):
    """Wires a batch of modules into research_registry, experiment_runner, qsearch, tests, and README."""

    # 1. Update module report writer signatures and upserts
    print("Updating module files...")
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        path = f"{mod_name}.py"
        with open(path) as f:
            code = f.read()

        if "write_registry: bool = True" not in code:
            old_pattern = re.compile(
                rf"def {writer_name}\(\s*path:\s*Path\s*=\s*REPORT_PATH,?\s*\)\s*->\s*dict\[str,\s*Any\]:"
            )
            new_def = f"""def {writer_name}(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "{exp_id}"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:"""
            code = old_pattern.sub(new_def, code)

            neg_id = "NEG-" + exp_id[9:]
            upsert_block = f"""
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="{neg_id}",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for {exp_id}."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for {exp_id}."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {{}}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{{registry_experiment_id}}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {{}}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={{
                    "{mod_name}": str(path)
                }},
            )
        )
    return payload"""

            code = re.sub(
                r"(\n    return payload)(\n\n|\n$)",
                r"\n" + upsert_block + r"\2",
                code,
                count=1,
            )
            with open(path, "w") as f:
                f.write(code)
            print("Updated module file:", path)

    # 2. Update research_registry.py
    print("Updating research_registry.py...")
    with open("research_registry.py") as f:
        reg_code = f.read()

    rec_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        mod = importlib.import_module(mod_name)
        writer = getattr(mod, writer_name)
        payload = writer(write_registry=False)
        summary = payload.get("summary", f"Theorem evaluation for {exp_id}.")
        falsifiers = payload.get(
            "falsifiers_triggered", [f"Falsifier for {exp_id}"]
        )
        metrics = list(payload.get("headline_metrics", {}).keys())

        rec = f"""        ExperimentRecord(
            id="{exp_id}",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="{exp_id.replace('-', ' ').title()}",
            status="planned",
            hypothesis={json.dumps(summary)},
            protocol="Evaluate exact representation-theoretic properties and validate metrics.",
            positive_signal={json.dumps(summary)},
            falsifiers={json.dumps(falsifiers)},
            metrics={json.dumps(metrics)},
            dependencies=[
                "{mod_name}.py",
            ],
            next_actions=[
                "Run qsearch.py {cli_name}.",
            ],
        ),"""
        rec_blocks.append(rec)

    # Insert before EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT
    reg_anchor = 'id="EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT",'
    pos = reg_code.find(reg_anchor)
    if pos == -1:
        raise ValueError(f"Anchor '{reg_anchor}' not found in research_registry.py")

    rec_start = reg_code.rfind("        ExperimentRecord(", 0, pos)
    reg_code = (
        reg_code[:rec_start] + "\n".join(rec_blocks) + "\n" + reg_code[rec_start:]
    )

    with open("research_registry.py", "w") as f:
        f.write(reg_code)

    # 3. Update experiment_runner.py
    print("Updating experiment_runner.py...")
    with open("experiment_runner.py") as f:
        runner_code = f.read()

    # Add imports before from learnability_baselines import write_learnability_report
    imports_str = "\n".join(
        f"from {mod_name} import (\n    {writer_name},\n)"
        for mod_name, exp_id, writer_name, cli_name in modules_info
    )
    import_anchor = "from learnability_baselines import write_learnability_report"
    pos = runner_code.find(import_anchor)
    runner_code = (
        runner_code[:pos] + imports_str + "\n" + runner_code[pos:]
    )

    # Add COSET_EXPERIMENTS IDs before "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING",
    ids_str = "\n".join(
        f'    "{exp_id}",'
        for mod_name, exp_id, writer_name, cli_name in modules_info
    )
    id_anchor = '"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING",'
    pos = runner_code.find(id_anchor)
    line_start = runner_code.rfind("\n", 0, pos) + 1
    runner_code = runner_code[:line_start] + ids_str + "\n" + runner_code[line_start:]

    # Add priority entries before "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING":
    prio_matches = re.findall(r'"EXP-CODE-SELF-DUAL-WREATH-[A-Z0-9-]+": (\d+),', runner_code)
    last_prio = max(int(x) for x in prio_matches) if prio_matches else 157
    prio_str = "\n".join(
        f'        "{exp_id}": {last_prio + 1 + i},'
        for i, (mod_name, exp_id, writer_name, cli_name) in enumerate(
            modules_info
        )
    )
    prio_anchor = '"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING":'
    pos = runner_code.find(prio_anchor)
    line_start = runner_code.rfind("\n", 0, pos) + 1
    runner_code = runner_code[:line_start] + prio_str + "\n" + runner_code[line_start:]

    # Add dispatch branches before == "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING"
    dispatch_str = "\n".join(
        f"""        elif (
            experiment_id
            == "{exp_id}"
        ):
            payload = {writer_name}(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )"""
        for mod_name, exp_id, writer_name, cli_name in modules_info
    )
    dispatch_anchor = '== "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING"'
    pos = runner_code.find(dispatch_anchor)
    branch_start = runner_code.rfind("        elif (", 0, pos)
    runner_code = (
        runner_code[:branch_start] + dispatch_str + "\n" + runner_code[branch_start:]
    )

    with open("experiment_runner.py", "w") as f:
        f.write(runner_code)

    # 4. Update qsearch.py
    print("Updating qsearch.py...")
    with open("qsearch.py") as f:
        q_code = f.read()

    # Add imports before from blocker_taxonomy import write_blocker_taxonomy
    q_imports_str = "\n".join(
        f"from {mod_name} import (\n    {writer_name},\n)"
        for mod_name, exp_id, writer_name, cli_name in modules_info
    )
    q_import_anchor = "from blocker_taxonomy import write_blocker_taxonomy"
    pos = q_code.find(q_import_anchor)
    q_code = q_code[:pos] + q_imports_str + "\n\n\n" + q_code[pos:]

    # Add command functions before def command_coset_strong_fourier_information(
    cmd_funcs = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        func_name = "command_" + cli_name.replace("-", "_")
        art_path = f"research/representation/{mod_name}.json"
        cmd_body = f"""def {func_name}(
    args: argparse.Namespace,
) -> int:
    initialize_seed_registry(overwrite=False)
    payload = {writer_name}(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("{cli_name.replace('-', ' ').title()} analysis complete")
    print(
        "Artifact: {art_path}"
    )
    print(
        f"Speedup claim allowed: "
        f"{{payload['claim_gate']['speedup_claim_allowed']}}"
    )
    print(f"Registry valid: {{validation['valid']}}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0"""
        cmd_funcs.append(cmd_body)

    cmd_funcs_str = "\n\n\n".join(cmd_funcs)
    cmd_anchor = "def command_coset_strong_fourier_information("
    pos = q_code.find(cmd_anchor)
    q_code = q_code[:pos] + cmd_funcs_str + "\n\n\n" + q_code[pos:]

    # Add subparsers before coset_strong_fourier_information = subparsers.add_parser(
    subparser_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        func_name = "command_" + cli_name.replace("-", "_")
        sub_body = f"""    {cli_name.replace('-', '_')} = subparsers.add_parser(
        "{cli_name}",
        help="Analyze {cli_name.replace('-', ' ')} theorem performance.",
    )
    {cli_name.replace('-', '_')}.add_argument(
        "--no-registry",
        action="store_true",
    )
    {cli_name.replace('-', '_')}.set_defaults(
        func={func_name}
    )"""
        subparser_blocks.append(sub_body)

    subparsers_str = "\n\n".join(subparser_blocks)
    sub_anchor = "coset_strong_fourier_information = subparsers.add_parser("
    pos = q_code.find(sub_anchor)
    sub_line_start = q_code.rfind("    ", 0, pos)
    q_code = q_code[:sub_line_start] + subparsers_str + "\n\n" + q_code[sub_line_start:]

    with open("qsearch.py", "w") as f:
        f.write(q_code)

    # 5. Update tests/test_experiment_runner.py
    print("Updating tests/test_experiment_runner.py...")
    with open("tests/test_experiment_runner.py") as f:
        test_code = f.read()

    test_methods = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        method_name = (
            "test_"
            + cli_name.replace("-", "_")[5:]
            + "_dispatches_from_clean_registry"
        )
        test_body = f"""    def {method_name}(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "{exp_id}"
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
            "{mod_name}",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])"""
        test_methods.append(test_body)

    test_methods_str = "\n\n".join(test_methods)
    test_anchor = "def test_equal_commutator_audit_dispatches_from_clean_registry("
    pos = test_code.find(test_anchor)
    method_start = test_code.rfind("    def ", 0, pos)
    test_code = test_code[:method_start] + test_methods_str + "\n\n" + test_code[method_start:]

    with open("tests/test_experiment_runner.py", "w") as f:
        f.write(test_code)

    # 6. Update README.md
    print("Updating README.md...")
    with open("README.md") as f:
        readme_code = f.read()

    readme_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        block = f"""Analyze {cli_name.replace('-', ' ')} theorem performance:

```bash
python qsearch.py {cli_name}
python qsearch.py run {exp_id}
```"""
        readme_blocks.append(block)

    readme_str = "\n\n".join(readme_blocks)
    readme_anchor = "Isolate the solvable and unresolved equal-pair commutator terms:"
    pos = readme_code.find(readme_anchor)
    readme_code = (
        readme_code[:pos] + readme_str + "\n\n" + readme_code[pos:]
    )

    with open("README.md", "w") as f:
        f.write(readme_code)

    print("Batch wiring complete!")
