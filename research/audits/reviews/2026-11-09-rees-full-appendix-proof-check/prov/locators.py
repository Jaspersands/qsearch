"""Check the section / statement locators that appendix-provenance.tex gives for its
source reports: for every \\file{X.md} followed by a parenthesis naming 'Section(s) N',
'Proposition N', 'Lemma N', 'Theorem N', 'Corollary N', 'Finding N', 'item N', check that
X.md has a heading numbered N (for sections) or contains the string 'Kind N' (for
statements). Read-only; a 'not found' is a lead to read by hand, not a verdict.
Usage: /opt/anaconda3/bin/python -I locators.py > locators.out
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
            # bare names are relative to research/audits/reviews
            full = os.path.join(R, "research/audits/reviews", os.path.basename(path))
        if not os.path.exists(full):
            print(f"{k:4d} {cur:26s} MISSING FILE {path}")
            continue
        text = open(full, encoding="utf-8", errors="replace").read()
        heads = [h for h in text.split("\n") if h.startswith("#")]
        par_t = par.replace("~", " ").replace("\\S", "Section ")
        # sections: 'Section 5.4', 'Sections 1--3', 'Section 1.9', 'Section 3'
        for sm in re.finditer(r"Sections?\s+([0-9]+(?:\.[0-9]+)*)(?:\s*(?:--|-|and|,)\s*([0-9]+(?:\.[0-9]+)*))?", par_t):
            for num in [g for g in sm.groups() if g]:
                pat = re.compile(r"^#+\s*(?:§\s*)?" + re.escape(num) + r"(?:[.\s:)]|$)")
                hit = any(pat.search(h) for h in heads)
                if not hit:
                    # bold-numbered items, e.g. '**1.9 ...**'
                    hit = re.search(r"(?m)^\*\*" + re.escape(num) + r"[\s.]", text) is not None
                print(f"{k:4d} {cur:26s} {'ok ' if hit else 'NOT FOUND'} Section {num:6s} in {os.path.basename(full)}")
        for sm in re.finditer(r"(Proposition|Lemma|Theorem|Corollary|Finding|Findings|item|items)\s+([A-Z]?[0-9]+(?:\.[0-9]+)*)", par_t):
            kind, num = sm.groups()
            kind0 = kind.rstrip("s")
            hit = re.search(re.escape(kind0) + r"\s*" + re.escape(num) + r"\b", text, flags=re.I) is not None
            print(f"{k:4d} {cur:26s} {'ok ' if hit else 'NOT FOUND'} {kind0} {num:6s} in {os.path.basename(full)}")
