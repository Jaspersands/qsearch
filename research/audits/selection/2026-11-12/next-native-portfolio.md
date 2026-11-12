# Next native portfolio: select conductivity's joint-precision boundary

2026-11-12. Independent selection after current STATE/TRAPS/GOAL. No
surface continuation, network, API, Git, new implementation, or archive
reading. Local corpus lookups used `/opt/anaconda3/bin/python`.

**Select ONE direction: fixed-contrast effective conductivity on succinct
periodic materials, at inverse-polynomial accuracy.** The next mechanism
to test is a correlated multiscale classical estimator for the complete
scalar observable. A successful estimator would decisively match the
written quantum algorithm. A failed coupling is only a failed classical
attack, never evidence of hardness. This choice has the best combination
of an externally meaningful output and an already paid end-to-end quantum
contract; it is not selected merely because a nearby proof remains open.

## Three independently scoped contenders

### 1. Succinct periodic conductivity — selected

**Input/output.** An entire size-B Boolean circuit specifies conductivities
in {1,rho} on the 2D torus of side 2^n, for fixed rational contrast rho>1.
Both algorithms receive the same circuit. Output the scalar finite-cell
effective conductivity K_j to additive epsilon with failure at most delta.
No IID, smoothness, mixing, or finite-correlation promise is added. This
models a macroscopic transport observable of a compactly specified material.

**Mechanism and target.** The repository's finite contrast series uses
the normalized gradient projection Pi and explicit Fourier arithmetic.
Fresh-flag projection blocks and unpostselected Hadamard tests estimate
the series in poly(B,n,log(1/epsilon))*epsilon^-2*log(1/delta) gates.
Uniform input preparation, material evaluation, small Fourier denominators,
arithmetic precision, and the zero-correction case are paid in the note.
At epsilon=n^-a for fixed a>0 this is polynomial in the native input size.

**Strongest matched baseline.** The paid marked heat-path estimator has
cost poly(B,n,1/epsilon,log(1/delta))*n^O(log(1/epsilon)), with finite-bit
sampling and errors included. It already matches fixed precision. Full-grid
FFT/CG, exact layers, and IID homogenization are additional baselines under
their actual access/ensemble assumptions. Full polynomial dependence on
both n and 1/epsilon for ALL coefficient circuits remains unproved here.

**Decisive next question.** Can shared heat increments and dyadic-scale
cancellation give an actual estimator with the bound specified below?
This tests the same K_j, not an easier coefficient ensemble or an assumed
corrector. A positive theorem closes this candidate by a classical match.

### 2. Native Ring-LWE recovery by short preimages — not selected

This direction is absent from the current front-state. **Input/output:**
two independent original records over Z_q[X]/(X^d+1), power-of-two d
and the audited q near d^4,
public ring labels, the actual small-secret/noise law, and a held-out
record; recover and verify the secret in poly(d,log q) time. Its external
value is cryptographic, provided the original distribution/access contract
is preserved; no hardness or security claim is imported.

**Concrete mechanism:** exploit the public rank-two NTRU-form/isodual
lattice through quantum Fourier/Gaussian operations to return measured
short preimages of chosen syndromes, then use the already written
classical two-query correlation decoder. Public modular arithmetic,
membership tests and the conditional moment-to-decoding reduction are
specified. The required sampler, its success probability and its useful
second-moment certificate are NOT paid. A centered homogeneous sampler
is a weaker alternative, but also needs label entropy and remains missing.

**Baseline/falsifier:** exact public LLL/Babai with its actual Gram--Schmidt
radius, dual/hybrid attacks, and classical Gaussian sampling with the
same basis/access. Ambient-Gaussian postselection on a chosen syndrome
has about q^-d mass; generic amplification remains exponential. The
audited native Klein and local-walk constructions do not remove this
cost. Isoduality is not a short basis. **Next proof question:** give the
actual structured sampler with polynomial total cost and certified abort/
moment bounds strong enough for a positive correlation-decoding gap,
without a trapdoor or chosen-preimage oracle. This is still the central
unsolved algorithm, so another decoder refinement has low immediate value.

### 3. Native polynomial quadratic-character reconstruction — not selected

**Input/output:** coherent chosen BASE-FIELD BIT access to the padded
quadratic character of an unknown monic squarefree degree-d polynomial
over F_p, p>=256d^2; recover its coefficients with charged verification.
This is a structured character/PRF recovery problem, not arbitrary
black-box secret finding. The intended target is poly(d,log p) gates,
queries and workspace with inverse-polynomial total success.

**Mechanism:** nonlinear processing of native BIT transcripts to prepare
a broad resultant-character phase, followed by the coefficient Fourier/
Hankel receiver. A usable broad ideal phase has a decoder; its native
relative nonsplit phases are missing. Already on irreducible targets,
the split-support Fourier/Hankel receiver has the proved d^-d success
ceiling. The explicit 4d-query AND-phase escapes the
bounded parity-l1 obstruction, but does not prepare the needed source.

**Baseline/falsifier:** O(d log p) classical chosen queries suffice with
p^d candidate enumeration; actual polynomial-time reconstruction is not
established by that query bound. The AND-phase escape as written, after
uncomputing its transcript, depends on Q through only ONE bit H(Q).
That output alone cannot recover a uniform target from an exponentially
large family, regardless of its exponentially large parity expansion.
**Next proof question:** construct a complete relative broad phase or a
different informative full output law from nonlinear BIT operations,
with polynomial gates and total success, rather than only escaping a
restricted source bound. There is no new admitted mechanism to dispatch
yet, and query-model cryptographic value is narrower than the selected
fully explicit circuit-input transport observable.

## Exact next proof obligation for the selected direction

Use the existing contrast expansion, with c=(rho+1)/2 and
z=(rho-1)/(rho+1):

    K_j=c[1+z<eta_j,Sigma eta_j>
         -z^2 sum_(r>=0)(-z)^r T_r],
    T_r=<eta_j,Sigma Pi(Sigma Pi)^r Sigma eta_j>.

Keep r<k=O_rho(log(1/epsilon)). The existing independent marked paths
have second moment [O(J^2)]^(r+1), where J=O(n+loglog(1/epsilon)).
Repeating that argument, changing the contrast constant, or estimating
each dense kernel entry is not a new operation.

The proposed new attack is to retain CORRELATIONS across dyadic heat
scales, rather than independently resampling a scale at every projection.
For K0=D*D and V=D K0^(+,-1/2), the exact bands are

    B_small=V(I-exp(-K0))V*,
    B_s=V(exp(-2^s K0)-exp(-2^(s+1)K0))V*.

They are positive, commute, and their sum is the truncated projection.
This is an ANALYTICAL decomposition, not permission to sample V or a
dense band kernel for free. A proposed sampler must specify the joint
law of its shared random-walk/Poisson increments, antithetic or martingale
corrections, material-circuit calls, and finite-bit implementation.

A sufficient, concrete acceptance test is an estimator Y_r of T_r whose
bias is at most epsilon/poly(k), with, for absolute fixed exponents a,b,

    E|Y_r|^2 <= (n+r+log(1/epsilon))^a C_rho^r,
    expected work <= poly(B,n,r,log(1/epsilon))*C_rho^r,

and a paid bounded-clock/failure version. C_rho must be independent of n
and of the material circuit. Since r=O(log(1/epsilon)), these bounds give
a complete classical polynomial match after allocating moment errors.
An equivalent direct estimator of the entire series is also sufficient.

First analytic falsifiers: constant and layered materials, and a circuit
combining separated dyadic spatial scales. The scalar answers for layers
are already classical. If the proposed correlation still leaves n^Omega(r)
variance even there, reject THAT estimator before any API refinement or
simulation. Conversely these controls cannot establish a uniform bound:
arbitrary circuit coefficients can mix frequency bands, so cancellation
must be proved without smoothness/IID assumptions. Do not infer a quantum
separation if this attack fails.

## Evidence and source gates

Read topic notes: `PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`,
`CHARACTER_BROAD_PHASE_SOURCE.md`, `LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md`,
`NATIVE_RLWE_{COVARIANT_DECODER_TARGET,CHOSEN_PREIMAGE_REDUCTION,
HOMOGENEOUS_DGS_REDUCTION,GAUSSIAN_SAMPLER_AUDIT}.md`. The Kummer
perturbation note was also checked for triage; its missing reduced-coordinate
and halving interface would continue an arithmetic conditioning bridge,
with less immediate evidence of a new end-to-end quantum mechanism.

Local `been-tried` and `baselines` searches were run for all three topics:
succinct periodic conductivity/Riesz-Neumann estimation; native Ring-LWE
chosen short preimages; and Legendre polynomial character recovery. They
returned the scoped notes/barriers above. The baseline catalog had no
named conductivity or Legendre match; that is NOT evidence of absence.
For Ring-LWE it returned LLL/Babai. No literature search was performed
because this task prohibited network access.

Published-source claims inherited from these notes, including IID
homogenization, signed-path sampling, Gaussian preimage algorithms and
character-learning literature, NEED PARENT PRIMARY-SOURCE CHECK before
being used in the next theorem or novelty comparison. Ring-LWE local
reduction notes themselves retain review-pending status. This selection
does not promote them. No speedup, hardness, separation, novelty, quantum
execution, or general classical lower bound is claimed.
