"""v2 rule = Schedule 1H+ (rule.py, read-only import, refereed PROVED WITH FIXES) plus
  TL6   two-level contraction RC(6; Z_6 -> {0}) (Lemma R + Lemma SM of fragment.tex), degree 2:
        certificate (v2/certs_tl6.json, checked by check_rc) for p = 1 mod 2520, p < 837384;
        Lemma SM for every p = 1 mod 6, p >= 837384 (v2/tl6_threshold.out, exact rationals).
  L4/L3 l-level {0}-contraction tables (Lemmas T_l, W_l of fragment-v2.tex) of
        2026-11-13-rees-k9-below-21: (kappa,p) = (9,37),(9,19),(9,73) degree 4; (4,13),(6,13) degree 3.
        Tables re-verified by v2/verify_ell.py (third program).
Post-adjustment is exact: the adjusted grades (kappa = 6, 9 anywhere; kappa = 4 at p = 13) feed no other
grade kappa' <= 9 (multiples 12, 18, ... and 8 does not divide 12); asserted below.
Usage: nice -n 19 python v2/rule_v2.py [limit] [variant]   variant in {all, noTL6, noELL}"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import rule as R1
TL6_T = 837384
TL6 = {int(p) for p in json.load(open(os.path.join(HERE, 'certs_tl6.json')))['two-level 6 (p=1 mod 2520)']['found']}
if os.path.exists(os.path.join(HERE, 'certs_tl6_all.json')) and os.environ.get('TL6ALL', '1') == '1':
    TL6 |= {int(p) for p in json.load(open(os.path.join(HERE, 'certs_tl6_all.json')))['found']}
ELL = {(9, 37): 4, (9, 19): 4, (9, 73): 4, (4, 13): 3, (6, 13): 3}
VARIANT = 'all'

def degrees_v2(p, tierB=True, new=True):
    e = _orig(p, new=new, tierB=tierB)
    if not new: return e
    if 6 in e and VARIANT != 'noTL6' and (p >= TL6_T or p in TL6):
        e[6] = min(e[6], (2, 'TL6'))
    if VARIANT != 'noELL':
        for (k, q), d in ELL.items():
            if q == p and k in e:
                assert not any(k2 % k == 0 and k2 != k and k2 in e for k2 in range(2, 10)), (p, k)
                e[k] = min(e[k], (d, f'L{d}'))
    return e

_orig = R1.degrees
R1.degrees = degrees_v2
R1.TAIL = dict(R1.TAIL); R1.TAIL[6] = 2       # p > 2e6 > 837384: TL6 by Lemma SM
assert R1.LIMIT > TL6_T

if __name__ == '__main__':
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else R1.LIMIT
    VARIANT = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if VARIANT == 'noTL6': R1.TAIL[6] = 3
    Emax, tail, top9 = R1.main(lim, True)
    # every class-9 prime with E >= 20 and its grades
    hi = [(v, p) for v, p, e in top9 if v >= 20]
    print('class-9 primes with E >= 20 below', lim, ':', len(hi))
    print('  not = 1 mod 2520:', [(v, p) for v, p in hi if p % 2520 != 1])
    print('  = 1 mod 2520 count:', sum(1 for v, p in hi if p % 2520 == 1), 'values', sorted({v for v, p in hi if p % 2520 == 1}))
