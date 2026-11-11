"""Collect verdicts, timings, proof checks and CNF sha256 from the .out files of this folder into
cnf_sha256.txt and print a per-file summary (counts of UNSAT / LRAT VERIFIED / SAT / model_check OK)."""
import json, re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rows = []
for fn in sorted(glob.glob('*.out')):
    for line in open(fn):
        m = re.search(r'(UNSAT|SAT|UNKNOWN) (\{.*\})\s*$', line)
        if m:
            info = json.loads(m.group(2))
            case = re.match(r'case (\d+):', line)
            rows.append((fn, case.group(1) if case else '-', m.group(1), info))
        m2 = re.search(r"UNSAT \[([0-9.]+)s\] (\{.*\})", line)
        if m2:   # gadget_cnf5 format (python dict)
            info = eval(m2.group(2), {})
            rows.append((fn, '-', 'UNSAT', {'cnf_sha256': info['cnf_sha256'], 'vars': info['vars'], 'clauses': info['clauses'],
                                             'solve_s': float(m2.group(1)), 'proof': info.get('proof'), 'proof_bytes': info.get('proof_bytes')}))
with open('cnf_sha256.txt', 'w') as f:
    f.write('# file case verdict vars clauses solve_s proof cnf_sha256\n')
    for fn, c, v, i in rows:
        f.write(f"{fn} {c} {v} {i.get('vars')} {i.get('clauses')} {i.get('solve_s')} {str(i.get('proof', i.get('model_check'))).replace(' ', '_')} {i.get('cnf_sha256')}\n")
summ = {}
for fn, c, v, i in rows:
    s = summ.setdefault(fn, {'UNSAT': 0, 'LRAT_VERIFIED_fixed': 0, 'SAT': 0, 'model_OK': 0, 'UNKNOWN': 0, 'solve_s': 0.0, 'check_s': 0.0})
    s[v] += 1
    if 'LRAT VERIFIED' in str(i.get('proof', '')): s['LRAT_VERIFIED_fixed'] += 1
    if i.get('model_check') == 'OK': s['model_OK'] += 1
    s['solve_s'] += float(i.get('solve_s') or 0); s['check_s'] += float(i.get('check_s') or 0)
for fn, s in summ.items():
    print(fn, s)
