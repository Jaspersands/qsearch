# Structured EDCP: A Profile-Matched Classical List Decoder

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

This is a conditional algorithm and resource comparison, not a new short-basis
algorithm, an unconditional EDCP solver, a classical simulation of the source,
or a novelty claim. It closes a specific gap in the preceding Klein audit:
the case where the WHOLE rejection profile is manageable but deterministic
Babai's largest-direction bound is not useful.

## 1. Result And Scope

Given the same noise-independent public kernel basis used by a Gaussian-fiber
proposal, randomized nearest-plane decoding on its reversed dual produces a
list containing the true secret. Its cost is governed by essentially the same
theta profile as the universal-envelope quantum rejection sampler.

For the exact discrete noise, the certified list size is O(J^2). A sharper
O(J) bound follows after a charged classical uniform jitter, with all error
parameters displayed below. In the growing native regime, J and the quantum
rejection factor H differ by at most a constant. Polynomial H therefore also
permits polynomial classical list decoding AFTER local Fourier readout.
The sharper bound is consistent with a quadratic rejection-sampling benefit,
not a superpolynomial separation from that profile alone. This comparison is
of sufficient resource bounds, not an optimal lower bound on either method.

A list is NOT a decoded secret. Selecting its best marginal likelihood loses
at most the coverage error relative to full classical maximum likelihood.
If that full measurement lacks information, this algorithm cannot invent it.
Appending independent source blocks can add information without increasing H;
section 7 proves the basis-augmentation statement exactly.

Randomized lattice decoding itself is established prior art: see
[Liu, Ling and Stehle](https://arxiv.org/pdf/1003.0064), which analyzes repeated
Klein decoding and selection among sampled lattice points. The following
source-specific moment bounds and connection to our rejection profile are
derived directly. Classical sampling is not an invented new quantum primitive.

## 2. Contract And Notation

Use the full-kernel, width and source contracts from
`STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md`. In particular,

    Q=q^d+1, D=d*L, f=(a_l*q^i), a_1=1,
    Lambda={c in Z^D: f*c=0 mod Q}, det(Lambda)=Q,
    K is an explicit COLUMN basis of Lambda,
    g_i=||b_i^*||, C=K^(-T)*J_rev,
    h_i=||c_i^*||=1/g_(D+1-i),
    s_G=sigma/sqrt(2), tau=1/(2*s_G), r_e=Q*tau.

Here J_rev reverses columns; it is not the scalar profile J below. The basis
may be computed from public labels, but MUST NOT be chosen using the noisy
observation, unknown secret, or jitter. Charge its computation. A center- or
fiber-dependent basis is outside this fixed-basis certificate.

The ideal classical measurements are y=f^T*x+e mod Q, where the integer
coordinates e_i have mass proportional to exp(-pi*e_i^2/r_e^2). Thus
y/Q=lambda+e/Q for a true lambda in Lambda^*. The true lambda can depend
on the chosen modular representatives; all formulas are translation invariant
under dual-lattice points. The secret is lambda's first coordinate times Q
modulo Q. Independent noise, rather than a specific secret prior, is needed.

Put theta(t)=sum_k exp(-pi*k^2/t^2) and define

    J = prod_i theta(g_i/s_G),
    H = (s_G/theta(s_G))^D * J.                               (1)

H is exactly the preceding note's universal-envelope factor, not an
unexplained new score. Calculate logarithms for large profiles.

## 3. The Actual Randomized Decoder

Run Klein's randomized nearest-plane algorithm on C, centered at y/Q, with
PROBABILITY width tau. At coordinate i, conditioned on already selected
later coefficients, draw an integer from the one-dimensional discrete
Gaussian with center given by that residual and width

    beta_i=tau/h_i=g_(D+1-i)/(2*s_G).

Use ordinary independent randomness, not a coherent sampler. Equivalently
operate on the integer basis Q*C, integer-scale target y, and width r_e.
Validate every returned vector's modular code membership before extracting
its secret. Q*C is integral for this full index-Q kernel; generic rational
bases must not be silently cast to integers.

The construction requires conditional one-dimensional Gaussian sampling,
NOT an oracle that samples an arbitrary lattice Gaussian. At narrow widths
the Klein output need not be the target lattice Gaussian; that fact is fully
allowed in the proof. Repeat this procedure and deduplicate the secret list.

## 4. Exact Discrete-Noise Coverage Theorem

Let xi_i=<e/Q,c_i^*/h_i> and t_i=xi_i/h_i. Along the path returning the TRUE
lambda, subtracting its integer coefficients leaves the coordinate center
t_i. Therefore the exact probability p(e) of returning that lattice point
in one trial is

    p(e) = prod_i 1/sum_(k in Z) R_i(k),
    R_i(k)=exp(-pi*k^2/beta_i^2+2*pi*k*t_i/beta_i^2).          (2)

These are theoretical quantities, not secret-noise inputs to the decoder.
For nonnegative numbers, sqrt(sum R)<=sum sqrt(R), so

    p(e)^(-1/2) <= S(e)=prod_i sum_k sqrt(R_i(k)).

Expand this positive product. Let v_k=sum_i k_i*h_i*(c_i^*/h_i).
The discrete Gaussian MGF from the preceding note gives

    E exp(<v,e/Q>) <= exp(tau^2*||v||^2/(4*pi)).

Applying it termwise at v=(pi/tau^2)*v_k, with orthogonal directions,
proves

    E_e[p(e)^(-1/2)] <= E_e[S(e)]
       <= sum_k exp(-pi*||v_k||^2/(4*tau^2))
       = prod_i theta(2*tau/h_i) = J.                       (3)

Tonelli justifies the nonnegative sums. Rotated integer noise coordinates
are NOT assumed independent or continuous. This is the important distinction
from a Gaussian heuristic.

For any 0<delta,epsilon<1, Markov gives p(e)>=(delta/J)^2 except on noise
mass at most delta. Hence

    T_discrete=ceil((J/delta)^2*ln(1/epsilon))                 (4)

independent trials include the true lattice point, and thus true secret,
with probability at least 1-delta-epsilon. Add sampling implementation error.
The guarantee holds for every fixed secret and therefore any independent
secret prior. It is not a guarantee for every adversarial noise vector.

## 5. Sharper Coverage With Charged Classical Jitter

For continuous isotropic Gaussian noise of probability width tau, the
orthogonal t_i are independent continuous Gaussians of widths beta_i.
For one coordinate, define theta_beta(t)=sum_k exp(-pi*(k-t)^2/beta^2).
The inverse-square-root success moment equals

    I(beta)=(1/beta) integral_R
           sqrt(exp(-pi*t^2/beta^2)*theta_beta(t)) dt
      =(1/beta) integral_0^1 sqrt(theta_beta(t))
                                 *theta_(sqrt(2)*beta)(t) dt.

Cauchy--Schwarz and Gaussian convolution yield

    integral_0^1 theta_beta(t) dt=beta,
    integral_0^1 theta_(sqrt(2)*beta)(t)^2 dt=beta*theta(2*beta),
    I(beta)<=sqrt(theta(2*beta)).

Thus the continuous-noise counterpart of (3) is sqrt(J), and the list size

    T_jitter=ceil(J*delta^(-2)*ln(1/epsilon))                  (5)

has coverage at least 1-delta-epsilon in that model.

This continuous calculation is NOT a silent substitution for discrete noise.
Add independent U_i uniform in [-1/2,1/2] to each integer measurement y_i
before running the decoder, retaining the ORIGINAL y for likelihood scoring.
Then (e+U)/Q is close to the continuous noise just used. In unscaled units,
let f(t)=r_e^(-1)*exp(-pi*t^2/r_e^2), and let a(t)=f(k) on the unit cell
centered at k. Since integral |f'|=2/r_e,

    ||a-f||_1 <= (1/2)*integral |f'| = 1/r_e.

Normalizing a changes its L1 norm by at most the same amount. Thus

    TV(integer Gaussian + uniform jitter, continuous Gaussian)
        <= min(1,1/r_e),
    joint noise TV <= min(1,D/r_e)=min(1,2*D*s_G/Q).          (6)

The step-density normalization is theta(r_e)/r_e, not one by assumption.
The coverage guarantee from (5) consequently loses at most (6). In the
native growing-modulus regime this is negligible; in a small reference it
can be vacuous and MUST be reported that way.

### Finite Precision Is An Output-Kernel Obligation

Finite-bit jitter and continuous jitter have TV distance one as measures;
do NOT claim that their raw distributions are TV-close. Couple them so their
values differ by at most 2^(-b), and bound the CHANGE IN THE DECODER'S OUTPUT
distribution instead.

For unscaled integer observations with that jitter resolution, the target
perturbation for the unscaled dual basis C is at most sqrt(D)*2^(-b)/Q.
If using Q*C and target y+U instead, scale both the target and Gram--Schmidt
lengths consistently; do not charge or omit the factor Q twice.

For a one-dimensional Gaussian restricted to a fixed integer range [-Z,Z],
differentiating its normalized probabilities gives a TV Lipschitz bound
2*pi*Z/beta^2 in the center. For identical later coefficients, perturbing a
target by norm eta changes the next center by at most eta/h_i. A sequential
coupling bounds per-trial output TV by

    eta * sum_i 2*pi*Z_i/(beta_i^2*h_i),                      (7)

plus charged coordinate-tail errors. Multiply by T for the list. Fixed global
coefficient ranges can be bounded by recursively bounding the truncated
centers; their LOGARITHMS, along with rational Gram--Schmidt bit lengths,
are polynomial in the basis/input bit lengths and tail-precision parameters.
Choosing b to make (7) sufficiently small therefore needs polynomially many
bits in the polynomial-profile regime, even if the Lipschitz constant itself
is large. Use certified one-dimensional Gaussian sampling and arithmetic;
do not enumerate these potentially large ranges. This is an implementation
contract, not an executed arbitrary-precision compiler.

## 6. Selection And The Quantum Resource Comparison

Under the ideal noise, score each listed secret using its MARGINAL likelihood

    L_y(x)=prod_j sum_(k in Z)
              exp(-pi*(y_j-f_j*x+k*Q)^2/r_e^2).

Normalization factors common to x cancel. This is not nearest-lift distance:
all aliases contribute. A known efficiently evaluable prior can be included
for MAP selection; otherwise use uniform-prior ML. These are one-dimensional
Gaussian sums, not a Q-sized candidate enumeration in the actual algorithm.

If the true secret is listed and global full-space ML selects it, list-ML
selects it too, using consistent tie handling. Thus

    success(list-ML) >= success(full-ML) - coverage_error.     (8)

This does not assert that the list contains the full-space ML winner on
every input. A list can contain the truth while insufficient information
still makes ML choose incorrectly. Add the true Fourier-noise correction,
source/periodization errors, jitter error and numerical errors separately.

SOURCE-SPECIFIC FOLLOW-UP: section 7 of
`research/STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md` supplies an efficient
residual verifier when the original separated classical instance (A,b) and
a valid error bound are retained. In THAT model, verify every list candidate;
truth coverage suffices and marginal-likelihood ranking is unnecessary.
The source's unheralded clean-batch weight and preparation errors remain
charged. This is not a free verifier for standalone EDCP, and external
classical side information must not be smuggled into the information model.

For finite-precision likelihood comparison, one conservative average-risk
certificate is to evaluate each joint score pi(x)*P(y|x) with additive error
at most eta/(2*Q^D). With fixed tie handling, the excess Bayes risk contributed
by score approximation is at most eta after summing over all Q^D possible y.
This requires O(D*log Q+log(1/eta)) precision bits in addition to evaluating
the Gaussian sums and any prior; it does not require enumerating all y.

Poisson summation relates the two profiles exactly:

    J=H*(theta(s_G)/s_G)^D=H*theta(1/s_G)^D.

If s_G^2>=ln(4D)/pi, the last factor is at most exp(1). Thus polynomial H
implies polynomial J. The exact-discrete list bound is polynomial in H even
without jitter. With the jitter and numerical charges satisfied, (5) is
O(H*delta^(-2)*log(1/epsilon)), compared with the quantum universal-envelope
amplification scale sqrt(H). Basis finding is charged to BOTH alternatives.

This is a scoped computational comparison after quantum readout. It does
not rule out other coherent proposals, a stronger measurement at fixed
sample count, a non-Gaussian source, or a quantum algorithm for finding the
basis itself. At small fixed s_G the ambient theta factor may grow
exponentially; do not drop that factor or invoke this corollary there.

## 7. Adding Information Without Rebuilding The Basis

Suppose K describes an existing label batch. For a new block with multiplier
a, form a D-by-d matrix V supported in the old FIRST coefficient block with
that block equal to -T_a. The augmented basis is

    K_new = [ K  V ],
            [ 0  I ].

It has determinant Q and zero augmented Phi on every column, so is the whole
new kernel. Its old Gram--Schmidt vectors are unchanged and its d new ones
are coordinate unit vectors. Consequently

    H_new=H,         J_new=J*theta(1/s_G)^d.                  (9)

No new lattice reduction is required. In a growing-width regime, a polynomial
number of appended blocks changes J by at most a negligible factor. Provided
the REAL source can supply fresh independent labels and states, the sufficient
local-readout information bounds in the earlier note can therefore be used
without an exponential increase in this decoder profile. This is not a claim
that the initial good basis exists or can be found efficiently.

## 8. Bounded Checks And Falsifiers

These are mathematical references, not production tests or scaling evidence.

Twelve native one-block kernel cases used q in {3,5}, d=2, s_G in {1,2,4},
with native K and K*[[1,0],[3,1]]. Over 132,396 integer-noise points they
checked the exact correct-path probability (2), p^(-1/2)<=S, E S<=J, the
Markov bad-noise mass, and integrated list-miss probabilities for (4).
Integer noise was truncated at ceil(8*r_e); its Gaussian tail was retained
as a separate error, not promoted into an exact full-distribution computation.
For delta=0.1, epsilon=0.01, sufficient list lengths ranged from 486 to
311,663. These large lengths were integrated analytically as (1-p)^T,
not executed as repeated trials. Integrated miss probabilities lay between
2.01e-5 and 4.04e-4, within the conservative 0.11 bound.

Seven one-dimensional quadratures tested I(beta)<=sqrt(theta(2*beta)) at
beta=0.05,0.1,0.2,0.5,1,2,10. At beta=0.5, I=1.0396657350 versus bound
1.0423218367; at beta=2, I=1.99999999999 versus bound 2. These are numeric
controls of the analytic identity, not exact equality or novelty evidence.

Six step-density quadratures checked the jitter TV bound at r_e=0.6,1,2,5,
10,50. TV values included 0.1202836916 at r_e=2, 0.0249671196 at r_e=10,
and 0.0049997382 at r_e=50, below 1/r_e. Small-width bounds were correctly
vacuous. Eight exact augmentation checks used q in {5,7}, d in {2,4},
native/reduced bases and two appended labels; determinant, full-kernel and
unchanged-old/unit-new Gram--Schmidt identities all passed.

An actual bounded randomized-list reference used q=17,d=2,Q=290,s_G=2.5,
labels [1,127], with 64 or 256 draws on eight independent instances each.
Truth was listed in 5/8 and 8/8; ML selected truth in 3/8 and 4/8, exactly
matching full-space ML's correct counts. The distinction is intentional:
list coverage did NOT falsely report all secrets decoded.

A separate matched-prefix control used the SAME eight secrets and initial
noise/jitter, appending labels 77 and 208 while retaining the original basis:

| blocks L | draws per list | truth listed | list-ML correct | full-ML correct |
|---|---|---|---|---|
| 2 | 256 | 8/8 | 5/8 | 5/8 |
| 3 | 256 | 8/8 | 7/8 | 7/8 |
| 4 | 256 | 8/8 | 8/8 | 8/8 |

These small samples are NOT a success-probability estimate or an asymptotic
advantage. Full-space enumeration was used only as the Q=290 reference.
Every sampled lattice point satisfied the public modular code constraint.
All randomized references used NumPy seed 20260925. Their floating-point
Gaussian-coordinate samplers used radius ceil(8*max(1,beta_i)) about the
center, and the input integer noise radius was ceil(8*r_e). A production
implementation must certify conditional tails and arithmetic, not inherit
these numerical references as a proof of its output law.

## 9. Red Team And Implementation Handoff

The result would fail if one silently assumed independent rotated integer
noise, dropped the ambient theta factor, confused list inclusion with exact
recovery, optimized a basis using hidden noise, or treated finite-bit jitter
as TV-close to continuous jitter. Each is excluded explicitly above.

Remaining escapes worth research are a source-dependent coherent proposal
not governed by H, a useful non-Gaussian measurement, and a new efficient
basis-construction method. A few poor basis directions by themselves are
no longer evidence of a superpolynomial quantum decoder advantage.

Gemini: create `theorems/structured_edcp_profile_list_decoder.py`, sharing
kernel and exact reversed-dual validation with the preceding checker. Add
profile/coverage certificates, a charged randomized-coordinate sampler,
optional finite-bit jitter with output-kernel error accounting, deduplicated
lists, marginal Gaussian likelihood selection, and augmentation (9).
Keep `truth_in_list`, `selected_secret_correct`, `full_ML_reference_correct`,
and certified versus observed error separate. The actual algorithm must not
know e or x, enumerate Q candidates, receive CVP access, or use dense tables
outside capped references. Basis cost, noise-law correction, precision and
source coverage remain explicit. Do not globally label EDCP dequantized.

Main-model next target: the remaining-block conditional proposal or a
source-specific basis construction. This list decoder is the stronger
classical competitor those proposals must now survive.
