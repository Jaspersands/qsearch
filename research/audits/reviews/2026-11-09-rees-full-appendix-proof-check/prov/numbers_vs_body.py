"""Heuristic: list, per provenance item, the numbers it quotes that do not occur
anywhere in the body (main.tex and the other appendices, comments stripped).
A number missing from the body is not an error by itself (many are copied from
sources); the list is a worklist for manual checks. Read-only.
Usage: /opt/anaconda3/bin/python -I numbers_vs_body.py > numbers_vs_body.out
"""
import glob
import os
import re

R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"


def strip_comments(s):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in s.split("\n"))


def norm(s):
    s = s.replace("{,}", "").replace("\\,", "")
    return s


body = ""
for fn in sorted(glob.glob(T + "/*.tex")):
    b = os.path.basename(fn)
    if b in ("main-full-draft.tex", "appendix-provenance.tex"):
        continue
    body += norm(strip_comments(open(fn, encoding="utf-8").read())) + "\n"
# numbers.tex macros: include their values too
body_nums = set(re.findall(r"\d+(?:\.\d+)?", body))

src = open(T + "/appendix-provenance.tex", encoding="utf-8").read().split("\n")
cur = None
acc = {}
for ln in src:
    m = re.search(r"\\label\{(prov:[^}]*)\}", ln)
    if m:
        cur = m.group(1)
    if ln.lstrip().startswith("%") or cur is None:
        continue
    t = norm(ln)
    t = re.sub(r"\\file\{[^}]*\}", " ", t)  # paths carry dates, skip
    t = re.sub(r"\\(?:ref|label|cite)\{[^}]*\}", " ", t)
    t = re.sub(r"\\cite\[[^]]*\]\{[^}]*\}", " ", t)
    for x in re.findall(r"\d+(?:\.\d+)?", t):
        acc.setdefault(cur, []).append(x)

for item, xs in acc.items():
    miss = sorted({x for x in xs if x not in body_nums and len(x) >= 2}, key=lambda z: float(z))
    if miss:
        print(f"{item:28s} {' '.join(miss)}")
