# Handoff: Explicit Surface Receiver

Do not merge into source/staging during migration. Read the proof note
before integrating; no accepted quantum speedup follows from this bundle.

## Research Result

For the existing Sp_4(F_ell) source, the receiver's generic HPGP step can
be replaced by the explicit two-chirp cancellation protocol. It needs
only the same legal source queries, public finite-field arithmetic,
prime Fourier transforms, translations and a two-register shear.

The decoder and small Qiskit controls are implemented. The controls never
feed hidden graph coefficients into the receiver. They DO enumerate
native oracle fibers classically, at exponential cost, to construct
post-label states. This is not a production coherent source.

## Integration Work For Gemini

1. Preserve the two-source interfaces separately: a real coherent source
   implementation versus `NativeFiberControl` for bounded proof controls.
   Report classical table queries separately from ideal source-copy counts.
2. Reuse the real source's public U_X D_t query compiler. Uncompute the
   query and source workspace before measuring labels and frequencies.
3. Replace dense prime Fourier/permutation matrices with a genuine
   poly(log ell,log(1/eta)) reversible compiler only when a scalable
   source is available. Dense controls must keep their size guards.
4. Retain both row budgets, independent fresh states, nondegenerate root
   choice, four charts and ORIGINAL-oracle transvection certificates.
   Bad-chart local consistency is insufficient.
5. Add source, Fourier-synthesis and capped root-search errors separately.
   The current ideal copy bound alone is not an end-to-end error budget.
6. Update the existing proof artifact to "explicit receiver protocol;
   finite post-query quantum simulation verified", not "quantum algorithm
   on geometric input executed". Do not create a new toy candidate family.
7. After migration verification, run repository tests and qsearch validate.

## Next Research Question

Audit and instantiate the stabilized geometric label generator without
target-ring advice, including actual model conversion, field embeddings,
joint canonicalization and workspace cleanup. A representative target
must not already be killed by the product/mixing-endomorphism baseline.
Use the new decoder to localize any eventual failure to the source or
to an explicit tested measurement step, not an unspecified HPGP routine.

Independent prior-art and proof review remain required. Quadratic phase
learning is known; this specialization must not be sold as the discovery.
