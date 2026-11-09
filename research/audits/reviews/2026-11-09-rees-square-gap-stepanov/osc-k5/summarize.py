"""Collect the JSON lines of osc_k5.py outputs (*.out in this folder) into one table per k.
Usage: python summarize.py [files...]"""
import sys, os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, '*.out')))
rows = {}
cls = {}
for f in files:
    last = None
    for line in open(f):
        line = line.strip()
        if line.startswith('{'):
            d = json.loads(line)
            last = (d['k'], d['p'])
            rows[last] = (d, os.path.basename(f))
            cls[last] = []
        elif line.startswith('CLASS') and last:
            cls[last].append(json.loads(line[6:]))
for k in sorted({a for a, _ in rows}):
    print('k=%d' % k)
    print('%5s %6s %12s %8s %8s %7s %6s %6s %6s %6s %7s %6s %6s %6s %7s %s' % (
        'p', 'lam', 'Rees', 'PW', 'PW_pair', 'N1/mu1', 'B_L', 'B_H', 'B_Lcc', 'B_Hcc', 'sh_pair', 'sh_L', 'sh_H',
        'cpu_h', 'val', 'file'))
    for (kk, p) in sorted(rows):
        if kk != k:
            continue
        d, f = rows[(kk, p)]
        v = d.get('validate')
        vs = '-' if not v else ('diff=%g' % v['max_abs_diff'])
        print('%5d %6.3f %12d %8.4f %8.4f %7.3f %6.3f %6.2f %6.3f %6.2f %7.4f %6.3f %6.3f %6.3f %7s %s' % (
            p, d['lam'], round(d['Rees']), d['PW'], d['PW_pair'], d['N1_mu1'], d['B_L'], d['B_H'], d['B_L_cc'],
            d['B_H_cc'], d['share_pair'], d['share_L'], d['share_H'], d['enum_cpu'] / 3600, vs, f))
    print()
    print('B_all = max over ALL non-pair classes of n|Fh|/(k Fh0) (L-type normalisation applied to every class)')
    for (kk, p) in sorted(cls):
        if kk != k:
            continue
        cand = [(r['max_n_absF'] / k, (r['r'], r['c'])) for r in cls[(kk, p)] if sorted((r['r'], r['c'])) != [0, 2]]
        b, rc = max(cand)
        m6 = max(r['max_n_absF'] / k for r in cls[(kk, p)] if r['r'] + r['c'] >= 6)
        print('%5d  B_all=%.3f at %s   max over m>=6 of n|Fh|/(k Fh0) = %.3f' % (p, b, rc, m6))
    print()
    print('per-class: max n|Fh|/(k Fh0) [L-type]  and  max |Fh| sqrt(N1)/(sqrt(m) Fh0) [H-type]')
    keys = sorted({(r['r'], r['c']) for (kk, p) in cls if kk == k for r in cls[(kk, p)] if r['r'] <= r['c']})
    print('%5s ' % 'p' + ' '.join('%11s' % ('(%d,%d)' % rc) for rc in keys))
    for (kk, p) in sorted(cls):
        if kk != k:
            continue
        m = {(r['r'], r['c']): r for r in cls[(kk, p)]}
        out = []
        for rc in keys:
            r = m.get(rc)
            if r is None:
                out.append('%11s' % '-')
            elif rc[0] + rc[1] <= 5:
                out.append('%11.3f' % (r['max_n_absF'] / k))
            else:
                out.append('%11.2f' % r['max_H'])
        print('%5d ' % p + ' '.join(out))
    print()
