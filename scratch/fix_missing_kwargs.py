import glob
import re

def fix_kwargs():
    fixed = 0
    for p in glob.glob("*.py"):
        with open(p) as f:
            code = f.read()

        if "kwargs" in code and "def write_" in code:
            lines = code.split("\n")
            in_writer = False
            writer_start = -1
            writer_end = -1
            has_kwargs_param = False
            uses_kwargs_body = False

            for i, line in enumerate(lines):
                if line.lstrip().startswith("def write_"):
                    in_writer = True
                    writer_start = i
                    has_kwargs_param = False
                    uses_kwargs_body = False

                if in_writer:
                    if "kwargs" in line and not line.lstrip().startswith("def "):
                        uses_kwargs_body = True
                    if "kwargs" in line and line.lstrip().startswith("def ") or ("**kwargs" in line and i <= writer_start + 10):
                        has_kwargs_param = True
                    if line.startswith("def ") and i > writer_start:
                        in_writer = False

            if uses_kwargs_body and not has_kwargs_param:
                # Add **kwargs: Any to writer signature
                def_idx = code.find("def write_")
                ret_idx = code.find(") ->", def_idx)
                if ret_idx != -1:
                    code = code[:ret_idx] + ", **kwargs: Any" + code[ret_idx:]
                    with open(p, "w") as f:
                        f.write(code)
                    fixed += 1
                    print("Added **kwargs to signature in:", p)

    print(f"Total fixed kwargs signatures: {fixed}")

if __name__ == "__main__":
    fix_kwargs()
