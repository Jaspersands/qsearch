# Native Short-Preimage Reduction

Local constructive derivation / external review pending. This is a reduction
and an admission falsifier, not a polynomial short-preimage solver or a new
quantum speedup. The existing DCP projected-encoding and canonical-erasure
modules already address comparison normalization; this pass connects the
missing helper to the actual original noisy-linear data.

## Actual Helper Interface

The previous group workbench uses, for each original label pair a,c,

```
selector0: frequency a,    response y1,      coefficients(1,0)
selector1: frequency c-a,  response y2-y1,   coefficients(-1,1)
selector2: frequency -c,   response -y2,     coefficients(0,-1).
```

A word chooses one selector per source pair in one cohort. Its total
frequency is sigma, and its response is eta=y.beta (modq). The active
coefficient vector beta has squared Euclidean norm at most2M, where M is
the number of source pairs in a cohort. This is the real word/frequency map
of the coupled native source, not an invented value oracle.

The helper receives ONLY q, dimensions and public paired labels. It does
not receive values, mask, original source IDs, secret, or errors. Receipts
bind to a canonical public-family hash, name the requested target/cohort/word,
and are independently checked against the actual public map. A successful
helper response is not trusted merely because it says it found a preimage.

A label-only API is not a proof that an arbitrary caller obeys it: closures,
external data and uncharged source access remain explicit audit obligations.
The noise theorem below is conditional on true label-only operation and
original errors independent of labels/helper randomness. No finite receipt
or matching hash establishes those independence promises.

## Original-Data Classical Decoder

For q=3^r and original secret s in(Z_q)^n, request all nr NONADAPTIVE targets

```
sigma_(i,d) = 3^(r-1-d) * unit_i,   d=0,...,r-1.
```

Verify each helper receipt, evaluate eta on the given original responses,
and only THEN reconstruct the trits. If the known lower prefix of s_i is u,
subtract3^(r-1-d)*u from eta. The ideal remainder is a multiple of q/3.
Choose the nearest of0,q/3,2q/3 using EXACT circular integer distance. Its
trit extends u. If every unwrapped response error is smaller than q/6,
induction recovers every coordinate, including zero. No all-secret search,
quantum phase sampler, fresh original noise or true-secret check is used.

When the known source mask m is present, evaluate masked responses from
actual values plus a.m, recover s+m, then subtract m classically. The helper
still sees no response or mask. The same original dataset supplies every
probe. Repeated ancestors are legal classical data reuse, not new IID errors.
Exhaustion, a mismatched/invalid word, or a helper's failure returns an
explicit incomplete result; there is no accepted-only success assertion.

## Noise And Helper-Failure Ledger

Condition on all public labels and label-only helper randomness. With
independent zero-mean original integer errors E e_j^2<=V,

```
E(e.beta)^2 <= V*||beta||^2 <= 2M V
Pr[|e.beta| >= q/6] <= 72M V/q^2
Pr[any decoding error] <= min(1,72*n*r*M*V/q^2 + helper_failure_upper).
```

The probes may have overlapping original ancestors and correlated response
errors; the proof uses a union bound, NOT independence of derived probes.
Targets are fixed before reading responses. A wrong early trit cannot be
quietly corrected by consulting the secret. A uniform public helper-failure
promise may cover the full batch or be summed over calls; it is not measured
from a few successful small instances.

An OPTIONAL conservative alternative permits helper choices depending on
responses, under the same coefficient bound: for any beta in one cohort,
(e.beta)^2 <= 2M*||e_all||^2. With2BM originals, simultaneous failure is
bounded by min(1,144*B*M^2*V/q^2 + helper_failure_upper). This is one global
moment event, not a union over adaptive choices. It still assumes the true
original second moments and the verified bounded word coefficients; it does
not infer noise quality from a selected small response. It is deliberately
weaker and does not turn arbitrary data-dependent helper access into an
efficient preimage algorithm.
Unlike the label-only variance argument, this pathwise global bound needs
neither centred nor mutually independent original errors, nor independence
from the labels or helper choices. Uniform marginal second-moment upper
bounds suffice. Its larger coefficient is the price of that weaker premise.

For M=n^2+24 and V=q^2/(3n^6)+1/2, the label-only bound tends to zero even
at exponential modulusq=3^n. Thus granting a polynomial classical short-
preimage helper would already grant a polynomial classical original-secret
decoder in this regime. Calling the helper a harmless quantum compilation
step hides the main problem. A genuine QUANTUM-only efficient preimage
mechanism could itself be a major SIS/LWE result; this reduction does not
exclude it and does not assume classical hardness as a theorem.

## What Is Implemented

The general receipt-checked decoder consumes an EXTERNAL helper and never
constructs one silently. The only provided helper is a BOUNDED EXHAUSTIVE
LABEL-ONLY CONTROL. It enumerates B*3^M words, reports that count and has a
hard finite cap. It demonstrates the reduction, not efficiency at scale.
Missing frequencies remain missing. Its complexity is exponential in M;
even if all requested probes happen to exist, this does not become a new
algorithmic claim or a chosen-query oracle for free.

Controls reconstruct ideal original records, exercise
missing/wrong receipts, and preserve noisy failures. All public-family
fingerprints, probe words, signed responses and trit decisions can be replayed
with exact arithmetic. Scalable moment/cost ledgers do not enumerate words,
frequency targets, q^n secrets or q-sized phase tables.
The general decoder is also tested at root3^64 on an explicitly easy,
deterministic chosen-label fixture; that fixture does not establish uniform
random-label coverage or an efficient LWE algorithm. Public evaluation checks
that the supplied response records match the receipt's actual label family.

Falsifiers: a helper reads hidden/noisy response information while using the
label-only variance bound; a receipt has the wrong frequency or family; derived
records are declared independent; an incomplete probe batch is called recovery;
enumeration is called polynomial; or a classical preimage implementation is
presented as evidence of a uniquely quantum speedup.

Run `python theorems/native_short_preimage_reduction.py --write`, its tests and
`node research/certificates/native_short_preimage_crosscheck.js`. Physical
quantum gates, a scalable preimage solver, new speedup or full hardness
transfer are not supplied. External proof review and production admission
integration remain obligations.
