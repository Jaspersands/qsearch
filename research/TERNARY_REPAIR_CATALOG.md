# Native Repair Catalogs And Collision Mass

LOCAL DERIVATIONS / REVIEW PENDING. This is a classical decoder-family test,
not a new algorithm, asymptotic no-go, native-source dequantization or accepted
candidate. Read `TERNARY_PAIR_CELL_COVERAGE.md` for the exact repair predicate.

## Implemented Mechanism

`theorems/ternary_repair_catalog.py` verifies the complete original kernel and
the actual Gram-Schmidt directions of saved public bases. Earlier-row
orthogonality and the reciprocal projection coefficient alone are insufficient:
adding a later orthogonal direction can pass those checks. Actual prefix-span
reconstruction is now independently checked, with an adversarial regression.

Training uses 512 independent publicly generated known words per label set.
There is no target, incoming quantum word, unknown phase or secret in training.
Each word determines its exact forced nearest-plane repair pattern. Catalogs
retain the most frequent patterns, reserve a charged ordinary Babai slot, and
use per-chart budgets 16, 64 and 256. Two saved bases and three centers give six
charts. Held-out evaluation uses 256 different words, then actual decoding uses
eight independent uniform targets for each of 15 saved label sets. The target
decoder uses the 64-pattern budget, verifies the original shell/congruence and
requires distinct witnesses. Every fresh-label attempt owes training and both
original LLL preparations; replaying a saved basis is not free physical reuse.

## Proven Conditional Bounds

For a fixed chart, let p_e be its true uniform-word repair-pattern distribution,
C=sum_e p_e^2 and S a target-independent catalog with at most K patterns.
Cauchy gives

```text
gamma_chart=sum_{e in S}p_e <= sqrt(K*C).
gamma_union <= min(1,sum_chart sqrt(K_chart*C_chart)).
beta_label <= gamma_union/6 at Q=3^(M+1).
```

These statements require neither independent GS errors nor independent charts.
They hold after choosing a catalog from public training, but do not constrain
target-dependent pattern generation. Exact small-source censuses compute true
collision mass and pair bucket coverage, separately charged as exponential
analysis and never supplied to training.

Collision statistics use 256 DISJOINT word pairs, not 512*511/2 fictitiously
independent comparisons. Exact rational one-sided binomial endpoints and a
Bonferroni bound across all 90 charts give conditional failure probability at
most 1/20, assuming IID words and fixed charts. The resulting union word-mass
upper bounds are all 1: statistically valid but uninformative. Zero observed
collisions is not zero true collision mass or an asymptotic entropy theorem.

## Live Evidence

The live report is `phase_workbench/ternary_repair_catalog.json`.

| Root digits | Held-out word recall at K64, out of 768 | Pairs in 24 targets |
| --- | ---: | ---: |
| 8 | 768 | 2 |
| 12 | 735 | 1 |
| 16 | 529 | 0 |
| 24 | 5 | 0 |
| 32 | 0 | 0 |

K256 recovers only one of 768 held-out words at root32. Targets share their
label set in groups of eight: these are conditional batches, NOT 120
independent fresh-label population trials. Held-out words are planted geometry
diagnostics, NOT uniform-target pair trials. Finite deterioration disfavors
this recorded policy; it does not rule out every polynomial-size catalog.

Run locally:

```sh
python theorems/ternary_repair_catalog.py --write
python -m pytest -q tests/test_ternary_repair_catalog.py
node research/certificates/ternary_repair_catalog_crosscheck.js
```

The independent BigInt checker replays all 120 actual target outcomes and
39,864 candidate decodes, including exhausted paths, duplicate outputs, basis
coefficients, fresh-label costs and 90 binomial endpoints. It does not replay
Python PRNG training, rerun LLL or independently repeat the exponential catalog
census. The separate native-cell checker validates source geometry/moments.

## Falsification And Next Decision

A fixed-catalog population obstruction would need a theorem bounding true C as
dimension grows; the present confidence bounds do not supply one. A positive
claim needs costed population pair coverage, not high small-width word recall.
The best immediate escape is target-adaptive branching with exact native
constraints, implemented separately in `TERNARY_ADAPTIVE_SHELL.md`. Do not
promote a candidate or erase the receiver's reduction/runtime obligations.
