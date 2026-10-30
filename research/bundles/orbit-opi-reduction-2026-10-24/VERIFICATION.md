# Verification And Exact Scope

2026-10-24. All work is in this external local bundle. No original/staging
repository, main registry, CLI, UI or Git state was edited. No commits or
pushes were made. The intended main Developer checkout remained absent
when checked. The authorized independent Rees reviewer was not reused.

## Changed Files

- opi_reduction.py: exact native-to-scalar restriction, K-wise Bonferroni
  probability certificate, paid retries, partial/full witness lift.
- test_opi_reduction.py: 30 focused controls, including exhaustive algebra,
  limited-independence countercontrols and independent native replay.
- make_receipt.py: frozen input restrictions, bounded scalar witnesses,
  failed deterministic restriction, provenance and scope flags.
- REDUCTION.md: local proof, prior-art consequence, falsifiers and stop rule.
- HANDOFF.md: bounded future integration, not another discovery candidate.
- receipt.json: live materialized-list hashes, all sampled components,
  preimage counts, paid work, original inputs and small native witnesses.
- VERIFICATION.md: this evidence ledger.

The parent RESEARCH_CHECKPOINT_2026-10-23.md also received a new leading
entry. Prior research bundles and their hashed artifacts were not edited.

## Executed Checks

The focused suite passed **30 tests in9.24s**, warnings treated as errors.
The broad external research milestone passed **671 tests in15.46s**:
these30 plus the previous641. No skips. The suite includes the preceding
capacity, norm-flat/optimality, orbit decoder, Rees, BPQM, HDQI and central
rank Python controls. This is NOT the complete original repository suite
and is NOT a new Lean rebuild or independent mathematical review.

All three new Python files pass py_compile. The receipt was regenerated
twice and compared byte-for-byte; all8 source/dependency hashes matched.

    receipt SHA256:
    db85604c8f51215bda400f334a8fc795ec549783ea2c42c9abf91ca1aa1378aa

Reproduction from this bundle:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-opi-reduction-pycache \
      /opt/anaconda3/bin/python make_receipt.py --output receipt.json
    env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-opi-reduction-pycache \
      /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_opi_reduction.py

## Live Outcomes

Both runs use p2053,M684 and the SAME frozen original halfsets, multipliers,
nonsquare and ordered orbits. Algorithm seed271026, ell769, budget4.

| Native Dimension | Original n204 Preserved | Attempts | Preimage Sizes |
|---|---|---|---|
| 204, K68 | yes | 1 | 941 to1100 |
| 1314, K438 | NO, explicitly changed | 1 | 943 to1096 |

Each materialized instance contains684 lists of exactly769 elements.
Per run,1,404,252 native table lookups were charged. The lower dimension
used136 random field draws and93,024 Horner steps; the higher used876
draws and599,184 steps. Counts are named operations, not a full bit-time
or memory measurement. All input validation, serialization and replay also
take work. Neither run invoked a scalar OPI solver or produced a native P.

The fixed-input mathematical restriction-success lower bound is
approximately0.006631587817727274 for BOTH parameter choices. This is a
local unreviewed uniform-coin certificate, not inferred from the successful
seeded trials. The K438 rate plus retained density exceeds1, but the cited
quantum theorem's finite length threshold is NOT instantiated at M684.

The independent verifier evaluates P_fixed at the ORIGINAL three points,
then checks all possible constant additions t directly against the frozen
native tables. This replays all2,808,504 preimage bits across both runs,
without using the quadratic coefficients or vertex formula. Canonical
reduced-list hashes match:

    n204:  9de185141e9ee952540e3dd0d89cd95c83690dfcdfa628c1657384f105ac0ed1
    n1314: 094bd4e9abceb9bf74225bafba2855eaa6958106c7e0f492ae3b027909062915

Four p13,M4,K3 controls found scalar witnesses after218,1,714,351 bounded
coefficient trials and lifted them to4/4 native witnesses, independently
replayed. Exhaustive coefficient enumeration is not a scalable algorithm.
The frozen-zero-component counterexample has ALL reduced lists empty;
the recorded random restriction repairs its list sizes, without claiming
to solve that scalar or native instance.

## What Remains Unverified

- The new mathematical reduction needs independent review.
- The external scalar OPI theorem is a preprint dependency, not a project
  proof. Its concrete decoder, finite thresholds and coherent costs are
  not implemented here.
- No large native witness, classical dequantization, uniform sampler,
  natural-problem hardness reduction or quantum speedup was established.
- Main qsearch validation, Node syntax and whole-repository tests were not
  run against the incomplete/moving checkout. No claim of main integration.
- No process started for this pass was left running.

The research decision is to avoid wiring a custom cubic capacity receiver
as if its rate threshold were evidence of a new quantum mechanism. This
does not prove that every possible cubic-orbit idea is exhausted.
