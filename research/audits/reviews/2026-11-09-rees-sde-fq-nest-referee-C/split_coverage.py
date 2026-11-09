"""Referee C: independent coverage check of the *_split.out files of the F_q nest note.
For each (outfile, casefile, p, k, S, expected |L|): every case line x every gamma_(1,1) in F_p^k
must appear exactly once (duplicates reported), each with UNSAT and 'proof': 'LRAT VERIFIED',
and the header (p, S, k, d=2, L=nest) must match.  Any other non-DONE line is reported."""
import sys, os, re, itertools, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-08-rees-sde-fq-nest')
jobs = [('cases11_split.out', 'cases11.txt', 11, 2, '[0, 1, 3, 4, 5, 9]', 110),
        ('cases13_split.out', 'cases13.txt', 13, 2, '[0, 1, 3, 4, 9, 10, 12]', 156),
        ('k3_7_split.out', 'cases7k3.txt', 7, 3, '[0, 1, 2, 4]', 294)]
pat = re.compile(r"^p=(\d+) S=(\[[^\]]*\]) k=(\d+) d=(\d+) L=(\S+) \(\|L\|=(\d+)\) \[reduced, weak nondeg\] fix=(\S+): (\w+) \[")
for out, cf, p, k, S, nL in jobs:
    cases = [l.strip() for l in open(os.path.join(D, cf)) if l.strip()]
    want = {c + ';1,1,0:' + ','.join(map(str, g)) for c in cases for g in itertools.product(range(p), repeat=k)}
    seen = collections.Counter(); bad = []; other = 0
    for line in open(os.path.join(D, out)):
        line = line.rstrip('\n')
        if line.startswith('DONE'):
            continue
        m = pat.match(line)
        if not m:
            other += 1; bad.append(line[:160]); continue
        pp, SS, kk, dd, LL, nn, fix, res = m.groups()
        ok = (int(pp) == p and SS == S and int(kk) == k and dd == '2' and LL == 'nest' and int(nn) == nL
              and res == 'UNSAT' and "'proof': 'LRAT VERIFIED'" in line)
        if not ok:
            bad.append(line[:200])
        seen[fix] += 1
    missing = want - set(seen); extra = set(seen) - want
    dups = [f for f, c in seen.items() if c > 1]
    print(f'{out}: {len(cases)} cases x {p**k} = {len(want)} wanted; {len(seen)} distinct lines; '
          f'missing {len(missing)}, extra {len(extra)}, duplicated {len(dups)}, bad {len(bad)}, unparsed {other}')
    for b in bad[:5]:
        print('   BAD:', b)
    for mm in sorted(missing)[:5]:
        print('   MISSING:', mm)
