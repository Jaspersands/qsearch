# Next Decision: Joint Local/PSD Feasibility Versus Decoder Leverage

IMPLEMENTED. All37 selected native local inequalities plus full PSD admit an
exact continuation on the empty source prefix. The follow-up zero-LP
Boolean-event separator detects14 local failures in that new continuation.
Read `TERNARY_JOINT_REALIZABILITY.md`, `TERNARY_EVENT_TRIANGLES.md` and
`NATIVE_TERNARY_EVENT_FAMILY_TARGET.md`. The original specification below
is retained for proof review. Read `TERNARY_LOCAL_MARGINALS.md`. A real PSD relaxation
gap fails37 tiny local inequalities, but the base model with those inequalities
admits another exact indefinite continuation. The joint constraint set is
unknown. This diagnostic is secondary to finding the actual scalable native
two-witness mechanism; do not spend unlimited effort on one empty prefix.

## Bounded Joint Audit

Reconstruct the original target11366831/winding3 model, apply all37 certified
native-valid local cuts and independently replay the saved exact full primal.
Preserve nonnegative local slacks but NEVER make them indicators. Audit
original source/conditional/marginal/winding equations in every re-solve.

A bounded PSD separation loop may now be meaningful because this is a NEW
constraint system, not merely a larger budget for the earlier failed one.
Every exact square cut must have zero coefficients on all prior slack
variables. An exact final signed dual must include ALL local and PSD cut
rows/slack columns. A PSD continuation must have full original-coordinate
evidence; neither numerical optimality nor a cap proves feasibility/infeasibility.
If several joint-valid points are supplied to a convex search, recheck every
point against ALL37 local cuts first. Old positive mixtures violate those
cuts and cannot be silently reused.

Retain the complete branch scope: ONE fixed winding. Other windings and
prefixes remain unexamined; no new pair or source-law coverage is implied.

## What Would Justify Further Investment

- An exact joint continuation closes this diagnostic with a stronger finite
  gap. Do not automatically expand to fourth-order or growing-degree moments.
- A global dual at this winding justifies testing the constraint family on
  other actual prefixes, with total cost included, not declaring a solver.
- Continued numerical/bit-complexity failure is a reason to stop this
  selected-prefix exercise and reassess direct two-witness mechanisms.

The next strategically useful benchmark is whether cheap local inequalities
improve fresh-target native pair recovery at roots24/32 per charged work,
including moment construction, source/basis compilation, proposal cost and
exact certification. Compare against the existing ordinary native search;
do not select only prefixes whose emptiness is already known. Any classical
improvement is not a quantum speedup and must be treated as a dequantization
baseline, not algorithmic novelty.

No generic cut-budget inflation, favorable-lift choice, missing-row shortcut,
unreviewed theorem promotion, or legacy circuit search. Gemini owns routine
CLI/registry/UI wiring and production validation; GPT owns this mathematical
decision and rigorous targeted evidence.
