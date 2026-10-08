# Native Prefix Integrality: Next Mathematical Target

IMPLEMENTED: see `TERNARY_PREFIX_INTEGRALITY.md` and its exact reports/checker.
The audit records 16 true fixed-winding false prefixes; the certified-LP
decoder still finds no larger-root witnesses. `TERNARY_PREFIX_MODULAR.md`
also supplies native modulo-two words on all 26 LP-feasible prefixes.
The next target is `NATIVE_TERNARY_COUPLED_MOMENTS_TARGET.md`.

Original specification follows. LOCAL DERIVATION / REVIEW PENDING. Do not simply increase
catalog sizes, sphere caps or dual iteration counts. Read the three current
native decoder notes and use their saved independent-uniform-target fixtures.

## Question That Changes The Next Action

At a genuinely unresolved partial coefficient branch, is the failure to prune
caused by weak separator search, or by an EXACT fractional continuation in the
native product simplex? In the latter case no assigned-span linear separator
can help. A discrete mechanism or different representation is required.

Use original one-hot coordinates u_j,v_j with u_j>=0,v_j>=0,u_j+v_j<=1.
The fractional native error is E(ones)-3E(u,v). For primitive assigned GS
directions w_i, i>=b, with H the actual partial integer residual, impose

```text
sum_j [(w_i[3j]-w_i[3j+1])*u_j
      +(w_i[3j]-w_i[3j+2])*v_j]
  = (<E(ones),w_i>-<H,w_i>)/3.
```

These are exact rational linear constraints, no hidden phase and no planted
target. Together with the block triangle inequalities they specify the
continuous prefix relaxation precisely. A fractional solution is a PRIMAL
certificate opposing any dual separator for this branch, not a native word.

## High-Value Implementation

1. Extract actual bounded-search/Babai prefixes, with assigned row boundary,
   full public basis, original target and integer coefficients. Never silently
   substitute the vacuous zero-assigned-row root as meaningful evidence.
2. Use a numerical LP only to propose active constraints. Recover a rational
   basic solution with FLINT/SymPy, then check EVERY original equality and
   triangle inequality exactly. A floating feasible flag is not a certificate.
3. On affordable sources, use charged original-digit MITM to prove that the
   corresponding native prefix has no word. Whole-fiber emptiness suffices;
   for nonempty fibers filter by the actual assigned projections.
4. Record nontrivial exact fractional-but-not-integral prefixes and their
   depths. Separate conditional label batches from population samples.
5. Independently replay primal rational certificates and original native truth.
   Tests must include LP false proposals, degeneracy, unsupported rank, tiny
   negative rationals, honest source prefixes and a true native continuation.
6. If fractional continuations are frequent, seek a source-law lower bound on
   surviving branches or a costed discrete cut outside this relaxation. If
   infeasible prefixes dominate instead, improve certificate search with a
   proof and matched costed experiment. Do not choose based on wall-time plots.

## Why This May Fail

Finite fractional witnesses can be incidental. The selected prefixes may be
unrepresentative, and good branch order can avoid them. LP feasibility does not
force any decoder to visit a branch; one tree's broad frontier is not an
algorithmic lower bound. Even a theorem for this relaxation does not obstruct
integer cuts, combinatorial representations, other bases or arbitrary quantum
receivers. Preserve these limits and keep candidate acceptance blocked.

The decisive positive target remains a new polynomial-cost ordinary native
pair finder with a proved source-law success probability, or another quantum
receiver that avoids requiring it. Do not confuse another conditional wrapper
with that missing invention.
