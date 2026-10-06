# Native Ring-LWE: Repeated Preparation Is Not Unlimited Ideal Access

Date: 2026-09-29. LOCAL DERIVATION / REVIEW PENDING.

This audits the source in `NATIVE_RLWE_PHASE_DECODER_TARGET.md`, not all
possible reductions or quantum decoders. No novelty, independently verified
theorem, or speedup is claimed. Production checks belong to Gemini.

## 1. Why This Matters

After local Fourier transform, the ideal native state has a real Gaussian
amplitude centered at C_a*s. This resembles quantum-amplitude LWE, so its
known algorithms must be checked before calling the decoder target new.

[Chen--Hu--Liu--Luo--Tu, Theorem 4 and Section 4](https://arxiv.org/html/2310.00644v2)
give a subexponential algorithm for known real amplitudes with subexponentially
many independent samples, and polynomial algorithms under complex-Gaussian
phase and modulus promises. Neither is an automatic solver here: rows within
C_a are dependent, original sample count is limited, and the native real
Gaussian does not have the promised error-centered quadratic phase.

A new proof could conceivably exploit those structures. It must not hide
sample creation, noise accumulation, or an unknown-center phase operation.
The elementary lower bound below strengthens the source's earlier sufficient
upper error budget: repeating one preparation superpolynomially many times
actually destroys closeness to the ideal source when q is polynomial and
sigma>=1, either with the original input retained OR with the hidden secret
preserved as an inaccessible mathematical reference. It is not merely an
inconclusive upper bound. Forgetting BOTH registers is a different comparison.

## 2. Exact Repeated-Copy Experiment

Keep the original classical record X, including a,b. One record satisfies
b=C_a*s+e mod q. For the scalar truncated coefficient law put

    mu(c)=exp(-2*pi*c^2/sigma^2)/Z_R, -R_c<=c<=R_c,
    Z_R=sum_(c=-R_c)^(R_c) exp(-2*pi*c^2/sigma^2),
    1<=R_c<q/2, sigma>=1.

Let |Psi_b> be the actual d-coordinate phase state, and |Psi_z> its ideal
counterpart with z=C_a*s. Conditional on X, actual L-copy output is PURE:
|Psi_b>^(tensor L). The ideal cq output mixes |Psi_z>^(tensor L) over the
conditional hidden-secret law given X. Both outputs retain the SAME X.

Test the quantum output with the projector onto |Psi_b>^(tensor L), chosen
using X. This is a valid measurement witness for trace distance, whether or
not a particular implementation compiles it efficiently. Actual acceptance
is one; ideal acceptance, averaged over the original instance, is exactly

    F_L=E_e |phi_mu(e/q)|^(2*L),
    phi_mu(e/q)=prod_i sum_c mu(c)*exp(2*pi*i*e_i*c/q).

Consequently

    D(rho_actual,cq,rho_ideal,cq)>=1-F_L.                     (1)

The expectation uses the actual marginal of e. It does not assume the
secret is known, that posterior errors are independent, or that the ideal
conditional output is pure. Additional classical records can remain in X.

### A Hidden-Secret Reference Survives Discarding b

Alternatively, retain a classical reference register S recording the TRUE
secret, inaccessible to the decoder, and discard b if desired. Conditional
on S=s and a, the ideal output is pure |Psi_(C_a*s)>^(tensor L); the actual
output mixes |Psi_(C_a*s+e)>^(tensor L) over the conditional noise law.
The reference-controlled projector onto the IDEAL state has acceptance one
on the ideal experiment and average acceptance F_L on the actual experiment.
Thus (1) also holds for the joint (S,a,quantum-output) states without b.

This does NOT give the solver the secret. It is a mathematical reference
needed to transfer a secret-RECOVERY success probability. For a common
decoder, trace distance of the secret-referenced experiments bounds the
difference of Pr[decoder output=S]. Comparing only state marginals after
forgetting S does not establish that recovery guarantee.

## 3. A Polynomial Gap For Every Nonzero Error

For a nonzero scalar residue k, expand the squared characteristic function:

    1-|sum_c mu(c)*exp(2*pi*i*k*c/q)|^2
      =sum_(c,c') mu(c)*mu(c')
                    *[1-cos(2*pi*k*(c-c')/q)]
      >=4*mu(0)*mu(1)*sin(pi/q)^2 = eta.                    (2)

Only the ordered pairs (0,1),(1,0) were retained; every discarded term is
nonnegative. Thus if e is nonzero in Z_q^d, at least one coordinate gives
|phi_mu(e/q)|^2<=1-eta, while all other coordinate factors are at most one.
With p0=Pr[e=0 mod q], equations (1)-(2) imply

    F_L <=p0+(1-p0)*exp(-eta*L),
    D(rho_actual,cq,rho_ideal,cq)
        >=(1-p0)*(1-exp(-eta*L)).                            (3)

This is exact for the finite coefficient reference, before implementation
errors. There is no Gaussian Fourier approximation or uncharged tail.

For a fully elementary bound, Z_R<=min(q,1+sigma/sqrt(2)),
mu(0)*mu(1)=exp(-2*pi/sigma^2)/Z_R^2, and sin(pi/q)>=2/q. Hence

    eta >=16*exp(-2*pi) /
                  [q^2*min(q,1+sigma/sqrt(2))^2]
         >=16*exp(-2*pi)/q^4.                               (4)

The last bound is weak numerically but uniform in sigma>=1 and the allowed
cutoff. If q is polynomial in d, it is inverse polynomial. For a requested
joint trace-distance budget epsilon<1-p0, a NECESSARY condition is

    L <= -log(1-epsilon/(1-p0))/eta.                         (5)

Use the actual eta for finite comparisons. A useful necessary bound is not
a sufficient accuracy certificate; use the source upper bound as well.

For spherical integer noise of probability width rho,

    p0=[Theta(rho/q)/Theta(rho)]^d,
    Theta(t)=sum_(j in Z) exp(-pi*j^2/t^2).

For q much larger than rho>1, this is approximately rho^(-d). A certified
upper bound replaces the numerator by
1+2*exp(-pi*q^2/rho^2)/(1-exp(-3*pi*q^2/rho^2)) and the denominator by rho.
Do not use this iid formula for the correlated elliptical lane. Equation (3)
still holds there with its actual p0, including any hidden-shape mixture.

## 4. Scope, Counterexamples And What Remains Open

**Keep either the input record or the hidden-secret reference.** With uniform
scalar secret, a=1 and independent error, both phase ensembles are identical
after BOTH b and S are discarded: averaging either secret or noisy secret
gives the same state, also for repeated copies. Yet retaining either b or S
gives positive distance. Equation (3) is NOT a lower bound on the fully
averaged quantum marginal. The hidden-secret version above remains applicable
to a recovery-transfer claim when the actual decoder ignores b. Forgetting
the reference does not make that claim valid.

**Closeness failure is not algorithm failure.** A decoder could work on the
actual noisy states without a close ideal-source replacement. It would need
its own success proof. This audit blocks one black-box transfer argument,
not every use of many states generated from known classical data.

**Repeated labels are not independent labels.** Even before the quantum
distance issue, reusing a fixed input does not supply the independent sample
model of the published sieve. Random small combinations of original samples
would require their own native-ring label-distribution and joint error proof.

**Subunit widths are not covered by (4).** Equation (2) remains valid but
mu(1) can become extremely small. A proposal which shrinks sigma with L must
charge that altered amplitude distribution and the probability/cost of
extracting useful phase states. The theorem does not rule out every such
tradeoff or every adaptive source construction.

**Periodized and implemented states need explicit transfer.** The result
above is for matching finite, truncated actual and ideal states. To compare
against the periodized ideal target subtract its joint shape error from
the lower bound, and subtract any actual/ideal implementation errors once.
Do not interchange a many-copy marginal guarantee with a joint guarantee.

**A public chirp is not an error-centered chirp.** Multiplication by
exp(-pi*i*y^2/t) on a register centered at z differs from the desired
exp(-pi*i*(y-z)^2/t) by a z-dependent linear phase and a global phase.
The missing operation is not known merely because b=z+e is known.
Preparing a chirped state around b changes the center error sensitivity;
the real-Gaussian source bound cannot be reused unchanged. The existing
DIRECT_PHASE_SOURCE and NONLINEAR_CHIRP_AUDIT notes contain explicit controls.

## 5. Checks And Integration Contract

Checks actually run:

- 3,136 nonzero-error/repetition controls over q=3,5,7,11,17,31,
  sigma=1,1.7,3,7, several legal cutoffs and L=1,3,19,100. Checked (2),
  the elementary eta bound, and the repeated-copy exponential bound.
- 24 full cq density comparisons, q=3,5,7, sigma=1,1.8, L=1,2, with both
  uniform and Gaussian secret priors. The retained-b distance respected
  (1) and (3); maximum acceptance-identity error was 1.12e-15.
- In the uniform-prior controls, discarding b reduced distance to at most
  1.12e-16 when S was ALSO absent, while the retained-b distance was positive.
- 24 further secret-referenced density comparisons after b was discarded
  verified (1). Maximum acceptance-identity error was 1.34e-15; fully averaged
  uniform-prior marginals had distance at most 7.00e-17. These are mandatory
  scope regressions, not optional illustrations.

These scalar controls test a coordinate identity, not a toy-oracle research
direction. No full suite, live registry runs, production wiring or commits.

Gemini: distinguish original samples, copies per original sample, selector-
derived samples, and ideal independent samples in every record. Implement
both the source upper ledger and this repeated-copy lower witness, with
explicit retained-side-information and width/cutoff tags. If the lower
witness exceeds the requested source budget, record a falsified JOINT SOURCE
CLAIM, not a universal negative result for quantum decoding. Distinguish
retained-b and hidden-secret-reference witnesses. Never give S to the decoder
or apply the lower bound to a marginal that retains neither b nor S.

Main-model work remains an explicit decoder under the access actually
supplied, or a proved alternative source conversion. Calling a published
ideal-amplitude solver without matching sample and phase promises is not
that work.
