"""Collect the SUMMARY rows of hsp_all_{7,11,13}.out into one markdown table (prints to stdout)."""
import re, os
here = os.path.dirname(os.path.abspath(__file__))
rows = {}; order = []
for p in (7, 11, 13):
    txt = open(os.path.join(here, 'hsp_all_%d.out' % p)).read()
    summ = txt.split('SUMMARY p=%d' % p)[1]
    for line in summ.strip().splitlines():
        m = re.match(r'\s*(.+?)\s{2,}(.+?)\s+instances (\d+) correct (\d+) WRONG (\d+)\s+mean quantum (\d+)\s+mean classical ([\d.]+)', line)
        if not m: continue
        t, b, n, c, w, q, cl = m.groups()
        key = (t, b)
        if key not in rows: rows[key] = {}; order.append(key)
        rows[key][p] = (int(n), int(c), int(w), int(q))
    fails = re.findall(r"'(is_frontend_fail|is_eq_wrong|f23_eq_wrong|C0_closed_form_fail)': ([1-9]\d*)", txt)
    print('p=%d nonzero diagnostic failure counters: %s' % (p, fails if fails else 'none'))
print()
print('| type | branch | p = 7: correct/n (mean quantum) | p = 11 | p = 13 |')
print('|---|---|---|---|---|')
for key in order:
    cells = []
    for p in (7, 11, 13):
        if p in rows[key]:
            n, c, w, q = rows[key][p]; cells.append('%d/%d (%d)%s' % (c, n, q, '' if w == 0 else ' WRONG %d' % w))
        else: cells.append('-')
    print('| %s | %s | %s |' % (key[0], key[1], ' | '.join(cells)))
