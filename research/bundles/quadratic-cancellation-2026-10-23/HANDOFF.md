# Integration Handoff

Do not edit the source or staging copy while the project migration runs.
This bundle is not installed in `qsearch.py` or any registry. It is not a new
CandidateRecord and must not be represented as a discovered quantum algorithm.

## After Migration Is Verified Complete

1. Move the implementation into `theorems/quadratic_diagonal_solver.py`, using
   local imports for the rank and bounded scalar/root helpers. Remove the
   standalone sibling-directory `sys.path` setup during integration. Preserve
   tests and the exact original-equation verification.
2. Add an adapter between column-form inputs and this module's row matrix.
   In `weighted_two_erasure_cascade.required_bezout_arity`, remove ONLY the
   `g==2` restriction `p==3 mod4`. The general bound is `(rank+1)^2`. Keep
   higher-coset degrees unsupported unless a separately verified solver exists.
3. In `solve_bezout_sde_weights`, route the newly supported `g==2` regime to
   this solver, then use the EXISTING Bezout lift and verify the ORIGINAL
   degree-d moments. Preserve zeros when applying the exponent. A public
   rank bound must be fixed before quantum source acquisition; do not infer
   a cheaper source budget after observing a lucky bank.
4. Keep the existing `p=3 mod4` specialized route if its simpler conic
   implementation is cheaper. At rank one the scalar backend uses 3 labels
   instead of 4. Select any such optimization before acquiring its bank.
5. Update `test_higher_coset_and_unimplemented_quadratic_regimes_still_fail_closed`
   in `tests/test_cubic_diagonal_solver.py`: `(13,2)` should now be accepted;
   `(43,6)`, `(43,7)`, `(13,4)` must STILL fail. Add lift checks for
   `(p,d)=(13,10),(17,6),(29,6),(41,6)` with gcd(d,p-1)=2.
6. Integrate one `p=13` class-three erasure/instrument control where both
   quadratic and cubic power maps are nonbijective. Use the existing physical
   state/reference-safe controls and include every zero-scale input in the
   source ledger. Do not substitute symbolic phase cancellation for an
   actual instrument test or discard unsuccessful branches from its budget.
7. For the bounded-index FPT path, allow public rank-dependent selection of
   the cheaper of the scalar and polynomial constructions. Do not relabel
   an exponential scalar bank as polynomial merely because finite ranks run.
8. Rerun focused suites, complete pytest, syntax checks and registry validation.
   Only then regenerate research-critical CLI artifacts. No UI redesign.

## Do Not Claim

- A new SDE theorem: this is Ivanyos--Santha's published construction.
- A newly polynomial `p=3 mod4` route: one already exists in this repository.
- A completed or clocked class-three quantum algorithm: source, instrument,
  full proof and cubic timing obligations are separate.
- A Shor-level result, a new hard oracle problem, or classical hardness.

## Research Priority After Integration

An independent adversarial review of `REES_HSP_REDUCTION.md` and the complete
manuscript is more valuable than more scalar arithmetic controls. Audit the
nonhomogeneous hidden subgroup's retention through the Rees cover, conditional
branch/source density, quotient access, and the outer bounded-codimension
reduction. Each claimed lemma needs its exact input/output contract. Separately,
do not reopen graph/code/succinct-polynomial applications without addressing
the classical and source-access attacks already recorded in their audits.
