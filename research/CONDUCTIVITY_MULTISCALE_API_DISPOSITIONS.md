# Conductivity multiscale API findings: checked dispositions

2026-11-12. Four distinct requests in
api_inputs/2026-11-12-conductivity-multiscale/dispatch.json. This note records
mathematics, not review votes. Independent correlated-tree and wavelet calls
are still active. Cross-scale Claude exhausted its output budget EMPTY:
no scientific result and no retry. The parent counterfamily was derived
independently and now has a complete parent-read internal proof.

## Variational/resolvent report (completed, fully parent-read)

Bundle: audits/claude_runs/2026-11-12-conductivity-variational-resolvent.

ACCEPT scoped local-window warning: a medium with two macroscopic constant
layers retains an arithmetic-versus-harmonic gap in zero-boundary local-cell
trial fields whose windows are microscopic relative to L. It is not a proof
against all hierarchical Schur or sampled variational algorithms. REJECT the
report's broad opening verdict claiming that entire class is falsified.
The later conditional wording is the correct boundary. No computational
lower bound follows from literal full-tree assembly costing N operations.

REPAIR Green-Kubo normalization. With normalized eta and f=D* a eta,

    K_j=<eta,a eta>-<f,(D* a D)^+ f>
       =<eta,a eta>-integral_0^infinity <f,e^(-t D*aD) f> dt.

There is NO factor2 in this energy correction. Mourrat's asymptotic-variance
sigma^2 has a factor2, not K_j's correction. The report's factor2 formula
and half-sized integral value are rejected. The independent uniform-decay
review gives the actual all-L spectral counterfamily; the report's unproved
intermediate t^-1/2 description is unnecessary. Likewise an assumed need to
average over all N sites is not a lower bound on possible estimators.

ACCEPT exact positivity identity T_(2m)=||Pi(Sigma Pi)^m Sigma eta||^2.
Squaring two independent noisy paths alone supplies no useful smaller
variance bound. Its one-column importance-sampling inequality follows from
Cauchy-Schwarz, but the asserted uniform discrete row-l1 asymptotic and an
intrinsic multiplicative n^r path lower bound are NOT established by that
inequality. Do not import either as a proved obstruction to all couplings.

## Conditional sampled Galerkin bracket (parent derivation)

For any finite evaluable trial potential space V and divergence-free current
space W, primal energy gives an upper bound U, and

    L=max_(J in W) [2<eta,J>-<J,a^-1 J>]

is a lower bound. Indeed the difference from exact K is the nonnegative
squared a^-1-norm distance from the exact minimizing flux. No corrector or
flux is supplied by this identity. Both are small quadratic optimization
problems if their actual Gram matrices are computed.

For Fourier modes 0<|k|_infinity<=p<L/4, take
psi_k=L exp(2pi i k.x/L)/(2pi |k|), real/conjugate-paired coefficients,
and the compatible discrete curl on faces. Normalized gradient energies are
in [4/pi^2,1], modes orthogonal; constants in W are included separately.
Since 1<=a<=rho, the primal and dual Gram eigenvalues have explicit positive
lower bounds. Actual basis values, material circuit and their products can
be sampled at uniform edges to approximate all entries; include the factor2
for two edge orientations. Entrywise Hoeffding bounds plus the known norm
bounds for minimizers pay an outward enlarged interval [L-eps,U+eps] with
polynomial cost in B,n,p,1/eps,log1/delta. Finite trigonometric evaluation
pays n extra bits for small frequencies; the report's precision shorthand
without n is insufficient. This is a conditional useful classical method,
not a proof that the interval always narrows at polynomial p.

A simple blindness witness needs a stricter frequency condition than the
report states. If the two-phase material has only coefficient frequencies in
q Z^2, mean half in each phase, and 2p<q, all nonconstant trial correlations
vanish. The exact bracket is [2rho/(rho+1),(rho+1)/2]. Both a and a^-1 have
that Fourier support. The condition p<q alone is insufficient for Gram
frequency differences. Thus the suggested L64, side8, p3 checker fixture
is NOT licensed by the claimed exact-diagonal argument (q=4,2p=6).
No extra fixture sweep is run. Corner-tail and union-subspace claims remain
unproved, and are not needed for the accepted conditional bracket.

## Primary wavelet baseline scope

Actual Beylkin--Coifman--Rokhlin1991 PDF retained as
sources/periodic_conduction/bcr1991.pdf with source hash metadata. Parent
checked Section4 compression discussion, Section4.6 and Section5/Remark5.1.
Its nonstandard wavelet representation pays O(N) application to a full
N-entry vector, with O(N) or O(N^2) setup depending on kernel knowledge.
This is a strong full-grid baseline, not a poly(logN) scalar estimator.
No theorem is inferred from the OCR-omitted mathematical kernel estimates.
The active wavelet request must pay material multiplication and sampled
coarse/fine interactions; ordinary matrix compression is not that operation.

## Independently verified source-rate counterexample

The full271line review conductivity-uniform-decay was parent-read. For the
one-bit layered medium and normalized f=D*a eta, write z=(rho-1)/(rho+1).
An explicit triangular corrector u has ||u||²=z²(L²+8)/48 and
Q=<f,A^+f>=z²(rho+1)/2. Its low spectral mass proves

 C_L(t)>=8z²/(3L²) exp(-48(rho+1)t/L²),
 R_L(T)>=z²/6 exp(-48(rho+1)T/L²).

Thus every L-uniform rate C(1+t)^(-alpha), alpha>1, is false; the required
prefactor grows at least L^(2alpha-2). The general alpha=1 bound follows
from Q<=rho and lambda exp(-t lambda)<=1/(et), so it is sharp in this
uniform exponent sense. Squared-semigroup identities have the same temporal
obstruction. Ordinary time cutoff is Theta_rho(L² log1/epsilon); the exact
geometric resolvent remainder persists through about2log2L levels.
These are source-assumption/cutoff falsifiers, not multilevel impossibility;
long FREE heat times are already efficiently sampled by the prior baseline.
The layered answer itself is the classical harmonic mean.

## Terminal correlated-tree and Haar reports: checked

Both OpenAI reports read in full; the stable224line independent review
2026-11-12-conductivity-api-sampler-attacks.md was also fully parent-read.
ACCEPT the exact period-four shared-translation bias (-1/2 versus-3/8),
including all mixed scales. Martingale E[uv]=0 does not survive insertion
of Sigma: E[u Sigma v]=-1/4 on the explicit two-bit law.

ACCEPT the unbiased antithetic four-corner repair but reject its target
variance: with independent factor innovations and separate uniform start,
EVERY full-support joint SCALE law gives EZ²>=3(H²/16)^m. This includes
scale correlations, not innovation/start-adaptive laws, covariance-corrected
factor coupling, grouped cancellations or circuit-specific simplification.
Upper constants64(second)/4096(fourth) and conservative finite-transcript
V=(256H²)^m are checked for the specified near-uniform PRODUCT scale law.
No backend implementation or test was inferred from that written clock.

ACCEPT separable tensor-product Haar parity path identity:
absolute path sum=(n-1)^(r/2) for evenr. Any ungrouped single-complete-path
importance estimator has second moment>=(n-1)^r; it is variance for positive
evenr because mean0. r0 variance0; oddr has no nonzero complete paths.
The actual moment vanishes by U0^T u=0, so grouping solves this easy family.
The coarse-to-fine vector lower bound and rank<N/4 failure concern the whole
specified overlapping block, not arbitrary separated blocks/bases/sketches.
Native entry estimates pay one circuit draw from a known overlap envelope;
they do not sample unknown absolute entries or obtain relative entry accuracy.
No generic wavelet, classical-hardness or quantum-separation claim follows.

## Full scalar-output consequence and final scope

Completed Claude full-energy-excursion report parent-read/checked. The actual
native series convention was already proved independently; the report's
laminate check is only corroboration. Accepted stronger uniform-in-r window
inclusion-exclusion proof is written in CONDUCTIVITY_SEPARATED_SCALE_ATTACK.
It proves limiting shortcut error c z^4/[2(2-z²)] on the actual scalar output
for every w=o(n), uniformly in the finite series length. Corrected q/q0 reuse,
AT MOST window multiplicity at the lower boundary, and unproved O(1/L)
interface heuristic (proved O(L^-1/2)). No new control/sweep is necessary.

All five paid tasks are terminal: four completed/nonempty, one cross-scale
empty truncation, no findings/retry for the latter. Frozen46hashes and usage:
audits/controls/conductivity_multiscale_round/. Round estimatedUSD7.399194,
cumulative149.879808 across131priced records; twoUNKNOWN historical bills
excluded. Estimates are not invoices or balances. Full all-circuit joint-poly
classical conductivity match remains OPEN; these specified sampler failures
are not hardness. After independent comparison, the next pass selects native
local Jacobian halving instead of another adjacent conductivity barrier.
