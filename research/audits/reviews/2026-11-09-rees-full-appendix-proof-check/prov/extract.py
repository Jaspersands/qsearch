"""Extract \\file{} paths and \\ref{} labels from appendix-provenance.tex and
check (a) that each path exists in the repo and (b) that each label is defined
somewhere in T/*.tex. Read-only; prints a report to stdout.

Usage: /opt/anaconda3/bin/python -I extract.py
"""
import os
import re
import glob

R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
SRC = T + "/appendix-provenance.tex"

lines = open(SRC, encoding="utf-8").read().split("\n")

# all labels defined in the paper (T/*.tex only, as the brief says)
labels = {}
for fn in sorted(glob.glob(T + "/*.tex")):
    base = os.path.basename(fn)
    if base == "main-full-draft.tex":
        continue
    for i, ln in enumerate(open(fn, encoding="utf-8").read().split("\n"), 1):
        for m in re.finditer(r"\\label\{([^}]*)\}", ln):
            labels.setdefault(m.group(1), []).append((base, i))

dups = {k: v for k, v in labels.items() if len(v) > 1}

cur_item = None
file_hits = []
ref_hits = []
for i, ln in enumerate(lines, 1):
    m = re.search(r"\\label\{(prov:[^}]*)\}", ln)
    if m:
        cur_item = m.group(1)
    if ln.lstrip().startswith("%"):
        continue  # comments are checked separately
    for m in re.finditer(r"\\file\{([^}]*)\}", ln):
        file_hits.append((i, cur_item, m.group(1)))
    for m in re.finditer(r"\\(?:ref|eqref|Cref|cref)\{([^}]*)\}", ln):
        for lab in m.group(1).split(","):
            ref_hits.append((i, cur_item, lab.strip()))


def exists(p):
    p = p.rstrip("/")
    return os.path.exists(os.path.join(R, p))


print("== duplicate labels in T/*.tex ==")
for k, v in sorted(dups.items()):
    print(k, v)

print("\n== \\file paths ==")
last_dir = None
for (i, item, p) in file_hits:
    if "*" in p:
        status = "GLOB"
    elif p.startswith(".../"):
        status = "ABBREV"
    elif exists(p):
        status = "OK"
    else:
        # try relative to the last folder named on the same item
        status = "MISSING"
    print(f"{i:4d} {item or '-':28s} {status:8s} {p}")

print("\n== \\ref labels ==")
missing = 0
for (i, item, lab) in ref_hits:
    if lab not in labels:
        print(f"{i:4d} {item or '-':28s} UNDEFINED {lab}")
        missing += 1
print("undefined:", missing, "of", len(ref_hits))

# defined prov labels and where they are referenced from outside the appendix
print("\n== prov labels: references from other files ==")
prov_labels = [k for k in labels if k.startswith("prov:")]
alltext = {}
for fn in sorted(glob.glob(T + "/*.tex")):
    base = os.path.basename(fn)
    if base == "main-full-draft.tex":
        continue
    alltext[base] = open(fn, encoding="utf-8").read()
for k in sorted(prov_labels):
    users = [b for b, t in alltext.items() if ("{" + k + "}") in t.replace("\\label{" + k + "}", "")]
    print(f"{k:28s} referenced in: {', '.join(users) if users else 'NOWHERE'}")
# references to prov: labels that are undefined
print("\n== prov: references anywhere that are undefined ==")
for b, t in alltext.items():
    for m in re.finditer(r"\\ref\{(prov:[^}]*)\}", t):
        if m.group(1) not in labels:
            print(b, m.group(1))
