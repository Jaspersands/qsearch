# Local dfs2b queue: final results, witness checks and reconciliation (10 Nov 2026)

AI-written, AI-checked only. No human has read it. These are finite computations, and nothing
here is a proof. No dfs2b run was started for this report. Every run cited had finished, and no
dfs2b process was running when the files were read. Scripts and outputs are in
`2026-11-10-rees-dfs2b-queue-final/`. The paper is not edited here; the prepared update is in
`2026-11-09-rees-paper-pass-prep/` (section 1h of its README).

## 1. The queue

`2026-11-07-rees-dfs2b-local-queue/` holds the local run of the 11-06 other-device brief:
- `queue.orig.txt` lists the 143 jobs originally planned.
- `queue.txt` lists the 99 that ran.
- `run.sh` uses the canonical `small-prime/dfs2b` with node limit 10^15.

All 99 output files have a DONE line, and none has a LIMIT or BUG line.

| part | jobs | result |
|---|---|---|
| κ = 8, plain mode, members 7649–10753 | 47 | 47 INFEASIBLE (same verdicts as the pruned search) |
| κ = 9, plain mode, 13807 and 14149 | 2 | 2 INFEASIBLE (same verdicts) |
| κ = 9, pruned (`print`), sweep exceptions 21871–24967 | 50 | 45 INFEASIBLE, 5 FEASIBLE: 21871, 22051, 22303, 23671, 24841 |

## 2. Reconciliation of the 44 jobs not run locally

`queue.orig.txt` minus `queue.txt` is 44 jobs. **None is missing.** Every one has a verdict in
`2026-11-07-rees-cloud-late-results.txt`. That file holds verdict lines collected on 7 Nov from
cloud sessions running the same program; it gives the comment-stripped source md5 244a31ed…, and
that session's node counts match local runs exactly where both exist.

| jobs | where the result is | verdict |
|---|---|---|
| κ = 9 plain, 36 primes 11701, 11719, …, 13933 | late cloud file, session E | 36 INFEASIBLE, agreeing with the local pruned verdicts |
| κ = 9 pruned, 8 exceptions 21313, 21493, 21529, 21601, 21673, 21727, 21799, 21817 | late cloud file, session C | 8 INFEASIBLE; **cloud only**, with no local run |

The late cloud file has verdict lines but no DONE lines. The eight session-C verdicts are the
only E_2 verdicts below 25000 that rest on a single cloud run. The cloud brief
`2026-11-09-rees-dfs2b-cloud-plain-brief.md` (shards S1–S3) covers κ = 9 13807 and 14149 and
the κ = 8 plain jobs 7649–10753. All of these were also run locally, so the brief adds nothing
beyond the local queue. One more record does not reconcile. The 11-05 batch summary
(`2026-11-05-rees-cloud-batch-results.md`) mentions a κ = 9 non-member 304687, but no verdict line
or witness for it was found in the repository. It is not used.

## 3. Witness verification

`verify_witness.py` was written for this report from the definition in the Schedule 2 appendix
(subsection *Two-level contractions*) and shares no code with `dfs2b.c`. For each line
(κ, p, g, β, α) it checks the following, exactly:
1. p is prime and p ≡ 1 (mod κ).
2. g^((p−1)/κ) has order exactly κ, so g is a coset generator.
3. C_ij = g^i g^j (α_j + β_i) is 0 or a κ-th power for every i, j, and C_00 ≠ 0.
4. Σ C_ij X_ij = 0 for every X in W ⊗ W, with W = {w : Σ_m g^m w_m = 0}. This is tested on a
   basis of W ⊗ W, so it does not use the normal-form lemma.

| set | lines | primes | bad |
|---|---|---|---|
| every FEASIBLE line with a witness, κ = 8, 9, all sources | 530 | 328 | **0** |
| the five new queue witnesses (21871, 22051, 22303, 23671, 24841) | 5 | 5 | **0** |

`verify_witness.gp` is a second, independent check in PARI/GP 2.17 (env `qsearch-cas`). It covers
the six κ = 9 non-members above 20000: the five queue primes and 21187. It checks `isprime`,
`znorder(Mod(g,p)^((p-1)/9)) == 9`, `ispower(C[i,j], 9)` for each nonzero cell, and
`B~*C*B == 0` for a `matker` basis B of W. All six pass. Each g is in fact a primitive root
(`znorder(Mod(g,p)) = p−1`). In both programs, a negative control (α_1 + 1) is rejected.

| p | g | factorisation of p − 1 | verdict |
|---|---|---|---|
| 21187 | 2 | 2·3²·11·107 | contraction, checked |
| 21871 | 6 | 2·3⁷·5 | contraction, checked |
| 22051 | 3 | 2·3²·5²·7² | contraction, checked |
| 22303 | 6 | 2·3³·7·59 | contraction, checked |
| 23671 | 3 | 2·3²·5·263 | contraction, checked |
| 24841 | 14 | 2³·3³·5·23 | contraction, checked |

An INFEASIBLE verdict has no certificate and cannot be checked this way. It rests on a complete
run of the pruned search, whose prunes are proved in `2026-11-03-rees-dfs2-prune.md`, and for the
members listed in section 4 also on an unpruned or plain-mode re-run.

## 4. Final counts

`collect.py` (output `collect.out`) reads every FEASIBLE, INFEASIBLE and LIMIT line for κ = 8, 9
in four places: `2026-11-02-rees-schedules/small-prime/*.out`, `2026-11-04-rees-k9-sweep/out/dfs*.out`,
the local queue, and the late cloud file. Runs stopped by the node limit are ignored. No prime
has both verdicts.

| | κ = 8 | κ = 9 |
|---|---|---|
| primes p ≡ 1 (mod κ) up to 20000 | 556, all decided | 372, all decided |
| members of E_2(κ) up to 20000 | 293, largest 14281 = 1.2327·8^{4.5} | 342, largest 19963 = 0.3381·9^5 |
| above 20000 | E_2(8) ∩ (20000, T_A(8)] = ∅ by the explicit contraction sweeps | 1373 sweep exceptions in (20000, 9^9/2]: the 78 below 25000 decided, 72 members (largest 24967 = 0.4228·9^5) and 6 non-members; 1295 above 25000 undecided |
| status | **E_2(8) determined**: 293 primes, max 14281 | E_2(9) ∩ [3, 25000] determined (414 primes); E_2(9) and its maximum **not determined** (1295 open exceptions; (9^9/2, T_A(9)] not covered) |

The older counts still in the text agree with the final data (`consistency.out`):
- 82 of the 83 primes below 2442 (κ = 8) and below 3584 (κ = 9) are members.
- Below 4202 and 5690 there are 137 and 122 primes, with 5 and 4 feasible.

Cross-checks against records (`crosscheck_records.py`, output `crosscheck_records.out`):
- The constraint solver of `2026-11-04-rees-cloud-e2k8low.md` agrees with the final verdicts at
  all of the 145 κ = 8 primes in (9769, 20000] that it decided (35 members, 110 non-members),
  with 0 conflicts.
- **Plain mode (unpruned order, no symmetry breaking).** Every member up to 10753 for κ = 8 (264
  primes) and up to 14149 for κ = 9 (254 primes) has a plain-mode or older unpruned verdict
  agreeing with the pruned one. The members in (7577, 10753] and (11593, 14149] are checked line
  by line here: 47 run locally, 36 in the late cloud file and 2 run locally. Below 7577 and 11593
  the record is the 11-05 batch summary for cloud sessions D and E ("166 of 213" and "174 of 211",
  contiguous through 7577 and 11593). Their verdict lines are not stored in the repository, so
  these 340 checks are recorded only as counts.

## 5. Claim gates and next step

These must stay false:
- no threshold of order κ^{(κ+1)/2} is proved;
- E_2(9) is not determined;
- nothing changes for κ ≥ 10;
- no gate in `research/reductions/rees_hsp_reduction.json` changes (file untouched).

The next hard question is E_2(9) above 25000. There are 1295 open exceptions up to 424549, and
dfs2b costs about p^5.6, so they cannot all be decided this way. The uncovered range
(9^9/2, T_A(9)] needs a sweep or a proved threshold.
