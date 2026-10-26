# Hermite Streaming Composition Audit

2026-10-21. Written theorem proposal and executable identity controls.
Independent mathematical and novelty review remain pending. No central
claim admission or native quantum circuit execution.

## What This Pass Changes

The two preceding passes specify a syndrome-only decoder and a compact
implementation. This pass audits their use inside a quantum computation:
source loading, diagonal acceptance, clean label erasure, bounded pin
sampling, and whole-computation precision.

Two accounting points are now explicit:

1. A capped random-subset sampler can abort. Its failure is additional to
   source rejection and the decoder's pin ambiguity.
2. Membership-table updates need only exact Boolean phase gates. Approximate
   rotations need not be repeated at every stream arrival. The earlier
   `log N` precision allowance was conservative, not necessary for this
   logical gate model.

The possible contribution remains the small-characteristic, compact,
guarded decoder substitution, not the source preparation or Fourier method.

## Dependencies And Scope

- Local decoder proofs: `HERMITE_PINNED_DECODER.md`, Sections 1--4.
- Local storage proof: `HERMITE_COMPACT_DECODER.md`, Sections 1--5.
- [Wu--Yang](https://arxiv.org/html/2610.01902v1), Lemma 4.3 supplies the
  one-pass source; Section 5 supplies the augmented-syndrome score argument.
  Their exponential decoder is NOT being cited as an efficient subroutine.
- [Mosca--Zalka](https://arxiv.org/abs/quant-ph/0301093) supplies uniform
  prime-order Fourier circuits with clean workspace. This avoids allocating
  a dense Fourier matrix or assuming that a `q^ell`-dimensional transform
  is one elementary operation.
- [Bennett](https://doi.org/10.1137/0218053) supplies input-preserving
  reversible simulation with its logarithmic workspace overhead.
- Finite-gate compilation uses standard
  [elementary gate decompositions](https://arxiv.org/abs/quant-ph/9503016)
  and [Solovay--Kitaev](https://arxiv.org/abs/quant-ph/0505030).

The input consists of arbitrary explicit membership tables in arbitrary
stream order, with each row containing `(q^ell-1)/2` good addresses.
There is no succinct evaluator, QRAM, repeated table access, or promise of
a classically difficult physical instance.

## Source Checks

Write `Q=q^ell`, `a=1/Q`, `rho=(1-a)/2`, and
`theta=lambda*(1-a^2)`. The post-Fourier zero-address selector vector is

    v = (sqrt(1-lambda), -a*sqrt(lambda)).

After flipping the selector at nonzero addresses, apply at address zero

    U = [[v0,v1],[-v1,v0]] / sqrt(1-theta).

Then `Uv=(sqrt(1-theta),0)`. Omitting this public rotation leaves selector
mass `lambda/Q^2`; discarding that selector is NOT clean state preparation.
The resulting row's good-score probability is

    rho + (1-2rho)*theta
        + 2*sqrt(theta*(1-theta)*rho*(1-rho)).

The implementation verifies this identity, arbitrary-order phase updates,
and the tensor Fourier transform on the additive vector group `F_q^ell`.
A cyclic transform on `Z/(q^ell)` is a different operation.

These statevectors and exhaustive stream-promise checks are diagnostic
code. They allocate full tables and do NOT measure the quantum algorithm's
space. The promised-input algorithm need not validate the stream.

## Clean Decoder Instrument

Let `D_R(s,p)` be the deterministic compact decoder with failure tag.
Its interpolant is a function of the UNaugmented syndrome `s` only.
Its final affine constraints may use the public pin set `R` and the
retained blocks `p`. Set `H_R e=(G e,e_R)`.

Define the accepted set

    A_R = {e : wt(e)<=d and D_R(H_R e)=e},

where the decoder certifies uniqueness throughout `B_(d+2)`. This is
usually a strict subset of all isolated errors. Conservative rejection
is permitted, but its mass must be charged.

An input-preserving reversible implementation has the form

    |h>|0>|0> -> |h>|D_R(h)>|0>,

including an explicit valid/failure flag. On malformed bit encodings the
bounded computation returns failure; it must be total, not throw an
exception. Pad variable-time branches to a known polynomial upper bound.
The Python reference is not itself such a gate compiler.

To measure acceptance:

1. Compute `h=H_R e` into a clean register.
2. Run the input-preserving decoder on `h`.
3. Copy `(wt(e)<=d AND valid AND D_R(h)=e)` into the herald.
4. Reverse the decoder, then reverse the computation of `h`.
5. Measure ONLY the herald.

Thus no syndrome, polynomial, pivot choice, runtime history or decoded
error remains outside the original error register. The successful
measurement is exactly the diagonal projection onto `A_R`.

On success, compute `h` again, compute `D_R(h)`, subtract this decoded value
from the original error register, and reverse the decoder. The retained
register is `h`; the error and temporary registers are zero. The decoder
can be reversed because its input `h` has not changed.

Do not reverse the original `h=H_R e` computation after erasing `e`.
That would no longer be its inverse on the current registers.

The sparse executable control uses the actual compact decoder and three
equally weighted basis labels. Two are accepted and one fails the source
cap. Keeping the error register would halve the accepted contribution at
the zero Fourier character: numerator `2/3` instead of `4/3`, with the
same Fourier denominator. This is a coherence check, not a full product
source experiment or a high-score demonstration.

## Why The Conservative Decoder Still Suffices

For fixed `e` with `wt(e)<=d`, every radius-`d+2` competitor lies in the
interpolant's affine differential solution space. This space contains the
true associated polynomial and is fixed before choosing `R`. Its dimension
is at most

    t = s*ceil(K/q),  K=ell*(q-1)/2.

The previous rank-exposure proof therefore bounds failure to recover this
particular `e` by

    eta = Pr[Bin(r,1/2)<t],

or zero when the deterministic jet information threshold is exceeded.
No enumeration of `q^t` points occurs. For a product source independent
of `R`, diagonal rejection averages these pointwise bounds, so the same
`eta` applies to rejected source mass.

Isolation in the larger ball is also retained. If two one-block neighbors
of accepted labels have the same augmented syndrome, moving their two
translations to one side produces a radius-`d+2` competitor of an accepted
label. Uniqueness forces the neighbors to coincide.

This proves that replacing the published isolation projector by `A_R`
preserves the needed neighbor-support injectivity. It does not assert
global injectivity, nor require the decoder to accept every isolated label.
The native same-code second-moment counterexample `8 -> 12` in the pinned
report remains a required negative control.

## Bounded Pin Randomness

Use partial Fisher--Yates selection. At step `j`, let `b=n-j`, generate
`ceil(log2 b)` fair bits, and accept the resulting integer if it is below
`b`. Stop after `L` attempts; abort the algorithm if none succeeds.
The `b=1` draw is deterministic.

An accepted integer is exactly uniform. Moreover, the chance that this
step succeeds depends on `b`, not on which integer was accepted.
The successive bounds are deterministic. Therefore, conditional on all
draws succeeding, the resulting subset is exactly uniform among size-`r`
subsets. No bias is introduced by the cap.

The exact abort probability is

    1 - product_(b=n-r+1)^n
          (1 - ((2^ceil(log2 b)-b)/2^ceil(log2 b))^L).

It is at most `r*2^-L`. Taking `L=b_security+ceil(log2 r)` suffices
for error at most `2^-b_security`. Store the sampling pool in `O(n log n)`
classical bits, which fits the decoder's workspace. This randomness is
independent of the input and source. Abort produces a fixed fallback
answer and counts as failure; it never retries the input stream.

Tests enumerate all bit strings for a small sampler, including its abort
branches, and verify exact conditional uniformity.

## Unconditional Probability Ledger

Let `d=floor(tau*n)`, `lambda<tau<1/2`, and let `mu` be the product score
mean. The source tail plus pin ambiguity gives

    delta <= exp(-2*(tau-lambda)^2*n) + eta.

For unnormalized accepted states, the transferred centered second moment
is bounded by `n/2+2*n^2*delta`. With

    g = mu/n - alpha - r/n > 0,

the joint probability of acceptance and a bad answer is at most
`(1/(2n)+2*delta)/g^2`. Thus our complete ledger is

    failure <= pin_sampler_abort + delta
               + (1/(2n)+2*delta)/g^2 + total_output_TV,

capped at one. There is NO division by the acceptance probability for
an individual pin set. In particular, a pin set that rejects everything
does not make the analysis undefined. The rejection is already paid.

## Precision And Real Resources

Encode each field symbol in `ceil(log2 q)` qubits. An input entry specifies
a classical row, a classical address, and one classical bit. Its update
is an address-equality-controlled sign. Compute equality using NOT and
Toffoli gates, apply Z conditioned on the selector, and uncompute.
These operations admit EXACT Clifford+T realizations with clean ancillas.
Classical row routing can even scan all rows; its time is still polynomial.

All nonexact gates are confined to preparation and final processing:
uniform states, field Fourier transforms, and the public selector rotation.
Use a uniform Fourier circuit per field symbol, not a dense matrix.
Generate and compile gates incrementally; do not retain the whole gate list.
For `G=poly_s(q,ell)` such gates, individual operator error at most
`epsilon/G` bounds total state/output error by `epsilon`. Exact stream
updates preserve that norm difference even across `N` arrivals.

This is a logical circuit statement, NOT a fault-tolerance claim.
Physical gate errors accumulated over a huge stream still need their own
error-correction analysis. Exact logical Clifford+T synthesis does not
make hardware noiseless.

Apply Bennett only to the retained-register postprocessing, whose
deterministic time is `poly_s(q,ell)`. Do not reversibly simulate the
whole input-reading history. Classical decoder space
`O_s(q*ell*log q)` then gives reversible space

    O_s(q*ell*log q*log(q*ell)).

For inverse-polynomial total precision, incremental circuit generation
and compilation require only additional polylogarithmic scratch.
The logarithmic reversible overhead is NOT removed.

Total input-processing time is `N*poly_s(q,ell)`, not `polylog(N)`.
Only preprocessing, EACH update, postprocessing, and memory become
polylogarithmic in `N` when `ell=floor(q^a)`, `0<a<1`.

## Complete Proposed Upper Bound

For every fixed target `alpha<1`, choose fixed
`0<lambda<tau<1/2` with `1/2+sqrt(lambda*(1-lambda))>alpha`, and fixed
`s` satisfying

    (s+3)/(2*(s+2)) < 1-tau.

There is a sufficiently large constant `ell0(alpha)` such that the strict
interpolation inequality holds for all `ell>=ell0` and sufficiently large
prime `q`, including the guard `d+2`. For any sequence `ell=o(q)` in this
range, use `r=O_s(ell+log q)` pins, pin ambiguity at most `1/n`, pin-sampler
abort at most `1/n`, and total output-TV at most `1/n`.

Then `r/n -> 0`, the score gap stays positive, and the unconditional
failure bound tends to zero. Together with the compact-decoder lemmas,
this gives a proposed one-pass algorithm with polynomial preprocessing,
per-update and postprocessing time and the reversible workspace above.

This includes sufficiently large FIXED multiplicity. It does not include
every fixed multiplicity or `ell=1`, does not give exact optimum, and does
not give a uniform guarantee as `alpha` approaches one with the input size.
It is a review-pending theorem proposal, not an admitted discovery.

The classical lower bound remains external, model-specific, and carries
unknown approximation-dependent constants. This pass neither proves
unrestricted classical hardness nor claims a practical time speedup.

## Novelty And Attempts To Disprove It

- The source loader is prior art. Random side-information decoding is
  also prior art, including
  [Guruswami--Wang, Section 4.2](https://arxiv.org/abs/1106.3951).
  The proposed novelty is the exact small-characteristic guarded
  streaming substitution and its resource bound, if valid and new.
- [Jo, 2607.16541](https://arxiv.org/html/2607.16541v1) already gives
  coherent complete-list summation for OPI under membership-oracle access
  and a Johnson-radius condition. It is relevant prior work, but its
  input model, rate regime and full-list step do not automatically supply
  this half-rate, one-pass Hermite decoder. A targeted search is not an
  exhaustive novelty certification.
- The most consequential possible mathematical failure remains the
  interpolation module's completeness or the descending differential
  solver's treatment of all residual equations. Source tests cannot
  validate those lemmas.
- If the interpolant or source depends on the random pin set, the fixed
  affine-space rejection argument fails. Pins cannot be tuned on a
  promising branch.
- If any branch-dependent garbage survives, the classical decoder is
  not a coherent erasure procedure. The instrument control detects one
  such failure but is not a compiled gate-level certificate.
- The only output-observable transfer being used is the guarded local
  second moment. A claim about arbitrary observables would require a
  stronger and generally false global isometry.
- The explicit stream can be enormous. Even a correct upper-bound
  improvement here is not a Shor-comparable practical breakthrough.

## Reproduce And Next Decision

    python -m theorems.hermite_streaming_composition
    python -m pytest -q tests/test_hermite_streaming_composition.py \
      tests/test_hermite_compact_decoder.py tests/test_hermite_pinned_decoder.py \
      tests/test_folded_rs_decoder.py -W error::RuntimeWarning

The large-parameter JSON entry is ONLY an arithmetic check at
`q=1000000007, ell=256, s=15`. It constructs no code matrices or circuit.
Its 4301-pin sampler uses at most 53 trials per draw. Finite loader
controls and a sparse decoder instrument are recorded separately.

Next work should independently attempt to refute the compact-decoder
lemmas and check novelty of the resulting upper-bound theorem. Do not
substitute bigger statevector runs, a claim dashboard, or another size
sweep for that review. Routine integration remains separate.

Verification: 15 new tests and 70 connected tests passed in 32.77 seconds
with runtime warnings treated as errors. Python and site JavaScript syntax,
site checks, and registry validation passed. The full repository suite was
not run. Both preceding Hermite producers and reports retain their original
hashes. No central claim admission, CLI/UI wiring, commit or push.
