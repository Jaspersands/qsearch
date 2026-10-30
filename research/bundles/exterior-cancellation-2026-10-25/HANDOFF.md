# Exterior Cancellation Handoff

This isolated bundle was developed while the main Desktop checkout remained
migration-sensitive. It does not modify the main CLI, registry, UI or Git.
Do not copy it into a moving source/staging checkout. First verify that
the real migration has completed and the intended repository is local.

## What Is Implemented

`exterior_sde.py` implements the standalone public-label problem
sum s_i^k v_i=0 over an odd prime field, 1<=k<p, with a nonzero witness.
It reduces to d=gcd(k,p-1), compresses an Ivanyos-Santha-style collision
to exterior powers, handles even-degree signs by explicit accumulation,
and verifies the original moment after lifting. No hidden information,
field-size enumeration on the large-field path, or resampled labels.

The local proof and scope are in EXTERIOR_CANCELLATION.md. The method is
unreviewed and its novelty is unverified. The earlier independent Rees
review does not cover this new arithmetic argument. The finite examples
are proof controls, not new algorithm candidates or quantum executions.

## Mechanical Integration, After Mathematical Review

1. Port the arithmetic and tests into theorems/tests with imports adapted.
   Keep this frozen bundle and its receipt as provenance.
2. Retain the existing all-odd-prime specialized quadratic solver. Retain
   linear dispatch when gcd(k,p-1)=1. Do not make the generic accumulation
   path a regression for those cases.
3. For genuine d>=3, compare verified PUBLIC bank sizes, not observed
   favorable matrix rank. Update the public plan before sources are
   acquired. Keep old tensor implementation as a diagnostic until the
   new invariant receives independent scrutiny, not as duplicate production
   research infrastructure indefinitely.
4. Connect the public higher-degree dispatcher for d>3. Every rejected
   plan, exhausted sampling cap or arithmetic error must stay an abort,
   not a reason to resample favorable quantum labels. Root timing is a
   separate unresolved obligation from the explicit sampling caps.
5. Preserve one weight per acquired slot. Account for zero-scale discards,
   unused suffixes, repeated rounds, upstream source preparation and final
   tomography/Fourier repetitions in the existing ledger.
6. Run a genuine grade-four/vector-center complete-instrument control.
   Check Pi*rho*Pi and positive branch probabilities, not just a scalar
   zero sum. Confirm the quotient state including zero labels and empty
   sectors. Do not construct a new oracle candidate to advertise this test.
7. Run affected tests, repository validation, syntax checks, and live
   affected workflows. Record the precise scope; this isolated pass did
   not run the entire main repository suite.

## Research Work, Not A Wiring Task

The important open question is the native input source/reduction, not the
constant in the public cubic bank. The general backend removes a missing
arithmetic implementation for higher-index degrees; it does not make
growing nilpotency class polynomial, solve DHSP, or defeat known classical
attacks on explicit sources. Do not spend a pass extending scalar seed
tables. Challenge the exterior lemma or apply the verified backend to a
receiver obligation that was genuinely inaccessible before.

## Reproduce Locally

From this bundle, using a Python with python-flint and pytest:

```sh
python -m pytest -q -W error test_exterior_sde.py
python -m py_compile exterior_sde.py test_exterior_sde.py replay.py
python replay.py --write
python replay.py --check
```

`--write` regenerates only this bundle's receipt. The receipt records full
public bank counts, deterministic input hashes, sparse exact witnesses,
node checks, the original-degree residual and root timing limitations.
Seeded replay is not an estimate of real random failure probability.
