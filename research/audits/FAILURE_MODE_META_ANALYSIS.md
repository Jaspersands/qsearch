# Failure-Mode Meta-Analysis

Generated 2026-10-19 by `tools/audit/failure_modes.py`; do not edit by hand.
Scope: the 976 records in `research/registry/negative_results.json`. Each record gets one primary failure mode, the step at which
the proposal died. Judge labels come from in-session subagents reading claim, reason and lesson;
records without a judge label fall back to the keyword rules.

Labels by source: 976 judge, 0 rule.

## Where proposals die

| Failure mode | Records | Share | Definition |
|---|---|---|---|
| Classical competitor | 311 | 32% | A classical algorithm, invariant or canonicalization solves the instance, separates the pair, or matches the quantum route. |
| Proof gap | 149 | 15% | A required theorem, reduction, bound or certificate is missing or does not follow from what was shown. |
| No signal | 116 | 12% | The quantum state or observable carries no usable information: labels stay uniform, bias or correlation is zero or negligible, the channel is the identity or the state maximally mixed. |
| Readout | 95 | 10% | Information is present but extracting it costs too much: the needed measurement (Helstrom, PGM, collective) is not efficiently implementable or needs exponentially many copies. |
| Overbroad claim | 73 | 7% | The claim says more than the evidence covers: one case generalized to a family, a scoped barrier stated as universal, or a mismatched model. |
| Finite-size evidence | 66 | 7% | Evidence comes only from small or finite instances, with no scaling law or uniform statement. |
| Resource blow-up | 65 | 7% | The proposed route itself needs exponential time, memory, enumeration, precision or bit length. |
| Hidden advice or oracle | 62 | 6% | The speedup relies on an uncharged oracle, planted secret, toy promise or artificial family rather than a natural input. |
| State preparation and access | 30 | 3% | The input state, source superposition or access model cannot be prepared or accessed efficiently, or covers negligible source mass. |
| Unclear | 9 | 1% | The record does not say enough to tell where the proposal died. |

## By track

| Track | Records | Top mode | Second | Third |
|---|---|---|---|---|
| Code equivalence | 457 | Classical competitor 45% | Proof gap 19% | Overbroad claim 8% |
| Coset observables / nonabelian HSP | 255 | Classical competitor 27% | Readout 18% | No signal 17% |
| Dihedral coset / hidden shift | 154 | Resource blow-up 18% | No signal 16% | Proof gap 13% |
| Legacy toy oracles | 53 | Hidden advice or oracle 100% |  |  |
| Query lower bounds | 22 | Classical competitor 55% | No signal 41% | Resource blow-up 5% |
| Other | 17 | No signal 35% | Proof gap 24% | Readout 12% |
| Applied-QC barriers from the literature | 10 | Classical competitor 50% | Readout 40% | No signal 10% |
| Lattices | 7 | Finite-size evidence 43% | Resource blow-up 14% | Proof gap 14% |
| DQI / OPI / prime characters | 1 | Proof gap 100% |  |  |

## Over time

Period is the month a record first appeared in the committed registry (from git history). The earliest
period also holds every record that was already present when the registry was first committed.

| Period | Records | Classical competitor | Proof gap | No signal | Readout | Overbroad claim | Finite-size evidence |
|---|---|---|---|---|---|---|---|
| 2026-07 | 525 | 48% | 7% | 9% | 6% | 4% | 7% |
| 2026-08 | 298 | 13% | 31% | 9% | 13% | 13% | 8% |
| 2026-09 | 110 | 0% | 18% | 26% | 19% | 13% | 7% |
| 2026-10 | 43 | 40% | 0% | 30% | 16% | 0% | 0% |

## How far to trust the labels

Keyword rules against judge labels on 976 records: primary mode agrees on 49%, and the rule's mode is among the judge's primary or secondary modes on 58% (Cohen's kappa 0.40).

| Mode | Rule precision | Rule recall | Judge support |
|---|---|---|---|
| Classical competitor | 87% | 85% | 311 |
| Proof gap | 30% | 14% | 149 |
| No signal | 54% | 17% | 116 |
| Readout | 34% | 49% | 95 |
| Overbroad claim | 20% | 1% | 73 |
| Finite-size evidence | 23% | 55% | 66 |
| Resource blow-up | 41% | 37% | 65 |
| Hidden advice or oracle | 85% | 89% | 62 |
| State preparation and access | 11% | 7% | 30 |
| Unclear | 3% | 44% | 9 |

Use the rules for triage of new records only where precision is high; the judge labels are the ones the distribution above rests on.

A second judge, the same model in a fresh context, relabeled 150 groups (214 records). Its primary mode matches the first judge's on 84% of the groups and falls within the first judge's primary or secondary modes on 91% (kappa 0.81). This measures how repeatable one model's labels are; it is not a second expert's opinion.

## Pre-filters

One check per failure mode, most frequent first. Running the check before a proposal is built would have
stopped the records counted here at the cheapest point.

**Classical competitor** (311 records). Run the track's standard classical attacks (canonicalization, refinement or WL, support splitting, LLL, dynamic programming, norm constructions) on the exact instance before building a quantum observable.
- `AFFINE-GEOMETRY-CODE-SEARCH-AG2_F2_K3`: "Affine-geometry collisions found so far are affine-linear or canonical controls."
- `AFFINE-GEOMETRY-CODE-SEARCH-AG2_F3_K6`: "Affine-geometry collisions found so far are affine-linear or canonical controls."

**Proof gap** (149 records). List the lemmas the claim needs and mark which are proved; promote nothing with an open lemma on the critical path.
- `ASYMPTOTIC-CARRIER-CONTEXTUALITY-NOT-QUANTUM-ALGORITHM`: "The theorem supplies no efficient coherent Racah resolver, PGM, hidden-involution decoder, or classical separation."
- `BOUNDED-COVARIANCE-LCU-NOT-INVERSE-SQRT-GAP`: "QSVT degree also depends on the minimum retained positive eigenvalue, for which no all-n lower bound is proved."

**No signal** (116 records). Compute the one-copy and few-copy bias or mutual information of the proposed observable on a small instance; a zero or exponentially small value ends the proposal.
- `ADAPTIVE-PALETTE-CATALOGUE-NOT-FREE-ESCAPE`: "The S1024 two-palette control gives T <= 2^-601."
- `CARRIER-CONTEXTUALITY-NOT-HIDDEN-INVOLUTION-IDENTITY-SIGNAL`: "its distribution is identical for every involution in the fixed cycle-type conjugacy class."

**Readout** (95 records). Name the measurement with its gate and copy count before claiming a success probability; compare it against product and local Helstrom readout.
- `AFFINE-NODE-NORMALIZED-FRAME-QSVT-NO-NATURAL-RESPONSE`: "the full-sibling native mass and rank above every inverse-polynomial eigenvalue of Fbar_s vanish"
- `CARRIER-HOLEVO-RETENTION-NOT-ACCESSIBLE-INFORMATION`: "Holevo information is an upper bound on accessible information and may be locked"

**Overbroad claim** (73 records). Write the claim's exact scope (family, model, parameters) next to the evidence's scope and cut the claim to the intersection.
- `CARRIER-ANGLE-WORST-SECTOR-N-MINUS-ONE-PATTERN-FALSE`: "Use natural weighted rank expansion, not worst-sector small-n extrapolation."
- `CARRIER-INVARIANCE-NOT-A-BINARY-NO-GO`: "The two tasks have different priors and alternatives."

**Finite-size evidence** (66 records). Fix the growing family and the asymptotic statement before running finite scans; treat finite scans as falsifiers, not evidence.
- `FINITE-CARRIER-BRANCH-SUCCESS-NOT-ALL-N-DECODER`: "no all-n distinct-collision bound, coherent branch PGM implementation, outcome decoder, or classical separation has been proved"
- `FINITE-CARRIER-CONTEXTUALITY-TREND-NOT-ASYMPTOTIC-NO-GO`: "The samples have finite Hoeffding intervals but no uniform all-n character or centralizer bound."

**Resource blow-up** (65 records). Count the route's own time, memory and precision as a function of n, including classical pre- and post-processing.
- `AFFINE-FLAG-ADDRESSED-LOCAL-KERNELS-NO-POLYLOG-AGGREGATE-SCHUR-COMPILER`: "BBBV forces Omega(sqrt(q)) addressed queries."
- `BOUNDED-PAIR-LCU-MEAN-NOT-THRESHOLD-COMPOSABLE`: "a typical pair still costs approximately four, or two per source copy"

**Hidden advice or oracle** (62 records). State the access model and charge every oracle call; reject families whose hardness comes from a planted secret or masking.
- `LEGACY-BERNSTEIN_VAZIRANI`: "arbitrary oracle_secret_finding proposal; N=3 simulation cap"
- `LEGACY-BITWISEMAJORITYSECRETFINDING`: "arbitrary oracle_secret_finding proposal; N=3 simulation cap; claimed speedup despite zero simulation success"

**State preparation and access** (30 records). Write down the state-preparation circuit and the fraction of natural source mass it covers before analysing the readout.
- `DCP-CANONICAL-WITNESS-RATE-NOT-PAIRING-MASS`: "heralded mass is at most N/2^m even at witness rate one"
- `FAITHFUL-SIGNED-TENSOR-DIAGRAM-RANGE-MISSES-TYPICAL-SOURCE`: "degrees at most m cover exponentially vanishing necessary K-type mass under the h-even marginal."
