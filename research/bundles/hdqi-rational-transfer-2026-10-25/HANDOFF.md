# Handoff: Check The Classical Upper Bound Before Quantum Compilation

All work is isolated outside the unverified migrating main checkout.
Preserve these source/receipt pairs. Do not label them integrated qsearch
commands, accepted quantum candidates, or a discovered quantum algorithm.

## Reasoning Priority

The local argument in RATIONAL_TRANSFER.md is the most important new claim
to scrutinize. Attack, in particular:

1. The same native trace/output isometry, including all degeneracy sectors.
2. The transfer factorization with the SAME occupation operators as H.
3. The squared angle-error bound for the pure canonical pilot.
4. The lower bound on the reference product norm from the positive even part.
5. The number of precision BITS needed for complex roots, rather than
   accidentally charging only coefficient precision or assuming exact roots.
6. Exact conjugate environment contraction and the bond (R+1)^L.
7. Applicability only to path powers and specified output measurements.

This pass did self-checks, literature checks and direct numerical/exact
controls; it did NOT receive a new independent reasoning review. Earlier
Rees/exterior reviews do not cover it. No reviewer has been spawned here.

The degrees are currently impractical. An exp(O(log^3 n)) bound is not a
polynomial sampler, but is a much stronger comparator than 2^m enumeration.
Do not spend another pass improving the quantum filter constants before
considering this competitor and the missing native useful-task reduction.

## Mechanical Work For Gemini

After the main checkout migration is VERIFIED, wire the three bundles as
diagnostics/baselines with their current claim flags. Run main validation,
all affected tests and each exact replay. Keep dense controls out of
algorithm input paths. Preserve recorded source and context hashes.

If implementing the remaining factor backend:
- Square-free factor the reciprocal integer polynomial; preserve repeated
  roots and certify ALL complex disks at the recorded radius or a separately
  proved tighter budget. Reject missing/overlapping/uncertified roots.
- Round to exact Gaussian rationals, preserving conjugate pairs when possible.
- Extend WordSampler with exact conjugation in environments and exact
  rational squared norms/coins. Test complex phase cancellation against
  direct Pauli multiplication, including conjugate pairs and zero products.
- Enforce an explicit bond/resource budget. An enormous computed bond is
  not a runnable large-instance benchmark. A budget refusal is inconclusive,
  not classical hardness or a quantum-positive signal.
- Only then connect the uniform approximation, factor rounding and exact
  surrogate sampler into a full native sampling error certificate.

No background search, extra commits, push, UI work or automations are part
of this handoff. Keep the user-visible progress summary short and scientific.
