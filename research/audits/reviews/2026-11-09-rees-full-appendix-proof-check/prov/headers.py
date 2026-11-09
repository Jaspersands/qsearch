"""For every label referenced in appendix-provenance.tex, print the environment
and the optional title (status label) of the statement it labels in T/*.tex.
Read-only. Usage: /opt/anaconda3/bin/python -I headers.py > headers.out
"""
import os
import re
import glob

R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
SRC = T + "/appendix-provenance.tex"

files = {}
for fn in sorted(glob.glob(T + "/*.tex")):
    b = os.path.basename(fn)
    if b == "main-full-draft.tex":
        continue
    files[b] = open(fn, encoding="utf-8").read().split("\n")

where = {}
for b, ls in files.items():
    for i, ln in enumerate(ls):
        for m in re.finditer(r"\\label\{([^}]*)\}", ln):
            where[m.group(1)] = (b, i)

def header(lab):
    b, i = where[lab]
    ls = files[b]
    # search back up to 3 lines for \begin{env}[title] or \section/\subsection
    for j in range(i, max(-1, i - 4), -1):
        m = re.search(r"\\begin\{(\w+\*?)\}(\[(.*)\])?", ls[j])
        if m:
            title = m.group(3) or ""
            return f"{b}:{j+1} {m.group(1)} [{title[:160]}]"
        m = re.search(r"\\(sub)*section\*?\{(.*)\}", ls[j])
        if m:
            return f"{b}:{j+1} section {{{m.group(2)[:160]}}}"
        m = re.search(r"\\item", ls[j])
        if m:
            return f"{b}:{j+1} item: {ls[j][:160]}"
    return f"{b}:{i+1} ?? {ls[i][:160]}"

src = open(SRC, encoding="utf-8").read().split("\n")
cur = None
seen = set()
for k, ln in enumerate(src, 1):
    m = re.search(r"\\label\{(prov:[^}]*)\}", ln)
    if m:
        cur = m.group(1)
        print(f"\n### {cur} (line {k})")
    if ln.lstrip().startswith("%"):
        continue
    for m in re.finditer(r"\\(?:ref|eqref)\{([^}]*)\}", ln):
        lab = m.group(1)
        if lab.startswith("prov:"):
            continue
        key = (cur, lab)
        if key in seen:
            continue
        seen.add(key)
        print(f"  {lab:36s} {header(lab)}")
