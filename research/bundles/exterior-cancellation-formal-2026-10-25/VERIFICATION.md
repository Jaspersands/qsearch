# Verification Record

2026-10-25. Final commands completed successfully; no subprocess remains
from this pass. Compilation used the existing pinned sibling runtime,
with outputs only in this new bundle's `.build` directory.

## Final Commands

From exterior-cancellation-formal-2026-10-25:

```sh
/opt/anaconda3/bin/python -m pytest -q -W error test_verify.py
/opt/anaconda3/bin/python -m py_compile verify.py test_verify.py
/opt/anaconda3/bin/python verify.py --write
/opt/anaconda3/bin/python verify.py --check
```

- 24 verifier tests PASS. These exercise axiom-audit completeness, duplicate
  and unknown records, unsupported axioms including sorryAx, diagnostics,
  declaration-manifest mutations, exact source hashes and prior-source
  tampering. They are not independent tests of Lean's kernel.
- Two Python syntax checks PASS.
- Both final proof rebuilds PASS with no warnings or other compile
  diagnostics. All 21 theorems and eight definitions/abbreviations audited.
  The complete dependency union is propext, Classical.choice, Quot.sound.
- Lean 4.35.0, release commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc.
- mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679; clean source checkout.
- Deterministic receipt SHA256:
  5f6f8a97e5de2ce8b91a15d2607cdaf1fa5bfd6112a58f9334ba341a098d6c97.

From exterior-cancellation-2026-10-25:

```sh
/opt/anaconda3/bin/python -m pytest -q -W error test_exterior_sde.py
/opt/anaconda3/bin/python replay.py --check
```

- All 56 existing arithmetic tests PASS, 9.06 seconds for the test suite.
- The complete deterministic nine-case replay matches the unchanged prior
  receipt, including forced full accumulation and 127/128-bit prime cases.
- Unchanged arithmetic receipt SHA256:
  8e2f31784c0642fbac6a9370b43ba130533f6daecd379730da0a4bf7de9bec55.

Earlier Lean elaboration failures and one deprecated API were repaired;
the final source was rebuilt and audited afterward. No failed attempt is
treated as a verified result. No arithmetic source or prior receipt changed.

## Exact Scope

New: actual exterior-algebra coordinate recovery, kernel dimension,
multi-row dependence existence, right-wedge closedness preservation,
top-degree vanishing, and two missing-assumption counterexamples.

Not established: the original-leaf support induction in Lean, Python
refinement, full solver correctness in Lean, runtime/probability bounds,
novelty, a native source reduction, or an end-to-end quantum speedup.

No new independent reviewer was used. The previous authorized Rees review
does not extend to this new proof. No main/staging/Git/CLI/UI/registry or
migration edits; no commits or pushes. Main repository validation and its
full test suite were NOT run. See FORMAL_SCOPE.md for the trust boundary.
