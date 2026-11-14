"""Full descent with the repo simulator theorems/rees_end_to_end_sim.py (ExactBackend) on the
free two-generator class-three Lie algebra over F_5 (cover of order 5^10).
Hidden subgroups: H = exp(F_5 (x+z+u)) and H' = exp(F_5 (z+u)).

The simulator's run_rees caches one conditioned top-level state per label; with 25 labels at
stage 3 and dense states of 5^10 x 5 integers that cache would need about 10 GB. The function
below is run_rees copied verbatim except that it does NOT cache conditioned states (it still
caches the label law of the identical top-level sources). Nothing else is changed.
Usage: nice -n 19 /opt/anaconda3/bin/python run_sim_free.py [extra_samples]
"""
import sys
import json
import time
import random
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/theorems")
import rees_end_to_end_sim as sim  # noqa: E402


def run_rees_nocache(cover, oracle, backend, *, seed=0, extra_samples=4, keep_states=False):
    solver = sim.brute_force_sde
    rng = random.Random(seed)
    rec = sim.RunRecord()
    source, rec.source_info = backend.prepare_source(oracle)
    top_law = {}

    def fresh_top():
        rec.top_sources += 1
        rec.oracle_queries += len(cover.points)
        return source

    def make(d):
        if d == cover.c:
            return fresh_top()
        Mm = sim.sde_arity(cover, d+1)
        while True:
            block, labels = [], []
            for _ in range(Mm):
                st = make(d+1)
                if d+1 < cover.c:
                    law = backend.label_probabilities(st)
                else:
                    if "law" not in top_law:
                        top_law["law"] = backend.label_probabilities(st)
                    law = top_law["law"]
                lam = sim._sample(law, rng)
                rec.labels.setdefault(d+1, []).append(lam)
                rec.label_laws.setdefault(d+1, []).append(law)
                block.append(backend.condition(st, lam, law[lam]))
                labels.append(lam)
            witness, count = solver(labels, d+1, cover.p, rng)
            rec.witnesses.setdefault(d+1, []).append((witness, count))
            if witness is not None:
                out = backend.channel(block, witness)
                if keep_states:
                    rec.stage_states.setdefault(d, []).append(out)
                return out

    samples = []
    for _ in range(cover.algebra.dim+extra_samples):
        st = make(1)
        law = backend.readout_probabilities(st)
        k = sim._sample(law, rng)
        rec.readout.append((k, law))
        samples.append(k)
    recovered = sim.nullspace(samples, cover.algebra.dim, cover.p)
    return sim.rref(recovered, cover.p), rec


extra = int(sys.argv[1]) if len(sys.argv) > 1 else 4
p = 5
alg = sim.lie_from_brackets(f"free23(F_{p})", p, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})
t0 = time.time()
cover = sim.make_cover(alg)
print(f"p={p}: cover dims {cover.dims}, order {cover.stage_group(cover.c).order}; series "
      f"{[[list(map(int, v)) for v in b] for b in cover.series]}", flush=True)
backend = sim.ExactBackend(cover)
print(f"  backend ready {time.time()-t0:.0f}s", flush=True)
out = []
for name, gens in (("<x+z+u>", ((1, 0, 1, 1, 0),)), ("<z+u>", ((0, 0, 1, 1, 0),))):
    inst = sim.HiddenInstance(f"free23(F_{p}) H={name}", alg, gens)
    t1 = time.time()
    basis, rec = run_rees_nocache(cover, inst.oracle, backend, seed=20261112, extra_samples=extra, keep_states=True)
    row = sim.grade_run(cover, inst, basis, rec, backend)
    row["stage_outputs_equal_rho_H_d"] = sim.stage_outputs_correct(cover, inst, rec)
    row["source_info"] = rec.source_info
    row["seconds"] = round(time.time()-t1, 1)
    row["label_examples"] = {d: [list(map(int, l)) for l in rec.labels[d][:6]] for d in rec.labels}
    row["witness_examples"] = {d: rec.witnesses[d][:3] for d in rec.witnesses}
    out.append(row)
    print(f"  {name}: recovered={row['recovered_equals_log_H']} basis={row['recovered_basis']} truth={row['truth_basis']} "
          f"normal={row['normal']} order={row['order_H']} fibres={rec.source_info} "
          f"states_exact={row['stage_outputs_equal_rho_H_d']} queries={row['oracle_queries']} {row['seconds']}s", flush=True)
    for d, st in row["stages"].items():
        print(f"    stage {d}: |K_d^perp|={st['label_support_size']} arity(CW)={st['arity']} "
              f"B_d(g_d)={st['schedule_one_arity_B_d(g_d)']} law_exact_uniform={st['every_source_law_uniform_on_K_perp']} "
              f"labels_in_support={st['observed_labels_in_support']} blocks={st['blocks']} min#witnesses={st['min_witness_count']}")
    print(f"    labels {row['label_examples']}  witnesses {row['witness_examples']}", flush=True)
ok = all(r["recovered_equals_log_H"] and r["stage_outputs_equal_rho_H_d"]
         and all(s["every_source_law_uniform_on_K_perp"] and s["observed_labels_in_support"] for s in r["stages"].values())
         for r in out)
print("ALL RUNS OK:", ok)
with open("run_sim_free_5.json", "w") as fh:
    json.dump(out, fh, indent=1, default=str)
