# Predeclared Structural Classical Attack

2026-10-23. Same public balanced signed MPI problem. No new oracle, no
changed centers, no planted solution and no quantum-advantage claim.

## Hypothesis

The native contiguous evaluation range contains large complete affine
subspaces over F2. Walsh characters supported on these blocks induce
row-phase directions with few distinct values up to sign. This may give
classical search more useful nonlocal moves than the original columns.
Few phase values alone do NOT imply easy optimization or rapid mixing.

## Frozen Protocol Before Execution

- Use the existing native h=13,m=6000,n=420 input, center seed 261006753.
- Verify its center hash and inherited best assignment against the saved
  balanced_signed_mpi.json. Do not tune points, seed or score threshold.
- Partition evaluations 6000..6419 into maximal aligned dyadic intervals.
  Each is an affine binary subspace. Use its complete Walsh character basis;
  their direct sum is a basis over the odd ring Z_8191.
- Reuse the unchanged resident fft_line_search body through AST extraction.
  Do not import the moving checkout or its offloaded dependency tree.
- Four runs: original and block-Walsh bases, each from zero and from the
  inherited best assignment. Cap each at two sweeps of 420 directions;
  early stop on a no-improvement sweep is allowed by the existing solver.
- Score ALL 6,000 rows and replay EVERY returned assignment through both
  the explicit matrix and the original fast convolution. Record actual
  scans and improving moves, including failed controls.
- Verify the Walsh transform against direct sums and its affine-translation
  identity. Report phase cardinalities, not just search scores.
- For five fixed modes (0,1,2,127,255) of the largest block, enumerate the
  nonzero scalar multiples and record the best worst-row phase magnitude.
  This tests whether compression already gives small moves at native size.
- Do not increase budgets or add restarts because a result is disappointing.

## Falsifiers / Interpretation

Reaching score 0.3 would falsify this native instance's separation from this
classical attack, not prove general dequantization. Matching or failing to
beat the inherited score deprioritizes this concrete move set, not all
classical algorithms. An algebraic identity failure invalidates the proposed
compression. A different field presentation or center hash invalidates a
same-instance comparison. Finite native results cannot establish asymptotic
hardness, mixing, or a scaling advantage.

The MPI construction is prior art:
https://arxiv.org/html/2610.06753 . The exact translation identity is derived
in this bundle; novelty of this use of Walsh preconditioning is unclaimed.
