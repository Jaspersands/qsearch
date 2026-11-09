"""Print the per-part status phrases (\\emph{...} headings and '(a) ... proved' patterns)
inside given remarks of the paper. Read-only. Usage: python -I partlabels.py"""
import re, glob, os
T = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
txt = {os.path.basename(f): open(f, encoding="utf-8").read() for f in glob.glob(T + "/*.tex") if "full-draft" not in f}
labs = ["rem:fc-zero-sum-sis", "rem:fc-zero-sum-arity", "rem:fc-witness-h3", "rem:fc-tradeoff",
        "rem:sde-subquadratic", "rem:sde-worst-case", "rem:sde-worst-case-q1", "rem:sde-block-steered",
        "rem:filters", "rem:mixed-source"]
for lab in labs:
    for b, t in txt.items():
        i = t.find("\\label{" + lab + "}")
        if i < 0: continue
        j = t.find("\\end{remark}", i)
        body = t[i:j]
        hs = re.findall(r"\\emph\{([^{}]{0,120}?\((?:proved|argued|conditional|open|finite)[^)]{0,100}\))", body)
        hs += re.findall(r"(\((?:[a-e]|i{1,3}|iv)\)[^()]{0,25}?\b(?:is |are )?(?:proved|argued|conditional|open)\b[^.;]{0,40})", body)
        print("===", lab, b, "len", len(body))
        for h in hs: print("   ", h[:200].replace("\n", " "))
