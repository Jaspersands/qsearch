# Structured EDCP: Global Shear Decoder And Its Integer Aliases

Date: 2026-09-27. LOCAL DERIVATION / REVIEW PENDING.

## 1. Decision

A natural global arithmetic attempt is to concentrate the phase into one
coefficient block, Fourier-measure the other blocks, and use their outcomes
to correct the remaining Gaussian before reading it out. The concentration
is efficient and exact. It does not solve the decoder:

1. With classically chosen linear phase corrections and final Fourier readout,
   its ENTIRE output distribution is classical local Fourier readout followed
   by arithmetic. This includes adaptive nonlinear classical correction rules.
2. The continuous-Gaussian interpretation exposes an unknown integer alias,
   not an available matrix-inversion solution. Completing the square leaves
   an explicit lattice theta sum. Dropping it is not an approximation justified
   by the source's large coefficient width alone.
3. A genuinely coherent, nonlinear alias operation remains open. The results
   below are not a lower bound on arbitrary joint measurements or all uses of
   this shear as an intermediate circuit.

This tests a concrete global constructor for the three-block regime from
`STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md`; it is not a new generic no-go
principle, an efficient decoder or a claimed novel Fourier identity.

FOLLOW-UP: `STRUCTURED_EDCP_MODULE_GLUING_AUDIT.md` audits the alternative
of solving orthogonal rank-one ideals. It identifies their missing integral
index and bounds the fidelity of constructors discarding the associated
cosets. Neither field orthogonalization nor ideal PIP removes that work.

## 2. Exact Arithmetic Concentration

Work first at scalar rank one with a UNIT first label. Normalize it to one
and absorb that multiplication into the secret. Charge this event separately:
full binary rank is not the same promise at composite Q. Write D=d*L,
k=(L-1)*d, and let T_a be integer negacyclic multiplication by an explicitly
chosen coefficient lift of a. It satisfies E(T_a c)=a*E(c) mod Q.

Set

    T=[T_(a_2) ... T_(a_L)],
    U=[ I_d  T ],
      [  0  I_k],
    (x,z)=U*(c_1,c_rest).

U and its inverse are integer unimodular matrices. Modular versions are
invertible over Z_Q for ANY modulus, without dividing by det(T). On finite
coefficient registers Z_Q^D this is an efficient permutation, and

    sum_l a_l*E(c_l) = E(x) mod Q.                           (1)

Hence the hidden phase is confined to x. No sample has been discarded, but
the amplitude is now correlated between x and z. On unwrapped integer
registers its Gaussian part is

    exp(-pi*(||x-T*z||^2+||z||^2)/sigma^2).                  (2)

Finite periodic registers, infinite integer registers and continuous variables
are DISTINCT models. Equation (1) is exact on finite registers. Equation (2)
is exact for the infinite integer Gaussian under the integer shear; transferring
between them requires the actual wrap/tail budget, not a declaration that q
or sigma is large.

## 3. Exact Classical Simulation Of The Measured-Shear Family

Use the QFT convention

    F psi(p)=Q^(-D/2)*sum_c psi(c)*exp(-2*pi*i*p dot c/Q).

For ANY input state, not only a Gaussian, the permutation U obeys

    F(U psi)(y)=(F psi)(U^T*y).

Consequently, if p=(p_1,p_rest) is its original joint Fourier outcome, the
sheared joint Fourier outcome has exactly the law

    y_x=p_1,
    theta=p_rest-T^T*p_1 mod Q.                             (3)

Now consider the actual adaptive protocol:

- Apply U; Fourier-measure only z and retain its outcome theta.
- Compute any classically available g(theta) in Z_Q^d, possibly nonlinear
  or randomized, with its computation cost included.
- Apply exp(-2*pi*i*g(theta) dot x/Q) on the remaining block.
- Fourier-measure x, then perform arbitrary classical postprocessing.

Its FULL joint output law is precisely sampled by

    sample the original Fourier outcome p;
    compute theta=p_rest-T^T*p_1 mod Q;
    return (p_1-g(theta) mod Q, theta).                      (4)

Proof: measuring z in the Fourier basis commutes with subsequently measuring
x there. For fixed theta the linear phase just translates that Fourier
outcome. Equation (3) then proves the joint law, including every outcome's
Born weight. A classical nonlinear CHOICE of g does not make the applied
x-dependent phase nonlinear. Public independent random coins can be sampled
identically by both procedures.

Conditional invertible linear relabelings of x before its final QFT also
only change the classical inverse-transpose map. This does not include
arbitrary nonlinear permutations of x, arbitrary diagonal phases in x,
non-Fourier final measurements or coherent processing of unmeasured theta.
Real-valued affine corrections on a rotor require a separate discretization
ledger; (4) is stated exactly for the finite modular circuit.

Postselection based on returned classical data is also simulated with its
actual success probability. Conditional error bounds may amplify a small
sampler discrepancy. Do not compare only normalized successful branches.

For the retained classical source, the existing local-readout sampler supplies
the required p distribution within its complete error budget. Data processing
does not increase that discrepancy. For the NEW direct-phase construction,
the internally known tags t_l themselves specify the physical product-state
Fourier distributions; a matched classical implementation can use the same
fresh tags and labels. No secret, lift witness or general quantum simulator
is needed. Gaussian sampling/periodization precision must still be charged.

Thus an algorithm in this family does not establish a quantum separation on
the retained classical input. If g is obtained by an essential quantum
algorithm on the classical outcome theta, that separate algorithm is the
possible source of advantage; it has not been supplied by the shear.

## 4. What Completing The Square Actually Leaves

In the infinite integer model, Fourier-transform z to a torus outcome theta
in [-1/2,1/2)^k. Ignore only global normalization when defining

    A(x,theta)=sum_(z in Z^k)
       exp(-pi*(||x-T*z||^2+||z||^2)/sigma^2)
       *exp(2*pi*i*theta dot z).

This uses the positive-sign transform for the following identity; replace
theta by -theta to match section 3's convention. Put

    G=I_k+T^T*T, B=I_d+T*T^T, mu_x=G^(-1)*T^T*x.

Completing the square and applying Poisson summation gives EXACTLY

    A(x,theta)
      = exp(-pi*x^T*B^(-1)*x/sigma^2) * sigma^k/sqrt(det G)
        * sum_(m in Z^k)
          exp(-pi*sigma^2*(m-theta)^T*G^(-1)*(m-theta))
          * exp(2*pi*i*(theta-m) dot mu_x).                  (5)

The first factor looks like a greatly widened Gaussian in x. It is multiplied
by a coherent sum over integer aliases with x-dependent phases. Diagonalizing
G over the reals does not remove m or preserve the integer summation lattice.
A single alias would give a Gaussian with a correctable linear phase, but
finding, isolating or coherently managing such an alias is additional work.

The alias ellipsoid can be long in the row-space directions of T and very
thin in its null directions. Its volume alone is not a posterior decoder:
low expected occupancy can make the likely alias unique while leaving it
computationally difficult to identify. Conversely, dropping all aliases but
zero is not justified when a sample lies near a nonzero alias.

## 5. The Matched Classical Alias Problem

In the explicitly CHARGED continuous wrapped-Gaussian readout approximation,
let the independent original Fourier errors have covariance v*I_D, with

    v=1/(4*pi*sigma^2).

For the shear (3), let eta_1 be the first block's unwrapped error and

    Theta=eta_rest-T^T*eta_1,
    theta=Theta mod Z^k.

The ideal hidden phase cancels from theta. The unwrapped variable has
covariance v*G. Given a particular lift Theta=theta+m,

    E[eta_1 | Theta] = -T*G^(-1)*Theta,
    Cov(eta_1 | Theta) = v*B^(-1),                           (6)

since I-T*G^(-1)*T^T=B^(-1). Its conditional alias law is

    Pr[m | theta] proportional to
       exp(-(theta+m)^T*G^(-1)*(theta+m)/(2*v)).              (7)

Computing (6) is easy AFTER the integer alias is known. Inferring that alias
from theta is a closest-vector/posterior problem in the metric G^(-1), of
dimension k=(L-1)d. It is not ordinary least squares on the observed torus
coordinate. Quantum formula (5) is coherent; classical formula (7) is a
posterior mixture. They must not be silently identified as quantum states.

Equation (4) explains why classical alias estimation plus linear correction
and Fourier readout cannot by itself exploit the extra coherence. It does
not exclude a different subsequent measurement that acts on it.

The Gaussian surrogate is not exact physical Fourier noise at finite width.
Use `STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md` and its physical-noise
and precision ledger before using (6)-(7) as a bound on a real workflow.

## 6. A Quantitative Failure Of Fixed-Alias Guessing

Assume T has full row rank. Project Theta onto the d-dimensional row space
of T in R^k. Its covariance eigenvalues are v times those of B. If Theta
lies in any one fixed integer unit cube, its projection lies in a ball of
radius sqrt(k)/2. Bounding that Gaussian density by its maximum gives

    Pr[Theta in m+[-1/2,1/2]^k] <= min(1,C_box),
    C_box=(sigma*sqrt(pi*k/2))^d /
                  (Gamma(d/2+1)*sqrt(det B)).               (8)

For a FIXED set of J aliases, chosen independently of theta, the probability
is at most min(1,J*C_box). An adaptive alias decoder can evade this bound;
that is exactly why (8) is not a lower bound on all classical or quantum
decoders. Nor is a hidden classical alias an automatically measurable quantum
branch. The result concerns the classical surrogate and invalidates its
fixed-principal-branch shortcut, not arbitrary interference in (5).

The determinant is a public, computable quantity; no heuristic random-matrix
bound is needed to state (8). T=0 is the easy no-shear control and is outside
the full-row-rank derivation; no suppression is claimed there.

Three naturally sampled public-label references used the L=3 moment widths
from `STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md`. The first label is fixed to one
under the separately charged unit normalization; the other two are independent
uniform residues. Their centered coefficient lifts define T.

| d | log10 det(B) reference | log10 C_box reference |
|---:|---:|---:|
| 64 | 2835.04272219 | -840.88362510 |
| 256 | 15180.71108009 | -3940.80126351 |
| 1024 | 76113.14810394 | -18005.43133886 |

These determinant values used floating negacyclic FFT eigenvalues and are
NOT certified enclosures or natural-ensemble concentration results. The bound
formula itself is rigorous under its premises. They illustrate how severely
the principal-alias approximation can fail, not the performance of an actual
quantum decoder. There were no large statevector simulations at these d.

Reproduction: Python Random seed 20260927, dimensions in the displayed order,
two consecutive randrange(Q) labels per dimension. Take the centered residue,
extract balanced base-q digits by r=(value+(q-1)/2) mod q-(q-1)/2, then subtract
the final carry from coefficient zero. Exact evaluations were checked mod Q.
SHA256 of compact JSON encoding of the two lift arrays, by dimension:

    64:   b5ed3dd607ce4af35d6043f8669e4938130f653d72731600812a517f90660f7f
    256:  a74114fe87e52925abab35f8549ffe6d5a5971c61bf65a61c84cec8aa50db046
    1024: 59bc00a873e9cf12798d5474c98a3866ce781045cb0c7fa69fad843491de2bab

## 7. Independent Controls Actually Run

- Twenty-four complete complex-amplitude circuit comparisons used native
  (q,d,L)=(2,2,3),(3,2,2), two random label sets, widths 0.8,1.4 and secrets
  0,1,Q-1. The correction g depended NONLINEARLY on the measured theta.
  Direct partial QFT, conditional phase and final QFT agreed with (4), with
  maximum L1 discrepancy 6.62e-16. All U permutations and phase-concentration
  identities were checked with integers. Sixteen comparisons confirmed that
  theta's marginal was secret-independent in the ideal phase ensemble.
- Thirty exact rational matrix controls at (d,k)=(1,1),(1,2),(2,2),(2,4),
  (3,6),(4,8) verified det G=det B and the Schur-complement identity in (6).
- Thirty-six independent complex Poisson-sum comparisons used integer
  matrices [3], [2,3], [[1,2],[-2,1]], [1,-2,3], widths 0.8,2,5 and random
  integer x/torus theta. Primal and alias sums were truncated beyond eight
  Gaussian widths in the corresponding Euclidean bounds. Largest observed
  absolute discrepancy was 1.78e-15; these are finite numerical references.
- Fifteen scalar controls compared the exact Gaussian interval probability
  from erf with (8), including zero, small and large shears. All passed.
- Three public-matrix analytic references evaluated (8), as qualified above.

No production integration, full-suite run, candidate promotion or large
decoder experiment occurred. The recent external DCP erasure claim and its
GRZ refutation were rechecked against `DCP_LABEL_DIGEST_AUDIT.md`; the repo
already records that obstruction. It is not a fresh lead or evidence that
the present full-label problem is impossible.

## 8. Next Theory And Gemini Contract

Do not build a purported quantum decoder out of U, ordinary matrix inversion,
a classical alias guess and final Fourier measurements. That family has the
explicit matched simulation (4). It can still be a useful classical baseline.

The remaining high-upside target must specify an operation outside that
family: a coherent alias transformation, a nonlinear measurement on the
remaining block, or a quantum algorithm that genuinely solves the public
integer inference problem faster. It must preserve the naturally distributed
labels and charge preprocessing, precision, acceptance and source errors.
Assuming a closest-vector oracle, known short basis or theta-function oracle
does not implement that step.

Gemini should add this exact circuit-identity check and the classical alias
baseline to the direct-phase source workflow, after the upstream numerical
repair. Keep finite modular, integer-torus and continuous-Gaussian models
separate. Record g's actual computational access, all failures, and whether
the final measurement lies inside (4)'s scope. Use exact/sound log-determinant
enclosures for a certificate; the displayed FFT numbers are only references.
Retain adaptive-alias and non-Fourier measurements as open cases, not blanket
negative results. The next main-model pass must attack one of those cases.
