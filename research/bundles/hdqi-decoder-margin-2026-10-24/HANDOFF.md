# Actual Readout Transfer, Not Another Sampler

This pass follows the line-graph pilot-preparation construction. Its single
question is whether nonlinear classical decoding evades the existing
additive-Pauli classical comparator. A uniform decoding margin prevents
that escape. Do not broaden the conclusion to all nonlinear decoders.

## Mathematical Contracts

- Short public word h: a decoder correct on EVERY weight<=t label gives
  expectation error <=2sqrt(Pr[|Y|>t-|h|]) relative to its canonical Pauli.
- Arbitrary specified Pauli: for t>=2k, one decoder call identifies its
  unique relevant lift or a zero low-weight block. Error <=4sqrt(Pr[|Y|>k]).
- Tail calculations are exact factorial-moment bounds, not independence
  assumptions. Physical phases, Y operators and out-of-image labels stay.
- A radius in a record is an assumption, not a proof. Finite exhaustive
  checks and the explicit repetition-code proof have separate provenance.
- The all-size classical result depends on the earlier LOCAL UNREVIEWED
  marked-cluster theorem. The production FPRAS is not implemented here.

The four-cycle degree-one filter has perfect radius-one decoding and zero
weight tail, but its two-representative readout is 1 rather than the guessed
single-lift 1/2. This prevents dropping the doubled-margin condition.

## Live Artifacts

`replay.py --write` generates exact contract/tail plans, small native Bell
controls, and a 496-generator, 495-physical-qubit input with no Hilbert-space
allocation. Its majority decoder is genuinely nonlinear. The large-s
growing-degree ledger is symbolic only. These are comparator controls,
not hard oracle problems or speedup candidates.

## Gemini Integration After Verified Migration

Integrate the new reduction plans into the EXISTING readout evaluation path,
retaining conditional decoder-contract and unexecuted-estimator flags.
Do not mark old nonlinear decoder cases dequantized unless their margins
are actually proved. Expose total-energy versus density precision if used.
Run full repository validation then. No UI redesign or new registry system
is requested; main/staging/Git were not changed in this pass.

## Next Research Decision

Do not extend this into more easy nonlinear-code examples. A serious next
HDQI application must name a useful task beyond these specified Pauli
readouts, or an average-case decoder without the relevant worst-case margin.
Joint output sampling remains open. A source requiring only energy terms
with a uniform one-bit spare margin does not survive this comparator.
Independent proof review and prior-art assessment remain missing; do not
reuse the consumed one-Rees-reviewer authorization for a new reviewer.
