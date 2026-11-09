"""prov:core claims every core result is implied by a companion statement (cross-check of
5 Nov). For the labelled statements added to the core on 9 Nov (read from the + lines of
O/diffs/patch9nov-core_main-core.tex.diff, not from T/core), compare each statement's text
with the companion's statement of the same label (T/main.tex). Prints a similarity ratio and
the first differing words. Read-only; a high ratio is not a proof of implication.
Usage: /opt/anaconda3/bin/python -I core_vs_main.py > core_vs_main.out
"""
import re, difflib
R = "/Users/jaspersands/Developer/qsearch"
O = R + "/research/audits/reviews/2026-11-09-rees-full-appendix-proof-check"
T = R + "/research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree"
diff = open(O + "/diffs/patch9nov-core_main-core.tex.diff", encoding="utf-8").read().split("\n")
plus = "\n".join(l[1:] for l in diff if l.startswith("+") and not l.startswith("+++"))
main = open(T + "/main.tex", encoding="utf-8").read()

def statement(text, lab):
    k = text.find("\\label{" + lab + "}")
    if k < 0:
        return None
    b = text.rfind("\\begin{", 0, k)
    env = re.match(r"\\begin\{(\w+)\}", text[b:]).group(1)
    e = text.find("\\end{" + env + "}", k)
    return text[b:e] if e > 0 else text[b:k + 3000]

def norm(s):
    s = re.sub(r"(?m)^\s*%.*$", " ", s)
    return re.sub(r"\s+", " ", s).strip()

labs = sorted(set(re.findall(r"\\label\{([^}]*)\}", plus)))
print("labels on + lines of the core diff:", labs)
for lab in labs:
    a, b = statement(plus, lab), statement(main, lab)
    if a is None or b is None:
        print(f"{lab}: core={'yes' if a else 'no'} main={'yes' if b else 'no'}")
        continue
    a, b = norm(a), norm(b)
    sm = difflib.SequenceMatcher(None, a.split(), b.split(), autojunk=False)
    print(f"\n{lab}: core {len(a.split())} words, main {len(b.split())} words, ratio {sm.ratio():.3f}")
    n = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal" and n < 6:
            n += 1
            print(f"  {op}: core[{' '.join(a.split()[i1:i2])[:160]}] main[{' '.join(b.split()[j1:j2])[:160]}]")
