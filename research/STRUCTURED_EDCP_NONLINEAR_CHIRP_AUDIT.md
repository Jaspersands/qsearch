# Structured EDCP: Nonlinear Shears And Modular Quadratic Readout

Date: 2026-09-27. LOCAL DERIVATION / REVIEW PENDING.

No novelty, independent proof verification, efficient secret decoder, or
quantum speedup is claimed. These are scoped mathematical comparisons for
the actual direct-phase source, not a new oracle family. Gemini owns
production implementation and routine full-suite execution.

FOLLOW-UP (2026-09-28): `STRUCTURED_EDCP_POLYNOMIAL_LIFT_AUDIT.md` treats
coherent reuse as a phase program, quantifies legitimate approximate
quadratic kickback, and audits the uniform-amplitude promise behind
published polynomial phase linearization. It distinguishes observable
envelope coherence from actual hidden-secret information.

## 1. Research Decision

Four tempting decoder components now have explicit adversarial controls:

1. A nonlinear controlled addition followed by Fourier measurement of its
   target leaves a KNOWN outcome-dependent phase, not the purported hidden
   nonlinear phase. The identity holds for any product input.
2. A global quadratic phase followed by Fourier readout has an efficient
   classical sampler under an explicit finite-modulus alias bound. This
   includes weak curvature AND fast small-denominator quadratic cores with
   weak residual curvature. Entanglement alone does not escape this test.
3. For a nonnegative coefficient envelope, ANY diagonal phase fails to
   improve a fixed affine secret estimate from the Fourier outcomes over
   the corresponding unmodified source. This is exact and does not require
   the alias bound, Gaussianity, or a quadratic phase.
   More generally, a fixed affine estimate after an explicit normalizer
   circuit has a constructible local-Fourier estimator with at least the
   same ideal success, under the signal-gain condition below.
4. Quadratic phases in the TOTAL frequency f(c) have a separate classical
   comparison using the existing overlap bound. This includes strong phases
   that fail the weak-curvature test and can erase secret information.

None excludes general coherent processing, nonlinear decoding of measured
data, or all modular quadratic circuits. Failure of a sufficient sampler
bound is not evidence of quantum advantage. The remaining proposal must
specify both an operation outside these scopes and a useful decoding effect.

## 2. Nonlinear Shear: The Hidden Phase Cancels

Let x in Z_Q^a and z in Z_Q^b have product input psi_S(x)*psi_R(z).
Let F:Z_Q^a -> Z_Q^b be any known function. It need not be linear or
injective; (x,z) -> (x,z+F(x)) is reversible regardless. Fourier-transform
and measure the target with the negative-sign convention. For outcome y,
the unnormalized control vector is exactly

    hat_psi_R(y) * psi_S(x) * exp(-2*pi*i*y dot F(x)/Q).       (1)

Indeed, change variables from z+F(x) back to z in that Fourier sum.
The outcome law is |hat_psi_R(y)|^2. Multiplication by the known opposite
phase restores psi_S. Thus this instrument is equivalent to local Fourier
measurement of R followed by a known y-controlled operation on S.

For psi_R(z)=g_R(z)*exp(2*pi*i*s*b dot z/Q), writing the shifted state
first seems to introduce -s*b dot F(x). The shifted Gaussian Fourier sum
contributes the cancelling term. Keeping only the former is incorrect.
The residual coefficient in (1) is y, not the hidden s*b. The statement
covers negacyclic squaring, arbitrary polynomial F, and nonpolynomial F.

This does NOT simulate arbitrary subsequent quantum computation on S.
Keeping the target coherent, using correlated inputs, or applying further
joint gates before its measurement falls outside (1). Selecting a rare y
must retain its Born probability. Known y-dependent nonlinear phases can
still be useful operations; they just do not manufacture a new secret.

## 3. Exact Affine-Readout Domination

Let G=Z_Q^D, v public, and g(c)>=0 with sum_c g(c)^2=1. Start from

    psi_s(c)=g(c)*exp(2*pi*i*s*(v dot c)/Q).

Add ANY known diagonal phase exp(i*phi(c)), Fourier-measure all coordinates
to p, and estimate s by w dot p-b mod Q. The public w,b are selected BEFORE
this measurement, and w dot v=1 mod Q. A unit coefficient w dot v can be
rescaled to this normalization. Then, for every s and every phi,

    Pr_phi[w dot p-b=s]
      <= Pr_no_phase[w dot p=s]
       = (1/Q)*sum_(r in Z_Q) sum_c g(c+r*w)*g(c).            (2)

Proof: Fourier-expand the indicator w dot p=s+b. The secret phase cancels
because w dot v=1, leaving

    (1/Q)*sum_r exp(-2*pi*i*r*b/Q)
       *sum_c g(c+r*w)*g(c)*exp(i*(phi(c+r*w)-phi(c))).

The absolute-value triangle inequality gives (2), attained by phi=0,b=0.
This proves a probability comparison, not a classical simulator. It also
does not say that the right-hand side is large or efficiently maximized
over w. Input-dependent but public choices of w and independent classical
randomization are allowed. Choices of w based on the SAME Fourier outcomes,
nonlinear estimators, preceding non-diagonal operations, and conditional
postselection are not included. Multiple diagonal gates before that QFT
combine into a single phi and do not escape the result.

Nonnegativity matters. An already chirped uniform envelope on Z_5 has
uncorrected zero-outcome probability 1/5; undoing its chirp gives probability
1. The native Gaussian envelope is nonnegative, but intermediate states
in a general circuit need not retain that property.

### Extension: Arbitrary Explicit Normalizer Circuits, Affine Output Only

This is a success-probability comparison, NOT a simulation of Gaussian-input
normalizer circuits. Let U be any explicitly described finite normalizer
circuit on Z_Q^D: arbitrary interleavings of partial QFTs, invertible linear
coordinate maps and valid quadratic phases. Fourier signs are fixed above.
Measure U*psi_s in the computational basis and form Y=w dot p. Classical
Pauli propagation through U computes a,b,gamma such that

    U^dagger * Z_w * U = gamma*Z_b*T_a,
    (Z_b*f)(c)=exp(2*pi*i*b dot c/Q)*f(c), (T_a*f)(c)=f(c+a).

The definition of T_a is important: on basis kets it translates by -a.
Let eta=v dot a. Fourier expansion of the event Y=eta*s+b0 gives

    Pr_U[Y=eta*s+b0]
       <= (1/Q)*sum_r sum_c g(c+r*a)*g(c)
        = Pr_local_Fourier[a dot P=eta*s].                  (2a)

Proof: (gamma*Z_b*T_a)^r is a unit-modulus diagonal function times T_(r*a).
Its expectation on psi_s has the factor exp(2*pi*i*eta*s*r/Q). The event
character cancels it, and the triangle inequality gives (2a). All phases,
including even-modulus Pauli phases, remain in the expectation before
taking this bound. An arbitrary initial known diagonal phase on g is also
allowed: its difference contributes only another unit-modulus factor.

If eta is a unit, rescale both outputs by eta^(-1) to compare exact secret
recovery. In particular, when eta=1, the ordinary local-Fourier estimate
a dot P is at least as successful as w dot p-b0 after the whole circuit.
For nonunit eta this only compares the linear FEATURE eta*s, not full
secret recovery. Pauli propagation obtains a from the public gate list in
polynomial time; no search for the best a is needed to match this circuit.
Its gate-list construction cost must still be charged.

This comparator consumes local Fourier DATA. It is not a classical attack
on a standalone phase-state oracle unless a lawful classical sampler for
that data is independently supplied, as in our retained-input source.

This excludes a larger computational claim than (2), without assuming
stabilizer inputs. Nonlinear output functions, intermediate measured and
adaptively selected circuits, quantum generation of a gate description,
and nonnormalizer operations between Fourier stages remain outside scope.
It also does not compare full output distributions or simulate a later
quantum algorithm. The existing finite normalizer simulation theorem is
not being used to justify Gaussian-input simulation.

For the PHYSICAL retained-input problem, do not silently replace its tags
by s*v. If the full unconditioned forward cq contract INCLUDING the secret
reference is within Delta_src of the ideal source, the two transfers give

    success_quantum_physical <= success_classical_physical
                           +2*Delta_src+delta_classical+delta_quantum.

Here the implementation deltas cover the matched readout sampler and
quantum circuit, respectively. Rejection/conditioning losses remain in
Delta_src's contract. A constant error does not exclude an arbitrarily
small advantage. Without that joint source guarantee, (2a) remains an
ideal-source comparison only.

## 4. Finite-Modulus Quadratic Sampler

Use the normalized product PERIODIZED amplitude

    g_Q(c) proportional to sum_(m in Z^D)
                               exp(-pi*||c+Q*m||^2/sigma^2),
    psi_k(c)=g_Q(c)*exp(2*pi*i*k dot c/Q), k in Z_Q^D.

Apply exp(2*pi*i*c^T*T*c/Q), where T is an integer upper-triangular matrix,
then Fourier-measure. This parametrizes integer-coefficient quadratic
polynomials, including odd cross coefficients at even Q. Symmetrizing T
can introduce HALF-INTEGER off-diagonal entries; do not round them away.
This is not asserted to enumerate every abstract quadratic function on
every finite group.

Choose a VERIFIED divisor t of Q and an integer upper-triangular U. Set

    T=(Q/t)*U+V, V integer,
    E=(V+V^T)/Q,
    chi(c)=exp(2*pi*i*c^T*U*c/t),
    A=sigma^(-2)*I-i*E,
    M=Re(A^(-1))=sigma^2*(I+sigma^4*E^2)^(-1),
    H=(Q^2/2)*M^(-1)
      = Q^2/(2*sigma^2)*I+(Q^2*sigma^2/2)*E^2.             (3)

The original phase is chi(c)*exp(pi*i*c^T*E*c). Both factors are
Q-periodic. The choice t=1,U=0 is always available; other t require an
actual divisor, not an uncharged factorization oracle. T,U,E may depend
on public labels. A large or poorly chosen lift can yield a vacuous bound.

The claimed sampler is:

    sample J with law |alpha_j|^2, the Fourier law of chi on Z_t^D;
    independently sample N from D_(Z^D,H);
    output P=k+(Q/t)*J+N mod Q.                             (4)

The convention for D_(Z^D,H) is mass proportional to
exp(-pi*n^T*H^(-1)*n); its continuous analogue has covariance H/(2*pi).
Neither exact discrete covariance equality nor an exact convolution law
with the unchirped discrete Gaussian is assumed.

### Alias Bound

Define the UNCAPPED nonnegative sum

    R_t(M)=sum_(h in Z^D, h!=0)
                        exp(-pi*h^T*M*h/(2*t^2)).           (5)

If R_t(M)<1, the total-variation distance between the exact measured law
and (4) is at most

    delta_alias <= min(1,R_t(M)/(1-R_t(M))).                (6)

For R_t>=1 report the trivial bound 1, not a negative denominator. A
convenient sufficient certificate is obtained from

    m0=sigma^2/(1+sigma^4*||E||_op^2),
    a=pi*m0/(2*t^2), r=2*exp(-a)/(1-exp(-3*a)),
    R_t(M) <= expm1(D*log1p(r)).                            (7)

Use a SOUND upper enclosure of ||E||_op, giving a lower bound on m0.
Compute tiny tails in log space. Floating-point underflow is not an exact
zero error. A bound >=1 is an inconclusive test, not a positive signal.

### Proof Retaining All Coherent Aliases

Let

    alpha_j=t^(-D)*sum_(c in Z_t^D) chi(c)*exp(-2*pi*i*j dot c/t),
    a_E(x)=det(A)^(-1/2)*exp(-pi*x^T*A^(-1)*x).

Parseval gives sum_j |alpha_j|^2=1. Periodicity and Poisson summation give
the exact output amplitude, up to a global common normalization, as

    sum_j alpha_j * sum_(m in Z^D)
                             a_E((p-k)/Q-j/t+m).            (8)

The determinant's square-root choice affects only a common phase. The
incoherent version replaces the squared absolute value of (8) by

    G(p)=sum_j |alpha_j|^2 * sum_m
                            |a_E((p-k)/Q-j/t+m)|^2.         (9)

Its total mass is I=sum_(n in Z^D)|a_E(n/Q)|^2, because k and Q*j/t
are integer grid shifts. Its normalized law is exactly (4).

For two terms whose offsets differ by h/t, completing the real Gaussian
square gives

    sum_(n in Z^D) |a_E(n/Q)|*|a_E(n/Q+h/t)|
      <= I*exp(-pi*h^T*M*h/(2*t^2)).                       (10)

The remaining shifted fine-lattice Gaussian sum is at most its centered
sum: Poisson summation expresses the shift as phases multiplying positive
dual-Gaussian coefficients. This inequality holds for correlated M.

For fixed h, the residues of the two core indices differ by h mod t.
Cauchy--Schwarz gives sum_j |alpha_j*alpha_(j+h)|<=1. Summing (10) over
every nonzero h bounds the total absolute interference by I*R_t(M).
Thus, for F(p)=|expression (8)|^2 and J=sum_p F(p),

    ||F-G||_1 <= I*R_t, |J-I|<=I*R_t, J>=I*(1-R_t).

Normalizing both laws proves (6). Finally M>=m0*I bounds the lattice sum
by a product of scalar theta sums. The elementary tail estimate
sum_(j>=1) exp(-a*j^2)<=exp(-a)/(1-exp(-3*a)) proves (7).
No exponentially many modes need to be enumerated to evaluate that bound.

### Sampling The Quadratic Core Without Enumerating t^D Modes

Put S=U+U^T and K=ker(S mod t). Since S*x=0 on K, the map
chi(x) restricted to K is a character. Expanding |alpha_j|^2 gives

    |alpha_j|^2 = |K|/t^D  if j dot x=x^T*U*x mod t for all x in K,
                 0        otherwise.                     (11)

These constraints specify one affine coset j0+K^perp. Smith normal form
over the integers supplies generators for K and solves the linear
congruences for j0. Character extension guarantees consistency; it must
still be checked in an implementation. Since S is symmetric,
K^perp=image(S), so sample uniform Z in Z_t^D and return j0+S*Z mod t.
For odd t, j0=0 is valid. At even t it need not be: the diagonal example
t=2,U=[1] has J=1 deterministically. Never silently set j0=0 there.

This is polynomial-size integer linear algebra in D and log(t), not
enumeration and not an assumed hidden-subgroup oracle. It is also a case
where finite normalizer simulation DOES apply: the core Fourier problem
starts in the uniform coset state. The full Gaussian input is different.

There is a useful refinement of (5): because this core law is uniform on
an affine coset, sum_j |alpha_j*alpha_(j+h)| is EXACTLY 1 for
h mod t in image(S), and 0 otherwise. One may replace R_t by the sum over
nonzero h in the lattice t*Z^D+S*Z^D. The coarser (7) remains valid.
For a pure-character core S=0 mod t this refined sum is the unchirped
integer-alias sum, with no t penalty. Do not assume that evaluating a
general restricted theta sum is efficient merely because its lattice is
explicit; any improved certificate needs its own justified computation.

### Sampling The Correlated Gaussian

Equation (3) gives H>=Q^2/(2*sigma^2)*I. Choose a public rounding width
tau with H-tau^2*I positive definite. Sample a continuous Gaussian of
width matrix H-tau^2*I, then apply coordinatewise randomized Gaussian
rounding of width tau. Section 3 of
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md` proves the uniform error bound

    epsilon_tau=2*exp(-pi*tau^2)/(1-exp(-3*pi*tau^2)) < 1,
    delta_round <= min(1,expm1(D*(log1p(epsilon_tau)
                                    -log1p(-epsilon_tau)))). (12)

In the native Q/sigma regime, tau=log(D+2) is an available choice. Larger
tau may be chosen for a requested error if the positive-definiteness check
still passes. Finite-bit covariance factorization, continuous sampling,
conditional rounding, and tail truncation require separate error budgets.
Polynomial bit-length and conditioning controls are prerequisites for the
efficient-sampler claim. A merely formal Gaussian sum is not a sampler.

## 5. Strong Frequency-Aligned Phases Are Also Covered

There is a second comparator that does NOT require (7). For any normalized
g, public v, and unit-modulus function chi on Z_Q, multiply the source by
chi(f(c)), f(c)=v dot c. Write

    chi(u)=sum_(j in Z_Q) alpha_j*exp(2*pi*i*j*u/Q),
    alpha_j=(1/Q)*sum_u chi(u)*exp(-2*pi*i*j*u/Q).

For any original phase vector k, the final Fourier amplitude is exactly
sum_j alpha_j*hat_g(p-k-j*v). Compare it to the CLASSICAL mixture

    sample P0 from original local Fourier readout;
    independently sample J with law |alpha_j|^2;
    return P=P0+J*v.                                      (13)

Define nu=|hat_g|^2 and the same uncapped overlap sum as in
`STRUCTURED_EDCP_FOURIER_ERASURE_AUDIT.md`:

    A(v)=sum_(r=1)^(Q-1) sum_p sqrt(nu(p)*nu(p+r*v)).

Both the true measured law and (13) are already normalized. Expanding only
their cross terms and using sum_j |alpha_j*alpha_(j+r)|<=1 gives

    TV(true readout, (13)) <= min(1,A(v)/2).                (14)

This statement is uniform in chi and k. It needs no positivity assumption
on hat_g; bounding A in our Gaussian regime uses the earlier source proof.
For arbitrary chi, efficient classical sampling of J is NOT supplied.
An efficient phase evaluator is not automatically an efficient Fourier-law
sampler. The following important family does have one.

Let chi(u)=exp(2*pi*i*(b*u^2+a*u)/Q). By the scalar form of (11), set

    g0=gcd(2*b,Q), j0=(a+b*(Q/g0)) mod g0.

Then J is uniform on j0+g0*Z_Q: sample R uniformly in
{0,...,Q/g0-1} and output j0+g0*R. This costs polynomially many bit
operations without factoring Q. It covers arbitrary b, including strong
frequency-aligned chirps whose curvature matrix makes (7) vacuous.
For the native even Q with exactly one factor 2, a unit b has g0=2.

The wide-source average A(v)/2 bounds already proved in the erasure note
therefore apply without recomputing a Gaussian approximation: reference
upper values 7.63e-7,8.72e-6,5.45e-7 at d=64,256,1024 with sufficient
L=4,3,3 respectively, before the full source/sampler ledger. These are
LABEL-AVERAGED ideal bounds under that note's label-conditioning contract,
not pointwise guarantees for every v. Source-specific distributions must
be transferred with their actual errors. No expensive core lattice theta
evaluation is needed for this particular aligned family.

The mixture can be actively harmful. For the IDEAL phase-only experiment
k=s*v, uniform s in Z_Q and no extra s-correlated side information, (13)
depends on s only through s mod g0. Thus ANY decoder of its classical
output has exact-recovery probability at most g0/Q. The true final
Fourier readout has probability at most g0/Q+min(1,A(v)/2). More generally,
for a prior pi on s the mixture bound is
sum_(r mod g0) max_(s=r mod g0) pi(s). This does NOT bound an algorithm
also given the original retained RLWE data: those records can already
determine s information-theoretically. It is a diagnostic for this
measurement's secret information, not a cryptographic hardness theorem.

Keeping the Fourier output coherent and subsequently interfering its
peaks is outside (14). Merely appending classical decoding cannot undo
the missing random J in the measured mixture.

## 6. Consequences And Attempts To Falsify Them

### Nontrivial Gates Are Included

For t=1, ||E||_op<=1/sigma^2 gives m0>=sigma^2/2. Disjoint cross-block
pairs with upper-triangular coefficients floor(Q/sigma^2) provide examples.
The phase varies by order one on typical Gaussian coefficients, so the
test is not restricted to gates acting nearly as the identity. Nevertheless,
the readout is approximated by the correlated classical Gaussian in (4).

For a core divisor t and residual ||E||_op<=1/sigma^2, a sufficient regime
is sigma^2/t^2 much larger than log D. The core can be a rapidly oscillating
entangling phase; its many Fourier peaks are efficiently sampled by (11).
An exponentially large SUPPORT does not imply expensive sampling.

### The Naive Continuous Approximation Is False

At Q=101,sigma=8,D=1,T=[101], the exact modular phase is the identity.
Taking t=1,U=0 without reducing this lift gives E=2 and a continuum-based
Gaussian sampler at TV about 0.816869918263 from the actual readout.
Equation (7) is correctly vacuous. The identical gate represented by T=0
has the small unchirped bound. More generally, adding a symmetric integer
matrix with even diagonal to a curvature matrix does not change its phase
exp(pi*i*c^T*E*c) on integer c. Diagonal and cross coefficients have
different periods; all reductions must preserve the actual phase exactly.

The conclusion is NOT that every quadratic phase can be reduced to weak
curvature. Simultaneous useful rational approximation, divisor availability,
and the Gaussian smoothing criterion are genuine restrictions.

### Literature Does Not Supply A Blanket No-Go Theorem

[Van den Nest, normalizer circuits, Theorem 1](https://arxiv.org/pdf/1201.4867)
assumes suitable coset inputs. Our nonconstant Gaussian amplitudes do not
meet that input premise. Applying its abstract's unrestricted-sounding
wording to this source would be an error; only the core problem in (11)
uses the required uniform coset input.

[Bartlett--Sanders--Braunstein--Nemoto](https://arxiv.org/pdf/quant-ph/0109047)
gives continuous-variable Gaussian simulation under quadratic dynamics and
the specified measurements. It does not discard digital modular aliases
for us. Equations (5)-(10), including their vacuous cases, are the additional
finite-grid argument needed here. Neither source proves the new scoped
claims in this note; those remain local derivations requiring review.

## 7. Source Access And Composition

For ideal EDCP, k=s*v is hidden. Giving (4) that k would not be a legal
classical attack. Instead use the repository's RETAINED classical source:
sample the same allowed fresh selectors u_l, construct the same public
labels a_l=u_l*A and internally known tags t_l=u_l*b, and set
k_(l,i)=q^i*t_l mod Q. These are exactly the frequencies of the physical
direct-phase product states. Do not reveal selectors or tags to the decoder.
This simulator uses the same original input, not a new evaluation oracle.

The bound is uniform in k, hence also applies to this mixture and its
retained classical labels. Charge periodized-versus-prepared coefficient
state error, (6), (12), and all numerical/QFT implementation errors. When
transferring a claim to the ideal s*v ensemble, additionally use the FULL
forward source contract, with its rejection flags and conditioning losses.
Do not replace it by the phase-error budget alone or grant an ideal secret
to the sampler. See `STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md` and
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md` for the source distinctions.

The theorem describes one final measured law, not a quantum-state sampler
or arbitrary adaptive normalizer circuit. For a y-dependent chirp after
(1), condition on y, check the residual input and branchwise criterion,
and average errors using the TRUE outcome law, including bad branches.
Fourier outcome y is typically not a small curvature coefficient. Assuming
the criterion without checking it would erase the potentially hard case.
Postselection also needs an explicit error/acceptance calculation.

## 8. Targeted Checks Performed

These finite arrays check the algebra, not asymptotic algorithm performance.
No candidate was accepted, benchmark promoted, or routine suite run.

- 24 nonlinear-shear complex-amplitude controls at (Q,D)=(5,1),(10,1),
  (5,2),(10,2), for Gaussian and arbitrary complex product inputs, scalar
  quadratic maps and negacyclic squaring. Maximum amplitude residual
  2.62e-16. Marginals and known-phase cancellation were also checked.
- A Q=17 Gaussian control for the alleged hidden quadratic phase gives
  trace distance 0.486322272305 from the true outcome-zero residual state.
- 80 affine-readout domination checks at Q=5,6,7,10 with arbitrary positive
  envelopes and phases. The unmodified orbit identity residual was at most
  6.67e-16. The complex-envelope countercontrol gives 1/5 versus 1.
- 80 further full-matrix normalizer comparisons at Q=5,6,7,10 in dimension
  two, with nine random partial-Fourier, quadratic/linear-phase and shear
  gates. Both Gaussian and arbitrary positive envelopes were used. The
  extracted translated-Pauli residual was at most 3.90e-15 and no affine
  success-domination violation exceeded the 2e-11 test tolerance. Circuits
  were selected for unit signal gain (169 attempts for 80 controls); this
  is a premise check, not a research candidate acceptance experiment.
- 135 quadratic-core character/support checks at t=2,3,4,5,6,8,9,10,12
  in dimensions 1,2,3, including degenerate and even-modulus forms. Maximum
  probability residual 2.78e-16; support size times |K| equals t^D exactly.
- Forty frequency-aligned mixture controls for quadratic and arbitrary
  phases at (Q,D,sigma)=(7,1,2),(10,2,3),(17,2,4),(17,3,5),(31,3,6).
  All satisfy (14). Quadratic controls also check the exact scalar gcd
  support and the uniform-secret optimal-decoder bound. For example,
  Q=31,D=3,sigma=6,b=25 gives measured TV 0.0426516 against overlap bound
  0.0691760, and optimal recovery 0.0366118 against bound 0.1014341.
  These small reference cases do not establish the growing-regime bound.
- Twelve full finite FFT versus Gaussian-mixture comparisons, with integer
  phase residues evaluated BEFORE complex exponentiation. Selected rows:

| Q | D | sigma | t | U; V (upper triangular) | observed TV | bound (6)-(7) |
|---:|---:|---:|---:|---|---:|---:|
| 31 | 1 | 3 | 1 | 0; 1 | 1.73083e-5 | 5.12179e-5 |
| 101 | 1 | 3 | 1 | 0; 1 | 1.52097e-6 | 2.24048e-6 |
| 120 | 2 | 5 | 2 | [[0,1],[0,0]]; 0 | 1.08602e-4 | 2.18023e-4 |
| 120 | 2 | 5 | 2 | [[0,1],[0,0]]; [[1,1],[0,-1]] | 3.96201e-4 | 1.25705e-3 |
| 126 | 2 | 9 | 3 | [[1,1],[0,0]]; 0 | 9.66294e-7 | 2.89980e-6 |
| 126 | 2 | 9 | 3 | [[1,1],[0,0]]; [[1,0],[0,0]] | 3.08113e-3 | 1.98848e-2 |

The Gaussian reference sums used an eight-width spectral-radius box;
these are numerical checks, not interval-certified tail/error guarantees.
A separate 85-digit scalar check at Q=101,sigma=6,T=[1] gives
TV 3.09062971095165514836e-17 below the bound 1.04081456248519968057e-16.
Its nine-width sum and mass residual 5.64e-86 are numerical references,
not formal enclosures. Double precision cannot validate that tiny bound.
The unreduced identity countercontrol's large TV must remain in the suite.

## 9. Next Theory And Gemini Contract

Gemini should extend the existing direct-phase comparator, not create a
new circuit-search subsystem. Preserve these concrete obligations:

1. Record the original integer T, verified t|Q, integer U,V, and exact
   phase equivalence. Never silently identify half-integer symmetric
   entries with rounded integer entries or assume factoring is free.
2. Verify (11) with even and composite moduli. Generate the affine support
   by modular linear algebra; production code must not enumerate t^D.
3. Enclose the spectral/tail and rounding bounds, keep an uncapped R_t,
   and distinguish certified-small, vacuous, and numerical-reference-only.
4. Use actual retained-source tags internally and preserve the complete
   source, numerical, rejection, and conditional-error ledger.
5. Keep the wrong-hidden-phase, complex-envelope, and unreduced-identity
   countercontrols. Assert (2) only for its positive-envelope, fixed-affine
   output class; assert (6) only for final Fourier measurement.
6. Add the frequency-aligned comparator (13)-(14) and scalar gcd sampler.
   Do not turn arbitrary chi's formal Fourier expansion into an assumed
   sampler. Distinguish label-average error from a pointwise certificate,
   and phase-only information loss from the retained-input decoding task.
7. Propagate the final affine observable through explicitly specified
   normalizer circuits, verify its signal gain, and compare the resulting
   local-Fourier estimator by (2a). This is success domination, not a
   distribution simulator. Charge BOTH ideal/physical source transfers.

The next main-model target should be a CONCRETE coherent cross-block
operation or non-affine decoder, not more wrappers around linear readout.
Fast modular alias interference beyond (7) remains open, but it needs a
secret-recovery consequence and charged computational cost, not merely a
hard-looking output distribution. A quantum solver on classical noisy
linear data is also a valid target; calling its input quantum does not
implement that solver. Independent review of these new bounds is still
required before registry proof-status promotion.
