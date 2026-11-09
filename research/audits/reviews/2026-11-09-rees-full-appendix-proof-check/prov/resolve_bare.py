"""Resolve the \\file{} names that extract.py could not find at the repo root: bare file
names ("outputs foo.out in that folder"), '.../' abbreviations and globs. Each is tried
(1) relative to every folder or file's folder named earlier in the same item, (2) relative
to research/audits/reviews and research/, (3) under docs/papers/rees-hsp/. Prints the
resolution or UNRESOLVED. Read-only.
Usage: /opt/anaconda3/bin/python -I resolve_bare.py > resolve_bare.out
"""
import glob, os, re
R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
src = open(T + "/appendix-provenance.tex", encoding="utf-8").read().split("\n")
cur, dirs = None, []
bad = 0
for k, l in enumerate(src, 1):
    m = re.search(r"\\label\{(prov:[^}]*)\}", l)
    if m:
        cur, dirs = m.group(1), []
    if l.lstrip().startswith("%"):
        continue
    for fm in re.finditer(r"\\file\{([^}]*)\}", l):
        p = fm.group(1).replace("\\_", "_")
        full = os.path.join(R, p.rstrip("/"))
        if os.path.exists(full) and "*" not in p:
            dirs.append(full if os.path.isdir(full) else os.path.dirname(full))
            continue
        name = p[4:] if p.startswith(".../") else p
        cands = []
        for d in reversed(dirs):
            cands += glob.glob(os.path.join(d, name)) + glob.glob(os.path.join(d, "*", name))
        for base in ("research/audits/reviews", "research", "docs/papers/rees-hsp"):
            cands += glob.glob(os.path.join(R, base, name))
        cands = sorted(set(cands))
        if cands:
            print(f"{k:4d} {(cur or "-"):26s} {p:48s} -> {os.path.relpath(cands[0], R)}" + (f" (+{len(cands)-1} more)" if len(cands) > 1 else ""))
        else:
            bad += 1
            print(f"{k:4d} {(cur or "-"):26s} {p:48s} UNRESOLVED")
print("unresolved:", bad)
