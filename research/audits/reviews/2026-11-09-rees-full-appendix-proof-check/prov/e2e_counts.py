"""prov:bb-corollary says the folder 2026-11-08-rees-blackbox-e2e/ has 'four groups of order
up to 5^5, 30 hidden subgroups, all recovered; two negative controls rejected'. Count from the
JSON records. Read-only. Usage: /opt/anaconda3/bin/python -I e2e_counts.py > e2e_counts.out
"""
import glob, json, os
D = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-08-rees-blackbox-e2e"
tot = 0
for f in sorted(glob.glob(D + "/*.json")):
    d = json.load(open(f))
    d = d[0] if isinstance(d, list) else d
    subs = d.get("subgroups") or d.get("runs") or []
    nc = d.get("negative_controls", {})
    naive = nc.get("naive_pullback", {}).get("checks", {}).get("chart_exp_homomorphism")
    one = nc.get("one_sample", {}).get("caught_by_las_vegas_check")
    strict = nc.get("strict_subkernel", {})
    tot += len(subs)
    rec = sum(1 for x in subs if x.get("blackbox_subgroup_recovered") and x.get("recovered_equals_log_H"))
    print(f"{os.path.basename(f):14s} subgroups={len(subs):2d} recovered={rec:2d} naive_pullback_hom_check={naive} "
          f"one_sample_caught={one} strict_subkernel_applicable={strict.get('applicable')} "
          f"strict_hom_check={strict.get('checks', {}).get('chart_exp_homomorphism')} "
          f"mtime={os.path.getmtime(f):.0f}")
print("groups:", len(glob.glob(D + "/*.json")), "subgroups:", tot)
