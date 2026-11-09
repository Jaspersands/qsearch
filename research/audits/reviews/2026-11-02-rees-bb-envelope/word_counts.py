"""(mul, pow) counts of the certified inverse-BCH words for c = 2..9.

Read-only use of theorems/universal_lazard_words.py. Each certificate is verified
exactly before its counts are printed. Run from the repo root:
  /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-bb-envelope/word_counts.py
"""
import sys, time
sys.path.insert(0, ".")
from theorems.universal_lazard_words import compile_lazard_word

top = int(sys.argv[1]) if len(sys.argv) > 1 else 9
for c in range(2, top + 1):
    row = [c]
    for op in ("add", "bracket"):
        t0 = time.time()
        cert = compile_lazard_word(c, op)
        cert.verify()
        muls = sum(1 for s in cert.instructions if s[0] == "mul")
        pows = sum(1 for s in cert.instructions if s[0] == "pow")
        row += [op, muls, pows, round(time.time() - t0, 1)]
    print(*row, flush=True)
