# Gaussian Dither Sampler: Mathematical Specification For Implementation

NOT IMPLEMENTED. This is the next sampler task for Gemini / Antigravity,
separate from GPT's quantum-mechanism/source-theorem work. No certified
dither source or source-conditioned coverage amplification is admitted yet.

## Distribution And Coupling

For a positive exact rational sigma, sample E=nearest(W), where W has density
exp(-pi*w^2/sigma^2)/sigma. The integer CDF is

    F(t) = (1 + erf(sqrt(pi)*(t+1/2)/sigma))/2.

Use the EXISTING Gaussian-radius Arb primitive if convenient:
for t>=0, F(t)=1-tail(t)/2; for t<=-1, F(t)=tail(-t-1)/2. Directed rational
enclosures, not floating CDF values, must determine every comparison.
Same-library replay is not an independent transcendental certificate.

Let f>=1 be a declared per-draw failure-bit target. Set B=ceil(f*sigma).
The probability |E|>B is erfc(sqrt(pi)*(B+1/2)/sigma), at most
exp(-pi*f^2)<=exp(-3*f^2)<=2^(-3*f^2)<=2^(-f-1).
A stored directed Arb tail box may give a sharper bound, but never erase it.

Draw ONE latent U uniform[0,1) using fresh ideal-random bits. Read its dyadic
prefix lazily, retaining the SAME prefix across every CDF comparison. Find
the smallest t with U<F(t) by integer binary search in [-B,B], with explicit
tail rejection using F(-B-1) and F(B). A successful decision is allowed only
when the U prefix interval lies entirely to one side of the CDF enclosure.
If all K uniform bits are exhausted, return an explicit precision abort.
Never choose a midpoint of an unresolved interval or silently resample.

## The Adaptive-Threshold Precision Trap

DO NOT bound ambiguity by the number of queried CDF thresholds times2^-K.
Binary-search thresholds are selected adaptively from the SAME U. The tree
has up to2B+2 possible thresholds, even though a draw queries onlyO(log B).
For huge sigma, a query-count union can be catastrophically optimistic.

Require every CDF enclosure to have width<=2*2^-K. A K-bit U cell that
intersects it corresponds to U in a set of length at most4*2^-K, allowing
one cell width on either side. The safe union is therefore

    precision_abort_probability <= 4*(2B+2)*2^-K.

Choose K=f+ceil(log2(16*(B+1))). Then this budget is at most2^(-f-1).
Together with the tail, per-draw coupling loss is at most2^-f.
Compute ceiling logs and budgets by INTEGER inequalities. Do not expand
the full CDF tree; the union is analytical and actual queries remain paid.
The width must be fixed before this draw; an adaptively selected root uses
fresh U bits and the same conditional argument.

CDF precision should escalate until the enclosure-width requirement holds.
If implementation applies a numerical precision/work cap, its possible
failure is an ADDITIONAL abort event requiring a justified budget. Visited
endpoint success is not a proof that all potential threshold calls clear a
fixed numerical cap. Prefer an explicit trusted convergent special-function
primitive with charged actual precision work; do not declare numerical
failures impossible merely because several controls succeeded.

## Complete Batch And Integration

For k output dithers, set f=lambda+ceil(log2 k) for a total target2^-lambda,
or retain the exact k-times loss. Each dither gets independent fresh bits.
If a draw aborts, abort the COMPLETE source-refresh batch and retain partial
transcripts only for diagnostics. Do not use a shortened output as a full
k-sample source or condition on success without charging the lost mass.

Record sigma,B,K, all bit draws, CDF thresholds/endpoints, comparison outcomes,
tail/precision losses, observed numerical work, and every abort reason.
The full public sampler loss feeds native_source_refresh.source_ledger;
producer advantage remains an EXTERNAL promise at the NEW target width.
Fresh dither randomness is never counted as fresh original observations.

## Required Tests

- Complete bounded uniform-prefix censuses for a small sigma/K control,
  comparing every accepted integer to certified CDF quantile intervals.
- Negative, positive and tail outcomes with no floating guesses.
- Giant rational widths / original roots beyond2^53 using canonical integers.
- Forced tail, uniform-bit precision and numerical-cap aborts.
- A regression showing the all-threshold union differs fromO(log B) times
  the per-threshold bound; do not generate a toy oracle candidate.
- Complete-batch abort accounting, independent draw lineage and repeat costs.
- Tampering of sigma, thresholds, endpoints, integer outputs and budgets.
- Separate trusted-Arb CDF replay; explicitly deny an independent
  transcendental certificate unless one is actually supplied.

After implementing, run the standalone workflow and targeted tests, then
wire the existing sign/mask transform with complete sign/mask random-bit
accounting. Do not set source_refresh_sampler_implemented=true before the
actual sampler, coupled losses, replay and complete-batch tests exist.
