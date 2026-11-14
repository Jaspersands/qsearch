"""Full descent runs of the repo simulator theorems/rees_end_to_end_sim.py on the
class-three example: filiform n4 over F_5 and F_7, hidden subgroups
  H = exp(F_p (x1 + x2 + x3 + x4))   and   Z(G) = exp(F_p x4).
The driver sees only the oracle table; H is used only to grade the run.
Usage: nice -n 19 /opt/anaconda3/bin/python run_sim.py [p ...]   (default 5 7)
"""
import sys
import json
import time
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/theorems")
import rees_end_to_end_sim as sim  # noqa: E402

primes = [int(a) for a in sys.argv[1:]] or [5, 7]
out = []
for p in primes:
    alg = sim.filiform4(p)
    cover = sim.make_cover(alg)
    print(f"p={p}: cover dims (g1,g2,g3) = {cover.dims}, order {cover.stage_group(cover.c).order}, "
          f"points {cover.points}", flush=True)
    print("  series bases:", [[list(map(int, v)) for v in b] for b in cover.series])
    backend = sim.ExactBackend(cover)
    for name, gens in (("<x1+x2+x3+x4>", ((1, 1, 1, 1),)), ("Z(G)=<x4>", ((0, 0, 0, 1),))):
        inst = sim.HiddenInstance(f"n4(F_{p}) H={name}", alg, gens)
        for seed in (20261112, 20261113):
            t0 = time.time()
            rec_basis, rec = sim.run_rees(cover, inst.oracle, backend, seed=seed, keep_states=True)
            row = sim.grade_run(cover, inst, rec_basis, rec, backend)
            row["stage_outputs_equal_rho_H_d"] = sim.stage_outputs_correct(cover, inst, rec)
            row["source_info"] = rec.source_info
            row["seconds"] = round(time.time() - t0, 1)
            row["p"], row["seed"] = p, seed
            row["witness_examples"] = {d: [w for w in rec.witnesses[d][:3]] for d in rec.witnesses}
            row["label_examples"] = {d: [list(map(int, l)) if hasattr(l, "__iter__") else l
                                         for l in rec.labels[d][:6]] for d in rec.labels}
            out.append(row)
            print(f"  {name} seed {seed}: recovered={row['recovered_equals_log_H']} basis={row['recovered_basis']} "
                  f"truth={row['truth_basis']} flags(normal={row['normal']}, order={row['order_H']}) "
                  f"fibres={rec.source_info} states_exact={row['stage_outputs_equal_rho_H_d']} "
                  f"queries={row['oracle_queries']} {row['seconds']}s", flush=True)
            for d, st in row["stages"].items():
                print(f"    stage {d}: |K_d^perp|={st['label_support_size']} arity(CW)={st['arity']} "
                      f"B_d(g_d)={st['schedule_one_arity_B_d(g_d)']} law_exact_uniform={st['every_source_law_uniform_on_K_perp']} "
                      f"labels_in_support={st['observed_labels_in_support']} blocks={st['blocks']} "
                      f"min#witnesses={st['min_witness_count']}")
            print(f"    label examples {row['label_examples']}  witness examples {row['witness_examples']}")
ok = all(r["recovered_equals_log_H"] and r["stage_outputs_equal_rho_H_d"]
         and all(s["every_source_law_uniform_on_K_perp"] and s["observed_labels_in_support"]
                 for s in r["stages"].values()) for r in out)
print("ALL RUNS OK:", ok)
with open(f"run_sim_{'_'.join(map(str, primes))}.json", "w") as fh:
    json.dump(out, fh, indent=1, default=str)
