# Scoped Rees Formal Verification

2026-10-24. This is an isolated checked successor of the uncompiled
`formal/drafts/ReesHomogenization.lean`. It does not replace the main
checkout while migration is unresolved. The full quantum algorithm is NOT
formalized here, and no novelty or speedup is inferred from this result.

## Research Decision

The last pass established a classical falsifier for coordinate-MM orbit
extensions. The remaining anisotropic high-rate candidate has an existing
intrinsic classical portfolio, supplied-norm inversion, and related MQ
infrastructure. Another generic encoding would duplicate existing work;
its high-rate execution is already specified for Gemini. No new natural
problem reduction emerged from the algebraic comparison in this pass.

The proposed Rees HSP composition remains a concrete end-to-end theoretical
route. It has one completed independent AI review, but its formal draft
had never reached the compiler because of offloaded dependencies. Closing
that precise gap is useful evidence; it does not create a new algorithm.

## Exactly What Is Checked

Lean4.35.0 with mathlib commit56a005855ea17e0b0958f73ec801ae140b0a1679
checks sixteen theorems in ReesHomogenization.lean, fifteen additional
theorems in ReesLie.lean, thirteen in ReesDilation.lean, and 31 in
ReesCentralInstrument.lean, together with 24 definitions/instances/structures.
Audit.lean prints the axioms of all 99 declared items. verify.py recompiles
all four modules first, requires all 99 results exactly once, and rejects warnings, errors,
missing entries, extra axioms, changed snapshots or an altered audit script.

The original nine statements now compile:

- Module-valued matrix-row composition and identity.
- The nonconstant evaluation matrix has powers1 throughn and nonzero
  determinant at n distinct nonzero field points.
- Membership of all n evaluations in ANY submodule is equivalent to
  coefficientwise membership. No homogeneous-hidden-subspace promise.
- Given actual evaluation homomorphisms, their coefficient identity, and
  an original hiding function, the tuple hides that coefficient condition.
- The finite central coefficient transforms with the correct character
  and includes the full hidden-intersection multiplicity on allowed branches.

Seven additional statements check:

- Nonzero graded dilation preserves coefficientwise hidden membership.
- Zero dilation erases all coefficients and is not an allowed automorphism.
- The hidden/embedded intersection contains the identity and has positive size.
- Coefficients outside H times the embedded subgroup are zero.
- A character nontrivial on that intersection has ZERO coefficients everywhere;
  it cannot be normalized as an allowed source branch.
- A zero evaluation point can lose a nonzero coefficient.
- Repeated nonzero evaluation points can also lose a nonzero coefficient.

The last two are general field counterexamples proved in Lean, not sampled
finite examples. The character statements do not assume H normal. They
are finite-sum identities; centrality is an additional requirement for
their intended spectral/channel interpretation.

The second pass constructs a concrete positive Rees Lie cover inside the
product of L at the evaluation points. Its15 additional theorems establish
the actual lower-central bracket bound, closure without discarding nonzero
high-degree terms, nilpotency preservation, injective evaluation, explicit
inverse coefficient recovery, coefficientwise hidden membership and retention
of ALL of L in grade one. Evaluation maps are actual Lie homomorphisms.
The constructors and Lie instances are included in the axiom audit, not
just theorems that happen to reference them. See REES_LIE_SCOPE.md for the
precise construction, mathematical argument and remaining limitations.

The third pass constructs the actual graded dilation Lie automorphism,
including its inverse, composition law and invariance of tuple hidden
membership. It checks top-grade centrality and its scaling exponent,
zero-scaling erasure, and a universal obstruction to uniform rescaling of
noncommuting elements. The evaluation points need not be closed under
rescaling. See REES_DILATION_SCOPE.md. No group/BCH or quantum-operation
conclusion is silently inferred from this Lie result.

The fourth pass derives the complete central instrument from explicit
two-sided measurement operators, including nontrivial hidden intersections
and zero-mass records. It proves Kraus completeness and arbitrary-reference
controlled discard, then joins them in `central_instrument`. Support and
phase cancellation remain explicit group-theoretic certificate obligations.
See REES_CENTRAL_SCOPE.md for the full boundary and finite falsifiers.

## What Is Still Assumed Or Unformalized

`tuple_hides` explicitly ASSUMES the group homomorphisms, coefficient
evaluation identity, and original hiding law. It does not prove these
premises for a concrete BCH group. ReesLie now supplies the concrete Lie
cover, evaluation maps and coefficient recovery, but not the passage to
group homomorphisms. The interface theorem is not the complete algorithm.

Still outside this check: Lazard/BCH correspondence; efficient construction
of the complete character family and the public cancellation certificate;
SDE existence/algorithm/runtime; approximate recursive composition;
general positive-semidefinite/diamond-norm API statements; final Fourier recovery; outer black-box
reductions; precision/gate complexity; natural applications and classical
separation. No full quantum circuit was executed.

The coefficient uses the DOMAIN preimage {w : C | embed(w) in H}. Equating
its cardinality to an actual subgroup intersection in G additionally needs
embed injective. The physical central subgroup embedding has that premise;
the algebraic theorem deliberately does not silently assume it.

Standard foundational axioms propext, Classical.choice and Quot.sound are
allowed. This is NOT an axiom-free or constructive implementation claim.
The audit excludes sorryAx and any additional axioms in these proof terms.
Lean and imported mathlib binaries remain in the trusted toolchain; the
entire dependency library was not independently rebuilt or re-audited.

## Changes From The Frozen Draft

The original is preserved in source/ReesHomogenization.lean, SHA256
ded56af5166e119d7dbc912c01e365b63d6d7dcba102a1de84f07b1cd509ffed.
The old import path moved to Mathlib.Algebra.Group.Subgroup.Basic.
The old Equiv.mulRight_apply identifier was unavailable; the translated
sum proof now states its summand explicitly and performs the group rewrite
BEFORE simplifying map_mul. This avoids rewriting away the required
membership identity. No original theorem conclusion or premise was weakened.
The other changes add the seven statements and update the status comment.
ReesLie.lean is new and does not weaken the older interface statements.

## Reproduce

This directory has a separate local mathlib checkout and pinned dependency
manifest, outside iCloud. From this directory:

```sh
/opt/anaconda3/bin/python verify.py --output receipt.json
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_verify.py
OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_central_controls.py
OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python central_controls.py --output central_control_receipt.json
```

For a new environment, install the declared Lean toolchain; clone the pinned
mathlib revision into mathlib; then run lake update. The official cache tool
can retrieve Mathlib.LinearAlgebra.Vandermonde,
Mathlib.LinearAlgebra.Matrix.NonsingularInverse, Mathlib.Analysis.Complex.Basic,
Mathlib.Algebra.Group.Subgroup.Basic, and Mathlib.Algebra.Lie.Nilpotent
with their dependency closure. In this local
path-dependency layout its cache lands in the root .lake/build/lib/lean;
verify.py puts that directory first. A generic lake build started rebuilding
dependencies and was stopped, then the published cache was restored.
The successful proof check is the explicit Lean invocation in verify.py,
not a claimed successful full lake build. No build job is left running.

## Integration Handoff

After migration is verified, port the import/proof repair, added lemmas and
new ReesLie.lean, ReesDilation.lean and ReesCentralInstrument.lean into the real formal project. Reconcile its locally defined
pointwise Lie instances with any existing instances. Retain the original
source hash and rerun the complete 99-item axiom audit under that project's
normal module paths. Only then update
the repository's stale UNVERIFIED-draft notice for this exact scope.
Do not change the independent-review status or promote the full HSP theorem
to FORMALLY_VERIFIED. No new candidate, UI feature or CLI is needed.

The second pass closes the previously named Lie-construction obligation;
the third closes the graded Lie-automorphism obligation; the fourth closes
the finite all-record central channel identity under the explicit certificate.
Further formalization is useful only when it targets another real obligation:
BCH compatibility or efficient public cancellation. See CENTRAL_HANDOFF.md.
Natural-problem applications and a matched classical comparison remain the
larger research-value gap; more nearby finite fixtures do not close it.
