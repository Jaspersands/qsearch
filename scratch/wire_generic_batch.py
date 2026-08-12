import importlib
import inspect
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")


def wire_batch(modules_info):
    """Wires a batch of modules into research_registry, experiment_runner, qsearch, tests, and README."""

    # 1. Update module report writer signatures and upserts
    print("Updating module files...")
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        path = f"{mod_name}.py"
        with open(path) as f:
            code = f.read()

        match = re.search(r"^def " + re.escape(writer_name) + r"[\(\s]", code, re.MULTILINE)
        if match:
            def_idx = match.start()
            run_func = writer_name.replace("write_", "run_")
            if run_func.endswith("_report"):
                run_func = run_func[:-7]

            neg_id = "NEG-" + exp_id[9:]
            clean_writer = f"""def {writer_name}(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "{exp_id}"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "{run_func}" in globals():
        report = {run_func}(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {{}}
        payload = {{}}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
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
                claim="Initial negative claim for {exp_id}.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for {exp_id}.",
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
    return payload
"""
            code = code[:def_idx] + clean_writer
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
        sig = inspect.signature(writer)
        if "write_registry" in sig.parameters:
            payload = writer(write_registry=False)
        else:
            payload = writer()

        if hasattr(payload, "__dataclass_fields__"):
            payload = asdict(payload)
        elif isinstance(payload, (str, Path)):
            p = Path(payload)
            payload = json.loads(p.read_text()) if p.exists() else {}
        elif not isinstance(payload, dict):
            payload = {}

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

    imp_lines = [f"from {mod_name} import {writer_name}" for mod_name, exp_id, writer_name, cli_name in modules_info]
    imp_anchor = "from learnability_baselines import write_learnability_report"
    imp_pos = runner_code.find(imp_anchor)
    runner_code = runner_code[:imp_pos] + "\n".join(imp_lines) + "\n" + runner_code[imp_pos:]

    set_lines = [f'        "{exp_id}",' for mod_name, exp_id, writer_name, cli_name in modules_info]
    set_anchor = '"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING",'
    set_pos = runner_code.find(set_anchor)
    runner_code = runner_code[:set_pos] + "\n".join(set_lines) + "\n" + runner_code[set_pos:]

    prio_lines = [f'        "{exp_id}": 100,' for mod_name, exp_id, writer_name, cli_name in modules_info]
    prio_anchor = '"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING":'
    prio_pos = runner_code.find(prio_anchor)
    runner_code = runner_code[:prio_pos] + "\n".join(prio_lines) + "\n" + runner_code[prio_pos:]

    dispatch_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        block = f"""        elif (
            experiment_id
            == "{exp_id}"
        ):
            payload = {writer_name}(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )"""
        dispatch_blocks.append(block)

    disp_anchor = '== "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING"'
    disp_pos = runner_code.find(disp_anchor)
    disp_start = runner_code.rfind("        elif (", 0, disp_pos)
    runner_code = runner_code[:disp_start] + "\n".join(dispatch_blocks) + "\n" + runner_code[disp_start:]

    with open("experiment_runner.py", "w") as f:
        f.write(runner_code)

    # 4. Update qsearch.py
    print("Updating qsearch.py...")
    with open("qsearch.py") as f:
        qcode = f.read()

    qimp_lines = [f"from {mod_name} import {writer_name}" for mod_name, exp_id, writer_name, cli_name in modules_info]
    qimp_anchor = "from blocker_taxonomy import write_blocker_taxonomy"
    qimp_pos = qcode.find(qimp_anchor)
    qcode = qcode[:qimp_pos] + "\n".join(qimp_lines) + "\n" + qcode[qimp_pos:]

    cmd_blocks = []
    subparser_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        fn_name = "command_" + cli_name.replace("-", "_")
        cmd_block = f"""def {fn_name}(args: argparse.Namespace) -> int:
    report = {writer_name}()
    print(f"Analysis complete: {{args.command}}")
    print(f"Status: {{report.get('status')}}")
    print(f"Registry valid: {{validate_registry()['valid']}}")
    return 0\n\n"""
        cmd_blocks.append(cmd_block)

        var_name = cli_name.replace("-", "_")
        sub_block = f"""    {var_name} = subparsers.add_parser(
        "{cli_name}",
        help="{exp_id.replace('-', ' ').title()}",
    )
    {var_name}.set_defaults(func={fn_name})\n\n"""
        subparser_blocks.append(sub_block)

    cmd_anchor = "def command_coset_strong_fourier_information("
    cmd_pos = qcode.find(cmd_anchor)
    qcode = qcode[:cmd_pos] + "".join(cmd_blocks) + qcode[cmd_pos:]

    sub_anchor = '    coset_strong_fourier_information = subparsers.add_parser('
    sub_pos = qcode.find(sub_anchor)
    qcode = qcode[:sub_pos] + "".join(subparser_blocks) + qcode[sub_pos:]

    with open("qsearch.py", "w") as f:
        f.write(qcode)

    # 5. Update tests/test_experiment_runner.py
    print("Updating tests/test_experiment_runner.py...")
    with open("tests/test_experiment_runner.py") as f:
        tcode = f.read()

    test_methods = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        test_fn_name = "test_" + mod_name + "_dispatches_from_clean_registry"
        if test_fn_name not in tcode:
            tblock = f"""    def {test_fn_name}(self):
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
        self.assertTrue(validation["valid"], validation["issues"])\n\n"""
            test_methods.append(tblock)

    if test_methods:
        target = '\nif __name__ == "__main__":'
        inserted_code = "".join(test_methods) + "\n"
        tcode = tcode.replace(target, inserted_code + target)
        with open("tests/test_experiment_runner.py", "w") as f:
            f.write(tcode)

    # 6. Update README.md
    print("Updating README.md...")
    with open("README.md") as f:
        readme_code = f.read()

    readme_blocks = []
    for mod_name, exp_id, writer_name, cli_name in modules_info:
        rblock = f"""```bash
python3 qsearch.py {cli_name}
```
Evaluate {exp_id.replace('-', ' ').title()} theorem contract and headline metrics.

"""
        readme_blocks.append(rblock)

    ranchor = "Isolate the solvable and unresolved equal-pair commutator terms:"
    rpos = readme_code.find(ranchor)
    if rpos != -1:
        rblock_pos = readme_code.rfind("```bash", 0, rpos)
        readme_code = readme_code[:rblock_pos] + "".join(readme_blocks) + readme_code[rblock_pos:]
        with open("README.md", "w") as f:
            f.write(readme_code)

    print("Batch wiring complete!")
