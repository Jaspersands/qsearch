#!/opt/anaconda3/bin/python
"""Caption numbers of tab:query-crossover with exact 8*ln 6 (first integer p with closed_form_Q >= Q_new,
and the largest prime below it), Q_new from verify_headline.json. Read-only use of classical_lb.py."""
import importlib.util, json, math, sys
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
src = ROOT / "research/audits/reviews/2026-11-02-rees-classical-lower-bound/classical_lb.py"
spec = importlib.util.spec_from_file_location("classical_lb", src)
CL = importlib.util.module_from_spec(spec); sys.path.insert(0, str(src.parent)); spec.loader.exec_module(CL)
rows = json.loads((HERE / "verify_headline.json").read_text())["crossover"]
m_of = {"Heisenberg": 3, "filiform": 4, "free, two generators": 5, "Dixmier--Lister": 8}
out = []
for r in rows:
    if r["family"] not in m_of:
        continue
    m, Q = m_of[r["family"]], int(r["Q_new"])
    p = 11
    while CL.closed_form_Q(p, m, Fraction(1, 3)) < Q:
        p += 1
    q = p - 1
    while not CL.is_prime(q):
        q -= 1
    out.append({"family": r["family"], "first_integer_exact_8l": p, "largest_prime_below": q})
print(json.dumps(out, indent=1))
(HERE / "crossover_exact8l.json").write_text(json.dumps(out, indent=1) + "\n")
