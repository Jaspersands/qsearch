# Stronger Classical Baseline Handoff

Wait for verified migration completion before repository integration.

Scientific delta: replace the generic unrestricted line-probe birthday cost
q^((n-1)/2) with the isotropic restriction cost q^((n-2)/2), times polynomial
rank/error overhead. This matches the published-bound application's exponent
in both q and n. It does NOT turn the opaque problem into a classical
polynomial-time problem or prove the quantum algorithm new.

The full proof is CLASSICAL_ATTACK.md. The essential steps are the uniform
isotropic sampler, parity-based nonzero intersection probability, exact
without-replacement birthday bound, equivariant successful-direction
distribution, and bounded rank accumulation. Preserve all five.

Routine integration for Gemini:

1. Reuse the existing field and matrix helpers instead of sibling path imports.
2. Register as a SAME-ORACLE classical baseline for the existing orthogonal
   candidate, not as a new quantum candidate or a natural-source attack.
3. Preserve query and memory caps; actual parameter draws and oracle queries
   are different quantities. No full table or hidden kernel is supplied.
4. Store failed/incomplete rounds and their charged calls. Do not drop the
   final exact certificate or accept a rank-r span without it.
5. Mark the prime-field executable scope separately from the effective-field
   mathematical argument. Reference default budgets are not arbitrary-epsilon
   schedules without rescheduling B and the per-probe failure allowance.
6. Keep independent review and novelty status pending. Run full repository
   validation only after safe integration; no dashboard change is needed.

Do not optimize finite query constants next. The remaining critical work is
independent proof/prior-art scrutiny and a natural input source that survives
matched classical attacks. The concurrent Rees reviewer is reviewing a
different theorem and does not certify this argument.
