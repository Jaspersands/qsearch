#!/bin/sh
# Round-2 runs (2026-11-05), from the repository root, PYTHONPATH=. ; at most two at once, nice 10.
R=research/audits/reviews/2026-11-05-rees-receiver-round2
P=/opt/anaconda3/bin/python
# 1. exact level-0 output law, Heis(F_3), all 19 subgroups, checkpoints K1-K5, plain level-0 cross-check
nice -n 10 /usr/bin/time -l $P -c "import theorems.rees_circuit_mono as M; M.exact_report(out_path='$R/exact_heis_f3_level0.json')" > $R/exact_heis_f3_level0.out 2>&1
# 2. negative controls through the exact level-0 law and its checkpoints
nice -n 10 /usr/bin/time -l $P -c "import theorems.rees_circuit_mono as M; M.negative_controls(out_path='$R/negative_controls_exact.json')" > $R/negative_controls_exact.out 2>&1
# 2b. trajectory mode with checkpoint KS (one changed oracle entry), Heis(F_3) and n4(F_5)
nice -n 10 /usr/bin/time -l $P -c "import theorems.rees_circuit_mono as M; M.trajectory_controls('heis_f3', names=['<[(0, 0, 1)]> normal','<[(1, 0, 0)]> non-normal','<[(1, 0, 0), (0, 0, 1)]> normal'], n=60, out_path='$R/trajectory_controls_heis.json')" > $R/trajectory_controls_heis.out 2>&1
nice -n 10 /usr/bin/time -l $P -c "import theorems.rees_circuit_mono as M; M.trajectory_controls('n4_f5', names=['n4(F_5) H=Z(G)','n4(F_5) H=<e2> non-normal'], n=4, out_path='$R/trajectory_controls_n4.json')" > $R/trajectory_controls_n4.out 2>&1
# 3. Lean: step (R)
(cd formal && nice -n 10 lake build --wfail Formal.ReesMergeReduction) > $R/lean_build.out 2>&1
# 4. class five seeded runs, n6(F_7), power-class solver
nice -n 10 /usr/bin/time -l $P -c "from theorems.rees_circuit_exhaustive import seeded_report; seeded_report('n6',7,seeds=(1,2),out_path='$R/seeded_n6_f7.json')" > $R/seeded_n6_f7.out 2>&1
# Sections 1-2b rerun after the independent check (2026-11-05), same commands, via a 5 GB RSS / 40 min watchdog.
