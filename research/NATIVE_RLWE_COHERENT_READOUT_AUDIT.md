# Native Gaussian Readout: Teleportation Comparator And Wigner Limits

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to NATIVE_RLWE_COVARIANT_DECODER_TARGET and
NATIVE_RLWE_GAUSSIAN_SAMPLER_AUDIT. This tests a coherent readout proposal
and an attempted broader dequantization argument. Routine integration and
large experiments are assigned to Gemini. No novelty, independently checked
theorem, efficient general Gaussian decoder or quantum speedup is claimed.

## 1. Research Decision

The entangled-resource/Bell/final-QFT protocol below has an EXACT classical
sampler for its ENTIRE measured transcript on ACTUAL observed tags. Any
subsequent classical decoder or acceptance rule has the same success and
rejection distribution. Its scalar-table cost is O(n*q*log q), polynomial
in the audited regime q=poly(d), n=O(d). Entanglement and a Choi-state
description alone therefore do not implement the missing native inverse.

There is also a scope correction: periodized finite Gaussians retain
substantial discrete Wigner negativity. A positive-Wigner argument cannot
dismiss arbitrary Clifford circuits on these inputs. Section 4 gives a
four-lobe representation and a signed estimator with an exponential
sufficient cost. That larger class remains outside a polynomial simulation
claim. Both the prior-aware L1 and coherent L2 research targets remain open.

## 2. An Explicit Teleportation-Style Decoder

Let q be an odd prime, n the coefficient-register count, k the encoded
output dimension, D=q^n and N=q^k. For native L2 use n=2*d, k=d and the
PUBLIC linear map F=[C_(a_1)^T C_(a_2)^T]. Let

    G(x)=prod_j g_j(x_j), H(y)=prod_j r_j(y_j),
    sum_t |g_j(t)|^2=sum_t |r_j(t)|^2=1.

These known envelopes may be complex and different. Finite-cutoff Gaussians
are included, with their signed coefficients embedded in Z_q. Prepare

    |Psi_b>=sum_x G(x)*omega^(b dot x)|x>, omega=exp(2*pi*i/q),
    |Omega_F>=sum_y H(y)|F*y>_U|y>_C.                       (1)

Here b is the OBSERVED native tag vector, including actual errors. The
resource uses independent H coefficients and reversible public arithmetic.
No unknown ideal phase, secret or hidden error shape is supplied.

Bell-measure data X and resource C using

    <B_(h,l)|=D^(-1/2)*sum_x omega^(-l dot x)
                              <x|_X <x+h|_C.

Retain BOTH h,l, then Fourier-measure U with kernel
N^(-1/2)*omega^(-z dot u). Define

    f_h(x)=G(x)*H(x+h),
    f_hat_h(v)=D^(-1/2)*sum_x f_h(x)*omega^(-v dot x).

Direct contraction gives the complete transcript law

    A_b(h,l,z)=N^(-1/2)*omega^(-z dot F*h)
                              *f_hat_h(l+F^T*z-b),
    Pr_b[h,l,z]=(1/N)*|f_hat_h(l+F^T*z-b)|^2.              (2)

This holds pointwise for every b and F, including deficient rank. No
ideal-source comparison or averaging away a secret reference is involved.

### Exact Classical Sampler

1. Draw z uniformly from Z_q^k.
2. Independently for each j draw x_j from |g_j|^2 and y_j from |r_j|^2;
   set h_j=y_j-x_j mod q. Keep these assignments PRIVATE.
3. Form f_(j,h_j)(t)=g_j(t)*r_j(t+h_j). Its squared norm is
   p_j(h_j)=sum_t |g_j(t)|^2*|r_j(t+h_j)|^2, exactly the difference law
   in step 2. Sample v_j from |F_q f_(j,h_j)(v_j)|^2/p_j(h_j).
4. Return h,l=b-F^T*z+v,z, discarding the private assignments.

The sampled p_j is nonzero almost surely. Multiplying the probabilities
cancels every p_j and yields (2). Scalar FFTs/categorical draws require
O(n*q*log q) arithmetic operations and O(n*q) table storage, or O(q)
working space with sequential rows. There is no q^n or q^k enumeration.
The table argument is polynomial for the project's q-near-d^4 and d^12
families; it does not give polynomial dependence on log q when q may be
exponential in rank. Precision costs must be included.

A measurement-order proof explains the factorization. The resource's
reduced U state is diagonal in u, so its Fourier outcome z is EXACTLY
uniform. Measuring it first collapses C to

    sum_y H(y)*omega^(-z dot F*y)|y>,

a known product state because F is linear. That measurement commutes
with the Bell measurements on the other registers. Each remaining Bell
pair is independent. Near-flat fibers and maximal entanglement are
unnecessary for this comparator.

### Decisions, Corrections, Retries And Precision

Arbitrary polynomial classical decisions from h,l,z,b,F preserve the
comparator, including nonlinear decoding, likelihoods, residual verification
and measured postselection. Matching the full JOINT law is necessary:
z alone is uniform, while its correlations with l can carry information.
Returning independent uniforms would be wrong.

Outcome-dependent Pauli corrections on U only relabel its Fourier output
or add an unobserved phase. Invertible linear coordinate maps also give
computable output relabelings. Fresh measured trials, with settings chosen
from earlier CLASSICAL transcripts, are covered inductively. Charge
acceptance/retry costs in both algorithms. Coherent amplification across
unmeasured outcomes changes the circuit and needs separate analysis.

For a numerical sampler, absolute amplitude accuracy does not imply
harmless normalized error on rare h_j. One bounded-error implementation
declares failure if p_j(h_j)<tau. Its lost mass is at most n*q*tau.
Choose tau from the transcript error budget; on retained branches the
normalizer is bounded below, so absolute table/FFT precision can certify
the scalar laws. Gaussian source and circuit errors remain separate.

Constant-size entangled blocks are also eligible if input and resource
share an explicit block factorization: replace scalar FFTs by q^w tables
for largest block size w. Fixed w and polynomial q still give polynomial
cost. Growing blocks require a different analysis.

## 3. What This Does And Does Not Falsify

The measured protocol (1)-(2), including its classical decoder and ordinary
postselection, cannot establish a superpolynomial quantum advantage in
the audited modulus regime. The simulator consumes b legitimately because
this source is prepared from those original classical records. It matches
success under any secret/noise law consistent with that preparation.

A nonlinear F gives a coupled phase after the early Fourier measurement;
an arbitrary entangled envelope also removes the product argument. Neither
modification automatically solves native decoding. Their preparation costs,
operations and benefit must be proved. A retained quantum output,
outcome-dependent change of measurement basis, or other operation preventing
measurement commutation is also outside this comparator. There is no claim
covering all teleportation, all Clifford circuits or unknown HSP inputs.

## 4. A Positive-Wigner Shortcut Fails

Use the scalar PERIODIZED-AMPLITUDE reference

    t_sigma(x)=sum_j exp(-pi*(x+q*j)^2/sigma^2),
    Z=sum_(x mod q) t_sigma(x)^2, g(x)=t_sigma(x)/sqrt(Z).

For the odd-q convention

    W_g(x,p)=(1/q)*sum_(a mod q)
                  g(x+a)*g(x-a)*omega^(-2*p*a),

set s=sigma/sqrt(2), t=q/(2*s), and positive functions

    X_epsilon(x)=sum_j exp(-pi*(x+q*j+epsilon*q/2)^2/s^2),
    Y_eta(p)=sum_j exp(-pi*(p+q*j+eta*q/2)^2/t^2).

The exact normalized four-lobe expression is

    W_g=s/(q*Z)*[X_0*Y_0+X_0*Y_1+X_1*Y_0-X_1*Y_1].       (3)

This reparameterizes [Cotfas--Dragoman, Theorem 4](https://arxiv.org/pdf/1205.6302)
for our widths and normalization. No novelty is claimed. Expanding the
periodized amplitudes separates lift parities; Poisson summation of the
relative coordinate gives sign (-1)^(epsilon*eta).

For the known tag b, W_(g*omega^(b*x))(x,p)=W_g(x,p-b). The original
noise does not change this conditional-on-input resource quantity.
Discarding and averaging the tag changes the state and does not justify
a comparator for a solver retaining that tag.

Let A_epsilon=sum_x X_epsilon(x), B_eta=sum_p Y_eta(p). For odd q these
are ordinary/half-shifted integer theta masses, so shifted-Gaussian
maximality gives A_1<=A_0 and B_1<=B_0. Normalization yields

    Z=(s/q)*[A_0*(B_0+B_1)+A_1*(B_0-B_1)],
    T=[(A_0+A_1)*(B_0+B_1)]
          /[A_0*(B_0+B_1)+A_1*(B_0-B_1)]<=2,
    ||W_g||_1<=T.                                         (4)

When both sigma and q/sigma grow, the four lobes separate. Their component
masses approach 1/2 each, with the last negative; Gaussian tail bounds
on disjoint neighborhoods give

    ||W_g||_1 ->2, sum_(W<0) |W| ->1/2.                    (5)

The boundary-by-boundary quarter of modular phase space has mass approaching
-1/2, which also gives ||W||_1>=1-2*W(quarter). Pointwise small lobes still
retain their integrated weights and cannot be discarded.

| q | sigma | Numerical ||W_g||_1 | Negative-quarter mass |
| --- | --- | ---: | ---: |
| 31 | 2*sqrt(q) | 1.9729390182 | -0.4864695091 |
| 61 | 2*sqrt(q) | 1.9989303642 | -0.4994651821 |
| 127 | 2*sqrt(q) | 1.9999988228 | -0.4999994114 |
| 251 | 2*sqrt(q) | 1.999999999996 | -0.499999999998 |

For n independent coefficient registers the l1 norm is the PRODUCT of
scalar norms, approaching 2^n; mana is approximately n*log(2). These
scalar calculations are identity controls, not algorithm discoveries.

This agrees with [Gross, discrete Hudson theorem](https://arxiv.org/pdf/quant-ph/0602001):
pure nonnegative Wigner states are stabilizer states. Nonconstant Gaussian
amplitudes do not meet that premise. The positive-input simulation of
[Veitch--Ferrie--Gross--Emerson](https://arxiv.org/pdf/1201.1256) does not
replace (3) by an ordinary probability distribution.

For a finite-cutoff scalar state at trace distance Delta from this reference,
Wigner-frame orthogonality and Cauchy--Schwarz give

    ||W_finite-W_reference||_1<=sqrt(2*q)*Delta.             (6)

The native exponentially accurate cutoffs at polynomial q preserve the
scalar negativity conclusion. Use the actual shape ledger; this initial
product-source statement does not transfer unchecked through postselection.

## 5. A Signed Estimator And Its Cost

Equation (3) supplies a quasiprobability baseline. Choose epsilon with
weight A_epsilon/(A_0+A_1), eta with B_eta/(B_0+B_1), then sample x from
X_epsilon/A_epsilon and p from Y_eta/B_eta. Assign sign (-1)^(epsilon*eta)
and weight T; shift p by the known tag. Product inputs give signed samples
of weight T_total=prod_j T_j<=2^n.

Clifford gates propagate these phase points by public affine symplectic
maps. Computational measurements return position and uniformly randomize
conjugate momentum; other Pauli measurements can be conjugated to that
case. Adaptive classical choices act on the sampled transcript. Linearity
preserves signed expectations.

For a bounded transcript statistic H, averaging T_total*sign*H is unbiased
in exact arithmetic. Hoeffding gives sufficient sample count

    O(T_total^2*epsilon^(-2)*log(1/delta))
       <=O(4^n*epsilon^(-2)*log(1/delta)).                  (7)

These signed paths are not physical output samples. Conditional statistics
also pay for the acceptance denominator. Series/sampling/arithmetic errors
are amplified by T_total and require a budget. Further Gaussian resources
add their own factors; positive stabilizer ancillas do not.

An exponential sufficient estimate is not a lower bound for classical
algorithms. Exponential mana is also not evidence of useful computation:
the identity circuit has it already and its position law is easy to sample.
For Section 2's protocol the measurement-order sampler is stronger.

## 6. Checks Actually Run

Targeted derivation controls, without routine wiring, a full suite or commit:

- 64 scalar four-lobe controls at q=3,5,7,11,17,31,61,127 and eight widths,
  including narrow/wide stabilizer limits. Direct Wigner sums agreed with
  (3), maximum discrepancy 1.39e-16. Checked normalization, reality,
  total weight and the negative-quarter bound.
- Six growing scalar references through q=509 checked (5).
- Seed 290938: 432 two-register Clifford gates at q=3,5,7: Fourier,
  quadratic phase, controlled phase, SUM and shifts. Thirty-six destructive-
  measurement/adaptive-Clifford protocols matched direct state calculations;
  maximum probability discrepancy 1.23e-15.
- Replacing W by normalized |W| gave position TV errors approximately
  .48747,.49952,.49999946,.499999999998 at q=31,61,127,251 for an
  IDENTITY circuit. This falsifies the positive-Wigner shortcut.
- Seed 290939: 40 complete complex-envelope teleportation circuits at
  (q,n,k)=(3,2,1),(5,2,1),(3,3,1),(3,2,2),(7,2,1). Compared 184,728
  joint entries to (2) and the comparator, including classical decisions.
  Maximum error 2.09e-17; final-z uniformity error 5.28e-16.
- Seed 290940: six native negacyclic L2 Gaussian cases, d=2,q=3,
  actual tags without substitution of a hidden ideal secret. All 354,294
  joint entries matched, maximum error 2.82e-18.
- A nonlinear-syndrome scope control gave a conditional Fourier law at
  TV .01164945 from the product of its own marginals. The product proof
  cannot be applied to arbitrary nonlinear maps. This is a scope control,
  not a toy-oracle research proposal.

These can expose algebra or implementation errors; independent review of
the application and complexity statements remains required.

## 7. Gemini Contract And Next Theory Target

Implement the comparator as a separate ACTUAL-input baseline. Inputs:
q,F,b, product/bounded-block envelopes, cutoffs and precision. Outputs:
full h,l,z transcript, table/FFT cost, rare-branch loss, sampler error,
preparation/sample counts and source IDs. Private coefficient assignments
must stay hidden from the simulated decoder.

Regression controls should compare joint laws, deficient-rank maps, complex
envelopes, cutoff zeros, Pauli/linear corrections, measured rejection and
multiple trials. A nonlinear F or growing entangled block must fail the
certificate's premises rather than receive an automatic dequantized flag.
Store negative results with the exact operation family and q-scaling premise.

Keep the Wigner diagnostic separate: report signed norm, estimator sample
bound and numerical error. Negativity is not an advantage flag; exponential
signed cost is not a hardness proof. A positive-Wigner certificate must
check positivity. Full tests and live registry workflows belong to Gemini's
implementation pass; these notes do not promote proof status automatically.

Main-model work should target a coherent transformation of the native
Gaussian fibers that prevents the measurement-order factorization, with
explicit useful decoding action and cost. Adaptive changes of basis and
nonlocal operations are possible directions; their presence alone does
not solve Gaussian preimage erasure. Preserve the prior-aware L1 track
and benchmark every proposal against attacks on original classical samples.
