import glob
import re

def fix_signatures():
    fixed = 0
    for p in glob.glob("*.py"):
        if p in ("research_registry.py", "experiment_runner.py", "qsearch.py", "wire_generic_batch.py"):
            continue
        with open(p) as f:
            code = f.read()

        writers = re.findall(r"def (write_[a_zA-Z0-9_]+)\(", code)
        if not writers:
            continue

        writer_name = writers[0]
        def_idx = code.find(f"def {writer_name}(")
        if def_idx == -1:
            continue

        ret_idx = code.find("->", def_idx)
        if ret_idx != -1:
            colon_idx = code.find(":\n", ret_idx)
        else:
            colon_idx = code.find(":\n", def_idx)

        old_sig = code[def_idx:colon_idx + 1]

        # Get exp_id if available
        exp_match = re.search(r"EXP-[A-Z0-9-]+", code)
        exp_id = exp_match.group(0) if exp_match else "EXP-CODE-COSET"

        new_sig = f"""def {writer_name}(
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
        kwargs.pop(_k, None)"""

        if old_sig != new_sig:
            code = code[:def_idx] + new_sig + code[colon_idx + 1:]
            with open(p, "w") as f:
                f.write(code)
            fixed += 1
            print("Fixed signature in:", p)

    print(f"Total fixed signatures: {fixed}")

if __name__ == "__main__":
    fix_signatures()
