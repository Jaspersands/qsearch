"""Compare own verdicts (e2dfs_c / e2dfs.py) with the threshold-8 dfs2b outputs and the
paper's exact lists; check E2row c E_2 and the divisor inclusion on the decided ranges.
usage: compare.py   (reads the *.out files in this folder and ../2026-11-05-rees-threshold-8/)"""
import re, os, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, "..", "2026-11-05-rees-threshold-8")

def parse(path):
    v = {}
    for line in open(path):
        m = re.search(r"k=(\d+) p=(\d+) (INFEASIBLE|FEASIBLE)", line)      # own format
        if m:
            v[(int(m.group(1)), int(m.group(2)))] = m.group(3) == "INFEASIBLE"; continue
        m = re.match(r"(INFEASIBLE|FEASIBLE) k=(\d+) p=(\d+)", line)       # dfs2b format
        if m:
            v[(int(m.group(2)), int(m.group(3)))] = m.group(1) == "INFEASIBLE"
    return v

def main():
    own = {}
    for f in sorted(glob.glob(os.path.join(HERE, "e2dfs_c_k*.out"))):
        own.update(parse(f))
    py = parse(os.path.join(HERE, "e2dfs_py_k10_partial.out"))
    dis = [key for key in py if key in own and py[key] != own[key]]
    print(f"python vs C port: {len([k for k in py if k in own])} common primes, {len(dis)} disagreements")
    rep = {}
    for f in glob.glob(os.path.join(REP, "dfs2b_k1*.out")):
        rep.update(parse(f))
    E2row = {}
    for line in open(os.path.join(HERE, "cyclo_check.out")):
        m = re.match(r"k=(\d+) .*E2row=\[(.*?)\]", line)
        if m:
            E2row[int(m.group(1))] = {int(x) for x in m.group(2).split(",") if x.strip()}
    exact = {4: {5, 13, 17, 29, 37, 53}, 5: {11, 31, 41, 61, 71, 101, 131, 151, 181},
             # E_2(6): threshold-7-check e2six.out (53 primes, max 859); E_2(7): threshold-2 Thm 6
             6: {7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181,
                 193, 199, 211, 223, 241, 271, 277, 283, 307, 331, 349, 367, 373, 379, 409, 421, 433,
                 439, 463, 487, 499, 523, 547, 577, 619, 631, 643, 661, 673, 691, 751, 757, 787, 859},
             7: {29, 43, 71, 113, 127, 197, 211, 239, 281, 337, 379, 421, 449, 463, 491, 547, 617, 631,
                 659, 673, 701, 743, 757, 827, 883, 911, 953, 1009, 1051, 1093, 1163, 1289, 1303, 1373,
                 1471, 1499, 1583, 1597, 1667, 1709, 1877, 2017, 2087, 2143, 2213, 2297, 2339, 2381,
                 2423, 2591, 2731, 2801, 2843, 2969, 3137, 3221}}
    for k in sorted({k for k, _ in own}):
        keys = sorted(p for kk, p in own if kk == k)
        inE = [p for p in keys if own[(k, p)]]
        notE = [p for p in keys if not own[(k, p)]]
        allp = [p for p in range(3, keys[-1] + 1) if p % k == 1 and all(p % d for d in range(2, int(p ** 0.5) + 1))]
        assert allp == keys, ("gap in decided range", k)
        common = [p for p in keys if (k, p) in rep]
        bad = [p for p in common if rep[(k, p)] != own[(k, p)]]
        print(f"k={k}: own decided {len(keys)} primes up to {keys[-1]}; in E_2: {len(inE)}; "
              f"not in E_2: {notE if len(notE) <= 10 else str(len(notE)) + ' primes'}; vs dfs2b: {len(common)} common, {len(bad)} disagree {bad}")
        if k in exact:
            ex = {p for p in exact[k] if p <= keys[-1]}
            print(f"   own E_2({k}) n [3,{keys[-1]}] == paper/earlier exact list: {set(inE) == ex}"
                  f" (own {len(inE)}, list {len(ex)})")
        if k in E2row:
            miss = [p for p in E2row[k] if p <= keys[-1] and not own.get((k, p), True)]
            print(f"   E2row({k}) n decided range c E_2: {'yes' if not miss else 'NO ' + str(miss)}")
        for D in range(2, k):
            if k % D: continue
            if D in exact:
                viol = [p for p in exact[D] if p % k == 1 and p <= keys[-1] and not own[(k, p)]]
                print(f"   E_2({D}) n {{p=1 mod {k}}} c E_2({k}) on decided range: "
                      f"{'yes' if not viol else 'NO ' + str(viol)} "
                      f"({sorted(p for p in exact[D] if p % k == 1)})")
            own_D = {p for (kk, p), v in own.items() if kk == D and v}
            if own_D:
                top = max(p for (kk, p) in own if kk == D)
                viol = [p for p in own_D if p % k == 1 and p <= min(top, keys[-1]) and not own[(k, p)]]
                print(f"   own E_2({D}) c E_2({k}) on common range: {'yes' if not viol else 'NO ' + str(viol)}"
                      f" (gcd(D,k/D) = {math.gcd(D, k // D)})")

if __name__ == "__main__":
    main()
