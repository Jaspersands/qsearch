# Odd Content Reduction Handoff

The original odd-degree kernel need not be cyclic. This is a conditional
extension of the same geometric source, not a new oracle input or an
implemented quantum algorithm. Read ODD_CONTENT_REDUCTION.md before wiring.

## Integration After Verified Migration

1. Retain the source's original degree-n plan, common-mask weak data, paid
   fields, full source order, fixed clocks and joint canonical labels.
   Generalize only the unknown kernel's freeness promise as proved here.
2. Generate probe_schedule(n,factors). Obtain each f(query)==f(I) boolean
   from the ACTUAL source, then call recover_content. Do not import supplied
   Smith data from controls into a solver or infer validity from boolean
   consistency alone. The function itself does not verify the source.
3. For each positive residual depth d=e-2a, use the earlier local Fourier
   method over q^d, with its matrices lifted to q^e and CRT-embedded at the
   FULL q^e component of the original n. A CRT embedding of q^d directly
   into n is invalid when d<e. There is no ring-section assumption.
4. Certify the direction using BOTH full-level Sp4 queries. Only the line
   modulo q^d is meaningful; higher digits are arbitrary lifts. Skip d=0.
5. Let c=product q^a and m=n/c^2. Build I_psi from the recovered residual
   lines and output I_phi=c I_psi. If m=1, output cO. Its index is n^2;
   do not output the residual ideal as if it were the original kernel.
6. Keep native/quantum execution and advantage flags false until actual
   backends have run. Reconcile the verified main checkout before any CLI,
   UI, registry or Git changes. None were made during this pass.

## What Remains

The expensive, independently unreviewed source is unchanged. General-degree
weak-IsERP is already known quantum prior art; possible value remains in
avoiding its powersmooth lifting assumptions. The full2025 manuscript was
not retrievable in this pass, so a full novelty audit remains incomplete.
Even degree, missing common fields or unknown full source orders are still
outside the construction. The authorized Rees review does not cover this
proof. Do not spawn another reviewer without new authorization.
