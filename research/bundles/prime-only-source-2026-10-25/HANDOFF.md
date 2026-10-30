# Prime-Only Source Handoff

## Theory Change

Use the new parity-controlled lift and an odd squarefree multiplier N.
The new construction needs only prime-order weak evaluations, not the
old r^2 and order-4 weak data. Its source and output remain the SAME
ell-isogeny kernel problem. See PRIME_ONLY_SOURCE.md for the full proof,
resource bound, falsifiers and remaining imported obligations.

This is not permission to relabel the OLD source as prime-only. That
source actually requires its prime-square data. Keep it and its non-free
kernel counterexamples as independent controls. Only the revised lift,
multiplier, quotient and transport path earns the weaker access contract.

## Wiring After Migration

1. Call odd_trace_bound on the full paid source order and ell. Build the
   plan ONCE from that uniform bound, not from observed traces. Preserve
   all original access restrictions; abort if required levels are missing.
2. Replace lift_symplectic with odd_trace_lift in this new path. All
   elementary coefficients are evenized BEFORE appending the ell-shear.
   The one extra factor raises the maximum word length to157. Do not
   append the shear to an arbitrary old lift and assume its trace is odd.
3. Build the eight-square certificate with multiplier N, not N^2. Use a
   verified/capped four-square backend for coherent-clock claims. The local
   SymPy witness routine does not itself certify the required uniform clock.
4. At each quotient prime r, use only B[r]. Compute ker(F_r)=im(C_r), check
   rank16 and isotropy, and call A26 for an r-polarized quotient. Push later
   kernels and marks through it. No r^2 flags are needed in THIS path.
5. Transport marks using N^(-1) C, not N^(-2) C. Use one common weak mask
   across the copied factors and one automorphism across all marking levels.
6. Preserve base-field embeddings and scalar-Frobenius descent. Public
   level-4 theta coordinates/8-torsion remain charged model dependencies,
   even though phi is not weakly queried at those orders.
7. Retain product-target and extra-endomorphism classical falsifiers. Do
   not promote arithmetic certificate success into native geometry or
   quantum-advantage evidence.
8. Run the main CLI/registry validation only after its checkout is verified
   local. No main/staging edit or integration was made during this pass.

## Elliptic Reduction

ELLIPTIC_COROLLARY.md spells out the conditional reduction phi -> phi x phi
and the prior-art boundary. Reuse ONE weak response in both copies to keep
the common scalar. The polarization multiplier remains ell, not ell^2.
After the genuine receiver supplies its certified plane, the narrow
elliptic_reduction.py extracts the common line and its LEFT annihilator
ideal. It refuses a plane not of the doubled form. It does not implement a
source, secret recovery or IdealToIsogeny. Tests distinguish annihilating L
from having image in L; these opposite module conventions cannot be mixed.

The possible contribution is bypassing powersmooth quaternion lifting,
not inventing a first quantum solution of weak IsERP. Existing quantum
IsERP prior art and its heuristic preprocessing are recorded in the note.
Independent review and a fuller novelty audit remain required.

## What To Avoid

- Another opaque-label receiver benchmark: the receiver did not change.
- A large kernel-point enumeration as proof of scalability: the cost still
  grows as r^16 at fixed dimension, with severe constants.
- A new prime-only oracle candidate: this is a weaker interface for the
  original promised isogeny, not a newly invented oracle search problem.
- Calling the construction independently reviewed or novel. The previously
  authorized Rees reviewer did not inspect this new source improvement.

Next high-value work remains a genuine geometric source implementation or
independent mathematical falsification of this complete source, followed by
the strongest matched classical attacks. The arithmetic controls do not
settle any of those wholesale.
