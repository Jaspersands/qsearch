# Secret Coordinates, Not Every Auxiliary Feature

Constructive classical comparison and conditional source analysis; external
review and Arora-Ge prior-art comparison pending. No unbounded-Gaussian solver,
usable-multiple producer or quantum algorithm is supplied.

## Exact Affine Coordinate Certificate

Linearize the actual mod9 integer-divided cubic equations overF3 as before.
RREF the WHOLE augmented matrix. An original low-secret coordinate is fixed
across its entire affine solution space iff it is a pivot and its reduced
row has zero coefficients at EVERY free column. Nonpivots and pivots with
free dependence remain unknown. No particular assignment to free variables
is a certificate. Inconsistent systems and whole-matrix caps stay explicit.

Recover the certified low trits u, then compute their actual canonical
squares, mixed quadratics and cubics. For the cubic method, solve next trits
v with these features fixed. Verify EVERY compiled equation and perform the
existing unit-minor/Hensel full-root lift and complete original alphabet fit.
The signed-only quadratic method also uses certified secret coordinates,
then verifies actual squares. It does not silently accept zero-error noise.

Full-rank nonphysical feature vectors remain rejected. Rank-deficient
systems can succeed, but only if the real secret coordinates are fixed and
their canonical substitution is consistent. Other nonlinear identifiability
is not guessed. Certificates retain reduced nonzero rows, pivots, free
columns and per-coordinate dependence; independent replay reconstructs them
from actual original records. Stored RREF is an observation, not a granted
oracle. Two cubic field eliminations and all original verification are paid.

Any alphabet-compatible secret must satisfy the compiled affine system,
so it has the certified u. Its actual nonlinear features then force the
certified v. The original higher-root unit minor and spacing separate the
remaining digits. This establishes fixed-instance alphabet-compatible
uniqueness, NOT planted truth under a false source promise.

## Why Zero-Error Base Rank Suffices

Use the preceding Gaussian quotient derivation's secret translation ONLY
in the proof. Zero-error rows span the D-K base, K=n(n+1)/2. In translated
coordinates their high-label trits force u=0. The linear low-label columns
force v_i-u_i^2=0; once the actual canonical squares are enforced, v=0.
The remaining mixed-cubic constraints are also satisfied. No independent
rank of the rare-noise quadratic feature block is necessary.

Undoing the secret translation preserves affine uniqueness of the low u
coordinates, since those coordinates transform affinely independently of
the auxiliaries. Next-digit carries depend only on canonical low features,
which the second solve enforces. Thus the actual decoder does not need to
know the proof's translation or identify zero-error rows in the dataset.

With p0 a true zero-error probability floor in the independently truncated
triplet law, sufficient source failure is bounded by

    ((3^(D-K)-1)/2)*(1-2p0/9)^m + whole_bank_triplet_tail.

The adapter, original Gaussian radius, code separation, entire valuation
union and missing external coefficient/multiple coverage remain charged.
This needs the actual IID label/noise laws, not successful finite fixtures.
The conditional row order is O((D-K)/p0), rather than demanding rare-noise
quadratic rank. The old full-feature bound remains a sufficient comparator,
not a necessary sample count or lower bound.

The translation acts invertibly on the ENTIRE affine feature space, not
only on physical embedded points: the constant, canonical monomials and
linear next-digit coordinate functions are linearly independent overF3.
Their translated expansions stay in this basis; translating back gives
the identity on independent functions, hence on coefficient matrices.
This is why the proof implies affine coordinate uniqueness before nonlinear
substitution, rather than merely physical-model identifiability.

## Controls And Scope

Original-record controls include the rank25/34 n4,3^16 probe, a rank129/164
n8,3^64 low-noise example, a zero-noise case, and strict signed quadratic
noise. No artificial oracle problem or free input secret is introduced.
The source ledgers use declared decreasing Gaussian widths and keep matrix
costs/caps visible; large profiles are not claimed as executed huge-bank
experiments. Gaussian boxes use trusted Arb, with a separate same-library
replay, not an independent transcendental proof.

The Gaussian quotient completion API now uses this decoder by default.
The former full-feature solver is retained only as an explicit costed
comparison. The current three ledgers require1610,60490,3579210 rows;
the prior full-feature sufficient bounds at the same widths were about
7.7e8,6.1e16,9.1e17. Only the n8 logical matrix fits the default2million
entry cap. These are improved CONDITIONAL SUFFICIENT BOUNDS, not empirical
speedups or claims that the previous counts were necessary.

    python theorems/native_partial_coordinate_decoder.py --write
    python theorems/native_partial_coordinate_decoder.py --check-probabilities
    node research/certificates/native_partial_coordinate_decoder_crosscheck.js
    python -m pytest -q tests/test_native_partial_coordinate_decoder.py
