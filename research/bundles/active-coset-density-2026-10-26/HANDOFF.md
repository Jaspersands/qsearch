# Handoff: Separate Coset Density From Within-Coset Success

Read ACTIVE_COSETS.md. This is a new, NOT independently reviewed counting
argument for the existing classical attack, not a replacement quantum
candidate or an implemented native source.

For the specified uniform-beta sampler with fixed source frame, odd index
d, and coprime converter, a coset containing any useful query has at least
a 1/3 fraction of useful queries. The missing success theorem is therefore
precisely a uniform lower bound on the fraction of active cosets. It is NOT
established by the conditional 1/3 bound.

For the special Pell frame, exactly d-1 of the d queries in the integral
coset H succeed. That contribution is (d-1)/d^4 under uniform native beta,
and native isogeny division already gives exactly the same successes.
The arithmetic p=11,index17 fixture is Bass and uses supplied full-order
coordinates. It is not a hard native instance or a native sampling run.

## Next Research Pass

Investigate active NONINTEGRAL cosets for this explicit sampler. Preserve
the complete-group criterion, fixed frame, and native provenance. Do not
repeat an integral-coset sweep: its entire behavior is now classified and
matched classically. Do not infer full dequantization from conditional
success or classical hardness from a particular inactive source.

The source has inherited copy symmetries. Their size is not a useful-hit
metric; actual entries outside the current order are necessary. For any
proposed hitting argument, account for every adaptively reached order,
one sampler, one polynomial and the original native input length. A bare
existence claim or an unknown-O interpolation stencil is not sufficient.

## Mechanical Integration, Only After The Checkout Is Safe

Gemini may transplant the two small Python files into the existing exact
arithmetic test layout. coset_controls.py has no native automorphism,
sampling, division or registry interface. Keep it a test adapter. The
unit-i generator routine is complete ONLY for the checked p=11 fixture,
not for arbitrary quaternion orders. No new CLI/framework is needed.

Future ACTUAL native runs should distinguish total uniform queries,
division-detected successes, and extra geometric successes on nonintegral
queries. Never use the supplied hidden translates to populate native
result or success-rate fields. Do not rewrite the preserved historical
additive or harvest receipts; link this later extension separately.

Reproduction commands and exact scope are in VERIFICATION.md. The main
local checkout remained absent; no moving source, staging directory,
CLI, registry, UI or Git was changed. No new reviewer was used.
