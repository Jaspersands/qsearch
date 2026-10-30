# Integration Handoff

Do not integrate into the moving Desktop checkout. Verify migration first.
This is an isolated research bundle, not a new accepted algorithm candidate.

1. Preserve the original all-one native input, including all 49 frozen
   evaluation points. Reuse the repository's native verifier on integration.
2. Port modular_norm.py only if a proposed PUBLIC carry-acquisition method
   needs it. Do not build a random-carry job or generic search UI around it.
3. The fixed_carry API requires W as EXTRA input. Expose that obligation in
   any registry record. Witness-derived W is correctness evidence only.
4. Preserve NO_SOLUTION_FOR_THIS_CARRY vs UNKNOWN_ORIENTATION_CAP. Neither
   is a negative result for the unrestricted native relation.
5. Record the written uniform-carry counting bound as a scoped falsifier,
   not native hardness, a quantum lower bound, or an independent theorem.
6. Keep mixed-target support, carry construction, independent review,
   novelty assessment and full-repository validation explicitly pending.

Reproduce locally with /opt/anaconda3/bin/python:

    python -B -W error -m pytest -q -p no:cacheprovider test_modular_norm.py
    python -B verify_modular_norm.py --check

The live receipt reuses a frozen previously verified witness. It does NOT
run a new seed search. --write regenerates only this bundle's receipt;
--check verifies equality without modifying it. Source/dependency hashes
include the frozen predecessor receipt. See VERIFICATION.md for the exact
checks completed, not an assumption that all repository tests were run.
