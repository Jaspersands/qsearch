"""Extract every \\file{...} argument from the Rees paper .tex files and test each path.

Resolution order for a cited path P: repo root, paper directory, formal/ (for Formal/...),
then (for bare names or short relative paths) any file in the repo whose path ends with /P.
"""
import os
import re
import sys
from collections import defaultdict

REPO = "/Users/jaspersands/Developer/qsearch"
PAPER = os.path.join(REPO, "docs/papers/rees-hsp")

def files_in_paper():
    out = []
    for root, _, names in os.walk(PAPER):
        for n in names:
            if n.endswith(".tex"):
                out.append(os.path.join(root, n))
    return sorted(out)

def extract(path):
    text = open(path, encoding="utf-8").read()
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        commented = stripped.startswith("%")
        for m in re.finditer(r"\\file\{([^{}]*)\}", line):
            hits.append((lineno, m.group(1), commented))
    return hits

def build_index():
    idx = defaultdict(list)
    skip = {".git", ".lake", "node_modules", "__pycache__"}
    for root, dirs, names in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in skip]
        for n in names + dirs:
            full = os.path.join(root, n)
            idx[n].append(os.path.relpath(full, REPO))
    return idx

def resolve(arg, idx):
    a = arg.replace("\\_", "_").rstrip("/")
    for base in (REPO, PAPER, os.path.join(REPO, "formal")):
        if os.path.exists(os.path.join(base, a)):
            return "exact", os.path.relpath(os.path.join(base, a), REPO)
    cands = [c for c in idx.get(os.path.basename(a), []) if c.endswith(a)]
    if cands:
        return "by-suffix", "; ".join(sorted(cands)[:4]) + (" ..." if len(cands) > 4 else "")
    return "MISSING", ""

def main():
    idx = build_index()
    rows = []
    for f in files_in_paper():
        for lineno, arg, commented in extract(f):
            status, where = resolve(arg, idx)
            rows.append((os.path.relpath(f, PAPER), lineno, arg, commented, status, where))
    for r in rows:
        print("\t".join(str(x) for x in r))
    live = [r for r in rows if not r[0].startswith("archive/")]
    print("\n# totals", file=sys.stderr)
    print(f"citations={len(rows)} live(non-archive)={len(live)}", file=sys.stderr)
    for st in ("exact", "by-suffix", "MISSING"):
        print(st, sum(1 for r in rows if r[4] == st), file=sys.stderr)

main()
