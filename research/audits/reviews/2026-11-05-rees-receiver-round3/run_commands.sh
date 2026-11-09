#!/bin/zsh
# Round 3 runs, in the order they were run (two queues in parallel). Each line ran under a guard:
# nice -n 10, RSS cap 4.8 GB, 40 min wall cap, PYTHONPATH=. from the repo root; output to the log_*.txt named.
P="/opt/anaconda3/bin/python -B -m theorems.rees_circuit_mono_c3"; RD=research/audits/reviews/2026-11-05-rees-receiver-round3
# --- queue q1
$P --mode relabel --out $RD/relabeling.json   # log: log_relabel.txt
$P --mode merge --out $RD/merge_proofs_f5.json   # log: log_merge_f5.txt
$P --mode A --names trivial --nodes 0 1 2 3 4 5 --out $RD/A_trivial_all_nodes.json   # log: log_A_trivial.txt
$P --mode A --names "Z(G)" --nodes 0 1 2 3 4 5 --out $RD/A_ZG_all_nodes.json   # log: log_A_ZG.txt
$P --mode A --names "<e2> non-normal" --nodes 0 1 2 3 4 5 --out $RD/A_e2_all_nodes.json   # log: log_A_e2.txt
$P --mode A --names "<e1> non-normal" --nodes 0 1 2 3 4 5 --out $RD/A_e1_all_nodes.json   # log: log_A_e1.txt
$P --mode A --names "<e1+e3> non-normal" --nodes 0 1 2 3 4 5 --out $RD/A_e1pe3_all_nodes.json   # log: log_A_e1e3.txt
$P --mode A --names "<e2,e4> non-normal" --nodes 0 --out $RD/A_e2e4_node0.json   # log: log_A_e2e4.txt
$P --mode A --names "<e2,e3> non-normal" --nodes 0 --out $RD/A_e2e3_node0.json   # log: log_A_e2e3.txt
$P --mode A --names "<e2> non-normal" "Z(G)" trivial --nodes 0 --coset-x0 -1 --seed 5 --out $RD/A_symmetry_random_coset.json   # log: log_Asym.txt
# --- queue q2
$P --mode heis --out $RD/heis_f3_reduction_check.json   # log: log_heis.txt
$P --mode B --names "<e3,e4> = gamma_2" --out $RD/B_gamma2_exact.json   # log: log_B_gamma2.txt
$P --mode B --names "<e3,e4> = gamma_2" --cosets random --seed 7 --out $RD/B_gamma2_exact_random_cosets.json   # log: log_B_gamma2_sym.txt
$P --mode B --names "<e1+e2,e3> (closure)" --out $RD/B_closure_exact.json   # log: log_B_closure.txt
$P --mode B --names trivial "Z(G)" "<e2> non-normal" --tuples zero random --out $RD/B_conditional_1.json   # log: log_B_small.txt
$P --mode B --names "<e1> non-normal" "<e1+e3> non-normal" "<e2,e4> non-normal" "<e2,e3> non-normal" --tuples zero random --out $RD/B_conditional_2.json   # log: log_B_small2.txt
$P --mode B --names "<e2> non-normal" --tuples zero --cosets random --seed 11 --out $RD/B_symmetry_random_cosets.json   # log: log_B_sym.txt
$P --mode A --names "<e3,e4> = gamma_2" --nodes 0 --out $RD/A_gamma2_node0.json   # log: log_A_gamma2.txt
# --- queue q3
$P --mode relabel --out $RD/relabeling.json   # log: log_relabel.txt
$P --job n4_f7 --mode merge --out $RD/merge_proofs_f7.json   # log: log_merge_f7.txt
$P --job n4_f7 --mode relabel --out $RD/f7_relabeling.json   # log: log_f7_relabel.txt
$P --job n4_f7 --mode A --names trivial --nodes 0 --sources-only --out $RD/f7_sources_timing.json   # log: log_f7_src_timing.txt
$P --mode heis --out $RD/heis_f3_reduction_check.json   # log: log_heis.txt
$P --mode neg --names "<e2> non-normal" --phase A --part 0 2 --out $RD/negative_controls_c3_phaseA_part0.json   # log: log_negA0.txt
# --- queue q4
$P --mode neg --names "<e2> non-normal" --phase A --part 1 2 --out $RD/negative_controls_c3_phaseA_part1.json   # log: log_negA1.txt
$P --mode A --names "<e1+e2,e3> (closure)" --nodes 0 --hub-range 0 5209 --out $RD/A_closure_node0_hubs_0_5209.json   # log: log_A_closure_r0.txt
$P --mode A --names "<e1+e2,e3> (closure)" --nodes 0 --hub-range 5209 10417 --out $RD/A_closure_node0_hubs_5209_10417.json   # log: log_A_closure_r1.txt
$P --mode A --names "<e1+e2,e3> (closure)" --nodes 0 --hub-range 10417 15625 --out $RD/A_closure_node0_hubs_10417_15625.json   # log: log_A_closure_r2.txt
# --- queue q5
$P --mode heis --out $RD/heis_f3_reduction_check.json   # log: log_heis.txt
$P --mode B --names trivial "Z(G)" "<e2> non-normal" --tuples zero random --out $RD/B_conditional_1.json   # log: log_B_small.txt
$P --mode B --names "<e2> non-normal" "Z(G)" --tuples zero --cosets random --seed 11 --out $RD/B_symmetry_random_cosets.json   # log: log_B_sym.txt
$P --mode B --names "<e3,e4> = gamma_2" --out $RD/B_gamma2_exact.json   # log: log_B_gamma2.txt
$P --mode B --names "<e3,e4> = gamma_2" --cosets random --seed 7 --out $RD/B_gamma2_exact_random_cosets.json   # log: log_B_gamma2_sym.txt
$P --mode B --names "<e1> non-normal" "<e1+e3> non-normal" "<e2,e4> non-normal" "<e2,e3> non-normal" --tuples zero random --out $RD/B_conditional_2.json   # log: log_B_small2.txt
$P --mode B --names "<e1+e2,e3> (closure)" --out $RD/B_closure_exact.json   # log: log_B_closure.txt
$P --mode neg --names "<e2> non-normal" --phase B --out $RD/negative_controls_c3_phaseB.json   # log: log_negB.txt
# --- queue q6
$P --mode heis --out $RD/heis_f3_reduction_check.json   # log: log_heis.txt
$P --job n4_f7 --mode A --nodes 0 1 2 3 4 5 --sources-only --out $RD/f7_sources_all_subgroups_all_nodes.json   # log: log_f7_sources.txt  (stopped by hand after 19 runs, before the fast left_coset_ids; the rest ran in q10)
$P --job n4_f7 --mode A --nodes 0 --sources-only --mutate-oracle --out $RD/f7_sources_oracle_mutant.json   # log: log_f7_sources_mut.txt
$P --job n4_f7 --mode A --names "Z(G)" --nodes 0 --out $RD/f7_A_ZG_node0.json   # log: log_f7_A_ZG.txt
$P --job n4_f7 --mode B --names "Z(G)" --tuples zero random --out $RD/f7_B_ZG_conditional.json   # log: log_f7_B_ZG.txt
# --- queue q7a
$P --mode B --names trivial "<e2> non-normal" "<e1> non-normal" "<e1+e3> non-normal" --tuples random --n-random 10 --seed 1 --out $RD/B_conditional_more_random_1.json   # log: log_B_more1.txt
# --- queue q7b
$P --mode B --names "Z(G)" "<e2,e4> non-normal" "<e2,e3> non-normal" --tuples random --n-random 10 --seed 1 --out $RD/B_conditional_more_random_2.json   # log: log_B_more2.txt
# --- queue q8 (conditional: skipped, A_e2e3_node0.json had passed)
# $P --mode A --names "<e2,e3> non-normal" --nodes 0 --hub-range 0 130209 --out $RD/A_e2e3_node0_hubs_0_130209.json   # log: log_A_e2e3_r0.txt
# $P --mode A --names "<e2,e3> non-normal" --nodes 0 --hub-range 130209 260417 --out $RD/A_e2e3_node0_hubs_130209_260417.json   # log: log_A_e2e3_r1.txt
# $P --mode A --names "<e2,e3> non-normal" --nodes 0 --hub-range 260417 390625 --out $RD/A_e2e3_node0_hubs_260417_390625.json   # log: log_A_e2e3_r2.txt
# --- queue q9
$P --mode neg --names "<e2> non-normal" --phase B --tuples random --seed 0 --out $RD/negative_controls_c3_phaseB_random_tuple.json   # log: log_negB_random_tuple.txt
# --- queue q10
$P --job n4_f7 --mode A --names trivial "Z(G)" "<e2,e3> non-normal" "<e3,e4> = gamma_2" "<e1+e2,e3> (closure)" --nodes 0 1 2 3 4 5 --sources-only --out $RD/f7_sources_part2.json   # log: log_f7_sources2.txt
$P --job n4_f7 --mode A --names "<e2,e4> non-normal" --nodes 1 2 3 4 5 --sources-only --out $RD/f7_sources_part3.json   # log: log_f7_sources3.txt
# --- queue q11
$P --mode relabel --out $RD/relabeling.json   # log: log_relabel.txt
$P --job n4_f7 --mode relabel --out $RD/f7_relabeling.json   # log: log_f7_relabel.txt
$P --mode A --names trivial "Z(G)" --nodes 0 --direct-gram --out $RD/A_direct_gram_trivial_ZG_node0.json   # log: log_A_direct_gram.txt
# --- after the review: combine the three hub ranges of <e1+e2,e3> (theorems.rees_circuit_mono_c3.combine_hub_ranges)
#   -> $RD/closure_hub_ranges_combined.json
# --- tests (one process, nice -n 10)
# PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py tests/test_rees_circuit_round2.py tests/test_rees_circuit_round3.py   # -> pytest_final.txt
# REES_SLOW=1 ... -m pytest -q -p no:cacheprovider tests/test_rees_circuit_round3.py -k "phase_a_trivial or g_sign or gamma2_exact"   # -> pytest_slow_round3.txt
