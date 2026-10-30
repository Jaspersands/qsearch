# Verification

2026-10-25. Isolated exact arithmetic and proof-scope audit.

## Executed

Working directory: this bundle. Interpreter: `/opt/anaconda3/bin/python`.

    python -B -W error -m pytest -q -p no:cacheprovider \
        test_bridge_controls.py \
        ../rees-class-three-2026-10-24/test_class_three.py

**62 passed**, warnings treated as errors, no skips: 45 new bridge tests
and 17 existing class-three controls. Final combined run: 1.44 seconds.
An initial FLINT tuple/list conversion error was corrected before the
passing runs. A prior partial run is not counted as verification.

Three Python sources pass syntax checks using `compile(source,path,'exec')`
without writing bytecode. `replay.py --output receipt.json` produces the
live exact report. A separate invocation recomputes it and checks full
JSON equality, including five source hashes and five dependency hashes.
The receipt SHA256 is recorded in the external research checkpoint.
All four source hashes in the frozen class-three receipt still match.

The source-hashed receipt includes:

- Seven parameter examples, always keeping class and rank costs explicit.
- Exhaustive scalar null-polynomial checks for six prime-power moduli.
- The exact ramified p=3,q=9,n=1 ring and character pairing.
- Newton dilation leakage and a nontrivial unipotent action, including
  six prime controls of the general I+E_(1,p) identity.
- Different original secrets that collapse under coefficient reduction
  mod 3 but have phase-state fidelity exactly 1/3.
- Three exhaustive normalizer checks on the original 243-element group.

The general statements are written proofs in CYCLOTOMIC_BRIDGE.md, not
inferences from these finite tests. In particular, the all-prime unipotent
argument uses the characteristic-p generating-function identity, not a
scaling fit or an exhaustive enumeration of primes.

## Not Executed Or Established

No native secret-recovery solver, new sieve, quantum circuit, geometric
oracle, classical hardness proof, novelty certification, formal proof
assistant build, or independent review of these new deductions.
No claim of an LWE consequence. The published paper has not been audited
in its entirety; the comparison concerns its native source and the
specific proposed transfer of the existing Rees receiver.

No main-repository tests, `qsearch.py validate`, UI syntax check, CLI run,
registry update, commit or push. The intended verified Developer checkout
is still absent, and the original Desktop checkout is protected during
migration. Nothing in this pass changes prior reviewer conclusions or
the frozen Rees proof files.

Seven new bundle files plus an external checkpoint update. All owned
verification subprocesses completed; no background search was launched.
