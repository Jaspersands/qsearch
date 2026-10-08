# Exact Native Flat Certificate And Classical Extraction

LOCAL DERIVATION / REVIEW PENDING. A supplied classical moment completion
can now be checked and decoded exactly. There is still NO algorithm for
constructing that completion from native noisy measurements, no approximate
flatness theorem and no quantum speedup.

## What Changed

The finite-group construction in `NATIVE_FLAT_EXTENSION_TARGET.md` is now
implemented in `theorems/ternary_flat_character_certificate.py`. It compiles
the public unit-difference basis, all commutation sums, INTEGER q-loops,
every native frequency reconstruction and W=V+S translates. It charges the
actual enlarged dense matrix and field degree, not just the small input V.
Whole-object caps stop verification; no truncated matrix is accepted.

Input consists of the complete original matrix and complete extension matrix,
encoded as exact rational polynomials in zeta_q. Float/rounded coefficients
are not supported. The original block must remain EXACTLY unchanged. The
root is the full q=3^r, not a field3 stand-in.

The verifier checks Hermiticity, diagonal1 and ALL equal-difference entries.
An independent original base Gram block determines coordinates for every
extension node. Their reconstructed Gram matrix must reproduce every supplied
entry exactly: this proves rank(M_W)=rank(M_V), not approximate effective rank.
It avoids a full W-dimensional numerical rank or PSD eigensolve.

## No Trusted PSD Flag

The selected base block is used as a nonsingular Hermitian metric. Without
initially trusting its positivity, reconstruct every shift as an operator
on its exact coordinate space. Check metric unitarity, all original-vector
dependencies, every addition trace, commuting generators and q-order.
Finite-order projectors refine the anchor by generator root eigenvalues;
there are at mostR nonzero common branches. Recover each genuine secret via
the public full-root unit-basis inverse.

Check that each extracted weight is strictly positive, sums exactly to1,
and that those characters reproduce EVERY supplied extension entry. This
reconstruction itself certifies PSD, because it writes the matrix as a
positive sum of rank-one character matrices. An indefinite, signed character
mixture therefore cannot pass merely because it is translation-consistent,
flat and unit-diagonal. There is no floating eigenvalue/rank tolerance.

This is the constructive form of the conditional representation argument,
not an application of a general theorem with unverified assumptions. For
related background see the primary
[Laurent--Mourrain flat-extension paper](https://arxiv.org/abs/0812.2563).
Independent mathematical review and novelty checks remain required.

## Exact Weight Positivity

Rational weights are checked as rationals. Nonrational cyclotomic weights
must equal their exact conjugates; otherwise they are rejected. Real weights
use certified RATIONAL sign intervals, never a numerical sign tolerance.

Machin's identity pi=16*atan(1/5)-4*atan(1/239), alternating-series brackets,
and cosine Taylor remainder bound |x|^(2L)/(2L)! give rational intervals for
the real part of the coefficient polynomial. The pi interval radius is
propagated through cosine's Lipschitz constant1. Terms double until a strict
positive/negative interval is found. An unresolved sign is UNKNOWN, not PSD.
The identity can be checked algebraically: tan(4*atan(1/5))=120/119 and
tan(4*atan(1/5)-atan(1/239))=1 on the principal positive quadrant.

Exact zero is checked in the cyclotomic quotient first. No nonzero character
branch with zero/negative weight is accepted. Signs certify the specified
embedding zeta=exp(2*pi*i/q), not a different conjugate embedding.

## Calibrations Versus Discovery

Two controls use TRUE original native ring labels at level4/root9 (n2) and
level6/root27 (n1). Known character mixtures supply the matrices only to test
the certificate. The extractor receives no support secrets or weights.
These matrices were NOT learned from native noisy outcomes; accepting them
does not establish a decoder. Controls retain their actual ring-frequency
charts and explicitly deny external physical IID certification.

The existing roots9/27 higher-rank native counterexamples are retained too.
A public unit-difference saturation guard rejects their moment blocks before
constructing any enlarged matrix. They cannot admit a representing character
distribution or the required flat extension. Resource limits cannot hide
this exact contradiction. A legitimate HIGHER-rank, nonflat matrix may still
be a character distribution: rejection of flatness alone is not a global
nonrepresentation theorem.

Tests also include signed mixtures, unchanged original blocks, corrupted
equalities, integer loops, cap failure, outcome blindness and nonrational
positive/negative weights. Unknown/cap results are never accepted candidates.

## Costs And The Dequantization Consequence

The explicit cyclotomic field degree is2q/3. Projectors scan q eigenvalues
per surviving branch and compute q terms per eigenvalue, costing
O(n*q^2*R) charged vector terms, plus exact matrix operations. At mostR
character candidates survive. This is NOT q^n secret search, but it is also
NOT polynomial in log q; the current extraction requires q=poly(n) for a
polynomial-in-n claim. Rational coefficient heights and classical matrix
supply must also be charged; field arithmetic is not unit-cost bit arithmetic.
The report retains compact classical input bytes and rational coefficient
bit heights of the input and retained coordinates/operators/atoms. These
are measured retained values, not a certificate of every internal arithmetic
intermediate or a complete bit-operation complexity proof.

For any LINEAR score in these moments, some extracted character scores at
least as well as the moment matrix. Thus an efficient classical procedure
finding these certificates would also supply a classical decoding route for
that score. Held-out native prediction is still required. Native harmonic
score and full log likelihood are different objectives. Quantum state supply
does not supply a free classical moment matrix or free tomography.

## Remaining Barrier And Next Decision

Exact completion/flatness can be hard to find. A posterior with positive mass
at all secrets generally has full rank on the full group, even if numerically
concentrated. Approximate rank compression requires a new certified error
and native-source inference argument. The previous observable saturation
bound, often vacuous at noise harmonic1/3, is not such a theorem.

Do NOT add a generic optimizer and promote its small eigenvalues. The next
substantive target is either a costed approximate character-extraction law
under explicit spectral/constraint gaps, or native source structure that
makes a completion recoverable. Any promising classical completion is first
a dequantization check; a quantum opportunity needs a genuinely different
state-access/receiver mechanism, not a classical-matrix fit relabeled quantum.

`TERNARY_TRANSLATION_STABILITY.md` now tests a further failure mode: exact
q-order almost-commuting operators can have nonzero winding and stay far
from commuting in operator norm. A q-dependent pair repair is retained too,
but its sequential many-generator bound loses precision rapidly. Neither
establishes native approximate flat extraction or an observable-only no-go.

Gemini owns CLI/registry integration and full production tests/validation.
Run the mathematics-focused workflow with:

```sh
python theorems/ternary_flat_character_certificate.py --write
node research/certificates/ternary_flat_character_certificate_crosscheck.js
python -m pytest -q tests/test_ternary_flat_character_certificate.py
```
