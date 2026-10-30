# Verification

2026-10-23, `/opt/anaconda3/bin/python`, isolated local research workspace.

- New scalar/controller suite: **65 passed in 0.67s**.
- Existing central-rank suite, separate process: **32 passed in 0.05s**.
- Existing reference-safe Rees-channel suite, separate process:
  **12 passed in 0.80s**.
- `py_compile` passed for all four new Python files.
- `replay_scalar.py --write` generated nine live matrix controls.
- A separate read of the saved receipt verified all **seven source hashes**
  and all **nine moment witnesses against their original matrices**.

Tests disable pytest plugin autoload and cache writes; Python bytecode is
redirected to `/tmp/qsearch-scalar-pycache`. No moving source or staging
file was edited, and no Git commit or push was made.

The first integration run had 62 passes and one expected-contract mismatch:
the fixture requested degree 9 over F7, outside the existing degree<p
receiver contract. The fixture was corrected to F13 and the F7 case kept
as an explicit rejection test. No acceptance guard was relaxed.

## Verified Scope

Exact scalar/root arithmetic, original-equation cancellation, public-rank
accounting, capped-failure behavior, malformed-input rejection, and the
existing finite central-channel controls. The large-prime replays scan zero
field elements. Small fields are explicitly counted and degree-bounded.

The seeded tests do not establish the IID random-source premise. The
probability/runtime argument is in `SCALAR_CANCELLATION.md` and has not had
independent specialist review or proof-assistant verification.

No quantum source, complete receiver, natural hard instance, full repository
tests, qsearch CLI validation, JavaScript check, registry integration, or UI
refresh was run. Those repository operations are deferred until the ongoing
migration is verified and the handoff is integrated. The isolated code has
no JavaScript and makes no UI/CLI compatibility claim.
