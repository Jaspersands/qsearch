"""Check the appendix's claim 'Entries are ordered as the results appear in the
paper: first the body, then the appendices'. For each prov item, take the first
\\ref label in its bold title, locate it (file in \\input order, line), and flag
items that appear earlier in the paper than the previous item. Read-only.
Usage: /opt/anaconda3/bin/python -I order.py > order.out
"""
import re, os, glob
R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
main = open(T + "/main.tex", encoding="utf-8").read().split("\n")
# main.tex body, then \input files in order of appearance
order = ["main.tex"]
inputs = {}
for i, l in enumerate(main):
    if l.lstrip().startswith("%"):
        continue
    for m in re.finditer(r"\\(?:input|include)\{([^}]*)\}", l):
        f = m.group(1)
        if not f.endswith(".tex"):
            f += ".tex"
        if os.path.exists(os.path.join(T, f)) and f not in order:
            order.append(f)
            inputs[f] = i + 1
pos = {}
for f in order:
    for i, l in enumerate(open(os.path.join(T, f), encoding="utf-8").read().split("\n"), 1):
        for m in re.finditer(r"\\label\{([^}]*)\}", l):
            key = (order.index(f), i) if f != "main.tex" else (0, i)
            # a main.tex line after an \input of an appendix belongs after that appendix
            pos[m.group(1)] = (f, i)
def rank(lab):
    f, i = pos[lab]
    if f == "main.tex":
        # place main.tex lines relative to the \input lines
        later = [inputs[g] for g in inputs if inputs[g] < i]
        return (len(later), 0, i)
    return (order.index(f), 1, i)
src = open(T + "/appendix-provenance.tex", encoding="utf-8").read().split("\n")
prev = None
print("input order:", order)
for k, l in enumerate(src, 1):
    m = re.search(r"\\item \\label\{(prov:[^}]*)\}\s*\\textbf\{(.*)", l)
    if not m:
        continue
    labs = [x for x in re.findall(r"\\ref\{([^}]*)\}", m.group(2)) if x in pos and not x.startswith("prov:")]
    if not labs:
        print(f"{k:4d} {m.group(1):28s} (no label in title)")
        continue
    r = rank(labs[0])
    flag = "  <-- earlier than previous item" if prev and r < prev[0] else ""
    print(f"{k:4d} {m.group(1):28s} {labs[0]:34s} {pos[labs[0]][0]}:{pos[labs[0]][1]}{flag}")
    prev = (r, m.group(1))
