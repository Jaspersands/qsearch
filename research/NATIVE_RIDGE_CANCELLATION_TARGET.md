# Next Constructive Target: Depth-Independent Ridge Cancellation

FIRST STAGE IMPLEMENTED / OPTIONAL SECOND STAGE NOT IMPLEMENTED /
LOCAL DERIVATION REVIEW PENDING. See `TERNARY_RIDGE_CANCELLATION.md` and
`theorems/ternary_ridge_cancellation.py` for the actual first-stage factory.
Use `ternary_native_phase_identity.py`, not expanded high-degree tensors.
This is a proposed phase-shaping primitive, not a decoder or speedup.

## Cancel The Native Odd Top At Any Depth

Fix d logical data coordinates and n secret components. Let
P_d=(3^d-1)/2 be the number of canonical nonzero projective forms L over F3.
Each actual sourced program has normalized numerator tables T_j,L,l at
modulus N=3^(r+1), with T(2)=2T(1) mod3 and global kernel

    sum_L a_j,L,l * L = 0, a_j,L,l=T_j,L,l(1) mod3.

These signature vectors live in a space of dimension at most n*(P_d-d):
the map sending coefficients to sum_L a_L*L has rank d, because the ambient
projective dictionary contains all coordinate forms. Therefore

    B_odd = n*(P_d-d)+1

actual programs guarantee a nonzero F3 relation c_j among their LOW ridge
signatures. Use exact Gaussian elimination on only occupied dictionary keys;
the ambient dimension bound does not require materializing all projective
forms. All B_odd acquisitions are charged, including c_j=0 states. The
relation must read only these low signature residues, not high linear digits.

Signed one-use injection gives shifted local tables

    T_j,L,l(L*m_j+c_j*t)-T_j,L,l(L*m_j).

Their new low linear coefficient is c_j*a_j,L,l, independently of m_j.
Thus every aggregate table is divisible by3 for EVERY injection transcript.
Divide each table only AFTER this per-key certificate, obtaining ordinary
normalized tables at retained root q=3^r. The exact local valuation bound
then gives GLOBAL additive degree<=2r, instead of2r+1. The root is not
automatically reduced; no unknown inverse, cloned program or rare outcome
is needed. Charge source ancestors and all original measurements/injections.

With K=d+n odd inputs per program, each acquisition charges
(d+n)*(n+1)^2 original inputs. This first stage has source cap
B_odd*(d+n)*(n+1)^2=O(n^4*3^d+n^3*d*3^d), independent of r except public
bit arithmetic. For constant d or d=O(log n), this is polynomial. For
d=poly(n), the ambient guarantee is exponential; do NOT hide that fact.
At d1 the signature space is zero-dimensional and the stage is trivial:
one standardized qutrit already has local degree<=2r. This is not evidence
of a breakthrough. Only explicit useful higher-width/output-law evidence
can establish research value.

## Optional Second Stage: Cancel The Even Top

For independently acquired first-stage output programs, each per-key phase
table is now an integer-valued q-root function f with canonical F3 values.
Let kappa_L,l=f(2)-2*f(1) mod3. Translation of its F3 quadratic reduction
preserves kappa, and domain sign2 scales it by2^2=1, not by2.

Use a BINARY support zero-sum, not an arbitrary F3 coefficient relation for
this even top. The existing F3 diagonal SDE can find a nonempty support from
(n*P_d+1)^2 curvature-signature vectors. Inject each selected output ONCE,
keep every outcome, and cancel every per-key curvature. The resulting local
tables satisfy f(2)=2*f(1) mod3, hence global additive degree<=2r-1 by exact
valuation certificates. This is a conditional constructive derivation,
not an implemented factory. Its straightforward source cap is polynomial
only while the chosen dictionary width is; charge complete first-stage
cohorts for every supplied second-stage program, not just selected supports.

At r1 the final state is an ordinary linear field3 phase and Fourier readout
is known. At larger r it remains a NONCLASSICAL phase at root3^r, not an
ordinary F3 character. The visibility bound says2r-1 is already the minimum
degree for full phase order3^r. Driving all degrees lower will lose secret
residue digits unless another register/channel carries them. Two degree
drops DO NOT provide a full-root Fourier decoder. The n*(r) information
requirement and actual label law remain separate obligations.

## Research Decision And Tests

The first stage is implemented as a depth-independent source-accounted
primitive, with bounded transcript checks, exact denominator handling,
degree valuations and original-root phases. Include full high-root controls
whose component frequency family has order q (not merely a q label attached
to field3 phases). Search for an output observable or persistent-program
construction that USES the retained higher-depth structure before investing
in extensive second-stage infrastructure.

Falsifiers: relation chosen from high metadata; c2 implemented as two copies;
translation changes the predicted low signature; per-group divisibility
fails; rare outcomes are excluded; a sparse occupied dictionary is called
a guarantee for arbitrarily many new source-dependent keys; a degree bound
is called an efficient decoder; or source counts/rank/error claims are
inherited from unrelated IID inputs. Compare any decoder against known
cyclotomic sieves under the SAME sample budget and error model.

The likely failure is straightforward: phase shaping stays polynomial at
small d but cannot decode n high-modulus secret coordinates without another
hard step. Larger d may make relation search exponential. The prior primitive
already exposes this gap with explicit higher-root quadratic counterexamples.
Do not reinterpret a successful degree-drop test as resolving it.

The first collective receiver attempt is implemented and costed in
`TERNARY_COLLECTIVE_CHARACTER_RECEIVER.md`. Its exact character feedforward
has exponentially weak direct correct yield at growing roots. All-record
classical likelihood inference and noncharacter collective transforms remain
open; the yield ceiling does not rule them out. Do not build the optional
second stage without a receiver exploiting it.

GPT owns this construction/source-law/receiver analysis. Gemini owns CLI,
registry/UI wiring, full production validation and integrated Git backups.
