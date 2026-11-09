"""Companion to locators.py: for each 'Section N' / 'Proposition N' locator, print the
provenance's parenthesis and the matching heading (or first matching line) of the source,
so that content can be compared by eye. Read-only.
Usage: /opt/anaconda3/bin/python -I locators2.py > locators2.out
"""
import re, os
R = "/Users/jaspersands/Developer/qsearch"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
src = open(T + "/appendix-provenance.tex", encoding="utf-8").read().split("\n")
cur = None
for k, l in enumerate(src, 1):
    m = re.search(r"\\label\{(prov:[^}]*)\}", l)
    if m:
        cur = m.group(1)
    if l.lstrip().startswith("%"):
        continue
    for fm in re.finditer(r"\\file\{([^}]*\.md)\}\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", l):
        path, par = fm.group(1), fm.group(2)
        full = os.path.join(R, path)
        if not os.path.exists(full):
            full = os.path.join(R, "research/audits/reviews", os.path.basename(path))
        if not os.path.exists(full):
            continue
        lines = open(full, encoding="utf-8", errors="replace").read().split("\n")
        par_t = par.replace("~", " ")
        nums = re.findall(r"Sections?\s+([0-9]+(?:\.[0-9]+)*)(?:\s*(?:--|-)\s*([0-9]+(?:\.[0-9]+)*))?", par_t)
        stmts = re.findall(r"(Proposition|Lemma|Theorem|Corollary)\s+([0-9]+(?:\.[0-9]+)*)", par_t)
        if not nums and not stmts:
            continue
        print(f"\n{k} {cur} {os.path.basename(full)}\n   PROV: ({par[:300]})")
        for a, b in nums:
            for num in [x for x in (a, b) if x]:
                pat = re.compile(r"^(#+\s*(?:§\s*)?|\*\*)" + re.escape(num) + r"(?:[.\s:)*]|$)")
                hs = [h for h in lines if pat.search(h)]
                print(f"   SRC Section {num}: {hs[0][:150] if hs else '-'}")
        for kind, num in stmts:
            hs = [h for h in lines if re.search(kind + r"\s*" + re.escape(num) + r"\b", h)]
            print(f"   SRC {kind} {num}: {hs[0].strip()[:150] if hs else '-'}")
