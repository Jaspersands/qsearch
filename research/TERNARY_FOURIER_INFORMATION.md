# A Source-Aware Information Ceiling For Local Fourier Readout

LOCAL DERIVATION / REVIEW PENDING. This measures the information cost of the
all-outcome Fourier receiver, not its computational hardness or impossibility.
No novelty, accepted candidate, speedup or cryptographic attack is claimed.

## A Native Source Fourth Moment

Condition on original curvatures, native low ell rows, all low-only selections,
Gaussian frames, source pointer/syndrome outcomes and uniform injection words.
Do NOT condition on full high alpha/delta public metadata in this SOURCE
expectation. Under the physical IID premise, selected odd inputs have

    a=ell+3alpha, c=2a+3delta,
    alpha,delta independent uniform in Z_q^n.

The resulting full-root phase, including exact carry division, consists of
fixed low terms plus alpha.t(z)+delta.1[t(z)=2], summed over physically
distinct selected inputs. Each physical t is an affine permutation of a
known F3 linear form in the retained d coordinates. Translation and domain
sign do not change whether two pairs of physical trits have the same multiset.

Fix ANY nonzero secret s in Z_q^n. Its effective order is q_s>=3; alpha.s
and delta.s are independent uniform at that order. A phase fourth moment
at words z1,z2,z3,z4 survives the source average exactly if EACH selected
physical trit satisfies

    multiset{t(z1),t(z3)}=multiset{t(z2),t(z4)}.

To prove necessity, the delta coefficient is the difference in the count
of trit2, in[-2,2]; zero modulo q_s means zero as an integer. After that,
the alpha coefficient is the difference in the count of trit1, again in
[-2,2], so it also vanishes exactly. These count equalities give the multiset
condition even at q_s3. Sufficiency cancels every local frequency including
the fixed low carries, so the surviving moment is1, not an arbitrary phase.
The full-rank physical frame ensures that these conditions imply
z1-z2+z3-z4=0 over F3, the additional word-Fourier fourth-moment constraint.

Let D=3^d and E be the number of ordered four-word tuples satisfying that
physical multiset condition. The exact conditional SOURCE expectation is

    E_source[sum_t P(t|s,labels)^2]=E/D^3, s!=0.

This is not a collision estimate after the full labels are fixed. Mutual
information below DOES condition on those labels, then averages over their
physical source distribution; these are different conditioning operations.

The first-stage selector reads original LOW ell signatures only. A later
curvature selector can read delta mod3, even if called a "low" selector at
the output root. That conditioning does NOT satisfy this theorem's premise.
For example, restricting field-root outputs to c=2a makes every nonzero-secret
phase linear and its Fourier collision1, not5/9. The optional second-stage
factory needs a new conditional source-law analysis; this bound cannot be
imported to dismiss it, or to any high-label-filtered source family.

## Compact Certificate: Separate Unordered Word Pairs

For each selected physical direction L, unordered trit pairs are uniquely
specified by their sum and sum of squares in F3. If the forms L span the
linear coordinates and their squares span all d*(d+1)/2 quadratic features,
equal physical pair multisets determine both

    z1+z3=z2+z4,
    z1*z1^T+z3*z3^T=z2*z2^T+z4*z4^T.

Since2 is invertible, this determines the outer product of z1-z3. Equality
of rank-one outer products over F3 implies equal vectors up to sign, also
in the zero case. Thus the unordered WORD pairs coincide. Exactly

    E=2D^2-D,
    mean Fourier collision=2/D-1/D^2.

The implementation checks the actual selected source-frame directions,
not just the declared compact output table. A rank check is polynomial in
the source frames and d. Full square rank is sufficient, not necessary.
If it fails, an explicit ordered-pair census counts multiset keys in O(D^2)
and obtains E exactly at bounded widths; a missing rank certificate is not
silently promoted when that census exceeds its cap.

## Information Cost Even With The Best Classical Decoder

For each public label realization, Shannon entropy dominates collision
entropy. Jensen gives, for every nonzero secret,

    E_labels[H(T|s,labels)] >= log D-log(E/D^2).

For s0 the state is flat and its word-Fourier outcome is deterministic.
With a uniform full-root secret, G=q^n, therefore

    E_labels[I(S;T|labels)]
      <= c+(log D-c)/G, c=log(E/D^2).

With a full-square-rank certificate c=log(2-1/D)<log2: approximately ONE BIT
per output, not d trits. The displayed tiny1/G correction must not be dropped
as an exact assertion. This is an ensemble-mean upper bound, not a pointwise
bound for every favorable label realization.

For B independent output measurements, their distributions factor conditional
on S and all labels. Entropy subadditivity bounds total mean information by
the sum of these per-output costs. The shared public frequency shift in the
all-record instrument just relabels a uniform secret, so the same bound holds.
Fano's inequality gives the necessary condition for mean full-secret error e:

    sum_j information_upper_j >= (1-e)*log G-h(e).

For certified outputs this requires B=Omega(n*log q) even if each output
contains d=O(log n) quantum trits and an unlimited classical decoder is used.
This is still a POLYNOMIAL sample requirement. It does not prove classical
inference intractable, invalidate the measurement or lower-bound coherent
collective receivers. Label-dependent bases, outcome-adaptive measurements,
nonproduct processing and evidence changing the secret prior are outside scope.

## Evidence And Research Decision

Controls use actual original-source factories at roots9/27 and check selected
physical rows. A complete81-word alpha/delta census mutates TRUE original
pivot frequencies at original root9, not an imagined supplied state. It
preserves acquisition supports and low frames; all9 resulting output frequency
pairs occur9 times. Direct Fourier probabilities give mean collision5/9 for
both nonzero field secrets and1 for secret0. This is a finite arithmetic
control, not proof of external physical IID supply.

The all-record route remains a positive target ONLY with B and original
source costs charged at this stronger information scale. Likelihood evaluation
is cheap for one secret; finding the secret is still missing. Wider factories
must be justified by computational structure or coherent decoding, not a
claim of d-fold information yield from these fixed Fourier measurements.
Do not treat this measurement-specific bound as a global quantum no-go.

```
python theorems/ternary_fourier_information.py --write
node research/certificates/ternary_fourier_information_crosscheck.js
python -m pytest -q tests/test_ternary_fourier_information.py
```
